# RWB-P4-AD003-APP Scope per role

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: first issue for rwb-access — the microservice change for legacy RWB-AD-003: the scope of a role held as data, the predicate every service applies, the out-of-scope refusal and the access-policy event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD003-APP |
|---|---|
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP08, DP13, DP19 |
| Parallel lane | L-P4-C |
| Ready to start | Day 1 |
| Depends on (build) | `RWB-P4-AD003-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-P4-E1037-CON`, `RWB-PLT-N001-CON` |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As an **application owner**, I want **each role given a scope of own cases, team, region or all as data in `rwb_access`, and that scope applied as one predicate in every service that answers a case, so that a person sees only the cases their role allows and a record outside it is answered as not found and recorded**, so that **the legacy rule that lived inside one process over one schema becomes a published value and a published predicate that rwb-access owns and every consumer applies in its own query**.

The story builds the scope slice of P4 on the contract baseline of RWB-P4-AD003-CON: the two operations that read and change a role's scope, the four values of `LOV-SCOPE`, the predicate `scope` + `teamCode` + `regionCode` + `caseOwnerRef` returned to the guard of RWB-PLT-E1037-CON, the refusal of a record outside it with MSG-P4-003 and one local decision-record entry, and the publication of `rwb.access.AccessPolicyChanged.v1` with change kind `SCOPE`. What a role may do is not built here: the permission matrix is RWB-P4-E1037-APP's, masking is RWB-P4-AD004-APP's, separation of duty is RWB-P4-AD005-APP's and sign-in is RWB-P4-AD001-APP's. rwb-access holds no case row and runs no case query; the case owner, team and region columns are P3's, named only (ASM-3735).

### 2. Business rationale

The design decision is one deployable service per module with one schema and one login (DP-01, DP-02), contract-first REST with one hop and a 2 s timeout (DP-11), and one authorise contract plus one guard library that every service binds (DP-08). In the monolith the scope was a column that the same connection read while it filtered the case query; there was one shape because there was one process. Once the case query belongs to rwb-case and the role row to rwb-access, the scope has to travel as a value and a predicate, and the refusal has to be a rule both sides agree, or every consumer invents its own.

That is the risk this story removes. Without a stated predicate a consumer compares the wrong column — a queue code for a team code, a branch for a region — and leaks cases, or refuses everything and hides work. Without a stated refusal a consumer answers 403, which confirms that a record exists, or returns an empty page with a total, which tells the caller how many records were hidden. Without a recorded refusal the PDPA and audit reading of who reached what stops at the screen. And without one access event every service that caches permission data refreshes on its own guess (REQ-ACA-009, REQ-ACA-007).

The microservice change is therefore narrow and precise: the value moves from a code constant to a `role` row (REQ-ACA-002), the enforcement moves from the monolith's interceptor to the guard library in the owner's query (DP-08, DP-19), the refusal moves from a local exception to a 404 with MSG-P4-003 and an `AC-DENY` entry on `rwb.decision-record.v1` (DP-03), and the change becomes one event on `rwb.access.events.v1` (DP-09 by reference). Business values stay out of code: the four scope values and the messages are data and catalogue rows (BR-P4-014).

### 3. Preconditions

- `RWB-P4-AD003-CON` is the baseline this story builds against: the two operations, the three schemas, the predicate shape, the refusal and the event are fixed there and consumed here unchanged.
- `RWB-PLT-E1027-CON` gives the local decision-record library, its append and the shared topic `rwb.decision-record.v1`; `RWB-PLT-E1037-CON` gives the `AccessGuard`/`ScopeGuard` interfaces, the scope descriptor type and the fakes; `RWB-P4-E1037-CON` publishes the authorise answer of which the scope element is a part; `RWB-PLT-N001-CON` gives the gateway-bff composite route for SCR-43.
- Service baseline: schema `rwb_access`, one login per service (DP-02), base `/api/recovery/access/v1` (DP-13), topic `rwb.access.events.v1`, task queue `rwb-access`, Java package `th.co.scb.ace.workbench.recovery.access`.
- TSD P4 v3 T3.1 fixes `role.default_scope` (DF-REF-038, `LOV-SCOPE`, varchar(8), required) and T3.2 fixes the list `OWN`, `TEAM`, `REGION`, `ALL`; T6.2 fixes the rule "scope filters every query".
- TSD P4 v3 T6.1 fixes the rights this story reads: Platform administration R for a read and C for a change — RW-SECADM CRUDA, RW-PLATADM CRUD, RW-AUDIT R, RW-COE R, RW-DATASTEW R, RW-COMPLY R, and "-" for every business role.
- The case columns the predicate is compared with are P3's: DF-CAS-009 `owner_user_id`, DF-CAS-011 `team_code` (`LOV-TEAM`), DF-CAS-012 `region_code` (`LOV-REGION`) of `rwb_case` (TSD P3 v3 T3.1).
- No source gives the scope read or the scope change a path or a right: the legacy key names only `GET monolith-base/admin/roles`, the Ownership Map has no scope row and TSD P4 v3 T-A has no scope path — **Not specified in the source documents (GAP-2265; ASM-3735)**.
- No source fixes the predicate payload, the refused-entry codes or the version rule of a scope — **Not specified in the source documents (GAP-2265; ASM-3735)**.
- The legacy master and the Epic 8 BRD carry no approved status in this run; stories proceed in Draft by the D-RCV-60 overlay (ASM-3734). Release 30 June 2027 is copied unchanged and marked tentative (U7).

### 4. Flow

1. On start-up the service loads its own Flyway baseline, the `role` and `permission` rows in `rwb_access`, and binds the guard, the decision-record library and the outbox from the service template.
2. `GET /api/recovery/access/v1/admin/role-scopes` answers every role in force with its scope value and the four `LOV-SCOPE` values as the enumeration; the caller's Platform administration R letter is checked first and the view is filtered by the caller's own scope.
3. `PATCH /api/recovery/access/v1/admin/role-scopes/{roleCode}` takes the new value under `If-Match` and `Idempotency-Key`, validates the role (exists, active), the value (in `LOV-SCOPE`) and the required fields, and refuses 422 with MSG-GEN-001 before any write.
4. The change writes `default_scope` of the one role row, appends one local decision-record entry with decision code `AC-CHG` through the library of DP-03, and publishes `rwb.access.AccessPolicyChanged.v1` with change kind `SCOPE`, the role code and the new value through the outbox.
5. Where the entry cannot be written the change is not stored and the answer is 503 with MSG-P7-003; where the `If-Match` version is stale the answer is 409 with no write and no entry.
6. The scope element travels in the authorise answer of RWB-P4-E1037-CON as `scope`, `teamCode`, `regionCode` and `caseOwnerRef`; the caller's own team and region codes come from the session of RWB-P4-AD001-APP, and the descriptor type stays the library's.
7. A consumer's guard applies the predicate in its own query: `OWN` matches `caseOwnerRef` against the case owner, `TEAM` matches `teamCode` against the case team code, `REGION` matches `regionCode` against the case region code, `ALL` adds no field comparison. Scope is applied before the permission letter is checked.
8. A record outside the predicate is answered 404 with MSG-P4-003, with no field of the record and no count of the excluded records, and one entry with decision code `AC-DENY` and reason code `OUT_OF_SCOPE` is appended; where that entry cannot be written the answer is 503 with MSG-P7-003 and the record is not returned.
9. SCR-43 renders the role list, its scope and the access log through the gateway-bff composite route; no screen calls a service directly and no screen chains two calls.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller has no Workbench role in the session | The call is refused before any row is read; the refusal is one `AC-DENY` entry | MSG-P4-001 | AC2, TC-AD-003-03 |
| X2 | The caller holds a role whose Platform administration letter is "-" | The call is refused with no row and no count disclosed | MSG-P4-002 | AC2, TC-AD-003-03 |
| X3 | The posted value is outside `LOV-SCOPE`, or a required field is empty | 422 with the field named; no row is written, no entry, no event | MSG-GEN-001 | TC-AD-003-03 |
| X4 | The `If-Match` version is stale, or the role code does not exist or is inactive | 409 for the stale version, 404 for the unknown or inactive role; nothing is written | None specified for 409 | X4 |
| X5 | The decision-record library answers 503 while a change is being recorded | The change is not stored; the role keeps its value in force | MSG-P7-003 | TC-AD-003-04 |
| X6 | A caller reaches a record outside the predicate | 404 with no field, no header and no count; one `AC-DENY` entry with reason code `OUT_OF_SCOPE` | MSG-P4-003 | AC2, TC-AD-003-02 |
| X7 | The refusal entry cannot be written | 503; the record is not returned, so a refusal is never silent | MSG-P7-003 | TC-AD-003-04 |
| X8 | The access owner does not answer inside the 2 s budget while a consumer builds its predicate | The consumer answers 503 for that read and never answers a record it could not bound; the breaker opens per downstream | MSG-GEN-006 | X8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Yes: one legacy key, one service, one lane. It builds on CON baselines only (all five H rows are CON stories) and changes no other service. |
| Negotiable | The scope values and the messages are business-owned data and catalogue rows; the paths, the predicate field names and the entry codes are the contract's and are negotiable only through RWB-P4-AD003-CON. |
| Valuable | Every screen that lists a case depends on it: without it the case list is either over-exposed or empty, and the refusal is unattributable (REQ-ACA-009, REQ-ACA-007). |
| Estimable | Yes: two operations, two tables, one library binding, one event and one screen state, all fixed by the contract baseline. |
| Small | Yes: one release at wave 4 with no workflow, no schedule and no migration beyond the two tables of the service baseline. |
| Testable | Yes: four legacy test cases with the four scope values, the 404 refusal and the forced record failure; every cross-service answer is a contract mock. |

### 7. Acceptance criteria

```gherkin
Feature: Scope per role

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given a role's scope is the "default_scope" of its "role" row and its values are "OWN", "TEAM", "REGION" and "ALL"

  Scenario: AC1 Own scope (legacy RWB-AD-003 AC1)
    Given the rwb-case contract mock returns only the cases the caller owns
    Given a case owner with scope Own
    When they list cases
    Then the system returns only cases they own

  Scenario: AC2 Out of scope (legacy RWB-AD-003 AC2)
    Given a case owned by another team
    When a case owner with scope Team opens it
    Then the system does not find the response and the refusal is logged
```

Both criteria are the legacy criteria of RWB-AD-003 copied word for word, with the origin tag, the value `Own` of AC1 and the value `Team` of AC2 unchanged. One line is added to AC1 and nothing else: the faked answer of the case read, whose owner is P3 rwb-case, so that "returns only cases they own" is observable without a case row in this service (DP-11, one hop, `rwb-case` contract mock). No value of either criterion is replaced.

AC1 is answered by the scope value of the role row and by the predicate this story publishes; it is observed through the case list, whose query the consumer's guard filters. AC2 is answered by the same predicate and by the refusal rule of BR8: the record is not found, the answer is 404 with MSG-P4-003 and one `AC-DENY` entry with reason code `OUT_OF_SCOPE` is written, which is what "the refusal is logged" means in the target. The 404 is rendered by the record's owner; the rule, the message, the reason code and the entry are this story's. Neither criterion restates a value of RWB-P4-E1019-APP, RWB-P4-E1037-APP or RWB-P4-AD001-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A role's scope is the `default_scope` of its `role` row in `rwb_access`, one value of `LOV-SCOPE`; no scope value and no role code is written in code | Legacy RWB-AD-003 story line; TSD P4 v3 T3.1 (DF-REF-038) and T3.2; BR-P4-014 |
| BR2 | `LOV-SCOPE` is `OWN`, `TEAM`, `REGION`, `ALL`; a value outside the list is refused 422 before any row is written | TSD P4 v3 T3.2; FSD P4 v3 A2.14.3.1; MSG-GEN-001 |
| BR3 | `OWN` compares `caseOwnerRef` with the case owner, `TEAM` compares `teamCode` with the case team code, `REGION` compares `regionCode` with the case region code, `ALL` adds no comparison; the predicate carries those four fields and no fifth | FSD P4 v3 A2.14; TSD P3 v3 T3.1 (DF-CAS-009, DF-CAS-011, DF-CAS-012); ASM-3735 |
| BR4 | Scope is applied before the permission letter is checked, so a record outside the scope is never named and the excluded count is never returned | FSD P4 v3 A2.14; FSD P4 v3 VR-P4-014-1; REQ-ACA-009 |
| BR5 | The scope read needs Platform administration R and the scope change needs C; no Workbench role is 401 with MSG-P4-001, a missing letter is 403 with MSG-P4-002, and both are recorded | TSD P4 v3 T6.1 and API-P4-007; FSD P4 v3 VR-P4-001-1; legacy RWB-AD-003 Permission checks |
| BR6 | A change is checked before the row is written: the role exists and is active, the value is in `LOV-SCOPE`, the `If-Match` version is current, the required fields are filled | FSD P4 v3 A2.14.3.1; TSD P4 v3 T3.1; MSG-GEN-001 |
| BR7 | Every change appends one local decision-record entry (`AC-CHG`) through the library of DP-03 and publishes `rwb.access.AccessPolicyChanged.v1` with change kind `SCOPE`; where the entry cannot be written the change is not stored | DP-03; Architecture v5 (topic `rwb.access.events.v1`); ASM-3735 |
| BR8 | A record outside the predicate is answered 404 with MSG-P4-003 "This case is not in your scope.", with no field of the record and no count, and one entry (`AC-DENY`, reason code `OUT_OF_SCOPE`) is appended | Legacy RWB-AD-003 AC2; FSD P4 v3 VR-P4-014-1 and AC-EXC-P4-014-01; ASM-3735 |
| BR9 | Where the refusal entry cannot be written the answer is 503 with MSG-P7-003 and the record is not returned: a refusal is never silent and a reach is never answered as a success | Legacy RWB-AD-003 TC-AD-003-04; MSG-P7-003; DP-03 |
| BR10 | The guard of DP-08 applies the predicate in the owning service's own query and returns no record; rwb-access runs no query over a case and holds no case row | Architecture v5 slides 10 and 14; RWB-PLT-E1037-CON; ASM-3735 |
| BR11 | A scope change needs no second approval: the security or platform administrator writes it under the C letter and the entry names the actor and the time; the change is not versioned, its history is the decision record | TSD P4 v3 T6.1; ASM-3735 |
| BR12 | A consumer applies the changed scope when it next refreshes on `rwb.access.AccessPolicyChanged.v1`; until then the answer it cached stays in force and no answer mixes two scopes | Architecture v5 (consumers of `rwb.access.events.v1`); FSD P4 v3 A2.14 |

### 9. State transitions

None for a case, a task or a session. The state this story owns is the scope value of one role row; its history is the decision record.

| From | Event | Condition | To |
|---|---|---|---|
| A role with no row in this service | the role load of RWB-P4-E1019-APP writes the role | The role file passes its checks | The role carries a value of `LOV-SCOPE` and the catalogue answers it |
| A role with scope `OWN` | the security administrator posts `TEAM` | Value in `LOV-SCOPE`, `If-Match` current, entry written | The row carries `TEAM` from the commit; one `AC-CHG` entry and one `AccessPolicyChanged` with kind `SCOPE` |
| A role with scope `TEAM` | the same value posted again | The value equals the value in force | No transition: no write, no entry, no event |
| A role with scope `REGION` | a check fails, or the entry cannot be written | 422, 409 or a 503 from the library | The role keeps `REGION`; nothing is stored and nothing is published |
| Any scope | a caller reaches a record outside the predicate | The record does not match the predicate of the caller | 404 with MSG-P4-003 and one `AC-DENY` entry with reason code `OUT_OF_SCOPE` |
| Any scope | the refusal entry cannot be written | The library answers 503 | 503 with MSG-P7-003; the record is not returned |

TSD P4 v3 T4 gives a rule package version the lifecycle `LOADED` to `REFUSED` (`LOV-VERSION-STATUS`). This story adopts none of it: `role` carries no version and no effective date, so a scope change is a current value with a recorded decision and not a version (ASM-3735).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (per-service login, DP-02) | Answers the scope read, writes a scope change, runs the checks, builds the predicate, appends the entries and publishes the access-policy event |
| RW-SECADM, security administrator | CRUDA in Platform administration: maintains and reads every role's scope, and reads the entries of the changes and refusals |
| RW-PLATADM, platform administrator | CRUD in Platform administration: maintains and reads every role's scope |
| RW-AUDIT, internal audit | R in Platform administration: reads the scopes and the entries; writes nothing |
| RW-COE, center of excellence analyst | R in Platform administration: reads the scopes only; a scope is not a rule package or a parameter |
| RW-DATASTEW and RW-COMPLY | R in Platform administration: read the scopes for the data-product and the PDPA reading of the same rows |
| Every business role (RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and the rest) | Uses the scope of its own roles when a case list or a case is answered, and is refused out-of-scope records with MSG-P4-003; holds no right in Platform administration |
| RW-REFADM, reference data administrator | R in Rules and parameters and no right in Platform administration: maintains no scope, which is not reference data |
| Every other service identity (SY-* and the 19 services) | Receives the scope-predicated answer through the guard and reads no operation of this story; no agent bypasses the predicate |
| Delegation of authority | No level of `delegation_limit` applies: a scope is role administration, not a credit decision |

The scope is role administration, not reference data. `role` and `permission` are P4's own tables under the Ownership Map, and the reference-data contract of rwb-case holds `lov_value`, `reference_row` and `reference_version` only; `LOV-SCOPE` is carried as this service's own list constraint (ASM-3735). The legacy Permission checks table gives this key one row, Platform administration R, for API-P4-007 `GET /admin/roles`; that read belongs to RWB-P4-E1019-APP and is neither restated nor changed here. The legacy Endpoints table gives no write endpoint, so the two scope operations and their rights are the contract's decision recorded in RWB-P4-AD003-CON (GAP-2265; ASM-3735).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | `id` | Read |
| DF-REF-035 | `role` | `role_code` | Read, and the key of the change path |
| DF-REF-036 | `role` | `role_name` | Read |
| DF-REF-037 | `role` | `role_class` | Read |
| DF-REF-038 | `role` | `default_scope` | Read and write — the scope of this story |
| DF-REF-039 | `role` | `entra_group` | Read |
| DF-REF-041 | `permission` | `role_id` | Read |
| DF-REF-042 | `permission` | `capability_area` | Read |
| DF-REF-043 | `permission` | `letters` | Read — the R and C of the caller |
| DF-REF-044 | `permission` | `matrix_version` | Read |
| — | role row standard columns | `version`, `is_active`, `updated_at`, `updated_by` | Read; `version` is the `If-Match`, `updated_at`/`updated_by` are written by the change |
| — | decision record (library of DP-03) | entry id, decision code, reason code, actor, role code, scope value, time | Write |

The legacy Data table also named `recovery_case` (DF-CAS-001 to DF-CAS-023), `assignment` (DF-WRK-009 to DF-WRK-016) and `decision_log_entry` (DF-DEC-001 to DF-DEC-018). `recovery_case` and `assignment` are P3's and `decision_log_entry` is P7's; they appear in this story only as the columns DF-CAS-009, DF-CAS-011 and DF-CAS-012 that the predicate is compared with, in P3's own query, and as the shared topic the local entry is forwarded to (ASM-3735). No foreign key crosses a schema and no table outside `rwb_access` is read or written.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1` (DP-13). The shapes are RWB-P4-AD003-CON's and are implemented here unchanged.

| Method | Path | Shape | Access |
|---|---|---|---|
| GET | `/admin/role-scopes` | `RoleScopePage`: query `scope`, `roleClass`, `page`, `size` (default 50, max 200); each role in force with its scope value and the four `LOV-SCOPE` values | Platform administration R |
| PATCH | `/admin/role-scopes/{roleCode}` | `RoleScopeChange` in with `If-Match` and `Idempotency-Key`; the role out with its new scope and the entry reference | Platform administration C |

Both operations are served through the gateway-bff composite route for SCR-43 (DP-19). Errors: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 unknown or inactive role, 409 stale `If-Match` or a repeated key answered differently, 422 a value outside `LOV-SCOPE` or a missing field (MSG-GEN-001), 503 the entry not written (MSG-P7-003). The read is safe and repeatable; the change is idempotent by `Idempotency-Key`, and a repeated key returns the first answer and writes no second change.

#### 12.2 REST operations consumed

None. This story consumes no operation of another service at run time. The case list behind AC1 is P3's own `GET /cases` and appears only as the `rwb-case` contract mock in tests (DP-11); rwb-access holds no contract dependency on it and no case row is read.

| Called by | What it uses | Owner |
|---|---|---|
| Every service that authorises a record | The scope element of the authorise answer, and the guard that applies it in its own query | P4 for the data, RWB-PLT-E1037-CON for the library |
| SCR-43 through gateway-bff | The composite route over the two operations of 12.1 | P4 for the operations, RWB-PLT-N001-CON for the route |

#### 12.3 Events published

| Event | Topic | Contract element |
|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | Change kind `SCOPE`, the role code, the new scope value, the actor and the time |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Entry id, decision code (`AC-CHG` for a change, `AC-DENY` for a refusal with reason code `OUT_OF_SCOPE`), role code, scope value, time |

Both messages use the CloudEvents 1.0 envelope (id, source, type, specversion, time, subject, datacontenttype) written through the outbox of the service template, with a retry topic and a `.dlt` topic. No message carries a person, a case, a case count, a name, an e-mail address or an identity number.

#### 12.4 Events consumed

None. `rwb-access` is the owner of the access answer, not a subscriber of it; the service adds no subscription to this capability.

#### 12.5 Workflows and activities

None. Both operations are synchronous REST answers in the caller's thread: no workflow, no activity, no signal, and no Temporal dependency. The six-monthly access review Schedule (`JOB-18`) is RWB-P4-AD008-CON's; a scope is applied inside a request and never by a workflow.

#### 12.6 Schedules

None. Nothing about a scope runs on a clock.

#### 12.7 Tables owned

| Table | Owner | Use contracted here |
|---|---|---|
| `role` | P4 (`rwb_access`) | `default_scope` (DF-REF-038) is the scope; the code, name and class travel with it; `version` is the `If-Match` |
| `permission` | P4 (`rwb_access`) | The Platform administration R and C letters of the caller (DF-REF-040 to DF-REF-044), read only |
| `recovery_case`, `assignment` | P3 (`rwb_case`) | Not read and not written; DF-CAS-009, DF-CAS-011 and DF-CAS-012 are named as the columns the predicate is compared with, in P3's query |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written; the local entry is the library's and reaches P7 on `rwb.decision-record.v1` |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | Not read; `LOV-SCOPE` is this service's own constraint (ASM-3735) |

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` role-scope WireMock (from RWB-P4-AD003-CON) | The two paths of 12.1 with one role of each `LOV-SCOPE` value, one change of `OWN` to `TEAM` with its entry reference, the stored answer for a repeated key, 409 stale version, 422 MSG-GEN-001, 404 unknown role, 403 MSG-P4-002 and 503 MSG-P7-003 | This story, the screen tests, the wave 4 harness |
| Scope predicate fake (with RWB-PLT-E1037-CON) | A predicate of each of the four values with `teamCode`, `regionCode` and `caseOwnerRef`, the `TEAM` predicate of a session with no team code, and no record | This story, every consuming service |
| `rwb-case` case-list mock (RWB-P3-E1018-CON) | `GET /cases` returning only the cases the caller owns, and the out-of-scope case answering 404 with MSG-P4-003 | This story, AC1 and AC2 |
| Decision-record fake (RWB-PLT-E1027-CON) | The `AC-CHG` and `AC-DENY` appends, the hash-chain check and 503 with MSG-P7-003 | This story, TC-AD-003-04 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | The scope read and the scope change under `/api/recovery/access/v1`; the predicate travels in the authorise answer and is applied by the consumer, one hop, 2 s timeout |
| Kafka | 2 published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`; `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None | No workflow, activity or Schedule |
| File | None | No file in this story |

### 13. Solution plan

**Deliverables.** The two REST resources and their OpenAPI-generated interfaces, the `role` and `permission` read/write layer, the `LOV-SCOPE` enumeration as data and as schema, the scope assembler that fills the library descriptor, the guard binding for the consumer side, the `AC-CHG` and `AC-DENY` appends through the decision-record library, the outbox record for `rwb.access.AccessPolicyChanged.v1`, the SCR-43 list and change states, and the four test classes of section 16.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none — the caller's identity arrives in the ACE sign-in claim and no `v_ace_*` view is read here |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H `RWB-PLT-E1037-CON`; C `RWB-P4-E1037-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` → `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-43 | H `RWB-PLT-N001-CON` |

DP-05 is applied by keeping the boundary: the caller's user, team and region codes come from the session, and no ACE view or ACE table is read. The C row `RWB-P4-E1037-CON` does not block the build: the story builds against its published fake (DP-11).

**Build steps.** (1) Flyway step for the two tables in `rwb_access` and the `LOV-SCOPE` constraint, if the service baseline does not already carry them. (2) Read and change services with the checks of BR5 and BR6. (3) Scope assembler and guard binding against the library fake. (4) Decision-record append and outbox record with the entry reference returned in the change answer. (5) SCR-43 states through the gateway-bff route. (6) Contract tests and the four test classes, then the acceptance run of section 16.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. | The session holds no Workbench role (VR-P4-001-1) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The caller lacks the R or C letter of Platform administration |
| MSG-P4-003 | Error | This case is not in your scope. | A record outside the predicate (VR-P4-014-1) |
| MSG-GEN-001 | Error | Enter {field}. | A required field is empty or a value is outside `LOV-SCOPE` |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision-record library answers 503 |

409 for a stale `If-Match` and 404 for an unknown or inactive role code are answered as RFC 9457 problem details with no business text, because no message id is fixed for them in the sources (GAP-2265; ASM-3735). No message contains a person, a case number, a count or a field value.

### 15. Screens and states

| Screen | States | Route |
|---|---|---|
| SCR-43 Roles and access | List of roles with scope, class and the four values; Scope change (value, `If-Match`, confirm); Refused (MSG-P4-002); Validation (MSG-GEN-001); Conflict (stale version); Recording failed (MSG-P7-003); Access log tab | gateway-bff composite route over `GET /admin/role-scopes` and `PATCH /admin/role-scopes/{roleCode}`, and the existing `GET /admin/access-log` of RWB-P4-AD007-APP |

The screen shows the four `LOV-SCOPE` values as labels, never as free text, and shows no case data: it is a role administration screen. A refusal the screen shows is the 404 of a case read rendered by the case screen, not a screen of this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-003-01 | AC1 | Component | Role RW-CASEOWN with scope `OWN` owning 12 cases; the `rwb-case` mock returns those 12 only; the list returns 12 and a total of 12 |
| TC-AD-003-02 | AC2 | Component | Case `RW-2026-000456` in team `MTG-NE` under another owner; session scope `TEAM`; the read is 404 with MSG-P4-003, no field, no count, and one `AC-DENY` entry with `OUT_OF_SCOPE` |
| TC-AD-003-03 | Access | Contract | Role RW-PHONECOL, Platform administration letter "-": `GET /admin/role-scopes` is 403 with MSG-P4-002; no role row with a right is 401 with MSG-P4-001 |
| TC-AD-003-04 | Principle 5 | Component | The decision-record library forced to 503 on change and on refusal: the change is not stored (MSG-P7-003) and the refused record is not returned (MSG-P7-003) |

The four legacy test case IDs are kept unchanged; their level is assigned here (§R7.2). The data of each case is a business value already named in the legacy key or in FSD P4 v3 A2.14; no new business value is introduced.

### 17. Guardrails

- No business value in code: the four `LOV-SCOPE` values, the messages and the right letters come from data or from the message catalogue (BR-P4-014).
- No PII in events, workflow inputs or logs: the access-policy event and the decision entry carry a role code and a scope value only; a refusal entry carries no case number, no owner and no count.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE table and no `v_ace_*` view; the caller's codes come from the session.
- One schema, one login: every read and write of this story stays inside `rwb_access` under the per-service login (DP-01, DP-02).
- A refusal is indistinguishable from an absence and is always recorded; a record is never returned unbound and never answered as a success.

### 18. Traceability

| Item | Source |
|---|---|
| Legacy key and criteria | RWB-AD-003 (Administration Stories v3), AC1 and AC2, copied with the origin tag in section 7 |
| Legacy test cases | TC-AD-003-01 to TC-AD-003-04, kept unchanged in section 16 |
| Legacy data | `role` DF-REF-034 to DF-REF-038; `recovery_case`, `assignment` and `decision_log_entry` named only (section 11) |
| Feature and requirement | FEAT-ACA-14 "Scope a user's cases by team and region"; REQ-ACA-009, with REQ-ACA-003 and REQ-ACA-007 for the matrix and the refusal (FSD P4 v3 A2.14, Requirements served); TSD P4 v3 T8 maps REQ-ACA-009 to the sign-in story as well (ASM-3735) |
| Specification | FSD P4 v3 A2.14 (VR-P4-014-1, BR-P4-014, AC-P4-014-01, AC-EXC-P4-014-01); TSD P4 v3 T3.1, T3.2, T6.1, T6.2 and T-A.1 (API-P4-007) |
| Epic and release | Service epic RWB-SVC-P4 at arch wave 1; business epic EP08 at wave 4 by the W-MAP; release 30 June 2027 (tentative) |
| Gaps and assumptions | GAP-2265; ASM-3734 to ASM-3735 |
| Contract baseline | RWB-P4-AD003-CON (this key), RWB-P4-E1037-CON (authorise answer), RWB-PLT-E1037-CON (guard), RWB-PLT-E1027-CON (decision record), RWB-PLT-N001-CON (route) |

### 19. Out of scope

- The permission matrix and its versioned load: RWB-P4-AD002-APP and RWB-P4-E1037-APP.
- Masking of personal fields by role: RWB-P4-AD004-APP.
- Separation of duty and role conflicts: RWB-P4-AD005-APP.
- Sign-in, group mapping and the session answer: RWB-P4-AD001-APP and RWB-P4-E1022-APP.
- Break-glass grants and the access-log search and export: RWB-P4-AD006-APP and RWB-P4-AD007-APP.
- The role catalogue load itself, and its first roles: RWB-P4-E1019-APP.
- The delegation of authority table and its limits: RWB-P4-AD016-APP.
- The case query, the case owner, team and region columns and the rendering of the 404: P3 rwb-case (RWB-P3-E1018-CON).
- The central decision ledger and its hash chain: P7 rwb-decision.
