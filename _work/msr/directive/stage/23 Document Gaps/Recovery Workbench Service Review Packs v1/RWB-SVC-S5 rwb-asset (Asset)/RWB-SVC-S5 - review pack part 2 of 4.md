# RWB-SVC-S5 rwb-asset (Asset) - review pack, part 2 of 4 (RWB-S5-E3025-APP to RWB-S5-E4024-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 18 |
| Resolved in the stories | 398 |
| Cross-document (pending in another document) | 248 |
| Not applied (value not in the sources) | 36 |
| Open business decisions | 29 |
| Register gaps linked | 62 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S5-E3025-APP | 26 | 20 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3025 APP Maintain a held property v2.md |
| RWB-S5-E3025-CON | 15 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3025 CON Maintain a held property - contract v2.md |
| RWB-S5-E3026-APP | 23 | 14 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3026 APP Re-appraise a held asset on cycle v2.md |
| RWB-S5-E3026-CON | 16 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3026 CON Re-appraise a held asset on cycle - contract v2.md |
| RWB-S5-E3027-APP | 25 | 13 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3027 APP Recommend the disposal route v2.md |
| RWB-S5-E3027-CON | 28 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3027 CON Recommend the disposal route - contract v2.md |
| RWB-S5-E3028-APP | 26 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3028 APP Set the start and floor price v2.md |
| RWB-S5-E3028-CON | 15 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3028 CON Set the start and floor price - contract v2.md |
| RWB-S5-E3029-APP | 26 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3029 APP Publish the listing v2.md |
| RWB-S5-E3029-CON | 11 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E3029 CON Publish the listing - contract v2.md |
| RWB-S5-E4021-APP | 25 | 12 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4021 APP Evict occupants from a held property v2.md |
| RWB-S5-E4021-CON | 23 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4021 CON Evict occupants from a held property - contract v2.md |
| RWB-S5-E4022-APP | 28 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4022 APP Run the descending price schedule v2.md |
| RWB-S5-E4022-CON | 19 | 10 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4022 CON Run the descending price schedule - contract v2.md |
| RWB-S5-E4023-APP | 25 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4023 APP Allocate the asset to an auction vendor by distance v2.md |
| RWB-S5-E4023-CON | 26 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4023 CON Allocate the asset to an auction vendor by distance - contract v2.md |
| RWB-S5-E4024-APP | 24 | 10 | 8 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4024 APP Run auction rounds and report bids v2.md |
| RWB-S5-E4024-CON | 17 | 9 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4024 CON Run auction rounds and report bids - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S5-E3025-APP | R-02480 | CG-ALL-9791 | Script gap | Product owner | The story adds ASSET_HELD to the closed list LOV-HOLDING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3027-CON | R-02496 | CG-ALL-9864 | Script gap | Product owner | The story adds ROUTE_APPROVED_BUYBACK to the closed list LOV-SALE-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3027-CON | R-02497 | CG-ALL-9865 | Script gap | Product owner | The story adds RENTAL_ACTIVE to the closed list LOV-SALE-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3028-APP | R-02499 | CG-ALL-9877 | Script gap | Product owner | The story adds ROUTE_APPROVED_AUCTION to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3028-APP | R-02500 | CG-ALL-9878 | Script gap | Product owner | The story adds PRICE_PROPOSED to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3028-APP | R-02501 | CG-ALL-9879 | Script gap | Product owner | The story adds FLOOR_APPROVED to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3028-APP | R-02502 | CG-ALL-9880 | Script gap | Product owner | The story adds REAPPRAISAL_RECEIVED to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3028-APP | R-02503 | CG-ALL-9881 | Script gap | Product owner | The story adds ASSET_HELD to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02512 | CG-ALL-9910 | Script gap | Product owner | The story adds LISTING_LIVE to the closed list LOV-SALE-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02513 | CG-ALL-9911 | Script gap | Product owner | The story adds DISPOSAL_PAUSED_DEVIATION to the closed list LOV-SALE-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02514 | CG-ALL-9912 | Script gap | Product owner | The story adds FLOOR_APPROVED to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02515 | CG-ALL-9913 | Script gap | Product owner | The story adds LISTING_LIVE to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02516 | CG-ALL-9914 | Script gap | Product owner | The story adds DISPOSAL_PAUSED_DEVIATION to the closed list LOV-LISTING | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S5-E3029-APP | R-02517 | CG-ALL-9915 | Script gap | Product owner | The story adds FLOOR_APPROVED to the closed list LOV-SALE-CHANNEL | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5016-APP, RWB-S4-E5016-CON, RWB-S4-E5020-APP, RWB-S4-E5020-CON, RWB-S5-E4021-APP, RWB-S5-E4021-CON | R-09245 | GAP-1471 | Register gap | Head of Litigation | Enforcement after judgment and the eviction of a held property have no named owner role | Use the enforcement owner role the rules already name for enforcement, with Legal counsel named on an eviction, and record the assignment as an assumption until the operating model names the holder. |
| RWB-S5-E3026-APP | R-12824 | CG-ALL-9834 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3027-APP | R-12835 | CG-ALL-9859 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3028-APP | R-12846 | CG-ALL-9892 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3029-APP | R-12858 | CG-ALL-9930 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4021-APP | R-12867 | CG-ALL-9955 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4022-APP | R-12876 | CG-ALL-9979 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4023-APP | R-12881 | CG-ALL-10003 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E4024-APP | R-12895 | CG-ALL-10028 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S5-E3027-APP, RWB-S5-E3027-CON, RWB-S5-E3028-APP, RWB-S5-E3028-CON | R-23496 | GAP-1760 | Register gap | Solution architect with the model risk officer | The pricing agent proposes the route and the price, and Architecture v5 connects this service to no agent | Carry the recommendation and the price proposal as decisions of the disposal rule set, and treat the agent as an optional proposer used only through the rwb-agent contract with its 60 s limit, its fallback to the rule result and its run record; record the missing cell. |
| RWB-S5-E3028-APP, RWB-S5-E3028-CON, RWB-S5-E4025-APP, RWB-S5-E4025-CON | R-23503 | GAP-1763 | Register gap | Risk with the product heads | The floor approval ladder is named in amounts and percentages whose comparison signs cannot be read | Read every floor limit from the versioned delegation table of rwb-access at run time, carry the three amounts and the three percentages as stated, and treat the direction of the test as open until DL18 and Q-001 answer. |
| RWB-S5-E3028-APP, RWB-S5-E3028-CON | R-29165 | GAP-2883 | Register gap | P10 rwb-agent owner, P7 rwb-decision model risk owner | The price model, its version and the reserve basis of R-DIS-28 are not specified and no service owns the model | The P10 owner publishes the model reference and its version in the proposal and the model risk owner records the reserve basis with the model governance documents. |
| RWB-S5-E4023-APP, RWB-S5-E4023-CON | R-29173 | GAP-2904 | Register gap | Solution architect and the business owner of the Asset module | The FSD S5, the TSD S5 and the Epics 3 to 8 Specification that the two slices read are in review with empty sign-off tables and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes. |
| RWB-S5-E3028-APP | R-38410 | ASM-4779 | Register assumption |  | The price model and the reserve basis are the pricing agent own and are read from its answer as a model reference with its version; this service stores the reference in the decision record, computes no proposal and fixes no reserve basis. | The P10 rwb-agent owner and the model risk owner of rwb-decision |
| RWB-S5-E4023-APP, RWB-S5-E4023-CON, RWB-S5-E4031-APP, RWB-S5-E4031-CON | R-38441 | ASM-4802 | Register assumption |  | Both stories carry Status Draft (realignment v1) and the missing approval of the realigned stories and of the FSD S5, the TSD S5 and the Epics 3 to 8 Specification they read is treated as an assumption of this run rather than as a blocker; no behaviour and no value of either story depends on a signature and no status of a source document is changed. | The verification loop collects the sign-offs and only then changes the status of the stories. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S5-E3025-APP | R-29160 | GAP-2865 | 14 | The legacy data table names the custody of documents, which is P5's fact, and the legacy message set carries two price messages that no path of this step raises | Section 14 MSG-S5-001/002 rows and the section 11 Data table are not in this chunk, so no exact text to edit. Section 12.5 already has the custody cost with no document row read. Resubmit sections 11 and 14. |
| RWB-S5-E3026-APP | R-02491 | CG-ALL-9829 | 12.5 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | The AssetDisposalWorkflow row is not changed in the diff; the task queue cell still needs the catalog value. |
| RWB-S5-E3026-APP | R-08217 | DOR-RWB-S5-E3026-APP-8 | 12.5 | Definition of Ready item 8 Contract: Fail | The P1 queue row is not in the diff, and the +1 more item is not named in the source, so the item is not resolved. |
| RWB-S5-E3026-APP | R-20223 | DOR-RWB-S5-E3026-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 text is not in this chunk, so no exact old text exists to edit. The SCR-21/23 empty, loading, error and no-access states need that section. |
| RWB-S5-E3026-APP | R-20224 | DOR-RWB-S5-E3026-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Sections 11 and 17 are not in this chunk, so no exact old text exists. Per-field personal-data class needs Data Classification v5 and those sections. |
| RWB-S5-E3026-CON | R-20237 | DOR-RWB-S5-E3026-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | The fix needs new criteria in section 7 and test rows in section 16, which are not in this chunk. No AC or TC ID was invented; BR1 to BR12 stay unmapped. |
| RWB-S5-E3026-CON | R-20239 | DOR-RWB-S5-E3026-CON-7 | 11 | Definition of Ready item 7 Data: Partial | BR Field IDs for the 9 section 11 rows are not in the sources and cannot be added without inventing them. Legacy wording in section 7 is outside this chunk. |
| RWB-S5-E3027-APP | R-08225 | DOR-RWB-S5-E3027-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version is recorded as published. Searched 03 Requirements and specifications; the only fake reference is S3 NFR-S3-003, which is not S5. No value written. |
| RWB-S5-E3027-APP | R-20241 | DOR-RWB-S5-E3027-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | The story text listing the carried fields is not in this chunk, so no edit can be anchored. Needs the header or the field section of the story to resolve. |
| RWB-S5-E3027-APP | R-20247 | DOR-RWB-S5-E3027-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR11 to BR13 are already in section 8. BR1 to BR10 need section 7 criteria and section 16 test rows, which are not in this chunk, so no edit can be anchored. |
| RWB-S5-E3027-APP | R-27350 | CG-ALL-9860 | 7 | Criteria and tests keep legacy job and decision-log wording | Only AC1 and AC4 were changed. The other legacy job and decision-log lines were not located in the chunk, so the item is not fully resolved. |
| RWB-S5-E3028-CON | R-27366 | CG-ALL-9906 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | No JOB-nn, decision log or job record wording found in sections 7 or 16 of story v2. Only DP-03 (library name) and JOB-19 in section 12 match. Lines not located; left unchanged. |
| RWB-S5-E3029-APP | R-20284 | DOR-RWB-S5-E3029-APP-4 | 8, 16 | Definition of Ready item 4 Business rules: Partial | BR11 and BR12 rule text is not in §8. Add the rule definitions before this item is resolved; the tags are only valid once those rules exist. |
| RWB-S5-E4021-APP | R-20295 | DOR-RWB-S5-E4021-APP-11 | 12.3, 17 | Definition of Ready item 11 Guardrails: Partial | Hit is idempotency_key (Data Classification v5 Fields: Confidential / Customer data). The handling rule sits in §12.3 and §17, outside this chunk, and is not in the given text. |
| RWB-S5-E4021-APP | R-27378 | CG-ALL-9956 | 7, 12.5, 16 | Criteria and tests keep legacy job and decision-log wording | §12.5 already uses decision record with no legacy wording. Legacy lines in §7 and §16 are kept word for word by the change log, so changing them conflicts with it. |
| RWB-S5-E4022-APP | R-27386 | CG-ALL-9977 | 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | DOR-RWB-S5-E4022-APP-9 records the standard text as identical to the story, so no rewording is supported. |
| RWB-S5-E4022-CON | R-23510 | GAP-2895 |  | No published operation name for the rwb-source-data appraisal and asset product or for the rwb-case case-move answer | Consumed-row text (section 5) was not in the supplied story text, and no story .md exists in the folder. Operation names are not in any source. Change log already names GAP-2895. |
| RWB-S5-E4022-CON | R-23511 | GAP-2896 |  | listing names no column for the per-round price that R-DIS-38 steps down | The listing-section text and round-price row were not supplied. Change log already names GAP-2896 and ASM-4793. The column name is not in any source. |
| RWB-S5-E4022-CON | R-23512 | GAP-2897 |  | API-S5-004 is claimed by the pricing story and by the price step, and no source splits it | The API-S5-004 ownership text was not supplied. No story .md found in the folder. Change log already names GAP-2897. The operation split is not in the sources. |
| RWB-S5-E4022-CON | R-29168 | GAP-1754 |  | The round operation and the REST base are named differently on the architecture slide, in the TSD and in the Ownership Map | Header already fixes base /api/recovery/asset/v1. The operation-path text (section 5 or 9) was not supplied, so no edit could anchor. Paths are in the Ownership Map. |
| RWB-S5-E4023-APP | R-08277 | DOR-RWB-S5-E4023-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off wording exists in the project sources (Grep for 'epic design' outside 23 Document Gaps: no match). Sign-off cannot be confirmed; left open. |
| RWB-S5-E4023-APP | R-12883 | CG-ALL-9993 | 4 | Name `vendor_capacity` is not a field or entity in LDM v9 or Data Classification v5 | vendor_capacity is not a field or entity in LDM v9 or Data Classification v5. Lines 55 and 175 are outside this chunk and still need their own edit, so the item is not resolved. |
| RWB-S5-E4024-APP | R-08288 | DOR-RWB-S5-E4024-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources (prior search of the project folder). The header placeholder stays until the sign-off record is supplied. |
| RWB-S5-E4024-APP | R-12891 | CG-ALL-10023 | 12.1 | HTTP errors with no message ID: 400; 401; 404; 409 for a listing that is not live or a round out of order; 503 when a library or a contract does not answer | Error and Message Standard v4 has no HTTP status mapping, so 503 is not tied to MSG-GEN-006 either. All five codes stay Not specified; BA to confirm. |
| RWB-S5-E4024-APP | R-20349 | DOR-RWB-S5-E4024-APP-10 | SCR-21, SCR-24 (not in supplied parts) | Definition of Ready item 10 Screens and states: Partial | Screen-state text for SCR-21 and SCR-24 is outside the supplied story parts, so there is no exact anchor for an edit. |
| RWB-S5-E4024-APP | R-20350 | DOR-RWB-S5-E4024-APP-11 | not in supplied parts | Definition of Ready item 11 Guardrails: Partial | P2 fields classed as personal data are not named in the supplied parts; they cannot be reconciled with BR10 or section 17 from this chunk. |
| RWB-S5-E4024-APP | R-20355 | DOR-RWB-S5-E4024-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR IDs beyond BR10 are not in the sources. Criteria and tests for BR1 to BR10 still open and need a QA decision. |
| RWB-S5-E4024-APP | R-23522 | GAP-2914 | 12.5 | The legacy endpoints table names the listings write for the accept while the TSD gives the round write the sale answer | Legacy endpoint row sits outside this chunk and is not edited, so the gap is not resolved here. |
| RWB-S5-E4024-APP | R-23524 | GAP-2927 | 7 | Legacy AC2, AC3 and the FSD A2.18 rule list name R-DIS-11 and R-DIS-37, rules of the work order and the auction round, not the payment term | AC2 and AC3 text in section 7 is unchanged and sits outside this chunk. |
| RWB-S5-E4024-APP | R-27405 | CG-ALL-10029 | 7, 16 (not in supplied parts) | Criteria and tests keep legacy job and decision-log wording | The three legacy criterion and test lines are in sections 7 and 16, outside the supplied parts. Section 12.5 has no legacy wording to change. |
| RWB-S5-E4024-CON | R-02551 | CG-ALL-10034 | 12.5 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | The queue row is not changed in this diff; it needs the rwb-recovery namespace and the rwb-asset queue value. |
| RWB-S5-E4024-CON | R-08295 | DOR-RWB-S5-E4024-CON-16 | Header | Definition of Ready item 16 Size: Fail | No size value in the source documents; the row carries the placeholder. |
| RWB-S5-E4024-CON | R-08296 | DOR-RWB-S5-E4024-CON-23 | find it | Definition of Ready item 23 Contract version fixed: Fail | No contract version number in sources. Searched all .md files in the folder: PRD S5 rwb-asset and FSD S5 v4 give only REST base /api/recovery/asset/v1. A version is not invented. |
| RWB-S5-E4024-CON | R-08297 | DOR-RWB-S5-E4024-CON-3 | 7 | Definition of Ready item 3 Acceptance criteria: Fail | Section 16 is in the story and can take a test row; the AC3 wording is not in the source documents, so no criterion is added. |
| RWB-S5-E4024-CON | R-20361 | DOR-RWB-S5-E4024-CON-15 | header | Definition of Ready item 15 INVEST: Partial | The 'Small, fits within two weeks' value is not in the source documents and was removed. |
| RWB-S5-E4024-CON | R-32693 | NEWAC-RWB-S5-E4024-CON-AC5 | 7 | AC5: activity retry and timeout (no criterion covers a retried or timed-out activity) | Section 7 closing sentence still says seven criteria; the text is outside the diff and needs editing. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (45)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17805 | RWB-S5-E3025-APP | CG-ALL-9798 | 12.2 | Declare REST base /api/recovery/source-data/v1 as given in the Document Index service table. |
| CDC-17806 | RWB-S5-E3025-APP | CG-ALL-9799 | 12.2 | Declare REST base /api/recovery/case/v1 as given in the Document Index service table. |
| CDC-17825 | RWB-S5-E3025-CON | CG-ALL-9815 | 12.2 | Declare REST base /api/recovery/source-data/v1 from the Document Index service table. |
| CDC-17826 | RWB-S5-E3025-CON | CG-ALL-9816 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-17829 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-8 | 12 | Publish the cost-write operation and the source-data and case REST bases; the task queue is already fixed in the story. |
| CDC-17843 | RWB-S5-E3026-APP | CG-ALL-9827 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the rwb-source-data operations, taken from the Document Index service table. |
| CDC-17844 | RWB-S5-E3026-APP | CG-ALL-9828 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case operations, taken from the Document Index service table. |
| CDC-17857 | RWB-S5-E3026-CON | CG-ALL-9839 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data, taken from the Document Index service table |
| CDC-17858 | RWB-S5-E3026-CON | CG-ALL-9840 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, taken from the Document Index service table |
| CDC-17886 | RWB-S5-E3028-APP | CG-ALL-9885 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases/{caseId} family (read). |
| CDC-17887 | RWB-S5-E3028-APP | CG-ALL-9886 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the asset and COLLINS fact read. |
| CDC-17888 | RWB-S5-E3028-APP | CG-ALL-9887 | 12.2 | Declare REST base /api/recovery/valuation/v1 for the appraisal read. |
| CDC-17909 | RWB-S5-E3028-CON | CG-ALL-9899 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case (P3) in the yaml. |
| CDC-17910 | RWB-S5-E3028-CON | CG-ALL-9900 | 12.2 | Declare REST base /api/recovery/source-data/v1 for rwb-source-data (P1) in the yaml. |
| CDC-17911 | RWB-S5-E3028-CON | CG-ALL-9901 | 12.2 | Declare REST base /api/recovery/valuation/v1 for rwb-valuation (S1) in the yaml. |
| CDC-17913 | RWB-S5-E3028-CON | DOR-RWB-S5-E3028-CON-8 | 12.2 | Declare the three REST bases (CG-ALL-9899 to CG-ALL-9901); the task queue is fixed in the story. |
| CDC-17926 | RWB-S5-E3029-APP | CG-ALL-9920 | 12.2 | Declare REST base /api/recovery/source-data/v1 for provider P1 rwb-source-data, using the Document Index service table. |
| CDC-17927 | RWB-S5-E3029-APP | CG-ALL-9921 | 12.2 | Declare REST base /api/recovery/document/v1 for provider P5 rwb-document, using the Document Index service table. |
| CDC-17928 | RWB-S5-E3029-APP | CG-ALL-9922 | 12.2 | Declare REST base /api/recovery/deviation/v1 for provider S8 rwb-deviation, using the Document Index service table. |
| CDC-17929 | RWB-S5-E3029-APP | CG-ALL-9923 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case, using the Document Index service table. |
| CDC-17930 | RWB-S5-E3029-APP | CG-ALL-9924 | 12.2 | Declare REST base /api/recovery/integration/v1 for provider P2 rwb-integration, using the Document Index service table. |
| CDC-17934 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-8 | 12 | Add base paths /api/recovery/source-data/v1, /api/recovery/document/v1, /api/recovery/deviation/v1, /api/recovery/case/v1 and the five further paths in the detcheck output. |
| CDC-17945 | RWB-S5-E3029-CON | CG-ALL-9935 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the provider named in the Document Index service table |
| CDC-17946 | RWB-S5-E3029-CON | CG-ALL-9936 | 12.2 | Declare the REST base /api/recovery/document/v1 for the provider named in the Document Index service table |
| CDC-17947 | RWB-S5-E3029-CON | CG-ALL-9937 | 12.2 | Declare the REST base /api/recovery/deviation/v1 for the provider named in the Document Index service table |
| CDC-17948 | RWB-S5-E3029-CON | CG-ALL-9938 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider named in the Document Index service table |
| CDC-17949 | RWB-S5-E3029-CON | CG-ALL-9939 | 12.2 | Declare the REST base /api/recovery/integration/v1 for the provider named in the Document Index service table |
| CDC-17952 | RWB-S5-E3029-CON | DOR-RWB-S5-E3029-CON-8 | 12.2 | Declare the REST bases of the consumed paths in section 12.2 (source-data, document, deviation, case, integration) |
| CDC-17963 | RWB-S5-E4021-APP | CG-ALL-9950 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case provider, using the REST base in the Document Index service table. |
| CDC-17983 | RWB-S5-E4022-APP | CG-ALL-9971 | 12.2 | Declare REST base /api/recovery/source-data/v1 in the yaml. |
| CDC-17984 | RWB-S5-E4022-APP | CG-ALL-9972 | 12.2 | Declare REST base /api/recovery/case/v1 in the yaml. |
| CDC-17988 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-8 | 12.2 | Declare both REST bases; add message IDs for 400, 401, 404, 409 and 503 in section 14. |
| CDC-17999 | RWB-S5-E4022-CON | CG-ALL-9984 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for P1 rwb-source-data, taken from the Document Index service table |
| CDC-18000 | RWB-S5-E4022-CON | CG-ALL-9985 | 12.2 | Declare the REST base /api/recovery/case/v1 for P3 rwb-case, taken from the Document Index service table |
| CDC-18002 | RWB-S5-E4022-CON | DOR-RWB-S5-E4022-CON-8 | 12.2 | Declare REST bases for /api/recovery/source-data/v1 and /api/recovery/case/v1; the workflow ID and start rule are stated in 12.5 |
| CDC-18009 | RWB-S5-E4023-APP | CG-ALL-9995 | 12.2 | Declare the REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-18010 | RWB-S5-E4023-APP | CG-ALL-9996 | 12.2 | Declare the REST base /api/recovery/source-data/v1 using the provider's base from the Document Index service table. |
| CDC-18014 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-8 | 12.5 | Declare the REST bases for /api/recovery/case/v1 and /api/recovery/source-data/v1 (CG-ALL-9995 and CG-ALL-9996). |
| CDC-18024 | RWB-S5-E4023-CON | CG-ALL-10010 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table; the story already uses this base. |
| CDC-18025 | RWB-S5-E4023-CON | CG-ALL-10011 | 12.2 | Declare the REST base /api/recovery/source-data/v1 from the Document Index service table; the operation name stays Not specified in the source documents. |
| CDC-18026 | RWB-S5-E4023-CON | DOR-RWB-S5-E4023-CON-8 | 12.1, 12.2, 12.5 | Declare REST bases /api/recovery/case/v1 and /api/recovery/source-data/v1. Story-side items (own operation, task queue) are resolved. |
| CDC-18033 | RWB-S5-E4024-APP | CG-ALL-10022 | 12.2 | Add the REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |
| CDC-18036 | RWB-S5-E4024-APP | DOR-RWB-S5-E4024-APP-8 | 12.5 | Add the REST base /api/recovery/case/v1 for the rwb-case provider; the yaml part of the check is not in this story. |
| CDC-18043 | RWB-S5-E4024-CON | CG-ALL-10033 | 12.2 | Declare the REST base /api/recovery/case/v1 for GET /cases/{caseId} (rwb-case). |
| CDC-18045 | RWB-S5-E4024-CON | DOR-RWB-S5-E4024-CON-8 | 12.5 | Declare the REST base /api/recovery/case/v1 (CG-ALL-10033); the other detcheck lines are resolved in the story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (27)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17816 | RWB-S5-E3025-APP | CG-ALL-9802 | 12.5 | Add activity recordHoldingCost (design name, task queue rwb-asset, in AssetDisposalWorkflow) to the Activities sheet, or use a catalogued activity. |
| CDC-17817 | RWB-S5-E3025-APP | CG-ALL-9803 | 12.5 | Add activity raiseWorkOrder (design name, task queue rwb-asset, in AssetDisposalWorkflow) to the Activities sheet, or use a catalogued activity. |
| CDC-17818 | RWB-S5-E3025-APP | CG-ALL-9804 | 12.5 | Add activity applyWorkOrderAnswer (design name, task queue rwb-asset, in AssetDisposalWorkflow) to the Activities sheet, or use a catalogued activity. |
| CDC-17827 | RWB-S5-E3025-CON | CG-ALL-9817 | 12.5 | Namespace restored in the table to match the naming line at L41; no story edit |
| CDC-17834 | RWB-S5-E3025-CON | CG-ALL-9819 | 12.5 | Add an Activities row recordHoldingCost for rwb-asset, or name a catalogued activity in its place. |
| CDC-17835 | RWB-S5-E3025-CON | CG-ALL-9820 | 12.5 | Add an Activities row raiseWorkOrder for rwb-asset, or name a catalogued activity in its place. |
| CDC-17851 | RWB-S5-E3026-APP | CG-ALL-9831 | 12.5 | Add activity orderReappraisal to the Activities sheet, or name a catalogued activity in the story. |
| CDC-17863 | RWB-S5-E3026-CON | CG-ALL-9843 | 12.5 | Add an Activities row for orderReappraisal on task queue rwb-asset, or name a catalogued activity instead; the solution architect decides. |
| CDC-17870 | RWB-S5-E3027-APP | DOR-RWB-S5-E3027-APP-8 | 12.5 | Add activities recommendDisposalRoute, releaseAssetToHold and recordRouteRecommendation (plus the one further flagged activity) to the Workflows and activities list. Task queue now matches as rwb-asset; Workflow ID form and start rule are marked not specified in 12.5. |
| CDC-17875 | RWB-S5-E3027-APP | CG-ALL-9854 | 12.5 | Add a row for activity recommendDisposalRoute on task queue rwb-asset, or name a catalogued activity in the story. Owner: Solution architect. |
| CDC-17876 | RWB-S5-E3027-APP | CG-ALL-9855 | 12.5 | Add a row for activity releaseAssetToHold on task queue rwb-asset, or name a catalogued activity in the story. Owner: Solution architect. |
| CDC-17877 | RWB-S5-E3027-APP | CG-ALL-9856 | 12.5 | Add a row for activity recordRouteRecommendation on task queue rwb-asset, or name a catalogued activity in the story. Owner: Solution architect. |
| CDC-17915 | RWB-S5-E3028-CON | CG-ALL-9904 | 12.5 | Add activity setStartAndFloorPrice to the Activities sheet, or name the catalogued activity that performs the pricing step. |
| CDC-17939 | RWB-S5-E3029-APP | CG-ALL-9927 | 12.5 | Add activity publishListing on task queue rwb-asset with the contract element given in section 12.5. |
| CDC-17940 | RWB-S5-E3029-APP | CG-ALL-9928 | 12.5 | Add activity pauseListing on task queue rwb-asset with the contract element given in section 12.5. |
| CDC-17953 | RWB-S5-E3029-CON | CG-ALL-9942 | 12.5 | Add an Activities row for publishListing on task queue rwb-asset, or name a catalogued activity instead. |
| CDC-17954 | RWB-S5-E3029-CON | CG-ALL-9943 | 12.5 | Add an Activities row for pauseListing on task queue rwb-asset, or name a catalogued activity instead. |
| CDC-17969 | RWB-S5-E4021-APP | CG-ALL-9953 | 12.5 | Add an Activities row for openEviction on task queue rwb-asset, or name a catalogued activity in the story. |
| CDC-17991 | RWB-S5-E4022-APP | CG-ALL-9976 | 12.5 | Add activity stepDownPrice to the Activities sheet on task queue rwb-asset, with the contract element in section 12.5, or name a catalogued activity. |
| CDC-18003 | RWB-S5-E4022-CON | CG-ALL-9988 | 12.5 | Add activity stepDownPrice to the Activities sheet on task queue rwb-asset |
| CDC-18011 | RWB-S5-E4023-APP | CG-ALL-9997 | 12.5 | Story already reads rwb-asset in 12.5 and the header; no story edit made |
| CDC-18015 | RWB-S5-E4023-APP | CG-ALL-10000 | 12.5 | Add the rwb-partner vendor-panel activity to the Activities sheet on queue rwb-partner, or name a catalogued activity; its name is Not specified in the source documents (GAP-2901; ASM-4799). |
| CDC-18018 | RWB-S5-E4023-APP | CG-ALL-9999 | 12.5 | Add activity allocateVendor on queue rwb-asset to the Activities sheet, or name a catalogued activity. |
| CDC-18027 | RWB-S5-E4023-CON | CG-ALL-10014 | 12.5 | Add an Activities row for allocateVendor (activity, queue rwb-asset, contract element as in section 12.5), or name a catalogued activity. |
| CDC-18028 | RWB-S5-E4023-CON | CG-ALL-10015 | 12.5 | Add an Activities row for the rwb-partner vendor-panel activity on queue rwb-partner, name Not specified in the source documents (GAP-2901; ASM-4799). |
| CDC-18038 | RWB-S5-E4024-APP | CG-ALL-10026 | 12.5 | Add activity reportAuctionRound to the Activities sheet, or the story uses a catalogued activity |
| CDC-18046 | RWB-S5-E4024-CON | CG-ALL-10036 | 12.5 | Add an Activities row for reportAuctionRound on task queue rwb-asset, or the story must use a catalogued activity. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (27)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17819 | RWB-S5-E3025-APP | CG-ALL-9805 | 16 | Add rows TC-E3-025-01 to TC-E3-025-05 with Given, When and Then copied from the criteria they cover (AC1 to AC3, the access case, principle 5). |
| CDC-17838 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E3-025-01 to -05 and TC-S5-E3025-CON-01 to -05. |
| CDC-17842 | RWB-S5-E3025-CON | CG-ALL-9821 | 16 | Add rows for TC-E3-025-01 to -05 and TC-S5-E3025-CON-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-17852 | RWB-S5-E3026-APP | CG-ALL-9832 | 16 | Add rows TC-E3-026-01 to TC-E3-026-06, and TC-E3-026-07 and TC-E3-026-08, with Given, When and Then copied from the criteria they cover. |
| CDC-17865 | RWB-S5-E3026-CON | DOR-RWB-S5-E3026-CON-12 | 12.7, 16 | Add rows for TC-E3-026-01 to -06 and TC-S5-E3026-CON-01 to -05 under the same IDs. |
| CDC-17867 | RWB-S5-E3026-CON | CG-ALL-9844 | 16 | Add rows for TC-E3-026-01 to -06 and TC-S5-E3026-CON-01 to -04, with Given, When and Then copied from the criterion each covers. |
| CDC-17878 | RWB-S5-E3027-APP | CG-ALL-9858 | 16 | Add rows TC-E3-027-01 to TC-E3-027-06 with Given, When and Then copied from AC1 to AC4 and the Access and Principle 5 cases in section 16. Owner: QA. |
| CDC-17883 | RWB-S5-E3027-CON | DOR-RWB-S5-E3027-CON-12 | 12.7, 16 | Add Story test cases tab rows for TC-E3-027-01 to -06 and TC-S5-E3027-CON-01 to -09. Boundary test TC-S5-E3027-CON-06 added in section 16. |
| CDC-17885 | RWB-S5-E3027-CON | CG-ALL-9871 | 16 | Add rows for TC-E3-027-01 to TC-E3-027-06 and TC-S5-E3027-CON-01 to TC-S5-E3027-CON-05, with Given, When and Then copied from the criterion each covers. |
| CDC-17898 | RWB-S5-E3028-APP | CG-ALL-9891 | 16 | Add rows TC-E3-028-01 to TC-E3-028-06 with Given, When and Then copied from the criterion each one covers. |
| CDC-17899 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-12 | 12, 12.7, 16 | Section 16 now has sixteen rows, TC-E3-028-01 to TC-E3-028-16; the v8 workbook must carry all sixteen rows. |
| CDC-17918 | RWB-S5-E3028-CON | DOR-RWB-S5-E3028-CON-12 | 16 | Add rows under Story test cases for TC-E3-028-01 to -06 and TC-S5-E3028-CON-01 to -05. |
| CDC-17924 | RWB-S5-E3028-CON | CG-ALL-9905 | 16 | Add rows for TC-E3-028-01 to -06 and TC-S5-E3028-CON-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-17941 | RWB-S5-E3029-APP | CG-ALL-9929 | 16 | Add rows TC-E3-029-01 to TC-E3-029-06 with Given, When and Then copied from the criterion each row covers in section 16 |
| CDC-17956 | RWB-S5-E3029-CON | DOR-RWB-S5-E3029-CON-12 | 12.7, 16 | Add rows for TC-E3-029-01 to -06 and TC-S5-E3029-CON-01 to -04. The §12.7 boundary test is TC-S5-E3029-CON-05 in the story. |
| CDC-17960 | RWB-S5-E3029-CON | CG-ALL-9944 | 16 | Add rows for TC-E3-029-01 to -06 and TC-S5-E3029-CON-01 to -04 with Given, When and Then copied from the criteria they cover |
| CDC-17970 | RWB-S5-E4021-APP | CG-ALL-9954 | 16 | Add rows TC-E4-021-01 to TC-E4-021-05 to Story test cases, Given, When and Then copied from the section 7 criterion each covers. |
| CDC-17979 | RWB-S5-E4021-CON | DOR-RWB-S5-E4021-CON-12 | 16 | Add rows for TC-E4-021-01 to TC-E4-021-05 and TC-S5-E4021-CON-01 to TC-S5-E4021-CON-05 under the same IDs. |
| CDC-17980 | RWB-S5-E4021-CON | CG-ALL-9965 | 16 | Add rows for TC-E4-021-01 to TC-E4-021-05 and TC-S5-E4021-CON-01 to TC-S5-E4021-CON-04 with Given, When and Then copied from the criteria they cover. |
| CDC-17992 | RWB-S5-E4022-APP | CG-ALL-9978 | 16 | Add rows TC-E4-022-01 to -06 to the next version, tab Story test cases, with Given, When and Then copied from the criteria. Also add TC-E4-022-07 and -08. |
| CDC-18005 | RWB-S5-E4022-CON | DOR-RWB-S5-E4022-CON-12 | 12.7, 16 | Add tab Story test cases rows for TC-E4-022-01 to -06 and TC-S5-E4022-CON-01 to -13 |
| CDC-18008 | RWB-S5-E4022-CON | CG-ALL-9989 | 16 | Add rows for TC-E4-022-01, TC-E4-022-02, TC-E4-022-03, TC-E4-022-04, TC-E4-022-05, TC-E4-022-06, TC-S5-E4022-CON-01, TC-S5-E4022-CON-02, TC-S5-E4022-CON-03 and TC-S5-E4022-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18016 | RWB-S5-E4023-APP | CG-ALL-10002 | 16 | Add rows TC-E4-023-01 to TC-E4-023-06 with Given, When and Then copied from the criteria they cover (AC1 to AC4, Access, Principle 5). |
| CDC-18031 | RWB-S5-E4023-CON | CG-ALL-10017 | 16 | Add rows for TC-E4-023-01 to TC-E4-023-06 and TC-S5-E4023-CON-01 to TC-S5-E4023-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-18039 | RWB-S5-E4024-APP | CG-ALL-10027 | 16 | Add rows for TC-E4-024-01 to -05 under Story test cases with Given, When and Then from AC1 to AC3 |
| CDC-18048 | RWB-S5-E4024-CON | DOR-RWB-S5-E4024-CON-12 | 16 | Add the nine TC IDs named in the detcheck (TC-E4-024-01 to -05, TC-S5-E4024-CON-01 to -04) to tab Story test cases. |
| CDC-18051 | RWB-S5-E4024-CON | CG-ALL-10037 | 16 | Add rows for TC-E4-024-01 to TC-E4-024-05 and TC-S5-E4024-CON-01 to TC-S5-E4024-CON-04, with Given, When and Then copied from the criterion each covers. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17821 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-7 | 11 | Register or align holding_cost_to_date, holding_status, decision_record, recovery_svc and the one further name in the detcheck with the DF-COL and DF-ACE IDs now given in section 11. |
| CDC-17830 | RWB-S5-E3025-CON | CG-ALL-9810 | 11, 12.1, 12.7 | Record holding_status as a field of the asset entity, or give its dictionary name. |
| CDC-17831 | RWB-S5-E3025-CON | CG-ALL-9811 | 11, 12.1, 12.7 | Record holding_cost_to_date against DF-COL-042 in the dictionary, or give its dictionary name. |
| CDC-17832 | RWB-S5-E3025-CON | CG-ALL-9812 | 12.7 | Record decision_record as a PLT library table created in rwb_asset, or use the dictionary name for it. |
| CDC-17854 | RWB-S5-E3026-APP | DOR-RWB-S5-E3026-APP-7 | 11 | Hold DF-COL-028, DF-COL-029, DF-COL-031 and DF-COL-041; add one_year_rule_applied and relist_count as fields or entities of LDM v9 or Data Classification v5. |
| CDC-17872 | RWB-S5-E3027-APP | CG-ALL-9849 | 9 | Record holding_status as an asset field with domain LOV-HOLDING, or confirm the dictionary name; no entity or field of this name exists. |
| CDC-17880 | RWB-S5-E3027-APP | DOR-RWB-S5-E3027-APP-7 | 11 | Add asset fields DF-COL-028, DF-COL-029, DF-COL-031, DF-COL-033, DF-COL-037 and DF-COL-041 (holding_status). Legacy job wording kept per change log. |
| CDC-17894 | RWB-S5-E3028-APP | CG-ALL-9882 | 8 | Record asset_id as a listing field in rwb_asset under its dictionary name, or name the dictionary field that holds the asset key. |
| CDC-17935 | RWB-S5-E3029-APP | CG-ALL-9916 | 2; 4 | Add a field for photographs_count (rwb-document photograph count) or record it as a document-owned object under that name. |
| CDC-17936 | RWB-S5-E3029-APP | CG-ALL-9917 | 2; 4 | Add a field for inspection_report (rwb-document document) or record it as a document-owned object under that name. |
| CDC-17937 | RWB-S5-E3029-APP | CG-ALL-9918 | 2; 4 | Add a field for title_status (rwb-source-data asset fact) or record it as an asset-owned object under that name. |
| CDC-17938 | RWB-S5-E3029-APP | CG-ALL-9919 | 12.7 | Record decision_record as the platform library object created in rwb_asset (DP-03), as section 12.7 already states. |
| CDC-17967 | RWB-S5-E4021-APP | CG-ALL-9948 | none | Record decision_record as a platform library object created in rwb_asset (PLT library, DP-03), or record it in the owning document. |
| CDC-17968 | RWB-S5-E4021-APP | CG-ALL-9949 | none | Record inbox_event as a platform library object created in rwb_asset (PLT library, DP-09), or record it in the owning document. |
| CDC-17990 | RWB-S5-E4022-APP | CG-ALL-9969 | 11 | Name the dictionary field that holds the round price used by R-DIS-38, or add a round price field to listing (S5, rwb_asset). No field named price_at_round exists. |
| CDC-17995 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-7 | 11 | Confirm DF-COL-028 and DF-COL-042 as BR Field IDs of the asset entity (S5). Story side done: price_at_round and decision_record names replaced. |

### Epic design record (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17807 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-14 | header | Record the signed epic design sign-off, then confirm DoR item 14 as Pass. |
| CDC-17828 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S5 so the story can cite it. |
| CDC-17845 | RWB-S5-E3026-APP | DOR-RWB-S5-E3026-APP-14 | none | Record the signed epic design sign-off for RWB-S5-E3026-APP that Definition of Ready item 14 requires. |
| CDC-17859 | RWB-S5-E3026-CON | DOR-RWB-S5-E3026-CON-14 | find it | Record the signed epic design sign-off that DOR-RWB-S5-E3026-CON-14 requires for RWB-S5-E3026-CON; the story cannot confirm it. |
| CDC-17868 | RWB-S5-E3027-APP | DOR-RWB-S5-E3027-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S5 and confirm it to this story. |
| CDC-17881 | RWB-S5-E3027-CON | DOR-RWB-S5-E3027-CON-14 | find it | Record the signed sign-off of the epic design; no signed epic design is in the story or source documents. |
| CDC-17889 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-14 | find it | Record the signed epic design sign-off for RWB-S5-E3028-APP |
| CDC-17912 | RWB-S5-E3028-CON | DOR-RWB-S5-E3028-CON-14 |  | Record and confirm the signed epic design sign-off; no sign-off exists in the story or sources. |
| CDC-17931 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-14 | n/a | Record the signed epic design sign-off, which is absent from the story and source documents. |
| CDC-17950 | RWB-S5-E3029-CON | DOR-RWB-S5-E3029-CON-14 | header | Confirm and record the signed sign-off of the epic design for Service epic RWB-SVC-S5 |
| CDC-17964 | RWB-S5-E4021-APP | DOR-RWB-S5-E4021-APP-14 | none | Record the signed sign-off for the epic design of RWB-SVC-S5; no signed epic design is in the source documents. |
| CDC-17976 | RWB-S5-E4021-CON | DOR-RWB-S5-E4021-CON-14 | header | Confirm and record the signed epic design sign-off for RWB-SVC-S5. |
| CDC-17985 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-14 | header | Record the signed epic design sign-off. |
| CDC-18001 | RWB-S5-E4022-CON | DOR-RWB-S5-E4022-CON-14 |  | Record the signed epic design sign-off |
| CDC-18044 | RWB-S5-E4024-CON | DOR-RWB-S5-E4024-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S5 in the epic design record. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17836 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-1 | 1 | Record 'tech lead' as a role name there, or §1 names a role code that exists in that document. |
| CDC-17853 | RWB-S5-E3026-APP | DOR-RWB-S5-E3026-APP-6 | 10 | Add role SY-DATALOAD to Users Roles and Permissions v5 with the Asset and disposal rights of TSD S5 T6.1 that section 10 cites. |
| CDC-17864 | RWB-S5-E3026-CON | DOR-RWB-S5-E3026-CON-1 | 1 | Add a role row for tech lead of rwb-asset, or the story names an existing role code from the document. |
| CDC-17879 | RWB-S5-E3027-APP | DOR-RWB-S5-E3027-APP-6 | 10, 13 | Add role SY-DATALOAD to the role list. Story side: §13 now names the rwb-access guard as the authorise check; its check name is Not specified in the sources. |
| CDC-17900 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-6 | 10 | Add role SY-DATALOAD, which section 10 names, to the role list |
| CDC-17916 | RWB-S5-E3028-CON | DOR-RWB-S5-E3028-CON-1 | 1 | Add a role code or role name for the tech lead of rwb-asset, or confirm the role the story should use. |
| CDC-17943 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-6 | 10 | Add role SY-DATALOAD with its asset and disposal right as the access matrix gives it |
| CDC-17955 | RWB-S5-E3029-CON | DOR-RWB-S5-E3029-CON-1 | 1 | Add a role code or role name for tech lead of rwb-asset, or name the existing role this story maps to. |
| CDC-17971 | RWB-S5-E4021-APP | DOR-RWB-S5-E4021-APP-6 | 10 | Add role SY-DATALOAD, which section 10 of RWB-S5-E4021-APP uses. The rwb-access authorise check is recorded as Not specified in section 10. |
| CDC-17994 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-6 | 10 | Add role SY-DATALOAD or confirm its removal from section 10. Story side done: the rwb-access authorise check is now named per operation. |
| CDC-18004 | RWB-S5-E4022-CON | DOR-RWB-S5-E4022-CON-1 | 1 | Add a role code and name for 'tech lead' of rwb-asset, or confirm the existing role code §1 should use |
| CDC-18020 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-6 | 10 | Add role SY-DATALOAD (data-load identity, asset and disposal C) to the roles list, or withdraw it from section 10. |
| CDC-18029 | RWB-S5-E4023-CON | DOR-RWB-S5-E4023-CON-1 | 1 | Add a role name matching section 1's 'tech lead' (as in section 10, 'Tech lead of rwb-asset'), or map section 1 to an existing role code. |
| CDC-18040 | RWB-S5-E4024-APP | DOR-RWB-S5-E4024-APP-6 | 10 | Add role SY-DATALOAD, which section 10 uses for the round write, the award cancellation and the reopen. |
| CDC-18047 | RWB-S5-E4024-CON | DOR-RWB-S5-E4024-CON-1 | 1 | Add a role row for the technical lead persona used in section 1 (role code and name not specified in the source documents (DOR-RWB-S5-E4024-CON-1)). Story text unchanged; the Users Roles v5 role table has no tech lead row. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17812 | RWB-S5-E3025-APP | CG-ALL-9792 | 1, 4, 8, 11, 12.1, 12.7, 12.9, 13 | Add field holding_cost_to_date (DF-COL-042, asset in rwb_asset) to LDM v9 and Data Classification v5, or record the object in the owning document. |
| CDC-17813 | RWB-S5-E3025-APP | CG-ALL-9793 | 3, 5, 9, 11, 12.7 | Add field holding_status (DF-COL-041, asset in rwb_asset) to LDM v9 and Data Classification v5, or record the object in the owning document. |
| CDC-17814 | RWB-S5-E3025-APP | CG-ALL-9794 | 11, 12.7 | Record decision_record as the PLT library object created in rwb_asset (DP-03) in LDM v9 and Data Classification v5, or in the owning PLT library document. |
| CDC-17840 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-7 | 11 | Declare holding_status, holding_cost_to_date and decision_record as LDM v9 or Data Classification v5 fields or entities. |
| CDC-17849 | RWB-S5-E3026-APP | CG-ALL-9825 | 4, 11, 12.2, 12.8 | Record one_year_rule_applied as a dictionary field, or record the object in the owning document. Nearest name next_action_rule_id is not equivalent. |
| CDC-17850 | RWB-S5-E3026-APP | CG-ALL-9826 | 11 | Record relist_count as a dictionary field, or record the object in the owning document. Nearest name case_list_count is not equivalent. |
| CDC-17874 | RWB-S5-E3027-APP | CG-ALL-9851 | 12.1, 13 | Add route_recommendation as a named field, or record the object (API-S5-002 element at lines 249 and 356) in the owning document under a dictionary name. Owner: Data. |
| CDC-17895 | RWB-S5-E3028-APP | CG-ALL-9883 | 8 | Record outlier_flag as a field of the appraisal (S1) read, or use the dictionary name for the outlier flag. |
| CDC-17896 | RWB-S5-E3028-APP | CG-ALL-9884 | 12.7 | Record decision_record as a platform decision-record library object in rwb_asset (DP-03), or use the dictionary name. |
| CDC-17901 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-7 | 11 | Add or confirm field IDs DF-COL-028 and DF-COL-042, and fields asset_id and outlier_flag and entity decision_record |
| CDC-17972 | RWB-S5-E4021-APP | DOR-RWB-S5-E4021-APP-7 | 11 | Add BR Field IDs DF-COL-028 and DF-COL-042, and add decision_record and inbox_event as fields or entities. |
| CDC-18021 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-7 | 11 | Register vendor_capacity (rwb-partner vendor panel) and decision_record (platform library object in rwb_asset) as fields or entities. |
| CDC-18037 | RWB-S5-E4024-APP | CG-ALL-10021 | 9, 11 | Section 11 states decision_record is not an LDM v9 or DC v5 entity. |
| CDC-18041 | RWB-S5-E4024-APP | DOR-RWB-S5-E4024-APP-7 | 11 | Record decision_record as a library object of rwb_asset (DP-03), or add it as an entity. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17848 | RWB-S5-E3026-APP | GAP-1750 | 12.2 | Add the missing S5 to P1 cell for reads of ACE views through rwb-source-data. Story side done: FSD field names carried in 12.2. |
| CDC-17855 | RWB-S5-E3026-APP | GAP-1758 | BR4 | Add the S5 to S1 cell to the slide 13 connection matrix; the order goes through rwb-valuation and the accepted value is read back on rwb-source-data. |
| CDC-17866 | RWB-S5-E3026-CON | GAP-1758 | 8 | Add the S5 to S1 cell to the connection matrix on slide 13. The story already orders via rwb-valuation API-S5-003 and reads appraisal via rwb-source-data. |
| CDC-17893 | RWB-S5-E3028-APP | GAP-1750 | 12.2 | Add S5 to the P1 cell of the connection matrix. Name rwb-source-data contract fields in the FSD S5 field catalog and A2 integration points in place of v_ace_* views. Confirm contract fields, business key and freshness with P1. |
| CDC-17903 | RWB-S5-E3028-APP | GAP-2877 | 12.5 | P10 publishes the pricing proposal operation with its model reference; P1 publishes the asset and COLLINS fact; architecture adds the arrows P10 and P1 to S5 with call type. |
| CDC-17904 | RWB-S5-E3028-APP | GAP-2878 | 4 | S1 rwb-valuation publishes the appraisal read; architecture adds the S5 to S1 arrow; S5 data owner confirms whether a listing copy of the appraised value is needed. |
| CDC-17914 | RWB-S5-E3028-CON | GAP-1750 | 12.2 | Add the S5 to P1 cell as a read through rwb-source-data only, with no direct ACE view read. |
| CDC-17919 | RWB-S5-E3028-CON | GAP-2877 | 11 | Publish the proposal operation with its model reference and the asset and COLLINS fact, or state the call type (REST, event or Temporal activity) on slide 13. |
| CDC-17920 | RWB-S5-E3028-CON | GAP-2878 | 11 | S1 publishes the appraisal read on rwb-valuation; S5 data owner confirms whether an appraised-value copy is needed on the listing row. |
| CDC-17962 | RWB-S5-E3029-CON | GAP-1754 | All | Rebase API-S5-001 to API-S5-005 on /api/recovery/asset/v1 with the ACE business key; read POST /auction-rounds as the listing sub-resource |
| CDC-17989 | RWB-S5-E4022-APP | GAP-1750 | 12.2 | Add S5 to the P1 cell of the connection matrix. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17822 | RWB-S5-E3025-APP | GAP-1752 | 12.7 | Add rows for the S5 auction round, bid, holding-cost movement, award and work order under rwb_asset before the S5 DB story starts. |
| CDC-17841 | RWB-S5-E3025-CON | GAP-1752 | find it | Add rows for the auction round, bid, award, holding cost and work order as rwb-asset entity groups before the S5 DB story starts. |
| CDC-17908 | RWB-S5-E3028-APP | GAP-2884 | 12.7 | Add the asset row with owner S5 at its next version; the DB story of the service creates the table in schema rwb_asset |
| CDC-17925 | RWB-S5-E3028-CON | GAP-2884 | 12.7 | Add the asset row with owner S5 (S5 rwb-asset data owner) at its next version; the DB story of the service creates asset in schema rwb_asset |
| CDC-17996 | RWB-S5-E4022-APP | GAP-1752 | 11 | Add rows for auction round, bid, award, holding cost and work order as S5 entity groups of rwb_asset. Story side done in section 11. |
| CDC-18006 | RWB-S5-E4022-CON | GAP-1752 | 12.7 | Add S5 rows for auction round, bid, award, holding cost and work order of rwb_asset before the S5 DB story starts |
| CDC-18042 | RWB-S5-E4024-APP | GAP-1752 | find it | Add rows for round, bid, award, holding cost and work order as service entity groups; physical names left to the DB story. |
| CDC-18049 | RWB-S5-E4024-CON | GAP-1752 | 12.7 | Add rows for the auction round, the bid and the holding cost of rwb_asset before the S5 DB story starts. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17810 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-5 | 9 | Owner to confirm whether ASSET_HELD is added to the closed list of LOV-HOLDING; the source defines only HELD. |
| CDC-17815 | RWB-S5-E3025-APP | CG-ALL-9796 |  | Add list LOV-HOLDING-COST to Reference Data v5 Lists, or use an existing Reference Data v5 list. |
| CDC-17820 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-20 | 11 | Add list LOV-HOLDING-COST with the values maintenance, insurance and custody as section 11 names them. |
| CDC-17833 | RWB-S5-E3025-CON | CG-ALL-9813 | find it | Add list LOV-HOLDING-COST (closed list of three cost kinds, BR5) to Lists. |
| CDC-17839 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-20 | 8 | Add list LOV-HOLDING-COST (closed list of three cost kinds) to Lists. |
| CDC-17907 | RWB-S5-E3028-APP | GAP-2881 | 4 | S5 data owner confirms the channel and status values the pricing step uses; P7 publishes the step schedule per asset class; the two legacy screen states are mapped to list values. |
| CDC-17923 | RWB-S5-E3028-CON | GAP-2881 | 16 | S5 owner confirms the channel and status values; P7 publishes the step schedule per asset class; map below-limit and published screen states to list values. |

### RWB-S5-E3026-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17846 | RWB-S5-E3026-APP | DOR-RWB-S5-E3026-APP-21 | none | Move build status from Not started to Done so the contract is published. |
| CDC-17847 | RWB-S5-E3026-APP | DOR-RWB-S5-E3026-APP-22 | none | Record a published contract fake library version for the contract. |
| CDC-17856 | RWB-S5-E3026-APP | GAP-2870 |  | Declare the appraisal reference, type, value and date as a view of the consumed fact, not as rwb_asset columns; publish the reason and route vocabulary; declare one_year_rule_applied and relist_count as versioned inputs with placeholder Not specified in the source documents (GAP-2870). |

### RWB-S5-E4021-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17965 | RWB-S5-E4021-APP | DOR-RWB-S5-E4021-APP-21 | none | Publish the contract so that its build status reads Done. |
| CDC-17973 | RWB-S5-E4021-APP | GAP-2892 | 11 | Declare the step operation as None with this gap, the eviction element with its type and source and no column, and name the asset table as S5's. |
| CDC-17974 | RWB-S5-E4021-APP | GAP-2893 | 12.5 | Declare the stage signal and case-move answer with placeholder element names, declare no event, and record the instruction call type to rwb-litigation as Not specified. |

### RWB-S5-E4022-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17986 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-21 | header | Set the build status of the contract story to Done once published. |
| CDC-17987 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-22 | header | Record the published contract fake library version. |
| CDC-17997 | RWB-S5-E4022-APP | GAP-2897 | 7 | Declare API-S5-004 once for both stories: pricing owns start price and floor approval; this step owns the input reset and the round price step. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17804 | RWB-S5-E3025-APP | CG-ALL-9797 | 12.1 | Publish the cost-write operation in rwb-asset.yaml through RWB-S5-E3025-CON, or remove the POST row from section 12.1. |
| CDC-17824 | RWB-S5-E3025-CON | CG-ALL-9814 | 12.1 | Publish the cost-write POST operation at /api/recovery/asset/v1 with its operation name, as used in 12.1. |

### RWB-S5-E3025-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17808 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-21 | header | Set build status from Not started to Done. |
| CDC-17809 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-22 | header | Publish a contract fake library version and record it against this story. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17811 | RWB-S5-E3025-APP | DOR-RWB-S5-E3025-APP-8 | 12.1, 12.5 | Add the cost write POST path (operation name per GAP-2862) to rwb-asset.yaml; add bases /api/recovery/source-data/v1 and /api/recovery/case/v1 to their yamls; align the task queue rwb-asset with the catalog. |
| CDC-17892 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-8 | 12.2 | Add the yaml paths for /api/recovery/case/v1, /api/recovery/source-data/v1 and /api/recovery/valuation/v1; align the AssetDisposalWorkflow task queue with the catalog. |

### OTHER:(no target) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17860 | RWB-S5-E3026-CON | DOR-RWB-S5-E3026-CON-8 | 12.2, 12.5 | Listed P1s and P2 closed via CG-ALL-9839/9840/9841/9842 rows |
| CDC-17861 | RWB-S5-E3026-CON | GAP-1479 | 12.2 | E3 valuation order read against the published rwb-valuation contract and fake |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17897 | RWB-S5-E3028-APP | CG-ALL-9890 | 12.5 | Add the activity setStartAndFloorPrice on task queue rwb-asset, or replace it with a catalogued activity. |
| CDC-17978 | RWB-S5-E4021-CON | CG-ALL-9964 | 12.5 | Add activity openEviction with its inputs and outputs. |

### RWB-PLT-N001-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17917 | RWB-S5-E3028-CON | DOR-RWB-S5-E3028-CON-10 | find it | Add empty, loading, error and no-access states for SCR-21 and SCR-23. |
| CDC-18030 | RWB-S5-E4023-CON | DOR-RWB-S5-E4023-CON-10 | find it | Add empty, loading, error and no-access states for SCR-21 and SCR-23 to the screen definitions. |

### RWB-S5-E3029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17932 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-21 | n/a | Move build status from Not started to Done once the contract is published. |
| CDC-17933 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-22 | n/a | Record the published contract fake library version. Version is not specified in the source documents. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17942 | RWB-S5-E3029-APP | DOR-RWB-S5-E3029-APP-11 | 17 | Align the personal-data class of idempotency_key (decision_log_entry, interaction) and asset_key (asset_sale, listing, v_ace_asset) with the story §17 statement that no personal data is carried. |
| CDC-18019 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-11 | 12.7 | Confirm which fields of this story's contract are classed as personal data; the story states none is carried, so either the classification or the statement must change. |

### OTHER:Run extract set (_work/msr/extract) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17944 | RWB-S5-E3029-APP | GAP-2887 | none | Add the FSD S5 and TSD S5 extracts to the run extract set before the verification loop and re-check the module section citations. |
| CDC-17961 | RWB-S5-E3029-CON | GAP-2887 | All | Add the FSD S5 and TSD S5 extracts before the verification loop and re-check the module citations of this story |

### RWB-S5-E3029-APP; RWB-S5-E3029-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17957 | RWB-S5-E3029-CON | GAP-2886 | Header | Add DP-16 to the pattern set and C row RWB-P2-E1007-CON to the C list of both slices |
| CDC-17959 | RWB-S5-E3029-CON | GAP-2885 | 8 | Add REQ-S5-005 to the reqs list of both slices |

### API:(service not named); OTHER:P3) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17975 | RWB-S5-E4021-CON | CG-ALL-9961 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases/{caseId} family. |
| CDC-17977 | RWB-S5-E4021-CON | DOR-RWB-S5-E4021-CON-8 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /cases/{caseId} family. |

### OTHER:Recovery Workbench split plan, requirement rows (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17981 | RWB-S5-E4021-CON | GAP-2890 | 9 | Allocate a plan row for slice RWB-S5-E4021-APP citing REQ-S5-006 to REQ-S5-010 mapped to FEAT-AST-08 (TSD S5 v2 T8). |
| CDC-17982 | RWB-S5-E4021-CON | GAP-2894 | 1 | Header PRD reference cites the five module requirements |

### RWB-S5-E4024-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18034 | RWB-S5-E4024-APP | DOR-RWB-S5-E4024-APP-21 | Header | Complete the build of RWB-S5-E4024-CON (currently Not started) and publish the contract so its build status is Done. |
| CDC-18035 | RWB-S5-E4024-APP | DOR-RWB-S5-E4024-APP-22 | Header | Publish the contract fake library and record its published version. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:legacy criterion and FSD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17823 | RWB-S5-E3025-APP | GAP-2864 | 7, 16 | R-DIS-37 removed from the cost requirement anchors; AC2 kept word for word |

### RWB-S5-E3025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17837 | RWB-S5-E3025-CON | DOR-RWB-S5-E3025-CON-10 | find it | Give SCR-21 and SCR-22 empty, loading, error and no-access states. |

### OTHER:Connection matrix (P1 cell) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17862 | RWB-S5-E3026-CON | GAP-1750 | 12.2 | Add S5 to the P1 cell; story side done in 12.2 (FSD field names carried, contract fields and freshness to confirm with P1) |

### RWB-S5-E3027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17869 | RWB-S5-E3027-APP | DOR-RWB-S5-E3027-APP-21 | header | Set build status to Done before this story starts; it is currently Not started. |

### OTHER:rwb-source-data data-product contract (DP-05) and the connection matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17871 | RWB-S5-E3027-APP | GAP-1750 | find it | Carry the FSD asset, collateral and score field names as the source field names the contract returns; add S5 to the P1 cell of the connection matrix; confirm fields, business key and freshness response with P1 before wave 2 system test. |

### OTHER:Platform decision-record library (PLT library) specification (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17873 | RWB-S5-E3027-APP | CG-ALL-9850 | 11 | Record decision_record as a platform library object created in rwb_asset by the library migration (DP-03) in the owning document. |

### OTHER:Connection matrix (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17882 | RWB-S5-E3027-CON | GAP-1750 | find it | Add S5 to the P1 cell of the connection matrix for the ACE asset, collateral and score reads via rwb-source-data. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17884 | RWB-S5-E3027-CON | DOR-RWB-S5-E3027-CON-9 | 14 | Align MSG-P1-001 text with the standard, or record the difference there; section 14 wording is unchanged. |

### RWB-S5-E3028-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17890 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-21 | header | Set build status to Done (currently Not started). |

### OTHER:Contract fake library release record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17891 | RWB-S5-E3028-APP | DOR-RWB-S5-E3028-APP-22 | find it | Record a published contract fake library version for the contract RWB-S5-E3028-CON that this story builds against |

### OTHER:rwb-case service contract (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17902 | RWB-S5-E3028-APP | GAP-2876 | 13 | Publish the case state read and the case-move operation, or confirm the stage-outcome signal as the only boundary, before the wave 2 tag |

### OTHER:DISPOSAL package (P7 rwb-decision) and rwb-access (P4) delegated-authority table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17905 | RWB-S5-E3028-APP | GAP-2879 | 7 | P4 confirms the delegated-authority table; P7 places the floor percentage and approval limit in the DISPOSAL package at its next version and records the version in the decision record. |

### OTHER:rwb-decision (P7) approval child workflow contract and rwb-access (P4) role binding (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17906 | RWB-S5-E3028-APP | GAP-2880 | 7 | P7 publishes the approval child workflow request and answer elements; P4 confirms RW-HEADNPA is the role the floor approval asks for. |

### OTHER:Recovery Workbench DISPOSAL package (P7 rwb-decision) and the P4 rwb-access delegated-authority table (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17921 | RWB-S5-E3028-CON | GAP-2879 | 14 | Publish the floor percentage and approval limit for VR-S5-011-1 and MSG-S5-001 at a recorded version, and name the level that holds the limit. |

### OTHER:Temporal and Drools Design slide 12 (Approval DoA kit template) and TSD S5 T6.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17922 | RWB-S5-E3028-CON | GAP-2880 | 12.5 | P7 publishes the approval child request and answer elements; P4 confirms RW-HEADNPA is the role the floor approval asks for. |

### OTHER:Refinement sizing record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17951 | RWB-S5-E3029-CON | DOR-RWB-S5-E3029-CON-16 | header | Size row set to a Not specified placeholder citing DOR-RWB-S5-E3029-CON-16 |

### OTHER:TSD S5 T5.1 (INT-27) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17958 | RWB-S5-E3029-CON | GAP-1756 | 8 | BR5 reverted to the original wording; the bank channel interface absence is owned by INT-27. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17966 | RWB-S5-E4021-APP | DOR-RWB-S5-E4021-APP-8 | 12.5 | Add activity openEviction to AssetDisposalWorkflow in Temporal Catalog v1, and declare the REST base /api/recovery/case/v1 in the API yaml. Workflow ID form and start rule: Not specified in the source documents (DOR-RWB-S5-E4021-APP-8). |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17993 | RWB-S5-E4022-APP | DOR-RWB-S5-E4022-APP-10 | 9 | SCR-21 and SCR-23 list empty, error and no-access states as Not specified in the source documents |

### RWB-S5-E4022-CON; OTHER:TSD S5 T-A.1; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17998 | RWB-S5-E4022-APP | GAP-1754 | 7 | Publish GET /assets, GET /assets/{assetKey}, POST /assets/{assetKey}/listings and POST /listings/{listingId}/rounds under /api/recovery/asset/v1 with the ACE business key, with the round as a sub-resource of the listing; read slide 19 /auction-rounds as the same resource. |

### RWB-S5-E4026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18007 | RWB-S5-E4022-CON | GAP-2918 | find it | Declare R-DIS-38 once in the contract baseline and record the duplicate in RWB-S5-E4026 AC2 for the assembler to close. |

### RWB-S5-E4023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18012 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-21 | header | Move the build status from Not started to Done so the contract is published. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18013 | RWB-S5-E4023-APP | DOR-RWB-S5-E4023-APP-22 | header | Publish the contract fake and record its library version. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18017 | RWB-S5-E4023-APP | CG-ALL-9994 | 12.7 | Record decision_record as a library table in the library's owning document, or use the dictionary name. |

### OTHER:Plan dependency list, next revision (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18022 | RWB-S5-E4023-APP | GAP-2901 | 13 | Register a class C row for RWB-S5-E4023-APP covering the parent-forwarded DISPOSAL signals, the rwb-partner vendor-panel activity and the rwb-source-data asset and score product. |

### OTHER:rwb-partner contract (owner S9 rwb-partner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18023 | RWB-S5-E4023-APP | GAP-2905 | 12.5 | Publish the vendor-panel activity name and its answer fields; the story keeps the placeholder until then. |

### OTHER:Module requirements; OTHER:FSD S5 A2.14 (requirement row at step D1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18032 | RWB-S5-E4023-CON | GAP-2903 | find it | Traceability set to FEAT-AST-14 in the story; the vendor-allocation requirement row is added in the module requirements. |

### OTHER:Legacy RWB-E4-025 (Endpoints table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18050 | RWB-S5-E4024-CON | GAP-2914 |  | Endpoints table write for the accept must read POST /listings/{listingId}/rounds (API-S5-005) per TSD S5 T-A.2, not POST /assets/{assetId}/listings, which stays API-S5-004 for list price and floor. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0427 | The re-appraisal harness pack, the fixed clock, the SVAF interface and the evidence format are not specified | Integration lead | Resolved (directive) |
| GAP-1468 | The provision step thresholds and the held-asset re-appraisal interval are not specified | NPA and asset manager | Resolved (directive) |
| GAP-1479 | Epic 3 features depend on Epic 4 features that release a month later | Solution architect | Resolved (directive) |
| GAP-1750 | FSD S5 reads the ACE asset, collateral and score views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1752 | The Ownership Map lists no table for auction rounds, bids or holding costs, although Architecture v5 and the rules need them | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1754 | The round operation and the REST base are named differently on the architecture slide, in the TSD and in the Ownership Map | Solution architect | Resolved (directive) |
| GAP-1755 | The vendor allocation rule is written by distance in the FSD and by scorecard in the FSD's own rule row | Business analyst, S5 | Resolved (directive) |
| GAP-1756 | The listing must publish to the bank channel and the auction portal, and the bank channel interface does not exist | Solution architect with the integration lead | Resolved (directive) |
| GAP-1757 | The E4 vendor allocation depends on a partner capability delivered one wave later | Solution architect | Resolved (directive) |
| GAP-1758 | The re-appraisal order leaves for SVAF, which Architecture v5 does not connect to this service and gives to rwb-valuation | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2862 | The cost record has no owned operation, no closed list and no column of its own, and the only write the legacy endpoint table gives is the valuation order of another service | S5 rwb-asset service owner with the solution architect, the S1 rwb-valuation owner and the data steward | Resolved (directive) |
| GAP-2863 | The work order to the property services vendor has no owned operation, no vendor vocabulary and no instruction element, and the plan records no contract dependency although three owners are needed | S5 rwb-asset service owner with the S9 rwb-partner owner, the platform workflow kit owner and the P3 rwb-case owner | Resolved (directive) |
| GAP-2864 | R-DIS-37, the bid-in-round rule, is attached to a cost feature by the legacy criterion and the FSD, while the held-property work orders of the routing logic are R-DIS-10 to R-DIS-12 | S5 rwb-asset service owner with the P7 rwb-decision rule owner and the business analyst of S5 | Resolved (directive) |
| GAP-2865 | The legacy data table names the custody of documents, which is P5's fact, and the legacy message set carries two price messages that no path of this step raises | S5 rwb-asset service owner with the P5 rwb-document owner and the business analyst of S5 | Resolved (directive) |
| GAP-2866 | No requirement id covers FEAT-AST-07 in the technical specification and the plan carries no requirement for either slice | S5 rwb-asset service owner with the business analyst | Resolved (directive) |
| GAP-2867 | The contract baseline has no sourced element, closed list, answer shape or event for a holding cost, a work-order instruction or a case move, and the catalogue gives the service one event only | S5 rwb-asset service owner with the solution architect and the S9 rwb-partner and P3 rwb-case owners | Resolved (directive) |
| GAP-2868 | The connection matrix shows subscribes cells and Temporal cells towards four services, and no source names the events, the operations or the outbox library of this step | S5 rwb-asset service owner with the platform event library owner and the solution architect | Resolved (directive) |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-2870 | RWB-S5-E3026-CON: the published surface of the cycle has no source for its appraisal properties, its reason and route vocabulary, the order path or the JOB-19 parameters | Solution architect | Resolved (directive) |
| GAP-2871 | The trigger of the step, the home of the recommendation and the mapping of the five route words to a closed list have no single source | S5 rwb-asset service owner with the P3 rwb-case owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-2872 | The five consumed rows are class C in fact while both metadata rows carry None, the service holds no v_ace_* grant, and the asset table is absent from the ownership list | S5 rwb-asset service owner with the solution architect and the P1, P3, P7 and P10 owners | Resolved (directive) |
| GAP-2873 | The legacy key carries no requirement id in the story master and the module requirement set has none for the route recommendation | S5 rwb-asset service owner with the business analyst | Resolved (directive) |
| GAP-2874 | No source names an operation, an event or a representation for the disposal-route recommendation, so the element and its property are design names of the baseline | S5 rwb-asset service owner with the solution architect and the API contract owner | Resolved (directive) |
| GAP-2875 | The unit of the expected return, the mapping of the five route words to a closed list and the reason codes are fixed by no source | S5 rwb-asset service owner with the data steward and the P7 rwb-decision owner | Resolved (directive) |
| GAP-2876 | No source publishes the rwb-case case state read or the case-move answer the pricing step consumes | P3 rwb-case owner | Resolved (directive) |
| GAP-2877 | No source publishes the pricing proposal of rwb-agent or the asset and COLLINS fact the price is computed from, and the connection matrix carries no arrow for either | P10 rwb-agent owner, P1 rwb-source-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2878 | R-DIS-17 updates the appraised value, no column of rwb_asset holds it and the appraisal belongs to rwb-valuation | S5 rwb-asset data owner with S1 rwb-valuation owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2879 | The floor percentage and the approval limit of VR-S5-011-1 have no value and no owner row in the sources | P7 rwb-decision rule owner, P4 rwb-access delegated-authority owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2880 | The approval child workflow of the floor is not published, and the sources do not say how the head of NPA role is bound to the approval | P7 rwb-decision owner, P4 rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2881 | The channel and status values of this step, the step schedule by asset class and two legacy screen states have no value or list in the sources | S5 rwb-asset data owner, P7 rwb-decision rule owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2882 | The split plan carries no requirement id for this slice | Program requirements owner | Resolved (directive) |
| GAP-2884 | The asset table is absent from the Ownership Map table list for S5 | Ownership Map owner, S5 rwb-asset data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2885 | The listing record, its publication channels, its price schedule and its pause marker have no legacy Data row, no list value and no owner operation, and the plan carries no requirement id | S5 rwb-asset service owner with the data steward and the business analyst | Resolved (directive) |
| GAP-2886 | The publication to HOME.SCB, the EASY app and the auction portal has no owner contract in the plan, DP-16 is not in the pattern set, and the publish request and answer have no published shape | Integration architect with the P2 rwb-integration service owner and the S5 rwb-asset service owner | Resolved (directive) |
| GAP-2887 | The module FSD and TSD extracts named by the work package are absent from the run extract set, so the module section citations of the fill order are not available | Realignment coordinator with the S5 module business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2888 | No table and no column are named for the occupancy refusal, the eviction status or the eviction record | S5 rwb-asset service owner with the data steward | Resolved (directive) |
| GAP-2889 | No source publishes an operation for the officer action, the stage signal or the case-move answer, and none names how the eviction instruction reaches Legal | P3 rwb-case owner with the S5 rwb-asset owner and the S4 rwb-litigation owner | Resolved (directive) |
| GAP-2890 | The split plan carries no requirement row for the application slice, and the requirement is taken from TSD S5 T8 | Program requirements owner with the business analyst | Resolved (directive) |
| GAP-2891 | The legacy screen list gives SCR-22 four states and names no eviction state, and no source names the state the screen shows | S5 rwb-asset service owner with the screen designer of the gateway-bff composite route | Resolved (directive) |
| GAP-2892 | The contract baseline declares no eviction operation and no named column for the eviction element, because no source gives either | S5 rwb-asset service owner with the solution architect | Resolved (directive) |
| GAP-2893 | The stage signal, the case-move answer and the eviction instruction have no published element names, and no call type is given from rwb-asset to rwb-litigation | Solution architect with the owners of rwb-case and rwb-litigation | Resolved (directive) |
| GAP-2894 | The split plan carries no requirement row for the contract slice | Program requirements owner with the tech lead of rwb-asset | Resolved (directive) |
| GAP-2895 | No published operation name for the rwb-source-data appraisal and asset product or for the rwb-case case-move answer | Solution architect | Resolved (directive) |
| GAP-2896 | listing names no column for the per-round price that R-DIS-38 steps down | Solution architect | Resolved (directive) |
| GAP-2897 | API-S5-004 is claimed by the pricing story and by the price step, and no source splits it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2898 | The split plan carries no requirement id for this slice | Business analyst | Resolved (directive) |
| GAP-2899 | The step evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2900 | The feature describes the vendor choice as distance and capacity while the two rules it names allocate on the scorecard predicted price and not by distance | S5 rwb-asset service owner with the rule owner of the DISPOSAL route set in P7 | Resolved (directive) |
| GAP-2901 | The trigger of the step, the vendor-panel facts and the partner activity have no published operation, no event and no row in the plan dependency lists | S5 rwb-asset service owner with the owners of S9 rwb-partner, P1 rwb-source-data and P3 rwb-case | Resolved (directive) |
| GAP-2902 | The allocation has no column, no list value and no owned row, and the two tables of the service carry no vendor, distance or allocation state | S5 rwb-asset service owner with the data steward of the Asset module | Resolved (directive) |
| GAP-2903 | No requirement of the module covers vendor allocation and the plan carries no requirement id for either slice | S5 rwb-asset service owner with the business analyst of the Asset module | Resolved (directive) |
| GAP-2905 | No source publishes an operation for the allocation step itself and the panel element, its field names and the allocation reference have no published shape | S5 rwb-asset tech lead with the owner of S9 rwb-partner | Resolved (directive) |
| GAP-2906 | No table, column or request element holds the bids of an auction round | Solution architect | Resolved (directive) |
| GAP-2907 | No published operation name for the rwb-case state read, the case-move answer, the rwb-payment payment fact or the rwb-partner vendor score | Solution architect | Resolved (directive) |
| GAP-2908 | Legacy AC2 tests R-DIS-49 while the award and the five-day term belong to FEAT-AST-18, and no source names an owner for R-DIS-49 and R-DIS-50 | Business analyst | Resolved (directive) |
| GAP-2909 | The split plan carries no requirement id for this slice | Business analyst | Resolved (directive) |
| GAP-2910 | The round branch evaluates the DISPOSAL package while DP-04 is outside the pattern set of the slice | Solution architect | Resolved (directive) |
| GAP-2911 | No element holds the award of a round or its cancellation, while the round write answers a sale record with mandatory dates | Solution architect | Resolved (directive) |
| GAP-2914 | The legacy endpoints table names the listings write for the accept while the TSD gives the round write the sale answer | Solution architect | Resolved (directive) |
| GAP-2918 | R-DIS-38 is carried by the ladder story and by the re-list story, and the legacy story repeats the rule | Business analyst | Resolved (directive) |
| GAP-2926 | The five-day term's rules R-DIS-47 to R-DIS-50 sit across this story and RWB-S5-E4024-APP, and no source splits them | Business analyst | Resolved (directive) |
| GAP-2927 | Legacy AC2, AC3 and the FSD A2.18 rule list name R-DIS-11 and R-DIS-37, rules of the work order and the auction round, not the payment term | Business analyst | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S5-E3029-APP | Not specified without item ID | 400 | \| `AssetListing` \| React component \| Shows the listing, its prices, its channel, its status and its schedule on SCR-21 and SCR-23, read only, with the refusal a |
