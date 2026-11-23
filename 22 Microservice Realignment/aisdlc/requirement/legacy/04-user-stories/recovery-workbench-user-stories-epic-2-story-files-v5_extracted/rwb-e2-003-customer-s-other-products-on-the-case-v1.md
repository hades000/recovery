<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 003 Customer s other products on the case v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 003 Customer s other products on the case v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-003 Customer's other products on the case

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-003 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-03 Read customer facts from ACE |
| Requirement IDs | REQ-CHO-003, REQ-RDF-010 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-069, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the customer's other products and their status on the case, read from the product holding ACE holds for each person**, so that **I can see the whole relationship before I decide a route**.

## 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. ACE holds the customer product holding it receives from SCBPDM (DL20, INT-04), keyed by person_key. This story reads v_ace_party_product for the borrowers and co-borrowers of the case, shows each product with its status and business date, marks the list stale when the holding is older than the expected business date, and masks account numbers by role. Nothing is copied into a Workbench table; the view is the record. It meets REQ-CHO-003 and REQ-RDF-010.

## 3. Preconditions

- RWB-E1-069 (read-only ACE source views, grants and boundary rule) and RWB-E1-007 (adapters) are done; the case record view (SCR-03) is in production from Epic 1.
- v_ace_party_product ships in V0003, the Section B migration of RWB-ACE-001 (DL43); the feature stays behind its flag until V0003 is applied in the environment.
- v_ace_customer and v_ace_contact are granted SELECT to the recovery service identity.
- The masking rules for v_ace_party_product.account_no are loaded (DL26; assumed: unmasked for RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, masked to the last four digits for every other role).
- The list LOV-PRODUCT-STATUS is loaded (values: ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF).
- The ACE PII logging service is available.

## 4. Flow

1. Case owner: opens SCR-03 Case record for a case in scope.
2. Front end: calls GET /cases/{caseId}/customer-products (API-P2-011).
3. System: checks the Case record right and the scope of the case.
4. System: reads the borrower and co-borrower parties of the case through the P3 CaseQuery.
5. System: reads each person's rows from v_ace_party_product by person_key through the P2 CustomerProductsReader, excluding the account_key values already linked to the case.
6. System: compares data_as_of of the holding with the expected business date of DP02; if older, sets the stale marker.
7. System: applies the masking rule for the caller's role to each account_no.
8. System: writes one PII access event (user, case, person keys, fields shown) through the ACE PII logging service.
9. Front end: shows each product with product type, masked or clear account number, status and business date; a stale list shows MSG-P1-001.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The customer product holding is older than the expected business date | The last loaded products show with a stale marker; a stale read is logged | MSG-P1-001 | AC2 |
| X2 | The caller's role is not allowed to see account numbers | Account numbers are masked to the last four digits | None | AC3 |
| X3 | The customer holds no other product | An empty list shows | MSG-P2-017 | AC4 |
| X4 | The case is outside the caller's scope | Refused | MSG-P4-003 | AC5 |
| X5 | The PII access log cannot be written | The products are not returned; the request fails | MSG-GEN-006 | AC6 |
| X6 | A role without the Case record right calls the endpoint | Refused; nothing is shown | MSG-P4-002 | TC-E2-003-07 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ACE views (RWB-E1-069) and the case record view; no other Epic 2 story |
| Negotiable | Masking, product status codes and the parties shown are data rows |
| Valuable | The case owner sees the relationship without a lookup in another system |
| Estimable | One read service, one endpoint, one React panel, one view |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case

  Background:
    Given case "RW-2026-000410" has borrower "C-0410" and linked synthetic account "A-0410"
    Given the expected business date of the customer product holding is 2026-12-14

  Scenario: AC1 Other products shown
    Given "C-0410" holds a revolving credit line "A-0411" with status "ACTIVE" and a personal loan "A-0412" with status "DELINQUENT" in v_ace_party_product, both with data as of 2026-12-14
    When the case record view loads for a case owner
    Then the other products panel shows 2 products with their type and status
    Then each product shows the business date 2026-12-14
    Then the system does not list account "A-0410" because its account_key is on the case

  Scenario: AC2 Holding older than the business date
    Given v_ace_party_product holds no row for 2026-12-14 and its last rows are for 2026-12-13
    When the view loads
    Then the 2 products show with data as of 2026-12-13
    Then the panel shows message MSG-P1-001 with product "Customer products" and date 2026-12-13
    Then the system logs a stale read event with the case ID and the data product "DP02"

  Scenario: AC3 Masking
    Given a phone collector (RW-PHONECOL) with the case in scope
    Given product "A-0411" has synthetic account number "9900015678"
    When the view loads
    Then the other products show with the account number "XXXXXX5678"
    Then a case owner sees "9900015678"

  Scenario: AC4 No other products
    Given borrower "C-0420" of case "RW-2026-000420" holds no product other than the case account
    When the view loads
    Then the panel shows an empty list with message MSG-P2-017

  Scenario: AC5 Case outside the scope
    Given a case owner with scope "Own" and case "RW-2026-000410" owned by another person
    When the case owner calls GET /cases/{caseId}/customer-products
    Then the response is 404 with message MSG-P4-003

  Scenario: AC6 PII access log unavailable
    Given the ACE PII logging service does not accept the access event
    When the view loads
    Then the system returns no product
    Then the response is 503 with message MSG-GEN-006
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Customer product facts are read from v_ace_party_product, which ACE holds from SCBPDM | DL20; INT-04; RWB-ACE-001 |
| BR2 | Products of every party with role borrower or co-borrower on the case are shown, except accounts already on the case, matched on account_key | LOV-PARTY-ROLE; story intent |
| BR3 | Each product shows the business date of its holding; a holding older than the expected business date shows as stale | REQ-RDF-009; VR-P2-001-1 |
| BR4 | Account numbers are masked by role on the masking rules | REQ-RDF-010; CTL-11; DL26 |
| BR5 | Every read of customer data is logged to the PII log with who, what, when and which record | INT-22; REQ-RDF-010 |
| BR6 | Product status codes are those in LOV-PRODUCT-STATUS; an unknown code is held on the data quality break list | DQ-020, DQ-027 Lists of values |
| BR7 | The products are not copied into a Workbench table; the view is read on each request | D-RCV-35 U1; tier map section 9.1 |

## 9. State transitions

None. This story does not change a case status. It reads only; the PII access log receives one event per read.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads other products on cases in scope, account numbers clear (Case record, R) |
| RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Read other products on cases in scope, account numbers clear (assumed; DL26) |
| RW-PHONECOL, RW-CONDUCT and other roles with Case record R | Read other products on cases in scope, account numbers masked |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rule rows |
| The recovery service identity | Reads v_ace_party_product for the endpoint (Case record, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-004 | recovery_case | primary_person_key | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | person_key | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-280 | v_ace_party_product | person_key | Read |
| DF-ACE-281 | v_ace_party_product | account_no | Read |
| DF-ACE-282 | v_ace_party_product | account_key | Read |
| DF-ACE-283 | v_ace_party_product | product_type | Read |
| DF-ACE-284 | v_ace_party_product | product_status | Read |
| DF-ACE-285 | v_ace_party_product | data_as_of | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. v_ace_party_product is read through the P2 CustomerProductsReader, never from a public table.

## 12. Contract

**Endpoint (API-P2-011).**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /cases/{caseId}/customer-products | Path: caseId | CustomerProducts: dataAsOf, stale, messageCode, items (personKey, partyRole, productType, accountNo masked by role, productStatus, dataAsOf) | 401 (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 PII log unavailable (MSG-GEN-006) | Case record, R | Read only |

**Published interfaces called.**

```java
// P2 recovery.integration.ace, reads recovery.v_ace_party_product
List<PartyProductView> CustomerProductsReader.otherProducts(List<String> personKeys, Set<String> excludeAccountKeys);
// P1 recovery.data.api
DataProductFreshness DataProductStatus.freshness(String dataProduct); // dataAsOf, expectedBusinessDate, stale
// P3 recovery.casewf.api
List<CasePartyView> CaseQuery.partiesOf(UUID caseId, Set<String> partyRoles);
// ACE common module
void PiiAccessLog.write(PiiAccessEvent event); // throws PiiLogUnavailableException
String Masking.apply(String field, String value, Set<String> roleCodes);
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/customer`, Java package `recovery.integration.customer`; front end `src/modules/recovery/case/OtherProductsPanel.tsx`.

| Component | Type | Responsibility |
|---|---|---|
| CustomerProductsController | Controller | GET /cases/{caseId}/customer-products with the scope check |
| CustomerProductsService | Service | Parties, products, freshness, masking, PII log, response |
| CustomerProductsReader | Repository | Read-only select from v_ace_party_product by person_key; no other ACE access |
| OtherProductsPanel | React component | List with product type, account number, status, date; stale banner MSG-P1-001; empty state MSG-P2-017 |

- **Database:** no new table. The product holding stays in ACE and is read through v_ace_party_product; no copy is written to the recovery schema.
- **Configuration and reference data:** masking rule rows for v_ace_party_product.account_no (RW-COMPLY, DL26); LOV-PRODUCT-STATUS (RW-DATASTEW); party roles shown, BORROWER and CO_BORROWER, as a property `rwb.customer.products.party-roles`.
- **Build steps:**
  1. Agree the PartyProductView and the reader with the P2 squad; build a stub of v_ace_party_product for tests.
  2. Build CustomerProductsService with party selection and exclusion of case accounts by account_key.
  3. Add the freshness check and the stale marker.
  4. Add masking through the ACE Masking service and the PII access event; fail the call when the log fails.
  5. Build the endpoint with the access and scope checks.
  6. Build OtherProductsPanel with its loading, list, stale and empty states.
- **Feature flag:** `rwb.integration.customer-products`.
- **Done when:** the tests in section 16 pass and the panel shows synthetic products in SIT with masking for RW-PHONECOL.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Customer product holding older than the expected business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-017 | No other product held | The customer holds no other product with the bank in the customer product holding of {date}. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | PII access log unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-03 Case record, states loading and read only: the other products panel shows the list, a stale banner when the holding is older than the expected business date, and an empty state when there is none. A role with masking sees account numbers masked to the last four digits.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-01 | AC1, BR1, BR2, BR3 | System | Synthetic customer C-0410 with two other products in v_ace_party_product |
| TC-E2-003-02 | AC2, BR3 | System | Holding last loaded 2026-12-13 |
| TC-E2-003-03 | AC3, BR4 | System | RW-PHONECOL and RW-CASEOWN read the same case |
| TC-E2-003-04 | AC4 | System | Customer C-0420 with no other product |
| TC-E2-003-05 | AC5 | System | Case owner with scope Own and a case of another owner |
| TC-E2-003-06 | AC6, BR5 | Resilience | PII logging stub refuses the event |
| TC-E2-003-07 | Access | Access | RW-REFADM (no Case record right) calls GET /cases/{caseId}/customer-products; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: masking, product status codes and the party roles shown are rows or properties.
- No personal data in logs, tests or prompts; test data is synthetic, application logs hold case and person keys only.
- No read of another module's tables: v_ace_party_product and v_ace_customer are read through the reader over the views; parties through the P3 interface.
- No customer data is returned without its PII access event.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer and product facts from the ACE customer profile | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-01, TC-E2-003-02, TC-E2-003-04, TC-E2-003-05 |
| REQ-RDF-010 | Access by role and masking under PDPA | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | None | TC-E2-003-03, TC-E2-003-06 |

## 19. Out of scope

- Merging a duplicate case for the same customer and product (R-UNI-17, REQ-CHO-010): Epic 3 backlog.
- The role to masking rule table: RWB-E1-037.
- Balances of the other products: v_ace_party_product carries the product type and status only (DL20).
