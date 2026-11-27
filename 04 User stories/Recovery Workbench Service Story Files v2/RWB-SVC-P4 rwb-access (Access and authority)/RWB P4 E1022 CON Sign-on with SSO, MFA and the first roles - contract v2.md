# RWB-P4-E1022-CON Sign-on with SSO, MFA and the first roles

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-022 for rwb-access — the published access contract of the key: authorise, me/permissions and the refusal vocabulary. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 13 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Screens | None defined by this contract; the states of SCR-43 and SCR-47 belong to the story that owns those screens |
| Open decisions | DL10 is open; the status of its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 is Not specified in the source documents (DOR-RWB-P4-E1022-CON-18) |
| Business epic | EP01 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P4-E1022-CON-14) |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E1022-CON-16) |
| Contract version built against | v1 (the /v1 path of both operations) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-001, FR-P4-002, FR-P4-003, FR-P4-004, FR-P4-006, FR-P4-007, FR-P4-019, FR-P4-033, FR-P4-035, FR-P4-037) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-access**, I want **the published access contract of this service — `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions`, with their request and answer shapes, their scope and version labels, their refusal vocabulary with message ids, the statement of what this service does not hold, and their fakes — instead of the monolith's published Java interfaces `AccessCheck` and `SessionResolver` inside one process**, so that **the edge and all 19 services can authorise and be tested from Day 1 against one frozen answer while the roles stay with P4**.

The contract is a contract before it is code. Two operations fix what a caller may ask and what it must never expect: the authorise answer tells a guard whether a resolved session may take an action in a capability area with a right, and the permission answer tells a caller what its own session holds. The refusal vocabulary fixes the status and the message id a caller receives, so a screen and a service show the same sentence. The negative statements keep the split honest: this service holds no session, no token and no password, publishes no event and consumes none, does not answer the delegation limits, and does not own the maintenance of the role-to-group mapping.

This is the contract slice of legacy RWB-E1-022. The legacy story published `AccessCheck.check`, `SessionResolver.resolve` and `AccessEventPublisher.publish` as Java interfaces in package `recovery.access.signin`, called in-process by every module's controller through a Spring method interceptor. In the 19-service target an in-process interface becomes a REST contract with a mock, one hop and a 2 s timeout (DP-11), and each service authorises its own object against it (Architecture v5 slide 10).

**The division is fixed and is the same in every story of this legacy key.** The seven criteria of the app story — legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9 — are carried by **RWB-P4-E1022-APP** word for word; the schema is **RWB-P4-E1022-DB**'s; and legacy AC1 and legacy AC3 belong to **RWB-ITG-E1022-ITG**, not to this key's app or contract story. This contract story copies no legacy acceptance criterion: every criterion in section 7 is tagged (new, D-RCV-60) and tests only the contract deliverable in the title, and the ten legacy test cases are executed by RWB-P4-E1022-APP and RWB-ITG-E1022-ITG (section 18).

### 2. Business rationale

In the monolith the answer to "may this session do this" was a method call on a Spring bean over a session object the same process held, and the answer was only available inside the Workbench. In the target the answer must be available to gateway-bff and to every service, each of which is a separate deployment with its own pods, its own schema and its own release cadence, and each of which must check its own object before the handler runs (Architecture v5 slide 10; ADR-020). Without a published contract each of them would implement the check against the tables of another service, which the schema rule forbids (slide 29), or call a path nobody published.

With the contract, four things become true at once. A consuming service compiles against one frozen answer from Day 1 and tests against its fake while rwb-access is still being built. The refusal vocabulary is one sentence in the screen, the service and the log. The version labels travel with the answer, so a session that resolved `PM-2026.11` keeps `PM-2026.11` until it ends (legacy BR7). And the negative space is stated once, for every reader: no event, no session store, no token, no delegation limit, no mapping maintenance — so a caller that wants one of them knows which story owns it instead of assuming this service will grow it.

The values the criteria use are the legacy values unchanged — matrix version `PM-2026.11`, conflict version `SOD-2026.11`, the role codes RW-CASEOWN, RW-PHONECOL, RW-LITOFF, RW-LEGAL and RW-SECADM, the groups `RWB-SIT-RW-CASEOWN` and `RWB-SIT-SY-RULES`, the managed identity SY-RULES, the area `PLATFORM_ADMINISTRATION` and `DOCUMENTS`, the rights C, R, U, D and A, the letters "CRU" and "CRUA", the scopes OWN, TEAM, REGION and ALL, the users U-1002, U-1004, U-1005, U-1006, U-1008 and U-1009, and the messages MSG-P4-001, MSG-P4-002, MSG-P4-005, MSG-P4-006 and MSG-GEN-006. It supports REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 and keeps control CTL-09 in place.

Where the sources do not fix the contract, it states the shape in force and records the open point: the two paths, because Architecture v5 slide 14 names the operations and the Ownership Map has no path row — Not specified in the source documents (GAP-0776; ASM-1403) — and the request and answer payloads, which no source fixes — Not specified in the source documents (GAP-0776; ASM-1404).

### 3. Preconditions

- Wave 1 is the wave of this service; the contract is published before the code of the app story, and the consuming services build against it and its fake (Template and Rules §R5.7; Architecture v5 slide 11).
- Architecture v5 slide 10 fixes the model the contract publishes: each service authorises the object itself, using cached permission data from rwb-access, 2 s timeouts, a circuit breaker per downstream, deny by default and a GET retried once with jitter.
- Architecture v5 slide 14 names the operations and the topic of this service: `POST /authorise` (role, scope, DoA), `GET /me/permissions`, `GET /doa-limits`, `/masking-policies`, and the events `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`.
- Architecture v5 slides 11, 20 and 35 fix the rules the contract restates: REST is one hop with a 2 s timeout and RFC 9457 problem details; a session lives in the Redis store of gateway-bff and a service holds no token; personal data never travels in an event, a workflow payload or a log.
- ADR-010 and ADR-020 fix the identity and the call boundary: staff sign-in is ACE Common's, there is no token store, and every REST contract is published before code with contract tests in every build.
- Architecture v5 slide 41 keeps `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` with P4 and slide 29 gives each service one login and its own schema; the contract names the tables it reads and owns none of them (DP-01, DP-02).
- The Ownership Map has no path row for `authorise`, `me/permissions`, `doa-limits` or `masking-policies`; the base is therefore the one of §R4 and DP-13, and the open point is carried as a gap (GAP-0776; ASM-1403).
- The OpenAPI 3.1 document, the error envelope, the fakes and their fixtures are published as one version of the contract, pinned by the service template of RWB-PLT-TPL.
- The test users, roles, groups and versions of the fixture are synthetic; no production entitlement, person or credential is read or published.
- No build dependency: the contract is Day 1 by rule (Template and Rules §R5.7), and its H and C rows in the metadata table read None for that reason.

### 4. Flow

1. Fix the two operations and their base: `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions`, OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream, RFC 9457 problem details (DP-11, DP-13).
2. Fix the authorise request: the role codes of the resolved session, the scope type and the team and region codes, the capability area, the right, and the delegation band key of the action where the caller's action needs one. The shape is stated and stays open until the freeze (ASM-1404).
3. Fix the authorise answer: the decision ALLOWED or REFUSED, the area and right asked, the matrix version and the conflict version the session resolved, and on a refusal the reason code and the message id. The answer carries no record and no personal value.
4. Fix the permission answer: the role codes with their names and default scopes, the letters of each capability area the session holds, the scope type with the team and region codes, the matrix version, the conflict version and the resolution time.
5. Fix the refusal vocabulary: 401 with MSG-P4-001 for a session with no role, 401 with MSG-P4-005 for a token without a second factor, 403 with MSG-P4-002 for a right the session does not hold, and the conflict refusal with MSG-P4-006 naming the pair; 503 with no business data when the answer cannot be given.
6. Fix the refusal and sign-in fact: the user reference, the area, the right, the result REFUSED, and the reason code NO_ROLE, NO_MFA, ROLE_CONFLICT or NO_RIGHT, recorded through the local decision-record library by the writer of RWB-P4-E1039-APP (DP-03).
7. Fix the negative statements: this contract publishes no event and consumes none; it holds no session, no token and no password; it does not answer `GET /api/recovery/access/v1/doa-limits`, which belongs to the delegation-of-authority story of this service; and it does not maintain the role-to-group mapping, whose maintenance contract is RWB-P4-AD001-CON while the mapping rows themselves are `role.entra_group` data of this service.
8. Fix the consumed surface: the rwb-case reference-data contract for the role classes, the areas and the scopes, and the ACE Common sign-in through gateway-bff, each with its owner and its call type.
9. Publish the fakes: a session fake, a role fixture, a reference-data fake, a roles-and-teams fake and an access-entry fake, so a consuming service needs no running rwb-access to build.
10. Wire the contract test into the build of every consuming service, and publish the contract document with the nine tables of section 12.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A caller asks a path this contract does not publish, for example the delegation limits | The answer is 404 and the contract names the owning story; this service grows no path by accident | None | AC5 |
| X2 | A caller sends a body outside the published shape | 400 with an RFC 9457 problem detail and no business data; nothing is resolved | None | AC1 |
| X3 | A consumer calls with no verified session, or with a session the edge no longer holds | 401 with MSG-P4-001; no role is answered | MSG-P4-001 | AC4 |
| X4 | A consumer calls an operation with no declared area or right | 400 on the contract test of the consuming service, and 422 at run time; the caller fixes the declaration instead of the contract | None | AC6 |
| X5 | A consuming service implements its own check instead of calling the contract | Its drift and contract test fails the build | None | AC6 |
| X6 | A document publishes a session table, a token or a password field | The review refuses the change: the target has none, and the session is gateway-bff's (ADR-010) | None | AC5 |
| X7 | A consumer expects an event from this service | There is none on this contract; the policy events belong to the stories that load a policy version | None | AC5 |
| X8 | The answer cannot be given because the reference contract is unreachable or malformed | 503, fail closed, no business data, nothing cached | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; the contract refers to the rwb-case reference contract, the edge session store and the tables of this service by name only |
| Negotiable | The payload detail and the field names are agreed at the contract freeze; the two operations, the vocabulary, the version labels and the negative statements are fixed by the target architecture |
| Valuable | Unblocks the edge and every consuming service from Day 1 against one frozen answer and its fakes |
| Estimable | One OpenAPI document, two operations, one refusal vocabulary, five fakes and one contract test |
| Small | Fits two weeks with its contract tests |
| Testable | Every criterion below is a contract test that the build of a consuming service runs against the published fakes |

### 7. Acceptance criteria

```gherkin
Feature: Access contract of rwb-access — authorise and me/permissions

  Background:
    Given the rwb-access contract document is published with major version 1 on base /api/recovery/access/v1
    Given permission matrix version "PM-2026.11" is in force from 30 November 2026 and separation of duty version "SOD-2026.11" is in force
    Given every role, group and test user of the fixture is synthetic

  Scenario: AC1 The two operations and their call rules are published (new, D-RCV-60)
    Given the contract document of this story
    When a consuming service compiles its client against it
    Then POST /api/recovery/access/v1/authorise accepts the role codes of a resolved session, the scope type, the capability area and the right, and answers a decision of ALLOWED or REFUSED
    Then GET /api/recovery/access/v1/me/permissions accepts no parameter and answers the caller's own resolved set
    Then each operation is one hop with a 2 s timeout, a circuit breaker per downstream and an error as an RFC 9457 problem detail
    Then the two paths are stated at the base of the service because Architecture v5 slide 14 names the operations and the Ownership Map has no path row: Not specified in the source documents (GAP-0776; ASM-1403)

  Scenario: AC2 The authorise answer carries the decision and the versions the session resolved (new, D-RCV-60)
    Given a session resolved under matrix version "PM-2026.11" with role "RW-CASEOWN"
    When the guard asks for area "PLATFORM_ADMINISTRATION" and right "R"
    Then the answer is REFUSED, because the Platform administration letter of "RW-CASEOWN" is "-"
    Then the answer carries matrix version "PM-2026.11", conflict version "SOD-2026.11" and the reason code NO_RIGHT
    When the guard asks for the area "DOCUMENTS" and right "R" for a session holding "RW-LITOFF" and "RW-LEGAL"
    Then the answer is ALLOWED with the letters "CRUA" as the union of "CRU" and "CRUA"
    Then the answer carries no record, no case id and no personal value

  Scenario: AC3 The permission answer and the scope of the caller are published (new, D-RCV-60)
    Given a session resolved to "RW-CASEOWN" with default scope "OWN" and a team code and a region code read through the rwb-case contract
    When the caller reads GET /api/recovery/access/v1/me/permissions
    Then the answer holds the role code "RW-CASEOWN", its name and default scope, and the letters of each capability area the session holds
    Then the answer holds the scope type "OWN" with the team and region codes, matrix version "PM-2026.11", conflict version "SOD-2026.11" and the resolution time
    Then the answer holds no token, no session reference of a store this service owns and no personal value
    When the rwb-case reference contract is unreachable or answers malformed
    Then the answer is 503 with no business data and nothing is cached

  Scenario: AC4 The refusal vocabulary and the recorded fact are fixed (new, D-RCV-60)
    Given a session that resolved with role "RW-PHONECOL" and the letter "-" in Platform administration
    When the guard asks for area "PLATFORM_ADMINISTRATION" and right "R"
    Then the caller receives 403 with MSG-P4-002 and the action it names
    Then the recorded fact holds the user reference, area "PLATFORM_ADMINISTRATION", right "R", result "REFUSED" and reason code NO_RIGHT
    Then a token without a second factor, a session with no role and a conflicting pair are refused with MSG-P4-005, MSG-P4-001 and MSG-P4-006 respectively
    Then the conflict refusal names both roles of the pair and carries reason code ROLE_CONFLICT
    Then no message id is invented and every one used is the legacy id of this key

  Scenario: AC5 The negative statements of the contract are published (new, D-RCV-60)
    Given the published contract document
    When a consumer asks it for a session, a token, a password, an event or a delegation limit
    Then the document has no such operation, no such field and no such event: this service publishes none of them and consumes none
    Then GET /api/recovery/access/v1/doa-limits is named as the delegation-of-authority story's of this service and is not published here
    Then the maintenance of the role-to-group mapping is named as RWB-P4-AD001-CON, and the mapping rows themselves are role.entra_group data of this service
    Then role, permission and role_conflict are named only, as the tables of this service created by RWB-P4-E1022-DB
    Then a document that adds a session table, a token or a password field is refused at review

  Scenario: AC6 The fakes and the contract test of every consuming service (new, D-RCV-60)
    Given the five published fakes: session, role fixture, reference data, roles and teams, and access entry
    When the contract test of a consuming service runs against the published document and its fakes
    Then the fakes answer an ALLOWED decision, a REFUSED decision with NO_RIGHT, a conflict refusal, a 503 and the permission answer of AC3
    Then a consumer that omits the area or the right declaration fails its own test with the operation named
    Then a consumer that re-implements the check instead of calling the contract fails its drift test
    Then the fake set is the same for every consumer and needs no running rwb-access

  Scenario: AC7 Each business rule BR1 to BR12 of section 8 is named by a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the contract story is reviewed for rule coverage
    Then each rule BR1 to BR12 is named by a criterion of this section or by a guardrail or boundary test, and a rule with neither fails review

  Scenario: AC8 The two operations answer 401 and 404 on their error paths (new, D-RCV-60)
    Given the two operations of the published contract
    When a caller sends a request without a caller identity or to a path the contract does not publish
    Then the answer is 401 for the missing identity and 404 for the unpublished path.
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is copied: legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9 are carried by RWB-P4-E1022-APP, and legacy AC1 and legacy AC3 by RWB-ITG-E1022-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A capability area and a right are checked before the caller's handler runs, and a refused action changes nothing | permission.letters (DF-REF-043); REQ-ACA-010; CTL-09 |
| BR2 | Deny by default: an answer that cannot be given is a refusal, never an allow, and no failed answer is cached | Architecture v5 slides 10 and 29; REQ-ACA-002 |
| BR3 | The answer carries the matrix version and the conflict version the session resolved, and the session keeps them until it ends | Legacy BR7; Admin and access model, section 4.2 |
| BR4 | A role pair listed in the conflict table may not be held in one session, and the refusal names the pair | Legacy BR5; separation of duty version SOD-2026.11 |
| BR5 | A service identity is resolved and checked on the same contract as a person | Legacy BR6; REQ-ACA-010; NFR-051 |
| BR6 | Group names, roles, letters, scopes and conflicts are data rows with a version; none is a constant of the contract or of the code | Legacy BR8; Principle 1; DT02 |
| BR7 | The contract holds no session, no token and no password, and the identity boundary is ACE Common's through gateway-bff | ADR-010; Architecture v5 slide 35 |
| BR8 | The contract publishes no event and consumes none; the policy events belong to the stories that load a policy version | Architecture v5 slide 14; DP-14 |
| BR9 | The contract answers the authorise and permission questions only: the delegation limits and the masking policies are the operations of their own stories | Architecture v5 slide 14; ownership map |
| BR10 | The role-to-group mapping is maintained under RWB-P4-AD001-CON, and the mapping rows are role.entra_group data of this service | Ownership Map (role, P4); Template and Rules §R7 |
| BR11 | The service owns its tables and its schema; the contract names the tables of this service and reads no table of another service | DP-01, DP-02; Architecture v5 slide 29 |
| BR12 | A published version is never edited in place; a breaking change is a new major version with a migration note and a new pin | Architecture v5 slides 11 and 38 |

### 9. State transitions

The contract fixes the states of a decision and the lifecycle of the contract version; it holds no case status and no stored object of its own.

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Contract version | 1 | A backward-compatible change to a payload, an attribute or a fake | Version 1, minor change | The pinned consumers build unchanged |
| Contract version | 1 | A breaking change to an operation, an answer or the vocabulary | Version 2 with a migration note | A consumer moves only by changing the pin and passing its contract test |
| Access decision | UNCHECKED | The letters of the area hold the right the caller declares | ALLOWED | The caller's handler runs |
| Access decision | UNCHECKED | The letters do not hold the right, or the area holds no row | REFUSED | 403 with MSG-P4-002 and reason code NO_RIGHT |
| Access decision | UNCHECKED | The answer cannot be given | FAIL_CLOSED | 503 with no business data and nothing cached |
| Session resolution | UNRESOLVED | The claims carry a second factor, a mapped active role and no conflicting pair | RESOLVED | The role set, the scope and the two versions are answered |
| Session resolution | UNRESOLVED | No second factor, no mapped role, or a conflicting pair | REFUSED | MSG-P4-005, MSG-P4-001 or MSG-P4-006, and the reason code on the fact |

A REFUSED or FAIL_CLOSED decision is never cached by the contract's own means: the contract stores nothing, and a cache is the consumer's with its own time to live (DP-08, RWB-PLT-E1037-CON).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract owner of rwb-access (any team, per U3) | Owns the document, the two operations, the vocabulary, the fakes and the versioning of the contract |
| The service template owner | Pins exactly one version of the contract in the template and moves the pin with the build as the gate |
| The consuming squads of the 19 services and gateway-bff | Compile and test against the published document and its fakes, and raise a change request instead of a local override |
| RW-SECADM Security administrator | Owns the role-to-group mapping rows and their maintenance contract RWB-P4-AD001-CON; receives the conflict incident |
| RW-REFADM Reference data administrator | Loads an approved role or matrix version; the contract reads it and never writes it |
| RW-CASEOWN, RW-PHONECOL, RW-LITOFF, RW-LEGAL, RW-SECADM and SY-RULES | Hold the roles whose answers the criteria exercise |
| No approval level of the delegation of authority applies | The contract publishes no delegation limit and takes no credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034, DF-REF-035, DF-REF-036 | role (P4 rwb-access) | id, role_code, role_name | Named only: carried in the two answers |
| DF-REF-037, DF-REF-038 | role (P4 rwb-access) | role_class, default_scope | Named only: class and the source of the scope type |
| DF-REF-039 | role (P4 rwb-access) | entra_group | Named only: the mapping row the resolution reads; the maintenance contract is RWB-P4-AD001-CON |
| DF-REF-040 to DF-REF-044 | permission (P4 rwb-access) | id, role_id, capability_area, letters, matrix_version | Named only: the letters and the version the answers carry |
| DF-REF-205 to DF-REF-211 | role_conflict (P4 rwb-access) | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Named only: the conflict version and the pairs the refusal names |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | delegation_limit (P4 rwb-access) | the limit fields | **Not published here**: `GET /api/recovery/access/v1/doa-limits` belongs to the delegation-of-authority story of this service |
| Session claim (no field ID) | The verified claims of gateway-bff | the `groups` claim, the `amr` claim, the user reference | Named only: the input of the resolution, never stored by this service |
| No data of its own | The contract | None | The contract stores nothing, caches nothing and owns no schema |

Field IDs are those in the Logical Data Model and Data Dictionary. Every row is named and none is written by the contract: the tables are created by RWB-P4-E1022-DB and written by the role and matrix stories of this service (DP-01). A contract that carried a value, a table or a token would break the identity boundary of ADR-010, so the shapes are published without one.

### 12. Contract

#### 12.1 REST operations provided

| Method and path | Request | Answer | Errors |
|---|---|---|---|
| POST /api/recovery/access/v1/authorise | The role codes of the resolved session, the scope type with the team and region codes, the capability area, the right, and the delegation band key of the action where the action needs one | The decision ALLOWED or REFUSED, the area and right asked, the matrix version, the conflict version and, on a refusal, the reason code and the message id | 400 malformed; 401 MSG-P4-001 or MSG-P4-005; 403 MSG-P4-002; 422 an assertion no area or right; 503 fail closed |
| GET /api/recovery/access/v1/me/permissions | None | The role codes with their names and default scopes, the letters of each capability area, the scope type with the team and region codes, the matrix version, the conflict version and the resolution time | 401 MSG-P4-001 or MSG-P4-005; 503 fail closed |

Both paths are published under the base of §R4 and DP-13. Architecture v5 slide 14 names the operations `authorise` and `me/permissions` and the Ownership Map has no path row for them: Not specified in the source documents (GAP-0776; ASM-1403). The request and answer fields are stated by this contract and stay open until the freeze: Not specified in the source documents (GAP-0776; ASM-1404).

The contract does **not** publish `GET /api/recovery/access/v1/doa-limits`: that read belongs to the delegation-of-authority story of this service, RWB-P4-E1038-APP. It does not publish `GET /api/recovery/access/v1/masking-policies` either, which is the masking story's. The two legacy reads `GET /api/recovery/access/v1/admin/roles` and `GET /api/recovery/access/v1/me/session` are the role-to-permission contract's, RWB-P4-E1037-CON, and are not republished here.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | P3 rwb-case | The values of `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` in force, through the reference-data contract behind RWB-PLT-E1043-CON (DP-07) |
| The roles-and-teams read of the rwb-case contract | P3 rwb-case | The team and region codes a TEAM or REGION scope names, through RWB-P3-E1019-CON |
| ACE Common sign-in, group-to-role (INT-21) | ACE Common, through gateway-bff | The verified claims the resolution reads; the service never calls Entra ID directly and holds no token |

Each call is one hop with a 2 s timeout and a breaker per downstream (DP-11, ADR-020). This contract story has no build dependency on them: it names them and the app story calls them.

#### 12.3 Events published

None. This service publishes no event on this contract. `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1` are published by the stories that load a policy version, not by the sign-on contract.

#### 12.4 Events consumed

None. The resolution holds no cache, so there is nothing for this contract to invalidate; the cache with its time to live and its refresh is the consumer's, published by RWB-PLT-E1037-CON.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity; the resolution and the check are synchronous request handling.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of this service and belongs to the access-review story.

#### 12.7 Tables owned

None created here. The contract reads the tables of this service — `role`, `permission` and `role_conflict`, all P4 and all in `rwb_access` — which RWB-P4-E1022-DB creates and the role and matrix stories write. `delegation_limit` and `masking_rule` are P4's as well and are the other stories' operations. `lov_value` is P3's and is read through the reference-data contract (DP-07). No table of another service is named in a statement of this story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Session fake | The verified claims of gateway-bff behind RWB-PLT-N001-CON | A token with `amr` holding `mfa`, one with `pwd` only, a workload token for SY-RULES, a set with an unmapped group, and an expired session (AC1, AC3, AC4) |
| Role fixture | The `role`, `permission` and `role_conflict` rows of `PM-2026.11` and `SOD-2026.11` | RW-CASEOWN with scope OWN and `-` in Platform administration; RW-PHONECOL with `-`; RW-LITOFF CRU and RW-LEGAL CRUA in Documents; RW-SECADM with any business role (AC2, AC4) |
| Reference-data fake | `GET /api/recovery/case/v1/admin/lists/{listCode}` | The values in force, an unreachable answer and a malformed answer (AC3) |
| Roles-and-teams fake | The rwb-case roles-and-teams read | The team and region codes of a TEAM or REGION scope (AC3) |
| Access-entry fake | The writer of RWB-P4-E1039-APP | A recorder of the user reference, the area, the right, the result and the reason code, and a switch that fails the write (AC4) |

The five fakes are published with the contract so that a consuming service needs no running rwb-access to build or test (AC6).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 | 2 | The authorise and permission answers are provided; the rwb-case reference read and the team read are named as the app story's |
| Kafka | 0 | 0 | No event on this contract |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** The OpenAPI 3.1 document and the generated client and server shapes for the two operations, published as one versioned contract artefact of the service, with the fakes and their fixtures as resources of the same artefact. The implementation is RWB-P4-E1022-APP's, in `th.co.scb.ace.workbench.recovery.access`; the published shapes sit in `th.co.scb.ace.workbench.recovery.access.api`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract names `role`, `permission` and `role_conflict` as `rwb_access` tables and owns none of them | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The refusal and sign-in facts are recorded by the writer of RWB-P4-E1039-APP, which this contract names and does not build | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The classes, the areas and the scopes are named by the contract and read through it at run time | referred to; the consuming story carries the dependency |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. This story is the contract of the authorise answer that the guard library calls | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The three in-process interfaces of the legacy story become two REST operations and one named fact writer | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. Both operations sit at `/api/recovery/access/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The contract adds no migration and states that the schema is RWB-P4-E1022-DB's | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route. The contract fixes the 401, 403 and 503 answers the route renders and the session line it shows | referred to; the consuming story carries the dependency |

The H and C dependencies named in the last column belong to RWB-P4-E1022-APP and to the consuming stories; this contract story has no build dependency of its own, which is why its H, C, I and X rows read None.

**Hardware and software change.** The `recovery.access.signin` package's published Java interfaces — `AccessCheck.check`, `SessionResolver.resolve` and `AccessEventPublisher.publish` — are replaced by two REST operations with a published document, a mock and a contract test in every consumer's build. The roles, the letters and the conflict pairs leave the monolith's single schema and stay in `rwb_access`; the reference values and the team codes are asked of rwb-case one hop away. The contract adds no schema, no topic, no queue, no Schedule and no bucket, so no new hardware is implied: the document is published to the artefact registry and the operations run in the service's existing pods on the existing AKS cluster.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OpenAPI 3.1 document | Document | The two operations, their shapes, their errors and their examples (AC1, AC2, AC3, AC4) |
| Error vocabulary | Document | 401 with MSG-P4-001 or MSG-P4-005, 403 with MSG-P4-002, the conflict refusal with MSG-P4-006, 503 with no business data, and the refusal fact with its reason code (AC4) |
| Negative statements | Document | No event, no session, no token, no password, no delegation limit, no mapping maintenance, named with the story that owns each (AC5) |
| Fakes and fixtures | Test asset | The five fakes of section 12.8 and the synthetic rows they answer from (AC6) |
| Contract test | Test asset | The test a consuming service runs against the document and the fakes, including the drift test on the version pin (AC6) |

**Build steps**

1. Write the two operations in the OpenAPI document with their examples, and run the contract test of a sample consumer against the generated client (AC1).
2. Write the authorise answer and the permission answer with the version labels and the scope, and prove them against the role fixture (AC2, AC3).
3. Write the error vocabulary with the four message ids and the reason codes, and prove each refusal path with a consumer test (AC4).
4. Write the negative statements and check that the document has no session, token, password, event or delegation-limit surface (AC5).
5. Publish the five fakes and wire the contract and drift tests into the build of a consuming service; test the ALLOWED, REFUSED, conflict, 503 and permission answers (AC6).
6. Publish the document with the nine tables of section 12, record its version and its compatibility rule, and hand the pin to the service template.

**Done when.** The six criteria pass as contract tests, the five fakes are published with the document, the nine tables of section 12 name their owner from the Ownership Map, and RWB-P4-E1022-APP and the guard library of RWB-PLT-E1037-APP build and pass their tests against the published document.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | A session with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-005 | Token without a second factor (new) | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Conflicting role pair at sign-in (new) | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-GEN-006 | ACE sign-in service unavailable | {system} is not available. Your request is queued and will be retried. |

The message ids and the wording are copied unchanged from RWB-E1-022, and the Thai text of each follows DL10; the contract adds no message of its own. The 503 fail-closed answer carries no message id and no business data: one RFC 9457 problem detail with the trace identifier and the operation.

### 15. Screens and states

No screen of its own. The contract fixes what a screen receives: 401 with MSG-P4-001 or MSG-P4-005 on the access request page, 403 with MSG-P4-002 where a menu entry is absent or an action refused, the conflict refusal with MSG-P4-006 naming the pair, and the role and scope line the edge renders at the top of every page. Those are gateway-bff composite screens under RWB-PLT-N001-CON; SCR-43 Roles and access and SCR-47 Personal data arrive in Epic 8 and are out of scope. SCR-43 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-4948). SCR-47 states: empty, error and no access are Not specified in the source documents (CG-ALL-4949); its loading state is as Screen Specifications v1 section SCR-47 gives it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P4-E1022-CON-01 | AC1 | Contract | A sample consumer compiles against the document; the two paths; the 2 s timeout, the breaker and the RFC 9457 error of each |
| TC-P4-E1022-CON-02 | AC2, AC3 | Contract | The role fixture of `PM-2026.11`; RW-CASEOWN REFUSED on Platform administration R with reason code NO_RIGHT; RW-LITOFF and RW-LEGAL ALLOWED on Documents with letters CRUA; the permission answer with scope OWN and the team and region codes; the 503 on an unreachable reference contract |
| TC-P4-E1022-CON-03 | AC4 | Contract | One refusal of each kind: 403 MSG-P4-002, 401 MSG-P4-005, 401 MSG-P4-001 and the conflict refusal with MSG-P4-006 naming RW-SECADM and RW-CASEOWN; the fact with its subject, area, right, result and reason code |
| TC-P4-E1022-CON-04 | AC5 | Contract | A search of the document for a session, a token, a password, an event and a delegation-limit operation; the named owners of the doa-limits read and of the mapping maintenance |
| TC-P4-E1022-CON-05 | AC6 | Contract | The five fakes; the ALLOWED, REFUSED, conflict, 503 and permission answers; a consumer without an area declaration and a consumer that pins another version, each failing its own test |
| TC-P4-E1022-CON-06 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-P4-E1022-CON-AC10) |
| TC-P4-E1022-CON-07 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P4-E1022-CON-AC11) |

No test in this story is an integration copy: the contract is exercised against its own fakes, never against a running service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in the contract: roles, groups, letters, scopes, versions and message ids are data rows or message-catalogue entries, never constants of the document or of the code.
- No personal data in a payload, a fixture or a log; the two answers carry identifiers, codes and version labels only.
- No session, token, password or local account in the contract: the session is gateway-bff's in its Redis store, and the identity boundary is ADR-010's.
- No event on this contract: the policy events belong to their own stories, and the refusal fact goes through the decision-record library.
- Deny by default and fail closed, with no business data in the 503 answer.
- The contract names the tables of this service only; a consumer that reads a P4 table directly fails its boundary test.
- A published version is never edited in place; a breaking change is a new major version with a migration note and a new pin.
- No place name, no person name and no credential anywhere: the fixture is synthetic and the users are references.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-001 | Single sign-on through Entra ID with MFA | Epic 1, 3.4 | FEAT-ACA-01, FEAT-ACA-02 | All recovery processes | BR7, BR8 | TC-P4-E1022-CON-03, TC-P4-E1022-CON-04 |
| REQ-ACA-002 | Roles as data, changed without a code release | Epic 1, 3.4 | FEAT-ACA-03 | All recovery processes | BR3, BR6, BR12 | TC-P4-E1022-CON-02, TC-P4-E1022-CON-05 |
| REQ-ACA-010 | Service identities under the same role checks | Epic 1, 3.4 | FEAT-ACA-02 | All recovery processes | BR1, BR2, BR4, BR5 | TC-P4-E1022-CON-03, TC-P4-E1022-CON-05 |
| Legacy TC-E1-022-01, TC-E1-022-02, TC-E1-022-03, TC-E1-022-04, TC-E1-022-05, TC-E1-022-06, TC-E1-022-07, TC-E1-022-08, TC-E1-022-09, TC-E1-022-10 | The ten legacy test cases of RWB-E1-022, at component and end-to-end level | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-01, FEAT-ACA-02, FEAT-ACA-03 | All recovery processes | BR1 to BR12 | Executed by RWB-P4-E1022-APP and RWB-ITG-E1022-ITG |

The ten legacy test cases of RWB-E1-022 are executed by RWB-P4-E1022-APP — which owns legacy AC2, AC4, AC5, AC6, AC7, AC8 and AC9 — and by RWB-ITG-E1022-ITG, which owns legacy AC1 and legacy AC3 and the end-to-end form of all ten. This contract story copies no legacy acceptance criterion and lists no legacy test case of its own.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1022-APP | App development | Implements the two operations, the resolver and the refusal path against this contract, and owns the seven legacy criteria of this key |
| RWB-P4-E1022-DB | ACE DB | Creates `role`, `permission`, `role_conflict`, the library objects and the login in `rwb_access` |
| RWB-P4-E1037-CON | Contract | The role-to-permission contract that publishes the legacy `GET /admin/roles` and `GET /me/session`, and the masking policies |
| RWB-P4-E1038-APP | App development | The delegation-of-authority story whose `GET /api/recovery/access/v1/doa-limits` is not published here |
| RWB-P4-AD001-CON | Contract | The maintenance contract of the role-to-group mapping rows this contract reads |
| RWB-PLT-E1037-CON | Contract | The guard library whose contract test consumes the authorise answer |
| RWB-PLT-E1027-CON | Contract | The decision-record library the refusal facts are recorded through |
| RWB-PLT-N001-CON | Contract | The edge that renders the answers and holds the session this contract never stores |
| RWB-ITG-E1022-ITG | Integration | Owns legacy AC1 and legacy AC3 and the end-to-end form of the same business outcome |

### 19. Out of scope

- The implementation of the two operations, the resolver and the refusal path: RWB-P4-E1022-APP.
- The schema, the tables, the library objects and the login: RWB-P4-E1022-DB.
- The delegation of authority table and `GET /api/recovery/access/v1/doa-limits`: RWB-P4-E1038-APP.
- The masking policies and `GET /api/recovery/access/v1/masking-policies`: RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- The role catalogue and the session line on `GET /api/recovery/access/v1/admin/roles` and `GET /api/recovery/access/v1/me/session`: RWB-P4-E1037-CON.
- The maintenance of the role-to-group mapping rows: RWB-P4-AD001-APP and RWB-P4-AD001-CON.
- The access log, the break-glass path and the decision-record writer: RWB-P4-E1039-APP.
- The guard library and its cache: RWB-PLT-E1037-APP and RWB-PLT-E1037-CON.
- Partner identities through the external gateway: RWB-P4-E2019-APP.
- The end-to-end SSO sign-in across the edge: RWB-ITG-E1022-ITG.
