# RWB-S8-E1023-APP Case record view v1, read only

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E1023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 1 |
| Business epic | EP01 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S8-E1023-APP-14) |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S8-E1023-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | L-S8-C |
| Ready to start | Day 1 |
| Depends on (build) | Build prerequisites as fakes: RWB-PLT-E1027-CON, RWB-PLT-E1042, RWB-PLT-E1043, RWB-PLT-E1037, RWB-PLT-E1047, RWB-PLT-E1044 and N001 |
| Contract dependencies | RWB-P3-E1023-CON, version Not specified in the source documents (DOR-RWB-S8-E1023-APP-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S8-E1023-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006, REQ-ACA-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the read-only case record view of RWB-E1-023 is realigned onto rwb-deviation (S8, service wave 2, business wave 1), as the secondary serving of the page the split plan places in this service. The page is composed from the published contracts of its owners instead of the `recovery.v_ace_*` views: the case header, its links, its queue and its parameters come from rwb-case on RWB-P3-E1023-CON (DP-11), the account, party, contact and contact-history facts from rwb-source-data (DP-05, DP-18), the documents from rwb-document, and the masking rules, the scope and the AC-READ access record from rwb-access (DP-08). The AC-READ record is written locally through the decision-record library before any personal field is returned (DP-03), the five legacy read paths move onto `/api/recovery/deviation/v1` (DP-13), the page is reached through the gateway-bff composite route (DP-19), and the schema, login, topic and migration rules of the service apply (DP-01, DP-02, DP-14, DP-15). No source publishes the five consumed operation names, the plan gives the slice no build row although seven platform stories are prerequisites, the plan assigns it no legacy criterion while it keeps thirteen legacy test cases, and the legacy module is P3 although the slice sits in S8 (GAP-3081 to GAP-3084; ASM-5242 to ASM-5251). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S8-E1023-APP-L271, X20 RWB-S8-E1023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history, deviation flag and documents, each read live from its owner with the business date of the answer**, so that **I stop searching files and systems to understand a case**.

This story owns:

- the read-only assembly of SCR-03 on `/api/recovery/deviation/v1`: the five legacy read paths re-based by DP-13, one section each, parallel, each on its own 3 s budget;
- the **deviation block** of the page: the codes open on the case, `deviation_open`, the contact-stop flag, the raise instant, the handler and the return point, read from `deviation` in `rwb_deviation` (REQ-DVH-006; FSD S8 A1.2);
- the **on hold banner** of the page: MSG-P3-004 with the code and the prescription date, from the case status and the open deviation;
- the **stale banner** per section: MSG-P1-001 with the product and the business date the answer carries;
- the **AC-READ access record** written through the local decision-record library before any personal field is returned, with the field IDs and their masked flags;
- the masking by role, the scope filter and the refusals of the page as consumed from rwb-access.

It does not own: the published shapes, the error set and the fakes (RWB-P3-E1023-CON); the case of record, its status, stage, queue, owner, entry and prescription dates and its links (`recovery_case`, `case_account`, `case_party`, `queue` - rwb-case, P3); the account, party, contact and contact-history facts of ACE (rwb-source-data, P1); the documents (rwb-document, P5); the rights, the masking rules and the access log (rwb-access, P4); the timers (rwb-case); and the schema, migration, deployment and observability of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. The Workbench holds no copy of the account, the customer or the contact point: every section is read live by business key and shows the business date of the answer, so the page can never show a value older than the batch behind it (REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006, REQ-ACA-009).

D-RCV-60 changes who answers, not what the owner sees:

- **The sections are the owners' answers**, one hop each and with a fake on Day 1: no service reads another service's tables and none reads `v_ace_*` on another's behalf (DP-01, DP-05, DP-11).
- **The deviation block is this service's**, and it is why the slice sits in S8: REQ-DVH-006 requires the flag on the case record view, `deviation` is S8's one table, and a flag copied from a case column would be another service's fact.
- **Personal data is masked and logged once**, by rwb-access, on an identity already masked inside the P1 answer, so no clear value is copied into `rwb_deviation` or a screen cache (DP-08).
- **The read carries its own proof**: the AC-READ record is written in the read's transaction through the library of DP-03 before the first personal field leaves the service, and a failed write refuses the read (AC7).
- **The page is one route**: SCR-03 reaches this service through the gateway-bff composite route, which answers only its five reads on its own base (DP-13, DP-19).

No business value moves: labels, section timeouts, masking rules and lists of values stay reference data or parameters read with their version, never a constant.

### 3. Preconditions

- RWB-P3-E1023-CON is published and tagged: the case header, its account and party links, its queue, its parameter set and its list of values are baselined, with their fakes, and handed to this story (DP-11).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the read (DP-03; not in the empty build row, ASM-5244).
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-E1037-CON are published: the parameter, reference-data and authorise clients this page consumes (DP-06, DP-07, DP-08; ASM-5244).
- RWB-PLT-E1044-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON are published: the per-service Flyway sequence, the naming library and the gateway-bff composite route (DP-15, DP-14, DP-19).
- `deviation` exists in `rwb_deviation` from the DB story of this service with its columns and the standard record columns of TSD S8 T3.0; this story reads it and adds no table, no column and no migration.
- The rwb-source-data data-product contract answers accounts, parties with contacts and the merged contact history with a business date per answer and a freshness answer for the latest business date; its operation names are not published (GAP-3081; ASM-5246, ASM-5247).
- The rwb-document contract answers the document list of a case; its operation name is not published (GAP-3081; ASM-5247).
- The rwb-access contract answers the capability right, the scope and the masking rule of the caller, and accepts the AC-READ record (ASM-5249).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-02, DP-05).
- No approval is needed to build against a Draft contract baseline; the status of the source documents is taken as an assumption and the story stays in Draft (ASM-5242).

### 4. Flow

1. The case owner opens a case from SCR-02 Case list; the gateway-bff composite route resolves SCR-03 and shows the Loading state (DP-19).
2. `CaseRecordPage` calls the five reads of `/api/recovery/deviation/v1` in parallel: `GET /cases/{caseId}`, `/accounts`, `/parties`, `/contact-history` and `/documents` (DP-13).
3. `CaseRecordViewGuard` checks the Case record right and the scope with rwb-access on its consumed authorise operation (Not specified in the source documents (GAP-3081)), the authorise attributes and the policy version: Not specified in the source documents (GAP-0989); a case out of scope answers 404 and nothing else is called (DP-08).
4. `CaseSectionReader` reads the case header, its owner, queue, stage, status, entry date and prescription date from rwb-case on its contract (case-record read: Not specified in the source documents (GAP-3081)), plus the two hold flags (DP-11).
5. `DeviationBlockReader` reads the open `deviation` rows of the case from `rwb_deviation`: code, raised-at, raised-by, handler, contact stop, paused state and state; no other service writes them.
6. `CaseSectionReader` reads the accounts, the parties with their contact points and the contact history from rwb-source-data on its contract (account, party, contact and contact-history reads: Not specified in the source documents (GAP-3081)); each answer carries its `dataAsOf` and its freshness answer (DP-05, DP-18).
7. `CaseSectionReader` reads the document list from rwb-document on its contract (document-list read: Not specified in the source documents (GAP-3081)), 3 s budget, one hop (DP-11).
8. `MaskingApplier` takes the masking rule and the scope of the caller from rwb-access, fills every personal field from the masked or the clear column the answer offers (masking version and field-ID roster: Not specified in the source documents (GAP-0989)), and writes one AC-READ record through the local library with the field IDs and their masked flags before the answer leaves the service (DP-03, DP-08).
9. `CaseRecordViewService` assembles the page: header, deviation block, accounts, parties with contacts, contact history and documents, each with the ACE business date of its answer.
10. `StaleSectionBanner` shows MSG-P1-001 on any section whose answer is not fresh for the latest business date; `OnHoldBanner` shows MSG-P3-004 when the case is on hold, with the deviation code and the prescription date.
11. An empty section shows MSG-P3-024, a section that fails shows MSG-P3-023 and the rest of the page shows, and no Workbench load, job or file status appears anywhere.
12. Nothing is written except the AC-READ record: the page has no edit control, moves no case status and starts no workflow.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer behind a section is not fresh for the latest business date | The section shows with its own business date and the stale banner above it | MSG-P1-001 | AC4 |
| X2 | The case is outside the caller's scope | 404; nothing shows and no section is read | MSG-P4-003 | AC5, TC-E1-023-05 |
| X3 | The rwb-document read does not answer inside 3 s or its breaker is open | The Documents section shows the section message; the rest shows | MSG-P3-023 | AC6 |
| X4 | The AC-READ record cannot be written | The read is refused with 503; no case data and no personal field leaves the service | MSG-P7-003 | AC7 |
| X5 | The role has no masking rule that lets it see a personal field in clear | The field shows from the masked column of the answer | None | AC8 |
| X6 | The case is on hold for a deviation or a legal hold | The on hold banner shows the code and the prescription date | MSG-P3-004 | AC9 |
| X7 | The case has no document and no contact-history entry | Each section shows its empty sentence | MSG-P3-024 | AC10 |
| X8 | The role lacks the Case record right | 403 before any section is read | MSG-P4-002 | AC13, TC-E1-023-11 |
| X9 | A case link holds an `account_key` that the P1 answer does not return | The Accounts row shows the key with empty values, the rest shows, and REC-05 lists it | None | AC12 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC14, TC-E1-023-14, Section 17, BR1, BR5 |

X1 to X9 are the paths of RWB-E1-023; X10 is the DP-01 and DP-05 boundary of the target.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P3-E1023-CON and six fakes (case, source data, documents, access, parameters and lists, decision record), on its own schema, and needs no live P1, P3, P4 or P5 |
| Negotiable | The section components, the assembly order and the shape of the page are this story's choice; the five paths, the messages, the masks and the fields are fixed |
| Valuable | One screen answers the case owner's first questions and shows the deviation flag, the contact stop and the prescription date without reading a second system |
| Estimable | Five read handlers, one guard, one assembler, one masking applier, one access record, six section components and the failure tests |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every criterion runs on synthetic cases through the contract fakes, plus the access refusal, the forced record failure and the boundary test |

### 7. Acceptance criteria

The split plan assigns this slice no legacy criterion (GAP-3083; ASM-5248), so the nineteen criteria are new under D-RCV-60 and keep the legacy scenario values of RWB-E1-023 word for word, with the owner's contract mock standing in for each read the legacy story took from `v_ace_*` or from a Workbench table.

```gherkin
Feature: Case record view v1, read only

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest ACE batch business date is 2026-12-02
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Loads fast (new, D-RCV-60)
    Given the rwb-case contract mock returns case RW-2026-000701 and the rwb-document contract mock returns 50 documents for it
    Given the rwb-source-data contract mock returns 120 contact history entries for RW-2026-000701
    When U-81 opens the case record view
    Then the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings

  Scenario: AC2 Data from the owners (new, D-RCV-60)
    Given the rwb-source-data contract mock returns account A-7001 with daysPastDue 97, totalBalance 206175.00 and dataAsOf 2026-12-02
    Given the rwb-case contract mock returns queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30 for RW-2026-000701
    When the view opens
    Then the Accounts section shows 97 days past due and THB 206,175.00 for A-7001
    Then the section shows business date 2026-12-02 read from the dataAsOf of the answer
    Then the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30

  Scenario: AC3 Customer and contacts from the owner (new, D-RCV-60)
    Given the rwb-source-data contract mock returns person_key P-7001 with first_name "Anan", last_name "Sukjai", category "RETAIL" and id_no_masked "XXXXXXXXX4821"
    Given it returns a mobile for P-7001 with contact_key "PHONE:88421" and contact_value "0812345678"
    Given it returns the EFS entries of A-7001 with their action code, time and promise status
    When the view opens
    Then the Parties section shows the borrower with role "BORROWER", category "RETAIL" and business date 2026-12-02
    Then the borrower's contact points show with their contact_type and usage_code
    Then the contact history shows the EFS entries with their action code, time and promise status

  Scenario: AC4 Stale answer (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the account answer with dataAsOf 2026-12-02 and marks the ALS answer for 2026-12-03 as not COMPLETED
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows business date 2026-12-02
    Then the stale banner shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-02
    Then no Workbench load or job status shows

  Scenario: AC5 Case outside the scope (new, D-RCV-60)
    Given the rwb-case contract mock returns case RW-2026-000702 of team "LIT-BKK"
    Given the rwb-access contract mock returns scope Own for U-81
    When U-81 opens case RW-2026-000702
    Then the response is 404 with MSG-P4-003
    Then no case data shows

  Scenario: AC6 Document read unavailable (new, D-RCV-60)
    Given the rwb-document contract mock does not answer within 3 seconds
    When U-81 opens the view
    Then the Documents section shows MSG-P3-023 for "Documents"
    Then the header, accounts, parties and contact history show

  Scenario: AC7 The access record cannot be written (new, D-RCV-60)
    Given the local decision-record stub of RWB-PLT-E1027-CON rejects every AC-READ write
    When U-81 opens the view
    Then the call returns status 503 with MSG-P7-003 and no case data
    Then no personal field shows

  Scenario: AC8 Masking by role (new, D-RCV-60)
    Given phone collector U-82 holds no masking rule that lets RW-PHONECOL see DF-ACE-078 in clear
    Given the rwb-access contract mock returns scope Own for U-82 on case RW-2026-000701
    When U-82 opens the view
    Then the identity shows "XXXXXXXXX4821" from the id_no_masked of the answer
    Then the phone shows "XXXXXX5678" from the contact_value_masked of the answer
    Then the access record holds the read with user U-82, the field IDs and the masked flags

  Scenario: AC9 Case on hold (new, D-RCV-60)
    Given `rwb_deviation` holds an open deviation X1 on case RW-2026-000701
    Given the rwb-case contract mock returns status "ON_HOLD" and prescription date 2028-03-15
    When U-81 opens the view
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15

  Scenario: AC10 No documents and no contact history (new, D-RCV-60)
    Given the rwb-document contract mock returns no document and the rwb-source-data contract mock returns no contact-history entry for case RW-2026-000703
    When its owner opens the view
    Then the Documents and Contact history sections each show MSG-P3-024

  Scenario: AC11 No copy of the account on the case (new, D-RCV-60)
    Given the rwb-source-data contract mock returned THB 206,175.00 for A-7001 with dataAsOf 2026-12-02
    Given it now returns THB 210,000.00 for A-7001 with dataAsOf 2026-12-03
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows THB 210,000.00 and business date 2026-12-03
    Then no table of `rwb_deviation` holds the previous balance for the case

  Scenario: AC12 An account link with no answer row (new, D-RCV-60)
    Given the rwb-case contract mock returns case RW-2026-000701 with account_key A-7010 linked
    Given the rwb-source-data contract mock returns no account answer for A-7010
    When U-81 opens the view
    Then the Accounts section shows A-7010 with empty balance and days past due
    Then the rest of the case shows
    Then REC-05 lists account_key A-7010 for the data steward and the ACE team

  Scenario: AC13 Role without the Case record right (new, D-RCV-60)
    Given a caller with role RW-REFADM, which lacks the Case record right
    Given the rwb-access contract mock refuses the Case record right for that caller
    When the caller opens case RW-2026-000701
    Then the response is 403 with MSG-P4-002 before any section is read

  Scenario: AC14 Statement outside the own schema (new, D-RCV-60)
    Given a component or statement under test reads a `v_ace_*` view, a `rwb_case` row or another service's schema
    When the boundary test runs in the build
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC15 Read only page (new, D-RCV-60)
    Given the rwb-case contract mock returns case RW-2026-000701
    When U-81 opens the case record view
    Then the page shows no edit control
    Then no case status changes

  Scenario: AC16 Deviation block from its own table (new, D-RCV-60)
    Given `rwb_deviation` holds an open deviation X1 on case RW-2026-000701
    When U-81 opens the view
    Then the deviation block reads `deviation` in `rwb_deviation` only
    Then no flag is copied from another service's case column

  Scenario: AC17 No personal data at rest (new, D-RCV-60)
    Given U-81 opens the view with personal fields on the case
    When the view has answered
    Then no person name, contact value, address or identity number is in `rwb_deviation`, the AC-READ record, a log or a prompt

  Scenario: AC18 Error answers 401 of GET /cases/{caseId} (new, D-RCV-60)
    Given a request to GET /cases/{caseId} without a valid session
    When the request reaches the service
    Then the response is 401 and no section is read

  Scenario: AC19 Disallowed status change refused (new, D-RCV-60)
    Given the rwb-case contract mock returns a status change for RW-2026-000701 that the status model does not allow
    When U-81 opens the view
    Then the change is refused
    Then no case status changes
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every section shows the business date of its own answer, taken from the `dataAsOf` the owner's contract carries; no Workbench load date is used and no `v_ace_*` view is read here | REQ-RDF-009; DP-05; VR-S8-001-1; ASM-5246 |
| BR2 | A section whose answer is not fresh for the latest business date shows the stale banner with the product and that date | MSG-P1-001; legacy BR2 |
| BR3 | A personal field shows from the masked column of the answer unless the masking rule in force lets the role see it in clear; the identity number is never in clear because the P1 answer exposes `id_no_masked` and `id_no_last4` only | REQ-ACA-005; CTL-11; DL26; DP-08 |
| BR4 | Every read of personal data writes one AC-READ record before the answer leaves the service; a failed write refuses the read with 503 | REQ-ACA-006; DP-03; AC7 |
| BR5 | Only cases in the caller's scope open; others return 404 and read no section | CTL-09; REQ-ACA-009 |
| BR6 | The page has no edit control in Epic 1 and moves no case status | SCR-03 "E1 read only" |
| BR7 | The page shows with 50 documents and 120 contact-history entries in under 2 seconds at the 95th percentile | NFR-009 |
| BR8 | The account, party, contact and contact-history facts are read live from their owner by business key; `rwb_deviation` holds no copy and the page shows no Workbench load status | Legacy BR8; DP-01, DP-05, DP-18 |
| BR9 | A case link with no answer row shows the business key with empty values and is listed by REC-05; it is never deleted or rewritten | REC-05; Data Tier Map section 5 |
| BR10 | The contact history merges the ACE EFS entries and the interaction ledger in one time order, each entry naming its source system, both on the P1 answer; page size taken from a parameter, value Not specified in the source documents (GAP-0695) | E1-068; DF-INT-013; DP-18 |
| BR11 | The deviation block reads `deviation` in `rwb_deviation` and nothing else; a flag is never copied from another service's case column | REQ-DVH-006; DP-01; ASM-5243 |
| BR12 | No person name, contact value, address or identity number enters `rwb_deviation`, the AC-READ record, a log or a prompt | Template and Rules v1 §R7.2 s17 |

### 9. State transitions

None that this story makes: it changes no case status, no deviation state and no timer (BR6). It reads the case status and the deviation `state` and shows them, and the on hold banner is a rendering of state, not a transition.

| Read | Source | Shown as |
|---|---|---|
| Case status `ON_HOLD`, `IN_PROGRESS` or another value | rwb-case answer | Header status; `ON_HOLD` also opens the banner with the code and the prescription date |
| `deviation.state` of an open row, over the nine DEVIATION states of TSD S8 T4 | `rwb_deviation` | Deviation block, with the code, the handler, the return point and the contact stop |
| Freshness of a section | The stamp and the freshness answer of the owner's contract | No banner, or MSG-P1-001 with the product and the date |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Opens cases in scope Own (Case record R, TSD S8 T6.1) |
| RW-TEAMMGR | Opens cases in scope Team (R) |
| RW-PHONECOL | Opens cases in scope Own, read only, with masking (R) |
| RW-CONDUCT, RW-AUDIT | Open every case (scope All, R) |
| RW-REFADM, RW-SECADM | No Case record right on this page; refused |
| rwb-case (P3) | Owns the case header, the links, the queue, the parameters and the lists this page consumes |
| rwb-source-data (P1) | Owns the ACE account, party, contact and contact-history answers, with their business date and their ledger |
| rwb-access (P4) | Owns the rights, the masking rules, the scope and the AC-READ log this page calls |
| rwb-document (P5) | Owns the document list of the case |
| Solution architect | Confirms the placement of the page in S8 and the five consumed operation names (GAP-3081, GAP-3082) |

### 11. Data

| BR Field ID | Field or entity | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Read**, one row per open code: `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome`, `state` |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | **Write**, one AC-READ record per read, hash-linked, before the answer (DP-03) |
| DF-CAS-002, 003, 005, 006, 008, 009, 010, 013, 017, 019, 020 | `recovery_case` | P3 rwb-case | The header and the two hold flags; consumed on the contract, never written |
| DF-CAS-026, 027, 032, 033 | `case_account`, `case_party` | P3 rwb-case | The links this page expands; consumed, never written |
| DF-WRK-002, DF-WRK-003 | `queue` | P3 rwb-case | The queue code and name of the header; consumed, never written |
| DF-ACE-001, 002, 018, 020, 036 | `v_ace_account` | P1 rwb-source-data | account_key, account_code, days_past_due, total_balance, data_as_of; **not read here**, consumed on the P1 answer (DP-05) |
| DF-ACE-055, 057, 058, 059, 068, 073, 074 | `v_ace_customer` | P1 rwb-source-data | cif_no, names, date_of_birth, category, id_no_masked, id_no_last4; consumed, masked by role (DP-08) |
| DF-ACE-075 to DF-ACE-080 | `v_ace_contact` | P1 rwb-source-data | contact_type, contact_key, person_key, contact_value, contact_value_masked, usage_code; consumed, masked by role |
| DF-ACE-108, 111, 112, 114, 116, 117, 120 | `v_ace_efs_action` | P1 rwb-source-data | The EFS entries of the contact history; consumed |
| DF-ACE-178, 179, 182 | `v_ace_batch_status` | P1 rwb-source-data | The freshness behind each section; carried on the answer, never read here |
| DF-INT-004, 005, 008, 013 | `interaction` | P1 rwb-source-data (ledger owner, DP-18) | The Workbench entries of the contact history; consumed on the ledger part of the P1 answer |
| DF-DOC-004, 005, 011 | `document` | P5 rwb-document | document_type, source, doc_version; consumed |

The field IDs are those of the Logical Data Model and Data Dictionary v9 and the DF-ACE-* are the `recovery.v_ace_*` fields of Physical Schema v7, which is why they are named here and read by P1 only (DP-05). The one row this service writes is the AC-READ record and it holds identifiers, field IDs and masked flags, no value (BR12). The lists this page shows are reference data of rwb-case - LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE, LOV-PARTY-ROLE and LOV-DEVIATION - read at their version (DP-07; ASM-5250).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The five paths are the legacy paths of RWB-E1-023 section 12 with the base moved; every one is a read and none writes a table except the AC-READ record (DP-03).

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}` | Case header: case no, product, status, stage, route, owner, queue, entry date, prescription date, deviation and legal hold flags, each with the business date of its answer | Case record R, scope applied | Not applicable; a read |
| GET | `/cases/{caseId}/accounts` | CaseAccount[]: account key, account code, days past due, total balance, `dataAsOf` | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/parties` | CasePartyView[]: person key, party role, display name, customer no, identity masked or last four, category, contacts[] with type, key, value by role and `dataAsOf` | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/contact-history` | ContactHistoryPage: the EFS entries and the ledger entries, one time order, each with its `sourceSystem`; query from, to, page, size | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/documents` | DocumentPage: type, source, version, page and size; answered by P5 | Documents R, scope applied | Not applicable |

Every operation answers 400, 401, 403 with MSG-P4-002, 404 with MSG-P4-003, 422 and 503 with MSG-P7-003, each in the platform error envelope; the exact shapes and status list are RWB-P3-E1023-CON's. The Ownership Map gives S8 two write operations and no read, so these five reads are recorded as a conflict (GAP-3082; ASM-5243).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The case header, link, queue, parameter and list read of rwb-case; operation names Not specified in the source documents (GAP-3081; ASM-5247) | P3 rwb-case | The header fields, the two hold flags, the links, the queue, `caserecord.section.timeout.ms` and the six lists; baselined by RWB-P3-E1023-CON |
| The account, party and contact read of rwb-source-data; operation name Not specified in the source documents (GAP-3081; ASM-5246) | P1 rwb-source-data | The accounts, the parties with their contact points and the identity mask, each with its `dataAsOf` and its freshness answer |
| The contact-history read of rwb-source-data (ledger owner, DP-18); operation name Not specified in the source documents (GAP-3081; ASM-5246) | P1 rwb-source-data | The EFS entries and the ledger entries, one time order, each with its source system |
| The document list read of rwb-document; operation name Not specified in the source documents (GAP-3081; ASM-5247) | P5 rwb-document | The document list of the case with its type, source and version |
| The authorise and mask read of rwb-access; operation name Not specified in the source documents (GAP-3081; ASM-5249) | P4 rwb-access | The capability right, the scope and the masking rule of the caller, and the accept of the AC-READ record |

Every call is one hop with a 2 s budget and a breaker, and none retries inside the section; the case-record contract is the one C row of this slice (DP-11, ADR-020).

#### 12.3 Events published

None. A read publishes no business event: the AC-READ access record is written locally through the library of DP-03 and relayed by rwb-decision on the shared `rwb.decision-record.v1`, and this service's own topic `rwb.deviation.events.v1` carries the two events of its write stories, not this one (DP-14 applied as naming only; ASM-5245).

#### 12.4 Events consumed

None. Every section is read when the page is opened, so a stale answer is answered with its own stamp and MSG-P1-001 rather than kept fresh by a subscription (BR1, BR2). The deviation block reads its own table; no other service's event changes it.

#### 12.5 Workflows and activities

None. The page is a synchronous read with no workflow, no activity and no timer; the `deviation` rows it reads are written by `DeviationWorkflow` on `rwb-deviation`, which belongs to the write stories of this service.

#### 12.6 Schedules

None. The Ownership Map gives S8 no job, and this story declares no Schedule, no Quartz row and no shared job table.

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | Read only: the open codes, the raise facts, the contact stop, the handler, the return point and the state |
| `decision_record` | Platform library in `rwb_deviation` | Written: one AC-READ record per read, before the answer (DP-03) |

`recovery_case`, `case_account`, `case_party`, `queue`, `timer`, `interaction`, `document`, `rule_row` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` and `deviation` carries no column of another service's fact (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case case-record fake (`RWB-P3-E1023-CON`) | The header of a synthetic case with its queue, owner, status, entry and prescription dates, its links, its parameters and its six lists; an out-of-scope team; a case on hold; a link with no answer | AC1, AC2, AC5, AC9, AC12 |
| rwb-source-data data-product fake | Accounts, parties with contacts and the contact history with fresh stamps; a stale stamp; an account with no answer; an empty contact history | AC1, AC2, AC3, AC4, AC10, AC11, AC12 |
| rwb-document list fake | 50 documents; an empty list; no answer inside 3 s | AC1, AC6, AC10 |
| rwb-access authorise and mask fake | A right and a scope; a refusal; a masking rule per role; the accept of the AC-READ record | AC5, AC8, TC-E1-023-11 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain; a rejected AC-READ write | AC7 |
| gateway-bff composite route fake | The assembled SCR-03 for a synthetic case | AC1 to AC12 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 5 consumed | The five reads on `/api/recovery/deviation/v1`; the rwb-case, rwb-source-data (two), rwb-document and rwb-access calls; one hop, 2 s, 3 s for the document section |
| Kafka | None | No business event published or consumed; the AC-READ record rides the library's `rwb.decision-record.v1` |
| Temporal | None | A synchronous read; no workflow, activity or Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The five read handlers on the target base, `CaseRecordViewGuard`, `CaseRecordViewService`, `CaseSectionReader`, `DeviationBlockReader`, `MaskingApplier` with the AC-READ writer, the six section components with their badges and banners, and the failure, access and boundary tests.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, "recovery schema" | Own schema `rwb_deviation`; no other service's table is read | None |
| DP-02 | `recovery_svc` login | One login per service; login name Not specified in the source documents (GAP-0692) | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` (not in the empty build row, ASM-5244) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts through rwb-source-data's contract | None |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H `RWB-PLT-E1042-CON`; C `RWB-P3-E1042-CON` |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H `RWB-PLT-E1037-CON`; C `RWB-P4-E1037-CON` |
| DP-11 | In-process call, published interface | REST contract with mock, one hop, 2 s | C from the legacy dependency (`RWB-P3-E1023-CON`) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topics | Topic `rwb.deviation.events.v1`; naming library | H `RWB-PLT-E1047-CON` (naming only, ASM-5245) |
| DP-15 | V0001 baseline, migration | Per-service Flyway in `rwb_deviation` | H `RWB-PLT-E1044-CON` |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

**Build steps.** (1) Wire the guard and the five read handlers on the target base. (2) Read the header, links, queue, parameters and lists from rwb-case on its contract, the accounts, parties and contact history from rwb-source-data with their stamps and freshness answers, the documents from rwb-document, and the deviation block from `deviation`. (3) Apply the masks and the scope and write the AC-READ record before the answer. (4) Build the six section components with their badges and the stale, on hold and empty banners. (5) Prove AC1 to AC19, the access refusal, the forced record failure and the boundary test; the section timeout, the masks and the lists are parameters and reference data (DP-06, DP-07; ASM-5250).

**Done when.** AC1 to AC19 pass at component and contract level on the fakes, NFR-009 holds in SIT, the boundary test shows no `v_ace_*` read and no statement on any schema but `rwb_deviation`, and a refused AC-READ write returns 503 with MSG-P7-003 and no data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A section's answer is not fresh for the latest business date (X1) | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | The case is on hold (X6) | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-024 | A section has nothing to show (X7) | Nothing is recorded in {section} yet. |
| MSG-P3-023 | A section cannot be shown (X3) | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | The role lacks the right (X8) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the scope (X2) | This case is not in your scope. |
| MSG-P7-003 | The AC-READ record cannot be written (X4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The wording is the legacy and FSD wording, copied unchanged except MSG-P1-001, which takes the Error and Message Standard v4 wording; no other message is reworded and none is added. The legacy "decision log store" of MSG-P7-003 is read here as the local AC-READ record, which is why the message is not reworded (DP-03; ASM-5245).

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-02 Case list | Empty and Loading: as Screen Specifications v1 SCR-02. Error: Not specified in the source documents (CG-ALL-11303). No access: Not specified in the source documents (CG-ALL-11303). | Not owned by this story; the timers only, via the gateway-bff composite route (ASM-5243) |
| SCR-03 Case record | Loading: skeleton rows per section. Read only: fields without edit controls; the header, the deviation block and five sections, each with the business date of its answer. On hold: the banner with the code and the prescription date. Stale input: MSG-P1-001 above the section. Error: Not specified in the source documents (CG-ALL-11304). Empty: Not specified in the source documents (CG-ALL-11304). No access: Not specified in the source documents (CG-ALL-11304). | The five reads of section 12.1 and the deviation block behind the gateway-bff composite route (DP-19) |
| SCR-04 | Loading: as Screen Specifications v1 SCR-04. Empty: Not specified in the source documents (CG-ALL-11305). Error: Not specified in the source documents (CG-ALL-11305). No access: Not specified in the source documents (CG-ALL-11305). | Not owned by this story; the timers only, via the gateway-bff composite route (ASM-5243) |

The screen shows no Workbench load, job or file status, and no edit control (BR6). The composite route also calls rwb-case for the case list and the timers of SCR-02 and SCR-04; this story fixes only its own answers (ASM-5243).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-01 | AC1, BR7 | NFR | Case with 50 documents and 120 contact-history entries; 50 openings |
| TC-E1-023-02 | AC2, BR1 | Component | Account answer A-7001 at 97 days past due, `dataAsOf` 2026-12-02; header answer of RW-2026-000701 |
| TC-E1-023-03 | AC3, BR8, BR10 | Component | Person answer P-7001 with category RETAIL, a mobile contact, EFS entries and ledger entries |
| TC-E1-023-04 | AC4, BR2 | Component | Account answer at 2026-12-02 with the ALS answer for 2026-12-03 not COMPLETED |
| TC-E1-023-05 | AC5, BR5 | Contract | Case of team LIT-BKK, rwb-access answer scope Own |
| TC-E1-023-06 | AC6 | Component | rwb-document answer absent inside 3 s |
| TC-E1-023-07 | AC7, BR4 | Component | Decision-record stub rejecting every AC-READ write |
| TC-E1-023-08 | AC8, BR3 | Component | Phone collector with no clear-view masking rule |
| TC-E1-023-09 | AC9 | Component | Open deviation X1 in `rwb_deviation`, case answer ON_HOLD with 2028-03-15 |
| TC-E1-023-10 | AC10 | Component | Empty document answer and empty contact history |
| TC-E1-023-11 | Access (AC5, AC13, X8) | Contract | RW-REFADM calls `GET /cases/{caseId}` and is refused with MSG-P4-002 |
| TC-E1-023-14 | Boundary (AC14, X10) | Build | A statement reads a `v_ace_*` view or another service's schema; the grant refuses it and the boundary test fails the build |
| TC-E1-023-15 | Read only (AC15, BR6) | Component | The page shows no edit control and moves no case status |
| TC-E1-023-16 | Deviation block (AC16, BR11) | Contract | The deviation block reads `deviation` in `rwb_deviation` only and copies no flag from another service |
| TC-E1-023-17 | No personal data at rest (AC17, BR12) | Contract | No person name, contact value, address or identity number is written to `rwb_deviation`, the AC-READ record, a log or a prompt |
| TC-E1-023-18 | AC18, X8 | Contract | GET /cases/{caseId} without a valid session answers 401; a caller refused the access right answers 403 |
| TC-E1-023-19 | AC19 | Contract | rwb-case answer carries a status change the status model does not allow; the change is refused |
| TC-E1-023-12 | AC11, BR8 | Contract | A-7001 balance changed between two P1 answers |
| TC-E1-023-13 | AC12, BR9 | Component | Case link A-7010 with no P1 answer row |

The thirteen ids are the legacy cases of RWB-E1-023, kept in their legacy order; TC-E1-023-14 is the boundary test of AC14 and has no legacy case; the two that read two services at once are carried at Contract level and their end-to-end half belongs to the wave 1 harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id.

### 17. Guardrails

- No business value in code: the section timeout, the masks, the labels and the six lists are parameters and reference data read at their version (DP-06, DP-07).
- No personal data in `rwb_deviation`, the AC-READ record, a log, a screen cache or a prompt; test parties are synthetic and the application log holds case numbers only.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema is read here, and a statement that tries is refused by the grant and fails the boundary test (DP-01, DP-02, DP-05).
- The page holds no copy of a source record; the identity number is masked inside the P1 answer and the contact values are masked at the API by role (BR3, BR8).
- A personal field is never shown when the AC-READ record cannot be written (BR4).
- One base, one topic, one queue and one login per service; this story adds no second base and no new topic (DP-13, DP-14).

### 18. Traceability

| Legacy | Story | Test | Feature | L3 process |
|---|---|---|---|---|
| RWB-E1-023 AC1 to AC12 | Not copied as owned criteria: the plan assigns this slice no legacy AC (GAP-3083); AC1 to AC12 restate each scenario as new (D-RCV-60) with the legacy values kept | TC-E1-023-01 to TC-E1-023-10, TC-E1-023-12, TC-E1-023-13 | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| RWB-E1-023 section 12, five read endpoints | Section 12.1 on `/api/recovery/deviation/v1` | TC-E1-023-02, TC-E1-023-05 | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| RWB-E1-023 Access test | AC5, X8 | TC-E1-023-11 | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| RWB-E1-023 BR1 to BR10 | BR1 to BR10, restated with the owner's contract as the source | Section 16 | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |

| Source | What it supplies | Feature | L3 process |
|---|---|---|---|
| REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006, REQ-ACA-009 | The view, its freshness stamp, the masking, the access log and the scope | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| REQ-DVH-006 (FSD S8 Requirements served) | The deviation flag on the case record view, which is why the block is this service's | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| Legacy RWB-E1-023 sections 1 to 19 | The story, the flow, the twelve scenarios, the ten rules, the seven messages, the fields, the thirteen test cases and the screen states, all kept in substance | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| TSD S8 T3.0, T3.1, T4, T6.1 and T5.2 | The `deviation` columns, the DEVIATION states, the Case record rights and the published-interface rule | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| Context pack S8 rwb-deviation and the connection matrix | Schema, base, topic, queue, the one owned table, and the P1 REST and event link | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |
| Split plan, slice RWB-S8-E1023-APP | H, C, I, X, the lane, the wave and the release (GAP-3082, GAP-3084; ASM-5251) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1023-APP-2) |

### 19. Out of scope

- The contract surface of the case reads: the OpenAPI document, the shapes, the error set and the fakes (RWB-P3-E1023-CON).
- The case of record, its status transitions, its stage, its route, its timers and its assignment (rwb-case, P3), including the case list and the other SCR-03 consumers.
- The ingestion, the views and the freshness batches of ACE (rwb-source-data, P1); the documents, their upload and their retention (rwb-document, P5); the rights and the access log store (rwb-access, P4).
- Raising, working and clearing a deviation, the contact stop and the on hold transition (the deviation write stories of this service, RWB-E1-062, RWB-E2-015 and RWB-S8-E7001-APP).
- The editable case view (RWB-E2-016), the history timeline (RWB-E1-035), document upload and search (RWB-E1-026) and the ledger write (RWB-E1-066, RWB-E1-067).
- The schema, the migration, the login and the deployment of `rwb_deviation` (the DB, INF and OPS stories of this key), and any change to a legacy file or to built Epic 1 code.
