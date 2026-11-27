# RWB-SVC-S8 rwb-deviation (Deviation) - review pack, part 3 of 3 (RWB-S8-E7008-APP to RWB-S8-E7010-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 117 |
| Cross-document (pending in another document) | 74 |
| Not applied (value not in the sources) | 8 |
| Open business decisions | 11 |
| Register gaps linked | 6 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S8-E7008-APP | 26 | 13 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7008 APP Review an override v2.md |
| RWB-S8-E7008-CON | 15 | 8 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7008 CON Review an override - contract v2.md |
| RWB-S8-E7009-APP | 24 | 14 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7009 APP Match a complaint to the preceding contact v2.md |
| RWB-S8-E7009-CON | 12 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7009 CON Match a complaint to the preceding contact - contract v2.md |
| RWB-S8-E7010-APP | 25 | 14 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7010 APP Handle a contact sent while a block is on v2.md |
| RWB-S8-E7010-CON | 15 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7010 CON Handle a contact sent while a block is on - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S8-E7008-APP | R-03109 | CG-ALL-11623 | Script gap | Product owner | The story adds DEV_WITH_OWNER to the closed list LOV-DEV-OUTCOME | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S8-E7008-APP | R-13477 | CG-ALL-11635 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7008-CON | R-13480 | CG-ALL-11648 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S8-E7009-APP | R-13486 | CG-ALL-11663 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-S8-E7009-APP, RWB-S8-E7009-CON | R-23272 | GAP-3068 | Register gap | Solution architect; business lead; access owner in rwb-access | RWB-S8-E7009-APP: neither deviation nor any other owned table carries a complaint or contact reference, no published rule row expresses the match, no requirement row traces to FEAT-DVF-09, the Conduct and QA officer holds R only while the feature needs U, the plan's C row is empty while two contracts are consumed, DP-04, DP-05, DP-09 and DP-18 are absent, and no event carries the match to rwb-reporting | Keep the plan's H, C, I and X rows as they stand; carry the complaint and contact references and the match outcome as request inputs recorded on the local decision record until the business lead confirms their names, formats and value set; declare the two consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-05, DP-09 and DP-18 rows; read the contact through rwb-source-data as the connection matrix gives it and never through EFS; authorise the match on the case-record right U the permission table gives and record the matrix row as the conflict; let the trace rest on the legacy key and the feature row until the E7 BRD and the PRD publish a requirement; leave the conduct measure on the decision-record ledger until an event exists |
| RWB-S8-E7001-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON | R-23644 | GAP-3071 | Register gap | Solution architect with the rwb-source-data owner, the rwb-access owner, the platform library owner and Compliance | RWB-S8-E7010-CON: the consumed ledger operation, the breach-entry attributes, the breach read, the conduct-officer right and the clock length have no published baseline | Publish the interaction-ledger read operation with its fields and its 2 s budget; confirm the breach-entry attributes against the local record schema; publish the SCR-08 breach read; record the RW-CONDUCT conflict and resolve it in the access matrix rather than in a contract; settle the service level with DL22; confirm that no breach event is published in wave 4. Until then the baseline declares the consumed row and the entry with the placeholders and the three absences. |
| RWB-S8-E7008-APP, RWB-S8-E7008-CON | R-23645 | GAP-3066 | Register gap | Business lead; solution architect; rwb-decision rule owner; rwb-access owner | RWB-S8-E7008-APP: no source defines the override as a record of S8 or gives the forum's reason a field, no rule row names the review forum and no operation reads the deviation list, the plan's C row is empty while the package read is consumed and the S8 matrix row carries no P7 edge, the primary role holds R only while the review needs U, and no requirement row traces to FEAT-DVF-08 | Read the override as the open deviation record of the case, record the forum's outcome and its reason through DeviationOutcome (outcome over LOV-DEV-OUTCOME, the reason on note) into the local decision record and deviation.outcome, move the deviation on R-DEV-09, R-DEV-10 and R-DEV-22 only, leave cleared_at, the contact stop, the clock resume and the route reopen to FEAT-DVH-06 and the route stories, read the package on a class C row with a fake, keep the case and the clock with rwb-case, and hold the requirement row and the list read as open items. |
| RWB-S8-E7008-APP, RWB-S8-E7008-CON | R-23646 | GAP-3067 | Register gap | Solution architect; rwb-deviation tech lead; business lead; rwb-decision rule owner; rwb-access owner | RWB-S8-E7008-CON: the DeviationOutcome element carries no reason property and no source publishes its name, field ID or value format, no operation reads the deviation list, the plan's C row is empty while the baseline declares one consumed row and DP-04, DP-05, DP-07, DP-08 and DP-09 are absent, the primary role holds R only, and no requirement row traces to FEAT-DVF-08 | Publish the review branch inside API-S8-002 with the published DeviationOutcome (outcome over LOV-DEV-OUTCOME and note carrying the reason with a placeholder), declare the package read as a class C row with a fake and no rule row, declare no override entity, no list read, no event, no Schedule and no cleared_at property, fix the twelve holders of right U and the three read-only review roles as a recorded conflict, and hold the requirement row open. |
| RWB-S8-E7009-APP, RWB-S8-E7009-CON | R-23647 | GAP-3069 | Register gap | Solution architect; business lead | RWB-S8-E7009-CON: the Deviation, DeviationRequest and DeviationOutcome elements carry no complaint or contact reference and no match outcome, no source publishes their names, formats or value set, the two consumed operation names have no published baseline, no requirement row traces to FEAT-DVF-09, and the plan's C row is empty while the baseline declares two consumed rows | Publish the baseline with the placeholders, bind every error condition to one message id of section 14, declare the match inside the one published deviation-outcome operation and not as a second path, declare the contact and package rows as consumed and faked, record the decision-record element, the lists of TSD S8 T3.2 and the rights, and trace to the legacy key and the feature row until the E7 BRD and the PRD publish a requirement |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S8-E7008-APP | R-08927 | DOR-RWB-S8-E7008-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off is in the story or the 03 Requirements sources. Recording one would invent a value. Story text not edited. |
| RWB-S8-E7008-APP | R-21290 | DOR-RWB-S8-E7008-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | SCR-06 states belong to the raise stories. No SCR-08 empty, loading, error or no-access state is in the sources, so adding them would invent states. Section 10 text not in chunk. |
| RWB-S8-E7008-CON | R-21302 | DOR-RWB-S8-E7008-CON-11 | Not located | Definition of Ready item 11 Guardrails: Partial | The P2 personal-data section is not in the supplied story text (header and headings only). Grep found no matching story section to anchor an edit. |
| RWB-S8-E7008-CON | R-29235 | GAP-1488 | Not located | The override rate is reported monthly with no target | The override-rate measure text is not in the supplied story text, so there is no old text to anchor. Publish-by-decision-and-product fix needs that section. |
| RWB-S8-E7009-APP | R-08944 | DOR-RWB-S8-E7009-APP-22 | header | Definition of Ready item 22 Fake published: Fail | No fake library version in the sources. Searched aisdlc yaml files for 'fake' (no match); CON story not in 22 folder. Placeholder kept. |
| RWB-S8-E7009-APP | R-21308 | DOR-RWB-S8-E7009-APP-11 | 9 | Definition of Ready item 11 Guardrails: Partial | Story already states no personal data (lines 267, 438). The field classing that conflicts is in section 9 text not in this chunk, and no matching P2 source was found. No edit made. |
| RWB-S8-E7009-CON | R-08947 | DOR-RWB-S8-E7009-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the sources. Grep of 23 Document Gaps and the project found no match for the ID or for signed epic design; the only hits are scratch escalation files. Recording a sign-off would invent a fact. |
| RWB-S8-E7010-APP | R-33185 | NEWAC-RWB-S8-E7010-APP-AC8 | 5 | AC8: activity retry and timeout (no criterion covers a retried or timed-out activity) | X4 Covered by column still lacks AC8 and TC-E7-010-10 (and AC9, TC-E7-010-11). The X4 row text was not in the provided diff, so an exact edit could not be made; add these to the X4 row. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19753 | RWB-S8-E7008-APP | CG-ALL-11628 | 12.2 | Add REST base /api/recovery/decision/v1 for P7 rwb-decision, as stated in the PRD P7 rwb-decision v1 REST base row. |
| CDC-19766 | RWB-S8-E7008-CON | CG-ALL-11642 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule-package read, as given in the Document Index service table. |
| CDC-19770 | RWB-S8-E7008-CON | DOR-RWB-S8-E7008-CON-6 | 10 | Add the rwb-access authorise check (DP-08) that RWB-S8-E7008-CON consumes, with its operation name and path |
| CDC-19774 | RWB-S8-E7009-APP | CG-ALL-11656 | 12.2 | Confirm REST base /api/recovery/source-data/v1 for rwb-source-data from the Document Index service table and declare it in the owner yaml. |
| CDC-19775 | RWB-S8-E7009-APP | CG-ALL-11657 | 12.2 | Confirm REST base /api/recovery/decision/v1 for rwb-decision from the Document Index service table and declare it in the owner yaml. |
| CDC-19788 | RWB-S8-E7009-CON | CG-ALL-11670 | 12.2 | Declare REST base /api/recovery/source-data/v1 using the provider's base from the Document Index service table. |
| CDC-19789 | RWB-S8-E7009-CON | CG-ALL-11671 | 12.2 | Declare REST base /api/recovery/decision/v1 using the provider's base from the Document Index service table. |
| CDC-19791 | RWB-S8-E7009-CON | DOR-RWB-S8-E7009-CON-8 | 12.1 | Add POST /cases/{caseId}/deviations and PATCH /deviations/{deviationId} to rwb-deviation yaml; add the /api/recovery/source-data/v1 and /api/recovery/decision/v1 bases; add the other listed paths |
| CDC-19797 | RWB-S8-E7010-APP | CG-ALL-11682 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the rwb-source-data provider |
| CDC-19811 | RWB-S8-E7010-CON | CG-ALL-11695 | 12.2 | Declare REST base /api/recovery/source-data/v1 for rwb-source-data in the yaml. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19759 | RWB-S8-E7008-APP | CG-ALL-11634 | 16 | Add rows TC-E7-008-01, TC-E7-008-02, TC-E7-008-03 and TC-E7-008-04 with Given, When and Then copied from the criteria they cover. |
| CDC-19760 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-12 | 12, 12.7, 16 | Tab Story test cases: add rows TC-E7-008-01 to TC-E7-008-07 under the same IDs as section 16, including TC-E7-008-05 contract and TC-E7-008-06 boundary. |
| CDC-19771 | RWB-S8-E7008-CON | CG-ALL-11647 | 16 | Add rows TC-E7-008-01 to -04 and TC-S8-E7008-CON-01 to -05 to tab Story test cases, with Given, When and Then copied from the criteria they cover |
| CDC-19782 | RWB-S8-E7009-APP | CG-ALL-11662 | 16 | Add rows TC-E7-009-01, TC-E7-009-02, TC-E7-009-03 and TC-E7-009-04 with Given, When and Then copied from the criteria they cover. |
| CDC-19784 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-12 | 16 | Section 16 test rows added for contract, boundary and component cases. |
| CDC-19795 | RWB-S8-E7009-CON | DOR-RWB-S8-E7009-CON-12 Test cases: Partial | 16 | Story adds TC-S8-E7009-CON-06 (AC8) and TC-S8-E7009-CON-07 (AC7 boundary) to the §16 table. |
| CDC-19796 | RWB-S8-E7009-CON | CG-ALL-11676 | 16 | Add Story test cases rows for TC-E7-009-01 to -04 and TC-S8-E7009-CON-01 to -05, with Given, When and Then copied from the criterion each covers. |
| CDC-19805 | RWB-S8-E7010-APP | CG-ALL-11689 | 16 | Add rows TC-E7-010-01 to -04 to Story test cases, with Given, When and Then copied from AC1, AC2, AC2 with X2, and AC2 with X1. |
| CDC-19819 | RWB-S8-E7010-CON | DOR-RWB-S8-E7010-CON-12 | 12.7, 16 | Add rows TC-E7-010-01 to -04 and TC-S8-E7010-CON-01 to -09 under tab Story test cases; the new boundary test for section 12.7 tables is TC-S8-E7010-CON-08. |
| CDC-19824 | RWB-S8-E7010-CON | CG-ALL-11702 | 16 | Add Story test cases rows for TC-E7-010-01 to -04 and TC-S8-E7010-CON-01 to -09, plus -10 and -11 added here, with Given, When and Then copied from their criteria |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19751 | RWB-S8-E7008-APP | CG-ALL-11626 | 12.1 | Publish PATCH /deviations/{deviationId} (API-S8-002) under base /api/recovery/deviation/v1 through RWB-S8-E7008-CON, or remove it from 12.1. |
| CDC-19752 | RWB-S8-E7008-APP | CG-ALL-11627 | 12.1 | Publish POST /cases/{caseId}/deviations (API-S8-001) under base /api/recovery/deviation/v1 through RWB-S8-E7008-CON, or remove it from 12.1. |
| CDC-19756 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-8 | find it | Add paths POST /cases/{caseId}/deviations (API-S8-001) and PATCH /deviations/{deviationId} (API-S8-002); add base /api/recovery/decision/v1; model outcome as data, not a closed enum. Story PATCH idempotency cell set to placeholder. |
| CDC-19764 | RWB-S8-E7008-CON | CG-ALL-11640 | 12.1 | Publish PATCH /deviations/{deviationId} (API-S8-002) under base /api/recovery/deviation/v1 with DeviationOutcome in and Deviation of status 200 out. |
| CDC-19765 | RWB-S8-E7008-CON | CG-ALL-11641 | 12.1 | Publish POST /cases/{caseId}/deviations (API-S8-001) under base /api/recovery/deviation/v1 with DeviationRequest in and Deviation out. |
| CDC-19772 | RWB-S8-E7009-APP | CG-ALL-11654 | 12.1 | Publish PATCH /deviations/{deviationId} under base /api/recovery/deviation/v1 through RWB-S8-E7009-CON, or remove it from the yaml. |
| CDC-19773 | RWB-S8-E7009-APP | CG-ALL-11655 | 12.1 | Publish POST /cases/{caseId}/deviations under base /api/recovery/deviation/v1 through RWB-S8-E7009-CON, or remove it from the yaml. |
| CDC-19786 | RWB-S8-E7009-CON | CG-ALL-11668 | 12.1 | Publish PATCH /deviations/{deviationId} (API-S8-002) under base /api/recovery/deviation/v1 with DeviationOutcome in and Deviation of status 200 out. |
| CDC-19787 | RWB-S8-E7009-CON | CG-ALL-11669 | 12.1 | Publish POST /cases/{caseId}/deviations (API-S8-001) under base /api/recovery/deviation/v1 with DeviationRequest in and Deviation out. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19768 | RWB-S8-E7008-CON | CG-ALL-11646 | 12.5 | Add activity recordDeviationReview to the Activities sheet, or name a catalogued activity in its place |
| CDC-19781 | RWB-S8-E7009-APP | CG-ALL-11661 | 12.5 | Add an Activities row for recordComplaintMatch on task queue rwb-deviation as the one match step of the stage. |
| CDC-19792 | RWB-S8-E7009-CON | CG-ALL-11675 | 12.5 | Add an Activities row for recordComplaintMatch on task queue rwb-deviation, or name a catalogued activity in the story instead |
| CDC-19802 | RWB-S8-E7010-APP | CG-ALL-11686 | 12.5 | Add readBreachFacts to Activities on task queue rwb-deviation, as described in section 12.5, or use a catalogued activity. |
| CDC-19803 | RWB-S8-E7010-APP | CG-ALL-11687 | 12.5 | Add evaluateBreachRules to Activities on task queue rwb-deviation, as described in section 12.5, or use a catalogued activity. |
| CDC-19804 | RWB-S8-E7010-APP | CG-ALL-11688 | 12.5 | Add recordAndApplyBreach to Activities on task queue rwb-deviation, as described in section 12.5, or use a catalogued activity. |
| CDC-19814 | RWB-S8-E7010-CON | CG-ALL-11699 | 12.5 | Add an Activities row readBreachFacts on task queue rwb-deviation, or name a catalogued activity to use instead. |
| CDC-19815 | RWB-S8-E7010-CON | CG-ALL-11700 | 12.5 | Add an Activities row evaluateBreachRules on task queue rwb-deviation, or name a catalogued activity to use instead. |
| CDC-19816 | RWB-S8-E7010-CON | CG-ALL-11701 | 12.5 | Add an Activities row recordAndApplyBreach on task queue rwb-deviation, or name a catalogued activity to use instead. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19757 | RWB-S8-E7008-APP | CG-ALL-11624 | 11 | Record decision_record as a PLT library object created in rwb_deviation (DP-03), as section 11 already states, or add it as a dictionary field. |
| CDC-19762 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-7 | 11 | Add or align the names decision_record and recovery_log with LDM v9 and Data Classification v5 entities; the story names the PLT library decision record of DP-03. |
| CDC-19779 | RWB-S8-E7009-APP | CG-ALL-11652 | 11 | Record decision_record as a PLT library object created in rwb_deviation (DP-03), or add it to the dictionary under its dictionary name. |
| CDC-19780 | RWB-S8-E7009-APP | CG-ALL-11653 | 17 | Confirm recovery_log is a retired legacy object absent from the target model, or record it as a retired element in the owning document. |
| CDC-19807 | RWB-S8-E7010-APP | DOR-RWB-S8-E7010-APP-7 | 11 | List decision_record as a platform library table of rwb_deviation outside the entity list, and recovery_log as a retired name. Story P3 decision-log wording is already reworded. |
| CDC-19820 | RWB-S8-E7010-CON | DOR-RWB-S8-E7010-CON-7 | 11 | Register decision_record as a PLT library object entity in LDM v9 and Data Classification v5, or name its source |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19761 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-6 | 10 | Add role SY-DATALOAD with case record right U as TSD S8 T6.1 gives it, so the §10 role resolves. |
| CDC-19769 | RWB-S8-E7008-CON | DOR-RWB-S8-E7008-CON-1 | 1 | Add a role row for tech lead, or confirm the role name section 1 should use for rwb-deviation |
| CDC-19785 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-6 | 10 | Add role SY-DATALOAD with case record right U, as TSD S8 T6.1 gives it |
| CDC-19793 | RWB-S8-E7009-CON | DOR-RWB-S8-E7009-CON-1 | 1 | Register 'tech lead' as a role code or role name, or the story names a role that exists in Users Roles and Permissions v5 |
| CDC-19817 | RWB-S8-E7010-CON | DOR-RWB-S8-E7010-CON-1 | 1 | Add a role code and name for tech lead, or map the section 1 persona to an existing role in the workbook. |

### Epic design record (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19767 | RWB-S8-E7008-CON | DOR-RWB-S8-E7008-CON-14 | header | Record the signed epic design sign-off for RWB-S8-E7008-CON. |
| CDC-19776 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-14 | 1 | Record the signed epic design sign-off for this story's epic, or confirm the existing sign-off, since none is in the story or source documents. |
| CDC-19798 | RWB-S8-E7010-APP | DOR-RWB-S8-E7010-APP-14 | header | Record signed epic design sign-off for RWB-S8-E7010-APP |
| CDC-19812 | RWB-S8-E7010-CON | DOR-RWB-S8-E7010-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S8; no sign-off exists in the source set. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19800 | RWB-S8-E7010-APP | CG-ALL-11680 | 12.7 | Record decision_record as a Platform library table in rwb_deviation (DP-03), or use the dictionary name. Story unchanged. |
| CDC-19801 | RWB-S8-E7010-APP | CG-ALL-11681 | 17 | Record recovery_log as a retired legacy object, or use the dictionary name. The story names it only as a retired element in section 17. |
| CDC-19813 | RWB-S8-E7010-CON | CG-ALL-11694 | 12.7 | Record decision_record as a PLT library object created in schema rwb_deviation (local hash-linked breach entry, DP-03), alongside idempotency_key and outbox_event, so the name resolves in the dictionary. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19808 | RWB-S8-E7010-APP | GAP-1819 | 11 | Add rows in schema rwb_deviation, owner S8, for the screening run with mode, the score row per code, the contact stop, the agent feedback row and the breach record. |
| CDC-19821 | RWB-S8-E7010-CON | GAP-1819 | find it | Add S8 rows for shadow screening run, screening score, contact stop, agent feedback and breach record with key fields, in the change that writes the S8 DB story |

### RWB-S8-E7008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19754 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-21 | header | Set build status to Done once the contract is published (currently Not started). |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19755 | RWB-S8-E7008-APP | DOR-RWB-S8-E7008-APP-5 | 9 | Keep DEV_WITH_OWNER out of the closed outcome list LOV-DEV-OUTCOME; it is a deviation state, not an outcome value. No story edit. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19758 | RWB-S8-E7008-APP | CG-ALL-11633 | 12.5 | Add activity recordDeviationReview on task queue rwb-deviation as the one review step of the DeviationWorkflow stage, or name a catalogued activity. |

### OTHER:Not specified in the source documents (GAP-1488) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19763 | RWB-S8-E7008-APP | GAP-1488 | find it | Publish the override rate by decision and product with the reason mix; the review forum sets the target after the first three months of data. |

### RWB-S8-E7009-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19777 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-21 | 1 | Complete the contract story and set its build status from Not started to Done. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml; OTHER:source-data and decision yamls) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19778 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-8 | 12.1 | Add POST /cases/{caseId}/deviations and PATCH /deviations/{deviationId} with an idempotency key; add paths for bases /api/recovery/source-data/v1 and /api/recovery/decision/v1 and the 3 others named. |

### OTHER:22 Microservice Realignment/aisdlc/requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19783 | RWB-S8-E7009-APP | DOR-RWB-S8-E7009-APP-10 | 9 | SCR-08 States line (line 310, 'Loading; list.') needs empty, error and no-access states. Their content is not in the sources (DOR-RWB-S8-E7009-APP-10). |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19790 | RWB-S8-E7009-CON | CG-ALL-11672 | 13 | Create story RWB-P7-E1073-CON or name an existing story for the Drools rule evaluation in place of RWB-P7-E1073-CON. |

### RWB-S8-E7009-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19794 | RWB-S8-E7009-CON | DOR-RWB-S8-E7009-CON-10 |  | State the empty, loading, error and no-access states of SCR-06 and SCR-08 |

### RWB-S8-E7010-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19799 | RWB-S8-E7010-APP | DOR-RWB-S8-E7010-APP-8 | find it | Resolve the workflow ID form and start rule of DeviationWorkflow and the remaining detcheck findings |

### OTHER:Requirements source (14-row count) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19806 | RWB-S8-E7010-APP | DOR-RWB-S8-E7010-APP-2 | 18 | Feature column (FEAT-DVF-10) and L3 process column added; L3 value not in sources. |

### OTHER:FSD S8 Deviation handling v3 (A2.10.4.1 to A2.19.4.2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19809 | RWB-S8-E7010-APP | GAP-1824 | 7 | Keep placeholder 'Written one epic ahead' and 'None. No alternate path' unchanged until wave 4 criteria are groomed. |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; OTHER:rwb-access; OTHER:rwb-source-data; OTHER:FSD S8 Deviation handling v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19810 | RWB-S8-E7010-APP | GAP-3070 | 8 | Publish a UNIVERSAL row for a contact sent against a stop with its own ID; publish the ledger read and SCR-08 breach read; correct RW-CONDUCT; decide breach storage and event; settle the service level with DL22. |

### RWB-S8-E7010-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19818 | RWB-S8-E7010-CON | DOR-RWB-S8-E7010-CON-10 | find it | Add empty, loading, error and no-access states for SCR-06 and SCR-08 in the app story. |

### OTHER:Recovery Workbench FSD S8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19822 | RWB-S8-E7010-CON | GAP-1824 | find it | Keep placeholder criteria A2.10.4.1 to A2.19.4.1 and the None alternate rows unchanged until E7 stories are groomed |

### 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:rwb-access; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-19823 | RWB-S8-E7010-CON | GAP-3070 | find it | Publish the contact-breach UNIVERSAL rule row, ledger read, SCR-08 breach read, event decision, RW-CONDUCT right and the service level |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-1488 | The override rate is reported monthly with no target | Center of excellence analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1816 | The FSD reads the ACE views and the batch-status view directly, while Architecture v5 gives that read to rwb-source-data alone and the connection matrix gives S8 only an R and an E to P1 | Solution architect | Resolved (directive) |
| GAP-1818 | The deviation REST operations disagree between the Architecture slide, the Ownership Map and the FSD, and no read operation is recorded for the case record deviation query that the FSD times at two seconds | Solution architect | Resolved (directive) |
| GAP-1819 | The Ownership Map gives rwb-deviation one table, while the FSD and the Architecture slide require screening runs, screening scores, contact stops and a breach record as well | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1824 | All ten E7 deviation features carry the placeholder criterion 'Written one epic ahead' and no alternate flow | Business analyst, S8 with the QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3070 | RWB-S8-E7010-APP: the contact-breach path has no rule row, no column, no published ledger read, no operation of its own, no event and no write right for its primary role | Center of excellence with the solution architect, the rwb-decision rule owner, the rwb-source-data owner and the rwb-access owner | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
