# TB0001-1357 [RWB-E1-001] BE - Migration, seeds and dictionary conformance (TASK-02..06, 12)

| Field | Value |
|---|---|
| Jira | [TB0001-1357](https://scbjira.atlassian.net/browse/TB0001-1357) |
| Type | Sub-task |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1163 |
| Epic link | - |
| Assignee | - |
| Reporter | PREMMAST SUWANNIKOM |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad1 |
| Team | RWB_SQ1 |
| Created | 2026-11-11T16:11:04.142+0700 |
| Updated | 2026-11-18T09:17:03.255+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

h2. Scope

Implementation Builder work for RWB-E1-001, parent [TB0001-1163|https://scbjira.atlassian.net/browse/TB0001-1163]. This sub-task carries TASK-RWB-E1-001-02, -03, -04, -05, -06 and -12 of the approved plan.

Canonical plan: {{output/INC-010-epic-1-RWB-E1-001/plan/plan.md}}, {{tasks.md}} and {{data-model.md}}.

h2. Readiness — NOT READY

Blocked by *PRE-6*: RWB-E1-044 is not implemented. {{output/INC-001-epic-1-RWB-E1-044/}} holds {{specify/}}, {{plan/}} and {{review/}} only — there is no {{implement/}} run. Without it there is no recovery Flyway bean, no {{flyway_schema_history_recovery}}, no {{db/modulemigration/recovery/}} folder and no migration lint to run against.

Linked: _is blocked by_ [TB0001-1205|https://scbjira.atlassian.net/browse/TB0001-1205].

Do not stub the Flyway bean or the history table to start early.

h2. Tasks

||Task||Work||
|TASK-02|Generate the migration: run the transformation in {{data-model.md}} §1 over {{recovery-workbench-physical-schema-v4.sql}}, producing {{db/modulemigration/recovery/V<seq>__rwb_e1_001_recovery_schema.sql}} with line 1 exactly {{-- Story: RWB-E1-001}}. All 16 deltas of §3 applied; the counts of §2 present. {{<seq>}} is planned {{0003}} (D-RCV-34) but taken at merge as the next free number (D-RCV-28), with the merge-order map updated in the same MR. The transformation script lives in test support, not production code.|
|TASK-03|Verify the generated file against the source by parsing both: 44 {{CREATE TABLE}}, 841 columns, 21 {{rwb_uq_*}} constraints across 19 tables with three on {{rwb_decision_log_entry}}, 68 foreign keys with {{fk_notice_dispatch_file_id}} absent, 76 {{rwb_ix_*}} indexes, 1 function, 2 triggers, 1 view; no surviving {{CREATE SCHEMA}}, {{SET search_path}}, {{CREATE EXTENSION}} or {{COMMENT ON}}; {{rwb_sys_objects.data_product}} nullable; the {{DF-REF-091}} seed row at {{is_mandatory = false}} (delta 14); no {{delegation_limit}} insert.|
|TASK-04|Seed verification: 14 {{rwb_data_product}} before 108 {{rwb_sys_objects}} (75 carrying DP01–DP14, 33 NULL with {{OPS}}/{{AGT}}/{{RPT}}), then 1,256 {{rwb_sys_fields}}, 598 {{rwb_lov_value}}, 54 {{rwb_role}}, 421 {{rwb_permission}}, and *0* {{rwb_delegation_limit}}. Assert each of the 421 permission rows resolved a {{role_code}}.|
|TASK-05|Run the RWB-E1-044 {{RecoveryMigrationLintTest}} over the generated file, including the {{rwb_}} prefix on all 21 named {{UNIQUE}} constraints. Add a negative fixture leaving one {{uq_*}} unprefixed. The 68 {{fk_*}} and two {{trg_*}} names must not fail (D-RCV-55).|
|TASK-06|{{DataDictionaryConformanceTest}}, {{@Tag("recovery-it")}}, Testcontainers PostgreSQL: compare {{information_schema.tables}} rows with {{table_type = 'BASE TABLE'}} named {{rwb_*}} against {{rwb_sys_fields}}, both ways. The {{BASE TABLE}} filter is required or the view is compared against itself. A {{sys_fields}} row whose object does not yet exist is not a failure (D-RCV-29). After this story it compares 533 columns.|
|TASK-12|Migration integration tests ({{recoveryIntegrationTest}}, {{@Tag("recovery-it")}}): TC-E1-001-01, -02, -04, -06, -16, -17.|

h2. Delta 14 — a judgement call the Builder may be asked to reverse

D-RCV-51 made {{sys_objects.data_product}} nullable, but the {{sys_fields}} seed row describing it, {{DF-REF-091}}, still ships {{is_mandatory = true}}, and D-RCV-57 closed the Physical Schema v5 reissue that would have corrected it. The conformance test compares name and physical type, not nullability, so nothing catches it. The migration therefore sets that row to {{false}}, recorded as derived from D-RCV-51 with BR1 rather than as a new decision. {{plan.md}} §Risks states that FDA or BA may overrule and leave the seed untouched. OPEN-034 carries it.

h2. Why the migration is generated rather than pasted

44 tables and 841 columns out of a 6,652-line source. A pasted DDL block would be checked against nothing and could not be re-derived if the schema is reissued. RWB-E1-043 carries literal DDL because its migration is two tables.

h2. Branch policy

D-RCV-50 as on the parent story. Never run against a shared database; ACE {{application.yaml}} has Flyway {{clean-disabled: false}}.

## Linked issues

- is blocked by TB0001-1205: [RWB-E1-044] Database migrations versioned with parameterized schema names (Hold)

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-11 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
