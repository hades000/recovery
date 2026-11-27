# RWB-SVC-S3 rwb-guarantee (Guarantee) - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 17 |
| Resolved in the stories | 364 |
| Cross-document (pending in another document) | 208 |
| Not applied (value not in the sources) | 18 |
| Open business decisions | 27 |
| Register gaps linked | 53 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S3-E2010-APP | 17 | 15 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E2010 APP Stage 2 data products contracts, plans and treatments v2.md |
| RWB-S3-E4013-APP | 28 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4013 APP Prepare a TCG guarantee claim v2.md |
| RWB-S3-E4013-CON | 18 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4013 CON Prepare a TCG guarantee claim - contract v2.md |
| RWB-S3-E4014-APP | 25 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4014 APP Submit the claim to the TCG portal v2.md |
| RWB-S3-E4014-CON | 11 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4014 CON Submit the claim to the TCG portal - contract v2.md |
| RWB-S3-E4015-APP | 29 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4015 APP Track the claim to payment v2.md |
| RWB-S3-E4015-CON | 16 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4015 CON Track the claim to payment - contract v2.md |
| RWB-S3-E4016-APP | 32 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4016 APP Record the subrogation position v2.md |
| RWB-S3-E4016-CON | 18 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4016 CON Record the subrogation position - contract v2.md |
| RWB-S3-E4017-APP | 25 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4017 APP Notify guarantors and co-borrowers v2.md |
| RWB-S3-E4017-CON | 18 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4017 CON Notify guarantors and co-borrowers - contract v2.md |
| RWB-S3-E4018-APP | 20 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4018 APP Negotiate with a guarantor v2.md |
| RWB-S3-E4018-CON | 16 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4018 CON Negotiate with a guarantor - contract v2.md |
| RWB-S3-E4019-APP | 20 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4019 APP Close the case when a guarantee clears the debt v2.md |
| RWB-S3-E4019-CON | 18 | 7 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4019 CON Close the case when a guarantee clears the debt - contract v2.md |
| RWB-S3-E4020-APP | 36 | 12 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4020 APP File an insurance claim on a collateral event v2.md |
| RWB-S3-E4020-CON | 17 | 8 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4020 CON File an insurance claim on a collateral event - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S3-E4016-APP | R-02247 | CG-ALL-8874 | Script gap | Product owner | The story adds CLAIM_PAID to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4018-APP | R-02255 | CG-ALL-8918 | Script gap | Product owner | The story adds SUBROGATION_POSITION to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4018-APP | R-02256 | CG-ALL-8919 | Script gap | Product owner | The story adds RESIDUAL_TO_ROUTE to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4018-CON | R-02258 | CG-ALL-8930 | Script gap | Product owner | The story adds PATCH to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4018-CON | R-02259 | CG-ALL-8931 | Script gap | Product owner | The story adds SUBROGATION_POSITION to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4019-APP | R-02260 | CG-ALL-8936 | Script gap | Product owner | The story adds RESIDUAL_TO_ROUTE to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4019-APP | R-02261 | CG-ALL-8937 | Script gap | Product owner | The story adds GUARANTEE_CLOSED to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4019-CON | R-02262 | CG-ALL-8945 | Script gap | Product owner | The story adds GUARANTEE_CLOSED to the closed list LOV-CLAIM-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S3-E4013-APP | R-12399 | CG-ALL-8834 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S3-E4014-APP | R-12407 | CG-ALL-8848 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S3-E4015-APP | R-12417 | CG-ALL-8865 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S3-E4016-APP | R-12425 | CG-ALL-8885 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S3-E4018-CON | R-12448 | CG-ALL-8934 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S3-E4020-APP | R-12464 | CG-ALL-8961 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E6021-ITG, RWB-S3-E4013-APP, RWB-S3-E4013-CON, RWB-S7-E6021-APP, RWB-S7-E6021-CON | R-22822 | GAP-1619 | Register gap | Business lead with the center of excellence analyst | A committee decision has no field for the members present or their votes, although the requirement and the screen need both | Agree a member and vote structure for the committee path before Epic 4, either as two child tables of approval or as a versioned structure inside terms, and extend the decision-log entry so the committee's outcome and its members are queryable in the population query. |
| RWB-S3-E4016-APP, RWB-S3-E4016-CON | R-23401 | GAP-2723 | Register gap | P7 rwb-decision owner with the business owner of module S3 | R-GUA-23 and R-GUA-24 carry the same action and differ only in their from-state, and the claim status list is not mapped to the GUARANTEE case states | The rule owner confirms whether the partially paid claim carries the same position, and the data owner publishes the mapping of LOV-CLAIM-STATUS to the GUARANTEE case states; if the partial path is confirmed, one activity serves both rows with no criterion change, and if a mapping is published the record carries it as a coded value. |
| RWB-S3-E4016-APP, RWB-S3-E4016-CON | R-23402 | GAP-2724 | Register gap | S3 rwb-guarantee service owner with the business owner of module S3 and the P8 rwb-payment owner | The TCG share has no published source and the TCG interface INT-29 is recorded as not available | The business owner names the source of the TCG share, either a governed reference row with its version or a TCG interface published by rwb-integration, and the value is read on that source; the element set and the criteria do not change. |
| RWB-S3-E4016-APP, RWB-S3-E4019-APP, RWB-S3-E4019-CON | R-23404 | GAP-2733 | Register gap | Data owner of the Logical Data Model with the business lead of module S3 | The subrogation position the feature must record has no entity, no field and no identifier in the target | Publish the subrogation position as a field group with its own identifiers, or confirm that the closing element of this contract is the position record and that all future recoveries read it there; the sibling story RWB-S3-E4016-APP enters the state |
| RWB-S3-E4018-APP, RWB-S3-E4018-CON | R-23407 | GAP-2728 | Register gap | Business owner of module S3 with the rwb-guarantee tech lead and the solution architect | The approved range, the negotiation outcome vocabulary, the TCG-share column, the rule that authorises an out-of-range outcome and the guarantee payment event have no source in S3, and the state the story moves is the claim's and not the case's | The range bounds, the notice expiry and the outcome list are added to the S3 reference-data register with their version and owner; the outcome list is published as LOV-NEG-OUTCOME; the TCG share is a numeric(18,2) column of guarantee_claim added by this story's Flyway version with its percentage basis recorded; the guarantee payment reaches the stage as a signal the parent forwards until the payment story publishes an event, and the subscription is then added to the event catalogue. |
| RWB-S3-E4020-APP, RWB-S3-E4020-CON | R-23414 | GAP-1724 | Register gap | Product Owner | The insurance claim is Must in the epic BRD but has no program requirement | Trace the insurance claim through BR-025 and REQ-S3-002 (claim status on the case) and raise a program requirement for the collateral event when the program requirement set is next versioned. |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35376 | ASM-2559 | Register assumption |  | The four decision-owner cells of section 7 that named people (DL06, DL09, DL12 and DL20) carry the Template and Rules section R9 placeholder; the owner role is not stated in the source. | Business lead states the four owner roles |
| RWB-ITG-E1007-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E2001-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P4-E1007-APP, RWB-P4-E2003-APP, RWB-P5-E1007-APP, RWB-P6-E1007-APP, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP | R-35377 | ASM-2608 | Register assumption |  | The four owner cells in section 9 that name persons are replaced by the value placeholder, and the role behind each is left to be confirmed. | Programme governance |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-S3-E4016-APP, RWB-S3-E4016-CON | R-38152 | ASM-4521 | Register assumption |  | One activity serves both subrogation rows: R-GUA-23 from CLAIM_PAID and R-GUA-24 from CLAIM_PART_PAID set the same position with the same action and the same to-state, the claim record's status moves to PAID under LOV-CLAIM-STATUS in the same transaction, and the case states CLAIM_PAID, CLAIM_PART_PAID and SUBROGATION_POSITION are reported to the parent CaseWorkflow as the rows of the GUARANTEE state set. | The P7 rwb-decision owner as the owner of the GUARANTEE rule set and the P3 rwb-case owner |
| RWB-S3-E4016-APP, RWB-S3-E4016-CON | R-38153 | ASM-4522 | Register assumption |  | The TCG share, its basis and its effective scope are governed values entered or confirmed on the claim update under right U of Treatment and offer, and no TCG interface is called, because INT-29 is recorded as not available today; the share is never a constant, a percentage or a default of the build. | The business owner of module S3 with the P4 rwb-access owner for the right and the P2 rwb-integration owner for the TCG channel |
| RWB-S3-E4019-APP, RWB-S3-E4019-CON | R-38168 | ASM-4539 | Register assumption |  | The subrogation position of a closed guarantee is carried by the GuaranteeClose element recorded against the claim, with the guaranteed share and the balance after it; the state SUBROGATION_POSITION itself is entered by R-GUA-23 and R-GUA-24 and belongs to the sibling story RWB-S3-E4016-APP. No position entity, no position table and no position column is created by this legacy key until the data owner publishes its identifiers. | Data owner of the Logical Data Model with the business lead of module S3 and the owner of RWB-S3-E4016-APP, before the wave 3 contract tag |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S3-E2010-APP | R-07818 | DOR-RWB-S3-E2010-APP-14 |  | Definition of Ready item 14 Epic design: Fail | Sign-off needs the signed epic design record, which is not in the story text or the supplied sources. No value added; nothing invented. |
| RWB-S3-E2010-APP | R-07819 | DOR-RWB-S3-E2010-APP-16 Size: Fail | header | Definition of Ready item 16 Size: Fail | Size is not in the sources, so the row cannot resolve the item. The squad-sizing statement was removed as not sourced. |
| RWB-S3-E2010-APP | R-07820 | DOR-RWB-S3-E2010-APP-21 | header | Definition of Ready item 21 Contract published: Fail | Header already names RWB-P1-E2010-CON as contract dependency. RWB-S3-E2010-CON cannot be named. Contract publication status is not in the sources. |
| RWB-S3-E2010-APP | R-07821 | DOR-RWB-S3-E2010-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | No rwb-case contract fake name or published fake library version is in the sources. Section 12.8 lists only this story's fakes; no row added. |
| RWB-S3-E2010-APP | R-12391 | CG-ALL-8823 | 7 | Criteria and test data read ACE views directly | AC5 (story line 147) is a Then absence check naming recovery.v_ace_* as forbidden. No Given or test data sets up ACE data, so no rewrite made. QA to confirm false positive. |
| RWB-S3-E2010-APP | R-27006 | CG-ALL-8820 | 14 | MSG-P4-003 text differs from the Error and Message Standard v4 | Standard text fits only out-of-scope. Story MSG-P4-003 also covers feature switch off, so copying it would be wrong. Splitting needs a new message ID, which would be invented. |
| RWB-S3-E4013-APP | R-07827 | DOR-RWB-S3-E4013-APP-23 |  | Definition of Ready item 23 Contract version fixed: Fail | Version v1 may not be written in the change log; no other story location was edited, so the item stays open. |
| RWB-S3-E4014-APP | R-19571 | DOR-RWB-S3-E4014-APP-11 | 12.3; 17 | Definition of Ready item 11 Guardrails: Partial | Field names sit in §12.3 and §17, not supplied. detcheck X10 hits are not stored in the sources read (chunks c02.md, notapplied u01.json). No edit. |
| RWB-S3-E4014-CON | R-19584 | DOR-RWB-S3-E4014-CON-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Section 18 text is not in the supplied story text, so no exact anchor exists. Glob found no story .md under 22 Microservice Realignment. DL10 and ASM IDs not anchored. |
| RWB-S3-E4015-APP | R-19591 | DOR-RWB-S3-E4015-APP-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | The SCR-17 screen-states section is not in this chunk, so no old text can be matched. No edit made. Needs that section in a later chunk. |
| RWB-S3-E4015-APP | R-19592 | DOR-RWB-S3-E4015-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | The personal-data statement section is not in this chunk, so no old text can be matched. No edit made. Needs that section in a later chunk. |
| RWB-S3-E4017-CON | R-19646 | DOR-RWB-S3-E4017-CON-4 | 16 | Definition of Ready item 4 Business rules: Partial | Adding 12 TC rows needs the section 16 table text, which is not in this chunk. Section 8 coverage line already maps BR1 to BR12 to AC1 to AC5. |
| RWB-S3-E4019-CON | R-12455 | CG-ALL-8949 | 12.8 | Criteria and test data read ACE views directly | Criteria still read ACE views; the AC2 line is outside this chunk. Test data fixture is updated to the rwb-source-data contract fake. |
| RWB-S3-E4020-APP | R-19687 | DOR-RWB-S3-E4020-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 (SCR-17 states) is not in the supplied text, so no exact old text to anchor the empty, loading, error and no-access states. Re-run with section 15. |
| RWB-S3-E4020-APP | R-19688 | DOR-RWB-S3-E4020-APP-11 | 11 and 17 | Definition of Ready item 11 Guardrails: Partial | Sections 11 (Data) and 17 (Guardrails) are not in the supplied text, so the personal-data field lines cannot be anchored. Re-run with sections 11 and 17. |
| RWB-S3-E4020-APP | R-32362 | NEWAC-RWB-S3-E4020-APP-AC9 | 7 and 16 | AC9: §5 X8: No rule row, deadline source, claimed-amount source or insurer interface is stated for this claim type (covered by 'Sections 8, 11, 12 and 13' only) | Sections 7 and 16 are not in the supplied text, so AC9 and its TC row cannot be anchored; next AC number unconfirmed (X8 cites AC17). Re-run with sections 7 and 16. |
| RWB-S3-E4020-CON | R-07896 | DOR-RWB-S3-E4020-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the chunk or the project (Grep timed out; Glob for the story file found nothing). Sign-off value cannot be recorded without it. |
| RWB-S3-E4020-CON | R-19701 | DOR-RWB-S3-E4020-CON-20 |  | Definition of Ready item 20 Reference data: Partial | Parameter names and the DP-06/DP-07 reference-data contract are not in the chunk; the Definition of Ready section is not provided. Not specified in the source documents (DOR-RWB-S3-E4020-CON-20). |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (25)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16668 | RWB-S3-E2010-APP | CG-ALL-8821 | 16 | Add rows TC-S3-E2010-APP-01 to TC-S3-E2010-APP-06 to Story test cases, with Given, When and Then copied from the criterion each covers. |
| CDC-16691 | RWB-S3-E4013-APP | CG-ALL-8833 | 16 | Add rows TC-E4-013-01 to -06 with Given, When and Then copied from the criterion each covers; also add rows TC-E4-013-07 to -15. |
| CDC-16703 | RWB-S3-E4013-CON | DOR-RWB-S3-E4013-CON-12 | 12.7, 16 | Boundary test TC-06 added to section 16 |
| CDC-16709 | RWB-S3-E4013-CON | CG-ALL-8838 | 16 | Add rows for TC-S3-E4013-CON-01 to TC-S3-E4013-CON-05 with Given, When and Then copied from the criteria they cover in the next Test Cases version. |
| CDC-16722 | RWB-S3-E4014-APP | CG-ALL-8847 | 16 | Add rows TC-E4-014-01 to TC-E4-014-13 with Given, When and Then copied from AC1 to AC9 in section 7 (next version). |
| CDC-16732 | RWB-S3-E4014-CON | DOR-RWB-S3-E4014-CON-12 | 12.7, 16 | Register TC-S3-E4014-CON-01 to -06 in Test Cases v8. |
| CDC-16737 | RWB-S3-E4014-CON | CG-ALL-8853 | 16 | Add rows TC-S3-E4014-CON-01 to TC-S3-E4014-CON-05 with Given, When and Then copied from AC1 to AC5. |
| CDC-16746 | RWB-S3-E4015-APP | CG-ALL-8864 | 16 | Add rows TC-E4-015-01 to TC-E4-015-06 with Given, When and Then copied from the criterion each covers. |
| CDC-16761 | RWB-S3-E4015-CON | CG-ALL-8871 | 16 | Add rows for TC-E4-015-01 to TC-E4-015-06 and TC-S3-E4015-CON-01 to TC-S3-E4015-CON-04, with Given, When and Then copied from the criteria they cover. |
| CDC-16770 | RWB-S3-E4016-APP | CG-ALL-8884 | 16 | In the next version add rows for TC-E4-016-01 to -06 and TC-S3-E4016-APP-01 and -02, with Given, When and Then copied from the criteria they cover; also TC-S3-E4016-APP-03 and -04 added by this story. |
| CDC-16782 | RWB-S3-E4016-CON | DOR-RWB-S3-E4016-CON-12 | 16 | Add rows for TC-E4-016-01 to TC-E4-016-06, TC-S3-E4016-CON-01 to TC-S3-E4016-CON-03, and the new TC-S3-E4016-CON-04 (boundary of §12.7 tables) |
| CDC-16786 | RWB-S3-E4016-CON | CG-ALL-8894 | 16 | Add rows for TC-E4-016-01 to -06 and TC-S3-E4016-CON-01 to -08, with Given, When and Then copied from the criteria they cover. |
| CDC-16799 | RWB-S3-E4017-APP | CG-ALL-8908 | 16 | Add rows TC-E4-017-01 to TC-E4-017-04 with Given, When and Then copied from the criteria they cover. |
| CDC-16810 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-12 | 12.7, 16 | Register TC-S3-E4017-CON-01 to TC-S3-E4017-CON-06 |
| CDC-16815 | RWB-S3-E4017-CON | CG-ALL-8916 | 16 | Add rows TC-S3-E4017-CON-01 to TC-S3-E4017-CON-05 with Given, When and Then copied from the section 7 criteria they cover |
| CDC-16824 | RWB-S3-E4018-APP | CG-ALL-8926 | 16 | Rows are missing from Test Cases v8 for the six legacy IDs. Section 16 keeps them unchanged; new IDs TC-E4-018-07 to -20 are in section 16. |
| CDC-16831 | RWB-S3-E4018-CON | DOR-RWB-S3-E4018-CON-12 | 16 | Add test case rows TC-S3-E4018-CON-01 to TC-S3-E4018-CON-05 to Test Cases v8. |
| CDC-16834 | RWB-S3-E4018-CON | CG-ALL-8933 | 16 | Add rows for TC-S3-E4018-CON-01 to TC-S3-E4018-CON-05 with Given, When and Then copied from the criterion each covers. |
| CDC-16841 | RWB-S3-E4019-APP | CG-ALL-8942 | 16 | Add rows TC-E4-019-01 to TC-E4-019-06 with Given, When and Then copied from the criteria they cover. |
| CDC-16842 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-12 | 12.7, 16 | Add TC-E4-019-01 to TC-E4-019-06 and new TC-E4-019-07 to TC-E4-019-20 to Test Cases v8; story side adds contract test TC-07 and boundary test TC-08. |
| CDC-16850 | RWB-S3-E4019-CON | DOR-RWB-S3-E4019-CON-12 | 16 | Register TC-S3-E4019-CON-01 to TC-S3-E4019-CON-06 in Test Cases v8. |
| CDC-16853 | RWB-S3-E4019-CON | CG-ALL-8948 | 16 | Add rows TC-S3-E4019-CON-01 to TC-S3-E4019-CON-06 with Given, When and Then copied from AC1 to AC6 of section 7 of RWB-S3-E4019-CON. |
| CDC-16863 | RWB-S3-E4020-APP | CG-ALL-8960 | 16 | Add rows TC-E4-020-01 to TC-E4-020-04 and TC-S3-E4020-APP-01 and -02 to Story test cases, with Given, When and Then copied from their criteria. |
| CDC-16868 | RWB-S3-E4020-CON | DOR-RWB-S3-E4020-CON-12 | 16 | Add rows TC-S3-E4020-CON-01 to TC-S3-E4020-CON-06. |
| CDC-16871 | RWB-S3-E4020-CON | CG-ALL-8966 | 16 | Add rows TC-S3-E4020-CON-01 to TC-S3-E4020-CON-05 to Story test cases in the next version, with Given, When and Then copied from AC1 to AC5 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (19)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16689 | RWB-S3-E4013-APP | CG-ALL-8831 | 12.5 | Add activity assembleChecklist on task queue rwb-guarantee to the Activities sheet, with missing reference non-retryable. |
| CDC-16690 | RWB-S3-E4013-APP | CG-ALL-8832 | 12.5 | Add activity recordPreparation on task queue rwb-guarantee to the Activities sheet. |
| CDC-16720 | RWB-S3-E4014-APP | CG-ALL-8844 | 12.5 | Add the activity readAccountFacts to the Activities sheet with task queue rwb-guarantee and its contract element. |
| CDC-16743 | RWB-S3-E4015-APP | CG-ALL-8860 | 12.5 | Add an Activities row for recordAndApply on rwb-guarantee, or name a catalogued activity in RWB-S3-E4015-APP section 12.5. |
| CDC-16744 | RWB-S3-E4015-APP | CG-ALL-8861 | 12.5 | Add an Activities row for armClaimDeadline on rwb-guarantee, or name a catalogued activity in RWB-S3-E4015-APP section 12.5. |
| CDC-16745 | RWB-S3-E4015-APP | CG-ALL-8862 | 12.5 | Add an Activities row for raiseBreach on rwb-guarantee, or name a catalogued activity in RWB-S3-E4015-APP section 12.5. |
| CDC-16777 | RWB-S3-E4016-CON | DOR-RWB-S3-E4016-CON-8 | 12.5 | Add matchFullPayment, evaluateSubrogationRules and recordAndApply as Activities with task queue rwb-guarantee, or map them to catalogued activities. |
| CDC-16778 | RWB-S3-E4016-CON | CG-ALL-8891 | 12.5 | Add an Activities row for matchFullPayment on task queue rwb-guarantee, with the input and output given in 12.5, or name a catalogued activity. |
| CDC-16779 | RWB-S3-E4016-CON | CG-ALL-8892 | 12.5 | Add an Activities row for evaluateSubrogationRules on task queue rwb-guarantee, with the input and output given in 12.5, or name a catalogued activity. |
| CDC-16780 | RWB-S3-E4016-CON | CG-ALL-8893 | 12.5 | Add an Activities row for recordAndApply on task queue rwb-guarantee, with the input and output given in 12.5, or name a catalogued activity. |
| CDC-16808 | RWB-S3-E4017-CON | CG-ALL-8914 |  | Add activity notifyGuarantor on queue rwb-comms with the GuarantorNotice payload as input, to Activities |
| CDC-16812 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-8 | 8 | Add activity notifyGuarantor, or align the catalog with the workflow kit's Notify activity on queue rwb-comms that AC3 names. |
| CDC-16819 | RWB-S3-E4018-APP | DOR-RWB-S3-E4018-APP-8 | 12.5 | Add activities evaluateNegotiation, applyOutcome and recordAndApply under GuaranteeClaimWorkflow |
| CDC-16840 | RWB-S3-E4019-APP | CG-ALL-8940 | 12.5 | Add an Activities row for closeGuarantee on rwb-guarantee, or name a catalogued activity instead. |
| CDC-16844 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-8 | 4 | Add activity closeGuarantee of GuaranteeClaimWorkflow on queue rwb-guarantee. |
| CDC-16859 | RWB-S3-E4020-APP | CG-ALL-8956 | 12.5 | Add activity readCollateralFacts to the Activities sheet on task queue rwb-guarantee. |
| CDC-16860 | RWB-S3-E4020-APP | CG-ALL-8957 | 12.5 | Add activity evaluateClaimRules to the Activities sheet on task queue rwb-guarantee. |
| CDC-16861 | RWB-S3-E4020-APP | CG-ALL-8958 | 12.5 | Add activity recordAndApply to the Activities sheet on task queue rwb-guarantee. |
| CDC-16862 | RWB-S3-E4020-APP | CG-ALL-8959 | 12.5 | Add activity reportCollateralEvent to the Activities sheet on task queue rwb-guarantee. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16685 | RWB-S3-E4013-APP | CG-ALL-8827 | 3, 11, 12.7, 13 | Add decision_record to LDM v9 Fields, or record the platform library object (DP-03) in its owning document. |
| CDC-16686 | RWB-S3-E4013-APP | CG-ALL-8828 | 4, 9 | Add guarantee_type to LDM v9 Fields, or use the dictionary name in the owning document. |
| CDC-16687 | RWB-S3-E4013-APP | CG-ALL-8829 | 4, 9 | Add scheme_code to LDM v9 Fields, or use the dictionary name in the owning document. |
| CDC-16693 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-7 | 11 | Add or map decision_record, guarantee_type and scheme_code, or record decision_record as the PLT library object of DP-03 outside the LDM. |
| CDC-16723 | RWB-S3-E4014-APP | DOR-RWB-S3-E4014-APP-7 | 11 | Add decision_record as an entity or record it as a PLT library object outside the LDM; confirm DF-ACE field identifiers against v_ace_batch_status; confirm test data reads views as DP-05 requires. |
| CDC-16733 | RWB-S3-E4014-CON | DOR-RWB-S3-E4014-CON-7 | 11 | Add decision_record as an entity or field, or confirm it is the RWB-PLT-E1027-CON library object outside both; the story names it only as that library object. BR Field ID column added to section 11. |
| CDC-16794 | RWB-S3-E4017-APP | CG-ALL-8898 | 1, 4, 8, 9 | Add guarantee_type as a dictionary field, or record the object that holds it (index, library table or flag) in the owning document. |
| CDC-16801 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-7 | 11 | Resolve or rename the names recovery_svc, guarantee_type and decision_record as fields or entities; the legacy AC wording stays verbatim. |
| CDC-16820 | RWB-S3-E4018-APP | CG-ALL-8920 | n/a | Record decision_record as a library object in its owning document, or use the dictionary name |
| CDC-16825 | RWB-S3-E4018-APP | DOR-RWB-S3-E4018-APP-7 | 11 | Add decision_record as the RWB-PLT-E1027-CON library object, or record it as outside LDM v9 and Data Classification v5. P3 wording is fixed in the story under CG-ALL-8927. |
| CDC-16832 | RWB-S3-E4018-CON | DOR-RWB-S3-E4018-CON-7 | 11 | Define decision_record as a field or entity, or confirm the library object name it uses. Story rows now carry BR Field IDs. |
| CDC-16843 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-7 | 11 | Add decision_record as an entity or field; confirm DF-ACE-001 to DF-ACE-042 are fields of the ACE view named in section 11. |
| CDC-16851 | RWB-S3-E4019-CON | DOR-RWB-S3-E4019-CON-7 | 11 | Name decision_record as a field or entity, or confirm it is the DP-03 library object outside both documents. |
| CDC-16857 | RWB-S3-E4020-APP | CG-ALL-8951 | 3, 10 | Add decision_record as a PLT library object in schema rwb_guarantee, or confirm the object in the owning document. Owner role: Data. |

### Epic design record (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16681 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S3 in the epic design record; no signed record exists in the sources. |
| CDC-16700 | RWB-S3-E4013-CON | DOR-RWB-S3-E4013-CON-14 | find it | Record the signed epic design sign-off for RWB-S3-E4013-CON, which is not in this story or the source documents |
| CDC-16713 | RWB-S3-E4014-APP | DOR-RWB-S3-E4014-APP-14 | header | Record the signed sign-off of the epic design so that the story can cite it. |
| CDC-16727 | RWB-S3-E4014-CON | DOR-RWB-S3-E4014-CON-14 |  | Epic design sign-off row added as Not specified in the source documents |
| CDC-16738 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-14 | find it | Record the signed epic design sign-off for RWB-S3-E4015-APP; no signed epic design is recorded in the sources. |
| CDC-16752 | RWB-S3-E4015-CON | DOR-RWB-S3-E4015-CON-14 | find it | Record the signed epic design sign-off for EP04 in the epic design record and confirm it against DOR-RWB-S3-E4015-CON-14 |
| CDC-16764 | RWB-S3-E4016-APP | DOR-RWB-S3-E4016-APP-14 | header | Record the signed epic design sign-off, then the story can cite it. |
| CDC-16788 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-14 | header | Record the signed epic design sign-off. |
| CDC-16806 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-14 |  | Record the signed epic design sign-off for RWB-S3-E4017-CON in the epic design record |
| CDC-16816 | RWB-S3-E4018-APP | DOR-RWB-S3-E4018-APP-14 | n/a | Record the signed epic design sign-off for RWB-SVC-S3 |
| CDC-16828 | RWB-S3-E4018-CON | DOR-RWB-S3-E4018-CON-14 | Header | Record the signed epic design sign-off for EP04 / RWB-SVC-S3 in the epic design record. |
| CDC-16835 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S3 in the epic design record. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16716 | RWB-S3-E4014-APP | GAP-1718 | 12.5 | Add fields for the submission reference, the submission date and the submission channel on guarantee_claim, then confirm with the integration lead before wave 3 system test. |
| CDC-16717 | RWB-S3-E4014-APP | CG-ALL-8841 | 11 | Section 11 now states decision_record is the PLT library object of DP-03, not a service-owned object |
| CDC-16718 | RWB-S3-E4014-APP | CG-ALL-8842 | 11 | Add field rows for v_ace_batch_status (product date of the ACE batch) with their DF-ACE IDs. |
| CDC-16742 | RWB-S3-E4015-APP | CG-ALL-8856 | find it | Record decision_record as the PLT library table created in rwb_guarantee by the library migration, or add it to the dictionary. |
| CDC-16747 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-7 | 11 | Add decision_record as an entity or field of the PLT library, and add it to Data Classification v5. claim_status is not in this chunk; legacy wording fixed in AC1 and AC4. |
| CDC-16756 | RWB-S3-E4015-CON | DOR-RWB-S3-E4015-CON-7 | 11 | Register decision_record as a field or entity, or confirm it is a library object outside LDM v9 and Data Classification v5. |
| CDC-16766 | RWB-S3-E4016-APP | CG-ALL-8875 | 12.7 | Record decision_record as a PLT library object in rwb_guarantee, or name the dictionary field it uses; the story keeps the library object as written. |
| CDC-16771 | RWB-S3-E4016-APP | DOR-RWB-S3-E4016-APP-7 Data: Partial | 11 | decision_record is not an LDM v9 entity; story side kept as a library object. Decision-record wording follows CG-ALL-8886. |
| CDC-16793 | RWB-S3-E4017-APP | CG-ALL-8897 | header (change log, line 6) | Owner role Data: record recovery_svc as an object (index, library table or flag) in the owning document. Dictionary name not changed. |
| CDC-16838 | RWB-S3-E4019-APP | CG-ALL-8938 | 3; 11; 12.7; 13 | Record decision_record under its dictionary name, or record it as the PLT library object of DP-03 in the owning document. |
| CDC-16839 | RWB-S3-E4019-APP | CG-ALL-8939 | 11 | Confirm the LDM v9 field IDs for the product date of v_ace_batch_status and supply them to replace the placeholder in section 11. |
| CDC-16847 | RWB-S3-E4019-CON | CG-ALL-8946 | 11, 12.7 | Record decision_record as the platform library object of DP-03 (same-schema record of RWB-PLT-E1027-CON), or map it to a dictionary field name. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16702 | RWB-S3-E4013-CON | DOR-RWB-S3-E4013-CON-1 | 1 | Add 'service contract owner' as a role code or role name |
| CDC-16731 | RWB-S3-E4014-CON | DOR-RWB-S3-E4014-CON-1 | 1 | Add role 'service contract owner' or confirm the role name used in section 1 against its role list. |
| CDC-16754 | RWB-S3-E4015-CON | DOR-RWB-S3-E4015-CON-1 | 1 | Add 'service contract owner' as a role code or role name |
| CDC-16781 | RWB-S3-E4016-CON | DOR-RWB-S3-E4016-CON-1 | 1 | Add a role code and name for tech lead of rwb-guarantee, or name the existing role code that §1 should use |
| CDC-16809 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-1 | 1 | Add role contract owner of rwb-guarantee, or name the listed role code for it |
| CDC-16830 | RWB-S3-E4018-CON | DOR-RWB-S3-E4018-CON-1 | 1 | Add the role 'contract owner for rwb-guarantee' as a role code or role name. |
| CDC-16848 | RWB-S3-E4019-CON | DOR-RWB-S3-E4019-CON-1 | 1 | Add role name 'contract owner of rwb-guarantee' or the existing role code this story maps to. |
| CDC-16867 | RWB-S3-E4020-CON | DOR-RWB-S3-E4020-CON-1 | 1 | Add a role code or name for 'service contract owner', the role used in section 1. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16666 | RWB-S3-E2010-APP | CG-ALL-8818 | 4, 14 | Add a new message ID for 'A page or a size is out of range' with text '{field} is outside the accepted range {range}.' The story's section 14 then cites that new ID. |
| CDC-16667 | RWB-S3-E2010-APP | CG-ALL-8819 | 4, 14 | Add a new message ID for 'The caller is not signed in' with text 'Sign in to continue.' The story's section 14 then cites that new ID. |
| CDC-16669 | RWB-S3-E2010-APP | DOR-RWB-S3-E2010-APP-9 | 14 | Confirm the meaning of MSG-GEN-003 and MSG-P4-001 and the MSG-P4-003 text; then align the §14 rows to the standard. |
| CDC-16748 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-9 | 14 | Change MSG-P1-001 wording to name the ACE batch: '{product} is from {date}. Today's ACE batch has not arrived.' (per FSD P1 v3 OQ-P1-07). |
| CDC-16749 | RWB-S3-E4015-APP | CG-ALL-8863 | 14 | MSG-P1-001 text left unchanged |
| CDC-16772 | RWB-S3-E4016-APP | DOR-RWB-S3-E4016-APP-9 | 14 | Align MSG-P1-001 text with the standard, or record the standard text as source; story text is that of FSD S3 A2.4.3.1 and is unchanged. |
| CDC-16813 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-9 | 14 | Align the MSG-P1-001 text with the standard, or the standard text is quoted in section 14. The standard text is not in this chunk. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16757 | RWB-S3-E4015-CON | GAP-2714 | 10 | Publish the stage-outcome and service-level breach operation with its shape before the wave 3 tag. |
| CDC-16775 | RWB-S3-E4016-APP | GAP-1721 | 11 | Add S3 rows for the guarantee, guarantor pursuit and subrogation share entity groups named after Arch v5 slide 18; fix the physical tables with the S3 DB story. |
| CDC-16785 | RWB-S3-E4016-CON | GAP-1721 | 12.7 | Add rows for the guarantee, guarantor pursuit and subrogation share entity groups named after Arch v5 slide 18, with the claim fields the sources confirm; physical tables fixed in the S3 DB story. |
| CDC-16803 | RWB-S3-E4017-APP | GAP-1721 | find it | State the guarantee, guarantor pursuit and subrogation groups named after Arch v5 slide 18, give guarantee_claim only the confirmed fields, fix the physical table set, and add the S3 Ownership Map rows. |
| CDC-16814 | RWB-S3-E4017-CON | GAP-1721 | 11 | Add rows for the guarantee, guarantor pursuit and subrogation share entity groups of schema rwb_guarantee, named after Architecture v5 slide 18. |
| CDC-16826 | RWB-S3-E4018-APP | GAP-1721 | 11 | Add the guarantee, guarantor-pursuit and subrogation-position entity groups of schema rwb_guarantee named after Arch v5 slide 18, with owner rows and fields the sources confirm. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16767 | RWB-S3-E4016-APP | CG-ALL-8880 | 12.5 | Add an Activities row for matchFullPayment on task queue rwb-guarantee, or confirm a catalogued activity to use. |
| CDC-16768 | RWB-S3-E4016-APP | CG-ALL-8881 | 12.5 | Add an Activities row for evaluateSubrogationRules on task queue rwb-guarantee, or confirm a catalogued activity to use. |
| CDC-16769 | RWB-S3-E4016-APP | CG-ALL-8882 | 12.5 | Add an Activities row for recordAndApply on task queue rwb-guarantee, or confirm a catalogued activity to use. |
| CDC-16796 | RWB-S3-E4017-APP | CG-ALL-8903 | 12.5 | Add activity resolveAddressees, task queue rwb-guarantee, with input and output as stated in section 12.5. |
| CDC-16797 | RWB-S3-E4017-APP | CG-ALL-8904 | 12.5 | Add activity notifyGuarantor as the Notify template on task queue rwb-comms, as stated in section 12.5. |
| CDC-16798 | RWB-S3-E4017-APP | CG-ALL-8905 | 12.5 | Add activity recordAndApply on task queue rwb-guarantee, as stated in section 12.5. |

### RWB-S3-E4013-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16682 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-21 | header | Set build status to Done (contract published) before this story starts. |
| CDC-16683 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-22 | header | Publish the contract fake library and record its version as published. |
| CDC-16735 | RWB-S3-E4014-CON | GAP-2709 | 11 | Confirm the split by operation of the single guarantee-claim resource or merge the two documents; decide the retention rule of a claim row and whether the checklist becomes Logical Data Model fields. |
| CDC-16802 | RWB-S3-E4017-APP | GAP-2726 | find it | Publish GuarantorNotice with seven properties on the claim update operation, the approved-template accepted and refused answers, the rwb-comms activity input, the notice-period key, the DP-03 record rule, and v1 fakes with a drift test; record unnamed values as the working read of the assumption. |
| CDC-16805 | RWB-S3-E4017-APP | GAP-2725 | 4 | Operation and base of the demand removed from step 6; the story names only the GuarantorNotice payload |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16688 | RWB-S3-E4013-APP | CG-ALL-8830 | 12.4 | Add rwb-guarantee as a consumer of rwb.decision.RulePackageInForce.v1 (EV-30) and grant its ACL. |
| CDC-16719 | RWB-S3-E4014-APP | CG-ALL-8843 | 12.4 | Add rwb-guarantee as a consumer of rwb.decision.RulePackageInForce.v1 (EV-30) and add its ACL. |
| CDC-16856 | RWB-S3-E4020-APP | DOR-RWB-S3-E4020-APP-8 | 12.4; 12.5 | Register rwb-guarantee as a consumer of rwb.decision.RulePackageInForce.v1 on topic rwb.decision.events.v1. |
| CDC-16858 | RWB-S3-E4020-APP | CG-ALL-8953 | 12.4 | Add rwb-guarantee as a consumer of rwb.decision.RulePackageInForce.v1 (EV-30) and grant its ACL. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16721 | RWB-S3-E4014-APP | CG-ALL-8845 | 12.5 | Add activity recordSubmission on task queue rwb-guarantee, with the contract element of section 12.5 (pack and claim row in; GuaranteeClaimUpdate out). |
| CDC-16821 | RWB-S3-E4018-APP | CG-ALL-8923 | 12.5 | Add an Activities row named evaluateNegotiation on task queue rwb-guarantee |
| CDC-16822 | RWB-S3-E4018-APP | CG-ALL-8924 | 12.5 | Add an Activities row named applyOutcome on task queue rwb-guarantee |
| CDC-16823 | RWB-S3-E4018-APP | CG-ALL-8925 | 12.5 | Add an Activities row named recordAndApply on task queue rwb-guarantee |

### RWB-PLT-E1027-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16730 | RWB-S3-E4014-CON | CG-ALL-8852 | 12.7 | Record decision_record as the library object in the owning document, or use the dictionary name in LDM v9 or Data Classification v5. |
| CDC-16753 | RWB-S3-E4015-CON | CG-ALL-8869 | 12.7 | Record decision_record as a library table applied in rwb_guarantee in its owning document |
| CDC-16829 | RWB-S3-E4018-CON | CG-ALL-8932 | 11, 12.7 | Record decision_record as the library object, not an LDM v9 or Data Classification v5 field. |
| CDC-16866 | RWB-S3-E4020-CON | CG-ALL-8965 | 12.7 | Record decision_record as a library object (index, library table or flag) applied in rwb_guarantee; it is not an LDM v9 or Data Classification v5 field. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16773 | RWB-S3-E4016-APP | GAP-2721 | 8 | Publish the posted-payment event with its name, key and elements; the fake then moves to the published contract in a minor version. |
| CDC-16774 | RWB-S3-E4016-APP | GAP-2722 | 8 | Confirm the guarantee events P3, P6 and P9 consume and their names; add them to rwb.guarantee.events.v1 with outbox rows in a later story. |
| CDC-16846 | RWB-S3-E4019-APP | GAP-2735 | 4 | Confirm the SELECT-only grant of recovery.v_ace_account, recovery.v_ace_payment and recovery.v_ace_batch_status to this service's login, or amend slide 8 to allow it. |
| CDC-16852 | RWB-S3-E4019-CON | GAP-2735 | 10 | Record the SELECT-only read of recovery.v_ace_account, recovery.v_ace_payment and recovery.v_ace_batch_status by rwb-guarantee's own ACE login, or a rwb-source-data contract with its dependency. |

### RWB-S3-E4014-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16708 | RWB-S3-E4013-CON | GAP-2726 | find it | Publish GuarantorNotice with its properties, required set and order, approved-template answers, rwb-comms activity input, notice-period key and due-date rule, DP-03 record rule and version 1 on the claim update operation. |
| CDC-16714 | RWB-S3-E4014-APP | DOR-RWB-S3-E4014-APP-21 | header | Move the build status of RWB-S3-E4014-CON from Not started to Done, with the contract published. |
| CDC-16715 | RWB-S3-E4014-APP | DOR-RWB-S3-E4014-APP-22 | header | Publish a contract fake library version and record it as published. |

### RWB-S3-E4015-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16739 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-21 | find it | Set build status to Done (publish the contract) before this story starts. |
| CDC-16740 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-22 | 12.8 | Record the published contract fake library version for the guarantee-claim fake. |
| CDC-16741 | RWB-S3-E4015-APP | DOR-RWB-S3-E4015-APP-8 | 12.5 | State whether PATCH /guarantee-claims/{claimId} takes an Idempotency-Key; add recordAndApply and armClaimDeadline to Temporal Catalog v1. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16758 | RWB-S3-E4015-CON | GAP-2715 | 8 | Add versioned rule and reference rows for the stall horizon, warning window and breach escalation of R-GUA-05 and R-GUA-09. |
| CDC-16763 | RWB-S3-E4015-CON | GAP-1723 | find it | Keep both from-states of each rule pair in the package and count the set as 32 rules until the Center of excellence analyst confirms the split. |
| CDC-16845 | RWB-S3-E4019-APP | GAP-2731 | 4, 7 | Publish the share basis as a governed reference row of the GUARANTEE rule set; allocate a field identifier in the Logical Data Model only if the balance after the share must be auditable as a value. |

### RWB-P1-E2010-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16672 | RWB-S3-E2010-APP | GAP-0509 |  | Add the guarantee claim read and the rwb-case case-existence answer as C dependencies, each with its fake. |
| CDC-16673 | RWB-S3-E2010-APP | GAP-2695 |  | Publish GET /treatments and GET /treatments/active-count on /api/recovery/treatment/v1 (S2 rwb-treatment); remove the case-contract reads; DP04 build calls them with a fake. |

### RWB-P1-E2010-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16675 | RWB-S3-E2010-APP | GAP-0512 | none | Publish DP04 record and guarantee claim read property names from RWB-E2-010 data rows and API Specification v4; required flags and lengths go to baseline review; fake the claim read. |
| CDC-16677 | RWB-S3-E2010-APP | GAP-2738 | 4 | Step 2 maps 400 and a message code the standard does not yet define (CG-ALL-8818); maximum size is not specified in the source documents. |

### OTHER:FSD S3 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16684 | RWB-S3-E4013-APP | GAP-1717 | 11 | Read source fields through the rwb-source-data contract instead of recovery.v_ace_* views; validate freshness via that contract. |
| CDC-16707 | RWB-S3-E4013-CON | GAP-1733 | find it | Write AC-S3-001-01 to AC-S3-008-01 and the exception rows from the named rules and messages, keep the FSD IDs as evidence, and state alternate flows and background events. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16787 | RWB-S3-E4017-APP | CG-ALL-8900 | 12.1 | Publish PATCH /guarantee-claims/{claimId} (the notice form) through the RWB-S3-E4013-CON contract, or remove it from the story. |
| CDC-16791 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-23 | header | Publish a contract version for base /api/recovery/guarantee/v1 so the story can state the version it builds against. |

### RWB-S3-E4017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16789 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-21 | header | Set build status to Done once the contract story is built. |
| CDC-16790 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-22 | header | Publish a contract fake library version and record it. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16807 | RWB-S3-E4017-CON | CG-ALL-8913 |  | Add list LOV-NOTICE-TYPE to Lists, or name the existing Reference Data v5 list for the notice type |
| CDC-16811 | RWB-S3-E4017-CON | DOR-RWB-S3-E4017-CON-20 | 8 | Add LOV-NOTICE-TYPE, the notice type list that BR5 and X7 rely on. |

### RWB-S3-E4018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16817 | RWB-S3-E4018-APP | DOR-RWB-S3-E4018-APP-21 | n/a | Set build status to Done (currently Not started) |
| CDC-16818 | RWB-S3-E4018-APP | DOR-RWB-S3-E4018-APP-22 | n/a | Publish the contract fake library and record its version |

### RWB-S3-E4019-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16836 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-21 | header | Complete the build of RWB-S3-E4019-CON to Done and publish the contract. |
| CDC-16837 | RWB-S3-E4019-APP | DOR-RWB-S3-E4019-APP-22 | 12.8 | Publish a contract fake library version and record its version. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16865 | RWB-S3-E4020-APP | GAP-1726 |  | Add a GET operation on the claim read path the gateway calls; cite it in SCR-17 and case tab stories. The story names no path. |
| CDC-16869 | RWB-S3-E4020-CON | GAP-1726 |  | Add a GET operation for the claim read on the path the gateway will call; cite it from the SCR-17 and case tab stories; mirror it in TSD S3 T-A.1 and the Ownership Map Endpoints sheet |

### OTHER:Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16670 | RWB-S3-E2010-APP | GAP-3176 |  | Confirm no Epic 2 step depends on JOB-01; carry AceIngestCheck (JOB-04) and AceDataReady (EV-26) as the only entry points. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16671 | RWB-S3-E2010-APP | GAP-3194 |  | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop, or attach it to the owning APP story; cite the chosen story on row 121. |

### OTHER:DP04 harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16674 | RWB-S3-E2010-APP | GAP-0392 | none | Record the agreed composite DP04 route and merge order, harness environment, seed pack (40 treatments, 12 plans, 5 claims), evidence format, retention and pass or fail gate at the wave 2 entry check. |

### RWB-S2-E2010-APP; OTHER:parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16676 | RWB-S3-E2010-APP | GAP-2696 | 4 | Treatment operations and active-state parameter row belong to S2 and the parameters contract. Reference-data read path GET /api/recovery/case/v1/reference-data/{tableCode} added to section 4 step 6. |

### OTHER:DP04 release note (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16678 | RWB-S3-E2010-APP | GAP-2739 | none | Record that the rwb-guarantee claim record is wave 3 and the DP04 guarantee part stays empty in wave 2 until the wave 3 claim stories land. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16679 | RWB-S3-E2010-APP | CG-ALL-8822 | 18 | Align REQ-RDF-014 and REQ-RDF-010 test lists with the TC-S3-E2010-APP IDs in section 18 of this story. |

### OTHER:DP04 harness pack; OTHER:wave 2 entry check (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16680 | RWB-S3-E2010-APP | GAP-0513 deployment value, threshold, probe timing or fixture owner | 1 | Fixture owner marked Not specified in the source documents (GAP-0513), to be named at the wave 2 entry check; deployment values stay as named chart value sets |

### OTHER:P3 SCR-17 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16692 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-10 | not in chunk | Define the empty, loading, error and no access states of SCR-17; this story carries no screen state. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16694 | RWB-S3-E4013-APP | DOR-RWB-S3-E4013-APP-8 | 12.1 | Register rwb-guarantee as consumer of rwb.decision.RulePackageInForce.v1; add activities assembleChecklist and recordPreparation to the Temporal Catalog. |

### RWB-S3-E4013-CON; RWB-S3-E4014-CON; OTHER:TSD S3 v2 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16695 | RWB-S3-E4013-APP | GAP-2709 | 12 | Split the guarantee-claim resource by operation between the two contract stories; add a read operation if SCR-17 needs one; decide checklist fields in the LDM; state claim-row retention. |

### API:(service not named); OTHER:TSD S3 v2 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16696 | RWB-S3-E4013-APP | GAP-1726 | 12 | Add the claim read operation to the service contract on the path the gateway will call; the path is not asserted in this document. |

### OTHER:Functional Specification S3 (FSD S3 A2.1.4.1 to A2.8.4.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16697 | RWB-S3-E4013-APP | GAP-1733 | 7 | Replace the placeholder acceptance criteria of A2.1.4.1 to A2.8.4.4 with the criteria written in section 7 of this story, keeping the FSD criterion IDs as evidence. |

### OTHER:Edge and gateway design (gateway-bff) with the platform edge owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16698 | RWB-S3-E4013-APP | GAP-1621 | 15 | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations and which the service owns, and record the four screen contracts there. |

### OTHER:Edge catalogue (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16699 | RWB-S3-E4013-APP | GAP-1730 | 15 | Record SCR-17 as a gateway-bff composite route over the rwb-guarantee claim answer and the rwb-case read, with its owner and route. |

### OTHER:FSD S3; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16701 | RWB-S3-E4013-CON | GAP-1717 | find it | FSD S3 carries rwb-source-data contract field names, not ACE view reads; Arch v5 is the source. Confirm contract fields and freshness response with P1 before wave 3 system test |

### OTHER:Temporal and Drools Design v1 (slide 19); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:P10 cell); 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16704 | RWB-S3-E4013-CON | GAP-1719 |  | Call the agent through the rwb-agent contract as a Temporal activity on rwb-guarantee; take the checklist result if no answer in 60 seconds or the schema check fails; record which assembled the claim. |

### OTHER:FSD S3 A2.1.3.1; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:rwb-document interface; OTHER:rwb-agent binding; OTHER:TSD S3 T4 state map (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16705 | RWB-S3-E4013-CON | GAP-2708 |  | Publish the preparation window, the default-conditions date, the checklist interface, the agent binding, the 17-state map, the event set and the missing-document message. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:TSD S3 T3.2 and T4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16706 | RWB-S3-E4013-CON | GAP-1720 |  | Make the 17-state workflow the state of record and publish a versioned map from the states to the five LOV-CLAIM-STATUS values. |

### OTHER:Edge and gateway design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16710 | RWB-S3-E4013-CON | GAP-1621 | find it | Decide which of SCR-10, SCR-11, SCR-12 and SCR-38 gateway-bff composes from this service's operations and which the service owns, and record the four screen contracts there. |

### OTHER:Platform edge catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16711 | RWB-S3-E4013-CON | GAP-1730 | find it | Record the owner of SCR-17 as a gateway-bff composite route over this resource and the case read, per DP-19. |

### OTHER:Shared message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16712 | RWB-S3-E4013-CON | GAP-1731 | find it | Name the owner of the shared message wording for MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001, and record the Thai and English approval against the shown versions. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:TSD S3 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16724 | RWB-S3-E4014-APP | DOR-RWB-S3-E4014-APP-8 | 4 | Add rwb-guarantee as consumer of rwb.decision.RulePackageInForce.v1; add readAccountFacts and recordSubmission to Temporal Catalog v1; add an idempotency key rule for PATCH or confirm not applicable. |

### OTHER:TSD S3 T-A.1; RWB-S3-E4013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16725 | RWB-S3-E4014-APP | GAP-2709 | 15 | Confirm the split by operation with RWB-S3-E4013-CON; publish or drop the claim read; state the retention rule of guarantee_claim; decide checklist fields in the LDM. |

### OTHER:State map owner (GAP-2711) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16726 | RWB-S3-E4014-APP | GAP-2711 | 4; 11 | Step 7 status-map entry removed; no state map is in the sources |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16728 | RWB-S3-E4014-CON | DOR-RWB-S3-E4014-CON-16 |  | Size row added as Not specified in the source documents |

### RWB-S3-E4014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16729 | RWB-S3-E4014-CON | GAP-1718 | 1 | Record submission reference, submission date and channel on the claim to move it to CLAIM_SUBMITTED; add rwb-integration interface when INT-29 is available; confirm with integration lead before wave 3 system test. |

### OTHER:Scheme reference data (quota and claim deadline per scheme) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16734 | RWB-S3-E4014-CON | GAP-1476 | 11 | Hold the quota and the claim deadline of each scheme as reference data, and show the remaining quota and remaining days on the claim; the officer files manually until INT-29 is available. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; OTHER:INT-29 TCG claim channel (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16736 | RWB-S3-E4014-CON | GAP-2711 | 8 | Name a submission-reference field on guarantee_claim or confirm none; publish the INT-29 interface or keep the recorded officer filing; confirm the claim status map and the timer home. |

### OTHER:split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16750 | RWB-S3-E4015-APP | GAP-2716 | find it | Add dependency rows for the P7 rwb-decision GUARANTEE package and the P3 rwb-case reference data to slice RWB-S3-E4015-APP, or declare both as platform template capabilities. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16751 | RWB-S3-E4015-APP | GAP-2718 | Header | PRD reference row no longer traces to REQ-S3-002 |

### OTHER:P3 screen specification (SCR-17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16755 | RWB-S3-E4015-CON | DOR-RWB-S3-E4015-CON-10 | find it | Add empty, loading, error and no-access states to SCR-17 |

### OTHER:P1 rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16759 | RWB-S3-E4015-CON | GAP-2717 | 10 | Publish the payment-fact read operation and the shape of its answer before the wave 3 tag. |

### OTHER:TSD S3 (T-A.2 and T3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16760 | RWB-S3-E4015-CON | GAP-2719 | 7 | Confirm the element list of both request schemas, the 409 cause, and whether the lost-claim reason and amount take a guarantee_claim column; then republish in a minor version. |

### RWB-S3-E4015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16762 | RWB-S3-E4015-CON | GAP-2716 | find it | Add the P7 guarantee rule package and the P3 reference-data contract as rows at the next plan revision, or declare both as template capabilities. |

### RWB-S3-E4016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16765 | RWB-S3-E4016-APP | DOR-RWB-S3-E4016-APP-21 | header | Set build status to Done with the contract published before this story is ready. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx; OTHER:MSG-P1-001 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16776 | RWB-S3-E4016-APP | CG-ALL-8883 MSG-P1-001 text differs from the Error and Message Standard v4 | 14 | Standard v4 wording is not in the sources, so the section 14 text is marked Not specified (CG-ALL-8883). BR11 in section 8 keeps its FSD wording. |

### OTHER:rwb-guarantee DB story and the data steward's field list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16783 | RWB-S3-E4016-CON | GAP-2720 | 11 | Name the field for the subrogation share, its basis, its effective scope and the guaranteed amount, and add the column in the service's own Flyway sequence; then add the elements to the contract in a minor version |

### OTHER:rwb-payment (P8) posted-payment event contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16784 | RWB-S3-E4016-CON | GAP-2721 | 11 | Publish the posted-payment event with its name, its key and its elements; this baseline then replaces the placeholder and the fake in a minor version |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16792 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-8 | not in chunk | Publish PATCH /guarantee-claims/{claimId} in rwb-guarantee.yaml (CG-ALL-8900). Align task queue rwb-guarantee and namespace rwb-recovery with the catalog. Add resolveAddressees and the GuaranteeClaimWorkflow ID and start rule to Temporal Catalog v1. |

### RWB-PLT-E1027-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16795 | RWB-S3-E4017-APP | CG-ALL-8899 | 3, 7, 8, 11, 12.7, 13 | Record decision_record as a library object in the dictionary, or use the dictionary name the owning document gives. |

### OTHER:Business owner of open decision DL10 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16800 | RWB-S3-E4017-APP | DOR-RWB-S3-E4017-APP-18 Open decisions: Partial | 18 | Open decision DL10 and its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are named in section 18. |

### OTHER:FSD S3 v3 (A2.5.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16804 | RWB-S3-E4017-APP | GAP-1722 | find it | Write the notice rules from R-GUA-06 and R-GUA-28 to R-GUA-32 with the recipient set, the template, the period from proof of delivery, the answer to the route decision, and a field catalog. |

### OTHER:TSD S3 v2 (T-A.1; OTHER:T-A.2) and the rwb-guarantee contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16827 | RWB-S3-E4018-APP | GAP-2730 | 11 | Invented element name and type removed; name, type and unit stay Not specified |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S3 DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16833 | RWB-S3-E4018-CON | GAP-1721 | 11 | Add S3 rows for the guarantee, guarantor pursuit and subrogation position groups; fix the physical table set in the S3 DB story. |

### OTHER:platform edge story (SCR-17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16849 | RWB-S3-E4019-CON | DOR-RWB-S3-E4019-CON-10 | 1 | Add empty, loading, error and no access states for SCR-17. |

### RWB-S3-E4020-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16854 | RWB-S3-E4020-APP | DOR-RWB-S3-E4020-APP-14 | Header | Record the signed epic design sign-off for RWB-S3-E4020-APP. The story row stays Not specified until then. |

### RWB-S3-E4020-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16855 | RWB-S3-E4020-APP | DOR-RWB-S3-E4020-APP-21 | header | Set the build status of RWB-S3-E4020-CON to Done; it is currently Not started. |

### OTHER:FSD S3 v3 and TSD S3 v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16864 | RWB-S3-E4020-APP | GAP-1720 | 8 | Map the five LOV-CLAIM-STATUS values to the 17 workflow states of Routing Logic v4 R-GUA-01 to R-GUA-32 as versioned reference data. |

### OTHER:Functional Specification Document S3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16870 | RWB-S3-E4020-CON | GAP-1733 |  | Replace AC-S3-001-01 to AC-S3-008-01 and the AC-EXC-S3-00x rows with criteria stating a scenario, value or outcome from the named rules and messages; add alternate flows and system events |

### OTHER:edge catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16872 | RWB-S3-E4020-CON | GAP-1730 | 15 | Record the owner of SCR-17 and its gateway-bff composite route over this contract and the case contract. Story text already states the route and the service split. |

### OTHER:shared message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16873 | RWB-S3-E4020-CON | GAP-1731 | find it | Name the owner of the shared wording for MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001, and the role approving the Thai and English versions. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0066 | Wave conflict S3 / EP02 | Tech lead | Resolved (directive) |
| GAP-0392 | DP04 integration harness: composite record route, environment, seed pack, evidence format and gate not specified | Integration lead | Resolved (directive) |
| GAP-0509 | The guarantee claim read of rwb-guarantee and the case-existence answer are not in the Work Package's contract list | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0510 | The workflow and activity names of the stage 2 build are a target design choice | Solution architect | Resolved (directive) |
| GAP-0511 | The expected-by time of DP04 is assumed from the decision log and stated by no source | Data steward | Resolved (directive) |
| GAP-0512 | The field-level DP04 record schema and the shape of the guarantee claim read are not specified | Tech lead | Resolved (directive) |
| GAP-0513 | No deployment value, threshold, probe timing or fixture owner exists for the stage 2 build | DevOps lead | Resolved (directive) |
| GAP-1476 | The TCG quota and the claim deadline for each scheme are not specified | Guarantee officer | Resolved (directive) |
| GAP-1621 | Four screens are attributed to P7 while the edge ruling composes every screen in gateway-bff | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1716 | The treatment record exists twice: as this service's live record and as P1's dated copy | Data architect | Resolved (directive) |
| GAP-1717 | FSD S3 reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1718 | The claim submission has no interface: INT-29 is not available today and the S3 row has no call to an outside system | Solution architect with the integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1719 | The claim is assembled by an agent that has no call path from this service | Solution architect with the P10 owner | Resolved (directive) |
| GAP-1720 | The claim status list has five values while the claim workflow has seventeen states, and no mapping is given | Business analyst, S3 with the P7 owner | Resolved (directive) |
| GAP-1721 | The guarantee, the guarantor pursuit and the subrogation position have no owned record | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1722 | The guarantor notice feature names no notice rule and no field set | Business analyst, S3 with the P6 owner | Resolved (directive) |
| GAP-1723 | Two rule pairs repeat and one submission rule appears under claim tracking | Center of excellence analyst | Resolved (directive) |
| GAP-1726 | The claim read has no operation, although the architecture gives the service a GET | Solution architect | Resolved (directive) |
| GAP-1728 | The TCG quota and the claim deadline for each scheme are not set | Guarantee officer | Resolved (directive) |
| GAP-1730 | No source fixes the screen ownership or the gateway route of SCR-17 | Solution architect | Resolved (directive) |
| GAP-1731 | Four messages are shown without an owner for their wording | Business analyst, S3 | Resolved (directive) |
| GAP-1732 | The guarantee claim route has two numbers in the sources | Business analyst, S3 with the P7 owner | Resolved (directive) |
| GAP-1733 | Every acceptance criterion of the FSD is a placeholder | Business analyst, S3 | Resolved (directive) |
| GAP-2695 | The owner of the treatment changed-window and active-count reads conflicts between the DP04 story and the service ownership | Solution architect | Resolved (directive) |
| GAP-2696 | The two operation shapes, the active-state rule and the reference-data read path are fixed by no source document | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2708 | The preparation of a TCG guarantee claim on the target: no window value, no home for the default-conditions date, no checklist interface, no agent binding, no state map, no service event and no message for a missing scheme document | Solution architect with the rwb-guarantee service owner, the P7 rule owner and the P5 document owner | Resolved (directive) |
| GAP-2709 | The guarantee-claim resource contract: two contract stories on one resource, no read operation in the inventory, no checklist or document element and no retention rule | Solution architect with the rwb-guarantee contract owner and the platform API owner | Resolved (directive) |
| GAP-2711 | The submission of a guarantee claim on the target: no reference field, no channel interface, no state map, no timer home and no service event | Tech lead of rwb-guarantee | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2712 | The guarantee-claim resource contract: nothing to publish for the submission reference, for the TCG channel or for the text of the 409, and no retention rule for a claim row | Tech lead of rwb-guarantee | Resolved (directive) |
| GAP-2714 | No source publishes the operation that carries a stage outcome and a service level breach from rwb-guarantee to rwb-case | P3 rwb-case owner with the S3 rwb-guarantee owner | Resolved (directive) |
| GAP-2715 | The stall horizon, the warning window and the breach escalation behind 'raises the service level breach' have no value in any source | S3 rwb-guarantee owner with the P3 rwb-case owner and the business rule owner | Resolved (directive) |
| GAP-2716 | The GUARANTEE rule package and the two claim lists are consumed with no dependency row in this slice | P7 rwb-decision owner with the P3 rwb-case owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2717 | No source publishes the payment-fact read of rwb-source-data that replaces the legacy v_ace_payment read | P1 rwb-source-data owner | Resolved (directive) |
| GAP-2718 | No REQ-S3 identifier is given for this legacy key by any source | Requirements owner with the S3 rwb-guarantee owner | Resolved (directive) |
| GAP-2719 | The source names the three claim entities and the eight columns, and states no element list, no 409 cause and no field for the lost-claim reason and amount | S3 rwb-guarantee owner with the S3 data owner | Resolved (directive) |
| GAP-2720 | No field, column or element exists for the subrogation position or for the guaranteed amount that R-GUA-22 compares the payment with | S3 rwb-guarantee service owner with the data steward and the P7 rwb-decision owner | Resolved (directive) |
| GAP-2721 | The posted payment reaches this service only on an rwb-payment event, and the legacy v_ace_payment read is closed to it | P8 rwb-payment owner with the P1 rwb-source-data owner and the S3 service owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2722 | The service publishes no event, while the connection matrix shows three peers subscribing to it, and no peer event name is published | P9 rwb-reporting owner, P3 rwb-case owner and P6 rwb-comms owner with the S3 service owner | Resolved (directive) |
| GAP-2725 | The dispatch of the demand, the addressee set, the approved template and the notice period are not specified for rwb-guarantee | Solution architect with the rwb-guarantee tech lead and the rwb-comms owner | Resolved (directive) |
| GAP-2726 | The notice payload, its required set, the approved-template answer, the delivery contract and the notice due date have no published shape | Solution architect with the rwb-guarantee tech lead and the rwb-comms owner | Resolved (directive) |
| GAP-2729 | The story master, the functional specification and the technical specification disagree on who owns the state, on its vocabulary and on whom the outcome is recorded against | Solution architect with the rwb-case and rwb-guarantee tech leads and the screen owners | Resolved (directive) |
| GAP-2730 | The contract surface has no read operation, no negotiation element, no element name for the share and no entry format for the messages | Solution architect, S3, with the rwb-guarantee tech lead, the gateway-bff owner and the API owner | Resolved (directive) |
| GAP-2731 | The guaranteed share and the balance after it have no field, no field identifier and no governed row, so the element of a closed guarantee has no published basis | Data owner of the Logical Data Model with the business analyst of module S3 and the owner of the rwb-decision rule registry | Resolved (directive) |
| GAP-2732 | The rules close the guarantee and close the case, while LOV-CLAIM-STATUS has no closed value and the case closure is outside the service | Solution architect of S3 with the owner of P3 rwb-case and the business analyst of module S3 | Resolved (directive) |
| GAP-2734 | The trigger of the close step is unnamed: the FSD offers a batch, an event or a timer, and no source says which reaches this feature | Solution architect of S3 with the owner of P8 rwb-payment and the owner of P3 rwb-case | Resolved (directive) |
| GAP-2735 | Architecture v5 gives the recovery.v_ace_* views to rwb-source-data alone, while these stories read three of them through the service's own login under DP-05 | Solution architect with ACE and its DBA and the owner of P1 rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2736 | The collateral-insurance claim on the target: no rule row, no deadline or claimed-amount source, no insurer interface, no re-appraisal edge and no state map | Tech lead of rwb-guarantee | Resolved (directive) |
| GAP-2737 | The collateral-event branch of the guarantee-claim resource contract: no field identifier for the collateral or appraisal element, no deadline or amount basis and no text for the 409 | Tech lead of rwb-guarantee | Resolved (directive) |
| GAP-2738 | No source publishes a claim-side changed-window read for the DP04 build: the operation, its path, its page parameters, its maximum size, its error mapping and a count read all have no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2739 | The owner and the timing of the dated DP04 copy of a guarantee claim conflict: the legacy story writes dp_guarantee_claim itself and puts the claim interface in Epic 4, the target gives the copy to rwb-source-data in wave 2 and the claim record to rwb-guarantee in wave 3 | Solution architect | Resolved (directive) |
| GAP-2740 | No source says which side resolves a claim whose case does not exist, or whether the claim read answers such a claim at all | Data steward | Resolved (directive) |
| GAP-3176 | JOB-01 is retired, yet three Epic 2 stories are keyed on it | Integration lead with the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S3-E4020-APP | skipped AC ID | 126 | missing: AC9 |
| RWB-S3-E4020-APP | duplicate TC ID | 475 | TC-S3-E4020-APP-03 |
