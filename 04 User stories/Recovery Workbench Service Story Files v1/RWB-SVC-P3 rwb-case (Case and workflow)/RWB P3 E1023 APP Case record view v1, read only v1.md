# RWB-P3-E1023-APP Case record view v1, read only

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1018-APP |
| Depends on (build) | RWB-P3-E1023-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1018-APP |
| Contract dependencies | RWB-P4-E1037-CON, RWB-P4-E1039-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-019, FR-P3-020, FR-P3-021) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-023 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read live through the owner of each fact with the business date of each**, so that **I stop searching files and systems to understand a case**.

The screen is SCR-03, delivered as a gateway-bff composite route (DP-19, H RWB-PLT-N001-CON). gateway-bff calls rwb-case `GET /cases/{caseId}` and, in parallel, rwb-source-data for the customer and account parts, then merges the answers into the screen model. rwb-case serves the case block, the account and party links, the timeline and the timers from its own schema `rwb_case`; it reads no other service's tables and no ACE view (DP-01). The customer, account, contact and collections history facts arrive through the rwb-source-data contract (DP-05), and the interaction ledger belongs to rwb-source-data (DP-18). Masking is applied by the rwb-access policy (DP-08, C RWB-P4-E1037-CON), with the personal-field read shaped by C RWB-P4-E1039-CON.

### 2. Business rationale

A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. Under D-RCV-35 the Workbench holds no copy of the account, the customer or the contact point: the screen reads the ACE views by `account_key` and `person_key` through rwb-source-data, which is the only reader of `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action`. The identity number is already masked inside `v_ace_customer` (`id_no_masked` and `id_no_last4`) and the contact values are masked by role through the rwb-access masking policy, so no clear personal value is copied into a Workbench table or a screen cache.

This story puts the case, its accounts and arrears, its parties and contacts, its contact history and its documents on SCR-03, each section showing the ACE business date behind it, and writes every view of personal data to the access log through the rwb-access access-log contract. It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006 and REQ-ACA-009. The read is the first screen of the service, so it also fixes the read shape the whole service reuses: one hop per owner, a 2 s budget, a composite route at the edge and no chained call.

### 3. Preconditions

- RWB-P3-E1018-APP is done: cases exist in schema `rwb_case` with `account_key` links on case_account and `person_key` links on case_party.
- RWB-P3-E1023-CON is done: the OpenAPI 3.1 document and the fakes for the read-only case record operations, through which this story builds.
- RWB-PLT-N001-CON is done: the gateway-bff composite route that serves SCR-03. The exact route specification (path, merge rules, timeout ownership) is Not specified in the source documents (GAP-0693; ASM-1240).
- RWB-PLT-E1037-CON and C RWB-P4-E1037-CON are done: the authorise, masking-policy and access-log contracts of rwb-access are published with their fakes (DP-08).
- C RWB-P4-E1039-CON is published: the customer and account read contract that also carries the masking contract for personal fields. The exact shape of the field masking contract is Not specified in the source documents (GAP-0694; ASM-1241).
- The published rwb-source-data contract serves `GET /customers/{id}`, `GET /accounts/{id}`, `GET /freshness` and the interaction read, with its fake. The timeline page size and the interaction read operation are Not specified in the source documents (GAP-0695; ASM-1242).
- RWB-P3-E1018-APP cases carry the case header fields this view shows: case number, product group, status, stage, route, owner, queue, entry date and prescription date.
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON (parameters), RWB-PLT-E1043-CON and RWB-P3-E1043-CON (reference data), RWB-PLT-E1047-CON (event and topic naming), RWB-PLT-E1044-CON (Flyway sequence) and RWB-PLT-E1027-CON (decision record) are done.
- The rwb-case login (DP-02) holds SELECT on schema `rwb_case` and no privilege on any other schema. The login name is Not specified in the source documents (GAP-0692; ASM-1239).
- The user holds a role with Case record R in rwb-access and the case is in the user's scope.
- Personal data access is recorded through the rwb-access access-log contract, which also sends the PII access record to PII Kafka through the ACE common module.
- `v_ace_batch_status` is a Section B view, so the freshness line reaches the screen through rwb-source-data and the stale banner stays behind its flag until RWB-ACE-001 lands (DL43).

### 4. Flow

1. Case owner: opens a case from SCR-02 Case list; the gateway-bff composite route shows SCR-03 in the Loading state.
2. gateway-bff: checks the session in Redis, takes the short-lived JWT through ACE Common sign-in and checks the coarse permission.
3. gateway-bff: calls rwb-case `GET /api/recovery/case/v1/cases/{caseId}` and, in parallel, rwb-source-data `GET /customers/{id}` and `GET /accounts/{id}`; the document panel is one further hop to rwb-document `GET /cases/{id}/documents`.
4. rwb-case CaseRecordController: checks Case record R and the scope through the cached rwb-access `POST /authorise`; out of scope returns 404.
5. rwb-case CaseRecordQueryService: reads the header from recovery_case and the links from case_account and case_party, plus queue, timers and the reference labels, all inside schema `rwb_case` (DP-01).
6. rwb-case SourceDataClient: calls the rwb-source-data contract for the account facts by `account_key`, the customer and contact facts by `person_key` and the collections history from `v_ace_efs_action`; every row carries the ACE business date from `data_as_of` and the freshness contract.
7. rwb-case TimelineComposer: merges the rwb-case state changes and the Workbench entries read from the rwb-source-data interaction read (DP-18) into one contact history ordered by time, each row carrying its source system.
8. rwb-case MaskingApplier: asks rwb-access `GET /masking-policies` for the caller's role, fills each personal field from the masked or the clear column through the guard library, and publishes one AC-READ access record with the field IDs read and their masked flags. A read whose record cannot be written returns nothing.
9. rwb-document (P5): returns the document list for the case through its endpoint.
10. gateway-bff: merges the three answers into the screen model and returns it.
11. CaseRecordPage: shows the header (case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags), then Accounts, Parties with their contact points, Contact history and Documents, each with its ACE business date (read only state).
12. CaseRecordPage: shows the stale banner with MSG-P1-001 on any section whose ACE batch is not COMPLETE for the latest business date, and no Workbench load or job status anywhere.
13. CaseRecordPage: shows the on hold banner with MSG-P3-004 when the case is on hold.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch behind a section is not COMPLETE for the latest business date | Section shows with its business date and the stale banner | MSG-P1-001 | AC4 |
| X2 | The case is outside the user's scope | 404; nothing shows | MSG-P4-003 | AC5 |
| X3 | The document hub does not answer | Documents section shows the section message; the rest shows | MSG-P3-023 | AC6 |
| X4 | The access record cannot be written | The read is refused; no case data and no personal field shows | MSG-P7-003 | AC7 |
| X5 | The role may not see a personal field in clear | The field shows from the masked column of the view, through the masking policy | None | AC8 |
| X6 | The case is on hold | On hold banner with the prescription date | MSG-P3-004 | AC9 |
| X7 | The case has no documents and no contact history | Each section shows its empty sentence | MSG-P3-024 | AC10 |
| X8 | A role without Case record R opens the view | Refused with 403 | MSG-P4-002 | Access test TC-E1-023-11 |
| X9 | A case link holds an `account_key` that the account contract does not return | The Accounts row shows the key with empty values; REC-05 lists it; the rest shows | None | AC12 |
| X10 | rwb-source-data does not answer within the 2 s budget | The Accounts and Parties sections show MSG-P3-023; the header, timeline and documents show | MSG-P3-023 | AC6 pattern, new in D-RCV-60 |
| X11 | The gateway-bff composite route merge fails | The screen shows the section message for the part that failed; no partial case data with a missing scope check is shown | MSG-P3-023 | AC6 pattern, new in D-RCV-60 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads data other stories write; no write in this story other than the access record |
| Negotiable | Section order and the masking rules are data and design choices |
| Valuable | One screen answers the case owner's first questions, from the same ACE rows every other module reads |
| Estimable | One page, five read operations, one query service, three contract clients, one composite route |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Case record view v1, read only

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest ACE batch business date is 2026-12-02 and v_ace_batch_status shows the ALS, SCBPDM and EFS batches COMPLETED for it

  Scenario: AC1 Loads fast (legacy RWB-E1-023 AC1)
    Given case RW-2026-000701 has 50 documents and 120 contact history entries
    When U-81 opens the case record view
    Then the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings

  Scenario: AC2 Data from ACE (legacy RWB-E1-023 AC2)
    Given v_ace_account holds days_past_due 97, total_balance THB 206,175.00 and data_as_of 2026-12-02 for account A-7001
    Given the rwb-source-data contract mock returns days_past_due 97, total_balance THB 206,175.00 and data_as_of 2026-12-02 for account A-7001
    When the view opens
    Then the Accounts section shows 97 days past due and THB 206,175.00 for A-7001
    Then the section shows business date 2026-12-02 read from v_ace_account.data_as_of
    Then the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30

  Scenario: AC3 Customer and contacts from ACE (legacy RWB-E1-023 AC3)
    Given v_ace_customer holds person_key P-7001 with first_name "Anan", last_name "Sukjai", category "RETAIL" and id_no_masked "XXXXXXXXX4821"
    Given v_ace_contact holds a mobile for P-7001 with contact_key "PHONE:88421" and contact_value "0812345678"
    Given the rwb-source-data contract mock returns person_key P-7001 with category "RETAIL", id_no_masked "XXXXXXXXX4821" and the mobile for P-7001 with contact_key "PHONE:88421"
    When the view opens
    Then the Parties section shows the borrower with role "BORROWER", category "RETAIL" and business date 2026-12-02
    Then the borrower's contact points show from v_ace_contact with their contact_type and usage_code
    Then the contact history shows the v_ace_efs_action entries with action code, time and promise status

  Scenario: AC5 Case outside the scope (legacy RWB-E1-023 AC5)
    Given case RW-2026-000702 belongs to team "LIT-BKK" and U-81 has scope Own
    Given the rwb-access contract mock returns scope Own for U-81
    When U-81 opens case RW-2026-000702
    Then the response is 404 with MSG-P4-003
    Then no case data shows

  Scenario: AC6 Document hub unavailable (legacy RWB-E1-023 AC6)
    Given the document hub does not answer within 3 seconds
    When U-81 opens the view
    Then the Documents section shows MSG-P3-023 for "Documents"
    Then the header, accounts, parties and contact history show

  Scenario: AC7 The access event cannot be written (legacy RWB-E1-023 AC7)
    Given the access event stream rejects every write
    Given the rwb-access contract mock rejects every AC-READ access record write
    When U-81 opens the view
    Then the call returns status 503 with MSG-P7-003 and no case data
    Then no personal field shows

  Scenario: AC8 Masking by role (legacy RWB-E1-023 AC8)
    Given phone collector U-82 holds no masking rule that lets RW-PHONECOL see DF-ACE-078 in clear
    Given the case is in U-82's scope
    Given the rwb-access contract mock returns the masking policy for RW-PHONECOL with DF-ACE-078 masked and DF-ACE-079 clear
    When U-82 opens the view
    Then the identity shows "XXXXXXXXX4821" from v_ace_customer.id_no_masked
    Then the phone shows "XXXXXX5678" from v_ace_contact.contact_value_masked
    Then the access log holds the read with user U-82, the field IDs and the masked flags

  Scenario: AC9 Case on hold (legacy RWB-E1-023 AC9)
    Given case RW-2026-000701 has status "ON_HOLD" for deviation X1 with prescription date 2028-03-15
    When U-81 opens the view
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15

  Scenario: AC10 No documents and no contact history (legacy RWB-E1-023 AC10)
    Given case RW-2026-000703 has no documents and no contact history
    Given the rwb-source-data contract mock returns no interaction for case RW-2026-000703
    When its owner opens the view
    Then the Documents and Contact history sections each show MSG-P3-024
```

The Background, and every Given and Then line above, are copied unchanged from legacy RWB-E1-023. In the target the view facts reach rwb-case through the rwb-source-data contract, so `v_ace_account`, `v_ace_customer`, `v_ace_contact`, `v_ace_efs_action` and `v_ace_batch_status` are named as the system of record behind that contract, and rwb-case reads none of them directly (DP-01, DP-05). AC4, AC11 and AC12 of the legacy story are not owned here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every section shows the ACE business date behind it: rwb-case takes the case dates from schema `rwb_case` and the accounts, parties, contact history and freshness dates from the rwb-source-data contract; no Workbench load date is used | REQ-RDF-009; VR-P3-001-1; DP-05 |
| BR2 | A section whose ACE batch is not COMPLETE for the latest business date shows the stale banner | MSG-P1-001; screens.txt Common states "Stale input"; the rwb-source-data freshness operation |
| BR3 | A personal field shows from the masked column unless the masking rule in force lets the role see it in clear; the identity number is never in clear because the customer contract exposes `id_no_masked` and `id_no_last4` only | REQ-ACA-005; CTL-11; DL26; DF-ACE-073, DF-ACE-074; DP-08 |
| BR4 | Every read of personal data is written to the access log of rwb-access; a read whose record cannot be written returns no data | REQ-ACA-006; legacy RWB-E1-039 BR2; C RWB-P4-E1037-CON |
| BR5 | Only cases in the caller's scope open; others return 404 | CTL-09; REQ-ACA-009 |
| BR6 | The view has no edit control in Epic 1 | SCR-03 "E1 read only" |
| BR7 | The view loads in under 2 seconds with 50 documents | NFR-009 |
| BR8 | Account, customer, contact and collections history data are read live through the rwb-source-data contract by business key; the Workbench holds no copy and shows no Workbench load status | D-RCV-35 U1 and U4; ADR-010; DP-05 |
| BR9 | A case link with no view row shows the business key with empty values and is listed by REC-05; it is never deleted or rewritten | REC-05; Data Tier Map section 5 |
| BR10 | The contact history merges the ACE EFS entries and the Workbench interaction ledger in one time order, each row naming its source system; the ledger belongs to rwb-source-data | E1-068; interaction.source_system (DF-INT-013); DP-18 |
| BR11 | The read path carries no write operation: the OpenAPI document of RWB-P3-E1023-CON declares GET operations on the five read paths only | D-RCV-60; DP-19; ADR-020 |
| BR12 | rwb-case reads only schema `rwb_case`; another service's facts arrive through its published contract and never through a table read | D-RCV-60; DP-01; DP-11 |
| BR13 | The timeline page size and the interaction read operation come from the rwb-source-data contract; the value is Not specified in the source documents (GAP-0695; ASM-1242) | D-RCV-60; DP-18 |

### 9. State transitions

None. This story does not change a case status. It reads the case and shows its status, its stage, its timers and its hold flag. The events that move a case are published by other rwb-case stories on topic `rwb.case.events.v1`; this story consumes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Opens cases in scope Own (Case record R) |
| RW-TEAMMGR | Opens cases in scope Team |
| RW-PHONECOL | Opens cases in scope Own, read only, with masking |
| RW-CONDUCT, RW-AUDIT | Open every case (scope All) |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| The rwb-case login (DP-02) | Reads schema `rwb_case` only; SELECT on its own tables; no privilege on another schema. The login name is Not specified in the source documents (GAP-0692; ASM-1239) |
| rwb-access | Owns the roles, the scope, the masking policy and the access log; answers every authorise and masking call |
| rwb-source-data | Owns the ACE views, the freshness and the interaction ledger; answers every customer, account and interaction read |
| ACE team lead | Owns the ACE tables and columns behind the four views |

### 11. Data

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
| DF-ACE-001 | v_ace_account | account_key | Read through the rwb-source-data contract |
| DF-ACE-002 | v_ace_account | account_code | Read through the rwb-source-data contract |
| DF-ACE-018 | v_ace_account | days_past_due | Read through the rwb-source-data contract |
| DF-ACE-020 | v_ace_account | total_balance | Read through the rwb-source-data contract |
| DF-ACE-036 | v_ace_account | data_as_of | Read through the rwb-source-data contract |
| DF-ACE-055 | v_ace_customer | cif_no | Read through the rwb-source-data contract |
| DF-ACE-057 | v_ace_customer | first_name | Read, masked by role |
| DF-ACE-058 | v_ace_customer | last_name | Read, masked by role |
| DF-ACE-059 | v_ace_customer | date_of_birth | Read, masked by role |
| DF-ACE-068 | v_ace_customer | category | Read through the rwb-source-data contract |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read |
| DF-ACE-074 | v_ace_customer | id_no_last4 | Read, only with the personal-data permission |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read, only with the personal-data permission |
| DF-ACE-079 | v_ace_contact | contact_value_masked | Read |
| DF-ACE-080 | v_ace_contact | usage_code | Read |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read through the rwb-source-data contract |
| DF-ACE-111 | v_ace_efs_action | action_code | Read through the rwb-source-data contract |
| DF-ACE-112 | v_ace_efs_action | action_code_name | Read through the rwb-source-data contract |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read through the rwb-source-data contract |
| DF-ACE-116 | v_ace_efs_action | comments | Read, masked by role |
| DF-ACE-117 | v_ace_efs_action | is_call | Read through the rwb-source-data contract |
| DF-ACE-120 | v_ace_efs_action | promise_status | Read through the rwb-source-data contract |
| DF-ACE-178 | v_ace_batch_status | source_system | Read through the rwb-source-data freshness operation |
| DF-ACE-179 | v_ace_batch_status | business_date | Read through the rwb-source-data freshness operation |
| DF-ACE-182 | v_ace_batch_status | status | Read through the rwb-source-data freshness operation |
| DF-INT-004 | interaction | occurred_at | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-005 | interaction | channel | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-008 | interaction | contact_result | Read through the rwb-source-data interaction read (DP-18) |
| DF-INT-013 | interaction | source_system | Read through the rwb-source-data interaction read (DP-18) |
| DF-DOC-004 | document | document_type | Read through the rwb-document contract |
| DF-DOC-005 | document | source | Read through the rwb-document contract |
| DF-DOC-011 | document | doc_version | Read through the rwb-document contract |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-003 | queue | queue_name | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v7. DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v6, read only by rwb-source-data (DP-05). No field in this story is written. The only record written is the AC-READ access record, written by rwb-access on its own contract (DP-08).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Purpose | Owner | Read or write |
|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId} | Case header: case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags | rwb-case (P3) | Read |
| GET /api/recovery/case/v1/cases/{caseId}/accounts | The account links of the case with the balance and arrears facts from the rwb-source-data contract, each with its business date | rwb-case (P3) | Read |
| GET /api/recovery/case/v1/cases/{caseId}/parties | The parties of the case with role, category, masked identity and contact points | rwb-case (P3) | Read |
| GET /api/recovery/case/v1/cases/{caseId}/timeline | The case history as one timeline: rwb-case state changes plus the interaction read of rwb-source-data, ordered by time with the source system on each row | rwb-case (P3) | Read |
| GET /api/recovery/case/v1/cases/{caseId}/timers | The timers on the case: type, started, expires, warn, paused flag and status | rwb-case (P3) | Read |

The service provides the full operation set in Template and Rules §R4; this story builds and serves these five read operations only. The other operations are built by RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP and RWB-P3-E1042/E1043 stories.

#### 12.2 REST operations consumed

| Operation | Owner | Use in this story |
|---|---|---|
| GET /api/recovery/source-data/v1/customers/{id} | rwb-source-data (P1) | Customer and contact facts for Parties, masked by role |
| GET /api/recovery/source-data/v1/accounts/{id} | rwb-source-data (P1) | Balance, days past due and `data_as_of` for Accounts |
| GET /api/recovery/source-data/v1/freshness | rwb-source-data (P1) | The business date and batch state behind each section (MSG-P1-001) |
| The interaction read of the rwb-source-data contract | rwb-source-data (P1) | The ledger part of the timeline and the contact history (DP-18). Path and paging are Not specified in the source documents (GAP-0695; ASM-1242) |
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | Case record R and the scope check (DP-08) |
| GET /api/recovery/access/v1/masking-policies | rwb-access (P4) | The masking policy of the caller's role, by view field ID (C RWB-P4-E1039-CON) |
| The access-log write of the rwb-access contract | rwb-access (P4) | The AC-READ access record with field IDs and masked flags |
| GET /api/recovery/document/v1/cases/{id}/documents | rwb-document (P5) | The Documents section |

#### 12.3 Events published

None. This story publishes no case event. The AC-READ access record goes to the rwb-access access log through its contract (DP-08), not to topic `rwb.case.events.v1`.

#### 12.4 Events consumed

None. SCR-03 reads on open and subscribes to no topic in this story.

#### 12.5 Workflows and activities

None. The read is synchronous REST and starts, signals and queries no workflow. CaseWorkflow (parent, one per case, queue `rwb-case`) owns the case state this story reads; it is built and driven by the other rwb-case stories.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| recovery_case | rwb_case | P3 | Case header, stage, owner, queue, clocks, deviation and hold flags |
| case_account | rwb_case | P3 | The account links by `account_key` and `is_primary` |
| case_party | rwb_case | P3 | The party links by `person_key` and `party_role` |
| queue | rwb_case | P3 | `queue_code` and `queue_name` for the header |
| timer | rwb_case | P3 | The timers on the case |
| lov_value | rwb_case | P3 | Labels for status, stage, route, party role and contact type |
| reference_row | rwb_case | P3 | LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE, LOV-PARTY-ROLE |
| reference_version | rwb_case | P3 | The version in force on the read date |
| parameter_catalog | rwb_case | P3 | `caserecord.section.timeout.ms` |
| parameter_value | rwb_case | P3 | The value in force on the read date |

The service also owns case_entry_exclusion, queue_member, queue_measure, task and assignment; this story touches none of them. The interaction ledger, the account, customer, contact and collections views and the document estate are read through their owners' contracts, never through a table (DP-01, DP-05, DP-18).

#### 12.8 Contract fakes

| Fake | Operations | Owner | Used for |
|---|---|---|---|
| rwb-source-data fake | customers, accounts, freshness, interaction read | P1 | AC2, AC3, AC10 |
| rwb-access fake | authorise, masking policies, access-log write | P4 | AC5, AC7, AC8 |
| rwb-document fake | documents by case | P5 | AC6 |
| gateway-bff composite route stub | the SCR-03 route | edge (RWB-PLT-N001-CON) | AC1 |
| The masking and customer/account read fake of C RWB-P4-E1039-CON | the customer and account read with the masking contract | P4 | AC3, AC8 |

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | Yes. Five read operations provided under `/api/recovery/case/v1`; four contracts consumed, one hop each, 2 s timeout, GET retried once with jitter |
| Kafka | None. The service topic `rwb.case.events.v1` is not used by a read; the AC-READ access record goes through the rwb-access contract |
| Temporal | None. No workflow is started, signalled or queried |
| File | None |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case`, read module `caserecord`; the screen module is served by the gateway-bff composite route of RWB-PLT-N001-CON and holds no server code of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseRecordController | Controller | The five read operations with the access check and the scope, mapping errors to the problem response |
| CaseRecordQueryService | Service | Composes the case header, the account links, the party links and the timers, and adds the ACE business date per section |
| CaseRecordRepository | Repository | Reads recovery_case, case_account, case_party, queue, timer and the reference and parameter tables inside `rwb_case`; no other schema |
| SourceDataClient | Client | Calls the rwb-source-data contract for accounts, customers, contacts, collections history, the interaction read and the freshness; 2 s timeout, one retry on GET |
| AccessClient | Client | Calls the rwb-access authorise, masking-policy and access-log operations; refuses the read when the access record cannot be written |
| DocumentClient | Client | Calls the rwb-document documents-by-case operation; a failure degrades one section |
| TimelineComposer | Service | Merges the rwb-case state changes and the ledger rows into one time order, each row naming its source system |
| MaskingApplier | Service | Fills each personal field from the masked or the clear column through the guard library and records the field IDs and masked flags |
| CaseRecordPage | Screen component | SCR-03 read-only layout with the Loading, read-only, on-hold, stale and error states |
| CaseHeader, AccountsPanel, PartiesPanel, ContactHistoryPanel, DocumentsPanel | Screen component | One section each, each with an AceDataDateBadge |
| StaleBanner, OnHoldBanner, SectionMessage | Screen component | MSG-P1-001, MSG-P3-004, MSG-P3-023 and MSG-P3-024 |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Database**

- Reads recovery_case, case_account, case_party, queue, timer, lov_value, reference_row, reference_version, parameter_catalog and parameter_value in schema `rwb_case` only, through the rwb-case login (DP-02). The login name is Not specified in the source documents (GAP-0692; ASM-1239).
- No migration. The tables and the Flyway sequence come from RWB-P3-E1018-CON and RWB-PLT-E1044-CON.
- The timeline uses the index on the ledger owned by rwb-source-data through its interaction read; rwb-case creates no index on another schema.

**Configuration and reference data**

- Masking rules over the view field IDs, held by rwb-access (DL26); labels (DL10), LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE, LOV-PARTY-ROLE through the reference-data contract.
- Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11) from the parameters contract, not from code.

**Build steps**

1. CaseRecordRepository and the five read operations against schema `rwb_case`; test the header composition for AC2.
2. SourceDataClient against the rwb-source-data fake for accounts, customers, contacts and collections history; tests AC2, AC3, AC12 pattern.
3. TimelineComposer over the rwb-case state changes and the interaction read; tests AC3, AC10.
4. AccessClient with the authorise, masking-policy and access-log calls and the refusal path; tests AC5, AC7, AC8.
5. DocumentClient with the per-section degradation; test AC6.
6. CaseRecordPage and the composite route against the gateway-bff stub, with the per-section timeout and the section messages; tests AC6, AC10.
7. StaleBanner and OnHoldBanner over the freshness contract and the case hold flag; tests AC9 and the AC4 pattern.
8. No-copy and performance tests with 50 documents and 120 EFS entries; tests AC1.
9. Access test through the rwb-access contract.

**Feature flag.** `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only. The stale banner reads the freshness of a Section B view behind rwb-source-data, so it is on only after RWB-ACE-001 lands and the freshness contract exposes it (DL43).

**Done when.** The tests in section 16 pass and the view meets NFR-009 in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A section's ACE batch is not complete for the latest business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P3-004 | Case on hold | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-024 | A section has nothing to show | Nothing is recorded in {section} yet. |
| MSG-P3-023 | A section cannot be shown | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Every error is returned as the service's problem response (TSD P3 v3 T2.1) carrying the MSG code and the trace ID; the response schema and the status codes 401, 403, 404 and 503 are fixed by the contract in RWB-P3-E1023-CON. Validation: the path identifier must be a case identifier; an unknown or out-of-scope case is 404 and never 403, so the view leaks nothing about the case.

### 15. Screens and states

SCR-03 Case record, served as the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). The exact route specification is Not specified in the source documents (GAP-0693; ASM-1240). States: Loading, skeleton rows per section. Read only: fields without edit controls; the header and five sections, each with the ACE business date of its source. On hold: the banner with the deviation or legal hold and the prescription date. Stale input: MSG-P1-001 above the section when the ACE batch behind it is not complete. Error: MSG-P3-023 in the section that failed, MSG-P4-003 when the case is out of scope and MSG-P7-003 when the access record cannot be written. The screen shows no Workbench load, job or file status.

Sections and their owner: the header, the timers and the case timeline rows come from rwb-case; the account, customer, contact and collections history facts come from rwb-source-data; the document list comes from rwb-document; the masking and the scope come from rwb-access.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-01 | AC1, BR7 | End to end | Case with 50 documents and 120 EFS entries |
| TC-E1-023-02 | AC2, BR1 | End to end | `v_ace_account` A-7001 at 97 days past due, data_as_of 2026-12-02 |
| TC-E1-023-03 | AC3, BR8 | End to end | `v_ace_customer` P-7001 with category RETAIL, `v_ace_contact` mobile, EFS entries |
| TC-E1-023-04 | AC4, BR2 | End to end | No COMPLETED ALS row for 2026-12-03, data_as_of 2026-12-02 |
| TC-E1-023-05 | AC5, BR5 | End to end | Case of team LIT-BKK, user with scope Own |
| TC-E1-023-06 | AC6 | End to end | Document hub not answering |
| TC-E1-023-07 | AC7, BR4 | End to end | Access event stream rejecting every write |
| TC-E1-023-08 | AC8, BR3 | End to end | Phone collector without the personal-data permission |
| TC-E1-023-09 | AC9 | End to end | Case on hold for X1 |
| TC-E1-023-10 | AC10 | End to end | Case with no documents and no history |
| TC-E1-023-11 | Access | Component | RW-REFADM calls GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-023-12 | AC11, BR8 | End to end | A-7001 balance changed by the 2026-12-03 ALS batch |
| TC-E1-023-13 | AC12, BR9 | End to end | Case link A-7010 with no view row |

The legacy TC IDs, the legacy Covers and the legacy Data are kept unchanged. The legacy Level System maps to End to end and Access maps to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: masking rules, labels and timeouts are data, read through the parameters and reference-data contracts.
- No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only. No PII in events, workflow inputs or logs.
- ACE data only through its owner: account, customer, contact and collections history come through the rwb-source-data contract, freshness included. rwb-case holds no foreign key into a `public` table and reads no `recovery.v_ace_*` view (DP-01, DP-05).
- The interaction ledger is read through its owner's contract, never by a table read (DP-18).
- No service reads another service's tables and no call chains: gateway-bff asks each owner in parallel, one hop, 2 s timeout.
- The view holds no copy of a source record and caches no clear personal value; the identity number is masked inside the view and the contact values are masked by role through rwb-access.
- Personal fields are never shown when the access record cannot be written.
- The read path exposes no write operation.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | Case record view with account, arrears, owner, queue, stage, status, contact history and documents | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-01, TC-E1-023-02, TC-E1-023-03, TC-E1-023-06, TC-E1-023-09, TC-E1-023-10 |
| REQ-RDF-009 | Every data product carries a freshness stamp | Epic 1, 3.1; Program, 5.1 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-02, TC-E1-023-04 |
| REQ-ACA-005 | Personal data masked by role | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-07, TC-E1-023-08 |
| REQ-ACA-006 | Every read of the case store written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | None | TC-E1-023-05, TC-E1-023-08 |
| REQ-ACA-009 | Only cases in the caller's scope are visible | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | 06 Take over and own the case | CTL-09 | TC-E1-023-05, TC-E1-023-11 |
| D-RCV-35 U1 and U4 | The view reads account, customer, contact and collections history only by business key through their owner, and copies nothing | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-ACA-11 | 06 Take over and own the case | ADR-010; CTL-02; DP-05 | TC-E1-023-12, TC-E1-023-13 |

| Trace | Reference |
|---|---|
| Legacy key | RWB-E1-023, disposition Split (rework) |
| Contract story | RWB-P3-E1023-CON (OpenAPI 3.1, fakes, tables) |
| Build dependency | RWB-P3-E1018-APP (cases and links exist) |
| Contract dependencies | RWB-P4-E1037-CON (authorise, masking policy, access log), RWB-P4-E1039-CON (customer and account read with the masking contract) |
| Edge dependency | RWB-PLT-N001-CON (gateway-bff composite route, DP-19) |
| Pattern rows | DP-01, DP-02, DP-03, DP-05, DP-06, DP-07, DP-08, DP-11, DP-13, DP-14, DP-15, DP-18, DP-19 |

### 19. Out of scope

- The history timeline screen SCR-04 with its own filters (RWB-E1-035); this story composes the timeline data behind SCR-03 only.
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Writing a Workbench entry to the interaction ledger (RWB-E1-066, RWB-E1-067); the ledger is written by rwb-source-data.
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF ingestion lands in ACE).
- The write operations of rwb-case (transfer, legal hold, task update, placements, reference loads), which belong to their own stories.
