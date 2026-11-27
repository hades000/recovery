# RWB-PLT-E1037-CON Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-037 for the platform library RWB-PLT-LIB — the published contract of the access guard and masker library. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 50 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1037-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-PLT-E1037-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-PLT-E1037-CON-16); squad sizes at refinement |
| Contract version | Not specified in the source documents (DOR-RWB-PLT-E1037-CON-23); /v1 path only |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6. Specified the guard’s fail-closed 503 Problem and messageCode.


### 1. Story

As a **platform contract owner**, I want **the published contract of the guard and masker library — the `AccessGuard`, `ScopeGuard` and `MaskApplier` interfaces, the `@PersonalData` annotation, the scope descriptor, the error vocabulary with its message ids, the fail-closed rule, the statement that the library owns no table and no token, and the fakes — instead of the monolith's `recovery.access.matrix` package that read the permission and masking tables in the same database**, so that **every service can be built and tested against one frozen authorisation and masking contract while the data stays with P4**.

The contract is a contract before it is code. The three interfaces fix what a service may call and what it may never pass; the annotation fixes how a response field is declared as personal data; the scope descriptor fixes what the owning service receives and applies; the error vocabulary fixes the two statuses and the message ids a caller sees; the fail-closed rule fixes the behaviour of every failure; and the fakes let a service build on Day 1 while the access owner and the data owner are still being built.

The contract also fixes the negative space, which is the part that keeps the split honest: the library owns no table, holds no login and no token, can never receive the clear identity number, publishes no event of its own and takes no delegation decision. A service that wants a table, a cache store or a user list of its own is outside this contract by design.

**The division is fixed and is the same in both stories of this legacy key.** The permission matrix as data, the masking rules, the scope rule, the access log and the matrix load and approve operations stay with **RWB-P4-E1037-APP**, which owns the legacy acceptance criteria; the end-to-end proof across the wave 1 services is **RWB-ITG-E1037-ITG**; this story and its app story RWB-PLT-E1037-APP deliver the **shared guard library and masker library** that every service binds, so that the right check and the masking are one mechanism and not nineteen copies. Neither story copies a legacy acceptance criterion: every criterion in section 7 is tagged (new, D-RCV-60) and tests only the contract deliverable in the title, and the fifteen legacy test cases are executed by RWB-P4-E1037-APP and RWB-ITG-E1037-ITG (section 18).

### 2. Business rationale

In the monolith the permission matrix, the masking rules, the scope rule and the guard sat in one database and one package: `recovery.access.matrix` read `permission`, `masking_rule`, `role` and `delegation_limit` in the same connection, built a `ScopeFilter`, filled annotated DTOs and answered `isUnmasked`. There was one implementation because there was one process. In the 19-service target those tables stay with one owner (DP-01): P4 rwb-access owns `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit`, P3 rwb-case owns `lov_value`, and P1 rwb-source-data owns the ACE view fields. Every service still has to check a right, bound a query and mask a field.

Without a published contract that check becomes nineteen implementations of the same four things, drifting apart at the first policy change. With it, a service compiles against one frozen interface from Day 1, tests against fakes before the access owner exists, and cannot quietly read a P4 table because the contract gives it no connection to do so. Each service authorises the object itself, using cached permission data from rwb-access (Architecture v5 slide 10); the access owner publishes `POST /authorise` for role, scope and DoA, `GET /me/permissions`, `GET /doa-limits` and `GET /api/recovery/access/v1/masking-policies`, and writes `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1` (slide 14); the masking rules of the access owner are enforced in each service and the clear identity number never leaves ACE (slide 35; ADR-010).

The values the criteria use are the legacy values unchanged — matrix version `PM-2026.11`, masking version `MASK-SIT-01`, cases `RW-2026-000123` and `RW-2026-000456`, team `MTG-NE`, the role codes RW-CASEOWN, RW-LEGAL, RW-PHONECOL, RW-SECADM, RW-REFADM, RW-COE and RW-AUDIT, the field ids DF-ACE-073 `id_no_masked`, DF-ACE-074 `id_no_last4`, DF-ACE-078 `contact_value`, DF-ACE-079 `contact_value_masked` and DF-ACE-059 `date_of_birth`, the area `QUEUE_AND_ALLOCATION`, the letters C, R, U, D and A, the scopes OWN, TEAM, REGION and ALL, and the messages MSG-P4-002, MSG-P4-003, MSG-P4-001 and MSG-GEN-004. It supports REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011.

Where the sources do not fix the contract shapes — what the authorise request and answer carry, what the `/masking-policies` answer holds, what the audit record carries and how a failure maps to a status — the contract states the shape in force and records the open point as Not specified in the source documents (GAP-1405; ASM-2448) and (GAP-1405; ASM-2449).

### 3. Preconditions

- Wave 0 is the platform wave: the shared libraries are published once and every later epic binds them (Architecture v5 slide 38).
- Architecture v5 slide 10 fixes the authorisation model the contract publishes: each service authorises the object itself with cached permission data from rwb-access, 2 s timeouts and a circuit breaker per downstream, deny by default.
- Architecture v5 slide 14 names the access operations and the two events the contract refers to: `POST /authorise` (role, scope, DoA), `GET /me/permissions`, `GET /doa-limits`, `/masking-policies`, and `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`.
- Architecture v5 slides 20 and 35 fix the cache-refresh rule, the deny-by-default rule and the rule that personal data never travels in events, workflow payloads or logs.
- ADR-010 fixes the identity boundary the contract restates: the clear identity number never leaves ACE, there is no token store, and `id_no_last4` is the clearest identity value any role can receive.
- The Ownership Map keeps `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` with P4 rwb-access and `lov_value` with P3 rwb-case; the contract names those tables and owns none of them (DP-01, DP-07).
- The unmasking answer for `interaction.summary` comes from the rwb-access authorise contract under DP-08, applied for the caller's roles; `data_product_access` is P1's data product access catalogue and not the masking authority (GAP-0584). The matrix, role and masking tables stay with P4 rwb-access, the entity registry and ACE views with P1 rwb-source-data, masking is applied by rwb-source-data at the data read, and the platform library publishes the guard and annotations only (GAP-0358).
- The paths of the three consumed operations are reached at `/api/recovery/access/v1/…` under the per-service base rule of §R4, because slide 14 names the operations and the Ownership Map has no path row for them (GAP-1405; ASM-2448).
- The library is published as one versioned artefact with major version 1, its contract shapes and its fakes, pinned by the service template; the coordinates themselves are Not specified in the source documents (GAP-1405; ASM-2449).
- No build dependency: the contract is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Fix the three interfaces: `AccessGuard.check`, `ScopeGuard.describe` and `MaskApplier.fill`, with their input and output types and their exceptions, and the rule that each is synchronous and one hop at most.
2. Fix the fail-closed rule in the interface documentation: a 2 s timeout, a circuit breaker per downstream, deny by default, 503 on an unreachable, timed-out or malformed access owner, and no caching of a failed or malformed answer.
3. Fix the scope descriptor: the type OWN, TEAM, REGION or ALL with the user, team and region codes; the contract states that the owning service applies it in its own query and that the library returns no record.
4. Fix the annotation: `@PersonalData("DF-…")` on a response field, and the masked-versus-clear source rule — masked column or last-four value where the policy does not allow the clear value, the clear value where it does, and masked where no rule covers the field.
5. Fix the error vocabulary: 403 `MSG-P4-002` for a denied right, 404 `MSG-P4-003` for a record outside the descriptor, 503 MSG-GEN-006 with no business data for a failure of the access owner, and the audit record shape with the case id, the field id and the flag `clear` or `masked`, never the value.
6. Fix the negative statements: the library owns no table, holds no login and no token, and no method, parameter, cache entry or fake accepts a clear identity number.
7. Fix the consumed surface: the three access operations and the two access events, with their owner, their base and their call type.
8. Publish the fakes: an authorise fake with allow, deny, unreachable and malformed answers, a masking-policy fake, a scope fake and an audit fake.
9. Wire the contract test and the drift test into the build of every consuming service, and publish the contract document with the nine tables of section 12.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A service implements its own guard instead of calling `AccessGuard` | The contract test fails and the build is refused | None | AC1, AC6 |
| X2 | A service passes a clear identity number to the masker | The signature does not compile; no overload accepts it | None | AC5 |
| X3 | The access owner is unreachable, times out or answers malformed | 503, fail closed, nothing cached, no business data in the answer | MSG-GEN-006 | AC1 |
| X4 | A service applies the descriptor to another service's table or query | The boundary test fails on the cross-schema reference and the build is refused | None | AC2 |
| X5 | A field is annotated but no rule covers it | The contract states that the field is masked | None | AC3 |
| X6 | A rule names the clear identity number | The access owner refuses the rule at load; the contract states the clearest value it can receive is `id_no_last4` | MSG-P1-002 (raised by P4) | AC5 |
| X7 | A service resolves another version of the library | The drift test fails the build with the pinned and the resolved version named | None | AC6 |
| X8 | An audit record is written with a value instead of a flag | The audit fake refuses the record and the contract test fails | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; the contract refers to the access owner, the data owner and the platform contracts by name only |
| Negotiable | The artefact coordinates and the payload details are agreed at the contract freeze; the interfaces, the annotation, the descriptor, the vocabulary and the fail-closed rule are fixed by the target architecture |
| Valuable | Unblocks every service CON and APP story that checks a right or masks a field, from Day 1, against one frozen contract and its fakes |
| Estimable | Three interfaces, one annotation, one value type, one error vocabulary, one audit shape and four fakes |
| Small | Fits two weeks with its contract tests |
| Testable | Every criterion below is a contract test that the build of a consuming service runs |

### 7. Acceptance criteria

```gherkin
Feature: Access guard and masker library contract

  Background:
    Given the platform library contract document is published with major version 1
    Given permission matrix version "PM-2026.11" is in force and masking version "MASK-SIT-01" is in force
    Given RW-CASEOWN holds "R" in Queue and allocation and RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"

  Scenario: AC1 The interfaces and the fail-closed rule are published (new, D-RCV-60)
    Given the contract jar of the platform library is published
    When a service compiles against it
    Then AccessGuard.check(ActionRef action, SessionRef session) returns a Decision of ALLOWED or REFUSED, with the area "QUEUE_AND_ALLOCATION" and the right "U" taken from the caller
    Then ScopeGuard.describe(SessionRef session) returns a ScopeDescriptor with type OWN, TEAM, REGION or ALL and the user, team and region codes
    Then MaskApplier.fill(Object dto, SessionRef session) returns the same dto with every annotated field filled, masked or left clear, and no method accepts a clear identity number
    Then every method is synchronous, is one hop at most, has a 2 s timeout and a circuit breaker per downstream
    Then an unreachable, timed-out or malformed access owner answers 503 with messageCode MSG-GEN-006 and nothing is cached, so deny by default holds

  Scenario: AC2 The scope descriptor contract and the rule that the owning service applies it (new, D-RCV-60)
    Given the published ScopeDescriptor of type "OWN" with user "U-2105" and the team and region codes
    When a consuming service receives it for a case read
    Then the descriptor carries no record and no query and the library runs no query of another service
    Then the owning service applies the descriptor in its own query and returns 12 records for 12 owned cases
    Then a record outside the descriptor, case "RW-2026-000456" in team "MTG-NE", is refused by the owner with 404 and message MSG-P4-003
    Then the descriptor of each type OWN, TEAM, REGION and ALL is the same shape, and the library states that it never returns a record

  Scenario: AC3 The annotation contract and the masked-versus-clear source rule (new, D-RCV-60)
    Given a response field annotated @PersonalData("DF-ACE-079") and a field annotated @PersonalData("DF-ACE-059")
    When the masker fills them for a session in "MASK-SIT-01"
    Then DF-ACE-079 is filled from the masked value the data owner supplies, and the clear contact value is requested only where the rule allows it for one of the session's roles
    Then DF-ACE-074 is filled from the last-four value and DF-ACE-078 from the clear value only where the rule allows it
    Then the field for DF-ACE-059, which no rule covers, is masked
    Then the contract states that a field with no rule is masked and that the masker holds no value of its own

  Scenario: AC4 The error vocabulary and the audit record shape are fixed (new, D-RCV-60)
    Given a denied right, a record outside the descriptor and a failing access owner
    When a consuming service raises each of the three through the contract
    Then the denied right is 403 with MSG-P4-002 and the handler does not run
    Then the out-of-descriptor record is 404 with MSG-P4-003 and the record is not returned
    Then the failing access owner is 503 with no business data in the body, the log or the trace
    Then every masked or clear read writes one audit record with the case id, the field id and the flag "clear" or "masked", and the audit fake refuses a record that carries a value

  Scenario: AC5 The library owns no table, holds no token and never receives the clear identity number (new, D-RCV-60)
    Given the published contract and its declared inputs
    When a service tries to give the library a schema, a table, a login or a token
    Then the contract has no parameter, no configuration key and no method for any of them
    Then role, permission, masking_rule, role_conflict, delegation_limit and lov_value are named only, as the tables of P4 rwb-access and P3 rwb-case
    Then the clearest identity value the contract carries is id_no_last4 and a clear identity number cannot be expressed
    Then the contract states that there is no token store (ADR-010)

  Scenario: AC6 The fakes and the drift test of every consuming service (new, D-RCV-60)
    Given the four published fakes: authorise with allow, deny, unreachable and malformed answers, masking policy, scope and audit
    When the contract test of a consuming service runs against the published jar
    Then the fake answers each of the four authorise variants and the service behaves as section 7 states for each
    Then a service that pins another version, overrides a class or re-implements a guard fails the drift test with the pinned and the resolved version named
    Then the fake set is the same for every consuming service and needs no access owner to be running
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is copied: legacy AC1 to AC13 belong to RWB-P4-E1037-APP, and their end-to-end form belongs to RWB-ITG-E1037-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The capability area and the right are checked before the handler runs, and a denied action changes nothing | permission.letters (DF-REF-043); REQ-ACA-007; CTL-09 |
| BR2 | Deny by default and fail closed: an unreachable, timed-out or malformed access owner is a 503 refusal, never an allow, and no failed answer is cached | Architecture v5 slides 10, 29 and 35; REQ-ACA-007 |
| BR3 | The library produces the scope descriptor and the owning service applies it in its own query; the library runs no query and returns no record | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
| BR4 | A personal data field is masked unless the masking policy in force lets one of the session's roles see it; a masked field is filled from the masked column or the last-four value, and a field with no rule is masked | Masking rules reference table; DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355 confirmed); CTL-11; REQ-ACA-005; DF-ACE-073, DF-ACE-079 |
| BR5 | Every masked or clear read writes one audit record with the case id, the field id and the flag, never the value | REQ-ACA-006; RWB-E1-039 BR3; NFR-040 |
| BR6 | The library owns no table, no login and no token: the matrix, masking, role, conflict and delegation data are P4 rwb-access's and the reference values are P3 rwb-case's | DP-01; DP-02; Ownership Map |
| BR7 | No clear identity number is expressible in the contract: no parameter, cache entry or fake accepts it, and `id_no_last4` is the clearest value | ADR-010; Data Tier Map section 7; D-RCV-35 U1 |
| BR8 | The policy is refreshed on `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` through the inbox, and a change takes effect within the time to live with no deployment | Arch v5 slide 20; RWB-E1-037 AC1; REQ-ACA-003 |
| BR9 | One version of the contract is pinned by the service template; a service that resolves another version, overrides a class or re-implements a guard fails its build | Arch v5 slides 20 and 38; RWB-PLT-NF02-APP |
| BR10 | No personal data in a log record, a span attribute, a metric label, an error body, a cache key or a fixture; personal data is logged only through the ACE Common PII logging path to the SOC (INT-34), and the Recovery business-event topics rwb.<service>.events.v1 are separate and carry no personal data | Architecture v5 slides 11 and 35; INT-34 |
| BR11 | The contract takes no business decision: it relays the access owner's decision and the data owner's value, and holds no delegation limit or approver role | Arch v5 slide 10; slide 35 note on attribute-based access control |
| BR12 | The two events the contract refers to are consumed by the consuming service through the library, under that service's own consumer group and inbox | Arch v5 slide 20 (cache refresh); RWB-PLT-TE006-CON |

### 9. State transitions

The contract fixes the states of a guard decision and of an annotated field; it holds no case status and no stored object of its own.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Contract version | 1 | A backward-compatible change to a payload, an attribute or a fake | Version 1, minor change | The pinned services build unchanged |
| Contract version | 1 | A breaking change to an interface, the annotation, the descriptor or the vocabulary | Version 2 with a migration note | A service moves only by changing the pin and passing the drift test |
| Guard decision | UNCHECKED | Allow, deny or failure of the access owner | ALLOWED, REFUSED or FAIL_CLOSED | The handler runs, is refused with 403, or is refused with 503 |
| Annotated field | UNFILLED | A rule allows the role a clear or a last-four view, or no rule covers the field | CLEAR or MASKED | The value is filled from the source the rule names, or masked, and the audit flag records which |

A published version is never edited in place; a breaking change is a new major version with a migration note.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform library team (any team, per U3) | Owns the interfaces, the annotation, the descriptor, the vocabulary, the fail-closed rule and the fakes; publishes version 1 and later versions |
| The service template owner | Pins exactly one version of the contract in the template and moves the pin with the build as the gate |
| The consuming squads of the 19 services | Compile and test against the published jar and its fakes, and raise a change request instead of a local override |
| The access owner (P4 rwb-access) | Owns the data and the authorise, permission and masking-policy operations the contract calls; the contract only names them |
| The data owner (P1 rwb-source-data) | Owns the ACE views and the masked and last-four columns the masker fills from |
| RW-COMPLY Compliance and PDPA officer | Sets the masking values behind the rules the contract refers to (DL26); the contract holds none |
| The security architecture reviewer | Confirms that the fail-closed rule, the annotation and the audit shape meet the architecture standards |
| No approval level from the delegation of authority applies | The contract takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-035, DF-REF-037, DF-REF-038 | role (P4 rwb-access) | role_code, role_class, default_scope | Named only: carried in the authorise and permission answers |
| DF-REF-040 to DF-REF-044 | permission (P4 rwb-access) | letters, matrix_version and the other fields | Named only: carried in the permission answer |
| DF-REF-198 to DF-REF-204 | masking_rule (P4 rwb-access) | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Named only: carried in the masking-policy answer |
| DF-ACE-073 | v_ace_customer (P1 rwb-source-data) | id_no_masked | Named only: the masked identity value a consuming service supplies |
| DF-ACE-074 | v_ace_customer (P1 rwb-source-data) | id_no_last4 | Named only: the clearest identity value the contract can carry |
| DF-ACE-059 | v_ace_customer (P1 rwb-source-data) | date_of_birth | Named only: masked where no rule covers it |
| DF-ACE-078 | v_ace_contact (P1 rwb-source-data) | contact_value | Named only: clear only where the rule allows it, and audited |
| DF-ACE-079 | v_ace_contact (P1 rwb-source-data) | contact_value_masked | Named only: the masked contact value |
| No data of its own | Library | None | The contract stores nothing, caches nothing on disk, holds no table and owns no schema |

Field IDs are those in the Logical Data Model and Data Dictionary. Every row is named and none is written by the library: the contract states the field id it annotates and the owner it comes from (DP-01). A contract that carried a value, a table or a token would break the identity boundary of ADR-010, so the shapes are published without one.

### 12. Contract

#### 12.1 REST operations provided

None. The library provides no REST operation and publishes no API document: it is a versioned artefact inside the consuming service. The authorise, permission and masking-policy operations belong to P4 rwb-access and the access-log operation to P4 rwb-access through RWB-P4-E1039-CON.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/access/v1/authorise | P4 rwb-access | The role, scope and delegation decision the guard asks for on a cache miss, a stale entry or a policy event |
| GET /api/recovery/access/v1/me/permissions | P4 rwb-access | The letters and the default scope in force, used to refill the cache after `rwb.access.AccessPolicyChanged.v1` |
| GET /api/recovery/access/v1/masking-policies | P4 rwb-access | The masking rules in force for the fields and roles of the session |

The contract fixes the call shape, not the service: each is one hop, 2 s timeout, breaker per downstream, deny by default, at the owner's `/api/recovery/access/v1` base (DP-11, DP-13, ADR-020). The paths are the base rule of §R4 applied to the operations slide 14 names, because the Ownership Map has no path row for them (GAP-1405; ASM-2448).

#### 12.3 Events published

None. The library publishes no event and owns no topic. `AccessPolicyChanged` and `DoaLimitChanged` are published by P4 rwb-access on `rwb.access.events.v1`.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | P4 rwb-access | Consumed by the consuming service through the library, to drop the cached permissions and masking policy |
| rwb.access.DoALimitChanged.v1 | rwb.access.events.v1 | P4 rwb-access | Consumed by the consuming service through the library, to drop the cached delegation band |

Both are consumed under the consuming service's own consumer group and recorded in its own `processed_event` inbox (RWB-PLT-TE006-CON); the library supplies the listener and not the consumer group, and a repeated delivery changes nothing.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity; the guard and the masker are synchronous calls inside the caller's handler or activity, and the contract states that no workflow code may call them with a personal value in the payload.

#### 12.6 Schedules

None. The contract owns no Schedule. The six-monthly access review list (JOB-18) is a P4 rwb-access Schedule and is not this story.

#### 12.7 Tables owned

None. The contract owns no table and no schema: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` are P4 rwb-access's tables and `lov_value` is P3 rwb-case's, named here only so that no consuming service reads them or copies them into a local store (DP-01, DP-07).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Authorise fake | `POST /api/recovery/access/v1/authorise` | Allow, deny, unreachable and malformed answers for area "QUEUE_AND_ALLOCATION" and right "U" (AC1, AC6) |
| Masking-policy fake | `GET /api/recovery/access/v1/masking-policies` | One rule that lets RW-CASEOWN see DF-ACE-078 in clear, and no rule for DF-ACE-059 (AC3) |
| Scope fake | The scope part of the authorise answer | Type OWN with user "U-2105" and the team and region codes, and type ALL for the comparison (AC2) |
| Audit fake | The access-log contract of P4 rwb-access | A recorder of the case id, the field id and the flag, and a refusal of a record that carries a value (AC4) |

The four fakes are published with the contract jar so that a consuming service needs no access owner to build or test (AC6).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | The authorise, permission and masking-policy operations of P4; the audit record goes through the access-log contract and adds no path |
| Kafka | 0 | 2 | `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`, consumed by the consuming service through the library |
| Temporal | 0 | 0 | No workflow, activity or Schedule; the calls run inside the caller |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** A versioned shared-library contract artefact of the platform: the three interfaces and the exceptions in `th.co.scb.ace.workbench.recovery.platform.api`, the annotation and the scope descriptor with them, the contract document and the fakes as resources of the same artefact. The implementation is the APP story of this legacy key, in `th.co.scb.ace.workbench.recovery.platform.access`. The artefact coordinates are Not specified in the source documents (GAP-1405; ASM-2449).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract states that the library owns no table and names the P4 and P3 tables only | none |
| DP-02 | `recovery_svc` login | One login per service. The contract states that the library holds no login and borrows none | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. Referred to; the consuming story carries the dependency | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The contract fills from the value the data owner supplies and reads no view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The time to live and the breaker settings are read through it | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The scope codes and the letter set are reference values, named and not owned | referred to; the consuming story carries the dependency |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. This story is the contract of that guard library | referred to; the consuming story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. Referred to for the activity context the guard is proven in | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The contract fixes the three consumed calls and their timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. Every consumed path uses the base of its owner and the library adds none | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The contract adds no migration and states that each service migrates its own | referred to; the consuming story carries the dependency |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The contract names no lake endpoint and no export | none |
| DP-19 | Screen, ace-web | gateway-bff composite route. The contract fixes the 403 and 404 answers the route renders; SCR-43 and SCR-47 are not built here | referred to; the consuming story carries the dependency |

The H and C dependencies named in the last column belong to the consuming stories and to RWB-PLT-E1037-APP; this contract story has no build dependency of its own, which is why its `H` and `C` rows in the metadata table read `None`.

**Hardware and software change.** The contract replaces the `recovery.access.matrix` package with a versioned artefact: the permission matrix and the masking rules are no longer read from the same database by the same process, but asked of their owner over three one-hop operations and cached per service against a published policy version. The ACE values reach the masker already masked or cut to the last four, through the data owner's contract. The contract adds no schema, no topic, no queue, no Schedule and no bucket, so no new hardware is implied: the artefact is published to the package registry and runs inside each service's existing pods on the existing AKS cluster.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessGuard` | Published interface | One method returning ALLOWED or REFUSED for an action and a session, with the pre-handler rule and the 403 `MSG-P4-002` (AC1, AC4) |
| `ScopeGuard` | Published interface | One method returning the `ScopeDescriptor`, with the statement that the owning service applies it (AC2) |
| `MaskApplier` | Published interface | One method filling the annotated fields from the masked, last-four or clear value the policy allows (AC3) |
| `@PersonalData` | Annotation | The field-id marker on a response field; the only way a field becomes maskable and auditable (AC3, AC4) |
| ScopeDescriptor | Value type | Type OWN, TEAM, REGION or ALL with the user, team and region codes, and no record (AC2) |
| Error vocabulary | Document | 403 `MSG-P4-002`, 404 `MSG-P4-003`, 503 with no business data, and the audit record shape (AC4) |
| Contract document | Document | The fail-closed rule, the timeout and breaker settings, the ownership and token statements, and the versioning rule (AC1, AC5) |
| Fakes and fixtures | Test asset | The four fakes of section 12.8 and the fixture set used by every consuming service (AC6) |

**Build steps**

1. Write the three interfaces, the annotation, the scope descriptor and the exception types; run the compile and drift test of a sample service (AC1, AC2, AC3).
2. Write the fail-closed rule into the interface documentation and prove it with the authorise fake: unreachable, timeout and malformed each answer 503 and cache nothing (AC1).
3. Write the error vocabulary and the audit record shape; prove the 403, the 404, the 503 and the refusal of a record that carries a value (AC4).
4. Write the ownership and identity statements and check that the contract has no parameter, key or method for a schema, a table, a login, a token or a clear identity number (AC5).
5. Publish the four fakes and wire the contract and drift tests into the build of a consuming service; test all four authorise variants and a service that pins another version (AC6).
6. Publish the contract document with the nine tables of section 12 and record the version and the compatibility rule.

**Done when.** The six criteria pass as contract tests, the four fakes are published with the jar, the nine tables of section 12 name their owner from the Ownership Map, and RWB-PLT-E1037-APP builds and passes its tests against the published jar.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The access owner reports that the session has ended; the contract relays it unchanged and does not retry | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A denied right, refused before the handler runs | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the scope descriptor, refused by the owning service | This case is not in your scope. |
| MSG-GEN-006 | The access owner is unavailable, times out or returns an unusable answer | {system} is not available. Try again in a few minutes. |
| MSG-GEN-004 | A consumed access operation answers 409; the contract relays it unchanged and the caller re-reads its permissions | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Not specified in the source documents (DOR-RWB-PLT-E1037-CON-9) | Not specified in the source documents (DOR-RWB-PLT-E1037-CON-9) |

The message ids and the wording are copied unchanged from RWB-E1-037; the contract adds no message of its own, and the Thai text of each follows DL10. Open decision DL10 stays open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive. The 503 fail-closed answer carries messageCode MSG-GEN-006 and traceId in the shared RFC 9457 Problem (RD-P1-004). It contains no business data.

### 15. Screens and states

No screen of its own. The contract has no user interface: what it fixes for the screens of the 19 services is the status and the message id a screen receives (403 `MSG-P4-002`, 404 `MSG-P4-003`, 503 with no business data), the masked value a field carries, and the rule that no screen error reveals a token, an internal path or a personal value. SCR-43 Roles and access and SCR-47 Personal data are Epic 8 and out of scope (DP-19). SCR-43 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-1323). SCR-47 empty, error and no access states: Not specified in the source documents (CG-ALL-1324).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1037-CON-01 | AC1 | Contract | A sample service compiles against the jar; area "QUEUE_AND_ALLOCATION" and right "U"; the four authorise fake variants, with 503 and no cache on the last two |
| TC-PLT-E1037-CON-02 | AC2 | Contract | A `ScopeDescriptor` of each type OWN, TEAM, REGION and ALL; the assertion that the descriptor holds no record and the library runs no query |
| TC-PLT-E1037-CON-03 | AC3 | Component | Annotated DF-ACE-079, DF-ACE-074, DF-ACE-078 and DF-ACE-059; values "XXXXXX5678", "0123" and "XXXXXXXXX1234"; the no-rule field masked |
| TC-PLT-E1037-CON-04 | AC4 | Contract | A denied right, an out-of-descriptor record, a failing access owner, one clear audit record and one audit record carrying a value that the fake refuses |
| TC-PLT-E1037-CON-05 | AC5, AC6 | Contract | A search of the published jar for a schema, a table, a login, a token or a clear identity number parameter; the four fakes and the drift test of a service that pins another version |

No test in this story is an integration copy: the contract is exercised against its own fakes, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in the contract: letters, scopes, masking positions, approver roles and the time to live are data or parameters behind the interfaces.
- No personal data in a payload, a fixture or a log; the interfaces carry field ids and IDs only.
- No schema, table, login or token in the contract: the library owns none, and the P4 and P3 tables are named only.
- A clear identity number cannot be expressed: `id_no_last4` is the clearest value the contract can carry, and there is no token store (ADR-010).
- Deny by default and fail closed on every failure of the access owner, with no business data in the 503 answer.
- A published version is never edited in place; a breaking change is a new major version with a migration note and a new pin.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR6, BR8, BR9 | TC-PLT-E1037-CON-01, TC-PLT-E1037-CON-05 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR4, BR7, BR10 | TC-PLT-E1037-CON-03, TC-PLT-E1037-CON-05 |
| REQ-ACA-007 | Access outside the matrix refused and recorded | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR2 | TC-PLT-E1037-CON-01, TC-PLT-E1037-CON-04 |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | Epic 1, 3.4 | FEAT-ACA-14 | All recovery processes | BR3 | TC-PLT-E1037-CON-02 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | Epic 2, 3.4 | FEAT-ACA-13 | All recovery processes | BR8, BR12 | TC-PLT-E1037-CON-01, TC-PLT-E1037-CON-05 |
| REQ-ACA-006 | Every read of a personal data field written to the access log | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR5, BR10 | TC-PLT-E1037-CON-04 |
| Legacy TC-E1-037-01, TC-E1-037-02, TC-E1-037-03, TC-E1-037-04, TC-E1-037-05, TC-E1-037-06, TC-E1-037-07, TC-E1-037-08, TC-E1-037-09, TC-E1-037-10, TC-E1-037-11, TC-E1-037-12, TC-E1-037-13, TC-E1-037-14, TC-E1-037-15 | The fifteen legacy test cases of RWB-E1-037, at component and end-to-end level | Epic 1, 3.4; Epic 2, 3.4; Program, 5.4 | FEAT-ACA-04, FEAT-ACA-05, FEAT-ACA-13, FEAT-ACA-14 | All recovery processes | BR1 to BR12 | executed by RWB-P4-E1037-APP and RWB-ITG-E1037-ITG |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1037-APP | App development | H: implements the three interfaces, the annotation, the scope descriptor, the cache and the audit writer against this contract, and passes the drift test this story publishes |
| RWB-P4-E1037-APP | App development | C: owns the permission matrix as data, the masking rules, the scope rule, the access log and the load and approve operations, and owns legacy AC1 to AC13 |
| RWB-P4-E1039 | App development | C: the access-log contract whose record shape this contract fixes |
| RWB-ITG-E1037-ITG | Integration | The end-to-end proof of the same business outcome across P4, P1 and the library |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | The parameters and reference-data clients the time to live, the breaker settings and the scope and letter values are read through |
| RWB-PLT-E1027-CON, RWB-PLT-TE006-CON | Contract | The decision-record library and the inbox contract the two policy events are consumed through |
| RWB-PLT-N001-CON | Contract | The gateway route that renders the 403 and the 404 this contract fixes |
| RWB-P1-E1069-APP | App development | The data owner of the ACE view fields the masker fills from |

### 19. Out of scope

- The permission matrix as data, the masking rules and the matrix load and approve operations: RWB-P4-E1037-APP.
- The access log store and its retention: RWB-P4-E1039.
- The ACE views and the masked read: RWB-P1-E1069-APP.
- The implementation of the interfaces, the cache and the audit writer: RWB-PLT-E1037-APP.
- The administration screens SCR-43 Roles and access and SCR-47 Personal data: Epic 8 (FEAT-ADM-01, FEAT-ADM-14).
- The masking values for each role and field: Compliance, DL26.
- The end-to-end proof across the wave 1 services: RWB-ITG-E1037-ITG.
- The token store, which does not exist: ADR-010.
- The six-monthly access review list (JOB-18) and the leaver reallocation of RWB-E1-030.
