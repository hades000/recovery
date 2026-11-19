# TB0001-1319 [RWB-TE-003] TASK-018 Contract harness and RecoveryContractTest

| Field | Value |
|---|---|
| Jira | [TB0001-1319](https://scbjira.atlassian.net/browse/TB0001-1319) |
| Type | Sub-task |
| Status | Review |
| Resolution | - |
| Parent | TB0001-1237 |
| Epic link | - |
| Assignee | - |
| Reporter | thanapat khumprom |
| Priority | Medium |
| Labels | AISDLC, RWB-TE-003 |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-10T11:51:41.935+0700 |
| Updated | 2026-11-11T11:15:54.764+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

*Story:* RWB-TE-003 — TB0001-1237 · *Plan task:* TASK-018 · *Surface:* Backend
*Blocked by:* TASK-002 (TB0001-1303), TASK-003 (TB0001-1304), TASK-016
*Held:* until RWB-TE-001 is merged in ACE {{develop}} (gate TASK-004).
*Approved plan:* commit {{fd93eb7}} — [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md] · [plan.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md] (PD-06, PD-08, PD-09, §5.4)

h3. What to do

*Contract harness and* {{RecoveryContractTest}}.

* Web slice per PD-06 with the real {{SecurityConfig}} ({{auth.enabled=true}}); only its collaborators mocked; no {{DataSource}}, Flyway, JPA or session store.
* {{ContractFixtureProvider}} extension point: per operation, a synthetic fixture, service stand-ins, and the signed-in synthetic principal allowed to call it with the stand-in permission data its real access check reads, so the success call passes that check. Providers are discovered by the harness under {{th.co.scb.ace.demo.recovery}} and are never Spring components.
* Validator (TASK-003 choice) checks request and response: status, content type, schema.
* The success call passes only with a 2xx status that the operation declares; any other status (a declared 403 included) gives {{contract broken: {operationId} at $: expected a declared 2xx status, got {status}}}.
* A second dynamic set checks that the response status is declared.
* *Precedence:* an undeclared status reports only {{undocumented status {status} for {operationId}}} (SPEC-009); the 2xx rule applies only to a declared non-2xx status; schema and content-type checks run on declared statuses; the report row carries the first failing message in that order and the test output lists every message.
* Messages: {{contract broken: {operationId} at {path}: {reason}}} (first-difference JSON path) and {{undocumented status {status} for {operationId}}}.
* One dynamic test per implemented operation, whatever its release; zero implemented operations pass (PD-09).
* Add the validator as {{testImplementation}}.

h3. Deliverable

Harness classes; test class

h3. Done when

{{RecoveryContractTest}} green on ACE today (0 implemented, 144 pending).

h3. Trace

SPEC-RWB-TE-003-008, -009, -014; FR-RWB-003; CLAR-005, CLAR-013

h3. Rules

* ACE repo {{ace-monorepo}}, branch {{feature/TB0001-1237-api-contract-tests}}; commits {{TB0001-1237: <summary>}}. Shared-file edits only as listed in plan §7; {{SecurityConfig}} and {{GlobalExceptionHandler}} unchanged.
* No database: before any Gradle {{test}}/{{check}}, {{backend/dev.env}} must not point to a shared database and no {{SPRING_DATASOURCE_*}} is set.
* Synthetic data only; no payload in logs. Never replace the access check with an always-allow or always-refuse stub. If _Done when_ cannot be met, stop and report.

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| Actual Start Date | customfield_14457 | 2026-11-11 |
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-10 |
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
