# RWB-SVC-P4 rwb-access (Access and authority) - review pack, part 4 of 11 (RWB-P4-E1020-APP to RWB-P4-E1037-APP)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 8 |
| Resolved in the stories | 176 |
| Cross-document (pending in another document) | 151 |
| Not applied (value not in the sources) | 25 |
| Open business decisions | 28 |
| Register gaps linked | 96 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-P4-E1020-APP | 28 | 21 | 5 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1020 APP Allocation and assignment engine v1 v2.md |
| RWB-P4-E1021-APP | 27 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1021 APP Transfer rules and engine v1 v2.md |
| RWB-P4-E1022-APP | 18 | 10 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1022 APP Sign-on with SSO, MFA and the first roles v2.md |
| RWB-P4-E1022-CON | 9 | 13 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1022 CON Sign-on with SSO, MFA and the first roles - contract v2.md |
| RWB-P4-E1022-DB | 13 | 19 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1022 DB Sign-on with SSO, MFA and the first roles - ACE DB v2.md |
| RWB-P4-E1023-APP | 27 | 20 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1023 APP Case record view v1, read only v2.md |
| RWB-P4-E1028-APP | 20 | 18 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1028 APP Service levels, timers, escalation and prescription dates v2.md |
| RWB-P4-E1037-APP | 34 | 32 | 6 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1037 APP Role to permission matrix as data and PDPA field masking by role v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-P4-E1023-APP | R-10651 | CG-ALL-4970 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-22002 | GAP-0685 | Register gap | Business owner; reference data administrator | The source of the caseload cap is not fixed: parameter row or reference data | Keep the cap as versioned reference data on queue.capacity_cap and queue_member.capacity, as the legacy data model does, and add a parameter key only if a product-level override is wanted; state the ruling in the Reference Data and Parameters design. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22094 | GAP-1575 | Register gap | Compliance with the solution architect | The personal field list the masking policy must cover and the content of a masking version are not enumerated in any source | Produce the personal field register with its field IDs and its masked form per data type, the per-role unmasked list and a masking version label that names the register it belongs to, as the seed of the masking policy, and answer DL26 for it, so FR-P4-016 and FR-P4-017 are testable beyond the five fields the FSD names. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22104 | GAP-2037 | Register gap | Architecture with Compliance | Two sources disagree on who applies the mask: rwb-source-data or each service | Both controls are kept and written as defence in depth: rwb-source-data masks in the view and in its contract, and each service re-applies the masking_rule rows of rwb-access before the response leaves. The story RWB-P4-E1037-APP owns the profile; the P1 story owns the view mask. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-22105 | GAP-2136 | Register gap | Compliance | The plan does not say which service applies the mask once the masking rules are rwb-access data | rwb-access holds the approved masking version; rwb-source-data applies the mask at the 30 views; display masking at the API is applied by the service that owns the field, under the same version. |
| RWB-P4-AD005-APP, RWB-P4-AD005-CON, RWB-P4-E1022-APP, RWB-P4-E1037-CON | R-23009 | GAP-0795 | Register gap | rwb-access service owner with the security administrator role owner and the audit owner | The path and payload of the separation-of-duty check, the incident channel, the text of MSG-P4-006 and the approval route of a new conflict version are not specified for the app slice | Publish the check as POST /api/recovery/access/v1/authorise/separation-of-duty on the base of §R4 and DP-13 with a payload stated by this revision; carry the incident as the recorded refusal addressed to RW-SECADM until an incident operation exists; keep the ID MSG-P4-006 and leave its text to the business, reconciling it with RWB-P4-E1022-APP; load a version through the load path of RWB-P4-E1037-CON and let the check resolve the version in force; read the environment code through the parameters contract |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-28522 | GAP-0686 | Register gap | Business owner, Shared operations; platform team, Temporal | The exact cadence of the rebalancing trigger is not defined for rwb-case | Run JOB-06 as its own Temporal Schedule at 06:30 Asia/Bangkok, after DailyCaseRun has finished, with overlap policy SKIP and a catch-up window; confirm the order with the operations owner and record it in the Temporal Workflow and Activity Catalog. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1022-ITG, RWB-P4-E1022-APP, RWB-P4-E1022-CON, RWB-P4-E1022-DB | R-28537 | GAP-1578 | Register gap | Product owner | FEAT-ACA-15, the release checklist and go-live readiness, is a delivery activity inside the product feature list and has no product requirement | Retire FEAT-ACA-15 from the module feature list and carry the release checklist in the programme delivery plan, so the P4 feature list holds only behaviour that a product can be accepted against. |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28578 | GAP-0162 | Register gap | Product head (Mortgage, HP, SSME) | The DoA limit amounts are not in this document | v5 names the owner (P4), the table (delegation_limit) and the two operations that serve it; the amounts stay in the Delegation of Authority Matrix and the DoA rule package and no amount is copied into this document. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28579 | GAP-0163 | Register gap | Compliance and PDPA officer | The masking rules per role, area and field group are not in this document | v5 names P4 as owner of masking_rule and GET /masking-policies as the contract; the rule values stay with Compliance and are loaded as a versioned reference data set. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON | R-28585 | GAP-2048 | Register gap | P4 rwb-access with Compliance | The alert recipient roles of version 3 are not mapped to role codes in rwb-access | The six recipient names are kept as they are and read as role names; the role codes are settled with the rwb-access role model before the per-service alert rules are built, and no code is invented here. |
| RWB-ITG-E1037-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1038-APP | R-28587 | GAP-1579 | Register gap | Solution architect with Risk | No performance target covers the authorise answer, although every request passes one, and the nearest targets belong to other objects | Set one target for the authorise answer at the busiest hour, with the cache hit and the miss stated separately, and record it under DL11 beside the screen and rule-evaluation targets, so NFR-P4-001 becomes a testable number. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-P4-E1020-APP | R-05635 | DOR-RWB-P4-E1020-APP-23 | 3 | Definition of Ready item 23 Contract version fixed: Fail | API Spec v6 index.yaml gives only rest-base /api/recovery/access/v1 and document version 5.0.0, not a contract version. Placeholder added in section 3 row RWB-P4-E1037-CON. |
| RWB-P4-E1020-APP | R-16610 | DOR-RWB-P4-E1020-APP-10 | not in this chunk | Definition of Ready item 10 Screens and states: Partial | SCR-02 and SCR-03 state rows are outside this chunk. No source gives empty, loading, error or no-access states (Not specified in the source documents (DOR-RWB-P4-E1020-APP-10)). |
| RWB-P4-E1020-APP | R-25349 | CG-ALL-4922 | 13 | Flyway file V1020_1__allocation_authority_read_path.sql is not in the V0001..Vnnnn form | Migration row (line 413) is outside this chunk. The next V-number of the rwb_access Flyway sequence is not in the sources (Not specified in the source documents (CG-ALL-4922)). |
| RWB-P4-E1020-APP | R-28529 | GAP-2150 | 1 | The worked example is a monolith story key with no service and no realignment equivalent | Section 1 text is not in this chunk. Accepted fix (keep RWB-E1-020, add RWB-P3-E1042-CON beside it) waits until section 1 is in scope. |
| RWB-P4-E1020-APP | R-30847 | NEWAC-RWB-P4-E1020-APP-AC12 | 7, 16 | AC12: §8 BR1, BR3, BR4, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Sections 7 and 16 are outside this chunk, so there is no AC anchor or test row. Proposed test is Not specified in the source documents (NEWAC-RWB-P4-E1020-APP-AC12). |
| RWB-P4-E1021-APP | R-25354 | CG-ALL-4933 | 3, 3.1 | Flyway file V1021_1__transfer_authority_path.sql is not in the V0001..Vnnnn form | Migration line not in chunk; next Flyway number for rwb_access not found in Service Template Spec v1 §3.1. No number invented. |
| RWB-P4-E1022-APP | R-01203 | CG-ALL-4937 | 18 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | Ruling is closed list (Reference Data v5). The story row reading roles as data is in section 18, not in this chunk. yaml enum stays. |
| RWB-P4-E1022-APP | R-01204 | CG-ALL-4938 | 18 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | Ruling is closed list (Reference Data v5, LOV-SCOPE). The story row reading scope as data is in section 18, not in this chunk. yaml enum stays. |
| RWB-P4-E1022-APP | R-05650 | DOR-RWB-P4-E1022-APP-8 | 18 | Definition of Ready item 8 Contract: Fail | Same closed-list ruling as CG-ALL-4937/4938. The contract trace text is in section 18, not in this chunk. |
| RWB-P4-E1022-APP | R-16622 | DOR-RWB-P4-E1022-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | SCR-43 and SCR-47 are in section 10, which is not in this chunk. Nothing edited here. |
| RWB-P4-E1022-CON | R-01205 | CG-ALL-4944 | not in supplied parts | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | Ruling is closed list per Reference Data v5 (LOV-ROLE-CLASS), so yaml enum stays. The data-reading sentence is outside the supplied story parts, so no anchor for an edit. |
| RWB-P4-E1022-CON | R-01206 | CG-ALL-4945 | not in supplied parts | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | Ruling is closed list per Reference Data v5 (LOV-SCOPE), so yaml enum stays. The data-reading sentence is outside the supplied story parts, so no anchor for an edit. |
| RWB-P4-E1022-CON | R-05654 | DOR-RWB-P4-E1022-CON-8 | not in supplied parts | Definition of Ready item 8 Contract: Fail | Ruling is closed lists for roleClass and defaultScope, so yaml stays. The contradicting sentences are outside the supplied story parts, so no edit can be made here. |
| RWB-P4-E1022-CON | R-16632 | DOR-RWB-P4-E1022-CON-4 | 7 and 16 | Definition of Ready item 4 Business rules: Partial | BR1 to BR12 need criteria in section 7 and rows in section 16. Neither part is in the supplied text, so there is no anchor for an edit. |
| RWB-P4-E1022-DB | R-05655 | DOR-RWB-P4-E1022-DB-14 |  | Definition of Ready item 14 Epic design: Fail | No epic design record or sign-off for RWB-SVC-P4 or EP01 in the story or sources (Grep of 04 User stories). A sign-off cannot be recorded without inventing it. |
| RWB-P4-E1022-DB | R-25367 | CG-ALL-4957 |  | Flyway file V_E1_022__role_conflict.sql is not in the V0001..Vnnnn form | The migration name is outside this chunk, so there is no exact text to edit. Story §13 fixes V0001 then the next files, but says the owner assigns numbers at build time. |
| RWB-P4-E1023-APP | R-22028 | CG-ALL-3425 | 7 | RWB-S8-E1023-APP: the plan assigns the slice no legacy acceptance criterion while it keeps thirteen legacy test cases, and the legacy criteria lose their owned ids | AC1 to AC12 (section 7) and the section 18 mapping are not in this chunk; no current text to edit. Needs their text in a later chunk. Test cases TC-E1-023-01 to -13 already unchanged. |
| RWB-P4-E1023-APP | R-25372 | CG-ALL-4971 | 12.3 | Flyway file V1023_1__case_record_read_path.sql is not in the V0001..Vnnnn form | Migration line L394 is blank in this chunk. No rwb_access V0001-form next number found in the sources; Admin Stories v4 uses V4001-style names. Needs the Service Template §3 value. |
| RWB-P4-E1028-APP | R-25377 | CG-ALL-4983 | 3 | Flyway file V1028_1__case_read_index.sql is not in the V0001..Vnnnn form | Next rwb_access Flyway number is not in the sources (searched Service Template Spec v2 and TSD/ADR files); L390 is outside this chunk. Resend that line. |
| RWB-P4-E1037-APP | R-01217 | CG-ALL-4993 | Not in this chunk | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | LOV-ROLE-CLASS sentence is not in this chunk. Ruling: closed list per Reference Data v5 Lists. Apply in the holding chunk. |
| RWB-P4-E1037-APP | R-01218 | CG-ALL-4994 | Not in this chunk | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | LOV-SCOPE sentence is not in this chunk. Ruling: closed list per Reference Data v5 Lists. Apply in the holding chunk. |
| RWB-P4-E1037-APP | R-22098 | GAP-0164 | Not in this chunk | Partner roles sit in the roles table while the partner user is owned by S9 | PT role and partner_user text is not in this chunk. Ruling: PT rows stay with P4; partner user, instruction and result stay with S9. Apply in the holding chunk. |
| RWB-P4-E1037-APP | R-22100 | GAP-0778 | Not in this chunk | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Masking-policy path, event payload and roster count text are outside this chunk. Apply the ruling in the holding chunk; header already states base path and event name. |
| RWB-P4-E1037-APP | R-22107 | GAP-0779 | Not in this chunk | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Load path, masking path, event payload and matrix read text are outside this chunk. Apply the ruling in the holding chunk. |
| RWB-P4-E1037-APP | R-23008 | GAP-0793 | Not in this chunk | The masking-profile operations, the PII read record and the view-column naming of a masking_rule row are not specified in any source | Masking-profile operations, PII read record and view-column text are outside this chunk. Apply the ruling in the holding chunk. |

## 5. Cross-document changes (pending in the target document)


### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08039 | RWB-P4-E1020-APP | CG-ALL-4915 | find it | Remove the closed enum on defaultScope and read its values from LOV-SCOPE through the reference-data contract |
| CDC-08060 | RWB-P4-E1021-APP | CG-ALL-4927 | none | Remove the closed enum on defaultScope and accept LOV-SCOPE values as data per Reference Data v5 Lists; story unchanged. |
| CDC-08099 | RWB-P4-E1022-DB | CG-ALL-4951 | 8 | Remove the fixed roleClass enum so LOV-ROLE-CLASS values are accepted as reference data without a schema change. |
| CDC-08100 | RWB-P4-E1022-DB | CG-ALL-4952 | 8 | Remove the fixed defaultScope enum so LOV-SCOPE values are accepted as reference data without a schema change. |
| CDC-08102 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-8 | 8 | Remove the fixed roleClass and defaultScope enums so LOV-ROLE-CLASS and LOV-SCOPE are accepted as data. |
| CDC-08118 | RWB-P4-E1023-APP | CG-ALL-4962 | find it | Remove the closed enum on defaultScope so LOV-SCOPE values are accepted as data without a code change, as the story states. |
| CDC-08122 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-8 | 12 | Make defaultScope (lines 249 and 331) read LOV-SCOPE as data, not a closed enum. Catalog v1 gives AccessPolicyChanged payload as Not specified (GAP-0127; ASM-0204). |
| CDC-08138 | RWB-P4-E1028-APP | CG-ALL-4975 |  | Remove the fixed enum on defaultScope so LOV-SCOPE values are accepted as data without a code change |
| CDC-08163 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-8 | find it | Add the paths the detcheck lists: POST admin/reference-loads, POST admin/reference-loads/{loadId}/approve, GET admin/roles, GET masking-policies and three more not shown. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08043 | RWB-P4-E1020-APP | CG-ALL-4918 | 4, 14 | Add a new message ID for the text '{role} may not be held together with {role}.' for RWB-P4-E1020-APP. MSG-P4-006 keeps its standard meaning. New ID Not specified in the source documents (CG-ALL-4918). |
| CDC-08065 | RWB-P4-E1021-APP | CG-ALL-4930 | 14 | Add a new message ID for the role-conflict refusal text '{role} may not be held together with {role}.'; the story cites it once it exists |
| CDC-08104 | RWB-P4-E1022-DB | CG-ALL-4953 | 14 | Add a new message ID for a NOT NULL column empty at role or matrix load; the story then cites that ID in section 14. |
| CDC-08105 | RWB-P4-E1022-DB | CG-ALL-4954 | 4, 14 | Add a message ID for 'A matrix load names a role code the reference list does not know', distinct from MSG-P1-002; the story then cites it |
| CDC-08109 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-9 | 14 | Confirm MSG-GEN-001 meaning 'Enter {field}'; give the role-code message a new ID in place of MSG-P1-002 (CG-ALL-4954) |
| CDC-08125 | RWB-P4-E1023-APP | CG-ALL-4965 | 4, 14 | Business analyst adds a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; the story then cites it. |
| CDC-08129 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-9 | 14 | Align MSG-P4-006 to one meaning; this story uses it for a role conflict (X6, §14). |
| CDC-08143 | RWB-P4-E1028-APP | CG-ALL-4978 | 4, 14 | Add a new message ID for 'Two roles of the caller conflict' with text '{role} may not be held together with {role}.'; MSG-P4-006 keeps its standard meaning |
| CDC-08147 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-9 | 14 | Add a new message ID for the role-pair conflict text; MSG-P4-006 keeps the standard's meaning |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08052 | RWB-P4-E1020-APP | GAP-2439 | 11 | Confirm the rule_package_version columns for state, valid-from, approver, generated DRL and SHA-256 checksum; confirm the artifact payload with the embedded Drools kit of RWB-PLT-E1072-CON |
| CDC-08078 | RWB-P4-E1022-APP | DOR-RWB-P4-E1022-APP-7 | 11 | DF-REF-039 is not in LDM v9; the row is marked Not specified in the source documents (CG-ALL-4936). |
| CDC-08086 | RWB-P4-E1022-CON | CG-ALL-4943 | 11 | Add a row for DF-REF-039 on entity role (field entra_group). PRD P4 rwb-access v1 places the Entra group on role. Story section 11 row stays as is. |
| CDC-08089 | RWB-P4-E1022-CON | DOR-RWB-P4-E1022-CON-7 | 11 | Add DF-REF-039 entra_group as a field of role (P4 rwb-access), as TSD P4 v3 T3.1 defines it |
| CDC-08103 | RWB-P4-E1022-DB | CG-ALL-4950 | 3 | Record flyway_schema_history as the Flyway-managed history object of the rwb_access sequence. |
| CDC-08146 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-7 | 11 | Add field ID DF-REF-039 for the role field entra_group read from rwb_access |
| CDC-08165 | RWB-P4-E1037-APP | CG-ALL-4987 | find it | Record uk_permission_version as an index on permission (matrix_version, role_id, capability_area). |
| CDC-08166 | RWB-P4-E1037-APP | CG-ALL-4988 | find it | Record uk_masking_rule as an index on masking_rule (role_code, field_id, masking_version) from baseline V0001. |

### RWB-P4-E1037-CON (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08072 | RWB-P4-E1021-APP | GAP-0990 | 5 | Publish the authorise request and answer schema with legalHold; confirm the matrix version label with the matrix owner; tabulate Queue and allocation letters in T6.1 |
| CDC-08082 | RWB-P4-E1022-APP | GAP-0791 | 8 | BR12 session-sourced team and region sentence removed |
| CDC-08161 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-21 | header | Complete the build to Done and publish the contract. |
| CDC-08162 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-22 | header | Publish a contract fake library version for RWB-P4-E1037-CON. |
| CDC-08176 | RWB-P4-E1037-APP | GAP-0159 |  | Publish the OpenAPI document for POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies with operation IDs, bodies, status codes and error model; mark bodies as placeholder until then. |
| CDC-08177 | RWB-P4-E1037-APP | GAP-0160 |  | Map GET /me/session to GET /me/permissions as the contract name and record the rename in the API catalogue. |
| CDC-08181 | RWB-P4-E1037-APP | GAP-2036 |  | Write request and response shapes, error codes and cache-refresh behaviour for POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies, and add Endpoints rows in the Ownership Map. |
| CDC-08186 | RWB-P4-E1037-APP | GAP-0248 | 2 | State that the masking function stays in the recovery view schema with the views and that rwb-source-data applies the mask in the view and in its responses. This story now states its own part (policy rows in rwb_access). |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08053 | RWB-P4-E1020-APP | CG-ALL-4921 | 18 | Align the test lists of REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and the fourth requirement with RWB-P4-E1020-APP section 18 in the next version |
| CDC-08071 | RWB-P4-E1021-APP | CG-ALL-4932 | 18 | Align the test lists of REQ-CWC-010, REQ-CWC-016, REQ-WKM-003 and REQ-CWC-005 with section 18 of RWB-P4-E1021-APP (owner QA). |
| CDC-08084 | RWB-P4-E1022-APP | CG-ALL-4939 | 18 | Align the REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 test lists with section 18 of RWB-P4-E1022-APP in the next version. |
| CDC-08098 | RWB-P4-E1022-CON | CG-ALL-4947 | 18 | Align the test lists of REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 to RWB-P4-E1022-CON section 18 (TC-P4-E1022-CON-02 to -05) in its next version. |
| CDC-08117 | RWB-P4-E1022-DB | CG-ALL-4956 | 18 | In the next versions, align the §18 and RTM v7 test lists for REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010. |
| CDC-08136 | RWB-P4-E1023-APP | CG-ALL-4969 | 18 | Align the test lists for the five requirements, including REQ-OCC-007 and REQ-RDF-009, with RWB-P4-E1023-APP section 18 in the next version |
| CDC-08183 | RWB-P4-E1037-APP | CG-ALL-4997 | 18 | Align the test lists of the six requirements (REQ-ACA-003, REQ-ACA-005 and others) with RWB-P4-E1037-APP section 18 at the next RTM version. |

### Epic design record (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08040 | RWB-P4-E1020-APP | DOR-RWB-P4-E1020-APP-14 | find it | Record the signed epic design sign-off for RWB-P4-E1020-APP |
| CDC-08061 | RWB-P4-E1021-APP | DOR-RWB-P4-E1021-APP-14 | Metadata | Record the signed epic design sign-off for this story; no signed design is in the source documents. |
| CDC-08120 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-14 | find it | Record the signed epic design sign-off for RWB-P4-E1023-APP and confirm it against this story. |
| CDC-08140 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-14 |  | Record the signed epic design sign-off for RWB-SVC-P4 against this story |
| CDC-08160 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-14 | header | Confirm and record the signed epic design sign-off for RWB-P4-E1037-APP. |

### RWB-P4-E1022-CON (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08076 | RWB-P4-E1022-APP | DOR-RWB-P4-E1022-APP-21 | header | Set build status to Done (currently Not started) before this story relies on the published contract. |
| CDC-08077 | RWB-P4-E1022-APP | DOR-RWB-P4-E1022-APP-22 | header | Publish the contract fake library and record its version as published. |
| CDC-08081 | RWB-P4-E1022-APP | GAP-0776 | 12 | Section 12 names POST authorise and GET me/permissions under the R4 base and DP-13; payloads deferred to RWB-P4-E1022-CON. |
| CDC-08101 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-21 | header | Publish the contract so the build status moves from Not started to Done. |
| CDC-08113 | RWB-P4-E1022-DB | GAP-0776 | - | Publish POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions under the section R4 base, with contract-stated payloads and two version labels per answer. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08097 | RWB-P4-E1022-CON | CG-ALL-4946 | 16 | Add Story test cases rows for TC-P4-E1022-CON-01 to -05, with Given, When and Then copied from AC1 to AC6 of section 7; TC-P4-E1022-CON-06 and -07 from AC10 and AC11. |
| CDC-08116 | RWB-P4-E1022-DB | CG-ALL-4955 | 16 | Add rows for TC-P4-E1022-DB-01 to TC-P4-E1022-DB-07, with Given, When and Then copied from AC1 to AC7. |
| CDC-08126 | RWB-P4-E1023-APP | CG-ALL-4966 | 16 | Add rows TC-E1-023-12 and TC-E1-023-13 with Given, When and Then copied from the story's Covers and Data cells. |
| CDC-08144 | RWB-P4-E1028-APP | CG-ALL-4979 | 16 | Add a row for TC-E1-028-14 with Given, When and Then copied from AC1, the criterion it covers |
| CDC-08168 | RWB-P4-E1037-APP | CG-ALL-4996 | 16 | Add rows TC-E1-037-13, TC-E1-037-14 and TC-E1-037-15 with Given, When and Then copied from criteria AC11, AC12 and AC13. |

### API:(service not named) (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08045 | RWB-P4-E1020-APP | GAP-0345 | find it | Publish the JOB-03 step state on the rwb-case run result; keep the catalogue read and rerun on the P1 job catalogue; fix the rerun facade for a workflow step before wave 1 exit. |
| CDC-08080 | RWB-P4-E1022-APP | GAP-1568 | 12 | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, version fields and masking marker vocabulary. |
| CDC-08094 | RWB-P4-E1022-CON | GAP-0776 | find it | Publish POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions with their payloads and the two version labels |
| CDC-08111 | RWB-P4-E1022-DB | GAP-1568 | - | Publish the four rwb-access operations with request and answer schemas, refusal and not-found codes, version fields and masking vocabulary; state the group-to-role read and session retirement in TSD P4 T3.1. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08047 | RWB-P4-E1020-APP | GAP-2443 | find it | Add the rule package artifact operation to the P7 row and the API Specification with the same base, the model-owner identity and the checksum in the answer. |
| CDC-08153 | RWB-P4-E1028-APP | GAP-0022 | find it | Keep PLT as owner of retired EV-18 TimerDue; keep P3 as owner of EV-19 TimerBreached. |
| CDC-08185 | RWB-P4-E1037-APP | GAP-2039 | 3 | Add access_log to the Tables sheet owned by P4 rwb-access with its key and retention class, and its own DB story in RWB-SVC-P4. |
| CDC-08187 | RWB-P4-E1037-APP | GAP-2063 | 2 | Add component rows for gateway-bff and the partner gateway, owner RWB-PLT-EDGE, with S9 rwb-partner behind the partner gateway, at the next revision. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08064 | RWB-P4-E1021-APP | CG-ALL-4928 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 in the Events row (gap-0127; asm-0204), then align section 12.3 to it |
| CDC-08124 | RWB-P4-E1023-APP | CG-ALL-4963 | 12.3 | Define the payload of rwb.access.AccessPolicyChanged.v1 (policy kind, version label, valid-from date, change reference) as in story section 12.3 (gap-0127). |
| CDC-08142 | RWB-P4-E1028-APP | CG-ALL-4976 | 12.3 | Specify the payload of rwb.access.AccessPolicyChanged.v1 (gap-0127; asm-0204) so the story payload can be aligned |
| CDC-08167 | RWB-P4-E1037-APP | CG-ALL-4995 | 12.3 | Add to the rwb.access.AccessPolicyChanged.v1 Events row the payload of section 12.3: change kind, version label, effective date and approver reference; no field value, person or case. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08088 | RWB-P4-E1022-CON | DOR-RWB-P4-E1022-CON-12 | 16, 18 | Register TC-P4-E1022-CON-01 to TC-P4-E1022-CON-05 in Test Cases v8; align the REQ-ACA test lists in RTM v7 with section 18 of RWB-P4-E1022-CON. |
| CDC-08107 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-12 | 12.7, 16, 18 | Register TC-P4-E1022-DB-01 to -07 in Test Cases v8; align the §18 test lists with RTM v7 |
| CDC-08119 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-12 | 16 | AC2 (TC-14), AC5 (TC-15, -17) and AC9 (TC-16, -18) are covered; TC-05 now maps AC3. TC-26 and TC-27 are placeholders; TC-27 carries no ASM ID. |
| CDC-08139 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-12 | 12, 16 | Add test rows TC-E1-028-14 to TC-E1-028-17 for this key; RTM v7 to list the same section 18 test cases |

### RWB-P4-E1037-CON; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08156 | RWB-P4-E1037-APP | CG-ALL-4989 | 12.1 | Publish POST /api/recovery/access/v1/admin/reference-loads in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08157 | RWB-P4-E1037-APP | CG-ALL-4990 | 12.1 | Publish POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08158 | RWB-P4-E1037-APP | CG-ALL-4991 | 12.1 | Publish GET /api/recovery/access/v1/admin/roles in rwb-access.yaml through RWB-P4-E1037-CON. |
| CDC-08159 | RWB-P4-E1037-APP | CG-ALL-4992 | 12.1 | Publish GET /api/recovery/access/v1/masking-policies in rwb-access.yaml through RWB-P4-E1037-CON. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08042 | RWB-P4-E1020-APP | DOR-RWB-P4-E1020-APP-8 | 12.3 | Hold defaultScope as a LOV-SCOPE reference, not a closed enum; use the Kafka Catalog v1 event name rwb.decision.DecisionRecorded.v1 and the catalog payload for AccessPolicyChanged. |
| CDC-08063 | RWB-P4-E1021-APP | DOR-RWB-P4-E1021-APP-8 |  | rwb-access.yaml: event type of the decision record as rwb.decision.DecisionRecorded.v1; defaultScope reads LOV-SCOPE as data, not a closed enum; AccessPolicyChanged payload aligned with the catalog (CG-ALL-4928) |
| CDC-08141 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-8 | 12.3 | yaml: remove the fixed defaultScope enum (CG-ALL-4975). Catalog: specify the AccessPolicyChanged payload (CG-ALL-4976). Story event type already fixed. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08087 | RWB-P4-E1022-CON | DOR-RWB-P4-E1022-CON-1 | 1 | Add 'contract owner of rwb-access' as a role code or role name, or the story in section 1 is changed to an existing role code. |
| CDC-08106 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-1 | 1 | Add 'ACE database engineer' as a role name in Users Roles and Permissions v5 |
| CDC-08169 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-1 | 1 | Add a role code or name for 'product owner', or name the role code the story means. |

### RWB-P3-E1028-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08145 | RWB-P4-E1028-APP | DOR-RWB-P4-E1028-APP-10 | 4 | Add empty, loading, error and no-access states for SCR-03 and SCR-09 |
| CDC-08149 | RWB-P4-E1028-APP | GAP-2016 | 3 | Make the durable timer authoritative; the timer row is the audit copy written by ApplyStateActivity in the same transaction as the state, and read back on reopen. |
| CDC-08150 | RWB-P4-E1028-APP | GAP-0353 | 3, 16 | Assert timer via GET /api/recovery/case/v1/cases/{caseId}/timers, breach on rwb.case.events.v1, decision record in P7; prove catch-up by pausing the worker; P1 inputs proved there; no TimerDue asserted. |

### RWB-S8-E1020-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08048 | RWB-P4-E1020-APP | GAP-3072 | find it | Publish the case element and stage outcome of RWB-P3-E1020-CON, the queue-and-members element, the handler rule, the DEV-HANDLER parameter row and the four handler role codes. |
| CDC-08058 | RWB-P4-E1020-APP | GAP-3073 | 1 | Keep wave 1 and the tentative date; use the event names DeviationRaised and DeviationCleared with consumers from TSD S8 T0.2 and T5.2.1; build behind the service baseline with no element of its own; treat DP platform contracts as wave 0 preconditions. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08108 | RWB-P4-E1022-DB | DOR-RWB-P4-E1022-DB-7 | 11 | LDM v9: confirm DF-REF-039 for role.entra_group; add flyway_schema_history to LDM v9 or Data Classification v5 |
| CDC-08128 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-7 | 11 | Define DF-REF-039 as role.entra_group; confirm or remove P2 names id_no_token and value_token as fields or entities. |

### RWB-P4-E1039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08134 | RWB-P4-E1023-APP | GAP-0694 | 8 | Publish the masking policy request and response keyed by view field ID with a masked flag and the source column per field. |
| CDC-08173 | RWB-P4-E1037-APP | GAP-0355 |  | Name the read-back contract for the AC-EXPT export entry, the masking source for the xlsx as P4 rules over the P1 masked columns, and the owner display name path from the ACE user directory. |

### RWB-PLT-E1037-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08179 | RWB-P4-E1037-APP | GAP-1404 |  | Publish the library artefact at a platform coordinate with major version 1, hold the cache time to live in a parameter read through the parameters client, and publish the authorise and masking-policy payloads. |
| CDC-08180 | RWB-P4-E1037-APP | GAP-1405 |  | Publish the guard, scope guard, mask applier and annotation contract shapes, and the audit record as case id, field id and flag, with failure mapping to 503 with no business data. |

### RWB-P3-E1020-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08041 | RWB-P4-E1020-APP | DOR-RWB-P4-E1020-APP-22 | find it | Publish the contract fake library and record its version |

### RWB-P4-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08044 | RWB-P4-E1020-APP | DOR-RWB-P4-E1020-APP-9 | 14 | Align the meaning of MSG-P4-006 in P2 with the standard, or rename the P2 message so that its meaning is not reused; this story's section 14 row is unchanged. |

### OTHER:Service Catalog and RWB-PLT-DB stories (19-schema list) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08046 | RWB-P4-E1020-APP | GAP-0684 | find it | Allocate the rwb-case service login with schema rwb_case, derive the name from the schema, store it in Key Vault and record it in the Service Catalog before first deployment. |

### OTHER:RWB-PLT-DB and the rwb-case DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08049 | RWB-P4-E1020-APP | GAP-3207 | find it | Publish the per-service rwb-case login there; keep the placeholder in RWB-P3-E1020; keep caseload cap as queue.capacity_cap and queue_member.capacity with the default from the parameter contract. |

### RWB-P3-E1020-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08050 | RWB-P4-E1020-APP | GAP-3208 | find it | State the Temporal cron expression for DailyCaseRun, keep the AceDataReady event start as primary with one catch-up Schedule per business date (overlap SKIP), and keep 07:00 Asia/Bangkok as the alert deadline. |

### RWB-PLT-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08051 | RWB-P4-E1020-APP | GAP-2441 | find it | Carry the business date as a record attribute and the queue and owner identifiers as named members of the actions payload, fixed at the envelope contract review. |

### OTHER:Work package C-WEX (work package index) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08054 | RWB-P4-E1020-APP | GAP-3206 | - | Correct the heading (E1-018) to RWB-E1-020 at the next run; read the label as scheduling only and keep RWB-E1-020 as the subject |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08055 | RWB-P4-E1020-APP | GAP-3209 | - | Add one criterion-ownership column listing, for each legacy criterion of RWB-E1-020, the single new story that owns it |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08056 | RWB-P4-E1020-APP | GAP-0687 | - | Record SIT findings for the rwb-case allocation worker topology; expose replicas, autoscaling bounds, node pool, connection pool size and history archive as chart values with documented defaults |

### OTHER:P7 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08057 | RWB-P4-E1020-APP | GAP-2442 | 14 | Approve wording for MSG-P7-009 and the chain-break warning, and name the per-entry chain-result field. The ID and the named field stay as they are. |

### OTHER:Build Notes v6 (wave plan and service epic for rwb-deviation) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08059 | RWB-P4-E1020-APP | GAP-3173 | header | State the wave 1 delivery of rwb-deviation in the service epic and wave plan, and let the rwb-deviation service wave (2) govern its later stories. |

### RWB-P4-E1037-CON; RWB-P3-E1021-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08062 | RWB-P4-E1021-APP | DOR-RWB-P4-E1021-APP-22 | Metadata | Publish the fake library and record its version as published; no fake version is in the source documents. |

### RWB-P3-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08066 | RWB-P4-E1021-APP | GAP-0346 | 3 | Assert TRF-002 route-decided trigger on rwb.case.CaseStateChanged.v1 in wave 1; assert S1 RouteDecided announcement separately in wave 3. |

### RWB-P3-E1021-CON; RWB-P4-E1037-CON; OTHER:contracts of P1; OTHER:P4; OTHER:P7 and S8 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08067 | RWB-P4-E1021-APP | GAP-3076 | 3 | Each owner publishes its operation name for the consumed row before the release date; placeholders are replaced in a minor contract version. |

### RWB-S8-E1021-APP; OTHER:rwb.case.events.v1; OTHER:rwb.source-data.events.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08068 | RWB-P4-E1021-APP | GAP-3079 | 3 | P3 and P1 publish case-trigger event names on the two topics before the release date; the S8 consumer groups bind to them. |

### RWB-S8-E1021-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08069 | RWB-P4-E1021-APP | GAP-3080 | 3 | The rule ID, package version and from and to queue and owner are recorded in the DP-03 decision record; the case-side label stays with P3. |

### RWB-PLT-NF06-DB; OTHER:P3 DB story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08070 | RWB-P4-E1021-APP | GAP-0688 | 3 | The ACE DB team names the rwb-case database login and its grant set; the chart takes it by vault secret reference. |

### OTHER:Platform team chart values for rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08073 | RWB-P4-E1021-APP | GAP-0691 |  | Publish cluster, node pool, replica counts, ingress host, resource limits and disruption budget as chart values, with no environment default |

### OTHER:P5 contract baseline story for rwb.document.events.v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08074 | RWB-P4-E1021-APP | GAP-1036 |  | Publish producer AsyncAPI 3.0 and registered JSON schemas for DocumentStored.v1 and DocumentFieldsExtracted.v1 with the BACKWARD rule; hand the DocumentStored schema to RWB-P3-E1021-CON |

### RWB-PLT-NF06-DB; OTHER:P5 database story and service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08075 | RWB-P4-E1021-APP | GAP-1037 |  | Allocate the rwb-document login name, its grants (schema rwb_document only) and its secret reference |

### 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08079 | RWB-P4-E1022-APP | GAP-3103 | 11 | Publish the partner_user fields in the T3.1 catalogue and the PRD; name the contract-end Schedule and its clock; decide whether a recall is announced by an event. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08083 | RWB-P4-E1022-APP | GAP-0807 | header | Add RWB-PLT-E1071-CON to Depends on (build) and DP-10 to Patterns applied; set the cron as deployment configuration under the DL38 placeholder; create the Schedule in its operations story. |

### OTHER:Work Package files B-P4-02 and B2-P4-004 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08085 | RWB-P4-E1022-APP | GAP-2269 | none | Remove RWB-AD-005 from the B-P4-02 fanout or retire B2-P4-004 for this key; number CG-B-P4-02-AD005-1 and -2 and ASM-B-P4-02-AD005-1 to -13 once. |

### OTHER:Technical Solution Design S9; 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08090 | RWB-P4-E1022-CON | GAP-3104 | find it | Publish a PartnerUser element or confirm table-only; publish the rwb-access operation names; map EV-20 and EV-21 to their names |

### OTHER:Technical Solution Design S9; OTHER:Functional Specification S9 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08091 | RWB-P4-E1022-CON | GAP-3103 | find it | Publish partner_user fields in TSD S9 T3.1 and the PRD; name the contract-end Schedule and clock; decide whether recall is announced by an event |

### API:(service not named); OTHER:Technical Solution Design P4 appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08092 | RWB-P4-E1022-CON | GAP-1568 | find it | Publish POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies with request and answer schemas, refusal and not-found codes, and version fields |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; OTHER:Technical Solution Design P4 (gateway-bff) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08093 | RWB-P4-E1022-CON | GAP-0347 | find it | Fix the short-lived user JWT claims (Entra ID object reference, session ID, amr) and enforce the amr mfa check at gateway-bff before any owner call |

### OTHER:Technical Solution Design P4; OTHER:sign-on app slice source documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08095 | RWB-P4-E1022-CON | GAP-0775 | 8 | Session home is not specified in the sources. BR3 is kept as it was. Team and region read sit outside this chunk. |

### RWB-P4-E1022-DB; OTHER:P1 data contract (ACE v_ace_iam_group) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08096 | RWB-P4-E1022-CON | GAP-0777 | find it | Grant to a login named rwb_access per the section R4 pattern; keep mapping rows in role.entra_group; read ACE group facts only through the P1 contract |

### OTHER:TSD S9 T3.1 and PRD (S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08110 | RWB-P4-E1022-DB | GAP-3103 | - | Publish partner_user fields in TSD S9 T3.1; name the contract-end Schedule and clock; decide the recall event; confirm the feature the T8 rows serve. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08112 | RWB-P4-E1022-DB | GAP-0347 | - | Fix the user JWT claim set (Entra object reference, session ID, amr); enforce the amr mfa check at gateway-bff, repeated by rwb-access on session resolve. |

### RWB-P3-E1019-CON; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08114 | RWB-P4-E1022-DB | GAP-0775 | - | rwb-access resolves per call and hands role set, scope and two version labels to the edge; conflict incident rides refusal with ROLE_CONFLICT; team and region read via the RWB-P3-E1019-CON roles-and-teams operation. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08115 | RWB-P4-E1022-DB | GAP-3194 | - | Raise one ACE DB story each for S2, S4, S5, S6, S7, P6 and P8 for the column drop; cite the chosen story on row 121 before wave 2. |

### RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08121 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-22 | find it | Publish the contract fake library and record its version as published. |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08123 | RWB-P4-E1023-APP | GAP-0693 | find it | Publish the gateway-bff composite route for SCR-03: path, parallel call set, merge field map, 2 s budget split and partial-failure rule. Keep the five rwb-case read operations unchanged. |

### RWB-P3-E1023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08127 | RWB-P4-E1023-APP | DOR-RWB-P4-E1023-APP-10 | 4 | State the empty, loading, error and no-access states of SCR-03 Case record in its story. |

### OTHER:Business requirements document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08130 | RWB-P4-E1023-APP | GAP-1456 |  | State in section 8.2 that Epic 1 stories keep the business-epic wave; delivery lead confirms the wave per story at build sequencing. |

### RWB-ITG-E1023-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08131 | RWB-P4-E1023-APP | GAP-0348 |  | Fix the case-scoped deviation read, treat rwb-deviation as available in SIT for the wave 1 run, and keep the W1J01 synthetic fixture. |

### OTHER:RWB-PLT-DB; OTHER:rwb-case story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08132 | RWB-P4-E1023-APP | GAP-0692 |  | Name the rwb-case login per DP-02 from RWB-PLT-DB when issued; grant SELECT, INSERT and UPDATE on schema rwb_case only. |

### OTHER:rwb-source-data contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08133 | RWB-P4-E1023-APP | GAP-0695 | 8 | Add the interaction read with its path and page and size parameters; fix timeline default order as occurred_at descending with page size from a parameter. |

### RWB-S8-E1023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08135 | RWB-P4-E1023-APP | GAP-3081 | 3 | Publish the five read paths with the shapes of legacy RWB-E1-023 section 12 and the RWB-P3-E1023-CON error envelope; confirm the consumed placeholders with their owners before the tag |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; RWB-P3-E1023-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08137 | RWB-P4-E1023-APP | GAP-0989 | 3 | Authorise attribute set restored to Not specified (GAP-0989; ASM-1735). Masked-by-default and PM/MASK version wording kept. |

### RWB-P3-E1028-CON; OTHER:A2.16 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08148 | RWB-P4-E1028-APP | GAP-1623 | 3 | Record that the Waiting approval state move and the approval task are a P3 reaction to ApprovalRequested (preferred), not a call from this service; align A2.15 and A2.16. |

### RWB-P3-E1028-CON; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08151 | RWB-P4-E1028-APP | GAP-2202 | 12.2 | Add the two P1 rows (accountDates, holidays) with query and answer shape to the Ownership Map; record in the P3 contract which operation carries the wave 1 pause. |

### RWB-P3-E1028-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08152 | RWB-P4-E1028-APP | GAP-2203 | 3 | Add escalated_to_role and escalated_at columns and the TimerBreached payload fields to the logical model and event catalogue; settle detail in baseline review. |

### API:(service not named); OTHER:policy pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08154 | RWB-P4-E1028-APP | GAP-0986 | 5, 8 | Interim scope rule kept with the Not specified marker restored; matrix version label left out |

### OTHER:rwb-case values files and runbook (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08155 | RWB-P4-E1028-APP | GAP-2204 | find it | Set poll window, catch-up window, breach band and record-failure rate; confirm at UAT; record agreed values in the runbook entry each alert links. |

### OTHER:Not specified in the source documents (GAP-0013) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08164 | RWB-P4-E1037-APP | GAP-0013 | find it | Version the six ACE Common contracts and run contract tests on both sides from wave 1; owner ACE team. |

### RWB-P4-E1037-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08170 | RWB-P4-E1037-APP | DOR-RWB-P4-E1037-APP-10 | find it | Give SCR-43 and SCR-47 empty, loading, error and no-access states in the story that owns those screens. |

### OTHER:TSD P1 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08171 | RWB-P4-E1037-APP | GAP-0481 | 11 | T3.6: masking_rule owned by rwb-access; P1 holds data_product_access only and takes masking answers from POST /api/recovery/access/v1/authorise and the FieldMasker interface of RWB-P4-E1037-CON, one hop, 2 s timeout |

### API:(service not named); OTHER:TSD P4 v3 appendix T-A and T3.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08172 | RWB-P4-E1037-APP | GAP-1568 | 12 | Publish the four rwb-access operations with request, answer, refusal and not-found schemas; state group-to-role resolution in T3.1 |

### OTHER:TSD P3 v3 T-A.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08174 | RWB-P4-E1037-APP | GAP-2208 |  | Add team as an optional filter on API-P3-001 to match API-P3-017 and legacy section 12; resolve owner display name at the edge against the ACE user directory. |

### RWB-P7-E2041-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08175 | RWB-P4-E1037-APP | GAP-2414 |  | Add to its metadata the eight platform and four published contracts the DP table names, and set its build dependency list from that table. |

### OTHER:Data model v4 Fields tab (rows DF-DOC-089 and DF-DOC-015) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08178 | RWB-P4-E1037-APP | GAP-0262 | Not in this chunk | Data steward to set one classification for document_text.text_content (DF-DOC-089) and document_field.field_value (DF-DOC-015) so the two rows agree. Story rule (never in event, workflow input or log; page id only in log) applies in the holding chunk. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08182 | RWB-P4-E1037-APP | GAP-1569 |  | Add AccessPolicyChanged and DoaLimitChanged with CloudEvents type, topic rwb.access.events.v1, key, payload, versioning and refresh window; change T5.3 from None to the two events. |

### OTHER:Security and Access Design v4 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-08184 | RWB-P4-E1037-APP | GAP-2035 | 7 | Write section 7 per service: one login rwb_<short> per service with grants on its own schema only, view grant held by rwb_source_data alone, and recovery_svc row replaced by a service login isolation row. |

### 05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-case.asyncapi.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20585 | RWB-P4-E1021-APP | R-22013 |  | Target is story RWB-S8-E1021-APP; consumer-group binding to the case-trigger topics belongs to the S8 story, not this spec. |

### 05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20714 | RWB-P4-E1037-APP | R-22054 |  | write failed: DISPOSITION INCOMPLETE: no row for ['R-21918', 'R-22054', 'R-22286', 'R-22289', 'R-22316', 'R-28613'] |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0013 | ACE Common contracts are not versioned or scheduled | ACE team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0022 | TimerDue owner recorded as P3 and as PLT | Solution architect | Resolved (directive) |
| GAP-0064 | Wave conflict S8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0159 | The four authorise operations have no request, response or error schema in any source | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0160 | The sign-in permission read has two names, /me/permissions and /me/session | TechX | Resolved (directive) |
| GAP-0161 | No cache lifetime and no rule for a failed authorise call | TechX | Resolved (directive) |
| GAP-0164 | Partner roles sit in the roles table while the partner user is owned by S9 | Partner and agency manager | Resolved (directive) |
| GAP-0166 | How the six non-human actors authenticate is not stated | Security administrator | Resolved (directive) |
| GAP-0168 | The Key tab scope values do not include REGION, which the access story uses | TechX | Resolved (directive) |
| GAP-0248 | The masking function and the masking policy have no stated home after the schema split | Security architect | Resolved (directive) |
| GAP-0262 | OCR text is classified Not personal while the same content at field level is Restricted | Data steward | Resolved (directive) |
| GAP-0264 | The PII log path is named PII Kafka with no owner and no separation from the business topics | Security team | Resolved (directive) |
| GAP-0345 | JOB-03 run surface and exact rerun facade are not specified for an ITG suite | Service owner of rwb-case with the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0347 | Claims of the short-lived user JWT and the place of the multi-factor gate are not fixed | Service owner of rwb-access; platform owner of gateway-bff | Resolved (directive) |
| GAP-0348 | RWB-E1-023 integration slice: the S8 deviation read path, the wave of rwb-deviation and the fixture composition are not fixed by the sources | TechX | Resolved (directive) |
| GAP-0353 | E1028 durable timers replace JOB-05 and the P1 account-date path leaves the slice | Solution architect | Resolved (directive) |
| GAP-0355 | Export access entry, masking source and owner display name path are not named for the target | Tech lead | Resolved (directive) |
| GAP-0358 | Matrix load owner, masking read path and the platform library boundary are not named for the target | Solution architect | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0584 | Two sources give the masking of a ledger field to two different services | Tech lead | Resolved (directive) |
| GAP-0684 | The rwb-case service login name is not given in any source | ACE team, DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0687 | The deployment topology of the rwb-case allocation worker is not specified | Platform team; DevOps | Resolved (directive) |
| GAP-0688 | Per-service database login name for rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0691 | Deployment topology of the transfer capability is not specified | Platform team | Resolved (directive) |
| GAP-0692 | The per-service database login name for rwb-case is not given | ACE DB owner | Resolved (directive) |
| GAP-0693 | The gateway-bff composite route specification for SCR-03 is not given | Solution architect | Resolved (directive) |
| GAP-0694 | The exact field masking contract shape is not given | P4 access owner | Resolved (directive) |
| GAP-0695 | The timeline paging and the interaction ledger read operation are not given | P1 source data owner | Resolved (directive) |
| GAP-0775 | The home of the resolved session labels, the target of the conflict incident and the team and region read behind the scope line are not specified for the sign-on app slice | rwb-access service owner with the architecture review | Resolved (directive) |
| GAP-0776 | The two operation paths and their request and answer payloads are not specified by any source for the access contract of rwb-access | contract owner of rwb-access with the consuming squads | Resolved (directive) |
| GAP-0777 | The rwb-access login name, the ACE group source behind a mapping row and the column set of the three library objects are not specified for the schema slice | ACE database engineer with the rwb-access service owner and the P1 data owner | Resolved (directive) |
| GAP-0778 | Missing and conflicting values in the rwb-access matrix and masking slice (RWB-P4-E1037-APP) | Solution architect | Resolved (directive) |
| GAP-0779 | The load, approve and masking-policy contract of rwb-access has a missing path and a conflicting owner (RWB-P4-E1037-CON) | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0791 | The two scope operation paths, the scope predicate fields and the home of the LOV-SCOPE list are not specified for the scope app slice | rwb-access service owner with the contract owner and the architecture review | Resolved (directive) |
| GAP-0793 | The masking-profile operations, the PII read record and the view-column naming of a masking_rule row are not specified in any source | Solution architect | Resolved (directive) |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0876 | Where a correction is applied and where an erasure removes a field are not assigned | Solution architect, with the data steward | Resolved (directive) |
| GAP-0896 | rwb-access sandbox seed: the owner, the key format and the retirement rule of the DEV synthetic test identity per role are not specified | Platform administrator | Resolved (directive) |
| GAP-0975 | Which story owns the DDL of the five rwb_access authority tables is stated twice | Solution architect with the TechX tech lead | Resolved (directive) |
| GAP-0986 | rwb-access timer and case read: the authorise request attribute set, the label of the matrix version in force and the scope that prevails under an escalation are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0987 | Authority attributes, matrix version label and role roster for an allocation and queue read | Solution architect of rwb-access | Resolved (directive) |
| GAP-0989 | The authorise attribute set, the policy version labels and the full field-ID roster of the read-only case record view are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1245 | Scope predicate and Compliance incident queue of the audit read have no owner document | Solution architect, with the P4 access owner and the P3 case owner | Resolved (directive) |
| GAP-1404 | Library artefact coordinates, the policy cache time to live, the authorise payload and the split of the masking read between P4's policy and P1's read are not specified | Platform library architect with the P4 rwb-access owner and the P1 rwb-source-data owner | Resolved (directive) |
| GAP-1405 | The contract shapes of the guard and masker, the /masking-policies path, the audit record shape and the failure mapping are not specified | Platform library contract owner with the P4 rwb-access contract owner | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1564 | The load, verify, approve and rollback surface of the permission matrix and the delegation of authority table is rwb-case's under the Ownership Map, while the tables and every validation rule that decides a refusal are rwb-access's | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1569 | AccessPolicyChanged and DoaLimitChanged are published by rwb-access in Architecture v5 but have no row, payload, key or refresh window in the event design | Solution architect with the platform event owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2035 | The source keeps one recovery schema and one recovery_svc login; Architecture v5 has 19 schemas and 19 logins | Architecture with the ACE DBA | Resolved (directive) |
| GAP-2036 | The authorise contract has no request or response shape in any source | TechX with P4 rwb-access | Resolved (directive) |
| GAP-2039 | The access log is named as an rwb_access object but has no row in the Ownership Map | P4 rwb-access with the ACE DBA | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2041 | Partner users moved to S9 rwb-partner, while the approving role owner stays in P4 | S9 rwb-partner with P4 rwb-access | Resolved (directive) |
| GAP-2063 | The edge components have no owner row in the Ownership Map, and section 5 needs one | Platform (RWB-PLT-EDGE) with S9 rwb-partner | Resolved (directive) |
| GAP-2076 | The versions in force in the access log come from two services | Service owners P4 rwb-access and P7 rwb-decision | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2202 | The account-date and holiday reads and the deviation pause have no published surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2203 | No source gives the field-level detail of the two escalation columns or of the TimerBreached payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2204 | No source gives the operational values for a durable timer: poll window, catch-up window, breach band and record-failure rate | DevOps lead | Resolved (directive) |
| GAP-2208 | Four target-side facts of the case list and its export are not fixed by any source, and the sources disagree on the team filter | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2269 | Two Work Packages write the same two story files and two fragments for legacy RWB-AD-005 on rwb-access | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2300 | Three sources disagree on who holds the right to work a data subject request | Security administrator | Resolved (directive) |
| GAP-2304 | The access-change record code, the matrix version label, the matrix screen, the agent identity source and the grant's service event are not in the sources, and two sources disagree on the group column of a role and on the right of the path | Solution architect | Resolved (directive) |
| GAP-2414 | The metadata rows name no build dependency and the P3 contract only, while the DP table adds eight platform contracts and four published contracts, and the registry operations this story amends sit in another lane of the same service | Delivery lead | Resolved (directive) |
| GAP-2439 | The physical columns of rule_package_version and the payload a compiled package is served in are not in the sources | TechX and the P7 solution architect | Resolved (directive) |
| GAP-2440 | The rule ID of the same allocation row is ALLOC-014 in the legacy story and ALLOC-MTG-BKK-01 in the FSD | P7 business analyst and the reference data administrator | Resolved (directive) |
| GAP-2441 | How the business date, the queue identifier and the owner identifier travel in the decision record is not in the sources | P7 and P3 contract owners | Resolved (directive) |
| GAP-2442 | The text of MSG-P7-009, the text of the chain-break warning and the field name of the per-entry chain result are not in the sources | P7 business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2443 | No provided operation of the Ownership Map serves a compiled rule package version to the owning service | P7 solution architect and the Ownership Map owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3072 | RWB-S8-E1020-APP: the allocation-to-deviation boundary, the handler roster, the assignment method and any handler cap have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3073 | RWB-S8-E1020-APP: the key has no contract story of its own, the event names are taken from the TSD, and the business wave is earlier than the service wave | Programme lead and solution architect | Resolved (directive) |
| GAP-3074 | The business epic places the story in wave 1 while the service sits in wave 2 | Programme planner with the S8 service owner | Resolved (directive) |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3076 | No source publishes the operation names of the six rows this slice consumes | P1 rwb-source-data owner, P3 rwb-case owner, P4 rwb-access owner, P7 rwb-decision owner and the S8 service owner | Resolved (directive) |
| GAP-3077 | No source says which service hosts the TRANSFER package evaluation after the split | Solution architect with the S8 service owner and the P7 rwb-decision owner | Resolved (directive) |
| GAP-3079 | The event names of the P3 and P1 subscriptions are not published | P3 rwb-case owner, P1 rwb-source-data owner and the S8 service owner | Resolved (directive) |
| GAP-3080 | No source fixes where this slice records the rule ID and the package version of a transfer | S8 service owner with the data steward of module S8 and the P3 rwb-case owner | Resolved (directive) |
| GAP-3081 | RWB-S8-E1023-APP: the five read operations and the four consumed operation names of the case record view have no published baseline, and the freshness, scope and mask answers of the owners are unnamed | Solution architect | Resolved (directive) |
| GAP-3082 | RWB-S8-E1023-APP: a P3 Case and workflow module story is placed in rwb-deviation with an empty build row, and the plan gives the slice no platform dependency although seven pattern rows add one | Solution architect | Resolved (directive) |
| GAP-3083 | RWB-S8-E1023-APP: the plan assigns the slice no legacy acceptance criterion while it keeps thirteen legacy test cases, and the legacy criteria lose their owned ids | Solution architect | Resolved (directive) |
| GAP-3084 | RWB-S8-E1023-APP: the story wave is 1 by the business-epic map while the service wave is 2 in Arch v5, and the section timeout and the six lists have no published values for this page | Solution architect | Resolved (directive) |
| GAP-3103 | RWB-S9-AD022-APP: the partner user catalogue, the date trigger, the recall event and the legacy predecessor are unstated | Business analyst, S9; solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3104 | RWB-S9-AD022-CON: no element for the partner user, no operation name for the rwb-access read, and no ID mapping for the two events | Solution architect; tech lead of rwb-partner | Resolved (directive) |
| GAP-3173 | Service S8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3194 | The 42-column drop of DEF-05 has no named story for seven services | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3207 | No source names the rwb-case database login or where the caseload cap is stored | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3208 | The schedule expression of the DailyCaseRun (legacy JOB-03) is not stated by any source | Solution architect | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
