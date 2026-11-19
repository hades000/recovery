# TB0001-1211 [RWB-E1-050] Document classification

| Field | Value |
|---|---|
| Jira | [TB0001-1211](https://scbjira.atlassian.net/browse/TB0001-1211) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:46.849+0700 |
| Updated | 2026-11-18T16:29:23.173+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a case owner (RW-CASEOWN), I want each scanned document classified into one of the six agreed types with a confidence score, and any document below the threshold sent to the review queue with its top two candidate types, so that each document is filed under the right type and checklist item without a person typing it.

## Acceptance criteria

```gherkin
Feature: Document classification

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given parameter CLASSIFY_THRESHOLD is 0.80
    Given CLASSIFY_MAX_PAGES is 3 and CLASSIFY_TIMEOUT_SECONDS is 60

  Scenario: AC1 Accuracy
    Given the labeled sample of 180 synthetic documents, 30 of each type, with ocr_status "DONE"
    When ClassificationEvaluationRunner runs on the sample
    Then at least 162 of the 180 documents get the labeled type as predicted_type
    Then the report "evaluation/classification/2026-11-20.json" holds the accuracy, the 6 by 6 confusion matrix and the model version

  Scenario: AC2 Low confidence routed
    Given a scanned intake item whose scores are COURT_NOTICE 0.62, DEMAND_LETTER 0.21 and the rest below 0.10
    When classification runs
    Then the item has predicted_type "COURT_NOTICE", classification_confidence 0.6200 and review_reason "LOW_CONFIDENCE"
    Then type_candidates holds COURT_NOTICE 0.62 and DEMAND_LETTER 0.21
    Then the system passes the item to attach marked for type review, with write_once to be set false on the stored document

  Scenario: AC3 Score at the threshold
    Given a scanned intake item whose top score is APPRAISAL_REPORT 0.80
    When classification runs
    Then the system classifies the item as "APPRAISAL_REPORT" with no review_reason

  Scenario: AC4 Classifier does not answer
    Given the classifier stub does not answer within 60 seconds
    When classification runs for one item
    Then the item has review_reason "MODEL_UNAVAILABLE" and no predicted_type
    Then the item records that the fallback was used

  Scenario: AC5 Type not in the table
    Given the classifier returns "LOAN_CONTRACT" 0.91 for an item
    When classification runs
    Then the item has review_reason "UNKNOWN_TYPE"
    Then type_candidates holds the two highest agreed types

  Scenario: AC6 Upload with a type given
    Given an intake item created from an upload of type "TITLE_DEED"
    When classification runs
    Then the classifier receives no call for it and its type stays "TITLE_DEED"

  Scenario: AC7 Item waiting for rescan
    Given an intake item with ocr_status "RESCAN"
    When classification runs
    Then the classifier receives no call for it

  Scenario: AC8 Repeat run
    Given 20 items already classified
    When JOB-12 runs again
    Then the classifier receives no call for those 20 items and their results are unchanged

  Scenario: AC9 Threshold changed as data
    Given parameter CLASSIFY_THRESHOLD is changed to 0.90 in document_hub_parameter
    Given a scanned item whose top score is COURT_NOTICE 0.85
    When classification runs
    Then the item has review_reason "LOW_CONFIDENCE"
    Then no code or deployment changed between the two values

  Scenario: AC10 Personal identifiers masked before the model call
    Given a scanned page holding the synthetic national ID number "0000000000000" and account number "TEST-ACC-0001"
    When classification runs
    Then the text received by the classifier stub holds tokens in place of both values
```

## Attachments

- [Screenshot 2569-11-16 at 17.39.19.png](../../Attachments/TB0001-1211/Screenshot%202569-11-16%20at%2017.39.19.png) (99220 bytes, Nate Trakarntanasuk, 2026-11-16T17:42:33.256+0700)

## Comments (3)

### Comment 1: Nate Trakarntanasuk, 2026-11-16T17:42:33.457+0700, edited 2026-11-16T17:49:11.839+0700

Comment ID 1793310

@CHANISSARA MAHAKITTIKUN 

*Open QA questions from spec review:*

# Confirming: if a classifier result scores above {{CLASSIFY_THRESHOLD}} but the returned type isn't one of the six types in the table currently in force, it should go to {{UNKNOWN_TYPE}} (not auto-filed), with the two highest-scoring _agreed_ types as candidates — correct?
# For case below the threshold i want to know what dose the two candidates meaning in that case 
!Screenshot 2569-11-16 at 17.39.19.png|width=700,alt="Screenshot 2569-11-16 at 17.39.19.png"!
# {{evaluation/classification/{runDate}.json}} — is there a formal schema for this report beyond "accuracy, confusion matrix, model version"? Checked RWB-E1-060's output; it doesn't contain this yet.
# {{CLASSIFY_THRESHOLD=0.80}} / {{CLASSIFY_MAX_PAGES=3}} / {{CLASSIFY_TIMEOUT_SECONDS=60}} are still pinned to open decision item DL11 (owner: Solution architect with Risk), whose need-by date appears to have passed. Can we get a status update / confirmed values before this moves further?
# TC-E1-050-11 depends on {{GET /documents/{documentId}}} is about access Can I test in this story?
# Component : DocumentIntakeRepository field : *Responsibility* it say From RWB-E1-049; adds the classification columns — It adds in this story or add on RWB-E1-049?

### Comment 2: RACHATAPON PONGANANTAYOTIN, 2026-11-17T12:29:46.278+0700

Comment ID 1794375

@CHANISSARA MAHAKITTIKUN 

Open DEV question from spec review:

# Which model endpoint do we use (Azure OpenAI in the SCB tenant, or the ACE endpoint through AAL)? We need the model, version and route.
## {{ModelGatewayClassifier}} and the evaluation cannot be built without it.
## DL33 / DEP-11 (Open, overdue since 6 Nov)
# Can the ACE PII service tokenize free text (national ID, account, phone numbers)? Neither RWB-E1-037 nor DEP-04 describes that. What is the package and API?
## AC10 and BR6 depend on it. No story builds it, and it does not exist in ACE.
## DEP-04 (Open, due 9 Nov); OPEN-024 (Open)

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T12:36:17.573+0700

Comment ID 1794379

These points add to the QA and dev questions already on this card (UNKNOWN_TYPE, DL11 values, DL33 endpoint, PII service).

# *Two thresholds.* This story uses one CLASSIFY_THRESHOLD in {{document_hub_parameter}}, while RWB-E1-054 uses a {{classify_threshold}} per type in DOCTYPE. Please choose one place.
# *Missing dependency.* Whatever DL33 decides, the gateway itself is built in RWB-E1-058 (agent platform and P10 model gateway), which is groomed on Day 5 and is not in "Depends on". Please add it, so the build order shows that this story runs against a stub until then.
# *Personal data sent to the model.* Even if the ACE PII service is built, it masks ID, account and phone numbers only. Party names, guarantor names and addresses in a court notice or demand letter still go to the model.
#* Question: does Compliance accept this under DL26 and DL33, or must names and addresses be masked too?
# *MODEL_UNAVAILABLE has no retry.* One timeout sends the item to a person, and RWB-E1-032 leaves it as NO_TYPE. If the model is down for half a day, the review queue fills and nothing re-classifies when the model returns.
#* Proposal: retry with back-off, and re-classify NO_TYPE items automatically.
# *The evaluation is on synthetic data.* AC1 measures accuracy on 180 synthetic documents.
#* Proposal: before PROD, evaluate on a masked sample of real scans, with RW-RISK sign-off.
# *Classifier or LLM.* AC5 has the model answer LOAN_CONTRACT, a type outside the list, which suggests a generative model.
#* Question: is this a classifier or an LLM? It changes cost, latency and model risk.

Who answers: AI architect, Compliance, Model Risk, Henka (BA).


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
