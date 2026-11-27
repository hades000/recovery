# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 5 of 11 (RWB-P4-E1037-CON to RWB-P4-E1039-OPS)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 6 |
| Resolved in the stories | 131 |
| Cross-document (pending in another document) | 185 |
| Not applied (value not in the sources) | 19 |
| Open business decisions | 28 |
| Register gaps linked | 118 |
| Unconfirmed assumptions | 0 |
| Lint findings | 2 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E1037-CON | 40 | 67 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1037 CON Role to permission matrix as data and PDPA field masking by role - contract v2.md |
| RWB-P4-E1038-APP | 21 | 19 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1038 APP Delegation of authority table as reference data v2.md |
| RWB-P4-E1039-APP | 13 | 22 | 11 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1039 APP Access log into the decision log and break-glass admin v2.md |
| RWB-P4-E1039-CON | 30 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1039 CON Access log into the decision log and break-glass admin - contract v2.md |
| RWB-P4-E1039-DB | 16 | 33 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1039 DB Access log into the decision log and break-glass admin - ACE DB v2.md |
| RWB-P4-E1039-OPS | 11 | 28 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1039 OPS Access log into the decision log and break-glass admin - deployment v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E1039-APP | R-10667 | CG-ALL-5031 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E1039-DB | R-10678 | CG-ALL-5053 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-E1039-OPS | R-10680 | CG-ALL-5060 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22104 | GAP-2037 | Register gap | Architecture with Compliance | Two sources disagree on who applies the mask: rwb-source-data or each service | Both controls are kept and written as defence in depth: rwb-source-data masks in the view and in its contract, and each service re-applies the masking_rule rows of rwb-access before the response leaves. The story RWB-P4-E1037-APP owns the profile; the P1 story owns the view mask. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22105 | GAP-2136 | Register gap | Compliance | The plan does not say which service applies the mask once the masking rules are rwb-access data | rwb-access holds the approved masking version; rwb-source-data applies the mask at the 30 views; display masking at the API is applied by the service that owns the field, under the same version. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-22113 | GAP-1570 | Register gap | Compliance with the solution architect | The access log has no stated retention, no stated searchable period, no stated storage object and no stated cross-service read right, although it is the evidence for every access question | Answer DL26 for the access log in one row: the retention period, whether it equals the decision log period, which object answers the query (the local record, the central ledger, or a projection of both), which fields are searchable and for how far back, and which roles in other services may read it. Until then this PRD keeps the classification at PII and marks the retention as not set. |
| RWB-ITG-E1062-ITG, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-P4-E1039-APP, RWB-P4-E1062-APP, RWB-P5-E1062-APP, RWB-S8-E1062-APP | R-22216 | GAP-2330 | Register gap | Internal audit role and the solution architect, P4 | The access entry of an agent read has no source row, element list or decision-code vocabulary of its own | Fix the entry members of a non-human read in the access-entry writer of RWB-P4-E1039-APP and publish them once for every service identity, so an audit query by agent code and policy version answers from the same chain as the screen entries. |
| RWB-ITG-E2004-ITG, RWB-P3-E2004-APP, RWB-P3-E2004-CON, RWB-P3-E2004-OPS, RWB-P4-E1038-APP, RWB-P4-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP | R-22353 | GAP-0919 | Register gap | Business lead | Which delegation limit version is in force on the approval date of a treatment is a data state, not a document value | Decide the version in force per environment at the DoA load (RWB-P4-E1038-APP) and keep it out of code; the lookup always answers the version whose window covers the date asked, and the answer names it |
| RWB-ITG-E2005-ITG, RWB-P4-E1037-CON, RWB-P7-E2005-APP, RWB-P7-E2005-CON | R-22366 | GAP-1243 | Register gap | Compliance and PDPA officer, with the P4 access owner | Whether the audit role may see unmasked person keys in an entry or an export | The audit read and the export carry the masked value under the policy of rwb-access in force, with no unmasking operation on either read; Compliance either confirms that reading or publishes an audit-specific policy row before the wave 2 exit. |
| RWB-ITG-E2013-ITG, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E8008-APP, RWB-P4-E8008-CON, RWB-P6-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-CON, RWB-P7-E2013-OPS | R-22463 | GAP-1616 | Register gap | Risk and model risk officer with the rwb-access owner | The delegation of authority table is loaded and approved inside P7 while the ownership ruling gives the table to rwb-access | Keep in this service only the lookup at the moment of the decision and the recording of the row ID and version; move A2.24 with AC-P7-024-01 to AC-EXC-P7-024-05 to rwb-access, and confirm the lookup answer shape (level, row ID, version, NOT_COVERED, RELATED_PARTY reason) in the access contract. Until then this PRD reads the limits and records the version, and OQ-P7-05 stays open. |
| RWB-P4-AD005-APP, RWB-P4-AD005-CON, RWB-P4-E1022-APP, RWB-P4-E1037-CON | R-23009 | GAP-0795 | Register gap | rwb-access service owner with the security administrator role owner and the audit owner | The path and payload of the separation-of-duty check, the incident channel, the text of MSG-P4-006 and the approval route of a new conflict version are not specified for the app slice | Publish the check as POST /api/recovery/access/v1/authorise/separation-of-duty on the base of §R4 and DP-13 with a payload stated by this revision; carry the incident as the recorded refusal addressed to RW-SECADM until an incident operation exists; keep the ID MSG-P4-006 and leave its text to the business, reconciling it with RWB-P4-E1022-APP; load a version through the load path of RWB-P4-E1037-CON and let the check resolve the version in force; read the environment code through the parameters contract |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28578 | GAP-0162 | Register gap | Product head (Mortgage, HP, SSME) | The DoA limit amounts are not in this document | v5 names the owner (P4), the table (delegation_limit) and the two operations that serve it; the amounts stay in the Delegation of Authority Matrix and the DoA rule package and no amount is copied into this document. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28579 | GAP-0163 | Register gap | Compliance and PDPA officer | The masking rules per role, area and field group are not in this document | v5 names P4 as owner of masking_rule and GET /masking-policies as the contract; the rule values stay with Compliance and are loaded as a versioned reference data set. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28585 | GAP-2048 | Register gap | P4 rwb-access with Compliance | The alert recipient roles of version 3 are not mapped to role codes in rwb-access | The six recipient names are kept as they are and read as role names; the role codes are settled with the rwb-access role model before the per-service alert rules are built, and no code is invented here. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1038-APP | R-28587 | GAP-1579 | Register gap | Solution architect with Risk | No performance target covers the authorise answer, although every request passes one, and the nearest targets belong to other objects | Set one target for the authorise answer at the busiest hour, with the cache hit and the miss stated separately, and record it under DL11 beside the screen and rule-evaluation targets, so NFR-P4-001 becomes a testable number. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28588 | GAP-1576 | Register gap | Compliance with the solution architect | REQ-ACA-006 still requires an access entry for every read of the data lake copy, which Architecture v5 removes | Re-issue REQ-ACA-006 and NFR-042 in the next business requirement version as 'every read of the case store, the document store and a data product', so the requirement, the functional specification and this PRD use one list of objects; nothing else in the requirement changes. |
| RWB-ITG-E1039-ITG, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28591 | GAP-1591 | Register gap | Compliance and PDPA officer | NFR-042 still requires logging the data lake copy of the document store although the data lake is removed | The PRD requires every read of a document and of its extracted fields to be logged and carries no lake clause. NFR-042 needs the same correction in its next version. |
| RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-CON | R-28957 | GAP-0265 | Register gap | Compliance team | The masking rule has no owner on the page that lists who sees what | An Enforced by column names P4 rwb-access for the policy, the owning service that applies it, P10 rwb-agent for a prompt and the P1 login for an ACE value; DL26 still owns the rule content. |
| RWB-PLT-E1037-CON, RWB-PLT-E1072-CON, RWB-P4-E1037-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29029 | GAP-2809 | Register gap | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P4 rwb-access and platform library architects and the business owner of S4 | The D7.4 limit, the approval row and the rule-package read carry no value and no dependency row | Declare the approval as the P7 child workflow consumed on queue rwb-decision, the D7.4 limit and the approver's delegation as consumed on the rwb-access authorise contract, and the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43 as consumed from rwb-decision, each with the placeholder on its operation name and ceiling; fix no limit value in code or in the document, and leave the metadata rows as the plan gives them. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35559 | ASM-2839 | Register assumption |  | Every route approval limit is read from the versioned delegation table of rwb-access at run time, and the level applied and the approver are recorded on the decision. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35560 | ASM-2859 | Register assumption |  | Every approval limit is read from the versioned delegation table of rwb-access at run time, the level applied and the approver role are recorded on the treatment, and the module is tested with one documented test set until DL18 is answered. | Risk with the product heads, before wave 3 release |
| RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-P2-E2006-APP, RWB-P3-E1043-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P4-AD016-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-S2-E2006-APP | R-35561 | ASM-2883 | Register assumption |  | A release of a guarantor or of a TCG guarantee runs through the approval path in rwb-decision with the level read from the delegation table at run time, and the levels quoted in the design are not restated as values in this document. | Risk with the product heads, before wave 3 release |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E1038-APP | R-23040 | GAP-0838 |  | Who raises the incident behind a NOT_COVERED answer is not specified | Exception path X6 and the NOT_COVERED answer text are not in the chunk's story text, so no old text can be anchored. Re-send X6 with its section. |
| RWB-P4-E1038-APP | R-23043 | GAP-0970 |  | No DoA-specific load, approve, rollback or version-read operation is specified for rwb-access | Section 12.1 operation and shape rows are not in the chunk's story text, so the four admin rows cannot be anchored. Re-send section 12.1 with its table rows. |
| RWB-P4-E1038-APP | R-23045 | GAP-0971 |  | The rollback of a delegation version has no acceptance criterion, business rule or window semantics | Sections 7, 12.1 and 16 are not in the chunk's story text, so no AC, rollback row or TC can be anchored. Re-send those sections with their rows. |
| RWB-P4-E1039-APP | R-05693 | DOR-RWB-P4-E1039-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design in story or sources; sign-off must come from the epic design record. Searched the project folder; no value found. |
| RWB-P4-E1039-APP | R-05694 | DOR-RWB-P4-E1039-APP-16 | find it | Definition of Ready item 16 Size: Fail | No size in story or sources; the squad sizes the story at refinement, so no value can be written here. |
| RWB-P4-E1039-APP | R-05696 | DOR-RWB-P4-E1039-APP-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | rwb-case fake is already named in 12.8. Its library version is not in the sources (searched folder); the Not specified marker stays. |
| RWB-P4-E1039-APP | R-16678 | DOR-RWB-P4-E1039-APP-10 | find it | Definition of Ready item 10 Screens and states: Partial | SCR-38 and SCR-43 state text is outside this chunk, so the empty, loading, error and no-access states cannot be matched or added here. |
| RWB-P4-E1039-APP | R-16683 | DOR-RWB-P4-E1039-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR7, BR9, BR10, BR11 need criteria in section 7 and test cases in section 16, which are outside this chunk; no anchor to edit. |
| RWB-P4-E1039-APP | R-22112 | GAP-1571 | 7 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | L138 already holds the 4-hour placeholder as a versioned parameter. Reason bounds and review window are in AC text outside this chunk, so no old text was available. |
| RWB-P4-E1039-APP | R-22114 | GAP-0359 | 12 | Break-glass grant operation, central ledger fault point and SIT evidence are not named for the 19-service target | Section 12 text is not in this chunk. The grant operation and fault point are to be named at the future integration pack review, so no value is available now. |
| RWB-P4-E1039-APP | R-22115 | GAP-0780 | 12 | Local decision-record table, legacy break-glass path and the composition of the entry actions are not fixed by the sources | Section 12 criterion text is not in this chunk. The local table name and actions keys are in no source, so Not specified in the source documents (GAP-0780) applies. |
| RWB-P4-E1039-APP | R-22116 | GAP-0781 | 12 | The grant end and read paths, the 401 business message id and the full grant answer are not fixed by the sources | Section 12 operation text is not in this chunk. The 401 message id and grant state field are in no source, so they stay unspecified. |
| RWB-P4-E1039-APP | R-22117 | GAP-0782 | 13 | No source names the grant table, its two-person constraint, the retention period or the partition granularity of the access log | Section 13 text is not in this chunk. The grant table columns, retention period and partition granularity are not in sources (DL26 open). |
| RWB-P4-E1039-APP | R-22118 | GAP-0783 | 5 | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are deployment values in no source. Not applied. |
| RWB-P4-E1039-CON | R-05699 | DOR-RWB-P4-E1039-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | No signed epic design record in story sections 12 or 14 or in the cited sources. Sign-off stays Not specified in the source documents (DOR-RWB-P4-E1039-CON-14). |
| RWB-P4-E1039-DB | R-30884 | NEWAC-RWB-P4-E1039-DB-AC11 | 7 | AC11: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 text is not in this chunk, and the story file was not found by search, so no exact anchor exists. Needs the current section 7 and 16 text. |
| RWB-P4-E1039-OPS | R-05708 | DOR-RWB-P4-E1039-OPS-14 | Not located in chunk | Definition of Ready item 14 Epic design: Fail | No epic design record is named in the sources (22 and 04 searched). Setting sign-off would invent a record. Needs the record name. |
| RWB-P4-E1039-OPS | R-05711 | DOR-RWB-P4-E1039-OPS-22 | Not located in chunk | Definition of Ready item 22 Fake published: Fail | Sources name only the access-writer fake, with no version. A published contract fake version would be invented. Needs the version. |
| RWB-P4-E1039-OPS | R-22118 | GAP-0783 | Not located in chunk | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | Routes, thresholds, ACL set, cadence and secret names are absent from sources (GAP-0783, ASM-1430). Values need agreement with security and platform on-call. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (26)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08188 | RWB-P4-E1037-CON | CG-ALL-5003 | 12.1 | Publish POST /api/recovery/access/v1/admin/reference-loads in the rwb-access.yaml paths, as §12.1 provides it. |
| CDC-08189 | RWB-P4-E1037-CON | CG-ALL-5004 | 12.1 | Publish POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve in the rwb-access.yaml paths, as §12.1 provides it. |
| CDC-08190 | RWB-P4-E1037-CON | CG-ALL-5005 | 12.1 | Publish GET /api/recovery/access/v1/admin/roles in the rwb-access.yaml paths, as §12.1 provides it. |
| CDC-08191 | RWB-P4-E1037-CON | CG-ALL-5006 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in the rwb-access.yaml paths, as §12.1 provides it. |
| CDC-08192 | RWB-P4-E1037-CON | DOR-RWB-P4-E1037-CON-8 | 12.1 | Publish in rwb-access.yaml the paths detcheck flags: the four named in CG-ALL-5003 to 5006 and three more not named in this chunk. |
| CDC-08199 | RWB-P4-E1037-CON | GAP-1568 | 12 | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary; state in TSD P4 T3.1 how a group resolves to a role row and how a session behaves when a role is retired. |
| CDC-08203 | RWB-P4-E1037-CON | GAP-0159 |  | Add POST /authorise (role, scope, DoA), GET /me/permissions, GET /doa-limits and GET /masking-policies with request, response, status and error schemas; mark the bodies as placeholder per Architecture v5 slide 14. |
| CDC-08205 | RWB-P4-E1037-CON | GAP-2036 |  | Add request and response schemas, error codes and cache-refresh behaviour for POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies under /api/recovery/access/v1, with matching Ownership Map endpoint rows. |
| CDC-08207 | RWB-P4-E1037-CON | GAP-0779 |  | Keep /admin/reference-loads and its approve operation for rwb-access's own permission and masking tables under /api/recovery/access/v1; publish /masking-policies with Reference data R; publish AccessPolicyChanged with change kind, version and effective date and no personal value; answer the matrix read from both role slices under one contract. |
| CDC-08208 | RWB-P4-E1037-CON | GAP-0966 |  | Add the rule-package action vocabulary (LOAD, APPROVE, ROLLBACK, DRY_RUN, EVALUATE), its request and answer fields and a change decision code to the authorise contract; stub them in the contract fake. |
| CDC-08211 | RWB-P4-E1037-CON | GAP-2326 |  | Add the POST /authorise operation to the API specification index and define its agent-authority request and answer elements inside the operation this contract publishes; confirm them at the wave 1 contract review with the P10 owner. |
| CDC-08213 | RWB-P4-E1037-CON | GAP-0898 |  | Add the authorise and GET /me/permissions paths with request and answer schemas to the API specification and TSD P4 appendix T-A; stub them in the contract fake; publish the SCR-43 composite route with gateway-bff (DP-19). |
| CDC-08215 | RWB-P4-E1037-CON | GAP-0917 |  | Add the POST /authorise and GET /doa-limits request and answer schemas, with the fields listed in the item, and the rwb-access login in the platform DB story of DP-02. |
| CDC-08218 | RWB-P4-E1037-CON | GAP-0922 |  | Add the authorise path with request and answer schema, publish with RWB-P4-E1037-CON, stub in the contract fake, fix the rwb-access login in the platform DB story, and publish the gateway-bff route (DP-19). |
| CDC-08223 | RWB-P4-E1037-CON | GAP-0932 |  | Add the authorise, me-permissions and masking-policies request and answer shapes, and state whether the routed role or the holder is a request field. |
| CDC-08228 | RWB-P4-E1037-CON | GAP-0952 | 8 | Publish the authorise request and answer shapes, GET /me/permissions and the masking-policies shapes, and state whether a sync is authorised once for the manifest or once per item and how the field list is carried. Not specified in the source documents (GAP-0952). |
| CDC-08248 | RWB-P4-E1037-CON | GAP-0990 | 2 | Publish the authorise request and answer schema with the legalHold attribute; confirm the matrix version label with the matrix owner; TSD P4 T6.1 to tabulate the Queue and allocation letters. |
| CDC-08251 | RWB-P4-E1037-CON | GAP-0988 | 12.1 | Publish the review-item authorise request and answer schema, naming the review team attribute and all other attributes; record matrix and masking version labels with valid-from dates and environment; list review-field IDs with the masking pack version. |
| CDC-08274 | RWB-P4-E1039-APP | CG-ALL-5024 | 12.1 | Publish GET /api/recovery/access/v1/admin/access-log in rwb-access.yaml through RWB-P4-E1039-CON |
| CDC-08275 | RWB-P4-E1039-APP | CG-ALL-5025 | 12.1 | Publish POST /api/recovery/access/v1/admin/break-glass-grants in rwb-access.yaml through RWB-P4-E1039-CON |
| CDC-08276 | RWB-P4-E1039-APP | CG-ALL-5026 | 12.1 | Publish POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end in rwb-access.yaml through RWB-P4-E1039-CON |
| CDC-08277 | RWB-P4-E1039-APP | CG-ALL-5027 | 12.1 | Publish GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} in rwb-access.yaml through RWB-P4-E1039-CON |
| CDC-08278 | RWB-P4-E1039-APP | CG-ALL-5028 |  | Remove the closed fixed enum from defaultScope so LOV-SCOPE values are accepted as data without a code change |
| CDC-08280 | RWB-P4-E1039-APP | DOR-RWB-P4-E1039-APP-8 | 12.1 | Add the four paths named in the detcheck, including GET /api/recovery/access/v1/admin/access-log, POST .../admin/break-glass-grants, POST .../{grantId}/end and GET .../{grantId}, plus the two further paths; both POSTs carry Idempotency-Key as the story states. |
| CDC-08296 | RWB-P4-E1039-CON | CG-ALL-5036 | 12.1 | Add path POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end with the shape stated in section 12.1 |
| CDC-08297 | RWB-P4-E1039-CON | CG-ALL-5037 | 12.1 | Add path GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} with the shape stated in section 12.1 |

### RWB-P4-E1039-CON (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08201 | RWB-P4-E1037-CON | GAP-2208 | 13 | Add team as an additive optional filter on GET /cases; resolve owner display name at the edge against the ACE Common user directory; name the rwb-access access-log operation with the AC-EXPT fields in RWB-P4-E1039-CON. |
| CDC-08279 | RWB-P4-E1039-APP | DOR-RWB-P4-E1039-APP-21 |  | Complete the contract story to Done so its contract is published; its build status is currently Not started |
| CDC-08287 | RWB-P4-E1039-APP | GAP-2339 | 12.2 | State how grant ID and incident reference reach a consuming service (signed claim or call), their lifetime and reuse bound, and add the mechanism to GET /me/session. |
| CDC-08288 | RWB-P4-E1039-APP | GAP-2452 | 11 | Publish actions element names with grantId, incidentReference and reviewDueAt as working names; accept AC-VERS as an access code and map it; take parameter path from rwb-case contract. |
| CDC-08291 | RWB-P4-E1039-APP | GAP-2076 | 15 | Record that the access row carries the version the owning service applied at the event; rwb-decision registry stays the source of version and effective date. |
| CDC-08300 | RWB-P4-E1039-CON | DOR-RWB-P4-E1039-CON-10 | find it | Add empty, loading, error and no-access states for screen SCR-43 in the P3 screen document. |
| CDC-08313 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-21 | header | Complete the build and publish the contract; build status is Not started, not Done. |
| CDC-08334 | RWB-P4-E1039-DB | GAP-2339 |  | Fix how grant ID and incident reference reach rwb-document (signed short-lived claim or session call), their lifetime and reuse bound, and add the mechanism to the session contract. |
| CDC-08340 | RWB-P4-E1039-DB | GAP-2076 | find it | State that the access row records the version the owning service applied at the event, and that the rwb-decision registry remains the source of each version and its effective date. |
| CDC-08343 | RWB-P4-E1039-DB | GAP-2340 | find it | Add the capability-area code list including the document hub, the result code list, and the rule for a content read with no field values. Interim: area DOCUMENTS, legacy success result, no field ID. |
| CDC-08346 | RWB-P4-E1039-OPS | DOR-RWB-P4-E1039-OPS-21 | Header table | Publish the contract and set build status to Done. |
| CDC-08347 | RWB-P4-E1039-OPS | Definition of Ready item 23 Contract version fixed: Fail | header | Contract version row still records 5.0.0 from API Specification v5 as the service API version, pending the contract's own version. |
| CDC-08356 | RWB-P4-E1039-OPS | GAP-0966 | 12 | Add the rule-package action vocabulary, request and answer fields of POST /authorise and a change decision code; agree the code with the RWB-E1-039 access-log owner. |
| CDC-08359 | RWB-P4-E1039-OPS | GAP-0780 | none | Confirm the local decision-record table name with the DP-03 owner. Keep legacy POST /admin/break-glass as an alias of POST /api/recovery/v1/admin/break-glass-grants. Fix the actions keys in the contract before the endpoint is frozen. |
| CDC-08362 | RWB-P4-E1039-OPS | GAP-2339 | none | Add the mechanism that carries the grant ID and incident reference to a consuming service, as a signed short-lived claim in the session envelope, with its lifetime and reuse bound. A missing or expired claim means no grant. |
| CDC-08363 | RWB-P4-E1039-OPS | GAP-2452 | none | Keep the legacy actions list as the minimum content. Use grantId, incidentReference and reviewDueAt as working names. Map AC-VERS as an access code without fixing its subject. Take the parameter path from the rwb-case parameters contract. |
| CDC-08371 | RWB-P4-E1039-OPS | GAP-2340 |  | Add the capability-area code list including the document hub, the result code list, and the rule for a content read with no field values. Until then: area DOCUMENTS, legacy success result, no field ID. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08197 | RWB-P4-E1037-CON | DOR-RWB-P4-E1037-CON-7 | 11 | Add DF-REF-039 (role entra_group) to the LDM v9 or retire the ID from section 11 of this story. |
| CDC-08283 | RWB-P4-E1039-APP | DOR-RWB-P4-E1039-APP-7 | 11 | Add break_glass_grant as an entity with its fields in the LDM, or the dictionary name recorded in RWB-P4-E1039-DB. |
| CDC-08298 | RWB-P4-E1039-CON | CG-ALL-5035 | 12.7 | Record the object `break_glass_grant` as an entity or field in LDM v9, or the owning document must name its dictionary entry |
| CDC-08315 | RWB-P4-E1039-DB | CG-ALL-5041 | 1, 2, 4, 12.7, 13 | Add break_glass_grant as an entity with its fields, or record it as a table in the owning document. |
| CDC-08316 | RWB-P4-E1039-DB | CG-ALL-5042 | 3 | Record flyway_schema_history as a Flyway-managed library table in the owning document. |
| CDC-08317 | RWB-P4-E1039-DB | CG-ALL-5043 | 13 | Add grant_id as a field of break_glass_grant, or use the dictionary name in the owning document. |
| CDC-08318 | RWB-P4-E1039-DB | CG-ALL-5044 | 13 | Add incident_reference as a field of break_glass_grant, or use the dictionary name in the owning document. |
| CDC-08319 | RWB-P4-E1039-DB | CG-ALL-5045 | 13 | Add iam_request_id as a field of break_glass_grant, or use the dictionary name in the owning document. |
| CDC-08320 | RWB-P4-E1039-DB | CG-ALL-5046 | 13 | Record break_glass_grant column right_code in LDM v9 Fields, or name the dictionary field it maps to |
| CDC-08321 | RWB-P4-E1039-DB | CG-ALL-5047 | 13 | Record break_glass_grant column scope_code in LDM v9 Fields, or name the dictionary field it maps to |
| CDC-08322 | RWB-P4-E1039-DB | CG-ALL-5048 | 13 | Record break_glass_grant column starts_at in LDM v9 Fields, or name the dictionary field it maps to |
| CDC-08323 | RWB-P4-E1039-DB | CG-ALL-5049 | 13 | Record break_glass_grant column ends_at in LDM v9 Fields, or name the dictionary field it maps to |
| CDC-08349 | RWB-P4-E1039-OPS | CG-ALL-5055 | 12.7 | Record break_glass_grant as a table object of rwb_access, as the dictionary has no entity or field of that name. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08202 | RWB-P4-E1037-CON | GAP-1564 | header | Record that the permission matrix and DoA load, approve, verify and rollback stay with rwb-access (P4), keeping API-P4-005, 006, 009 and 010 with P4; parameter and LOV load stays with rwb-case (RWB-P3). |
| CDC-08220 | RWB-P4-E1037-CON | GAP-1252 |  | Add GET /api/recovery/access/v1/doa-limits to the API catalogue with P4 owner, P7/P3/P2 consumers, the query and the answer fields in the item. |
| CDC-08249 | RWB-P4-E1037-CON | GAP-2039 | 3 | Add access_log row: owner P4 rwb-access, schema rwb_access, own DB story in RWB-SVC-P4, with the ACE DBA. |
| CDC-08290 | RWB-P4-E1039-APP | GAP-2039 | 18 | Add an access_log row to the Tables sheet: owner P4 rwb-access, schema rwb_access, append-only, created by RWB-P4-E1039-DB. |
| CDC-08293 | RWB-P4-E1039-APP | GAP-0165 | 18 | Section 18 row for RWB-P4-E1039-DB names the append-only access log; the Ownership Map row is still to be added. |
| CDC-08294 | RWB-P4-E1039-APP | GAP-2069 |  | Add an access_log table owned by rwb_access (P4), append-only with a hash chain, behind GET /admin/access-log; DB story creates it and CON story publishes the read path. |
| CDC-08309 | RWB-P4-E1039-CON | GAP-2039 | find it | Add an access_log row to the Tables sheet: schema rwb_access, owner P4 rwb-access, append-only, with ACE DBA review of its key and retention. |
| CDC-08339 | RWB-P4-E1039-DB | GAP-2039 | find it | Add an access_log row: schema rwb_access, owner P4 rwb-access with the ACE DBA, linked to DB story RWB-P4-E1039-DB and read operation GET /admin/access-log. |
| CDC-08366 | RWB-P4-E1039-OPS | GAP-2039 |  | Add an access_log row owned by P4 rwb-access behind GET /admin/access-log, and add its DB story in RWB-SVC-P4. No story edit needed here. |
| CDC-08369 | RWB-P4-E1039-OPS | GAP-0165 |  | Add the access log as a P4 table in rwb_access, append-only, created by RWB-P4-E1039-DB, with its columns, retention and hash rule. |
| CDC-08370 | RWB-P4-E1039-OPS | GAP-2069 |  | Add an append-only access_log table in rwb_access owned by P4, with its hash chain, behind GET /admin/access-log; DB story creates it, contract story publishes the read. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08217 | RWB-P4-E1037-CON | GAP-1343 |  | Publish the six DP-added dependencies (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P4-E1037-CON as contract) with this story as consumer. |
| CDC-08237 | RWB-P4-E1037-CON | GAP-2335 | 13 | Add C RWB-P3-E1018-CON and C RWB-P4-E1037-CON to the search story's dependency map at D1 and state that the search builds against the two fakes. |
| CDC-08240 | RWB-P4-E1037-CON | GAP-1885 | find it | Carry the five consumed rows as non-blocking rows per the proposed fix; leave the plan metadata rows unchanged. |
| CDC-08241 | RWB-P4-E1037-CON | GAP-2751 | find it | Carry API-P5-002, API-P5-008, API-P3-002 and the other consumed reads as non-blocking rows per the proposed fix; leave plan metadata rows unchanged. |
| CDC-08242 | RWB-P4-E1037-CON | GAP-2801 | find it | Carry the four consumed appeal surfaces as non-blocking rows per the proposed fix; leave slice metadata rows unchanged. |
| CDC-08253 | RWB-P4-E1037-CON | GAP-1282 | 13 | Carry H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON as DP-added; correct metadata rows at the next story-set version. |
| CDC-08254 | RWB-P4-E1037-CON | GAP-1308 | 13 | Carry H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1047-CON and H RWB-PLT-E1044-CON as DP-added; correct metadata rows at the next version. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08244 | RWB-P4-E1037-CON | CG-ALL-5011 | 18 | Align the test lists of the REQ-ACA requirements in RTM v7 with the section 18 test case IDs of this story. |
| CDC-08269 | RWB-P4-E1038-APP | CG-ALL-5020 | 18 | Align the REQ-ACA-004 and REQ-APD-010 test case lists in RTM v7 with section 18 of RWB-P4-E1038-APP. |
| CDC-08282 | RWB-P4-E1039-APP | DOR-RWB-P4-E1039-APP-12 | 12.7, 16, 18 | Add TC-E1-039-13 against REQ-ACA-006 and align the test lists with this story's section 18. |
| CDC-08289 | RWB-P4-E1039-APP | CG-ALL-5030 | 18 | Align REQ-ACA-006 and REQ-ACA-008 test lists with section 18 of RWB-P4-E1039-APP at the next version. |
| CDC-08308 | RWB-P4-E1039-CON | CG-ALL-5039 | 18 | Align the test lists for REQ-ACA-006 and REQ-ACA-008 with section 18 of RWB-P4-E1039-CON in the next RTM version. |
| CDC-08338 | RWB-P4-E1039-DB | CG-ALL-5052 | 18 | Align the test lists of REQ-ACA-006 and REQ-ACA-008 with RWB-P4-E1039-DB section 18 in the next version of the RTM. |
| CDC-08365 | RWB-P4-E1039-OPS | CG-ALL-5059 | 18 | Align the REQ-ACA-006 and REQ-ACA-008 test lists in RTM with story section 18 (TC-E1-039-OPS-03, -05 and -06). Story section 18 is unchanged. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08194 | RWB-P4-E1037-CON | CG-ALL-5009 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (Events row 'new'; currently 'Not specified in the source documents (GAP-0127; ASM-0204)'): change kind, version label, effective date, approver reference; no field value, person, case id or role letter. |
| CDC-08257 | RWB-P4-E1038-APP | DOR-RWB-P4-E1038-APP-8 | 12.3 | State the payload of rwb.access.DoaLimitChanged.v1; the catalog row reads Not specified in the source documents (GAP-0127; ASM-0204). |
| CDC-08258 | RWB-P4-E1038-APP | CG-ALL-5016 | 12.3 | State the payload of rwb.access.DoaLimitChanged.v1; the catalog row reads Not specified in the source documents (GAP-0127; ASM-0204). |
| CDC-08345 | RWB-P4-E1039-OPS | CG-ALL-5057 | 12.3 | Add Events row for rwb.access.DoALimitChanged.v1 on topic rwb.access.events.v1, or name the catalogued type; story row kept. |
| CDC-08348 | RWB-P4-E1039-OPS | DOR-RWB-P4-E1039-OPS-8 | 12.3 | Add rwb.access.DoALimitChanged.v1 to Events sheet (see CG-ALL-5057). |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08195 | RWB-P4-E1037-CON | DOR-RWB-P4-E1037-CON-1 | 1 | Add role 'contract owner of rwb-access' as a role code or role name, or map section 1 to an existing role in Users Roles and Permissions v5. |
| CDC-08299 | RWB-P4-E1039-CON | DOR-RWB-P4-E1039-CON-1 | 1 | Add a role code or role name for 'tech lead', or confirm which existing role code section 1 should use. The v5 file has RW-* codes and no tech lead role. |
| CDC-08324 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-1 | 1 | Add role 'ACE database engineer' as a role code or role name |
| CDC-08350 | RWB-P4-E1039-OPS | DOR-RWB-P4-E1039-OPS-1 | 1 | Add role 'platform engineer' as a role code or name for the DevOps persona. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08243 | RWB-P4-E1037-CON | CG-ALL-5010 | 16 | Add rows for TC-P4-E1037-CON-01 to TC-P4-E1037-CON-05 with Given, When and Then copied from the criteria they cover. |
| CDC-08307 | RWB-P4-E1039-CON | CG-ALL-5038 | 16 | Add a Story test cases row for each of TC-E1-039-CON-01 to TC-E1-039-CON-07, with Given, When and Then copied from the criteria AC1 to AC7 they cover. |
| CDC-08337 | RWB-P4-E1039-DB | CG-ALL-5051 | 16 | Add rows for TC-E1-039-DB-01 to TC-E1-039-DB-07 with Given, When and Then copied from the criteria they cover. |
| CDC-08364 | RWB-P4-E1039-OPS | CG-ALL-5058 | 16 | Test case rows for OPS-01 to OPS-06 are added in the next Test Cases version. Section 16 now carries TC-07 to TC-09 as story rows. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08246 | RWB-P4-E1037-CON | GAP-0982 | find it | Add the case-authority request and answer schema, record where caller teams and regions are held, and list the case-record personal field IDs with their version. |
| CDC-08262 | RWB-P4-E1038-APP | GAP-1568 | find it | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary. In TSD P4 T3.1, state how a group resolves to a role row and what happens to a session when a role is retired. |
| CDC-08302 | RWB-P4-E1039-CON | GAP-2208 | 8 | Add the optional team filter to GET /cases (API-P3-001) as legacy section 12 states; resolve owner display name at the edge; record masking travel in the authorise answer. |
| CDC-08354 | RWB-P4-E1039-OPS | GAP-0661 | 12 | Baseline the read-only case-list and export on /api/recovery/integration/v1 with the columns, filters, paging envelope and problem body; declare the consumed operations and their paths in the P3 and P4 contract stories. |

### RWB-P4-E1037-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08256 | RWB-P4-E1038-APP | DOR-RWB-P4-E1038-APP-21 | Header | Move to Done the CON stories this story depends on, RWB-P4-E1037-CON and the others named in Depends on (build) and Contract dependencies, before contract publication. |
| CDC-08286 | RWB-P4-E1039-APP | GAP-0966 | unknown | Add rule-package actions LOAD, APPROVE, ROLLBACK, DRY_RUN and EVALUATE, their request and answer fields, and a change decision code agreed with the RWB-E1-039 access-log owner. |
| CDC-08305 | RWB-P4-E1039-CON | GAP-0966 | 7, 11 | Add the rule-package actions LOAD, APPROVE, ROLLBACK, DRY_RUN and EVALUATE, their request and answer fields, and a change decision code to POST /authorise, agreed with the decision codes of this story. |
| CDC-08329 | RWB-P4-E1039-DB | GAP-0966 | find it | Add rule-package actions LOAD, APPROVE, ROLLBACK, DRY_RUN, EVALUATE, their request and answer fields and a change decision code agreed with the access-log owner of RWB-E1-039. |

### OTHER:TSD P5 v2 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08292 | RWB-P4-E1039-APP | GAP-2341 | 18 | Add a rule stating which P5 reads write an access entry, under which decision code, and the owner of each entry. |
| CDC-08310 | RWB-P4-E1039-CON | GAP-2341 | find it | State which P5 reads write an access entry, under which decision code, and the owner of each entry; until then keep the content read only. |
| CDC-08368 | RWB-P4-E1039-OPS | GAP-2341 |  | State in the P5 contract which reads write an access entry, under which decision code, and the owner of each entry; until then only the content read is owned by this key. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08301 | RWB-P4-E1039-CON | DOR-RWB-P4-E1039-CON-7 | 11 | Define break_glass_grant as a field or entity so the P2 Name resolves. Section 11 BR Field ID column added here with placeholders. |
| CDC-08326 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-7 | 11 | Register break_glass_grant and its columns (grant_id, actor_user_id, incident_reference, iam_request_id, capability_area, right_code, scope_code, reason, state, starts_at, ends_at), flyway_schema_history and the other flagged names as fields or entities. |
| CDC-08353 | RWB-P4-E1039-OPS | DOR-RWB-P4-E1039-OPS-7 | 11 | Add break_glass_grant as an entity or field in LDM v9 and Data Classification v5, or align the name to an existing entry. |

### OTHER:Platform observability and parameters baseline (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08311 | RWB-P4-E1039-CON | GAP-2342 | find it | Name the incident queue and the session-answer reuse bound and record them as parameter rows. |
| CDC-08344 | RWB-P4-E1039-DB | GAP-2342 | find it | Name the incident queue and the session-answer reuse bound as parameter rows. Values: Not specified in the source documents (GAP-2342). Interim: queue is a service parameter; answer reused within one request. |
| CDC-08372 | RWB-P4-E1039-OPS | GAP-2342 |  | Name the platform administrator incident queue and the session-answer reuse bound, and record both as parameter rows. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08196 | RWB-P4-E1037-CON | DOR-RWB-P4-E1037-CON-12 | 12.7, 16, 18 | Register TC-P4-E1037-CON-01 to -05 in Test Cases v8; align P3 section 18 test lists with RTM v7. Story TC-P4-E1037-CON-06 added in section 16 and 18. |
| CDC-08352 | RWB-P4-E1039-OPS | DOR-RWB-P4-E1039-OPS-12 | 16 | Register TC-E1-039-OPS-01 to 07 in Test Cases v8; align the section 18 test lists with RTM v7. Story added TC-E1-039-OPS-07 as the contract test for AC2. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08212 | RWB-P4-E1037-CON | GAP-0895 |  | Record the rwb-access seed file path, format, owner, version label and row count, and state whether the DEV seed carries the SIT matrix version or a DEV-only label. |
| CDC-08250 | RWB-P4-E1037-CON | GAP-1083 | 3 | Record that the Litigation right and the scope test of the notice operations are enforced at the edge under RWB-PLT-N001-CON. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08255 | RWB-P4-E1038-APP | DOR-RWB-P4-E1038-APP-14 | none | Record the signed epic design sign-off for RWB-SVC-P4; no sign-off appears in the source documents. |
| CDC-08312 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-14 | header | Record the signed epic design sign-off for RWB-P4-E1039-DB. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08259 | RWB-P4-E1038-APP | CG-ALL-5018 | 4, 14 | Add a new message ID for 'The load or version reference is unknown to the caller's scope' with text 'We cannot find that. It may have been removed, or it may be outside your scope.', keeping MSG-P4-003 for 'A record outside the role's scope'. New ID not specified in the source documents (CG-ALL-5018). |
| CDC-08260 | RWB-P4-E1038-APP | CG-ALL-5019 | 4, 14 | Add a new message ID for 'The reference-data read or the store is unavailable during a load' with text 'The service is busy. Try again in a few minutes.', keeping MSG-GEN-006 for 'System of record unavailable (R-UNI-33)'. New ID not specified in the source documents (CG-ALL-5019). |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08284 | RWB-P4-E1039-APP | GAP-0661 | find it | Close GAP-0661 per R-22109: accept the proposed fix. Baseline the two read-only operations on /api/recovery/integration/v1 with unsettled JSON field names marked Not specified; state GET /cases and GET /cases/export stay with rwb-case. |
| CDC-08285 | RWB-P4-E1039-APP | GAP-0660 | find it | Close GAP-0660 per R-22110: keep GET /cases and GET /cases/export with rwb-case; add the composed read and export on the integration base as additional read-only composition, one hop each, 2 s budget. |

### OTHER:Integration register INT-34 (ACE Common contracts) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08193 | RWB-P4-E1037-CON | GAP-0013 | find it | Version each of the six ACE Common contracts and run contract tests on both sides from wave 1; owner ACE team. |

### OTHER:Technical Specification P1 v3 (T3.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08198 | RWB-P4-E1037-CON | GAP-0481 | 12.7 | Remove masking_rule from the P1 schema (V0001) and the P1 masking application; P1 takes the masking answer from POST /api/recovery/access/v1/authorise. |

### OTHER:rwb-case export story of legacy RWB-E1-031 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08200 | RWB-P4-E1037-CON | GAP-0355 | 11 | Read the export entry back through the P4 access-log contract; keep AC-EXPT with filters and row count in the entry; apply P4 masking rules over the P1 masked columns; keep owner display names synthetic in SIT. |

### OTHER:API catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08204 | RWB-P4-E1037-CON | GAP-0160 | L47 | Record the rename: GET /me/session (API Specification v4) maps to GET /me/permissions (Architecture v5). |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08206 | RWB-P4-E1037-CON | GAP-1569 |  | Add rows for AccessPolicyChanged and DoaLimitChanged on rwb.access.events.v1 with CloudEvents type, partition key, payload, versioning, consumer refresh window and missed-event fallback; update TSD P4 T5.3 from None to the two events. |

### RWB-P6-E1046-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08209 | RWB-P4-E1037-CON | GAP-1068 |  | Enforce the declared area and right at gateway-bff for every admin route and refuse an absent right with 403 MSG-P4-002; if a service-side authorise call is needed, add DP-08 and RWB-P4-E1037-CON to this story's patterns and contract dependencies. |

### RWB-P6-E1055-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08210 | RWB-P4-E1037-CON | GAP-1098 |  | Record that the declared area and right are enforced at gateway-bff on the screen path, and either add RWB-P4-E1037-CON as a contract dependency or state that a service identity call carries no user right. |

### OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08214 | RWB-P4-E1037-CON | GAP-0908 |  | Add the authorise path and the resolved permission view with request and answer schemas to appendix T-A and the API specification; publish with RWB-P4-E1037-CON; keep GET /me/session as its own story's read. |

### RWB-ITG-E2006-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08216 | RWB-P4-E1037-CON | GAP-1344 |  | Correct attribution: delegation_limit stays with P4 rwb-access; rwb-decision holds only the level read and the version applied, per Ownership Map v1 ruling. |

### RWB-P7-E2013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08219 | RWB-P4-E1037-CON | GAP-1251 | 8 | State that the level lookup is a read on the P4 contract with a 2 s budget, and that the approval stores delegation_limit_id, approval_level and limit_version only, with no join, view or foreign key into rwb_access (as BR14 in RWB-P4-E1037-CON). |

### RWB-P7-E2013-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08221 | RWB-P4-E1037-CON | GAP-1256 | 8 | Record the delegation version cache rule: local read-through cache warmed before readiness, refreshed on DoaLimitChanged, effective date as the switch, no copied table, alert when the cached version is older than the version in force (as BR15 in RWB-P4-E1037-CON). |

### OTHER:Story Build Order (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08222 | RWB-P4-E1037-CON | GAP-1223 |  | Read H as None plus the platform contracts named in the DP table; C as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. Story stays Day 1. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; OTHER:TSD P4 v3 appendix T-A and T6.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08224 | RWB-P4-E1037-CON | GAP-0941 |  | Publish the authorise path with request and answer schema, and state the service identity scope rule in TSD P4 T6.2. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; OTHER:TSD P4 v3 appendix T-A and the ledger code list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08225 | RWB-P4-E1037-CON | GAP-0946 |  | Add the authorise path with request and answer schema and the access entry decision codes to the ledger code list. |

### RWB-P6-E2021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08226 | RWB-P4-E1037-CON | GAP-1092 |  | Declare the capability area and right per operation, so gateway-bff asks rwb-access (DP-08) before the notice read call. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08227 | RWB-P4-E1037-CON | GAP-0955 |  | Publish the composite route field list for SCR-03 and SCR-04, and publish the authorise shapes in RWB-P4-E1037-CON before the send story. |

### RWB-P5-E2026-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08229 | RWB-P4-E1037-CON | GAP-0938 |  | Stub the generation facts in RWB-P5-E2026-CON, and add the authorise request and answer schema to the API spec and TSD P4 appendix T-A. |

### RWB-P2-E2033-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08230 | RWB-P4-E1037-CON | GAP-2320 |  | Fix the session answer element list, the authorise branch with its batch bound, and the extract record fields in baseline review, and record the P2 attribution as a build-against dependency. |

### RWB-P2-E2035-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; API:(service not named) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08231 | RWB-P4-E1037-CON | GAP-0667 | 4, 7, 12 | Serve GET /cases/{caseId}/next-action from the integration base under DP-13, correct the Ownership Map row to P2 read and P3 write, fix consumed names in the rwb-case, rwb-access and rwb-decision baselines, and record the timer register change. |

### RWB-P2-E2035-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:rwb-case, rwb-access and rwb-decision contract baselines (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08232 | RWB-P4-E1037-CON | GAP-0668 | 12 | Baseline the next-action contract with the three operation names, nine consumed shapes, split note, workflow and Schedule contract and error mapping; record the read path ruling in the Ownership Map; confirm the five message texts. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; OTHER:TSD P4 v3 appendix T-A; OTHER:platform DB story; OTHER:message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08233 | RWB-P4-E1037-CON | GAP-2322 | 12 | Add GET /api/recovery/access/v1/role-catalogue/{roleCode} with its answer schema, the authorise request and answer of a next-action read, the rwb-access login and the unknown or inactive role code message. |

### RWB-P2-E2036-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08234 | RWB-P4-E1037-CON | GAP-0957 | 12 | Carry the legacy section 12.1 element names of the placement admission and the non-human part of GET /me/permissions as the baseline; reconfirm with rwb-integration at review; keep caller type as a value of the approved callers list. |

### RWB-P2-E2036-CON; RWB-PLT-E1027-CON; OTHER:FSD P7 v3; OTHER:Work Package dependency rows; OTHER:platform DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08235 | RWB-P4-E1037-CON | GAP-2412 | 12 | Publish the placement fact element names on rwb.decision-record.v1; publish the P3 case-read, P4 authorise and reference-data shapes at wave 2 entry; add the MSG-P7-009 text; fix the per-service login; carry the C and H rows. |

### RWB-S8-E7004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08236 | RWB-P4-E1037-CON | GAP-3057 | 4 | Add the five consumed rows and the rule kit, outbox, access guard and Aric entries as class C or H with placeholders; publish the deviation state list before the DB story; bind escalation and unmapped code to messages. |

### RWB-P4-AD003-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08238 | RWB-P4-E1037-CON | GAP-0791 | 12 | Publish GET and PATCH /api/recovery/access/v1/admin/role-scopes/{roleCode} on the base of section R4 and DP-13; carry the predicate fields in the authorise answer; record scope change as AccessPolicyChanged kind SCOPE. |

### RWB-P4-AD003-CON; RWB-PLT-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08239 | RWB-P4-E1037-CON | GAP-0792 | 12 | Fix GET and PATCH admin/role-scopes on /api/recovery/access/v1 with Platform administration R and C; declare the predicate once; refusal 404 with MSG-P4-003 and OUT_OF_SCOPE; AccessPolicyChanged kind SCOPE. |

### OTHER:Security and Access Design version 5, section 7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08245 | RWB-P4-E1037-CON | GAP-2035 | find it | Write section 7 per service: one rwb_ login per service with grants on its own schema; rwb_source_data the only holder of the view grant; replace the recovery_svc row with a service login isolation row. |

### OTHER:TSD P4 T3.1 and the approved role conflict list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08247 | RWB-P4-E1037-CON | GAP-1574 | find it | Publish the approved role conflict list with its version label and effective dates; add matrix effective-date columns to T3.1; confirm the row counts of the version in force. |

### OTHER:TSD P7 v2 appendix T-A (API-P7-006) and RWB-E2-005 section 12 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08252 | RWB-P4-E1037-CON | GAP-1249 | 12.1 | Bind the 401 answer of the audit read to MSG-P4-001 once the platform catalogue binds that identifier to these reads. |

### OTHER:P3 screen definition SCR-41 (rwb-case) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08261 | RWB-P4-E1038-APP | DOR-RWB-P4-E1038-APP-10 | find it | Add empty, loading, error and no-access states to SCR-41. This story has no screen and states no UI state. |

### OTHER:RWB-P3 reference-data contract review (rwb-case contract owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08263 | RWB-P4-E1038-APP | GAP-1564 | find it | Confirm that rwb-access publishes the authorise, masking and DoA lookup answers and that load, approve, verify and rollback stay with rwb-case, with P4 validation called as part of that load. If the DoA and matrix files load inside rwb-access, restore API-P4-005, 006, 009 and 010 to P4 and record the ruling on the Ownership Map. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:TSD P4 v3 (T5.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08264 | RWB-P4-E1038-APP | GAP-1569 | none | Add AccessPolicyChanged and DoaLimitChanged rows on rwb.access.events.v1 with CloudEvents type, key, payload, versioning, refresh window and missed-event fallback; change TSD P4 T5.3 from None to the two events. |

### OTHER:Contract review (lookup division) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08265 | RWB-P4-E1038-APP | GAP-0842 | 12.1 | Division left open; no further edit |

### OTHER:TSD P4 v3 (T-A.2 API-P4-006) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08266 | RWB-P4-E1038-APP | GAP-0836 | 4, 12.1 | Correct the generic approve path declaration to right A in Rules and parameters for the DoA approval, through the change register. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08267 | RWB-P4-E1038-APP | GAP-0972 | none | Specify DoaLimitChanged as CloudEvents 1.0 on rwb.access.events.v1, key limitVersion, payload limitVersion, table, change kind, validFrom, validTo, rowCount, no personal data, published by outbox relay after commit. |

### OTHER:Service baseline rwb-access (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08268 | RWB-P4-E1038-APP | GAP-0973 | none | Add the dependency on RWB-PLT-TE006-CON (outbox and inbox library) at service-baseline review; metadata row left as the WP fixes it. |

### OTHER:Recovery Workbench P4 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08270 | RWB-P4-E1038-APP | GAP-0837 | 14 | Add MSG-P1-002 and MSG-P7-010 as shared entries, one id each, with the texts used in section 14 of RWB-P4-E1038-APP. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08271 | RWB-P4-E1038-APP | GAP-0841 | 12.3 | Specify rwb.access.DoaLimitChanged.v1 on rwb.access.events.v1 keyed on limitVersion, payload limitVersion, table, change kind, validFrom, validTo, rowCount, CloudEvents 1.0 envelope, no personal data, sent via outbox after commit. |

### OTHER:FSD P4 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08272 | RWB-P4-E1038-APP | GAP-0974 | 7 | Correct A2.6.3.3 and A2.6.2: RW-REFADM holds Reference data C and loads; the approver role in rwb.refload.approver.delegation_limit (RW-RISK) approves and rolls back; no screen in wave 1. |

### OTHER:Work Package plan (wp/B-P4-04.md, wp/B2-P4-010.md, checks/run_all.py) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08273 | RWB-P4-E1038-APP | GAP-2278 |  | Remove RWB-AD-016 from the B-P4-04 fanout so B2-P4-010 alone owns it; number CG and ASM ids once; add a plan-uniqueness check to checks/run_all.py. |

### RWB-P4-E1039-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08281 | RWB-P4-E1039-APP | CG-ALL-5023 | 11 | Record break_glass_grant and its fields as the object it creates in rwb_access, with the dictionary name if one is assigned in LDM v9 or Data Classification v5. |

### OTHER:_work/msr/wp/B-P4-02.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08295 | RWB-P4-E1039-APP | GAP-2270 |  | Remove RWB-AD-006 and its three story lines from the fanout (5 to 4) so B2-P4-005 alone owns the key; write the edit log row. |

### OTHER:Integration contract story for rwb-integration (composed case-list read) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08303 | RWB-P4-E1039-CON | GAP-0661 | 11 | Baseline the two read-only operations on /api/recovery/integration/v1 and fix the consumed access-log operation as GET /admin/access-log of this story. |

### OTHER:Integration contract story for rwb-integration (composed case-list read and export) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08304 | RWB-P4-E1039-CON | GAP-0660 | 11 | Add the composed read and export as additive read-only paths and fix the access-log read as GET /admin/access-log of this story. |

### OTHER:rwb-access session contract (GET /api/recovery/access/v1/me/session) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08306 | RWB-P4-E1039-CON | GAP-2339 | 12.2 | Add a signed, short-lived claim carrying grantId and incidentReference to the session envelope, with its lifetime and reuse bound; a missing or expired claim is no grant. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08314 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-22 | header | Publish a contract fake library version for the rwb-access contract. |

### RWB-P4-E1039-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08325 | RWB-P4-E1039-DB | DOR-RWB-P4-E1039-DB-10 |  | Give SCR-43 its empty, loading, error and no-access states in the app story that owns the screen |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08327 | RWB-P4-E1039-DB | GAP-0661 | find it | Baseline GET /api/recovery/integration/v1/case-list and its export with columns, filters, breach filter, order, paging envelope and problem body; declare the eight consumed operations; state that GET /cases and /cases/export stay with rwb-case. |

### OTHER:rwb-integration API contract and the P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08328 | RWB-P4-E1039-DB | GAP-0660 | find it | Add the composed case-list read and export on the integration base as additional read-only composition; fix ageing, reference-data and access-log operations and parameters in the P3 and P4 contract stories. |

### OTHER:RWB-P4 integration pack review record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08330 | RWB-P4-E1039-DB | GAP-0359 |  | Name POST /admin/break-glass-grants as the grant operation, the local decision-record write as the fault point and the SIT evidence location before the SIT run. |

### OTHER:DP-03 library contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08331 | RWB-P4-E1039-DB | GAP-0780 |  | Confirm the local decision-record table name in rwb_access with the DP-03 owner; fix the actions keys in the contract before the endpoint is frozen. |

### OTHER:TSD P4 v3 (T-A) and message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08332 | RWB-P4-E1039-DB | GAP-0781 |  | Add end and read operations for break-glass grants, the 401 expired-session message id and the full grant answer with state field. |

### OTHER:Platform deployment values and secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08333 | RWB-P4-E1039-DB | GAP-0783 |  | Agree alert routes and thresholds for failed access-log writes and break-glass use; set Kafka ACL set, retry cadence and secret names in values files and secret store. |

### OTHER:FSD P7 decision-log contract and message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08335 | RWB-P4-E1039-DB | GAP-2452 |  | Name the actions elements and the read elements grantId, incidentReference and reviewDueAt as working names; map AC-VERS as an access code; use the catalogue format for MSG-P7-009. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08336 | RWB-P4-E1039-DB | GAP-3194 |  | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the 42-column drop, or attach the drop to the creating APP story, and cite the chosen story on Ownership Map row 121. |

### OTHER:TSD P5 v2 (API-P5-003; OTHER:API-P5-009; OTHER:API-P5-011) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08341 | RWB-P4-E1039-DB | GAP-2341 | find it | State which P5 reads write an access entry, under which decision code, and the owner of each entry; until then only the content read is owned by this key. |

### OTHER:ownership.json (api and table entries) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08342 | RWB-P4-E1039-DB | GAP-2069 | 8 | Add an access_log table entry in rwb_access owned by P4, linked to GET /admin/access-log. BR5 now names the table and the DB story creates it. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08351 | RWB-P4-E1039-OPS | Definition of Ready item 11 Guardrails: Partial | 11 | Personal-data status of the data table fields is marked Not specified and left to Data Classification v5; the unsupported 'none personal' claim is removed. |

### OTHER:P3 and P4 contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08355 | RWB-P4-E1039-OPS | GAP-0660 | 12 | Fix the ageing read, reference-data read and access-log operation in the P3 and P4 contract stories; keep GET /cases and GET /cases/export with rwb-case. |

### OTHER:Recovery Workbench FSD P4 (FEAT-ACA-10) and its parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08357 | RWB-P4-E1039-OPS | GAP-1571 | none | Hold the break-glass maximum duration, the reason bounds and the review window as versioned parameters read at run time by FR-P4-028 and FR-P4-031. Keep 4 hours and 20 to 1000 characters as placeholders. Review window: Not specified in the source documents (GAP-1571). |

### RWB-ITG-E1039-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08358 | RWB-P4-E1039-OPS | GAP-0359 | none | At the integration pack review before the SIT run, name the grant operation, the local decision-record fault point and the evidence location. Keep the window, incident pattern and reason length as parameter values. |

### OTHER:TSD P4 v3 (API-P4-013) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08360 | RWB-P4-E1039-OPS | GAP-0781 | none | Add the end and read operations at /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end and /api/recovery/access/v1/admin/break-glass-grants/{grantId}. Confirm the grant state field with the security administrator. Expired-session message id: Not specified in the source documents (GAP-0781). |

### RWB-P4-E1039-DB; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08361 | RWB-P4-E1039-OPS | GAP-0782 | none | Name the grant table break_glass_grant with a unique partial constraint on the active grant of an actor. Set access-log retention and partition granularity as parameter rows. Retention period: Not specified in the source documents (GAP-0782). |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08367 | RWB-P4-E1039-OPS | GAP-2076 |  | State that the access row records the version the owning service applied at the event, with rwb-decision keeping the registry as source of version and effective date. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0013 | ACE Common contracts are not versioned or scheduled | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0359 | Break-glass grant operation, central ledger fault point and SIT evidence are not named for the 19-service target | Tech lead | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0660 | rwb-integration composed case-list read and export: ownership duplication, service-base paths, ageing and access-log contracts, parameters, reference data and flag switch not settled | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0661 | rwb-integration composed case-list contract baseline: page shape, filter names, aging read, access-log operation and path attribution not settled by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0667 | rwb-integration next action resolution: login, ownership of the read path, contract field names, operation names, Schedule values, message texts, legacy rule values and the timer vocabulary not settled | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0668 | rwb-integration next action contract: the read path ownership, the three operation names, the consumed shapes, the Schedule values and the timer vocabulary are not fixed by a source | Solution architect; contract owners of rwb-case, rwb-access and rwb-decision; platform workflow kit owner | Resolved (directive) |
| GAP-0679 | The column-level split of the legacy role and permission tables between rwb-case and rwb-access is not defined | Solution architect | Resolved (directive) |
| GAP-0694 | The exact field masking contract shape is not given | P4 access owner | Resolved (directive) |
| GAP-0776 | The two operation paths and their request and answer payloads are not specified by any source for the access contract of rwb-access | contract owner of rwb-access with the consuming squads | Resolved (directive) |
| GAP-0778 | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0780 | Local decision-record table, legacy break-glass path and the composition of the entry actions are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0781 | The grant end and read paths, the 401 business message id and the full grant answer are not fixed by the sources | Solution architect | Resolved (directive) |
| GAP-0782 | No source names the grant table, its two-person constraint, the retention period or the partition granularity of the access log | ACE database engineer | Resolved (directive) |
| GAP-0783 | Alert routes, thresholds, Kafka ACL set, retry cadence and secret names are not fixed by the sources | DevOps engineer | Resolved (directive) |
| GAP-0791 | The two scope operation paths, the scope predicate fields and the home of the LOV-SCOPE list are not specified for the scope app slice | rwb-access service owner with the contract owner and the architecture review | Resolved (directive) |
| GAP-0792 | The scope contract has no source for its two paths, its predicate shape, its refusal entry fields or its version rule | contract owner of rwb-access with the consuming squads and the guard library owner | Resolved (directive) |
| GAP-0796 | The check path and payloads, the name of the conflict-version field of the session answer and the rights of the two administrative reads are this contract's decision and not a source value | contract owner of rwb-access with the sign-in contract owner and the session contract owner | Resolved (directive) |
| GAP-0833 | The DoA load and approval paths are not in an approved source, and two P4 stories declare them | Solution architect | Resolved (directive) |
| GAP-0836 | The right that gates the approval is stated as Reference data A in one source and as Rules and parameters A in another, and as a parameter in a third | Security administrator | Resolved (directive) |
| GAP-0837 | MSG-P1-002 and MSG-P7-010 are messages of other catalogues and the P4 message list does not carry them | Business analyst, P4 | Resolved (directive) |
| GAP-0838 | Who raises the incident behind a NOT_COVERED answer is not specified | Solution architect | Resolved (directive) |
| GAP-0839 | The RELATED_PARTY answer does not say whether the reason is a code on the answer or a row condition | Business analyst, P4 | Resolved (directive) |
| GAP-0841 | The DoaLimitChanged event key and payload are not specified | Solution architect | Resolved (directive) |
| GAP-0842 | The lookup operation is claimed by two P4 stories | Solution architect | Resolved (directive) |
| GAP-0895 | rwb-access sandbox seed: the access seed file's location, format, version label and row count are not specified, and whether the DEV matrix version must equal the SIT version is not stated | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0898 | rwb-access sandbox seed: the authorise and me/permissions request and answer shapes, and the screen route that shows the seeded rows, are absent from the TSD appendix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0908 | rwb-access plan status: the authorise request and answer shapes and the resolved permission view are absent from the TSD P4 appendix, including whether the plan reference travels in the authorise request | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0915 | The field names of the masking answer inside the authorise reply and the masking-policies read are not specified | Solution architect | Resolved (directive) |
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0922 | rwb-access booking confirmation: the authorise request and answer shapes, the contract entry of the authorise path and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0925 | POST /authorise request and response shape is not specified for the payment-matching reads | Solution architect | Resolved (directive) |
| GAP-0932 | The request and response shape of the authorise operation is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0934 | The object attributes an authorise request carries are not specified | Solution architect | Resolved (directive) |
| GAP-0938 | The authorise request and answer for a document generation request are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0941 | rwb-access document set: the authorise request and answer shape for the document screens, and the scope a service identity is asked for, are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0946 | rwb-access letter dispatch loop: the authorise request and answer shape for a notice request, a notice read and a dispatch read is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0952 | The request and answer shape of the authorise call for a multi-item sync is not specified | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0955 | The authorise shape for a send and the field list of the composite route are not specified | Solution architect, P4 and the gateway-bff owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0957 | rwb-access queue-write authority: the request and answer element set of the placement admission part of POST /authorise and of the non-human part of GET /me/permissions is named by no source | Solution architect | Resolved (directive) |
| GAP-0966 | rwb-access rule-package authority: the action vocabulary, the request and answer shape of the rule-package part of POST /authorise and the access-log decision code of a rule-package change are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0970 | No DoA-specific load, approve, rollback or version-read operation is specified for rwb-access | Solution architect | Accepted (directive); not applied: value not in the source documents |
| GAP-0971 | The rollback of a delegation version has no acceptance criterion, business rule or window semantics | Business analyst, P4 | Accepted (directive); not applied: value not in the source documents |
| GAP-0972 | The payload, key and publication point of rwb.access.DoaLimitChanged.v1 are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0973 | Publishing DoaLimitChanged needs the outbox library of DP-09, which this slice's dependency list and pattern list do not carry | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0974 | FSD P4 v3 gives the DoA feature to the Security administrator as primary actor, while the story, the parameter and the criteria give RW-REFADM as loader and RW-RISK as approver | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0988 | The review-item authorise request shape, the label of the matrix and masking versions in force at the release date, and the review-field roster of the masking pack are fixed by no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1068 | The service-side guard on the admin operations is not specified and DP-08 is not declared | Solution architect | Resolved (directive) |
| GAP-1083 | The scope and right check of the notice operations has no rwb-access dependency row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1092 | The scope test of the notice read has no scope source in the dependencies of this story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1249 | Message identifier of the 401 answer is not given by any source | Solution architect, with the platform library owner | Resolved (directive) |
| GAP-1250 | Access record of a query: local decision record or the rwb-access access log | Solution architect, with the P4 access owner | Resolved (directive) |
| GAP-1251 | The delegation of authority table is P4 rwb-access's while the routing rules and the approval resource are P7 rwb-decision | Solution architect | Resolved (directive) |
| GAP-1252 | The delegation limits operation has no row in the Ownership Map API catalogue | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1256 | The delegation snapshot and its cache refresh have no named operation, store or interval | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1343 | The platform and published dependencies this slice adds through the decoupling patterns are not carried by the empty metadata rows | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1344 | The delegation of authority table is ruled to rwb-access by the Ownership Map while the integration story of this key attributes the required level to rwb-decision | Solution architect | Resolved (directive) |
| GAP-1404 | Library artefact coordinates, the policy cache time to live, the authorise payload and the split of the masking read between P4's policy and P1's read are not specified | Platform library architect with the P4 rwb-access owner and the P1 rwb-source-data owner | Resolved (directive) |
| GAP-1405 | The contract shapes of the guard and masker, the /masking-policies path, the audit record shape and the failure mapping are not specified | Platform library contract owner with the P4 rwb-access contract owner | Resolved (directive) |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1569 | AccessPolicyChanged and DoaLimitChanged are published by rwb-access in Architecture v5 but have no row, payload, key or refresh window in the event design | Solution architect with the platform event owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1571 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | SCB IT security with the security administrator | Resolved (directive) |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2036 | The authorise contract has no request or response shape in any source | TechX with P4 rwb-access | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2041 | Partner users moved to S9 rwb-partner, while the approving role owner stays in P4 | S9 rwb-partner with P4 rwb-access | Resolved (directive) |
| GAP-2063 | The edge components have no owner row in the Ownership Map, and section 5 needs one | Platform (RWB-PLT-EDGE) with S9 rwb-partner | Resolved (directive) |
| GAP-2069 | The access log has an API and an owner but no table in the Ownership Map | Service owner P4 rwb-access | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2270 | Two Work Packages write the same three story files and three fragments for legacy RWB-AD-006 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2316 | The agent-monitor object of the access log, the record code of a read, the field list of an entry and the migration step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2320 | rwb-access answer behind the case and queue list: element names, the P2 attribution of the contract dependency, the authorise branch, the extract record, the login and the parameter and reference paths are not settled by any source read | Solution architect | Resolved (directive) |
| GAP-2321 | The masking version label, the covered ledger field IDs, the access-log granularity, the parameter rows and the login name of the access answer are not in the sources | Solution architect and the rwb-access contract owner | Resolved (directive) |
| GAP-2322 | rwb-access next action: the role-catalogue operation, the authorise request and answer of a next-action read, the rwb-access login and the message for an unknown role code are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2326 | The agent-authority part of POST /authorise has no operation row, request shape or answer shape in any source | Solution architect, P4 and the API specification owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2332 | The access-event codes of a dashboard read, the entry field list, the page bounds, the read index and the Flyway step are named in no source | Tech lead of rwb-access with the ledger owner | Resolved (directive) |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2339 | How the active break-glass grant and its incident reach rwb-document on a document content read is not stated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2340 | The capability-area code, the result code and the field list of a document content read in an access entry are not specified | Data steward | Resolved (directive) |
| GAP-2341 | Which reads of the document hub other than the content read write an access entry in the target is not fixed | Solution architect | Resolved (directive) |
| GAP-2342 | The incident queue name and the session-answer reuse bound of the content read are not specified | DevOps team | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2452 | No source gives the ledger's access shape: the element names inside the actions payload beyond the legacy list, the grant, incident and review-due elements of the decision-log read, the use of the access code AC-VERS, and the catalogue entry format of MSG-P7-009 | Business analyst P7 | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-P4-E1038-APP | new AC without TC row | 484 | AC10 is new and no section 16 row covers it |
| RWB-P4-E1039-DB | duplicate TC ID | 357 | TC-E1-039-DB-08 |
