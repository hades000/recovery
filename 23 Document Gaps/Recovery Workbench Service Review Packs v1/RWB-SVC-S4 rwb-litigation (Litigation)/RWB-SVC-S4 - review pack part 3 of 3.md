# RWB-SVC-S4 rwb-litigation (Litigation) - review pack, part 3 of 3 (RWB-S4-E5016-CON to RWB-S4-E5022-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 13 |
| Resolved in the stories | 265 |
| Cross-document (pending in another document) | 201 |
| Not applied (value not in the sources) | 10 |
| Open business decisions | 19 |
| Register gaps linked | 44 |
| Unconfirmed assumptions | 0 |
| Lint findings | 7 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S4-E5016-CON | 20 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5016 CON Record the judgment - contract v2.md |
| RWB-S4-E5017-APP | 25 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5017 APP Trace assets for enforcement v2.md |
| RWB-S4-E5017-CON | 15 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5017 CON Trace assets for enforcement - contract v2.md |
| RWB-S4-E5018-APP | 28 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5018 APP Apply for the writ and seizure v2.md |
| RWB-S4-E5018-CON | 12 | 13 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5018 CON Apply for the writ and seizure - contract v2.md |
| RWB-S4-E5019-APP | 23 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5019 APP Follow the LED auction ladder v2.md |
| RWB-S4-E5019-CON | 15 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5019 CON Follow the LED auction ladder - contract v2.md |
| RWB-S4-E5020-APP | 30 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5020 APP Record an enforcement deferral with its reason v2.md |
| RWB-S4-E5020-CON | 16 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5020 CON Record an enforcement deferral with its reason - contract v2.md |
| RWB-S4-E5021-APP | 20 | 19 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5021 APP File a bankruptcy petition v2.md |
| RWB-S4-E5021-CON | 7 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5021 CON File a bankruptcy petition - contract v2.md |
| RWB-S4-E5022-APP | 31 | 21 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5022 APP Match enforcement proceeds to the case v2.md |
| RWB-S4-E5022-CON | 23 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S4 rwb-litigation (Litigation)/RWB S4 E5022 CON Match enforcement proceeds to the case - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S4-E5022-APP | R-02417 | CG-ALL-9556 | Script gap | Product owner | The story adds JUDGMENT_RECORDED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5022-APP | R-02418 | CG-ALL-9557 | Script gap | Product owner | The story adds PROCEEDS_MATCHED to the closed list LOV-LEGAL-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5022-APP | R-02419 | CG-ALL-9558 | Script gap | Product owner | The story adds JUDGMENT_RECORDED to the closed list LOV-LEGAL-TYPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5022-APP | R-02420 | CG-ALL-9559 | Script gap | Product owner | The story adds PROCEEDS_MATCHED to the closed list LOV-LEGAL-TYPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S4-E5016-APP, RWB-S4-E5016-CON, RWB-S4-E5020-APP, RWB-S4-E5020-CON, RWB-S5-E4021-APP, RWB-S5-E4021-CON | R-09245 | GAP-1471 | Register gap | Head of Litigation | Enforcement after judgment and the eviction of a held property have no named owner role | Use the enforcement owner role the rules already name for enforcement, with Legal counsel named on an eviction, and record the assignment as an assumption until the operating model names the holder. |
| RWB-S4-E5017-APP | R-12644 | CG-ALL-9431 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5018-APP | R-12655 | CG-ALL-9457 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5019-APP | R-12670 | CG-ALL-9486 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5020-APP | R-12690 | CG-ALL-9521 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5021-APP | R-12705 | CG-ALL-9545 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5021-CON | R-12707 | CG-ALL-9552 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5022-APP | R-12712 | CG-ALL-9568 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S4-E5003-APP, RWB-S4-E5003-CON, RWB-S4-E5010-APP, RWB-S4-E5010-CON, RWB-S4-E5017-APP, RWB-S4-E5017-CON, RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-23420 | GAP-1746 | Register gap | Product Owner | REQ-S4-009 (prescription warnings) has no BRD requirement row, and BR-038 and BR-042 carry no program requirement ID | Carry REQ-S4-009 into this PRD as FR-S4-051 and FR-S4-052 under BR-034, the requirement that owns the statutory clock, and record the gap so the E5 BRD can add the row. Carry BR-038 and BR-042 from the FSD features and the RWB-E5 story keys. Nothing is dropped and no requirement is merged. |
| RWB-S4-E5018-APP, RWB-S4-E5018-CON | R-23458 | GAP-2823 | Register gap | Business owner of the LITIGATION route set in rwb-decision with the reference-data owner | The writ deadline of R-LIT-54 has no interval in any source and the story carries it as a reference value | Add the writ deadline as a versioned reference row owned with the LITIGATION package and read by the timer; no code constant is created. |
| RWB-S4-E5016-APP, RWB-S4-E5016-CON | R-29140 | GAP-2814 | Register gap | Solution architect and the business owner of S4 | The FSD S4 and the TSD S4 that the two slices read are In review with an empty sign-off table and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes. |
| RWB-S4-E5018-APP, RWB-S4-E5018-CON | R-29143 | GAP-2822 | Register gap | Solution architect and the business owner of S4 | The FSD S4 and the TSD S4 that both slices read are In review with an empty sign-off table and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes. |
| RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-29148 | GAP-2834 | Register gap | Solution architect and the business owner of S4 | The FSD S4 and the TSD S4 that the two slices read are In review with an empty sign-off table and the realigned stories have no approval | Keep both stories at Draft (realignment v1) and let the verification loop collect the sign-offs before any status changes. |
| RWB-S4-E5016-APP, RWB-S4-E5018-APP, RWB-S4-E5021-APP, RWB-S4-E5021-CON | R-38284 | ASM-4658 | Register assumption |  | Both stories carry Status Draft (realignment v1) and the missing approval of the realigned stories and of the FSD S4 and the TSD S4 they read is treated as an assumption of this run rather than as a blocker; no behaviour and no value of either story depends on a signature, and no status of a source document is changed. | The verification loop collects the sign-offs and only then changes the status of the stories. |
| RWB-S4-E5018-APP, RWB-S4-E5018-CON | R-38296 | ASM-4669 | Register assumption |  | The writ deadline of R-LIT-54 is one durable timer of LitigationWorkflow armed from a versioned reference value at its version; the reference value is Not specified in the source documents (CG-B2-S4-018-5; ASM-B2-S4-018-5), and no timer row, no Temporal Schedule and no Quartz row is created. | The owner of the LITIGATION route set and the reference-data owner publish the writ deadline as a versioned row and the S4 owner confirms the timer is a workflow timer. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S4-E5017-APP | R-19985 | DOR-RWB-S4-E5017-APP-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Sections 7, 15 and 16 text not in this chunk; no exact old anchor. Evidence (§15 SCR-19/SCR-20 states 'none') found in _work/msr/directive/mp/chunks/RWB-S4-E5017-APP/c04.md. Re-issue with §15 and §16. |
| RWB-S4-E5017-APP | R-19986 | DOR-RWB-S4-E5017-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Sections 11 and 16 text not in this chunk; no exact old anchor. primary_person_key is only a candidate and its DF-CAS row was not in this chunk. Re-issue with §11 and §16. |
| RWB-S4-E5018-CON | R-20013 | DOR-RWB-S4-E5018-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-19 and SCR-20 text is not in this chunk; section 15 is cited as the source of their states but was not supplied. No row can be placed without the current text. |
| RWB-S4-E5018-CON | R-20016 | DOR-RWB-S4-E5018-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Rule-coverage test is not specified in the sources (R-32521). Section 7 is not in this chunk. |
| RWB-S4-E5018-CON | R-32521 | NEWAC-RWB-S4-E5018-CON-AC9 | 7, 8, 16 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Proposed test is Not specified in the source documents (NEWAC-RWB-S4-E5018-CON-AC9). Sections 7 and 16 text is not in this chunk, so no AC9 or test row can be written. |
| RWB-S4-E5019-APP | R-20020 | DOR-RWB-S4-E5019-APP-11 | 11 | Definition of Ready item 11 Guardrails: Partial | Section 11 text is not in this chunk, so no exact old text exists and no edit is made. Send section 11 to classify the P2 personal-data fields. |
| RWB-S4-E5021-APP | R-20059 | DOR-RWB-S4-E5021-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | ID cells of 5 rule rows (R-LIT-56/57/58, R-UNI-39/40) now lead with BR IDs in section 8. Coverage of BR1, BR2, BR4-BR7 needs sections 7 and 16, not in this chunk. |
| RWB-S4-E5021-CON | R-08117 | DOR-RWB-S4-E5021-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No epic design record ID in the sources. A grep of the project found only directive escalation files. Section 14 text is not in this chunk, so no anchor exists to edit. |
| RWB-S4-E5021-CON | R-32550 | NEWAC-RWB-S4-E5021-CON-AC9 | 7; 16 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in this chunk, so their anchor lines cannot be matched. The proposed test is not specified in the sources. Resend sections 7 and 16 to apply. |
| RWB-S4-E5022-APP | R-27254 | CG-ALL-9570 | 7, 16 | Criteria and tests keep legacy job and decision-log wording | Partly applied: visible decision-log lines changed. The JOB-nn and job record lines are in section 7 and 16, outside this chunk. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (22)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17341 | RWB-S4-E5016-CON | CG-ALL-9408 | 12.2 | Declare the REST base of /api/recovery/case/v1 using the provider's base from the Document Index service table (rwb-case, P3). |
| CDC-17342 | RWB-S4-E5016-CON | CG-ALL-9409 | 12.2 | Declare the REST base of /api/recovery/decision/v1 using the provider's base from the Document Index service table (rwb-decision, P7). |
| CDC-17353 | RWB-S4-E5017-APP | CG-ALL-9421 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the provider named in the Document Index service table |
| CDC-17354 | RWB-S4-E5017-APP | CG-ALL-9422 | 12.2 | Declare REST base /api/recovery/integration/v1 for the provider named in the Document Index service table |
| CDC-17355 | RWB-S4-E5017-APP | CG-ALL-9423 | 12.2 | Declare REST base /api/recovery/agent/v1 for the provider named in the Document Index service table |
| CDC-17356 | RWB-S4-E5017-APP | CG-ALL-9424 | 12.2 | Declare REST base /api/recovery/decision/v1 for the provider named in the Document Index service table |
| CDC-17360 | RWB-S4-E5017-APP | DOR-RWB-S4-E5017-APP-8 | 12 | Add the base paths /api/recovery/source-data/v1, /api/recovery/integration/v1, /api/recovery/agent/v1 and /api/recovery/decision/v1 and the 4 further paths listed, with the operations this story consumes. |
| CDC-17369 | RWB-S4-E5017-CON | CG-ALL-9436 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the ACE asset and batch-status read of rwb-source-data (P1). |
| CDC-17370 | RWB-S4-E5017-CON | CG-ALL-9437 | 12.2 | Declare the REST base /api/recovery/integration/v1 for the bureau, registry and insurer search of rwb-integration (P2). |
| CDC-17371 | RWB-S4-E5017-CON | CG-ALL-9438 | 12.2 | Declare the REST base /api/recovery/agent/v1 for the trace plan of rwb-agent (P10). |
| CDC-17372 | RWB-S4-E5017-CON | CG-ALL-9439 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule package in force of rwb-decision (P7). |
| CDC-17374 | RWB-S4-E5017-CON | DOR-RWB-S4-E5017-CON-8 | 12.2 | Declare the REST bases the detcheck lists for the consumed rows (source-data, integration, agent, decision, plus the four further listed items). |
| CDC-17424 | RWB-S4-E5019-CON | CG-ALL-9498 | 12.2 | Declare the REST base of /api/recovery/case/v1 using the provider's REST base from the Document Index service table |
| CDC-17425 | RWB-S4-E5019-CON | CG-ALL-9499 | 12.2 | Declare the REST base of /api/recovery/decision/v1 using the provider's REST base from the Document Index service table |
| CDC-17446 | RWB-S4-E5020-APP | CG-ALL-9514 | 12.2 | Declare the REST base /api/recovery/case/v1 for the case read (P3 rwb-case) in the yaml REST bases. |
| CDC-17447 | RWB-S4-E5020-APP | CG-ALL-9515 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule package in force (P7 rwb-decision) in the yaml REST bases. |
| CDC-17458 | RWB-S4-E5020-CON | CG-ALL-9527 | 12.2 | Declare the REST base of /api/recovery/case/v1 from the Document Index service table |
| CDC-17459 | RWB-S4-E5020-CON | CG-ALL-9528 | 12.2 | Declare the REST base of /api/recovery/decision/v1 from the Document Index service table |
| CDC-17504 | RWB-S4-E5022-APP | CG-ALL-9561 | 12.2 | Declare REST base /api/recovery/payment/v1 for the match operation of RWB-P8-E4044-CON |
| CDC-17505 | RWB-S4-E5022-APP | CG-ALL-9562 | 12.2 | Declare REST base /api/recovery/payment/v1 for the apply operation of RWB-P8-E4049-CON |
| CDC-17525 | RWB-S4-E5022-CON | CG-ALL-9574 | 12.2 | Declare REST base /api/recovery/payment/v1 for rwb-payment (P8) so that RWB-P8-E4044-CON resolves. |
| CDC-17526 | RWB-S4-E5022-CON | CG-ALL-9575 | 12.2 | Declare REST base /api/recovery/payment/v1 for rwb-payment (P8) so that RWB-P8-E4049-CON resolves. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (21)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17345 | RWB-S4-E5016-CON | CG-ALL-9412 | 12.5 | Add an Activities row for recordJudgment, or map the story to a catalogued activity. |
| CDC-17346 | RWB-S4-E5016-CON | CG-ALL-9413 | 12.5 | Add activity armAppealWindow to the Activities sheet, or name a catalogued activity in section 12.5. |
| CDC-17375 | RWB-S4-E5017-CON | CG-ALL-9442 |  | Add activity traceAssets to the Activities sheet, or name a catalogued activity in §12.5 |
| CDC-17376 | RWB-S4-E5017-CON | CG-ALL-9443 |  | Add activity presentEnforcementDecision to the Activities sheet, or name a catalogued activity in §12.5 |
| CDC-17388 | RWB-S4-E5018-APP | CG-ALL-9453 | 12.5 | Add an openWritAction row to the Activities sheet. |
| CDC-17389 | RWB-S4-E5018-APP | CG-ALL-9454 | 12.5 | Add an Activities row for recordWritFiling: activity, the filing reported by the firm, task queue rwb-litigation |
| CDC-17390 | RWB-S4-E5018-APP | CG-ALL-9455 | 12.5 | Add an Activities row for armWritDeadline: activity, the timer of R-LIT-54, task queue rwb-litigation |
| CDC-17409 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-8 | 12.1; 12.5 | LitigationWorkflow row: state namespace rwb-recovery with task queue rwb-litigation. Add activities openLedAuction, recordAuctionRound and closeUnsoldLadder on task queue rwb-litigation. |
| CDC-17415 | RWB-S4-E5019-APP | CG-ALL-9481 | 12.5 | Add an Activities row for openLedAuction on task queue rwb-litigation, or name a catalogued activity to use instead. |
| CDC-17416 | RWB-S4-E5019-APP | CG-ALL-9482 | 12.5 | Add an Activities row for recordAuctionRound on task queue rwb-litigation, or name a catalogued activity to use instead. |
| CDC-17417 | RWB-S4-E5019-APP | CG-ALL-9483 | 12.5 | Add an Activities row for closeUnsoldLadder on task queue rwb-litigation, or name a catalogued activity to use instead. |
| CDC-17453 | RWB-S4-E5020-APP | CG-ALL-9518 | 12.5 | Add activity recordEnforcementDeferral (queue rwb-litigation, deferral step of RWB-S4-E5020-APP) to Activities, or use a catalogued activity. |
| CDC-17454 | RWB-S4-E5020-APP | CG-ALL-9519 | 12.5 | Add activity armReviewDate (queue rwb-litigation, review-date step of RWB-S4-E5020-APP) to Activities, or use a catalogued activity. |
| CDC-17464 | RWB-S4-E5020-CON | CG-ALL-9531 | 12.5 | Add activity recordEnforcementDeferral to the Activities sheet, or name a catalogued activity in its place |
| CDC-17465 | RWB-S4-E5020-CON | CG-ALL-9532 | 12.5 | Add activity armReviewDate to the Activities sheet, or name a catalogued activity in its place |
| CDC-17476 | RWB-S4-E5021-APP | CG-ALL-9539 | 12.5 | Add activity openPetition to the Activities sheet, or use a catalogued activity. |
| CDC-17477 | RWB-S4-E5021-APP | CG-ALL-9540 | 12.5 | Add activity recordDecision to the Activities sheet, or use a catalogued activity. |
| CDC-17484 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-8 | 12.5 | register activities openPetition, recordDecision and submitForApproval and the two further items of the detcheck; state the workflow ID form and start rule of LitigationWorkflow |
| CDC-17510 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-8 | 12.1 | Register matchEnforcementOutcome in Temporal Catalog v1; state Workflow ID form and start rule of LitigationWorkflow; declare the rwb-payment REST base |
| CDC-17512 | RWB-S4-E5022-APP | CG-ALL-9565 | 12.5 | Add activity matchEnforcementOutcome to the Activities sheet, or name a catalogued activity in its place. |
| CDC-17529 | RWB-S4-E5022-CON | CG-ALL-9578 | 12.5 | Add an Activities row for matchEnforcementOutcome on task queue rwb-litigation, or name the catalogued activity that replaces it. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (20)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17351 | RWB-S4-E5016-CON | CG-ALL-9415 | 16 | Add rows for TC-E5-016-01 to -06, TC-S4-E5016-CON-01 to -05 and TC-S4-E5016-CON-06, with Given, When and Then from the covered criteria. |
| CDC-17364 | RWB-S4-E5017-APP | CG-ALL-9430 | 16 | Add rows TC-E5-017-01 to TC-E5-017-06 with Given, When and Then copied from the criteria they cover. |
| CDC-17379 | RWB-S4-E5017-CON | DOR-RWB-S4-E5017-CON-12 | 12.7, 16 | Add the story test cases TC-E5-017-01 to -06 and TC-S4-E5017-CON-01 to -06 on tab Story test cases |
| CDC-17383 | RWB-S4-E5017-CON | CG-ALL-9445 | 16 | Add rows TC-E5-017-01 to -06 and TC-S4-E5017-CON-01 to -04, with Given, When and Then copied from the criterion each covers. |
| CDC-17391 | RWB-S4-E5018-APP | CG-ALL-9456 | 16 | Add rows TC-E5-018-01 to TC-E5-018-05 in the next version, with Given, When and Then copied from the criterion each covers |
| CDC-17401 | RWB-S4-E5018-CON | DOR-RWB-S4-E5018-CON-12 | 12.7, 16 | Add rows TC-E5-018-01 to -05 and TC-S4-E5018-CON-01 to -05; the boundary test TC-S4-E5018-CON-05 is added in section 16 |
| CDC-17403 | RWB-S4-E5018-CON | CG-ALL-9470 | 16 | Add rows for TC-E5-018-01 to TC-E5-018-05 and TC-S4-E5018-CON-01 to TC-S4-E5018-CON-04, with Given, When and Then copied from the criterion each covers. |
| CDC-17418 | RWB-S4-E5019-APP | CG-ALL-9485 | 16 | In the next version, add rows TC-E5-019-01 to TC-E5-019-05 to the Story test cases tab, with Given, When and Then copied from the criteria they cover. |
| CDC-17441 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-12 | 16 | Add rows for TC-E5-019-01 to TC-E5-019-05 and TC-S4-E5019-CON-01 to TC-S4-E5019-CON-06 under tab Story test cases. |
| CDC-17445 | RWB-S4-E5019-CON | CG-ALL-9506 | 16 | Add rows for TC-E5-019-01 to TC-E5-019-05 and TC-S4-E5019-CON-01 to TC-S4-E5019-CON-04, with Given, When and Then copied from the criterion each covers |
| CDC-17455 | RWB-S4-E5020-APP | CG-ALL-9520 | 16 | Add rows TC-E5-020-01 to TC-E5-020-06 to Story test cases in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-17468 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-12 | 16 | Add rows for TC-E5-020-01 to -06, TC-S4-E5020-CON-01 to -04 and new TC-S4-E5020-CON-05 and -06 |
| CDC-17471 | RWB-S4-E5020-CON | CG-ALL-9533 | 16 | Add rows for TC-E5-020-01 to -06 and TC-S4-E5020-CON-01 to -04 with Given, When and Then copied from the criterion each covers; also add TC-S4-E5020-CON-07 and -08 once the next version is cut. |
| CDC-17481 | RWB-S4-E5021-APP | CG-ALL-9544 | 16 | Add rows TC-E5-021-01 to -05 with Given, When and Then from their criteria; also add TC-E5-021-06 to -08 from section 16. |
| CDC-17495 | RWB-S4-E5021-CON | DOR-RWB-S4-E5021-CON-12 | 12.7, 16 | Add Story test cases rows for TC-E5-021-01 to 05, TC-S4-E5021-CON-01 to 04 and new TC-S4-E5021-CON-05. |
| CDC-17501 | RWB-S4-E5021-CON | CG-ALL-9551 | 16 | Add rows for TC-E5-021-01 to 05 and TC-S4-E5021-CON-01 to 04 in the next version, with Given, When and Then copied from the criterion each covers. |
| CDC-17513 | RWB-S4-E5022-APP | CG-ALL-9567 | 16 | Add rows TC-E5-022-01 to TC-E5-022-06 with Given, When and Then copied from the criteria they cover. |
| CDC-17514 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-12 | 16 | Add TC-E5-022-01 to TC-E5-022-10 to tab Story test cases under the same IDs with their Given, When and Then. |
| CDC-17531 | RWB-S4-E5022-CON | DOR-RWB-S4-E5022-CON-12 | 12.7, 16 | Add rows for TC-E5-022-01 to -06 and TC-S4-E5022-CON-01 to -06 under the IDs of section 16. |
| CDC-17537 | RWB-S4-E5022-CON | CG-ALL-9580 | 16 | Add rows for TC-E5-022-01 to TC-E5-022-06 and TC-S4-E5022-CON-01 to TC-S4-E5022-CON-04, with Given, When and Then copied from the criteria they cover. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (15)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17344 | RWB-S4-E5016-CON | CG-ALL-9407 | 11 | Record judgment_type as a process input and decision-record fact with no column, or record the owning object (GAP-2811; ASM-4651). |
| CDC-17349 | RWB-S4-E5016-CON | DOR-RWB-S4-E5016-CON-7 | 11 | Add a BR Field ID for each of the eight §11 data rows of this story (legal action, judgment, appeal window, hearing, case answer, decision record, rule rows, reference values). Until then Not specified in the source documents (DOR-RWB-S4-E5016-CON-7). |
| CDC-17361 | RWB-S4-E5017-APP | CG-ALL-9420 | 12.7 | Record decision_record as the platform library table created in rwb_litigation (DP-03), or map it to an existing name such as decision_log_id. |
| CDC-17365 | RWB-S4-E5017-APP | DOR-RWB-S4-E5017-APP-7 | 7, 11, 16 | Name decision_record as a PLT library object of rwb_litigation or as an LDM v9 entity, and align Data Classification v5. AC1 and AC4 wording fixed in the story. |
| CDC-17410 | RWB-S4-E5019-APP | CG-ALL-9474 | 4 | Record auction_price_basis as a request input element of the LED auction step with no column, or use the dictionary name. |
| CDC-17411 | RWB-S4-E5019-APP | CG-ALL-9475 | 4 | Record official_value as a request input element of the LED auction step with no column, or use the dictionary name. |
| CDC-17412 | RWB-S4-E5019-APP | CG-ALL-9476 | 4 | Record round_result as a request input element of the LED auction step with no column, or use the dictionary name. |
| CDC-17413 | RWB-S4-E5019-APP | CG-ALL-9477 | 4 | Record bid_amount as an auction request element with no column (BR5), or give the dictionary name of the bid amount. |
| CDC-17414 | RWB-S4-E5019-APP | CG-ALL-9478 | 11, 12.7 | Record decision_record as a platform library table created in rwb_litigation (DP-03), or give the dictionary name of the decision record. |
| CDC-17451 | RWB-S4-E5020-APP | CG-ALL-9512 | 4, 8, 11 | Record deferral_review_date as an operation input element of the enforcement deferral (BR5), or use its dictionary name. |
| CDC-17452 | RWB-S4-E5020-APP | CG-ALL-9513 | 11, 12.7 | Record decision_record as a PLT library object created in rwb_litigation (DP-03), or use its dictionary name. |
| CDC-17462 | RWB-S4-E5020-CON | CG-ALL-9525 | 11 | Record deferral_reason as a field, or name the dictionary field it maps to (or record the object in the owning document) |
| CDC-17463 | RWB-S4-E5020-CON | CG-ALL-9526 | 11 | Record deferral_review_date as a field, or name the dictionary field it maps to (or record the object in the owning document) |
| CDC-17475 | RWB-S4-E5021-APP | CG-ALL-9536 | 11 | Record decision_record as a platform library object created in rwb_litigation by the DP-03 library migration, or use the dictionary name. |
| CDC-17516 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-7 | 11 | Confirm decision_record as an entity or field of the PLT decision-record library in LDM v9 and Data Classification v5, or rename it in the story. |

### Epic design record (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17343 | RWB-S4-E5016-CON | DOR-RWB-S4-E5016-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S4 so the story can cite it. |
| CDC-17357 | RWB-S4-E5017-APP | DOR-RWB-S4-E5017-APP-14 | header | Record the signed epic design sign-off for RWB-S4-E5017-APP |
| CDC-17373 | RWB-S4-E5017-CON | DOR-RWB-S4-E5017-CON-14 | header | Record the signed epic design sign-off for RWB-S4-E5017-CON, then confirm it against the record. |
| CDC-17384 | RWB-S4-E5018-APP | DOR-RWB-S4-E5018-APP-14 | header | Confirm and record the signed epic design sign-off; no signed design is in the story or source documents. |
| CDC-17396 | RWB-S4-E5018-CON | DOR-RWB-S4-E5018-CON-14 |  | Record the signed epic design sign-off for RWB-S4-E5018-CON; the story and source documents record none. |
| CDC-17406 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-14 | n/a | Record the signed epic design sign-off for RWB-S4-E5019-APP in the epic design record. |
| CDC-17426 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-14 | find it | Record the signed epic design sign-off for RWB-S4-E5019-CON in the epic design record |
| CDC-17448 | RWB-S4-E5020-APP | DOR-RWB-S4-E5020-APP-14 | header | Confirm and record the signed epic design sign-off for RWB-S4-E5020-APP. |
| CDC-17460 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-14 | Header | Record the signed epic design sign-off for the epic of RWB-S4-E5020-CON |
| CDC-17472 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-14 | header | Record the signed epic design sign-off for EP05 and confirm it against this story. |
| CDC-17506 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-14 | - | Record the signed sign-off of the epic design for RWB-S4-E5022-APP |
| CDC-17527 | RWB-S4-E5022-CON | DOR-RWB-S4-E5022-CON-14 | header | Record the signed epic design sign-off so the Epic design item can be confirmed against it. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17420 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-7 | 11 | register or declare out of scope the four named elements (auction_price_basis, official_value, round_result, bid_amount) and the two further names the detcheck reports |
| CDC-17428 | RWB-S4-E5019-CON | CG-ALL-9491 | 11 | Use the dictionary name for auction_round, or record it as a non-column object in the owning document |
| CDC-17429 | RWB-S4-E5019-CON | CG-ALL-9492 | 11 | Use the dictionary name for auction_price_basis, or record it as a non-column object in the owning document |
| CDC-17430 | RWB-S4-E5019-CON | CG-ALL-9493 | 11 | Use the dictionary name for official_value, or record it as a non-column object in the owning document |
| CDC-17431 | RWB-S4-E5019-CON | CG-ALL-9494 | 11 | Record `round_result` as a dictionary field or name the dictionary term it maps to; the story (§11) already states it has no column. |
| CDC-17432 | RWB-S4-E5019-CON | CG-ALL-9495 | 11 | Record `bid_amount` as a dictionary field or name the dictionary term it maps to; the story (§11) already states it has no column. |
| CDC-17433 | RWB-S4-E5019-CON | CG-ALL-9496 | 11 | Record `auction_date` as a dictionary field or name the dictionary term it maps to; the story (§11) already states it has no column. |
| CDC-17434 | RWB-S4-E5019-CON | CG-ALL-9497 | 11 | Record `led_reference` as a dictionary field or name the dictionary term it maps to; the story (§11) already states it has no column. |
| CDC-17469 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-7 | 11 | Confirm deferral_reason and deferral_review_date as contract inputs with no LDM column (BR6), or add them as fields |
| CDC-17483 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-7 | 11 | name decision_record as an entity or field of LDM v9 or Data Classification v5, or confirm it is a PLT library object outside both |
| CDC-17491 | RWB-S4-E5021-CON | CG-ALL-9550 | 8 | Register decision_record as the PLT library table object applied in rwb_litigation, or name its dictionary field; owner role Data. |
| CDC-17496 | RWB-S4-E5021-CON | DOR-RWB-S4-E5021-CON-7 | 11 | Declare decision_record as an entity or field, or add it to the platform library entry the story names in section 11. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17347 | RWB-S4-E5016-CON | DOR-RWB-S4-E5016-CON-1 | 1 | Add 'tech lead' as a role name or code, or confirm the code the story should use; the story text stays as is. |
| CDC-17377 | RWB-S4-E5017-CON | DOR-RWB-S4-E5017-CON-1 | 1 | Register the role 'tech lead' (or its role code) so that §1 resolves to a role in the catalogue |
| CDC-17392 | RWB-S4-E5018-APP | DOR-RWB-S4-E5018-APP-6 | 10 | Add role SY-DATALOAD |
| CDC-17400 | RWB-S4-E5018-CON | DOR-RWB-S4-E5018-CON-1 | 1 | Add a role entry for the role named 'tech lead' used in section 1 of RWB-S4-E5018-CON, with its role code. |
| CDC-17419 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-6 | 10 | add role SY-DATALOAD, which section 10 names |
| CDC-17439 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-1 | 1 | Confirm the role code and name for the persona 'tech lead' of RWB-S4-E5019-CON, or record that it is not a system role. No Roles tab row (54 roles) carries that name. |
| CDC-17456 | RWB-S4-E5020-APP | DOR-RWB-S4-E5020-APP-6 | 10 | Confirm role SY-DATALOAD with its Litigation U right as TSD S4 T6.1 gives it, or add the role. Story side: section 10 now names the rwb-access check per operation. |
| CDC-17466 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-1 | 1 | Add 'tech lead' as a role name, or map the section 1 role to a role code already in the document |
| CDC-17492 | RWB-S4-E5021-CON | DOR-RWB-S4-E5021-CON-1 | 1 | Add a role code and name for 'contract owner of rwb-litigation (S4)', or confirm the existing role that matches it. |
| CDC-17515 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-6 | 10 | Add role SY-DATALOAD with the Litigation right TSD S4 T6.1 gives it, or the story drops it from section 10. |
| CDC-17530 | RWB-S4-E5022-CON | DOR-RWB-S4-E5022-CON-1 | 1 | Register tech lead as a role of rwb-litigation, or name the existing role code or name that §1 should use. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17362 | RWB-S4-E5017-APP | CG-ALL-9427 | 12.5 | Add the activity traceAssets on task queue rwb-litigation, or name a catalogued activity instead. |
| CDC-17363 | RWB-S4-E5017-APP | CG-ALL-9428 | 12.5 | Add the activity presentEnforcementDecision on task queue rwb-litigation, or name a catalogued activity instead. |
| CDC-17397 | RWB-S4-E5018-CON | CG-ALL-9467 | 12.5 | Add activity openWritAction (enforcement element in; record, legal action, instruction, case move and timer out) or name a catalogued activity. |
| CDC-17398 | RWB-S4-E5018-CON | CG-ALL-9468 | 12.5 | Add an Activities row for recordWritFiling, or the owner names a catalogued activity |
| CDC-17399 | RWB-S4-E5018-CON | CG-ALL-9469 | 12.5 | Add an Activities row for armWritDeadline, or the owner names a catalogued activity |
| CDC-17435 | RWB-S4-E5019-CON | CG-ALL-9502 | 12.5 | Add an activity row for `openLedAuction` (task queue rwb-litigation), or name a catalogued activity to replace it. |
| CDC-17436 | RWB-S4-E5019-CON | CG-ALL-9503 | 12.5 | Add an activity row for `recordAuctionRound` (task queue rwb-litigation), or name a catalogued activity to replace it. |
| CDC-17437 | RWB-S4-E5019-CON | CG-ALL-9504 | 12.5 | Add an activity row for `closeUnsoldLadder` (task queue rwb-litigation), or name a catalogued activity to replace it. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17368 | RWB-S4-E5017-APP | GAP-2818 | 8, 11 | Fix trace request and answer element names in the contract review; confirm the enforcement decision belongs to the writ, deferral and petition stories. |
| CDC-17382 | RWB-S4-E5017-CON | GAP-2818 | find it | Confirm the enforcement decision belongs to the writ, deferral and petition stories; trace element names fixed in contract review. |
| CDC-17486 | RWB-S4-E5021-APP | GAP-1885 | 10 | carry the five consumed contracts as non-blocking rows: RWB-P7-E2013-CON as C of wave 2, the case and partner contracts as built on fakes, RWB-P3-E1043-CON as C, and the DP-08 authorise guard as edge rule |
| CDC-17498 | RWB-S4-E5021-CON | GAP-1885 | 11 | Carry RWB-P7-E2013-CON as C of wave 2, the case and partner contracts as published contracts against their fakes, and RWB-P3-E1043-CON as C, all non-blocking. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17421 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-9 | 14 | align the wording of MSG-P1-001 with the standard or confirm the standard text for this message |
| CDC-17423 | RWB-S4-E5019-APP | CG-ALL-9484 | 14 | MSG-P1-001 wording changed to 'Today's load has not arrived.' |
| CDC-17443 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-9 | 14 | Reconcile the MSG-P1-001 text with the Standard v4 text; the story keeps the FSD wording unchanged. |

### RWB-S4-E5020-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17449 | RWB-S4-E5020-APP | DOR-RWB-S4-E5020-APP-21 | header | Bring build status to Done (currently Not started) before this story starts. |
| CDC-17450 | RWB-S4-E5020-APP | DOR-RWB-S4-E5020-APP-22 | header | Publish the contract fake library and record its published version against RWB-S4-E5020-CON. |
| CDC-17457 | RWB-S4-E5020-APP | GAP-2830 | 13 | Declare in the absence test that no judgment write, JUDGMENT_RECORDED move or enforcement task request is built in rwb-litigation; the judgment path is RWB-S4-E5016-APP's. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17478 | RWB-S4-E5021-APP | CG-ALL-9541 | 12.5 | Add a row for activity submitForApproval, or name a catalogued activity in section 12.5 instead. |
| CDC-17479 | RWB-S4-E5021-APP | CG-ALL-9542 | 12.5 | Add a row for activity announceCaseRoute, or name a catalogued activity in section 12.5 instead. |
| CDC-17480 | RWB-S4-E5021-APP | CG-ALL-9543 | 12.5 | Add a row for activity recordFiling, or name a catalogued activity in section 12.5 instead. |

### RWB-S4-E5022-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17507 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-21 | - | Reach build status Done with the contract published before this story starts |
| CDC-17508 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-22 | - | Publish a contract fake library version and record it as published |
| CDC-17509 | RWB-S4-E5022-APP | DOR-RWB-S4-E5022-APP-23 | - | Declare the contract version this story builds against |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17350 | RWB-S4-E5016-CON | GAP-1744 | 7 | Number LawsuitFiled, JudgmentRecorded and AuctionResult as catalogue rows on topic rwb.litigation.events.v1, keyed by case, consumers rwb-asset and rwb-case; EV ids by that change. |
| CDC-17535 | RWB-S4-E5022-CON | GAP-1744 | none | Add numbered event catalogue rows for LawsuitFiled, JudgmentRecorded and AuctionResult on rwb.litigation.events.v1, keyed by case, with the consumers the source rows give; EV numbers by catalogue change. |

### RWB-S4-E5017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17358 | RWB-S4-E5017-APP | DOR-RWB-S4-E5017-APP-21 | header | Bring the contract story build status to Done |
| CDC-17359 | RWB-S4-E5017-APP | DOR-RWB-S4-E5017-APP-22 | header | Record a published contract fake library version |

### RWB-S4-E5018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17385 | RWB-S4-E5018-APP | DOR-RWB-S4-E5018-APP-21 | header | Publish the contract and set its build status to Done. |
| CDC-17386 | RWB-S4-E5018-APP | DOR-RWB-S4-E5018-APP-22 | header | Publish the contract fake library and record its published version. |

### RWB-PLT-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17387 | RWB-S4-E5018-APP | CG-ALL-9450 | 12.7 | Record decision_record as a library table in its owning document, or use the LDM v9 dictionary name. |
| CDC-17511 | RWB-S4-E5022-APP | CG-ALL-9560 | Section 11 | Record decision_record in the library contract as the object created by the library migration in rwb_litigation, or use the LDM v9 name for it. |

### RWB-S4-E5018-APP; RWB-S4-E5018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17402 | RWB-S4-E5018-CON | GAP-2819 | 8 | Step D1 adds the four consumed rows (rwb-case ENFORCEMENT_DECISION and WRIT_AND_SEIZURE, rwb-partner instruction, rwb-decision LITIGATION rule package with R-LIT-54) as class C dependencies of both slices, or records that they build against the owners' documents and fakes. |
| CDC-17404 | RWB-S4-E5018-CON | GAP-2820 | Header | Requirement row set to Not specified in the source documents (GAP-2820); PRD reference left without a REQ ID |

### RWB-S4-E5019-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17407 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-21 | n/a | Build the contract story to Done and publish the contract, so its build status is Done. |
| CDC-17408 | RWB-S4-E5019-APP | DOR-RWB-S4-E5019-APP-22 | n/a | Publish a contract fake library version and record its version number. |

### RWB-S4-E5021-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17473 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-21 | header | Set build status to Done, as the contract must be published before this story starts. |
| CDC-17474 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-22 | 13 | Publish the contract fake library and record its version as published. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17482 | RWB-S4-E5021-APP | DOR-RWB-S4-E5021-APP-11 | 8 | Close Q-P2-04: state the P2 field list, or confirm that no P2 field is personal data, so that it matches BR7 (no personal data). |
| CDC-17502 | RWB-S4-E5021-CON | GAP-1886 | header | Add one requirement row for the petition taken to the approver at D7.5 and filed through the firm, then rewrite the requirement column of both stories. |

### RWB-P7-E2013-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17485 | RWB-S4-E5021-APP | GAP-1889 | 12.5 | publish the raise as a POST on the decision base with the approval row body and an answer carrying approval ID, level, limit version and due time, with its error set |
| CDC-17497 | RWB-S4-E5021-CON | GAP-1889 | 11 | Publish the approval raise as a POST on the decision base with its body, an answer carrying approval ID, level, limit version and due time, and its error set. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17490 | RWB-S4-E5021-APP | GAP-1887 | find it | Decide whether a legal action filing raises LawsuitFiled; name the publishing story in the LawsuitFiled row, or record that no story owns it. Both petition stories keep publishing nothing. |
| CDC-17503 | RWB-S4-E5021-CON | GAP-1887 | 9 | Decide whether filing a legal action raises LawsuitFiled and name the single publishing story in the catalogue row. Neither petition story publishes it until then. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17519 | RWB-S4-E5022-APP | GAP-1738 | 12.5 | Add rows for judgment, enforcement, auction round, pack, notice state, deferral and decision record with their key fields; keep the two existing legal_action and hearing rows as the only physical table names. |
| CDC-17532 | RWB-S4-E5022-CON | GAP-1738 | none | Add the six missing entity groups (judgment, enforcement record, auction round, pack, notice state, deferral and decision record) with key fields and fix no table name beyond legal_action and hearing. |

### OTHER:rwb-decision (P7) rule registry and approval contract (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17522 | RWB-S4-E5022-APP | GAP-1895 | 4 | Publish the rule rows R-LIT-51, R-LIT-65 and R-LIT-70, their LITIGATION package version and test cases, and name the approval operation and limit in the approval contract. |
| CDC-17536 | RWB-S4-E5022-CON | GAP-1895 | none | Publish rule rows R-LIT-51, R-LIT-65 and R-LIT-70 with package version and test cases for the LITIGATION package, and name the approval operation and limit in the approval contract. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17524 | RWB-S4-E5022-APP | GAP-1747 | find it | Record the owning service of SCR-18, SCR-19 and SCR-20 in the screen owner cell, with the composite route serving each. |
| CDC-17528 | RWB-S4-E5022-CON | GAP-1737 | header, 12.2 | Contract dependencies list the P8, P5 and P10 rows; the ALS and GL edge is not covered by a contract row and is Not specified in the source documents. |

### OTHER:Screen specifications for SCR-19 and SCR-20 (outside this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17348 | RWB-S4-E5016-CON | DOR-RWB-S4-E5016-CON-10 |  | Add empty, loading, error and no-access states for SCR-19 and SCR-20 |

### OTHER:Recovery Workbench plan reqs list (step D1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17352 | RWB-S4-E5016-CON | GAP-2813 | header | Requirement row marked Not specified in the source documents (GAP-2813); PRD reference cell updated to match. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17366 | RWB-S4-E5017-APP | GAP-2815 | 11, 13 | Publish the asset and batch-status read on rwb-source-data's contract with its fake; add class C row RWB-P1-E5017-C to both slices in step D1; record the refused v_ace_* grant. |

### OTHER:Dependency plan of RWB-E5-017 and the rwb-integration and rwb-agent contracts (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17367 | RWB-S4-E5017-APP | GAP-2816 | 8, 13 | Add the search as a consumed contract of rwb-integration and the trace plan as a consumed contract of rwb-agent; publish operations and fakes; add two class C rows in step D1. |

### RWB-S4-E5017-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17378 | RWB-S4-E5017-CON | DOR-RWB-S4-E5017-CON-10 |  | Add empty, loading, error and no-access states to SCR-19 and SCR-20 |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17380 | RWB-S4-E5017-CON | GAP-2815 | find it | Publish the asset and batch-status read on rwb-source-data's contract with its fake; add class C row RWB-P1-E5017-C to both slices in step D1; record the refused v_ace_* grant in the Service Contract Catalog. |

### OTHER:rwb-integration contract (P2); OTHER:rwb-agent contract (P10) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17381 | RWB-S4-E5017-CON | GAP-2816 | find it | Publish the search operation on rwb-integration and the trace-plan operation on rwb-agent with their fakes; add two class C rows to both slices in step D1. |

### API:(service not named); OTHER:P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17393 | RWB-S4-E5018-CON | CG-ALL-9462 | 12.2 | Declare REST base /api/recovery/case/v1 for rwb-case (P3), as in the service table of aisdlc/.github/contexts/realignment-v5-context.md line 151. The consumed verb stays a placeholder. |

### API:(service not named); OTHER:S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17394 | RWB-S4-E5018-CON | CG-ALL-9463 | 12.2 | Declare REST base /api/recovery/partner/v1 for rwb-partner (S9), as in the service table of aisdlc/.github/contexts/realignment-v5-context.md line 167. The consumed verb stays a placeholder. |

### API:(service not named); OTHER:P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17395 | RWB-S4-E5018-CON | CG-ALL-9464 | 12.2 | Declare REST base /api/recovery/decision/v1 for rwb-decision (P7), as in the service table of aisdlc/.github/contexts/realignment-v5-context.md line 155. The consumed verb stays a placeholder. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17405 | RWB-S4-E5018-CON | GAP-2825 | 8 | Mark the Endpoints table of RWB-E5-018 incomplete for this key, since it lists POST and GET only and omits API-S4-004 PATCH. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17422 | RWB-S4-E5019-APP | GAP-1744 | 13 | number the rows LawsuitFiled, JudgmentRecorded and AuctionResult on rwb.litigation.events.v1 in the event catalogue, keyed by case; EV numbers come from that change |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17427 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-8 | 12.1, 12.5 | Section 12.5 carries the workflow-ID placeholder; section 2 duplicate still to be removed |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; OTHER:test data owner (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17438 | RWB-S4-E5019-CON | CG-ALL-9507 | 12.8 | Seventh fake row removed; the source of test data is not given by the story |

### OTHER:Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17440 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-10 | 14, 15 | Screen states named as Not specified; no answers invented |

### OTHER:rwb-access API contract (authorise operation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17442 | RWB-S4-E5019-CON | DOR-RWB-S4-E5019-CON-6 | 10 | Publish the authorise operation name and its DP-08 call for the three operations. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17444 | RWB-S4-E5019-CON | GAP-1744 | 11 | Add numbered EV rows for LawsuitFiled, JudgmentRecorded and AuctionResult on rwb.litigation.events.v1, keyed by the case. |

### API:(service not named); OTHER:catalog task queue entry for LitigationWorkflow) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17461 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-8 | 12.1 | Add the bases /api/recovery/case/v1 and /api/recovery/decision/v1; align the LitigationWorkflow task queue to rwb-litigation in namespace rwb-recovery as story header L43 states. |

### RWB-S4-E5020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17467 | RWB-S4-E5020-CON | DOR-RWB-S4-E5020-CON-10 | 10 | Add empty, loading, error and no-access states for SCR-20 |

### OTHER:Recovery Workbench Business Requirements Program v5 (DL10) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17470 | RWB-S4-E5020-CON | GAP-1748 | 14 | Supply Thai wording, field-level text for MSG-GEN-001 and the approver for the S4 message wording; FSD IDs and English wording stay as written |

### OTHER:Temporal design (slides 12 and 13) and the workflow catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17487 | RWB-S4-E5021-APP | GAP-1888 | 12.5 | name the child workflow type, its workflow ID convention, its queue registration, and whether the 5-working-day clock is the child's durable timer, in the workflow catalogue |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:P4 role model (D7.5 approver role); OTHER:TSD S4 v2 (legal_action index rows); 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:platform problem document (400 answer) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17488 | RWB-S4-E5021-APP | GAP-1890 | 10 | publish the bankruptcy test as versioned reference rows; name the D7.5 approver role; add legal_action index rows by case_id; decide the refused-petition status; state the 400 answer for an unparseable body on the three operations |

### OTHER:Epics 3 to 8 PRD (EP05) and the S4 module trace (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17489 | RWB-S4-E5021-APP | GAP-1886 | find it | Add one requirement row for FEAT-LIT-21 covering the bankruptcy petition as a legal action taken to the approver at D7.5 and filed through the firm; then rewrite the requirement column of both stories. |

### OTHER:P3 screen specification (SCR-19; OTHER:SCR-20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17493 | RWB-S4-E5021-CON | DOR-RWB-S4-E5021-CON-10 | 1 | Declare empty, loading, error and no-access states for SCR-19 and SCR-20. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17494 | RWB-S4-E5021-CON | DOR-RWB-S4-E5021-CON-11 | 8 | Align the personal-data class of the P2 fields flagged by detcheck with BR11 (no personal data carried). |

### OTHER:Workflow catalogue (D7.5 approval child workflow row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17499 | RWB-S4-E5021-CON | GAP-1888 | 7 | Name the child workflow type, its workflow ID convention, queue registration and whether the 5-working-day clock is its durable timer; then point the AC at that row. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:TSD S4 v2; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx; OTHER:P4 role model; OTHER:platform problem envelope (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17500 | RWB-S4-E5021-CON | GAP-1890 | 11 | Publish the bankruptcy test rows with version, name the D7.5 approver role, add the legal_action lookup index, decide the refused-petition status, and state the 400 answer. |

### OTHER:Wave 3 harness (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17517 | RWB-S4-E5022-APP | GAP-1891 | 13 | Record which legacy balance application maps to which P8 operation (matchPayments, postProceeds) against RWB-P8-E4044-CON and RWB-P8-E4049-CON. |

### OTHER:(no target) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17518 | RWB-S4-E5022-APP | GAP-1892 | 13 | Section 13 states no event is consumed (GAP-1892); the ProceedsMatched consumer list belongs to the P8 event catalogue. |

### OTHER:FSD S4 (A2.1.4.1 to A2.22.4.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17520 | RWB-S4-E5022-APP | GAP-1743 | 7 | Replace the generic three-column criteria and No alternate path / No background event rows with one step-specific criterion per feature, citing the FSD row as evidence. |

### OTHER:FSD S4 (A2.6.3.2 to A2.21.3.2 field catalogs) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17521 | RWB-S4-E5022-APP | GAP-1739 | 12.5 | Retype legal_action.case_id from uuid to varchar(255) as a business key with no foreign key, keeping the field name. |

### OTHER:Recovery Workbench Business Requirements Program v5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17523 | RWB-S4-E5022-APP | GAP-1641 | find it | Add section 5.11 (REQ-S4-010) to the note after the program requirement trace in section 11. |

### OTHER:03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5/Recovery Workbench FSD S4 L (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17533 | RWB-S4-E5022-CON | GAP-1743 | find it | Replace the generic main-success criterion of each of the 22 features with a step-specific criterion from its named rules, cite the FSD row, and state the alternate flow and background event where a feature names one. |

### OTHER:Recovery Workbench FSD S4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17534 | RWB-S4-E5022-CON | GAP-1739 | none | Type legal_action.case_id as varchar(255) business key with no foreign key in every field catalogue (A2.6.3.2 to A2.21.3.2), keeping the field name. |

### OTHER:Screen Specifications v1 (SCR-19) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17538 | RWB-S4-E5022-CON | CG-ALL-9581 | 15 | Add empty, loading, error and no access states for SCR-19; the story takes its states from the specification. |

### OTHER:Screen Specifications v1 (SCR-20) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17539 | RWB-S4-E5022-CON | CG-ALL-9582 | 15 | Add empty, loading, error and no access states for SCR-20; the story takes its states from the specification. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17540 | RWB-S4-E5022-CON | GAP-1747 | find it | Record that SCR-18, SCR-19 and SCR-20 are served by gateway-bff composite routes, with this service answering the legal-action part; record the screen owner cell with the edge work. |

### OTHER:FSD S4 v3 (VR-S4-022-1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-17541 | RWB-S4-E5022-CON | GAP-1897 | find it | Assign VR-S4-022-1 to rwb-payment and rwb-source-data where the ACE data product is read, not to rwb-litigation, unless the solution architect decides otherwise. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1641 | The program BRD note on P8 requirements leaves out the enforcement proceeds requirement it also cites | Business analyst, P8 | Resolved (directive) |
| GAP-1736 | FSD S4 reads the ACE views and the batch-status view directly, while Architecture v5 allows only rwb-source-data to read them and the connection matrix gives S4 no cell to P1 | Solution architect | Resolved (directive) |
| GAP-1737 | The connection matrix gives S4 no cell to rwb-document, rwb-payment or rwb-agent, while the FSD names the document hub, ALS and GL and the model gateway | Solution architect | Resolved (directive) |
| GAP-1738 | The Ownership Map gives rwb-litigation two tables, while Architecture v5 gives the schema judgments, enforcement and the LED auction ladder and the FSD holds notice, pack and deferral state | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1739 | legal_action.case_id is a uuid in the FSD, while ADR-014 and DP-01 forbid a cross-schema foreign key and require a varchar(255) business key | Data architect | Resolved (directive) |
| GAP-1742 | Thirty-two of the seventy-nine R-LIT rules are named in the FSD and the litigation rule package is Phase 2 | Center of excellence analyst | Resolved (directive) |
| GAP-1743 | Every FSD acceptance criterion is the same generic sentence and there is no alternate flow and no background event for any of the twenty-two features | Business analyst, S4 | Resolved (directive) |
| GAP-1744 | LawsuitFiled, JudgmentRecorded and AuctionResult have no EV number and no catalogue row | Solution architect | Resolved (directive) |
| GAP-1747 | The three S4 screens have no owner cell in the v5 screen matrix, and SCR-18's first-in is Epic 2 | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-1749 | The sources state no litigation, hearing or enforcement volume for this module, and no release date other than the program release plan | Solution architect | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1886 | The legacy master carries no requirement identifier for RWB-E5-021, so both stories trace to the feature only | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1887 | The catalogue lists LawsuitFiled on the litigation topic but assigns no story to it, so the filing of a bankruptcy petition is tied to no event | Solution architect, S4 rwb-litigation, with the event platform owner and the rwb-case and rwb-asset analysts | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1888 | The D7.5 approval child workflow has no type name, workflow ID or queue registration beyond the queue of rwb-decision | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the Temporal platform owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1889 | The approval contract publishes no operation that raises an approval item, so the petition's take-to-the-approver shape has no owner | Solution architect, P7 rwb-decision, with the S4 rwb-litigation architect and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1890 | Five values of the petition exist in no source: the bankruptcy test, the approver role at D7.5, the index set of legal_action, the status of a refused petition and the 400 answer | Business analyst and solution architect, S4 rwb-litigation, with the P4 rwb-access analyst for the approver role and the DBA for the index set | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1891 | The target gives the matching, the proceeds and the balance application to rwb-payment while the legacy story gives them to S4, and the plan adds no contract dependency for them | Solution architect | Resolved (directive) |
| GAP-1892 | ProceedsMatched does not list rwb-litigation as a consumer, so the payment fact cannot arrive as an event | Solution architect | Resolved (directive) |
| GAP-1893 | The legacy story runs unattended while the target trigger is one step of LitigationWorkflow that no source names | Solution architect | Resolved (directive) |
| GAP-1894 | The legacy story master carries no requirement ID for this feature | Solution architect | Resolved (directive) |
| GAP-1895 | The rule rows of R-LIT-51, R-LIT-65 and R-LIT-70 and the D7 approval of a close are governed in rwb-decision but are not listed for this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1896 | The LED round result, the percentage of official value, the proceeds source code and three operation names have no field or name in any source | Solution architect | Resolved (directive) |
| GAP-1897 | VR-S4-022-1 tests the freshness of the ACE batch of the source, and rwb-litigation holds no ACE view to test it | Solution architect | Resolved (directive) |
| GAP-2811 | The judgment type, the dismissal, the appeal window and the enforcement task have no column, no list value and no owned row, and the delivery that opens them has no source | S4 rwb-litigation service owner with the P3 rwb-case owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-2812 | The trigger of the step, the v_ace_lawsuit read of the feature extract and the three consumed owner contracts have no single source, and no contract row is planned | S4 rwb-litigation service owner with the solution architect and the P2 rwb-integration owner | Resolved (directive) |
| GAP-2813 | The legacy key carries no requirement id in the story master and the plan carries no requirement for either slice | S4 rwb-litigation service owner with the business analyst | Resolved (directive) |
| GAP-2815 | The ACE asset and data-product read of the trace has no grant to S4, no published operation and no contract row in the plan | S4 rwb-litigation service owner with the P1 rwb-source-data owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2816 | The NCB, registry and insurer search and the agent trace plan have no dependency row, no adapter in this service and no published operation | S4 rwb-litigation service owner with the P2 rwb-integration and P10 rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2817 | The trigger of the trace step is not stated by any source and no event, subscription or Schedule is declared for it | S4 rwb-litigation service owner with the solution architect | Resolved (directive) |
| GAP-2818 | The trace result, the trace request elements and the enforcement-decision boundary have no table, no field list and no owning story in the sources | S4 rwb-litigation service owner with the business analyst and the data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2819 | The four consumed owner operations of the writ step are named by no source and the plan carries no contract dependency for either slice | S4 rwb-litigation service owner with the P3 rwb-case, S9 rwb-partner and P7 rwb-decision owners | Resolved (directive) |
| GAP-2820 | The legacy key carries no requirement id in the story master and the plan carries no requirement for either slice | S4 rwb-litigation service owner with the business analyst | Resolved (directive) |
| GAP-2821 | LOV-LEGAL-TYPE names no writ value and legal_action carries no writ, seizure or deadline column | S4 rwb-litigation service owner with the data steward | Resolved (directive) |
| GAP-2824 | The case route state, the traced asset and the economic test that R-LIT-54 turns on have no home in this service | S4 rwb-litigation service owner with the P3 rwb-case owner and the owner of RWB-S4-E5017-APP | Resolved (directive) |
| GAP-2825 | The legacy Endpoints table names two operations while the flow of the feature and TSD appendix T-A.1 need a third, the update | S4 rwb-litigation service owner with the solution architect | Resolved (directive) |
| GAP-2826 | The auction ladder facts, the ladder states, the trigger, the three consumed owner contracts and the requirement id have no single source in the app slice of RWB-E5-019 | S4 rwb-litigation service owner with the business analyst and the data steward | Resolved (directive) |
| GAP-2827 | The contract slice of RWB-E5-019 fixes an auction element, a timer element, three consumed owner operations and a baseline status that no source gives in full | Tech lead of rwb-litigation with the solution architect and the owners of rwb-case and rwb-decision | Resolved (directive) |
| GAP-2828 | The coded deferral reason, its code list and the review date have no column, no field list and no list of values in any source | Business analyst of EP05 with the data steward of S4 and the reference-data owner of rwb-case | Resolved (directive) |
| GAP-2829 | Three consumed owner contracts of the deferral step have no dependency row, and the plan gives both stories no contract or integration dependency | Solution architect with the P3 and P7 owners | Resolved (directive) |
| GAP-2830 | R-LIT-44 and the judgment write are named by two legacy keys, so the judgment criterion of RWB-E5-020 is a regression and not a second build | Solution architect with the tech lead of S4 and the business analyst of EP05 | Resolved (directive) |
| GAP-2831 | The Workbench scheduler of R-LIT-55 has no equivalent in the target, and DP-10 is not in the pattern set of this key | Solution architect with the workflow platform owner and the tech lead of S4 | Resolved (directive) |
| GAP-2832 | SCR-20 carries no deferred state and no source gives a screen field list for the reason and the review date | Solution architect with the edge owner and the business analyst of EP05 | Resolved (directive) |
| GAP-2833 | The legacy master carries no requirement identifier for RWB-E5-020, so both stories trace to the feature and to the nearest module requirement | Business analyst of EP05 and the PRD owner of the epic | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S4-E5017-APP | new AC without TC row | 479 | AC5 is new and no section 16 row covers it |
| RWB-S4-E5017-APP | new AC without TC row | 479 | AC6 is new and no section 16 row covers it |
| RWB-S4-E5019-APP | new AC without TC row | 480 | AC4 is new and no section 16 row covers it |
| RWB-S4-E5019-APP | new AC without TC row | 480 | AC5 is new and no section 16 row covers it |
| RWB-S4-E5020-APP | new AC without TC row | 461 | AC5 is new and no section 16 row covers it |
| RWB-S4-E5020-APP | new AC without TC row | 461 | AC6 is new and no section 16 row covers it |
| RWB-S4-E5020-APP | new AC without TC row | 461 | AC7 is new and no section 16 row covers it |
