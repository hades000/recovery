    # -*- coding: utf-8 -*-
import io, re, os

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(BASE, r"04 User stories\Recovery Workbench Administration Stories v2.md")
DST = os.path.join(BASE, r"04 User stories\Recovery Workbench Administration Stories v3.md")

doc = io.open(SRC, encoding="utf-8").read()

# ------------------------------------------------------------------ 1. intro
old_intro = ("User and role administration, reference data, rule versions, queue and timer configuration, "
             "interface monitoring and the audit log. Epic 1 builds the services and loads by file; these "
             "stories add the administration screens and approvals in Epic 8, when full administration is "
             "delivered, and partner administration in Epic 4.")
new_intro = ("User and role administration, reference data, rule versions, queue and timer configuration, "
             "job and ACE batch monitoring, and the audit log. Epic 1 builds the services and the reference "
             "and rule loads by file; these stories add the administration screens and approvals in Epic 8, "
             "when full administration is delivered, and partner administration in Epic 4.\n\n"
             "Version 3 is re-based on D-RCV-35 and ADR-010. The Workbench loads no source data: the job "
             "monitor shows Workbench jobs beside the ACE batch status, the console shows reconciliation "
             "breaks, and masking profiles name the columns of the recovery.v_ace_* views. Two stories are "
             "rewritten around the read path (RWB-AD-018, RWB-AD-019) and one is a minor edit (RWB-AD-004).")
assert old_intro in doc
doc = doc.replace(old_intro, new_intro, 1)

# ------------------------------------------------------------------ 2. summary table dependencies
doc = doc.replace("| RWB-AD-018 | Interface and job monitor | P1 | E8 | RWB-E1-056 |",
                  "| RWB-AD-018 | Interface and job monitor | P1 | E8 | RWB-E1-056, RWB-E1-069 |", 1)
doc = doc.replace("| RWB-AD-019 | Data quality and reconciliation console | P1 | E8 | RWB-E1-011 |",
                  "| RWB-AD-019 | Data quality and reconciliation console | P1 | E8 | RWB-E1-011, RWB-E1-069 |", 1)

# ------------------------------------------------------------------ 3. new sections
AD004 = """## RWB-AD-004 Masking profiles per role

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-037 |
| Decision | DL26, D-RCV-35 |

**Story.** As a Compliance and PDPA officer, I want a masking profile per role and per personal field held as data, naming the view column the masked value comes from, so that personal data is shown only to the roles allowed to see it and the clear identity number never leaves ACE.

**Acceptance criteria**

```gherkin
Feature: Masking profiles per role

  Scenario: AC1 Masked by default
    Given a role with no unmasked rule in the version in force
    When it reads a case
    Then the identity number shows from v_ace_customer.id_no_masked
    And the phone number shows from v_ace_contact.contact_value_masked

  Scenario: AC2 Unmask is logged
    Given a role allowed to unmask the contact value
    When it unmasks the phone number on a case
    Then the system fills the field from v_ace_contact.contact_value and writes the read to the PII log
    And the identity number is still shown from id_no_masked, never in clear

  Scenario: AC3 Profile change
    Given a new masking_rule version approved by Compliance
    When its valid from date arrives
    Then responses use the new version and the access log carries the version in force
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| masking_rule | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | DF-REF-198 to DF-REF-204 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |
| v_ace_customer | cif_no, person_key, first_name, last_name, id_no_masked, id_no_last4 and 14 more | DF-ACE-055 to DF-ACE-074 |
| v_ace_contact | contact_type, contact_key, person_key, contact_value, contact_value_masked and 4 more | DF-ACE-075 to DF-ACE-083 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/reference-loads | Reference data C |
| POST | /api/recovery/v1/admin/reference-loads/{loadId}/approve | Reference data A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-47 Personal data | Loading; list |
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Reference data | C | RW-COE, RW-REFADM |
| Reference data | A | RW-COMPLY |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-004-01 | AC1 | Masked by default |
| TC-AD-004-02 | AC2 | Unmask is logged |
| TC-AD-004-03 | AC3 | Profile change |
| TC-AD-004-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-004-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A masking rule names a view column, and no rule returns the clear identity number.

---

"""

AD018 = """## RWB-AD-018 Interface and job monitor

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-056, RWB-E1-069 |
| Decision | D-RCV-35 |

**Story.** As a platform administrator, I want every Workbench job and outbound action with its status, business date, duration and checks, and the last complete ACE business date per source beside it, so that a failed job is found and rerun the same morning and a late ACE batch is not mistaken for a failed job.

**Acceptance criteria**

```gherkin
Feature: Interface and job monitor

  Scenario: AC1 Workbench jobs and their ACE date
    Given the jobs of the job catalog and the outbound actions for 2026-11-30
    When I open the monitor
    Then each shows its job ID, business date, status, duration and the result of each check
    And each job that reads ACE shows the last complete business date of its source from v_ace_batch_status

  Scenario: AC2 Rerun a Workbench job
    Given a failed Workbench job
    When I rerun it from its run book after the cause is fixed
    Then the job runs again and both runs are in the job log

  Scenario: AC3 A late ACE batch
    Given v_ace_batch_status shows EFS for business date 2026-12-01 with status FAILED
    When the dependent job reaches its schedule
    Then the job is recorded WAITING and is not rerun
    And its data product shows STALE with MSG-P1-001
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| job_catalog | id, job_id, job_name, owner_role, schedule_text, expected_minutes, alert_after_minutes, first_release | DF-OPS-224 to DF-OPS-232 |
| data_product_load | id, product_code, source_system, business_date, loaded_at, status, stale_flagged_at | DF-OPS-001 to DF-OPS-008 |
| v_ace_batch_status | source_system, business_date, started_at, completed_at, status, record_count and 3 more | DF-ACE-178 to DF-ACE-186 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/jobs | Platform administration R |
| POST | /api/recovery/v1/admin/jobs/{jobId}/rerun | Platform administration U |
| GET | /api/recovery/v1/data-products/freshness | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-44 Interface and job monitor | Running; failed; waiting for the ACE batch; complete |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |
| Platform administration | U | RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-018-01 | AC1 | Workbench jobs and their ACE date |
| TC-AD-018-02 | AC2 | Rerun a Workbench job |
| TC-AD-018-03 | AC3 | A late ACE batch |
| TC-AD-018-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views, and ACE batch status only through v_ace_batch_status. No ACE batch is rerun from the Workbench: ACE ingestion owns the source runs, and the Workbench records the dependent job as WAITING.

---

"""

AD019 = """## RWB-AD-019 Data quality and reconciliation console

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-011, RWB-E1-015, RWB-E1-069 |
| Decision | D-RCV-35 |

**Story.** As a data steward, I want the reconciliation breaks of REC-01 to REC-05, the referential completeness of every business key and the stale data products on one screen, so that I fix data problems before they reach a decision.

**Acceptance criteria**

```gherkin
Feature: Data quality and reconciliation console

  Scenario: AC1 A reconciliation break
    Given v_ace_account holds 2,903 SSME accounts at 90 days past due or more less the exclusions and the case list holds 2,891
    When the reconciliation step of JOB-04 runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    And the 12 account keys are on the break list with their days past due from v_ace_account

  Scenario: AC2 Referential completeness
    Given case_party on case "RW-2026-000140" carries person_key "P0099881" with no row in v_ace_customer
    When the REC-05 step runs
    Then the orphan shows with its table, its column and its key
    And the case and its case_party row are unchanged

  Scenario: AC3 A stale data product
    Given a data product past its expected business date
    When I open the console
    Then it shows as stale with its last complete ACE business date
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| case_list_row | id, business_date, case_id, case_no, account_key, product_group and 13 more | DF-RPT-001 to DF-RPT-019 |
| reconciliation_result | id, rec_code, business_date, product_group, source_count, workbench_count and 6 more | DF-OPS-118 to DF-OPS-129 |
| data_product_load | id, product_code, source_system, business_date, loaded_at, status, stale_flagged_at | DF-OPS-001 to DF-OPS-008 |
| v_ace_account | account_key, account_code, product_category_efs, days_past_due, total_balance, data_as_of and 36 more | DF-ACE-001 to DF-ACE-042 |

**Endpoints**

No endpoint in this story. The console reads the reconciliation and data quality extract that the reconciliation step of JOB-04 writes, and the freshness stamp in `data_product_load`. The data quality exception endpoint is withdrawn by D-RCV-35 and there is no exception table.

**Screen and states**

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks; referential completeness; stale |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-019-01 | AC1 | A reconciliation break |
| TC-AD-019-02 | AC2 | Referential completeness |
| TC-AD-019-03 | AC3 | A stale data product |
| TC-AD-019-04 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A break never deletes or changes a Workbench record or an ACE row.

---

"""

def swap_section(text, key, new):
    pat = re.compile(r"(?ms)^## " + re.escape(key) + r" .*?(?=^## RWB-AD-)")
    m = pat.search(text)
    assert m, key
    return text[:m.start()] + new + text[m.end():]

doc = swap_section(doc, "RWB-AD-004", AD004)
doc = swap_section(doc, "RWB-AD-018", AD018)
doc = swap_section(doc, "RWB-AD-019", AD019)

# ------------------------------------------------------------------ 4. file-wide field-name fixes
before = doc
doc = doc.replace("| role | id, role_code, role_name, role_class, default_scope, entra_group | DF-REF-034 to DF-REF-039 |",
                  "| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |")
doc = doc.replace("| document | id, case_id, party_id, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |",
                  "| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |")
doc = doc.replace("| recovery_case | id, case_no, product_group, primary_customer_id, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |",
                  "| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |")
print("role rows", before.count("entra_group | DF-REF-034"))

# AD-001: the group-to-role mapping lives in the view, not on role
old_ad001 = "| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |\n\n**Endpoints**\n\n| Method | Path | Access |\n|---|---|---|\n| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |"
new_ad001 = ("| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |\n"
             "| v_ace_iam_group | entra_group, role_code, source_system, data_as_of | DF-ACE-301 to DF-ACE-304 |\n\n"
             "**Endpoints**\n\n| Method | Path | Access |\n|---|---|---|\n| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |")
assert old_ad001 in doc
doc = doc.replace(old_ad001, new_ad001, 1)

# ------------------------------------------------------------------ 5. guardrail
old_g = ("**Guardrails.** No value that a business person may change is written in code. "
         "No personal data in logs, tests or prompts. No read of another module's tables.")
new_g = ("**Guardrails.** No value that a business person may change is written in code. "
         "No personal data in logs, tests or prompts. No read of another module's tables; "
         "ACE data only through recovery.v_ace_* views.")
n = doc.count(old_g)
print("guardrails replaced", n)
doc = doc.replace(old_g, new_g)

io.open(DST, "w", encoding="ascii", newline="\n").write(doc)
print("written", DST, len(doc))
