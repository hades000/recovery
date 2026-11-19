<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-037 |
| Epic | E1, release 30 November 2026 |
| Module | P4 Access and administration |
| Feature | FEAT-ACA-04 Hold the role to permission matrix as data; FEAT-ACA-05 Mask PDPA fields by role; FEAT-ACA-13 Apply joiner, mover and leaver changes to access; FEAT-ACA-14 Scope a user's cases by team and region |
| Requirement IDs | REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009, REQ-ACA-011 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Epic 2, section 3.4 (REQ-ACA-011); Business Requirements Program, section 5.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-022, RWB-E1-043, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies**, so that **a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it**.

## 2. Business rationale

Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank. Today rights are set inside each system and cannot be shown for a past date. This story holds the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applies scope before permission on every request, and ends access at the next request when a person leaves. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and puts controls CTL-09, CTL-10 and CTL-11 in place. The measure is rule and limit changes made without a code release: target 100 percent (FSD P4 A2.4).

## 3. Preconditions

- RWB-E1-022 is done: sessions resolve roles from Entra ID groups, and AccessCheck runs on every endpoint.
- RWB-E1-043 is done: POST /admin/reference-loads validates and versions a load file.
- RWB-E1-027 is done: the decision log writer is available through its published interface.
- Permission matrix version PM-2026.11 (from the Users, roles and permissions workbook) is the version in force.
- Masking version MASK-2026.11 is loaded with no unmasked rows in PROD until Compliance supplies the rules (DL26), so every personal field is masked for every role. SIT carries a test version MASK-SIT-01.
- The P3 queue membership interface from RWB-E1-019 returns the teams and regions of a user.
- Parameters `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` are in the parameter catalog (RWB-E1-042).

## 4. Flow

1. Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.
2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.
3. Security administrator (RW-SECADM): reviews the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve.
4. Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.
5. Workbench: from the valid from date, every new session resolves the new version (RWB-E1-022 keeps open sessions on their version), and the screens and endpoints of the new letters open with no deployment.
6. Person: requests a list or a record; ScopeService builds the filter from the role's default scope (own, team, region, all) and the person's teams and regions; the owning module applies it in its query.
7. Workbench: AccessCheck tests the right in the capability area on the records inside the scope.
8. Workbench (FieldMasker): masks every field tagged as personal data unless the masking rule in force lets one of the session's roles see it; unmasked values are fetched through the ACE PII service, which logs the read to PII Kafka (INT-22).
9. Workbench: on each request, compares the session's groups with the groups the ACE common module holds for the person (refreshed at most every 5 minutes, assumed; DL38); if a group has been removed the session ends and the request is refused.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an action, for example a transfer | Refused with 403 before the handler runs; nothing changes; refusal logged | MSG-P4-002 | AC3 |
| X2 | A record outside the person's scope is requested | Refused with 404; the record is not returned and the count of excluded records is never shown | MSG-P4-003 | AC4 |
| X3 | A matrix file misses a role, repeats a role and area, or holds a letter outside C, R, U, D, A and "-" | The load is refused in full; the version in force stays | MSG-P1-002 | AC5 |
| X4 | The person who loaded a version tries to approve it | Refused; the version stays Loaded | MSG-P7-002 | AC6 |
| X5 | A role other than the table's approver role calls approve | Refused with 403 | MSG-P4-002 | AC6 |
| X6 | The decision log write for an approval fails | The version is not approved and stays Loaded | MSG-P7-003 | AC7 |
| X7 | A leaver's group is removed while a session is open | The next request after the membership refresh ends the session | MSG-P4-001 | AC8 |
| X8 | No masking rule exists for a personal field and role | The field is masked | None | AC9 |
| X9 | Two approve calls for the same load arrive at once | One approves; the second returns 409 and writes nothing | MSG-GEN-004 | AC10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the session (RWB-E1-022), the load service (RWB-E1-043) and the writer (RWB-E1-027), all earlier in Epic 1 |
| Negotiable | Letters, scopes and masking positions are data; Compliance sets the masking values under DL26 |
| Valuable | A change of rights takes effect by an approved load, and personal data is masked by default |
| Estimable | One loader, one scope service, one masker, one approval check |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Role to permission matrix as data and PDPA field masking by role

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force
    Given RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"
    Given masking version "MASK-SIT-01" is in force, in which only RW-CASEOWN sees contact_point.value_token unmasked

  Scenario: AC1 Matrix as data
    Given test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01"
    Given the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11"
    Given test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    When test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues
    Then the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment
    Then one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102"

  Scenario: AC2 Masking
    Given test user "U-2104" holds only RW-PHONECOL
    When the user opens case "RW-2026-000123" in the case record view
    Then the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678"
    Then the system makes no request to the ACE PII service for clear values
    Then the system writes the view to the access event stream with the case ID and the fields shown masked

  Scenario: AC3 Denied action
    Given test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R"
    When the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123"
    Then the system refuses the call with status 403 and message MSG-P4-002 before the handler runs
    Then the case owner and queue are unchanged
    Then the system writes one refusal event with area "QUEUE_AND_ALLOCATION" and right "U"

  Scenario: AC4 A case outside the scope is not returned
    Given test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases
    Given case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When the user calls GET /cases
    Then 12 cases return and the total is 12
    Then GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003

  Scenario: AC5 A matrix file with an error is refused in full
    Given matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting
    When test user "U-2101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the duplicate row and the invalid letters
    Then the system stores no row of "PM-2026.13" and "PM-2026.11" stays in force

  Scenario: AC6 The loader cannot approve, and only the table's approver role may
    Given load "PM-2026.12" was loaded by test user "U-2101"
    When "U-2101" calls approve on that load
    Then the system refuses the call with message MSG-P7-002 and the load stays "Loaded"
    Then when test user "U-2106" holding RW-COE calls approve on that load
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC7 An approval that cannot be recorded does not take effect
    Given the decision log store is unavailable
    When test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    Then the call returns status 503 with message MSG-P7-003
    Then the load stays "Loaded" and "PM-2026.11" stays in force

  Scenario: AC8 A leaver loses access at the next request
    Given test user "U-2107" holds RW-TEAMMGR and has an open session since 08:00
    Given the access administrator removes "U-2107" from group "RWB-SIT-RW-TEAMMGR" at 10:00
    When the user calls GET /cases at 10:06, after the 5 minute membership refresh
    Then the system refuses the call with status 401 and message MSG-P4-001
    Then the system ends the session and a new sign-in is refused

  Scenario: AC9 A personal field with no masking rule is masked
    Given no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role
    When test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123"
    Then the date of birth shows masked as "XXXX-XX-XX"

  Scenario: AC10 Two approvals of the same load at once
    Given load "PM-2026.12" is "Loaded"
    When two approve calls for it arrive at the same time from "U-2102" and test user "U-2108" holding RW-SECADM
    Then one call approves and one decision log entry is written
    Then the other call returns status 409 with message MSG-GEN-004 and writes nothing
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The permission matrix version in force is the only source of what a role may do; a capability area with "-" refuses every action in it | permission.letters (DF-REF-043), matrix_version (DF-REF-044); REQ-ACA-003; CTL-09 |
| BR2 | A matrix file holds every active role once for each of the 14 capability areas, with letters from C, R, U, D, A in that order or "-"; a file with any error is refused in full | LOV-CAPABILITY; reference data change process, step 3 |
| BR3 | A version is approved by the role the parameter names for the table, and never by the person who loaded it | Parameters rwb.refload.approver.*; Admin and access model, section 3.3; CTL-05 |
| BR4 | Scope filters records first and the permission is checked second; an out-of-scope record is never returned and the excluded count is never shown | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
| BR5 | OWN means cases the person owns or has a task on; TEAM means cases in the person's team queues; REGION means cases in the regions of the person's teams; ALL means every case | Key sheet, roles.txt |
| BR6 | A personal data field is masked unless the masking rule in force lets one of the session's roles see it; with no rule it is masked | Masking rules reference table; DL26; CTL-11; REQ-ACA-005 |
| BR7 | Masking is applied before data reaches a screen or an agent | NFR-039; NFR-040 |
| BR8 | A leaver's removal from a group ends the open session at the next request after the membership refresh; leaver removal is within the same working day | DL38; CTL-10; REQ-ACA-011 |
| BR9 | A version approval that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39; CTL-06 |

## 9. State transitions

None. This story does not change a case status. It moves a reference load from Loaded to Approved (or Refused at validation), and a session from Resolved to Ended when a group is removed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Application owner (level 1, assumed DL02) | Approves each permission matrix version outside the Workbench; the approval reference is carried in the load file |
| Role owners (level 2) | Request matrix changes for the roles they own |
| RW-REFADM Reference data administrator | Loads a matrix or masking version (Reference data C). Approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission or role conflict version (approver role for the table, parameter) |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version (approver role for the table, parameter) |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| Access administrator (level 3, bank IAM) | Removes leavers and movers from Entra ID groups |
| Line manager (level 4, bank IAM) | Starts mover and leaver changes |
| Every bank role | Sees cases inside the default scope of its roles, with fields masked per the masking rules |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-040 to DF-REF-044 | permission | all fields | Write (one row per role and area of each new version) |
| DF-REF-035 | role | role_code | Read |
| DF-REF-038 | role | default_scope | Read |
| DF-REF-037 | role | role_class | Read |
| DF-REF-199 | masking_rule | role_code | Write, read |
| DF-REF-200 | masking_rule | field_id | Write, read |
| DF-REF-201 | masking_rule | unmasked | Write, read |
| DF-REF-202 | masking_rule | masking_version | Write, read |
| DF-REF-203 | masking_rule | valid_from | Write, read |
| DF-PTY-007 | party | id_no_token | Read through the owning module's DTO; masked by FieldMasker |
| DF-PTY-008 | party | date_of_birth | Read through the owning module's DTO; masked by FieldMasker |
| DF-PTY-016 | contact_point | value_token | Read through the owning module's DTO; masked by FieldMasker |
| DF-CAS-009 | recovery_case | owner_user_id | Read by the P3 repository applying the scope filter |
| DF-CAS-011 | recovery_case | team_code | Read by the P3 repository applying the scope filter |
| DF-CAS-012 | recovery_case | region_code | Read by the P3 repository applying the scope filter |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per approved version) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005)

| Item | Value |
|---|---|
| Request | Multipart: file (xlsx or csv), table ("permission" or "masking_rule"), validFrom (date) |
| Response | 201 ReferenceLoad: id, table, validFrom, status "Loaded", rows |
| Errors | 401 no session; 403 no Reference data C (MSG-P4-002); 409 a version with the same name exists (MSG-GEN-004); 422 validation failed (MSG-P1-002, with the failed check in detail); 503 store unavailable (MSG-GEN-006) |
| Authorization | Reference data, right C |
| Idempotency | Idempotency-Key header; the same key returns the first response |

**POST /admin/reference-loads/{loadId}/approve** (API-P4-006)

| Item | Value |
|---|---|
| Request | None |
| Response | 200 ReferenceLoad with status "Approved" |
| Errors | 401; 403 caller does not hold the approver role for the table (MSG-P4-002); 404 no such load (MSG-P4-003); 409 caller loaded it (MSG-P7-002), or the load is not "Loaded" (MSG-GEN-004); 503 decision log write failed (MSG-P7-003) |
| Authorization | api.yaml declares Reference data, right A, which no role holds in PM-2026.11. This story checks the approver role named for the table in the parameter catalog instead; the change is recorded in the additions file |
| Idempotency | Idempotency-Key header; a repeat approve of an Approved load returns 409 and writes nothing |

**POST /api/recovery/v1/cases/{caseId}/transfer** (owned by P3; used in AC3 only to show the refusal): Queue and allocation, right U.

**Published interfaces** (package recovery.access.matrix):

```java
ScopeFilter scopeFor(SessionContext session);            // type OWN|TEAM|REGION|ALL, userRef, teamCodes, regionCodes
<T> T mask(T dto, SessionContext session);               // masks every field annotated @PersonalData("DF-...")
boolean isUnmasked(String fieldId, SessionContext session);
```

## 13. Solution plan

- Package: folder `recovery/access/matrix` in the recovery module; Java package `recovery.access.matrix`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | Reference load and approve endpoints for the permission and masking_rule tables |
| PermissionMatrixLoader | Service | Validates a matrix file whole and stores rows with status Loaded |
| MaskingRuleLoader | Service | Validates a masking file: known role codes, field IDs that exist in sys_fields with is_personal true |
| ReferenceLoadApprovalService | Service | Approver role check, maker and checker check, decision log write, status change in one transaction |
| ScopeService | Published interface | Builds ScopeFilter from the default scope and the P3 queue membership interface |
| FieldMasker | Published interface | Masks annotated DTO fields; asks the ACE PII service for clear values only where the rule allows |
| SessionRevalidationFilter | Service | Compares session groups with the ACE common module's current groups on each request |
| AccessAndAdministrationRepository | Repository | Reads and writes permission and masking_rule rows |
| MaskingRule | Entity | Maps the new masking_rule table |

- Database: writes permission (role_id, capability_area, letters, matrix_version, state, is_active). Adds unique index uk_permission_version on permission (matrix_version, role_id, capability_area). Creates table masking_rule (id uuid, role_code varchar(20), field_id varchar(16), unmasked boolean, masking_version varchar(20), valid_from date, valid_to date, plus the standard columns) with Flyway migration V_E1_037__masking_rule.sql and unique index on (masking_version, role_code, field_id). Writes decision_log_entry through the P7 writer only.
- Configuration and reference data: PM-2026.11 (RW-REFADM loads, RW-SECADM approves); MASK-2026.11 (RW-REFADM loads, RW-COMPLY approves; values DL26); parameters rwb.refload.approver.permission, rwb.refload.approver.masking_rule, rwb.access.membership-refresh-minutes=5 (assumed, DL38), rwb.access.mask.keep-last=4 (characters kept for identity and phone, assumed, DL26); LOV-CAPABILITY, LOV-SCOPE.
- Build steps:
  1. Create the masking_rule migration and the permission unique index.
  2. Build PermissionMatrixLoader and MaskingRuleLoader with whole-file validation and a difference report against the version in force; tests for AC5.
  3. Build ReferenceLoadApprovalService with the approver role check, maker and checker check, optimistic lock on the load and the decision log write in one transaction; tests for AC1, AC6, AC7, AC10.
  4. Build ScopeService and the ScopeFilter contract; give P3 a repository test that applies it to GET /cases and GET /cases/{caseId}; tests for AC4.
  5. Build FieldMasker with the @PersonalData annotation and the ACE PII service call; tests for AC2 and AC9.
  6. Build SessionRevalidationFilter; test for AC8 with a group removed in the ACE test double.
  7. Confirm AC3 through the AccessCheckInterceptor from RWB-E1-022 on the transfer endpoint.
- Feature flag: `rwb.access.permission-matrix`.
- Done when: the tests in section 16 pass, and the masking test in the access test set (three roles open the same case) passes in SIT and is signed by Compliance.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Session ended after a leaver's group was removed | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission, or approve by a role that is not the table's approver | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P1-002 | A matrix or masking file fails validation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The loader tries to approve their own load | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The approval cannot be written to the decision log | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A second approve of a load already approved | Someone else changed this record. Reload it to see their change. |

Thai text for each message follows DL10.

## 15. Screens and states

No screen in this story. Matrix and masking versions arrive by file load until SCR-43 Roles and access and SCR-47 Personal data come in Epic 8. A person sees the effect in the menu (RWB-E1-022), in masked fields on the case record view (RWB-E1-023) and in 404 responses for out-of-scope cases.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-037-01 | AC1, BR1 | System | Matrix files PM-2026.11 and PM-2026.12 differing in one letter |
| TC-E1-037-02 | AC2, BR6, BR7 | System | Synthetic case with tokenized identity number and phone; RW-PHONECOL test user |
| TC-E1-037-03 | AC3, BR1 | System | RW-CASEOWN test user calling the transfer endpoint |
| TC-E1-037-04 | AC4, BR4, BR5 | System | 12 owned cases and one case in another team |
| TC-E1-037-05 | AC5, BR2 | System | Matrix file with a duplicate row and an invalid letter |
| TC-E1-037-06 | AC6, BR3 | System | Load approved by its loader, then by RW-COE |
| TC-E1-037-07 | AC7, BR9 | System | Decision log store switched off in the test double |
| TC-E1-037-08 | AC8, BR8 | System | Group removed in the ACE test double during a session |
| TC-E1-037-09 | AC9, BR6 | System | Personal field with no masking rule |
| TC-E1-037-10 | AC10 | System | Two parallel approve calls on one load |
| TC-E1-037-11 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E1-037-12 | Principle 5 | Resilience | The decision log write forced to fail during an approval |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: letters, scopes, masking positions, approver roles and the refresh interval are data or parameters.
- No personal data in logs, tests or prompts. Tests use tokenized synthetic values; the access event lists field IDs, never values.
- No read of another module's tables: the scope filter is applied by the owning module's repository; masking works on DTOs.
- An unmasked value is fetched only through the ACE PII service, which logs every read.
- A field with no masking rule is masked.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR2, BR3, BR9 | TC-E1-037-01, TC-E1-037-05, TC-E1-037-06, TC-E1-037-07, TC-E1-037-10 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR6, BR7 | TC-E1-037-02, TC-E1-037-09 |
| REQ-ACA-007 | Access outside the matrix refused and recorded | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1 | TC-E1-037-03, TC-E1-037-11 |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | Epic 1, 3.4 | FEAT-ACA-14 | All recovery processes | BR4, BR5 | TC-E1-037-04 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | Epic 2, 3.4 | FEAT-ACA-13 | All recovery processes | BR8 | TC-E1-037-08 |

## 19. Out of scope

- Reallocation of a leaver's or mover's open cases (RWB-E1-030 daily rebalancing; R-UNI-18 and R-UNI-19 in Epic 2).
- Administration screens SCR-43 and SCR-47 (Epic 8, FEAT-ADM-01 and FEAT-ADM-14).
- Masking values for each role and field (Compliance, DL26).
- Access per data product in the data lake copy (RWB-E1-016).
- The six-monthly access review list (JOB-18, Epic 2 control CTL-10).
