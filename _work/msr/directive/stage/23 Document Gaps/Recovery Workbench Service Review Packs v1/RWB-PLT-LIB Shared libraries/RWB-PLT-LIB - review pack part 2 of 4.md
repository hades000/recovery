# RWB-PLT-LIB Shared libraries - review pack, part 2 of 4 (RWB-PLT-E1037-CON to RWB-PLT-E1043-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 5 |
| Resolved in the stories | 69 |
| Cross-document (pending in another document) | 173 |
| Not applied (value not in the sources) | 9 |
| Open business decisions | 16 |
| Register gaps linked | 103 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1037-CON | 13 | 50 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1037 CON Role to permission matrix as data and PDPA field masking by role - contract v2.md |
| RWB-PLT-E1042-APP | 10 | 23 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1042 APP Central configuration service and parameter catalog v2.md |
| RWB-PLT-E1042-CON | 21 | 48 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1042 CON Central configuration service and parameter catalog - contract v2.md |
| RWB-PLT-E1042-OPS | 10 | 26 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1042 OPS Central configuration service and parameter catalog - deployment v2.md |
| RWB-PLT-E1043-APP | 15 | 25 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-LIB Shared libraries/RWB PLT E1043 APP Reference data service with versioned tables v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22104 | GAP-2037 | Register gap | Architecture with Compliance | Two sources disagree on who applies the mask: rwb-source-data or each service | Both controls are kept and written as defence in depth: rwb-source-data masks in the view and in its contract, and each service re-applies the masking_rule rows of rwb-access before the response leaves. The story RWB-P4-E1037-APP owns the profile; the P1 story owns the view mask. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22105 | GAP-2136 | Register gap | Compliance | The plan does not say which service applies the mask once the masking rules are rwb-access data | rwb-access holds the approved masking version; rwb-source-data applies the mask at the 30 views; display masking at the API is applied by the service that owns the field, under the same version. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28578 | GAP-0162 | Register gap | Product head (Mortgage, HP, SSME) | The DoA limit amounts are not in this document | v5 names the owner (P4), the table (delegation_limit) and the two operations that serve it; the amounts stay in the Delegation of Authority Matrix and the DoA rule package and no amount is copied into this document. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28579 | GAP-0163 | Register gap | Compliance and PDPA officer | The masking rules per role, area and field group are not in this document | v5 names P4 as owner of masking_rule and GET /masking-policies as the contract; the rule values stay with Compliance and are loaded as a versioned reference data set. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28585 | GAP-2048 | Register gap | P4 rwb-access with Compliance | The alert recipient roles of version 3 are not mapped to role codes in rwb-access | The six recipient names are kept as they are and read as role names; the role codes are settled with the rwb-access role model before the per-service alert rules are built, and no code is invented here. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1038-APP | R-28587 | GAP-1579 | Register gap | Solution architect with Risk | No performance target covers the authorise answer, although every request passes one, and the nearest targets belong to other objects | Set one target for the authorise answer at the busiest hour, with the cache hit and the miss stated separately, and record it under DL11 beside the screen and rule-evaluation targets, so NFR-P4-001 becomes a testable number. |
| RWB-PLT-E1037-CON, RWB-PLT-E1072-CON, RWB-P4-E1037-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29029 | GAP-2809 | Register gap | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P4 rwb-access and platform library architects and the business owner of S4 | The D7.4 limit, the approval row and the rule-package read carry no value and no dependency row | Declare the approval as the P7 child workflow consumed on queue rwb-decision, the D7.4 limit and the approver's delegation as consumed on the rwb-access authorise contract, and the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43 as consumed from rwb-decision, each with the placeholder on its operation name and ceiling; fix no limit value in code or in the document, and leave the metadata rows as the plan gives them. |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-S4-E5015-APP, RWB-S4-E5015-CON | R-29032 | GAP-2807 | Register gap | Solution architect, S4 rwb-litigation, with the P3 rwb-case reference-data owner and the business owner of S4 | The fee schedule has no field list, no owner row and no version in any source | Read the fee schedule, the fee types and the court levels as versioned reference data of rwb-case on its contract, name the read on the contract rows of both stories with the operation name left as the placeholder, carry the schedule version on every decision record, and leave the metadata rows as the plan gives them. |
| RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1043-APP, RWB-P3-E1043-CON | R-29035 | GAP-0222 | Register gap | Data steward and data product owner | The Owner column is a stewardship role, not a service, and it is kept unchanged | Read column D as the stewardship owner that approves a value, and the appended 'Owning service (D-RCV-60)' as the service that loads and serves it; the Key sheet gains the two terms that say so. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1037-CON | R-18543 | DOR-RWB-PLT-E1037-CON-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is not in this chunk, so no anchor exists. No empty, loading, error or no-access state for SCR-43 or SCR-47 is given in the sources; not invented. |
| RWB-PLT-E1037-CON | R-18547 | DOR-RWB-PLT-E1037-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Sections 7 and 16 are not in this chunk, so no criterion or test row can be anchored or formatted. Re-issue with those parts. BR1 to BR12 coverage remains open. |
| RWB-PLT-E1037-CON | R-31742 | NEWAC-RWB-PLT-E1037-CON-AC14 | 7, 16 | AC14: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Section 7 and 16 text is not in this chunk, so the criterion style and the test row anchor cannot be matched. Proposed test is Not specified in the source documents. Re-issue with those parts. |
| RWB-PLT-E1042-APP | R-18549 | DOR-RWB-PLT-E1042-APP-1 | 1 | Definition of Ready item 1 Story: Partial | No role code or name in the sources matches the user; the §1 role stays as in the source. A role name must be supplied. |
| RWB-PLT-E1042-OPS | R-18568 | DOR-RWB-PLT-E1042-OPS-4 | 8 | Definition of Ready item 4 Business rules: Partial | BR1-BR8 map to AC1-AC8 and TC-01 to TC-07 in section 8, but section 7 and 16 text is not in this chunk. Cannot anchor the AC8 and TC row edits; needs next chunk. |
| RWB-PLT-E1043-APP | R-07182 | DOR-RWB-PLT-E1043-APP-14 | n/a | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or source set; searched .md sources for epic design and sign-off, none found outside cache and quarantine copies. Sign-off cannot be confirmed here. |
| RWB-PLT-E1043-APP | R-18576 | DOR-RWB-PLT-E1043-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Coverage needs criteria in section 7 and test case rows in section 16; neither is in this chunk, so no edit is possible. Section 8 left unchanged. |
| RWB-PLT-E1043-APP | R-18578 | DOR-RWB-PLT-E1043-APP-9 Messages: Partial | 14 | Definition of Ready item 9 Messages: Partial | Error and Message Standard v4 text is not in this chunk, so MSG-P3-027 cannot be copied from it; message text left unchanged. |
| RWB-PLT-E1043-APP | R-31749 | NEWAC-RWB-PLT-E1043-APP-AC11 (AC9 in story) | 7, 8, 16 | AC11: §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | AC9 with TC-PLT-E1043-APP-08 covers BR1 (eleven codes). BR2 to BR10 still have no criterion and no test. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (28)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13868 | RWB-PLT-E1037-CON | CG-ALL-1319 | header | Renumber the duplicate FR-PLT-008 in the PRD's next version |
| CDC-13869 | RWB-PLT-E1037-CON | CG-ALL-1320 | header | Renumber the duplicate FR-PLT-019 in the PRD's next version |
| CDC-13870 | RWB-PLT-E1037-CON | CG-ALL-1321 | header | Renumber the duplicate FR-PLT-026 in the PRD's next version |
| CDC-13871 | RWB-PLT-E1037-CON | CG-ALL-1322 | 18 | Renumber the duplicate FR-PLT-033 in the PRD's next version. |
| CDC-13874 | RWB-PLT-E1037-CON | DOR-RWB-PLT-E1037-CON-2 | 18 | Renumber the duplicate FR-PLT-008, FR-PLT-019, FR-PLT-026 and FR-PLT-033 in the PRD's next version. |
| CDC-13920 | RWB-PLT-E1042-APP | CG-ALL-1328 | find it | Renumber the duplicate FR-PLT-008 (synthetic development, masked acceptance, personal-data scan). |
| CDC-13921 | RWB-PLT-E1042-APP | CG-ALL-1329 | find it | Renumber the duplicate FR-PLT-016 (feature flags with a removal date; versioned feature flag rows). |
| CDC-13922 | RWB-PLT-E1042-APP | CG-ALL-1330 | header | Renumber the duplicate FR-PLT-017 in the PRD's next version so that one meaning remains. |
| CDC-13923 | RWB-PLT-E1042-APP | CG-ALL-1331 | header | Renumber the duplicate FR-PLT-018 in the PRD's next version so that one meaning remains. |
| CDC-13924 | RWB-PLT-E1042-APP | CG-ALL-1332 | header | Renumber the duplicate FR-PLT-019 in the PRD's next version so that one meaning remains. |
| CDC-13926 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-2 | 18 | Renumber the duplicate meanings of FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018 and FR-PLT-019 in the PRD's next version. |
| CDC-13939 | RWB-PLT-E1042-CON | CG-ALL-1338 | header | Renumber one of the two FR-PLT-008 rows in the PRD's next version so that each ID has one meaning. |
| CDC-13940 | RWB-PLT-E1042-CON | CG-ALL-1339 | header | Renumber one of the two FR-PLT-016 rows in the PRD's next version so that each ID has one meaning. |
| CDC-13941 | RWB-PLT-E1042-CON | CG-ALL-1340 | header | Renumber one of the two FR-PLT-017 rows in the PRD's next version so that each ID has one meaning. |
| CDC-13942 | RWB-PLT-E1042-CON | CG-ALL-1341 | header | Renumber one of the two FR-PLT-018 rows in the PRD's next version so that each ID has one meaning. |
| CDC-13943 | RWB-PLT-E1042-CON | CG-ALL-1342 | header | Renumber one of the two FR-PLT-019 rows in the PRD's next version so that each ID has one meaning. |
| CDC-13947 | RWB-PLT-E1042-CON | DOR-RWB-PLT-E1042-CON-2 | 18 | Make FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018 and the one further FR-PLT ID in detcheck each have a single meaning. |
| CDC-13991 | RWB-PLT-E1042-OPS | CG-ALL-1347 |  | Renumber the duplicate FR-PLT-008 in the next PRD version |
| CDC-13992 | RWB-PLT-E1042-OPS | CG-ALL-1348 |  | Renumber the duplicate FR-PLT-016 in the next PRD version |
| CDC-13993 | RWB-PLT-E1042-OPS | CG-ALL-1349 |  | Renumber the duplicate FR-PLT-017 in the next PRD version |
| CDC-13994 | RWB-PLT-E1042-OPS | CG-ALL-1350 | find it | Renumber one of the two FR-PLT-018 rows in the next PRD version |
| CDC-13995 | RWB-PLT-E1042-OPS | CG-ALL-1351 | find it | Renumber one of the two FR-PLT-019 rows in the next PRD version |
| CDC-13999 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-2 | 18 | Renumber the duplicate rows of FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018 and the further duplicate in the detcheck |
| CDC-14017 | RWB-PLT-E1043-APP | CG-ALL-1359 | 18 | Renumber the duplicate FR-PLT-016 entry (feature flags with a removal date) in the PRD's next version. |
| CDC-14018 | RWB-PLT-E1043-APP | CG-ALL-1360 | 18 | Renumber the duplicate FR-PLT-017 entry (parameter and configuration client) in the PRD's next version. |
| CDC-14019 | RWB-PLT-E1043-APP | CG-ALL-1361 | 18 | Renumber the duplicate FR-PLT-018 entry (reference-data client) in the PRD's next version. |
| CDC-14020 | RWB-PLT-E1043-APP | CG-ALL-1362 | 18 | Renumber the duplicate FR-PLT-020 entry (embedded rules kit) in the PRD's next version. |
| CDC-14023 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-2 | 18 | Renumber the four duplicate FR-PLT IDs (016, 017, 018, 020) in the PRD's next version so each has one meaning. |

### RWB-PLT-E1042-CON (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13916 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-21 | find it | Reach Done with the contract published; the story is In build. |
| CDC-13917 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-22 | find it | Publish a contract fake library version and record it as published. |
| CDC-13928 | RWB-PLT-E1042-APP | GAP-1406 | 13 | Pin artefact coordinates from the platform library baseline at version freeze in the service template; read TTL from refdata.cache.ttl-seconds; name rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1; publish both build-check rule sets. |
| CDC-13929 | RWB-PLT-E1042-APP | GAP-1407 | 11 | Publish one versioned contract artefact at major version 1 with the interface, four types, key set, DF-REF-132 to DF-REF-158 contract, four P3 operations with status codes and message ids, cache, refresh and start-up rules, two build-check contracts and a fake. |
| CDC-13987 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-21 | Header | Publish the contract; its build status must reach Done |
| CDC-13988 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-22 | find it | Record the published version of the contract fake library that this story's tests run against. |
| CDC-13989 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-23 | find it | State the contract version this story builds against, in place of the /v1 path only. |
| CDC-14001 | RWB-PLT-E1042-OPS | GAP-1406 | 13 | Pin artefact coordinates from the library baseline in the service template; read cache TTL from refdata.cache.ttl-seconds; name rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1; publish build-check rule sets 0, 1, -1 and test code. |
| CDC-14002 | RWB-PLT-E1042-OPS | GAP-1407 | find it | Publish one versioned contract artefact v1 with the interface, four types, key set, DF-REF-132 to DF-REF-158, four operations with status codes and message ids, cache and refresh rule, start-up rule, build-check contracts and a fake. |
| CDC-14010 | RWB-PLT-E1042-OPS | GAP-2215 |  | Confirm the capability area and right of the three reference-load write operations with the rwb-access owner and record them in the authorise model. Until then keep the legacy rights and the guard the service template wires. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13864 | RWB-PLT-E1037-CON | CG-ALL-1316 | 12.4 | Add rwb.access.DoALimitChanged.v1 to the Events sheet of the catalog |
| CDC-13865 | RWB-PLT-E1037-CON | DOR-RWB-PLT-E1037-CON-8 | 12.4 | Add platform as a consumer of rwb.access.AccessPolicyChanged.v1 and add the rwb.access.DoALimitChanged.v1 Events row |
| CDC-13867 | RWB-PLT-E1037-CON | CG-ALL-1315 | 12.4 | Add platform as a consumer of rwb.access.AccessPolicyChanged.v1 in the Events row and in its ACL |
| CDC-13914 | RWB-PLT-E1042-APP | CG-ALL-1325 | 12.4 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet on topic rwb.case.events.v1. |
| CDC-13918 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-8 | 12.4 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet on topic rwb.case.events.v1. |
| CDC-13937 | RWB-PLT-E1042-CON | CG-ALL-1335 | 12.4 | Add rwb.case.ParameterVersionApproved.v1 to the Events sheet: topic rwb.case.events.v1, producer P3 rwb-case, fields paramKeys, versionNo, validFrom. |
| CDC-13938 | RWB-PLT-E1042-CON | DOR-RWB-PLT-E1042-CON-8 | 12.4 | Add rwb.case.ParameterVersionApproved.v1 to the Events sheet: topic rwb.case.events.v1, producer P3 rwb-case, fields paramKeys, versionNo, validFrom. |
| CDC-13985 | RWB-PLT-E1042-OPS | CG-ALL-1344 | 12.4 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet |
| CDC-13990 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-8 | 12.4 | Add event type rwb.case.ParameterVersionApproved.v1 to the Events sheet |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13881 | RWB-PLT-E1037-CON | GAP-1564 |  | Confirm at the RWB-P3 reference-data contract review that the load, approve, verify and rollback surface stays with rwb-case, and record the ruling on the Ownership Map. |
| CDC-13908 | RWB-PLT-E1037-CON | GAP-2039 | find it | Add an access_log row owned by P4 rwb-access, with its key and retention class, and its own DB story in RWB-SVC-P4. |
| CDC-13912 | RWB-PLT-E1037-CON | GAP-2041 | 2 | State that the S9 rwb-partner administrator creates and ends the partner user, the roles it holds are P4 role rows granted by the P4 role owner, and both actions are written to the access log. |
| CDC-13913 | RWB-PLT-E1037-CON | GAP-2063 | 5 | Add owner rows for gateway-bff and the partner gateway: screen response composition owned by RWB-PLT-EDGE; partner gateway owned by RWB-PLT-EDGE with S9 rwb-partner behind it. |
| CDC-13931 | RWB-PLT-E1042-APP | GAP-2213 | 12 | Add the run-time read of the catalog with the right a service identity holds and the keys artefact the platform client publishes. Until then, serve the key-prefix query of GET /admin/parameters to a service identity holding Rules and parameters R. |
| CDC-13970 | RWB-PLT-E1042-CON | GAP-2213 | 7, 13 | Add the run-time catalog read to the Ownership Map with the right and scope a service identity holds. Record the keys artefact the platform client publishes. |
| CDC-14005 | RWB-PLT-E1042-OPS | GAP-2213 | find it | Add the run-time catalog read with the right a service identity holds and the keys artefact; until then serve the key-prefix query of GET /admin/parameters to a service identity holding Rules and parameters R. |
| CDC-14034 | RWB-PLT-E1043-APP | GAP-0698 | 8 | Give Reference data A on the verify and rollback operations, with the separation of duty of RWB-E1-043 section 10 unchanged. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13872 | RWB-PLT-E1037-CON | DOR-RWB-PLT-E1037-CON-1 | 1 | Add 'platform contract owner' as a role code or role name, or confirm the existing role it maps to. |
| CDC-13910 | RWB-PLT-E1037-CON | GAP-0166 | find it | Resolve the six SY actors through POST /authorise with their SY role code and managed identity as subject; leave the credential type to RWB-P4-E1037-CON. |
| CDC-13944 | RWB-PLT-E1042-CON | DOR-RWB-PLT-E1042-CON-1 | 1 | Add the role name 'platform contract owner' or map section 1 to an existing role code and name in the document. |
| CDC-13996 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-1 | 1 | Add role 'DevOps engineer of the platform' with its role code to Users Roles and Permissions v5 |
| CDC-14021 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-1 | 1 | Add 'service developer' as a role code or role name so that the role in section 1 resolves to it. |

### API:(service not named) (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13876 | RWB-PLT-E1037-CON | GAP-1568 |  | Publish the four rwb-access operations with request and answer schemas, refusal and not-found codes, version fields and the masking marker vocabulary, then freeze the contract. |
| CDC-13932 | RWB-PLT-E1042-APP | GAP-1558 |  | Set x-module to P3 for GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling paths. |
| CDC-13971 | RWB-PLT-E1042-CON | GAP-1558 |  | Set the x-module to P3 for GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling paths. |
| CDC-14006 | RWB-PLT-E1042-OPS | GAP-1558 | find it | Set x-module to P3 for GET /admin/lists/{listCode}, POST /admin/reference-loads and the three sibling paths. |
| CDC-14025 | RWB-PLT-E1043-APP | GAP-1558 | find it | Set x-module to P3 for the five list and reference-load paths: GET /admin/lists/{listCode}, POST /admin/reference-loads and three sibling paths. |

### RWB-P4-E1037-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13880 | RWB-PLT-E1037-CON | GAP-1245 |  | Authorise answer carries the scope kind and case-scope predicate applied to each case ID; the Compliance incident queue is read from platform configuration. Confirm with the P4 and P3 owners. |
| CDC-13882 | RWB-PLT-E1037-CON | GAP-0159 |  | Publish the OpenAPI document with operation IDs, bodies, status codes and error model for POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies. |
| CDC-13883 | RWB-PLT-E1037-CON | GAP-0160 |  | Map /me/session to /me/permissions as the contract name and record the rename in the API catalogue. |
| CDC-13911 | RWB-PLT-E1037-CON | GAP-0248 | 2 | State that the masking function recovery.ace_mask_value stays in the recovery view schema with the views, that masking policy rows stay in rwb_access (P4), and that rwb-source-data applies the mask in the view and in its responses. |
| CDC-14024 | RWB-PLT-E1043-APP | GAP-0779 | find it | Keep load and approve for permission and masking tables on /api/recovery/access/v1; publish /api/recovery/access/v1/masking-policies with Reference data R; publish AccessPolicyChanged with change kind, version and effective date, no personal value. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13903 | RWB-PLT-E1037-CON | CG-ALL-1317 | 16 | Add Story test cases rows for TC-PLT-E1037-CON-01 to TC-PLT-E1037-CON-05, with Given, When and Then copied from the criteria AC1 to AC6 in section 7. |
| CDC-13919 | RWB-PLT-E1042-APP | CG-ALL-1326 | 16 | Add rows TC-PLT-E1042-APP-01 to TC-PLT-E1042-APP-07 with Given, When and Then copied from the criterion each covers. |
| CDC-13974 | RWB-PLT-E1042-CON | CG-ALL-1336 | 16 | Add rows for TC-PLT-E1042-CON-01 to TC-PLT-E1042-CON-05 with Given, When and Then copied from the covered criteria. |
| CDC-14007 | RWB-PLT-E1042-OPS | CG-ALL-1345 | 16 | Add rows TC-PLT-E1042-OPS-01 to TC-PLT-E1042-OPS-06 with Given, When and Then copied from the criteria each row covers. |
| CDC-14016 | RWB-PLT-E1043-APP | CG-ALL-1356 | 16 | Add rows TC-PLT-E1043-APP-01 to TC-PLT-E1043-APP-07 with Given, When and Then copied from the criteria they cover in section 7. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13904 | RWB-PLT-E1037-CON | CG-ALL-1318 | 18 | Align the test lists for the six requirements with the story section 18 (TC-PLT-E1037-CON-01 to -05), in the next RTM version. |
| CDC-13933 | RWB-PLT-E1042-APP | CG-ALL-1327 | 18 | In the next RTM version, align the REQ-DRI-010 test list with section 18: TC-PLT-E1042-APP-01 to TC-PLT-E1042-APP-07. |
| CDC-13975 | RWB-PLT-E1042-CON | CG-ALL-1337 | 18 | Align the test lists of RTM and section 18 in their next versions. |
| CDC-14008 | RWB-PLT-E1042-OPS | CG-ALL-1346 | 18 | Align REQ-DRI-010 in RTM v7 with story section 18 (TC-PLT-E1042-OPS-01, -02, -06). |
| CDC-14030 | RWB-PLT-E1043-APP | CG-ALL-1357 | 18 | Align the test lists traced for REQ-DRI-011 and the other differing requirements between section 18 and RTM v7 in their next versions. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13873 | RWB-PLT-E1037-CON | DOR-RWB-PLT-E1037-CON-12 | 16 | Add TC-PLT-E1037-CON-01 to TC-PLT-E1037-CON-05 to Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-13946 | RWB-PLT-E1042-CON | DOR-RWB-PLT-E1042-CON-12 | 16, 18 | Add TC-PLT-E1042-CON-01 to TC-PLT-E1042-CON-05 to Test Cases v8; align the section 18 test lists with RTM v7. |
| CDC-13997 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-12 | 16, 18 | Add TC-PLT-E1042-OPS-01 to -06 to Test Cases v8; align the section 18 test lists in RTM v7 with this story |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13900 | RWB-PLT-E1037-CON | GAP-1885 |  | Carry the five consumed rows as non-blocking dependencies; name the case read, route fact and instruction request in the case and partner contract stories. |
| CDC-13901 | RWB-PLT-E1037-CON | GAP-2751 |  | Carry API-P5-002, API-P5-008 and API-P3-002 as non-blocking consumed rows; RWB-P3-E1043-CON as C; name case-state announcement and task raise in the P3 contract. |
| CDC-13902 | RWB-PLT-E1037-CON | GAP-2801 |  | Carry the four consumed surfaces as non-blocking rows with RWB-P3-E1043-CON as C; name case read, route facts and instruction request in the case and partner contracts. |

### OTHER:rwb-case repository and service template (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13935 | RWB-PLT-E1042-APP | GAP-2214 | 7 | Fix the five names: target Java package, used_by convention, flag name the platform library allocates, next free rwb-case migration numbers, one primary key for parameter_catalog. |
| CDC-13982 | RWB-PLT-E1042-CON | GAP-2214 | Header | Fix the five legacy names (Java package, used_by convention, feature flag, next migration numbers, parameter_catalog primary key) to target forms. Values not specified in the source documents (GAP-2214). |
| CDC-14009 | RWB-PLT-E1042-OPS | GAP-2214 |  | Fix the five names: the target package, a used_by convention, the flag name the platform library allocates, the next free numbers of the rwb-case sequence and one primary key for parameter_catalog. |

### OTHER:23 Document Gaps/Recovery Workbench Gap Register v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13966 | RWB-PLT-E1042-CON | GAP-1406 | 3, 4, 8, 13 | Take artefact coordinates from the platform library baseline at version freeze; read cache TTL from refdata.cache.ttl-seconds; refresh on rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1; publish both build-check rule sets. |
| CDC-13967 | RWB-PLT-E1042-CON | GAP-1407 | 11, 12 | Publish one versioned contract artefact at major version 1 with interface, types, key set, DF-REF-132 to DF-REF-158, four operations with status codes, cache and start-up rules, build-check contracts and a fake. |
| CDC-13968 | RWB-PLT-E1042-CON | GAP-1408 | 3, 4, 5 | Fix chart values RWB_ENV, RWB_PARAMETER_CATALOG and RWB_PARAMETER_TTL_KEY; add a seed hook before rollout; one page and two warnings from library metrics. |

### RWB-PLT-E1043-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14013 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-21 |  | Set the build status of RWB-PLT-E1043-CON to Done once the contract is published. |
| CDC-14014 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-22 |  | Record the published contract fake library version in RWB-PLT-E1043-CON. |
| CDC-14029 | RWB-PLT-E1043-APP | GAP-1410 published reference-data client contract not specified in a technical specification | header; 15 | Story states the contract version as Not specified (DOR-23) and the non-retryable checked refusal carrying MSG-P3-027, table code and business date. The artefact sits in RWB-PLT-E1043-CON. |

### RWB-P7-E2041-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13879 | RWB-PLT-E1037-CON | GAP-2414 |  | Carry H as None plus the eight platform contracts of the DP table and C as RWB-P3-E2041-CON plus the four published contracts; keep Ready to start at Day 1. |
| CDC-13954 | RWB-PLT-E1042-CON | GAP-2414 |  | Set H to None plus eight platform contracts and C to RWB-P3-E2041-CON plus the four published contracts; treat RWB-P7-E2042-APP as the registry set, rechecked at wave 2. |

### RWB-P4-AD003-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13898 | RWB-PLT-E1037-CON | GAP-0791 |  | Publish role-scopes read and change paths under the R4 base and DP-13; carry the predicate as the scope element of RWB-P4-E1037-CON's authorise answer; record scope change as AccessPolicyChanged. |
| CDC-13899 | RWB-PLT-E1037-CON | GAP-0792 |  | Fix GET and PATCH admin role-scopes paths, the four-field predicate, 404 MSG-P4-003 refusal with OUT_OF_SCOPE, and AccessPolicyChanged with kind SCOPE. |

### Epic design record (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13915 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-14 | find it | Record the signed epic design sign-off for RWB-PLT-E1042-APP. |
| CDC-13986 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-14 | find it | Record the signed epic design sign-off for RWB-PLT-E1042, then confirm it in this story's Definition of Ready. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13925 | RWB-PLT-E1042-APP | DOR-RWB-PLT-E1042-APP-12 | 16, 18 | Test Cases v8 must add TC-PLT-E1042-APP-01 to TC-PLT-E1042-APP-07; RTM v7 test lists must match §18. |
| CDC-14022 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-12 | 16 | Add TC-PLT-E1043-APP-01 to TC-PLT-E1043-APP-07 to Test Cases v8; align the §18 test lists for this story with RTM v7. |

### RWB-P6-E1073-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13927 | RWB-PLT-E1042-APP | GAP-1214 | 13 | Fix the five points at the contract review: local copy table and columns, the two parameter rows and read path, the two check values, the travel shape of the scenario set, and the 300 ms measurement point. |
| CDC-13979 | RWB-PLT-E1042-CON | GAP-1218 | 13 | Add RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON to its H list or state them as wave-0 prerequisites; keep Ready Day 1. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13934 | RWB-PLT-E1042-APP | GAP-3232 | 18 | Use the catalog as the source of the v5 graph and state the template baseline once on the Dependency classes sheet. Story files keep their rows; no story is re-cut. |
| CDC-14032 | RWB-PLT-E1043-APP | GAP-3232 | none | Use the catalog as the source of the v5 graph and state the template baseline once on the Dependency classes sheet; story files keep their rows. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13969 | RWB-PLT-E1042-CON | GAP-2212 | 13 | Add ParameterVersionApproved with its number, key and payload paramKeys, versionNo and validFrom. Until then publish it on rwb.case.events.v1 and keep the TTL as fallback. |
| CDC-14004 | RWB-PLT-E1042-OPS | GAP-2212 | find it | Add the parameter event with its number, key and payload; until then publish rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1 with paramKeys, versionNo, validFrom, and keep cache TTL as fallback. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14011 | RWB-PLT-E1043-APP | CG-ALL-1354 | 13 | Create story RWB-P7-E1073-CON, or name the existing story that carries the same capability and update the dependency in the header and section 13. |
| CDC-14012 | RWB-PLT-E1043-APP | DOR-RWB-PLT-E1043-APP-17 | header, 13 | Create RWB-P7-E1073-CON or name the existing story carrying the same capability, so all 12 named dependencies are story files. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14026 | RWB-PLT-E1043-APP | GAP-0217 | find it | Keep the 25 LOV-REF-TABLE values unchanged; reference data administrator reconciles the twelve-code contract subset before the first approved wave 1 reference load. |
| CDC-14027 | RWB-PLT-E1043-APP | GAP-0219 | find it | Add the S1 rwb-valuation and S7 rwb-writeoff starter rows at the next revision; each service story names the lists it reads. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13866 | RWB-PLT-E1037-CON | GAP-0013 | n/a | Version the six ACE Common contracts and run contract tests on both sides from wave 1; owner ACE team |

### OTHER:Technical Specification P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13875 | RWB-PLT-E1037-CON | GAP-0481 | 8 | Remove masking_rule from the P1 schema (T3.6); P1 holds data_product_access only and takes the masking answer from POST /api/recovery/access/v1/authorise and the FieldMasker of RWB-P4-E1037-CON. |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13877 | RWB-PLT-E1037-CON | GAP-0355 |  | Name the access-log read-back operation for the AC-EXPT entry, apply P4 masking rules over the P1 masked columns, and keep owner display names synthetic in SIT. |

### OTHER:TSD P3 v3 T-A.2 (API-P3-001; RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13878 | RWB-PLT-E1037-CON | GAP-2208 |  | Publish team as an additive optional filter on GET /cases; name the rwb-access access-log operation with the AC-EXPT fields; record masking travels in the authorise answer. |

### RWB-P4-E1037-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13884 | RWB-PLT-E1037-CON | GAP-0161 |  | Record fail-closed rule, refresh on AccessPolicyChanged and DoaLimitChanged, and 5 minute membership refresh; cache lifetime stays a placeholder (Not specified in the source documents, GAP-0161). |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Roles) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13885 | RWB-PLT-E1037-CON | GAP-0164 |  | Record that PT role rows, letters and default scope stay with P4, S9 holds partner user and user-to-role link, and S9 calls POST /authorise with the PT role code. |

### OTHER:Data dictionary v4 (DF-DOC-089; OTHER:DF-DOC-015) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13886 | RWB-PLT-E1037-CON | GAP-0262 |  | Classification left to the data steward; row carries rule never in an event, workflow input or log, and page id only in a log, as for a Restricted field. |

### API:(service not named); OTHER:TSD P4 v3 (T6.1; OTHER:T-A); 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13887 | RWB-PLT-E1037-CON | GAP-0778 |  | Fix path as /api/recovery/access/v1/masking-policies with Reference data R; count rows from approved file (756 rows at 54 roles); AccessPolicyChanged carries change kind, version label and effective date only. |

### parameter-catalog.csv; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13888 | RWB-PLT-E1037-CON | GAP-1404 |  | Add cache time to live parameter key with value Not specified in the source documents (GAP-1404); publish library artefact at a platform coordinate with major version 1. |

### OTHER:Platform library contract and P4 rwb-access contract (API yaml and contract freeze record) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13889 | RWB-PLT-E1037-CON | GAP-1405 | 8 | Publish the three interface signatures with input and output types and the personal-data annotation with its field-id attribute. Masking policy at GET /api/recovery/access/v1/masking-policies. Audit record: case id, field id, flag clear or masked. Every access-owner failure maps to 503 with no business data. Record the four shapes at contract freeze. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx; OTHER:TSD P4 v3 T5.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13890 | RWB-PLT-E1037-CON | GAP-1569 |  | Add AccessPolicyChanged and DoaLimitChanged rows (CloudEvents type, topic rwb.access.events.v1, key, payload, versioning, refresh window); replace T5.3 'None' with the two events. |

### API:(service not named); OTHER:TSD P4 v3 (T-A) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13891 | RWB-PLT-E1037-CON | GAP-0779 |  | Keep load and approve on /api/recovery/access/v1 for P4 tables; generic reference-load path with P3 rwb-case; publish masking-policies with Reference data R; AccessPolicyChanged with no personal value. |

### RWB-P6-E1055-APP; OTHER:rwb-comms API document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13892 | RWB-PLT-E1037-CON | GAP-1098 |  | Record that the Litigation area and R right are enforced at gateway-bff on the screen path; add RWB-P4-E1037-CON as C dependency or state the service identity call carries no user right. |

### RWB-P6-E2021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13893 | RWB-PLT-E1037-CON | GAP-1223 | Header | Set H to None plus the platform contracts the DP table names; set C to RWB-P7-E2013-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. Story stays Day 1. |

### RWB-P6-E2021-CON; RWB-P6-E2021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13894 | RWB-PLT-E1037-CON | GAP-1092 |  | Declare capability area and right per operation in RWB-P6-E2021-CON; add a guard call to rwb-access DP-08 and a scope fact source from the rwb-case read, or add C RWB-P4-E1037-CON. |

### RWB-P2-E2036-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13895 | RWB-PLT-E1037-CON | GAP-2412 |  | Publish placement fact element names, P3 case-read and P4 authorise shapes, reference-data operation, MSG-P7-009 text, service login and platform contract rows. |

### RWB-S8-E7004-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13896 | RWB-PLT-E1037-CON | GAP-3057 |  | Record the five consumed rows, the DP-04, DP-05, DP-09 and DP-16 rows, the rule kit, outbox and inbox, access guard, and the deviation state list of values. |

### OTHER:Search story and its Work Package dependency rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13897 | RWB-PLT-E1037-CON | GAP-2335 |  | Add C RWB-P3-E1018-CON and C RWB-P4-E1037-CON to the search story dependency map at D1; state buildable from Day 1 against two fakes. |

### OTHER:Security and Access Design v4 (section 7 and section 1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13905 | RWB-PLT-E1037-CON | GAP-2035 | find it | Write section 7 per service: one login per service, grants on own schema only, view grant held only by rwb_source_data, and replace the recovery_svc isolation row. State the change in v5 realignment table. |

### RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13906 | RWB-PLT-E1037-CON | GAP-1028 | find it | Record the split and origin of the six new criteria; publish GET /api/recovery/document/v1/retention-classes and GET /api/recovery/document/v1/retention-classes/{classCode} with the RetentionClass shape of RWB-P5-AD021-CON; add the four missing C entries; add no H dependency. |

### OTHER:TSD P4 T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13907 | RWB-PLT-E1037-CON | GAP-1574 | find it | Publish the approved role conflict list with its version label and effective dates; add matrix effective-date columns to T3.1 or state the date lives on the load; confirm the role and permission row counts. |

### OTHER:RWB-P4-E1039 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13909 | RWB-PLT-E1037-CON | GAP-2076 | find it | State that the access row records the version the owning service applied at the event; the rwb-decision registry stays the source of the version and its effective date. |

### RWB-PLT-E1042-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13930 | RWB-PLT-E1042-APP | GAP-1408 | 3 | Fix RWB_ENV, RWB_PARAMETER_CATALOG and RWB_PARAMETER_TTL_KEY; add a pre-rollout parameter-catalog-seed hook failing on a key with no entry, owner or default; probe the start-up check; one page and two warnings from library metrics. |

### OTHER:rwb-access authorise model and TSD P3 v3 rights for the reference-load paths (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13936 | RWB-PLT-E1042-APP | GAP-2215 | 7 | Record capability area and right for the load (C), rollback (U) and approve (A) operations; keep the legacy rights until the rwb-access owner confirms. |

### RWB-P3-E1042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13945 | RWB-PLT-E1042-CON | DOR-RWB-PLT-E1042-CON-10 |  | Add empty, loading, error and no-access states for SCR-39 in the P3 story's screen section. |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13948 | RWB-PLT-E1042-CON | GAP-1946 | find it | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes; read the ACE-side check as the DP06 data product; drop the two extracts and the INT-19 path. |

### RWB-P6-E1011-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13949 | RWB-PLT-E1042-CON | GAP-1167 | find it | Keep H at None; record the seven platform CONs as wave-0 build prerequisites as platform prerequisites, not lane dependencies, so the L-P6-C depth is unchanged. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13950 | RWB-PLT-E1042-CON | GAP-1174 | find it | Add RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON and RWB-PLT-E1044-CON to the RWB-P6-E1019-APP dependency rows, or record them in the platform release train. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13951 | RWB-PLT-E1042-CON | GAP-2404 |  | Set the H list to None plus the five platform contracts in the DP table and the C list to RWB-P10-E2032-CON plus the P3 and P4 contracts, as the proposed fix states. |

### OTHER:Work package story line for the story concerned and its section 13 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13952 | RWB-PLT-E1042-CON | GAP-2448 |  | Keep the work package metadata rows as fixed; record the DP-table platform, rwb-case and rwb-access contracts in section 13 of that story. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13953 | RWB-PLT-E1042-CON | GAP-1198 |  | Add the seven platform contracts and the two P3 contracts to the dependency rows of RWB-P6-E1032-APP, or record them in the platform release train. |

### RWB-P5-E1049-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13955 | RWB-PLT-E1042-CON | GAP-1206 |  | Update the plan dependency row to six H rows and three C rows from the DP table; keep the written story metadata until the plan is corrected. |

### OTHER:Legacy RWB-E1-063; OTHER:TSD P4 v3 T6.1; OTHER:FSD P4 REQ-ACA-006 and NFR-042; RWB-P10-E1063-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13956 | RWB-PLT-E1042-CON | GAP-2333 |  | Record Reporting letters in the matrix load, replace the lake copy rule with the served-read access entry, correct REQ-ACA-006 and NFR-042, and add the platform and rwb-case contracts to the story concerned. |

### OTHER:rwb-decision and rwb-comms contract review; RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13957 | RWB-PLT-E1042-CON | GAP-1214 |  | Fix the local copy table and columns, the two parameter rows and read path, the two check values with message text, the scenario set shape, and the 300 ms measurement point. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md; RWB-P7-E1073-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13958 | RWB-PLT-E1042-CON | GAP-0672 |  | Record the eight DP H rows as wave-0 prerequisites, publish the model fetch in RWB-P7-E1073-CON, fix the local copy table, and name the login before the baseline. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13959 | RWB-PLT-E1042-CON | GAP-1328 |  | Complete the metadata rows from the DP table (eight H rows, C rows of DP-06 and DP-07, DP-09 pattern) or state in R5.5 that platform and self-referential rows are held elsewhere. |

### OTHER:Work package B2-P3-020 story line and the assembler lane allocation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13960 | RWB-PLT-E1042-CON | GAP-2261 |  | Add the platform CON dependencies to the lane and the Day-1 allocation, keeping the metadata row as delivered by the work package. |

### RWB-P7-E2002-APP; OTHER:Template and Rules v1 R5.5 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13961 | RWB-PLT-E1042-CON | GAP-2470 |  | Complete the H and C rows of RWB-P7-E2002-APP from the DP table, and state in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories. |

### OTHER:Template and Rules v1 R5.5; RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13962 | RWB-PLT-E1042-CON | GAP-2475 |  | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories and are not repeated on secondary APP lines. Keep the plan rows until then. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13963 | RWB-PLT-E1042-CON | GAP-1223 |  | Read H as None plus the platform contracts named in the DP table. Read C as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON. The story stays Day 1. |

### RWB-S4-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13964 | RWB-PLT-E1042-CON | GAP-1898 |  | Keep the plan lists and the Day 1 status with RWB-P5-E2025-CON as the only contract. Remove DP-09 and DP-10 from the pattern list. Add the five H and two C rows when they publish. |

### RWB-P8-E2027-CON; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13965 | RWB-PLT-E1042-CON | GAP-1291 |  | Keep the metadata rows as the plan gives them. Record the DP-added H and C rows in the Dependency Map as non-blocking platform and published contracts. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; RWB-P4-E8015-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13972 | RWB-PLT-E1042-CON | GAP-2296 |  | Add a JOB-nn row for the daily rwb-access chain check; add RWB-PLT-E1071-CON to the H list of RWB-P4-E8015-APP. |

### OTHER:RWB-P4 rule-version load story and build plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13973 | RWB-PLT-E1042-CON | GAP-0822 |  | Keep compile, checks and SIT scenario run in rwb-decision; record that rwb-access embeds no Drools kit and carries no DP-04. |

### OTHER:TSD P7 v2 and the RWB-P8 database story build plan (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13976 | RWB-PLT-E1042-CON | GAP-1279 |  | Name the rwb-decision login (DP-02); fix the migration file at merge; follow the naming convention; hand field rows to RWB-P1-E1001-APP; carry the six platform contracts in the preconditions. |

### OTHER:Work package, story WP B2-P8-008 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13977 | RWB-PLT-E1042-CON | GAP-2540 |  | Keep metadata H at None and Ready Day 1; carry the six platform contracts as the service baseline in preconditions and fakes. |

### OTHER:Story definition document, section 1 (worked example) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13978 | RWB-PLT-E1042-CON | GAP-2150 |  | Keep RWB-E1-020 word for word and stand RWB-P3-E1042-CON beside it as the microservice example. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13980 | RWB-PLT-E1042-CON | GAP-2389 | 13 | At next plan revision add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list; keep H empty. |

### OTHER:Wave 2 build sequence (Work Package set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13981 | RWB-PLT-E1042-CON | GAP-2410 | Header | Record that a secondary slice builds against platform contracts and published fakes and reads same-service wave-1 rows through its own schema |

### OTHER:rwb-access owner, authorise model (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13983 | RWB-PLT-E1042-CON | GAP-2215 | Header | Confirm the capability area and right for the three reference-load write operations and record them in the authorise model |

### OTHER:wp/B-P4-04.md, wp/B2-P4-010.md, checks/run_all.py (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13984 | RWB-PLT-E1042-CON | GAP-2278 | Header | De-duplicate: one Work Package per AD016 slice; number CG and ASM rows once; add a plan-uniqueness check |

### OTHER:Open decisions list of the Recovery Workbench document set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-13998 | RWB-PLT-E1042-OPS | DOR-RWB-PLT-E1042-OPS-18 | find it | Record DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) with their confirmed assumptions |

### OTHER:wave-1 rwb-decision and rwb-comms DB stories (contract review) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14000 | RWB-PLT-E1042-OPS | GAP-1214 | find it | Record the local copy table and columns, the two parameter rows and read path, the two added check values with message text, the scenario and run result shape, and the 300 ms measurement point. |

### RWB-PLT-N004-OPS; RWB-PLT-E1044-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14003 | RWB-PLT-E1042-OPS | GAP-1408 | 15 | Fix chart values RWB_ENV, RWB_PARAMETER_CATALOG, RWB_PARAMETER_TTL_KEY; add a seed hook before rollout that fails on a key with no entry, owner or default; probe the start-up check. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14015 | RWB-PLT-E1043-APP | CG-ALL-1355 MSG-P3-027 text differs from the Error and Message Standard v4 | 14 | Message text left as legacy |

### OTHER:RWB-PLT-TPL (artefact coordinates); parameter-catalog.csv (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14028 | RWB-PLT-E1043-APP | GAP-1409 | 3; 13 | Record the artefact group, name and publication channel in RWB-PLT-TPL; add the cache TTL entry with default 300 to the rwb-case parameter catalog; add no change event. |

### OTHER:RWB-E2-041 (legacy story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14031 | RWB-PLT-E1043-APP | GAP-0719 | none | Record the rule-package scope for RWB-E2-041 and keep the reference-data checklist and its report with RWB-E1-043. |

### OTHER:Lists sheet of the Recovery Workbench lists workbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14033 | RWB-PLT-E1043-APP | GAP-0221 | none | Keep every list row and Source cell; record the holding service in the Owning service (D-RCV-60) and Owning schema (D-RCV-60) columns and name the serving contract in the route column. |

### OTHER:Reference tables sheet of the Recovery Workbench workbook (Table column, rows 11; OTHER:13; OTHER:14; OTHER:15 and 16) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14035 | RWB-PLT-E1043-APP | GAP-0223 | 8 | Record each row's owner from the map item behind it, name reference_row as the carrier of the message catalogue, and leave the Table cells unchanged. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20801 | RWB-PLT-E1037-CON | R-22054 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-22054', 'R-22162', 'R-22286', 'R-22289', 'R-22316', 'R-22567', 'R-28613', 'R-28624'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0013 | ACE Common contracts are not versioned or scheduled | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0081 | Owner and table of the model version in force are not stated | ACE | Resolved (directive) |
| GAP-0159 | The four authorise operations have no request, response or error schema in any source | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0160 | The sign-in permission read has two names, /me/permissions and /me/session | TechX | Resolved (directive) |
| GAP-0161 | No cache lifetime and no rule for a failed authorise call | TechX | Resolved (directive) |
| GAP-0164 | Partner roles sit in the roles table while the partner user is owned by S9 | Partner and agency manager | Resolved (directive) |
| GAP-0166 | How the six non-human actors authenticate is not stated | Security administrator | Resolved (directive) |
| GAP-0168 | The Key tab scope values do not include REGION, which the access story uses | TechX | Resolved (directive) |
| GAP-0217 | LOV-REF-TABLE carries 25 table codes in v4 but the rwb-case reference-data contract fixes twelve | Reference data administrator | Resolved (directive) |
| GAP-0219 | Two services derive no starter row: S1 rwb-valuation and S7 rwb-writeoff | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0220 | No source states which lists a service needs at its first deployment | Data architecture team | Resolved (directive) |
| GAP-0221 | Four source lists are held in another service's table although the sheet calls every list Workbench-held | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0223 | Five reference-data rows name no table, and no message table exists in the Ownership Map | Data architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0248 | The masking function and the masking policy have no stated home after the schema split | Security architect | Resolved (directive) |
| GAP-0262 | OCR text is classified Not personal while the same content at field level is Restricted | Data steward | Resolved (directive) |
| GAP-0264 | The PII log path is named PII Kafka with no owner and no separation from the business topics | Security team | Resolved (directive) |
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0696 | Legacy AC2 and BR1 load DELEGATION_LIMIT through the reference-data service, but the Ownership Map keeps delegation_limit with P4 rwb-access | Solution architect | Resolved (directive) |
| GAP-0697 | The column definitions of each reference table code and the element types of the reference resources have no source field by field | Data steward | Resolved (directive) |
| GAP-0698 | The answer of a dated read with no version in force, and the rights of the verify and the rollback, are not stated | Solution architect | Resolved (directive) |
| GAP-0719 | FSD A2.16 reports reference-data changes while the legacy story and the test cases govern rule package versions | Business analyst | Resolved (directive) |
| GAP-0778 | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0791 | The two scope operation paths, the scope predicate fields and the home of the LOV-SCOPE list are not specified for the scope app slice | rwb-access service owner with the contract owner and the architecture review | Resolved (directive) |
| GAP-0792 | The scope contract has no source for its two paths, its predicate shape, its refusal entry fields or its version rule | contract owner of rwb-access with the consuming squads and the guard library owner | Resolved (directive) |
| GAP-0822 | rwb-access rule-version load: the compile, the checks and the SIT scenario run need the Drools kit RWB-PLT-E1072-CON, which is not in this story's build list | Solution architect | Resolved (directive) |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1092 | The scope test of the notice read has no scope source in the dependencies of this story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1098 | No access guard story covers the notice read of rwb-comms | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1214 | RWB-P6-E1073-APP: the local copy table and its columns, the parameter read path, the two added check names and the local run record are not specified in the source documents | Solution architect | Resolved (directive) |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1279 | rwb-decision login, migration file and sequence, constraint and index names, standard-column Field IDs, the dictionary handover and the platform-contract carriage are not fixed by any source | Solution architect | Resolved (directive) |
| GAP-1282 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1288 | The DP table and the service baseline add platform, store and published dependencies that the metadata rows do not carry | Solution architect, P7 rwb-decision, with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1404 | Library artefact coordinates, the policy cache time to live, the authorise payload and the split of the masking read between P4's policy and P1's read are not specified | Platform library architect with the P4 rwb-access owner and the P1 rwb-source-data owner | Resolved (directive) |
| GAP-1405 | The contract shapes of the guard and masker, the /masking-policies path, the audit record shape and the failure mapping are not specified | Platform library contract owner with the P4 rwb-access contract owner | Resolved (directive) |
| GAP-1406 | The client artefact coordinates, the owner of the cache time to live, the refresh event name and the exact build-check rule set are not specified | Platform team (PLT) architect with rwb-case (P3) and the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1407 | The published catalog and value contract, the operation status codes as a library contract, the refresh event name and the start-up error surface are not specified | Platform team (PLT) contract owner with rwb-case (P3) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1408 | The chart values, the seed ordering, the probe and the alert thresholds of the library are not specified | Platform team (PLT) DevOps engineer with rwb-case (P3) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1409 | Reference-data client artefact coordinates, the cache time-to-live catalog entry, the refresh rule with no change event and the client-to-kit boundary are not specified | Platform team (PLT) architect with the rwb-case and rwb-decision owners | Resolved (directive) |
| GAP-1410 | The published reference-data client contract, the version and row data contract, the LOV-REF-TABLE code list and the no-version failure surface are not specified in a technical specification | Platform team (PLT) contract owner with the rwb-case owner | Resolved (directive) |
| GAP-1558 | The parameter and reference-data load interface is claimed by P4 in the API specification and by P3 in the default ruling | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1569 | AccessPolicyChanged and DoaLimitChanged are published by rwb-access in Architecture v5 but have no row, payload, key or refresh window in the event design | Solution architect with the platform event owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1885 | Three consumed contracts and two platform reads of the petition have no dependency row, and two of the three operation names exist in no source | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case and S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2036 | The authorise contract has no request or response shape in any source | TechX with P4 rwb-access | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2041 | Partner users moved to S9 rwb-partner, while the approving role owner stays in P4 | S9 rwb-partner with P4 rwb-access | Resolved (directive) |
| GAP-2063 | The edge components have no owner row in the Ownership Map, and section 5 needs one | Platform (RWB-PLT-EDGE) with S9 rwb-partner | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2212 | The parameter version event has no place in the rwb-case event catalogue | Solution architect | Resolved (directive) |
| GAP-2213 | The run-time read of the catalog by the other 18 services has no published operation, right or key artefact | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2214 | The target form of the names, migration numbers and catalog key that survived the monolith is not restated | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2215 | The rights of the four operations are not republished under the rwb-case ownership | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2278 | Two Work Packages write the same two story files and the same two fragments for legacy RWB-AD-016 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2296 | The daily chain check has no job row in the Batch and Scheduling Design and the workflow kit dependency is absent from the Work Package | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2312 | DP-added platform and published contracts are not in the metadata dependency rows | Solution architect, P4 | Resolved (directive) |
| GAP-2333 | The Reporting right of the legacy story, the data-lake copy of the access rule, the event row of the service and the DP dependencies disagree with the target sources | Solution architect with the rwb-access and rwb-agent owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2335 | The two DP-11 contract reads of the legacy in-process calls are absent from the Work Package dependency rows and DP-08 is not among the patterns | Solution architect | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2412 | Placement record slice: element names of the decision-record fact, the case read and the authorise call, the reference-data operation, the MSG-P7-009 text, the per-service login name and the platform contract rows are not in any source this story may read | Solution architect, rwb-decision, with the rwb-integration and rwb-case contract owners | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2540 | The plan gives this story no H row, while its migration needs the schema, the login and the Flyway pipeline of the service | Solution architect | Resolved (directive) |
| GAP-2751 | The four consumed reads and the two handed-over operations of the pack carry no dependency row, and two of the operations have no published name | Solution architect, S4 rwb-litigation, with the P5 rwb-document, P3 rwb-case and P4 rwb-access architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2801 | Four consumed surfaces of the appeal have no dependency row, and the plan carries no contract, integration or external dependency for either slice | Solution architect, S4 rwb-litigation, with the P7 rwb-decision, P3 rwb-case, S9 rwb-partner architects and the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3057 | RWB-S8-E7004-APP: the X4 slice has no plan row for its five consumed contracts, its rule kit, its ACE read, its outbox and inbox, its Aric route or its state vocabulary, and its legacy success criterion is owned by the harness | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3232 | The story catalog carries 2,534 dependency rows while the story files carry 2,609 for the same 1,034 stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
