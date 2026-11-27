# RWB-PLT-N009-APP RFC 9457 problem and Idempotency-Key helpers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the shared Problem members and v6 message map, with the replay code log-only. Backfilled 8 mapped v9 test case IDs.
- Problem body: `code` renamed to `messageCode`; `messageTh`, `field`, `errors` added; the owning service stamps `instance` (RD-P1-004; findings #1, #6, #7; AC1, AC10).
- Idempotency filter: UUID header, endpoint and request hash, replayed status, 409 for mismatch and in flight, 503 code, 24-hour expiry (RD-P1-001; #2 to #5; X3 to X6, AC2 to AC5, AC9).
- Left pending: package coordinates and map path (GAP-1400, ASM-2436); endpoint longer than 100 characters (GAP-3317, #8).

**Change log.** D-RCV-60, 22 November 2026: new platform story for the implementation of the RFC 9457 problem detail and Idempotency-Key helpers and their wiring into the service template, with no legacy story behind it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 5 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-N009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N009 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-LIB-A |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-PLT-N009-CON, RWB-PLT-TE006-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| Contract version | RWB-PLT-N009-CON v1 (v3 story) and its fake of the same version; `Problem` schema identical to the component of API Specification v7 |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004 |

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the two helpers implemented in the platform library and wired into the service template — the problem detail writer with its error map and trace identifier, the idempotency filter that requires the header on every POST and stores and replays the first response in the calling service's own `idempotency_key` table through the outbox library's guard, and the usage examples**, so that **every one of the 19 services answers an error and a repeated command the same way without writing a local implementation**.

This is the app story of new platform key N009 under epic RWB-PLT-LIB. The Change Register reads "RFC 9457 problem and Idempotency-Key helpers - interface and fake" and creates the pair RWB-PLT-N009-CON and RWB-PLT-N009-APP; there is no legacy story, no legacy acceptance criterion and no legacy test case behind the key, so every criterion below is new and tests only the implementable deliverable in the title.

The story builds against two published contracts at major version 1 and adds no rule of its own:

- RWB-PLT-N009-CON fixes the two interfaces, the problem detail members of RD-P1-004, the media type `application/problem+json`, the error map as data, the `Idempotency-Key` header rule, the stored-response scope and the same-key, mismatch, in-flight and 24-hour expiry rules of RD-P1-001.
- RWB-PLT-TE006-CON publishes the DDL contract of the `idempotency_key` table, and of the outbox and inbox tables beside it, so the stored response is written into the calling service's own schema through that template and not through a table of this story.

What the story delivers is the working implementation and its wiring: the problem detail writer with its map loader and its trace identifier, the error map file shipped with the library, the idempotency filter in front of every POST, the replay of a stored response and the refusals of a missing key, a mismatched body and an unavailable store, the usage examples, and the template change that puts both helpers into every generated service. The implementation reads and writes the calling service's own schema through the library's own login context, so no service writes a local implementation and no helper opens a second connection of its own.

The package name, the registry and the version label of the helper, and the file path the error map is built from are Not specified in the source documents (GAP-1400; ASM-2436); section 13 carries the working read of each.

### 2. Business rationale

Architecture v5 slide 11 fixes two rules for every call: errors as RFC 9457 problem details, and an `Idempotency-Key` on every POST. Slide 20 fixes that every service comes from the service template and the shared libraries. Read together, the two slides are a delivery constraint: if the error body and the repeat rule live in each service's code, nineteen teams write nineteen versions of them, and the estate drifts from the standards it claims to follow at the first incident.

A contract alone does not stop that drift; a pinned implementation in the template does. This story is what makes the contract the only way a service writes an error: the problem detail writer is the library's, the error map is data shipped with it, the filter sits on the template's POST path, and a generated service carries no local copy of either. The contract test then fails the build of a service that writes its own body or its own key table.

The repeat rule is the part with a business consequence. A timeout after a payment or a treatment command is common, and a retried submission that posts twice is not a technical defect but a wrong outcome on a customer's account. Storing the first response and replaying it is the only way to make a retry safe without asking an officer to remember whether the first attempt worked. Doing it in the library, in the caller's own schema, through the table contract of RWB-PLT-TE006-CON, keeps the ownership rule intact: no service reads another service's table, and the library creates none.

The measure is the one the contract sets: one error shape across the 19 services and zero second effects for a repeated key, proven in the contract test of every generated service.

### 3. Preconditions

- RWB-PLT-N009-CON is published with major version 1: the two interfaces, the member set of BR1, the media type, the error map as data, the header rule and the stored-response rules, with its fakes.
- RWB-PLT-TE006-CON is published: the DDL contract of the `idempotency_key` table, with the columns `idempotency_key` (uuid, unique), `endpoint`, `request_hash` and `response` (LDM DF-OPS-184 to DF-OPS-188), applied by each service's own Flyway sequence in its own schema (DP-09, DP-15).
- Architecture v5 slide 11 fixes the behaviour the filter applies: HTTPS/JSON with mesh mutual TLS, a 2 s timeout, GET retried once with jitter, an `Idempotency-Key` on every POST and RFC 9457 problem details on every error, with no call chain deeper than one hop.
- Architecture v5 slides 11, 22 and 49 fix the trace standard: OpenTelemetry with the W3C Trace Context, one trace across REST, Kafka and Temporal, and the trace identifier that the problem detail carries.
- The service template generates every one of the 19 services and carries the baseline it pins, so a helper that the template wires reaches all of them (Architecture v5 slide 20).
- The gateway route contract RWB-PLT-N001-CON fixes the public envelope at the edge and the pass-through of the owner's `messageCode` and detail.
- The package name, the registry and the version label of the artefact, and the file path the error map is built from are Not specified in the source documents (GAP-1400; ASM-2436).
- The stored response is the `idempotency_key` table of RWB-PLT-TE006-CON applied in the calling service's own schema, so this story creates no table and no column of its own (ASM-2437).
- No approval is required to start: the story is Draft (realignment v1) and builds against the two published contracts and their fakes.

### 4. Flow

1. Pin the contract: resolve RWB-PLT-N009-CON at major version 1 through the template's baseline pin and record the version in the library manifest with the usage examples.
2. Build the problem detail writer: the members `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional), the `application/problem+json` media type, the trace identifier taken from the current W3C trace context, and the refusal of a stack trace, an internal path, SQL and a personal value.
3. Build the error map loader: the map file shipped with the library, one row per message code, loaded at start-up, with a code that has no row failing the start-up check and no default status substituted.
4. Build the domain error to message code map: an exception type maps to the message code and the instance of the failing request, and the writer takes the status, the `type`, the `title` and the `detail` from the map row.
5. Build the idempotency filter on the template's POST path: the header read; a missing, blank or non-UUID value refused with 400 `MSG-PLT-N009-03` before the handler; `endpoint` taken as method plus resolved path and `request_hash` as the SHA-256 of the raw request body, of the empty string when there is no body. PUT, PATCH, GET and DELETE pass without a key.
6. Build the stored-response read and write through the outbox library's guard against the `idempotency_key` table of the calling service's own schema: the first status, body and headers stored for 24 hours; a replay of the stored status and body for the same key, endpoint and hash; 409 `MSG-PLT-N009-05` for another endpoint or hash and for a request while the first is in flight; 503 `MSG-PLT-N009-06` for an unreachable store with the caller's transaction rolled back; a purge of rows older than 24 hours.
7. Wire both helpers into the service template: the filter registered on the POST path, the writer registered as the exception handler, the map packaged with the service, and the generated build carrying the pinned helper version.
8. Publish the usage examples: one error written from a domain exception, one error written from a message code, one command replayed from a stored response, one command refused for a different body, and the check that a generated service carries no local copy of either helper.
9. Run the contract test against the published artefact and the fakes, and fail the build of a generated service that writes its own error body, its own error map or its own key table.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A handler writes its own error body or a local error map | The contract test fails the build; the local class and the local map are removed in favour of the library | MSG-PLT-N009-01 | AC1, AC7 |
| X2 | An error is raised for a message code with no map row | The start-up check fails and names the code; the service does not start | MSG-PLT-N009-02 | AC1, AC6 |
| X3 | A POST arrives with no `Idempotency-Key` header, with a blank value or with a value that is not a UUID | Refused with a 400 problem detail; the handler is not invoked and no transaction is opened | MSG-PLT-N009-03 | AC2 |
| X4 | The same key arrives on the same endpoint with the same request body within 24 hours | The stored status, body and headers are replayed, and the handler does not run again | MSG-PLT-N009-04 (log only) | AC3 |
| X5 | The same key arrives with a different endpoint or request body, or while the first request is still in flight | Refused with a 409 problem detail; the stored response is not overwritten and no row is added | MSG-PLT-N009-05 | AC4, AC9 |
| X6 | The `idempotency_key` table is unreachable, or its read times out | A 503 problem detail, nothing written and the caller's transaction rolled back | MSG-PLT-N009-06 | AC5 |
| X7 | The error map, the log record or a usage example carries a business value or a personal value | The scan fails the build and names the field and the rule, never the value | MSG-PLT-N009-07 | AC6 |
| X8 | A value no source names is needed (package name, registry, version label, map path) | Published as the working read of the assumption with the gap open; it is never guessed into code or into an example | Not specified in the source documents (GAP-1400; ASM-2436) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the two published contracts and their fakes; it needs no service and no producer to exist, and the stored response uses the caller's own schema in a throwaway test schema |
| Negotiable | The package coordinates, the map file path and the wording of a usage example are open until the release; the members, the media type, the header name, the three repeat rules and the template wiring are fixed by the contract |
| Valuable | All 19 services inherit one error shape and one repeat rule from the template on Day 1, and no squad writes either |
| Estimable | Two helpers, one map loader, one filter, the stored-response path, the template wiring and five usage examples |
| Small | One sprint for the implementation and the template wiring, with its tests |
| Testable | Each criterion is a component test, a contract test or an NFR assertion against the fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: the RFC 9457 problem detail and Idempotency-Key helpers in the platform library and the service template

  Background:
    Given the two helpers are published by RWB-PLT-N009-CON with major version 1
    Given the idempotency_key table is created in each service's own schema from the DDL contract of RWB-PLT-TE006-CON
    Given every one of the 19 services is generated from the service template

  Scenario: AC1 One problem detail shape from every service, with the media type, the members and the trace identifier (new, D-RCV-60)
    Given a service generated from the service template and built with the helper
    When any operation fails
    Then the answer is one application/problem+json body with type, title, status, messageCode and traceId, optionally detail, instance, messageTh, field and errors, and no other member
    Then instance, where written, is the request path plus the trace identifier stamped by the owning service
    Then the status and the type come from the error map row of the message code and never from a literal in the service
    Then traceId is the W3C trace identifier of the request and the body carries no stack trace, no internal path, no SQL and no personal data
    Then the shape is identical in all 19 services because it comes from the library and not from a local class

  Scenario: AC2 A POST with no key or a blank key is refused with 400 and a problem detail (new, D-RCV-60)
    Given a service with the idempotency filter in front of every POST
    When a POST arrives with no Idempotency-Key header, with a blank value or with the value "abc-123"
    Then each answer is 400 with messageCode MSG-PLT-N009-03
    Then the handler is not invoked, the transaction is not opened and nothing is written
    Then the same POST with a UUID value passes the filter and runs once
    Then a PUT, a PATCH, a GET and a DELETE with no header are not refused and store nothing

  Scenario: AC3 A repeated key returns the stored response with no second effect (new, D-RCV-60)
    Given the first POST of a command answered 201 and stored its response against the key, its endpoint and its request hash
    When the same key arrives again on the same endpoint with the same request body within 24 hours
    Then the stored 201 status, body and headers are returned and MSG-PLT-N009-04 appears in the log only
    Then the handler runs no second time, no second row is written and no event is published a second time
    Then the stored response is read from the calling service's own idempotency_key table
    Given the same command with no request body, so that request_hash is the SHA-256 of the empty string
    Then the replay on the same resolved path returns the stored response

  Scenario: AC4 A repeated key with a different request body is refused with 409 (new, D-RCV-60)
    Given a key stored with its first endpoint and request body
    When the same key arrives with a different request body or on a different endpoint
    Then the answer is 409 with messageCode MSG-PLT-N009-05 and never 422
    Then the stored response is not overwritten, no row is added and the handler does not run

  Scenario: AC5 An unavailable idempotency store is answered with a 503 problem detail and nothing is written (new, D-RCV-60)
    Given the calling service's idempotency_key table is unreachable
    When a POST arrives with a UUID header, or the store read times out
    Then the answer is 503 with messageCode MSG-PLT-N009-06 and the caller's transaction is rolled back
    Then no row is written in the idempotency_key table and no event is published
    Then the failure is logged with the trace identifier, the operation and the message code, and with no request body, no header value and no personal data

  Scenario: AC6 The error map carries no business value and no record carries personal data, a stack trace or an internal path (new, D-RCV-60)
    Given the error map and the log record the helper writes
    When both are scanned
    Then no error-map row carries a threshold, a band, a limit, a rate or a date
    Then the log record carries the trace identifier, the span identifier, the service identifier, the operation, the status and the message code only
    Then no record carries a name, an email address, an account number, an amount, the request body or a credential

  Scenario: AC7 The template wires both helpers into every generated service and the contract test fails on drift (new, D-RCV-60)
    Given the service template at the pinned baseline version that carries the two helpers
    When a service is generated from it
    Then the generated build carries the problem detail writer and the idempotency filter with no local copy of either
    Then the contract test of the generated service runs against the published artefact and fails its build on any drift from RWB-PLT-N009-CON section 12
    Then a service that writes its own error body, its own error map or its own key table fails the same build

  Scenario: AC8 Each rule BR1 to BR8 of section 8 is covered by a criterion and a test case of this story (new, D-RCV-60)
    Given the eight business rules BR1 to BR8 of section 8
    When the criteria of section 7 and the test cases of section 16 are reviewed against them
    Then BR1 and BR2 are proved by AC1 and TC-PLT-N009-APP-01, BR3 by AC2 and TC-PLT-N009-APP-02, BR4 by AC3 and TC-PLT-N009-APP-03 and BR5 by AC4 and TC-PLT-N009-APP-04
    Then BR6 is proved by AC5 and TC-PLT-N009-APP-05, BR7 by AC6 and TC-PLT-N009-APP-06, and BR8 by the contract test of AC7 and TC-PLT-N009-APP-06
    Then no rule of section 8 is left without a criterion and a test case

  Scenario: AC9 A second request in flight is refused and a row expires after 24 hours (new, RD-P1-001)
    Given a first POST with key "3f0c9a52-7d1e-4c0b-9a1e-2b6f5d8c1a10" is still running and its row is locked
    When a second POST with the same key arrives
    Then the answer is 409 with messageCode MSG-PLT-N009-05 and the handler runs once only
    Then after the first completes the same request receives the replay
    Given the stored row is older than 24 hours
    When the purge has run and the same key arrives again
    Then the request is a first request and the handler runs

  Scenario: AC10 Several failing inputs are listed in errors (new, RD-P1-004)
    Given a request with two failing inputs
    When the writer answers 422 with messageCode MSG-GEN-001
    Then field names the first failing input and errors holds one row of field, messageCode and detail for each
    Given one failing input
    Then the body has no errors member
```

These criteria are new and test only the library implementation and its template wiring: N009 has no legacy story, no legacy acceptance criterion and no legacy test case, and every value quoted comes from Architecture v5 slides 11, 20, 22 and 49, from the two contract stories and from the Ownership Map. The package coordinates and the map path are Not specified in the source documents (GAP-1400; ASM-2436).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every error a service answers is one RFC 9457 problem detail with the members `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional), with the media type `application/problem+json` | Architecture v5 slide 11; RWB-PLT-N009-CON; RD-P1-004 |
| BR2 | The implementation reads the status and the `type` from the error map shipped as data; a literal status, type or title in service code is a defect and a code with no row fails the start-up check | RWB-PLT-N009-CON; ASM-2436 |
| BR3 | The `Idempotency-Key` header with a UUID value is required on every POST; a missing, blank or non-UUID value is refused with 400 `MSG-PLT-N009-03` before the handler runs | Architecture v5 slide 11; RD-P1-001 |
| BR4 | The first response is stored against the key, with `endpoint` and `request_hash`, in the calling service's own `idempotency_key` table for 24 hours, and a repeat on the same endpoint with the same body replays it with no second effect | Architecture v5 slide 11; ASM-2437; RD-P1-001 |
| BR5 | A repeated key with a different endpoint or request body, or one still in flight, is refused with 409 `MSG-PLT-N009-05` and the stored response is unchanged | RWB-PLT-N009-CON; RD-P1-001 |
| BR6 | An unavailable idempotency store is answered with 503 `MSG-PLT-N009-06`, nothing is written and the caller's transaction is rolled back | Architecture v5 slide 11 |
| BR7 | The helper carries no business value and no personal data: the map holds codes and text, and the log record holds identifiers, the operation, the status and the message code | Architecture v5 slides 11 and 35; Template and Rules §R7.2 s17 |
| BR8 | The helper is pinned by the service template and never copied into a service: a local error body, a local map or a local key table fails the contract test of that service | Architecture v5 slide 20; Template and Rules §R5.7 |

### 9. State transitions

The case status does not change in this story. The states below are the stored response of one key and the pin of one consuming service.

| From | Event | Condition | To |
|---|---|---|---|
| Stored response ABSENT | A POST with a UUID key commits | The handler succeeds | STORED, with the status, the body and the headers of that answer |
| Stored response ABSENT | A POST with a UUID key fails | The handler raises an error | ABSENT, with the problem detail returned and nothing stored |
| Stored response STORED | The same key arrives on the same endpoint with the same request body | No older than 24 hours | REPLAYED, the stored response returned and no second effect |
| Stored response STORED | The same key arrives with a different endpoint or request body | None | REFUSED with 409, the stored response unchanged |
| Stored response STORED | 24 hours pass since the first write | A purge removes older rows | EXPIRED, and the next request with that key is a first request |
| Stored response ABSENT | The `idempotency_key` table is unreachable | None | ABSENT, 503 with a problem detail and the caller's transaction rolled back |
| Consumer pin PINNED | The template moves the pin with the build passing | The contract test is green | PINNED at the new version |
| Consumer pin PINNED | A service carries a local error body or a local key table | None | DRIFTED, the build fails |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform library team (any team, per U3) | Implements, tests and publishes the two helpers with the map and the usage examples, and owns their changelog |
| The service template owner | Wires both helpers into the template and moves the pin, with the build as the gate |
| The consuming squads of the 19 services | Generate their service from the template, use the usage examples and raise a change request against the library instead of a local override |
| The message-catalogue owner | Owns the message codes and their text; the library only loads the map built from the catalogue |
| RW-SECADM, security administrator | Confirms the header rule, the no-personal-data rule of the log record and the no-stack-trace rule of the body |
| RW-PLATADM, platform administrator | Reads the stored responses through the admin path that the owning service and the platform provide, never through a table of another service |
| The security architecture reviewer | Confirms that the implementation meets the standards of Architecture v5 slides 11, 20 and 49 |
| No delegation of authority level applies | A library and a technical rule, not a credit decision |

No personal name, no email address and no credential appears in the library, in a usage example, in a test or in a log. A user, a workload and a service are identifiers and role or scope codes only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Package metadata | The package name, the registry, the version label, the checksum, the usage example path and the pinned contract version: the package name, the registry and the version label are taken from the baseline release of RWB-PLT-NF02-APP (GAP-1400; ASM-2436) | BR8 |
| Problem detail members | `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional); media type `application/problem+json`; the owning service stamps `instance` (request path plus trace ID) and the edge passes `messageCode` and `detail` through (RD-P1-004) | BR1 |
| Error map | The data file shipped with the library, built from the message catalogue: one row per message code, with the status, the `type`, the `title`, the `detail` and the owning service; its build path is Not specified in the source documents (GAP-1400; ASM-2436) | BR2 |
| Log record shape fixed by the helper | Trace identifier, span identifier, service identifier, operation, status and message code. Nothing else | BR7 |
| `Idempotency-Key` header | The name `Idempotency-Key` on every POST; the value is a UUID in canonical 8-4-4-4-12 lower-case form (RD-P1-001) and is never logged | BR3 |
| Stored response | The status, the body and the headers of the first answer, held against the key with `endpoint` (method plus resolved path) and `request_hash`; scope = service schema plus key, the key unique on its own (RD-P1-001; DF-OPS-185 to DF-OPS-188) | BR4 |
| Stored response table | The calling service's own `idempotency_key` table, created from the DDL contract of RWB-PLT-TE006-CON: this story adds no table and no column (ASM-2437) | BR4 |
| Business data | None. The library stores no customer, account, case, document, payment or decision value | BR7 |
| Personal data | None, in any stored response body, log record or example: no name, no email address, no account number, no amount and no request body | BR7 |
| Retention | A stored response is kept 24 hours from its first write; the purge removes older rows; the chart value is the platform's with default 24 h (RD-P1-001) | BR4 |
| Reference data | The error map (the data file shipped with the library, read under BR2) and the expiry window of a stored response (a chart value with default 24 h, RD-P1-001); the reference-data contracts are DP-06 and DP-07 | BR2 |

### 12. Contract

#### 12.1 REST operations provided

None — the library has no REST surface of its own. It supplies the problem detail writer and the idempotency filter that a consuming service applies to the operations its own contract story publishes, and the public envelope belongs to RWB-PLT-N001-CON.

#### 12.2 REST operations consumed

None — the helper joins the caller's own request and calls no service. The contract test reads the published artefact and the fakes, and the stored response is read from the calling service's own schema.

#### 12.3 Events published

None — the library publishes no event of its own. A replayed POST publishes no second event, and an event the consuming service publishes carries the trace context of the request in its headers.

#### 12.4 Events consumed

None — the library consumes no event; the inbox rule for events belongs to RWB-PLT-TE006-CON.

#### 12.5 Workflows and activities

None — the library defines no workflow and no activity and starts none; a command that starts a workflow starts it once, because the repeated POST is answered from the stored response first.

#### 12.6 Schedules

None — the library owns no Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| idempotency_key | PLT | library object created in each service's own schema from the DDL template of RWB-PLT-TE006-CON; this story adds no table and no column |

The stored response is written through the outbox library's guard into the calling service's own copy of the table, under that service's own login: no table of another service is read, no key crosses a schema boundary and the library creates no schema of its own (DP-01, DP-15; ASM-2437).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Problem detail fake | The published member set, the media type and the trace identifier | A body written from a domain error and a body written from a message code, plus a refused body with a stack trace, a path, SQL and a personal value (AC1, AC6) |
| Error-map fixture | One row per message code with its status, its `type`, its `title` and its `detail` | A code with a row, a code with no row and a row with a refused value (AC1, AC6) |
| Idempotency store fake | The stored response per key with endpoint and request hash, in a throwaway schema | A first request, a replay with the stored status, a 409 mismatch, an in-flight request, an expired row, and an unavailable store that answers no read and no write (AC3, AC4, AC5, AC9) |
| Event and edge route fake | The header set of an event and the public error envelope of RWB-PLT-N001-CON | A replayed POST that publishes no second event, and the pass-through of the owner's `messageCode` and detail (AC3, AC7) |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The library adds no path; it supplies the filter and the writer that a service applies to its own operations |
| Kafka | 0 | 0 | No topic and no consumer group; a replayed POST publishes no second event |
| Temporal | 0 | 0 | No workflow and no task queue; a replayed command starts no second workflow |
| File | 0 | 0 | No file is read or written by the library |

The library creates no service, no schema, no topic, no queue, no schedule and no screen: it is a versioned library, a filter and an exception handler that the service template wires into every generated service (ASM-2436).

### 13. Solution plan

**Package.** The platform library artefact, with the two published interfaces in `th.co.scb.ace.workbench.recovery.platform.api` and the implementation in `th.co.scb.ace.workbench.recovery.platform.http`; the error map is a resource of the library, packaged with every service that uses it. The package name, the registry and the version label are Not specified in the source documents (GAP-1400; ASM-2436); the working read is that the baseline release of RWB-PLT-NF02-APP publishes the helper with the rest of the shared libraries and the service template pins one version of that set.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| `ProblemDetailWriter` | Service | Builds the members of BR1, sets `application/problem+json`, reads the trace identifier from the current W3C trace context and refuses a stack trace, a path, SQL and a personal value (BR1, BR3) |
| `ErrorMapLoader` | Service | Loads the map file at start-up, holds one row per code and fails the start-up check on a code with no row (BR2) |
| `DomainErrorMap` | Service | Maps a domain exception type to the message code and the instance of the failing request; holds no status and no text of its own (BR2) |
| `IdempotencyFilter` | Filter | Reads the header on every POST, refuses a missing, blank or non-UUID value with 400, derives the endpoint and the request hash, and calls the store (BR3, BR4, BR5) |
| `IdempotencyStoreAdapter` | Service | Reads and writes the stored response through the outbox library's guard against the calling service's own `idempotency_key` table (BR4, BR6) |
| `StoredResponse` | Value object | The status, the body and the headers of the first answer, with the endpoint and the SHA-256 request hash that the mismatch rule compares (BR5) |
| `ErrorMap` resource | Resource | The data file of one row per message code, packaged with the service |
| Usage examples | Documentation | One error from a domain exception, one from a message code, one replayed command, one refused mismatch and the no-local-copy check (AC7) |

**Database.** No table and no column are added by this story. The stored response is written into the calling service's own `idempotency_key` table, created from the DDL template of RWB-PLT-TE006-CON (`id`, `idempotency_key` uuid unique, `endpoint` varchar(100), `request_hash` char(64), `response` jsonb, plus the standard columns; LDM DF-OPS-184 to DF-OPS-188); the per-service database story applies it through that service's own Flyway sequence, and the library creates no schema, no login and no table (DP-01, DP-15; ASM-2437). The answer for a method plus resolved path longer than 100 characters is Pending: owner platform library owner, tracked as GAP-3317.

**Configuration.** The helper reads the map path, the expiry window of a stored response and the store timeout as configuration of the environment, never as a value in code; the expiry window is a chart value with default 24 h (RD-P1-001), and no business value, threshold, band or rate is read by the helper.

**Pattern application.** None. N009 is a new platform key with no legacy marker, so no Template and Rules §R5.5 row is applied here: the two helpers are the shared mechanism that the consuming stories apply through their own DP rows, and this story adds no pattern row of its own.

**Build steps**

1. Resolve RWB-PLT-N009-CON at major version 1 through the template pin and publish the manifest with the usage example paths (AC7).
2. Write the `ProblemDetailWriter` and the trace identifier binding, and prove the member set and the media type on both an error from a domain exception and an error from a message code (AC1).
3. Write the `ErrorMapLoader` and the map resource; prove the start-up failure on a code with no row and the absence of a default status (AC1, AC6).
4. Write the `DomainErrorMap` for the exception types a service raises, with no status and no text in it (AC1).
5. Write the `IdempotencyFilter` and prove the 400 of a missing, a blank and a non-UUID header, with the handler not invoked (AC2).
6. Write the `IdempotencyStoreAdapter` over the outbox library's guard and prove the replay of the first response, the 409 of a different endpoint or body and of an in-flight request, the 24-hour purge and the 503 of an unavailable store with the transaction rolled back (AC3, AC4, AC5).
7. Add the scan over the map, the log record and the examples for a business value and a personal value, and the no-local-copy check (AC6).
8. Wire both helpers into the service template, generate a service from it and prove that the generated build carries both and no local copy (AC7).
9. Publish the five usage examples and the contract test result, and hand the pinned version to the 19 service stories.

**Done when.** A service generated from the template answers every error in one problem detail shape, refuses a POST without a key, replays a stored response with no second effect, refuses a mismatched body with 409, answers an unavailable store with 503 and writes nothing in that case, and its contract test is green against the published artefact and red on a local error body, a local map and a local key table.

### 14. Validation and messages

MSG-PLT-N009-03, -05 and -06 are runtime answers and -04 is a log code only, with the English texts of Error and Message Standard v6 (Thai pending under DL10); MSG-PLT-N009-01, -02 and -07 are technical messages of the build, the start-up check and the test harness. A business message an officer reads belongs to the owning service.

| ID | When | Message | Result |
|---|---|---|---|
| MSG-PLT-N009-01 | A service writes its own error body or carries a local error map | Names the service, the class and the rule; never the value | The contract test fails the build |
| MSG-PLT-N009-02 | An error is raised for a message code with no map row | Names the code and the map version | The service does not start |
| MSG-PLT-N009-03 | A POST arrives with no `Idempotency-Key` header, with a blank value or with a non-UUID value | The Idempotency-Key header is required and must be valid for {operation}. | 400 with a problem detail, the handler is not invoked |
| MSG-PLT-N009-04 | The same key and request arrive again inside the window | The stored response for {operation} was replayed; no second action was taken. | Log only; the stored response is returned |
| MSG-PLT-N009-05 | The key is reused for a different endpoint or request, or the first request is still in flight | The Idempotency-Key conflicts with another request to {operation}. | 409 with a problem detail, the stored response unchanged |
| MSG-PLT-N009-06 | The idempotency store is unavailable or its read times out | The idempotency store for {operation} is unavailable. No changes were saved. Try again in a few minutes. | 503 with a problem detail, nothing written, the transaction rolled back |
| MSG-PLT-N009-07 | The map, the log record or an example carries a business value or a personal value | Names the field and the rule that failed, never the value | The scan fails the build |

Every runtime error a service answers through the helper is one RFC 9457 problem detail with `messageCode` and `traceId`, with no stack trace, no internal path and no personal data.

### 15. Screens and states

No screen of its own. The library has no user interface: the states it fixes are the stored-response states of section 9, and the only surface a person sees is the error a screen of one of the 19 services receives when a call fails — one problem detail with a message code and a trace identifier, with no stack trace, no internal path and no personal value. The public envelope and the route belong to RWB-PLT-N001-CON and the screens to the owning services.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N009-APP-01 | AC1 | Contract | A service generated from the template: an error from a domain exception and an error from a message code, each with the member set of BR1 and `application/problem+json`; the status and the type from the map row; the trace identifier of the request. |
| TC-PLT-N009-APP-02 | AC2 | Component | A POST with no header, a blank header, a non-UUID header and a UUID header; `MSG-PLT-N009-03`; 400 with a problem detail, the handler not invoked, nothing written, and the UUID request running once. |
| TC-PLT-N009-APP-03 | AC3 | Component | A first command stored in the throwaway schema and the same key and body replayed; the stored status and body returned, one row, one event; a body-less command. |
| TC-PLT-N009-APP-04 | AC4 | Component | A stored key and a second body that differs; 409 with a problem detail, no new row, the stored response unchanged; the same key on a second endpoint; `MSG-PLT-N009-05`. |
| TC-PLT-N009-APP-05 | AC5 | NFR | The `idempotency_key` table unreachable and its read timed out; 503 with a problem detail, no row written, no event published, the transaction rolled back, and the log record with no body and no header value |
| TC-PLT-N009-APP-06 | AC6, AC7 | Contract | The map, the log record and the five examples scanned for a business value and a personal value; the template-generated build carrying both helpers with no local copy, and the contract test red on a local error body, a local map and a local key table |
| TC-PLT-N009-APP-08 | AC8 | Contract | The rules BR1 to BR8 of section 8 each traced to one criterion and one test case of this story; a rule with no criterion or no test case fails the review |
| TC-PLT-N009-APP-07 | AC3 | Component | The `idempotency_key` table of the throwaway schema and a second schema holding a table of the same name; the write checked in the calling schema only, no other schema read, no table or column added (ASM-3438) |
| TC-PLT-N009-APP-09 | AC9 | Component | AC9 A second request in flight is refused and a row expires after 24 hours (new, RD-P1-001) |
| TC-PLT-N009-APP-10 | AC10 | Contract | AC10 Several failing inputs are listed in errors (new, RD-P1-004) |

No test in this story is an integration copy: the helpers are exercised against the contract fakes and a throwaway test schema, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in code or in the map: a threshold, a band, a limit, a rate, a date and a message text live in the owning service and the message catalogue, and the map holds codes, statuses and types only.
- No personal data in a stored response, a log record, a fixture or an example: identifiers, the operation, the status and the message code only.
- No stack trace, no internal path and no SQL in any error body, and no request body and no header value in any log.
- ACE data only through the owner's contract or a `v_ace_*` view read by the source-data service; the helper reads no ACE table.
- One trace context across REST, Kafka and Temporal in the W3C format, and the trace identifier on every problem detail.
- No cross-schema write: the stored response goes into the calling service's own `idempotency_key` table, under that service's own login.
- The helper is pinned by the template and never copied: a local error body, a local map or a local key table fails the contract test.
- A replayed POST publishes no second event and starts no second workflow: the stored response is returned before the handler runs.
- No credential, key or token is committed to the library, an example or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| N009 legacy trace | RFC 9457 problem and Idempotency-Key helpers | Change Register v1 N009 row | TC-PLT-N009-APP-01 … -06 |

No requirement identifier exists for N009: the Change Register creates the key as a new story with no legacy requirement row, and the standards it implements are the architecture standards named in section 8. The row above is the trace for the key itself.

| Story | Work type | Feature | L3 process | Relation to this story |
|---|---|---|---|---|
| RWB-PLT-N009-CON | Contract | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | H: publishes the two interfaces, the media type, the error map schema, the header and stored-response rules and the fakes this story implements |
| RWB-PLT-TE006-CON | Contract | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | H: the DDL contract of the `idempotency_key` table the stored response is written into, through the outbox library's guard |
| RWB-PLT-TE006-APP | App development | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | The outbox library whose guard the idempotency store adapter calls; it creates the table through the same template and owns the inbox and outbox behaviour beside it |
| RWB-PLT-N001-CON | Contract | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | The gateway-bff route contract whose error shape this story writes and whose envelope passes the owner's `messageCode` and detail through unchanged |
| RWB-PLT-NF02-APP | App development | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | The shared library baseline that publishes these helpers with the rest of the set and whose build carries the pin |
| The service stories of waves 1 to 4 | All work types | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N009-APP-2) | Consumers: each is generated from the template with both helpers and writes no local error body and no local key table |

### 19. Out of scope

- The contract itself — the interfaces, the member set, the media type, the map schema, the header and stored-response rules and the fakes: RWB-PLT-N009-CON.
- The DDL of the `idempotency_key`, outbox and inbox tables and the migration that applies it in a service schema: RWB-PLT-TE006-CON, RWB-PLT-TE006-APP and the per-service database stories.
- The gateway's own error translation and its public problem envelope: RWB-PLT-N001-CON and RWB-PLT-N001-APP.
- Any business message text and its Thai text: the owning services and DL10.
- The retention and purge of a stored response beyond the expiry window of the chart value: the service's own database story.
- The authorisation, masking and scope data a failed call may mention: the access owner (rwb-access) and the owning services.
- The logging and tracing instrumentation itself and the configuration loader: RWB-PLT-NF02-APP and the observability stories.
- The operations that carry the header and write the error body: each service's own contract and app stories.

### Remaining delivery steps

- Fix the package name, registry, version label and map path (GAP-1400) (platform library team).
- Publish the helpers and wire them into the service template; record the pinned version (service template owner).
- Size the story at refinement (squad).
- Add the new and changed TC-PLT-N009-APP assertions to Test Cases v9 and the RTM (QA lead).
