# RWB-ITG-E2003-ITG Customer's other products on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2003-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1069-APP, RWB-P2-E2003-APP, RWB-P4-E2003-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-003 for the wave 2 integration harness, which proves the customer's other products panel as one cross-service deliverable — the holding read through rwb-source-data's contract, the answer served by rwb-integration, the case facts from rwb-case, the masking decision and the two refusals from rwb-access, the stale stamp, the empty answer, the PII-log failure and the schema boundary — in one repeatable run per business date. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and test team (QA)**, I want **a repeatable cross-service harness that drives the customer's other products panel through gateway-bff, rwb-integration, rwb-source-data, rwb-case and rwb-access and writes one evidence report per run**, so that **the two products, their status, the business date, the stale stamp, the masked or clear account number, the empty answer and both refusals are proved to arrive from their owning service and to be returned unchanged — on Day 1 against the contract fakes and on every release after**.

This story is the wave 2 integration harness for the legacy key. It builds no production endpoint, table, workflow or schedule, and it owns no table. The three integration dependencies hold the behaviour:

- **RWB-P1-E1069-APP** — the read-only ACE view contract of rwb-source-data and the granted `recovery.v_ace_party_product` read that answers the holding, with the freshness stamp and the stale read log of DP02.
- **RWB-P2-E2003-APP** — the other-products read in rwb-integration and the `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` answer; ownership.json gives that operation to P2.
- **RWB-P4-E2003-APP** — the rights, scope and masking check: the authorise contract of rwb-access, the masking rule for the caller's role, and the two refusals returned unchanged.

The harness builds the runner, the fake pack, the seeds and the evidence, and it owns the seven acceptance criteria of section 7. The criteria of the legacy key stay with the app stories.

### 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. ACE holds the customer product holding it receives from SCBPDM (DL20, INT-04), keyed by person_key, and the legacy story read `v_ace_party_product` for the borrowers and co-borrowers of a case, showed each product with its status and business date, marked the list stale when the holding was older than the expected business date, and masked account numbers by role. In the target architecture that one panel is served by four services: rwb-source-data reads ACE and stamps the freshness, rwb-integration holds the other-products read and serves the answer, rwb-case holds the case facts, the accounts on the case and the reference data, and rwb-access decides the caller's right, the caller's scope and the masking rule.

A defect at any seam — the case accounts not excluded, a stale holding shown as fresh, a masking rule applied in the wrong service, a refusal rewritten on the way back, a product returned when the PII access log failed — would only appear with a live case, unless the panel is exercised across the services as one flow. This story is that exercise. It runs the panel journey through the contract fakes and then through the real services as their app stories land, reproduces the mask, the stale answer, the empty answer and both refusals in the same run, and attaches one evidence report per run keyed by story and business date, so the panel can be shown to hold before the wave is accepted and after every change. It meets REQ-CHO-003, REQ-RDF-010, REQ-RDF-009 and REQ-CHO-010 at the integration level and leaves every business rule, every screen behaviour and every table with the owning stories.

### 3. Preconditions

- The three I stories are published and deployed in the SIT environment as they land: RWB-P1-E1069-APP (the read-only ACE view contract and the granted `recovery.v_ace_party_product` read, with the freshness stamp and the stale read log), RWB-P2-E2003-APP (the other-products read and the customer-products operation) and RWB-P4-E2003-APP (the rights, scope and masking check).
- gateway-bff is deployed with the composite case-record route of DP-19 available, so the panel is read as one gateway answer and not by the browser calling each service. The composite route path and its merge order, the harness repository, its SIT and UAT environments, its seeding, its evidence format and retention and its pass or fail gate are Not specified in the source documents (GAP-0390; ASM-0565).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The synthetic seeds of the legacy story exist: open case "RW-2026-000410" with borrower "C-0410" and linked synthetic account "A-0410"; the revolving credit line "A-0411" with status "ACTIVE" and the personal loan "A-0412" with status "DELINQUENT", both with data as of 2026-12-14; the account number "9900015678" on "A-0411", masked as "XXXXXX5678"; and case "RW-2026-000420" with borrower "C-0420", who holds no other product.
- The expected business date of the customer product holding is 2026-12-14, and the holding of 2026-12-13 is seeded for the stale case of AC2.
- The reference rows the read depends on are held by their owners and read through their contracts: the product-group map and the list LOV-PRODUCT-STATUS with the values ACTIVE, DELINQUENT, CLOSED and WRITTEN_OFF from rwb-case (DP-07), the party roles shown from the same contract, the role, permission and masking rule rows from rwb-access (DP-08) and the DP02 freshness stamp from rwb-source-data. The harness holds no copy of any of them.
- Feature `rwb.integration.customer-products`, the legacy switch of this story, is on in the harness environment, so the read is served; the harness asserts the off state does not serve the panel.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands.

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the pack version and the fake or real mode of each service it touches.
2. Harness: seeds the run through the contract of each owning service, or through the fake in fake mode — case "RW-2026-000410" with borrower "C-0410" and account "A-0410", the products "A-0411" with status "ACTIVE" and "A-0412" with status "DELINQUENT" with data as of 2026-12-14, the account number "9900015678" on "A-0411", case "RW-2026-000420" with borrower "C-0420", and the role, scope and masking rule rows of the three synthetic users.
3. Harness: asserts the business date is ready through `GET /api/recovery/source-data/v1/data-products/freshness` and calls `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` for "RW-2026-000410" through gateway-bff, then asserts the 2 products of AC1 with their type, status and business date 2026-12-14 and the absence of "A-0410".
4. Harness: reads the case facts through `GET /api/recovery/case/v1/cases/{caseId}` and asserts that the parties read are the borrower and the co-borrowers of the case and that the exclusion is matched on the account key on the case (DP-07 for the party roles, DP-05 for the holding).
5. Harness: replays the stale holding of 2026-12-13, calls the same operation and asserts the answer of AC2 — 2 products with data as of 2026-12-13, MSG-P1-001 with product "Customer products" and date 2026-12-13, and the stale read log carrying the case id and "DP02".
6. Harness: calls the same operation as RW-PHONECOL and as RW-CASEOWN for the same case, reads the role, scope and rights of each through `GET /api/recovery/access/v1/me/session`, and asserts "XXXXXX5678" and "9900015678" from the same answer with no masking branch in rwb-integration (AC3).
7. Harness: calls the operation for "RW-2026-000420" and asserts the empty list with MSG-P2-017 and the empty panel state of §15 (AC4).
8. Harness: calls the operation as a role without Case record R and as a caller whose scope does not hold the case, and asserts 403 with MSG-P4-002 and 404 with MSG-P4-003, each decided by rwb-access and returned unchanged (AC5).
9. Harness: makes the ACE PII logging service refuse the access entry through the fake, calls the operation, asserts no product and 503 with MSG-GEN-006 naming the ACE PII logging service, and asserts that nothing was read from the ACE view without the entry (AC6).
10. Harness: reads the trace of the run, asserts one hop per call with the 2 s timeout, no cross-schema read, join, view or foreign key between `rwb_source_data`, `rwb_integration`, `rwb_case` and `rwb_access`, the ACE views read only by rwb-source-data, and the product-group map from rwb-case's reference-data contract (AC7).
11. Harness: publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or fake that answered, the value observed and the pass or fail result; the evidence format and its retention are Not specified in the source documents (GAP-0390; ASM-0565).
12. Harness: releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | The customer product holding is older than the expected business date | The last loaded products show with data as of 2026-12-13 and a stale marker; the stale read is logged with the case id and "DP02" | MSG-P1-001 | AC2 |
| X2 | The caller's role is not allowed to see account numbers | The account number is masked to the last four digits; the decision is rwb-access's and not rwb-integration's | None | AC3 |
| X3 | The customer holds no other product | An empty list with the empty panel state | MSG-P2-017 | AC4 |
| X4 | A role without the Case record right calls the operation | Refused with 403; nothing is shown; the refusal is not rewritten | MSG-P4-002 | AC5; TC-E2-003-07-ITG |
| X5 | The case is outside the caller's scope | Refused with 404; nothing is shown; the refusal is not rewritten | MSG-P4-003 | AC5 |
| X6 | The PII access log cannot be written | No product is returned; the request fails | MSG-GEN-006 | AC6 |
| X7 | A service reads the ACE views or another service's schema | The run fails on the trace, with the schema and the statement named | None | AC7 |

X2 to X4 are the legacy exception paths of RWB-E2-003 and keep their legacy behaviour at the seam; X7 is the boundary the harness adds and no production behaviour.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the three I stories are deployed; until then it runs against the §12.8 fakes, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes and the assertions are configuration and data; the business values are the legacy ones |
| Valuable | The panel is proved to hold across four services, with the stale stamp, the masking decision and the refusals in the places their owners put them |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each of the seven `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case - wave 2 integration harness

  Background:
    Given case "RW-2026-000410" has borrower "C-0410" and linked synthetic account "A-0410"
    Given the expected business date of the customer product holding is 2026-12-14

  Scenario: AC1 The panel is answered across the two services (new, D-RCV-60)
    Given "C-0410" holds a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT" in the holding ACE holds for the person, both with data as of 2026-12-14
    When the harness calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for "RW-2026-000410" through gateway-bff
    Then rwb-integration takes the holding through rwb-source-data's contract, over the `v_ace_party_product` read that contract serves
    And rwb-integration takes the case facts and the accounts on the case through rwb-case's contract
    Then the answer holds 2 products with their product type and their status
    And each product carries the business date 2026-12-14
    And account "A-0410" is not listed, because its account key is on the case
    And each call is one hop with the 2 s timeout of DP-11

  Scenario: AC2 A holding older than the business date (new, D-RCV-60)
    Given the holding ACE holds has no row for 2026-12-14 and its last rows for "C-0410" are for 2026-12-13
    When the harness calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for "RW-2026-000410"
    Then the 2 products are returned with data as of 2026-12-13
    And the answer carries MSG-P1-001 with product "Customer products" and date 2026-12-13
    And rwb-source-data logs the stale read with the case id and the data product "DP02"
    And the stale stamp is rwb-source-data's, taken through its contract, and not computed in rwb-integration

  Scenario: AC3 Masking is rwb-access's decision (new, D-RCV-60)
    Given a phone collector (RW-PHONECOL) with case "RW-2026-000410" in scope
    Given product "A-0411" has synthetic account number "9900015678"
    When RW-PHONECOL calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for the case
    Then the other products show the account number "XXXXXX5678"
    When a case owner (RW-CASEOWN) calls the same operation for the same case
    Then the other products show "9900015678"
    And the decision is the masking rule of rwb-access for the caller's role (DP-08), returned unchanged by rwb-integration
    And rwb-integration holds no masking branch of its own

  Scenario: AC4 A borrower with no other product (new, D-RCV-60)
    Given borrower "C-0420" of case "RW-2026-000420" holds no product other than the case account
    When the harness calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for "RW-2026-000420"
    Then the answer holds an empty list
    And the answer carries MSG-P2-017
    And the panel shows the empty state of section 15

  Scenario: AC5 Rights and scope (new, D-RCV-60)
    Given a caller whose role does not hold Case record R
    When the caller calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for "RW-2026-000410"
    Then the answer is 403 with MSG-P4-002
    And the refusal is decided by rwb-access and returned unchanged by rwb-integration
    And no product is returned
    Given case "RW-2026-000410" is outside the caller's scope
    When the caller calls the same operation
    Then the answer is 404 with MSG-P4-003
    And the refusal is decided by rwb-access and returned unchanged by rwb-integration
    And no product is returned

  Scenario: AC6 The PII access log is unavailable (new, D-RCV-60)
    Given the ACE PII logging service does not accept the access entry for the read
    When the harness calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products for "RW-2026-000410"
    Then no product is returned
    And the answer is 503 with MSG-GEN-006 naming the ACE PII logging service
    And nothing is read from the ACE view without the access entry

  Scenario: AC7 The boundary of the read (new, D-RCV-60)
    Given the four calls of this feature run in one harness run: the filled case, the stale case, the empty case and the refusal case
    When the trace of the run is checked
    Then the `v_ace_party_product`, `v_ace_customer` and `v_ace_contact` views are read only by rwb-source-data through its contract; rwb-integration holds no granted ACE view and reads none, because ownership.json gives `rwb_integration` no ACE view and Architecture v5 gives the views to rwb-source-data alone
    And no cross-schema read, join, view or foreign key exists between `rwb_source_data`, `rwb_integration`, `rwb_case` and `rwb_access`
    And every call in the run is one hop with a 2 s timeout (DP-01, DP-05, DP-11)
    And the product-group map is read from rwb-case's reference-data contract (DP-07)
    And the run fails when any of these is broken, with the schema, the statement or the call chain named
```

These seven criteria are new for the ITG harness and do not restate the app criteria owned by the I stories. They use only the legacy values of RWB-E2-003: case "RW-2026-000410", borrower "C-0410", account "A-0410", the revolving credit line "A-0411" with status "ACTIVE", the personal loan "A-0412" with status "DELINQUENT", business dates 2026-12-14 and 2026-12-13, account number "9900015678" masked as "XXXXXX5678", case "RW-2026-000420" with borrower "C-0420", data product DP02, and the messages MSG-P1-001, MSG-P2-017, MSG-P4-003, MSG-P4-002 and MSG-GEN-006.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Customer product facts are read from v_ace_party_product, which ACE holds from SCBPDM | DL20; INT-04; RWB-ACE-001 |
| BR2 | Products of every party with role borrower or co-borrower on the case are shown, except accounts already on the case, matched on account_key | LOV-PARTY-ROLE; story intent |
| BR3 | Each product shows the business date of its holding; a holding older than the expected business date shows as stale | REQ-RDF-009; VR-P2-001-1 |
| BR4 | Account numbers are masked by role on the masking rules | REQ-RDF-010; CTL-11; DL26 |
| BR5 | Every read of customer data is logged to the PII log with who, what, when and which record | INT-22; REQ-RDF-010 |

BR1 to BR5 are the legacy rules of RWB-E2-003, copied word for word with their sources. The harness asserts them against the owning services; it does not re-implement them, and no BR row is changed by this story.

| ID | Realignment rule the harness proves | Source |
|---|---|---|
| BR6 | The ACE holding is read by rwb-source-data; every other service takes it through that contract, never from an ACE view or a public table of ACE | DP-05; Architecture v5 slides 11, 29 and 46; ownership.json (`account_ext`, `party_ext`, `contact_point_ext` = P1) |
| BR7 | The masking rule is rwb-access's data (`masking_rule`, owner P4); the decision is the guard's and no service carries a masking branch of its own | DP-08; ownership.json (`masking_rule` = P4); legacy BR4 read as a target rule instead of a local one |
| BR8 | The freshness stamp and the stale read log of DP02 are rwb-source-data's, taken from its freshness answer; the caller shows the stamp and never derives it | DP-05; *Architecture v5* slide 15 (P1 OUT: `rwb.source-data.events.v1`, freshness); legacy BR3 |
| BR9 | The product-group map, the product-status list and the party roles shown are reference data of rwb-case, read through its reference-data contract | DP-07; ownership.json (`reference_row`, `lov_value` = P3); R-PREC default ruling |

### 9. State transitions

None. This story changes no case status and no case state; it reads records only, and the harness adds no transition of its own. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| The other-products answer of a case | rwb-integration, over the holding read of rwb-source-data and the case facts of rwb-case | 2 products with type, status and business date 2026-12-14, with "A-0410" excluded (TC-E2-003-01-ITG) |
| The holding stamped older than the business date | rwb-source-data freshness | The 2 products with data as of 2026-12-13 and MSG-P1-001 (TC-E2-003-02-ITG) |
| The stale read logged | rwb-source-data | One stale read with the case id and "DP02" (TC-E2-003-02-ITG) |
| The account number masked for a role | rwb-access masking rule | "XXXXXX5678" for RW-PHONECOL and "9900015678" for RW-CASEOWN on the same answer (TC-E2-003-03-ITG) |
| The empty answer | rwb-integration | An empty list with MSG-P2-017 for "RW-2026-000420" (TC-E2-003-04-ITG) |
| The scope refusal | rwb-access | 404 with MSG-P4-003 (TC-E2-003-05-ITG) |
| The right refusal | rwb-access | 403 with MSG-P4-002 and no product (TC-E2-003-07-ITG) |
| The read refused when the access entry fails | rwb-integration, with the ACE PII logging service | 503 with MSG-GEN-006 and nothing read from the view (TC-E2-003-06-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the other products on cases in scope, account numbers clear (Case record R); the synthetic user the harness drives |
| RW-PHONECOL, phone collector | Reads the other products on cases in scope, account numbers masked (Case record R); the synthetic user the harness drives |
| RW-REFADM, reference data administrator | Loads the product-status list and the product-group map through the rwb-case contract (Reference data C); used by the access case as the role without Case record R |
| RW-COE, Center of Excellence | Owns the product-group map values and the lists the panel reads (Reference data U) |
| QA lead | Owns the harness pack, the seeds, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Access owner | Owns the role, scope and masking rule rows the answer is decided on, in rwb-access |
| No approval applies | The story takes no decision and the harness asserts the decisions of the owning stories |

No names of people appear anywhere in this story; the roles above are the actors, and the synthetic identifiers are the data.

### 11. Data

The harness owns no table (DP-01, DP-15). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary, and the schema column is the owner in ownership.json.

| Owner and schema | Entity | Field | Field ID | Read or write | Contract |
|---|---|---|---|---|---|
| P3 `rwb_case` | recovery_case | id | DF-CAS-001 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | recovery_case | primary_person_key | DF-CAS-004 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | case_party | case_id | DF-CAS-031 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | case_party | person_key | DF-CAS-032 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | case_party | party_role | DF-CAS-033 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | case_account | account_key | DF-CAS-026 | Read | `GET /api/recovery/case/v1/cases/{caseId}` |
| P3 `rwb_case` | reference_row, lov_value | the product-group map and the list LOV-PRODUCT-STATUS (ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF) | Not specified in the source documents (GAP-0390; ASM-0565) | Read | The rwb-case reference-data contract (DP-07) |
| P3 `rwb_case` | reference_row | the party roles shown, borrower and co-borrower | Not specified in the source documents (GAP-0390; ASM-0565) | Read | The rwb-case reference-data contract (DP-07) |
| P1 `rwb_source_data` | account_ext, party_ext, contact_point_ext | the extension tables behind the holding read | Not specified in the source documents (GAP-0390; ASM-0565) | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_customer | person_key | DF-ACE-056 | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | person_key | DF-ACE-280 | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | account_no | DF-ACE-281 | Read by rwb-source-data, asserted as masked or clear | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | account_key | DF-ACE-282 | Read by rwb-source-data, asserted on the exclusion | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | product_type | DF-ACE-283 | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | product_status | DF-ACE-284 | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 by the granted ACE read | v_ace_party_product | data_as_of | DF-ACE-285 | Read by rwb-source-data, asserted on the answer | The rwb-source-data contract (DP-05) |
| P1 `rwb_source_data` | data_product, data_product_load | the freshness stamp of DP02 and the stale read record | Not specified in the source documents (GAP-0390; ASM-0565) | Read by rwb-source-data, asserted on the answer | `GET /api/recovery/source-data/v1/data-products/freshness` |
| P4 `rwb_access` | role | role_code | DF-REF-035 (legacy field ID; the entity `role` is P4's in the target, ownership.json) | Read | `GET /api/recovery/access/v1/me/session` |
| P4 `rwb_access` | permission | the Case record right of the caller | Not specified in the source documents (GAP-0390; ASM-0565) | Read | `GET /api/recovery/access/v1/me/session` |
| P4 `rwb_access` | masking_rule | the masking rule of `v_ace_party_product.account_no` for each role | Not specified in the source documents (GAP-0390; ASM-0565) | Read | The rwb-access authorise contract (DP-08) |
| P2 `rwb_integration` | — | None: the answer is computed from the P1 and P3 reads, and this story reads no table of `rwb_integration`; the tables P2 owns there (`interface_config`, `outbound_item`, `job_catalog`) are not touched by the read | — | None | None |

`v_ace_party_product`, `v_ace_customer` and `v_ace_contact` are read through the rwb-source-data contract, never from a public table, and only rwb-source-data holds the grant on the views. Test data is synthetic: no production case, party, product or account number is used, and the run report holds identifiers, statuses, dates, message ids and results only.

### 12. Contract

#### 12.1 REST operations provided

None. The harness provides no REST operation, and rwb-integration's own operation is provided by RWB-P2-E2003-APP.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/cases/{caseId}/customer-products` | P2 rwb-integration | The other-products answer for a case: the products, their type and status, the business date, the stale flag and message, and the account number masked by role (AC1 to AC6) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The expected business date and the stale stamp of DP02 the answer is judged on (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts, the parties and the account keys on the case, and the reference rows the answer is built from (AC1, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, scope and rights of the caller the mask and the two refusals are decided on (AC3, AC5, AC6) |

The masking decision and the authorise check themselves are the rwb-access guard contract of DP-08, called by rwb-integration through the guard library and owned by RWB-P4-E2003-APP; the harness reads the decision through `GET /api/recovery/access/v1/me/session` and asserts it on the answer, and it calls no authorise operation of its own.

The composite case-record route the panel is read through is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0390; ASM-0565).

#### 12.3 Events published

None. The harness publishes no Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | The business date 2026-12-14 is ready and the holding read has run, so the answer of AC1 carries data as of 2026-12-14 and the stale answer of AC2 is judged against it (AC1, AC2) |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | All 19 services publish their own record; P7 rwb-decision seals the central ledger (EV-08) | The masked and the clear read each leave one decision record naming the role and the rule version, so the mask is shown to be a recorded decision and not a branch in the answer (AC3) |

The access refusal is asserted on the answer and the message only: ownership.json and the event catalogue give `rwb.access.events.v1` the events `AccessPolicyChanged` and `DoaLimitChanged` and no access-denied event, so no refusal event is asserted. The harness consumes both topics as a test consumer with its own group, holds no inbox table, gets no production record and publishes nothing.

#### 12.5 Workflows and activities

None added, and none started. rwb-integration holds no workflow for this read: ownership.json gives `rwb-integration` the activities `deliverFile` and `receiveFile` on the queue `rwb-integration` for its file work, and Arch v5 slide 16 gives it no domain workflow, so the customer-products answer is a REST read and not a Temporal step. The harness starts no workflow, calls no activity and uses no queue.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow, and it creates no Schedule.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01, DP-15); it seeds and reads through the owning services' contracts only.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers | Used by |
|---|---|---|---|
| rwb-source-data (WireMock, from its OpenAPI) | `GET /api/recovery/source-data/v1/data-products/freshness` and the holding read behind the P1 contract | DP02 fresh at 2026-12-14 with the 2 products of "C-0410"; DP02 with its last rows at 2026-12-13 and the stale read log; the empty holding of "C-0420"; the PII-log-refused answer | AC1, AC2, AC4, AC6 |
| rwb-integration (WireMock, from its OpenAPI) | `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` | The 2-product answer with data as of 2026-12-14; the stale answer of 2026-12-13 with MSG-P1-001; the empty answer with MSG-P2-017; 403 with MSG-P4-002; 404 with MSG-P4-003; 503 with MSG-GEN-006 | AC1 to AC6 |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases/{caseId}` and the reference-data contract | "RW-2026-000410" with borrower "C-0410" and account "A-0410"; "RW-2026-000420" with borrower "C-0420"; the product-group map with the product of "A-0411" and "A-0412"; LOV-PRODUCT-STATUS | AC1, AC2, AC4, AC5, AC7 |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` and the masking rule answer | RW-CASEOWN clear, RW-PHONECOL masked to the last four digits on "9900015678", RW-REFADM without Case record R with MSG-P4-002, and a caller with scope Own outside the case with MSG-P4-003 | AC3, AC5; TC-E2-003-07-ITG |
| gateway-bff composite case-record route (WireMock) | The one gateway answer the panel is read from, composing the other-products answer, the case facts and the session | The five states of §15 | AC1 to AC5 |

The fakes are published from the owning services' OpenAPI documents and are versioned with the harness pack. The harness repository and its environments, its seeding, its evidence format and retention, its pass or fail gate and the composite route detail are Not specified in the source documents (GAP-0390; ASM-0565).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 4 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 2 consumed: `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None: no workflow, no activity, no queue |
| File | None |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies the DP table adds are RWB-PLT-E1043-CON with C RWB-P3-E1043-CON (DP-07), RWB-PLT-E1037-CON with C RWB-P4-E1037-CON (DP-08), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19). They are held by the service and platform stories — the parameters and reference-data contract of rwb-case, the authorise contract of rwb-access, the per-service Flyway baseline and the gateway edge — and are not repeated in the metadata columns, which stay None. DP-15 resolves to no migration, because the harness owns no schema and runs no Flyway sequence. The gate of this story is the three I stories, which replace the fakes with real behaviour; they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ProductsJourneyRunner | Test harness | Runs the seven `-ITG` cases of §16 in one run per business date, in fake or real mode per service, and stops at the first failed assertion with the trace |
| ProductsClient | Harness adapter | Calls the four consumed operations of §12.2 through one hop, as the synthetic user of the case, and records the answer |
| HoldingEventReplayer | Harness adapter | Replays the business date of `AceDataReady` and the stale holding of 2026-12-13, and reads the record on `rwb.decision-record.v1` |
| FakePack | WireMock project | Serves the owning services and the gateway-bff route of §12.8 from the published OpenAPI documents |
| SeedLoader | Service | Seeds the cases "RW-2026-000410" and "RW-2026-000420", the products "A-0411" and "A-0412", the account number "9900015678" and the role, scope and masking rule rows through the owner's contract or the fake |
| ProductAsserter | Assertion | Asserts the count, the product type, the status, the business date, the account number by role and the exclusion of "A-0410" by account key |
| StaleAsserter | Assertion | Asserts the 2026-12-13 stamp, MSG-P1-001 with product "Customer products" and date 2026-12-13, and the stale read log with "DP02" |
| RefusalAsserter | Assertion | Asserts 403 with MSG-P4-002, 404 with MSG-P4-003, 503 with MSG-GEN-006, the empty answer with MSG-P2-017, and that no product is returned in the refusal and failure states |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, so only rwb-source-data reads the ACE views |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value otherwise |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01, DP-15).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.integration.customer-products` on in both. The data are the synthetic seeds of the legacy story: case "RW-2026-000410" with borrower "C-0410" and linked account "A-0410"; the revolving credit line "A-0411" with status "ACTIVE" and the personal loan "A-0412" with status "DELINQUENT", both with data as of 2026-12-14, and the stale copy of 2026-12-13; the account number "9900015678" on "A-0411" and its masked form "XXXXXX5678"; case "RW-2026-000420" with borrower "C-0420" and no other product; the business date 2026-12-14 for the run key. Each run starts from the seeded state, so a repeated run is deterministic. The harness repository and its environments, its seeding, its evidence format and retention, its pass or fail gate and the composite route detail are Not specified in the source documents (GAP-0390; ASM-0565).

**Build steps**

1. Build ProductsJourneyRunner and ProductsClient against the published OpenAPI documents of the owning services and the gateway-bff route.
2. Publish FakePack for the four services and the composite route from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write SeedLoader and the seed files, with the run lock and the fake or real mode per service, including the fresh and the stale holding and the empty case.
4. Write ProductAsserter for AC1 and AC4, with a unit test on fixtures for the product type, the status, the business date and the account-key exclusion.
5. Write StaleAsserter for AC2, including the message id, the product "Customer products", the date 2026-12-13 and the "DP02" stale read.
6. Write RefusalAsserter for AC3, AC5 and AC6, including the masked and the clear account number on the same answer and the nothing-read rule when the access entry fails.
7. Write SchemaBoundaryCheck for AC7, and assert one hop and the 2 s timeout on every call of the run.
8. Replace each fake with the real service as its I story lands, in the order rwb-source-data, rwb-integration, rwb-case, rwb-access, and rerun in UAT.
9. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.

**Feature switch.** `rwb.integration.customer-products`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — the panel is not served and no product is returned — and that the case record is unchanged in that state.

**Done when.** The seven `-ITG` test cases of section 16 pass in SIT and UAT with the three I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the seven owned criteria green; and the stale, empty and refusal states are green with the messages of section 14.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Customer product holding older than the expected business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-017 | No other product held | The customer holds no other product with the bank in the customer product holding of {date}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |

The harness asserts the message id and the substituted values of each row — product "Customer products" and date 2026-12-13 in MSG-P1-001, the holding date in MSG-P2-017, the attempted action in MSG-P4-002 and the ACE PII logging service in MSG-GEN-006 — and never rewrites the text. Thai text for each message follows decision DL10.

### 15. Screens and states

The panel is the other-products section of SCR-03 Case record, read through the gateway-bff composite route of DP-19. The harness builds no screen and renders no page: it asserts the composite route answer the screen consumes, and the screen-level behaviour stays with RWB-P2-E2003-APP and the case-record story of the legacy key. The composite route path and merge order are Not specified in the source documents (GAP-0390; ASM-0565).

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record, other products panel | Loading | The first call of the run returns the answer of "RW-2026-000410" through the composite route, within the 2 s budget |
| SCR-03 Case record, other products panel | Filled | 2 products with their type, status, account number by role and business date 2026-12-14, and "A-0410" absent |
| SCR-03 Case record, other products panel | Stale | The 2 products with data as of 2026-12-13 and the banner message MSG-P1-001 with product "Customer products" |
| SCR-03 Case record, other products panel | Empty | The case "RW-2026-000420" returns MSG-P2-017 with no product |
| SCR-03 Case record, other products panel | Hidden by masking | RW-PHONECOL reads "XXXXXX5678" and RW-CASEOWN reads "9900015678" on the same answer |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-07-ITG | Access; ITG AC5 | Component | RW-REFADM (no Case record right) calls GET /api/recovery/integration/v1/cases/{caseId}/customer-products; refused with MSG-P4-002 |
| TC-E2-003-01-ITG | AC1, BR1, BR2, BR3; ITG AC1, ITG AC7 | Integration | Synthetic customer C-0410 with two other products in the holding of 2026-12-14 |
| TC-E2-003-02-ITG | AC2, BR3; ITG AC2, ITG AC7 | Integration | Holding last loaded 2026-12-13 |
| TC-E2-003-03-ITG | AC3, BR4; ITG AC3 | Integration | RW-PHONECOL and RW-CASEOWN read the same case with account number "9900015678" |
| TC-E2-003-04-ITG | AC4; ITG AC4 | Integration | Customer C-0420 with no other product |
| TC-E2-003-05-ITG | AC5; ITG AC5 | Integration | Case owner with scope Own and a case of another owner |
| TC-E2-003-06-ITG | AC6, BR5; ITG AC6 | NFR | PII logging stub refuses the event |

The legacy criteria stay with the app stories; this story owns none of them, and the `-ITG` cases add the seam. Each `-ITG` id keeps the legacy Covers text and its Data, appends the new criterion it proves, and runs at the level its seam needs: Component for the access case, NFR for the resilience case, Integration for the cross-service reads. The full legacy test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the product-status list, the product-group map, the party roles shown, the masking rules and the expected business date are rows held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the account number is synthetic, the answer is masked by role, and the harness stores identifiers, statuses, dates, message ids and results only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views through its own granted read (DP-05).
- No customer data is returned without its PII access entry: the harness asserts the refused read returns no product.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- The harness owns no table, no endpoint, no screen, no workflow and no schedule (DP-01, DP-15); it is test and evidence only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer and product facts from the ACE customer profile | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.3 | FEAT-CHO-03 | 06 Take over and own the case | `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` (P2) over the holding read of the rwb-source-data contract (P1) | TC-E2-003-01-ITG, TC-E2-003-02-ITG, TC-E2-003-04-ITG |
| REQ-RDF-010 | Access by role and masking under PDPA | Business Requirements Program, section 5.1; Business Requirements Epic 2, section 3.2 | FEAT-CHO-03 | 06 Take over and own the case | The rwb-access masking rule and authorise contract (DP-08) and `GET /api/recovery/access/v1/me/session` (P4) | TC-E2-003-03-ITG, TC-E2-003-06-ITG, TC-E2-003-07-ITG |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used | Business Requirements Program, section 5.1 | Not specified in the source documents (GAP-0390; ASM-0565) | 06 Take over and own the case | `GET /api/recovery/source-data/v1/data-products/freshness` (P1) and the DP02 stale read log | TC-E2-003-01-ITG, TC-E2-003-02-ITG |
| REQ-CHO-010 | A duplicate case for the same customer and product merges into the earlier case, carrying its documents and decision log | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.3 | Not specified in the source documents (GAP-0390; ASM-0565) | 06 Take over and own the case | None (out of scope, section 19) | None (out of scope, section 19) |

The two requirements the legacy story tabulates keep their legacy BRD section and feature text, with the feature of REQ-RDF-009 and REQ-CHO-010 missing from every source read. REQ-CHO-010 is traced for completeness only and is out of scope for this story.

### 19. Out of scope

- The three owning I stories and everything they build: RWB-P1-E1069-APP (the read-only ACE view contract and the granted `recovery.v_ace_party_product` read), RWB-P2-E2003-APP (the other-products read and the customer-products operation) and RWB-P4-E2003-APP (the rights, scope and masking check).
- The app criteria of the legacy key RWB-E2-003, which stay with the app stories; this story owns none of them and asserts the seams only.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-source-data, rwb-integration, rwb-case and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Masking rule maintenance, which is RWB-E1-037 and the owner of the `masking_rule` rows.
- The neighbouring integration stories of the same wave: RWB-E2-001 (the EFS hand-over), RWB-E2-002 (the ACE plan status) and RWB-E2-016 (the full case record view).
- Merging a duplicate case for the same customer and product (R-UNI-17, REQ-CHO-010): Epic 3 backlog.
- Balances of the other products: the holding carries the product type and status only (DL20).
