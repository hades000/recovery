# TB0001-1214 [RWB-E1-053] Field extraction for the six types into the index

| Field | Value |
|---|---|
| Jira | [TB0001-1214](https://scbjira.atlassian.net/browse/TB0001-1214) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Requirement, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:49.428+0700 |
| Updated | 2026-11-18T16:26:27.126+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a case owner, I want the key fields of each of the six document types extracted and written to the document index with a confidence per field, so that documents are searchable by their content.

## Acceptance criteria

```gherkin
Feature: Field extraction for the six types into the index

  Background:
    Given DOCTYPE-2026.11 is in force
    Given COURT_NOTICE lists court_name (text), black_case_no (text, pattern two to four letters, a space, digits, "/" and four digits), notice_date (date) and hearing_date (date)
    Given EXTRACT_FIELD_THRESHOLD is 0.80

  Scenario: AC1 Fields extracted
    Given intake item "IN-0001" classified "COURT_NOTICE" with confidence 0.9400
    Given its OCR text holds court "Civil Court", black case number "Por 1234/2569", notice date "1 ธันวาคม 2569" and hearing date "15 ธันวาคม 2569"
    When extractStep runs
    Then extracted_fields of "IN-0001" holds court_name "Civil Court" 0.9600, black_case_no "Por 1234/2569" 0.9100, notice_date "2026-12-01" 0.9000 and hearing_date "2026-12-15" 0.8800, each with state "OK" and extractor version "EXT-TPL-1.0"
    Then extract_status is "DONE"
    Then when matchStep stores the document on case "RW-2026-000123" the four fields are in the index and review_status is "NOT_NEEDED"

  Scenario: AC2 Precision and recall
    Given the labeled sample of 180 documents and the pass marks precision 0.90 and recall 0.90 per field
    When the extraction evaluation run processes the sample
    Then the report lists precision and recall for each of the 26 fields with the extractor version
    Then the system lists TITLE_DEED area_sq_wa with precision 0.84 as "review-only"
    Then the run writes a proposed DOCTYPE load file with review_only true for area_sq_wa only
    Then the version in force does not change until the proposed version is loaded and approved

  Scenario: AC3 A field below the threshold goes to review
    Given intake item "IN-0002" classified "COURT_NOTICE"
    Given the extractor returns hearing_date with confidence 0.6200
    When extractStep runs
    Then hearing_date has state "REVIEW" and the other three fields state "OK"
    Then when the document is stored its review_status is "PENDING" and SCR-30 shows MSG-P5-003

  Scenario: AC4 A review-only field always goes to review
    Given TITLE_DEED field area_sq_wa has review_only true
    Given the extractor returns area_sq_wa "940" with confidence 0.9900 on item "IN-0003"
    When extractStep runs
    Then area_sq_wa has state "REVIEW"

  Scenario: AC5 Confidence equal to the threshold passes
    Given the extractor returns black_case_no on item "IN-0004" with confidence 0.8000
    When extractStep runs
    Then black_case_no has state "OK"

  Scenario: AC6 A value that cannot be converted goes to review
    Given the OCR text of item "IN-0005" holds hearing date "32 ธันวาคม 2569"
    When extractStep runs
    Then hearing_date keeps the value "32 ธันวาคม 2569" with confidence 0.0000 and state "REVIEW"

  Scenario: AC7 The extracted case number and account number are given to matchStep
    Given intake item "IN-0006" classified "DEMAND_LETTER" whose text holds case "RW-2026-000123" and an account number
    When extractStep runs
    Then extracted_fields holds case_no "RW-2026-000123" and account_no
    Then the system marks account_no personal and is not written to the job record or the logs

  Scenario: AC8 The extractor does not answer
    Given the extractor does not answer within 60 seconds on 3 attempts for item "IN-0007"
    When extractStep runs
    Then extract_status is "FAILED" and review_reason is "EXTRACTION_FAILED"
    Then extracted_fields is empty
    Then matchStep does not attach "IN-0007"

  Scenario: AC9 A repeated run has no effect
    Given item "IN-0001" has extract_status "DONE"
    When extractStep runs again
    Then the system does not read "IN-0001" again and extracted_fields is unchanged

  Scenario: AC10 Two workers on the same item
    Given two extractStep workers start at the same time
    When both select item "IN-0008"
    Then one worker extracts it and the other skips it
    Then "IN-0008" has one set of fields

  Scenario: AC11 A new version of an uploaded document
    Given uploaded court notice "DOC-0001" has four active document_field rows from version 1
    Given version 2 of "DOC-0001" is added with hearing date "20 มกราคม 2570"
    When extractStep runs on the intake item for version 2
    Then the system writes four new active rows with hearing_date "2027-01-20"
    Then the four version 1 rows have is_active false and stay readable
    Then one DocumentFieldsExtracted event is in the outbox for "DOC-0001"

  Scenario: AC12 An English document is extracted
    Given item "IN-0009" classified "APPRAISAL_REPORT" with English text holding appraisal number "AP-2026-0457", date "3 October 2026" and value "THB 4,250,000"
    When extractStep runs
    Then appraisal_no is "AP-2026-0457", appraisal_date is "2026-10-03" and appraised_value is "4250000.00"

  Scenario: AC13 A document outside the caller's scope
    Given a case owner whose scope is team "MTG-BKK"
    Given document "DOC-0010" belongs to a case in team "HP-NE"
    When the case owner calls GET /api/recovery/v1/documents/DOC-0010
    Then the response is 404 with MSG-P4-003 and no field value is returned
```

## Comments (3)

### Comment 1: thanapat khumprom, 2026-11-17T11:08:30.087+0700

Comment ID 1794117

h2. Open questions for BA: RWB-E1-053 (hub v17)

Questions 1–9 block the build. Questions 10–17 can be answered during the build. Items marked *(new)* came from cross-checking this story against other stories in hub v17.

h3. A. Needed before the build starts

*Field extraction*

# *Anchors for TEMPLATE (new).* Where are the anchor texts for each field stored, and who provides them? Section 13 defines {{TemplateFieldExtractor}} as a "layout and anchor-text extractor", but {{field_definitions}} holds only name, data_type, personal, extraction_method, review_only and pattern. No document in the hub defines anchors. Hard-coding them would break DT02. Should we add an {{anchors}} key to {{field_definitions}} (this changes RWB-E1-025), or keep them in a separate config table?
# *Confidence formula (new).* How is the confidence of each field calculated, for TEMPLATE and for MODEL? The story only says that {{FieldExtractor}} returns a confidence. The OCR output (RWB-E1-049) gives only word confidence and page quality.
# *Layout (new).* Flow step 4 reads "page text and layout" through {{OcrOutputReader}}. But {{document_text}} holds only {{text_content}} and {{quality}}. Word positions exist only in {{ocr/{intakeId}.json}} ({{ocr_ref}}). Does {{PageText}} carry word positions, or should {{TemplateFieldExtractor}} read the OCR JSON file directly?

*LLM call*

# *Model gateway and dependencies.* The story says ModelFieldExtractor calls "the P10 model gateway (RWB-TE-013)". RWB-TE-013 is {{AgentStepClient}}, which needs {{caseId}}, {{decisionCode}} and {{RuleResult}}. This does not fit extraction, because most intake items have no case yet. The gateway itself is built in RWB-E1-058.
#* Can we follow RWB-E1-050, where {{ModelGatewayClassifier}} calls the gateway directly?
#* Preconditions also require RWB-E1-024 to be done, but {{Depends on}} lists only RWB-E1-049, RWB-E1-050 and RWB-E1-025. Should RWB-E1-058 and RWB-E1-024 be added as dependencies?
# *DL33.* Which model endpoint will ModelFieldExtractor call: (A) Azure OpenAI through Azure Foundry, or (B) the endpoint ACE uses through AAL? What value goes in {{rwb.dochub.extract.model-route}}?

*Reference data*

# *DL19.* Have the business lead and Legal approved DOCTYPE-2026.11 (6 types, 26 fields)? If the bank uses its own list (option B), will the field list change before the build? *(new)* What is the initial {{extraction_method}} (TEMPLATE or MODEL) for each type or field? RWB-E1-060 chooses the method only after its evaluation.
# *DL26.* Which fields are personal, and which roles may see them unmasked? We need this for BR9 and AC7 (account_no).

*Field not found*

# *Field not found (new).* No AC or exception path covers a field that cannot be found in the OCR text. Should we write a row with {{field_value}} null, confidence 0.0000 and state REVIEW (as in BR5), or write no row? Is {{document_field.field_value}} nullable?
# *Field absent from the document (new).* Example: a demand letter with no pay-by date. How does the reviewer in RWB-E1-054 confirm "no value"? Today, Correct with an empty value returns 422 with MSG-GEN-001, and the review cannot be completed while a field is still in REVIEW.

h3. B. Can be answered during the build

# *DL11.* The threshold and the 6 parameters (0.80, 0.90, 0.90, 3, 60, 543) are assumed until the RWB-E1-060 report. When will the real values be available? Should SIT and UAT for E1 use the assumed values?
# *Tests that depend on another story.* The last results of AC1 and AC3 need matchStep to store the document. matchStep belongs to RWB-E1-032, which is downstream and out of scope. Should we test this part with a stub, or wait for RWB-E1-032?
# *document_field columns.* Section 11 lists {{state}} and {{is_active}} as standard columns, but this story's migration adds only {{extracted_value}} and {{extractor_version}}. Does RWB-E1-024 already create {{state}} and {{is_active}}? The unique index {{ux_document_field_active}} needs {{is_active}}.
# *Additions file.* Preconditions say the {{field_definitions}} keys are "recorded in the additions file". Where is this file?
# *ExtractionEvaluationRunner.* Where should {{evaluation/extraction/{runDate}.json}} and the proposed DOCTYPE load file be kept (repo, storage, or attached to the story)? How are they handed to RW-COE or RW-REFADM?
# *MSG-GEN-006.* The story uses it for "The document store is unavailable on read", but the hub defines it for "The reference data store is unavailable". The text is the same. Can we use it for the document store?
# *ACE DB Alignment Tracker v1.* This story is marked "No impact", but its status is "Not started" with "Confirm at the Wave 5 sweep". Must we wait for this confirmation before starting the build?
# *DL10.* Is the Thai text for MSG-P5-003 (shown on SCR-30) available?

### Comment 2: Nate Trakarntanasuk, 2026-11-17T11:37:57.551+0700

Comment ID 1794241

@CHANISSARA MAHAKITTIKUN 

*Clarification needed*: *Possible values for classified type*

_"Can you confirm the exact_ {{doc_type_code}} _value for 'settlement agreement' (is it_ {{SETTLEMENT_AGREEMENT}}_?) — all five other types have a literal code confirmed in the specs, this one doesn't." EX:_ 

* {{COURT_NOTICE}}, {{APPRAISAL_REPORT}}, {{DEMAND_LETTER}}, {{TITLE_DEED}}, {{GUARANTOR_NOTICE}}

*Clarification needed: conflicting HTTP status code for out-of-scope document read*

Both specs use the same message code {{MSG-P4-003}} for a reader whose scope excludes the document's case, but they disagree on the HTTP status:

* *RWB-E1-024* (owns {{GET /documents/{documentId}}} and its authorization) — AC12 / X9 / TC-E1-024-12: out-of-scope read → *403* MSG-P4-003.
* *RWB-E1-053* (reuses the same endpoint, {{NO_API_CHANGE}}, introduces no new authorization logic) — AC13 / TC-E1-053-13: out-of-scope read → *404* MSG-P4-003.

Since RWB-E1-053 doesn't change this endpoint's authorization behavior, it shouldn't have a different expected status than RWB-E1-024 for the same scope-exclusion case. Which status code is correct — 403 or 404 — so we can align both specs and the test case before TC-E1-053-13 is executed?

*Clarification needed:* {{ExtractionEvaluationRunner}} *report — path and schema*

# The evaluation report path {{evaluation/extraction/{runDate}.json}} is recorded as a Technical Specifier decision (agent-run-log A-002, sourced from the legacy story §13) but isn't stated in {{spec.md}} itself — it only says "writes the report and the proposed load file." Can {{spec.md}} be updated to restate the path explicitly, the way RWB-E1-050 does for {{evaluation/classification/{runDate}.json}}?
# Is there a formal JSON schema for this report (field names/types for the per-field precision/recall/extractor-version entries across the 26 fields), or is the narrative description in AC2 ("the report lists precision and recall for each of the 26 fields with the extractor version") the full spec QA should design test data against?
# Separately: is the "proposed DOCTYPE load file" (written alongside the JSON report, marking under-performing fields review-only) expected to follow the existing DOCTYPE load-file format from RWB-E1-025, or does it have its own format?

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T12:45:30.335+0700

Comment ID 1794386

These points add to the spec and QA questions already on this card (anchors, confidence, gateway, DL19, DL26, field not found, report and load file format, 403 vs 404).

# *Proposed load files will be refused.* AC2 builds a DOCTYPE load file that sets {{review_only}} automatically. Even in the RWB-E1-025 format (asked above), RWB-E1-025 refuses any row without Legal and NPA sign-off.
#* Question: what is the flow for COE to obtain sign-off before the proposed file is loaded?
# *Re-extraction on a new DOCTYPE version.* BR8 and the idempotency key use item plus table version, but {{document_intake}} and {{document_field}} in Physical Schema v6 have no table version column.
#* Question: when a new DOCTYPE version adds a field (for example {{court_region}} in RWB-E1-025 AC6), are old documents extracted again?
# *Untyped values and unencrypted personal data.* {{document_field.field_value}} is varchar(1000) with no typed column, and personal values are stored unencrypted. RWB-E1-033 searches "appraised_value > 5,000,000", which needs a cast on every row, and BR9 masks only on read.
#* Proposal: typed value columns, and encryption for personal fields.
# *The case number pattern.* Please check the {{black_case_no}} pattern (2 to 4 letters, space, number / 4-digit year) against real Thai court case numbers, including forms with dots such as ผบ.

Who answers: Henka (BA), Legal, DBA, Security.


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
