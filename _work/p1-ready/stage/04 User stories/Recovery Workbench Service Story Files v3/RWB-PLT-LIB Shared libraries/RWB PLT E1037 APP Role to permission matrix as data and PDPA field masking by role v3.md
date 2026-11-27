# RWB-PLT-E1037-APP Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: platform library slice split from RWB-E1-037 for RWB-PLT-LIB — the access guard and masker library that every service binds. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 40 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1037-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-PLT-LIB-D |
| Size | To be sized by the squad at refinement |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1037-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P4-E1037-CON, RWB-P4-E1039-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| Contract version | v1 (the /v1 path the story builds against) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **service developer**, I want **one guard library that checks the capability area and the right before the handler runs and one masker library that fills every field annotated as personal data from the masked or last-four value the data owner supplies, with a cache of the permission and masking policy that refreshes on the access owner's policy events and fails closed**, so that **every service refuses an action the matrix does not allow and no service ever holds or prints a clear personal value**.

This is the platform-library slice of legacy key RWB-E1-037 under epic RWB-PLT-LIB. The library is not one of the 19 services: it has no service short name, no schema, no topic, no task queue and no REST base of its own. It is a versioned artefact that a service binds, and it holds no data of its own — the permission matrix, the masking rules, the roles, the scope and the delegation limits stay with P4 rwb-access, the ACE fields it masks stay with P1 rwb-source-data, and the access log store stays with P4 rwb-access through RWB-P4-E1039.

The story covers:

- The `AccessGuard`: the capability area and the right of the action are checked before the handler runs, against the access owner's answer, and a refusal returns 403 `MSG-P4-002` with the handler never invoked.
- The `ScopeGuard`: the library produces a scope descriptor (OWN, TEAM, REGION, ALL plus the user, team and region codes) and the owning service applies it in its own query. The library never runs another service's query and never returns a record.
- The `MaskApplier`: a `@PersonalData("DF-…")` annotation on a response field, filled from the masked column or the last-four value the data owner supplies; with no rule in force the field is masked; the clearest identity value the library may hold is `id_no_last4`.
- The policy cache: the permission and masking policy is cached per service with the time to live read through the parameters client, and refreshed on `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` through the inbox.
- The fail-closed rule: an unreachable, timed-out or malformed access owner means refusal with 503 and no business data anywhere in the response or the log.
- The audit record: every masked or clear read writes one record with the case id, the field id and the flag `clear` or `masked`, never the value, through the access-log contract of P4 rwb-access.

### 2. Business rationale

The legacy story holds the role-to-permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned tables that every screen and API applies, with `ScopeFilter`, `FieldMasker` and `AccessCheck` published from one package, `recovery.access.matrix`, inside one process and one database.

**The division is fixed and is the same in both stories of this legacy key.** The permission matrix as data, the masking rules, the scope rule, the access log and the matrix load and approve operations stay with **RWB-P4-E1037-APP**, which owns the legacy acceptance criteria; the end-to-end proof across the wave 1 services is **RWB-ITG-E1037-ITG**; this story and its contract story RWB-PLT-E1037-CON deliver the **shared guard library and masker library** that every service binds, so that the right check and the masking are one mechanism and not nineteen copies. Neither story copies a legacy acceptance criterion: every criterion in section 7 is tagged (new, D-RCV-60) and tests only the library deliverable in the title, and the fifteen legacy test cases are executed by RWB-P4-E1037-APP and RWB-ITG-E1037-ITG (section 18).

The split follows the architecture and not a preference. Each service authorises the object itself, using cached permission data from rwb-access, with a 2 s timeout and a circuit breaker per downstream (Architecture v5 slide 10); the access owner publishes `POST /authorise` for role, scope and DoA, `GET /me/permissions`, `GET /doa-limits` and `/api/recovery/access/v1/masking-policies`, and writes `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1` (slide 14); personal data stays in the owning service and the masking rules of the access owner are enforced in each service (slide 35). A shared library is the only shape that makes those three sentences true at nineteen services: without it, nineteen services each write their own guard against the same contract, nineteen cache implementations expire at nineteen different moments, and the masking rule is re-implemented wherever a DTO is mapped. Until RWB-P4-E1037-CON publishes the operation IDs, bodies, status codes, error model and cache lifetime of these operations, their shapes are open; each service denies by default when rwb-access does not answer.

The negative side is fixed as tightly as the positive one. Deny by default and fail closed (slides 35 and 29), no personal data in logs, payloads or events, no token store (ADR-010; slide 35), and no cross-schema read: the library holds no table, so it cannot read a P4 or a P1 table even by accident. The values the criteria use are the legacy values unchanged — matrix version `PM-2026.11`, masking version `MASK-SIT-01`, cases `RW-2026-000123` and `RW-2026-000456`, team `MTG-NE`, the role codes RW-CASEOWN, RW-LEGAL, RW-PHONECOL, RW-SECADM, RW-REFADM, RW-COE, RW-AUDIT, RW-COMPLY, the field ids DF-ACE-073 `id_no_masked`, DF-ACE-074 `id_no_last4`, DF-ACE-078 `contact_value`, DF-ACE-079 `contact_value_masked`, DF-ACE-059 `date_of_birth`, the area `QUEUE_AND_ALLOCATION`, the letters C, R, U, D and A, the scopes OWN, TEAM, REGION and ALL, and the messages MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-GEN-004.

It supports REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and keeps controls CTL-09, CTL-10 and CTL-11 in place. Where the sources do not fix the library artefact coordinates, the cache time to live, the authorise payload, or the split of the masking read between the policy of P4 and the record of P1, the story builds to the assumption in force and records the open point as Not specified in the source documents (GAP-1404; ASM-2445), (GAP-1404; ASM-2446) and (GAP-1404; ASM-2447). The measure is unchanged from the legacy story: rule and limit changes made without a code release, target 100 percent (FSD P4 A2.4).

### 3. Preconditions

- RWB-PLT-E1037-CON is published (this story's contract deliverable): the `AccessGuard`, `ScopeGuard` and `MaskApplier` interfaces, the `@PersonalData` annotation, the scope descriptor, the error vocabulary, the fail-closed rule and the fakes.
- RWB-P4-E1037-CON and RWB-P4-E1039-CON are published: the authorise, permission and masking-policy operations of P4 rwb-access, and the access-log contract that the audit record is written through (DP-08, DP-11).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1`, which the library refers to and does not write (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library (DP-06, DP-07); RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the rwb-case contracts behind them.
- RWB-PLT-TE006-CON is published: the inbox contract through which the two access policy events are consumed and deduplicated (the library consumes no event without an inbox row in the consuming service's own schema).
- RWB-PLT-E1071-CON is published: the workflow kit, so the guard is proven to run inside a workflow activity as well as inside a REST handler (DP-10).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence. The library itself adds no migration; a service that wants a local cache table applies its own (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route, so the 403 and 404 answers of the guard reach the screen in the route's problem-detail shape (DP-19).
- Permission matrix version `PM-2026.11` is in force. In it RW-LEGAL holds `-` in Queue and allocation and RW-CASEOWN holds `R` in Queue and allocation.
- Masking version `MASK-SIT-01` is in force, in which only RW-CASEOWN may see `v_ace_contact.contact_value` in clear for DF-ACE-078; no unmasked rows go to PROD until Compliance supplies the rules (DL26).
- The access owner answers `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions` and `GET /api/recovery/access/v1/masking-policies` under its own per-service base, one hop, 2 s timeout and breaker per downstream (DP-11, DP-13, ADR-020).
- No table is read by the library: the role, permission, masking_rule, role_conflict and delegation_limit tables are P4 rwb-access's and `lov_value` is P3 rwb-case's (DP-01, DP-07). The unmasking answer for `interaction.summary` comes from the authorise answer of rwb-access; P1's `data_product_access` is its data product catalogue and is not the masking authority (GAP-0584).
- The library artefact coordinates, the cache time to live and the authorise request and answer payload are Not specified in the source documents (GAP-1404; ASM-2445), (GAP-1404; ASM-2446) and (GAP-1404; ASM-2447).
- No build dependency blocks the start: every dependency in the metadata table is a CON story, so the story is ready on Day 1 against the published contracts and their fakes.

### 4. Flow

1. A service binds the published library. The service template pins exactly one version of it, and the consuming service writes no guard, no cache and no masker of its own.
2. A request arrives at the consuming service. The `AccessGuard` reads the action's capability area and right from the service's own annotation or route declaration, and asks the policy cache for the answer of the signed-in role.
3. On a cache miss, the guard calls `POST /api/recovery/access/v1/authorise` with the role, the scope and the delegation band of the action, one hop, 2 s timeout, with the breaker of that downstream.
4. The guard stores the answer in the cache with the time to live read through the parameters client, and answers the request from the cached policy while it is fresh. The time to live and the parameter key are Not specified in the source documents (GAP-1404; ASM-2446).
5. A denied action is refused with 403 `MSG-P4-002` before the handler runs; the handler is never invoked, nothing changes, and the refusal is written to the log with the area and the right and no business data.
6. A permitted action runs. Where the action reads a set of records, `ScopeGuard` produces a scope descriptor with the type (OWN, TEAM, REGION or ALL) and the user, team and region codes, and hands it to the owning service, which applies it in its own query. The library returns no record and runs no query of another service.
7. The owning service writes its own answer. A record outside the descriptor is refused by the owner with 404 `MSG-P4-003`; the library supplies the message id and the status only.
8. The answer passes through `MaskApplier` before it leaves the service. Every field annotated `@PersonalData("DF-…")` is filled from the masked column or the last-four value that the data owner supplies, or from the clear value only where the masking policy of the access owner allows it for one of the session's roles.
9. Where no rule in force covers an annotated field, the field is masked. The masker never asks for the clear identity number, never receives it, never caches it and never logs it; `id_no_last4` is the clearest identity value the library may hold.
10. Every masked or clear read writes one audit record through the access-log contract of P4 rwb-access (RWB-P4-E1039-CON): the case id, the field id and the flag `clear` or `masked`, and never the value.
11. `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` are consumed from `rwb.access.events.v1` through the inbox of the consuming service. Each one drops the stale cache entries before the next guard call, so a policy change takes effect within the time to live and with no deployment.
12. The access owner is unreachable, times out, or answers outside its contract: the guard refuses with 503, the handler does not run, the failure is logged with the operation and the trace identifier and with no business data, and the decision is counted as a fail-closed decision.
13. The library reports its own counters on the platform observability path: guard decisions by outcome, cache hits and misses, fail-closed decisions, masker fills by flag, and audit writes refused.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an action, for example a transfer | Refused with 403 before the handler runs; nothing changes; the refusal is logged | MSG-P4-002 | AC1 |
| X2 | The access owner is unreachable or answers after the 2 s timeout | Refused with 503, fail closed; the handler does not run; no business data in the log or the error body | None | AC2 |
| X3 | The access owner answers a malformed or partial policy answer | Refused with 503, fail closed; the malformed answer is discarded and never cached | None | AC2 |
| X4 | A policy event arrives while a request is in flight | The in-flight request keeps the answer it was given; the next request reads the refreshed entry | None | AC3 |
| X5 | The same policy event is delivered twice | The inbox drops the second delivery; one refresh happens | None | AC3 |
| X6 | A record outside the scope descriptor is requested | Refused with 404; the record is not returned and the excluded count is never shown | MSG-P4-003 | AC4 |
| X7 | A consuming service builds its own query result instead of applying the descriptor | The contract and drift test fails the build; the library returns no record by design | None | AC4, AC8 |
| X8 | An annotated field has no rule in force | The field is masked | None | AC5 |
| X9 | A masking rule names the clear identity number | The rule is refused at load by the access owner; the clearest value the library can receive is `id_no_last4` | MSG-P1-002 (raised by P4) | AC6 |
| X10 | The audit write fails | The read is refused, not served, because an unaudited personal read is not allowed | None | AC7 |
| X11 | A consuming service pins another library version or overrides a class | The drift test fails the build and names the pinned and the resolved version | None | AC8 |
| X12 | A log record, a span attribute or an error body is found to carry a personal value | The redaction test fails the build; the record is purged under the owning service's retention and a defect is raised | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the library CON story and the platform contract stories; the access owner and the data owner are reached through their contract fakes, so no service has to be finished first |
| Negotiable | The artefact coordinates, the cache time to live and the payload shapes are open until the contract freeze; the interfaces, the fail-closed rule, the annotation and the audit shape are fixed by the target architecture |
| Valuable | Gives every service one guard and one masker instead of nineteen copies, and makes fail-closed and no-clear-personal-data the default rather than a review finding |
| Estimable | Three interfaces, one annotation, one cache, one audit writer and the fakes |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below is a component, contract or NFR test in section 16, against the fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Access guard and masker library for the 19 services

  Background:
    Given the guard and masker library is published with major version 1 and pinned by the service template
    Given permission matrix version "PM-2026.11" is in force
    Given RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11" and RW-CASEOWN holds "R" in Queue and allocation
    Given masking version "MASK-SIT-01" is in force, in which only RW-CASEOWN may see v_ace_contact.contact_value in clear for DF-ACE-078

  Scenario: AC1 The right is checked before the handler runs (new, D-RCV-60)
    Given a consuming service that binds the guard library and a test user "U-2105" holding only RW-CASEOWN, whose Queue and allocation letter is "R"
    When the service handles an action that needs Queue and allocation U for case "RW-2026-000123", with a probe handler that records its first line
    Then the guard calls POST /api/recovery/access/v1/authorise for area "QUEUE_AND_ALLOCATION" and right "U"
    Then the action is refused with status 403 and message MSG-P4-002 before the probe handler records its first line
    Then the case owner and queue are unchanged and one refusal is logged with the area and the right

  Scenario: AC2 An unreachable or malformed access owner fails closed (new, D-RCV-60)
    Given the access owner fake is unreachable and answers only after the 2 s timeout
    When test user "U-2105" holding RW-CASEOWN calls an action in Queue and allocation
    Then the guard refuses with status 503 and the handler does not run
    When the access owner fake returns a malformed answer that names no role and no area
    Then the guard refuses with status 503 as well and caches neither answer
    Then no case id, no personal value and no token appears in the log record, the trace or the error body

  Scenario: AC3 The policy cache refreshes on the two access policy events (new, D-RCV-60)
    Given a service holds a fresh cache entry in which RW-LEGAL holds "-" in Queue and allocation
    When rwb.access.AccessPolicyChanged.v1 for matrix version "PM-2026.12" arrives on rwb.access.events.v1 through the inbox
    Then the entry is dropped and refilled from GET /api/recovery/access/v1/me/permissions before the next guard call
    Then the next call for RW-LEGAL in Queue and allocation U is allowed with no deployment and within the time to live
    When rwb.access.DoALimitChanged.v1 arrives on rwb.access.events.v1 through the inbox
    Then the cached delegation band is dropped and the next guard call asks the access owner again
    Then a repeated delivery of the same event changes nothing, because the inbox holds the event id

  Scenario: AC4 The scope descriptor is applied by the owning service (new, D-RCV-60)
    Given test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases
    And case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When the guard asks for the scope of the action and the owning service applies the descriptor in its own query
    Then the descriptor holds type "OWN" with the user, the team and the region codes and holds no record
    Then the owning service returns 12 cases and the total is 12
    Then the read of case "RW-2026-000456" returns status 404 with message MSG-P4-003
    Then the library ran no query of another service and returned no record of its own

  Scenario: AC5 A masked field is filled from the masked value and a field with no rule is masked (new, D-RCV-60)
    Given a response field annotated @PersonalData("DF-ACE-079") and a field annotated @PersonalData("DF-ACE-059") that no rule in "MASK-SIT-01" covers
    And the data owner supplies contact_value_masked "XXXXXX5678" and id_no_masked "XXXXXXXXX1234" for case "RW-2026-000123"
    When test user "U-2104" holding only RW-PHONECOL reads the record through the service
    Then the field for DF-ACE-079 is filled with "XXXXXX5678" and no clear contact value is requested from the data owner
    Then the field for DF-ACE-059 is masked as "XXXX-XX-XX"
    Then the masker filled two annotated fields and asked for no clear personal value

  Scenario: AC6 The library never receives the clear identity number (new, D-RCV-60)
    Given the data owner exposes id_no_masked "XXXXXXXXX0123" and id_no_last4 "0123" for person_key "P-0001"
    When the masker fills a field annotated @PersonalData("DF-ACE-074") for a role whose rule allows the last four
    Then the value filled is "0123" and the field for DF-ACE-073 is filled with "XXXXXXXXX0123"
    Then no method, parameter, cache entry or fake of the library accepts a clear identity number
    Then no library record, log record or error body holds a clear identity number

  Scenario: AC7 Every masked or clear read writes one audit record (new, D-RCV-60)
    Given test user "U-2109" holds RW-CASEOWN, which may see DF-ACE-078 in clear, and test user "U-2105" holds only RW-CASEOWN
    When "U-2109" reads the borrower's phone number on case "RW-2026-000123" and "U-2105" reads the same field
    Then one audit record is written through the access-log contract of P4 rwb-access with the case id "RW-2026-000123", field id DF-ACE-078 and the flag "clear"
    Then one audit record is written with the case id "RW-2026-000123", field id DF-ACE-078 and the flag "masked"
    Then each record holds exactly the case id, the field id and the flag, and no field value
    When the audit write is forced to fail
    Then the read is refused with status Not specified in the source documents (ACR-RWB-PLT-E1037-APP-AC7) and no unaudited personal value is served

  Scenario: AC8 Every service behaves the same and no personal data leaves in a log, trace or error (new, D-RCV-60)
    Given two services of different epics that bind the same published version of the library
    When each service runs the library contract test against the same fakes
    Then both produce the same refusal status, the same message id, the same audit record shape and the same masked value
    Then a service that pins another version or overrides a library class fails its drift test with both versions named
    Then no log record, span attribute, metric label or error body of either service holds a name, a contact value or an identity number
```

These criteria are new and test only the library deliverable. No legacy acceptance criterion is copied: legacy AC1 to AC13 belong to RWB-P4-E1037-APP, and their end-to-end form belongs to RWB-ITG-E1037-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The capability area and the right are checked before the handler runs; a denied action changes nothing and is logged with the area and the right | permission.letters (DF-REF-043); REQ-ACA-007; CTL-09 |
| BR2 | Deny by default: an action with no matching permission entry, an unreachable access owner, a timeout or a malformed answer is refused, never allowed | Architecture v5 slides 10, 29 and 35; REQ-ACA-007 |
| BR3 | Scope filters records first and the permission is checked second; the library produces the descriptor and the owning service applies it in its own query, and the excluded count is never shown | role.default_scope (DF-REF-038); LOV-SCOPE; REQ-ACA-009 |
| BR4 | OWN means cases the person owns or has a task on; TEAM means cases in the person's team queues; REGION means cases in the regions of the person's teams, used only when the P4 and P3 design adds a region predicate; ALL means every case. The scope set otherwise follows the Key tab | Key sheet, roles.txt |
| BR5 | A personal data field is masked unless the masking policy in force lets one of the session's roles see it; a masked field is filled from the masked column or the last-four value the data owner supplies; with no rule it is masked | Masking rules reference table; DL26; CTL-11; REQ-ACA-005; DF-ACE-073, DF-ACE-079 |
| BR6 | Masking is applied inside the owning service before data reaches a screen, an agent or an event | NFR-039; NFR-040 |
| BR7 | The policy cache is refreshed on `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` through the inbox, and a change takes effect within the time to live with no deployment | Arch v5 slide 20 (cache refresh); RWB-E1-037 AC1; REQ-ACA-003 |
| BR8 | There is no tokenization and no token store. The clear `customer.identification_number` never leaves ACE; the library never receives it, and `id_no_last4` is the clearest identity value it may hold | ADR-010; Data Tier Map section 7; D-RCV-35 U1 |
| BR9 | Every masked or clear read of a personal data field writes one audit record with the case id, the field id and the flag, never the value; an unaudited personal read is refused. The audit record goes through the ACE Common PII logging path to the SOC (INT-34); the Recovery business topics are separate and carry no personal data | REQ-ACA-006; RWB-E1-039 BR3; NFR-040 |
| BR10 | The library owns no table and reads no service's schema: the matrix, masking, role, conflict and delegation data are P4 rwb-access's and the reference values are P3 rwb-case's | DP-01; Ownership Map; REQ-ACA-003 |
| BR11 | No personal data in a log record, a span attribute, a metric label, an error body or a cache key: identifiers, codes and flags only | Architecture v5 slides 11 and 35 |
| BR12 | A joiner, mover or leaver change reaches the service through the access owner's policy and session state, never through a library-held user list | DL38; CTL-10; REQ-ACA-011 |
| BR13 | One version of the library is pinned by the service template, and a service that resolves another version or overrides a class fails its build | Arch v5 slides 20 and 38; RWB-PLT-NF02-APP |
| BR14 | The library takes no business decision of its own: it relays the access owner's decision and the data owner's value, and it holds no delegation limit | Arch v5 slide 10; slide 35 note on attribute-based access control |

### 9. State transitions

No case status changes in this story. The library holds three small states of its own, all in memory or in the consuming service's own cache:

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Guard decision | UNCHECKED | The access owner answers allow for the role, the area and the right | ALLOWED | The handler runs; the answer is cached with the time to live |
| Guard decision | UNCHECKED | The access owner answers deny, or holds no entry for the area | REFUSED | 403 `MSG-P4-002`, the handler does not run, the refusal is logged |
| Guard decision | UNCHECKED | The access owner is unreachable, times out, or answers malformed | FAIL_CLOSED | 503, the handler does not run, the decision is counted and nothing is cached |
| Cache entry | EMPTY | A guard call fills it from the authorise or permission answer | FRESH | The answer is served from the cache until the time to live ends |
| Cache entry | FRESH | The time to live ends | STALE | The next call asks the access owner again |
| Cache entry | FRESH or STALE | `rwb.access.AccessPolicyChanged.v1` or `rwb.access.DoALimitChanged.v1` arrives through the inbox | EMPTY | The entry is dropped before the next guard call |
| Annotated field | UNFILLED | A rule in force allows the role a clear or a last-four view | CLEAR | The field is filled from the value the data owner supplies, and the audit flag is `clear` |
| Annotated field | UNFILLED | No rule allows the role a clear view, or no rule covers the field | MASKED | The masked value is filled, or the value is masked, and the audit flag is `masked` |

A `FAIL_CLOSED` decision is never cached: the next request tries the access owner again, so a recovered access owner restores service without a restart.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform library team (any team, per U3) | Builds, tests and publishes the guard and masker library, owns its versioning and its changelog |
| The service template owner | Pins exactly one library version in the template and moves the pin with the build as the gate |
| The consuming squads of the 19 services | Bind the library, annotate their response fields, supply the scope descriptor to their own query, and raise a change request against the library instead of a local override |
| The access owner (P4 rwb-access) | Owns the role, permission, masking_rule, role_conflict and delegation_limit data, the authorise, permission and masking-policy operations and the access log; the library only calls them |
| The data owner (P1 rwb-source-data) | Owns the ACE views and the masked and last-four columns the masker fills from; the library never reads a view |
| RW-CASEOWN, RW-LEGAL, RW-PHONECOL, RW-SECADM, RW-REFADM, RW-COE, RW-AUDIT, RW-COMPLY | Hold the roles whose answers the criteria exercise; each sees only what the matrix and the masking policy allow |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version outside this story (DL26) |
| The security architecture reviewer | Confirms that the fail-closed rule, the annotation and the audit shape of a library version meet the architecture standards |
| No delegation of authority decision is made in the library | A delegation band is the access owner's data and the owning service's decision, never a value in a shared library |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-035 | role (P4 rwb-access) | role_code | Read through the authorise and permission answers |
| DF-REF-037 | role (P4 rwb-access) | role_class | Read through the authorise and permission answers |
| DF-REF-038 | role (P4 rwb-access) | default_scope | Read through the authorise and permission answers; the source of the scope descriptor type |
| DF-REF-040 to DF-REF-044 | permission (P4 rwb-access) | letters, matrix_version and the other fields | Read through the authorise and permission answers |
| DF-REF-198 to DF-REF-204 | masking_rule (P4 rwb-access) | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read through the masking-policy answer |
| DF-ACE-073 | v_ace_customer (P1 rwb-source-data) | id_no_masked | Read as the masked identity value the data owner supplies |
| DF-ACE-074 | v_ace_customer (P1 rwb-source-data) | id_no_last4 | Read as the clearest identity value; only where the rule allows it |
| DF-ACE-059 | v_ace_customer (P1 rwb-source-data) | date_of_birth | Read as a masked value; masked by the masker where the data owner supplies no masked column |
| DF-ACE-078 | v_ace_contact (P1 rwb-source-data) | contact_value | Read in clear only where the rule allows it, and every such read is audited |
| DF-ACE-079 | v_ace_contact (P1 rwb-source-data) | contact_value_masked | Read as the masked contact value |
| DF-CAS-009, DF-CAS-011, DF-CAS-012 | recovery_case (P3 rwb-case) | owner_user_id, team_code, region_code | Named only: the fields the owning service applies the descriptor to, in its own query |
| DF-ACE-055, DF-ACE-057, DF-ACE-058 | v_ace_customer (P1 rwb-source-data) | cif_no, first_name, last_name | Read as masked values where an annotated field names them |
| Cache entry (no field ID) | Library cache, in the consuming service's memory | role code, area, right, scope type, policy version, expiry | Write and read, in memory only; no table and no schema |

Field IDs are those in the Logical Data Model and Data Dictionary. The library holds no table, no schema and no login of its own (DP-01, DP-02): every value above arrives in an answer of the access owner or of the data owner, and the cache entry has no field ID in the source because no source defines a library cache (GAP-1404; ASM-2446). No clear identity number is read, cached, logged or accepted by any method of the library (BR8).

### 12. Contract

#### 12.1 REST operations provided

None. The library provides no REST surface of its own: it has no service short name, no `/api/recovery/<short>/v1` base and no OpenAPI document. The authorise, permission and masking-policy operations are provided by P4 rwb-access, and the access-log operation by P4 rwb-access through RWB-P4-E1039-CON; this story consumes them and never republishes them.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/access/v1/authorise | P4 rwb-access | The guard check for the role, the scope and the delegation band of the action, cached with the time to live and called again on a miss, a stale entry or a policy event |
| GET /api/recovery/access/v1/me/permissions | P4 rwb-access | The letters and the default scope in force for the signed-in role, used to refill the cache after `rwb.access.AccessPolicyChanged.v1` |
| GET /api/recovery/access/v1/masking-policies | P4 rwb-access | The masking rules in force for the fields and roles of the session, used to decide clear, masked or last-four and refilled after `rwb.access.AccessPolicyChanged.v1` |

Every call is one hop with a 2 s timeout, a circuit breaker per downstream and a deny-by-default answer on failure (DP-11, ADR-020). The audit record is written through the access-log contract of P4 rwb-access (RWB-P4-E1039-CON), not through a path of this story.

#### 12.3 Events published

None. The library publishes no event of its own. The policy changes it reacts to are published by P4 rwb-access, and the refusal and audit facts it writes go to the access log through the P4 contract.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | P4 rwb-access | Drops the cached permissions and masking policy of the consuming service before its next guard call |
| rwb.access.DoALimitChanged.v1 | rwb.access.events.v1 | P4 rwb-access | Drops the cached delegation band before the next guard call, so the next authorise call carries the band in force |

Both are consumed through the inbox of the consuming service, under that service's own consumer group and in that service's own `processed_event` table (RWB-PLT-TE006-CON); a repeated delivery changes nothing.

#### 12.5 Workflows and activities

None of its own. The guard and the masker are synchronous code inside the caller: the guard runs in a REST handler before the handler body, and inside a workflow activity when a service calls it from one. The library starts no workflow, starts no activity and holds no task queue.

#### 12.6 Schedules

None. The library owns no Schedule. The six-monthly access review list (JOB-18) is a P4 rwb-access Schedule and is not this story.

#### 12.7 Tables owned

None. The library owns no `rwb_*` schema, no table and no login: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` are P4 rwb-access's tables, `lov_value` is P3 rwb-case's, and the ACE view fields are P1 rwb-source-data's. They are named here only, so that no reader mistakes a shared cache for a stored copy (DP-01, DP-02).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Authorise fake | `POST /api/recovery/access/v1/authorise` | Allow, deny, unreachable, timeout and malformed answers for the same role, area and right (AC1, AC2) |
| Permission fake | `GET /api/recovery/access/v1/me/permissions` | The letters of `PM-2026.11` and, after the policy event, of `PM-2026.12` (AC3) |
| Masking-policy fake | `GET /api/recovery/access/v1/masking-policies` | One rule that lets RW-CASEOWN see DF-ACE-078 in clear, and no rule for DF-ACE-059 (AC5, AC6) |
| Scope fake | The scope part of the authorise answer | Type OWN with the user, team and region codes, and type ALL for the comparison (AC4) |
| Audit fake | The access-log contract of P4 rwb-access | A recorder that captures the case id, the field id and the flag, and a switch that fails the write (AC7) |
| Policy-event fake | `rwb.access.events.v1` with the inbox | `AccessPolicyChanged` and `DoaLimitChanged`, each delivered twice (AC3) |
| Data-owner value fake | The masked and last-four values P1 rwb-source-data supplies | `id_no_masked` "XXXXXXXXX1234", `id_no_last4` "0123" and `contact_value_masked` "XXXXXX5678" for case RW-2026-000123 (AC5, AC6) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | The authorise, permission and masking-policy operations of P4; the audit record goes through the access-log contract of P4 and adds no path of its own |
| Kafka | 0 | 2 | `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`, through the inbox of the consuming service |
| Temporal | 0 | 0 | No workflow, activity or Schedule; the guard runs inside the caller's handler or activity |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** A versioned shared-library artefact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.access` for the implementation, with the published interfaces in `th.co.scb.ace.workbench.recovery.platform.api`. The artefact coordinates, the repository and the publication channel are Not specified in the source documents (GAP-1404; ASM-2445).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The library holds no table, so the matrix and the masking rows are read only through the P4 operations | none |
| DP-02 | `recovery_svc` login | One login per service. The library has no login of its own and borrows none: every value arrives over a contract | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. A policy approval and its consequences are recorded by P4, not by the guard | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The masker fills from the masked or last-four value the data owner supplies and reads no view itself | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The cache time to live and the breaker settings are read through it | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The scope codes OWN, TEAM, REGION and ALL and the letter set are reference values, never library constants | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. This story is that guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. The guard is proven inside an activity context as well as inside a REST handler | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. Each of the three consumed operations is one hop with its own breaker | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The library adds no base of its own; every consumed path uses the base of its owner | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The library adds no migration; a service that wants a local cache table migrates it itself | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The access log and the refusal facts stay in the P4 access log, and no library path writes a lake copy | none |
| DP-19 | Screen, ace-web | gateway-bff composite route. The 403 and 404 answers reach the screen through the route, and SCR-43 and SCR-47 are not built here | H RWB-PLT-N001-CON |

**Hardware and software change.** The `recovery.access.matrix` package of the monolith is replaced by a versioned library that every service binds. The permission and masking rows leave the monolith's single schema and stay in the P4 schema, read through the access owner's operations; the ACE values stay behind the P1 contract and reach the masker already masked or cut to the last four. The guard caches its answers per service with the time to live from the parameters client and refreshes them from the two access policy events through the inbox, instead of reading a shared table on every request. No new hardware is implied: the library runs inside each service's existing pods on the existing AKS cluster, the cache is per-process memory, and no database, topic, queue or bucket is added. The two libraries RWB-PLT-E1027-CON and RWB-PLT-TE006-CON are used unchanged for the decision record and the inbox.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AccessGuard` | Published interface | Decides the area and the right before the handler runs, from the cache or from the authorise call, and refuses with 403 `MSG-P4-002` or 503 on failure (BR1, BR2) |
| `ScopeGuard` | Published interface | Produces the scope descriptor with its type and the user, team and region codes; returns no record and runs no query (BR3, BR4) |
| `MaskApplier` | Published interface | Fills the annotated fields from the masked, last-four or clear value the policy allows, masks a field with no rule, and never accepts a clear identity number (BR5, BR8) |
| `@PersonalData` | Annotation | Names the DF field id of a response field so the masker and the audit writer can act without a per-DTO list (BR5, BR9) |
| ScopeDescriptor | Value type | The type OWN, TEAM, REGION or ALL with the user, team and region codes; the owning service applies it (BR3) |
| PolicyCache | Service | Per-process cache of permissions, masking policy and delegation band, with the time to live from the parameters client and the drop on the two policy events (BR7) |
| PolicyEventInboxListener | Service | Consumes `AccessPolicyChanged` and `DoaLimitChanged` through the inbox and drops the matching cache entries (BR7) |
| AccessAuditWriter | Service | Writes one audit record per masked or clear read through the access-log contract of P4, with the field id and the flag and never the value (BR9) |
| FailClosedPolicy | Component | The timeout, the breaker and the deny-by-default mapping of every failure to 503 (BR2) |
| Library fake and fixtures | Test asset | The fakes of section 12.8, used by the contract test of every consuming service (BR13) |

**Configuration.** The cache time to live and the parameter key that holds it, the 2 s timeout and the breaker thresholds are configuration read through the parameters client (DP-06). The time to live and its key are Not specified in the source documents (GAP-1404; ASM-2446). Letters, scopes and masking positions are never library constants: they arrive in the access owner's answers and the reference data of P3 (DP-07).

**Build steps**

1. Publish the three interfaces, the annotation, the scope descriptor and the exception types from RWB-PLT-E1037-CON; prove that a sample service compiles against the jar and that no method of the library accepts a clear identity number (AC6, AC8).
2. Build the policy cache with the time to live from the parameters client and the refusal to cache a failed or malformed answer; test a fresh entry, a stale entry and a fail-closed answer (AC2, AC3).
3. Build the `PolicyEventInboxListener` over the inbox contract of RWB-PLT-TE006-CON; test both events, a repeated delivery and the drop of the exposed entry (AC3).
4. Build `AccessGuard` with the pre-handler check, the 403 `MSG-P4-002` and the 503 fail-closed path; test the allow, the deny, the unreachable, the timeout and the malformed answer with the probe handler (AC1, AC2).
5. Build `ScopeGuard` and the descriptor; give the owning service a repository test that applies OWN, TEAM, REGION and ALL in its own query and returns 404 `MSG-P4-003` for a record outside it (AC4).
6. Build `MaskApplier` over the annotation, the masking-policy answer and the values the data owner supplies; test the masked fill, the last-four fill, the clear fill and the no-rule field (AC5, AC6).
7. Build `AccessAuditWriter` over the access-log contract of P4; test one `clear` record, one `masked` record and the refusal of the read when the write fails (AC7).
8. Wire the redaction and drift checks: a log, a span or an error body that carries a personal value fails the build, and a service that pins another version fails the drift test (AC8).
9. Run the contract test of a second service of another epic against the same fakes and prove the identical status, message id, audit shape and masked value (AC8).

**Feature flag.** One flag per service, read as a parameter: off, the guard answers from the last known policy and refuses every action whose policy is unknown, so a switch-off never opens an unchecked path.

**Done when.** The tests in section 16 pass, the contract tests of section 12.8 pass against the fakes, two services of different epics produce the same refusal, audit and masking behaviour against the same version of the library, the masked read is proven through the P1 data product contract, and no log record, trace, metric label or error body carries a personal value.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The access owner reports that the session has ended after a leaver's group was removed; the guard relays it unchanged and does not retry | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission, refused before the handler runs | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the scope descriptor, refused by the owning service | This case is not in your scope. |
| MSG-GEN-004 | A consumed access operation answers 409; the library relays it unchanged and the caller re-reads its permissions | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Not specified in the source documents (DOR-RWB-PLT-E1037-APP-9) | Not specified in the source documents (DOR-RWB-PLT-E1037-APP-9) |

The message ids and the wording are copied unchanged from RWB-E1-037; the library adds no message of its own, and the Thai text of each follows DL10. The 503 fail-closed answer carries no message id and no business data: it is one RFC 9457 problem detail with the trace identifier and the operation, per Architecture v5 slide 11.

### 15. Screens and states

No screen of this story. The library has no route and no state of its own. A person sees only the effect: a menu entry absent where the role has no right (RWB-E1-022), a masked field on the case record view (RWB-E1-023), a 403 with `MSG-P4-002` and a 404 with `MSG-P4-003` rendered by gateway-bff. SCR-43 Roles and access and SCR-47 Personal data arrive in Epic 8 and are out of scope (DP-19). SCR-43 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-1313). SCR-47 states: loading is as given in Screen Specifications v1 section SCR-47; empty, error and no access are Not specified in the source documents (CG-ALL-1314).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1037-APP-01 | AC1, BR1 | Contract | A sample service and a probe handler: RW-CASEOWN with letter "R" for Queue and allocation U denied, and the same area with the right allowed; the handler's first line is never recorded on the denial |
| TC-PLT-E1037-APP-02 | AC2, BR2, BR11 | NFR | The authorise fake unreachable, timing out at 2 s and malformed; 503 on each; the log, the trace and the error body searched for a case id, a personal value and a token |
| TC-PLT-E1037-APP-03 | AC3, BR7 | Component | A fresh cache entry, `AccessPolicyChanged` for `PM-2026.12`, `DoaLimitChanged`, each delivered twice through the inbox; the entry dropped and refilled within the time to live |
| TC-PLT-E1037-APP-04 | AC4, BR3, BR4 | Component | 12 owned cases, case RW-2026-000456 in team MTG-NE, and a descriptor of each type OWN, TEAM, REGION and ALL applied in an owner-side repository test; 404 `MSG-P4-003` outside the descriptor |
| TC-PLT-E1037-APP-05 | AC5, BR5, BR6 | Component | Annotated DF-ACE-079, DF-ACE-073 and DF-ACE-059; values "XXXXXX5678", "XXXXXXXXX1234" and no masked column for the date of birth; RW-PHONECOL and RW-CASEOWN compared |
| TC-PLT-E1037-APP-06 | AC6, BR8 | NFR | `id_no_masked` "XXXXXXXXX0123" and `id_no_last4` "0123"; the reflect-and-scan check that no method, parameter, cache entry or fake accepts a clear identity number; the log, the cache dump and the error body searched for it |
| TC-PLT-E1037-APP-07 | AC7, AC8, BR9, BR13 | Contract | One clear read of DF-ACE-078 and one masked read, the audit fake capturing case id, field id and flag; the failing audit write; two services of different epics run the same contract test and the drift test refuses another pinned version |

No test in this story is an integration copy: the library is exercised against the fakes of section 12.8, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in code: letters, scopes, masking positions, approver roles, the time to live and the breaker settings are data or parameters read through their contracts.
- No personal data in a log record, a span attribute, a metric label, an error body, a cache key or a fixture: field ids and the masked flag only, never values.
- ACE data only through the owner's contract or a `v_ace_*` view read by the data owner; the library reads no database at all.
- No tokenization and no token store: the library never receives the clear identity number, and `id_no_last4` is the clearest identity value it may hold (ADR-010).
- A field with no masking rule is masked, and a clear read happens only where the rule allows it and is audited.
- Deny by default and fail closed on every failure of the access owner, with no business data in the 503 answer.
- The library owns no table, publishes no event, starts no workflow and takes no delegation decision of its own.
- The library is pinned at one version by the service template, and a local override fails the build.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-003 | Permission matrix as data, the only source of rights | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR7, BR10, BR13 | TC-PLT-E1037-APP-01, TC-PLT-E1037-APP-03 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR5, BR6, BR8 | TC-PLT-E1037-APP-05, TC-PLT-E1037-APP-06 |
| REQ-ACA-007 | Access outside the matrix refused and recorded | Epic 1, 3.4 | FEAT-ACA-04 | All recovery processes | BR1, BR2 | TC-PLT-E1037-APP-01, TC-PLT-E1037-APP-02 |
| REQ-ACA-009 | A user sees only the cases their role and scope allow | Epic 1, 3.4 | FEAT-ACA-14 | All recovery processes | BR3, BR4 | TC-PLT-E1037-APP-04 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench | Epic 2, 3.4 | FEAT-ACA-13 | All recovery processes | BR7, BR12 | TC-PLT-E1037-APP-03 |
| REQ-ACA-006 | Every read of a personal data field written to the access log | Epic 1, 3.4 | FEAT-ACA-05 | All recovery processes | BR9, BR11 | TC-PLT-E1037-APP-07 |
| Legacy TC-E1-037-01, TC-E1-037-02, TC-E1-037-03, TC-E1-037-04, TC-E1-037-05, TC-E1-037-06, TC-E1-037-07, TC-E1-037-08, TC-E1-037-09, TC-E1-037-10, TC-E1-037-11, TC-E1-037-12, TC-E1-037-13, TC-E1-037-14, TC-E1-037-15 | The fifteen legacy test cases of RWB-E1-037, at component and end-to-end level | Epic 1, 3.4; Epic 2, 3.4; Program, 5.4 | FEAT-ACA-04, FEAT-ACA-05, FEAT-ACA-13, FEAT-ACA-14 | All recovery processes | BR1 to BR14 | executed by RWB-P4-E1037-APP and RWB-ITG-E1037-ITG |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1037-CON | Contract | H: publishes the interfaces, the annotation, the scope descriptor, the error vocabulary, the fail-closed rule and the fakes this story implements |
| RWB-P4-E1037-APP | App development | C: owns the permission matrix as data, the masking rules, the scope rule, the access log and the load and approve operations, and owns legacy AC1 to AC13 |
| RWB-P4-E1039 | App development | C: the access-log contract the one audit record per read is written through |
| RWB-ITG-E1037-ITG | Integration | The end-to-end proof of the same business outcome across P4, P1 and this library; it owns no legacy criterion either |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data clients for the time to live, the breaker settings and the scope and letter values |
| RWB-PLT-E1027-CON, RWB-PLT-TE006-CON | Contract | H: the decision-record library and the inbox through which the two policy events are consumed |
| RWB-PLT-N001-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON | Contract | H: the gateway route, the workflow kit that proves the guard inside an activity, and the per-service migration sequence the library adds nothing to |
| RWB-P1-E1069-APP | App development | The data owner of the ACE views and the masked and last-four columns the masker fills from |

### 19. Out of scope

- The permission matrix as data, the masking rules, the scope rule and the matrix load and approve operations: RWB-P4-E1037-APP, which owns legacy AC1 to AC13.
- The access log store and its retention: RWB-P4-E1039.
- The authorise decision data — role, permission, masking_rule, role_conflict and delegation_limit: P4 rwb-access.
- The ACE views and the masked read itself: RWB-P1-E1069-APP.
- The administration screens SCR-43 Roles and access and SCR-47 Personal data: Epic 8 (FEAT-ADM-01, FEAT-ADM-14).
- The masking values for each role and field: Compliance, DL26.
- The end-to-end proof across the wave 1 services: RWB-ITG-E1037-ITG.
- The token store, which does not exist: ADR-010.
- The six-monthly access review list (JOB-18) and the leaver reallocation of RWB-E1-030.
