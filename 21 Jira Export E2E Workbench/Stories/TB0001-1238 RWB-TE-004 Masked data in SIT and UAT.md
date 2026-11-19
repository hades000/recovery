# TB0001-1238 [RWB-TE-004] Masked data in SIT and UAT

| Field | Value |
|---|---|
| Jira | [TB0001-1238](https://scbjira.atlassian.net/browse/TB0001-1238) |
| Type | Story |
| Status | To Design - Solution |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | PRACHYA RUNGTWEESUK |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ1 |
| Created | 2026-11-05T16:11:12.520+0700 |
| Updated | 2026-11-17T21:30:38.266+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 4 |

## Description

As a Tribe lead and squad member (RW-TRIBE), I want masked copies of recovery data loaded into SIT and UAT from the PII service, so that tests run on realistic volumes without exposing customers.

## Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 loan accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with total_balance sums per product

  Scenario: AC1 Masked copy
    Given a masked copy from the PII service
    When it is loaded into SIT
    Then every column tagged is_personal in party and contact_point holds a token or a masked value
    Then balances keep their shape: the count and the total_balance sum per product equal the manifest
    Then each party token joins to the same case_party and loan account rows as in the extract

  Scenario: AC2 A personal value left in the copy
    Given party row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in id_no_token
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in party.id_no_token"
    Then the previous SIT copy stays in use

  Scenario: AC3 Totals that do not match the manifest
    Given the loan_account file holds 28,118 rows
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals loan_account 28,118 against 28,119"

  Scenario: AC4 A copy aimed at DEV
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file

  Scenario: AC5 The same extract twice
    Given extract "PII-SIT-20261120" was loaded into SIT on 2026-11-20
    When it is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20

  Scenario: AC6 A masking rule version that is not in force
    Given a manifest with masking rule version "MASK-2026.10"
    When the copy is loaded into UAT
    Then the system refuses the load in full with MSG-P1-002 and check "masking rule version MASK-2026.10 is not in force"

  Scenario: AC7 A second load while one runs
    Given a masked copy load into SIT is running
    When a second load into SIT starts
    Then the system refuses the second load with MSG-P2-006
```

## Comments (4)

### Comment 1: RAPEEPAT CHULAOTRAKUL, 2026-11-12T18:33:29.085+0700

Comment ID 1788480

@CHANISSARA MAHAKITTIKUN 

As discussed, the ACE team will prepare mock data based on Collin's schema for the SIT and UAT environments. Data masking is not required. This user story should be descoped.



CC @Chanapai Gingpuwaluck 

### Comment 2: CHANISSARA MAHAKITTIKUN, 2026-11-17T10:32:12.136+0700

Comment ID 1793983

@RAPEEPAT CHULAOTRAKUL Noted

### Comment 3: PRACHYA RUNGTWEESUK, 2026-11-17T10:48:27.799+0700

Comment ID 1794030

@RAPEEPAT CHULAOTRAKUL Please note that   ACE team already have mock data in SIT and UAT for collection workbench which can be shared to recovery workbench team.  However, if any required data is not available in the existing environments, TechX should be responsible for preparing the additional mock data accordingly.

### Comment 4: PRACHYA RUNGTWEESUK, 2026-11-17T11:00:34.899+0700

Comment ID 1794074

@RAPEEPAT CHULAOTRAKUL For more information, some data in SIT / UAT is masked production data using this script. [https://gitdop.se.scb.co.th/AP2477-ACE/ace-etl-job/-/blob/develop/aceetl/masking.py|https://gitdop.se.scb.co.th/AP2477-ACE/ace-etl-job/-/blob/develop/aceetl/masking.py].

If a significant amount of additional data is expected to be added, this story could be considered for implementation.


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
