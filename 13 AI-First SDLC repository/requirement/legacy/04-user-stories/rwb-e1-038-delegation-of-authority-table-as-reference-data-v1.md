<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 038 Delegation of authority table as reference data v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 038 Delegation of authority table as reference data v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-038 Delegation of authority table as reference data

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-038 |
| Epic | E1, release 30 November 2026 |
| Module | P4 Access and administration |
| Feature | FEAT-ACA-06 Hold the delegation of authority table as reference data; FEAT-APD-10 Apply the delegation of authority limits |
| Requirement IDs | REQ-ACA-004, REQ-APD-010 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Epic 2, section 3.7 (REQ-APD-010); Business Requirements Program, sections 5.4 and 5.7 |
| L3 process | 17 Run the decision center |
| Decision | D6.4 to D6.6, D7.1 |
| Priority | Must |
| Depends on | RWB-E1-043, RWB-E1-029, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **Risk and model risk officer (RW-RISK)**, I want **the delegation of authority (which approval level may approve which decision, by product, principal amount and second condition) held as a versioned table that the approval router reads**, so that **approval limits change by an approved data load and every approval can be checked against the limit that applied on its date**.

## 2. Business rationale

Approval and authority governance is an audit finding, and limits today sit in the bank regulation and in people's heads. This story loads the 95 limits of Regulation กกค.540031 as amended by กกค.690070 (chapter 2 for problem loans, chapter 3 for assets held for sale) as versioned rows, and gives the approval router one lookup that returns the lowest approval level whose limit covers a decision, with the version used. It meets REQ-ACA-004 and REQ-APD-010 and is the data behind control CTL-04. The measure is decisions within the delegation of authority: target 100 percent (FSD P7 A2.1).

## 3. Preconditions

- RWB-E1-043 is done: POST /admin/reference-loads validates and versions a load file.
- RWB-E1-029 is done: the rule load template and rollback by one call exist for versioned tables.
- RWB-E1-027 is done: the decision log writer is available.
- The delegation_limit table exists (RWB-E1-001).
- LOV-DECISION holds D5, D6.4, D6.5, D6.6, D7.1, D7.4, D7.5, D8.2, D8.3, D8.4, D9.2 and D9.3; LOV-APPROVAL-LEVEL holds L1 to L6; LOV-PRODUCT holds MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED.
- Parameter `rwb.refload.approver.delegation_limit=RW-RISK` is in the parameter catalog (RWB-E1-042).
- The holder and substitute of each level are not yet named (DL18); rows load with holder_user_id and substitute_user_id empty in PROD and with named test users in SIT and UAT.

## 4. Flow

1. Reference data administrator (RW-REFADM): converts the Delegation of authority matrix to the load file: one row per limit and decision code, for MORTGAGE and SSME, amounts converted from THB million to baht.
2. RW-REFADM: calls POST /admin/reference-loads with table "delegation_limit", validFrom and the version name, for example DOA-2026.11.
3. Workbench (DelegationLimitLoader): validates the file whole and stores 218 rows with status Loaded.
4. Risk and model risk officer (RW-RISK): reviews the difference report and calls POST /admin/reference-loads/{loadId}/approve.
5. Workbench: checks that the approver holds RW-RISK and did not load the file; writes one decision log entry with decision code AC-VERS and no case; sets valid_to on the rows of the previous version to the day before the new valid from; marks the new version Approved.
6. Approval router (RWB-E2-013): calls DelegationOfAuthority.lowestLevel with the decision, the regulation item (one decision code can cover several items, for example D7.5 covers items 2.1.4, 2.1.6 and 2.1.9), the product, the amounts, the conditions and the decision date.
7. Workbench (DelegationLookupService): walks levels L6 to L1 over the rows valid on that date and returns the first level with a row that covers the request, the row IDs and the version.
8. Workbench: where no row covers the request at any level, returns NOT_COVERED and raises an incident to RW-RISK naming the decision and product.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A file repeats a decision, regulation item, product, level and condition, or a level's highest principal limit falls below a lower level's | The load is refused in full; the version in force stays | MSG-P1-002 | AC4 |
| X2 | A file holds an unknown decision code, level or product, or a required field is empty | The load is refused in full | MSG-P1-002 | AC4 |
| X3 | The person who loaded the version approves it | Refused; the version stays Loaded | MSG-P7-002 | AC5 |
| X4 | A role other than RW-RISK approves | Refused with 403 | MSG-P4-002 | AC5 |
| X5 | The decision log write for the approval fails | The version is not approved | MSG-P7-003 | AC6 |
| X6 | A lookup finds no row for the decision and product, for example hire purchase before the chapter 8 limits arrive | NOT_COVERED is returned and an incident is raised to RW-RISK | MSG-P7-010 | AC7 |
| X7 | A lookup date falls on the last day of the old version or the first day of the new one | The version valid on that date is used | None | AC8 |
| X8 | A write-off is for a director, senior executive, major shareholder or related party | Level L1 is returned whatever the amount | None | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the load service (RWB-E1-043), the rule load template (RWB-E1-029) and the writer (RWB-E1-027) |
| Negotiable | Limits, holders and substitutes are data; names follow DL18 |
| Valuable | Every Epic 2 approval reads its limit from one approved table |
| Estimable | One loader, one lookup, one approval check |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Delegation of authority table as reference data

  Background:
    Given the environment is SIT
    Given test user "U-3101" holds RW-REFADM and test user "U-3102" holds RW-RISK

  Scenario: AC1 Table loaded
    Given the delegation of authority file "DOA-2026.11" built from Regulation กกค.540031 as amended by กกค.690070, with 95 limits
    When "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it
    Then the system stores 218 rows : 109 decision and limit rows for MORTGAGE and 109 for SSME
    Then every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits
    Then the system stores item 2.1.1 at level L4 as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit

  Scenario: AC2 Lookup
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026
    Then the lookup returns level L6, the row ID of item 2.1.1 at L6 and version "DOA-2026.11"

  Scenario: AC3 Change
    Given "DOA-2026.11" is in force
    Given file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01"
    When "U-3101" loads it and "U-3102" approves it
    Then the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31"
    Then a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01"
    Then one decision log entry records the approval of "DOA-2027.01" with its valid from date

  Scenario: AC4 A file with an error is refused in full
    Given file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4
    Given it gives one row the decision code "D6.9"
    When "U-3101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the falling limit and the unknown decision code
    Then the system stores no row of "DOA-2026.12" and "DOA-2026.11" stays in force

  Scenario: AC5 The loader cannot approve and only Risk may
    Given load "DOA-2027.01" was loaded by "U-3101"
    When "U-3101" calls approve on it
    Then the system refuses the call with message MSG-P7-002
    Then when test user "U-3103" holding RW-PRODHEAD calls approve on it
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC6 An approval that cannot be recorded does not take effect
    Given the decision log store is unavailable
    When "U-3102" approves load "DOA-2027.01"
    Then the call returns status 503 with message MSG-P7-003 and the load stays "Loaded"

  Scenario: AC7 No limit covers the request
    Given "DOA-2026.11" holds no row for product HIRE_PURCHASE
    When the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00
    Then the lookup returns "NOT_COVERED"
    Then the system raises an incident to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE

  Scenario: AC8 The version valid on the decision date is used
    Given "DOA-2026.11" is valid to 31 December 2026 and "DOA-2027.01" from 1 January 2027
    When the router looks up D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 31 December 2026 and again dated 1 January 2027
    Then the first lookup returns L4 and "DOA-2026.11"
    Then the second returns L5 and "DOA-2027.01"

  Scenario: AC9 A write-off for a related party goes to the Board
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true
    Then the lookup returns level L1 with reason "RELATED_PARTY"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Limits are held as the regulation states them: principal limit in baht, loss as a percentage, maximum loss in baht, payment or price against fair market value, and price against principal outstanding; an empty limit means no limit | delegation_limit fields DF-REF-020 to DF-REF-022; Delegation of authority matrix, Key sheet |
| BR2 | Where a level has two rows, the approval is within limit if either row is met | Delegation of authority matrix, How it applies, rule 3 |
| BR3 | The lowest level, from L6 up to L1, with a row for the decision code and regulation item valid on the decision date that covers the request is the level returned | LOV-APPROVAL-LEVEL; FEAT-APD-10 |
| BR4 | A decision that no limit covers goes to the next level up; a decision and product with no row at any level returns NOT_COVERED and raises an incident | Delegation of authority matrix, How it applies, rule 8 |
| BR5 | A write-off for a director, senior executive, major shareholder or related party goes to the Board (L1) | Delegation of authority matrix, How it applies, rule 6 |
| BR6 | A delay of legal action, of seizure or of an auction is within a level's limit only while the count of delays on the case, including this one, is not above the level's delay count | Delegation of authority matrix, How it applies, rule 4; items 2.1.3 and 2.1.6 |
| BR7 | A decision keeps the version it was approved under; a new version applies from its valid from date | Delegation of authority matrix, How it applies, rule 9; R-UNI-38; REQ-APD-010 |
| BR8 | A limit change is a data load approved by Risk, never by its loader | Delegation of authority matrix, How it applies, rule 11; CTL-08; separation of duty, reference data administrator and Risk |
| BR9 | Hire purchase and unsecured limits follow chapter 8 of credit approval regulation รบ.-กส.450032 and load when supplied | Delegation of authority matrix, How it applies, rule 7; DL18 |
| BR10 | A version approval that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |

## 9. State transitions

None. This story does not change a case status. It moves a delegation version from Loaded to Approved (or Refused at validation) and closes the previous version with a valid_to date.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM Reference data administrator | Prepares and loads a delegation version (Reference data C). Approves none |
| RW-RISK Risk and model risk officer | Approves a delegation version (approver role for the table) |
| RW-PRODHEAD Product head | Agrees the limits for their product with Risk before the load; may not approve the load |
| Risk with the product heads | Name the holder and substitute of each level (DL18) |
| Approval levels L1 to L6 | Board of Directors, Executive Committee, Problem Asset Resolution Committee or Management Committee, Head of Recovery at function level, Recovery executive at division level, Recovery executive at department level (doa.txt, Levels sheet). Levels L1 to L3 approve by committee resolution recorded in the decision log; L4 to L6 approve in the Workbench |
| SY-RULES Rules component | Calls the lookup for the approval router |
| RW-AUDIT Internal audit | Reads every version and its approval entry |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-016 to DF-REF-026 | delegation_limit | all fields | Write (rows of each new version); read by the lookup |
| DF-REF-055 | delegation_limit | limit_version | Write, read |
| DF-REF-056 | delegation_limit | regulation_item | Write, read |
| DF-REF-057 | delegation_limit | applies_when | Write, read |
| DF-REF-058 | delegation_limit | max_loss_amount | Write, read |
| DF-REF-059 | delegation_limit | max_delay_count | Write, read |
| DF-REF-060 | delegation_limit | min_price_pct_principal | Write, read |
| DF-REF-061 | delegation_limit | min_received_pct | Write, read |
| DF-REF-062 | delegation_limit | max_term_years | Write, read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per approved version) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005)

| Item | Value |
|---|---|
| Request | Multipart: file, table "delegation_limit", validFrom |
| Response | 201 ReferenceLoad: id, table, validFrom, status "Loaded", rows |
| Errors | 401; 403 no Reference data C (MSG-P4-002); 409 version name exists (MSG-GEN-004); 422 validation failed (MSG-P1-002); 503 (MSG-GEN-006) |
| Authorization | Reference data, right C |
| Idempotency | Idempotency-Key header |

**POST /admin/reference-loads/{loadId}/approve** (API-P4-006)

| Item | Value |
|---|---|
| Request | None |
| Response | 200 ReferenceLoad with status "Approved" |
| Errors | 401; 403 caller is not RW-RISK (MSG-P4-002); 404 (MSG-P4-003); 409 caller loaded it (MSG-P7-002) or load not "Loaded" (MSG-GEN-004); 503 decision log write failed (MSG-P7-003) |
| Authorization | api.yaml declares Reference data A, which no role holds; the approver role for the table (RW-RISK, parameter) is checked instead, as recorded in the additions file |
| Idempotency | Idempotency-Key header |

**Published interface DelegationOfAuthority** (package recovery.access.delegation):

```java
DelegationResult lowestLevel(DelegationRequest request);
// DelegationRequest: decisionCode, regulationItem, productGroup, appliesWhen, principal (BigDecimal, baht), lossPct, lossAmount,
//   pricePctFmv, pricePctPrincipal, receivedPct, delayCount, termYears, relatedParty, decisionDate (LocalDate)
// DelegationResult: status COVERED | NOT_COVERED, approvalLevel, rowIds, limitVersion, reason, holderUserId, substituteUserId
```

## 13. Solution plan

- Package: folder `recovery/access/delegation` in the recovery module; Java package `recovery.access.delegation`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | Reference load and approve for table delegation_limit |
| DelegationLimitLoader | Service | Validates the file whole: known codes, required fields, no repeated rows, highest principal limit per level does not fall from L6 to L1 |
| ReferenceLoadApprovalService | Service | Shared with RWB-E1-037: approver role, maker and checker, decision log write, closing the previous version |
| DelegationLookupService | Published interface | Implements DelegationOfAuthority.lowestLevel |
| DelegationLimitRepository | Repository | Reads rows valid on a date for a decision code, regulation item, product and applies_when |
| DelegationLimit | Entity | Maps delegation_limit with the new columns |

- Database: writes delegation_limit (decision_code, approval_level, product_group, principal_limit, loss_pct_limit, min_price_pct_fmv, holder_user_id, substitute_user_id, valid_from, valid_to). Flyway migration V_E1_038__delegation_limit_columns.sql adds limit_version varchar(20) not null, regulation_item varchar(10) not null, applies_when varchar(40), max_loss_amount numeric(18,2), max_delay_count integer, min_price_pct_principal numeric(5,2), min_received_pct numeric(5,2), max_term_years numeric(4,1); index ix_delegation_lookup on (decision_code, regulation_item, product_group, approval_level, valid_from) where is_active.
- Configuration and reference data: DOA-2026.11 (RW-REFADM loads, RW-RISK approves); LOV-DECISION, LOV-APPROVAL-LEVEL, LOV-PRODUCT; applies_when values WO_CRITERIA_MET and WO_CRITERIA_NOT_MET for the two write-off rows of item 2.1.10, loaded with the version; parameter rwb.refload.approver.delegation_limit. Holders and substitutes per DL18.
- Build steps:
  1. Write the migration for the new columns and the lookup index.
  2. Build the converter template: one matrix row and decision code per load row, THB million to baht, "No limit" to empty, "Up to X%" to loss_pct_limit, "At least X%" against fair market value to min_price_pct_fmv, "Once" and "Twice" to max_delay_count.
  3. Build DelegationLimitLoader with whole-file validation; tests for AC1 and AC4.
  4. Reuse ReferenceLoadApprovalService with the RW-RISK approver parameter; tests for AC5 and AC6.
  5. Build DelegationLookupService: rows valid on the date, levels L6 to L1, either-row rule, related party rule, delay count rule; tests for AC2, AC8 and AC9.
  6. Raise the NOT_COVERED incident through the ACE incident path; test for AC7.
  7. Test version change and boundary dates for AC3 and AC8.
- Feature flag: `rwb.access.delegation-table`.
- Done when: the tests in section 16 pass and the 218 rows of DOA-2026.11 reconcile to the 95 limits in the matrix in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The delegation file fails validation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The loader approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role other than RW-RISK approves | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The approval cannot be written to the decision log | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-010 | No limit covers a decision and product (new) | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |
| MSG-GEN-004 | A second approve of an approved load | Someone else changed this record. Reload it to see their change. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-010 is in the additions file.

## 15. Screens and states

No screen in this story. Delegation versions arrive by file load until SCR-41 Delegation of authority comes in Epic 8. RW-RISK sees the difference report returned by the load and the approval result.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-038-01 | AC1, BR1, BR2 | System | Delegation file DOA-2026.11 from the 95 matrix limits |
| TC-E1-038-02 | AC2, BR3 | System | D6.4 Mortgage request at 2.4 million baht principal and 20 percent loss |
| TC-E1-038-03 | AC3, BR7 | System | Versions DOA-2026.11 and DOA-2027.01 |
| TC-E1-038-04 | AC4, BR1 | System | File with a falling limit and an unknown decision code |
| TC-E1-038-05 | AC5, BR8 | System | Approve by the loader, then by RW-PRODHEAD |
| TC-E1-038-06 | AC6, BR10 | System | Decision log store switched off in the test double |
| TC-E1-038-07 | AC7, BR4, BR9 | System | Hire purchase request with no rows |
| TC-E1-038-08 | AC8, BR7 | System | Lookups on 31 December 2026 and 1 January 2027 |
| TC-E1-038-09 | AC9, BR5 | System | D9.2 request with the related party flag |
| TC-E1-038-10 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E1-038-11 | Principle 5 | Resilience | The decision log write forced to fail during an approval |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: levels, limits, conditions, products and the approver role are data.
- No personal data in logs, tests or prompts; holders are test user references in SIT and UAT.
- No read of another module's tables; the router calls the published interface.
- No limit is converted or rounded at lookup time; amounts are stored in baht with two decimals.
- A version already approved is never edited; a change is a new version.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-004 | Delegation of authority table as reference data, setting every limit | Epic 1, 3.4 | FEAT-ACA-06 | 17 Run the decision center | BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10 | TC-E1-038-01, TC-E1-038-02, TC-E1-038-04, TC-E1-038-05, TC-E1-038-06, TC-E1-038-07, TC-E1-038-09 |
| REQ-APD-010 | Delegation changes versioned, approved and dated; open items keep their version | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR7 | TC-E1-038-03, TC-E1-038-08 |

## 19. Out of scope

- Routing an approval to the holder of the level, the queue and escalation (RWB-E2-013).
- Names of holders and substitutes, and the chapter 8 limits for hire purchase and unsecured loans (Risk with the product heads, DL18).
- The rule that new credit to a problem loan takes the higher of the restructuring and credit authorities (Epic 3 restructure stories).
- The Delegation of authority screen SCR-41 and moving a limit through screens (Epic 8, FEAT-ADM-03).
