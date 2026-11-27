# RWB-P4-E8006-APP Run the full administration screens

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8006-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-AZ |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8006-APP-16); the squad sizes it at refinement |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E8006-APP-23); only the /v1 path is stated |
| Depends on (build) | RWB-P4-E8006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-006 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator**, I want **one read of `rwb-access` that answers, capability area by capability area, what of the administration surface my role entitles me to open — with my letters, my default scope and the matrix, masking and list versions in force — and that records the open in the decision log with those versions**, so that **roles, queues, parameters, templates, panels and autonomy change from one place and without a code release, and no panel is rendered on the administration surface that my role does not entitle**.

Inside `rwb-access` this is the administration-home slice of the legacy story RWB-E8-006:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- One deliverable, and nothing else: the read `GET /api/recovery/access/v1/admin/home`, which answers an `AdminHome` of `areas[]` — one row per capability area in force in LOV-CAPABILITY, each with `capabilityArea`, `letters`, `scope` and `mayOpen` — plus `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain` and `recordedAt`.
- The rows are the answer to the "one place" of the legacy story: `letters` are the caller's `permission` letters in that area, `scope` is the caller's `role.default_scope`, and `mayOpen` is true where the letters are not a dash. The capability areas in force, with the version of the list that holds them, are read through DP-07 and never copied into code (BR-P4-017; AC4).
- The administration surface itself is composed at the edge: the gateway-bff composite route of DP-19 calls this read and, beside it, each owner's own panel list — queues and parameters of `rwb-case` (P3), templates of `rwb-comms` (P6), panels of `rwb-partner` (S9) and autonomy of `rwb-agent` (P10) — and renders only the panels the home entitles. `rwb-access` holds no panel list, no queue and no template (BR10).
- Every open appends one entry of the local decision-record chain of DP-03 in the same transaction as the answer, carrying the library's read code, the caller reference, the matrix and masking versions and the areas answered, with no case id. Where the entry cannot be written the answer is withheld with 503 and MSG-P7-003, because no action proceeds unlogged (R-UNI-39; legacy AC2).
- A caller without the Platform administration R letter is refused with 403 and MSG-P4-002 and nothing is answered or recorded. A caller with no session is refused with 401 and MSG-P4-001.
- The cache lifetime of the entitlement answer is a parameter row read through DP-06 with the version in force. Its name is Not specified in the source documents (GAP-0867; ASM-1569) and is fixed by this story and its contract.
- The two endpoints of the legacy story are other services' now and are not built here: `POST /admin/reference-loads` is `rwb-case`'s (P3) and the rule-version paths are `rwb-decision`'s (P7). `GET /admin/roles` is RWB-P4-E1019-APP's, `GET /me/session` another P4 story's and `GET /admin/access-log` RWB-P4-AD007-APP's. This story provides neither and duplicates none of them.
- No workflow is started, no Schedule is registered and no event of its own is published: the only message is `rwb.decision.DecisionRecorded.v1`. The six-monthly access review list (JOB-18) is RWB-P4-AD008-APP's.
- The operation, its fields, the parameter name, the entitlement rule of an area and the record code of a home read are Not specified in the source documents (GAP-0867; ASM-1568).

### 2. Business rationale

The administration surface is the reason the Workbench can change without a release. The FSD puts the target in one sentence: one place for roles, queues, parameters, templates, panels and autonomy, and rule and limit changes made without a code release at 100 percent, measured every month from the decision log and from the Workbench records (FSD P4 v3 A2.17.1). The problem the FSD names beside it is the one the legacy story carried: access, limits and rules live in documents and in people's heads, and a change needs a code release or a manual check (FSD P4 v3 A2.17.1; RWB-E8-006).

In the monolith that place was one screen that read the recovery schema directly, and the legacy story's two endpoints wrote reference loads and rule versions through it. In the target no service owns the whole surface: roles and permissions are held as data in `rwb-access` (REQ-ACA-002, REQ-ACA-003), queues and parameters in `rwb-case` (REQ-CWC-006), templates in `rwb-comms`, panels in `rwb-partner` and autonomy in `rwb-agent`. A single page therefore cannot be a single service's screen; it is a composite route at the edge (DP-19) and one entitlement answer that says, before any panel is drawn, what the caller may open. That answer is what this story builds, and it is the only part of the surface that must be decided by the service that owns the permission matrix.

The answer is also the audit unit of the surface. R-UNI-39 says no action proceeds unlogged, and the legacy criterion says the result is written to the decision log with the rule version (RWB-E8-006 AC1). Here the logged fact is the open of the administration surface itself: one entry, in the same transaction as the answer, naming the caller, the matrix and masking versions and the areas answered, so an auditor can show which entitlement view an administrator held when a role or a limit was changed. When that entry cannot be written the entitlement view is not given at all, which is the legacy "nothing changes and the user sees MSG-P7-003" carried onto a read (AC2).

The story meets REQ-ACA-013 (the full administration screens are available to the security administrator) directly, and it carries REQ-ACA-002, REQ-ACA-003 and REQ-CWC-006 on the entitlement side: the areas, the letters, the scope and the versions are rows and reference data, so a new role, a new letter or a new area needs no build. It supports the measure rule and limit changes made without a code release, because the surface that makes such a change possible cannot itself ship with a release.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8006-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the read, the `AdminHome` and `AdminHomeArea` schemas, the error envelope, the consumed-operation declarations and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry this story appends for every open, and its hash link to the entry before it |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the cache lifetime of the entitlement answer as a row with the version in force |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that composes the administration surface from this answer and each owner's own panel list, one hop per call |

Business preconditions carried from RWB-E8-006:

- The permission row of a role in a capability area is data: `permission.letters` holds C, R, U, D and A or a dash for none, with `permission.matrix_version` (TSD P4 v3 T3.1, DF-REF-040 to DF-REF-044; FSD P4 v3 A2.17.3.2).
- The roles that hold Platform administration R are RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM; RW-PLATADM holds CRUD there and RW-SECADM CRUDA (TSD P4 v3 T6.1).
- The role list is data and a role carries its class and its default scope: LOV-ROLE-CLASS is BANK_USER, PARTNER_USER and NON_HUMAN_ACTOR, and LOV-SCOPE is OWN, TEAM, REGION and ALL (TSD P4 v3 T3.2).
- The capability areas are the 14 values of LOV-CAPABILITY and are read through DP-07; no area is a constant in code (TSD P4 v3 T3.2; DP-07).
- The matrix, the masking policy and the role administration in force in SIT were loaded by RWB-P4-E1037-APP; this story reads their versions and changes none of them.
- The legacy screen table names SCR-39 Rules and parameters and SCR-43 Roles and access; in the target the entitlement home is the entry panel of the whole administration surface, and the panel lists are the owners' (DP-19).
- The entitlement rule of an area — which combination of letters makes an area openable, and which areas are read-only — is Not specified in the source documents (GAP-0867; ASM-1568).

### 4. Flow

1. The platform administrator opens the administration surface through the gateway-bff composite route (DP-19), which calls `GET /api/recovery/access/v1/admin/home` on `rwb-access` with the session of the signed-in user and no query parameter.
2. `AdminHomeController` resolves the caller's session. A caller with no session is refused with 401 and MSG-P4-001, and no read and no entry follow.
3. The controller calls the service's own `POST /api/recovery/access/v1/authorise`, one hop with a 2 s timeout and the answer cached for the session, for Platform administration R. A caller without the right is refused with 403 and MSG-P4-002, and nothing is read and nothing is written (AC3).
4. `EntitlementReader` reads the caller's `permission` rows and the caller's `role` row in `rwb_access`: the letters of each capability area, the matrix version they were written under, the role class and the default scope (DF-REF-034 to DF-REF-044).
5. `ReferenceListClient` reads LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS through the reference-data contract of DP-07 at the version in force, and takes `listVersion` from that answer. No area, class or scope is a constant in code (BR5).
6. `MaskingVersionReader` reads the masking version in force for the caller's role from `masking_rule` (DF-REF-198 to DF-REF-204) and puts it on the answer as `maskingVersion`.
7. `AdminHomeService` builds one row per capability area of the list in force, in the order of the list: `capabilityArea`, `letters` (a dash where the caller holds no letter), `scope` (the role's default scope) and `mayOpen` (true where the letters are not a dash and the area is not a read-only area of the administration surface). An area that is not in the list in force is never answered, and no area the caller does not hold is dropped from the answer: the row is present with `mayOpen` false, so the surface can render the difference (AC4).
8. The answer is an `AdminHome`: `areas[]` of step 7, `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain` and `recordedAt`, cached for the lifetime the parameter row of step 10 holds.
9. `AdminHomeRecorder` appends one entry of the local decision-record chain of DP-03 in the same transaction as the answer: the library's read code, the caller reference, `matrixVersion`, `maskingVersion`, the areas answered as a count and as a list, and no case id (AC5).
10. `ParameterReader` reads the cache lifetime of the answer through the parameters contract of DP-06 with the version in force. The value is a row and never a constant; its name is Not specified in the source documents (GAP-0867; ASM-1569) and is fixed as `access.home.cache.ttl.seconds` by this story and its contract.
11. Where the entry cannot be written, the transaction rolls back, nothing is cached and the answer is withheld: the call fails with 503 and MSG-P7-003, and no partial area list leaves the service (AC2; R-UNI-39).
12. The composite route of the gateway-bff merges this answer with each owner's panel list and renders the surface: a panel whose area is not entitled is not shown, and a panel whose owner does not answer is shown as unavailable and not as permitted.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller has no session | 401, no read and no entry | MSG-P4-001 | AC3 |
| X2 | The caller holds no Platform administration R | 403, no read, no entry and no area list | MSG-P4-002 | AC3 |
| X3 | The caller's role holds no letter in any area | 200 with every area row present and `mayOpen` false, and an empty `areas[]` is never answered | None | AC4 |
| X4 | The reference list read answers no version, or an area of the answer is not in the list in force | 503 and no answer; an area is never invented and a list without a version is never used | MSG-P7-003 | AC4 |
| X5 | The parameters read answers no value for the cache lifetime | The answer is served with the lifetime in force last known to the service, and no constant is used; the open is recorded | None | AC4 |
| X6 | The masking version of the caller's role is missing | 503 and no answer, because an entitlement view without its masking version cannot be defended | MSG-P7-003 | AC5 |
| X7 | The entry of the open cannot be written | 503, MSG-P7-003 and no area list; nothing is cached and nothing is left behind | MSG-P7-003 | AC2, AC5 |
| X8 | The same caller opens the surface twice | Two opens, two entries: the read is not idempotent and is not deduplicated | None | AC5 |
| X9 | The matrix version in force changes while a session is open | The next open answers the new `matrixVersion` with no build, no restart and no cache flush | None | AC4 |

No exception path of this story changes a role, a permission, a matrix, a masking rule or a case: this service reads its own tables and appends its own entries, and the state machine of access belongs to RWB-P4-E1037-APP and RWB-P4-E1039-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract of RWB-P4-E8006-CON and its fakes; reads the `role`, `permission` and `masking_rule` rows of its own schema and two reference and parameter contracts, and no panel list, queue or template |
| Negotiable | The operation name, the field names and the cache lifetime parameter are settled with the contract review; the areas, the letters, the scopes and the versions are data and reference data |
| Valuable | One answer makes the whole administration surface composable at the edge, and one entry makes each open auditable with the versions it was answered under |
| Estimable | One controller, one entitlement reader, one list client, one masking reader, one parameter reader, one recorder, one contract-fake run and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the refusal is provable against a role without the right and the withheld answer against a forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Run the full administration screens

  Background:
    Given the environment is SIT
    Given test user "U-2102" holds RW-SECADM with Platform administration CRUDA and the default scope "ALL"
    Given test user "U-2104" holds only RW-PHONECOL and holds no right in the capability area "PLATFORM_ADMINISTRATION"
    Given the permission matrix "PM-2026.11" and the masking version "MSK-2026.11" are in force

  Scenario: AC1 Run the full administration screens (legacy RWB-E8-006 AC1)
    Given the rwb-case contract mock returns reference version "REF-2026.11" in force with LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then gives administration one place for roles, queues, parameters, templates, panels and autonomy
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-006 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller without the Platform administration right is refused (new, D-RCV-60)
    Given test user "U-2104" holds only RW-PHONECOL
    When "U-2104" calls GET /api/recovery/access/v1/admin/home
    Then the response is 403 with message MSG-P4-002 and no area is answered
    Then no entry is written to the decision record
    When "U-2104" calls the same operation without a session
    Then the response is 401 with message MSG-P4-001 and no entry is written

  Scenario: AC4 One row per area of the list in force, with the three versions (new, D-RCV-60)
    Given the reference list LOV-CAPABILITY in force holds 14 areas
    When "U-2102" calls GET /api/recovery/access/v1/admin/home
    Then the answer carries 14 area rows, one per area of the list in force
    Then each row carries capabilityArea, letters, scope and mayOpen
    Then mayOpen is true only where the caller's letters are not "-"
    Then the answer carries matrixVersion "PM-2026.11", maskingVersion "MSK-2026.11" and listVersion "REF-2026.11"
    When the matrix version in force becomes "PM-2026.12"
    Then the next open answers matrixVersion "PM-2026.12" with no build and no restart

  Scenario: AC5 Exactly one entry per open, and no answer without its entry (new, D-RCV-60)
    Given test user "U-2102" holds RW-SECADM with Platform administration CRUDA
    When "U-2102" calls GET /api/recovery/access/v1/admin/home twice
    Then exactly two entries are written, one per open
    Then each entry carries the caller reference "U-2102", matrixVersion "PM-2026.11", maskingVersion "MSK-2026.11" and the areas answered
    Given the decision record store is forced to fail
    When "U-2102" calls the same operation
    Then the response is 503 with message MSG-P7-003 and no area is answered
    Then no entry is left behind and nothing is cached

  Scenario: AC6 The answer carries no personal field, no panel list and no other path, and reads its cache lifetime from a parameter row (new, D-RCV-60)
    Given the cache lifetime is a parameter row read at the version in force
    When "U-2102" calls GET /api/recovery/access/v1/admin/home
    Then the answer carries no name, no e-mail address and no personal field
    Then rwb_access holds no panel list for any area
    Then the cache lifetime is read from the parameter row and no lifetime is a constant in code
    Then rwb_access exposes no path other than the entitlement read of the administration home
    When the request arrives with no session
    Then the response is 401 with message MSG-P4-001 before any read

  Scenario: AC7 A path of rwb_access this story does not provide answers 404 (new, D-RCV-60)
    Given test user "U-2102" holds RW-SECADM with Platform administration CRUDA
    When "U-2102" calls a path of rwb_access that this story does not provide
    Then the response is 404 and no area is answered
```

AC1 and AC2 are the legacy criteria of RWB-E8-006, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the reference-data mock, so the answer is provable while the reference-data contract is still a fake. AC3 to AC7 are new under D-RCV-60 and test only what this story adds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The administration surface is opened from one entitlement answer of `rwb-access`: one row per capability area in force, with the caller's letters, the default scope and whether the area may be opened | RWB-E8-006 AC1; FSD P4 v3 A2.17.1 and A2.17.2 |
| BR2 | Every open of the surface appends one entry of the local decision-record chain with the caller reference, the matrix and masking versions and the areas answered, in the same transaction as the answer; an answer that cannot be recorded is not returned | R-UNI-39; RWB-E8-006 AC2; FSD P4 v3 A2.17.4.3 |
| BR3 | A caller must hold Platform administration R; a caller without it is refused with 403 and MSG-P4-002, and nothing is read or written | REQ-ACA-007; FSD P4 v3 A2.17.4.3 AC-EXC-P4-017-01; TSD P4 v3 T6.1 |
| BR4 | A caller with no session is refused with 401 and MSG-P4-001 before any read | FSD P4 v3 A2.3.4.3 AC-EXC-P4-003-03; API-P4-012 |
| BR5 | The capability areas, the scopes and the role classes are reference lists read with their version in force; no area, scope or class is a value in code, and the version of the list is on the answer as `listVersion` | BR-P4-017; DP-07; TSD P4 v3 T3.2 |
| BR6 | The matrix version and the masking version on the answer are the ones in force for the caller when the answer is built; a later version does not rewrite an entry already written | FSD P4 v3 A2.4.4.1; TSD P4 v3 T3.1 DF-REF-044 and DF-REF-202 |
| BR7 | An area the caller holds no letter in is answered with `mayOpen` false and is never dropped from the answer, so the surface can show what the role does not entitle | RWB-E8-006 AC1; ASM-1568 |
| BR8 | The surface is composed at the edge: the gateway-bff composite route merges this answer with each owner's panel list, and no panel is shown whose area the answer does not entitle. `rwb-access` holds no panel, queue or template | DP-19; Architecture v5 slide 14 |
| BR9 | The cache lifetime of the entitlement answer is a parameter row read with the version in force; no lifetime is a constant in code, and a changed lifetime needs no build | DP-06; FSD P4 v3 A2.17.3.1 BR-P4-017 |
| BR10 | This story provides no other operation: the role list, the session read, the access log, the reference loads and the rule-version paths are other services' and are neither provided nor duplicated | Ownership Map v1; TSD P4 v3 API-P4-007, API-P4-012; RWB-P4-E1019-APP, RWB-P4-AD007-APP |
| BR11 | The answer names the chain it was recorded in and the time it was recorded, so a printed answer is defensible without a second read | FSD P4 v3 A2.17.4.1; DP-03 |
| BR12 | The answer carries references, codes, versions, counts and times only: no name, no e-mail address and no personal field | NFR-040; TSD P4 v3 T6.2 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR5 and BR7 are one select over `permission` and `role` joined to the capability list in force, projected into one row per area with a computed `mayOpen`; the join is by the area code the list supplies, so an area missing from the list cannot appear and an area missing from the caller's permissions appears with a dash.
- BR2 is the record appender of DP-03 inside the transaction that builds the answer; the transaction commits the entry and the cached answer together, so a failed append leaves neither.
- BR3 is the authorise call in step 3 of section 4, on the caller's session and with the refusal mapped to MSG-P4-002.
- BR4 is the session resolution that precedes every other step; it writes nothing.
- BR6 is two columns of the answer read from the rows that were in force: `permission.matrix_version` and `masking_rule.masking_version`, neither computed from a current setting at render time.
- BR8 is the absence of a panel list in `rwb_access`: the service answers areas and entitlement, and the composite route holds the mapping from an area to a panel.
- BR9 is the parameter read of step 10 at the version in force.
- BR11 is the `chain` and `recordedAt` fields of the answer, written by the same append as BR2.
- BR12 is the field list of the answer in section 12.1: no field of a person is read or returned.

### 9. State transitions

This story holds no case, task, role or permission state. The states it answers are the states of an open, and the chain it writes is append-only.

| From | Event | Condition | To |
|---|---|---|---|
| No open | The surface is opened | Session present and Platform administration R held | Authorised, the answer is built |
| No open | The surface is opened | Session present and the right absent | Refused with MSG-P4-002, nothing written |
| No open | The surface is opened | No session | Refused with MSG-P4-001, nothing written |
| Authorised | The reference or parameter read answers | The lists answer with a version | Answer built |
| Authorised | The reference read answers no version | None | 503 with MSG-P7-003, nothing written |
| Answer built | The record is appended | The append commits | Answer returned and cached for the lifetime in force |
| Answer built | The record cannot be appended | The append fails | 503 with MSG-P7-003, no answer |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | An open of the surface | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| Append-only local chain | A matrix or masking version changes | New entries carry the new version; old entries keep theirs |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform administrator (RW-PLATADM, Platform administration CRUD) | Opens the surface and is the primary reader of the answer (FSD P4 v3 A2.17.3.3) |
| Security administrator (RW-SECADM, CRUDA) | Opens the same surface; the administrator the requirement REQ-ACA-013 names |
| Center of excellence analyst (RW-COE, R) | Opens the surface and reads the answer; its write panels are other stories' |
| RW-DATASTEW, RW-AUDIT, RW-COMPLY (R) | Hold Platform administration R and may open the surface; the same answer, the same entry |
| A role without Platform administration R | Is refused with 403 and MSG-P4-002 and learns nothing about the areas |
| The gateway-bff route | Calls this read and each owner's panel list, one hop each, and renders only the areas the answer entitles; it never caches an answer across users |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in its own schema, its own decision-record chain and its own records; it writes only entries of its own chain |
| `rwb-case` (P3), `rwb-comms` (P6), `rwb-partner` (S9), `rwb-agent` (P10) | Own their panels and their lists; this story calls their panel lists not at all and their parameter and reference contracts only as declared in section 12.2 |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002, and the unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the role class and the default scope of the caller, per role |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the letters of each capability area of the caller and the matrix version |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read: the masking version in force for the caller's role |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the entry of an open: `decision_code` DF-DEC-003 with the library's read code, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the caller reference, the matrix version, the masking version and the areas answered, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS with the version in force | Read through the reference-data contract (DP-07) |
| (parameters) | the parameter rows of `rwb-case` | the cache lifetime of the entitlement answer, with the version in force | Read through the parameters contract (DP-06) |
| DF-REF-205 to DF-REF-211 | `role_conflict` | none in this story | None: the conflict check is the sign-in story's |
| DF-REF-016 to DF-REF-026, 055 to 062 | `delegation_limit` | none in this story | None: the DoA table is RWB-P4-E2013-APP's and RWB-P4-E1038-APP's |
| (outbox) | outbox library table in `rwb_access` | the record row of an open | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `queue`, `template`, `rule_row`, `rule_package`, `lov_value`, `reference_version` or `reference_row` is read as a table and no row of `decision_log_entry` is read or written: the queue belongs to `rwb-case` (P3), the template to `rwb-comms` (P6), the rule registry to `rwb-decision` (P7), the reference data to `rwb-case` (P3) and the central ledger to `rwb-decision` (P7). No foreign key crosses a schema (DP-01).

The operation is `GET /api/recovery/access/v1/admin/home`, answering `AdminHome`: one row per capability area in force with `capabilityArea`, `letters`, `scope` and `mayOpen`, plus `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain` and `recordedAt`. The cache lifetime is the parameter row `access.home.cache.ttl.seconds`, read through DP-06. The open entry uses the decision-record library's read code. The composite route and the panel lists are RWB-PLT-N001-CON's. The field types and the rule that decides `mayOpen` for a read-only area are Not specified in the source documents (GAP-0867; ASM-1568) and are fixed by the contract of RWB-P4-E8006-CON. Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/home` | P4 `rwb-access` | None | `AdminHome`: `areas[]` of `AdminHomeArea` — `capabilityArea`, `letters`, `scope`, `mayOpen` — plus `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain`, `recordedAt` | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only; no Idempotency-Key |

One row per capability area of the list in force, in the order of the list, 14 rows in the LOV-CAPABILITY of TSD P4 v3 T3.2. `letters` is the caller's `permission.letters` value or a dash, `scope` is `role.default_scope`, and `mayOpen` is true where the letters are not a dash and the area is not a read-only area of the administration surface. The operation is a new path on the base `/api/recovery/access/v1` of DP-13 and it changes no other operation of the service: `GET /admin/roles` stays API-P4-007 of RWB-P4-E1019-APP, `GET /me/session` stays API-P4-012 and `GET /admin/access-log` stays API-P4-008 of RWB-P4-AD007-APP.

The operation name, the field names and the entitlement rule are Not specified in the source documents (GAP-0867; ASM-1568): the shape above is the one this story and its contract fix, and the review confirms it with the security administrator before the endpoint is frozen.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Platform administration R check behind the read, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The cache lifetime of the entitlement answer, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS in force (DP-07) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the reference and parameter answers are cached for the life of the request and the authorise answer for the session. No operation of `rwb-comms`, `rwb-partner`, `rwb-agent` or `rwb-decision` is called: the panel lists are the composite route's, not this service's (BR8).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of an open of the administration surface, with the caller reference, the matrix version, the masking version and the areas answered |

CloudEvents 1.0 envelope; the payload carries references, codes, versions and times and no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: `AccessPolicyChanged` is RWB-P4-E1037-APP's and `DoaLimitChanged` is RWB-P4-E1038-APP's.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and an entitlement answer needs no subscription.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.6 Schedules

None. The open of the surface is request-driven.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the class and the default scope of the caller's role |
| `permission` | P4 (`rwb_access`) | Read only: the letters of each capability area and the matrix version |
| `masking_rule` | P4 (`rwb_access`) | Read only: the masking version in force for the caller's role |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of each open. Read: nothing in this story |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of each appended entry; no inbox row, because no event is consumed (DP-09) |
| `role_conflict`, `delegation_limit` | P4 (`rwb_access`) | Not read and not written: the conflict check is the sign-in story's and the DoA table is another story's |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |

`lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling and are read through DP-07; `queue` is P3's, `template` is P6's, `rule_package` and `rule_row` are P7's and `partner_user` is S9's. No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E1037-CON, RWB-P4-E8006-CON | The granted answer with Platform administration R for RW-PLATADM, RW-SECADM, RW-COE, RW-DATASTEW, RW-AUDIT and RW-COMPLY, and the refused answer with MSG-P4-002 for RW-PHONECOL |
| decision-record fake | RWB-PLT-E1027-CON | The append of an open entry, the hash-link check, and the forced write failure of AC5 |
| parameters fake | RWB-P3-E1042-CON | The cache lifetime of the entitlement answer as a parameter row with the version in force |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with its 14 areas, LOV-SCOPE and LOV-ROLE-CLASS at version REF-2026.11 |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of the administration surface: the entitlement panel of this answer and the panel lists of P3, P6, S9 and P10 |

Fake library version: Not specified in the source documents (DOR-RWB-P4-E8006-APP-22).

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1; consumed 3 | Base `/api/recovery/access/v1`; one hop, 2 s timeout |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/adminhome`, Java package `th.co.scb.ace.workbench.recovery.access.adminhome`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process read of the role, queue, parameter, template and rule tables of one schema (DP-01 and DP-03: the entitlement rows of this service's own schema and a local hash-linked entry for every open) and the ace-web screen that drew the whole administration surface in process (DP-19: a composite route at the edge). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AdminHomeController | Controller | The read: session resolution, the authorise call, the RFC 9457 problem responses |
| AdminHomeService | Service | One row per area of the list in force, the letters, the scope, `mayOpen` and the three versions |
| EntitlementReader | Service | The `permission` and `role` rows of the caller with the matrix version, the role class and the default scope |
| MaskingVersionReader | Service | The masking version in force for the caller's role from `masking_rule` |
| ReferenceListClient | Client | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS through DP-07 with the version in force, one hop, 2 s timeout |
| ParameterReader | Client | The cache lifetime through DP-06 with the version in force, one hop, 2 s timeout |
| AdminHomeRecorder | Service | The entry of the open with its outbox row, in the transaction that produces the answer (DP-03, DP-09) |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role`, `permission` and `masking_rule` are created by RWB-P4-E1037-APP and the local decision-record table by RWB-P4-E1039-APP in the per-service sequence of DP-15; this story reads them and appends to the chain.
- The read predicates are the caller's role id, the capability area and the validity window of the masking rule; if the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration, not to a new one here.
- The only write of this story is the append through the DP-03 library, and it commits in the same transaction as the cached answer: a failure rolls both back and the answer is not returned (MSG-P7-003).

**Configuration and reference data**

- The cache lifetime of the answer is a parameter row of `rwb-case` read through DP-06 with the version in force; no lifetime is a constant in code (BR9). Its name is fixed by the contract of RWB-P4-E8006-CON.
- LOV-CAPABILITY (14 areas), LOV-SCOPE and LOV-ROLE-CLASS are read through DP-07 at the version in force (RWB-P3-E1043-CON); no area, scope or class is a constant in code (BR5).
- The matrix version and the masking version are columns of the rows in force; the answer never computes a current version at render time (BR6).

**Build steps**

1. `EntitlementReader` over `permission` and `role` with the matrix version and the default scope; test that a caller with a dash in every area gets every row with `mayOpen` false (BR7).
2. `ReferenceListClient` over the reference-data fake, and `AdminHomeService` building one row per area of the list in force; tests for AC4, including a list of 14 areas and an area the caller does not hold.
3. The authorise call of step 3 and the two refusals of X1 and X2; tests for AC3.
4. `MaskingVersionReader` and the `maskingVersion` field; test that a changed masking version changes the answer and no old entry (BR6).
5. `ParameterReader` over the parameters fake; test that a changed lifetime is data and needs no build (BR9).
6. `AdminHomeRecorder` and the 503 when the entry cannot be written; test for AC2 and AC5 (TC-E8-006-04).
7. The contract-fake run of the read through the gateway-bff fake, so the surface can be demonstrated while the panel owners are being built.
8. The denial test through the guard for a role without Platform administration R, and the service-identity test of section 10.

**Feature switch.** The read is a read path and carries no switch of its own. The entitlement panel is shown on the administration surface by the gateway-bff route when the service baseline is on (RWB-P4-E1037-CON); this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; the answer holds one row per area of the list in force with the caller's letters, scope and `mayOpen`; the matrix, masking and list versions are on the answer and a changed matrix version changes it with no build; a caller without Platform administration R is refused with MSG-P4-002 and nothing is written; every open leaves exactly one entry with the caller reference and the two versions; and a forced record failure withholds the answer with 503 and MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | This story, before any read |
| MSG-P4-002 | The caller holds no Platform administration R | You cannot {action} here. Your role does not include it. | This story, at the authorise step |
| MSG-GEN-001 | A required field of the answer has no value in the rows in force | Enter {field}. | This story, when the answer cannot be built from the rows |
| MSG-P7-003 | The entry of the open cannot be written, or a version the answer needs is missing | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, before the answer leaves |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | RWB-P4-E1039-APP's grant; this story carries it on the answer when the session holds one |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The two business texts this story returns are copied unchanged from the legacy story RWB-E8-006 (MSG-P4-001, MSG-P4-002 and MSG-P7-003) and from the FSD (MSG-GEN-001). No message text is invented here.

### 15. Screens and states

The entitlement home is the entry panel of the administration surface, served by the gateway-bff composite route of DP-19, which calls this read and each owner's panel list in parallel, one hop each, and merges the answers.

| Screen | State | What it shows |
|---|---|---|
| Administration surface | Home, entitled | One card per capability area of the answer with `mayOpen` true, each card opening the owner's panel for that area |
| Administration surface | Home, not entitled | The areas of the answer with `mayOpen` false, shown as not available and not clickable; the surface never hides them and never invents one |
| Administration surface | Home, versions | The matrix version, the masking version and the list version in force, with the time the answer was recorded and the chain it was recorded in |
| Administration surface | Home, masked areas | The masking version the caller's role sees, so a personal field of a panel is rendered under the version the answer named |
| Administration surface | Home, refused | The MSG-P4-002 refusal for a role without Platform administration R; no card is shown |
| Administration surface | Home, not recorded | The 503 of X7 with MSG-P7-003 and an invitation to try again; no card is shown |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | Panel of an entitled area | The owner's panel, reached from the card of the area the answer entitled; the panel content is the owner's story's, not this story's |
| SCR-39 Rules and parameters | Empty, loading, error, no access | Not specified in the source documents (DOR-RWB-P4-E8006-APP-10; CG-ALL-5431) |
| SCR-42 Queues and service levels | Empty, loading, error, no access | Not specified in the source documents (DOR-RWB-P4-E8006-APP-10; CG-ALL-5432) |
| SCR-43 Roles and access | Empty, loading, error, no access | Not specified in the source documents (DOR-RWB-P4-E8006-APP-10; CG-ALL-5433) |
| SCR-47 Personal data | Empty, loading, error, no access | Loading and list per Screen Specifications v1 SCR-47; empty, error and no access: Not specified in the source documents (CG-ALL-5434; DOR-RWB-P4-E8006-APP-10) |
| Administration surface | Break-glass warning | The banner with MSG-P4-004 and the end time of the grant, over the cards, when the session holds an active grant |

The legacy story named SCR-39 Rules and parameters and SCR-43 Roles and access on the same screen table; the target keeps both as panels of one composite surface, reached through the cards of the entitlement answer. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work. This story renders no screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-006-01 | AC1, BR1, BR2 | Contract | The read over the contract fakes: 14 area rows from LOV-CAPABILITY at version REF-2026.11, the matrix version PM-2026.11, the masking version MSK-2026.11, and one entry for the open with the versions |
| TC-E8-006-02 | AC2, BR2 | Component | The record store forced to fail during an open: 503, MSG-P7-003, no area list and no cached answer, and nothing changed |
| TC-E8-006-03 | AC3, BR3 | Component | Test user U-2104 with RW-PHONECOL and no Platform administration R: 403, MSG-P4-002, no area and no entry |
| TC-E8-006-04 | AC2, BR2 | NFR | A forced decision-record write failure on the open, repeated under load: 503 and MSG-P7-003 every time, no answer and no entry left behind |
| TC-E8-006-05 | AC4, BR5, BR6, BR7 | Component | A list in force of 14 areas, a caller with a dash in 12 of them, and a change of matrix version from PM-2026.11 to PM-2026.12 with no build |
| TC-E8-006-06 | AC5, BR6, BR11 | Component | Two opens by U-2102: exactly two entries, each with the caller reference, the two versions and the areas answered, and no case id |
| TC-E8-006-07 | ASM-3438; section 12.7 | Component | Boundary reads of `role`, `permission` and `masking_rule` as listed in section 12.7; the boundary values are Not specified in the source documents (DOR-RWB-P4-E8006-APP-12) |
| TC-E8-006-08 | BR4 | Component | A request with no session: 401, MSG-P4-001, and no read of any table |
| TC-E8-006-09 | BR8 | Component | An answer with one area the caller does not entitle: that area is answered with `mayOpen` false, and `rwb_access` holds no panel list for it |
| TC-E8-006-10 | BR9 | Component | A changed cache lifetime in the parameter row read through DP-06, at the version in force, with no build |
| TC-E8-006-11 | BR10 | Contract | The contract of RWB-P4-E8006-CON: no path other than the entitlement read of the administration home is exposed by `rwb_access` |
| TC-E8-006-12 | BR12 | Contract | The field list of the answer: no name, no e-mail address and no personal field is present |
| TC-E8-006-13 | AC6, BR4, BR8, BR9, BR10, BR12 | Component | A read of the answer with no name, e-mail address or personal field; no panel list in rwb_access; the cache lifetime read from its parameter row; no path other than the entitlement read; no session gives 401 and MSG-P4-001 before any read |
| TC-E8-006-14 | AC7 | Component | U-2102 calls a path of rwb_access this story does not provide: 404, and no area answered |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-006-01 for AC1, TC-E8-006-02 for AC2, TC-E8-006-03 for the access refusal and TC-E8-006-04 for the forced record failure; two rows are added for the new criteria of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. The ITG copy of the set is the integration story's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the capability areas, the scopes and the role classes are reference lists with a version (BR5), the cache lifetime is a parameter row (BR9), and a test proves that a new area or a changed lifetime needs no build.
- No personal data anywhere: the answer carries area codes, letters, scopes, versions and times, and no name, e-mail address or personal field appears in the answer, the entry or the tests (BR12, NFR-040).
- No read of another service's tables (DP-01): `queue`, `template`, `rule_package`, `rule_row`, `partner_user`, `lov_value` and `decision_log_entry` are their owners', and no join crosses a schema.
- One writer for the chain: only the append of DP-03 writes the decision record, and this story has no update and no delete, so an open can never rewrite an entry.
- No answer without its record: the entry commits with the answer and the answer is withheld with MSG-P7-003 when it cannot be written (BR2, R-UNI-39).
- The entitlement answer is the only gate: no panel list is held here and the surface cannot show an area the answer does not entitle (BR8).
- A refused caller learns nothing: the refusal names the missing right and nothing else, and no area list is returned with it.
- ACE data only through the owner's contract or the service's own `v_ace_*` view; this story reads neither, because an entitlement answer needs no ACE field.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | Program, Access and audit | FEAT-ADM-01 | 20 Administer access and audit | BR1, BR5 | TC-E8-006-01, TC-E8-006-05 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | Program, Access and audit | FEAT-ADM-01 | 20 Administer access and audit | BR3, BR6, BR7 | TC-E8-006-01, TC-E8-006-03, TC-E8-006-05 |
| REQ-CWC-006 | Roles, teams, queues and capacity are held as versioned reference data and change without a code release | Program, Case and workflow | FEAT-ADM-01 | 20 Administer access and audit | BR5, BR8 | TC-E8-006-01, TC-E8-006-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 BRD | FEAT-ADM-01 | 20 Administer access and audit | BR1, BR8, BR11 | TC-E8-006-01, TC-E8-006-06 |

The requirement IDs are the four rows this story serves; each is taken from the FSD "Requirements served" table and the Program BRD under the fill order of Template and Rules §R7.3, because the Work Package carries no requirement list for this story.

| Legacy reference | Where it is kept |
|---|---|
| AC1 one place for roles, queues, parameters, templates, panels and autonomy, with the result written to the decision log with the rule version | Sections 4, 7, 8, 12.1, 12.3, 15 |
| AC2 not recorded: nothing changes and MSG-P7-003 | Sections 4, 7, 8, 5 (X7), 14 |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The permission checks on Reference data C and Rules and parameters C | Sections 3, 10: the two writes are other services' stories, and this story checks Platform administration R for the open |
| TC-E8-006-01 to TC-E8-006-04 | Section 16 |
| Rule IDs R-UNI-39 (no action proceeds unlogged) | Sections 2, 8, 17 |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-DEC-001 to DF-DEC-018 | Section 11 |
| Legacy screens SCR-39 and SCR-43 as the story named them | Section 15, carried to the composite administration surface |
| Legacy entities `queue`, `rule_row`, `template` and `decision_log_entry` as the story named them | Sections 11 and 12.7: owned by P3, P7, P6 and P7, read not at all |
| Legacy endpoints `POST /admin/reference-loads` and `POST /admin/rule-versions` | Section 19: P3's and P7's, not built here |
| Legacy key RWB-E8-006, story RWB-P4-E8006-APP, contract RWB-P4-E8006-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The role list, the permission matrix, the masking rules, the role conflict pairs and the delegation table as data: RWB-P4-E1037-APP and RWB-P4-E2013-APP. This story reads their versions.
- `GET /admin/roles`: RWB-P4-E1019-APP. `GET /me/session`: another P4 story's. `GET /admin/access-log` and its export: RWB-P4-AD007-APP. The break-glass grant: RWB-P4-E1039-APP. This story provides none of them.
- `POST /admin/reference-loads` and the reference-load approval, verification and rollback: `rwb-case` (P3) and the P4 reference-load stories RWB-P4-AD009-APP and RWB-P4-AD010-APP.
- `POST /admin/rule-versions` and the rule-package paths: `rwb-decision` (P7), with the P4 rule stories RWB-P4-AD011-APP and RWB-P4-AD012-APP as ingest and approval only.
- The rule change of RWB-P4-E8007-APP, the approval-limit move of RWB-P4-E8008-APP, the product policy edition of RWB-P4-E8009-APP and the template approval of RWB-P4-E8010-APP.
- The panel lists of the other owners: queues and parameters of `rwb-case` (P3), templates of `rwb-comms` (P6), panels of `rwb-partner` (S9) and autonomy of `rwb-agent` (P10).
- The composite route specification and the screen field list of the administration surface: RWB-PLT-N001-CON and the Epic 8 screen work.
- The entity that writes an access event for a read: RWB-P4-E1039-APP. This story appends its own open entry only.
- The central decision ledger, the chain verification and the daily seal: `rwb-decision` (P7).
- The access review list (JOB-18) and its six-monthly Schedule: RWB-P4-AD008-APP.
- The integration harness and the `-ITG` copies of the test cases; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability.
