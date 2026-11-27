# RWB-ITG-E1023-ITG Case record view v1, read only

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Freshness fields and the STALE rule: AC4 restated to the DP01 `expected_by` of the next day, never-stamped AC31 added (RD-P1-005, RD-P1-041; findings #2, #3).
- Contact history is the P1 ledger only; case-scoped append and read with the 5.1.0 names and business keys (RD-P1-007, RD-P1-023; findings #4, #5).
- `AceDataLate` key and payload; REC-05 read through the reconciliation results; build dependencies (RD-P1-003, RD-P1-022, RD-P1-040; findings #1, #6, #7).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1023-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1023-ITG-16); the squad sizes it at refinement; the two-week fit is not specified in the source documents (DOR-RWB-ITG-E1023-ITG-15) |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P1-E1066-APP, RWB-P5-E1024-APP, RWB-P4-E1039-APP, RWB-P1-E1068-APP, RWB-P1-E1069-APP, RWB-P3-E1023-APP, RWB-P4-E1023-APP, RWB-S8-E1023-APP (not done yet) |
| Contract dependencies | None. Consumed P1 contract: rwb-source-data.yaml 5.1.0 (API Specification v7) with its AsyncAPI file; reconciliation results as published by RWB-P1-E1011-CON |
| Integration dependencies | RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P1-E1066-APP, RWB-P5-E1024-APP, RWB-P4-E1039-APP, RWB-P1-E1068-APP, RWB-P1-E1069-APP, RWB-P3-E1023-APP, RWB-P4-E1023-APP, RWB-S8-E1023-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-030, FR-PLT-031, FR-PLT-032, FR-PLT-033) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003; RD-P1-005; RD-P1-007; RD-P1-022; RD-P1-023; RD-P1-040; RD-P1-041 |
| Open decisions | DL26 open; assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355 confirmed by the programme directive |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-023 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1023-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (33 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-023 read-only case record view composed by gateway-bff from rwb-case (P3), rwb-source-data (P1), rwb-document (P5), rwb-access (P4) and rwb-deviation (S8)**, so that **the freshness stamp of every section, the no-copy boundary, a case link with no ACE row, the masking position, the access record, the merged contact history and the degraded document section are proved on the real wave 1 services before the wave exits**.

### 2. Business rationale

RWB-E1-023 puts one read-only screen per case in front of the case owner: case number, accounts and arrears, parties and contacts, contact history, documents, each section carrying the ACE business date behind it. Under the legacy design the screen read `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_efs_action` inside the P3 module, merged the EFS entries with the Workbench interaction ledger in one time order, masked each personal field by the caller's role and wrote one AC-READ access record per open. The component copy of that behaviour sits in RWB-P3-E1023-APP, which owns the legacy criteria AC1, AC2, AC3, AC5, AC6, AC7, AC8, AC9 and AC10 against the published contracts of the services it needs.

This integration story owns the three criteria that no single service can prove: AC4 (a section whose ACE batch is not complete shows its earlier business date and the stale banner, with no Workbench load date anywhere), AC11 (the Accounts section follows the newest ACE batch and no Workbench table holds the earlier balance) and AC12 (an `account_key` on a case link with no view row shows with empty values, the rest of the case still shows, and the key is listed for the data steward and the ACE team). Each of the three is a statement about two owners at once: the staleness and the freshness stamp are facts about the P1 data product, the no-copy rule is a fact about the boundary between P1 and P3, and the missing view row is found by the P1 reconciliation while the link that must not be invented is the P3 case link. Asserted inside one service, each of them passes while the other side is wrong.

The target moves the source of the facts, never the behaviour. Only rwb-source-data reads the ACE views (DP-05, DP-01), so account, customer, contact and EFS facts and the business date of each data product reach the screen through the P1 contract and its freshness read. The interaction ledger belongs to rwb-source-data under the default ruling (DP-18), so the contact history is the P1 ledger merged with the case entries of rwb-case in one time order, each row naming its own source system. Documents belong to rwb-document and are read on the P5 contract. The masking rule and the access log belong to rwb-access (DP-08), so the question of which field is clear is answered by P4 and the personal value itself never leaves the owner. The screen is composed by gateway-bff with the owner calls in parallel, one hop each, inside the 2 s budget and with a breaker per service (DP-19, DP-11), and the paths become `/api/recovery/<short>/v1` (DP-13). The section budget, the labels and the list values are data read through the P3 parameter and reference-data contracts (DP-06, DP-07), the topic names follow `rwb.<short>.events.v1` (DP-14), each schema is migrated by its own service (DP-15), and each service signs in with its own login (DP-02).

Three points are not fixed by the sources and are carried as one gap and one assumption. The ownership map holds `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` for rwb-deviation but no read of the deviations of a case, and Arch v5 puts rwb-deviation in wave 2 while this wave 1 story lists RWB-S8-E1023-APP as an integration dependency, so the read path of AC18 is read from Arch v5 slides 15 and 41 and the service is assumed present in SIT. The fixture composition of the run is the RWB-ITG-W1J01-ITG set and is not itemised in any source. Both are recorded in GAP-0348 and ASM-0442. Release 30 November 2026 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1023-APP is done: the case record reads, the section composition, the scope check, the masking call and the refusal when the access record cannot be written are in SIT on rwb-case.
- RWB-P1-E1069-APP is done: the ACE view contract and the account, customer, contact and EFS facts by business key are published on base `/api/recovery/source-data/v1`. RWB-P1-E1015-APP is done: the freshness stamp of each data product is written and served, and `AceDataReady` and `AceDataLate` are published. RWB-P1-E1011-APP is done: REC-05 runs in `ReconciliationWorkflow`.
- RWB-P1-E1068-APP and RWB-P1-E1066-APP are done: the interaction ledger is appended through `POST /cases/{caseId}/interactions` and read through `GET /cases/{caseId}/interactions`, with `occurredAt`, `channel`, `contactResult` and `sourceSystem` (`WORKBENCH` or `EFS`).
- RWB-P5-E1024-APP is done: the documents of a case are readable through the rwb-document contract on base `/api/recovery/document/v1`.
- RWB-P4-E1023-APP is done: the masking rules by role are in force and name the view field IDs, and the answer carries the clear or masked position of each field.
- RWB-P4-E1039-APP is done: the access log records one AC-READ entry per read with the field IDs and their masked flags, and the log is readable on `GET /api/recovery/access/v1/admin/access-log`.
- RWB-S8-E1023-APP is done: the deviation of a case and its prescription date are readable through the rwb-deviation contract for AC18.
- The published contracts of P1, P3, P4, P5 and S8 are versioned in the registry, and the run consumes only those contracts.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic accounts, parties, contacts, case links, documents, ledger entries, batch rows and masking rules.
- SIT is in place with gateway-bff in front of every owner base, the namespace `rwb-recovery`, the topic `rwb.source-data.events.v1` with its retry and `.dlt` topics, and the schema registry.
- rwb-deviation is a wave 2 service in Arch v5 slide 41 and this story lists it as an integration dependency; the run therefore needs its contract in SIT. That reading is the assumption ASM-0442 and the point is in GAP-0348.
- No production data is read, copied or connected to; every account, person, contact value, case number and document used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: seeds the synthetic set for case RW-2026-000701 through the harness RWB-ITG-W1J01-ITG — account A-7001 at 97 days past due with THB 206,175.00 and data as of 2026-12-02, person P-7001 with the masked identity and one mobile contact, the link to A-7010 with no view row, 50 documents, 120 ledger entries, and the batch rows for 2026-12-02 and 2026-12-03; each ledger entry is appended through `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` (`InteractionRequest` 5.1.0, header `Idempotency-Key`, body `idempotencyKey` in the business key form `<code>-<caseNo>-<yyyyMMdd>-<actionId>`, or `EFS:<efsRecordKey>` for a history entry); no service schema is opened and no production row is used.
2. Harness: signs in through gateway-bff as U-81 holding RW-CASEOWN with Case record R and scope Own, and reads `GET /api/recovery/access/v1/me/permissions` for the masking position of the role.
3. Harness: opens SCR-03 for RW-2026-000701 through the gateway-bff composite route and records the call set and the elapsed time of each owner call.
4. Gateway-bff: calls the P3 header read, the P3 accounts read, the P3 parties read, the P1 interactions read, the P5 documents read, the P1 freshness read and the S8 deviation read in parallel, one hop each, inside the 2 s budget and with the breaker of each owner.
5. Harness: asserts the header (case number, product, status "IN_PROGRESS", stage, route, owner U-81, queue "TDR-BKK-CO", entry date, prescription date, deviation and hold flags) and the five sections, each with the business date of its own data product read from the P1 freshness contract.
6. Harness: asserts the Accounts section for A-7001 at 97 days past due and THB 206,175.00 with business date 2026-12-02, and that no response holds a load date, a job status or a batch run of a service.
7. Harness, AC4: sets the batch state so that no COMPLETED ALS row exists for 2026-12-03, advances past the DP01 `expected_by` of 08:00 on 2026-12-04, opens the view and asserts that the Accounts section keeps business date 2026-12-02 with `status` STALE and `staleSince` 2026-12-03, that the stale banner shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-02, and that no Workbench load or job status shows.
8. Harness, AC11: moves the ALS batch of 2026-12-03 to THB 210,000.00 for A-7001, opens the view again and asserts that the Accounts section shows THB 210,000.00 with business date 2026-12-03, and that no service holds the earlier balance for the case: the case read, the accounts read and the P1 contract are the only sources and none of them returns 206,175.00 for that date.
9. Harness, AC12: reads the case link A-7010 with no view row, opens the view and asserts that the Accounts section shows A-7010 with empty balance and days past due, that the other four sections show, and that the P1 reconciliation results of REC-05 list A-7010 for the data steward and the ACE team.
10. Harness: asserts the contact history as one time order of 120 entries with the source system on each row and no duplicate, the masking outcome for U-82 under a clear rule and under no clear rule, the one AC-READ record in the P4 access log with the field IDs and their masked flags, the refused read when that record cannot be written, the deviation flags of AC18 without a copy in the P3 response, the document-hub timeout path, and the refusal of a role without Case record R at the first owner call.
11. Harness: proves from the call set of the run that no service schema and no view was opened, that no call passed through another service, and that no fake stood in for a P1, P3, P4, P5 or S8 contract; then writes the evidence report, removes the synthetic set and restores the batch state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The data product behind a section is STALE: no completed batch exists for the expected business date at its `expected_by` | The section shows with the business date of the stamp in use and the stale banner; a product never stamped shows no business date | MSG-P1-001 | AC4, AC31 |
| X2 | The case is outside the caller's scope | The scope answer of the P4 contract refuses the case and the screen returns 404 with nothing shown | MSG-P4-003 | AC24; TC-E1-023-05-ITG, regression for RWB-P3-E1023-APP |
| X3 | The document hub does not answer inside the 2 s budget | The Documents section shows the section message, the breaker opens for that owner, and the other sections show | MSG-P3-023 | AC19 |
| X4 | The access record cannot be written | The authorise call is refused, the read returns no case data and no personal field shows | MSG-P7-003 | AC15 |
| X5 | The role may not see a personal field in clear | The field shows from the masked field of the owner and the access record carries the masked flag | None | AC16 |
| X6 | The case is on hold | The on-hold banner shows the deviation and the prescription date read from the S8 contract | MSG-P3-004 | AC18 |
| X7 | The case has no documents and no contact history | Each section shows its empty sentence | MSG-P3-024 | AC21; TC-E1-023-10-ITG, regression for RWB-P3-E1023-APP |
| X8 | A role without Case record R opens the view | The first owner call, the P4 authorise check, refuses with 403 and no other owner is called | MSG-P4-002 | AC20 |
| X9 | A case link holds an `account_key` that the view does not return | The Accounts row shows the key with empty values, REC-05 lists it, and the rest of the case shows | None | AC12 |
| X10 | A consumed call exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy, the breaker of that owner is recorded, and no assertion is made on data that was not read | None | AC13 |
| X11 | A consumed contract drifts from the published one, or the synthetic set does not match the run | The preflight fails on the contract test or on the fixture check and the run stops before any assertion; no fake is put in place of a service contract | None | AC13, section 17 |

X1, X3, X4, X5, X6 and X9 are the exception paths of the legacy story read on the wave 1 services; X2, X7 and X8 are the legacy paths whose criteria belong to RWB-P3-E1023-APP; here X2 is covered by AC24 and X7 by AC21, and all three run as regression evidence; X10 and X11 are the suite's own failure modes, so that a timeout never becomes a pass.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the integration dependencies and the published contracts of P1, P3, P4, P5 and S8, not their source code, and it owns no schema and no table |
| Negotiable | The fixture sizes, the poll interval, the retry of the suite and the report layout are configuration; the criteria, the message IDs, the keys and the values are fixed by the legacy story |
| Valuable | Proves across services what no single service can prove: the freshness stamp of each section, the no-copy boundary, the missing view row, the masking position, the access record, the merged contact history and the degraded section |
| Estimable | One suite module, one fixture pack, eight probes, one composed-route assertion and one evidence report |
| Small | Eleven scenarios over five services, one composed route and one topic, with no service code and no schema change |
| Testable | Every criterion asserts a contract response, a record, a message, a status or the absence of a value, and every value is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Case record view v1, read only, proven across the wave 1 services

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest ACE batch business date is 2026-12-02 and the P1 freshness read shows DP01, DP02 and DP05 with status LOADED and businessDate 2026-12-02
    Given the wave 1 services rwb-case, rwb-source-data, rwb-document and rwb-access are deployed in SIT with their published contracts behind gateway-bff, and rwb-deviation is treated as available in SIT for the wave 1 run (GAP-0348)
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production data is used
    Given the authorise request for the CASE_RECORD area carries the case reference, the owner, the queue, the team, the region, the action and the field IDs asked about, and the matrix version PM-2026.12 and the masking version MASK-SIT-01 are the versions in force on 30 November 2026; a later version reaches the view only through rwb.access.AccessPolicyChanged.v1
    Given the field IDs of this slice are DF-PTY-007, DF-PTY-008 and DF-PTY-016, and any other field ID is accepted as data and marked masked when no row covers it

  Scenario: AC4 Stale ACE batch (legacy RWB-E1-023 AC4)
    Given no COMPLETED ALS batch row exists for 2026-12-03 and the DP01 expected_by of 08:00 on 2026-12-04 has passed
    Given GET /api/recovery/source-data/v1/data-products/freshness answers DP01 with businessDate 2026-12-02, status STALE and staleSince 2026-12-03
    When U-81 opens the view on 2026-12-04
    Then the Accounts section shows business date 2026-12-02
    Then the stale banner shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-02
    Then no Workbench load or job status shows

  Scenario: AC11 No copy of the account on the case (legacy RWB-E1-023 AC11)
    Given the balance of account A-7001 for case RW-2026-000701 was THB 206,175.00 on 2026-12-02
    Given the ALS batch for 2026-12-03 holds THB 210,000.00 for A-7001 and the DP01 stamp of 2026-12-03 is LOADED
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows THB 210,000.00 and business date 2026-12-03
    Then no Workbench table holds the previous balance for the case

  Scenario: AC12 An account link with no ACE row (legacy RWB-E1-023 AC12)
    Given case RW-2026-000701 links account_key A-7010
    Given the rwb-source-data account read, through the owner contract under DP-01 and DP-05, returns no row for A-7010
    When U-81 opens the view
    Then the Accounts section shows A-7010 with empty balance and days past due
    Then the rest of the case shows
    Then after ReconciliationWorkflow recon-{businessDate} has run, GET /api/recovery/source-data/v1/admin/reconciliation/results lists account_key A-7010 under REC-05 for the data steward and the ACE team (rwb-case key-list read that feeds REC-05: path Pending, GAP-3273)

  Scenario: AC13 The composed screen loads from the owners in parallel (new, D-RCV-60)
    Given case RW-2026-000701 has 50 documents and 120 contact history entries
    Given the gateway-bff composite route settles the view from the P3, P1, P5, P4 and S8 owner calls
    When U-81 opens case RW-2026-000701
    Then the header and the five sections show from one composed response
    Then GET /api/recovery/case/v1/cases/{caseId}, GET /api/recovery/case/v1/cases/{caseId}/accounts, GET /api/recovery/case/v1/cases/{caseId}/parties, GET /api/recovery/source-data/v1/cases/{caseId}/interactions and GET /api/recovery/document/v1/cases/{caseId}/documents are issued in parallel, one hop each
    Then each owner call answers inside the 2 s budget and no call passes through another service

  Scenario: AC14 The freshness stamp of every section comes from the P1 contract (new, D-RCV-60)
    Given GET /api/recovery/source-data/v1/data-products/freshness returns business date 2026-12-02 for "DP01 Account and arrears"
    Given the Accounts section reads account A-7001 at 97 days past due with THB 206,175.00
    When U-81 opens the view
    Then the Accounts section shows business date 2026-12-02 and each other section shows the business date of its own data product
    Then no Workbench load date, job status or batch run of a service appears in any section or in any response
    Then no rwb.source-data.AceDataLate.v1 with record key "ALS:2026-12-02" is on rwb.source-data.events.v1 while DP01 reads status LOADED for 2026-12-02

  Scenario: AC15 One AC-READ record per open, across rwb-case and rwb-access (new, D-RCV-60)
    Given U-81 holds RW-CASEOWN with Case record R and the case is in scope Own
    Given the P4 access-record contract accepts the write
    When U-81 opens the view
    Then GET /api/recovery/access/v1/admin/access-log holds exactly one AC-READ record for case RW-2026-000701 with user U-81, the field IDs read and their masked flags
    Then the record holds no clear personal value
    When the P4 access record cannot be written and the authorise call is refused
    Then rwb-case returns status 503 with MSG-P7-003 and no case data
    Then the access log holds no record for that call

  Scenario: AC16 The masking rule of rwb-access decides the clear field (new, D-RCV-60)
    Given phone collector U-82 holds the masking rule that lets RW-PHONECOL see DF-ACE-078 in clear
    Given the case is in U-82's scope
    When U-82 opens the view
    Then GET /api/recovery/access/v1/me/permissions returns the position of RW-PHONECOL for DF-ACE-078 as clear
    Then the phone shows 0812345678 from the P1 field DF-ACE-078 and the identity shows XXXXXXXXX4821 from DF-ACE-073
    Then the clear phone value appears in no rwb-case response, no cache and no log of the run
    When the masking rule in force for RW-PHONECOL names DF-ACE-078 as masked
    Then the phone shows XXXXXX5678 from DF-ACE-079

  Scenario: AC17 One contact history from the P1 ledger (new, D-RCV-60)
    Given the entries of case RW-2026-000701 are appended through POST /api/recovery/source-data/v1/cases/{caseId}/interactions, 120 entries with distinct business keys, the EFS history entries keyed "EFS:<efsRecordKey>"
    Given GET /api/recovery/source-data/v1/cases/{caseId}/interactions returns them with occurredAt, channel, contactResult and sourceSystem WORKBENCH or EFS
    When U-81 opens the view
    Then the Contact history section shows 120 entries in one time order by occurredAt descending, the page size read from a parameter
    Then each row carries the source system of its own row and no entry appears twice
    Then the view reads the contact history from rwb-source-data only, and no rwb-case response holds a copy of a ledger entry

  Scenario: AC18 The deviation and hold flags come from the S8 contract (new, D-RCV-60)
    Given case RW-2026-000701 has status "ON_HOLD" for deviation X1 with prescription date 2028-03-15
    Given GET /api/recovery/deviation/v1/deviations?caseId={caseId} returns deviation X1 with prescription date 2028-03-15
    When U-81 opens the view
    Then the header shows the deviation flag "X1" and the hold flag
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15
    Then the case read holds no copy of the deviation or of its prescription date

  Scenario: AC19 The document hub timeout shows one section message (new, D-RCV-60)
    Given the document hub does not answer within the 2 s budget
    When U-81 opens the view
    Then the Documents section shows MSG-P3-023 for "Documents"
    Then the header, accounts, parties and contact history show
    Then the breaker of rwb-document is open for the next call of the run

  Scenario: AC20 A role without Case record R is refused at the first owner call (new, D-RCV-60)
    Given RW-REFADM holds no Case record R
    When RW-REFADM opens the view for case RW-2026-000701
    Then POST /api/recovery/access/v1/authorise refuses the request with MSG-P4-002
    Then no rwb-case, rwb-source-data, rwb-document or rwb-deviation call is made
    Then no case data shows

  Scenario: AC21 The view shows the empty state of a case with no documents and no history (new, D-RCV-60)
    Given case RW-2026-000701 has no documents and no contact history entries
    When U-81 opens the view
    Then the Documents section shows no document row
    Then the Contact history section shows no entry
    Then the header and the Accounts section still show
    Then the Documents section shows MSG-P3-024 for "Documents"
    Then the Contact history section shows MSG-P3-024 for "Contact history"

  Scenario: AC22 The view shows a loading state until the composed response settles (new, D-RCV-60)
    Given the gateway-bff composite route has not yet settled the view for case RW-2026-000701
    When U-81 opens case RW-2026-000701
    Then every section shows its loading state and no stale or empty value
    Then the sections change to their values from the one composed response

  Scenario: AC23 The view shows the error state when rwb-case refuses the read (new, D-RCV-60)
    Given rwb-case answers status 503 for GET /api/recovery/case/v1/cases/{caseId}
    When U-81 opens case RW-2026-000701
    Then the view shows MSG-P7-003 and no case data
    Then no section shows a value from a previous response

  Scenario: AC24 A case outside the caller's scope is refused with 404 and nothing shown (legacy RWB-E1-023 X2, new, D-RCV-60) (new, D-RCV-60)
    Given U-81 holds RW-CASEOWN with Case record R
    Given case RW-2026-000701 is outside the scope of U-81
    When U-81 opens the view for case RW-2026-000701
    Then the P4 scope answer refuses the case with MSG-P4-003
    Then the screen returns 404 and no section shows

  Scenario: AC25 The view has no edit control in Epic 1 (BR6, new, D-RCV-60) (new, D-RCV-60)
    Given case owner U-81 owns case RW-2026-000701
    When U-81 opens the view
    Then no section of the view shows an edit control
    Then the view sends no write request for the case

  Scenario: AC26 The labels, budget and list values come from the P3 contracts (BR13, new, D-RCV-60) (new, D-RCV-60)
    Given the P3 parameter and reference-data contracts are published
    When U-81 opens the view
    Then every section label, the section budget and every list value show from those contracts
    Then no label or list value is coded in the view
    Then the section timeout is read as a parameter of rwb-case and the six lists are read as reference data of rwb-case, with no value copied into code

  Scenario: AC27 Topics and logins follow the service convention (BR14, new, D-RCV-60) (new, D-RCV-60)
    When the run publishes and signs in for each wave 1 service
    Then every topic is named rwb.<short>.events.v1
    Then each service signs in with its own login and no shared login or legacy topic prefix is used

  Scenario: AC28 Each service migrates its own schema (BR15, new, D-RCV-60) (new, D-RCV-60)
    When the run starts
    Then the suite runs no migration and owns no schema
    Then each wave 1 service migrates its own schema on its own Flyway sequence

  Scenario: AC29 No personal data in the suite's fixtures, events, logs or report (BR17, new, D-RCV-60) (new, D-RCV-60)
    When the run writes its fixtures, events, logs and report
    Then they hold account keys, person keys, case numbers, document IDs, field IDs and business dates only
    Then the clear contact value of AC16 is read from the owner inside the run only

  Scenario: AC30 No service schema is opened and no published contract is faked (BR18, new, D-RCV-60) (new, D-RCV-60)
    Given a consumed service contract drifts from its published contract
    When the preflight runs
    Then the preflight fails on the contract test and the run stops before any assertion
    Then no service schema is opened and no fake replaces a service contract

  Scenario: AC31 A data product that has never been stamped shows no business date
    Given no freshness stamp has ever been written for DP05
    When U-81 opens the view
    Then GET /api/recovery/source-data/v1/data-products/freshness answers DP05 with businessDate null and status STALE
    Then the section fed by DP05 shows the stale banner with MSG-P1-001 and no business date, and the other sections show
```

**Target reading.** In the monolith the P3 module reads `recovery.v_ace_*` itself, merges the EFS rows with its own ledger and writes the access event from inside the case module. In the target only rwb-source-data reads the views and serves the account, customer, contact and EFS facts and the business date of each data product (DP-05, DP-01), the interaction ledger is P1's (DP-18), the documents are P5's, the masking rule and the access log are P4's (DP-08), the screen is composed by gateway-bff with the owner calls in parallel and a breaker per owner (DP-19, DP-11), and every path moves to `/api/recovery/<short>/v1` (DP-13). `v_ace_batch_status` and `v_ace_account.data_as_of` of AC4, the earlier balance of AC11 and the missing row of AC12 are therefore asserted through the P1 freshness read and the P1 reconciliation output, never by opening a view; the deviation of AC18 is read from the S8 contract and never copied into rwb-case. No value is invented and no service table is read (GAP-0348; ASM-0442).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every section shows the business date of the data product behind it, read from the P1 freshness contract; no Workbench load date is used | REQ-RDF-009; VR-P3-001-1; DP-05 |
| BR2 | A section whose data product has status STALE shows the stale banner | MSG-P1-001; screens.txt Common states "Stale input"; the P1 freshness stamp |
| BR3 | A personal field shows in clear only when the masking rule in force lets the caller's role see it; the identity number is never in clear because the owner exposes the masked identity and the last four digits only | REQ-ACA-005; CTL-11; DL26; DF-ACE-073, DF-ACE-074 |
| BR4 | Every read of personal data writes one AC-READ record with the field IDs and their masked flags; a read whose record cannot be written returns no data | REQ-ACA-006; RWB-E1-039 BR2; DP-08 |
| BR5 | Only cases in the caller's scope open; others return 404, and the refusal is the answer of the P4 authorise contract | CTL-09; REQ-ACA-009 |
| BR6 | The view has no edit control in Epic 1 | SCR-03 "E1 read only" |
| BR7 | The view loads in under 2 seconds with 50 documents | NFR-009 |
| BR8 | Account, customer, contact and collections history data are read live by business key through the owner's contract; no service holds a copy and no service shows its own load status | D-RCV-35 U1 and U4; ADR-010; DP-01; DP-05 |
| BR9 | A case link with no view row shows the business key with empty values and is listed by REC-05; it is never deleted or rewritten | REC-05; Data Tier Map section 5 |
| BR10 | The contact history is the P1 ledger in one time order, each row naming its source system (`WORKBENCH` or `EFS`); other services append to it and no service keeps its own copy | E1-068; interaction.source_system (DF-INT-013); DP-18 |
| BR11 | The screen is composed by gateway-bff with one hop per owner, the owner calls in parallel, a 2 s budget and a breaker per owner; no owner calls another owner for this screen | ADR-020; DP-11; DP-19; Arch v5 slide 20 |
| BR12 | The deviation and hold flags of the header and the on-hold banner are read from the S8 contract; rwb-case keeps the flag, never a copy of the deviation or its prescription date | Arch v5 slide 15; DP-01 |
| BR13 | The section budget, the labels and the list values on the screen are data read through the P3 parameter and reference-data contracts, never code | DP-06; DP-07; Principle 1 |
| BR14 | Topic names follow `rwb.<short>.events.v1` and every service signs in with its own login; there is no shared login and no legacy topic prefix; the rwb-case login is the DP-02 login, named from RWB-PLT-DB when it is issued, and holds SELECT, INSERT and UPDATE on schema rwb_case only | DP-14; DP-02; Arch v5 slide 41 |
| BR15 | Each service migrates its own schema on its own Flyway sequence; the suite owns no schema and runs no migration | DP-15; ADR-021 |
| BR16 | A section that fails shows its own message and the rest of the case shows; a failure is never turned into a blank screen and never into a pass | SCR-03 Error; MSG-P3-023 |
| BR17 | No personal data in the suite's fixtures, events, logs or report: account keys, person keys, case numbers, document IDs, field IDs and business dates only, and the clear contact value of AC16 is read from the owner inside the run only | Guardrail of RWB-E1-023; Arch v5 slide 42 notes |
| BR18 | No service schema is opened by the suite and no published service contract is faked; a run that needs either fails the preflight | DP-01; section 17 |

### 9. State transitions

None. This story changes no case status and no record; it reads the case and shows its status.

The states the run observes across the services:

| Item | States |
|---|---|
| Screen section | Loading (skeleton rows), Shown with its business date, Stale (MSG-P1-001 above the section), Section message (MSG-P3-023 or MSG-P3-024) |
| Case status as read | "IN_PROGRESS", "ON_HOLD" with the deviation and the prescription date from the S8 contract |
| Access record | Written (AC-READ with the field IDs and masked flags), Refused (no data returned, MSG-P7-003) |
| Masking position of a field | Clear (the rule in force allows the role), Masked (the masked field of the owner) |
| Suite run | Not started, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixture pack, the batch-state control, the probes and the evidence report |
| Case owner (RW-CASEOWN) | Opens the cases in scope Own with Case record R; read only |
| Phone collector (RW-PHONECOL) | Opens the cases in scope Own with the masking of the rule in force; read only |
| Reference-data administrator (RW-REFADM) | Holds no Case record right; refused at the first owner call |
| Service owner of rwb-case | Owns the case reads, the section composition, the scope check and the refusal path |
| Service owner of rwb-source-data | Owns the ACE facts, the freshness stamp of each data product, the interaction ledger and the reconciliation that lists a missing key |
| Service owner of rwb-document | Owns the document list of a case and its timeout behaviour |
| Service owner of rwb-access | Owns the authorise answer, the masking rules, the access log and the AC-READ record |
| Service owner of rwb-deviation | Owns the deviation of a case and its prescription date |
| Data steward | Receives the REC-05 list of a key with no view row and decides the data correction |
| No role | Reads a service schema, opens a view directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-008, DF-CAS-009, DF-CAS-010, DF-CAS-013 | recovery_case | case_no, product_group, status, stage_code, route_code, owner_user_id, queue_id, entry_date | Read through `GET /api/recovery/case/v1/cases/{caseId}` |
| DF-CAS-017, DF-CAS-019, DF-CAS-020 | recovery_case | prescription_date, deviation_open, legal_hold | Read through the P3 contract; the deviation itself through the S8 contract |
| DF-CAS-026, DF-CAS-027 | case_account | account_key, is_primary | Read through `GET /api/recovery/case/v1/cases/{caseId}/accounts` |
| DF-CAS-032, DF-CAS-033 | case_party | person_key, party_role | Read through `GET /api/recovery/case/v1/cases/{caseId}/parties` |
| DF-ACE-001, DF-ACE-002, DF-ACE-018, DF-ACE-020, DF-ACE-036 | v_ace_account | account_key, account_code, days_past_due, total_balance, data_as_of | Synthetic value only, seeded through the P1 data set; read through the P1 contract |
| DF-ACE-055, DF-ACE-057, DF-ACE-058, DF-ACE-059, DF-ACE-068 | v_ace_customer | cif_no, first_name, last_name, date_of_birth, category | Synthetic value only, seeded through the P1 data set; masked by role |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read through the P1 contract; the only identity form shown |
| DF-ACE-074 | v_ace_customer | id_no_last4 | Read through the P1 contract, only with the personal-data permission |
| DF-ACE-075, DF-ACE-076, DF-ACE-077, DF-ACE-078, DF-ACE-079, DF-ACE-080 | v_ace_contact | contact_type, contact_key, person_key, contact_value, contact_value_masked, usage_code | Synthetic value only, seeded through the P1 data set; the clear value only under the masking rule of AC16 |
| DF-ACE-108, DF-ACE-111, DF-ACE-112, DF-ACE-114, DF-ACE-116, DF-ACE-117, DF-ACE-120 | v_ace_efs_action | efs_record_key, action_code, action_code_name, contact_at, comments, is_call, promise_status | Read through the P1 contract; the EFS half of the contact history |
| DF-ACE-178, DF-ACE-179, DF-ACE-182 | v_ace_batch_status | source_system, business_date, status | Read only through the P1 freshness contract (`status` LOADED or STALE); never opened by the suite |
| DF-INT-004, DF-INT-005, DF-INT-008, DF-INT-013 | interaction | occurred_at (wire `occurredAt`), channel, contact_result (wire `contactResult`), source_system (wire `sourceSystem`) | Appended by the fixture and read through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`; the ledger is P1's (DP-18) |
| DF-DOC-004, DF-DOC-005, DF-DOC-011 | document | document_type, source, doc_version | Read through `GET /api/recovery/document/v1/cases/{caseId}/documents` |
| DF-WRK-002, DF-WRK-003 | queue | queue_code, queue_name | Read through the P3 contract |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and are copied unchanged; DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v7. The suite owns no field and no table: every row of this table is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract, and no production value is used. The criteria and the test data read no `recovery.v_ace_*` view; each DF-ACE-* value is read through the P1 contract or seeded through the P1 data set. The masking contract of rwb-access is keyed by view field ID, with a masked flag and the source column per field, and rwb-case sends the field list it read (RWB-P4-E1039-CON).

The exact fixture composition - the row counts of the synthetic set, the document set behind the 50 documents and the keys of the ledger entries - is Not specified in the source documents (GAP-0348; ASM-0442). The fixture is the W1J01 data set, it is synthetic, and its keys are the ones the criteria name.

The `{caseId}` of every P1 call is the uuid of the case; RW-2026-000701 is display text and the opaque part of the ledger business key, and the fixture declares one synthetic uuid for the case. A `caseId` that is not a uuid answers 400 (MSG-GEN-001).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved P2 names - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are unused, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Header of the case: case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation and hold flags; the case entries of the contact history | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | Accounts section: `account_key`, `is_primary` and the account facts the owner reads from P1 by business key; AC2, AC11, AC12 | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | Parties section: `person_key`, `party_role` and the contacts by role; AC3 | 2 s |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (rwb-source-data.yaml 5.1.0, `InteractionPage`) | The contact history with `occurredAt`, `channel`, `contactResult` and `sourceSystem`; AC17 | 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Documents section and its section message when the owner does not answer; AC19 | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | `DataProductFreshness` per product: `businessDate` (null when never stamped), `status` LOADED or STALE, `staleSince`; the business date of every section and the stale banner; AC4, AC11, AC14, AC31 | 2 s |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Fixture only: appends the synthetic ledger entries, header `Idempotency-Key`; 201 for a new entry, 200 for a repeated business key | 2 s |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data (published by RWB-P1-E1011-CON) | The REC-05 result that lists A-7010; AC12 | 2 s |
| GET | `/api/recovery/deviation/v1/deviations?caseId={caseId}` | S8 rwb-deviation | The deviation and the prescription date behind the header and the on-hold banner; AC18 | 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Case record R and the scope at the first owner call, and the refusal of a role without the right; AC20 | 2 s |
| GET | `/api/recovery/access/v1/me/permissions` | P4 rwb-access | The masking position of the caller's role for the fields of the view; AC16 | 2 s |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | The one AC-READ record of the open with the field IDs and their masked flags; AC15 | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget behind gateway-bff; the suite calls no service through another service. The deviation read follows Arch v5 slide 15 (`GET /deviations`) and the S8 base of slide 41, because the ownership map carries only the POST and PATCH rows for the resource (GAP-0348; ASM-0442). The operations are built against the /v1 base (DP-13); the exact contract file version is Not specified in the source documents (DOR-RWB-ITG-E1023-ITG-23).

#### 12.3 Events published

None. The suite publishes no business event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | No late event exists for ALS and the business date while DP01 reads LOADED, so the banner of AC4 and the stamp of AC14 agree; published at 05:30 per source system and business date, record key `{sourceSystem}:{businessDate}`, payload `sourceSystem`, `businessDate`, `status`, `completedAt` (nullable); CloudEvents 1.0, no personal data field |

The suite asserts no other event: every other fact it proves is a synchronous answer of an owner's contract or a record of the P4 access log, and the events of the same behaviour are asserted by the owning service stories RWB-P3-E1023-APP, RWB-P5-E1024-APP and RWB-S8-E1023-APP.

#### 12.5 Workflows and activities

None. The view is a REST composition and this story starts no workflow, observes no workflow and asserts no activity; the case workflow of rwb-case is not on the read path of SCR-03.

#### 12.6 Schedules

None. The suite starts no schedule and moves no clock.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). Every fact it asserts is read through a contract of 12.2 or 12.4.

#### 12.8 Contract fakes

None for a service contract. The only stubs are external to the nineteen services:

| Stub | Purpose |
|---|---|
| Synthetic party, account and contact fixture (RWB-ITG-W1J01-ITG) | Stands in for the ACE ingestion and the ACE rows behind the P1 contract, outside the nineteen services |
| Mock Entra sign-in | Gives the run its synthetic test identities U-81, U-82 and RW-REFADM, as the platform demo sign-in does |

No published service contract is faked: the run needs the real P1, P3, P4, P5 and S8 services on their published contracts, and a run that needs a fake for any of them fails the preflight. No contract fake library version is recorded as published, and none is named for rwb-access, rwb-case, rwb-deviation, rwb-document or rwb-source-data (DOR-RWB-ITG-E1023-ITG-22).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 10 | Ten reads and one command-free path of section 12.2; one hop each, 2 s budget, breaker per owner (DP-11, DP-13, DP-19) |
| Kafka | None | 1 event type | `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1`; CloudEvents 1.0 (DP-14) |
| Temporal | None | None | No workflow and no activity in this story |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture pack for the synthetic case, accounts, parties, contacts, documents, ledger entries, batch rows and masking rules; a batch-state control; eight probes; a composed-route assertion; and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts and the fixture set, run order, report and exit code |
| FixtureDriver | Test harness | Seeds and removes the synthetic case RW-2026-000701, A-7001, A-7010, P-7001, the 50 documents, the 120 ledger entries, the batch rows for 2026-12-02 and 2026-12-03 and the masking rules |
| CompositeRouteProbe | Test harness | Opens SCR-03 through gateway-bff, records the call set and the elapsed time of each owner call, and proves the parallel composition and the one-hop rule of AC13 |
| AccountsProbe | Test harness | The Accounts section of AC2, AC11 and AC12 on A-7001 and A-7010 through the P1 and P3 contracts |
| FreshnessProbe | Test harness | The business date of every section from the P1 freshness read, the stale banner of AC4, the absent Workbench load date and the AceDataLate agreement of AC14 |
| MissingKeyProbe | Test harness | Takes A-7010 out of the view and reads the P1 reconciliation output for the REC-05 list of AC12 |
| MaskingProbe | Test harness | The P4 masking position and the clear and masked outcomes of AC16, including the assertion that the clear value never leaves the owner |
| AccessLogProbe | Test harness | The one AC-READ record of AC15 and the refused path, and the refusal of AC20 at the first owner call |
| ContactHistoryProbe | Test harness | The merged time order of AC17, the source system on each row and the absence of a duplicate |
| DeviationProbe | Test harness | The header flags and the on-hold banner of AC18 from the S8 contract, and the absence of a copy in the P3 response |
| DocumentHubProbe | Test harness | The timeout, the breaker and the section message of AC19 |
| ReportWriter | Test harness | One row per test case with its evidence and elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object, and it holds no client for a service schema.

**Configuration and reference data**

- The SIT endpoints of P1, P3, P4, P5 and S8 behind gateway-bff, the topic name, the schema-registry address and the namespace `rwb-recovery`, all as configuration.
- The synthetic keys and values of the W1J01 set, the business dates 2026-12-02 and 2026-12-03, and the case number RW-2026-000701.
- The section budget, the labels and the list values read through the P3 parameter and reference-data contracts (DP-06, DP-07), including LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE and LOV-PARTY-ROLE; the legacy `caserecord.section.timeout.ms` gives way to the 2 s client budget of DP-11 and is read, not written, where the screen still needs it.
- The masking rules of RW-CASEOWN and RW-PHONECOL, read through the P4 contract and never written in the suite code.
- The 2 s client budget, the retry of the suite and the poll interval.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
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

DP-01, DP-05 and DP-18 carry the source facts and the ledger behind the owners; DP-08 carries the authorise answer and the masking position; DP-11 and DP-19 carry the composed route and the 2 s budget; DP-13 and DP-14 carry the base and the topic names; DP-03 applies to the refused read, whose refusal is recorded by the owner in its local decision record and collected in the central ledger, and the suite asserts it through the P4 access log rather than through a table; DP-06 and DP-07 carry the section budget, the labels and the list values; DP-02 and DP-15 keep one login and one migration sequence per service. The H and C entries of the table belong to the service, platform and operations stories that own them: this ITG story carries no H, C or X entry of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the seven services whose behaviour the run exercises.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Case set | Case RW-2026-000701 with status "IN_PROGRESS", queue "TDR-BKK-CO", owner U-81, entry date 2026-11-30 and 2 accounts, seeded through the W1J01 set | AC13 to AC20 |
| Account facts | A-7001 at 97 days past due with THB 206,175.00 and data as of 2026-12-02; the 2026-12-03 batch at THB 210,000.00 | AC11, AC14 |
| Missing key | The link to A-7010 with no row in the account view | AC12 |
| Party and contact facts | P-7001 with the masked identity XXXXXXXXX4821 and one mobile, its clear form 0812345678 and its masked form XXXXXX5678 | AC16 |
| Documents and ledger | 50 documents on the case and 120 ledger entries with their source systems | AC13, AC17 |
| Batch state | The 2026-12-02 rows complete for ALS, SCBPDM and EFS, and no COMPLETED ALS row for 2026-12-03 | AC4, AC11, AC14 |
| Deviation | Deviation X1 on the case with prescription date 2028-03-15 | AC18 |
| Masking rules | The rule set of RW-CASEOWN and RW-PHONECOL, with and without the clear position for DF-ACE-078 | AC15, AC16 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the topic and the namespace, with the contract preflight that fails on any drift.
2. Build FixtureDriver and the fixture pack; assert that the case, its accounts, its parties, its documents and its ledger entries read back through the owners before any assertion is made.
3. Build CompositeRouteProbe and prove the parallel composition, the one-hop rule and the 2 s budget of AC13 from the recorded call set.
4. Build AccountsProbe and FreshnessProbe; assert A-7001 at 97 days past due with THB 206,175.00 and business date 2026-12-02, the absent Workbench load date, the stale banner of AC4 after 08:00 on 2026-12-04 and the never-stamped answer of AC31.
5. Build the AC11 step: move the batch, re-read the case, assert THB 210,000.00 with business date 2026-12-03 and prove that no response of the run returns the earlier balance.
6. Build MissingKeyProbe for AC12 and read `GET /admin/reconciliation/results` for the REC-05 list.
7. Build MaskingProbe and AccessLogProbe; assert the clear and masked outcomes of AC16, the one AC-READ record of AC15 and the refused read of the same scenario, and the refusal of AC20 at the first owner call.
8. Build ContactHistoryProbe and DeviationProbe; assert the merged time order of AC17 and the S8 flags of AC18 with no copy in the P3 response.
9. Build DocumentHubProbe for AC19, ReportWriter and the cleanup; run the whole suite twice to prove that a repeated open adds no second AC-READ record and no duplicate entry.

**Done when.** The thirteen test cases of section 16 pass on the real services in SIT, the three criteria this story owns (AC4, AC11, AC12) and the eight cross-service criteria (AC13 to AC20) are signed off against the contracts, the access log holds exactly one AC-READ record per open of the run, no service table and no view was opened, the synthetic set is removed, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A section's data product has status STALE | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | Case on hold | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-024 | A section has nothing to show | Nothing is recorded in {section} yet. |
| MSG-P3-023 | A section cannot be shown | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The seven texts are copied unchanged from RWB-E1-023 and this story adds no message ID. The messages are rendered by the owning service and passed through gateway-bff unchanged, so the suite asserts the ID and the text on the composed response.

### 15. Screens and states

SCR-03 Case record, composed by gateway-bff (DP-19) from the P3, P1, P5 and S8 reads. Empty: MSG-P3-024 in the Documents and Contact history sections (AC21). Loading: skeleton rows per section. Read only: fields without edit controls; the header and the five sections, each with the business date of its own data product read from the P1 freshness contract. On hold: the banner with the deviation and the prescription date from the S8 contract. Stale input: MSG-P1-001 above the section whose data product is not complete. Error: MSG-P3-023 in the section that failed, with the breaker of that owner open for the next call; when rwb-case refuses the case read, MSG-P7-003 and no case data (AC23). The screen shows no Workbench load, job or file status, and no section shows a copy of a record it does not own. No access: the view is refused with MSG-P4-002 and no case data shows (AC20).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-11-ITG | Access, AC20 | Integration | RW-REFADM calls the case read and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-01-ITG | run by RWB-P3-E1023-APP for AC1; AC13, AC14, BR7 | Integration | Case with 50 documents and 120 EFS entries; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-02-ITG | run by RWB-P3-E1023-APP for AC2; AC13, AC14, BR1 | Integration | rwb-source-data account read for A-7001 at 97 days past due, business date 2026-12-02; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-03-ITG | run by RWB-P3-E1023-APP for AC3; AC17, BR8 | Integration | rwb-source-data customer read P-7001 with category RETAIL, contact read mobile, EFS entries; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-04-ITG | AC4, BR2 | Integration | No COMPLETED ALS batch for 2026-12-03, view opened after 08:00 on 2026-12-04, P1 freshness read STALE with business date 2026-12-02; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-05-ITG | run by RWB-P3-E1023-APP for AC5; BR5 | Integration | Case of team LIT-BKK, user with scope Own; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-06-ITG | run by RWB-P3-E1023-APP for AC6; AC19 | Integration | Document hub not answering; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-07-ITG | run by RWB-P3-E1023-APP for AC7; AC15, BR4 | Integration | Access event stream rejecting every write; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-08-ITG | run by RWB-P3-E1023-APP for AC8; AC16, BR3 | Integration | Phone collector without the personal-data permission; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-09-ITG | run by RWB-P3-E1023-APP for AC9; AC18 | Integration | Case on hold for X1; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-10-ITG | run by RWB-P3-E1023-APP for AC10 | Integration | Case with no documents and no history; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-12-ITG | AC11, BR8 | Integration | A-7001 balance changed by the 2026-12-03 ALS batch; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-13-ITG | AC12, BR9 | Integration | Case link A-7010 with no rwb-source-data account row; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-14-ITG | AC13 | Integration | Case with 50 documents and 120 contact history entries; gateway-bff composite route with the five owner calls in parallel; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-15-ITG | AC14 | Integration | P1 freshness read with business date 2026-12-02 for "DP01 Account and arrears"; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-32-ITG | AC31 | Integration | No DP05 stamp row; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-16-ITG | AC15 | Integration | U-81 with RW-CASEOWN and Case record R, scope Own; P4 access record write accepted, then refused; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-17-ITG | AC16 | Integration | Phone collector U-82 with the clear masking rule for DF-ACE-078, then the masked rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-18-ITG | AC17 | Integration | P1 ledger entries and P3 case entries of RW-2026-000701, 120 entries; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-19-ITG | AC18 | Integration | Case on hold for deviation X1 with prescription date 2028-03-15 from the S8 contract; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-20-ITG | AC19 | Integration | Document hub not answering within the 2 s budget; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-21-ITG | AC20 | Integration | RW-REFADM without Case record R; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-22-ITG | AC21 | Integration | Case with no documents and no contact history entries; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-23-ITG | AC22 | Integration | Composed route not yet settled for RW-2026-000701; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-24-ITG | AC23 | Integration | rwb-case answers status 503 on the case read; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-25-ITG | AC24, X2 | Integration | Case RW-2026-000701 outside the scope of U-81 with RW-CASEOWN and Case record R; the P4 scope answer refuses it; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-26-ITG | AC25, BR6 | Integration | U-81 opens case RW-2026-000701; no edit control in any section and no write request for the case; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-27-ITG | AC26, BR13 | Integration | Published P3 parameter and reference-data contracts: section labels, section timeout and the six lists; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-28-ITG | AC27, BR14 | Integration | Topic names rwb.<short>.events.v1 and the own login of each wave 1 service; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-29-ITG | AC28, BR15 | Integration | Run start: no migration run and no schema owned by the suite; the Flyway sequence of each wave 1 service; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-30-ITG | AC29, BR17 | Integration | Fixtures, events, logs and report of the run; end-to-end: real services on the wave 1 contracts |
| TC-E1-023-31-ITG | AC30, BR18 | Integration | A consumed service contract that drifts from its published contract, checked at preflight; end-to-end: real services on the wave 1 contracts |

The -ITG copy of each row also carries the cross-service step of the new criteria: AC13 and AC14 on TC-E1-023-01-ITG and TC-E1-023-02-ITG, AC15 on TC-E1-023-07-ITG, AC16 on TC-E1-023-08-ITG, AC17 on TC-E1-023-03-ITG, AC18 on TC-E1-023-09-ITG, AC19 on TC-E1-023-06-ITG and AC20 on TC-E1-023-11-ITG. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration and the legacy Access level becomes Integration.

TC-E1-023-04-ITG, TC-E1-023-12-ITG and TC-E1-023-13-ITG are the three copies this story signs off, one for AC4, AC11 and AC12. The other ten are regression evidence for RWB-P3-E1023-APP, which owns their criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed.

### 17. Guardrails

- No copy of an ACE record in any Workbench table, cache or screen state: the account, customer, contact and collection facts are read by the owner on every open and are held nowhere (DP-01, DP-05).
- No clear personal value in a cache or a log: the identity number is shown only in its masked form from the owner, and the clear contact value of AC16 exists inside the run only and is asserted absent from every response, cache and log.
- ACE data only through the owner's contract or the `v_ace_*` views, and those views only through rwb-source-data; the suite ships with no client for a service schema and no client for a view.
- The identity number is masked in the view itself, so no role and no path can return it in clear.
- No business value in code: the section budget, the labels, the list values and the masking rules are read through the P3 and P4 contracts.
- No personal data in the suite's fixtures, topic payloads, logs or report: keys, case numbers, document IDs, field IDs and business dates only.
- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every account, person, contact, document and batch row, and the run refuses any environment that is not SIT.
- One hop and a 2 s budget on every call, with a breaker per owner and no service called through another service (ADR-020; DP-11; DP-19).
- Clean-up in the same run: the synthetic set and the moved batch state are removed or restored, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-007 | Case record view with account, arrears, owner, queue, stage, status, contact history and documents | `GET /api/recovery/case/v1/cases/{caseId}`, `.../accounts`, `.../parties`, `GET /api/recovery/document/v1/cases/{caseId}/documents`, `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | TC-E1-023-01-ITG, TC-E1-023-02-ITG, TC-E1-023-03-ITG, TC-E1-023-06-ITG, TC-E1-023-09-ITG, TC-E1-023-10-ITG |
| REQ-RDF-009 | Every data product carries a freshness stamp | `GET /api/recovery/source-data/v1/data-products/freshness`, `rwb.source-data.AceDataLate.v1` | TC-E1-023-02-ITG, TC-E1-023-04-ITG; TC-E1-023-32-ITG (AC31) |
| REQ-ACA-005 | Personal data masked by role | `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions`, the masked flags of the AC-READ record | TC-E1-023-07-ITG, TC-E1-023-08-ITG |
| REQ-ACA-006 | Every read of the case store written to the access log | The AC-READ record in `GET /api/recovery/access/v1/admin/access-log`, MSG-P7-003 | TC-E1-023-05-ITG, TC-E1-023-08-ITG |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow | `POST /api/recovery/access/v1/authorise` with the scope, MSG-P4-002, MSG-P4-003 | TC-E1-023-05-ITG, TC-E1-023-11-ITG |
| D-RCV-35 U1 and U4 | The view reads account, customer, contact and collections history only through the owner, by business key, and copies nothing | The P1 contract and the P1 freshness read, the P1 reconciliation output of REC-05 | TC-E1-023-12-ITG, TC-E1-023-13-ITG |
| ADR-010 | The ACE boundary holds: only rwb-source-data reads the views | `GET /api/recovery/source-data/v1/data-products/freshness`, the P1 account and party facts | TC-E1-023-02-ITG, TC-E1-023-04-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The ten operations of 12.2 and the preflight contract test | TC-E1-023-01-ITG, TC-E1-023-11-ITG |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| DP-01 and DP-05 | Owner's schema and the ACE access through the owner | The P1 contract, the freshness read, the absent service-schema client | TC-E1-023-02-ITG, TC-E1-023-12-ITG |
| DP-06 and DP-07 | Parameters contract and reference-data contract of rwb-case | The section budget, the labels and the list values of the screen | TC-E1-023-01-ITG, TC-E1-023-03-ITG |
| DP-08 | Authorise contract of rwb-access and the guard library | `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions`, the access log | TC-E1-023-07-ITG, TC-E1-023-08-ITG, TC-E1-023-11-ITG |
| DP-11 and DP-19 | gateway-bff composite route with one hop and a 2 s budget | The composed route of AC13 and its recorded call set | TC-E1-023-01-ITG, TC-E1-023-06-ITG |
| DP-13 and DP-14 | The base and the topic naming of the owner | `/api/recovery/<short>/v1` on every operation of 12.2, `rwb.source-data.events.v1` | TC-E1-023-04-ITG, TC-E1-023-11-ITG |
| DP-18 | The interaction ledger is owned by rwb-source-data | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | TC-E1-023-03-ITG |
| D-RCV-60 GAP-0348; ASM-0442 | The S8 read path and the S8 wave, and the fixture composition of the run | `GET /api/recovery/deviation/v1/deviations?caseId={caseId}`, the fixture pack of section 13 | TC-E1-023-09-ITG |
| RWB-E1-023 (legacy story) | Case record view v1, read only: AC4, AC11, AC12 | The ten operations, the one event and the composed route of section 12 | The three signed-off copies of section 16 |
| RWB-P3-E1023-APP (component copy) | The case record view in rwb-case, owning AC1, AC2, AC3, AC5 to AC10 | The P3 case reads, the section composition and the refusal path | The ten regression copies of section 16 |

### 19. Out of scope

- The application builds this run depends on: RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P1-E1066-APP, RWB-P5-E1024-APP, RWB-P4-E1039-APP, RWB-P1-E1068-APP, RWB-P1-E1069-APP, RWB-P3-E1023-APP, RWB-P4-E1023-APP and RWB-S8-E1023-APP.
- The contract story of the legacy key in rwb-case, and the database, operations and infrastructure stories of the legacy key.
- The criteria this story does not own: AC1, AC2, AC3, AC5, AC6, AC7, AC8, AC9 and AC10, which belong to RWB-P3-E1023-APP.
- The history timeline on the case view (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Writing a Workbench entry to the interaction ledger (RWB-E1-066, RWB-E1-067).
- The build of the harness RWB-ITG-W1J01-ITG itself.
- The non-functional epic RWB-ITG-NFR.

### Remaining delivery steps

- rwb-source-data contracts (RWB-P1-E1015-CON, RWB-P1-E1011-CON, ledger contract) Done and published: owner rwb-source-data service owner.
- rwb-case key-list read path for REC-05 fixed (GAP-3273): owner rwb-case service owner.
- Test Cases and RTM rows for AC4, AC12, AC17 and AC31: owner QA.
- Synthetic case uuid, ledger entries and batch rows loaded in SIT: owner QA integration engineer.
- Size, two-week fit and epic design sign-off: owner squad and Solution architect.
