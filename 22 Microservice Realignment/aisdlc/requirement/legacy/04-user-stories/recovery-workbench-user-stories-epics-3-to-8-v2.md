<!-- source: 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v2.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v2.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench user stories, Epics 3 to 8

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Epic | Stories | Status |
|---|---|---|
| E3 | 31 | Ready for refinement |
| E4 | 50 | Draft; refined one epic ahead |
| E5 | 26 | Draft; refined one epic ahead |
| E6 | 37 | Draft; refined one epic ahead |
| E7 | 18 | Draft; refined one epic ahead |
| E8 | 19 | Draft; refined one epic ahead |

One story per feature in the Epic 3 to 8 scope. Each carries its acceptance criteria, data, endpoints, screens, permission checks, messages and test cases. The squads size each story when it is refined; dependencies name features until the story keys are set.

---

## RWB-E4-001 Order an appraisal when the last one is stale

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-01 Order an appraisal when the last one is stale |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-RDF-06 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to check the appraisal age against the limit and raise the order to SVAF with no person involved, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Order an appraisal when the last one is stale

  Scenario: AC1 Order an appraisal when the last one is stale
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then checks the appraisal age against the limit and raises the order to SVAF with no person involved
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-001-01 | AC1 | Order an appraisal when the last one is stale |
| TC-E4-001-02 | AC2 | Not recorded |
| TC-E4-001-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-001-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-002 Receive the appraisal value from SVAF

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-02 Receive the appraisal value from SVAF |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-01 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to take the value, date and appraiser back from SVAF onto the collateral record, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Receive the appraisal value from SVAF

  Scenario: AC1 Receive the appraisal value from SVAF
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes the value, date and appraiser back from SVAF onto the collateral record
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-002-01 | AC1 | Receive the appraisal value from SVAF |
| TC-E4-002-02 | AC2 | Not recorded |
| TC-E4-002-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-002-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-003 Flag appraisal outliers against market and last value

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-03 Flag appraisal outliers against market and last value |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-02 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to compare the new value to the market and the previous value and flag the gap for a person, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Flag appraisal outliers against market and last value

  Scenario: AC1 Flag appraisal outliers against market and last value
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then compares the new value to the market and the previous value and flags the gap for a person
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-003-01 | AC1 | Flag appraisal outliers against market and last value |
| TC-E4-003-02 | AC2 | Not recorded |
| TC-E4-003-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-003-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-004 Accept the appraisal value

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-04 Accept the appraisal value |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-03 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to let the case owner accept the value, which fixes the band the route decision runs on, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Accept the appraisal value

  Scenario: AC1 Accept the appraisal value
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the case owner accept the value, which fixes the band the route decision runs on
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-004-01 | AC1 | Accept the appraisal value |
| TC-E4-004-02 | AC2 | Not recorded |
| TC-E4-004-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-004-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-005 Call COLLINS for return by route

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-05 Call COLLINS for return by route |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AGT-01 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to ask the COLLINS model for the expected return on each route and record the answer with its version, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Call COLLINS for return by route

  Scenario: AC1 Call COLLINS for return by route
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then asks the COLLINS model for the expected return on each route and records the answer with its version
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-005-01 | AC1 | Call COLLINS for return by route |
| TC-E4-005-02 | AC2 | Not recorded |
| TC-E4-005-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-005-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-006 Calculate the payoff and settlement range

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-06 Calculate the payoff and settlement range |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DRI-07 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to work out the payoff from ALS and the settlement range from the rules, with the floor applied, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Calculate the payoff and settlement range

  Scenario: AC1 Calculate the payoff and settlement range
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then works out the payoff from ALS and the settlement range from the rules, with the floor applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-006-01 | AC1 | Calculate the payoff and settlement range |
| TC-E4-006-02 | AC2 | Not recorded |
| TC-E4-006-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-006-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-007 Score the routes and recommend one with reasons

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-07 Score the routes and recommend one with reasons |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-05, FEAT-VAL-06 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to run the route agent, which recommends a route and states the reasons and the alternatives, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Score the routes and recommend one with reasons

  Scenario: AC1 Score the routes and recommend one with reasons
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the route agent, which recommends a route and states the reasons and the alternatives
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-007-01 | AC1 | Score the routes and recommend one with reasons |
| TC-E4-007-02 | AC2 | Not recorded |
| TC-E4-007-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-007-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-008 Approve a route inside the limit

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-08 Approve a route inside the limit |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-02, FEAT-VAL-07 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to let the case owner approve the recommended route within their delegated limit, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Approve a route inside the limit

  Scenario: AC1 Approve a route inside the limit
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the case owner approve the recommended route within their delegated limit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-008-01 | AC1 | Approve a route inside the limit |
| TC-E4-008-02 | AC2 | Not recorded |
| TC-E4-008-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-008-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-009 Approve a route above the limit at committee

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-09 Approve a route above the limit at committee |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-05 |
| Decision | None |

**Story.** As the Credit approval committee member, I want to take the route to the credit committee when it is beyond the case owner's limit, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Approve a route above the limit at committee

  Scenario: AC1 Approve a route above the limit at committee
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the route to the credit committee when it is beyond the case owner's limit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-009-01 | AC1 | Approve a route above the limit at committee |
| TC-E4-009-02 | AC2 | Not recorded |
| TC-E4-009-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-009-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-010 Hold the case and set a review date

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-10 Hold the case and set a review date |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CWC-11 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to let the owner hold a case where no route is right yet, with a date the hold is reviewed, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Hold the case and set a review date

  Scenario: AC1 Hold the case and set a review date
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the owner hold a case where no route is right yet, with a date the hold is reviewed
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-010-01 | AC1 | Hold the case and set a review date |
| TC-E4-010-02 | AC2 | Not recorded |
| TC-E4-010-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-010-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-011 Reconsider the route after new information

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-11 Reconsider the route after new information |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-07 |
| Decision | None |

**Story.** As a case owner, I want to reopen the route decision when a value, a payment or a deviation changes the picture, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Reconsider the route after new information

  Scenario: AC1 Reconsider the route after new information
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then reopens the route decision when a value, a payment or a deviation changes the picture
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-011-01 | AC1 | Reconsider the route after new information |
| TC-E4-011-02 | AC2 | Not recorded |
| TC-E4-011-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-011-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-012 Start the route flow and set its timers

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Feature | FEAT-VAL-12 Start the route flow and set its timers |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-08 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to open the chosen route, create its tasks and start its clocks, so that the route is chosen on expected return with reasons.

**Acceptance criteria**

```gherkin
Feature: Start the route flow and set its timers

  Scenario: AC1 Start the route flow and set its timers
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then opens the chosen route, creates its tasks and starts its clocks
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/route | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-012-01 | AC1 | Start the route flow and set its timers |
| TC-E4-012-02 | AC2 | Not recorded |
| TC-E4-012-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-012-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-001 Create the treatment record

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-01 Create the treatment record |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CHO-06 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to open the treatment for the chosen route, holding the terms, the approval and the outcome, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Create the treatment record

  Scenario: AC1 Create the treatment record
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then opens the treatment for the chosen route, holding the terms, the approval and the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-01
    Given a case in state ROUTE_APPROVED_RESTRUCTURE
    When route approved
    Then open the treatment record and ask COLLINS for the restructure proposal
    Then the case moves to PROPOSED_IN_COLLINS

  Scenario: AC3 Rule R-RES-10
    Given a case in state WITH_FCR_OFFICER
    When offer prepared
    Then route the offer to credit approval; 44% of TDR cases deviate today
    Then the case moves to AWAITING_CREDIT_APPROVAL

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-001-01 | AC1 | Create the treatment record |
| TC-E3-001-02 | AC2 | Rule R-RES-01 |
| TC-E3-001-03 | AC3 | Rule R-RES-10 |
| TC-E3-001-04 | AC4 | Not recorded |
| TC-E3-001-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-001-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-002 Offer a settlement inside the range

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-02 Offer a settlement inside the range |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-01, FEAT-VAL-06 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to let the officer build and send a settlement offer within the calculated range, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Offer a settlement inside the range

  Scenario: AC1 Offer a settlement inside the range
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the officer build and send a settlement offer within the calculated range
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-07
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-04
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-002-01 | AC1 | Offer a settlement inside the range |
| TC-E3-002-02 | AC2 | Rule R-RES-07 |
| TC-E3-002-03 | AC3 | Rule R-RES-04 |
| TC-E3-002-04 | AC4 | Not recorded |
| TC-E3-002-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-002-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-003 Approve a settlement below the floor

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-03 Approve a settlement below the floor |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As a product head (Mortgage, HP, SSME), I want to route a settlement below the floor price to the approver or the committee named in the matrix, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Approve a settlement below the floor

  Scenario: AC1 Approve a settlement below the floor
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then routes a settlement below the floor price to the approver or the committee named in the matrix
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-15
    Given a case in state TRANSFER_PRICE_SET
    When price below floor
    Then route the price for a second signature
    Then the case moves to AWAITING_SECOND_SIGNATURE

  Scenario: AC3 Rule R-DIL-17
    Given a case in state AWAITING_SECOND_SIGNATURE
    When second signature refused
    Then return the case to the route decision with reason price_below_floor
    Then the case moves to RETURNED_TO_ROUTE_DIL

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-003-01 | AC1 | Approve a settlement below the floor |
| TC-E3-003-02 | AC2 | Rule R-DIL-15 |
| TC-E3-003-03 | AC3 | Rule R-DIL-17 |
| TC-E3-003-04 | AC4 | Not recorded |
| TC-E3-003-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-003-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-004 Offer a TDR plan

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-04 Offer a TDR plan |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-01 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to let the restructuring officer build and send the plan offer, with the band and the rule version applied, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Offer a TDR plan

  Scenario: AC1 Offer a TDR plan
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the restructuring officer build and send the plan offer, with the band and the rule version applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-04
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-07
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-004-01 | AC1 | Offer a TDR plan |
| TC-E3-004-02 | AC2 | Rule R-RES-04 |
| TC-E3-004-03 | AC3 | Rule R-RES-07 |
| TC-E3-004-04 | AC4 | Not recorded |
| TC-E3-004-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-004-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-005 Pre-assess affordability through ACE

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-05 Pre-assess affordability through ACE |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CHO-02 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to call the ACE affordability calculation and record the result against the offer, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Pre-assess affordability through ACE

  Scenario: AC1 Pre-assess affordability through ACE
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then calls the ACE affordability calculation and records the result against the offer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-06
    Given a case in state WITH_FCR_OFFICER
    When affordability required
    Then send the case to ACE for affordability and plan calculation
    Then the case moves to AFFORDABILITY_IN_ACE

  Scenario: AC3 Rule R-RES-07
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-005-01 | AC1 | Pre-assess affordability through ACE |
| TC-E3-005-02 | AC2 | Rule R-RES-06 |
| TC-E3-005-03 | AC3 | Rule R-RES-07 |
| TC-E3-005-04 | AC4 | Not recorded |
| TC-E3-005-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-005-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-006 Calculate the plan installment

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-06 Calculate the plan installment |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-05 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to produce the model installment and the range the officer may move within, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Calculate the plan installment

  Scenario: AC1 Calculate the plan installment
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the model installment and the range the officer may move within
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-SET-01
    Given a case in state ROUTE_APPROVED_SETTLEMENT
    When route approved
    Then calculate the payoff from ALS and set the range from reference data
    Then the case moves to PAYOFF_AND_RANGE_SET

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-006-01 | AC1 | Calculate the plan installment |
| TC-E3-006-02 | AC2 | Rule R-SET-01 |
| TC-E3-006-03 | AC3 | Not recorded |
| TC-E3-006-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-006-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-007 Send the offer and start the validity timer

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-07 Send the offer and start the validity timer |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-01, FEAT-TRT-04 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to send the offer to the customer and start the validity clock, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Send the offer and start the validity timer

  Scenario: AC1 Send the offer and start the validity timer
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-04
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-11
    Given a case in state AWAITING_CREDIT_APPROVAL
    When credit approved
    Then release the offer and send it to the customer
    Then the case moves to OFFER_WITH_CUSTOMER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |
| POST | /api/recovery/v1/treatments/{treatmentId}/submit | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-007-01 | AC1 | Send the offer and start the validity timer |
| TC-E3-007-02 | AC2 | Rule R-RES-04 |
| TC-E3-007-03 | AC3 | Rule R-RES-11 |
| TC-E3-007-04 | AC4 | Not recorded |
| TC-E3-007-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-007-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-008 Route the signed offer to operations for booking

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-08 Route the signed offer to operations for booking |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-09 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to move the case to operations when the customer signs inside the validity period, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Route the signed offer to operations for booking

  Scenario: AC1 Route the signed offer to operations for booking
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then moves the case to operations when the customer signs inside the validity period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-16
    Given a case in state OFFER_WITH_CUSTOMER
    When customer signed
    Then route the case to operations to complete the booking
    Then the case moves to WITH_OPS_BOOKING

  Scenario: AC3 Rule R-SET-10
    Given a case in state OFFER_WITH_CUSTOMER_SET
    When customer signed
    Then route the case to operations and raise the payment instruction
    Then the case moves to WITH_OPS_SETTLEMENT

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-008-01 | AC1 | Route the signed offer to operations for booking |
| TC-E3-008-02 | AC2 | Rule R-RES-16 |
| TC-E3-008-03 | AC3 | Rule R-SET-10 |
| TC-E3-008-04 | AC4 | Not recorded |
| TC-E3-008-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-008-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-009 Return the case to its prior status on no signature

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-09 Return the case to its prior status on no signature |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-07 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to send the case back to the status it held in COLLINS when the customer declines or the offer expires, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Return the case to its prior status on no signature

  Scenario: AC1 Return the case to its prior status on no signature
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the case back to the status it held in COLLINS when the customer declines or the offer expires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-17
    Given a case in state OFFER_WITH_CUSTOMER
    When customer declined
    Then return the case to its prior status in COLLINS
    Then the case moves to RETURNED_TO_COLLINS

  Scenario: AC3 Rule R-RES-18
    Given a case in state OFFER_WITH_CUSTOMER
    When offer expired
    Then return the case to its prior status in COLLINS
    Then the case moves to RETURNED_TO_COLLINS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-009-01 | AC1 | Return the case to its prior status on no signature |
| TC-E3-009-02 | AC2 | Rule R-RES-17 |
| TC-E3-009-03 | AC3 | Rule R-RES-18 |
| TC-E3-009-04 | AC4 | Not recorded |
| TC-E3-009-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-009-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-010 Book the plan and set the schedule

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-10 Book the plan and set the schedule |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CHO-07, FEAT-CHO-08 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to write the plan to NLEADS and ALS, set the payment schedule and start the plan timers, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Book the plan and set the schedule

  Scenario: AC1 Book the plan and set the schedule
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the plan to NLEADS and ALS, sets the payment schedule and starts the plan timers
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-22
    Given a case in state WITH_OPS_BOOKING
    When booking confirmed
    Then record the booking reference and set the payment schedule
    Then the case moves to BOOKED_IN_ALS_NLEADS

  Scenario: AC3 Rule R-RES-25
    Given a case in state BOOKED_IN_ALS_NLEADS
    When schedule set
    Then start the plan timers and move the plan to running
    Then the case moves to PLAN_RUNNING

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-010-01 | AC1 | Book the plan and set the schedule |
| TC-E3-010-02 | AC2 | Rule R-RES-22 |
| TC-E3-010-03 | AC3 | Rule R-RES-25 |
| TC-E3-010-04 | AC4 | Not recorded |
| TC-E3-010-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-010-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-011 Detect and handle a broken plan

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-11 Detect and handle a broken plan |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-11 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to count missed payments against the break rule and move the case to the point the rule names, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Detect and handle a broken plan

  Scenario: AC1 Detect and handle a broken plan
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then counts missed payments against the break rule and moves the case to the point the rule names
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-29
    Given a case in state PLAN_CURE_PERIOD
    When cure period expired
    Then increment the break count and mark the plan broken
    Then the case moves to PLAN_BROKEN

  Scenario: AC3 Rule R-RES-30
    Given a case in state PLAN_BROKEN
    When break recorded
    Then return the case to the route decision with reason broken_plan
    Then the case moves to BACK_TO_ROUTE_DECISION

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-011-01 | AC1 | Detect and handle a broken plan |
| TC-E3-011-02 | AC2 | Rule R-RES-29 |
| TC-E3-011-03 | AC3 | Rule R-RES-30 |
| TC-E3-011-04 | AC4 | Not recorded |
| TC-E3-011-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-011-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-012 Run a deed in lieu to ownership transfer

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-12 Run a deed in lieu to ownership transfer |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-01 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want to take the deed in lieu from offer through inspection, documents and transfer to the asset record, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Run a deed in lieu to ownership transfer

  Scenario: AC1 Run a deed in lieu to ownership transfer
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the deed in lieu from offer through inspection, documents and transfer to the asset record
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-28
    Given a case in state AWAITING_TRANSFER
    When transfer completed
    Then record the asset in AMIS, settle the debt and release the registration
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIL-16
    Given a case in state AWAITING_SECOND_SIGNATURE
    When second signature given
    Then generate the documents and put the offer to the customer
    Then the case moves to OFFER_WITH_CUSTOMER_DIL

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-16 Deed in lieu | Checks; appraisal; approved; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-012-01 | AC1 | Run a deed in lieu to ownership transfer |
| TC-E3-012-02 | AC2 | Rule R-DIL-28 |
| TC-E3-012-03 | AC3 | Rule R-DIL-16 |
| TC-E3-012-04 | AC4 | Not recorded |
| TC-E3-012-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-012-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-013 Check encumbrance and eligibility before negotiation

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-13 Check encumbrance and eligibility before negotiation |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-12 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to run the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Check encumbrance and eligibility before negotiation

  Scenario: AC1 Check encumbrance and eligibility before negotiation
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-SET-22
    Given a case in state COLLATERAL_RELEASE_REQUESTED
    When title documents missing
    Then raise a task to re-create the title set before release
    Then the case moves to COLLATERAL_RELEASE_REQUESTED

  Scenario: AC3 Rule R-DIL-01
    Given a case in state ROUTE_APPROVED_DIL
    When route approved
    Then prioritize the lead and start the early readiness checks
    Then the case moves to EARLY_READINESS_CHECK

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-16 Deed in lieu | Checks; appraisal; approved; transferred |
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-013-01 | AC1 | Check encumbrance and eligibility before negotiation |
| TC-E3-013-02 | AC2 | Rule R-SET-22 |
| TC-E3-013-03 | AC3 | Rule R-DIL-01 |
| TC-E3-013-04 | AC4 | Not recorded |
| TC-E3-013-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-013-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-014 Unlock the asset as a non performing asset by rule

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-14 Unlock the asset as a non performing asset by rule |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-13 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to apply the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Unlock the asset as a non performing asset by rule

  Scenario: AC1 Unlock the asset as a non performing asset by rule
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the auto-unlock rule so the asset moves to the asset list without a person for the cases that qualify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-22
    Given a case in state WITH_FIELD_INSPECTION
    When inspection completed
    Then run the asset unlock rule
    Then the case moves to ASSET_UNLOCK_DECISION

  Scenario: AC3 Rule R-DIL-23
    Given a case in state ASSET_UNLOCK_DECISION
    When auto unlock passed
    Then release the asset for transfer
    Then the case moves to AWAITING_TRANSFER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-16 Deed in lieu | Checks; appraisal; approved; transferred |
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-014-01 | AC1 | Unlock the asset as a non performing asset by rule |
| TC-E3-014-02 | AC2 | Rule R-DIL-22 |
| TC-E3-014-03 | AC3 | Rule R-DIL-23 |
| TC-E3-014-04 | AC4 | Not recorded |
| TC-E3-014-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-014-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-015 Capture the collateral inspection in the field

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-15 Capture the collateral inspection in the field |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-12 |
| Decision | None |

**Story.** As a field collector, I want the Workbench to let the field officer record the inspection, the checklist and the bills against the case, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Capture the collateral inspection in the field

  Scenario: AC1 Capture the collateral inspection in the field
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the field officer record the inspection, the checklist and the bills against the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-12
    Given a case in state AWAITING_CREDIT_APPROVAL
    When credit declined
    Then record the reason against the limit applied
    Then the case moves to DECLINED_BY_CREDIT

  Scenario: AC3 Rule R-SET-09
    Given a case in state OFFER_WITH_CUSTOMER_SET
    When customer counter offered
    Then return the case to the officer and re-test against the floor
    Then the case moves to WITH_FCR_OFFICER_SET

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |
| POST | /api/recovery/v1/treatments/{treatmentId}/submit | Treatment and offer U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-015-01 | AC1 | Capture the collateral inspection in the field |
| TC-E3-015-02 | AC2 | Rule R-RES-12 |
| TC-E3-015-03 | AC3 | Rule R-SET-09 |
| TC-E3-015-04 | AC4 | Not recorded |
| TC-E3-015-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-015-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-016 Set up a deed in lieu buy-back rental

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-16 Set up a deed in lieu buy-back rental |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-12 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to open the rental record, the auto-debit and the receipt loop where the customer buys back, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Set up a deed in lieu buy-back rental

  Scenario: AC1 Set up a deed in lieu buy-back rental
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then opens the rental record, the auto-debit and the receipt loop where the customer buys back
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-32
    Given a case in state ASSET_ON_BOOKS
    When buyback agreed
    Then create the rental record and set the auto-debit
    Then the case moves to RENTAL_RUNNING

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-16 Deed in lieu | Checks; appraisal; approved; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-016-01 | AC1 | Set up a deed in lieu buy-back rental |
| TC-E3-016-02 | AC2 | Rule R-DIL-32 |
| TC-E3-016-03 | AC3 | Not recorded |
| TC-E3-016-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-016-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-017 Release the collateral after settlement

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-17 Release the collateral after settlement |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CHO-08 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to tell CCMS to release the security once the settlement has cleared, and record the release, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Release the collateral after settlement

  Scenario: AC1 Release the collateral after settlement
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tells CCMS to release the security once the settlement has cleared, and records the release
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-33
    Given a case in state PLAN_RUNNING
    When final installment paid
    Then close the treatment, release the collateral and close the case
    Then the case moves to PLAN_COMPLETED

  Scenario: AC3 Rule R-SET-20
    Given a case in state PAYMENT_CLEARED
    When clearance confirmed
    Then close the account in ALS and request the collateral release
    Then the case moves to COLLATERAL_RELEASE_REQUESTED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-017-01 | AC1 | Release the collateral after settlement |
| TC-E3-017-02 | AC2 | Rule R-RES-33 |
| TC-E3-017-03 | AC3 | Rule R-SET-20 |
| TC-E3-017-04 | AC4 | Not recorded |
| TC-E3-017-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-017-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-018 Generate the treatment document set

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S2 TDR, settlement and deed in lieu |
| Feature | FEAT-TRT-18 Generate the treatment document set |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-07 |
| Decision | None |

**Story.** As a restructuring officer (FCR), I want the Workbench to produce the agreement, contract, credit approval and mortgage documents for the treatment chosen, so that restructures and settlements reach booking in days.

**Acceptance criteria**

```gherkin
Feature: Generate the treatment document set

  Scenario: AC1 Generate the treatment document set
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the agreement, contract, credit approval and mortgage documents for the treatment chosen
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIL-14
    Given a case in state TRANSFER_PRICE_SET
    When price inside floor
    Then generate the credit approval, the contract and the mortgage documents
    Then the case moves to OFFER_WITH_CUSTOMER_DIL

  Scenario: AC3 Rule R-RES-10
    Given a case in state WITH_FCR_OFFICER
    When offer prepared
    Then route the offer to credit approval; 44% of TDR cases deviate today
    Then the case moves to AWAITING_CREDIT_APPROVAL

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/treatments | Treatment and offer C |
| GET | /api/recovery/v1/treatments/{treatmentId} | Treatment and offer R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-14 Treatment record | Draft; submitted; approved; booked; broken |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S2-001 | Error | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Information | The offer to the customer ends on {date}. |
| MSG-S2-002 | Warning | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-018-01 | AC1 | Generate the treatment document set |
| TC-E3-018-02 | AC2 | Rule R-DIL-14 |
| TC-E3-018-03 | AC3 | Rule R-RES-10 |
| TC-E3-018-04 | AC4 | Not recorded |
| TC-E3-018-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-018-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-013 Prepare a TCG guarantee claim

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-01 Prepare a TCG guarantee claim |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-16 |
| Decision | None |

**Story.** As a guarantee officer, I want the Workbench to assemble the claim from the case facts and the documents the scheme requires, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Prepare a TCG guarantee claim

  Scenario: AC1 Prepare a TCG guarantee claim
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then assembles the claim from the case facts and the documents the scheme requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-04
    Given a case in state DEADLINE_TIMER_RUNNING
    When preparation due
    Then the claim preparation agent assembles the claim against the scheme checklist
    Then the case moves to CLAIM_PREPARATION

  Scenario: AC3 Rule R-GUA-01
    Given a case in state GUARANTEE_DETECTED
    When guarantee found
    Then start the claim deadline timer from the date the default conditions are met
    Then the case moves to DEADLINE_TIMER_RUNNING

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-013-01 | AC1 | Prepare a TCG guarantee claim |
| TC-E4-013-02 | AC2 | Rule R-GUA-04 |
| TC-E4-013-03 | AC3 | Rule R-GUA-01 |
| TC-E4-013-04 | AC4 | Not recorded |
| TC-E4-013-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-013-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-014 Submit the claim to the TCG portal

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-02 Submit the claim to the TCG portal |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-01 |
| Decision | None |

**Story.** As a guarantee officer, I want the Workbench to file the prepared claim and record the submission reference on the case, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Submit the claim to the TCG portal

  Scenario: AC1 Submit the claim to the TCG portal
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then files the prepared claim and records the submission reference on the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-12
    Given a case in state CLAIM_APPROVAL
    When claim approved
    Then submit the claim through the TCG claim channel
    Then the case moves to CLAIM_SUBMITTED

  Scenario: AC3 Rule R-GUA-21
    Given a case in state CLAIM_PART_PAID
    When balance claimed
    Then submit the balance claim
    Then the case moves to CLAIM_SUBMITTED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-014-01 | AC1 | Submit the claim to the TCG portal |
| TC-E4-014-02 | AC2 | Rule R-GUA-12 |
| TC-E4-014-03 | AC3 | Rule R-GUA-21 |
| TC-E4-014-04 | AC4 | Not recorded |
| TC-E4-014-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-014-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-015 Track the claim to payment

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-03 Track the claim to payment |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-02 |
| Decision | None |

**Story.** As a guarantee officer, I want the Workbench to follow the claim through its states and raise the service level breach if it stalls, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Track the claim to payment

  Scenario: AC1 Track the claim to payment
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then follows the claim through its states and raises the service level breach if it stalls
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-05
    Given a case in state DEADLINE_TIMER_RUNNING
    When claim deadline missed
    Then record the lost claim, the reason and the amount, and report the breach
    Then the case moves to DEADLINE_MISSED

  Scenario: AC3 Rule R-GUA-09
    Given a case in state CLAIM_PREPARATION
    When claim deadline missed
    Then record the lost claim and the reason, and report the breach
    Then the case moves to DEADLINE_MISSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-015-01 | AC1 | Track the claim to payment |
| TC-E4-015-02 | AC2 | Rule R-GUA-05 |
| TC-E4-015-03 | AC3 | Rule R-GUA-09 |
| TC-E4-015-04 | AC4 | Not recorded |
| TC-E4-015-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-015-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-016 Record the subrogation position

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-04 Record the subrogation position |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-03 |
| Decision | None |

**Story.** As a guarantee officer, I want the Workbench to record what the guarantor may reclaim after payment, so the position is not lost, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Record the subrogation position

  Scenario: AC1 Record the subrogation position
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then records what the guarantor may reclaim after payment, so the position is not lost
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-22
    Given a case in state CLAIM_SUBMITTED
    When full payment received
    Then match the payment, post it, and set the subrogation position
    Then the case moves to CLAIM_PAID

  Scenario: AC3 Rule R-GUA-23
    Given a case in state CLAIM_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the case moves to SUBROGATION_POSITION

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| case_party | id, case_id, party_id, party_role, role_from, role_to | DF-CAS-030 to DF-CAS-035 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-016-01 | AC1 | Record the subrogation position |
| TC-E4-016-02 | AC2 | Rule R-GUA-22 |
| TC-E4-016-03 | AC3 | Rule R-GUA-23 |
| TC-E4-016-04 | AC4 | Not recorded |
| TC-E4-016-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-016-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-017 Notify guarantors and co-borrowers

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-05 Notify guarantors and co-borrowers |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-01 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to send the demand to every guarantor and co-borrower on the case, from the approved template, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Notify guarantors and co-borrowers

  Scenario: AC1 Notify guarantors and co-borrowers
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the demand to every guarantor and co-borrower on the case, from the approved template
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| case_party | id, case_id, party_id, party_role, role_from, role_to | DF-CAS-030 to DF-CAS-035 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-017-01 | AC1 | Notify guarantors and co-borrowers |
| TC-E4-017-02 | AC2 | Not recorded |
| TC-E4-017-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-017-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-018 Negotiate with a guarantor

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-06 Negotiate with a guarantor |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-05 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to let the case owner negotiate within the range and record the outcome against the party, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Negotiate with a guarantor

  Scenario: AC1 Negotiate with a guarantor
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the case owner negotiate within the range and record the outcome against the party
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-23
    Given a case in state CLAIM_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the case moves to SUBROGATION_POSITION

  Scenario: AC3 Rule R-GUA-24
    Given a case in state CLAIM_PART_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the case moves to SUBROGATION_POSITION

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| case_party | id, case_id, party_id, party_role, role_from, role_to | DF-CAS-030 to DF-CAS-035 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-018-01 | AC1 | Negotiate with a guarantor |
| TC-E4-018-02 | AC2 | Rule R-GUA-23 |
| TC-E4-018-03 | AC3 | Rule R-GUA-24 |
| TC-E4-018-04 | AC4 | Not recorded |
| TC-E4-018-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-018-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-019 Close the case when a guarantee clears the debt

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-07 Close the case when a guarantee clears the debt |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-03 |
| Decision | None |

**Story.** As a guarantee officer, I want the Workbench to close the case and record the position when a guarantee payment clears the balance in full, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: Close the case when a guarantee clears the debt

  Scenario: AC1 Close the case when a guarantee clears the debt
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then closes the case and records the position when a guarantee payment clears the balance in full
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-19
    Given a case in state CLAIM_REJECTED
    When resubmission not possible
    Then close the guarantee and return the full balance to the route decision
    Then the case moves to RESIDUAL_TO_ROUTE

  Scenario: AC3 Rule R-GUA-26
    Given a case in state SUBROGATION_POSITION
    When balance satisfied
    Then close the guarantee and close the case
    Then the case moves to GUARANTEE_CLOSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-019-01 | AC1 | Close the case when a guarantee clears the debt |
| TC-E4-019-02 | AC2 | Rule R-GUA-19 |
| TC-E4-019-03 | AC3 | Rule R-GUA-26 |
| TC-E4-019-04 | AC4 | Not recorded |
| TC-E4-019-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-019-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-020 File an insurance claim on a collateral event

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S3 Guarantees and guarantors |
| Feature | FEAT-GUA-08 File an insurance claim on a collateral event |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-01 |
| Decision | None |

**Story.** As a case owner, I want to file the claim where collateral is stolen, written off or damaged, and trigger re-appraisal, so that no guarantee claim misses its deadline.

**Acceptance criteria**

```gherkin
Feature: File an insurance claim on a collateral event

  Scenario: AC1 File an insurance claim on a collateral event
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then files the claim where collateral is stolen, written off or damaged, and triggers re-appraisal
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| guarantee_claim | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at and 2 more | DF-TRT-015 to DF-TRT-022 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/guarantee-claims/{claimId} | Treatment and offer U |
| POST | /api/recovery/v1/cases/{caseId}/guarantee-claims | Treatment and offer C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Treatment and offer | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |
| Treatment and offer | C | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-020-01 | AC1 | File an insurance claim on a collateral event |
| TC-E4-020-02 | AC2 | Not recorded |
| TC-E4-020-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-020-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-001 Issue demand and recall notices

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-01 Issue demand and recall notices |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DRI-14 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to produce and send the statutory notices by rule, with no person in the path, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Issue demand and recall notices

  Scenario: AC1 Issue demand and recall notices
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces and sends the statutory notices by rule, with no person in the path
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-03
    Given a case in state NOTICE_GENERATED
    When template selected
    Then generate the demand and recall notices from the Legal-approved template
    Then the case moves to NOTICE_DISPATCHED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-001-01 | AC1 | Issue demand and recall notices |
| TC-E5-001-02 | AC2 | Rule R-LIT-03 |
| TC-E5-001-03 | AC3 | Not recorded |
| TC-E5-001-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-001-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-002 Record proof of delivery on a notice

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-02 Record proof of delivery on a notice |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DRI-17 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to write the delivery confirmation onto the case, which the notice period timer starts from, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Record proof of delivery on a notice

  Scenario: AC1 Record proof of delivery on a notice
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the delivery confirmation onto the case, which the notice period timer starts from
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-07
    Given a case in state NOTICE_DISPATCHED
    When proof of delivery received
    Then attach the proof and start the notice period from delivered_at
    Then the case moves to WITH_CUSTOMER_NOTICE_PERIOD

  Scenario: AC3 Rule R-LIT-08
    Given a case in state NOTICE_DISPATCHED
    When proof window expired
    Then mark the notice unserved; the notice period does not start
    Then the case moves to NOTICE_UNSERVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-002-01 | AC1 | Record proof of delivery on a notice |
| TC-E5-002-02 | AC2 | Rule R-LIT-07 |
| TC-E5-002-03 | AC3 | Rule R-LIT-08 |
| TC-E5-002-04 | AC4 | Not recorded |
| TC-E5-002-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-002-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-003 Run the notice period timer

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-03 Run the notice period timer |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CWC-11 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to start and track the statutory notice period and raise it when it expires, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Run the notice period timer

  Scenario: AC1 Run the notice period timer
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then starts and tracks the statutory notice period and raises it when it expires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-07
    Given a case in state NOTICE_DISPATCHED
    When proof of delivery received
    Then attach the proof and start the notice period from delivered_at
    Then the case moves to WITH_CUSTOMER_NOTICE_PERIOD

  Scenario: AC3 Rule R-LIT-08
    Given a case in state NOTICE_DISPATCHED
    When proof window expired
    Then mark the notice unserved; the notice period does not start
    Then the case moves to NOTICE_UNSERVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-003-01 | AC1 | Run the notice period timer |
| TC-E5-003-02 | AC2 | Rule R-LIT-07 |
| TC-E5-003-03 | AC3 | Rule R-LIT-08 |
| TC-E5-003-04 | AC4 | Not recorded |
| TC-E5-003-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-003-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-004 Assemble the litigation pack

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-04 Assemble the litigation pack |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-02 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to build the pack from the document index and the case facts, ready for the officer to verify, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Assemble the litigation pack

  Scenario: AC1 Assemble the litigation pack
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the pack from the document index and the case facts, ready for the officer to verify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-04
    Given a case in state NOTICE_GENERATED
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-16
    Given a case in state PACK_ASSEMBLY
    When pack complete
    Then present the pack to the litigation officer for verification
    Then the case moves to PACK_VERIFIED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-004-01 | AC1 | Assemble the litigation pack |
| TC-E5-004-02 | AC2 | Rule R-LIT-04 |
| TC-E5-004-03 | AC3 | Rule R-LIT-16 |
| TC-E5-004-04 | AC4 | Not recorded |
| TC-E5-004-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-004-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-005 Check the pack against the defect list

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-05 Check the pack against the defect list |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-04, FEAT-DCM-16 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to test the pack against the known defect list and name what is missing, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Check the pack against the defect list

  Scenario: AC1 Check the pack against the defect list
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests the pack against the known defect list and names what is missing
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-18
    Given a case in state PACK_DEFECT_HOLD
    When document retrieved
    Then re-run the defect list check
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC3 Rule R-LIT-32
    Given a case in state FILING_REJECTED
    When pack reworked
    Then re-run the defect list check and re-file
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-005-01 | AC1 | Check the pack against the defect list |
| TC-E5-005-02 | AC2 | Rule R-LIT-18 |
| TC-E5-005-03 | AC3 | Rule R-LIT-32 |
| TC-E5-005-04 | AC4 | Not recorded |
| TC-E5-005-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-005-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-006 Recover a missing or lost document

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-06 Recover a missing or lost document |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-05 |
| Decision | None |

**Story.** As a litigation officer, I want to open the recovery path for a document the pack needs and the bank cannot find, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Recover a missing or lost document

  Scenario: AC1 Recover a missing or lost document
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the recovery path for a document the pack needs and the bank cannot find
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-006-01 | AC1 | Recover a missing or lost document |
| TC-E5-006-02 | AC2 | Not recorded |
| TC-E5-006-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-006-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-007 Verify the pack and approve filing

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-07 Verify the pack and approve filing |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-05 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to let the litigation officer confirm the pack and authorize the filing, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Verify the pack and approve filing

  Scenario: AC1 Verify the pack and approve filing
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the litigation officer confirm the pack and authorize the filing
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-04
    Given a case in state NOTICE_GENERATED
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-11
    Given a case in state NOTICE_UNSERVED
    When prescription warning
    Then head of Litigation approves substituted service or filing where the law allows
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-007-01 | AC1 | Verify the pack and approve filing |
| TC-E5-007-02 | AC2 | Rule R-LIT-04 |
| TC-E5-007-03 | AC3 | Rule R-LIT-11 |
| TC-E5-007-04 | AC4 | Not recorded |
| TC-E5-007-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-007-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-008 Select the law firm from the panel

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-08 Select the law firm from the panel |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-02 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to pick the firm by the panel rule: scorecard, capacity, court and conflict, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Select the law firm from the panel

  Scenario: AC1 Select the law firm from the panel
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then picks the firm by the panel rule: scorecard, capacity, court and conflict
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-23
    Given a case in state PACK_VERIFIED
    When pack approved
    Then select the law firm by rule from the panel
    Then the case moves to FIRM_SELECTION

  Scenario: AC3 Rule R-LIT-27
    Given a case in state FIRM_INSTRUCTED
    When instruction declined
    Then record the decline and re-select the next firm on the scorecard
    Then the case moves to FIRM_DECLINED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-008-01 | AC1 | Select the law firm from the panel |
| TC-E5-008-02 | AC2 | Rule R-LIT-23 |
| TC-E5-008-03 | AC3 | Rule R-LIT-27 |
| TC-E5-008-04 | AC4 | Not recorded |
| TC-E5-008-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-008-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-009 Instruct the firm through the portal

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-09 Instruct the firm through the portal |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-08 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to send the instruction and the pack to the firm and start the partner clock, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Instruct the firm through the portal

  Scenario: AC1 Instruct the firm through the portal
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the instruction and the pack to the firm and starts the partner clock
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-24
    Given a case in state FIRM_SELECTION
    When firm matched
    Then issue the instruction with the pack through the portal
    Then the case moves to FIRM_INSTRUCTED

  Scenario: AC3 Rule R-LIT-26
    Given a case in state FIRM_ESCALATED
    When firm nominated
    Then issue the instruction with the pack through the portal
    Then the case moves to FIRM_INSTRUCTED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-009-01 | AC1 | Instruct the firm through the portal |
| TC-E5-009-02 | AC2 | Rule R-LIT-24 |
| TC-E5-009-03 | AC3 | Rule R-LIT-26 |
| TC-E5-009-04 | AC4 | Not recorded |
| TC-E5-009-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-009-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-010 Record the court filing and receipt

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-10 Record the court filing and receipt |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-09 |
| Decision | None |

**Story.** As a law firm user, I want to take the filing confirmation and the court case number from the firm onto the case, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Record the court filing and receipt

  Scenario: AC1 Record the court filing and receipt
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the filing confirmation and the court case number from the firm onto the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-31
    Given a case in state FILED_IN_COURT
    When court rejected filing
    Then record the defect and return the pack for rework
    Then the case moves to FILING_REJECTED

  Scenario: AC3 Rule R-LIT-30
    Given a case in state FIRM_INSTRUCTED
    When case filed
    Then write the court case number to the Legal Action and set the hearing timers
    Then the case moves to FILED_IN_COURT

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| PATCH | /api/recovery/v1/legal-actions/{legalActionId} | Litigation U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | U | RW-LITOFF, RW-ENFORCE, PT-LAWFIRM, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-010-01 | AC1 | Record the court filing and receipt |
| TC-E5-010-02 | AC2 | Rule R-LIT-31 |
| TC-E5-010-03 | AC3 | Rule R-LIT-30 |
| TC-E5-010-04 | AC4 | Not recorded |
| TC-E5-010-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-010-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-011 Track hearings, deadlines and fees

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-11 Track hearings, deadlines and fees |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-10 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to follow the court calendar, raise each deadline and accrues the fees against the case, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Track hearings, deadlines and fees

  Scenario: AC1 Track hearings, deadlines and fees
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then follows the court calendar, raises each deadline and accrues the fees against the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-011-01 | AC1 | Track hearings, deadlines and fees |
| TC-E5-011-02 | AC2 | Not recorded |
| TC-E5-011-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-011-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-012 Recommend the next litigation step

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-12 Recommend the next litigation step |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-11 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to propose the next step with reasons, for the officer or the approver to decide, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Recommend the next litigation step

  Scenario: AC1 Recommend the next litigation step
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then proposes the next step with reasons, for the officer or the approver to decide
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-04
    Given a case in state NOTICE_GENERATED
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-16
    Given a case in state PACK_ASSEMBLY
    When pack complete
    Then present the pack to the litigation officer for verification
    Then the case moves to PACK_VERIFIED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/notices/{noticeId}/approve | Litigation A |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | A | RW-LITOFF, RW-LEGAL, RW-PRODHEAD, RW-HEADLIT |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-012-01 | AC1 | Recommend the next litigation step |
| TC-E5-012-02 | AC2 | Rule R-LIT-04 |
| TC-E5-012-03 | AC3 | Rule R-LIT-16 |
| TC-E5-012-04 | AC4 | Not recorded |
| TC-E5-012-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-012-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-013 Settle before judgment

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-13 Settle before judgment |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As a litigation officer, I want to take a settlement during the case to the approver named by the limit, and books it if approved, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Settle before judgment

  Scenario: AC1 Settle before judgment
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a settlement during the case to the approver named by the limit, and books it if approved
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-36
    Given a case in state IN_HEARING
    When settlement proposed
    Then the agent proposes the step with its cost and effect, and routes it to the approver
    Then the case moves to SETTLEMENT_OFFERED_AT_COURT

  Scenario: AC3 Rule R-LIT-37
    Given a case in state SETTLEMENT_OFFERED_AT_COURT
    When settlement approved
    Then book the treatment and hold the litigation rather than withdraw it
    Then the case moves to LITIGATION_HELD

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-013-01 | AC1 | Settle before judgment |
| TC-E5-013-02 | AC2 | Rule R-LIT-36 |
| TC-E5-013-03 | AC3 | Rule R-LIT-37 |
| TC-E5-013-04 | AC4 | Not recorded |
| TC-E5-013-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-013-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-014 Decide and manage an appeal

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-14 Decide and manage an appeal |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-12 |
| Decision | None |

**Story.** As a litigation officer, I want to record the appeal decision, the grounds and the approval, and track it to its end, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Decide and manage an appeal

  Scenario: AC1 Decide and manage an appeal
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records the appeal decision, the grounds and the approval, and tracks it to its end
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-014-01 | AC1 | Decide and manage an appeal |
| TC-E5-014-02 | AC2 | Not recorded |
| TC-E5-014-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-014-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-015 Pay court fees and legal expenses

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-15 Pay court fees and legal expenses |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-05 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to check the fee against the schedule, route it for approval where needed and pay it, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Pay court fees and legal expenses

  Scenario: AC1 Pay court fees and legal expenses
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then checks the fee against the schedule, routes it for approval where needed and pays it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-30
    Given a case in state FIRM_INSTRUCTED
    When case filed
    Then write the court case number to the Legal Action and set the hearing timers
    Then the case moves to FILED_IN_COURT

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-015-01 | AC1 | Pay court fees and legal expenses |
| TC-E5-015-02 | AC2 | Rule R-LIT-30 |
| TC-E5-015-03 | AC3 | Not recorded |
| TC-E5-015-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-015-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-016 Record the judgment

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-16 Record the judgment |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-11 |
| Decision | None |

**Story.** As an enforcement owner, I want the Workbench to write the judgment date and amount onto the case and open the enforcement step, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Record the judgment

  Scenario: AC1 Record the judgment
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the judgment date and amount onto the case and opens the enforcement step
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-44
    Given a case in state IN_HEARING
    When judgment for the bank
    Then record the judgment date and amount and open the enforcement task
    Then the case moves to JUDGMENT_RECORDED

  Scenario: AC3 Rule R-LIT-45
    Given a case in state IN_HEARING
    When judgment against the bank
    Then record the dismissal and open the appeal window
    Then the case moves to JUDGMENT_DISMISSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/legal-actions/{legalActionId} | Litigation U |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | U | RW-LITOFF, RW-ENFORCE, PT-LAWFIRM, SY-DATALOAD |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-016-01 | AC1 | Record the judgment |
| TC-E5-016-02 | AC2 | Rule R-LIT-44 |
| TC-E5-016-03 | AC3 | Rule R-LIT-45 |
| TC-E5-016-04 | AC4 | Not recorded |
| TC-E5-016-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-016-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-017 Trace assets for enforcement

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-17 Trace assets for enforcement |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AGT-01 |
| Decision | None |

**Story.** As an enforcement owner, I want the Workbench to search the bureau, registries and insurers for assets to enforce against, and report what it finds, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Trace assets for enforcement

  Scenario: AC1 Trace assets for enforcement
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then searches the bureau, registries and insurers for assets to enforce against, and reports what it finds
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-50
    Given a case in state JUDGMENT_RECORDED
    When enforcement opened
    Then trace assets across NCB, internal data, registries and insurers
    Then the case moves to ASSET_TRACE

  Scenario: AC3 Rule R-LIT-52
    Given a case in state ASSET_TRACE
    When assets found
    Then present the enforcement decision with the traced assets
    Then the case moves to ENFORCEMENT_DECISION

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-017-01 | AC1 | Trace assets for enforcement |
| TC-E5-017-02 | AC2 | Rule R-LIT-50 |
| TC-E5-017-03 | AC3 | Rule R-LIT-52 |
| TC-E5-017-04 | AC4 | Not recorded |
| TC-E5-017-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-017-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-018 Apply for the writ and seizure

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-18 Apply for the writ and seizure |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-17 |
| Decision | None |

**Story.** As a law firm user, I want to instruct the writ and the seizure through the firm and track it to execution, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Apply for the writ and seizure

  Scenario: AC1 Apply for the writ and seizure
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then instructs the writ and the seizure through the firm and tracks it to execution
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-54
    Given a case in state ENFORCEMENT_DECISION
    When enforce approved
    Then instruct the firm to apply for the writ and seizure
    Then the case moves to WRIT_AND_SEIZURE

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-018-01 | AC1 | Apply for the writ and seizure |
| TC-E5-018-02 | AC2 | Rule R-LIT-54 |
| TC-E5-018-03 | AC3 | Not recorded |
| TC-E5-018-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-018-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-019 Follow the LED auction ladder

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-19 Follow the LED auction ladder |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-18 |
| Decision | None |

**Story.** As an enforcement owner, I want the Workbench to track the enforcement auction through the 100, 90, 80 and 70 percent steps of official value, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Follow the LED auction ladder

  Scenario: AC1 Follow the LED auction ladder
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-67
    Given a case in state LED_AUCTION
    When ladder exhausted
    Then record the unsold result and refer it to the enforcement owner
    Then the case moves to NO_BID_AT_70

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| PATCH | /api/recovery/v1/legal-actions/{legalActionId} | Litigation U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | U | RW-LITOFF, RW-ENFORCE, PT-LAWFIRM, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-019-01 | AC1 | Follow the LED auction ladder |
| TC-E5-019-02 | AC2 | Rule R-LIT-67 |
| TC-E5-019-03 | AC3 | Not recorded |
| TC-E5-019-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-019-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-020 Record an enforcement deferral with its reason

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-20 Record an enforcement deferral with its reason |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-16 |
| Decision | None |

**Story.** As an enforcement owner, I want the Workbench to let the enforcement owner defer with a coded reason and a review date, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Record an enforcement deferral with its reason

  Scenario: AC1 Record an enforcement deferral with its reason
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-55
    Given a case in state ENFORCEMENT_DECISION
    When defer recorded
    Then record the deferral and re-queue the case on the review date
    Then the case moves to DEFERRAL_RECORDED

  Scenario: AC3 Rule R-LIT-44
    Given a case in state IN_HEARING
    When judgment for the bank
    Then record the judgment date and amount and open the enforcement task
    Then the case moves to JUDGMENT_RECORDED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| queue | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | DF-WRK-001 to DF-WRK-008 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/legal-actions/{legalActionId} | Litigation U |
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | U | RW-LITOFF, RW-ENFORCE, PT-LAWFIRM, SY-DATALOAD |
| Litigation | C | RW-LITOFF, RW-ENFORCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-020-01 | AC1 | Record an enforcement deferral with its reason |
| TC-E5-020-02 | AC2 | Rule R-LIT-55 |
| TC-E5-020-03 | AC3 | Rule R-LIT-44 |
| TC-E5-020-04 | AC4 | Not recorded |
| TC-E5-020-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-020-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-021 File a bankruptcy petition

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-21 File a bankruptcy petition |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As an enforcement owner, I want to take the petition to the approver and file it through the firm, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: File a bankruptcy petition

  Scenario: AC1 File a bankruptcy petition
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the petition to the approver and files it through the firm
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-58
    Given a case in state ENFORCEMENT_DECISION
    When petition proposed
    Then route the petition to the approver at D7.5
    Then the case moves to BANKRUPTCY_PETITION

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-021-01 | AC1 | File a bankruptcy petition |
| TC-E5-021-02 | AC2 | Rule R-LIT-58 |
| TC-E5-021-03 | AC3 | Not recorded |
| TC-E5-021-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-021-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-022 Match enforcement proceeds to the case

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S4 Litigation and enforcement |
| Feature | FEAT-LIT-22 Match enforcement proceeds to the case |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-04 |
| Decision | None |

**Story.** As an enforcement owner, I want the Workbench to match money from the LED or the firm to the case and apply it to the balance, so that cases reach court faster with complete packs.

**Acceptance criteria**

```gherkin
Feature: Match enforcement proceeds to the case

  Scenario: AC1 Match enforcement proceeds to the case
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches money from the LED or the firm to the case and applies it to the balance
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-51
    Given a case in state JUDGMENT_RECORDED
    When debtor paid after judgment
    Then match the payment, close the enforcement and close the case
    Then the case moves to CASE_CLOSED

  Scenario: AC3 Rule R-LIT-65
    Given a case in state LED_AUCTION
    When round sold
    Then match the proceeds to the case
    Then the case moves to PROCEEDS_MATCHED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/legal-actions | Litigation C |
| GET | /api/recovery/v1/legal-actions/{legalActionId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S4-001 | Error | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Warning | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-022-01 | AC1 | Match enforcement proceeds to the case |
| TC-E5-022-02 | AC2 | Rule R-LIT-51 |
| TC-E5-022-03 | AC3 | Rule R-LIT-65 |
| TC-E5-022-04 | AC4 | Not recorded |
| TC-E5-022-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-022-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-019 Take a repossessed vehicle onto the books

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-01 Take a repossessed vehicle onto the books |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CWC-02 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to create the asset record from the repossession result and start the holding clock, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Take a repossessed vehicle onto the books

  Scenario: AC1 Take a repossessed vehicle onto the books
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record from the repossession result and starts the holding clock
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-06
    Given a case in state ASSET_ON_BOOKS
    When asset record confirmed
    Then start the holding age clock and the provision step clock, and charge cost of carry monthly
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-01
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-019-01 | AC1 | Take a repossessed vehicle onto the books |
| TC-E3-019-02 | AC2 | Rule R-DIS-06 |
| TC-E3-019-03 | AC3 | Rule R-DIS-01 |
| TC-E3-019-04 | AC4 | Not recorded |
| TC-E3-019-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-019-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-020 Take a property onto the books after a deed in lieu

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-02 Take a property onto the books after a deed in lieu |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-14 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to create the asset record when a deed in lieu transfer completes, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Take a property onto the books after a deed in lieu

  Scenario: AC1 Take a property onto the books after a deed in lieu
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record when a deed in lieu transfer completes
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-02
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-01
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-020-01 | AC1 | Take a property onto the books after a deed in lieu |
| TC-E3-020-02 | AC2 | Rule R-DIS-02 |
| TC-E3-020-03 | AC3 | Rule R-DIS-01 |
| TC-E3-020-04 | AC4 | Not recorded |
| TC-E3-020-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-020-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-021 Take a property onto the books after an LED auction

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-03 Take a property onto the books after an LED auction |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-LIT-19 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to create the asset record when the bank takes the property at the enforcement auction, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Take a property onto the books after an LED auction

  Scenario: AC1 Take a property onto the books after an LED auction
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record when the bank takes the property at the enforcement auction
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-01
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-02
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-021-01 | AC1 | Take a property onto the books after an LED auction |
| TC-E3-021-02 | AC2 | Rule R-DIS-01 |
| TC-E3-021-03 | AC3 | Rule R-DIS-02 |
| TC-E3-021-04 | AC4 | Not recorded |
| TC-E3-021-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-021-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-022 Serve the statutory notice and prove delivery

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-04 Serve the statutory notice and prove delivery |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-02 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to send the notice the repossession requires and record the proof, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Serve the statutory notice and prove delivery

  Scenario: AC1 Serve the statutory notice and prove delivery
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the notice the repossession requires and records the proof
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-04
    Given a case in state ASSET_PENDING_TAKE_ON
    When statutory notice failed
    Then hold the take-on, raise a failed notice task and re-serve on a confirmed address
    Then the case moves to FAILED_NOTICE_QUEUE

  Scenario: AC3 Rule R-DIS-05
    Given a case in state FAILED_NOTICE_QUEUE
    When notice reissued
    Then re-serve the statutory notice and resume the take-on
    Then the case moves to ASSET_PENDING_TAKE_ON

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| contact_point | id, party_id, channel, value_token, source, consent_status and 2 more | DF-PTY-013 to DF-PTY-020 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-022-01 | AC1 | Serve the statutory notice and prove delivery |
| TC-E3-022-02 | AC2 | Rule R-DIS-04 |
| TC-E3-022-03 | AC3 | Rule R-DIS-05 |
| TC-E3-022-04 | AC4 | Not recorded |
| TC-E3-022-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-022-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-023 Track holding age against the provision steps

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-05 Track holding age against the provision steps |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-01 |
| Decision | None |

**Story.** As a nPA and asset manager, I want the Workbench to count the days held and apply the provision step the policy sets at each threshold, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Track holding age against the provision steps

  Scenario: AC1 Track holding age against the provision steps
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then counts the days held and applies the provision step the policy sets at each threshold
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-06
    Given a case in state ASSET_ON_BOOKS
    When asset record confirmed
    Then start the holding age clock and the provision step clock, and charge cost of carry monthly
    Then the case moves to ASSET_HELD

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets | Asset and disposal R |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-023-01 | AC1 | Track holding age against the provision steps |
| TC-E3-023-02 | AC2 | Rule R-DIS-06 |
| TC-E3-023-03 | AC3 | Not recorded |
| TC-E3-023-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-023-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-024 Record and track the asset stock balance

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-06 Record and track the asset stock balance |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-05 |
| Decision | None |

**Story.** As a nPA and asset manager, I want to give the stock balance an owner and a number on one screen, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Record and track the asset stock balance

  Scenario: AC1 Record and track the asset stock balance
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then gives the stock balance an owner and a number on one screen. It has no owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-01
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-02
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-024-01 | AC1 | Record and track the asset stock balance |
| TC-E3-024-02 | AC2 | Rule R-DIS-01 |
| TC-E3-024-03 | AC3 | Rule R-DIS-02 |
| TC-E3-024-04 | AC4 | Not recorded |
| TC-E3-024-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-024-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-025 Maintain a held property

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-07 Maintain a held property |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-05 |
| Decision | None |

**Story.** As a nPA and asset manager, I want to record maintenance, insurance and custody costs against the asset, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Maintain a held property

  Scenario: AC1 Maintain a held property
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records maintenance, insurance and custody costs against the asset
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-37
    Given a case in state ROUND_OPEN
    When bid placed
    Then record the bid against the round and the asset
    Then the case moves to BID_RECEIVED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| document_custody | id, document_id, moved_at, from_location, to_location, held_by and 1 more | DF-DOC-018 to DF-DOC-024 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-025-01 | AC1 | Maintain a held property |
| TC-E3-025-02 | AC2 | Rule R-DIS-37 |
| TC-E3-025-03 | AC3 | Not recorded |
| TC-E3-025-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-025-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-021 Evict occupants from a held property

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-08 Evict occupants from a held property |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-07 |
| Decision | None |

**Story.** As a sale officer, I want to open and track the eviction, which needs Legal and has no legal owner today, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Evict occupants from a held property

  Scenario: AC1 Evict occupants from a held property
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens and tracks the eviction, which needs Legal and has no legal owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-13
    Given a case in state ASSET_HELD
    When occupants refuse possession
    Then raise the eviction instruction to Legal
    Then the case moves to EVICTION_REQUIRED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-021-01 | AC1 | Evict occupants from a held property |
| TC-E4-021-02 | AC2 | Rule R-DIS-13 |
| TC-E4-021-03 | AC3 | Not recorded |
| TC-E4-021-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-021-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-026 Re-appraise a held asset on cycle

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-09 Re-appraise a held asset on cycle |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-VAL-01 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to raise the re-appraisal order when the holding period passes the re-appraisal interval, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Re-appraise a held asset on cycle

  Scenario: AC1 Re-appraise a held asset on cycle
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then raises the re-appraisal order when the holding period passes the re-appraisal interval
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-44
    Given a case in state NO_BID_AT_FLOOR
    When relist rule applied
    Then re-list the asset and order a re-appraisal where the cycle is due
    Then the case moves to RELISTED

  Scenario: AC3 Rule R-DIS-15
    Given a case in state ASSET_HELD
    When reappraisal cycle due
    Then order the re-appraisal through SVAF
    Then the case moves to REAPPRAISAL_ORDERED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets | Asset and disposal R |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-23 Listing and price | Draft; below limit; approved; published |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-026-01 | AC1 | Re-appraise a held asset on cycle |
| TC-E3-026-02 | AC2 | Rule R-DIS-44 |
| TC-E3-026-03 | AC3 | Rule R-DIS-15 |
| TC-E3-026-04 | AC4 | Not recorded |
| TC-E3-026-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-026-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-027 Recommend the disposal route

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-10 Recommend the disposal route |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-05 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to propose auction, broker, RAMC, buy-back or rental with the expected return on each, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Recommend the disposal route

  Scenario: AC1 Recommend the disposal route
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then proposes auction, broker, RAMC, buy-back or rental with the expected return on each
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-14
    Given a case in state EVICTION_REQUIRED
    When possession taken
    Then return the asset to hold and resume the disposal route
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-08
    Given a case in state TITLE_BLOCKED
    When title cleared
    Then release the asset to hold and to the disposal route
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-027-01 | AC1 | Recommend the disposal route |
| TC-E3-027-02 | AC2 | Rule R-DIS-14 |
| TC-E3-027-03 | AC3 | Rule R-DIS-08 |
| TC-E3-027-04 | AC4 | Not recorded |
| TC-E3-027-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-027-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-028 Set the start and floor price

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-11 Set the start and floor price |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-10 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to let the sale officer set the opening price and the floor, with the head of NPA approving the floor, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Set the start and floor price

  Scenario: AC1 Set the start and floor price
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the sale officer set the opening price and the floor, with the head of NPA approving the floor
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-28
    Given a case in state ROUTE_APPROVED_AUCTION
    When price model run
    Then pricing agent proposes the opening price and the floor price as the reserve
    Then the case moves to PRICE_PROPOSED

  Scenario: AC3 Rule R-DIS-17
    Given a case in state REAPPRAISAL_RECEIVED
    When value accepted
    Then update the appraised value and reset the list and floor price inputs
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-23 Listing and price | Draft; below limit; approved; published |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-028-01 | AC1 | Set the start and floor price |
| TC-E3-028-02 | AC2 | Rule R-DIS-28 |
| TC-E3-028-03 | AC3 | Rule R-DIS-17 |
| TC-E3-028-04 | AC4 | Not recorded |
| TC-E3-028-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-028-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-029 Publish the listing

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-12 Publish the listing |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-11 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to put the asset on HOME.SCB and the auction portal with its price and schedule, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Publish the listing

  Scenario: AC1 Publish the listing
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then puts the asset on HOME.SCB and the auction portal with its price and schedule
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-33
    Given a case in state FLOOR_APPROVED
    When listing evidence complete
    Then publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published
    Then the case moves to LISTING_LIVE

  Scenario: AC3 Rule R-DIS-67
    Given a case in state LISTING_LIVE
    When deviation raised
    Then pause the listing and the price schedule
    Then the case moves to DISPOSAL_PAUSED_DEVIATION

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-23 Listing and price | Draft; below limit; approved; published |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-029-01 | AC1 | Publish the listing |
| TC-E3-029-02 | AC2 | Rule R-DIS-33 |
| TC-E3-029-03 | AC3 | Rule R-DIS-67 |
| TC-E3-029-04 | AC4 | Not recorded |
| TC-E3-029-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-029-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-022 Run the descending price schedule

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-13 Run the descending price schedule |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-12 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to step the price down on the ladder at each round until a bid clears the floor, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Run the descending price schedule

  Scenario: AC1 Run the descending price schedule
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then steps the price down on the ladder at each round until a bid clears the floor
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-38
    Given a case in state ROUND_OPEN
    When round closed no bid
    Then step the price down on the published schedule and open the next round
    Then the case moves to ROUND_OPEN

  Scenario: AC3 Rule R-DIS-17
    Given a case in state REAPPRAISAL_RECEIVED
    When value accepted
    Then update the appraised value and reset the list and floor price inputs
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-23 Listing and price | Draft; below limit; approved; published |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-022-01 | AC1 | Run the descending price schedule |
| TC-E4-022-02 | AC2 | Rule R-DIS-38 |
| TC-E4-022-03 | AC3 | Rule R-DIS-17 |
| TC-E4-022-04 | AC4 | Not recorded |
| TC-E4-022-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-022-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-023 Allocate the asset to an auction vendor by distance

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-14 Allocate the asset to an auction vendor by distance |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-03 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to pick one of the four vendors by distance and capacity, as the current rule does, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Allocate the asset to an auction vendor by distance

  Scenario: AC1 Allocate the asset to an auction vendor by distance
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then picks one of the four vendors by distance and capacity, as the current rule does
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-30
    Given a case in state FLOOR_APPROVED
    When vendor required
    Then allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance
    Then the case moves to VENDOR_ALLOCATED

  Scenario: AC3 Rule R-DIS-31
    Given a case in state VENDOR_ALLOCATED
    When vendor unavailable
    Then re-allocate to the next vendor on the scorecard
    Then the case moves to VENDOR_ALLOCATED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-23 Listing and price | Draft; below limit; approved; published |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-023-01 | AC1 | Allocate the asset to an auction vendor by distance |
| TC-E4-023-02 | AC2 | Rule R-DIS-30 |
| TC-E4-023-03 | AC3 | Rule R-DIS-31 |
| TC-E4-023-04 | AC4 | Not recorded |
| TC-E4-023-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-023-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-024 Run auction rounds and report bids

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-15 Run auction rounds and report bids |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-14 |
| Decision | None |

**Story.** As an auction vendor, I want the Workbench to let the vendor run each round and report the bids back into the case, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Run auction rounds and report bids

  Scenario: AC1 Run auction rounds and report bids
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the vendor run each round and report the bids back into the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-49
    Given a case in state AWAITING_PAYMENT
    When payment term expired
    Then cancel the award, score the vendor and reopen the round
    Then the case moves to AWARD_CANCELED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/listings/{listingId}/rounds | Asset and disposal U |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-24 Auction rounds | Scheduled; open; result; settled |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | U | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, PT-AUCTION, PT-RAMC, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-024-01 | AC1 | Run auction rounds and report bids |
| TC-E4-024-02 | AC2 | Rule R-DIS-49 |
| TC-E4-024-03 | AC3 | Not recorded |
| TC-E4-024-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-024-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-025 Accept a bid below the floor with a second signature

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-16 Accept a bid below the floor with a second signature |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As a sale officer, I want to route any bid under the floor for a second approval before it can be accepted, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Accept a bid below the floor with a second signature

  Scenario: AC1 Accept a bid below the floor with a second signature
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then routes any bid under the floor for a second approval before it can be accepted
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-42
    Given a case in state SECOND_SIGNATURE_PENDING
    When second signature given
    Then accept the bid below the floor and agree the sale
    Then the case moves to SALE_AGREED

  Scenario: AC3 Rule R-DIS-41
    Given a case in state BID_RECEIVED
    When bid below floor
    Then route the bid for a second signature
    Then the case moves to SECOND_SIGNATURE_PENDING

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-23 Listing and price | Draft; below limit; approved; published |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-025-01 | AC1 | Accept a bid below the floor with a second signature |
| TC-E4-025-02 | AC2 | Rule R-DIS-42 |
| TC-E4-025-03 | AC3 | Rule R-DIS-41 |
| TC-E4-025-04 | AC4 | Not recorded |
| TC-E4-025-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-025-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-026 Re-list on no bid

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-17 Re-list on no bid |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-13 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to put the asset back on the schedule at the next price step when a round closes with no bid, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Re-list on no bid

  Scenario: AC1 Re-list on no bid
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then puts the asset back on the schedule at the next price step when a round closes with no bid
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-38
    Given a case in state ROUND_OPEN
    When round closed no bid
    Then step the price down on the published schedule and open the next round
    Then the case moves to ROUND_OPEN

  Scenario: AC3 Rule R-DIS-29
    Given a case in state PRICE_PROPOSED
    When floor approved by officer
    Then fix the floor as the reserve and set the step schedule by asset class
    Then the case moves to FLOOR_APPROVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-23 Listing and price | Draft; below limit; approved; published |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-026-01 | AC1 | Re-list on no bid |
| TC-E4-026-02 | AC2 | Rule R-DIS-38 |
| TC-E4-026-03 | AC3 | Rule R-DIS-29 |
| TC-E4-026-04 | AC4 | Not recorded |
| TC-E4-026-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-026-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-027 Enforce the five-day payment term

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-18 Enforce the five-day payment term |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-16 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to track the winning bidder's payment against the term and release the asset if it is missed, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Enforce the five-day payment term

  Scenario: AC1 Enforce the five-day payment term
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tracks the winning bidder's payment against the term and releases the asset if it is missed
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-11
    Given a case in state WORK_ORDER_OPEN
    When work accepted
    Then release the invoice for payment and return the asset to hold
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-37
    Given a case in state ROUND_OPEN
    When bid placed
    Then record the bid against the round and the asset
    Then the case moves to BID_RECEIVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |
| POST | /api/recovery/v1/listings/{listingId}/rounds | Asset and disposal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |
| Asset and disposal | U | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, PT-AUCTION, PT-RAMC, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-027-01 | AC1 | Enforce the five-day payment term |
| TC-E4-027-02 | AC2 | Rule R-DIS-11 |
| TC-E4-027-03 | AC3 | Rule R-DIS-37 |
| TC-E4-027-04 | AC4 | Not recorded |
| TC-E4-027-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-027-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-028 Transfer vehicle registration

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-19 Transfer vehicle registration |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-18 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to prepare and submits the registration transfer through SCIS, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Transfer vehicle registration

  Scenario: AC1 Transfer vehicle registration
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then prepares and submits the registration transfer through SCIS
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-51
    Given a case in state TITLE_TRANSFER_PENDING
    When registration transferred
    Then transfer the registration through SCIS
    Then the case moves to ASSET_SOLD

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-028-01 | AC1 | Transfer vehicle registration |
| TC-E4-028-02 | AC2 | Rule R-DIS-51 |
| TC-E4-028-03 | AC3 | Not recorded |
| TC-E4-028-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-028-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-029 Record a property transfer at the Land Office

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-20 Record a property transfer at the Land Office |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-18 |
| Decision | None |

**Story.** As a sale officer, I want to track the Land Office transfer, which stays a person and officer step, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Record a property transfer at the Land Office

  Scenario: AC1 Record a property transfer at the Land Office
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then tracks the Land Office transfer, which stays a person and officer step
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-52
    Given a case in state TITLE_TRANSFER_PENDING
    When title registered
    Then release the documents from custody and record the transfer at the Land Office
    Then the case moves to ASSET_SOLD

  Scenario: AC3 Rule R-DIS-02
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| document_custody | id, document_id, moved_at, from_location, to_location, held_by and 1 more | DF-DOC-018 to DF-DOC-024 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-029-01 | AC1 | Record a property transfer at the Land Office |
| TC-E4-029-02 | AC2 | Rule R-DIS-52 |
| TC-E4-029-03 | AC3 | Rule R-DIS-02 |
| TC-E4-029-04 | AC4 | Not recorded |
| TC-E4-029-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-029-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-030 Apply proceeds and raise the shortfall

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-21 Apply proceeds and raise the shortfall |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-10 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to apply the sale money to the balance and raise any residual to the next decision, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Apply proceeds and raise the shortfall

  Scenario: AC1 Apply proceeds and raise the shortfall
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the sale money to the balance and raises any residual to the next decision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-55
    Given a case in state PROCEEDS_APPLIED
    When shortfall calculated
    Then raise the residual for the D9 decision
    Then the case moves to SHORTFALL_RAISED

  Scenario: AC3 Rule R-DIS-54
    Given a case in state ASSET_SOLD
    When proceeds posted
    Then apply the proceeds to the case and the loan account, and match the vendor fee
    Then the case moves to PROCEEDS_APPLIED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| GET | /api/recovery/v1/assets | Asset and disposal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-030-01 | AC1 | Apply proceeds and raise the shortfall |
| TC-E4-030-02 | AC2 | Rule R-DIS-55 |
| TC-E4-030-03 | AC3 | Rule R-DIS-54 |
| TC-E4-030-04 | AC4 | Not recorded |
| TC-E4-030-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-030-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-031 Transfer a pool to RAMC or the joint venture

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-22 Transfer a pool to RAMC or the joint venture |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As a sale officer, I want to take a pool of assets to RAMC with committee approval, and record the transfer, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Transfer a pool to RAMC or the joint venture

  Scenario: AC1 Transfer a pool to RAMC or the joint venture
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a pool of assets to RAMC with committee approval, and records the transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-59
    Given a case in state ROUTE_APPROVED_RAMC
    When transfer instructed
    Then instruct the RAMC or joint venture transfer on the portal
    Then the case moves to RAMC_TRANSFER_PENDING

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| PRT-06 Transfer confirmation | Pending; confirmed |
| SCR-21 Asset list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-031-01 | AC1 | Transfer a pool to RAMC or the joint venture |
| TC-E4-031-02 | AC2 | Rule R-DIS-59 |
| TC-E4-031-03 | AC3 | Not recorded |
| TC-E4-031-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-031-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-032 Arrange a customer buy-back

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-23 Arrange a customer buy-back |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-10 |
| Decision | None |

**Story.** As a sale officer, I want to open the buy-back where the former owner repurchases, with the approval the limit requires, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Arrange a customer buy-back

  Scenario: AC1 Arrange a customer buy-back
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the buy-back where the former owner repurchases, with the approval the limit requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-66
    Given a case in state ASSET_HELD
    When deviation raised
    Then pause the disposal, stop contact where required and route to the deviation owner
    Then the case moves to DISPOSAL_PAUSED_DEVIATION

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-032-01 | AC1 | Arrange a customer buy-back |
| TC-E4-032-02 | AC2 | Rule R-DIS-66 |
| TC-E4-032-03 | AC3 | Not recorded |
| TC-E4-032-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-032-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-033 Rent a held asset to a third party

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-24 Rent a held asset to a third party |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-05 |
| Decision | None |

**Story.** As a sale officer, I want to record the rental, the debit and the arrears follow-up while the asset is held, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Rent a held asset to a third party

  Scenario: AC1 Rent a held asset to a third party
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records the rental, the debit and the arrears follow-up while the asset is held
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-25
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then set the rental terms and the auto-debit, and hold the asset as rented
    Then the case moves to RENTAL_ACTIVE

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-22 Asset record | Take-on; held; listed; sold |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-033-01 | AC1 | Rent a held asset to a third party |
| TC-E4-033-02 | AC2 | Rule R-DIS-25 |
| TC-E4-033-03 | AC3 | Not recorded |
| TC-E4-033-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-033-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-034 Sell through a broker

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S5 Assets and auction |
| Feature | FEAT-AST-25 Sell through a broker |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-10 |
| Decision | None |

**Story.** As a sale officer, I want to open the broker route with its fee and terms, and track it to the sale, so that assets sell sooner at approved prices.

**Acceptance criteria**

```gherkin
Feature: Sell through a broker

  Scenario: AC1 Sell through a broker
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the broker route with its fee and terms, and tracks it to the sale
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-24
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then agree the buy-back terms at the template price
    Then the case moves to ROUTE_APPROVED_BUYBACK

  Scenario: AC3 Rule R-DIS-25
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then set the rental terms and the auto-debit, and hold the asset as rented
    Then the case moves to RENTAL_ACTIVE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R |
| POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-21 Asset list | Loading; list |
| SCR-23 Listing and price | Draft; below limit; approved; published |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more |
| Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-034-01 | AC1 | Sell through a broker |
| TC-E4-034-02 | AC2 | Rule R-DIS-24 |
| TC-E4-034-03 | AC3 | Rule R-DIS-25 |
| TC-E4-034-04 | AC4 | Not recorded |
| TC-E4-034-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-034-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-023 Select eligible accounts for sale by rule

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-01 Select eligible accounts for sale by rule |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DRI-07 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to apply the eligibility rules, including the 54 percent cap, to pick the sale population, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Select eligible accounts for sale by rule

  Scenario: AC1 Select eligible accounts for sale by rule
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the eligibility rules, including the 54 percent cap, to pick the sale population
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-01
    Given a case in state LOT_CANDIDATE_SELECTED
    When debt sale cycle opened
    Then select the accounts for sale from the case list
    Then the case moves to LOT_BUILT

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots | Debt sale C |
| GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-25 Lot builder | Draft; priced; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | C | RW-DEBTSALE |
| Debt sale | R | RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD and 13 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-023-01 | AC1 | Select eligible accounts for sale by rule |
| TC-E5-023-02 | AC2 | Rule R-DS-01 |
| TC-E5-023-03 | AC3 | Not recorded |
| TC-E5-023-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-023-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-024 Build the lots and estimate the price

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-02 Build the lots and estimate the price |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-01 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to group the accounts into lots and estimates the price from the COLLINS lot economics, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Build the lots and estimate the price

  Scenario: AC1 Build the lots and estimate the price
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then groups the accounts into lots and estimates the price from the COLLINS lot economics
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots | Debt sale C |
| GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-25 Lot builder | Draft; priced; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | C | RW-DEBTSALE |
| Debt sale | R | RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD and 13 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-024-01 | AC1 | Build the lots and estimate the price |
| TC-E5-024-02 | AC2 | Not recorded |
| TC-E5-024-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-024-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-025 Prepare the masked data tape

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-03 Prepare the masked data tape |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-RDF-15 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to build the data tape with personal data masked under PDPA, ready for the data room, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Prepare the masked data tape

  Scenario: AC1 Prepare the masked data tape
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the data tape with personal data masked under PDPA, ready for the data room
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-10
    Given a case in state LOT_APPROVED
    When tape build run
    Then build the masked data tape under the PII masking rules
    Then the case moves to TAPE_PREPARED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-25 Lot builder | Draft; priced; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-025-01 | AC1 | Prepare the masked data tape |
| TC-E5-025-02 | AC2 | Rule R-DS-10 |
| TC-E5-025-03 | AC3 | Not recorded |
| TC-E5-025-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-025-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E5-026 Open the buyer data room

| Item | Value |
|---|---|
| Epic | E5, release 31 March 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-04 Open the buyer data room |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-03 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to publish the lot and the masked tape to the data room for qualified buyers, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Open the buyer data room

  Scenario: AC1 Open the buyer data room
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then publishes the lot and the masked tape to the data room for qualified buyers
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| PRT-05 Data room | Admitted; bidding; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E5-026-01 | AC1 | Open the buyer data room |
| TC-E5-026-02 | AC2 | Not recorded |
| TC-E5-026-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E5-026-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-001 Approve lots, reserve and tiered terms

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-05 Approve lots, reserve and tiered terms |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-01 |
| Decision | None |

**Story.** As the Head of Asset Liquidity, I want to take the lot, the reserve price and the terms to the committee for approval, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Approve lots, reserve and tiered terms

  Scenario: AC1 Approve lots, reserve and tiered terms
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the lot, the reserve price and the terms to the committee for approval
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-06
    Given a case in state LOT_WITH_COMMITTEE
    When lot approved by committee
    Then approve the lot, the reserve and the tiered terms, and log the decision
    Then the case moves to LOT_APPROVED

  Scenario: AC3 Rule R-DS-04
    Given a case in state LOT_BUILT
    When lot priced
    Then propose the lots, the tiered buyer terms and the reserve price
    Then the case moves to LOT_WITH_COMMITTEE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R |
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-25 Lot builder | Draft; priced; approved |
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | R | RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD and 13 more |
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-001-01 | AC1 | Approve lots, reserve and tiered terms |
| TC-E6-001-02 | AC2 | Rule R-DS-06 |
| TC-E6-001-03 | AC3 | Rule R-DS-04 |
| TC-E6-001-04 | AC4 | Not recorded |
| TC-E6-001-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-001-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-002 Qualify a buyer against KYC and licensing

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-06 Qualify a buyer against KYC and licensing |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-04 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to run the KYC, licensing and eligibility checks before a buyer can bid, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Qualify a buyer against KYC and licensing

  Scenario: AC1 Qualify a buyer against KYC and licensing
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the KYC, licensing and eligibility checks before a buyer can bid
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-14
    Given a case in state DATA_ROOM_OPEN
    When buyer requested access
    Then run the KYC, licensing and eligibility check on the bidder
    Then the case moves to BUYER_PENDING_KYC

  Scenario: AC3 Rule R-DS-18
    Given a case in state BIDDING_OPEN
    When bid submitted
    Then record the bid against the lot and the buyer
    Then the case moves to BIDS_RECEIVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-002-01 | AC1 | Qualify a buyer against KYC and licensing |
| TC-E6-002-02 | AC2 | Rule R-DS-14 |
| TC-E6-002-03 | AC3 | Rule R-DS-18 |
| TC-E6-002-04 | AC4 | Not recorded |
| TC-E6-002-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-002-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-003 Bar a buyer that fails qualification

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-07 Bar a buyer that fails qualification |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-06 |
| Decision | None |

**Story.** As the Head of Asset Liquidity, I want the Workbench to remove a buyer from the panel on a license breach and release the lot to the next bidder, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Bar a buyer that fails qualification

  Scenario: AC1 Bar a buyer that fails qualification
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then removes a buyer from the panel on a license breach and releases the lot to the next bidder
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-41
    Given a case in state BUYER_REJECTED
    When buyer barred
    Then remove the buyer from the panel and release the lot to the next bidder
    Then the case moves to BACK_TO_CASE_LIST

  Scenario: AC3 Rule R-DS-14
    Given a case in state DATA_ROOM_OPEN
    When buyer requested access
    Then run the KYC, licensing and eligibility check on the bidder
    Then the case moves to BUYER_PENDING_KYC

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-003-01 | AC1 | Bar a buyer that fails qualification |
| TC-E6-003-02 | AC2 | Rule R-DS-41 |
| TC-E6-003-03 | AC3 | Rule R-DS-14 |
| TC-E6-003-04 | AC4 | Not recorded |
| TC-E6-003-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-003-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-004 Take buyer bids

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-08 Take buyer bids |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-06 |
| Decision | None |

**Story.** As a debt buyer and AMC, I want the Workbench to let a qualified buyer bid on a lot through the portal, inside the bid window, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Take buyer bids

  Scenario: AC1 Take buyer bids
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets a qualified buyer bid on a lot through the portal, inside the bid window
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-34
    Given a case in state GL_POSTED
    When claim window closed
    Then close the lot and record realized recovery by lot and by buyer
    Then the case moves to LOT_CLOSED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-004-01 | AC1 | Take buyer bids |
| TC-E6-004-02 | AC2 | Rule R-DS-34 |
| TC-E6-004-03 | AC3 | Not recorded |
| TC-E6-004-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-004-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-005 Award the lot and test the price

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-09 Award the lot and test the price |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-08 |
| Decision | None |

**Story.** As a debt sale officer, I want to compare the best bid to the reserve and the model, and awards with the approval the limit requires, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Award the lot and test the price

  Scenario: AC1 Award the lot and test the price
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then compares the best bid to the reserve and the model, and awards with the approval the limit requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-19
    Given a case in state BIDS_RECEIVED
    When bidding window closed
    Then test the price against the reserve and the 54 percent cap, and route the award
    Then the case moves to AWARD_PENDING

  Scenario: AC3 Rule R-DS-04
    Given a case in state LOT_BUILT
    When lot priced
    Then propose the lots, the tiered buyer terms and the reserve price
    Then the case moves to LOT_WITH_COMMITTEE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |
| SCR-25 Lot builder | Draft; priced; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Debt sale | R | RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD and 13 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-005-01 | AC1 | Award the lot and test the price |
| TC-E6-005-02 | AC2 | Rule R-DS-19 |
| TC-E6-005-03 | AC3 | Rule R-DS-04 |
| TC-E6-005-04 | AC4 | Not recorded |
| TC-E6-005-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-005-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-006 Generate the sale agreement and notices

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-10 Generate the sale agreement and notices |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-07 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to produce the agreement and the customer notices the sale requires, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Generate the sale agreement and notices

  Scenario: AC1 Generate the sale agreement and notices
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the agreement and the customer notices the sale requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-23
    Given a case in state AWARD_PENDING
    When award confirmed
    Then award the lot and generate the sale agreement and the customer notices
    Then the case moves to LOT_AWARDED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-006-01 | AC1 | Generate the sale agreement and notices |
| TC-E6-006-02 | AC2 | Rule R-DS-23 |
| TC-E6-006-03 | AC3 | Not recorded |
| TC-E6-006-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-006-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-007 Transfer the data to the buyer

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-11 Transfer the data to the buyer |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-09 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to send the awarded account data to the buyer and record the transfer, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Transfer the data to the buyer

  Scenario: AC1 Transfer the data to the buyer
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the awarded account data to the buyer and records the transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-29
    Given a case in state SETTLED
    When data transfer run
    Then transfer the account data to the buyer
    Then the case moves to DATA_TRANSFERRED

  Scenario: AC3 Rule R-DS-25
    Given a case in state SETTLEMENT_PENDING
    When buyer settled
    Then confirm settlement and release the data transfer
    Then the case moves to SETTLED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-007-01 | AC1 | Transfer the data to the buyer |
| TC-E6-007-02 | AC2 | Rule R-DS-29 |
| TC-E6-007-03 | AC3 | Rule R-DS-25 |
| TC-E6-007-04 | AC4 | Not recorded |
| TC-E6-007-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-007-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-008 Derecognize and post to the general ledger

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-12 Derecognize and post to the general ledger |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-11 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to remove the sold accounts from the book and post the result to ALS and the ledger, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Derecognize and post to the general ledger

  Scenario: AC1 Derecognize and post to the general ledger
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then removes the sold accounts from the book and posts the result to ALS and the ledger
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-31
    Given a case in state DERECOGNISED
    When gl posting run
    Then post to the general ledger and send the provision input to Finance
    Then the case moves to GL_POSTED

  Scenario: AC3 Rule R-DS-33
    Given a case in state POSTING_REJECTED_DS
    When posting corrected
    Then re-post to ALS and the general ledger
    Then the case moves to GL_POSTED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 7 more | DF-INT-001 to DF-INT-013 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots | Debt sale C |
| GET | /api/recovery/v1/debt-sale-lots/{lotId} | Debt sale R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-25 Lot builder | Draft; priced; approved |
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | C | RW-DEBTSALE |
| Debt sale | R | RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD and 13 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-008-01 | AC1 | Derecognize and post to the general ledger |
| TC-E6-008-02 | AC2 | Rule R-DS-31 |
| TC-E6-008-03 | AC3 | Rule R-DS-33 |
| TC-E6-008-04 | AC4 | Not recorded |
| TC-E6-008-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-008-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-009 Handle a buyer put-back claim

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-13 Handle a buyer put-back claim |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-11 |
| Decision | None |

**Story.** As a debt sale officer, I want to review a claim that an account should not have been sold, and settles or reject it, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Handle a buyer put-back claim

  Scenario: AC1 Handle a buyer put-back claim
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then reviews a claim that an account should not have been sold, and settles or rejects it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-29
    Given a case in state SETTLED
    When data transfer run
    Then transfer the account data to the buyer
    Then the case moves to DATA_TRANSFERRED

  Scenario: AC3 Rule R-DS-34
    Given a case in state GL_POSTED
    When claim window closed
    Then close the lot and record realized recovery by lot and by buyer
    Then the case moves to LOT_CLOSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-009-01 | AC1 | Handle a buyer put-back claim |
| TC-E6-009-02 | AC2 | Rule R-DS-29 |
| TC-E6-009-03 | AC3 | Rule R-DS-34 |
| TC-E6-009-04 | AC4 | Not recorded |
| TC-E6-009-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-009-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-010 Close a case awarded in a sold lot

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-14 Close a case awarded in a sold lot |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-09 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to stop every open action on a case whose account is sold in a lot, and close it, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Close a case awarded in a sold lot

  Scenario: AC1 Close a case awarded in a sold lot
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then stops every open action on a case whose account is sold in a lot, and closes it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-010-01 | AC1 | Close a case awarded in a sold lot |
| TC-E6-010-02 | AC2 | Not recorded |
| TC-E6-010-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-010-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-011 Confirm buyer remittance

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-15 Confirm buyer remittance |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-12 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to match the buyer's payment to the award and close the money side of the lot, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Confirm buyer remittance

  Scenario: AC1 Confirm buyer remittance
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches the buyer's payment to the award and closes the money side of the lot
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-25
    Given a case in state SETTLEMENT_PENDING
    When buyer settled
    Then confirm settlement and release the data transfer
    Then the case moves to SETTLED

  Scenario: AC3 Rule R-DS-26
    Given a case in state SETTLEMENT_PENDING
    When buyer canceled
    Then cancel the award and score the cancellation against the buyer
    Then the case moves to AWARD_CANCELED_DS

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/debt-sale-lots/{lotId}/award | Debt sale A |
| GET | /api/recovery/v1/partner/data-room/{lotId} | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Debt sale | A | RW-DEBTSALE, RW-PRODHEAD, RW-HEADASL |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-011-01 | AC1 | Confirm buyer remittance |
| TC-E6-011-02 | AC2 | Rule R-DS-25 |
| TC-E6-011-03 | AC3 | Rule R-DS-26 |
| TC-E6-011-04 | AC4 | Not recorded |
| TC-E6-011-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-011-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-012 Apply the debt sale cap

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S6 Debt sale |
| Feature | FEAT-DBS-16 Apply the debt sale cap |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-01 |
| Decision | None |

**Story.** As a debt sale officer, I want the Workbench to hold the sale population inside the policy cap and report the headroom, so that debt sales run on approved lots and masked data.

**Acceptance criteria**

```gherkin
Feature: Apply the debt sale cap

  Scenario: AC1 Apply the debt sale cap
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then holds the sale population inside the policy cap and reports the headroom
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-26 Award | Open; closed; awarded; transferred |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-012-01 | AC1 | Apply the debt sale cap |
| TC-E6-012-02 | AC2 | Not recorded |
| TC-E6-012-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-012-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-013 Run the monthly eligibility scan on both tracks

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-01 Run the monthly eligibility scan on both tracks |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DRI-07 |
| Decision | None |

**Story.** As a write-off team member, I want the Workbench to scan the portfolio each month against the eligibility rules and propose the write-off population, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Run the monthly eligibility scan on both tracks

  Scenario: AC1 Run the monthly eligibility scan on both tracks
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then scans the portfolio each month against the eligibility rules and proposes the write-off population
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-01
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-013-01 | AC1 | Run the monthly eligibility scan on both tracks |
| TC-E6-013-02 | AC2 | Rule R-WO-01 |
| TC-E6-013-03 | AC3 | Not recorded |
| TC-E6-013-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-013-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-014 Apply the tax criteria

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-02 Apply the tax criteria |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-01 |
| Decision | None |

**Story.** As a write-off team member, I want the Workbench to test each proposed account against the tax criteria and record the result, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Apply the tax criteria

  Scenario: AC1 Apply the tax criteria
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests each proposed account against the tax criteria and records the result
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-01
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Rule R-WO-51
    Given a case in state REMITTED_TO_BUYER
    When remittance confirmed
    Then record the remittance against the sold account and close the item
    Then the case moves to CASE_CLOSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-014-01 | AC1 | Apply the tax criteria |
| TC-E6-014-02 | AC2 | Rule R-WO-01 |
| TC-E6-014-03 | AC3 | Rule R-WO-51 |
| TC-E6-014-04 | AC4 | Not recorded |
| TC-E6-014-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-014-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-015 Prepare the write-off pack

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-03 Prepare the write-off pack |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-01 |
| Decision | None |

**Story.** As a write-off team member, I want the Workbench to assemble the committee pack from the case facts, the documents and the recovery history, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Prepare the write-off pack

  Scenario: AC1 Prepare the write-off pack
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then assembles the committee pack from the case facts, the documents and the recovery history
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-05
    Given a case in state POPULATION_PROPOSED
    When pack built
    Then write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual
    Then the case moves to PACK_PREPARED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-015-01 | AC1 | Prepare the write-off pack |
| TC-E6-015-02 | AC2 | Rule R-WO-05 |
| TC-E6-015-03 | AC3 | Not recorded |
| TC-E6-015-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-015-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-016 Remove a case from the proposed population

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-04 Remove a case from the proposed population |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-03 |
| Decision | None |

**Story.** As a write-off team member, I want the Workbench to let the write-off team take a case out of the population before committee, with a reason, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Remove a case from the proposed population

  Scenario: AC1 Remove a case from the proposed population
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the write-off team take a case out of the population before committee, with a reason
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-07
    Given a case in state POPULATION_PROPOSED
    When team removed case
    Then remove the case from the proposed population with the reason recorded
    Then the case moves to CASE_REMOVED_BY_TEAM

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-016-01 | AC1 | Remove a case from the proposed population |
| TC-E6-016-02 | AC2 | Rule R-WO-07 |
| TC-E6-016-03 | AC3 | Not recorded |
| TC-E6-016-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-016-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-017 Route the population to the committee and schedule it

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-05 Route the population to the committee and schedule it |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-03 |
| Decision | None |

**Story.** As a write-off committee member, I want the Workbench to send the pack to the committee queue and books it into the monthly meeting, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Route the population to the committee and schedule it

  Scenario: AC1 Route the population to the committee and schedule it
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the pack to the committee queue and books it into the monthly meeting
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-11
    Given a case in state PACK_PREPARED
    When pack routed
    Then route the pack to the committee and schedule the meeting
    Then the case moves to WITH_COMMITTEE

  Scenario: AC3 Rule R-WO-06
    Given a case in state POPULATION_PROPOSED
    When case has open deviation
    Then hold the case out of the population and route it to the deviation handler
    Then the case moves to CASE_REMOVED_BY_TEAM

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| queue | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | DF-WRK-001 to DF-WRK-008 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-017-01 | AC1 | Route the population to the committee and schedule it |
| TC-E6-017-02 | AC2 | Rule R-WO-11 |
| TC-E6-017-03 | AC3 | Rule R-WO-06 |
| TC-E6-017-04 | AC4 | Not recorded |
| TC-E6-017-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-017-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-018 Approve a write-off inside the limit

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-06 Approve a write-off inside the limit |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-02 |
| Decision | None |

**Story.** As a write-off committee member, I want the Workbench to let the committee approve within its delegation and record the limit applied, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Approve a write-off inside the limit

  Scenario: AC1 Approve a write-off inside the limit
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee approve within its delegation and records the limit applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-15
    Given a case in state WITH_COMMITTEE
    When committee approved
    Then record the final call, the approver and the limit applied, and release to posting
    Then the case moves to APPROVED

  Scenario: AC3 Rule R-WO-12
    Given a case in state PACK_PREPARED
    When limit exceeded
    Then route the pack to the credit approval committee chaired by the product head with Risk
    Then the case moves to ESCALATED_TO_CREDIT_COMMITTEE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| delegation_limit | id, decision_code, approval_level, product_group, principal_limit, loss_pct_limit and 5 more | DF-REF-016 to DF-REF-026 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-018-01 | AC1 | Approve a write-off inside the limit |
| TC-E6-018-02 | AC2 | Rule R-WO-15 |
| TC-E6-018-03 | AC3 | Rule R-WO-12 |
| TC-E6-018-04 | AC4 | Not recorded |
| TC-E6-018-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-018-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-019 Reject a write-off

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-07 Reject a write-off |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-06 |
| Decision | None |

**Story.** As a write-off committee member, I want the Workbench to let the committee reject, with a reason that returns the case to recovery, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Reject a write-off

  Scenario: AC1 Reject a write-off
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee reject, with a reason that returns the case to recovery
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-019-01 | AC1 | Reject a write-off |
| TC-E6-019-02 | AC2 | Not recorded |
| TC-E6-019-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-019-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-020 Defer a write-off

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-08 Defer a write-off |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-06 |
| Decision | None |

**Story.** As a write-off committee member, I want the Workbench to let the committee defer with a review date, and hold the case until then, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Defer a write-off

  Scenario: AC1 Defer a write-off
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee defer with a review date, and holds the case until then
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-17
    Given a case in state WITH_COMMITTEE
    When committee deferred
    Then set the review timer and hold the case for the next scan
    Then the case moves to DEFERRED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-020-01 | AC1 | Defer a write-off |
| TC-E6-020-02 | AC2 | Rule R-WO-17 |
| TC-E6-020-03 | AC3 | Not recorded |
| TC-E6-020-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-020-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-021 Post an approved write-off

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-09 Post an approved write-off |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-06 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to post the write-off to ALS and the general ledger and release the provision, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Post an approved write-off

  Scenario: AC1 Post an approved write-off
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then posts the write-off to ALS and the general ledger and releases the provision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-05
    Given a case in state POPULATION_PROPOSED
    When pack built
    Then write-off agent prepares the pack: balance, provision carried, route history, legal and asset state, residual
    Then the case moves to PACK_PREPARED

  Scenario: AC3 Rule R-WO-23
    Given a case in state POSTING_REJECTED
    When rejection cleared
    Then re-post to ALS and the general ledger
    Then the case moves to POSTING_PENDING

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 7 more | DF-INT-001 to DF-INT-013 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-021-01 | AC1 | Post an approved write-off |
| TC-E6-021-02 | AC2 | Rule R-WO-05 |
| TC-E6-021-03 | AC3 | Rule R-WO-23 |
| TC-E6-021-04 | AC4 | Not recorded |
| TC-E6-021-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-021-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-022 Send provision inputs to Finance

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-10 Send provision inputs to Finance |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-09 |
| Decision | None |

**Story.** As a finance and CFO delegate, I want the Workbench to produce the provision file Finance needs from the posted population, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Send provision inputs to Finance

  Scenario: AC1 Send provision inputs to Finance
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the provision file Finance needs from the posted population
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-26
    Given a case in state PROVISION_RELEASED
    When finance feed run
    Then send the provision inputs and the tax file to Finance
    Then the case moves to FINANCE_FEED_SENT

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-022-01 | AC1 | Send provision inputs to Finance |
| TC-E6-022-02 | AC2 | Rule R-WO-26 |
| TC-E6-022-03 | AC3 | Not recorded |
| TC-E6-022-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-022-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-023 Reconcile the approved and posted populations

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-11 Reconcile the approved and posted populations |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-09 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to compare what the committee approved to what was posted, and raise every difference, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Reconcile the approved and posted populations

  Scenario: AC1 Reconcile the approved and posted populations
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then compares what the committee approved to what was posted, and raises every difference
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-13
    Given a case in state ESCALATED_TO_CREDIT_COMMITTEE
    When credit committee approved
    Then record the final call and release the case to posting
    Then the case moves to APPROVED

  Scenario: AC3 Rule R-WO-15
    Given a case in state WITH_COMMITTEE
    When committee approved
    Then record the final call, the approver and the limit applied, and release to posting
    Then the case moves to APPROVED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-023-01 | AC1 | Reconcile the approved and posted populations |
| TC-E6-023-02 | AC2 | Rule R-WO-13 |
| TC-E6-023-03 | AC3 | Rule R-WO-15 |
| TC-E6-023-04 | AC4 | Not recorded |
| TC-E6-023-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-023-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-024 Work the write-off exception loop

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-12 Work the write-off exception loop |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-WOF-11 |
| Decision | None |

**Story.** As a write-off committee member, I want to open the exception path for a case the rules cannot clear, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Work the write-off exception loop

  Scenario: AC1 Work the write-off exception loop
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the exception path for a case the rules cannot clear. This loop has no owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-24
    Given a case in state POSTING_REJECTED
    When retry limit reached
    Then raise the write-off exception for correction
    Then the case moves to WRITEOFF_EXCEPTION

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-024-01 | AC1 | Work the write-off exception loop |
| TC-E6-024-02 | AC2 | Rule R-WO-24 |
| TC-E6-024-03 | AC3 | Not recorded |
| TC-E6-024-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-024-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-025 Close the case after the retention period

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-13 Close the case after the retention period |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-17 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to close the case once the retention period has run and no action is open, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Close the case after the retention period

  Scenario: AC1 Close the case after the retention period
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then closes the case once the retention period has run and no action is open
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-36
    Given a case in state PLACED_WITH_AGENCY
    When placement term expired
    Then close the placement and start the retention timer
    Then the case moves to RETENTION_RUNNING

  Scenario: AC3 Rule R-WO-47
    Given a case in state RETENTION_RUNNING
    When retention timer expired
    Then close the case, stop every timer and write the closing entry with cash recovered and loss
    Then the case moves to CASE_CLOSED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-025-01 | AC1 | Close the case after the retention period |
| TC-E6-025-02 | AC2 | Rule R-WO-36 |
| TC-E6-025-03 | AC3 | Rule R-WO-47 |
| TC-E6-025-04 | AC4 | Not recorded |
| TC-E6-025-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-025-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-026 Change the eligibility or tax criteria

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-14 Change the eligibility or tax criteria |
| Process | See module |
| Priority | Should |
| Depends on | FEAT-CWC-14 |
| Decision | None |

**Story.** As a center of excellence analyst, I want the Workbench to let the center of excellence change the criteria as a versioned rule load, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Change the eligibility or tax criteria

  Scenario: AC1 Change the eligibility or tax criteria
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the center of excellence change the criteria as a versioned rule load
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-01
    Given a case in state SCAN_DUE
    When monthly scan started
    Then test every open case against the eligibility rule on both tracks and the tax criteria
    Then the case moves to POPULATION_PROPOSED

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-026-01 | AC1 | Change the eligibility or tax criteria |
| TC-E6-026-02 | AC2 | Rule R-WO-01 |
| TC-E6-026-03 | AC3 | Not recorded |
| TC-E6-026-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-026-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-027 Record a customer payment after charge-off

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-15 Record a customer payment after charge-off |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-01 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to take a payment on a charged-off balance, apply it and record the recovery, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Record a customer payment after charge-off

  Scenario: AC1 Record a customer payment after charge-off
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes a payment on a charged-off balance, applies it and records the recovery
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-37
    Given a case in state PLACED_WITH_AGENCY
    When payment received after chargeoff
    Then post the recovery as post charge-off income and calculate the agency fee
    Then the case moves to PAYMENT_MATCHED

  Scenario: AC3 Rule R-WO-49
    Given a case in state CASE_CLOSED
    When payment received after chargeoff
    Then post the recovery as post charge-off income against the closed case
    Then the case moves to PAYMENT_MATCHED

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-027-01 | AC1 | Record a customer payment after charge-off |
| TC-E6-027-02 | AC2 | Rule R-WO-37 |
| TC-E6-027-03 | AC3 | Rule R-WO-49 |
| TC-E6-027-04 | AC4 | Not recorded |
| TC-E6-027-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-027-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-028 Sell a post charge-off population

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S7 Write-off and recovery |
| Feature | FEAT-WOF-16 Sell a post charge-off population |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DBS-09 |
| Decision | None |

**Story.** As a debt sale officer, I want to open the sale of charged-off accounts, with the approval the limit requires, so that write-offs follow the criteria and the committee's decision.

**Acceptance criteria**

```gherkin
Feature: Sell a post charge-off population

  Scenario: AC1 Sell a post charge-off population
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the sale of charged-off accounts, with the approval the limit requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-12
    Given a case in state PACK_PREPARED
    When limit exceeded
    Then route the pack to the credit approval committee chaired by the product head with Risk
    Then the case moves to ESCALATED_TO_CREDIT_COMMITTEE

  Scenario: AC3 Rule R-WO-32
    Given a case in state PLACEMENT_DECIDED
    When sale selected
    Then hand the charged-off population to the debt sale route
    Then the case moves to SOLD_POST_CHARGEOFF

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/write-offs/{writeOffId}/committee-decision | Write-off and posting A |
| POST | /api/recovery/v1/write-off-scans | Write-off and posting C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-27 Write-off proposal | Scan; proposed; in committee; approved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | A | RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE |
| Write-off and posting | C | RW-WRITEOFF, RW-CREDITAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-028-01 | AC1 | Sell a post charge-off population |
| TC-E6-028-02 | AC2 | Rule R-WO-12 |
| TC-E6-028-03 | AC3 | Rule R-WO-32 |
| TC-E6-028-04 | AC4 | Not recorded |
| TC-E6-028-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-028-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-001 Run X1 dispute and complaint end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-01 Run X1 dispute and complaint end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-04 |
| Decision | None |

**Story.** As a complaint officer, I want to take the dispute from detection through the evidence pack to resolution and the return point, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X1 dispute and complaint end to end

  Scenario: AC1 Run X1 dispute and complaint end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the dispute from detection through the evidence pack to resolution and the return point
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-06 Raise deviation | Form; saved |
| SCR-08 Deviation queue | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-001-01 | AC1 | Run X1 dispute and complaint end to end |
| TC-E7-001-02 | AC2 | Not recorded |
| TC-E7-001-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-001-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-002 Run X2 vulnerability and hardship end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-02 Run X2 vulnerability and hardship end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-04 |
| Decision | None |

**Story.** As a hardship and vulnerability specialist, I want to take the case to the specialist queue with contact limits, through to the hardship decision, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X2 vulnerability and hardship end to end

  Scenario: AC1 Run X2 vulnerability and hardship end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the case to the specialist queue with contact limits, through to the hardship decision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DEV-17
    Given a case in state DEV_WITH_OWNER
    When contact not found
    Then route to escalation or to the route decision
    Then the case moves to DEV_REROUTE

  Scenario: AC3 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| queue | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | DF-WRK-001 to DF-WRK-008 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-002-01 | AC1 | Run X2 vulnerability and hardship end to end |
| TC-E7-002-02 | AC2 | Rule R-DEV-17 |
| TC-E7-002-03 | AC3 | Not recorded |
| TC-E7-002-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-002-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-003 Run X3 deceased customer end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-03 Run X3 deceased customer end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-04 |
| Decision | None |

**Story.** As a hardship and vulnerability specialist, I want to stop contact, notify heirs, file the insurance claim and settles the estate position, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X3 deceased customer end to end

  Scenario: AC1 Run X3 deceased customer end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then stops contact, notifies heirs, files the insurance claim and settles the estate position
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DEV-03
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then assign to the specialist; Legal joins X3 for the estate claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-06
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then agent handles within policy; a person approves an insurance claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-003-01 | AC1 | Run X3 deceased customer end to end |
| TC-E7-003-02 | AC2 | Rule R-DEV-03 |
| TC-E7-003-03 | AC3 | Rule R-DEV-06 |
| TC-E7-003-04 | AC4 | Not recorded |
| TC-E7-003-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-003-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-004 Run X4 fraud end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-04 Run X4 fraud end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-04 |
| Decision | None |

**Story.** As a fraud investigator, I want to refer to the fraud team, track the investigation and route the case on the outcome, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X4 fraud end to end

  Scenario: AC1 Run X4 fraud end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then refers to the fraud team, tracks the investigation and routes the case on the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-004-01 | AC1 | Run X4 fraud end to end |
| TC-E7-004-02 | AC2 | Not recorded |
| TC-E7-004-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-004-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-005 Run X5 bankruptcy and seizure end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-05 Run X5 bankruptcy and seizure end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-04 |
| Decision | None |

**Story.** As the Legal counsel, I want to stop direct collection and file the claim with the receiver or the LED before the deadline, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X5 bankruptcy and seizure end to end

  Scenario: AC1 Run X5 bankruptcy and seizure end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then stops direct collection and files the claim with the receiver or the LED before the deadline
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DEV-05
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then assign to Legal; file with the official receiver or the LED before the deadline
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-15
    Given a case in state DEV_WITH_OWNER
    When bankruptcy filed
    Then route to litigation, then to write-off after the receiver reports
    Then the case moves to DEV_REROUTE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-005-01 | AC1 | Run X5 bankruptcy and seizure end to end |
| TC-E7-005-02 | AC2 | Rule R-DEV-05 |
| TC-E7-005-03 | AC3 | Rule R-DEV-15 |
| TC-E7-005-04 | AC4 | Not recorded |
| TC-E7-005-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-005-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-006 Run X6 lost contact and skip trace end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-06 Run X6 lost contact and skip trace end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVF-01 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to run the skip trace through the bureau, internal data and agency sources and route on the result, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X6 lost contact and skip trace end to end

  Scenario: AC1 Run X6 lost contact and skip trace end to end
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the skip trace through the bureau, internal data and agency sources and routes on the result
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-006-01 | AC1 | Run X6 lost contact and skip trace end to end |
| TC-E7-006-02 | AC2 | Not recorded |
| TC-E7-006-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-006-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-007 Run X7 collateral event end to end

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-07 Run X7 collateral event end to end |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-GUA-08 |
| Decision | None |

**Story.** As a case owner, I want to file the insurance claim, re-appraises the collateral and return the case to the route decision, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Run X7 collateral event end to end

  Scenario: AC1 Run X7 collateral event end to end
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then files the insurance claim, re-appraises the collateral and returns the case to the route decision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DEV-06
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then agent handles within policy; a person approves an insurance claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-12
    Given a case in state DEV_WITH_OWNER
    When estate confirmed
    Then return to the route decision against the estate
    Then the case moves to DEV_REROUTE

  Scenario: AC4 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 4 more | DF-COL-018 to DF-COL-027 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-007-01 | AC1 | Run X7 collateral event end to end |
| TC-E7-007-02 | AC2 | Rule R-DEV-06 |
| TC-E7-007-03 | AC3 | Rule R-DEV-12 |
| TC-E7-007-04 | AC4 | Not recorded |
| TC-E7-007-05 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-007-06 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-008 Review an override

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-08 Review an override |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-APD-07 |
| Decision | None |

**Story.** As a risk and model risk officer, I want to put overrides in front of the review forum, with the reason and the outcome of each, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Review an override

  Scenario: AC1 Review an override
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts overrides in front of the review forum, with the reason and the outcome of each
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-06 Raise deviation | Form; saved |
| SCR-08 Deviation queue | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-008-01 | AC1 | Review an override |
| TC-E7-008-02 | AC2 | Not recorded |
| TC-E7-008-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-008-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-009 Match a complaint to the preceding contact

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-09 Match a complaint to the preceding contact |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-05 |
| Decision | None |

**Story.** As a conduct and QA officer, I want to link each complaint to the contact that caused it, which is how conduct is measured, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Match a complaint to the preceding contact

  Scenario: AC1 Match a complaint to the preceding contact
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then links each complaint to the contact that caused it, which is how conduct is measured
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-009-01 | AC1 | Match a complaint to the preceding contact |
| TC-E7-009-02 | AC2 | Not recorded |
| TC-E7-009-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-009-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-010 Handle a contact sent while a block is on

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S8 Deviation handling |
| Feature | FEAT-DVF-10 Handle a contact sent while a block is on |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-06 |
| Decision | None |

**Story.** As a conduct and QA officer, I want to open the breach path when a message goes out against a contact stop, so that every deviation has a handler and a clock.

**Acceptance criteria**

```gherkin
Feature: Handle a contact sent while a block is on

  Scenario: AC1 Handle a contact sent while a block is on
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the breach path when a message goes out against a contact stop
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/deviations | Case record U |
| PATCH | /api/recovery/v1/deviations/{deviationId} | Case record U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-08 Deviation queue | Loading; list |
| SCR-06 Raise deviation | Form; saved |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | U | RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF and 4 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-S8-001 | Information | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-010-01 | AC1 | Handle a contact sent while a block is on |
| TC-E7-010-02 | AC2 | Not recorded |
| TC-E7-010-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-010-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-029 Onboard a partner and set terms

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-01 Onboard a partner and set terms |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-13 |
| Decision | None |

**Story.** As a partner and agency manager, I want to take a partner onto the panel with its contract, fee schedule, service levels and scope, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Onboard a partner and set terms

  Scenario: AC1 Onboard a partner and set terms
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a partner onto the panel with its contract, fee schedule, service levels and scope
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-029-01 | AC1 | Onboard a partner and set terms |
| TC-E6-029-02 | AC2 | Not recorded |
| TC-E6-029-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-029-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-030 Hold the partner panel and fee schedule as data

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-02 Hold the partner panel and fee schedule as data |
| Process | See module |
| Priority | Should |
| Depends on | FEAT-CWC-23 |
| Decision | None |

**Story.** As a reference data administrator, I want to keep every panel, fee schedule and service level as versioned reference data, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Hold the partner panel and fee schedule as data

  Scenario: AC1 Hold the partner panel and fee schedule as data
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then keeps every panel, fee schedule and service level as versioned reference data
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-030-01 | AC1 | Hold the partner panel and fee schedule as data |
| TC-E6-030-02 | AC2 | Not recorded |
| TC-E6-030-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-030-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-031 Allocate work by measured return

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-03 Allocate work by measured return |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-02 |
| Decision | None |

**Story.** As a partner and agency manager, I want the Workbench to place work with the partner the scorecard rule picks, not by rotation or habit, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Allocate work by measured return

  Scenario: AC1 Allocate work by measured return
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then places work with the partner the scorecard rule picks, not by rotation or habit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/instructions | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-031-01 | AC1 | Allocate work by measured return |
| TC-E6-031-02 | AC2 | Not recorded |
| TC-E6-031-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-031-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-032 Override an allocation with a reason

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-04 Override an allocation with a reason |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-03 |
| Decision | None |

**Story.** As a partner and agency manager, I want the Workbench to let the partner manager place work differently, with the reason recorded, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Override an allocation with a reason

  Scenario: AC1 Override an allocation with a reason
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the partner manager place work differently, with the reason recorded
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/instructions | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-35 Placement and allocation | Loading; list |
| SCR-34 Partner list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-032-01 | AC1 | Override an allocation with a reason |
| TC-E6-032-02 | AC2 | Not recorded |
| TC-E6-032-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-032-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-033 Receive a partner result into the case

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-05 Receive a partner result into the case |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-03 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to take contact, promise and cash results from the portal onto the case the same day, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Receive a partner result into the case

  Scenario: AC1 Receive a partner result into the case
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes contact, promise and cash results from the portal onto the case the same day
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 7 more | DF-INT-001 to DF-INT-013 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-033-01 | AC1 | Receive a partner result into the case |
| TC-E6-033-02 | AC2 | Not recorded |
| TC-E6-033-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-033-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-034 Place a charged-off account with an agency

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-06 Place a charged-off account with an agency |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-03 |
| Decision | None |

**Story.** As a partner and agency manager, I want to place post charge-off accounts with an agency under the placement rule, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Place a charged-off account with an agency

  Scenario: AC1 Place a charged-off account with an agency
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then places post charge-off accounts with an agency under the placement rule
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-35 Placement and allocation | Loading; list |
| SCR-34 Partner list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-034-01 | AC1 | Place a charged-off account with an agency |
| TC-E6-034-02 | AC2 | Not recorded |
| TC-E6-034-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-034-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-035 Match a recovery and calculate the agency fee

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-07 Match a recovery and calculate the agency fee |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-01 |
| Decision | None |

**Story.** As a partner and agency manager, I want the Workbench to match money recovered by an agency to the case and work out the fee due, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Match a recovery and calculate the agency fee

  Scenario: AC1 Match a recovery and calculate the agency fee
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches money recovered by an agency to the case and works out the fee due
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-35 Placement and allocation | Loading; list |
| SCR-34 Partner list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-035-01 | AC1 | Match a recovery and calculate the agency fee |
| TC-E6-035-02 | AC2 | Not recorded |
| TC-E6-035-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-035-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-011 Score partners monthly

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-08 Score partners monthly |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-05 |
| Decision | None |

**Story.** As a partner and agency manager, I want the Workbench to build the scorecard from the measured results and publish it to the panel, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Score partners monthly

  Scenario: AC1 Score partners monthly
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the scorecard from the measured results and publishes it to the panel
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-36 Partner scorecard | Loading; scored |
| SCR-34 Partner list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-011-01 | AC1 | Score partners monthly |
| TC-E7-011-02 | AC2 | Not recorded |
| TC-E7-011-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-011-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-012 Approve partner fees

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-09 Approve partner fees |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-07 |
| Decision | None |

**Story.** As a partner and agency manager, I want to check the fee claim against the schedule and the result, and approve it, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Approve partner fees

  Scenario: AC1 Approve partner fees
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then checks the fee claim against the schedule and the result, and approves it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/instructions | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-012-01 | AC1 | Approve partner fees |
| TC-E7-012-02 | AC2 | Not recorded |
| TC-E7-012-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-012-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-013 Hold a partner review

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-10 Hold a partner review |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-08 |
| Decision | None |

**Story.** As a partner and agency manager, I want to run the review against the six points every partner type is managed on, and record the actions, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Hold a partner review

  Scenario: AC1 Hold a partner review
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs the review against the six points every partner type is managed on, and records the actions
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-013-01 | AC1 | Hold a partner review |
| TC-E7-013-02 | AC2 | Not recorded |
| TC-E7-013-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-013-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-014 Issue a notice on a missed target

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-11 Issue a notice on a missed target |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-08 |
| Decision | None |

**Story.** As a partner and agency manager, I want to send the contractual notice when a partner misses its targets, and start the cure period, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Issue a notice on a missed target

  Scenario: AC1 Issue a notice on a missed target
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then sends the contractual notice when a partner misses its targets, and starts the cure period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/instructions | Partner portal C |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | C | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-014-01 | AC1 | Issue a notice on a missed target |
| TC-E7-014-02 | AC2 | Not recorded |
| TC-E7-014-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-014-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-015 End a partner contract and recall the work

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-12 End a partner contract and recall the work |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-11 |
| Decision | None |

**Story.** As a partner and agency manager, I want to close the contract and pulls every open case back for re-selection, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: End a partner contract and recall the work

  Scenario: AC1 End a partner contract and recall the work
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then closes the contract and pulls every open case back for re-selection
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/instructions | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-35 Placement and allocation | Loading; list |
| SCR-34 Partner list | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-015-01 | AC1 | End a partner contract and recall the work |
| TC-E7-015-02 | AC2 | Not recorded |
| TC-E7-015-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-015-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-016 Check partner conduct

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-13 Check partner conduct |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PRM-08 |
| Decision | None |

**Story.** As a conduct and QA officer, I want the Workbench to sample partner contacts and complaints against the conduct rules and raise breaches, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Check partner conduct

  Scenario: AC1 Check partner conduct
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then samples partner contacts and complaints against the conduct rules and raises breaches
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partner/instructions | Partner portal R |
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-016-01 | AC1 | Check partner conduct |
| TC-E7-016-02 | AC2 | Not recorded |
| TC-E7-016-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-016-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-017 Manage extra costs and services on an asset

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-14 Manage extra costs and services on an asset |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-AST-07 |
| Decision | None |

**Story.** As a partner and agency manager, I want to record and approve additional partner costs on a held asset, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Manage extra costs and services on an asset

  Scenario: AC1 Manage extra costs and services on an asset
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records and approves additional partner costs on a held asset
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| SCR-35 Placement and allocation | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-017-01 | AC1 | Manage extra costs and services on an asset |
| TC-E7-017-02 | AC2 | Not recorded |
| TC-E7-017-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-017-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E7-018 Capture field work through the field app

| Item | Value |
|---|---|
| Epic | E7, release 31 May 2027 |
| Module | S9 Partner management |
| Feature | FEAT-PRM-15 Capture field work through the field app |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-21 |
| Decision | None |

**Story.** As a field collector, I want the Workbench to let the field collector record visits, photos and bills against the case from the field, so that partners are placed, paid and measured by rule.

**Acceptance criteria**

```gherkin
Feature: Capture field work through the field app

  Scenario: AC1 Capture field work through the field app
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the field collector record visits, photos and bills against the case from the field
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U |
| GET | /api/recovery/v1/partners | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-35 Placement and allocation | Loading; list |
| PRT-02 Instruction | New; accepted; in progress; result; closed |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | U | RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-AGENCYMG, PT-AGENCY and 5 more |
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E7-018-01 | AC1 | Capture field work through the field app |
| TC-E7-018-02 | AC2 | Not recorded |
| TC-E7-018-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E7-018-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-035 View the offer on LINE and web

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-01 View the offer on LINE and web |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-OCC-04 |
| Decision | None |

**Story.** As a customer (borrower), I want the Workbench to let the customer see the offer the bank has made, on the channel they use, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: View the offer on LINE and web

  Scenario: AC1 View the offer on LINE and web
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the customer see the offer the bank has made, on the channel they use
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-002 | Error | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-035-01 | AC1 | View the offer on LINE and web |
| TC-E4-035-02 | AC2 | Not recorded |
| TC-E4-035-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-035-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-036 Accept an offer in self-service

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-02 Accept an offer in self-service |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-COM-01 |
| Decision | None |

**Story.** As a customer (borrower), I want the Workbench to let the customer accept without a call or a branch visit, which records the acceptance on the case, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Accept an offer in self-service

  Scenario: AC1 Accept an offer in self-service
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the customer accept without a call or a branch visit, which records the acceptance on the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-002 | Error | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-036-01 | AC1 | Accept an offer in self-service |
| TC-E4-036-02 | AC2 | Not recorded |
| TC-E4-036-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-036-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-037 Pay in self-service

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-03 Pay in self-service |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-COM-01 |
| Decision | None |

**Story.** As a customer (borrower), I want the Workbench to let the customer pay against the plan or the settlement from the same screen, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Pay in self-service

  Scenario: AC1 Pay in self-service
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the customer pay against the plan or the settlement from the same screen
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | Error | The customer has not consented to {channel}. Use another channel. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-037-01 | AC1 | Pay in self-service |
| TC-E4-037-02 | AC2 | Not recorded |
| TC-E4-037-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-037-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-038 Raise a dispute in self-service

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-04 Raise a dispute in self-service |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DVH-05 |
| Decision | None |

**Story.** As a customer (borrower), I want the Workbench to let the customer raise a dispute, which opens X1 and apply the contact stop, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Raise a dispute in self-service

  Scenario: AC1 Raise a dispute in self-service
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the customer raise a dispute, which opens X1 and applies the contact stop
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | Error | The customer has not consented to {channel}. Use another channel. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-038-01 | AC1 | Raise a dispute in self-service |
| TC-E4-038-02 | AC2 | Not recorded |
| TC-E4-038-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-038-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-039 Maintain the contact repository

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-05 Maintain the contact repository |
| Process | See module |
| Priority | Should |
| Depends on | FEAT-RDF-04 |
| Decision | None |

**Story.** As a compliance and PDPA officer, I want to keep the verified contact points for every party, with consent state per channel, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Maintain the contact repository

  Scenario: AC1 Maintain the contact repository
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then keeps the verified contact points for every party, with consent state per channel
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| party | id, cif_no, party_type, first_name, last_name, id_type and 6 more | DF-PTY-001 to DF-PTY-012 |
| contact_point | id, party_id, channel, value_token, source, consent_status and 2 more | DF-PTY-013 to DF-PTY-020 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-002 | Error | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-039-01 | AC1 | Maintain the contact repository |
| TC-E4-039-02 | AC2 | Not recorded |
| TC-E4-039-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-039-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-040 Record a custody movement of a document

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-06 Record a custody movement of a document |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-19 |
| Decision | None |

**Story.** As the Legal counsel, I want the Workbench to track a physical document leaving and returning, so the original is never lost, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Record a custody movement of a document

  Scenario: AC1 Record a custody movement of a document
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tracks a physical document leaving and returning, so the original is never lost
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| document_custody | id, document_id, moved_at, from_location, to_location, held_by and 1 more | DF-DOC-018 to DF-DOC-024 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | Confirmation | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-040-01 | AC1 | Record a custody movement of a document |
| TC-E4-040-02 | AC2 | Not recorded |
| TC-E4-040-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-040-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-041 Answer a legal or audit document request

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-07 Answer a legal or audit document request |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-06 |
| Decision | None |

**Story.** As the Legal counsel, I want to return the documents and the index entries a legal or audit request asks for, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Answer a legal or audit document request

  Scenario: AC1 Answer a legal or audit document request
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then returns the documents and the index entries a legal or audit request asks for
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | Confirmation | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-041-01 | AC1 | Answer a legal or audit document request |
| TC-E4-041-02 | AC2 | Not recorded |
| TC-E4-041-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-041-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-042 Apply retention on case closure

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P6 Communications |
| Feature | FEAT-COM-08 Apply retention on case closure |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-DCM-17 |
| Decision | None |

**Story.** As a compliance and PDPA officer, I want the Workbench to apply the retention class to every document on the case when the case closes, so that every notice is sent from an approved template with proof of delivery.

**Acceptance criteria**

```gherkin
Feature: Apply retention on case closure

  Scenario: AC1 Apply retention on case closure
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the retention class to every document on the case when the case closes
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C |
| GET | /api/recovery/v1/notices/{noticeId} | Litigation R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-33 Template approval | Draft; approved; withdrawn |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Litigation | C | RW-LITOFF, RW-ENFORCE |
| Litigation | R | RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 22 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P6-003 | Warning | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | Confirmation | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | Error | Contact with this customer is stopped for {reason}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-042-01 | AC1 | Apply retention on case closure |
| TC-E4-042-02 | AC2 | Not recorded |
| TC-E4-042-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-042-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-043 Match a settlement payment

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-03 Match a settlement payment |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-01 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to match a settlement payment to the treatment and close the money side, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Match a settlement payment

  Scenario: AC1 Match a settlement payment
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches a settlement payment to the treatment and closes the money side
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/proceeds | Write-off and posting R |
| POST | /api/recovery/v1/proceeds/{proceedsId}/match | Write-off and posting U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | R | RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK and 9 more |
| Write-off and posting | U | RW-WRITEOFF, RW-CREDITAD, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-043-01 | AC1 | Match a settlement payment |
| TC-E4-043-02 | AC2 | Not recorded |
| TC-E4-043-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-043-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-044 Match auction and enforcement proceeds

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-04 Match auction and enforcement proceeds |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-01 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to match money from an auction, a broker or the LED to the right case, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Match auction and enforcement proceeds

  Scenario: AC1 Match auction and enforcement proceeds
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches money from an auction, a broker or the LED to the right case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/proceeds | Write-off and posting R |
| POST | /api/recovery/v1/proceeds/{proceedsId}/match | Write-off and posting U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | R | RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK and 9 more |
| Write-off and posting | U | RW-WRITEOFF, RW-CREDITAD, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-044-01 | AC1 | Match auction and enforcement proceeds |
| TC-E4-044-02 | AC2 | Not recorded |
| TC-E4-044-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-044-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-045 Calculate fees and charges

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-05 Calculate fees and charges |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CWC-23 |
| Decision | None |

**Story.** As a finance and CFO delegate, I want the Workbench to work out partner fees, court fees and charge from the fee tables held as data, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Calculate fees and charges

  Scenario: AC1 Calculate fees and charges
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then works out partner fees, court fees and charges from the fee tables held as data
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-045-01 | AC1 | Calculate fees and charges |
| TC-E4-045-02 | AC2 | Not recorded |
| TC-E4-045-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-045-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-046 Post a settlement booking to ALS

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-06 Post a settlement booking to ALS |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-CHO-08 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to write the agreed settlement terms to ALS and read the booked position back, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Post a settlement booking to ALS

  Scenario: AC1 Post a settlement booking to ALS
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the agreed settlement terms to ALS and reads the booked position back
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-046-01 | AC1 | Post a settlement booking to ALS |
| TC-E4-046-02 | AC2 | Not recorded |
| TC-E4-046-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-046-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-047 Post to the general ledger

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-07 Post to the general ledger |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-06 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to post the accounting entries for settlements, sales and write-offs to the ledger, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Post to the general ledger

  Scenario: AC1 Post to the general ledger
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then posts the accounting entries for settlements, sales and write-offs to the ledger
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 7 more | DF-INT-001 to DF-INT-013 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-047-01 | AC1 | Post to the general ledger |
| TC-E4-047-02 | AC2 | Not recorded |
| TC-E4-047-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-047-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-036 Produce provision inputs

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-08 Produce provision inputs |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-07 |
| Decision | None |

**Story.** As a finance and CFO delegate, I want the Workbench to build the provision inputs Finance needs from the case and asset positions, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Produce provision inputs

  Scenario: AC1 Produce provision inputs
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the provision inputs Finance needs from the case and asset positions
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-036-01 | AC1 | Produce provision inputs |
| TC-E6-036-02 | AC2 | Not recorded |
| TC-E6-036-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-036-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-048 Run the deed in lieu rental auto-debit

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-09 Run the deed in lieu rental auto-debit |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-TRT-16 |
| Decision | None |

**Story.** As a sale officer, I want the Workbench to take the rental by auto-debit, issue the receipt and follow up arrears, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Run the deed in lieu rental auto-debit

  Scenario: AC1 Run the deed in lieu rental auto-debit
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes the rental by auto-debit, issues the receipt and follows up arrears
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/proceeds/{proceedsId}/match | Write-off and posting U |

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | U | RW-WRITEOFF, RW-CREDITAD, SY-DATALOAD |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-048-01 | AC1 | Run the deed in lieu rental auto-debit |
| TC-E4-048-02 | AC2 | Not recorded |
| TC-E4-048-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-048-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-049 Apply proceeds to the case balance

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-10 Apply proceeds to the case balance |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-PAY-04 |
| Decision | None |

**Story.** As a case owner, I want the Workbench to apply every receipt to the balance in the order the policy sets, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Apply proceeds to the case balance

  Scenario: AC1 Apply proceeds to the case balance
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies every receipt to the balance in the order the policy sets
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| proceeds | id, case_id, treatment_id, account_payment_id, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/proceeds/{proceedsId}/match | Write-off and posting U |
| GET | /api/recovery/v1/proceeds | Write-off and posting R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Write-off and posting | U | RW-WRITEOFF, RW-CREDITAD, SY-DATALOAD |
| Write-off and posting | R | RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK and 9 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-049-01 | AC1 | Apply proceeds to the case balance |
| TC-E4-049-02 | AC2 | Not recorded |
| TC-E4-049-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-049-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E4-050 Reconcile money movements daily

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | P8 Payments and posting |
| Feature | FEAT-PAY-11 Reconcile money movements daily |
| Process | See module |
| Priority | Must |
| Depends on | FEAT-RDF-11 |
| Decision | None |

**Story.** As the Credit Administration officer, I want the Workbench to compare what the Workbench matched to what ALS and the ledger show, every day, so that every payment and booking is matched to its case.

**Acceptance criteria**

```gherkin
Feature: Reconcile money movements daily

  Scenario: AC1 Reconcile money movements daily
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then compares what the Workbench matched to what ALS and the ledger show, every day
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 15 more | DF-ACC-001 to DF-ACC-021 |
| account_payment | id, account_id, payment_code, payment_date, payment_amount, payment_channel and 1 more | DF-ACC-022 to DF-ACC-028 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 7 more | DF-INT-001 to DF-INT-013 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

| Screen | States |
|---|---|
| SCR-28 Proceeds matching | Loading; matched; unmatched |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E4-050-01 | AC1 | Reconcile money movements daily |
| TC-E4-050-02 | AC2 | Not recorded |
| TC-E4-050-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E4-050-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E6-037 Track benefit realisation

| Item | Value |
|---|---|
| Epic | E6, release 30 April 2027 |
| Module | P9 Reporting |
| Feature | FEAT-RPT-06 Track benefit realisation |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-RPT-01 |
| Decision | None |

**Story.** As a finance and CFO delegate, I want to track the measures in the benefit model against the baseline, monthly, so that the measures come from the decision log.

**Acceptance criteria**

```gherkin
Feature: Track benefit realisation

  Scenario: AC1 Track benefit realisation
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then tracks the measures in the benefit model against the baseline, monthly
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/reports/measures | Reporting R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Reporting | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF and 28 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E6-037-01 | AC1 | Track benefit realisation |
| TC-E6-037-02 | AC2 | Not recorded |
| TC-E6-037-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E6-037-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-001 Produce regulatory returns

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P9 Reporting |
| Feature | FEAT-RPT-07 Produce regulatory returns |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-RPT-04 |
| Decision | None |

**Story.** As a compliance and PDPA officer, I want the Workbench to build the regulatory extracts from the data products and the decision log, so that the measures come from the decision log.

**Acceptance criteria**

```gherkin
Feature: Produce regulatory returns

  Scenario: AC1 Produce regulatory returns
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the regulatory extracts from the data products and the decision log
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by | DF-DOC-012 to DF-DOC-017 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/reports/measures | Reporting R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Reporting | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF and 28 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-001-01 | AC1 | Produce regulatory returns |
| TC-E8-001-02 | AC2 | Not recorded |
| TC-E8-001-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-001-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-002 Classify, stage and re-age an account

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P9 Reporting |
| Feature | FEAT-RPT-10 Classify, stage and re-age an account |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-RDF-03 |
| Decision | None |

**Story.** As a risk and model risk officer, I want the Workbench to apply the classification and re-ageing rules and recomputes the segment when they change, so that the measures come from the decision log.

**Acceptance criteria**

```gherkin
Feature: Classify, stage and re-age an account

  Scenario: AC1 Classify, stage and re-age an account
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the classification and re-ageing rules and recomputes the segment when they change
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by | DF-DOC-012 to DF-DOC-017 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/reports/measures | Reporting R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Reporting | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF and 28 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-002-01 | AC1 | Classify, stage and re-age an account |
| TC-E8-002-02 | AC2 | Not recorded |
| TC-E8-002-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-002-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-030 Change an autonomy level

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-12 Change an autonomy level |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-CWC-22 |
| Decision | None |

**Story.** As a risk and model risk officer, I want to change the autonomy level for one agent and one decision, as a versioned configuration row, so that agents prepare the work and people decide where they must.

**Acceptance criteria**

```gherkin
Feature: Change an autonomy level

  Scenario: AC1 Change an autonomy level
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then changes the autonomy level for one agent and one decision, as a versioned configuration row
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/agent-runs | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-46 Agent monitor | Shadow; live; paused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-030-01 | AC1 | Change an autonomy level |
| TC-E3-030-02 | AC2 | Not recorded |
| TC-E3-030-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-030-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E3-031 Detect model drift and raise a decision

| Item | Value |
|---|---|
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-13 Detect model drift and raise a decision |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-AGT-06 |
| Decision | None |

**Story.** As a risk and model risk officer, I want the Workbench to watch calibration and drift, and raise a decision with an owner and a date on a breach, so that agents prepare the work and people decide where they must.

**Acceptance criteria**

```gherkin
Feature: Detect model drift and raise a decision

  Scenario: AC1 Detect model drift and raise a decision
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then watches calibration and drift, and raises a decision with an owner and a date on a breach
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E3-031-01 | AC1 | Detect model drift and raise a decision |
| TC-E3-031-02 | AC2 | Not recorded |
| TC-E3-031-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E3-031-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-003 Run a champion and challenger test

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-14 Run a champion and challenger test |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-AGT-05 |
| Decision | None |

**Story.** As a center of excellence analyst, I want to run two rule or model versions side by side and compare the outcome, so that agents prepare the work and people decide where they must.

**Acceptance criteria**

```gherkin
Feature: Run a champion and challenger test

  Scenario: AC1 Run a champion and challenger test
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs two rule or model versions side by side and compares the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

None. The work runs as a service or a scheduled job inside the recovery module.

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-003-01 | AC1 | Run a champion and challenger test |
| TC-E8-003-02 | AC2 | Not recorded |
| TC-E8-003-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-003-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-004 Raise or lower an autonomy level with approval

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-15 Raise or lower an autonomy level with approval |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-AGT-12 |
| Decision | None |

**Story.** As a risk and model risk officer, I want to step an agent up on measured evidence, and drop it on a breach, with the approval each needs, so that agents prepare the work and people decide where they must.

**Acceptance criteria**

```gherkin
Feature: Raise or lower an autonomy level with approval

  Scenario: AC1 Raise or lower an autonomy level with approval
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then steps an agent up on measured evidence, and drops it on a breach, with the approval each needs
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/agent-runs | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-46 Agent monitor | Shadow; live; paused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-004-01 | AC1 | Raise or lower an autonomy level with approval |
| TC-E8-004-02 | AC2 | Not recorded |
| TC-E8-004-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-004-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-005 Review agent risk at the committee

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-16 Review agent risk at the committee |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-AGT-06 |
| Decision | None |

**Story.** As a risk and model risk officer, I want to put agent performance, overrides and incidents in front of the strategy and model committee, so that agents prepare the work and people decide where they must.

**Acceptance criteria**

```gherkin
Feature: Review agent risk at the committee

  Scenario: AC1 Review agent risk at the committee
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts agent performance, overrides and incidents in front of the strategy and model committee
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/agent-runs | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-46 Agent monitor | Shadow; live; paused |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-005-01 | AC1 | Review agent risk at the committee |
| TC-E8-005-02 | AC2 | Not recorded |
| TC-E8-005-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-005-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-006 Run the full administration screens

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-01 Run the full administration screens |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-CWC-22 |
| Decision | None |

**Story.** As a platform administrator, I want to give administration one place for roles, queues, parameters, templates, panels and autonomy, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Run the full administration screens

  Scenario: AC1 Run the full administration screens
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then gives administration one place for roles, queues, parameters, templates, panels and autonomy
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| queue | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | DF-WRK-001 to DF-WRK-008 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/reference-loads | Reference data C |
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Reference data | C | RW-COE, RW-REFADM |
| Rules and parameters | C | RW-COE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-006-01 | AC1 | Run the full administration screens |
| TC-E8-006-02 | AC2 | Not recorded |
| TC-E8-006-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-006-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-007 Change a decision rule through the administration screens

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-02 Change a decision rule through the administration screens |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-CWC-14 |
| Decision | None |

**Story.** As a center of excellence analyst, I want the Workbench to let the center of excellence change a rule, test it and put it in force as a new version, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Change a decision rule through the administration screens

  Scenario: AC1 Change a decision rule through the administration screens
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the center of excellence change a rule, test it and put it in force as a new version
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-007-01 | AC1 | Change a decision rule through the administration screens |
| TC-E8-007-02 | AC2 | Not recorded |
| TC-E8-007-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-007-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-008 Move an approval limit

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-03 Move an approval limit |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-ACA-06 |
| Decision | None |

**Story.** As a center of excellence analyst, I want to change a delegated limit, with Risk approving and the change versioned, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Move an approval limit

  Scenario: AC1 Move an approval limit
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then changes a delegated limit, with Risk approving and the change versioned
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| delegation_limit | id, decision_code, approval_level, product_group, principal_limit, loss_pct_limit and 5 more | DF-REF-016 to DF-REF-026 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-008-01 | AC1 | Move an approval limit |
| TC-E8-008-02 | AC2 | Not recorded |
| TC-E8-008-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-008-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-009 Set the treatment policy by product

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-04 Set the treatment policy by product |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-CWC-25 |
| Decision | None |

**Story.** As a product head (Mortgage, HP, SSME), I want the Workbench to let the product head set the bands, floors and ranges for their product, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Set the treatment policy by product

  Scenario: AC1 Set the treatment policy by product
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the product head set the bands, floors and ranges for their product
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | DF-TRT-001 to DF-TRT-014 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-009-01 | AC1 | Set the treatment policy by product |
| TC-E8-009-02 | AC2 | Not recorded |
| TC-E8-009-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-009-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-010 Add a letter template with Compliance approval

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-05 Add a letter template with Compliance approval |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-DRI-15 |
| Decision | None |

**Story.** As a center of excellence analyst, I want to add a new template through the approval path and record who approved it, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Add a letter template with Compliance approval

  Scenario: AC1 Add a letter template with Compliance approval
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then adds a new template through the approval path and records who approved it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |
| template | id, template_code, template_version, language, product_group, body_ref and 1 more | DF-REF-045 to DF-REF-051 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-010-01 | AC1 | Add a letter template with Compliance approval |
| TC-E8-010-02 | AC2 | Not recorded |
| TC-E8-010-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-010-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-011 Roll back a configuration version

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-06 Roll back a configuration version |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-CWC-15 |
| Decision | None |

**Story.** As a platform administrator, I want to return any versioned table to its previous version and record the rollback, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Roll back a configuration version

  Scenario: AC1 Roll back a configuration version
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then returns any versioned table to its previous version and records the rollback
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-011-01 | AC1 | Roll back a configuration version |
| TC-E8-011-02 | AC2 | Not recorded |
| TC-E8-011-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-011-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-012 Publish a panel change

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-07 Publish a panel change |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-PRM-02 |
| Decision | None |

**Story.** As a partner and agency manager, I want to put a partner panel change in force with an effective date, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Publish a panel change

  Scenario: AC1 Publish a panel change
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts a partner panel change in force with an effective date
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-012-01 | AC1 | Publish a panel change |
| TC-E8-012-02 | AC2 | Not recorded |
| TC-E8-012-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-012-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-013 Run a QA sample against the rule version applied

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-08 Run a QA sample against the rule version applied |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-DRI-03 |
| Decision | None |

**Story.** As a conduct and QA officer, I want to sample closed decisions and test each against the rule version that was in force, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Run a QA sample against the rule version applied

  Scenario: AC1 Run a QA sample against the rule version applied
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then samples closed decisions and tests each against the rule version that was in force
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-013-01 | AC1 | Run a QA sample against the rule version applied |
| TC-E8-013-02 | AC2 | Not recorded |
| TC-E8-013-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-013-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-014 Return a defective pack

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-09 Return a defective pack |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-LIT-05 |
| Decision | None |

**Story.** As a litigation officer, I want the Workbench to send a pack that fails the check back to its owner with the defects named, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Return a defective pack

  Scenario: AC1 Return a defective pack
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends a pack that fails the check back to its owner with the defects named
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-014-01 | AC1 | Return a defective pack |
| TC-E8-014-02 | AC2 | Not recorded |
| TC-E8-014-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-014-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-015 Detect a broken hash chain in the decision log

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-10 Detect a broken hash chain in the decision log |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-DRI-01 |
| Decision | None |

**Story.** As an internal audit, I want the Workbench to test the log chain and raise a control breach if a record does not verify, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Detect a broken hash chain in the decision log

  Scenario: AC1 Detect a broken hash chain in the decision log
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests the log chain and raises a control breach if a record does not verify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-015-01 | AC1 | Detect a broken hash chain in the decision log |
| TC-E8-015-02 | AC2 | Not recorded |
| TC-E8-015-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-015-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-016 Handle a data subject request

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-11 Handle a data subject request |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-ACA-05 |
| Decision | None |

**Story.** As a compliance and PDPA officer, I want to work a PDPA access, correction or erasure request inside the statutory period, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Handle a data subject request

  Scenario: AC1 Handle a data subject request
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then works a PDPA access, correction or erasure request inside the statutory period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-47 Personal data | Loading; list |
| SCR-39 Rules and parameters | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-016-01 | AC1 | Handle a data subject request |
| TC-E8-016-02 | AC2 | Not recorded |
| TC-E8-016-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-016-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-017 Manage an incident

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-12 Manage an incident |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-DRI-18 |
| Decision | None |

**Story.** As a platform administrator, I want to run the incident path: detect, hold, fix, record and report, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Manage an incident

  Scenario: AC1 Manage an incident
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs the incident path: detect, hold, fix, record and report
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-017-01 | AC1 | Manage an incident |
| TC-E8-017-02 | AC2 | Not recorded |
| TC-E8-017-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-017-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-018 Refer a case to Aric

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-13 Refer a case to Aric |
| Process | All recovery processes |
| Priority | Must |
| Depends on | FEAT-DVF-04 |
| Decision | None |

**Story.** As a fraud investigator, I want the Workbench to send a case to Aric where the fraud rules require it, and take the result back, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Refer a case to Aric

  Scenario: AC1 Refer a case to Aric
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends a case to Aric where the fraud rules require it, and takes the result back
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-018-01 | AC1 | Refer a case to Aric |
| TC-E8-018-02 | AC2 | Not recorded |
| TC-E8-018-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-018-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-E8-019 Control access by role and by agent

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | FEAT-ADM-14 Control access by role and by agent |
| Process | All recovery processes |
| Priority | Should |
| Depends on | FEAT-ACA-04 |
| Decision | None |

**Story.** As a security administrator, I want to review and set what each role and each agent may read and do, and report the matrix, so that access, limits and rules change without a code release.

**Acceptance criteria**

```gherkin
Feature: Control access by role and by agent

  Scenario: AC1 Control access by role and by agent
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then reviews and sets what each role and each agent may read and do, and reports the matrix
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |
| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-E8-019-01 | AC1 | Control access by role and by agent |
| TC-E8-019-02 | AC2 | Not recorded |
| TC-E8-019-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-E8-019-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---
