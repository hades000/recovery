# RWB-PLT-E1042-CON Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E1-042 for the platform library RWB-PLT-LIB; the catalog, the value versions and the five operations stay with RWB-P3-E1042-APP and RWB-P3-E1042-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 48 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1042-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-042 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-PLT-E1042-CON-16); not specified in the source documents |
| Contract version | v1 (fixed to the /v1 path) |
| Depends on (build) | None |
| Contract dependencies | None |
| Wave-0 shared baseline (not H) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON (DP-03, DP-06, DP-07, DP-09, DP-10, DP-15, DP-19; DP-added, carried in the dependency map, not H; Ready to start stays Day 1) |
| Contract reads built against fakes until published (not C) | RWB-P3-E1042-CON, RWB-P3-E1043-CON (DP-06, DP-07); fakes per section 12.8 |
| Integration dependencies | None |
| External dependencies | None |
| Epic design sign-off | Accepted by the programme directive of 26 November 2026; no separate signed epic design record is in the source documents |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-019) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **platform contract owner**, I want **the published contract of the parameters client — the client interface and its types, the catalog and value data contract with the field ids of the logical data model, the four operations it consumes with their owner and their errors, the cache and refresh rule, the start-up rule, the two build-check contracts and the fakes** — instead of **the monolith's `recovery.casewf.config` package that read two tables in the same database**, so that **all 19 services read parameters through one client and one frozen data contract while the catalog and the endpoints stay with P3** (Template and Rules §R6, DP-06).

### 2. Business rationale

The legacy story published a Java interface and one read endpoint inside one application, and it left the loader, the cache and the two build checks to the same module (legacy sections 12 and 13). Nineteen services cannot share that shape: each has its own schema, its own login and its own image, none may read another service's tables, and a client written nineteen times drifts in its types, in its cache and in its build rule (Arch v5 slides 11, 20 and 29; DP-01, DP-06, DP-11). The contract is therefore the deliverable that lets the other eighteen services, and the owner's own service, build and test on Day 1 against a frozen interface and a fake.

**The division is fixed.** The catalog rows, the value versions, the owning service rwb-case, that service's own decision of which version is in force and its server-side cache, and the five REST operations of the legacy story stay with **RWB-P3-E1042-APP** and **RWB-P3-E1042-CON**, under the REST base `/api/recovery/case/v1`. That story owns the legacy acceptance criteria and executes the legacy test cases `TC-E1-042-01` to `TC-E1-042-12`. This contract publishes the **parameters client library** that all 19 services bind, and the two build-check contracts that make "no business value in code" true; it copies no legacy acceptance criterion.

What the contract freezes is the behaviour, not the storage (ASM-2451): a typed read by key, business date and product group that reports the environment and the version; a cache whose time to live is itself a catalog entry; a refresh on the owner's approval event, consumed through the inbox; a start-up rule that refuses to let a service serve traffic without a required value; a generated key set; and two build checks with one finding shape. What it deliberately does not freeze is anything the owner owns: the catalog columns beyond the contract members, the load validation, the approval separation of duty and the authorisation of the five paths.

The contract also fixes the one boundary that keeps the split honest. A service may read a parameter only through the interface and a generated key; it may not call the owner's read path itself, may not read the catalog table, may not cache a secret and may not hold a default in its own code. Held to that, a value changes as data without a release and the same rule holds in all 19 services.

It supports REQ-DRI-010 and REQ-ACA-005: a value changes without a code release, every parameter has an owner and a default, and a secret is listed and never served.

### 3. Preconditions

- The catalog and the values belong to rwb-case under the Ownership Map and the §R3 default ruling: `parameter_catalog` and `parameter_value` are P3 tables, and the five operations are P3 operations.
- The client has no service short: it is library code inside each service, so it declares no REST base, no topic, no consumer group and no Temporal task queue of its own.
- The field identifiers DF-REF-132 to DF-REF-146 (`parameter_catalog`) and DF-REF-147 to DF-REF-158 (`parameter_value`) are taken from the Logical Data Model and Data Dictionary, character for character.
- The legacy members of the published types are taken from legacy section 12: `ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment)`, `get(ParameterKey<T>, LocalDate)`, `get(ParameterKey<T>, String productGroup, LocalDate)` and `CatalogEntry entry(String key)`.
- The message ids MSG-P3-032, MSG-GEN-002, MSG-P1-002, MSG-GEN-001, MSG-P7-002, MSG-P3-015 and MSG-P4-002 are used unchanged; the contract invents none.
- The event name `rwb.case.ParameterVersionApproved.v1` on the owner's topic `rwb.case.events.v1` follows §R4 naming on the legacy event "ParameterVersionApproved"; the mapping is recorded in ASM-2453 because no source states the name.
- The artifact coordinates of the library — the group, the artefact name, the version scheme and the publication channel — are Not specified in the source documents (GAP-1407; ASM-2454).
- The published status codes of the consumed operations beyond the legacy story's — 200, 201, 401, 403, 409, 422 and 503 — are carried from legacy section 12 and from the message rows; a status that the legacy story does not state for an operation is Not specified in the source documents (GAP-1407; ASM-2454).
- No build dependency: the contract is Day 1 by rule (Template and Rules §R5.7), and no approval is needed to publish a draft baseline, which is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the client interface and its four types: `Parameters`, `ParameterKey<T>`, `ParameterValue<T>` and `CatalogEntry`.
2. The author writes the generated key contract: `ParameterKeys`, generated from `config/parameter-catalog.csv`, one constant per key with its type, for example `ParameterKeys.CASE_ENTRY_DPD : ParameterKey<Integer>`; a key that the file does not list has no constant.
3. The author writes the catalog and value data contract from the legacy members and the field identifiers of section 11, so the interface, the generated keys, the fakes and the owner's schemas agree.
4. The author writes the four consumed operations exactly as the Ownership Map and the legacy story name them, with the owner, the request, the responses, the status codes and the message ids, and states that the library provides no path of its own.
5. The author writes the cache and refresh rule: one line per key, product group, business date and environment; the time to live read from the catalog entry `refdata.cache.ttl-seconds`; the eviction on `rwb.case.ParameterVersionApproved.v1` through the inbox; approved versions only.
6. The author writes the start-up rule: every required key of a service must have a value for its deployment's environment, and a missing one fails the start with MSG-P3-032 and keeps the pod out of traffic.
7. The author writes the two build-check contracts: what `RwbMagicNumberCheck` and `CatalogCompletenessCheck` accept, what they refuse, and the finding shape — file, line and key.
8. The author publishes the fake and the fixture set, and wires one drift test into the build of every consuming service.
9. The contract is validated: the four paths compared with the Ownership Map, every message id compared with the legacy message table, every type member compared with the field identifiers, and every value taken from the legacy story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A service declares a read path of its own or calls the owner's path directly | The drift test fails the build: the only read is through `Parameters` | None | AC1, AC6 |
| X2 | A published type gains, loses or renames a member | The contract test of every consuming service fails until the version is raised with a migration note | None | AC1, AC6 |
| X3 | A consumed operation is published with a path that the Ownership Map does not own | The lint step fails and the document is not published | None | AC2 |
| X4 | An operation is published without its status codes or its message id | The lint step fails the build | None | AC2 |
| X5 | A caller reads a key with a string literal | The interface refuses it, so the read does not compile; the completeness check has nothing to compare | None (build output) | AC3 |
| X6 | A service caches a value without a version or reads a value that is not approved | The contract test fails and the review rejects the change | None | AC5 |
| X7 | A consuming service's build drifts from section 12 | The drift test fails naming the member or the operation that moved | None | AC6 |
| X8 | A consumer needs a member that no source defines | The member is not invented; the contract carries the placeholder and the gap stays open | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents, a jar and a fake; builds nothing and depends on nothing |
| Negotiable | The member order, the example values and the finding layout are open until the version is frozen |
| Valuable | Every service and the owner's own service start on Day 1 against one interface and one fake |
| Estimable | One interface, four types, one generated key set, four consumed operations, two build-check contracts and the fake |
| Small | One sprint for the contract and the fake, with the lint and contract tests |
| Testable | Each criterion is a schema, lint or drift assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Parameters client contract

  Background:
    Given the platform library has no service short
    Given the catalog and the values are served by rwb-case under /api/recovery/case/v1
    Given the contract version is v1

  Scenario: AC1 The client interface, the types and the generated keys are published (new, D-RCV-60)
    Given the client library declaration of Parameters
    When a service compiles against it
    Then it publishes get(ParameterKey<T> key, LocalDate businessDate), get(ParameterKey<T> key, String productGroup, LocalDate businessDate) and CatalogEntry entry(String key)
    Then ParameterValue<T> carries key, value, versionNo, validFrom and environment
    Then CatalogEntry carries key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, versionNo and validFrom
    Then ParameterKeys is generated from config/parameter-catalog.csv and Parameters.CASE_ENTRY_DPD is a ParameterKey<Integer>
    Then no method takes a string key, so a literal cannot be read

  Scenario: AC2 The four consumed operations are fixed with their owner and their errors (new, D-RCV-60)
    Given the four operations exactly as the Ownership Map names them: GET /api/recovery/case/v1/admin/parameters, POST /api/recovery/case/v1/admin/reference-loads, POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve and POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback
    When the contract is linted
    Then the owner of all four is P3 rwb-case and the library provides no path of its own
    Then the read answers 200 with the value in force, 401 without a session, 403 without Rules and parameters R (MSG-P4-002) and 503
    Then the load answers 201, 403 without Reference data C (MSG-P4-002) and 422 with MSG-GEN-002, MSG-P1-002 or MSG-GEN-001
    Then the approval answers 409 when the approver is the author (MSG-P7-002)
    Then the rollback answers 409 when no earlier version exists (MSG-P3-015)

  Scenario: AC3 The catalog and value data contract carries the legacy field ids and members (new, D-RCV-60)
    Given the catalog and value data contract of the client
    When it is compared with the Logical Data Model and the legacy members
    Then parameter_catalog carries DF-REF-132 to DF-REF-146 and parameter_value carries DF-REF-147 to DF-REF-158
    Then the catalog line carries key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, versionNo and validFrom
    Then the value line carries key, value, versionNo, validFrom, environment and productGroup
    Then the value is absent from a line whose secret is true
    Then no member is published that no source defines, and the cache line carries no field identifier because none exists

  Scenario: AC4 The error and start-up vocabulary is fixed (new, D-RCV-60)
    Given the published message table of the contract
    When it is compared with the legacy message table
    Then MSG-P3-032 is the start-up refusal naming the key and the environment
    Then MSG-GEN-002, MSG-P1-002 and MSG-GEN-001 are the load refusals with their legacy texts
    Then no other message id is invented and every id keeps its legacy text and its status code
    Then the two build checks raise no user-facing message, only a finding with the file, the line and the key

  Scenario: AC5 The refresh is consumed on the owner's topic and no unapproved value is served (new, D-RCV-60)
    Given the approval event rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1
    When the contract is validated
    Then the event carries paramKeys, versionNo and validFrom and is consumed through the inbox with a consumer group per service
    Then a repeated CloudEvents id has no second effect
    Then the contract states that a value whose load status is VALIDATED and not APPROVED is never served, cached or returned
    Then an approved version takes effect on its valid-from date with no restart

  Scenario: AC6 The fakes and the drift test of every consuming service are published (new, D-RCV-60)
    Given the contract fake and the fixture set
    When a consuming service builds against the published jar
    Then the fake answers the read, the three load operations, the approval event and the three interface cases
    Then the drift test fails the build when a published member, operation or message id differs from section 12
    Then the fixture set covers the literal 90, the unknown key "allocation.retry.limit", the allowed literals 0, 1 and -1 and test code
    Then the examples carry no personal data, no secret value and no credential

  Scenario: AC7 The business rules BR1 to BR8 of section 8 hold in the contract (new, D-RCV-60)
    Given the business rules BR1 to BR8 of section 8
    When the contract is validated
    Then a service reads a parameter only through the interface and a generated key, and never reads the catalog table or calls the owner's path itself
    Then every key a service reads is in the catalog file with an owner and a default
    Then the value line, version, environment and read time are fixed, and the owner's approved version is the only truth
    Then a version that is not APPROVED is never served
    Then a secret is listed and never served
    Then a service does not start without every required value for its environment
    Then the contract publishes platform resources only
    Then a published version is never edited in place
```

Every criterion above is new and tests only the contract artefact. No legacy acceptance criterion is copied: the eleven criteria of RWB-E1-042 stay with RWB-P3-E1042-APP, and the legacy test cases `TC-E1-042-01` to `TC-E1-042-12` execute there.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A service reads a parameter only through the interface and a generated key; it never reads the catalog table and never calls the owner's path itself | Legacy guardrails; DP-01; DP-06 |
| BR2 | Every key a service reads is in the catalog file with an owner and a default; the contract publishes the generated key set and the completeness rule | Legacy BR2; REQ-DRI-010 |
| BR3 | The client is not authoritative: the contract fixes the value line, the version, the environment and the read time, and states that the owner's approved version is the only truth | Legacy section 4 steps 8 and 9 |
| BR4 | A value version that is not APPROVED is never served; the approval event follows §R4 naming on the owner's topic | Legacy BR5; ASM-2453 |
| BR5 | A secret is listed and never served: the value member is absent from a secret line, and no example carries a secret value | Legacy BR6; DL26; REQ-ACA-005 |
| BR6 | A service does not start without every required value for its environment, and MSG-P3-032 names the key and the environment | Legacy BR7 |
| BR7 | The contract publishes platform resources only: the catalog, the values and the five operations stay with P3 rwb-case | Template and Rules §R3 default ruling; Ownership Map |
| BR8 | A published version is never edited in place; a breaking change is a new major version with a migration note | Legacy section 12 versioning; ASM-2454 |

### 9. State transitions

None in this story: a contract has no runtime state. The states it describes are the value version states of the owner — VALIDATED, APPROVED, ROLLED_BACK — and the client cache line states the APP story implements: absent, loaded, stale and evicted. Each is described with the call or the event that produces it, and the behaviour itself is specified in RWB-PLT-E1042-APP section 9.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the interface, the data contract, the operation list, the message table and the fake |
| The platform library owner | Approves a breaking change and the version freeze |
| The consuming teams of all 19 services | Read the contract, pin a version, raise a change request |
| rwb-case (P3) | Owns the catalog, the values, the five operations and their authorisation model |
| rwb-access (P4) | Owns the Reference data and Rules and parameters rights that the operations check |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

Role names appear as role codes only, resolved by rwb-access at run time (DP-08). No name of a person, no email address and no credential appears in the contract or in an example.

### 11. Data

| Item | Value |
|---|---|
| Field identifiers published | DF-REF-132 to DF-REF-146 (`parameter_catalog`); DF-REF-147 to DF-REF-158 (`parameter_value`); BR Field ID: DF-REF-132 to DF-REF-158 |
| Members published from the legacy contract | key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, versionNo, validFrom; the value, its version and its valid-from date; the environment and the product group; BR Field ID: DF-REF-132 to DF-REF-158 |
| Members with no field identifier | The client cache line and the event payload members (`paramKeys`, `versionNo`, `validFrom`); the working read of this run; BR Field ID: None |
| Tables owned by the contract | None. `parameter_catalog` and `parameter_value` are P3 tables, named only; BR Field ID: None |
| Personal data in examples | None. Users appear as user ids such as `U-2101`, roles as role codes, values as numbers and dates; BR Field ID: None |

The contract carries no value that no source holds. The catalog members and their order are the legacy section 12 response, the field identifiers are the Logical Data Model's, and the event members are the legacy section 12 event. A member that a consumer needs and no source defines is not invented: the contract carries the placeholder and the gap stays open (GAP-1407; ASM-2454).

### 12. Contract

#### 12.1 REST operations provided

None — the client declares no REST operation. The catalog read and the four reference-load operations are provided by P3 rwb-case under `/api/recovery/case/v1` and are consumed, never provided or republished by the library.

#### 12.2 REST operations consumed

| Operation | Owner | Request | Responses and messages | Used by |
|---|---|---|---|---|
| GET `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | Query: key prefix, kind, owner, environment | 200 array of the catalog line with the value in force, its version and its valid-from date; 401 without a session; 403 without Rules and parameters R (MSG-P4-002); 503 | `get`, `entry` and the start-up check |
| POST `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | multipart/form-data: file of key, environment and value; table = "PARAMETER"; validFrom | 201 load with id, table, validFrom, status and rows; 401; 403 without Reference data C (MSG-P4-002); 422 range (MSG-GEN-002), type or unknown key (MSG-P1-002), empty file (MSG-GEN-001); 503 | The contract test and the operator rehearsal; the client never loads |
| POST `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | None | 200 approved; 401; 403; 409 when the approver is the author (MSG-P7-002); 503 | The approval whose event refreshes the cache |
| POST `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 rwb-case | None | 200 with the previous version in force; 401; 403; 409 when no earlier version exists (MSG-P3-015); 503 | The rollback whose event returns the previous value |

These are exactly the four operations of the Ownership Map rows, at v1, and the owner of all four is P3 rwb-case. The contract states that the library declares no path, no base and no service short, and that a service calls the read only through `Parameters` (DP-11, DP-13). The status codes and message ids are the legacy story's, character for character.

#### 12.3 Events published

None — the library publishes no event. The approval event that refreshes the cache is published by P3 rwb-case through its own outbox.

#### 12.4 Events consumed

| Event | Topic | Producer | Members | Use |
|---|---|---|---|---|
| `rwb.case.ParameterVersionApproved.v1` | `rwb.case.events.v1` | P3 rwb-case | `paramKeys`, `versionNo`, `validFrom` | The client evicts the named keys before the next read, through the inbox, with one consumer group per service |

The name follows §R4 on the legacy event "ParameterVersionApproved", which the legacy story calls a new internal event without a topic; the mapping is recorded in ASM-2453. A repeated CloudEvents id has no second effect, and an older `versionNo` never replaces a newer one (DP-09).

#### 12.5 Workflows and activities

None — the client is library code inside each service; the contract declares no workflow, no activity and no task queue of its own.

#### 12.6 Schedules

None — the refresh is event-driven and otherwise lazy by the time to live, which is the catalog entry `refdata.cache.ttl-seconds`; no Schedule and no Quartz job (GAP-1407; ASM-2454).

#### 12.7 Tables owned

None — `parameter_catalog` and `parameter_value` are P3 tables in the rwb_case schema under the Ownership Map, and the contract names them only. The client creates no table, holds no copy and writes no row; the one row the listener writes is the inbox row of the outbox and inbox library in the consuming service's own schema (DP-01, DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Parameters fake (this story) | The read, the catalog entry, the start-up check and the three interface cases | Every consuming service's drift test and RWB-PLT-E1042-APP |
| Reference-load fake | The three load operations with their success and refusal examples | The contract test of this story and the operator rehearsal of the deployment story |
| Approval-event fake | `rwb.case.ParameterVersionApproved.v1` with one new id, one repeat and one rollback | The cache and refresh tests of RWB-PLT-E1042-APP |
| Build-check fixture set | The two build checks | `RwbMagicNumberCheck` and `CatalogCompletenessCheck` tests: the literal 90, `allocation.retry.limit`, 0, 1, -1 and test code |
| rwb-case reference-data fake | The product-group codes behind RWB-P3-E1043-CON | The typed read examples that carry a product group |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 4 consumed | Four operations of P3 rwb-case, at v1; the read at run time, the three load operations in the contract test and the operator rehearsal |
| Kafka | None published, 1 consumed | `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1`, through the inbox |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | `config/parameter-catalog.csv` is a build input of the generator and the completeness check |

### 13. Solution plan

**Package.** Contract artefact of the platform, the interface and types in `th.co.scb.ace.workbench.recovery.platform.params.api`, the data contract and the fake as resources; the implementation is RWB-PLT-E1042-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract reads the catalog through the owner and holds no copy | referred to; the consuming story carries the dependency |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the contract supplies the version and the owning service writes the record | referred to; the consuming story carries the dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. This story is the client's contract and names the rwb-case contract it consumes | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the product-group codes are reference rows of the owner | referred to; the consuming story carries the dependency |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The contract fixes the inbox rule for the approval event | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The contract replaces the in-process `ParameterService` call with one documented read and a fake | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; every consumed path is a `/api/recovery/case/v1` path and the library declares no base | referred to; the consuming story carries the dependency |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The event name and the topic are fixed on the owner's naming | referred to; the consuming story carries the dependency |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the inbox table the contract refers to is created by that sequence | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route; the contract adds no route and no screen | referred to; the consuming story carries the dependency |

**Hardware and software change.** The contract replaces a two-table read in one database with four documented operations of rwb-case and one interface compiled into nineteen deployments; it fixes a per-service cache with a time to live that is itself a catalog entry, an approval event on the owner's topic and a start-up rule that keeps a pod out of traffic. No new hardware is implied; the contract is a jar and a document, and the owner's service and its two tables stay where they are.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `Parameters` | Published interface | Three methods: two typed reads and one catalog entry |
| `ParameterKey<T>`, `ParameterValue<T>`, `CatalogEntry` | Published types | The key with its type; the value with its version, date and environment; the catalog line with its members |
| `ParameterKeys` | Generated source, contract | One constant per catalog key, generated from the catalog file |
| Catalog and value data contract | Document | The members of section 11 with their field identifiers and the secret rule |
| Operation list and message table | Document | The four operations, their owner, their status codes and the seven legacy message ids |
| Cache, refresh and start-up rule | Document | The line, the time to live from the catalog, the eviction on the event and the refusal at start-up |
| Build-check contract | Document | The two checks, their allowed and refused inputs and the finding shape |
| Contract fake and fixtures | Test asset | The four operations, the event, the three interface cases and the build-check fixtures |

**Build steps**

1. Write the interface and the two record types with their members and types; run a compile test of a sample service (AC1).
2. Write the generated key contract and the generator's input rule; prove that a key outside the catalog file has no constant (AC1, AC3).
3. Write the catalog and value data contract from section 11 and cross-check every member with the field identifiers (AC3).
4. Write the operation list from section 12.2 and lint it against the Ownership Map rows; check every status code and message id (AC2).
5. Write the message table from section 14 and compare it with the legacy table, character for character (AC4).
6. Write the cache, refresh and start-up rules as testable sentences, with the time to live as the catalog entry (AC5).
7. Write the two build-check contracts with the finding shape and the allowed literals (AC6).
8. Generate the fake and the fixtures, and wire the drift test into a sample service build (AC6).
9. Publish v1 to the contract registry and hand it to RWB-PLT-E1042-APP and to every consuming service.

**Done when.** The five test cases of section 16 pass, the four operations match the Ownership Map rows, every message id matches the legacy table, and the drift test fails on a changed member and passes on the published jar.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value at start-up, published as the start-up refusal | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | A loaded value is outside its range, published on the load operation | {field} must be between {min} and {max}. |
| MSG-P1-002 | A loaded value has the wrong type or an unknown key, published on the load operation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | The load file is empty, published on the load operation | Enter {field}. |
| MSG-P7-002 | The approver is the author, published on the approval operation | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | A rollback has no earlier version, published on the rollback operation | There is no earlier version of {table} to return to. |
| MSG-P4-002 | A role without the right, published on all four operations | You cannot {action} here. Your role does not include it. |

The ids and the texts are the legacy story's, character for character, and the status code beside each one in section 12.2 is the legacy status. The two build checks raise no message id: their finding is the build output, with the file, the line and the key. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The contract is read by the teams that build the client and by the services that consume it; the catalog screen SCR-39 Rules and parameters belongs to Epic 8 and reads the owner's operation, and the client adds no route and no state to any screen (DP-19). The states the contract describes are the value version states of the owner and the client cache line states of the APP story. SCR-39 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-1343).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1042-CON-01 | AC1 | Contract | The interface and the four types compiled in a sample service; `CASE_ENTRY_DPD` as a `ParameterKey<Integer>`; a string key refused at compile time |
| TC-PLT-E1042-CON-02 | AC2 | Contract | The four operations compared with the Ownership Map rows; every status code and message id compared with the legacy table |
| TC-PLT-E1042-CON-03 | AC3 | Contract | Every member compared with DF-REF-132 to DF-REF-158 and the legacy section 12 response; the secret line with no value |
| TC-PLT-E1042-CON-04 | AC4, AC5 | Contract | The seven message ids compared with the legacy table; the event on `rwb.case.events.v1`; the approved-only rule; the repeat id |
| TC-PLT-E1042-CON-05 | AC6 | Component | The fake run against the four operations, the event and the three interface cases; the drift test red on a changed member and green on the jar |
| TC-PLT-E1042-CON-06 | BR1 | Contract | A service reads a parameter only through the interface and a generated key; a direct catalog read or owner-path call is refused |
| TC-PLT-E1042-CON-07 | BR2 | Contract | Every key in the catalog file has an owner and a default; the generated key set and the completeness rule are compared with the catalog file |
| TC-PLT-E1042-CON-08 | BR3 | Contract | The value line, version, environment and read time are fixed in the contract; the owner's approved version is stated as the only truth |
| TC-PLT-E1042-CON-09 | BR4 | Contract | A version that is not APPROVED is never served; the approval event follows the section R4 naming on rwb.case.events.v1 |
| TC-PLT-E1042-CON-10 | BR5 | Contract | A secret line lists the key with no value member; no example carries a secret value |
| TC-PLT-E1042-CON-11 | BR6 | Component | A service does not start without every required value for its environment; MSG-P3-032 names the key and the environment |
| TC-PLT-E1042-CON-12 | BR7 | Contract | The contract publishes platform resources only; the catalog, the values and the five operations are absent from it |
| TC-PLT-E1042-CON-13 | BR8 | Contract | A published version is not edited in place; a breaking change is a new major version with a migration note |
| TC-PLT-E1042-CON-14 | AC7 | Contract | The rules BR1 to BR8 checked as in TC-PLT-E1042-CON-06 to TC-PLT-E1042-CON-13; the proposed test itself is Not specified in the source documents (NEWAC-RWB-PLT-E1042-CON-AC7) |

### 17. Guardrails

- No business value in the contract: the members are typed, the values are data, and the time to live is the catalog entry `refdata.cache.ttl-seconds`.
- No member that no source defines; a needed member carries the placeholder and the gap stays open.
- No personal data and no secret value in an example, a fixture or a log; only user ids, role codes, numbers and dates.
- No cross-schema reference: the two tables are named as P3 tables and the client holds no copy.
- The four consumed operations stay exactly as the Ownership Map owns them, with owner P3 rwb-case and no path of the library's own.
- A published version is never edited in place; a breaking change raises a new major version with a migration note.
- Every consuming service runs the drift test; a service that skips it has not met the contract.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | Epic 1, 3.3; Program, 5.7 | FEAT-CWC-22 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1042-CON-01 to TC-PLT-E1042-CON-05 |
| REQ-ACA-005 | Secrets are listed in the catalog and held only in the secret store | Epic 1, 3.4 | FEAT-ACA-05 | 14 Set strategy, policy and decision rules | DL26 | TC-PLT-E1042-CON-03, TC-PLT-E1042-CON-04 |

| Legacy test cases | Disposition |
|---|---|
| `TC-E1-042-01, TC-E1-042-02, TC-E1-042-03, TC-E1-042-04, TC-E1-042-05, TC-E1-042-06, TC-E1-042-07, TC-E1-042-08, TC-E1-042-09, TC-E1-042-10, TC-E1-042-11, TC-E1-042-12` | executed by RWB-P3-E1042-APP |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1042-APP | App development | H consumer: builds the client against this contract and its fake |
| RWB-PLT-E1042-OPS | DevOps | The deployment of the client: the pinned version, the chart values, the catalog file, the probe and the alerts |
| RWB-P3-E1042-APP, RWB-P3-E1042-CON | App development, Contract | C: the owner of the catalog, the values, the five operations and the legacy acceptance criteria and test cases |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract behind the product-group codes |
| RWB-PLT-E1043-CON, RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | The platform contracts the app story builds on (DP-07, DP-03, DP-09, DP-14, DP-15, DP-19); this contract documents the relation and adds no build dependency of its own |

REQ-ACA-005 has no row in legacy section 18; its short text is legacy BR6 and its BRD section is the one the legacy Epic 1 story of the same requirement carries.

Open decisions that apply to this story: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355). Both decisions remain open; the confirmation status of each assumption is Not specified in the source documents (DOR-RWB-PLT-E1042-CON-18).

### 19. Out of scope

- The catalog, the value versions, the service that serves them and its own cache: RWB-P3-E1042-APP.
- The five REST operations, their validation, their status codes in code and the approval separation of duty: RWB-P3-E1042-APP and RWB-P3-E1042-CON.
- The authorisation model of the load operations — the Reference data C, Reference data A, Reference data U and Rules and parameters R rights — which belong to P4 rwb-access and are checked by P3 rwb-case.
- The administration screen SCR-39 Rules and parameters: Epic 8.
- Product-specific parameters and service levels: the product-parameter story of RWB-E1-045, RWB-P3-E1045-APP.
- The reference tables and the reference-data service: RWB-PLT-E1043-APP, RWB-PLT-E1043-CON and RWB-P3-E1043-APP.
- The implementation, the metrics and the deployment of the client: RWB-PLT-E1042-APP and RWB-PLT-E1042-OPS.
- The secret store itself, its rotation and its access path: the platform, and the secrets baseline of the platform.
