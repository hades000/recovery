# RWB-SVC-S9 rwb-partner (Partner) - review pack, part 2 of 3 (RWB-S9-E6033-CON to RWB-S9-E7016-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 17 |
| Resolved in the stories | 343 |
| Cross-document (pending in another document) | 251 |
| Not applied (value not in the sources) | 20 |
| Open business decisions | 17 |
| Register gaps linked | 37 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S9-E6033-CON | 17 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6033 CON Receive a partner result into the case - contract v2.md |
| RWB-S9-E6034-APP | 31 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6034 APP Place a charged-off account with an agency v2.md |
| RWB-S9-E6034-CON | 16 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6034 CON Place a charged-off account with an agency - contract v2.md |
| RWB-S9-E6035-APP | 26 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6035 APP Match a recovery and calculate the agency fee v2.md |
| RWB-S9-E6035-CON | 15 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E6035 CON Match a recovery and calculate the agency fee - contract v2.md |
| RWB-S9-E7011-APP | 21 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7011 APP Score partners monthly v2.md |
| RWB-S9-E7011-CON | 15 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7011 CON Score partners monthly - contract v2.md |
| RWB-S9-E7012-APP | 18 | 18 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7012 APP Approve partner fees v2.md |
| RWB-S9-E7012-CON | 14 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7012 CON Approve partner fees - contract v2.md |
| RWB-S9-E7013-APP | 25 | 21 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7013 APP Hold a partner review v2.md |
| RWB-S9-E7013-CON | 19 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7013 CON Hold a partner review - contract v2.md |
| RWB-S9-E7014-APP | 28 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7014 APP Issue a notice on a missed target v2.md |
| RWB-S9-E7014-CON | 10 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7014 CON Issue a notice on a missed target - contract v2.md |
| RWB-S9-E7015-APP | 28 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7015 APP End a partner contract and recall the work v2.md |
| RWB-S9-E7015-CON | 16 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7015 CON End a partner contract and recall the work - contract v2.md |
| RWB-S9-E7016-APP | 27 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7016 APP Check partner conduct v2.md |
| RWB-S9-E7016-CON | 17 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S9 rwb-partner (Partner)/RWB S9 E7016 CON Check partner conduct - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S9-E6035-APP | R-03211 | CG-ALL-11914 | Script gap | Product owner | The story adds PLACED_WITH_AGENCY to the closed list LOV-INSTR-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S9-E6035-APP | R-03212 | CG-ALL-11915 | Script gap | Product owner | The story adds PAYMENT_MATCHED to the closed list LOV-INSTR-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S9-E6035-CON | R-03222 | CG-ALL-11936 | Script gap | Product owner | The story adds PAYMENT_MATCHED to the closed list LOV-INSTR-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S9-E6034-APP | R-13561 | CG-ALL-11897 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E6035-APP | R-13568 | CG-ALL-11931 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E7012-APP | R-13590 | CG-ALL-11992 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S9-E7014-APP | R-13608 | CG-ALL-12054 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E7014-ITG, RWB-S9-E7014-APP, RWB-S9-E7014-CON | R-22892 | GAP-3127 | Register gap | Business lead; solution architect; rwb-comms owner; rwb-case reference-data owner; rwb-decision rule owner | RWB-S9-E7014-APP: no source owns the partner notice in S9, publishes a notice, target or cure-period property, or gives the notice a message; no partner route set exists, and no requirement row traces to FEAT-PRM-11 | Read the contractual notice as a rwb-comms element requested on its contract with a fake, keep the panel change on partner.panel_status at ON_NOTICE, submit the act on API-S9-002 with the Idempotency-Key, write the local decision record before any change with the rule ID and the version where they exist and the placeholder where they do not, hold the target, the cure period, the two exits from ON_NOTICE, the refusal message, the direction of EV-21 and the requirement row as open items with placeholder text. |
| RWB-ITG-E7014-ITG, RWB-S9-E7014-APP, RWB-S9-E7014-CON | R-22893 | GAP-3128 | Register gap | Solution architect; rwb-partner tech lead; business lead; rwb-comms owner; rwb-case reference-data owner; rwb-decision rule owner | RWB-S9-E7014-CON: the contract has no notice, target or cure-period property or operation, partner_user has no field list, no partner route set exists, the plan's C row is empty while two consumed rows are declared and DP-06 and DP-07 are absent, EV-21 has two directions, and no requirement row traces to FEAT-PRM-11 | Publish the three operation baselines of /api/recovery/partner/v1 with the Partner and PartnerInstruction elements and the four lists, declare the notice of rwb-comms and the reference data of rwb-case as two consumed rows with fakes and placeholders, declare no notice, target or cure-period property and no partner_user property, declare EV-20 published and EV-21 consumed with the conflict recorded, declare no Schedule and no job, and hold the requirement row and the refusal message open. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23241 | GAP-3117 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S9-E6034-APP: the legacy story names two read endpoints and no operation that places the account, partner_instruction carries no rule-version or decision column, S9 owns no route set so the placement rule is only expressible as the D9 rows R-WO-29 to R-WO-32, the legacy permission table gives the Partner portal right R while the issue needs C and the FSD also-uses role has no matrix row, both screens are list states with no placement form, the plan C row is empty while the case and the rule package are consumed, DP-04 and DP-09 are absent, the EV-20 consumer set and payload are not published, and no requirement row traces to FEAT-PRM-06 | Keep the plan H, C, I and X rows as they stand; issue the placement through API-S9-002 and never through a new path; record the rule version and the picked agency on the local decision record and add no column to partner_instruction; read the placement rows from rwb-decision as data and record the absent DP-04 rows; read the case on the rwb-case contract and record the absent C rows; authorise the issue on the Partner portal right C the matrix gives and record the legacy right R and the missing also-uses row as conflicts; serve the placement from the list state of SCR-35 through the composite route and carry the form as a placeholder; publish EV-20 with IDs only and record the absent DP-09 row; let the trace rest on the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-S9-E6033-CON, RWB-S9-E7018-APP, RWB-S9-E7018-CON | R-23655 | GAP-3136 | Register gap | Solution architect; rwb-partner tech lead; business lead; rwb-document owner; rwb-source-data owner; rwb-decision rule owner; rwb-access role owner | RWB-S9-E7018-CON: the contract has no field-work, evidence, result-vocabulary, media-type or document-reference source, partner_user publishes no role list, the plan's C row is empty while three consumed rows are declared, DP-05, DP-09 and DP-18 are absent, the element overlaps the baseline of RWB-S9-E6033-CON, EV-21 has two directions, the field app has no interface ID, and TSD S9 T8 maps REQ-S9-009 to another feature | Add one FieldWorkResult element inside the published baseline of RWB-S9-E6033-CON, declare the visit, the evidence and the rule as three consumed rows with fakes and placeholders, declare no evidence column, no visit table, no result enumeration and no partner role enumeration, declare EV-21 with one direction and the conflict recorded, declare no new operation, Schedule or job, and hold the media types, the result vocabulary, the field-app interface, the 409 text and the requirement row open. |
| RWB-S9-E6034-APP, RWB-S9-E6034-CON | R-23657 | GAP-3118 | Register gap | Solution architect; business lead; data steward | RWB-S9-E6034-CON: no source publishes the property list of InstructionRequest, of the Partner and PartnerInstruction answers or of the paged instruction answer, no message ID is published per error condition, partner_user has no field catalog, the two consumed operation names have no baseline, the plan C row is empty while the baseline declares two consumed rows, and no requirement row traces to FEAT-PRM-06 | Publish the baseline with the placeholders, bind every error condition to one message of section 14, declare the three operations of the key on the one base and name the other three as their stories, declare partner_user without properties, declare the case and rule rows as consumed and faked, record the decision-record and EV-20 elements, and trace to the legacy key and the feature row until the E6 BRD and the PRD publish a requirement |
| RWB-S9-E6035-APP, RWB-S9-E6035-CON | R-23658 | GAP-3119 | Register gap | Business lead; reference-data owner in rwb-case; solution architect; owner of rwb-payment | RWB-S9-E6035-APP: the contracted fee schedule has no table, column, rate, tier, basis or rounding in any source, the legacy data table carries no payment or recovery entity, the plan's C row is empty while four rows are consumed, DP-04, DP-06, DP-07, DP-10 and DP-16 are absent from the pattern set, TSD S9 T8 maps every requirement row away from FEAT-PRM-07, the two service events carry no fee, and no message is published for a payment that matches no placement or a date with no schedule row | Confirm the contracted fee schedule as versioned reference data of rwb-case with its columns, rate basis, tiers, rounding and effective dates before wave 4 starts; confirm the operation and the fact shape of the posted payment of rwb-payment and add the C rows for the four consumed contracts; add the pattern rows DP-04, DP-06, DP-07, DP-10 and DP-16 or record their absence; decide whether the fee is announced on an event of the service; publish the messages for a payment that matches no placement and for a date with no schedule row; and add the requirement row that traces to FEAT-PRM-07 at the next version of TSD S9 T8 and in the E6 BRD and the S9 PRD. |
| RWB-S9-E6035-APP, RWB-S9-E6035-CON | R-23659 | GAP-3120 | Register gap | Business lead; solution architect; tech lead of rwb-partner; owners of rwb-payment, rwb-case and rwb-decision | RWB-S9-E6035-CON: the Partner and PartnerInstruction elements carry no fee property and no source publishes their names, formats or value sets, no source publishes the contracted fee schedule, the four consumed operation names have no published baseline, no requirement row traces to FEAT-PRM-07, and the plan's C row is empty while the baseline declares four consumed rows | Publish the three fee properties of the instruction answer with their names, formats and value sets as an additive change of major version 1; publish the contracted fee schedule as a documented reference-data contract of rwb-case with its columns, rate basis, tiers, rounding and effective dates; publish the operation names of the four consumed rows; add the C rows for the four contracts and the pattern rows DP-04, DP-06, DP-07, DP-10 and DP-16 or record their absence; pair EV-20 and EV-21 with their names in the event catalogue; and add the requirement row that traces to FEAT-PRM-07 at the next version of TSD S9 T8 and in the E6 BRD and the S9 PRD. |
| RWB-S9-E7014-APP, RWB-S9-E7016-APP | R-29238 | GAP-1853 | Register gap | Compliance and PDPA officer | No retention class is stated for partner, partner_instruction or partner_user | Carry the Workbench record class and leave the period open until DL26 answers, as every other service does. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S9-E6035-APP | R-09067 | DOR-RWB-S9-E6035-APP-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-S9-E6035-CON in project sources (Grep, per earlier notes). Placeholder already in Contract dependencies row. Not invented. |
| RWB-S9-E6035-APP | R-27963 | CG-ALL-11932 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The four lines (AC1, AC2, TC-E6-035-04) sit in sections 7 and 16, outside the supplied story text. Section 12.5 has no such wording. Exact old text unavailable. |
| RWB-S9-E6035-CON | R-03230 | CG-ALL-11944 Workflow task queue/namespace | 12.5 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | Lines 41 and 162 still state namespace rwb-recovery; the story must be made consistent before this is resolved. |
| RWB-S9-E6035-CON | R-09072 | DOR-RWB-S9-E6035-CON-17 Dependencies: Fail | header | Definition of Ready item 17 Dependencies: Fail | Section 13 still names RWB-P7-E1073-CON (see R-03229), so the item is not resolved. |
| RWB-S9-E7011-APP | R-09076 | DOR-RWB-S9-E7011-APP-14 | not in chunk | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources. Hub v18 DT05 only says sign-offs run in parallel. Sign-off must come from the record, so it cannot be confirmed here. |
| RWB-S9-E7011-APP | R-33285 | NEWAC-RWB-S9-E7011-APP-AC5 | 7; 16 | AC5: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Proposed rule-level test still needs a ruling. AC5 stub is a placeholder; no test row added in section 16. |
| RWB-S9-E7012-APP | R-03237 | CG-ALL-11981 |  | rwb-partner.yaml holds status as a closed enum while the story reads LOV-INSTR-STATUS as data | Ruled closed list (Reference Data v5 Lists), so the rwb-partner.yaml enum stays. The LOV-INSTR-STATUS data sentence is not in this chunk; no story edit. |
| RWB-S9-E7012-APP | R-03238 | CG-ALL-11982 |  | rwb-partner.yaml holds instructionType as a closed enum while the story reads LOV-INSTRUCTION as data | Ruled closed list (Reference Data v5 Lists), so the rwb-partner.yaml enum stays. The LOV-INSTRUCTION data sentence is not in this chunk; no story edit. |
| RWB-S9-E7012-APP | R-03239 | CG-ALL-11983 |  | rwb-partner.yaml holds panelStatus as a closed enum while the story reads LOV-PANEL as data | Ruled closed list (Reference Data v5 Lists), so the rwb-partner.yaml enum stays. The LOV-PANEL data sentence is not in this chunk; no story edit. |
| RWB-S9-E7012-APP | R-03240 | CG-ALL-11984 |  | rwb-partner.yaml holds partnerType as a closed enum while the story reads LOV-PARTNER-TYPE as data | Ruled closed list (Reference Data v5 Lists), so the rwb-partner.yaml enum stays. The LOV-PARTNER-TYPE data sentence is not in this chunk; no story edit. |
| RWB-S9-E7012-APP | R-27981 | CG-ALL-11993 | 12.5 | Criteria and tests keep legacy job and decision-log wording | Section 12.5 has no 'decision log', 'job record' or JOB-nn wording. The AC2 and AC5 lines are in section 7, not in this chunk. No edit. |
| RWB-S9-E7012-APP | R-33293 | NEWAC-RWB-S9-E7012-APP-AC7 | 7 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 content is not specified in the source documents (NEWAC-RWB-S9-E7012-APP-AC7); the rule-coverage content needs sourcing. |
| RWB-S9-E7012-CON | R-09092 | DOR-RWB-S9-E7012-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists in the chunk or the sources. A sign-off or record ID would be invented, so no edit was made. The record is needed to resolve this. |
| RWB-S9-E7014-APP | R-21534 | DOR-RWB-S9-E7014-APP-10 | 9-10 | Definition of Ready item 10 Screens and states: Partial | Sections 9-10 text is not in the chunk, so no exact old text to anchor an edit. Source SCR-34/35 lists only Loading and list states; empty, error and no-access are not in the sources. |
| RWB-S9-E7014-APP | R-21535 | DOR-RWB-S9-E7014-APP-11 | 17 | Definition of Ready item 11 Guardrails: Partial | Section 17 Guardrails text is not in the chunk, so no exact old text to anchor an edit. Applied v2 story line 372 states no personal data; the fix needs the chunk's section 17 text. |
| RWB-S9-E7014-CON | R-03272 | CG-ALL-12064 | 12.5 | Workflow InstructionWorkflow task queue rwb-partner` in namespace `rwb-recovery differs from the catalog | Only the table row at line 306 was corrected. Lines 52 and 171 still name namespace rwb-recovery, so the item is not resolved in the story. |
| RWB-S9-E7015-CON | R-09125 | DOR-RWB-S9-E7015-CON-8 | 12.5 | Definition of Ready item 8 Contract: Fail | Covers the P1 rows of items CG-ALL-12087 to 12090 (yaml, task queue, branch, ID form). The other five detcheck rows are outside this chunk and remain open. |
| RWB-S9-E7016-APP | R-09126 | DOR-RWB-S9-E7016-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design in the supplied story text or prior source search. Sign-off is not specified in the source documents (DOR-RWB-S9-E7016-APP-14). |
| RWB-S9-E7016-APP | R-09127 | DOR-RWB-S9-E7016-APP-16 |  | Definition of Ready item 16 Size: Fail | No size in the story or sources; the squad sizes at refinement. Size is not specified in the source documents (DOR-RWB-S9-E7016-APP-16). |
| RWB-S9-E7016-APP | R-09129 | DOR-RWB-S9-E7016-APP-22 |  | Definition of Ready item 22 Fake published: Fail | No contract fake library version recorded as published in the story or sources. None specified in the source documents (DOR-RWB-S9-E7016-APP-22). |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml (35)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20057 | RWB-S9-E6033-CON | CG-ALL-11874 | 12.1 | Publish POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results (API-S9-005) in rwb-partner.yaml. |
| CDC-20058 | RWB-S9-E6033-CON | CG-ALL-11875 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions (API-S9-003) in rwb-partner.yaml. |
| CDC-20060 | RWB-S9-E6033-CON | DOR-RWB-S9-E6033-CON-8 | 12.5 | Publish paths for API-S9-005 and API-S9-003; the story now records the Workflow ID form and start rule as not specified. |
| CDC-20069 | RWB-S9-E6034-APP | CG-ALL-11885 | 12.1 | Publish POST /cases/{caseId}/instructions (API-S9-002) under base /api/recovery/partner/v1 through RWB-S9-E6034-CON. |
| CDC-20070 | RWB-S9-E6034-APP | CG-ALL-11886 | 12.1 | Publish GET /partners (API-S9-001) under base /api/recovery/partner/v1 through RWB-S9-E6034-CON. |
| CDC-20071 | RWB-S9-E6034-APP | CG-ALL-11887 | 12.1 | Publish GET /partner/instructions (API-S9-003) under base /api/recovery/partner/v1 through RWB-S9-E6034-CON. |
| CDC-20077 | RWB-S9-E6034-APP | DOR-RWB-S9-E6034-APP-8 | header | Add POST /cases/{caseId}/instructions, GET /partners, GET /partner/instructions, base /api/recovery/case/v1 and the 6 further paths named in detcheck. |
| CDC-20085 | RWB-S9-E6034-CON | CG-ALL-11902 | 12.1 | Declare POST /cases/{caseId}/instructions (API-S9-002) under base /api/recovery/partner/v1 as section 12.1 states. |
| CDC-20086 | RWB-S9-E6034-CON | CG-ALL-11903 | 12.1 | Declare GET /partners (API-S9-001) under base /api/recovery/partner/v1 as section 12.1 states. |
| CDC-20087 | RWB-S9-E6034-CON | CG-ALL-11904 | 12.1 | Declare GET /partner/instructions (API-S9-003) under base /api/recovery/partner/v1 as section 12.1 states. |
| CDC-20090 | RWB-S9-E6034-CON | DOR-RWB-S9-E6034-CON-8 | header | Add paths POST /cases/{caseId}/instructions (API-S9-002), GET /partners (API-S9-001), GET /partner/instructions (API-S9-003); add base /api/recovery/case/v1 to its owning yaml. |
| CDC-20097 | RWB-S9-E6035-APP | CG-ALL-11917 | 12.1 | Publish GET /partner/instructions (API-S9-003) under base /api/recovery/partner/v1 through RWB-S9-E6035-CON, or remove the operation. |
| CDC-20098 | RWB-S9-E6035-APP | CG-ALL-11918 | 12.1 | Publish GET /partners (API-S9-001) under base /api/recovery/partner/v1 through RWB-S9-E6035-CON, or remove the operation. |
| CDC-20108 | RWB-S9-E6035-APP | DOR-RWB-S9-E6035-APP-8 | 13 | Add GET /partner/instructions (API-S9-003) and GET /partners (API-S9-001) to rwb-partner.yaml, and the 6 further paths and bases the detcheck lists. |
| CDC-20117 | RWB-S9-E6035-CON | CG-ALL-11937 | 12.1 | Add path /api/recovery/partner/v1/partner/instructions with GET operation API-S9-003 as described in RWB-S9-E6035-CON section 12.1. |
| CDC-20118 | RWB-S9-E6035-CON | CG-ALL-11938 | 12.1 | Add path /api/recovery/partner/v1/partners with GET operation API-S9-001 as described in RWB-S9-E6035-CON section 12.1. |
| CDC-20125 | RWB-S9-E6035-CON | DOR-RWB-S9-E6035-CON-8 | find it | Add GET /partner/instructions (API-S9-003) and GET /partners (API-S9-001) on base /api/recovery/partner/v1, add bases /api/recovery/payment/v1 and /api/recovery/case/v1, and add the five further paths or bases named in the detcheck. |
| CDC-20195 | RWB-S9-E7013-APP | CG-ALL-12014 | 12.2 | Remove the fixed enum on status; treat LOV-INSTR-STATUS values as reference data accepted without a code change. |
| CDC-20196 | RWB-S9-E7013-APP | CG-ALL-12015 | 12.2 | Remove the fixed enum on instructionType; treat LOV-INSTRUCTION values as reference data accepted without a code change. |
| CDC-20197 | RWB-S9-E7013-APP | CG-ALL-12016 | 12.2 | Remove the fixed enum on panelStatus; treat LOV-PANEL values as reference data accepted without a code change. |
| CDC-20198 | RWB-S9-E7013-APP | CG-ALL-12017 | 12.2 | Remove the fixed enum on partnerType; treat LOV-PARTNER-TYPE values as reference data accepted without a code change. |
| CDC-20201 | RWB-S9-E7013-APP | DOR-RWB-S9-E7013-APP-8 | 12 | Add the bases /api/recovery/decision/v1 and /api/recovery/case/v1 to an API Specification v5 yaml; hold status and instructionType as LOV references in rwb-partner.yaml, not closed enums. |
| CDC-20217 | RWB-S9-E7013-CON | DOR-RWB-S9-E7013-CON-8 | 11 | Add the bases /api/recovery/decision/v1 and /api/recovery/case/v1; declare status and instructionType as LOV references, not closed enums, in rwb-partner.yaml |
| CDC-20225 | RWB-S9-E7014-APP | CG-ALL-12044 | 12.1 | Publish POST /api/recovery/partner/v1/cases/{caseId}/instructions (API-S9-002) through RWB-S9-E7014-CON, or remove it. |
| CDC-20226 | RWB-S9-E7014-APP | CG-ALL-12045 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions (API-S9-003) through RWB-S9-E7014-CON, or remove it. |
| CDC-20227 | RWB-S9-E7014-APP | CG-ALL-12046 | 12.1 | Publish GET /api/recovery/partner/v1/partners (API-S9-001) through RWB-S9-E7014-CON, or remove it. |
| CDC-20239 | RWB-S9-E7014-CON | CG-ALL-12059 | 12.1 | Publish POST /api/recovery/partner/v1/cases/{caseId}/instructions (API-S9-002) in the yaml, or remove it from the story. |
| CDC-20240 | RWB-S9-E7014-CON | CG-ALL-12060 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions (API-S9-003) in the yaml, or remove it from the story. |
| CDC-20241 | RWB-S9-E7014-CON | CG-ALL-12061 | 12.1 | Publish GET /api/recovery/partner/v1/partners (API-S9-001) in the yaml, or remove it from the story. |
| CDC-20245 | RWB-S9-E7014-CON | DOR-RWB-S9-E7014-CON-8 | 12.1, 12.2 | Publish or confirm the paths and REST bases in CG-ALL-12059 to CG-ALL-12063; the story rows are already in place. |
| CDC-20267 | RWB-S9-E7015-CON | CG-ALL-12087 | 12.1 | Publish GET /api/recovery/partner/v1/partners in the paths of rwb-partner.yaml under the single base prefix, or remove the row from RWB-S9-E7015-CON. |
| CDC-20268 | RWB-S9-E7015-CON | CG-ALL-12088 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions in the paths of rwb-partner.yaml under the single base prefix, or remove the row from RWB-S9-E7015-CON. |
| CDC-20292 | RWB-S9-E7016-CON | CG-ALL-12117 | 12.1 | Publish GET /api/recovery/partner/v1/partners in rwb-partner.yaml |
| CDC-20293 | RWB-S9-E7016-CON | CG-ALL-12118 | 12.1 | Publish GET /api/recovery/partner/v1/partner/instructions in rwb-partner.yaml |
| CDC-20295 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-8 | 12.1, 12.5 | Publish GET partners and GET partner/instructions operations (CG-ALL-12117, CG-ALL-12118) |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (31)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20111 | RWB-S9-E6035-APP | CG-ALL-11927 | 12.5 | Add activity matchAgencyRecovery to the Activities sheet. |
| CDC-20112 | RWB-S9-E6035-APP | CG-ALL-11928 | 12.5 | Add activity calculateAgencyFee to the Activities sheet. |
| CDC-20134 | RWB-S9-E7011-APP | DOR-RWB-S9-E7011-APP-8 | 12.2 | Add activities collectMeasuredResults and evaluateScorecardRules. The +1 more finding: Not specified in the source documents (DOR-RWB-S9-E7011-APP-8). |
| CDC-20137 | RWB-S9-E7011-APP | CG-ALL-11957 | 12.5 | Add activity collectMeasuredResults to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-20138 | RWB-S9-E7011-APP | CG-ALL-11958 | 12.5 | Add activity evaluateScorecardRules to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-20139 | RWB-S9-E7011-APP | CG-ALL-11959 | 12.5 | Add activity publishScorecard to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-20171 | RWB-S9-E7012-APP | CG-ALL-11988 | 12.5 | Add activity readFeeClaim on task queue rwb-partner, or use a catalogued activity. |
| CDC-20172 | RWB-S9-E7012-APP | CG-ALL-11989 | 12.5 | Add activity evaluateFeeClaim on task queue rwb-partner, or use a catalogued activity. |
| CDC-20184 | RWB-S9-E7012-CON | CG-ALL-12003 | 12.5 | Add activity readFeeClaim with task queue rwb-partner to the Activities sheet, or name a catalogued activity |
| CDC-20185 | RWB-S9-E7012-CON | CG-ALL-12004 | 12.5 | Add activity evaluateFeeClaim with task queue rwb-partner to the Activities sheet, or name a catalogued activity |
| CDC-20186 | RWB-S9-E7012-CON | CG-ALL-12005 | 12.5 | Add activity recordFeeApproval with task queue rwb-partner to the Activities sheet, or name a catalogued activity |
| CDC-20236 | RWB-S9-E7014-APP | CG-ALL-12051 | 12.5 | Add the activity issuePartnerNotice to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-20246 | RWB-S9-E7014-CON | CG-ALL-12066 | 12.5 | Add an Activities row for issuePartnerNotice on task queue rwb-partner, or name a catalogued activity in RWB-S9-E7014-CON section 12.5. |
| CDC-20254 | RWB-S9-E7015-APP | DOR-RWB-S9-E7015-APP-8 | 12.5 | Add catalog entries for activity readOpenInstructions and the other 12.5 names not in v1, and state the InstructionWorkflow Workflow ID form and start rule. |
| CDC-20256 | RWB-S9-E7015-APP | CG-ALL-12076 | 12.5 | Add an Activities row for readOpenInstructions on task queue rwb-partner, with the inputs and outputs stated in §12.5. |
| CDC-20257 | RWB-S9-E7015-APP | CG-ALL-12077 | 12.5 | Add an Activities row for evaluateRecallRules on task queue rwb-partner, with the inputs and outputs stated in §12.5. |
| CDC-20258 | RWB-S9-E7015-APP | CG-ALL-12078 | 12.5 | Add an Activities row for recordAndApplyExit on task queue rwb-partner, with the inputs and outputs stated in §12.5. |
| CDC-20259 | RWB-S9-E7015-APP | CG-ALL-12079 | 12.5 | Add an Activities row for requestCaseReselection on task queue rwb-partner, with the inputs and outputs stated in §12.5. |
| CDC-20271 | RWB-S9-E7015-CON | CG-ALL-12092 | 12.5 | Add activity readOpenInstructions with task queue rwb-partner. Story §12.5 is unchanged. |
| CDC-20272 | RWB-S9-E7015-CON | CG-ALL-12093 | 12.5 | Add activity evaluateRecallRules with task queue rwb-partner. Story §12.5 is unchanged. |
| CDC-20273 | RWB-S9-E7015-CON | CG-ALL-12094 | 12.5 | Add activity recordAndApplyExit with task queue rwb-partner. Story §12.5 is unchanged. |
| CDC-20274 | RWB-S9-E7015-CON | CG-ALL-12095 | 12.5 | Add activity requestCaseReselection with task queue rwb-partner. Story §12.5 is unchanged. |
| CDC-20280 | RWB-S9-E7016-APP | DOR-RWB-S9-E7016-APP-8 | 12.5 | Add catalogue rows for activity readConductSample and the other 12.5 activities not listed, and the InstructionWorkflow ID form and start rule. |
| CDC-20283 | RWB-S9-E7016-APP | CG-ALL-12105 | 12.5 | Add activity readConductSample (task queue rwb-partner) to the Activities sheet. |
| CDC-20284 | RWB-S9-E7016-APP | CG-ALL-12106 | 12.5 | Add activity evaluateConductRules (task queue rwb-partner) to the Activities sheet. |
| CDC-20285 | RWB-S9-E7016-APP | CG-ALL-12107 | 12.5 | Add activity recordAndApplyBreach (task queue rwb-partner) to the Activities sheet. |
| CDC-20286 | RWB-S9-E7016-APP | CG-ALL-12108 | 12.5 | Add activity requestCaseReselection (task queue rwb-partner) to the Activities sheet. |
| CDC-20296 | RWB-S9-E7016-CON | CG-ALL-12122 | 12.5 | Add an Activities row for readConductSample, or the story names a catalogued activity instead |
| CDC-20297 | RWB-S9-E7016-CON | CG-ALL-12123 | 12.5 | Add an Activities row for evaluateConductRules, or the story names a catalogued activity instead |
| CDC-20298 | RWB-S9-E7016-CON | CG-ALL-12124 | 12.5 | Add an Activities row for recordAndApplyBreach, or the story names a catalogued activity instead |
| CDC-20299 | RWB-S9-E7016-CON | CG-ALL-12125 | 12.5 | Add an Activities row for requestCaseReselection, or the story names a catalogued activity instead |

### API:(service not named) (30)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20072 | RWB-S9-E6034-APP | CG-ALL-11888 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |
| CDC-20073 | RWB-S9-E6034-APP | CG-ALL-11889 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision provider, taken from the Document Index service table. |
| CDC-20088 | RWB-S9-E6034-CON | CG-ALL-11905 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read, per the Document Index service table. |
| CDC-20089 | RWB-S9-E6034-CON | CG-ALL-11906 | 12.2 | Declare REST base /api/recovery/decision/v1 for the placement-rule read, per the Document Index service table. |
| CDC-20099 | RWB-S9-E6035-APP | CG-ALL-11919 | 12.2 | Declare REST base /api/recovery/payment/v1, taken from the Document Index service table. |
| CDC-20100 | RWB-S9-E6035-APP | CG-ALL-11920 | 12.2 | Declare REST base /api/recovery/case/v1, taken from the Document Index service table. |
| CDC-20101 | RWB-S9-E6035-APP | CG-ALL-11921 | 12.2 | Declare REST base /api/recovery/case/v1 for the reference-data read, taken from the Document Index service table. |
| CDC-20102 | RWB-S9-E6035-APP | CG-ALL-11922 | 12.2 | Declare REST base /api/recovery/decision/v1, taken from the Document Index service table. |
| CDC-20119 | RWB-S9-E6035-CON | CG-ALL-11939 | 12.2 | Declare REST base /api/recovery/payment/v1 for the posted-payment read (operation name not specified in source; GAP-3120, ASM-5404). |
| CDC-20120 | RWB-S9-E6035-CON | CG-ALL-11940 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read (operation name not specified in source; GAP-3120, ASM-5404). |
| CDC-20121 | RWB-S9-E6035-CON | CG-ALL-11941 | 12.2 | Declare REST base /api/recovery/case/v1 for the reference-data read of the fee schedule and LOVs (operation name not specified; GAP-3120, ASM-5407). |
| CDC-20122 | RWB-S9-E6035-CON | CG-ALL-11942 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read in force (operation name not specified; GAP-3120, ASM-5406). |
| CDC-20130 | RWB-S9-E7011-APP | CG-ALL-11955 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the rwb-source-data provider, using the Document Index service table. |
| CDC-20131 | RWB-S9-E7011-APP | CG-ALL-11956 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider, using the Document Index service table. |
| CDC-20150 | RWB-S9-E7011-CON | CG-ALL-11966 | 12.2 | Declare the REST base `/api/recovery/source-data/v1` for the provider, as in the Document Index service table. |
| CDC-20151 | RWB-S9-E7011-CON | CG-ALL-11967 | 12.2 | Declare the REST base `/api/recovery/decision/v1` for the provider, as in the Document Index service table. |
| CDC-20163 | RWB-S9-E7012-APP | CG-ALL-11979 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-20164 | RWB-S9-E7012-APP | CG-ALL-11980 | 12.2 | Declare REST base /api/recovery/document/v1 from the Document Index service table. |
| CDC-20168 | RWB-S9-E7012-APP | DOR-RWB-S9-E7012-APP-8 | header | Add the case/v1 and document/v1 base paths; replace closed enums for status and instructionType in rwb-partner.yaml with LOV-INSTR-STATUS and LOV-INSTRUCTION; clear the 8 further findings. |
| CDC-20181 | RWB-S9-E7012-CON | CG-ALL-11998 | 12.2 | Declare the REST base `/api/recovery/document/v1` for the rwb-document provider (P5) from the Document Index service table. |
| CDC-20182 | RWB-S9-E7012-CON | CG-ALL-11999 | 12.2 | Declare the REST base `/api/recovery/case/v1` for the rwb-case provider (P3) from the provider's REST base in the service table. |
| CDC-20183 | RWB-S9-E7012-CON | DOR-RWB-S9-E7012-CON-8 | find it | Declare REST bases `/api/recovery/document/v1` and `/api/recovery/case/v1` (CG-ALL-11998, CG-ALL-11999); the story-side P1 items and the workflow ID rule are resolved in this story. |
| CDC-20193 | RWB-S9-E7013-APP | CG-ALL-12012 | 12.2 | Declare the REST base /api/recovery/decision/v1, using the provider's REST base from the Document Index service table. |
| CDC-20194 | RWB-S9-E7013-APP | CG-ALL-12013 | 12.2 | Declare the REST base /api/recovery/case/v1, using the provider's REST base from the Document Index service table. |
| CDC-20214 | RWB-S9-E7013-CON | CG-ALL-12029 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision provider, taken from the Document Index service table. |
| CDC-20215 | RWB-S9-E7013-CON | CG-ALL-12030 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |
| CDC-20228 | RWB-S9-E7014-APP | CG-ALL-12047 | 12.2 | Declare REST base /api/recovery/comms/v1 in the rwb-comms yaml, using the provider base from the Document Index service table. |
| CDC-20229 | RWB-S9-E7014-APP | CG-ALL-12048 | 12.2 | Declare REST base /api/recovery/case/v1 in the rwb-case yaml, using the provider base from the Document Index service table. |
| CDC-20242 | RWB-S9-E7014-CON | CG-ALL-12062 | 12.2 | Declare REST base /api/recovery/comms/v1 for the rwb-comms provider, taken from the Document Index service table. |
| CDC-20243 | RWB-S9-E7014-CON | CG-ALL-12063 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (22)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20063 | RWB-S9-E6033-CON | DOR-RWB-S9-E6033-CON-12 | 7, 16 | Register TC-E6-033-03, TC-S9-E6033-CON-01, TC-S9-E6033-CON-02, TC-S9-E6033-CON-03 and TC-S9-E6033-CON-04. |
| CDC-20068 | RWB-S9-E6033-CON | CG-ALL-11878 | 16 | Add rows TC-E6-033-03 and TC-S9-E6033-CON-01 to TC-S9-E6033-CON-04, with Given, When and Then copied from the criteria they cover |
| CDC-20081 | RWB-S9-E6034-APP | CG-ALL-11896 | 16 | Add rows TC-E6-034-01 to TC-E6-034-10 with Given, When and Then copied from the criterion or exception each row covers, including the new rows of section 16. |
| CDC-20093 | RWB-S9-E6034-CON | DOR-RWB-S9-E6034-CON-12 | 12.7, 16 | Add story test cases TC-E6-034-01 to -04 and TC-S9-E6034-CON-01 to -05 to tab Story test cases; add TC-S9-E6034-CON-06 and -07. |
| CDC-20096 | RWB-S9-E6034-CON | CG-ALL-11910 | 16 | Add rows for TC-E6-034-01 to -04 and TC-S9-E6034-CON-01 to -05, with Given, When and Then copied from the criterion each covers. |
| CDC-20113 | RWB-S9-E6035-APP | CG-ALL-11930 | 16 | Add rows TC-E6-035-01 to TC-E6-035-04 to tab Story test cases, with Given, When and Then copied from the criterion or section 5 path each covers. |
| CDC-20129 | RWB-S9-E6035-CON | CG-ALL-11949 | 16 | Add rows for TC-E6-035-01 to TC-E6-035-04 and TC-S9-E6035-CON-01 to TC-S9-E6035-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-20140 | RWB-S9-E7011-APP | CG-ALL-11961 | 16 | Add rows TC-E7-011-01 to TC-E7-011-04 with Given, When and Then copied from the criteria they cover. |
| CDC-20159 | RWB-S9-E7011-CON | DOR-RWB-S9-E7011-CON-12 | 16 | Add rows for TC-E7-011-01 to TC-E7-011-04 and TC-S9-E7011-CON-01 to TC-S9-E7011-CON-07, and TC-S9-E7011-CON-08 added in §16. |
| CDC-20162 | RWB-S9-E7011-CON | CG-ALL-11972 | 16 | Add rows TC-E7-011-01 to -04 and TC-S9-E7011-CON-01 to -07 with Given, When and Then copied from the criterion each covers. |
| CDC-20174 | RWB-S9-E7012-APP | CG-ALL-11991 | 16 | New rows -05 to -08 in section 16 |
| CDC-20192 | RWB-S9-E7012-CON | CG-ALL-12006 | 16 | Add rows for TC-E7-012-01 to -04 and TC-S9-E7012-CON-01 to -07 with Given, When and Then copied from the criteria they cover; also add TC-S9-E7012-CON-10 and -11 added in this story. |
| CDC-20205 | RWB-S9-E7013-APP | CG-ALL-12021 | 16 | Add rows TC-E7-013-01 to TC-E7-013-04 to Story test cases with Given, When and Then copied from the criteria they cover. |
| CDC-20221 | RWB-S9-E7013-CON | DOR-RWB-S9-E7013-CON-12 | 16 | Add Story test case rows for TC-E7-013-01 to -04 and TC-S9-E7013-CON-01 to -08 |
| CDC-20224 | RWB-S9-E7013-CON | CG-ALL-12037 | 16 | Add rows for TC-E7-013-01 to TC-E7-013-04 and TC-S9-E7013-CON-01 to TC-S9-E7013-CON-07, with Given, When and Then copied from the criteria they cover. |
| CDC-20237 | RWB-S9-E7014-APP | CG-ALL-12052 | 16 | Add rows TC-E7-014-01 to TC-E7-014-04 to the next version, tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-20250 | RWB-S9-E7014-CON | CG-ALL-12067 | 16 | Add rows TC-E7-014-01 to -04 and TC-S9-E7014-CON-01 to -07 with Given, When and Then copied from their criteria. |
| CDC-20260 | RWB-S9-E7015-APP | CG-ALL-12080 | 16 | In tab Story test cases, add rows TC-E7-015-01 to TC-E7-015-04 with Given, When and Then copied from the criteria and Data in §16. |
| CDC-20278 | RWB-S9-E7015-CON | CG-ALL-12096 | 16 | Add rows for TC-E7-015-01 to -04 and TC-S9-E7015-CON-01 to -08, plus new -09 and -10, with Given, When and Then copied from the criterion each covers. |
| CDC-20287 | RWB-S9-E7016-APP | CG-ALL-12110 | 16 | Add rows TC-E7-016-01, TC-E7-016-02, TC-E7-016-03 and TC-E7-016-04 with Given, When and Then copied from the criterion each covers. |
| CDC-20302 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-12 | 16 | Test case rows TC-S9-E7016-CON-08 to -14 added to section 16. |
| CDC-20307 | RWB-S9-E7016-CON | CG-ALL-12127 | 16 | Add rows for TC-E7-016-01 to -04 and TC-S9-E7016-CON-01 to -11, each with Given, When and Then copied from the criterion it covers. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20078 | RWB-S9-E6034-APP | CG-ALL-11882 | 4 | Record soft_recovery as a dictionary field or entity, or record the object (index, library table, flag) in the owning document. |
| CDC-20079 | RWB-S9-E6034-APP | CG-ALL-11883 | 11 | Record decision_record as a dictionary field or entity, or record the object (index, library table, flag) in the owning document. |
| CDC-20080 | RWB-S9-E6034-APP | CG-ALL-11884 | 17 | Record recovery_log as a dictionary field or entity, or record the object (index, library table, flag) in the owning document. |
| CDC-20141 | RWB-S9-E7011-APP | DOR-RWB-S9-E7011-APP-7 | 11 | Register decision_record and recovery_log as rwb_partner library objects, or confirm they are not needed. |
| CDC-20153 | RWB-S9-E7011-CON | CG-ALL-11965 | 12.7 | Record `decision_record` as a PLT library object created in `rwb_partner` (local hash-linked scorecard entry, DP-03), or use a dictionary name. |
| CDC-20175 | RWB-S9-E7012-APP | DOR-RWB-S9-E7012-APP-7 | 11 | Add decision_record (DP-03 library table) and recovery_log as fields or entities, or confirm their names; AC2 legacy wording stays by design. |
| CDC-20202 | RWB-S9-E7013-APP | CG-ALL-12010 | 12.7 | Add decision_record as a dictionary entity, or record the platform library object in rwb_partner in the owning document. |
| CDC-20203 | RWB-S9-E7013-APP | CG-ALL-12011 | 12.9 | Add recovery_log to the dictionary or confirm it is retired, since the story names it only in a no-write rule. |
| CDC-20207 | RWB-S9-E7013-APP | DOR-RWB-S9-E7013-APP-7 | 11, 17 | Add entity decision_record as a platform library object of rwb_partner; do not add recovery_log. |
| CDC-20218 | RWB-S9-E7013-CON | CG-ALL-12028 | 12.7 | Record decision_record as the PLT library object of DP-03 (local hash-linked review entry) or add its dictionary name |
| CDC-20255 | RWB-S9-E7015-APP | CG-ALL-12071 | 11, 12.7, 13 | Record decision_record as a platform library object created in rwb_partner by the library migration (DP-03), or add the dictionary name. |
| CDC-20261 | RWB-S9-E7015-APP | DOR-RWB-S9-E7015-APP-7 | 11 | Add decision_record as the platform library table in rwb_partner (DP-03), or record it as outside LDM scope; add recovery_log as an entity or field, or record it as not an entity. Legacy job and decision-log wording fixed in story (CG-ALL-12082). |
| CDC-20270 | RWB-S9-E7015-CON | CG-ALL-12086 | 12.7 | Record decision_record as a PLT library created in rwb_partner (object, not a field), or align the story name to a dictionary field. |
| CDC-20276 | RWB-S9-E7015-CON | DOR-RWB-S9-E7015-CON-7 | 11 | Add decision_record as a field or entity, or confirm the library name the section 12 decision_record row uses. Story side: BR Field ID column added to section 11. |

### Epic design record (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20059 | RWB-S9-E6033-CON | DOR-RWB-S9-E6033-CON-14 | header | Record the signed epic design sign-off for this story's epic; no sign-off appears in the story or sources. |
| CDC-20074 | RWB-S9-E6034-APP | DOR-RWB-S9-E6034-APP-14 | header | Record the signed epic design sign-off for EP06 covering RWB-S9-E6034-APP. |
| CDC-20104 | RWB-S9-E6035-APP | DOR-RWB-S9-E6035-APP-14 | n/a | Record the signed epic design sign-off, then confirm DoR item 14 against it. |
| CDC-20124 | RWB-S9-E6035-CON | DOR-RWB-S9-E6035-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S9, which no source document contains; confirm it before the story is marked ready. |
| CDC-20165 | RWB-S9-E7012-APP | DOR-RWB-S9-E7012-APP-14 | find it | Record the signed epic design sign-off, or confirm it is recorded; no signed design is in the story or source documents. |
| CDC-20199 | RWB-S9-E7013-APP | DOR-RWB-S9-E7013-APP-14 | header | Confirm and record the signed epic design sign-off for EP07 / RWB-SVC-S9; no sign-off is recorded in the story or source documents. |
| CDC-20230 | RWB-S9-E7014-APP | DOR-RWB-S9-E7014-APP-14 |  | Record the signed epic design sign-off in the epic design record; no sign-off is in the source set. |
| CDC-20251 | RWB-S9-E7015-APP | DOR-RWB-S9-E7015-APP-14 | Not in story | Record the signed epic design sign-off for this story's epic. |
| CDC-20269 | RWB-S9-E7015-CON | DOR-RWB-S9-E7015-CON-14 | 1 | Record the signed epic design sign-off that this story relies on, so the story can cite it. |
| CDC-20294 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S9 (EP07) in the epic design record and confirm it. Not specified in the source documents (DOR-RWB-S9-E7016-CON-14). |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20082 | RWB-S9-E6034-APP | GAP-1799 | find it | Add the S7 to S6 hand-over cell and the S6 to S7 cell; record the call type and direction as an open question for the S6 owner before wave 4 system test. |
| CDC-20083 | RWB-S9-E6034-APP | GAP-1798 | find it | Add the S7 to S9 cell for placement, result and recall; hold placement decisions until the rwb-partner contract is published in wave 4; sequence the placement slice last in wave 4. |
| CDC-20091 | RWB-S9-E6034-CON | GAP-1845 | 12.5 | Publish InstructionWorkflow, EV-20 and EV-21 as a contract ahead of wave 4 so rwb-litigation and rwb-asset build against the fake in wave 3. No release date changes in this story. |
| CDC-20169 | RWB-S9-E7012-APP | GAP-1836 | 12.5 | Add the S9 cell to P8 and confirm the rwb-payment path for payment, proceeds, ALS and GL posting and fees. |
| CDC-20180 | RWB-S9-E7012-APP | GAP-1857 |  | Add the S9 Partner row cell to P7 and route the fee approval through the rwb-decision approval workflow on Temporal, as the other route services do. |
| CDC-20191 | RWB-S9-E7012-CON | GAP-1857 | 7 | Add the S9 Partner row cell to P7 as T for the fee approval, routed through the rwb-decision ApprovalWorkflow by Temporal, as the S2, S3, S5, S6 and S7 rows show. |
| CDC-20212 | RWB-S9-E7013-APP | GAP-1859 | 5 | Add the S9 cells to P6 for the Temporal notice call and the subscription to the rwb-comms delivery event. |
| CDC-20223 | RWB-S9-E7013-CON | GAP-1859 | none | Add the two S9 cells to P6: a Temporal call to rwb-comms for the contractual notice and a subscription to its delivery event, as rwb-litigation has. |
| CDC-20264 | RWB-S9-E7015-APP | GAP-1841 | find it | Add rwb-partner rows for the monthly scorecard and the conduct sample as Temporal Schedules through the workflow kit. |
| CDC-20265 | RWB-S9-E7015-APP | GAP-1858 | find it | Publish scorecard, review outcome and conduct result as events on rwb.partner.events.v1 and add S9 to the P9 subscription, or confirm the report is produced inside this service. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20136 | RWB-S9-E7011-APP | CG-ALL-11953 | 13 | Ownership row marks decision_record as a library object, not an LDM v9 entity |
| CDC-20160 | RWB-S9-E7011-CON | DOR-RWB-S9-E7011-CON-7 | 11 | Add decision_record as an entity or field, or confirm it as the PLT library object of DP-03 that rwb_partner holds. It is absent from LDM v9 and Data Classification v5 (pipeline cache copies). |
| CDC-20170 | RWB-S9-E7012-APP | CG-ALL-11977 | 17 | Record decision_record as a library table of rwb_partner (or use the dictionary name) in LDM v9 Fields. |
| CDC-20234 | RWB-S9-E7014-APP | CG-ALL-12042 | 2 | Record cure_period_days as a field or object in LDM v9 or Data Classification v5, or the story uses the dictionary name. Story line 55 is outside this chunk. |
| CDC-20235 | RWB-S9-E7014-APP | CG-ALL-12043 | 11 | Record decision_record as the PLT library table created in rwb_partner (already named in section 12.7), or use a dictionary name from the nearest-names list. |
| CDC-20281 | RWB-S9-E7016-APP | CG-ALL-12100 | 11, 12.7, 13 | Record decision_record as a platform library object created in rwb_partner by the library migration (DP-03), not as an LDM field or entity. |
| CDC-20282 | RWB-S9-E7016-APP | CG-ALL-12101 | 17 | Record recovery_log as a retired legacy object so the negative reference in the story resolves; no current field or entity of that name. |
| CDC-20288 | RWB-S9-E7016-APP | DOR-RWB-S9-E7016-APP-7 | 11 | Record decision_record as the platform library table of rwb_partner (DP-03) or name it under Data Classification v5 as a library object. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20061 | RWB-S9-E6033-CON | DOR-RWB-S9-E6033-CON-1 | 1 | Add the role contract owner of the partner service, or its role code, so that section 1 names a listed role. |
| CDC-20092 | RWB-S9-E6034-CON | DOR-RWB-S9-E6034-CON-1 | 1 | Confirm a role code for the rwb-partner tech lead; 'tech lead' is not a role code or role name in this document. |
| CDC-20157 | RWB-S9-E7011-CON | DOR-RWB-S9-E7011-CON-1 | 1 | Add a role code and role name for the delivery role 'tech lead' to Users Roles and Permissions v5. Role code: Not specified in the source documents (DOR-RWB-S9-E7011-CON-1). Story §1 stays unchanged until then. |
| CDC-20219 | RWB-S9-E7013-CON | DOR-RWB-S9-E7013-CON-1 | 1 | Add a role code and role name for 'tech lead of rwb-partner' |
| CDC-20247 | RWB-S9-E7014-CON | DOR-RWB-S9-E7014-CON-1 | 1 | Add the role tech lead with its role code, or name the existing role code that the story should use in section 1. |
| CDC-20275 | RWB-S9-E7015-CON | DOR-RWB-S9-E7015-CON-1 | 1 | Add the role 'tech lead' as a role code or role name, or the story must use an existing role name. |
| CDC-20300 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-1 | 1 | Add a role code or role name for tech lead, or name an existing role in section 1 |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20154 | RWB-S9-E7011-CON | CG-ALL-11968 | 12.5 | Add activity `collectMeasuredResults` (task queue `rwb-partner`) or use a catalogued activity. |
| CDC-20155 | RWB-S9-E7011-CON | CG-ALL-11969 | 12.5 | Add activity `evaluateScorecardRules` (task queue `rwb-partner`) or use a catalogued activity. |
| CDC-20156 | RWB-S9-E7011-CON | CG-ALL-11970 | 12.5 | Add activity `publishScorecard` (task queue `rwb-partner`) or use a catalogued activity. |
| CDC-20173 | RWB-S9-E7012-APP | CG-ALL-11990 | 12.5 | Add activity recordFeeApproval on task queue rwb-partner, matching the contract element in section 12.5. |
| CDC-20204 | RWB-S9-E7013-APP | CG-ALL-12020 | 12.5 | Add readReviewFacts to the Activities sheet, or point the story at a catalogued activity. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20109 | RWB-S9-E6035-APP | GAP-1840 | 8 | Author the partner route set from FSD A2.3, A2.4 and A2.8 to A2.15 and govern it in rwb-decision. |
| CDC-20135 | RWB-S9-E7011-APP | GAP-1840 | 9 | Add a partner route set from FSD A2.3, A2.4 and A2.8 to A2.15, governed in rwb-decision and evaluated in this service with the embedded Drools kit. |
| CDC-20143 | RWB-S9-E7011-APP | GAP-3121 | 7, 8 | Publish scorecard rule rows, the two consumed reads, and a reporting path or a recorded decision that no scorecard fact is reported. |
| CDC-20208 | RWB-S9-E7013-APP | GAP-3125 | 8 | Publish a partner review rule row, its route set, event and route to partner and agency manager; add the in-service H row for the scorecard to RWB-S9-E7011-APP. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20103 | RWB-S9-E6035-APP | CG-ALL-11923 | 13 | Create story RWB-P7-E1073-CON for the rule-package dependency, or name the existing story that carries it. |
| CDC-20105 | RWB-S9-E6035-APP | DOR-RWB-S9-E6035-APP-17 | header | Depends on (build) names three stories; none is RWB-P7-E1073-CON in the supplied text, so the story cannot resolve the item. |
| CDC-20123 | RWB-S9-E6035-CON | CG-ALL-11943 | 13 | Create the story file for RWB-P7-E1073-CON, the Drools kit row named in section 13, or re-point the dependency to an existing story. Owner: Solution architect. |

### RWB-S9-E7011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20132 | RWB-S9-E7011-APP | DOR-RWB-S9-E7011-APP-21 | header | Set the build status of RWB-S9-E7011-CON to Done. |
| CDC-20133 | RWB-S9-E7011-APP | DOR-RWB-S9-E7011-APP-22 | header | Record a published contract fake library version for RWB-S9-E7011-CON. |
| CDC-20144 | RWB-S9-E7011-APP | GAP-3122 | 12 | Tag the baseline with placeholders for the two consumed reads, publish the scorecard operations and reads or record that the score is the only scorecard fact. |

### RWB-S9-E7011-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20158 | RWB-S9-E7011-CON | DOR-RWB-S9-E7011-CON-10 |  | No story edit in this document |
| CDC-20161 | RWB-S9-E7011-CON | GAP-3121 | 11 | Placeholders recorded in §11 of the contract story only as a pointer |
| CDC-20213 | RWB-S9-E7013-APP | CG-ALL-12026 | 15 | Add the empty, loading, error and no access states of SCR-36 from Screen Specifications v1, with Not specified in the source documents (CG-ALL-12026) where the spec lacks them. |

### RWB-S9-E7012-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20166 | RWB-S9-E7012-APP | DOR-RWB-S9-E7012-APP-21 | header | Set build status to Done so the contract is published. |
| CDC-20167 | RWB-S9-E7012-APP | DOR-RWB-S9-E7012-APP-22 | header | Publish a contract fake library version and record it as published. |
| CDC-20178 | RWB-S9-E7012-APP | GAP-3124 |  | Publish the approval and decided-claim read operations with rights and errors; confirm approval-entry attributes; publish the fee-schedule entity; add rwb-document and partner gateway to plan C and X rows; resolve delegate in TSD S9 T6.1; settle the P3 subscription; decide the route to rwb-payment. |

### RWB-S9-E7015-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20252 | RWB-S9-E7015-APP | DOR-RWB-S9-E7015-APP-21 | Header | Bring the contract story build status from Not started to Done. |
| CDC-20253 | RWB-S9-E7015-APP | DOR-RWB-S9-E7015-APP-22 | Header | Publish a contract fake library version and record it. |
| CDC-20263 | RWB-S9-E7015-APP | GAP-3130 | find it | Publish contract-end operation or confirm workflow command; define open; publish case-side re-selection command and answer; settle refusal code for a result on a recalled instruction; author partner service level row or confirm R-UNI-26; confirm partner_user engagement. |

### RWB-S9-E6034-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20075 | RWB-S9-E6034-APP | DOR-RWB-S9-E6034-APP-21 | header | Set build status to Done. |
| CDC-20076 | RWB-S9-E6034-APP | DOR-RWB-S9-E6034-APP-22 | header | Publish the contract fake library and record its version. |

### RWB-S9-E6035-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20106 | RWB-S9-E6035-APP | DOR-RWB-S9-E6035-APP-21 | header | Build to Done and publish; its build status is Not started. |
| CDC-20107 | RWB-S9-E6035-APP | DOR-RWB-S9-E6035-APP-22 | header | Publish a contract fake library version and record it. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20126 | RWB-S9-E6035-CON | CG-ALL-11946 | 12.5 | Add an activity row for matchAgencyRecovery (rwb-partner, the match step) or name a catalogued activity in this story. |
| CDC-20127 | RWB-S9-E6035-CON | CG-ALL-11947 | 12.5 | Add an activity row for calculateAgencyFee (rwb-partner, the fee step) or name a catalogued activity in this story. |

### OTHER:Wave 4 integration harness configuration (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20176 | RWB-S9-E7012-APP | GAP-0473 |  | Record the harness environment and base hosts, fixture layout and synthetic keys, fee claim and schedule answer shape, evidence format and retention, and the pass or fail gate at the wave 4 entry check. |
| CDC-20209 | RWB-S9-E7013-APP | GAP-0474 | 16 | Record environment, base hosts, fixture layout, synthetic keys, evidence shape, retention and pass or fail gate. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20189 | RWB-S9-E7012-CON | GAP-3123 | find it | Publish the fee-approval operation on the partner base or name the existing one; decide column, list value or decision record only; add the partner-fee rule row, fee-schedule entity and Finance and CFO delegate correction |
| CDC-20305 | RWB-S9-E7016-CON | GAP-3131 | find it | Publish the conduct rule package and row IDs, the sample contract of the contact and complaint owners, the check trigger binding, the definition of upheld, and the case re-selection command with its answer shape. |

### RWB-S9-E7013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20200 | RWB-S9-E7013-APP | DOR-RWB-S9-E7013-APP-21 | header | Complete the contract story and set its build status to Done; the contract is then published. Current status is Not started. |
| CDC-20210 | RWB-S9-E7013-APP | GAP-3126 | 8, 13 | Publish the rule-package and reference-data reads with fields and 2 s budget, status and action lists with versions, partner_user description, and confirm no review event. |

### RWB-ITG-E7015-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20262 | RWB-S9-E7015-APP | GAP-0479 | find it | Agree SIT base hosts, fixture layout and synthetic keys, stub answer shapes, contract-end fixture hook and answer, open-case definition, evidence format and retention, and pass or fail gate; record in README. |
| CDC-20277 | RWB-S9-E7015-CON | GAP-0479 | 7 | Record SIT base hosts, fixture layout, synthetic keys, stub answer shapes, contract-end fixture hook and answer, open-case definition, evidence format and retention, and pass or fail gate at the wave 4 entry check. |

### RWB-S9-E7016-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20279 | RWB-S9-E7016-APP | DOR-RWB-S9-E7016-APP-21 | n/a | Complete the build of RWB-S9-E7016-CON to Done (currently Not started) so the contract is published. |
| CDC-20291 | RWB-S9-E7016-APP | GAP-3132 | find it | Publish the sample contract and owner, the upheld outcome, the case re-selection command and the conduct rule package; re-tag the baseline additively. |

### RWB-ITG-E7016-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20289 | RWB-S9-E7016-APP | GAP-0476 | 3, 12.8, 13, 15 | Record the harness environment, fixtures, answer shapes, sample size and method, conduct hook, evidence format and gate; keep the placeholder here. |
| CDC-20304 | RWB-S9-E7016-CON | GAP-0476 | find it | Record the harness environment and base hosts, fixture layout and synthetic keys, stub answer shapes, sample size and method, conduct-trigger hook, evidence format and gate in the harness configuration at wave 4 entry. |

### OTHER:The document that defines SCR-34 and SCR-35 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20062 | RWB-S9-E6033-CON | DOR-RWB-S9-E6033-CON-10 | find it | Add empty, loading, error and no-access states to SCR-34 and SCR-35. |

### OTHER:Specification APIs sheet and features sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20064 | RWB-S9-E6033-CON | GAP-1482 | 1 | Keep the E4 tag on /cases/{caseId}/instructions and /partner/instructions; FEAT-PRM-03 and FEAT-PRM-05 consume them under E6. |

### RWB-ITG-E6033-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20065 | RWB-S9-E6033-CON | GAP-0463 | 1, 3, 12.8, 13, 15 | Record the SIT base hosts, fixture layout, synthetic key scheme, result reference and answer shape, same-day cut-off, evidence format and retention, and pass or fail gate at the wave 4 entry check |

### OTHER:TSD S9 T-A.2 and the parameters contract of rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20066 | RWB-S9-E6033-CON | GAP-3114 | 7 | Publish the API-S9-005 multipart bound, the two activity names, and the decision code and version in force at contract freeze; confirm retention with the records owner |

### OTHER:TSD S9 T-A.2 and T3.1; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20067 | RWB-S9-E6033-CON | GAP-3115 | 5, 7 | Publish the PartnerInstruction, InstructionPage and multipart schemas and the EV-21 payload with the case ID as key and ce_subject; take the partner gateway profile from the platform edge story |

### OTHER:Recovery Workbench Business Requirements Program v5 (BR-059 in BRD E38) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20084 | RWB-S9-E6034-APP | GAP-1854 | 11 | Source BR-059 placement to S9 FEAT-PRM-06 only; keep treatment and recovery with S7 under REQ-S7-006 and REQ-S7-007. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:FSD S7 A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20094 | RWB-S9-E6034-CON | GAP-1799 | none | Record the charged-off hand-over to the debt sale route (S6 rwb-debtsale) with population, route and approval; add the S6 and S7 cells with direction; settle call type with the S6 owner before wave 4 system test. |

### OTHER:FSD S7 A2.15 and A2.16; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20095 | RWB-S9-E6034-CON | GAP-1798 | none | Carry placement, result and recall as S7 product behaviour; add the S7 to S9 cell; hold placement decisions until the partner contract is published; sequence the placement slice last in wave 4. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:S9 row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20110 | RWB-S9-E6035-APP | GAP-1836 | 9 | Add the S9 cell to P8 and confirm the read-back contract path from rwb-payment. |

### RWB-S9-E6035-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20114 | RWB-S9-E6035-APP | GAP-3048 | find it | Keep the C row as None; record DP-04, DP-07, DP-09 and DP-16 as dependencies the plan does not hold; raise fee ownership to the solution architect before the baseline tag. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20115 | RWB-S9-E6035-APP | GAP-1838 | find it | partner_instruction.case_id: remove the CROSS_REF foreign key to recovery_case and the N:1 relationship; type it as a varchar(255) business key with no foreign key. |

### OTHER:Functional Specification Document S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20116 | RWB-S9-E6035-APP | GAP-1842 | find it | Replace the generic main-success rows of A2.1.4.1 to A2.15.4.4 with feature-specific statements; fill the alternate-flow and background tables; keep the AC-EXC rows. |

### OTHER:BA decision on MSG-P1-001 payment use (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20128 | RWB-S9-E6035-CON | CG-ALL-11948 MSG-P1-001 text differs from Error and Message Standard v4 | 14 | Text copied from Standard v4 |

### RWB-S9-E7013-APP; 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20142 | RWB-S9-E7011-APP | GAP-3125 | 8 | Publish one partner route set with a review rule row, review act and read, status, action and six-point lists with versions, review storage and event decisions, and the scorecard in-service H row. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20145 | RWB-S9-E7011-APP | GAP-1837 | 11 | Name the scorecard, fee-claim, review, conduct-sample and field-visit tables with the DB story, keeping partner, partner_user and partner_instruction. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20146 | RWB-S9-E7011-APP | GAP-1841 | 4 | Add job map rows for the monthly scorecard and the conduct sample as Temporal Schedules in rwb-partner through the workflow kit; give S9 its row in the Ownership Map. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:EV-20 and EV-21 consumers slide 43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20147 | RWB-S9-E7011-APP | GAP-1858 | 4 | Add S9 as a subscriber on the P9 Reporting row and publish the scorecard, review outcome and conduct result as events on rwb.partner.events.v1 for rwb-reporting. |

### OTHER:FSD S9 (field catalogs A2.1.3.2 to A2.15.3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20148 | RWB-S9-E7011-APP | GAP-1839 | 4 | Replace the eight repeated partner and instruction columns with one entity definition, and write the remaining field lists (scorecard, fee claim, review, conduct sample, breach, field visit, photograph, bill) in the story that first needs them. |

### OTHER:FSD S9 A2.8.2 (integration points) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20149 | RWB-S9-E7011-APP | GAP-1846 | 4 | Remove 'Power BI' from the A2.8 integration points; publish scorecard and review outcome as events and serve the forum from the rwb-reporting read model. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20152 | RWB-S9-E7011-CON | DOR-RWB-S9-E7011-CON-8 |  | Resolve the listed gaps: REST bases for source-data and decision (CG-ALL-11966, CG-ALL-11967); activities collectMeasuredResults, evaluateScorecardRules, publishScorecard (CG-ALL-11968 to CG-ALL-11970). Check the unlisted +1 item. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20177 | RWB-S9-E7012-APP | GAP-3123 |  | Publish or name the fee-approval operation; decide whether approved fee is a column, list value or decision record only; publish the partner-fee rule row; add the fee-schedule entity; add the Finance and CFO delegate to TSD S9 T6.1 or correct FSD S9 A2.9.3.3. |

### 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20179 | RWB-S9-E7012-APP | GAP-1837 |  | Name the scorecard, fee-claim, review, conduct-sample and field-visit tables with the DB story; keep partner, partner_user and partner_instruction unchanged. |

### RWB-S9-E7012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20187 | RWB-S9-E7012-CON | DOR-RWB-S9-E7012-CON-10 | find it | Add empty, loading, error and no-access states to the screen definitions of SCR-34 and SCR-35 |

### RWB-ITG-E7012-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20188 | RWB-S9-E7012-CON | GAP-0473 | find it | At the wave 4 entry check, record the harness environment and base hosts, fixture layout and synthetic keys, fee claim and schedule answer shape, evidence format and retention, and pass or fail gate |

### OTHER:TSD S9; OTHER:Context pack S9; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:plan C and X rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20190 | RWB-S9-E7012-CON | GAP-3124 | 1 | Publish the approval and decided-claim read operations on rwb-partner; confirm the approval-entry attributes; publish the fee-schedule entity or reference code; add rwb-document and the partner gateway to plan C and X rows; resolve the Finance and CFO delegate in TSD S9 T6.1; settle the T4 P3 subscription; decide how an approved fee reaches rwb-payment. |

### RWB-S9-E7011-APP; OTHER:SCR-36 Partner scorecard) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20206 | RWB-S9-E7013-APP | DOR-RWB-S9-E7013-APP-10 | 15 | Name the loading, list, empty, error and no access states of SCR-36 Partner scorecard in the screens and states section of RWB-S9-E7011-APP, as FEAT-PRM-08's screen. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20211 | RWB-S9-E7013-APP | GAP-1837 | 11 | Name the scorecard, fee-claim, review, conduct-sample and field-visit tables with the DB story; keep partner, partner_user and partner_instruction. |

### OTHER:Workflow catalog (InstructionWorkflow row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20216 | RWB-S9-E7013-CON | CG-ALL-12035 | 12.5 | Namespace rwb-recovery restored in the InstructionWorkflow row so it matches the baseline at L43. |

### RWB-S9-E7013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20220 | RWB-S9-E7013-CON | DOR-RWB-S9-E7013-CON-10 | 1 | State empty, loading, error and no-access states of SCR-34, SCR-35 and SCR-36 |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:FSD S9; RWB-S9-E7011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20222 | RWB-S9-E7013-CON | GAP-3125 | 8 | Publish a partner review rule row, its route set, the review operation, the status and action lists, and the in-service H row for the scorecard |

### RWB-S9-E7014-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20231 | RWB-S9-E7014-APP | DOR-RWB-S9-E7014-APP-21 |  | Set build status to Done once the contract is published. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20232 | RWB-S9-E7014-APP | DOR-RWB-S9-E7014-APP-22 |  | Publish the contract fake library version and record it as published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20233 | RWB-S9-E7014-APP | DOR-RWB-S9-E7014-APP-8 | 12 | Add POST /cases/{caseId}/instructions (API-S9-002), GET /partner/instructions (API-S9-003) and GET /partners (API-S9-001) to rwb-partner.yaml, and the base /api/recovery/comms/v1 to a v5 yaml. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:S9 rwb_partner rows); 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20238 | RWB-S9-E7014-APP | GAP-1837 | 11 | Add scorecard result, fee claim and approval, review, conduct sample and field visit tables to rwb_partner with field lists and keys, named with the DB story; keep partner, partner_user and partner_instruction as they are. |

### Epic design record; OTHER:RWB-SVC-S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20244 | RWB-S9-E7014-CON | DOR-RWB-S9-E7014-CON-14 | header | Confirm the signed epic design sign-off for EP07 and RWB-SVC-S9; the story and source documents record none. |

### RWB-S9-E7014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20248 | RWB-S9-E7014-CON | DOR-RWB-S9-E7014-CON-10 | find it | Add empty, loading, error and no-access states for SCR-34 and SCR-35 in the app story. |

### RWB-ITG-E7014-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20249 | RWB-S9-E7014-CON | GAP-0475 | find it | Record SIT base hosts, fixture layout, synthetic keys, stub answer shapes, score comparison, evidence format and pass or fail gate at the wave 4 entry check. |

### OTHER:Functional Specification Document S9 (FSD S9), section A2.8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20266 | RWB-S9-E7015-APP | GAP-1846 | find it | Replace Power BI in the integration points with the rwb-reporting read model served from events (Architecture v5, ADR-018); remove the data lake and daily copy interfaces. |

### OTHER:rwb-decision rule package and S9 contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20290 | RWB-S9-E7016-APP | GAP-3131 | find it | Publish the conduct rule package with row IDs, the sample contract with owner and fields, the trigger binding, the upheld definition, the case command and the batch-status read. |

### RWB-S9-E7016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20301 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-10 | find it | Add empty, loading, error and no-access states for SCR-34 and SCR-35 |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20303 | RWB-S9-E7016-CON | DOR-RWB-S9-E7016-CON-20 | find it | Add keys for sample size and sample period, and the lists read under DP-06 and DP-07; keys not specified in the source documents |

### OTHER:Recovery Workbench rwb-decision and the S9 contact and complaint owner contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20306 | RWB-S9-E7016-CON | GAP-3132 | find it | Publish the sample contract and its owner, the definition of upheld with the outcome recorded, the case re-selection command with its answer shape, and the conduct rule package. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0463 | Partner-result integration harness: environment, fixture keys, answer shapes, same-day cut-off, evidence and gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0473 | Wave 4 partner fee harness: environment, fixture, answer shapes, evidence and gate unspecified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0474 | Wave 4 integration harness for the partner review has no specified environment, fixture set or evidence gate | Integration lead | Resolved (directive) |
| GAP-0475 | Wave 4 notice-on-a-missed-target harness: environment, fixture keys, missed-target comparison, evidence and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0476 | Wave 4 conduct-check harness: environment, fixtures, sample size and method, conduct-trigger hook, evidence and gate are not specified | Integration lead | Resolved (directive) |
| GAP-0479 | Wave 4 contract-end and recall harness: environment, fixture hook, open-case definition and evidence gate are not specified | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1482 | Partner instruction is an Epic 4 endpoint in the specification and an Epic 6 feature in the same specification | Partner and agency manager | Resolved (directive) |
| GAP-1798 | Agency placement, result and recall run through the partner portal, which is S9 and is created in the same wave | Partner and agency manager with S9 | Resolved (directive) |
| GAP-1799 | A charged-off population is handed to the debt sale route, and neither service's matrix row shows the other | Solution architect with the S6 owner | Resolved (directive) |
| GAP-1836 | The FSD matches the agency recovery and the fee in this module, including ALS and GL, while v5 gives payment and proceeds to rwb-payment and the matrix gives S9 no cell to P8 | Solution architect with the P8 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1837 | The Ownership Map and the physical schema give three tables, while the service catalogue says the schema holds results, fees and scorecards as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1838 | partner_instruction.case_id is a cross-schema foreign key to recovery_case, while ADR-014 requires a business key and no foreign key out of the schema | Data architect with the platform DB owner | Resolved (directive) |
| GAP-1839 | The field catalog repeats the same eight partner columns in nine features and names no field for the scorecard, the fee claim, the review, the conduct sample or the field visit | Business analyst, S9 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1840 | No rule row covers allocation by measured return, scoring, review, fee approval, conduct sampling or the field app | Center of excellence analyst with P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1841 | The job map has no rwb-partner job, while the monthly scorecard and the conduct sample need a schedule | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1842 | Every FSD acceptance criterion in this module is the same generic statement, and no feature has an alternate flow or a background event | Business analyst, S9 | Resolved (directive) |
| GAP-1845 | Epic 4 and Epic 5 need partner instructions in wave 3, while rwb-partner is created in wave 4 | Solution architect with the S4 and S5 owners | Resolved (directive) |
| GAP-1846 | The FSD names Power BI as an integration point, and the data lake it reads was removed | Solution architect with the P9 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1854 | One placement rule has two owners: S7 owns the treatment decision and the recovery, and the FSD gives the placement itself to S9 | Solution architect with the S7 owner | Resolved (directive) |
| GAP-1856 | The scorecard measures, weights and thresholds are not in the sources, which repeat one metric for all fifteen features | Partner and agency manager with the center of excellence analyst | Resolved (directive) |
| GAP-1857 | The fee approval needs the approval workflow on rwb-decision, and the matrix gives S9 no cell to P7 | Solution architect with the P7 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1858 | Partner performance, conduct and complaint data must reach the review forum, and rwb-reporting subscribes to no partner event | Solution architect with the P9 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1859 | The contractual notice on a missed target has no path: the FSD gives the notice to this module and the matrix gives S9 no cell to rwb-comms | Solution architect with the P6 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2103 | The deck does not say whether a partner result is a partner record or a dated data product | Solution architect | Resolved (directive) |
| GAP-3048 | R-WO-37's agency fee calculation is also FEAT-PRM-07 of rwb-partner, and neither the plan's C rows nor DP-04, DP-07, DP-09 and DP-16 carry what the recovery step consumes | Solution architect | Resolved (directive) |
| GAP-3114 | The result-intake elements of rwb-partner are not fixed by any source: the 409 and 404 problem texts, the multipart bound, the decision code and version the local record names, the activity and signal names, and the retention of the request | Solution architect with the partner service owner | Resolved (directive) |
| GAP-3115 | The published shapes of the partner result contract are not fixed by any source: the multipart schema, the PartnerInstruction and InstructionPage element names, the event payload beyond three fields, the partner gateway profile and the error bodies | Solution architect with the platform edge owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3121 | RWB-S9-E7011-APP: the monthly scorecard has no rule row of its own, no trigger, no job, no workflow of its own, no published scorecard read and no reporting channel | Solution architect with the rwb-decision rule owner, the rwb-source-data owner and the platform scheduling owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3122 | RWB-S9-E7011-CON: the scorecard baseline declares no operation, no event, no Schedule and no scorecard table, and the two consumed reads and the SCR-36 measures element have no published artefact | Solution architect with the rwb-source-data owner, the rwb-decision owner and the rwb-access owner | Resolved (directive) |
| GAP-3123 | RWB-S9-E7012-APP: the fee-approval path has no published operation, no approval column or list value, no rule row and no fee-schedule entity | Solution architect with the API owner, the rwb-case reference-data owner, the rwb-decision rule owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3124 | RWB-S9-E7012-CON: the approval operation, the approval-entry attributes, the fee-schedule read, the three consumed rows and the delegate right have no published baseline | Solution architect with the API owner, the platform library owner, the rwb-case reference-data owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3125 | RWB-S9-E7013-APP: the partner review has no rule row, no operation, no action list, no column, no event and no in-service build row for its scorecard | Center of excellence with the solution architect, the rwb-decision rule owner, the rwb-access owner and the rwb-case reference-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3126 | RWB-S9-E7013-CON: the consumed operation names, the review read, the entry attributes, the action list and the review column have no published baseline | Solution architect with the rwb-decision owner, the rwb-case reference-data owner, the rwb-access owner and the platform library owner | Resolved (directive) |
| GAP-3129 | RWB-S9-E7015-APP: the contract end has no operation, the recall has no event, "open" has no definition, the partner service level sits on no PRM rule row and the case-side re-selection has no published boundary | Solution architect with the rwb-case owner, the rwb-decision rule owner and the center of excellence | Resolved (directive) |
| GAP-3130 | RWB-S9-E7015-CON: the contract-end act, the definition of "open", the case command name, the refusal code of a recalled instruction and the partner service level have no published baseline | Solution architect with the rwb-case owner, the rwb-decision rule owner, the rwb-access owner and the platform library owner | Resolved (directive) |
| GAP-3131 | RWB-S9-E7016-APP: the conduct check has no operation and no named trigger, the sample of contacts and complaints has no entity or owner, the sample size and period are unpublished, "upheld" is undefined, no PRM rule row carries the conduct rules, the batch status sits with rwb-source-data and the case re-selection boundary has no published name | Solution architect with the S9 business analyst, the rule owner in rwb-decision and the owners of rwb-comms and rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3132 | RWB-S9-E7016-CON: the sample element, the breach record element, the "upheld" outcome, the case command, the check operation and the rule set have no published baseline | Solution architect with the rwb-partner tech lead, the rule owner in rwb-decision and the owners of the sample and the case command | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S9-E7011-APP | new AC without TC row | 408 | AC5 is new and no section 16 row covers it |
| RWB-S9-E7012-APP | new AC without TC row | 421 | AC7 is new and no section 16 row covers it |
