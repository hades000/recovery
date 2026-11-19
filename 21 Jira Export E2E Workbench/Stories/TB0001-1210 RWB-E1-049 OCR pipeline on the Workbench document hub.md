# TB0001-1210 [RWB-E1-049] OCR pipeline on the Workbench document hub

| Field | Value |
|---|---|
| Jira | [TB0001-1210](https://scbjira.atlassian.net/browse/TB0001-1210) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Dependency, R-Environment, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:46.103+0700 |
| Updated | 2026-11-18T16:45:40.286+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a case owner (RW-CASEOWN), I want every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document, so that classification and extraction can start and an unreadable page is sent back for rescan the same day.

## Acceptance criteria

```gherkin
Feature: OCR pipeline on the Workbench document hub

  Background:
    Given OCR_MIN_QUALITY is 0.70, OCR_WORKERS is 4 and OCR_MAX_ATTEMPTS is 3
    Given the OCR service stub in SIT is replaced by the OCR service for AC1 and AC2

  Scenario: AC1 Sample processed
    Given the 180 synthetic sample documents, 30 of each of the six agreed types, in Thai and English, each as a CLEAN intake item
    When JOB-12 Document intake runs
    Then each of the 180 items has ocr_status "DONE" or "RESCAN" and an ocr_ref to its JSON output
    Then each page has a document_text row with the page text and its quality
    Then the text of the sample pages holds Thai and English words, and the languages recorded per item are "th" and "en" where both appear

  Scenario: AC2 Throughput
    Given 500 pages in 125 CLEAN intake items in SIT
    When they are processed by JOB-12 with 4 workers
    Then all 125 items reach "DONE" or "RESCAN" within 60 minutes of the first item starting

  Scenario: AC3 Unreadable page on a known case
    Given an uploaded court notice of 4 pages on case "RW-2026-000123" owned by user "TEST-CO-01"
    Given page 3 has quality 0.41 and the other pages are above 0.70
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN" and rescan_pages "3"
    Then "TEST-CO-01" receives MSG-P5-018 naming page 3, the document and case "RW-2026-000123"

  Scenario: AC4 Unreadable page with no case yet
    Given a mailroom scan of 2 pages with no case and page 1 at quality 0.30
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN", rescan_pages "1" and review_reason "RESCAN"
    Then the system sends no notification

  Scenario: AC5 Quality at the threshold
    Given a scan of 1 page with quality 0.70
    When the OCR step runs
    Then the item has ocr_status "DONE" and no rescan pages

  Scenario: AC6 OCR service unavailable
    Given the OCR service stub returns HTTP 503 for every call
    When JOB-12 runs twice
    Then each pending item has ocr_status "PENDING" and ocr_attempts 2
    Then the job monitor shows the OCR step failed in both runs and an alert is raised to the platform administrator
    Then when the service answers again the next run sets the items "DONE"

  Scenario: AC7 File that cannot be read
    Given a password-protected PDF as a CLEAN intake item
    When the OCR step runs
    Then the item has ocr_status "FAILED" and review_reason "UNREADABLE_FILE"
    Then no document_text row exists for it

  Scenario: AC8 Repeat run
    Given 10 intake items already "DONE" with 25 document_text rows
    When JOB-12 runs again
    Then the OCR service receives no call for those items
    Then they still have 25 document_text rows

  Scenario: AC9 Two workers on one item
    Given one CLEAN pending item and 4 workers starting at the same time
    When the OCR step runs
    Then the OCR service receives exactly one call for the item
    Then the item has one set of document_text rows
```

## Attachments

- [image-20261117-033858.png](../../Attachments/TB0001-1210/image-20261117-033858.png) (32237 bytes, Piyawan Sanpanya, 2026-11-17T10:48:14.058+0700)

## Comments (3)

### Comment 1: Piyawan Sanpanya, 2026-11-17T10:48:14.205+0700

Comment ID 1794029

@CHANISSARA MAHAKITTIKUN  *QA Question* 

* *Where is the "platform administrator" defined/referenced?*
* *Is JOB-12 a batch job, and does it already have its technical specification?*
* *At Flow step 8:* It states, _"Sends MSG-P5-018 to the case owner through the ACE notification path"_. However, since we likely need to decouple from ACE now, does Recovery need to handle this notification independently?
* *At AC1 (Sample processed):* In which field of the {{document_text}} table should the Thai ({{th}}) and English ({{en}}) languages be specified?
* Is Thai-only recorded as {{th}} and English-only as {{en}}? For bilingual content, does it accept both {{th,en}} and {{en,th}}, or is the order enforced? Please confirm that not every file is forced to be bilingual just because both languages are sent in the request. ref : [Story AC1|] · [Spec CLAR-002|]
* *At AC4 (Unreadable page with no case yet):* The second result seems to be missing the condition where the item needs to be sent to the document review queue.
* *At Contract section (Restart behavior):* Which story does the endpoint {{POST /api/recovery/v1/admin/jobs/{jobId}/rerun}} belong to?
* What service, engine, or version is used? Where are the endpoint, authentication, network access, request/response schema, error codes, quota, page/file limits, and response examples located? ref : [Compliance warning 002|]
* What status should be assigned for missing words, handwriting, null/out-of-range confidence, missing pages / duplicate page numbers / page numbers resetting to zero? Should rounding be done before or after comparing against 0.70? ref : [Spec: Quality rule|] 
* At Field-level behaviour matrix definition {{document_text}} as Unique ({{intake_id}}, {{page_no}}) but in the Physical Schema v6 บรรทัด 1724 as {{UNIQUE (page_no)}} ref : [Physical Schema v6|] · [Spec: Data and migration|]
* Does summary quality use mean or min? If it fails 2 times and succeeds 1 time, is attempts 2 or 3? Does {{source_ref}} need to support 400 characters?  ref : [Dictionary v8: DF-DOC-047 / 064 / 067|] · [Spec|]

!image-20261117-033858.png|width=200,alt="image-20261117-033858.png"!



* How is duplicate retry prevented within the same run? If it fails on the 3rd attempt, should it immediately become FAILED or on the next cycle? How are retries categorized across HTTP 400, 401, 403, 429, and 5xx errors? ref : [Spec: Retry and failure|]
* If 1 item out of 100 fails, does the entire step fail? Can the successful items proceed to the next step? When do consecutive run counters reset, and do alerts repeat? ref : [Spec CLAR-005 / AC6|]

### Comment 2: THAMMASAK JUKCHAN, 2026-11-17T12:17:38.041+0700

Comment ID 1794350

*Dev questions before design: RWB-E1-049*
Ref: User Stories Epic 1 v7 §RWB-E1-049. +1 to the QA list; below are the points that block our build.

{quote}🔴 *Top blockers*

# *No OCR service contract*: endpoint, auth, SY-OCR, SIT network path (PO-51, PO-65)
# *Schema defect*: {{document_text UNIQUE (page_no)}} must be {{(intake_id, page_no)}}
# *Tables already in the schema*: is our migration an ALTER only? (PO-101)
# *JOB-12 has two owners*: this story (Spring Batch) vs RWB-E1-056 (Quartz){quote}

h3. 🔴 Blocking

# *OCR service contract.* §3 says only "the OCR service run by Autonomous Ops". We need *the product/version, endpoint per environment, auth method, SY-OCR identity, SIT network path, request/response schema, error codes and page/file limits*. Who provides these, and *by when*? (PO-51, PO-65)
_Default until then: we build OcrClient against a stub (build step 2)._
# *document_text unique key.* §13 says {{(intake_id, page_no)}}, but the Physical Schema has {{UNIQUE (page_no)}}, which *blocks the second multi-page item (AC1, AC8, AC9)*. Can the Data architect fix the schema?
# *Table ownership and migration.* §11/§13 say this story creates {{document_intake}} and {{document_text}} (V1_5_049), but the *schema already holds both tables with all later columns*. Is the schema the baseline, making our migration add only {{ix_intake_ocr_pending}}? Which naming rule applies? (PO-101, PO-76, PO-29)
# *JOB-12 owner.* §13: this story builds DocumentIntakeJob (Spring Batch). RWB-E1-056 AC4 adds JOB-12 as a new Quartz job (defect E1-056 step 3, open). *Who owns the job class and the schedule?*

h3. 🟠 Need a value

# OCR parameters *0.70 / 4 / 120 / 3 are all "assumed, DL11" (overdue 5 Nov)*. When will they be confirmed? _Default: we load them as data._
# *The six document types (DL19, overdue 6 Nov)*, and who supplies the *180 labelled synthetic documents* for AC1?
# Format of {{document_intake.languages}}: {{th}}, {{en}}, {{th,en}}? Fixed order or detection order?

h3. 🟡 Design gaps

# Depends on: *E1-045 is never used; E1-025 (types) and E1-041 (scan step) are missing.*
# {{document_text.document_id}} is set only for items already attached at OCR time. *Scans attached later by RWB-E1-032 never get it, so RWB-E1-033 search cannot find their text.* Who fills it in?
# *OcrOutputReader returns no layout*, but the RWB-E1-053 template extractor needs positions. Add layout to the interface, or read it from {{ocr/{intakeId}.json}}?
# *Does the ACE notification path for MSG-P5-018 exist?* API/template owner? (+1 QA)
# Retry classes: which HTTP errors count as an attempt (4xx / 429 / 5xx)? Does one failed item mark the whole step failed for the AC6 alert?
# *Scope split:* DEP-22 says Autonomous Ops delivers "OCR and *extraction*" by 16 Nov. Confirm they provide *the OCR service only*, and that we build the pipeline here and extraction in RWB-E1-053.

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T12:27:00.899+0700

Comment ID 1794369

These points add to the QA and dev questions already on this card (OCR contract, {{document_text}} key, JOB-12 owner, retry classes, dependencies).

# *Uploads are marked CLEAN without a scan.* DocumentStoredListener sets {{scan_result}} CLEAN for uploads because "the upload was scanned before storage". RWB-E1-024 has no scan before storage, and the scan step (RWB-E1-041) depends on this story.
#* Question: may {{rwb.dochub.ocr}} be switched on before RWB-E1-041 is done? If so, which files does OCR read unscanned?
# *Raw files leave the Workbench unmasked.* Beyond the service contract, OCR sends whole files with personal data on every page to a service that has no INT in Interface Specifications v3 (feedback #75, DL33). RWB-E1-050 masks before calling the model; OCR sends the raw file.
#* Question: what is the PDPA basis, and is there a data processing agreement with the service owner (Autonomous Ops)?
# *AC1 passes even if every item is RESCAN.* AC1 checks only DONE or RESCAN.
#* Proposal: a minimum share of pages that pass quality on the 180-file sample.
# *The quality threshold depends on the engine.* OCR_MIN_QUALITY 0.70 is a mean of word confidence, which depends on the engine.
#* Proposal: tie the value to {{ocr_engine_version}}. Business should also give the daily page volume, so that OCR_WORKERS = 4 and AC2 (500 pages in 60 minutes) are sized on real numbers (DL11).

Who answers: Autonomous Ops, Security, Privacy, Business SME.


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
