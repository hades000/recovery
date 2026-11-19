# TB0001-1178 [RWB-E1-016] Access control per data product and catalog entries

| Field | Value |
|---|---|
| Jira | [TB0001-1178](https://scbjira.atlassian.net/browse/TB0001-1178) |
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
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:17.900+0700 |
| Updated | 2026-11-18T17:22:59.990+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want read access to each data product granted by role, PDPA fields tagged, every read logged, and a catalog entry per product with owner, system of record, freshness and fields, so that personal data is read only by the roles that need it and every product is findable.

## Acceptance criteria

```gherkin
Feature: Access control per data product and catalog entries

  Background:
    Given data product access version "DPA-2026.11" is in force from 2026-11-20
    Given case "RW-2026-000102" has borrower party "PTY-SYN-0102" with mobile contact point value "0812345678" stored as token
    Given no masking rule from Compliance is loaded for party or contact_point fields

  Scenario: AC1 Role access
    Given user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the mobile number shows as "******5678" and the national ID token is returned as "MASKED"
    Then the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read

  Scenario: AC2 Catalog entry
    Given the 14 data products DP01 to DP14
    When a data steward calls GET /admin/data-products
    Then the system returns 14 entries
    Then each has an owner role, a system of record, a refresh cycle, an expected-by time, a retention class and the field list with PDPA tags
    Then the DP02 entry lists 20 fields of which 9 are tagged personal

  Scenario: AC3 Access denied
    Given user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06
    When the user calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system writes the refusal to the access log with user "u-phone-01" and product "DP06"

  Scenario: AC4 An access load with an unknown role is refused
    Given an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "unknown role RW-UNKNOWN"
    Then version "DPA-2026.11" stays in force

  Scenario: AC5 A case outside the user's scope
    Given user "u-owner-07" holds RW-CASEOWN with scope Own and does not own case "RW-2026-000102"
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 404 and MSG-P4-003
    Then the system reads no row

  Scenario: AC6 No masking rule loaded keeps every personal field masked
    Given user "u-comply-01" holds RW-COMPLY, which reads DP02
    When the user calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then first_name, last_name, cif_no, date_of_birth and the contact value are returned masked

  Scenario: AC7 The PII access log is unavailable
    Given the PII access log rejects every write
    When user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102
    Then the system refuses the call with status 503 and MSG-GEN-006 for system "PII access log"
    Then the system returns no personal field

  Scenario: AC8 An access row not yet in force
    Given access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15
    Given today is 2026-12-14
    When user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102
    Then the system refuses the call with status 403 and MSG-P4-002
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
