# RWB-ITG-W1 Wave 1 integration - review pack, part 3 of 5 (RWB-ITG-E1030-ITG to RWB-ITG-E1050-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 10 |
| Resolved in the stories | 158 |
| Cross-document (pending in another document) | 165 |
| Not applied (value not in the sources) | 8 |
| Open business decisions | 31 |
| Register gaps linked | 150 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E1030-ITG | 21 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1030 ITG Daily rebalancing and queue measures - integration v2.md |
| RWB-ITG-E1031-ITG | 12 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1031 ITG Queue and owner on the case list with filters - integration v2.md |
| RWB-ITG-E1032-ITG | 21 | 34 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1032 ITG Automatic attach from the OCR intake - integration v2.md |
| RWB-ITG-E1034-ITG | 16 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1034 ITG Letter template management - integration v2.md |
| RWB-ITG-E1037-ITG | 20 | 31 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1037 ITG Role to permission matrix as data and PDPA field masking by role - integration v2.md |
| RWB-ITG-E1039-ITG | 18 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1039 ITG Access log into the decision log and break-glass admin - integration v2.md |
| RWB-ITG-E1046-ITG | 11 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1046 ITG Template and merge field catalog as data - integration v2.md |
| RWB-ITG-E1047-ITG | 10 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1047 ITG Feature flags for module release with a removal date - integration v2.md |
| RWB-ITG-E1049-ITG | 13 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1049 ITG OCR pipeline on the Workbench document hub - integration v2.md |
| RWB-ITG-E1050-ITG | 16 | 12 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1050 ITG Document classification - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-P3-E1050-APP, RWB-P5-E1049-APP, RWB-P5-E1049-CON, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1053-CON, RWB-P6-E1049-APP | R-09185 | GAP-1586 | Register gap | Solution architect with the AI product owner | The OCR, classification and extraction services are named as external pieces but no source names them or their owner | The PRD keeps the pipeline behaviour in P5 and states the OCR, classification and extraction engines as an external contract reached as an AgentRunCompleted event or a Temporal child run, with the provider, the contract and the version scheme carried as OQ-P5-06. |
| RWB-ITG-E1032-ITG | R-09352 | CG-ALL-314 | Script gap | Product owner | Open decision DL21 has no assumption | Owner rules DL21; until then build on the recommended option. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E2014-ITG, RWB-ITG-E2021-ITG, RWB-ITG-E2022-ITG, RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P3-E1052-APP, RWB-P3-E1055-APP, RWB-P3-E2014-APP, RWB-P3-E2021-APP, RWB-P4-E2014-APP, RWB-P4-E2021-APP, RWB-P4-E2022-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E1055-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P6-E2014-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-P7-E1046-APP, RWB-P7-E1052-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS, RWB-P7-E2021-APP, RWB-P7-E2022-APP | R-22077 | GAP-1614 | Register gap | Business lead with Legal counsel and the rwb-comms owner | Notice generation, letter templates, the template catalog and proof of delivery are built in P7 while the ownership ruling gives notices and templates to rwb-comms | Move FEAT-DRI-14 to FEAT-DRI-17 and A2.10 to A2.13 with their acceptance criteria to the rwb-comms and rwb-document documents, keep FEAT-APD-08 and AC-P7-022-01 to AC-EXC-P7-022-04 here as the notice approval, and correct TSD P7 T5.2 so that the notice is reached through the rwb-comms contract. |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22078 | GAP-1595 | Register gap | Product owner | The document module is said to own the letter templates and their fields, while Architecture v5 gives templates and merge fields to rwb-comms | Hold the template record, its versions and the Legal approval in rwb-comms, hold the merge-field catalog in rwb-comms, and keep the template body file in rwb-document as a document with a reference on the template row; record DL28 as superseded by D-RCV-60 and close it with the product owner. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2014-ITG, RWB-P3-E2014-APP, RWB-P4-E2014-APP, RWB-P6-E1034-APP, RWB-P6-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P7-E2014-OPS | R-22079 | GAP-1606 | Register gap | Product owner with Legal counsel | It is not stated whether the approval is taken on a template version or on a generated notice | Record the Legal approval on the template version as a decision record written through rwb-decision, and take the notice approval for the demand and recall types through the approval workflow on the generated notice; state both in the story's acceptance criteria. |
| RWB-ITG-E1034-ITG, RWB-ITG-E2021-ITG, RWB-P1-E2021-APP, RWB-P3-E2021-APP, RWB-P4-E2021-APP, RWB-P6-E1034-APP, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P7-E2021-APP | R-22081 | GAP-1598 | Register gap | Product owner with the solution architect | Two of the module's business requirements describe the case record view and the case timeline, which the case service owns | Read both requirements as this service's contribution to the case record view: the notice and message block with its states, and the ordered notice and message history. The view, the timeline and the timer projection stay with rwb-case; the ledger entries stay with rwb-source-data. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22104 | GAP-2037 | Register gap | Architecture with Compliance | Two sources disagree on who applies the mask: rwb-source-data or each service | Both controls are kept and written as defence in depth: rwb-source-data masks in the view and in its contract, and each service re-applies the masking_rule rows of rwb-access before the response leaves. The story RWB-P4-E1037-APP owns the profile; the P1 story owns the view mask. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22105 | GAP-2136 | Register gap | Compliance | The plan does not say which service applies the mask once the masking rules are rwb-access data | rwb-access holds the approved masking version; rwb-source-data applies the mask at the 30 views; display masking at the API is applied by the service that owns the field, under the same version. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-22113 | GAP-1570 | Register gap | Compliance with the solution architect | The access log has no stated retention, no stated searchable period, no stated storage object and no stated cross-service read right, although it is the evidence for every access question | Answer DL26 for the access log in one row: the retention period, whether it equals the decision log period, which object answers the query (the local record, the central ledger, or a projection of both), which fields are searchable and for how far back, and which roles in other services may read it. Until then this PRD keeps the classification at PII and marks the retention as not set. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-22125 | GAP-2089 | Register gap | Product owner; service owners of P6 rwb-comms and P5 rwb-document | The Decision Log gives the letter templates to the document module, while Architecture v5 and the Ownership Map give them to rwb-comms | Follow Architecture v5 and the Ownership Map: templates and merge fields are P6 rwb_comms. Record the DL28 answer as a gap and ask the product owner to reaffirm or amend DL28 before the template story is Done. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28578 | GAP-0162 | Register gap | Product head (Mortgage, HP, SSME) | The DoA limit amounts are not in this document | v5 names the owner (P4), the table (delegation_limit) and the two operations that serve it; the amounts stay in the Delegation of Authority Matrix and the DoA rule package and no amount is copied into this document. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28579 | GAP-0163 | Register gap | Compliance and PDPA officer | The masking rules per role, area and field group are not in this document | v5 names P4 as owner of masking_rule and GET /masking-policies as the contract; the rule values stay with Compliance and are loaded as a versioned reference data set. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28585 | GAP-2048 | Register gap | P4 rwb-access with Compliance | The alert recipient roles of version 3 are not mapped to role codes in rwb-access | The six recipient names are kept as they are and read as role names; the role codes are settled with the rwb-access role model before the per-service alert rules are built, and no code is invented here. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1038-APP | R-28587 | GAP-1579 | Register gap | Solution architect with Risk | No performance target covers the authorise answer, although every request passes one, and the nearest targets belong to other objects | Set one target for the authorise answer at the busiest hour, with the cache hit and the miss stated separately, and record it under DL11 beside the screen and rule-evaluation targets, so NFR-P4-001 becomes a testable number. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28588 | GAP-1576 | Register gap | Compliance with the solution architect | REQ-ACA-006 still requires an access entry for every read of the data lake copy, which Architecture v5 removes | Re-issue REQ-ACA-006 and NFR-042 in the next business requirement version as 'every read of the case store, the document store and a data product', so the requirement, the functional specification and this PRD use one list of objects; nothing else in the requirement changes. |
| RWB-ITG-E1039-ITG, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28591 | GAP-1591 | Register gap | Compliance and PDPA officer | NFR-042 still requires logging the data lake copy of the document store although the data lake is removed | The PRD requires every read of a document and of its extracted fields to be logged and carries no lake clause. NFR-042 needs the same correction in its next version. |
| RWB-ITG-E1046-ITG, RWB-P5-E1046-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P7-E1046-APP | R-28596 | GAP-2098 | Register gap | Service owner of P6 rwb-comms; Compliance and Legal roles | The Compliance approval of customer wording has no artefact in the target template | Record the Compliance approval as a second approval of P7 with the template as its source, and keep approved_by_legal on the template row for the Legal approval that the endpoint records. |
| RWB-ITG-E1032-ITG | R-33382 | ASM-ALL-314 | Script assumption |  | Built on the recommended option of DL21: A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead rules DL21 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1011-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2009-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2031-ITG, RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P10-E1063-APP, RWB-P10-E2031-APP, RWB-P2-E2007-APP, RWB-P3-E1002-APP, RWB-P3-E1011-APP, RWB-P3-E1013-APP, RWB-P3-E1030-APP, RWB-P3-E1030-CON, RWB-P3-E2007-APP, RWB-P3-E2009-APP, RWB-P6-E1011-APP, RWB-P7-E1030-APP, RWB-P7-E2007-APP, RWB-P7-E2008-APP, RWB-P8-DM013-APP, RWB-P8-E2008-APP, RWB-P9-E2009-APP, RWB-P9-E2009-CON, RWB-P9-E2009-OPS, RWB-S2-E2007-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-S5-E1011-APP, RWB-S8-E2009-APP | R-35389 | ASM-2602 | Register assumption |  | The daily case list reconciliation reports variance by data product with no tolerance until DL25 is decided, and the agreed tolerance is applied by version once it is set. | Data steward and data product owner |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-E1034-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E2017-ITG, RWB-P3-E1045-APP, RWB-P5-E1046-APP, RWB-P5-E1052-APP, RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P6-AD017-APP, RWB-P6-AD017-CON, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1046-CON, RWB-P6-E2017-APP, RWB-P6-E2026-APP, RWB-P7-E1046-APP, RWB-P7-E2026-APP, RWB-S2-E2017-APP | R-35450 | ASM-2727 | Register assumption |  | The template record, its versions and the Legal approval are held in rwb-comms, the merge-field catalog is held in rwb-comms, and the template body file is held in rwb-document with a reference on the template row. | Product owner, before wave 1 release |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |
| RWB-ITG-TE010-ITG, RWB-ITG-E1047-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P3-E1042-APP | R-35662 | ASM-3199 | Register assumption |  | The six open-point rows that named an individual (DL03, DL04, DL05, DL06, DL07, DL37) carry the Template and Rules R9 placeholder in the Owner column, with the organisation the same row already stated kept after it, and the five roles of section 9 are left as the only owner labels in the document. | Confirm the role that owns each of the six open points. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E1037-ITG | R-03549 | DOR-RWB-ITG-E1037-ITG-16 | Header | Definition of Ready item 16 Size: Fail | No size value exists in the sources, so the squad must set it at refinement. |
| RWB-ITG-E1037-ITG | R-14004 | DOR-RWB-ITG-E1037-ITG-15 | Header | Definition of Ready item 15 INVEST: Partial | The INVEST small criterion cannot be confirmed until the squad sets the size. |
| RWB-ITG-E1046-ITG | R-03559 | DOR-RWB-ITG-E1046-ITG-16 |  | Definition of Ready item 16 Size: Fail | No size for RWB-ITG-E1046-ITG or legacy RWB-E1-046 in story, plan or *E1-046*.md files (Size/Estimate/points grep). The squad sets it at refinement. |
| RWB-ITG-E1046-ITG | R-14020 | DOR-RWB-ITG-E1046-ITG-15 |  | Definition of Ready item 15 INVEST: Partial | No estimate for RWB-ITG-E1046-ITG or RWB-E1-046 in md/csv/json sources, so 'fits two weeks' would be invented. The squad judges it at refinement. |
| RWB-ITG-E1047-ITG | R-03564 | DOR-RWB-ITG-E1047-ITG-16 | header | Definition of Ready item 16 Size: Fail | The header records that the story is not sized. The squad must size it at refinement before this item can pass. |
| RWB-ITG-E1047-ITG | R-14029 | DOR-RWB-ITG-E1047-ITG-17 | header | Definition of Ready item 17 Dependencies: Partial | RWB-P1-E1001-APP and RWB-PLT-E1047-APP stay listed as integration dependencies. Build dependency stays None, consistent with Ready to start Day 1; confirm at refinement. |
| RWB-ITG-E1049-ITG | R-03569 | DOR-RWB-ITG-E1049-ITG-16 | header | Definition of Ready item 16 Size: Fail | No estimate is available; the squad sizes the story at refinement. |
| RWB-ITG-E1049-ITG | R-14035 | DOR-RWB-ITG-E1049-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | The Small criterion cannot be confirmed without a size; the squad sizes the story at refinement (DOR-16). |

## 5. Cross-document changes (pending in the target document)


### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00585 | RWB-ITG-E1031-ITG | CG-ALL-309 | 16 | Add rows for TC-ITG-E1031-ITG-10 with Given, When and Then copied from the criterion it covers (AC10, NFR). Owner: QA. |
| CDC-00587 | RWB-ITG-E1031-ITG | DOR-RWB-ITG-E1031-ITG-12 | 16 | Add the row for TC-ITG-E1031-ITG-10 (same change as CG-ALL-309). |
| CDC-00626 | RWB-ITG-E1034-ITG | CG-ALL-315 | 16 | Add rows for TC-ITG-E1034-ITG-12 with Given, When and Then copied from AC12 in section 7. |
| CDC-00629 | RWB-ITG-E1034-ITG | DOR-RWB-ITG-E1034-ITG-12 | 16 | Section 16 now lists 14 cases. The missing row for TC-ITG-E1034-ITG-12 belongs in Test Cases v8 (owner QA). |
| CDC-00641 | RWB-ITG-E1037-ITG | CG-ALL-319 | 16 | Test Cases needs a new version with TC-E1-037-13-ITG, 14-ITG and 15-ITG, and also the new 16-ITG and 17-ITG rows in section 16 of the story. |
| CDC-00643 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-12 | 16 | Add test cases TC-E1-037-13-ITG, TC-E1-037-14-ITG and TC-E1-037-15-ITG, which are in section 16 of this story. |
| CDC-00668 | RWB-ITG-E1039-ITG | CG-ALL-323 | 16 | Add a row for TC-ITG-E1039-ITG-08 with Given, When and Then copied from AC8. |
| CDC-00670 | RWB-ITG-E1039-ITG | DOR-RWB-ITG-E1039-ITG-12 | 16 | Add a row for TC-ITG-E1039-ITG-08 with Given, When and Then copied from AC8. |
| CDC-00687 | RWB-ITG-E1046-ITG | CG-ALL-327 | 16 | Add rows TC-ITG-E1046-ITG-10 (from AC9) and TC-ITG-E1046-ITG-11 (from AC10) with Given, When and Then copied from those criteria. |
| CDC-00689 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-12 | 16 | Section 16 holds the test cases, including the new TC-12 and TC-13. Rows missing from Test Cases v8 must be added there (see also CG-ALL-327). |
| CDC-00705 | RWB-ITG-E1047-ITG | CG-ALL-331 | 16 | Add a Story test cases row for TC-ITG-E1047-ITG-11 with Given, When and Then copied from AC11 in section 7. |
| CDC-00707 | RWB-ITG-E1047-ITG | DOR-RWB-ITG-E1047-ITG-12 | 16 | Add a Story test cases row for TC-ITG-E1047-ITG-11 with Given, When and Then copied from AC11 in section 7. |
| CDC-00715 | RWB-ITG-E1049-ITG | CG-ALL-335 | 16 | Add rows TC-ITG-E1049-ITG-11 (AC1) and TC-ITG-E1049-ITG-12 (AC10) with Given, When and Then copied from the criteria they cover |
| CDC-00717 | RWB-ITG-E1049-ITG | DOR-RWB-ITG-E1049-ITG-12 | 16 | Section 16 lists 13 test cases; TC-ITG-E1049-ITG-11, TC-ITG-E1049-ITG-12 and the new TC-ITG-E1049-ITG-13 need rows in Test Cases v8. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00578 | RWB-ITG-E1030-ITG | DOR-RWB-ITG-E1030-ITG-1 | 1 | Register 'QA integration engineer' as a role (code and name) in v5, or confirm the existing role to use in section 1 and section 9. |
| CDC-00586 | RWB-ITG-E1031-ITG | DOR-RWB-ITG-E1031-ITG-1 | 1 | Add the role 'QA integration engineer' with a role code, or confirm the existing role to use in section 1. |
| CDC-00595 | RWB-ITG-E1032-ITG | DOR-RWB-ITG-E1032-ITG-1 | 1 | Add a role code and name for 'QA integration engineer', or confirm an existing listed role for section 1. |
| CDC-00627 | RWB-ITG-E1034-ITG | DOR-RWB-ITG-E1034-ITG-1 | 1 | Add QA integration engineer as a role name, or confirm the existing role it maps to, so section 1 matches it. |
| CDC-00642 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-1 | 1 | Add QA integration engineer as a role name, or give the role code the story should use |
| CDC-00661 | RWB-ITG-E1037-ITG | GAP-0166 |  | Six SY actors resolved through POST /authorise with their SY role code and managed identity as subject; credential type left to the P4 contract story |
| CDC-00662 | RWB-ITG-E1037-ITG | GAP-0168 |  | Carry the four Key tab scope values (Own, Team, All, Placed cases) unchanged; revise only when the P4 and P3 design decides on a region predicate |
| CDC-00669 | RWB-ITG-E1039-ITG | DOR-RWB-ITG-E1039-ITG-1 | 1 | Register the role 'QA integration engineer' with a role code, or the story must use an existing role code and name. |
| CDC-00688 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-1 | 1 | Add the role name 'QA integration engineer' used in section 1 and the role table, or align the story to the existing QA role name. |
| CDC-00706 | RWB-ITG-E1047-ITG | DOR-RWB-ITG-E1047-ITG-1 | 1 | Add role 'QA integration engineer' or confirm the role code it maps to. |
| CDC-00716 | RWB-ITG-E1049-ITG | DOR-RWB-ITG-E1049-ITG-1 | 1 | Add the QA integration engineer role, with its role code, to Users Roles and Permissions v5 |
| CDC-00729 | RWB-ITG-E1050-ITG | DOR-RWB-ITG-E1050-ITG-1 | 1 | Add a role for 'QA integration engineer' (or map it to an existing role code) so section 1 can name a role that exists. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00579 | RWB-ITG-E1030-ITG | GAP-2205 | 13 | Add rows for the reporting feed (queue, ageing and breach measures and fields), the delivery service for MSG-P3-028, MSG-P3-011 and MSG-P3-029, and the run record and rerun surface. |
| CDC-00649 | RWB-ITG-E1037-ITG | GAP-0164 |  | Record that PT role rows, letters and default scope stay with P4, while S9 holds partner_user and the user-to-role link and asks POST /authorise with the PT role code. |
| CDC-00659 | RWB-ITG-E1037-ITG | GAP-2039 |  | Add an access_log row to the Tables sheet with owner P4 rwb-access, at the next revision. |
| CDC-00665 | RWB-ITG-E1037-ITG | GAP-2063 |  | Add owner rows for gateway-bff (screen response composition, owner RWB-PLT-EDGE) and the partner gateway (owner RWB-PLT-EDGE, behind S9 rwb-partner) at the next revision. |
| CDC-00679 | RWB-ITG-E1039-ITG | GAP-2039 | not in chunk | Add an access_log row to the Tables sheet with owner P4 rwb-access and ACE DBA as DBA; key and retention class Not specified in the source documents (GAP-2039); own DB story in RWB-SVC-P4. |
| CDC-00681 | RWB-ITG-E1039-ITG | GAP-0165 | 8 | Add a P4 access log row for rwb_access: append-only, created by RWB-P4-E1039-DB; define its columns, retention and hash rule there. |
| CDC-00682 | RWB-ITG-E1039-ITG | GAP-2069 | 8 | Add an access_log table entry owned by P4 in rwb_access, append-only with a hash chain, read through GET /admin/access-log. |
| CDC-00708 | RWB-ITG-E1047-ITG | GAP-1411 | header | Record the schema name RWB-PLT-DB allocates for the platform flag store and the deployment of its admin component on the rwb-integration platform route. |
| CDC-00710 | RWB-ITG-E1047-ITG | GAP-1667 | header | Add a platform row for the flag store and name the component that serves the four feature-flag paths. |
| CDC-00734 | RWB-ITG-E1050-ITG | GAP-2133 |  | Story does not reference rwb-valuation; no story edit. |

### Epic design record (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00575 | RWB-ITG-E1030-ITG | DOR-RWB-ITG-E1030-ITG-14 | none | Record the signed epic design sign-off for EP01 against RWB-ITG-E1030-ITG. No sign-off is in the story or source documents. |
| CDC-00583 | RWB-ITG-E1031-ITG | DOR-RWB-ITG-E1031-ITG-14 | 1 | Confirm and record the signed epic design for RWB-ITG-E1031-ITG. |
| CDC-00590 | RWB-ITG-E1032-ITG | DOR-RWB-ITG-E1032-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-W1 and EP01 in the epic design record. |
| CDC-00635 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-14 | Header | Record the signed sign-off for the epic design of RWB-ITG-W1 |
| CDC-00666 | RWB-ITG-E1039-ITG | DOR-RWB-ITG-E1039-ITG-14 | header | Confirm and record the signed epic design sign-off for this story's epic. |
| CDC-00683 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-14 | find it | Record the signed epic design sign-off for RWB-ITG-E1046-ITG (DOR-RWB-ITG-E1046-ITG-14). |
| CDC-00702 | RWB-ITG-E1047-ITG | DOR-RWB-ITG-E1047-ITG-14 | none | Confirm and record the signed epic design sign-off for EP01. |
| CDC-00711 | RWB-ITG-E1049-ITG | DOR-RWB-ITG-E1049-ITG-14 | header | Confirm and record the signed epic design sign-off for RWB-ITG-E1049-ITG |
| CDC-00726 | RWB-ITG-E1050-ITG | DOR-RWB-ITG-E1050-ITG-14 |  | No signed epic design in the source documents; sign-off must be confirmed in the epic design record. |

### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00644 | RWB-ITG-E1037-ITG | GAP-1568 | 13 | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request, answer, refusal and not-found schemas, version fields and masking marker vocabulary; state the group-to-role read path in TSD P4 T3.1. |
| CDC-00645 | RWB-ITG-E1037-ITG | GAP-2208 |  | The team filter conflict and the target-side facts are document fixes. No story text names them. |
| CDC-00646 | RWB-ITG-E1037-ITG | GAP-1564 |  | The owner of the load surface is a document ruling. The story states the load only as a P3 parameter path. |
| CDC-00651 | RWB-ITG-E1037-ITG | GAP-0778 |  | Add /api/recovery/access/v1/masking-policies with x-module P4 and x-capability Reference data R; no verb is given in the sources, so the base rule of R4 applies. |
| CDC-00656 | RWB-ITG-E1037-ITG | GAP-0779 |  | Set load and approve paths for P4 permission and masking tables on /api/recovery/access/v1; add /api/recovery/access/v1/masking-policies with Reference data R; publish AccessPolicyChanged; generic reference-load path stays with P3. |
| CDC-00733 | RWB-ITG-E1050-ITG | GAP-0761 | 13 | Section 13 states the story asserts the answer once the contract is extended; no fake is claimed. |

### RWB-P6-E1046-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00694 | RWB-ITG-E1046-ITG | GAP-1065 | 12 | Add one resolution rule for body_ref: opaque claim-check reference, resolved via P5 rwb-document contract or the service's own container. |
| CDC-00695 | RWB-ITG-E1046-ITG | GAP-1066 | 12 | State that LEG-0001 resolves to the USER_REF uuid at approval time via the existing staff directory, or widen approved_by to the staff identifier. |
| CDC-00696 | RWB-ITG-E1046-ITG | GAP-1067 | 12 | Baseline the four admin resources from TSD P6 T3.1 field names in camelCase; add current-version filter (code, language, on-date) to API-P6-003. |
| CDC-00697 | RWB-ITG-E1046-ITG | GAP-2343 | 12 | Name the identifier property of the version answer; fix the rwb-document login name in RWB-PLT-DB; document the template stamp as a soft reference with reconciliation check. |
| CDC-00699 | RWB-ITG-E1046-ITG | GAP-2453 | 12 | Keep the catalogue in P6; P7 holds a template_use record table in rwb_decision with the listed columns; publish the reads in RWB-P6-E1046-CON; treat H rows as wave-0 prerequisites. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00647 | RWB-ITG-E1037-ITG | GAP-0159 |  | The authorise schemas are defined by the P4 contract story, not by this ITG story. |
| CDC-00648 | RWB-ITG-E1037-ITG | GAP-0160 |  | The name conflict is resolved in the API catalogue, not in this story text. |
| CDC-00653 | RWB-ITG-E1037-ITG | GAP-1405 |  | Publish guard, scope guard, mask applier and annotation types; reach masking policy at GET /api/recovery/access/v1/masking-policies; audit record as case id, field id and clear or masked flag; map access-owner failures to 503 with no business data. |
| CDC-00674 | RWB-ITG-E1039-ITG | GAP-0966 | 8 | The authorise contract belongs to P4-E1037-CON; no story edit made here. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00604 | RWB-ITG-E1032-ITG | GAP-2445 | 11 | Hold DOCATT as a value of LOV-DECISION in force, read through the rwb-case reference-data contract; refuse an unknown code with MSG-P7-009. |
| CDC-00722 | RWB-ITG-E1049-ITG | GAP-1207 | find it | Add one LOV-NOTICE value for an operational notice to the case owner, named by the business owner, loaded as a reference row; then set DF-LEG-018 from it. |
| CDC-00735 | RWB-ITG-E1050-ITG | GAP-1007 |  | Add EXTRACTION_FAILED to LOV-INTAKE-REVIEW in the next approved list load; keep MODEL_UNAVAILABLE for the classification fallback; no code change. |

### OTHER:Work Package (plan) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00684 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-21 | header | No contract story key for this item is in the set, so the header stays unchanged. Naming and publishing the contract dependency belongs in the plan. |
| CDC-00686 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-23 | header | The contract version number is not in the source documents. It is fixed with the contract dependency outside this story; the header stays unchanged. |
| CDC-00700 | RWB-ITG-E1046-ITG | GAP-2344 | header | Add the rwb-case reference-data contract and platform contract stories to this slice's dependency rows; RWB-P5-E2026-CON to name the generation and regenerate request fields. |

### RWB-P6-E1046-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00691 | RWB-ITG-E1046-ITG | GAP-1064 | 13 | Add the rwb-source-data data-dictionary contract (GET /admin/data-dictionary/fields) to the C list, or confirm the published admin surface covers it; until then fake with one hop and 2 s timeout (DP-11). |
| CDC-00692 | RWB-ITG-E1046-ITG | GAP-1068 | 13 | Enforce declared area and right at gateway-bff for every admin route; service refuses absent right with 403 MSG-P4-002; add DP-08 with RWB-P4-E1037-CON only if a service-side authorise call is required. |
| CDC-00698 | RWB-ITG-E1046-ITG | GAP-2345 | 12 | Add a resolved current-version read (for example GET /admin/templates/current with code, language, onDate) and record it in RWB-P6-E1046-CON as additive within v1. |

### RWB-P4-E1039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00588 | RWB-ITG-E1031-ITG | GAP-2208 | 8 | BR2, BR7 and BR9 record the target-side facts as Not specified in the source documents; the contract change belongs to RWB-P4-E1039-CON. |
| CDC-00678 | RWB-ITG-E1039-ITG | GAP-2339 | not in chunk | Fix how the grant ID and incident reference reach a consuming service (signed claim or session call), their lifetime and reuse bound, and add the mechanism to the GET /me/session contract. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00596 | RWB-ITG-E1032-ITG | GAP-0742 | 13 | Add rwb_case.case_document_link with case_id, document_id, checklist_state, extracted_field_count, linked_at and source_event_id; unique key (case_id, document_id); no cross-service foreign key; data steward to supply field IDs. |
| CDC-00731 | RWB-ITG-E1050-ITG | GAP-0765 |  | Owned by RW-DATASTEW; not a story edit. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00597 | RWB-ITG-E1032-ITG | GAP-0991 | 13 | Add rwb.document.DocumentAttached.v1 on rwb.document.events.v1, or confirm DocumentStored, before the wave 1 release. |
| CDC-00602 | RWB-ITG-E1032-ITG | GAP-1202 | 12.4 | Record that rwb.comms.NoticeGenerated.v1 is a notification for rwb-decision only and the document hub is called by rwb-comms; align the P5 story and integration suite to this. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00599 | RWB-ITG-E1032-ITG | GAP-1197 | 12 | Publish the P5 generated-document request and answer with the intake item created, the letter copy document type and source, the notice parameters, the P1 recipient field IDs, the event payload fields and the notice screen identifier. |
| CDC-00600 | RWB-ITG-E1032-ITG | GAP-1199 | 12.4 | State whether the hub creates an intake item from a generated document and which request fields it needs, so the handoff is specified once. |

### RWB-P3-E1032-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00615 | RWB-ITG-E1032-ITG | GAP-0744 | 12.6 | Reconcile Schedule row: keep daily, overlap SKIP and catch-up window; add that the time of day is set with the operations team before go-live. |
| CDC-00617 | RWB-ITG-E1032-ITG | GAP-0747 | 11 | State that until the decision log owner agrees the decision code and final call, the link record names only the case, the document and the event id. |

### RWB-P7-E1032-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00622 | RWB-ITG-E1032-ITG | GAP-2449 | none | Use 'the rwb-decision login (DP-02)'; keep placeholders for the parameter names and MSG-P7-009 and MSG-GEN-006 texts; read parameters through the rwb-case parameters contract. |
| CDC-00623 | RWB-ITG-E1032-ITG | GAP-2450 | none | Run the ledger completeness check on the DP-06 ledger ingest window, with no Temporal Schedule and no cron entry of rwb-decision. |

### RWB-ITG-E1034-ITG (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00625 | RWB-ITG-E1034-ITG | DOR-RWB-ITG-E1034-ITG-21 | header | No contract story for this key exists in the story set, so Contract dependencies stays None. The contract versions are stated in the header. |
| CDC-00634 | RWB-ITG-E1034-ITG | GAP-1147 | 8 | Add DP07 to the pattern set and rows H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON so the four lists are read through the reference-data contract of rwb-case. |

### OTHER:Feature-flag API contract (platform, /v1) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00704 | RWB-ITG-E1047-ITG | DOR-RWB-ITG-E1047-ITG-23 | header | The header records that no contract version is specified. The contract must fix the version; only the /v1 path is named. |
| CDC-00709 | RWB-ITG-E1047-ITG | GAP-1412 | header | Publish the feature-flag schemas from DF-OPS-207 to DF-OPS-223 with placeholder schema names; POST takes Idempotency-Key and PATCH takes If-Match; errors as RFC 9457. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00712 | RWB-ITG-E1049-ITG | DOR-RWB-ITG-E1049-ITG-21 | header | No contract story key for this story exists in the set; Contract dependencies stays None until the plan names the published contracts. |
| CDC-00723 | RWB-ITG-E1049-ITG | GAP-1206 | find it | Add six H rows (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) and three C rows (RWB-P3-E1042-CON, RWB-P3-E1043-CON, and the rwb-case contract read dependency, ID Not specified in the source documents (GAP-1206)). |

### RWB-P5-E1049-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00714 | RWB-ITG-E1049-ITG | GAP-1205 | find it | Add rwb.document.OcrRescanRequested.v1 on rwb.document.events.v1, produced by P5 rwb-document in the same transaction as the intake item state change, with elements intakeItemId, documentId, caseId (absent when no case), rescanPages, quality, languages, occurredAt |
| CDC-00719 | RWB-ITG-E1049-ITG | GAP-0998 | 13 | The two-event catalogue for rwb-document sits in Architecture v5 and the P5 contract; the third event name must be added there. The story side needs no change. |

### OTHER:Wave 1 backlog (RWB-ITG-W1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00576 | RWB-ITG-E1030-ITG | DOR-RWB-ITG-E1030-ITG-21 | header | Create contract story RWB-ITG-E1030-CON and add it as the contract dependency of RWB-ITG-E1030-ITG. |

### OTHER:Contract fake library for rwb-case, rwb-decision, rwb-reporting and rwb-source-data (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00577 | RWB-ITG-E1030-ITG | DOR-RWB-ITG-E1030-ITG-22 | 12.8 | Name the contract fake for each of the four services and record its published library version. |

### RWB-ITG-E1059-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00580 | RWB-ITG-E1030-ITG | GAP-0610 | none | Keep legacy AC5 and TC-E1-059-05 with RWB-ITG-E1059-ITG as the split places them; name the rwb-agent login and gateway-bff route with their owners. |

### RWB-P3-E1030-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00581 | RWB-ITG-E1030-ITG | GAP-2206 | none | State in the P3 contract baseline review whether a business date's run is readable; if yes add the operation and ownership row and publish the run record schema in version 1. |

### OTHER:Recovery Workbench Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00582 | RWB-ITG-E1030-ITG | GAP-3166 | none | Keep RWB-TE-007 retired for traceability only; read JOB-06 and each map Job as a Temporal Schedule in the owning service. |

### RWB-ITG-E1031-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00584 | RWB-ITG-E1031-ITG | DOR-RWB-ITG-E1031-ITG-21 | n/a | Create contract story RWB-ITG-E1031-CON and publish its contract, then add it to Contract dependencies in the header. |

### RWB-P3-E1031-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00589 | RWB-ITG-E1031-ITG | GAP-2209 | 13 | Section 13 records the row, envelope and page-token names and the 401 text as Not specified in the source documents; the contract change belongs to RWB-P3-E1031-CON. |

### OTHER:Story register (integration contract to be published) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00591 | RWB-ITG-E1032-ITG | DOR-RWB-ITG-E1032-ITG-21 | header | No contract story exists in the set; Contract dependencies stays None until the contract is published and registered. |

### OTHER:Contract fake library (rwb-case, rwb-comms, rwb-decision, rwb-document, rwb-partner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00592 | RWB-ITG-E1032-ITG | DOR-RWB-ITG-E1032-ITG-22 | 12.8 | Publish a contract fake for each of the five services and record its library version. |

### OTHER:Integration contract (to be published) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00593 | RWB-ITG-E1032-ITG | DOR-RWB-ITG-E1032-ITG-23 | header | Version row added with placeholder; the true version must come from the published contract. |

### RWB-S9-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00594 | RWB-ITG-E1032-ITG | GAP-1843 |  | Keep RWB-S9-E1032-APP in wave 1 as a contract-only slice: partner identity and partner document path published; panel, allocation and fees in wave 4. |

### OTHER:environment files (SCB IT infrastructure) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00598 | RWB-ITG-E1032-ITG | GAP-0993 | 13 | Provision the capacity shape now; record the per-environment replica, request and limit, KEDA ceiling, storage, container and scan rate values after SIT measurement. |

### OTHER:Recovery Workbench test case register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00601 | RWB-ITG-E1032-ITG | GAP-1201 | 16 | Record that the attach proof of TC-E1-032-01 to TC-E1-032-15 is owned by RWB-P5-E1032-APP and the P6 copy proves the service side; note TC-E1-032-16 as the notice-read refusal. |

### OTHER:TSD P7 v2 decision_log_entry field mapping and rwb_decision migration V1032_1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00603 | RWB-ITG-E1032-ITG | GAP-2444 | 11 | Map the document reference, intake item and match method into actions, classifier version into model_version, confidence and type candidates into recommendation, refusal message id into outcome, final_call ATTACHED; add the columns by migration V1032_1. |

### RWB-P5-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00605 | RWB-ITG-E1032-ITG | GAP-2447 | 12.3 | Define DecisionRecorded for attach keyed by caseId with decisionCode, caseId, documentId, intakeItemId, matchMethod, classifierVersion, confidence, approverUserId, finalCall, messageId and inputsRef; exclude OCR text, file and account number; refuse a fact without a document reference. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00606 | RWB-ITG-E1032-ITG | GAP-3137 | Header | Confirm the secondary partner slice in the Change Register and publish the S9 frame for RWB-S9-E1032-APP in the Service Contract Catalog. |

### OTHER:S9 contract baseline (rwb-partner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00607 | RWB-ITG-E1032-ITG | GAP-3138 | 2 | Publish the partner file channel: the submission row, the PartnerDocumentSubmitted fact, the attach event consumed and the item read used to copy the match state. |

### RWB-S9-E1032-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00608 | RWB-ITG-E1032-ITG | GAP-3141 |  | Publish the two partner submission operations, the intake creation path, the PartnerDocumentSubmitted.v1 payload, and the 404 and 409 bodies in RFC 9457 shape. |

### parameter-catalog.csv; 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00609 | RWB-ITG-E1032-ITG | GAP-3142 |  | Publish the intake bound parameter row, the acceptance decision code with version, and LOV-DOC-TYPE; keep values out of code. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00610 | RWB-ITG-E1032-ITG | GAP-3143 |  | Add partner_intake with its field IDs before the wave 1 entry check. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00611 | RWB-ITG-E1032-ITG | GAP-3144 |  | Record the primary/secondary AC split so AC1 to AC15 are counted once against RWB-P5-E1032-APP. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00612 | RWB-ITG-E1032-ITG | GAP-1198 |  | Add seven platform contracts and two P3 contracts, or record in the platform release train that wave 1 services compile against them. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00613 | RWB-ITG-E1032-ITG | GAP-0746 |  | Hold the review task code, element type and task status values as reference data and load them before the review queue story starts. |

### OTHER:rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00614 | RWB-ITG-E1032-ITG | GAP-0743 |  | Publish the account lookup path GET /api/recovery/source-data/v1/accounts/{id} with the ACE account number as identifier, and agree the query form before integration. |

### parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00616 | RWB-ITG-E1032-ITG | GAP-0745 | Not in chunk | The rwb-case feature switch key is owned by the parameter catalog; this story uses no switch key. |

### OTHER:Platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00618 | RWB-ITG-E1032-ITG | GAP-0748 | Not in chunk | Per-service login names belong to the platform DB story; this suite names no login. |

### RWB-P5-E1032-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00619 | RWB-ITG-E1032-ITG | GAP-0994 | 12.6 | Keep the section 4 text: business-hours window, overlap SKIP, catch-up of one run, thresholds as environment values, lag-alert placeholder. Reconcile its intake Schedule with DP-10. |

### OTHER:FSD P6 Communications v3 / TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00620 | RWB-ITG-E1032-ITG | GAP-1200 | Not in chunk | The notice parameter must be declared by the P6 documents; no value is invented here. |

### OTHER:FSD P6 Communications v3 and TSD P6 Communications v2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00621 | RWB-ITG-E1032-ITG | GAP-1203 | Not in chunk | Approval of the base documents belongs to their owners; no story edit. |

### Epic design record; OTHER:EP01 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00624 | RWB-ITG-E1034-ITG | DOR-RWB-ITG-E1034-ITG-14 | find it | Record the signed epic design sign-off for EP01 and cite it in this story. |

### OTHER:07 Screens and experience/Recovery Workbench Screen Specifications v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00628 | RWB-ITG-E1034-ITG | DOR-RWB-ITG-E1034-ITG-10 | 15 | SCR-33 there lists only Draft, approved, withdrawn. Story has the four rows: common Loading and Error apply, access check and MSG-P4-002 stated; Empty and the No access layout are not specified. |

### OTHER:TSD P4 RBAC matrix T6.1 (rwb-access document set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00630 | RWB-ITG-E1034-ITG | GAP-0942 | 8 | Add a Documents column: CRU for RW-RESTRUCT and RW-CASEOWN, R for RW-TEAMMGR, CRUA for RW-LEGAL; confirm with matrix owner and publish in PM-2026.12 pack via RWB-P4-AD002-APP |

### 22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00631 | RWB-ITG-E1034-ITG | GAP-1146 | 8, 13 | Record template and merge_field as P6 rwb-comms; DL28 superseded by Architecture v5 slide 41 under precedence; confirm Documents right of T-A.1 and retire legacy Litigation rows |

### OTHER:TSD P6 decision code and rule catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00632 | RWB-ITG-E1034-ITG | GAP-1148 | 13 | Reason rule and template shape stated in section 13; decision code and rule id marked Not specified |

### OTHER:rwb-case contract and service values file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00633 | RWB-ITG-E1034-ITG | GAP-1149 | 13 | Name the operation, task code, target queue and fields of the litigation officer task; record code and queue as configuration |

### RWB-ITG-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00636 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-21 | Header | Create contract story RWB-ITG-E1037-CON and add it as the contract dependency of RWB-ITG-E1037-ITG |

### OTHER:Contract fake library (rwb-access, rwb-source-data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00637 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-22 | 12.8 | Publish contract fakes for rwb-access and rwb-source-data and record the library version |

### OTHER:P4 rwb-access and P1 rwb-source-data API yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00638 | RWB-ITG-E1037-ITG | DOR-RWB-ITG-E1037-ITG-23 | Header | Record the exact contract version the story builds against |

### OTHER:INT-34 ACE Common contract register (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00639 | RWB-ITG-E1037-ITG | GAP-0013 | Header | Version each of the six ACE Common contracts and run contract tests on both sides from wave 1 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00640 | RWB-ITG-E1037-ITG | CG-ALL-318 | Header | Record recovery_svc as a database login role object (service identity) in the owning document |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00650 | RWB-ITG-E1037-ITG | GAP-0262 |  | DF-DOC-089 document_text.text_content row: rule is never in an event, workflow input or log; page id only in a log; data steward sets the classification |

### RWB-PLT-E1037-APP; RWB-P4-E1037-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00652 | RWB-ITG-E1037-ITG | GAP-1404 |  | Publish library at platform coordinate major 1; cache TTL in a parameter via parameters client; authorise and masking-policy payloads from slide 14; policy decides, data owner masks |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00654 | RWB-ITG-E1037-ITG | GAP-2036 |  | State that POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies are P4 operations whose shapes stay open until RWB-P4-E1037-CON freezes. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00655 | RWB-ITG-E1037-ITG | GAP-1569 |  | Add AccessPolicyChanged and DoaLimitChanged on rwb.access.events.v1 with CloudEvents type, key, payload and versioning; state refresh window and missed-event fallback; change TSD P4 T5.3 from None. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00657 | RWB-ITG-E1037-ITG | GAP-2035 | 11 | The count of one schema and one login against 19 is a source conflict. The story already treats recovery_svc as the DP-02 login. |

### OTHER:Technical Solution Design P4 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00658 | RWB-ITG-E1037-ITG | GAP-1574 |  | Add valid-from and valid-to effective-date columns to the matrix version fields, or state that the date lives on the load. Publish the complete role conflict list with its version label and the role and permission row counts. |

### OTHER:Recovery Workbench Security and Access Design v5 (access log row) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00660 | RWB-ITG-E1037-ITG | GAP-2076 |  | Access row records the version the owning service applied at the event; rwb-decision registry stays the source of version and effective date |

### OTHER:P1 and P4 CON stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00663 | RWB-ITG-E1037-ITG | GAP-0248 |  | Keep the masking function in the recovery view schema and the policy rows in rwb_access (P4). State that rwb-source-data applies the mask in the view and in its responses. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx; OTHER:Key row 16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00664 | RWB-ITG-E1037-ITG | GAP-0264 |  | Name the ACE Common PII logging path to the SOC (INT-34); state Recovery business topics are separate and carry no personal data |

### OTHER:Integration contract story for this suite (not yet in the story set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00667 | RWB-ITG-E1039-ITG | DOR-RWB-ITG-E1039-ITG-21 | section header | No published contract story is named in the sources; the header reads Not specified. The contract must be created and published outside this file. |

### RWB-P4-E1039-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00671 | RWB-ITG-E1039-ITG | DOR-RWB-ITG-E1039-ITG-4 | 16 | Add a criterion and test for the break-glass review rules BR7 and BR9, or name the bank IAM check that proves them; its Covers column lists neither. |

### OTHER:rwb-integration composed case-list contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00672 | RWB-ITG-E1039-ITG | GAP-0661 | 8 | The contract baseline belongs to the integration contract; not in this story. |

### OTHER:RWB-P3 and RWB-P4 contract stories; OTHER:rwb-integration contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00673 | RWB-ITG-E1039-ITG | GAP-0660 | 8 | Ownership, paths and contract fixes sit in the P3, P4 and integration contracts. |

### OTHER:Message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00675 | RWB-ITG-E1039-ITG | GAP-0781 | not in chunk | Add the expired-session 401 business message id: Not specified in the source documents (GAP-0781). Grant paths and state field to be confirmed with the security administrator. |

### RWB-P4-E1039-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00676 | RWB-ITG-E1039-ITG | GAP-0782 | 12.7 | Confirm break_glass_grant, columns and one-active-grant constraint with the security administrator; retention and partition stay parameter rows, value set at DL26. |

### RWB-P4-E1039-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00677 | RWB-ITG-E1039-ITG | GAP-0783 | 13 | Record alert routes and thresholds as parameter-backed deployment values; Kafka ACL per platform producer rule; platform retry topics; secrets in secret store and values files. |

### OTHER:TSD P5 v2 (P5 contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00680 | RWB-ITG-E1039-ITG | GAP-2341 | not in chunk | State which P5 reads write an access entry and under which decision code, and the owner of each entry; until then only the content read is owned here. |

### OTHER:Contract fake library (not named in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00685 | RWB-ITG-E1046-ITG | DOR-RWB-ITG-E1046-ITG-22 | 12.8 | Publish contract fakes for rwb-case, rwb-comms, rwb-decision, rwb-document and rwb-source-data, and record the library version as published. |

### OTHER:TSD P5 (document table) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00690 | RWB-ITG-E1046-ITG | GAP-1023 | 13 | Add template_code varchar(30) and template_version integer beside template_id and treatment_id; build partial unique index on (treatment_id, template_id) where state is DRAFT and is_active. Story path set to Ownership Map. |

### OTHER:rwb-comms API file and wave 1 harness (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00693 | RWB-ITG-E1046-ITG | GAP-1063 | 13 | Record that the legacy POST /api/recovery/v1/admin/reference-loads maps to POST /admin/templates plus approve and withdraw on /api/recovery/comms/v1, with the SHA-256 file hash kept as the idempotency rule. |

### OTHER:split plan (Work Package) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00701 | RWB-ITG-E1046-ITG | GAP-2346 | 16 | Record one owning story per legacy criterion and mark this slice as test-case-bearing but criterion-free for the traceability reports. |

### RWB-ITG-E1047-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00703 | RWB-ITG-E1047-ITG | DOR-RWB-ITG-E1047-ITG-21 | header | Publish contract story RWB-ITG-E1047-CON and add it as a CON dependency for this story, or confirm none applies. |

### OTHER:Contract fake library for rwb-case, rwb-comms, rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00713 | RWB-ITG-E1049-ITG | DOR-RWB-ITG-E1049-ITG-22 | 12.8 | This integration story calls the real SIT services and fakes no service contract; fake publication belongs outside the story. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00718 | RWB-ITG-E1049-ITG | GAP-1590 | 13 | State intake as event-started DocumentIntakeWorkflow with KEDA workers on queue rwb-document; keep the 15-minute cadence as a schedule that raises the intake; state JOB-17 as a Temporal Schedule on the 1st Sunday of the month. |

### RWB-P5-E1049-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00720 | RWB-ITG-E1049-ITG | GAP-0999 | 13 | Field names, path and payload are published in the P5 contract baseline; sign-off and the not-found message belong there. |

### OTHER:TSD P6 v2 and RWB-E1-049 section 13 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00721 | RWB-ITG-E1049-ITG | GAP-1204 | find it | Publish the rescan notice template row (code, version, language, body, channel); extend LOV-NOTICE with the business owner's value; baseline Notice answer of API-P6-002 and ACE request and result; set retry values and state list. |

### RWB-P1-E1065-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00724 | RWB-ITG-E1049-ITG | GAP-1051 | find it | Publish the per-case document count and the version depth as seed parameters for this story and RWB-P5-E1025-APP. |

### OTHER:RWB-E1-049 section 14 (MSG-P5-018 message baseline) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00725 | RWB-ITG-E1049-ITG | GAP-1208 | find it | The reference form of the document token must be named in the MSG-P5-018 message baseline. No criterion in this story changes. |

### OTHER:contract story for this suite (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00727 | RWB-ITG-E1050-ITG | DOR-RWB-ITG-E1050-ITG-21 | header | No published contract story key is confirmed; the Contract dependencies row reads Not specified in the source documents. |

### OTHER:contract fake library for rwb-agent, rwb-case, rwb-document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00728 | RWB-ITG-E1050-ITG | DOR-RWB-ITG-E1050-ITG-22 | 12.8 | Publish a contract fake for each of the three services and record the library version as published. |

### RWB-P10-TE013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00730 | RWB-ITG-E1050-ITG | GAP-1005 |  | Contract baseline lives outside this story. |

### RWB-P5-E2026-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00732 | RWB-ITG-E1050-ITG | GAP-1003 |  | Change belongs to the event and API baseline. |

### OTHER:Service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00736 | RWB-ITG-E1050-ITG | GAP-0762 | 8 | Story names the login as the rwb-case login (DP-02) until the agreed name is recorded in the service catalogue. |

### OTHER:rwb-case parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00737 | RWB-ITG-E1050-ITG | GAP-0766 | 8 | Story marks switch key and re-drive time as Not specified in the source documents; set by RW-COE. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20619 | RWB-ITG-E1037-ITG | R-09184 |  | Versioning and dual-side contract tests for the six ACE Common contracts belong to INT-34 (ACE Common contract register), not this catalogue. Catalogue already tracks ACE Common as class X against the owning party. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20634 | RWB-ITG-E1030-ITG | R-28558 |  | RWB-TE-007 is retired (Quartz replaced by Temporal Schedules); RWB-E1-031 reads JOB-06 as a Temporal Schedule (GAP-3166). |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0013 | ACE Common contracts are not versioned or scheduled | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0065 | Wave conflict S9 / EP01 | Tech lead | Resolved (directive) |
| GAP-0159 | The four authorise operations have no request, response or error schema in any source | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0160 | The sign-in permission read has two names, /me/permissions and /me/session | TechX | Resolved (directive) |
| GAP-0161 | No cache lifetime and no rule for a failed authorise call | TechX | Resolved (directive) |
| GAP-0164 | Partner roles sit in the roles table while the partner user is owned by S9 | Partner and agency manager | Resolved (directive) |
| GAP-0165 | The access log is named by Architecture v5 but is not itemised in the Ownership Map | ACE team | Resolved (directive) |
| GAP-0166 | How the six non-human actors authenticate is not stated | Security administrator | Resolved (directive) |
| GAP-0168 | The Key tab scope values do not include REGION, which the access story uses | TechX | Resolved (directive) |
| GAP-0248 | The masking function and the masking policy have no stated home after the schema split | Security architect | Resolved (directive) |
| GAP-0262 | OCR text is classified Not personal while the same content at field level is Restricted | Data steward | Resolved (directive) |
| GAP-0264 | The PII log path is named PII Kafka with no owner and no separation from the business topics | Security team | Resolved (directive) |
| GAP-0354 | Rebalancing trigger, measure delivery and rerun facade change in the target | Tech lead | Resolved (directive) |
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0356 | Intake trigger, attach operation and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0357 | Moved template operations, screen route and freshness stamp need a target reading | Tech lead | Resolved (directive) |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0359 | Break-glass grant operation, central ledger fault point and SIT evidence are not named for the 19-service target | Tech lead | Resolved (directive) |
| GAP-0360 | Reference-load owner, field-ID check and template body storage move in the target | Solution architect | Resolved (directive) |
| GAP-0361 | Feature-flag owner, flag operations and the weekly report trigger move in the target | Platform lead | Resolved (directive) |
| GAP-0362 | OCR trigger, worker count and parameter home change in the target | Tech lead | Resolved (directive) |
| GAP-0363 | Classifier route, parameter home and agent run evidence are not named for the target | Tech lead | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0610 | Open points of the intake shadow run on the service: login, route, the legacy criterion AC5 of the integration slice and the P5 contract row | Tech lead and solution architect | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0742 | No case-side document link table or field IDs in the sources | RW-DATASTEW | Resolved (directive) |
| GAP-0743 | No named rwb-source-data operation for the ACE account number | RW-COE | Resolved (directive) |
| GAP-0744 | Cadence and time of the daily reconcile Schedule not specified | RW-COE | Resolved (directive) |
| GAP-0745 | The rwb-case feature switch key is not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0746 | The case review task code and its status values are not specified | RW-COE | Resolved (directive) |
| GAP-0747 | Decision code and final call for the case document link are not specified | RW-COE | Resolved (directive) |
| GAP-0748 | Per-service login names for rwb-case and rwb-document are not specified | RW-SECADM | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0761 | The classification answer the case needs is not carried by the published document contract or by EV-16 and EV-17 | Solution architect | Resolved (directive) |
| GAP-0762 | The rwb-case login name is not in the sources | Tech lead | Resolved (directive) |
| GAP-0763 | The texts of MSG-GEN-004 and MSG-GEN-006 are not in the source extracts | Solution architect | Resolved (directive) |
| GAP-0764 | No source names a classifier version label or its format | Solution architect | Resolved (directive) |
| GAP-0765 | The case document link is not an Owner row and has no field IDs | RW-DATASTEW | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0766 | The rwb-case switch key and the re-drive time of day are not specified | RW-COE | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0767 | The decision record is written here although DP-03 and its library story are not applied | Solution architect | Resolved (directive) |
| GAP-0778 | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0780 | Local decision-record table, legacy break-glass path and the composition of the entry actions are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0781 | The grant end and read paths, the 401 business message id and the full grant answer are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0782 | No source names the grant table, its two-person constraint, the retention period or the partition granularity of the access log | ACE database engineer | Resolved (directive) |
| GAP-0783 | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | DevOps engineer | Resolved (directive) |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0991 | The attach operation, its right and the attach event name differ between the legacy story, the TSD and the Arch v5 event catalogue | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0992 | The intake-match contract baseline fixes shapes and paths the sources do not name at field level, and the plan's C list omits the two rwb-case reads | Tech lead | Resolved (directive) |
| GAP-0993 | The compute, storage, hold-container and scanning capacity values of the intake-match path are not specified | SCB IT infrastructure | Resolved (directive) |
| GAP-0994 | The Schedule window, the catch-up policy, the alert thresholds and the lag-alert identifier of the intake path are not specified | DevOps team | Resolved (directive) |
| GAP-0997 | OCR engine product, endpoint, engine version, capacity, intake request property names and the business-hours window are not named in the sources | Tech lead | Resolved (directive) |
| GAP-0998 | The pipeline publishes a third event name on rwb.document.events.v1 while the architecture catalogue lists two events for rwb-document | Solution architect | Resolved (directive) |
| GAP-0999 | Field-level names of IntakeItem, OcrTextPage and IntakeStatus, the OCR status path and the not-found message ID are not specified | Tech lead | Resolved (directive) |
| GAP-1000 | OCR engine capacity, admission queue depth, per-page text size and container quota are not named in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1001 | The business-hours window, the deployment slot and the alert thresholds of the document intake pipeline are not specified | DevOps team | Resolved (directive) |
| GAP-1002 | The classify run is drawn as an rwb-agent child while the legacy story calls the P10 model gateway in process, and no source names the model provider, endpoint or model version | Solution architect with the TechX tech lead of rwb-document and the rwb-agent owner | Resolved (directive) |
| GAP-1003 | No source names a classification operation, path or field-level name, a 404 message identifier is absent, and a classification event would be a third event for rwb-document | Solution architect with the TechX contract owner of rwb-document | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1004 | The classifier artefact production and versioning, the evaluation report container, the alert thresholds and the deployment topology values are named by no source | DevOps engineer with the platform administrator and the data steward | Resolved (directive) |
| GAP-1005 | The extractor provider, model name and model version behind extraction_method MODEL are not named | Solution architect with the rwb-agent owner | Resolved (directive) |
| GAP-1007 | The review reason EXTRACTION_FAILED is not a value of LOV-INTAKE-REVIEW | Data steward with the P5 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1023 | The generation operation name conflicts with the architecture, the template catalog moves to P6, two document columns are absent from the TSD, and six values this engine needs are not specified | Solution architect | Resolved (directive) |
| GAP-1051 | The number of synthetic documents per case and the version depth of a seeded document are not specified | Solution architect, P5 | Resolved (directive) |
| GAP-1063 | The legacy template and catalog load path is replaced by the TSD admin template operations | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1064 | The data-dictionary read has no contract dependency in the plan | Solution architect | Resolved (directive) |
| GAP-1065 | No source says where the template body object lives | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1066 | The approver identity type of a template version is not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1067 | The request and answer field names of the five admin operations are not in T-A.2 | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1137 | Legacy /templates paths disagree with the TSD /admin/templates paths | Tech lead | Resolved (directive) |
| GAP-1138 | Legacy 'set current' has no operation in the target contract | Tech lead | Resolved (directive) |
| GAP-1139 | Allowed body file types and the size limit are marked assumed and fixed by no source | Tech lead | Resolved (directive) |
| GAP-1140 | Template body container: own Blob store or a P5 rwb-document object | Solution architect | Resolved (directive) |
| GAP-1146 | Template ownership is a conflict between DL28 and the catalogue, and the split of the surface between RWB-E1-034 and RWB-AD-017 is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1147 | The reference lists the template screen needs have no contract row and no DP-07 in this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1148 | The withdrawal reason, the field that holds it and the decision code of an approval or a withdrawal are not stated | Business analyst, P6 | Resolved (directive) |
| GAP-1149 | The task target of a withdrawn template and the resumption of held generation are not specified | Business analyst, P6 | Resolved (directive) |
| GAP-1197 | The request and answer shape of the letter-copy handoff, the document type and source the hub assigns, the notice parameters, the P1 recipient field IDs, the payload field names of the event and the notice screen identifier are all unspecified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1199 | No source describes the letter copy becoming an intake item at the document hub, and FSD P6 keeps a generated document as a stored document on the case | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1200 | The P6 module declares no notice parameter, so DP-06 has no named value to read | Business analyst | Resolved (directive) |
| GAP-1201 | The legacy access case and the legacy attach cases have no subject in rwb-comms, so the carried test cases prove the notice read instead | Test lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1202 | The event catalogue names rwb-decision as the only consumer of NoticeGenerated, while the document hub is expected to turn the copy into an intake item | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1203 | The base documents of the story are in review, not approved | Business analyst | Resolved (directive) |
| GAP-1204 | The values the rescan notice needs are not named in any source | Business analyst, P6 | Resolved (directive) |
| GAP-1205 | The document rescan event that triggers the notice is in no event catalogue and has no name or payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1207 | The notice list of values has no value for an operational rescan notice | Business analyst, P6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1208 | The document token of the rescan message has no named reference form | Business analyst, P6 | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1404 | Library artefact coordinates, the policy cache time to live, the authorise payload and the split of the masking read between P4's policy and P1's read are not specified | Platform library architect with the P4 rwb-access owner and the P1 rwb-source-data owner | Resolved (directive) |
| GAP-1405 | The contract shapes of the guard and masker, the /masking-policies path, the audit record shape and the failure mapping are not specified | Platform library contract owner with the P4 rwb-access contract owner | Resolved (directive) |
| GAP-1411 | Platform feature-flag store, its schema name and the deployment of the admin component are not specified | Platform team (PLT) architect with the ACE DBA | Resolved (directive) |
| GAP-1412 | Feature-flag contract schemas, the schema names of the two PLT tables and the idempotency rule of the POST are not specified | Platform team (PLT) contract owner with the ACE DBA | Resolved (directive) |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1569 | AccessPolicyChanged and DoaLimitChanged are published by rwb-access in Architecture v5 but have no row, payload, key or refresh window in the event design | Solution architect with the platform event owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1571 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | SCB IT security with the security administrator | Resolved (directive) |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1590 | The FSD makes document intake a 15-minute scheduled job while Architecture v5 makes it an event-started workflow with KEDA workers | Platform administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1652 | Queue depth and ageing are computed in P3 and published in P9 | Solution architect with P3 | Resolved (directive) |
| GAP-1667 | The feature-flag store has an owner and a schema in the Ownership Map but no service row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1843 | Two S9 stories sit in wave 1 while the service is created in wave 4 | Solution architect with the programme manager | Resolved (directive) |
| GAP-1879 | The template catalogue and merge fields sit with the document module in the legacy and with rwb-comms in the target | Solution architect | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2036 | The authorise contract has no request or response shape in any source | TechX with P4 rwb-access | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2041 | Partner users moved to S9 rwb-partner, while the approving role owner stays in P4 | S9 rwb-partner with P4 rwb-access | Resolved (directive) |
| GAP-2063 | The edge components have no owner row in the Ownership Map, and section 5 needs one | Platform (RWB-PLT-EDGE) with S9 rwb-partner | Resolved (directive) |
| GAP-2069 | The access log has an API and an owner but no table in the Ownership Map | Service owner P4 rwb-access | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2133 | rwb-valuation owns no table, so the plan does not say where a route decision is kept | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2205 | The measure feed, the alert delivery path and the run record have no target artifact once the data lake and the job monitor are removed | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2206 | The published run record and the rerun operation of the legacy contract have no target shape | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2207 | No source gives the operating values for the rebalance Schedule or the deployment | DevOps lead | Resolved (directive) |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2209 | The row, envelope and page-token names of the case list and the 401 message text have no source | Solution architect | Resolved (directive) |
| GAP-2339 | How the active break-glass grant and its incident reach rwb-document on a document content read is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2340 | The capability-area code, the result code and the field list of a document content read in an access entry are not specified | Data steward | Resolved (directive) |
| GAP-2341 | Which reads of the document hub other than the content read write an access entry in the target is not fixed | Solution architect | Resolved (directive) |
| GAP-2342 | The incident queue name and the session-answer reuse bound of the content read are not specified | DevOps team | Resolved (directive) |
| GAP-2343 | The catalog version answer read by rwb-document, its field names and the rwb-document login name are not specified, and the legacy document-to-template key becomes a soft cross-service reference | Solution architect, with the P5 TechX squad and the P6 rwb-comms squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2344 | The dependency rows of this slice name one contract only, and the request field names, the reason field, the index name and the migration step name are not specified | Solution architect, with the P5 TechX squad | Resolved (directive) |
| GAP-2345 | The rwb-comms catalog baseline declares no operation that answers the current Approved version for a template code, language and date | Tech lead of rwb-comms, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2346 | This slice owns no legacy acceptance criterion while the Work Package lists all nine legacy test cases for it | Solution architect, with the traceability owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2444 | DOCATT attach entry has no defined field set for the document reference, the intake item, the match method, the confidence, the final call and the message id | Solution architect, P7 | Resolved (directive) |
| GAP-2445 | The decision code list in force does not enumerate DOCATT in any source readable here | Reference data administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2446 | Whether an item held for a person leaves a decision record is not stated | Business analyst, P7 | Resolved (directive) |
| GAP-2447 | The DecisionRecorded payload of an attach has no defined field set | Solution architect, integration | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2449 | Login name, parameter names and message texts are not written in any source readable here | Tech lead, P7 | Resolved (directive) |
| GAP-2450 | The trigger of the ledger completeness check is not stated | Solution architect, P7 | Resolved (directive) |
| GAP-2452 | No source gives the ledger's access shape: the element names inside the actions payload beyond the legacy list, the grant, incident and review-due elements of the decision-log read, the use of the access code AC-VERS, and the catalogue entry format of MSG-P7-009 | Business analyst P7 | Resolved (directive) |
| GAP-2453 | The P7 slice of RWB-E1-046, the row that holds the template version, the catalog read paths, the table and columns and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3137 | The partner slice of RWB-E1-032 and its target service frame are not stated in any source | Solution architect | Resolved (directive) |
| GAP-3138 | The partner-origin channel of an intake item and its attach state are a boundary no source states | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3139 | Wave conflict: EP01 puts this story in wave 1 while rwb-partner is wave 4 in Arch v5 | Tech lead | Resolved (directive) |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3141 | The two partner submission operations, the intake creation path and the PartnerDocumentSubmitted event are not published | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3142 | The intake bound, the decision code and version, and the two lists in force are not named | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3143 | No data model carries a partner-side submission row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3144 | No source states how the legacy criteria split between the document-hub and partner slices | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3145 | The partner portal screen that submits a file is not fixed | Business analyst | Resolved (directive) |
| GAP-3161 | Feature flags are a P2 module table in the story and a platform library object in the Ownership Map | Platform lead | Resolved (directive) |
| GAP-3166 | The Quartz note remains in the build notes although a Temporal Schedule replaces it | Platform lead | Resolved (directive) |
| GAP-3174 | Service S9 takes Epic 1 stories in wave 1 although its Arch v5 wave is 4 | Delivery lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
