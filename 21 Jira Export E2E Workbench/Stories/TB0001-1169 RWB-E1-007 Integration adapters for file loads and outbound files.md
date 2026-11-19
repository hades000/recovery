# TB0001-1169 [RWB-E1-007] Integration adapters for file loads and outbound files

| Field | Value |
|---|---|
| Jira | [TB0001-1169](https://scbjira.atlassian.net/browse/TB0001-1169) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Requirement, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:09.955+0700 |
| Updated | 2026-11-18T19:58:15.218+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 9 |
| Comments | 18 |

## Description

As a platform administrator (RW-PLATADM), I want one adapter pattern for every file load and outbound file, with file checks, a run log, retry and an exception queue, so that every later interface follows one pattern and a failed file is found on the day it fails.

## Acceptance criteria

```gherkin
Feature: Integration adapters for file loads and outbound files

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"

  Scenario: AC1 Pattern described
    Given a developer adds the file load "INT-15" WIN proof of delivery
    When the build pipeline runs
    Then the system declares the load as an interface configuration row and uses FileLoadAdapter
    Then the contract test "INT-15" parses the synthetic sample file of 120 records and passes
    Then the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter

  Scenario: AC2 File load checked
    Given a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201
    When the adapter loads it
    Then the system refuses the file in full with failed check "DQ-059 Control total"
    Then the system passes no collateral record to the loader
    Then the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale
    Then the system alerts the data steward with message MSG-P1-002

  Scenario: AC3 Retry and exception queue
    Given the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases
    Given the SFTP transfer fails on attempts 1, 2 and 3
    When the outbox sender runs
    Then attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2
    Then each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33)
    Then after attempt 3 the item status is "EXCEPTION"
    Then each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34)
    Then the item shows in the exception queue with message MSG-P2-001

  Scenario: AC4 Every file check runs before any record is used
    Given a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected
    When the adapter loads it
    Then the system refuses the file with failed check "DQ-057 Business date"
    Then the run row shows status "REFUSED" and record count 0

  Scenario: AC5 File missing at the cut-off
    Given no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00
    When JOB-09 runs
    Then the run row for "INT-11" shows status "MISSING"
    Then the system marks on 2026-11-10 the SVAF data product stale with message MSG-P1-001

  Scenario: AC6 Same file delivered twice
    Given the CCMS file for business date 2026-11-09 with hash "9f2c" was loaded at 04:05
    When the same file arrives again at 04:40
    Then the system writes a run row with status "DUPLICATE"
    Then the system passes no record to the loader

  Scenario: AC7 Duplicate application event ignored
    Given consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1"
    When the same event arrives again with the same key
    Then the consumer does not act
    Then the hit count for that key becomes 2 (R-UNI-40)

  Scenario: AC8 Two senders pick the same item
    Given outbound item "OB-0001" is due
    When two sender threads run at 10:00:00
    Then the system sends the file once
    Then the attempt count is 1

  Scenario: AC9 Resend from the exception queue
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    When a platform administrator resends it
    Then the item status is "PENDING" with attempt count 0
    Then the system writes the resend to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005
```

## Attachments

- [image-20261111-094548.png](../../Attachments/TB0001-1169/image-20261111-094548.png) (85047 bytes, NAMTIP WONGSOMBOON, 2026-11-11T16:45:51.792+0700)
- [image-20261111-100145.png](../../Attachments/TB0001-1169/image-20261111-100145.png) (269090 bytes, NAMTIP WONGSOMBOON, 2026-11-11T17:04:03.199+0700)
- [image-20261112-033153.png](../../Attachments/TB0001-1169/image-20261112-033153.png) (64028 bytes, Chanapai Gingpuwaluck, 2026-11-12T10:31:55.893+0700)
- [RWB-E1-007 Integration adapters for file loads and outbound files.txt](../../Attachments/TB0001-1169/RWB-E1-007%20Integration%20adapters%20for%20file%20loads%20and%20outbound%20files.txt) (45458 bytes, Pe Chichareon, 2026-11-15T10:14:40.652+0700)

## Comments (18)

### Comment 1: NAMTIP WONGSOMBOON, 2026-11-11T16:06:53.060+0700, edited 2026-11-11T17:04:03.191+0700

Comment ID 1785959

@CHANISSARA MAHAKITTIKUN 

!image-20261111-100145.png|width=439,alt="image-20261111-100145.png"!

As discussed during the Grooming session on 11 Nov 2026, 

Please provide the detailed specification and business rules in the User Story description, not in the Acceptance Criteria (AC). The ACs should focus on testable expected outcomes.

*Clarification Required – Specification*

Please provide the detailed FileCheckRunner specification in the User Story description, clearly defining:

# *Files to Validate:* Which files are required to be checked?
# *Fields to Validate:* Which fields or columns must be validated in each file?
# *Validation Rules:* What specific conditions and business rules must be applied to each field?
# *Expected Results:* What are the expected outcomes for each validation scenario, including success and failure cases?
# *Sample Files:* Please provide sample input files, including both valid and invalid data, with expected validation results.

Please provide a *file-by-file and field-by-field breakdown* of the validation rules to ensure DEV can proceed with Technical Design and Task generation without making assumptions.

The Acceptance Criteria (AC) should focus on testable expected outcomes, while the detailed validation rules must be documented in the User Story description. 


!image-20261111-094548.png|width=458,alt="image-20261111-094548.png"!

### Comment 2: NAMTIP WONGSOMBOON, 2026-11-11T16:45:39.973+0700, edited 2026-11-11T16:49:46.620+0700

Comment ID 1786116

@CHANISSARA MAHAKITTIKUN 

*AC2 File load checked*: the system alerts the data steward with message {{MSG-P1-002}}

*AC3 Retry and exception queue*: the item shows in the exception queue with message {{MSG-P2-001}}

*AC5 File missing at the cut-off*: the system marks on 2026-11-10 the SVAF data product stale with message {{MSG-P1-001}}

*AC9 Resend from the exception queue*: the response carries message {{MSG-GEN-005}}

*Clarification Required — Error Notification & Handling*

Please clarify the following for each error scenario:

# *API Response:* Is the error returned via API? If yes, please specify the API name.
# *Non-API Handling:* If not returned via API, how and where is the error communicated (Email, Application Log, or User Interface)?
# *Recipients:* Who should receive or be notified of each error?

Please confirm the error handling method for each scenario to support Technical Design and QA validation.

### Comment 3: NAMTIP WONGSOMBOON, 2026-11-11T17:01:29.394+0700

Comment ID 1786198

@CHANISSARA MAHAKITTIKUN  *DL-11* 

*Clarification Required — Non-Functional Targets*

Please provide the confirmed target values for each non-functional requirement, including availability, performance, and recovery (RTO/RPO).

For any target that has not yet been confirmed, please specify:

* The responsible owner
* The expected confirmation date
* The impact on Technical Design and Non-Functional Testing

These details are required to finalize the Non-Functional Specification, support the availability, performance, and recovery design, and establish measurable acceptance criteria for Non-Functional Testing.

### Comment 4: NAMTIP WONGSOMBOON, 2026-11-11T17:20:48.986+0700

Comment ID 1786331

@CHANISSARA MAHAKITTIKUN As discussed during the Grooming session on {{2026-11-11}},

For *Epic 1*, all *Job-xx* Execution scope will be removed from the existing User Stories and consolidated into a new User Story dedicated to Data Loading.

*The new Story scope must clearly define:*

* Jobs and related interfaces
* Trigger conditions and execution schedules
* Processing flows and dependencies
* Input/Output and Business Rules
* Error Handling and Expected Results

For *RWB-E1-007*, *JOB-09, JOB-10, and JOB-11* will be removed and moved to the new Story. All related dependencies and Acceptance Criteria (ACs) must be reviewed and updated accordingly.

### Comment 5: Chanapai Gingpuwaluck, 2026-11-12T10:31:56.039+0700, edited 2026-11-12T10:33:37.856+0700

Comment ID 1786968

@NAMTIP WONGSOMBOON According to
Decision from K.@PONGCHAI CHAROENRUNGRODKUN Henka must provide outbound path for E2E this job.

!image-20261112-033153.png|width=972,alt="image-20261112-033153.png"!

### Comment 6: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:00:18.141+0700

Comment ID 1790617

@NAMTIP WONGSOMBOON We have answer it via email and Team.

### Comment 7: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:00:29.389+0700

Comment ID 1790619

@NAMTIP WONGSOMBOON We have answer it via email and Team.

### Comment 8: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:00:39.765+0700

Comment ID 1790620

@NAMTIP WONGSOMBOON We have answer it via email and Team.

### Comment 9: CHANISSARA MAHAKITTIKUN, 2026-11-13T17:07:47.237+0700

Comment ID 1790644

@Chanapai Gingpuwaluck As per our discuss in pervious session we have  removed these jobs because of the recent discussion of using ACE(still under discussion).

### Comment 10: Pe Chichareon, 2026-11-15T10:14:40.867+0700

Comment ID 1791302

Due to Microsoft tool outage, Henka responded via email as txt file on 13 Nov 

[^RWB-E1-007 Integration adapters for file loads and outbound files.txt]



### Comment 11: NATAPATCHARA ANUROJE, 2026-11-17T01:38:50.662+0700

Comment ID 1793628

Read the full txt attachment (Henka's answer) properly now. It's not resolved; more open than I first thought.

* *FileCheckRunner stays in this story* (not removed) — Part D of the attachment has a full file-by-file, field-by-field spec, 4 check rules in fixed order, 23 sample files, and new ACs (4-9) replacing the old AC2/AC4. Our local v7 story file says "Removed in this version... moved to RWB-ACE-001" — that looks stale against this answer.
* *JOB-09/10/11* — the *execution* (schedule, job bodies) moves to the new Data Loading story (no key yet); the *classes* (incl. FileCheckRunner, OutboundFilesImpl, SftpTransport...) and 4 tables stay in RWB-E1-007 as "build only."
* *DL-11* — most NFR targets now have proposed values (ACE-based), but RPO/RTO (NFR-022/023) are still fully open, no value at all.
* The attachment itself raises its own "please confirm" list in each part — roughly 20 items total: file layouts for AMIS/RPS/GL (DEP-15, due date already passed), key/amount fields for those three, the retry-wait math (3 attempts of 5/15/45 min never uses the 45th), the stale-rule stated two different ways, the INT-14 outbound path and ack file name from Henka, whether checks stop at first failure or always run all four, and the new Data Loading story's own key/number.

Given that count, this still reads like it needs the Block/R-* labels, not fewer than before.

### Comment 12: Ratchadaphorn Kasemphin, 2026-11-17T11:48:28.802+0700

Comment ID 1794278

@CHANISSARA MAHAKITTIKUN 

cc. @Chitchaya Muanchonchana 

*Concerns (Dependencies):*

# *Story scope conflict.* Part D of the attachment keeps FileCheckRunner in this story. It gives a field-by-field spec for each file, 4 check rules in fixed order, 23 sample files, and new AC4–AC9 that replace the old AC2 and AC4. Our local v7 story file still says FileCheckRunner was "Removed in this version... moved to RWB-ACE-001", and the story-defects log closes its defects under D-RCV-35 U1. The story file has to be updated to match the attachment before specify can start.
# *Split with the new Data Loading story (no key yet).* Running JOB-09, JOB-10 and JOB-11 (schedule and job bodies) moves to the Data Loading story. RWB-E1-007 keeps only the build of the classes (FileCheckRunner, OutboundFilesImpl, SftpTransport, etc.) and the 4 tables. Without the job runs, nothing in this story can be tested end to end. That includes AC5, which needs a scheduled cut-off run.
# *DEP-15 file layouts for AMIS, RPS and GL are overdue.* The due date has passed. Without the layouts we cannot write the FileCheckRunner field checks or the sample files for these three sources.
# *DL-11 NFR.* Most targets now have proposed values based on ACE. RPO and RTO (NFR-022 and NFR-023) still have no value at all, which affects the retry, resend and recovery design.
# *Henka (INT-14).* We are still waiting for the outbound path and the ack file name. The SftpTransport config cannot be finished without them.
# *Schedule.* The build window for this story (Window 1, 2–13 Nov) has already passed. Several stories depend on it, including RWB-E1-056, RWB-TE-006, RWB-E1-002, RWB-E1-063, RWB-E2-001 and RWB-E2-007, so any delay moves them too.

----

*Clarification needed:*

*A. Business*

# *Scope.* Please confirm that the attachment replaces the v7 note that FileCheckRunner was removed. Please also confirm that RWB-ACE-001 no longer includes FileCheckRunner, DQ-057 or DQ-059, so the same work is not built twice.
# *Data Loading story.* We need its key and number, and its owner. Please also confirm the boundary: does RWB-E1-007 deliver only the classes and the 4 tables, while Data Loading owns the schedule, the job bodies and the job-run ACs?
# *Stale rule.* The attachment states the stale rule in two different ways. Which one is correct?
#* (a) The data product goes stale at the cut-off time on the day the file is due.
#* (b) The data product goes stale one business day after the file was due.
# *AMIS, RPS and GL layouts (DEP-15).* What is the new committed date? Please also confirm the key fields and amount fields for each of the three sources.
# *RPO and RTO (NFR-022 and NFR-023).* Please provide target values, or name the owner and a date.
# *INT-14 (Henka).* Please confirm the outbound path and the ack file name.

*B. Details in the ACs*

# *AC2 – File load checked.*
#* When one of the 4 checks fails, does the run stop there, or do all 4 checks always run and every failure get reported?
#* Is one result record written per check or per file?
# *AC3 – Retry and exception queue.* The settings are 3 attempts with waits of 5, 15 and 45 minutes, so the 45-minute wait is never used. Which is correct?
#* (a) 4 attempts (first send plus 3 retries)
#* (b) 3 attempts with waits of 5 and 15 minutes only
# Please also confirm whether the first send counts as attempt 1.
# *AC4–AC9 (new).* Please send the final AC numbering and text. They replace the old AC2 and AC4, so the test cases (TC-E1-007-xx) need to be mapped again.
# *AC5 – File missing at the cut-off.*
#* What is the cut-off time for each source?
#* Which business-day or holiday calendar applies?
#* Which data product code is SVAF?
#* When the late file arrives, is the stale flag cleared automatically?
# *AC9 – Resend from the exception queue.*
#* Does the resend send the same file as before, or build a new file from current ACE data?
#* Does the attempt count go back to 0?
# *Sample files (23).* Do they cover AMIS, RPS and GL, or only the sources whose layouts are already confirmed?

----

*Clarification Required — Error Notification & Handling*

Please answer the following for each error scenario:

* *API Response:* Is the error returned through an API? If yes, please give the API name.
* *Non-API Handling:* If not, how and where is the error shown (email, application log or user interface)?
* *Recipients:* Who should receive the error or be notified of it?

||AC||Scenario||Message||
|AC2|File load checked: the system alerts the data steward|MSG-P1-002|
|AC3|Retry and exception queue: the item shows in the exception queue|MSG-P2-001|
|AC5|File missing at the cut-off: the system marks the SVAF data product stale on 2026-11-10|MSG-P1-001|
|AC9|Resend from the exception queue: the response carries the message|MSG-GEN-005|

### Comment 13: Chanapai Gingpuwaluck, 2026-11-17T12:08:02.683+0700

Comment ID 1794338

These points add to the open items in Henka's answer and the questions already on this card.

# *One transport failure creates 85 tasks.* In AC3, one SFTP failure moves 85 cases to RETRY_QUEUE and creates one RW-PLATADM task per case.
#* Proposal: one task per file or item, and no case state change for a transport failure.
# *AC4 uses a Saturday.* The previous stamp for business date Tue 10 Nov should be Mon 9 Nov, but AC4 uses 2026-11-07, which is a Saturday.
# *WIN files carry personal data.* The story does not state the retention class or the file encryption (PGP). The INT-14 path is already asked above; INT-19, INT-20 and INT-25 also name no transport (File Hub, feedback #68).
# *Flag off behaviour.* The readiness check depends on {{v_ace_batch_status}}.
#* Question: with the flag off, are files built unchecked or not at all?
# *Hit count differs from RWB-E1-015.* AC5 counts a duplicate as hit 2, while RWB-E1-015 AC5 has {{duplicate_count}} = 1 (R-UNI-40). Please use one meaning.

Who answers: Integration architect, Henka (BA), Security, Compliance.

### Comment 14: VAISHNAVI KAULGE, 2026-11-17T18:31:56.531+0700

Comment ID 1795609

@Ratchadaphorn Kasemphin 

h2. A. Business clarifications

# *FileCheckRunner / duplicate work — mostly confirmed.*
The current {{RWB-E1-007 story}} explicitly removes the inbound {{FileCheckRunner}}, {{DQ-057}}, {{DQ-059}}, inbound folder checks and load jobs from E1-007. The {{Data Load Story Removals v2 note}} says source ingestion moves to ACE under {{RWB-ACE-001}}.
*Caveat:* the documents establish that E1-007 no longer builds those checks, but I can’t confirm that ACE itself will not use those class or rule names. That needs confirmation from the ACE story owner.
# *Data Loading key, owner and boundary.*
The cited key is {{RWB-ACE-001}}, owned by the *ACE team*; I found no separate “Data Loading” story key. The current E1-007 is *not* “classes plus four new tables”: it is outbound-only and says there are no new tables for this story; its five P2 tables already exist in {{RWB-E1-001}}. E1-007 still covers its outbound jobs and retry flow. ACE owns inbound source ingestion, its checks and scheduling.
# *Stale rule.*
The old “one business day after file due” rule and the old missing-file AC are removed from E1-007. The current story holds outbound generation until the ACE batch is {{COMPLETE}}; it does not mark a source data product stale for a missing inbound file. The ACE/P1 freshness process must define the applicable stale timing.
# *DEP-15 date and fields.*
I found the prior DEP-15 date *13 November*, but no replacement committed date. The interface specification lists these fields:
#* *AMIS (INT-12):* {{Asset ID}}, {{Asset Code}}, transfer/type fields, {{Book Value}}, {{Auction Purchase Price}}, sale fields and taxes/fees. {{Asset ID}} looks like the likely key, but the final key is not explicitly confirmed.
#* *RPS (INT-13):* {{AccNo}}, {{ContractNo}}, repossession/status fields and {{OutBal}}. The source does not identify which field(s) form the definitive key.
#* *GL (INT-16):* {{DATE}}, {{RC}}, {{OC}}, {{ACCOUNT}}, {{PRODUCT}}, {{EVENT}}, {{AMT}}. {{AMT}} is the amount field; the natural key is not confirmed.
# *RPO/RTO.*
No target values are set. The named owner is the *IT lead with Operational Risk*; the documents say to resolve them before resilience testing but give no calendar date. See the {{NFR specification}}.
# *INT-14 (WIN).*
The current story shows an outbound SFTP path using environment/configuration values and gives {{WIN_NOTICE_20261110.txt}} as an example filename. It does *not* specify a committed SFTP folder/path or acknowledgment filename. The {{WIN proof-of-delivery story}} describes acknowledgment contents—contract number, sent date, barcode and sent type—but not the filename.
# *23 sample files.*
The current E1-007 acceptance tests do not establish that the 23 files cover AMIS, RPS and GL. They cover outbound cases such as WIN and INT-25; inbound samples now belong with ACE ingestion. Coverage of those three sources needs to be confirmed in {{RWB-ACE-001}}’s layout/test-data list.

h2. B. Acceptance criteria and tests

* *AC2 “File load checked”* is no longer an E1-007 criterion. Current AC2 is “Outbound file reads ACE only through the views.” The inbound check and {{MSG-P1-002}} scenario moved out of this story.
* *AC3 retries:* the current AC explicitly treats attempts 1, 2 and 3 as the three sends, so *the first send counts as attempt 1*. The 5- and 15-minute waits are used; the 45-minute wait is not. If three attempts is fixed, the config should contain only {{[5, 15]}}. If all three waits are intended, the maximum must be four attempts. The source doesn’t decide between those options.
* *Current AC numbering and test mapping* in v7:
{{TC-E1-007-05}} (missing file) and {{TC-E1-007-06}} (duplicate inbound file) are retired with inbound loading. {{TC-E1-007-10}} covers access control. Thus, the requested old “AC9 resend” is *AC7* now.

||Current AC||Scenario||Test case||
|AC1|One outbound pattern|{{TC-E1-007-01}}|
|AC2|Read ACE through views only|{{TC-E1-007-02}}|
|AC3|Retry and exception queue|{{TC-E1-007-03}}|
|AC4|Hold outbound file until ACE batch is complete|{{TC-E1-007-04}}|
|AC5|Ignore duplicate application event|{{TC-E1-007-07}}|
|AC6|Prevent duplicate send by two sender threads|{{TC-E1-007-08}}|
|AC7|Resend from exception queue|{{TC-E1-007-09}}|

h2. Error notification and handling in the current story

||Scenario from your list||Current handling||API, display and recipient||
|*Old AC2: inbound file check /* {{MSG-P1-002}}|Removed from E1-007.|No E1-007 API or recipient is specified for the ACE-side check; that must be specified by {{RWB-ACE-001}}.|
|*Current AC3: retry /* {{MSG-P2-001}}|Background SFTP retries; after the limit, item enters the exception queue and a task is raised. {{MSG-GEN-006}} is used during retry; {{MSG-P2-001}} on exception.|Not an API response. Shown in the exception queue; task goes to {{RW-PLATADM}}. The story also says the data steward receives failed-file email from Log Analytics, so whether both notifications are intended should be confirmed.|
|*Old AC5: missing-file stale alert /* {{MSG-P1-001}}|Removed from E1-007. The current *AC4* is an outbound hold when the ACE batch is incomplete.|Not an API response. There is a recipient mismatch: AC4 says the platform administrator receives {{MSG-P1-001}}, while the authority/notification sections say the data steward receives the held-file alert by email. This needs a decision.|
|*Old AC9 / current AC7: resend /* {{MSG-GEN-005}}|Resend resets the item to {{PENDING}}, attempt count {{0}}, and audits user/time.|*Yes:* {{POST /admin/outbound-items/{itemId}/resend}} with {{If-Match}}. The story says the response carries {{MSG-GEN-005}}. It also lists {{401}}, {{403}}, {{404}}, {{409}} and {{503}} error cases.|

So, the main unresolved confirmations are: ACE’s exact class/rule naming and ownership, the retry interval choice, held/failed alert recipients, final source layouts and sample coverage, the INT-14 acknowledgment filename/path, and RPO/RTO targets/date. No files were edited.

### Comment 15: VAISHNAVI KAULGE, 2026-11-17T18:37:04.497+0700

Comment ID 1795625

@Chanapai Gingpuwaluck 

# *One transport failure creates 85 tasks* (Integration architect and Product Owner to confirm)

We agree. The INT-14 spec says "after the third failure raise a task to the owning team", which is one task.

* *Proposal:*
** A transport failure belongs to the file, not to the cases.
** The outbound item carries the status (RETRY, then EXCEPTION), and the exception queue (SCR-09) plus the alert is the owner's work item.
** The 85 cases keep their route state.
* *Task table:* {{task.case_id}} is NOT NULL today, so a task for one file can't exist without a case. Either we make the case link optional and add an item reference, or we use the exception queue alone. We recommend the exception queue alone.
* *Rules to confirm:* R-UNI-33 and R-UNI-34 are written as case-level rules, so someone has to confirm they apply to a file transfer. If the business needs the cases marked, keep the case state change but still raise one task per file.
* *Story changes:*
** AC3, X2, X3 and section 9 change to "one item, one alert".
** BR4 and BR6 are reworded accordingly.

# *AC4 uses a Saturday* (Product Owner and data steward to answer)

* *Date fix:* 2026-11-07 is a Saturday. The previous stamp for Tuesday 10 Nov is Monday 9 Nov, so AC4 changes to 2026-11-09. The same fix applies to the held reason, the MSG-P1-001 example text and TC-E1-007-04.
* *Calendar rule:* the previous business date comes from the bank holiday calendar (v_ace_holiday), not from "minus 1 day". We add that to BR3.

# *WIN files carry personal data* (Security, Compliance and Integration architect to answer)

* *Gap:* the INT-14 file holds addressee and address. The story states no retention class and no encryption. BR10 only covers the outbound item, not the file. Interface Specifications v2 does not mention PGP or the transport for INT-19, INT-20 and INT-25.
* *Proposals:*
** Add two interface configuration fields: {{encryption}} (NONE or PGP) and {{retention_class}}.
** The file is encrypted with PGP for the receiver before the SFTP send, and the clear file is not kept.
** INT-14 is encrypted and uses a legal retention class (LEGAL10Y, assumed until DL26).
** INT-25 follows the sale terms. INT-19 and INT-20 carry case and decision data with no addressee.
** A send is refused if no key is set.
* *Questions to answer:* the transport (File Hub or SFTP), the key owner and the retention class for each of INT-14, INT-19, INT-20 and INT-25.
* *Story changes:* add an acceptance criterion for the encryption and refusal, and put the transport and encryption into each interface row.

# *Flag off: files built unchecked or not at all?* (Product Owner and Integration architect to answer)

* *Recommendation: not at all for INT-14 and INT-25.*
** A demand notice or a debt buyer tape built on unchecked arrears data can reach the wrong customer or buyer.
** With the flag off, {{v_ace_batch_status}} does not exist yet (DL43). The request is held, no file is built, and the platform administrator and data steward get MSG-P1-001.
* *INT-19 and INT-20:* these are reporting files with no addressee that are re-run every night. They may be built unchecked, with the item marked "readiness unchecked". Please confirm.
* *Trade-off:* no WIN file goes out until RWB-ACE-001 lands. If the business can't accept that, the data steward confirms readiness by hand for a day, as a separate decision.
* *Story changes:* one acceptance criterion, "flag off: INT-14 held, no outbound item", plus a statement in section 3.

# *Hit count differs from RWB-E1-015* (Integration architect to answer)

* *Where they differ:* E1-007 AC5 says the hit count becomes 2, because {{processed_event.hit_count}} starts at 1. E1-015 AC5 says {{duplicate_count}} 1, because that column starts at 0.
* *Proposal:* one meaning everywhere, namely the number of repeats ignored, starting at 0.
** {{processed_event.hit_count}} becomes {{duplicate_count}}, with default 0.
** AC5 then says 1 for one repeat, as in E1-015.
** The Physical Schema v6 and the dictionary (DF-OPS-182) change to match.

### Comment 16: VAISHNAVI KAULGE, 2026-11-17T18:44:38.931+0700

Comment ID 1795634

@NATAPATCHARA ANUROJE 

*Status:* the attachment predates the ACE re-base (D-RCV-35, 15 Nov). The current story (Project Hub v17, Epic 1 v8) is outbound-only. FileCheckRunner, FileLoadAdapter, JOB-09 and {{interface_run}} are removed, and their home is ACE ingestion (RWB-ACE-001).

*Your points*

# *FileCheckRunner:* it is not kept in E1-007. We hand the Part D spec and the 23 sample files to RWB-ACE-001 as the starting input for the ACE ingestion checks.
# *JOB-09/10/11:* JOB-09 is obsolete. JOB-10 and JOB-11 stay in E1-007 as outbound jobs, so no separate Data Loading story is needed.
# *DL-11:* RPO and RTO still have no value. This is platform-wide, not specific to E1-007.
# *Open questions:* about 30 were raised. 17 are closed by the re-base or by v8, and 2 are duplicates. 11 remain open and 3 of them block E1-007.

*Blocking E1-007*

||#||Item||Owner||
|B1|INT-14 outbound path: DEV and SIT SFTP folder, write access for the service identity ({{recovery_svc}} in v8), and the acknowledgment folder and file name.|Delivery team|
|B2|Retry: 3 attempts with waits of 5, 15 and 45 minutes never uses the 45. We recommend 4 attempts (NFR-026 "three retries").|Integration architect|
|B3|One task per failed file instead of one per case (85 tasks today).|Integration architect, Product Owner|

*Open, not blocking*

* The 30-minute resend wait is assumed under DL11. It is a configuration value.
* The resend response carries no message code, but AC7 says it does. We either add a message field or change the AC.
* MSG-P2-001 and MSG-GEN-005 are missing from the SCR-09 message list.

*Open, platform level* (Epic 1 go-live gate, not the E1-007 build):

* RPO and RTO values.
* Whether DL-11 option A is approved.
* The change window.
* The document backup schedule.
* The two extra test pass marks.

*Raised separately on this card:*

* The encryption, retention class and transport for INT-14, INT-19, INT-20 and INT-25.
* The flag-off behaviour.
* The Saturday date in AC4.
* The hit-count meaning.

### Comment 17: Chanapai Gingpuwaluck, 2026-11-18T17:14:18.067+0700

Comment ID 1797449

@VAISHNAVI KAULGE Thank you for the replies. The AC4 date fix (2026-11-09, previous business date from v_ace_holiday) closes that point. The other four are proposals that still need a decision, and five related points are not yet covered.

# *Decisions still needed on the proposals.*
#* One task per failed file (B3): Integration architect and PO choose between the exception queue alone and an optional task.case_id with an item reference, and confirm whether R-UNI-33 and R-UNI-34 apply to a file transfer.
#* WIN personal data: Security and Compliance confirm the transport, key owner and retention class for INT-14, INT-19, INT-20 and INT-25. Proposal: no INT-14 file is sent until PGP and the retention class are in place, since the file holds names and addresses.
#* Flag off: PO confirms that no INT-14 or INT-25 file is built until RWB-ACE-001 lands. RWB-ACE-001 has no ticket and DL43 is open, so this means no WIN notice from the Workbench on the 30 Nov release unless the manual readiness option is approved.
#* Hit count: see point 2.
# *Renaming hit_count affects RWB-E1-067.* processed_event is shared. RWB-E1-067 X1, X5 and AC3 count a "hit", and its section 13 creates processed_event again with first_interaction_id and last_hit_at (also raised on TB0001-1228). Please change both stories and Physical Schema v6 in one decision by the schema owner.
# *One retry rule for the module.* The 4-attempt proposal (B2) matches RWB-E1-067 AC5 ("tried 4 times in all", NFR-026). The waits differ: SFTP 5, 15 and 45 minutes, outbox (RWB-TE-006) 1, 5 and 15 minutes. Please confirm the difference is intended and that both are configuration values.
# *Notification recipients.* For a held or failed file, AC4 names the platform administrator, the authority section names the data steward, the flag-off proposal names both, and the data steward also gets a Log Analytics email. Please state one recipient list and one channel for each case (held, failed after retries).
# *Story version.* The replies refer to Project Hub v17 and Epic 1 v8 (outbound-only). The attachment on this card (15 Nov) predates the re-base. Please attach the v8 story text so QA and SA review the same ACs and test IDs.

Who answers: Integration architect, PO, Security, Compliance, Data architect (schema owner).

### Comment 18: VAISHNAVI KAULGE, 2026-11-18T19:57:39.407+0700

Comment ID 1797795

h2. Q01 Decisions still needed on the proposals

*Question (from the comment):*

* One task per failed file (B3): Integration architect and PO choose between the exception queue alone and an optional task.case_id with an item reference, and confirm whether R-UNI-33 and R-UNI-34 apply to a file transfer.
* WIN personal data: Security and Compliance confirm the transport, key owner and retention class for INT-14, INT-19, INT-20 and INT-25. Proposal: no INT-14 file is sent until PGP and the retention class are in place.
* Flag off: PO confirms that no INT-14 or INT-25 file is built until RWB-ACE-001 lands. RWB-ACE-001 has no ticket and DL43 is open, so this means no WIN notice from the Workbench on the 30 Nov release unless the manual readiness option is approved.
* Hit count: see point 2.

*Answer (RECOMMENDATION, Henka will answer):*

* *One task per failed file (B3).* INT-14 says "raise a task to the owning team", which is one task. In Physical Schema v6 {{task.case_id}} is NOT NULL, so a task for one file cannot exist without a case. Option a: the exception queue alone (SCR-09 and the alert are the owner's work item, and the 85 cases keep their route state). Option b: keep the case state change and raise one task per file, which needs {{task.case_id}} to be optional with an item reference. Recommendation: option a. No document says whether R-UNI-33 and R-UNI-34 (case-level rules) apply to a file transfer. Henka will answer.
* *WIN personal data.* Interface Specifications v3 name no encryption and no transport for INT-14, INT-19, INT-20 and INT-25. Records Retention v2 gives "Legal actions and notices" 10 years after the legal action ends, with archive after 2 years, the nearest class for INT-14. DL26 (retention and masking, Compliance) is open in Decision Log v10. Recommendation: no INT-14 file is sent until PGP and the retention class are in place. Henka will answer the transport, the key owner and the retention class.
* *Flag off.* The readiness check reads {{v_ace_batch_status}}, which exists only after RWB-ACE-001 (DL43, open in Decision Log v10). RWB-ACE-001 has no Jira key in the document set. Recommendation: with the flag off, INT-14 and INT-25 are not built; INT-19 and INT-20 (reporting files, no addressee) may be built marked "readiness unchecked". So no WIN notice leaves the Workbench for the 30 Nov release unless the data steward confirms readiness by hand. Henka will answer.
* *Hit count.* See Q02.

h2. Q02 Renaming hit_count also affects RWB-E1-067

*Question (from the comment):* processed_event is shared. RWB-E1-067 X1, X5 and AC3 count a "hit", and its section 13 creates processed_event again with first_interaction_id and last_hit_at (also raised on TB0001-1228). Please change both stories and Physical Schema v6 in one decision by the schema owner.

*Answer (RECOMMENDATION, Henka will answer):* Physical Schema v6 defines {{processed_event}} with {{idempotency_key}}, {{event_id}}, {{hit_count}} (default 1) and {{last_seen_at}}. RWB-E1-067 section 13 defines the table again (idempotency key as primary key, {{first_interaction_id}}, {{hit_count}}, {{last_hit_at}}). RWB-E1-015 uses {{duplicate_count}} (default 0). Recommendation: one meaning of the count ("repeats ignored, starting at 0") and one definition of the table for RWB-E1-007, RWB-E1-015 and RWB-E1-067, with Physical Schema v6 as the single source. Where to look: {{06 Data/Recovery Workbench Physical Schema v6.sql}}. Henka will answer who owns the schema decision.

h2. Q03 One retry rule for the module

*Question (from the comment):* The 4-attempt proposal (B2) matches RWB-E1-067 AC5 ("tried 4 times in all", NFR-026). The waits differ: SFTP 5, 15 and 45 minutes, outbox (RWB-TE-006) 1, 5 and 15 minutes. Please confirm the difference is intended and that both are configuration values.

*Answer (RECOMMENDATION):* The waits differ because the channels differ: SFTP 5, 15 and 45 minutes (RWB-E1-007) and the outbox 1, 5 and 15 minutes (RWB-TE-006, section 3: "3 retries at 1, 5 and 15 minutes after the previous attempt (assumed; NFR-026, DL11)"). Both are marked as assumed under DL11. Recommendation: the same number of attempts for both, with each channel's waits kept as configuration values. Henka will answer whether the difference is intended.

h2. Q04 Recipients for a held or failed file

*Question (from the comment):* For a held or failed file, AC4 names the platform administrator, the authority section names the data steward, the flag-off proposal names both, and the data steward also gets a Log Analytics email. Please state one recipient list and one channel for each case (held, failed after retries).

*Answer (RECOMMENDATION, Henka will answer):* Today the documents give:

* *Held file (MSG-P1-001).* AC4 names the platform administrator. The authority and notification sections name the data steward. The flag-off proposal names both.
* *Failed after retries (MSG-P2-001).* A task to RW-PLATADM and an exception queue item in SCR-09. The data steward also gets a Log Analytics email on {{rwb.integration.outbound.failed}}.

Recommendation: held file, the platform administrator and the data steward, through the Log Analytics alert. Failed after retries, RW-PLATADM through the SCR-09 item and task, and the data steward by email. Where to look: {{05 Technical architecture/}} (Observability and Monitoring Design v3, alert rules). Henka will answer the final list.

h2. Q05 Which story version QA and SA review

*Question (from the comment):* The replies refer to Project Hub v17 and Epic 1 v8 (outbound-only). The attachment on this card (15 Nov) predates the re-base. Please attach the v8 story text so QA and SA review the same ACs and test IDs.

*Answer (REFERENCE, Henka will answer):* The current E1-007 text in the document set is {{04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 007 Integration adapters for file loads and outbound files v1.md}}, dated 15 Nov. The same text is in Epic 1 v9. The attachment on the card (Henka's answer of 13 Nov) predates the ACE re-base (D-RCV-35). "Project Hub v17 and Epic 1 v8" do not match the file names in the set. Henka will answer which version is the review baseline.


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
