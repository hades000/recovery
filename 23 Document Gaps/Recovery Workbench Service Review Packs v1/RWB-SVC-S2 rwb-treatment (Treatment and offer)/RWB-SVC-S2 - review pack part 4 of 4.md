# RWB-SVC-S2 rwb-treatment (Treatment and offer) - review pack, part 4 of 4 (RWB-S2-E3013-CON to RWB-S2-E3018-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 11 |
| Resolved in the stories | 177 |
| Cross-document (pending in another document) | 141 |
| Not applied (value not in the sources) | 16 |
| Open business decisions | 10 |
| Register gaps linked | 26 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S2-E3013-CON | 15 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3013 CON Check encumbrance and eligibility before negotiation - contract v2.md |
| RWB-S2-E3014-APP | 20 | 7 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3014 APP Unlock the asset as a non performing asset by rule v2.md |
| RWB-S2-E3014-CON | 16 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3014 CON Unlock the asset as a non performing asset by rule - contract v2.md |
| RWB-S2-E3015-APP | 20 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3015 APP Capture the collateral inspection in the field v2.md |
| RWB-S2-E3015-CON | 12 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3015 CON Capture the collateral inspection in the field - contract v2.md |
| RWB-S2-E3016-APP | 16 | 16 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3016 APP Set up a deed in lieu buy-back rental v2.md |
| RWB-S2-E3016-CON | 17 | 7 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3016 CON Set up a deed in lieu buy-back rental - contract v2.md |
| RWB-S2-E3017-APP | 17 | 23 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3017 APP Release the collateral after settlement v2.md |
| RWB-S2-E3017-CON | 14 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3017 CON Release the collateral after settlement - contract v2.md |
| RWB-S2-E3018-APP | 16 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3018 APP Generate the treatment document set v2.md |
| RWB-S2-E3018-CON | 14 | 12 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3018 CON Generate the treatment document set - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S2-E3013-CON | R-12333 | CG-ALL-8708 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3014-APP | R-12340 | CG-ALL-8718 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3016-CON | R-12365 | CG-ALL-8772 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3017-APP | R-12373 | CG-ALL-8788 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3017-CON | R-12376 | CG-ALL-8797 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3018-APP | R-12384 | CG-ALL-8808 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3018-CON | R-12387 | CG-ALL-8815 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S2-E3015-APP, RWB-S2-E3015-CON | R-23383 | GAP-2678 | Register gap | Business owner of module S2 with the solution architect of rwb-treatment and the rwb-document owner | The inspection capture has no entity, no fields, no screen and no event, its two legacy rule rows belong to other steps of the module, and no requirement maps to FEAT-TRT-15 | Hold the six inspection elements on the treatment row with no new table, carry the checklist, the photographs and the bills as rwb-document references, let the field app reach the service through the gateway-bff composite route with right U of the treatment roles, keep AC2 and AC3 verbatim and hand R-RES-12 and R-SET-09 to the restructure and settlement slices, report the inspection completion on the case signal with no event, and leave the requirement mapping open until a requirement is written for FEAT-TRT-15. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON, RWB-S2-E3018-APP, RWB-S2-E3018-CON | R-29105 | GAP-1714 | Register gap | Product Owner | No approval is recorded for the requirements this PRD states | Keep the document at status Draft, leave the approval table empty, and treat the missing approval as an assumption rather than an answer; the gate is cleared by the Product Owner and the FDA after this run. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S2-E3013-CON | R-19447 | DOR-RWB-S2-E3013-CON-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Section 15 text (about lines 375-383) is not in this chunk, so no exact old text to anchor the edit. Story not edited. Rerun with section 15 included. |
| RWB-S2-E3014-APP | R-12341 | CG-ALL-8719 | 7 | Criteria and test data read ACE views directly | The Given lines that read the ACE view are in section 7, which is not in this chunk. Section 12.8 has no v_ace_ read. Needs section 7 text. |
| RWB-S2-E3014-APP | R-19456 | DOR-RWB-S2-E3014-APP-10 | 7, 16 | Definition of Ready item 10 Screens and states: Partial | SCR-14 and SCR-16 empty, loading, error and no-access states are Not specified in the source documents (CG-ALL-8721, CG-ALL-8722); no criteria can be written without invention. |
| RWB-S2-E3014-APP | R-19459 | DOR-RWB-S2-E3014-APP-18 | 7 | Definition of Ready item 18 Open decisions: Partial | DL10 and ASM-2250, ASM-2357, ASM-2377, ASM-2863 sit in a section not in this chunk. The exact current text is needed to edit it. Needs that section. |
| RWB-S2-E3016-APP | R-19491 | DOR-RWB-S2-E3016-APP-15 | find it | Definition of Ready item 15 INVEST: Partial | INVEST text is not in this chunk. The Size row says the squad sets it, so a two-week fit cannot be stated without inventing a value. |
| RWB-S2-E3016-APP | R-19492 | DOR-RWB-S2-E3016-APP-18 | find it | Definition of Ready item 18 Open decisions: Partial | DL10 and ASM-2250, ASM-2357, ASM-2377, ASM-2863 are not in this chunk, so the open-decision text cannot be anchored or edited. |
| RWB-S2-E3016-CON | R-07797 | DOR-RWB-S2-E3016-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed EP03 epic design record found. Searched all .md sources; only the process rule (DoR v3 item 14, ways-of-working v3) appears. Cannot record sign-off. |
| RWB-S2-E3016-CON | R-19499 | DOR-RWB-S2-E3016-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-14 and SCR-16 text is not in this chunk, so the empty, loading, error and no-access states cannot be added here. |
| RWB-S2-E3016-CON | R-26992 | CG-ALL-8775 |  | Story cites document versions that are not the highest | The API Specification v4 citation is not in this chunk, so its old text cannot be copied and changed to v5 here. |
| RWB-S2-E3017-APP | R-19511 | DOR-RWB-S2-E3017-APP-18 | 18 | Definition of Ready item 18 Open decisions: Partial | Open decisions are in section 18, outside this chunk, so no anchor text to edit. Could not find DL10 with ASM-2250 in the 22 folder to confirm the link. |
| RWB-S2-E3017-APP | R-32251 | NEWAC-RWB-S2-E3017-APP-AC6 | 8 | AC6: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | A new AC needs section 7 and section 16 anchor text, which is not in this chunk. BR4 and BR7 have no source for a test, so a criterion would invent values. |
| RWB-S2-E3017-CON | R-12377 | CG-ALL-8798 | 7; 12.8 | Criteria and test data read ACE views directly | The current text of AC1 and AC5 is not in this chunk, so no line can be copied exactly. The scratch copy (mp/out, lines 118-165) has no ACE-read Given or test-data line. Needs the current story text. |
| RWB-S2-E3018-APP | R-07810 | DOR-RWB-S2-E3018-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or project sources (prior search of *.md). Sign-off would be invented; needs the epic design record. |
| RWB-S2-E3018-APP | R-07813 | DOR-RWB-S2-E3018-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | No published contract fake library version in the project sources (prior search of *.md). Stating one would invent it; needs the published version. |
| RWB-S2-E3018-APP | R-19530 | DOR-RWB-S2-E3018-APP-18 | 9 | Definition of Ready item 18 Open decisions: Partial | DL10 row and section 9 text are outside this chunk, so no exact old text to edit. Add the DL10 open-decision line with ASM-2250, ASM-2357, ASM-2377, ASM-2863 in the chunk that holds section 9. |
| RWB-S2-E3018-CON | R-07816 | DOR-RWB-S2-E3018-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record exists in the story or sources; a sign-off cannot be confirmed without inventing one. Searched all project .md files for epic design sign-off; only the same DoR item 14 Fail line appears. |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16531 | RWB-S2-E3013-CON | DOR-RWB-S2-E3013-CON-12 | 16 | Add test case rows TC-S2-E3013-CON-01 to TC-S2-E3013-CON-05 from section 16 to Test Cases v8. |
| CDC-16536 | RWB-S2-E3013-CON | CG-ALL-8707 | 16 | Add rows for TC-S2-E3013-CON-01 to -05, and -06 to -08 once added, with Given, When and Then copied from the criterion each covers. |
| CDC-16542 | RWB-S2-E3014-APP | CG-ALL-8717 | 16 | Add rows TC-E3-014-01 to TC-E3-014-06 to Story test cases with Given, When and Then copied from the criterion each covers. |
| CDC-16550 | RWB-S2-E3014-CON | DOR-RWB-S2-E3014-CON-12 | 16 | Add rows TC-S2-E3014-CON-01 to TC-S2-E3014-CON-07 with Given, When and Then copied from AC1 to AC7 of this story. |
| CDC-16552 | RWB-S2-E3014-CON | CG-ALL-8729 | 16 | Add rows TC-S2-E3014-CON-01 to TC-S2-E3014-CON-07 with Given, When and Then copied from AC1 to AC7 of this story. |
| CDC-16563 | RWB-S2-E3015-APP | CG-ALL-8740 | 16 | Add rows TC-E3-015-01 to TC-E3-015-06 with Given, When and Then copied from AC1 to AC4 and the access and Principle 5 criteria |
| CDC-16571 | RWB-S2-E3015-CON | DOR-RWB-S2-E3015-CON-12 | 16 | Register TC-S2-E3015-CON-01 to TC-S2-E3015-CON-06 in Test Cases v8 |
| CDC-16573 | RWB-S2-E3015-CON | CG-ALL-8748 | 16 | Add rows TC-S2-E3015-CON-01 to TC-S2-E3015-CON-05 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-16588 | RWB-S2-E3016-APP | CG-ALL-8761 | 16 | Add rows TC-E3-016-01 to TC-E3-016-05 with Given, When and Then copied from the criterion each covers. |
| CDC-16597 | RWB-S2-E3016-CON | DOR-RWB-S2-E3016-CON-12 | 16 | Register TC-S2-E3016-CON-01 to TC-S2-E3016-CON-06 in Test Cases v8 |
| CDC-16598 | RWB-S2-E3016-CON | CG-ALL-8771 | 16 | Add rows for TC-S2-E3016-CON-01 to TC-S2-E3016-CON-05 with Given, When and Then copied from AC1 to AC6 of section 7 of RWB-S2-E3016-CON. |
| CDC-16613 | RWB-S2-E3017-APP | CG-ALL-8786 | 16 | Add rows TC-E3-017-01 to TC-E3-017-06 with Given, When and Then copied from the criteria they cover. |
| CDC-16616 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-12 | 16 | TC-E3-017-07 to -10 rows are in the story; the Test Cases v8 change is outstanding. |
| CDC-16630 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-12 | 16 | Register TC-S2-E3017-CON-01 to TC-S2-E3017-CON-06 with their Covers and Level from section 16, and the new TC-S2-E3017-CON-07. |
| CDC-16635 | RWB-S2-E3017-CON | CG-ALL-8796 | 16 | Add rows TC-S2-E3017-CON-01 to TC-S2-E3017-CON-06 with Given, When and Then copied from the criterion each covers. |
| CDC-16644 | RWB-S2-E3018-APP | CG-ALL-8807 | 16 | Add rows TC-E3-018-01 to TC-E3-018-06 with Given, When and Then copied from the criterion each covers. |
| CDC-16658 | RWB-S2-E3018-CON | DOR-RWB-S2-E3018-CON-12 | 16 | Register TC-S2-E3018-CON-01 to TC-S2-E3018-CON-06 in Test Cases v8. |
| CDC-16662 | RWB-S2-E3018-CON | CG-ALL-8814 | 16 | Add rows TC-S2-E3018-CON-01 to TC-S2-E3018-CON-05 with Given, When and Then copied from the criteria they cover. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (18)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16541 | RWB-S2-E3014-APP | CG-ALL-8716 | 12.5 | Add activity recordAndApply to the Activities sheet, or name a catalogued activity in its place. |
| CDC-16553 | RWB-S2-E3015-APP | CG-ALL-8734 | 12.5 | Task queue rwb-treatment matches the catalog. The namespace rwb-recovery difference is not settled by any source and needs the catalog. |
| CDC-16557 | RWB-S2-E3015-APP | DOR-RWB-S2-E3015-APP-8 | 12.5 | Add Activities rows for attachInspectionCaptures, recordInspection and the two further activities in the detcheck. |
| CDC-16576 | RWB-S2-E3016-APP | CG-ALL-8753 | 12.5 | Add a Workflows row for TreatmentWorkflow (rental stage) with its task queue and contract element, or name the catalogued workflow that replaces it. |
| CDC-16580 | RWB-S2-E3016-APP | DOR-RWB-S2-E3016-APP-8 | 12.5 | Add Workflows and Activities rows for every name in the detcheck list, including TreatmentWorkflow (rental stage), openRentalRecord and setUpAutoDebit, and the three further names. |
| CDC-16582 | RWB-S2-E3016-APP | CG-ALL-8754 | 12.5 | Add an Activities row for openRentalRecord with task queue rwb-treatment and its contract element. |
| CDC-16583 | RWB-S2-E3016-APP | CG-ALL-8755 | 12.5 | Add an Activities row for setUpAutoDebit with task queue rwb-treatment and its contract element. |
| CDC-16584 | RWB-S2-E3016-APP | CG-ALL-8756 | 12.5 | Add activity followRentalReceipts to the Activities sheet, or the story uses a catalogued activity instead. |
| CDC-16585 | RWB-S2-E3016-APP | CG-ALL-8757 | 12.5 | Add activity evaluateRentalArrears to the Activities sheet, or the story uses a catalogued activity instead. |
| CDC-16586 | RWB-S2-E3016-APP | CG-ALL-8758 | 12.5 | Add activity recordAndApply to the Activities sheet, or the story uses a catalogued activity instead. |
| CDC-16587 | RWB-S2-E3016-APP | CG-ALL-8759 | 12.5 | Add activity reportRentalOutcome to the Activities sheet, or the story uses a catalogued activity instead. |
| CDC-16602 | RWB-S2-E3017-APP | CG-ALL-8781 | 12.5 | Add a Workflows row for TreatmentWorkflow (collateral-release branch) on task queue rwb-treatment in namespace rwb-recovery. |
| CDC-16609 | RWB-S2-E3017-APP | CG-ALL-8782 | 12.5 | Add activity readClearance on task queue rwb-treatment, or name a catalogued activity. |
| CDC-16610 | RWB-S2-E3017-APP | CG-ALL-8783 | 12.5 | Add activity requestRelease on task queue rwb-treatment, or name a catalogued activity. |
| CDC-16611 | RWB-S2-E3017-APP | CG-ALL-8784 | 12.5 | Add activity confirmRelease on task queue rwb-treatment, or name a catalogued activity. |
| CDC-16612 | RWB-S2-E3017-APP | CG-ALL-8785 | 12.5 | Add activity recordAndApply on task queue rwb-treatment, or name a catalogued activity. |
| CDC-16636 | RWB-S2-E3018-APP | CG-ALL-8803 | 12.5 | Add a Workflows row for TreatmentWorkflow (document-set branch) on task queue rwb-treatment in namespace rwb-recovery, as named in section 12.5. |
| CDC-16641 | RWB-S2-E3018-APP | CG-ALL-8804 | 12.5 | Add Activities row composeDocumentSet on task queue rwb-treatment, with the input and output given in section 12.5. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16539 | RWB-S2-E3014-APP | DOR-RWB-S2-E3014-APP-8 | 12.5 | Add activities runAssetUnlockRule and recordAndApply on task queue rwb-treatment. |
| CDC-16540 | RWB-S2-E3014-APP | CG-ALL-8715 | 12.5 | Add activity runAssetUnlockRule on task queue rwb-treatment. |
| CDC-16559 | RWB-S2-E3015-APP | CG-ALL-8736 | 12.5 | Add an Activities row for attachInspectionCaptures, or substitute a catalogued activity. |
| CDC-16560 | RWB-S2-E3015-APP | CG-ALL-8737 | 12.5 | Add activity recordInspection to Activities, or use a catalogued activity |
| CDC-16561 | RWB-S2-E3015-APP | CG-ALL-8738 | 12.5 | Add activity recordAndApply to Activities, or use a catalogued activity |
| CDC-16562 | RWB-S2-E3015-APP | CG-ALL-8739 | 12.5 | Add activity reportInspectionOutcome to Activities, or use a catalogued activity |
| CDC-16642 | RWB-S2-E3018-APP | CG-ALL-8805 | 12.5 | Add an Activities row for evaluateSetRules on task queue rwb-treatment, with the generation result in and the completeness answer and rule outcomes out. |
| CDC-16643 | RWB-S2-E3018-APP | CG-ALL-8806 | 12.5 | Add an Activities row for recordAndApply on task queue rwb-treatment, with the DecisionRecord and treatment row written in one transaction through RWB-PLT-E1027-CON. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16546 | RWB-S2-E3014-CON | CG-ALL-8726 | 12.1 | Add the treatment column inspection_outcome (jsonb, rwb_treatment) to the field dictionary, or record it as a treatment column in the owning document. |
| CDC-16547 | RWB-S2-E3014-CON | CG-ALL-8727 | 12.1 | Add the treatment column unlock_decision (varchar(30), rwb_treatment) to the field dictionary, or record it in the owning document. |
| CDC-16548 | RWB-S2-E3014-CON | CG-ALL-8728 | 12.1 | Add the treatment column unlock_decided_at (timestamptz, rwb_treatment) to the field dictionary, or record it in the owning document. |
| CDC-16569 | RWB-S2-E3015-CON | CG-ALL-8746 | 12.7 | Record decision_record as the library object of DP-03 with its owning contract RWB-PLT-E1027-CON, or name its dictionary field |
| CDC-16581 | RWB-S2-E3016-APP | CG-ALL-8752 | 11, 12.6, 13 | Record the decision record object as a named entity or field in LDM v9 for schema rwb_treatment, or name its dictionary entry. |
| CDC-16595 | RWB-S2-E3016-CON | CG-ALL-8766 | 4, 11, 12.7, 13 | Record decision_record as the library object of DP-03, or use the dictionary name, so the story name resolves. |
| CDC-16639 | RWB-S2-E3018-APP | CG-ALL-8801 | section 8 | Occurrences remain in the BR5 text and the rule-location paragraph of section 8; the owning data dictionary must record the object. |
| CDC-16640 | RWB-S2-E3018-APP | CG-ALL-8802 | find it | Record approval_escalation_limit as a field, or confirm which existing name (approval_authority or delegation_limit) the story should use. |

### Epic design record (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16525 | RWB-S2-E3013-CON | DOR-RWB-S2-E3013-CON-14 | find it | Record the signed epic design sign-off in the epic design record, then mark DoR item 14 as Pass. |
| CDC-16537 | RWB-S2-E3014-APP | DOR-RWB-S2-E3014-APP-14 | header | Confirm and record the signed sign-off of the epic design for RWB-SVC-S2 / EP03. |
| CDC-16544 | RWB-S2-E3014-CON | DOR-RWB-S2-E3014-CON-14 |  | Record the signed epic design sign-off for RWB-S2-E3014-CON in the epic design record. |
| CDC-16554 | RWB-S2-E3015-APP | DOR-RWB-S2-E3015-APP-14 | header | Record the signed epic design sign-off for EP03 in the epic design record. |
| CDC-16567 | RWB-S2-E3015-CON | DOR-RWB-S2-E3015-CON-14 | none | Record the signed epic design sign-off for RWB-S2-E3015-CON |
| CDC-16577 | RWB-S2-E3016-APP | DOR-RWB-S2-E3016-APP-14 | Header | Record the signed epic design sign-off for this epic and confirm it against the epic design record. |
| CDC-16603 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-14 | find it | Record the signed epic design sign-off so the story can cite it. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16527 | RWB-S2-E3013-CON | CG-ALL-8705 | 3 | Record encumbrance_status as a column of the ACE collateral read in the owning document, or add the dictionary entry under the dictionary name. |
| CDC-16532 | RWB-S2-E3013-CON | DOR-RWB-S2-E3013-CON-7 | 11 | Add encumbrance_status as a field of the ACE collateral read and decision_record as an entity, or confirm both as working reads named in the source. |
| CDC-16564 | RWB-S2-E3015-APP | DOR-RWB-S2-E3015-APP-7 | 11 | Record decision_record as an LDM entity or field, or as the library object of RWB-PLT-E1027-CON, and classify it in Data Classification v5. |
| CDC-16572 | RWB-S2-E3015-CON | DOR-RWB-S2-E3015-CON-7 | 11 | Register decision_record as the DP-03 library object in LDM v9 and Data Classification v5, or confirm it sits outside both models. |
| CDC-16589 | RWB-S2-E3016-APP | DOR-RWB-S2-E3016-APP-7 | 11 | Add decision_record as the library object entity of rwb_treatment written through RWB-PLT-E1027-CON, or name the document that holds it. |
| CDC-16617 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-7 | 7, 11, 16 | Story uses installments and the decision_record library object. |
| CDC-16654 | RWB-S2-E3018-CON | CG-ALL-8813 | 11, 12.7 | Record decision_record as the decision-record library object of RWB-PLT-E1027-CON, or use its dictionary name. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16529 | RWB-S2-E3013-CON | DOR-RWB-S2-E3013-CON-1 | 1 | Add the role 'contract owner for rwb-treatment' to Users Roles and Permissions v5, or confirm the existing role code to use in section 1. |
| CDC-16549 | RWB-S2-E3014-CON | DOR-RWB-S2-E3014-CON-1 | 1 | Add a role code or name for 'contract owner of rwb-treatment' to Users Roles and Permissions v5. |
| CDC-16570 | RWB-S2-E3015-CON | DOR-RWB-S2-E3015-CON-1 | 1 | Add the role contract owner of rwb-treatment as a role code or role name |
| CDC-16596 | RWB-S2-E3016-CON | DOR-RWB-S2-E3016-CON-1 | 1 | Add a role code for contract owner of rwb-treatment, or confirm which existing role the story uses. |
| CDC-16627 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-1 | 1 | Add 'contract owner for rwb-treatment' as a role with a role code, or confirm the existing role code this story should use. |
| CDC-16645 | RWB-S2-E3018-APP | DOR-RWB-S2-E3018-APP-1 | 1 | Add or confirm the role name restructuring officer (FCR) with role code RW-RESTRUCT, as used in section 1. |
| CDC-16655 | RWB-S2-E3018-CON | DOR-RWB-S2-E3018-CON-1 | 1 | Add the role 'contract owner for rwb-treatment' as a role code or role name. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16599 | RWB-S2-E3017-APP | CG-ALL-8778 | 12.3 | Add event type rwb.treatment.CollateralReleaseRequested.v1 to the Events sheet. |
| CDC-16600 | RWB-S2-E3017-APP | CG-ALL-8779 | 12.3 | Add event type rwb.treatment.CollateralReleased.v1 to the Events sheet. |
| CDC-16601 | RWB-S2-E3017-APP | CG-ALL-8780 | 12.4 | Add event type rwb.payment.PaymentCleared.v1 to the Events sheet. |
| CDC-16622 | RWB-S2-E3017-CON | CG-ALL-8794 | 12.3 | Add event type rwb.treatment.CollateralReleaseRequested.v1 to the Events sheet. |
| CDC-16623 | RWB-S2-E3017-CON | CG-ALL-8795 | 12.3 | Add event type rwb.treatment.CollateralReleased.v1 to the Events sheet. |
| CDC-16624 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-8 | 12.3 | Add event types rwb.treatment.CollateralReleaseRequested.v1 and rwb.treatment.CollateralReleased.v1 to the Events sheet. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16566 | RWB-S2-E3015-CON | CG-ALL-8747 | 3 | Remove the fixed enum on treatmentType so LOV-TREATMENT values are accepted as data without a code change |
| CDC-16568 | RWB-S2-E3015-CON | DOR-RWB-S2-E3015-CON-8 | 3 | Remove the fixed enum on treatmentType so LOV-TREATMENT values are accepted as data without a code change |
| CDC-16592 | RWB-S2-E3016-CON | CG-ALL-8768 | 3 | Remove the closed treatmentType enum so LOV-TREATMENT values are accepted as data without a code change. |
| CDC-16593 | RWB-S2-E3016-CON | CG-ALL-8769 | 3 | Remove the closed outcome enum so LOV-TRT-OUTCOME values are accepted as data without a code change. |
| CDC-16594 | RWB-S2-E3016-CON | DOR-RWB-S2-E3016-CON-8 | 3 | Remove the closed treatmentType and outcome enums so LOV-TREATMENT and LOV-TRT-OUTCOME values are accepted as data. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16530 | RWB-S2-E3013-CON | DOR-RWB-S2-E3013-CON-11 | 11 | Align the personal-data class of the P2 fields with section 11, which states that no personal data is carried. |
| CDC-16615 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-11 | find it | Reconcile the personal-data class of the fields carried by this story with the statement that none is carried. |
| CDC-16629 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-11 | 11 | Confirm the class of the field the detcheck found personal; the story now states that no field of this story is personal data. |
| CDC-16657 | RWB-S2-E3018-CON | DOR-RWB-S2-E3018-CON-11 | - | Align the personal-data class of the P2 fields with the rule that this story carries no personal value (AC2, AC3). |

### RWB-PLT-E1027-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16528 | RWB-S2-E3013-CON | CG-ALL-8706 | 9 and 12.9 | Record decision_record as the library object in its owning story and document, or add the dictionary name to LDM v9. |
| CDC-16545 | RWB-S2-E3014-CON | CG-ALL-8725 |  | Record decision_record as the library object of DP-03 so the object is recorded in its owning document. |
| CDC-16626 | RWB-S2-E3017-CON | CG-ALL-8793 | 11, 12.7 | Record decision_record as the library object (index, library table or flag) it is, so the name resolves in the owning document. |

### RWB-S2-E3016-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16578 | RWB-S2-E3016-APP | DOR-RWB-S2-E3016-APP-21 | Header | Set the contract story build status to Done once the contract is published. |
| CDC-16590 | RWB-S2-E3016-APP | GAP-2681 | 8, 11 | Publish at v1 the working read of ASM-B2-S2-011-2 and ASM-B2-S2-011-7: rent in offer_amount (DF-TRT-007), first due in first_due_date (DF-TRT-029), instalments in installments_paid (DF-TRT-032), rentalRef, autoDebitRef and autoDebitStatus with no published field and absent until answered, no rental table, no new event. |
| CDC-16591 | RWB-S2-E3016-APP | GAP-2680 | 4, 8, 11, 12.5 | Publish at v1 the working read of ASM-B2-S2-011-1 to ASM-B2-S2-011-7: RENTAL treatment row, no rental table, rentalRef/autoDebitRef/autoDebitStatus, case status moved by CaseWorkflow, AMIS and ATS requested through rwb-asset and rwb-integration. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16618 | RWB-S2-E3017-APP | GAP-1705 | 7 | Story states the CCMS path from this service is not specified |
| CDC-16625 | RWB-S2-E3017-CON | GAP-1696 | find it | FSD S2 A2.6.3.1, A2.13.2, A2.10.2 and A2.17.2 read source facts through the rwb-source-data contract; Architecture v5 connection matrix (slide 13) adds S2 to the P1 REST cell. |
| CDC-16633 | RWB-S2-E3017-CON | GAP-1705 | none | Route the asset take-on to rwb-asset and the CCMS release and Land Office title check through rwb-integration; record each returned reference; add the two cells this service needs. |

### RWB-S2-E3014-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16538 | RWB-S2-E3014-APP | DOR-RWB-S2-E3014-APP-21 | header | Set build status to Done so the contract is published. |
| CDC-16543 | RWB-S2-E3014-APP | GAP-2677 | 11 | Publish the working read of ASM-B2-S2-009-7, ASM-B2-S2-009-8 and ASM-B2-S2-009-9: AssetUnlock with inspectionOutcome, unlockDecision, unlockDecidedAt, assetRef, ruleId and ruleVersion; unlockDecision as a width carrying the returned event code; the element a component of the treatment representation on GET /treatments/{treatmentId}; no unlock or release event. |

### RWB-S2-E3015-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16555 | RWB-S2-E3015-APP | DOR-RWB-S2-E3015-APP-21 | header | Set build status to Done once the contract is published. |
| CDC-16556 | RWB-S2-E3015-APP | DOR-RWB-S2-E3015-APP-22 | header | Fake set row states publication is pending; the contract story is Not started |

### RWB-PLT-E1027-CON; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16558 | RWB-S2-E3015-APP | CG-ALL-8733 | 7, 11, 12.7, 13 | Record decision_record as the library object of RWB-PLT-E1027-CON, or add it to LDM v9 Fields. |
| CDC-16608 | RWB-S2-E3017-APP | CG-ALL-8776 | find it | Record decision_record as a library object (index, library table or flag) in the owning document, or use the dictionary name. |

### RWB-S2-E3017-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16604 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-21 | find it | Reach build status Done (currently Not started). |
| CDC-16605 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-22 | find it | Publish the contract fake library and record its version. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16621 | RWB-S2-E3017-APP | GAP-1700 |  | Add a TreatmentClosed row (producer rwb-treatment; consumers rwb-case and rwb-reporting) on rwb.treatment.events.v1; allocate an EV number when the catalogue assigns one. |
| CDC-16647 | RWB-S2-E3018-APP | GAP-1698 | find it | Add rows under rwb-treatment for contracts, settlement and deed-in-lieu agreements, and plan timers, with the four entity groups and key fields. |

### RWB-S2-E3018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16637 | RWB-S2-E3018-APP | DOR-RWB-S2-E3018-APP-21 | find it | Set build status to Done once the contract is published. |
| CDC-16651 | RWB-S2-E3018-APP | GAP-2685 | find it | Publish the working read of ASM-B2-S2-013-4 as rwb-treatment contract v1: documentSet section, DocumentSetRequest element, status vocabulary, and error set. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16648 | RWB-S2-E3018-APP | GAP-1709 | find it | State in the release slicing: wave 2 publishes the contract and delivers the treatment record with its data date; offer, settlement, plan and deed in lieu release with E3. |
| CDC-16660 | RWB-S2-E3018-CON | GAP-1709 | header | State the split: contract in wave 2, offer, settlement, plan and deed in lieu capabilities released with E3; no requirement changes. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:37; OTHER:45) and FSD S2 (A2.6.3.1; OTHER:A2.10.2; OTHER:A2.13.2; OTHER:A2.17.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16526 | RWB-S2-E3013-CON | GAP-1696 | find it | Add S2 to the P1 REST cell of the connection matrix; FSD S2 obtains ACE, ALS, COLLINS, NLEADS and CCMS facts through the rwb-source-data contract, with no direct read. |

### RWB-S2-E3013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16533 | RWB-S2-E3013-CON | GAP-1702 | 8 | Replace the batch and timer triggers of A2.1.2 to A2.18.2 with steps of TreatmentWorkflow started by rwb-case and by owning-service events; add no schedule. |

### RWB-S2-E3013-APP; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16534 | RWB-S2-E3013-CON | GAP-1705 |  | Request asset take-on from S5 and the CCMS release and Land Office title check through the rwb-integration contract; add the two connection-matrix cells this service needs. |

### OTHER:Integration interface and SIT harness specification (outside the source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16535 | RWB-S2-E3013-CON | GAP-0425 | none | Publish the check interface with its codes and fixture result set, the SIT harness environment and repository, the two-case seeding set, the six fake response values, the evidence report shape and its gate, held in configuration. |

### RWB-S2-E3014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16551 | RWB-S2-E3014-CON | GAP-2676 | 11 | Apply working read of ASM-B2-S2-009-1, -3 and -4: four optional treatment columns (answer, instant, inspection outcome, asset reference) on the service's Flyway sequence; release reported to the parent CaseWorkflow; rwb-asset links the property under FEAT-AST-02 on the case fact; no event invented; no recovery.v_ace_* view named; confirm with rwb-asset owner. |

### OTHER:rwb-treatment service contract document (major version 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16565 | RWB-S2-E3015-APP | GAP-2679 | 11 | Publish six inspection element names, domains, required/optional flags and absent-until rule; capture rides on the terms change with no own operation or event; generated fake set for four consumers. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:16; OTHER:17) and FSD S2 v3 (A2.18.2; OTHER:A2.15.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16574 | RWB-S2-E3015-CON | GAP-1704 | 10 | Route document generation, review and signature through the P5 and P6 contracts and replace 'the Workbench document hub' with those owners in the FSD and the integration map. |

### OTHER:rwb-treatment (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16575 | RWB-S2-E3015-CON | GAP-2679 | 11 | Element names and absent-until rule are published. Domains are only a working read, the fake set is not addressed, and the owning document must publish the rest. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16579 | RWB-S2-E3016-APP | DOR-RWB-S2-E3016-APP-22 | Header | Record the published contract fake library version. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16606 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-8 | 12.3, 12.4, 12.5 | Clear catalog gaps CG-ALL-8778 to CG-ALL-8781 and the four further P1 findings in the detcheck. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:slides 37 and 45) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16607 | RWB-S2-E3017-APP | GAP-1696 | 4 | Add S2 to P1 REST cell in the connection matrix; restate slides 37 and 45 so rwb-source-data is the only ACE reader and other modules use its REST contract or a Temporal activity. |

### OTHER:Screen Specifications v1 (SCR-14; OTHER:SCR-15 loading and error states) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16614 | RWB-S2-E3017-APP | DOR-RWB-S2-E3017-APP-10 | 4 | SCR-14 empty and no-access states added in step 10 and section 15. |

### OTHER:TSD S2 v2 and FSD S2 v3 (rwb-treatment contract v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16619 | RWB-S2-E3017-APP | GAP-2683 |  | Publish as rwb-treatment contract v1: collateralRelease section on GET /treatments/{treatmentId}; events rwb.treatment.CollateralReleaseRequested.v1 and rwb.treatment.CollateralReleased.v1 on rwb.treatment.events.v1; release vocabulary and view column contract. |

### OTHER:Wave 2 integration and harness specification (CCMS interface; OTHER:harness pack) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16620 | RWB-S2-E3017-APP | GAP-0426 |  | Agree CCMS interface config and test endpoint with the integration owner; publish the R-SET-21 confirmation fixture; name the account data product code; agree harness pack, seeding and evidence format with QA. |

### OTHER:Screen specification for SCR-14 and SCR-15 (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16628 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-10 | find it | Add empty, loading, error and no access states for SCR-14 and SCR-15. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx; OTHER:rwb-source-data (P1) contract read (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16631 | RWB-S2-E3017-CON | DOR-RWB-S2-E3017-CON-7 | 11 | Name decision_record as a field or entity in LDM v9 or DC v5, or remove it; confirm the four ACE view reads go through the P1 contract read or its fallback. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:A2.11; OTHER:A2.17) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16632 | RWB-S2-E3017-CON | GAP-1703 | none | Record the booking reference from TreatmentBooked and the break from PaymentMissed in rwb-payment; the release request leaves via the integration contract and this service records the reference returned. |

### OTHER:Integration interface catalogue and wave 2 harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16634 | RWB-S2-E3017-CON | GAP-0426 | 15 | Agree CCMS interface config and test endpoint with integration owner; publish R-SET-21 confirmation fixture; name account data product code; agree harness pack, seeding and evidence format with QA; build on fakes until then. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16638 | RWB-S2-E3018-APP | DOR-RWB-S2-E3018-APP-8 | 12.5 | Add Workflows row TreatmentWorkflow (document-set branch) and Activities rows composeDocumentSet, evaluateSetRules and recordAndApply on task queue rwb-treatment. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx; parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16646 | RWB-S2-E3018-APP | DOR-RWB-S2-E3018-APP-7 | 11, 12.8 | Story side done: the party read uses the rwb-source-data contract fake and AC1 and AC4 use decision record wording. Model entries are elsewhere. |

### OTHER:FSD S2 (field catalogs A2.2.3.2; OTHER:A2.3.3.2; OTHER:A2.4.3.2; OTHER:A2.12.3.2; OTHER:A2.15.3.2; OTHER:A2.18) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16649 | RWB-S2-E3018-APP | GAP-1712 | find it | Require the eight catalog fields as written and hold the contract, agreement, plan timer and booking reference, with the physical list left to the data architect. |

### OTHER:FSD S2 v3 (A2.1.4.1 to A2.18.4.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16650 | RWB-S2-E3018-APP | GAP-1708 | find it | Replace the placeholder acceptance criteria with observable criteria and name the module's alternate flows and background events. |

### OTHER:Owning services' message catalogues; OTHER:DL10 (message wording) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16652 | RWB-S2-E3018-APP | GAP-1710 | 8 | Story records ownership of MSG-P4-002, MSG-P7-003 and MSG-S2-001 only. Agreed wording of the five messages is a DL10 and catalogue task, not resolved by this story. |

### OTHER:FSD S2 version 3 (Functional Specification S2; OTHER:15 November 2026) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16653 | RWB-S2-E3018-APP | GAP-1715 | n/a | Carry version 3 in full; mark versions 1 and 2 as Not specified in the source documents; read the repeated FEAT-CHO-08 in A1.1 as one dependency; FSD owner supplies both change notes at the next FSD version. |

### OTHER:P3 screen specification for SCR-14 and SCR-15 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16656 | RWB-S2-E3018-CON | DOR-RWB-S2-E3018-CON-10 | - | Add empty, loading, error and no-access states to SCR-14 and SCR-15. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Tables sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16659 | RWB-S2-E3018-CON | GAP-1698 | 11 | Add rows for rwb-treatment contracts, settlement and deed-in-lieu agreements and plan timers (S2); physical names come with the DB story. |

### OTHER:Functional Specification Document S2 (A2.1.4.1 to A2.18.4.4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16661 | RWB-S2-E3018-CON | GAP-1708 | 2 | Replace the eighteen placeholder success criteria and the None alternate and background rows with observable criteria naming the module's flows and events. |

### OTHER:FSD S2 (A2.18.2; OTHER:A2.15.2; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:17; OTHER:41) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16663 | RWB-S2-E3018-CON | GAP-1704 | 8 | Name the P5 and P6 contracts instead of the Workbench document hub in A2.18.2 and A2.15.2, and route the A2.8.3.1 signature check through P6. Story side done in BR8. |

### OTHER:S2 message catalogue and the owning services' catalogues (DL10) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16664 | RWB-S2-E3018-CON | GAP-1710 | 5 | Hold MSG-S2-001 in the S2 catalogue with Thai and English wording; serve MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 from their owning services; close DL10 before wave 3 release. |

### OTHER:FSD S2 (document control and A1.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-16665 | RWB-S2-E3018-CON | GAP-1715 |  | The FSD history and the A1.1 dependency sentence sit in FSD S2, not in this contract story. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0425 | The CCMS and Land Office check interface, the harness environment and seeding set, the fake response values and the evidence and gate of the early readiness harness are not in the sources | Integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0426 | The CCMS release interface, the harness pack and the case-state screen are not specified | Integration lead | Resolved (directive) |
| GAP-0736 | The encumbrance-check slice leaves the requirement ID, the check-versus-state boundary, the S2 answer shape, the rule timer specs and three new field IDs unspecified | Tech lead | Resolved (directive) |
| GAP-1696 | FSD S2 reads ACE views and the ALS, COLLINS, NLEADS and CCMS systems directly, while Architecture v5 allows only rwb-source-data to read ACE | Solution architect with the P1 owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1698 | The Ownership Map lists one table for rwb-treatment, although Architecture v5 gives it four entity groups | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1700 | TreatmentClosed has no event number and no row in the Ownership Map event sheet | Solution architect | Resolved (directive) |
| GAP-1702 | The FSD triggers on a completed ACE batch, and AceDataReady does not reach this service while no S2 job exists in the job map | Solution architect with the P1 owner | Resolved (directive) |
| GAP-1703 | Booking, payment matching and posting are rwb-payment's in Architecture v5, while the FSD writes them from this module | Solution architect with the P8 owner | Resolved (directive) |
| GAP-1704 | The document set and the signature are rwb-document's and rwb-comms's in Architecture v5, while the FSD names the Workbench document hub | Solution architect with the P5 and P6 owners | Resolved (directive) |
| GAP-1705 | The CCMS release, the Land Office title check and the asset take-on have no path from this service in Architecture v5 | Solution architect with the integration lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1708 | The FSD acceptance criteria are placeholders, so no criterion of this module is observable as written | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1709 | The service is wave 2 and EP02 while every requirement of the module is an Epic 3 requirement | Solution architect | Resolved (directive) |
| GAP-1710 | Only one of the five messages this service shows is its own, and none has agreed wording | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1712 | The field catalog covers eight fields and none of them describes a contract, an agreement, a plan timer or a booking | Data architect | Resolved (directive) |
| GAP-1715 | The history of FSD S2 versions 1 and 2 is not in the sources read, and the dependency sentence repeats a feature code | Business analyst, S2 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2674 | The readiness check result, the title-set task, the trigger and the ACE status field are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P1 owner of the ACE read and the owner of the local decision-record library | Resolved (directive) |
| GAP-2675 | The published shape of the readiness section, of the title-set task request and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract and the P1 owner of the ACE read | Resolved (directive) |
| GAP-2676 | The home of the unlock answer and of the asset reference, the announcement of the release, and the trigger of FEAT-AST-02 are not specified for rwb-treatment | Tech lead of rwb-treatment with the rwb-asset, rwb-source-data and rwb-case owners | Resolved (directive) |
| GAP-2677 | The field list, the value domain and the home of the unlock element, and the announcement of the release, have no published shape | Solution architect with the rwb-treatment tech lead and the P7 owner of the rule packages | Resolved (directive) |
| GAP-2679 | The inspection contract identifiers, the element domains, the reference shapes and the fake set are not published for rwb-treatment | Contract owner of rwb-treatment with the rwb-document owner and the field app owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2680 | The buy-back rental element set, the rental table, the AMIS and ATS path, the receipt loop and the rental event are not specified for rwb-treatment | Tech lead of rwb-treatment with the S5 owner of the asset record, the P8 owner of payments and the P2 owner of the integration contract | Resolved (directive) |
| GAP-2681 | The rental element names, their domains, their absent-until rule and the absence of a rental event are not specified for the rwb-treatment contract | Contract author of rwb-treatment with the P8 owner of payments, the S5 owner of the asset record and the P3 owner of the case contract | Resolved (directive) |
| GAP-2682 | The release result, the release instruction, the confirmation read and the case outcome are not specified for rwb-treatment | Tech lead of rwb-treatment with the P3 owner of the case contract, the P8 owner of the payment contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2683 | The published shape of the release section, of the two release events, of the release vocabulary and of the view column contract has no source | Solution architect with the rwb-treatment tech lead, the P3 owner of the case contract, the P1 owner of the ACE read and the platform integration owner of the CCMS adapter | Resolved (directive) |
| GAP-2684 | The document-set result, the rendering hand-off, the party set and the case trigger are not specified for rwb-treatment | Tech lead of rwb-treatment with the P5 owner of the document contract, the P6 owner of the template catalogue and the P3 owner of the case contract | Resolved (directive) |
| GAP-2685 | The published shape of the document-set section, of the set request and of the status vocabulary has no source | Solution architect with the rwb-treatment tech lead, the P5 owner of the document contract and the P6 owner of the template catalogue | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-S2-E3017-APP | skipped AC ID | 117 | missing: AC3, AC6 |
| RWB-S2-E3017-APP | new AC without TC row | 380 | AC7 is new and no section 16 row covers it |
| RWB-S2-E3017-APP | new AC without TC row | 380 | AC8 is new and no section 16 row covers it |
