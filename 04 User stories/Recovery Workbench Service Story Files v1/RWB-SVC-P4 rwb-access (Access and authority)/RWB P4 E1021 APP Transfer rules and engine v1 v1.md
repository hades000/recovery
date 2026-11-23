# RWB-P4-E1021-APP Transfer rules and engine v1
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-R |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1021-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-021 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager, a capacity planner, a litigation officer or a legal counsel who moves a case between queues or puts a case on legal hold**, I want **the access service to answer, before the case service moves anything, whether my role holds the right for this transfer or this hold, which scope admits the case, and which transfer reason values are in force**, so that **a case changes hands only for a person entitled to change it, a hold is placed only for a person entitled to place it, and nobody is told that a case exists when it is outside their scope**.

Inside `rwb-access` this is the authority and access side of legacy RWB-E1-021:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers behind the three operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`, and it adds no operation. `POST /cases/{caseId}/transfer` and `POST /cases/{caseId}/legal-hold` are the case service's operations (P3); this story is the answer they ask for before the handler runs.
- The right for a transfer is `QUEUE_AND_ALLOCATION` letter `U` with the default scope `TEAM`; the right for a legal hold, placed or lifted, is `CASE_RECORD` letter `U` with the caller's scope. A caller without the letter is refused 403 with MSG-P4-002 naming the action ("transfer the case", "place a legal hold", "lift a legal hold"); a case outside the scope is answered 404 with MSG-P4-003 and no case fact; a caller with no Workbench role is refused 401 with MSG-P4-001 before any case fact is read.
- The transfer reason list `LOV-TRANSFER-REASON` (`R01` to `R06`) is read through the reference-data contract of `rwb-case` (DP-07) as a list of values with the version in force. The reason is required by the case service and its value is not a right: no reason is a constant in code and this story never refuses a transfer for a reason.
- Everything that moves the case is RWB-P3-E1021-APP's and is out of scope here: the `TRANSFER` rule package and its evaluation, the eight triggers, the version lock, the assignment swap, the overflow queue, `CaseTransferred`, `legal_hold` and `status_before_hold`, and the skip of R-UNI-20. The rule packages are `rwb-decision`'s (P7), the document link of a `DocumentStored` trigger is `rwb-document`'s (P5), and the transfer surface the case service renders is P3's.
- No delegation of authority level applies to a transfer or a hold. The DoA table, `GET /doa-limits` and the approval-routing lookup are RWB-P4-E2013-APP's, and this story reads no `delegation_limit` row.
- The access log is a decision-record entry on `rwb.decision-record.v1`, written through the local library of DP-03: one `AC-READ` entry per granted authorise answer, one `AC-DENY` entry per refusal with no case fact, and the entry is written before the answer is returned (FEAT-ACA-07, FEAT-ACA-08).
- The service holds no `recovery_case`, `queue`, `assignment` or `rule_row` row: the case facts arrive in the authorise request from `rwb-case`, one hop, inside 2 s (DP-01, DP-11). The attribute set of an authorise request for a transfer or a hold, including `legalHold`, is Not specified in the source documents (GAP-0990; ASM-1738).

The legacy behaviour carried into the access service is unchanged: the same authorisation of the two calls of RWB-E1-021 section 12 (Queue and allocation right U with scope Team, Case record right U with the scope applied), the same refusal of a role without the right (X11, MSG-P4-002) before the handler runs, the same list of transfer reasons as data, and the same rule that a legal hold stops an automated transfer without changing who may read the case.

### 2. Business rationale

A case changes hands between the TDR, litigation, NPA and debt sale teams by e-mail today, and a case can wait between teams with nobody holding it. The transfer engine that ends that wait is P3's; what is missing on the access side is the answer in front of it: today the two calls are authorised inside a monolith against a shared table, so a role change, a team change or a new transfer reason needs a release, a case outside a person's scope is answered with a page that confirms the case exists, and nobody can say from one log who moved a case or who placed a hold on it. Under Architecture v5 each service authorises its own object against cached permission data from `rwb-access`, with a 2 s timeout (slide 14; slide 11), and the access answer plus its record are what the case service calls first.

This story supplies that answer for the transfer and the legal hold. It meets REQ-CWC-010 and REQ-CWC-016 on the access side, REQ-WKM-003 for the transfer reason list as data, and REQ-CWC-005 because the answer is the precondition of a move that keeps one queue and one open assignment; it supports the measure "rule and limit changes made without a code release" at 100 percent, because the letters, the scope values and the reason list are data read with their versions. The measure of success is that no transfer and no hold is carried out without a granted answer and one record of it, that a refusal never confirms a case, and that an approved matrix version changes the answer on the next call with no deployment.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix as data (legacy RWB-E1-037). This story implements the decision behind those operations for a transfer and a hold; it adds no operation |
| RWB-P3-E1021-CON | The published contract and fake of the case-side transfer and legal-hold calls: the request, the answer, the error shape and the reference to the reason list, as the P3 slice of this legacy key publishes them. Which attributes an authorise request for a transfer or a hold carries, including `legalHold`, is Not specified in the source documents (GAP-0990; ASM-1738) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-TRANSFER-REASON and LOV-SCOPE with the version in force (DP-07); `lov_value` stays P3's, and no reason code and no scope name is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case screen and its hold banner (DP-19); the route itself is the case service's story |

Business preconditions carried from RWB-E1-021, owned by other services where they say so:

- Permission matrix version `PM-2026.11` is in force and gives `QUEUE_AND_ALLOCATION` letter `U` to RW-TEAMMGR and RW-CAPACITY, `QUEUE_AND_ALLOCATION` letter `R` only to RW-CASEOWN, `CASE_RECORD` letter `U` to RW-LITOFF, and no `QUEUE_AND_ALLOCATION` letter to RW-LITOFF or RW-REFADM (legacy RWB-E1-021 sections 3, 10 and 12; FSD P4 A2.4 AC-ALT-P4-004-02). Which role holds `QUEUE_AND_ALLOCATION` `U` in the matrix as loaded is Not specified in the source documents (GAP-0990; ASM-1743), and the label of the matrix version in force at the release date is Not specified in the source documents (GAP-0990; ASM-1742).
- The transfer reason list LOV-TRANSFER-REASON holds R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue (DL23), and it is loaded and approved through the reference-data load path of P3 (RWB-E1-043).
- The `TRANSFER` package is approved and in force, the eight triggers are wired and the case service calls this answer first: all of it is RWB-P3-E1021-APP's, and this story reads none of its rows.
- The case screen SCR-03 and its hold banner exist (RWB-P3-E1023-APP, RWB-P3-E1021-APP).
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login (DP-02); the story says "the rwb-access login (DP-02)" and never the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None).

### 4. Flow

1. Caller: a person acts on the case screen or through the case service's own call: a team manager transfers a case with a reason, a capacity planner transfers a case, or a litigation officer or legal counsel places or lifts a legal hold.
2. Caller: the case service builds the authorise request from its own rows and calls `rwb-access` first. The request names the area (`QUEUE_AND_ALLOCATION` or `CASE_RECORD`), the right (`U`), the case reference, the action, and the object attributes the policy reads: the team and the owner of the case, and `legalHold`. The transfer call also presents the transfer reason code it will send. The full attribute set of a request, including `legalHold`, is Not specified in the source documents (GAP-0990; ASM-1738).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in. With no Recovery role the answer is 401 MSG-P4-001 and no case fact is read (BR6).
4. `rwb-access`, right check: reads `permission` for the caller's roles and the matrix version in force, `PM-2026.11`, and looks for the letter the area needs: `U` in `QUEUE_AND_ALLOCATION` for a transfer, `U` in `CASE_RECORD` for a hold placed or lifted. No letter gives a refusal, 403 with MSG-P4-002 naming the action, and no case fact (BR1).
5. `rwb-access`, scope check: the case is in scope when the attributes satisfy the caller's `default_scope` in force, read through the reference-data contract of DP-07: `TEAM` for a transfer, the caller's scope as applied for a hold. A case outside the scope is answered 404 with MSG-P4-003 and no case fact, so the answer never confirms that a case exists (BR2).
6. `rwb-access`, reason list: for a transfer, reads LOV-TRANSFER-REASON through DP-07 with the version in force and reports the presented reason code as a value of the list or not. The reason is a P3 requirement and is not a right: this step grants and withholds nothing, and a value outside the list is refused by the case service with MSG-P3-001 (BR3).
7. `rwb-access`, hold: while the case carries `legalHold` true, the answer for `CASE_RECORD` `R` to the roles in scope is unchanged and the transfer answer is unchanged; the skip of an automated transfer (R-UNI-20) is the case service's, and this story writes no skip (BR7).
8. `rwb-access`: writes the record through the library of DP-03 before the answer is returned: an `AC-READ` entry for a granted authorise answer with the case reference, the area, the right, the scope used and the matrix version in force; an `AC-DENY` entry for a refusal with the area, the right and the result, and no case fact (BR4, BR5).
9. `rwb-access`: returns the answer to the caller inside the 2 s timeout of DP-11. The answer carries the decision, the scope used, the matrix version in force, the letters held in the area, the action it answered, and for a transfer the reason list version and the membership of the presented code. It reads no `delegation_limit` row and names no DoA level (BR8).
10. `rwb-access`: caches the answer for the policy versions in force. A caller that asks again under the same versions is answered from the cache and reads no matrix row twice; the record is still written for that call (BR9).
11. Policy change: a new matrix version (`PM-2026.12`, which gives RW-LEGAL the letter `R` in Queue and allocation) is loaded and approved through the load path, `rwb-access` writes the rows and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`. Every caller drops its cached answer and the next call is answered under the new version, with no deployment (BR9).
12. Case service: with a granted answer it carries out the transfer or the hold and writes its own decision record with the rule ID and package version, or with the caller and the reason; with 403, 404 or 401 it refuses the call and shows the message, and the case keeps its queue, its owner and its hold state.

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no transfer and no hold is ever unlogged (BR4, BR5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's roles hold no `QUEUE_AND_ALLOCATION` `U` for a transfer, or no `CASE_RECORD` `U` for a hold | Refused before any case fact is read: 403 naming the action; one `AC-DENY` entry, no case fact | MSG-P4-002 | AC2, AC5 |
| X2 | The case is outside the caller's scope | Not found: 404 with no case fact; one `AC-DENY` entry, no case fact | MSG-P4-003 | AC3 |
| X3 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read and before any case fact is taken from the request; one refusal entry | MSG-P4-001 | AC4 |
| X4 | The decision record cannot be written | Nothing is returned: 503 with no case fact, nothing changes, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC8 |
| X5 | The LOV-TRANSFER-REASON list is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | BR3, BR9 |
| X6 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | BR6 |
| X7 | A trigger fires for a case on legal hold | The authority answer is unchanged: the roles in scope are still granted the read and the transfer answer is still given. The skip of the automated transfer is R-UNI-20 in RWB-P3-E1021-APP, and this story records no skip | None | AC5, BR7 |
| X8 | A caller asks about both areas in one call | The answer is per area and per right, and one record is written per area and right; no letter of one area admits the other | None | BR1, BR4 |
| X9 | The transfer reason presented is not a value of the list in force | The answer names the list version in force and reports the value as not a member of it; it withholds no right, because the reason is the case service's requirement (MSG-P3-001) | None | BR3 |

The answer for a hold uses the caller's scope as the role row carries it; a range answer with two matrix versions in force on the same day is not specified in the source documents (GAP-0990; ASM-1742); until it is, the version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P3-E1021-CON and the contract fake of the transfer and hold calls; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack (roles, letters, scopes, matrix version) and the reason list are data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | A case changes hands or goes on hold only for a person entitled to do it, a refusal never confirms a case, and every granted answer and every refusal is recorded once |
| Estimable | Two rights behind existing operations, one scope rule, one list read, one record path and one cache |
| Small | Fits one sprint with its tests; no screen, no rule evaluation, no workflow and no case change |
| Testable | Every owned criterion has a test case in section 16; the case side and the reference list are published fakes |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1, the authority side

  Background:
    Given the environment is SIT
    Given the service is rwb-access on base /api/recovery/access/v1 with schema rwb_access
    Given permission matrix version "PM-2026.11" is in force and gives QUEUE_AND_ALLOCATION "U" to RW-TEAMMGR and RW-CAPACITY, QUEUE_AND_ALLOCATION "R" only to RW-CASEOWN, CASE_RECORD "U" to RW-LITOFF and RW-LEGAL, CASE_RECORD "R" to RW-ENFORCE, and no QUEUE_AND_ALLOCATION and no CASE_RECORD right to RW-REFADM
    Given the default scope in force is "TEAM" for RW-TEAMMGR and "OWN" for RW-CASEOWN
    Given the transfer reason list "LOV-TRANSFER-REASON" with version "TRF-REASON-2026.11" holds R01, R02, R03, R04, R05 and R06
    Given the rwb-case contract mock returns case "RW-2026-000301" in queue "TDR-BKK-CO" in team "TDR-BKK", owned by "U-7401", with legal hold clear
    Given the rwb-case contract mock returns case "RW-2026-000307" in queue "SME-NTH-CO" in team "SME-NTH", owned by "U-7401", with legal hold clear
    Given the rwb-case contract mock returns case "RW-2026-000311" in queue "LIT-BKK-OFF" in team "LIT-BKK", owned by "U-7401", with legal hold clear, and the same case with legal hold true

  Scenario: AC1 A team manager of the case's team is granted the transfer answer (new, D-RCV-60)
    Given test user "U-7402" holds RW-TEAMMGR with default scope "TEAM" in team "TDR-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000301" in team "TDR-BKK" owned by "U-7401"
    When the caller asks POST /api/recovery/access/v1/authorise for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U", action "transfer the case" and transfer reason "R03"
    Then the answer is granted with scope "TEAM" under matrix version "PM-2026.11"
    Then the answer names the action "transfer the case" and the reason list version in force, and reports "R03" as a value of the list
    Then the answer carries no case fact other than the case reference, the area, the right and the scope it used
    Then one AC-READ decision record is written with the case reference, area "QUEUE_AND_ALLOCATION", right "U", scope "TEAM" and matrix version "PM-2026.11"
    Then the answer is returned inside the 2 s timeout of the one hop
    Then no delegation_limit row is read for the answer and the answer names no delegation level

  Scenario: AC2 A case owner with Queue and allocation R is refused the transfer (new, D-RCV-60)
    Given test user "U-7403" holds RW-CASEOWN with default scope "OWN" and QUEUE_AND_ALLOCATION "R" only
    Given test user "U-7403" owns case "RW-2026-000301"
    When "U-7403" asks for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U" and action "transfer the case"
    Then the answer is refused with status 403 and message MSG-P4-002 with action "transfer the case"
    Then no granted answer, no queue, no team and no owner is returned
    Then one AC-DENY decision record is written with area "QUEUE_AND_ALLOCATION", right "U" and result "REFUSED"

  Scenario: AC3 A case outside the caller's scope is answered not found (new, D-RCV-60)
    Given test user "U-7402" holds RW-TEAMMGR with default scope "TEAM" in team "TDR-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000307" in team "SME-NTH" owned by "U-7401"
    When "U-7402" asks for case "RW-2026-000307", area "QUEUE_AND_ALLOCATION", right "U" and action "transfer the case"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no case fact: no queue, no team and no owner
    Then one AC-DENY decision record is written with area "QUEUE_AND_ALLOCATION", right "U", result "REFUSED" and status 404

  Scenario: AC4 A caller with no Workbench role is refused before any case fact is read (new, D-RCV-60)
    Given test user "U-7404" holds no Recovery Workbench role
    When "U-7404" asks for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U" and action "transfer the case"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then no case fact is read from the request and the rwb-case contract mock is never called
    Then one AC-DENY decision record is written with no case fact

  Scenario: AC5 A litigation officer places and lifts a legal hold and the authority of the case is unchanged (new, D-RCV-60)
    Given test user "U-7405" holds RW-LITOFF with CASE_RECORD "U" and a case inside the scope its role row carries
    Given the rwb-case contract mock returns case "RW-2026-000311" in team "LIT-BKK" owned by "U-7401" with legal hold clear
    When "U-7405" asks for case "RW-2026-000311", area "CASE_RECORD", right "U" and action "place a legal hold"
    Then the answer is granted with the scope it used named in it and one AC-READ decision record is written
    When the rwb-case contract mock returns the same case with legal hold true
    Then the same caller is granted CASE_RECORD "U" again for the action "lift a legal hold"
    Then a caller holding RW-TEAMMGR of team "LIT-BKK" is still granted CASE_RECORD "R" and QUEUE_AND_ALLOCATION "U" on that case while legal hold is true
    Then the answer changes no case fact and names no paused authority

  Scenario: AC6 A refusal record carries no case fact (new, D-RCV-60)
    Given test user "U-7403" holds RW-CASEOWN with QUEUE_AND_ALLOCATION "R" only and owns case "RW-2026-000301"
    When "U-7403" asks for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U" and the answer is refused
    Then one AC-DENY decision record is written with area "QUEUE_AND_ALLOCATION", right "U" and result "REFUSED"
    Then the record carries no case ID, no queue, no team, no owner and no transfer reason value
    Then the record is written before the answer is returned

  Scenario: AC7 A policy version change reaches the answer with no deployment (new, D-RCV-60)
    Given test user "U-7406" holds RW-LEGAL, which has no QUEUE_AND_ALLOCATION row in "PM-2026.11"
    When "U-7406" asks for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U" and action "transfer the case"
    Then the answer is refused with status 403 and message MSG-P4-002 and it names matrix version "PM-2026.11"
    Then when "U-7406" asks the same question again inside one policy version
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then when matrix version "PM-2026.12" is approved with RW-LEGAL holding the letter "R" in Queue and allocation, and rwb.access.AccessPolicyChanged.v1 is published for it
    Then the next ask is answered under matrix version "PM-2026.12" with no deployment
    Then the answer names the letters "R" and still refuses the transfer with MSG-P4-002, because "R" is not the letter "U"
    Then the same caller's Queue and allocation "R" question is granted under "PM-2026.12"

  Scenario: AC8 An answer that cannot be recorded is not given (new, D-RCV-60)
    Given test user "U-7402" holds RW-TEAMMGR with default scope "TEAM" in team "TDR-BKK"
    Given the decision-record write is forced to fail
    When "U-7402" asks for case "RW-2026-000301", area "QUEUE_AND_ALLOCATION", right "U" and action "transfer the case"
    Then the call answers 503 with message MSG-P7-003 and no case fact
    Then no granted answer is returned and nothing changes: no queue, no owner and no hold state
    Then an incident is raised to the platform administrator queue
```

AC1 to AC8 are the criteria this story owns, and all eight are new under D-RCV-60 because the legacy key states its access behaviour as an exception path and a test case rather than as a criterion. In AC1 the answer proves the right, the scope and the reason list are read as data and that the answer carries no case fact. In AC2 the caller owns the case and is still refused: the scope never confers a right, which is the legacy X11 refusal and FSD P4 AC-ALT-P4-004-02. In AC3 the same manager is refused on a case of another team, and the 404 never confirms that the case exists. In AC4 the refusal happens before the policy and before any case fact, so an unauthenticated role learns nothing about any case. In AC5 the two `CASE_RECORD` `U` answers prove the hold call, and the third line proves that a hold changes no authority: the roles in scope still read the case and the transfer question is still answered, while the skip of R-UNI-20 stays with RWB-P3-E1021-APP. AC6 proves the audit side of a refusal: the entry exists and carries no case fact. AC7 proves the policy is data: the version label in the answer changes on the event, and the letter `R` is not silently read as `U`. AC8 proves the record-before-answer rule.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force: a transfer needs `QUEUE_AND_ALLOCATION` letter `U`, a hold placed or lifted needs `CASE_RECORD` letter `U`; a caller whose roles hold no such letter is refused 403 with MSG-P4-002 naming the action and no case fact | Legacy RWB-E1-021 sections 10 and 12; FSD P4 A2.4 VR-P4-004-1 and AC-ALT-P4-004-02; TSD P4 T6.1, T6.2; FEAT-ACA-04 |
| BR2 | A transfer is admitted by the scope `TEAM` and a hold by the caller's scope read from `default_scope`; a case outside the scope is answered 404 with MSG-P4-003 and no case fact | Legacy RWB-E1-021 section 12; FSD P4 A2.14 VR-P4-014-1 and AC-EXC-P4-004-01; LOV-SCOPE |
| BR3 | The transfer reason is a required value of LOV-TRANSFER-REASON read through DP-07 with the version in force; its value is not a right, no reason code is a constant, and a value outside the list is refused by the case service (MSG-P3-001) and not here | Legacy RWB-E1-021 sections 3, 5 and 13; REQ-WKM-003; DL23; DP-07 |
| BR4 | Every granted authorise answer writes one `AC-READ` decision record with the case reference, the area, the right, the scope used and the matrix version in force, before the answer is returned | FSD P4 A2.7 AC-P4-007-01; FSD P4 A2.8; FEAT-ACA-07; FEAT-ACA-08; DP-03 |
| BR5 | Every refusal writes one `AC-DENY` decision record with the area, the right and the result, and carries no case fact | FSD P4 A2.7 AC-EXC-P4-007-04; FEAT-ACA-07; DP-03 |
| BR6 | A refusal comes before any case fact is read: no Recovery role answers 401 with MSG-P4-001, no right answers 403 with MSG-P4-002, and a case outside the scope answers 404 with MSG-P4-003 without confirming that it exists | FSD P4 A2.1 VR-P4-001-1, A2.4 VR-P4-004-1, A2.14 VR-P4-014-1; legacy RWB-E1-021 X11 |
| BR7 | A legal hold neither pauses nor widens the authority of the case: while `legal_hold` is true the roles in scope still read the case and the transfer answer is still given; the skip of an automated transfer is R-UNI-20 in RWB-P3-E1021-APP | Legacy RWB-E1-021 BR6, BR7 and section 9; R-UNI-20, R-UNI-21 |
| BR8 | No delegation of authority level applies to a transfer or a hold: the answer reads no `delegation_limit` row and names no DoA level; the DoA table and its lookup are RWB-P4-E2013-APP's | Legacy RWB-E1-021 section 12 (authorization of the two calls); TSD P4 T3.1 (`delegation_limit`); ownership map |
| BR9 | An answer is cached for the policy versions in force and dropped when `rwb.access.AccessPolicyChanged.v1` is written, so a policy change reaches the next call with no deployment; an unavailable reference list is no answer at all | Architecture v5 slides 14 and 43; FSD P4 AC-P4-004-01; DP-07; DP-11 |
| BR10 | Role codes, area names, letters, scope values and the reason list are data: the roles and letters in `rwb_access`, the scope and reason lists through DP-07; no business value is written in code | FSD P4 BR-P4-004, BR-P4-005; TSD P4 T3.2; principle 1 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are held as the five-character field of TSD P4 T3.1, and the answer names the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; `OWN`, `TEAM`, `REGION` and `ALL` are list values, never Java constants. Which attribute names a request must carry, including `legalHold`, is Not specified in the source documents (GAP-0990; ASM-1738).
- BR3 is a read of LOV-TRANSFER-REASON with its version, and the answer reports membership rather than granting a right; a reason code appears in this service only as a value read from the list.
- BR4 and BR5 are the same `RecordAndApply` transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and changes nothing (X4).
- BR6 is the order of the checks in `TransferAuthorityService` (role, right, scope, hold, list) and the reason no refusal ever echoes a case fact.
- BR7 is visible in the code review: `legalHold` is an input to the answer and to no branch that narrows a `CASE_RECORD` read, and no status, no queue and no owner is written here.
- BR8 is the absence of any `delegation_limit` read in this module; a review that finds one is a defect of this story.
- BR9 is a cache keyed by the matrix version in force; the `AccessPolicyChanged` entry that drops it is published by the same transaction that writes the new policy rows.
- BR10 is visible in the code review: no role code, area name, scope name, reason code or version string appears in a constant.

### 9. State transitions

None for a case. This story changes no status, no queue, no owner, no `legal_hold` and no `status_before_hold`: a transfer moves a case inside RWB-P3-E1021-APP, a hold is placed and lifted there, and both are carried by the workflow that owns the case (Temporal and Drools design; Architecture v5 slides 42 and 44). This story runs no workflow of its own, owns no Schedule and evaluates no rule.

The only states this story has are the states of its answer, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds the letter in the area and the case is in scope | The granted answer with the scope used, the matrix version in force, the letters held, the action, and for a transfer the reason list version and the membership of the presented code | `AC-READ` |
| Refused, no right | No role of the caller holds `QUEUE_AND_ALLOCATION` `U` for a transfer or `CASE_RECORD` `U` for a hold | 403 MSG-P4-002 naming the action, no case fact | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope | 404 MSG-P4-003, no case fact | `AC-DENY` |
| Not answered | The record cannot be written, or the reason list cannot be read | 503 with MSG-P7-003 or MSG-GEN-006, no case fact, nothing changes | None for MSG-P7-003; the failure is raised as an incident |

A hold has no state of its own in this story: the `legal_hold` flag of the case is P3's, and this story reads it from the request on every call, so placing and lifting a hold changes no cached answer and needs no call between the services.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | `QUEUE_AND_ALLOCATION` `U` with default scope `TEAM`: granted the transfer answer for a case of its team; refused for a case of another team |
| RW-CAPACITY, capacity and workforce planner | `QUEUE_AND_ALLOCATION` `U`: granted the transfer answer inside its scope |
| RW-LITOFF, litigation officer | `CASE_RECORD` `U` with the caller's scope: granted the answer to place and to lift a legal hold on a case in scope |
| RW-LEGAL, legal counsel | `CASE_RECORD` `U`: granted the hold answer inside its scope; its `QUEUE_AND_ALLOCATION` letter is whatever the matrix version in force says, and under `PM-2026.12` the letter `R` is not the letter `U` |
| RW-ENFORCE, enforcement owner | `CASE_RECORD` `R`: reads the case, and is refused the hold answer with MSG-P4-002 because `R` is not `U` |
| RW-CASEOWN, case owner | `QUEUE_AND_ALLOCATION` `R` only: reads the queue and allocation facts, and is refused the transfer answer with MSG-P4-002 even for a case it owns |
| RW-AUDIT, internal audit | Reads the access log and the decision records; this story grants it no transfer and no hold right of its own |
| RW-REFADM, reference data administrator | No `QUEUE_AND_ALLOCATION` and no `CASE_RECORD` letter: refused with MSG-P4-002; loads the reason list through the reference-data load path of P3 and writes no row of this service |
| SY-CASEWF, case workflow module | Asks the same question for the workflow's own transfers with `QUEUE_AND_ALLOCATION` `CRU`; the roles of the service identity are checked as a person's are |
| SY-RULES, Drools evaluator | Evaluates the `TRANSFER` package in `rwb-decision`; it asks nothing of this story and this story reads no rule row |

Reading and answering is the whole of this story: it grants or refuses, records the answer and returns. It changes no case, no queue, no assignment, no hold, no policy row and no rule. A policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and a break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service. No delegation of authority level applies to a transfer or to a hold: `delegation_limit` is not read here, and the DoA table, `GET /doa-limits` and the approval-routing lookup are RWB-P4-E2013-APP's.

The database login is per service (DP-02) and is the rwb-access login of the service contract; the story refers to "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-044 | `role`, `permission` | role id, role_code, role_name, role_class, default_scope and entra_group; permission id, role_id, capability_area, letters and matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read by `GET /masking-policies` only; a transfer or a hold answer carries no personal field |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X6) |
| DF-REF-027 to DF-REF-033 | `lov_value` | the LOV-TRANSFER-REASON values R01 to R06 with their labels, sort order and valid_from, and the LOV-SCOPE values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case reference, actions, scope and matrix version, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The case facts of a request — the case reference, its queue, its team, its owner and `legalHold` — are read from the request and never from a table: `recovery_case`, `queue`, `assignment`, `rule_row`, `legal_hold` and `status_before_hold` are P3's and P7's, and no foreign key and no query crosses a schema (DP-01). Those six names are never named by a statement in this story: the case is moved, held, locked, assigned, queued and versioned in RWB-P3-E1021-APP, and the `TRANSFER` rows are read in `rwb-decision`. Which attributes a request must carry is Not specified in the source documents (GAP-0990; ASM-1738).

No personal value enters the answer, the record or the event: the answer carries a case reference, an area, a right, a scope, a matrix version and reason codes, and the `AC-DENY` entry carries the area, the right and the result only (NFR-039, NFR-040). Field IDs are those in the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The right, the scope, the reason list membership and the answer for one area, right, case and action. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003, MSG-GEN-006) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the matrix version and the scope of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the fields it covers for the caller's roles; a transfer and a hold answer carry no personal field |

`GET /doa-limits` is the same service's operation and is not used here: the delegation of authority table and its routing lookup are RWB-P4-E2013-APP's, and no delegation level applies to a transfer or a hold.

#### 12.2 REST operations consumed

None. The case facts arrive in the authorise request, built by the caller from its own rows; this story calls no service at run time and opens no call of its own. The shape it expects is the one RWB-P3-E1021-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build. The reason list is read through the reference-data client library and contract of DP-07 (RWB-PLT-E1043-CON, RWB-P3-E1043-CON) that the service already holds behind RWB-P4-E1037-CON, and it is held with the policy versions in force.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, roles), the version label, the valid-from date and the change reference |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value: the `AC-READ` record carries a case reference, an area, a right, a scope and a matrix version, the `AC-DENY` record carries the area, the right and the result, and the policy event carries version labels. `rwb.access.DoALimitChanged.v1` belongs to the delegation slice and is not published here.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh). The transfer and deviation events of the case (`CaseStateChanged`, `RouteDecided`, `TimerDue`, `DeviationRaised`, `DeviationCleared`, `ApprovalRequested`, `DocumentStored`, `PaymentMissed`) are P3's and P5's and are not consumed here.

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. The transfer and the hold are carried out inside the workflow that owns the case (Temporal and Drools design; Architecture v5 slides 42 and 44); this story answers one REST call in front of it.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service, and its story is RWB-P4-AD008-APP. This story starts no Schedule and reads no job row.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The `QUEUE_AND_ALLOCATION` and `CASE_RECORD` letters and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The masking rows behind `GET /masking-policies`; not used by an answer of this story |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-TRANSFER-REASON and LOV-SCOPE, read through the contract; not owned here |
| `delegation_limit` | P4 (`rwb_access`) | Not read in this story; no DoA level applies to a transfer or a hold |

No table of `rwb_case`, `rwb_decision` or `rwb_source_data` is read: the case, the queue, the assignment, the hold, the rule rows and the customer fields stay with their owners, and the only facts of them that enter this service are the identifiers and attributes carried by a request (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case transfer and hold WireMock | RWB-P3-E1021-CON | Case "RW-2026-000301" in queue TDR-BKK-CO in team TDR-BKK, owner "U-7401", legal hold clear; case "RW-2026-000307" in team SME-NTH; case "RW-2026-000311" in team LIT-BKK with legal hold clear and the same case with legal hold true |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X4 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.11 in force, the later PM-2026.12 for AC7, and the roles, letters and scopes of the background |
| reference-data fake | RWB-P3-E1043-CON | LOV-TRANSFER-REASON with version TRF-REASON-2026.11 and the six values, LOV-SCOPE with the version in force, and the unavailable list of X5 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the case facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output, and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/transfer`, Java package `th.co.scb.ace.workbench.recovery.access.transfer`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the reason the service answers from the attributes it is given: `recovery_case`, `queue`, `assignment` and `rule_row` are P3's and P7's, so the answer is built from a case reference and the request attributes and never from a joined query. DP-03 is the access log: a granted answer is an `AC-READ` and a refusal an `AC-DENY`, so the transfer question and the decision question are answered from one log. DP-04 is recorded because the legacy key evaluates package `TRANSFER` with first-match semantics: in the target that evaluation is RWB-P3-E1021-APP's, inside `rwb-case`, with the rule rows in `rwb-decision`; this story reads no rule row and evaluates no package. DP-05 is recorded and not used: no `v_ace_*` field is read, because a transfer and a hold carry a case reference and no customer value. DP-07 supplies LOV-TRANSFER-REASON and LOV-SCOPE with the version in force, because `lov_value` stays with P3 under the ownership map; no reason code and no scope name is a Java constant. DP-09 is the outbox of the policy event and the record, and the inbox of the policy listener. DP-10 is recorded because the legacy key carries the timer events JOB-05 and the decision-log write of JOB-13: in the target no job of this key runs from a shared Quartz table, the case timers are durable timers of the workflow that owns the case, and this story adds no job. DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it. DP-13, DP-14 and DP-15 are the naming and migration conventions of the service. DP-19 is the route that renders the answer: SCR-03 Case record and its hold banner belong to RWB-P3-E1023-APP and RWB-P3-E1021-APP, and this story supplies only the grant, the refusal and the records.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| TransferAuthorityService | Service | Right, scope, hold and reason list for one request, in that order; one answer, one record |
| RightResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters per area |
| ScopeRule | Service | Compares the attributes of the request with the `default_scope` value in force; `TEAM` for a transfer |
| ReasonListReader | Service | Reads LOV-TRANSFER-REASON through the client of DP-07 with the version in force and answers membership; no constant |
| HoldAuthorityService | Service | The `CASE_RECORD` `U` answer for a hold placed or lifted; it neither narrows nor widens the read of a case on hold |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer per policy version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new policy version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V1021_1__transfer_authority_path.sql` adds `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)`, so the letter read of an answer is an index read inside the 2 s budget of DP-11; no column is added and no table is created.
- The policy rows are versioned by `matrix_version` and the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).

**Configuration and reference data**

- The matrix version in force is data: the latest `valid_from` on or before the business date, read from `permission.matrix_version`. The version label in force at the release date is Not specified in the source documents (GAP-0990; ASM-1742); this story reads the label and never names one in code.
- LOV-TRANSFER-REASON (R01 to R06; DL23) and LOV-SCOPE (OWN, TEAM, REGION, ALL) through the reference-data contract of DP-07 (RWB-P3-E1043-CON).
- Which role holds `QUEUE_AND_ALLOCATION` `U` is a row of the matrix and not a rule of this story; that the rows are RW-TEAMMGR and RW-CAPACITY is Not specified in the source documents for the matrix as loaded (GAP-0990; ASM-1743).
- No parameter row, no timeout constant and no role code in code: the 2 s is the platform standard of the RWB-PLT-E1037-CON client, and the cache lives for the policy version in force (BR9).

**Build steps**

1. `RightResolver` over `permission` and `role` for the two areas and the letter `U`, with the matrix version named in the answer; tests for AC1 and AC2, and a test that a letter added by a new version is accepted as data.
2. `ScopeRule` for scope `TEAM` on a transfer and the caller's scope on a hold; tests for AC1, AC3 and AC5.
3. `ReasonListReader` over the DP-07 client with the version in force and the membership answer; test AC1 and the absent-list path X5.
4. `HoldAuthorityService` with `legalHold` in and a read answer that does not narrow; tests for AC5 with the hold clear and the hold true.
5. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer and the forced failure of X4; tests TC-E1-021-16 and AC6.
6. The denial path with the refusal shape and no case fact (401, 403, 404); tests TC-E1-021-15, AC2, AC3 and AC4.
7. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test AC7 against the PM-2026.12 fixture.
8. The migration of the index, a timing test that one answer stays inside the 2 s budget on a loaded policy pack, and the contract-fake run of the whole capability against RWB-P3-E1021-CON and the decision-record fake, so the story builds before the case side exists in the environment.

**Feature switch.** `rwb.p4.transfer-hold-authority`, read from the platform feature-flag library under the R-PREC default ruling. Off: the answer for `QUEUE_AND_ALLOCATION` `U` and `CASE_RECORD` `U` is a refusal with MSG-P4-002 whatever the matrix says, so no transfer and no hold is granted while every other area and right, the masking answer and the access log are unchanged. The switch narrows and never widens a right, needs no schema rollback, and blocks no read of a case that the policy allows.

**Done when.** The tests in section 16 pass; a team manager of the case's team is granted the transfer answer with its scope and the reason list version, a case owner with the letter `R` and a caller outside the scope are refused with no case fact, a caller with no role is refused before any case fact is read, a litigation officer is granted the hold answer to place and to lift it and a hold changes no authority, every granted answer leaves one `AC-READ` entry and every refusal one `AC-DENY` entry with no case fact, an approved matrix version changes the answer with no deployment, and an answer that cannot be recorded is not given.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer (X3) |
| MSG-P4-002 | No role of the caller holds the right in the area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 (X1); {action} is "transfer the case", "place a legal hold" or "lift a legal hold" |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR2 (X2) |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X6) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X4) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Your request is queued and will be retried. | This story, on the LOV-TRANSFER-REASON read of X5 |

For MSG-P4-002 the {action} value is the action the caller attempted, one of "transfer the case", "place a legal hold" and "lift a legal hold"; for MSG-P4-003 no case fact is echoed, because the message must not confirm that a case exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10. A missing or unknown transfer reason is MSG-P3-001 and is produced by the case service, not here.

### 15. Screens and states

This story builds no screen. SCR-03 Case record, its hold banner, its history and its route are RWB-P3-E1023-APP and RWB-P3-E1021-APP through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), and the transfer screen of Epic 2 is not part of this wave.

What this story decides for the screen is what each answer state allows:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Transfer, granted | The transfer control is offered and the case service carries the move out; the queue, the owner and the history lines are P3's |
| SCR-03 Case record | Transfer, refused | The page shows MSG-P4-002 with the action "transfer the case" and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Case not found | The page shows MSG-P4-003 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | On hold for a legal hold | The hold banner is P3's; the answer still grants the read to the roles in scope and still answers the transfer question, and the skip of an automated transfer is P3's |
| SCR-03 Case record | Hold placed or lifted, granted | The case service applies the status change and its own record; this story has written its `AC-READ` entry before the answer |
| SCR-03 Case record | Not available | The page shows MSG-P7-003 where the record could not be written, or MSG-GEN-006 where the reason list could not be read, and no case fact |

A screen that offers the transfer control because a client cached a grant is a defect of the screen, not of the answer: the answer always names the matrix version it used, and a control is offered only where the letters of that version say so.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-15 | AC2, AC6, BR1, BR5 | Component | RW-CASEOWN "U-7403" with `QUEUE_AND_ALLOCATION` letter "R" only calls the transfer path for case RW-2026-000301; refused 403 MSG-P4-002 with action "transfer the case" and one `AC-DENY` entry with area QUEUE_AND_ALLOCATION, right U and no case fact |
| TC-E1-021-01 | AC1 is this story's; here owned by RWB-P3-E1021-APP (the TRANSFER package and the owner choice) | Component | Case RW-2026-000301 in TDR-BKK-CO, route R4 approved, package TRANSFER "TRF-2026.11" |
| TC-E1-021-02 | Owned by RWB-P3-E1021-APP (the manual transfer call and its reason) | Component | Manual transfer of case RW-2026-000302 with reason code MANUAL and transfer reason R03 |
| TC-E1-021-03 | Owned by RWB-P3-E1021-APP (the version lock and the second refusal) | Component | Two transfers on record version 7 to LIT-BKK-OFF and DIL-BKK-CO |
| TC-E1-021-04 | Owned by RWB-P3-E1021-APP (the eight triggers) | Component | Eight TRANSFER rules, TRF-001 to TRF-009, case RW-2026-000304 |
| TC-E1-021-05 | AC5, BR1, BR7 | Component | The two rights behind the reassign, the hold and the lift: RW-TEAMMGR "U-7402" with QUEUE_AND_ALLOCATION U on case RW-2026-000301, and RW-LITOFF "U-7405" with CASE_RECORD U placing and lifting a hold on case RW-2026-000311, with legal hold true leaving the authority unchanged |
| TC-E1-021-06 | Owned by RWB-P3-E1021-APP (the missing reason, MSG-P3-001) | Component | Transfer of case RW-2026-000306 with no transfer reason |
| TC-E1-021-07 | Owned by RWB-P3-E1021-APP (the caseload cap) | Component | Owner "U-7407" at 150 open cases, case RW-2026-000307 |
| TC-E1-021-08 | Owned by RWB-P3-E1021-APP (a closed case) | Component | Case RW-2026-000308 in status CLOSED |
| TC-E1-021-09 | Owned by RWB-P3-E1021-APP (the transfer decision record of a manual call) | Component | Transfer decision record store down for a manual call on case RW-2026-000309 |
| TC-E1-021-10 | Owned by RWB-P3-E1021-APP (the skip of R-UNI-20) | Component | Case RW-2026-000310 with legal_hold true and a TimerDue that matches TRF-003 |
| TC-E1-021-11 | Owned by RWB-P3-E1021-APP (idempotency of a trigger event) | Component | PaymentMissed with event ID EVT-88120 twice for case RW-2026-000311 |
| TC-E1-021-12 | Owned by RWB-P3-E1021-APP (the overflow queue) | Component | Every member of LIT-BKK-OFF at 150, rule TRF-007, case RW-2026-000312 |
| TC-E1-021-13 | Owned by RWB-P3-E1021-APP (a hold on a case on hold) | Component | Case RW-2026-000313 in status ON_HOLD with a legal hold |
| TC-E1-021-14 | Owned by RWB-P3-E1021-APP with RWB-P7-E1021-APP (no rule matches) | Component | DocumentStored with no matching TRANSFER rule for case RW-2026-000314 |
| TC-E1-021-16 | AC8, BR4, BR5 | NFR | The decision-record write forced to fail during a granted transfer authorise for case RW-2026-000301; the call answers 503 MSG-P7-003, nothing changes, an incident is raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level Access maps to Component, System maps to Component where the case-side assertion is stubbed by RWB-P3-E1021-CON, and Resilience maps to NFR. TC-E1-021-15 is the access case of the legacy key and is a criterion of this story; TC-E1-021-05 answers the two rights behind the reassign, the hold and the lift calls; TC-E1-021-16 answers the record failure. The other thirteen test cases of the key are listed for traceability and are owned by RWB-P3-E1021-APP with the slice named in the Covers column. No `-ITG` copy sits in this story: the integration copy of this key is RWB-ITG-E1021-ITG.

### 17. Guardrails

- No business value in code: role codes, area names, letters, scope values, reason codes, the matrix version and the reason list version are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR10).
- No personal data in logs, events, the record or the tests. The answer carries a case reference, an area, a right, a scope and version labels; the `AC-DENY` entry carries the area and the right only; test data is synthetic and staff appear as user references.
- No cross-schema read (DP-01): `recovery_case`, `queue`, `assignment`, `rule_row`, `delegation_limit`, `decision_log_entry` and the `v_ace_*` views are never queried; the case facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories of this service write a role or a permission row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no case fact and raises an incident, so no transfer and no hold is unlogged (BR4, BR5).
- Default deny: with no letter in the area the answer is a refusal, and with no covering policy row or version the answer is a refusal or no answer at all, never a guessed grant.
- The hold does not widen a right: `legal_hold` true changes no letter and no scope in this service, and the only effect it has on a move (the skip of R-UNI-20) is RWB-P3-E1021-APP's.
- No rule evaluation here: this story loads no `TRANSFER` package, reads no `rule_row` and passes no fact to `RuleEvaluator`; the package, its versions and its approval are P7's.
- The feature switch changes one rule and no schema, and it never widens a right: off turns the two `U` answers into refusals and leaves every other decision as it was.
- The service never calls another service at run time and never chains a call: the answer is one hop and one transaction with its record.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-E1-021-15, TC-E1-021-05 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-E1-021-16, TC-E1-021-15 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | None named in the sources | All recovery processes | LOV-TRANSFER-REASON (DL23) | TC-E1-021-05, TC-E1-021-15 |
| REQ-CWC-005 | The case state model covers stage, status within stage, route and the deviation flags X1 to X7, and a case holds exactly one state at a time | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-01 | All recovery processes | None | TC-E1-021-15, TC-E1-021-16 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1021-CON | CON | The published contract and fake of the case-side transfer and legal-hold calls this story gates: the request, the answer, the error shape and the reference to the reason list. Metadata C; it never blocks the build |
| RWB-P3-E1021-APP | APP | The owner of every effect of a transfer and a hold: the `TRANSFER` package, the eight triggers, the version lock, the assignment swap, the overflow queue, `CaseTransferred`, `legal_hold`, `status_before_hold` and the skip of R-UNI-20. This story supplies the answer it calls first |
| RWB-P4-E1037-CON | CON | The wave-1 service contract of `rwb-access`: the three operations this story implements, the policy pack and the answer shape, on base `/api/recovery/access/v1` |
| RWB-PLT-E1037-CON | CON | The platform authorise client and guard library whose 2 s timeout, cache and problem responses the answer holds inside |
| RWB-P4-E2013-APP | APP | The delegation of authority table and the approval-routing lookup; no delegation level applies to a transfer or a hold, and this story reads no `delegation_limit` row |
| RWB-P5-E1021-APP | APP | The document link of a `DocumentStored` trigger; not read here |
| RWB-P7-E1021-APP | APP | The `TRANSFER` rule package registry, its versions and `RulePackageInForce` in `rwb-decision`; this story evaluates no rule row |
| RWB-S8-E1021-APP | APP | The deviation role in a transfer trigger (`DeviationRaised`, `DeviationCleared`); not read here |
| RWB-ITG-E1021-ITG | ITG | The integration harness copy that proves the real cross-service behaviour end to end, including the transfer and the hold |

| Legacy reference | Where it is kept |
|---|---|
| The authorization of the two calls: Queue and allocation right U with scope Team, Case record right U with the scope applied | Sections 1, 8, 10, 12, 14 |
| The transfer reason list R01 to R06 (LOV-TRANSFER-REASON) as data | Sections 1, 3, 4, 7, 8, 11, 13 |
| The refusal of a role without the right (MSG-P4-002) and the out-of-scope answer (MSG-P4-003) | Sections 4, 5, 7, 8, 14 |
| The legal hold that stops an automated transfer (R-UNI-20) and the status it paused in (R-UNI-21), owned by RWB-P3-E1021-APP | Sections 1, 5, 8, 9, 19 |
| The record of every transfer and every hold: the access entry here, the transfer decision record in P3 | Sections 1, 4, 8, 11, 12 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Legacy key RWB-E1-021, story RWB-P4-E1021-APP, contracts RWB-P3-E1021-CON and RWB-P4-E1037-CON | Metadata, sections 3 and 12 |

### 19. Out of scope

- The rwb-case slice of this legacy key, RWB-P3-E1021-APP and its contract RWB-P3-E1021-CON: the two case paths `POST /cases/{caseId}/transfer` and `POST /cases/{caseId}/legal-hold`, their request and answer bodies, the version lock, the assignment swap and the decision record of a transfer.
- The eight triggers and the engine: stage change, route decided, timer expired, deviation raised, deviation cleared, approval needed, document received and payment missed, the `TransferTrigger` fact, first-match evaluation, the no-match case and the skip of R-UNI-20.
- The `TRANSFER` rule package, its versions, its approval, its promotion and `RulePackageInForce`: RWB-P7-E1021-APP and the rule registry of `rwb-decision`.
- The document link of a `DocumentStored` trigger: RWB-P5-E1021-APP.
- The deviation role in `DeviationRaised` and `DeviationCleared`: RWB-S8-E1021-APP.
- The overflow queue, the caseload cap and the reallocation of an owner's cases (RWB-P4-E1020-APP and RWB-P3-E1021-APP).
- The integration harness copy of the tests of this key: RWB-ITG-E1021-ITG.
- Loading, approving and rolling back the permission matrix and the reason list: the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table, its lookup and `GET /doa-limits`: RWB-P4-E2013-APP and RWB-P4-E2014-APP, and `rwb.access.DoALimitChanged.v1`.
- Break-glass access, its incident reference, its ceiling and its review (the wave-1 stories of this service).
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other job, workflow and Schedule of this service.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
