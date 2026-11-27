# RWB-PLT-WF Temporal workflow platform - review pack

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 16 |
| Resolved in the stories | 161 |
| Cross-document (pending in another document) | 377 |
| Not applied (value not in the sources) | 11 |
| Open business decisions | 9 |
| Register gaps linked | 97 |
| Unconfirmed assumptions | 0 |
| Lint findings | 1 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-PLT-E1070-APP | 10 | 33 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E1070 APP Temporal platform on the ACE AKS clusters v2.md |
| RWB-PLT-E1070-CON | 8 | 31 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E1070 CON Temporal platform on the ACE AKS clusters - contract v2.md |
| RWB-PLT-E1071-APP | 17 | 37 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E1071 APP Temporal worker and SDK in the recovery module v2.md |
| RWB-PLT-E1071-CON | 21 | 81 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E1071 CON Temporal worker and SDK in the recovery module - contract v2.md |
| RWB-PLT-E2037-APP | 8 | 30 | 4 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2037 APP Temporal observability and run books v2.md |
| RWB-PLT-E2037-CON | 6 | 27 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2037 CON Temporal observability and run books - contract v2.md |
| RWB-PLT-E2038-APP | 13 | 11 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 APP Temporal security, codec server and admin audit v2.md |
| RWB-PLT-E2038-CON | 11 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 CON Temporal security, codec server and admin audit - contract v2.md |
| RWB-PLT-E2039-APP | 11 | 32 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2039 APP Temporal resilience backup, failover, upgrade and archive v2.md |
| RWB-PLT-E2039-CON | 5 | 27 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2039 CON Temporal resilience backup, failover, upgrade and archive - contract v2.md |
| RWB-PLT-E2040-APP | 9 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2040 APP Workflow versioning and replay test gate v2.md |
| RWB-PLT-E2040-CON | 7 | 13 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT E2040 CON Workflow versioning and replay test gate - contract v2.md |
| RWB-PLT-N003-INF | 8 | 6 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT N003 INF Temporal namespace rwb-recovery and codec key - infrastructure v2.md |
| RWB-PLT-N010-APP | 9 | 5 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT N010 APP Workflow kit templates and codec server v2.md |
| RWB-PLT-N010-CON | 7 | 3 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT N010 CON Workflow kit templates - interface and fake - contract v2.md |
| RWB-PLT-NF08-INF | 11 | 9 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-PLT-WF Temporal workflow platform/RWB PLT NF08 INF Temporal platform baseline - infrastructure v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-ITG-E1011-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P3-E1011-APP, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1011-APP, RWB-S5-E1011-APP | R-21929 | GAP-2972 | Register gap | TechX and the data steward and data product owner | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights, its run cadence and the owning row of the asset table, and the data-lake and Power BI target of the legacy key is removed | Confirm at the wave-1 design gate: the platform release train as the source of the seven platform CONs; the rwb-source-data contract as the only ACE-side read, with the FSD S5 view names read as the product behind it; the three quality tables, check names and read operations as the service design; the two quality reads in Platform administration right R; the asset table as an S5 object read in rwb_asset; and a daily Schedule with a cron and alert groups set as configuration. |
| RWB-ITG-E1017-ITG, RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-TE012-APP, RWB-PLT-E1071-CON, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-AD021-CON, RWB-P5-E1017-APP, RWB-P7-E1017-APP | R-21974 | GAP-1029 | Register gap | Solution architect, with the Compliance and PDPA officer and the platform storage owner | The P5 retention slice has no source value for its retention periods, its document age basis, its retention-load and run-read paths, its archive container name and its login, and the three contracts it consumes at run time are not in its contract-dependency list | Build the P5 slice on the recorded defaults: RET-2026.11 at 24 months for DP10 documents on created_at with end action ARCHIVE until Compliance supplies the bank schedule (DL26); the shared retention contract shape of RWB-P5-AD021-CON for the retention-class and document-retention reads, with the four admin operations on /api/recovery/document/v1; the write-once container rwb-docs-archive of RWB-PLT-TE012-APP with a manifest of row count and SHA-256 per file; the phrase 'the rwb-document login (DP-02)'; and the P3 case, P3 reference-data and P7 decision-record contracts named in 12.2 and 12.8 with their fakes. When Compliance supplies the schedule, load it as a new rule version with no code change; when the platform and contract owners publish, add the five H rows and the three consumed contracts to the plan, re-run the dependency check and swap each fake for the real contract in the same iteration. |
| RWB-PLT-E1071-CON, RWB-S7-E6013-APP, RWB-S7-E6014-APP, RWB-S7-E6014-CON | R-23202 | GAP-3018 | Register gap | Tech lead of rwb-writeoff with the P7 owner of the rule package and the Finance owner of the tax criteria | The tax criteria version, the remittance channel of R-WO-51, the home of the remittance record and the scan trigger have no owner, table or contract in rwb-writeoff | Publish the working read of ASM-B2-S7-002-1 to ASM-B2-S7-002-6 in RWB-S7-E6014-CON and apply it to RWB-S7-E6014-APP: tax_criteria_version is a package fact of rwb-decision read with its version and recorded with the outcome; the tax-criteria result is write_off.tax_criteria_met and the post charge off remittance is write_off.recovered_after with no new table or column; the R-WO-51 confirmation reaches the step as a signal the parent CaseWorkflow forwards and no subscription is declared; the monthly scan Schedule from JOB-16 belongs to RWB-S7-E6013-APP and the DP-10, DP-04 and DP-09 rows are recorded as absent rather than added; the three consumed rows are declared as class C rows on the baseline and faked. Confirm with the P7 owner of the rule package and the Finance owner of the tax criteria at the wave 4 contract freeze. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-S7-E6020-APP, RWB-S7-E6020-CON | R-23236 | GAP-3031 | Register gap | Solution architect; business lead | RWB-S7-E6020-APP: the review date has no property, field ID, column or list, the legacy timer table is not S7's, R-WO-17's owner conflicts with the FSD role and the permission table, the plan's C row is empty while the step consumes four contracts, DP-04, DP-09 and DP-10 are absent, and no source publishes a rule, a message or a state for a date in the past or a second decision at DEFERRED | Keep the plan's H, C, I and X rows as they stand; carry the review date as an additive request property recorded in the decision record and the case move, with no column and no field ID until the business lead and rwb-case confirm them; set the review timer as a durable workflow timer and let rwb-case own the timer row; map R-WO-17's owner to the roles that hold right A for the act and to the write-off team for the return; declare the four consumed rows in sections 12.2 and 12.8 and record the absent DP-04, DP-09 and DP-10 rows; leave a second decision at DEFERRED and a past review date unpublished and tracked |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28693 | GAP-2047 | Register gap | Solution architect with Risk and Internal Audit | The decision log is now written locally by each service and sealed centrally | Version 4 measures the local decision record of each service and the central ledger of P7 rwb-decision as two instances of the same two alerts, with the chain check read per service and once for the ledger. |
| RWB-ITG-E1073-ITG, RWB-PLT-E2037-APP, RWB-PLT-E2037-CON, RWB-P2-E1073-APP, RWB-P3-E1073-APP, RWB-P3-E1073-CON, RWB-P3-E1073-INF, RWB-P6-E1073-APP, RWB-P7-E1073-APP | R-28694 | GAP-2051 | Register gap | P7 rwb-decision with Compliance and Internal Audit | The hash chain check now spans 19 local chains and one central ledger | Version 4 raises the alert on the local chain of each service and once on the central ledger, and attributes a break to the service whose chain fails; the run book of RWB-E1-073 and RWB-E2-037 names the check. |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35380 | ASM-0247 | Register assumption |  | Masking rules are held in rwb_access.masking_rule, owned by P4, set by Compliance under DL26 and served by GET /masking-policies; v5 copies no rule. | Compliance and PDPA officer |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35381 | ASM-0264 | Register assumption |  | Tables with no data-product row keep no retention period in this version; the source schedule covers data products and document types only, as DL26 asks. |  |
| RWB-ITG-E1008-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1057-ITG, RWB-ITG-TE004-ITG, RWB-ITG-E2003-ITG, RWB-ITG-E2016-ITG, RWB-ITG-E2024-ITG, RWB-ITG-E2025-ITG, RWB-ITG-E2026-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E6025-ITG, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-CON, RWB-PLT-E1042-OPS, RWB-PLT-TE004-APP, RWB-PLT-TE011-APP, RWB-PLT-TE012-APP, RWB-PLT-E2039-APP, RWB-PLT-E2039-CON, RWB-P1-E1016-APP, RWB-P1-E1016-DB, RWB-P1-E1017-APP, RWB-P1-E1068-APP, RWB-P1-E2034-APP, RWB-P2-E2003-APP, RWB-P2-E2034-APP, RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E1031-CON, RWB-P3-E1035-APP, RWB-P3-E1042-APP, RWB-P3-E1042-CON, RWB-P3-E2016-APP, RWB-P3-E2016-CON, RWB-P3-E2024-APP, RWB-P3-E6025-APP, RWB-P4-AD004-APP, RWB-P4-AD004-CON, RWB-P4-AD006-DB, RWB-P4-E1008-APP, RWB-P4-E1016-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1039-DB, RWB-P4-E1064-APP, RWB-P4-E2003-APP, RWB-P4-E2019-APP, RWB-P4-E2026-APP, RWB-P4-E8016-APP, RWB-P4-E8016-CON, RWB-P5-AD021-APP, RWB-P5-AD021-CON, RWB-P5-E1016-APP, RWB-P5-E1017-APP, RWB-P5-E1025-APP, RWB-P5-E1033-APP, RWB-P5-E1041-APP, RWB-P5-E1041-CON, RWB-P5-E1046-APP, RWB-P5-E1050-APP, RWB-P5-E1050-CON, RWB-P5-E1050-OPS, RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1057-APP, RWB-P5-E1062-APP, RWB-P5-E1065-APP, RWB-P5-E2016-APP, RWB-P5-E2018-APP, RWB-P5-E2024-APP, RWB-P5-E2025-APP, RWB-P5-E2025-OPS, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-P6-E4042-APP, RWB-P6-E4042-CON, RWB-P7-E1008-APP, RWB-P7-E1008-CON, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-P7-E1017-APP, RWB-P7-E2005-APP, RWB-P7-E2017-APP, RWB-P7-E2024-APP, RWB-P7-E2025-APP, RWB-P7-E2026-APP, RWB-S2-E2025-APP, RWB-S2-E2026-APP, RWB-S4-E2025-APP, RWB-S7-E6025-APP, RWB-S7-E6025-CON, RWB-S8-E1023-APP, RWB-S9-E1057-APP | R-35383 | ASM-0355 | Register assumption |  | The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under DL26. | Compliance team issues the rule content and P4 confirms the masking_rule rows in the next release. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-PLT-E1070-APP | R-07225 | DOR-RWB-PLT-E1070-APP-17 | find it | Definition of Ready item 17 Dependencies: Fail | RWB-P7-E1073-CON is not in the header dependency rows supplied; its body section was not in the text given. RWB-PLT-E1056-OPS state sits in its own story; both need source text or the owning story to fix. |
| RWB-PLT-E1071-APP | R-07234 | DOR-RWB-PLT-E1071-APP-17 | header | Definition of Ready item 17 Dependencies: Fail | TE001 move applied (its build status is open in the story). RWB-P7-E1073-CON is not in this chunk's story text, so its removal needs the section that holds it. |
| RWB-PLT-E1071-APP | R-18652 | DOR-RWB-PLT-E1071-APP-10 | 10 | Definition of Ready item 10 Screens and states: Partial | Section 10 text is not in this chunk; needs a later chunk containing section 10. |
| RWB-PLT-E2037-APP | R-07252 | DOR-RWB-PLT-E2037-APP-14 | find it | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story or project .md files. Not specified in the source documents (DOR-RWB-PLT-E2037-APP-14). |
| RWB-PLT-E2037-APP | R-07255 | DOR-RWB-PLT-E2037-APP-22 | find it | Definition of Ready item 22 Fake published: Fail | Story CON v1 says fakes publish on Day 1 but records no version. Not specified in the source documents (DOR-RWB-PLT-E2037-APP-22). |
| RWB-PLT-E2037-APP | R-18687 | DOR-RWB-PLT-E2037-APP-4 | 8 | Definition of Ready item 4 Business rules: Partial | Adding AC and TC for BR6 and BR10 needs exact old text from sections 7 and 16, which are not in this chunk. |
| RWB-PLT-E2037-APP | R-26668 | CG-ALL-1726 | 12.5 | Criteria and tests keep legacy job and decision-log wording | The JOB-nn and decision-log wording is in AC8 and TC-E2-037-09, which are not in this chunk, so no exact old text can anchor the edit. |
| RWB-PLT-E2038-APP | R-07261 | DOR-RWB-PLT-E2038-APP-14 | header | Definition of Ready item 14 Epic design: Fail | No signed epic design record in the story, the Epic 2 requirements, or the 03/22/23 folders (searched for epic design sign-off). Sign-off would be invented; left open. |
| RWB-PLT-E2038-APP | R-07265 | DOR-RWB-PLT-E2038-APP-23 | 3 | Definition of Ready item 23 Contract version fixed: Fail | No contract version for RWB-PLT-E2038-CON in the verified contract JSON (_work/msr/directive/mp/esc/verified) or 03 Requirements. Only /v1 path and Temporal 1.30 (L57) exist; version would be invented. |
| RWB-PLT-E2039-APP | R-09202 | GAP-1670 | header | Several platform targets are unset: recovery point and time, the per-namespace quotas, the key rotation period and the retention periods | Values for recovery point, namespace quotas, rotation and retention are not in the sources. PRD P3 and P7 show the ACE objectives as '(value not set)' and 'open: DL11'. Needs DL11 and DL26. |
| RWB-PLT-E2039-CON | R-18716 | DOR-RWB-PLT-E2039-CON-18 | 8 | Definition of Ready item 18 Open decisions: Partial | DL26 assumptions are not referenced in story text, so the item stays open for that part. |

## 5. Cross-document changes (pending in the target document)


### 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (148)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14286 | RWB-PLT-E1070-APP | CG-ALL-1630 | header | Renumber the duplicate FR-PLT-001 entry in the PRD's next version. |
| CDC-14287 | RWB-PLT-E1070-APP | CG-ALL-1631 | header | Renumber the duplicate FR-PLT-009 entry in the PRD's next version. |
| CDC-14288 | RWB-PLT-E1070-APP | CG-ALL-1632 | header | Renumber the duplicate FR-PLT-010 entry in the PRD's next version. |
| CDC-14289 | RWB-PLT-E1070-APP | CG-ALL-1633 | header | Renumber the duplicate FR-PLT-011 entry in the PRD's next version. |
| CDC-14290 | RWB-PLT-E1070-APP | CG-ALL-1634 | header | Renumber the duplicate FR-PLT-012 entry in the PRD's next version. |
| CDC-14291 | RWB-PLT-E1070-APP | CG-ALL-1635 | Header | Renumber the duplicate FR-PLT-013 row in the PRD's next version so each FR-PLT-013 ID has one meaning. |
| CDC-14292 | RWB-PLT-E1070-APP | CG-ALL-1636 | Header | Renumber the duplicate FR-PLT-016 row in the PRD's next version so each FR-PLT-016 ID has one meaning. |
| CDC-14293 | RWB-PLT-E1070-APP | CG-ALL-1637 | Header | Renumber the duplicate FR-PLT-017 row in the PRD's next version so each FR-PLT-017 ID has one meaning. |
| CDC-14294 | RWB-PLT-E1070-APP | CG-ALL-1638 | Header | Renumber the duplicate FR-PLT-018 row in the PRD's next version so each FR-PLT-018 ID has one meaning. |
| CDC-14295 | RWB-PLT-E1070-APP | CG-ALL-1639 | Header | Renumber the duplicate FR-PLT-021 row in the PRD's next version so each FR-PLT-021 ID has one meaning. |
| CDC-14296 | RWB-PLT-E1070-APP | CG-ALL-1640 | Header | Renumber the duplicate FR-PLT-022 row in the PRD's next version so each FR-PLT-022 ID has one meaning. |
| CDC-14297 | RWB-PLT-E1070-APP | CG-ALL-1641 | Header | Renumber the duplicate FR-PLT-023 row in the PRD's next version so each FR-PLT-023 ID has one meaning. |
| CDC-14298 | RWB-PLT-E1070-APP | CG-ALL-1642 | Header | Renumber the duplicate FR-PLT-024 row in the PRD's next version so each FR-PLT-024 ID has one meaning. |
| CDC-14299 | RWB-PLT-E1070-APP | CG-ALL-1643 | Header | Renumber the duplicate FR-PLT-025 row in the PRD's next version so each FR-PLT-025 ID has one meaning. |
| CDC-14300 | RWB-PLT-E1070-APP | CG-ALL-1644 | Header | Renumber the duplicate FR-PLT-026 row in the PRD's next version so each FR-PLT-026 ID has one meaning. |
| CDC-14301 | RWB-PLT-E1070-APP | CG-ALL-1645 | header | Renumber the duplicate FR-PLT-028 in the PRD's next version. |
| CDC-14302 | RWB-PLT-E1070-APP | CG-ALL-1646 | header | Renumber the duplicate FR-PLT-029 in the PRD's next version. |
| CDC-14303 | RWB-PLT-E1070-APP | DOR-RWB-PLT-E1070-APP-2 | 18 | Renumber the duplicate ids FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and the 13 further duplicates flagged by detcheck in the PRD's next version. |
| CDC-14314 | RWB-PLT-E1070-CON | CG-ALL-1650 |  | Renumber the duplicate FR-PLT-001 row in the PRD's next version so each ID has one meaning. |
| CDC-14315 | RWB-PLT-E1070-CON | CG-ALL-1651 |  | Renumber the duplicate FR-PLT-009 row in the PRD's next version so each ID has one meaning. |
| CDC-14316 | RWB-PLT-E1070-CON | CG-ALL-1652 | header | Renumber the second FR-PLT-010 (transactional outbox) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14317 | RWB-PLT-E1070-CON | CG-ALL-1653 | header | Renumber the second FR-PLT-011 (inbox dedupe, retry ladder, dead-letter) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14318 | RWB-PLT-E1070-CON | CG-ALL-1654 | header | Renumber the second FR-PLT-012 (idempotency key) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14319 | RWB-PLT-E1070-CON | CG-ALL-1655 | header | Renumber the second FR-PLT-013 (RFC 9457 problem envelope) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14320 | RWB-PLT-E1070-CON | CG-ALL-1656 | header | Renumber the second FR-PLT-016 (feature flags with removal date) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14321 | RWB-PLT-E1070-CON | CG-ALL-1657 | header | Renumber the second FR-PLT-017 (parameter and configuration client) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14322 | RWB-PLT-E1070-CON | CG-ALL-1658 | header | Renumber the second FR-PLT-018 (reference-data client) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14323 | RWB-PLT-E1070-CON | CG-ALL-1659 | header | Renumber the second FR-PLT-021 (cluster, namespace, retention, search attributes) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14324 | RWB-PLT-E1070-CON | CG-ALL-1660 | header | Renumber the second FR-PLT-022 (versioned workflow kit) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14325 | RWB-PLT-E1070-CON | CG-ALL-1661 | header | Renumber the second FR-PLT-023 (schedules and durable timers) row in the functional table to a new free ID in the PRD's next version. |
| CDC-14326 | RWB-PLT-E1070-CON | CG-ALL-1662 | header | Renumber the duplicate FR-PLT-024 so that each ID has one meaning (retry policy, versus backup, failover, archive, replay gate) |
| CDC-14327 | RWB-PLT-E1070-CON | CG-ALL-1663 | header | Renumber the duplicate FR-PLT-025 so that each ID has one meaning (stuck-workflow scan, versus smoke workflow, codec) |
| CDC-14328 | RWB-PLT-E1070-CON | CG-ALL-1664 | header | Renumber the duplicate FR-PLT-026 so that each ID has one meaning (mutual TLS, versus admin audit, break-glass decode) |
| CDC-14329 | RWB-PLT-E1070-CON | CG-ALL-1665 | header | Renumber the duplicate FR-PLT-028 so that each ID has one meaning (topics, retry and dead-letter, versus ACLs, registry) |
| CDC-14330 | RWB-PLT-E1070-CON | CG-ALL-1666 | header | Renumber the duplicate FR-PLT-029 so that each ID has one meaning (Blob, key store and transfer, versus other resources) |
| CDC-14333 | RWB-PLT-E1070-CON | DOR-RWB-PLT-E1070-CON-2 | 18 | Give each FR-PLT ID with two meanings (FR-PLT-001, 009, 010, 011 and 13 more) one meaning in the PRD |
| CDC-14350 | RWB-PLT-E1071-APP | CG-ALL-1674 | header | Renumber the duplicate FR-PLT-001 definition in the next PRD version. |
| CDC-14351 | RWB-PLT-E1071-APP | CG-ALL-1675 | header | Renumber the duplicate FR-PLT-009 definition in the next PRD version. |
| CDC-14352 | RWB-PLT-E1071-APP | CG-ALL-1676 | header | Renumber the duplicate FR-PLT-010 definition in the next PRD version. |
| CDC-14353 | RWB-PLT-E1071-APP | CG-ALL-1677 | header | Renumber the duplicate FR-PLT-011 definition in the next PRD version. |
| CDC-14354 | RWB-PLT-E1071-APP | CG-ALL-1678 | header | Renumber the duplicate FR-PLT-012 definition in the next PRD version. |
| CDC-14355 | RWB-PLT-E1071-APP | CG-ALL-1679 |  | Renumber the second FR-PLT-013 entry in the PRD functional table so each ID has one meaning. |
| CDC-14356 | RWB-PLT-E1071-APP | CG-ALL-1680 |  | Renumber the second FR-PLT-014 entry in the PRD functional table so each ID has one meaning. |
| CDC-14357 | RWB-PLT-E1071-APP | CG-ALL-1681 |  | Renumber the second FR-PLT-015 entry in the PRD functional table so each ID has one meaning. |
| CDC-14358 | RWB-PLT-E1071-APP | CG-ALL-1682 |  | Renumber the second FR-PLT-016 entry in the PRD functional table so each ID has one meaning. |
| CDC-14359 | RWB-PLT-E1071-APP | CG-ALL-1683 |  | Renumber the second FR-PLT-017 entry in the PRD functional table so each ID has one meaning. |
| CDC-14360 | RWB-PLT-E1071-APP | CG-ALL-1684 |  | Renumber the second FR-PLT-018 entry in the PRD functional table so each ID has one meaning. |
| CDC-14361 | RWB-PLT-E1071-APP | CG-ALL-1685 |  | Renumber the second FR-PLT-021 entry in the PRD functional table so each ID has one meaning. |
| CDC-14362 | RWB-PLT-E1071-APP | CG-ALL-1686 |  | Renumber the second FR-PLT-022 entry in the PRD functional table so each ID has one meaning. |
| CDC-14363 | RWB-PLT-E1071-APP | CG-ALL-1687 |  | Renumber the second FR-PLT-023 entry in the PRD functional table so each ID has one meaning. |
| CDC-14364 | RWB-PLT-E1071-APP | CG-ALL-1688 |  | Renumber the second FR-PLT-024 entry in the PRD functional table so each ID has one meaning. |
| CDC-14365 | RWB-PLT-E1071-APP | CG-ALL-1689 | header | Renumber the duplicate FR-PLT-025 in the PRD's next version |
| CDC-14366 | RWB-PLT-E1071-APP | CG-ALL-1690 | header | Renumber the duplicate FR-PLT-026 in the PRD's next version |
| CDC-14367 | RWB-PLT-E1071-APP | CG-ALL-1691 | header | Renumber the duplicate FR-PLT-028 in the PRD's next version |
| CDC-14368 | RWB-PLT-E1071-APP | CG-ALL-1692 | header | Renumber the duplicate FR-PLT-029 in the PRD's next version |
| CDC-14370 | RWB-PLT-E1071-APP | DOR-RWB-PLT-E1071-APP-2 | 18 | Renumber every duplicate FR-PLT ID named in the detcheck (FR-PLT-001, 009, 010, 011 and 15 more) in the next version |
| CDC-14384 | RWB-PLT-E1071-CON | CG-ALL-1700 | header | Renumber the duplicate FR-PLT-001 entry in the PRD's next version. |
| CDC-14385 | RWB-PLT-E1071-CON | CG-ALL-1701 | header | Renumber the duplicate FR-PLT-009 (the OpenAPI contract-first row) in the PRD's next version so each ID has one meaning. |
| CDC-14386 | RWB-PLT-E1071-CON | CG-ALL-1702 | header | Renumber the duplicate FR-PLT-010 (the transactional outbox row) in the PRD's next version so each ID has one meaning. |
| CDC-14387 | RWB-PLT-E1071-CON | CG-ALL-1703 | header | Renumber the duplicate FR-PLT-011 (the inbox dedupe row) in the PRD's next version so each ID has one meaning. |
| CDC-14388 | RWB-PLT-E1071-CON | CG-ALL-1704 | header | Renumber the duplicate FR-PLT-012 (the idempotency key row) in the PRD's next version so each ID has one meaning. |
| CDC-14389 | RWB-PLT-E1071-CON | CG-ALL-1705 | header | Renumber the duplicate FR-PLT-013 (the RFC 9457 problem envelope row) in the PRD's next version so each ID has one meaning. |
| CDC-14390 | RWB-PLT-E1071-CON | CG-ALL-1706 | header | Renumber the duplicate FR-PLT-014 (the local decision record row) in the PRD's next version so each ID has one meaning. |
| CDC-14391 | RWB-PLT-E1071-CON | CG-ALL-1707 | header | Renumber the duplicate FR-PLT-015 (the daily hash-chain check row) in the PRD's next version so each ID has one meaning. |
| CDC-14392 | RWB-PLT-E1071-CON | CG-ALL-1708 | header | Renumber the duplicate FR-PLT-016 (the feature flags row) in the PRD's next version so each ID has one meaning. |
| CDC-14393 | RWB-PLT-E1071-CON | CG-ALL-1709 | header | Renumber the duplicate FR-PLT-017 (the parameter and configuration client row) in the PRD's next version so each ID has one meaning. |
| CDC-14394 | RWB-PLT-E1071-CON | CG-ALL-1710 | header | Renumber the duplicate FR-PLT-018 (the reference-data client row) in the PRD's next version so each ID has one meaning. |
| CDC-14395 | RWB-PLT-E1071-CON | CG-ALL-1711 | header | Renumber the duplicate definition of FR-PLT-021 (Cluster, namespace, retention, search attributes) in the next PRD version so the ID has one meaning. |
| CDC-14396 | RWB-PLT-E1071-CON | CG-ALL-1712 | header | Renumber the duplicate definition of FR-PLT-022 (versioned workflow kit) in the next PRD version so the ID has one meaning. |
| CDC-14397 | RWB-PLT-E1071-CON | CG-ALL-1713 | header | Renumber the duplicate definition of FR-PLT-023 (schedules and durable timers) in the next PRD version so the ID has one meaning. |
| CDC-14398 | RWB-PLT-E1071-CON | CG-ALL-1714 | header | Renumber the duplicate definition of FR-PLT-024 (retry policy, backup, failover, archive, replay gate) in the next PRD version so the ID has one meaning. |
| CDC-14399 | RWB-PLT-E1071-CON | CG-ALL-1715 | header | Renumber the duplicate definition of FR-PLT-025 (stuck-workflow scan, smoke workflow, codec) in the next PRD version so the ID has one meaning. |
| CDC-14400 | RWB-PLT-E1071-CON | CG-ALL-1716 | header | Renumber the duplicate definition of FR-PLT-026 (mutual TLS, admin audit, break-glass decode) in the next PRD version so the ID has one meaning. |
| CDC-14401 | RWB-PLT-E1071-CON | CG-ALL-1717 | header | Renumber the duplicate definition of FR-PLT-028 (topics, retry and dead-letter, ACLs, registry) in the next PRD version so the ID has one meaning. |
| CDC-14402 | RWB-PLT-E1071-CON | CG-ALL-1718 | header | Renumber the duplicate definition of FR-PLT-029 (blob, key store and transfer resources) in the next PRD version so the ID has one meaning. |
| CDC-14405 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-2 | 18 | Give FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and the 15 other flagged FR IDs one meaning each |
| CDC-14563 | RWB-PLT-E2037-APP | CG-ALL-1727 | Header | Renumber the duplicate FR-PLT-001 in the PRD's next version. |
| CDC-14564 | RWB-PLT-E2037-APP | CG-ALL-1728 | Header | Renumber the duplicate FR-PLT-009 in the PRD's next version. |
| CDC-14565 | RWB-PLT-E2037-APP | CG-ALL-1729 | Header | Renumber the duplicate FR-PLT-010 in the PRD's next version. |
| CDC-14566 | RWB-PLT-E2037-APP | CG-ALL-1730 | Header | Renumber the duplicate FR-PLT-011 in the PRD's next version. |
| CDC-14567 | RWB-PLT-E2037-APP | CG-ALL-1731 | Header | Renumber the duplicate FR-PLT-012 in the PRD's next version. |
| CDC-14568 | RWB-PLT-E2037-APP | CG-ALL-1732 | Header | Renumber the duplicate FR-PLT-013 in the PRD's next version. |
| CDC-14569 | RWB-PLT-E2037-APP | CG-ALL-1733 | header | Renumber one of the two FR-PLT-021 definitions in the next PRD version so each ID has one meaning. |
| CDC-14570 | RWB-PLT-E2037-APP | CG-ALL-1734 | header | Renumber one of the two FR-PLT-022 definitions in the next PRD version so each ID has one meaning. |
| CDC-14571 | RWB-PLT-E2037-APP | CG-ALL-1735 | header | Renumber one of the two FR-PLT-023 definitions in the next PRD version so each ID has one meaning. |
| CDC-14572 | RWB-PLT-E2037-APP | CG-ALL-1736 | header | Renumber one of the two FR-PLT-024 definitions in the next PRD version so each ID has one meaning. |
| CDC-14573 | RWB-PLT-E2037-APP | CG-ALL-1737 | header | Renumber one of the two FR-PLT-025 definitions in the next PRD version so each ID has one meaning. |
| CDC-14574 | RWB-PLT-E2037-APP | CG-ALL-1738 | header | Renumber one of the two FR-PLT-026 definitions in the next PRD version so each ID has one meaning. |
| CDC-14575 | RWB-PLT-E2037-APP | CG-ALL-1739 | header | Renumber one of the two FR-PLT-028 definitions in the next PRD version so each ID has one meaning. |
| CDC-14576 | RWB-PLT-E2037-APP | CG-ALL-1740 | header | Renumber one of the two FR-PLT-029 definitions in the next PRD version so each ID has one meaning. |
| CDC-14579 | RWB-PLT-E2037-APP | DOR-RWB-PLT-E2037-APP-2 | 18 | Give FR-PLT-001, FR-PLT-009, FR-PLT-010 and FR-PLT-011 (and the 10 others flagged) one meaning each. |
| CDC-14588 | RWB-PLT-E2037-CON | CG-ALL-1746 | header | Renumber the duplicate FR-PLT-001 row in the PRD's next version. |
| CDC-14589 | RWB-PLT-E2037-CON | CG-ALL-1747 | header | Renumber the duplicate FR-PLT-009 row in the PRD's next version. |
| CDC-14590 | RWB-PLT-E2037-CON | CG-ALL-1748 | header | Renumber the duplicate FR-PLT-010 row in the PRD's next version. |
| CDC-14591 | RWB-PLT-E2037-CON | CG-ALL-1749 | header | Renumber the duplicate FR-PLT-011 row (Inbox dedupe, retry ladder and dead-letter path meaning) to a free ID in the next PRD version. |
| CDC-14592 | RWB-PLT-E2037-CON | CG-ALL-1750 | header | Renumber the duplicate FR-PLT-012 row (Idempotency key meaning) to a free ID in the next PRD version. |
| CDC-14593 | RWB-PLT-E2037-CON | CG-ALL-1751 | header | Renumber the duplicate FR-PLT-013 row (RFC 9457 problem envelope meaning) to a free ID in the next PRD version. |
| CDC-14594 | RWB-PLT-E2037-CON | CG-ALL-1752 | header | Renumber the duplicate FR-PLT-021 row (Cluster, namespace, retention, search attributes meaning) to a free ID in the next PRD version. |
| CDC-14595 | RWB-PLT-E2037-CON | CG-ALL-1753 | header | Renumber the duplicate FR-PLT-022 row (versioned workflow kit meaning) to a free ID in the next PRD version. |
| CDC-14596 | RWB-PLT-E2037-CON | CG-ALL-1754 | header | Renumber the duplicate FR-PLT-023 row (Schedules and durable timers replace Quartz meaning) to a free ID in the next PRD version. |
| CDC-14597 | RWB-PLT-E2037-CON | CG-ALL-1755 | header | Renumber the duplicate FR-PLT-024 row (retry policy, backup, failover, archive, replay gate meaning) to a free ID in the next PRD version. |
| CDC-14598 | RWB-PLT-E2037-CON | CG-ALL-1756 | header | Renumber the duplicate FR-PLT-025 row (stuck-workflow scan, smoke workflow, codec meaning) to a free ID in the next PRD version. |
| CDC-14599 | RWB-PLT-E2037-CON | CG-ALL-1757 | header | Renumber the duplicate FR-PLT-026 row (mutual TLS, admin audit, break-glass decode meaning) to a free ID in the next PRD version. |
| CDC-14600 | RWB-PLT-E2037-CON | CG-ALL-1758 | header | Renumber the duplicate FR-PLT-028 row (topics, retry and dead-letter topics, ACLs, registry meaning) to a free ID in the next PRD version. |
| CDC-14601 | RWB-PLT-E2037-CON | CG-ALL-1759 | Header | Renumber the duplicate FR-PLT-029 (the Blob, key store and transfer resources entry) in the next PRD version. |
| CDC-14604 | RWB-PLT-E2037-CON | DOR-RWB-PLT-E2037-CON-2 | 18 | Resolve the duplicate meanings of FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and the ten further duplicate IDs detcheck names, in the next PRD version. |
| CDC-14615 | RWB-PLT-E2038-APP | CG-ALL-1763 | header | Renumber the duplicate FR-PLT-014 in the next PRD version. |
| CDC-14616 | RWB-PLT-E2038-APP | CG-ALL-1764 | header | Renumber the duplicate FR-PLT-015 in the next PRD version. |
| CDC-14617 | RWB-PLT-E2038-APP | DOR-RWB-PLT-E2038-APP-2 | 18 | Give FR-PLT-014 and FR-PLT-015 one meaning each so the story PRD reference links to a single requirement. |
| CDC-14623 | RWB-PLT-E2038-CON | CG-ALL-1769 | find it | Renumber the duplicate FR-PLT-014 meaning in the next PRD version |
| CDC-14624 | RWB-PLT-E2038-CON | CG-ALL-1770 | find it | Renumber the duplicate FR-PLT-015 meaning in the next PRD version |
| CDC-14628 | RWB-PLT-E2038-CON | DOR-RWB-PLT-E2038-CON-2 | 18 | Renumber the duplicate FR-PLT-014 and FR-PLT-015 meanings in the next PRD version |
| CDC-14648 | RWB-PLT-E2039-APP | CG-ALL-1781 | find it | Renumber the duplicate FR-PLT-001 entry in the PRD's next version. |
| CDC-14649 | RWB-PLT-E2039-APP | CG-ALL-1782 | find it | Renumber the duplicate FR-PLT-009 entry in the PRD's next version. |
| CDC-14650 | RWB-PLT-E2039-APP | CG-ALL-1783 | Header | Renumber the duplicate FR-PLT-010 entry in the PRD's next version. |
| CDC-14651 | RWB-PLT-E2039-APP | CG-ALL-1784 | Header | Renumber the duplicate FR-PLT-011 entry in the PRD's next version. |
| CDC-14652 | RWB-PLT-E2039-APP | CG-ALL-1785 | Header | Renumber the duplicate FR-PLT-012 entry in the PRD's next version. |
| CDC-14653 | RWB-PLT-E2039-APP | CG-ALL-1786 | Header | Renumber the duplicate FR-PLT-013 entry in the PRD's next version. |
| CDC-14654 | RWB-PLT-E2039-APP | CG-ALL-1787 | Header | Renumber the duplicate FR-PLT-021 entry in the PRD's next version. |
| CDC-14655 | RWB-PLT-E2039-APP | CG-ALL-1788 | Header | Renumber the duplicate FR-PLT-022 entry in the PRD's next version. |
| CDC-14656 | RWB-PLT-E2039-APP | CG-ALL-1789 | Header | Renumber the duplicate FR-PLT-023 entry in the PRD's next version. |
| CDC-14657 | RWB-PLT-E2039-APP | CG-ALL-1790 | Header | Renumber the duplicate FR-PLT-024 entry in the PRD's next version. |
| CDC-14658 | RWB-PLT-E2039-APP | CG-ALL-1791 | Header | Renumber the duplicate FR-PLT-025 entry in the PRD's next version. |
| CDC-14659 | RWB-PLT-E2039-APP | CG-ALL-1792 | Header | Renumber the duplicate FR-PLT-026 entry in the PRD's next version. |
| CDC-14660 | RWB-PLT-E2039-APP | CG-ALL-1793 | header | Renumber the duplicate FR-PLT-028 in the next PRD version. |
| CDC-14661 | RWB-PLT-E2039-APP | CG-ALL-1794 | header | Renumber the duplicate FR-PLT-029 in the next PRD version. |
| CDC-14663 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-2 | 18 | Renumber the duplicate IDs FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011 and the 10 further duplicates the detcheck lists, in the next PRD version. |
| CDC-14672 | RWB-PLT-E2039-CON | CG-ALL-1799 | find it | Renumber the duplicate FR-PLT-001 row in the PRD's next version. |
| CDC-14673 | RWB-PLT-E2039-CON | CG-ALL-1800 | find it | Renumber the duplicate FR-PLT-009 row in the PRD's next version. |
| CDC-14674 | RWB-PLT-E2039-CON | CG-ALL-1801 | header | Renumber one of the two FR-PLT-010 rows (transactional outbox meaning) in the PRD's next version. |
| CDC-14675 | RWB-PLT-E2039-CON | CG-ALL-1802 | header | Renumber one of the two FR-PLT-011 rows (inbox dedupe, retry ladder and dead-letter meaning) in the PRD's next version. |
| CDC-14676 | RWB-PLT-E2039-CON | CG-ALL-1803 | header | Renumber one of the two FR-PLT-012 rows (idempotency key meaning) in the PRD's next version. |
| CDC-14677 | RWB-PLT-E2039-CON | CG-ALL-1804 | header | Renumber one of the two FR-PLT-013 rows (RFC 9457 problem envelope meaning) in the PRD's next version. |
| CDC-14678 | RWB-PLT-E2039-CON | CG-ALL-1805 | header | Renumber one of the two FR-PLT-021 rows (cluster, namespace, retention and search attributes meaning) in the PRD's next version. |
| CDC-14679 | RWB-PLT-E2039-CON | CG-ALL-1806 | header | Renumber one of the two FR-PLT-022 rows (versioned workflow kit meaning) in the PRD's next version. |
| CDC-14680 | RWB-PLT-E2039-CON | CG-ALL-1807 | header | Renumber one of the two FR-PLT-023 rows (Schedules and durable timers replace Quartz meaning) in the PRD's next version. |
| CDC-14681 | RWB-PLT-E2039-CON | CG-ALL-1808 | header | Renumber one of the two FR-PLT-024 rows (retry policy, backup, failover, archive and replay gate meaning) in the PRD's next version. |
| CDC-14682 | RWB-PLT-E2039-CON | CG-ALL-1809 | header | Renumber one of the two FR-PLT-025 rows (stuck-workflow scan, smoke workflow and codec meaning) in the PRD's next version. |
| CDC-14683 | RWB-PLT-E2039-CON | CG-ALL-1810 | header | Renumber one of the two FR-PLT-026 rows (mutual TLS, admin audit and break-glass decode meaning) in the PRD's next version. |
| CDC-14684 | RWB-PLT-E2039-CON | CG-ALL-1811 | header | Renumber the duplicate FR-PLT-028 in the PRD's next version |
| CDC-14685 | RWB-PLT-E2039-CON | CG-ALL-1812 | header | Renumber the duplicate FR-PLT-029 in the PRD's next version |
| CDC-14688 | RWB-PLT-E2039-CON | DOR-RWB-PLT-E2039-CON-2 | 18 | Renumber the duplicate FR-PLT IDs (001, 009, 010, 011 and the other ten listed by detcheck) in the PRD's next version |
| CDC-14701 | RWB-PLT-E2040-APP | CG-ALL-1816 | none | Renumber the duplicate FR-PLT-014 row in the next PRD version |
| CDC-14702 | RWB-PLT-E2040-APP | CG-ALL-1817 | header | Renumber the duplicate FR-PLT-015 (Daily hash-chain check) in the next version; then update the PRD reference in the header table. |
| CDC-14704 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-2 | header | Renumber the duplicate FR-PLT-014 and FR-PLT-015 so each ID has one meaning in the next version; then update the PRD reference in the header. |
| CDC-14711 | RWB-PLT-E2040-CON | CG-ALL-1821 | header | Renumber the duplicate FR-PLT-014 in the PRD's next version. |
| CDC-14712 | RWB-PLT-E2040-CON | CG-ALL-1822 | header | Renumber the duplicate FR-PLT-015 in the PRD's next version. |
| CDC-14715 | RWB-PLT-E2040-CON | DOR-RWB-PLT-E2040-CON-2 | 18 | Renumber the duplicate FR-PLT-014 and FR-PLT-015 in the PRD's next version. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (23)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14308 | RWB-PLT-E1070-APP | GAP-2017 | none | Record rwb-platform as the platform team's queue, outside the 19 service queues, with its owner of record (RWB-PLT-WF). |
| CDC-14338 | RWB-PLT-E1070-CON | GAP-2017 | 12.5 | Write rwb-platform as the platform team queue (RWB-PLT-WF), outside the 19 service queues, with its schema and owner of record. |
| CDC-14343 | RWB-PLT-E1071-APP | DOR-RWB-PLT-E1071-APP-8 | 13 | Add activity PlatformSmokeActivity on rwb-platform to the Temporal Catalog v1. |
| CDC-14347 | RWB-PLT-E1071-APP | CG-ALL-1669 | 12.5 | Add an Activities row for PlatformSmokeActivity: type Activity, task queue rwb-platform, purpose as in section 12.5. |
| CDC-14373 | RWB-PLT-E1071-APP | GAP-2017 | find it | Record rwb-platform as the platform team's task queue outside the 19 service queues, with its owner and its place in the R4 naming rule. |
| CDC-14381 | RWB-PLT-E1071-CON | CG-ALL-1695 | 12.5 | Add an Activities row for PlatformSmokeActivity on task queue rwb-platform. |
| CDC-14406 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-8 | find it | Add activity PlatformSmokeActivity to the catalog |
| CDC-14444 | RWB-PLT-E1071-CON | GAP-2017 |  | Record rwb-platform as the platform queue of RWB-PLT-WF, outside the 19 service queues. R4 stays unchanged for services. |
| CDC-14580 | RWB-PLT-E2037-APP | GAP-3184 | 12.5 | List JOB-21 and the archive job as Temporal Schedules, and remove the Quartz option from the run books. |
| CDC-14610 | RWB-PLT-E2038-APP | CG-ALL-1760 | 12.5 | Catalog Workflows sheet has no admin-audit workflow; its reconciliation row covers a different purpose, so it cannot be used. AC6 now names TemporalAdminAuditListener in place of the legacy job; the catalog row is still missing. |
| CDC-14613 | RWB-PLT-E2038-APP | DOR-RWB-PLT-E2038-APP-8 |  | Add a Workflows row named TemporalAdminAuditListener: type Workflow, service platform, namespace rwb-recovery, activity on task queue rwb-platform, daily reconciliation of the frontend audit log against decision_log_entry (BR9 of RWB-PLT-E2038-APP section 12.5). |
| CDC-14634 | RWB-PLT-E2039-APP | CG-ALL-1773 | 12.5 | Add a Workflows row for ResilienceDrillWorkflow: type Workflow, runs on rwb-platform, namespace rwb-recovery, as named in RWB-PLT-E2039-APP section 12.5. |
| CDC-14635 | RWB-PLT-E2039-APP | CG-ALL-1774 | 12.5 | Add a Workflows row for TemporalHistoryArchiveWorkflow: type Workflow, started by the HistoryArchiveJob Schedule, runs on rwb-platform, as named in RWB-PLT-E2039-APP section 12.5. |
| CDC-14639 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-8 | 12.5 | Add Workflows rows for ResilienceDrillWorkflow and TemporalHistoryArchiveWorkflow, and Activities rows for compareVisibilityWithHistory and checkArchivePayload. The three unnamed detcheck rows: Not specified in the source documents (DOR-RWB-PLT-E2039-APP-8). |
| CDC-14643 | RWB-PLT-E2039-APP | CG-ALL-1775 | 12.5 | Add activity compareVisibilityWithHistory to the Activities sheet or use a catalogued one. |
| CDC-14644 | RWB-PLT-E2039-APP | CG-ALL-1776 | 12.5 | Add activity checkArchivePayload to the Activities sheet or use a catalogued one. |
| CDC-14645 | RWB-PLT-E2039-APP | CG-ALL-1777 | 12.5 | Add activity writeArchiveFile to the Activities sheet or use a catalogued one. |
| CDC-14646 | RWB-PLT-E2039-APP | CG-ALL-1778 | 12.5 | Add activity verifyArchiveChecksum to the Activities sheet or use a catalogued one. |
| CDC-14647 | RWB-PLT-E2039-APP | CG-ALL-1779 | 12.5 | Add activity recordDrillEvidence to the Activities sheet or use a catalogued one. |
| CDC-14664 | RWB-PLT-E2039-APP | GAP-3184 | 11 | List HistoryArchiveJob and the stuck-workflow scanner as Temporal Schedules on rwb-platform and remove the Quartz option from the run books of RWB-E2-037 and RWB-E2-039. |
| CDC-14690 | RWB-PLT-E2039-CON | GAP-3184 | 18 | List the stuck-workflow scanner and the 02:00 archive job as Temporal Schedules on rwb-platform, and remove the Quartz option from the run books |
| CDC-14693 | RWB-PLT-E2040-APP | CG-ALL-1814 | 12.5 | Add a Workflows row for HistoryExportJob, or name the catalogued workflow that the story should use in place of it |
| CDC-14698 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-8 | none | Add a HistoryExportJob row, or name the catalogued workflow the story uses |

### Epic design record (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14277 | RWB-PLT-E1070-APP | DOR-RWB-PLT-E1070-APP-14 | find it | Record the signed epic design sign-off for RWB-PLT-E1070-APP in the epic design record; the story cannot assert sign-off. |
| CDC-14309 | RWB-PLT-E1070-CON | DOR-RWB-PLT-E1070-CON-14 |  | Record the signed epic design sign-off for service epic RWB-PLT-WF. |
| CDC-14341 | RWB-PLT-E1071-APP | DOR-RWB-PLT-E1071-APP-14 | header | Record the signed epic design sign-off for RWB-PLT-WF so the story can cite it. |
| CDC-14377 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-WF so the story can cite it. |
| CDC-14583 | RWB-PLT-E2037-CON | DOR-RWB-PLT-E2037-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-WF in the epic design record. |
| CDC-14621 | RWB-PLT-E2038-CON | DOR-RWB-PLT-E2038-CON-14 | header | Confirm and record the signed epic design sign-off in the epic design record |
| CDC-14636 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-14 | find it | Record the signed epic design sign-off for RWB-PLT-WF; no signed design is recorded in the story or sources. |
| CDC-14666 | RWB-PLT-E2039-CON | DOR-RWB-PLT-E2039-CON-14 | header | Record the signed epic design sign-off for RWB-PLT-WF and EP02 in the epic design record. |
| CDC-14694 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-14 | none | Record the signed epic design sign-off for the RWB-PLT-WF epic |
| CDC-14708 | RWB-PLT-E2040-CON | DOR-RWB-PLT-E2040-CON-14 | n/a | Record the signed epic design sign-off in the epic design record. |
| CDC-15068 | RWB-PLT-N003-INF | DOR-RWB-PLT-N003-INF-14 | header | Record the signed epic design sign-off for RWB-PLT-WF |
| CDC-15111 | RWB-PLT-N010-APP | DOR-RWB-PLT-N010-APP-14 |  | Record the signed epic design sign-off for RWB-PLT-WF so that DoR item 14 can pass. |
| CDC-15116 | RWB-PLT-N010-CON | DOR-RWB-PLT-N010-CON-14 |  | Record the signed epic design sign-off for RWB-PLT-WF so that DOR item 14 can pass |
| CDC-15179 | RWB-PLT-NF08-INF | DOR-RWB-PLT-NF08-INF-14 | find it | Record the signed epic design sign-off for RWB-PLT-WF in the epic design record |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (14)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14306 | RWB-PLT-E1070-APP | CG-ALL-1629 | 18 | Align the REQ-DRI-007 and second differing requirement test lists with section 18 of RWB-PLT-E1070-APP in RTM v8; the RTM traces tests of other stories. |
| CDC-14336 | RWB-PLT-E1070-CON | CG-ALL-1649 | 18 | Align the test lists for REQ-DRI-007 and the other differing requirement with section 18 of RWB-PLT-E1070-CON in the next RTM version. |
| CDC-14369 | RWB-PLT-E1071-APP | DOR-RWB-PLT-E1071-APP-12 | 16 | Align the test lists of the §18 rows with the §16 test cases, TC-E1-071-01 to TC-E1-071-13 |
| CDC-14372 | RWB-PLT-E1071-APP | CG-ALL-1672 | 18 | Align the test case lists for REQ-DRI-005, REQ-DRI-007 and REQ-DRI-010 with section 18 of RWB-PLT-E1071-APP in the next RTM version |
| CDC-14439 | RWB-PLT-E1071-CON | CG-ALL-1699 | 18 | Align the test lists for the three differing requirements with section 18 in the next RTM and story versions. |
| CDC-14577 | RWB-PLT-E2037-APP | DOR-RWB-PLT-E2037-APP-12 | 12, 16, 18 | Align the test list for REQ-DRI-007 with story RWB-PLT-E2037-APP section 18, which now includes TC-E2-037-11 (contract test of section 12). |
| CDC-14582 | RWB-PLT-E2037-APP | CG-ALL-1725 | 18 | Align the REQ-DRI-007 test list with section 18 of RWB-PLT-E2037-APP in the next RTM version. |
| CDC-14609 | RWB-PLT-E2037-CON | CG-ALL-1745 | 18 | Align the REQ-DRI-007 test list in RTM v7 with RWB-PLT-E2037-CON section 18 (TC-PLT-E2037-CON-02, TC-PLT-E2037-CON-04, TC-PLT-E2037-CON-06) in the next RTM version. |
| CDC-14618 | RWB-PLT-E2038-APP | CG-ALL-1761 | 18 | Align the test list of REQ-DRI-001 and of the second differing requirement with RWB-PLT-E2038-APP section 18 in the next RTM version. |
| CDC-14631 | RWB-PLT-E2038-CON | CG-ALL-1768 | 18 | Align the requirement test lists with RWB-PLT-E2038-CON section 18 in the next RTM version; REQ-DRI-001 lists TC-PLT-E2038-CON-03 and -04 in the story. |
| CDC-14665 | RWB-PLT-E2039-APP | CG-ALL-1780 | 18 | Align the REQ-DRI-007 test list with section 18 of RWB-PLT-E2039-APP (TC-E2-039-01 to -04, -06 to -10); remove the TC-E1-007, TC-E1-056 and TC-E1-070 IDs that are not in section 18. |
| CDC-14692 | RWB-PLT-E2039-CON | CG-ALL-1798 | 18 | Align REQ-DRI-007 in the RTM to TC-PLT-E2039-CON-01, -02, -05 and -07, as listed in section 18 of this story, in the next version. |
| CDC-14705 | RWB-PLT-E2040-APP | CG-ALL-1815 | 18 | Align the REQ-DRI-005 test list with section 18 of RWB-PLT-E2040-APP (TC-E2-040-01, -02, -03, -04, -06, -08). |
| CDC-14718 | RWB-PLT-E2040-CON | CG-ALL-1820 | 18 | Align the REQ-DRI-005 test list with RWB-PLT-E2040-CON section 18 (TC-PLT-E2040-CON-03, TC-PLT-E2040-CON-06) in the next RTM version; RTM lists other test IDs for this requirement. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (9)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14331 | RWB-PLT-E1070-CON | DOR-RWB-PLT-E1070-CON-1 | 1 | Add a role for the consumer of the Temporal platform contract (service team or platform team) so that section 1 can cite a role code or role name |
| CDC-14403 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-1 | 1 | Add a role code and role name for the consumer of the workflow worker contract (any service team), as used in RWB-PLT-E1071-CON section 1 |
| CDC-14602 | RWB-PLT-E2037-CON | DOR-RWB-PLT-E2037-CON-1 | 1 | Add a role for the consumer of the Temporal observability contract (platform and operations teams, service teams), with its role code. |
| CDC-14625 | RWB-PLT-E2038-CON | DOR-RWB-PLT-E2038-CON-1 | 1 | Add a role code or name for the consumer of the codec and admin-audit contract, or confirm the story role wording |
| CDC-14686 | RWB-PLT-E2039-CON | DOR-RWB-PLT-E2039-CON-1 | 1 | Add a role code or role name for the consumer of the Temporal resilience contract, or map the audiences in section 1 to existing roles |
| CDC-14703 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-1 | 1 | Confirm a role code and name for 'developer', or name the existing role code that replaces it in section 1. |
| CDC-14713 | RWB-PLT-E2040-CON | DOR-RWB-PLT-E2040-CON-1 | 1 | Add a role code for the consumer of the versioning and replay-gate contract, or the roles it names (pipeline, platform administrators, workflow developers, release manager). |
| CDC-15115 | RWB-PLT-N010-APP | DOR-RWB-PLT-N010-APP-1 | 1 | Add a role code or name for 'platform engineer', or name an existing role in section 1. |
| CDC-15118 | RWB-PLT-N010-CON | DOR-RWB-PLT-N010-CON-1 | 1 | Add a role for the consumer of the workflow kit interface, or name the existing role code that section 1 should use |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14344 | RWB-PLT-E1071-APP | GAP-1442 | 13 | Register the platform login, task queue rwb-platform, the admin base for POST /admin/workflows/smoke and the codec key name in Key Vault. |
| CDC-14378 | RWB-PLT-E1071-CON | GAP-1442 | 4 | Name the platform login, the rwb-platform task-queue row, the admin base for POST /admin/workflows/smoke and the codec key name. |
| CDC-14380 | RWB-PLT-E1071-CON | GAP-1443 | 4 | Give the platform login, the admin base and host for POST /admin/workflows/smoke, the rwb-platform queue row and the codec key reference and build-ID format. |
| CDC-14430 | RWB-PLT-E1071-CON | GAP-2419 |  | Add seven platform contracts and RWB-P3-E1043-CON as build dependencies; authorise answer as platform guard; swap agent fake for RWB-P10-TE013-CON when it lands. |
| CDC-14641 | RWB-PLT-E2039-APP | GAP-1447 | 3, 13 | Publish one platform identity section: platform login and grants, provisioning record of task queue rwb-platform, backup window and restore-right owner, rwb-temporal-archive immutability period, approved server and SDK release. |
| CDC-14669 | RWB-PLT-E2039-CON | GAP-1447 | 3 | Publish the platform identity: login and grants, rwb-platform provisioning, backup window and restore owner, rwb-temporal-archive immutability period, and the Temporal server and SDK release. |
| CDC-15114 | RWB-PLT-N010-APP | GAP-1439 | 1 | Fix the platform login, task queue, admin base and kit version label in the Service Catalog and record them in the Ownership Map. |
| CDC-15117 | RWB-PLT-N010-CON | GAP-1439 | 1 | Fix the platform login, task queue rwb-platform, admin base and kit version label; record them in the Ownership Map |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14335 | RWB-PLT-E1070-CON | CG-ALL-1648 | 16 | Add rows TC-PLT-E1070-CON-01 to TC-PLT-E1070-CON-06 to the next Test Cases version, with Given, When and Then copied from the criterion each covers. |
| CDC-14438 | RWB-PLT-E1071-CON | CG-ALL-1698 | 16 | Add rows for TC-PLT-E1071-CON-01 to -06 with Given, When and Then copied from the criteria they cover. |
| CDC-14608 | RWB-PLT-E2037-CON | CG-ALL-1744 | 16 | Add rows to Story test cases for TC-PLT-E2037-CON-01 to TC-PLT-E2037-CON-06 and TC-PLT-E2037-CON-07 (AC7), with Given, When and Then copied from the criteria in RWB-PLT-E2037-CON section 7. |
| CDC-14630 | RWB-PLT-E2038-CON | CG-ALL-1767 | 16 | Add rows TC-PLT-E2038-CON-01 to TC-PLT-E2038-CON-06 with Given, When and Then copied from AC1 to AC6 of RWB-PLT-E2038-CON section 7. |
| CDC-14662 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-12 | 12, 16, 18 | TC-E2-039-12 added with a placeholder description. |
| CDC-14691 | RWB-PLT-E2039-CON | CG-ALL-1797 | 16 | Add rows for TC-PLT-E2039-CON-01 to TC-PLT-E2039-CON-08 in the next version, with Given, When and Then copied from AC1 to AC8. |
| CDC-14717 | RWB-PLT-E2040-CON | CG-ALL-1819 | 16 | Add rows TC-PLT-E2040-CON-01 to TC-PLT-E2040-CON-08 to Story test cases, with Given, When and Then copied from AC1 to AC8. |

### OTHER:Wave 0 Service Catalog; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14311 | RWB-PLT-E1070-CON | GAP-1442 |  | Fix the platform login, task-queue row for rwb-platform, admin base and codec key name in the Wave 0 Service Catalog, and record them in the Ownership Map. |
| CDC-14346 | RWB-PLT-E1071-APP | GAP-1443 | 4, 12.5 | Fix and record the platform login, the admin base for POST /admin/workflows/smoke, the codec key name and the platform queue name rwb-platform. Login, base and codec key: Not specified in the source documents (GAP-1443). |
| CDC-14556 | RWB-PLT-E2037-APP | GAP-1444 | header | Record the platform login, the task queue rwb-platform provisioning record, the admin base for the catalogue read, and the dashboard name and panel titles, with a platform row in the Ownership Map |
| CDC-14557 | RWB-PLT-E2037-APP | GAP-1445 | header | Record the platform login, the task queue rwb-platform provisioning record, the admin base for the catalogue read, and the published dashboard name as the contract owner identity |
| CDC-14584 | RWB-PLT-E2037-CON | GAP-1444 | header | Fix the platform login, task queue rwb-platform provisioning record, admin base and dashboard names; record them in the Ownership Map. |
| CDC-14585 | RWB-PLT-E2037-CON | GAP-1445 | header | Fix the platform login, task queue rwb-platform, admin base and dashboard names for the observability contract; record them in the Ownership Map. |

### 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14413 | RWB-PLT-E1071-CON | GAP-1206 |  | Update the plan and dependency map to six H rows and three C rows per the DP table; keep the written story metadata until the plan is corrected. |
| CDC-14419 | RWB-PLT-E1071-CON | GAP-2501 | 13 | Keep the metadata rows as the plan gives them; record the DP-added H and C rows as non-blocking platform and published contracts built against their fakes. |
| CDC-14434 | RWB-PLT-E1071-CON | GAP-2296 |  | Add a daily chain-check JOB-nn row for rwb-access and add RWB-PLT-E1071-CON to the H list of RWB-P4-E8015-APP. |
| CDC-14446 | RWB-PLT-E1071-CON | GAP-1335 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON as sequencing rows. Keep metadata rows unchanged. |
| CDC-14447 | RWB-PLT-E1071-CON | GAP-1337 | 13 | Carry RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-P7-E1073-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON as sequencing rows. Keep metadata rows unchanged. |
| CDC-14450 | RWB-PLT-E1071-CON | GAP-1277 | 13 | Carry the six platform H dependencies, the published C dependency and the two service baselines as DP-added rows. Keep Ready to start = Day 1. Correct metadata rows at next version. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14558 | RWB-PLT-E2037-APP | CG-ALL-1719 | 12.5 | Record workflow_stuck as a named metric object in the owning document, or add its dictionary name |
| CDC-14559 | RWB-PLT-E2037-APP | CG-ALL-1720 | 7, 12.5, 12.8, 13 | Register temporal_scanner_failures_total as a dictionary field, or record it as a named metric object in the owning document. |
| CDC-14586 | RWB-PLT-E2037-CON | CG-ALL-1742 | 4; 12.8; 13; 16 | Record workflow_stuck as a Prometheus metric in the platform metric contract; no dictionary field entry is needed. |
| CDC-14587 | RWB-PLT-E2037-CON | CG-ALL-1743 | 4; 12.8; 13; 16 | Record temporal_scanner_failures_total as a Prometheus counter in the platform metric contract; no dictionary field entry is needed. |
| CDC-14605 | RWB-PLT-E2037-CON | DOR-RWB-PLT-E2037-CON-7 | 11 | Confirm workflow_stuck and temporal_scanner_failures_total as metric names outside the field lists, or register them as entities. |
| CDC-15072 | RWB-PLT-N003-INF | DOR-RWB-PLT-N003-INF-7 | 11 | Record `temporal_visibility` (visibility database of RWB-PLT-E1070-APP) as a database entity, or confirm it is outside LDM scope. Story §11 now states no row carries a BR Field ID. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14283 | RWB-PLT-E1070-APP | CG-ALL-1625 | 2, 13 | Record the retired monolith login recovery_svc as a named object, or confirm its dictionary name, in LDM v9 Fields. |
| CDC-14284 | RWB-PLT-E1070-APP | CG-ALL-1626 | 2, 3, 7, 8, 11, 13 | Record temporal_svc as the platform persistence role in LDM v9 Fields and Data Classification v5 Fields, with the temporal and temporal_visibility stores it owns. |
| CDC-14285 | RWB-PLT-E1070-APP | CG-ALL-1627 | 3, 8, 13 | Record temporal_visibility as a Temporal persistence store in LDM v9 Fields and Data Classification v5 Fields. |
| CDC-14671 | RWB-PLT-E2039-CON | CG-ALL-1796 | 16 | Record temporal_visibility as a dictionary field, or record the Temporal visibility store object in the owning document. |
| CDC-14689 | RWB-PLT-E2039-CON | DOR-RWB-PLT-E2039-CON-7 | 11 | Record temporal_visibility as a field or entity name in the LDM v9 field list so the detcheck P2 Name check passes |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx; 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14332 | RWB-PLT-E1070-CON | DOR-RWB-PLT-E1070-CON-12 | 16, 18 | Add TC-PLT-E1070-CON-01 to -09 to Test Cases v8; align the section 18 test lists with RTM v7 |
| CDC-14603 | RWB-PLT-E2037-CON | DOR-RWB-PLT-E2037-CON-12 | 16, 18 | Add TC-PLT-E2037-CON-01 to TC-PLT-E2037-CON-06 to Test Cases v8; align the section 18 test lists of REQ-DRI-007 and ADR-023 with RTM v7. |
| CDC-14627 | RWB-PLT-E2038-CON | DOR-RWB-PLT-E2038-CON-12 | 16 | Add TC-PLT-E2038-CON-01 to -06 to Test Cases v8; align the RTM v7 test lists with section 18 |
| CDC-14687 | RWB-PLT-E2039-CON | DOR-RWB-PLT-E2039-CON-12 | 16, 18 | Add rows TC-PLT-E2039-CON-01 to TC-PLT-E2039-CON-09 to Test Cases v8; align the section 18 test lists with RTM v7 |
| CDC-14714 | RWB-PLT-E2040-CON | DOR-RWB-PLT-E2040-CON-12 | 16, 18 | Add TC-PLT-E2040-CON-01 to TC-PLT-E2040-CON-08 to Test Cases v8; align the section 18 test lists with RTM v7. |

### OTHER:Wave 0 Service Catalog; OTHER:Environment and Deployment Design; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14699 | RWB-PLT-E2040-APP | GAP-1449 | 13 | Fix the platform login, the gate pipeline identity, the replay container retention owner and the pinned workflow SDK release, and record them in the Ownership Map |
| CDC-14700 | RWB-PLT-E2040-APP | GAP-1450 | 13 | Fix the pipeline identity, replay container retention, pinned Temporal Java SDK version and build registry owner, and record them in the Ownership Map |
| CDC-14709 | RWB-PLT-E2040-CON | GAP-1449 | 1 | Record the platform login, the pipeline identity of the gate, the owner of the replay container retention and the pinned workflow SDK release. |
| CDC-14710 | RWB-PLT-E2040-CON | GAP-1450 | 1 | Record the pipeline identity, the replay container retention, the pinned Temporal Java SDK version and the build registry owner. |
| CDC-14716 | RWB-PLT-E2040-CON | DOR-RWB-PLT-E2040-CON-3 | 5, 7 | Five of six exceptions (X1 to X5) are tied to AC1, AC2, AC6, AC4, AC8. X6 has no criterion until GAP-1450 closes, so the item cannot be Resolved yet. |

### OTHER:Service Catalog v1 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14281 | RWB-PLT-E1070-APP | GAP-1672 | 2 | Name the accountable team for the shared Temporal cluster and for the business-event topics, and record both with that owner. |
| CDC-14312 | RWB-PLT-E1070-CON | GAP-1672 |  | Name the accountable team for the shared Temporal cluster and for the business-event topics, and record both in Service Catalog v1. |
| CDC-14345 | RWB-PLT-E1071-APP | GAP-1672 | 4 | Name the accountable team for the shared Temporal cluster and for the Recovery business-event topics. Team: Not specified in the source documents (GAP-1672). |
| CDC-14379 | RWB-PLT-E1071-CON | GAP-1672 | header | Name the accountable team for the shared Temporal cluster and for the Recovery business-event topics, and record both in the Service Catalog v1. |

### OTHER:Non Functional Specification v4 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14282 | RWB-PLT-E1070-APP | GAP-1670 | 2 | Set recovery point and time, per-namespace quotas, rate limits, key rotation period and retention periods under DL11 and DL26, and record them. Values Not specified in the source documents (GAP-1670). |
| CDC-14313 | RWB-PLT-E1070-CON | GAP-1670 |  | Set the recovery point and time, per-namespace quotas and rate limits, key rotation period and retention targets under DL11 and DL26, and record them in the Non Functional Specification v4. Values not specified in the source documents (GAP-1670). |
| CDC-14667 | RWB-PLT-E2039-CON | GAP-1670 | find it | Set the NFR-022 and NFR-023 recovery targets under DL11 and the NFR-030 retention under DL26, and record them in the specification. |
| CDC-15069 | RWB-PLT-N003-INF | GAP-1670 | 1 | Set the recovery point and time, per-namespace quotas, key rotation period and retention targets under DL11 and DL26 before wave-1 release, and record them |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14348 | RWB-PLT-E1071-APP | CG-ALL-1670 | 14 | Add a new message ID for 'No session, or the session has expired'; keep MSG-P4-001 for 'Sign-in with no Workbench role'. Text: Not specified in the source documents (CG-ALL-1670). |
| CDC-14349 | RWB-PLT-E1071-APP | CG-ALL-1671 | 14 | Add a new message ID for 'The same workflow ID has already completed'; keep MSG-GEN-004 for 'Record changed by someone else'. Text: Not specified in the source documents (CG-ALL-1671). |
| CDC-14382 | RWB-PLT-E1071-CON | CG-ALL-1696 | 14 | Add a new message ID for 'No session, or the session has expired' with its text; section 14 then cites that ID instead of MSG-P4-001. |
| CDC-14383 | RWB-PLT-E1071-CON | CG-ALL-1697 | 14 | Add a new message ID for 'The same workflow ID has already completed' with its text; section 14 then cites that ID instead of MSG-GEN-004. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (Solution architect) (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14560 | RWB-PLT-E2037-APP | CG-ALL-1722 | 12.5 | Add activity scanStuckWorkflows on task queue rwb-platform, or name a catalogued activity in its place. |
| CDC-14561 | RWB-PLT-E2037-APP | CG-ALL-1723 | 12.5 | Add activity publishScannerMetrics on task queue rwb-platform, or name a catalogued activity in its place. |
| CDC-14562 | RWB-PLT-E2037-APP | CG-ALL-1724 | 12.5 | Add activity recordScanRun on task queue rwb-platform, or name a catalogued activity in its place. |

### OTHER:Wave 0 Service Catalog; OTHER:key management runbook (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14614 | RWB-PLT-E2038-APP | GAP-1441 | header | Fix the platform login, task queue and admin base in the Service Catalog; fix the codec key rotation period and version retention in the runbook. |
| CDC-14622 | RWB-PLT-E2038-CON | GAP-1441 | find it | Fix platform login, task queue and admin base in the Service Catalog; fix codec key rotation period and version retention in the runbook |
| CDC-14668 | RWB-PLT-E2039-CON | GAP-1441 | find it | Fix the platform login, task queue and admin base in the Service Catalog; fix codec key rotation and version retention in the key management runbook. |

### RWB-PLT-E1070-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14278 | RWB-PLT-E1070-APP | DOR-RWB-PLT-E1070-APP-21 | header | Build status of the contract story must move from Not started to Done before this story is ready |
| CDC-15180 | RWB-PLT-NF08-INF | DOR-RWB-PLT-NF08-INF-22 | find it | Publish a contract fake library version and record it as published |

### OTHER:Wave 0 Service Catalog (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14279 | RWB-PLT-E1070-APP | GAP-1440 | 13 | Fix the platform database login, task queue and admin base; record the SCB IT approved Temporal release in Environment and Deployment Design |
| CDC-14280 | RWB-PLT-E1070-APP | GAP-1442 | 13 | Fix the platform login, task queue rwb-platform, admin base and codec key names; record the build-ID format and the Ownership Map entries |

### OTHER:Temporal and Drools Design (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14305 | RWB-PLT-E1070-APP | GAP-0378 | 13 | Worker registration paragraph replaced with a not-specified placeholder for GAP-0378. |
| CDC-14307 | RWB-PLT-E1070-APP | GAP-2038 | none | Read SY-CASEWF as the identity of P3 rwb-case only; a calling service starts a child workflow only through the CaseWorkflow signal. Read SY-RULES as one role held by each service identity inside its own runtime. |

### RWB-PLT-E1071-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14342 | RWB-PLT-E1071-APP | DOR-RWB-PLT-E1071-APP-21 | header | Complete RWB-PLT-E1071-CON and set its build status to Done so the contract is published. |
| CDC-14427 | RWB-PLT-E1071-CON | GAP-1437 | 13 | Fix schedule ID, catch-up and backfill rule and run-record retention in the schedule catalog; publish ingest completeness of a business date from rwb-decision; record the ACE path in the run book. |

### RWB-P6-E1063-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14440 | RWB-PLT-E1071-CON | GAP-2429 | header | Keep the metadata rows as the Work Package fixes them. Name the added rows in the pattern table and the 12.8 fakes. Step D1 decides the dependency map. |
| CDC-14443 | RWB-PLT-E1071-CON | GAP-1212 |  | Add the eight DP-added rows to the dependency lists, or record the five platform contracts and gateway route as the wave-0 baseline per ASM-B-P6-05-E1063-3. |

### RWB-P7-E2042-APP (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14452 | RWB-PLT-E1071-CON | GAP-1296 | n/a | Carry the eight platform H and three published C DP-added dependencies in the story; keep metadata as written; Ready to start stays Day 1. |
| CDC-14453 | RWB-PLT-E1071-CON | GAP-2398 | n/a | Carry the eleven added rows in its sections 13 and 18; leave metadata as the Work Package fixes it; Ready to start stays Day 1. |

### RWB-PLT-E2038-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14611 | RWB-PLT-E2038-APP | DOR-RWB-PLT-E2038-APP-21 | header | Build status moves from Not started to Done once the contract is published. |
| CDC-14612 | RWB-PLT-E2038-APP | DOR-RWB-PLT-E2038-APP-22 | header | Publish the contract fake library and record its version. |

### OTHER:ownership.json (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14620 | RWB-PLT-E2038-APP | GAP-2042 | 7 | Add a row for the codec server and the per-namespace codec keys: owner Platform (RWB-PLT-WF), key rotation under the key policy of SCB IT security. |
| CDC-14633 | RWB-PLT-E2038-CON | GAP-2042 | none in this story | Add rows: codec server and per-namespace codec keys owned by Platform (RWB-PLT-WF) with SCB IT security; key rotation run by the platform under SCB IT security key policy, one key per namespace with the old key kept for decode. |

### RWB-PLT-E2039-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14637 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-21 | find it | Set build status from Not started to Done with the contract published. |
| CDC-14638 | RWB-PLT-E2039-APP | DOR-RWB-PLT-E2039-APP-22 | find it | Publish the contract fake library and record the published version. |

### RWB-PLT-E2040-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14695 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-21 | none | Build the contract story to Done and publish the contract |
| CDC-14697 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-23 | Header | Contract version row kept as Not specified in the source documents; no version number added |

### OTHER:testing-standards.md (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14706 | RWB-PLT-E2040-APP | GAP-0021 | 16 | Add the v5 test obligations named in the detail: contract tests per API, event and activity; Temporal replay tests and gate E2-040; Testcontainers for Kafka and PostgreSQL; JOB-22; 50 scenarios per rule package; boundary test on every build. |
| CDC-14719 | RWB-PLT-E2040-CON | GAP-0021 | find it | Add the v5 test obligations: contract tests per API, event and activity; Temporal replay tests and replay gate E2-040; Testcontainers for Kafka and PostgreSQL; JOB-22 daily journey smoke; 50 scenarios per rule package; boundary test per build. |

### RWB-PLT-N010-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15112 | RWB-PLT-N010-APP | DOR-RWB-PLT-N010-APP-21 |  | Complete the contract build and set its build status from Not started to Done. |
| CDC-15113 | RWB-PLT-N010-APP | DOR-RWB-PLT-N010-APP-22 |  | Publish the contract fake library and record its version in RWB-PLT-N010-CON. |

### OTHER:Capacity forecast v3 (Read path note) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15186 | RWB-PLT-NF08-INF | GAP-0279 |  | Replace the lake refresh note with JOB-02, JOB-03, JOB-04 and JOB-10, each a Schedule or event-started workflow in its own service; keep the count of three. |
| CDC-15187 | RWB-PLT-NF08-INF | GAP-0283 |  | State that the three jobs are the Workbench-side jobs of v3 and name them; the full job map stays in the Batch and Scheduling and Temporal catalogues. |

### 05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20872 | RWB-PLT-E1070-CON | R-09199 |  | Temporal server 1.28.1 and Java SDK 1.31.0 are already in sections 3 and 3.1. Platform login, queue and admin base belong in the Wave 0 Service Catalog. |
| CDC-20888 | RWB-PLT-NF08-INF | R-09236 |  | Document not read: no Bash tool here to run docview.py, and Read cannot open the .docx. Re-run with shell access. |

### OTHER:04 User stories/Recovery Workbench Service Story Files v1/ (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14276 | RWB-PLT-E1070-APP | CG-ALL-1628 | 13 | Create story file RWB-P7-E1073-CON, or name the existing story that carries the same capability and update the DP-04 dependency |

### OTHER:ADR-011 and Workflow Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14304 | RWB-PLT-E1070-APP | GAP-0002 | find it | Update to the parent CaseWorkflow with a child workflow per stage, Continue-As-New at each stage end and at least every 28 days, and parent close policy ABANDON, before Epic 3 starts. |

### OTHER:Environment and Deployment Design v4; OTHER:Wave 0 Service Catalog (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14310 | RWB-PLT-E1070-CON | GAP-1440 |  | Record the SCB IT approved Temporal server and Java SDK release in Environment and Deployment Design v4; fix the platform login, queue and admin base in the Wave 0 Service Catalog. |

### OTHER:ADR-011 (Architecture Decision Record for the case workflow) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14334 | RWB-PLT-E1070-CON | GAP-0002 | find it | Update ADR-011 to the parent CaseWorkflow plus per-stage child model on the owning service queue, with Continue-As-New at stage end and at least every 28 days, parent close policy ABANDON, before Epic 3 starts. |

### OTHER:The v4 document holding the section 4.1 SY-CASEWF and SY-RULES rows and the section 7.1 Authorizer plugin row (GAP-2038) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14337 | RWB-PLT-E1070-CON | GAP-2038 | find it | Version 5 reads SY-CASEWF as the identity of P3 rwb-case, with calling services starting child workflows only through the CaseWorkflow signal; SY-RULES is one role held by each service identity inside its own runtime. |

### OTHER:Build Notes v6 (configuration notes RWB-E1-070 to RWB-E1-072) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14339 | RWB-PLT-E1070-CON | GAP-3163 | find it | Keep the build order and read Module P3 as consumed by P3 rather than owned by P3 for the Temporal platform and the Drools runtime. |

### OTHER:Recovery Workbench Service Story Files v1 (story folder) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14340 | RWB-PLT-E1071-APP | CG-ALL-1667 | 13 | Create story RWB-P7-E1073-CON or name the existing story for the same capability; then align the DP-04 dependency in section 13. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14371 | RWB-PLT-E1071-APP | GAP-2023 | find it | Publish the workflow kit as a versioned library with coordinates, first version and a per-minor compatibility table; fail the build when a worker carries an unreleased kit minor. |

### OTHER:Recovery Workbench Build Notes v6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14374 | RWB-PLT-E1071-APP | GAP-3163 | find it | In the RWB-E1-070 to RWB-E1-072 configuration notes, read Module P3 as consumed by P3, not owned by P3; keep the build order. |

### OTHER:Technical specification P4 and technical specification P3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14375 | RWB-PLT-E1071-APP | GAP-1566 | find it | Remove API-P4-021, the WorkflowAdminService and API-P3-027 for the smoke path; keep the operation once in this platform story and link the E8 surface to it. |

### OTHER:Story dependencies v5; OTHER:Dependency classes sheet (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14376 | RWB-PLT-E1071-APP | GAP-3234 | find it | Record that platform technical-enabler work is team-type work: keep X on the ten rows, tracked and never blocking. |

### 09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx; 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14404 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-12 | 16, 18 | Add TC-PLT-E1071-CON-01 to -06 (as in section 16) to Test Cases v8; align the RTM v7 test lists to section 18. |

### OTHER:Message catalogue (standard) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14407 | RWB-PLT-E1071-CON | DOR-RWB-PLT-E1071-CON-9 | 14 | Confirm the standard's meaning of MSG-P4-001 and MSG-GEN-004 or align the story to it |

### RWB-S5-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14408 | RWB-PLT-E1071-CON | GAP-1946 | find it | Keep H and C at None; record the nine platform and rwb-case CONs as wave-0 prerequisites and fakes; serve the ACE check from the quality-results and quality-runs reads |

### RWB-P6-E1011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14409 | RWB-PLT-E1071-CON | GAP-1167 | find it | Keep H at None; record the seven platform CONs as wave-0 build prerequisites and add them to the dependency map as platform prerequisites |

### OTHER:Recovery Workbench TSD S9 and PRD (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14410 | RWB-PLT-E1071-CON | GAP-3103 |  | Publish partner_user fields in the TSD S9 T3.1 catalogue and PRD; name the contract-end Schedule and its clock; decide whether a recall is announced by an event; confirm the feature the requirement rows serve. |

### OTHER:Work Package metadata rows for the affected story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14411 | RWB-PLT-E1071-CON | GAP-2448 |  | Keep metadata as the work package fixes it; record the DP-table platform H, P3 C and P4 authorise dependencies in that story's section 13, built against fakes on Day 1. |

### RWB-P6-E1032-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14412 | RWB-PLT-E1071-CON | GAP-1198 |  | Add seven platform H contracts and two P3 C contracts to the dependency rows of RWB-P6-E1032-APP, or record in the platform release train that wave 1 services compile against them. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14414 | RWB-PLT-E1071-CON | GAP-0672 |  | Record eight DP H rows as wave-0 prerequisites; publish the model fetch in RWB-P7-E1073-CON; fix the local copy table and migration; name the rwb_integration login before baseline. |

### RWB-P7-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14415 | RWB-PLT-E1071-CON | GAP-1328 |  | Complete the metadata from the DP table (eight H rows, the DP-06 and DP-07 C rows, DP-09 in the pattern list), or state in R5.5 that platform H and self-referential C rows are held by other stories. |

### OTHER:Work Package row B2-P3-020 and the Day-1 allocation (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14416 | RWB-PLT-E1071-CON | GAP-2261 |  | Add the platform CON dependencies (DP-03, DP-06, DP-07, DP-09, DP-10, DP-19) to the lane and Day-1 allocation; keep the metadata row as delivered. |

### RWB-P7-E2002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14417 | RWB-PLT-E1071-CON | GAP-2470 |  | Complete the metadata rows from the DP table, or keep the plan rows and read the DP rows as pattern-added dependencies as section 13 of that story does. |

### RWB-P7-E2004-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14418 | RWB-PLT-E1071-CON | GAP-2475 | 13 | State in R5.5 that platform H rows and self-referential C rows are held by the platform and contract stories and not repeated on a secondary APP line, or complete the metadata rows from the table. |

### RWB-P6-E2013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14420 | RWB-PLT-E1071-CON | GAP-1223 |  | Read H as None plus the named platform contracts; read C as RWB-P7-E2013-CON plus RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON; story stays Day 1. |

### OTHER:Work Package B2-P5-006 story line and the contract rows of stories claiming DP-07 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14421 | RWB-PLT-E1071-CON | GAP-2354 |  | Record the platform CONs as wave-0 release train prerequisites of wave-1 services; add RWB-P3-E1043-CON to contract rows of stories whose pattern set claims DP-07. |

### RWB-S4-E2025-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14422 | RWB-PLT-E1071-CON | GAP-1898 |  | Keep plan lists; story stays Day 1 with RWB-P5-E2025-CON as sole contract; add five H rows and two C rows when published, then re-run the dependency check. |

### RWB-P8-E2027-APP; 11 Delivery and operations/Recovery Workbench Dependency Map v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14423 | RWB-PLT-E1071-CON | GAP-1291 |  | Keep metadata rows; record DP-added H and C as non-blocking platform and published contracts built against fakes; keep DP-04 and DP-14 contracts visible in section 13. |

### RWB-P7-E2028-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14424 | RWB-PLT-E1071-CON | GAP-1295 |  | Read H as None plus six platform contracts named by the DP table; read C as RWB-P10-E2028-CON plus C RWB-P3-E1043-CON and the published P3 case read and P4 authorise call. |

### OTHER:split_plan.json and the RWB-S5-E3026 APP and ITG stories (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14425 | RWB-PLT-E1071-CON | GAP-2869 |  | Name RWB-PLT-E1071-CON as the wave-0 library the Schedule needs; declare valuation order as consumed from rwb-valuation; trace both slices to REQ-S5-003. |

### RWB-S8-E7003-APP; RWB-S8-E7003-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14426 | RWB-PLT-E1071-CON | GAP-3055 |  | Keep H, C, I and X rows; record rwb-source-data, rwb-case, rwb-access and rwb-decision rows as class C; track RWB-PLT-TE006-CON and RWB-PLT-E1071-CON as dependencies. |

### OTHER:RWB-P10 agent runtime app story set and TSD P10 v2 T-A.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14428 | RWB-PLT-E1071-CON | GAP-0619 |  | Add run-submit POST /api/recovery/agent/v1/agent-steps and link PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record with legacy members unchanged; 60 s budget as the single recorded exception. |

### OTHER:rwb-agent deployment story (P10 app deployment) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14429 | RWB-PLT-E1071-CON | GAP-0621 |  | Add login secret reference, grants on rwb_agent only, the V10_002 migration job, publish right on rwb.decision-record.v1, dashboard panels, alert rules and route as reviewed environment values. |

### RWB-P3-E1043-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14431 | RWB-PLT-E1071-CON | GAP-2337 |  | Intake Schedule ID row removed from the kit header. |

### OTHER:RWB-E5-020 story and S4 ownership rows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14432 | RWB-PLT-E1071-CON | GAP-2831 |  | Carry the review date as a durable timer of LitigationWorkflow on rwb-litigation, answer the R-LIT-56 return, and declare no Schedule or job row. |

### RWB-S9-E7011-APP; 02 Business architecture and process/Recovery Workbench Business Rules and Routing Logic v4.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14433 | RWB-PLT-E1071-CON | GAP-3121 |  | Add scorecard rule rows to rwb-decision, the two consumed reads, and a reporting path or recorded decision that no scorecard fact is reported. |

### RWB-P4-AD008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14435 | RWB-PLT-E1071-CON | GAP-0807 | header | Add RWB-PLT-E1071-CON to Depends on (build) and DP-10 to the pattern row. Cron stays under DL38 until the bank IAM value is supplied. Create the Schedule in the operations story. |

### RWB-S7-E6013-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14436 | RWB-PLT-E1071-CON | GAP-3016 |  | Add the four consumed-contract rows, DP-04, DP-05, DP-09 and DP-10, and the rule, ACE read, inbox and Schedule rows as the item fixes. |

### RWB-S7-E6023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14437 | RWB-PLT-E1071-CON | GAP-3037 |  | Fix the posting product and event on the rwb-source-data contract, publish the cross-reference, hold three class C rows and trace to REQ-S7-005. |

### OTHER:Build Notes v6 (RWB-TE-007 and RWB-E1-030) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14441 | RWB-PLT-E1071-CON | GAP-3166 | header | Read JOB-06 and every map Job as a Temporal Schedule. Keep RWB-TE-007 retired, for traceability only. |

### RWB-S9-E1032-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14442 | RWB-PLT-E1071-CON | GAP-3140 | header | Keep the H list as the Work Package fixes it. Record the seven platform rows as the wave-0 shared baseline, revisiting before the wave 1 entry check. |

### RWB-P6-E1073-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14445 | RWB-PLT-E1071-CON | GAP-1218 | 13 | State in the lane document that the platform CONs of the DP table are wave-0 prerequisites carried outside H for every wave-1 APP story. Keep Ready to start Day 1. |

### RWB-S8-E2012-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14448 | RWB-PLT-E1071-CON | GAP-3091 | 13 | Carry the eight platform H rows as tracked, not as build dependencies. Keep Depends on (build) = None and Ready to start = Day 1. |

### RWB-P6-E2014-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14449 | RWB-PLT-E1071-CON | GAP-2389 | 13 | At the next plan revision, add RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON to the C list. Keep H empty. |

### OTHER:Build sequence of the Recovery Workbench story set (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14451 | RWB-PLT-E1071-CON | GAP-2410 | n/a | Record that a secondary slice builds against platform contracts and published fakes and reads same-service wave-1 rows through its own schema, keeping lane depth within R5.7 rule 5. |

### OTHER:Build order of the Recovery Workbench story set (version 3 order) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14454 | RWB-PLT-E1071-CON | GAP-3241 | n/a | Keep items 19 and 21 as numbered places with no story against them; repoint any dependency on RWB-TE-007 to RWB-PLT-E1071-CON. |

### RWB-P10-TE013-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14455 | RWB-PLT-E1071-CON | GAP-1319 | n/a | Carry the seven platform H, three published C and the P4 authorise answer as DP-added; keep Ready to start Day 1; correct metadata at next version. |

### OTHER:TSD P4 and TSD P3 technical specifications (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14456 | RWB-PLT-E1071-CON | GAP-1566 | n/a | Authorise row no longer names the smoke path; it refers to the admin operation (GAP-1566). |

### OTHER:RWB-TE-007 story (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14457 | RWB-PLT-E1071-CON | GAP-3189 | n/a | Keep the section with a retirement banner and a step-by-step target table; the work moves to RWB-PLT-E1071-CON. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14553 | RWB-PLT-E2037-APP | CG-ALL-1721 | 12.5 | Add a Workflows row for StuckWorkflowScanner on task queue rwb-platform, or name the catalogued workflow that replaces it |

### RWB-PLT-E2037-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14554 | RWB-PLT-E2037-APP | DOR-RWB-PLT-E2037-APP-21 | header | Set build status to Done once the contract is published |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Workflows and Activities (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14555 | RWB-PLT-E2037-APP | DOR-RWB-PLT-E2037-APP-8 | 12.5 | Add rows for StuckWorkflowScanner and activities scanStuckWorkflows, publishScannerMetrics and recordScanRun on task queue rwb-platform |

### RWB-PLT-E1056-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14578 | RWB-PLT-E2037-APP | DOR-RWB-PLT-E2037-APP-17 | Header | Complete the build dependency RWB-PLT-E1056-OPS (run book catalog and RunbookCompletenessTest) before this story starts build. |

### RWB-PLT-N005-OPS (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14581 | RWB-PLT-E2037-APP | GAP-2043 | all | Version 4: each measure and alert per service (19 units, per-service reading of the 13 alerts, one Service health dashboard per service). Dashboard name, panel order, refresh interval and saved query stay at the RWB-PLT-N005-OPS baseline. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:run books for RWB-E2-037 and RWB-E2-039 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14606 | RWB-PLT-E2037-CON | GAP-3184 | 18 | List both jobs as Temporal Schedules in the catalog and remove the Quartz option from the run books. |

### OTHER:Observability measures, alerts and dashboards Version 3 (to become Version 4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14607 | RWB-PLT-E2037-CON | GAP-2043 |  | Issue Version 4 with the service as the unit: 19 measured units, the 13 alerts read per service, one Service health dashboard per service; leave name, panels, refresh and saved query to RWB-PLT-N005-OPS baseline. |

### OTHER:Recovery Workbench Temporal authorizer role mapping (v4 sections 4.1; OTHER:7; OTHER:7.1; OTHER:Version 5) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14619 | RWB-PLT-E2038-APP | GAP-2038 | 16 | Read SY-CASEWF as the identity of P3 rwb-case only; a calling service starts a child workflow only through the CaseWorkflow signal; read SY-RULES as one role held by each service identity inside its own runtime. |

### OTHER:Screen specification for SCR-38 (not in this story) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14626 | RWB-PLT-E2038-CON | DOR-RWB-PLT-E2038-CON-10 | find it | Add empty, loading, error and no-access states for SCR-38 |

### OTHER:Gap register; OTHER:GAP-0417 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14629 | RWB-PLT-E2038-CON | GAP-0417 | none in this story | Record the harness repository and SIT environment, seeded workflows, grant and key versions, per-run evidence format and retention, and test certificate set, agreed by the integration lead with platform workflow owner and QA at the wave 2 entry check. |

### OTHER:Temporal security design, version 4 (next version 5), sections 4.1 and 7.1 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14632 | RWB-PLT-E2038-CON | GAP-2038 | none in this story | Read SY-CASEWF as the identity of P3 rwb-case, with a calling service starting a child workflow only through the CaseWorkflow signal; read SY-RULES as one role held by each service identity inside its own runtime. |

### OTHER:Wave 0 Service Catalog (and key management runbook) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14640 | RWB-PLT-E2039-APP | GAP-1441 | find it | Fix the platform login, task queue and admin base for the codec server, audit receiver and reconciliation; fix codec key rotation period and version retention. |

### OTHER:Wave 0 Service Catalog and the parameters contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14642 | RWB-PLT-E2039-APP | GAP-1448 | find it | Publish the archive immutability period, the retry count owner, the manifest retention and the approved release the version step check compares against. |

### RWB-PLT-E1042-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14670 | RWB-PLT-E2039-CON | GAP-1448 | 3 | Publish the archive immutability period, the retry count owner, the manifest retention and the approved release the version check compares against. |

### OTHER:Contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14696 | RWB-PLT-E2040-APP | DOR-RWB-PLT-E2040-APP-22 | none | Publish a contract fake library version for RWB-PLT-E2040-CON and record its version |

### OTHER:Workflow Engine Design v3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14707 | RWB-PLT-E2040-APP | GAP-2020 | none | Add Continue-As-New to section 6: the closing run writes an in-flight signal to the new run before it returns; Continue-As-New only at a stage end; define the due durable timer at the cut. |

### OTHER:Workflow Engine Design v3, section 6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-14720 | RWB-PLT-E2040-CON | GAP-2020 | find it | Add Continue-As-New: the closing run's signal handler writes the event to the new run before it returns; Continue-As-New only at a stage end. A durable timer due at the cut is not covered by the proposed rule. |

### OTHER:Wave 0 Service Catalog; OTHER:platform run book; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; OTHER:Environment and Deployment Design (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15070 | RWB-PLT-N003-INF | GAP-1451 | 1 | Add the platform service row and fix its login and admin base, per-namespace quotas and rate limits, namespace certificate set, key rotation period and version policy, and exact retention; record them |

### RWB-PLT-E1070-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15071 | RWB-PLT-N003-INF | CG-ALL-1823 | 3 | Record `temporal_visibility` as the visibility persistence database of the cluster, outside the LDM and Data Classification dictionaries |

### OTHER:Access contract (text of MSG-P4-002) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15073 | RWB-PLT-N003-INF | DOR-RWB-PLT-N003-INF-9 | 14 | Row MSG-P4-002 added to section 14 with its text left as a named gap |

### OTHER:Environment and Deployment Design; OTHER:Service Catalog; OTHER:baseline record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15181 | RWB-PLT-NF08-INF | GAP-1452 | find it | Fix the supported version range, compatibility matrix, upgrade cadence and window, measurement window and conformance cadence at the platform infrastructure review before wave 0 exit |

### OTHER:Technical Specifications by Module v6 (T0 Service section or a PLT module file) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15182 | RWB-PLT-NF08-INF | GAP-1664 |  | Write the platform functional specification and map FR-PLT-001 to FR-PLT-034 to their requirement IDs. |

### OTHER:Capacity forecast v3 (new sheet Topics and queues) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15183 | RWB-PLT-NF08-INF | GAP-0280 |  | Add a sheet listing the 19 service topics and rwb.decision-record.v1, the 19 task queues, and the platform settings, with the ReportPublished consumer as a placeholder. |

### OTHER:Test plan section 6.3 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15184 | RWB-PLT-NF08-INF | GAP-2130 |  | State the shared pass marks for every event and workflow test from Architecture v5 slide 11 and the Temporal and Drools design, and apply them in the 19 service rows. |

### OTHER:Template and Rules section R5.6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-15185 | RWB-PLT-NF08-INF | GAP-3199 |  | State the epic-wave rule: epic wave is the earliest wave among its stories, with the service wave shown beside it; use NF only for NF-01 to NF-08. |

### 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20688 | RWB-PLT-E1071-CON | R-28558 |  | RWB-E1-030 runs JOB-06 as a Temporal Schedule and RWB-TE-007 is retired for traceability (GAP-3166). |

### 05 Technical architecture/Recovery Workbench Workflow Engine Design v4.docx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-20905 | RWB-PLT-E2040-CON | R-29057 |  | write failed: WRITE FAILED (nothing was written): X002-F2: old text found 0 time(s) in paragraphs, expected 1 |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0002 | ADR-011 still describes one long case workflow | Recovery tech lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0007 | Temporal version 1.30+, 1.28.1 and 1.29.7 | Platform team | Resolved (directive) |
| GAP-0021 | Testing standards lack the v5 test obligations | QA lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0073 | Who holds the AgentRunWorkflow handle and the parent-child link is not stated | P10 rwb-agent | Resolved (directive) |
| GAP-0154 | Nine live features name the Quartz scheduler as their system while D-RCV-60 replaces it with Temporal Schedules | Temporal platform lead and the solution architects of P3 rwb-case, S1 rwb-valuation, S4 rwb-litigation and S8 rwb-deviation | Resolved (directive) |
| GAP-0279 | The three scheduled Workbench jobs include a lake refresh that the target removes | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0280 | The forecast carries no Kafka topic, partition, retention or consumer figures | DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0283 | Three scheduled Workbench jobs in the forecast against 21 jobs in the Arch v5 job map | Solution architecture team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0378 | The worker registration, task-queue and namespace contract between the 19 services and the Temporal platform is not defined | Solution architect | Resolved (directive) |
| GAP-0417 | Workflow security harness environment, seeding, evidence format, retention and test certificate details are not specified | Integration lead | Resolved (directive) |
| GAP-0561 | The 05:30 late check and the worker and queue registration have no story in the build dependencies of this slice | DevOps team and platform workflow owner | Resolved (directive) |
| GAP-0619 | The app slice of the agent runtime client: the two operations the legacy Java interface spans, the call type and the budget of a step, the login, the record write and its link, the guardrail check-code list and the route in front of the run read are not fixed by any source | Solution architect with the P10 service owner and the owners of rwb-decision, rwb-case and rwb-access | Resolved (directive) |
| GAP-0621 | The deployment slice of the agent runtime client: the chart values, the login secret, the topic rights of the shared decision-record topic, the worker concurrency, the alert thresholds, the route path and the capacity figures are not specified by any source | SCB IT infrastructure and the DevOps team with the ACE platform team and security | Resolved (directive) |
| GAP-0672 | rwb-integration rule copy: the H and C rows, the model-fetch surface, the assigned package, the local copy table, the event consumers and the login are not settled by any one source | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-0807 | rwb-access access review list: JOB-18 is a Temporal Schedule but the story metadata carries no workflow-kit dependency and no cron | Solution architect and the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1161 | The dependencies DP-03, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists, and no fake is named for the reference data or the decision record | Solution architect | Resolved (directive) |
| GAP-1167 | RWB-P6-E1011-APP: the seven platform CONs added by DP-03, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 are missing from the story's H list | Solution architect | Resolved (directive) |
| GAP-1198 | The DP-added platform and P3 contracts are missing from the story dependency rows | Release manager | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1206 | The build and contract dependency lists of the plan do not carry the dependencies the DP table adds to this key | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1212 | The platform and reference contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are missing from the plan dependency lists of this story | platform owner, P3 case owner and delivery lead | Resolved (directive) |
| GAP-1218 | RWB-P6-E1073-APP: the platform H dependencies that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the story's H list | Tech lead | Resolved (directive) |
| GAP-1223 | The plan's H and C lists for this story name None and RWB-P7-E2013-CON, and omit the platform and published contracts that the DP table adds | Delivery lead | Resolved (directive) |
| GAP-1277 | The DP table adds platform and published dependencies, and two service baselines, that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1286 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case team | Resolved (directive) |
| GAP-1291 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-1295 | The metadata rows name no build dependency and the agent contract only, while the DP table of the story adds six platform contracts and one rwb-case contract and the story consumes two further operations | Delivery lead | Resolved (directive) |
| GAP-1296 | The DP-added H and C dependencies of RWB-P7-E2042-APP are absent from the metadata rows | Solution architect | Resolved (directive) |
| GAP-1308 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect with the platform team, the rwb-case team and the rwb-access team | Resolved (directive) |
| GAP-1319 | The DP table adds platform and published dependencies that the metadata rows of the story do not carry | Solution architect, P7 rwb-decision, with the platform team and the rwb-case and rwb-access teams | Resolved (directive) |
| GAP-1328 | RWB-P7-E1073-APP: the DP table adds eight platform H rows, one C row and one PLT object set that the metadata rows of the plan do not carry, and DP-04 points its C row at this service's own contract story | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-1335 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1337 | Platform and published dependencies added by the patterns but not carried in the metadata rows | Delivery lead | Resolved (directive) |
| GAP-1340 | DP-added platform and published dependencies are not carried in the metadata rows | Solution architect | Resolved (directive) |
| GAP-1437 | Owner, instance, run-record surface and reporting of the daily decision log hash-chain check after the split | Solution architect with RW-COMPLY | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1439 | Platform service identity, task queue and admin base are not specified for the workflow platform | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1440 | The platform identity and the SCB IT approved Temporal server and SDK release are not stated in any read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1441 | Platform identity and Temporal security values are not fixed in the read sources | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1442 | The platform worker has no platform login, no task-queue row and no admin base in any read source, and no source gives the build-ID format or the codec key name | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1443 | The worker contract has no source for the admin base it publishes, for the platform queue row, for the codec key reference or for the build-ID format | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1444 | The platform identity, the task queue provisioning record and the dashboard names are not specified | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1445 | The platform identity behind the observability contract is not specified | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1446 | The stuck workflow scan cadence conflicts: 15 minutes in the legacy story, 5 minutes in Architecture v5 and the Ownership Map | Platform team | Resolved (directive) |
| GAP-1447 | The shared Temporal platform has no row in the services table, so the platform login, the task queue, the owner of the backup and restore right, the archive container immutability period and the approved server and SDK release are named by no read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1448 | The platform has no service row, and the archive immutability period, the retry count owner, the manifest retention and the approved release the version check compares against are named by no read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1449 | The platform login, the gate's pipeline identity, the owner of the replay container's retention and the pinned SDK release the gate runs at are named by no read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1450 | The platform has no service row, and the pipeline identity, the replay container retention, the pinned SDK version and the build registry owner are named by no read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1451 | The platform has no service row, and the platform login, the quotas, the rate limits, the namespace certificate set, the key rotation period and the exact retention of the namespace are named by no read source | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1452 | The baseline parameters of a moved non-functional story are named by no read source beyond 1.30 or later and the ACE objectives | Platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1566 | POST /admin/workflows/smoke is claimed by the P3 and P4 technical specifications while the Ownership Map and Architecture v5 give the smoke workflow to the platform | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1664 | No FSD module exists for the platform, so no FSD requirement ID states a platform capability | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1670 | Several platform targets are unset: recovery point and time, the per-namespace quotas, the key rotation period and the retention periods | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1672 | The owner of record for the shared Temporal cluster and for the Kafka hosting is not named | Enterprise Architecture | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1898 | The five H rows and two C rows that DP-06, DP-07, DP-09, DP-10 and DP-19 add are absent from this story's build and contract lists | Solution architect, with the platform library owners and the rwb-case owners | Resolved (directive) |
| GAP-1899 | DP-09 and DP-10 are in the pattern list but this slice produces no event, consumes no event and registers no Schedule, and DocumentFieldsExtracted is consumed by rwb-case only | Solution architect | Resolved (directive) |
| GAP-1946 | RWB-S5-E1011-APP: the asset slice of RWB-E1-011 has no source for its dependency lists, its ACE-side read, its quality objects, its rights and its run cadence, and the data-lake and Power BI target of the legacy key is removed | Solution architect | Resolved (directive) |
| GAP-2017 | rwb-platform task queue is not in the 19 services or in the R4 naming rule | Platform team (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2020 | Continue-As-New and a signal that arrives during it | Platform team (RWB-PLT-WF) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2022 | Schedule ID, overlap policy, catch-up window and pause behaviour | Platform team (RWB-PLT-WF) with the owning service | Resolved (directive) |
| GAP-2023 | Workflow kit version, coordinates and compatibility rule | Platform team (RWB-PLT-WF) | Resolved (directive) |
| GAP-2038 | The mapping of a service workload identity to the SY- roles is not specified | Platform with P3 rwb-case | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2042 | The codec server and the per-namespace codec keys have no owner and no rotation rule | Platform (RWB-PLT-WF) with SCB IT security | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2043 | Version 3 measures, alerts and dashboards the Workbench as one; the target architecture is 19 services | Solution architect with the platform team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2130 | No pass mark for the outbox, the inbox, the retry topics or the workflow history | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2261 | Depends on (build) is empty while the DP table adds platform H dependencies | TechX | Resolved (directive) |
| GAP-2296 | The daily chain check has no job row in the Batch and Scheduling Design and the workflow kit dependency is absent from the Work Package | Solution architect with the platform workflow owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2337 | The rwb-case side of the checklist story is not fixed: the case read operation, the reference-load operation, the batch missing-count operation and the DocumentChecklist field names | Solution architect, with the P5 TechX squad and the P3 rwb-case squad | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2354 | The platform contracts and the P3 reference-data contract that the nine applied patterns add are absent from this story's build and contract rows, which the Work Package fixes as empty | Release manager | Resolved (directive) |
| GAP-2389 | The plan records no build row for the platform contracts that the patterns of this slice add | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2398 | The DP table adds eight H rows and three C rows that the Work Package dependency rows do not carry | Tech lead | Resolved (directive) |
| GAP-2410 | A secondary registry slice carries no build dependency while the DP rows add seven platform contracts and four published contracts | Delivery lead | Resolved (directive) |
| GAP-2419 | The platform build dependencies, the authorise answer and the agent contract that the patterns add are not in the metadata rows, and RWB-P10-TE013-CON is not written | Solution architect | Resolved (directive) |
| GAP-2429 | The eight patterns add five platform build dependencies, one reference-data contract and one authorise contract that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2448 | The metadata dependency rows name only the P5 contract, while the DP table adds platform and rwb-case and rwb-access contracts | Solution architect, P7 | Resolved (directive) |
| GAP-2470 | RWB-P7-E2002-APP: the DP table adds six platform H rows, two C rows and one PLT object set that the metadata rows of the plan do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2475 | RWB-P7-E2004-APP: the DP table adds eight platform H rows, three C rows and a workflow-kit dependency that the metadata rows of a secondary slice do not carry | Solution architect with the platform library owner and the rwb-decision service owner | Resolved (directive) |
| GAP-2488 | The eleven patterns add seven platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2496 | The twelve patterns add eight platform build dependencies and four consumed contracts that the metadata rows of a secondary slice do not carry | Solution architect, with the delivery lead | Resolved (directive) |
| GAP-2501 | The DP table adds platform and published contracts that the metadata rows do not carry | Delivery lead, with the platform contract owners | Resolved (directive) |
| GAP-2831 | The Workbench scheduler of R-LIT-55 has no equivalent in the target, and DP-10 is not in the pattern set of this key | Solution architect with the workflow platform owner and the tech lead of S4 | Resolved (directive) |
| GAP-2869 | RWB-S5-E3026: the cycle slice has no planned dependency row for its four consumed contracts or its Schedule library, and neither the plan nor the module model holds the re-appraisal record, the requirement id or the AC3 evidence | Solution architect | Resolved (directive) |
| GAP-3016 | RWB-S7-E6013-APP: the scan slice has no plan row for its four consumed contracts, its rule kit, its ACE read, its inbox and its schedule, and no table or list of values holds the scan | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3037 | RWB-S7-E6023-APP: the reconciliation step has no published operation, no posting-product operation or event name, no matching cross-reference, no plan C row for its three consumed services, no job or Schedule for its monthly trigger and no requirement row | Solution architect | Resolved (directive) |
| GAP-3055 | RWB-S8-E7003-APP: the X3 branch has no plan row for its four consumed contracts, its rule read, its outbox and its workflow, and no source names the claim reference, the heir notification or the escalation level | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3075 | The plan gives this slice no build dependency while the DP table adds eight platform contract rows and two further contract rows | Platform owner for the TPL, LIB, WF, DB, EVT and EDGE epics with the S8 service owner | Resolved (directive) |
| GAP-3091 | Plan build list is empty for RWB-S8-E2012-APP although the DP table adds eight platform contract rows | Platform architect | Resolved (directive) |
| GAP-3103 | RWB-S9-AD022-APP: the partner user catalogue, the date trigger, the recall event and the legacy predecessor are unstated | Business analyst, S9; solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3121 | RWB-S9-E7011-APP: the monthly scorecard has no rule row of its own, no trigger, no job, no workflow of its own, no published scorecard read and no reporting channel | Solution architect with the rwb-decision rule owner, the rwb-source-data owner and the platform scheduling owner | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3140 | The DP table names platform H rows that the plan's H list does not carry | Tech lead | Resolved (directive) |
| GAP-3163 | The Temporal platform and the Drools runtime sit in a P3 module in the story and in platform epics in the split plan | Platform lead | Resolved (directive) |
| GAP-3166 | The Quartz note remains in the build notes although a Temporal Schedule replaces it | Platform lead | Resolved (directive) |
| GAP-3184 | Quartz triggers appear in RWB-E2-037 and RWB-E2-039 after Quartz is retired | Platform lead with the DevOps team | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3189 | RWB-TE-007 content is outdated under D-RCV-60 | TechX | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3199 | The epic wave is not defined for an epic whose stories span several business-epic waves | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3227 | The 23 new wave-0 platform stories have no release date | Delivery lead | Resolved (directive) |
| GAP-3234 | Ten class X rows point at a platform application story rather than at a DB, INF or OPS story | TechX (platform) | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3241 | Two items that version 3 still orders are retired by D-RCV-60, and no source states what a squad does with a retired item in the order | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3251 | Non-feature tasks NF-01..NF-08 have no story master | Delivery lead | Resolved (directive) |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

| Story | Check | Line | Detail |
|---|---|---|---|
| RWB-PLT-NF08-INF | new AC without TC row | 358 | AC8 is new and no section 16 row covers it |
