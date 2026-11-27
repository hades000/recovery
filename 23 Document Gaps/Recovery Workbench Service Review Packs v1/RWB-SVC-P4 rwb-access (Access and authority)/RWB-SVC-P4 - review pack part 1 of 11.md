# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 1 of 11 (RWB-P4-AD001-APP to RWB-P4-AD008-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 16 |
| Resolved in the stories | 305 |
| Cross-document (pending in another document) | 224 |
| Not applied (value not in the sources) | 24 |
| Open business decisions | 23 |
| Register gaps linked | 48 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-AD001-APP | 14 | 16 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD001 APP Map Entra ID groups to Workbench roles v2.md |
| RWB-P4-AD001-CON | 24 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD001 CON Map Entra ID groups to Workbench roles - contract v2.md |
| RWB-P4-AD002-APP | 20 | 28 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD002 APP Permission matrix as a versioned load v2.md |
| RWB-P4-AD002-CON | 27 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD002 CON Permission matrix as a versioned load - contract v2.md |
| RWB-P4-AD003-APP | 21 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD003 APP Scope per role v2.md |
| RWB-P4-AD003-CON | 21 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD003 CON Scope per role - contract v2.md |
| RWB-P4-AD004-APP | 21 | 10 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD004 APP Masking profiles per role v2.md |
| RWB-P4-AD004-CON | 20 | 8 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD004 CON Masking profiles per role - contract v2.md |
| RWB-P4-AD005-APP | 14 | 14 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD005 APP Separation of duty check at sign-in v2.md |
| RWB-P4-AD005-CON | 21 | 11 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD005 CON Separation of duty check at sign-in - contract v2.md |
| RWB-P4-AD006-APP | 15 | 13 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD006 APP Break-glass access v2.md |
| RWB-P4-AD006-CON | 17 | 10 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD006 CON Break-glass access - contract v2.md |
| RWB-P4-AD006-DB | 18 | 18 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD006 DB Break-glass access - ACE DB v2.md |
| RWB-P4-AD007-APP | 20 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD007 APP Access log search and export v2.md |
| RWB-P4-AD007-CON | 16 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD007 CON Access log search and export - contract v2.md |
| RWB-P4-AD008-APP | 16 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD008 APP Access review list v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-AD002-CON | R-01058 | CG-ALL-4542 | Script gap | Product owner | The story adds MATRIX to the closed list LOV-CAPABILITY | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-AD003-APP | R-01066 | CG-ALL-4557 | Script gap | Product owner | The story adds SCOPE to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-AD003-CON | R-01071 | CG-ALL-4565 | Script gap | Product owner | The story adds SCOPE to the closed list LOV-SCOPE | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-P4-AD001-APP | R-10525 | CG-ALL-4516 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-AD005-APP | R-10544 | CG-ALL-4601 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-AD006-DB | R-10564 | CG-ALL-4642 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-AD007-APP | R-10568 | CG-ALL-4652 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-P4-AD008-APP | R-10580 | CG-ALL-4678 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-22113 | GAP-1570 | Register gap | Compliance with the solution architect | The access log has no stated retention, no stated searchable period, no stated storage object and no stated cross-service read right, although it is the evidence for every access question | Answer DL26 for the access log in one row: the retention period, whether it equals the decision log period, which object answers the query (the local record, the central ledger, or a projection of both), which fields are searchable and for how far back, and which roles in other services may read it. Until then this PRD keeps the classification at PII and marks the retention as not set. |
| RWB-ITG-E2003-ITG, RWB-P2-E2003-APP, RWB-P4-AD004-APP, RWB-P4-E2003-APP | R-22343 | GAP-0910 | Register gap | Compliance and PDPA officer (RW-COMPLY) | The roster of roles that see the other-products account number unmasked is an assumption of the legacy story | Confirm the five clear roles and that every other role holding Case record R is masked, then load the roster through the masking load path of RWB-P4-AD004-APP. |
| RWB-P4-AD004-APP, RWB-P4-AD004-CON | R-23006 | GAP-2266 | Register gap | Solution architect, P4 and ACE Common audit and PII owner | Masking-profile operations, the PII record and the field-to-column map are not named for rwb-access | Confirm the three profile paths and their rights at the contract-group review of wave 4, name the PII record producer and field list with the ACE Common audit and PII owner, and fix the field-to-view-and-column resolution as a P1 field-registry call with no column added to masking_rule. |
| RWB-P4-AD005-APP, RWB-P4-AD005-CON, RWB-P4-E1022-APP, RWB-P4-E1037-CON | R-23009 | GAP-0795 | Register gap | rwb-access service owner with the security administrator role owner and the audit owner | The path and payload of the separation-of-duty check, the incident channel, the text of MSG-P4-006 and the approval route of a new conflict version are not specified for the app slice | Publish the check as POST /api/recovery/access/v1/authorise/separation-of-duty on the base of §R4 and DP-13 with a payload stated by this revision; carry the incident as the recorded refusal addressed to RW-SECADM until an incident operation exists; keep the ID MSG-P4-006 and leave its text to the business, reconciling it with RWB-P4-E1022-APP; load a version through the load path of RWB-P4-E1037-CON and let the check resolve the version in force; read the environment code through the parameters contract |
| RWB-P4-AD007-APP, RWB-P4-AD007-CON | R-23015 | GAP-0803 | Register gap | Compliance and PDPA officer | No rule says which masking version applies to an old entry in the export | The masking version recorded on the entry applies and is shown in its masking_version column, in the answer and in the file. |
| RWB-ITG-E1039-ITG, RWB-P4-AD007-APP, RWB-P4-AD007-CON, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-P5-E1039-APP, RWB-P7-E1039-APP | R-28588 | GAP-1576 | Register gap | Compliance with the solution architect | REQ-ACA-006 still requires an access entry for every read of the data lake copy, which Architecture v5 removes | Re-issue REQ-ACA-006 and NFR-042 in the next business requirement version as 'every read of the case store, the document store and a data product', so the requirement, the functional specification and this PRD use one list of objects; nothing else in the requirement changes. |
| RWB-ITG-E2036-ITG, RWB-PLT-E1027-CON, RWB-P2-E2036-APP, RWB-P2-E2036-CON, RWB-P3-E2036-APP, RWB-P4-AD007-APP, RWB-P4-E2036-APP, RWB-P7-E2036-APP, RWB-S8-E2036-APP | R-28854 | GAP-0961 | Register gap | Internal audit | rwb-access queue-write authority: the decision code of the access entry for a placement admission and the entry fields beyond the standard record columns are fixed by no source | Use AC-READ for an admission and AC-DENY for a refusal, keep D6 for the adapter's own admission record where RWB-P2-E2036-CON already uses it, and leave the column set to RWB-PLT-E1027-CON; confirm with Internal audit at the access-log story (RWB-P4-AD007-APP) that a placement admission reads as an access entry and not as a business decision. |
| RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-CON | R-28957 | GAP-0265 | Register gap | Compliance team | The masking rule has no owner on the page that lists who sees what | An Enforced by column names P4 rwb-access for the policy, the owning service that applies it, P10 rwb-agent for a prompt and the P1 login for an ACE value; DL26 still owns the rule content. |
| RWB-P4-AD007-APP, RWB-P4-AD007-CON | R-28959 | GAP-0805 | Register gap | Compliance and PDPA officer | The retention of access entries is not specified | Retention follows the decision log's retention rule (NFR-030); no separate rule is built for the access log. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-P4-AD007-APP | R-36525 | ASM-1504 | Register assumption |  | The masking version recorded on an entry is the version that masks it in the answer and in the export, and it is shown in the masking_version column; a later masking version does not rewrite an old entry. | Compliance and PDPA officer and the data steward |
| RWB-P4-AD007-APP, RWB-P4-AD007-CON | R-36529 | ASM-1506 | Register assumption |  | Access entries are retained under the decision log's retention rule (NFR-030); no separate access-log retention rule, job or deletion path is built in this story. | Compliance and PDPA officer |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-AD001-APP | R-10524 | CG-ALL-4515 | 14 | MSG-GEN-006 is used with another meaning than the standard's | The standard's meaning and text are not in the sources, so the row cannot be aligned to them (see DOR-RWB-P4-AD001-APP-9). |
| RWB-P4-AD001-APP | R-16330 | DOR-RWB-P4-AD001-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | No field list or personal-data classification source is in the chunk or the cited sources. Naming fields would invent them. Needs the field list in a later chunk. |
| RWB-P4-AD001-APP | R-16332 | DOR-RWB-P4-AD001-APP-17 | header | Definition of Ready item 17 Dependencies: Partial | The six dependencies and the RWB-P4-E1022-APP gate must be added to the story; the diff does not show them. |
| RWB-P4-AD001-APP | R-16336 | DOR-RWB-P4-AD001-APP-4 | 7, 16 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so there is no exact text to anchor the BR1 to BR12 criteria and test rows. Needs a chunk with those sections. |
| RWB-P4-AD001-APP | R-25207 | CG-ALL-4517 | 3, 3.1 | Flyway file V4001_1__role_mapping_version.sql is not in the V0001..Vnnnn form | Next free number in rwb-access's V sequence is not in the sources; only V0001 is named. The V4001_1 filename sits outside this chunk. Renumbering would invent a value. |
| RWB-P4-AD002-APP | R-16353 | DOR-RWB-P4-AD002-APP-9 | 14 | Definition of Ready item 9 Messages: Partial | The standard's meaning of MSG-GEN-006 is not in the sources. Aligning the row would invent its text. Left unchanged. |
| RWB-P4-AD002-APP | R-23217 | GAP-2288 | find it | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | The pack ACs and test cases belong in sections 7 and 16, which are not in this chunk. Apply them in the chunk that holds those sections. |
| RWB-P4-AD002-APP | R-25212 | CG-ALL-4536 | 3, 3.1 | Flyway file V4001_2__permission_matrix_version.sql is not in the V0001..Vnnnn form | The next free number of the service Flyway sequence is not in the sources. Grep for V4001_2 and db/migration found no service sequence value. Line 336 is not in this chunk. |
| RWB-P4-AD003-CON | R-05439 | DOR-RWB-P4-AD003-CON-14 | none | Definition of Ready item 14 Epic design: Fail | No signed epic design record in 03 Requirements or 22 Jira Impact, or elsewhere in the project folder (grep). Needs the epic design record to confirm sign-off. |
| RWB-P4-AD003-CON | R-05440 | DOR-RWB-P4-AD003-CON-16 | header | Definition of Ready item 16 Size: Fail | Not specified in the source documents (DOR-RWB-P4-AD003-CON-16). No size in Jira Impact or Requirements; section 14 was not in this chunk, so no change there. |
| RWB-P4-AD005-APP | R-05454 | DOR-RWB-P4-AD005-APP-14 | 3 | Definition of Ready item 14 Epic design: Fail | No epic design sign-off record in the sources (grep of 03 Requirements found none). Section 3 already has the Not specified row, so no value can be confirmed. |
| RWB-P4-AD005-APP | R-05458 | DOR-RWB-P4-AD005-APP-23 | 3 | Definition of Ready item 23 Contract version fixed: Fail | No contract version in the sources. Section 3 already has the Not specified row naming only the Draft RWB-P4-AD005-CON. No version can be stated without inventing one. |
| RWB-P4-AD005-APP | R-16397 | DOR-RWB-P4-AD005-APP-17 | section header | Definition of Ready item 17 Dependencies: Partial | The claim that E1022-APP is the one build dependency not yet done is wrong: RWB-P4-AD005-CON is Not started. Row left unchanged; the dependency gap is not closed by the story. |
| RWB-P4-AD005-APP | R-25232 | CG-ALL-4602 | 3, 3.1 | Flyway file V4005_1__role_conflict_seed.sql is not in the V0001..Vnnnn form | The V4005_1 name is not in the supplied story text, so there is no old text to edit. Next free Flyway number is not in the sources; no number invented. |
| RWB-P4-AD006-APP | R-05465 | DOR-RWB-P4-AD006-APP-14 | 14 | Definition of Ready item 14 Epic design: Fail | Story v2 has no DoR-14 row in section 14 (only the screens table). No signed epic design record in the sources; searched story, 22 and 23 folders. Sign-off not invented. |
| RWB-P4-AD006-CON | R-05472 | DOR-RWB-P4-AD006-CON-14 |  | Definition of Ready item 14 Epic design: Fail | Definition of Ready row not in chunk, so no edit possible. No signed epic design record in sources (searched per prior notes). Not specified in the source documents (DOR-RWB-P4-AD006-CON-14). |
| RWB-P4-AD006-CON | R-05474 | DOR-RWB-P4-AD006-CON-17 |  | Definition of Ready item 17 Dependencies: Fail | Definition of Ready row and section 13 not in chunk, so the RWB-P4-E1019-APP dependency cannot be written. Needs those parts re-sent with the chunk. |
| RWB-P4-AD006-DB | R-16425 | DOR-RWB-P4-AD006-DB-15 | find it | Definition of Ready item 15 INVEST: Partial | The INVEST Small row is not in the supplied chunk, so no exact old text exists. 'Fits two weeks' is not in the sources. Grep of .md files found only generic INVEST text. |
| RWB-P4-AD006-DB | R-25241 | CG-ALL-4643 | 3, 3.1 | Flyway file V4003_1__break_glass_grant.sql is not in the V0001..Vnnnn form | Next Flyway number for rwb-access is not in the sources. Admin Stories v4 line 5504 gives V4003_1 only as an example name. Line 279 is not in the chunk. |
| RWB-P4-AD006-DB | R-30789 | NEWAC-RWB-P4-AD006-DB-AC8 | 8 | AC8: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 and section 16 text is not in the chunk, so the new AC8 cannot be anchored. Proposed test is Not specified in the source documents (NEWAC-RWB-P4-AD006-DB-AC8). |
| RWB-P4-AD007-APP | R-05483 | DOR-RWB-P4-AD007-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off in source docs. Grep found hits only in _work/msr scratch files. Sign-off cannot be written without inventing it. |
| RWB-P4-AD007-APP | R-16433 | DOR-RWB-P4-AD007-APP-11 |  | Definition of Ready item 11 Guardrails: Partial | Chunk gives no P2 field name or data-section text, so no exact old text to edit. Grep found no source naming the field. Needs the story data section. |
| RWB-P4-AD007-CON | R-05489 | DOR-RWB-P4-AD007-CON-14 | 14 | Definition of Ready item 14 Epic design: Fail | Section 14 text is not in this chunk, so no anchored edit is possible. Grep of the sources (excluding folder 17) found no epic design sign-off for AD007-CON. |
| RWB-P4-AD008-APP | R-25253 | CG-ALL-4680 | 15 | SCR-41 has no empty, loading, error, no access state in the story | SCR-41 is P3's and not in this story (R-16449); its states are not written here. The row is reverted. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (53)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07378 | RWB-P4-AD001-APP | CG-ALL-4509 | 12.1 | Publish GET /api/recovery/access/v1/admin/role-mappings under base /api/recovery/access/v1 through RWB-P4-AD001-CON. |
| CDC-07379 | RWB-P4-AD001-APP | CG-ALL-4510 | 12.1 | Publish POST /api/recovery/access/v1/admin/role-mappings under base /api/recovery/access/v1 through RWB-P4-AD001-CON. |
| CDC-07380 | RWB-P4-AD001-APP | CG-ALL-4511 | 12.1 | Publish GET /api/recovery/access/v1/admin/role-mapping-versions/{versionId} under base /api/recovery/access/v1 through RWB-P4-AD001-CON. |
| CDC-07381 | RWB-P4-AD001-APP | CG-ALL-4512 |  | Keep the roleClass enum: LOV-ROLE-CLASS is a closed list (Reference Data v5 Lists). No story change. |
| CDC-07382 | RWB-P4-AD001-APP | CG-ALL-4513 |  | Keep the defaultScope enum: LOV-SCOPE is a closed list (Reference Data v5 Lists). No story change. |
| CDC-07387 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-8 | 12 | Add GET and POST /api/recovery/access/v1/admin/role-mappings and GET /api/recovery/access/v1/admin/role-mapping-versions/{versionId}; hold roleClass as a reference to LOV-ROLE-CLASS, not a closed enum; resolve the 2 further listed mismatches. |
| CDC-07394 | RWB-P4-AD001-CON | CG-ALL-4520 | 12.1 | Add path /api/recovery/access/v1/admin/role-mappings with the GET operation as declared in RWB-P4-AD001-CON section 12.1 |
| CDC-07395 | RWB-P4-AD001-CON | CG-ALL-4521 | 12.1 | Add path /api/recovery/access/v1/admin/role-mappings with the POST operation as declared in RWB-P4-AD001-CON section 12.1 |
| CDC-07396 | RWB-P4-AD001-CON | CG-ALL-4522 | 12.1 | Add path /api/recovery/access/v1/admin/role-mapping-versions/{versionId} with the GET operation as declared in RWB-P4-AD001-CON section 12.1 |
| CDC-07413 | RWB-P4-AD002-APP | DOR-RWB-P4-AD002-APP-8 | 12.1 | Add the paths GET /api/recovery/access/v1/admin/permission-matrix, POST /api/recovery/access/v1/admin/permission-matrix-loads, GET /api/recovery/access/v1/admin/permission-matrix-versions/{matrixVersion}, GET /api/recovery/access/v1/admin/permission-matrix-versions, and the two further paths the detcheck names. |
| CDC-07433 | RWB-P4-AD002-CON | CG-ALL-4543 | 12.1 | Publish POST /api/recovery/access/v1/admin/permission-matrix-loads with the documented shape, errors and Platform administration C right. |
| CDC-07434 | RWB-P4-AD002-CON | CG-ALL-4544 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix with the documented query, shape, errors and Platform administration R right. |
| CDC-07435 | RWB-P4-AD002-CON | CG-ALL-4545 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix-versions/{matrixVersion} with the documented shape, errors and Platform administration R right. |
| CDC-07436 | RWB-P4-AD002-CON | CG-ALL-4546 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix-versions with the documented query, shape, errors and Platform administration R right. |
| CDC-07437 | RWB-P4-AD002-CON | CG-ALL-4547 | 8 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data without a code change. |
| CDC-07438 | RWB-P4-AD002-CON | CG-ALL-4548 | 8 | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data without a code change. |
| CDC-07440 | RWB-P4-AD002-CON | DOR-RWB-P4-AD002-CON-8 | 12.1 | Add POST /admin/permission-matrix-loads with the Idempotency-Key header, GET /admin/permission-matrix, GET /admin/permission-matrix-versions and GET /admin/permission-matrix-versions/{matrixVersion}, as §12.1 declares. |
| CDC-07447 | RWB-P4-AD003-APP | CG-ALL-4558 | 12.1 | Add path GET /api/recovery/access/v1/admin/role-scopes, published through RWB-P4-AD003-CON |
| CDC-07448 | RWB-P4-AD003-APP | CG-ALL-4559 | 12.1 | Add path PATCH /api/recovery/access/v1/admin/role-scopes/{roleCode}, published through RWB-P4-AD003-CON |
| CDC-07449 | RWB-P4-AD003-APP | CG-ALL-4561 | 12.1 | Remove the fixed enum on defaultScope so its values come from LOV-SCOPE in Reference Data v5 Lists |
| CDC-07453 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-8 | 4, 12.1 | Add paths GET /admin/role-scopes and PATCH /admin/role-scopes/{roleCode}; type defaultScope as a reference to LOV-SCOPE, not a closed enum |
| CDC-07464 | RWB-P4-AD003-CON | CG-ALL-4566 | 12.1 | Publish GET /api/recovery/access/v1/admin/role-scopes with query scope, roleClass, page, size (default 50, max 200) and the RoleScopePage response, as RWB-P4-AD003-CON §12.1 states. |
| CDC-07465 | RWB-P4-AD003-CON | CG-ALL-4567 | 12.1 | Publish PATCH /api/recovery/access/v1/admin/role-scopes/{roleCode} with the RoleScopeChange request, Idempotency-Key and If-Match headers, as RWB-P4-AD003-CON §12.1 states. |
| CDC-07466 | RWB-P4-AD003-CON | CG-ALL-4568 | 12.1 | Remove the fixed enum on roleClass so LOV-ROLE-CLASS values are accepted as data, as the story reads them. |
| CDC-07467 | RWB-P4-AD003-CON | DOR-RWB-P4-AD003-CON-8 | 12 | Add GET /admin/role-scopes and PATCH /admin/role-scopes/{roleCode}; declare roleClass and defaultScope against LOV-ROLE-CLASS and LOV-SCOPE, not closed enums; add Idempotency-Key to PATCH. |
| CDC-07474 | RWB-P4-AD004-APP | CG-ALL-4575 | 12.1 | Publish GET /api/recovery/access/v1/admin/masking-profiles in rwb-access.yaml through RWB-P4-AD004-CON. |
| CDC-07475 | RWB-P4-AD004-APP | CG-ALL-4576 | 12.1 | Publish POST /api/recovery/access/v1/admin/masking-profile-versions in rwb-access.yaml through RWB-P4-AD004-CON. |
| CDC-07476 | RWB-P4-AD004-APP | CG-ALL-4577 | 12.1 | Publish POST /api/recovery/access/v1/admin/masking-profiles/{roleCode}/unmask in rwb-access.yaml through RWB-P4-AD004-CON. |
| CDC-07480 | RWB-P4-AD004-APP | DOR-RWB-P4-AD004-APP-8 | 12.1 | Publish the three missing paths (GET admin/masking-profiles, POST admin/masking-profile-versions, POST admin/masking-profiles/{roleCode}/unmask) in rwb-access.yaml. |
| CDC-07484 | RWB-P4-AD004-CON | CG-ALL-4584 | 12.1 | Add path /admin/masking-profiles (GET; query roleCode, fieldId, validOn, page, size; answer MaskingProfilePage) under base /api/recovery/access/v1 |
| CDC-07485 | RWB-P4-AD004-CON | CG-ALL-4585 | 12.1 | Add path /admin/masking-profile-versions (POST; MaskingProfileVersion in; Idempotency-Key) under base /api/recovery/access/v1 |
| CDC-07486 | RWB-P4-AD004-CON | CG-ALL-4586 | 12.1 | Add path /admin/masking-profiles/{roleCode}/unmask (POST; UnmaskRequest in; Idempotency-Key) under base /api/recovery/access/v1 |
| CDC-07488 | RWB-P4-AD004-CON | DOR-RWB-P4-AD004-CON-8 | 12.1 | Publish the three paths with Idempotency-Key on both POST operations, as §12.1 states; the error-ID gap is CG-ALL-4587 |
| CDC-07492 | RWB-P4-AD005-APP | CG-ALL-4595 | 12.1 | Publish POST /api/recovery/access/v1/authorise/separation-of-duty through RWB-P4-AD005-CON, or remove it |
| CDC-07493 | RWB-P4-AD005-APP | CG-ALL-4596 | 12.1 | Publish GET /api/recovery/access/v1/admin/role-conflicts through RWB-P4-AD005-CON, or remove it |
| CDC-07494 | RWB-P4-AD005-APP | CG-ALL-4597 | 12.1 | Publish GET /api/recovery/access/v1/admin/role-conflict-versions/{versionId} through RWB-P4-AD005-CON, or remove it |
| CDC-07497 | RWB-P4-AD005-APP | DOR-RWB-P4-AD005-APP-8 | 12.1 | Publish the three missing operations listed in CG-ALL-4595 to CG-ALL-4597 |
| CDC-07506 | RWB-P4-AD005-CON | CG-ALL-4606 | 12.1 | Publish POST /authorise/separation-of-duty with SodCheckRequest and SodCheckResult, or remove the operation from the story |
| CDC-07507 | RWB-P4-AD005-CON | CG-ALL-4607 | 12.1 | Publish GET /admin/role-conflicts with its query and RoleConflict shape, or remove the operation from the story |
| CDC-07508 | RWB-P4-AD005-CON | CG-ALL-4608 | 12.1 | Publish GET /admin/role-conflict-versions/{versionId} with its RoleConflictVersion response, or remove the operation from the story |
| CDC-07517 | RWB-P4-AD006-APP | CG-ALL-4617 | 12.1 | Publish POST /api/recovery/access/v1/admin/break-glass-grants in rwb-access.yaml through RWB-P4-AD006-CON |
| CDC-07518 | RWB-P4-AD006-APP | CG-ALL-4618 | 12.1 | Publish POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end in rwb-access.yaml through RWB-P4-AD006-CON |
| CDC-07519 | RWB-P4-AD006-APP | CG-ALL-4619 | 12.1 | Publish GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} in rwb-access.yaml through RWB-P4-AD006-CON |
| CDC-07520 | RWB-P4-AD006-APP | CG-ALL-4620 |  | Remove the closed enum on defaultScope so LOV-SCOPE values are accepted as data, as the Reference Data v5 list defines them |
| CDC-07523 | RWB-P4-AD006-APP | DOR-RWB-P4-AD006-APP-8 | find it | Add POST /api/recovery/access/v1/admin/break-glass-grants, POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end and GET /api/recovery/access/v1/admin/break-glass-grants/{grantId}; take defaultScope as LOV-SCOPE data, not a closed enum |
| CDC-07530 | RWB-P4-AD006-CON | CG-ALL-4625 | 12.1 | Add path POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end with right C and Idempotency-Key as declared in RWB-P4-AD006-CON §12.1 |
| CDC-07531 | RWB-P4-AD006-CON | CG-ALL-4626 | 12.1 | Add path GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} with right R as declared in RWB-P4-AD006-CON §12.1 |
| CDC-07532 | RWB-P4-AD006-CON | DOR-RWB-P4-AD006-CON-8 | 12.1 | Yaml path gaps remain under CG-ALL-4625 and CG-ALL-4626. |
| CDC-07558 | RWB-P4-AD007-APP | CG-ALL-4647 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story. Story unchanged. |
| CDC-07560 | RWB-P4-AD007-APP | DOR-RWB-P4-AD007-APP-8 | 12.2, 12.3 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml (CG-ALL-4647). The event-type part is resolved in this story. |
| CDC-07567 | RWB-P4-AD007-CON | CG-ALL-4659 | 12.1 | Publish GET /api/recovery/access/v1/admin/access-log/export in rwb-access.yaml as declared in section 12.1 of this story. |
| CDC-07568 | RWB-P4-AD007-CON | CG-ALL-4660 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml so the consumed declaration in 12.2 resolves to a published operation. |
| CDC-07578 | RWB-P4-AD008-APP | CG-ALL-4670 | 12.2 | Publish POST /api/recovery/access/v1/authorise through RWB-P4-E1037-CON, or the story consumes a published operation (provider ruling). |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07398 | RWB-P4-AD001-CON | CG-ALL-4524 | 14 | Add a new message ID for 'The ACE group reference cannot be read', separate from MSG-GEN-006 (System of record unavailable, R-UNI-33). |
| CDC-07414 | RWB-P4-AD002-APP | CG-ALL-4535 | 4 | Business analyst adds a new message ID for LOV-CAPABILITY unavailable through DP-07; the story then cites it in §4 and §14 in place of MSG-GEN-006. |
| CDC-07454 | RWB-P4-AD003-APP | CG-ALL-4560 | 4, 12.1 | Business analyst assigns a message ID for 404 unknown or inactive role and for 409 stale If-Match or repeated key answered differently; MSG-GEN-006 does not fit a store failure. |
| CDC-07468 | RWB-P4-AD003-CON | CG-ALL-4571 | 14 | Add a new message ID for an access owner not answering inside the 2 s budget, with its own text; RWB-P4-AD003-CON §14 then cites it. No ID exists yet. |
| CDC-07470 | RWB-P4-AD003-CON | DOR-RWB-P4-AD003-CON-9 | 14 | Add a new message ID for the 2 s budget case so MSG-GEN-006 keeps its standard meaning; §14 then cites it. |
| CDC-07499 | RWB-P4-AD005-APP | CG-ALL-4599 | 14 | Add a new message ID for the conflicting-pair refusal at the conflict version in force, for this story's use; the standard keeps MSG-P4-006 for the role pair held in one session. |
| CDC-07500 | RWB-P4-AD005-APP | CG-ALL-4600 | 14 | Add a new message ID for the ACE group reference that cannot be read, for this story's use; the standard keeps MSG-GEN-006 for system of record unavailable. |
| CDC-07502 | RWB-P4-AD005-APP | DOR-RWB-P4-AD005-APP-9 | 14 | Confirm the standard's meaning of MSG-P4-006 (role conflict refusal) and MSG-GEN-006 (ACE group reference unreadable), or align the story to the standard's entries. |
| CDC-07510 | RWB-P4-AD005-CON | CG-ALL-4610 | 4, 14 | Add a new message ID for the role-pair refusal; the story then cites it in sections 4 and 14 |
| CDC-07511 | RWB-P4-AD005-CON | CG-ALL-4611 | 4, 14 | Add a new message ID for 'The ACE group reference cannot be read' so MSG-GEN-006 keeps its standard meaning; the story then cites the new ID in section 14. |
| CDC-07513 | RWB-P4-AD005-CON | DOR-RWB-P4-AD005-CON-9 | 14 | Confirm the meaning of MSG-P4-006 for a session refusal or assign a new ID; add the new ID for the ACE group reference (see CG-ALL-4611). |
| CDC-07562 | RWB-P4-AD007-APP | CG-ALL-4649 | 4, 14 | Add a new message ID for 'The caller has no session' with the text 'Your session has ended. Sign in again to continue.'; the story then cites it. |
| CDC-07571 | RWB-P4-AD007-CON | CG-ALL-4662 | 4, 14 | Add a new message ID for the No session text (Your session has ended. Sign in again to continue.) so the story can cite it; MSG-P4-001 keeps its standard meaning. |
| CDC-07575 | RWB-P4-AD007-CON | DOR-RWB-P4-AD007-CON-9 |  | Align the standard's meaning of MSG-P4-001 with this story's use as no session, or record the difference. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (12)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07524 | RWB-P4-AD006-APP | CG-ALL-4616 | 11 | Add entity break_glass_grant and its fields as recorded by RWB-P4-AD006-DB |
| CDC-07525 | RWB-P4-AD006-APP | DOR-RWB-P4-AD006-APP-7 | 11 | Add entity break_glass_grant and its fields as recorded by RWB-P4-AD006-DB |
| CDC-07535 | RWB-P4-AD006-CON | DOR-RWB-P4-AD006-CON-7 | 11 | Register break_glass_grant as an entity and assign BR Field IDs to the grant columns. |
| CDC-07543 | RWB-P4-AD006-DB | CG-ALL-4635 | 2 | Record flyway_schema_history as a platform-owned physical object (V0001 baseline, RWB-PLT-E1044-CON) or add it as a dictionary entity. |
| CDC-07544 | RWB-P4-AD006-DB | CG-ALL-4636 | 12.7, 13 | Add break_glass_marker as a break_glass_grant column (boolean, NOT NULL, check true) to LDM v9 Fields or Data Classification v5 Fields. |
| CDC-07545 | RWB-P4-AD006-DB | CG-ALL-4637 | 13 | Add incident_reference (varchar(20), NOT NULL) as a break_glass_grant field to LDM v9 Fields or Data Classification v5 Fields. |
| CDC-07546 | RWB-P4-AD006-DB | CG-ALL-4638 | 13 | Add iam_request_id (varchar(40), NOT NULL) as a break_glass_grant field to LDM v9 Fields or Data Classification v5 Fields. |
| CDC-07547 | RWB-P4-AD006-DB | CG-ALL-4639 | 13 | Add right_code (varchar(5), NOT NULL) as a break_glass_grant field to LDM v9 Fields or Data Classification v5 Fields. |
| CDC-07548 | RWB-P4-AD006-DB | CG-ALL-4640 | 13 | Add scope_code (varchar(8), NOT NULL) as a break_glass_grant field to LDM v9 Fields or Data Classification v5 Fields. |
| CDC-07552 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-7 | 11 | Add break_glass_grant and its columns from the section 13 table definition as entities and fields; story side now states the objects are owned by this story. |
| CDC-07583 | RWB-P4-AD008-APP | CG-ALL-4666 | 1, 4, 7, 8, 10, 11, 12.7, 13, 17 | Record access_review and access_review_item as new rwb_access tables created by the RWB-P4-AD008-APP migration, with their field IDs. |
| CDC-07593 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-7 | 11 | Register DF-REF-039, and add access_review and access_review_item with their fields including opened_on and closes_on at the next dictionary version. |

### Epic design record (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07383 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-14 | not located in chunk | Record the signed epic design sign-off for RWB-P4-AD001-APP. |
| CDC-07397 | RWB-P4-AD001-CON | DOR-RWB-P4-AD001-CON-14 | none | Record the signed epic design sign-off covering RWB-P4-AD001-CON; no sign-off exists in the source documents to write here. |
| CDC-07410 | RWB-P4-AD002-APP | DOR-RWB-P4-AD002-APP-14 | header | Confirm and record the signed epic design sign-off, then reference it in the story |
| CDC-07439 | RWB-P4-AD002-CON | DOR-RWB-P4-AD002-CON-14 | header | Record the signed epic design sign-off for this story in the epic design record. |
| CDC-07450 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-14 | header | Confirm the signed epic design sign-off and record it there; the story shows Not specified in the source documents (DOR-RWB-P4-AD003-APP-14) until then. |
| CDC-07477 | RWB-P4-AD004-APP | DOR-RWB-P4-AD004-APP-14 | header | Header row records the value as not specified; the signed epic design record is needed from another document. |
| CDC-07487 | RWB-P4-AD004-CON | DOR-RWB-P4-AD004-CON-14 | Header table | Record the signed epic design sign-off for RWB-SVC-P4 (business epic EP08) |
| CDC-07509 | RWB-P4-AD005-CON | DOR-RWB-P4-AD005-CON-14 |  | Record the signed epic design sign-off for EP08 so this story can cite it |
| CDC-07540 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-14 | find it | Record the signed epic design sign-off for EP08 in the epic design record. |
| CDC-07580 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-14 | Header | Confirm and record the signed epic design sign-off for EP08 and check it against this story. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07388 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-7 | 11 | Add field ID DF-REF-039 (role.entra_group) to the LDM v9 field list. |
| CDC-07457 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-7 | 11 | Confirm DF-REF-039 (role.entra_group) in LDM v9 or correct its ID here |
| CDC-07498 | RWB-P4-AD005-APP | CG-ALL-4594 | 12.7 | Record `access_log` as a table of `rwb_access` (the access log of RWB-P4-AD007-APP and RWB-P4-E1039-APP) or give its dictionary name. |
| CDC-07501 | RWB-P4-AD005-APP | DOR-RWB-P4-AD005-APP-7 | 11 | Add field ID DF-REF-039 (role.entra_group) to the model; confirm access_log is an entity or field of rwb_access, or remove the name from the story's table list. |
| CDC-07533 | RWB-P4-AD006-CON | CG-ALL-4624 | 12.7 | Record break_glass_grant as the table of rwb_access in the owning document, or add the dictionary name used |
| CDC-07565 | RWB-P4-AD007-APP | DOR-RWB-P4-AD007-APP-7 | 11 | Confirm whether DF-REF-039 (role entra_group) exists; add it to LDM v9 or retire it from the section 11 row |
| CDC-07584 | RWB-P4-AD008-APP | CG-ALL-4667 | 4 | Record access_review and access_review_item in rwb_access as new tables created by RWB-P4-AD008-APP migration (GAP-0806), or use the dictionary name for each. |
| CDC-07585 | RWB-P4-AD008-APP | CG-ALL-4668 | 4 | Record opened_on as a field of access_review in rwb_access, created by this story's migration (GAP-0806), or use the dictionary name. |
| CDC-07586 | RWB-P4-AD008-APP | CG-ALL-4669 | 4 | Record closes_on as a field of access_review in rwb_access, created by this story's migration (GAP-0806), or use the dictionary name. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07399 | RWB-P4-AD001-CON | DOR-RWB-P4-AD001-CON-1 | 1 | Add the role 'tech lead' as a role code or role name so that section 1 of RWB-P4-AD001-CON resolves to a listed role. |
| CDC-07415 | RWB-P4-AD002-APP | DOR-RWB-P4-AD002-APP-1 | 1 | Provide a role code or role name for the application owner that §1 can cite, or confirm the role name it uses. |
| CDC-07441 | RWB-P4-AD002-CON | DOR-RWB-P4-AD002-CON-1 | 1 | Add the role 'tech lead' with its role code or name, or the story names the role code the document uses. |
| CDC-07455 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-1 | 1 | Add role 'application owner' (code or name) so the section 1 role resolves to a role in force |
| CDC-07534 | RWB-P4-AD006-CON | DOR-RWB-P4-AD006-CON-1 | 1 | Add 'tech lead' as a role name or code, or confirm the existing role code that section 1 should name. |
| CDC-07549 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-1 | 1 | Add role 'ACE database engineer' as a role name, or map it to an existing role code, in Users Roles and Permissions v5. |
| CDC-07572 | RWB-P4-AD007-CON | DOR-RWB-P4-AD007-CON-1 | 1 | Add tech lead as a role code or role name in Users Roles and Permissions v5, or the owner confirms the role that section 1 should name. |
| CDC-07591 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-1 | 1 | Add role name or code "role owner" used by section 1, or name the role code of the role that owns the review. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07481 | RWB-P4-AD004-APP | CG-ALL-4579 | 16 | Add rows TC-AD-004-06, TC-AD-004-07 and TC-AD-004-08 to Story test cases, with Given, When and Then copied from AC1, AC2 and AC3 in RWB-P4-AD004-APP section 7. |
| CDC-07489 | RWB-P4-AD004-CON | DOR-RWB-P4-AD004-CON-12 | 12.7, 16 | Register TC-AD-004-CON-01 to TC-AD-004-CON-08 with their Covers and Level; TC-07 is the new §12.7 boundary test and TC-08 the new AC7 test. |
| CDC-07491 | RWB-P4-AD004-CON | CG-ALL-4589 | 16 | Add rows TC-AD-004-CON-01 to TC-AD-004-CON-06 with Given, When and Then copied from the criteria they cover in section 7 of this story. |
| CDC-07563 | RWB-P4-AD007-APP | CG-ALL-4650 | 16 | Add rows for TC-AD-007-05 and TC-AD-007-06, with Given, When and Then copied from the criteria AC4 and AC5 they cover |
| CDC-07576 | RWB-P4-AD007-CON | CG-ALL-4663 | 16 | Add rows for TC-AD-007-CON-01 to -06 with Given, When and Then copied from AC1 to AC6, and TC-AD-007-CON-07 from AC7. |
| CDC-07590 | RWB-P4-AD008-APP | CG-ALL-4676 | 16 | Add rows TC-AD-008-05 and TC-AD-008-06 in the next Test Cases version, with Given, When and Then copied from AC3, AC5 and their BR references. |
| CDC-07592 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-12 | 12, 12.7, 16, 18 | Section 16 now has contract test TC-AD-008-14, boundary test TC-AD-008-08 for section 12.7 tables. Test Cases v8 and RTM v7 sides are outside this story. |

### OTHER:TSD P4 T6.1 RBAC matrix (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07416 | RWB-P4-AD002-APP | GAP-0942 | find it | Add a Documents column and confirm RW-RESTRUCT and RW-CASEOWN CRU, RW-TEAMMGR R and RW-LEGAL CRUA, then publish in PM-2026.12 pack. |
| CDC-07418 | RWB-P4-AD002-APP | GAP-0900 | find it | Extend the matrix to the 14 LOV-CAPABILITY areas and publish the full matrix version with RWB-P4-AD002-APP. |
| CDC-07419 | RWB-P4-AD002-APP | GAP-0907 | find it | Add a Case record column for all roles and confirm CASE_RECORD letters and default scopes for RW-CASEOWN, RW-RESTRUCT, RW-AUDIT and RW-REFADM. |
| CDC-07421 | RWB-P4-AD002-APP | GAP-0923 | find it | Add Case record and Treatment and offer columns and publish the full 14-area matrix version with RWB-P4-AD002-APP. |
| CDC-07422 | RWB-P4-AD002-APP | GAP-0926 | find it | Publish letters for all 14 capability areas per role with default scope, as a new T6.1 version loaded through RWB-P4-AD002-APP. |
| CDC-07423 | RWB-P4-AD002-APP | GAP-0945 | find it | Add a Litigation column for the roles the legacy table names and confirm the C and R letters before the pack goes in force. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07417 | RWB-P4-AD002-APP | GAP-1564 | find it | Confirm that load, approve, verify and rollback stay with rwb-case and rwb-access publishes the authorise, masking and DoA lookup answers. |
| CDC-07459 | RWB-P4-AD003-APP | GAP-0791 | find it | Add rows for GET and PATCH /admin/role-scopes on /api/recovery/access/v1 with Platform administration R and C, and the predicate of the authorise answer |
| CDC-07460 | RWB-P4-AD003-APP | GAP-0792 | find it | Fix the scope read and change paths, the predicate descriptor, the 404 refusal entry and AccessPolicyChanged kind SCOPE |
| CDC-07482 | RWB-P4-AD004-APP | GAP-2267 | find it | Add the three masking-profile operations at version 1 to the API specification index and add masking-profile rows to the ownership map. |
| CDC-07490 | RWB-P4-AD004-CON | GAP-2267 | 1 | Add the three masking-profile operations to the API specification index at the next revision and add their rows to the ownership map; the profile is this story at version 1. |
| CDC-07514 | RWB-P4-AD005-CON | GAP-0796 | find it | Add rows for POST /authorise/separation-of-duty, GET /admin/role-conflicts and GET /admin/role-conflict-versions/{versionId} on /api/recovery/access/v1, owner rwb-access. |

### RWB-P4-AD002-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07405 | RWB-P4-AD002-APP | CG-ALL-4529 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix in rwb-access.yaml through the CON story |
| CDC-07406 | RWB-P4-AD002-APP | CG-ALL-4530 | 12.1 | Publish POST /api/recovery/access/v1/admin/permission-matrix-loads in rwb-access.yaml through the CON story |
| CDC-07407 | RWB-P4-AD002-APP | CG-ALL-4531 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix-versions/{matrixVersion} in rwb-access.yaml through the CON story |
| CDC-07408 | RWB-P4-AD002-APP | CG-ALL-4532 | 12.1 | Publish GET /api/recovery/access/v1/admin/permission-matrix-versions in rwb-access.yaml through the CON story |
| CDC-07409 | RWB-P4-AD002-APP | CG-ALL-4533 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07561 | RWB-P4-AD007-APP | CG-ALL-4646 | 12.2, 12.8 | Add list LOV-EVENT to Reference Data v5 Lists. Story unchanged. |
| CDC-07564 | RWB-P4-AD007-APP | DOR-RWB-P4-AD007-APP-20 | find it | Add LOV-EVENT to Reference Data v5 so the story's reference list resolves |
| CDC-07570 | RWB-P4-AD007-CON | CG-ALL-4658 | 12.2 | Add the list LOV-EVENT to Reference Data v5 Lists with the values the access-log event filter uses. |
| CDC-07574 | RWB-P4-AD007-CON | DOR-RWB-P4-AD007-CON-20 |  | Add the list LOV-EVENT, which the query parameter event of AC2 reads. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07566 | RWB-P4-AD007-APP | CG-ALL-4651 | 18 | Align the test lists of the requirements in section 18 (REQ-ACA-006, REQ-ACA-007 and the others) with RWB-P4-AD007-APP section 18 in its next version. |
| CDC-07573 | RWB-P4-AD007-CON | DOR-RWB-P4-AD007-CON-12 | 7, 12.7, 16, 18 | Align the test lists of section 18 with section 16, which now runs TC-AD-007-CON-01 to -07 with AC7 covering the owned-table boundary. |
| CDC-07577 | RWB-P4-AD007-CON | CG-ALL-4664 | 18 | Align the test lists of the three differing requirements in RTM v7 with section 18 of RWB-P4-AD007-CON, which already traces the tests in section 16. |
| CDC-07598 | RWB-P4-AD008-APP | CG-ALL-4677 | 18 | Align the REQ-ACA-002 and REQ-ACA-011 test lists in the RTM to section 18 of RWB-P4-AD008-APP in its next version |

### RWB-P4-AD002-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07411 | RWB-P4-AD002-APP | DOR-RWB-P4-AD002-APP-21 | header | Build RWB-P4-AD002-CON to Done with the contract published |
| CDC-07427 | RWB-P4-AD002-APP | GAP-0790 | 3 | Fix four operations and four schemas, one problem envelope with seven message IDs and six fakes, the event rwb.access.AccessPolicyChanged.v1 with change kind MATRIX on rwb.access.events.v1; deprecation and retention with the platform contract owner. |
| CDC-07428 | RWB-P4-AD002-APP | GAP-2264 | 3 | Fix the four schemas and their paths and rights, VALIDATED as end state of a load, the MATRIX event after commit, an additive-only change rule within major version 1, and a deprecation window and fake retention. |

### RWB-P4-AD005-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07495 | RWB-P4-AD005-APP | DOR-RWB-P4-AD005-APP-21 | header | Set build status to Done once the separation-of-duty contract is published |
| CDC-07496 | RWB-P4-AD005-APP | DOR-RWB-P4-AD005-APP-22 | 12.8 | Publish the separation-of-duty contract fake library version and record it |
| CDC-07503 | RWB-P4-AD005-APP | GAP-0796 | 3 | Publish POST /authorise/separation-of-duty, GET /admin/role-conflicts and GET /admin/role-conflict-versions/{versionId} on /api/recovery/access/v1; name conflictVersion in the session answer; grant Platform administration R to both reads; record refusal as decision; name the RWB-P4-E1037-CON load path as the new-version route. |

### RWB-P4-AD006-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07521 | RWB-P4-AD006-APP | DOR-RWB-P4-AD006-APP-21 |  | Build status moves from Not started to Done once the contract is published |
| CDC-07522 | RWB-P4-AD006-APP | DOR-RWB-P4-AD006-APP-22 |  | Publish the contract fake library and record its published version |
| CDC-07541 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-21 | find it | Build RWB-P4-AD006-CON to Done with the contract published. |

### OTHER:_work/msr/wp/B-P4-02.md and _work/msr/wp/B2-P4-005.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07529 | RWB-P4-AD006-APP | GAP-2270 |  | Keep B-P4-02 as the single Work Package for RWB-AD-006 on rwb-access with RWB-AD-002 to AD-005; withdraw B2-P4-005 with its edit log row; the six delivered artefacts stand |
| CDC-07539 | RWB-P4-AD006-CON | GAP-2270 | find it | Remove legacy RWB-AD-006 and its three slices from the B-P4-02 fanout; keep B2-P4-005 as the sole Work Package for the key and write its edit log row; withdraw the duplicate title. Delivered artefacts stand. |
| CDC-07557 | RWB-P4-AD006-DB | GAP-2270 | 4 | Keep one Work Package for legacy RWB-AD-006 and withdraw the other with its edit log row; B-P4-02 keeps RWB-AD-002 to AD-005. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07579 | RWB-P4-AD008-APP | CG-ALL-4673 |  | Catalogue the review workflow that the story names AccessReviewWorkflow in 12.5, or give its catalogued name so the story can use it. |
| CDC-07588 | RWB-P4-AD008-APP | CG-ALL-4674 | 12.5 | Add activity BuildReviewList to the Activities sheet on task queue rwb-access, or map it to a catalogued activity. |
| CDC-07589 | RWB-P4-AD008-APP | CG-ALL-4675 | 12.5 | Add activity RequestRemoval to the Activities sheet on task queue rwb-access, or map it to a catalogued activity. |

### API:(service not named) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07389 | RWB-P4-AD001-APP | GAP-1568 | find it | Publish authorise, /me/permissions, /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary; state in TSD P4 T3.1 how a group resolves to a role and what happens to a session when a role is retired. |
| CDC-07458 | RWB-P4-AD003-APP | GAP-1568 | find it | Publish the four rwb-access operations with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary |

### OTHER:Screen Specifications v1 (SCR-43) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07456 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-10 | 15 | Empty, loading, error and no-access states in the SCR-43 row marked Not specified in the source documents (CG-ALL-4563) |
| CDC-07461 | RWB-P4-AD003-APP | CG-ALL-4563 | 15 | Add empty, loading, error and no access states for SCR-43 |

### OTHER:plan generator (split_plan.json and B-P4-02 fanout) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07462 | RWB-P4-AD003-APP | GAP-2265 | find it | Keep one Work Package per AD003 story slice, remove the duplicate fanout and number citations once |
| CDC-07463 | RWB-P4-AD003-APP | GAP-2269 | find it | Keep one Work Package per AD005 story slice, remove the duplicate fanout and settle the B2 rewrite rule |

### OTHER:Contract fake library (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07479 | RWB-P4-AD004-APP | DOR-RWB-P4-AD004-APP-22 | 12.8 | Publish contract fakes for rwb-case and rwb-source-data and record their library version. |
| CDC-07542 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-22 | find it | Publish a contract fake library version and record its version. |

### parameter-catalog.csv (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07526 | RWB-P4-AD006-APP | GAP-0797 | 3 | Record the read right R beside the activation right C in T6.1; seed the window code and reason-floor code in the parameter catalogue; confirm the incident register contract with the security administrator |
| CDC-07555 | RWB-P4-AD006-DB | GAP-0797 | find it | Seed the window-hours and reason-floor parameter codes; record the read right beside the activation right in TSD P4 v3 T6.1; confirm the incident register with the security administrator before wave 4. |

### RWB-P2-E1007-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07599 | RWB-P4-AD008-APP | GAP-0981 | 3 | Register one OUTBOUND interface row for the access-review file with interface ID, file pattern, data product, owner role and alert role; publish layout and recipient with RWB-P4-AD008-APP |
| CDC-07600 | RWB-P4-AD008-APP | GAP-1572 | 3 | Register the access-review interface row; publish file layout and review-date convention; agree file-level delivery matching with the rwb-integration contract owner |

### RWB-P4-AD001-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07384 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-16 | not located in chunk | Squad sizes the story at refinement and records the size. |

### RWB-P4-AD001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07385 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-21 | not located in chunk | Complete the build and mark the contract story Done so the contract is published before this story starts. |

### OTHER:rwb-case contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07386 | RWB-P4-AD001-APP | DOR-RWB-P4-AD001-APP-22 | 12.8 | Publish a contract fake for rwb-case, record its library version, and name it in section 12.8. |

### OTHER:TSD P4 v3 T3.1 and appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07390 | RWB-P4-AD001-APP | GAP-0787 | find it | Add the mapping version label and valid-from and valid-to dates to the role rows; fix the three mapping operations under /api/recovery/access/v1/admin with their rights; read the environment code as a parameter. |

### OTHER:TSD P4 v3 appendix T-A and T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07391 | RWB-P4-AD001-APP | GAP-0788 | find it | Add the three mapping operations, their schemas and the problem envelope with the seven message IDs; declare rwb.access.AccessPolicyChanged.v1 with change kind MAPPING on rwb.access.events.v1. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07392 | RWB-P4-AD001-APP | GAP-2104 | find it | I16 reads roles through rwb-access; the group reference comes from the P1 rwb-source-data view recovery.v_ace_iam_group; sign-in and group-to-role stay with ACE Common. |

### OTHER:TSD P4 v3 T3.1, with TSD P3 and TSD S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07393 | RWB-P4-AD001-APP | GAP-1567 | find it | Drop lov_value and partner_user from TSD P4 T3.1; keep the lists of values in TSD P3 and the partner identity in TSD S9. |

### API:(service not named); OTHER:TSD P4 appendix T-A and T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07400 | RWB-P4-AD001-CON | GAP-1568 | none | Publish the four operations with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary; state group-to-role resolution and retired-role session handling in T3.1. |

### OTHER:Login and library column set in the owning documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07401 | RWB-P4-AD001-CON | GAP-0777 | 11 | Login name is not specified in the source documents, so the story says so. Mapping rows stay in role.entra_group with TSD P4 v3 precedence; ACE facts via the P1 contract. The login and the library column set belong to other documents. |

### OTHER:TSD P4 v3 T3.1 and appendix T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07402 | RWB-P4-AD001-CON | GAP-0787 | 11 | Add mapping version label, valid-from and valid-to columns to the role rows of rwb_access by this key's migration; add the three mapping operations under /api/recovery/access/v1/admin with Platform administration R for reads and C for change. |

### OTHER:TSD P4 v3 T3.1 and appendix T-A.1 (masking_rule and the masking-profile contract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07403 | RWB-P4-AD001-CON | GAP-0794 | 7 | Add status, view and column columns to masking_rule; publish the masking-profile path and the four schemas with roleCode, fieldId, viewName, columnName, unmasked, maskingVersion, validFrom and validTo; page default 50, maximum 200; unmask record with no clear value. |

### OTHER:TSD P4 v3 T3.1 and T3.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07404 | RWB-P4-AD001-CON | GAP-1567 | 7 | Drop lov_value (DF-REF-027 to 033) and partner_user (DF-REF-212 to 217) and the partner_user to partner relationship; keep the lists of values in TSD P3 and the partner identity in TSD S9. |

### RWB-P3-E1042-CON; RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07412 | RWB-P4-AD002-APP | DOR-RWB-P4-AD002-APP-22 | 12.8 | Publish the rwb-case contract fake library and record its version |

### RWB-P4-E1037-CON; RWB-P4-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07420 | RWB-P4-AD002-APP | GAP-0917 | find it | Freeze the authorise and doa-limits request and answer fields, and name the rwb-access login with the DP-02 platform DB story. |

### OTHER:TSD P4 v3 T6.1 (RBAC matrix) and the PM-2026.12 permission file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07424 | RWB-P4-AD002-APP | GAP-0948 | 3 | Add the JOB-10 runner service identity row with role class NON_HUMAN_ACTOR, scope ALL and its Litigation R; the role code is not in the sources. |

### OTHER:TSD P4 v3 T6.1 (RBAC matrix) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07425 | RWB-P4-AD002-APP | GAP-0949 | 3 | Add a Documents column carrying RW-FIELDCOL CR, RW-CASEOWN CRU, RW-RESTRUCT CRU, SY-OCR CRU and RW-PHONECOL R; the pack load carries the five rows. |

### RWB-P4-AD002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07426 | RWB-P4-AD002-APP | GAP-2324 | 3 | Extend the matrix with a Case record column for every role, publish the 14-area matrix as data, and fix the default scope of specialist roles with the security administrator. |

### OTHER:Technical Specification P4 v3 T3.1 and the approved role conflict list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07429 | RWB-P4-AD002-APP | GAP-1574 | 16 | Publish the full role conflict list with its version label and effective dates; add valid-from and valid-to to permission in TSD P4 T3.1 or state that the date lives on the load; confirm the role and permission row counts of the version in force. |

### OTHER:B-P4-02 and B2-P4-002 Work Packages; OTHER:plan generator checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07430 | RWB-P4-AD002-APP | GAP-2265 |  | Remove RWB-AD-003 from the B-P4-02 fanout or retire B2-P4-002 for this key; number CG-B-P4-02-AD003-1, -2 and ASM-B-P4-02-AD003-1 to -8 once; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:B-P4-02 and B2-P4-004 Work Packages; OTHER:plan generator (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07431 | RWB-P4-AD002-APP | GAP-2269 |  | Remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004; number CG-B-P4-02-AD005-1, -2 and ASM-B-P4-02-AD005-1 to -13 once; apply one settling rule across the B2 queue. |

### OTHER:B-P4-02 and B2-P4-005 Work Packages; OTHER:plan generator (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07432 | RWB-P4-AD002-APP | GAP-2270 |  | Keep one Work Package for legacy RWB-AD-006, closed by B-P4-02 or B2-P4-005; withdraw the other title and write its edit log row. |

### RWB-P3-E1042-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07442 | RWB-P4-AD002-CON | GAP-1564 | find it | Confirm that load, approve, verify and rollback of reference loads stay with rwb-case and that P4 validation rules run as part of that load; otherwise restore API-P4-005, 006, 009 and 010 to P4 in API Specification v4 and TSD P4 appendix T-A. |

### OTHER:Recovery Workbench TSD P4 (T3.1 permission and role_conflict tables) and the approved role conflict source (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07443 | RWB-P4-AD002-CON | GAP-1574 | find it | Publish the full approved role conflict list with its version label and effective dates; add valid-from and valid-to columns to the matrix version in T3.1 or state that the dates live on the load; confirm the role and permission row counts of the version in force. |

### OTHER:Work Package plan (B-P4-02 and B2-P4-002) and plan generator split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07444 | RWB-P4-AD002-CON | GAP-2265 | find it | Remove RWB-AD-003 from the B-P4-02 fanout or retire B2-P4-002 for this key; number CG-B-P4-02-AD003-1 to -2 and ASM-B-P4-02-AD003-1 to -8 once; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package plan (B-P4-02 and B2-P4-004) and plan generator split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07445 | RWB-P4-AD002-CON | GAP-2269 | find it | Remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004; number CG-B-P4-02-AD005-1 to -2 and ASM-B-P4-02-AD005-1 to -13 once; apply one settling rule across the B2 queue; add plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package plan (B-P4-02 and B2-P4-005) and plan generator split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07446 | RWB-P4-AD002-CON | GAP-2270 | find it | Keep one Work Package for legacy RWB-AD-006 (B-P4-02 or B2-P4-005), withdraw the other title with its edit log row written; keep the delivered six artefacts and citation set; add plan-uniqueness check to checks/run_all.py. |

### RWB-P4-AD003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07451 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-21 | header | Set build status from Not started to Done once the contract is published |

### OTHER:Contract fake library release record (not in the Recovery Workbench source set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07452 | RWB-P4-AD003-APP | DOR-RWB-P4-AD003-APP-22 | header | Record the published contract fake library version, or confirm none is published; the story shows Not specified in the source documents (DOR-RWB-P4-AD003-APP-22) until then. |

### OTHER:P3 screen specification (SCR-43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07469 | RWB-P4-AD003-CON | DOR-RWB-P4-AD003-CON-10 | 5 | Add empty, loading, error and no-access states to SCR-43 of P3. |

### API:(service not named); OTHER:TSD P4 v3 appendix T-A and T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07471 | RWB-P4-AD003-CON | GAP-1568 | 12 | Publish the four operations with request, answer, refusal and not-found schemas, version fields and masking marker vocabulary; state how a group resolves to a role row and what a retired role does to a session. |

### OTHER:Work Package plan of the run: B-P4-02.md and B2-P4-002.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07472 | RWB-P4-AD003-CON | GAP-2265 |  | Remove RWB-AD-003 from the B-P4-02 fanout or retire B2-P4-002 for this key; number CG-B-P4-02-AD003-1, -2 and ASM-B-P4-02-AD003-1 to -8 once; add a plan-uniqueness check to checks/run_all.py. |

### OTHER:Work Package plan of the run: B-P4-02.md and B2-P4-004.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07473 | RWB-P4-AD003-CON | GAP-2269 |  | Remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004; number CG-B-P4-02-AD005-1, -2 and ASM-B-P4-02-AD005-1 to -13 once; apply one settling rule to the B2 queue. |

### RWB-P4-AD004-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07478 | RWB-P4-AD004-APP | DOR-RWB-P4-AD004-APP-21 | header | Set RWB-P4-AD004-CON build status to Done once its contract is published. |

### API:(service not named); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07483 | RWB-P4-AD004-APP | GAP-0793 | find it | Add three masking-profile operations on /api/recovery/access/v1 with Reference data R and C rights, and the unmasked rule as the unmask right. |

### OTHER:TSD P4 v3 T3.1 and the role conflict list (reference data) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07504 | RWB-P4-AD005-APP | GAP-1574 | 11 | Publish the approved role conflict list with its version label and effective dates; add valid_from and valid_to to the permission table or state the date lives on the load; confirm the role and permission row counts of the version in force. |

### OTHER:Delivery plan: B-P4-02 and B2-P4-004 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07505 | RWB-P4-AD005-APP | GAP-2269 | 1 | Remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004 for this key; number CG-B-P4-02-AD005-1 and -2 and ASM-B-P4-02-AD005-1 to -13 once; apply one settling rule across the B2 queue. |

### OTHER:Recovery Workbench P3 screen specification (SCR-43) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07512 | RWB-P4-AD005-CON | DOR-RWB-P4-AD005-CON-10 | find it | Add empty, loading, error and no-access states for SCR-43, or record that none apply; this contract adds no screen. |

### OTHER:TSD P4 T3.1 and the approved role conflict list (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07515 | RWB-P4-AD005-CON | GAP-1574 | find it | Publish the approved role conflict list with its version label and effective dates; add matrix version effective-date columns to T3.1 or state the date lives on the load; confirm role and permission row counts of the version in force. |

### OTHER:Work Package plan: B-P4-02 and B2-P4-004 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07516 | RWB-P4-AD005-CON | GAP-2269 | find it | Keep one Work Package per story slice: remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004 for this key; number CG-B-P4-02-AD005-1 and -2 and ASM-B-P4-02-AD005-1 to -13 once; pick one settling rule for the B2 queue. |

### RWB-P4-AD006-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07527 | RWB-P4-AD006-APP | GAP-0798 | 12 | Add end and read rows and the BreakGlassActivation and BreakGlassGrant field lists to appendix T-A; freeze the three operations, two schemas and states ACTIVE and ENDED in the contract baseline; record the refusal status mapping |

### RWB-P4-AD006-DB; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07528 | RWB-P4-AD006-APP | GAP-0799 | 12 | Confirm break_glass_grant, its columns and one-active-grant constraint with the security administrator; set retention at DL26 with Compliance; assign BR Field IDs; record the login grant in the platform schema baseline |

### OTHER:TSD P4 v3 T6.1 and parameters catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07536 | RWB-P4-AD006-CON | GAP-0797 | find it | Record read right R beside activation right C in T6.1; seed the window and reason-floor parameter codes; confirm the incident register contract with the security administrator. |

### OTHER:TSD P4 v3 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07537 | RWB-P4-AD006-CON | GAP-0798 | find it | Add rows for POST /admin/break-glass-grants/{grantId}/end and GET /admin/break-glass-grants/{grantId} with rights C and R; freeze the BreakGlassActivation and BreakGlassGrant field lists. |

### OTHER:TSD P4 v4 T3.1 and the platform schema baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07538 | RWB-P4-AD006-CON | GAP-0799 | find it | Add the break_glass_grant table with its columns and one-active-grant constraint; set grant retention at DL26; record the login grant in the schema baseline. |

### OTHER:SCR-43 owning story (P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07550 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-10 | find it | Add the empty, loading, error and no-access states of SCR-43 to the owning P3 story; this DB story renders no screen. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07551 | RWB-P4-AD006-DB | DOR-RWB-P4-AD006-DB-11 | find it | Classify break_glass_grant fields actor_user_id, approver_user_id and reason as personal data or confirm none; the value is Not specified in the source documents (DOR-RWB-P4-AD006-DB-11). |

### parameter-catalog.csv; 01 Decisions and governance/Recovery Workbench Decision Log v11.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07553 | RWB-P4-AD006-DB | GAP-1571 | find it | Answer DL38 with the break-glass maximum duration, reason bounds, review window and review role, held as versioned parameters; keep 4 hours and 20 to 1000 as placeholders until answered. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07554 | RWB-P4-AD006-DB | GAP-3194 | find it | Raise one ACE DB story per service lacking one (S2, S4, S5, S6, S7, P6, P8) for the 42-column drop or attach it to the creating APP story, and cite it on row 121. |

### OTHER:TSD P4 v3 appendix T-A and contract baseline (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07556 | RWB-P4-AD006-DB | GAP-0798 | find it | Freeze the end and read operations, the two schemas and the grant state vocabulary in the contract baseline and add their rows to appendix T-A before the wave 4 harness runs. |

### RWB-P4-AD007-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07559 | RWB-P4-AD007-APP | DOR-RWB-P4-AD007-APP-21 |  | Reach Done with the contract published; its build status is Not started today. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07569 | RWB-P4-AD007-CON | CG-ALL-4658 | 12.2 | Yaml: publish GET /admin/access-log/export and POST /api/recovery/access/v1/authorise (CG-ALL-4659, CG-ALL-4660). Event name already aligned to catalog EV-08 (CG-ALL-4661). |

### RWB-P4-AD008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07581 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-21 | Header | Build RWB-P4-AD008-CON to Done so its contract is published (build status is Not started). |

### OTHER:rwb-access API yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07582 | RWB-P4-AD008-APP | DOR-RWB-P4-AD008-APP-8 |  | API yaml: publish POST /api/recovery/access/v1/authorise for rwb-access. Kafka Catalog v1: align rwb.access.AccessPolicyChanged.v1 payload and the DecisionRecorded event type. Temporal Catalog v1: catalogue AccessReviewWorkflow. Also the two further entries in the item. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07587 | RWB-P4-AD008-APP | CG-ALL-4671 | 12.3 | Events row rwb.access.AccessPolicyChanged.v1: payload review id, role codes, counts of confirmed and removed holders, change kind; no holder reference and no personal field (gap-0127; asm-0204). |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07594 | RWB-P4-AD008-APP | GAP-0806 | 11, 12.7 | Add access_review and access_review_item with their columns and unique keys; allocate field IDs at the next dictionary version. |

### OTHER:Integration catalogue (TSD P4 T5.1; RWB-P4-AD008-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07595 | RWB-P4-AD008-APP | GAP-0808 | 8 | Fix the ACE Common group membership removal path: request (group, role code, holder reference, review, reason), answer with request reference, INT-21 reference, failure contract. |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07596 | RWB-P4-AD008-APP | GAP-0809 | 8 | Record that a role's owner is the holder of the A letter in Platform administration for that role, RW-COE for reference-data roles; a caller with R only owns no role and is refused. |

### OTHER:Operations story of legacy key RWB-AD-008 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-07597 | RWB-P4-AD008-APP | GAP-0807 | Metadata, 8 | Create the access-review Schedule with its cron as deployment configuration under the DL38 placeholder until the bank IAM standard value is supplied. |

### 07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20582 | RWB-P4-AD006-DB | R-16423 |  | SCR-43 is a P3 screen. Its states belong to the owning P3 story, not this screen workbook or the P4 DB story. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0777 | The rwb-access login name, the ACE group source behind a mapping row and the column set of the three library objects are not specified for the schema slice | ACE database engineer with the rwb-access service owner and the P1 data owner | Resolved (directive) |
| GAP-0787 | The mapping version columns, the mapping operations, the environment code and the group names are not specified | Tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0788 | The mapping contract shapes, its three paths and its event payload are not specified | Tech lead of rwb-access | Resolved (directive) |
| GAP-0789 | The version status, the effective dates, the approver reference, the four matrix operations and the right of the load are not specified for the permission matrix | Tech lead of rwb-access with the security administrator and the application owner | Resolved (directive) |
| GAP-0790 | The matrix contract shapes, its four paths, its status vocabulary and its event payload are not specified | Tech lead of rwb-access with the solution architect | Resolved (directive) |
| GAP-0791 | The two scope operation paths, the scope predicate fields and the home of the LOV-SCOPE list are not specified for the scope app slice | rwb-access service owner with the contract owner and the architecture review | Resolved (directive) |
| GAP-0792 | The scope contract has no source for its two paths, its predicate shape, its refusal entry fields or its version rule | contract owner of rwb-access with the consuming squads and the guard library owner | Resolved (directive) |
| GAP-0793 | The masking-profile operations, the PII read record and the view-column naming of a masking_rule row are not specified in any source | Solution architect | Resolved (directive) |
| GAP-0794 | The masking-profile contract shapes, the unmask record, the page default and the view-column naming have no source definition | Solution architect | Resolved (directive) |
| GAP-0796 | The check path and payloads, the name of the conflict-version field of the session answer and the rights of the two administrative reads are this contract's decision and not a source value | contract owner of rwb-access with the sign-in contract owner and the session contract owner | Resolved (directive) |
| GAP-0797 | The incident register, the two parameter codes and the right of the grant read are not specified for the break-glass slice | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0798 | The end and read operations, the two schema shapes and the payload of the grant are specified by no source | Tech lead of rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0799 | The grant table, its columns, its field ids, its retention and its partition are specified by no source | ACE database engineer | Resolved (directive) |
| GAP-0801 | Access-log search over the local chain while the central ledger is P7's | Tech lead of rwb-access | Resolved (directive) |
| GAP-0802 | The export file format, columns and row cap are not specified | Tech lead of rwb-access | Resolved (directive) |
| GAP-0804 | Whether a person may be searched by name is not specified | Data steward | Resolved (directive) |
| GAP-0806 | rwb-access access review list: the review-cycle store is not defined in any source | Solution architect and the rwb-access tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0808 | rwb-access access review list: the bank IAM removal API is not specified | Solution architect and the ACE team integration owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0809 | rwb-access access review list: the sources do not name the role owner who certifies a role | Security administrator and the solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0810 | rwb-access access review list: the state not confirmed is not defined | Security administrator | Resolved (directive) |
| GAP-0900 | rwb-access sandbox seed: the matrix letters for 11 of the 14 capability areas are not tabulated, so the seed content has no source table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0907 | rwb-access plan status: the TSD RBAC matrix has no Case record column, so the CASE_RECORD letters this slice decides are not tabulated for any role | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0917 | rwb-access treatment and plan-timer slice: the authorise request and answer, the Treatment and offer and Case record letters and the rwb-access login are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0923 | rwb-access booking confirmation: the TSD RBAC matrix has no Case record column, so the CASE_RECORD R and U letters the booking tasks need are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0926 | Permission letters for WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER and the scope of the Credit Administration role are absent from the RBAC matrix | Security administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0942 | rwb-access document set: the TSD RBAC matrix has no Documents column, so the four role letters the document set needs are carried only by the legacy authority table | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0945 | rwb-access letter dispatch loop: the TSD RBAC matrix has no Litigation column, so the LITIGATION C and R letters the legacy authority table names are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0948 | rwb-access letter dispatch loop: the role code and scope of the service identity that runs JOB-10 are not specified | Security architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0949 | The Documents letters per role are not carried by the P4 access documents | Security administrator with the P4 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0981 | rwb-access access-review extract (JOB-18): the interface ID, the file pattern, the extract layout, the recipient and the review-cycle date convention are not specified, the two requester activity names and the manifest are named by no source, and the delivery events are keyed by case ID while an access-review file has no case | Solution architect, P4 with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1571 | The break-glass duration, the minimum reason length and the review window appear only inside acceptance criteria and are open in the decision log | SCB IT security with the security administrator | Resolved (directive) |
| GAP-1572 | The six-monthly access review list has no interface, no file layout, no review-date convention and no recipient | Security administrator with the rwb-integration contract owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-2104 | Users and roles are read through iam_group, and ADR-010 allows only the 30 views | Solution architect | Resolved (directive) |
| GAP-2263 | The version dates, status and approver of the permission matrix, its four operations and the right of the load are not specified in the sources | Solution architect | Resolved (directive) |
| GAP-2264 | The matrix contract shapes, its status at the end of a load, its event payload and its baseline rules are not specified | Solution architect | Resolved (directive) |
| GAP-2265 | Two Work Packages write the same two story files and two fragments for legacy RWB-AD-003 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2267 | The published masking-profile document has no source line in the API specification and no ownership row | Solution architect, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2269 | Two Work Packages write the same two story files and two fragments for legacy RWB-AD-005 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2270 | Two Work Packages write the same three story files and three fragments for legacy RWB-AD-006 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2288 | The pack, its three check codes, the two operations, the five schemas, the parameter rows, the decided-version rule and the record code are not in the sources | Tech lead of rwb-access | Resolved (directive) |
| GAP-2304 | The access-change record code, the matrix version label, the matrix screen, the agent identity source and the grant's service event are not in the sources, and two sources disagree on the group column of a role and on the right of the path | Solution architect | Resolved (directive) |
| GAP-2324 | rwb-access next action: the RBAC matrix tabulates three capability areas and gives no Case record letter, so the R rights and the scopes the next-action read needs are not tabulated | Business analyst, P4 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
