# TB0001-1184 [RWB-E1-022] Sign-on with SSO, MFA and the first roles

| Field | Value |
|---|---|
| Jira | [TB0001-1184](https://scbjira.atlassian.net/browse/TB0001-1184) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:23.150+0700 |
| Updated | 2026-11-18T17:28:27.394+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a case owner (RW-CASEOWN), I want to sign in to the Workbench once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow, so that access is controlled from the first release and nobody holds a Workbench password or a local account.

## Acceptance criteria

```gherkin
Feature: Sign-on with SSO, MFA and the first roles

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force from 30 November 2026
    Given separation of duty version "SOD-2026.11" is in force
    Given role RW-CASEOWN has entra_group "RWB-SIT-RW-CASEOWN" and default scope "OWN"

  Scenario: AC1 SSO sign-in
    Given test user "U-1001" is in Entra ID group "RWB-SIT-RW-CASEOWN"
    When the user opens the Workbench and signs in with password and second factor
    Then the session holds roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11"
    Then GET /me/session returns the line "Case owner. Scope: own cases."
    Then the menu shows the screens of the capability areas where RW-CASEOWN holds R, and no Administration menu

  Scenario: AC2 Role denied
    Given test user "U-1002" holds only RW-PHONECOL, whose Platform administration letter is "-"
    When the user calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002 with action "read roles"
    Then the system writes one refusal event with user "U-1002", area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED"

  Scenario: AC3 Not in group
    Given test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-"
    When the user opens the Workbench
    Then the access request page shows MSG-P4-001 and no case, queue or reference data
    Then every recovery endpoint returns status 401 for that token
    Then the system writes one refusal event with reason "NO_ROLE"

  Scenario: AC4 Sign-in without a second factor is refused
    Given test user "U-1004" is in group "RWB-SIT-RW-CASEOWN"
    Given the token's amr claim holds "pwd" and not "mfa"
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005
    Then the system writes one refusal event with reason "NO_MFA"

  Scenario: AC5 Two roles give the permissions of both
    Given test user "U-1005" is in groups "RWB-SIT-RW-LITOFF" and "RWB-SIT-RW-LEGAL"
    When the user signs in
    Then the session holds roles "RW-LITOFF" and "RW-LEGAL"
    Then the Documents letters are "CRUA", the union of "CRU" and "CRUA"
    Then no permission comes from any role the user does not hold

  Scenario: AC6 A conflicting role pair is refused
    Given test user "U-1006" is in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN"
    Given the role conflict table says RW-SECADM may not hold any business role
    When the user signs in
    Then the system refuses the session with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN"
    Then the system raises an incident to the security administrator queue
    Then the system writes one refusal event with reason "ROLE_CONFLICT"

  Scenario: AC7 A service identity is checked like a person
    Given managed identity "SY-RULES" is in group "RWB-SIT-SY-RULES"
    When it calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then the system writes one refusal event with user "SY-RULES"

  Scenario: AC8 An unmapped or inactive group gives no role
    Given test user "U-1008" is in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01"
    Given no active role row has entra_group "RWB-SIT-LEGACY01"
    When the user signs in
    Then the session holds only "RW-CASEOWN"
    Then the system writes the unmapped group name on the sign-in event

  Scenario: AC9 An open session keeps the versions it resolved
    Given test user "U-1009" signed in at 09:00 on 1 December 2026 under matrix version "PM-2026.11"
    Given matrix version "PM-2026.12" takes effect at 10:00 on 1 December 2026 and removes R in Reporting from RW-CASEOWN
    When the user calls GET /reports/measures at 10:30 in the same session
    Then the system checks the call against "PM-2026.11" and allowed
    Then after the user signs in again at 11:00 the same call is refused with MSG-P4-002
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
