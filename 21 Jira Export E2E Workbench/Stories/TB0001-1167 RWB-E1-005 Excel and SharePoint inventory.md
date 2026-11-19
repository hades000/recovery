# TB0001-1167 [RWB-E1-005] Excel and SharePoint inventory

| Field | Value |
|---|---|
| Jira | [TB0001-1167](https://scbjira.atlassian.net/browse/TB0001-1167) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Decision, R-Dependency, R-Requirement |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-05T12:37:08.395+0700 |
| Updated | 2026-11-18T17:18:18.839+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 4 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want every recovery team's Excel files, SharePoint lists and local files listed with owner, fields, update cycle and a load, retire or keep decision, so that each file can be loaded into its data product and then retired.

## Acceptance criteria

```gherkin
Feature: Excel and SharePoint inventory

  Background:
    Given the parameter tracker.inventory.teams holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF

  Scenario: AC1 Inventory covers six teams
    Given an inventory file "TRK-2026.11" with 23 rows: 5 for TDR, 3 for DIL, 6 for LIT, 4 for NPA, 2 for DEBT_SALE and 3 for WRITE_OFF
    Given each row has tracker code, tracker name, location type, location, owner user ID, field list, update cycle, decision and reason
    When the reference data administrator loads it and the data steward confirms it
    Then tracker_inventory holds 23 rows for version "TRK-2026.11"
    Then GET /admin/trackers with team "LIT" returns 6 trackers, among them "LIT-07 Litigation case tracker" on SharePoint, update cycle WEEKLY, with its owner and 18 fields

  Scenario: AC2 Decision per file
    Given the loaded version "TRK-2026.11"
    When the data steward calls GET /admin/trackers
    Then every one of the 23 trackers has a decision LOAD, RETIRE or KEEP and a reason
    Then the 14 LOAD trackers each name a target data product, for example "LIT-07" names DP07
    Then the 14 LOAD and 6 RETIRE trackers have status LISTED and the 3 KEEP trackers have status KEPT

  Scenario: AC3 A team is missing
    Given an inventory file with no row for team DEBT_SALE
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-016 "The inventory has no row for team DEBT_SALE. List its trackers, or add one row with location type NONE."
    Then the system writes no tracker_inventory row

  Scenario: AC4 A row without a decision
    Given an inventory file whose row 7 has no decision
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter decision." for row 7

  Scenario: AC5 A value outside its list
    Given an inventory file whose row 9 has decision "MAYBE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 9: decision must be one of LOAD, RETIRE, KEEP."

  Scenario: AC6 A load decision without a target data product
    Given an inventory file whose row 12 has decision LOAD and no target data product
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter target data product." for row 12

  Scenario: AC7 A tracker code twice
    Given an inventory file in which tracker code "NPA-02" is on rows 15 and 16
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-017 "Row 16: tracker code NPA-02 appears more than once."

  Scenario: AC8 The same file loaded again
    Given version "TRK-2026.11" is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The tracker inventory load for 2026-11-16 is already complete or running. It was not run again."
```

## Comments (4)

### Comment 1: NATAPATCHARA ANUROJE, 2026-11-10T11:30:36.233+0700

Comment ID 1782681

h3. Advance requirement clarification — RWB-E1-005: Excel and SharePoint Inventory

Hi team,

Although *RWB-E1-005 is not included in the current sprint*, I have reviewed the story and its supporting documentation in advance to identify questions for upcoming refinement.

The purpose of this comment is to collect the clarifications early, give the relevant owners time to review them, and reduce assumptions or rework when the story is brought into a future sprint. *This is a preparation activity, not a request to bring the story into the current sprint or start implementation.*

Please help confirm the following points.

h3. 1. Source of {{inventory_version}}

The story refers to loading inventory version {{TRK-2026.11}}, and the database includes a required {{inventory_version}} column.

However, the load contract lists only {{file}}, {{table}}, and {{validFrom}}. It does not explicitly identify how the inventory version is supplied.

*Please confirm:*

* Is the version provided in the uploaded Excel inventory template?
* If so, what is the exact column name or location—for example, a column on every row or a single value in a header/metadata section?
* Alternatively, is it supplied separately in the upload request, derived from the filename, or obtained from another source?
* If it is repeated on each row, must all rows in the file contain the same version?

This clarification is needed to define how the uploaded file is associated with its inventory version.

h3. 2. Data type of {{inventoryVersion}} in the API

There appears to be a difference between the documented representations:

* The story uses a value such as {{TRK-2026.11}}.
* The database defines {{inventory_version}} as {{varchar(20)}}.
* API Specification v2 defines {{Tracker.inventoryVersion}} as {{integer}}.

An integer cannot represent a value such as {{TRK-2026.11}}.

*Please confirm whether the API field should be changed to* {{string}} to align with the story and database. If the integer is intentional, please clarify what it represents and how it relates to the textual inventory version.

This decision is needed before finalizing the API response schema, generated types, and contract tests.

h3. 3. Visibility of {{ownerUserId}}

The inventory file contains the tracker owner’s user ID, and the tracker API includes {{ownerUserId}} in its response. This field is classified as staff personal data.

*Please confirm:*

* Can every caller with *Reference data R* see the owner’s full user ID?
* Are there additional role or team-scope restrictions?
* For callers who are not permitted to see the full value, should the field be omitted, masked, or represented in another approved form?

For example, should a team manager be able to see owner IDs across all teams, or only within their own team? This is an illustration of the access question, not a proposed rule.

This clarification concerns *who may receive the value and in what form*, rather than where the uploaded value comes from.

h3. 4. Required fields for a {{location_type = NONE}} row

AC3 states that if a team has no trackers, the inventory file should include one row with {{location_type = NONE}}. This distinguishes “the team has no trackers” from “the team’s information was omitted.”

However:

* AC1 describes rows containing tracker code, tracker name, location type, location, owner user ID, field list, update cycle, decision, and reason.
* AC4 rejects a row without a decision.
* AC3 does not explicitly state whether a {{NONE}} row is exempt from any of these requirements.

An illustrative row would look like this:

||Field||Illustrative value||
|{{team_code}}|{{DEBT_SALE}}|
|{{location_type}}|{{NONE}}|
|{{tracker_code}}|To be confirmed|
|{{tracker_name}}|To be confirmed|
|{{location_ref}}|To be confirmed|
|{{owner_user_id}}|To be confirmed|
|{{field_list}}|To be confirmed|
|{{update_cycle}}|To be confirmed|
|{{decision}}|To be confirmed|
|{{decision_reason}}|To be confirmed|

_This is an illustration, not an approved template._

*Please confirm:*

* Must a {{NONE}} row satisfy the same required-field rules as a normal tracker row?
* If not, which fields may be blank or null?
* If a decision is still required, which decision should be used for a row that represents no actual tracker?

A sample valid {{NONE}} row would help make the expected validation unambiguous.

h3. 5. Meaning of the priority values

The local story and increment card classify this story as *Must*, while Jira shows *Medium*.

These may be separate classifications rather than an actual conflict—for example, *Must* could indicate mandatory scope, while *Medium* could indicate Jira delivery priority.

*Please confirm:*

* Are both values intentional and allowed to coexist?
* If they should be aligned, which value or classification is authoritative?

This is a metadata clarification and does not change the functional behavior of the story.

h3. 6. Expected behavior when the feature flag is disabled

The story names the feature flag {{rwb.p1.tracker-inventory}}, but does not explicitly define the behavior when it is disabled.

*Please confirm which operations the flag controls:*

* Uploading and validating an inventory file through the reference-load service.
* Confirming/approving and applying an inventory version.
* Reading inventory through {{GET /admin/trackers}}.

For each operation that is unavailable while the flag is disabled:

* Should the system reject the request?
* What HTTP status and message should it return?
* Should previously loaded inventory remain readable?

The implementation mechanism can be handled by the development team; the clarification needed here is the *expected functional behavior when the configuration is off*.

h3. 7. Authority to confirm/approve an inventory version

The stories appear to describe different roles:

* *RWB-E1-005* states that *RW-DATASTEW* confirms the inventory version as its owner.
* *RWB-E1-043*, the shared reference-data service story, identifies *RW-RISK* with *Reference data A* as the approver.

Both require separation of duties: the person who uploads the version must not approve that same version.

*Please confirm:*

* Is the Data Steward’s owner confirmation the same action as the shared reference-data approval, or are they two separate steps?
* If they are the same action, which role and capability right should authorize it?
* If they are separate steps, what is the required sequence, who performs each step, and at which point are the inventory rows applied?

The restriction against self-approval will remain in place; the outstanding question is the intended approval responsibility and workflow.

----

Please provide the agreed answers, or identify the relevant decision owner for any items requiring further discussion. We can then update the specification and acceptance/test expectations before the story is planned for a future sprint.

### Comment 2: Pe Chichareon, 2026-11-11T15:42:15.773+0700

Comment ID 1785859

From 11 Nov requirement grooming in the morning 

  Some of ACs of this story rely on future ticket work

  TechX already feedback that this will cause this Jira ticket unable to be closed in the sprint

  Requested Henka to adjust story, ACs to have only content that can be completed in the sprint.



From 11 Nov requirement grooming in the afternoon 15:00

  Henka presented with new content Develop action plan 

Next action: TechX provided the feedback that Henka should revisit the content only content (Action item, AC) that can complete in current sprint 

  The content that can complete in future sprint should separated into new story.

### Comment 3: NAMTIP WONGSOMBOON, 2026-11-11T15:43:24.466+0700

Comment ID 1785869

* Scenario: AC1 Inventory covers six teams
* Scenario: AC2 Decision per file
* Scenario: AC3 A team is missing
* Scenario: AC4 A row without a decision
* Scenario: AC5 A value outside its list
* Scenario: AC6 A load decision without a target data product
* Scenario: AC7 A tracker code twice
* Scenario: AC8 The same file loaded again

As discussed during the Grooming session on 11 Nov 2026, all Acceptance Criteria (ACs) must be testable and aligned with the User Story. ACs that cannot be tested should be removed and replaced with appropriate, testable ACs that reflect the Story requirements.

@CHANISSARA MAHAKITTIKUN  

### Comment 4: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:11:31.008+0700

Comment ID 1790658

@NAMTIP WONGSOMBOON Noted


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
