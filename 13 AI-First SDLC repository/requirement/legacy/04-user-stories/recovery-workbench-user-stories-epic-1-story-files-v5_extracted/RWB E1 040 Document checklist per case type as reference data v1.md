<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 040 Document checklist per case type as reference data v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 040 Document checklist per case type as reference data v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-040 Document checklist per case type as reference data

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-040 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-16 Hold the document checklist per case type as reference data |
| Requirement IDs | REQ-DCM-011 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.2 |
| Priority | Should |
| Depends on | RWB-E1-024, RWB-E1-043, RWB-E1-025, RWB-E1-026 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read**, so that **a missing document shows on the case without a person checking a list**.

## 2. Business rationale

Litigation packs and guarantee claims fail when a required document is missing, and today the gap is found by a person reading a paper list, often at filing (CTL-19, R-LIT-17). This story holds the checklist per case stage and route as data and keeps a completeness flag per case, recomputed whenever a document is stored or the case changes stage. It meets REQ-DCM-011 and gives the pack checks of Epic 4 and Epic 5 (R-LIT-16, R-GUA-07) one checklist source. The measure is fields extracted without review (FSD P5 A2.16.1).

## 3. Preconditions

- RWB-E1-024 and RWB-E1-026 are done: documents are stored and GET /cases/{caseId}/document-checklist returns the placeholder.
- RWB-E1-025 is done: the six document types are in force.
- RWB-E1-043 is done: the reference data service serves versioned tables with valid from and valid to.
- Checklist version CHK-2026.11 loaded and approved, assumed until the bank list is signed (DL19): stage LITIGATION requires DEMAND_LETTER, COURT_NOTICE, TITLE_DEED and APPRAISAL_REPORT; stage DEED_IN_LIEU requires TITLE_DEED, APPRAISAL_REPORT and SETTLEMENT_AGREEMENT.
- The P3 published interface CaseDirectory returns stage_code, route_code and owner of a case; CaseStateChanged (EV-05) is published by P3.
- Feature flag rwb.dochub.checklist is on.

## 4. Flow

1. Reference data administrator: loads the checklist file with POST /api/recovery/v1/admin/reference-loads, table DOCUMENT_CHECKLIST; the owner approves it.
2. ChecklistLoader: validates every row: stage in LOV-STAGE, route in LOV-ROUTE or empty, document type in the type table in force, no duplicate row; refuses the load whole on any error.
3. ChecklistEvaluator: on DocumentStored (EV-16), on CaseStateChanged (EV-05) and when a checklist version takes effect, takes the case's stage and route through CaseDirectory.
4. ChecklistEvaluator: picks the rows of the version in force for that stage, using the rows for the route where they exist and the rows with no route otherwise.
5. ChecklistEvaluator: counts the active documents of each required type on the case and writes case_document_check: checklist version, required count, present count, missing types and complete.
6. Litigation officer: opens the Documents tab (SCR-30); GET /cases/{caseId}/document-checklist returns each required item marked present or missing.
7. Case owner: sees the number of missing documents for each case on the case list (SCR-02) through DocumentChecklistService.missingCounts.
8. JOB-12 Document intake: the step checklistRefreshStep finds checklist versions whose valid from date has been reached since the last run and recomputes the cases of the stages they change.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case stage has no checklist rows | The checklist shows "No checklist for this case type"; complete is empty | None | AC6 |
| X2 | A checklist load names a document type not in the type table, or a stage not in LOV-STAGE | Load refused in full | MSG-P3-027 | AC7 |
| X3 | The same DocumentStored event arrives twice | One recompute result; the second is ignored and counted | None | AC8 |
| X4 | A document type is present only as an inactive earlier version | Counted once, through its active version | None | AC9 |
| X5 | A role without Documents R opens the checklist | Refused with 403 | MSG-P4-002 | TC-E1-040-10 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store, the types and the placeholder endpoint, all earlier in Epic 1 |
| Negotiable | The items per stage and route are data under DL19; the story fixes how they are applied |
| Valuable | Missing documents show on the case and the case list before a pack is built |
| Estimable | One table, one loader, one evaluator, one stored flag |
| Small | Fits within one week with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Document checklist per case type as reference data

  Background:
    Given checklist version "CHK-2026.11" is in force
    Given stage "LITIGATION" requires DEMAND_LETTER, COURT_NOTICE, TITLE_DEED and APPRAISAL_REPORT
    Given stage "DEED_IN_LIEU" requires TITLE_DEED, APPRAISAL_REPORT and SETTLEMENT_AGREEMENT

  Scenario: AC1 Checklist by type
    Given case "RW-2026-000123" at stage "LITIGATION" holds a demand letter and a court notice
    When the litigation officer opens the Documents tab
    Then the checklist shows the 4 items from version "CHK-2026.11" for "LITIGATION"
    Then DEMAND_LETTER and COURT_NOTICE are marked present
    Then TITLE_DEED and APPRAISAL_REPORT are marked missing

  Scenario: AC2 Change as data
    Given version "CHK-2026.12" adds GUARANTOR_NOTICE for "DEED_IN_LIEU" and is approved with valid from 1 December 2026
    When case "RW-2026-000456" at stage "DEED_IN_LIEU" is opened on 1 December 2026
    Then the checklist shows 4 items including GUARANTOR_NOTICE
    Then no code was deployed between 30 November and 1 December 2026

  Scenario: AC3 Completeness flag
    Given case "RW-2026-000456" at stage "DEED_IN_LIEU" holds a title deed and an appraisal report
    When the pack check runs after the appraisal report is stored
    Then case_document_check for the case has complete false, missing count 1 and missing type SETTLEMENT_AGREEMENT
    Then the case owner sees "1 missing" for the case on the case list

  Scenario: AC4 The missing document arrives
    Given the case from AC3 with SETTLEMENT_AGREEMENT missing
    When a settlement agreement is stored on the case
    Then case_document_check has complete true and missing count 0
    Then the case list shows no missing documents for the case

  Scenario: AC5 Stage change
    Given case "RW-2026-000789" at stage "DEED_IN_LIEU" with complete true
    When CaseStateChanged moves it to stage "LITIGATION"
    Then the pack check uses the "LITIGATION" rows
    Then case_document_check has complete false with the missing litigation types

  Scenario: AC6 No checklist for the stage
    Given case "RW-2026-000321" at stage "DEBT_SALE" and no rows for "DEBT_SALE"
    When the Documents tab opens
    Then the checklist shows "No checklist for this case type"
    Then case_document_check has complete empty and missing count 0

  Scenario: AC7 Load with an unknown type
    Given a load file for table "DOCUMENT_CHECKLIST" with a row for stage "LITIGATION" and type "POWER_OF_ATTORNEY"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming the row and "document type not in the type table"
    Then version "CHK-2026.11" stays in force

  Scenario: AC8 The same event twice
    Given DocumentStored for one document on case "RW-2026-000123" is delivered twice with the same event ID
    When the evaluator handles both
    Then the system writes case_document_check once for that event
    Then the system counts the second delivery as a repeat

  Scenario: AC9 Earlier version of a document
    Given case "RW-2026-000123" holds an appraisal report at version 2 with version 1 inactive
    When the pack check runs
    Then APPRAISAL_REPORT counts as present once
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The checklist per case type is held as reference data so a missing document is visible | REQ-DCM-011; FEAT-DCM-16 |
| BR2 | The case type is the case stage, with route rows taking precedence over rows with no route | LOV-STAGE; LOV-ROUTE; checklist table (New) |
| BR3 | A checklist version takes effect on its valid from date, without a deployment | refdata.txt change process; R-UNI-38; DT02 |
| BR4 | Only active documents count, once per type | FEAT-DCM-20 |
| BR5 | The completeness flag is recomputed on every document stored and every stage change | EV-16; EV-05 |
| BR6 | A repeated event changes nothing | R-UNI-40 |
| BR7 | The checklist is the source the pack checks read in later epics | R-LIT-16, R-LIT-17, R-GUA-07, R-GUA-08 |

## 9. State transitions

None. This story does not change a case status. It writes the completeness flag of the case in case_document_check: complete false while a required type is missing, true when every required type is present, empty when the stage has no checklist.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads the checklist (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the legal counsel as co-owner of the checklist (DL01) |
| RW-LITOFF, RW-CASEOWN and roles with Documents R | Read the checklist and the flag for cases in their scope |
| RW-LEGAL, legal counsel | Agrees the items per stage (DL19) |
| SY-CASEWF | Publishes CaseStateChanged that triggers the recompute |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-006 | recovery_case | stage_code | Read, through CaseDirectory |
| DF-CAS-008 | recovery_case | route_code | Read, through CaseDirectory |
| DF-CAS-009 | recovery_case | owner_user_id | Read, through CaseDirectory |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| Standard column | document | is_active | Read |
| DF-REF-234 to DF-REF-243 | document_checklist_item | all fields | Write (this story creates the record) |
| DF-DOC-036 to DF-DOC-044 | case_document_check | all fields | Write (this story creates the record) |
| DF-REF-219 | document_type | doc_type_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}/document-checklist** (new, see additions; this story fills the required items)

| Item | Value |
|---|---|
| Request | Path caseId |
| Response | 200 DocumentChecklist: caseId, checklistVersion, stageCode, items [documentType, label, required, presentCount], missingCount, complete |
| Errors | 401; 403 no Documents R (MSG-P4-002) or out of scope (MSG-P4-003); 404; 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**POST /api/recovery/v1/admin/reference-loads** (table DOCUMENT_CHECKLIST)

| Item | Value |
|---|---|
| Request | multipart/form-data: file, table = "DOCUMENT_CHECKLIST", validFrom |
| Response | 201 ReferenceLoad |
| Errors | 401; 403 (MSG-P4-002); 409 version already loaded (MSG-P3-027); 422 row errors (MSG-P3-027); 503 |
| Authorization | Reference data, right C; approval with right A |
| Idempotency | Table code and table version |

**Listener**

| Item | Value |
|---|---|
| Events consumed | DocumentStored (EV-16); CaseStateChanged (EV-05) |
| Idempotency key | Event ID; a repeat is ignored and counted (R-UNI-40) |
| Restart behavior | A failed handling retries; after the retry limit the event goes to the exception queue with the platform administrator as owner |

**Published interface (P5, used by the P3 case list and by RWB-E1-054)**

```java
public interface DocumentChecklistService {
    CaseChecklist forCase(UUID caseId, LocalDate businessDate);
    Map<UUID, Integer> missingCounts(Collection<UUID> caseIds);   // at most 500 IDs per call
}
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/checklist`, Java package `recovery.dochub.checklist`; front end folder `recovery/documents`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| ChecklistLoader | Service | Implements ReferenceTableLoader for DOCUMENT_CHECKLIST |
| ChecklistEvaluator | Service | Picks the rows for the stage and route; counts documents; writes case_document_check |
| DocumentStoredChecklistListener, CaseStateChangedChecklistListener | Listener | Call the evaluator; keep the event ID for repeats |
| ChecklistRefreshStep | Job | Step of JOB-12 that recomputes cases when a version takes effect |
| DocumentChecklistService | Published interface | Section 12 |
| ChecklistRepository, CaseDocumentCheckRepository | Repository | Read and write the two new tables only |
| DocumentChecklistPanel | React component | Replaces the placeholder on SCR-30 with required items present or missing |
| MissingDocumentsBadge | React component | Count shown on the SCR-02 case list rows |

**Database.**
- Flyway migration `V1_5_040__document_checklist.sql` creates document_checklist_item (id, stage_code varchar(20), route_code varchar(4), document_type varchar(30), required boolean, sort_order integer, table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (stage_code, route_code, document_type, table_version); and case_document_check (id, case_id uuid, checklist_version varchar(20), required_count integer, present_count integer, missing_types jsonb, complete boolean, checked_at timestamptz, last_event_id uuid, standard columns) with unique (case_id).
- Index ix_checklist_stage on document_checklist_item (stage_code, valid_from).

**Configuration and reference data.**
- Checklist CHK-2026.11, prepared by the reference data administrator, agreed with legal counsel and the litigation officers (DL19).
- No property beyond the feature flag.

**Build steps.**
1. Write the migration; test the unique keys.
2. Build ChecklistLoader with validation against LOV-STAGE, LOV-ROUTE and the type table; test AC7.
3. Build ChecklistEvaluator with the route precedence and the active-version rule; unit test AC1, AC6 and AC9.
4. Build the two listeners with the repeat check; test AC3, AC4, AC5 and AC8.
5. Build ChecklistRefreshStep; test AC2 on 30 November and 1 December 2026.
6. Extend the checklist endpoint and build DocumentChecklistPanel and MissingDocumentsBadge; component tests and the access test.

**Feature flag.** `rwb.dochub.checklist`. Off: the endpoint returns the RWB-E1-026 placeholder and no flag is written.

**Done when.** The tests in section 16 pass and the case list shows the missing count for the synthetic litigation cases in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-023 | Required documents are missing on the case | {count} required documents are missing for this case: {types}. |
| MSG-P3-027 | Checklist load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-30 Case documents | list | The checklist panel with each required type present or missing, and MSG-P5-023 above it when a type is missing |
| SCR-30 Case documents | Loading | Skeleton rows while the checklist loads |
| SCR-02 Case list | list | A "Documents missing" count per case; 0 shows as empty |
| SCR-02 Case list | filtered | The user can filter cases with one or more missing documents |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-040-01 | AC1, BR1, BR2 | System | Litigation case with a demand letter and a court notice |
| TC-E1-040-02 | AC2, BR3 | System | Version CHK-2026.12 valid from 1 December 2026 |
| TC-E1-040-03 | AC3, BR5 | System | Deed in lieu case with two of three types |
| TC-E1-040-04 | AC4, BR5 | System | Settlement agreement stored on that case |
| TC-E1-040-05 | AC5, BR5 | System | Stage change from DEED_IN_LIEU to LITIGATION |
| TC-E1-040-06 | AC6 | System | Case at DEBT_SALE with no rows |
| TC-E1-040-07 | AC7 | System | Row with POWER_OF_ATTORNEY |
| TC-E1-040-08 | AC8, BR6 | System | DocumentStored delivered twice |
| TC-E1-040-09 | AC9, BR4 | System | Appraisal report with two versions |
| TC-E1-040-10 | Access | Access | Capacity and workforce planner (RW-CAPACITY, no Documents right) opens the checklist; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: stages, routes and required types are rows in document_checklist_item.
- No personal data in logs, tests or prompts: the flag holds type codes and counts only.
- No read of another module's tables: stage, route and owner come through CaseDirectory; P3 reads the flag through DocumentChecklistService.
- The evaluator never blocks a case move; it reports only.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-011 | Checklist per case type as reference data so a missing document is visible | Business Requirements Epic 1, section 3.5 | FEAT-DCM-16 | 13 Manage documents and correspondence | R-UNI-38, R-UNI-40, R-LIT-16, R-LIT-17 | TC-E1-040-01 to TC-E1-040-10 |

## 19. Out of scope

- The litigation pack check against the defect list and the block at filing (FEAT-LIT-05, Epic 5; CTL-19).
- The guarantee claim checklist (FEAT-GUA-01, Epic 4).
- Retrieval requests for missing documents (R-LIT-17, Epic 5).
- The review queue screen that shows the case checklist (RWB-E1-054).
