# TB0001-1195 [RWB-E1-033] Search across cases

| Field | Value |
|---|---|
| Jira | [TB0001-1195](https://scbjira.atlassian.net/browse/TB0001-1195) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:34.362+0700 |
| Updated | 2026-11-18T17:24:12.394+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 4 |

## Description

As a litigation officer (RW-LITOFF), I want a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log, so that I find a document in seconds without opening cases one by one, and every look at personal data can be audited.

## Acceptance criteria

```gherkin
Feature: Search across cases

  Background:
    Given 500 synthetic documents indexed across 120 cases
    Given 60 of them are "APPRAISAL_REPORT", 14 with appraised_value above 5,000,000, 9 of those stored in October 2026
    Given user "TEST-LIT-01" holds RW-LITOFF with scope ALL

  Scenario: AC1 Search by field
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches type "APPRAISAL_REPORT", field appraised_value greater than 5,000,000, stored from 1 October 2026 to 31 October 2026
    Then exactly the 9 matching documents list with case number, type, stored date and the field value
    Then the response arrives within 2 seconds

  Scenario: AC2 Role limit
    Given user "TEST-LIT-02" holds RW-LITOFF with scope TEAM on team "MTG-BKK-LIT", whose cases are all product group "MORTGAGE"
    Given 40 of the 500 documents are on "HIRE_PURCHASE" cases
    When "TEST-LIT-02" searches type "COURT_NOTICE" with no date
    Then no document on a "HIRE_PURCHASE" case appears
    Then the system writes one access event "DOCUMENT_SEARCH" with the user, the criteria, the result count and the case IDs returned

  Scenario: AC3 Free text
    Given the OCR text of 3 documents holds the synthetic guarantor name "ผู้ค้ำทดสอบ หนึ่ง"
    When "TEST-LIT-01" searches the free text "ผู้ค้ำทดสอบ หนึ่ง"
    Then the 3 documents list with a snippet in which the name is highlighted
    Then the access event holds the SHA-256 hash of the term and not the term

  Scenario: AC4 Free text refused for a masked role
    Given user "TEST-CO-01" holds RW-CASEOWN, whose masking rule hides party names
    When "TEST-CO-01" searches the free text "ผู้ค้ำทดสอบ"
    Then the system refuses the request with 422 and MSG-P5-020 naming "document text"
    Then no query runs

  Scenario: AC5 No criterion
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches with every criterion empty
    Then the system refuses the request with 422 and MSG-GEN-001 naming "a search criterion"

  Scenario: AC6 Date range in the wrong order
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches stored from 31 October 2026 to 1 October 2026
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC7 Free text length boundary
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches the free text "ab" and then the free text "abc"
    Then the system refuses "ab" with 422 and MSG-GEN-002 showing 3 and 100
    Then "abc" runs

  Scenario: AC8 More results than the limit
    Given 1,250 documents of type "DEMAND_LETTER" in the user's scope
    When "TEST-LIT-01" searches type "DEMAND_LETTER"
    Then the first page of 50 rows returns with total 1000 and capped true
    Then MSG-P5-021 shows with the count 1000

  Scenario: AC9 Access log not confirmed
    Given the PII access log does not confirm writes
    When "TEST-LIT-01" searches type "COURT_NOTICE"
    Then the request returns 503 with MSG-P5-019
    Then the system returns no result row

  Scenario: AC10 Nothing matches
    Given no document holds the free text "ไม่มีคำนี้"
    When "TEST-LIT-01" searches it
    Then the page shows the empty state "No documents match this search." and the action "Clear the search"
    Then the access event records a result count of 0
```

## Comments (4)

### Comment 1: Piyawan Sanpanya, 2026-11-17T12:43:42.863+0700

Comment ID 1794384

@CHANISSARA MAHAKITTIKUN 

QA question

FLOW 

# Litigation officer : A person opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value), and/or a free text term. => but on Foundation, there is no screen
# API GET /documents with the [criteria. Is it|http://criteria.it] a new API? Implement it in this story? , Does Henka provide the specification?
# step 5 : What about CaseDirectory.caseIdsInScope is it a DB function or a coding function? Does Henka provide the logic for checking the user ID by searching the case id and matching the document?

Business rules

# BR1: How to check active documents?



AC 

# AC Scenario : 500 synthetic documents test; does Henka provide for AC testing
# AC1 Search by field: the AC test by searching from the screen? But, for EP1 not stil have the screen once so how we can testing?
# AC2 Role limit : Does Henka can provide the matrix about right for search?

### Comment 2: Chanapai Gingpuwaluck, 2026-11-17T12:49:42.668+0700

Comment ID 1794392

These points add to the QA questions already on this card (screen, API, CaseDirectory scope, active documents, test data, role matrix). Points 5 and 6 partly answer two of them.

# *Every search fails without the access log.* The precondition says the ACE common module writes the PII access log, but there is no INT for it, it is not in "Depends on", and it is not part of RWB-ACE-001. Physical Schema v6 has no access log table (feedback #49). Under AC9, every search returns 503 if that service is missing.
#* Question: who provides the access log, and by when?
# *Free-text search has no index.* {{document_text}} has no full-text or trigram index, and Thai has no spaces between words, so free text becomes a substring scan of every page. AC1 measures 2 seconds only for a field search on 500 documents.
#* Proposal: choose the Thai tokenisation, and add a performance AC for free text at real volume.
# *Searching unconfirmed fields.* Field conditions such as {{appraised_value > 5,000,000}} cast from varchar.
#* Question: are fields still in REVIEW (not confirmed by a person) searchable? They may hold OCR misreads.
# *The query hash does not protect the query.* A SHA-256 hash of the query with no salt is easy to reverse with a dictionary of names. Auditors also cannot read what was searched.
#* Proposal: encrypt the query and restrict who can read it.
# *On "is GET /documents a new API?".* API Specification v4 already has {{GET /documents}}, and the flow and section 12 use it. Section 13 and the feature flag still say {{GET /documents/search}} (Defect 2, open). Please correct section 13, so the story builds only the v4 path.
# *On the role matrix for search.* It comes from RWB-E1-037 (role masking matrix, groomed Day 3), and the access log from RWB-E1-039. Neither is in "Depends on"; please add both, together with the story that publishes {{CaseDirectory.caseIdsInScope}} (RWB-E1-002 or RWB-E1-020).

Who answers: Solution architect, ACE team, DBA, Privacy, Audit.

### Comment 3: RACHATAPON PONGANANTAYOTIN, 2026-11-17T12:57:32.787+0700, edited 2026-11-18T11:30:51.324+0700

Comment ID 1794397

DEV Question:

# Does the PII access log confirm each write synchronously, and what is its API and package?
## DEP-04 (Open, overdue since 9 Nov); OPEN-024 (Open)
# Do you have more detail about API ?

### Comment 4: NAMTIP WONGSOMBOON, 2026-11-18T11:18:38.871+0700, edited 2026-11-18T11:19:27.758+0700

Comment ID 1796198

@CHANISSARA MAHAKITTIKUN 
Ref: Grooming Session – Room 2 with Henka , {{2026-11-18}}
AC2 Role Limits
Which Story covers the role management required for testing AC2? 
Could you also provide an example of the role configuration?



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
