# RWB-P1-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P1-L |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1018-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1018-CON; RWB-P1-E1018-CON (rwb-source-data contract story) |
| Contract version | Not specified in the source documents (DOR-RWB-P1-E1018-APP-23); base path /api/recovery/source-data/v1 |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL16 (ASM-1094, ASM-5264); DL43 (ASM-0193, ASM-0737, ASM-0748, ASM-0816) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-018 for rwb-source-data. The in-process `AceSourceQuery` reads of the monolith — `accountsAtOrAbove(daysPastDue, businessDate)`, `relationsFor(accountKey)` and `customer(personKey)` — become one REST read of this service, `GET /api/recovery/source-data/v1/entry-candidates` on base `/api/recovery/source-data/v1` (DP-05, DP-11, DP-13), which returns the entry candidates for a business date and a threshold together with the exclusion facts of the four owners joined by business key, behind the ALS batch gate read from `v_ace_batch_status` (DP-05), and writes the two extension facts of case creation 1:1 by business key in schema `rwb_source_data` (DP-01, DP-15). The case ID, the case record, the ENTRY and EXCLUSION packages and the entry decision stay with rwb-case and rwb-decision, and `AceDataReady` and `AceDataLate` stay with RWB-P1-E1015-APP. Gaps GAP-0571 to GAP-0576 and their assumptions are carried in sections 3, 4, 12, 13 and 16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 26 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case-creation job of rwb-case (SY-CASEWF)**, I want **one read of rwb-source-data for a business date and a threshold that returns every account in the ACE account view at or above that threshold with its exclusion facts, each fact read from the owner of the field, behind a gate that answers nothing until the ALS batch for that date is complete**, so that **the entry decision is taken on one set of ACE facts that has one owner, one date and no copy, and no case is created from a day whose ACE batch has not arrived**.

This is the source-fact slice of legacy RWB-E1-018. It delivers five things and nothing else:

- **the entry-candidate read** on `/api/recovery/source-data/v1`: `GET /entry-candidates?businessDate=&threshold=`, one row per account in `v_ace_account` whose `days_past_due` is at or above the threshold and whose `data_as_of` is the business date, carrying `account_key`, `account_code`, `product_group` (the ACE `product_category`), `days_past_due`, `total_balance`, `contract_no`, `data_as_of`, `tdr_flag`, `deceased_flag` (from `v_ace_customer`), `dispute_open` (from `account_ext`), `deceased_override`, `bankruptcy` and `fraud_flag` (from `party_ext`), and the BORROWER `person_key` resolved through `v_ace_ca_relation` (DP-05, DP-11, DP-13);
- **the exclusion facts joined by business key only**, each value read in the table or view of its owner — `v_ace_account`, `v_ace_customer`, `account_ext`, `party_ext` — and never copied into another table (DP-01, DP-05);
- **the extension part of case creation**: `account_ext.dispute_open` and the `party_ext` flags — `vulnerable` with `deceased_override`, `bankruptcy` and `fraud_flag` — written 1:1 by business key, with no `id`, no foreign key and no copy of an ACE column (FSD AC-ALT-P1-001-03; DP-01, DP-15);
- **the ALS batch gate**: no fact for a business date whose ALS batch is not COMPLETE in `v_ace_batch_status`, answered with MSG-P1-001 and the STALE stamp of DP01 (DP-05);
- **the REC-05 listing of a key with no view row**: the key is listed for the data steward and the ACE team and is never invented and never turned into a case.

It does **not** claim the other criteria of the legacy key. It issues and formats no case ID and draws no sequence, writes no `recovery_case`, `case_account` or `case_party` row, and evaluates no ENTRY or EXCLUSION package: the packages belong to rwb-decision and the entry decision, the case row, the links, the primary account and the exclusion record belong to rwb-case (legacy AC1, AC2, AC3, AC4, AC6, AC8, AC10, AC11, AC12, AC15). It serves no case attribute of any kind: case number, status, stage, owner, queue and exposure band are rwb-case's, and this story has no field for them. Legacy AC5 (the state model as data) is owned by the rwb-case slice, legacy AC7 (the threshold boundary) and AC12 (two products, two cases) are proved here only for the facts, legacy AC9 (no cases before the batch is complete) is proved here as the gate of the read, legacy AC13 (a key with no view row) is proved here as the listing, and legacy AC14 (a refused read) belongs to the rwb-access slice and to RWB-ITG-E1018-ITG.

### 2. Business rationale

Every account at 90 days past due or more has to become a case the morning the ACE batch lands, and an account that is deceased, in bankruptcy, under fraud investigation, on an active restructure plan or in an open dispute must not. Today that decision is taken inside one monolith that holds the account copy, the customer copy and the exclusion flags in the same schema, so nobody can say which copy a given answer came from. Under D-RCV-35 the Workbench holds no source copy at all: ACE ingests ALS and SCBPDM, and the Workbench reads them through the 30 `recovery.v_ace_*` views. One read that returns the facts and one owner for each fact is what makes the entry decision auditable; REQ-CWC-001, REQ-CWC-004 and REQ-CHO-004 are answered by it.

**Why the facts are a service of their own.** The views may be read by one login only — `rwb_source_data` (Architecture v5 slides 11 and 29; TSD P1 v3 T6.3) — and no other service may read a `v_ace_*` view at all (Architecture v5 slide 11, the "SQL view" column: "Any other service reading the views" is in the *Never* row). So the facts cannot be assembled by the case service, and a read of rwb-source-data is the only way the case creation job can see an account, a customer and a relation at all. Keeping that read on the owner side also keeps the four extension tables honest: they are P1's tables (ownership map; TSD P1 v3 T3.5), they are 1:1 with an ACE record, and only the service that owns them may write them.

**Why the read is not the decision.** The ENTRY and EXCLUSION packages are authored by RW-COE, approved by RW-RISK and evaluated by rwb-decision (Temporal and Drools design, slide 15; the package in force check, MSG-P3-027). Handing the case creation job a set of facts, and leaving the threshold, the package and the reason code on the decision side, is what keeps a rule change free of a release: this service returns the same row whether the threshold is 90 or 120, and it returns `dispute_open` whether or not OPEN_DISPUTE is in force. The threshold therefore arrives in the request, not in this service's code, and this story reads no parameter catalog (DP-06 applied as a prohibition).

**Why the gate is here.** CTL-02 and legacy BR7 say that no case is created from an incomplete day, and the record of completeness is the ACE batch record, read through `v_ace_batch_status` — which only this service may read. The gate is therefore on the read, not on the job: a job that asks for a date whose ALS batch is not complete receives MSG-P1-001 and no facts, and cannot create a case by accident. `v_ace_batch_status` is a Section B view of RWB-ACE-001 (DL43), so the gate has a defined behaviour before the view lands (GAP-0574), and the stamp that names DP01 STALE on a late batch is RWB-P1-E1015-APP's, not this story's.

### 3. Preconditions

- The published baseline of rwb-source-data is in place: schema `rwb_source_data` with the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`, their business keys, their seven standard record columns and their dictionary rows (RWB-P1-E1001-APP; TSD P1 v3 T3.0 and T3.5). This story takes **no build dependency** on that story: the baseline, the view contract and the RWB-P3-E1018-CON fake are what Wave 1 is cut against, and this story builds against the baseline from Day 1 (a Day-1 APP story with no H dependency, Template and Rules §R5.7 rules 2 and 8).
- The view contract is published: the Section A views `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`, and the Section B view `v_ace_batch_status` behind its flag, as defined in the ACE Source Views v1 definitions and the service's `recovery_views.sql` (RWB-P1-E1069-APP; DP-05). `v_ace_batch_status` lands with RWB-ACE-001, and what the gate answers before the view lands is Not specified in the source documents (GAP-0574; ASM-0816).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; the sequence is part of the service template baseline).
- RWB-P3-E1018-CON is published with its fake: it fixes the shared vocabulary of the two sides — `account_key` and `person_key` as the business keys, the ISO business date, the RFC 9457 problem envelope and the error codes — so the entry-candidate resource and the case contract cannot drift apart while rwb-case is being built (C RWB-P3-E1018-CON; DP-11).
- The login `rwb_source_data` holds SELECT on the 30 `recovery.v_ace_*` views, USAGE on schema `rwb_source_data`, and no SELECT, INSERT, UPDATE or DELETE on any `public` table and no grant on any other `rwb_*` schema (DP-02; Architecture v5 slides 11 and 29; TSD P1 v3 T6.3; FSD AC-EXC-P1-001-05).
- The parameter `case.entry.dpd` = 90 is in force and is read by the caller, rwb-case, through its own parameter contract (DL16; legacy §3). This story reads no parameter: the threshold arrives in the query and is validated against its bounds only (DP-06).
- The callers are known: the read is called by the service identity of rwb-case's case creation step (SY-CASEWF, a workload identity token), and the extension writes are called by the exclusion screen of the rwb-case slice through gateway-bff with the user's token (DP-19).
- The shape of the read — its resource name, query parameters, response entity, field names, paging, error status set and read grant — is a target choice and not a legacy value, because the legacy read was an in-process Java interface with no path and no status code, and no contract story of its own exists for this key (GAP-0571; ASM-0813).
- Which service writes the two extension facts and under which right is Not specified in the source documents (GAP-0573; ASM-0815); this story writes them, because rwb-source-data is the owner of the two tables and the only login that may write its schema.

### 4. Flow

1. The case creation step of rwb-case calls `GET /api/recovery/source-data/v1/entry-candidates?businessDate=2026-12-01&threshold=90` with its workload identity token: one hop, 2 s budget, breaker on the caller side (DP-11, DP-13).
2. `EntryCandidateController` validates the query against the published schema: `businessDate` as an ISO date, `threshold` as an integer inside its bounds, and the page and size parameters if they are given (12.1; GAP-0571).
3. `BatchStatusReader` reads `v_ace_batch_status` for `source_system` = ALS and the requested business date: `status`, `is_complete` and `completed_at` (DF-ACE-178, DF-ACE-179, DF-ACE-181, DF-ACE-182, DF-ACE-186; DP-05).
4. When the ALS row is absent, not COMPLETE, or `is_complete` is false, the call is refused with 409 and MSG-P1-001 for "DP01 Account and arrears" with the last complete business date, and the response holds no candidate and no break row (AC4). The gate is read from `v_ace_batch_status` only and is never inferred from `data_as_of`, a row count or a file (FSD BR-P1-014-2).
5. `EntryCandidateService` reads `v_ace_account` once for the business date and the threshold: `days_past_due` at or above the threshold and `data_as_of` equal to the business date, returning `account_key`, `account_code`, `contract_no`, `product_category`, `days_past_due`, `total_balance`, `tdr_flag` and `data_as_of` (DF-ACE-001, 002, 006, 010, 018, 020, 031, 036). One statement for the whole date, never one call per account: the read is one operation for the date, paged by the page and size parameters, with the default and maximum page size fixed in the published contract (DP-11; GAP-0572; ASM-0814; ASM-B-P1-07-E1018-2). The product group is the `product_category` value read, returned as read: unvalidated and unmapped, so a value outside LOV-PRODUCT is never coerced, dropped or defaulted. Any mapping or validation is the consumer's, through the rwb-case reference-data contract (ASM-B-P1-07-E1018-6).
6. For each candidate it resolves the borrower through `v_ace_ca_relation` on `account_key` with `relation_type` "BORROWER", taking `person_key` (DF-ACE-084, 085, 086). An account with a borrower key and a co-borrower key yields the borrower key only.
7. It reads `v_ace_customer` once for the set of borrower keys and takes `deceased_flag` (DF-ACE-056, DF-ACE-061); a borrower key with no customer row is not invented.
8. It reads the extension facts by business key: `account_ext.dispute_open` for the candidate `account_key`, and `party_ext.deceased_override`, `bankruptcy` and `fraud_flag` for the borrower `person_key` (DF-EXT-027, 028, 001, 003, 004, 005). A missing extension row is returned as an absent flag and is never defaulted to false, and the read never writes a row to answer (AC2).
9. Keys that do not resolve are separated from the candidates: an `account_key` with no `v_ace_account` row for the date, or a borrower `person_key` with no `v_ace_customer` row, goes to the `breaks` of the response with its key type, its key and the view that has no row, for the data steward and the ACE team, and is read again on the next complete batch (AC5; REC-05; GAP-0575).
10. The page is assembled: `businessDate`, `threshold`, `asOf` (the `completed_at` of the ALS row), the page, size and total, the candidate rows and the breaks (12.1). No case attribute is served, stored or counted anywhere in the page (AC6).
11. Separately, when a fraud specialist or a case officer records an exclusion fact on the exclusion screen of the rwb-case slice, the screen calls `PUT /api/recovery/source-data/v1/extension-facts/parties/{personKey}` or `PUT /api/recovery/source-data/v1/extension-facts/accounts/{accountKey}` through gateway-bff; `ExtensionFactService` upserts one row by business key, sets the standard record columns, reads the row back and answers 200 with it. ACE is untouched (AC3; FSD AC-ALT-P1-001-03).
12. A view error or a statement that exceeds the 5 s statement timeout answers 503 with MSG-GEN-006 for "ACE database" and returns no partial page; nothing is cached, so the next call re-reads the view (12.1).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The account is at 89 days past due and the threshold is 90 | No candidate row for that account; the account is read again on the next complete ALS batch | None | AC1 |
| X2 | An exclusion fact has no row in its owner (no `party_ext` row for the borrower) | The field is absent in the candidate row and is named as absent; no row is written to answer the read and nothing is defaulted | None | AC2 |
| X3 | An extension fact is recorded for a key with no view row | The 1:1 row is written by business key and the key is listed by REC-05 on the next read; no ACE record is invented and no case is created from it | None | AC5 |
| X4 | The ALS batch for the business date is not COMPLETE, or `v_ace_batch_status` does not exist yet | 409 with MSG-P1-001; no candidate and no break row; DP01 shows STALE; the call is answered as soon as the batch is complete for that date | MSG-P1-001 | AC4 |
| X5 | An ACE view raises an error or the statement exceeds its timeout | 503 with MSG-GEN-006 naming "ACE database"; no partial page and nothing cached | MSG-GEN-006 | AC7 |
| X6 | The caller is not the case service identity, or the extension write arrives without the screen's right | 403 with the problem envelope and MSG-P4-002; nothing is read or written | MSG-P4-002 | AC6 (the read side; the write side runs in RWB-ITG-E1018-ITG) |
| X7 | A statement reads `public.account` or inserts into `rwb_case.recovery_case` | Refused by the database grant with permission denied; the conformance test fails the build if the grant ever allows it | None | AC6 |

X1, X2 and X3 are the legacy exception paths of RWB-E1-018 that this slice owns (legacy X3, and the fact side of X1 and X9), carried with their values. X4 is legacy X5 and BR7, proved here on the read instead of on JOB-02. X5 and X6 are the paths a cross-service read adds: in the monolith the view was a local query that could not time out and the caller was an in-process class. X7 is the boundary rule of D-RCV-35 (U4; ADR-010) as the database enforces it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published baseline, the view contract and the RWB-P3-E1018-CON fake from Day 1; needs no other story of the wave |
| Negotiable | The internal class split, the query shape, the page size and the break row are the squad's choice behind the contract (§13; GAP-0571); the four views, the two extension tables and their 1:1 keys are fixed |
| Valuable | One read that gives the case creation job the facts of the day with one owner per fact, behind the ACE batch gate |
| Estimable | One controller, one service, one repository over the ACE views, one extension writer and one migration that asserts the keys |
| Small | Fits one sprint with its tests, as the source-fact slice of the legacy key |
| Testable | Every criterion in section 7 is one call of the read or the write with synthetic keys, the ACE view fixture and the case fake |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1

  Background:
    Given the parameter "case.entry.dpd" is 90 and the threshold sent in the request is 90
    Given the business date is 2026-12-01
    Given v_ace_batch_status holds the ALS batch for 2026-12-01 with status "COMPLETED" and is_complete true

  Scenario: AC1 Entry candidates at or above the threshold, one row per account (new, D-RCV-60)
    Given v_ace_account holds account A-5006 at days_past_due 89 and account A-5007 at days_past_due 90 for 2026-12-01, both with no exclusion
    Given v_ace_ca_relation holds person_key P-0101 on account A-5007 as "BORROWER" and v_ace_customer holds P-0101
    Given v_ace_account holds mortgage account A-5011 and hire purchase account A-5012 for borrower P-0103, both at days_past_due 91
    When the case creation job calls GET /api/recovery/source-data/v1/entry-candidates with businessDate 2026-12-01 and threshold 90
    Then the response holds one candidate row for A-5007 and no candidate row for A-5006
    Then the row for A-5007 carries daysPastDue 90, dataAsOf 2026-12-01 and borrower personKey P-0101
    Then the response holds two rows for P-0103, one with productGroup "MORTGAGE" and one with "HIRE_PURCHASE"

  Scenario: AC2 The exclusion facts come from the four owners, each value named (new, D-RCV-60)
    Given v_ace_account holds account A-5002 at days_past_due 92 with tdr_flag true, product_category "HIRE_PURCHASE", contract_no "CN-5002" and total_balance 300,000.00
    Given v_ace_customer holds person_key P-0101 with deceased_flag true and v_ace_ca_relation holds P-0101 on A-5002 as "BORROWER"
    Given account_ext holds account_key A-5002 with dispute_open true
    Given party_ext holds person_key P-0101 with vulnerable false, deceased_override false, bankruptcy true and fraud_flag false
    When the case creation job calls the operation for 2026-12-01 at threshold 90
    Then the row for A-5002 carries tdrFlag true read from v_ace_account, deceasedFlag true read from v_ace_customer, disputeOpen true read from account_ext, and deceasedOverride false, bankruptcy true and fraudFlag false read from party_ext
    Then every value in the row is read from the owner of the field and no ACE column is stored in another table of this service

  Scenario: AC3 An extension row is written 1:1, the ACE record is untouched and no foreign key exists (new, D-RCV-60)
    Given person_key "P0000123" exists in v_ace_customer and has no party_ext row
    Given account_key "A-5005" exists in v_ace_account and has no account_ext row
    When the exclusion screen calls PUT /api/recovery/source-data/v1/extension-facts/parties/P0000123 with fraudFlag true
    Then party_ext holds one row for "P0000123" with fraud_flag true and the seven standard columns
    When the same call is repeated with the same body
    Then party_ext still holds one row for "P0000123"
    When the exclusion screen calls PUT /api/recovery/source-data/v1/extension-facts/accounts/A-5005 with disputeOpen true
    Then account_ext holds one row for "A-5005" with dispute_open true and the seven standard columns
    Then public.customer for "P0000123" and public.account for "A-5005" are unchanged
    Then no foreign key links party_ext or account_ext to a public table, neither table carries an id, and neither carries a copy of an ACE column

  Scenario: AC4 No facts before the ALS batch for the business date is complete (new, D-RCV-60)
    Given v_ace_batch_status shows the ALS batch for 2026-12-02 with status "RUNNING" at the 09:00 cut-off
    When the case creation job calls the operation for 2026-12-02 at threshold 90
    Then the call is refused with status 409 and MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-01
    Then the response holds no candidate row and no break row
    Then no LOADED stamp is written for DP01 for 2026-12-02 and the stamp RWB-P1-E1015-APP holds for that date shows STALE
    When the ALS batch for 2026-12-02 becomes COMPLETE
    Then the same call returns the candidate rows for 2026-12-02

  Scenario: AC5 A key with no view row is listed, never invented (new, D-RCV-60)
    Given v_ace_ca_relation holds person_key P-0105 on account_key A-5013 as "BORROWER" for 2026-12-01
    Given v_ace_account has no row for A-5013 on 2026-12-01 and v_ace_customer has no row for P-0105
    When the case creation job calls the operation for 2026-12-01 at threshold 90
    Then the response holds no candidate row for A-5013
    Then the response lists account_key A-5013 with v_ace_account and person_key P-0105 with v_ace_customer in its breaks, for the data steward and the ACE team
    Then no key is invented and no case is created from the missing view row
    Then both keys are read again on the next complete ALS batch

  Scenario: AC6 No direct ACE read and no case attribute served or stored (new, D-RCV-60)
    Given the service runs as the login rwb_source_data
    When it runs SELECT on public.account
    Then the statement is refused with permission denied
    When the case creation job calls the operation for 2026-12-01 at threshold 90
    Then the response carries no case number, status, stage, owner or queue field
    Then schema rwb_source_data holds no recovery_case, case_account or case_party table, and an insert of one into rwb_case.recovery_case is refused
    Then the response returns no case number and the value of the case-number sequence is unchanged after the call

  Scenario: AC7 A view error or a timeout answers 503 with no partial page (new, D-RCV-60)
    Given the ACE view v_ace_account raises an error for 2026-12-01 or the statement exceeds its 5 s timeout
    When the case creation job calls GET /api/recovery/source-data/v1/entry-candidates with businessDate 2026-12-01 and threshold 90
    Then the call is refused with status 503 and MSG-GEN-006 naming "ACE database"
    Then the response holds no partial page and nothing is cached

  Scenario: AC8 The exclusion facts and case attributes are never copied into a table of this service (new, D-RCV-60)
    Given the tables of schema rwb_source_data are listed after the migration
    Then no table of rwb_source_data holds a column copied from v_ace_account, v_ace_customer or v_ace_ca_relation other than the business keys
    Then no table of rwb_source_data holds a case column named case_number, status, stage, owner or queue
    Then tdr_flag and deceased_flag are returned as read from ACE and are stored in no table of this service, and dispute_open is returned as read from account_ext

  Scenario: AC9 A call without a credential, a caller other than the case service or an unknown path is refused with its status (new, D-RCV-60)
    When a call to GET /api/recovery/source-data/v1/entry-candidates arrives without a credential
    Then the call is refused with status 401
    When a call arrives from a caller that is not the case service identity
    Then the call is refused with status 403 and MSG-P4-002
    When a call names a path that is not an operation of /api/recovery/source-data/v1
    Then the call is refused with status 404

  Scenario: AC10 A replayed write with the same body answers the same result and writes nothing new (new, D-RCV-60)
    Given party_ext holds one row for "P0000123" with fraud_flag true
    When the exclusion screen repeats PUT /api/recovery/source-data/v1/extension-facts/parties/P0000123 with the same body of all four party flags, fraudFlag true
    Then the response repeats the first answer with fraudFlag true
    Then party_ext still holds one row for "P0000123"
```

**Target reading.** Every assertion above is new for this slice and keeps the legacy values: accounts A-5006, A-5007, A-5011, A-5012, A-5002, A-5013 and A-5005, persons P-0101, P-0103, P-0105 and the FSD person "P0000123", the threshold 90 and the business date 2026-12-01. What changes is where they are read. `AceSourceQuery.accountsAtOrAbove()`, `relationsFor()` and `customer()` are no longer in-process methods of the monolith but one REST read of this service, `GET /api/recovery/source-data/v1/entry-candidates`, with the error envelope of the case contract (DP-11, DP-13; C RWB-P3-E1018-CON). The three views and the extension tables are read through the one login that may read ACE, `rwb_source_data`, and no other service reads a `v_ace_*` view at any point (DP-02, DP-05; Architecture v5 slides 11 and 29; ADR-010). The threshold, the package in force and the reason codes stay on the decision side: this story returns `tdr_flag`, `deceased_flag`, `dispute_open`, `deceased_override`, `bankruptcy` and `fraud_flag` as facts and evaluates no package (DP-04 applied as a prohibition; rwb-decision owns the ENTRY and EXCLUSION packages). `party_ext` and `account_ext` are written 1:1 by business key on this service's own Flyway sequence, with no `id`, no foreign key and no ACE column, exactly as FSD AC-ALT-P1-001-03 states it (DP-01, DP-15). The gate is read from `v_ace_batch_status`, which is P1's to read, so a date whose ALS batch is late answers nothing; the STALE stamp and the `AceDataReady` and `AceDataLate` events belong to RWB-P1-E1015-APP (DP-05, DP-09). While `v_ace_batch_status` does not exist (until RWB-ACE-001 is deployed), the read answers as for an incomplete batch: status 409 with MSG-P1-001, no candidate row, no break row, and no LOADED stamp for DP01, so the case creation job creates no case for that date; the gate is read from the view only and is never inferred from data_as_of, a row count or a file. The response carries no case attribute at all: the case number, the status, the stage, the owner and the queue are rwb-case's, and nothing of them is served or stored here (AC6). Legacy AC1, AC2, AC3, AC4, AC5, AC6, AC8, AC10, AC11, AC12, AC14 and AC15 are owned by the rwb-case, rwb-decision, rwb-access and rwb-document slices of this key and by RWB-ITG-E1018-ITG, and this story claims none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account is a candidate when `days_past_due` in `v_ace_account` for the ACE business date is at or above the entry threshold; an account below it is never a candidate | Legacy RWB-E1-018 BR1; parameter case.entry.dpd = 90 (DL16); DF-ACE-018 |
| BR2 | The exclusion facts are read from the owner of each field — `v_ace_account.tdr_flag`, `v_ace_customer.deceased_flag`, `account_ext.dispute_open`, `party_ext.deceased_override`, `.bankruptcy` and `.fraud_flag` — by business key, and are never copied | Legacy §3 and BR3; FSD P1 v3 BR-P1-001-2 and BR-P1-001-5; TSD P1 v3 T3.5 |
| BR3 | An extension row is 1:1 with its ACE record, keyed by the business key, with no `id`, no foreign key and no column ACE already holds | FSD P1 v3 BR-P1-001-3, BR-P1-001-5 and AC-ALT-P1-001-03; TSD P1 v3 T3.5 |
| BR4 | No fact is returned for a business date whose ALS batch is not COMPLETED in `v_ace_batch_status`, and no data job for that date starts | Legacy BR7; CTL-02; FSD P1 v3 BR-P1-014-4 and VR-P1-001-1 (MSG-P1-001) |
| BR5 | A key with no view row is listed for the data steward and the ACE team and is never invented from a partial record; it is read again on the next complete batch | Legacy BR11; D-RCV-35 U4; ADR-010; REC-05 |
| BR6 | This service serves and stores no case attribute: the case number, the status, the stage, the owner and the queue belong to rwb-case | D-RCV-35 U4; Architecture v5 slide 41 (P3 owns case, CMMN state, queues, tasks, allocation, timers) |
| BR7 | The product group of a candidate is the ACE `product_category` value it read; it is returned unvalidated and never coerced into a list value | DF-ACE-010; TSD P1 v3 T3.4; §13 GAP-0576 |

**Coverage.** BR2 is covered by AC2 and AC8 (every exclusion value is read from its owner) and BR6 by AC6 and AC8 (no case attribute in the response or in the schema).

**Where each rule lives in the target.** BR1 is the single SQL predicate of the read plus the caller's threshold, which is what keeps the 90 a parameter of rwb-case and not a constant of this service (DP-06 applied as a prohibition: no parameter catalog is read here). BR2 is the four separate reads of step 5 to 8 of section 4 and the deliberate absence of any table of this service that holds an account, a customer or a relation column: the only place a value is stored is the extension row, and the extension row holds a Workbench decision, not a copy (DP-01, DP-05; FSD BR-P1-001-5). BR3 is the database shape — the primary key of `party_ext` is `person_key`, the primary key of `account_ext` is `account_key` — plus the conformance test that fails the build on a foreign key into `public` (FSD AC-EXC-P1-001-04; DP-15). BR4 is the gate of step 3 and 4, read from `v_ace_batch_status` and from nowhere else (FSD BR-P1-014-2). BR5 is the `breaks` of the response and the REC-05 reading; the durable break list stays with the reconciliation story RWB-P1-E1011-APP, whose own open point GAP-0575 records. BR6 is an absence that has to be built as one: the response schema, the entities and the schema `rwb_source_data` carry no case column, and AC6 asserts it by trying the insert that would break it. BR7 is a pass-through with no mapping table, so a product category ACE introduces tomorrow is returned as read and never silently dropped (GAP-0576).

### 9. State transitions

None in the business sense. This story changes no case status and holds no case. It reads ACE facts and it writes one row per ACE record in two extension tables; a change of an extension row is a version increment on the same key, never a new row.

| From | Event | Condition | To |
|---|---|---|---|
| an account at 89 days past due | the next complete ALS batch | `days_past_due` reaches the threshold for the business date | the account is a candidate row of that date |
| a candidate with no `party_ext` row | the exclusion screen records a flag | The key resolves to a `v_ace_customer` row or is listed by REC-05 | one `party_ext` row for the `person_key` |
| a `party_ext` row with a flag false | the exclusion screen records the same flag true | The caller holds the screen's right | the same row, the flag true, `version` plus one |
| a migration version applied on the service sequence | the keys or the standard columns need a fix | The sequence owner assigns the next version | a new Flyway version is merged; the applied version is never edited (DP-15) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case, case creation step (SY-CASEWF) | Calls the entry-candidate read for a business date and a threshold with its workload identity token; the only caller of the read |
| The exclusion screen's right-holder (a case role of rwb-case) | Records an exclusion fact through the extension write, arriving through gateway-bff with the user's token (DP-19) |
| RW-DATASTEW, data steward and data product owner | Reads the REC-05 breaks for a business date; changes no row |
| ACE team lead | Owns the ACE tables and columns behind the four views and reads the same breaks; reads no Workbench table |
| RW-PLATADM, platform administrator | Receives the incident of a view failure and reads the read's counter and latency series |
| RW-AUDIT, internal audit | Reads; may not record an exclusion fact |
| rwb-decision (P7) | Owns the ENTRY and EXCLUSION packages and evaluates them; this story hands it facts and evaluates nothing |
| rwb-case (P3) | Owns the case, the case number, the entry decision, the exclusion record and the case record API (C RWB-P3-E1018-CON) |

The read runs as the service identity of rwb-source-data (DP-02; Architecture v5 slides 11 and 29), and the caller's identity travels in the token so that the refusal of X6 is made for the caller. The extension write runs as the same service identity and carries the screen's user token; this service holds no role model of its own, and the right itself is the screen owner's (GAP-0573). Each operation is authorised by the rwb-access authorise check (DP-08) on the caller's token and right, under a check code Not specified in the source documents (DOR-RWB-P1-E1018-APP-6). The screen's body carries all four party flags on every call, so vulnerable is always written by the caller and never defaulted by P1; a repeat of the same body leaves one row, and a changed body replaces the flags on the same key with a version increment. The confirmation and its audit stay with the screen.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |
| DF-ACE-006 | v_ace_account | contract_no | Read |
| DF-ACE-010 | v_ace_account | product_category (returned as `productGroup`) | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-031 | v_ace_account | tdr_flag | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-061 | v_ace_customer | deceased_flag | Read |
| DF-ACE-084 | v_ace_ca_relation | person_key | Read |
| DF-ACE-085 | v_ace_ca_relation | account_key | Read |
| DF-ACE-086 | v_ace_ca_relation | relation_type | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read (the `asOf` of the page) |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-EXT-027 | account_ext | account_key | Read and write |
| DF-EXT-028 | account_ext | dispute_open | Read and write |
| DF-EXT-029 to DF-EXT-035 | account_ext | the seven standard columns | Write |
| DF-EXT-001 | party_ext | person_key | Read and write |
| DF-EXT-002 | party_ext | vulnerable | Read and write |
| DF-EXT-003 | party_ext | deceased_override | Read and write |
| DF-EXT-004 | party_ext | bankruptcy | Read and write |
| DF-EXT-005 | party_ext | fraud_flag | Read and write |
| DF-EXT-006 to DF-EXT-012 | party_ext | the seven standard columns | Write |

Field IDs are those in the Logical Data Model and Data Dictionary, and the view fields those of TSD P1 v3 T3.4.

**Which side is this story's.** `DF-ACE-001` to `DF-ACE-186` are ACE's own columns, read through four `recovery.v_ace_*` views and never stored: the service schema holds no account, customer or relation column at all (DP-05; FSD BR-P1-001-2). `DF-EXT-001` to `DF-EXT-005` and `DF-EXT-027` to `DF-EXT-028` are this story's write surface, with the seven standard columns of each table; `contact_point_ext` (DF-EXT-013 to DF-EXT-026) and `valuation_ext` (DF-EXT-036 to DF-EXT-049) are owned by P1 as well and are untouched here because case creation needs neither a contact point nor an appraisal. No `DF-CAS-*` field appears in this table: the recovery case, its account links and its party links are written by rwb-case in `rwb_case` and read by nobody here (BR6, AC6). No `DF-REF-*` row and no `DF-DEC-*` row is read or written: this story loads no reference data, takes no parameter and records no decision (DP-03 applied as a prohibition, DP-06 and DP-07 applied as prohibitions).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). The entry-candidate read and the two extension-fact writes, on the resources of this story. This key has no contract story of its own, so the OpenAPI 3.1 fragment of these three operations is published with the service API document by this story (GAP-0571; ASM-0813).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/entry-candidates?businessDate={date}&threshold={n}&page={p}&size={s}` | Returns one candidate row per account in `v_ace_account` at or above the threshold for the business date, with its exclusion facts and its borrower key, plus the keys that resolve to no view row | The rwb-case case creation service identity only; a staff role does not call it | Idempotent by the two parameters; nothing is cached and each call re-reads the views |
| PUT | `/extension-facts/parties/{personKey}` | Writes the 1:1 `party_ext` row of a customer and returns it | The exclusion screen's right-holder through gateway-bff (DP-19); the screen owns the right, this service validates the token | `PUT` by business key: the same body twice leaves one row and no second key |
| PUT | `/extension-facts/accounts/{accountKey}` | Writes the 1:1 `account_ext` row of an account and returns it | The same caller as the party write | The same rule as the party write |

The read's query is `businessDate` (ISO `yyyy-mm-dd`, required), `threshold` (integer, required, 0 to 999), `page` and `size` (optional, with the default and the maximum fixed by the published contract). Its response entity is `EntryCandidatePage`: `businessDate`, `threshold`, `asOf` (the `completed_at` of the COMPLETED ALS row), `page`, `size`, `total`, `candidates[]` and `breaks[]`. A candidate carries `accountKey`, `accountCode`, `productGroup`, `daysPastDue`, `totalBalance`, `contractNo`, `dataAsOf`, `tdrFlag`, `deceasedFlag`, `disputeOpen`, `deceasedOverride`, `bankruptcy`, `fraudFlag` and `personKey`; an absent extension row leaves its flags absent rather than false. A break carries `keyType` (`ACCOUNT` or `PERSON`), `businessKey`, `viewName` and `businessDate`. The exact response field set, the parameter names and the break row are a target choice: Not specified in the source documents (GAP-0571; ASM-0813) and Not specified in the source documents (GAP-0575; ASM-0817). Errors are 400 for a query that fails schema validation, 401 without a token, 403 for a caller that is not the case service identity (MSG-P4-002), 409 when the ALS batch for the date is not COMPLETE (MSG-P1-001) and 503 when a view raises an error or the statement times out (MSG-GEN-006, system "ACE database").

The two writes take `PartyExtFacts` (`vulnerable`, `deceasedOverride`, `bankruptcy`, `fraudFlag`, all required, because the table's seven flags and keys are mandatory) and `AccountExtFacts` (`disputeOpen`, required), and answer 200 with the stored row — the business key, the flags and the seven standard columns — read back inside the same call. Errors are 400 for a body that fails schema validation, 401, 403, 409 when the key is blank, 422 for a missing flag (MSG-GEN-001 naming the field) and 503 when the row cannot be written. Both writes are 1:1 by business key and are the only HTTP path by which the two tables are written; the exact paths and body shapes are a target choice of GAP-0571 and the guarantee attached to the caller is that of GAP-0573.

#### 12.2 REST operations consumed

None. This story calls no operation of another service: the four ACE reads are SQL over `recovery.v_ace_*` through this service's own login (DP-05), and the caller reaches it, not the other way round.

RWB-P3-E1018-CON is still a contract dependency of this story and its fake is used, because the case contract is the contract of the consumer of this read: it fixes the shared business keys (`account_key`, `person_key`), the ISO business date, the RFC 9457 problem envelope and the error codes both sides use, and its fake stands in for rwb-case in the contract test of 12.1, so a schema change on either side fails a build while rwb-case is still being built (DP-11; C RWB-P3-E1018-CON; 12.8).

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 41; DP-09). This story reads the same batch row that raises them and publishes no message of its own; it writes no outbox row, and a caller that needs the readiness fact reads the freshness stamp through RWB-P1-E1015-APP's contract.

#### 12.4 Events consumed

None. Architecture v5 slide 15 gives this service no consumed event ("none: Airflow call; fallback polls ACE batch record"), and this read is a synchronous REST call from the case creation job. The gate reads `v_ace_batch_status` on each call instead of waiting on a message, so a late batch needs no replay.

#### 12.5 Workflows and activities

None. The read is a synchronous REST step and completes in one statement set with no state of its own. The Temporal activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are other P1 stories, and JOB-02 Case creation is rwb-case's `DailyCaseRun` (Architecture v5 slide 44). The task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story; JOB-04 Reconciliation, which is the only job of this service that reads the same views on a schedule, is RWB-P1-E1011-APP's.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `party_ext` | `rwb_source_data` | P1 rwb-source-data | 1:1 by `person_key`: the read returns `vulnerable`, `deceased_override`, `bankruptcy` and `fraud_flag`, and the write upserts the one row with those flags and the seven standard columns. No `id`, no foreign key, no ACE column |
| `account_ext` | `rwb_source_data` | P1 rwb-source-data | 1:1 by `account_key`: `dispute_open` is read and written the same way. No `id`, no foreign key, no ACE column |
| `contact_point_ext` | `rwb_source_data` | P1 rwb-source-data | Owned by P1, keyed by `contact_key`; untouched here, because case creation reads no contact point |
| `valuation_ext` | `rwb_source_data` | P1 rwb-source-data | Owned by P1, keyed by `valuation_key`; untouched here, because case creation reads no appraisal |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library, created in this service's schema | The DP-09 library objects. This story publishes and consumes no message and keeps no stored response, so it writes no row of them |
| `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_batch_status` | `recovery` (ACE-owned schema) | ACE team, read only | SELECT only through the `rwb_source_data` login, one method per view. No copy, no foreign key, no write (DP-05) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` stay in `rwb_case` and are neither read nor written here; `v_ace_*` rows are never stored, so there is no table of this service that holds an account, a customer or a relation.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P3-E1018-CON fake | The rwb-case case contract, as the consumer stand-in of this read | A call of `GET /entry-candidates` with the two parameters by the case service identity; the same call with no token and with a staff token; and the shared error envelope and business-key types both sides must agree on |
| ACE view fixture | `recovery.v_ace_account`, `v_ace_customer`, `v_ace_ca_relation`, `v_ace_batch_status` | The synthetic rows of AC1 to AC5 — A-5002, A-5005, A-5006, A-5007, A-5011, A-5012, A-5013, P-0101, P-0103, P-0105 — a COMPLETED ALS row for 2026-12-01, a RUNNING ALS row for 2026-12-02, a customer row for "P0000123", and a relation row whose account and customer row are missing |
| Batch status absent fixture | The Section B state before RWB-ACE-001 lands | No `v_ace_batch_status` at all, with the flag off, so the gate of X4 is proved on the absent view as well as on an incomplete batch |
| Extension fixture | `rwb_source_data` | A container at the baseline plus this story's migration, with `party_ext` and `account_ext` and their business-key primary keys, so the 1:1 writes and the conformance test of AC3 run on the real keys |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations on `/api/recovery/source-data/v1` | None | OpenAPI 3.1; the caller's one hop with a 2 s budget is the caller's (DP-11); RFC 9457 problem details |
| Kafka | None | None | The topic and its two events belong to RWB-P1-E1015-APP (DP-14); this story writes no message |
| Temporal | None | None | No workflow, activity or Schedule in this story; queue `rwb-source-data` is untouched |
| File | None | None | No file is read or written; the facts are read from the views on each call, so no extract, staging file or lake path exists in this flow |

SQL view, not a call type of the matrix but the fifth row of Architecture v5 slide 11: four SELECT-only reads of `recovery.v_ace_*` through the `rwb_source_data` login, with a 5 s statement timeout, available to this service only (DP-02, DP-05).

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `casefacts`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P3-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency column is quoted from Template and Rules §R5.5, except the C dependency of DP-04: the contract story of that capability is RWB-P3-E1073-CON, which states the rwb-decision rule operations as consumed, and it is named here in place of the key §R5.5 gives, which has no story file. The metadata of this story carries no build dependency, because it is a Day-1 story of the Wave 1 baseline and builds against the published baseline of rwb-source-data, the published view contract and the RWB-P3-E1018-CON fake before the stories that deliver those three land: the platform contracts in the column above are part of the service template and the Wave 1 cut, not waits of this story (§R5.7 rules 2 and 8). Of the C dependencies in the column above, only DP-11's is named in the metadata of this story, beside RWB-P1-E1018-CON, the rwb-source-data contract story, and a C dependency never blocks a build.

DP-05 is this story's own pattern: the three `AceSourceQuery` calls of the monolith become one read of P1's own views through P1's own login, and no other service may read a view (Architecture v5 slides 11 and 29). DP-01 applies twice, once to the views (nothing is copied) and once to the two extension tables (P1 writes its own schema, and no foreign key crosses it). DP-02 is the single `rwb_source_data` login that makes both true. DP-15 applies on the service's own sequence, which carries the key assertion of the two extension tables and never a monolith version number.

**DP-03 applies as a prohibition.** The legacy story wrote a decision log entry per created case (legacy step 11, BR8, AC10). That entry is a decision of rwb-case and is recorded in the tenant of rwb-case through the decision-record library of RWB-PLT-E1027-CON; a read of ACE facts is not a decision and this story records none. It holds no `DecisionLogWriter` dependency and publishes nothing on `rwb.decision-record.v1`.

**DP-04 applies as a prohibition.** No Drools kit, no `RuleEvaluator`, no package and no `rule_row` read exists in this story. The ENTRY and EXCLUSION packages are rwb-decision's, evaluated in rwb-decision, and the reason code, the rule ID and the package version are recorded by rwb-case in `case_entry_exclusion`. This story hands over facts only, which is what keeps a package change free of a release on this side.

**DP-06 applies as a prohibition and a boundary.** The threshold is a parameter of rwb-case (`case.entry.dpd`, DL16) and is read by rwb-case; it reaches this service only as the `threshold` argument of one call. This story reads no parameter catalog and holds no default of its own, so a parameter change is invisible here.

**DP-07 applies as a prohibition.** No list is loaded, written or validated here. The product group is returned as the ACE `product_category` value it read (BR7; GAP-0576), and a caller that needs the LOV-PRODUCT label resolves it through the rwb-case reference-data contract.

**DP-09 applies as a statement.** The outbox, inbox and idempotency library objects exist in `rwb_source_data` because every schema of the platform has them, and this story writes none of them: it publishes no event, consumes none, and a GET keeps no stored response. The batch-readiness events belong to RWB-P1-E1015-APP, which owns the outbox rows that raise them.

**DP-10 applies as a statement.** The Quartz job of the monolith becomes rwb-case's event-started `DailyCaseRun` (Architecture v5 slide 44, JOB-02), which is the caller of this read. This story runs nothing on a schedule: the only clock in the flow is the ACE batch record, read per call.

**DP-11 applies as the shape of the read.** What was an in-process interface is a REST operation with a published schema, one hop and a 2 s budget on the caller's side, and a breaker on the caller's side; the read itself answers from the views in one statement set and never calls another service, so no chain of depth greater than one can form.

**DP-14 applies as a statement.** The topic name `rwb.source-data.events.v1` follows the naming library, and this story publishes nothing on it; the two event names it does not own follow the same pattern as `rwb.source-data.<Event>.v1`.

**DP-19 applies to the screens this story serves and does not build.** The exclusion screen of the rwb-case slice arrives through gateway-bff and calls the two extension writes; it never calls this service directly and this story renders nothing.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<next>__rwb_e1_018_entry_candidates.sql` (the next version on the service sequence) | Migration | Asserts, and where the baseline lacks them creates, the business-key primary keys of `party_ext` and `account_ext`, the `NOT NULL` of their mandatory columns and the absence of a foreign key into `public`; no ACE column, no new table |
| `EntryCandidateController` | Controller | The three operations of 12.1 on `/api/recovery/source-data/v1`; query and body validation; RFC 9457 problem details |
| `EntryCandidateService` | Service | The gate, the threshold predicate, the fact joins, the breaks and the page |
| `ExtensionFactService` | Service | The 1:1 upsert of the two extension tables, the read-back and the standard columns |
| `AceSourceReadRepository` | Repository | SELECT only on the four views, one method per view; names no `public` table |
| `BatchStatusReader` | Reader | The ALS row of `v_ace_batch_status` for the business date: `status`, `is_complete`, `completed_at` |
| `ExtensionFactRepository` | Repository | Upsert and read of `party_ext` and `account_ext` by business key; no ACE column and no foreign key |
| `EntryCandidate`, `EntryCandidatePage`, `Break` | Entity | The response of 12.1, with an absent flag kept absent and a break carrying keyType ACCOUNT or PERSON, businessKey, viewName and businessDate, listed in the response and counted in the run log; no table holds the breaks |

**Migrations and sequence (DP-15).** The migration sits on rwb-source-data's own Flyway sequence, after the baseline, and creates no table and no column: the four extension tables come from the baseline of RWB-P1-E1001-APP, and this story's version exists to make the two keys this story relies on an asserted fact rather than an assumption — the primary key `party_ext (person_key)`, the primary key `account_ext (account_key)`, the `NOT NULL` of the five mandatory `party_ext` columns and the two `account_ext` columns, and a catalog assertion that neither table holds a foreign key into `public`. Where the baseline already carries them, the version is a no-op and the same assertions run in the conformance test, so a repeated run changes nothing (FSD AC-EXC-P1-001-03). The exact version number is assigned by the sequence owner at build time and no monolith version number is reused; an applied version is never edited.

**Database.** Two tables of this service are written, `party_ext` and `account_ext`, 1:1 by business key. No table is created for the views, no view row is copied, no foreign key crosses a schema and no `public` table is named in any statement (DP-01, DP-05). Schema `rwb_source_data` is owned by rwb-source-data; schema `rwb_case` named in AC6 and in Done when is owned by rwb-case, and this service's login is refused any write to it.

**Configuration and reference data**

- The bounds of `threshold` (0 to 999), the default and maximum page size, and the 5 s statement timeout of the view reads are properties of the service, not business values. The threshold value itself is never a property of this service: it is the caller's parameter (DP-06).
- The source code `ALS` is the value of `v_ace_batch_status.source_system` the gate reads, held as configuration per source and never as a second completeness rule (DP-07 applied as a prohibition).
- The flag `rwb.dataengine.entry-candidates` gates the read at deployment; off, the operation answers 503 with MSG-P1-001's envelope and the case creation job creates no case for the date.
- No list of values is loaded by this story: the product group is passed through and the reason codes, the packages and the exposure bands stay with rwb-decision and rwb-case (DP-07).

**Build steps**

1. The migration version with the two business-key primary keys, the mandatory columns and the no-foreign-key assertion, with a repeated run that changes nothing; the matching conformance assertion (AC3, AC6).
2. `AceSourceReadRepository` with one SELECT per view over the four `recovery.v_ace_*` views and a statement timeout, with an architecture test that no class names a `public` table and no statement text contains one (AC6).
3. `BatchStatusReader` and the gate: the ALS row for the business date, the 409 with MSG-P1-001 and the last complete date, and the absent-view behaviour behind the flag (AC4; X4).
4. The threshold predicate and the candidate read for one business date, with a test that the query is one statement and not a loop over accounts (AC1; GAP-0572).
5. The fact joins: the borrower key through `v_ace_ca_relation`, `deceased_flag` through `v_ace_customer`, `dispute_open` through `account_ext` and the three party flags through `party_ext`, each read from its owner and with an absent row kept absent (AC2).
6. The breaks: an account key and a person key that resolve to no view row are separated from the candidates and listed with their view, and the count is written to the run log (AC5; GAP-0575).
7. `ExtensionFactService` and the two writes: the upsert, the seven standard columns, the read-back, the repeat with the same body and the refusal of a missing flag (AC3; X3).
8. The response entity, the OpenAPI 3.1 fragment of the three operations and the contract test against the RWB-P3-E1018-CON fake (12.1, 12.8; GAP-0571). The read takes businessDate and threshold as required query parameters and page and size as optional ones; the response EntryCandidatePage holds businessDate, threshold, asOf, page, size, total, candidates[] and breaks[], each candidate element named after the field it reads; the status set is 400, 401, 403, 409, 422 and 503.
9. The failure paths: the view error and the timeout answer 503 with MSG-GEN-006 and no partial page, and the 403 for a caller that is not the case service identity (X5, X6).
10. Tests for AC1 to AC10 on the ACE view fixture, seeded through the W1J01 harness with the ALS batch for 2026-12-01 at COMPLETE, and the fakes of 12.8, and the regression rows of section 16 where the fixture of the owning slice is available.

**Feature flag.** `rwb.dataengine.entry-candidates`. Off, the operation is refused at the edge of this service and the case creation job creates no case for the business date; nothing is read from the views and no extension row is written.

**Done when.** The tests in section 16 pass, the read answers AC1 to AC5 on the view fixture and the fakes, the two extension writes leave one row per business key with no `id`, no foreign key and no ACE column, the direct `public.account` read and the insert into `rwb_case.recovery_case` are both refused, and the schema `rwb_source_data` holds no case attribute and no copy of an ACE column.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ALS batch for the business date is not COMPLETE, or the batch view is not available yet | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required value is missing (a query parameter, a body flag) | Enter {field}. |
| MSG-P4-002 | The caller is not the case creation service identity, or the write arrives without the screen's right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A view raises an error, or the statement exceeds its timeout | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10. MSG-P1-001 fills {product} with "DP01 Account and arrears" and {date} with the last complete business date, both read from `v_ace_batch_status` and never written in code; MSG-GEN-001 fills {field} with the parameter or flag name and never a data value; MSG-GEN-006 fills {system} with "ACE database". MSG-P4-002 is raised by the caller's token check and passed on unchanged.

### 15. Screens and states

No screen in this story. The exclusion screen and the case record view belong to the rwb-case slice, which arrives through gateway-bff (DP-19) and calls the two extension writes; the case list and the reconciliation screens belong to RWB-P1-E1002-APP and RWB-P1-E1011-APP. On the caller's side the read has three visible states: candidates returned with the business date and the `asOf` of the ALS batch; a refusal with MSG-P1-001 in the Error state of the case creation run; and a page whose `breaks` are non-empty, which the data steward sees on the reconciliation screen and the ACE team sees in the same list. This story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02 | AC2 (the `tdr_flag` fact), BR3 — regression evidence: the EXCLUSION decision and the `case_entry_exclusion` row belong to rwb-decision and the rwb-case slice | End to end | `v_ace_account` A-5002 with `tdr_flag` true; package EXCLUSION "EXCL-2026.11" |
| TC-E1-018-01 | AC1 (the 90 boundary and the borrower key) — regression evidence: the case, its links and its number belong to the rwb-case slice and to RWB-ITG-E1018-ITG | End to end | `v_ace_account` A-5001 at 90 days past due, borrower P-0101, last number RW-2026-000122 |
| TC-E1-018-03 | AC1 (two accounts, one borrower) — regression evidence: grouping and the primary flag belong to the rwb-case slice | End to end | Borrower P-0102 with two HP accounts of 300,000.00 and 112,350.00 |
| TC-E1-018-04 | AC6 (no number is issued here) — regression evidence: issue-once belongs to the rwb-case slice and to RWB-ITG-E1018-ITG | End to end | Closed case RW-2026-000123 |
| TC-E1-018-05 | AC6 (no status list is held here) — regression evidence: the state model as data belongs to the rwb-case and rwb-access slices | End to end | New status value WAITING_COURT in LOV-CASE-STATUS |
| TC-E1-018-06 | AC2 (the `dispute_open` fact), BR3 — regression evidence: the exclusion decision belongs to rwb-decision and the record to the rwb-case slice | End to end | A-5005 with `dispute_open` true in account_ext; EXCLUSION rule "EXCL-006" |
| TC-E1-018-07 | AC1, BR1 | End to end | Accounts at 89 and 90 days past due in `v_ace_account` |
| TC-E1-018-08 | AC6 (a repeated call writes nothing) — regression evidence: the repeated run of case creation belongs to the rwb-case slice and to RWB-ITG-E1018-ITG | End to end | JOB-02 run twice for 2026-12-01 |
| TC-E1-018-09 | AC4, BR4 | End to end | ALS batch for 2026-12-02 at status RUNNING |
| TC-E1-018-10 | AC6 (no decision is recorded here) — regression evidence: the decision log write belongs to the rwb-case slice and to RWB-ITG-E1018-ITG | End to end | Decision log store unavailable for one account |
| TC-E1-018-11 | AC6 (no sequence is drawn here) — regression evidence: the yearly range belongs to the rwb-case slice | End to end | Sequence at 999999 |
| TC-E1-018-12 | AC1 (two product groups), BR7 | End to end | Borrower P-0103 with a mortgage and an HP account |
| TC-E1-018-13 | AC5, BR5 — the listing is this story's; the refused case read is the rwb-access slice's | Component | RW-REFADM reads GET /cases/{caseId} and is refused with MSG-P4-002 |
| TC-E1-018-14 | AC6 (a failed read changes nothing) — regression evidence: the resilience path of case creation belongs to the rwb-case slice and to RWB-ITG-E1018-ITG | Component | Decision log write forced to fail for the whole run |
| TC-E1-018-15 | AC5, BR5 | End to end | Case links A-5013 and P-0105 with no view row for 2026-12-01 |
| TC-E1-018-16 | AC2 (the exclusion facts as data) — regression evidence: the package in force check belongs to rwb-decision and the rwb-case slice | End to end | No EXCLUSION version in force on 2026-12-01 |
| TC-E1-018-17 | AC3 (the two extension writes are 1:1 by business key) — the component test of build step 7 against the FSD criterion AC-ALT-P1-001-03 | Component | Key "P0000123" written twice with the same body |
| TC-E1-018-18 | Contract of the three operations of 12.1 against the RWB-P3-E1018-CON fake and the OpenAPI 3.1 fragment (build step 8) | Component | The fragment of 12.1 and the fake of 12.8 |
| TC-E1-018-19 | Boundary of the tables of 12.7 (`party_ext` and `account_ext`, 1:1 by business key, mandatory columns, no foreign key) (ASM-3438) | Component | The migration assertions of build step 1 in `rwb_source_data`, run twice |
| TC-E1-018-20 | AC7 (X5: an ACE view error or a timeout answers 503 with no partial page) | Component | `v_ace_account` raises an error or the statement exceeds its 5 s timeout for 2026-12-01 |
| TC-E1-018-21 | AC8, BR2, BR6 | Component | The tables of schema `rwb_source_data` after the migration, listed and checked for copied ACE columns and case columns |
| TC-E1-018-22 | AC9 | Component | A call without a credential, a call from a caller other than the case service identity, a call to an unknown path |
| TC-E1-018-23 | AC10 | Component | Key "P0000123" repeated with the same body |

The Covers column of Test Cases v8 for TC-E1-018-01 to TC-E1-018-14 cites the criteria of the legacy story RWB-E1-018, not the criteria of section 7 of this story: TC-E1-018-01 to TC-E1-018-12 cover legacy AC1 to AC12 in the same order (TC-E1-018-07 is legacy AC7), TC-E1-018-13 covers Access and TC-E1-018-14 covers Principle 5. The Covers column above names the criteria of section 7 that this slice proves with the same test case. The legacy test case IDs are kept in the order this key's split plan gives them, with their Covers and Data kept character for character where the row is a regression row; the legacy level "System" maps to "End to end", "Access" to "Component" and "Resilience" to "Component", as in the other stories of this run. TC-E1-018-07, TC-E1-018-09, TC-E1-018-12 and TC-E1-018-15 are the four rows that prove what this story owns outright, and TC-E1-018-01, TC-E1-018-02 and TC-E1-018-06 contribute the fact side of AC1 and AC2 while standing as regression evidence for the slices that own their case, exclusion and decision parts; the other rows are kept as regression evidence for the slices of this legacy key that own those criteria — the rwb-case slice (the case, the number, the links, the grouping, the state model and the repeated run), the rwb-decision slice (the packages and the reason codes), the rwb-access slice (the refused read) and the rwb-document slice — and they run again in RWB-ITG-E1018-ITG against the live contracts. AC3 and AC6 are new criteria with no legacy test case: AC3 is proved by the component test of build step 7 against the FSD criterion AC-ALT-P1-001-03 with the key "P0000123", and AC6 by the architecture and catalog tests of build steps 1, 2 and 9. AC7 to AC10 are also new criteria, tested by TC-E1-018-20 to TC-E1-018-23. For TC-E1-018-01 to TC-E1-018-14 the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; TC-E1-018-15 to TC-E1-018-23 are still to be added to that workbook.

### 17. Guardrails

- No business value in code: the threshold arrives in the request and the parameter `case.entry.dpd` is rwb-case's; the source code `ALS` is configuration; no list value, band or reason code is written here (DP-06, DP-07).
- Personal data is carried and is kept out of logs, tests and prompts (Data Classification and Personal Data Inventory v5): `person_key`, `account_key` and `contract_no` are indirect identifiers (Confidential); `deceased_flag`, `vulnerable`, `deceased_override` and `bankruptcy` are Sensitive (Restricted), masked unless the role handles the deviation, never logged, and their read is audited through the ACE Common PII path; `fraud_flag`, `dispute_open`, `days_past_due` and `total_balance` are customer data (Confidential). The read returns no name, address, identity number or contact value, the run log carries counts and key types and never a clear key or a flag value, and test data is synthetic.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: four SELECT-only view reads through the `rwb_source_data` login, with no `public` table named in any statement and no copy of an ACE column anywhere (DP-05; FSD BR-P1-001-2).
- No foreign key crosses a schema and no extension table carries an `id`: the two writes are 1:1 by business key and the conformance test fails the build on a foreign key into `public` (DP-01, DP-15; FSD AC-EXC-P1-001-04).
- No case attribute is served or stored: the response schema, the entities and schema `rwb_source_data` hold no case number, status, stage, owner, queue or band, and the grant refuses a write into `rwb_case` (BR6; AC6).
- No package is evaluated and no decision is recorded: ENTRY and EXCLUSION stay in rwb-decision and the decision record in the tenant of the story that takes the decision (DP-03, DP-04).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-04 | 6.1 Take over the case at 90 days past due | R-UNI-16 | TC-E1-018-01, TC-E1-018-07, TC-E1-018-09 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-01 | 6.1 | None | TC-E1-018-01, TC-E1-018-04, TC-E1-018-11 |
| REQ-CWC-003 | One case per customer and product | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-02 | 6.1 | R-UNI-17 | TC-E1-018-03, TC-E1-018-08, TC-E1-018-12 |
| REQ-CWC-004 | Exclusion rules as data | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-05 | 6.1 | None | TC-E1-018-02, TC-E1-018-06, TC-E1-018-16 |
| REQ-CWC-005 | State model with one state at a time | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-03 | 6.1 | None | TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | Business Requirements Epic 1, sections 3.3 and 4; Program, section 5.3 | FEAT-CWC-21 | 6.1 | R-UNI-39 | TC-E1-018-10, TC-E1-018-14 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | Business Requirements Epic 1, section 3.3 | FEAT-CWC-01, FEAT-CWC-02, FEAT-CWC-03, FEAT-CWC-04, FEAT-CWC-05, FEAT-CWC-20, FEAT-CWC-21 | 6.1 Take over the case at 90 days past due | None | TC-E1-018-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1018-CON | Contract | C contract dependency: the case contract and its fake, the shared business keys and the error envelope this read and its consumer both use |
| RWB-P3-E1018-APP | App development | Sibling of the same legacy key: the case creation job that calls this read, the case number, the case row, the links and the exclusion record |
| RWB-P7-E1018-APP | App development | Sibling: the ENTRY and EXCLUSION packages and their evaluation, which consume the facts this read returns |
| RWB-P4-E1018-APP | App development | Sibling: the access right and the refusal of legacy AC14 |
| RWB-P5-E1018-APP | App development | Sibling: the document slice of this key, which reads the case this read makes possible |
| RWB-P3-E1018-OPS | DevOps | Sibling: the deployment of the case creation job that calls this read |
| RWB-ITG-E1018-ITG | Integration | The cross-service proof of the legacy key, including the write side of X6 and the end-to-end gate of AC4 |
| RWB-P1-E1015-APP | App development | Sibling in the same service: the freshness stamp and the `AceDataReady` and `AceDataLate` events this read relies on and does not own |
| RWB-P1-E1011-APP | App development | Sibling in the same service: JOB-04 Reconciliation, which keeps the durable REC-05 break list this read reports per call |
| RWB-P1-E1001-APP, RWB-P1-E1069-APP | App development, ACE DB | The published baseline and the view contract this story builds against with no build dependency (§3) |

### 19. Out of scope

- Issuing, formatting or reserving a case ID, the yearly number range and the RW-YYYY-NNNNNN rule (RWB-P3-E1018-APP; legacy AC1, AC4, AC11).
- Writing `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion`, the primary account rule, the total outstanding at entry and the exposure band (RWB-P3-E1018-APP; legacy AC1, AC2, AC3, AC12).
- Grouping accounts into a case, skipping an account that already sits on an open case, and the one-case-per-customer-and-product rule (RWB-P3-E1018-APP; legacy AC3, AC8, AC12).
- Evaluating package ENTRY or EXCLUSION, the reason codes, the package-in-force check and the exclusion record (RWB-P7-E1018-APP and RWB-P3-E1018-APP; legacy AC2, AC6, AC15).
- The decision log write for a created case (RWB-P3-E1018-APP; legacy AC10, AC14).
- The case status list, the state model and the refusal of a read without Case record R (RWB-P3-E1018-APP and RWB-P4-E1018-APP; legacy AC5, AC14).
- The freshness stamp of DP01, the STALE flag, `AceDataReady`, `AceDataLate` and the cut-off alert (RWB-P1-E1015-APP).
- JOB-04 Reconciliation, `reconciliation_result` and the durable REC-05 break list (RWB-P1-E1011-APP); this story reports the breaks of one call and keeps no table of them.
- The extension facts beyond case creation — consent and contact quality in `contact_point_ext`, the appraisal decision in `valuation_ext`, and the screens that record a death, a bankruptcy, a fraud or a dispute (the P1 and rwb-case slices of those keys).
- The case record view, the case list and every case attribute (RWB-P3-E1018-APP, RWB-P1-E1002-APP).
- The retention class of the extension rows and the archive of any record (RWB-P1-E1017-APP).
