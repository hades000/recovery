# RWB-P4-E2035-APP Next action on the case

**Version 3 changes.**

- MSG-GEN-006 and MSG-P4-001 carry the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2035-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AV |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E2035-APP-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2035-CON; build sequence: the platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are built against the published fakes |
| Contract version | v1 of the rwb-access REST base /api/recovery/access/v1 and of the event names rwb.access.<Event>.v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2035-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 29 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a team manager (RW-TEAMMGR) or an internal auditor (RW-AUDIT) who reads the next action of a case**, I want **the access service to answer whether my role may read that case's next action, which scope admits the case, and what the role named as the owner is called and of which class it is**, so that **the next action reaches only the people entitled to it and always names its owner in the words the role catalogue holds**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E2-035:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers two questions behind the service contract of wave 1: does the caller hold Case record right R on this case, and does the scope in force admit it (`POST /authorise`); and what are the name, the class and the default scope of the role code the next action names (`GET /role-catalogue/{roleCode}`).
- The next action itself — the action text, the owner role code, the due date, `next_action_waiting`, the rule ID and its version, the `NEXT_ACTION_MISSING` task and its cancellation, the JOB-05 check, the read endpoint and the case list and export columns — is the primary slice `RWB-P2-E2035-CON` and `RWB-P2-E2035-APP`, with the case fields at P3 and the rule row, the package version and the decision-log query at P7. This story builds no screen, starts no timer and runs no workflow.
- The case facts the decision needs — the case ID, its owner, its team and the queue role of the case — arrive in the authorise request. `recovery_case`, `queue` and `task` are P3's, so this story reads no case table (DP-01).
- The policy the answers come from is data in `rwb_access`: `role`, `permission`, `masking_rule` and `role_conflict`, with the matrix version in force (`PM-2026.12`). Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP.
- The access log is a decision-record entry on `rwb.decision-record.v1` written through the local library of DP-03: `AC-READ` for a granted read of the next action, `AC-DENY` for a refusal that carries no case data (FEAT-ACA-07, FEAT-ACA-08).

The legacy behaviour carried into the access service is unchanged: a reader whose roles hold no Case record R is refused with MSG-P4-002 and sees no next action (legacy AC13), a case outside the reader's scope is answered as not found, the owner shown for a role whose name and class are data is the role's name, and a role of a customer-party class is the case for the waiting text of BR5 of the legacy key.

### 2. Business rationale

A case owner today reads the case history to work out what is owed next, and a case can wait for weeks with nobody owing anything on it. The rule package that moves the case already holds the action, the owner role and the timer, and the Workbench copies them onto the case; two parts of that copy belong to this service. The owner is a role code, so the words the case owner reads — "Restructuring officer (FCR)", "Waiting for Customer (borrower):" — come from the role catalogue, and if they are written in code a new role or a renamed role needs a release. The next action is also case data, so who may read it is an access decision rather than a screen decision: today any role that reaches the case list sees it, and NFR-042 requires every read of the case store to be logged.

This story supplies the access answer and the role catalogue behind the next action. It meets REQ-WKM-012 on the owner, REQ-WKM-014 on visibility, REQ-WKM-015 and REQ-WKM-016 on the case that has no next action or is overdue, and supports REQ-WKM-013 without reading the rule row. The measures are the FSD one, rule and limit changes made without a code release at 100 percent, because roles and the matrix are versioned data, and the legacy one, the count of active cases with no next action at zero, which this slice supports by keeping the exception task readable to the team manager it is raised for. Under Architecture v5 the access decision is a cached answer of `rwb-access`, each service authorises its own object against it within the 2 s budget, and the answer is one hop (slide 10 note; DP-11).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` in force from wave 1: `POST /authorise`, `GET /me/permissions` and the role-to-permission matrix and masking rows of legacy RWB-E1-037, on base `/api/recovery/access/v1`. This story implements the answer behind the authorise operation for the next-action read and adds the role-catalogue operation |
| RWB-P2-E2035-CON | The next-action facts the request and the tests are built from: the case, the action text, the owner role code, the due date, `next_action_waiting`, the rule ID and the rule version, as the primary slice publishes them. Which of them an authorise request carries is Not specified in the source documents (GAP-2322; ASM-3863) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and contract that carry LOV-SCOPE, LOV-CAPABILITY and LOV-ROLE-CLASS with the version in force (DP-07); the list table stays P3's and no scope name, capability area or role class is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves SCR-03 (DP-19); the route itself is the case service's story |

Business preconditions carried from RWB-E2-035, owned by other services where they say so:

- Permission matrix version `PM-2026.12` is in force and gives CASE_RECORD right R to the reader roles of the background below. The TSD RBAC matrix tabulates three capability areas only, so those letters are read from the pack as data (GAP-2324; ASM-3865).
- Masking version `MASK-SIT-01` is in force (FSD A2.5). The next-action fields themselves are not personal, so no masking row covers them and they come back clear.
- The roles `RW-RESTRUCT`, `CU-BORROW` and `SY-CASEWF` exist in the role catalogue with the names of the background; `CU-BORROW` is of a customer-party class, which the list of role classes does not carry (GAP-2323; ASM-3864).
- The next-action read, its columns in the case list and the export, and the `NEXT_ACTION_MISSING` task exist (RWB-P2-E2035-APP; RWB-P3-E2035-APP).
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 with MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-2322; ASM-3863); the story says "the rwb-access login (DP-02)" and never the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no build dependency of its own (metadata H = None; ASM-1664).
- DL22 service-level durations per route state load as data; the DailyCaseRun check time is Not specified in the source documents (GAP-0734); the owner role class comes from the rwb-access answer as data (GAP-0734).

### 4. Flow

1. Caller: a person opens SCR-03 Case record, or reads the next-action columns of the case list. gateway-bff resolves the session and calls the service that owns the next action; that service builds the authorise request from its own rows and the rule package facts.
2. Caller: the request names the area `CASE_RECORD`, the right `R`, the case ID, the case owner, the team code and the queue role of the case, and the field IDs the screen shows — DF-CAS-049 to DF-CAS-053. The full attribute set is Not specified in the source documents (GAP-2322; ASM-3863).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the rights from `permission` for the matrix version in force, `PM-2026.12`. `role`, `permission` and their versions are read from `rwb_access` only.
4. `rwb-access`, right check: no CASE_RECORD R for any role the caller holds gives a refusal, 403 with MSG-P4-002 naming the action, and no next-action fact in the answer (BR1). The refusal is written as an `AC-DENY` entry (BR7).
5. `rwb-access`, scope check: the case is in scope when its attributes satisfy the caller's `default_scope` in force, read from LOV-SCOPE through the reference-data contract of DP-07 — OWN for a case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case (BR2). A case outside it is answered 404 with MSG-P4-003 and no case data, so the answer never confirms that a case exists (BR2).
6. `rwb-access`, markers: each field ID is answered `masked` or `clear` from `masking_rule` for the masking version in force and the caller's roles; a field with no covering row is masked (BR3). The next-action field IDs are not personal and come back clear.
7. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03 with the case ID and the field IDs and their markers, and returns the answer inside the 2 s timeout of DP-11 (BR6, BR7).
8. Caller, role labels: for the owner role code of the next action it calls `GET /api/recovery/access/v1/role-catalogue/{roleCode}` and gets the role name, the role class and the default scope under the matrix version in force, so it can show "Restructuring officer (FCR)" and produce the waiting text of the legacy BR5 for a party class (BR4, BR5).
9. `rwb-access`: caches the authorise answer and the role rows for the matrix version in force; a caller that asks again under the same version is answered from the cache and reads no matrix row twice, and the read still writes its own `AC-READ` entry (BR8).
10. Policy change: a new matrix version or a role change is approved through the load path, `rwb-access` writes the rows and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction. Every caller and the local cache drop the earlier answer and the next request is served under the new version, with no deployment (BR8).

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of a next action is ever unlogged (BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is outside the caller's scope | Not found: 404 with no case data; one `AC-DENY` entry | MSG-P4-003 | AC3 |
| X2 | The caller holds no role with Case record R | Refused before any case fact is read: 403, no case data, no next-action fact | MSG-P4-002 | AC2 |
| X3 | The decision record cannot be written | Nothing is returned: 503 with no case data, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC9 |
| X4 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read | MSG-P4-001 | AC10 |
| X5 | The role code has no row in force, or is inactive | 404 and no role name; the caller shows the role code as it stands and never a guessed name; the message is Not specified in the source documents (GAP-2322; ASM-3863) | Placeholder | AC11 |
| X6 | Two roles of the caller conflict, for example RW-SECADM with a business role | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | AC12 |
| X7 | A cached answer outlives a policy change | The version-keyed entry is dropped on `AccessPolicyChanged` and the next ask is answered under the new version; no stale grant is served | None | AC7 |
| X8 | The caller is an agent or a service identity | The same checks run under the service identity's roles; a service identity with no role is refused 401, and a role of the non-human class gives no waiting text | MSG-P4-001 | AC6 |
| X9 | A reference list the answer needs is not available | No answer is given rather than a guessed one: 503, and the refusal is recorded | MSG-GEN-006 | AC13 |

A read that carries both an escalation grant and the caller's own scope is not a case of this story: the escalation scope of RWB-E2-015 is RWB-P4-E2015-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P2-E2035-CON and its fake; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, names, classes, scopes and their versions — is data; the story fixes the shape of the two answers and the refusal behaviour only |
| Valuable | The right people see the next action, nobody else is told the case exists, and the owner is named and classed from data so a new role needs no release |
| Estimable | One answer behind an existing operation, one new read operation, one cache, one decision-record path and two indexes |
| Small | Fits one sprint with its tests; no screen, no timer, no workflow and no case field |
| Testable | Every criterion below has a test case in section 16; the next-action side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT and RW-AUDIT, and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR and "ALL" for RW-AUDIT
    Given the role catalogue in force holds "RW-RESTRUCT" named "Restructuring officer (FCR)" of class "BANK_USER", "CU-BORROW" named "Customer (borrower)" of class "CUSTOMER_PARTY" and "SY-CASEWF" named "Case workflow module" of class "NON_HUMAN_ACTOR"
    Given masking version "MASK-SIT-01" is in force and holds no row for DF-CAS-049, DF-CAS-050, DF-CAS-051, DF-CAS-052 and DF-CAS-053
    Given the rwb-integration contract mock returns next action for case "RW-2026-000401" with owner role "RW-RESTRUCT", text "Assign the case to a restructuring officer and start the offer clock", due date 2026-12-15 and rule "R-RES-04" of version "RES-2026.12"

  Scenario: AC1 A reader with Case record R is granted the next action (new, D-RCV-60)
    Given test user "U-7401" holds RW-CASEOWN with default scope "OWN" and owns case "RW-2026-000401"
    Given the rwb-integration contract mock returns next action for case "RW-2026-000401" for team "MTG-BKK" owned by "U-7401"
    When "U-7401" asks POST /api/recovery/access/v1/authorise for case "RW-2026-000401", area "CASE_RECORD", right "R" and field IDs DF-CAS-049, DF-CAS-050, DF-CAS-051, DF-CAS-052 and DF-CAS-053
    Then the answer is granted with scope "OWN" under matrix version "PM-2026.12"
    Then the answer marks DF-CAS-049, DF-CAS-050, DF-CAS-051, DF-CAS-052 and DF-CAS-053 "clear"
    Then one AC-READ decision record is written with the case ID and the five field IDs

  Scenario: AC2 A role without Case record R is refused (new, D-RCV-60)
    Given test user "U-REF-01" holds RW-REFADM and no role with Case record R
    Given the rwb-integration contract mock returns next action for case "RW-2026-000401"
    When "U-REF-01" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" for the next-action read of RWB-P2-E2035-CON
    Then the answer is refused with status 403 and message MSG-P4-002 with action "read the next action"
    Then the answer carries no action text, no owner role, no due date and no rule version
    Then one AC-DENY decision record is written with area "CASE_RECORD", right "R" and result "REFUSED"

  Scenario: AC3 A case outside the scope is not found (new, D-RCV-60)
    Given test user "U-7402" holds RW-TEAMMGR with default scope "TEAM" in team "MTG-BKK"
    Given the rwb-integration contract mock returns next action for case "RW-2026-000407" of team "SME-NTH" owned by another user
    When "U-7402" asks for case "RW-2026-000407", area "CASE_RECORD", right "R"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no case data: no owner, no team, no action text and no due date
    Then one AC-DENY decision record is written and it carries no case ID

  Scenario: AC4 The role catalogue names the owner role (new, D-RCV-60)
    Given the role catalogue in force holds "RW-RESTRUCT" named "Restructuring officer (FCR)" of class "BANK_USER" under matrix version "PM-2026.12"
    When test user "U-7403" holding RW-SPECIAL calls GET /api/recovery/access/v1/role-catalogue/RW-RESTRUCT
    Then the answer is 200 with roleCode "RW-RESTRUCT", roleName "Restructuring officer (FCR)", roleClass "BANK_USER" and matrix version "PM-2026.12"
    Then the answer carries no personal value and no permission row of another role

  Scenario: AC5 A party role is classed as a waiting owner (new, D-RCV-60)
    Given the role catalogue in force holds "CU-BORROW" named "Customer (borrower)" of class "CUSTOMER_PARTY"
    When the caller holding the next action of case "RW-2026-000403" reads GET /api/recovery/access/v1/role-catalogue/CU-BORROW
    Then the answer carries roleName "Customer (borrower)" and roleClass "CUSTOMER_PARTY"
    Then the class is the one the next-action caller turns into the waiting text "Waiting for Customer (borrower):" of the legacy BR5, and this service writes no waiting text of its own

  Scenario: AC6 A non-human role never gives a waiting owner (new, D-RCV-60)
    Given the role catalogue in force holds "SY-CASEWF" named "Case workflow module" of class "NON_HUMAN_ACTOR"
    When the caller holding a next action whose owner role is "SY-CASEWF" reads GET /api/recovery/access/v1/role-catalogue/SY-CASEWF
    Then the answer carries roleClass "NON_HUMAN_ACTOR"
    Then the class is neither a bank user nor a party class, so no waiting text is produced for it

  Scenario: AC7 A policy change replaces the cached answer with no deployment (new, D-RCV-60)
    Given test user "U-7404" holds RW-COMPLAIN, which has no CASE_RECORD right in "PM-2026.12"
    Given the same user asks for case "RW-2026-000401" and is refused with status 403
    When matrix version "PM-2026.13" is approved and gives RW-COMPLAIN CASE_RECORD right "R", and rwb.access.AccessPolicyChanged.v1 is published for it
    Then the next ask by "U-7404" is answered granted under matrix version "PM-2026.13" with no deployment
    Then no answer cached under "PM-2026.12" is served after the change

  Scenario: AC8 Every answer is logged and the refusal carries no case data (new, D-RCV-60)
    Given test user "U-7401" holds RW-CASEOWN and owns case "RW-2026-000401"
    When "U-7401" asks for the same case twice under one matrix version
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then each answer is returned inside the 2 s timeout and each granted read writes its own AC-READ entry
    Then the AC-DENY entry of a refused read carries the area and the right and no case ID

  Scenario: AC9 The record cannot be written, so nothing is returned (new, D-RCV-60)
    Given the decision-record write is forced to fail
    When test user "U-7401" asks for case "RW-2026-000401", area "CASE_RECORD", right "R"
    Then the answer is 503 with message MSG-P7-003 and no case data
    Then an incident is raised to the platform administrator queue and no AC-READ entry is written

  Scenario: AC10 A token with no Recovery role or no second factor gets no answer (new, D-RCV-60)
    Given test user "U-7405" holds a token with no Recovery role, or a Recovery role and no second factor
    When "U-7405" asks for case "RW-2026-000401", area "CASE_RECORD", right "R"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then no policy row is read and the answer carries no case data

  Scenario: AC11 A role code with no row in force gives no name (new, D-RCV-60)
    Given a role code with no row in force, or an inactive row, under matrix version "PM-2026.12"
    When test user "U-7403" holding RW-SPECIAL calls GET /api/recovery/access/v1/role-catalogue/{roleCode} for that role code
    Then the answer is 404 with no roleName and no roleClass
    Then the caller shows the role code as it stands and no guessed name

  Scenario: AC12 Conflicting roles are refused at sign-in (new, D-RCV-60)
    Given test user "U-7406" holds RW-SECADM and a business role that the role_conflict rows in force name as conflicting with RW-SECADM
    When "U-7406" signs in and the sign-in access check runs
    Then the session is refused with message MSG-P4-006
    Then no authorise request is made to POST /api/recovery/access/v1/authorise

  Scenario: AC13 A reference list that is not available gives no answer (new, D-RCV-60)
    Given the reference list LOV-SCOPE is not available from the reference-data contract of DP-07
    When test user "U-7407" asks for case "RW-2026-000401", area "CASE_RECORD", right "R"
    Then the answer is 503 with message MSG-GEN-006 and no guessed scope
    Then the refusal is recorded in the decision record and no case data is returned

  Scenario: AC14 A field with no covering masking row is answered masked (new, D-RCV-60)
    Given test user "U-7401" holds RW-CASEOWN and owns case "RW-2026-000401"
    Given the masking version in force holds no row covering the field ID under test
    When "U-7401" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the field ID under test
    Then the answer marks the field ID "masked" and carries no value for it

  Scenario: AC15 A scope value added as a list row needs no code change (new, D-RCV-60)
    Given LOV-SCOPE in force holds a scope value added as a new list row
    When test user "U-7401" asks for case "RW-2026-000401", area "CASE_RECORD", right "R"
    Then the scope check uses the list value from the reference-data contract and no code change is made

  Scenario: AC16 The case facts come from the request and no case table is read (new, D-RCV-60)
    Given test user "U-7401" holds RW-CASEOWN and owns case "RW-2026-000401"
    When "U-7401" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" with the case owner, team and queue role in the request
    Then the answer is built from the request facts and the access repository reads no table of rwb_case, rwb_decision or rwb_source_data
```

AC1 to AC16 are the criteria this story owns; the fourteen criteria of the legacy key (AC1 to AC14) are owned by RWB-P2-E2035-APP and are proved against this story's answers. In AC1 to AC3 the two assertions that belong to this service are the decision it names, the scope it used and the markers on the field IDs; the next action itself is the fake's. AC4 to AC6 prove that the owner label and its class are data rows with a version, not constants, which is what makes a renamed role or a new role need no release. AC7 and AC8 prove the cache behaves on the policy event rather than on a clock, and that a grant and a refusal are both recorded. AC9 proves the log-first rule: no unlogged read is ever returned. In every case the request and the answer carry identifiers and markers, never a personal value.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force; a caller whose roles hold no Case record R is refused with MSG-P4-002 and no next-action fact | Legacy AC13 and X9; FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.2 |
| BR2 | A case is in scope when its attributes satisfy the caller's `default_scope` in force: OWN, TEAM, REGION or ALL. A case outside it is answered 404 with MSG-P4-003 and no case data | FSD P4 A2.14 VR-P4-014-1; TSD P4 T3.2 LOV-SCOPE |
| BR3 | A field ID is answered `masked` unless a `masking_rule` row for a role the caller holds and that field says unmasked for the masking version in force; with no covering row it is masked | FSD P4 A2.5; NFR-039; NFR-040 |
| BR4 | The role catalogue answers the role name, the role class and the default scope of a role code under the matrix version in force, and names that version; it holds no permission row and no personal value | Legacy section 12 (`ReferenceData.role(roleCode)` returning roleName and roleClass); TSD P4 T3.1 `role`; FSD P4 A2.3 |
| BR5 | A role code with no row in force, or an inactive row, is answered 404 with no name and no class; the caller shows the role code and never a guessed name | Legacy BR9; TSD P4 T3.1 `is_active` |
| BR6 | The owner shown for a next action whose owner role is the role of the case's queue is the case owner, otherwise the role name; the role name and class are this story's, the queue role is P3's | Legacy BR9; `queue.role_code`; ASM-3863 |
| BR7 | Every granted read writes one `AC-READ` entry with the case ID and the field IDs with their markers before the answer is returned, and every refusal writes one `AC-DENY` entry with the area and the right and no case data | FSD P4 A2.7 AC-P4-007-01 and AC-EXC-P4-007-04; FEAT-ACA-07; FEAT-ACA-08 |
| BR8 | An answer is cached for the matrix version in force and dropped when `AccessPolicyChanged` arrives, so a policy or role change takes effect with no deployment and no stale grant is served | FSD P4 AC-P4-004-01; Architecture v5 slide 43; DP-11 |
| BR9 | Role codes, role names, role classes, scope values, capability areas, field IDs and every version are data; no business value is written in code | FSD P4 BR-P4-004, BR-P4-005, BR-P4-014; TSD P4 T3.2 |
| BR10 | The case facts used by a decision arrive in the request; no table of `rwb_case`, `rwb_decision` or `rwb_source_data` is read | DP-01; ownership map |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are the five-character field of TSD P4 T3.1 and the answer names the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` read through DP-07; OWN, TEAM, REGION and ALL are list values, never Java constants, and the attribute names of a request are Not specified in the source documents (GAP-2322; ASM-3863).
- BR3 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`; the answer carries markers, never values.
- BR4 and BR5 are one indexed read of `role` by `role_code` under the matrix version in force; the version named in the answer is the one the role rows were loaded with (GAP-2325; ASM-3866).
- BR6 is the reason the request carries the queue role: this story supplies the role name and class and the caller applies the substitution, so the service needs no case row.
- BR7 is one `RecordAndApply` transaction: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and changes nothing (X3).
- BR8 is a cache keyed by the matrix version; the `AccessPolicyChanged` entry is published by the same transaction that writes the new rows.
- BR9 is visible in the code review: no role code, role name, role class, scope name, capability area, field ID or version string appears in a constant.
- BR10 is the reason there is no case repository: the service holds `role`, `permission`, `masking_rule`, `role_conflict`, the decision record and the outbox, and nothing else.

### 9. State transitions

None. This story changes no case status, writes no next-action field and creates or cancels no task: those are the primary slice's. It owns no workflow and no Schedule. The screens SCR-02, SCR-03 and SCR-09 are not built here; their empty, loading, error and no-access states belong to the primary slice, RWB-P2-E2035-CON and RWB-P2-E2035-APP, which own the screens.

The only states this story has are the states of its two answers:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds Case record R and the case is in scope | The decision, the scope it used, the matrix version and the field markers | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R | 403 MSG-P4-002, no case data | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope | 404 MSG-P4-003, no case data | `AC-DENY` |
| Not answered | The record cannot be written, or the policy cannot be read | 503, no case data | None; the failure is raised as an incident |
| Role resolved | The role code has a row in force | Name, class, default scope and matrix version | None; the catalogue is a read |
| Role not resolved | No row in force, or an inactive row | 404, no name and no class | None |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record R with default scope OWN: reads the next action of a case it owns |
| RW-TEAMMGR, team manager | Case record R with default scope TEAM: reads the next action of a case of its team, including the case that carries `NEXT_ACTION_MISSING` |
| RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Case record R with the role default scope: read the next action of a case within it |
| RW-AUDIT, internal audit | Case record R with default scope ALL: reads any next action |
| RW-REFADM and every role with no Case record R | Refused with MSG-P4-002; no next-action fact is returned |
| SY-CASEWF, SY-RULES, systems and agents | Ask the same questions for their own service under their own roles; a non-human role brings no waiting text |
| RW-COE, center of excellence analyst | Owns the action, owner and timer columns of the rule rows and loads them through the rule package store; this story reads none of them |
| RW-REFADM, reference data administrator | Loads the service levels, the timers and the holiday list of the primary slice; this story reads no such row |
| RW-SECADM, security administrator | Approves the matrix and the role rows through the load path stories; this story reads the versions in force and publishes the change |

Reading is the whole of this story: it grants or refuses a read, names a role and writes the record of it. It changes no case, no role row and no policy row; a policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and break-glass access stays with the wave-1 stories of the service.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-2322; ASM-3863); the story refers to "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X6) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE, LOV-CAPABILITY and LOV-ROLE-CLASS, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The field IDs the answer marks — DF-CAS-049 `next_action_text`, DF-CAS-050 `next_action_owner_role`, DF-CAS-051 `next_action_due_date`, DF-CAS-052 `next_action_rule_id` and DF-CAS-053 `next_action_waiting` — appear in the answer as identifiers with a marker only, and their values are the primary slice's. None of them is personal data, so no `masking_rule` row covers them and they come back clear (BR3).

The case facts of a request — the case ID, its owner, its team and the queue role — are read from the request and never from a table: `recovery_case`, `queue` and `task` are P3's, and no foreign key and no query crosses a schema (DP-01, BR10). Which attributes a request must carry is Not specified in the source documents (GAP-2322; ASM-3863). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Status | What this story decides behind it |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | Existing from wave 1 in RWB-P4-E1037-CON | The right, the scope and the field markers for one area, right, case and field list. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003) |
| GET | `/api/recovery/access/v1/role-catalogue/{roleCode}` | New in this story | The role name, class, default scope and matrix version of one role code; 200, 401, 404 (BR5), 503 |

`GET /me/permissions` and `GET /masking-policies` are the same service's operations and are used by the screens; they are unchanged here. `GET /admin/roles` (API-P4-007) is the Platform administration list and is not used on this path, because a service identity holds no letter there. `GET /doa-limits` belongs to the delegation slice.

#### 12.2 REST operations consumed

None. The case facts arrive in the authorise request, built by the caller from its own rows; this story calls no service at run time. The shape it expects is the one RWB-P2-E2035-CON publishes for the next action, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build. That the authorise request carries those facts rather than an object reference is Not specified in the source documents (GAP-2322; ASM-3863).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, roles, masking), the version label, the valid-from date and the change reference |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value: the `AC-READ` record carries field IDs and markers, the `AC-DENY` record carries the area and the right only, and the policy event carries version labels.

#### 12.4 Events consumed

None. A role or matrix change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged`; the topic exists for the other services' caches (Architecture v5 slide 43: every holder of permission data consumes it for cache refresh).

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`.

#### 12.6 Schedules

None. The JOB-05 next-action check is the primary slice's and becomes a Temporal Schedule on `rwb-integration`; the six-monthly access review list (JOB-18) is RWB-P4-AD008-APP. This story starts no Schedule.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The role code, name, class and default scope of the owner role and of the caller's roles |
| `permission` | P4 (`rwb_access`) | The CASE_RECORD R right and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The markers per role, field and masking version |
| `role_conflict` | P4 (`rwb_access`) | The conflicting pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | The three lists, read through the contract; not owned here |
| `delegation_limit` | P4 (`rwb_access`) | Not read in this story |
| `recovery_case`, `queue`, `task`, `decision_log_entry` | P3 and P7 | Never read; the facts arrive in the request (BR10) |

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration next-action WireMock | RWB-P2-E2035-CON | Case "RW-2026-000401" with owner role RW-RESTRUCT, text "Assign the case to a restructuring officer and start the offer clock", due date 2026-12-15, rule R-RES-04 of version RES-2026.12, team MTG-BKK, owner U-7401; case "RW-2026-000403" with owner role CU-BORROW and waiting true; case "RW-2026-000407" of team SME-NTH |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X3 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.12 and the later PM-2026.13 of AC7; masking version MASK-SIT-01; the roles RW-RESTRUCT, CU-BORROW, SY-CASEWF, RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN and RW-REFADM |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE, LOV-CAPABILITY and LOV-ROLE-CLASS with the version in force, and the unavailable list of X9 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1 new and 1 existing implemented; consumed 0 | Base `/api/recovery/access/v1`; the case facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/nextaction`, Java package `th.co.scb.ace.workbench.recovery.access.nextaction`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the reason the request carries the case facts: `recovery_case`, `queue` and `task` are P3's, so the answer is built from identifiers and never from a joined query. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so an access question and a decision question are answered from one log. DP-04 is recorded because the legacy key carries the RESTRUCTURE rule row and its package version, which the primary slice reads through the rule catalogue of P7; this slice reads no Drools object and needs no KieBase. DP-05 is recorded because the case the next action belongs to shows customer fields; this answer carries the field IDs and the markers and no value, so no `v_ace_*` view is queried here. DP-06 is recorded because the legacy key carries a feature flag and the timers of JOB-05; this slice reads one flag and no parameter value. DP-07 supplies the three lists with the version in force, because `lov_value` stays with P3 under the ownership map and no scope name, capability area or role class is a Java constant. DP-10 is recorded because the legacy key carries JOB-05; in the target that check is a Temporal Schedule of the primary slice, so this story adds no job. DP-11 is the boundary: one hop, 2 s timeout, cached, and both answers must hold inside it. DP-13, DP-14 and DP-15 are the naming and migration conventions. DP-19 is the route that renders the answers; the screen itself is the case service's.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None; ASM-1664).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | The existing authorise operation on `/api/recovery/access/v1`; validation and problem responses |
| AccessDecisionService | Service | Right, scope and markers for one request, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters |
| ScopeRule | Service | Compares the attributes of the request with the `default_scope` value in force |
| RoleCatalogueController | Controller | `GET /role-catalogue/{roleCode}` |
| RoleCatalogueService | Service | The role name, class, default scope and matrix version of one role code; no row in force is a 404 (BR5) |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer and role rows per matrix version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new matrix or role version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of the service behind RWB-P4-E1037-CON, and their rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V2035_1__nextaction_access_read_path.sql` adds `ix_role_code_active` on `role (role_code) WHERE is_active` and `ix_permission_role_area_matrix` on `permission (role_id, capability_area, matrix_version)`, so both reads of an answer are index reads inside the 2 s budget of DP-11.
- The rows are versioned by `matrix_version`, `masking_version` and their `valid_from`; this story writes none of them, and a version is never edited in place.

**Configuration and reference data**

- The matrix version and the masking version in force are data: the latest `valid_from` on or before the business date, read from `permission.matrix_version` and `masking_rule.masking_version`. The masking version of SIT is assumed to be MASK-SIT-01 (ASM-3866).
- LOV-SCOPE, LOV-CAPABILITY and LOV-ROLE-CLASS through the reference-data contract of DP-07 (RWB-P3-E1043-CON). The class `CUSTOMER_PARTY` the party roles carry is not in the list of TSD P4 T3.2 (GAP-2323; ASM-3864).
- No parameter row, no timeout constant and no role code in code: the 2 s is the platform standard of the service client, and the cache lives for the matrix version in force (BR8).
- The database login is the rwb-access login (DP-02): Not specified in the source documents (GAP-2322; ASM-3863).

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the reference lists, with the matrix version named in the answer; tests for AC1 to AC3 and a test that scope values come from LOV-SCOPE, a closed list in Reference Data v5, so a new value is a list change and not a code change.
2. `RoleCatalogueService` and its controller over `role` under the matrix version in force, with the 404 of X5; tests for AC4, AC5 and AC6.
3. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of X3; test AC9.
4. The denial path with the refusal shape and no case data; tests for AC2 and AC8.
5. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test AC7 against the PM-2026.13 fixture.
6. The migration of the two indexes, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size.
7. The contract-fake run of both answers against RWB-P2-E2035-CON and the decision-record fake, so the story builds before the next action exists in the environment.

**Feature switch.** `rwb.access.nextaction.role-labels`, read from the platform feature-flag library under the R-PREC default ruling. Off: the role-catalogue operation answers 404 and the next action shows the role code with no name and no waiting text, so a role label can never be guessed; the access decision, the markers and the access log are unchanged. The switch changes no schema and never widens a scope.

**Done when.** The tests in section 16 pass; a caller holding Case record R is granted the next action of a case it may read, a case outside the scope is answered 404 with no case data, a role without the right is refused with no case data, the owner role is returned with its name and class from a versioned row, a role with no row in force is answered 404, a policy change replaces a cached refusal with no deployment, every answer leaves its record, and nothing is returned when the record cannot be written.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | The access check before this story's answer (X4) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR2 |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X6) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X3) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Try again in a few minutes. | This story, on a reference-list failure (X9) |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "read the next action"; for MSG-P4-003 no case fact is echoed, because the message must not confirm that a case exists. An unknown or inactive role code carries no message of its own in the sources (GAP-2322; ASM-3863); the answer is 404 with an RFC 9457 problem response and no name. Every error is a problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10 (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed by the directive).

### 15. Screens and states

This story builds no screen. SCR-03 Case record, SCR-02 Case list and SCR-09 Exception queue are the case service's through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), and the next action panel and columns are the primary slice's.

What this story decides for those screens is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Read only, granted | The next action, its owner name from the role catalogue, its due date and the rule ID with its version are rendered; the screen holds no access rule of its own |
| SCR-03 Case record | Waiting | The owner class is a party class, so the caller renders "Waiting for {owner}" with the name from the catalogue; the waiting end date is the primary slice's |
| SCR-03 Case record | Overdue | The overdue marker is the primary slice's; the reader is the one this answer granted, and the read is logged |
| SCR-03 Case record | Refused | The page shows MSG-P4-002 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not found | The page shows MSG-P4-003 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not available | The page shows MSG-P7-003 where the record could not be written, and no case fact |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-5390) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-5390) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-5390) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-5390) |
| SCR-02 Case list | Columns shown | The next action, owner and due date columns are rendered only for the readers this answer grants, row by row |
| SCR-02 Case list | Empty | Not specified in the source documents (CG-ALL-5389) |
| SCR-02 Case list | Loading | Not specified in the source documents (CG-ALL-5389) |
| SCR-02 Case list | Error | Not specified in the source documents (CG-ALL-5389) |
| SCR-02 Case list | No access | Not specified in the source documents (CG-ALL-5389) |
| SCR-09 Exception queue | Task open | The team manager reads the case behind `NEXT_ACTION_MISSING` under the same grant; the task itself is P3's |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-5391) |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-5391) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-5391) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-5391) |

A screen that names a role from a constant, or that shows a next action to a reader this service refused, is a defect of the screen: the answer always names the matrix version it used and the catalogue always names the version its rows came from.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01 | AC1, AC4, BR1, BR6 | Component | Case RW-2026-000401 moved by R-RES-04 on 11 December 2026, due 2026-12-15, owner role RW-RESTRUCT |
| TC-E2-035-02 | AC2, BR1, BR2 | Contract | The authorise request of a next-action read by the owning case owner under PM-2026.12 |
| TC-E2-035-03 | AC3, BR4 | Component | Case RW-2026-000403 with owner role CU-BORROW and waiting true |
| TC-E2-035-04 | AC4, BR7 | Component | Case list read by RW-TEAMMGR "U-7402" with the next-action columns of two cases |
| TC-E2-035-05 | AC5, BR6 | Component | R-RES-03 with owner role RW-CASEOWN and a case owner named on the case |
| TC-E2-035-06 | AC6, BR7 | Component | R-DEV-05 with owner role RW-LEGAL read by a role with no Case record R |
| TC-E2-035-07 | AC7, BR2 | Contract | Move on 30 December 2026 with two bank holidays, read by the case owner |
| TC-E2-035-08 | AC8, BR7 | Component | Closed case "RW-2026-000404" read by its owner; the grant is unchanged |
| TC-E2-035-09 | AC9, BR8 | Component | The same read twice under one matrix version |
| TC-E2-035-10 | AC8, BR8 | Component | Two concurrent reads of one case under one matrix version |
| TC-E2-035-11 | AC8, BR1 | Component | Rows filled by the next-action check and read by the team manager of MTG-BKK |
| TC-E2-035-12 | AC4, BR4 | Component | Owner role RW-RESTRUCT on a same-day due date, catalogue read under PM-2026.12 |
| TC-E2-035-13 | AC2, AC3, BR1, BR2 | Component | RW-REFADM "U-REF-01" reads the next action; refused with MSG-P4-002, and the same user on a case of SME-NTH is answered 404 |
| TC-E2-035-14 | AC2, BR1 | Contract | A next-action read on 2027-01-04, asked by a reader whose role holds the right |
| TC-E2-035-15 | AC6 | Component | A role code with no row in force under the matrix version in force; catalogue read, answered 404 |
| TC-E2-035-16 | AC7 | Component | A cached refusal under PM-2026.12 replaced by a policy change to PM-2026.13 (PM-2026.13 fixture) |
| TC-E2-035-17 | AC9 | Component | Forced failure of the access record write; no answer returned |
| TC-E2-035-18 | AC10 | Component | Token with no Recovery role, or a Recovery role and no second factor; answered 401 with MSG-P4-001 |
| TC-E2-035-19 | AC11 | Component | Role code with no row in force under PM-2026.12; catalogue read answered 404 with no name |
| TC-E2-035-20 | AC12 | Component | Session of a user holding RW-SECADM and a conflicting business role; refused at sign-in with MSG-P4-006 |
| TC-E2-035-21 | AC13 | Component | LOV-SCOPE not available from the reference-data contract; answered 503 with MSG-GEN-006 |
| TC-E2-035-22 | AC14 | Component | Field ID with no covering masking row in force; answered masked |
| TC-E2-035-23 | AC15 | Component | Scope value added as a LOV-SCOPE list row; no code change made |
| TC-E2-035-24 | AC16 | Component | Case facts supplied in the request; no rwb_case, rwb_decision or rwb_source_data table read |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the legacy level System maps to Component where the next-action side is stubbed by RWB-P2-E2035-CON and to End to end where the whole screen is exercised, and the legacy Access level of TC-E2-035-13 maps to Component. Every legacy test case of the key is listed above, with its Covers column rewritten to the criteria this story owns; each one is proved twice, at its own legacy assertions in RWB-P2-E2035-APP and at the access and role assertions here. No `-ITG` copy sits in this story: the integration copy of the key is RWB-ITG-E2035-ITG.

### 17. Guardrails

- No business value in code: role codes, role names, role classes, scope values, capability areas, field IDs and the matrix version are data rows and list values; the only switch is a platform flag (BR9).
- No personal data in logs, events, the record or the tests. The answer carries identifiers and markers, the `AC-READ` entry carries the case ID and field IDs, the `AC-DENY` entry carries the area and the right, and test data is synthetic with staff as user references.
- ACE data only through the owner's contract or `v_ace_*` views: this service stores no customer value and queries no ACE view on this path (DP-05).
- No cross-schema read (DP-01): `recovery_case`, `queue`, `task`, `decision_log_entry` and the `v_ace_*` views are never queried; the case facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories write a role, a permission or a masking row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no case data and raises an incident, so no read of a next action is unlogged (BR7).
- The answers are idempotent for a matrix version: the same question under the same version returns the same answer, and the cache is dropped on the policy event rather than on a clock (BR8).
- The feature switch changes one behaviour and no schema, and it never invents a label: off shows the role code and no waiting text.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01, TC-E2-035-04, TC-E2-035-05, TC-E2-035-08, TC-E2-035-13 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04 | TC-E2-035-02, TC-E2-035-12 |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06, TC-E2-035-11 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01, TC-E2-035-04, TC-E2-035-09 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-07, TC-E2-035-10 |

| Legacy reference | Where it is kept |
|---|---|
| The refusal of a role without Case record R (legacy AC13 and X9) | Sections 1, 4, 5, 7, 10, 14 |
| The role table DF-REF-036 `role_name` and DF-REF-037 `role_class`, and `ReferenceData.role(roleCode)` | Sections 1, 8, 11, 12.1 |
| Rules in the catalog: R-RES-03, R-RES-04, R-SET-13, R-DEV-05, R-RES-07, and package version RES-2026.12 | Background, sections 7, 16 |
| BR5 waiting classes, BR9 owner shown and queue role, BR10 rule version | Sections 7, 8, 10 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Legacy key RWB-E2-035, story RWB-P4-E2035-APP, contract RWB-P2-E2035-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The primary slice RWB-P2-E2035-APP and its contract RWB-P2-E2035-CON: the action text, the owner role code, the due date, `next_action_waiting`, the `NEXT_ACTION_MISSING` task and its cancel, the JOB-05 check, the read endpoint and the case list and export columns.
- RWB-P3-E2035-APP: the next-action columns on `recovery_case`, the migration of the five fields, the index on the case table and the case list of RWB-E2-033.
- RWB-P7-E2035-APP: the rule catalogue row, the package version in force, `NoPackageInForce` and the decision-log query of the latest state change.
- The case record view itself (RWB-P3-E1023-APP) and the timers, escalation and deviation panel of RWB-E2-015 (RWB-P4-E2015-APP).
- The RESTRUCTURE rule rows, their values and the timer specs (RWB-E2-042, RWB-E1-073, DL22, DL24) and the service levels and timers table.
- The escalation of an overdue next action (RWB-E2-015) and the next action column in the queue view screens (RWB-E2-011).
- Loading, approving and rolling back the policy pack and the role rows: the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP and RWB-P4-E2014-APP) and the DoA-limits operation.
- Break-glass access, its incident reference, its ceiling and its review, and the access-log search of RWB-P4-AD007-APP.
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP), every other Schedule, and the Helm chart, Kafka subscriptions, metrics, alerts and runbook of this capability (the OPS story of this key).
- RWB-ITG-E2035-ITG, the wave-2 integration harness copy that proves the real cross-service behaviour end to end.
