# TB0001-1219 [RWB-E1-058] Agent platform set-up [E1a]

| Field | Value |
|---|---|
| Jira | [TB0001-1219](https://scbjira.atlassian.net/browse/TB0001-1219) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:53.441+0700 |
| Updated | 2026-11-17T10:08:47.761+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a platform administrator (RW-PLATADM), I want the model gateway, the prompt and policy store, the guardrail checker and the evaluation harness deployed in the recovery module, so that every Workbench agent is built, called, checked and scored through one path with its versions recorded.

## Acceptance criteria

```gherkin
Feature: Agent platform set-up [E1a]

  Background:
    Given the test agent "ECHO" has policy version "P1" approved with model "MODEL-A-2026-10", timeout 60 seconds, confidence floor 0.80 and allowed tools "read_case"
    Given prompt version "PR1" is approved for agent "ECHO"
    Given the model endpoint stub answers in 1,200 milliseconds with 900 input tokens and 150 output tokens
    Given the policy price is 0.0500 baht per 1,000 tokens

  Scenario: AC1 Approved endpoint
    Given the approved model endpoint on the private endpoint of the SCB tenant
    When the orchestrator runs agent "ECHO" for case "RW-2026-000101"
    Then the call succeeds with run status "ANSWERED"
    Then one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht
    Then the system writes one AgentRunCompleted event to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false

  Scenario: AC2 Prompt versions
    Given prompt version "PR1" is in force for agent "ECHO"
    When RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20
    Then prompt version "PR2" exists with status "APPROVED"
    Then prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged
    Then a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2"

  Scenario: AC3 Schema check
    Given the model stub returns an answer with field "summary" missing from the output schema of "ECHO"
    When the guardrail runs
    Then the system rejects the output with run status "GUARDRAIL_FAILED" and fallback true
    Then the guardrail result holds check code "SCHEMA" with the missing field name
    Then the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1

  Scenario: AC4 Evaluation suite
    Given labeled sample "ECHO-S1" version 1 with 20 rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S1"
    Then one evaluation run ends with status "DONE" and 20 agent run rows with trigger "EVALUATION" and mode "SHADOW"
    Then one score row per label key holds sample size, true positives, false positives, false negatives, precision and recall
    Then each score row holds policy version "P1", prompt version "PR1" and model version "MODEL-A-2026-10"

  Scenario: AC5 Guardrails
    Given an agent with the allowed tool list "read_case"
    When it calls the tool "propose_deviation", which is not on its list
    Then the system refuses the tool call and not executed
    Then the agent run holds status "GUARDRAIL_FAILED", check code "TOOL_NOT_ALLOWED" and fallback true
    Then the orchestrator returns a fallback result with reason "TOOL_NOT_ALLOWED" so the calling step takes the rule path

  Scenario: AC6 The model does not answer inside the timeout
    Given the model stub does not answer for 61 seconds
    When the orchestrator runs agent "ECHO" for case "RW-2026-000102"
    Then the system ends the call at 60 seconds
    Then the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms
    Then the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32)

  Scenario: AC7 Personal data is masked before the model call
    Given case "RW-2026-000103" has a borrower with a synthetic national ID number and a synthetic mobile number
    When the orchestrator builds the request to the model endpoint
    Then the request body holds the masking tokens returned by the P4 masking service for SY-AGENT
    Then the request body, the agent run row and the application log hold no national ID number, phone number, name or account number

  Scenario: AC8 A configuration file that fails a check is refused
    Given a policy file for agent "ECHO" with timeout_seconds 0
    When RW-COE loads it through POST /admin/agent-configs
    Then the system refuses the load with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120"
    Then policy version "P1" stays in force and no new version row exists

  Scenario: AC9 The loader cannot approve their own version
    Given user "coe.user01" loaded policy version "P2" for agent "ECHO"
    When user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
    Then version "P2" keeps status "LOADED"

  Scenario: AC10 An answer below the confidence floor falls back
    Given the model stub returns a valid answer with confidence 0.79
    When the guardrail runs with confidence floor 0.80
    Then the agent run holds status "BELOW_FLOOR" and fallback true
    Then the orchestrator returns a fallback result with reason "BELOW_FLOOR"

  Scenario: AC11 A repeated run request has no further effect
    Given agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30"
    When the same request arrives again with the same key
    Then no second agent run row and no second model call exist
    Then the system returns the first result and the idempotency hit is counted (R-UNI-40)

  Scenario: AC12 Two approvals of one version at the same time
    Given policy version "P2" for agent "ECHO" has status "LOADED" and row version 1
    When two RW-RISK users approve "P2" at the same time
    Then one approval succeeds and "P2" has status "APPROVED"
    Then the system refuses the other with 409 and MSG-GEN-004

  Scenario: AC13 An evaluation on an empty sample is refused
    Given sample "ECHO-S2" has 0 labeled rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S2"
    Then the system refuses the request with 422 and MSG-P10-002
    Then no evaluation run and no agent run row exist

  Scenario: AC14 A second evaluation while one is running is refused
    Given the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING"
    When RW-COE starts the same evaluation again
    Then the system refuses the request with 409 and MSG-P10-003
    Then one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING"

  Scenario: AC15 Agent runs are listed without their content
    Given 3 runs of agent "ECHO" between 2026-11-30 and 2026-12-01
    When RW-PLATADM calls GET /admin/agent-runs with agent "ECHO", from "2026-11-30" and to "2026-12-01"
    Then 3 AgentRun items return with id, agent, agentVersion, caseId, outcome, fallback and latencyMs
    Then no item holds the prompt text, the model answer or a personal field
```

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
| Created Date | customfield_10249 | 2026-11-05 |
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
