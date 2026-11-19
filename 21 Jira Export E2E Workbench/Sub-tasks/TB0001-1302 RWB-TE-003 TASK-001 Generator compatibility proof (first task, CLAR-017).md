# TB0001-1302 [RWB-TE-003] TASK-001 Generator compatibility proof (first task, CLAR-017)

| Field | Value |
|---|---|
| Jira | [TB0001-1302](https://scbjira.atlassian.net/browse/TB0001-1302) |
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
| Created | 2026-11-10T11:48:20.512+0700 |
| Updated | 2026-11-11T10:42:20.218+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

*Story:* RWB-TE-003 — TB0001-1237 · *Plan task:* TASK-001 · *Surface:* Backend
*Blocked by:* NONE
*Held:* stage 7 waits for the plan-gate re-check of plan run 7, the approver's confirmation of the final commit (AC-PLAN-11) and OPEN-044. RWB-TE-001 is merged in ACE {{develop-recovery}} (2026-11-10).
*Plan text:* plan run 7 (2026-11-11; runs 5–6 approved by Jesniphat Pukkham 2026-11-10, final commit to be confirmed) — [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md] · [plan.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/spec/INC-005-te-003-attempt-02/recovery/output/INC-005-epic-1-RWB-TE-003/plan/plan.md] on branch {{spec/INC-005-te-003-attempt-02}} (MR !21). Last approved version: {{fd93eb7}}.

h3. What to do

*Generator compatibility proof (first task, CLAR-017).* In a throwaway local copy of ACE {{develop-recovery}} (never merged), apply candidate DEP-1 with the configuration of plan §5.3 to the real API file (split into one copy per {{x-module}}, with one tag per operation and only the reachable {{components}}, by a prototype of the pre-processor, PD-04) and build with ACE's Gradle 9.4.1 wrapper, {{org.gradle.configuration-cache=true}} and {{org.gradle.caching=true}}. Try in order: G1 Spring Boot 4 mode of the pinned version (if offered); G2 Boot 3 / Jakarta mode on Boot 4.2; G3 G1/G2 plus minimal custom templates (needs tech-lead acceptance *and* a plan amendment approved by the plan approver, because the template files are new recovery files not listed in plan §7). Acceptance: *AC-1* the 144 per-operation interfaces and each module's own models (19 module packages, each with a {{model}} sub-package; PD-02 run 6) compile with {{./gradlew compileJava}} and no other ACE dependency change; *AC-2* generated sources import no {{com.fasterxml.jackson.databind}}, {{com.fasterxml.jackson.datatype}} or {{org.openapitools.jackson.nullable}} type (only {{com.fasterxml.jackson.annotation}}, shared by Jackson 3), checked with {{grep -r}}, because Jackson 2 databind is on ACE's classpath ({{jackson-datatype-jsr310:2.22.1}}; {{JsonConverter}}, {{JsonListConverter}}, {{EntityReferenceSerializer}}) and would hide the problem at compile time; the same scan shows no type from RWB-TE-001's {{clientLibraries}} list in the module map (rule BND-5, R-22); *AC-3* runtime round-trip through MockMvc with Spring's Jackson 3 mapper, using throwaway controllers on the generated P3 interface; each part is pass/fail: (i) {{getCasesCaseidTimers}} returns a {{Timer}} list in which the 8 required fields ({{id}}, {{caseId}}, {{timerType}}, {{startedAt}}, {{expiresAt}}, {{paused}}, {{status}}, {{escalationLevel}}) are written, an unset optional field (for example {{taskId}}) is omitted and not written as {{null}} (the file declares no nullable property), {{date-time}} ({{startedAt}}) is ISO-8601 text and {{uuid}} ({{id}}) is text; (ii) {{getCasesCaseid}} returns a {{Case}} whose {{format: date}} field {{entryDate}} is written as {{YYYY-MM-DD}}; (iii) request side — the file declares required request data only as {{requestBody.required: true}} (no request schema has a {{required}} list and no query parameter is required; checked on 2026-11-10), so for {{postCasesCaseidInteractions}} (P3, first in E1, {{requestBody.required: true}}) the generated body parameter is required (reflection on {{@RequestBody}}), and a POST with no body but a valid CSRF token and a signed-in principal is refused by body handling before the controller method runs (invocation count 0; the response is not the CSRF or authorization refusal) with a 4xx status, recorded with its value (Spring is expected to answer 400; that this 400 is not declared for the operation is a contract matter for the story that implements it, not a generator defect); (iv) no {{JsonNullable}} type is generated; *AC-4* the operation answers at {{/api/recovery/v1/cases/{caseId}/timers}} behind ACE's context path {{/api}}; *AC-5* (PD-05, run 3) each operation is generated as its own interface (for example {{GetCasesCaseidTimersApi}}) with one abstract method, in its module's package; a throwaway controller implementing only {{GetCasesCaseidTimersApi}} compiles, and leaving its method out fails compilation; a signed-in call to {{getCasesCaseid}} (not implemented) reaches no recovery handler — status recorded (expected 404), never 200 or 501 — and an unauthenticated call answers 401; *AC-6* two clean generations give byte-identical sources; *AC-7* the plugin resolves through the SCB {{gradle-m2-proxy}} with {{DISABLE_SCB_REPO=0}}, as in the Jenkins image build of the root {{Dockerfile}} (or the gap is recorded for P-3), and {{DISABLE_SCB_REPO=1 ./gradlew bootJar}} succeeds in a copy holding only {{backend/}}, as {{backend/Dockerfile}} does (plugin from {{gradlePluginPortal()}}); *AC-8* {{checkstyleMain}} passes with the planned suppression entry; also confirm SnakeYAML is on the classpath ({{dependencyInsight}}) and whether PD-04's applied script works with the configuration cache. *Stop rule:* if no candidate meets AC-1..AC-5 (all parts of AC-3 included), stop, record the failures and report BLOCKED to the recovery tech lead; no other task starts.

h3. Deliverable

{{implement/generator-proof.md}} (configuration, pinned version, command output, grep result, AC table)

h3. Done when

Every AC row (and each part (i)–(iv) of AC-3) PASS with command, exit code and output excerpt; tech lead reads the record

h3. Trace

SPEC-RWB-TE-003-003, SPEC-RWB-TE-003-013; FR-RWB-003; CLAR-002, CLAR-017

h3. Rules

* ACE repo {{ace-monorepo}}, branch {{feature/TB0001-1237-api-contract-tests}} from {{develop-recovery}}; merge request into {{develop-recovery}} (D-RCV-56); commits {{TB0001-1237: <summary>}}. Edit only the paths listed in plan §7.
* If _Done when_ cannot be met, stop and report.
* Evidence ({{implement/...}}) goes to {{recovery/output/INC-005-epic-1-RWB-TE-003/implement/}} in the AISDLC repo {{AP2477-ACE/ace-aisdlc}}.

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
