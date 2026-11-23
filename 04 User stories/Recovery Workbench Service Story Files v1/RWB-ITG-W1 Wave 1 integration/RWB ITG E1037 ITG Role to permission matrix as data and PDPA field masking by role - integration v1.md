# RWB-ITG-E1037-ITG Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1037-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1069-APP, RWB-PLT-E1037-APP, RWB-P4-E1037-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-037 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-037 permission matrix as data, the scope rule and the PDPA field masking across P4 rwb-access (matrix, roles, masking rules, the guard and the access log), P1 rwb-source-data (the ACE view boundary and the masked read) and the platform guard and masker library, with the decision records collected by P7**, so that **a rights change is a load with an approver, an out-of-scope record never returns, and the clear identity number never leaves ACE, proved on the real wave 1 services**.

### 2. Business rationale

The legacy story holds the permission matrix (54 roles against 14 capability areas), the scope rule and the masking rules as versioned tables that every screen and API applies, with the `ScopeFilter`, `FieldMasker` and `AccessCheck` published interfaces inside one monolith. In the 19-service target the tables stay with one owner each (DP-01): the role, permission, masking_rule, role_conflict and delegation_limit tables sit with P4 rwb-access, and the entity and field registry with P1 rwb-source-data. The matrix is data in P4's schema and the fields it masks are data in P1's schema; no service reads the other's tables, and the suite reads both through the published contracts only.

The legacy published interfaces split three ways. The right check and the scope rule become the authorise contract of P4 rwb-access behind the platform guard library (DP-08), with one login per service (DP-02). The masking is applied by rwb-source-data at the data read, against the masking policy that P4 owns and publishes on `rwb.access.events.v1` (Arch v5 slide 46; D-RCV-35 U1), so the clear identity number never leaves ACE and the clear contact value is read only where the rule allows it. Parameters and reference data are read as data through the contracts of P3 rwb-case (DP-06, DP-07), and the legacy `recovery.access.matrix` package disappears with no replacement library of its own.

Every approval writes its local decision record in `rwb_access` in the same transaction and publishes `DecisionRecorded` to `rwb.decision-record.v1`, collected by P7 rwb-decision within five minutes (DP-03; ADR-022). Access policy changes travel as `AccessPolicyChanged` on `rwb.access.events.v1` (DP-10 is the Schedule only, and the legacy event marker belongs to the owner; DP-14 is not in the pattern list of this story and is not claimed). Every call in the suite is one hop with a 2 s timeout (DP-11) under the per-service REST bases (DP-13), each service keeps its own schema and its own Flyway sequence (DP-15), the data lake copy is removed and reporting comes from events (DP-17), and SCR-43 and SCR-47 are reached through gateway-bff but are not built here (DP-19).

The split is stated plainly. This ITG story owns no legacy acceptance criterion. Legacy AC1 to AC13 sit at component level with RWB-P4-E1037-APP and the platform library story RWB-PLT-E1037-APP, and the fifteen scenarios of section 7 are the integration proof across the two services and the shared topic. The I list of this story names P1, the platform library and P4 only, so the suite proves the scope and masking outcomes through P4's guard and P1's masked read, not through a P3 case read. The measure is unchanged from the legacy story: rule and limit changes made without a code release, target 100 percent (FSD P4 A2.4). The story meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and supports controls CTL-09, CTL-10 and CTL-11.

Where the sources do not name who owns the matrix load operation at integration level, the exact masking read path between P4's policy and P1's read, the boundary of the platform guard and masker library, or how the scope is proved without a P3 case read, the suite asserts through the owners' contracts and records the open point as Not specified in the source documents (GAP-0358; ASM-0462), (GAP-0358; ASM-0463), (GAP-0358; ASM-0464) and (GAP-0358; ASM-0465).

### 3. Preconditions

- RWB-P4-E1037-APP is done: the permission matrix as data, the masking rules, the scope rule, the guard and the access log are in SIT on P4 rwb-access.
- RWB-PLT-E1037-APP is done: the guard library and the masker library are published and versioned for the wave 1 services.
- RWB-P1-E1069-APP is done: `v_ace_customer` and `v_ace_contact` exist, `recovery_svc` holds SELECT on them and no privilege on `public`, and the boundary rule is enforced.
- The published contracts of P4 rwb-access and P1 rwb-source-data are deployed under their own per-service bases behind gateway-bff, and permission matrix version PM-2026.11 is in force.
- A test version PM-2026.12 differs from PM-2026.11 in one letter, and a refused file PM-2026.13 carries a duplicate row and an invalid letter.
- Masking version MASK-SIT-01 is in force, in which only RW-CASEOWN may see `v_ace_contact.contact_value` in clear for DF-ACE-078. No unmasked rows go to PROD until Compliance supplies the rules (DL26).
- The synthetic users U-2101 to U-2109, U-2111 and the group RWB-SIT-RW-TEAMMGR exist in SIT, and the harness RWB-ITG-W1J01-ITG is available with its synthetic users and cases.
- The parameters rwb.refload.approver.permission=RW-SECADM, rwb.refload.approver.masking_rule=RW-COMPLY and rwb.access.membership-refresh-minutes=5 are loaded, read as data rows through the parameters contract of P3 rwb-case.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic users U-2101 to U-2111, the group RWB-SIT-RW-TEAMMGR, the 12 owned cases of U-2105 and case RW-2026-000456 of team MTG-NE from harness RWB-ITG-W1J01-ITG, and signs the users in through gateway-bff as RW-REFADM, RW-SECADM, RW-LEGAL, RW-PHONECOL, RW-CASEOWN, RW-COE and RW-TEAMMGR; no production data is used.
2. Harness: loads matrix file PM-2026.12 as U-2101 with table "permission" and validFrom "2026-12-01" through POST /api/recovery/access/v1/admin/reference-loads, and asserts 756 rows with status "Loaded".
3. Harness: approves PM-2026.12 as U-2102 through POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve, then reads GET /api/recovery/access/v1/admin/roles and GET /api/recovery/access/v1/admin/access-log and asserts one approval entry with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102".
4. Harness: with the clock at 1 December 2026 signs in U-2103 as RW-LEGAL and calls POST /api/recovery/access/v1/authorise for Queue and allocation U; asserts the call is allowed, where under PM-2026.11 it was refused, with no deployment; reads the letters through GET /api/recovery/access/v1/me/permissions.
5. Harness: signs in U-2104 as RW-PHONECOL, reads the data product record of case RW-2026-000123 through GET /api/recovery/source-data/v1/data-products/{productCode}/records, and asserts id_no_masked "XXXXXXXXX1234" and contact_value_masked "XXXXXX5678" with no clear contact value read.
6. Harness: runs the refusals (U-2105 holding RW-CASEOWN for Queue and allocation U, the out-of-scope read of case RW-2026-000456, U-2101 approving its own load, U-2111 and U-2106 holding RW-COE approving) and records every status and message.
7. Harness: removes U-2107 from group RWB-SIT-RW-TEAMMGR at 10:00 and calls GET /api/recovery/access/v1/me/session at 10:06, after the 5 minute membership refresh; asserts 401 with MSG-P4-001 and a refused new sign-in.
8. Harness: loads the refused file PM-2026.13 as U-2101, reads the record of U-2105 as RW-CASEOWN where no masking rule covers `v_ace_customer.date_of_birth` (DF-ACE-059), and runs the two approval calls of AC10 for one load.
9. Harness: reads GET /api/recovery/source-data/v1/admin/data-dictionary/fields and GET /api/recovery/source-data/v1/data-products/freshness, runs the identity test with `recovery_svc` on `public.customer` and `recovery.v_ace_customer`, and with U-2109 reads the borrower's phone number on case RW-2026-000123.
10. Harness: writes the evidence report, removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an action, for example a transfer | Refused with 403 before the handler runs; nothing changes; the refusal is logged | MSG-P4-002 | AC3 |
| X2 | A record outside the person's scope is requested | Refused with 404; the record is not returned and the count of excluded records is never shown | MSG-P4-003 | AC4 |
| X3 | A matrix file misses a role, repeats a role and area, or holds a letter outside C, R, U, D, A and "-" | The load is refused in full; the version in force stays | MSG-P1-002 | AC5 |
| X4 | The person who loaded a version tries to approve it | Refused; the version stays Loaded | MSG-P7-002 | AC6 |
| X5 | A role other than the table's approver role calls approve | Refused with 403 | MSG-P4-002 | AC6, AC15 |
| X6 | The decision record write for an approval fails | The version is not approved and stays Loaded | MSG-P7-003 | AC7, AC12 |
| X7 | A leaver's group is removed while a session is open | The next request after the membership refresh ends the session | MSG-P4-001 | AC8 |
| X8 | No masking rule exists for a personal field and role | The field comes from the masked view column, or is masked by the masker where the view holds no masked column | None | AC9 |
| X9 | Two approve calls for the same load arrive at once | One approves; the second returns 409 and writes nothing | MSG-GEN-004 | AC10 |
| X10 | A rule asks for the clear identity number | The rule is refused at load; the clearest value a rule can name is `id_no_last4` | MSG-P1-002 | AC13 |
| X11 | A consumed call exceeds the 2 s timeout or returns a server error | The call is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC12 |
| X12 | The fixture set does not match the harness RWB-ITG-W1J01-ITG expectations, or the clock control cannot move the time | The suite fails as a harness fault and names the element; no service defect is raised | None | AC4, AC8 |

X1 to X10 are the legacy exception paths with their messages; X11 and X12 are added for the integration run.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P4 and P1, not their source code |
| Negotiable | The matrix files, the masking version, the letters, the scopes, the fixture sizes and the exact fault-switch mechanism are data or properties of the harness; the story fixes the assertions and the call set |
| Valuable | A rights change by load, a scope boundary and the masking of personal data are proved on the real wave 1 services, and the clear identity number is shown absent from every response, before wave 1 exits |
| Estimable | One suite module, one matrix file pack, one identity and grant test, one session control and one evidence report |
| Small | Fifteen scenarios over two services and two events; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an access event, a status or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Role to permission matrix as data and PDPA field masking by role, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-access and rwb-source-data are deployed in SIT with their published contracts behind gateway-bff
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force
    Given RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"
    Given masking version "MASK-SIT-01" is in force, in which only RW-CASEOWN may see v_ace_contact.contact_value in clear for DF-ACE-078
    Given the RWB-ITG-W1J01-ITG synthetic users and cases are loaded and no production data is used

  Scenario: AC1 The matrix is data (new, D-RCV-60)
    Given U-2101 holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01"
    And the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11"
    And U-2102 holding RW-SECADM approves load "PM-2026.12"
    When U-2103 holding RW-LEGAL signs in on 1 December 2026 and calls POST /api/recovery/access/v1/authorise for Queue and allocation U
    Then the call is allowed, where under "PM-2026.11" it was refused, with no deployment
    Then GET /api/recovery/access/v1/admin/access-log holds one approval entry with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102"

  Scenario: AC2 Masking from the view columns (new, D-RCV-60)
    Given U-2104 holds only RW-PHONECOL
    And `v_ace_customer` returns the borrower of case "RW-2026-000123" with id_no_masked "XXXXXXXXX1234"
    And `v_ace_contact` returns the mobile as contact_value "0812345678" and contact_value_masked "XXXXXX5678"
    When the user reads the data product record for the case through GET /api/recovery/source-data/v1/data-products/{productCode}/records
    Then the identity number shows "XXXXXXXXX1234" and the phone "XXXXXX5678"
    Then no clear contact value is read for the role
    Then one access event holds the case ID, the field IDs and each field's masked flag

  Scenario: AC3 A denied action (new, D-RCV-60)
    Given U-2105 holds only RW-CASEOWN, whose Queue and allocation letter is "R"
    When the user calls POST /api/recovery/access/v1/authorise for Queue and allocation U
    Then the call returns 403 with MSG-P4-002 before any handler runs
    Then the owner and queue of the case are unchanged
    Then one refusal event holds area "QUEUE_AND_ALLOCATION" and right "U"

  Scenario: AC4 A case outside the scope is not returned (new, D-RCV-60)
    Given U-2105 holds RW-CASEOWN with default scope "OWN" and owns 12 cases
    And case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When the user reads the data product records for the case set
    Then 12 cases return and the total is 12
    Then the read of "RW-2026-000456" returns 404 with MSG-P4-003

  Scenario: AC5 A matrix file with an error is refused in full (new, D-RCV-60)
    Given matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting
    When U-2101 loads it
    Then the load is refused with MSG-P1-002 naming the duplicate row and the invalid letters
    Then no row of "PM-2026.13" is stored and "PM-2026.11" stays in force

  Scenario: AC6 The loader cannot approve (new, D-RCV-60)
    Given load "PM-2026.12" was loaded by U-2101
    When U-2101 calls approve on it
    Then the call is refused with MSG-P7-002 and the load stays "Loaded"

  Scenario: AC7 An approval that cannot be recorded does not take effect (new, D-RCV-60)
    Given the local decision record write is switched to fail by the agreed test-only fault switch
    When U-2102 holding RW-SECADM approves load "PM-2026.12"
    Then the call returns 503 with MSG-P7-003
    Then the load stays "Loaded" and "PM-2026.11" stays in force

  Scenario: AC8 A leaver loses access at the next request (new, D-RCV-60)
    Given U-2107 holds RW-TEAMMGR and has an open session since 08:00
    And the access administrator removes U-2107 from group "RWB-SIT-RW-TEAMMGR" at 10:00
    When the user calls GET /api/recovery/access/v1/me/session at 10:06, after the 5 minute membership refresh
    Then the call returns 401 with MSG-P4-001
    Then the session ends and a new sign-in is refused

  Scenario: AC9 A personal field with no masking rule is masked (new, D-RCV-60)
    Given no masking rule in "MASK-SIT-01" covers `v_ace_customer.date_of_birth` (DF-ACE-059) for any role
    When U-2105 holding RW-CASEOWN reads the record through the P1 data product
    Then the date of birth shows masked as "XXXX-XX-XX"

  Scenario: AC10 Two approvals of the same load at once (new, D-RCV-60)
    Given load "PM-2026.12" is "Loaded"
    When two approve calls arrive at the same time from U-2102 and U-2108 holding RW-SECADM
    Then one call approves and one decision record is written
    Then the other returns 409 with MSG-GEN-004 and writes nothing

  Scenario: AC11 A role without the right is refused (new, D-RCV-60)
    Given test user "U-2111" holds RW-COE
    When the user calls the approve operation
    Then the call returns 403 with MSG-P4-002

  Scenario: AC12 A decision record that cannot be written blocks the approval (new, D-RCV-60)
    Given the local record write is switched to fail for every call by the agreed test-only fault switch
    When an approved load and a refused right are attempted
    Then nothing is approved and no refusal is recorded as complete
    Then MSG-P7-003 is returned and the version in force is unchanged

  Scenario: AC13 The clear identity number never leaves ACE (new, D-RCV-60)
    Given the recovery service identity `recovery_svc` in SIT
    And `v_ace_customer` holds the identity number "1234567890123" for person_key "P-0001"
    When the identity test runs
    Then SELECT on public.customer is refused with permission denied
    Then SELECT on recovery.v_ace_customer returns id_no_masked "XXXXXXXXX0123" and id_no_last4 "0123" and no column holds the clear value
    Then GET /api/recovery/source-data/v1/admin/data-dictionary/fields shows DF-ACE-073 and DF-ACE-074 and no field for the clear value
    Then no Workbench table, token store or service returns the clear identity number for any role

  Scenario: AC14 A read of a personal field is audited (new, D-RCV-60)
    Given U-2109 holds RW-CASEOWN, which may see DF-ACE-078 in clear
    When U-2109 reads the borrower's phone number on case "RW-2026-000123"
    Then one access event holds the case ID, field ID DF-ACE-078 and the flag "clear"
    Then the event holds no field value

  Scenario: AC15 Only the table's approver role may approve (new, D-RCV-60)
    Given load "PM-2026.12" is "Loaded"
    When U-2106 holding RW-COE calls approve on it
    Then the call returns 403 with MSG-P4-002
    Then the load stays "Loaded"
```

**Target reading.** Every scenario is new at integration level, because each one is re-expressed against the P4 and P1 contracts behind gateway-bff; the business values, the matrix versions, the masking version, the message IDs, the user IDs, the case IDs, the team code and the row count are the legacy values unchanged. AC11 is the legacy access test at integration level. AC4 proves the scope through the records of the P1 data product, because the I list of this story names P1, the platform library and P4 only and not P3 rwb-case (GAP-0358; ASM-0465). The guard and masker library is exercised through the P4 and P1 operations and is never called by the suite (GAP-0358; ASM-0464).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The permission matrix version in force is the only source of what a role may do; a capability area with "-" refuses every action in it | permission.letters (DF-REF-043), matrix_version (DF-REF-044); REQ-ACA-003; CTL-09 |
| BR2 | A matrix file holds every active role once for each of the 14 capability areas, with letters from C, R, U, D, A in that order or "-"; a file with any error is refused in full | LOV-CAPABILITY; reference data change process, step 3 |
| BR3 | A version is approved by the role the parameter names for the table, and never by the person who loaded it | Parameters rwb.refload.approver.*; Admin and access model, section 3.3; CTL-05 |
| BR4 | Scope filters records first and the permission is checked second; an out-of-scope record is never returned and the excluded count is never shown | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
| BR5 | OWN means cases the person owns or has a task on; TEAM means cases in the person's team queues; REGION means cases in the regions of the person's teams; ALL means every case | Key sheet, roles.txt |
| BR6 | A personal data field is masked unless the masking rule in force lets one of the session's roles see it. A masked field is filled from the masked view column (`id_no_masked`, `contact_value_masked`), or masked by the masker where the view holds no masked column; with no rule it is masked | Masking rules reference table; DL26; CTL-11; REQ-ACA-005; DF-ACE-073, DF-ACE-079 |
| BR7 | Masking is applied before data reaches a screen or an agent | NFR-039; NFR-040 |
| BR8 | A leaver's removal from a group ends the open session at the next request after the membership refresh; leaver removal is within the same working day | DL38; CTL-10; REQ-ACA-011 |
| BR9 | A version approval that cannot be written to the decision record does not take effect | Principle 5; R-UNI-39; CTL-06 |
| BR10 | There is no tokenization and no token store. The clear `customer.identification_number` never leaves ACE; `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only, and `id_no_last4` is the clearest identity value any role can receive | ADR-010; Data Tier Map section 7; D-RCV-35 U1 |
| BR11 | Every read of a personal data field is written to the access log with the field ID and its masked flag, never the value | REQ-ACA-006; RWB-E1-039 BR3; NFR-040 |
| BR12 | A masking rule names a field ID that exists in `sys_fields` with `is_personal` true and belongs to a `recovery.v_ace_*` view or a Workbench table; a rule that names the clear identity number is refused | RWB-E1-069; Data Tier Map section 7 |
| BR13 | The matrix, role, role_conflict, delegation_limit and masking_rule tables are P4 rwb-access's, and the entity and field registry and the ACE boundary are P1 rwb-source-data's; no service reads another's tables | DP-01, DP-05; Ownership Map |
| BR14 | An approval writes its local decision record in `rwb_access` in the same transaction and publishes `DecisionRecorded`, collected by P7 within five minutes; every call in the suite is one hop with a 2 s timeout | DP-03; ADR-022; ADR-020; DP-11 |

### 9. State transitions

None for the case status. This story does not change a case status. It moves a reference load from Loaded to Approved, or to Refused at validation, and a session from Resolved to Ended when a group is removed.

| Object | State | Meaning |
|---|---|---|
| Reference load | Loaded, or Refused at validation | The rows of the version are stored with the new version name and no right changes yet; the loader may not approve it, no other role may approve it, and a file that fails validation stores no row |
| Reference load | Approved | The approver role named for the table approved the load, one local decision record is written in `rwb_access` and the version takes effect from its valid from date |
| Session | Resolved, then Ended | The session holds the roles and the scope of the version in force and the guard resolves the letters at each request; when a group is removed and the membership refresh has run, the session returns 401 with MSG-P4-001 and a new sign-in is refused |

The suite reads these states through the owners' contracts; it changes none of them directly, apart from the agreed test-only fault switch and the group removal in the ACE test double.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| Application owner (level 1, assumed DL02); role owners (level 2) | Approves each permission matrix version outside the Workbench, with the approval reference carried in the load file; requests matrix changes for the roles they own |
| RW-REFADM Reference data administrator | Loads a matrix or masking version (Reference data C). Approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission or role conflict version (approver role for the table, parameter) |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version (approver role for the table, parameter) |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| Access administrator (level 3, bank IAM); line manager (level 4, bank IAM) | Removes leavers and movers from Entra ID groups; starts mover and leaver changes |
| Every bank role | Sees cases inside the default scope of its roles, with fields masked per the masking rules |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_customer` and `v_ace_contact` |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-040 to DF-REF-044 | permission (P4 rwb-access) | all fields | Write through the P4 reference load; read through the P4 contracts |
| DF-REF-035, DF-REF-037, DF-REF-038 | role (P4 rwb-access) | role_code, role_class, default_scope | Read |
| DF-REF-198 to DF-REF-204 | masking_rule (P4 rwb-access) | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-ACE-073 | v_ace_customer (P1 rwb-source-data) | id_no_masked | Read; the masked identity value |
| DF-ACE-074 | v_ace_customer (P1 rwb-source-data) | id_no_last4 | Read; only with the personal-data permission |
| DF-ACE-055 | v_ace_customer (P1 rwb-source-data) | cif_no | Read through the P1 contract; masked |
| DF-ACE-057 | v_ace_customer (P1 rwb-source-data) | first_name | Read through the P1 contract; masked |
| DF-ACE-058 | v_ace_customer (P1 rwb-source-data) | last_name | Read through the P1 contract; masked |
| DF-ACE-059 | v_ace_customer (P1 rwb-source-data) | date_of_birth | Read through the P1 contract; masked |
| DF-ACE-078 | v_ace_contact (P1 rwb-source-data) | contact_value | Read; only with the personal-data permission |
| DF-ACE-079 | v_ace_contact (P1 rwb-source-data) | contact_value_masked | Read; the masked contact value |
| DF-CAS-009 | recovery_case (P3 rwb-case) | owner_user_id | Read by the owner's scope filter; never read by the suite |
| DF-CAS-011 | recovery_case (P3 rwb-case) | team_code | Read by the owner's scope filter; never read by the suite |
| DF-CAS-012 | recovery_case (P3 rwb-case) | region_code | Read by the owner's scope filter; never read by the suite |
| DF-DEC-001 to DF-DEC-018, DF-DEC-030 | decision_log_entry (local in P4 rwb-access; ledger in P7 rwb-decision) | all fields, including actor_user_id | Write one entry per approved version; read through the ledger contract |

Field IDs are those in the Logical Data Model and Data Dictionary. DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema. In the target the permission and masking rows are written by P4 rwb-access and read by the suite through the P4 contract, and the ACE fields are read only through the P1 data product; the suite holds no schema. Every value in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/access/v1/authorise | P4 rwb-access | The guard check for Queue and allocation U by RW-LEGAL and by RW-CASEOWN |
| GET /api/recovery/access/v1/me/permissions | P4 rwb-access | The letters in force for the signed-in role |
| GET /api/recovery/access/v1/admin/roles | P4 rwb-access | The roles and their default scope as data |
| GET /api/recovery/access/v1/admin/access-log | P4 rwb-access | The one approval entry and the refusal events |
| GET /api/recovery/access/v1/me/session | P4 rwb-access | The session state after the leaver's group is removed |
| POST /api/recovery/access/v1/admin/reference-loads | P4 rwb-access | The matrix file load of PM-2026.12 and the refused file PM-2026.13 |
| POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve | P4 rwb-access | The approval, the loader refusal, the wrong approver role and the two approvals |
| GET /api/recovery/source-data/v1/admin/data-dictionary/fields | P1 rwb-source-data | The field registry, DF-ACE-073 and DF-ACE-074, and no field for the clear value |
| GET /api/recovery/source-data/v1/data-products/{productCode}/records | P1 rwb-source-data | The masked record read of the case, the out-of-scope refusal and the no-rule field |
| GET /api/recovery/source-data/v1/data-products/freshness | P1 rwb-source-data | The freshness stamp of the data product read |

Every call is one hop with a 2 s timeout (ADR-020, DP-11). The paths use the per-service bases of DP-13.

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | P4 rwb-access | The suite waits for the policy change before it asserts the new letters and the new masking rule |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | every service, with the ledger owned by P7 rwb-decision | The suite waits for the ledger entry of the approval before it asserts the access log |

The suite consumes no other event, and it produces none.

#### 12.5 Workflows and activities

None. No workflow, activity or Nexus operation is started or awaited by this story; the guard and the masking are synchronous, and every call is a REST read or write.

#### 12.6 Schedules

None. No Schedule is started, moved or waited for. The six-monthly access review list (JOB-18) is a P4 rwb-access Schedule and is not this story. The clock control moves the request time only.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01).

#### 12.8 Contract fakes

No service contract is faked: every call in section 12.2 goes to the real SIT service. AC7 and AC12 use the agreed test-only fault switch on the P4 decision-record write, and it is the only intervention in a running service. The subgroup membership change of AC8 is the ACE test double, which is an outside system and not a service contract. The platform guard and masker library is exercised through the P4 and P1 operations and is never called by the suite (GAP-0358; ASM-0464).

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 10 |
| Kafka | 0 | 2 |
| Temporal | 0 | 0 |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the fifteen scenarios against SIT and holds no service code |
| Matrix and masking file pack: PM-2026.11, PM-2026.12, PM-2026.13 and MASK-SIT-01 | Test data | The version in force, the version that differs in one letter with 756 rows, the file refused in full, and the rule that lets RW-CASEOWN see DF-ACE-078 in clear with no rule for DF-ACE-059 |
| Identity, grant and session controls | Database test and harness control | `recovery_svc` on `public.customer` and `recovery.v_ace_customer` in SIT only; removes U-2107 from group RWB-SIT-RW-TEAMMGR in the ACE test double at 10:00 and moves the request clock to 10:06 |
| Evidence report | Report | Records per scenario the status, the message, the load ID, the access event and the masked or clear flag |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | P4 holds role, permission, masking_rule, role_conflict and delegation_limit in rwb_access; P1 holds sys_fields, sys_objects, sys_field_version, data_contract and data_product in rwb_source_data; the suite asserts through both contracts |
| DP-02 | recovery_svc login | One login per service | none | P4, P1 and the platform library each sign in with their own login; the identity test of AC13 uses recovery_svc in SIT only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | On RWB-P4-E1037-APP for the approval record; the suite waits for the ledger entry within five minutes |
| DP-05 | AceSourceQuery, v_ace_*, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | RWB-P1-E1069-APP owns the two ACE views, the grants and the boundary rule; the suite reads the masked record through P1 and never a table |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On RWB-P4-E1037-APP for rwb.refload.approver.permission, rwb.refload.approver.masking_rule and rwb.access.membership-refresh-minutes; the suite reads the same rows as data |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On RWB-P4-E1037-APP for LOV-CAPABILITY and LOV-SCOPE; the suite sends the letters and the scopes as data |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON | The guard library is built on RWB-PLT-E1037-APP and used by RWB-P4-E1037-APP; the suite calls POST /authorise as a client |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | Only the six-monthly access review list JOB-18, a P4 Schedule; no Schedule is started or waited for here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The ten consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P4-E1037-APP for the permission version index and on RWB-P1-E1069-APP for the view grants; the suite migrates nothing |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none | The legacy data lake copy of access data is absent; the suite asserts no lake endpoint in the call set of the run |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; SCR-43 and SCR-47 are not built here and no screen is in scope |

The dependency-added column records the build dependency of the owning story. The H and C dependencies in the table belong to the owning APP stories. The H, C and X lists of this story are exactly those of the metadata table: no H, no C, no X, and the three I dependencies RWB-P1-E1069-APP, RWB-PLT-E1037-APP and RWB-P4-E1037-APP. An ITG story waits on no build of its own.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire the SIT endpoints of P4 rwb-access and P1 rwb-source-data through gateway-bff.
2. Prepare the matrix files PM-2026.11, PM-2026.12 and PM-2026.13 as data, with the 756 rows of PM-2026.12, and the masking file MASK-SIT-01 with the rule that lets RW-CASEOWN see DF-ACE-078 in clear and no rule for DF-ACE-059.
3. Implement AC1, AC5, AC6, AC10 and AC15: the load, the approval, the refused file, the loader refusal, the wrong approver role and the two approvals, with the exact messages and one writer per entry.
4. Implement AC2, AC9, AC13 and AC14: the masked identity and contact values, the no-rule field, the field registry, the view boundary and the audited clear read.
5. Implement AC3, AC4, AC11 and AC8: the guard refusal, the scope boundary through the P1 records, the role without the right and the session revalidation control (GAP-0358; ASM-0465).
6. Implement AC7 and AC12 through the agreed test-only fault switch on the P4 decision-record write, and assert that the version in force is unchanged.
7. Run the suite in SIT against the wave 1 release candidate, write the evidence report, remove the synthetic fixtures and restore the clock. The masking read path is asserted through the P1 record and the P4 policy response, because its internal wiring is Not specified in the source documents (GAP-0358; ASM-0463).

Done when: all fifteen test cases pass in SIT against the published wave 1 contracts of P4 rwb-access and P1 rwb-source-data, the evidence report shows every masked value and no clear identity number in any response, log or event, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Session ended after a leaver's group was removed | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission, or approve by a role that is not the table's approver | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P1-002 | A matrix or masking file fails validation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The loader tries to approve their own load | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The approval cannot be written to the decision record | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A second approve of a load already approved | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The reference data store is unavailable | {system} is not available. Your request is queued and will be retried. |

The message IDs and wording are copied from RWB-E1-037. No new message ID is added by this story. Thai text for each message follows DL10.

### 15. Screens and states

No screen in this story. A person sees the effect in the menu (RWB-E1-022), in masked fields on the case record view (RWB-E1-023) and in 404 responses for out-of-scope cases. SCR-43 Roles and access and SCR-47 Personal data are Epic 8. The suite reads through the P4 and P1 contracts only, and no screen is built or tested here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-037-01-ITG | AC1, BR1 | Integration | Matrix files PM-2026.11 and PM-2026.12 differing in one letter, 756 rows; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-02-ITG | AC2, BR6, BR7 | Integration | Synthetic case with `v_ace_customer.id_no_masked` and `v_ace_contact.contact_value_masked`; RW-PHONECOL test user; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-03-ITG | AC3, BR1 | Integration | RW-CASEOWN test user calling the authorise operation for Queue and allocation U; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-04-ITG | AC4, BR4, BR5 | Integration | 12 owned cases and one case in another team, read through the P1 data product; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-05-ITG | AC5, BR2 | Integration | Matrix file PM-2026.13 with a duplicate row and an invalid letter; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-06-ITG | AC6, BR3 | Integration | Load approved by its loader; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-07-ITG | AC7, BR9 | Integration | Decision record write switched to fail on P4 rwb-access; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-08-ITG | AC8, BR8 | Integration | Group removed in the ACE test double during a session; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-09-ITG | AC9, BR6 | Integration | `v_ace_customer.date_of_birth` with no masking rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-10-ITG | AC10 | Integration | Two parallel approve calls on one load; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-11-ITG | AC11 | Component | A role without the right is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-12-ITG | AC12 | NFR | The decision record write forced to fail during an approval and a refusal; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-13-ITG | AC13, BR10, BR12 | NFR | `public.customer` grant refused; `v_ace_customer` id_no_masked and id_no_last4; the field registry; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-14-ITG | AC14, BR11 | Integration | RW-CASEOWN test user reading DF-ACE-078 in clear; end-to-end: real services on the wave 1 contracts |
| TC-E1-037-15-ITG | AC15, BR3 | Integration | RW-COE test user calling approve on a Loaded version; end-to-end: real services on the wave 1 contracts |

### 17. Guardrails

- No business value in code: letters, scopes, masking positions, approver roles and the refresh interval are data rows read through the contracts.
- No personal data in logs, events, evidence or fixtures: field IDs and the masked flag only, never values.
- No cross-service table read: every assertion goes through the owner's contract, and the suite owns no table.
- ACE data only through the P1 contract or `recovery.v_ace_*`; the suite holds no grant on a `public` table and reads no ACE view directly outside the identity test of AC13. There is no tokenization and no token store: the clear identity number never leaves ACE, and no Workbench column, service or rule returns it.
- A field with no masking rule is masked, and an unmasked contact value is read only where the masking rule allows it; every such read is audited.
- One hop and a 2 s timeout on every call (ADR-020).
- The session end is enforced on the next request after the membership refresh and never by a job; the suite moves only its own clock.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG, and no production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | POST /api/recovery/access/v1/admin/reference-loads, POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve, GET /api/recovery/access/v1/admin/roles, GET /api/recovery/access/v1/me/permissions | TC-E1-037-01-ITG, TC-E1-037-05-ITG, TC-E1-037-06-ITG, TC-E1-037-07-ITG, TC-E1-037-10-ITG, TC-E1-037-15-ITG |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | GET /api/recovery/source-data/v1/data-products/{productCode}/records, GET /api/recovery/source-data/v1/admin/data-dictionary/fields, MSG-P4-002 | TC-E1-037-02-ITG, TC-E1-037-09-ITG, TC-E1-037-13-ITG |
| REQ-ACA-007 | Access outside the matrix refused and recorded | POST /api/recovery/access/v1/authorise, MSG-P4-002, the refusal event in GET /api/recovery/access/v1/admin/access-log | TC-E1-037-03-ITG, TC-E1-037-11-ITG |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | The scope filter behind GET /api/recovery/source-data/v1/data-products/{productCode}/records, MSG-P4-003 | TC-E1-037-04-ITG |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | GET /api/recovery/access/v1/me/session, MSG-P4-001 | TC-E1-037-08-ITG |
| REQ-ACA-006 | Every read of a personal data field written to the access log | The access event of the P1 read and of the P4 refusal, through GET /api/recovery/access/v1/admin/access-log | TC-E1-037-02-ITG, TC-E1-037-14-ITG |
| D-RCV-35 U1 | Masking is applied to the view columns; no token is stored at load and the clear identity number never leaves ACE | DF-ACE-073, DF-ACE-074, DF-ACE-078, DF-ACE-079 over the P1 contract | TC-E1-037-02-ITG, TC-E1-037-13-ITG |
| ADR-022 | Local decision record plus central ledger | The local record in rwb_access in the approval transaction and rwb.decision.DecisionRecorded.v1 collected by P7 | TC-E1-037-07-ITG, TC-E1-037-12-ITG |
| ADR-010 | No tokenization; identity masked inside ACE | `recovery_svc` on `public.customer` and `recovery.v_ace_customer` | TC-E1-037-13-ITG |

The four assumptions ASM-0462 to ASM-0465 are traced by the reference-load test cases, the masked read test cases, the guard and registry test cases and the scope test case of section 16.

The legacy AC1 to AC13 at component level belong to RWB-P4-E1037-APP and RWB-PLT-E1037-APP, not to this story.

### 19. Out of scope

- The P4 rwb-access APP build and the platform guard and masker library build, with their unit and component tests.
- The CON, DB and OPS stories of P4 rwb-access, P1 rwb-source-data and the platform library.
- The legacy AC1 to AC13 at component level, which the sibling APP stories own.
- Reallocation of a leaver's open cases (RWB-E1-030).
- Administration screens SCR-43 Roles and access and SCR-47 Personal data (Epic 8, FEAT-ADM-01 and FEAT-ADM-14).
- The masking values for each role and field (Compliance, DL26).
- The six-monthly access review list (JOB-18, Epic 2).
- The shape of the mask itself, which is the view function `recovery.ace_mask_value` and the ACE team's definition.
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
