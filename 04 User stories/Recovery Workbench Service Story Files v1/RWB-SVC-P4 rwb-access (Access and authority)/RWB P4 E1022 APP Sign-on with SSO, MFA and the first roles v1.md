# RWB-P4-E1022-APP Sign-on with SSO, MFA and the first roles

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E1-022 for rwb-access — the sign-in resolver, the access check and the first roles of the ACE Common sign-in, inside the service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E1022-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1019-CON |
| Integration dependencies | None |
| External dependencies | RWB-P4-E1022-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-001, FR-P4-002, FR-P4-003, FR-P4-004, FR-P4-006, FR-P4-007, FR-P4-019, FR-P4-033, FR-P4-035, FR-P4-037) |
| Status | Draft (realignment v1) |

### 1. Story

As a **case owner (RW-CASEOWN) and the service identities the Workbench calls (SY-RULES)**, I want **my Entra ID sign-in and its second factor turned inside rwb-access into a resolved set of roles, scope and policy versions, every call checked against that set before the handler runs, and an unmapped, inactive or conflicting group refused at the door**, so that **access is controlled from the first release, every service reads one authority instead of a copy of the roles, and nobody holds a Workbench password or a local account**.

This is the application slice of legacy RWB-E1-022 for rwb-access, and it is the authority half of that key. The legacy story resolved the session, checked the right and wrote the sign-in fact in one process against one schema; D-RCV-60 keeps the behaviour and separates the ownership:

- **This story, rwb-access (P4), schema `rwb_access`:** the session resolver over the verified claims, the group-to-role mapping on the active `role` rows, the conflict check over `role_conflict`, the letter union over `permission`, the two answers the rest of the platform uses — `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions` — and the refusal facts with their reason codes (DP-01, DP-08).
- **Not this story, the contract of the same key:** RWB-P4-E1022-CON publishes the two operations, their shapes, their error vocabulary and their fakes. This story implements them and adds no path.
- **Not this story, the schema of the same key:** RWB-P4-E1022-DB creates `role`, `permission` and `role_conflict` in `rwb_access`, the library objects and the login. This story reads `permission` and writes none of the three tables at run time.
- **Not this story, legacy AC1 and legacy AC3:** the SSO sign-in across the edge and the "no group at all" refusal are carried by **RWB-ITG-E1022-ITG**, which owns those two criteria and their end-to-end form. This story owns legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9.
- **Not this story, the lead time:** there is no Workbench password, no local account, no session table and no token store in the service. Staff sign-in is ACE Common (Entra ID, MFA) at the shared gateway-bff, and the session lives in the Redis store of gateway-bff (RWB-PLT-N006-INF; ADR-010).
- **Service naming:** base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1`, task queue `rwb-access` in namespace `rwb-recovery` (not used here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **Events:** this story publishes no event and consumes none. A policy change is published by the story that loads a policy version, not by the resolver that reads it.

### 2. Business rationale

Access to recovery data today is granted system by system, and the bank cannot show who could see a case on a given date. The legacy story made Entra ID group membership the only way to hold a Workbench role: one group per role per environment, granted through the bank IAM, read at each sign-in and turned into a session with roles, scope and the permission matrix version in force. That answer is still right, and the realignment makes it narrower and stronger by moving the resolution into the service that owns the roles.

There is one change of substance and it is the point of the split. In the monolith the resolver read `role`, `permission` and `role_conflict` in the same connection, kept a `SessionContext` object for the life of the process session, and every module called `AccessCheck` in the same JVM. In the 19-service target the roles are read by **every** service and by gateway-bff, each of which must authorise its own object (Architecture v5 slide 10), while the tables stay with one owner (DP-01). So the resolution becomes an answer of rwb-access over two published operations, and the session itself belongs to the shared edge: gateway-bff holds it in Redis, P4 holds no session table, and what travels is identifiers and version labels, never a token and never business data (ADR-010; slide 35). Three sentences of the architecture are what this story must make true: each service authorises the object itself with cached permission data from rwb-access and a 2 s timeout (slide 10); the access owner publishes `authorise` and `me/permissions` and writes `AccessPolicyChanged` when a policy version changes (slide 14); personal data stays in the owning service and never travels in an event, a workflow payload or a log (slides 11 and 35).

The negative side is fixed as tightly as the positive one. An unmapped or inactive group gives no role; a conflicting pair refuses the session; the matrix and conflict versions a session resolved stay with it until it ends; a service identity is checked exactly like a person; and no value the resolver needs — a letter, a scope, a group name, a conflict pair — is written in code (legacy BR1 to BR8, kept unchanged). It meets REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 and supports control CTL-09 (access by role and scope). The measure is unchanged from the legacy story, the access test set of section 16 passing for every role with real users at the release (DL39: administration roles at Epic 1), and additionally the guard of every consuming service passing its contract test against these two answers.

**The division is fixed and is the same in every story of this legacy key.** The seven criteria of this story — legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9 — are carried here word for word with their origin tag; legacy AC1 (SSO sign-in end to end) and legacy AC3 (not in any group) are **not** this story's; they are carried by RWB-ITG-E1022-ITG, and this story copies no part of them as a scenario of its own.

Where the sources do not fix a value this story must build on, it carries the placeholder: the home of the resolved version labels now that P4 keeps no session table, the target of the incident that a conflicting pair raises, and the operation that returns a person's team and region codes for the scope line — Not specified in the source documents (GAP-0775; ASM-1398), (GAP-0775; ASM-1399) and (GAP-0775; ASM-1401).

### 3. Preconditions

- RWB-P4-E1022-CON is published (this story's build dependency, H): `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions` with their shapes, their error vocabulary and their fakes. This story adds no path and no payload field.
- RWB-P4-E1022-DB has created `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044) and `role_conflict` (DF-REF-205 to DF-REF-211) in `rwb_access`, with the partial index on `role.entra_group` where `is_active` (DP-15; tracked as the external dependency of the same key).
- RWB-P4-E1037-CON is published (C): the role-to-permission and masking contract that publishes `GET /api/recovery/access/v1/admin/roles` and `GET /api/recovery/access/v1/me/session` for the role catalogue and the session line. Those two legacy reads are that contract's and are not republished here; this story answers the two operations of its own contract only.
- RWB-PLT-E1037-CON is published (H): the guard library contract that every consuming service binds; the authorise answer of this story is what that guard calls, and the two stories are tested against each other's fakes.
- RWB-PLT-E1027-CON is published (H): the local decision-record library and the topic `rwb.decision-record.v1`, through which the sign-in and refusal facts reach the access log (DP-03). The writer itself is RWB-P4-E1039-APP.
- RWB-PLT-E1043-CON is published and RWB-P3-E1043-CON is the contract behind it (H, C): `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` are read with the version in force through the reference-data contract (DP-07). `LOV-SCOPE` holds OWN, TEAM, REGION and ALL; `LOV-CAPABILITY` holds the 14 areas, including PLATFORM_ADMINISTRATION.
- RWB-PLT-N001-CON is published (H): the gateway-bff route contract. gateway-bff is the only entry for staff, it holds the session in its Redis store, and it hands the verified claims to this service (DP-19; RWB-PLT-N006-INF).
- RWB-PLT-E1044-CON is published (H): the per-service Flyway sequence. This story writes no migration; the schema is RWB-P4-E1022-DB's.
- Permission matrix version `PM-2026.11` is in force from 30 November 2026 and separation of duty version `SOD-2026.11` is in force. In `PM-2026.11`, RW-PHONECOL holds `-` in Platform administration and RW-CASEOWN holds `R` in the areas its menu shows.
- The role rows of the environment are loaded by the role story of this service, and each environment's row carries that environment's group name in `role.entra_group`, for example `RWB-SIT-RW-CASEOWN` in SIT (legacy precondition, names DL40). The mapping rows are `role.entra_group` data of this service; their maintenance contract is RWB-P4-AD001-CON.
- RWB-P3-E1019-CON is published (C): the roles, teams and queues contract of rwb-case, from which the team and region codes of a TEAM or REGION scope are read. This story builds against its fake from Day 1 (DP-11) and copies no team row into `rwb_access`.
- The ACE Common sign-in is configured for the Workbench application in Entra ID (INT-21), with the bank conditional access policy that requires a second factor. The verified claims reach this service from gateway-bff, never directly from the browser.
- The test users, groups, roles and matrix rows of this story are synthetic; no production entitlement, person or credential is read, written or logged.
- No approval is required to build against a Draft contract: the contract is Draft (realignment v1) and the shapes are frozen when the consuming services pass their contract tests.

### 4. Flow

1. The person opens the Workbench in the ACE front end. gateway-bff redirects to Entra ID through ACE Common sign-in; the person signs in with password and second factor, and Entra ID returns an OpenID Connect token with the `groups` claim and the `amr` claim.
2. gateway-bff verifies the token, stores the session in its Redis store with the identifiers and the version labels it is given, and calls this service for the resolution. The token and the session never reach this service's database (ADR-010).
3. `SessionResolver` checks that the `amr` claim contains `mfa`. Without it the session is refused and nothing is resolved (legacy X3, AC4).
4. `SessionResolver` maps each value of the `groups` claim to an active `role` row on `role.entra_group`, through the partial index on the column. A group with no active row is ignored and its name is carried on the sign-in fact, as a group name only and never as a person's attribute (legacy X6, AC8; GAP-0775; ASM-1400).
5. `SessionResolver` reads `role_conflict` at the conflict version in force and refuses the session where the resolved set holds both halves of a pair. The refusal names the pair and raises the incident (legacy X4, AC6).
6. `SessionResolver` resolves the session: the user reference, the role codes with their names and default scopes, the matrix version in force, the conflict version in force, the scope type and the team and region codes read through the rwb-case contract. The version labels are what the session keeps until it ends (legacy X7, AC9; ASM-1398).
7. The resolved identifiers and version labels are handed back to gateway-bff for its session record; this service writes no session row and no token anywhere.
8. gateway-bff renders the first screen with one line naming the roles and the scope, for example "Case owner. Scope: own cases.", and a menu holding only the screens whose capability area has R for at least one role. That rendering is the edge's and its contract is RWB-PLT-N001-CON; this story supplies the answer it renders.
9. The person, or another service on the person's behalf, calls an endpoint. The guard of that service calls `POST /api/recovery/access/v1/authorise` with the role set, the scope, the capability area and the right the endpoint declares, one hop, 2 s timeout, breaker per downstream.
10. `AccessCheckService` unions the letters of the session's roles in that area and answers ALLOWED or REFUSED. A refusal is 403 with MSG-P4-002 and the refusal fact carries the user reference, the area, the right and the result; the handler of the caller never runs.
11. A service identity is resolved and checked exactly like a person: its group maps to its non-human role row and its call is refused on the same rule as a human call (legacy X5, AC7).
12. A caller reads its own set on `GET /api/recovery/access/v1/me/permissions`: the roles, the letters per area, the scope, the matrix version and the conflict version it is being checked against.
13. Every sign-in and every refusal is passed to the access-entry writer of RWB-P4-E1039-APP with its reason code — NO_ROLE, NO_MFA, ROLE_CONFLICT or NO_RIGHT — and that writer records it locally and publishes it to `rwb.decision-record.v1` (DP-03; ASM-1402).
14. The reference-data contract of rwb-case is unreachable, times out or answers malformed: the resolution fails closed with 503, nothing is cached, and no letter is assumed. The call is counted as a fail-closed resolution.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an endpoint, for example the admin API | Refused with 403 before the handler runs; the refusal fact carries the area and the right | MSG-P4-002 | AC2 |
| X2 | The person is in no Workbench group | Session refused with 401; the access request page shows the message and no data. Carried by RWB-ITG-E1022-ITG, not by this story | MSG-P4-001 | legacy AC3 (RWB-ITG-E1022-ITG) |
| X3 | The token has no second factor in the `amr` claim | Session refused with 401; the refusal is recorded with reason NO_MFA | MSG-P4-005 | AC4 |
| X4 | The groups give a role pair listed in the conflict table version in force | Session refused with MSG-P4-006 naming the pair; the incident is raised; the refusal is recorded with reason ROLE_CONFLICT | MSG-P4-006 | AC6 |
| X5 | A service identity calls an area its role does not hold | Refused with 403, exactly as for a person, with the identity reference on the refusal fact | MSG-P4-002 | AC7 |
| X6 | A group maps to no active role row, or to an inactive one | The group is ignored and its name is written on the sign-in fact; if no group maps, the no-role path applies | None on the ignored group | AC8 |
| X7 | A new matrix version takes effect while a session is open | The open session keeps the version it resolved; the next session resolves the new one | None | AC9 |
| X8 | The verified claims arrive after the session has ended, or with no session reference | Refused with 401 and no resolution; the service resolves nothing for a session the edge does not hold | MSG-P4-001 | AC2 |
| X9 | The reference-data contract of rwb-case is unreachable, times out or answers malformed | The resolution fails closed with 503; no letter and no scope is assumed, nothing is cached, and the failure carries no business data | None | AC9 |
| X10 | The `permission` rows of the matrix version in force hold no row for an area | The area answers with no letter for every role, so every action in it is refused | MSG-P4-002 | AC2 |

No exception path of this story changes a case, a task or a queue: this service answers roles, scope and rights, and the case state machine is rwb-case's. X2 remains the property of RWB-ITG-E1022-ITG and appears here only so that the table of the legacy story is not silently narrowed.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against its own contract, the guard library contract, the reference-data fake and the rwb-case team contract fake; no other service has to be finished first |
| Negotiable | The role roster, the group names, the letters, the conflict pairs and the versions are data rows; the story fixes the resolution, the two answers and the refusal rules only |
| Valuable | Every service and the edge get one authority for who may do what, and a person with an unmapped, inactive or conflicting group is stopped at the door |
| Estimable | One resolver, one check service, two answers, one conflict check, one refusal path and the fixtures |
| Small | Fits one sprint with its tests, with the schema and the contract built by the sibling stories of the same key |
| Testable | Every criterion in section 7 is one automated test over synthetic role rows, a session fake and a reference-data fake |

### 7. Acceptance criteria

```gherkin
Feature: Sign-on with SSO, MFA and the first roles

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force from 30 November 2026
    Given separation of duty version "SOD-2026.11" is in force
    Given role RW-CASEOWN has entra_group "RWB-SIT-RW-CASEOWN" and default scope "OWN"
    Given the rwb-case reference-data contract mock returns the reference values in force
    Given every role, group and test user of this story is synthetic

  Scenario: AC2 Role denied (legacy RWB-E1-022 AC2)
    Given the gateway-bff session contract mock returns the verified claims of test user "U-1002", who holds only RW-PHONECOL, whose Platform administration letter is "-"
    When the user calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002 with action "read roles"
    Then the system writes one refusal event with user "U-1002", area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED"

  Scenario: AC4 Sign-in without a second factor is refused (legacy RWB-E1-022 AC4)
    Given the gateway-bff session contract mock returns the verified claims of test user "U-1004" in group "RWB-SIT-RW-CASEOWN"
    Given the token's amr claim holds "pwd" and not "mfa"
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005
    Then the system writes one refusal event with reason "NO_MFA"

  Scenario: AC5 Two roles give the permissions of both (legacy RWB-E1-022 AC5)
    Given the gateway-bff session contract mock returns the verified claims of test user "U-1005" in groups "RWB-SIT-RW-LITOFF" and "RWB-SIT-RW-LEGAL"
    When the user signs in
    Then the session holds roles "RW-LITOFF" and "RW-LEGAL"
    Then the Documents letters are "CRUA", the union of "CRU" and "CRUA"
    Then no permission comes from any role the user does not hold

  Scenario: AC6 A conflicting role pair is refused (legacy RWB-E1-022 AC6)
    Given the gateway-bff session contract mock returns the verified claims of test user "U-1006" in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN"
    Given the role conflict table says RW-SECADM may not hold any business role
    When the user signs in
    Then the system refuses the session with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN"
    Then the system raises an incident to the security administrator queue
    Then the system writes one refusal event with reason "ROLE_CONFLICT"

  Scenario: AC7 A service identity is checked like a person (legacy RWB-E1-022 AC7)
    Given the gateway-bff session contract mock returns the verified workload claims of managed identity "SY-RULES" in group "RWB-SIT-SY-RULES"
    When it calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then the system writes one refusal event with user "SY-RULES"

  Scenario: AC8 An unmapped or inactive group gives no role (legacy RWB-E1-022 AC8)
    Given the gateway-bff session contract mock returns the verified claims of test user "U-1008" in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01"
    Given no active role row has entra_group "RWB-SIT-LEGACY01"
    When the user signs in
    Then the session holds only "RW-CASEOWN"
    Then the system writes the unmapped group name on the sign-in event

  Scenario: AC9 An open session keeps the versions it resolved (legacy RWB-E1-022 AC9)
    Given test user "U-1009" signed in at 09:00 on 1 December 2026 under matrix version "PM-2026.11"
    Given matrix version "PM-2026.12" takes effect at 10:00 on 1 December 2026 and removes R in Reporting from RW-CASEOWN
    When the user calls GET /reports/measures at 10:30 in the same session
    Then the system checks the call against "PM-2026.11" and allowed
    Then after the user signs in again at 11:00 the same call is refused with MSG-P4-002
```

These seven criteria are the legacy criteria of RWB-E1-022 unchanged, each tagged with its origin. The first Given of each is the boundary a service test has to fake — the verified claims that gateway-bff hands over, or the reference values that rwb-case supplies — and every value the legacy line carries is kept. Legacy AC1 and legacy AC3 are not scenarios of this story: they are carried by RWB-ITG-E1022-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role. The Workbench holds no password and no local account | role.entra_group (DF-REF-039); DT07; Admin and access model, section 4.2 |
| BR2 | A session is refused unless the token carries a second factor | NFR-049; FEAT-ACA-02 |
| BR3 | No role inherits from another. A person with two roles holds the union of both roles' letters | permission.letters (DF-REF-043) |
| BR4 | A capability area with no letter for any of the session's roles refuses every action in that area | Permission matrix; CTL-09 |
| BR5 | A role pair listed in the role conflict table may not be held in one session | Separation of duty sheet, roles.txt; role conflict table (new) |
| BR6 | A service identity holds a role in the same table and is checked the same way as a person | REQ-ACA-010; NFR-051 |
| BR7 | A session keeps the matrix and conflict versions it resolved at sign-in until it ends | Admin and access model, section 4.2 |
| BR8 | Group names, roles, letters and conflicts are data rows with a version; none is written in code | Principle 1; DT02 |
| BR9 | The answer is one hop with a 2 s timeout and a breaker per downstream, and a reference contract that cannot be reached refuses the resolution instead of assuming a value | Architecture v5 slides 10 and 11; DP-11 |
| BR10 | An unmapped or inactive group gives no role, and the group name is written on the sign-in fact as a name only, never as a person's attribute | Legacy X6 and BR1; Architecture v5 slide 35 |
| BR11 | The service holds no session, no token and no local account, and a fact it records carries an identifier, an area, a right and a reason code, never a name, a contact value or a credential | ADR-010; Architecture v5 slides 11 and 35 |
| BR12 | The role rows, the letters and the conflict pairs are read in `rwb_access`; the reference values are read through the rwb-case contract and the team codes through the roles-and-teams contract, and nothing is copied | DP-01, DP-07; ownership map |

### 9. State transitions

No case status changes in this story. It resolves a session with the states RESOLVED and REFUSED, and it records the refusal reason as a value of the fact:

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Session resolution | UNRESOLVED | The `amr` claim holds `mfa`, at least one group maps to an active role row and no conflicting pair is held | RESOLVED | The role set, the scope and the matrix and conflict versions are answered and kept for the session |
| Session resolution | UNRESOLVED | The `amr` claim holds no `mfa` | REFUSED (NO_MFA) | 401 with MSG-P4-005; no role is resolved |
| Session resolution | UNRESOLVED | No group maps to an active role row | REFUSED (NO_ROLE) | 401 with MSG-P4-001; carried by RWB-ITG-E1022-ITG |
| Session resolution | UNRESOLVED | The resolved set holds both halves of a conflicting pair | REFUSED (ROLE_CONFLICT) | MSG-P4-006 naming the pair, the incident raised, no role answered |
| Access decision | UNCHECKED | The letter of the area holds the right the endpoint declares | ALLOWED | The caller's handler runs |
| Access decision | UNCHECKED | The letter of the area does not hold the right, or the area has no row | REFUSED (NO_RIGHT) | 403 with MSG-P4-002; the caller's handler does not run |
| Access decision | UNCHECKED | The reference contract cannot be reached, times out or answers malformed | FAIL_CLOSED | 503; nothing is assumed and nothing is cached |
| Resolved version | PM-2026.11 | A new matrix version takes effect while the session is open | PM-2026.11 until the session ends | The open session keeps its labels; the next resolution reads PM-2026.12 |

A REFUSED resolution is final for that token: a second attempt needs a new sign-in, and the resolver holds nothing of the first attempt.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Line manager (bank IAM, level 4) | Requests a Workbench role for a team member in the bank IAM, naming the person, the role and the reason. May not approve the request they raised |
| Role owner (bank IAM, level 2), the head of the unit whose staff hold the role | Approves or rejects each grant of a role they own after checking the separation of duty table |
| Access administrator (bank IAM, level 3), Chief Debt Recovery Management Office (assumed, DL01) | Adds the person to the Entra ID group of the approved role in each environment requested. Approves no grant |
| Application owner (level 1), Tribe Lead of the Collections and Recovery Tribe (assumed, DL02) | Approves the roles table and each group to role mapping |
| RW-SECADM Security administrator | Maintains the Entra ID groups and the IAM link (DL40); owns the role-to-group mapping rows and their maintenance contract RWB-P4-AD001-CON; receives the conflict incident in AC6 |
| RW-REFADM Reference data administrator | Loads an approved role or group mapping version. Approves none |
| RW-CASEOWN and every bank role | Signs in and uses the screens of the role |
| RW-PHONECOL Phone collector | Signs in; refused on Platform administration (AC2) |
| SY-RULES and the other service identities | Act under their managed identity and their own role row, checked exactly as a person |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the role catalogue on the contract of RWB-P4-E1037-CON (Platform administration R) |
| The ACE DB team and the platform edge team | Own the schema, the login and the session store; this story writes none of them |

The four administration levels act in the bank IAM, not in the Workbench. If the bank chooses central administration (DL01), level 3 moves to the central IAM team and nothing in this build changes.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | role (P4 rwb-access) | id | Read |
| DF-REF-035 | role (P4 rwb-access) | role_code | Read |
| DF-REF-036 | role (P4 rwb-access) | role_name | Read |
| DF-REF-037 | role (P4 rwb-access) | role_class | Read |
| DF-REF-038 | role (P4 rwb-access) | default_scope | Read |
| DF-REF-039 | role (P4 rwb-access) | entra_group | Read |
| DF-REF-040 | permission (P4 rwb-access) | id | Read |
| DF-REF-041 | permission (P4 rwb-access) | role_id | Read |
| DF-REF-042 | permission (P4 rwb-access) | capability_area | Read |
| DF-REF-043 | permission (P4 rwb-access) | letters | Read |
| DF-REF-044 | permission (P4 rwb-access) | matrix_version | Read |
| DF-REF-205 to DF-REF-211 | role_conflict (P4 rwb-access) | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read |
| Session claim (no field ID) | The verified claims handed over by gateway-bff | the `groups` claim, the `amr` claim, the user reference | Read in memory only; never stored, never logged with a value |
| Team and region of the caller (no field ID) | The roles-and-teams contract of rwb-case (P3) | team code, region code | Read through the contract for a TEAM or REGION scope; no local row |

Field IDs are those in the Logical Data Model and Data Dictionary. `permission` is read only by this story: the permission matrix is loaded by RWB-P4-E1037-APP and this story writes none of the three tables at run time. The session claim has no field ID in any source because the target keeps no session object of this service's own (GAP-0775; ASM-1398). No personal value is read by this story: the resolver works on group names, role codes, letters and version labels.

### 12. Contract

#### 12.1 REST operations provided

| Method and path | Published by | Use in this story |
|---|---|---|
| POST /api/recovery/access/v1/authorise | RWB-P4-E1022-CON | The guard of a consuming service and the edge ask whether a session may take the action, in the area and with the right the endpoint declares |
| GET /api/recovery/access/v1/me/permissions | RWB-P4-E1022-CON | A caller reads the roles, the letters per capability area, the scope and the matrix and conflict versions its own session is checked against |

The two paths sit at the base of §R4 and DP-13, because Architecture v5 slide 14 names the operations and the Ownership Map has no path row for either; the derivation of the base is the contract's, and its open point is stated in RWB-P4-E1022-CON section 12.1. The legacy reads `GET /admin/roles` and `GET /me/session` are not republished here: the catalogue and the session line belong to the role-to-permission contract RWB-P4-E1037-CON, and AC2 and AC7 exercise the refusal before the handler rather than the catalogue itself.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | P3 rwb-case | The values of `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` in force, read through the reference-data contract behind RWB-PLT-E1043-CON (DP-07; C RWB-P3-E1043-CON) |
| The roles-and-teams read of the rwb-case contract | P3 rwb-case | The team and region codes of a TEAM or REGION scope, read through RWB-P3-E1019-CON and its fake (DP-11; C RWB-P3-E1019-CON) |
| ACE Common sign-in, group-to-role (INT-21) | ACE Common, through gateway-bff | The verified claims and the group-to-role read of the sign-in; the service never calls Entra ID directly and holds no token |

Every call is one hop with a 2 s timeout and a breaker per downstream (DP-11; ADR-020). The team and region read is the one operation the sources do not name: Not specified in the source documents (GAP-0775; ASM-1401).

#### 12.3 Events published

None. This story publishes no event and owns no topic. The policy events `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` on `rwb.access.events.v1` are published by the stories that load a policy version, not by the resolver.

#### 12.4 Events consumed

None. The resolver holds no cache of a policy version, so there is nothing to invalidate: every answer is read at the version in force at the moment of the call.

#### 12.5 Workflows and activities

None. The resolution, the check and the two answers are synchronous request handling in this service; no workflow, activity or task queue is used, and the task queue `rwb-access` is not started by this story.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of this service and belongs to the access-review story, not to the resolver.

#### 12.7 Tables owned

| Table | Owner (ownership map) | This story |
|---|---|---|
| role | P4 | Read only. Created by RWB-P4-E1022-DB, written by the role story RWB-P4-E1019-APP |
| permission | P4 | Read only. Created by RWB-P4-E1022-DB, written by RWB-P4-E1037-APP |
| role_conflict | P4 | Read only. Created by RWB-P4-E1022-DB, written by the role story RWB-P4-E1019-APP |
| lov_value | P3 | Not read by SQL: the values are read through the reference-data contract of rwb-case (DP-07) |
| queue, queue_member | P3 | Not read: the team and region codes come through the rwb-case contract, never from its tables (DP-01) |

No table of another service is named in a statement of this story, and the boundary test of the service fails on a cross-schema reference.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Session fake | The verified claims gateway-bff hands over (RWB-PLT-N001-CON) | A token with `amr` holding `mfa`; a token with `amr` holding `pwd` only; a workload token for SY-RULES; a set of groups with one unmapped group; an expired session reference (AC2, AC4, AC5, AC6, AC7, AC8) |
| Reference-data fake | `GET /api/recovery/case/v1/admin/lists/{listCode}` behind RWB-P3-E1043-CON | The values of `PM-2026.11` and of `PM-2026.12`, and an unreachable and a malformed answer (AC2, AC9) |
| Roles-and-teams fake | The rwb-case roles-and-teams read behind RWB-P3-E1019-CON | Team and region codes for the TEAM and REGION scopes (AC9) |
| Role fixture | The `role`, `permission` and `role_conflict` rows of the schema | RW-CASEOWN with `RWB-SIT-RW-CASEOWN` and scope OWN; RW-PHONECOL with `-` in Platform administration; RW-LITOFF and RW-LEGAL with CRU and CRUA in Documents; RW-SECADM with any business role; one inactive role row; `SOD-2026.11` with the pair of AC6 (AC2, AC5, AC6, AC8, AC9) |
| Access-entry fake | The writer of RWB-P4-E1039-APP | A recorder of the reason code, the user reference, the area and the right, and a switch that fails the write (AC2, AC4, AC6, AC7) |

The fakes are the ones this story builds against; the fakes of its own contract are published by RWB-P4-E1022-CON.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 | 2 | The authorise and permission answers are provided; the rwb-case reference values and team codes are consumed, one hop each |
| Kafka | 0 | 0 | No event is published or consumed by the resolver |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.access` for the implementation, with the published shapes of the two operations in `th.co.scb.ace.workbench.recovery.access.api`. The front end is not part of this service: the shell, the session line and the menu filter are gateway-bff's composite route (DP-19; RWB-PLT-N001-CON).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. `role`, `permission` and `role_conflict` are `rwb_access` tables and this story reads them in its own schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The sign-in and refusal facts are recorded locally by the access-entry writer of RWB-P4-E1039-APP; the dependency is carried here | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The role classes, the capability areas and the scope codes are read with the version in force and copied nowhere | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. This story is the authorise answer that the guard library calls, and the two are tested against each other's fakes | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The rwb-case reference read and the team read each get their own breaker | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The two operations are published at `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. This story writes no migration; the schema is RWB-P4-E1022-DB's on that sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The one-line roles and scope banner, the menu filter and the access request page are the edge's, not this service's | H RWB-PLT-N001-CON |

**Hardware and software change.** The monolith's `SessionResolver`, `AccessCheckService`, `AccessCheckInterceptor` and `AccessEventPublisher` inside `recovery.access.signin` become one service that answers two published operations, and the `SessionContext` object of the monolith becomes an answer plus the version labels the shared edge keeps in its Redis session record. The roles, the letters and the conflict pairs leave the monolith's single schema and stay in `rwb_access`; the reference values and the team codes are asked of rwb-case one hop away and are copied nowhere. No new hardware is implied: the service runs on the existing AKS cluster, the Redis session store is part of gateway-bff (RWB-PLT-N006-INF), and the resolver adds no database, no topic, no Schedule and no bucket.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessDecisionController` | Controller | Serves the two operations of section 12.1 and maps a refusal to an RFC 9457 problem detail with its message id (BR9) |
| `SessionResolver` | Service | Checks the `amr` claim, maps groups to active role rows on `role.entra_group`, applies the conflict check and resolves the role set, the scope and the version labels (BR1, BR2, BR5, BR7) |
| `AccessCheckService` | Service | Unions the letters of the session's roles in the area and answers ALLOWED or REFUSED with the area and the right (BR3, BR4) |
| `AccessCheckInterceptor` | Service | Reads the `x-capability` area and right declared on each endpoint of this service and refuses before the handler runs; an endpoint with no declaration fails the build (BR4, BR9) |
| `PolicyVersionSnapshot` | Value type | The role set, the scope type, the team and region codes, the matrix version and the conflict version of one resolution; what the edge keeps and what the answer carries (BR7) |
| `RoleConflict` | Entity | Maps `role_conflict` and answers whether two role codes of the resolved set form a pair at the version in force (BR5) |
| `AccessRepository` | Repository | Reads `role` on the partial index of `entra_group` where active, `permission` and `role_conflict` in `rwb_access`; writes nothing (BR12) |
| `AccessEntryClient` | Service | Passes the sign-in and refusal facts with their reason code to the writer of RWB-P4-E1039-APP (BR11) |
| `FailClosedPolicy` | Component | The 2 s timeout, the breaker and the 503 mapping of the reference read, with no assumed letter and nothing cached (BR9) |

**Configuration.** `rwb.access.required-amr=mfa` (legacy) and the timeout and breaker settings, read through the parameters client (DP-06 is not in this story's pattern set, so the two values are configuration of the service template). Group names, roles, letters, scopes and conflicts are never constants: they are rows. The scope line wording follows the labels of DL10.

**Build steps**

1. Implement `SessionResolver` over the session fake: the `amr` check and the group mapping on active rows through the partial index; test AC4 and AC8, including the inactive row and the group name on the sign-in fact.
2. Implement the conflict check over `role_conflict` at the version in force and the refusal with the pair named; test AC6, with a pair that is not a conflict at the version in force allowed.
3. Implement the letter union and `AccessCheckService`; test AC5 with CRU and CRUA in Documents and the dash in Platform administration, and test BR4 for an area with no row.
4. Implement the resolution snapshot: the role set, the scope, the team and region codes from the roles-and-teams fake, the matrix and conflict versions; test AC9 with `PM-2026.11` and `PM-2026.12` one hour apart.
5. Implement the two answers of section 12.1 against the shapes of RWB-P4-E1022-CON, and the contract test that compares them with the published document.
6. Implement `AccessCheckInterceptor` and the declared area and right; the contract test that every operation of this service declares one, and the refusal of AC2 and AC7 before the handler.
7. Implement `AccessEntryClient` over the fake of RWB-P4-E1039-APP and the reason codes NO_ROLE, NO_MFA, ROLE_CONFLICT and NO_RIGHT; test one refusal of each kind (AC2, AC4, AC6, AC7).
8. Wire the fail-closed path of the reference read and the team read: unreachable, timeout at 2 s and malformed each answer 503 with nothing cached and no business data in the body (BR9).
9. Prove that no statement of the package names a table of another schema, no log line carries a claim value, and no session, token or password column exists in `rwb_access` (BR11, BR12).

**Feature flag.** `rwb.access.sso-roles` (legacy). Off, the resolver refuses every resolution with 503 rather than answering from a stale set, so a switch-off never opens an unchecked path.

**Done when.** The tests in section 16 pass, a test user per Epic 1 administration role resolves with MFA in SIT, the contract test finds no endpoint of this service without a declared area and right, and the guard library of RWB-PLT-E1037-APP passes its contract test against the two answers.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-005 | Token without a second factor (new) | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Conflicting role pair at sign-in (new) | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-GEN-006 | ACE sign-in service unavailable | {system} is not available. Your request is queued and will be retried. |

The message ids and the wording are copied unchanged from RWB-E1-022, and the Thai text of each follows DL10; the proposed Thai for the two new messages is in the additions file of the legacy story. MSG-P4-001 appears here because the no-role path is a reason code of this service even though its end-to-end criterion is RWB-ITG-E1022-ITG's. The 503 fail-closed answer carries no message id and no business data: one RFC 9457 problem detail with the trace identifier and the operation.

### 15. Screens and states

No screen of this story. What a person sees is the edge's rendering of the answers: the one-line roles and scope at the top of every page, the menu with only the entries whose capability area the session can read, and the access request page with MSG-P4-001 and no data. Those are gateway-bff composite screens under RWB-PLT-N001-CON, and the legacy `SessionBanner` and `AccessRequestPage` components are not built in this service. Epic 1 has no business screens (DL39); RW-CASEOWN test users exist in SIT and UAT only, and the full administration screens SCR-43 and SCR-47 arrive in Epic 8.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-022-02 | AC2 (legacy RWB-E1-022 AC2), BR4 | Component | Test user holding RW-PHONECOL only; the session fake and the role fixture of `PM-2026.11`; the refusal recorded with user, area, right and result |
| TC-E1-022-04 | AC4 (legacy RWB-E1-022 AC4), BR2 | Component | A token with `amr` holding `pwd` only; the refusal reason NO_MFA |
| TC-E1-022-05 | AC5 (legacy RWB-E1-022 AC5), BR3 | Component | Test user in the RW-LITOFF and RW-LEGAL groups; Documents letters CRU and CRUA and the union CRUA |
| TC-E1-022-06 | AC6 (legacy RWB-E1-022 AC6), BR5 | Component | Test user in the RW-SECADM and RW-CASEOWN groups; `SOD-2026.11` holding the pair; the incident and the refusal reason ROLE_CONFLICT |
| TC-E1-022-07 | AC7 (legacy RWB-E1-022 AC7), BR6 | Component | Managed identity SY-RULES with its non-human role row; the refusal of GET /admin/roles with MSG-P4-002 |
| TC-E1-022-08 | AC8 (legacy RWB-E1-022 AC8), BR8 | Component | One mapped and one unmapped group; one inactive role row; the unmapped group name on the sign-in fact |
| TC-E1-022-09 | AC9 (legacy RWB-E1-022 AC9), BR7 | Component | Matrix versions PM-2026.11 and PM-2026.12 with effective times one hour apart; one session held across the change |
| TC-E1-022-10 | Access (legacy RWB-E1-022 TC-E1-022-10), BR4 | Component | A role without the right is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The two legacy test cases whose only criteria are legacy AC1 and legacy AC3 — TC-E1-022-01 and TC-E1-022-03 — are executed at the integration slice and are named in section 18.

### 17. Guardrails

- No business value in code: group names, roles, letters, scopes and conflicts are read from tables with their version.
- No personal data in logs, tests or prompts: a sign-in or refusal fact carries the Entra ID object reference, never the person's name or e-mail, and a claim value is never logged.
- ACE data only through the owner's contract or a `v_ace_*` view read by the data owner; this service reads no ACE view and no table in `public`.
- No read of another service's tables: the reference values and the team codes arrive over the rwb-case contract, one hop, never by SQL (DP-01).
- No local password, local account, session table, token or role cache that outlives the session (ADR-010).
- Every endpoint of this service declares its capability area and right; an endpoint without one fails the contract test.
- Deny by default and fail closed: an unreachable or malformed reference read refuses the resolution and assumes no letter.
- No place name, no person name and no credential in a fixture or a runbook; every role, group and user of the tests is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-001 | Single sign-on through Entra ID with MFA | Epic 1, 3.4 | FEAT-ACA-01, FEAT-ACA-02 | All recovery processes | BR1, BR2, BR9 | TC-E1-022-04 |
| REQ-ACA-002 | Roles as data, changed without a code release | Epic 1, 3.4 | FEAT-ACA-03 | All recovery processes | BR3, BR7, BR8 | TC-E1-022-05, TC-E1-022-08, TC-E1-022-09 |
| REQ-ACA-010 | Service identities under the same role checks | Epic 1, 3.4 | FEAT-ACA-02 | All recovery processes | BR4, BR5, BR6, BR10 | TC-E1-022-02, TC-E1-022-06, TC-E1-022-07, TC-E1-022-10 |
| Legacy TC-E1-022-01, TC-E1-022-02, TC-E1-022-03, TC-E1-022-04, TC-E1-022-05, TC-E1-022-06, TC-E1-022-07, TC-E1-022-08, TC-E1-022-09, TC-E1-022-10 | The ten legacy test cases of RWB-E1-022, at component and end-to-end level | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-01, FEAT-ACA-02, FEAT-ACA-03 | All recovery processes | BR1 to BR12 | Executed by RWB-P4-E1022-APP and RWB-ITG-E1022-ITG |

The ten legacy test cases of RWB-E1-022 are executed by this story and by RWB-ITG-E1022-ITG: the eight whose criteria this story owns run here against the session and reference fakes, and TC-E1-022-01 and TC-E1-022-03 run at the integration slice because their criteria — legacy AC1 and legacy AC3 — are **not** this story's. Legacy AC1 and legacy AC3 are carried by RWB-ITG-E1022-ITG, and this story copies no part of them as a scenario of its own.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1022-CON | Contract | H: publishes the two operations, their shapes and their fakes that this story implements |
| RWB-P4-E1022-DB | ACE DB | X: creates `role`, `permission`, `role_conflict`, the library objects and the login in `rwb_access` |
| RWB-P4-E1037-CON | Contract | C: the role-to-permission contract that publishes the legacy `GET /admin/roles` and `GET /me/session` reads |
| RWB-PLT-E1037-CON | Contract | H: the guard library whose contract test consumes the authorise answer of this story |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the refusal facts are recorded through |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data client and the rwb-case contract behind it, for the role classes, areas and scopes |
| RWB-PLT-N001-CON, RWB-PLT-N006-INF | Contract, Infrastructure | H and the session store: the edge that holds the session and renders the answers of this story |
| RWB-P3-E1019-CON | Contract | C: the roles-and-teams contract that answers the team and region codes of a TEAM or REGION scope |
| RWB-ITG-E1022-ITG | Integration | Owns legacy AC1 and legacy AC3 and the end-to-end form of all ten legacy criteria |
| RWB-P4-AD001-CON | Contract | The maintenance contract of the role-to-group mapping rows this story reads |

### 19. Out of scope

- The contract of the two operations, their payloads and their fakes: RWB-P4-E1022-CON.
- The schema, the tables, the library objects and the login: RWB-P4-E1022-DB.
- The permission matrix load, PDPA masking, scope filtering and leaver handling: RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- Writing access events into the decision log and break-glass: RWB-P4-E1039-APP.
- The role-to-group mapping maintenance operations: RWB-P4-AD001-APP and RWB-P4-AD001-CON.
- The delegation of authority table and the `GET /doa-limits` read: RWB-P4-E1038-APP.
- Partner identities through the external gateway: RWB-P4-E2019-APP.
- The end-to-end SSO sign-in and the no-group refusal across the edge: RWB-ITG-E1022-ITG.
- Full administration screens for roles and access, SCR-43 (Epic 8, FEAT-ADM-01).
- The request, approval and grant steps themselves, which run in the bank IAM, not in the Workbench.
