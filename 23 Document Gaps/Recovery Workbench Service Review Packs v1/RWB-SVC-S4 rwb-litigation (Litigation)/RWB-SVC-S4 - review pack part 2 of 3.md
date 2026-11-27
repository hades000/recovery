# RWB-SVC-S4 rwb-litigation (Litigation) - review pack, part 2 of 3 (RWB-S4-E5007-CON to RWB-S4-E5016-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 18 |
| Resolved in the stories | 375 |
| Cross-document (pending in another document) | 238 |
| Not applied (value not in the sources) | 15 |
| Open business decisions | 51 |
| Register gaps linked | 47 |
| Unconfirmed assumptions | 0 |
| Lint findings | 13 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S4-E5007-CON | 15 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5007 CON Verify the pack and approve filing - contract v2.md |
| RWB-S4-E5008-APP | 26 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5008 APP Select the law firm from the panel v2.md |
| RWB-S4-E5008-CON | 17 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5008 CON Select the law firm from the panel - contract v2.md |
| RWB-S4-E5009-APP | 27 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5009 APP Instruct the firm through the portal v2.md |
| RWB-S4-E5009-CON | 14 | 15 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5009 CON Instruct the firm through the portal - contract v2.md |
| RWB-S4-E5010-APP | 25 | 17 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5010 APP Record the court filing and receipt v2.md |
| RWB-S4-E5010-CON | 22 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5010 CON Record the court filing and receipt - contract v2.md |
| RWB-S4-E5011-APP | 29 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5011 APP Track hearings, deadlines and fees v2.md |
| RWB-S4-E5011-CON | 17 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5011 CON Track hearings, deadlines and fees - contract v2.md |
| RWB-S4-E5012-APP | 26 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5012 APP Recommend the next litigation step v2.md |
| RWB-S4-E5012-CON | 17 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5012 CON Recommend the next litigation step - contract v2.md |
| RWB-S4-E5013-APP | 28 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5013 APP Settle before judgment v2.md |
| RWB-S4-E5013-CON | 15 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5013 CON Settle before judgment - contract v2.md |
| RWB-S4-E5014-APP | 20 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5014 APP Decide and manage an appeal v2.md |
| RWB-S4-E5014-CON | 8 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5014 CON Decide and manage an appeal - contract v2.md |
| RWB-S4-E5015-APP | 25 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5015 APP Pay court fees and legal expenses v2.md |
| RWB-S4-E5015-CON | 16 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5015 CON Pay court fees and legal expenses - contract v2.md |
| RWB-S4-E5016-APP | 28 | 9 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5016 APP Record the judgment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S4-E5010-APP | R-02326 | CG-ALL-9212 | Script gap | Product owner | The story adds FILING_REJECTED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5010-CON | R-02328 | CG-ALL-9229 | Script gap | Product owner | The story adds FILING_REJECTED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5013-APP | R-02352 | CG-ALL-9301 | Script gap | Product owner | The story adds LITIGATION_HELD to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5013-APP | R-02353 | CG-ALL-9302 | Script gap | Product owner | The story adds SETTLEMENT_OFFERED_AT_COURT to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-APP | R-02359 | CG-ALL-9325 | Script gap | Product owner | The story adds JUDGMENT_DISMISSED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-APP | R-02360 | CG-ALL-9326 | Script gap | Product owner | The story adds APPEAL_DECISION to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-APP | R-02361 | CG-ALL-9327 | Script gap | Product owner | The story adds APPEAL_FILED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-APP | R-02362 | CG-ALL-9328 | Script gap | Product owner | The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-APP | R-02363 | CG-ALL-9329 | Script gap | Product owner | The story adds TO_WRITE_OFF to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-CON | R-02364 | CG-ALL-9344 | Script gap | Product owner | The story adds JUDGMENT_DISMISSED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-CON | R-02365 | CG-ALL-9345 | Script gap | Product owner | The story adds APPEAL_DECISION to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-CON | R-02366 | CG-ALL-9346 | Script gap | Product owner | The story adds APPEAL_FILED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-CON | R-02367 | CG-ALL-9347 | Script gap | Product owner | The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5014-CON | R-02368 | CG-ALL-9348 | Script gap | Product owner | The story adds TO_WRITE_OFF to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-APP | R-02369 | CG-ALL-9355 | Script gap | Product owner | The story adds LEGAL_SPEND_APPROVAL to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-APP | R-02370 | CG-ALL-9356 | Script gap | Product owner | The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-CON | R-02376 | CG-ALL-9372 | Script gap | Product owner | The story adds IN_HEARING to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-CON | R-02377 | CG-ALL-9373 | Script gap | Product owner | The story adds FEE_DUE to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-CON | R-02378 | CG-ALL-9374 | Script gap | Product owner | The story adds LEGAL_SPEND_APPROVAL to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-CON | R-02379 | CG-ALL-9375 | Script gap | Product owner | The story adds FEE_APPROVED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5015-CON | R-02380 | CG-ALL-9376 | Script gap | Product owner | The story adds FEE_REJECTED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5016-APP | R-02386 | CG-ALL-9392 | Script gap | Product owner | The story adds JUDGMENT_RECORDED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5016-APP | R-02387 | CG-ALL-9393 | Script gap | Product owner | The story adds JUDGMENT_DISMISSED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5016-APP, RWB-S4-E5016-CON, RWB-S4-E5020-APP, RWB-S4-E5020-CON, RWB-S5-E4021-APP, RWB-S5-E4021-CON | R-09245 | GAP-1471 | Register gap | Head of Litigation | Enforcement after judgment and the eviction of a held property have no named owner role | Use the enforcement owner role the rules already name for enforcement, with Legal counsel named on an eviction, and record the assignment as an assumption until the operating model names the holder. |
| RWB-S4-E5008-APP | R-12553 | CG-ALL-9170 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5009-APP | R-12561 | CG-ALL-9194 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5010-APP | R-12573 | CG-ALL-9224 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5010-CON | R-12578 | CG-ALL-9237 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5012-APP | R-12594 | CG-ALL-9282 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5013-APP | R-12602 | CG-ALL-9309 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5014-CON | R-12617 | CG-ALL-9351 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5016-APP | R-12633 | CG-ALL-9402 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E5009-ITG, RWB-S4-E5009-APP, RWB-S4-E5009-CON | R-22811 | GAP-2783 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case and S9 rwb-partner architects and the business owner of the partner service levels | The partner clock of 2 working days has no stated home, and the working-day calendar and instruction types have no value in any source | Declare the partner clock as one durable timer of LitigationWorkflow of 2 working days started at instructed_at, measured on a working-day calendar read as a versioned reference row whose content is the placeholder; fire R-LIT-28 on expiry, answer FIRM_BREACHED_SLA to rwb-case with the partner-and-agency-manager task, mark the breach on the P9 contract and leave the re-selection to the firm-selection story; keep the case-stage timer and the task rows with rwb-case. |
| RWB-P10-TE013-CON, RWB-S4-E5012-APP, RWB-S4-E5012-CON | R-22978 | GAP-2793 | Register gap | Solution architect of S4 with the P10 architect and the business owner of S4 | The recommendation, its reasons and its cost and effect have no table, no operation and no vocabulary in any source | The proposal is not a business row: it is a view of the decision record answered on API-S4-003, with the step vocabulary as a versioned reference value, and the cost and effect are read on rwb-agent's contract under DP-20 with the rule as fallback. No sixth operation is added to the five of TSD S4 T-A.1 and the C row stays None until D1 or the plan owner rules otherwise. |
| RWB-S4-E5003-APP, RWB-S4-E5003-CON, RWB-S4-E5010-APP, RWB-S4-E5010-CON, RWB-S4-E5017-APP, RWB-S4-E5017-CON, RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-23420 | GAP-1746 | Register gap | Product Owner | REQ-S4-009 (prescription warnings) has no BRD requirement row, and BR-038 and BR-042 carry no program requirement ID | Carry REQ-S4-009 into this PRD as FR-S4-051 and FR-S4-052 under BR-034, the requirement that owns the statutory clock, and record the gap so the E5 BRD can add the row. Carry BR-038 and BR-042 from the FSD features and the RWB-E5 story keys. Nothing is dropped and no requirement is merged. |
| RWB-S4-E5011-APP, RWB-S4-E5011-CON | R-23440 | GAP-2788 | Register gap | Solution architect, S4 rwb-litigation, with the P8 rwb-payment architect and the business owner of S4 | The fee accrual has no home in rwb-litigation and no named operation on rwb-payment | Keep the legacy sentence unchanged with its origin tag and record the target reading: the accrued fee, its spend deadline, its value date and its approval state are read on rwb-payment's contract (one hop, 2 s, faked, operation name left as the placeholder); this service records the spend decision of R-LIT-41 to R-LIT-43 through its decision record and raises the approved fact, and posts nothing; rwb-payment appears on the contract rows of both stories and the metadata rows stay as the plan gives them. |
| RWB-S4-E5012-APP, RWB-S4-E5012-CON | R-23443 | GAP-2795 | Register gap | Solution architect of S4 with the P5 and P6 architects and the business owner of S4 | The template status of R-LIT-04 and the pack element of R-LIT-16 have no owner field, no identifier and no published operation | The template status is read on rwb-comms' notice contract as part of the notice answer and its field identifier carries the placeholder; the pack index is read on rwb-document's contract with the defect list items and carries the placeholder on its element and operation name. When a fact is absent, the rule does not fire, nothing is written and no move is answered. |
| RWB-S4-E5014-APP, RWB-S4-E5014-CON | R-23447 | GAP-2805 | Register gap | Business analyst and business owner, S4 rwb-litigation | The length of the appeal window and the filing deadline of R-LIT-47 are given by no source read, though both rules turn on them | Publish the appeal window length and the filing deadline as versioned reference rows of the litigation route, with their effective dates and the product groups they apply to, and reference those rows from R-LIT-46 and R-LIT-47; until then both stories read them as reference data at their version in force and carry the placeholder. |
| RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-23448 | GAP-2806 | Register gap | Solution architect, S4 rwb-litigation, with the P8 rwb-payment architect and the business owner of S4 | The fee has no home in rwb-litigation and no named payment operation on rwb-payment | Keep the legacy sentence unchanged with its origin tag and record the target reading: the approved fee is paid and posted against the case by rwb-payment on its contract (one hop, 2 s, faked, operation name left as the placeholder); this service checks the fee, routes it, records the decision and stores the payment reference, and posts nothing; rwb-payment appears on the contract rows of both stories, and the metadata rows stay exactly as the plan gives them. |
| RWB-PLT-E1037-CON, RWB-PLT-E1072-CON, RWB-P4-E1037-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29029 | GAP-2809 | Register gap | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P4 rwb-access and platform library architects and the business owner of S4 | The D7.4 limit, the approval row and the rule-package read carry no value and no dependency row | Declare the approval as the P7 child workflow consumed on queue rwb-decision, the D7.4 limit and the approver's delegation as consumed on the rwb-access authorise contract, and the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43 as consumed from rwb-decision, each with the placeholder on its operation name and ceiling; fix no limit value in code or in the document, and leave the metadata rows as the plan gives them. |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29032 | GAP-2807 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case reference-data owner and the business owner of S4 | The fee schedule has no field list, no owner row and no version in any source | Read the fee schedule, the fee types and the court levels as versioned reference data of rwb-case on its contract, name the read on the contract rows of both stories with the operation name left as the placeholder, carry the schedule version on every decision record, and leave the metadata rows as the plan gives them. |
| RWB-S4-E5016-APP, RWB-S4-E5016-CON | R-29140 | GAP-2814 | Register gap | Solution architect and the business owner of S4 | The FSD S4 and the TSD S4 that the two slices read are In review with an empty sign-off table and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes. |
| RWB-S4-E5009-APP, RWB-S4-E5009-CON | R-38244 | ASM-4617 | Register assumption |  | The partner clock is one durable timer of LitigationWorkflow of 2 working days started at instructed_at on a working-day calendar read as a versioned reference row; on expiry R-LIT-28 fires, the instruction is marked breached on the partner contract, FIRM_BREACHED_SLA is answered to rwb-case with the partner-and-agency-manager task and the re-selection stays with the firm-selection story. The case-stage timer and the task row stay rwb-case's, requested on the stage outcome. | Business owner of the partner service levels with the S4, P3 and S9 solution architects |
| RWB-S4-E5011-APP, RWB-S4-E5011-CON | R-38252 | ASM-4626 | Register assumption |  | The accrued fee, the spend deadline, the value date and the approval state are read on rwb-payment's contract and are never written here. rwb-litigation owns no fee table and no fee column: its only durable effects are the hearing row, the decision record, the workflow timers and the stage answer, and the approved fee is posted by P8. | Solution architect of S4 with the P8 rwb-payment architect and the business owner of S4 |
| RWB-S4-E5012-APP, RWB-S4-E5012-CON | R-38257 | ASM-4631 | Register assumption |  | The proposal is not a business row. It is a view of the local decision record answered on API-S4-003 GET /legal-actions/{legalActionId}, with the proposed step, the reasons (rule ID, condition and facts), the cost and effect with its source, the deciding role and the package version. The step vocabulary is a versioned reference value whose content is not published, and the cost and effect are read on rwb-agent's contract under DP-20 with the rule as fallback. No sixth REST operation is added to the five of TSD S4 T-A.1 and `legal_action` gains no column. | Solution architect of S4 with the P10 architect and the business owner of S4 |
| RWB-S4-E5012-APP, RWB-S4-E5012-CON | R-38259 | ASM-4633 | Register assumption |  | The template status of R-LIT-04 is read on rwb-comms' notice contract as part of the notice answer, and the pack index of R-LIT-16 is read on rwb-document's contract with its defect list items. Both elements and both operation names carry the placeholder. When one of the two facts is absent the rule does not fire, nothing is written, no move is answered and the case keeps its state. | Solution architect of S4 with the P5 and P6 architects and the business owner of S4 |
| RWB-S4-E5014-APP, RWB-S4-E5014-CON | R-38271 | ASM-4645 | Register assumption |  | The appeal window length and the filing deadline of R-LIT-47 are versioned reference rows read with their version in force, held as durable timers of LitigationWorkflow, and their content is carried as the placeholder in both stories. No value is written in code and no figure is taken from another module's clock. |  |
| RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-38272 | ASM-4646 | Register assumption |  | The approved court fee or legal expense is paid and posted against the case by rwb-payment (P8) and is never written in rwb_litigation: this service checks the fee against the schedule, routes it to the approver, writes one decision record per outcome and stores the payment reference the owner returns. No fee column, fee table, posting, ledger entry or balance exists here. | Solution architect of S4 with the P8 rwb-payment architect and the business owner of S4 |
| RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-38273 | ASM-4647 | Register assumption |  | The fee schedule, the fee types and the court levels are versioned reference data of rwb-case, read on its contract; the schedule version is carried on every decision record; no schedule value, fee type or court level is a constant of the code, and DP-06 and DP-07 stay outside this key's pattern set with their dependency rows unclaimed. | Business owner of S4 with the P3 rwb-case reference-data owner and the S4 solution architect |
| RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-38275 | ASM-4649 | Register assumption |  | The approval is the P7 rwb-decision child workflow named in TSD S4 T5.2.2 on queue rwb-decision, the D7.4 limit and the approver's delegation limit are read on the rwb-access authorise contract, and the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43 is read from rwb-decision at its version in force. None of the three is rebuilt here, no limit value is fixed in code or in the document, and the H, C and I metadata rows stay exactly as the plan gives them. | Solution architect of S4 with the P7 rwb-decision and P4 rwb-access architects and the platform library owner |
| RWB-S4-E5016-APP, RWB-S4-E5018-APP, RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-38284 | ASM-4658 | Register assumption |  | Both stories carry Status Draft (realignment v1) and the missing approval of the realigned stories and of the FSD S4 and the TSD S4 they read is treated as an assumption of this run rather than as a blocker; no behaviour and no value of either story depends on a signature, and no status of a source document is changed. | The verification loop collects the sign-offs and only then changes the status of the stories. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S4-E5009-CON | R-02325 | CG-ALL-9204 | 12.5 | Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog | The task queue cell change is not in the story as it stands; the 12.5 row text is not in this chunk. Resubmit with that section. |
| RWB-S4-E5009-CON | R-19865 | DOR-RWB-S4-E5009-CON-9 | 14 | Definition of Ready item 9 Messages: Partial | No section 14 change is in the story. Resubmit with section 14 text so the FSD P1 wording can be applied and verified. |
| RWB-S4-E5009-CON | R-22808 | GAP-0435 | 12.2 | The split of the legacy instruction step, the instruction and pack field names, and which clock is the partner clock | Sections 12.2 and 16 text is not in this chunk, so no old text can be copied. Resubmit with those sections; directive default is ASM-B-ITG-W3-02-E5009-1. |
| RWB-S4-E5009-CON | R-27139 | CG-ALL-9207 | 14 | MSG-P1-001 text differs from the Error and Message Standard v4 | No section 14 change is in the story. The Error and Message Standard v4 source conflicts with R-19865, which says Standard v4 is not in the 03 folder. |
| RWB-S4-E5010-APP | R-19867 | DOR-RWB-S4-E5010-APP-11 | Not in chunk | Definition of Ready item 11 Guardrails: Partial | Guardrail section is not in this chunk, so no old text can be copied. Personal-data class of P2 fields is not in the sources (DOR-RWB-S4-E5010-APP-11); no value invented. |
| RWB-S4-E5011-APP | R-29067 | GAP-2790 | 12.2 | The rule package read and the reference values carry no dependency row, and DP-04, DP-06 and DP-07 are outside the pattern set | Needs the rwb-decision rule-package read and the rwb-case reference-data ride named on the 12.2 contract rows. 12.2 text is not in this chunk, so no anchor. H, C and I rows unchanged. |
| RWB-S4-E5014-APP | R-27182 | CG-ALL-9340 | 16 | Criteria and tests keep legacy job and decision-log wording | Section 16 is in the story. Added rows TC-E5-014-05 to -15 use decision record. Rows TC-E5-014-01 to -04 are outside this diff and must be checked for decision-log wording. |
| RWB-S4-E5014-CON | R-19944 | DOR-RWB-S4-E5014-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-18 and SCR-19 state text lies outside the chunk's story parts, so no exact old text exists to anchor an edit. Grep of 23 Document Gaps found no screen-state text. |
| RWB-S4-E5014-CON | R-32485 | NEWAC-RWB-S4-E5014-CON-AC9 | 7 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are outside the chunk, so no anchor exists for the new AC9 or its TC row. The proposed test is Not specified in the source documents (NEWAC-RWB-S4-E5014-CON-AC9). |
| RWB-S4-E5015-CON | R-19964 | DOR-RWB-S4-E5015-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Needs AC7 in section 7 and its TC row in section 16. Neither text is in this chunk, so there is no safe anchor. Re-run with sections 7 and 16. |
| RWB-S4-E5015-CON | R-32493 | NEWAC-RWB-S4-E5015-CON-AC7 | 8 | AC7: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC7 needs a section 7 anchor and a section 16 row, neither in this chunk. Proposed test is Not specified in the source documents. No TC ID invented. Re-run with sections 7 and 16. |
| RWB-S4-E5016-APP | R-08061 | DOR-RWB-S4-E5016-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or sources; sign-off value not given, so not invented. Project folder checked. |
| RWB-S4-E5016-APP | R-19973 | DOR-RWB-S4-E5016-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR10/BR11 mapping already in §8 text. BR1-BR9 criteria and tests are in §7 and §16, not in this chunk. |
| RWB-S4-E5016-APP | R-19975 | DOR-RWB-S4-E5016-APP-7 | 11 | Definition of Ready item 7 Data: Partial | §11 already states judgment_type and decision_record are not LDM v9 entries. Criteria and tests in §7 and §16 not in this chunk. |
| RWB-S4-E5016-APP | R-27202 | CG-ALL-9403 | 12.5 | Criteria and tests keep legacy job and decision-log wording | §12.5 has no legacy wording. AC1, AC4 and TC-E5-016-06 are in §7 and §16, not in this chunk; resend those lines. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (44)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17143 | RWB-S4-E5009-APP | CG-ALL-9185 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case, per the Document Index service table. |
| CDC-17144 | RWB-S4-E5009-APP | CG-ALL-9186 | 12.2 | Declare REST base /api/recovery/partner/v1 for provider P9 rwb-partner, per the Document Index service table. |
| CDC-17145 | RWB-S4-E5009-APP | CG-ALL-9187 | 12.2 | Declare REST base /api/recovery/document/v1 for provider P5 rwb-document, per the Document Index service table. |
| CDC-17146 | RWB-S4-E5009-APP | CG-ALL-9188 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider P7 rwb-decision, per the Document Index service table. |
| CDC-17150 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-8 | 12 | Add the base paths /api/recovery/case/v1, /api/recovery/partner/v1, /api/recovery/document/v1 and /api/recovery/decision/v1, and the three further bases named in the detcheck. |
| CDC-17160 | RWB-S4-E5009-CON | CG-ALL-9199 | 12.2 | Declare REST base /api/recovery/case/v1 for the case service, taken from the Document Index service table. |
| CDC-17161 | RWB-S4-E5009-CON | CG-ALL-9200 | 12.2 | Declare REST base /api/recovery/partner/v1 for the partner service, taken from the Document Index service table. |
| CDC-17162 | RWB-S4-E5009-CON | CG-ALL-9201 | 12.2 | Declare REST base /api/recovery/document/v1 for the document service, taken from the Document Index service table. |
| CDC-17163 | RWB-S4-E5009-CON | CG-ALL-9202 | 12.2 | Declare REST base /api/recovery/decision/v1 for the decision service, taken from the Document Index service table. |
| CDC-17166 | RWB-S4-E5009-CON | DOR-RWB-S4-E5009-CON-8 | header | Declare REST bases for /api/recovery/case/v1, partner/v1, document/v1, decision/v1 and the four further paths in the detcheck list. |
| CDC-17202 | RWB-S4-E5011-APP | CG-ALL-9243 | 12.2 | Declare the REST base of /api/recovery/payment/v1 using the provider REST base from the Document Index service table |
| CDC-17203 | RWB-S4-E5011-APP | CG-ALL-9244 | 12.2 | Declare the REST base of /api/recovery/case/v1 using the provider REST base from the Document Index service table |
| CDC-17204 | RWB-S4-E5011-APP | CG-ALL-9245 | 12.2 | Declare the REST base of /api/recovery/decision/v1 using the provider REST base from the Document Index service table |
| CDC-17213 | RWB-S4-E5011-CON | CG-ALL-9257 | 12.2 | Declare REST base /api/recovery/payment/v1 using the provider P8 rwb-payment REST base from the Document Index service table. |
| CDC-17214 | RWB-S4-E5011-CON | CG-ALL-9258 | 12.2 | Declare REST base /api/recovery/case/v1 using the provider P3 rwb-case REST base from the Document Index service table. |
| CDC-17215 | RWB-S4-E5011-CON | CG-ALL-9259 | 12.2 | Declare REST base /api/recovery/decision/v1 using the provider P7 rwb-decision REST base from the Document Index service table. |
| CDC-17226 | RWB-S4-E5012-APP | CG-ALL-9271 | 12.2 | Declare REST base /api/recovery/case/v1 for provider rwb-case |
| CDC-17227 | RWB-S4-E5012-APP | CG-ALL-9272 | 12.2 | Declare REST base /api/recovery/comms/v1 for provider rwb-comms |
| CDC-17228 | RWB-S4-E5012-APP | CG-ALL-9273 | 12.2 | Declare REST base /api/recovery/comms/v1 for provider rwb-comms |
| CDC-17229 | RWB-S4-E5012-APP | CG-ALL-9274 | 12.2 | Declare REST base /api/recovery/document/v1 for provider rwb-document |
| CDC-17230 | RWB-S4-E5012-APP | CG-ALL-9275 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider rwb-decision |
| CDC-17231 | RWB-S4-E5012-APP | CG-ALL-9276 | 12.2 | Declare REST base /api/recovery/agent/v1 for provider rwb-agent |
| CDC-17234 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-8 | header | Add the base paths /api/recovery/case/v1, /api/recovery/comms/v1, /api/recovery/document/v1, /api/recovery/decision/v1 and the four further bases in the detcheck list. |
| CDC-17241 | RWB-S4-E5012-CON | CG-ALL-9287 | 12.2 | Declare REST base `/api/recovery/case/v1` for the case read (provider rwb-case, P3). |
| CDC-17242 | RWB-S4-E5012-CON | CG-ALL-9288 | 12.2 | Declare REST base `/api/recovery/comms/v1` for the notice and template read (provider rwb-comms, P6). |
| CDC-17243 | RWB-S4-E5012-CON | CG-ALL-9289 | 12.2 | Declare REST base `/api/recovery/comms/v1` for the notice hold (provider rwb-comms, P6). |
| CDC-17244 | RWB-S4-E5012-CON | CG-ALL-9290 | 12.2 | Declare REST base `/api/recovery/document/v1` for the pack-index read (provider rwb-document, P5). |
| CDC-17245 | RWB-S4-E5012-CON | CG-ALL-9291 | 12.2 | Declare REST base `/api/recovery/decision/v1` for the rule package read (provider rwb-decision, P7). |
| CDC-17246 | RWB-S4-E5012-CON | CG-ALL-9292 | 12.2 | Declare REST base `/api/recovery/agent/v1` for the cost-and-effect read (provider rwb-agent, P10). |
| CDC-17248 | RWB-S4-E5012-CON | DOR-RWB-S4-E5012-CON-8 | 12.2 | Add the base paths /api/recovery/case/v1, /api/recovery/comms/v1, /api/recovery/document/v1 and /api/recovery/decision/v1, and the four further bases named in the detcheck, to the yaml files. |
| CDC-17264 | RWB-S4-E5013-CON | CG-ALL-9314 | 12.2 | Declare REST base /api/recovery/agent/v1 for the P10 proposal operation, taken from the Document Index service table. |
| CDC-17265 | RWB-S4-E5013-CON | CG-ALL-9315 | 12.2 | Declare REST base /api/recovery/decision/v1 for the P7 approval operation, taken from the Document Index service table. |
| CDC-17266 | RWB-S4-E5013-CON | CG-ALL-9316 | 12.2 | Declare REST base /api/recovery/treatment/v1 for the S2 booking operation, taken from the Document Index service table. |
| CDC-17268 | RWB-S4-E5013-CON | DOR-RWB-S4-E5013-CON-8 | 12.2 | Declare the three consumed REST bases; the catalog task-queue mismatch is fixed in 12.5 and needs no yaml change. |
| CDC-17305 | RWB-S4-E5015-APP | CG-ALL-9357 | 12.2 | Declare the REST base of /api/recovery/payment/v1 for P8 rwb-payment, taken from the Document Index service table |
| CDC-17306 | RWB-S4-E5015-APP | CG-ALL-9358 | 12.2 | Declare the REST base of /api/recovery/case/v1 for P3 rwb-case, taken from the Document Index service table |
| CDC-17307 | RWB-S4-E5015-APP | CG-ALL-9359 | 12.2 | Declare the REST base of /api/recovery/decision/v1 for P7 rwb-decision, taken from the Document Index service table |
| CDC-17308 | RWB-S4-E5015-APP | CG-ALL-9360 | 12.2 | Declare the REST base of /api/recovery/access/v1 for P4 rwb-access, taken from the Document Index service table |
| CDC-17312 | RWB-S4-E5015-APP | DOR-RWB-S4-E5015-APP-8 | 12.1 | Add base paths /api/recovery/payment/v1, /api/recovery/case/v1, /api/recovery/decision/v1 and /api/recovery/access/v1, the five further paths in the detcheck list, and the Idempotency-Key header on POST /cases/{caseId}/legal-actions. |
| CDC-17319 | RWB-S4-E5015-CON | CG-ALL-9377 | 12.2 | Declare the REST base /api/recovery/payment/v1 from the Document Index service table. |
| CDC-17320 | RWB-S4-E5015-CON | CG-ALL-9378 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-17321 | RWB-S4-E5015-CON | CG-ALL-9379 | 12.2 | Declare the REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-17322 | RWB-S4-E5015-CON | CG-ALL-9380 | 12.2 | Declare the REST base /api/recovery/access/v1 from the Document Index service table. |
| CDC-17324 | RWB-S4-E5015-CON | DOR-RWB-S4-E5015-CON-8 | 12.2 | Declare REST bases for the consumed paths in CG-ALL-9377 to CG-ALL-9380 and the other flagged paths. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (34)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17104 | RWB-S4-E5007-CON | DOR-RWB-S4-E5007-CON-8 | 12.5 | Add activities verifyPack and authoriseFiling as named in section 12.5, or the story switches to catalogued activities. |
| CDC-17105 | RWB-S4-E5007-CON | CG-ALL-9155 | 12.5 | Add activity verifyPack (task queue rwb-litigation; case and legal action in; rule ID with package version, outcome and case route fact out). |
| CDC-17106 | RWB-S4-E5007-CON | CG-ALL-9156 | 12.5 | Add activity authoriseFiling (task queue rwb-litigation; approval code, rule ID with version, PACK_APPROVED route fact and decided-at time out). |
| CDC-17123 | RWB-S4-E5008-APP | CG-ALL-9167 | 12.5 | Add activity selectPanelFirm to the Activities sheet on task queue rwb-litigation |
| CDC-17152 | RWB-S4-E5009-APP | CG-ALL-9191 | 12.5 | Add activity instructFirm on task queue rwb-litigation to the Activities sheet, or name a catalogued activity in this story. |
| CDC-17178 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-8 | 12.5 | Register activities recordFiling, rejectFiling, recordDecision, armFilingClock and announceFilingMove on task queue rwb-litigation. |
| CDC-17192 | RWB-S4-E5010-CON | CG-ALL-9230 | 12.5 | Story names task queue rwb-litigation, but the namespace rwb-recovery is not stated; the catalog must confirm the namespace. |
| CDC-17195 | RWB-S4-E5010-CON | DOR-RWB-S4-E5010-CON-8 | 12.5 | Add Activity rows recordFiling and rejectFiling on task queue rwb-litigation; the workflow ID and start rule are now stated in the story. |
| CDC-17196 | RWB-S4-E5010-CON | CG-ALL-9232 | 12.5 | Add Activity row recordFiling on task queue rwb-litigation. |
| CDC-17197 | RWB-S4-E5010-CON | CG-ALL-9233 | 12.5 | Add Activity row rejectFiling on task queue rwb-litigation. |
| CDC-17198 | RWB-S4-E5010-CON | CG-ALL-9234 | 12.5 | Add activity recordDecision on task queue rwb-litigation to the Activities sheet. |
| CDC-17208 | RWB-S4-E5011-APP | CG-ALL-9248 | 12.5 | Add activity recordHearing to the Activities sheet, or the story uses a catalogued activity. |
| CDC-17209 | RWB-S4-E5011-APP | CG-ALL-9249 | 12.5 | Add activity armHearingDeadline to the Activities sheet, or the story uses a catalogued activity. |
| CDC-17210 | RWB-S4-E5011-APP | CG-ALL-9250 | 12.5 | Add activity recordSpendDecision to the Activities sheet, or the story uses a catalogued activity. |
| CDC-17217 | RWB-S4-E5011-CON | CG-ALL-9262 | 12.5 | Add activity recordHearing on task queue rwb-litigation to the Activities sheet. |
| CDC-17218 | RWB-S4-E5011-CON | CG-ALL-9263 | 12.5 | Add an Activities row for armHearingDeadline (Task queue rwb-litigation), or name a catalogued activity in its place. |
| CDC-17219 | RWB-S4-E5011-CON | CG-ALL-9264 | 12.5 | Add an Activities row for recordSpendDecision (Task queue rwb-litigation), or name a catalogued activity in its place. |
| CDC-17236 | RWB-S4-E5012-APP | CG-ALL-9279 | 12.5 | Add an Activities row for recommendNextStep on task queue rwb-litigation, or name a catalogued activity in this story. |
| CDC-17249 | RWB-S4-E5012-CON | CG-ALL-9295 | 12.5 | Add a row for activity recommendNextStep on task queue rwb-litigation, or name a catalogued activity in 12.5 instead. |
| CDC-17257 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-8 | 12.5 | Add activities routeSettlementOffer and applySettlementHold on task queue rwb-litigation to the Workflows and activities catalog. |
| CDC-17259 | RWB-S4-E5013-APP | CG-ALL-9306 | 12.5 | Add activity routeSettlementOffer on task queue rwb-litigation to the Activities sheet. |
| CDC-17260 | RWB-S4-E5013-APP | CG-ALL-9307 | 12.5 | Add activity applySettlementHold on task queue rwb-litigation to the Activities sheet. |
| CDC-17270 | RWB-S4-E5013-CON | CG-ALL-9320 | 12.5 | Add activity applySettlementHold on task queue rwb-litigation (booking and hold step) to the Activities sheet, or name a catalogued activity in §12.5. |
| CDC-17281 | RWB-S4-E5014-APP | CG-ALL-9333 | 12.5 | Add activity openAppeal on rwb-litigation to the Activities sheet, or name a catalogued activity. |
| CDC-17289 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-8 | 12.5 | Register LitigationWorkflow and activities openAppeal, recordDecision, requestApproval, instructFirm, recordFiling and announceCaseRoute on task queue rwb-litigation. |
| CDC-17314 | RWB-S4-E5015-APP | CG-ALL-9363 | 12.5 | Add activity recordSpendDecision on task queue rwb-litigation, or name a catalogued activity in its place. |
| CDC-17315 | RWB-S4-E5015-APP | CG-ALL-9364 | 12.5 | Add activity requestSpendApproval on task queue rwb-litigation, or name a catalogued activity in its place. |
| CDC-17316 | RWB-S4-E5015-APP | CG-ALL-9365 | 12.5 | Add activity payLegalSpend on task queue rwb-litigation, or name a catalogued activity in its place. |
| CDC-17326 | RWB-S4-E5015-CON | CG-ALL-9383 | 12.5 | Add an Activities row for recordSpendDecision on task queue rwb-litigation, matching the contract element in 12.5. |
| CDC-17327 | RWB-S4-E5015-CON | CG-ALL-9384 | 12.5 | Add an Activities row for requestSpendApproval on task queue rwb-litigation, matching the contract element in 12.5. |
| CDC-17328 | RWB-S4-E5015-CON | CG-ALL-9385 | 12.5 | Add an Activities row for payLegalSpend on task queue rwb-litigation, matching the contract element in 12.5. |
| CDC-17334 | RWB-S4-E5016-APP | DOR-RWB-S4-E5016-APP-8 | 12.2, 12.5 | Add activities recordJudgment and armAppealWindow on task queue rwb-litigation. |
| CDC-17335 | RWB-S4-E5016-APP | CG-ALL-9398 | 12.5 | Add activity recordJudgment to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-17336 | RWB-S4-E5016-APP | CG-ALL-9399 | 12.5 | Add activity armAppealWindow to the Activities sheet, or name a catalogued activity in section 12.5. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (28)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17108 | RWB-S4-E5007-CON | DOR-RWB-S4-E5007-CON-12 | 16 | Add rows TC-S4-E5007-CON-04 and TC-S4-E5007-CON-05 and the nine TC IDs listed in the item to tab Story test cases |
| CDC-17113 | RWB-S4-E5007-CON | CG-ALL-9157 | 16 | Add rows for TC-E5-007-01 to -06 and TC-S4-E5007-CON-01 to -03, with Given, When and Then copied from the criterion each covers. |
| CDC-17124 | RWB-S4-E5008-APP | CG-ALL-9169 | 16 | Add TC-E5-008-01 to TC-E5-008-06 to Story test cases, with Given, When and Then copied from the criteria they cover |
| CDC-17136 | RWB-S4-E5008-CON | DOR-RWB-S4-E5008-CON-12 | 16 | Add tab Story test cases rows for TC-E5-008-01 to -06 and TC-S4-E5008-CON-01 to -05 under the same IDs. |
| CDC-17140 | RWB-S4-E5008-CON | CG-ALL-9181 | 16 | Workbook change needed; story adds TC-S4-E5008-CON-05 and -06, which also need v8 rows. |
| CDC-17153 | RWB-S4-E5009-APP | CG-ALL-9193 | 16 | Add rows for TC-E5-009-02, TC-E5-009-03, TC-E5-009-04, TC-E5-009-05 and TC-E5-009-06 with Given, When and Then copied from the criterion each covers. |
| CDC-17170 | RWB-S4-E5009-CON | DOR-RWB-S4-E5009-CON-12 | 12.7, 16 | Add rows for TC-E5-009-02 to TC-E5-009-06 and TC-S4-E5009-CON-01 to -04 under the same IDs. |
| CDC-17173 | RWB-S4-E5009-CON | CG-ALL-9208 | 16 | Add rows TC-E5-009-02 to -06 and TC-S4-E5009-CON-01 to -04, with Given, When and Then copied from the criterion each covers. |
| CDC-17185 | RWB-S4-E5010-APP | CG-ALL-9223 | 16 | Add rows TC-E5-010-01 to TC-E5-010-06 with Given, When and Then copied from the criterion each one covers. |
| CDC-17186 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-12 | 12, 12.7, 16 | Add rows for TC-E5-010-01 to TC-E5-010-09 on the story tab, including the new contract (-08) and boundary (-09) tests |
| CDC-17200 | RWB-S4-E5010-CON | DOR-RWB-S4-E5010-CON-12 | 12.7, 16 | Add story test cases TC-E5-010-01 to -06 and TC-S4-E5010-CON-01 to -05 on tab Story test cases. |
| CDC-17201 | RWB-S4-E5010-CON | CG-ALL-9236 | 16 | Add rows TC-E5-010-01 to TC-E5-010-06 and TC-S4-E5010-CON-01 to TC-S4-E5010-CON-04 with Given, When and Then copied from the criteria they cover |
| CDC-17211 | RWB-S4-E5011-APP | CG-ALL-9252 | 16 | Add rows TC-E5-011-01 to TC-E5-011-04 to Story test cases in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-17222 | RWB-S4-E5011-CON | DOR-RWB-S4-E5011-CON-12 | 12.7, 16 | Add tab Story test cases rows for TC-E5-011-01 to -04 and TC-S4-E5011-CON-01 to -04. |
| CDC-17224 | RWB-S4-E5011-CON | CG-ALL-9266 | 16 | Add rows for TC-E5-011-01 to -04 and TC-S4-E5011-CON-01 to -04 in the next version, with Given, When and Then copied from the criteria each covers. |
| CDC-17237 | RWB-S4-E5012-APP | CG-ALL-9281 | 16 | Add rows TC-E5-012-01 to TC-E5-012-06 with Given, When and Then copied from the criteria they cover in section 7. |
| CDC-17238 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-12 | 12, 12.7, 16 | Add rows TC-E5-012-01 to TC-E5-012-11 on tab Story test cases |
| CDC-17252 | RWB-S4-E5012-CON | DOR-RWB-S4-E5012-CON-12 | 12.7, 16 | Add rows TC-E5-012-01 to -06 and TC-S4-E5012-CON-01 to -05 under the same IDs; -05 is the 12.7 boundary row. |
| CDC-17253 | RWB-S4-E5012-CON | CG-ALL-9297 | 16 | Add rows for TC-E5-012-01 to TC-E5-012-06 and TC-S4-E5012-CON-01 to TC-S4-E5012-CON-04, with Given, When and Then copied from the criteria they cover. |
| CDC-17261 | RWB-S4-E5013-APP | CG-ALL-9308 | 16 | Add rows TC-E5-013-01 to TC-E5-013-06 to tab Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-17273 | RWB-S4-E5013-CON | DOR-RWB-S4-E5013-CON-12 | 12.7, 16 | Add rows for TC-E5-013-01 to -06 and TC-S4-E5013-CON-01 to -05 under the same IDs. |
| CDC-17275 | RWB-S4-E5013-CON | CG-ALL-9321 | 16 | Add tab Story test cases rows for TC-E5-013-01 to -06 and TC-S4-E5013-CON-01 to -04, plus new TC-S4-E5013-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-17287 | RWB-S4-E5014-APP | CG-ALL-9339 | 16 | Add rows for TC-E5-014-01 to TC-E5-014-04 in the next version, with Given, When and Then copied from the criterion each row covers |
| CDC-17298 | RWB-S4-E5014-CON | DOR-RWB-S4-E5014-CON-12 | 16 | Add rows for TC-E5-014-01 to -04 and TC-S4-E5014-CON-01 to -05 under the same IDs. |
| CDC-17302 | RWB-S4-E5014-CON | CG-ALL-9350 | 16 | Add rows to the next version for TC-E5-014-01 to TC-E5-014-04 and TC-S4-E5014-CON-01 to TC-S4-E5014-CON-04, with Given, When and Then copied from their criteria. |
| CDC-17317 | RWB-S4-E5015-APP | CG-ALL-9367 | 16 | Add rows TC-E5-015-01 to TC-E5-015-07 with Given, When and Then copied from the criterion each covers. |
| CDC-17330 | RWB-S4-E5015-CON | CG-ALL-9387 | 16 | Add rows for TC-E5-015-01 to TC-E5-015-05 and TC-S4-E5015-CON-01 to TC-S4-E5015-CON-04, Given, When and Then copied from the criterion each covers |
| CDC-17337 | RWB-S4-E5016-APP | CG-ALL-9401 | 16 | Add rows for TC-E5-016-01 to TC-E5-016-06 in Story test cases with Given, When and Then from AC1 to AC4, access and NFR; add TC-E5-016-07 and TC-E5-016-08 in the next version. |

### Epic design record (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17103 | RWB-S4-E5007-CON | DOR-RWB-S4-E5007-CON-14 |  | Record the signed epic design sign-off for this story's epic. |
| CDC-17117 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-14 | none | Record the signed epic design sign-off. |
| CDC-17133 | RWB-S4-E5008-CON | DOR-RWB-S4-E5008-CON-14 | find it | Record the signed epic design sign-off for RWB-S4-E5008-CON. |
| CDC-17147 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-14 | - | Record the signed epic design sign-off for RWB-S4-E5009-APP; the story and source documents hold no sign-off. |
| CDC-17165 | RWB-S4-E5009-CON | DOR-RWB-S4-E5009-CON-14 | header | Record the signed epic design sign-off for RWB-S4-E5009-CON. |
| CDC-17175 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S4; no sign-off is recorded in the story or source documents. |
| CDC-17193 | RWB-S4-E5010-CON | DOR-RWB-S4-E5010-CON-14 |  | No signed epic design in the story or source documents; the sign-off belongs to the epic design record. |
| CDC-17205 | RWB-S4-E5011-APP | DOR-RWB-S4-E5011-APP-14 | Header | Record the signed epic design sign-off for RWB-S4-E5011-APP |
| CDC-17216 | RWB-S4-E5011-CON | DOR-RWB-S4-E5011-CON-14 | Header | Record the signed epic design sign-off for RWB-SVC-S4, then cite it in the story. |
| CDC-17232 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-14 | header | Record the signed epic design sign-off for RWB-S4-E5012-APP |
| CDC-17247 | RWB-S4-E5012-CON | DOR-RWB-S4-E5012-CON-14 | header | Confirm the signed epic design sign-off and record its reference in this story. |
| CDC-17254 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-14 | none | Record the signed epic design sign-off for RWB-S4-E5013-APP; no sign-off exists in this story or the sources. |
| CDC-17267 | RWB-S4-E5013-CON | DOR-RWB-S4-E5013-CON-14 | none | Record the signed epic design sign-off, which the story cannot carry. |
| CDC-17276 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-14 | header | Record the signed epic design sign-off for RWB-SVC-S4 in the epic design record. |
| CDC-17294 | RWB-S4-E5014-CON | DOR-RWB-S4-E5014-CON-14 | n/a | Record the signed sign-off of the epic design for EP05 and RWB-SVC-S4 in the epic design record. |
| CDC-17309 | RWB-S4-E5015-APP | DOR-RWB-S4-E5015-APP-14 | header | Confirm and record the signed epic design sign-off for RWB-SVC-S4 |
| CDC-17323 | RWB-S4-E5015-CON | DOR-RWB-S4-E5015-CON-14 | header | Record the signed epic design sign-off in the epic design record and confirm it there. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17107 | RWB-S4-E5007-CON | DOR-RWB-S4-E5007-CON-1 | 1 | Confirm the role 'tech lead' as a role name in Users Roles and Permissions v5, or align section 1 to the role listed there. |
| CDC-17125 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-6 | 10 | Add role SY-DATALOAD with the litigation R or U rights of TSD S4 T6.1, or remove it from the s10 row. DP-08 authorise check sentence added to s10. |
| CDC-17135 | RWB-S4-E5008-CON | DOR-RWB-S4-E5008-CON-1 | 1 | Add a role code for tech lead of rwb-litigation (S4), or name the matching role code from that document. |
| CDC-17155 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-6 | 10 | Add role SY-DATALOAD to the role list or confirm it as an existing service identity. Story side: authorise check of each REST operation marked Not specified in the source documents. |
| CDC-17168 | RWB-S4-E5009-CON | DOR-RWB-S4-E5009-CON-1 | 1 | Add 'tech lead' of rwb-litigation as a role name or role code. |
| CDC-17187 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-6 | 10 | Add role SY-DATALOAD with Litigation U on the filing fields, as §10 states it |
| CDC-17199 | RWB-S4-E5010-CON | DOR-RWB-S4-E5010-CON-1 | 1 | Add role 'tech lead' of rwb-litigation, or confirm the role name section 1 uses. |
| CDC-17220 | RWB-S4-E5011-CON | DOR-RWB-S4-E5011-CON-1 | 1 | Add 'tech lead' as a role code or role name, or confirm it maps to an existing role code or name. |
| CDC-17239 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-6 | 10 | Add role SY-DATALOAD as used in section 10 of this story |
| CDC-17250 | RWB-S4-E5012-CON | DOR-RWB-S4-E5012-CON-1 | 1 | Add tech lead as a role code or role name, or confirm it is a delivery persona and not a platform role. |
| CDC-17271 | RWB-S4-E5013-CON | DOR-RWB-S4-E5013-CON-1 | 1 | Add role name 'tech lead' (the tech lead of rwb-litigation used in §1 and §10) or confirm the role code it maps to. |
| CDC-17296 | RWB-S4-E5014-CON | DOR-RWB-S4-E5014-CON-1 | 1 | Add the role 'contract owner of rwb-litigation (S4)' as a role name, or give the role code it maps to. |
| CDC-17329 | RWB-S4-E5015-CON | DOR-RWB-S4-E5015-CON-1 | 1 | Add a role code and role name for 'tech lead' as used in section 1, or map it to an existing role code. |
| CDC-17338 | RWB-S4-E5016-APP | DOR-RWB-S4-E5016-APP-6 | 10 | Confirm role SY-DATALOAD in v5 with the Litigation U or R right that section 10 gives it |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17134 | RWB-S4-E5008-CON | CG-ALL-9179 | 12.5 | Add activity selectPanelFirm on queue rwb-litigation, or name a catalogued activity in the story. |
| CDC-17167 | RWB-S4-E5009-CON | CG-ALL-9206 | 12.5 | Add an instructFirm activity row on task queue rwb-litigation, or name a catalogued activity in section 12.5. |
| CDC-17269 | RWB-S4-E5013-CON | CG-ALL-9319 | 12.5 | Add an Activities row for routeSettlementOffer on task queue rwb-litigation, or name a catalogued activity instead. |
| CDC-17282 | RWB-S4-E5014-APP | CG-ALL-9334 | 12.5 | Add an Activities row for activity recordDecision, or the story uses a catalogued activity |
| CDC-17283 | RWB-S4-E5014-APP | CG-ALL-9335 | 12.5 | Add an Activities row for activity requestApproval, or the story uses a catalogued activity |
| CDC-17284 | RWB-S4-E5014-APP | CG-ALL-9336 | 12.5 | Add an Activities row for activity instructFirm, or the story uses a catalogued activity |
| CDC-17285 | RWB-S4-E5014-APP | CG-ALL-9337 | 12.5 | Add an Activities row for activity recordFiling, or the story uses a catalogued activity |
| CDC-17286 | RWB-S4-E5014-APP | CG-ALL-9338 | 12.5 | Add an Activities row for activity announceCaseRoute, or the story uses a catalogued activity |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17151 | RWB-S4-E5009-APP | CG-ALL-9184 | 12.7 | Record decision_record as a platform library object created in rwb_litigation by the library migration (DP-03), or use the dictionary name for it. |
| CDC-17156 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-7 | 11 | Add decision_record as a field or entity; Data Classification v5 must carry it as well. Story side: AC4 wording changed to decision record. |
| CDC-17280 | RWB-S4-E5014-APP | CG-ALL-9330 | 11 | Record decision_record as a platform library object of rwb_litigation (DP-03) or give its dictionary name. |
| CDC-17291 | RWB-S4-E5014-APP | GAP-2802 | 8, 11 | Decide once where the appeal grounds live: a legal_action column with a dictionary row, or an rwb-document reference from the decision record inputs. Until then no column. |
| CDC-17293 | RWB-S4-E5014-APP | GAP-2804 | 7 | Record once: OPEN from window opening, FILED when the firm files, WITHDRAWN when approver declines or appeal not pursued; decision and reason on the decision record. |
| CDC-17295 | RWB-S4-E5014-CON | CG-ALL-9349 | 12.7 | Add decision_record as a platform library object in rwb_litigation, or record it as defined in RWB-PLT-E1027-CON, its owning document. |
| CDC-17301 | RWB-S4-E5014-CON | GAP-2802 | 11 | Record once where the appeal grounds live: a rwb-document reference from the decision record inputs reference, or a new legal_action column with a new DDL major version. Placeholder stays until then. |
| CDC-17304 | RWB-S4-E5014-CON | GAP-2804 | 11 | Record the mapping once: OPEN from window opening, FILED when the firm files, WITHDRAWN when the approver declines or the appeal is not pursued, with the decision and reason on the decision record. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17121 | RWB-S4-E5008-APP | CG-ALL-9161 | 2, 8 | Name pack_verified_at kept as in Business Rules v4; no rename applied |
| CDC-17126 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-7 | 7, 11 | Add field pack_verified_at and entry decision_record, or confirm the rule row field names. Story side: AC1 and AC4 now say decision record. |
| CDC-17188 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-7 | 11 | P3 data wording is not changed. AC1 wording changed from decision log to decision record under CG-ALL-9225, so it is not word for word. |
| CDC-17240 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-7 | 11 | Add decision_record as a platform library object created in rwb_litigation (DP-03) |
| CDC-17263 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-7 | 11 | Record decision_record and idempotency_key as platform library objects of RWB-PLT-E1027-CON, or confirm they sit outside the model. |
| CDC-17288 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-7 | 11, 7 | State decision_record as a platform library object created by the PLT library migration (DP-03), outside both documents; section 11 already says so. P3 wording fixed in section 7. |
| CDC-17299 | RWB-S4-E5014-CON | DOR-RWB-S4-E5014-CON-7 | 11 | Added paragraph marking whether the eight shape rows carry a BR Field ID as Not specified in the source documents |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17180 | RWB-S4-E5010-APP | CG-ALL-9217 | 12.5 | Add activity recordFiling (type Activity, task queue rwb-litigation) or name a catalogued activity to replace it. |
| CDC-17181 | RWB-S4-E5010-APP | CG-ALL-9218 | 12.5 | Add activity rejectFiling (type Activity, task queue rwb-litigation) or name a catalogued activity to replace it. |
| CDC-17182 | RWB-S4-E5010-APP | CG-ALL-9219 | 12.5 | Add activity recordDecision (type Activity through the library, task queue rwb-litigation) or name a catalogued activity to replace it. |
| CDC-17183 | RWB-S4-E5010-APP | CG-ALL-9220 | 12.5 | Add activity armFilingClock (type Activity, task queue rwb-litigation) or name a catalogued activity to replace it. |
| CDC-17184 | RWB-S4-E5010-APP | CG-ALL-9221 | 12.5 | Add activity announceFilingMove (type Activity, task queue rwb-litigation) or name a catalogued activity to replace it. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17115 | RWB-S4-E5008-APP | CG-ALL-9163 | 12.2 | Publish the operation ID of GET /partners at /api/recovery/partner/v1/partners in the rwb-partner contract; the path is already present with GET. |
| CDC-17116 | RWB-S4-E5008-APP | CG-ALL-9164 | 12.2 | Declare REST base /api/recovery/partner/v1 taken from the Document Index service table. |
| CDC-17131 | RWB-S4-E5008-CON | CG-ALL-9175 | 12.2 | Publish GET /partners under /api/recovery/partner/v1 through the provider CON story, or name a published operation (GAP-2773). |
| CDC-17132 | RWB-S4-E5008-CON | CG-ALL-9176 | 12.2 | Declare REST base /api/recovery/partner/v1 taken from the Document Index service table. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17127 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-9 | 14 | Align the MSG-P1-001 text in section 14 to the Standard v4 wording for this message. |
| CDC-17129 | RWB-S4-E5008-APP | CG-ALL-9168 | 14 | MSG-P1-001 text kept as in the legacy story |
| CDC-17189 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-9 | 14 | Confirm MSG-P1-001 wording against the standard |
| CDC-17223 | RWB-S4-E5011-CON | DOR-RWB-S4-E5011-CON-9 | 14 | Change MSG-P1-001 text to match section 14: '{product} is from {date}. Today's ACE batch has not arrived.' |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17158 | RWB-S4-E5009-APP | GAP-2785 | 11 | Record DP-04 with H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON at realignment and carry the rwb-decision LITIGATION read as a non-blocking consumed row with its fake. No rule row authored in this key. |
| CDC-17172 | RWB-S4-E5009-CON | GAP-2785 | 4 | Record DP-04 with H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON when the rule-governance keys are realigned. Keep metadata rows; rwb-decision read stays non-blocking. |
| CDC-17290 | RWB-S4-E5014-APP | GAP-2801 | find it | Carry four non-blocking consumed rows: rwb-decision approval contract (C, its wave); rwb-case and rwb-partner contracts (published, built against fakes); RWB-P3-E1043-CON (C); edges use each operation's declared right per DP-08. |
| CDC-17300 | RWB-S4-E5014-CON | GAP-2801 | 11 | Carry the four consumed surfaces as non-blocking rows: approval contract as C of its wave; rwb-case and rwb-partner contracts as published; RWB-P3-E1043-CON as C. Metadata rows unchanged. |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17122 | RWB-S4-E5008-APP | CG-ALL-9162 | 12.7 | Record decision_record in the owning document as a library table created in rwb_litigation by the library migration (DP-03) |
| CDC-17235 | RWB-S4-E5012-APP | CG-ALL-9270 | 11, 12.7 | Record decision_record as a platform library table created in rwb_litigation by the library migration (DP-03), or use the dictionary name. |
| CDC-17258 | RWB-S4-E5013-APP | CG-ALL-9303 | none | Record decision_record as a named library table object in its own document, or use the dictionary field name. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17154 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-11 | 11 | Set the personal-data class of each field this story carries to match the source of record, and align the story's statement that no personal data is carried with it. |
| CDC-17262 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-11 | 17 | Fields rows idempotency_key in decision_log_entry and interaction (Confidential / Customer data): state the handling rule (codec, masking) or reclassify. Not specified in the source documents (CG-ALL-9309). |
| CDC-17297 | RWB-S4-E5014-CON | DOR-RWB-S4-E5014-CON-11 | n/a | Reconcile the personal-data class of the fields the story carries with its statement that no personal data is carried. |

### RWB-S4-E5011-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17206 | RWB-S4-E5011-APP | DOR-RWB-S4-E5011-APP-21 | Header | Set build status to Done |
| CDC-17207 | RWB-S4-E5011-APP | DOR-RWB-S4-E5011-APP-22 | Header | Publish the contract fake library and record its version |
| CDC-17212 | RWB-S4-E5011-APP | GAP-2789 | find it | Name the workflow kit contract as a contract dependency for LitigationWorkflow timers; the story's metadata rows stay as they are. |

### RWB-S4-E5014-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17277 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-21 | header | Publish the contract and set its build status to Done. |
| CDC-17278 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-22 | header | Publish the contract fake and record its library version as published. |
| CDC-17279 | RWB-S4-E5014-APP | DOR-RWB-S4-E5014-APP-23 | header | Publish a contract version and name it in the header Contract version row. |

### RWB-S4-E5016-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17332 | RWB-S4-E5016-APP | DOR-RWB-S4-E5016-APP-21 | header | Set build status to Done; it is currently Not started. |
| CDC-17333 | RWB-S4-E5016-APP | DOR-RWB-S4-E5016-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-17340 | RWB-S4-E5016-APP | GAP-2830 | 9 | Add a CON absence test that it holds no judgment write for R-LIT-44; AC3 regression is proven in this story |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17110 | RWB-S4-E5007-CON | GAP-2771 | 8 | Record the E2 delivery of API-S4-001 so the key is not reopened for a notice approval |
| CDC-17112 | RWB-S4-E5007-CON | GAP-2766 | 8 | Record the legacy data and endpoint blocks of RWB-E5-007 as Outdated |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17114 | RWB-S4-E5007-CON | GAP-2769 | header | Trace legacy key RWB-E5-007 to REQ-S4-003 and FEAT-LIT-07 in the RTM and in the legacy story; the Epics 3 to 8 PRD adds the identifiers. |
| CDC-17141 | RWB-S4-E5008-CON | GAP-2776 | header | Add reverse link of RWB-E5-008 and RWB-S4-E5008-CON to REQ-S4-004 when the RTM is next versioned. |

### RWB-S4-E5008-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17118 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-21 | header | Publish the contract and set its build status to Done. |
| CDC-17119 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-22 | header | Record the published contract fake library version. |

### RWB-S4-E5009-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17148 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-21 | - | Move build status of contract story RWB-S4-E5009-CON from Not started to Done. |
| CDC-17149 | RWB-S4-E5009-APP | DOR-RWB-S4-E5009-APP-22 | - | Publish a contract fake library version for RWB-S4-E5009-CON and record it as published. |

### RWB-ITG-W3J01-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17157 | RWB-S4-E5009-APP | GAP-0436 | find it | Agree at the wave 3 entry check with integration and QA leads the harness environment, seeding set, business date, product codes, evidence format, gate thresholds and the three unnamed operations; record the values in that story. |
| CDC-17171 | RWB-S4-E5009-CON | GAP-2160 | 4 | Prove the instruction hop against the published S9 contract fake in wave 3. Move the real-owner instruction, result and review to RWB-ITG-W4J01-ITG. |

### RWB-S4-E5010-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17176 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-21 | header | Complete the build of RWB-S4-E5010-CON (build status Not started) and publish the contract. |
| CDC-17177 | RWB-S4-E5010-APP | DOR-RWB-S4-E5010-APP-22 | header | Publish the contract fake library version for RWB-S4-E5010-CON and record that version. |

### RWB-S4-E5013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17255 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-21 | header | Publish the contract and set its build status to Done before this story starts. |
| CDC-17256 | RWB-S4-E5013-APP | DOR-RWB-S4-E5013-APP-22 | header | Publish a contract fake library version and record it on RWB-S4-E5013-CON. |

### OTHER:rwb-document, rwb-comms, rwb-case and rwb-decision contracts (wave 3 freeze) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17109 | RWB-S4-E5007-CON | GAP-2765 | 12.2 | Publish the pack and defect-list read, the notice and template-status read, the case read with route fact and task raise, and the D7 approval raise, each with a fake and a 2 s budget |

### OTHER:FSD S4 field catalogue A2.6.3.2 to A2.21.3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17111 | RWB-S4-E5007-CON | GAP-1739 | 11 | Type legal_action.case_id as varchar(255) business key with no foreign key, keeping the field name |

### OTHER:TSD S4 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17120 | RWB-S4-E5008-APP | DOR-RWB-S4-E5008-APP-8 | 12.1 | Add an idempotency key to PATCH /legal-actions/{legalActionId} (API-S4-004). |

### OTHER:rwb-partner (S9) panel and instruction contract; OTHER:TSD S9 v2 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17128 | RWB-S4-E5008-APP | GAP-2778 | 11 | Publish the score, capacity, court coverage and conflict status fields of the panel answer and the two operation names before baseline tag. |

### OTHER:rwb-source-data and rwb-partner stories (FSD S4 v3 A2.8.3.1 rule VR-S4-008-1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17130 | RWB-S4-E5008-APP | GAP-2779 | 14 | Apply VR-S4-008-1 where the ACE data product is read, in rwb-source-data and rwb-partner. This story already carries MSG-P1-001 in section 14 and on SCR-19. |

### OTHER:plan (step D1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17137 | RWB-S4-E5008-CON | GAP-2773 | 13 | Story names the reads and defers plan rows to step D1; the plan change is outside this story. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17138 | RWB-S4-E5008-CON | GAP-2777 | 8 | Publish R-LIT-23 and R-LIT-27 rule rows, package version, scoring and capacity parameters, court coverage set, conflict rule and accept window as versioned reference data. |

### OTHER:rwb-partner panel contract (S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17139 | RWB-S4-E5008-CON | GAP-2778 | 4 | Fix the panel field list for score, capacity, court coverage and conflict status and the two operation names with the rwb-partner owner before tagging the baseline. |

### OTHER:rwb-source-data and rwb-partner contracts (FSD S4 v3 VR-S4-008-1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17142 | RWB-S4-E5008-CON | GAP-2779 | 15 | Apply VR-S4-008-1 where the ACE data product is read; freshness read in 12.2 not added unless the solution architect decides so. |

### OTHER:Epics 3 to 8 PRD and S4 module trace (PRD owner of EP05) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17159 | RWB-S4-E5009-APP | GAP-2784 | 19 | Add one requirement row for the firm instruction as its own requirement; then rewrite the requirement column of RWB-E5-009, this story and their fragments. Until then REQ-S4-004 stays with the section 18 reading. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17164 | RWB-S4-E5009-CON | CG-ALL-9203 | 7 | Remove the fixed enum on actionType so LOV-LEGAL-TYPE values are accepted as data without a code change. |

### RWB-S4-E5009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17169 | RWB-S4-E5009-CON | DOR-RWB-S4-E5009-CON-10 | find it | Add the empty, loading, error and no access states of SCR-19 and SCR-20. |

### OTHER:Epics 3 to 8 PRD and S4 module trace (EP05 PRD owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17174 | RWB-S4-E5009-CON | GAP-2784 | 18 | Add one requirement row for the firm-instruction step of RWB-E5-009 as its own requirement, then rewrite the requirement column of RWB-S4-E5009-CON and its fragments. Until then REQ-S4-004 stays. |

### OTHER:PLT library document (decision record library) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17179 | RWB-S4-E5010-APP | CG-ALL-9213 | 12.9 | Record decision_record as a library table object, with its DDL and migration, in the owning library document. |

### OTHER:Legacy story RWB-E5-015 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17190 | RWB-S4-E5010-APP | GAP-2808 | 7 | Keep its AC2 word for word with origin tag, proven as post-condition against contract fakes; write no black_case_no and arm no hearing timer; spend states as route states, no LOV value. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17191 | RWB-S4-E5010-APP | GAP-1744 | 12 | Add numbered rows for LawsuitFiled, JudgmentRecorded and AuctionResult on rwb.litigation.events.v1, keyed by case, consumers rwb-asset and rwb-case; EV numbers from the catalogue change. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17194 | RWB-S4-E5010-CON | DOR-RWB-S4-E5010-CON-5 | 9 | Add FILING_REJECTED to the closed list LOV-LEGAL-STATUS. |

### RWB-S4-E5011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17221 | RWB-S4-E5011-CON | DOR-RWB-S4-E5011-CON-10 | find it | Add empty, loading, error and no-access states for SCR-19 and SCR-20. |

### OTHER:rwb-case contract (case answer operation name) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17225 | RWB-S4-E5011-CON | GAP-2791 | 12.5 | Trigger marked Not specified in the source documents (GAP-2791). Case answer operation name left as placeholder. |

### RWB-S4-E5012-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17233 | RWB-S4-E5012-APP | DOR-RWB-S4-E5012-APP-21 | header | Set build status to Done so the contract is published |

### OTHER:P3 screen set for SCR-18 and SCR-19 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17251 | RWB-S4-E5012-CON | DOR-RWB-S4-E5012-CON-10 | none | Add empty, loading, error and no access states for SCR-18 and SCR-19. |

### RWB-S4-E5013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17272 | RWB-S4-E5013-CON | DOR-RWB-S4-E5013-CON-10 | 1 | Add empty, loading, error and no-access states for SCR-18 and SCR-19; this contract story declares no screen. |

### OTHER:Recovery Workbench FSD S4 (field catalogs A2.6.3.2 to A2.21.3.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17274 | RWB-S4-E5013-CON | GAP-1739 | 11 | Type legal_action.case_id as varchar(255) business key with no foreign key, keeping the field name; the case number is the business key. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17292 | RWB-S4-E5014-APP | GAP-2803 | header | Add one requirement row for the appeal decision, its grounds, approval and tracking to the hearing; then rewrite the requirement column of RWB-E5-014 and its fragments. |

### OTHER:Epics 3 to 8 PRD and FSD S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17303 | RWB-S4-E5014-CON | GAP-2803 | header | Add one requirement row covering the appeal decision with grounds and approval, and tracking to the hearing; then rewrite the requirement column of both slices. |

### RWB-S4-E5015-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17310 | RWB-S4-E5015-APP | DOR-RWB-S4-E5015-APP-21 | header | Set build status to Done with the contract published |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17311 | RWB-S4-E5015-APP | DOR-RWB-S4-E5015-APP-22 | header | Publish and record a contract fake library version for the four consumed REST paths |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17313 | RWB-S4-E5015-APP | GAP-1737 | header | Add S4 cells to rwb-document (P5), rwb-payment (P8) and rwb-agent (P10) on slides 13 and 19, and record the S4 contract paths in the Ownership Map. |

### OTHER:Run folder _work/msr/extract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17318 | RWB-S4-E5015-APP | GAP-2810 | header | Add the FSD S4 and TSD S4 module extracts so the citations and the extract agree. |

### OTHER:connection matrix (rwb-document, rwb-payment, rwb-agent; OTHER:ALS and GL cells) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17325 | RWB-S4-E5015-CON | GAP-1737 | header | Contract dependencies row names P5, P8 and P10; ALS, GL and rwb-agent cells are not in the story. |

### OTHER:_work/msr/extract (run folder; OTHER:S4 FSD and TSD module extracts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17331 | RWB-S4-E5015-CON | GAP-2810 | header | Add the S4 module extracts to the run folder at the next assembly step so the citations and the extract agree |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17339 | RWB-S4-E5016-APP | GAP-1744 | 12.5 | Add numbered catalogue rows and events-sheet rows for LawsuitFiled, JudgmentRecorded and AuctionResult on rwb.litigation.events.v1; EV ids set there |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0435 | The split of the legacy instruction step, the instruction and pack field names, and which clock is the partner clock | Solution architect | Resolved (directive) |
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-1737 | The connection matrix gives S4 no cell to rwb-document, rwb-payment or rwb-agent, while the FSD names the document hub, ALS and GL and the model gateway | Solution architect | Resolved (directive) |
| GAP-1739 | legal_action.case_id is a uuid in the FSD, while ADR-014 and DP-01 forbid a cross-schema foreign key and require a varchar(255) business key | Data architect | Resolved (directive) |
| GAP-1744 | LawsuitFiled, JudgmentRecorded and AuctionResult have no EV number and no catalogue row | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-2160 | The wave 3 journey drives rwb-partner, which the wave map places in wave 4 | Integration lead | Resolved (directive) |
| GAP-2765 | No source publishes the four consumed surfaces the pack step needs: the pack and defect-list read of rwb-document, the notice and template-status read of rwb-comms, the case read with its task raise and route fact of rwb-case, and the D7 approval item of rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2766 | The legacy data block and endpoint block give this story the case, the task, the timer, the notice and the decision ledger, which the target assigns to rwb-case, rwb-comms and rwb-decision | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2767 | No stored field or list value carries the pack verification, the filing authorisation, the defect-list result, the template status or the prescription days, and no status value names the two acts | Solution architect | Resolved (directive) |
| GAP-2768 | No source fixes how the template-withdrawn fact and the prescription warning reach the service, or who owns the 1-working-day and 2-working-day service levels of R-LIT-04 and R-LIT-16 | Solution architect | Resolved (directive) |
| GAP-2769 | The legacy story and the Epics 3 to 8 specification carry no requirement identifier for this feature | Business analyst | Resolved (directive) |
| GAP-2770 | No source gives the element names or the field lists of the pack verification, the filing authorisation, the case route fact or the task raise, and no source states which document publishes the pack element | Solution architect | Resolved (directive) |
| GAP-2771 | The legacy endpoint block gives the contract the notice approval operation, which the TSD places first in Epic 2 and which the ownership rows still list under rwb-litigation | Solution architect | Resolved (directive) |
| GAP-2773 | The panel read, the decline read and the case-move answer are consumed by both stories, have no contract story in the plan and no C row | Solution architect | Resolved (directive) |
| GAP-2774 | PartnerResultSubmitted lists rwb-litigation as a consumer while DP-09 is not in this key's pattern set, so the decline cannot arrive as an event | Solution architect | Resolved (directive) |
| GAP-2775 | The legacy selection runs unattended while the target runs it as one step of LitigationWorkflow that no source names | Solution architect | Resolved (directive) |
| GAP-2776 | The legacy story master carries no requirement identifier for RWB-E5-008 | Solution architect | Resolved (directive) |
| GAP-2777 | The rule rows of R-LIT-23 and R-LIT-27, their scorecard weights, capacity test, court set, conflict check and accept window, and the D7 level have no content in any source read for this key | Solution architect | Resolved (directive) |
| GAP-2778 | The score, capacity, court coverage and conflict fields of a panel firm have no field list and no operation name, and the legacy v_ace_score read has no grant in this service | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2779 | VR-S4-008-1 tests the freshness of the ACE batch of the source, and rwb-litigation holds no ACE view to test it | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2781 | The instruction has no row and no published operation in rwb-litigation, and the partner rows and the pack are other services' | Solution architect, S4 rwb-litigation, with the S9 rwb-partner and P5 rwb-document architects | Resolved (directive) |
| GAP-2782 | The firm events are named in the rules while the service publishes and consumes nothing, and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and S9 rwb-partner architects and the event platform team | Resolved (directive) |
| GAP-2784 | The legacy master carries no requirement identifier for RWB-E5-009, so both stories trace to the feature and to REQ-S4-004 | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2785 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |
| GAP-2786 | The LIT lawsuit read, the four consumed operations, the filing clocks and the requirement identifier have no owner, no element and no value in the sources read | Business analyst, S4, with the solution architect, the API owner and the rwb-case, rwb-document, rwb-partner, rwb-source-data and rwb-decision tech leads | Resolved (directive) |
| GAP-2787 | The update element names courtCaseNo while the row and the response name black_case_no, and it carries neither a filing date nor a defect field | API owner with the solution architect and the rwb-litigation tech lead, at the wave 3 contract freeze | Resolved (directive) |
| GAP-2789 | The deadline has no value in any source and its row belongs to rwb-case, while the service owns no Schedule or job | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the Temporal platform owner | Resolved (directive) |
| GAP-2790 | The rule package read and the reference values carry no dependency row, and DP-04, DP-06 and DP-07 are outside the pattern set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision and P3 rwb-case architects | Resolved (directive) |
| GAP-2791 | The trigger of the step is named by no source, the legacy endpoints name no hearing operation, and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case, S9 rwb-partner architects and the event platform team | Resolved (directive) |
| GAP-2792 | No requirement identifier, hearing lead time, spend limit or prescription horizon is given for this key | Business analyst, S4, with the PRD builder and the reference-data owner of rwb-case | Resolved (directive) |
| GAP-2794 | The trigger of the step, the officer task raise and the generation hold have no event and no published operation | Solution architect of S4 with the P3 and P6 architects | Resolved (directive) |
| GAP-2796 | The legacy master carries no requirement identifier for RWB-E5-012, so both stories trace to the feature and one nearest module requirement | Business analyst of S4 and the PRD owner of EP05 | Resolved (directive) |
| GAP-2797 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | P7 rwb-decision architect with the solution architect of S4 | Resolved (directive) |
| GAP-2798 | The four consumed rows of the settlement step — the agent proposal, the approval at D7.4, the treatment booking and the case move — are in no C row of the plan | S4 rwb-litigation service owner with the P10, P7, S2 and P3 owners | Resolved (directive) |
| GAP-2799 | The trigger of the step, the shape of the agent proposal and the storage of the hold LITIGATION_HELD have no single source, and no source gives a held status value | S4 rwb-litigation service owner with the solution architect | Resolved (directive) |
| GAP-2800 | The approver named by the limit has no Litigation role row, and the legacy screen table names SCR-18 for a settlement step whose states it cannot show | S4 rwb-litigation service owner with the P7 rwb-decision owner and the access owner of P4 | Resolved (directive) |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2802 | The appeal grounds that legacy AC1 records are neither a column of legal_action nor a field of the FSD catalog | Data steward and business analyst, S4 rwb-litigation, with the P5 rwb-document owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2803 | The legacy master carries no requirement identifier for RWB-E5-014, so both slices trace to the feature only | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2804 | No value of LOV-LEGAL-STATUS names an appeal decision or a declined appeal, and the appeal's own states are case route states | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the business analyst of S4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2808 | Legacy AC2 of this key carries R-LIT-30, a filing rule already owned by two sibling stories, and the spend states are not values of LOV-LEGAL-STATUS | Solution architect, S4 rwb-litigation, with the story owners of RWB-S4-E5010 and RWB-S4-E5011 | Resolved (directive) |
| GAP-2810 | No requirement identifier exists for FEAT-LIT-15 and the S4 module extracts are absent from the run folder | Business analyst of EP05 with the S4 tech lead and the run coordinator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2811 | The judgment type, the dismissal, the appeal window and the enforcement task have no column, no list value and no owned row, and the delivery that opens them has no source | S4 rwb-litigation service owner with the P3 rwb-case owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-2812 | The trigger of the step, the v_ace_lawsuit read of the feature extract and the three consumed owner contracts have no single source, and no contract row is planned | S4 rwb-litigation service owner with the solution architect and the P2 rwb-integration owner | Resolved (directive) |
| GAP-2813 | The legacy key carries no requirement id in the story master and the plan carries no requirement for either slice | S4 rwb-litigation service owner with the business analyst | Resolved (directive) |
| GAP-2830 | R-LIT-44 and the judgment write are named by two legacy keys, so the judgment criterion of RWB-E5-020 is a regression and not a second build | Solution architect with the tech lead of S4 and the business analyst of EP05 | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC5 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC6 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC7 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC8 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC9 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC10 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC11 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC12 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC13 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC14 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC15 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC16 is new and no section 16 row covers it |
| RWB-S4-E5009-APP | new AC without TC row | 494 | AC17 is new and no section 16 row covers it |
