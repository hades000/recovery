# TB0001-1236 [RWB-TE-002] Code owners for the recovery module

| Field | Value |
|---|---|
| Jira | [TB0001-1236](https://scbjira.atlassian.net/browse/TB0001-1236) |
| Type | Story |
| Status | Dev To Do |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | NAMTIP WONGSOMBOON |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Decision |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-05T16:11:10.696+0700 |
| Updated | 2026-11-18T00:58:38.602+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 8 |

## Description

As a squad member (RW-TRIBE), I want a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge, so that every change in the recovery module is reviewed by its owners.

## Acceptance criteria

```gherkin
Feature: Code owners for the recovery module

  Background:
    Given the code owners file maps the recovery folders to "@scb-ace/techx-recovery-tech-leads" and the common module folder to "@scb-ace/ace-team"
    Given main requires one code owner approval and dismisses stale approvals

  Scenario: AC1 Review required
    Given a pull request that changes "ace-service/src/main/java/<ACE base path>/recovery/casewf/internal/AllocationService.java"
    When it is opened
    Then a TechX tech lead is required as reviewer
    Then an approval from a squad member outside the team leaves the merge blocked

  Scenario: AC2 A common module change needs the ACE team
    Given a pull request that changes a file under "ace-service/src/main/java/<ACE base path>/common/"
    When it is opened
    Then "@scb-ace/ace-team" is required as reviewer

  Scenario: AC3 A change across both modules needs both teams
    Given a pull request that changes one recovery file and one common module file
    When a TechX tech lead approves
    Then the merge stays blocked until a member of "@scb-ace/ace-team" also approves

  Scenario: AC4 Front end, migrations and the module map are covered
    Given a pull request that changes "ace-web/src/modules/recovery/caselist/CaseListPage.tsx", a file under "ace-service/src/main/resources/db/migration/recovery/" and "architecture/recovery-modules.yaml"
    When it is opened
    Then "@scb-ace/techx-recovery-tech-leads" is required for all three

  Scenario: AC5 An author cannot approve their own change
    Given a TechX tech lead opens a pull request on a recovery folder
    When the same tech lead approves it
    Then the merge stays blocked until a second member of the team approves

  Scenario: AC6 A new commit needs a new approval
    Given an approved pull request on a recovery folder
    When a new commit is pushed to it
    Then the system dismisses the approval and code owner review is required again

  Scenario: AC7 An owner that does not exist fails the check
    Given the code owners file names "@scb-ace/recovery-leads-typo" for a recovery path
    When the pipeline runs
    Then the code owners validation step fails and names the owner not found
```

## Sub-tasks

- TB0001-1275 [To Do] [RWB-TE-002] GitLab group creation & access grant
- TB0001-1276 [To Do] [RWB-TE-002]  Protected-branch rule + CODEOWNERS file

## Comments (8)

### Comment 1: PREMMAST SUWANNIKOM, 2026-11-09T10:44:37.514+0700, edited 2026-11-09T10:46:11.268+0700

Comment ID 1780455

[Dev-TechX]

Status update / scope clarification

Implementing code owners requires changes at the Git repository level (CODEOWNERS configuration), which is outside the scope that our team can change directly.

This has been discussed within the working team and aligned with Khun Pipat (SCB). The agreement is:

* Any change in the Pipeline, Git, or Lint layer will be pulled out of our delivery scope.
* If the setting is genuinely required, it must be aligned and configured jointly with the Collection team.

Action required: please confirm whether this item should be descoped or scheduled as a joint setup with the Collection team.



cc @PIPAT SAENGOW  @Pachara Thipgate @Jesniphat Pukkham  @pongpat.jantanon 

### Comment 2: PONGCHAI CHAROENRUNGRODKUN, 2026-11-10T14:17:03.162+0700

Comment ID 1783155

@PREMMAST SUWANNIKOM Yes, Confirmed

### Comment 3: PONGCHAI CHAROENRUNGRODKUN, 2026-11-10T14:42:21.032+0700

Comment ID 1783259

@PREMMAST SUWANNIKOM confirm to proceed

### Comment 4: PONGCHAI CHAROENRUNGRODKUN, 2026-11-11T11:05:33.960+0700

Comment ID 1784921

@PREMMAST SUWANNIKOM Confirm to Proceed

### Comment 5: PONGCHAI CHAROENRUNGRODKUN, 2026-11-11T11:30:31.232+0700

Comment ID 1785028

Assign code owner to @Jesniphat Pukkham so he will be main approval

### Comment 6: PONGCHAI CHAROENRUNGRODKUN, 2026-11-11T12:20:16.000+0700

Comment ID 1785148

@PONGCHAI CHAROENRUNGRODKUN follow ACE standard

### Comment 7: NAMTIP WONGSOMBOON, 2026-11-13T09:37:06.915+0700, edited 2026-11-13T09:37:42.651+0700

Comment ID 1789027

@CHANISSARA MAHAKITTIKUN Please clarify this issue with the ACE team and provide a proposed solution.
cc: @PIPAT SAENGOW @PONGCHAI CHAROENRUNGRODKUN @Jesniphat Pukkham @PREMMAST SUWANNIKOM 

### Comment 8: CHANISSARA MAHAKITTIKUN, 2026-11-16T17:16:47.096+0700

Comment ID 1793190

@NAMTIP WONGSOMBOON 

Here is the clarification and proposed solution regarding [RWB-TE-002] Code owners for the recovery module:

h3. 1. Scope & Story Clarification

* *Item Identity:* This item is *RWB-TE-002* ("Code owners for the recovery module", Increment {{INC-004}}) under {{EPIC-001}} (Module: P2 Integration). It is a technical enabler tracing to {{REQ-DRI-006}} (BRD Program §7), with no UI, API, or DB migrations.
* *Collection Module:* As defined in the story contract, *collection-module ownership is strictly out of scope*. There is no dependency on the Collection team to deliver this enabler.

h3. 2. Deliverables & Repository Controls

RWB-TE-002 delivers three specific repository controls:

# {{.github/CODEOWNERS}} file
# {{CodeOwnersValidation}} PR pipeline step
# {{main}} branch protection rule (1 code-owner approval required, stale approvals dismissed, author approval excluded)

h3. 3. Ownership & Handle Rules (Addressing Individual Assignment)

Regarding the suggestion to assign ownership to an individual:

* Per the story contract and ACE governance standards, *team handles must be used—never individual accounts*.
* Ownership mapping:
** Recovery backend, test, migration, frontend, and {{architecture/recovery-modules.yaml}} → {{@scb-ace/techx-recovery-tech-leads}}
** Common module → {{@scb-ace/ace-team}}
** {{.github/CODEOWNERS}} file → Both teams
_(Note: Decision D-RCV-21 mentions squad developers, but the formal story contract governs and requires team handles)._

h3. 4. Proposed Solution & Implementation Split

To address TechX's permission and delivery boundary:

# *TechX Scope:*
#* Create and commit {{.github/CODEOWNERS}} with the agreed team handles.
#* Add the {{CodeOwnersValidation}} step into the PR pipeline.
#* Verify verification criteria TC-TE-002-01 through TC-TE-002-08.
# *ACE / Repo Admin Scope:*
#* Configure the GitHub {{main}} branch protection rule to require code-owner review.
#* Confirm GitHub team handles {{@scb-ace/techx-recovery-tech-leads}} and {{@scb-ace/ace-team}} exist and have appropriate squad membership (pending DL36/DL37).


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
