<!-- source: 04 User stories/Recovery Workbench Data Migration Stories v2.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench Data Migration Stories v2.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench data migration stories

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

One story per data product: extract, transform, load, reconcile and cut over.

---

## RWB-DM-001 Migrate account and arrears

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the account and arrears data product extracted, transformed, loaded and reconciled to Core bank (ALS) before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate account and arrears

  Scenario: AC1 Extract
    Given the source extract for account and arrears
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-001-01 | AC1 | Extract |
| TC-DM-001-02 | AC2 | Reconcile |
| TC-DM-001-03 | AC3 | Cutover |
| TC-DM-001-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-002 Migrate customer and party

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the customer and party data product extracted, transformed, loaded and reconciled to SCBPDM and core bank before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate customer and party

  Scenario: AC1 Extract
    Given the source extract for customer and party
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| party | id, cif_no, party_type, first_name, last_name, id_type and 7 more | DF-PTY-001 to DF-PTY-021 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-002-01 | AC1 | Extract |
| TC-DM-002-02 | AC2 | Reconcile |
| TC-DM-002-03 | AC3 | Cutover |
| TC-DM-002-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-003 Migrate case and ownership

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the case and ownership data product extracted, transformed, loaded and reconciled to Recovery Workbench before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate case and ownership

  Scenario: AC1 Extract
    Given the source extract for case and ownership
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 4 more | DF-WRK-009 to DF-WRK-040 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-003-01 | AC1 | Extract |
| TC-DM-003-02 | AC2 | Reconcile |
| TC-DM-003-03 | AC3 | Cutover |
| TC-DM-003-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-004 Migrate treatment and offers

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the treatment and offers data product extracted, transformed, loaded and reconciled to Recovery Workbench; restructure plans in ACE before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate treatment and offers

  Scenario: AC1 Extract
    Given the source extract for treatment and offers
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 19 more | DF-TRT-001 to DF-TRT-033 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-004-01 | AC1 | Extract |
| TC-DM-004-02 | AC2 | Reconcile |
| TC-DM-004-03 | AC3 | Cutover |
| TC-DM-004-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-005 Migrate contact and promises

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the contact and promises data product extracted, transformed, loaded and reconciled to EFS before day 90; the Workbench after before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate contact and promises

  Scenario: AC1 Extract
    Given the source extract for contact and promises
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |
| interaction | id, case_id, party_id, occurred_at, channel, direction and 23 more | DF-INT-001 to DF-INT-029 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-005-01 | AC1 | Extract |
| TC-DM-005-02 | AC2 | Reconcile |
| TC-DM-005-03 | AC3 | Cutover |
| TC-DM-005-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-006 Migrate collateral and assets

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the collateral and assets data product extracted, transformed, loaded and reconciled to CCMS, SVAF, AMIS, RPS before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate collateral and assets

  Scenario: AC1 Extract
    Given the source extract for collateral and assets
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| collateral | id, collateral_no, collateral_type, title_doc_no, plot_no, area_text and 7 more | DF-COL-001 to DF-COL-013 |
| valuation | id, collateral_id, asset_id, appraisal_no, appraisal_type, appraised_value and 6 more | DF-COL-018 to DF-COL-044 |
| asset | id, case_id, collateral_id, asset_ref, asset_code, asset_type and 9 more | DF-COL-028 to DF-COL-042 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-006-01 | AC1 | Extract |
| TC-DM-006-02 | AC2 | Reconcile |
| TC-DM-006-03 | AC3 | Cutover |
| TC-DM-006-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-007 Migrate legal events and cases

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the legal events and cases data product extracted, transformed, loaded and reconciled to LIT for court records; the Workbench for instructions before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate legal events and cases

  Scenario: AC1 Extract
    Given the source extract for legal events and cases
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/data-products/{productCode}/records | Case record R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Case record | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-007-01 | AC1 | Extract |
| TC-DM-007-02 | AC2 | Reconcile |
| TC-DM-007-03 | AC3 | Cutover |
| TC-DM-007-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-008 Migrate partner performance

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the partner performance data product extracted, transformed, loaded and reconciled to Recovery Workbench before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate partner performance

  Scenario: AC1 Extract
    Given the source extract for partner performance
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-008-01 | AC1 | Extract |
| TC-DM-008-02 | AC2 | Reconcile |
| TC-DM-008-03 | AC3 | Cutover |
| TC-DM-008-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-009 Migrate debt sale

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the debt sale data product extracted, transformed, loaded and reconciled to Recovery Workbench before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate debt sale

  Scenario: AC1 Extract
    Given the source extract for debt sale
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-009-01 | AC1 | Extract |
| TC-DM-009-02 | AC2 | Reconcile |
| TC-DM-009-03 | AC3 | Cutover |
| TC-DM-009-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-010 Migrate documents and extracted fields

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the documents and extracted fields data product extracted, transformed, loaded and reconciled to Recovery Workbench document hub before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate documents and extracted fields

  Scenario: AC1 Extract
    Given the source extract for documents and extracted fields
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document | id, case_id, party_id, document_type, source, storage_ref and 14 more | DF-DOC-001 to DF-DOC-033 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-010-01 | AC1 | Extract |
| TC-DM-010-02 | AC2 | Reconcile |
| TC-DM-010-03 | AC3 | Cutover |
| TC-DM-010-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-011 Migrate scores and route economics

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the scores and route economics data product extracted, transformed, loaded and reconciled to COLLINS before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate scores and route economics

  Scenario: AC1 Extract
    Given the source extract for scores and route economics
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |
| score | id, account_id, case_id, model_code, model_version, score_value and 3 more | DF-DEC-019 to DF-DEC-027 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-011-01 | AC1 | Extract |
| TC-DM-011-02 | AC2 | Reconcile |
| TC-DM-011-03 | AC3 | Cutover |
| TC-DM-011-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-012 Migrate decision log

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the decision log data product extracted, transformed, loaded and reconciled to Recovery Workbench before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate decision log

  Scenario: AC1 Extract
    Given the source extract for decision log
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 16 more | DF-DEC-001 to DF-DEC-031 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-012-01 | AC1 | Extract |
| TC-DM-012-02 | AC2 | Reconcile |
| TC-DM-012-03 | AC3 | Cutover |
| TC-DM-012-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-DM-012-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-013 Migrate money and closure

| Item | Value |
|---|---|
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the money and closure data product extracted, transformed, loaded and reconciled to Core bank (ALS) and GL before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate money and closure

  Scenario: AC1 Extract
    Given the source extract for money and closure
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-013-01 | AC1 | Extract |
| TC-DM-013-02 | AC2 | Reconcile |
| TC-DM-013-03 | AC3 | Cutover |
| TC-DM-013-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---

## RWB-DM-014 Migrate reference data

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Decision | DL25 |

**Story.** As a data steward, I want the reference data data product extracted, transformed, loaded and reconciled to Recovery Workbench before its first release, so that every case starts with complete, checked data.

**Acceptance criteria**

```gherkin
Feature: Migrate reference data

  Scenario: AC1 Extract
    Given the source extract for reference data
    When the load runs
    Then every record passes the load checks or is held in the exception list

  Scenario: AC2 Reconcile
    Given the loaded data
    When the reconciliation runs
    Then counts and balances match the source within the tolerance

  Scenario: AC3 Cutover
    Given ten clean days
    When the data steward signs off
    Then the system retires the old copy with a read-only archive
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
| loan_account | id, account_no, contract_no, product_code, product_category_efs, business_unit and 18 more | DF-ACC-001 to DF-ACC-031 |
| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A |
| GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R |

**Screen and states**

No screen in this story.

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Queue and allocation | A | RW-TEAMMGR |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Error | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-DM-014-01 | AC1 | Extract |
| TC-DM-014-02 | AC2 | Reconcile |
| TC-DM-014-03 | AC3 | Cutover |
| TC-DM-014-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables.

---
