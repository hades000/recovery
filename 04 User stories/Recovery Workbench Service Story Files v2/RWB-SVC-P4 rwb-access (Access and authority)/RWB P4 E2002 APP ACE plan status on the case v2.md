# RWB-P4-E2002-APP ACE plan status on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-AD |
| Size | Set by the squad at refinement |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2002-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E2002-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DRI-013, REQ-CHO-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 30 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a restructuring officer (RW-RESTRUCT) and an internal auditor (RW-AUDIT) who open the case record and the plan status of a case**, I want **the access service to answer, in one hop, which roles I hold, which Case record letters are in force, which scope admits this case and which matrix version the answer came from, and to record the decision for the plan-status read as one access entry naming the case ID and the field IDs only**, so that **the plan-status panel of a case is shown to the roles the matrix admits and to nobody else, a role without the right and a case outside the scope are refused with one message each, and no plan reference, no plan status and no personal value is ever copied into the access log**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E2-002:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers behind the two operations the service already publishes on RWB-P4-E1037-CON: the resolved permission view of `GET /api/recovery/access/v1/me/permissions` — the caller's roles, the CASE_RECORD letters in force, the scope (OWN, TEAM, REGION or ALL) and the matrix version — so the case record and the plan-status panel learn from one answer whether the caller may read the case at all; and the authorise decision of `POST /api/recovery/access/v1/authorise` for the plan-status read, with the scope test on the case attributes carried in the request.
- The case attributes the decision needs — the case ID, its owner, its queue and its team — and the plan reference `TDR-SYN-0310` arrive in the authorise request, built by the caller from its own rows. This story reads no `rwb_case` table, calls no rwb-case operation at run time and reads no `v_ace_*` view (DP-01, DP-05); the shape of the request and of the answer is Not specified in the source documents (GAP-0908; ASM-1628).
- The policy the answer comes from is data in `rwb_access`: the role list, the role-to-permission matrix version in force (`PM-2026.12`) and the scope rule (`OWN`, `TEAM`, `REGION`, `ALL`). Loading and approving a matrix version is the load path of RWB-P4-AD002-APP and is out of scope here.
- The access log is a decision-record entry written through the local library of DP-03 (`AC-READ` for a granted read, `AC-DENY` for a refusal) and relayed on `rwb.decision-record.v1`; the entry carries the case ID, the area, the right and the field IDs `DF-CAS-046`, `DF-CAS-047` and `DF-CAS-048`, never the plan reference, never the plan status and never a personal value.
- The masking question is answered by saying there is none to answer: the plan-status panel shows the plan reference, the status and the status date only, none of the three is a personal field, and no `masking_rule` row applies (FSD P4 A2.5; TSD P4 T3.1).

The legacy behaviour carried into the access service is unchanged: a case owner and a restructuring officer read the plan status of a case in their scope, the auditor reads with scope ALL, a case outside the caller's scope is answered as not found, and a role that does not hold Case record R is refused. Legacy AC8 (a case outside the scope is answered 404 with MSG-P4-003) and legacy TC-E2-002-10 (a role without the Case record right is refused with MSG-P4-002) are answered here; the rest of the legacy key is carried by the other slices.

### 2. Business rationale

A restructure plan is calculated and held in ACE, and the plan status on the case is what tells a recovery officer whether the customer is paying a plan, whether the plan broke and whether litigation may start. The read itself is rwb-integration's and the stored status, the compare and the rules are rwb-case's; what is missing in the legacy story is the control around the read. The legacy story names the roles in its authority table, records one refusal of a role without the right in its exception path X7 and one out-of-scope refusal in X6, and leaves the role model, the scope and the access log where they always were: in the access module. Under Architecture v5 the access decision is a cached answer of `rwb-access`, and every service authorises its own object against it, one hop, 2 s (slide 10; slide 14). rwb-access owns Recovery roles as data, scope, the masking policy, the DoA table and the access log (slide 41).

This story is the rwb-access part of legacy RWB-E2-002: the right and the scope that let the plan-status read happen, not the plan read. The plan read, `RestructurePlanQuery`, the 2-second timeout, the `plan_ref`, `plan_status` and `plan_status_as_of` columns and the stored fallback are rwb-integration's and rwb-case's; the RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rwb-decision's and rwb-case's; the route moves and the decision-log entries of the broken plan are rwb-case's; and the end-to-end proof is the integration harness. This slice delivers the resolved permission view, the authorise decision for the plan-status read, and one access entry per decision, and it states and proves that no masking row applies because the panel carries no personal field.

It meets REQ-CHO-002 and REQ-DRI-013 on the access side, keeps R-UNI-39 (a decision that cannot be recorded does not proceed) and gives NFR-042 its entry for this capability. The measure of success is that every look at a plan status is granted or refused by the policy in force, that the refusal of a role without the right and of a case outside the scope are indistinguishable from a case that does not exist, and that no access entry carries a plan reference, a plan status or a personal value.

### 3. Preconditions

- RWB-P4-E1037-CON is published: the service contract of `rwb-access` already in force from wave 1, with `POST /authorise`, `GET /me/permissions` and `/masking-policies` on base `/api/recovery/access/v1`, the error envelope and the masking read (DP-08). This story serves the decision behind those operations for the plan-status read and adds no operation.
- RWB-P2-E2002-CON is published as the fixture of this key: the plan-status envelope for case `RW-2026-000310` with plan reference `TDR-SYN-0310`, status `APPROVED` and status date `2026-12-10`, and the plan reference the caller passes in the authorise request (DP-11). The rwb-integration contract is consumed as a fixture only; rwb-access calls no rwb-integration operation.
- RWB-P4-E1037-APP and RWB-P4-E1039-APP delivered the matrix and access-log baseline in `rwb_access`: `role`, `permission`, `masking_rule`, `role_conflict` and the local decision-record table exist before this story adds its index and its own migration.
- The matrix version `PM-2026.12` is in force in `permission` with CASE_RECORD right R for `RW-CASEOWN`, `RW-RESTRUCT` and `RW-AUDIT`, no CASE_RECORD row for `RW-REFADM`, and the default scope OWN for `RW-CASEOWN`, OWN for `RW-RESTRUCT` and ALL for `RW-AUDIT` (DF-REF-035 to DF-REF-044). The TSD P4 RBAC matrix tabulates Rules and parameters, Reference data and Platform administration only and has no Case record column, so the CASE_RECORD letters are read from the pack as data and confirmed with the matrix owner (GAP-0907; ASM-1630).
- No `masking_rule` row is needed for this capability: the plan-status panel shows the plan reference, the status and the status date only, and none of the three is a personal field, so no mask answer is produced and none is asked for (FSD P4 A2.5; TSD P4 T3.1).
- The caller sends the case attributes the scope test needs — the case ID, its owner, its queue, its team and the plan reference — inside the authorise request and inside the resolved-view call; rwb-access reads no `rwb_case` table, calls no rwb-case operation and reads no `v_ace_*` view (DP-01, DP-05). The attribute set and its field names are Not specified in the source documents (GAP-0908; ASM-1628).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live (DP-03), and the outbox and inbox library is live in `rwb_access` (DP-09).
- The parameters contract of rwb-case and its client library are live for the feature switch and the cache size (DP-06); the reference-data contract of rwb-case is live for LOV-CAPABILITY and LOV-SCOPE (DP-07), so no capability area and no scope value is written in code.
- The login is the rwb-access login (DP-02). The per-service login name is Not specified in the source documents (GAP-0909; ASM-1629).
- The platform contract libraries the DP rows name — DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 — are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None).

### 4. Flow

1. A person opens SCR-03 Case record for a case; gateway-bff resolves the session, calls rwb-case for the case and rwb-integration for the plan-status answer, and the plan-status panel is composed at the edge (DP-19).
2. gateway-bff or rwb-case asks `GET /api/recovery/access/v1/me/permissions` once for the session, and receives the caller's roles, the CASE_RECORD letters in force, the scope and the matrix version.
3. From that one answer the caller learns whether the caller may read the case at all: a caller with no CASE_RECORD letter is refused before any case is read and the panel is not assembled; this story produces the refusal and its entry (BR1).
4. The caller that may read the case builds the authorise request: the caller identity from the session, the capability area `CASE_RECORD`, the right `R`, the case reference, the plan reference `TDR-SYN-0310` and the case attributes the scope test reads — the owner, the queue and the team. The full attribute set is Not specified in the source documents (GAP-0908; ASM-1628).
5. `rwb-access`: the request is served from the decision cache when the same identity, area, right, case reference and field list is already held under the matrix version in force; otherwise it is decided. The cache is keyed on the version, not on a clock, so no answer decided under an older version is served (BR7).
6. `rwb-access`, right check: the CASE_RECORD letters are unioned across the roles the caller holds from `permission` at the matrix version in force, `PM-2026.12`; no letter is written in code. No CASE_RECORD R gives a refusal, 403 with MSG-P4-002 naming the action, and no case data (BR1).
7. `rwb-access`, scope check: the case is in scope when the attributes carried in the request satisfy the caller's `default_scope` read through the reference-data contract of DP-07 — OWN for a case the caller owns, TEAM for a case of the caller's queue's team, REGION for a case of the caller's region, ALL for any case (BR2). A missing attribute never decides an allow (BR8).
8. `rwb-access`: a case that is absent, or that sits outside the caller's scope, is answered as not found, 404 with MSG-P4-003, and carries no case data, no plan reference, no plan status and no status date, so the answer never confirms that a case or a plan exists (BR3).
9. `rwb-access`, masking: the field IDs of the panel are `DF-CAS-046` (`plan_ref`), `DF-CAS-047` (`plan_status`) and `DF-CAS-048` (`plan_status_as_of`), and none of them is a personal field; no `masking_rule` row is read and no mask answer is produced or owed (BR9).
10. `rwb-access`: the access entry is written first, in the same transaction as the answer — decision code `AC-READ` or `AC-DENY` (FSD P4 A2.7), the actor, the case ID, the area, the right, the field IDs and the time. The entry names the field IDs and never their values; the `case_id` is empty only for an access event with no case (DF-DEC-002).
11. `rwb-access`: the local decision record is written through the decision-record library with its hash link and its outbox row; the relay publishes `DecisionRecorded` on `rwb.decision-record.v1` for the central ledger in rwb-decision. If the record cannot be written the answer is 503 MSG-P7-003 and no case data is returned (R-UNI-39).
12. `rwb-access`: the caller receives the decision with the decision code, the matrix version, the scope result and the entry reference, and the panel shows the plan reference, the status and the status date that rwb-integration's and rwb-case's answers carry.
13. When a new matrix version is put in force through the load path, the cached letter set under the old version is dropped in the transaction that writes the new one and the next request is decided on the new version, with no restart (AC6).

Every answer, granted or refused, is written before it is returned: no plan-status read is ever unlogged, and a read that cannot be recorded returns nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No role the caller holds gives CASE_RECORD R at the matrix version in force | Refused before any case fact is read: 403, no case data, one `AC-DENY` entry | MSG-P4-002 | AC3 |
| X2 | The case is absent, or sits outside the caller's scope | Not found: 404 with no case data, no plan reference and no plan status; one `AC-DENY` entry naming the case ID | MSG-P4-003 | AC4 |
| X3 | The request carries no owner, queue or team attribute and the scope needs it | No allow is decided from a partial answer: 404, no case data, the refusal recorded | MSG-P4-003 | AC8 |
| X4 | The decision record cannot be written | Nothing is returned: 503 with no case data, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC2, TC-E2-002-11 |
| X5 | The reference list of scope or capability is not available | No answer is given rather than a guessed one: 503, and the refusal is recorded | MSG-GEN-006 | AC9 |
| X6 | The token carries no Workbench role | No answer is given: 401 before the policy is read | MSG-P4-001 | AC10, AC11 |
| X7 | A cached answer outlives a matrix version change | The version is compared on every served answer and the entry cached under the old version is dropped on the change, with no restart | None | AC6 |
| X8 | The request names no field IDs | The entry records no field IDs; the decision itself is unchanged | None | AC5 |

A matrix version that changes twice on one business date is not specified in the source documents (GAP-0907; ASM-1630); until it is, the version whose latest `valid_from` is on or before the business date is used and the answer names the version it used.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against the rwb_access version this story applies (DDL owned by RWB-P4-E1001-APP), RWB-P4-E1037-CON and the RWB-P2-E2002-CON fixture; the case attributes arrive in the request and no other service is called at run time |
| Negotiable | Roles, letters, scope values, matrix version, cache size and switch are data rows and parameters; the story fixes the decision path, the two refusals and the entry only |
| Valuable | The plan status of a case is shown to the roles the matrix admits and to nobody else, both refusals are safe, and every look leaves one entry |
| Estimable | Two answers behind existing operations, one cache, one entry path and one index |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test with a fixture; the plan-status answer is stubbed from RWB-P2-E2002-CON |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case — access decisions and access entries

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-RESTRUCT and RW-AUDIT, and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "OWN" for RW-RESTRUCT and "ALL" for RW-AUDIT
    Given the rwb-integration contract mock returns the plan-status envelope for case "RW-2026-000310" with plan reference "TDR-SYN-0310", status "APPROVED" and status date 2026-12-10

  Scenario: AC1 The resolved permission view answers in one hop (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN and owns case "RW-2026-000310"
    When the caller calls GET /api/recovery/access/v1/me/permissions
    Then the answer names role "RW-CASEOWN", CASE_RECORD right "R", scope "OWN" and matrix version "PM-2026.12"
    Then the answer is returned in one hop inside the 2 s budget, with no call to rwb-case and no read of the case
    Then the plan-status panel learns from that one answer that CASE_RECORD right "R" is granted for case "RW-2026-000310", and the plan read itself is not made here

  Scenario: AC2 The plan-status read is granted and recorded once (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN with scope "OWN" and owns case "RW-2026-000310"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000310", plan reference "TDR-SYN-0310" and field IDs "DF-CAS-046", "DF-CAS-047" and "DF-CAS-048", with owner, queue and team attributes
    Then the answer grants the read with decision code "AC-READ", scope "OWN" and matrix version "PM-2026.12"
    Then one access entry is written with decision code "AC-READ", the actor, case "RW-2026-000310", area "CASE_RECORD", right "R", the three field IDs and decided at
    Then the panel shows plan "TDR-SYN-0310" with status "APPROVED" and status date 2026-12-10 from the rwb-integration fixture, and this service supplies only the grant

  Scenario: AC3 A role without the Case record right is refused (new, D-RCV-60)
    Given test user "U-7104" holds RW-REFADM, which has no CASE_RECORD row in "PM-2026.12"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310"
    Then the answer is refused with status 403 and message MSG-P4-002 for action "read the plan status"
    Then no plan reference, no plan status, no status date and no case data is returned
    Then one entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R" and result "REFUSED"

  Scenario: AC4 A case outside the scope is not found (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN with scope "OWN" in team "MTG-BKK"
    And case "RW-2026-000310" is owned by another user and sits in team "SME-NTH"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310"
    Then the answer is status 404 with message MSG-P4-003
    Then the answer carries no case data, no plan reference, no plan status and no status date
    Then one entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R" and the case ID

  Scenario: AC5 The entry carries the case ID and the field IDs only (new, D-RCV-60)
    Given test user "U-7103" holds RW-AUDIT with scope "ALL" and reads case "RW-2026-000310"
    When the plan-status read is decided with field IDs "DF-CAS-046", "DF-CAS-047" and "DF-CAS-048"
    Then the entry names the case ID, area "CASE_RECORD", right "R" and the three field IDs
    Then the entry carries no plan reference "TDR-SYN-0310", no plan status "APPROVED", no status date 2026-12-10, no account number, no amount, no name and no identity number
    Then the entry is appended through the decision-record library and relayed on "rwb.decision-record.v1", with no other Kafka event for the access log

  Scenario: AC6 The cached letter set is refreshed on a matrix version change (new, D-RCV-60)
    Given test user "U-7105" holds RW-LEGAL and is refused CASE_RECORD R under "PM-2026.12", and the refusal is cached
    When the matrix in force moves to "PM-2026.13" with CASE_RECORD R for "RW-LEGAL"
    Then the next ask is granted with decision code "AC-READ" and matrix version "PM-2026.13"
    Then the service is not restarted and no answer cached under "PM-2026.12" is returned after the change
    Then the change itself is published as "AccessPolicyChanged" by the story that puts the version in force, not by this story

  Scenario: AC7 No masking row applies to the plan-status panel (new, D-RCV-60)
    Given masking version "MASK-SIT-01" is in force and covers no row for "DF-CAS-046", "DF-CAS-047" or "DF-CAS-048"
    Given test user "U-7102" holds RW-RESTRUCT with scope "OWN" and owns case "RW-2026-000310"
    When the caller asks for case "RW-2026-000310", area "CASE_RECORD", right "R" and the three field IDs
    Then the answer is granted and produces no masked marker, because none of the three is a personal field
    Then no masking row is read for the request and no mask answer is owed
    Then the entry records the three field IDs as returned and carries no value of any of them

  Scenario: AC8 The decision comes from the request alone (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN with scope "OWN"
    When the caller asks for case "RW-2026-000310", area "CASE_RECORD", right "R", with no owner attribute in the request
    Then the answer is status 404 with message MSG-P4-003 and carries no case data
    Then no case row is read: no call to rwb-case and no query on "rwb_case"
    Then one entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R" and the case ID

  Scenario: AC9 The reference list is not available and nothing is guessed (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN with scope "OWN"
    And the reference-data list of scope values is not available
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310"
    Then the answer is status 503 with message MSG-GEN-006 and carries no case data
    Then no scope value or capability value is taken from code in its place
    Then the refusal is recorded as one entry with decision code "AC-DENY", area "CASE_RECORD", right "R" and the case ID

  Scenario: AC10 A token with no Workbench role gets no answer (new, D-RCV-60)
    Given a test user holds a token that carries no Workbench role
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310"
    Then the answer is status 401 with message MSG-P4-001, before the permission policy is read

  Scenario: AC11 A token with no Workbench role gets no permission view (new, D-RCV-60)
    Given a test user holds a token that carries no Workbench role
    When the caller calls GET /api/recovery/access/v1/me/permissions
    Then the answer is status 401 with message MSG-P4-001 and names no role, matrix version or scope
    Then no role, permission row or matrix version is read for the caller

  Scenario: AC12 The service holds only its own tables and writes the entry through the library (new, D-RCV-60)
    Given the rwb-access service is built from its code and configuration
    When the architecture guardrail scans rwb-access for case-side reads and hard-coded values
    Then no table of "rwb_case", no rwb-case operation and no "v_ace_*" view is read, and nothing is copied into "rwb_access"
    Then the service holds only role, permission, masking_rule, the decision record, the outbox and the inbox table processed_event
    Then no role code, area, letter or scope value is written in Java, and the entry is relayed on "rwb.decision-record.v1" only

  Scenario: AC13 Each error answer carries its status code and message ID (new, D-RCV-60)
    Given a test user holds RW-REFADM, which has no CASE_RECORD row in "PM-2026.12"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310"
    Then the error answers of both operations use only the status codes and message IDs listed in section 5, namely 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006 and 503 MSG-P7-003
    Then each error answer carries no case data

  Scenario: AC14 A replayed write with the same idempotency key writes nothing new (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN with scope "OWN" and owns case "RW-2026-000310"
    And the caller has already asked POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000310" under matrix version "PM-2026.12" with an idempotency key
    When the caller replays the same POST /api/recovery/access/v1/authorise with the same idempotency key
    Then the replayed answer equals the first answer with decision code "AC-READ" and matrix version "PM-2026.12"
    Then no second access entry is written and the entry count is unchanged
```

The fourteen criteria above are new and test only this deliverable: the resolved permission view, the authorise decision for the plan-status read and the access entry per decision. The legacy criteria of RWB-E2-002 are owned elsewhere: AC1 to AC9 are carried by rwb-integration (RWB-P2-E2002-APP), the stored status, the route moves and the rules by rwb-case (RWB-P3-E2002-APP) and the package by rwb-decision (RWB-P7-E2002-APP). The legacy exception X6 (a case outside the scope, MSG-P4-003) is answered here by AC4, and the legacy exception X7 (a role without the Case record right, MSG-P4-002) by AC3 and AC5; legacy test case TC-E2-002-10 is answered here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force, unioned across the roles the caller holds; a caller whose roles hold no Case record R is refused with MSG-P4-002 and no case data | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; DP-08 |
| BR2 | A case is in scope when the attributes the request carries satisfy the caller's `default_scope` in force — OWN, TEAM, REGION or ALL — read through the reference-data contract; no scope value is written in code | FSD P4 A2.14 VR-P4-014-1; TSD P4 T3.2 LOV-SCOPE; DP-07 |
| BR3 | A case that is absent, or outside the caller's scope, is answered 404 with MSG-P4-003 and no case data, no plan reference, no plan status and no status date, so the answer never confirms that a case or a plan exists | FSD P4 A2.14 AC-EXC-P4-014-01; legacy AC8 |
| BR4 | Every decision, granted or refused, writes one access entry with decision code `AC-READ` or `AC-DENY`, the actor, the case ID when the decision is on a case, the area, the right, the field IDs and the time, before the answer is returned | FSD P4 A2.7 AC-P4-007-01; FEAT-ACA-07 |
| BR5 | The access entry is a decision-record entry written through the local library and relayed on `rwb.decision-record.v1`; it is never a new Kafka event and never a new topic | FSD P4 A2.8; DP-03; Architecture v5 slide 20 |
| BR6 | A read that cannot be recorded returns nothing: 503 MSG-P7-003 and no case data, and an incident is raised | FSD P4 A2.7 AC-EXC-P4-007-03; R-UNI-39 |
| BR7 | An answer is cached only under the matrix version it was decided on; a change of version drops the entry in the transaction that writes the new version, with no restart and no clock | Architecture v5 slides 14 and 43; DP-11 |
| BR8 | The case attributes for the scope test arrive in the request and a missing attribute never decides an allow; no table of `rwb_case`, no rwb-case operation and no `v_ace_*` view is read, and nothing is copied into `rwb_access` | DP-01, DP-05, DP-11; ownership map (case to P3, ACE views to P1) |
| BR9 | No masking row applies to the plan-status panel: the field IDs `DF-CAS-046`, `DF-CAS-047` and `DF-CAS-048` name the plan reference, the status and the status date, none is a personal field, and no mask answer is produced or owed | FSD P4 A2.5; TSD P4 T3.1 `masking_rule`; NFR-040 |
| BR10 | The entry names IDs and field IDs only: no plan reference, no plan status, no status date, no amount, no account number and no personal value is written on it | FSD P4 A2.7; DF-DEC-002, DF-DEC-014; NFR-039 |
| BR11 | Roles, capability areas, letters, scope values, the matrix version and the field IDs are data rows and list values; no role code, area, letter or scope value is written in Java | FSD P4 BR-P4-004; TSD P4 T3.1 and T3.2; principle 1 |
| BR12 | The plan read, the stored status and its date, the route moves and the rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are not decided here: this story grants or refuses the read and records it | Architecture v5 slides 41 and 44; DP-01 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles at the `matrix_version` in force, with the letters held as the five-character field of TSD P4 T3.1 and the answer naming the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; the scope names are list values, never Java constants, and the attribute names of a request are Not specified in the source documents (GAP-0908; ASM-1628).
- BR3 is the only refusal that hides a case, and it is deliberate: MSG-P4-003 echoes no case fact and the entry still names the case ID, so the audit can see the attempt.
- BR4 and BR6 are one `RecordAndApply` transaction: the record is written first, the answer is returned after it commits, and a failure answers 503 and changes nothing (X4).
- BR7 is a cache keyed on `matrix_version`; the cache size is a parameter of DP-06, and no lifetime in seconds is used, so no answer survives a version change.
- BR8 is the reason there is no repository for a case: the service holds `role`, `permission`, `masking_rule`, the decision record and the outbox, and nothing else.
- BR9 and BR10 are visible in the code review and in the entry itself: the three field IDs appear as identifiers, and no value of them appears anywhere in the service.

### 9. State transitions

None. This story changes no case status, no plan status and no route state: the case and its stored plan status are P3's, the live plan read is P2's, and the rules that move a case on a broken plan are rwb-decision's package and rwb-case's move (TSD P4 T4: no case state machine of its own). This story runs no workflow, owns no Schedule and starts no timer.

The only states this story has are the states of its answer and of its record, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds Case record R and the case is in scope | The decision code, the scope it used, the matrix version and the entry reference; no mask answer, because none is owed | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R | 403 MSG-P4-002, no case data | `AC-DENY` |
| Not found | The caller holds the right and the case is absent or outside the scope, or an attribute is missing | 404 MSG-P4-003, no case data | `AC-DENY` |
| Not answered | The record cannot be written, or the policy cannot be read | 503, no case data | None; the failure is raised as an incident |

A matrix version moves from LOADED to APPROVED to IN_FORCE to SUPERSEDED or ROLLED_BACK in the load path (TSD P4 T3.2 LOV-VERSION-STATUS); this story only reads the version in force, answers from it and drops its cached answer when it changes. The plan status values CREATED, APPROVED, BOOKED and BROKEN are rwb-integration's and rwb-case's and are never interpreted here: this story carries the field ID `DF-CAS-047`, never the value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Resolves the letters and the scope, decides, writes the access entry and the outbox row |
| Decision-record library identity | Writes the local entry with its hash link and relays it on `rwb.decision-record.v1` (Decision log C, DP-03) |
| RW-CASEOWN, case owner | Case record R with default scope OWN: reads the plan status of a case it owns |
| RW-RESTRUCT, restructuring officer | Case record R with the role default scope: reads the plan status of a case in that scope |
| RW-AUDIT, internal audit | Case record R with default scope ALL: reads any case's plan status, including the entries of this capability through the access-log search of RWB-P4-E1039-APP |
| RW-REFADM, reference data administrator | No CASE_RECORD row: the plan-status read is refused with MSG-P4-002 |
| RW-SECADM, security administrator | Puts a matrix version in force through the load path stories; this story reads the version in force and answers from it |
| SY-CASEWF and the other service identities | Ask the same question for their own service; the roles of a service identity are checked as a person's are |

Reading is the whole of this story: it grants or refuses a read and writes the record of it. It changes no case, no plan, no route state and no policy row; a policy row changes only through the load path of RWB-P4-AD002-APP. The roles, areas and letters above are rows of the pack and are not fixed in code; no role in this story may grant itself a letter.

The per-service login name is Not specified in the source documents (GAP-0909; ASM-1629); the story refers to "the rwb-access login (DP-02)" until the platform DB story fixes it.

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read; entra_group has no BR Field ID in LDM v9 (Not specified in the source documents (DOR-RWB-P4-E2002-APP-7)) |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read; no row covers `DF-CAS-046`, `DF-CAS-047` or `DF-CAS-048`, and none is needed |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-CAPABILITY and LOV-SCOPE values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | access entry (local decision record, DP-03) | the `AC-READ` and `AC-DENY` entries: decision code, actor, case ID, actions, decided at, hash chain, idempotency key | Write |
| DF-DEC-002 | access entry (local decision record) | case_id | Write |
| DF-DEC-014 | access entry (local decision record) | actions (area, right, field IDs, result) | Write |
| (outbox) | outbox library table in `rwb_access` | the `DecisionRecorded` row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| DF-CAS-046, DF-CAS-047, DF-CAS-048 | case (in the entry; whether the authorise request names them is Not specified in the source documents (GAP-0908); owned by rwb-case) | plan_ref, plan_status, plan_status_as_of | Not read and not written; carried as field IDs on the entry |
| DF-CAS-001, DF-CAS-009, DF-CAS-010 | case attributes in the authorise request (owned by rwb-case) | case ID, owner, queue and team for the scope test | Read from the request; nothing copied |

No case row, no plan row and no ACE row is copied into `rwb_access`: the case attributes for the scope test arrive with the authorise request on each decision, and the plan reference and the plan status stay with rwb-integration and rwb-case. No plan reference, plan status, status date, amount, account number or personal value is written on the access entry; the entry holds IDs and field IDs only. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decisions are served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path and error shape. This slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | Decide the plan-status read for a case and a field list, with the scope test on the request attributes and the access entry | Any authenticated caller with a Workbench role | Idempotent by identity, area, right, case reference and field list within the matrix version in force |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, the CASE_RECORD letters in force, the scope and the matrix version | Authenticated caller, own record only | Not applicable |

Request for `/authorise`: the caller identity from the session, the capability area `CASE_RECORD`, the right `R`, the case reference, the plan reference, the field IDs and the case attributes for the scope test (owner, queue, team). Answer: the decision code (`AC-READ` or `AC-DENY`), the matrix version, the scope result and the access-entry reference. The field names of the request and of the answer are Not specified in the source documents (GAP-0908; ASM-1628). Errors: 401 no Workbench role (MSG-P4-001), 403 no letter for the area or right (MSG-P4-002), 404 case absent or out of scope (MSG-P4-003), 503 decision record unwritable (MSG-P7-003).

The same service surface carries `GET /me/session` (TSD P4 API-P4-012, the resolved session), `GET /admin/roles` (TSD P4 API-P4-007, the role list with permissions and scope), `/masking-policies`, `GET /doa-limits` and `GET /admin/access-log`; those belong to other P4 stories (RWB-P4-E1037-APP, RWB-P4-E1022-APP, RWB-P4-E1039-APP, RWB-P4-E2013-APP) and this story changes none of them. The TSD appendix names the resolved view as `GET /me/session` and has no `/me/permissions` entry, so the resolved view is answered behind `/me/permissions` under R-PREC and the session read keeps its own story and its own shape (GAP-0908; ASM-1628).

#### 12.2 REST operations consumed

None. The case attributes and the plan reference for the decision arrive in the authorise request, built by the caller from its own rows; rwb-access calls no service at run time, and the one hop and the 2 s budget of DP-11 apply to the inbound call.

The rwb-integration contract (RWB-P2-E2002-CON) is consumed as a fixture only: the plan-status envelope names case `RW-2026-000310`, plan reference `TDR-SYN-0310`, status `APPROVED` and status date `2026-12-10`, and its plan reference is what the caller passes in the authorise request. rwb-access calls no rwb-integration operation, reads no ACE view and reads no `rwb_case` row: the reference-data values reach it through the client library of rwb-case (DP-07).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId, or the actor for an entry with no case | decision code, area, right, field IDs, matrix version, record reference, business date |

The event is written to the outbox in the same transaction as the answer and relayed with the CloudEvents envelope; no personal data is carried (DP-09). The access log is never published as its own event: it is the decision-record entry of this service (DP-03). `AccessPolicyChanged` on `rwb.access.events.v1` belongs to the story that puts a matrix version in force — the load path of RWB-P4-AD002-APP — and is not republished here; `DoaLimitChanged` belongs to the delegation slice of RWB-P4-E2013-APP.

#### 12.4 Events consumed

None. This slice consumes no topic: the decision is served from the matrix version in force on each call, and a change of the version drops the cached answer in the transaction that writes the new version. `AccessPolicyChanged` is published for the other services' caches and for gateway-bff; this service does not consume its own outbox.

#### 12.5 Workflows and activities

None. The decision is a synchronous REST call in the caller's thread, and this story runs no workflow and registers no activity on `rwb-access` (Temporal and Drools design slide 11: each service has a worker, and this capability needs none). The Drools kit is applied only as a read of the evaluated policy rows: the letters of a capability area are rows, not a decision table, and the RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are evaluated in rwb-case and rwb-decision, never here (DP-04).

#### 12.6 Schedules

None. The daily plan-status step is JOB-02 Case creation's, owned by rwb-case (Architecture v5 slide 44) with the plan-status read carried by RWB-P2-E2002-APP, and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP. This story holds no Schedule of its own.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `role` | P4 (`rwb_access`) | Recovery roles as data, with role class and default scope |
| `permission` | P4 (`rwb_access`) | Capability area, letters and matrix version per role |
| `masking_rule` | P4 (`rwb_access`) | Read only; no row covers the three plan-status field IDs, because none is a personal field |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | The access log of this capability as `AC-READ` and `AC-DENY` entries (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`role_conflict` is the same service's table and is read by the sign-in path, not by this story; `delegation_limit` is served by RWB-P4-E2013-APP and is not read here. rwb-access reads no table of another service and holds no foreign key across services (DP-01); the central ledger copy of the entries is written in `rwb_decision` from the topic by RWB-P7-E1027-CON.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration fixture (RWB-P2-E2002-CON) | The P2 contract of this legacy key | The plan-status envelope for case `RW-2026-000310` with plan reference `TDR-SYN-0310`, status `APPROVED` and status date `2026-12-10`; replayed for the granted and the refused cases |
| RWB-P4-E1037-CON fake | The P4 authorise, resolved-view and masking contract | `/authorise` and `/me/permissions`, with a granted case, a refused case and an out-of-scope case |
| decision-record library stub | DP-03 | A healthy chain and outbox, and a stopped chain for the 503 path (TC-E2-002-11) |
| reference-data fake | DP-07 | LOV-CAPABILITY with `CASE_RECORD` and LOV-SCOPE with OWN, TEAM, REGION and ALL, with the version in force |

The exact request and answer shapes of `/authorise` and `/me/permissions` are stubbed from the published fixture of RWB-P4-E1037-CON; their field list is Not specified in the source documents (GAP-0908; ASM-1628).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided (2 existing operations implemented), 0 consumed | The decisions are served on `/authorise` and `/me/permissions` of RWB-P4-E1037-CON on `/api/recovery/access/v1`; the case attributes arrive in the request, one hop within 2 s |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published; no topic consumed and no access event on `rwb.access.events.v1` from this story |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `caserecord`, Java package `th.co.scb.ace.workbench.recovery.access.caserecord`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own (metadata "Depends on (build)" = None, "Contract dependencies" = RWB-P2-E2002-CON), and it builds against the rwb-access baseline and its contract fake, with the platform contract libraries and the P4 contract stories already delivered by the baseline. DP-05 applies as a prohibition — no ACE view is read here, and the plan reference arrives in the authorise request from the caller. DP-04 applies as a statement that the letters of a capability area are rows, not a decision table, and that the RESTRUCTURE rows are evaluated in rwb-case and rwb-decision. DP-06 carries the feature switch and the cache size as parameters, so no value is a Java constant. DP-10 applies as a statement that the daily plan-status step and the plan timer are not this service's: JOB-02 is rwb-case's with its plan-status read in RWB-P2-E2002-APP, and the only Schedule on this service is JOB-18 of RWB-P4-AD008-APP. DP-19 is the route that renders the answer on SCR-03.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | `POST /authorise` with validation and the problem mapping for 401, 403, 404 and 503 |
| PermissionController | Controller | `GET /me/permissions` for the caller's own record only |
| PermissionViewService | Service | Resolves the roles, the CASE_RECORD letters at the matrix version in force and the scope into the one answer the panel reads |
| AccessDecisionService | Service | Right, then scope, for one request; one answer and one record in that order |
| ScopeRule | Service | Compares the case attributes of the request with the `default_scope` value in force; refuses an allow when an attribute is missing |
| PolicyRepository | Repository | Reads `role`, `permission` and `masking_rule` at the version in force in `rwb_access`; reads no other schema |
| AccessRecordWriter | Service | Writes the `AC-READ` and `AC-DENY` entries through the decision-record library, first in the transaction, and the outbox row |
| PolicyCache | Cache | Holds an answer under the matrix version it was decided on and drops it on a version change |
| ReferenceCatalog | Service | Reads LOV-CAPABILITY and LOV-SCOPE through the reference-data contract; no area or scope value in Java |

**Database and migrations**

- Reads `role`, `permission` and `masking_rule` in schema `rwb_access`; writes the access entry of the decision-record library and the outbox row.
- Migration in this story: `V2002_1__plan_status_access.sql` adds the index on `permission (capability_area, matrix_version, role_id)` used by the letter read and the index on the access entry `(actor, decided_at)` used by the access-log search of RWB-P4-E1039-APP. The tables arrive with the `rwb_access` baseline; no column is added for case, plan or customer data.
- No row of `role`, `permission` or `masking_rule` is written by this story: the matrix version is put in force by the load path of RWB-P4-AD002-APP.

**Configuration and reference data**

- The policy pack slice in force at matrix version `PM-2026.12`: CASE_RECORD R for `RW-CASEOWN`, `RW-RESTRUCT` and `RW-AUDIT`; no CASE_RECORD row for `RW-REFADM`; default scope OWN for `RW-CASEOWN`, OWN for `RW-RESTRUCT` and ALL for `RW-AUDIT`. The slice is read as data, and the TSD matrix has no Case record column, so the letters are confirmed with the matrix owner (GAP-0907; ASM-1630).
- No masking row for `DF-CAS-046`, `DF-CAS-047` or `DF-CAS-048`: none of the three is a personal field.
- LOV-CAPABILITY (the 14 capability areas, including `CASE_RECORD`) and LOV-SCOPE (OWN, TEAM, REGION, ALL), a closed list in Reference Data v5, through the reference-data contract of DP-07; a new scope value is a change to the list and to this story, not a data row.
- The cache size is a parameter of the parameters contract (DP-06); no cache lifetime in seconds is used, because the cache is keyed on the matrix version.
- The feature switch is `rwb.access.plan-status-authorise`, read as a parameter through the parameters contract: off means the decision is refused closed and the caller is told the capability is not open, never allowed by default.
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0909; ASM-1629).

**Build steps**

1. `PolicyRepository` and `PermissionViewService` over the matrix version in force, with a test per letter set and a test that the resolved view names roles, letters, scope and version in one answer; no role, area or letter in code.
2. `AccessDecisionService` with the letter union and the default-deny path; tests for AC3.
3. `ScopeRule` over the request attributes, with the not-found, the missing-attribute and the no-partial-allow tests; tests for AC4 and AC8.
4. The no-masking statement in the answer and the entry: a test that the three field IDs produce no mask marker and read no masking row; test for AC7.
5. `AccessRecordWriter` with the entry before the answer, the `AC-READ` and `AC-DENY` codes, IDs and field IDs only, and the 503 when the record cannot be written; tests for AC2, AC5 and TC-E2-002-11.
6. `PolicyCache` with the version-keyed answer and the drop on a version change; tests for AC6.
7. The outbox relay for `DecisionRecorded`, with the topic name and the payload carrying no plan value and no personal value; test the envelope with the contract fake.
8. The contract-fake run of the whole capability against RWB-P2-E2002-CON and the decision-record fake, so the story builds before the other slices of the key exist in the environment.

**Feature switch.** `rwb.access.plan-status-authorise`, read as a parameter; off refuses closed, allows nothing and changes no schema, so a rollback is one value.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P2-E2002-CON and RWB-P4-E1037-CON stay green, and a SIT week shows every plan-status read decided with one entry, every refusal answered with MSG-P4-002 or MSG-P4-003 and no case data, no access entry carrying a plan reference, a plan status, a status date or a personal value, and a matrix version change taking effect with no restart.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer (X6) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 (AC3) |
| MSG-P4-003 | The case is absent or outside the caller's scope, or an attribute is missing | This case is not in your scope. | This story, on the refusal of BR2 (AC4, AC8) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X4) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Your request is queued and will be retried. | This story, on a reference-list failure (X5) |
| MSG-P2-008 | The plan status shown is the stored value, on the screen this decision guards | The ACE plan status is from {date}. Today's status was not returned. | rwb-integration and rwb-case, on the panel answer; copied here unchanged because the screen this decision guards shows it |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "read the plan status"; for MSG-P4-003 no case fact, no plan reference and no plan status is echoed, because the message must not confirm that a case or a plan exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10.

### 15. Screens and states

This story builds no screen. SCR-03 Case record and its plan status panel are served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which calls rwb-case for the case and the stored plan status, rwb-integration for the live plan status and rwb-access for the resolved view and the decision — one hop each, in parallel, then merges the answers into the screen model; the panel itself, the plan read and the stored fallback are RWB-P3-E2002-APP's and RWB-P2-E2002-APP's.

What this story decides for SCR-03 is whether the panel may be assembled at all, and what each state shows:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record, plan status panel | Read only, granted | The panel is assembled with the plan reference, the status and the status date; the fields this story names are rendered as they arrive, and no masking marker is applied because none is owed |
| SCR-03 Case record, plan status panel | Status from the stored value | The same grant applies; MSG-P2-008 with its date is rwb-integration's and rwb-case's message, and the grant is unchanged |
| SCR-03 Case record, plan status panel | A role without Case record R | The panel is not assembled; the page shows MSG-P4-002 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record, plan status panel | Case outside the scope | The page shows MSG-P4-003, the same page a case that does not exist shows, and no case fact, plan reference or plan status |
| SCR-03 Case record, plan status panel | Not available | The page shows MSG-P7-003 where the record could not be written, or MSG-GEN-006 where a list could not be read, and no case fact |
| SCR-03 Case record, plan status panel | Loading | Not specified in the source documents (CG-ALL-5145) |
| SCR-03 Case record, plan status panel | Empty | Not specified in the source documents (CG-ALL-5145) |
| SCR-03 Case record, plan status panel | Error | Not specified in the source documents (CG-ALL-5145) |
| SCR-03 Case record, plan status panel | No access | Not specified in the source documents (CG-ALL-5145) |

The panel shows the plan reference, the status and the status date only; no personal field is on it for this capability, so nothing is masked and no masking row is read. The screen field list of the composite route, its merge order, its field-level masking and its route specification are Not specified in the source documents (GAP-0909; ASM-1631).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-10 | AC3, AC5, BR1, BR4 | Component | RW-REFADM (no Case record right) asks for the plan-status read of case RW-2026-000310; refused with MSG-P4-002, one AC-DENY entry, no case data |
| TC-E2-002-01 | AC1, AC2, AC7, BR1, BR4, BR9 | End to end | Fixture plan TDR-SYN-0310 APPROVED with status date 2026-12-10; the access answer grants and writes one AC-READ entry; the plan read and the display are RWB-P2-E2002-APP's |
| TC-E2-002-02 | AC2, BR4, BR12 | End to end | Fixture plan BROKEN for a case in PLAN_CURE_PERIOD; this story answers only the access entry of the read that follows, and no route state moves here |
| TC-E2-002-03 | AC3, BR10 | End to end | Fixture returns no plan for the case; the access answer is unchanged and the entry carries field IDs only |
| TC-E2-002-04 | AC4, BR7 | NFR | Fixture delayed beyond the 2 s budget; this story's own answer stays inside 2 s because it calls nothing, and the panel's fallback is P3's |
| TC-E2-002-05 | AC5, BR10 | End to end | Fixture returns status SUSPENDED; no status value of any kind appears on the access entry |
| TC-E2-002-06 | AC6, BR7 | End to end | The daily step runs twice for 2026-12-15; this story's answer is idempotent under one matrix version and writes one entry per decision |
| TC-E2-002-07 | AC7, BR6 | End to end | Decision record store stopped; this story answers 503 MSG-P7-003 with no case data |
| TC-E2-002-08 | AC8, BR2, BR3 | End to end | Case owner with scope OWN and a case of another owner in team SME-NTH; answered 404 MSG-P4-003 with no case data |
| TC-E2-002-09 | AC1, BR1, BR12 | End to end | No RESTRUCTURE version in force on 2026-12-15; the package refusal is rwb-case's and rwb-decision's, and this story's grant is unchanged |
| TC-E2-002-11 | AC2, BR6 | NFR | Decision record write forced to fail on the plan-status read; nothing is returned, and the entry count is unchanged |
| TC-E2-002-12 | AC8, BR8 | Component | Case attributes with one scope attribute missing for a case of the caller; the scope test refuses the allow, no partial allow, and the answer carries no case data |
| TC-E2-002-13 | §12.1, §12.3, BR5 | Contract | The POST /authorise and GET /me/permissions operations and the DecisionRecorded event of §12 checked against the rwb-access contract fake; each matches its contract shape |
| TC-E2-002-14 | §12.7 | Component | Boundary of the §12.7 tables: the read reaches role, permission and masking_rule in rwb_access only; no read of another schema or table |
| TC-E2-002-15 | AC9, BR11 | Component | Reference list of scope values not available for the ask on case RW-2026-000310; answered 503 MSG-GEN-006 with no case data and the refusal recorded; no scope value taken from code |
| TC-E2-002-16 | AC10 | Component | Token with no Workbench role asks for the plan-status read of case RW-2026-000310; answered 401 MSG-P4-001 before the permission policy is read |
| TC-E2-002-17 | AC8, BR8 | Component | Caller asks for case RW-2026-000310 with no owner attribute in the request; answered 404 MSG-P4-003 with no case data, no rwb_case read and one AC-DENY entry |
| TC-E2-002-18 | AC11, BR1 | Component | Token with no Workbench role asks for GET /me/permissions; answered 401 MSG-P4-001 with no role, matrix version or scope returned |
| TC-E2-002-19 | AC12, BR5, BR8, BR11 | Component | Architecture guardrail scan of rwb-access: no rwb_case table, rwb-case operation or v_ace_* view read; no role, area, letter or scope value in Java; entry relayed on rwb.decision-record.v1 only |
| TC-E2-002-20 | AC13 | Contract | POST /authorise and GET /me/permissions error answers checked against the rwb-access contract fake; each status code and message ID matches section 5 |
| TC-E2-002-21 | AC14, BR4, BR7 | End to end | Same POST /authorise repeated with the same idempotency key under PM-2026.12; the replayed answer equals the first and no second AC-READ entry is written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. Every legacy test case of this key is listed above with the slice of the behaviour this story answers; the `-ITG` copies of these cases are not here — they belong to the integration slice RWB-ITG-E2002-ITG, which proves the same values across rwb-integration, rwb-case, rwb-decision and rwb-access end to end.

### 17. Guardrails

- No business value in code: roles, capability areas, letters, scope values, field IDs and the matrix version are data rows and list values read with the version in force. No role code, area, letter or scope value appears in Java.
- No personal data in events, logs, workflow inputs or tests. This story writes case IDs, role codes and field IDs only; the access entry never carries a plan reference, a plan status, a status date, a name, an address, an identity number, an account number or an amount. Test data uses synthetic keys (`RW-2026-000310`, `TDR-SYN-0310`, `A-0310`).
- ACE data only through the owner's contract or the owner's `v_ace_*` views, and this service reads neither: the plan reference and the case attributes for the scope test arrive in the authorise request from the caller, and rwb-access holds no ACE grant and queries no view.
- No cross-schema read (DP-01): `recovery_case`, `case_account`, `timer`, `task`, `rule_row`, `decision_log_entry` and the `v_ace_*` views are never queried; the case facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads the version in force and answers from it.
- One evaluator per concern: the letters of an area are versioned rows, not a decision table, and the RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 stay in rwb-decision's package and rwb-case's move. rwb-access holds no route table, no DRL source and no workbook (DP-04).
- The record is written before the answer: a failure answers 503 with no case data and raises an incident, so no plan-status read is unlogged (BR4, BR6).
- The answer is idempotent for a matrix version: the same question under the same version returns the same answer, and the cache is dropped on the version change rather than on a timer.
- The feature switch refuses closed and changes no schema, and it never widens a scope or a letter.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module, so a case is current the morning after it changes — the access side: the caller's right and scope for that read, decided once and recorded once | Business Requirements Epic 2, section 3.2; Program, sections 5.2 and 5.3 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07, TC-E2-002-11 |
| REQ-CHO-002 | A change to a restructure plan status in ACE is visible on the case through the ACE common module — the access side: the plan status is visible only to the roles the matrix admits, and a case outside the scope is not found | Business Requirements Epic 2, section 3.2; Program, sections 5.3 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09, TC-E2-002-10 |

| Legacy reference | Where it is kept |
|---|---|
| The roles of section 10 (RW-CASEOWN, RW-RESTRUCT, RW-AUDIT) and the Case record R right | Sections 1, 3, 8, 10 |
| Legacy AC8, the out-of-scope case answered 404 with MSG-P4-003 | Sections 5, 7, 8, 14 |
| Legacy exception X7 and TC-E2-002-10, the role without the Case record right refused with MSG-P4-002 | Sections 5, 7, 14, 16 |
| The plan reference TDR-SYN-0310, status APPROVED, status date 2026-12-10 and case RW-2026-000310 | Background, AC2, AC4, AC5, sections 3 and 12.8 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-006, MSG-P2-008 | Section 14, exception paths |
| Matrix version PM-2026.12, scope OWN/TEAM/REGION/ALL, roles RW-CASEOWN, RW-RESTRUCT, RW-AUDIT, RW-REFADM | Background, AC1 to AC8, sections 3 and 10 |
| Legacy key RWB-E2-002, story RWB-P4-E2002-APP, contract RWB-P2-E2002-CON | Metadata, sections 3, 12 |

The supporting features of the policy pack are FEAT-ACA-04 (role to permission matrix as data) and FEAT-ACA-07 (every access event to the access log), which the FSD P4 module pairs with its own requirements in RWB-E1-037 and RWB-E1-039; this slice answers them only for the plan-status capability and changes neither matrix nor log design. The `-ITG` copies of the test cases are carried by RWB-ITG-E2002-ITG.

### 19. Out of scope

- The plan read itself, `RestructurePlanQuery`, the 2-second timeout, the batches and the live answer: rwb-integration (RWB-P2-E2002-APP), with its contract in RWB-P2-E2002-CON.
- The stored plan status, the `plan_ref`, `plan_status` and `plan_status_as_of` columns, the daily compare, the route moves, the queues and the timers of the broken plan: rwb-case (RWB-P3-E2002-APP).
- The RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, the package version and the central ledger entries they produce: rwb-decision (RWB-P7-E2002-APP) and RWB-P3-E2042-APP.
- The end-to-end proof of these values across the four services: RWB-ITG-E2002-ITG.
- The plan read path of the monolith, `GET /cases/{caseId}/plan-status`, which belongs to rwb-integration and rwb-case and is not served here.
- The composite route itself, the SCR-03 layout, the plan status panel and its states: RWB-P3-E2002-APP and RWB-PLT-N001-CON.
- Loading, approving and rolling back a matrix version, and publishing `AccessPolicyChanged`: RWB-P4-AD002-APP and the load path of this service.
- The role list, the session read, the masking-policies read, the DoA limits and the access-log search: RWB-P4-E1037-APP, RWB-P4-E1022-APP, RWB-P4-E1039-APP and RWB-P4-E2013-APP.
- Break-glass access and its review, the six-monthly access review list (JOB-18, RWB-P4-AD008-APP), and every other job, workflow and Schedule of this service.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
