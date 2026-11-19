# RWB-E1-023 Case record view v1, read only

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read from the data products with the business date of each**, so that **I stop searching files and systems to understand a case**.

## 2. Business rationale

A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. This story puts the case, its accounts and arrears, its parties, its contact history and its documents on SCR-03, each section showing the business date of the data product it comes from, with personal fields masked by role and every view of personal data written to the access log. It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005 and REQ-ACA-006.

## 3. Preconditions

- RWB-E1-018 is done: cases, account links and party links exist.
- RWB-E1-024 is done: the document hub lists documents by case.
- RWB-E1-037 is done: masking rules by role are in force (DL26).
- RWB-E1-039 is done: access events are published to the access log.
- The account, arrears and party data products carry their data_as_of date from the COLLINS load (DL20).
- The user holds a role with Case record R and the case is in the user's scope.
- Personal data access is logged through AccessEventPublisher (RWB-E1-039), which also sends the PII access record to PII Kafka through the ACE common module.

## 4. Flow

1. Case owner: opens a case from SCR-02 Case list; SCR-03 shows the Loading state.
2. CaseRecordPage: calls GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/interactions and GET /cases/{caseId}/documents in parallel.
3. CaseAndWorkflowController: checks Case record R and the scope; out of scope returns 404.
4. CaseRecordQueryService: reads the case from P3 tables, and the account balances, arrears and party facts through the P1 interface with their data_as_of dates.
5. CaseRecordQueryService: applies the masking rules for the caller's role through FieldMasker and publishes one AC-READ access event with the field IDs read and their masked flags.
6. DocumentHub (P5): returns the document list for the case through its endpoint.
7. CaseRecordPage: shows the header (case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags), then Accounts, Parties, Contact history and Documents, each with its business date (read only state).
8. CaseRecordPage: shows the stale banner with MSG-P1-001 on any section whose business date is before the latest business date.
9. CaseRecordPage: shows the on hold banner with MSG-P3-004 when the case is on hold.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product is from an earlier date | Section shows with its date and the stale banner | MSG-P1-001 | AC4 |
| X2 | The case is outside the user's scope | 404; nothing shows | MSG-P4-003 | AC5 |
| X3 | The document hub does not answer | Documents section shows the section message; the rest shows | MSG-P3-023 | AC6 |
| X4 | The personal data access log cannot be written | Personal fields stay masked; the rest shows | MSG-P3-023 | AC7 |
| X5 | The role may not see a personal field unmasked | Field shows masked | None | AC8 |
| X6 | The case is on hold | On hold banner with the prescription date | MSG-P3-004 | AC9 |
| X7 | The case has no documents and no contact history | Each section shows its empty sentence | MSG-P3-024 | AC10 |
| X8 | A role without Case record R opens the view | Refused with 403 | MSG-P4-002 | Access test TC-E1-023-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads data other stories write; no write in this story |
| Negotiable | Section order and the masking rules are data and design choices |
| Valuable | One screen answers the case owner's first questions |
| Estimable | One page, five read endpoints, one query service |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Case record view v1, read only

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest business date is 2026-12-02

  Scenario: AC1 Loads fast
    Given case RW-2026-000701 has 50 documents and 120 contact history entries
    When U-81 opens the case record view
    Then the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings

  Scenario: AC2 Data from products
    Given the account data product for 2026-12-02 holds days past due 97 and total balance THB 206,175.00 for account A-7001
    When the view opens
    Then the Accounts section shows 97 days past due and THB 206,175.00 for A-7001
    Then the section shows business date 2026-12-02
    Then the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30

  Scenario: AC3 Customer facts from the load
    Given the customer profile for the borrower arrived in the COLLINS load of 2026-12-02
    When the view opens
    Then the Parties section shows the borrower with role "BORROWER", segment "RETAIL" and business date 2026-12-02
    Then the contact history shows the EFS entries with channel, direction, result and time

  Scenario: AC4 Stale data product
    Given the COLLINS load for 2026-12-03 was refused and the account data product is from 2026-12-02
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows business date 2026-12-02
    Then the stale banner shows MSG-P1-001 for the account data product with date 2026-12-02

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

  Scenario: AC7 Personal data access log unavailable
    Given the personal data access log cannot be written
    When U-81 opens the view
    Then the borrower's name and customer number show masked
    Then the Parties section shows MSG-P3-023 for "Personal details"

  Scenario: AC8 Masking by role
    Given phone collector U-82 may not see the customer number unmasked
    Given the case is in U-82's scope
    When U-82 opens the view
    Then the customer number shows masked as "xxxxxx4821"
    Then the access log holds the read with user U-82 and the masked result

  Scenario: AC9 Case on hold
    Given case RW-2026-000701 has status "ON_HOLD" for deviation X1 with prescription date 2028-03-15
    When U-81 opens the view
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15

  Scenario: AC10 No documents and no contact history
    Given case RW-2026-000703 has no documents and no contact history
    When its owner opens the view
    Then the Documents and Contact history sections each show MSG-P3-024
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every section shows the business date of the data product it reads | REQ-RDF-009; VR-P3-001-1 |
| BR2 | A section older than the latest business date shows the stale banner | MSG-P1-001; screens.txt Common states "Stale input" |
| BR3 | Personal fields show masked unless the role may see them | REQ-ACA-005; CTL-11; DL26 |
| BR4 | Every read of personal data is written to the access log | REQ-ACA-006 |
| BR5 | Only cases in the caller's scope open; others return 404 | CTL-09; REQ-ACA-009 |
| BR6 | The view has no edit control in Epic 1 | SCR-03 "E1 read only" |
| BR7 | The view loads in under 2 seconds with 50 documents | NFR-009 |
| BR8 | Customer facts come from the profile ACE receives through COLLINS | DL20 |

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
| SY-CASEWF | Reads P1 data through the published interface |

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
| DF-CAS-026 | case_account | account_id | Read |
| DF-CAS-027 | case_account | is_primary | Read |
| DF-CAS-032 | case_party | party_id | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-ACC-002 | loan_account | account_no | Read |
| DF-ACC-009 | loan_account | principal_outstanding | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-015 | loan_account | bucket | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-PTY-002 | party | cif_no | Read |
| DF-PTY-004 | party | first_name | Read |
| DF-PTY-005 | party | last_name | Read |
| DF-PTY-009 | party | segment | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-013 | interaction | source_system | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-005 | document | source | Read |
| DF-DOC-011 | document | doc_version | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Endpoint | Request | Response | Errors | Authorization |
|---|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId} | Path caseId | Case | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 503 | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/accounts | Path caseId | CaseAccount[] with new fields accountNo, daysPastDue, principalOutstanding, totalBalance, bucket, dataAsOf (see additions) | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/parties | Path caseId | CaseParty[] masked by role, with new fields displayName, customerNo, segment, dataAsOf (see additions) | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/interactions | Path caseId; query channel, from, to, page, size | InteractionPage | Same | Case record R, scope applied |
| GET /api/recovery/v1/cases/{caseId}/documents | Path caseId; query type, page, size | DocumentPage (P5) | Same | Documents R, scope applied |

Idempotency: not applicable; every endpoint is a read.

```java
// P1, used by this story
public interface RecoveryDataQuery {
    List<AccountView> accountsFor(List<UUID> accountIds);       // balances, arrears, data_as_of
    List<PartyView> partiesFor(List<UUID> partyIds);            // profile facts, data_as_of
}
// P4, package recovery.access.matrix (RWB-E1-037)
<T> T mask(T dto, SessionContext session);               // FieldMasker
ScopeFilter scopeFor(SessionContext session);            // ScopeService
// P4, package recovery.access.accesslog (RWB-E1-039)
public interface AccessEventPublisher {
    void publish(AccessEvent event) throws DecisionLogUnavailableException;   // eventCode AC-READ with field IDs and masked flags
}
```

## 13. Solution plan

**Package.** Back end `recovery/casewf/caserecord` (Java package `recovery.casewf.caserecord`); front end `src/modules/recovery/casewf/caserecord`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | The four P3 read endpoints with access check and scope |
| CaseRecordQueryService | Service | Composes case, accounts, parties and interactions; adds data_as_of per section |
| MaskingApplier | Service | Calls FieldMasker (RWB-E1-037) and publishes AC-READ through AccessEventPublisher; masks every personal field when the publish fails |
| CaseAndWorkflowRepository | Repository | recovery_case, case_account, case_party, interaction, queue |
| CaseRecordPage | React component | SCR-03 read only layout with Loading, read only and on hold states |
| CaseHeader, AccountsPanel, PartiesPanel, ContactHistoryPanel, DocumentsPanel | React component | One section each, each with a DataDateBadge |
| StaleBanner, OnHoldBanner, SectionMessage | React component | MSG-P1-001, MSG-P3-004, MSG-P3-023 and MSG-P3-024 |

**Database**

- Reads recovery_case, case_account, case_party, interaction, queue only. Uses ix_interaction_case_time for the contact history page.
- No migration.

**Configuration and reference data**

- Masking rules (RWB-E1-037; DL26), labels (DL10), LOV-CHANNEL, LOV-CONTACT-RESULT, LOV-PARTY-ROLE.
- Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11) from RWB-E1-042.

**Build steps**

1. CaseRecordQueryService with P1 reads and data_as_of per section; tests AC2, AC3.
2. MaskingApplier with the access log call and the masked fallback; tests AC7, AC8.
3. Scope check returning 404; test AC5.
4. CaseRecordPage with parallel calls, per-section timeout and section messages; tests AC6, AC10.
5. StaleBanner and OnHoldBanner; tests AC4, AC9.
6. Performance test with 50 documents and 120 interactions; test AC1.
7. Access test.

**Feature flag.** `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only.

**Done when.** The tests in section 16 pass and the view meets NFR-009 in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A section's data product is from an earlier date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | Case on hold | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-024 | A section has nothing to show | Nothing is recorded in {section} yet. |
| MSG-P3-023 | A section cannot be shown | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |

## 15. Screens and states

SCR-03 Case record. Loading: skeleton rows per section. Read only: fields without edit controls; the header and five sections with their business dates. On hold: the banner with the deviation or legal hold and the prescription date. Stale input: MSG-P1-001 above the section. Error: MSG-P3-023 in the section that failed.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-01 | AC1, BR7 | System | Case with 50 documents and 120 interactions |
| TC-E1-023-02 | AC2, BR1 | System | Account A-7001 at 97 days past due |
| TC-E1-023-03 | AC3, BR8 | System | Customer profile from the 2026-12-02 load |
| TC-E1-023-04 | AC4, BR2 | System | Load for 2026-12-03 refused |
| TC-E1-023-05 | AC5, BR5 | System | Case of team LIT-BKK, user with scope Own |
| TC-E1-023-06 | AC6 | System | Document hub not answering |
| TC-E1-023-07 | AC7, BR4 | System | Access log unavailable |
| TC-E1-023-08 | AC8, BR3, BR4 | System | Phone collector without unmask right |
| TC-E1-023-09 | AC9 | System | Case on hold for X1 |
| TC-E1-023-10 | AC10 | System | Case with no documents and no history |
| TC-E1-023-11 | Access | Access | RW-REFADM calls GET /cases/{caseId} and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: masking rules, labels and timeouts are data.
- No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only.
- No read of another module's tables: account and party data through RecoveryDataQuery (P1), documents through the P5 endpoint.
- Personal fields are never shown unmasked when the access log write fails.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | Case record view with account, arrears, owner, queue, stage, status, contact history and documents | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-01, TC-E1-023-02, TC-E1-023-03, TC-E1-023-06, TC-E1-023-09, TC-E1-023-10 |
| REQ-RDF-009 | Every data product carries a freshness stamp | Epic 1, 3.1; Program, 5.1 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-02, TC-E1-023-04 |
| REQ-ACA-005 | Personal data masked by role | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-07, TC-E1-023-08 |
| REQ-ACA-006 | Every read of the case store written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-05, TC-E1-023-08 |

## 19. Out of scope

- The history timeline on the case view (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF loads).

