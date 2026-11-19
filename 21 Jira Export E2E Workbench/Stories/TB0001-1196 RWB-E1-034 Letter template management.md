# TB0001-1196 [RWB-E1-034] Letter template management

| Field | Value |
|---|---|
| Jira | [TB0001-1196](https://scbjira.atlassian.net/browse/TB0001-1196) |
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
| Created | 2026-11-05T12:37:35.111+0700 |
| Updated | 2026-11-17T10:08:10.253+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer (RW-LITOFF), I want a screen to upload a template version, have Legal counsel record the approval and set it current, so that templates are managed without a developer.

## Acceptance criteria

```gherkin
Feature: Letter template management

  Background:
    Given user "LIT-0101" holds RW-LITOFF
    Given user "LEG-0001" holds RW-LEGAL
    Given template "DEMAND-MTG" in language "TH" has version 2 Approved by "LEG-0001" with valid from 2026-11-01
    Given today is 2026-11-20

  Scenario: AC1 New version
    Given "LIT-0101" uploads "demand-mtg-th-v3.docx" for "DEMAND-MTG" "TH" using merge codes "CASE_NO" and "TOTAL_OUTSTANDING"
    Given version 3 is created in state "Draft"
    When "LEG-0001" approves version 3 with valid from 2026-11-20
    Then version 3 has state "Approved", approver "LEG-0001" and an approval time on 2026-11-20
    Then TemplateCatalog returns version 3 as current for "DEMAND-MTG" "TH" on 2026-11-20
    Then version 2 stays readable on SCR-33 with approver "LEG-0001"

  Scenario: AC2 Approval required
    Given version 3 of "DEMAND-MTG" "TH" is in state "Draft" with no approver
    When "LIT-0101" chooses set current on version 3
    Then the system refuses it with MSG-P6-005 naming "DEMAND-MTG" version 3
    Then version 2 stays current

  Scenario: AC3 The uploader cannot approve the version
    Given "LEG-0001" uploaded version 4 of "RECALL-SSME" "TH"
    When "LEG-0001" approves version 4
    Then the system refuses it with status 409 and MSG-P7-002
    Then version 4 stays "Draft"

  Scenario: AC4 Unknown merge code refused at upload
    Given "LIT-0101" uploads a body for "DEMAND-HP" "TH" that uses the merge code "LINE_ID"
    Given "LINE_ID" is not in the merge field catalog
    When the upload is sent
    Then the system refuses it with status 422 and MSG-P6-006 naming "LINE_ID"
    Then the system creates no version of "DEMAND-HP" and no file is stored

  Scenario: AC5 Required field empty
    Given "LIT-0101" uploads a body with no template code
    When the upload is sent
    Then the system refuses it with status 422 and MSG-GEN-001 naming "template code"

  Scenario: AC6 File type not allowed
    Given "LIT-0101" uploads "demand.pdf" for "DEMAND-MTG" "TH"
    When the upload is sent
    Then the system refuses it with status 415 and MSG-P6-010 naming "DOCX"

  Scenario: AC7 Valid from before today
    Given version 3 of "DEMAND-MTG" "TH" is "Draft"
    When "LEG-0001" approves it with valid from 2026-11-19
    Then the system refuses it with status 422 and MSG-GEN-003 naming "valid from" and "today"

  Scenario: AC8 Withdraw the current version
    Given version 3 of "DEMAND-MTG" "TH" is Approved and current
    When "LEG-0001" withdraws version 3 with reason "Wording under review"
    Then version 3 has state "Withdrawn"
    Then TemplateCatalog throws TemplateWithdrawnException for "DEMAND-MTG" "TH" with MSG-P6-003
    Then the system does not mak version 2 current again

  Scenario: AC9 Two approvals at the same time
    Given version 3 of "DEMAND-MTG" "TH" is "Draft" at record version 1
    Given "LEG-0001" and "LEG-0002" both open it
    When both approve within the same second
    Then one approval succeeds
    Then the system refuses the other with status 409 and MSG-GEN-004

  Scenario: AC10 Repeated approval request
    Given "LEG-0001" approved version 3 with Idempotency-Key "7f1c0d2e-0001"
    When the same request is sent again with Idempotency-Key "7f1c0d2e-0001"
    Then the response is the first response with status 200
    Then the audit log holds one approval for version 3
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
