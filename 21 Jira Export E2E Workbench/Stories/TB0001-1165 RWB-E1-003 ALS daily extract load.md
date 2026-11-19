# TB0001-1165 [RWB-E1-003] ALS daily extract load

| Field | Value |
|---|---|
| Jira | [TB0001-1165](https://scbjira.atlassian.net/browse/TB0001-1165) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Non-Block, R-Requirement |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-05T12:37:06.567+0700 |
| Updated | 2026-11-18T17:18:01.593+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 3 |
| Comments | 5 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want ALS balances, arrears, payments and classification loaded every working day from the COLLINS daily batch for accounts at 90 days past due or more, so that account and arrears data is current to the previous working day.

## Acceptance criteria

```gherkin
Feature: ALS daily extract load

  Background:
    Given the expected business date is 2026-11-30 and the previous completed load is for 2026-11-27
    Given the mapping version "ALS-MAP-1" for INT-01 and INT-02 is approved
    Given the parameters load.hold.tolerance.pct = 0.50 and load.movement.tolerance.pct = 10.00 are in force

  Scenario: AC1 Daily load
    Given COLLINS completed the staging records for 2026-11-30 at 04:40 with 184,500 INT-01 accounts and 2,310 INT-02 payments, each with a matching trailer
    When JOB-01 runs at 05:00
    Then loan_account holds 184,500 rows with data_as_of 2026-11-30 before 07:00
    Then the load_run for INT-01 shows 184,500 read, 184,500 loaded and 0 held, with status COMPLETED
    Then the load_run for INT-02 shows 2,310 read, 2,310 loaded and 0 held
    Then one LoadCompleted event is in the outbox for each interface with business date 2026-11-30

  Scenario: AC2 Failure alerts
    Given the INT-01 trailer states 184,500 records and the staging holds 184,498
    When JOB-01 runs
    Then the system refuses the INT-01 load at DQ-003 and no loan_account row changes
    Then loan_account keeps data_as_of 2026-11-27
    Then the data steward and platform administrator groups receive MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: control total. The previous load is still in use."
    Then one LoadRefused event is in the outbox with failedCheck "DQ-003"

  Scenario: AC3 Sample matches
    Given the INT-01 load for 2026-11-30 is complete
    When the sample check picks 50 accounts at random
    Then for all 50 the total_balance, days_past_due and classification equal the INT-01 staging values after mapping
    Then the load_run check results show "SAMPLE" = "50 of 50"

  Scenario: AC4 Wrong business date
    Given the INT-01 staging records and trailer carry business date 2026-11-27
    When JOB-01 runs for 2026-11-30
    Then the system refuses the load at DQ-001 with MSG-P1-002 naming "business date"
    Then no loan_account row changes

  Scenario: AC5 Duplicate account key
    Given account key "ACC0000017" appears twice in the INT-01 staging records
    When JOB-01 runs
    Then the system refuses the load at DQ-004 with MSG-P1-002 naming "keys"
    Then no loan_account row changes

  Scenario: AC6 Unmatched payments within the tolerance are held
    Given 11 of the 2,310 INT-02 payments name an account key not in loan_account, which is 0.48 percent
    When JOB-01 runs
    Then the system writes 2,299 payments to account_payment
    Then the system writes 11 dq_exception rows with check code "DQ-012", the account key and raised_on 2026-11-30
    Then the INT-02 load_run shows 11 held and status COMPLETED

  Scenario: AC7 Unmatched payments above the tolerance refuse the load
    Given 13 of the 2,310 INT-02 payments name an account key not in loan_account, which is 0.56 percent
    When JOB-01 runs
    Then the system refuses the INT-02 load at DQ-012 with MSG-P1-002
    Then the system writes no account_payment row for 2026-11-30

  Scenario: AC8 Code missing from the code map is held
    Given 3 INT-01 records carry bucket code "Z9", which is not in the code map for LOV-BUCKET
    When JOB-01 runs
    Then the system holds the 3 records in dq_exception with check code "DQ-006"
    Then the system loads 184,497 accounts

  Scenario: AC9 Movement outside the expected range
    Given the previous load for 2026-11-27 held 165,000 accounts and the load for 2026-11-30 holds 184,500, a change of 11.82 percent
    When JOB-01 runs
    Then the system loads the accounts
    Then the data steward group receives MSG-P1-006 "The INT-01 load for 2026-11-30 changed by 11.82 percent against the previous load, outside the expected 10.00 percent. Check it before use."
    Then a change of exactly 10.00 percent sends no alert

  Scenario: AC10 Late delivery
    Given COLLINS has not completed the INT-01 staging records for 2026-11-30 by 09:00
    When the last JOB-01 attempt runs at 09:00
    Then the INT-01 load_run status is LATE and loan_account keeps data_as_of 2026-11-27
    Then one LoadRefused event is in the outbox with failedCheck "LATE"
    Then the data steward group receives MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: no delivery by 09:00. The previous load is still in use."

  Scenario: AC11 Rerun of a completed load
    Given the INT-01 load for 2026-11-30 is COMPLETED
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for that load
    Then the response is 409 with MSG-P1-011 "The INT-01 load for 2026-11-30 is already complete or running. It was not run again."
    Then no loan_account or load_run row changes

  Scenario: AC12 Two runs at the same time
    Given two ACE nodes fire JOB-01 for 2026-11-30 at 05:00
    When both start
    Then one load_run row exists for INT-01 and 2026-11-30
    Then loan_account holds 184,500 rows with no duplicate account_no

  Scenario: AC13 Database failure during the write
    Given the database connection is cut after 90,000 of 184,500 accounts are written in the transaction
    When the write step fails
    Then no loan_account row carries data_as_of 2026-11-30
    Then the load_run status is FAILED
    Then the attempt at 06:00 loads 184,500 accounts and sets the status to COMPLETED

  Scenario: AC14 Rerun after a refused load
    Given the INT-01 load for 2026-11-30 was refused at DQ-003
    Given COLLINS has delivered corrected staging records with a matching trailer
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for that load
    Then the response is 200 with a Job of status RUNNING
    Then the load completes with 184,500 accounts and one LoadCompleted event is in the outbox
```

## Comments (5)

### Comment 1: NAMTIP WONGSOMBOON, 2026-11-11T08:45:56.915+0700, edited 2026-11-11T09:03:36.585+0700

Comment ID 1784512

@CHANISSARA MAHAKITTIKUN  How are {{load.hold.tolerance.pct}} (0.50) and {{load.movement.tolerance.pct}} (10.00) calculated? Could you please provide the formulas, calculation examples, and rounding rules (decimal precision and rounding method) for each?

### Comment 2: NAMTIP WONGSOMBOON, 2026-11-11T08:59:46.375+0700, edited 2026-11-11T16:49:23.823+0700

Comment ID 1784520

@CHANISSARA MAHAKITTIKUN 

*Clarification Required — Error Notification & Handling*

Please clarify the following for each error scenario:

# *API Response:* Is the error returned via API? If yes, please specify the API name.
# *Non-API Handling:* If not returned via API, how and where is the error communicated (Email, Application Log, or User Interface)?
# *Recipients:* Who should receive or be notified of each error?

Please confirm the error handling method for each scenario to support Technical Design and QA validation.

### Comment 3: Pe Chichareon, 2026-11-11T15:56:35.444+0700

Comment ID 1785923

From requirement grooming 11 Nov afternoon session,

  The content (Action Item, AC) that unable to complete in current sprint should separate into new story.

  Only content (Action Item, AC) that can complete in sprint should be in this story.

### Comment 4: Pe Chichareon, 2026-11-13T14:56:48.156+0700

Comment ID 1790095

ANSWER from Henka

Both parameters are percentages (DECIMAL, two decimals). They are held as

data and never written in code. Both values are assumed (decision DL25)

until you confirm them.

# load.hold.tolerance.pct = 0.50

----

Purpose: limits how many records can be held out of a load before the whole

interface is refused.

Formula (per interface, per run):

held_pct = held records / rows read x 100

Held records are those failing:

* DQ-005 (reference) or DQ-006 (code map) on INT-01
* DQ-012 (account key not in loan_account) on INT-02

Rule:

* held_pct at or below 0.50: held records are written to dq_exception and
the rest of the records load.
* held_pct above 0.50: the whole interface is refused and no row is
written.
* Exactly 0.50 percent counts as within tolerance (the check is "greater
than", not "greater than or equal").

Examples:

  a) 11 of 2,310 INT-02 payments have an unknown account key

    11 / 2,310 x 100 = 0.4762 percent (shown as 0.48)

    Result: within tolerance. 2,299 payments load, 11 DQ-012 rows are

    held, status COMPLETED.

  b) 13 of 2,310 payments have an unknown account key

   13 / 2,310 x 100 = 0.5628 percent (shown as 0.56)

   Result: above tolerance. INT-02 is refused at DQ-012, no payment row

   is written, MSG-P1-002 is sent.

  c) Boundary: 5 of 1,000 records held

   5 / 1,000 x 100 = 0.5000 percent

   Result: within tolerance. 5 held, the rest load.

For 2,310 payments the most that can be held is 11. A 12th gives 0.5195

percent and refuses the load.

# load.movement.tolerance.pct = 10.00

----

Purpose: limits how much a load may change against the previous completed

load of the same interface (DQ-007 for INT-01, DQ-014 for INT-02).

Formula:

{noformat}movement_pct = |current - previous| / previous x 100{noformat}

"Previous" is the last COMPLETED load for the same interface. For business

date 2026-11-30 that is the load for 2026-11-27.

Rule:

* movement_pct above 10.00: the load still completes (nothing is held
back) and MSG-P1-006 is sent to the data steward group.
* movement_pct at or below 10.00: no alert is sent.
* Exactly 10.00 percent sends no alert.

Examples:

  a) Previous load 165,000 accounts, current load 184,500 accounts  |184,500 - 165,000| = 19,500

 19,500 / 165,000 x 100 = 11.8182 percent (shown as 11.82)

 Result: above 10.00. Load completes and MSG-P1-006 is sent.

  b) Boundary: previous 165,000, current 181,500 

 16,500 / 165,000 x 100 = 10.0000 percent

 Result: no alert.

# Rounding rules (PROPOSED - not yet in the story)

----

  Counts .................. Whole numbers, no rounding.

  Calculation ............. Exact decimal arithmetic, no floating point.

  Decision ................ Pass, refuse or alert is decided on the UNROUNDED value, by cross-multiplication. For example, hold passes when held x 100 <= tolerance x rows read. A value of 0.504 percent is therefore above 0.50.

  Displayed / alert values  2 decimal places, round half up (0.005 rounds up). This matches the parameter precision (0.50, 10.00) and the story figures (0.48, 0.56, 11.82).

  Balance totals .......... THB with 2 decimals, never rounded before the comparison.

  Audit trail ............. Row counts are stored on load_run, so any percentage can be recomputed.

  No previous load ........ The movement check is marked NOT_APPLICABLE.

PLEASE CONFIRM:

# Should decisions use the unrounded value (our proposal) or the
2-decimal rounded value?
# Should movement be judged on record count, on balance total, or on
either one exceeding the limit?

### Comment 5: Pe Chichareon, 2026-11-13T14:58:54.789+0700

Comment ID 1790101

ANSWER from Henka

The load runs as a scheduled job (CollinsLoadJob, 05:00 Asia/Bangkok on

working days, hourly retry to 09:00) with no screen. Only the rerun endpoint

returns an API response. Everything else is communicated through:

* ACE notification path: MSG-P1-002 and MSG-P1-006, sent to recipient
groups held in reference data and set per environment by the platform
administrator.
* load_run and dq_exception records, read through GET /admin/jobs and
GET /admin/data-quality/exceptions (need Platform administration R).
* Event outbox: LoadRefused (EV-27) and LoadCompleted (EV-26).
* Application log: the message ID and rule ID go to the log (Error and
Message Standard).

Scenario 1 - Business date wrong (DQ-001), structure bad (DQ-002), control

total mismatch (DQ-003), duplicate account key (DQ-004), or mapping version

not approved

  API response ... No (scheduled job).

  Handling ....... Whole load refused, nothing written, previous data stays in use. load_run is REFUSED with failed_check set. LoadRefused goes to the outbox. MSG-P1-002 is sent through the ACE notification path.

  Recipients ..... Data steward group and platform administrator group.

Scenario 2 - Held records above 0.50 percent (DQ-012, DQ-005, DQ-006)

  API response ... No.

  Handling ....... Same as scenario 1: the interface is refused in full.

  Recipients ..... Data steward and platform administrator groups (assumed same as scenario 1; the AC does not name them).

Scenario 3 - Held records within 0.50 percent (including a code missing from

the code map, DQ-006)

  API response ... No.

  Handling ....... Records are written to dq_exception. The load completes. load_run.rows_held shows the count. NO alert is sent.

  Recipients ..... None pushed. The data steward and platform administrator read the list through the admin endpoints.

Scenario 4 - Movement above 10.00 percent

  API response ... No.

  Handling ....... Load completes. MSG-P1-006 is sent through the ACE notification path.

  Recipients ..... Data steward group.

Scenario 5 - Late delivery (no complete delivery by 09:00)

  API response ... No.

  Handling ....... load_run is LATE and the previous data stays in use. LoadRefused with failedCheck LATE goes to the outbox. MSG-P1-002 ("no delivery by 09:00") is sent. RWB-E1-015 then marks DP01 stale.

  Recipients ..... Data steward group (as written in the AC). Whether the platform administrator is also included is to be confirmed.

Scenario 6 - Database failure during the write

  API response ... No.

  Handling ....... Whole interface is rolled back. load_run is FAILED. The next hourly attempt retries the load.

  Recipients ..... NOT YET DEFINED (see confirmation 2 below).

Scenario 7 - Rerun of a load that is already COMPLETED or RUNNING

  API response ... Yes. POST /admin/jobs/{jobId}/rerun returns 409 (application/problem+json) with MSG-P1-011.

  Handling ....... Nothing changes in load_run or loan_account.

  Recipients ..... The calling administrator, in the response.

Scenario 8 - Rerun by a caller without Platform administration U

  API response ... Yes. 403 with MSG-P4-002.

  Handling ....... Nothing changes.

  Recipients ..... The caller.

Scenario 9 - No valid session or role, unknown jobId, store unavailable

  API response ... Yes. 401 (MSG-P4-001), 404 (MSG-P4-003) or 503, as application/problem+json.

  Handling ....... Standard error response.

  Recipients ..... The caller.

Scenario 10 - Two scheduler nodes start at the same time

  API response ... No.

  Handling ....... The unique key uk_load_run_active stops the second run. One load_run row exists. No error is shown.

  Recipients ..... None.

Scenario 11 - Case users see stale data after a refusal

  API response ... No.

  Handling ....... MSG-P1-001 is shown beside the product on the Case record screen (SCR-03).

  Recipients ..... Case roles (read on screen, not pushed).

PLEASE CONFIRM:

# Channel: the design says "ACE notification path" but does not name the
medium. Is it email, Teams or another channel?
# Scenario 6: the design lists an "Alert" for a failed run but gives no
message ID or recipient. Which message and which groups should it use?
# Scenario 3: should held records within tolerance notify the data
steward, or is the exception list enough?
# Scenario 5: should the platform administrator also receive the
late-delivery alert, as in scenarios 1 and 2?


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
