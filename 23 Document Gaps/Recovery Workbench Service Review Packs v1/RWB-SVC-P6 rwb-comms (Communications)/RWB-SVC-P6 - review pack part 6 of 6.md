# RWB-SVC-P6 rwb-comms (Communications) - review pack, part 6 of 6 (RWB-P6-E4041-CON to RWB-P6-E5002-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 4 |
| Resolved in the stories | 60 |
| Cross-document (pending in another document) | 56 |
| Not applied (value not in the sources) | 11 |
| Open business decisions | 14 |
| Register gaps linked | 27 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P6-E4041-CON | 19 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4041 CON Answer a legal or audit document request - contract v2.md |
| RWB-P6-E4042-APP | 12 | 11 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4042 APP Apply retention on case closure v2.md |
| RWB-P6-E4042-CON | 9 | 9 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E4042 CON Apply retention on case closure - contract v2.md |
| RWB-P6-E5002-APP | 20 | 21 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P6 rwb-comms (Communications)/RWB P6 E5002 APP Record proof of delivery on a notice v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E6025-ITG, RWB-P3-E6025-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-09218 | GAP-1475 | Register gap | Compliance and PDPA officer | Retention periods and masking rules by record class and role are not set | Hold a retention class and a masking rule per record class and role as versioned reference data, apply the class at creation, and record every disposal as a decision so a period that is not yet set cannot be breached silently. |
| RWB-P6-E4041-CON | R-11135 | CG-ALL-6780 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4042-APP | R-11138 | CG-ALL-6787 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E4042-CON | R-11139 | CG-ALL-6794 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P6-E5002-APP | R-11143 | CG-ALL-6803 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P6-E4040-APP, RWB-P6-E4040-CON, RWB-P6-E4041-APP, RWB-P6-E4041-CON, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22551 | GAP-1607 | Register gap | Product owner | Seven features in the Communications functional specification belong to other services in Architecture v5 | Keep the seven features in the source with their identifiers, mark them as not carried in section 5.1 of this PRD with their owning service, and raise the story-level split in the service work packages. |
| RWB-ITG-E5002-ITG, RWB-P3-E5002-APP, RWB-P6-E5002-APP, RWB-S4-E5002-APP, RWB-S4-E5002-CON | R-22803 | GAP-2746 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case architect and the business owner of the notice period | The notice-period timer has no stated home and the notice period has no value in any source | Declare the proof window of 7 days and the notice period as two durable timers of LitigationWorkflow, the first started at dispatch and the second at delivered_at under R-LIT-07; read the notice period as a versioned reference row per product and notice type, carry its content as the placeholder until the business owner publishes it, hold the timer and answer no move when the row is missing, and keep the case-stage timer and the officer task rows with rwb-case on the stage outcome. |
| RWB-ITG-E3013-ITG, RWB-ITG-E5002-ITG, RWB-ITG-E6017-ITG, RWB-ITG-E6025-ITG, RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP, RWB-P3-E6025-APP, RWB-P6-E5002-APP, RWB-S2-E3013-APP, RWB-S2-E3013-CON, RWB-S4-E5002-APP, RWB-S4-E5002-CON, RWB-S7-E6017-APP, RWB-S7-E6017-CON, RWB-S7-E6025-APP, RWB-S7-E6025-CON | R-28884 | GAP-1562 | Register gap | Product owner | Four P3 slices in the wave plan carry no business requirement row | Add a BRD row per slice, or retire the slice with a recorded decision. |
| RWB-P6-E4042-APP, RWB-P6-E4042-CON | R-29006 | GAP-1144 | Register gap | Compliance and PDPA officer with the Data steward | The retention classes, the class per document type and the periods are unset and are not this service's data | Close DL26 with the retention class list and the class per document type in rwb-document as the owner of the reference data, carry the class code through the coverage read as the owner returns it, and keep every period and every disposal rule out of this service so that no story of this key validates, defaults or maps a class. |
| RWB-P6-E4042-APP, RWB-P6-E4042-CON | R-29008 | GAP-1604 | Register gap | Compliance with Legal | The retention class and period for notices, templates and merge fields are open | Declare a retention class on the notice record, the template version and the merge-field catalog as versioned data, leave the period to Compliance under DL26, and let rwb-document apply the archive and disposal. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-P6-E4042-APP, RWB-P6-E4042-CON | R-37344 | ASM-2091 | Register assumption |  | The retention class list, the class per document type and the periods are P5 rwb-document reference data and stay unset for this key (NFR-028, DL26). This story needs only the presence or the absence of a class per notice document, so a class value is carried through the coverage read as the owner returns it and is never validated, mapped, defaulted or stored here; when P5 publishes the list the coverage read carries the code and no rule of this story changes. | Compliance and PDPA officer with the Data steward when DL26 is closed. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P6-E4042-APP | R-06608 | DOR-RWB-P6-E4042-APP-23 | 12.1 | Definition of Ready item 23 Contract version fixed: Fail | No contract version found: grepped RWB P6 E4042 CON story v2 and found none. Placeholder kept; needs the owner's version value. |
| RWB-P6-E4042-APP | R-11136 | CG-ALL-6784 | 4, 12.1 | HTTP errors with no message ID: 401 no session; 404 the case is absent or out of scope; 503 the class read of the owner is unavailable. The exact field types and the page shape are fixed in the contract story and are Not specified in the source documents (GAP-1142 | Error and Message Standard v4 has no 401 or 404 message. MSG-GEN-006 (system unavailable) promises queue and retry, which a synchronous read does not do. Business analyst to confirm. |
| RWB-P6-E4042-APP | R-17826 | DOR-RWB-P6-E4042-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | States for SCR-33 and SCR-44 need section 9 text, which is not in this chunk. Resubmit with section 9. |
| RWB-P6-E4042-APP | R-17827 | DOR-RWB-P6-E4042-APP-11 | 1 | Definition of Ready item 11 Guardrails: Partial | Personal-data statement needs section 1 and Data text, which are not in this chunk. Resubmit with them. |
| RWB-P6-E4042-APP | R-17832 | DOR-RWB-P6-E4042-APP-4 | 7, 8, 16 | Definition of Ready item 4 Business rules: Partial | Criteria for BR2 to BR12 belong in section 7 and test rows in section 16, neither in this chunk. Resubmit with those sections. |
| RWB-P6-E4042-CON | R-06610 | DOR-RWB-P6-E4042-CON-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design record found in the project files by name or text search. No sign-off recorded in the story or sources, so none was written; needs the epic design record. |
| RWB-P6-E4042-CON | R-17834 | DOR-RWB-P6-E4042-CON-10 |  | Definition of Ready item 10 Screens and states: Partial | SCR-33 is Template approval in FSD P6 Communications v4 (P6, not P3), and this story has no screen. No empty, loading, error or no-access state is in the sources; none invented. |
| RWB-P6-E4042-CON | R-17835 | DOR-RWB-P6-E4042-CON-11 |  | Definition of Ready item 11 Guardrails: Partial | Personal-data class of the coverage fields is not specified in the source documents (DOR-RWB-P6-E4042-CON-11); none invented. Section 11 text is not in the chunk. |
| RWB-P6-E4042-CON | R-31404 | NEWAC-RWB-P6-E4042-CON-AC9 | 7 and 16 | AC9: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are not in the chunk, so the insert anchors cannot be verified. The proposed test is not specified in the source documents (NEWAC-RWB-P6-E4042-CON-AC9). |
| RWB-P6-E5002-APP | R-17843 | DOR-RWB-P6-E5002-APP-11 | find it | Definition of Ready item 11 Guardrails: Partial | Data Classification v5 (pipeline cache): barcode is an indirect identifier; sent_date, callback_date, delivery_status are customer data (DF-LEG-019 to 022). The 'none carried' statement is not in the parts supplied. |
| RWB-P6-E5002-APP | R-22766 | GAP-0436 | find it | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Harness values for W3J01 are not in the sources and W3J01 is not in this story. Agree at the wave 3 entry check with the integration lead. No edit here. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml (16)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11484 | RWB-P6-E4041-CON | CG-ALL-6776 | 12.1 | Publish POST /api/recovery/comms/v1/cases/{caseId}/document-requests with the shape, statuses and idempotency stated in section 12.1. |
| CDC-11485 | RWB-P6-E4041-CON | CG-ALL-6777 | 12.1 | Publish GET /api/recovery/comms/v1/document-requests/{requestId} with the shape and statuses stated in section 12.1. |
| CDC-11487 | RWB-P6-E4041-CON | DOR-RWB-P6-E4041-CON-8 | 12.1, 12.3 | Publish the two operations of section 12.1 in rwb-comms.yaml. Event name in 12.3 already corrected to rwb.decision.DecisionRecorded.v1. |
| CDC-11491 | RWB-P6-E4042-APP | CG-ALL-6783 | 12.1 | Publish GET /api/recovery/comms/v1/cases/{caseId}/retention-coverage in the owner's yaml, or remove it from section 12.1. |
| CDC-11495 | RWB-P6-E4042-APP | DOR-RWB-P6-E4042-APP-8 | 12.1 | Publish GET /cases/{caseId}/retention-coverage (see CG-ALL-6783). |
| CDC-11502 | RWB-P6-E4042-CON | CG-ALL-6791 | 12.1 | Publish GET /api/recovery/comms/v1/cases/{caseId}/retention-coverage with the 200, 401, 403, 404 and 503 responses of section 12.1. |
| CDC-11503 | RWB-P6-E4042-CON | DOR-RWB-P6-E4042-CON-8 | 12.1 | Publish GET /api/recovery/comms/v1/cases/{caseId}/retention-coverage with the 200, 401, 403, 404 and 503 responses of section 12.1. |
| CDC-11511 | RWB-P6-E5002-APP | CG-ALL-6798 | 12.1 | Publish POST /api/recovery/comms/v1/notices/{noticeId}/proof-of-delivery through the owner's contract story, or remove the operation from RWB-P6-E5002-APP section 12.1. |
| CDC-20910 | RWB-P6-E4042-CON | R-06613 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20911 | RWB-P6-E4041-CON | R-01747 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20912 | RWB-P6-E4041-CON | R-01748 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20914 | RWB-P6-E4042-APP | R-06609 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20915 | RWB-P6-E4042-CON | R-23119 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20917 | RWB-P6-E4042-CON | R-01751 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20918 | RWB-P6-E4042-APP | R-01750 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |
| CDC-20919 | RWB-P6-E4041-CON | R-06603 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-01742', 'R-01743', 'R-01747', 'R-01748', 'R-01750', 'R-01751', 'R-06599', 'R-06603', 'R-06609', 'R-06613', 'R-2 |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11490 | RWB-P6-E4041-CON | CG-ALL-6779 | 16 | On tab Story test cases, add rows for TC-E4-041-01 to TC-E4-041-04 and TC-P6-E4041-CON-01 to TC-P6-E4041-CON-06, with Given, When and Then copied from the criterion each covers. |
| CDC-11496 | RWB-P6-E4042-APP | CG-ALL-6785 | 16 | Add rows TC-E4-042-01 to TC-E4-042-04 in the next version, with Given, When and Then from the covered criteria. |
| CDC-11497 | RWB-P6-E4042-APP | DOR-RWB-P6-E4042-APP-12 | 12, 12.7, 16, 18 | Add TC-E4-042-01 to TC-E4-042-06 under the same IDs with Given, When and Then. |
| CDC-11508 | RWB-P6-E4042-CON | CG-ALL-6792 | 16 | Add rows for the twelve listed cases, with Given, When and Then copied from the criterion each covers, and a row for TC-P6-E4042-CON-10. |
| CDC-11518 | RWB-P6-E5002-APP | CG-ALL-6801 | 16 | Add rows TC-E5-002-01 to -06 with Given, When and Then from the criteria they cover; also add TC-E5-002-07 and -08 added in section 16. |

### RWB-S4-E5002-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11514 | RWB-P6-E5002-APP | DOR-RWB-P6-E5002-APP-22 | header | Record the published fake library version for the contract this story consumes. |
| CDC-11516 | RWB-P6-E5002-APP | GAP-1741 | header | Publish the notice contract, its fake and its schema as slice 2.1 in wave 2, before the wave 3 build. |
| CDC-11521 | RWB-P6-E5002-APP | GAP-0437 | 11 | Publish the proof-record operation with path, request and answer shapes and error envelopes; add notice lifecycle state and three case notice facts to LDM with field IDs; add LOV-DELIVERY mapping and notice-period and proof-window reference rows with codes; record in P6 and S4 appendices that the v_ace_pod loop is the Epic 2 dispatch story. |
| CDC-11523 | RWB-P6-E5002-APP | GAP-1189 | find it | Name the proof-record operation with its request (notice reference, case reference, delivery status, delivered or callback date, barcode where required), its answer (outcome, rule ID, package version), its error envelope and the no-response answer. |

### Epic design record (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11486 | RWB-P6-E4041-CON | DOR-RWB-P6-E4041-CON-14 | header | Record the signed epic design sign-off for EP04 in the epic design record so RWB-P6-E4041-CON can pass Definition of Ready item 14. |
| CDC-11492 | RWB-P6-E4042-APP | DOR-RWB-P6-E4042-APP-14 | header | Record the signed epic design sign-off for EP04. |
| CDC-11513 | RWB-P6-E5002-APP | DOR-RWB-P6-E5002-APP-14 | header | Record the signed epic design sign-off for RWB-P6-E5002-APP. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11501 | RWB-P6-E4042-APP | CG-ALL-6786 | 18 | Align the REQ-DCM-010 and REQ-DCM-016 test lists with section 18 of RWB-P6-E4042-APP in the next RTM version. |
| CDC-11509 | RWB-P6-E4042-CON | CG-ALL-6793 | 18 | Align the RTM test lists for REQ-DCM-010 and REQ-DCM-016 with section 18 of this story in the next RTM version. |
| CDC-11526 | RWB-P6-E5002-APP | CG-ALL-6802 | 18 | Align the REQ-OCC-003 test list between section 18 (TC-E5-002-01 to -03) and the RTM (TC-E1-055-02, -05, -11, TC-E2-021-01 to -03) in the next versions. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11488 | RWB-P6-E4041-CON | CG-ALL-6774 | 4, 11 | Add document_request as a P6 (rwb_comms) table, new in this baseline, with the columns given in section 11. |
| CDC-11489 | RWB-P6-E4041-CON | CG-ALL-6775 | 4, 11 | Add document_request_entry as a P6 (rwb_comms) table, new in this baseline, with the columns given in section 11. |

### RWB-P6-E4042-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11493 | RWB-P6-E4042-APP | DOR-RWB-P6-E4042-APP-21 | header | Set build status to Done with the contract published. |
| CDC-11494 | RWB-P6-E4042-APP | DOR-RWB-P6-E4042-APP-22 | 12.1 | Publish the contract fake library and record its published version. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11504 | RWB-P6-E4042-CON | DOR-RWB-P6-E4042-CON-12 | 16 | Add rows TC-E4-042-01 to -04 and TC-P6-E4042-CON-01 to -09 to Story test cases; align the section 18 test lists with RTM v7. |
| CDC-11519 | RWB-P6-E5002-APP | DOR-RWB-P6-E5002-APP-12 | 16, 18 | Add TC-E5-002-01 to -08 to Story test cases in Test Cases v8; align the section 18 test lists for this story with RTM v7. |

### RWB-P6-E4042-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11498 | RWB-P6-E4042-APP | GAP-1141 | find it | Fix the rwb-document retention-class read path and answer in RWB-P6-E4042-CON; record in the Service Contract Catalog that rwb-comms reads a class and never sets one. |

### OTHER:rwb-comms OpenAPI file; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11499 | RWB-P6-E4042-APP | GAP-1142 | find it | Add GET /cases/{caseId}/retention-coverage on /api/recovery/comms/v1 with its five entry elements and the presence boolean; settle field types, page shape and optional class code at the RWB-P6-E4042-CON review. |

### OTHER:rwb-case contract; RWB-P6-E4042-CON; 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11500 | RWB-P6-E4042-APP | GAP-1143 | find it | Publish one case-fact operation carrying case ID and RETENTION_CLASS_MISSING that holds closure and raises the Document Hub task with 5 working days; declare it in RWB-P6-E4042-CON with a placeholder body. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11505 | RWB-P6-E4042-CON | GAP-1141 | 11 | Record that rwb-comms reads a retention class from rwb-document and never sets one; add the rwb-document class read as a consumed C row of RWB-P6-E4042-APP once P5 publishes the operation. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11506 | RWB-P6-E4042-CON | GAP-1142 | 11 | Add GET /cases/{caseId}/retention-coverage on /api/recovery/comms/v1 with its five elements and boolean presence fact; settle field types, page shape and optional class code in the baseline review. |

### OTHER:rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11507 | RWB-P6-E4042-CON | GAP-1143 | 11 | Fix one case-fact operation carrying case ID and reason RETENTION_CLASS_MISSING that holds closure and raises the Document Hub task with 5 working days; publish its missing-class message standard. |

### OTHER:Functional Specification Document P6 (A2.21.3.3; OTHER:A2.21.4.4) and legacy RWB-E4-042 Screen and states (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11510 | RWB-P6-E4042-CON | GAP-1145 | 8 | Keep SCR-33 with the template capability of the same module and show its coverage on the case record documents panel via the gateway-bff composite route. Record AC-BG-P6-021-01 as a copy of AC-BG-P6-020-01 under notice dispatch, not a retention run. |

### API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11512 | RWB-P6-E5002-APP | CG-ALL-6799 | 12.2 | Declare REST base /api/recovery/litigation/v1 for rwb-litigation, as given in the Document Index service table. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11515 | RWB-P6-E5002-APP | GAP-1740 | 12.1 | Align notice paths: S4 owns decision, approval and notice period; rwb-comms owns template, delivery and proof of delivery. Story POST row updated. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11517 | RWB-P6-E5002-APP | CG-ALL-6797 | 12.7 | Record decision_record as a library table created in rwb_comms by the library migration (DP-03), with its name and owner, in that document. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11520 | RWB-P6-E5002-APP | DOR-RWB-P6-E5002-APP-7 | 11 | Register decision_record as a platform library object created in rwb_comms (DP-03), so that the name in §11 resolves to a defined entity or field. |

### OTHER:EP05 PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11522 | RWB-P6-E5002-APP | GAP-0737 | find it | Attach the REQ identifier to FEAT-LIT-02 (C1); publish the S4 answer on /api/recovery/litigation/v1 in RWB-S4-E5002-CON; put the notice-period duration in a SERVICE_LEVEL reference row of rwb-case, owner RW-COE. |

### OTHER:rwb-case contract story (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11524 | RWB-P6-E5002-APP | GAP-2745 | find it | Name the case read and the case-stage answer when that story is written; treat PROOF_OF_DELIVERY_RECEIVED, PROOF_WINDOW_EXPIRED and DELIVERY_FAILED as workflow signals, not Kafka subscriptions, with one hop and a 2 s budget. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11525 | RWB-P6-E5002-APP | GAP-2748 | 13 | Record DP-04 with contracts RWB-PLT-E1072-CON and RWB-P7-E1073-CON; the rwb-decision package read stays on the S4 slice, and no rule row is authored in this key. |

### OTHER:FSD P6 Communications (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11527 | RWB-P6-E5002-APP | GAP-1194 | 18 | Record that the officer-recorded path is the manual correction path of the same notice; the automatic v_ace_pod read stays in RWB-P6-E2021-APP and RWB-P6-E1055-APP. |

### OTHER:split_plan.json (next plan revision) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11528 | RWB-P6-E5002-APP | GAP-1191 | 12 | Add DP-11 to the pattern set of RWB-E5-002 slices that consume or serve a contract; the Patterns applied row stays unchanged until then. |

### OTHER:Candidate gap and assumption registers; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11529 | RWB-P6-E5002-APP | GAP-1193 | 7 | Quote ACs as 'RWB-P6-E5002-APP ACn' in registers, RTM and the test-case Covers column; section 16 text is not in this chunk. |

### OTHER:Epics 3 to 8 PRD and S4 module trace (EP05) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11530 | RWB-P6-E5002-APP | GAP-2747 | 18 | Add one requirement row for the proof of delivery as the start of the notice period, then rewrite the requirement column of both stories. |

### OTHER:split_plan.json and WP B-P6-04 (plan regeneration) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-11531 | RWB-P6-E5002-APP | GAP-1190 | header | Add H RWB-PLT-E1027-CON and H RWB-PLT-N001-CON to this story's build dependencies when the plan is regenerated. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0436 | Wave 3 journey harness pack, seeded identifiers, fixed business date, product codes, unnamed operations, evidence format and gate thresholds are not specified | Integration lead | Resolved (directive) |
| GAP-0437 | The legacy delivery step is split across rwb-comms, rwb-litigation and rwb-case with no named hand-off operation and no named reference rows, so the end-to-end chain of RWB-E5-002 has no single source of record | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0737 | The split of the proof-of-delivery key between rwb-case, rwb-litigation and rwb-comms, the S4 answer, the notice-period duration and the requirement ID are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1141 | Retention is module P6 in the story and P5 rwb-document in the ownership map, and no C row declares the retention contract | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1142 | No source names a retention-coverage operation, its answer shape or its access right | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1143 | The hold of the closure and the Document Hub task of R-WO-48 have no operation, no body and no message | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1145 | Screen SCR-33, the legacy permission checks and the FSD background-event row do not fit an unattended retention check | Solution architect | Resolved (directive) |
| GAP-1151 | No published rwb-document operation for the discovery production, and no C row for the document contract this key reads | Solution architect | Resolved (directive) |
| GAP-1152 | No document-request operation, answer shape, decision code or rule id in any source | Tech lead | Resolved (directive) |
| GAP-1153 | Selector conflict: REQ-DCM-017 asks for a named population and the legacy story answers per case | Solution architect | Resolved (directive) |
| GAP-1154 | The legacy rows of RWB-E4-041 are carried over from notice generation | Business analyst | Resolved (directive) |
| GAP-1155 | The answer format and the protection of a produced document are not stated | Solution architect | Resolved (directive) |
| GAP-1189 | The proof-record operation of RWB-S4-E5002-CON is not named in the source documents | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1190 | The platform contract rows that DP-03 and DP-19 add are not in this story's build list | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1191 | DP-11 is absent from the pattern set of a story that consumes one published operation | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1192 | The meaning of the two unexercised LOV-DELIVERY values, and the contract the list is read on, are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1193 | The labels AC1 to AC8 are reused by three documents of the same legacy key for different criteria | Business analyst, P6 | Resolved (directive) |
| GAP-1194 | The source reads the proof of delivery from v_ace_pod in process, and this story may read no ACE view | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1195 | The proof-record path, its fields and its right are this story's design, because no source names a proof-record operation | Solution architect | Resolved (directive) |
| GAP-1597 | Proof of delivery is this service's in Architecture v5 and a read of an ACE view in the functional specification | Solution architect with the ACE team | Resolved (directive) |
| GAP-1740 | The notice and its proof of delivery sit in S4 in the FSD and in rwb-comms in Architecture v5 and the Ownership Map, and the three notice paths are split across the two services | Solution architect | Resolved (directive) |
| GAP-1741 | The notice capability is first needed in Epic 2 (wave 2, 31 December 2026 (tentative)) while the service is created in wave 3 | Solution architect | Resolved (directive) |
| GAP-1748 | The message wording and the Thai and English versions of the S4 messages are not in the FSD | Business analyst, S4 | Resolved (directive) |
| GAP-2744 | The delivery fact has no home in rwb-litigation and no published operation on any of the three services it crosses | Solution architect, S4 rwb-litigation, with the P1 rwb-source-data and P6 rwb-comms architects | Resolved (directive) |
| GAP-2745 | The proof of delivery is named as an event in the rules and the FSD, while the service publishes and consumes nothing and the case answer has no operation name | Solution architect, S4 rwb-litigation, with the P3 rwb-case and P6 rwb-comms architects and the event platform team | Resolved (directive) |
| GAP-2747 | The legacy master carries no requirement identifier for RWB-E5-002, so both stories trace to the feature and one module requirement | Business analyst, S4 rwb-litigation, with the PRD owner of EP05 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2748 | The rule package that decides the three rules is a consumed contract of another service with no dependency row and no pattern in the set | Solution architect, S4 rwb-litigation, with the P7 rwb-decision architect and the platform rule-kit owner | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
