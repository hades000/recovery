# RWB-P2-E2003-APP Customer's other products on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P2-E2003-APP-16); the squad sizes it at refinement |
| Contract version | /v1 path version of the operations in section 12.2; a fixed contract version is Not specified in the source documents (DOR-RWB-P2-E2003-APP-23) |
| Patterns applied | DP01, DP05, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CHO-003, REQ-RDF-010, REQ-RDF-009, REQ-CHO-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-003 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the other products the customer holds with the bank shown on the case with each product's type, status and business date, a stale marker when the holding is older than the expected business date, account numbers masked by my role and one PII access event for the read**, so that **I see the whole relationship before I decide a route, without a lookup in another system and without a copy of ACE data anywhere**.

The legacy story read `v_ace_party_product` from a reader inside the integration module and served the case parties through an in-process call. Under D-RCV-60 the read is a contract-composed read: rwb-integration owns `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` (the Ownership Map keeps `GET /cases/{caseId}/customer-products` with P2, and DP-13 moves the base to the service base), the case parties and the `account_key` values on the case come from the rwb-case contract, the customer product holding and the DP02 freshness come from the rwb-source-data contract, the role check and the masking rule come from the rwb-access contract, and the PII access event goes to ACE Common (INT-22). Only rwb-source-data reads the `recovery.v_ace_*` views (Arch v5 slides 8, 9, 13, 29 and 37; ADR-010), so this story holds no reader over the view; the legacy TSD P2 v3 wording that P2 reads `v_ace_party_product` directly is superseded (GAP-0662; ASM-1149).

The split is deliberate. The product holding stays in ACE, the parties stay with rwb-case, the roles and the masking rows stay with rwb-access and the access log stays with ACE Common: rwb-integration owns only the composition, the cache-free read and the response. Nothing is copied into `rwb_integration` (DP-01, BR7), no event is published, no workflow is started and no Schedule is created, because the legacy story wrote nothing either.

### 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. ACE holds the customer product holding it receives from SCBPDM (DL20, INT-04), keyed by `person_key`. The legacy story reads `v_ace_party_product` for the borrowers and co-borrowers of the case, shows each product with its status and business date, marks the list stale when the holding is older than the expected business date, and masks account numbers by role. Nothing is copied into a Workbench table; the view is the record. It meets REQ-CHO-003 (customer and product facts from the ACE customer profile) and REQ-RDF-010 (access by role and masking under PDPA), and it carries REQ-RDF-009 (a freshness stamp on every data product).

In the target the data is in the same place but the path changes. One service reads ACE: rwb-source-data owns the ACE view contract and the freshness stamp (Arch v5 slide 41), so the product holding and the expected business date are read through its contract and never from the view (DP-05, DP-11). The parties of the case and the accounts linked to it are case facts of rwb-case (DP-01), so they are read through the case contract and never from `recovery_case` or `case_account`. The roles, the scope and the masking policy are data of rwb-access (Arch v5 slide 41), so the authorise check and the masking rule are read through its contract (DP-08). The PII access log is ACE Common's (Arch v5 slide 30), so the read writes one event on INT-22 and nothing else. The panel on SCR-03 is composed at the edge by gateway-bff, which calls the owner once and merges the answer into the case screen (DP-19).

Three legacy calls disappear. `CustomerProductsReader.otherProducts` over `v_ace_party_product` becomes the rwb-source-data contract read, `DataProductStatus.freshness` becomes the same contract's freshness read, and `CaseQuery.partiesOf` becomes the rwb-case contract read; all three are one-hop REST calls with a 2 s timeout and a breaker, built on Day 1 against their fakes (DP-11). `Masking.apply` becomes the masking policy of rwb-access applied by the ACE common masking path, and `PiiAccessLog.write` stays the ACE Common path it always was.

The two sources disagree on the view, and the ruling is recorded. Architecture v5 says only rwb-source-data reads the thirty `recovery.v_ace_*` views, and the TSD P2 Integration v3 says P2 reads `v_ace_party_product` directly in T1.1 and T5.2; by R-PREC the architecture wins and the TSD wording is superseded (GAP-0662; ASM-1149). The login of the service, the field names of the three consumed contracts, the masking row shape, the composite route of the panel and the platform switch of the feature flag are the other open points, all carried in the same register row.

### 3. Preconditions

- RWB-P2-E1007-APP is done: the rwb-integration contract baseline is published, with the service base `/api/recovery/integration/v1`, the problem-details mapping, the error catalogue, the contract-test harness and the contract fakes of the services this base consumes.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case carries LOV-PARTY-ROLE and LOV-PRODUCT-STATUS with the version in force (DP-07). The party roles shown and the product status list are rows of that contract, not code (ASM-1155).
- RWB-PLT-E1037-CON and RWB-P4-E1037-CON are published: the authorise contract, the masking-policy read and the guard library that caches the rights of a session (DP-08).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and the migration conventions of `rwb_integration` (DP-15). This story adds no migration, because it stores nothing (ASM-1156).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the SCR-03 Case record and its other products panel (DP-19).
- The ACE view `v_ace_party_product` is live behind the rwb-source-data contract: it ships in V0003, the Section B migration of RWB-ACE-001 (DL43), and the feature stays behind its flag until V0003 is applied in the environment.
- The thirty `recovery.v_ace_*` views are granted SELECT to the rwb_source_data login only (ADR-010); rwb-integration holds no grant on the `recovery` schema and no grant on any other service's schema.
- LOV-PRODUCT-STATUS is loaded with the values ACTIVE, DELINQUENT, CLOSED and WRITTEN_OFF, and LOV-PARTY-ROLE with the roles the case shows (legacy precondition; DQ-020 and DQ-027).
- The masking rows for `v_ace_party_product.account_no` are loaded in rwb-access (DL26; the legacy split is assumed: clear for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, the last four digits for every other role) and are read through the rwb-access contract, never from a table of this service (GAP-0662; ASM-1152).
- The ACE PII logging path (INT-22) is available through ACE Common, and the integration service identity is enrolled on it.
- The case record view (SCR-03) is in production from Epic 1, and a case in scope exists with a borrower and a co-borrower and at least one linked account.
- The person holds a role with Case record R and the case in scope.
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0662; ASM-1148).

### 4. Flow

1. Case owner: opens SCR-03 Case record. The browser calls the gateway-bff composite route and never an owner service directly (DP-19).
2. gateway-bff: calls `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` on rwb-integration, one hop, and merges the answer into the case screen model with the case answer it already holds.
3. rwb-integration: checks the session and then the Case record right and the scope of the case through the rwb-access authorise contract, cached per session by the guard library; no Case record right is a 403 and a case outside the scope is a 404.
4. rwb-integration: reads the parties of the case with role borrower or co-borrower through the rwb-case contract, and the `account_key` values linked to the case through the same contract (DP-01).
5. rwb-integration: reads, for each `person_key`, the products held in the customer product holding through the rwb-source-data contract, excluding the `account_key` values already linked to the case (DP-05, DP-11).
6. rwb-integration: reads the freshness of data product DP02 through the rwb-source-data contract; when the holding is older than the expected business date, the answer carries the stale marker and the date the holding actually has.
7. rwb-integration: applies the masking rule for the caller's roles to each `account_no`, reading the rule through the rwb-access contract and applying it with the ACE common masking path.
8. rwb-integration: writes one PII access event (user, case, person keys and the fields shown) through the ACE Common PII logging path (INT-22); if the log does not accept the event the read fails and no product is returned.
9. rwb-integration: returns `CustomerProducts` with `dataAsOf`, `stale`, `messageCode` and `items[]`, each item carrying `personKey`, `partyRole`, `productType`, `accountNo` masked by role, `productStatus` and `dataAsOf` (GAP-0662; ASM-1153).
10. Case owner: the other products panel shows each product with its type, account number, status and business date; a stale list shows the stale message with its product and date, and a case with no other product shows the empty message.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The customer product holding is older than the expected business date | The last loaded products show with a stale marker and the date the holding has; a stale read is logged on the response and in the PII event | MSG-P1-001 | AC2 |
| X2 | The caller's role is not allowed to see account numbers | Account numbers are masked to the last four digits; the unmasked value is never returned and never logged | None | AC3 |
| X3 | The customer holds no other product | The empty list returns and the panel shows the empty message | MSG-P2-017 | AC4 |
| X4 | The case is outside the caller's scope | Refused before any contract is called; nothing is read and nothing is written | MSG-P4-003 | AC5 |
| X5 | The PII access log cannot be written | The products are not returned; the request fails | MSG-GEN-006 | AC6 |
| X6 | A role without the Case record right calls the endpoint | Refused; nothing is read, shown or logged as a product read | MSG-P4-002 | AC7 |
| X7 | The rwb-case, rwb-source-data or rwb-access contract does not answer inside the REST budget | One hop, 2 s timeout and a breaker per downstream; the read fails with the unavailable message and no product is returned | MSG-GEN-006 | AC1, AC6 |

X7 is the mechanism that replaces the legacy in-process calls: a caller that cannot have the parties, the products or the freshness has no answer to show, so the failure is a 503 and not a partial list. The masking and the PII log are not degraded: a rule that cannot be read and a log that cannot be written both stop the read (X5, BR5).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the published contracts: the rwb-integration baseline, the reference-data contract, the authorise and masking contract, the migration conventions and the edge route. The rwb-case, rwb-source-data and rwb-access answers come from their contract fakes |
| Negotiable | The party roles shown, the product status list and the masking split are data rows; the story fixes only the behaviour and the response shape |
| Valuable | The case owner sees the whole relationship without a lookup in another system, and no service holds a copy of the holding |
| Estimable | One endpoint, one composition service, four consumed contracts, one panel |
| Small | Fits one iteration with its tests |
| Testable | Each owned criterion is one automated test against the contract fakes; the access case is a component test and the resilience case is an NFR test |

### 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case

  Background:
    Given case "RW-2026-000410" has borrower "C-0410" and linked synthetic account "A-0410"
    Given the expected business date of the customer product holding is 2026-12-14
    Given the rwb-case contract mock returns case "RW-2026-000410" with borrower "C-0410" and linked synthetic account "A-0410"

  Scenario: AC1 Other products shown (legacy RWB-E2-003 AC1)
    Given the rwb-source-data contract mock returns for "C-0410" a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT", both with data as of 2026-12-14
    When the case record view loads for a case owner
    Then the other products panel shows 2 products with their type and status
    Then each product shows the business date 2026-12-14
    Then the system does not list account "A-0410" because its account_key is on the case

  Scenario: AC2 Holding older than the business date (legacy RWB-E2-003 AC2)
    Given the rwb-source-data contract mock returns data product "DP02" as of 2026-12-13 with no row for 2026-12-14, its last rows for 2026-12-13 and the expected business date 2026-12-14
    When the view loads
    Then the 2 products show with data as of 2026-12-13
    Then the panel shows message MSG-P1-001 with product "Customer products" and date 2026-12-13
    Then the system logs a stale read event with the case ID and the data product "DP02"

  Scenario: AC3 Masking (legacy RWB-E2-003 AC3)
    Given a phone collector (RW-PHONECOL) with the case in scope
    Given the rwb-source-data contract mock returns product "A-0411" with synthetic account number "9900015678"
    Given the rwb-access contract mock returns the masking policy of role "RW-PHONECOL", which keeps the last four digits of an account number
    When the view loads
    Then the other products show with the account number "XXXXXX5678"
    Then a case owner sees "9900015678"

  Scenario: AC4 No other products (legacy RWB-E2-003 AC4)
    Given the rwb-case contract mock returns case "RW-2026-000420" with borrower "C-0420" and linked synthetic account "A-0420"
    Given the rwb-source-data contract mock returns no product for borrower "C-0420" other than the case account
    Given the rwb-source-data contract mock returns no product for "C-0420" beyond "A-0420"
    When the view loads
    Then the panel shows an empty list with message MSG-P2-017

  Scenario: AC5 Case outside the scope (legacy RWB-E2-003 AC5)
    Given a case owner with scope "Own" and case "RW-2026-000410" owned by another person
    Given the rwb-access contract mock returns no scope for that case owner over case "RW-2026-000410"
    When the case owner calls GET /cases/{caseId}/customer-products
    Then the response is 404 with message MSG-P4-003

  Scenario: AC6 PII access log unavailable (legacy RWB-E2-003 AC6)
    Given the ACE PII logging service does not accept the access event
    Given the ACE Common PII logging mock refuses the access event
    When the view loads
    Then the system returns no product
    Then the response is 503 with message MSG-GEN-006

  Scenario: AC7 A role without the Case record right is refused (new, D-RCV-60)
    Given role "RW-REFADM" has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When the caller calls GET /cases/{caseId}/customer-products
    Then the response is refused with message MSG-P4-002
    Then nothing is read, shown or logged as a product read

  Scenario: AC8 Rules BR6, BR7 and BR9 hold on every read (new, D-RCV-60)
    Given the rwb-source-data contract mock returns product "A-0411" with a status code that is not in LOV-PRODUCT-STATUS
    When the view loads
    Then the product status code is held on the data quality break list
    Then nothing is written to rwb_integration and the holding is read again on the next request
    Then the read writes no row, decision record, event or workflow; its only write is the PII access event

  Scenario: AC9 Error answers 401 and 403 (new, D-RCV-60)
    Given the caller has no session
    When the caller calls GET /cases/{caseId}/customer-products
    Then the response is 401 with message MSG-P4-001
    Then a caller without the Case record right gets 403 with message MSG-P4-002

  Scenario: AC10 A status change is not an operation of this story (new, D-RCV-60)
    When the caller calls GET /cases/{caseId}/customer-products
    Then the read changes no case status and applies no transition of the Status transitions sheet
    Then a status change the model does not allow is refused by the case service, not by this story
```

AC1 to AC10 are the criteria this story owns; every value of AC1 to AC6 is copied unchanged from the legacy story, and AC7 (X6), AC8, AC9 and AC10 are new for D-RCV-60. Three statements inside them are answered by a contract fake rather than by a table of this service. AC1, AC2 and AC4 are answered by the rwb-source-data contract fake: it serves the products of `C-0410` with their status and business date, the DP02 freshness with its dates and its stale marker, and the empty holding of `C-0420`. The Background, AC4 and the exclusion of `A-0410` are answered by the rwb-case contract fake, which serves the parties and the `account_key` values of the case. AC3, AC5 and AC7 are answered by the rwb-access contract fake: it serves the Case record right, the scope and the masking policy of the caller's roles, and the masking itself is an rwb-access behaviour applied by the ACE common masking path, so the unmasked value never leaves the service. AC6 is an ACE Common behaviour: the PII logging mock refuses the event and the read fails. The Givens of AC1 and AC2 read the rwb-source-data contract only; the view v_ace_party_product is read by rwb-source-data, and this story sees only its contract (GAP-0662; ASM-1149). The panel that shows the answer is SCR-03's other products panel, served by the gateway-bff composite route (DP-19). Its states: empty is AC4 with MSG-P2-017; error is X7 with MSG-GEN-006; no access is X6 with MSG-P4-002, and no session is MSG-P4-001; the loading state is Not specified in the source documents (DOR-RWB-P2-E2003-APP-10).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Customer product facts are read from the holding ACE receives from SCBPDM, and in the target only rwb-source-data reads it, through the `v_ace_party_product` view; every other service reads it through the rwb-source-data contract | DL20; INT-04; RWB-ACE-001; ADR-010; DP-05 |
| BR2 | Products of every party with role borrower or co-borrower on the case are shown, except accounts already on the case, matched on `account_key` | LOV-PARTY-ROLE; legacy story intent |
| BR3 | Each product shows the business date of its holding; a holding older than the expected business date is shown as stale, with the date it has | REQ-RDF-009; VR-P2-001-1 |
| BR4 | Account numbers are masked by role on the masking rule owned by rwb-access, read through its contract with the version in force; the unmasked value is never returned and never logged | REQ-RDF-010; CTL-11; DL26; DP-08 |
| BR5 | Every read of customer data is logged to the PII log with who, what, when and which record, through ACE Common (INT-22); a read that cannot be logged is not answered | INT-22; REQ-RDF-010 |
| BR6 | Product status codes are those in LOV-PRODUCT-STATUS; an unknown code is held on the data quality break list | DQ-020; DQ-027 |
| BR7 | The products are not copied into a Workbench table: nothing is written to `rwb_integration` and the holding is read on each request | D-RCV-35 U1; tier map section 9.1; DP-01 |
| BR8 | The service reads no ACE view and no other service's table: parties and case accounts through the rwb-case contract, products and DP02 freshness through the rwb-source-data contract, rights and masking through the rwb-access contract | Arch v5 slides 8, 9, 29 and 41; ADR-010; DP-01; DP-05; DP-08 |
| BR9 | The read writes nothing: no row, no decision record, no event and no workflow; its only write is the PII access event of ACE Common | Legacy solution plan; Template and Rules §R7.2 s17 |
| BR10 | The party roles shown and the product status list are reference-data rows read through the rwb-case reference-data contract with the version in force; no role code and no status code is in code | DP-07; DQ-020 |
| BR11 | The switch is the platform feature flag `rwb.integration.customer-products`; while the flag is off, and while `v_ace_party_product` is not deployed, the panel is hidden and the endpoint answers with an error rather than an empty list | Legacy solution plan; TSD P2 v3 API-P2-011; ASM-1154 |
| BR12 | The case links to ACE by business key (`person_key`, `account_key`) only, with no foreign key and no copy of an ACE or case row in `rwb_integration` | DP-01; D-RCV-35 U4; ADR-010 |

Open decisions: DL20 (ASM-0189, ASM-2559, ASM-2608), DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) and DL43 (ASM-0193, ASM-0737, ASM-0748, ASM-0816) are still open. The story proceeds on the listed assumptions until each decision is recorded (DOR-RWB-P2-E2003-APP-18).

### 9. State transitions

None. This story does not change a case status and does not move a case. It reads only; the PII access log receives one event per read.

| Observed fact | Written by | Appears as |
|---|---|---|
| Case parties and linked accounts | rwb-case (P3) | The persons whose products are read, and the `account_key` values excluded from the answer |
| Customer product holding | ACE ingestion, read by rwb-source-data (P1) | Each product with its type, status and business date |
| ACE business date and DP02 freshness | rwb-source-data (P1) | `dataAsOf`, the expected business date and the stale marker |
| Masking rule and scope | rwb-access (P4) | The account number clear or at the last four digits, and whether the case is in scope |
| PII access event | ACE Common (INT-22) | One log row per read |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads other products on cases in scope, account numbers clear (Case record, R) |
| RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Read other products on cases in scope, account numbers clear (assumed; DL26) |
| RW-PHONECOL, RW-CONDUCT and other roles with Case record R | Read other products on cases in scope, account numbers masked |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rule rows, in rwb-access; this story reads them through the rwb-access contract and holds no copy |
| rwb-integration service identity (the rwb-integration login, DP-02) | Applies the access check, calls the rwb-case, rwb-source-data and rwb-access contracts one hop away, writes the PII access event and writes nothing else |
| rwb-access delegation and masking contract | Supplies the right, the scope and the masking rule with the version in force; it is the owner of the masking rows |
| rwb-source-data contract | Supplies the customer product holding and the DP02 freshness; it is the only reader of the `recovery.v_ace_*` views |
| gateway-bff (the platform edge) | Calls the operation once and merges the answer into the SCR-03 screen model; holds no copy of the products |
| RW-REFADM and every role without Case record R | Refused on the operation with MSG-P4-002 |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0662; ASM-1148).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the rwb-case contract |
| DF-CAS-004 | recovery_case | primary_person_key | Read through the rwb-case contract |
| DF-CAS-031 | case_party | case_id | Read through the rwb-case contract |
| DF-CAS-032 | case_party | person_key | Read through the rwb-case contract |
| DF-CAS-033 | case_party | party_role | Read through the rwb-case contract |
| DF-CAS-026 | case_account | account_key | Read through the rwb-case contract |
| DF-ACE-056 | v_ace_customer | person_key | Read through the rwb-source-data contract |
| DF-ACE-280 | v_ace_party_product | person_key | Read through the rwb-source-data contract |
| DF-ACE-281 | v_ace_party_product | account_no | Read through the rwb-source-data contract; masked by role before it leaves rwb-integration |
| DF-ACE-282 | v_ace_party_product | account_key | Read through the rwb-source-data contract; used to exclude the accounts on the case |
| DF-ACE-283 | v_ace_party_product | product_type | Read through the rwb-source-data contract |
| DF-ACE-284 | v_ace_party_product | product_status | Read through the rwb-source-data contract |
| DF-ACE-285 | v_ace_party_product | data_as_of | Read through the rwb-source-data contract; carried on each item |
| DF-REF-035 | role | role_code | Read through the rwb-access contract, with the masking policy of the role |

Field IDs are those in the Logical Data Model and Data Dictionary v9. `v_ace_party_product` is an ACE view in the `recovery` schema and is read only by rwb-source-data (ADR-010), so this story reads its seven fields through the P1 contract and never from the view; the JSON field names of that contract are Not specified in the source documents (GAP-0662; ASM-1150). No row of `recovery_case`, `case_party`, `case_account`, of the holding or of `role` is copied into `rwb_integration` (BR7, BR12), and the schema holds no foreign key into another schema. Personal data: DF-ACE-280 (person_key) and DF-ACE-281 (account_no) are personal data read on each request; account_no is masked by role before it leaves the service (BR4) and each read is logged to the PII log (BR5); this story stores none of them.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/customer-products` | The other products of the case's borrowers and co-borrowers: `dataAsOf`, `stale`, `messageCode` and `items[]` of `personKey`, `partyRole`, `productType`, `accountNo` masked by role, `productStatus` and `dataAsOf` | Case record R, scope applied, through the rwb-access authorise contract | Not applicable: the call writes nothing |

The Ownership Map keeps `GET /cases/{caseId}/customer-products` with P2 (legacy API-P2-011), and DP-13 gives it the service base. Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 unknown case or case outside the scope (MSG-P4-003); 503 the PII log does not accept the event, or a consumed contract does not answer inside the budget (MSG-GEN-006). The response carries `stale` and the `dataAsOf` of the holding, and `messageCode` carries the stale message when the holding is older than the expected business date and the empty message when the customer holds no other product. The JSON field names of the response and the shape of the problem body are Not specified in the source documents (GAP-0662; ASM-1153).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | rwb-case (P3) | The parties of the case with role borrower or co-borrower: `personKey`, `partyRole` | One hop, 2 s, breaker |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | rwb-case (P3) | The `account_key` values linked to the case, excluded from the answer | One hop, 2 s, breaker |
| GET | Not specified in the source documents (GAP-0662; ASM-1150) | rwb-source-data (P1) | The products of each `person_key` in the customer product holding: `personKey`, `productType`, `accountNo`, `productStatus`, `dataAsOf`; the path is not in the sources because Architecture v5 slide 15 gives P1 `/customers/{id}` and `/accounts/{id}` only, and the product read is added by this contract | One hop, 2 s, breaker |
| GET | `/api/recovery/source-data/v1/freshness` | rwb-source-data (P1) | The business date, the expected business date and the stale marker of data product DP02 (REQ-RDF-009) | One hop, 2 s, breaker |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Case record R and the scope of the case, cached per session by the guard library | One hop, 2 s, cached |
| GET | `/api/recovery/access/v1/masking-policies` | rwb-access (P4) | The masking rule of `account_no` for the caller's roles, with the version in force (CTL-11, DL26) | One hop, 2 s, cached |
| POST (ACE Common path) | INT-22, the PII logging path | ACE Common | One PII access event per read: user, case, person keys and the fields shown | One hop, 2 s |

The TSD P2 Integration v3 says P2 reads `v_ace_party_product` directly (T1.1 view B11, T5.2 and API-P2-011) and calls nothing in P1. Architecture v5 slides 8, 9, 13, 29 and 37, ADR-010 and the P1 row of slide 41 give the views to rwb-source-data alone; by R-PREC the architecture wins, so the view is read through the P1 contract and the TSD wording is superseded (GAP-0662; ASM-1149). The masking policy path is the operation Architecture v5 slide 14 gives rwb-access (`/masking-policies`); the Ownership Map API section has no row for it, so its path and its row shape are taken from that slide and fixed in the rwb-access contract baseline (GAP-0662; ASM-1152). The party and account paths are the Ownership Map rows of P3.

#### 12.3 Events published

None. The read publishes no event, writes no outbox row and holds no decision record. The service's topic `rwb.integration.events.v1` carries only FileDelivered and FileFailed, which belong to the file stories of this service (Arch v5 slide 16), and this story declares no topic of its own.

#### 12.4 Events consumed

None. The freshness of DP02 is read at request time through the P1 contract, so the endpoint subscribes to no topic and holds no inbox: a late ACE batch is answered as a stale list with the date the holding has, not as a projection of `AceDataReady` or `AceDataLate`.

#### 12.5 Workflows and activities

None. The read is served inside the request: it starts no workflow, adds no activity and holds no timer. The effect that a stale list has on a case decision belongs to the case workflow, which this story does not touch.

#### 12.6 Schedules

None. The legacy story had no Quartz job and the target adds none: the holding is read on each request, and no Schedule, no Temporal timer and no batch window is created by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| None | — | — | This story creates, reads and writes no table; nothing is copied into `rwb_integration` (DP-01, BR7) |
| `v_ace_party_product` (ACE view) | recovery | ACE team; read only by rwb-source-data (P1) | The holding behind the rwb-source-data contract; this story never reads it |

The `rwb_integration` schema holds interface config, file runs and outbound items for the file stories of this service (Arch v5 slide 41); this read adds no table, no column and no index to it, and adds no migration in the service's Flyway sequence (DP-15, ASM-1156).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contract | Case `RW-2026-000410` with borrower `C-0410` and linked `A-0410`; case `RW-2026-000420` with borrower `C-0420` and linked `A-0420`; the parties and accounts of both |
| rwb-source-data WireMock | The P1 contract | Products `A-0411` ACTIVE and `A-0412` DELINQUENT as of 2026-12-14; DP02 holding as of 2026-12-13 with expected business date 2026-12-14; no product for `C-0420` beyond the case account; a delayed answer beyond 2 s for X7 |
| rwb-access WireMock | The P4 contract | Allow RW-CASEOWN and RW-PHONECOL with Case record R in scope; refuse a role without Case record R with MSG-P4-002; refuse a case out of scope with MSG-P4-003; the masking policy of RW-PHONECOL keeping the last four digits and of RW-CASEOWN keeping the value clear |
| ACE Common PII logging stub | INT-22 | Accepts the access event; refuses it for AC6 |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-03 other products panel route and the merged screen model (DP-19) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 named paths and the product read consumed, plus the ACE Common PII path | The customer products read provided; the rwb-case parties and accounts, the rwb-source-data product and freshness reads, and the rwb-access authorise and masking reads consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None | No event is published and none is consumed (12.3, 12.4) |
| Temporal | None | No workflow and no activity (12.5) |
| File | None | This story reads and writes no file; the WIN and debt-buyer files are other stories of this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `customerproducts`, Java package `th.co.scb.ace.workbench.recovery.integration.customerproducts`; front end `src/modules/recovery/case/OtherProductsPanel.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; here only its contract, because rwb-integration owns no ACE view | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-15 applies to the service baseline and not to this read: the story adds no table and no migration, and the H dependency is on the conventions of the sequence (ASM-1156). DP-05 applies as a prohibition as well as a rule: rwb-integration owns no view and no table of the `recovery` schema, so the only path to the holding is the P1 contract.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CustomerProductsController | Controller | `GET /cases/{caseId}/customer-products`; the session and scope checks; the error mapping |
| CustomerProductsService | Service | Composes the answer: parties, accounts, products, freshness, exclusion, masking, stale marker and message code |
| PartyClient | Client | Calls the rwb-case contract for the parties and the linked accounts (DP-01) |
| ProductClient | Client | Calls the rwb-source-data contract for the products of each `person_key` (DP-05) |
| FreshnessClient | Client | Calls the rwb-source-data contract for the DP02 business date and stale marker (REQ-RDF-009) |
| AccessCheckClient | Client | Calls the rwb-access authorise contract for Case record R and the scope, cached by the guard library (DP-08) |
| MaskingClient | Client | Calls the rwb-access masking-policy read for the rule of the caller's roles (DP-08) |
| MaskingAdapter | Library adapter | Applies the rule to `account_no` through the ACE common masking path; the unmasked value is not returned and not logged |
| PiiAccessLogClient | Client | Writes one PII access event per read through the ACE Common path (INT-22); a refusal fails the read |
| StatusCatalog, PartyRoleCatalog | Service | Read LOV-PRODUCT-STATUS and LOV-PARTY-ROLE through the reference-data contract with the version in force (DP-07) |
| SourceCallGuard | Component | Wraps each contract call with the 2 s timeout, a breaker and a bulkhead, and turns a failure into the unavailable message (X7) |
| OtherProductsPanel | React component | SCR-03's other products panel: list, stale banner, empty state and the masked account column |

**Database and migrations**

- No table, no column and no index: the read copies nothing and the schema `rwb_integration` is not touched by this story (BR7, BR9).
- No migration in the rwb-integration Flyway sequence. DP-15 is satisfied by the baseline of RWB-P2-E1007-APP and by the conventions of RWB-PLT-E1044-CON (ASM-1156).
- The service connects with its own login, `rwb_integration`, holding grants on its own schema only and no grant on `recovery` or on another `rwb_*` schema (DP-02, Arch v5 slide 29). The login name is Not specified in the source documents (GAP-0662; ASM-1148).

**Configuration and reference data**

- LOV-PARTY-ROLE and LOV-PRODUCT-STATUS through the rwb-case reference-data contract with the version in force; the party roles shown are BORROWER and CO_BORROWER, and they replace the legacy property `rwb.customer.products.party-roles` (DP-07, ASM-1155).
- The masking rows of `account_no` stay in rwb-access and are read through its contract; this story holds no copy (ASM-1152).
- The feature flag `rwb.integration.customer-products` is kept as the legacy name of the switch and is read from the platform flag library (ASM-1154).

**Build steps**

1. `CustomerProductsService` against the three contract fakes, with the exclusion of the case `account_key` values and one test per AC; AC1 and AC4.
2. `PartyClient` and `ProductClient` over the rwb-case and rwb-source-data contracts, one hop and 2 s; AC1.
3. `FreshnessClient` and the stale marker with its message code and date; AC2.
4. `AccessCheckClient` and the scope refusal with 403 and 404; AC5 and the access case of section 16.
5. `MaskingClient` and `MaskingAdapter` with the clear and the last-four-digits paths for the two roles of AC3.
6. `PiiAccessLogClient` with the refusal path that returns no product; AC6.
7. `SourceCallGuard` with the timeout, breaker and the unavailable message; X7 as a component test.
8. `StatusCatalog` and `PartyRoleCatalog` over the reference-data contract, so no status code and no role code is in code; BR10.
9. `OtherProductsPanel` on SCR-03 against the gateway-bff stub, with the list, stale, empty and masked states of section 15.
10. Contract-fake run of every consumed answer in isolation, so the story builds before P1, P3 and P4 land.

**Feature switch.** The legacy flag name `rwb.integration.customer-products` is kept as the legacy reference for the switch. In the target the switch is a feature flag of the platform flag library (Template and Rules §R3 default ruling; Ownership Map `feature_flag` is PLT); off hides the panel and the endpoint answers with an error rather than an empty list, and while `v_ace_party_product` is not deployed the TSD P2 v3 records the same error state (GAP-0662; ASM-1154).

**Done when.** The tests in section 16 pass, the panel shows synthetic products in SIT with masking for RW-PHONECOL, the contract tests of the rwb-integration baseline and of RWB-P4-E1037-CON and RWB-P3-E1043-CON stay green, and no query of this story reaches the `recovery` schema or another `rwb_*` schema.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The customer product holding is older than the expected business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-017 | No other product held | The customer holds no other product with the bank in the customer profile of {date}. |
| MSG-P4-001 | No session, or a session with no Recovery role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The PII access log does not accept the event, or a consumed contract does not answer | {system} is not available. Your request is queued and will be retried. |

No identifier is renumbered by the realignment. MSG-P1-001 and MSG-P2-017 use the wording of the Error and Message Standard v4; MSG-P4-002, MSG-P4-003 and MSG-GEN-006 keep their legacy text unchanged, and MSG-P4-001 is the access message of the Access and authority module.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-03 Case record, other products panel | Loading | Sees the panel placeholder while the composite route answers |
| SCR-03 Case record, other products panel | Read only | Reads each product with its type, account number, status and business date; the account number is clear or at the last four digits by role |
| SCR-03 Case record, other products panel | Stale | Reads the stale message with the product and the date the holding has, and the products as last loaded |
| SCR-03 Case record, other products panel | Empty | Reads the empty message when the customer holds no other product |
| SCR-03 Case record, other products panel | Loading | Not specified in the source documents (CG-ALL-3090) |
| SCR-03 Case record, other products panel | Error | Reads MSG-GEN-006 and no product is returned when a downstream contract does not answer (X7) |
| SCR-03 Case record, other products panel | No access | Refused with MSG-P4-002 for a role without the Case record right (X6); MSG-P4-001 when there is no session |

The panel is SCR-03's other products panel and is served by the gateway-bff composite route, which calls rwb-integration once and merges the answer into the case screen model, one hop (DP-19). The route path, the screen-model field list and the merge order are Not specified in the source documents (GAP-0662; ASM-1151) and belong to RWB-PLT-N001-CON; the field-level masking of the screen model is the same masking rule the endpoint applied, so the screen never receives an unmasked value for a masked role.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-07 | AC7 | Component | RW-REFADM (no Case record right) calls GET /cases/{caseId}/customer-products; refused with MSG-P4-002 |
| TC-E2-003-01 | AC1, BR1, BR2, BR3 | End to end | rwb-source-data contract fake returns two other products, A-0411 and A-0412, for synthetic customer C-0410 |
| TC-E2-003-02 | AC2, BR3 | End to end | rwb-source-data contract fake returns DP02 as of 2026-12-13; expected business date 2026-12-14 |
| TC-E2-003-03 | AC3, BR4 | End to end | RW-PHONECOL and RW-CASEOWN read the same case |
| TC-E2-003-04 | AC4 | End to end | rwb-source-data contract fake returns no product for customer C-0420 beyond A-0420 |
| TC-E2-003-05 | AC5 | End to end | Case owner with scope Own and a case of another owner |
| TC-E2-003-06 | AC6, BR5 | NFR | PII logging stub refuses the event |
| TC-E2-003-08 | BR8, BR10 | Contract | Operations and events of section 12 called against the rwb-case, rwb-source-data and rwb-access contract fakes; no ACE view or other service table is read |
| TC-E2-003-09 | BR7, BR12 | Boundary | Each table of section 12.7 at its boundary; no row written to rwb_integration; ACE joined on person_key and account_key only |
| TC-E2-003-10 | BR6 | Component | Product status code not in LOV-PRODUCT-STATUS is held on the data quality break list |
| TC-E2-003-11 | BR9 | Component | The read writes no row, decision record, event or workflow; its only write is the PII access event |
| TC-E2-003-12 | BR11 | Component | Flag rwb.integration.customer-products off: panel hidden and endpoint answers with an error |
| TC-E2-003-13 | AC8, BR6, BR7, BR9 | Component | Product status code not in LOV-PRODUCT-STATUS is held on the data quality break list; the read writes no row, decision record, event or workflow |
| TC-E2-003-14 | AC9 | Component | Caller without a session gets 401 with MSG-P4-001; role RW-REFADM without the Case record right gets 403 with MSG-P4-002 |
| TC-E2-003-15 | AC10, BR9 | Contract | rwb-case contract fake serves case RW-2026-000410; section 12 has no status change operation; the case status is unchanged after the read |

For TC-E2-003-01 to TC-E2-003-07, the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-E2-003-08 to TC-E2-003-15 are added by this story; their workbook entries are Not specified in the source documents (DOR-RWB-P2-E2003-APP-12). Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-003-01 to TC-E2-003-15 are the ones this story runs, against its own endpoint and the contract fakes; the real cross-service journey of the key is proven by RWB-ITG-E2003-ITG.

### 17. Guardrails

- No business value in code: the party roles, the product status list and the masking rule are data rows read through the reference-data and access contracts; the story fixes only the behaviour.
- No personal data in logs, tests, workflow history or prompts. The read carries `person_key`, `account_key` and the masked account number; the unmasked number is returned only to a role whose rule allows it and is never logged. Test data is synthetic and no production customer, account or product is copied.
- No read of another service's tables and no ACE view: parties and case accounts come only through the rwb-case contract, products and DP02 freshness only through the rwb-source-data contract, rights and masking only through the rwb-access contract (DP-01, DP-05, DP-08, ADR-010).
- The `rwb_integration` schema holds no foreign key into another schema, and the case links to ACE by `person_key` and `account_key` only.
- No product is returned without its PII access event: a refused event fails the read with MSG-GEN-006 (BR5, AC6).
- The read writes nothing: no row, no decision record, no event and no workflow state, and a refusal writes nothing either (BR9).
- One hop, no chaining: the operation never calls a downstream of a downstream, and the breaker and bulkhead are per downstream (DP-11).
- A role without the Case record right sees a refusal, never a partial list and never another role's data (X6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer and product facts from the ACE customer profile | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | BR1, BR2, BR3 | TC-E2-003-01, TC-E2-003-02, TC-E2-003-04, TC-E2-003-05, TC-E2-003-08, TC-E2-003-09 |
| REQ-RDF-010 | Access by role and masking under PDPA | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | BR4, BR5 | TC-E2-003-03, TC-E2-003-06, TC-E2-003-07 |
| REQ-RDF-009 | Every data product carries a freshness stamp, and a stale product is shown as stale | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | BR3 | TC-E2-003-02 |
| REQ-CHO-010 | A duplicate case for the same customer and product is merged | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | None (out of scope, section 19) |

REQ-CHO-010 is carried in the traceability of the legacy key and is not served by this story; the legacy story puts the merge of a duplicate case in the Epic 3 backlog and section 19 repeats it.

### 19. Out of scope

- Merging a duplicate case for the same customer and product (R-UNI-17, REQ-CHO-010): the Epic 3 backlog.
- The masking rule rows themselves, their versions and their maintenance: carried by the rwb-access slice of this legacy key (RWB-P4-E2003-APP); this story only reads the rule through its contract.
- The reference-data rows LOV-PARTY-ROLE and LOV-PRODUCT-STATUS and their versions: the rwb-case reference-data stories; this story reads them through the contract.
- The rwb-case, rwb-source-data and rwb-access contracts themselves, their schemas and their fakes as artefacts: their CON stories.
- The gateway-bff composite route, its path and its merge order: RWB-PLT-N001-CON.
- The service baseline, the adapter pattern, the problem mapping and the contract-test harness of rwb-integration: RWB-P2-E1007-APP.
- Balances of the other products: the holding carries the product type and status only (DL20).
- The real cross-service journey with all services live, recorded as the integration slice of this legacy key (RWB-ITG-E2003-ITG).
