# RWB-P4-E1037-APP Role to permission matrix as data and PDPA field masking by role

**Version 3 changes.**

- MSG-GEN-006 and MSG-P4-001 carry the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E1-037 for rwb-access — the role to permission matrix, the masking rules and their approve path held as data in `rwb_access`, with the thirteen legacy criteria carried verbatim. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E1037-APP-L313, X20 RWB-P4-E1037-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (34 resolved, 32 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1037-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Contract version | v1 (base /api/recovery/access/v1; event rwb.access.AccessPolicyChanged.v1) |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E1037-APP-16) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP (not built yet; the start gate for this story) |
| Depends on (build) | RWB-P4-E1037-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-003, FR-P4-005, FR-P4-006, FR-P4-008, FR-P4-009, FR-P4-010, FR-P4-011, FR-P4-012, FR-P4-013, FR-P4-014, FR-P4-015, FR-P4-016, FR-P4-017, FR-P4-018, FR-P4-019, FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-032, FR-P4-033, FR-P4-038) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned rows in `rwb_access` that this service publishes and every screen and API applies, with the identity number masked inside the ACE view and contact values masked at the API**, so that **a change of rights is a data load with an approver, a person is scoped to the cases their role allows, and personal data shows unmasked only to the roles that need it**.

This is the rwb-access slice of legacy RWB-E1-037, and it is the data half of that legacy key. The legacy story held the matrix, the masking rules, the scope rule, the loader, the approver, the masker and the identity boundary in one package over one database. D-RCV-60 keeps the behaviour and separates who answers what:

- **This story, rwb-access (P4), schema `rwb_access`:** `permission` (DF-REF-040 to DF-REF-044) and `masking_rule` (DF-REF-198 to DF-REF-204) written and read, `role` (DF-REF-034 to DF-REF-039) and `role_conflict` (DF-REF-205 to DF-REF-211) read, the whole-file checks of a matrix and a masking version, the approver check with maker and checker, the version in force on its date, the permission rows on `GET /api/recovery/access/v1/admin/roles`, the rules in force on `GET /api/recovery/access/v1/masking-policies`, the load and approve operations on `POST /api/recovery/access/v1/admin/reference-loads` and `POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve`, and the publication of `rwb.access.AccessPolicyChanged.v1` when a matrix or a masking version is approved (DP-01, DP-13).
- **Not this story, the platform library (RWB-PLT-E1037-APP and RWB-PLT-E1037-CON):** the guard, the masker, the `@PersonalData` annotation, the scope descriptor and the fakes that every service binds. This story publishes the data the guard and the masker read; it implements neither, and it holds no copy of a library class.
- **Not this story, sign-in and session (RWB-P4-E1022-APP):** the Entra ID sign-in, the multi-factor check, the group-to-role answer, the session in the Redis store of gateway-bff, and the ending of a session when a group is removed. Criterion AC8 is carried here verbatim and is proven at the session boundary against the session contract; the session itself is E1022's.
- **Not this story, the access log and break-glass (RWB-P4-E1039-APP):** the access event stream, the refusal entry, the search and export of the access log and every break-glass grant. Criteria AC2, AC3 and AC12 name an access event; this story supplies the decision and the field ids, and the access-entry writer of E1039 writes the record through the local decision-record library (DP-03).
- **Not this story, the end-to-end proof (RWB-ITG-E1037-ITG):** the same business outcome across P4, P1, P3 and the library, including the ACE grant check of AC11 and the three-role masking test in SIT.
- **Not this story, P3 and P7:** `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` are rwb-case's (DP-07, DP-06); `decision_log_entry` and `approval` are rwb-decision's (DP-03). This story writes no row of any of them.
- **Not this story, the six-monthly access review:** JOB-18 and its access review list are RWB-P4-AD008-APP's Temporal Schedule on the `rwb-access` queue. DP-10 appears in the pattern table as referred to; this story registers no Schedule, and the workflow-kit dependency is carried for that sibling.
- **Service naming:** base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1` with the event `rwb.access.AccessPolicyChanged.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **Criteria and tests:** the thirteen legacy criteria are carried verbatim with their origin tag, and the part of a criterion that calls another service is exercised through that service's contract mock — `Given the rwb-case contract mock returns …`, `Given the rwb-decision contract mock returns …`, `Given the rwb-source-data contract mock returns …` — with every value, id and code of the legacy line kept. The fifteen legacy test cases are kept with their legacy cover in section 16.

### 2. Business rationale

Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank, and today rights are set inside each system and cannot be shown for a past date. The legacy answer was one package that held the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applied scope before permission on every request, and ended access at the next request when a person left. That answer is still the right one, and the realignment makes it a narrower and a stronger one: the policy is data with an owner and an approver, the enforcement is one library every service binds, and the personal value never leaves ACE.

This story is the policy owner. A matrix load is one file, checked whole, approved by a second person and in force from its date with no deployment; a masking load is the same path with Compliance as its approver. The rules the service publishes are what every screen, every API and every agent call applies, so a change of rights is a row and not a release: the measure is rule and limit changes made without a code release, target 100 percent (FSD P4 A2.4). Under D-RCV-35 there is no load of a token and no tokenization: ACE ingests the source row once, `v_ace_customer` exposes the identity number as `id_no_masked` and `id_no_last4` only, and `v_ace_contact` exposes the full phone, e-mail and address because notices and calls need them. Masking is therefore a rule over view columns, not a token stored at load, and `id_no_last4` is the clearest identity value any role can receive (ADR-010).

**The division of this legacy key is fixed.** The guard, the masker and the `@PersonalData` annotation that every service binds are the platform library contract **RWB-PLT-E1037-CON** and its app story **RWB-PLT-E1037-APP**. This story publishes the **data-side contract** of `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit`: the five objects, their versions, the two loads and their approval, the two read operations and the policy event. RWB-P4-E1022-APP owns sign-in and the session, RWB-P4-E1039-APP owns the access log and break-glass, and RWB-ITG-E1037-ITG owns the end-to-end proof. Neither this story nor its contract copies a legacy section wholesale, and neither claims the other's deliverable. Masking home: the function `recovery.ace_mask_value(...)` stays in the recovery view schema with the views, the masking policy rows stay in `rwb_access` (this story), and rwb-source-data applies the mask in the view and in its responses. A read of a personal field goes to the ACE Common PII logging path to the SOC (INT-34); the Recovery business-event topics are separate from that path and carry no personal data. A partner user is created and ended by the S9 rwb-partner administrator; the roles it holds are permission rows granted by the P4 role owner; both actions are written to the access log. The screen response is composed at the edge and owned by RWB-PLT-EDGE; the partner gateway is RWB-PLT-EDGE with S9 rwb-partner behind it.

The values the criteria use are the legacy values unchanged: matrix version `PM-2026.11`, the new version `PM-2026.12` with 756 rows, the rejected file `PM-2026.13`, masking version `MASK-SIT-01`, the production version `MASK-2026.11`, cases `RW-2026-000123` and `RW-2026-000456`, team `MTG-NE`, the role codes RW-REFADM, RW-SECADM, RW-LEGAL, RW-PHONECOL, RW-CASEOWN, RW-COE and RW-AUDIT, the group `RWB-SIT-RW-TEAMMGR`, the field ids DF-ACE-073 `id_no_masked`, DF-ACE-074 `id_no_last4`, DF-ACE-059 `date_of_birth`, DF-ACE-078 `contact_value` and DF-ACE-079 `contact_value_masked`, the area `QUEUE_AND_ALLOCATION`, the letters C, R, U, D and A, the scopes Own, Team, All and Placed cases as the Key tab lists them (a region predicate is decided by the P4 and P3 design), and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-P7-002, MSG-P7-003, MSG-GEN-004 and MSG-GEN-006. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011, and puts controls CTL-09, CTL-10 and CTL-11 in place.

Three assumptions fix the behaviour the sources leave to the run, and each is a register row: a matrix version and a masking version resolve at sign-in and stay until the session ends, so open work keeps the version it was decided under (ASM-1408); a person whose roles include both halves of a `role_conflict` row at the conflict version in force is refused the session (ASM-1409); and an unmapped or inactive group gives no role at all (ASM-1410). Values no source fixes are carried as placeholders: the path and the right of the masking-policy operation of Arch v5 slide 14, and the payload of the policy event — Not specified in the source documents (GAP-0778; ASM-1416) and (GAP-0778; ASM-1417).

### 3. Preconditions

- RWB-P4-E1022-APP is done (H, same lane): sessions resolve roles from Entra ID groups, the guard runs on every endpoint, and a session names the matrix version and the masking version it signed in under.
- RWB-P4-E1037-CON is published (H): the nine contract tables of this service, the four operations of section 12.1, the load and approve shapes, the approver rule, the error vocabulary and the fakes. This story implements it and adds no path.
- The six non-human actors (SY-CASEWF, SY-RULES, SY-RECOVERY, SY-OCR, SY-DECLOG, SY-AGENT) are resolved through POST /authorise with their SY role code and their managed identity as the subject; the credential type is set by RWB-P4-E1037-CON.
- RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON and RWB-PLT-E1044-CON are in place: the decision-record library, the parameter and reference-data client libraries, the guard and masker library, and the migration baseline (DP-03, DP-06, DP-07, DP-08, DP-15).
- RWB-PLT-N001-CON is in place: the gateway-bff composite route that renders the 403 and the 404 and the masked field on the case record view (DP-19).
- RWB-PLT-E1071-CON is in place for the sibling six-monthly access review Schedule (JOB-18, RWB-P4-AD008-APP); this story registers no Schedule (DP-10, ASM-1421).
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published (C): the parameters `rwb.refload.approver.permission=RW-SECADM`, `rwb.refload.approver.masking_rule=RW-COMPLY` and `rwb.access.membership-refresh-minutes=5`, and the lists `LOV-CAPABILITY` (14 areas), `LOV-SCOPE` (OWN, TEAM, REGION, ALL) and `LOV-ROLE-CLASS`. This story builds against their fakes from Day 1 and never against the rwb-case build (DP-11). The five-minute refresh is the legacy assumption (DL38) and is carried as ASM-1413.
- RWB-P7-E1027-CON is published (C): the decision-record write contract, so the approval entry of decision code `AC-VERS` is written through it and no P7 table is touched (DP-03).
- The `rwb_access` baseline exists: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` with their dictionary rows, created by the service baseline migration `V0001` of RWB-PLT-E1044-CON; WP B-P4-01 carries no DB story for this legacy key, so this story adds only its two unique indexes (DP-15, ASM-1418).
- Permission matrix version `PM-2026.11` is the version in force; `PM-2026.12` is the next version and carries 756 permission rows.
- The matrix is kept as rows of permission each stamped with its matrix version; one set mints the next label and supersedes the version in force, so a change is a new version and not an edit in place. The decision code of an access change and the label format beyond `PM-2026.11` are Not specified in the source documents (GAP-2304).
- The system roles of TSD P4 v3 T6.1 are the agent roles; the grant carries an agent reference, not an identity column held by this service (GAP-2304).
- The effective date of a matrix version is held on its load, not on the permission table; the approved role conflict list is Not specified in the source documents (GAP-1574).
- The access log row records the version the owning service applied at the time of the event; the registry in rwb-decision (P7) stays the source of each version and its effective date (GAP-2076).
- Masking version `MASK-2026.11` is loaded with no unmasked rows in production until Compliance supplies the rules (DL26), so every personal field is masked for every role; SIT carries the test version `MASK-SIT-01`, in which only RW-CASEOWN may see `v_ace_contact.contact_value` in clear for DF-ACE-078.
- The masking rules name the view field ids of Physical Schema v7: DF-ACE-073 `id_no_masked`, DF-ACE-074 `id_no_last4`, DF-ACE-059 `date_of_birth`, DF-ACE-078 `contact_value` and DF-ACE-079 `contact_value_masked`, plus the customer number and name fields. `is_personal` on those rows of `sys_fields` is P1 rwb-source-data's registry, read through its contract and never copied here (DP-05).
- The matrix file covers the role roster of TSD P4 v3 T6.1 (42 role codes) and grows to the 54 roles the legacy criteria count; the number of roles and the 756 rows are carried as ASM-1415 with the register row.
- The capability area of a personal-data request is PLATFORM_ADMINISTRATION: the write takes letter U and the reads take letter R; RW-COMPLY holds U in PLATFORM_ADMINISTRATION at the matrix load of this story, and the T6.1 columns of every other role stay unchanged (GAP-2300).
- Every user, case, file and value in the tests is synthetic; no production role, entitlement or personal value is read, and no name is stored in a row, a log or a prompt.
- The load, verify, approve and rollback surface of the permission matrix and the DoA table is confirmed at the RWB-P3 reference-data contract review; until then the load path is a dependency and FR-P4-012 is marked load-based (GAP-1564).

### 4. Flow

1. RW-REFADM prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls `POST /api/recovery/access/v1/admin/reference-loads` with table "permission" and the `validFrom` date.
2. PermissionMatrixLoader validates the file whole: every active role once against all 14 capability areas of `LOV-CAPABILITY`, letters only from C, R, U, D and A in that order or "-", known role codes of `role` at the version in force, and no required value empty. It stores the rows with state Loaded and the new `matrix_version`, and produces the difference report against the version in force (BR2).
3. RW-SECADM reviews the difference report and calls `POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve`.
4. ReferenceLoadApprovalService checks that the approver holds the role the parameter names for the table and is not the person who loaded it, writes one decision-record entry with decision code `AC-VERS` and no case through RWB-PLT-E1027-CON, and marks the version Approved with its valid-from date in one transaction (BR3, BR9).
5. On approval the service publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with the version label, the change kind and the effective date, through the outbox of the service baseline and with no personal value (BR13).
6. From the valid-from date every new session resolves the new version, and a session already open keeps the version it signed in under (RWB-P4-E1022-APP; ASM-1408). The screens and endpoints that the new letters open need no deployment.
7. A person requests a list or a record; the session answer carries the scope descriptor built from the role's `default_scope` and the person's teams and regions, and the owning service applies it in its own query (BR4, BR5). This service answers the descriptor; it runs no query over a case.
8. The guard of RWB-PLT-E1037-CON tests the right in the capability area on the records inside the scope, with the letters of the permission rows this service publishes (BR1).
9. A consuming service reads `GET /api/recovery/access/v1/masking-policies` for the fields and roles of the session. For each field tagged as personal data, when no rule lets a role see it in clear the value comes from the masked view column (`v_ace_customer.id_no_masked`, `v_ace_contact.contact_value_masked`) or is masked where the view holds no masked column; when a rule allows it, the value comes from `v_ace_contact.contact_value` where ACE exposes it, or from `id_no_last4` for the identity number. There is no token and no detokenization call (BR6, BR10).
10. The clear `customer.identification_number` never leaves ACE: no Workbench column, token store or service returns it, and `id_no_last4` is the clearest identity value any role receives.
11. Criterion AC2, AC3 and AC12 name an access event; the decision and the field ids are this story's, and the access-entry writer of RWB-P4-E1039-APP writes one event with the field ids and their masked flags and never a value (BR11, ASM-1412).
12. On each request, the session compares the groups the session holds with the group answer of ACE common, refreshed at most every five minutes; where a group has been removed, the session ends and the request is refused with status 401 and MSG-P4-001 (BR8, ASM-1413). The session lifecycle is RWB-P4-E1022-APP's.
13. The version in force is read from `rwb_access` on each call, with no cache of another service's data and no cache of a peer's answer (ASM-1411).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an action, for example a transfer | Refused with 403 before the handler runs; nothing changes; the refusal is passed to the access-entry writer of RWB-P4-E1039-APP | MSG-P4-002 | AC3 |
| X2 | A record outside the person's scope is requested | Refused with 404; the record is not returned and the count of excluded records is never shown | MSG-P4-003 | AC4 |
| X3 | A matrix file misses a role, repeats a role and area, or holds a letter outside C, R, U, D, A and "-" | The load is refused in full and the version in force stays | MSG-P1-002 | AC5 |
| X4 | The person who loaded a version tries to approve it | Refused; the version stays Loaded | MSG-P7-002 | AC6 |
| X5 | A role other than the table's approver role calls approve | Refused with 403 | MSG-P4-002 | AC6, AC13 |
| X6 | The decision-record write for an approval fails | The version is not approved and stays Loaded; nothing is published | MSG-P7-003 | AC7 |
| X7 | A leaver's group is removed while a session is open | The next request after the membership refresh ends the session | MSG-P4-001 | AC8 |
| X8 | No masking rule exists for a personal field and role | The field shows from the masked view column, or is masked where the view holds no masked column | None | AC9 |
| X9 | Two approve calls for the same load arrive at once | One approves and one decision-record entry is written; the second returns 409 and writes nothing | MSG-GEN-004 | AC10 |
| X10 | A rule asks for the clear identity number | The rule is refused at load; the clearest value a rule can name is `id_no_last4` | MSG-P1-002 | AC14 |
| X11 | A masking file names a role code the `role` table does not hold, or a field id that is not `is_personal` | The whole masking version is refused and the field is named | MSG-P1-002 | AC15 |
| X12 | The masking store or the matrix store is unavailable | The call answers 503 and no version changes | MSG-GEN-006 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the session (RWB-P4-E1022-APP), the four contract fakes and the published contracts of this WP, all earlier in wave 1 |
| Negotiable | Letters, scopes, masking positions, approver roles and the refresh interval are data or parameters; Compliance sets the masking values under DL26 |
| Valuable | A change of rights takes effect by an approved load, and personal data is masked by default at the view and at the API |
| Estimable | One loader, one masking loader, one approval service, one catalogue read, one policy read and one event |
| Small | Fits a sprint with its tests as one slice of a legacy key whose criteria are already written |
| Testable | Each of the thirteen criteria below is one test in section 16, and the boundary parts are proven against the named contract mocks |

### 7. Acceptance criteria

```gherkin
Feature: Role to permission matrix as data and PDPA field masking by role

  Background:
    Given the environment is SIT
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given permission matrix version "PM-2026.11" is in force
    Given RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"
    Given masking version "MASK-SIT-01" is in force, in which only RW-CASEOWN may see v_ace_contact.contact_value in clear for DF-ACE-078

  Scenario: AC1 Matrix as data (legacy RWB-E1-037 AC1)
    Given test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01"
    Given the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11"
    Given test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    Given the rwb-case contract mock returns status 403 with message MSG-P4-002 for GET /queues under "PM-2026.11" and status 200 for GET /queues on 1 December 2026 under "PM-2026.12", authorising against the matrix version in force
    Given the rwb-decision contract mock returns one decision log entry with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102"
    When test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues
    Then the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment
    Then one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102"

  Scenario: AC2 Masking from the view columns (legacy RWB-E1-037 AC2)
    Given test user "U-2104" holds only RW-PHONECOL
    Given the rwb-source-data contract mock returns the borrower of case "RW-2026-000123" with id_no_masked "XXXXXXXXX1234"
    Given the rwb-source-data contract mock returns the mobile as contact_value "0812345678" and contact_value_masked "XXXXXX5678"
    Given the rwb-decision contract mock returns the access event stream of the case record view with the case ID, the field IDs and each field's masked flag
    When the user opens case "RW-2026-000123" in the case record view
    Then the identity number shows "XXXXXXXXX1234" from id_no_masked and the phone number shows "XXXXXX5678" from contact_value_masked
    Then the system reads no clear contact value for the role
    Then the system writes the view to the access event stream with the case ID, the field IDs and each field's masked flag

  Scenario: AC3 Denied action (legacy RWB-E1-037 AC3)
    Given test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R"
    Given the rwb-case contract mock returns the transfer handler of case "RW-2026-000123" and records whether it ran
    Given the rwb-decision contract mock returns the refusal event stream with area "QUEUE_AND_ALLOCATION" and right "U"
    When the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123"
    Then the system refuses the call with status 403 and message MSG-P4-002 before the handler runs
    Then the case owner and queue are unchanged
    Then the system writes one refusal event with area "QUEUE_AND_ALLOCATION" and right "U"

  Scenario: AC4 A case outside the scope is not returned (legacy RWB-E1-037 AC4)
    Given test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases
    Given case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    Given the rwb-case contract mock returns the 12 cases owned by "U-2105" and case "RW-2026-000456" in team "MTG-NE" with another owner, and applies the scope descriptor it is given
    When the user calls GET /cases
    Then 12 cases return and the total is 12
    Then GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003

  Scenario: AC5 A matrix file with an error is refused in full (legacy RWB-E1-037 AC5)
    Given matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting
    When test user "U-2101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the duplicate row and the invalid letters
    Then the system stores no row of "PM-2026.13" and "PM-2026.11" stays in force

  Scenario: AC6 The loader cannot approve (legacy RWB-E1-037 AC6)
    Given load "PM-2026.12" was loaded by test user "U-2101"
    When "U-2101" calls approve on that load
    Then the system refuses the call with message MSG-P7-002 and the load stays "Loaded"

  Scenario: AC7 An approval that cannot be recorded does not take effect (legacy RWB-E1-037 AC7)
    Given the rwb-decision contract mock returns the decision log store as unavailable
    When test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    Then the call returns status 503 with message MSG-P7-003
    Then the load stays "Loaded" and "PM-2026.11" stays in force

  Scenario: AC8 A leaver loses access at the next request (legacy RWB-E1-037 AC8)
    Given test user "U-2107" holds RW-TEAMMGR and has an open session since 08:00
    Given the access administrator removes "U-2107" from group "RWB-SIT-RW-TEAMMGR" at 10:00
    Given the rwb-case contract mock returns the case list of "U-2107" only while the session contract answers the session as open
    When the user calls GET /cases at 10:06, after the 5 minute membership refresh
    Then the system refuses the call with status 401 and message MSG-P4-001
    Then the system ends the session and a new sign-in is refused

  Scenario: AC9 A personal field with no masking rule is masked (legacy RWB-E1-037 AC9)
    Given no masking rule in "MASK-SIT-01" covers v_ace_customer.date_of_birth (DF-ACE-059) for any role
    Given the rwb-source-data contract mock returns the date of birth (DF-ACE-059) for case "RW-2026-000123" and holds no masked value for it
    When test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123"
    Then the date of birth shows masked as "XXXX-XX-XX"

  Scenario: AC10 Two approvals of the same load at once (legacy RWB-E1-037 AC10)
    Given load "PM-2026.12" is "Loaded"
    When two approve calls for it arrive at the same time from "U-2102" and test user "U-2108" holding RW-SECADM
    Then one call approves and one decision log entry is written
    Then the other call returns status 409 with message MSG-GEN-004 and writes nothing

  Scenario: AC11 The clear identity number never leaves ACE (legacy RWB-E1-037 AC11)
    Given the recovery service identity recovery_svc in SIT
    Given the rwb-source-data contract mock returns the customer source record with the identity number "1234567890123" for person_key "P-0001" held only behind id_no_masked and id_no_last4
    When the identity test runs
    Then the rwb-source-data contract mock refuses any read of the clear identity number
    Then the rwb-source-data contract mock returns id_no_masked "XXXXXXXXX0123" and id_no_last4 "0123" and no field holds the clear value
    Then no Workbench table, token store or service returns the clear identity number for any role

  Scenario: AC12 A read of a personal field is audited (legacy RWB-E1-037 AC12)
    Given test user "U-2109" holds RW-CASEOWN, which permits DF-ACE-078 in clear
    Given the rwb-decision contract mock returns the access event stream of case "RW-2026-000123"
    When "U-2109" opens case "RW-2026-000123" and reads the borrower's phone number
    Then one access event is written with the case ID, field ID DF-ACE-078 and the flag "clear"
    Then the event holds no field value, and the phone number "0812345678" appears in no event field

  Scenario: AC13 Only the table's approver role may approve (legacy RWB-E1-037 AC13)
    Given load "PM-2026.12" is "Loaded"
    When test user "U-2106" holding RW-COE calls approve on that load
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then the load stays "Loaded"

  Scenario: AC14 A masking rule that names the clear identity number is refused at load (exception X10) (new, D-RCV-60)
    Given test user "U-2101" loads a masking file in which one rule names the clear identity number
    When the load is checked
    Then the system refuses the load with message MSG-P1-002 and names the rule
    Then the system stores no row of that file and "MASK-SIT-01" stays in force

  Scenario: AC15 A masking file that names an unknown role or a field that is not personal is refused (exception X11) (new, D-RCV-60)
    Given test user "U-2101" loads a masking file that names a role code the role table does not hold or a field id that is not is_personal
    When the load is checked
    Then the system refuses the whole masking version with message MSG-P1-002 and names the field
    Then the system stores no row of that file and "MASK-SIT-01" stays in force

  Scenario: AC16 An approved version is published as a policy event with no personal value (rule BR13) (new, D-RCV-60)
    Given load "PM-2026.12" is "Loaded"
    When test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    Then the system publishes rwb.access.AccessPolicyChanged.v1 on rwb.access.events.v1 with the version, the change kind and the effective date
    Then the event holds no personal value

  Scenario: AC17 Each operation demands the right it declares before its handler runs (rule BR14) (new, D-RCV-60)
    Given a test user holds no right in the Reference data area
    When the user calls GET /masking-policies
    Then the guard refuses the call with message MSG-P4-002 before the handler runs; the status is Not specified in the source documents (DOR-RWB-P4-E1037-APP-4)

  Scenario: AC18 A value a business person may change takes effect from its row with no deployment (rule BR15) (new, D-RCV-60)
    Given the approver role parameter holds "RW-SECADM"
    When the parameter is changed to another approver role in the parameter store
    Then the next approval checks the approver role from the parameter and no code holds the role

```

The thirteen criteria above are the legacy criteria of RWB-E1-037, copied verbatim and tagged with their origin, with the cross-service part of a criterion expressed by the contract mock it runs against: `rwb-case` for GET /queues, GET /cases, GET /cases/{caseId} and POST /cases/{caseId}/transfer, `rwb-decision` for the decision-record entry and the access event stream, and `rwb-source-data` for the ACE view columns. Every value, id, code, field id, message id and version of the legacy line is kept. Where a criterion names the case record view (AC2, AC9, AC12) or the session (AC8), the value the user sees is produced by the policy this story publishes applied by the guard and masker library in the owning service; the end-to-end form of the same criterion is RWB-ITG-E1037-ITG, and the access record it writes is RWB-P4-E1039-APP's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The permission matrix version in force is the only source of what a role may do; a capability area with "-" refuses every action in it | permission.letters (DF-REF-043), matrix_version (DF-REF-044); REQ-ACA-003; CTL-09 |
| BR2 | A matrix file holds every active role once for each of the 14 capability areas, with letters from C, R, U, D, A in that order or "-"; a file with any error is refused in full | LOV-CAPABILITY; reference data change process, step 3; FSD P4 BR-P4-004 |
| BR3 | A version is approved by the role the parameter names for the table, and never by the person who loaded it | Parameters rwb.refload.approver.*; Admin and access model, section 3.3; CTL-05 |
| BR4 | Scope filters records first and the permission is checked second; an out-of-scope record is never returned and the excluded count is never shown | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
| BR5 | OWN means the cases the person owns or has a task on; TEAM means the cases in the person's team queues; REGION means the cases in the regions of the person's teams; ALL means every case | Key sheet, roles.txt |
| BR6 | A personal data field is masked unless the masking rule in force lets one of the session's roles see it; a masked field is filled from the masked view column (`id_no_masked`, `contact_value_masked`), or masked where the view holds no masked column; with no rule it is masked | Masking rules reference table; DL26; CTL-11; REQ-ACA-005; DF-ACE-073, DF-ACE-079 |
| BR7 | Masking is applied before data reaches a screen or an agent, by the masker of RWB-PLT-E1037-CON reading the rules this service publishes | NFR-039; NFR-040 |
| BR8 | A leaver's removal from a group ends the open session at the next request after the membership refresh; leaver removal is within the same working day | DL38; CTL-10; REQ-ACA-011 |
| BR9 | A version approval that cannot be written to the decision record does not take effect, and nothing is published | Principle 5; R-UNI-39; CTL-06 |
| BR10 | There is no tokenization and no token store; the clear `customer.identification_number` never leaves ACE, `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only, and `id_no_last4` is the clearest identity value any role can receive | ADR-010; Data Tier Map section 7; D-RCV-35 U1 |
| BR11 | Every read of a personal data field is written to the access log with the field id and its masked flag, never the value; the writer is RWB-P4-E1039-APP's | REQ-ACA-006; RWB-E1-039 BR3; NFR-040 |
| BR12 | A masking rule names a field id that exists in `sys_fields` with `is_personal` true and belongs to a `recovery.v_ace_*` view or a Workbench table; a rule that names the clear identity number is refused | RWB-E1-069; Data Tier Map section 7 |
| BR13 | A matrix or a masking version that reaches Approved is published as `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with the version, the change kind and the effective date, and no personal value | Arch v5 slide 14; slide 20; ASM-1417 |
| BR14 | Every operation of this story demands the right it declares, through the guard of RWB-PLT-E1037-CON: Reference data C to load, the parameter's approver role to approve, Platform administration R to read the matrix, Reference data R to read the masking rules | TSD P4 v3 T-A; DP-08; TSD P4 v3 API-P4-006 |
| BR15 | No value a business person may change is written in code: the letters, the scopes, the approver roles, the refresh interval, the versions and the effective dates are rows and parameters | FSD P4 BR-P4-004; BR-P4-005; DP-06; DP-07 |
| BR16 | A correction of a personal field is applied by the service that owns the field: rwb-source-data for the source field, rwb-case for the case field and rwb-document for the document; an erasure removes or blanks the field in its owning service, and this service applies neither. The default field set of an erasure and the precedence between a masking row, a retention class and a case hold are Not specified in the source documents (GAP-0876) | Ownership map; FSD P4 A2.27; TSD P4 v3 T3.1; GAP-0876 |

Where each rule sits in the target: BR1 and BR2 are answered from `permission` in `rwb_access` and the whole-file checks before any row is written. BR3 and BR9 are the approve path with the parameter's approver role, the maker and checker check, the decision-record write and the optimistic lock in one transaction. BR4 and BR5 are the scope descriptor in the session answer, applied by the owning service. BR6, BR7 and BR12 are the masking rules this service publishes and the masker that reads them. BR8 is the group comparison on each request, and the session lifecycle is RWB-P4-E1022-APP's. BR10 and BR11 are the identity boundary and the access record. BR13 is the policy event. BR14 and BR15 are the guard and the data rows.

### 9. State transitions

None for a case; this story changes no case status (TSD P4 v3 T4). It moves a matrix or a masking version from Loaded to Approved and into force, or refuses it at validation, and it ends a session when a group is removed. The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P4 v3 T3.2, and the `state` column of the standard record columns holds it.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Matrix or masking version | No version of the table | A file passes every check | LOADED | The rows are stored with the version label and no version is in force yet |
| Matrix or masking version | LOADED | A second person holding the table's approver role approves it | APPROVED | One decision-record entry with code `AC-VERS`, the valid-from date, and `rwb.access.AccessPolicyChanged.v1` published |
| Matrix or masking version | LOADED | Any check fails, or the loader tries to approve, or the approver role is not held | REFUSED for a failed check; LOADED for a refused approval | No row of a refused version is stored; a refused approval changes nothing |
| Matrix or masking version | LOADED | The decision record cannot be written | LOADED | The version is not approved, nothing is published, and the call answers 503 with MSG-P7-003 |
| Matrix or masking version | APPROVED | The valid-from date arrives | IN_FORCE | Every new session resolves it; the version before stays readable with its end date |
| Matrix or masking version | IN_FORCE | A later version is approved with a later date | SUPERSEDED | The later version answers from its date; the rows of this one stay for audit |
| Session | RESOLVED | The person's group is removed and the membership refresh has run | ENDED | The next request answers 401 with MSG-P4-001; the session lifecycle is RWB-P4-E1022-APP's |

A version is never edited in place: a change is a new version with its own label and effective date, and a refused version leaves the version in force untouched.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Application owner (level 1, assumed DL02) | Approves each permission matrix version outside the Workbench; the approval reference is carried in the load file |
| Role owners (level 2) | Request matrix changes for the roles they own |
| RW-REFADM Reference data administrator | Loads a matrix or a masking version (Reference data C); approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission version: the approver role for the `permission` table, from the parameter `rwb.refload.approver.permission=RW-SECADM` |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version: the approver role for the `masking_rule` table, from the parameter `rwb.refload.approver.masking_rule=RW-COMPLY` |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| RW-PLATADM Platform administrator | Reads the matrix and the masking rules through the administration view; changes no row here |
| Access administrator (level 3, bank IAM) | Removes leavers and movers from Entra ID groups |
| Line manager (level 4, bank IAM) | Starts mover and leaver changes |
| Every bank role | Sees cases inside the default scope of its roles, with fields masked per the masking rules |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_customer` and `v_ace_contact` |
| rwb-access service identity (the per-service login, DP-02) | Validates and stores a version, answers the two reads, writes the approval entry and publishes the policy event; holds no grant outside `rwb_access` |

### 11. Data

| BR Field ID | Entity in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Write (one row per role and area of each new version); Read |
| DF-REF-035 | `role` | role_code | Read; the known role codes a matrix file may name |
| DF-REF-038 | `role` | default_scope | Read; the scope descriptor of a role |
| DF-REF-037 | `role` | role_class | Read; the roster check |
| DF-REF-198 | `masking_rule` | id | Write, Read |
| DF-REF-199 | `masking_rule` | role_code | Write, Read |
| DF-REF-200 | `masking_rule` | field_id | Write, Read |
| DF-REF-201 | `masking_rule` | unmasked | Write, Read |
| DF-REF-202 | `masking_rule` | masking_version | Write, Read |
| DF-REF-203 | `masking_rule` | valid_from | Write, Read |
| DF-REF-204 | `masking_rule` | valid_to | Write, Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read only; the rows and the refusal are RWB-P4-E1019-APP's |
| DF-REF-016 to DF-REF-062 | `delegation_limit` | the DoA fields | Named in the contract only; written and read by RWB-P4-E1038-APP and RWB-P4-E2013-APP |
| DF-ACE-073 | `v_ace_customer` (P1) | id_no_masked | Named only; the masked identity value a consuming service shows |
| DF-ACE-074 | `v_ace_customer` (P1) | id_no_last4 | Named only; only with the personal-data permission, and the clearest identity value |
| DF-ACE-055, DF-ACE-057, DF-ACE-058, DF-ACE-059 | `v_ace_customer` (P1) | cif_no, first_name, last_name, date_of_birth | Named only; masked by the masker where no rule covers them |
| DF-ACE-078 | `v_ace_contact` (P1) | contact_value | Named only; clear only where the rule allows it, and audited |
| DF-ACE-079 | `v_ace_contact` (P1) | contact_value_masked | Named only; the masked contact value |
| DF-CAS-009, DF-CAS-011, DF-CAS-012 | `recovery_case` (P3) | owner_user_id, team_code, region_code | Named only; read by the P3 repository applying the scope descriptor |
| DF-DEC-001 to DF-DEC-018 | decision record (P7 through the local library, DP-03) | the approval entry | Write (one entry per approved version) through RWB-PLT-E1027-CON; no P7 table is written |
| DF-DEC-030 | decision record | actor_user_id | Write through the decision-record library |

Field IDs are those of the Logical Data Model and Data Dictionary v9, and DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v7. This story writes no ACE value and no personal value: it writes the rows of the two policy tables and the label of the version they belong to. The unique keys `uk_permission_version` and `uk_masking_rule` are constraints of the two policy tables named in section 12.7; they are not fields and carry no DF id.

Two values the sources do not fix are carried as placeholders. The path and the right of the masking-policy operation are named by Arch v5 slide 14 without a path in the API Specification v5 or TSD P4 v3 appendix T-A, so the base rule of §R4 is applied — Not specified in the source documents (GAP-0778; ASM-1416). The role count is a conflict between the legacy criteria, which count 54 roles against 14 areas for the 756 rows of AC1, and the roster of TSD P4 v3 T6.1, which lists 42 role codes — Not specified in the source documents (GAP-0778; ASM-1415); the story seeds and counts exactly the rows of the approved file and never a constant.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/reference-loads` | Load a matrix file with table "permission" or a masking file with table "masking_rule", with `validFrom`; validate whole and store the version as Loaded | Reference data C (TSD P4 v3 API-P4-005) | `Idempotency-Key`; the same key returns the first response |
| POST | `/api/recovery/access/v1/admin/reference-loads/{loadId}/approve` | Approve a loaded version with the approver role the parameter names, after the maker and checker check, and write the decision record | Reference data A as declared; the approver role of the table in force (TSD P4 v3 API-P4-006) | `Idempotency-Key`; a repeat approve of an Approved load returns 409 and writes nothing |
| GET | `/api/recovery/access/v1/admin/roles` | The permission rows of each role at the matrix version in force: role code, capability area, letters and matrix version, with the scope descriptor of the role | Platform administration R (TSD P4 v3 API-P4-007; Ownership Map path) | Not applicable, read only |
| GET | `/api/recovery/access/v1/masking-policies` | The masking rules in force for the fields and roles of the session: field id, role code, `unmasked`, masking version and validity | Reference data R (Arch v5 slide 14 names the operation; the right is assumed — GAP-0778; ASM-1416) | Not applicable, read only |

All four paths sit on the base `/api/recovery/access/v1` of DP-13. The two load and approve operations keep the legacy shape of RWB-E1-037 section 12 and the path of API Specification v5 `x-module: P4` and TSD P4 v3 appendix T-A (API-P4-005, API-P4-006), and they are the load and approve of **this service's own two tables**; the generic reference-load path for lists, queues, timers, templates and parameters stays with rwb-case (GAP-0778; ASM-1414). `GET /admin/roles` is the Ownership Map path and is one operation with one contract: RWB-P4-E1019-APP answers the role, class, default scope and conflict fields, and this story answers the permission rows and the matrix version of the same answer (ASM-1419). `GET /masking-policies` is the operation Arch v5 slide 14 names; neither the API Specification v5 nor TSD P4 v3 T-A gives it a path, so the base rule is applied and the gap is recorded.

Request and answer field names are the dictionary names DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204 and DF-REF-205 to DF-REF-211; the answer envelope and the problem response are those of RWB-P4-E1037-CON. Errors: 401 no Workbench role (MSG-P4-001); 403 no letter or not the table's approver (MSG-P4-002); 404 no such load (MSG-P4-003); 409 a version of the same label exists, the load is not Loaded, or the caller loaded it (MSG-GEN-004, MSG-P7-002); 422 a failed check with the failed check in the detail (MSG-P1-002); 503 the store or the decision record is unavailable (MSG-GEN-006, MSG-P7-003).

#### 12.2 REST operations consumed

None at run time. This service answers and calls no service on a request: the caller's identity and the group answer arrive in the session of RWB-P4-E1022-APP, the lists and the parameters arrive through the client libraries of DP-06 and DP-07, and the decision record is written through RWB-PLT-E1027-CON. The case, decision and source-data contracts of the criteria exist in this story only as test fakes (section 12.8), each one hop with a 2 s budget under DP-11.

#### 12.3 Events published

| Event | Topic | Payload | When |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | The change kind (`matrix` or `masking`), the version label, the effective date and the approver reference; no field value, no person and no case | On the approval of a matrix or a masking version, in the same transaction as the approval, through the outbox of the service baseline (BR13) |

The topic name and the event name are those Arch v5 slide 14 fixes. The payload shape is not specified by any source — Not specified in the source documents (GAP-0778; ASM-1417) — and the payload carries no personal data by BR13 and NFR-040. The publish uses the outbox of the service baseline; DP-09 and RWB-PLT-TE006-CON are not in this slice's pattern set, and the delivery guarantee is the platform event platform's (ASM-1420). `rwb.access.DoALimitChanged.v1` belongs to RWB-P4-E1038-APP and is not published here.

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Arch v5 slide 14, and the version in force is read from `rwb_access` on each call, so this story subscribes to no topic and writes no inbox row.

#### 12.5 Workflows and activities

None. The load, the approve, the two reads and the publish are synchronous work in the caller's thread. The six-monthly access review (JOB-18) is a Temporal Schedule on the `rwb-access` queue owned by RWB-P4-AD008-APP; DP-10 is referred to here and this story registers no workflow, no activity and no Schedule (ASM-1421).

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job sits in this story: a version takes effect on its date, which is a value the read resolves, and the review Schedule of JOB-18 is RWB-P4-AD008-APP's.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `permission` | `rwb_access` | P4 | Writes the rows of each loaded version; reads them for the matrix answer. Adds `uk_permission_version` on (matrix_version, role_id, capability_area) |
| `masking_rule` | `rwb_access` | P4 | Writes the rows of each loaded version; reads them for the masking-policy answer. `uk_masking_rule` on (role_code, field_id, masking_version) |
| `role` | `rwb_access` | P4 | Read only: the role codes a file may name, the class and the default scope |
| `role_conflict` | `rwb_access` | P4 | Read only: named in the contract; the rows are RWB-P4-E1019-APP's |
| `delegation_limit` | `rwb_access` | P4 | Named only: written and read by RWB-P4-E1038-APP and RWB-P4-E2013-APP |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; this story writes one outbox row per policy event |
| `decision_log_entry`, `approval` | `rwb_decision` | P7 | **Never written**; the approval entry goes through the decision-record library (DP-03) |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; the lists and the parameters arrive through their contracts (DP-06, DP-07) |
| the `recovery.v_ace_*` views and `public.customer` | ACE | P1 / ACE | **Never read**; the field ids are named in the rules and the values stay with their owner (DP-05) |

No foreign key crosses a schema, and no statement of this story names a table outside `rwb_access` or a `public` table.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-case contract mock | `GET /queues`, `GET /cases`, `GET /cases/{caseId}` and `POST /cases/{caseId}/transfer` of rwb-case, with the scope descriptor applied | AC1 (the 200 and the 403 of GET /queues), AC3 (the handler that must not run), AC4 (the 12 cases and the out-of-scope case), AC8 (the case list of a session) |
| rwb-decision contract mock | The decision-record write and the access event stream | AC1 and AC10 (one entry with `AC-VERS`), AC2, AC3 and AC12 (the access event of the view), AC7 (the store unavailable) |
| rwb-source-data contract mock | The `v_ace_customer` and `v_ace_contact` columns DF-ACE-073, DF-ACE-074, DF-ACE-059, DF-ACE-078 and DF-ACE-079 | AC2, AC9 and AC11 |
| rwb-case parameters fake (RWB-P3-E1042-CON) | `rwb.refload.approver.permission=RW-SECADM`, `rwb.refload.approver.masking_rule=RW-COMPLY`, `rwb.access.membership-refresh-minutes=5` | AC1, AC6, AC8, AC13 |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `LOV-CAPABILITY` (14 areas), `LOV-SCOPE`, `LOV-ROLE-CLASS` with a version | AC1, AC5, AC9, so no list value is a constant in a test |
| Matrix and masking file fixtures | This story's own approved and failing files | AC1, AC5, AC6, AC7, AC10, AC13 |

The case, decision and source-data mocks are the fakes of those services' published contracts; WP B-P4-01 carries no C row for the rwb-case case contract, so the mock is taken as that contract's fake and no build of rwb-case is needed (ASM-1422).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/access/v1` | 0 | OpenAPI 3.1, one hop, 2 s timeout; the two reads are read only |
| Kafka | 1 event on `rwb.access.events.v1` | 0 | `rwb.access.AccessPolicyChanged.v1`, published on approval through the baseline outbox |
| Temporal | 0 | 0 | No workflow, activity or Schedule; JOB-18 is RWB-P4-AD008-APP's |
| File | 0 at run time | 0 | The matrix and masking files arrive in the multipart body of the load operation |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.matrix`, module `matrix`, in the service root `th.co.scb.ace.workbench.recovery.access`. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The five policy tables are `rwb_access`'s, the lists are P3's and the views are P1's | none |
| DP-02 | `recovery_svc` login | One login per service: the per-service rwb-access login; the ACE grant the identity test names is RWB-P1-E1069-APP's | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the approval entry of code `AC-VERS` is written through it | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. This service reads no view: it holds the field ids the rules name, and the values stay with the owner | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, for the two approver roles and the refresh interval | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, for `LOV-CAPABILITY`, `LOV-SCOPE` and `LOV-ROLE-CLASS` with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library: every operation demands the letter it declares before its handler runs | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. Referred to: JOB-18 and its six-monthly access review are RWB-P4-AD008-APP's, and this story registers no Schedule | H RWB-PLT-E1071-CON, carried for that sibling |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout: the four operations of this story and the fakes of section 12.8 | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`: every path of this story is on `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema: `V0002__permission_version_index.sql` adds the two unique indexes | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The legacy lake copy of the decision log (RWB-E1-014) is retired and nothing here reads or writes a lake | none |
| DP-19 | Screen, ace-web | gateway-bff composite route: the route renders the masked field, the 403 and the 404 this story produces | H RWB-PLT-N001-CON |

All nine build dependencies and three contract dependencies of the metadata table are carried by this story except RWB-PLT-E1071-CON, which is carried for the sibling Schedule of JOB-18; no dependency is added beyond that row.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | The four operations of section 12.1; validation; problem responses with their message ids |
| PermissionMatrixLoader | Service | Validates a matrix file whole — 54 roles, 14 areas, letters CRUDA or "-", known role codes, no empty value — stores the rows as Loaded and builds the difference report (AC1, AC5) |
| MaskingRuleLoader | Service | Validates a masking file: known role codes, field ids present with `is_personal` true, and no rule naming the clear identity number; stores the rows as Loaded (TC-E1-037-13) |
| ReferenceLoadApprovalService | Service | The approver role from the parameter, the maker and checker check, the decision-record write, the status change and the publish, in one transaction on an optimistic lock (AC1, AC6, AC7, AC10, AC13) |
| MatrixCatalogueService | Service | Answers the permission rows, letters and matrix version of `GET /admin/roles` at the version in force, with the scope descriptor of each role |
| MaskingPolicyService | Service | Answers the rules in force of `GET /masking-policies` for the fields and roles of the session |
| ScopeService | Published interface | Builds the scope descriptor from `role.default_scope` and the teams and regions the session holds; the descriptor carries the scope kind and the case-scope predicate, which the owning service applies to the case ID of each entry inside the query, with case facts from the P3 case read (AC4) |
| AccessPolicyEventPublisher | Service | Writes the outbox row of `rwb.access.AccessPolicyChanged.v1` in the approval transaction; no personal value (BR13) |
| AccessAndAdministrationRepository | Repository | Reads and writes `permission`, `masking_rule`, `role` and `role_conflict` in `rwb_access`; no statement names another schema |
| MaskingRule | Entity | Maps the `masking_rule` table |

**Database and migrations**

- Writes `permission` (role_id, capability_area, letters, matrix_version) and `masking_rule` (role_code, field_id, unmasked, masking_version, valid_from, valid_to) in `rwb_access`, each row carrying the `state` and `version` of the standard record columns.
- The DDL, keys, constraints, indexes, dictionary rows and the Flyway baseline V0001 of the five `rwb_access` authority tables are RWB-P4-E1001-APP's; this story applies that baseline and creates no table.
- Migration `V0002__permission_version_index.sql` adds `uk_permission_version` on `permission (matrix_version, role_id, capability_area)`; `uk_masking_rule` on `masking_rule (role_code, field_id, masking_version)` comes from the baseline V0001. It adds no other object, and the baseline objects are the service template's (DP-15, ASM-1418).
- The approve path locks the load row (`version`), so two approvals of one load cannot both write: one commits and one answers 409 (AC10).
- DB access uses the per-service rwb-access login (DP-02). No grant on any schema other than `rwb_access` is added by this story.
- The decision record is written only through RWB-PLT-E1027-CON, never by SQL against a P7 table (DP-03).
- Masking at the data read is applied by rwb-source-data; this story asserts its effect through the P1 data product contract and the authorise answer, while the guard and the masker stay the platform library's (GAP-0358).

**Configuration and reference data**

- Matrix versions `PM-2026.11` (RW-REFADM loads, RW-SECADM approves) and `PM-2026.12` with 756 permission rows; masking versions `MASK-2026.11` (values DL26, RW-COMPLY approves) and `MASK-SIT-01` for SIT.
- Parameters `rwb.refload.approver.permission=RW-SECADM`, `rwb.refload.approver.masking_rule=RW-COMPLY` and `rwb.access.membership-refresh-minutes=5`, read through RWB-PLT-E1042-CON and RWB-P3-E1042-CON; the five-minute value is the legacy assumption and is carried as ASM-1413.
- `LOV-CAPABILITY`, `LOV-SCOPE` and `LOV-ROLE-CLASS` are read with the version in force through DP-07; no list value is a Java constant.
- Authorisation cache: each service authorises against cached permission data from rwb-access and refuses the action when rwb-access does not answer (fail-closed reading of Architecture v5 slide 35); the cache lifetime is Not specified in the source documents (GAP-0161), fixed by RWB-P4-E1037-CON.
- The masking shape — the last four characters, or the first character and the domain of an e-mail address — is the view function `recovery.ace_mask_value`, owned by the ACE team, so no Workbench parameter sets it.
- The unmasking answer for `interaction.summary` for the caller's roles comes from rwb-access under DP-08; `data_product_access` is P1's data product access catalogue and holds no masking decision, and P1 keeps no masking row of its own (GAP-0584).
- Open decisions carried with their assumptions, each still open: DL02 (ASM-0189, ASM-0324, ASM-5687); DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355); DL38 (ASM-0245, ASM-1413, ASM-1424, ASM-1508). Each assumption stands until its decision closes.

**Build steps**

1. `V0002__permission_version_index.sql` and the two unique indexes, proven by a second apply that reports the version as already applied (DP-15).
2. PermissionMatrixLoader with whole-file validation, the difference report and a failing fixture for each check; tests AC1 and AC5.
3. MaskingRuleLoader with the personal-field check and the refusal of a rule naming the clear identity number; the clear identity rule case of TC-E1-037-13.
4. ReferenceLoadApprovalService with the parameter's approver role, the maker and checker check, the decision-record write, the optimistic lock and the publish in one transaction; tests AC1, AC6, AC7, AC10 and AC13.
5. MatrixCatalogueService and MaskingPolicyService over the version in force, with the guard and the two rights; tests AC1, AC9 and the masking-policy contract cases.
6. ScopeService and the scope descriptor in the session answer, given to P3 as a repository test over `GET /cases` and `GET /cases/{caseId}` through the rwb-case mock; test AC4.
7. AccessPolicyEventPublisher with its outbox row and the no-personal-data assertion on the payload; the contract test of RWB-P4-E1037-CON AC4.
8. The boundary checks: the identity statement of AC11 against the source-data mock, the ACE grant half being RWB-P1-E1069-APP's; the session boundary of AC8 against the session contract, the session being RWB-P4-E1022-APP's; and AC2, AC3 and AC12 against the access-entry writer of RWB-P4-E1039-APP.

**Feature switch.** `rwb.access.permission-matrix`, read through the platform feature-flag library: off returns the version in force to the baseline file and refuses a load with MSG-P4-002. The switch changes no letter, scope, masking position or approver role.

**Done when.** The tests of section 16 pass; the thirteen criteria are proven against the named contract mocks; the masker in SIT shows the same case to three roles with the expected masked and clear fields and Compliance signs that test; the two unique indexes are applied; a second version takes effect on its date with no deployment; and no statement in the package names a table outside `rwb_access`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Session ended after a leaver's group was removed | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission, or approve by a role that is not the table's approver | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P1-002 | A matrix or masking file fails validation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The loader tries to approve their own load | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The approval cannot be written to the decision log | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A second approve of a load already approved | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The reference data store is unavailable | {system} is not available. Try again in a few minutes. |

The message ids and their wording are copied unchanged from RWB-E1-037. Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the text with its placeholders filled; for MSG-P4-002 the `{action}` value names the action the caller tried and never a case fact or a field value, and for MSG-P1-002 the `{check}` value names the failed check and `{source}` and `{date}` name the version and its effective date. Thai text for each message follows DL10.

### 15. Screens and states

No screen is built by this story. The matrix and masking versions arrive by file load until SCR-43 Roles and access and SCR-47 Personal data come in Epic 8 (FEAT-ADM-01, FEAT-ADM-14); the gateway-bff composite route renders the matrices from the two read operations in one hop (DP-19). A person sees the effect in the menu of RWB-P4-E1022-APP, in the masked fields of the case record view of RWB-E1-023, and in 404 responses for out-of-scope cases.

The states an administrator sees are the states of a version: Loaded with its difference report, Approved with its approver and effective date, in force from that date, superseded by a later version, or refused with the failed check named. A refused approval leaves the version Loaded and shows MSG-P7-002 or MSG-P4-002.

Screen states not in the screen specification: SCR-43 has empty, loading, error and no access Not specified in the source documents (CG-ALL-5000). SCR-47 has empty, error and no access Not specified in the source documents (CG-ALL-5001); its loading state follows the screen specification.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-037-13 | AC11, BR10, BR12 | End to end | A rule naming the clear identity number is refused; `public.customer` grant refused; `v_ace_customer` id_no_masked and id_no_last4; the grant and view half is RWB-P1-E1069-APP's and the -ITG copy is RWB-ITG-E1037-ITG's |
| TC-E1-037-01 | AC1, BR1 | End to end | Matrix files PM-2026.11 and PM-2026.12 differing in one letter; 756 rows; the rwb-case and rwb-decision mocks |
| TC-E1-037-02 | AC2, BR6, BR7 | End to end | Synthetic case with `v_ace_customer.id_no_masked` and `v_ace_contact.contact_value_masked` returned by the rwb-source-data contract mock; RW-PHONECOL test user |
| TC-E1-037-03 | AC3, BR1 | End to end | RW-CASEOWN test user calling the transfer endpoint through the rwb-case mock, with the handler asserted not to run |
| TC-E1-037-04 | AC4, BR4, BR5 | End to end | 12 owned cases and one case in another team; the rwb-case mock applies the scope descriptor |
| TC-E1-037-05 | AC5, BR2 | End to end | Matrix file with a duplicate row and an invalid letter |
| TC-E1-037-06 | AC6, BR3 | End to end | Load approved by its loader |
| TC-E1-037-07 | AC7, BR9 | End to end | Decision-record store switched off in the rwb-decision mock |
| TC-E1-037-08 | AC8, BR8 | End to end | Group removed in the ACE test double during a session; the session lifecycle is RWB-P4-E1022-APP's |
| TC-E1-037-09 | AC9, BR6 | End to end | rwb-source-data contract mock returns `v_ace_customer.date_of_birth` (DF-ACE-059) with no masking rule, the view holding no masked column |
| TC-E1-037-10 | AC10 | End to end | Two parallel approve calls on one load |
| TC-E1-037-11 | Access | Component | A role without the right is refused with MSG-P4-002; the legacy level Access maps to Component |
| TC-E1-037-12 | Principle 5 | NFR | The decision-record write forced to fail during an approval; the legacy level Resilience maps to NFR |
| TC-E1-037-14 | AC12, BR11 | End to end | RW-CASEOWN test user reading DF-ACE-078 in clear, with the access event asserted to hold no value |
| TC-E1-037-15 | AC13, BR3 | End to end | RW-COE test user calling approve on a Loaded version |
| TC-E1-037-16 | §12 operations, events and activities | Contract | Consumer contract tests of RWB-P4-E1037-CON for the four operations of section 12.1, the event rwb.access.AccessPolicyChanged.v1 and the activities of section 12 |
| TC-E1-037-17 | §12.7 tables | Boundary | Each table of section 12.7 is read and written in `rwb_access` only; no statement names another schema |
| TC-E1-037-18 | AC14, BR10, BR12 | Component | A masking file with a rule naming the clear identity number; refused with MSG-P1-002 at load |
| TC-E1-037-19 | AC15, BR12 | Component | A masking file naming an unknown role code and a field id that is not is_personal; the whole version refused |
| TC-E1-037-20 | AC16, BR13 | End to end | Approval of PM-2026.12; the publish to rwb.access.events.v1 captured and asserted to hold no personal value |
| TC-E1-037-21 | AC17, BR14 | Component | Test user with no Reference data right calls GET /masking-policies; the handler asserted not to run |
| TC-E1-037-22 | AC18, BR15 | Component | Approver role parameter changed in the parameter store; the next approval checks the new role with no deployment |

The fifteen legacy test cases are kept with their legacy cover and their legacy ids; the Level column maps the legacy level System to End to end, Access to Component and Resilience to NFR. One case is added to a legacy row and no id is invented: TC-E1-037-13 carries the identity rule case and the boundary test of AC11, whose grant and view half is RWB-P1-E1069-APP's and whose -ITG copy is RWB-ITG-E1037-ITG's. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case id.

### 17. Guardrails

- No business value in code: letters, scopes, masking positions, approver roles, versions and the refresh interval are rows or parameters, and a new area or letter is accepted as data (BR15).
- No personal data in logs, tests or prompts: tests use synthetic values, the access event lists field ids and their masked flag and never a value, and the policy event carries no value (BR11, BR13).
- ACE data only through the owner's contract or the service's own `v_ace_*` views, and this service reads neither: the field ids are named in the rules and the values stay in ACE (DP-05, BR10).
- No tokenization and no token store: the clear identity number never leaves ACE, no Workbench column, service or rule returns it, and a rule that names it is refused (BR10, BR12).
- A field with no masking rule is masked, and an unmasked contact value is read only where a rule allows it and every such read is audited (BR6, BR11).
- Default deny on every operation: a missing role answers 401 with MSG-P4-001 and a missing letter 403 with MSG-P4-002, never allow (BR14).
- One writer for a version: only the load and approve path of this story writes `permission` and `masking_rule`, the loading person never approves, and the decision record is written before the change takes effect (BR3, BR9).
- No statement names a table outside `rwb_access`, and no grant on another schema is added (BR1, DP-01).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR2, BR3, BR9, BR15 | TC-E1-037-01, TC-E1-037-05, TC-E1-037-06, TC-E1-037-07, TC-E1-037-10, TC-E1-037-15 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR6, BR7, BR10, BR12 | TC-E1-037-02, TC-E1-037-09, TC-E1-037-13 |
| REQ-ACA-007 | Access outside the matrix refused and recorded | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR11, BR14 | TC-E1-037-03, TC-E1-037-11 |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | Epic 1, 3.4 | FEAT-ACA-14 | All recovery processes | BR4, BR5 | TC-E1-037-04 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | Epic 2, 3.4 | FEAT-ACA-13 | All recovery processes | BR8 | TC-E1-037-08 |
| REQ-ACA-006 | Every read of a personal data field written to the access log | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR11 | TC-E1-037-14 |
| D-RCV-35 U1 | Masking is applied to the view columns; no token is stored at load and the clear identity number never leaves ACE | Decision Log, D-RCV-35 section 6.1; ADR-010 | FEAT-ACA-05 | All recovery processes | BR10, BR12; ADR-010 | TC-E1-037-02, TC-E1-037-13 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1037-CON | Contract | H: the published access and masking contract this story implements, with its fakes |
| RWB-PLT-E1037-CON | Contract | H: the guard, masker and annotation contract every service binds, and the fakes this story tests against; its app story RWB-PLT-E1037-APP implements it and is not built here |
| RWB-P4-E1022-APP | App development | H, in lane: the sign-in, the session, the group-to-role answer and the ending of a session (AC8) |
| RWB-P4-E1039-APP | App development | The access log, the refusal entry and break-glass; it writes the access event of AC2, AC3 and AC12 |
| RWB-P4-E1019-APP, RWB-P4-E1038-APP | App development | The role, class and conflict rows of `GET /admin/roles`; the DoA table this contract names |
| RWB-P1-E1069-APP | App development | The ACE views, the grants and the identity boundary behind AC11 |
| RWB-P7-E1027-CON | Contract | C: the decision-record write of the approval entry |
| RWB-ITG-E1037-ITG | Integration | The end-to-end proof of the same outcome across P4, P1, P3 and the library |

| Legacy reference | Where it is kept |
|---|---|
| The matrix, the masking rules and the scope rule as versioned data (legacy sections 1, 4, 8, 11) | Sections 1, 4, 8, 11, 12 |
| The thirteen legacy criteria with their values and messages (legacy section 7) | Section 7, carried verbatim with the contract mock of the cross-service part |
| The exception paths X1 to X10 of the legacy story (legacy section 5) | Section 5, with the two masking-load paths added |
| The fifteen legacy test cases with their covers (legacy section 16) | Section 16 |
| The messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-P7-002, MSG-P7-003, MSG-GEN-004 and MSG-GEN-006 | Section 14 |
| The authority table of the legacy story (legacy section 10) | Section 10 |
| The legacy solution plan with its loaders, approval service, scope service, masker and revalidation filter (legacy section 13) | Section 13, with the masker and the guard moved to RWB-PLT-E1037 |
| The legacy out of scope list (legacy section 19) | Section 19 |

### 19. Out of scope

- Reallocation of a leaver's or mover's open cases (RWB-E1-030 daily rebalancing; R-UNI-18 and R-UNI-19 in Epic 2).
- Administration screens SCR-43 and SCR-47 (Epic 8, FEAT-ADM-01 and FEAT-ADM-14), and the gateway route that renders them (RWB-PLT-N001-CON).
- Masking values for each role and field (Compliance, DL26).
- The guard, the masker, the `@PersonalData` annotation and the fakes: RWB-PLT-E1037-CON and RWB-PLT-E1037-APP.
- The sign-in, the multi-factor check, the session and the ending of a session: RWB-P4-E1022-APP.
- The access log store, its search and export, the refusal entries and break-glass: RWB-P4-E1039-APP.
- The role, class, default scope and conflict rows of the matrix answer: RWB-P4-E1019-APP; the DoA table: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- Access per data product in the data lake copy (RWB-E1-016 and RWB-P1-E1069-APP); the data lake itself is removed.
- The six-monthly access review list (JOB-18, CTL-10): RWB-P4-AD008-APP.
- The shape of the mask itself, which is the view function `recovery.ace_mask_value` and the ACE team's definition.
- The ACE views, their columns and the grant boundary behind AC11: RWB-P1-E1069-APP, with the -ITG copy of the test in RWB-ITG-E1037-ITG.
