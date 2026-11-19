# TB0001-1323 [RWB-TE-003] TASK-022 Fixtures and harness self-tests

| Field | Value |
|---|---|
| Jira | [TB0001-1323](https://scbjira.atlassian.net/browse/TB0001-1323) |
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
| Created | 2026-11-10T11:53:28.239+0700 |
| Updated | 2026-11-11T11:29:01.157+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

*Story:* RWB-TE-003 — TB0001-1237 · *Plan task:* TASK-022 · *Surface:* Backend
*Blocked by:* TASK-019 (TB0001-1320), TASK-021
*Held:* until RWB-TE-001 is merged in ACE {{develop}} (gate TASK-004).
*Approved plan:* commit {{fd93eb7}} — [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md] · [plan.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md] (PD-07, PD-08) · [test scenarios|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tests/scenarios.md]

h3. What to do

*Fixtures and harness self-tests* (package {{…recovery.apicontract.fixture}}, PD-07, PD-08):

* {{ContractFixtures}} (synthetic) and a fixture provider; test-only matrix CSV.
* Fixture controllers implementing {{GetCasesCaseidTimersApi}} (P3): valid; text for {{escalationLevel}}; returns undeclared 400; no access check (deliberately broken); access check against the test-only matrix with the scoped advice.
* One fixture controller implementing {{GetFeatureFlagsApi}} (area {{None}}) and {{GetCasesCaseidPlanStatusApi}} (first in E2) (P2).
* *Isolation:* every fixture controller and test-only bean (check bean, scoped advice, stand-ins) is a static nested class of its self-test class or carries {{@TestComponent}}, so ACE's application scan of {{th.co.scb.ace.demo}} skips it; each self-test slice registers its fixtures with an explicit {{@Import}}. Each slice holds at most one controller per generated interface (two would map the same route).
* *TC-TE-003-02 mechanism:* the fixture implements {{GetCasesCaseidTimersApi}} and returns, through an unchecked cast of the erased {{ResponseEntity}}, a body whose item 0 holds {{"escalationLevel": "high"}}; fallback, a test-only Jackson 3 mix-in registered only in that self-test slice.

Self-tests:

* TC-TE-003-02 → {{contract broken: getCasesCaseidTimers at $[0].escalationLevel: …}}
* TC-TE-003-04 → {{undocumented status 400 for getCasesCaseidTimers}}
* TC-TE-003-06: {{rwb.release=E1}}; {{postQueuesQueueidPlacements}} (E2) and an E1 operation unimplemented → both PENDING, run passes.
* TC-TE-003-08: no check → {{access not enforced for getCasesCaseidTimers}}; with check → PASSED (403, {{application/problem+json}}, MSG-P4-002).
* UT-014: {{getCasesCaseidPlanStatus}} implemented at {{rwb.release=E1}} → contract and access tests run, report shows E2.
* UT-015: allow-all stub → {{access not enforced}} (the test is not hollow).
* UT-009 at slice level.
* UT-P19: only {{GetCasesCaseidTimersApi}} implemented → a signed-in call to {{getCasesCaseid}} reaches no recovery handler (status recorded, never 200 or 501); {{getCasesCaseid}} PENDING; run passes.
* UT-P20 {{FixtureIsolationTest}}: Spring's candidate-component scan of {{th.co.scb.ace.demo}} with the filters of {{@SpringBootApplication}} plus Spring Boot's test-type exclude filter, without starting a context or a database, finds no class from {{…apicontract..}}.

h3. Deliverable

Fixture classes and resources; {{ContractHarnessSelfTest}}, {{AccessHarnessSelfTest}}, {{FixtureIsolationTest}}

h3. Done when

All self-tests green; each negative case asserts FAILED with the exact message; ACE's full-context tests ({{DemoApplicationTests}}, {{HealthEndpointTests}} and the other {{@SpringBootTest}} classes) pass with the fixtures on the test classpath, without editing ACE's tests; {{FixtureIsolationTest}} passes.

h3. Trace

SPEC-RWB-TE-003-005, -007, -008, -009, -010, -011, -014; FR-RWB-003, FR-RWB-012; CLAR-008, CLAR-011

h3. Rules

* ACE repo {{ace-monorepo}}, branch {{feature/TB0001-1237-api-contract-tests}}; commits {{TB0001-1237: <summary>}}. Do not edit other ACE modules or their tests.
* No database; synthetic data and role codes only.
* Never disable, skip or weaken a test. If _Done when_ cannot be met, stop and report.

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
