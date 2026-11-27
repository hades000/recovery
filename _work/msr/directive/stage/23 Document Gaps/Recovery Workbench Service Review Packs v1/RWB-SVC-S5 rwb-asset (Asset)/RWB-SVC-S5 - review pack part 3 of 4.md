# RWB-SVC-S5 rwb-asset (Asset) - review pack, part 3 of 4 (RWB-S5-E4025-APP to RWB-S5-E4033-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 17 |
| Resolved in the stories | 429 |
| Cross-document (pending in another document) | 242 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 24 |
| Register gaps linked | 84 |
| Unconfirmed assumptions | 0 |
| Lint findings | 17 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S5-E4025-APP | 32 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4025 APP Accept a bid below the floor with a second signature v2.md |
| RWB-S5-E4025-CON | 21 | 8 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4025 CON Accept a bid below the floor with a second signature - contract v2.md |
| RWB-S5-E4026-APP | 29 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4026 APP Re-list on no bid v2.md |
| RWB-S5-E4026-CON | 19 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4026 CON Re-list on no bid - contract v2.md |
| RWB-S5-E4027-APP | 31 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4027 APP Enforce the five-day payment term v2.md |
| RWB-S5-E4027-CON | 25 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4027 CON Enforce the five-day payment term - contract v2.md |
| RWB-S5-E4028-APP | 29 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4028 APP Transfer vehicle registration v2.md |
| RWB-S5-E4028-CON | 17 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4028 CON Transfer vehicle registration - contract v2.md |
| RWB-S5-E4029-APP | 28 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4029 APP Record a property transfer at the Land Office v2.md |
| RWB-S5-E4029-CON | 18 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4029 CON Record a property transfer at the Land Office - contract v2.md |
| RWB-S5-E4030-APP | 32 | 24 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4030 APP Apply proceeds and raise the shortfall v2.md |
| RWB-S5-E4030-CON | 22 | 20 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4030 CON Apply proceeds and raise the shortfall - contract v2.md |
| RWB-S5-E4031-APP | 31 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4031 APP Transfer a pool to RAMC or the joint venture v2.md |
| RWB-S5-E4031-CON | 20 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4031 CON Transfer a pool to RAMC or the joint venture - contract v2.md |
| RWB-S5-E4032-APP | 20 | 21 | 7 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4032 APP Arrange a customer buy-back v2.md |
| RWB-S5-E4032-CON | 28 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4032 CON Arrange a customer buy-back - contract v2.md |
| RWB-S5-E4033-APP | 27 | 17 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4033 APP Rent a held asset to a third party v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S5-E4025-APP | R-02552 | CG-ALL-10041 | Script gap | Product owner | The story adds SALE_AGREED to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4028-APP | R-02569 | CG-ALL-10124 | Script gap | Product owner | The story adds TITLE_TRANSFER_PENDING to the closed list LOV-ASSET-TYPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4028-APP | R-02570 | CG-ALL-10125 | Script gap | Product owner | The story adds TITLE_TRANSFER_PENDING to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4030-APP | R-02583 | CG-ALL-10176 | Script gap | Product owner | The story adds PROCEEDS_APPLIED to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4030-APP | R-02584 | CG-ALL-10177 | Script gap | Product owner | The story adds SHORTFALL_RAISED to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4033-APP | R-02599 | CG-ALL-10246 | Script gap | Product owner | The story adds RENTAL_ACTIVE to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E4025-APP | R-12906 | CG-ALL-10054 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4026-APP | R-12916 | CG-ALL-10079 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4027-APP | R-12929 | CG-ALL-10106 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4028-APP | R-12940 | CG-ALL-10136 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4029-APP | R-12951 | CG-ALL-10162 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4030-APP | R-12961 | CG-ALL-10187 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4031-APP | R-12970 | CG-ALL-10208 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4033-APP | R-12993 | CG-ALL-10258 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3028-APP, RWB-S5-E3028-CON, RWB-S5-E4025-APP, RWB-S5-E4025-CON | R-23503 | GAP-1763 | Register gap | Risk with the product heads | The floor approval ladder is named in amounts and percentages whose comparison signs cannot be read | Read every floor limit from the versioned delegation table of rwb-access at run time, carry the three amounts and the three percentages as stated, and treat the direction of the test as open until DL18 and Q-001 answer. |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-23539 | GAP-2941 | Register gap | Business analyst of the Asset module with the business lead | R-DIS-53, the rejected transfer that blocks the title, sits in the state of this rule and is owned by no criterion and no story of the split | Leave the rejection out of this slice, name R-DIS-53 and its TITLE_BLOCKED state in the out-of-scope list of both stories, and open a story for it in the next realignment pass rather than inventing a criterion or a message now. |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-29180 | GAP-2937 | Register gap | Business lead of the Asset module with the solution architect of S5 | The Land Office transfer has no interface, no integration id and no operation, and the officer's registration has no published write surface | Keep the Land Office as a person and officer step outside every service, carry the registration as the TITLE_REGISTERED signal of the case task, and declare no interface, no file, no operation and no X row for it. |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-29182 | GAP-2943 | Register gap | Solution architect and the business owner of the Asset module | The FSD S5, the TSD S5 and the Epics 3 to 8 Specification that the two slices read are in review with empty sign-off tables and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the signatures; nothing in the build waits on them. |
| RWB-S5-E4031-APP, RWB-S5-E4031-CON | R-29198 | GAP-2958 | Register gap | Solution architect and the business owner of the Asset module | The FSD S5, the TSD S5 and the Epics 3 to 8 Specification the two slices read are in review with empty sign-off tables and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status change. |
| RWB-S5-E4032-APP, RWB-S5-E4032-CON | R-29199 | GAP-1926 | Register gap | Owner of rwb-access with the sales business owner | The FSD lists the customer as an also-user of the feature and the rights matrix has no customer role | Represent the former owner by the sale officer acting on the case and carry the former owner as a party key the owner's contract answers; add no customer role, no customer screen and no external edge in this story. |
| RWB-S5-E4023-APP, RWB-S5-E4023-CON, RWB-S5-E4031-APP, RWB-S5-E4031-CON | R-38441 | ASM-4802 | Register assumption |  | Both stories carry Status Draft (realignment v1) and the missing approval of the realigned stories and of the FSD S5, the TSD S5 and the Epics 3 to 8 Specification they read is treated as an assumption of this run rather than as a blocker; no behaviour and no value of either story depends on a signature and no status of a source document is changed. | The verification loop collects the sign-offs and only then changes the status of the stories. |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-38472 | ASM-4833 | Register assumption |  | The Land Office stays a person and officer step outside every service: the officer records the registration on the case task, it enters the service as the TITLE_REGISTERED signal of AssetDisposalWorkflow, and no interface, file, operation or X row is declared for it. | Business lead of the Asset module and the solution architect of S5 at the contract tag |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-38476 | ASM-4837 | Register assumption |  | R-DIS-53, the rejected transfer and its TITLE_BLOCKED state, is out of scope of both slices until a story owns it; no criterion, message or task is invented for it now. | Business analyst of the Asset module at the next realignment pass |
| RWB-S5-E4029-APP, RWB-S5-E4029-CON | R-38478 | ASM-4839 | Register assumption |  | Both stories stand at Status Draft (realignment v1) and the missing approvals of FSD S5 v3, TSD S5 v2 and the Epics 3 to 8 Specification v3 are recorded rather than waited for. | Solution architect and the business owner of the Asset module in the verification loop |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S5-E4025-CON | R-08306 | DOR-RWB-S5-E4025-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source documents. Grep for 'epic design' only hit _work/msr scratch files. Recording a sign-off would invent it. |
| RWB-S5-E4026-APP | R-20385 | DOR-RWB-S5-E4026-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Personal-data fields flagged by detcheck are not named in the chunk, the story text, or the 22 Microservice Realignment folder (no match for the item). Cannot correct the statement without inventing fields. |
| RWB-S5-E4027-CON | R-20417 | DOR-RWB-S5-E4027-CON-4 | 7 and 16 (not in chunk) | Definition of Ready item 4 Business rules: Partial | New AC and TC rows for BR1-4 and BR7-10 need the text of sections 7 and 16, which are not in this chunk. No anchor exists, so no edit was made. |
| RWB-S5-E4028-CON | R-08342 | DOR-RWB-S5-E4028-CON-23 | header | Definition of Ready item 23 Contract version fixed: Fail | Major v1 is taken from path /api/recovery/asset/v1; minor and patch are not in sources, so DOR-23 stays open. |
| RWB-S5-E4028-CON | R-08343 | DOR-RWB-S5-E4028-CON-3 | 7 | Definition of Ready item 3 Acceptance criteria: Fail | Renaming to AC1-AC9 broke trace against section 16 (C1-C9) and the PRD row (C1); reverted. Item stays open until section 16 is edited with the rename. |
| RWB-S5-E4028-CON | R-20434 | DOR-RWB-S5-E4028-CON-15 | header | Definition of Ready item 15 INVEST: Partial | Size is not in the sources (DOR-16); the row carries the not-specified placeholder, so no fits-two-weeks claim is made. |
| RWB-S5-E4029-APP | R-20441 | DOR-RWB-S5-E4029-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Item names no field and section 11 text is not in this chunk. Story says no personal data (BR10, line 381). Field cannot be identified without the Data Classification v5 list. |
| RWB-S5-E4030-APP | R-20458 | DOR-RWB-S5-E4030-APP-11 | 16 (AC5), 9, 6 (BR10 line) | Definition of Ready item 11 Guardrails: Partial | The P2 personal-data field named by detcheck is not in the checks folder or the story. Without it the no-personal-data lines (BR10, section 9 'No personal data' line, AC5) cannot be corrected. Left unchanged. |
| RWB-S5-E4031-CON | R-32755 | NEWAC-RWB-S5-E4031-CON-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so AC8 and its TC row cannot be placed. Proposed test is Not specified in the source documents (NEWAC-RWB-S5-E4031-CON-AC8); no test invented. |
| RWB-S5-E4032-APP | R-08378 | DOR-RWB-S5-E4032-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design sign-off in the story or sources (Grep 'epic design sign-off/record'). No value to write. Needs the epic design record. |
| RWB-S5-E4032-APP | R-08382 | DOR-RWB-S5-E4032-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | No contract version found in the story or sources. The file revision v2 is not a contract version. Needs the version from RWB-S5-E4032-CON. |
| RWB-S5-E4032-APP | R-20498 | DOR-RWB-S5-E4032-APP-20 |  | Definition of Ready item 20 Reference data: Partial | PLT Platform v1 line 122 names P3 rwb-case parameters and reference data (DP-06, DP-07) but no parameter names. Section text not in this chunk. |
| RWB-S5-E4032-APP | R-23555 | GAP-1925 | 7, 16 | Legacy AC1 gives no from state while the buy-back rule starts at ROUTE_WITH_APPROVER and the asset is held | AC1 (section 7) and its test row (section 16) are not in this chunk, so there is no exact old text to copy. Needs those sections. |
| RWB-S5-E4032-APP | R-23560 | GAP-2962 | 7 | Legacy AC1 gives no from state while R-DIS-24 starts at ROUTE_WITH_APPROVER, and the criterion's screen action has no state of its own | AC1 text (section 7) is not in this chunk, so there is no exact old text to copy. Needs section 7 to read AC1 from ROUTE_WITH_APPROVER. |
| RWB-S5-E4032-APP | R-23561 | GAP-1938 | 7, 16 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule and state sit outside the rule table of the slice | Criteria (section 7) and rule rows (section 16) are not in this chunk, so there is no exact old text to copy. Needs those sections. |
| RWB-S5-E4032-APP | R-23562 | GAP-2968 | 7, 16 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule has no criterion of the key | Criteria (section 7) and rule-table rows (section 16) are not in this chunk, so there is no exact old text to copy. Needs those sections. |
| RWB-S5-E4033-APP | R-02604 | CG-ALL-10254 | 12.5 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | L37 still names namespace rwb-recovery; outside this chunk, so the item is not yet resolved. |
| RWB-S5-E4033-APP | R-12994 | CG-ALL-10259 | 12.8 | Criteria and test data read ACE views directly | AC3 Given lines are in section 7, not in this chunk. Section 12.8 already has the rwb-source-data fake with a GAP-1934 placeholder. Nothing else to edit here. |
| RWB-S5-E4033-APP | R-20518 | DOR-RWB-S5-E4033-APP-2 | 18 | Definition of Ready item 2 Links: Partial | The 12-row count is not reproduced; the table has four requirement rows, so the item is not resolved. |
| RWB-S5-E4033-APP | R-23565 | GAP-1934 | 12.5 | The rental element, the consumed operation names and the ATS interface are not specified in the source documents | Rental property names, types and flags are not in the sources (GAP-1934 a). 12.5 already has the rwb-comms notice request and placeholders, and no ATS operation or fake exists. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (31)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18052 | RWB-S5-E4025-APP | CG-ALL-10045 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the provider named in the Document Index service table. |
| CDC-18053 | RWB-S5-E4025-APP | CG-ALL-10046 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider named in the Document Index service table. |
| CDC-18057 | RWB-S5-E4025-APP | DOR-RWB-S5-E4025-APP-8 | find it | Declare REST bases for /api/recovery/source-data/v1 and /api/recovery/case/v1, and message IDs for HTTP 400, 401, 404 and 409. |
| CDC-18065 | RWB-S5-E4025-CON | CG-ALL-10059 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for P1 rwb-source-data. |
| CDC-18066 | RWB-S5-E4025-CON | CG-ALL-10060 | 12.2 | Declare the REST base /api/recovery/case/v1 for P3 rwb-case. |
| CDC-18067 | RWB-S5-E4025-CON | DOR-RWB-S5-E4025-CON-8 | 12.2 | Declare the REST bases /api/recovery/source-data/v1 and /api/recovery/case/v1 so the contract detcheck passes. |
| CDC-18073 | RWB-S5-E4026-APP | CG-ALL-10070 | 12.2 | Declare the REST base /api/recovery/source-data/v1 from the Document Index service table. |
| CDC-18074 | RWB-S5-E4026-APP | CG-ALL-10071 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-18078 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-8 | 14 | Give the base /api/recovery/source-data/v1 and /api/recovery/case/v1 in the yaml (CG-ALL-10070, CG-ALL-10071). Task queue rwb-asset in rwb-recovery is already set in the story. |
| CDC-18088 | RWB-S5-E4026-CON | CG-ALL-10084 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the asset and valuation data product. |
| CDC-18089 | RWB-S5-E4026-CON | CG-ALL-10085 | 12.2 | Declare REST base /api/recovery/case/v1 for the case family. |
| CDC-18102 | RWB-S5-E4027-APP | CG-ALL-10098 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider |
| CDC-18116 | RWB-S5-E4027-CON | CG-ALL-10113 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case read GET /cases/{caseId} family. |
| CDC-18125 | RWB-S5-E4028-APP | CG-ALL-10128 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case GET /cases/{caseId} family. |
| CDC-18126 | RWB-S5-E4028-APP | CG-ALL-10129 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the rwb-source-data product. |
| CDC-18130 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-8 | 12.2 | Declare the two REST bases; assign message IDs to the 400, 401, 404 and 503 errors in section 14 (not specified in source documents). |
| CDC-18138 | RWB-S5-E4028-CON | CG-ALL-10142 | 12.2 | Declare REST base /api/recovery/case/v1 for the case service (P3 rwb-case). |
| CDC-18139 | RWB-S5-E4028-CON | CG-ALL-10143 | 12.2 | Declare REST base /api/recovery/source-data/v1 (P1 rwb-source-data). |
| CDC-18141 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-8 | 12.2, 12.5 | Declare REST bases /api/recovery/case/v1 and /api/recovery/source-data/v1. |
| CDC-18151 | RWB-S5-E4029-APP | CG-ALL-10155 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |
| CDC-18152 | RWB-S5-E4029-APP | CG-ALL-10156 | 12.2 | Declare REST base /api/recovery/document/v1 for the rwb-document provider, taken from the Document Index service table. |
| CDC-18162 | RWB-S5-E4029-CON | CG-ALL-10167 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases/{caseId} family (read) of P3 rwb-case, taken from the Document Index service table. |
| CDC-18163 | RWB-S5-E4029-CON | CG-ALL-10168 | 12.2 | Declare REST base /api/recovery/document/v1 for the custody release of P5 rwb-document, taken from the Document Index service table. |
| CDC-18173 | RWB-S5-E4030-APP | CG-ALL-10181 | 12.2 | Declare the REST base /api/recovery/case/v1 for the case provider. Story path in 12.2 is already correct. |
| CDC-18197 | RWB-S5-E4030-CON | CG-ALL-10192 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases/{caseId} family (rwb-case), taken from the Document Index service table. |
| CDC-18199 | RWB-S5-E4030-CON | DOR-RWB-S5-E4030-CON-8 | 12.5 | Declare REST base /api/recovery/case/v1 (see CG-ALL-10192). Queue, workflow ID/start rule and applyProceeds parts are handled in this story or catalog. |
| CDC-18217 | RWB-S5-E4031-APP | CG-ALL-10203 | 12.2 | Declare REST base /api/recovery/case/v1 for the case service (rwb-case, P3) |
| CDC-18277 | RWB-S5-E4033-APP | CG-ALL-10250 | 12.2 | Declare REST base /api/recovery/payment/v1 for the payment provider, taken from the Document Index service table. |
| CDC-18278 | RWB-S5-E4033-APP | CG-ALL-10251 | 12.2 | Declare REST base /api/recovery/case/v1 for the case provider, taken from the Document Index service table. |
| CDC-18279 | RWB-S5-E4033-APP | CG-ALL-10252 | 12.2 | Declare REST base /api/recovery/case/v1 for the case provider, taken from the Document Index service table. |
| CDC-18280 | RWB-S5-E4033-APP | CG-ALL-10253 | 12.2 | Declare REST base /api/recovery/comms/v1 for the comms provider, taken from the Document Index service table. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (24)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18058 | RWB-S5-E4025-APP | CG-ALL-10042 | 8; 11 | Add bid_amount to the listing or round entity in LDM v9 Fields, or name the dictionary field the rules use in R-DIS-41. |
| CDC-18059 | RWB-S5-E4025-APP | CG-ALL-10043 | 8; 11 | Add second_signature_by to the approval entity in LDM v9 Fields, or name the dictionary field that records the second signature in R-DIS-42. |
| CDC-18063 | RWB-S5-E4025-APP | DOR-RWB-S5-E4025-APP-7 | 11 | Confirm or map DF-COL-028 and DF-COL-042 for the asset extension, or confirm them against TSD S5 T3.1; the names bid_amount, second_signature_by and decision_record are not LDM v9 or Data Classification v5 fields and stay flagged. |
| CDC-18079 | RWB-S5-E4026-APP | CG-ALL-10068 | 8 | Add the re-list count as a field, or record the object that holds it (index, library table, flag), for RWB-S5-E4026-APP. Owner role Data. |
| CDC-18084 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-7 | 11 | Legacy criteria note now states the decision log to decision record term change (CG-ALL-10080); no other wording change. |
| CDC-18106 | RWB-S5-E4027-APP | CG-ALL-10095 | 8 | Add the payment due date element, or record the object (index, library table or flag) that holds it, under its dictionary name; no such name is in the sources (Not specified in the source documents (CG-ALL-10095)). R-DIS-48 cites payment_due_date. |
| CDC-18107 | RWB-S5-E4027-APP | CG-ALL-10096 | 12.7 | Record decision_record as a PLT library object in rwb_asset (DP-03), or give it the dictionary name. |
| CDC-18108 | RWB-S5-E4027-APP | CG-ALL-10097 | 12.7 | Record payment_match as the P8 table it names, or give it the dictionary name. |
| CDC-18113 | RWB-S5-E4027-APP | DOR-RWB-S5-E4027-APP-7 | 11 | Add DF-COL-028 and DF-COL-042 to the asset entity field IDs. |
| CDC-18131 | RWB-S5-E4028-APP | CG-ALL-10126 | 4 | Name the dictionary field for holding_status on asset (LOV-HOLDING) or record the object in the owning document; it is in neither LDM v9 Fields nor Data Classification v5 Fields. |
| CDC-18135 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-7 | 7 | Add field IDs DF-COL-028 and DF-COL-042 and confirm the holding_status and decision_record elements against Data Classification v5 |
| CDC-18156 | RWB-S5-E4029-APP | CG-ALL-10153 | 11 | Add field asset.holding_status (entity asset, schema rwb_asset, S5) with the sold value of LOV-HOLDING, or record the holding status object in the owning document. |
| CDC-18160 | RWB-S5-E4029-APP | DOR-RWB-S5-E4029-APP-7 | 11 | Add field IDs DF-COL-028 and DF-COL-042 and the fields holding_status and decision_record, or confirm they are TSD S5 T3.1 and PLT library names. |
| CDC-18179 | RWB-S5-E4030-APP | CG-ALL-10178 | 4, 9, 13 | Record shortfall_amount as a field, or name the dictionary field the story should use. |
| CDC-18180 | RWB-S5-E4030-APP | CG-ALL-10179 | 5, 9 | Record residual_route as a field or route flag in LDM v9 Fields, or give the dictionary name it maps to. |
| CDC-18181 | RWB-S5-E4030-APP | CG-ALL-10180 | 11, 12.7 | Record decision_record as the PLT library table in rwb_asset in LDM v9, or give the dictionary name it maps to. |
| CDC-18206 | RWB-S5-E4030-CON | GAP-2947 | find it | Element request: residual, residual_route and the D9 hand-off as the R-DIS-55 decision-record outcome and case stage outcome; no column added this wave. |
| CDC-18227 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-7 | 11 | Add or correct DF-COL-028 and DF-COL-042, and resolve the names holding_status, asset_id and decision_record in LDM v9 or Data Classification v5. |
| CDC-18251 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-7 | 11 | Confirm or publish field IDs DF-COL-028 and DF-COL-042 for the asset entity so they resolve in LDM v9. |
| CDC-18271 | RWB-S5-E4032-CON | DOR-RWB-S5-E4032-CON-7 | 11 | Publish DF-COL-028 and DF-COL-042 as BR Field IDs in LDM v9, or correct the AssetPage range in section 11. |
| CDC-18285 | RWB-S5-E4033-APP | CG-ALL-10247 | find it | Add field holding_status of entity asset (rwb_asset, DF-COL-041, values per LOV-HOLDING) so the story name resolves. |
| CDC-18286 | RWB-S5-E4033-APP | CG-ALL-10248 | find it | Add collateral_id to the entity that holds it, or confirm it is only the reference identifier named in BR5. |
| CDC-18287 | RWB-S5-E4033-APP | CG-ALL-10249 | find it | Record decision_record as the PLT library object created in rwb_asset (DP-03), not as an entity. |
| CDC-18291 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-7 | 11 | Register or correct field IDs DF-COL-028, DF-COL-029, DF-COL-031, DF-COL-033, DF-COL-041 and names holding_status, collateral_id, decision_record. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (24)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18062 | RWB-S5-E4025-APP | CG-ALL-10053 | 16 | Add rows TC-E4-025-01 to TC-E4-025-06 to the Story test cases tab in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-18070 | RWB-S5-E4025-CON | DOR-RWB-S5-E4025-CON-12 | 12.7, 16 | Add TC-E4-025-01 to -06 and TC-S5-E4025-CON-01 to -05 to tab Story test cases. |
| CDC-18072 | RWB-S5-E4025-CON | CG-ALL-10064 | 16 | Add rows for TC-E4-025-01 to TC-E4-025-06 and TC-S5-E4025-CON-01 to TC-S5-E4025-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18082 | RWB-S5-E4026-APP | CG-ALL-10078 | 16 | Add rows TC-E4-026-01 to TC-E4-026-06 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-18096 | RWB-S5-E4026-CON | DOR-RWB-S5-E4026-CON-12 | 12.7, 16 | Add rows for the ten listed IDs and for TC-S5-E4026-CON-05 and TC-S5-E4026-CON-06 |
| CDC-18100 | RWB-S5-E4026-CON | CG-ALL-10090 | 16 | Add rows for TC-E4-026-01 to TC-E4-026-06 and TC-S5-E4026-CON-01 to TC-S5-E4026-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18111 | RWB-S5-E4027-APP | CG-ALL-10105 | 16 | Add Story test case rows TC-E4-027-01 to -06, and -07 and -08, with Given, When and Then copied from the criteria they cover. |
| CDC-18124 | RWB-S5-E4027-CON | CG-ALL-10119 | 16 | Add rows TC-E4-027-01 to TC-E4-027-06 and TC-S5-E4027-CON-01 to TC-S5-E4027-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18133 | RWB-S5-E4028-APP | CG-ALL-10135 | 16 | Add rows TC-E4-028-01 to TC-E4-028-05 with Given, When and Then copied from the criteria they cover. |
| CDC-18147 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E4-028-01 to -05, TC-S5-E4028-CON-01 to -04 and the new TC-S5-E4028-CON-05 |
| CDC-18150 | RWB-S5-E4028-CON | CG-ALL-10149 | 16 | Add rows for TC-E4-028-01 to TC-E4-028-05 and TC-S5-E4028-CON-01 to TC-S5-E4028-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18158 | RWB-S5-E4029-APP | CG-ALL-10161 | 16 | Add rows TC-E4-029-01 to TC-E4-029-06 with Given, When and Then copied from the criterion each covers. |
| CDC-18168 | RWB-S5-E4029-CON | DOR-RWB-S5-E4029-CON-12 | 12.7, 16 | Add to tab Story test cases the rows TC-E4-029-01 to 06 and TC-S5-E4029-CON-01 to 05 |
| CDC-18172 | RWB-S5-E4029-CON | CG-ALL-10172 | 16 | add the rows for TC-E4-029-01 to TC-E4-029-06 and TC-S5-E4029-CON-01 to TC-S5-E4029-CON-04 with Given, When and Then copied from the criterion each covers |
| CDC-18183 | RWB-S5-E4030-APP | CG-ALL-10186 | 16 | Add TC-E4-030-01 to -06 with Given, When and Then copied from their criteria, and TC-E4-030-07 and -08 from section 16. |
| CDC-18201 | RWB-S5-E4030-CON | DOR-RWB-S5-E4030-CON-12 | 16 | Add rows for TC-E4-030-01 to -06 and TC-S5-E4030-CON-01 to -08 with their Given, When and Then, including the new boundary and rule cases. |
| CDC-18208 | RWB-S5-E4030-CON | CG-ALL-10196 | 16 | Add rows for TC-E4-030-01 to TC-E4-030-06 and TC-S5-E4030-CON-01 to TC-S5-E4030-CON-04 with Given, When and Then copied from their criteria. |
| CDC-18225 | RWB-S5-E4031-APP | CG-ALL-10207 | 16 | In tab Story test cases, add rows TC-E4-031-01 to TC-E4-031-05 with Given, When and Then copied from the criterion each covers. |
| CDC-18234 | RWB-S5-E4031-CON | DOR-RWB-S5-E4031-CON-12 | 16 | Add Story test cases rows for TC-E4-031-01 to -05, TC-S5-E4031-CON-01 to -04, and new TC-S5-E4031-CON-05 and -06 under the same IDs. |
| CDC-18237 | RWB-S5-E4031-CON | CG-ALL-10220 | 16 | Add rows for TC-E4-031-01 to TC-E4-031-05 and TC-S5-E4031-CON-01 to TC-S5-E4031-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18249 | RWB-S5-E4032-APP | CG-ALL-10230 | 16 | Add Story test cases rows for TC-E4-032-01 to TC-E4-032-05 and TC-S5-E4032-APP-01 and TC-S5-E4032-APP-02, with Given, When and Then copied from the criterion each covers. |
| CDC-18274 | RWB-S5-E4032-CON | CG-ALL-10241 | 16 | Add rows for TC-E4-032-01 to TC-E4-032-05 and TC-S5-E4032-CON-01 to TC-S5-E4032-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-18289 | RWB-S5-E4033-APP | CG-ALL-10257 | 16 | Add rows TC-E4-033-01 to TC-E4-033-05 with Given, When and Then copied from the criteria they cover. |
| CDC-18290 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-12 | 16 | Add rows TC-E4-033-01 to TC-E4-033-05 and new TC-E4-033-06, TC-E4-033-07 and TC-E4-033-08 under the same IDs. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18060 | RWB-S5-E4025-APP | CG-ALL-10050 | 12.5 | Add activity assessBelowFloorBid on task queue rwb-asset (R-DIS-41) to the Activities sheet, or name the catalogued activity used instead. |
| CDC-18061 | RWB-S5-E4025-APP | CG-ALL-10051 | 12.5 | Add activity agreeSale on task queue rwb-asset (R-DIS-42) to the Activities sheet, or name the catalogued activity used instead. |
| CDC-18068 | RWB-S5-E4025-CON | CG-ALL-10063 | 12.5 | Add an Activities row for the below-floor branch activity, named by the application story, on task queue rwb-asset. |
| CDC-18080 | RWB-S5-E4026-APP | CG-ALL-10075 | 12.5 | Add an Activities row for relistOnNoBid on task queue rwb-asset for the no-bid re-list. |
| CDC-18081 | RWB-S5-E4026-APP | CG-ALL-10076 | 12.5 | Add an Activities row for fixFloorAsReserve on task queue rwb-asset for the floor approval. |
| CDC-18109 | RWB-S5-E4027-APP | CG-ALL-10102 | 12.5 | Add an Activities row for startPaymentTerm on task queue rwb-asset, with the inputs and outputs §12.5 states. |
| CDC-18110 | RWB-S5-E4027-APP | CG-ALL-10103 | 12.5 | Add an Activities row for confirmSalePayment on task queue rwb-asset, with the inputs and outputs §12.5 states. |
| CDC-18120 | RWB-S5-E4027-CON | CG-ALL-10116 | 12.5 | Add activity startPaymentTerm on task queue rwb-asset to the Activities sheet, or name a catalogued activity. |
| CDC-18121 | RWB-S5-E4027-CON | CG-ALL-10117 | 12.5 | Add activity confirmSalePayment, task queue rwb-asset, to the Activities sheet |
| CDC-18132 | RWB-S5-E4028-APP | CG-ALL-10133 | 12.5 | Add an Activities row for submitRegistrationTransfer on task queue rwb-asset, or name the catalogued activity to use instead. |
| CDC-18143 | RWB-S5-E4028-CON | CG-ALL-10146 | 12.5 | Add the Activities row submitRegistrationTransfer on task queue rwb-asset, or name a catalogued activity |
| CDC-18144 | RWB-S5-E4028-CON | CG-ALL-10147 | 12.5 | Add the SCIS transfer activity row on task queue rwb-integration once its owner publishes the name (GAP-2931) |
| CDC-18157 | RWB-S5-E4029-APP | CG-ALL-10160 | 12.5 | Add activity recordLandOfficeTransfer (queue rwb-asset; registration and case in; rule ID with version, two statuses, release answer and case move out) to Activities, or name a catalogued activity. |
| CDC-18182 | RWB-S5-E4030-APP | CG-ALL-10185 | 12.5 | Add applyProceeds to the Activities sheet on task queue rwb-asset, or name the catalogued activity that replaces it. |
| CDC-18200 | RWB-S5-E4030-CON | CG-ALL-10195 | 12.5 | Add activity applyProceeds to the Activities sheet on task queue rwb-asset. |
| CDC-18224 | RWB-S5-E4031-APP | CG-ALL-10206 | 12.5 | Add an Activities row for transferToRamc (Activity, task queue rwb-asset) with the contract element of section 12.5. |
| CDC-18231 | RWB-S5-E4031-CON | CG-ALL-10219 | 12.5 | Add activity transferToRamc to the Activities sheet on task queue rwb-asset, or name a catalogued activity in its place. |
| CDC-18288 | RWB-S5-E4033-APP | CG-ALL-10256 | 12.5 | Add activity rentHeldAsset on task queue rwb-asset to the Activities sheet. |

### Epic design record (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18054 | RWB-S5-E4025-APP | DOR-RWB-S5-E4025-APP-14 | find it | Record the signed epic design sign-off for RWB-S5-E4025-APP. |
| CDC-18075 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-14 | n/a | Record the signed epic design sign-off. |
| CDC-18090 | RWB-S5-E4026-CON | DOR-RWB-S5-E4026-CON-14 | find it | Record the signed epic design sign-off for RWB-S5-E4026-CON. |
| CDC-18103 | RWB-S5-E4027-APP | DOR-RWB-S5-E4027-APP-14 | Header | Record the signed epic design sign-off so this story can cite it |
| CDC-18117 | RWB-S5-E4027-CON | DOR-RWB-S5-E4027-CON-14 | header | Record the signed epic design sign-off; the story cites it once recorded. |
| CDC-18127 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-14 | Header | Record the signed epic design sign-off for RWB-SVC-S5. |
| CDC-18140 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S5. |
| CDC-18153 | RWB-S5-E4029-APP | DOR-RWB-S5-E4029-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S5 in the epic design record. |
| CDC-18164 | RWB-S5-E4029-CON | DOR-RWB-S5-E4029-CON-14 | header | Header row states the epic design sign-off as Not specified, without any acceptance or date. |
| CDC-18174 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-14 | header | Record the signed epic design sign-off for RWB-S5-E4030-APP. |
| CDC-18198 | RWB-S5-E4030-CON | DOR-RWB-S5-E4030-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S5 and link it to this story. |
| CDC-18218 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-14 | n/a | Record the signed sign-off of the epic design so the story can cite it |
| CDC-18229 | RWB-S5-E4031-CON | DOR-RWB-S5-E4031-CON-14 | Not located in story | Record the signed epic design sign-off so that Definition of Ready item 14 can pass. |
| CDC-18262 | RWB-S5-E4032-CON | DOR-RWB-S5-E4032-CON-14 | header | Record the signed epic design sign-off for RWB-S5-E4032-CON in the epic design record. |
| CDC-18281 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-14 | header | Record the signed epic design sign-off. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18069 | RWB-S5-E4025-CON | DOR-RWB-S5-E4025-CON-1 | 1 | Add the role name 'tech lead' of rwb-asset, or confirm the role code that section 1 should use, so that it matches a role in v5. |
| CDC-18083 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-6 | 10 | Add role SY-DATALOAD (asset and disposal C, listing and price write) to the role list, or the story removes it from section 10 on a ruling. |
| CDC-18094 | RWB-S5-E4026-CON | DOR-RWB-S5-E4026-CON-1 | 1 | Add 'tech lead' of rwb-asset as a role code or role name |
| CDC-18112 | RWB-S5-E4027-APP | DOR-RWB-S5-E4027-APP-6 | 10 | Add role SY-DATALOAD to the role list, or remove it from §10 of RWB-S5-E4027-APP. |
| CDC-18122 | RWB-S5-E4027-CON | DOR-RWB-S5-E4027-CON-1 | 1 | Add a role code or name for the tech lead of rwb-asset, the role §1 and §10 use |
| CDC-18145 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-1 | 1 | Add role 'tech lead' for rwb-asset, or name the existing role code the story should use |
| CDC-18159 | RWB-S5-E4029-APP | DOR-RWB-S5-E4029-APP-6 | 10 | Add role SY-DATALOAD or confirm it is not a role; story now states the authorise check as Not specified (DOR-RWB-S5-E4029-APP-6). |
| CDC-18167 | RWB-S5-E4029-CON | DOR-RWB-S5-E4029-CON-1 | 1 | Add 'tech lead' as a role code or name for the rwb-asset tech lead, or name the existing role code it maps to |
| CDC-18184 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-6 | 10 | Add role SY-DATALOAD or remove it from section 10 of this story. Story now names the authorise check as Not specified in the source documents. |
| CDC-18226 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-6 | 10 | Add the role SY-DATALOAD to the roles list. |
| CDC-18232 | RWB-S5-E4031-CON | DOR-RWB-S5-E4031-CON-1 | 1 | Add the role 'tech lead' as a role code or role name, matching the role used in §1 and §10. |
| CDC-18250 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-6 | 10 | Add role SY-DATALOAD (listed in section 10 of RWB-S5-E4032-APP) to the role catalogue, or confirm it is not a valid role. |
| CDC-18269 | RWB-S5-E4032-CON | DOR-RWB-S5-E4032-CON-1 | 1 | Add a role code and name for 'solution architect of rwb-asset' so section 1 can cite it |
| CDC-18270 | RWB-S5-E4032-CON | DOR-RWB-S5-E4032-CON-6 | 10 | Publish role SY-DATALOAD, used in the buy-back row of section 10, in Users Roles and Permissions v5. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18123 | RWB-S5-E4027-CON | CG-ALL-10118 | 14 | MSG-P1-001 text kept as now written; no further change |
| CDC-18136 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-9 | 14 | Confirm the MSG-P1-001 wording against the standard, or supply the standard so the text can be verified; the FSD P1 v3 wording ('ACE batch') differs. |
| CDC-18137 | RWB-S5-E4028-APP | CG-ALL-10134 | 14 | MSG-P1-001 text kept as FSD P1 v3 wording ('Today's ACE batch has not arrived.'); not copied from Standard v4 |
| CDC-18244 | RWB-S5-E4032-APP | CG-ALL-10225 | 14 | Business analyst adds a new message ID for the story's floor-price use; the story then cites that ID. |
| CDC-18245 | RWB-S5-E4032-APP | CG-ALL-10226 | 14 | Business analyst adds a new message ID for the story's appraisal-age use; the story then cites that ID. |
| CDC-18246 | RWB-S5-E4032-APP | CG-ALL-10227 | 4, 14 | Add a new message ID for the buy-back required-field use, so MSG-GEN-001 keeps its standard meaning; the story then cites the new ID. |
| CDC-18247 | RWB-S5-E4032-APP | CG-ALL-10228 | 4, 14 | Add a new message ID for the story's outside-permission use, so MSG-P4-002 keeps its standard meaning; the story then cites the new ID. |
| CDC-18248 | RWB-S5-E4032-APP | CG-ALL-10229 | 4, 14 | Add a new message ID for the story's failed decision-record use, so MSG-P7-003 keeps its standard meaning; the story then cites the new ID. |
| CDC-18252 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-9 | 14 | Confirm the standard meaning of MSG-S5-001, MSG-S5-002, MSG-GEN-001, MSG-P4-002 and MSG-P7-003, or re-key the slice messages to new IDs. |
| CDC-18264 | RWB-S5-E4032-CON | CG-ALL-10236 | 14 | Add a new message ID for the story's use of MSG-S5-001 in section 14; the story then cites that ID. |
| CDC-18265 | RWB-S5-E4032-CON | CG-ALL-10237 | 14 | Add a new message ID for the story's use of MSG-S5-002 in section 14; the story then cites that ID. |
| CDC-18266 | RWB-S5-E4032-CON | CG-ALL-10238 | 14 | Add a new message ID for the story's use of MSG-GEN-001 in section 14; the story then cites that ID. |
| CDC-18267 | RWB-S5-E4032-CON | CG-ALL-10239 | 4, 14 | Add a new message ID for the buy-back access text, then cite it in the MSG-P4-002 row of section 14 |
| CDC-18268 | RWB-S5-E4032-CON | CG-ALL-10240 | 4, 14 | Add a new message ID for the decision-record write failure text, then cite it in the MSG-P7-003 row of section 14 |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18064 | RWB-S5-E4025-APP | GAP-1752 | 12.7 | Add rows for the auction round, bid, award, holding cost and work order as entity groups of rwb-asset before the S5 DB story starts. |
| CDC-18071 | RWB-S5-E4025-CON | GAP-1752 | find it | Add S5 rows, owner rwb_asset, for auction round, bid, award, holding-cost movement and work order as entity groups; physical names left to the S5 DB story. |
| CDC-18085 | RWB-S5-E4026-APP | GAP-1752 | 11 | Add rows for the auction round, bid, award, holding-cost movement and work order as entity groups of rwb-asset (S5), before the S5 DB story starts. |
| CDC-18193 | RWB-S5-E4030-APP | GAP-1915 | 5 | Add an asset row to the S5 table list; the requirement owner allocates a REQ id for the contract slice at the next plan revision. |
| CDC-18212 | RWB-S5-E4030-CON | GAP-1915 | not in chunk | Allocate a REQ id for the contract slice at the next plan revision; add the asset row to S5's Ownership Map table list. |
| CDC-18228 | RWB-S5-E4031-APP | GAP-2957 | 8 | Add the asset table with owner S5 (rwb-asset) per TSD S5 T3.1 DF-COL-028 to DF-COL-042 and correct the row in its next version. |
| CDC-18236 | RWB-S5-E4031-CON | GAP-1916 | 11 | Add the RAMC transfer table and the pool, transfer-price template version and committee-approval reference columns, or accept the defaults recorded in ASM-B-S5-05-E4031-1. |
| CDC-18238 | RWB-S5-E4031-CON | GAP-2957 | 15 | Add asset to the S5 table list alongside asset_sale and listing, as the object this story reads (GAP-2957), in the next version. |
| CDC-18259 | RWB-S5-E4032-APP | GAP-1930 | 9 | Add a row for the asset table (rwb_asset) with owner S5 in the next version; listing and asset_sale already show S5. |
| CDC-18275 | RWB-S5-E4032-CON | GAP-1930 | 5 | Add a row for the asset table rwb_asset (rwb-asset) with owner S5, read from Architecture v5 slides 19 and 41 and TSD S5 T3.1. |
| CDC-18292 | RWB-S5-E4033-APP | GAP-1935 | 12.5 | Supersede the GET /assets/{assetId} row with the business-key path under ASM-A6-api-15; TSD S5 T3.1 also needs an asset business-key column for that path. |
| CDC-18293 | RWB-S5-E4033-APP | GAP-2966 | 12.5 | Add an asset row assigning the asset table to S5 (rwb-asset), per Architecture v5 slides 19 and 41 and TSD S5 T3.1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18119 | RWB-S5-E4027-CON | CG-ALL-10112 | 12.2 | Name the received-at field for payment_received_at, or record the object in the owning document; nearest names are unverified. |
| CDC-18142 | RWB-S5-E4028-CON | CG-ALL-10141 | 11, 12.1, 12.7 | Add holding_status as a field, or record the object that holds it (index, library table or flag) in the owning document. |
| CDC-18148 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-7 | 11 | Add field holding_status to LDM v9 or Data Classification v5, or name the field that exists |
| CDC-18185 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-7 | 11 | Add DF-COL-028 and DF-COL-042, and fields shortfall_amount, residual_route and decision_record, or name where they are held. Story decision-log wording fixed in AC1 and AC4. |
| CDC-18222 | RWB-S5-E4031-APP | CG-ALL-10200 | 4 | Record holding_status as the asset status field, or name the dictionary field the story should use |
| CDC-18223 | RWB-S5-E4031-APP | CG-ALL-10201 | 4; 8 | Record asset_id as the asset identifier of asset_sale, or name the dictionary field the story should use |
| CDC-18230 | RWB-S5-E4031-CON | CG-ALL-10213 | 11 | Confirm the dictionary name for the asset_id column of DF-SAL-001 to DF-SAL-019, or record asset_id as an object in its owning document. |
| CDC-18235 | RWB-S5-E4031-CON | DOR-RWB-S5-E4031-CON-7 | 11 | Confirm or add asset_id as a field or entity in LDM v9 and Data Classification v5 for the AssetSale and Listing elements. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18178 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-8 | 12.2 | Set the yaml base path to /api/recovery/asset/v1 (story section 12.2, DP-13). Queue rwb-asset already matches section 12.5. HTTP message IDs and the workflow ID rule are not in the sources (CG-ALL-10184), so they stay Not applied. |
| CDC-18239 | RWB-S5-E4032-APP | CG-ALL-10223 | 12.1 | Publish GET /api/recovery/asset/v1/assets in rwb-asset.yaml through RWB-S5-E4032-CON (API-S5-001). |
| CDC-18240 | RWB-S5-E4032-APP | CG-ALL-10224 | 12.1 | Publish GET /api/recovery/asset/v1/assets/{assetId} in rwb-asset.yaml through RWB-S5-E4032-CON (API-S5-002). |
| CDC-18243 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-8 | 12.1 | Publish GET /api/recovery/asset/v1/assets and GET /api/recovery/asset/v1/assets/{assetId} (see CG-ALL-10223, CG-ALL-10224). |
| CDC-18260 | RWB-S5-E4032-CON | CG-ALL-10234 | 12.1 | Publish GET /api/recovery/asset/v1/assets with the query and AssetPage response of section 12.1, or remove the row from 12.1. |
| CDC-18261 | RWB-S5-E4032-CON | CG-ALL-10235 | 12.1 | Publish GET /api/recovery/asset/v1/assets/{assetId} with the Asset response of section 12.1, or remove the row from 12.1. |
| CDC-18263 | RWB-S5-E4032-CON | DOR-RWB-S5-E4032-CON-8 | 12.1 | Add paths GET /api/recovery/asset/v1/assets and GET /api/recovery/asset/v1/assets/{assetId} as listed in section 12.1. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18091 | RWB-S5-E4026-CON | DOR-RWB-S5-E4026-CON-8 | find it | Declare the REST bases (CG-ALL-10084, 10085) and catalog rows for queue, relistOnNoBid (CG-ALL-10086, 10088). |
| CDC-18118 | RWB-S5-E4027-CON | DOR-RWB-S5-E4027-CON-8 | 12.2 | Declare base /api/recovery/case/v1 (CG-ALL-10113); add startPaymentTerm (CG-ALL-10116); clear the remaining detcheck finding. |
| CDC-18165 | RWB-S5-E4029-CON | DOR-RWB-S5-E4029-CON-8 | 12.2 | Declare REST bases /api/recovery/case/v1 and /api/recovery/document/v1; add activity recordLandOfficeTransfer to the catalog. Story-side items 3 and 9 resolved here. |
| CDC-18221 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-8 | 12.5 | Yaml: declare REST base /api/recovery/case/v1. Catalog: add activity transferToRamc on task queue rwb-asset |
| CDC-18284 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-8 | find it | Add bases /api/recovery/payment/v1, /api/recovery/case/v1 and /api/recovery/comms/v1; align the AssetDisposalWorkflow task queue and namespace with rwb-asset and rwb-recovery, or record the difference. |

### RWB-S5-E4032-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18241 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-21 | header | Set build status from Not started to Done once the contract is published. |
| CDC-18242 | RWB-S5-E4032-APP | DOR-RWB-S5-E4032-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-18255 | RWB-S5-E4032-APP | GAP-1928 | 5 | Declare the two asset reads as provided, the buy-back as an element of the Asset answer and rows of listing and asset_sale, and the four consumed rows as placeholders. Add no operation, list value or other owner's property. |
| CDC-18256 | RWB-S5-E4032-APP | GAP-1929 | 5 | Derive the approval and template-price fakes from the owners' published documents, mark unsourced fields with the placeholder, and hold them under the drift test. |
| CDC-18258 | RWB-S5-E4032-APP | GAP-2961 | 5 | Publish the two reads with the buy-back element. Declare the four unnamed consumed rows with a placeholder and a 2 s timeout. Reference the platform decision-record element. Keep the lists unchanged with a placeholder for the buy-back value. Tag baseline v1 before the application story builds. |

### RWB-S5-E4026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18076 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-21 | n/a | Move build status from Not started to Done so the contract is published. |
| CDC-18086 | RWB-S5-E4026-APP | GAP-2918 | 7, 8 | Declare R-DIS-38 once in the contract baseline; the ladder story owns the step and this story the no-bid outcome that opens the next round. |
| CDC-18087 | RWB-S5-E4026-APP | GAP-2919 | 7 | Declare API-S5-004 and R-DIS-29 once for the pricing, ladder and re-list stories, with the owner split stated in GAP-2919. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18095 | RWB-S5-E4026-CON | DOR-RWB-S5-E4026-CON-10 | find it | Add empty, loading, error and no-access states for SCR-21 and SCR-23 to the screen field list |
| CDC-18146 | RWB-S5-E4028-CON | DOR-RWB-S5-E4028-CON-10 | 15 | Screen states belong to the screen field list owner (DP-19), which this story does not own. |
| CDC-18233 | RWB-S5-E4031-CON | DOR-RWB-S5-E4031-CON-10 | 1 | Add empty, loading, error and no-access states for SCR-21 to the screen field list owned by RWB-PLT-N001-CON. |

### OTHER:Change log (assembler) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18098 | RWB-S5-E4026-CON | GAP-2918 | header | Change log is not edited in this story; shared declaration of R-DIS-38 with RWB-S5-E4022 left to the assembler (GAP-2918; ASM-4816). |
| CDC-18099 | RWB-S5-E4026-CON | GAP-2919 | header | Change log is not edited in this story; shared declaration of R-DIS-29 and API-S5-004 left to the assembler (GAP-2919; ASM-4817). |
| CDC-18101 | RWB-S5-E4026-CON | GAP-2924 | header | DP-04 package declaration is not in the story text or diff; left to the assembler (GAP-2924; ASM-4796). |

### RWB-S5-E4027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18104 | RWB-S5-E4027-APP | DOR-RWB-S5-E4027-APP-21 | Header | Set build status to Done for the published contract |
| CDC-18105 | RWB-S5-E4027-APP | DOR-RWB-S5-E4027-APP-22 | Header | Publish the contract fake library and record its version |
| CDC-18115 | RWB-S5-E4027-APP | GAP-2929 | 12.5 | Declare the three consumed rows (case-move answer, payment fact, payment event) in the contract baseline with placeholder names and GAP-2929; adopt the owner's names at the tag. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18161 | RWB-S5-E4029-APP | GAP-1767 | find it | Add S5 cells to P6 for notices through rwb-comms (slide 17) and to P5 for photographs, inspection reports and transfer documents through rwb-document (slide 16). |
| CDC-18170 | RWB-S5-E4029-CON | GAP-1767 | none | Add the S5 to P6 cell for the statutory notice request and its proof-of-delivery event, and the S5 to P5 cell for photograph, inspection report and transfer document upload |
| CDC-18186 | RWB-S5-E4030-APP | GAP-1759 | 17 | Remove ALS and GL as integration points of FSD A2.5, A2.18, A2.21 and A2.23; route all posting through rwb-payment postProceeds (Arch v5 slides 19, 41, 43). |

### RWB-S5-E4030-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18175 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-21 | header | Move build status from Not started to Done. |
| CDC-18176 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-22 | header | Publish the contract fake library and record its version. |
| CDC-18192 | RWB-S5-E4030-APP | GAP-1914 | 12 | Declare the two asset reads for the screens and the step operation as None with GAP-1914; declare a residual element only when its owner names the column. |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18077 | RWB-S5-E4026-APP | DOR-RWB-S5-E4026-APP-22 | n/a | Record the published fake library version for the contract. |
| CDC-18220 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-22 | n/a | Publish a contract fake library version and record it as published |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18093 | RWB-S5-E4026-CON | CG-ALL-10089 | 12.5 | Add activity fixFloorAsReserve to the Activities sheet, or name a catalogued activity in its place |
| CDC-18166 | RWB-S5-E4029-CON | CG-ALL-10171 | 12.5 | Add a row for activity recordLandOfficeTransfer (title-transfer step, task queue rwb-asset) or name a catalogued activity. |

### RWB-S5-E4029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18154 | RWB-S5-E4029-APP | DOR-RWB-S5-E4029-APP-21 | header | Complete the contract build and publish the contract so its build status is Done. |
| CDC-18155 | RWB-S5-E4029-APP | DOR-RWB-S5-E4029-APP-22 | header | Publish a contract fake library version and record its version. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18188 | RWB-S5-E4030-APP | GAP-2944 | 12.5 | Register the case-move operation, the proceeds-fact activity and the source-data product as boundary rows; keep the plan C list empty. |
| CDC-18204 | RWB-S5-E4030-CON | GAP-2944 | find it | Register the case-move operation, the proceeds-fact activity and the source-data product as boundary rows of the platform envelope; keep the plan C list empty. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18194 | RWB-S5-E4030-APP | GAP-2945 | 12 | Add rwb-asset to the EV-25 ProceedsMatched consumer list at its next version; the subscription to rwb.payment.events.v1 stays declared with consumer group rwb-asset. |
| CDC-18213 | RWB-S5-E4030-CON | GAP-2945 | not in chunk | Add rwb-asset to the EV-25 ProceedsMatched consumer list at the next catalogue version; keep the subscription declared in the story. |

### RWB-S5-E4033-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18282 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-21 | header | Set build status to Done with the contract published before this story starts. |
| CDC-18283 | RWB-S5-E4033-APP | DOR-RWB-S5-E4033-APP-22 | header | Record the published contract fake library version. |

### RWB-S5-E4025-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18055 | RWB-S5-E4025-APP | DOR-RWB-S5-E4025-APP-21 | find it | Move the build status of the contract story from Not started to Done. |

### OTHER:contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18056 | RWB-S5-E4025-APP | DOR-RWB-S5-E4025-APP-22 | find it | Publish the contract fake and record its library version. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18092 | RWB-S5-E4026-CON | CG-ALL-10088 | 12.5 | Add activity relistOnNoBid on task queue rwb-asset, or name a catalogued activity. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18097 | RWB-S5-E4026-CON | GAP-1752 | find it | Add rows for the auction round, the bid, the award, the holding cost and the work order, owned by S5 (rwb_asset), before the S5 DB story starts |

### OTHER:FSD S5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18114 | RWB-S5-E4027-APP | GAP-1759 | 8 | Remove ALS and GL as integration points of A2.5, A2.18, A2.21 and A2.23; route postings through rwb-payment postProceeds. |

### RWB-S5-E4028-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18128 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-21 | 12.2 | Complete the contract story to Done so the contract is published; its build status is Not started. |

### OTHER:rwb-integration contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18129 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-22 | 12.8 | Publish the SCIS transfer fake with a recorded library version. |

### OTHER:03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S5 A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18134 | RWB-S5-E4028-APP | DOR-RWB-S5-E4028-APP-10 | 13 | Add the empty, error and no-access states for SCR-21 and SCR-22, and the loading state for SCR-22, with their content per the detcheck finding for DOR-RWB-S5-E4028-APP-10. |

### OTHER:Split revision of the service story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18149 | RWB-S5-E4028-CON | GAP-2934 | 14 | Rejection handling stated as Not specified; R-DIS-53 belongs to no story row of this split |

### OTHER:rwb-access API yaml (DP-08) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18169 | RWB-S5-E4029-CON | DOR-RWB-S5-E4029-CON-6 | 10 | Publish the authorise check operation path that the declared operations call |

### RWB-S5-E4029-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18171 | RWB-S5-E4029-CON | GAP-2940 | 8 | Keep legacy AC3 verbatim with its origin tag; assert R-DIS-02 only as a take-on regression, with no second implementation |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18177 | RWB-S5-E4030-APP | DOR-RWB-S5-E4030-APP-5 | 9 | Add PROCEEDS_APPLIED and SHORTFALL_RAISED to the closed list LOV-HOLDING. |

### OTHER:TSD S5 T3.1; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18187 | RWB-S5-E4030-APP | GAP-1912 | 11 | S5 data owner confirms the residual column on asset_sale or names the rwb-writeoff store; P8 owner confirms the vendor-fee match as its own fact. |

### OTHER:Connection matrix (S5 Asset row; OTHER:P1 Source data column) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18189 | RWB-S5-E4030-APP | GAP-2946 | 12.5 | Add the S5-to-P1 edge for reads of the balance and NPA sale facts from rwb-source-data. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18190 | RWB-S5-E4030-APP | GAP-1753 | 12.5 | Allocate the EV number and catalogue row for AssetSold on rwb.asset.events.v1 in the next catalogue version. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18191 | RWB-S5-E4030-APP | GAP-1913 | 5 | Allocate a REQ id for the proceeds and shortfall slice at the next plan revision and repoint the traceability row to it. |

### OTHER:DISPOSAL rule package (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18195 | RWB-S5-E4030-APP | GAP-2949 | 7 | Name the vendor fee element at the next rule version; the story reads the fee from the proceeds row and matches it against transfer_fee. |

### OTHER:TSD S5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18196 | RWB-S5-E4030-APP | GAP-2951 | 5 | Add a FEAT-AST-21 row to the TSD S5 T8 requirement traceability table and REQ ids for both slices at their next versions. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:A2.18; OTHER:A2.21; OTHER:A2.23) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18202 | RWB-S5-E4030-CON | GAP-1759 | 11 | Move all postings to rwb-payment through postProceeds; remove the ALS and GL integration points from A2.5, A2.18, A2.21 and A2.23; pass the cost of carry with its period. |

### OTHER:Technical Solution Design S5 (T3.1) and Functional Solution Design S5 (A2.21) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18203 | RWB-S5-E4030-CON | GAP-1912 | find it | Name the residual column on asset_sale or the rwb-writeoff store; P8 rwb-payment owner confirms the vendor-fee match as its own fact; DB story adds the column in its own Flyway sequence if absent. |

### OTHER:Connection matrix (S5 Asset row; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18205 | RWB-S5-E4030-CON | GAP-2946 | find it | Add the S5-to-P1 edge; read balance and NPA sale facts from the rwb-source-data product or the rwb-case view; no v_ace_* grant in rwb_asset. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18207 | RWB-S5-E4030-CON | GAP-2948 | find it | Case side of R-DIS-54 stays in rwb-asset; balance application stays with FEAT-PAY-10 of rwb-payment; no Agent Runtime call in this wave. |

### OTHER:split_plan.json (next plan revision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18209 | RWB-S5-E4030-CON | GAP-2953 | find it | Raise the platform dependency for the inbox, outbox and rule package with the platform owners; no new H row this wave. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18210 | RWB-S5-E4030-CON | GAP-1753 | not in chunk | Allocate an EV number and catalogue row for AssetSold on rwb.asset.events.v1 at the next catalogue version. |

### OTHER:Split plan (program requirements owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18211 | RWB-S5-E4030-CON | GAP-1913 | not in chunk | Allocate a REQ id for the FEAT-AST-21 proceeds and shortfall slice at the next plan revision. |

### OTHER:DISPOSAL rule workbook (rule owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18214 | RWB-S5-E4030-CON | GAP-2949 | not in chunk | Name the vendor fee element at the next rule version, matched against transfer_fee as the rule outcome. |

### OTHER:Programme story backlog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18215 | RWB-S5-E4030-CON | GAP-2950 | not in chunk | Raise a new story for the no-shortfall close (R-DIS-56) and residual routing (R-DIS-57, R-DIS-58, R-DIS-71, R-DIS-72) with the write-off route owner. |

### OTHER:TSD S5 requirement traceability table and split plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18216 | RWB-S5-E4030-CON | GAP-2951 | not in chunk | Add FEAT-AST-21 requirement ids for both slices to the TSD T8 traceability table and the register at their next versions. |

### RWB-S5-E4031-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18219 | RWB-S5-E4031-APP | DOR-RWB-S5-E4031-APP-21 | n/a | Publish the contract: move its build status from Not started to Done |

### OTHER:FSD S5 (A2.5; OTHER:A2.18; OTHER:A2.21; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18253 | RWB-S5-E4032-APP | GAP-1759 | find it | Remove ALS and GL as integration points of this module; state that all postings go to rwb-payment through postProceeds, with cost of carry passed with its period. |

### OTHER:Contracts of rwb-case, rwb-deviation and rwb-decision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18254 | RWB-S5-E4032-APP | GAP-1921 | find it | Publish operation names for the case-move answer, the deviation raise and the approval child workflow, and confirm them with their owners before the baseline is tagged. |

### RWB-S5-E4032-CON; OTHER:owners' contracts (rwb-case, rwb-deviation, rwb-decision, rwb-comms) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18257 | RWB-S5-E4032-APP | GAP-2960 | 4, 5, 15 | Declare the case-move answer, deviation raise and template read on their owners' contracts with placeholders. Keep listing and asset_sale as the only rows. Treat the limit as a delegated-authority row read at its version. Step D1 adds REQ-S5-010 to the reqs of both slices. |

### OTHER:Legacy RWB-E4-034 and its broker route split story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18272 | RWB-S5-E4032-CON | GAP-1938 |  | Keep the four legacy criteria word for word; table R-DIS-24 and R-DIS-25; name R-DIS-26 and BROKER_INSTRUCTED in prose; record the rental build as RWB-S5-E4033-APP's; rule owner confirms the three-route boundary. |

### OTHER:Legacy RWB-E4-034 and its broker route app story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18273 | RWB-S5-E4032-CON | GAP-2968 |  | Keep four legacy criteria verbatim; table R-DIS-24, R-DIS-25, R-DIS-26, R-DIS-64 and R-DIS-65; rental build stays RWB-S5-E4033-APP's; rule owner confirms boundary. |

### OTHER:Functional specification of module S5; OTHER:A2.23.3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18276 | RWB-S5-E4032-CON | GAP-2963 | 5 | Add R-DIS-24 to the rule list of A2.23.3.1 with source Business Rules and Routing Logic v4 (route = buy_back and second signature given), after the verification loop. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1752 | The Ownership Map lists no table for auction rounds, bids or holding costs, although Architecture v5 and the rules need them | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1753 | AssetSold has no event number and no row in the Ownership Map event sheet | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1759 | Proceeds, cost of carry and fees are posted to ALS and the ledger by this service, while Architecture v5 gives posting to rwb-payment | Solution architect | Resolved (directive) |
| GAP-1767 | The statutory notice and the document evidence have no cell in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1911 | The operation names of the rwb-payment proceeds and vendor-fee read, the rwb-case case-move answer and the rwb-source-data account and sale data product are not published | P3 rwb-case owner, P8 rwb-payment owner, P1 rwb-source-data owner | Resolved (directive) |
| GAP-1912 | No source names the table and column that hold the residual and its D9 hand-off, and the vendor-fee match is not assigned to a service | S5 rwb-asset owner with P8 rwb-payment owner; P3 rwb-case owner for the D9 routing | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1913 | The split plan carries no requirement id for this slice | Program requirements owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1914 | No source names a published operation for the proceeds and shortfall step itself, and no element is defined for the residual in the contract | S5 rwb-asset service owner | Resolved (directive) |
| GAP-1915 | The split plan carries no requirement id for the contract slice and the Ownership Map table list omits the asset row | Program requirements owner and the Ownership Map maintainer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1916 | RWB-S5-E4031-APP: the RAMC transfer step has no source for its call names, its pool, price and approval references, its timer or its screen owner | Solution architect | Resolved (directive) |
| GAP-1917 | RWB-S5-E4031-APP: the legacy endpoints name an S1 operation and a later S5 pricing operation, neither of which the transfer step calls | Solution architect | Resolved (directive) |
| GAP-1918 | RWB-S5-E4031-APP: the split plan and TSD S5 T8 carry no requirement id for FEAT-AST-22 | Business analyst | Resolved (directive) |
| GAP-1919 | RWB-S5-E4031-CON: the transfer element, the instruction element and the four consumed rows have no published names or fields | Solution architect | Resolved (directive) |
| GAP-1920 | RWB-S5-E4031-CON: the instruction is both a partner REST path and a Temporal activity, and no source reconciles the two | Solution architect | Resolved (directive) |
| GAP-1921 | The buy-back step has no operation of its own and the consumed rows have no published operation names | Tech lead of rwb-asset with the owners of rwb-case and rwb-deviation | Resolved (directive) |
| GAP-1922 | Which table and column hold the buy-back terms and the template price is not settled and the template price has no field identifier | Tech lead of rwb-asset with the owner of rwb-comms and the data steward | Resolved (directive) |
| GAP-1923 | The approval the limit requires has no limit value in any source and no published approval shape | Owner of rwb-decision with the owner of rwb-access | Resolved (directive) |
| GAP-1924 | The buy-back channel and the buy-back listing status have no value in the closed lists | Owner of the reference data with the tech lead of rwb-asset | Resolved (directive) |
| GAP-1925 | Legacy AC1 gives no from state while the buy-back rule starts at ROUTE_WITH_APPROVER and the asset is held | Owner of rwb-decision with the owner of rwb-case | Resolved (directive) |
| GAP-1927 | The split plan carries no requirement id for this slice | Traceability manager with the business analyst | Resolved (directive) |
| GAP-1928 | No published surface exists for the buy-back step so the baseline declares it as an element and the consumed rows as placeholders | Tech lead of rwb-asset | Resolved (directive) |
| GAP-1929 | The approval answer and the template price element are not published and their fakes are derived | Tech lead of rwb-asset with the owners of rwb-decision and rwb-comms | Resolved (directive) |
| GAP-1930 | The asset row is absent from the Ownership Map table list although three sources give it to S5 | Solution architect with the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1931 | The rental terms, the auto-debit and case-move operation names, the arrears follow-up owner and threshold, the ATS interface and the step name are not specified in the source documents | Tech lead of rwb-asset, solution architect, and the owners of rwb-payment and rwb-case | Resolved (directive) |
| GAP-1932 | The legacy Data, Endpoints and Screen tables name views, tables, an operation and a screen state that this slice does not read, call or show | Solution architect and data steward | Resolved (directive) |
| GAP-1933 | The split plan carries no requirement id for this slice | Business analyst and traceability manager | Resolved (directive) |
| GAP-1934 | The rental element, the consumed operation names and the ATS interface are not specified in the source documents | Tech lead of rwb-asset and solution architect, with the owners of rwb-payment, rwb-case and rwb-source-data | Resolved (directive) |
| GAP-1935 | The read path carries the ACE asset business key while the asset table is keyed by a record identifier | Solution architect and data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1936 | No approval record, deprecation window or fake retention is stated for the contract baseline | Solution architect and governance lead | Resolved (directive) |
| GAP-1938 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule and state sit outside the rule table of the slice | Business analyst, solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-1939 | The split plan carries no requirement id for this slice | Business analyst and traceability manager | Resolved (directive) |
| GAP-2912 | No published operation name for the rwb-source-data appraisal and asset product, for the rwb-case case-state read or for the case-move answer | Solution architect | Resolved (directive) |
| GAP-2913 | No S5 field holds the bid amount or the second signature that R-DIS-41 and R-DIS-42 condition on | Solution architect | Resolved (directive) |
| GAP-2914 | The legacy endpoints table names the listings write for the accept while the TSD gives the round write the sale answer | Solution architect | Resolved (directive) |
| GAP-2915 | No published operation raises the second-signature approval item, and no S5 field carries its outcome | Solution architect | Resolved (directive) |
| GAP-2916 | The split plan carries no requirement id for this slice | Business analyst | Resolved (directive) |
| GAP-2917 | The step evaluates a DISPOSAL rule package and uses the approval template while neither carries a pattern row of this slice | Solution architect | Resolved (directive) |
| GAP-2918 | R-DIS-38 is carried by the ladder story and by the re-list story, and the legacy story repeats the rule | Business analyst | Resolved (directive) |
| GAP-2919 | R-DIS-29 and API-S5-004 are carried by the pricing story and by the re-list story, and no source splits them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2920 | No column or reference row holds the re-list count, the re-list limit or the per-round price | Solution architect | Resolved (directive) |
| GAP-2921 | No published operation name for the rwb-source-data asset and valuation product or for the rwb-case case-answer row | Solution architect | Resolved (directive) |
| GAP-2922 | A re-listed round reaches the auction portals through no declared operation | Solution architect | Resolved (directive) |
| GAP-2923 | REQ-S5-006 is mapped to FEAT-AST-08 in the traceability table while its text names the no-bid re-list | Business analyst | Resolved (directive) |
| GAP-2924 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2925 | No element holds the award, the payment due date, the payment received-at time or the five-day term | Solution architect | Resolved (directive) |
| GAP-2926 | The five-day term's rules R-DIS-47 to R-DIS-50 sit across this story and RWB-S5-E4024-APP, and no source splits them | Business analyst | Resolved (directive) |
| GAP-2927 | Legacy AC2, AC3 and the FSD A2.18 rule list name R-DIS-11 and R-DIS-37, rules of the work order and the auction round, not the payment term | Business analyst | Resolved (directive) |
| GAP-2928 | No requirement row names the five-day payment term | Business analyst | Resolved (directive) |
| GAP-2929 | The consumed rows and the rwb-payment event carry no published name | Solution architect | Resolved (directive) |
| GAP-2930 | DP-04 sits outside the declared pattern set while the DISPOSAL package must still be evaluated | Solution architect | Resolved (directive) |
| GAP-2931 | SCIS has no interface row in TSD S5, no call type, and DP-16 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2932 | The FSD makes the step a system submission while INT-28 records SCIS as prepared by the officer | Business analyst | Resolved (directive) |
| GAP-2933 | No element holds the vehicle registration particulars or the SCIS submission reference and its date | Solution architect | Resolved (directive) |
| GAP-2934 | R-DIS-53 (transfer rejected, TITLE_BLOCKED) belongs to no story row of the split | Business analyst | Resolved (directive) |
| GAP-2935 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2936 | REQ-S5-008 is claimed by FEAT-AST-08 in the TSD and by FEAT-AST-19 and FEAT-AST-20 in BR-029 | Business analyst | Resolved (directive) |
| GAP-2938 | No element of rwb_asset holds the title status, the Land Office registration date and reference or the custody release, and the ownership rows name only asset_sale and listing | Solution architect of S5 with the DB story owner of rwb_asset | Resolved (directive) |
| GAP-2939 | The document custody release has no published operation on rwb-document and the plan carries no contract dependency for the boundary | Owner of rwb-document (P5) with the tech lead of rwb-asset | Resolved (directive) |
| GAP-2940 | Legacy AC3 of RWB-E4-029 owns R-DIS-02, the deed in lieu take-on that RWB-S5-E3020-APP already builds for the same rule | Business analyst of the Asset module with the solution architect of S5 | Resolved (directive) |
| GAP-2942 | The plan carries no requirement id for either slice and TSD S5 T8 does not trace REQ-S5-008 or FEAT-AST-20 | S5 rwb-asset service owner with the business analyst of the Asset module | Resolved (directive) |
| GAP-2944 | The case-move answer, the proceeds-fact activity and the source-data product the step needs have no published operation name and no row in the plan dependency lists | S5 rwb-asset service owner with the owners of P3 rwb-case, P8 rwb-payment and P1 rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2945 | The event catalogue names Case and workflow as the only consumer of ProceedsMatched while Architecture v5 gives S5 an event subscription to P8 | S5 rwb-asset service owner with the owner of the P8 rwb-payment event catalogue row | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2946 | The legacy data table reads v_ace_account and v_ace_npa_sale while the target gives S5 no edge to rwb-source-data and reserves the views to that service | S5 rwb-asset service owner with the owner of P1 rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2947 | No table, column or list carries the residual, its route or its hand-off to the D9 decision | S5 rwb-asset service owner with the data model owner and the owner of P7 rwb-decision | Resolved (directive) |
| GAP-2948 | Legacy AC3 applies the proceeds to the loan account while that application is FEAT-PAY-10 of rwb-payment, and R-DIS-54 also names Agent Runtime as a system | S5 rwb-asset service owner with the owners of P8 rwb-payment and P10 rwb-agent | Resolved (directive) |
| GAP-2949 | The vendor fee that R-DIS-54 matches has no element in S5 and no stated owner of the match | S5 rwb-asset service owner with the owner of P8 rwb-payment and the DISPOSAL rule owner in P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2950 | Five rules of the feature own no legacy criterion, so the no-shortfall close, the residual routing and the unmatched exception have no story | S5 rwb-asset service owner with the write-off route owner and the programme backlog owner | Resolved (directive) |
| GAP-2951 | The split plan carries no requirement id for either slice and the TSD traceability table has no FEAT-AST-21 row | Business analyst, S5 with the requirements register owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2952 | The legacy screen states of SCR-22 do not match the holding lists and the states this step produces are case states | S5 rwb-asset service owner with the screen owner of RWB-PLT-N001 and the case owner of P3 | Resolved (directive) |
| GAP-2953 | The slice consumes an event and evaluates a rule package, while DP-09 and DP-04 are outside its pattern set and no platform build row is carried | S5 rwb-asset service owner with the platform event and workflow owners | Resolved (directive) |
| GAP-2954 | The pool reference, the transfer price element and its template version, the approval reference, the instruction element names, the acceptance and refusal codes and the 'per agreement' timer have no source | S5 rwb-asset service owner with the business analyst of the Asset module and the rwb-partner owner | Resolved (directive) |
| GAP-2955 | No source names an operation of the transfer step and the legacy endpoints table names operations of other steps | Solution architect and the S5 rwb-asset service owner | Resolved (directive) |
| GAP-2956 | Neither slice carries a requirement id and the module requirement rows name no transfer requirement | S5 rwb-asset service owner with the business analyst of the Asset module | Resolved (directive) |
| GAP-2957 | The asset table is absent from the Ownership Map table list while Architecture v5 and the TSD attribute it to S5 | Solution architect and the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2959 | No source publishes the operation names and element names of the consumed rows the baseline must fake | Solution architect with the owners of P1, P3, P7 and S9 | Resolved (directive) |
| GAP-2960 | The buy-back step has no published operation for its case move, its deviation raise, its approval or its template read, gives no limit value and no field that holds the template price, and the buy-back has no value in the two closed lists | S5 rwb-asset service owner with the data steward, the P7 rwb-decision owner and the P4 rwb-access owner | Resolved (directive) |
| GAP-2961 | The contract baseline of the buy-back slice has no published payload for the approval answer or the deviation reference, no published name for four of the five consumed rows, and no buy-back value in LOV-SALE-CHANNEL or LOV-LISTING | Solution architect of S5 rwb-asset with the S8 rwb-deviation, P7 rwb-decision and P6 rwb-comms contract owners | Resolved (directive) |
| GAP-2962 | Legacy AC1 gives no from state while R-DIS-24 starts at ROUTE_WITH_APPROVER, and the criterion's screen action has no state of its own | S5 rwb-asset service owner with the P3 rwb-case owner and the business analyst of module S5 | Resolved (directive) |
| GAP-2963 | The FSD rule list of A2.23 omits R-DIS-24, which the rule set assigns to the buy-back route, so the module document and the rule set disagree on the rules of the feature | Business analyst of module S5 with the P7 rwb-decision rule owner | Resolved (directive) |
| GAP-2964 | The FSD gives the customer (borrower) as an also-user of the buy-back while the rights matrix has no customer role | P4 rwb-access owner with the business analyst of module S5 | Resolved (directive) |
| GAP-2965 | Rental terms, auto-debit, case-move, arrears follow-up and ATS have no value or name in the sources (APP slice) | Solution architect | Resolved (directive) |
| GAP-2966 | Rental element, consumed operation names, asset key path and Draft baseline have no source shape (CON slice) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2968 | The legacy feature is titled Sell through a broker while two of its four criteria are the buy-back and rental rules, and the broker route's own rule has no criterion of the key | Business analyst, solution architect and the rule owner in rwb-decision | Resolved (directive) |
| GAP-2970 | The split plan carries no requirement id for either slice | Business analyst and traceability manager | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S5-E4025-APP | Not specified without item ID | 332 | Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `approval`, `delegation_limit`, `decision_log_entry`, `rule_row` (P7 a |
| RWB-S5-E4027-CON | new AC without TC row | 402 | AC1 is new and no section 16 row covers it |
| RWB-S5-E4027-CON | new AC without TC row | 402 | AC3 is new and no section 16 row covers it |
| RWB-S5-E4027-CON | new AC without TC row | 402 | AC4 is new and no section 16 row covers it |
| RWB-S5-E4027-CON | new AC without TC row | 402 | AC5 is new and no section 16 row covers it |
| RWB-S5-E4027-CON | new AC without TC row | 402 | AC6 is new and no section 16 row covers it |
| RWB-S5-E4027-CON | Not specified without item ID | 87 | Term data (GAP-2925): the award, the payment due date, the payment received-at time and the term length are Not specified in the source documents for any elemen |
| RWB-S5-E4027-CON | Not specified without item ID | 257 | \| The award, payment_due_date, payment_received_at, the buyer and the term length \| none \| Not specified in the source documents for the element they occupy (GA |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC1 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC2 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC3 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC4 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC5 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC6 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC7 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC8 is new and no section 16 row covers it |
| RWB-S5-E4029-CON | new AC without TC row | 376 | AC9 is new and no section 16 row covers it |
