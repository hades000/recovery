<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 023 Case record view v1 read only v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 023 Case record view v1 read only v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-023 Case record view v1, read only

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-023 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-ACA-11 Show the case record view read only |
| Requirement IDs | REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.3, 3.4 and 3.6; Business Requirements Program, sections 5.1, 5.4 and 5.6 |
| L3 process | 06 Take over and own the case |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 open |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039, RWB-E1-068, RWB-E1-069 |
| Status | Ready for build, the freshness line behind a flag until RWB-ACE-001 lands (DL43) |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read live from the ACE views by business key with the business date of each**, so that **I stop searching files and systems to understand a case**.

## 2. Business rationale

A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. Under D-RCV-35 the Workbench holds no copy of the account, the customer or the contact point: the screen reads `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` by `account_key` and `person_key`. The identity number is already masked inside `v_ace_customer` (`id_no_masked` and `id_no_last4`) and the contact values are masked at the API by role (RWB-E1-037), so no clear personal value is copied into a Workbench table or a screen cache. This story puts the case, its accounts and arrears, its parties and contacts, its contact history and its documents on SCR-03, each section showing the ACE business date behind it, and writes every view of personal data to the access log. It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005 and REQ-ACA-006.

## 3. Preconditions

- RWB-E1-018 is done: cases exist with `account_key` links on case_account and `person_key` links on case_party.
- RWB-E1-024 is done: the document hub lists documents by case.
- RWB-E1-068 is done: the interaction ledger reads back through its published interface.
- RWB-E1-037 is done: the masking rules by role are in force (DL26) and name the view field IDs.
- RWB-E1-039 is done: access events are published to the access log.
- RWB-E1-069 is done: `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` are Section A views. `v_ace_batch_status` is a Section B view, so the freshness banner stays behind its flag until RWB-ACE-001 lands (DL43).
- The account, customer and contact views carry the ACE business date: `v_ace_account.data_as_of` and the ALS, SCBPDM and EFS rows in `v_ace_batch_status`.
- `recovery_svc` holds SELECT on `recovery.v_ace_*` and no privilege on `public`.
- The user holds a role with Case record R and the case is in the user's scope.
- Personal data access is logged through AccessEventPublisher (RWB-E1-039), which also sends the PII access record to PII Kafka through the ACE common module.

## 4. Flow

1. Case owner: opens a case from SCR-02 Case list; SCR-03 shows the Loading state.
2. CaseRecordPage: calls GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/interactions and GET /cases/{caseId}/documents in parallel.
3. CaseAndWorkflowController: checks Case record R and the scope; out of scope returns 404.
4. CaseRecordQueryService: reads the header from recovery_case and the links from case_account and case_party.
5. CaseRecordQueryService: reads the account facts from `v_ace_account` by `account_key`, the customer facts from `v_ace_customer` by `person_key` and the contact points from `v_ace_contact` by `person_key` and `contact_type`; every row carries the ACE business date from `data_as_of` or from `v_ace_batch_status`.
6. CaseRecordQueryService: reads the collections history from `v_ace_efs_action` by `account_key` and the Workbench entries through InteractionLedgerReader (RWB-E1-068), and merges them into one contact history ordered by time, each row carrying its source system.
7. MaskingApplier: fills each personal field from the masked or the clear view column for the caller's role through FieldMasker, and publishes one AC-READ access event with the field IDs read and their masked flags. A read whose event cannot be written returns nothing.
8. DocumentHub (P5): returns the document list for the case through its endpoint.
9. CaseRecordPage: shows the header (case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags), then Accounts, Parties with their contact points, Contact history and Documents, each with its ACE business date (read only state).
10. CaseRecordPage: shows the stale banner with MSG-P1-001 on any section whose ACE batch is not COMPLETE for the latest business date, and no Workbench load or job status anywhere.
11. CaseRecordPage: shows the on hold banner with MSG-P3-004 when the case is on hold.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch behind a section is not COMPLETE for the latest business date | Section shows with its business date and the stale banner | MSG-P1-001 | AC4 |
| X2 | The case is outside the user's scope | 404; nothing shows | MSG-P4-003 | AC5 |
| X3 | The document hub does not answer | Documents section shows the section message; the rest shows | MSG-P3-023 | AC6 |
| X4 | The access event cannot be written | The read is refused; no case data and no personal field shows | MSG-P7-003 | AC7 |
| X5 | The role may not see a personal field in clear | The field shows from the masked view column | None | AC8 |
| X6 | The case is on hold | On hold banner with the prescription date | MSG-P3-004 | AC9 |
| X7 | The case has no documents and no contact history | Each section shows its empty sentence | MSG-P3-024 | AC10 |
| X8 | A role without Case record R opens the view | Refused with 403 | MSG-P4-002 | Access test TC-E1-023-11 |
| X9 | A case link holds an `account_key` that `v_ace_account` does not return | The Accounts row shows the key with empty values; REC-05 lists it; the rest shows | None | AC12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads data other stories write; no write in this story |
| Negotiable | Section order and the masking rules are data and design choices |
| Valuable | One screen answers the case owner's first questions, from the same ACE rows every other module reads |
| Estimable | One page, five read endpoints, one query service, four views |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Case record view v1, read only

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest ACE batch business date is 2026-12-02 and v_ace_batch_status shows the ALS, SCBPDM and EFS batches COMPLETED for it

  Scenario: AC1 Loads fast
    Given case RW-2026-000701 has 50 documents and 120 contact history entries
    When U-81 opens the case record view
    Then the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings

  Scenario: AC2 Data from ACE
    Given v_ace_account holds days_past_due 97, total_balance THB 206,175.00 and data_as_of 2026-12-02 for account A-7001
    When the view opens
    Then the Accounts section shows 97 days past due and THB 206,175.00 for A-7001
    Then the section shows business date 2026-12-02 read from v_ace_account.data_as_of
    Then the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30

  Scenario: AC3 Customer and contacts from ACE
    Given v_ace_customer holds person_key P-7001 with first_name "Anan", last_name "Sukjai", category "RETAIL" and id_no_masked "XXXXXXXXX4821"
    Given v_ace_contact holds a mobile for P-7001 with contact_key "PHONE:88421" and contact_value "0812345678"
    When the view opens
    Then the Parties section shows the borrower with role "BORROWER", category "RETAIL" and business date 2026-12-02
    Then the borrower's contact points show from v_ace_contact with their contact_type and usage_code
    Then the contact history shows the v_ace_efs_action entries with action code, time and promise status

  Scenario: AC4 Stale ACE batch
    Given v_ace_batch_status holds no COMPLETED ALS row for 2026-12-03 and v_ace_account.data_as_of is 2026-12-02
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows business date 2026-12-02
    Then the stale banner shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-02
    Then no Workbench load or job status shows

  Scenario: AC5 Case outside the scope
    Given case RW-2026-000702 belongs to team "LIT-BKK" and U-81 has scope Own
    When U-81 opens case RW-2026-000702
    Then the response is 404 with MSG-P4-003
    Then no case data shows

  Scenario: AC6 Document hub unavailable
    Given the document hub does not answer within 3 seconds
    When U-81 opens the view
    Then the Documents section shows MSG-P3-023 for "Documents"
    Then the header, accounts, parties and contact history show

  Scenario: AC7 The access event cannot be written
    Given the access event stream rejects every write
    When U-81 opens the view
    Then the call returns status 503 with MSG-P7-003 and no case data
    Then no personal field shows

  Scenario: AC8 Masking by role
    Given phone collector U-82 holds no masking rule that lets RW-PHONECOL see DF-ACE-078 in clear
    Given the case is in U-82's scope
    When U-82 opens the view
    Then the identity shows "XXXXXXXXX4821" from v_ace_customer.id_no_masked
    Then the phone shows "XXXXXX5678" from v_ace_contact.contact_value_masked
    Then the access log holds the read with user U-82, the field IDs and the masked flags

  Scenario: AC9 Case on hold
    Given case RW-2026-000701 has status "ON_HOLD" for deviation X1 with prescription date 2028-03-15
    When U-81 opens the view
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15

  Scenario: AC10 No documents and no contact history
    Given case RW-2026-000703 has no documents and no contact history
    When its owner opens the view
    Then the Documents and Contact history sections each show MSG-P3-024

  Scenario: AC11 No copy of the account on the case
    Given the balance of account A-7001 for case RW-2026-000701 was THB 206,175.00 on 2026-12-02
    Given the ALS batch for 2026-12-03 holds THB 210,000.00 for A-7001
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows THB 210,000.00 and business date 2026-12-03
    Then no Workbench table holds the previous balance for the case

  Scenario: AC12 An account link with no ACE row
    Given case RW-2026-000701 links account_key A-7010
    Given v_ace_account holds no row for A-7010
    When U-81 opens the view
    Then the Accounts section shows A-7010 with empty balance and days past due
    Then the rest of the case shows
    Then REC-05 lists account_key A-7010 for the data steward and the ACE team
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every section shows the ACE business date behind it, read from `v_ace_account.data_as_of` or from `v_ace_batch_status`; no Workbench load date is used | REQ-RDF-009; VR-P3-001-1 |
| BR2 | A section whose ACE batch is not COMPLETE for the latest business date shows the stale banner | MSG-P1-001; screens.txt Common states "Stale input"; v_ace_batch_status |
| BR3 | A personal field shows from the masked view column unless the masking rule in force lets the role see it in clear; the identity number is never in clear because `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only | REQ-ACA-005; CTL-11; DL26; DF-ACE-073, DF-ACE-074 |
| BR4 | Every read of personal data is written to the access log; a read whose event cannot be written returns no data | REQ-ACA-006; RWB-E1-039 BR2 |
| BR5 | Only cases in the caller's scope open; others return 404 | CTL-09; REQ-ACA-009 |
| BR6 | The view has no edit control in Epic 1 | SCR-03 "E1 read only" |
| BR7 | The view loads in under 2 seconds with 50 documents | NFR-009 |
| BR8 | Account, customer, contact and collections history data are read live from `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` by business key; the Workbench holds no copy and shows no Workbench load status | D-RCV-35 U1 and U4; ADR-010 |
| BR9 | A case link with no view row shows the business key with empty values and is listed by REC-05; it is never deleted or rewritten | REC-05; Data Tier Map section 5 |
| BR10 | The contact history merges the ACE EFS entries and the Workbench interaction ledger in one time order, each row naming its source system | E1-068; interaction.source_system (DF-INT-013) |

## 9. State transitions

None. This story does not change a case status. It reads the case and shows its status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Opens cases in scope Own (Case record R) |
| RW-TEAMMGR | Opens cases in scope Team |
| RW-PHONECOL | Opens cases in scope Own, read only, with masking |
| RW-CONDUCT, RW-AUDIT | Open every case (scope All) |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| recovery_svc, recovery service identity | Reads `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` through the P1 query; SELECT only |
| ACE team lead | Owns the ACE tables and columns behind the four views |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-CAS-027 | case_account | is_primary | Read |
| DF-CAS-032 | case_party | person_key | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-055 | v_ace_customer | cif_no | Read |
| DF-ACE-057 | v_ace_customer | first_name | Read, masked by role |
| DF-ACE-058 | v_ace_customer | last_name | Read, masked by role |
| DF-ACE-059 | v_ace_customer | date_of_birth | Read, masked by role |
| DF-ACE-068 | v_ace_customer | category | Read |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read |
| DF-ACE-074 | v_ace_customer | id_no_last4 | Read, only with the personal-data permission |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read, only with the personal-data permission |
| DF-ACE-079 | v_ace_contact | contact_value_masked | Read |
| DF-ACE-080 | v_ace_contact | usage_code | Read |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-112 | v_ace_efs_action | action_code_name | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-116 | v_ace_efs_action | comments | Read, masked by role |
| DF-ACE-117 | v_ace_efs_action | is_call | Read |
| DF-ACE-120 | v_ace_efs_action | promise_status | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-INT-004 | interaction | occurred_at | Read through RWB-E1-068 |
| DF-INT-005 | interaction | channel | Read through RWB-E1-068 |
| DF-INT-008 | interaction | contact_result | Read through RWB-E1-068 |
| DF-INT-013 | interaction | source_system | Read through RWB-E1-068 |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-005 | document | source | Read |
| DF-DOC-011 | document | doc_version | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v7. DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v5.

## 12. Contract

| Endpoint | Request | Response | Errors | Authorization |
|---|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId} | Path caseId | Case | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 503 | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/accounts | Path caseId | CaseAccount[] with accountNo, daysPastDue, totalBalance, dataAsOf read from `v_ace_account` by `account_key` (see additions) | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/parties | Path caseId | CasePartyView[]: personKey, partyRole, displayName, customerNo, idNo or idNoLast4, category, contacts[] with contactType, contactKey, contactValue by role and dataAsOf (see additions) | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/interactions | Path caseId; query channel, from, to, page, size | ContactHistoryPage: the ACE EFS entries from `v_ace_efs_action` and the ledger entries from RWB-E1-068, ordered by time, each with sourceSystem | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/documents | Path caseId; query type, page, size | DocumentPage (P5) | Same | Documents R, scope applied |

Idempotency: not applicable; every endpoint is a read.

```java
// P1, used by this story (RWB-E1-016); every method reads recovery.v_ace_*
public interface AceSourceQuery {
    List<AceAccountView> accountsFor(List<String> accountKeys);              // v_ace_account
    List<AceCustomerView> customersFor(List<String> personKeys);             // v_ace_customer
    List<AceContactView> contactsFor(String personKey, String contactType);  // v_ace_contact
    List<AceEfsActionView> actionsFor(List<String> accountKeys);             // v_ace_efs_action
}
// P4, package recovery.access.matrix (RWB-E1-037)
<T> T mask(T dto, SessionContext session);               // FieldMasker, fills from the masked or clear view column
ScopeFilter scopeFor(SessionContext session);            // ScopeService
// P4, package recovery.access.accesslog (RWB-E1-039)
public interface AccessEventPublisher {
    void publish(AccessEvent event) throws DecisionLogUnavailableException;   // eventCode AC-READ with field IDs and masked flags
}
// P3, package recovery.casewf.interaction (RWB-E1-068)
public interface InteractionLedgerReader {
    InteractionPage read(UUID caseId, InteractionFilter filter);
}
```

## 13. Solution plan

**Package.** Back end `recovery/casewf/caserecord` (Java package `recovery.casewf.caserecord`); front end `src/modules/recovery/casewf/caserecord`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | The four P3 read endpoints with access check and scope |
| CaseRecordQueryService | Service | Composes case, accounts, parties with contacts and contact history; adds the ACE business date per section |
| AceSourceReader | Repository | Reads `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` by business key; SELECT only |
| MaskingApplier | Service | Calls FieldMasker (RWB-E1-037) and publishes AC-READ through AccessEventPublisher; refuses the read when the publish fails |
| CaseAndWorkflowRepository | Repository | recovery_case, case_account, case_party, queue |
| CaseRecordPage | React component | SCR-03 read only layout with Loading, read only and on hold states |
| CaseHeader, AccountsPanel, PartiesPanel, ContactHistoryPanel, DocumentsPanel | React component | One section each, each with an AceDataDateBadge |
| StaleBanner, OnHoldBanner, SectionMessage | React component | MSG-P1-001, MSG-P3-004, MSG-P3-023 and MSG-P3-024 |

**Database**

- Reads recovery_case, case_account, case_party and queue only, plus the four views through AceSourceReader. Uses ix_interaction_case_time in RWB-E1-068 for the ledger part of the contact history.
- No migration.

**Configuration and reference data**

- Masking rules over the view field IDs (RWB-E1-037; DL26), labels (DL10), LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE, LOV-PARTY-ROLE.
- Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11) from RWB-E1-042.

**Build steps**

1. AceSourceReader with the four view reads by `account_key` and `person_key`; test the join and the business date for AC2, AC3, AC12.
2. CaseRecordQueryService with the section composition and the merged contact history; tests AC2, AC3, AC10.
3. MaskingApplier with the access log call and the refusal path; tests AC7, AC8.
4. Scope check returning 404; test AC5.
5. CaseRecordPage with parallel calls, per-section timeout and section messages; tests AC6, AC10.
6. StaleBanner and OnHoldBanner over `v_ace_batch_status`; tests AC4, AC9.
7. No-copy and performance tests with 50 documents and 120 EFS entries; tests AC1, AC11.
8. Access test.

**Feature flag.** `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only. The stale banner reads a Section B view, so it is on only after RWB-ACE-001 lands and V0003 creates `v_ace_batch_status` (DL43).

**Done when.** The tests in section 16 pass and the view meets NFR-009 in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A section's ACE batch is not complete for the latest business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P3-004 | Case on hold | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-024 | A section has nothing to show | Nothing is recorded in {section} yet. |
| MSG-P3-023 | A section cannot be shown | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

## 15. Screens and states

SCR-03 Case record. Loading: skeleton rows per section. Read only: fields without edit controls; the header and five sections, each with the ACE business date of its source. On hold: the banner with the deviation or legal hold and the prescription date. Stale input: MSG-P1-001 above the section when the ACE batch is not complete. Error: MSG-P3-023 in the section that failed. The screen shows no Workbench load, job or file status.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-01 | AC1, BR7 | System | Case with 50 documents and 120 EFS entries |
| TC-E1-023-02 | AC2, BR1 | System | `v_ace_account` A-7001 at 97 days past due, data_as_of 2026-12-02 |
| TC-E1-023-03 | AC3, BR8 | System | `v_ace_customer` P-7001 with category RETAIL, `v_ace_contact` mobile, EFS entries |
| TC-E1-023-04 | AC4, BR2 | System | No COMPLETED ALS row for 2026-12-03, data_as_of 2026-12-02 |
| TC-E1-023-05 | AC5, BR5 | System | Case of team LIT-BKK, user with scope Own |
| TC-E1-023-06 | AC6 | System | Document hub not answering |
| TC-E1-023-07 | AC7, BR4 | System | Access event stream rejecting every write |
| TC-E1-023-08 | AC8, BR3 | System | Phone collector without the personal-data permission |
| TC-E1-023-09 | AC9 | System | Case on hold for X1 |
| TC-E1-023-10 | AC10 | System | Case with no documents and no history |
| TC-E1-023-11 | Access | Access | RW-REFADM calls GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-023-12 | AC11, BR8 | System | A-7001 balance changed by the 2026-12-03 ALS batch |
| TC-E1-023-13 | AC12, BR9 | System | Case link A-7010 with no `v_ace_account` row |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: masking rules, labels and timeouts are data.
- No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only.
- ACE data only through the `recovery.v_ace_*` views: account, customer, contact and collections history come from `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action`, and freshness from `v_ace_batch_status`. The recovery schema holds no foreign key into a `public` table.
- The view holds no copy of a source record and caches no clear personal value; the identity number is masked inside the view and the contact values are masked at the API by role.
- Personal fields are never shown when the access event cannot be written.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | Case record view with account, arrears, owner, queue, stage, status, contact history and documents | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-01, TC-E1-023-02, TC-E1-023-03, TC-E1-023-06, TC-E1-023-09, TC-E1-023-10 |
| REQ-RDF-009 | Every data product carries a freshness stamp | Epic 1, 3.1; Program, 5.1 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-02, TC-E1-023-04 |
| REQ-ACA-005 | Personal data masked by role | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-07, TC-E1-023-08 |
| REQ-ACA-006 | Every read of the case store written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-05, TC-E1-023-08 |
| D-RCV-35 U1 and U4 | The view reads account, customer, contact and collections history only through the `recovery.v_ace_*` views, by business key, and copies nothing | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-ACA-11 | 06 Take over and own the case | ADR-010; CTL-02 | TC-E1-023-12, TC-E1-023-13 |

## 19. Out of scope

- The history timeline on the case view (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Writing a Workbench entry to the interaction ledger (RWB-E1-066, RWB-E1-067).
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF ingestion lands in ACE).
