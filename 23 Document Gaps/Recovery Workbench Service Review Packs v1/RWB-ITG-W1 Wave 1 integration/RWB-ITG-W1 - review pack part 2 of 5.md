# RWB-ITG-W1 Wave 1 integration - review pack, part 2 of 5 (RWB-ITG-E1016-ITG to RWB-ITG-E1028-ITG)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 13 |
| Resolved in the stories | 325 |
| Cross-document (pending in another document) | 171 |
| Not applied (value not in the sources) | 14 |
| Open business decisions | 35 |
| Register gaps linked | 146 |
| Unconfirmed assumptions | 0 |
| Lint findings | 3 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-ITG-E1016-ITG | 23 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1016 ITG Access control per data product and catalog entries - integration v2.md |
| RWB-ITG-E1017-ITG | 14 | 15 | 3 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1017 ITG Retention and archive rule for the data store - integration v2.md |
| RWB-ITG-E1018-ITG | 32 | 29 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1018 ITG Case ID issuance and case record v1 - integration v2.md |
| RWB-ITG-E1019-ITG | 24 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1019 ITG Roles, teams and queues as data - integration v2.md |
| RWB-ITG-E1020-ITG | 39 | 23 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1020 ITG Allocation and assignment engine v1 - integration v2.md |
| RWB-ITG-E1021-ITG | 35 | 11 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1021 ITG Transfer rules and engine v1 - integration v2.md |
| RWB-ITG-E1022-ITG | 19 | 9 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1022 ITG Sign-on with SSO, MFA and the first roles - integration v2.md |
| RWB-ITG-E1023-ITG | 33 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1023 ITG Case record view v1, read only - integration v2.md |
| RWB-ITG-E1024-ITG | 21 | 9 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1024 ITG Document store and index - integration v2.md |
| RWB-ITG-E1025-ITG | 21 | 7 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1025 ITG Document types and fields agreed - integration v2.md |
| RWB-ITG-E1026-ITG | 23 | 6 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1026 ITG Attach and search screen - integration v2.md |
| RWB-ITG-E1027-ITG | 25 | 10 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1027 ITG Decision log writer v1 - integration v2.md |
| RWB-ITG-E1028-ITG | 16 | 10 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-ITG-W1 Wave 1 integration/RWB ITG E1028 ITG Service levels, timers, escalation and prescription dates - integration v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1025-ITG, RWB-P5-E1025-APP, RWB-P5-E1053-APP, RWB-P5-E1053-CON | R-09182 | GAP-1585 | Register gap | Business lead with Legal counsel and the Head of NPA | The six document types are counted at 26 fields but only two types name their fields | FR-P5-011 and FR-P5-016 require the full field list to be delivered as the signed reference load and this PRD requires the count to reconcile, not a specific list. OQ-P5-01 and OQ-P5-14 carry the question. |
| RWB-ITG-E1018-ITG | R-09330 | CG-ALL-233 | Script gap | Product owner | Open decision DL17 has no assumption | Owner rules DL17; until then build on the recommended option. |
| RWB-ITG-E1020-ITG | R-09336 | CG-ALL-255 | Script gap | Product owner | Open decision DL24 has no assumption | Owner rules DL24; until then build on the recommended option. |
| RWB-ITG-E1025-ITG | R-09347 | CG-ALL-291 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-21966 | GAP-1501 | Register gap | Compliance and PDPA officer | Field-level masking rules belong to the access service, while the FSD loads them here | This service keeps data_product_access (role, product, read right) and applies the masking policy of rwb-access, cached per the platform pattern; the masking rows themselves are rwb-access's. Confirm the split with Compliance and Security before the first masking test. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P7-E1017-APP | R-21967 | GAP-2070 | Register gap | Service owners P7 rwb-decision, P1 rwb-source-data and P4 rwb-access with Compliance | Where the retention period of the ledgers and the access log is held, and which job enforces it | Keep every period as written and mark the owner open: P7 enforces the ledger period, P1 the interaction ledger and P4 the access log, each as a row of its own retention data, until Compliance states where the periods are held. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21971 | GAP-1500 | Register gap | Compliance and PDPA officer | The retention rule table and the archive job move to the document service, while the FSD keeps both here | This service declares the retention class per data product and recovery table as versioned reference data, refuses a rule that names a read-only ACE view or the decision log, and archives nothing itself; the rule table and the monthly archive run belong to rwb-document. Confirm with Compliance that a class declared here and applied there is acceptable for the PDPA position. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-22002 | GAP-0685 | Register gap | Business owner; reference data administrator | The source of the caseload cap is not fixed: parameter row or reference data | Keep the cap as versioned reference data on queue.capacity_cap and queue_member.capacity, as the legacy data model does, and add a parameter key only if a product-level override is wanted; state the ruling in the Reference Data and Parameters design. |
| RWB-ITG-E1021-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-22012 | GAP-3078 | Register gap | P7 rwb-decision owner with the business owner of module S8 | The TRANSFER rows that fire on the deviation triggers and the text of R-DEV-04 to R-DEV-06 are not published | The rule owner publishes the DEV transfer rows and the text of R-DEV-04 to R-DEV-06 with the package version; the story then reads them unchanged and no code changes. |
| RWB-ITG-E1027-ITG, RWB-ITG-E1037-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-22037 | GAP-2073 | Register gap | Service owner P7 rwb-decision with P4 rwb-access and Compliance | The approver identifier is personal data under a rule that forbids personal data in records | Store the identifier, never a name; mask it in every export under the masking rows of rwb-access (P4) and record the read in the PII log. The protection of the column itself is a decision for Compliance and Information Security. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1027-ITG, RWB-PLT-E1027-APP, RWB-PLT-E1027-CON, RWB-P4-E1008-APP, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1027-APP, RWB-P7-E1027-CON | R-28460 | GAP-2067 | Register gap | Document owner of the audit and logging design | The source reads version 1 in its metadata table and v2 in its file name | Take the file name as the family version, so this document becomes version 3, and keep the source values in a 'Source version' row: 1, 28 October 2026. The change log carries both readings. |
| RWB-ITG-E1016-ITG, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P4-E1016-APP, RWB-P5-E1016-APP | R-28495 | GAP-1510 | Register gap | Compliance with Security | The classification scheme per data product and the retention periods are open, so the PRD labels are a reading of the field markers | Apply the four-label scheme from the field markers now: personal fields and the party and contact extension rows as personal data, balances and amounts as sensitive financial data, case, legal, collateral and metadata as confidential, and no data product as public. Replace with the approved scheme when DL26 closes. |
| RWB-ITG-E1017-ITG, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-28498 | GAP-1618 | Register gap | Compliance and PDPA officer | The decision log and the ledger carry no retention period, and the WORM seal period is unstated | Set the decision-log class period and the seal period under DL26 before the first release, keep the class per record class in reference data, and state in the retention rule that no archive runs inside this service. |
| RWB-ITG-E1020-ITG, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1020-OPS, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP | R-28522 | GAP-0686 | Register gap | Business owner, Shared operations; platform team, Temporal | The exact cadence of the rebalancing trigger is not defined for rwb-case | Run JOB-06 as its own Temporal Schedule at 06:30 Asia/Bangkok, after DailyCaseRun has finished, with overlap policy SKIP and a catch-up window; confirm the order with the operations owner and record it in the Temporal Workflow and Activity Catalog. |
| RWB-ITG-E1021-ITG, RWB-ITG-E2012-ITG, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2012-OPS, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-P7-E2012-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-28530 | GAP-0689 | Register gap | Business owner, case and workflow | No source names who may override a transfer refused by a rule, the cap check or the status check | Confirm with the business owner in the Epic 2 transfer screen story (RWB-E2-012). This run assumes no override path in Epic 1: a refused transfer changes nothing and the caller retries with another target. |
| RWB-ITG-E1021-ITG, RWB-PLT-E1043-APP, RWB-PLT-E1043-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1043-APP, RWB-P3-E1043-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP | R-28535 | GAP-0690 | Register gap | Business owner, case and workflow | Ownership and change control of the transfer reason list are not specified | P3 owns the list as reference data under the R-PREC default ruling and DP-07, and the business owner of DL23 approves every addition or retirement through the reference-load approve operation of rwb-case. |
| RWB-ITG-E1022-ITG, RWB-P4-E1022-APP, RWB-P4-E1022-CON, RWB-P4-E1022-DB | R-28537 | GAP-1578 | Register gap | Product owner | FEAT-ACA-15, the release checklist and go-live readiness, is a delivery activity inside the product feature list and has no product requirement | Retire FEAT-ACA-15 from the module feature list and carry the release checklist in the programme delivery plan, so the P4 feature list holds only behaviour that a product can be accepted against. |
| RWB-ITG-E1023-ITG, RWB-ITG-E2016-ITG, RWB-P3-E1023-APP, RWB-P3-E1023-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P4-E1023-APP, RWB-P5-E2016-APP, RWB-S8-E1023-APP | R-28538 | GAP-1577 | Register gap | Business analyst with the P3 product owner | The case record view and its history timeline are listed as P4 features while the screen and its endpoints belong to rwb-case | Move FEAT-ACA-11 and FEAT-ACA-12 with their acceptance criteria to FSD P3 in the next version, and leave in FSD P4 only the authorise, scope and masking behaviour the screen consumes, so each feature has one owner and one acceptance set. |
| RWB-ITG-E1025-ITG, RWB-P5-E1025-APP | R-28545 | GAP-1040 | Register gap | Business lead with Legal | No role holds Reference data A to approve a document-type load | Decide in DL01 which role holds Reference data A for the document-type table (the assumed answer is the legal counsel who owns the table) and record it in the rwb-access permission matrix; if the Head of NPA is intended as the approver, grant the right there instead |
| RWB-ITG-E1028-ITG, RWB-ITG-E1055-ITG, RWB-P1-E1055-APP, RWB-P3-E1028-APP, RWB-P3-E1028-CON, RWB-P3-E1028-OPS, RWB-P3-E1055-APP, RWB-P4-E1028-APP, RWB-P5-E1055-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-P7-E1028-APP | R-28550 | GAP-2244 | Register gap | Business lead and Legal | No warning point is defined for a notice period | If a warning is wanted on the notice period, load a warning percentage or a warning day count as a reference row of rwb-case and add one criterion; until then warn_at stays null. |
| RWB-ITG-E1018-ITG | R-33380 | ASM-ALL-233 | Script assumption |  | Built on the recommended option of DL17: A. | Product owner with the solution architect rules DL17 |
| RWB-ITG-E1020-ITG | R-33381 | ASM-ALL-255 | Script assumption |  | Built on the recommended option of DL24: A. The route decision goes live in a later epic. | Product owner rules DL24 |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1020-APP, RWB-P3-E1020-CON, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35401 | ASM-1232 | Register assumption |  | The caseload cap (150 in the legacy examples) stays reference data on queue.capacity_cap and queue_member.capacity, versioned with the QUEUE and QUEUE_MEMBER reference tables; no parameter key is added for it in wave 1. | Business owner; reference data administrator |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35402 | ASM-1237 | Register assumption |  | The transfer reason list is reference data of rwb-case: P3 owns the LOV-TRANSFER-REASON rows, the business owner of DL23 approves additions and retirements through the reference-load approve operation, and the published contract references the list without enumerating it. | Business owner, case and workflow |
| RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2012-ITG, RWB-ITG-E2036-ITG, RWB-P2-E2036-APP, RWB-P3-E1019-APP, RWB-P3-E1019-CON, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1021-CON, RWB-P3-E1021-OPS, RWB-P3-E1030-APP, RWB-P3-E1045-APP, RWB-P3-E2002-APP, RWB-P3-E2011-APP, RWB-P3-E2012-APP, RWB-P3-E2012-CON, RWB-P3-E2036-APP, RWB-P4-AD014-APP, RWB-P4-AD014-CON, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1020-APP, RWB-P7-E1030-APP, RWB-P7-E2012-APP, RWB-S8-E1020-APP, RWB-S8-E1021-APP, RWB-S8-E2012-APP | R-35404 | ASM-1560 | Register assumption |  | No caseload cap value and no default cap is written anywhere: a queue row without a cap is accepted, a cap present in the file is validated as a positive integer, and the in-force caps are supplied by the business under DL23 and carried by the file. | Product owner when the cap values are agreed under DL23 |
| RWB-ITG-E1019-ITG, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P4-E1022-APP, RWB-P5-E1025-APP, RWB-P5-E1025-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP | R-35406 | ASM-1988 | Register assumption |  | The approver of a document-type load is the legal counsel who owns the type table, holding Reference data A, as the legacy story assumes under DL01; the loader holds Reference data C and may not approve | Business lead with Legal confirms the role that approves the type list |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1043-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-AD016-APP, RWB-P4-E1028-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2006-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S2-E2006-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35409 | ASM-2569 | Register assumption |  | Every approval limit, range, floor, period and criterion that Epics 3 to 8 refer to is a versioned reference-data row loaded from the regulation and the approved policy. No limit or value is asserted in this document, and each acceptance criterion runs against the loaded version. | Risk with the product heads, before the E3 release |
| RWB-ITG-E1020-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E2004-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2013-ITG, RWB-ITG-E2015-ITG, RWB-ITG-E2033-ITG, RWB-ITG-E2035-ITG, RWB-ITG-AD015-ITG, RWB-P2-E2006-APP, RWB-P2-E2033-APP, RWB-P2-E2035-APP, RWB-P3-E1020-APP, RWB-P3-E1028-APP, RWB-P3-E1045-APP, RWB-P3-E1065-APP, RWB-P3-E2004-APP, RWB-P3-E2006-APP, RWB-P3-E2013-APP, RWB-P3-E2014-APP, RWB-P3-E2015-APP, RWB-P3-E2033-APP, RWB-P3-E2035-APP, RWB-P4-AD015-APP, RWB-P4-E1028-APP, RWB-P4-E2013-APP, RWB-P4-E2015-APP, RWB-P4-E2033-APP, RWB-P4-E2035-APP, RWB-P6-E2013-APP, RWB-P7-E1020-APP, RWB-P7-E2013-APP, RWB-P7-E2013-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-APP, RWB-P7-E2035-APP, RWB-S2-E2004-APP, RWB-S8-E7001-APP, RWB-S8-E7004-APP, RWB-S8-E7005-APP, RWB-S8-E7006-APP, RWB-S8-E7006-CON, RWB-S8-E7007-APP, RWB-S8-E7008-APP, RWB-S8-E7009-APP, RWB-S8-E7010-APP, RWB-S8-E7010-CON, RWB-S9-E7011-CON, RWB-S9-E7014-APP | R-35411 | ASM-2217 | Register assumption |  | The service level and the escalation run on three data values: rwb.approval.route.<decision>.service-level and rwb.approval.service-level.default as the legacy assumes them (1 working day for D7.1, 3 working days default, DL22), one working day per escalation step as AC2 shows, and rwb.approval.escalation.max-levels with the behaviour at the ceiling held as data with no value until the register closes the point. | Business lead with the Center of excellence at the RWB-P7-E2013-CON baseline review. |
| RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1034-ITG, RWB-PLT-TE012-APP, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1041-APP, RWB-P6-AD017-APP, RWB-P6-E1034-APP | R-35419 | ASM-2709 | Register assumption |  | The values of the Non-Functional Specification v3 are the values this PRD is written against, with the status each one carries. A value marked Proposed is used as written until its owner confirms it under the decision named; a value marked Open is recorded as not set. | Solution architect with Risk at DL11 |
| RWB-ITG-E1026-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-P3-E2024-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1026-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P7-E2024-APP, RWB-S9-E2019-APP | R-35429 | ASM-2567 | Register assumption |  | The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text. | Product owner and the owners of DL03 and DL09 |
| RWB-ITG-TE010-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E2002-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2006-ITG, RWB-ITG-E2007-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E2019-ITG, RWB-ITG-E2024-ITG, RWB-PLT-E1047-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-PLT-TE001-APP, RWB-PLT-TE001-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS, RWB-P1-E1015-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E2007-APP, RWB-P1-E2010-APP, RWB-P2-E1007-APP, RWB-P2-E2001-APP, RWB-P2-E2002-APP, RWB-P2-E2002-CON, RWB-P2-E2002-OPS, RWB-P2-E2003-APP, RWB-P2-E2006-APP, RWB-P2-E2007-APP, RWB-P3-E1007-APP, RWB-P3-E1019-APP, RWB-P3-E1042-APP, RWB-P3-E1042-APP, RWB-P3-E2001-APP, RWB-P3-E2002-APP, RWB-P3-E2006-APP, RWB-P3-E2007-APP, RWB-P3-E2024-APP, RWB-P4-E1007-APP, RWB-P4-E1022-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2019-INF, RWB-P4-E2024-APP, RWB-P5-E1007-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P5-E1040-APP, RWB-P5-E1041-APP, RWB-P5-E1057-APP, RWB-P5-E2024-APP, RWB-P6-E1007-APP, RWB-P6-E1034-APP, RWB-P6-E2021-OPS, RWB-P7-E2001-APP, RWB-P7-E2006-APP, RWB-P7-E2007-APP, RWB-P7-E2013-OPS, RWB-P7-E2014-OPS, RWB-P7-E2024-APP, RWB-S2-E2006-APP, RWB-S2-E2007-APP, RWB-S3-E2010-APP, RWB-S9-E2019-APP | R-35657 | ASM-0189 | Register assumption |  | Every owner label that named an individual in v10 is replaced by the placeholder of Template and Rules §R9, and the role or organisation the same cell states is kept after the placeholder. No role is attributed to an individual. | Programme governance |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-ITG-E1017-ITG | R-03450 | DOR-RWB-ITG-E1017-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size value is in the sources, so the item stays open. |
| RWB-ITG-E1017-ITG | R-03452 | DOR-RWB-ITG-E1017-ITG-22 | 12.8 | Definition of Ready item 22 Fake published: Fail | Four fakes are named in 12.8 (Service Contract Catalog v1 §7.2). No published fake library version is in the sources, so 12.8 marks it Not specified and the item stays open. |
| RWB-ITG-E1017-ITG | R-13872 | DOR-RWB-ITG-E1017-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | No size value supports a Small fit claim, so the item stays open. |
| RWB-ITG-E1018-ITG | R-03460 | DOR-RWB-ITG-E1018-ITG-23 | header | Definition of Ready item 23 Contract version fixed: Fail | No contract version is in any source, so the header now carries the Not specified placeholder. The version must still be fixed before ready. |
| RWB-ITG-E1021-ITG | R-13902 | DOR-RWB-ITG-E1021-ITG-18 | 18 | Definition of Ready item 18 Open decisions: Partial | DL10 (Thai names, Decision Log v12) is an open business decision; the directive excludes those and no source gives Thai text, so it stays open. |
| RWB-ITG-E1022-ITG | R-03484 | DOR-RWB-ITG-E1022-ITG-14 | 17 | Definition of Ready item 14 Epic design: Fail | No signed epic design for EP01/RWB-ITG-W1 found by grep of project .md files or Decision Log v11 (DT05). A sign-off cannot be invented, so it needs the epic design record. |
| RWB-ITG-E1024-ITG | R-03499 | DOR-RWB-ITG-E1024-ITG-16 | header | Definition of Ready item 16 Size: Fail | No size is given in the sources. The header Size row records it as Not specified; the squad sizes the story at refinement. |
| RWB-ITG-E1024-ITG | R-13927 | DOR-RWB-ITG-E1024-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | The Small criterion cannot be confirmed from the sources; the squad sizes the story at refinement. |
| RWB-ITG-E1026-ITG | R-03512 | DOR-RWB-ITG-E1026-ITG-16 | Header | Definition of Ready item 16 Size: Fail | Header row Size states it is not specified in the source documents; the item stays open until the squad sizes the story at refinement. |
| RWB-ITG-E1027-ITG | R-03517 | DOR-RWB-ITG-E1027-ITG-14 | 17 | Definition of Ready item 14 Epic design: Fail | No signed epic design for RWB-ITG-W1 in 04 User stories, 05 Technical architecture or 22 Microservice Realignment .md files; a sign-off would be invented. |
| RWB-ITG-E1028-ITG | R-03524 | DOR-RWB-ITG-E1028-ITG-16 | header | Definition of Ready item 16 Size: Fail | Header states that the squad sets the size at refinement. No size is given in the story, so DoR item 16 stays open until the squad sizes it. |
| RWB-ITG-E1028-ITG | R-13959 | DOR-RWB-ITG-E1028-ITG-10 | 15 | Definition of Ready item 10 Screens and states: Partial | Screen Specifications v1 lists SCR-03 as Loading, read only, editable, on hold and SCR-09 as Loading, list. No empty or error state for either, so CG-ALL-301/302 stay. |
| RWB-ITG-E1028-ITG | R-13961 | DOR-RWB-ITG-E1028-ITG-15 | header | Definition of Ready item 15 INVEST: Partial | DoR v4 item 15 needs a fit of two weeks or less. Size is left to squad refinement and no sizing exists in the sources. Stating a fit would invent a value. |
| RWB-ITG-E1028-ITG | R-13962 | DOR-RWB-ITG-E1028-ITG-17 | header | Definition of Ready item 17 Dependencies: Partial | DoR v4 item 17 needs deps done, in progress on the board, or behind a flag. Board state is outside the story and no flag name is in the sources; naming one would invent it. |

## 5. Cross-document changes (pending in the target document)


### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00409 | RWB-ITG-E1016-ITG | DOR-RWB-ITG-E1016-ITG-1 | 1 | Add the role 'QA integration engineer' with a role code, or confirm the existing role code that section 1 should use. |
| CDC-00415 | RWB-ITG-E1017-ITG | DOR-RWB-ITG-E1017-ITG-1 | 1 | Add role QA integration engineer, or map the section 1 role to an existing role code |
| CDC-00438 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-1 | 1 | Add the role 'QA integration engineer' or name the existing URP role this story's user maps to. Section 1 is unchanged. |
| CDC-00458 | RWB-ITG-E1019-ITG | DOR-RWB-ITG-E1019-ITG-1 | 1 | Add a role for QA integration engineer, or confirm the role name that maps to an existing role code, so section 1 resolves. |
| CDC-00473 | RWB-ITG-E1020-ITG | DOR-RWB-ITG-E1020-ITG-1 | 1 | Add a role code or role name for 'QA integration engineer' so that section 1 of RWB-ITG-E1020-ITG can cite it. |
| CDC-00489 | RWB-ITG-E1020-ITG | GAP-0987 |  | Record PM-2026.11 in force at 30 November 2026 with PM-2026.12 from 2026-12-01, and the Queue and allocation role roster with scopes as the ruling states. |
| CDC-00497 | RWB-ITG-E1021-ITG | DOR-RWB-ITG-E1021-ITG-1 | 1 | Add a role code or role name for the QA integration engineer persona, or record it there as a non-role persona; §1 of the story is left unchanged. |
| CDC-00508 | RWB-ITG-E1022-ITG | DOR-RWB-ITG-E1022-ITG-1 | 1 | Add 'QA integration engineer' as a role name in Users Roles and Permissions v5, or the story takes a role code or name already in it. |
| CDC-00524 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-1 | 1 | Add the role 'QA integration engineer' with its role code, or the story must name the existing role used there. |
| CDC-00536 | RWB-ITG-E1024-ITG | DOR-RWB-ITG-E1024-ITG-1 | 1 | Add 'QA integration engineer' as a role code or role name, or confirm the existing role this story maps to. |
| CDC-00545 | RWB-ITG-E1025-ITG | DOR-RWB-ITG-E1025-ITG-1 | 1 | Add role 'QA integration engineer' or record the existing role code it maps to. |
| CDC-00551 | RWB-ITG-E1026-ITG | DOR-RWB-ITG-E1026-ITG-1 | 1 | Add QA integration engineer as a role code or role name, so the section 1 role resolves to a listed role. |
| CDC-00555 | RWB-ITG-E1027-ITG | DOR-RWB-ITG-E1027-ITG-1 | 1 | Add role 'QA integration engineer' (or the role code to be used) to Users Roles and Permissions v5. |
| CDC-00567 | RWB-ITG-E1028-ITG | DOR-RWB-ITG-E1028-ITG-1 | 1 | Add the role QA integration engineer so that the section 1 role resolves to a role in the document |

### Epic design record (10)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00406 | RWB-ITG-E1016-ITG | DOR-RWB-ITG-E1016-ITG-14 | n/a | Record the signed epic design sign-off for RWB-ITG-W1 in the epic design record. |
| CDC-00413 | RWB-ITG-E1017-ITG | DOR-RWB-ITG-E1017-ITG-14 | none | Record the signed epic design sign-off for RWB-ITG-W1 and EP01 |
| CDC-00457 | RWB-ITG-E1019-ITG | DOR-RWB-ITG-E1019-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-W1 / EP01 so the story can cite it. |
| CDC-00471 | RWB-ITG-E1020-ITG | DOR-RWB-ITG-E1020-ITG-14 |  | Confirm and record the signed epic design for RWB-ITG-W1. |
| CDC-00495 | RWB-ITG-E1021-ITG | DOR-RWB-ITG-E1021-ITG-14 | Header | Record the signed epic design sign-off for RWB-ITG-E1021-ITG. |
| CDC-00518 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-14 | header | Record the signed epic design sign-off for RWB-ITG-E1023-ITG. |
| CDC-00533 | RWB-ITG-E1024-ITG | DOR-RWB-ITG-E1024-ITG-14 |  | Record the signed epic design sign-off for RWB-ITG-E1024-ITG; the story cannot confirm it without that record. |
| CDC-00542 | RWB-ITG-E1025-ITG | DOR-RWB-ITG-E1025-ITG-14 | n/a | Record the signed epic design sign-off for RWB-ITG-E1025-ITG. |
| CDC-00549 | RWB-ITG-E1026-ITG | DOR-RWB-ITG-E1026-ITG-14 |  | No signed epic design in source; sign-off must come from the epic design record. |
| CDC-00565 | RWB-ITG-E1028-ITG | DOR-RWB-ITG-E1028-ITG-14 | find it | Record the signed epic design sign-off for RWB-E1-028 and link it to RWB-ITG-E1028-ITG |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00439 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-12 | 16 | Align the section 18 test lists for P3 with this story's section 16. Contract test TC-E1-018-17-ITG is added to section 16 and cited under ADR-020. |
| CDC-00450 | RWB-ITG-E1018-ITG | CG-ALL-228 | 18 | Align the test lists of the six listed requirements with section 18 of this story in the next RTM version. |
| CDC-00465 | RWB-ITG-E1019-ITG | CG-ALL-235 | 18 | Align the test case lists of REQ-CWC-006, REQ-ACA-002 and the other differing requirements with section 18 in the next RTM version. |
| CDC-00485 | RWB-ITG-E1020-ITG | CG-ALL-248 | 18 | Align the test lists of REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and the other differing requirements with section 18 in the next version. |
| CDC-00498 | RWB-ITG-E1021-ITG | DOR-RWB-ITG-E1021-ITG-12 | 18 | Next version: add the -ITG copies to REQ-CWC-010 (04, 05, 10) and REQ-CWC-016 (03, 09, 16); reconcile REQ-CWC-005 and REQ-WKM-003, which list only E1-018 and E2-012 tests. |
| CDC-00500 | RWB-ITG-E1021-ITG | CG-ALL-262 | 18 | Align the REQ-CWC-010 and REQ-CWC-016 test lists in RTM v7 with section 18 of RWB-ITG-E1021-ITG in the next RTM version. |
| CDC-00509 | RWB-ITG-E1022-ITG | DOR-RWB-ITG-E1022-ITG-12 | 16, 18 | Align the test case lists of section 18 with the test case IDs of RTM v7 for this story. |
| CDC-00513 | RWB-ITG-E1022-ITG | CG-ALL-271 | 18 | Align the test lists for REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 with section 18 of RWB-ITG-E1022-ITG in the next RTM version. |
| CDC-00531 | RWB-ITG-E1023-ITG | CG-ALL-280 | 18 | Align the trace lists of the five differing requirements with section 18 of RWB-ITG-E1023-ITG in the next RTM version. |

### API:(service not named) (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00444 | RWB-ITG-E1018-ITG | GAP-2433 | 14 | Write one sentence for MSG-P7-009 naming the field and case reference, and one warning for MSG-P7-012 naming the chain position; add both rows to the API specification. |
| CDC-00448 | RWB-ITG-E1018-ITG | GAP-2434 | 4 | Add finalCall to the query parameters of API-P7-006 and fix the creation filter answer as a page of entries with the thirteen fields this story names. |
| CDC-00477 | RWB-ITG-E1020-ITG | GAP-0345 | find it | Publish JOB-03 step state on the rwb-case run result; fix the rerun facade for a workflow step in the P1 contract before wave 1 exit. |
| CDC-00511 | RWB-ITG-E1022-ITG | GAP-1568 | none in this story | Publish the four rwb-access operations with request and answer schemas, refusal codes, version fields, masking vocabulary; state group-to-role read path |
| CDC-00512 | RWB-ITG-E1022-ITG | GAP-0776 | 7 | Publish POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions under the R4 base and DP-13 with contract payloads |
| CDC-00552 | RWB-ITG-E1026-ITG | GAP-1033 | 13 | Publish a P5 contract story for the case document operations, or add a contract part to RWB-P5-E1024-APP, fixing the Document, DocumentPage and DocumentChecklist field names and the MSG-GEN-006 virus-scan text; name the rwb_document login in the service DB story (DP-02). |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00408 | RWB-ITG-E1016-ITG | CG-ALL-213 | 16 | Add rows for TC-E1-016-10-ITG, TC-E1-016-11-ITG and TC-E1-016-12-ITG with Given, When and Then copied from AC9, AC10 and AC11. |
| CDC-00437 | RWB-ITG-E1018-ITG | CG-ALL-226 | 16 | Add rows TC-E1-018-15-ITG and TC-E1-018-16-ITG with Given, When and Then copied from the AC13 and AC15 criteria. |
| CDC-00523 | RWB-ITG-E1023-ITG | CG-ALL-277 | 16 | Add rows TC-E1-023-12-ITG and TC-E1-023-13-ITG with Given, When and Then copied from AC11 and AC12. |
| CDC-00566 | RWB-ITG-E1028-ITG | CG-ALL-299 | 16 | Owner role QA. Section 16 lists TC-E1-028-14-ITG to TC-E1-028-17-ITG; v8 needs the matching rows. |
| CDC-00568 | RWB-ITG-E1028-ITG | DOR-RWB-ITG-E1028-ITG-12 | 16 | Section 16 now has 17 test cases. The remaining gap is the v8 rows for TC-E1-028-14-ITG to TC-E1-028-17-ITG. |

### RWB-P7-E1017-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00422 | RWB-ITG-E1017-ITG | GAP-2427 | 14 | Write the MSG-P7-009 text and the not-found, chain-break and collection gap alert IDs and texts with the P7 business analyst; keep the legacy AC8 check name inside MSG-P7-009. Texts are in no source. |
| CDC-00423 | RWB-ITG-E1017-ITG | GAP-2428 | 12 | State JOB-14 as 02:00 Asia/Bangkok, queue rwb-decision, page size 5000, one run at a time; record property names and flag-off answer as configuration decisions in the service template. |
| CDC-00424 | RWB-ITG-E1017-ITG | GAP-2431 |  | The orphan file is from the superseded P7 Work Package B-P7-05. This ITG story is not that file and needs no edit. |
| CDC-00425 | RWB-ITG-E1017-ITG | GAP-2432 |  | This concerns the P7 slice. This ITG story keeps its own mapping and needs no edit here. |
| CDC-00427 | RWB-ITG-E1017-ITG | GAP-2429 | 3 | Keep metadata rows; name every added H and C row and the P4 authorise contract in the pattern table and 12.8 fakes; step D1 decides whether they enter the dependency map. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00505 | RWB-ITG-E1022-ITG | CG-ALL-269 | 12.2 | Publish POST /api/recovery/access/v1/authorise in rwb-access.yaml through the provider's CON story, or consume a published operation. |
| CDC-00506 | RWB-ITG-E1022-ITG | DOR-RWB-ITG-E1022-ITG-21 | header | The header row reads Not specified for contract story keys. No CON key is found in the sources. Publication of the contract belongs to rwb-access.yaml. |
| CDC-00507 | RWB-ITG-E1022-ITG | DOR-RWB-ITG-E1022-ITG-8 | header, 12.2 | Same provider gap as CG-ALL-269. The contract publication belongs to rwb-access.yaml, not this story. |
| CDC-00515 | RWB-ITG-E1023-ITG | CG-ALL-274 | 12.2 | Publish POST /api/recovery/access/v1/authorise through the rwb-access provider CON story. |
| CDC-00516 | RWB-ITG-E1023-ITG | CG-ALL-275 | 12.2 | Publish GET /api/recovery/access/v1/me/permissions through the rwb-access provider CON story. |

### RWB-P1-E1017-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00414 | RWB-ITG-E1017-ITG | DOR-RWB-ITG-E1017-ITG-21 | header | The story names RWB-P1-E1017-CON as its contract dependency. Publication of the contract must be confirmed in that contract story. |
| CDC-00417 | RWB-ITG-E1017-ITG | GAP-0342 |  | Specify the cross-service trigger and API for the P1 interaction rows, and the run-status surface of the P5 retention run, with P5 owning the rule and archive. |
| CDC-00418 | RWB-ITG-E1017-ITG | GAP-0489 |  | Fix POST /retention-runs and GET /retention-runs/{runId} on /api/recovery/source-data/v1 with rule version, run date and rules in the request, and run status, counts per table, rule version, archive location and held cases in the answer, with 202 and 409 responses. |

### parameter-catalog.csv (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00428 | RWB-ITG-E1018-ITG | CG-ALL-220 | find it | Record case.entry.dpd as the single threshold key; rename case.entry.dpd_threshold in Assumptions Register v1 and Test Cases v8 to match. |
| CDC-00433 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-20 | 13 | Add key case.entry.dpd as the single threshold key; section 13 now names it. |
| CDC-00562 | RWB-ITG-E1027-ITG | GAP-1617 | 8 | Add reference-data rows: ledger completeness target 5 minutes; gap alert threshold 5 minutes; strict-mode maximum wait Not specified in the source documents (GAP-1617), to confirm with Risk and Internal Audit at ADR-022 sign-off. |

### RWB-PLT-N001-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00449 | RWB-ITG-E1018-ITG | GAP-0674 | 12 | Publish the gateway-bff composite route for SCR-02 and SCR-03 with path, parallel calls, merge order, masking rules and the 2 s budget. |
| CDC-00521 | RWB-ITG-E1023-ITG | GAP-0693 | 7 | Publish the gateway-bff composite route for SCR-03: path, parallel call set, merge field map, 2 s budget split and partial-failure rule; keep the five rwb-case read operations unchanged. |
| CDC-00554 | RWB-ITG-E1026-ITG | GAP-1035 | 7 | Publish the SCR-30 gateway-bff composite route with its path, merged screen-model fields, and per-call timeout and breaker values, so this tab can read it. |

### RWB-S8-E1023-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00529 | RWB-ITG-E1023-ITG | GAP-3081 |  | Publish the five read paths on /api/recovery/deviation/v1 with the legacy section 12 shapes and the RWB-P3-E1023-CON error envelope; declare the four consumed operations as placeholders with owners and fakes; carry dataAsOf and per-product freshness on every answer; declare rwb-access authorise, mask and AC-READ as one consumed operation; confirm each placeholder with its owner before the tag. |
| CDC-00530 | RWB-ITG-E1023-ITG | GAP-3083 |  | Keep acs empty in the fragment; restate AC1 to AC12 as new under D-RCV-60 with the legacy values; carry TC-E1-023-01 to TC-E1-023-13 unchanged; map TC-E1-023-11 to the access refusal; record the mapping in section 18. |
| CDC-00532 | RWB-ITG-E1023-ITG | GAP-3082 |  | Keep the plan's service, lane, C row and empty H row; record the slice as secondary serving of the page, with the deviation block and assembly as its own and the case header consumed from RWB-P3-E1023-CON; declare the seven platform contracts as build prerequisites and fakes; keep wave 1 by R5.6 with the release tentative. |

### OTHER:P3 screen specification (SCR-47) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00416 | RWB-ITG-E1017-ITG | DOR-RWB-ITG-E1017-ITG-10 | none | Add empty, loading, error and no access states to SCR-47 |
| CDC-00421 | RWB-ITG-E1017-ITG | CG-ALL-219 |  | This story has no screen and puts SCR-47 out of scope (Epic 8). The missing states belong in the SCR-47 screen specification. |

### RWB-PLT-TE012-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00420 | RWB-ITG-E1017-ITG | GAP-0490 |  | Specify the write-once archive container contract: account, credential scope, immutability policy, request shape and manifest schema. |
| CDC-00541 | RWB-ITG-E1024-ITG | GAP-1031 |  | State the storage account, three container names per environment, immutability period per retention class and managed identity |

### OTHER:rwb-source-data API yaml (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00434 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-21 | header | Header now names the consumed provider contracts (P1, P3, P4, P5, P7). The readiness path is still not published by rwb-source-data; publication is provider-side. |
| CDC-00435 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-8 | 4 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready. The event name rwb.decision.DecisionRecorded.v1 already matches Kafka Catalog v1; no story change. |

### RWB-P3-E1018-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00443 | RWB-ITG-E1018-ITG | GAP-0676 | 12 | Agree the field-level OpenAPI schema (required flags, GET /cases page and sort parameters, caseNo pattern, error codes per operation) and record it in the rwb-case API file. |
| CDC-00455 | RWB-ITG-E1018-ITG | GAP-1038 | 16 | Name the rwb-document login, grants and pool size; publish the GET /cases/{caseId} request and response field names and the not-found message ID. |

### RWB-P6-E1019-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00462 | RWB-ITG-E1019-ITG | GAP-1178 | 16 | The missing target is in rwb-comms. This suite already calls the rwb-case load path in TC-E1-019-13-ITG as the access proof of AC8, so that row is unchanged. |
| CDC-00463 | RWB-ITG-E1019-ITG | GAP-1179 | 12.1 | Add the routing read GET /admin/notice-routing to the P6 API file with an allocated API identifier at the next module API revision. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00479 | RWB-ITG-E1020-ITG | GAP-2443 | find it | Add the package-artifact operation to the P7 row and the API Specification, with the same base, model-owner identity and checksum in the answer. |
| CDC-00558 | RWB-ITG-E1027-ITG | GAP-1235 | 12 | Record the decision-record append as a local (in-process, DP-03) operation of P7 on task queue rwb-decision; add no REST write path. |

### RWB-PLT-E1027-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00483 | RWB-ITG-E1020-ITG | GAP-2441 | none | Carry the business date as a record attribute and the queue and owner identifiers as named members of the actions payload. |
| CDC-00557 | RWB-ITG-E1027-ITG | GAP-1238 |  | This story now uses the one value rwb.decision.DecisionRecorded.v1 (CG-ALL-297). The published ce_type in the platform contract is changed there. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1 (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00494 | RWB-ITG-E1021-ITG | CG-ALL-258 | 13 | Create RWB-P7-E1073-CON or name the existing story carrying the same capability; then align the DP-04 dependency in section 13. |
| CDC-00496 | RWB-ITG-E1021-ITG | DOR-RWB-ITG-E1021-ITG-17 | Header | Complete RWB-P3-E1021-APP, RWB-P4-E1021-APP, RWB-P5-E1021-APP, RWB-P7-E1021-APP and RWB-S8-E1021-APP; resolve RWB-P7-E1073-CON (CG-ALL-258). |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00522 | RWB-ITG-E1023-ITG | CG-ALL-272 | none | LOV-CONTACT-TYPE does not appear in this story, so no story edit was made; the list must be added to Reference Data v5. |
| CDC-00525 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-20 | none | Add the P2 list LOV-CONTACT-TYPE |

### RWB-ITG-E1016-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00407 | RWB-ITG-E1016-ITG | DOR-RWB-ITG-E1016-ITG-21 | n/a | Publish the contract story RWB-ITG-E1016-CON and add it as a CON dependency of this story. |

### RWB-P1-E1016-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00410 | RWB-ITG-E1016-ITG | GAP-0484 | none in this story | Deliver the three indexes, read model v_data_product_catalog, DPA-2026.11 seed, 122/1,366 dictionary conformance check and schema checks; create no table already created by RWB-P1-E1001-APP or RWB-P1-E1069-DB; own no masking row; repeat run changes nothing. |

### OTHER:TSD P4 appendix T-A and the rwb-access OpenAPI file (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00411 | RWB-ITG-E1016-ITG | GAP-0983 | none in this story | Publish request and answer schemas of GET /admin/roles, GET /masking-policies and POST /authorise, including marker values, maskingExceptions part, two version fields and access resolution. |

### RWB-P5-E1016-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00412 | RWB-ITG-E1016-ITG | GAP-1028 | none in this story | Record the secondary P5 split and accept the six new criteria; publish GET retention-classes operations with shared RetentionClass shape; consume P4, P3 and P1 operations as published contracts with fakes; inherit guard library and gateway route from service template. |

### OTHER:TSD P7 v2 T3.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00419 | RWB-ITG-E1017-ITG | GAP-2426 |  | Enumerate LOV-DECISION and the final-call list, and state the decision code, final call, action and outcome for archive and purge records, with the run reference in inputsRef. |

### OTHER:Sequence v6 (items 19 and 21) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00426 | RWB-ITG-E1017-ITG | GAP-3230 |  | The retired items still carry v6 windows and dependants. The fix belongs in Sequence v6. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00429 | RWB-ITG-E1018-ITG | CG-ALL-221 | 12.2 | Publish POST /api/recovery/source-data/v1/business-days/{date}/ready through the provider's CON story. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00430 | RWB-ITG-E1018-ITG | CG-ALL-222 | 13 | Create RWB-P7-E1073-CON for the rwb-decision Drools kit (DP-04), or name the existing story that carries it. |

### RWB-ITG-E1018-ITG (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00431 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-14 | find it | Record the signed epic design sign-off for this story's epic in the epic design record. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (eight named dependency stories) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00432 | RWB-ITG-E1018-ITG | DOR-RWB-ITG-E1018-ITG-17 | find it | Complete the eight dependency stories before build start; create or name RWB-P7-E1073-CON (CG-ALL-222). |

### OTHER:Functional Specification Document P3 (FSD) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00436 | RWB-ITG-E1018-ITG | GAP-1549 |  | Restate the P3 A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged. |

### OTHER:P1 service API document (rwb-source-data OpenAPI 3.1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00440 | RWB-ITG-E1018-ITG | GAP-0571 | 7 | Add GET /api/recovery/source-data/v1/entry-candidates: required businessDate and threshold, optional page and size, response EntryCandidatePage, statuses 400, 401, 403, 409, 422, 503 |

### OTHER:RWB-SVC-P3 database story and service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00441 | RWB-ITG-E1018-ITG | GAP-0675 | none | Allocate rwb-case login name with grants on schema rwb_case only and no privilege on another schema; record it in the service catalogue |

### OTHER:P1 service API document (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00442 | RWB-ITG-E1018-ITG | GAP-0573 | 11 | Add two PUT operations by business key for party_ext and account_ext; body carries all four party flags; repeat-safe with version increment |

### OTHER:TSD P7 (DF-DEC-002; OTHER:T3.1; OTHER:T3.3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00445 | RWB-ITG-E1018-ITG | GAP-2435 | 4 | Restate DF-DEC-002 as an indexed business key with no foreign key; drop the recovery_case row of T3.3; state in T3.1 that the ALS business date is carried inside inputs_ref. |

### OTHER:Package ENTRY workbook (rule-row catalogue) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00446 | RWB-ITG-E1018-ITG | GAP-2436 | 4 | Name the admitting ENTER rule ID for package ENTRY in the rule-row catalogue so the registry fixture can copy it. |

### RWB-P1-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00447 | RWB-ITG-E1018-ITG | GAP-3162 | 7 | Write the party_ext and account_ext rows in its own transaction; RWB-P3-E1018-CON case story reads them back by contract. |

### OTHER:Work package C-WEX index (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00451 | RWB-ITG-E1018-ITG | GAP-3206 | find it | Correct the heading '(E1-018)' to a scheduling label; the subject of the document stays RWB-E1-020 as in the source file. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00452 | RWB-ITG-E1018-ITG | GAP-0982 | find it | Add the case-authority request and answer schema for POST /api/recovery/access/v1/authorise, the caller location source in T3.1, and the personal field IDs with version; publish with RWB-P4-E1037-CON. |

### RWB-P7-E1018-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00453 | RWB-ITG-E1018-ITG | GAP-2437 | find it | Record that a secondary slice builds against the platform contracts and fakes of section 12.8 and reads wave-1 tables in its own schema; no dependency row moves. |

### OTHER:rwb-case deployment topology and platform template (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00454 | RWB-ITG-E1018-ITG | GAP-0677 | find it | Publish the rwb-case deployment topology and environment values as values files, not chart defaults. |

### OTHER:RWB-PLT-DB and the secret store (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00456 | RWB-ITG-E1018-ITG | GAP-2438 |  | Fix the rwb-decision login name, keep the migration role and application role apart, and reference it from every P7 story. |

### RWB-P3-E1019-APP; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00459 | RWB-ITG-E1019-ITG | DOR-RWB-ITG-E1019-ITG-12 | section 16, 18 | Section 16 has 16 test rows (TC-E1-019-01 to 16-ITG). The P3 test lists and RTM v7 differ and sit in other documents. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00460 | RWB-ITG-E1019-ITG | GAP-0344 | section 3, 7 | The service contracts own the field names. The story already reads them from the published contracts and treats an absent field as drift. |

### RWB-P3-E1019-APP; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00461 | RWB-ITG-E1019-ITG | GAP-1176 | section 7, 11 | The P3/P4 split of reading and the membership operation are contract decisions that sit outside this story. |

### RWB-P6-E1019-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00464 | RWB-ITG-E1019-ITG | GAP-1174 | section header | Contract dependencies row lists the DP contracts, including RWB-PLT-N001-CON for DP-19 |

### OTHER:Legacy story RWB-AD-014 (Configure queues) and its RWB-E1-019 dependency (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00466 | RWB-ITG-E1019-ITG | GAP-0857 | header | Replace the rule-version endpoints row with this story's two operations and read the RWB-E1-019 dependency as RWB-P3-E1019-APP and RWB-P3-E1019-CON. |

### OTHER:TSD P4 Access and administration v4 (T3.1); 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md; OTHER:FR-P4-005; OTHER:FR-P4-008) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00467 | RWB-ITG-E1019-ITG | GAP-1574 |  | State that a matrix version is dated by validFrom on its reference load; record 756 permission rows for PM-2026.12; mark full role conflict list, its version label and dates, and role row count: Not specified in the source documents (GAP-1574). |

### OTHER:TSD P4 T3.1 (Technical specification P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00468 | RWB-ITG-E1019-ITG | GAP-1567 |  | Remove lov_value and partner_user from T3.1; keep lists of values in TSD P3 and partner identity in TSD S9; rwb-access contract states the LOV versions and partner attributes it reads and refresh rate. |

### OTHER:rwb-access role data (access owner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00469 | RWB-ITG-E1019-ITG | GAP-0683 | 3, 10 | Confirm RW-TEAMMGR holds Reference data A for TEAM, QUEUE and QUEUE_MEMBER and record the grant as rwb-access data; 403 MSG-P4-002 stays the refusal. |

### OTHER:Control register; OTHER:CTL-08 (Business analyst) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00470 | RWB-ITG-E1019-ITG | GAP-1180 | 8 | Register CTL-08 with its text, owner and evidence; then cite the register row in BR2, BR4 and BR14. |

### OTHER:Service story set (Recovery Workbench Service Story Files v1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00472 | RWB-ITG-E1020-ITG | DOR-RWB-ITG-E1020-ITG-21 |  | Create contract story RWB-ITG-E1020-CON, or name the existing CON story this story depends on. |

### RWB-P3-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00474 | RWB-ITG-E1020-ITG | DOR-RWB-ITG-E1020-ITG-10 | find it | Add the missing states: SCR-02 empty, error and no access; SCR-07 empty, loading, error and no access; SCR-09 empty, loading, error and no access. |

### OTHER:23 Document Gaps/Recovery Workbench Assumptions Register v1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00475 | RWB-ITG-E1020-ITG | DOR-RWB-ITG-E1020-ITG-18 | 8 | Add an assumption for DL24 recording the Decision Log recommendation: A, Epic 1 loads allocation, assignment and transfer rules only. Number it at step D1. |

### OTHER:Business Requirements Document (Epic 1), section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00476 | RWB-ITG-E1020-ITG | GAP-1456 | find it | State in section 8.2 that Epic 1 stories keep the W-MAP wave 1 while rwb-payment, rwb-asset and rwb-deviation start in wave 2. |

### OTHER:Service Catalog and RWB-PLT-DB stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00478 | RWB-ITG-E1020-ITG | GAP-0684 | find it | Record the rwb-case service login name, allocated with schema rwb_case, in the Service Catalog and the RWB-PLT-DB stories. |

### RWB-P3-E1020-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00480 | RWB-ITG-E1020-ITG | GAP-3072 | none | Publish case input and stage outcome field names, the queue-and-members element, the handler rule, the DEV-HANDLER parameter row and confirm the four handler role codes against TSD S8 T6.1. |

### OTHER:RWB-PLT-DB (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00481 | RWB-ITG-E1020-ITG | GAP-3207 | none | Publish the per-service database login name of rwb-case and state whether the caseload cap is a queue column, a parameter row or both. |

### RWB-P3-E1020-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00482 | RWB-ITG-E1020-ITG | GAP-3208 | 12.5 | State the Temporal cron expression of the catch-up Schedule for DailyCaseRun where the deployment is described. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00484 | RWB-ITG-E1020-ITG | GAP-2439 | none | Give rule_package_version columns for state, valid-from, approver, generated DRL and SHA-256, and confirm the artifact payload with RWB-PLT-E1072-CON. |

### OTHER:WP C-WEX work package index (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00486 | RWB-ITG-E1020-ITG | GAP-3206 |  | Correct the heading from E1-018 to a scheduling label; RWB-E1-020 stays the subject of the worked example, as the story already states. |

### 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00487 | RWB-ITG-E1020-ITG | GAP-3209 |  | Add one criterion-ownership column to the Legacy map sheet listing the single new story that owns each legacy criterion. |

### 05 Technical architecture/Recovery Workbench Service Template Specification v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00488 | RWB-ITG-E1020-ITG | GAP-0687 |  | Expose replicas, autoscaling bounds, node pool, connection pool size and history archive as chart values with documented defaults; record SIT findings. |

### OTHER:P7 message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00490 | RWB-ITG-E1020-ITG | GAP-2442 |  | Approve the text of MSG-P7-009 and the chain-break warning, and name the per-entry chain result field, then reuse the approved wording. |

### RWB-S8-E1020-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00491 | RWB-ITG-E1020-ITG | GAP-3073 |  | Keep wave 1 and the tentative date; take event names DeviationRaised and DeviationCleared from TSD S8 T0.2 and T5.2.1; build behind the service baseline with no own element; treat DP platform contracts as wave 0 preconditions. |

### OTHER:Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00492 | RWB-ITG-E1020-ITG | GAP-3173 |  | State the wave 1 delivery of rwb-deviation in the service epic and wave plan, and let the rwb-deviation service wave govern later stories. |

### 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00493 | RWB-ITG-E1020-ITG | GAP-2150 | 1 | Section 1, last paragraph: confirm the added contract example RWB-P3-E1042-CON stands beside the RWB-E1-020 worked example and does not replace it. |

### OTHER:Recovery Workbench BRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00499 | RWB-ITG-E1021-ITG | GAP-1456 | 8.2 | State in section 8.2 that a story keeps the wave of its legacy requirement under R5.6 and that a service starts in its own wave per Architecture v5. |

### RWB-P4-E1037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00501 | RWB-ITG-E1021-ITG | GAP-0990 |  | Publish the authorise request and answer schema with its legalHold attribute; confirm the matrix version label in force at 30 November 2026 with the matrix owner; tabulate the Queue and allocation letters in TSD P4 T6.1. |

### OTHER:Platform team chart values for rwb-case (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00502 | RWB-ITG-E1021-ITG | GAP-0691 |  | Publish cluster, node pool, replica counts per environment, ingress host, resource limits and pod disruption budget as chart values; no environment default shipped. |

### OTHER:P5 contract baseline story for rwb.document.events.v1 (not yet assigned) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00503 | RWB-ITG-E1021-ITG | GAP-1036 |  | Publish the producer-side AsyncAPI 3.0 document with the registered JSON schemas for DocumentStored.v1 and DocumentFieldsExtracted.v1, required fields and BACKWARD rule; hand the DocumentStored schema to RWB-P3-E1021-CON. |

### RWB-PLT-NF06-DB; OTHER:P5 database story and the service catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00504 | RWB-ITG-E1021-ITG | GAP-1037 |  | Allocate the rwb-document login name, its grants (schema rwb_document only, no privilege on another schema) and its secret reference. |

### OTHER:TSD S9 T3.1 and PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00510 | RWB-ITG-E1022-ITG | GAP-3103 | none in this story | Publish partner_user fields in TSD S9 T3.1 and PRD; name contract-end Schedule and clock time; decide if recall is an event; confirm the feature |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00514 | RWB-ITG-E1023-ITG | CG-ALL-273 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations?caseId={caseId} through the rwb-deviation provider CON story. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00517 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-12 | 16, 18 | Add TC-E1-023-12-ITG and TC-E1-023-13-ITG to Test Cases v8; align the section 18 test lists to RTM v7. |

### OTHER:Provider CON stories for rwb-access and rwb-deviation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00519 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-21 | header | Name the CON story and add it as a contract dependency once the three unpublished operations are published. |

### 05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml; 05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00520 | RWB-ITG-E1023-ITG | DOR-RWB-ITG-E1023-ITG-8 | 12.2 | Publish GET /api/recovery/deviation/v1/deviations?caseId={caseId}, POST /api/recovery/access/v1/authorise and GET /api/recovery/access/v1/me/permissions. |

### OTHER:BRD (Epic 1 requirement set), section 8.2 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00526 | RWB-ITG-E1023-ITG | GAP-1456 | none | State that an Epic 1 story keeps the business-epic wave; delivery lead confirms the wave per story at build sequencing |

### OTHER:rwb-source-data API contract (P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00527 | RWB-ITG-E1023-ITG | GAP-0695 | 7 | Add interaction read GET /api/recovery/source-data/v1/cases/{caseId}/interactions with page and size parameters |

### RWB-P4-E1039-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00528 | RWB-ITG-E1023-ITG | GAP-0694 | 11 | Publish masking request and response keyed by view field ID, with a masked flag and source column per field |

### OTHER:Backlog story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00534 | RWB-ITG-E1024-ITG | DOR-RWB-ITG-E1024-ITG-21 | header | Create contract story RWB-ITG-E1024-CON; story header now names it as the contract dependency. |

### OTHER:FSD P5 v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00535 | RWB-ITG-E1024-ITG | GAP-1583 |  | Add FR-P5-030, FR-P5-031, AC-P5-022 and AC-P5-023 as wave 1 release gates for REQ-DCM-014, 015 and 020; keep schedule and restore evidence open as OQ-P5-05. |

### OTHER:TSD P5 v2 and the PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00537 | RWB-ITG-E1024-ITG | GAP-1588 | 13 | Drop the EXTEND of ACE Attachment and the document party relation in the next TSD version; state the hub as the record with the file in Blob and metadata in rwb_document; OQ-P5-12 confirms. |

### OTHER:TSD P5 v2 (Document hub v2) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00538 | RWB-ITG-E1024-ITG | GAP-1594 |  | DF-DOC-003 party_id uuid with ACE relationship replaced by person_key varchar(255), business key, no foreign key (D-RCV-35, ADR-010); confirm via OQ-P5-14 |

### OTHER:rwb_document DB story (ACE DB team) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00539 | RWB-ITG-E1024-ITG | GAP-1030 |  | Name the rwb-document database login and its grants per DP-02 |

### OTHER:rwb-document contract stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00540 | RWB-ITG-E1024-ITG | GAP-1032 |  | Field names and the 404 message ID are not in the sources; the story keeps the paths and operation list. |

### OTHER:Story set (contract story for this suite) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00543 | RWB-ITG-E1025-ITG | DOR-RWB-ITG-E1025-ITG-21 | header | Contract dependencies reads Not specified in the source documents. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00544 | RWB-ITG-E1025-ITG | CG-ALL-288 | n/a | Record guarantor_email as an object in the owning document (its absence from the P1 dictionary is the AC4 case), or give its dictionary name. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00546 | RWB-ITG-E1025-ITG | DOR-RWB-ITG-E1025-ITG-9 | 14 | Section 14 lists MSG-GEN-006 and MSG-P5-006 as used. |

### OTHER:rwb-document OpenAPI 3.1 document; OTHER:rwb-case reference-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00547 | RWB-ITG-E1025-ITG | GAP-1039 | 7 | Publish the document-type admin surface (paths, request and response schemas, row-error schema, error codes) and the load template columns in the rwb-document OpenAPI 3.1 document; add the reference-version registration operation to the rwb-case reference-data contract. |

### RWB-PLT-E1044-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00548 | RWB-ITG-E1025-ITG | GAP-1041 | 8 | Allocate the rwb-document login name, secret reference and grants (schema rwb_document only, no privilege on rwb_case) and record them in the service catalogue. |

### RWB-ITG-E1026-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00550 | RWB-ITG-E1026-ITG | DOR-RWB-ITG-E1026-ITG-21 |  | No contract story exists in the set; the story itself cannot create it. |

### RWB-P5-E1041-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00553 | RWB-ITG-E1026-ITG | GAP-1034 | 13 | Fix the scan operation path, verb, request, response (CLEAN or INFECTED) and error shape in the contract story. |

### RWB-P7-E2032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00556 | RWB-ITG-E1027-ITG | GAP-2404 | Header | Read Depends on (build) as None plus H RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON as delivery prerequisites; add C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the published P4 authorise contract to Contract dependencies; story stays Day 1. |

### 06 Data/Recovery Workbench Physical Schema v7; RWB-P7-E1027-CON; OTHER:platform message catalogue (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00559 | RWB-ITG-E1027-ITG | GAP-1236 | 11 | Add the data-date column and inputs digest to schema and contract baseline, state local record retention, and publish the entry format of MSG-P7-009 and MSG-P7-003. |

### RWB-P7-E1027-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00560 | RWB-ITG-E1027-ITG | GAP-1237 | 7 | Freeze the canonical form of RWB-E1-008 BR4 (empty fields as null) and publish one cross-language fixture that the store verifier and every writer reproduce. |

### 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00561 | RWB-ITG-E1027-ITG | GAP-1622 |  | Add a contract version to the DecisionRecorded event, record it on the ledger entry, and dead-letter unknown versions. |

### OTHER:Batch and Scheduling (next version) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00563 | RWB-ITG-E1027-ITG | GAP-1240 |  | The story already describes JOB-13 as a continuous ingest. The change to the 01:00 copy job belongs to the Batch and Scheduling document. |

### OTHER:P7 module specification (FSD P7 A2.6) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00564 | RWB-ITG-E1027-ITG | GAP-1239 |  | Delete A2.6 and its acceptance criteria (AC-P7-006-01 to AC-EXC-P7-006-04). Move the reporting need to the rwb-reporting projection from events. |

### RWB-P3-E1028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00569 | RWB-ITG-E1028-ITG | DOR-RWB-ITG-E1028-ITG-7 | 11 | Replace legacy JOB and DecisionLogWriter wording with the durable timer in CaseWorkflow and the decision-record wording of DP-03. |

### OTHER:FSD P7 acceptance criteria A2.15 and A2.16 with the rwb-case contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00570 | RWB-ITG-E1028-ITG | GAP-1623 | 7 | Record the chosen option: P3 reacts to ApprovalRequested to move case state to Waiting approval and raise the task; align AC-P7-015-01 wording. |

### RWB-P3-E1028-APP; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00571 | RWB-ITG-E1028-ITG | GAP-2202 | 12.2 | Add the two P1 rows (linked-account date query, holiday query) with query and answer shape; name in the P3 contract the operation carrying the wave 1 pause. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00572 | RWB-ITG-E1028-ITG | GAP-2203 | find it | Add escalated_to_role and escalated_at with type, length and optionality, and the TimerBreached payload fields; settle the detail at the baseline review of RWB-P3-E1028-CON. |

### API:(service not named); OTHER:policy pack (matrix version in force at the release date) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00573 | RWB-ITG-E1028-ITG | GAP-0986 | find it | Fix the authorise attribute set for a case read and a timer read, with escalatedToRole and escalatedAt; name the matrix version in force at 30 November 2026; state the escalation grant scope with reason ESCALATED_TO_ROLE, no wider than the caller's role row. |

### OTHER:rwb-case values files and the runbook entry each alert links (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-00574 | RWB-ITG-E1028-ITG | GAP-2204 | find it | Set the poll window, catch-up window, breach band and record-failure rate, confirm them at UAT and record the agreed values in the runbook. Values Not specified in the source documents (GAP-2204). |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_access.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20600 | RWB-ITG-E1019-ITG | R-28517 |  | Grant confirmation of RW-TEAMMGR Reference data A belongs in rwb-access role data. This .sql file has REFERENCE_DATA 'R' for RW-TEAMMGR; no writer exists for .sql. |

### 06 Data/Recovery Workbench Physical Schema v7/rwb_document.sql (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20615 | RWB-ITG-E1024-ITG | R-28542 |  | Line 5 of rwb_document.sql already names login rwb_document. Grants are not in any source, so no story change, per the recommended resolution. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0022 | TimerDue owner recorded as P3 and as PLT | Solution architect | Resolved (directive) |
| GAP-0064 | Wave conflict S8 / EP01 | Tech lead | Resolved (directive) |
| GAP-0341 | E1016 catalog composition across rwb-source-data, rwb-access and rwb-document | Solution architect | Resolved (directive) |
| GAP-0342 | E1017 retention ownership and the P1 interaction path | Solution architect | Resolved (directive) |
| GAP-0343 | E1018 case-created event and decision record move to the platform | Solution architect | Resolved (directive) |
| GAP-0344 | Field names of the P4 session team scope and the P6 notice queue code are not fixed by any source | Service owner of rwb-access and service owner of rwb-comms | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0345 | JOB-03 run surface and exact rerun facade are not specified for an ITG suite | Service owner of rwb-case with the service owner of rwb-source-data | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0346 | Route-decided transfer trigger has no wave 1 owner event | Tech lead | Resolved (directive) |
| GAP-0347 | Claims of the short-lived user JWT and the place of the multi-factor gate are not fixed | Service owner of rwb-access; platform owner of gateway-bff | Resolved (directive) |
| GAP-0348 | RWB-E1-023 integration slice: the S8 deviation read path, the wave of rwb-deviation and the fixture composition are not fixed by the sources | TechX | Resolved (directive) |
| GAP-0349 | E1024 document store split across rwb-document, rwb-case and the shared decision-record topic | Solution architect | Resolved (directive) |
| GAP-0350 | E1025 document-type load path and field dictionary after the reference-data ruling | Solution architect | Resolved (directive) |
| GAP-0351 | E1026 attach and search screen as a gateway-bff composite over P5 and P3 | Solution architect | Resolved (directive) |
| GAP-0352 | E1027 decision codes and reference data move to P3 while the writer and the ledger are PLT and P7 | Solution architect | Resolved (directive) |
| GAP-0353 | E1028 durable timers replace JOB-05 and the P1 account-date path leaves the slice | Solution architect | Resolved (directive) |
| GAP-0481 | The masking rules stay in P1 in the TSD while the Ownership Map rules the table to rwb-access (P4) | Solution architect | Resolved (directive) |
| GAP-0482 | The data_product_access seed of the version in force is only partly specified | Data steward | Resolved (directive) |
| GAP-0483 | The monolith reference-load endpoint has no target owner for an access load | Tech lead | Resolved (directive) |
| GAP-0484 | The DB slice of this legacy key cannot deliver the table DDL, because two other stories already create the tables | ACE database lead | Resolved (directive) |
| GAP-0488 | retention_rule ownership: TSD P1 v3 keeps it in P1, the Ownership Map and Arch v5 move retention to P5 | Solution architect | Resolved (directive) |
| GAP-0489 | The rwb-source-data retention-run contract shape is not specified | Solution architect | Resolved (directive) |
| GAP-0490 | The write-once archive contract (container, path and manifest) belongs to RWB-PLT-TE012-APP and is not specified | Solution architect | Resolved (directive) |
| GAP-0491 | The legal-hold query is a published interface with no REST path in the sources | Solution architect | Resolved (directive) |
| GAP-0571 | The entry-candidate contract: the resource and parameter names, the response entity, its field names, the paging, the error status set and the access rule are not fixed by any source, and this legacy key has no contract story of its own | Tech lead of rwb-source-data with the solution architect and the P3 owner of the case contract | Resolved (directive) |
| GAP-0572 | Whether the entry read is one operation for a business date or one operation per account, and how a page of about 28,100 candidates is cut, are not specified | Tech lead of rwb-source-data with the owner of the rwb-case case creation job | Resolved (directive) |
| GAP-0573 | Which service writes account_ext.dispute_open and the party_ext flags, which right the confirmation needs, and where party_ext.vulnerable comes from on the first write are not settled | Solution architect with the P1 service owner, the P3 owner of the exclusion screen and the P4 owner of the role model | Resolved (directive) |
| GAP-0574 | The ALS batch gate before RWB-ACE-001 lands: v_ace_batch_status is a Section B view, and the behaviour of an entry read for a date whose batch record does not exist yet is not specified | Recovery tech lead with the ACE team lead and the platform team that owns the RWB-ACE-001 sequence | Resolved (directive) |
| GAP-0575 | The shape and the home of the REC-05 break list are not specified, and the table that held it leaves the schema | Data architect with the data steward and the P1 owner of the reconciliation job | Resolved (directive) |
| GAP-0576 | The product group of a candidate row: whether the ACE product_category value is passed through or mapped to the LOV-PRODUCT codes, and what happens to a value outside the list, is not specified | Business analyst, P1 with the center of excellence and the owner of the rwb-case reference data | Resolved (directive) |
| GAP-0674 | gateway-bff composite route for the case screens is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0675 | Per-service login name for rwb-case is not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0676 | Field-level OpenAPI schema of the case resource is not specified | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0677 | Deployment topology detail for rwb-case is not specified | DevOps engineer | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0678 | The per-service database login name of rwb-case is not specified | ACE DB team | Resolved (directive) |
| GAP-0679 | The column-level split of the legacy role and permission tables between rwb-case and rwb-access is not defined | Solution architect | Resolved (directive) |
| GAP-0680 | The column-level definition of queue measures and of the remaining list-of-values columns is not specified | Technical lead, rwb-case | Resolved (directive) |
| GAP-0681 | The queues reference-load template format is not specified | Reference data owner (Shared operations) | Resolved (directive) |
| GAP-0682 | The rollback and verify operations of reference loads sit outside the rwb-case operation set given for this legacy key | Solution architect | Resolved (directive) |
| GAP-0683 | The approver authority for a queues load is assumed, not confirmed | Access owner, rwb-access | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-0857 | rwb-access queue load: the legacy story's endpoints row names rule-version paths that belong to RWB-AD-011 and RWB-AD-012, and depends on the monolith queue story | Business analyst, P4 | Resolved (directive) |
| GAP-0982 | The case-authority request shape, the source of the caller teams and regions, and the case-record personal field list are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0983 | rwb-access policy and catalogue answers: no source names the request and answer field set of the role catalogue, the masking policy read or the data-product authorise answer, nor the marker vocabulary or the masking-exceptions part | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0985 | Role version: roster, row counts, role-file layout, matrix effective date, conflict list and MSG-P4-006 text not specified | Security administrator (RW-SECADM), with the reference data administrator (RW-REFADM) | Resolved (directive) |
| GAP-0986 | rwb-access timer and case read: the authorise request attribute set, the label of the matrix version in force and the scope that prevails under an escalation are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0987 | Authority attributes, matrix version label and role roster for an allocation and queue read | Solution architect of rwb-access | Resolved (directive) |
| GAP-0989 | The authorise attribute set, the policy version labels and the full field-ID roster of the read-only case record view are fixed by no source | Solution architect | Resolved (directive) |
| GAP-0990 | rwb-access transfer and legal hold: the authorise request attributes, the matrix version label in force at the release date and the role holding Queue and allocation U are not fixed by any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1028 | The secondary P5 slice of RWB-E1-016 owns no legacy AC, and the DP10 catalog composition, the retention-class operation path and answer, the consumed contracts, the login and the product code are not fixed as this slice needs them | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1030 | The per-service database login name for rwb-document is not specified | ACE DB team | Resolved (directive) |
| GAP-1031 | The storage account, the container names and the WORM policy of the platform storage product are not fixed in the sources | SCB IT infrastructure | Resolved (directive) |
| GAP-1032 | The request and response field names of the store operations and the not-found message are not specified | Solution architect | Resolved (directive) |
| GAP-1033 | Request and response field names of the three SCR-30 operations, the per-service login name and the text of MSG-GEN-006 are not fixed in the sources | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1034 | The scan operation path of the RWB-P5-E1041-CON malware-scan contract is not specified | Solution architect, with the P5 TechX squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1035 | The SCR-30 route specification in the gateway-bff composite route is not specified | Solution architect, with the gateway-bff squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1036 | Producer-side AsyncAPI and JSON schema of rwb.document.events.v1 are not assigned to a contract story | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1037 | Per-service login name for rwb-document is not specified | ACE database administrator | Resolved (directive) |
| GAP-1038 | The rwb-document login name, the not-found message ID of the case read and the case-read field names are not specified | Solution architect with the ACE DB team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1039 | The load, approve and in-force read shapes for document types are not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1041 | The rwb-document login name and its grants are not specified | ACE database administrator | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1174 | The DP-added platform and P3 contracts are missing from the story dependency lists | Release manager | Resolved (directive) |
| GAP-1175 | DP-08 is claimed while the authorise contract and the guard library are in no dependency list | Solution architect | Resolved (directive) |
| GAP-1176 | The split of the legacy role, queue and membership data between rwb-case and rwb-access is not stated, and the membership read has no published operation | Solution architect | Resolved (directive) |
| GAP-1177 | No source decides whether a reader keeps a local cache of the role and queue data | Solution architect | Resolved (directive) |
| GAP-1178 | The legacy reference-load path has no rwb-comms target, so the legacy access case has no endpoint in this service | Test lead | Resolved (directive) |
| GAP-1179 | The P6 API specification has no operation that exposes the approver role and the approver queue of a notice | Tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1180 | Control CTL-08 is cited by the legacy story and the case story but is absent from the rules register | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1235 | The decision-record write operation is absent from the Ownership Map | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1236 | The full record shape, the data-date column, the inputs digest and the message catalogue entry format are not specified | Data steward | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1237 | The canonical form of the entry hash is not specified | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1238 | Two ce_type values are published for DecisionRecorded | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1239 | The decision-log stream to the data lake is retired but still specified | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1240 | JOB-13 is a 01:00 copy job in the specifications and a continuous ingest in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1402 | Local decision-record library: artefact coordinates, no-case publish path, chain scope and incident routing | Solution architect | Resolved (directive) |
| GAP-1403 | Local decision-record contract: record schema, table shape, shared-topic envelope and message catalogue | Solution architect | Resolved (directive) |
| GAP-1456 | Epic 1 requirement stories sit in services whose Architecture v5 wave is later | Tech lead | Resolved (directive) |
| GAP-1549 | P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1567 | lov_value and partner_user are defined in the P4 technical specification but owned by rwb-case and rwb-partner | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1568 | The four operations Architecture v5 gives rwb-access first (authorise, /me/permissions, /doa-limits, /masking-policies) have no request or answer schema in the API Specification v4 or the P4 appendix, and the group-to-role mapping has no stated read path | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1574 | No source holds the full role conflict list, the role and permission row counts of a version, or the effective-date column of a matrix version | Security administrator with the reference data administrator | Resolved (directive) |
| GAP-1583 | Sizing, backup and the records management position have no FSD feature and no owned artifact | IT lead with the document hub owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1588 | The TSD extends the ACE Attachment object while the requirement makes the hub the system of record in Blob with WORM | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1594 | The FSD identifies the customer on a document by the ACE person key and the TSD by party id | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1617 | The ledger completeness target, the gap alert threshold and the strict-mode wait bound have no value in the BRD or the FSD | Solution architect with the platform administrator | Resolved (directive) |
| GAP-1622 | The decision record is published by 19 services on one topic with no schema version field in the field list | Platform event library owner | Resolved (directive) |
| GAP-1623 | The Waiting approval case state and the approval task are set inside P7 while the case state and the queue belong to rwb-case | Solution architect with the rwb-case contract owner | Resolved (directive) |
| GAP-2016 | Timer row and durable timer kept in step by one activity | Service owner P3 rwb-case with the platform team | Resolved (directive) |
| GAP-2068 | The local decision record has no table, no DDL and no case or trace column | Service owners of the 19 services with P7 rwb-decision | Resolved (directive) |
| GAP-2074 | One chain or 19 chains plus the ledger chain | Service owner P7 rwb-decision with the 19 service owners | Resolved (directive) |
| GAP-2075 | The record that governs while the central ledger lags by up to five minutes | Service owner P7 rwb-decision | Resolved (directive) |
| GAP-2150 | The worked example is a monolith story key with no service and no realignment equivalent | Document owner; analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2202 | The account-date and holiday reads and the deviation pause have no published surface in the target | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2203 | No source gives the field-level detail of the two escalation columns or of the TimerBreached payload | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2204 | No source gives the operational values for a durable timer: poll window, catch-up window, breach band and record-failure rate | DevOps lead | Resolved (directive) |
| GAP-2404 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds five platform contracts and two rwb-case contracts and the story consumes a further authorise operation | Delivery lead | Resolved (directive) |
| GAP-2426 | The decision code, final call, action and outcome values and the payload placement of an archive or purge record are in no source | Solution architect | Resolved (directive) |
| GAP-2427 | The text of MSG-P7-009 and the ids and texts of the not-found answer, the chain-break report and the collection gap alert are not written in any source | Business analyst, P7 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2428 | The JOB-14 timezone, page size, overlap and catch-up values, the property names and the behaviour of the feature flag when off are in no source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2430 | The name of the rwb-decision database login is in no source | ACE team | Resolved (directive) |
| GAP-2431 | The story file at the Work Package path already existed as a partial artefact of the superseded Work Package B-P7-05, with no fragment, no register rows and citations that resolve to nothing | Delivery lead, with the traceability owner | Resolved (directive) |
| GAP-2432 | A secondary slice with an empty acceptance-criteria list owns no legacy criterion while its ten legacy test cases are kept | Traceability owner | Resolved (directive) |
| GAP-2433 | The message text of MSG-P7-009 and of the chain warning MSG-P7-012 is named in the sources but never written | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2434 | The case-creation filter of the ledger read and the field list of its answer are not specified in any source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2435 | TSD P7 still models decision_log_entry.case_id as a uuid with a relationship to recovery_case and gives the row no business-date column | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2436 | The literal rule ID of the ENTER rule of package ENTRY is named in no source | Business analyst, Epic 1 | Resolved (directive) |
| GAP-2437 | A secondary slice carries no build dependency while its fourteen DP rows add eight platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2438 | The per-service database login name of rwb-decision is named in no source | Platform DB owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
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
| GAP-3158 | The retention tables are P1 tables in the story and P5 tables in the Ownership Map | P5 document owner | Resolved (directive) |
| GAP-3159 | The role table is loaded by P3 in the story and owned by P4 in the Ownership Map | P4 access owner | Resolved (directive) |
| GAP-3162 | The case story writes the P1 extension tables | P3 case owner | Resolved (directive) |
| GAP-3173 | Service S8 takes Epic 1 stories in wave 1 although its Arch v5 wave is 2 | Delivery lead | Resolved (directive) |
| GAP-3206 | The work package is labelled (E1-018) while the source worked example is story RWB-E1-020 | Delivery lead | Resolved (directive) |
| GAP-3207 | No source names the rwb-case database login or where the caseload cap is stored | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3208 | The schedule expression of the DailyCaseRun (legacy JOB-03) is not stated by any source | Solution architect | Resolved (directive) |
| GAP-3209 | No single source divides the thirteen legacy criteria of RWB-E1-020 across its seven stories | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3213 | A requirement whose own legacy stories do not cite it | Business analyst | Resolved (directive) |
| GAP-3230 | Two retired items still carry v6 windows and dependencies | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-ITG-E1016-ITG | skipped AC ID | 92 | missing: AC1, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11 |
| RWB-ITG-E1019-ITG | skipped AC ID | 106 | missing: AC11, AC12 |
| RWB-ITG-E1024-ITG | skipped AC ID | 104 | missing: AC10, AC11, AC12 |
