# RWB-SVC-S7 rwb-writeoff (Write-off) - review pack, part 1 of 2 (RWB-S7-E6013-APP to RWB-S7-E6020-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 16 |
| Resolved in the stories | 303 |
| Cross-document (pending in another document) | 237 |
| Not applied (value not in the sources) | 30 |
| Open business decisions | 28 |
| Register gaps linked | 30 |
| Unconfirmed assumptions | 0 |
| Lint findings | 8 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S7-E6013-APP | 31 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6013 APP Run the monthly eligibility scan on both tracks v2.md |
| RWB-S7-E6013-CON | 22 | 7 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6013 CON Run the monthly eligibility scan on both tracks - contract v2.md |
| RWB-S7-E6014-APP | 29 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6014 APP Apply the tax criteria v2.md |
| RWB-S7-E6014-CON | 15 | 12 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6014 CON Apply the tax criteria - contract v2.md |
| RWB-S7-E6015-APP | 22 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6015 APP Prepare the write-off pack v2.md |
| RWB-S7-E6015-CON | 11 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6015 CON Prepare the write-off pack - contract v2.md |
| RWB-S7-E6016-APP | 23 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6016 APP Remove a case from the proposed population v2.md |
| RWB-S7-E6016-CON | 13 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6016 CON Remove a case from the proposed population - contract v2.md |
| RWB-S7-E6017-APP | 20 | 18 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6017 APP Route the population to the committee and schedule it v2.md |
| RWB-S7-E6017-CON | 14 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6017 CON Route the population to the committee and schedule it - contract v2.md |
| RWB-S7-E6018-APP | 24 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6018 APP Approve a write-off inside the limit v2.md |
| RWB-S7-E6018-CON | 12 | 15 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6018 CON Approve a write-off inside the limit - contract v2.md |
| RWB-S7-E6019-APP | 23 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6019 APP Reject a write-off v2.md |
| RWB-S7-E6019-CON | 10 | 11 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6019 CON Reject a write-off - contract v2.md |
| RWB-S7-E6020-APP | 22 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6020 APP Defer a write-off v2.md |
| RWB-S7-E6020-CON | 12 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6020 CON Defer a write-off - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-S1-E4009-APP, RWB-S1-E4009-CON, RWB-S2-E3003-APP, RWB-S2-E3003-CON, RWB-S7-E6018-APP, RWB-S7-E6018-CON | R-09221 | GAP-1464 | Register gap | Risk with the product heads | The approval limits by decision, product and amount are not set, so no approval requirement can be tested against its limit | Load the regulation's published levels as reference data in the version that applies at the release date, keep every limit and substitute as a versioned row with a valid-from date, and let each acceptance criterion run against the loaded version. No limit is written in this document, in a story or in code. |
| RWB-S7-E6013-APP | R-13185 | CG-ALL-10842 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6013-CON | R-13188 | CG-ALL-10851 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6014-APP | R-13195 | CG-ALL-10865 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6014-CON | R-13199 | CG-ALL-10876 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6015-APP | R-13206 | CG-ALL-10893 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6015-CON | R-13211 | CG-ALL-10910 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6016-APP | R-13218 | CG-ALL-10924 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6016-CON | R-13222 | CG-ALL-10937 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6017-APP | R-13228 | CG-ALL-10953 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6017-CON | R-13231 | CG-ALL-10967 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6018-APP | R-13236 | CG-ALL-10982 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6018-CON | R-13239 | CG-ALL-10996 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6019-APP | R-13246 | CG-ALL-11011 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6019-CON | R-13249 | CG-ALL-11023 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6020-APP | R-13254 | CG-ALL-11036 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S7-E6020-CON | R-13257 | CG-ALL-11048 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E6028-ITG, RWB-P7-E6028-APP, RWB-S7-E6018-APP, RWB-S7-E6018-CON, RWB-S7-E6028-APP, RWB-S7-E6028-CON | R-22834 | GAP-3049 | Register gap | Solution architect, business lead and the rwb-writeoff tech lead | RWB-S7-E6028-APP: no source publishes a sale-selection operation or a sold-population read, placement_type and the sale reference have no column, field ID or list, the entry state PLACEMENT_DECIDED is produced by an unclaimed rule, AC2's R-WO-12 is already built by RWB-S7-E6018-APP, the hand-off to rwb-debtsale has no edge, the debt sale officer holds right R only, and the plan's C row is empty while the step consumes three contracts | Declare the two operations on /api/recovery/writeoff/v1 with placeholder paths and element names confirmed by the solution architect; read placement_type and the sale reference as request inputs with placeholder value sets and no column; start the step at PLACEMENT_DECIDED and record that R-WO-29 is unclaimed in S7; assert R-WO-12 on the branch RWB-S7-E6018-APP builds instead of building it twice; describe the hand-off as the case move plus the published population read and declare no event; declare the selection at right C with the role conflict recorded; state the post-charge-off and sold states as edge placeholders; build against the three consumed rows as class C dependencies; trace to REQ-S7-006 from the FSD row. |
| RWB-PLT-E1071-CON, RWB-S7-E6013-APP, RWB-S7-E6014-APP, RWB-S7-E6014-CON | R-23202 | GAP-3018 | Register gap | Tech lead of rwb-writeoff with the P7 owner of the rule package and the Finance owner of the tax criteria | The tax criteria version, the remittance channel of R-WO-51, the home of the remittance record and the scan trigger have no owner, table or contract in rwb-writeoff | Publish the working read of ASM-B2-S7-002-1 to ASM-B2-S7-002-6 in RWB-S7-E6014-CON and apply it to RWB-S7-E6014-APP: tax_criteria_version is a package fact of rwb-decision read with its version and recorded with the outcome; the tax-criteria result is write_off.tax_criteria_met and the post charge off remittance is write_off.recovered_after with no new table or column; the R-WO-51 confirmation reaches the step as a signal the parent CaseWorkflow forwards and no subscription is declared; the monthly scan Schedule from JOB-16 belongs to RWB-S7-E6013-APP and the DP-10, DP-04 and DP-09 rows are recorded as absent rather than added; the three consumed rows are declared as class C rows on the baseline and faked. Confirm with the P7 owner of the rule package and the Finance owner of the tax criteria at the wave 4 contract freeze. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23240 | GAP-3029 | Register gap | Solution architect; business lead | RWB-S7-E6019-APP: the reject reason and the decision code have no field, column or list, R-WO-16's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes three contracts, DP-04 and DP-09 are absent, and no published row moves a case out of RETURNED_TO_PURSUE | Keep the plan's H, C, I and X rows as they stand; record the reason and the decision code as request and record inputs with a placeholder until the business lead confirms them; map R-WO-16's owner to the four roles that hold right A in TSD S7 T6.1; declare the three consumed rows in sections 12.2 and 12.8 and record the absent DP-04 and DP-09 rows; leave the onward path of RETURNED_TO_PURSUE to the case owner and raise it in the next planning cut; keep committee_date and every other write_off column out of the reject slice |
| RWB-S7-E6013-APP, RWB-S7-E6013-CON, RWB-S7-E6023-APP, RWB-S7-E6023-CON | R-23622 | GAP-1805 | Register gap | Head of Asset Liquidity with Risk | The write-off cap the epic BRD's risk names has no requirement, no rule and no value | Report the population against the cap once the cap exists, and take the cap, its basis and its period as an open question; no value is asserted here and no cap is enforced in this release. |
| RWB-S7-E6018-APP, RWB-S7-E6018-CON, RWB-S7-E6019-APP, RWB-S7-E6019-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23630 | GAP-1806 | Register gap | Risk with the product heads | The committee that decides a write-off above the limit, and the delegation behind it, are not defined | Take the approval through the approval workflow with the limit read from the delegation table at run time, record the level applied and the approver role, and take the level values and the committee composition as an open question under DL18 and Q-001. |
| RWB-S7-E6019-APP, RWB-S7-E6019-CON | R-23631 | GAP-3030 | Register gap | Solution architect; business lead | RWB-S7-E6019-CON: the CommitteeDecision and DecisionLogEntry elements, the decision code set, the reason field and the three consumed operation names have no published baseline, and the error set carries no message ID per condition | Publish the baseline with the placeholders, bind every error condition to one message id of section 14, declare the rejection inside the one published operation and not as a second path, declare the case and package rows as consumed and faked, record the decision-record element and the rights, and trace to REQ-S7-003 on the FSD table until the TSD T8 map is corrected |
| RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23632 | GAP-3032 | Register gap | Solution architect; business lead | RWB-S7-E6020-CON: the CommitteeDecision and DecisionLogEntry properties, the review-date addition, the review-timer element name, the four consumed operation names and the message per error condition have no published baseline | Publish the baseline over the API Specification v4 elements and name TSD S7 T-A.2 as the source of the operation and the error codes; declare reviewDate as the one additive optional property with a placeholder; bind every error condition to one message id of section 14; declare the defer inside the one published operation and not as a second path; declare the case read, the two moves, the timer answer and the package row as consumed and faked; declare the review timer as a durable workflow timer and register nothing; trace to REQ-S7-003 on the FSD table until the TSD T8 map is corrected |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-P9-E6037-APP, RWB-P9-E6037-CON, RWB-S7-E6013-APP, RWB-S7-E6013-CON | R-29025 | GAP-1815 | Register gap | Product Owner | No approval is recorded for the BRD or the FSD this PRD is built from, and this version is Draft | Carry the PRD as Draft, leave the approval table empty, and record the missing approval as an assumption so that no approval is claimed for a document nobody signed. |
| RWB-S7-E6014-APP, RWB-S7-E6014-CON | R-38644 | ASM-5011 | Register assumption |  | The tax criteria are a versioned fact in force read with the WO rule package from rwb-decision (P7), and tax_criteria_version is recorded with every outcome; the value is never a constant, a default or a branch of the code. An absent version holds the scan under R-WO-03 with MSG-S7-001 and writes nothing. | P7 owner of the rule package with the Finance owner of the tax criteria and the rwb-writeoff tech lead at the wave 4 contract freeze |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S7-E6013-APP | R-20790 | DOR-RWB-S7-E6013-APP-11 | 17 | Definition of Ready item 11 Guardrails: Partial | Data Classification v5 DF-FIN-013 to DF-FIN-020 are Personal data Yes; Guardrails 'No personal data' line must change. Section 17 text is not in this chunk, so no exact old text. |
| RWB-S7-E6013-CON | R-08593 | DOR-RWB-S7-E6013-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the supplied story text or sources; the directive names no record ID. Sign-off would need an invented reference, so it stays open. |
| RWB-S7-E6013-CON | R-20804 | DOR-RWB-S7-E6013-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Conflicts with R-32903; new AC8 belongs in section 7 with a section 16 row, outside the supplied parts. |
| RWB-S7-E6013-CON | R-27616 | CG-ALL-10853 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The JOB-nn, decision log and job record wording is in AC7 (section 7), which is not in the supplied parts. Section 12.5 has no match, so no anchored edit. |
| RWB-S7-E6013-CON | R-32903 | NEWAC-RWB-S7-E6013-CON-AC8 | 7 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | New AC8 belongs in section 7 with a section 16 test row. Neither part is in the supplied text, so no anchored edit. The proposed test is not specified in the sources. |
| RWB-S7-E6014-CON | R-20822 | DOR-RWB-S7-E6014-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Fix needs BR1 to BR13 mapped to criteria and test rows in sections 7 and 16. Their text is not in this chunk, so there is no safe anchor. Not applied. |
| RWB-S7-E6014-CON | R-27622 | CG-ALL-10877 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The JOB-nn or decision-log line is in a section 7 criterion or section 16 test, outside this chunk. Its exact text cannot be copied as old. Not applied. |
| RWB-S7-E6014-CON | R-32912 | NEWAC-RWB-S7-E6014-CON-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 closing line and section 16 anchor are not in this chunk, so AC8 and its test row cannot be placed. Proposed test: Not specified in the source documents (NEWAC-RWB-S7-E6014-CON-AC8). |
| RWB-S7-E6015-APP | R-20834 | DOR-RWB-S7-E6015-APP-7 | 11 | Definition of Ready item 7 Data: Partial | §11 already says provision_carried, residual, pack_document_id and decision_record are in no LDM v9/DCv5 entry. ACE reads in criteria and test data are in sections not supplied, so Partial remains. |
| RWB-S7-E6015-CON | R-08619 | DOR-RWB-S7-E6015-CON-17 | Not in supplied text | Definition of Ready item 17 Dependencies: Fail | Dependency naming is in a section outside this chunk. RWB-P7-E1073-CON is not in the supplied text; header dependency rows already read None. Needs the naming section. |
| RWB-S7-E6015-CON | R-20836 | DOR-RWB-S7-E6015-CON-10 | Not in supplied text | Definition of Ready item 10 Screens and states: Partial | SCR-27 empty, loading, error and no-access states sit in section 8 or later, outside this chunk. No supplied text to edit; needs those sections. |
| RWB-S7-E6015-CON | R-20837 | DOR-RWB-S7-E6015-CON-11 | Not in supplied text | Definition of Ready item 11 Guardrails: Partial | The no-personal-data statement is outside this chunk, so it cannot be aligned with Data Classification v5. Needs the guardrails section. |
| RWB-S7-E6016-APP | R-20842 | DOR-RWB-S7-E6016-APP-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | Section text not in chunk. screen-specifications-v1.md (07-screens-and-experience) lists no empty, loading, error or no-access state for SCR-27. Not specified in the source documents (DOR-RWB-S7-E6016-APP-10). |
| RWB-S7-E6016-APP | R-20843 | DOR-RWB-S7-E6016-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | Guardrail sentence and P2 fields not in chunk. SCR-27 field table in screen-specifications-v1.md marks all 8 fields Personal data = No. Story text needed to edit; not in chunk. |
| RWB-S7-E6016-CON | R-27634 | CG-ALL-10938 | 7 | Criteria and tests keep legacy job and decision-log wording | AC7 line with JOB-nn, decision log or job record wording is not in this chunk; section 7 text needed. Section 12.5 is not a criterion or test. No edit made. |
| RWB-S7-E6017-APP | R-20860 | DOR-RWB-S7-E6017-APP-10 | not in chunk | Definition of Ready item 10 Screens and states: Partial | SCR-27 state text sits in the story's screen section, outside this chunk. FSD S7 v3/v4 name SCR-27 only in tables. No anchor to edit. |
| RWB-S7-E6017-APP | R-20861 | DOR-RWB-S7-E6017-APP-11 | not in chunk | Definition of Ready item 11 Guardrails: Partial | The personal-data statement and the Data Classification v5 field list are outside this chunk. No field can be classed without them. |
| RWB-S7-E6017-APP | R-20866 | DOR-RWB-S7-E6017-APP-3 | 5, 7 | Definition of Ready item 3 Acceptance criteria: Partial | AC5 needs a section 16 TC row. The next free TC ID and the rows after TC-E6-017-06 are outside this chunk. X9 cover unchanged. |
| RWB-S7-E6017-APP | R-32930 | NEWAC-RWB-S7-E6017-APP-AC5 | 7, 16 | AC5: §5 X9: A component, a statement or a test reaches another service's schema, a queue table or a `v_ace_*` view (covered by 'Section 17, BR6' only) | Proposed test is not specified in the sources. The section 16 TC row needs a next free TC ID and rows outside this chunk. |
| RWB-S7-E6017-APP | R-32931 | NEWAC-RWB-S7-E6017-APP-AC6 | 7, 16 | AC6: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Proposed test is not specified in the sources. The section 16 TC row needs a next free TC ID and rows outside this chunk. |
| RWB-S7-E6017-CON | R-27643 | CG-ALL-10968 | 7 | Criteria and tests keep legacy job and decision-log wording | AC7 line (section 7) is not in the supplied text, so its old text cannot be copied. Section 12.5 has no JOB-nn, decision log or job record wording to change. |
| RWB-S7-E6017-CON | R-32935 | NEWAC-RWB-S7-E6017-CON-AC8 | 7, 16 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in the supplied text, so no AC8 or test row can be placed in their style. Story file not found by Glob, so not read. |
| RWB-S7-E6018-APP | R-08644 | DOR-RWB-S7-E6018-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed E6 epic design record in the sources. Searched all .md exports: DoR v3, Ways of Working v3, DT05 and stakeholder map give only the monthly sign-off process. Needs the signed record. |
| RWB-S7-E6018-APP | R-32939 | NEWAC-RWB-S7-E6018-APP-AC6 | 7 | AC6: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Adding AC and TC rows needs section 7 and 16 text, which is outside this chunk. Test steps and data for BR1-BR11 are not in the sources (Not specified in the source documents). |
| RWB-S7-E6018-CON | R-20890 | DOR-RWB-S7-E6018-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | Field names are not in the sources. Grep of 22 Microservice Realignment finds no CON-11 entry, and the story text for the guardrails section was not in this chunk. Needs a data-owner list of fields. |
| RWB-S7-E6019-CON | R-20911 | DOR-RWB-S7-E6019-CON-7 | 11 | Definition of Ready item 7 Data: Partial | No BR Field ID for the 9 §11 rows in the story. The project grep finds BR Field ID only in TSD P2/P8 and scratch files, none for this story. Assigning one would invent a value. |
| RWB-S7-E6019-CON | R-27657 | CG-ALL-11024 | 7 | Criteria and tests keep legacy job and decision-log wording | AC7 text is not in this chunk, so its old text cannot be copied. §12.5 has no legacy JOB-nn or decision-log wording. AC7 needs an edit in a chunk that includes §7. |
| RWB-S7-E6019-CON | R-32952 | NEWAC-RWB-S7-E6019-CON-AC8 | 7 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so the AC8 criterion and its test row cannot be inserted. Proposed test: Not specified in the source documents (NEWAC-RWB-S7-E6019-CON-AC8). |
| RWB-S7-E6020-CON | R-27664 | CG-ALL-11049 | 7 | Criteria and tests keep legacy job and decision-log wording | AC7 text is outside this chunk, so no anchor exists. Section 12.5 has no legacy wording; JOB-16 is a catalog citation and is kept. |
| RWB-S7-E6020-CON | R-32960 | NEWAC-RWB-S7-E6020-CON-AC8 | 7 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so no anchor exists. Test data is Not specified in the source documents (NEWAC-RWB-S7-E6020-CON-AC8). |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (46)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18917 | RWB-S7-E6014-APP | CG-ALL-10858 | 12.2 | Declare REST base /api/recovery/case/v1 for the provider P3 rwb-case population read. |
| CDC-18918 | RWB-S7-E6014-APP | CG-ALL-10859 | 12.2 | Declare REST base /api/recovery/decision/v1 for the provider P7 rwb-decision rule-package read. |
| CDC-18931 | RWB-S7-E6014-CON | CG-ALL-10869 | 12.2 | Declare REST base /api/recovery/case/v1 for the provider P3 rwb-case from the Document Index service table |
| CDC-18932 | RWB-S7-E6014-CON | CG-ALL-10870 | 12.2 | Declare REST base /api/recovery/decision/v1 for the provider P7 rwb-decision from the Document Index service table |
| CDC-18934 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-8 | 12.2 | Declare REST bases for /api/recovery/case/v1 and /api/recovery/decision/v1 |
| CDC-18943 | RWB-S7-E6015-APP | CG-ALL-10882 | 12.2 | Declare REST base `/api/recovery/case/v1` for rwb-case (P3), as given in the Document Index service table. |
| CDC-18944 | RWB-S7-E6015-APP | CG-ALL-10883 | 12.2 | Declare REST base `/api/recovery/source-data/v1` for rwb-source-data (P1), as given in the Document Index service table. |
| CDC-18945 | RWB-S7-E6015-APP | CG-ALL-10884 | 12.2 | Declare REST base `/api/recovery/document/v1` for rwb-document (P5), as given in the Document Index service table. |
| CDC-18946 | RWB-S7-E6015-APP | CG-ALL-10885 | 12.2 | Declare REST base `/api/recovery/document/v1` for rwb-document (P5), as given in the Document Index service table. |
| CDC-18947 | RWB-S7-E6015-APP | CG-ALL-10886 | 12.2 | Declare REST base `/api/recovery/agent/v1` for rwb-agent (P10), as given in the Document Index service table. |
| CDC-18948 | RWB-S7-E6015-APP | CG-ALL-10887 | 12.2 | Declare REST base `/api/recovery/decision/v1` for rwb-decision (P7), as given in the Document Index service table. |
| CDC-18954 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-8 | n/a | Add the bases /api/recovery/case/v1, /api/recovery/source-data/v1, /api/recovery/document/v1, /api/recovery/agent/v1 and the four further listed bases. |
| CDC-18966 | RWB-S7-E6015-CON | CG-ALL-10899 | 12.2 | Declare REST base /api/recovery/case/v1 for the case-facts and route-history read. |
| CDC-18967 | RWB-S7-E6015-CON | CG-ALL-10900 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the balance and asset-state data-product read. |
| CDC-18968 | RWB-S7-E6015-CON | CG-ALL-10901 | 12.2 | Declare REST base /api/recovery/document/v1 for the document-index read. |
| CDC-18969 | RWB-S7-E6015-CON | CG-ALL-10902 | 12.2 | Declare REST base /api/recovery/document/v1 for the pack document registration. |
| CDC-18970 | RWB-S7-E6015-CON | CG-ALL-10903 | 12.2 | Declare REST base /api/recovery/agent/v1 for the write-off pack run. |
| CDC-18971 | RWB-S7-E6015-CON | CG-ALL-10904 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read in force. |
| CDC-18974 | RWB-S7-E6015-CON | DOR-RWB-S7-E6015-CON-8 | find it | Add bases /api/recovery/case/v1, /api/recovery/source-data/v1, /api/recovery/document/v1, /api/recovery/agent/v1 and the four further bases in the detcheck. |
| CDC-18985 | RWB-S7-E6016-APP | CG-ALL-10917 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table |
| CDC-18986 | RWB-S7-E6016-APP | CG-ALL-10918 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table |
| CDC-19002 | RWB-S7-E6016-CON | CG-ALL-10930 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case operations consumed in 12.2. |
| CDC-19003 | RWB-S7-E6016-CON | CG-ALL-10931 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read consumed in 12.2. |
| CDC-19018 | RWB-S7-E6017-APP | CG-ALL-10944 | 12.2 | Declare the REST base /api/recovery/case/v1 as given in the Document Index service table. |
| CDC-19019 | RWB-S7-E6017-APP | CG-ALL-10945 | 12.2 | Declare the REST base /api/recovery/deviation/v1 as given in the Document Index service table. |
| CDC-19020 | RWB-S7-E6017-APP | CG-ALL-10946 | 12.2 | Declare the REST base /api/recovery/decision/v1 as given in the Document Index service table. |
| CDC-19036 | RWB-S7-E6017-CON | CG-ALL-10958 | 12.2 | Declare the REST base /api/recovery/case/v1 taken from the Document Index service table. |
| CDC-19037 | RWB-S7-E6017-CON | CG-ALL-10959 | 12.2 | Declare the REST base /api/recovery/deviation/v1 taken from the Document Index service table. |
| CDC-19038 | RWB-S7-E6017-CON | CG-ALL-10960 | 12.2 | Declare the REST base /api/recovery/decision/v1 taken from the Document Index service table. |
| CDC-19040 | RWB-S7-E6017-CON | DOR-RWB-S7-E6017-CON-8 | 12.1, 12.2 | Resolve the yaml gaps so the contract check passes. |
| CDC-19053 | RWB-S7-E6018-APP | CG-ALL-10973 | 12.2 | Declare REST base /api/recovery/case/v1 as given by the Document Index service table. |
| CDC-19054 | RWB-S7-E6018-APP | CG-ALL-10974 | 12.2 | Declare REST base /api/recovery/case/v1 as given by the Document Index service table. |
| CDC-19055 | RWB-S7-E6018-APP | CG-ALL-10975 | 12.2 | Declare REST base /api/recovery/decision/v1 as given by the Document Index service table. |
| CDC-19056 | RWB-S7-E6018-APP | CG-ALL-10976 | 12.2 | Declare REST base /api/recovery/access/v1 as given by the Document Index service table. |
| CDC-19068 | RWB-S7-E6018-CON | CG-ALL-10987 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-19069 | RWB-S7-E6018-CON | CG-ALL-10988 | 12.2 | Declare REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-19070 | RWB-S7-E6018-CON | CG-ALL-10989 | 12.2 | Declare REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-19071 | RWB-S7-E6018-CON | CG-ALL-10990 | 12.2 | Declare REST base /api/recovery/access/v1 from the Document Index service table. |
| CDC-19083 | RWB-S7-E6019-APP | CG-ALL-11004 | 12.2 | Declare REST base /api/recovery/case/v1 using the provider's base from the Document Index service table. |
| CDC-19084 | RWB-S7-E6019-APP | CG-ALL-11005 | 12.2 | Declare REST base /api/recovery/decision/v1 using the provider's base from the Document Index service table. |
| CDC-19098 | RWB-S7-E6019-CON | CG-ALL-11016 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read, from the Document Index service table. |
| CDC-19099 | RWB-S7-E6019-CON | CG-ALL-11017 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule-package read, from the Document Index service table. |
| CDC-19109 | RWB-S7-E6020-APP | CG-ALL-11029 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case in its yaml, using the Document Index service table. |
| CDC-19110 | RWB-S7-E6020-APP | CG-ALL-11030 | 12.2 | Declare REST base /api/recovery/decision/v1 for rwb-decision in its yaml, using the Document Index service table. |
| CDC-19123 | RWB-S7-E6020-CON | CG-ALL-11041 | 12.2 | Declare REST base /api/recovery/case/v1 in the provider yaml. |
| CDC-19124 | RWB-S7-E6020-CON | CG-ALL-11042 | 12.2 | Declare REST base /api/recovery/decision/v1 in the provider yaml. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (24)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18903 | RWB-S7-E6013-APP | CG-ALL-10841 | 16 | Add rows TC-E6-013-01 to TC-E6-013-05 with Given, When and Then copied from the criterion each covers. |
| CDC-18916 | RWB-S7-E6013-CON | CG-ALL-10850 | 16 | Add rows for TC-E6-013-01 to -05 and TC-S7-E6013-CON-01 to -05 with Given, When and Then copied from the criteria they cover |
| CDC-18926 | RWB-S7-E6014-APP | CG-ALL-10864 | 16 | Add rows TC-E6-014-01 to TC-E6-014-06 with Given, When and Then copied from AC1 to AC4, the Access criterion and the Principle 5 criterion. |
| CDC-18941 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-12 | 12.7, 16 | Add Given, When and Then for TC-S7-E6014-CON-06 and the 11 listed IDs under the same IDs in Test Cases v8. |
| CDC-18942 | RWB-S7-E6014-CON | CG-ALL-10875 | 16 | Add rows for TC-E6-014-01 to -06 and TC-S7-E6014-CON-01 to -05, with Given, When and Then copied from the criterion each covers. |
| CDC-18959 | RWB-S7-E6015-APP | CG-ALL-10892 | 16 | Add rows for TC-E6-015-01 to TC-E6-015-07 with Given, When and Then copied from AC1 to AC5 of this story |
| CDC-18977 | RWB-S7-E6015-CON | DOR-RWB-S7-E6015-CON-12 | 12.7, 16 | Add rows for TC-E6-015-01 to -05, TC-S7-E6015-CON-01 to -05 and TC-S7-E6015-CON-06 under the same IDs. |
| CDC-18983 | RWB-S7-E6015-CON | CG-ALL-10909 | 16 | Add rows TC-E6-015-01 to TC-E6-015-05 and TC-S7-E6015-CON-01 to TC-S7-E6015-CON-05 with Given, When and Then from the criterion each covers |
| CDC-18995 | RWB-S7-E6016-APP | CG-ALL-10923 | 16 | Add rows TC-E6-016-01 to TC-E6-016-05 with Given, When and Then copied from the AC1, AC2, AC3, Access and Principle 5 criteria. |
| CDC-18996 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-12 | 12, 12.7, 16 | Add Story test cases rows TC-E6-016-01 to TC-E6-016-09 under the same IDs; §16 now holds the contract (06) and boundary (07) rows |
| CDC-19011 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-12 | 12.7 | Add rows TC-E6-016-01 to -05 and TC-S7-E6016-CON-01 to -07 on tab Story test cases. |
| CDC-19016 | RWB-S7-E6016-CON | CG-ALL-10936 | 16 | Add rows TC-E6-016-01 to TC-E6-016-05 and TC-S7-E6016-CON-01 to TC-S7-E6016-CON-05, with Given, When and Then copied from the criteria they cover. |
| CDC-19028 | RWB-S7-E6017-APP | CG-ALL-10952 | 16 | Add rows TC-E6-017-01 to TC-E6-017-06 with Given, When and Then copied from the criteria they cover. |
| CDC-19044 | RWB-S7-E6017-CON | DOR-RWB-S7-E6017-CON-12 | 12.7, 16 | On tab Story test cases, add rows for TC-E6-017-01 to -06 and TC-S7-E6017-CON-01 to -08. |
| CDC-19051 | RWB-S7-E6017-CON | CG-ALL-10966 | 16 | Add rows for TC-E6-017-01 to TC-E6-017-06 and TC-S7-E6017-CON-01 to TC-S7-E6017-CON-07, with Given, When and Then copied from the section 7 criterion each one covers. |
| CDC-19060 | RWB-S7-E6018-APP | CG-ALL-10981 | 16 | Add rows TC-E6-018-01 to TC-E6-018-06 with Given, When and Then copied from the criteria they cover. |
| CDC-19081 | RWB-S7-E6018-CON | CG-ALL-10995 | 16 | Add rows for TC-E6-018-01 to -06 and TC-S7-E6018-CON-01 to -05 with Given, When and Then copied from the criteria they cover |
| CDC-19093 | RWB-S7-E6019-APP | CG-ALL-11010 | 16 | Add rows TC-E6-019-01 to TC-E6-019-04 with Given, When and Then copied from the criteria for AC1, AC2, Access and Principle 5. |
| CDC-19094 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-12 | 16 | Add the Given, When and Then rows for TC-E6-019-01 to TC-E6-019-08 under the same IDs; TC-E6-019-05 to TC-E6-019-08 are new (D-RCV-60) |
| CDC-19106 | RWB-S7-E6019-CON | DOR-RWB-S7-E6019-CON-12 | 12.7, 16 | Add story test case rows TC-E6-019-01 to -04 and TC-S7-E6019-CON-01 to -06 under their IDs. |
| CDC-19107 | RWB-S7-E6019-CON | CG-ALL-11022 | 16 | Add rows for TC-E6-019-01 to TC-E6-019-04 and TC-S7-E6019-CON-01 to TC-S7-E6019-CON-05, with Given, When and Then copied from the criterion each covers. |
| CDC-19117 | RWB-S7-E6020-APP | CG-ALL-11035 |  | Add rows TC-E6-020-01 to TC-E6-020-05 with Given, When and Then copied from the criteria they cover. Owner: QA. |
| CDC-19130 | RWB-S7-E6020-CON | DOR-RWB-S7-E6020-CON-12 | 12.7, 16 | Add rows for TC-E6-020-01 to -05 and TC-S7-E6020-CON-01 to -06 (-06 new, D-RCV-60, boundary of the §12.7 tables). |
| CDC-19132 | RWB-S7-E6020-CON | CG-ALL-11047 | 16 | Add rows for TC-E6-020-01 to -05 and TC-S7-E6020-CON-01 to -05, with Given, When and Then copied from the criteria each row covers. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18900 | RWB-S7-E6013-APP | CG-ALL-10835 | find it | Record tax_criteria_version as a dictionary field or as the object that holds the tax criteria version, or name the dictionary field the story should use. |
| CDC-18901 | RWB-S7-E6013-APP | CG-ALL-10836 | find it | Record decision_record as the PLT library table created in rwb_writeoff, as section 12.7 of the story states. |
| CDC-18928 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-7 | 7, 11 | Register tax_criteria_version and decision_record as fields or entities, or confirm them as package-read and PLT library objects. |
| CDC-18955 | RWB-S7-E6015-APP | CG-ALL-10879 | header | Use the dictionary name for provision_carried, or record it as a pack element of RWB-S7-E6015-CON in the owning document. |
| CDC-18956 | RWB-S7-E6015-APP | CG-ALL-10880 | header | Use the dictionary name for pack_document_id, or record it as the pack document reference in the pack element of RWB-S7-E6015-CON. |
| CDC-18957 | RWB-S7-E6015-APP | CG-ALL-10881 | 11 | Record decision_record as the PLT library object created in rwb_writeoff, as section 11 already states. |
| CDC-18975 | RWB-S7-E6015-CON | CG-ALL-10898 | find it | Record provision_carried under its dictionary name, or record the object (index, library table or flag) in the owning document. No column exists (ASM-5023). |
| CDC-18978 | RWB-S7-E6015-CON | DOR-RWB-S7-E6015-CON-7 | 11 | Name provision_carried as a field or entity in LDM v9 and Data Classification v5, or the element it maps to |
| CDC-18991 | RWB-S7-E6016-APP | CG-ALL-10913 | header, 2, 3, 4, 9, 11 | Name removal_reason kept; section 11 row restored to 3 cells |
| CDC-18992 | RWB-S7-E6016-APP | CG-ALL-10914 | 11 | Add decision_record as a field or object, or record the local decision-record library as an object in the owning document. |
| CDC-18993 | RWB-S7-E6016-APP | CG-ALL-10915 | 17 | Add recovery_log as a field or entity, or record the object in the owning document. |
| CDC-18998 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-7 | 11 | Add removal_reason as a field and decision_record as an entity; recovery_log is named only as a retired element |
| CDC-19089 | RWB-S7-E6019-APP | CG-ALL-11000 | find it | Add decision_reason to the dictionary, or record the object in its owning document; the story then adopts the dictionary name. |
| CDC-19090 | RWB-S7-E6019-APP | CG-ALL-11001 | find it | Add decision_record to the dictionary, or record the object in its owning document; the story then adopts the dictionary name. |
| CDC-19091 | RWB-S7-E6019-APP | CG-ALL-11002 | find it | Add recovery_log to the dictionary, or record the object in its owning document; the story then adopts the dictionary name. |
| CDC-19096 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-7 | 11, 17 | Add decision_reason (R-WO-16 and R-WO-18 reason) and decision_record (DP-03 library object in rwb_writeoff) as entries; recovery_log is retired and needs no entry. |
| CDC-19115 | RWB-S7-E6020-APP | CG-ALL-11027 |  | Add decision_record to LDM v9 as a field or entity, or record it there as the PLT library object created in rwb_writeoff. Owner: Data. |
| CDC-19120 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-7 | 11 | Add decision_record as a library object of rwb_writeoff (DP-03) to the LDM v9 and Data Classification v5 entities. Story side P3 wording fixed under CG-ALL-11037. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18984 | RWB-S7-E6016-APP | CG-ALL-10916 | 12.1 | Publish POST /write-offs/{writeOffId}/removal through RWB-S7-E6016-CON, or remove the operation from section 12.1 |
| CDC-19001 | RWB-S7-E6016-CON | CG-ALL-10929 | 12.1 | Publish POST /write-offs/{writeOffId}/removal under base /api/recovery/writeoff/v1 with RemovalRequest in and WriteOffRemoval 200 out, or remove the operation from this story. |
| CDC-19005 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-8 |  | Publish the removal path and the REST bases /api/recovery/case/v1 and /api/recovery/decision/v1. Task queue fixed in 12.5 of this story. |
| CDC-19017 | RWB-S7-E6017-APP | CG-ALL-10943 | 12.1 | Publish the GET operation for the write-off read through RWB-S7-E6017-CON, or remove the read and its composite route leg. |
| CDC-19024 | RWB-S7-E6017-APP | DOR-RWB-S7-E6017-APP-8 | 12 | Add the GET path (GAP-3025; ASM-5038) to rwb-writeoff.yaml; add the bases /api/recovery/case/v1, /api/recovery/deviation/v1 and /api/recovery/decision/v1 and the four other flagged bases to the v5 yamls. |
| CDC-19035 | RWB-S7-E6017-CON | CG-ALL-10957 | 12.1 | Publish the GET operation on /api/recovery/writeoff/v1 with its owner operation ID, or remove it. Story keeps the placeholder until then. |
| CDC-19052 | RWB-S7-E6018-APP | CG-ALL-10972 | 12.1 | Publish POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision (API-S7-002) through RWB-S7-E6018-CON, or remove it. |
| CDC-19058 | RWB-S7-E6018-APP | DOR-RWB-S7-E6018-APP-8 | 12 | Add POST /write-offs/{writeOffId}/committee-decision (API-S7-002) to rwb-writeoff.yaml and add the listed /api/recovery bases to their yamls. |
| CDC-19067 | RWB-S7-E6018-CON | CG-ALL-10986 | 12.1 | Publish POST /write-offs/{writeOffId}/committee-decision (API-S7-002) under base /api/recovery/writeoff/v1. |
| CDC-19082 | RWB-S7-E6019-APP | CG-ALL-11003 | 12.1 | Publish POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision (API-S7-002) through RWB-S7-E6019-CON. |
| CDC-19097 | RWB-S7-E6019-CON | CG-ALL-11015 | 12.1 | Publish POST /write-offs/{writeOffId}/committee-decision (API-S7-002) in the yaml through RWB-S7-E6019-CON. |
| CDC-19108 | RWB-S7-E6020-APP | CG-ALL-11028 | 12.1 | Publish POST /write-offs/{writeOffId}/committee-decision (API-S7-002) in rwb-writeoff.yaml through RWB-S7-E6020-CON. |
| CDC-19122 | RWB-S7-E6020-CON | CG-ALL-11040 | 12.1 | Publish POST /write-offs/{writeOffId}/committee-decision (API-S7-002) under base /api/recovery/writeoff/v1 as declared in section 12.1. |
| CDC-19127 | RWB-S7-E6020-CON | DOR-RWB-S7-E6020-CON-8 | 12.2 | Publish the committee-decision path in rwb-writeoff.yaml and declare REST bases /api/recovery/case/v1 and /api/recovery/decision/v1. |

### Epic design record (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18896 | RWB-S7-E6013-APP | DOR-RWB-S7-E6013-APP-14 | find it | Record the signed epic design sign-off for RWB-S7-E6013-APP; no signed epic design is recorded in the story or the source documents. |
| CDC-18919 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-14 | Header | Record the signed sign-off of the epic design for RWB-SVC-S7 in the epic design record. |
| CDC-18933 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-14 | header | Record the signed sign-off of the epic design for service epic RWB-SVC-S7 (business epic EP06) |
| CDC-18950 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-14 | header | Record the signed epic design sign-off for RWB-S7-E6015-APP in the epic design record. |
| CDC-18973 | RWB-S7-E6015-CON | DOR-RWB-S7-E6015-CON-14 | none | Record the signed epic design sign-off; the story and source documents hold no signed epic design. |
| CDC-18987 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-14 |  | Record the signed epic design sign-off for this story |
| CDC-19004 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-14 |  | Record the signed epic design sign-off, then confirm it against this story. |
| CDC-19021 | RWB-S7-E6017-APP | DOR-RWB-S7-E6017-APP-14 | header | Confirm and record the signed epic design sign-off; the story cannot state a sign-off the sources do not contain. |
| CDC-19039 | RWB-S7-E6017-CON | DOR-RWB-S7-E6017-CON-14 | none | Confirm and record the signed epic design sign-off for RWB-S7-E6017-CON. |
| CDC-19073 | RWB-S7-E6018-CON | DOR-RWB-S7-E6018-CON-14 | header | Record the signed epic design sign-off that DoR item 14 relies on. |
| CDC-19085 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-14 |  | Record the signed epic design sign-off for RWB-SVC-S7. |
| CDC-19101 | RWB-S7-E6019-CON | DOR-RWB-S7-E6019-CON-14 | n/a | Record the signed epic design sign-off; no sign-off is in this story or the source documents. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18899 | RWB-S7-E6013-APP | DOR-RWB-S7-E6013-APP-8 | 12.5 | Add activity runMonthlyScan on task queue rwb-writeoff under WriteOffWorkflow; the story task queue and the workflow ID placeholder are fixed in this story. |
| CDC-18902 | RWB-S7-E6013-APP | CG-ALL-10840 | 12.5 | Add activity runMonthlyScan on task queue rwb-writeoff, or name the catalogued activity the story should use. |
| CDC-18925 | RWB-S7-E6014-APP | CG-ALL-10863 | 12.5 | Add activity evaluateTaxCriteria on task queue rwb-writeoff. |
| CDC-18994 | RWB-S7-E6016-APP | CG-ALL-10922 | 12.5 | Add activity removeCaseFromPopulation on task queue rwb-writeoff, or name a catalogued activity that performs the removal step. |
| CDC-19007 | RWB-S7-E6016-CON | CG-ALL-10935 | 12.5 | Add activity removeCaseFromPopulation with task queue rwb-writeoff to the Activities sheet. |
| CDC-19027 | RWB-S7-E6017-APP | CG-ALL-10950 | 12.5 | Add activity routePackToCommittee on task queue rwb-writeoff, or name the catalogued activity that performs this step. |
| CDC-19041 | RWB-S7-E6017-CON | CG-ALL-10964 | 12.5 | Add activity routePackToCommittee to the Activities sheet with task queue rwb-writeoff, or name a catalogued activity instead. |
| CDC-19072 | RWB-S7-E6018-CON | CG-ALL-10994 | 12.5 | ApprovalWorkflow row marked as not in Temporal Catalog v1; the story no longer claims it is catalogued. |
| CDC-19075 | RWB-S7-E6018-CON | CG-ALL-10993 | 12.5 | Add activity approveWriteOffInLimit on task queue rwb-writeoff to the Activities sheet, or name a catalogued activity |
| CDC-19092 | RWB-S7-E6019-APP | CG-ALL-11009 | 12.5 | Add activity recordCommitteeDecision to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-19116 | RWB-S7-E6020-APP | CG-ALL-11034 |  | Add the activity recordCommitteeDeferral to the Activities sheet, or name the catalogued activity to use. Owner: Solution architect. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18904 | RWB-S7-E6013-APP | DOR-RWB-S7-E6013-APP-6 | 10 | Add role SY-DATALOAD (service identity, Write-off and posting R) to Users Roles and Permissions v5 |
| CDC-18938 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-1 | 1 | Add 'tech lead' as a role name or code in Users Roles and Permissions v5, or the story role must be a listed role. |
| CDC-18961 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-6 | 10 | Add role SY-DATALOAD, or confirm it is not issued and remove it from section 10 of RWB-S7-E6015-APP. |
| CDC-18997 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-6 | 10 | Add role SY-DATALOAD to the role list |
| CDC-19008 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-1 | 1 | Add 'tech lead' as a role name, or name the existing role code that this story's role maps to. |
| CDC-19042 | RWB-S7-E6017-CON | DOR-RWB-S7-E6017-CON-1 | 1 | Add a role entry for 'tech lead' or confirm the role code or name the story uses for it. |
| CDC-19076 | RWB-S7-E6018-CON | DOR-RWB-S7-E6018-CON-1 | 1 | Register 'tech lead' as a role code or role name, or confirm the existing role code that section 1 should use |
| CDC-19095 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-6 | 10 | Add role SY-DATALOAD, listed in section 10 with Write-off and posting R or U as the matrix gives it. |
| CDC-19104 | RWB-S7-E6019-CON | DOR-RWB-S7-E6019-CON-1 | 1 | Add 'tech lead' as a role code or role name, or name the listed role used for rwb-writeoff. |
| CDC-19119 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-6 | 10 | Add role SY-DATALOAD to the role list, or remove it from the Authority row of RWB-S7-E6020-APP section 10. Story side: rwb-access authorise check stated. |
| CDC-19129 | RWB-S7-E6020-CON | DOR-RWB-S7-E6020-CON-1 | 1 | Add 'tech lead' as a role code or role name, or confirm the v5 role that §1 and §10 should cite. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18923 | RWB-S7-E6014-APP | CG-ALL-10856 | multiple | Record tax_criteria_version as the version of the rwb-decision WO package with owner P7, or give it a dictionary name; its table and owner are Not specified (GAP-3018). |
| CDC-18924 | RWB-S7-E6014-APP | CG-ALL-10857 | 12.7 | Record decision_record as a PLT library object created in rwb_writeoff by the library's own migration (DP-03). |
| CDC-19006 | RWB-S7-E6016-CON | CG-ALL-10928 | 8 | Record removal_reason in LDM v9 Fields as the free-text reason of the removal element, or record it as a non-table object; the story names no column (ASM-5030). |
| CDC-19015 | RWB-S7-E6016-CON | GAP-1810 | find it | Hold removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records and fix their physical names with the DB story. |
| CDC-19025 | RWB-S7-E6017-APP | CG-ALL-10941 | 4 | Name provision_carried in LDM v9 Fields, or record the flag or index that carries it in the owning document; the story keeps the name. |
| CDC-19026 | RWB-S7-E6017-APP | CG-ALL-10942 | 11 | Record decision_record as the PLT library table created in rwb_writeoff, as §12.7 states, in LDM v9 or Data Classification v5. |
| CDC-19065 | RWB-S7-E6018-APP | GAP-1810 |  | Hold removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records, with their physical names fixed. |
| CDC-19079 | RWB-S7-E6018-CON | GAP-1810 |  | Add removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records; fix physical names with the DB story |
| CDC-19121 | RWB-S7-E6020-APP | GAP-1810 | 11 | Hold removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records and fix their physical names in the DB story. |
| CDC-19131 | RWB-S7-E6020-CON | GAP-1810 | 8 | Hold removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records; fix physical names with the DB story. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18910 | RWB-S7-E6013-CON | CG-ALL-10849 | 12.5 | Add a row for activity runMonthlyScan on task queue rwb-writeoff, or name a catalogued activity in §12.5. |
| CDC-18937 | RWB-S7-E6014-CON | CG-ALL-10874 | 12.5 | Add activity evaluateTaxCriteria on task queue rwb-writeoff, or name a catalogued activity for this story. |
| CDC-18976 | RWB-S7-E6015-CON | CG-ALL-10908 | 12.5 | Add an Activities row for prepareWriteOffPack on task queue rwb-writeoff. |
| CDC-19059 | RWB-S7-E6018-APP | CG-ALL-10980 | 12.5 | Add activity approveWriteOffInLimit on task queue rwb-writeoff to the Activities sheet, or name a catalogued activity instead. |
| CDC-19103 | RWB-S7-E6019-CON | CG-ALL-11021 | 12.5 | Add an Activities row for recordCommitteeDecision on task queue rwb-writeoff, or name the catalogued activity used instead. |
| CDC-19128 | RWB-S7-E6020-CON | CG-ALL-11046 | 12.5 | Add an activity row for recordCommitteeDeferral on task queue rwb-writeoff, or name a catalogued activity in §12.5 instead. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18949 | RWB-S7-E6015-APP | CG-ALL-10888 | 13 | Create the story file for RWB-P7-E1073-CON, or name the existing story that carries the rwb-decision kit capability. |
| CDC-18951 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-17 | Metadata; 13 | Create the story file for RWB-P7-E1073-CON, or name the existing story that carries the rwb-decision kit capability. |
| CDC-18972 | RWB-S7-E6015-CON | CG-ALL-10905 | 13 | Create RWB-P7-E1073-CON, or name the existing story that carries the Drools kit row. |
| CDC-19100 | RWB-S7-E6019-CON | CG-ALL-11018 | 13 | Create RWB-P7-E1073-CON or name the existing story for the Drools kit row. |
| CDC-19125 | RWB-S7-E6020-CON | CG-ALL-11043 | 13 | Create story RWB-P7-E1073-CON or name the existing story for the same capability. |

### RWB-S7-E6017-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18905 | RWB-S7-E6013-APP | GAP-3025 | not in this story | Keep H, C, I, X rows; record rwb-case, rwb-deviation, rwb-decision as class C with placeholders; track RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element as dependencies; state no REST operation and placeholder SCR-27 read; record decision_log_id meaning; land freshness fact; add requirement row at next revision |
| CDC-19032 | RWB-S7-E6017-APP | GAP-3025 |  | Keep the H, C, I and X rows; record rwb-case, rwb-deviation and rwb-decision as class C in fact; track RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and the meeting calendar as dependencies; add a routing requirement row. |
| CDC-19048 | RWB-S7-E6017-CON | GAP-3025 | find it | Record rwb-case, rwb-deviation and rwb-decision as class C rows with placeholders; track RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and the meeting calendar as dependencies; add a routing-step requirement row at the next programme revision. |
| CDC-19062 | RWB-S7-E6018-APP | GAP-3025 |  | Record rwb-case, rwb-deviation and rwb-decision rows as class C with placeholders; add RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-TE006-CON and a meeting-calendar element as tracked dependencies; add routing requirement row. |

### RWB-S7-E6013-APP (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18908 | RWB-S7-E6013-APP | GAP-3016 | 12.5 | Add plan rows for the four consumed contracts as class C in fact with placeholders; add RWB-PLT-E1072-CON with RWB-P7-E1073-CON, RWB-PLT-TE006-CON and RWB-PLT-E1071-CON; declare JOB-16 Schedule and ACE data-ready trigger without registering them; add DP-04, DP-05, DP-09 rows per the owners' decision. |
| CDC-18911 | RWB-S7-E6013-CON | DOR-RWB-S7-E6013-CON-10 | find it | Add empty, loading, error and no-access states for SCR-27. This contract story has no screen. |
| CDC-18913 | RWB-S7-E6013-CON | GAP-3016 |  | Add plan rows for the four consumed contracts, DP-04, DP-05, DP-09 and DP-10 with the named rule kit, outbox and inbox library and Scheduled job kit; declare JOB-16 and the ACE data-ready trigger; publish the write-off state list of values before the DB story |
| CDC-18929 | RWB-S7-E6014-APP | GAP-3016 | find it | Add plan rows for rwb-case, rwb-source-data and rwb-decision (class C), RWB-PLT-E1072-CON with RWB-P7-E1073-CON, RWB-PLT-TE006-CON and RWB-PLT-E1071-CON; keep H, C, I and X rows as they stand. |

### RWB-S7-E6015-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18915 | RWB-S7-E6013-CON | GAP-3022 |  | Publish baseline: seven operation names, pack element with the five R-WO-05 elements and write-off read, event identity, field-level types, and error bindings to section 14 message IDs |
| CDC-18952 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-21 | n/a | Set build status to Done once the contract is published. |
| CDC-18953 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-22 | n/a | Record the published contract fake library version. |
| CDC-18965 | RWB-S7-E6015-APP | GAP-3022 | find it | Publish baseline with placeholders, message id per error, pack element with five R-WO-05 elements, sibling attributions, confirmed names and tag date in README. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18927 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-11 | 11 | Confirm the personal-data class of the case and write_off fields this story carries; the story now states that the class comes from Data Classification v5. |
| CDC-18940 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-11 | 17 | Reconcile the P2 personal-data classing of the fields this story carries with its statement that it carries no personal data (BR10, section 8). |
| CDC-19010 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-11 | 8 | Confirm the personal data class of the fields the detcheck names; this contract carries no personal data (BR8). |
| CDC-19118 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-11 |  | Reclassify the fields carried by RWB-S7-E6020-APP so that none is classed as personal data, since the story states none is carried. Owner: Data. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18979 | RWB-S7-E6015-CON | GAP-1795 |  | Publish under /api/recovery/writeoff/v1 the write-off read, the proposal create and the committee pack submit with x-module S7; keep the two existing paths |
| CDC-19029 | RWB-S7-E6017-APP | GAP-1795 | 13 | Publish the read of a write-off, the proposal creation and the committee submission under /api/recovery/writeoff/v1 with x-module S7, add them to the Ownership Map endpoints sheet and to API Specification v4, and keep the two existing paths unchanged. |
| CDC-19045 | RWB-S7-E6017-CON | GAP-1795 | find it | Publish under /api/recovery/writeoff/v1 the write-off read, the proposal creation and the committee submit operations (slide 20: GET/POST /write-offs, POST /write-offs/{id}/submit) with x-module S7, and add them to both documents; the two existing paths keep their paths. |
| CDC-19061 | RWB-S7-E6018-APP | GAP-1795 |  | Publish read, proposal create and pack submit operations under /api/recovery/writeoff/v1; add them to the Ownership Map endpoints and the API specification; keep the two existing paths. |

### RWB-S7-E6017-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19022 | RWB-S7-E6017-APP | DOR-RWB-S7-E6017-APP-21 | header | Set the build status to Done once the contract is published. |
| CDC-19023 | RWB-S7-E6017-APP | DOR-RWB-S7-E6017-APP-22 | header | Publish the contract fake and record its library version against RWB-S7-E6017-CON. |
| CDC-19030 | RWB-S7-E6017-APP | GAP-0738 |  | Publish the case-side routing operation in RWB-S7-E6017-CON; add the committee queue row and the committee-meeting timer type to rwb-case reference data as rows; the meeting date stays a CaseWorkflow durable timer. |
| CDC-19031 | RWB-S7-E6017-APP | GAP-3026 |  | Publish the baseline with its placeholders; bind each error condition to one section 14 message id; publish the queue and deviation elements, the complete 27-state list and the meeting-booking attribute; confirm operation names with the owners. |

### RWB-S7-E6013-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18897 | RWB-S7-E6013-APP | DOR-RWB-S7-E6013-APP-21 | find it | Publish the contract and set its build status to Done; it is currently Not started. |
| CDC-18898 | RWB-S7-E6013-APP | DOR-RWB-S7-E6013-APP-22 | find it | Publish the contract fake and record its library version; no fake version is recorded as published. |
| CDC-18909 | RWB-S7-E6013-APP | GAP-3017 | 12.5 | Publish the baseline with the placeholders for the rwb-case, rwb-source-data and rwb-decision operations; bind each error to one section 14 message ID; declare the case boundary as the child workflow input, signals and stage outcome; confirm the four operation names and two event names with owners; settle the scan table and list of values; record the tag date in the README. |

### RWB-S7-E6014-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18920 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-21 | Header | Move the build status of RWB-S7-E6014-CON from Not started to Done. |
| CDC-18921 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-22 | Header | Publish a fake library version for the contract and record it as published. |
| CDC-18930 | RWB-S7-E6014-APP | GAP-3019 | 12.2 | Publish the working read of ASM-B2-S7-002-1 to ASM-B2-S7-002-6: POST /write-off-scans element, properties and required set, tax criteria version as package fact, remittance as update, Idempotency-Key. |

### RWB-S7-E6016-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18988 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-21 |  | Move build status from Not started to Done |
| CDC-18989 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-22 |  | Record the published contract fake library version; not specified in the source documents |
| CDC-18999 | RWB-S7-E6016-APP | GAP-3024 | 11, 12, 13 | Publish the removal operation with placeholder path and element names, bind errors to section 14 message ids, and record the tag date in the README |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18990 | RWB-S7-E6016-APP | DOR-RWB-S7-E6016-APP-8 | 12.1 | Add POST /write-offs/{writeOffId}/removal to rwb-writeoff.yaml; add bases /api/recovery/case/v1 and /api/recovery/decision/v1; reconcile WriteOffWorkflow task queue rwb-writeoff in namespace rwb-recovery with the catalog row. |
| CDC-19088 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-8 | 8 | Add POST /write-offs/{writeOffId}/committee-decision (API-S7-002) to rwb-writeoff.yaml; add bases /api/recovery/case/v1 and /api/recovery/decision/v1; align WriteOffWorkflow task queue and namespace rwb-recovery with the catalog. |
| CDC-19114 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-8 |  | Add POST /write-offs/{writeOffId}/committee-decision and the bases /api/recovery/case/v1 and /api/recovery/decision/v1 to the API yaml; align the WriteOffWorkflow task queue rwb-writeoff in namespace rwb-recovery with the catalog. |

### RWB-S7-E6016-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19009 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-10 | 1 | Add the empty, loading, error and no-access states of SCR-27 to the app story RWB-S7-E6016-APP. |
| CDC-19013 | RWB-S7-E6016-CON | GAP-3023 | find it | Keep the H, C, I and X rows; record rwb-case and rwb-decision as class C rows with placeholders; add RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON as the rows the stage needs; add the requirement id. |
| CDC-19033 | RWB-S7-E6017-APP | GAP-3023 |  | Add the removal operation with placeholder path, removal_reason as validated free text stored in the decision record, class C rows and a requirement id; R-WO-06 hold stays with RWB-S7-E6017-APP. |

### RWB-S7-E6021-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18906 | RWB-S7-E6013-APP | GAP-3033 | not in this story | Record four consumed rows as class C without changing H; treat DP-05 as consumed on rwb-source-data contract; keep ALS/GL crossing, re-post and provision release with RWB-ITG-E6021-ITG; read R-WO-05 as the assertion of pack RWB-S7-E6015-APP; add REQ-S7-002 and REQ-S7-005 to traceability at D1 |
| CDC-19063 | RWB-S7-E6018-APP | GAP-3033 |  | Record four consumed rows as class C; treat DP-05 as consumed on rwb-source-data contract; keep ALS and GL crossing with RWB-ITG-E6021-ITG; add REQ-S7-002 and REQ-S7-005 to both stories at D1. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18907 | RWB-S7-E6013-APP | GAP-1794 | 11 | State the four entity groups of rwb_writeoff with key fields, fix write_off as the one table the map holds, write remaining tables with the S7 DB story, add missing Ownership Map rows in the same change |
| CDC-18912 | RWB-S7-E6013-CON | GAP-1794 | 12.7 | State the four rwb-writeoff entity groups with key fields, fix write_off as the physical table, add the remaining S7 table rows to the Ownership Map and the LDM |

### RWB-S7-E6018-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19014 | RWB-S7-E6016-CON | GAP-3027 | find it | Keep the H, C, I and X rows; record the five consumed rows as class C rows with placeholders; add the DP-06, DP-07, DP-08 and DP-09 pattern rows; add the requirement id. |
| CDC-19034 | RWB-S7-E6017-APP | GAP-3027 |  | Keep the H, C, I and X rows; read delegation_limit on the rwb-case contract; record approver and limit in the local decision record; raise R-WO-13 and R-WO-14; claim EV-24 for the approved path. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml; API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19074 | RWB-S7-E6018-CON | DOR-RWB-S7-E6018-CON-8 |  | Add POST /write-offs/{writeOffId}/committee-decision (API-S7-002) to rwb-writeoff.yaml; add the bases /api/recovery/case/v1, /api/recovery/decision/v1 and /api/recovery/access/v1 and the four more listed to the API Specification v5 yaml |
| CDC-19102 | RWB-S7-E6019-CON | DOR-RWB-S7-E6019-CON-8 | 12.5 | Publish the committee-decision path and declare the REST bases of /api/recovery/case/v1 and /api/recovery/decision/v1. |

### RWB-S7-E6019-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19086 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-21 |  | Set build status to Done once the contract is published. |
| CDC-19087 | RWB-S7-E6019-APP | DOR-RWB-S7-E6019-APP-22 |  | Record the published contract fake library version. |

### Epic design record; OTHER:RWB-SVC-S7) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19111 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-14 | header | Record the signed epic design sign-off; none is in the story or source documents. |
| CDC-19126 | RWB-S7-E6020-CON | DOR-RWB-S7-E6020-CON-14 | header | Record the signed epic design sign-off for EP06 and RWB-SVC-S7. |

### RWB-S7-E6020-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19112 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-21 | header | Move the build status from Not started to Done so the contract is published. |
| CDC-19113 | RWB-S7-E6020-APP | DOR-RWB-S7-E6020-APP-22 | header | Record the published contract fake library version. |

### OTHER:Contract README for rwb-writeoff; OTHER:TSD S7 T-A.1; OTHER:T-A.2 and T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18914 | RWB-S7-E6013-CON | GAP-3017 | 12.5 | Publish baseline with placeholders; bind error conditions to section 14 message IDs; confirm the four operation names and two event names with owners; settle scan table and list of values; record tag date in README |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18922 | RWB-S7-E6014-APP | DOR-RWB-S7-E6014-APP-8 | 12.2; 12.5 | Add the /api/recovery/case/v1 and /api/recovery/decision/v1 bases to the API yaml; confirm the WriteOffWorkflow task queue rwb-writeoff in namespace rwb-recovery against the catalog row. |

### OTHER:P7 rwb-decision (WO package and tax_criteria_version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18935 | RWB-S7-E6014-CON | GAP-1469 | 8 | Hold both tracks and the tax criteria as one versioned rule package with its test cases; name the tracks in the version label; the scan reports the version applied. |

### OTHER:P7 rwb-decision (owner of tax_criteria_version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18936 | RWB-S7-E6014-CON | CG-ALL-10868 | 8 | Record tax_criteria_version as a named object (field, library table or flag) with its home and key; no field of that name is in LDM v9 or Data Classification v5. |

### RWB-S7-E6014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18939 | RWB-S7-E6014-CON | DOR-RWB-S7-E6014-CON-10 | 1 | Add empty, loading, error and no-access states to SCR-27. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (Solution architect) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18958 | RWB-S7-E6015-APP | CG-ALL-10891 | 12.5 | Add activity prepareWriteOffPack on queue rwb-writeoff. |

### OTHER:Screen specification for SCR-27 (CG-ALL-10896) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18960 | RWB-S7-E6015-APP | DOR-RWB-S7-E6015-APP-10 | 13 | WriteOffPack names empty, loading, error and no-access states; their source is not in the screen specification |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18962 | RWB-S7-E6015-APP | GAP-1795 | find it | Publish GET and POST /write-offs and POST /write-offs/{id}/submit under /api/recovery/writeoff/v1 with x-module S7; keep the two existing paths. |

### RWB-S7-E6021-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18963 | RWB-S7-E6015-APP | GAP-3033 | find it | Record the four consumed rows as class C, treat DP-05 as consumed on rwb-source-data, keep ALS, GL, re-post and provision release with RWB-ITG-E6021-ITG. |

### RWB-S7-E6015-APP; OTHER:TSD S7 T8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18964 | RWB-S7-E6015-APP | GAP-3021 | header | Contract dependencies row lists three C rows; RWB-P7-E1073-CON removed because its story does not exist (CG-ALL-10888) |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:S7 row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18980 | RWB-S7-E6015-CON | GAP-1797 | 11 | Add a P5 cell and its call type for the pack document and its retention class, with the P5 owner |

### RWB-S7-E6015-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18981 | RWB-S7-E6015-CON | GAP-3021 |  | Record the seven consumed rows as class C in fact, C rows RWB-P10-TE013-CON, RWB-PLT-TE006-CON, RWB-PLT-E1072-CON and RWB-P7-E1073-CON; adopt REQ-S7-002 and correct TSD T8 |

### OTHER:TSD S7 T-A.2 and T3.1, and the contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18982 | RWB-S7-E6015-CON | GAP-3022 |  | Bind each error to a section 14 message id, declare the pack element properties, attribute the sibling operations, confirm the seven operation names and record the tag date |

### OTHER:Recovery Workbench FSD S7 field catalog; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19000 | RWB-S7-E6016-APP | GAP-1810 | find it | Hold removal_reason, review_date, decision_reason and pack_document_id as required fields of the committee and eligibility records; fix their physical names with the DB story. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19012 | RWB-S7-E6016-CON | DOR-RWB-S7-E6016-CON-20 | 12.7 | Add a key for each parameter this story reads, and name the reference-data contract (DP-06, DP-07) in the story. |

### OTHER:SCR-27 fragment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19043 | RWB-S7-E6017-CON | DOR-RWB-S7-E6017-CON-10 | find it | Add empty, loading, error and no-access states to SCR-27. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19046 | RWB-S7-E6017-CON | GAP-0738 | find it | Serve the case side of the routing answer as one operation of RWB-S7-E6017-CON; add the committee queue row and the committee-meeting timer type as reference rows; register no Schedule, JOB-16 stays in rwb-writeoff. |

### OTHER:Recovery Workbench TSD S7 (T4; OTHER:T-A.1; OTHER:T-A.2) and the rwb-case, rwb-deviation and rwb-decision contract owners (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19047 | RWB-S7-E6017-CON | GAP-3026 | find it | Publish the baseline with placeholders, bind each error condition to a section 14 message id, publish the complete 27-state list, queue and deviation elements, and confirm operation names before the baseline is tagged. |

### RWB-S7-E6025-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19049 | RWB-S7-E6017-CON | GAP-3042 | find it | Publish the case and timer operation names, the placement element, the two closure state values, the closing-entry element and the retention and class reference data; bind each error condition to a section 14 message id. |

### RWB-S7-E6023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19050 | RWB-S7-E6017-CON | GAP-3038 | find it | Publish the reconciliation operation, the result element, the posting-product name and the matching cross-reference, confirmed with the rwb-source-data owner before tagging; declare the four consumed rows as class C dependencies. |

### RWB-S7-E6018-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19057 | RWB-S7-E6018-APP | DOR-RWB-S7-E6018-APP-21 | header | Set build status to Done once the contract is published. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19064 | RWB-S7-E6018-APP | GAP-3037 |  | Fix posting product and event on the rwb-source-data contract; publish the matching cross-reference; hold three consumed rows as class C; trace to REQ-S7-005 placeholder. |

### OTHER:TSD S7 (T-A.1; OTHER:T-A.2; OTHER:T3.1; OTHER:T3.2; OTHER:T5.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19066 | RWB-S7-E6018-APP | GAP-3028 |  | Publish API-S7-001 and API-S7-002 property lists with placeholders; bind each error (401, 403, 404, 409, 422, 503) to one section 14 message id; publish delegation_limit as a consumed reference-data element and event element rwb.writeoff.WriteOffApproved.v1 on rwb.writeoff.events.v1; confirm with solution architect before tag. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19077 | RWB-S7-E6018-CON | GAP-1795 |  | Publish under /api/recovery/writeoff/v1 the read, create-proposal and submit-pack operations; add them to the Ownership Map and the API specification in the same change; the two existing paths unchanged |

### OTHER:TSD S7 T-A.1; OTHER:T-A.2; OTHER:T3.1 and T5.3; OTHER:rwb-writeoff contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19078 | RWB-S7-E6018-CON | CG-ALL-3425 |  | Publish the baseline: bind every error to a section 14 message id, declare the five R-WO-05 pack elements and write-off shape, confirm the seven operation names with owners, record the tag date in the README |

### OTHER:TSD S7 T-A.1; OTHER:T3.1 and T5.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19080 | RWB-S7-E6018-CON | GAP-3028 |  | Publish the element baseline with placeholders; bind errors to section 14 message ids; declare the delegation element as consumed reference data and the event element as rwb.writeoff.WriteOffApproved.v1; confirm with the solution architect before tag |

### RWB-S7-E6019-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19105 | RWB-S7-E6019-CON | DOR-RWB-S7-E6019-CON-10 | find it | Declare the empty, loading, error and no-access states of SCR-27. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0455 | The committee routing harness pack, the committee queue code and the committee meeting calendar are not specified | Integration lead | Resolved (directive) |
| GAP-0738 | The committee routing of RWB-E6-017 crosses two services with no operation, no committee queue code, no meeting timer type and no requirement ID in the sources | Solution architect | Resolved (directive) |
| GAP-1469 | The write-off tax criteria and the meaning of the two tracks are not specified | Write-off committee member | Resolved (directive) |
| GAP-1792 | The FSD reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them | Solution architect | Resolved (directive) |
| GAP-1794 | The Ownership Map lists one table for rwb-writeoff, while Architecture v5 gives the schema four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1795 | Slide 20 names write-off collection operations that neither the Ownership Map nor the API specification holds | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1797 | The committee pack is a document in the document hub, and the matrix connects S7 to P5 on no path | Solution architect with the P5 owner | Resolved (directive) |
| GAP-1800 | The FSD routing rules move the case through twenty states, while Architecture v5 gives the case state to rwb-case | Solution architect with the P3 owner | Resolved (directive) |
| GAP-1801 | The sources disagree on what starts the monthly scan: a Schedule, the ACE batch, or Quartz | Solution architect | Resolved (directive) |
| GAP-1802 | The fifty-one write-off rules exist but their package has no owner and no version in force | Center of excellence analyst with P7 | Resolved (directive) |
| GAP-1803 | No source states the write-off tax criteria, the meaning of the two tracks, or the criteria version in force | Write-off committee member | Resolved (directive) |
| GAP-1810 | The rules require a removal reason, a review date and a pack reference that no field of the module holds | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1811 | The pack is prepared by the write-off agent, and the matrix gives S7 no path to the agent service | Solution architect with the P10 owner | Resolved (directive) |
| GAP-1814 | The write-off proposal screen has no stated owner and no stated route through the gateway | Solution architect | Resolved (directive) |
| GAP-2018 | Strict-mode wait at a point of no return is not defined in this design | Service owner P7 rwb-decision with the saga owners S2, S5, S6 and S7 | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3017 | RWB-S7-E6013-CON: the consumed operation names, the case boundary element, the event names, the schedule parameters and the list of values of rwb-writeoff have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3019 | The scan element, its required set, the tax-criteria result shape and the remittance element have no published field list | Solution architect with the rwb-writeoff tech lead and the P3 and P7 owners | Resolved (directive) |
| GAP-3021 | RWB-S7-E6015-APP: the pack slice has no plan row for its seven consumed contracts, its agent, outbox and rule-kit dependencies, its pack columns, its requirement id or its screen read | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3022 | RWB-S7-E6015-CON: the pack element, the seven consumed operation names, the write-off read, the event identity and the field-level types have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3023 | RWB-S7-E6016-APP: the removal slice has no published operation, no field or list for the removal reason, no plan row for its three consumed contracts, and no requirement id | Solution architect | Resolved (directive) |
| GAP-3024 | RWB-S7-E6016-CON: the removal operation, its element names, the reason field and the three consumed operation names have no published baseline | Solution architect | Resolved (directive) |
| GAP-3025 | RWB-S7-E6017-APP: the routing slice has no plan row for its five consumed contracts, its rule kit, its event library, its meeting calendar, the operation it provides or the requirement it serves | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3026 | RWB-S7-E6017-CON: the consumed operation names, the queue and deviation elements, the unprinted state values and the meeting-booking element have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3027 | RWB-S7-E6018-APP: the delegation table and its owner, the approver and the limit applied have no column, the credit committee outcome is claimed by no story, and the plan's C row is empty while five rows are consumed | Solution architect | Resolved (directive) |
| GAP-3028 | RWB-S7-E6018-CON: the delegation element, the answer element and the five consumed operation names have no published baseline, and the credit committee outcome is declared nowhere | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3033 | RWB-S7-E6021-APP: the plan holds no C or X row for the four consumed contracts of the pack-prepared step, no dependency row for DP-05, no interface for the ALS and general-ledger crossing, and no separate story for the shared pack rule R-WO-05 | Solution architect with the rwb-writeoff tech lead, the rwb-source-data, rwb-case and rwb-decision owners and the wave 4 integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3038 | RWB-S7-E6023-CON: the reconciliation baseline has no published operation, element, posting-product name, matching cross-reference or completeness element, and its consumed rows have no plan row | Solution architect | Resolved (directive) |
| GAP-3042 | RWB-S7-E6025-CON: the consumed operation names, the placement element, the retention period and class, the closing amounts and the two unprinted rule rows have no published baseline | Solution architect | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC4 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC5 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC6 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC7 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC8 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC9 is new and no section 16 row covers it |
| RWB-S7-E6013-APP | new AC without TC row | 489 | AC10 is new and no section 16 row covers it |
| RWB-S7-E6017-APP | skipped AC ID | 123 | missing: AC5, AC6 |
