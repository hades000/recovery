# RWB-PLT-E1042-APP Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: client-library slice split from RWB-E1-042 for the platform library RWB-PLT-LIB; the catalog, the value versions and the five operations stay with RWB-P3-E1042-APP and RWB-P3-E1042-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1042-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-PLT-LIB-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-019) |
| Status | Draft (realignment v1) |

### 1. Story

As a **squad member**, I want **the parameters client implemented in the platform library — the typed read by key, business date, product group and environment with the version in the answer, the cache whose time to live is itself a catalog entry, the refresh on the owner's approval event, the start-up check that stops a service whose required parameter has no value, the generated key constants and the two build checks that fail a literal business value and an unknown key**, so that **every service reads its values at run time from the catalog and no team writes the same loader or the same lint rule again** (Template and Rules §R6, DP-06).

### 2. Business rationale

In the monolith one package, `recovery.casewf.config`, held the published `ParameterService` interface and read two tables, `parameter_catalog` and `parameter_value`, in the same `recovery` schema as every caller (legacy section 13). Under Arch v5 there are 19 services, 19 schemas and 19 logins, no service reads another service's tables, and the parameters belong to rwb-case (Arch v5 slides 14, 20 and 29; Template and Rules §R3 default ruling). A loader that reads two tables is therefore no longer possible for 18 of the 19 services, and a loader written 19 times is the same defect the legacy story was written to remove.

**The division is fixed.** The catalog rows, the value versions, the owning service rwb-case, that service's own decision of which version is in force and its server-side cache, and the five REST operations of the legacy story — `GET /api/recovery/case/v1/admin/parameters`, `POST /api/recovery/case/v1/admin/reference-loads`, `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify` and `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` — stay with **RWB-P3-E1042-APP** and **RWB-P3-E1042-CON**. That story owns the legacy acceptance criteria, and the legacy test cases `TC-E1-042-01` to `TC-E1-042-12` execute there. This story delivers the **parameters client library** that all 19 services bind, plus the **two build checks** that make "no business value in code" true; it copies no legacy acceptance criterion and claims none of the legacy test cases.

What the client keeps from the legacy story is its behaviour, unchanged (ASM-2451): a typed read that answers the value with its version number, resolves the business date and the product group, reports the environment, refreshes on the owner's approval, falls back to its time to live, and refuses to let a service start when a required value has no value for that environment. What it adds is the shape the split forces: the values arrive over the rwb-case contract instead of a second table read, the environment comes from the deployment, the cache is per service and never authoritative, and the time to live is itself a catalog entry rather than a property in a file.

The two build checks are the part of the legacy story that cannot live with the service owner, because they fail a service's build, not a request. `RwbMagicNumberCheck` fails on a numeric or string business literal in the recovery packages and names the catalog key whose default equals the literal; `CatalogCompletenessCheck` compares the keys a service reads with `config/parameter-catalog.csv` and fails on a key with no entry, no owner or no default (legacy section 13; ASM-2452). Held once in the library and applied by the service template, they are written once and enforced everywhere; copied per service they drift, and a check that drifts is worse than none.

It meets REQ-DRI-010 and REQ-ACA-005: a value changes as data without a release, every parameter has an owner and a default, and a secret is listed in the catalog and never served, cached, logged or exported by the client. The measure is the legacy one: zero business values found in code by the build checks, on every service, in every build.

### 3. Preconditions

- RWB-PLT-E1042-CON is published (this story's contract deliverable): the client interface and its types, the generated key set, the catalog and value data contract, the four consumed operations, the cache and refresh rule, the start-up rule, the two build-check contracts and the fakes.
- RWB-P3-E1042-CON is published: the rwb-case contract behind the operations, with the catalog entry members, the value-in-force members and the approval event (C dependency; DP-06).
- RWB-P3-E1043-CON is published: the reference-data contract of rwb-case, which carries the product-group codes the typed read resolves (C dependency; DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library, so the approval event is consumed through an inbox row in the consuming service's own schema instead of a second consumer loop (DP-09).
- RWB-PLT-E1027-CON is published: the local decision-record library that the owning service writes the parameter version into; the client only supplies the version (DP-03).
- RWB-PLT-E1047-CON is published: the naming library that fixes `rwb.case.ParameterVersionApproved.v1` and the topic `rwb.case.events.v1` (DP-14).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence, which creates the inbox table the listener uses in each service's own schema (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route; the library adds no route of its own (DP-19).
- The catalog file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, and lists at least `case.entry.dpd` (INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by `recovery.casewf.casecreation`), `refdata.cache.ttl-seconds` (default 300; 30 in SIT) and `ace.db.password` (kind ENVIRONMENT, secret true).
- The ACE secret store holds the secret values per environment; the catalog lists the secret entries and never their values.
- The artifact coordinates of the platform library — the group, the artefact name, the version scheme and the publication channel — are Not specified in the source documents (GAP-1406; ASM-2450).
- The environment name of each deployment (DEV, SIT, UAT, PROD) is a deployment value, not a code constant.
- No build dependency blocks the start of the work: every H dependency above is a platform contract story, so the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The build generates `ParameterKeys` from `config/parameter-catalog.csv`, one constant per catalog key with its Java type, for example `ParameterKeys.CASE_ENTRY_DPD : ParameterKey<Integer>`.
2. A service reads a value only through `Parameters.get(ParameterKeys.CASE_ENTRY_DPD, businessDate)`, optionally with a product group; it never passes a string literal and never reads a configuration file for a business value.
3. `ParameterClient` resolves the environment from the deployment, applies the business date and the product group, and asks `ParameterCache` for the key.
4. On a miss, a stale entry or a forced refresh, the client calls `GET /api/recovery/case/v1/admin/parameters` over one hop with a 2 s budget and the breaker of the caller, and takes the entry with its value in force, its version number and its valid-from date.
5. `ParameterCache` stores the value per key, product group and business date, with the time to live taken from the catalog entry `refdata.cache.ttl-seconds` — 30 in SIT and 300 in PROD — never from a constant.
6. `ParameterVersionApprovedListener` consumes `rwb.case.ParameterVersionApproved.v1` from `rwb.case.events.v1` through the inbox of the outbox and inbox library, records the CloudEvents id in `processed_event` in the consuming service's own schema, and evicts the named `paramKeys` before the next read.
7. A read on a date before the valid-from date of an approved version keeps the earlier version; on the valid-from date the next read answers the new version, with no restart and no deployment.
8. A rollback approved by the owner is announced on the same event; the cache evicts the key and the next read answers the previous value and its version.
9. At start-up `ParameterStartupCheck` reads every required key of the service's own list for the deployment's environment; when one has no value and no default, the check fails with MSG-P3-032, names the key and the environment, and the probe keeps the pod out of traffic.
10. `CatalogEntry entry(String key)` answers the catalog line — kind, type, unit, minimum, maximum, default, scope, required, owner, environments, used by, secret, version and valid-from — and never a value for a line marked secret.
11. The build runs `RwbMagicNumberCheck` over the recovery packages and `CatalogCompletenessCheck` over the keys read; each reports the file, the line and the key, and fails the build.
12. The owning service records the version in its decision record through the local decision-record library; the client writes no decision record of its own.
13. The client publishes its own counters and timers on the platform observability path: reads, cache hits, cache age per key, refreshes, failed refreshes and start-up refusals.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The catalog entry for a required key has no value and no default for the deployment's environment | The start-up check fails for that key and environment; the probe stays unready and the pod takes no traffic | MSG-P3-032 | AC5 |
| X2 | The rwb-case read fails, times out at 2 s or the breaker is open | The read fails with the client's own exception; a cached value inside its time to live is served with its own version and a stale marker; nothing is invented | None | AC8 |
| X3 | A cached value is older than `refdata.cache.ttl-seconds` | The next read re-reads the owner; a failed re-read returns the exception and never a guessed value | None | AC8 |
| X4 | The approval event arrives twice or out of order | The inbox drops the repeat; an older `versionNo` never replaces a newer one in the cache | None | AC8 |
| X5 | A secret entry is asked for as a value | The catalog line is answered without a value; the client never calls the secret store and never logs the line as a value | None | AC4 |
| X6 | Code holds a numeric or string business literal | The build fails and names the file, the line and the catalog key whose default equals the literal | None (build output) | AC6 |
| X7 | Code reads a key that the catalog file does not list | The build fails and names the key | None (build output) | AC7 |
| X8 | A caller passes a string literal instead of a generated key | The interface rejects it, so the read does not compile, and the catalog completeness check has nothing to compare | None (build output) | AC7 |
| X9 | The product-group override has no value for the group | The read answers the GLOBAL value of the same key with its version, never a default written in the service | None | AC1 |
| X10 | The refresh event names a key the service does not read | The event is recorded in the inbox and no cache line is evicted | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the library and platform contracts and the rwb-case fake; no other service has to exist first |
| Negotiable | The cache time to live, the read timeout and the key list are configuration; the types, the operations and the two checks are the published contract |
| Valuable | Gives all 19 services one loader and one build check on Day 1 and removes the two-table read from every service plan |
| Estimable | One interface, four types, one generated key set, one cache, one listener, one start-up check and two build checks |
| Small | Fits one sprint with its tests |
| Testable | Each criterion uses the rwb-case fake, a fixture module and the two build checks of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Parameters client library

  Background:
    Given the catalog lists "case.entry.dpd" as INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by "recovery.casewf.casecreation"
    Given the parameters client library is pinned in the service template at major version 1
    Given the catalog and the value versions are served by rwb-case under /api/recovery/case/v1

  Scenario: AC1 A typed read returns the value, the version and the environment (new, D-RCV-60)
    Given the rwb-case contract mock answers GET /api/recovery/case/v1/admin/parameters with valueInForce 90, versionNo 1 and environment PROD for "case.entry.dpd"
    When a service calls Parameters.get(ParameterKeys.CASE_ENTRY_DPD, businessDate 2026-12-01)
    Then the answer carries key "case.entry.dpd", value 90, versionNo 1, environment PROD and validFrom
    Then the answer is typed Integer and no value is read from a constant, a chart value or a local file

  Scenario: AC2 An approved version takes effect on its valid-from date with no restart (new, D-RCV-60)
    Given version 2 sets "case.entry.dpd" to 91 for PROD with valid from 2026-12-10 and is approved on 2026-12-05
    Given rwb.case.ParameterVersionApproved.v1 carries paramKeys [case.entry.dpd], versionNo 2 and validFrom 2026-12-10
    When the library serves the read on 2026-12-09 and on 2026-12-10
    Then it answers 90 with versionNo 1 on 2026-12-09 and 91 with versionNo 2 on 2026-12-10
    Then no pod restarts and no deployment runs between the two reads

  Scenario: AC3 A rollback returns the previous value (new, D-RCV-60)
    Given value version 2 of "case.entry.dpd" is in force and version 1 was in force before it
    Given the rwb-case contract mock answers POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback with 200 and the load status ROLLED_BACK
    Given rwb.case.ParameterVersionApproved.v1 follows for versionNo 1
    When the library serves the next read for PROD
    Then it answers 90 with versionNo 1
    Then the cache holds no line for version 2

  Scenario: AC4 A secret entry is listed and no value is returned (new, D-RCV-60)
    Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
    Given the rwb-case contract mock answers GET /api/recovery/case/v1/admin/parameters with the entry and no valueInForce
    When a service asks the client for CatalogEntry "ace.db.password"
    Then the answer carries kind ENVIRONMENT, owner, environments, used by and secret true
    Then the answer carries no value and the client asks neither the owner nor the secret store for one

  Scenario: AC5 A required value missing for UAT stops the start (new, D-RCV-60)
    Given "refdata.cache.ttl-seconds" is required and has no value and no default for UAT
    Given the rwb-case contract mock answers GET /api/recovery/case/v1/admin/parameters with no valueInForce for UAT
    When a service starts in UAT
    Then the start-up check fails with MSG-P3-032 naming "refdata.cache.ttl-seconds" and "UAT"
    Then the health probe answers DOWN and the pod takes no traffic

  Scenario: AC6 A literal business value fails the build (new, D-RCV-60)
    Given a fixture module in package "recovery.casewf.casecreation" with the literal 90 in the entry rule
    When RwbMagicNumberCheck runs in the build
    Then the build fails
    Then the report names the file, the line and the key "case.entry.dpd" whose default is 90
    When the same module carries the literals 0, 1 and -1 outside test code and the literal 90 in test code
    Then the check passes, because 0, 1, -1 and test code are the allowed literals

  Scenario: AC7 An unknown key fails the build (new, D-RCV-60)
    Given a fixture module that reads the key "allocation.retry.limit", which the catalog file does not list
    When CatalogCompletenessCheck compares the keys read with config/parameter-catalog.csv
    Then the build fails naming "allocation.retry.limit"
    Then a read through a generated ParameterKeys constant passes, because every generated key is in the catalog file with an owner and a default

  Scenario: AC8 The cache refreshes on the approval event and serves only approved values (new, D-RCV-60)
    Given the client holds versionNo 1 of "case.entry.dpd" and the catalog entry "refdata.cache.ttl-seconds" is 300 for PROD
    When rwb.case.ParameterVersionApproved.v1 for versionNo 2 arrives on rwb.case.events.v1
    Then the client evicts the key before the next read and the inbox drops a repeat of the same CloudEvents id
    When the event is lost and the time to live passes
    Then the client re-reads GET /api/recovery/case/v1/admin/parameters and still serves only the approved version
    Then a version whose load status is VALIDATED and not APPROVED is never served, read from the cache or from the owner
```

No legacy acceptance criterion is copied into this story. The eleven legacy criteria `AC1` to `AC11` of RWB-E1-042 stay with RWB-P3-E1042-APP, which owns the catalog, the value versions and the five operations; the eight criteria above are new and test only the client library and its two build checks. The values they use — `case.entry.dpd`, the range 1 to 365, the default 90, the scope GLOBAL, the owner RW-COE, the used-by `recovery.casewf.casecreation`, `refdata.cache.ttl-seconds` 30 in SIT and 300 in PROD, `allocation.retry.limit`, `ace.db.password`, versions 1 and 2, the dates 2026-12-05, 2026-12-09 and 2026-12-10 and the message ids — are the legacy story's, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No business value in code: every limit, threshold, name and timer is read at run time through a generated key, and the build fails on a literal business value | Legacy BR1; Principle 1; DT02; BR-P3-022; DP-06 |
| BR2 | Every key a service reads is in the catalog file with an owner and a default, and the build fails naming the key that is not | Legacy BR2; REQ-DRI-010 |
| BR3 | A value changes only through the owner's checked, approved, dated load; the client shows the new value on its valid-from date and the previous one before it | Legacy BR3; CTL-08; AC2 |
| BR4 | A client never serves a value version that is not APPROVED, and an open decision keeps the version it was taken under because the owning service records the version it read | Legacy BR5; R-UNI-38 |
| BR5 | A secret entry is listed in the catalog and held only in the secret store: the client returns no value for it and never asks for one | Legacy BR6; DL26; REQ-ACA-005 |
| BR6 | A service does not start without every required value for its environment; the probe keeps the pod out of traffic | Legacy BR7; AC5 |
| BR7 | The client is not authoritative: it caches a value it has read, with a time to live that is itself a catalog entry, and re-reads the owner when the event arrives or the time to live passes | Legacy section 4 step 8; ASM-2451 |
| BR8 | The environment is a deployment value and the product group is a request value; neither is a constant of the code | Legacy AC8; ASM-2451 |
| BR9 | The two build checks are held once in the library and applied by the service template: a literal business value and an unknown key fail the build with the file, the line and the key | Legacy section 13; ASM-2452 |

### 9. State transitions

The client holds no case status and changes none. It holds one cache line per key, product group, business date and environment, and the owner holds the version states the legacy story fixed (VALIDATED, APPROVED, ROLLED_BACK).

| From | Event | Condition | To |
|---|---|---|---|
| No line | First read | The owner answers an approved version | Loaded with that version and its valid-from date |
| Loaded | Read before the valid-from date of a newer approved version | The newer version is not yet in force | Loaded, still the earlier version |
| Loaded | The valid-from date arrives | The newer version is approved and in force | Loaded with the newer version, no restart |
| Loaded | `rwb.case.ParameterVersionApproved.v1` | The CloudEvents id is new to the inbox | Evicted, then loaded on the next read |
| Loaded | The time to live passes | None | Stale; re-read on the next read |
| Stale | The owner answers | None | Loaded with the version in force |
| Stale | The owner fails | A value inside the last known state exists | An exception to the caller; never a guessed value |
| Loaded | Owner rollback to an earlier version | The earlier version is APPROVED | Loaded with the earlier version |
| Any | A required key has no value at start-up | The deployment's environment | Start refused with MSG-P3-032 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Owns the catalog file and the values; the client reads what the owner approved |
| RW-RISK | Approves a value version where a threshold or a limit moves, on the owner's service; the client has no approval path |
| RW-PLATADM | Owns the environment settings and reads the client's counters and start-up refusals |
| RW-AUDIT, RW-COMPLY | Read the client's version trace and the build reports |
| The owning service of each caller | Chooses the keys it reads, lists the required ones and records the version it read in its decision record |
| Platform library team, owning the template | Publishes the interface, the generated keys, the cache rule and the two build checks; changes them only through the contract story |
| No delegation of authority level applies | A parameter is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-132 to DF-REF-146 | parameter_catalog | all fields | Read only, through the rwb-case contract |
| DF-REF-147 to DF-REF-158 | parameter_value | all fields | Read only, through the rwb-case contract |
| The outbox and inbox library tables | processed_event | ce_id, consumer_group, processed_at | Write, in the consuming service's own schema, through RWB-PLT-TE006-CON |

Field IDs are those in the Logical Data Model and Data Dictionary. `parameter_catalog` and `parameter_value` are P3 tables in the rwb_case schema under the Ownership Map; this story names them and never creates, reads or writes a copy of either (DP-01). The client holds no business table: its cache is in memory and its only row is the inbox row it already has through the outbox and inbox library. The cache line members — key, product group, business date, environment, value, version number, valid-from date and read time — are the working read of this run and have no field identifier of their own (GAP-1406; ASM-2451).

### 12. Contract

#### 12.1 REST operations provided

None — the library has no REST surface. The five operations of the legacy story belong to P3 rwb-case under the REST base `/api/recovery/case/v1`, and RWB-P3-E1042-APP provides them.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The typed read, the catalog entry and the start-up check; one hop, 2 s budget, breaker and bulkhead of the caller |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | Drives a new value version in the contract test of this story; the client never loads a value |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | The approval whose event refreshes the cache, driven by the contract test |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 rwb-case | The rollback whose event returns the previous value, driven by the contract test |

Only the read is called at run time; the three load operations are the owner's and are driven by the contract test and the operator rehearsal of the deployment story, so that the client is proved against a new version, an approval and a rollback on the owner's own paths and never against a value of its own.

#### 12.3 Events published

None — the client publishes no event. A cache refresh is local to the service that received the owner's event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.case.ParameterVersionApproved.v1` | `rwb.case.events.v1` | P3 rwb-case | Carries `paramKeys`, `versionNo` and `validFrom`; the listener evicts those keys through the inbox, in the consuming service's own consumer group |

The event name follows the §R4 naming of the owner's topic and is recorded in ASM-2453; the payload members are the legacy story's. The client subscribes once per service and adds no second consumer group.

#### 12.5 Workflows and activities

None — the client is library code inside each service; it starts no workflow and no activity, and a service that needs a workflow for its own step uses the workflow kit.

#### 12.6 Schedules

None — the refresh is event-driven and otherwise lazy by the time to live; no Temporal Schedule and no Quartz job is created (GAP-1406; ASM-2451).

#### 12.7 Tables owned

None — `parameter_catalog` and `parameter_value` are P3 tables, named only. The client creates no table, owns no table and writes no row except the inbox row that the outbox and inbox library already owns in the consuming service's own schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case parameters fake | `GET /api/recovery/case/v1/admin/parameters` | `case.entry.dpd` version 1 = 90 and version 2 = 91 from 2026-12-10 for PROD; `refdata.cache.ttl-seconds` 30 for SIT and 300 for PROD; `ace.db.password` listed with no value; a required key with no value for UAT |
| rwb-case reference-load fake | The three load operations | A load answered 201, an approval answered 200, a rollback answered 200 with status ROLLED_BACK, and one refusal of each kind |
| rwb-case approval-event fake | `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` | One event for `case.entry.dpd` version 2, one repeat of the same CloudEvents id and one rollback event for version 1 |
| Inbox fake | The outbox and inbox library | A repeated CloudEvents id that is dropped, and a new id that is recorded |
| Fixture modules | The two build checks | A module with the literal 90, a module reading `allocation.retry.limit`, a module with 0, 1 and -1, and a module with the literal 90 in test code |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 4 consumed | The read at run time; the three load operations in the contract test and the operator rehearsal |
| Kafka | None published, 1 consumed | `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1`, through the inbox |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | `config/parameter-catalog.csv` is a build input of the key generator and the completeness check, never a run-time read |

### 13. Solution plan

**Package.** Shared library artefact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.params`; the published interface and types in `th.co.scb.ace.workbench.recovery.platform.params.api`; the two build checks in `build-tools/rwb-checks`. The legacy package `recovery.casewf.config` is the monolith's and is not carried.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The client reads the catalog through the rwb-case contract and holds no copy | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the client supplies the version and the owning service writes the record | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. This story is that client library, and the rwb-case contract is what it reads | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the product-group codes the typed read resolves are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The approval event is consumed through the inbox | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The old in-process `ParameterService` call becomes one REST read with a mock and a breaker | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the client calls `/api/recovery/case/v1/admin/parameters` and adds no base of its own | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The refresh event is `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the inbox row the listener writes arrives through that sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route; the client adds no screen, no route and no state of its own | H RWB-PLT-N001-CON |

**Hardware and software change.** The two-table read in one database becomes one REST read of the rwb-case contract from each of the 19 services, with a per-service cache and a breaker; the time to live moves from a property to a catalog entry read through the same client; the approval event arrives on the owner's Kafka topic and is consumed through the library inbox; and the two build checks move from the monolith's build to the platform library, where the service template applies them to every service. No new hardware is implied: the client runs inside the existing service pods on the AKS cluster, and the catalog and the values stay on the ACE PostgreSQL server in the rwb_case schema under the owner's login.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `Parameters` | Published interface | `get(ParameterKey<T>, LocalDate)`, `get(ParameterKey<T>, String productGroup, LocalDate)` and `CatalogEntry entry(String key)` (BR1, BR7) |
| `ParameterKey<T>`, `ParameterValue<T>`, `CatalogEntry` | Published types | The key with its type; the value with `key`, `value`, `versionNo`, `validFrom` and `environment`; the catalog line with its thirteen members |
| `ParameterKeys` and `ParameterKeysGenerator` | Generated source and build tool | One constant per catalog key, generated from `config/parameter-catalog.csv`; a key that is not in the file is not generated (BR2) |
| `ParameterClient` | Service | Environment, business date and product-group resolution; one hop, 2 s budget, breaker and bulkhead; the version in the answer (BR3, BR8) |
| `ParameterCache` | Service | One line per key, product group, business date and environment; time to live from `refdata.cache.ttl-seconds`; approved versions only (BR4, BR7) |
| `ParameterVersionApprovedListener` | Service | Consumes the approval event through the inbox, drops a repeat and evicts the named keys (BR7) |
| `ParameterCatalogReadClient` | Client | Calls the read operation and leaves the value out of a secret line (BR5) |
| `ParameterStartupCheck` | Service | Reads the service's required keys for its environment and fails the start with MSG-P3-032 (BR6) |
| `RwbMagicNumberCheck` | Build tool | Fails on a numeric or string business literal in the recovery packages; allowed: 0, 1, -1, test code; names the catalog key whose default equals the literal (BR9) |
| `CatalogCompletenessCheck` | Build tool | Compares the keys read through `ParameterKeys` with the catalog file; fails on a missing key, owner or default (BR2, BR9) |
| `ParameterMetrics` | Service | Counters and timers for reads, cache age, refreshes, failed refreshes and start-up refusals |

**Configuration and reference data.** The environment name, the location of `config/parameter-catalog.csv` and the bootstrap of the cache time to live are deployment values; from the first successful read the time to live is the catalog entry `refdata.cache.ttl-seconds`, 30 in SIT and 300 in PROD (ASM-2451; ASM-2455). The required key list of each service is a short list in that service's own configuration, and the build check proves every key on it exists in the catalog file. The legacy feature flag `rwb.p3.configservice` stays with the owner's service (RWB-P3-E1042-APP); the library has no flag of its own.

**Build steps**

1. Publish the interface and the four types from the CON story; test that a string literal does not compile (AC1, AC7).
2. Write `ParameterKeysGenerator` and generate `ParameterKeys` from the catalog file; test a key that the file does not list (AC7).
3. Write `ParameterClient` with the environment, date and product-group resolution and the 2 s budget; test the read, the pre-valid-from date and the valid-from date (AC1, AC2).
4. Write `ParameterCache` with the time to live read from the catalog and the approved-only rule; test the stale line and the failed re-read (AC2, AC8).
5. Write `ParameterVersionApprovedListener` against the inbox; test the eviction, the repeat drop and the out-of-order event (AC8).
6. Write `ParameterCatalogReadClient` with the secret line left out; test the listed entry with no value and the owner not asked (AC4).
7. Write `ParameterStartupCheck` and the readiness probe wiring; test the missing value for UAT (AC5).
8. Write `RwbMagicNumberCheck` and `CatalogCompletenessCheck` with the file, line and key in the report; test both on the fixture modules (AC6, AC7).
9. Run the contract test against the fakes of section 12.8 for a rollback and for a load, with the owner's three operations driven from the test (AC3).
10. Wire the metrics and hand the version to the owning service's decision record as a contract test (AC1, AC8).

**Done when.** The seven test cases of section 16 pass, the contract test of the CON story passes against the fakes, the two build checks run green on main over the 19 services with the file, line and key in every finding, and one service in SIT reads `case.entry.dpd` through the client with no value in its own image or chart.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | A loaded value is outside its range, on the owner's operation | {field} must be between {min} and {max}. |
| MSG-P1-002 | A loaded value has the wrong type or an unknown key, on the owner's operation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | The load file is empty, on the owner's operation | Enter {field}. |
| MSG-P7-002 | The approver is the author, on the owner's operation | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | A rollback has no earlier version, on the owner's operation | There is no earlier version of {table} to return to. |
| MSG-P4-002 | A role without the right calls the owner's operation | You cannot {action} here. Your role does not include it. |

MSG-P3-032 is the only message the library raises; the other six are the owner's, carried here unchanged because the contract test of this story drives the operations that raise them. The two build checks raise no user-facing message: their finding is the build output, with the file, the line and the key. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen of its own. A squad member sees the two build findings in the pipeline output, with the file, the line and the key, and a cache or start-up event in the service's own log and on SCR-44 Interface and job monitor. SCR-39 Rules and parameters belongs to Epic 8 and reads the owner's operation; the client adds no screen, no route and no state to any screen (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1042-APP-01 | AC1, BR1, BR8 | Component | `case.entry.dpd` version 1 = 90 in PROD; the typed read, the product group and the version in the answer |
| TC-PLT-E1042-APP-02 | AC2, BR3, BR7 | Component | Version 2 = 91 from 2026-12-10, approved 2026-12-05; reads on 2026-12-09 and 2026-12-10 with no restart |
| TC-PLT-E1042-APP-03 | AC3, AC4, BR4, BR5 | Contract | The rollback to version 1; the secret line `ace.db.password` with no value; the owner's three operations driven from the test |
| TC-PLT-E1042-APP-04 | AC5, BR6 | NFR | UAT with no value and no default for `refdata.cache.ttl-seconds`; MSG-P3-032; the probe unready and no traffic |
| TC-PLT-E1042-APP-05 | AC6, BR1, BR9 | Component | Fixture with the literal 90, then 0, 1, -1 and test code; the file, line and key in the report |
| TC-PLT-E1042-APP-06 | AC7, BR2, BR9 | Component | Fixture reading `allocation.retry.limit`; a generated key that passes |
| TC-PLT-E1042-APP-07 | AC8, BR4, BR7 | NFR | Approval event, repeat event and a lost event with the 300 s time to live; cache age, eviction and no unapproved value |

The levels are the target shape: the legacy `System` level becomes Component, and the cache, the time to live and the start-up refusal are measured as NFR. The legacy test case ids are not reused here — they stay with RWB-P3-E1042-APP, which executes them.

### 17. Guardrails

- No business value in code: every limit, threshold, name and timer is a catalog entry read through a generated key, and `RwbMagicNumberCheck` fails the build on a literal.
- No key outside the catalog: `CatalogCompletenessCheck` fails the build naming a key that the catalog file does not list, and the generator cannot create a constant for it.
- No personal data in the cache, a log, a test or a prompt; a parameter is a threshold, a name or a timer, never a person.
- No secret value in the cache, a response, a log or a build report: a secret line is listed and its value is never asked for.
- No read of another service's tables: the catalog and the values arrive over the rwb-case contract only, and the client holds no copy (DP-01).
- No value change needs a deployment and no parameter needs a code change: a new value is the owner's load, and a new parameter is a reviewed catalog entry.
- The client is never authoritative: a cached value carries its version and its read time, and a stale value is marked rather than presented as current.
- The library adds no REST base, no topic and no task queue of its own; it is not one of the 19 services.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | Epic 1, 3.3; Program, 5.7 | FEAT-CWC-22 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1042-APP-01 to TC-PLT-E1042-APP-07 |
| REQ-ACA-005 | Secrets are listed in the catalog and held only in the secret store | Epic 1, 3.4 | FEAT-ACA-05 | 14 Set strategy, policy and decision rules | DL26 | TC-PLT-E1042-APP-03 |

| Legacy test cases | Disposition |
|---|---|
| `TC-E1-042-01, TC-E1-042-02, TC-E1-042-03, TC-E1-042-04, TC-E1-042-05, TC-E1-042-06, TC-E1-042-07, TC-E1-042-08, TC-E1-042-09, TC-E1-042-10, TC-E1-042-11, TC-E1-042-12` | executed by RWB-P3-E1042-APP |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1042-CON | Contract | H: publishes the interface, the types, the generated keys, the data contract, the cache and start-up rules and the fakes this story implements |
| RWB-PLT-E1042-OPS | DevOps | X: deploys the pinned library, the chart values, the catalog file, the probe and the alerts |
| RWB-P3-E1042-APP, RWB-P3-E1042-CON | App development, Contract | C: the owner of the catalog, the value versions, the five operations and the legacy acceptance criteria and test cases |
| RWB-PLT-E1043-CON | Contract | H: the reference-data client for the product-group codes; C RWB-P3-E1043-CON is the owner behind it |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the owning service writes the version into |
| RWB-PLT-TE006-CON | Contract | H: the inbox the approval event is consumed through |
| RWB-PLT-E1047-CON | Contract | H: the naming library behind `rwb.case.ParameterVersionApproved.v1` |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence that creates the inbox row |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route; the client adds no route |

REQ-ACA-005 has no row in legacy section 18; its short text is legacy BR6 and its BRD section is the one the legacy Epic 1 story of the same requirement carries.

### 19. Out of scope

- The catalog rows, the value versions and the seed of the catalog: RWB-P3-E1042-APP and its Flyway sequence in `rwb_case`.
- The service that serves the five operations, its own cache and its own decision of the version in force: RWB-P3-E1042-APP.
- The five REST operations themselves and their authorisation model: RWB-P3-E1042-APP and RWB-P3-E1042-CON.
- The administration screen SCR-39 Rules and parameters: Epic 8.
- Product-specific parameters and service levels: the product-parameter story of RWB-E1-045, RWB-P3-E1045-APP.
- The reference tables and the reference-data service: RWB-PLT-E1043-APP, RWB-PLT-E1043-CON and RWB-P3-E1043-APP.
- The decision record itself and the central ledger: the owning service through RWB-PLT-E1027-CON and RWB-P7-E1027-CON.
- The secret store, its rotation and its access path: the platform, and the secrets baseline of the platform.
- The Kafka topic, its ACLs and the schema registry: RWB-PLT-EVT.
