# RWB-P4-E1028-APP Service levels, timers, escalation and prescription dates
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-U |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-E1028-APP-16); no size is in the source documents |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1028-CON |
| Contract fake library | Not specified in the source documents (DOR-RWB-P4-E1028-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-011, REQ-CWC-012, REQ-CWC-016) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-028 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner, a team manager, a litigation officer or an auditor who opens a case and its timers**, I want **the access service to answer, for the case in front of me, whether my role may read its timers and its prescription date, which scope admits it, and whether an escalation puts it in front of me**, so that **the deadline behind the service level timer and the prescription date reach the people entitled to see them in time, and nobody else is told that the case, the timer or the date exists**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E1-028:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers three questions behind the three operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`: does the caller hold Case record right R, does the scope in force admit this case, and does an open escalation put the case in front of the caller. The two case read endpoints `GET /cases/{caseId}/timers` and `GET /cases/{caseId}`, the timer rows, the service level clock, the working-day calculation, the warning, the breach and the prescription date stay in `rwb-case` (P3); this story builds no screen, starts no timer and runs no workflow.
- The facts the decision needs — the case ID, its queue, its team, its owner, and the `SERVICE_LEVEL` timer's type, status, escalation level, `escalated_to_role` and `escalated_at` — arrive in the authorise request. Which attributes an authorise request for a timer or a case read must carry is Not specified in the source documents (GAP-0986; ASM-1731).
- The policy the answers come from is data in `rwb_access`: the role list, the role-to-permission matrix version in force (`PM-2026.12` in the tests), the scope rule and its list, and the role conflict rows. Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP and is out of scope here.
- The access log is a decision-record entry on `rwb.decision-record.v1` written through the local library of DP-03: `AC-READ` for a granted read with the case ID and the timer or field identifiers asked about, `AC-DENY` for a refusal with the area and the right and no case fact (FEAT-ACA-07, FEAT-ACA-08).

The legacy behaviour carried into the access service is the part of RWB-E1-028 that decides who may look: the refusal of X9 and its test TC-E1-028-12, the reading of the timers and the prescription date by a role holding Case record R within its scope, and the escalation to the named point of AC2 read as an access grant — the role the breach is escalated to may open the case while the escalation is open, and the case keeps its queue and its owner (R-UNI-30).

### 2. Business rationale

A programme finding behind this legacy key is that deadlines live in personal diaries: CTL-18 records a prescription date missed because nobody entitled to see it saw it in time, and audit found litigation not filed for debtors who met the criteria. The case-side story fixes the clock; this story fixes who may see the clock. A service level that only a screen shows, and an escalation that only an e-mail announces, leaves the deadline invisible to the one role that has to act on the day it breaches (legacy section 2; AC2; X9).

Under Architecture v5 the access decision is a cached answer of `rwb-access` and every service authorises its own object against it, inside a 2 s timeout (slide 14; slide 43). This story is the answer for a timer read and for the prescription date on a case read: the matrix right, the scope rule, the escalation grant of R-UNI-30, the refusal of a role with no Case record right, and the record of each answer. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 on the access side and supports the measure "rule and limit changes made without a code release" at 100 percent, because the matrix, the scopes, the escalation roles and their versions are data.

The measure of success is that every read of a timer or of a prescription date is granted or refused by the policy in force, that an escalated case is readable by the role it was escalated to while the escalation is open and by nobody else once it closes, and that every granted read and every refusal leaves one record naming the case and the identifiers, or the area and the right and no case fact.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix and the role list as data (legacy RWB-E1-037). This story implements the decision behind those operations for a timer read and a case read; it adds no operation |
| RWB-P3-E1028-CON | The case and timer facts the authorise request is built from: the case, its queue, its team, its owner, its prescription date, and the `SERVICE_LEVEL` timer with its type, status, escalation level, `escalated_to_role` and `escalated_at`, as the P3 slice of this legacy key publishes them. Which of those attributes an authorise request carries is Not specified in the source documents (GAP-0986; ASM-1731) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-SCOPE with the version in force (DP-07); `lov_value` stays P3's and no scope string is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route behind the case screens (DP-19); the route itself is the case service's story |

Business preconditions carried from RWB-E1-028, owned by other services where they say so:

- The permission matrix version in force gives CASE_RECORD right R to RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-AUDIT and no CASE_RECORD right to RW-REFADM (FSD P4 A2.4; TSD P4 T6.1). The label of the version in force on the release date is Not specified in the source documents (GAP-0986; ASM-1732); the story names `PM-2026.12` in its tests, as the FSD examples do, and whatever `permission.matrix_version` holds in force in the environment otherwise.
- The `default_scope` of each role is data in `role.default_scope`, read against LOV-SCOPE (OWN, TEAM, REGION, ALL); the test fixture of 12.8 carries OWN for RW-CASEOWN, TEAM for RW-TEAMMGR, REGION for RW-LITOFF and ALL for RW-AUDIT, and no scope value is written in code (FSD P4 A2.14; TSD P4 T3.2).
- The `SERVICE_LEVEL` row for product group HIRE_PURCHASE and status ASSIGNED is 5 working days with warning percent 80 and escalation role RW-TEAMMGR (legacy section 3, DL22). It is P3's data behind RWB-P3-E1042-CON; this story reads neither the row nor its values, and the role and the limit arrive in the request as facts.
- The case record view SCR-03 and the exception queue SCR-09 exist (RWB-E1-035, RWB-E1-043 and the P3 slice of this key); the timer panel of Epic 2 is RWB-P4-E2015-APP's screen-side sibling.
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The service connects with the rwb-access login of DP-02, fixed by the platform DB story of this service.
- The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None).
- Open decisions apply: DL10 is still open (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL22 is still open (assumptions ASM-1162, ASM-1304, ASM-2217, ASM-2569). Closing the decisions is outside this story.

### 4. Flow

1. Caller: a person opens SCR-03 Case record or asks for the timers of a case. gateway-bff resolves the session and calls the case service; the case service builds the authorise request from the case and its `SERVICE_LEVEL` timer.
2. Caller: the request names the area `CASE_RECORD`, the right `R`, the case, the object asked about (`GET /cases/{caseId}/timers` for the timers, `GET /cases/{caseId}` for the prescription date), and the object attributes the policy reads — the queue, the team, the owner, and the timer's type, status, escalation level, escalated role and time. The full attribute set is Not specified in the source documents (GAP-0986; ASM-1731).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the rights from `permission` for the matrix version in force. `role`, `permission`, `matrix_version` and their versions are read from `rwb_access` only.
4. `rwb-access`, right check: no CASE_RECORD R for any role the caller holds gives a refusal, 403 with MSG-P4-002 naming the action ("read the timers"), and no case fact (BR1). The refusal is written as an `AC-DENY` entry (BR6).
5. `rwb-access`, scope check: the case is in scope when the attributes of the request satisfy the caller's `default_scope` in force, read from LOV-SCOPE through the reference-data contract of DP-07: OWN for a case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case (BR2). A case outside it is answered 404 with MSG-P4-003 and no case fact, so the answer never confirms that a case or a deadline exists (BR2).
6. `rwb-access`, escalation grant: while a `SERVICE_LEVEL` timer of the case is EXPIRED at escalation level 1 and escalated to a role the caller holds, the answer is granted with the reason `ESCALATED_TO_ROLE` although the case is in neither the caller's own nor the caller's queue scope (BR3). The grant is computed per request from the attributes; when the escalation closes, the next request is answered by the scope rule again (BR3).
7. `rwb-access`, masking: nothing is decided here. The masking profile is the answer of `GET /masking-policies` under RWB-P4-E1037-CON, this story reads no masking row for a timer read, and a grant never makes a field clear that a masking row does not (BR10).
8. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03, with the case ID and the timer or field identifiers asked about, and returns the answer to the caller inside the 2 s timeout of DP-11 (BR6).
9. `rwb-access`: caches the answer for the policy versions in force and the caller's role set. A caller that asks again under the same versions is answered from the cache and reads no matrix row twice; the `AC-READ` entry is still written for that read (BR7).
10. Policy change: a new matrix version (`PM-2026.12`) or a new role row is approved through the load path, `rwb-access` writes the rows and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`. The cached answer is dropped and the next call is answered under the new version, with no deployment (BR7).
11. Case service: renders SCR-03 with the timers and the prescription date on a grant, and the "not in your scope" page on a 404; the timer rows, the warning, the breach, the prescription calculation and the exception queue listing are its own (RWB-P3-E1028-APP/CON).

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of a deadline is ever unlogged (BR6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Case record R reads the timers (legacy X9) | Refused before any case fact is read: 403 with no case fact; one `AC-DENY` entry | MSG-P4-002 | AC4, TC-E1-028-12 |
| X2 | The case is outside the caller's scope and no escalation covers it | Not found: 404 with no case fact; one `AC-DENY` entry | MSG-P4-003 | AC5 |
| X3 | The escalation closes while the caller holds the case open | The grant ends: the next request is answered by the scope rule and refused 404 | MSG-P4-003 | AC3 |
| X4 | The `SERVICE_LEVEL` timer is RUNNING, PAUSED or STOPPED and carries no escalated role | No grant: the answer is the scope answer alone, with no reason code | MSG-P4-003 where the case is out of scope | AC3 |
| X5 | The decision record cannot be written | Nothing is returned: 503 with no case fact, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC7, TC-E1-028-09, TC-E1-028-13 |
| X6 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | AC9 |
| X7 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | AC10 |
| X8 | The caller is a service identity, not a person | The same checks run under the service identity's roles; an identity with no role is refused 401 | MSG-P4-001 | AC11 |
| X9 | The scope list is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | AC12 |

Where a role and an escalation both admit the case, the answer names the scope it used and the reason; which of the two scopes prevails is Not specified in the source documents (GAP-0986; ASM-1733), so until it is fixed the answer names the scope of the escalation grant, records the reason `ESCALATED_TO_ROLE`, and never reports a wider scope than the caller's role row carries.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P3-E1028-CON and the contract fake of the case and timer facts; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, scopes, matrix version and escalation roles — is data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | The escalation role and the entitled reader see the deadline; nobody else is told the case or the date exists; every read is logged |
| Estimable | Three answers behind existing operations, one grant rule, one cache, one decision-record path and one index |
| Small | Fits one sprint with its tests; no screen, no timer, no workflow and no Schedule |
| Testable | Every owned criterion has a test case in section 16; the case side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates, access side

  Background:
    Given the environment is SIT and this service answers on base path "/api/recovery/access/v1" from schema "rwb_access"
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-AUDIT, and no CASE_RECORD right to RW-REFADM
    Given the scope list in force is LOV-SCOPE with values "OWN", "TEAM", "REGION" and "ALL", held as "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR, "REGION" for RW-LITOFF and "ALL" for RW-AUDIT
    Given the rwb-case contract mock returns case "RW-2026-000401" in queue "LIT-BKK-OFF", owner "U-31" and team "LIT-BKK", with a "SERVICE_LEVEL" timer started 2026-12-01 09:00, expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00, not escalated
    Given the rwb-case contract mock returns the same case "RW-2026-000401" with the "SERVICE_LEVEL" timer EXPIRED at escalation level 1 and escalated to "RW-TEAMMGR" at 2026-12-09 09:05

  Scenario: AC1 The owner's timer read is granted in own scope (new, D-RCV-60)
    Given test user "U-31" holds RW-CASEOWN and owns case "RW-2026-000401"
    Given the rwb-case contract mock returns case "RW-2026-000401" in queue "LIT-BKK-OFF", owner "U-31" and team "LIT-BKK", with the "SERVICE_LEVEL" timer not escalated
    When the caller asks POST /api/recovery/access/v1/authorise for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the answer is granted with scope "OWN" under matrix version "PM-2026.12"
    Then the answer names the timer identifiers the request carried, DF-WRK-027 to DF-WRK-036 and DF-WRK-041, and no timer value
    Then one AC-READ decision record is written with the case ID "RW-2026-000401" and those identifiers

  Scenario: AC2 Team scope admits a case of the caller's team (new, D-RCV-60)
    Given test user "U-32" holds RW-TEAMMGR with default scope "TEAM" in team "LIT-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000401" in queue "LIT-BKK-OFF", owned by "U-31" in team "LIT-BKK"
    When "U-32" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}"
    Then the answer is granted with scope "TEAM"
    Then when a caller with default scope "TEAM" in team "NPA-BKK" asks for the same case
    Then the answer is refused with status 404 and message MSG-P4-003

  Scenario: AC3 An escalation grants the case to the escalated role and the grant ends (new, D-RCV-60)
    Given test user "U-32" holds RW-TEAMMGR with default scope "TEAM" in team "NPA-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000401" in queue "LIT-BKK-OFF" with the "SERVICE_LEVEL" timer EXPIRED at escalation level 1 and escalated to "RW-TEAMMGR" at 2026-12-09 09:05
    When "U-32" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the attributes carry timerType "SERVICE_LEVEL", status "EXPIRED", escalationLevel 1, escalatedToRole "RW-TEAMMGR" and escalatedAt 2026-12-09 09:05
    Then the answer is granted with the reason "ESCALATED_TO_ROLE"
    Then the answer leaves the case in queue "LIT-BKK-OFF" with owner "U-31" and moves no timer
    Then the grant widens no masking row and a masked field stays masked under it
    Then when the rwb-case contract mock returns the same case with the escalation closed and no escalated role
    Then the same request is refused with status 404 and message MSG-P4-003

  Scenario: AC4 A role without Case record R is refused the timer read (new, D-RCV-60)
    Given test user "U-33" holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    Given the rwb-case contract mock returns case "RW-2026-000401" with the "SERVICE_LEVEL" timer not escalated
    When "U-33" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" for the timer read GET /cases/{caseId}/timers
    Then the answer is refused with status 403 and message MSG-P4-002 with action "read the timers"
    Then no timer identifier, no prescription date and no case fact is returned

  Scenario: AC5 A case outside the scope is answered with no case fact (new, D-RCV-60)
    Given test user "U-31" holds RW-CASEOWN with default scope "OWN" and owns another case
    Given the rwb-case contract mock returns case "RW-2026-000401" in queue "LIT-BKK-OFF" owned by another user in team "LIT-BKK"
    When "U-31" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no case fact: no owner, no queue, no team, no timer identifier and no prescription date

  Scenario: AC6 A granted read and a refusal each leave their record (new, D-RCV-60)
    Given test user "U-31" holds RW-CASEOWN and owns case "RW-2026-000401"
    Given test user "U-33" holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When "U-31" is granted the timer read and "U-33" is refused it
    Then one AC-READ decision record is written with the case ID "RW-2026-000401" and the identifiers asked about
    Then one AC-DENY decision record is written with area "CASE_RECORD", right "R" and result "REFUSED"
    Then the AC-DENY record carries no case ID, no owner, no team, no queue and no timer identifier
    Then both records are committed before their answers are returned

  Scenario: AC7 A read that cannot be recorded returns nothing (new, D-RCV-60)
    Given test user "U-31" holds RW-CASEOWN and owns case "RW-2026-000401"
    Given the decision-record fake is set to fail every write in this run
    When "U-31" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the call returns status 503 and message MSG-P7-003
    Then no timer identifier, no prescription date and no case fact is shown
    Then an incident is raised to the platform administrator queue

  Scenario: AC8 A policy version change reaches the answer with no deployment (new, D-RCV-60)
    Given test user "U-34" holds RW-LEGAL, which has no CASE_RECORD right in "PM-2026.11"
    Given the rwb-case contract mock returns case "RW-2026-000401"
    When "U-34" asks for case "RW-2026-000401" and the answer is refused under matrix version "PM-2026.11"
    Then policy version "PM-2026.12" is approved and rwb.access.AccessPolicyChanged.v1 is published on rwb.access.events.v1
    Then the cached answer keyed by "PM-2026.11" is dropped
    Then the next ask by "U-34" is answered under matrix version "PM-2026.12" with no deployment
    Then each answer was returned inside the 2 s timeout and every granted read wrote its own AC-READ entry

  Scenario: AC9 A token with no Recovery role or no second factor is refused before the policy is read (new, D-RCV-60)
    Given a test user whose token carries no Recovery role or no second factor
    When the caller asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then no policy row is read and no case fact is returned
    Then one refusal entry is written with the reason

  Scenario: AC10 Two conflicting roles of the caller refuse the session at sign-in (new, D-RCV-60)
    Given a test user holds RW-SECADM together with a business role that a role_conflict row lists against RW-SECADM
    When the caller signs in to the Recovery Workbench
    Then the sign-in access check refuses the session with message MSG-P4-006
    Then no authorise request is made

  Scenario: AC11 A service identity with no role is refused as a person would be (new, D-RCV-60)
    Given a service identity with no role calls the access service
    When the identity asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the same checks run under the service identity's roles and no policy row is read

  Scenario: AC12 A scope list that is not available gives no guessed answer (new, D-RCV-60)
    Given test user "U-31" holds RW-CASEOWN and owns case "RW-2026-000401"
    Given the scope list LOV-SCOPE cannot be read in this run
    When "U-31" asks for case "RW-2026-000401", area "CASE_RECORD", right "R" and the object "GET /cases/{caseId}/timers"
    Then the answer is 503 with message MSG-GEN-006 and no scope is guessed
    Then the refusal is recorded

  Scenario: AC13 Roles and scopes come from data and never from code, and the escalation grant leaves masking, DoA and break-glass unchanged (new, D-RCV-60)
    Given a role or scope row changes in the policy data
    When the caller asks for a case read
    Then the answer follows the changed row with no deployment
    Then the escalation grant leaves masking, DoA and break-glass unchanged
```

AC1 to AC12 are the criteria this story owns. The case-side criteria AC1 to AC12 of the legacy key are owned by RWB-P3-E1028-APP and are proved against these answers. In AC1 the two assertions that belong to this service are the scope it names and the identifiers it records; the timer list and the dates are P3's. In AC2 the two callers prove that scope is read per role and per team, not per case. In AC3 the grant is computed from `escalationLevel`, `escalatedToRole` and `escalatedAt` and ends when the escalation closes, so a case that leaves an escalation does not leak to the former escalated role, and no case and no timer moves. In AC4 the legacy access case TC-E1-028-12 is proved twice: as the answer the caller gets and as the entry the audit reads. In AC5 the refusal never confirms that the case exists. In AC6 both record kinds are proved. In AC7 the record-before-answer rule is proved under failure. In AC8 the cached answer is proved to change on the policy event and to need no deployment.



### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force; a caller whose roles hold no Case record R is refused with MSG-P4-002 naming the action and no case fact | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; FEAT-ACA-04; legacy X9 |
| BR2 | A case is in scope when the object attributes the request carries satisfy the caller's `default_scope` in force: OWN, TEAM, REGION or ALL; a case outside it is answered 404 with MSG-P4-003 and no case fact | FSD P4 A2.14 VR-P4-014-1; LOV-SCOPE |
| BR3 | While a `SERVICE_LEVEL` timer of a case is EXPIRED at escalation level 1 and escalated to a role the caller holds, the caller is granted Case record R on that case with the reason `ESCALATED_TO_ROLE`, although the case is in neither the caller's own nor the queue scope; the grant ends when the escalation closes, is recomputed from the attributes on every request, and moves no case and no timer | Legacy AC2 and R-UNI-30; REQ-CWC-011; FSD P4 A2.14 |
| BR4 | The facts the decision needs — timer type, timer status, escalation level, `escalated_to_role`, `escalated_at`, the queue and the team — arrive in the request; this service stores no timer, no service level and no legal period and reads none of them | DP-01; ownership map (timer, recovery_case to P3); legacy section 11 |
| BR5 | A caller with no Workbench role, or with no second factor, is refused 401 with MSG-P4-001 before any policy row is read | FSD P4 A2.1; NFR-049 |
| BR6 | One `AC-READ` entry per granted read carries the case ID and the timer or field identifiers asked about; one `AC-DENY` entry per refusal carries the area `CASE_RECORD` and the right `R` and no case fact; the entry is written before the answer, and a failure answers 503 with MSG-P7-003 and shows nothing | FSD P4 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; FEAT-ACA-07; FEAT-ACA-08 |
| BR7 | An answer is cached for the matrix version in force and the caller's role set, and dropped when `AccessPolicyChanged` is published, so a policy change reaches the next call with no deployment | Architecture v5 slide 43; FSD P4 AC-P4-004-01; DP-11 |
| BR8 | Which roles may read the exception queue listing produced by MSG-P3-026 for a case with no service level or no legal period follows the same Case record R and scope rule; the listing and its rows are the case service's | Legacy AC4, AC5 and MSG-P3-026; FSD P4 A2.14 |
| BR9 | Role codes, scope values, capability areas, escalation roles and every version are data read from `rwb_access` and the reference lists; no business value is written in code, and a list the answer needs that is unavailable gives 503 rather than a guessed value | FSD P4 BR-P4-004, BR-P4-005; TSD P4 T3.2; principle 1 |
| BR10 | The escalation grant adds Case record R for that case and nothing else: it widens no masking row, no data product right, no DoA limit and no break-glass state | FSD P4 A2.5; NFR-039; NFR-040; legacy BR3 ("the case does not move") |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are the five-character field of TSD P4 T3.1, and the answer names the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; the scope names OWN, TEAM, REGION and ALL are list values, never Java constants.
- BR3 is the only exception to BR2 and it is narrow: it needs an `EXPIRED` `SERVICE_LEVEL` timer at escalation level 1 and an escalated role the caller holds. Which scope prevails when the caller's own scope and the grant both admit the case, and what the answer names then, are Not specified in the source documents (GAP-0986; ASM-1733); the answer names the scope of the grant and records the reason.
- BR4 is why there is no repository for a case or a timer: the request is the only carrier of a case fact, and a test asserts that no statement of this story names `recovery_case`, `timer`, `queue`, `task`, `deviation` or the `reference_row` of a legal period.
- BR5 is the access check before this story's answer: a token with no role or no second factor never reaches the policy.
- BR6 is one `RecordAndApply` transaction per answer: the record is written first, the answer is returned after it commits, and a failure answers 503 and changes nothing (X5).
- BR7 is a cache keyed by the matrix version label and the caller's role set; the `AccessPolicyChanged` row is written in the same transaction that writes the new policy rows.
- BR8 is the same decision for the listing as for the case: the listing carries case IDs only for the cases the caller's right and scope admit, and the case service renders the list.
- BR9 is visible in the code review: no role code, scope name, capability area, escalation role or version string appears in a constant.
- BR10 is the boundary of the grant: `masking_rule`, `delegation_limit` and the break-glass state are untouched, and a test asserts a masked field stays masked under the grant.

### 9. State transitions

None for a case, a timer or an escalation. This story changes no case status, no timer status, no escalation level and no `escalated_at`; it reads none of them from a table. The timer itself is a durable timer inside the workflow that owns the case (Temporal and Drools design; Architecture v5 slides 42 and 44), JOB-05 is retired, and this service runs no workflow and owns no Schedule.

The only states this story has are the states of its answer:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted, by scope | The caller holds Case record R and the case satisfies the `default_scope` in force | The granted answer with the scope it used and the identifiers asked about | `AC-READ` |
| Granted, by escalation | The caller holds Case record R and a `SERVICE_LEVEL` timer of the case is EXPIRED at level 1 escalated to a role the caller holds | The granted answer with the reason `ESCALATED_TO_ROLE` and the identifiers asked about | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R, or the token carries no Recovery role | 403 MSG-P4-002 naming the action, or 401 MSG-P4-001, with no case fact | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope and outside an open escalation | 404 MSG-P4-003, no case fact | `AC-DENY` |
| Not answered | The record cannot be written, or the scope list cannot be read | 503 with MSG-P7-003 or MSG-GEN-006, no case fact | None; the failure is raised as an incident |

The escalation grant of BR3 has no stored state: it exists while the `SERVICE_LEVEL` timer of P3 carries `EXPIRED`, escalation level 1 and the escalated role and time, and it is recomputed on every request, so closing the escalation closes the grant with no call between the services and no row written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record R with default scope OWN: reads the timers and the prescription date of a case it owns |
| RW-TEAMMGR, team manager | Case record R with default scope TEAM: reads a case of its team, and — as the escalation point named by the `SERVICE_LEVEL` row — a case escalated to RW-TEAMMGR while the escalation is open |
| RW-LITOFF, litigation officer | Case record R within the scope its role row carries: reads the timers, including the prescription timer, of a case in that scope |
| RW-LEGAL, legal counsel | Reads the prescription date and the timers within its scope through the same decision; the legal periods themselves are its data through RWB-P3-E1043-CON, not a right of this story |
| RW-AUDIT, internal audit | Case record R with default scope ALL: reads any case, its timers and its prescription date; every read is recorded |
| RW-COMPLY, Compliance and PDPA officer | Reads which matrix version and which masking version are in force through `GET /masking-policies`; this story writes no value on their behalf and its grant widens no masking row |
| RW-REFADM and every role with no Case record R | Refused with MSG-P4-002 on the timer read and the case read; no case fact is returned (legacy X9, TC-E1-028-12) |
| RW-PLATADM, platform administrator | Holds no Case record right by its role row; it operates the service and the queue of incidents, not a case |
| SY-CASEWF and the other service identities | Ask the same question for their own service; a service identity with no role is refused 401, and a service identity's roles are checked as a person's are |

Reading is the whole of this story: it grants or refuses a read and writes the record of it. No DoA level applies to a timer read or to a case read — the delegation table and its lookup are RWB-P4-E2013-APP's and are never consulted here — and no policy row changes except through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP. A break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service.

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Not read by this answer; owned here, and no row changes (BR10) |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X7) |
| DF-REF-027 to DF-REF-033 | `lov_value` | the LOV-SCOPE values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The timer facts a request carries appear in it as identifiers and values of P3's own fields: `DF-WRK-027` to `DF-WRK-036` and `DF-WRK-041` name the timer type, status, start, expiry, warning point, paused state, escalation level and warned time, and they are carried only as `timerType`, `status`, `escalationLevel`, `escalatedToRole` and `escalatedAt`. They are not columns of `rwb_access` and no row of them is written or read here.

`recovery_case`, `timer`, `queue`, `task`, `deviation` and the `reference_row` of a legal period are P3's (and `deviation` is S8's) and are never named by a statement of this story: no foreign key, no view and no query crosses a schema (DP-01). The case ID, the queue, the team, the owner and the prescription date enter only in the request, and which attributes the request must carry is Not specified in the source documents (GAP-0986; ASM-1731).

No personal data enters `rwb_access`, the answer, the record or the event: the `AC-READ` entry carries a case ID and field or timer identifiers, the `AC-DENY` entry carries the area and the right, and neither carries a party value (NFR-039, NFR-040).

### 12. Contract

The contract version this story builds against is `/v1` of RWB-P4-E1037-CON, base `/api/recovery/access/v1`.

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The right, the scope and the escalation grant for one area, right and case read — a timer read on `/cases/{caseId}/timers` or a case read on `/cases/{caseId}` — with the identifiers asked about. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the matrix version and the default scope of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | Unchanged by this story: the masking version in force and the fields it covers for the caller's roles are read there, and this story reads no masking row and widens none |

`GET /doa-limits` is the same service's operation and is not used here: the delegation table and its routing lookup are RWB-P4-E2013-APP's, and no DoA level applies to a timer read.

#### 12.2 REST operations consumed

None. The case and timer facts arrive in the authorise request, built by the caller from its own rows; this story calls no service at run time. The shape it expects is the one RWB-P3-E1028-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, roles), the version label, the valid-from date and the change reference |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value and neither carries a timer value: the `AC-READ` record carries a case ID and identifiers, the `AC-DENY` record carries the area and the right, and the policy event carries version labels. `rwb.access.DoALimitChanged.v1` belongs to the delegation slice and is not published here.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh).

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. The timer it reasons about is a durable timer inside the workflow that owns the case — the `SERVICE_LEVEL` clock of CaseWorkflow — and the escalation level and escalated role are written there (Temporal and Drools design, parent and children and the four steps receive, ask, record and apply, wait; Architecture v5 slides 42 and 44).

#### 12.6 Schedules

None. This service owns one Schedule, the six-monthly access review list (JOB-18), and its story is RWB-P4-AD008-APP. JOB-05, the five-minute timer check of the legacy key, is retired: the service level clock is a durable timer inside the case workflow (Architecture v5 slide 44). This story starts no Schedule and reads no `timer` row.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles, their `default_scope` and `entra_group` |
| `permission` | P4 (`rwb_access`) | The CASE_RECORD right and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | Not read here; the table exists and no row changes (BR10) |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE, read through the contract; not owned here and, for the legal period, not read here |
| `delegation_limit` | P4 (`rwb_access`) | Not read in this story; it is the delegation slice's |

No table of `rwb_case`, `rwb_source_data`, `rwb_deviation` or `rwb_decision` is read: the case, the timer, the queue, the legal period and the deviation stay with their owners, and the only facts of them that enter this service are identifiers and attribute values carried by a request (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case case and timer WireMock | RWB-P3-E1028-CON | Case "RW-2026-000401" in queue LIT-BKK-OFF, owner "U-31", team "LIT-BKK", prescription date 2028-03-15, with a `SERVICE_LEVEL` timer started 2026-12-01 09:00, expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00, not escalated; the same case with the timer EXPIRED at escalation level 1 escalated to RW-TEAMMGR at 2026-12-09 09:05; the same case with the escalation closed for AC3; a case in queue NPA-BKK-CO with no service level and no `SERVICE_LEVEL` timer for TC-E1-028-04; an SSME case with no legal period and an empty prescription date for TC-E1-028-05 |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of AC7 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.12, the roles RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-AUDIT and RW-REFADM with their CASE_RECORD rights and default scopes (OWN, TEAM, REGION, ALL, none), the earlier PM-2026.11 for AC8, and the LOV-SCOPE list |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE with the version in force, and the unavailable list of X9 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the case and timer facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output, and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/timer-read`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

What each row means for this slice. DP-01 is the reason the service answers from the attributes it is given: `recovery_case`, `timer`, `queue`, `task` and the `reference_row` of a legal period are P3's, so the answer is built from identifiers and never from a joined query, and the service holds no timer, no service level and no legal period. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so the question "who saw this deadline" and the decision question are answered from one log. DP-05 adds nothing here: this story reads no ACE view and no ACCOUNT date — the last payment date and the holiday calendar belong to P1 through the case side (legacy BR4 and BR8). DP-06 and DP-07 supply the lists the decision needs and nothing more: `lov_value` stays with P3 and is read through the contract, and the service levels and legal periods are P3's data read by the case side, not here. DP-09 is one outbox row and one inbox row: the policy change event and the decision record, written in the transaction they belong to. DP-10 is recorded because the legacy key carries JOB-05: in the target the durable timer replaces JOB-05 inside the case workflow and this service runs no job. DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it. DP-13, DP-14 and DP-15 are the naming and migration conventions of the service. DP-19 is the route that renders the answer: the screen is the case service's and this story supplies only the grant and the refusal.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessContractController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| ObjectReadDecisionService | Service | Right, scope and escalation grant for one case read or timer read, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters |
| ScopeRule | Service | Compares the attributes of the request with the `default_scope` value in force |
| EscalationGrantService | Service | The grant of BR3 from the timer type, status, escalation level, escalated role and time; no stored state |
| RequestFactReader | Service | Reads the case and timer facts from the request only; holds no repository for a case or a timer |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyVersionCache | Service | The cached answer per matrix version and role set, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new policy version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V1028_1__case_read_index.sql` adds `ix_role_code_scope` on `role (role_code, default_scope)`, so the two reads of an answer — the right for the caller's roles and the scope of those roles — are index reads inside the 2 s budget of DP-11. No timer, case or period column is added anywhere.
- The policy rows are versioned by `matrix_version` and by the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).

**Configuration and reference data**

- The matrix version in force is data: the latest `permission.matrix_version` whose rows are valid on the business date. Its label on the release date is Not specified in the source documents (GAP-0986; ASM-1732); the tests use `PM-2026.12` and the earlier `PM-2026.11` for AC8, and the answer always names the version it read.
- LOV-SCOPE (OWN, TEAM, REGION, ALL) through the reference-data contract of DP-07 (RWB-P3-E1043-CON); no scope name is a constant.
- The service level values, the escalation role per product group and status, and the legal periods are P3's data through RWB-P3-E1042-CON and RWB-P3-E1043-CON; this story reads none of them and carries their values only as request attributes.
- No parameter row, no timeout constant and no role code in code: the 2 s is the platform standard of RWB-P4-E1037-CON's client, and the cache lives for the version in force (BR7).

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the LOV-SCOPE list, with the matrix version named in the answer; tests for AC1, AC2 and AC5, and a test that a new scope value is accepted as data.
2. `RequestFactReader` with the case and timer attributes of the request and a boundary test that no statement names `recovery_case`, `timer`, `queue`, `task`, `deviation` or a legal-period `reference_row` (BR4).
3. `EscalationGrantService` with the `EXPIRED` level-1 attributes, the reason code and the end of the grant; tests for AC3 with the escalation open and closed.
4. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of AC7; tests TC-E1-028-09 and TC-E1-028-13.
5. The refusal paths with the refusal shape and no case fact: 403 for a role with no right, 401 for no role, 404 for out of scope; tests TC-E1-028-12, AC4 and AC5.
6. `PolicyVersionCache` and `PolicyChangeListener` with the publish and the drop; test AC8 against the PM-2026.11 to PM-2026.12 fixture.
7. The migration of `ix_role_code_scope`, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size.
8. The contract-fake run of the whole capability against RWB-P3-E1028-CON and the decision-record fake, so the story builds before the case side exists in the environment.

**Feature switch.** `rwb.p4.escalation-scope`, read from the platform feature-flag library under the R-PREC default ruling. Off: the escalation grant of BR3 is not applied and the answer is the matrix-and-scope answer alone, while the record and the refusal behaviour are unchanged — so a case escalated to a role that does not hold it in scope stays refused, and nothing else in the service changes. The switch is the same flag the wave-2 sibling of another key uses, so the grant has one switch; it changes one rule, needs no schema rollback and never widens a scope.

**Done when.** The tests in section 16 pass; a case owned by the caller is answered granted with the timer identifiers recorded, a case of the caller's team is granted on team scope, a case outside the scope is answered 404 with no case fact, a case escalated to a role is granted to that role and refused again once the escalation closes, a role without Case record R is refused with MSG-P4-002 and no case fact, every granted read and every refusal leaves its record before the answer, a record failure answers 503 and shows nothing, and an approved policy version changes the answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer (X6, X8) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 (X1, AC4) |
| MSG-P4-003 | The case is outside the caller's scope and no escalation covers it | This case is not in your scope. | This story, on the refusal of BR2 and on an ended grant (BR3; X2, X3, AC5) |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X7) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X5, AC7) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Your request is queued and will be retried. | This story, on a scope-list failure (X9) |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "read the timers"; for MSG-P4-003 no case fact and no date is echoed, because the message must not confirm that a case or a deadline exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10.

### 15. Screens and states

This story builds no screen. SCR-03 Case record, its read-only state, its on-hold state and its prescription date are the case service's through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), and SCR-09 Exception queue, the listing produced from MSG-P3-026, is the case service's through the same route. The page a reader sees for a case outside the scope is the case service's; the text on it is the one this story produces.

What this story decides for those screens is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Read only, granted by scope | The timers and the prescription date are rendered for a caller whose right and scope admit the case, and the screen holds no rule of its own |
| SCR-03 Case record | On hold for a deviation | The same grant applies; the on-hold banner is P3's and S8's, the prescription date stays visible, and the stage clock is P3's |
| SCR-03 Case record | Escalated | The reader holding the escalated role sees the case although it is in neither its own nor its queue scope, and the reason code `ESCALATED_TO_ROLE` is what lets the case service render the escalation line |
| SCR-03 Case record | Refused | The page shows MSG-P4-002 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not found | The page shows MSG-P4-003 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not available | The page shows MSG-P7-003 where the record could not be written, and no case fact |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-4984) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-4984) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-4984) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-4984) |
| SCR-09 Exception queue | Listing | The cases listed for a caller are the ones its right and scope admit, on the same decision as a case read; the list and its rows are P3's and the row a reader may not see is never sent |
| SCR-09 Exception queue | Row opened | Opening a row is a case read and is answered again by this story; the listing is not a standing grant |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-4985) |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-4985) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-4985) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-4985) |

A screen that shows a timer because a client cached a grant is a defect of the screen, not of the answer: the answer names the matrix version it used and the scope or the reason it applied, and the case service asks again on every open.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-028-12 | AC4, AC6, BR1, BR6 | Component | RW-REFADM asks for the timers of case RW-2026-000401 and is refused with 403 MSG-P4-002 for action "read the timers"; one `AC-DENY` entry with area CASE_RECORD and right R and no case fact |
| TC-E1-028-01 | AC1, BR4 | Component | Owned by RWB-P3-E1028-APP: the `SERVICE_LEVEL` timer starts with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00 for the case placed in LIT-BKK-OFF at 2026-12-01 09:00; the access slice reads the same fixtures as the contract fake |
| TC-E1-028-02 | AC2 | Component | `SERVICE_LEVEL` timer EXPIRED at escalation level 1 escalated to RW-TEAMMGR at 2026-12-09 09:05; the grant to RW-TEAMMGR and its end when the escalation closes; the case keeps queue LIT-BKK-OFF and owner U-31 |
| TC-E1-028-03 | AC3 | Component | Owned by RWB-P3-E1028-APP: prescription date 2028-03-15 from the last payment date 2026-03-15 and the legal period; the access slice gates the `GET /cases/{caseId}` read that shows it |
| TC-E1-028-04 | AC4 | Component | Case in queue NPA-BKK-CO with no service level listed on the exception queue; a TEAM-scope manager of its team reads it and a manager of another team is refused 404 with no case fact |
| TC-E1-028-05 | AC5, AC1, BR8 | Component | Owned partly by RWB-P3-E1028-APP: SSME case with no legal period and an empty prescription date; the access slice grants the read in scope and refuses 404 outside it |
| TC-E1-028-06 | AC6 | Component | Owned by RWB-P3-E1028-APP: no last payment date, contract date 2025-06-30; the access slice reads the resulting date only as a request attribute |
| TC-E1-028-07 | AC7 | Component | Owned by RWB-P3-E1028-APP: JOB-05 stopped for 40 minutes and the missed runs caught up; retired in the target, where the durable timer inside the case workflow carries the wait and the access slice reads the resulting attributes |
| TC-E1-028-08 | AC8 | Component | Owned by RWB-P3-E1028-APP: the timer already EXPIRED and no second breach; the access slice reads the same `EXPIRED` level-1 attributes for AC3 |
| TC-E1-028-09 | AC7, BR6 | Component | Decision-record write forced to fail during a granted timer read; 503 MSG-P7-003 and no case fact |
| TC-E1-028-10 | AC1, BR2 | Component | Owned by RWB-P3-E1028-APP: deviation from 2026-12-02 to 2026-12-04; the access slice grants the same case read during the deviation |
| TC-E1-028-11 | AC1, BR2 | Component | Owned by RWB-P3-E1028-APP: 5 working days from Monday 2026-12-14 with the holiday calendar; the access slice never computes a date |
| TC-E1-028-13 | AC7, AC6, BR6 | NFR | Decision-record store unavailable for every read in a run; nothing is returned, no case fact is shown, and the incident is raised |
| TC-E1-028-14 | AC1, BR4 | Component | Owned by RWB-P3-E1028-APP: a class outside `recovery.casewf.timers` writes the timer table and the boundary test fails; here the boundary test reads the other way and no statement of this story names `timer` |
| TC-E1-028-15 | AC8, BR7 | Component | Policy change: a new matrix version (label Not specified in the source documents (GAP-0986)) or a new role row loaded through the load path; `rwb.access.AccessPolicyChanged.v1` published on `rwb.access.events.v1`; the cached answer dropped and the next call answered under the new version with no deployment; policy-pack fixture of build step 6 |
| TC-E1-028-16 | §12 operations and events | Contract | Each operation and event of section 12 checked against RWB-P4-E1037-CON: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on `/api/recovery/access/v1`; `rwb.access.AccessPolicyChanged.v1` and `rwb.decision.DecisionRecorded.v1` on their topics; no Temporal activity registered |
| TC-E1-028-17 | §12.7 tables | Component | Boundary of the tables of section 12.7: `role`, `permission` and `role_conflict` read in `rwb_access`; `masking_rule` and `delegation_limit` not read or changed; no table of `rwb_case`, `rwb_source_data`, `rwb_deviation` or `rwb_decision` read; the boundary test fails on any other read |
| TC-E1-028-18 | AC9, BR5 | Component | A token with no Recovery role and a token with no second factor are each refused 401 MSG-P4-001 before any policy row is read; one refusal entry is written |
| TC-E1-028-19 | AC10 | Component | RW-SECADM held with a business role that a `role_conflict` row lists against it; the sign-in access check refuses the session with MSG-P4-006 and no authorise request is made |
| TC-E1-028-20 | AC11, BR5 | Component | Service identity with no role calls the access service; refused 401 MSG-P4-001 under the identity's roles and no policy row is read |
| TC-E1-028-21 | AC12, BR9 | Component | LOV-SCOPE unavailable for a read of case RW-2026-000401 by U-31; 503 MSG-GEN-006, no scope guessed, refusal recorded |
| TC-E1-028-22 | AC3, BR10 | Component | Escalation grant on a case whose `masking_rule` row masks a field; the field stays masked under the grant and no `masking_rule` row changes |
| TC-E1-028-23 | AC13, BR7, BR9, BR10 | Component | Role or scope row changed in the policy data; the next read answers under the changed row with no deployment; escalation grant leaves masking, DoA and break-glass unchanged |

The mapping is by the criteria this story owns. TC-E1-028-12 answers the refused timer read, which is the legacy access case and the reason the key is split; TC-E1-028-02 answers the escalation grant and its end; TC-E1-028-09 and TC-E1-028-13 answer the record failure, once as a component case and once as a resilience requirement; TC-E1-028-04 and TC-E1-028-05 answer the visibility of the exception-queue case, one for a case with no service level and one for a case with no legal period. The remaining rows keep their legacy IDs and are owned by RWB-P3-E1028-APP, and their case-side assertion is the one the case story builds; the row is listed here so the key stays whole and the access assertion it touches is named. The level column maps the legacy levels: Access and System to Component, Resilience to NFR, Build to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. No `-ITG` copy sits in this story: the integration copy of this key is RWB-ITG-E1028-ITG. AC8 has no legacy test case of its own, because a matrix version change is proved by the load-path tests of RWB-E1-037; it is proved here by the policy-pack fixture of build step 6.

### 17. Guardrails

- No business value in code: role codes, scope values, capability areas, the escalation role and the matrix version are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR9).
- No personal data in logs, events, records or tests: the answer carries identifiers and scope, the `AC-READ` entry carries a case ID and field or timer identifiers, the `AC-DENY` entry carries the area and the right, and test data is synthetic and staff appear as user references (NFR-039, NFR-040).
- No cross-schema read (DP-01): `recovery_case`, `timer`, `queue`, `task`, `deviation` and the legal-period `reference_row` are never queried; the case facts arrive in the request and the policy is the service's own.
- The escalation grant never widens a masking row: it adds Case record R for one case and nothing else, so a field masked for the escalated role stays masked and the `masking_rule` table is not read or written here (BR10).
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no case fact and raises an incident, so no read of a deadline is unlogged (BR6).
- Default deny: a caller with no role is refused before the policy is read, and a case that satisfies neither the scope nor an open escalation is answered 404 rather than 403, so no case fact leaks through an error (BR2, BR5).
- The feature switch changes one rule and no schema, and it never widens a scope: off removes the escalation grant and leaves every other decision as it was.
- No timer in this service: no job, no Schedule, no durable timer and no clock is created, started, paused or expired here (DP-10; BR4).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-11, FEAT-CWC-13 | All recovery processes | R-UNI-30 | TC-E1-028-01, TC-E1-028-02, TC-E1-028-04, TC-E1-045-02, TC-E1-045-03, TC-E1-045-07, TC-TE-007-01, TC-TE-007-02, TC-TE-007-03 |
| REQ-CWC-012 | Prescription date from the legal periods at creation | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-12 | 08 Litigate and enforce | R-DEV-01, R-UNI-20 | TC-E1-028-03, TC-E1-028-05, TC-E1-028-06 |
| REQ-CWC-016 | Every timer event logged with rule and version | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-13 | All recovery processes | R-UNI-39 | TC-E1-028-09, TC-E1-028-13, TC-E1-028-12 |

These three requirements are met on the access side: the escalation role can open the escalated case while the escalation is open and the case does not move (REQ-CWC-011), the prescription date is shown only to a role whose right and scope admit the case (REQ-CWC-012), and every granted read and every refusal of a timer or a date leaves one record naming the case and the identifiers or the area and the right (REQ-CWC-016).

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1028-CON | CON | Contract dependency: publishes the case and timer facts the authorise request is built from, with the `SERVICE_LEVEL` status, escalation level, `escalated_to_role` and `escalated_at`; used as a fake here |
| RWB-P3-E1028-APP | APP | The case slice of this legacy key: the timers, the working-day calculator, the service level clock, the warning, the breach, `TimerBreached`, the prescription calculation and the exception queue listing; this story gates its reads and owns none of it |
| RWB-P4-E1037-CON | CON | The service contract this story builds behind: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on `/api/recovery/access/v1`, with the role and permission rows as data |
| RWB-PLT-E1037-CON | CON | The platform authorise contract and the guard library every caller uses, trusted as a wave-1 precondition (DP-08 at service level) |
| RWB-P4-E1023-APP | APP | The read-only case record view of this service's lane (legacy RWB-E1-023); the case read path it opens is answered by the same decision, and its screen is the case service's |
| RWB-P4-E2015-APP | APP | The wave-2 sibling of another key (RWB-E2-015): the timer panel, the escalation line and the deviation flag on the case record view. It reuses the grant of BR3 behind the same three operations for its own key and adds the masking markers this story does not decide; neither story duplicates the other's criteria, and the switch of this story serves both |
| RWB-ITG-E1028-ITG | ITG | The integration harness copy of the tests of this key; it proves the real cross-service behaviour end to end with the live case contract, which this story stubs |

| Legacy reference | Where it is kept |
|---|---|
| The refusal of X9 and its access test TC-E1-028-12 | Sections 1, 4, 5, 7, 10, 14, 16 |
| The escalation to the named point of AC2, read as an access grant, and rule R-UNI-30 | Sections 1, 4, 7, 8, 10, 18 |
| The case, queue, owner and team of the legacy examples (RW-2026-000401, LIT-BKK-OFF, U-31, LIT-BKK) | Background, AC1 to AC5, sections 3 and 12.8 |
| The SERVICE_LEVEL row for HIRE_PURCHASE and ASSIGNED, 5 working days, warning percent 80, escalation role RW-TEAMMGR | Background, sections 3, 8 and 10 (as P3's data, carried as request attributes) |
| The exception queue and MSG-P3-026 for a case with no service level or no legal period | Sections 8, 12.8, 15, 16 |
| JOB-05, the five-minute timer check, and its retirement | Sections 3, 8, 12.6, 13, 19 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Legacy key RWB-E1-028, story RWB-P4-E1028-APP, contract RWB-P3-E1028-CON | Metadata, sections 3 and 12 |

### 19. Out of scope

- The rwb-case slice of this legacy key, RWB-P3-E1028-APP and its contract RWB-P3-E1028-CON: the two read endpoints `GET /cases/{caseId}/timers` and `GET /cases/{caseId}`, the timer rows, the service level clock, the warning, the breach, `TimerBreached`, the prescription calculation and the exception queue listing.
- JOB-05 and the Quartz timer check, which the durable timer inside the workflow that owns the case retires; and every other job of the key.
- The working-day calculator and the holiday calendar, and the last payment date it needs, which are P3's and P1's through the case side.
- The prescription calculation from the legal periods, the parameter and reference rows behind it, and the legal period data owned by Legal through RWB-P3-E1043-CON.
- The decision log entry of a breach and of a warning, which are the case side's writes, and the central ledger sealing in rwb-decision.
- RWB-P4-E2015-APP and the Epic 2 timer panel, escalation line and deviation flag on the case record view; that wave-2 sibling of another key has its own criteria and this story adds none of them.
- RWB-P4-E1023-APP and the case record view's layout, panels, history and states.
- RWB-ITG-E1028-ITG, the integration harness copy of the tests of this key, which proves the real cross-service behaviour end to end.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table, its lookup and the DoA-limits operation (RWB-P4-E2013-APP and RWB-P4-E2014-APP), and `rwb.access.DoALimitChanged.v1`; no DoA level applies to a timer read.
- Break-glass access, its incident reference, its ceiling and its review (the wave-1 stories of this service).
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other workflow and Schedule of this service.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (the OPS story of this legacy key).
