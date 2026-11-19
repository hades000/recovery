# TB0001-1226 [RWB-E1-065] Sandbox database with synthetic recovery data

| Field | Value |
|---|---|
| Jira | [TB0001-1226](https://scbjira.atlassian.net/browse/TB0001-1226) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chanapai Gingpuwaluck |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Non-Block, QA-Reviewed, R-Requirement |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:59.080+0700 |
| Updated | 2026-11-18T17:41:53.065+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 4 |

## Description

As a Tribe lead and squad member (RW-TRIBE), I want a sandbox database holding synthetic recovery data, so that I can build and test before the real interfaces are available.

## Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data

  Background:
    Given the sandbox build uses seed 20261128
    Given volumes of 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases

  Scenario: AC1 The sandbox exists
    Given the data product schema from the Flyway migrations
    When the sandbox is provisioned
    Then it holds 2,812 synthetic cases plus 10 cases for each exception shape, across Mortgage, Hire Purchase and SSME
    Then every one of the 41 entity tables holds at least one row
    Then case "RW-2026-000001" has its accounts, parties and interactions linked

  Scenario: AC2 It is readable and extractable
    Given the sandbox
    When a member of RWB-DEV-RW-TRIBE runs "SELECT product_group, count(*) FROM recovery.recovery_case GROUP BY product_group"
    Then the result shows MORTGAGE, HIRE_PURCHASE and SSME with their counts
    Then the export script writes recovery_case to a CSV file without a request to another team
    Then the system refuses an UPDATE by the same database role

  Scenario: AC3 It scales with the schema
    Given a migration adds column "risk_tier varchar(10)" to recovery_case with its sys_fields row and list LOV-RISK-TIER
    When it is applied
    Then the sandbox rebuild fills risk_tier with values from LOV-RISK-TIER on every case
    Then no generator code was changed

  Scenario: AC4 A column with no dictionary entry
    Given a migration adds column "note_x varchar(40)" to loan_account with no sys_fields row
    When the sandbox build runs
    Then the build fails with "loan_account.note_x has no data dictionary entry"
    Then the previous sandbox stays in use

  Scenario: AC5 The same build twice
    Given the sandbox was built for commit "a1b2c3d"
    When the build runs again for commit "a1b2c3d"
    Then every table holds the same row count
    Then case "RW-2026-000001" holds the same total_outstanding_at_entry of 1,845,200.00

  Scenario: AC6 A generated value breaks a constraint
    Given list LOV-PRODUCT is empty in the seed data
    When the sandbox build runs
    Then the build fails naming table "recovery_case" and column "product_group"
    Then the previous sandbox stays in use

  Scenario: AC7 No personal data in the sandbox
    Given the verifier scans every column tagged is_personal
    When a value matches the 13-digit national ID pattern with a valid check digit
    Then the build fails naming the table and column
    Then the system publishes no sandbox from that build

  Scenario: AC8 Accounts at the entry boundary
    Given the exception shapes include the entry boundary
    When the sandbox is provisioned
    Then 10 loan accounts have days_past_due 89 and no case
    Then 10 loan accounts have days_past_due 90 and one open case each

  Scenario: AC9 Two builds at once
    Given a sandbox build is running for commit "a1b2c3d"
    When a second build starts for commit "e4f5a6b"
    Then the second build waits until the first ends
    Then the sandbox after both holds the data for commit "e4f5a6b"
```

## Comments (4)

### Comment 1: RAPEEPAT CHULAOTRAKUL, 2026-11-12T18:01:29.894+0700, edited 2026-11-12T18:34:55.307+0700

Comment ID 1788419

@CHANISSARA MAHAKITTIKUN 

For discussion, Grooming 12 Nov 2026

* *AC4 A column with no dictionary entry* 
** We recommend updating the expected behavior from a "*build failed*" status to simply excluding any columns not present in {{sys_field}} from being loaded for downstream processing.
* *AC7 No personal data in the sandbox* 
** Need Confirm logic to verify 13-digit national ID pattern with a valid check digit.



CC @Chanapai Gingpuwaluck 

### Comment 2: Nitchayaphan Kanpirompachira, 2026-11-17T11:35:41.296+0700, edited 2026-11-17T12:55:03.042+0700

Comment ID 1794231

*Clarification needed:*

# *Entry threshold scope*

AC8 currently generates the 89/90-day boundary accounts (10 at 89, 10 at 90) as one undifferentiated set, implying a single global entry threshold across all products. However, the supporting business rule (RWB-E1-045 BR2) and parameter catalog describe {{case.entry.dpd}} (ENTRY_DPD) as scope PRODUCT, keyed per product group (Mortgage, Hire Purchase, SSME) via {{ProductParameterService}}.

This implies the boundary set may need to be generated per product group once RWB-E1-045 is live, rather than as one shared set, so the sandbox stays valid if product values diverge later.

*Question:* Can we confirm whether the 90-day threshold is expected to stay identical across all three products for the life of this sandbox, or should AC8 generate the boundary accounts per product group now?



# *"days past due" calculation*

AC8 requires generating loan accounts with {{days_past_due}} at exactly 89 and 90 days, but does not specify the reference point for this calculation — whether it's based on the data load date ({{data_as_of}}) or computed live from the pipeline's run date at build time.

This affects sandbox correctness on rebuild: if {{days_past_due}} is fixed relative to the {{data_as_of}} set at first generation, a later rebuild (days/weeks after) would cause the value to drift past the 89/90 boundary (e.g., become 90/91 or higher), making AC8 fail for reasons unrelated to an actual defect.

*Question:* How to calculate {{days_past_due}}?



# *Refuse Upade*

AC2 the system refuses an UPDATE by the same database role.

*Question:* Are INSERT and DELETE also being refused?



note : Sandbox environment setup (may need consultation/guidance from devs).

### Comment 3: VAISHNAVI KAULGE, 2026-11-17T13:34:32.016+0700

Comment ID 1794466

@RAPEEPAT CHULAOTRAKUL 

AC4: a column with no dictionary entry

We agree with the change. A dictionary gap should not stop a squad from getting a sandbox. We recommend these details:

Skip the column, but report it.
The build leaves the column empty (NULL or its default).
The build report lists every skipped column as a warning, naming the table and column.
This keeps the dictionary gap visible to the dictionary owner (RWB-E1-064).
Keep a hard failure for two cases.
The column is NOT NULL with no default. The row insert fails anyway (AC6).
The column is read by one of the 30 views. The view check fails.
Safe for personal data. A skipped column gets no value, so a column with an unknown personal-data flag stays empty.
Story changes:
AC4 now says "the build publishes, the column is empty, and the report names it".
X1 and TC-E1-065-04 follow the same text.
"The previous sandbox stays in use" is removed from AC4. It stays in AC6.
AC7: 13-digit national ID with a valid check digit

We confirm the logic is the standard Thai national ID checksum:

Take the first 12 digits and multiply them by 13, 12, 11 … 2, then add them up.
The check digit is (11 − (sum mod 11)) mod 10. It must equal digit 13.
Example: 1123456789014 passes, and 1123456789015 fails. We tested both.
Details to add to the story:

Normalising: the scan removes dashes and spaces first, so 1-1234-56789-01-4 is caught. The 13 digits must stand alone, with no digit before or after.
Scope: only columns tagged is_personal in schema recovery are scanned. The 64-character hex tokens sit in other columns and stay out of scope. A hex token can contain 13 digits in a row by chance, and one in ten such runs passes the checksum. That would fail builds at random.
No false pass by design: the value generator gives synthetic IDs a wrong check digit, so a generated value never matches.
ACE-shaped tables: a clear ID in the ACE-shaped tables (for example public.customer) is allowed. This is already in AC7 and BR9.

### Comment 4: VAISHNAVI KAULGE, 2026-11-17T13:42:10.267+0700

Comment ID 1794489

@Nitchayaphan Kanpirompachira 

# AC4: a column with no dictionary entry

We agree with the change. A dictionary gap should not stop a squad from getting a sandbox.

The build skips the column and leaves it empty (NULL or its default).
The build report lists every skipped column as a warning, naming the table and column, so the dictionary owner (RWB-E1-064) sees the gap.
The build still fails in two cases:
The column is NOT NULL with no default. The row insert fails anyway (AC6).
The column is read by one of the 30 views. The view check fails.
A skipped column gets no value, so a column with an unknown personal-data flag stays empty.
Story changes:
AC4 says "the build publishes, the column is empty, and the report names it".
X1 and TC-E1-065-04 follow the same text.
"The previous sandbox stays in use" is removed from AC4. It stays in AC6.

# AC7: 13-digit national ID with a valid check digit

The logic is the standard Thai national ID checksum:

Take the first 12 digits and multiply them by 13, 12, 11 … 2, then add them up.
The check digit is (11 − (sum mod 11)) mod 10. It must equal digit 13.
Example: 1123456789014 passes, and 1123456789015 fails.
Details to add to the story:

Normalising: the scan removes dashes and spaces first, so 1-1234-56789-01-4 is caught. The 13 digits must stand alone, with no digit before or after.
Scope: only columns tagged is_personal in schema recovery are scanned. A hex token can contain 13 digits in a row by chance, and one in ten such runs passes the checksum. Scanning those columns would fail builds at random.
No false pass by design: the value generator gives synthetic IDs a wrong check digit, so a generated value never matches.
ACE-shaped tables: a clear ID in the ACE-shaped tables (for example public.customer) is allowed (AC7 and BR9).

# AC8: entry threshold, one global value or per product group?

We recommend generating the boundary accounts per product group now.

DL16 sets entry at 90 days past due, but E1-045 BR2 holds the value per product group (ENTRY_DPD). The business sets values per product, so we can't promise the three products stay identical for the life of the sandbox. The Business lead can confirm this.
For each of Mortgage, Hire Purchase and SSME, the generator creates 10 accounts at threshold minus 1 (no case) and 10 at the threshold (one open case each). That is 60 accounts in total.
The generator reads the threshold for each product group. Until E1-045 is live, it reads case.entry.dpd = 90 for all three, so today's result is still 89 and 90.
Story changes:
AC8 becomes "per product group".
BR4 says "the boundary is the entry threshold of that product group".
TC-E1-065-08 checks all three groups.

# AC8: how days_past_due is calculated

It is a stored value, not a live calculation.

In ACE, the account's delay_days field is the daily snapshot value. The view v_ace_account exposes it as days_past_due, with data_as_of as the core banking date. The Workbench never calculates it.
The generator writes days_past_due (89 or 90) as a fixed number on the synthetic ACE account row. It does not derive it from the pipeline's run date.
The reference point is the business date of the sandbox, which is a fixed property (for example rwb.sandbox.business-date). The boundary rows carry data_as_of equal to that date.
A rebuild days or weeks later gives the same 89 and 90 and the same rows (AC5).
The E1-018 case creation job reads accounts with days_past_due at or above the threshold and data_as_of equal to the business date. The sandbox business date and the boundary rows use the same date.
Any related date field the generator fills (for example when the account became overdue) is business date minus days_past_due.
Story changes:
AC8 gets the line "the boundary rows carry data_as_of = the sandbox business date".
We add the property rwb.sandbox.business-date to section 13.

# AC2: are INSERT and DELETE also refused?

Yes. Every write is refused.

Flow step 10 grants only SELECT on schema recovery to the role rwb_sandbox_read, which maps to the squad group RWB-DEV-RW-TRIBE. No INSERT, UPDATE, DELETE or TRUNCATE is granted, and none of them is allowed.
The role can't change the table structure either.
Only the pipeline's build connection writes to the sandbox. It uses a separate privileged role and fills rwb_sandbox_next.
Story changes:
AC2 and TC-E1-065-02 check that an INSERT, an UPDATE, a DELETE and a TRUNCATE are each refused.
Section 13 names the two roles: the build role (writes) and rwb_sandbox_read (SELECT only).
Open point for the devs (sandbox setup)

The story does not say whether rwb_sandbox_read may also read schema public (the ACE-shaped tables).
These tables hold clear identity numbers, synthetic but unmasked (BR9).
Our recommendation: squads read the ACE data only through the 30 views in schema recovery, with no direct SELECT on public.
The platform administrator (RW-PLATADM) and the tech lead should confirm this when the sandbox database is set up.


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
| QBR Date | customfield_17520 | 2026-11-12 |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Rework | customfield_17514 | Rework |
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
