# TB0001-1208 [RWB-E1-047] Feature flags for module release with a removal date

| Field | Value |
|---|---|
| Jira | [TB0001-1208](https://scbjira.atlassian.net/browse/TB0001-1208) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:44.525+0700 |
| Updated | 2026-11-18T17:05:35.381+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a platform administrator (RW-PLATADM), I want a feature flag service with each flag held as data (key, owner, value per environment, removal date) and read by the service and the front end at run time, so that a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told.

## Acceptance criteria

```gherkin
Feature: Feature flags for module release with a removal date

  Background:
    Given flag "rwb.casewf.case-list-queue-column" exists with default off, owner team "P3 squad" and removal date 2027-01-31

  Scenario: AC1 Flag off by default
    Given the flag has no value set for UAT
    When the case list service starts in UAT
    Then FeatureFlags.isOn("rwb.casewf.case-list-queue-column") returns false
    Then the system hides the queue column on SCR-02 Case list

  Scenario: AC2 Flag switched on
    Given a platform administrator sets the flag to on in UAT with reason "UAT test of queue column" at 10:15
    When the case list page is reloaded at 10:16
    Then the queue column shows without a deployment
    Then a change row holds environment "UAT", old value off, new value on, the user and the time 10:15
    Then the ACE audit log holds the same change

  Scenario: AC3 Flag expiry
    Given flag "rwb.p5.ocr-intake" has removal date 2026-11-30 and owner team "P5 squad"
    Given today is Monday 2026-12-07
    When the weekly flag report runs at 08:00
    Then the system lists the flag for removal with its owner and 7 days past its removal date
    Then the report carries message MSG-P2-003 for the flag
    Then the system does not list flag "rwb.casewf.case-list-queue-column" with removal date 2027-01-31

  Scenario: AC4 Removal date checked at creation
    Given today is 2026-11-16
    When a platform administrator creates flag "rwb.p6.line-dispatch" with removal date 2026-11-10
    Then the system does not creat the flag
    Then the response is 422 with message MSG-GEN-003
    Then a creation with no removal date returns 422 with message MSG-GEN-001

  Scenario: AC5 Change without a reason refused
    When a platform administrator sets the flag to on in SIT with an empty reason
    Then the response is 422 with message MSG-GEN-001
    Then the flag stays off in SIT

  Scenario: AC6 Unknown key in code
    When code calls FeatureFlags.isOn("rwb.casewf.not-defined")
    Then the result is false
    Then a warning with the key and no user data is written to the application log

  Scenario: AC7 Flag store unavailable
    Given the flag is on in UAT and the cache holds the value from 10:20
    When the flag table cannot be read at 10:21
    Then FeatureFlags.isOn returns true from the cache
    Then after a restart with the table still unavailable it returns false

  Scenario: AC8 Two changes at once
    Given two platform administrators read the flag at version 4
    When both send a change with If-Match version 4
    Then the system saves one change with version 5
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC9 Change to a key that does not exist
    When a platform administrator sends a change for flag "rwb.p9.unknown"
    Then the response is 404 with message MSG-P2-016
```

## Attachments

- [image-20261117-112555.png](../../Attachments/TB0001-1208/image-20261117-112555.png) (20647 bytes, Nuttapon Jittachotisak, 2026-11-17T18:25:59.912+0700)

## Comments (3)

### Comment 1: Ratchadaphorn Kasemphin, 2026-11-16T23:30:16.606+0700, edited 2026-11-17T12:03:07.780+0700

Comment ID 1793575

@CHANISSARA MAHAKITTIKUN  
cc. @Chitchaya Muanchonchana 

After reviewing the card, I have the following concerns and questions that need clarification:

*Concerns (Dependencies):* The card lists only RWB-E1-001 as a dependency. Several of its ACs and test cases also need the cards below to be completed first. All of them come later in the build sequence (this card is #16).

* *RWB-TE-007 (Scheduled jobs on Quartz, #21)* — provides the Quartz scheduler that runs the weekly flag report job ({{FlagRemovalReportJob}}, Monday 08:00 Asia/Bangkok). Without it, AC3 (Flag expiry) can only be tested by calling the job by hand, not as a scheduled run.
* *RWB-E1-022 (Sign-on with SSO, MFA and the first roles, #26)* — provides sign-on and the Entra ID group to role mapping, for example RWB-UAT-RW-PLATADM to RW-PLATADM. Without it, there is no signed-in RW-PLATADM user to create or change flags, and GET /feature-flags cannot do its session check (401 / MSG-P4-001).
* *RWB-E1-037 (Role to permission matrix and PDPA masking, #27)* — provides the "Platform administration" capability with C/R/U rights for each role. Without it, the endpoints cannot enforce access, so TC-E1-047-10 (RW-CASEOWN refused with 403 / MSG-P4-002) cannot be tested.
* *RWB-E1-002 (#45) and RWB-E1-031 (#48)* — build SCR-02 Case list and its queue column. The reference flag {{rwb.casewf.case-list-queue-column}} hides and shows that column, so AC1, AC2 and the "Done when" condition (column hidden and shown in UAT without a deployment) cannot be tested end to end until these cards are done.
* *ACE common module (external)* — AC2 needs the ACE audit log service, and the weekly report emails owners and the RW-PLATADM group through the ACE notification path for staff. We need confirmation that both are available in SIT and UAT, plus their API contracts.

----

*Clarification needed:*

*1.Response shape of GET /feature-flags*

The story's contract (section 12) says the response is a "Map of flag key to boolean for the caller's environment." API Specification v4 and TSD P2 (API-P2-005) define it as an array of {{FeatureFlagValue}}.

{color:#ff5630}*Question:*{color} Which shape is correct? The {{useFeatureFlag}} hook and the contract tests depend on the answer.

*2."Flag has no value set for UAT" (AC1)*

*AC1* starts with "the flag has no value set for UAT". The physical schema v6 defines {{uat_on boolean NOT NULL DEFAULT false}}, and Flow step 2 sets every environment to the default when the flag is created. So a "no value" state cannot exist in the data.

{color:#ff5630}*Question:* {color}Does AC1 mean "UAT still holds the default value (off)"? If so, what is {{default_on}} used for after creation? Is it only the starting value, or does {{isOn()}} fall back to it in some cases?

*3.Flag store unavailable after a restart (AC7, BR5)*

*AC7* and BR5 say that if the flag table cannot be read and there is no cached value (for example, after a restart), every flag returns off. In PROD, this means features that are already switched on would be switched off for users while the database is down.

{color:#ff5630}*Question:*{color} Can we confirm that Business and Operational Risk accept this behaviour in PROD? If not, is a fallback in scope, such as the last known snapshot or a config file?

*4.Flag key format validation*

Flow step 2 checks the key pattern {{rwb.<module>.<short-name>}}, and the solution plan adds a check constraint {{^rwb\.[a-z0-9]+\.[a-z0-9-]+$}}. However:

* No AC, exception path or test case covers an invalid key, for example {{RWB.P3.Test}} or {{rwb.p3}}.
* No AC or test case covers creating a flag whose key already exists. The contract lists 409 / MSG-GEN-004 for this.
* The examples mix naming styles: {{rwb.casewf.*}}, {{rwb.p5.*}}, {{rwb.p3.temporal}}.

{color:#ff5630}*Questions:*{color}

# What should the response be for an invalid key? 422 with which message ID?
# Should the {{<module>}} part be the module code ({{p3}}) or a short name ({{casewf}})?



*5.Removal date boundaries*

Exception X2 refuses a removal date "before today", and the weekly report lists flags with {{removal_date}} "before today."

{color:#ff5630}*Questions:* {color}Please confirm these two cases:

# A flag created with removal date = today is accepted.
# A flag whose removal date = today (for example, a Monday report on the removal date itself) is *not* listed until the following Monday.

Is there also a maximum allowed removal date, for example no more than 6 months ahead?

*6.Retiring a flag and changing flag details*

Section 10 says RW-PLATADM can retire flags, and the table has an {{is_active}} column. However, the contract has no endpoint for retiring a flag, and none for changing removal_date, owner or description after creation.

{color:#ff5630}*Questions:*{color}

# Are retire and edit in scope for this story, or deferred to SCR-44 (Epic 8)?
# After a flag is retired, what does {{FeatureFlags.isOn()}} return: off, or the last value?
# Is a retired flag still allowed to stay in code without a warning?

*7.Changing a flag to the value it already has*

The contract says "Setting the value it already has writes no change row," but no AC or test case covers this.

{color:#ff5630}*Questions:*{color} Can we confirm the expected result when a flag is already on in UAT and the admin sends PATCH value=on again?

* Is the response 200 with the unchanged flag?
* Does {{version}} stay the same?
* Is an ACE audit entry written?
* Is a reason still required?

*8.Weekly report rerun (idempotency)*

The job contract says "Idempotency key: report date; a rerun on the same date sends nothing new." No table or column stores the report date, and the schema has no job-run table for this job.

{color:#ff5630}*Questions:*{color}

# Where is the sent status stored for each report date?
# Can we confirm the expected result when the job is run again manually on the same Monday, both when the first run fully succeeded and when it partly failed (for example, one owner's email failed)?

*9.Change control for PROD*

Section 10 gives RW-SECADM CRUDA rights on flags, which includes "A" (Approve). However, the flow has no approval step: any RW-PLATADM can switch a flag in PROD with only a reason.

{color:#ff5630}*Questions:*{color}

# Do PROD flag changes need maker-checker approval, a change ticket reference, or a change window?
# If not, what is the "A" right of RW-SECADM used for in this story?

### Comment 2: Chanapai Gingpuwaluck, 2026-11-17T11:55:33.579+0700

Comment ID 1794302

These points add to the questions already on this card.

# *The weekly flag report has no run book.* FlagRemovalReportJob is a new Quartz job, but it is not among the 16 {{job_catalog}} rows in RWB-E1-056. RunbookCompletenessTest ("every Quartz job has a run book") will fail unless the job is added.
# *Front-end behaviour when the flag store is down.* The front end reads {{GET /feature-flags}} on page load, but the story does not say what it shows if the store is down. The 30-second cache is still an assumption under DL11, which is past due.
# *Allowed module names.* Please list the allowed {{<module>}} values (module code such as {{p3}}, or short name such as {{casewf}}), so that the key check has a fixed list.
# *Typo.* AC4 has a typo: "does not creat".

Who answers: Tech lead, Henka (BA).

### Comment 3: Nuttapon Jittachotisak, 2026-11-17T13:15:43.247+0700, edited 2026-11-17T18:27:05.134+0700

Comment ID 1794418

# Do you have feature_flag data to seeded into table or it will add on the while develop feature?
# PATCH /admin/feature-flags/{flagKey} would send version at the header?
# The scheduler is built later (RWB-TE-007, #26), and ACE has no e-mail service.
# What removal_date < today it just notice owner only? stay active, value still same?
# Several api are quite unclear and leave room for interpretation. For example:
This api is open to interpretation as meaning: 'Get an array of {{FeatureFlag}} where {{removalDate < today}}, along with the calculated {{daysOverdue}} derived from {{today - removalDate}}.'
I would like to have more description added to prevent misunderstandings

!image-20261117-112555.png|width=999,alt="image-20261117-112555.png"!


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
