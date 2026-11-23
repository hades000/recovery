# Recovery Workbench Jira Impact and Follow-up v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

## R2. Jira impact (for the separate follow-up file only)

This run makes no Jira change and reads nothing from Jira. A person with Jira access applies the follow-ups below later. The epic and story IDs are the new IDs in the Service Story Catalog v1.

| Legacy disposition | Follow-up in Jira |
|---|---|
| Retired (D-RCV-60) | Close the issue as won't do, with resolution note "Retired by D-RCV-60". Do not delete it. |
| Already retired | No change. |
| Preserved + delta | Keep the issue, its status, sprint and history. Create the delta and contract issues and link them with "relates to". |
| Must change (RWB-E1-001) | Keep the issue and its status. Add a comment with the Change Register row. Create the linked DB split issues. |
| Moved (no impact) | Keep the issue. Change its epic link to the new service epic. Add the business-epic label. |
| Split (rework) | Keep the issue as the main APP story in the service epic. Create the linked CON, DB, INF, OPS and ITG issues. |
| New | Create the issue in its epic, with the suggested-owner text as a label, not as an assignee. |

Create the 31 epics first: 7 PLT, 19 SVC and 5 ITG. Then create stories in this order: CON, then DB, INF and OPS, then APP, then ITG. Each story's dependency links come from the "Dependencies" sheet of the catalogue.


## Scale

- Epics to create: 31 (7 platform, 19 service, 5 integration).
- Issues to create: 695. Issues to close: 2.

| Disposition | Legacy issues |
|---|---|
| Moved (no impact) | 24 |
| Must change | 1 |
| New | 17 |
| Preserved + delta | 6 |
| Retired (D-RCV-60) | 2 |
| Split (rework) | 308 |

## Epics

| Epic | Stories |
|---|---|
| RWB-ITG-NFR | 2 |
| RWB-ITG-W1 | 52 |
| RWB-ITG-W2 | 43 |
| RWB-ITG-W3 | 9 |
| RWB-ITG-W4 | 41 |
| RWB-PLT-DB | 2 |
| RWB-PLT-EDGE | 5 |
| RWB-PLT-EVT | 3 |
| RWB-PLT-LIB | 18 |
| RWB-PLT-OBS | 2 |
| RWB-PLT-TPL | 19 |
| RWB-PLT-WF | 16 |
| RWB-SVC-P1 | 62 |
| RWB-SVC-P10 | 40 |
| RWB-SVC-P2 | 27 |
| RWB-SVC-P3 | 84 |
| RWB-SVC-P4 | 111 |
| RWB-SVC-P5 | 52 |
| RWB-SVC-P6 | 48 |
| RWB-SVC-P7 | 52 |
| RWB-SVC-P8 | 21 |
| RWB-SVC-P9 | 12 |
| RWB-SVC-S1 | 24 |
| RWB-SVC-S2 | 47 |
| RWB-SVC-S3 | 17 |
| RWB-SVC-S4 | 45 |
| RWB-SVC-S5 | 51 |
| RWB-SVC-S6 | 30 |
| RWB-SVC-S7 | 32 |
| RWB-SVC-S8 | 31 |
| RWB-SVC-S9 | 36 |

## Per legacy issue

| Legacy key | Disposition | Follow-up action | New issues | New story IDs |
|---|---|---|---|---|
| N001 | New | Create the issue in its service, platform or integration epic | 2 | RWB-PLT-N001-CON, RWB-PLT-N001-APP |
| N002 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N002-INF |
| N003 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N003-INF |
| N004 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N004-OPS |
| N005 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N005-OPS |
| N006 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N006-INF |
| N007 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N007-INF |
| N008 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N008-INF |
| N009 | New | Create the issue in its service, platform or integration epic | 2 | RWB-PLT-N009-CON, RWB-PLT-N009-APP |
| N010 | New | Create the issue in its service, platform or integration epic | 2 | RWB-PLT-N010-CON, RWB-PLT-N010-APP |
| N011 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N011-DB |
| N012 | New | Create the issue in its service, platform or integration epic | 1 | RWB-PLT-N012-INF |
| NF-01 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF01-OPS |
| NF-02 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF02-APP |
| NF-03 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF03-OPS |
| NF-04 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF04-OPS |
| NF-05 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF05-OPS |
| NF-06 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF06-DB |
| NF-07 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF07-INF |
| NF-08 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-NF08-INF |
| RWB-ACE-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P1-ACE001-DB |
| RWB-AD-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD001-CON, RWB-P4-AD001-APP |
| RWB-AD-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD002-CON, RWB-P4-AD002-APP |
| RWB-AD-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD003-CON, RWB-P4-AD003-APP |
| RWB-AD-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD004-CON, RWB-P4-AD004-APP |
| RWB-AD-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD005-CON, RWB-P4-AD005-APP |
| RWB-AD-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P4-AD006-CON, RWB-P4-AD006-APP, RWB-P4-AD006-DB |
| RWB-AD-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD007-CON, RWB-P4-AD007-APP |
| RWB-AD-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD008-CON, RWB-P4-AD008-APP |
| RWB-AD-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD009-CON, RWB-P4-AD009-APP |
| RWB-AD-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD010-CON, RWB-P4-AD010-APP |
| RWB-AD-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD011-CON, RWB-P4-AD011-APP |
| RWB-AD-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD012-CON, RWB-P4-AD012-APP |
| RWB-AD-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD013-CON, RWB-P4-AD013-APP |
| RWB-AD-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P4-AD014-CON, RWB-P4-AD014-APP, RWB-ITG-AD014-ITG |
| RWB-AD-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P4-AD015-CON, RWB-P4-AD015-APP, RWB-ITG-AD015-ITG |
| RWB-AD-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-AD016-CON, RWB-P4-AD016-APP |
| RWB-AD-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-AD017-CON, RWB-P6-AD017-APP |
| RWB-AD-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P1-AD018-CON, RWB-P1-AD018-APP, RWB-P1-AD018-OPS, RWB-ITG-AD018-ITG |
| RWB-AD-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P1-AD019-APP, RWB-P3-AD019-APP, RWB-P1-AD019-OPS, RWB-ITG-AD019-ITG |
| RWB-AD-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P10-AD020-CON, RWB-P10-AD020-APP |
| RWB-AD-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P5-AD021-CON, RWB-P5-AD021-APP |
| RWB-AD-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-AD022-CON, RWB-S9-AD022-APP, RWB-ITG-AD022-ITG |
| RWB-DM-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P1-DM001-APP |
| RWB-DM-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P1-DM002-APP |
| RWB-DM-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM003-APP, RWB-ITG-DM003-ITG |
| RWB-DM-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM004-APP, RWB-ITG-DM004-ITG |
| RWB-DM-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM005-APP, RWB-ITG-DM005-ITG |
| RWB-DM-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM006-APP, RWB-ITG-DM006-ITG |
| RWB-DM-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM007-APP, RWB-ITG-DM007-ITG |
| RWB-DM-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM008-APP, RWB-ITG-DM008-ITG |
| RWB-DM-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM009-APP, RWB-ITG-DM009-ITG |
| RWB-DM-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM010-APP, RWB-ITG-DM010-ITG |
| RWB-DM-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM011-APP, RWB-ITG-DM011-ITG |
| RWB-DM-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P1-DM012-APP, RWB-ITG-DM012-ITG |
| RWB-DM-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P1-DM013-APP, RWB-P8-DM013-APP, RWB-ITG-DM013-ITG |
| RWB-DM-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P1-DM014-APP |
| RWB-E1-001 | Must change | Keep the issue and its status; link the new delta and contract issues | 4 | RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP, RWB-P8-E1001-APP, RWB-ITG-E1001-ITG |
| RWB-E1-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P1-E1002-APP, RWB-P3-E1002-APP, RWB-P1-E1002-OPS, RWB-ITG-E1002-ITG, RWB-P1-E1002-CON |
| RWB-E1-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 8 | RWB-P2-E1007-CON, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P6-E1007-APP, RWB-P5-E1007-APP, RWB-P4-E1007-APP, RWB-P2-E1007-INF, RWB-P2-E1007-OPS, RWB-ITG-E1007-ITG |
| RWB-E1-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P7-E1008-CON, RWB-P7-E1008-APP, RWB-P4-E1008-APP, RWB-P7-E1008-DB, RWB-P7-E1008-OPS, RWB-ITG-E1008-ITG |
| RWB-E1-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P1-E1011-APP, RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P6-E1011-APP, RWB-P1-E1011-OPS, RWB-ITG-E1011-ITG, RWB-P1-E1011-CON |
| RWB-E1-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P9-E1013-CON, RWB-P9-E1013-APP, RWB-P3-E1013-APP, RWB-P1-E1013-APP, RWB-P9-E1013-OPS, RWB-ITG-E1013-ITG |
| RWB-E1-014 | Retired (D-RCV-60) | Close the issue as won't do (retired by D-RCV-60); no new issues | 0 |  |
| RWB-E1-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P1-E1015-CON, RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-ITG-E1015-ITG |
| RWB-E1-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P1-E1016-APP, RWB-P4-E1016-APP, RWB-P5-E1016-APP, RWB-P1-E1016-DB, RWB-ITG-E1016-ITG, RWB-P1-E1016-CON |
| RWB-E1-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P1-E1017-CON, RWB-P1-E1017-APP, RWB-P5-E1017-APP, RWB-P7-E1017-APP, RWB-P1-E1017-OPS, RWB-ITG-E1017-ITG |
| RWB-E1-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P3-E1018-CON, RWB-P3-E1018-APP, RWB-P5-E1018-APP, RWB-P1-E1018-APP, RWB-P4-E1018-APP, RWB-P7-E1018-APP, RWB-P3-E1018-OPS, RWB-ITG-E1018-ITG |
| RWB-E1-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P3-E1019-CON, RWB-P3-E1019-APP, RWB-P4-E1019-APP, RWB-P6-E1019-APP, RWB-P3-E1019-DB, RWB-ITG-E1019-ITG |
| RWB-E1-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P3-E1020-CON, RWB-P3-E1020-APP, RWB-P4-E1020-APP, RWB-P7-E1020-APP, RWB-S8-E1020-APP, RWB-P3-E1020-OPS, RWB-ITG-E1020-ITG |
| RWB-E1-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P3-E1021-CON, RWB-P3-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP, RWB-P5-E1021-APP, RWB-P4-E1021-APP, RWB-P3-E1021-OPS, RWB-ITG-E1021-ITG |
| RWB-E1-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P4-E1022-CON, RWB-P4-E1022-APP, RWB-P4-E1022-DB, RWB-ITG-E1022-ITG |
| RWB-E1-023 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P3-E1023-CON, RWB-P3-E1023-APP, RWB-P4-E1023-APP, RWB-S8-E1023-APP, RWB-ITG-E1023-ITG |
| RWB-E1-024 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P5-E1024-APP, RWB-ITG-E1024-ITG |
| RWB-E1-025 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P5-E1025-APP, RWB-ITG-E1025-ITG |
| RWB-E1-026 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P5-E1026-APP, RWB-ITG-E1026-ITG |
| RWB-E1-027 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-PLT-E1027-CON, RWB-PLT-E1027-APP, RWB-P7-E1027-CON, RWB-P7-E1027-APP, RWB-ITG-E1027-ITG |
| RWB-E1-028 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P3-E1028-CON, RWB-P3-E1028-APP, RWB-P4-E1028-APP, RWB-P7-E1028-APP, RWB-P3-E1028-OPS, RWB-ITG-E1028-ITG |
| RWB-E1-030 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P3-E1030-CON, RWB-P3-E1030-APP, RWB-P7-E1030-APP, RWB-P3-E1030-OPS, RWB-ITG-E1030-ITG |
| RWB-E1-031 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P3-E1031-CON, RWB-P3-E1031-APP, RWB-ITG-E1031-ITG |
| RWB-E1-032 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 8 | RWB-P5-E1032-CON, RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-P7-E1032-APP, RWB-P5-E1032-INF, RWB-P5-E1032-OPS, RWB-ITG-E1032-ITG |
| RWB-E1-033 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-P5-E1033-APP |
| RWB-E1-034 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P6-E1034-APP, RWB-ITG-E1034-ITG |
| RWB-E1-035 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P3-E1035-CON, RWB-P3-E1035-APP |
| RWB-E1-037 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-PLT-E1037-CON, RWB-PLT-E1037-APP, RWB-P4-E1037-CON, RWB-P4-E1037-APP, RWB-ITG-E1037-ITG |
| RWB-E1-038 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-P4-E1038-APP |
| RWB-E1-039 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P4-E1039-CON, RWB-P4-E1039-APP, RWB-P5-E1039-APP, RWB-P7-E1039-APP, RWB-P4-E1039-DB, RWB-P4-E1039-OPS, RWB-ITG-E1039-ITG |
| RWB-E1-040 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-P5-E1040-APP |
| RWB-E1-041 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P5-E1041-APP, RWB-P5-E1041-CON |
| RWB-E1-042 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 4 | RWB-PLT-E1042-CON, RWB-PLT-E1042-APP, RWB-PLT-E1042-OPS, RWB-P3-E1042-APP, RWB-P3-E1042-CON |
| RWB-E1-043 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 3 | RWB-PLT-E1043-CON, RWB-PLT-E1043-APP, RWB-P3-E1043-APP, RWB-P3-E1043-CON |
| RWB-E1-044 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 3 | RWB-PLT-E1044-APP, RWB-PLT-E1044-CON, RWB-PLT-E1044-APP-2, RWB-PLT-E1044-OPS |
| RWB-E1-045 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-P3-E1045-APP |
| RWB-E1-046 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P6-E1046-CON, RWB-P6-E1046-APP, RWB-P7-E1046-APP, RWB-P5-E1046-APP, RWB-ITG-E1046-ITG |
| RWB-E1-047 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-PLT-E1047-CON, RWB-PLT-E1047-APP, RWB-ITG-E1047-ITG |
| RWB-E1-049 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P5-E1049-CON, RWB-P5-E1049-APP, RWB-P6-E1049-APP, RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-ITG-E1049-ITG |
| RWB-E1-050 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P5-E1050-APP, RWB-P3-E1050-APP, RWB-P5-E1050-OPS, RWB-ITG-E1050-ITG, RWB-P5-E1050-CON |
| RWB-E1-052 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P6-E1052-CON, RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP, RWB-P7-E1052-APP, RWB-ITG-E1052-ITG |
| RWB-E1-053 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P5-E1053-APP, RWB-P5-E1053-CON |
| RWB-E1-054 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P5-E1054-CON, RWB-P5-E1054-APP, RWB-P4-E1054-APP, RWB-P3-E1054-APP, RWB-P7-E1054-APP, RWB-ITG-E1054-ITG |
| RWB-E1-055 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P6-E1055-CON, RWB-P6-E1055-APP, RWB-P3-E1055-APP, RWB-P5-E1055-APP, RWB-P1-E1055-APP, RWB-P6-E1055-INF, RWB-P6-E1055-OPS, RWB-ITG-E1055-ITG |
| RWB-E1-056 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-PLT-E1056-OPS |
| RWB-E1-057 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P5-E1057-CON, RWB-P5-E1057-APP, RWB-S9-E1057-APP, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-ITG-E1057-ITG |
| RWB-E1-058 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P10-E1058-CON, RWB-P10-E1058-APP, RWB-P10-E1058-INF, RWB-P10-E1058-OPS, RWB-ITG-E1058-ITG |
| RWB-E1-059 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P10-E1059-CON, RWB-P10-E1059-APP, RWB-ITG-E1059-ITG |
| RWB-E1-060 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P10-E1060-APP, RWB-ITG-E1060-ITG |
| RWB-E1-061 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P10-E1061-APP, RWB-P10-E1061-CON |
| RWB-E1-062 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P10-E1062-CON, RWB-P10-E1062-APP, RWB-S8-E1062-APP, RWB-P5-E1062-APP, RWB-P4-E1062-APP, RWB-ITG-E1062-ITG |
| RWB-E1-063 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P10-E1063-CON, RWB-P10-E1063-APP, RWB-P4-E1063-APP, RWB-P6-E1063-APP, RWB-P10-E1063-OPS, RWB-ITG-E1063-ITG |
| RWB-E1-064 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P1-E1064-CON, RWB-P1-E1064-APP, RWB-P4-E1064-APP, RWB-P1-E1064-OPS, RWB-ITG-E1064-ITG |
| RWB-E1-065 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P1-E1065-CON, RWB-P1-E1065-APP, RWB-P4-E1065-APP, RWB-P3-E1065-APP, RWB-S8-E1065-APP, RWB-P5-E1065-APP, RWB-P1-E1065-DB, RWB-ITG-E1065-ITG |
| RWB-E1-066 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P1-E1066-CON, RWB-P1-E1066-APP, RWB-P3-E1066-APP, RWB-P1-E1066-OPS, RWB-ITG-E1066-ITG |
| RWB-E1-067 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P1-E1067-CON, RWB-P1-E1067-APP, RWB-P3-E1067-APP, RWB-P5-E1067-APP, RWB-ITG-E1067-ITG |
| RWB-E1-068 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-P1-E1068-APP |
| RWB-E1-069 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P1-E1069-APP, RWB-P4-E1069-APP, RWB-P1-E1069-DB, RWB-ITG-E1069-ITG |
| RWB-E1-070 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-PLT-E1070-CON, RWB-PLT-E1070-APP, RWB-ITG-E1070-ITG |
| RWB-E1-071 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-E1071-CON, RWB-PLT-E1071-APP |
| RWB-E1-072 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-E1072-CON, RWB-PLT-E1072-APP |
| RWB-E1-073 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P3-E1073-CON, RWB-P3-E1073-APP, RWB-P7-E1073-APP, RWB-P6-E1073-APP, RWB-P2-E1073-APP, RWB-P3-E1073-INF, RWB-ITG-E1073-ITG |
| RWB-E2-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P2-E2001-CON, RWB-P2-E2001-APP, RWB-P1-E2001-APP, RWB-P3-E2001-APP, RWB-P7-E2001-APP, RWB-P2-E2001-OPS, RWB-ITG-E2001-ITG |
| RWB-E2-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P2-E2002-CON, RWB-P2-E2002-APP, RWB-P3-E2002-APP, RWB-P4-E2002-APP, RWB-P7-E2002-APP, RWB-P2-E2002-OPS, RWB-ITG-E2002-ITG |
| RWB-E2-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P2-E2003-APP, RWB-P4-E2003-APP, RWB-ITG-E2003-ITG |
| RWB-E2-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P3-E2004-CON, RWB-P3-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP, RWB-P4-E2004-APP, RWB-P3-E2004-OPS, RWB-ITG-E2004-ITG |
| RWB-E2-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P7-E2005-CON, RWB-P7-E2005-APP, RWB-ITG-E2005-ITG |
| RWB-E2-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P2-E2006-APP, RWB-P7-E2006-APP, RWB-S2-E2006-APP, RWB-P3-E2006-APP, RWB-ITG-E2006-ITG |
| RWB-E2-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 8 | RWB-P2-E2007-CON, RWB-P2-E2007-APP, RWB-P3-E2007-APP, RWB-P4-E2007-APP, RWB-S2-E2007-APP, RWB-P1-E2007-APP, RWB-P7-E2007-APP, RWB-P2-E2007-OPS, RWB-ITG-E2007-ITG |
| RWB-E2-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P8-E2008-CON, RWB-P8-E2008-APP, RWB-S2-E2008-APP, RWB-P1-E2008-APP, RWB-P7-E2008-APP, RWB-P4-E2008-APP, RWB-P8-E2008-OPS, RWB-ITG-E2008-ITG |
| RWB-E2-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P9-E2009-CON, RWB-P9-E2009-APP, RWB-P3-E2009-APP, RWB-S8-E2009-APP, RWB-P9-E2009-OPS, RWB-ITG-E2009-ITG |
| RWB-E2-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-P1-E2010-OPS, RWB-ITG-E2010-ITG |
| RWB-E2-011 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 1 | RWB-P3-E2011-CON, RWB-P3-E2011-APP |
| RWB-E2-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P3-E2012-CON, RWB-P3-E2012-APP, RWB-S8-E2012-APP, RWB-P7-E2012-APP, RWB-P3-E2012-OPS, RWB-ITG-E2012-ITG |
| RWB-E2-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P7-E2013-CON, RWB-P7-E2013-APP, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-OPS, RWB-ITG-E2013-ITG |
| RWB-E2-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P7-E2014-CON, RWB-P7-E2014-APP, RWB-P6-E2014-APP, RWB-P4-E2014-APP, RWB-P3-E2014-APP, RWB-P7-E2014-OPS, RWB-ITG-E2014-ITG |
| RWB-E2-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P3-E2015-CON, RWB-P3-E2015-APP, RWB-S8-E2015-APP, RWB-P4-E2015-APP, RWB-P3-E2015-OPS, RWB-ITG-E2015-ITG |
| RWB-E2-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P3-E2016-CON, RWB-P3-E2016-APP, RWB-P5-E2016-APP, RWB-ITG-E2016-ITG |
| RWB-E2-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P5-E2017-CON, RWB-P5-E2017-APP, RWB-S2-E2017-APP, RWB-P7-E2017-APP, RWB-P6-E2017-APP, RWB-P4-E2017-APP, RWB-ITG-E2017-ITG |
| RWB-E2-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-S2-E2018-APP, RWB-P6-E2018-OPS, RWB-ITG-E2018-ITG |
| RWB-E2-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P4-E2019-CON, RWB-P4-E2019-APP, RWB-S9-E2019-APP, RWB-P7-E2019-APP, RWB-P4-E2019-INF, RWB-ITG-E2019-ITG |
| RWB-E2-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P6-E2021-CON, RWB-P6-E2021-APP, RWB-P1-E2021-APP, RWB-P4-E2021-APP, RWB-P3-E2021-APP, RWB-P7-E2021-APP, RWB-P6-E2021-OPS, RWB-ITG-E2021-ITG |
| RWB-E2-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P6-E2022-CON, RWB-P6-E2022-APP, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P7-E2022-APP, RWB-P6-E2022-OPS, RWB-ITG-E2022-ITG |
| RWB-E2-024 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P5-E2024-CON, RWB-P5-E2024-APP, RWB-P4-E2024-APP, RWB-P3-E2024-APP, RWB-P7-E2024-APP, RWB-ITG-E2024-ITG |
| RWB-E2-025 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P5-E2025-CON, RWB-P5-E2025-APP, RWB-P7-E2025-APP, RWB-S4-E2025-APP, RWB-S2-E2025-APP, RWB-P5-E2025-OPS, RWB-ITG-E2025-ITG |
| RWB-E2-026 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P5-E2026-CON, RWB-P5-E2026-APP, RWB-P6-E2026-APP, RWB-S2-E2026-APP, RWB-P4-E2026-APP, RWB-P7-E2026-APP, RWB-ITG-E2026-ITG |
| RWB-E2-027 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P8-E2027-CON, RWB-P8-E2027-APP, RWB-P4-E2027-APP, RWB-S2-E2027-APP, RWB-P7-E2027-APP, RWB-P8-E2027-OPS, RWB-ITG-E2027-ITG |
| RWB-E2-028 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P10-E2028-CON, RWB-P10-E2028-APP, RWB-P7-E2028-APP, RWB-P10-E2028-OPS, RWB-ITG-E2028-ITG |
| RWB-E2-029 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P10-E2029-CON, RWB-P10-E2029-APP, RWB-S8-E2029-APP, RWB-P7-E2029-APP, RWB-ITG-E2029-ITG |
| RWB-E2-030 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-P10-E2030-CON, RWB-P10-E2030-APP, RWB-P5-E2030-APP, RWB-ITG-E2030-ITG |
| RWB-E2-031 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P10-E2031-CON, RWB-P10-E2031-APP, RWB-P4-E2031-APP, RWB-P10-E2031-OPS, RWB-ITG-E2031-ITG |
| RWB-E2-032 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P10-E2032-CON, RWB-P10-E2032-APP, RWB-S2-E2032-APP, RWB-P7-E2032-APP, RWB-P10-E2032-INF, RWB-ITG-E2032-ITG |
| RWB-E2-033 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 5 | RWB-P2-E2033-CON, RWB-P2-E2033-APP, RWB-P3-E2033-APP, RWB-P4-E2033-APP, RWB-S8-E2033-APP, RWB-ITG-E2033-ITG |
| RWB-E2-034 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P2-E2034-CON, RWB-P2-E2034-APP, RWB-S9-E2034-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P1-E2034-APP, RWB-P2-E2034-OPS, RWB-ITG-E2034-ITG |
| RWB-E2-035 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P2-E2035-CON, RWB-P2-E2035-APP, RWB-P4-E2035-APP, RWB-P3-E2035-APP, RWB-P7-E2035-APP, RWB-P2-E2035-OPS, RWB-ITG-E2035-ITG |
| RWB-E2-036 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 6 | RWB-P2-E2036-CON, RWB-P2-E2036-APP, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-S8-E2036-APP, RWB-P7-E2036-APP, RWB-ITG-E2036-ITG |
| RWB-E2-037 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-E2037-CON, RWB-PLT-E2037-APP |
| RWB-E2-038 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-PLT-E2038-CON, RWB-PLT-E2038-APP, RWB-ITG-E2038-ITG |
| RWB-E2-039 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-E2039-CON, RWB-PLT-E2039-APP |
| RWB-E2-040 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-E2040-CON, RWB-PLT-E2040-APP |
| RWB-E2-041 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P3-E2041-CON, RWB-P3-E2041-APP, RWB-P4-E2041-APP, RWB-P7-E2041-APP, RWB-ITG-E2041-ITG |
| RWB-E2-042 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 7 | RWB-P3-E2042-CON, RWB-P3-E2042-APP, RWB-P6-E2042-APP, RWB-P4-E2042-APP, RWB-P7-E2042-APP, RWB-P3-E2042-INF, RWB-P3-E2042-OPS, RWB-ITG-E2042-ITG |
| RWB-E2-043 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P3-E2043-CON, RWB-P3-E2043-APP, RWB-P7-E2043-APP, RWB-P3-E2043-OPS, RWB-ITG-E2043-ITG |
| RWB-E3-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3001-CON, RWB-S2-E3001-APP |
| RWB-E3-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3002-CON, RWB-S2-E3002-APP |
| RWB-E3-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3003-CON, RWB-S2-E3003-APP |
| RWB-E3-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3004-CON, RWB-S2-E3004-APP |
| RWB-E3-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3005-CON, RWB-S2-E3005-APP |
| RWB-E3-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S2-E3006-CON, RWB-S2-E3006-APP, RWB-ITG-E3006-ITG |
| RWB-E3-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3007-CON, RWB-S2-E3007-APP |
| RWB-E3-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3008-CON, RWB-S2-E3008-APP |
| RWB-E3-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3009-CON, RWB-S2-E3009-APP |
| RWB-E3-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S2-E3010-CON, RWB-S2-E3010-APP, RWB-ITG-E3010-ITG |
| RWB-E3-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3011-CON, RWB-S2-E3011-APP |
| RWB-E3-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3012-CON, RWB-S2-E3012-APP |
| RWB-E3-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-S2-E3013-CON, RWB-S2-E3013-APP, RWB-P3-E3013-APP, RWB-ITG-E3013-ITG |
| RWB-E3-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3014-CON, RWB-S2-E3014-APP |
| RWB-E3-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3015-CON, RWB-S2-E3015-APP |
| RWB-E3-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3016-CON, RWB-S2-E3016-APP |
| RWB-E3-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S2-E3017-CON, RWB-S2-E3017-APP, RWB-ITG-E3017-ITG |
| RWB-E3-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S2-E3018-CON, RWB-S2-E3018-APP |
| RWB-E3-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3019-CON, RWB-S5-E3019-APP |
| RWB-E3-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3020-CON, RWB-S5-E3020-APP |
| RWB-E3-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3021-CON, RWB-S5-E3021-APP |
| RWB-E3-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3022-CON, RWB-S5-E3022-APP |
| RWB-E3-023 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3023-CON, RWB-S5-E3023-APP |
| RWB-E3-024 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3024-CON, RWB-S5-E3024-APP |
| RWB-E3-025 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3025-CON, RWB-S5-E3025-APP |
| RWB-E3-026 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S5-E3026-CON, RWB-S5-E3026-APP, RWB-ITG-E3026-ITG |
| RWB-E3-027 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3027-CON, RWB-S5-E3027-APP |
| RWB-E3-028 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3028-CON, RWB-S5-E3028-APP |
| RWB-E3-029 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E3029-CON, RWB-S5-E3029-APP |
| RWB-E3-030 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P10-E3030-CON, RWB-P10-E3030-APP |
| RWB-E3-031 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P10-E3031-APP |
| RWB-E4-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S1-E4001-CON, RWB-S1-E4001-APP, RWB-ITG-E4001-ITG |
| RWB-E4-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S1-E4002-CON, RWB-S1-E4002-APP, RWB-ITG-E4002-ITG |
| RWB-E4-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4003-CON, RWB-S1-E4003-APP |
| RWB-E4-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4004-CON, RWB-S1-E4004-APP |
| RWB-E4-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4005-CON, RWB-S1-E4005-APP |
| RWB-E4-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4006-CON, RWB-S1-E4006-APP |
| RWB-E4-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4007-CON, RWB-S1-E4007-APP |
| RWB-E4-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4008-CON, RWB-S1-E4008-APP |
| RWB-E4-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4009-CON, RWB-S1-E4009-APP |
| RWB-E4-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4010-CON, RWB-S1-E4010-APP |
| RWB-E4-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4011-CON, RWB-S1-E4011-APP |
| RWB-E4-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S1-E4012-CON, RWB-S1-E4012-APP |
| RWB-E4-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4013-CON, RWB-S3-E4013-APP |
| RWB-E4-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4014-CON, RWB-S3-E4014-APP |
| RWB-E4-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4015-CON, RWB-S3-E4015-APP |
| RWB-E4-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4016-CON, RWB-S3-E4016-APP |
| RWB-E4-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4017-CON, RWB-S3-E4017-APP |
| RWB-E4-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4018-CON, RWB-S3-E4018-APP |
| RWB-E4-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4019-CON, RWB-S3-E4019-APP |
| RWB-E4-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S3-E4020-CON, RWB-S3-E4020-APP |
| RWB-E4-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4021-CON, RWB-S5-E4021-APP |
| RWB-E4-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4022-CON, RWB-S5-E4022-APP |
| RWB-E4-023 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4023-CON, RWB-S5-E4023-APP |
| RWB-E4-024 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4024-CON, RWB-S5-E4024-APP |
| RWB-E4-025 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4025-CON, RWB-S5-E4025-APP |
| RWB-E4-026 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4026-CON, RWB-S5-E4026-APP |
| RWB-E4-027 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4027-CON, RWB-S5-E4027-APP |
| RWB-E4-028 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4028-CON, RWB-S5-E4028-APP |
| RWB-E4-029 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4029-CON, RWB-S5-E4029-APP |
| RWB-E4-030 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4030-CON, RWB-S5-E4030-APP |
| RWB-E4-031 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4031-CON, RWB-S5-E4031-APP |
| RWB-E4-032 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4032-CON, RWB-S5-E4032-APP |
| RWB-E4-033 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4033-CON, RWB-S5-E4033-APP |
| RWB-E4-034 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S5-E4034-CON, RWB-S5-E4034-APP |
| RWB-E4-035 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4035-CON, RWB-P6-E4035-APP |
| RWB-E4-036 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4036-CON, RWB-P6-E4036-APP |
| RWB-E4-037 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4037-CON, RWB-P6-E4037-APP |
| RWB-E4-038 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4038-CON, RWB-P6-E4038-APP |
| RWB-E4-039 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4039-CON, RWB-P6-E4039-APP |
| RWB-E4-040 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4040-CON, RWB-P6-E4040-APP |
| RWB-E4-041 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4041-CON, RWB-P6-E4041-APP |
| RWB-E4-042 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P6-E4042-CON, RWB-P6-E4042-APP |
| RWB-E4-043 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4043-CON, RWB-P8-E4043-APP |
| RWB-E4-044 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4044-CON, RWB-P8-E4044-APP |
| RWB-E4-045 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4045-APP, RWB-ITG-E4045-ITG |
| RWB-E4-046 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P8-E4046-APP, RWB-P2-E4046-APP, RWB-ITG-E4046-ITG |
| RWB-E4-047 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4047-APP, RWB-ITG-E4047-ITG |
| RWB-E4-048 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4048-CON, RWB-P8-E4048-APP |
| RWB-E4-049 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4049-CON, RWB-P8-E4049-APP |
| RWB-E4-050 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P8-E4050-APP, RWB-ITG-E4050-ITG |
| RWB-E5-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5001-CON, RWB-S4-E5001-APP |
| RWB-E5-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-S4-E5002-CON, RWB-S4-E5002-APP, RWB-P6-E5002-APP, RWB-P3-E5002-APP, RWB-ITG-E5002-ITG |
| RWB-E5-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5003-CON, RWB-S4-E5003-APP |
| RWB-E5-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5004-CON, RWB-S4-E5004-APP |
| RWB-E5-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5005-CON, RWB-S4-E5005-APP |
| RWB-E5-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5006-CON, RWB-S4-E5006-APP |
| RWB-E5-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5007-CON, RWB-S4-E5007-APP |
| RWB-E5-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5008-CON, RWB-S4-E5008-APP |
| RWB-E5-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S4-E5009-CON, RWB-S4-E5009-APP, RWB-ITG-E5009-ITG |
| RWB-E5-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5010-CON, RWB-S4-E5010-APP |
| RWB-E5-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5011-CON, RWB-S4-E5011-APP |
| RWB-E5-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5012-CON, RWB-S4-E5012-APP |
| RWB-E5-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5013-CON, RWB-S4-E5013-APP |
| RWB-E5-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5014-CON, RWB-S4-E5014-APP |
| RWB-E5-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5015-CON, RWB-S4-E5015-APP |
| RWB-E5-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5016-CON, RWB-S4-E5016-APP |
| RWB-E5-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5017-CON, RWB-S4-E5017-APP |
| RWB-E5-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5018-CON, RWB-S4-E5018-APP |
| RWB-E5-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5019-CON, RWB-S4-E5019-APP |
| RWB-E5-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5020-CON, RWB-S4-E5020-APP |
| RWB-E5-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5021-CON, RWB-S4-E5021-APP |
| RWB-E5-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S4-E5022-CON, RWB-S4-E5022-APP |
| RWB-E5-023 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E5023-CON, RWB-S6-E5023-APP |
| RWB-E5-024 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E5024-CON, RWB-S6-E5024-APP |
| RWB-E5-025 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-S6-E5025-APP |
| RWB-E5-026 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E5026-CON, RWB-S6-E5026-APP |
| RWB-E6-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6001-CON, RWB-S6-E6001-APP |
| RWB-E6-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6002-CON, RWB-S6-E6002-APP |
| RWB-E6-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6003-CON, RWB-S6-E6003-APP |
| RWB-E6-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6004-CON, RWB-S6-E6004-APP |
| RWB-E6-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6005-CON, RWB-S6-E6005-APP |
| RWB-E6-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6006-CON, RWB-S6-E6006-APP |
| RWB-E6-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6007-CON, RWB-S6-E6007-APP |
| RWB-E6-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S6-E6008-CON, RWB-S6-E6008-APP, RWB-ITG-E6008-ITG |
| RWB-E6-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6009-CON, RWB-S6-E6009-APP |
| RWB-E6-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6010-CON, RWB-S6-E6010-APP |
| RWB-E6-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S6-E6011-CON, RWB-S6-E6011-APP |
| RWB-E6-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-S6-E6012-APP |
| RWB-E6-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6013-CON, RWB-S7-E6013-APP |
| RWB-E6-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6014-CON, RWB-S7-E6014-APP |
| RWB-E6-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6015-CON, RWB-S7-E6015-APP |
| RWB-E6-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6016-CON, RWB-S7-E6016-APP |
| RWB-E6-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-S7-E6017-CON, RWB-S7-E6017-APP, RWB-P3-E6017-APP, RWB-ITG-E6017-ITG |
| RWB-E6-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6018-CON, RWB-S7-E6018-APP |
| RWB-E6-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6019-CON, RWB-S7-E6019-APP |
| RWB-E6-020 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6020-CON, RWB-S7-E6020-APP |
| RWB-E6-021 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S7-E6021-CON, RWB-S7-E6021-APP, RWB-ITG-E6021-ITG |
| RWB-E6-022 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6022-CON, RWB-S7-E6022-APP |
| RWB-E6-023 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6023-CON, RWB-S7-E6023-APP |
| RWB-E6-024 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6024-CON, RWB-S7-E6024-APP |
| RWB-E6-025 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-S7-E6025-CON, RWB-S7-E6025-APP, RWB-P3-E6025-APP, RWB-ITG-E6025-ITG |
| RWB-E6-026 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6026-CON, RWB-S7-E6026-APP |
| RWB-E6-027 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S7-E6027-CON, RWB-S7-E6027-APP |
| RWB-E6-028 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 3 | RWB-S7-E6028-CON, RWB-S7-E6028-APP, RWB-P7-E6028-APP, RWB-ITG-E6028-ITG |
| RWB-E6-029 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E6029-CON, RWB-S9-E6029-APP, RWB-ITG-E6029-ITG |
| RWB-E6-030 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E6030-CON, RWB-S9-E6030-APP, RWB-ITG-E6030-ITG |
| RWB-E6-031 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E6031-CON, RWB-S9-E6031-APP, RWB-ITG-E6031-ITG |
| RWB-E6-032 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E6032-CON, RWB-S9-E6032-APP, RWB-ITG-E6032-ITG |
| RWB-E6-033 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E6033-CON, RWB-S9-E6033-APP, RWB-ITG-E6033-ITG |
| RWB-E6-034 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S9-E6034-CON, RWB-S9-E6034-APP |
| RWB-E6-035 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S9-E6035-CON, RWB-S9-E6035-APP |
| RWB-E6-036 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P8-E6036-APP |
| RWB-E6-037 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P9-E6037-CON, RWB-P9-E6037-APP |
| RWB-E7-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7001-CON, RWB-S8-E7001-APP, RWB-ITG-E7001-ITG |
| RWB-E7-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7002-CON, RWB-S8-E7002-APP, RWB-ITG-E7002-ITG |
| RWB-E7-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7003-CON, RWB-S8-E7003-APP, RWB-ITG-E7003-ITG |
| RWB-E7-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7004-CON, RWB-S8-E7004-APP, RWB-ITG-E7004-ITG |
| RWB-E7-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7005-CON, RWB-S8-E7005-APP, RWB-ITG-E7005-ITG |
| RWB-E7-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7006-CON, RWB-S8-E7006-APP, RWB-ITG-E7006-ITG |
| RWB-E7-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S8-E7007-CON, RWB-S8-E7007-APP, RWB-ITG-E7007-ITG |
| RWB-E7-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S8-E7008-CON, RWB-S8-E7008-APP |
| RWB-E7-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S8-E7009-CON, RWB-S8-E7009-APP |
| RWB-E7-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S8-E7010-CON, RWB-S8-E7010-APP |
| RWB-E7-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S9-E7011-CON, RWB-S9-E7011-APP |
| RWB-E7-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7012-CON, RWB-S9-E7012-APP, RWB-ITG-E7012-ITG |
| RWB-E7-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7013-CON, RWB-S9-E7013-APP, RWB-ITG-E7013-ITG |
| RWB-E7-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7014-CON, RWB-S9-E7014-APP, RWB-ITG-E7014-ITG |
| RWB-E7-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7015-CON, RWB-S9-E7015-APP, RWB-ITG-E7015-ITG |
| RWB-E7-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7016-CON, RWB-S9-E7016-APP, RWB-ITG-E7016-ITG |
| RWB-E7-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-S9-E7017-CON, RWB-S9-E7017-APP, RWB-ITG-E7017-ITG |
| RWB-E7-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-S9-E7018-CON, RWB-S9-E7018-APP |
| RWB-E8-001 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P9-E8001-CON, RWB-P9-E8001-APP |
| RWB-E8-002 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P9-E8002-CON, RWB-P9-E8002-APP |
| RWB-E8-003 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-P10-E8003-APP |
| RWB-E8-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P10-E8004-CON, RWB-P10-E8004-APP |
| RWB-E8-005 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P10-E8005-CON, RWB-P10-E8005-APP |
| RWB-E8-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8006-CON, RWB-P4-E8006-APP |
| RWB-E8-007 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8007-CON, RWB-P4-E8007-APP |
| RWB-E8-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8008-CON, RWB-P4-E8008-APP |
| RWB-E8-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8009-CON, RWB-P4-E8009-APP |
| RWB-E8-010 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8010-CON, RWB-P4-E8010-APP |
| RWB-E8-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8011-CON, RWB-P4-E8011-APP |
| RWB-E8-012 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-P4-E8012-CON, RWB-P4-E8012-APP, RWB-ITG-E8012-ITG |
| RWB-E8-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8013-CON, RWB-P4-E8013-APP |
| RWB-E8-014 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8014-CON, RWB-P4-E8014-APP |
| RWB-E8-015 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8015-CON, RWB-P4-E8015-APP |
| RWB-E8-016 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8016-CON, RWB-P4-E8016-APP |
| RWB-E8-017 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8017-CON, RWB-P4-E8017-APP |
| RWB-E8-018 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8018-CON, RWB-P4-E8018-APP |
| RWB-E8-019 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-P4-E8019-CON, RWB-P4-E8019-APP |
| RWB-TE-001 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 1 | RWB-PLT-TE001-APP, RWB-PLT-TE001-APP-2 |
| RWB-TE-002 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 1 | RWB-PLT-TE002-APP, RWB-PLT-TE002-OPS |
| RWB-TE-003 | Preserved + delta | Keep the issue and its status; link the new delta and contract issues | 1 | RWB-PLT-TE003-APP, RWB-PLT-TE003-APP-2 |
| RWB-TE-004 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-TE004-APP, RWB-ITG-TE004-ITG |
| RWB-TE-006 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 2 | RWB-PLT-TE006-CON, RWB-PLT-TE006-APP, RWB-ITG-TE006-ITG |
| RWB-TE-007 | Retired (D-RCV-60) | Close the issue as won't do (retired by D-RCV-60); no new issues | 0 |  |
| RWB-TE-008 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 1 | RWB-PLT-TE008-APP, RWB-ITG-TE008-ITG |
| RWB-TE-009 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-ITG-TE009-ITG |
| RWB-TE-010 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-ITG-TE010-ITG |
| RWB-TE-011 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 0 | RWB-PLT-TE011-APP |
| RWB-TE-012 | Moved (no impact) | Keep the issue; change its epic link to the service epic | 0 | RWB-PLT-TE012-APP |
| RWB-TE-013 | Split (rework) | Keep the issue as the main APP story; create the linked split issues; move it to the service epic | 4 | RWB-P10-TE013-CON, RWB-P10-TE013-APP, RWB-P7-TE013-APP, RWB-P10-TE013-OPS, RWB-ITG-TE013-ITG |
| W1J01 | New | Create the issue in its service, platform or integration epic | 1 | RWB-ITG-W1J01-ITG |
| W1J02 | New | Create the issue in its service, platform or integration epic | 1 | RWB-ITG-W1J02-ITG |
| W2J01 | New | Create the issue in its service, platform or integration epic | 1 | RWB-ITG-W2J01-ITG |
| W3J01 | New | Create the issue in its service, platform or integration epic | 1 | RWB-ITG-W3J01-ITG |
| W4J01 | New | Create the issue in its service, platform or integration epic | 1 | RWB-ITG-W4J01-ITG |
