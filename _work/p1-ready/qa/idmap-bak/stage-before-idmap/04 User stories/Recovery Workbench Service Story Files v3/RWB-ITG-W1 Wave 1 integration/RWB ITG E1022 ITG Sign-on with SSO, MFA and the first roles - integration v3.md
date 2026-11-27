# RWB-ITG-E1022-ITG Sign-on with SSO, MFA and the first roles

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1022-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Small; fits two weeks; the squad confirms it at refinement (DOR-RWB-ITG-E1022-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | Contract story keys: Not specified in the source documents (DOR-RWB-ITG-E1022-ITG-21) |
| Contract version | Recovery Workbench API Specification v5, version 5.0.0: rwb-access.yaml, rwb-case.yaml and rwb-source-data.yaml (`/v1` base paths) |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P3-E1019-APP, RWB-P4-E1022-APP (builds not yet done; each deployed in SIT before the run) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-ACA-001, REQ-ACA-002, REQ-ACA-010) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-022 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 9 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; finishing pass.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that one Entra sign-in through the ACE common module yields one short-lived user JWT that gateway-bff carries to rwb-access (P4), rwb-case (P3) and rwb-source-data (P1) on the same session**, so that **the group-to-role mapping held as one data row in rwb-access, the scope taken from the P3 queue membership, the refusal of a service identity at a service boundary, the refusal event on the audit path, the version pinned by the open session, the authorise answer that expires with the session and the Redis-only session record are proved on the real wave 1 services before the wave exits**.

### 2. Business rationale

RWB-E1-022 puts one sign-in in front of the whole Workbench: an Entra ID group per role per environment, granted through the bank IAM, read at each sign-in and turned into a session that carries the roles, the scope, the permission matrix version in force and the separation-of-duty version in force. Under the legacy design the SessionResolver lives in the P4 module, maps the `groups` claim against `role.entra_group` in the recovery schema, checks the `role_conflict` table, unions the letters of `permission` per capability area, and every controller of the monolith asks the in-process AccessCheck before its handler. The component copy of that behaviour sits in RWB-P4-E1022-APP, which owns the seven legacy criteria AC2, AC4, AC5, AC6, AC7, AC8 and AC9 against the published contracts of the services it needs.

This integration story owns the two legacy criteria that no single service can prove, AC1 (one sign-in gives a session with roles, scope and matrix version, and the same session answers the session line and the menu) and AC3 (an identity in no Workbench group is refused everywhere at once), and it adds the eight cross-service criteria AC10 to AC17. Each of the ten is a statement about two owners at once. The session of AC1 is minted by the ACE common module, stored by gateway-bff, resolved by rwb-access and honoured by every other owner: asserted inside one service, it passes while the next service accepts a token whose session was never resolved. The refusal of AC3 is a fact about the edge and about every owner base at the same moment: a service that lets the token through to its own handler makes the criterion fail while the P4 story still passes.

The target moves the source of the facts, never the behaviour. Roles, permissions, conflicts, the delegation-of-approval table and the access log belong to rwb-access in `rwb_access` (DP-01, DP-08), so no service holds a role row and no service holds a copy of the group-to-role mapping. The session itself belongs to the edge: gateway-bff exchanges the browser's opaque session cookie for a short-lived user JWT from ACE common sign-in and keeps the session in its Redis store with no business data (DP-19; Arch v5 slide 20). Each call is one hop from the edge to the owner it needs, in parallel for a composite screen, with the 2 s budget and a breaker per owner (DP-11), and every path moves from the single `/api/recovery/v1` base to `/api/recovery/<short>/v1` (DP-13). The scope line is no longer a value read from a role row in the caller's own module: it is answered from the P3 queue-membership contract (DP-07), the same rows that decide which cases a person may open, so the session's scope and the case read cannot drift. Group names and the capability-area and scope lists are reference data read through the P3 reference-data contract (DP-07), the refusal is recorded locally by the owner that refuses it and collected in the central ledger (DP-03), each service migrates its own schema on its own Flyway sequence (DP-15), and the sign-in and refusal facts leave each service as an event and never as a personal value.

One point is not fixed by the sources and is carried as one gap and one assumption. Arch v5 slide 20 says gateway-bff turns the ACE common sign-in into a session and a short-lived user JWT, and the legacy story puts the `amr` check inside the service's SessionResolver, but no source says which claims the user JWT carries or where the multi-factor gate sits in the target. This story reads the gate at the edge, before any owner is called, and has rwb-access repeat the check when it resolves the session; the claim set is asserted by shape only, never by a value. That reading is GAP-0347 and ASM-0441. Release 30 November 2026 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P4-E1022-APP is done: the role, permission and role-conflict tables are in force in `rwb_access`, and `GET /api/recovery/access/v1/me/session`, `GET /api/recovery/access/v1/admin/roles`, `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/admin/access-log` answer on the P4 base.
- RWB-P3-E1019-APP is done: the queue and membership rows in force answer through the rwb-case contract, including the membership of a person, which the scope line of the session is read from.
- RWB-P1-E1001-APP is done: the 14 data products and their tables are in place, and the freshness read answers the business date of each data product, so a case read in the run is served from data in force.
- The permission matrix version PM-2026.11 is in force from 30 November 2026, and separation of duty version SOD-2026.11 is in force, both loaded as data in `rwb_access`.
- Role RW-CASEOWN carries `entra_group` RWB-SIT-RW-CASEOWN and default scope OWN in SIT; the roles of the run, RW-PHONECOL, RW-LITOFF, RW-LEGAL and RW-SECADM, carry their own `entra_group` rows, and the service identity SY-RULES carries RWB-SIT-SY-RULES.
- The ACE common module sign-in is configured for the Workbench application in Entra ID with the bank conditional access policy that requires a second factor, and rwb-access reaches it for sign-in and group-to-role as its only external call.
- gateway-bff is in front of every owner base in SIT, holds its Redis session store, and carries the short-lived user JWT of the ACE common module to the owner of each call.
- The published contracts of P1, P3 and P4 are versioned in the registry, and the run consumes only those contracts.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic identities U-1001 to U-1009, their group membership and the synthetic cases of the run.
- No production data is read, copied or connected to; every identity, group, role, case and business date the run uses is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: loads the synthetic identity set of the harness RWB-ITG-W1J01-ITG - U-1001 in RWB-SIT-RW-CASEOWN, U-1002 in RW-PHONECOL only, U-1003 with no group whose name starts RWB-SIT-, U-1004 in RWB-SIT-RW-CASEOWN with a token whose `amr` claim holds `pwd` only, U-1005 in RWB-SIT-RW-LITOFF and RWB-SIT-RW-LEGAL, U-1006 in RWB-SIT-RW-SECADM and RWB-SIT-RW-CASEOWN, U-1008 in RWB-SIT-RW-CASEOWN and the unmapped RWB-SIT-LEGACY01, U-1009 for the two matrix versions, and the managed identity SY-RULES in RWB-SIT-SY-RULES; no service schema is opened and no production row is used.
2. Harness: opens the Workbench through gateway-bff as U-1001 and signs in once at the ACE common module with password and second factor.
3. ACE common module: returns the OpenID Connect token with the `groups` claim and the `amr` claim; gateway-bff records the one sign-in and exchanges it for a short-lived user JWT.
4. Gateway-bff: refuses the token at the edge when its `amr` claim does not contain `mfa`, with MSG-P4-005, before any owner is called (AC17).
5. Gateway-bff: calls `GET /api/recovery/access/v1/me/session` on the P4 base with the user JWT and stores the session record it receives in its Redis store, keyed by the session ID it issued.
6. rwb-access: checks the `amr` claim again, maps each group of the `groups` claim to an active `role` row by `entra_group`, ignores a group with no active row, checks the resulting role set against the role conflict version in force, reads the scope line from the P3 queue membership, and answers the session record: identity reference, roles with their default scope, matrix version, conflict version and scope line.
7. Harness: asserts the session record on `GET /api/recovery/access/v1/me/session` and the role list in force on `GET /api/recovery/access/v1/admin/roles`, both on the same user JWT (AC10).
8. Harness: calls `GET /api/recovery/case/v1/cases/{caseId}` on the P3 base with the same user JWT for the case of U-1001 and for the case of another officer, and reads `GET /api/recovery/source-data/v1/data-products/freshness` to separate "not in scope" from "no data" (AC12).
9. Harness: signs in as U-1003 and as U-1002 and asserts the refusals of AC3 and AC2 across every owner base, the refusal events on the ACE audit and SOC path, and the two records of `GET /api/recovery/access/v1/admin/access-log` (AC14).
10. Harness: signs in as SY-RULES and asserts that the service identity is refused at the P4 boundary with the same message and the same reason code as the person of AC2 (AC13).
11. Harness: moves matrix version PM-2026.12 into force at 10:00 on 1 December 2026 in an open session of U-1009 signed in at 09:00 under PM-2026.11, checks the P4 and P3 boundaries at 10:30, signs in again at 11:00 and checks both again (AC15).
12. Harness: inspects the Redis session record of a valid session for the fields it holds and for the business values it does not hold, and the Redis store after the session ends for an authorise answer left behind (AC16, AC17).
13. Harness: proves from the recorded call set that no owner called the ACE common module for a second sign-in of the same session, that no call passed through another service, and that no fake stood in for a P1, P3 or P4 contract; then writes the evidence report and removes the synthetic identities.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an endpoint, for example the admin API | Refused with 403 at the owner that declares the capability area and right; the refusal is written to the access event stream and the access log | MSG-P4-002 | AC13, AC14, TC-E1-022-02-ITG |
| X2 | The identity is in no Workbench group | Refused with 401 at the edge and at every owner base; the access request page shows the message and no data | MSG-P4-001 | AC3, AC14 |
| X3 | The token has no second factor in the `amr` claim | Refused with 401 at the edge before any owner is called; the refusal is logged | MSG-P4-005 | AC17, TC-E1-022-04-ITG |
| X4 | The groups give a role pair listed in the role conflict table | Session refused; an incident is raised to the security administrator; the refusal is logged | MSG-P4-006 | AC18, TC-E1-022-06-ITG, TC-E1-022-11-ITG, regression for RWB-P4-E1022-APP |
| X5 | A service identity calls an area its role does not hold | Refused with 403 at the service boundary, exactly as for a person, with the same reason code | MSG-P4-002 | AC13 |
| X6 | A group maps to no active role row | The group is ignored at rwb-access; if no other group maps, X2 applies | MSG-P4-001 | AC11, TC-E1-022-08-ITG |
| X7 | A new matrix version takes effect while a session is open | The open session keeps the version it resolved at the edge and at every owner; the next session uses the new one | None | AC15 |
| X8 | The ACE sign-in service does not answer | The sign-in fails with the general message and no session is created; no owner is called | MSG-GEN-006 | AC19, TC-E1-022-12-ITG |
| X9 | A cached authorise answer outlives its session | The answer is dropped with the session and the next call asks the owner again | None | AC16 |
| X10 | A consumed contract drifts from the published one, or the synthetic identity set does not match the run | The preflight fails on the contract test or on the identity check and the run stops before any assertion; no fake is put in place of a service contract | None | AC20, TC-E1-022-13-ITG |

X1 to X7 are the exception paths of the legacy story read on the wave 1 services; X4 is the legacy path whose criterion belongs to RWB-P4-E1022-APP and is run here as regression evidence; X8 to X10 are the suite's own failure modes, so that a missing answer never becomes a pass.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the three integration dependencies and the published contracts of P1, P3 and P4, not their source code, and it owns no schema and no table |
| Negotiable | The identity count, the poll interval, the retry of the suite and the report layout are configuration; the groups, roles, scopes, versions, messages and reason codes are fixed by the legacy story and read as data |
| Valuable | Proves across services what one service cannot prove: one sign-in for every boundary, the mapping held once, the scope from the queue membership, the same refusal for a service identity, the refusal event, the version pinned by the session, the cache that dies with it, and the session that lives only at the edge |
| Estimable | One suite module, one identity pack, eight probes, one Redis inspection and one evidence report |
| Small | Seventeen scenarios over three services and two topics, with no service code and no schema change |
| Testable | Every criterion asserts a response, a status, a message, a reason code, a record, a field of the Redis record or the absence of a value, and every identity is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Sign-on with SSO, MFA and the first roles, proven across the wave 1 services

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force from 30 November 2026
    Given separation of duty version "SOD-2026.11" is in force
    Given role RW-CASEOWN has entra_group "RWB-SIT-RW-CASEOWN" and default scope "OWN"
    Given the wave 1 services rwb-access, rwb-case and rwb-source-data are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic identities and their group membership are loaded and no production data is used

  Scenario: AC1 SSO sign-in (legacy RWB-E1-022 AC1)
    Given test user "U-1001" is in Entra ID group "RWB-SIT-RW-CASEOWN"
    When the user opens the Workbench and signs in with password and second factor
    Then the session holds roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11"
    Then GET /me/session returns the line "Case owner. Scope: own cases."
    Then the menu shows the screens of the capability areas where RW-CASEOWN holds R, and no Administration menu

  Scenario: AC3 Not in group (legacy RWB-E1-022 AC3)
    Given test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-"
    When the user opens the Workbench
    Then the access request page shows MSG-P4-001 and no case, queue or reference data
    Then every recovery endpoint returns status 401 for that token
    Then the system writes one refusal event with reason "NO_ROLE"

  Scenario: AC10 One sign-in is carried to every boundary as a short-lived user JWT (new, D-RCV-60)
    Given the ACE common module answers one sign-in for U-1001 with the groups claim holding "RWB-SIT-RW-CASEOWN" and the amr claim holding "mfa"
    Given gateway-bff stores the session it resolves from that sign-in
    When U-1001 opens the Workbench once
    Then gateway-bff holds the session in its Redis store and carries the short-lived user JWT of the ACE common module to the owner of each call
    Then GET /api/recovery/access/v1/me/session answers roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11" on that JWT
    Then GET /api/recovery/access/v1/admin/roles answers RW-CASEOWN as a role in force on the same JWT
    Then the ACE common module records one sign-in for the session and no owner asked for a second one

  Scenario: AC11 The group-to-role mapping is one data row in rwb-access (new, D-RCV-60)
    Given the role rows of rwb_access map "RWB-SIT-RW-CASEOWN" to RW-CASEOWN and map "RWB-SIT-LEGACY01" to no active role
    When test user "U-1008" signs in from both groups
    Then the session holds only "RW-CASEOWN" and GET /api/recovery/access/v1/admin/roles answers RW-CASEOWN with entra_group "RWB-SIT-RW-CASEOWN"
    Then the group "RWB-SIT-LEGACY01" is ignored at rwb-access and no other service decides a role
    Then the P3 case read and the P1 freshness read answer from their own contracts and hold no group name and no mapping row
    Then the next session of U-1008 resolves the same two rows with no deployment and no code change

  Scenario: AC12 The scope line comes from the P3 queue-membership contract (new, D-RCV-60)
    Given the queue-membership contract of rwb-case answers the queues that U-1001 is a member of
    Given case one belongs to U-1001 and case two belongs to another officer
    When U-1001 signs in and calls GET /api/recovery/access/v1/me/session
    Then the session answers scope "OWN" from the P3 queue-membership contract and not from a value held in the session resolver
    Then GET /api/recovery/case/v1/cases/{caseId} answers case one on the same JWT
    Then GET /api/recovery/case/v1/cases/{caseId} for case two answers status 404 while the same session is still valid at the P4 boundary
    Then GET /api/recovery/source-data/v1/data-products/freshness answers the data product behind the case, so the 404 is the scope answer and not a missing data product

  Scenario: AC13 A service identity is refused at a service boundary exactly as a person (new, D-RCV-60)
    Given managed identity "SY-RULES" is in group "RWB-SIT-SY-RULES" and holds no Platform administration R
    When SY-RULES calls GET /api/recovery/access/v1/admin/roles
    Then the call returns status 403 with MSG-P4-002 exactly as the person of AC2 is refused, with action "read roles"
    Then POST /api/recovery/access/v1/authorise answers the same reason code "NO_RIGHT" for SY-RULES and for U-1002
    Then GET /api/recovery/access/v1/admin/access-log holds one record per refused call with the identity and the reason code

  Scenario: AC14 The refusal event reaches the audit path with no personal data (new, D-RCV-60)
    Given test user "U-1003" has no group whose name starts "RWB-SIT-" and test user "U-1002" holds only RW-PHONECOL
    When both open the Workbench and the second calls GET /api/recovery/access/v1/admin/roles
    Then the ACE audit and SOC path receives one refusal event with reason "NO_ROLE" and one with reason "NO_RIGHT"
    Then each event carries the Entra ID object reference and no name, no e-mail and no case, account or person value
    Then GET /api/recovery/access/v1/admin/access-log holds the two refusals with the same reason codes and the same identity references
    Then no service holds a copy of the refusal in a business table

  Scenario: AC15 A matrix version that takes effect after sign-in reaches only the next session (new, D-RCV-60)
    Given test user "U-1009" signed in at 09:00 on 1 December 2026 under matrix version "PM-2026.11"
    Given matrix version "PM-2026.12" takes effect at 10:00 on 1 December 2026 and rwb-access publishes AccessPolicyChanged on rwb.access.events.v1
    When GET /api/recovery/access/v1/admin/roles and GET /api/recovery/case/v1/cases/{caseId} are called at 10:30 in the same session
    Then rwb-access and rwb-case both answer under "PM-2026.11" and the open session keeps the version it resolved
    Then after U-1009 signs in again at 11:00 both boundaries answer under "PM-2026.12"
    Then no owner re-resolved the version of the open session

  Scenario: AC16 The cached authorise answer dies with the session (new, D-RCV-60)
    Given the authorise answer for U-1001 is cached for the session, as the P4 contract allows
    When rwb-access publishes AccessPolicyChanged and the answer for the area of the cached call changes
    Then the open session keeps the answer it resolved and every call inside it receives the same answer
    Then after the session ends, or idles past its idle limit, the next call re-asks POST /api/recovery/access/v1/authorise and receives the new answer
    Then the Redis store holds no authorise answer after the session ends

  Scenario: AC17 The session lives only at the edge and the MFA gate is at the edge (new, D-RCV-60)
    Given test user "U-1004" is in group "RWB-SIT-RW-CASEOWN" and the token's amr claim holds "pwd" and not "mfa"
    When the token reaches gateway-bff
    Then the gateway refuses the session with status 401 and message MSG-P4-005 before any owner is called
    Then the recorded call set holds no P4, P3 or P1 call for that token
    Then the Redis session record of a valid session holds the session ID, the identity reference, the resolved roles, the two versions and the scope line, and no case, account, person or document value

  Scenario: AC18 A role pair listed in the role conflict table is refused and raised to the security administrator (new, D-RCV-60)
    Given a test user of the W1J01 set holds the groups of a role pair listed in the role conflict table
    When that user signs in
    Then the session is refused with MSG-P4-006 and no session is created
    Then an incident is raised to the security administrator and the refusal is logged in the access log

  Scenario: AC19 The ACE sign-in service does not answer and no session is created (new, D-RCV-60)
    Given the ACE common sign-in service does not answer for test user U-1001
    When U-1001 opens the Workbench
    Then the sign-in fails with the message MSG-GEN-006 and no session is created in the gateway Redis store
    Then no owner is called for that sign-in

  Scenario: AC20 A drifted contract or a mismatched identity set stops the run before any assertion (new, D-RCV-60)
    Given the consumed contract of a wave 1 service differs from its published contract, or the identity set does not match the run
    When the SuiteRunner preflight runs
    Then the run stops before any assertion and no fake is put in place of a service contract
    Then the report names the failed preflight check and writes no test case verdict

  Scenario: AC21 An endpoint without a declared capability area and right fails the contract test (new, D-RCV-60)
    Given an endpoint of rwb-access or rwb-case is published without a capability area and right
    When the contract test runs in the preflight
    Then the contract test fails on that endpoint and the run stops before any assertion

  Scenario: AC22 Each service signs in with its own login and the suite runs no migration (new, D-RCV-60)
    Given the wave 1 services rwb-access, rwb-case and rwb-source-data are deployed in SIT
    When the suite starts
    Then each service answers under its own login and the suite opens no service schema and runs no migration

  Scenario: AC23 A consumed call that fails or does not answer returns no default and no cached value (new, D-RCV-60)
    Given the P3 queue-membership contract of rwb-case does not answer for U-1001
    When U-1001 calls GET /api/recovery/case/v1/cases/{caseId} through gateway-bff
    Then the call fails with the general message and no default or cached value is answered
    Then the suite records no test case verdict as a pass
```

**Target reading.** In the monolith one SessionResolver inside the P4 module reads `recovery.role`, `recovery.permission` and `recovery.role_conflict` and every controller asks the in-process AccessCheck. In the target the role, permission, conflict, delegation and access-log rows live in `rwb_access` only (DP-01, DP-08), each service signs in with its own login (DP-15 keeps its own migration sequence), the session is minted at the ACE common module, stored in the gateway Redis store and carried to every owner as one short-lived user JWT with one hop per call and a 2 s budget (DP-19, DP-11), the authorise answer is the published contract of rwb-access cached per session, the scope line is answered from the P3 queue membership and the lists from the P3 reference-data contract (DP-07), the refusal is recorded locally by the owner that refuses it and collected in the central ledger (DP-03), and the legacy `/api/recovery/v1` base moves to `/api/recovery/access/v1/`, `/api/recovery/case/v1/` and `/api/recovery/source-data/v1/` (DP-13). The claims of the short-lived user JWT are Not specified in the source documents (GAP-0347); the multi-factor gate sits at gateway-bff before any owner is called and rwb-access repeats it when it resolves the session (BR12; ASM-0441), so the suite asserts the claims by shape and never by a value. Session home (GAP-0775): the resolved roles, the scope line and the two version labels are held in the session record in the gateway Redis store (BR11); the conflict incident rides the refusal with reason code ROLE_CONFLICT (BR15); the team and region read behind the scope line is Not specified in the source documents (GAP-0775). Login and mapping (GAP-0777): the rwb-access login name is Not specified in the source documents (GAP-0777); the group-to-role mapping row stays in `rwb_access` (AC11) and the ACE group name (DF-ACE-301) is read only through the P1 contract; the column set of the three library objects is Not specified in the source documents (GAP-0777).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role. The Workbench holds no password and no local account | v_ace_iam_group.entra_group (DF-ACE-301); DT07; Admin and access model, section 4.2 |
| BR2 | A session is refused unless the token carries a second factor | NFR-049; FEAT-ACA-02 |
| BR3 | No role inherits from another. A person with two roles holds the union of both roles' letters | permission.letters (DF-REF-043) |
| BR4 | A capability area with no letter for any of the session's roles refuses every action in that area | Permission matrix; CTL-09 |
| BR5 | A role pair listed in the role conflict table may not be held in one session | Separation of duty sheet, roles.txt; role_conflict table |
| BR6 | A service identity holds a role in the same table and is checked the same way as a person | REQ-ACA-010; NFR-051 |
| BR7 | A session keeps the matrix and conflict versions it resolved at sign-in until it ends | Admin and access model, section 4.2 |
| BR8 | Group names, roles, letters and conflicts are data rows with a version; none is written in code | Principle 1; DT02 |
| BR9 | The role, permission, conflict, delegation and access-log rows live in `rwb_access` only, and no service holds a role row or a copy of the group-to-role mapping | DP-01; DP-08; ownership map (role, permission, role_conflict, delegation_limit); covered by AC11 |
| BR10 | One sign-in per session: the ACE common module mints the short-lived user JWT once, gateway-bff carries it to every owner, and no owner signs in again for the same session | Arch v5 slide 20; DP-19; covered by AC10 |
| BR11 | The session record lives in the gateway Redis store and holds no business data: identity reference, roles, versions and scope line only | Arch v5 slide 20; DP-19; covered by AC10 and AC17 |
| BR12 | The multi-factor gate sits at the edge before any owner is called, and rwb-access repeats the check when it resolves the session; a token without `mfa` in its `amr` claim creates no session | BR2; ASM-0441; covered by AC17 |
| BR13 | The scope line of the session is answered from the P3 queue membership; the scope of a role and the membership of a person cannot drift apart because there is one source | DP-07; BR7; REQ-ACA-009; covered by AC12 |
| BR14 | The authorise answer is cached per session only, and the cache dies with the session | Arch v5 slide 14 (`authorise (cached)`); DP-08; covered by AC16 |
| BR15 | A refusal carries a reason code - NO_ROLE, NO_MFA, ROLE_CONFLICT or NO_RIGHT - from the owner that refuses it, and the event of the refusal carries the Entra ID object reference and no personal value | RWB-E1-022 build step 5; guardrail of RWB-E1-022; DP-03; covered by AC3, AC14 and AC17 |
| BR16 | Every endpoint declares its capability area and right, and the contract test fails on an endpoint without one | RWB-E1-022 guardrail; DP-08; covered by AC21 |
| BR17 | Each service signs in with its own login and migrates its own schema; the suite owns no schema and runs no migration | DP-02; DP-15; ADR-021; covered by AC22 |
| BR18 | No service schema is opened by the suite and no published service contract is faked; a run that needs either fails the preflight | DP-01; section 17; covered by AC20 and AC22 |

### 9. State transitions

None. This story changes no case status and no record; it creates a session with the states Resolved and Refused, and the session ends at sign-out or at its idle limit.

The states the run observes across the services:

| Item | States |
|---|---|
| Session at the edge | Created (gateway record and user JWT), Valid, Ended (sign-out or idle limit) |
| Session resolution at rwb-access | Resolved (roles, scope, matrix version, conflict version, scope line), Refused (reason code) |
| Refusal reason | NO_ROLE, NO_MFA, ROLE_CONFLICT, NO_RIGHT |
| Authorise answer | Cached for the session, Re-asked after the session ends |
| Suite run | Not started, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the synthetic identity pack, the version and clock control, the probes, the Redis inspection and the evidence report |
| Case owner (RW-CASEOWN) | Signs in with the second factor and reads the session line and the screens of the areas where the role holds R; read only |
| Phone collector (RW-PHONECOL) | Signs in; refused on Platform administration, with one refusal event and one access-log record |
| Litigation officer (RW-LITOFF) and legal counsel (RW-LEGAL) | Sign in together in the union case; regression evidence for RWB-P4-E1022-APP only |
| Security administrator (RW-SECADM) | Receives the conflict incident of the regression path; maintains the group rows through the bank IAM |
| Reference-data administrator (RW-REFADM) | Loads an approved role, group, matrix or duty version. Approves none |
| Service identity (SY-RULES) | Acts under its managed identity and its own role row, and is refused exactly as a person |
| Service owner of rwb-access | Owns the session resolution, the covering table rows, the authorise answer, the access log and the refusal events |
| Service owner of rwb-case | Owns the queue and membership rows that answer the scope line, and the case read with its 404 outside scope |
| Service owner of rwb-source-data | Owns the data products and the freshness stamp behind the case read |
| No role | Reads a service schema, calls an owner directly, or takes production data into the run |

The request, approval and grant of a role run in the bank IAM and are outside this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | role | id | Read through `GET /api/recovery/access/v1/admin/roles` |
| DF-REF-035 | role | role_code | Read through the P4 role read |
| DF-REF-036 | role | role_name | Read through the P4 role read |
| DF-REF-037 | role | role_class | Read through the P4 role read |
| DF-REF-038 | role | default_scope | Read through the P4 role read and through the session record |
| DF-ACE-301 | v_ace_iam_group | entra_group | Read through the P4 role read (`entraGroup`, read only); the group name behind the mapping of AC11 |
| DF-REF-041 | permission | role_id | Read through the P4 authorise answer |
| DF-REF-042 | permission | capability_area | Read through the P4 authorise answer |
| DF-REF-043 | permission | letters | Read through the P4 authorise answer |
| DF-REF-044 | permission | matrix_version | Read through `GET /api/recovery/access/v1/me/session` |
| DF-REF-206 | role_conflict | role_code | Read through the P4 session resolution |
| DF-REF-207 | role_conflict | conflicts_with | Read through the P4 session resolution |
| DF-REF-209 | role_conflict | conflict_version | Read through `GET /api/recovery/access/v1/me/session` |
| DF-REF-210 | role_conflict | valid_from | Read through the P4 session resolution |

Field IDs are those of the Logical Data Model and Data Dictionary and are copied unchanged from RWB-E1-022, except `entra_group`, which is DF-ACE-301 of the read-only ACE view `v_ace_iam_group` (Physical Schema v7). The suite owns no field and no table: every row above is read through a P4 contract of section 12.2 and, apart from the `v_ace_iam_group` row, is in `rwb_access`, the queue membership behind the scope line is in `rwb_case` and is read through the P3 contract, and the data product behind the case read is in `rwb_source_data`. No production value is used.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the task queue `rwb-integration` and the schema `rwb_integration` - are recorded as reserved and are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC1, AC10, AC12, AC15: the session record after one sign-in - identity reference, roles with their default scope, matrix version, conflict version and scope line | 2 s |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | AC10, AC11, AC13, AC15: the role list in force with `entra_group`, and the refusal of a role without Platform administration R | 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | AC13, AC16: the authorise answer for a role, a scope and a duty limit, cached per session; the published authorise contract of rwb-access on Arch v5 slide 14 | 2 s |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | AC13, AC14: one record per refused call with the identity and the reason code | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC12, AC15: the case of the session holder, the 404 outside the scope, and the version pinned by the open session | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | AC12: the data product behind the case, so a 404 is the scope answer and not a missing data product | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget behind gateway-bff, and the suite calls no service through another service. The session read, the role read and the access-log read are P4 operations in the ownership map, and the case read is a P3 operation there; the authorise operation is named for rwb-access on Arch v5 slide 14 (`POST /authorise`, `GET /me/permissions`, `GET /doa-limits`, `/masking-policies`), so the path shown is that operation on the P4 base of DP-13 and is a derivation of two sources, not a new contract.

#### 12.3 Events published

None. The suite publishes no business event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 rwb-access (observed as produced) | AC15: the version announcement that follows the matrix version in force; the open session keeps its version and the next session resolves the new one at two services |
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 rwb-access (observed as produced) | AC16: a duty-limit announcement while a session is open changes neither the cached authorise answer nor the session record; the values of the duty table themselves belong to RWB-P4-E1022-APP |

The suite asserts no other event. The local decision record of a refusal is written by the owner that refuses it and collected in the central ledger in rwb-decision (DP-03), and that record belongs to RWB-P4-E1022-APP; this story asserts the refusal on the audit path and in the access log instead. No event carries a case, an account or a person value.

#### 12.5 Workflows and activities

None. The sign-in, the session resolution, the authorise check and the refusal are synchronous service steps; this story starts no workflow, observes no workflow and asserts no activity, and no case workflow is on the path of a sign-in.

#### 12.6 Schedules

None. The six-monthly access review list of rwb-access (JOB-18, a Schedule in the owning service) is not asserted by this story and belongs to RWB-P4-E1022-APP; the suite starts no schedule and moves only the matrix version of AC15 with its own clock control.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises are listed in section 11 with their owners: `role`, `permission` and `role_conflict` in `rwb_access`, the queue and membership rows in `rwb_case`, and the data products of `rwb_source_data`.

#### 12.8 Contract fakes

None for a service contract. The only stub is external to the nineteen services:

| Stub | Purpose |
|---|---|
| Mock Entra sign-in with its synthetic groups | Gives the run its synthetic identities U-1001 to U-1009, the managed identity SY-RULES and their group membership, with the `groups` and `amr` claims, as the platform demo sign-in does |

No published service contract is faked: the run needs the real P1, P3 and P4 services on their published contracts, and a run that needs a fake for any of them fails the preflight. No contract fake of rwb-access, rwb-case or rwb-source-data is named, and the contract fake library version is Not specified in the source documents (DOR-RWB-ITG-E1022-ITG-22).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 operations | The session read, the role read, the authorise call, the access-log read, the case read and the freshness read; one hop each, 2 s budget (DP-11, DP-13, DP-19) |
| Kafka | None | 2 event types | `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`; CloudEvents 1.0 (DP-14) |
| Temporal | None | None | No workflow and no activity in this story |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: an identity pack for the synthetic people, the managed identity and their groups; a version and clock control for the matrix version of AC15; eight probes; a Redis inspection; and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts of P1, P3 and P4 and against the identity pack, run order, report and exit code |
| IdentityDriver | Test harness | Drives the mock Entra sign-in for U-1001 to U-1009 and SY-RULES, counts the sign-ins, and sets the `groups` and `amr` claims of each token |
| SessionProbe | Test harness | The session record of AC1 and AC10 on `GET /api/recovery/access/v1/me/session`, the role list on `GET /api/recovery/access/v1/admin/roles`, and the one-sign-in count |
| MappingProbe | Test harness | The mapped and the unmapped group of AC11, and the assertion that no service other than rwb-access decides a role |
| ScopeProbe | Test harness | The scope line of AC12 from the P3 queue membership, the case in scope and the 404 outside it, with the freshness read that separates the two |
| IdentityBoundaryProbe | Test harness | The refusal of SY-RULES at the P4 boundary of AC13 with the same message and the same reason code as U-1002 |
| RefusalEventProbe | Test harness | The two refusal events of AC14 on the ACE audit and SOC path, their Entra ID object reference and the absence of a personal value, and the two access-log records |
| VersionProbe | Test harness | The two matrix versions of AC15 across the P4 and P3 boundaries at 09:00, 10:00, 10:30 and 11:00 |
| CacheProbe | Test harness | The cached authorise answer of AC16 and its disappearance with the session |
| EdgeGateProbe | Test harness | The `amr` gate of AC17 at the edge, the empty owner call set for that token, and the fields held and not held by the Redis record |
| ReportWriter | Test harness | One row per test case with its evidence and elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object, and it holds no client for a service schema and no client for a `v_ace_*` view. The schema `rwb_access` is owned by rwb-access (RWB-P4-E1022-APP) and is read only through its published contract.

**Configuration and reference data**

- The SIT endpoints of P1, P3 and P4 behind gateway-bff, the topic name, the schema-registry address, the Redis inspection endpoint of the gateway and the gateway idle limit, all as configuration.
- The synthetic identities U-1001 to U-1009, the managed identity SY-RULES and their groups RWB-SIT-RW-CASEOWN, RWB-SIT-RW-LITOFF, RWB-SIT-RW-LEGAL, RWB-SIT-RW-SECADM, RWB-SIT-SY-RULES and RWB-SIT-LEGACY01, with no production identity.
- The role rows of the run, RW-CASEOWN, RW-PHONECOL, RW-LITOFF, RW-LEGAL and RW-SECADM, read through the P4 role read and never written in the suite code.
- Permission matrix versions PM-2026.11 and PM-2026.12 and separation of duty version SOD-2026.11, with their effective times, read through the P4 session record and the announcement topic.
- The capability-area and scope lists, LOV-CAPABILITY and LOV-SCOPE, read through the P3 reference-data contract (DP-07) and not typed in the suite.
- The 2 s client budget, the retry of the suite and the poll interval of the announcement topic.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 and DP-08 carry the role, permission, conflict and access-log facts behind one owner; DP-07 carries the scope line and the two lists, which are reference data of rwb-case; DP-11 and DP-19 carry the one hop from the edge and the 2 s budget; DP-13 carries the base of every path; DP-03 applies to the refusal, which the refusing owner records locally and which is collected in the central ledger, and the suite asserts it on the access log and the audit path rather than in a table; DP-15 keeps one migration sequence per service and one schema per owner. The H and C entries of the table belong to the service, platform and operations stories that own them: this ITG story carries no H, C or X entry of its own, and an integration story never becomes a build dependency of another story (Template and Rules section R5.4 and R5.7). The I list names the three service builds whose behaviour the run exercises.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Identities | U-1001 to U-1009 and SY-RULES, each with its group membership and its token claims, from the W1J01 set | AC1, AC3, AC10 to AC17 |
| Role rows | RW-CASEOWN with entra_group RWB-SIT-RW-CASEOWN and scope OWN, RW-PHONECOL, RW-LITOFF, RW-LEGAL and RW-SECADM | AC1, AC11, AC13, AC14 |
| Unmapped group | RWB-SIT-LEGACY01 held by U-1008 with no active role row | AC11 |
| Versions | PM-2026.11 in force from 30 November 2026, PM-2026.12 in force from 10:00 on 1 December 2026, SOD-2026.11 in force | AC1, AC15 |
| Cases | Case one owned by U-1001 and case two owned by another officer, with the data product behind case one complete | AC12, AC15 |
| Tokens | One token with `amr` holding `mfa`, and one token with `amr` holding `pwd` only | AC10, AC17 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the topic and the gateway Redis inspection, with the contract preflight that fails on any drift.
2. Build IdentityDriver and the identity pack; assert that each synthetic identity signs in and that each group membership is the one the criteria name, before any assertion is made.
3. Build SessionProbe and prove the one sign-in of AC10: the session record, the role read and one sign-in count at the ACE common module.
4. Build MappingProbe for AC11 and assert that the mapping is one row in `rwb_access` (owned by rwb-access, RWB-P4-E1022-APP, read only through its contract), that the unmapped group is ignored, and that the P3 and P1 responses hold no group name.
5. Build ScopeProbe for AC12: the scope line from the P3 queue membership, the case in scope, the 404 outside it and the freshness read behind the case.
6. Build IdentityBoundaryProbe and RefusalEventProbe; assert the same refusal for SY-RULES and for U-1002, the two reason codes, the two audit events with the Entra ID object reference, and the two access-log records.
7. Build VersionProbe for AC15 and CacheProbe for AC16 with the clock control; assert the version pinned by the open session at two services and the answer re-asked after the session ends.
8. Build EdgeGateProbe for AC17: the refusal at the edge with MSG-P4-005, the empty owner call set, and the fields held and not held by the Redis record.
9. Build ReportWriter and the cleanup; run the whole suite twice to prove that a repeated sign-in of the same identity opens a second session and leaves no answer of the first behind.

**Done when.** The ten test cases of section 16 pass on the real services in SIT, the two criteria this story owns (AC1 and AC3) and the eight cross-service criteria (AC10 to AC17) are signed off against the contracts, the gateway Redis store holds no authorise answer after a session ends and no business value during one, no service table and no view was opened by the suite, the synthetic identities are removed, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-005 | Token without a second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Conflicting role pair at sign-in | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-GEN-006 | ACE sign-in service unavailable | {system} is not available. Try again in a few minutes. |

The five texts are copied unchanged from RWB-E1-022 and this story adds no message ID. The messages are rendered by the service or the edge that refuses the call and passed through gateway-bff unchanged, so the suite asserts the ID and the text on the response it receives.

### 15. Screens and states

No screen is built by this story. The ACE front end shell is served through gateway-bff (DP-19): it shows the session line from `GET /api/recovery/access/v1/me/session` at the top of every page, hides the menu entries whose capability area the session cannot read, and shows no Administration menu for RW-CASEOWN. A person with no role sees the access request page with MSG-P4-001 and no data. A token without a second factor never reaches a page, because the gate is at the edge. Epic 1 has no business screens in this story, and the screen states the run observes are the session line, the filtered menu, the access request page and the refusal banner of the owner that refused the call.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-022-01-ITG | AC1, BR1, AC10, AC12 | Integration | Test user in RWB-SIT-RW-CASEOWN with MFA; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-02-ITG | AC2, BR4, AC14 | Integration | Test user holding RW-PHONECOL only; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-03-ITG | AC3, BR1, AC14 | Integration | Entra ID test account with no RWB-SIT group; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-04-ITG | AC4, BR2, AC17 | Integration | Token with amr "pwd" only; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-05-ITG | run by RWB-P4-E1022-APP (AC5, BR3) | Integration | Test user in the RW-LITOFF and RW-LEGAL groups; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-06-ITG | run by RWB-P4-E1022-APP (AC6, BR5) | Integration | Test user in the RW-SECADM and RW-CASEOWN groups; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-07-ITG | AC7, BR6, AC13 | Integration | Managed identity SY-RULES; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-08-ITG | AC8, BR8, AC11 | Integration | One mapped and one unmapped group; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-09-ITG | AC9, BR7, AC15, AC16 | Integration | Matrix versions PM-2026.11 and PM-2026.12 with effective times one hour apart; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-10-ITG | Access, BR4 | Integration | A role without the right is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-11-ITG | AC18, BR5 | Integration | Test user of the W1J01 set holding a role pair listed in the role conflict table; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-12-ITG | AC19 | Integration | Test user U-1001 with the ACE common sign-in service not answering; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-13-ITG | AC20 | Integration | A drifted copy of one wave 1 published contract and a non-matching identity set; preflight run only |
| TC-E1-022-14-ITG | AC21, BR16 | Integration | An endpoint of rwb-access or rwb-case published without a capability area and right; preflight run only |
| TC-E1-022-15-ITG | AC22, BR17, BR18 | Integration | The wave 1 services deployed in SIT; the suite starts and opens no service schema; end-to-end: real services on the wave 1 contracts |
| TC-E1-022-16-ITG | AC23 | Integration | A consumed call of a wave 1 service that fails or does not answer; end-to-end: real services on the wave 1 contracts |

The Level column follows Template and Rules section R7.2: the legacy System level becomes Integration and the legacy Access level becomes Integration. The -ITG copy of each row also carries the cross-service step of the new criteria: AC10 and AC12 on TC-E1-022-01-ITG, AC14 on TC-E1-022-02-ITG and TC-E1-022-03-ITG, AC17 on TC-E1-022-04-ITG, AC13 on TC-E1-022-07-ITG, AC11 on TC-E1-022-08-ITG, and AC15 and AC16 on TC-E1-022-09-ITG.

TC-E1-022-01-ITG for AC1 and TC-E1-022-03-ITG for AC3 are the two copies this story signs off. The other eight are regression evidence for RWB-P4-E1022-APP, which owns their criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed.

### 17. Guardrails

- No local password and no local account: the only credential is the ACE common module sign-in with a second factor, and the Workbench holds no secret of its own (DP-19; BR1).
- No role cache that outlives the session: the authorise answer is cached per session and dies with it, and the Redis store holds no answer after the session ends (DP-08).
- No copy of the group-to-role mapping in any service but rwb-access: no service holds a role row, a group name or a mapping table (DP-01; BR9).
- No personal data in events, logs or fixtures: a refusal carries the Entra ID object reference, the reason code and the area and right, and never a name, an e-mail or a case, account or person value (DP-03; BR15).
- Every endpoint declares its capability area and right, and the contract test fails on an endpoint without one (BR16).
- The identity number and every personal field stay behind the owners; this story reads no personal field at all.
- No business value in code: the roles, the groups, the letters, the versions and the lists are read as data through the P3 and P4 contracts.
- Synthetic identities only: the harness RWB-ITG-W1J01-ITG supplies every identity, and the run refuses any environment that is not SIT.
- One hop and a 2 s budget on every call, with no service called through another service and no owner signing in again for the same session (ADR-020; DP-11).
- Clean-up in the same run: the synthetic identities and the moved version are removed or restored, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-001 | Every person signs on through Entra ID single sign-on with multi-factor authentication | The ACE common module sign-in, the short-lived user JWT at gateway-bff, `GET /api/recovery/access/v1/me/session`, MSG-P4-001, MSG-P4-005 | TC-E1-022-01-ITG, TC-E1-022-03-ITG, TC-E1-022-04-ITG |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | `GET /api/recovery/access/v1/admin/roles`, the group-to-role row of `rwb_access`, `rwb.access.AccessPolicyChanged.v1` | TC-E1-022-05-ITG, TC-E1-022-08-ITG, TC-E1-022-09-ITG |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | `POST /api/recovery/access/v1/authorise` for SY-RULES, MSG-P4-002, `GET /api/recovery/access/v1/admin/access-log` | TC-E1-022-02-ITG, TC-E1-022-06-ITG, TC-E1-022-07-ITG, TC-E1-022-10-ITG |
| DP-01 and DP-08 | Owner's schema and the authorise contract of rwb-access | The role, permission and conflict rows in `rwb_access`, the guard library, the absent service-schema client | TC-E1-022-08-ITG, TC-E1-022-09-ITG |
| DP-07 | Reference-data contract of rwb-case | The scope line from the queue membership, LOV-CAPABILITY and LOV-SCOPE | TC-E1-022-01-ITG, TC-E1-022-09-ITG |
| DP-03 | Local decision record and the shared ledger | The refusal recorded by the refusing owner and collected in `rwb.decision-record.v1`, asserted on the audit path and the access log | TC-E1-022-02-ITG, TC-E1-022-03-ITG |
| DP-11, DP-13 and DP-19 | gateway-bff route, one hop, 2 s budget, the service bases | The six operations of section 12.2 and the composed route behind the edge | TC-E1-022-01-ITG, TC-E1-022-10-ITG |
| DP-15 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| BR7 | A session keeps the versions it resolved until it ends | `GET /api/recovery/access/v1/me/session`, the version at the P4 and P3 boundaries, `rwb.access.AccessPolicyChanged.v1` | TC-E1-022-09-ITG |
| GAP-0347; ASM-0441 | The claims of the user JWT and the split of the MFA gate between the edge and rwb-access | The edge gate of AC17 and the repeated check in the P4 session resolution | TC-E1-022-04-ITG |
| RWB-E1-022 (legacy story) | Sign-on with SSO, MFA and the first roles: AC1 and AC3 | The six operations, the two events and the edge route of section 12 | TC-E1-022-01-ITG, TC-E1-022-03-ITG |
| RWB-P4-E1022-APP (component copy) | The session resolution and the access check in rwb-access, owning AC2, AC4 to AC9 | The P4 session read, the role read, the authorise answer and the access log | The eight regression copies of section 16 |

### 19. Out of scope

- The three application builds this run depends on: RWB-P1-E1001-APP, RWB-P3-E1019-APP and RWB-P4-E1022-APP.
- The contract story of the legacy key in rwb-access, and the database, operations and infrastructure stories of the legacy key.
- The criteria this story does not own: AC2, AC4, AC5, AC6, AC7, AC8 and AC9, which belong to RWB-P4-E1022-APP.
- The permission matrix load, PDPA masking, scope filtering and leaver handling (RWB-E1-037).
- Writing access events into the decision log and break-glass (RWB-E1-039).
- Partner identities through the external gateway (RWB-E2-019).
- Full administration screens for roles and access, SCR-43 (Epic 8, FEAT-ADM-01).
- The request, approval and grant steps themselves, which run in the bank IAM, not in the Workbench.
- The build of the harness RWB-ITG-W1J01-ITG itself.
- The non-functional epic RWB-ITG-NFR.
