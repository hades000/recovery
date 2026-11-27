# Recovery Workbench Microservice Change Register v1

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

One row per legacy story. Built and in-build Epic 1 work is not changed unless absolutely needed (U2).

## Summary

| Disposition | Legacy stories | Meaning |
|---|---|---|
| Moved (no impact) | 24 | Moved to its service epic; content unchanged. |
| Must change | 1 | In build and must change to fit Arch v5. |
| New | 17 | New story created by the realignment. |
| Preserved + delta | 6 | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| Removed (D-RCV-35 U1) | 1 | Cancelled: removed under D-RCV-35 U1. No new story. |
| Retired (D-RCV-60) | 2 | Retired by the realignment. |
| Split (rework) | 308 | Split into linked stories by service and team type. |

## Stories

| Legacy key | Title | Disposition | Build status | New stories | Reason |
|---|---|---|---|---|---|
| N001 | gateway-bff route contract | New | Not started | RWB-PLT-N001-CON, RWB-PLT-N001-APP | New story created by the realignment. |
| N002 | Kafka topics, retry and dead-letter topics and ACLs | New | Not started | RWB-PLT-N002-INF | New story created by the realignment. |
| N003 | Temporal namespace rwb-recovery and codec key | New | Not started | RWB-PLT-N003-INF | New story created by the realignment. |
| N004 | Service pipeline template and Helm chart | New | Not started | RWB-PLT-N004-OPS | New story created by the realignment. |
| N005 | Platform dashboards and alerts baseline | New | Not started | RWB-PLT-N005-OPS | New story created by the realignment. |
| N006 | Redis session store for gateway-bff | New | Not started | RWB-PLT-N006-INF | New story created by the realignment. |
| N007 | Partner gateway in the DMZ (FAPI 2.0) | New | Not started | RWB-PLT-N007-INF | New story created by the realignment. |
| N008 | Schema registry with BACKWARD compatibility | New | Not started | RWB-PLT-N008-INF | New story created by the realignment. |
| N009 | RFC 9457 problem and Idempotency-Key helpers - interface and fake | New | Not started | RWB-PLT-N009-CON, RWB-PLT-N009-APP | New story created by the realignment. |
| N010 | Workflow kit templates - interface and fake | New | Not started | RWB-PLT-N010-CON, RWB-PLT-N010-APP | New story created by the realignment. |
| N011 | PgBouncer pools, migrator role and grant check | New | Not started | RWB-PLT-N011-DB | New story created by the realignment. |
| N012 | Blob, Key Vault and MFT/SFTP standard resources | New | Not started | RWB-PLT-N012-INF | New story created by the realignment. |
| NF-01 | Repository and pipeline baseline | Moved (no impact) | Not started | RWB-PLT-NF01-OPS | Moved to its service epic; content unchanged. |
| NF-02 | Shared library baseline | Moved (no impact) | Not started | RWB-PLT-NF02-APP | Moved to its service epic; content unchanged. |
| NF-03 | Environment baseline | Moved (no impact) | Not started | RWB-PLT-NF03-OPS | Moved to its service epic; content unchanged. |
| NF-04 | Secrets and configuration baseline | Moved (no impact) | Not started | RWB-PLT-NF04-OPS | Moved to its service epic; content unchanged. |
| NF-05 | Quality gates baseline | Moved (no impact) | Not started | RWB-PLT-NF05-OPS | Moved to its service epic; content unchanged. |
| NF-06 | Create the 19 rwb_* schemas and logins | Moved (no impact) | Not started | RWB-PLT-NF06-DB | Moved to its service epic; content unchanged. |
| NF-07 | Airflow edge integration | Moved (no impact) | Not started | RWB-PLT-NF07-INF | Moved to its service epic; content unchanged. |
| NF-08 | Temporal platform baseline | Moved (no impact) | Not started | RWB-PLT-NF08-INF | Moved to its service epic; content unchanged. |
| RWB-ACE-001 | ACE DB additions for the Recovery Workbench | Split (rework) | Not started | RWB-P1-ACE001-DB | Split into linked stories by service and team type. |
| RWB-AD-001 | Map Entra ID groups to Workbench roles | Split (rework) | Not started | RWB-P4-AD001-CON, RWB-P4-AD001-APP | Split into linked stories by service and team type. |
| RWB-AD-002 | Permission matrix as a versioned load | Split (rework) | Not started | RWB-P4-AD002-CON, RWB-P4-AD002-APP | Split into linked stories by service and team type. |
| RWB-AD-003 | Scope per role | Split (rework) | Not started | RWB-P4-AD003-CON, RWB-P4-AD003-APP | Split into linked stories by service and team type. |
| RWB-AD-004 | Masking profiles per role | Split (rework) | Not started | RWB-P4-AD004-CON, RWB-P4-AD004-APP | Split into linked stories by service and team type. |
| RWB-AD-005 | Separation of duty check at sign-in | Split (rework) | Not started | RWB-P4-AD005-CON, RWB-P4-AD005-APP | Split into linked stories by service and team type. |
| RWB-AD-006 | Break-glass access | Split (rework) | Not started | RWB-P4-AD006-CON, RWB-P4-AD006-APP, RWB-P4-AD006-DB | Split into linked stories by service and team type. |
| RWB-AD-007 | Access log search and export | Split (rework) | Not started | RWB-P4-AD007-CON, RWB-P4-AD007-APP | Split into linked stories by service and team type. |
| RWB-AD-008 | Access review list | Split (rework) | Not started | RWB-P4-AD008-CON, RWB-P4-AD008-APP | Split into linked stories by service and team type. |
| RWB-AD-009 | Load a list of values version | Split (rework) | Not started | RWB-P4-AD009-CON, RWB-P4-AD009-APP | Split into linked stories by service and team type. |
| RWB-AD-010 | Approve a reference data load | Split (rework) | Not started | RWB-P4-AD010-CON, RWB-P4-AD010-APP | Split into linked stories by service and team type. |
| RWB-AD-011 | Load a rule version | Split (rework) | Not started | RWB-P4-AD011-CON, RWB-P4-AD011-APP | Split into linked stories by service and team type. |
| RWB-AD-012 | Approve a rule version | Split (rework) | Not started | RWB-P4-AD012-CON, RWB-P4-AD012-APP | Split into linked stories by service and team type. |
| RWB-AD-013 | Roll back a rule or reference version | Split (rework) | Not started | RWB-P4-AD013-CON, RWB-P4-AD013-APP | Split into linked stories by service and team type. |
| RWB-AD-014 | Configure queues | Split (rework) | Not started | RWB-P4-AD014-CON, RWB-P4-AD014-APP, RWB-ITG-AD014-ITG | Split into linked stories by service and team type. |
| RWB-AD-015 | Configure service levels and timers | Split (rework) | Not started | RWB-P4-AD015-CON, RWB-P4-AD015-APP, RWB-ITG-AD015-ITG | Split into linked stories by service and team type. |
| RWB-AD-016 | Load the delegation of authority table | Split (rework) | Not started | RWB-P4-AD016-CON, RWB-P4-AD016-APP | Split into linked stories by service and team type. |
| RWB-AD-017 | Manage letter and notice templates | Split (rework) | Not started | RWB-P6-AD017-CON, RWB-P6-AD017-APP | Split into linked stories by service and team type. |
| RWB-AD-018 | Interface and job monitor | Split (rework) | Not started | RWB-P1-AD018-CON, RWB-P1-AD018-APP, RWB-P1-AD018-OPS, RWB-ITG-AD018-ITG | Split into linked stories by service and team type. |
| RWB-AD-019 | Data quality and reconciliation console | Split (rework) | Not started | RWB-P1-AD019-APP, RWB-P3-AD019-APP, RWB-P1-AD019-OPS, RWB-ITG-AD019-ITG | Split into linked stories by service and team type. |
| RWB-AD-020 | Autonomy level per decision step | Split (rework) | Not started | RWB-P10-AD020-CON, RWB-P10-AD020-APP | Split into linked stories by service and team type. |
| RWB-AD-021 | Retention classes and legal hold | Split (rework) | Not started | RWB-P5-AD021-CON, RWB-P5-AD021-APP | Split into linked stories by service and team type. |
| RWB-AD-022 | Partner firms and partner users | Split (rework) | Not started | RWB-S9-AD022-CON, RWB-S9-AD022-APP, RWB-ITG-AD022-ITG | Split into linked stories by service and team type. |
| RWB-DM-001 | Migrate account and arrears | Split (rework) | Not started | RWB-P1-DM001-APP | Split into linked stories by service and team type. |
| RWB-DM-002 | Migrate customer and party | Split (rework) | Not started | RWB-P1-DM002-APP | Split into linked stories by service and team type. |
| RWB-DM-003 | Migrate case and ownership | Split (rework) | Not started | RWB-P1-DM003-APP, RWB-ITG-DM003-ITG | Split into linked stories by service and team type. |
| RWB-DM-004 | Migrate treatment and offers | Split (rework) | Not started | RWB-P1-DM004-APP, RWB-ITG-DM004-ITG | Split into linked stories by service and team type. |
| RWB-DM-005 | Migrate contact and promises | Split (rework) | Not started | RWB-P1-DM005-APP, RWB-ITG-DM005-ITG | Split into linked stories by service and team type. |
| RWB-DM-006 | Migrate collateral and assets | Split (rework) | Not started | RWB-P1-DM006-APP, RWB-ITG-DM006-ITG | Split into linked stories by service and team type. |
| RWB-DM-007 | Migrate legal events and cases | Split (rework) | Not started | RWB-P1-DM007-APP, RWB-ITG-DM007-ITG | Split into linked stories by service and team type. |
| RWB-DM-008 | Migrate partner performance | Split (rework) | Not started | RWB-P1-DM008-APP, RWB-ITG-DM008-ITG | Split into linked stories by service and team type. |
| RWB-DM-009 | Migrate debt sale | Split (rework) | Not started | RWB-P1-DM009-APP, RWB-ITG-DM009-ITG | Split into linked stories by service and team type. |
| RWB-DM-010 | Migrate documents and extracted fields | Split (rework) | Not started | RWB-P1-DM010-APP, RWB-ITG-DM010-ITG | Split into linked stories by service and team type. |
| RWB-DM-011 | Migrate scores and route economics | Split (rework) | Not started | RWB-P1-DM011-APP, RWB-ITG-DM011-ITG | Split into linked stories by service and team type. |
| RWB-DM-012 | Migrate decision log | Split (rework) | Not started | RWB-P1-DM012-APP, RWB-ITG-DM012-ITG | Split into linked stories by service and team type. |
| RWB-DM-013 | Migrate money and closure | Split (rework) | Not started | RWB-P1-DM013-APP, RWB-P8-DM013-APP, RWB-ITG-DM013-ITG | Split into linked stories by service and team type. |
| RWB-DM-014 | Migrate reference data | Split (rework) | Not started | RWB-P1-DM014-APP | Split into linked stories by service and team type. |
| RWB-E1-001 | Recovery tables for the 14 data products | Must change | In build | RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP, RWB-P8-E1001-APP, RWB-ITG-E1001-ITG | In build: creates the single recovery schema (92 tables, 14 data products, dictionary). Arch v5 needs one rwb_<name> schema per service. The built migration is kept unchanged; the split is new work in RWB-PLT-NF06-DB and the per-service DB stories, and each table moves to its owner schema by the Ownership Map. Only change if absolutely needed (U2). |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | Split (rework) | Not started | RWB-P1-E1002-APP, RWB-P3-E1002-APP, RWB-P1-E1002-OPS, RWB-ITG-E1002-ITG, RWB-P1-E1002-CON | Split into linked stories by service and team type. |
| RWB-E1-007 | Integration adapters for outbound files | Split (rework) | Not started | RWB-P2-E1007-CON, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P6-E1007-APP, RWB-P5-E1007-APP, RWB-P4-E1007-APP, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-ITG-E1007-ITG | Split into linked stories by service and team type. |
| RWB-E1-008 | Decision log store v1, append only and hash chained | Split (rework) | Not started | RWB-P7-E1008-CON, RWB-P7-E1008-APP, RWB-P4-E1008-APP, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-ITG-E1008-ITG | Split into linked stories by service and team type. |
| RWB-E1-011 | Reconciliation and data quality report | Split (rework) | Not started | RWB-P1-E1011-APP, RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P6-E1011-APP, RWB-P1-E1011-OPS, RWB-ITG-E1011-ITG, RWB-P1-E1011-CON | Split into linked stories by service and team type. |
| RWB-E1-013 | Baseline measures | Split (rework) | Not started | RWB-P9-E1013-CON, RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP, RWB-P9-E1013-OPS, RWB-ITG-E1013-ITG | Split into linked stories by service and team type. |
| RWB-E1-014 | Decision log copy to the data lake | Retired (D-RCV-60) | Built | None | Decision log copy to the data lake. Arch v5 has no data lake (ADR-018); reporting reads events into the rwb-reporting read model. |
| RWB-E1-015 | Freshness stamp per data product | Split (rework) | Not started | RWB-P1-E1015-CON, RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-ITG-E1015-ITG | Split into linked stories by service and team type. |
| RWB-E1-016 | Access control per data product and catalog entries | Split (rework) | Not started | RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP, RWB-P1-E1016-DB, RWB-ITG-E1016-ITG, RWB-P1-E1016-CON | Split into linked stories by service and team type. |
| RWB-E1-017 | Retention and archive rule for the data store | Split (rework) | Not started | RWB-P1-E1017-CON, RWB-P1-E1017-APP, RWB-P5-E1017-APP, RWB-P7-E1017-APP, RWB-P1-E1017-OPS, RWB-ITG-E1017-ITG | Split into linked stories by service and team type. |
| RWB-E1-018 | Case ID issuance and case record v1 | Split (rework) | Not started | RWB-P3-E1018-CON, RWB-P3-E1018-APP, RWB-P5-E1018-APP, RWB-P1-E1018-APP, RWB-P4-E1018-APP, RWB-P7-E1018-APP, RWB-P3-E1018-OPS, RWB-ITG-E1018-ITG | Split into linked stories by service and team type. |
| RWB-E1-019 | Roles, teams and queues as data | Split (rework) | Not started | RWB-P3-E1019-CON, RWB-P3-E1019-APP, RWB-P4-E1019-APP, RWB-P6-E1019-APP, RWB-P3-E1019-DB, RWB-ITG-E1019-ITG | Split into linked stories by service and team type. |
| RWB-E1-020 | Allocation and assignment engine v1 | Split (rework) | Not started | RWB-P3-E1020-CON, RWB-P3-E1020-APP, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP, RWB-P3-E1020-OPS, RWB-ITG-E1020-ITG | Split into linked stories by service and team type. |
| RWB-E1-021 | Transfer rules and engine v1 | Split (rework) | Not started | RWB-P3-E1021-CON, RWB-P3-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP, RWB-P5-E1021-APP, RWB-P4-E1021-APP, RWB-P3-E1021-OPS, RWB-ITG-E1021-ITG | Split into linked stories by service and team type. |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | Split (rework) | Not started | RWB-P4-E1022-CON, RWB-P4-E1022-APP, RWB-P4-E1022-DB, RWB-ITG-E1022-ITG | Split into linked stories by service and team type. |
| RWB-E1-023 | Case record view v1, read only | Split (rework) | Not started | RWB-P3-E1023-CON, RWB-P3-E1023-APP, RWB-P4-E1023-APP, RWB-S8-E1023-APP, RWB-ITG-E1023-ITG | Split into linked stories by service and team type. |
| RWB-E1-024 | Document store and index | Moved (no impact) | Not started | RWB-P5-E1024-APP, RWB-ITG-E1024-ITG | Moved to its service epic; content unchanged. |
| RWB-E1-025 | Document types and fields agreed | Moved (no impact) | Not started | RWB-P5-E1025-APP, RWB-ITG-E1025-ITG | Moved to its service epic; content unchanged. |
| RWB-E1-026 | Attach and search screen | Moved (no impact) | Not started | RWB-P5-E1026-APP, RWB-ITG-E1026-ITG | Moved to its service epic; content unchanged. |
| RWB-E1-027 | Decision log writer v1 | Split (rework) | Not started | RWB-PLT-E1027-CON, RWB-PLT-E1027-APP, RWB-P7-E1027-CON, RWB-P7-E1027-APP, RWB-ITG-E1027-ITG | Split into linked stories by service and team type. |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | Split (rework) | Not started | RWB-P3-E1028-CON, RWB-P3-E1028-APP, RWB-P4-E1028-APP, RWB-P7-E1028-APP, RWB-P3-E1028-OPS, RWB-ITG-E1028-ITG | Split into linked stories by service and team type. |
| RWB-E1-030 | Daily rebalancing and queue measures | Split (rework) | Not started | RWB-P3-E1030-CON, RWB-P3-E1030-APP, RWB-P7-E1030-APP, RWB-P3-E1030-OPS, RWB-ITG-E1030-ITG | Split into linked stories by service and team type. |
| RWB-E1-031 | Queue and owner on the case list with filters | Split (rework) | Not started | RWB-P3-E1031-CON, RWB-P3-E1031-APP, RWB-ITG-E1031-ITG | Split into linked stories by service and team type. |
| RWB-E1-032 | Automatic attach from the OCR intake | Split (rework) | Not started | RWB-P5-E1032-CON, RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-P7-E1032-APP, RWB-P5-E1032-INF, RWB-P5-E1032-OPS, RWB-ITG-E1032-ITG | Split into linked stories by service and team type. |
| RWB-E1-033 | Search across cases | Moved (no impact) | Not started | RWB-P5-E1033-APP | Moved to its service epic; content unchanged. |
| RWB-E1-034 | Letter template management | Moved (no impact) | Not started | RWB-P6-E1034-APP, RWB-ITG-E1034-ITG | Moved to its service epic; content unchanged. |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | Split (rework) | Not started | RWB-P3-E1035-CON, RWB-P3-E1035-APP | Split into linked stories by service and team type. |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | Split (rework) | Not started | RWB-PLT-E1037-CON, RWB-PLT-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1037-APP, RWB-ITG-E1037-ITG | Split into linked stories by service and team type. |
| RWB-E1-038 | Delegation of authority table as reference data | Moved (no impact) | Not started | RWB-P4-E1038-APP | Moved to its service epic; content unchanged. |
| RWB-E1-039 | Access log into the decision log and break-glass admin | Split (rework) | Not started | RWB-P4-E1039-CON, RWB-P4-E1039-APP, RWB-P5-E1039-APP, RWB-P7-E1039-APP, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-ITG-E1039-ITG | Split into linked stories by service and team type. |
| RWB-E1-040 | Document checklist per case type as reference data | Moved (no impact) | Not started | RWB-P5-E1040-APP | Moved to its service epic; content unchanged. |
| RWB-E1-041 | Retention classes and virus scan on intake | Moved (no impact) | Not started | RWB-P5-E1041-APP, RWB-P5-E1041-CON | Moved to its service epic; content unchanged. |
| RWB-E1-042 | Central configuration service and parameter catalog | Preserved + delta | In build | RWB-PLT-E1042-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-OPS, RWB-P3-E1042-APP, RWB-P3-E1042-CON | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-E1-043 | Reference data service with versioned tables | Preserved + delta | In build | RWB-PLT-E1043-CON, RWB-PLT-E1043-APP, RWB-P3-E1043-APP, RWB-P3-E1043-CON | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-E1-044 | Database migrations versioned with parameterized schema names | Preserved + delta | In build | RWB-PLT-E1044-APP, RWB-PLT-E1044-CON, RWB-PLT-E1044-APP-2, RWB-PLT-E1044-OPS | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | Moved (no impact) | Not started | RWB-P3-E1045-APP | Moved to its service epic; content unchanged. |
| RWB-E1-046 | Template and merge field catalog as data | Split (rework) | Not started | RWB-P6-E1046-CON, RWB-P6-E1046-APP, RWB-P7-E1046-APP, RWB-P5-E1046-APP, RWB-ITG-E1046-ITG | Split into linked stories by service and team type. |
| RWB-E1-047 | Feature flags for module release with a removal date | Split (rework) | Not started | RWB-PLT-E1047-CON, RWB-PLT-E1047-APP, RWB-ITG-E1047-ITG | Split into linked stories by service and team type. |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | Split (rework) | Not started | RWB-P5-E1049-CON, RWB-P5-E1049-APP, RWB-P6-E1049-APP, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-ITG-E1049-ITG | Split into linked stories by service and team type. |
| RWB-E1-050 | Document classification | Split (rework) | Not started | RWB-P5-E1050-APP, RWB-P3-E1050-APP, RWB-P5-E1050-OPS, RWB-ITG-E1050-ITG, RWB-P5-E1050-CON | Split into linked stories by service and team type. |
| RWB-E1-052 | Notice generation v1 | Split (rework) | Not started | RWB-P6-E1052-CON, RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP, RWB-P7-E1052-APP, RWB-ITG-E1052-ITG | Split into linked stories by service and team type. |
| RWB-E1-053 | Field extraction for the six types into the index | Moved (no impact) | Not started | RWB-P5-E1053-APP, RWB-P5-E1053-CON | Moved to its service epic; content unchanged. |
| RWB-E1-054 | Review queue for low-confidence documents | Split (rework) | Not started | RWB-P5-E1054-CON, RWB-P5-E1054-APP, RWB-P4-E1054-APP, RWB-P3-E1054-APP, RWB-P7-E1054-APP, RWB-ITG-E1054-ITG | Split into linked stories by service and team type. |
| RWB-E1-055 | Proof of delivery capture design with WIN | Split (rework) | Not started | RWB-P6-E1055-CON, RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P1-E1055-APP, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-ITG-E1055-ITG | Split into linked stories by service and team type. |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | Split (rework) | Not started | RWB-PLT-E1056-OPS | Split into linked stories by service and team type. |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | Split (rework) | Not started | RWB-P5-E1057-CON, RWB-P5-E1057-APP, RWB-S9-E1057-APP, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-ITG-E1057-ITG | Split into linked stories by service and team type. |
| RWB-E1-058 | Agent platform set-up [E1a] | Split (rework) | Not started | RWB-P10-E1058-CON, RWB-P10-E1058-APP, RWB-P10-E1058-INF, RWB-P10-E1058-OPS, RWB-ITG-E1058-ITG | Split into linked stories by service and team type. |
| RWB-E1-059 | Case intake agent in shadow [E1b] | Split (rework) | Not started | RWB-P10-E1059-CON, RWB-P10-E1059-APP, RWB-ITG-E1059-ITG | Split into linked stories by service and team type. |
| RWB-E1-060 | Extraction evaluation [E1c] | Moved (no impact) | Not started | RWB-P10-E1060-APP, RWB-ITG-E1060-ITG | Moved to its service epic; content unchanged. |
| RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | Moved (no impact) | Not started | RWB-P10-E1061-APP, RWB-P10-E1061-CON | Moved to its service epic; content unchanged. |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | Split (rework) | Not started | RWB-P10-E1062-CON, RWB-P10-E1062-APP, RWB-S8-E1062-APP, RWB-P5-E1062-APP, RWB-P4-E1062-APP, RWB-ITG-E1062-ITG | Split into linked stories by service and team type. |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | Split (rework) | Not started | RWB-P10-E1063-CON, RWB-P10-E1063-APP, RWB-P4-E1063-APP, RWB-P6-E1063-APP, RWB-P10-E1063-OPS, RWB-ITG-E1063-ITG | Split into linked stories by service and team type. |
| RWB-E1-064 | Data dictionary for the 14 data products | Split (rework) | Not started | RWB-P1-E1064-CON, RWB-P1-E1064-APP, RWB-P4-E1064-APP, RWB-P1-E1064-OPS, RWB-ITG-E1064-ITG | Split into linked stories by service and team type. |
| RWB-E1-065 | Sandbox database with synthetic recovery data | Split (rework) | Not started | RWB-P1-E1065-CON, RWB-P1-E1065-APP, RWB-P4-E1065-APP, RWB-P3-E1065-APP, RWB-S8-E1065-APP, RWB-P5-E1065-APP, RWB-P1-E1065-DB, RWB-ITG-E1065-ITG | Split into linked stories by service and team type. |
| RWB-E1-066 | Interaction ledger store and writer | Split (rework) | Not started | RWB-P1-E1066-CON, RWB-P1-E1066-APP, RWB-P3-E1066-APP, RWB-P1-E1066-OPS, RWB-ITG-E1066-ITG | Split into linked stories by service and team type. |
| RWB-E1-067 | Every Workbench action into the interaction ledger | Split (rework) | Not started | RWB-P1-E1067-CON, RWB-P1-E1067-APP, RWB-P3-E1067-APP, RWB-P5-E1067-APP, RWB-ITG-E1067-ITG | Split into linked stories by service and team type. |
| RWB-E1-068 | Interaction ledger read interface | Moved (no impact) | Not started | RWB-P1-E1068-APP | Moved to its service epic; content unchanged. |
| RWB-E1-069 | Read-only ACE source views, grants and boundary rule | Split (rework) | Not started | RWB-P1-E1069-APP, RWB-P4-E1069-APP, RWB-P1-E1069-DB, RWB-ITG-E1069-ITG | Split into linked stories by service and team type. |
| RWB-E1-070 | Temporal platform on the ACE AKS clusters | Split (rework) | Not started | RWB-PLT-E1070-CON, RWB-PLT-E1070-APP, RWB-ITG-E1070-ITG | Split into linked stories by service and team type. |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | Split (rework) | Not started | RWB-PLT-E1071-CON, RWB-PLT-E1071-APP | Split into linked stories by service and team type. |
| RWB-E1-072 | Drools runtime and rule package store | Split (rework) | Not started | RWB-PLT-E1072-CON, RWB-PLT-E1072-APP | Split into linked stories by service and team type. |
| RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools | Split (rework) | Not started | RWB-P3-E1073-CON, RWB-P3-E1073-APP, RWB-P7-E1073-APP, RWB-P6-E1073-APP, RWB-P2-E1073-APP, RWB-P3-E1073-INF, RWB-ITG-E1073-ITG | Split into linked stories by service and team type. |
| RWB-E2-001 | EFS hand-over with full history | Split (rework) | Not started | RWB-P2-E2001-CON, RWB-P2-E2001-APP, RWB-P1-E2001-APP, RWB-P3-E2001-APP, RWB-P7-E2001-APP, RWB-P2-E2001-OPS, RWB-ITG-E2001-ITG | Split into linked stories by service and team type. |
| RWB-E2-002 | ACE plan status on the case | Split (rework) | Not started | RWB-P2-E2002-CON, RWB-P2-E2002-APP, RWB-P3-E2002-APP, RWB-P4-E2002-APP, RWB-P7-E2002-APP, RWB-P2-E2002-OPS, RWB-ITG-E2002-ITG | Split into linked stories by service and team type. |
| RWB-E2-003 | Customer's other products on the case | Split (rework) | Not started | RWB-P2-E2003-APP, RWB-P4-E2003-APP, RWB-ITG-E2003-ITG | Split into linked stories by service and team type. |
| RWB-E2-004 | Treatment entity and plan timers data model | Split (rework) | Not started | RWB-P3-E2004-CON, RWB-P3-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP, RWB-P4-E2004-APP, RWB-P3-E2004-OPS, RWB-ITG-E2004-ITG | Split into linked stories by service and team type. |
| RWB-E2-005 | Decision log query API for audit | Split (rework) | Not started | RWB-P7-E2005-CON, RWB-P7-E2005-APP, RWB-ITG-E2005-ITG | Split into linked stories by service and team type. |
| RWB-E2-006 | Credit approval pack for NLEADS | Split (rework) | Not started | RWB-P2-E2006-APP, RWB-P7-E2006-APP, RWB-S2-E2006-APP, RWB-P3-E2006-APP, RWB-ITG-E2006-ITG | Split into linked stories by service and team type. |
| RWB-E2-007 | Booking confirmation from the ALS load | Split (rework) | Not started | RWB-P2-E2007-CON, RWB-P2-E2007-APP, RWB-P3-E2007-APP, RWB-P4-E2007-APP, RWB-S2-E2007-APP, RWB-P1-E2007-APP, RWB-P7-E2007-APP, RWB-P2-E2007-OPS, RWB-ITG-E2007-ITG | Split into linked stories by service and team type. |
| RWB-E2-008 | Payment matching with the missed payment event | Split (rework) | Not started | RWB-P8-E2008-CON, RWB-P8-E2008-APP, RWB-S2-E2008-APP, RWB-P1-E2008-APP, RWB-P7-E2008-APP, RWB-P4-E2008-APP, RWB-P8-E2008-OPS, RWB-ITG-E2008-ITG | Split into linked stories by service and team type. |
| RWB-E2-009 | Steering dashboard v1 data set | Split (rework) | Not started | RWB-P9-E2009-CON, RWB-P9-E2009-APP, RWB-P3-E2009-APP, RWB-S8-E2009-APP, RWB-P9-E2009-OPS, RWB-ITG-E2009-ITG | Split into linked stories by service and team type. |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | Split (rework) | Not started | RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-P1-E2010-OPS, RWB-ITG-E2010-ITG | Split into linked stories by service and team type. |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | Moved (no impact) | Not started | RWB-P3-E2011-CON, RWB-P3-E2011-APP | Moved to its service epic; content unchanged. |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | Split (rework) | Not started | RWB-P3-E2012-CON, RWB-P3-E2012-APP, RWB-S8-E2012-APP, RWB-P7-E2012-APP, RWB-P3-E2012-OPS, RWB-ITG-E2012-ITG | Split into linked stories by service and team type. |
| RWB-E2-013 | Approval routing with the delegation of authority table | Split (rework) | Not started | RWB-P7-E2013-CON, RWB-P7-E2013-APP, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-OPS, RWB-ITG-E2013-ITG | Split into linked stories by service and team type. |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | Split (rework) | Not started | RWB-P7-E2014-CON, RWB-P7-E2014-APP, RWB-P6-E2014-APP, RWB-P4-E2014-APP, RWB-P3-E2014-APP, RWB-P7-E2014-OPS, RWB-ITG-E2014-ITG | Split into linked stories by service and team type. |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | Split (rework) | Not started | RWB-P3-E2015-CON, RWB-P3-E2015-APP, RWB-S8-E2015-APP, RWB-P4-E2015-APP, RWB-P3-E2015-OPS, RWB-ITG-E2015-ITG | Split into linked stories by service and team type. |
| RWB-E2-016 | Full case record view with the history timeline | Split (rework) | Not started | RWB-P3-E2016-CON, RWB-P3-E2016-APP, RWB-P5-E2016-APP, RWB-ITG-E2016-ITG | Split into linked stories by service and team type. |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | Split (rework) | Not started | RWB-P5-E2017-CON, RWB-P5-E2017-APP, RWB-S2-E2017-APP, RWB-P7-E2017-APP, RWB-P6-E2017-APP, RWB-P4-E2017-APP, RWB-ITG-E2017-ITG | Split into linked stories by service and team type. |
| RWB-E2-018 | E-signature flow for customers and the bank | Split (rework) | Not started | RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-S2-E2018-APP, RWB-P6-E2018-OPS, RWB-ITG-E2018-ITG | Split into linked stories by service and team type. |
| RWB-E2-019 | Partner identities through the external gateway | Split (rework) | Not started | RWB-P4-E2019-CON, RWB-P4-E2019-APP, RWB-S9-E2019-APP, RWB-P7-E2019-APP, RWB-P4-E2019-INF, RWB-ITG-E2019-ITG | Split into linked stories by service and team type. |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | Split (rework) | Not started | RWB-P6-E2021-CON, RWB-P6-E2021-APP, RWB-P1-E2021-APP, RWB-P4-E2021-APP, RWB-P3-E2021-APP, RWB-P7-E2021-APP, RWB-P6-E2021-OPS, RWB-ITG-E2021-ITG | Split into linked stories by service and team type. |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | Split (rework) | Not started | RWB-P6-E2022-CON, RWB-P6-E2022-APP, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P7-E2022-APP, RWB-P6-E2022-OPS, RWB-ITG-E2022-ITG | Split into linked stories by service and team type. |
| RWB-E2-023 | Automated EFS file load | Removed (D-RCV-35 U1) | Not specified in the source documents (GAP-3218) | None | Cancelled. ACE ingestion owns the EFS load and its checks; the later home of the work is the ACE team backlog (RWB-ACE-001). Its 8 acceptance criteria and 9 test cases are withdrawn (User Stories Epic 2 v6). |
| RWB-E2-024 | Field app photos and bills into the document hub | Split (rework) | Not started | RWB-P5-E2024-CON, RWB-P5-E2024-APP, RWB-P4-E2024-APP, RWB-P3-E2024-APP, RWB-P7-E2024-APP, RWB-ITG-E2024-ITG | Split into linked stories by service and team type. |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | Split (rework) | Not started | RWB-P5-E2025-CON, RWB-P5-E2025-APP, RWB-P7-E2025-APP, RWB-S4-E2025-APP, RWB-S2-E2025-APP, RWB-P5-E2025-OPS, RWB-ITG-E2025-ITG | Split into linked stories by service and team type. |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | Split (rework) | Not started | RWB-P5-E2026-CON, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-S2-E2026-APP, RWB-P4-E2026-APP, RWB-P7-E2026-APP, RWB-ITG-E2026-ITG | Split into linked stories by service and team type. |
| RWB-E2-027 | Payment matching rules with the data team | Split (rework) | Not started | RWB-P8-E2027-CON, RWB-P8-E2027-APP, RWB-P4-E2027-APP, RWB-S2-E2027-APP, RWB-P7-E2027-APP, RWB-P8-E2027-OPS, RWB-ITG-E2027-ITG | Split into linked stories by service and team type. |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | Split (rework) | Not started | RWB-P10-E2028-CON, RWB-P10-E2028-APP, RWB-P7-E2028-APP, RWB-P10-E2028-OPS, RWB-ITG-E2028-ITG | Split into linked stories by service and team type. |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | Split (rework) | Not started | RWB-P10-E2029-CON, RWB-P10-E2029-APP, RWB-S8-E2029-APP, RWB-P7-E2029-APP, RWB-ITG-E2029-ITG | Split into linked stories by service and team type. |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | Split (rework) | Not started | RWB-P10-E2030-CON, RWB-P10-E2030-APP, RWB-P5-E2030-APP, RWB-ITG-E2030-ITG | Split into linked stories by service and team type. |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | Split (rework) | Not started | RWB-P10-E2031-CON, RWB-P10-E2031-APP, RWB-P4-E2031-APP, RWB-P10-E2031-OPS, RWB-ITG-E2031-ITG | Split into linked stories by service and team type. |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | Split (rework) | Not started | RWB-P10-E2032-CON, RWB-P10-E2032-APP, RWB-S2-E2032-APP, RWB-P7-E2032-APP, RWB-P10-E2032-INF, RWB-ITG-E2032-ITG | Split into linked stories by service and team type. |
| RWB-E2-033 | Case and queue list with status, owner and ageing | Split (rework) | Not started | RWB-P2-E2033-CON, RWB-P2-E2033-APP, RWB-P3-E2033-APP, RWB-P4-E2033-APP, RWB-S8-E2033-APP, RWB-ITG-E2033-ITG | Split into linked stories by service and team type. |
| RWB-E2-034 | Interaction ledger on the case and from every channel | Split (rework) | Not started | RWB-P2-E2034-CON, RWB-P2-E2034-APP, RWB-S9-E2034-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P1-E2034-APP, RWB-P2-E2034-OPS, RWB-ITG-E2034-ITG | Split into linked stories by service and team type. |
| RWB-E2-035 | Next action on the case | Split (rework) | Not started | RWB-P2-E2035-CON, RWB-P2-E2035-APP, RWB-P4-E2035-APP, RWB-P3-E2035-APP, RWB-P7-E2035-APP, RWB-P2-E2035-OPS, RWB-ITG-E2035-ITG | Split into linked stories by service and team type. |
| RWB-E2-036 | Queue write interface for models and agents | Split (rework) | Not started | RWB-P2-E2036-CON, RWB-P2-E2036-APP, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-S8-E2036-APP, RWB-P7-E2036-APP, RWB-ITG-E2036-ITG | Split into linked stories by service and team type. |
| RWB-E2-037 | Temporal observability and run books | Split (rework) | Not started | RWB-PLT-E2037-CON, RWB-PLT-E2037-APP | Split into linked stories by service and team type. |
| RWB-E2-038 | Temporal security, codec server and admin audit | Split (rework) | Not started | RWB-PLT-E2038-CON, RWB-PLT-E2038-APP, RWB-ITG-E2038-ITG | Split into linked stories by service and team type. |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive | Split (rework) | Not started | RWB-PLT-E2039-CON, RWB-PLT-E2039-APP | Split into linked stories by service and team type. |
| RWB-E2-040 | Workflow versioning and replay test gate | Split (rework) | Not started | RWB-PLT-E2040-CON, RWB-PLT-E2040-APP | Split into linked stories by service and team type. |
| RWB-E2-041 | Rule change governance and audit report | Split (rework) | Not started | RWB-P3-E2041-CON, RWB-P3-E2041-APP, RWB-P4-E2041-APP, RWB-P7-E2041-APP, RWB-ITG-E2041-ITG | Split into linked stories by service and team type. |
| RWB-E2-042 | Epic 2 rule packages in Drools | Split (rework) | Not started | RWB-P3-E2042-CON, RWB-P3-E2042-APP, RWB-P6-E2042-APP, RWB-P4-E2042-APP, RWB-P7-E2042-APP, RWB-P3-E2042-INF, RWB-P3-E2042-OPS, RWB-ITG-E2042-ITG | Split into linked stories by service and team type. |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | Split (rework) | Not started | RWB-P3-E2043-CON, RWB-P3-E2043-APP, RWB-P7-E2043-APP, RWB-P3-E2043-OPS, RWB-ITG-E2043-ITG | Split into linked stories by service and team type. |
| RWB-E3-001 | Create the treatment record | Split (rework) | Not started | RWB-S2-E3001-CON, RWB-S2-E3001-APP | Split into linked stories by service and team type. |
| RWB-E3-002 | Offer a settlement inside the range | Split (rework) | Not started | RWB-S2-E3002-CON, RWB-S2-E3002-APP | Split into linked stories by service and team type. |
| RWB-E3-003 | Approve a settlement below the floor | Split (rework) | Not started | RWB-S2-E3003-CON, RWB-S2-E3003-APP | Split into linked stories by service and team type. |
| RWB-E3-004 | Offer a TDR plan | Split (rework) | Not started | RWB-S2-E3004-CON, RWB-S2-E3004-APP | Split into linked stories by service and team type. |
| RWB-E3-005 | Pre-assess affordability through ACE | Split (rework) | Not started | RWB-S2-E3005-CON, RWB-S2-E3005-APP | Split into linked stories by service and team type. |
| RWB-E3-006 | Calculate the plan installment | Split (rework) | Not started | RWB-S2-E3006-CON, RWB-S2-E3006-APP, RWB-ITG-E3006-ITG | Split into linked stories by service and team type. |
| RWB-E3-007 | Send the offer and start the validity timer | Split (rework) | Not started | RWB-S2-E3007-CON, RWB-S2-E3007-APP | Split into linked stories by service and team type. |
| RWB-E3-008 | Route the signed offer to operations for booking | Split (rework) | Not started | RWB-S2-E3008-CON, RWB-S2-E3008-APP | Split into linked stories by service and team type. |
| RWB-E3-009 | Return the case to its prior status on no signature | Split (rework) | Not started | RWB-S2-E3009-CON, RWB-S2-E3009-APP | Split into linked stories by service and team type. |
| RWB-E3-010 | Book the plan and set the schedule | Split (rework) | Not started | RWB-S2-E3010-CON, RWB-S2-E3010-APP, RWB-ITG-E3010-ITG | Split into linked stories by service and team type. |
| RWB-E3-011 | Detect and handle a broken plan | Split (rework) | Not started | RWB-S2-E3011-CON, RWB-S2-E3011-APP | Split into linked stories by service and team type. |
| RWB-E3-012 | Run a deed in lieu to ownership transfer | Split (rework) | Not started | RWB-S2-E3012-CON, RWB-S2-E3012-APP | Split into linked stories by service and team type. |
| RWB-E3-013 | Check encumbrance and eligibility before negotiation | Split (rework) | Not started | RWB-S2-E3013-CON, RWB-S2-E3013-APP, RWB-P3-E3013-APP, RWB-ITG-E3013-ITG | Split into linked stories by service and team type. |
| RWB-E3-014 | Unlock the asset as a non performing asset by rule | Split (rework) | Not started | RWB-S2-E3014-CON, RWB-S2-E3014-APP | Split into linked stories by service and team type. |
| RWB-E3-015 | Capture the collateral inspection in the field | Split (rework) | Not started | RWB-S2-E3015-CON, RWB-S2-E3015-APP | Split into linked stories by service and team type. |
| RWB-E3-016 | Set up a deed in lieu buy-back rental | Split (rework) | Not started | RWB-S2-E3016-CON, RWB-S2-E3016-APP | Split into linked stories by service and team type. |
| RWB-E3-017 | Release the collateral after settlement | Split (rework) | Not started | RWB-S2-E3017-CON, RWB-S2-E3017-APP, RWB-ITG-E3017-ITG | Split into linked stories by service and team type. |
| RWB-E3-018 | Generate the treatment document set | Split (rework) | Not started | RWB-S2-E3018-CON, RWB-S2-E3018-APP | Split into linked stories by service and team type. |
| RWB-E3-019 | Take a repossessed vehicle onto the books | Split (rework) | Not started | RWB-S5-E3019-CON, RWB-S5-E3019-APP | Split into linked stories by service and team type. |
| RWB-E3-020 | Take a property onto the books after a deed in lieu | Split (rework) | Not started | RWB-S5-E3020-CON, RWB-S5-E3020-APP | Split into linked stories by service and team type. |
| RWB-E3-021 | Take a property onto the books after an LED auction | Split (rework) | Not started | RWB-S5-E3021-CON, RWB-S5-E3021-APP | Split into linked stories by service and team type. |
| RWB-E3-022 | Serve the statutory notice and prove delivery | Split (rework) | Not started | RWB-S5-E3022-CON, RWB-S5-E3022-APP | Split into linked stories by service and team type. |
| RWB-E3-023 | Track holding age against the provision steps | Split (rework) | Not started | RWB-S5-E3023-CON, RWB-S5-E3023-APP | Split into linked stories by service and team type. |
| RWB-E3-024 | Record and track the asset stock balance | Split (rework) | Not started | RWB-S5-E3024-CON, RWB-S5-E3024-APP | Split into linked stories by service and team type. |
| RWB-E3-025 | Maintain a held property | Split (rework) | Not started | RWB-S5-E3025-CON, RWB-S5-E3025-APP | Split into linked stories by service and team type. |
| RWB-E3-026 | Re-appraise a held asset on cycle | Split (rework) | Not started | RWB-S5-E3026-CON, RWB-S5-E3026-APP, RWB-ITG-E3026-ITG | Split into linked stories by service and team type. |
| RWB-E3-027 | Recommend the disposal route | Split (rework) | Not started | RWB-S5-E3027-CON, RWB-S5-E3027-APP | Split into linked stories by service and team type. |
| RWB-E3-028 | Set the start and floor price | Split (rework) | Not started | RWB-S5-E3028-CON, RWB-S5-E3028-APP | Split into linked stories by service and team type. |
| RWB-E3-029 | Publish the listing | Split (rework) | Not started | RWB-S5-E3029-CON, RWB-S5-E3029-APP | Split into linked stories by service and team type. |
| RWB-E3-030 | Change an autonomy level | Split (rework) | Not started | RWB-P10-E3030-CON, RWB-P10-E3030-APP | Split into linked stories by service and team type. |
| RWB-E3-031 | Detect model drift and raise a decision | Split (rework) | Not started | RWB-P10-E3031-APP | Split into linked stories by service and team type. |
| RWB-E4-001 | Order an appraisal when the last one is stale | Split (rework) | Not started | RWB-S1-E4001-CON, RWB-S1-E4001-APP, RWB-ITG-E4001-ITG | Split into linked stories by service and team type. |
| RWB-E4-002 | Receive the appraisal value from SVAF | Split (rework) | Not started | RWB-S1-E4002-CON, RWB-S1-E4002-APP, RWB-ITG-E4002-ITG | Split into linked stories by service and team type. |
| RWB-E4-003 | Flag appraisal outliers against market and last value | Split (rework) | Not started | RWB-S1-E4003-CON, RWB-S1-E4003-APP | Split into linked stories by service and team type. |
| RWB-E4-004 | Accept the appraisal value | Split (rework) | Not started | RWB-S1-E4004-CON, RWB-S1-E4004-APP | Split into linked stories by service and team type. |
| RWB-E4-005 | Call COLLINS for return by route | Split (rework) | Not started | RWB-S1-E4005-CON, RWB-S1-E4005-APP | Split into linked stories by service and team type. |
| RWB-E4-006 | Calculate the payoff and settlement range | Split (rework) | Not started | RWB-S1-E4006-CON, RWB-S1-E4006-APP | Split into linked stories by service and team type. |
| RWB-E4-007 | Score the routes and recommend one with reasons | Split (rework) | Not started | RWB-S1-E4007-CON, RWB-S1-E4007-APP | Split into linked stories by service and team type. |
| RWB-E4-008 | Approve a route inside the limit | Split (rework) | Not started | RWB-S1-E4008-CON, RWB-S1-E4008-APP | Split into linked stories by service and team type. |
| RWB-E4-009 | Approve a route above the limit at committee | Split (rework) | Not started | RWB-S1-E4009-CON, RWB-S1-E4009-APP | Split into linked stories by service and team type. |
| RWB-E4-010 | Hold the case and set a review date | Split (rework) | Not started | RWB-S1-E4010-CON, RWB-S1-E4010-APP | Split into linked stories by service and team type. |
| RWB-E4-011 | Reconsider the route after new information | Split (rework) | Not started | RWB-S1-E4011-CON, RWB-S1-E4011-APP | Split into linked stories by service and team type. |
| RWB-E4-012 | Start the route flow and set its timers | Split (rework) | Not started | RWB-S1-E4012-CON, RWB-S1-E4012-APP | Split into linked stories by service and team type. |
| RWB-E4-013 | Prepare a TCG guarantee claim | Split (rework) | Not started | RWB-S3-E4013-CON, RWB-S3-E4013-APP | Split into linked stories by service and team type. |
| RWB-E4-014 | Submit the claim to the TCG portal | Split (rework) | Not started | RWB-S3-E4014-CON, RWB-S3-E4014-APP | Split into linked stories by service and team type. |
| RWB-E4-015 | Track the claim to payment | Split (rework) | Not started | RWB-S3-E4015-CON, RWB-S3-E4015-APP | Split into linked stories by service and team type. |
| RWB-E4-016 | Record the subrogation position | Split (rework) | Not started | RWB-S3-E4016-CON, RWB-S3-E4016-APP | Split into linked stories by service and team type. |
| RWB-E4-017 | Notify guarantors and co-borrowers | Split (rework) | Not started | RWB-S3-E4017-CON, RWB-S3-E4017-APP | Split into linked stories by service and team type. |
| RWB-E4-018 | Negotiate with a guarantor | Split (rework) | Not started | RWB-S3-E4018-CON, RWB-S3-E4018-APP | Split into linked stories by service and team type. |
| RWB-E4-019 | Close the case when a guarantee clears the debt | Split (rework) | Not started | RWB-S3-E4019-CON, RWB-S3-E4019-APP | Split into linked stories by service and team type. |
| RWB-E4-020 | File an insurance claim on a collateral event | Split (rework) | Not started | RWB-S3-E4020-CON, RWB-S3-E4020-APP | Split into linked stories by service and team type. |
| RWB-E4-021 | Evict occupants from a held property | Split (rework) | Not started | RWB-S5-E4021-CON, RWB-S5-E4021-APP | Split into linked stories by service and team type. |
| RWB-E4-022 | Run the descending price schedule | Split (rework) | Not started | RWB-S5-E4022-CON, RWB-S5-E4022-APP | Split into linked stories by service and team type. |
| RWB-E4-023 | Allocate the asset to an auction vendor by distance | Split (rework) | Not started | RWB-S5-E4023-CON, RWB-S5-E4023-APP | Split into linked stories by service and team type. |
| RWB-E4-024 | Run auction rounds and report bids | Split (rework) | Not started | RWB-S5-E4024-CON, RWB-S5-E4024-APP | Split into linked stories by service and team type. |
| RWB-E4-025 | Accept a bid below the floor with a second signature | Split (rework) | Not started | RWB-S5-E4025-CON, RWB-S5-E4025-APP | Split into linked stories by service and team type. |
| RWB-E4-026 | Re-list on no bid | Split (rework) | Not started | RWB-S5-E4026-CON, RWB-S5-E4026-APP | Split into linked stories by service and team type. |
| RWB-E4-027 | Enforce the five-day payment term | Split (rework) | Not started | RWB-S5-E4027-CON, RWB-S5-E4027-APP | Split into linked stories by service and team type. |
| RWB-E4-028 | Transfer vehicle registration | Split (rework) | Not started | RWB-S5-E4028-CON, RWB-S5-E4028-APP | Split into linked stories by service and team type. |
| RWB-E4-029 | Record a property transfer at the Land Office | Split (rework) | Not started | RWB-S5-E4029-CON, RWB-S5-E4029-APP | Split into linked stories by service and team type. |
| RWB-E4-030 | Apply proceeds and raise the shortfall | Split (rework) | Not started | RWB-S5-E4030-CON, RWB-S5-E4030-APP | Split into linked stories by service and team type. |
| RWB-E4-031 | Transfer a pool to RAMC or the joint venture | Split (rework) | Not started | RWB-S5-E4031-CON, RWB-S5-E4031-APP | Split into linked stories by service and team type. |
| RWB-E4-032 | Arrange a customer buy-back | Split (rework) | Not started | RWB-S5-E4032-CON, RWB-S5-E4032-APP | Split into linked stories by service and team type. |
| RWB-E4-033 | Rent a held asset to a third party | Split (rework) | Not started | RWB-S5-E4033-CON, RWB-S5-E4033-APP | Split into linked stories by service and team type. |
| RWB-E4-034 | Sell through a broker | Split (rework) | Not started | RWB-S5-E4034-CON, RWB-S5-E4034-APP | Split into linked stories by service and team type. |
| RWB-E4-035 | View the offer on LINE and web | Split (rework) | Not started | RWB-P6-E4035-CON, RWB-P6-E4035-APP | Split into linked stories by service and team type. |
| RWB-E4-036 | Accept an offer in self-service | Split (rework) | Not started | RWB-P6-E4036-CON, RWB-P6-E4036-APP | Split into linked stories by service and team type. |
| RWB-E4-037 | Pay in self-service | Split (rework) | Not started | RWB-P6-E4037-CON, RWB-P6-E4037-APP | Split into linked stories by service and team type. |
| RWB-E4-038 | Raise a dispute in self-service | Split (rework) | Not started | RWB-P6-E4038-CON, RWB-P6-E4038-APP | Split into linked stories by service and team type. |
| RWB-E4-039 | Maintain the contact repository | Split (rework) | Not started | RWB-P6-E4039-CON, RWB-P6-E4039-APP | Split into linked stories by service and team type. |
| RWB-E4-040 | Record a custody movement of a document | Split (rework) | Not started | RWB-P6-E4040-CON, RWB-P6-E4040-APP | Split into linked stories by service and team type. |
| RWB-E4-041 | Answer a legal or audit document request | Split (rework) | Not started | RWB-P6-E4041-CON, RWB-P6-E4041-APP | Split into linked stories by service and team type. |
| RWB-E4-042 | Apply retention on case closure | Split (rework) | Not started | RWB-P6-E4042-CON, RWB-P6-E4042-APP | Split into linked stories by service and team type. |
| RWB-E4-043 | Match a settlement payment | Split (rework) | Not started | RWB-P8-E4043-CON, RWB-P8-E4043-APP | Split into linked stories by service and team type. |
| RWB-E4-044 | Match auction and enforcement proceeds | Split (rework) | Not started | RWB-P8-E4044-CON, RWB-P8-E4044-APP | Split into linked stories by service and team type. |
| RWB-E4-045 | Calculate fees and charges | Split (rework) | Not started | RWB-P8-E4045-APP, RWB-ITG-E4045-ITG | Split into linked stories by service and team type. |
| RWB-E4-046 | Post a settlement booking to ALS | Split (rework) | Not started | RWB-P8-E4046-APP, RWB-P2-E4046-APP, RWB-ITG-E4046-ITG | Split into linked stories by service and team type. |
| RWB-E4-047 | Post to the general ledger | Split (rework) | Not started | RWB-P8-E4047-APP, RWB-ITG-E4047-ITG | Split into linked stories by service and team type. |
| RWB-E4-048 | Run the deed in lieu rental auto-debit | Split (rework) | Not started | RWB-P8-E4048-CON, RWB-P8-E4048-APP | Split into linked stories by service and team type. |
| RWB-E4-049 | Apply proceeds to the case balance | Split (rework) | Not started | RWB-P8-E4049-CON, RWB-P8-E4049-APP | Split into linked stories by service and team type. |
| RWB-E4-050 | Reconcile money movements daily | Split (rework) | Not started | RWB-P8-E4050-APP, RWB-ITG-E4050-ITG | Split into linked stories by service and team type. |
| RWB-E5-001 | Issue demand and recall notices | Split (rework) | Not started | RWB-S4-E5001-CON, RWB-S4-E5001-APP | Split into linked stories by service and team type. |
| RWB-E5-002 | Record proof of delivery on a notice | Split (rework) | Not started | RWB-S4-E5002-CON, RWB-S4-E5002-APP, RWB-P6-E5002-APP, RWB-P3-E5002-APP, RWB-ITG-E5002-ITG | Split into linked stories by service and team type. |
| RWB-E5-003 | Run the notice period timer | Split (rework) | Not started | RWB-S4-E5003-CON, RWB-S4-E5003-APP | Split into linked stories by service and team type. |
| RWB-E5-004 | Assemble the litigation pack | Split (rework) | Not started | RWB-S4-E5004-CON, RWB-S4-E5004-APP | Split into linked stories by service and team type. |
| RWB-E5-005 | Check the pack against the defect list | Split (rework) | Not started | RWB-S4-E5005-CON, RWB-S4-E5005-APP | Split into linked stories by service and team type. |
| RWB-E5-006 | Recover a missing or lost document | Split (rework) | Not started | RWB-S4-E5006-CON, RWB-S4-E5006-APP | Split into linked stories by service and team type. |
| RWB-E5-007 | Verify the pack and approve filing | Split (rework) | Not started | RWB-S4-E5007-CON, RWB-S4-E5007-APP | Split into linked stories by service and team type. |
| RWB-E5-008 | Select the law firm from the panel | Split (rework) | Not started | RWB-S4-E5008-CON, RWB-S4-E5008-APP | Split into linked stories by service and team type. |
| RWB-E5-009 | Instruct the firm through the portal | Split (rework) | Not started | RWB-S4-E5009-CON, RWB-S4-E5009-APP, RWB-ITG-E5009-ITG | Split into linked stories by service and team type. |
| RWB-E5-010 | Record the court filing and receipt | Split (rework) | Not started | RWB-S4-E5010-CON, RWB-S4-E5010-APP | Split into linked stories by service and team type. |
| RWB-E5-011 | Track hearings, deadlines and fees | Split (rework) | Not started | RWB-S4-E5011-CON, RWB-S4-E5011-APP | Split into linked stories by service and team type. |
| RWB-E5-012 | Recommend the next litigation step | Split (rework) | Not started | RWB-S4-E5012-CON, RWB-S4-E5012-APP | Split into linked stories by service and team type. |
| RWB-E5-013 | Settle before judgment | Split (rework) | Not started | RWB-S4-E5013-CON, RWB-S4-E5013-APP | Split into linked stories by service and team type. |
| RWB-E5-014 | Decide and manage an appeal | Split (rework) | Not started | RWB-S4-E5014-CON, RWB-S4-E5014-APP | Split into linked stories by service and team type. |
| RWB-E5-015 | Pay court fees and legal expenses | Split (rework) | Not started | RWB-S4-E5015-CON, RWB-S4-E5015-APP | Split into linked stories by service and team type. |
| RWB-E5-016 | Record the judgment | Split (rework) | Not started | RWB-S4-E5016-CON, RWB-S4-E5016-APP | Split into linked stories by service and team type. |
| RWB-E5-017 | Trace assets for enforcement | Split (rework) | Not started | RWB-S4-E5017-CON, RWB-S4-E5017-APP | Split into linked stories by service and team type. |
| RWB-E5-018 | Apply for the writ and seizure | Split (rework) | Not started | RWB-S4-E5018-CON, RWB-S4-E5018-APP | Split into linked stories by service and team type. |
| RWB-E5-019 | Follow the LED auction ladder | Split (rework) | Not started | RWB-S4-E5019-CON, RWB-S4-E5019-APP | Split into linked stories by service and team type. |
| RWB-E5-020 | Record an enforcement deferral with its reason | Split (rework) | Not started | RWB-S4-E5020-CON, RWB-S4-E5020-APP | Split into linked stories by service and team type. |
| RWB-E5-021 | File a bankruptcy petition | Split (rework) | Not started | RWB-S4-E5021-CON, RWB-S4-E5021-APP | Split into linked stories by service and team type. |
| RWB-E5-022 | Match enforcement proceeds to the case | Split (rework) | Not started | RWB-S4-E5022-CON, RWB-S4-E5022-APP | Split into linked stories by service and team type. |
| RWB-E5-023 | Select eligible accounts for sale by rule | Split (rework) | Not started | RWB-S6-E5023-CON, RWB-S6-E5023-APP | Split into linked stories by service and team type. |
| RWB-E5-024 | Build the lots and estimate the price | Split (rework) | Not started | RWB-S6-E5024-CON, RWB-S6-E5024-APP | Split into linked stories by service and team type. |
| RWB-E5-025 | Prepare the masked data tape | Split (rework) | Not started | RWB-S6-E5025-APP | Split into linked stories by service and team type. |
| RWB-E5-026 | Open the buyer data room | Split (rework) | Not started | RWB-S6-E5026-CON, RWB-S6-E5026-APP | Split into linked stories by service and team type. |
| RWB-E6-001 | Approve lots, reserve and tiered terms | Split (rework) | Not started | RWB-S6-E6001-CON, RWB-S6-E6001-APP | Split into linked stories by service and team type. |
| RWB-E6-002 | Qualify a buyer against KYC and licensing | Split (rework) | Not started | RWB-S6-E6002-CON, RWB-S6-E6002-APP | Split into linked stories by service and team type. |
| RWB-E6-003 | Bar a buyer that fails qualification | Split (rework) | Not started | RWB-S6-E6003-CON, RWB-S6-E6003-APP | Split into linked stories by service and team type. |
| RWB-E6-004 | Take buyer bids | Split (rework) | Not started | RWB-S6-E6004-CON, RWB-S6-E6004-APP | Split into linked stories by service and team type. |
| RWB-E6-005 | Award the lot and test the price | Split (rework) | Not started | RWB-S6-E6005-CON, RWB-S6-E6005-APP | Split into linked stories by service and team type. |
| RWB-E6-006 | Generate the sale agreement and notices | Split (rework) | Not started | RWB-S6-E6006-CON, RWB-S6-E6006-APP | Split into linked stories by service and team type. |
| RWB-E6-007 | Transfer the data to the buyer | Split (rework) | Not started | RWB-S6-E6007-CON, RWB-S6-E6007-APP | Split into linked stories by service and team type. |
| RWB-E6-008 | Derecognize and post to the general ledger | Split (rework) | Not started | RWB-S6-E6008-CON, RWB-S6-E6008-APP, RWB-ITG-E6008-ITG | Split into linked stories by service and team type. |
| RWB-E6-009 | Handle a buyer put-back claim | Split (rework) | Not started | RWB-S6-E6009-CON, RWB-S6-E6009-APP | Split into linked stories by service and team type. |
| RWB-E6-010 | Close a case awarded in a sold lot | Split (rework) | Not started | RWB-S6-E6010-CON, RWB-S6-E6010-APP | Split into linked stories by service and team type. |
| RWB-E6-011 | Confirm buyer remittance | Split (rework) | Not started | RWB-S6-E6011-CON, RWB-S6-E6011-APP | Split into linked stories by service and team type. |
| RWB-E6-012 | Apply the debt sale cap | Split (rework) | Not started | RWB-S6-E6012-APP | Split into linked stories by service and team type. |
| RWB-E6-013 | Run the monthly eligibility scan on both tracks | Split (rework) | Not started | RWB-S7-E6013-CON, RWB-S7-E6013-APP | Split into linked stories by service and team type. |
| RWB-E6-014 | Apply the tax criteria | Split (rework) | Not started | RWB-S7-E6014-CON, RWB-S7-E6014-APP | Split into linked stories by service and team type. |
| RWB-E6-015 | Prepare the write-off pack | Split (rework) | Not started | RWB-S7-E6015-CON, RWB-S7-E6015-APP | Split into linked stories by service and team type. |
| RWB-E6-016 | Remove a case from the proposed population | Split (rework) | Not started | RWB-S7-E6016-CON, RWB-S7-E6016-APP | Split into linked stories by service and team type. |
| RWB-E6-017 | Route the population to the committee and schedule it | Split (rework) | Not started | RWB-S7-E6017-CON, RWB-S7-E6017-APP, RWB-P3-E6017-APP, RWB-ITG-E6017-ITG | Split into linked stories by service and team type. |
| RWB-E6-018 | Approve a write-off inside the limit | Split (rework) | Not started | RWB-S7-E6018-CON, RWB-S7-E6018-APP | Split into linked stories by service and team type. |
| RWB-E6-019 | Reject a write-off | Split (rework) | Not started | RWB-S7-E6019-CON, RWB-S7-E6019-APP | Split into linked stories by service and team type. |
| RWB-E6-020 | Defer a write-off | Split (rework) | Not started | RWB-S7-E6020-CON, RWB-S7-E6020-APP | Split into linked stories by service and team type. |
| RWB-E6-021 | Post an approved write-off | Split (rework) | Not started | RWB-S7-E6021-CON, RWB-S7-E6021-APP, RWB-ITG-E6021-ITG | Split into linked stories by service and team type. |
| RWB-E6-022 | Send provision inputs to Finance | Split (rework) | Not started | RWB-S7-E6022-CON, RWB-S7-E6022-APP | Split into linked stories by service and team type. |
| RWB-E6-023 | Reconcile the approved and posted populations | Split (rework) | Not started | RWB-S7-E6023-CON, RWB-S7-E6023-APP | Split into linked stories by service and team type. |
| RWB-E6-024 | Work the write-off exception loop | Split (rework) | Not started | RWB-S7-E6024-CON, RWB-S7-E6024-APP | Split into linked stories by service and team type. |
| RWB-E6-025 | Close the case after the retention period | Split (rework) | Not started | RWB-S7-E6025-CON, RWB-S7-E6025-APP, RWB-P3-E6025-APP, RWB-ITG-E6025-ITG | Split into linked stories by service and team type. |
| RWB-E6-026 | Change the eligibility or tax criteria | Split (rework) | Not started | RWB-S7-E6026-CON, RWB-S7-E6026-APP | Split into linked stories by service and team type. |
| RWB-E6-027 | Record a customer payment after charge-off | Split (rework) | Not started | RWB-S7-E6027-CON, RWB-S7-E6027-APP | Split into linked stories by service and team type. |
| RWB-E6-028 | Sell a post charge-off population | Split (rework) | Not started | RWB-S7-E6028-CON, RWB-S7-E6028-APP, RWB-P7-E6028-APP, RWB-ITG-E6028-ITG | Split into linked stories by service and team type. |
| RWB-E6-029 | Onboard a partner and set terms | Split (rework) | Not started | RWB-S9-E6029-CON, RWB-S9-E6029-APP, RWB-ITG-E6029-ITG | Split into linked stories by service and team type. |
| RWB-E6-030 | Hold the partner panel and fee schedule as data | Split (rework) | Not started | RWB-S9-E6030-CON, RWB-S9-E6030-APP, RWB-ITG-E6030-ITG | Split into linked stories by service and team type. |
| RWB-E6-031 | Allocate work by measured return | Split (rework) | Not started | RWB-S9-E6031-CON, RWB-S9-E6031-APP, RWB-ITG-E6031-ITG | Split into linked stories by service and team type. |
| RWB-E6-032 | Override an allocation with a reason | Split (rework) | Not started | RWB-S9-E6032-CON, RWB-S9-E6032-APP, RWB-ITG-E6032-ITG | Split into linked stories by service and team type. |
| RWB-E6-033 | Receive a partner result into the case | Split (rework) | Not started | RWB-S9-E6033-CON, RWB-S9-E6033-APP, RWB-ITG-E6033-ITG | Split into linked stories by service and team type. |
| RWB-E6-034 | Place a charged-off account with an agency | Split (rework) | Not started | RWB-S9-E6034-CON, RWB-S9-E6034-APP | Split into linked stories by service and team type. |
| RWB-E6-035 | Match a recovery and calculate the agency fee | Split (rework) | Not started | RWB-S9-E6035-CON, RWB-S9-E6035-APP | Split into linked stories by service and team type. |
| RWB-E6-036 | Produce provision inputs | Split (rework) | Not started | RWB-P8-E6036-APP | Split into linked stories by service and team type. |
| RWB-E6-037 | Track benefit realisation | Split (rework) | Not started | RWB-P9-E6037-CON, RWB-P9-E6037-APP | Split into linked stories by service and team type. |
| RWB-E7-001 | Run X1 dispute and complaint end to end | Split (rework) | Not started | RWB-S8-E7001-CON, RWB-S8-E7001-APP, RWB-ITG-E7001-ITG | Split into linked stories by service and team type. |
| RWB-E7-002 | Run X2 vulnerability and hardship end to end | Split (rework) | Not started | RWB-S8-E7002-CON, RWB-S8-E7002-APP, RWB-ITG-E7002-ITG | Split into linked stories by service and team type. |
| RWB-E7-003 | Run X3 deceased customer end to end | Split (rework) | Not started | RWB-S8-E7003-CON, RWB-S8-E7003-APP, RWB-ITG-E7003-ITG | Split into linked stories by service and team type. |
| RWB-E7-004 | Run X4 fraud end to end | Split (rework) | Not started | RWB-S8-E7004-CON, RWB-S8-E7004-APP, RWB-ITG-E7004-ITG | Split into linked stories by service and team type. |
| RWB-E7-005 | Run X5 bankruptcy and seizure end to end | Split (rework) | Not started | RWB-S8-E7005-CON, RWB-S8-E7005-APP, RWB-ITG-E7005-ITG | Split into linked stories by service and team type. |
| RWB-E7-006 | Run X6 lost contact and skip trace end to end | Split (rework) | Not started | RWB-S8-E7006-CON, RWB-S8-E7006-APP, RWB-ITG-E7006-ITG | Split into linked stories by service and team type. |
| RWB-E7-007 | Run X7 collateral event end to end | Split (rework) | Not started | RWB-S8-E7007-CON, RWB-S8-E7007-APP, RWB-ITG-E7007-ITG | Split into linked stories by service and team type. |
| RWB-E7-008 | Review an override | Split (rework) | Not started | RWB-S8-E7008-CON, RWB-S8-E7008-APP | Split into linked stories by service and team type. |
| RWB-E7-009 | Match a complaint to the preceding contact | Split (rework) | Not started | RWB-S8-E7009-CON, RWB-S8-E7009-APP | Split into linked stories by service and team type. |
| RWB-E7-010 | Handle a contact sent while a block is on | Split (rework) | Not started | RWB-S8-E7010-CON, RWB-S8-E7010-APP | Split into linked stories by service and team type. |
| RWB-E7-011 | Score partners monthly | Split (rework) | Not started | RWB-S9-E7011-CON, RWB-S9-E7011-APP | Split into linked stories by service and team type. |
| RWB-E7-012 | Approve partner fees | Split (rework) | Not started | RWB-S9-E7012-CON, RWB-S9-E7012-APP, RWB-ITG-E7012-ITG | Split into linked stories by service and team type. |
| RWB-E7-013 | Hold a partner review | Split (rework) | Not started | RWB-S9-E7013-CON, RWB-S9-E7013-APP, RWB-ITG-E7013-ITG | Split into linked stories by service and team type. |
| RWB-E7-014 | Issue a notice on a missed target | Split (rework) | Not started | RWB-S9-E7014-CON, RWB-S9-E7014-APP, RWB-ITG-E7014-ITG | Split into linked stories by service and team type. |
| RWB-E7-015 | End a partner contract and recall the work | Split (rework) | Not started | RWB-S9-E7015-CON, RWB-S9-E7015-APP, RWB-ITG-E7015-ITG | Split into linked stories by service and team type. |
| RWB-E7-016 | Check partner conduct | Split (rework) | Not started | RWB-S9-E7016-CON, RWB-S9-E7016-APP, RWB-ITG-E7016-ITG | Split into linked stories by service and team type. |
| RWB-E7-017 | Manage extra costs and services on an asset | Split (rework) | Not started | RWB-S9-E7017-CON, RWB-S9-E7017-APP, RWB-ITG-E7017-ITG | Split into linked stories by service and team type. |
| RWB-E7-018 | Capture field work through the field app | Split (rework) | Not started | RWB-S9-E7018-CON, RWB-S9-E7018-APP | Split into linked stories by service and team type. |
| RWB-E8-001 | Produce regulatory returns | Split (rework) | Not started | RWB-P9-E8001-CON, RWB-P9-E8001-APP | Split into linked stories by service and team type. |
| RWB-E8-002 | Classify, stage and re-age an account | Split (rework) | Not started | RWB-P9-E8002-CON, RWB-P9-E8002-APP | Split into linked stories by service and team type. |
| RWB-E8-003 | Run a champion and challenger test | Split (rework) | Not started | RWB-P10-E8003-APP | Split into linked stories by service and team type. |
| RWB-E8-004 | Raise or lower an autonomy level with approval | Split (rework) | Not started | RWB-P10-E8004-CON, RWB-P10-E8004-APP | Split into linked stories by service and team type. |
| RWB-E8-005 | Review agent risk at the committee | Split (rework) | Not started | RWB-P10-E8005-CON, RWB-P10-E8005-APP | Split into linked stories by service and team type. |
| RWB-E8-006 | Run the full administration screens | Split (rework) | Not started | RWB-P4-E8006-CON, RWB-P4-E8006-APP | Split into linked stories by service and team type. |
| RWB-E8-007 | Change a decision rule through the administration screens | Split (rework) | Not started | RWB-P4-E8007-CON, RWB-P4-E8007-APP | Split into linked stories by service and team type. |
| RWB-E8-008 | Move an approval limit | Split (rework) | Not started | RWB-P4-E8008-CON, RWB-P4-E8008-APP | Split into linked stories by service and team type. |
| RWB-E8-009 | Set the treatment policy by product | Split (rework) | Not started | RWB-P4-E8009-CON, RWB-P4-E8009-APP | Split into linked stories by service and team type. |
| RWB-E8-010 | Add a letter template with Compliance approval | Split (rework) | Not started | RWB-P4-E8010-CON, RWB-P4-E8010-APP | Split into linked stories by service and team type. |
| RWB-E8-011 | Roll back a configuration version | Split (rework) | Not started | RWB-P4-E8011-CON, RWB-P4-E8011-APP | Split into linked stories by service and team type. |
| RWB-E8-012 | Publish a panel change | Split (rework) | Not started | RWB-P4-E8012-CON, RWB-P4-E8012-APP, RWB-ITG-E8012-ITG | Split into linked stories by service and team type. |
| RWB-E8-013 | Run a QA sample against the rule version applied | Split (rework) | Not started | RWB-P4-E8013-CON, RWB-P4-E8013-APP | Split into linked stories by service and team type. |
| RWB-E8-014 | Return a defective pack | Split (rework) | Not started | RWB-P4-E8014-CON, RWB-P4-E8014-APP | Split into linked stories by service and team type. |
| RWB-E8-015 | Detect a broken hash chain in the decision log | Split (rework) | Not started | RWB-P4-E8015-CON, RWB-P4-E8015-APP | Split into linked stories by service and team type. |
| RWB-E8-016 | Handle a data subject request | Split (rework) | Not started | RWB-P4-E8016-CON, RWB-P4-E8016-APP | Split into linked stories by service and team type. |
| RWB-E8-017 | Manage an incident | Split (rework) | Not started | RWB-P4-E8017-CON, RWB-P4-E8017-APP | Split into linked stories by service and team type. |
| RWB-E8-018 | Refer a case to Aric | Split (rework) | Not started | RWB-P4-E8018-CON, RWB-P4-E8018-APP | Split into linked stories by service and team type. |
| RWB-E8-019 | Control access by role and by agent | Split (rework) | Not started | RWB-P4-E8019-CON, RWB-P4-E8019-APP | Split into linked stories by service and team type. |
| RWB-TE-001 | Recovery module folder and boundary test | Preserved + delta | Built | RWB-PLT-TE001-APP, RWB-PLT-TE001-APP-2 | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-TE-002 | Code owners for the recovery module | Preserved + delta | Built | RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-TE-003 | Types and contract tests from the API specification | Preserved + delta | In build | RWB-PLT-TE003-APP, RWB-PLT-TE003-APP-2 | Built or in build. As-built story kept word for word; the microservice change is a separate delta story. |
| RWB-TE-004 | Masked data in SIT and UAT | Split (rework) | Not started | RWB-PLT-TE004-APP, RWB-ITG-TE004-ITG | Split into linked stories by service and team type. |
| RWB-TE-006 | Outbox and retry for outbound work | Split (rework) | Not started | RWB-PLT-TE006-CON, RWB-PLT-TE006-APP, RWB-ITG-TE006-ITG | Split into linked stories by service and team type. |
| RWB-TE-007 | Scheduled jobs on Quartz | Retired (D-RCV-60) | Built | None | Quartz scheduler. Retired by Arch v5; Temporal Schedules through the workflow kit replace it (RWB-PLT-E1071-CON, ADR-016). |
| RWB-TE-008 | Decision log hash chain check | Split (rework) | Not started | RWB-PLT-TE008-APP, RWB-ITG-TE008-ITG | Split into linked stories by service and team type. |
| RWB-TE-009 | Performance test harness | Split (rework) | Not started | RWB-ITG-TE009-ITG | Split into linked stories by service and team type. |
| RWB-TE-010 | Browser and accessibility tests | Moved (no impact) | Not started | RWB-ITG-TE010-ITG | Moved to its service epic; content unchanged. |
| RWB-TE-011 | PDPA lint for code, tests and logs | Split (rework) | Not started | RWB-PLT-TE011-APP | Split into linked stories by service and team type. |
| RWB-TE-012 | Document storage containers | Moved (no impact) | Not started | RWB-PLT-TE012-APP | Moved to its service epic; content unchanged. |
| RWB-TE-013 | Agent runtime client with fallback | Split (rework) | Not started | RWB-P10-TE013-CON, RWB-P10-TE013-APP, RWB-P7-TE013-APP, RWB-P10-TE013-OPS, RWB-ITG-TE013-ITG | Split into linked stories by service and team type. |
| W1J01 | Contract-test harness and synthetic test data | New | Not started | RWB-ITG-W1J01-ITG | New story created by the realignment. |
| W1J02 | Wave 1 v5 journey end to end | New | Not started | RWB-ITG-W1J02-ITG | New story created by the realignment. |
| W2J01 | Wave 2 journey end to end | New | Not started | RWB-ITG-W2J01-ITG | New story created by the realignment. |
| W3J01 | Wave 3 journey end to end | New | Not started | RWB-ITG-W3J01-ITG | New story created by the realignment. |
| W4J01 | Wave 4 journey end to end | New | Not started | RWB-ITG-W4J01-ITG | New story created by the realignment. |
