# Recovery Workbench administration stories

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories in this file | 22 |
| By epic | E4: 1, E8: 21 |
| Related stories already in the Epic 1 and Epic 2 backlog | 10 |

User and role administration, reference data, rule versions, queue and timer configuration, job and ACE batch monitoring, and the audit log. Epic 1 builds the services and the reference and rule loads by file; these stories add the administration screens and approvals in Epic 8, when full administration is delivered, and partner administration in Epic 4.

Version 3 is re-based on D-RCV-35 and ADR-010. The Workbench loads no source data: the job monitor shows Workbench jobs beside the ACE batch status, the console shows reconciliation breaks, and masking profiles name the columns of the recovery.v_ace_* views. Two stories are rewritten around the read path (RWB-AD-018, RWB-AD-019) and one is a minor edit (RWB-AD-004).

## Administration already in the backlog

| Key | Title | Module | Epic |
|---|---|---|---|
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | E1 |
| RWB-E1-029 | Rule load, validation and rollback | P3 | E1 |
| RWB-E1-034 | Letter template management | P6 | E1 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | P4 | E1 |
| RWB-E1-038 | Delegation of authority table as reference data | P4 | E1 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | P4,P7 | E1 |
| RWB-E1-041 | Retention classes and virus scan on intake | P5 | E1 |
| RWB-E1-043 | Reference data service with versioned tables | P3 | E1 |
| RWB-E1-048 | Rule change audit report | P3 | E1 |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | P2 | E1 |

## Stories in this file

| Key | Title | Module | Epic | Depends on |
|---|---|---|---|---|
| RWB-AD-001 | Map Entra ID groups to Workbench roles | P4 | E8 | RWB-E1-022 |
| RWB-AD-002 | Permission matrix as a versioned load | P4 | E8 | RWB-E1-037 |
| RWB-AD-003 | Scope per role | P4 | E8 | RWB-E1-037 |
| RWB-AD-004 | Masking profiles per role | P4 | E8 | RWB-E1-037 |
| RWB-AD-005 | Separation of duty check at sign-in | P4 | E8 | RWB-E1-022 |
| RWB-AD-006 | Break-glass access | P4 | E8 | RWB-E1-039 |
| RWB-AD-007 | Access log search and export | P4 | E8 | RWB-E1-039 |
| RWB-AD-008 | Access review list | P4 | E8 | RWB-E1-022 |
| RWB-AD-009 | Load a list of values version | P4 | E8 | RWB-E1-043 |
| RWB-AD-010 | Approve a reference data load | P4 | E8 | RWB-AD-009 |
| RWB-AD-011 | Load a rule version | P4 | E8 | RWB-E1-029 |
| RWB-AD-012 | Approve a rule version | P4 | E8 | RWB-AD-011 |
| RWB-AD-013 | Roll back a rule or reference version | P4 | E8 | RWB-AD-012 |
| RWB-AD-014 | Configure queues | P4 | E8 | RWB-E1-019 |
| RWB-AD-015 | Configure service levels and timers | P4 | E8 | RWB-E1-028 |
| RWB-AD-016 | Load the delegation of authority table | P4 | E8 | RWB-E1-038 |
| RWB-AD-017 | Manage letter and notice templates | P6 | E8 | RWB-E1-034 |
| RWB-AD-018 | Interface and job monitor | P1 | E8 | RWB-E1-056, RWB-E1-069 |
| RWB-AD-019 | Data quality and reconciliation console | P1 | E8 | RWB-E1-011, RWB-E1-015, RWB-E1-069 |
| RWB-AD-020 | Autonomy level per decision step | P10 | E8 | RWB-E1-063 |
| RWB-AD-021 | Retention classes and legal hold | P5 | E8 | RWB-E1-041 |
| RWB-AD-022 | Partner firms and partner users | S9 | E4 | RWB-E1-022 |

---

## RWB-AD-001 Map Entra ID groups to Workbench roles

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-022 |
| Decision | DL40 |

**Story.** As a security administrator, I want each Entra ID group mapped to one Workbench role in each environment as a data row, so that a person gets their roles from the group the bank IAM grants, with no code change.

**Acceptance criteria**

```gherkin
Feature: Map Entra ID groups to Workbench roles

  Scenario: AC1 Group gives the role
    Given the group RWB-SIT-RW-CASEOWN mapped to RW-CASEOWN
    When a member of the group signs in to SIT
    Then the session holds the role RW-CASEOWN

  Scenario: AC2 Unmapped group
    Given a person whose only group has no mapping
    When they sign in
    Then the system refuses they with MSG-P4-001 and the refusal is in the access log

  Scenario: AC3 Mapping change
    Given a new mapping version with a valid from date
    When the date arrives
    Then sessions from that date use the new mapping
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |
| v_ace_iam_group | entra_group, role_code, source_system, data_as_of | DF-ACE-301 to DF-ACE-304 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |
| Rules and parameters | C | RW-COE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-001-01 | AC1 | Group gives the role |
| TC-AD-001-02 | AC2 | Unmapped group |
| TC-AD-001-03 | AC3 | Mapping change |
| TC-AD-001-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-001-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-002 Permission matrix as a versioned load

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-037 |
| Decision | None |

**Story.** As an application owner, I want the permission matrix of roles against the 14 capability areas loaded as a versioned file, so that a permission changes without a code release and every change has an approver.

**Acceptance criteria**

```gherkin
Feature: Permission matrix as a versioned load

  Scenario: AC1 Load a matrix version
    Given a matrix file with every role and area
    When the reference data administrator loads it
    Then it passes the checks and waits for the application owner's approval

  Scenario: AC2 Incomplete matrix refused
    Given a file with a role missing
    When it is loaded
    Then the system refuses it in full with the missing role named

  Scenario: AC3 Takes effect on its date
    Given an approved version with a valid from date
    When the date arrives
    Then every endpoint checks against the new version
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |
| permission | id, role_id, capability_area, letters, matrix_version | DF-REF-040 to DF-REF-044 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| POST | /api/recovery/v1/admin/reference-loads | Reference data C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-40 Reference data | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Reference data | C | RW-COE, RW-REFADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-002-01 | AC1 | Load a matrix version |
| TC-AD-002-02 | AC2 | Incomplete matrix refused |
| TC-AD-002-03 | AC3 | Takes effect on its date |
| TC-AD-002-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-002-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-003 Scope per role

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-037 |
| Decision | None |

**Story.** As an application owner, I want each role given a scope of own cases, team, region or all as data, so that a person sees only the cases their role allows.

**Acceptance criteria**

```gherkin
Feature: Scope per role

  Scenario: AC1 Own scope
    Given a case owner with scope Own
    When they list cases
    Then the system returns only cases they own

  Scenario: AC2 Out of scope
    Given a case owned by another team
    When a case owner with scope Team opens it
    Then the system does not find the response and the refusal is logged
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/roles | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

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
| TC-AD-003-01 | AC1 | Own scope |
| TC-AD-003-02 | AC2 | Out of scope |
| TC-AD-003-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-003-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-004 Masking profiles per role

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

## RWB-AD-005 Separation of duty check at sign-in

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-022 |
| Decision | None |

**Story.** As a security administrator, I want a session refused when a person's groups hold a conflicting role pair, so that no one holds two roles the separation of duty table forbids.

**Acceptance criteria**

```gherkin
Feature: Separation of duty check at sign-in

  Scenario: AC1 Conflict refused
    Given a person in the groups for RW-WRITEOFF and RW-WOCOMM
    When they sign in
    Then the system refuses the session and an incident goes to the security administrator

  Scenario: AC2 Table as data
    Given a new separation of duty version
    When it is approved
    Then the next sign-in checks against it
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-005-01 | AC1 | Conflict refused |
| TC-AD-005-02 | AC2 | Table as data |
| TC-AD-005-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-005-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-006 Break-glass access

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-039 |
| Decision | DL38 |

**Story.** As a platform administrator, I want emergency access beyond my role, tied to an open incident, ending on its own, so that an incident can be fixed without a permanent grant.

**Acceptance criteria**

```gherkin
Feature: Break-glass access

  Scenario: AC1 Granted with an incident
    Given an open incident and a reason of at least 20 characters
    When the security administrator approves the request
    Then the system grants access for the window and every action is marked break-glass

  Scenario: AC2 Refused without an incident
    Given no open incident
    When the request is made
    Then the system refuses it

  Scenario: AC3 Ends on its own
    Given an active grant
    When the window ends
    Then the grant ends with no action by anyone
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/access-log | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-43 Roles and access | List; access log |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-006-01 | AC1 | Granted with an incident |
| TC-AD-006-02 | AC2 | Refused without an incident |
| TC-AD-006-03 | AC3 | Ends on its own |
| TC-AD-006-04 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-006-05 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-007 Access log search and export

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-039 |
| Decision | None |

**Story.** As an internal auditor, I want the access log searched by person, date, event and capability area, with export, so that I can show who accessed what without asking IT.

**Acceptance criteria**

```gherkin
Feature: Access log search and export

  Scenario: AC1 Search
    Given sign-ins and refusals for a week
    When I search by person and date
    Then the matching entries show with the role and versions in force

  Scenario: AC2 Export
    Given a search result
    When I export it
    Then the file carries the same masking as the screen
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/access-log | Platform administration R |
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-40 Reference data | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-007-01 | AC1 | Search |
| TC-AD-007-02 | AC2 | Export |
| TC-AD-007-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-007-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-008 Access review list

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-022 |
| Decision | DL38 |

**Story.** As a role owner, I want a list of every holder of my roles each review cycle, to confirm or remove, so that access is recertified on schedule.

**Acceptance criteria**

```gherkin
Feature: Access review list

  Scenario: AC1 List produced
    Given the review date
    When the review opens
    Then each role owner receives the holders of their roles

  Scenario: AC2 Not confirmed
    Given a holder not confirmed by the end of the review
    When the review closes
    Then the system requests removal through the bank IAM and logged
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/roles | Platform administration R |
| GET | /api/recovery/v1/admin/access-log | Platform administration R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-43 Roles and access | List; access log |
| SCR-41 Delegation of authority | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-008-01 | AC1 | List produced |
| TC-AD-008-02 | AC2 | Not confirmed |
| TC-AD-008-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-008-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-009 Load a list of values version

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-043 |
| Decision | None |

**Story.** As a reference data administrator, I want a list of values loaded as a new version with a valid from date, so that a code list changes without a code release.

**Acceptance criteria**

```gherkin
Feature: Load a list of values version

  Scenario: AC1 Valid load
    Given a file for LOV-ROUTE with codes and English labels
    When I load it
    Then it passes the checks and waits for the list owner's approval

  Scenario: AC2 Code in use removed
    Given a load that removes a code used by open cases
    When it is loaded
    Then the system refuses it with the count of records using the code
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-40 Reference data | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-009-01 | AC1 | Valid load |
| TC-AD-009-02 | AC2 | Code in use removed |
| TC-AD-009-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-009-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-010 Approve a reference data load

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-AD-009 |
| Decision | None |

**Story.** As a list owner, I want to approve or reject a loaded version before it takes effect, so that no reference data changes without its owner.

**Acceptance criteria**

```gherkin
Feature: Approve a reference data load

  Scenario: AC1 Approve
    Given a loaded version waiting for me
    When I approve it
    Then it takes effect from its valid from date and the approval is logged

  Scenario: AC2 Maker cannot approve
    Given a version I loaded
    When I try to approve it
    Then I am refused with MSG-P7-002
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| POST | /api/recovery/v1/admin/reference-loads/{loadId}/approve | Reference data A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-40 Reference data | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Reference data | A | Service identities only |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-010-01 | AC1 | Approve |
| TC-AD-010-02 | AC2 | Maker cannot approve |
| TC-AD-010-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-010-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-011 Load a rule version

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-029 |
| Decision | DL24 |

**Story.** As a center of excellence analyst, I want a route set loaded as a new rule version where each row names its test case, so that rules change as data and every row is tested.

**Acceptance criteria**

```gherkin
Feature: Load a rule version

  Scenario: AC1 Rule rows tested
    Given a route set file where every row has a test case ID
    When I load it
    Then the rule table tests run in SIT and the result is attached to the version

  Scenario: AC2 Row without a test
    Given a row with no test case ID
    When I load it
    Then the system refuses the version
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-47 Personal data | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-011-01 | AC1 | Rule rows tested |
| TC-AD-011-02 | AC2 | Row without a test |
| TC-AD-011-03 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-012 Approve a rule version

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-AD-011 |
| Decision | None |

**Story.** As a risk and model risk officer, I want to approve a rule version that has passed its tests, with its valid from date, so that only tested and approved rules decide cases.

**Acceptance criteria**

```gherkin
Feature: Approve a rule version

  Scenario: AC1 Approve
    Given a version with every test passed
    When I approve it
    Then it applies to decisions from its valid from date

  Scenario: AC2 Open cases keep their version
    Given a case decided under the previous version
    When the new version takes effect
    Then the decided case keeps the version it was decided under (R-UNI-38)
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-39 Rules and parameters | Versions; load; approval |
| SCR-47 Personal data | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-004 | Warning | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-012-01 | AC1 | Approve |
| TC-AD-012-02 | AC2 | Open cases keep their version |
| TC-AD-012-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-012-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-013 Roll back a rule or reference version

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-AD-012 |
| Decision | None |

**Story.** As a reference data administrator, I want the previous version restored through the same load, so that a bad change is undone in minutes.

**Acceptance criteria**

```gherkin
Feature: Roll back a rule or reference version

  Scenario: AC1 Roll back
    Given a version in force that causes a breach
    When I load the previous version with an immediate date and the owner approves
    Then decisions from that time use the previous version and both changes are logged
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-40 Reference data | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | C | RW-COE |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-013-01 | AC1 | Roll back |
| TC-AD-013-02 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-013-03 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-014 Configure queues

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-019 |
| Decision | DL23 |

**Story.** As a reference data administrator, I want queues with their team, role, assignment method, caseload cap and overflow queue loaded as data, so that allocation follows the team set-up without a code change.

**Acceptance criteria**

```gherkin
Feature: Configure queues

  Scenario: AC1 Queue loaded
    Given a queue file
    When it is loaded and approved
    Then allocation uses the new method and cap from the valid from date

  Scenario: AC2 Overflow must exist
    Given a queue that names an overflow queue that does not exist
    When it is loaded
    Then the system refuses the load
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| queue | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | DF-WRK-001 to DF-WRK-008 |
| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| role | id, role_code, role_name, role_class, default_scope | DF-REF-034 to DF-REF-038 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/admin/rule-versions | Rules and parameters R |
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |

**Screen and states**

| Screen | States |
|---|---|
| SCR-42 Queues and service levels | Versions; load |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | R | RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 30 more |
| Rules and parameters | A | RW-RISK |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-014-01 | AC1 | Queue loaded |
| TC-AD-014-02 | AC2 | Overflow must exist |
| TC-AD-014-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-014-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-015 Configure service levels and timers

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-028 |
| Decision | DL22 |

**Story.** As a reference data administrator, I want the time allowed in each case state, its warning and its escalation point loaded as data, so that clocks and escalations follow the agreed service levels.

**Acceptance criteria**

```gherkin
Feature: Configure service levels and timers

  Scenario: AC1 Service level loaded
    Given a service level of 10 working days for state LIT_PACK with a warning at 8
    When it is approved
    Then new timers in that state use the values

  Scenario: AC2 Running timers
    Given a timer already running
    When a new version takes effect
    Then the running timer keeps its due date unless the rule says to recompute
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | DF-WRK-027 to DF-WRK-036 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| POST | /api/recovery/v1/admin/rule-versions | Rules and parameters C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-42 Queues and service levels | Versions; load |
| SCR-39 Rules and parameters | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Rules and parameters | C | RW-COE |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-015-01 | AC1 | Service level loaded |
| TC-AD-015-02 | AC2 | Running timers |
| TC-AD-015-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-015-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-016 Load the delegation of authority table

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P4 Access and administration |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-038 |
| Decision | DL18 |

**Story.** As a reference data administrator, I want approval levels, limits, holders and substitutes loaded as data with effective dates, so that approvals route by the regulation without a code change.

**Acceptance criteria**

```gherkin
Feature: Load the delegation of authority table

  Scenario: AC1 Limits loaded
    Given limits by decision, level, product and amount
    When Risk approves the version
    Then approvals check against it from its date

  Scenario: AC2 Missing limit
    Given a decision with no limit at any level
    When it is submitted
    Then it goes to the next level up and an incident names the missing limit
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| delegation_limit | id, decision_code, approval_level, product_group, principal_limit, loss_pct_limit and 5 more | DF-REF-016 to DF-REF-026 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/admin/rule-versions/{versionId}/approve | Rules and parameters A |
| POST | /api/recovery/v1/admin/reference-loads | Reference data C |

**Screen and states**

| Screen | States |
|---|---|
| SCR-41 Delegation of authority | Versions; load; approval |
| SCR-39 Rules and parameters | Versions; load; approval |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Rules and parameters | A | RW-RISK |
| Reference data | C | RW-COE, RW-REFADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Error | This case is not in your scope. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-016-01 | AC1 | Limits loaded |
| TC-AD-016-02 | AC2 | Missing limit |
| TC-AD-016-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-016-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-017 Manage letter and notice templates

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P6 Communications |
| Feature | None |
| Process | See module |
| Priority | Must |
| Depends on | RWB-E1-034 |
| Decision | DL28 |

**Story.** As a legal counsel, I want templates by type, product and language approved by Legal before use, and withdrawn when they change, so that every notice uses wording Legal has approved.

**Acceptance criteria**

```gherkin
Feature: Manage letter and notice templates

  Scenario: AC1 Approve
    Given a new template version in Thai and English
    When Legal approves it
    Then notices generated from its date use it

  Scenario: AC2 Withdraw
    Given a template withdrawn
    When a notice of that type is due
    Then generation holds and a task goes to the litigation officer (R-LIT-04)
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 |
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
| TC-AD-017-01 | AC1 | Approve |
| TC-AD-017-02 | AC2 | Withdraw |
| TC-AD-017-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-017-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-018 Interface and job monitor

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

## RWB-AD-019 Data quality and reconciliation console

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

## RWB-AD-020 Autonomy level per decision step

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P10 Agent runtime |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-063 |
| Decision | None |

**Story.** As a risk and model risk officer, I want the autonomy level of each agent step held as data and changed only with committee approval, so that an agent never acts beyond what the committee approved.

**Acceptance criteria**

```gherkin
Feature: Autonomy level per decision step

  Scenario: AC1 Level applied
    Given step D6.3 at level L1
    When the route agent answers
    Then the system shows the answer as a recommendation and a person decides

  Scenario: AC2 Step up recorded
    Given a committee approval for L2
    When the new version takes effect
    Then the change shows the approval reference in the version
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |

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
| TC-AD-020-01 | AC1 | Level applied |
| TC-AD-020-02 | AC2 | Step up recorded |
| TC-AD-020-03 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-020-04 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-021 Retention classes and legal hold

| Item | Value |
|---|---|
| Epic | E8, release 30 June 2027 |
| Module | P5 Document hub |
| Feature | None |
| Process | See module |
| Priority | Must |
| Depends on | RWB-E1-041 |
| Decision | DL26 |

**Story.** As a Compliance and PDPA officer, I want retention classes by data product and document type, and legal holds that stop expiry, so that nothing is kept longer than its rule and nothing held is lost.

**Acceptance criteria**

```gherkin
Feature: Retention classes and legal hold

  Scenario: AC1 Expiry
    Given a document past its retention period with no hold
    When the retention job runs
    Then the system proposes disposal and recorded, never silent

  Scenario: AC2 Hold
    Given a document under legal hold
    When its retention period ends
    Then the system keeps it and the hold is shown
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 |
| rule_row | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | DF-REF-001 to DF-REF-015 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| POST | /api/recovery/v1/cases/{caseId}/documents | Documents C |
| GET | /api/recovery/v1/documents/{documentId} | Documents R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-31 Document review queue | Loading; list; reviewed |
| SCR-32 Document custody | Out; overdue; returned |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Documents | C | RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE and 12 more |
| Documents | R | RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-P5-002 | Error | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-003 | Information | Some fields need checking. The document is in the review queue. |
| MSG-P5-004 | Warning | {document} is due back from {holder} since {date}. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-021-01 | AC1 | Expiry |
| TC-AD-021-02 | AC2 | Hold |
| TC-AD-021-03 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---

## RWB-AD-022 Partner firms and partner users

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S9 Partner management |
| Feature | None |
| Process | See module |
| Priority | Must |
| Depends on | RWB-E1-022 |
| Decision | DL03 |

**Story.** As a partner and agency manager, I want partner firms, their contracts and panel status held as data, and partner users requested for each firm, so that partners see only the work placed with their firm.

**Acceptance criteria**

```gherkin
Feature: Partner firms and partner users

  Scenario: AC1 Firm scope
    Given a law firm user
    When they open the partner portal
    Then only instructions placed with their firm show

  Scenario: AC2 Contract ends
    Given a firm whose contract ends today
    When the day ends
    Then the system disables its user accounts and open instructions are recalled
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |
| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |

**Endpoints**

| Method | Path | Access |
|---|---|---|
| GET | /api/recovery/v1/partners | Partner portal R |
| GET | /api/recovery/v1/partner/instructions | Partner portal R |

**Screen and states**

| Screen | States |
|---|---|
| SCR-34 Partner list | Loading; list |
| PRT-01 Partner home | Loading; list |

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Partner portal | R | RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

**Test cases**

| ID | Covers | Test |
|---|---|---|
| TC-AD-022-01 | AC1 | Firm scope |
| TC-AD-022-02 | AC2 | Contract ends |
| TC-AD-022-03 | Access | A role without the right is refused with MSG-P4-002 |

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views.

---
