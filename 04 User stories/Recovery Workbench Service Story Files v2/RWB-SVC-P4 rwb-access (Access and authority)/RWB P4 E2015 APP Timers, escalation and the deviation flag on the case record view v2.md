# RWB-P4-E2015-APP Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E2015-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AK |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1037-CON; RWB-P3-E2015-CON |
| Contract version | RWB-P4-E1037-CON on base `/api/recovery/access/v1`, path version v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-WKM-004, REQ-WKM-005, REQ-DVH-002, REQ-DRI-001) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 22 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a team manager (RW-TEAMMGR), a specialist or an auditor (RW-AUDIT) who opens the case record view**, I want **the access service to answer, for the case and the timers in front of me, whether my role may read the case record, which scope admits it, whether an escalation puts it in front of me, and which personal fields come back masked**, so that **the case record view shows the next deadline, the escalation and the deviation to the people entitled to see them, and nothing about a case to anybody else**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E2-015:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers three questions behind the two operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`: does the caller hold Case record right R, does the scope in force admit this case, and which fields of it are returned masked. The screen SCR-03, the two case read endpoints `GET /cases/{caseId}` and `GET /cases/{caseId}/timers`, the timers, the escalation itself and the deviation panel stay in `rwb-case` (P3) and in `rwb-deviation` (S8); this story builds no screen, starts no timer and runs no workflow.
- The case and timer facts the decision needs — the case, its team, its owner, and the role a `SERVICE_LEVEL` timer is escalated to and the time it was escalated — arrive in the authorise request. The timer rows, the escalation fields `escalated_to_role` and `escalated_at` and the deviation flag are P3's and S8's; this story reads no case table (DP-01). The attribute set of an authorise request is Not specified in the source documents (GAP-0934; ASM-1660).
- The policy the answers come from is data in `rwb_access`: the role list, the role-to-permission matrix version in force (`PM-2026.12`), the scope rule and the masking rows (`MASK-SIT-01`). Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP and is out of scope here.
- The access log is a decision-record entry on `rwb.decision-record.v1` written through the local library of DP-03: `AC-READ` for a granted read with the field IDs returned and their masked markers, `AC-DENY` for a refusal with no case data (FEAT-ACA-07, FEAT-ACA-08).

The legacy behaviour carried into the access service is unchanged: the same five access decisions of RWB-E2-015 section 10 (Case record R with scope Own, Team, Team-plus-escalation, the read-only specialist roles and All for internal audit), the same refusal of a role with no Case record right, the same "not in your scope" answer for a case outside it, and the same masking of the personal fields whatever the screen.

### 2. Business rationale

A programme finding is that the case record view shows the next deadline and the reason a case left its path, but the controls around it are thin: an escalation role is told by e-mail that a service level has breached, a case outside a person's scope is answered with a page that confirms the case exists, and the personal fields on the view are hidden by whichever screen the reader happens to be on. CTL-18 records a prescription date missed because nobody entitled to see it saw it in time; NFR-039 and NFR-040 require role masking at rest and in use, and the PDPA exposure of a case record view read is the reason FEAT-ACA-07 and FEAT-ACA-08 exist. Under Architecture v5 the access decision is a cached answer of `rwb-access` and every service authorises its own object against it, with a 2 s timeout (slide 14; slide 43).

This story supplies that answer for the case record view: the matrix right, the scope rule, the escalation grant of REQ-WKM-004 and the masking profile behind SCR-03. It meets REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and REQ-DRI-001 on the access side, and supports the measure rule and limit changes made without a code release at 100 percent, because the matrix, the scope values, the masking rows and their versions are data. The measure of success is that every read of a case record is granted or refused by the policy in force, that an escalated case is readable by the role it was escalated to and by nobody else, and that every granted read leaves one `AC-READ` entry naming the fields returned and their masked markers.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix and the masking rows as data (legacy RWB-E1-037). This story implements the decision behind those operations for the case record view; it adds no operation |
| RWB-P3-E2015-CON | The case and timer facts the authorise request is built from: the case, its product, its status, its prescription date, its team, its owner, and the `SERVICE_LEVEL` timer with `escalated_to_role` and `escalated_at`, as the P3 slice of this legacy key publishes them. Which of those attributes an authorise request carries is Not specified in the source documents (GAP-0934; ASM-1660) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-SCOPE and LOV-CAPABILITY with the version in force (DP-07); `lov_value` stays P3's, and no scope or capability string is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case record view (DP-19); the route itself is P3's story |

Business preconditions carried from RWB-E2-015, owned by other services where they say so:

- Permission matrix version `PM-2026.12` is in force and gives CASE_RECORD right R to RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL and RW-AUDIT, with default_scope OWN for RW-CASEOWN, TEAM for RW-TEAMMGR and ALL for RW-AUDIT (FSD P4 A2.4, A2.5; TSD P4 T3.2 LOV-SCOPE). That RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and RW-LEGAL keep the scope their role row carries is assumed, since the source names the right and not a scope for them (ASM-1663).
- Masking version `MASK-SIT-01` is in force. That this is the masking version of the SIT environment is Not specified in the source documents (GAP-0936; ASM-1662).
- The `SERVICE_LEVEL` rows carry the escalation role for each product and status, and `prescription.warning-days` is in force (assumed 90; DL22). Both are P3's data; this story reads neither.
- The case record view SCR-03 and its timers exist (RWB-E1-035, RWB-E1-028, and the P3 slice of this key).
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-0934; ASM-1660); the story says "the rwb-access login (DP-02)" and never the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None).

### 4. Flow

1. Caller: a person opens SCR-03 Case record for a case. gateway-bff resolves the session and calls the case service; the case service builds the authorise request from the case and its timers.
2. Caller: the request names the area `CASE_RECORD`, the right `R`, the case, and the object attributes the policy reads — the team, the owner, and the escalated role and time from the `SERVICE_LEVEL` timer when one is escalated. The full attribute set is Not specified in the source documents (GAP-0934; ASM-1660).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the rights from `permission` for the matrix version in force, `PM-2026.12`. `role`, `permission`, `matrix_version` and their versions are read from `rwb_access` only.
4. `rwb-access`, right check: no CASE_RECORD R for any role the caller holds gives a refusal, 403 with MSG-P4-002 naming the action, and no case data (BR1). The refusal is written as an `AC-DENY` entry (BR6).
5. `rwb-access`, scope check: the case is in scope when the object attributes satisfy the caller's `default_scope` in force, read from LOV-SCOPE through the reference-data contract of DP-07: OWN for a case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case (BR2). A case outside the scope is answered 404 with MSG-P4-003 and no case data, so the answer never confirms that a case exists (BR2).
6. `rwb-access`, escalation scope: while a `SERVICE_LEVEL` timer of the case is escalated to a role the caller holds, the answer is granted even though the case is in nobody's own or team scope of that caller, and the answer carries the reason the grant was given (BR3; REQ-WKM-004). The grant is computed per request from the attributes: when the escalation closes, the next request is answered by the scope rule again (BR3).
7. `rwb-access`, masking: the profile for the field IDs the caller asks about is read from `masking_rule` for the masking version in force, `MASK-SIT-01`, and for the roles the caller holds. A field with no covering row is masked (BR4). The answer marks each field `masked` or `clear`; it never carries the value, clear or masked (BR4).
8. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03, with the case ID, the field IDs returned and their masked markers, and returns the answer to the caller inside the 2 s timeout of DP-11 (BR5; AC-READ).
9. `rwb-access`: caches the policy answer for the versions in force. A caller that asks again under the same versions is answered from the cache and reads no matrix row twice; the `AC-READ` entry is still written for that read (BR7).
10. Policy change: a new matrix version (`PM-2026.13`) or a new masking version is approved through the load path, `rwb-access` writes the rows, and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`. Every caller drops its cached answer and the next request is answered under the new version, with no deployment (BR7).
11. Case service: renders SCR-03 with the granted fields, the masked markers and the "not in your scope" page for a 404; the timers, the escalation line and the deviation panel are its own (RWB-P3-E2015-APP/CON). The empty, loading, error and no-access states of SCR-03 and SCR-04 are owned by RWB-P3-E2015-APP; this story supplies their data answers: the granted or masked fields, the 403 refusal (MSG-P4-002), the 404 refusal (MSG-P4-003), the 503 with MSG-P7-003 and the MSG-GEN-006 list failure.

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of a case is ever unlogged (BR5, BR6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is outside the caller's scope and no escalation covers it | Not found: 404 with no case data; one `AC-DENY` entry, no case data | MSG-P4-003 | AC2, AC3 |
| X2 | The caller holds no role with Case record R | Refused before any case fact is read: 403, no case data | MSG-P4-002 | AC7, AC8 |
| X3 | No masking rule covers a personal field | The field is marked `masked` with the default marker; the read is otherwise granted | None | AC5 |
| X4 | The escalation closes while the caller holds the case open | The grant ends: the next request is answered by the scope rule and refused 404 | MSG-P4-003 | AC4 |
| X5 | The decision record cannot be written | Nothing is returned: 503 with no case data, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC10, TC-E2-015-08 |
| X6 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | AC11, BR1 |
| X7 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | AC12, BR8 |
| X8 | The caller is an agent or a service identity, not a person | The same checks run under the service identity's roles; a service identity with no role is refused 401 | MSG-P4-001 | AC13, BR1, BR8 |
| X9 | The reference list of scope or capability is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | AC14, BR8 |

A range answer with two masking versions in force on the same day is not specified in the source documents (GAP-0936; ASM-1662); until it is, the version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P3-E2015-CON and the contract fake of the case and timer facts; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, scope values, masking rows and their versions — is data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | The right people see the deadline, the escalation and the deviation on the case; nobody else is told the case exists; the personal fields are masked by role everywhere |
| Estimable | Three answers behind existing operations, one cache, one decision-record path and one index |
| Small | Fits one sprint with its tests; no screen, no timer and no workflow |
| Testable | Every owned criterion has a test case in section 16; the case side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL and RW-AUDIT, and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR and "ALL" for RW-AUDIT
    Given masking version "MASK-SIT-01" is in force and holds unmasked "false" for DF-PTY-007, DF-PTY-008 and DF-PTY-016 for RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL and RW-AUDIT
    Given the rwb-case contract mock returns case "RW-2026-000501" with product "HIRE_PURCHASE", status "IN_PROGRESS", prescription date 2027-02-13, owner "U-7301", team "MTG-BKK" and a "SERVICE_LEVEL" timer escalated to "RW-TEAMMGR" at 2026-12-12 09:05

  Scenario: AC1 A granted read answers with the field markers (new, D-RCV-60)
    Given test user "U-7301" holds RW-CASEOWN and owns case "RW-2026-000501"
    Given the rwb-case contract mock returns case "RW-2026-000501" in team "MTG-BKK" owned by "U-7301"
    When the caller asks POST /api/recovery/access/v1/authorise for case "RW-2026-000501", area "CASE_RECORD", right "R" and field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016
    Then the answer is granted with scope "OWN" under matrix version "PM-2026.12"
    Then the answer marks DF-PTY-007, DF-PTY-008 and DF-PTY-016 "masked" under masking version "MASK-SIT-01"
    Then one AC-READ decision record is written with the case ID and the three field IDs marked "masked"

  Scenario: AC2 A case outside the scope is not found (new, D-RCV-60)
    Given test user "U-7301" holds RW-CASEOWN with default scope "OWN" in team "MTG-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000507" in team "SME-NTH" owned by another user
    When "U-7301" asks for case "RW-2026-000507", area "CASE_RECORD", right "R"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no case data: no owner, no team, no timer and no field marker

  Scenario: AC3 Team scope admits a case of the caller's team (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with default scope "TEAM" in team "SME-NTH"
    Given the rwb-case contract mock returns case "RW-2026-000507" in team "SME-NTH" owned by another user
    When "U-7302" asks for case "RW-2026-000507", area "CASE_RECORD", right "R"
    Then the answer is granted with scope "TEAM"
    Then when a caller with default scope "TEAM" in team "MTG-BKK" asks for the same case
    Then the answer is refused with status 404 and message MSG-P4-003

  Scenario: AC4 Escalation scope grants the case while the escalation is open (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with default scope "TEAM" in team "MTG-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000501" in team "SME-NTH" with a "SERVICE_LEVEL" timer escalated to "RW-TEAMMGR" at 2026-12-12 09:05
    When "U-7302" asks for case "RW-2026-000501", area "CASE_RECORD", right "R" and the attributes carry escalatedToRole "RW-TEAMMGR" at 2026-12-12 09:05
    Then the answer is granted with scope "TEAM" and the reason "ESCALATED_TO_ROLE"
    Then when the rwb-case contract mock returns the same case with the escalation closed and no escalated role
    Then the same request is refused with status 404 and message MSG-P4-003

  Scenario: AC5 A field with no masking row is masked (new, D-RCV-60)
    Given no masking rule in "MASK-SIT-01" covers DF-PTY-008 for any role
    Given test user "U-7301" holds RW-CASEOWN and owns case "RW-2026-000501"
    When the caller asks for case "RW-2026-000501", area "CASE_RECORD", right "R" and field IDs DF-PTY-008 and DF-PTY-016
    Then the answer marks DF-PTY-008 "masked" with the default marker "XXXX-XX-XX"
    Then the answer marks DF-PTY-016 "masked"
    Then the read is otherwise granted and one AC-READ entry names both field IDs as "masked"

  Scenario: AC6 Internal audit reads any case and still sees masked fields (new, D-RCV-60)
    Given test user "U-7303" holds RW-AUDIT with default scope "ALL"
    Given the rwb-case contract mock returns case "RW-2026-000507" in team "SME-NTH" owned by another user
    When "U-7303" asks for case "RW-2026-000507", area "CASE_RECORD", right "R" and field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016
    Then the answer is granted with scope "ALL"
    Then the three field IDs are still marked "masked" under masking version "MASK-SIT-01"

  Scenario: AC7 A role without Case record R is refused (new, D-RCV-60)
    Given test user "U-7304" holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When the caller asks for case "RW-2026-000501", area "CASE_RECORD", right "R" for the timer read GET /cases/{caseId}/timers
    Then the answer is refused with status 403 and message MSG-P4-002 with action "read the timers"
    Then no timer, no field marker and no case data is returned

  Scenario: AC8 A refusal is recorded with no case data (new, D-RCV-60)
    Given test user "U-7304" holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When "U-7304" asks for case "RW-2026-000501", area "CASE_RECORD", right "R" and the answer is refused
    Then one AC-DENY decision record is written with area "CASE_RECORD", right "R" and result "REFUSED"
    Then the record carries no case ID, no owner, no team and no field marker

  Scenario: AC9 A policy change refreshes the cached answer (new, D-RCV-60)
    Given test user "U-7305" holds RW-LEGAL, which has CASE_RECORD right "R" in "PM-2026.12"
    Given the rwb-case contract mock returns case "RW-2026-000501"
    When "U-7305" asks for case "RW-2026-000501" twice inside one policy version
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then each answer is returned inside the 2 s timeout and each granted read writes its own AC-READ entry
    Then when policy version "PM-2026.13" is approved and rwb.access.AccessPolicyChanged.v1 is published for it
    Then the next ask is answered under matrix version "PM-2026.13" with no deployment

  Scenario: AC10 A granted read whose decision record cannot be written is not answered (new, D-RCV-60)
    Given test user "U-7301" holds RW-CASEOWN and owns case "RW-2026-000501"
    When the caller asks for case "RW-2026-000501", area "CASE_RECORD", right "R" and the AC-READ decision record write fails
    Then the answer is refused with status 503 and message MSG-P7-003
    Then the answer carries no case data and no field marker
    Then an incident is raised to the platform administrator queue

  Scenario: AC11 A token with no Recovery role is refused before the policy is read (new, D-RCV-60)
    Given a test token carries no Recovery role
    When the caller asks for case "RW-2026-000501", area "CASE_RECORD", right "R"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the permission matrix is not read and one refusal entry with the reason is written

  Scenario: AC12 Two conflicting roles stop the session at sign-in (new, D-RCV-60)
    Given a test user holds RW-SECADM together with a business role
    When the caller signs in to the Recovery Workbench
    Then the sign-in access check refuses the session with message MSG-P4-006 naming both roles
    Then no authorise request is made

  Scenario: AC13 A service identity is checked under its own roles (new, D-RCV-60)
    Given a service identity holds no role
    When the service identity asks for case "RW-2026-000501", area "CASE_RECORD", right "R"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the same checks run under the roles of the service identity and no person role is assumed

  Scenario: AC14 An unavailable reference list gives no guessed answer (new, D-RCV-60)
    Given the reference list of scope or capability is not available
    When test user "U-7301" asks for case "RW-2026-000501", area "CASE_RECORD", right "R"
    Then the answer is refused with status 503 and message MSG-GEN-006
    Then no guessed scope or capability is used and the refusal is recorded

  Scenario: AC15 Role codes, scope values and masking rows are read as data (new, D-RCV-60)
    Given the default scope and the masking rows of "MASK-SIT-01" are read from rwb_access and the reference lists
    When test user "U-7301" holds RW-CASEOWN, owns case "RW-2026-000501" and asks for area "CASE_RECORD", right "R" and field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016
    Then the answer is granted with scope "OWN" and the three field IDs are marked "masked"
    Then no role code, scope name, capability area, field ID or version string is held as a constant in the code

  Scenario: AC16 Case facts arrive in the request and no case table is read (new, D-RCV-60)
    Given test user "U-7301" holds RW-CASEOWN and owns case "RW-2026-000501"
    When the caller asks for case "RW-2026-000501", area "CASE_RECORD", right "R" with the case ID, team, owner, status and escalation attributes in the request
    Then the answer is granted with scope "OWN"
    Then no table of rwb_case, rwb_deviation or rwb_decision is read

  Scenario: AC17 A provided operation answers 401 when the token is not valid (new, D-RCV-60)
    Given a request to a provided operation carries a token that is not valid
    When the caller asks POST /api/recovery/access/v1/authorise for case "RW-2026-000501", area "CASE_RECORD", right "R"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the caller asks GET /cases/{caseId}/timers for the same case and the answer is refused with status 401 and message MSG-P4-001
    Then no timer, no field marker and no case data is returned and the permission matrix is not read
```

AC1 to AC17 are the criteria this story owns; the case-side criteria AC1 to AC10 of the legacy key are owned by RWB-P3-E2015-APP/CON and are proved against this story's answers. In AC1 the two assertions that belong to this service are the scope it names and the masked markers on the field IDs; the timer list itself is P3's. In AC2 and AC3 the two callers prove that scope is read per role and per team, not per case. In AC4 the grant is computed from `escalatedToRole` and ends when the escalation closes, so a case that leaves the queue for an escalation does not leak to the former escalation role. In AC5 the default is masked when no row covers the field, which is the exception path AC-EXC-P4-004-05 of the FSD. In AC6 scope ALL widens the scope and changes no masking row. In AC7 and AC8 the refusal is proved twice: as the answer the caller gets, and as the entry the audit reads. In AC9 the cached answer is proved to change on the policy event and to need no deployment. In AC10 to AC14 each exception of section 5 that had no criterion has its own; AC15 and AC16 prove BR8 and BR9, which no criterion covered. AC17 proves the 401 answer of the provided operations, which no criterion covered.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force; a caller whose roles hold no Case record R is refused with MSG-P4-002 and no case data | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; FEAT-ACA-04 |
| BR2 | A case is in scope when the object attributes the request carries satisfy the caller's `default_scope` in force: OWN, TEAM, REGION or ALL; a case outside it is answered 404 with MSG-P4-003 and no case data | FSD P4 A2.14 VR-P4-014-1; LOV-SCOPE; legacy AC9 |
| BR3 | While a `SERVICE_LEVEL` timer of a case is escalated to a role, a caller holding that role gets Case record R on that case although it is in neither queue nor own scope; the grant ends when the escalation closes, and the case does not move | REQ-WKM-004; R-UNI-30; FSD P4 A2.14 |
| BR4 | A personal field is marked `masked` unless a `masking_rule` row for a role the caller holds and that field says unmasked true for the masking version in force; with no covering row the field is masked | FSD P4 A2.5; AC-EXC-P4-004-05; NFR-039; NFR-040 |
| BR5 | Every granted case read writes one `AC-READ` decision record with the case ID and the field IDs returned with their masked markers, before the answer is returned | FSD P4 A2.7 AC-P4-007-01; FEAT-ACA-07; FEAT-ACA-08 |
| BR6 | Every refusal writes one `AC-DENY` decision record with the area and the right, and carries no case data | FSD P4 A2.7 AC-EXC-P4-007-04; FEAT-ACA-07 |
| BR7 | An answer is cached for the policy versions in force and dropped when `AccessPolicyChanged` arrives, so a policy change takes effect with no deployment | Architecture v5 slide 43; FSD P4 AC-P4-004-01; DP-11 |
| BR8 | Role codes, scope values, capability areas, masking rows and every version are data read from `rwb_access` and the reference lists; no business value is written in code | FSD P4 BR-P4-004, BR-P4-005; TSD P4 T3.2; principle 1 |
| BR9 | The case and timer facts used by a decision arrive in the request; no table of `rwb_case`, `rwb_deviation` or `rwb_decision` is read | DP-01; ownership map (case, timer, deviation to P3 and S8) |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are held as the five-character field of TSD P4 T3.1, and the answer names the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; the scope names OWN, TEAM, REGION and ALL are list values, never Java constants, and the attribute names of a request are Not specified in the source documents (GAP-0934; ASM-1660).
- BR3 is the only exception to BR2, and it is narrow: it needs an escalated role the caller holds and an open escalation in the attributes. Which scope prevails when the caller's own scope and an escalation grant both admit the case, and what scope the answer names then, are Not specified in the source documents (GAP-0935; ASM-1661); this story names the wider of the two and records the reason.
- BR4 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`; the answer carries markers, never values, so no personal data crosses the boundary in either direction (NFR-039).
- BR5 and BR6 are the same `RecordAndApply` transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and changes nothing (X5).
- BR7 is a cache keyed by the matrix and masking versions in force; the `AccessPolicyChanged` entry that drops it is published by the same transaction that writes the new policy rows.
- BR8 is visible in the code review: no role code, scope name, capability area, field ID or version string appears in a constant, and the policy pack is loaded by the stories of the load path.
- BR9 is the reason there is no repository for a case: the service holds `role`, `permission`, `masking_rule`, `role_conflict`, the decision record and the outbox, and nothing else.

### 9. State transitions

None. This story changes no case status, no timer, no escalation and no deviation: the case, the timers and the deviation flag are P3's and S8's, and the durable timer that breaches a service level runs inside the workflow that owns the case (Temporal and Drools design; Architecture v5 slides 42 and 44). This story runs no workflow of its own and owns no Schedule.

The only states this story has are the states of its answer and of its record, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds Case record R and the case is in scope, by the scope rule or by an escalation grant | The granted answer with the scope it used, the reason where an escalation granted it, and the masked markers | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R | 403 MSG-P4-002, no case data | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope | 404 MSG-P4-003, no case data | `AC-DENY` |
| Not answered | The record cannot be written, or the policy cannot be read | 503, no case data | None; the failure is raised as an incident |

The escalation grant of BR3 has no stored state: it exists while the timer row of P3 carries the escalated role and time, and it is recomputed on every request, so closing the escalation closes the grant with no call between the services.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record R with default scope OWN: reads a case it owns, with the personal fields masked |
| RW-TEAMMGR, team manager | Case record R with default scope TEAM: reads a case of its team, and a case escalated to RW-TEAMMGR while the escalation is open |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Case record R with the role default scope: read the case, its timers and its deviation flag within that scope |
| RW-AUDIT, internal audit | Case record R with default scope ALL: reads any case; the personal fields stay masked |
| RW-REFADM and every role with no Case record R | Refused with MSG-P4-002; no case data is returned |
| RW-SECADM, security administrator | Approves the permission matrix and masking versions through the load path stories; this story reads the versions in force and publishes the change |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which fields it covers, through `GET /masking-policies`; this story writes no value on their behalf |
| SY-CASEWF and the other service identities | Ask the same question for their own service; the roles of the service identity are checked as a person's are |

Reading is the whole of this story: it grants or refuses a read and writes the record of it. It changes no case, no timer, no deviation and no policy row; a policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and a break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0934; ASM-1660); the story refers to "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X7) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE and LOV-CAPABILITY values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The field IDs the answer marks — DF-PTY-007 `id_no_token` over `v_ace_customer.id_no_masked`, DF-PTY-008 `date_of_birth` and DF-PTY-016 `value_token` — appear in `masking_rule.field_id` and in the answer as identifiers only. No personal value enters `rwb_access`, the answer, the record or the event: masking markers are the whole payload (NFR-039, NFR-040). Field IDs are those in the Logical Data Model and Data Dictionary v9.

The case and timer facts of a request — the case ID, its team, its owner, its status, and `escalated_to_role` and `escalated_at` of the escalated `SERVICE_LEVEL` timer — are read from the request and never from a table: `recovery_case`, `timer` and `task` are P3's and `deviation` is S8's, and no foreign key and no query crosses a schema (DP-01). Which attributes a request must carry is Not specified in the source documents (GAP-0934; ASM-1660).

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The right, the scope, the escalation grant and the masked markers for one area, right, case and field list. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the matrix version and the scope of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the fields it covers for the caller's roles |

`GET /doa-limits` is the same service's operation and is not used here: the delegation of authority table and its routing lookup are RWB-P4-E2013-APP's.

#### 12.2 REST operations consumed

None. The case and timer facts arrive in the authorise request, built by the caller from its own rows; this story calls no service at run time. The shape it expects is the one RWB-P3-E2015-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, masking, roles), the version label, the valid-from date and the change reference |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value: the `AC-READ` record carries field IDs and markers, the `AC-DENY` record carries the area and the right only, and the policy event carries version labels. `rwb.access.DoALimitChanged.v1` belongs to the delegation slice and is not published here.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh).

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. The timers it reasons about are durable timers inside the workflow that owns the case, and the escalation fields are written there (Temporal and Drools design; Architecture v5 slides 42 and 44).

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service, and its story is RWB-P4-AD008-APP. This story starts no Schedule and reads no `timer` row.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The CASE_RECORD right and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The masked markers per role, field and masking version |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE and LOV-CAPABILITY, read through the contract; not owned here |
| `delegation_limit` | P4 (`rwb_access`) | Not read in this story; it is the delegation slice's |

No table of `rwb_case`, `rwb_deviation`, `rwb_decision` or `rwb_source_data` is read: the case, the timer, the deviation and the customer fields stay with their owners, and the only fields of them that enter this service are identifiers carried by a request (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case case and timer WireMock | RWB-P3-E2015-CON | Case "RW-2026-000501" with product HIRE_PURCHASE, status IN_PROGRESS, prescription date 2027-02-13, owner "U-7301", team "MTG-BKK" and a `SERVICE_LEVEL` timer escalated to RW-TEAMMGR at 2026-12-12 09:05; case "RW-2026-000502" with deviation X3 open; case "RW-2026-000507" in team SME-NTH; the same case with the escalation closed for AC4 |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X5 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.12, masking version MASK-SIT-01 and the later PM-2026.13 for AC9; the roles, scopes and masking rows of the background |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE and LOV-CAPABILITY with the version in force, and the unavailable list of X9 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the case facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output, and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/authorise`, Java package `th.co.scb.ace.workbench.recovery.access.authorise`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the reason the service answers from the attributes it is given: `recovery_case`, `timer`, `task` and `deviation` are P3's and S8's, and the `v_ace_*` customer fields are P1's, so the answer is built from identifiers and never from a joined query. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so an access question and a decision question are answered from one log. DP-07 supplies LOV-SCOPE and LOV-CAPABILITY with the version in force, because `lov_value` stays with P3 under the ownership map; no scope name is a Java constant. DP-10 is recorded because the legacy key carries JOB-05 and JOB-18: in the target no job of this key runs from a shared Quartz table, the service level clock is a durable timer of the workflow that owns the case, and JOB-18 (access review) is RWB-P4-AD008-APP — so this story adds no job. DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it. DP-13, DP-14 and DP-15 are the naming and migration conventions of the service. DP-19 is the route that renders the answer: the screen, its panels and its states are RWB-P3-E2015-APP/CON, and this story supplies only the grant and the markers.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None; ASM-1664), and JOB-18 (access review) is RWB-P4-AD008-APP.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| AccessDecisionService | Service | Right, scope, escalation grant and masking profile for one request, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters |
| ScopeRule | Service | Compares the object attributes of the request with the `default_scope` value in force |
| EscalationScopeService | Service | The grant of BR3 from `escalatedToRole` and `escalatedAt`; no stored state |
| MaskingProfileService | Service | The masked markers per field ID for the caller's roles and the masking version in force; default masked |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer per policy version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new policy version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V2015_1__access_decision_read_path.sql` adds `ix_masking_rule_role_field` on `masking_rule (role_code, field_id, masking_version)` and `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)`, so the two reads of an answer are index reads inside the 2 s budget of DP-11.
- The policy rows are versioned by `matrix_version`, `masking_version` and the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).

**Configuration and reference data**

- The matrix version and the masking version in force are data: the latest `valid_from` on or before the business date, read from `permission.matrix_version` and `masking_rule.masking_version`. The masking version of SIT is assumed to be MASK-SIT-01 (GAP-0936; ASM-1662).
- LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-CAPABILITY (the 14 capability areas) through the reference-data contract of DP-07 (RWB-P3-E1043-CON).
- No parameter row, no timeout constant and no role code in code: the 2 s is the platform standard of RWB-PLT-E1037-CON's client, and the cache lives for the policy version in force (BR7).
- The database login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0934; ASM-1660).

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the reference lists, with the matrix version named in the answer; tests for AC2, AC3 and AC6, and a test that a new scope value is accepted as data.
2. `EscalationScopeService` with the attributes of the timer, the grant and its end; tests for AC4 with the escalation open and closed.
3. `MaskingProfileService` with the covering-row lookup and the default; tests for AC1, AC5 and AC6.
4. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of X5; test TC-E2-015-08.
5. The denial path with the refusal shape and no case data; test TC-E2-015-11 and AC8.
6. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test AC9 against the PM-2026.13 fixture.
7. The migration of the two indexes, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size.
8. The contract-fake run of the whole capability against RWB-P3-E2015-CON and the decision-record fake, so the story builds before the case side exists in the environment.

**Feature switch.** `rwb.p4.escalation-scope`, read from the platform feature-flag library under the R-PREC default ruling. Off: the escalation grant of BR3 is not applied and the answer is the matrix-and-scope answer alone, while the masking profile and the access log are unchanged — so a case escalated to a role that does not hold it in scope stays refused, and nothing else in the service changes. The switch needs no schema rollback and blocks no case read that the policy allows.

**Done when.** The tests in section 16 pass; a case owned by the caller is answered granted with its fields marked, a case outside the scope is answered 404 with no case data, a case escalated to a role is answered granted to that role and refused again once the escalation closes, a field with no masking row comes back masked, a role without Case record R is refused with no case data, every granted and every refused read leaves its record, and an approved policy version changes the answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer (X6, X8) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR2 and on an ended grant (BR3) |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The sign-in refusal of a conflicting role pair, naming both role codes (PRD P4 FR-P4-005; FSD P4 AC-EXC-P4-001-03) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X5) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Your request is queued and will be retried. | This story, on a reference-list failure (X9) |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "read the timers"; for MSG-P4-003 no case fact is echoed, because the message must not confirm that a case exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10. Open decisions this story rests on, each still open: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL22 (assumptions ASM-1162, ASM-1304, ASM-2217, ASM-2569).

### 15. Screens and states

This story builds no screen. SCR-03 Case record, its clocks and deviation panels, its history and its route are RWB-P3-E2015-APP/CON through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the page SCR-04 for a case outside the scope is the case service's, and the refusal text it shows is the one this story produces.

What this story decides for SCR-03 and SCR-04 is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Read only, granted | The case, its timers and its deviation flag are rendered; the fields this story marks masked are rendered masked, and the screens hold no rule of their own |
| SCR-03 Case record | On hold for a deviation | The same grant applies; the on-hold banner and the deviation panel are P3's and S8's, and the personal fields stay masked |
| SCR-03 Case record | Escalated | The reader is the role the escalation names and sees the case although it is in neither queue nor own scope; the escalation line itself is P3's |
| SCR-03 Case record | Refused | The page shows MSG-P4-002 and no case fact, and one AC-DENY entry exists |
| SCR-03 Case record | Not found | The page shows MSG-P4-003 and no case fact, and one AC-DENY entry exists |
| SCR-03 Case record | Not available | The page shows MSG-P7-003 where the record could not be written, and no case fact |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-5235) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-5235) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-5235) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-5235) |
| SCR-04 | Empty | Not specified in the source documents (CG-ALL-5236) |
| SCR-04 | Loading | Not specified in the source documents (CG-ALL-5236) |
| SCR-04 | Error | Not specified in the source documents (CG-ALL-5236) |
| SCR-04 | No access | Not specified in the source documents (CG-ALL-5236) |

A screen that renders a field clear because a client cached it is a defect of the screen, not of the answer: the answer always names the masking version it used, and a field is clear only where a row of that version says so.

Every message named in this section is served from the message catalogue in Thai and in English. Its Thai wording and its approver are Not specified in the source documents (GAP-1831; DL10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-01 | AC1, AC6, BR1, BR5 | Component | Case RW-2026-000501 owned by RW-CASEOWN "U-7301", with the NOTICE_PERIOD timer of the legacy set; the same read by RW-AUDIT with scope ALL |
| TC-E2-015-02 | AC1, BR4 | Component | Case RW-2026-000502 with deviation X3 open and the personal fields of the case asked for |
| TC-E2-015-03 | AC5, BR4 | Component | No masking row covers DF-PTY-008; case RW-2026-000501 read by RW-CASEOWN |
| TC-E2-015-04 | AC4, BR3 | Component | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR at 2026-12-12 09:05 |
| TC-E2-015-05 | AC4, BR3 | Component | Two deviations on one case, then the escalation closed at the clear |
| TC-E2-015-06 | AC1, BR5 | Component | Paused service level and running prescription; the AC-READ entry names the field IDs |
| TC-E2-015-07 | AC1, BR2 | Component | Case RW-2026-000505 with its timer resumed, read by its owner |
| TC-E2-015-08 | X5, AC10, BR5, BR6 | NFR | The decision record write forced to fail during a granted read |
| TC-E2-015-16 | X6, AC11, BR1 | Functional | A token with no Recovery role is refused before the policy is read |
| TC-E2-015-17 | X7, AC12, BR8 | Functional | Two conflicting roles refuse the session at sign-in with no authorise request |
| TC-E2-015-18 | X8, AC13, BR1, BR8 | Functional | A service identity is checked under its own roles and refused 401 with no role |
| TC-E2-015-19 | X9, AC14, BR8 | Functional | A reference list that is not available gives 503 and no guessed answer |
| TC-E2-015-13 | AC15, BR8 | Functional | Role codes, scope values and masking rows are read as data and no constant is held |
| TC-E2-015-14 | AC16, BR9 | Functional | Case facts come from the request and no case table is read |
| TC-E2-015-09 | AC2, AC3, BR2 | Component | Case RW-2026-000507 in team SME-NTH opened by an OWN-scope owner of MTG-BKK, and the same case opened by a TEAM-scope manager of SME-NTH |
| TC-E2-015-10 | AC9, BR7 | Contract | Policy version PM-2026.13 approved and published; the cached answer dropped |
| TC-E2-015-11 | AC7, AC8, BR1, BR6 | Component | RW-REFADM (no Case record right) asks for `GET /cases/{caseId}/timers`; refused with MSG-P4-002 |
| TC-E2-015-12 | BR1, BR4 | Component | Boundary of the section 12.7 tables: a role with no CASE_RECORD row in `permission` for `PM-2026.12`, and a field with no covering `masking_rule` row for `MASK-SIT-01`; each refused or masked, none granted clear |
| TC-E2-015-15 | AC17, BR1 | Functional | A token that is not valid is answered 401 with MSG-P4-001 by POST authorise and GET /cases/{caseId}/timers |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the legacy level System maps to Component where the case-side assertion is stubbed by RWB-P3-E2015-CON and to End to end where the whole screen is exercised, and Access maps to Component. Every legacy test case of the key is listed above, with its Covers column rewritten to the criteria this story owns. No `-ITG` copy sits in this story: the integration copy of this key is RWB-ITG-E2015-ITG.

### 17. Guardrails

- No business value in code: role codes, scope values, capability areas, field IDs, the matrix version and the masking version are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR8).
- No personal data in logs, events, the record or the tests. The answer carries markers, the `AC-READ` entry carries field IDs, the `AC-DENY` entry carries the area and the right, and the event carries version labels; test data is synthetic and staff appear as user references.
- ACE customer fields only through the owner's contract and masked by role: this service stores no customer value and answers with markers, and the field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016 name fields of P1's contract without copying their values (NFR-039, NFR-040).
- No cross-schema read (DP-01): `recovery_case`, `timer`, `task`, `deviation`, `decision_log_entry` and the `v_ace_*` views are never queried; the case facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no case data and raises an incident, so no case read is unlogged (BR5, BR6).
- The answer is idempotent for a policy version: the same question under the same versions returns the same answer, and the cache is dropped on the policy event rather than on a timer.
- The feature switch changes one rule and no schema, and it never widens a scope: off removes the escalation grant and leaves every other decision as it was.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30 | TC-E2-015-04, TC-E2-015-05 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-01 to TC-E2-015-03, TC-E2-015-06, TC-E2-015-07, TC-E2-015-09, TC-E2-015-12 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03 | 11 Handle customer care and deviations | R-UNI-04, R-UNI-05 | TC-E2-015-02, TC-E2-015-05, TC-E2-015-06 |
| REQ-DRI-001 | Every decision writes one record holding the case and the decision, the versions, the approval, the actions and the outcome | Program, section 5.7; Epic 1 | FEAT-DRI-01 | All recovery processes | BR5, BR6 | TC-E2-015-01, TC-E2-015-06, TC-E2-015-08 |

| Legacy reference | Where it is kept |
|---|---|
| The five access decisions of section 10 (Own, Team, Team-plus-escalation, the specialist roles, All) | Sections 1, 7, 8, 10 |
| The refusal of a role with no Case record right and the not-in-scope answer | Sections 4, 5, 7, 14 |
| Masking of DF-PTY-007, DF-PTY-008 and DF-PTY-016, and the default masked | Sections 3, 4, 7, 8, 11 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Rules R-UNI-04, R-UNI-05, R-UNI-30, R-UNI-31 | Sections 8, 18 |
| Matrix version PM-2026.12, masking version MASK-SIT-01, roles RW-CASEOWN, RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL, RW-AUDIT, RW-REFADM | Background, AC1 to AC9, sections 3 and 10 |
| Legacy key RWB-E2-015, story RWB-P4-E2015-APP, contract RWB-P3-E2015-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The rwb-case slice of this legacy key, RWB-P3-E2015-APP and its contract RWB-P3-E2015-CON: the two read endpoints `GET /cases/{caseId}` and `GET /cases/{caseId}/timers`, the timers themselves, the prescription warning, the escalation fields and the deviation panel.
- RWB-P3-E1023-APP, the read-only case record view, and the SCR-03 layout, its panels and its states.
- RWB-S8-E2015-APP and the deviation handling: raising, approving, clearing and the contact stop of X1 to X7.
- The history timeline on the case (RWB-E2-016) and the next action panel (RWB-E2-035).
- RWB-ITG-E2015-ITG, the wave-2 integration harness copy of the tests of this key, which proves the real cross-service behaviour end to end.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP and RWB-P4-E2014-APP), the DoA-limits operation and `rwb.access.DoALimitChanged.v1`.
- Break-glass access, its incident reference, its ceiling and its review (the wave-1 stories of this service).
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other job, workflow and Schedule of this service.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
