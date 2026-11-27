# RWB-PLT-N009-CON RFC 9457 problem and Idempotency-Key helpers - interface and fake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the shared Problem members and v6 message map, with the replay code log-only. Backfilled 7 mapped v9 test case IDs.
- `code` renamed to `messageCode`; `messageTh`, `field` and `errors` added; shared `Problem` schema (RD-P1-004; findings #1, #7; AC1, AC2, AC10).
- UUID header, 24-hour expiry, key scope, endpoint and request hash, replay, in-flight, store-down answers (RD-P1-001; #2 to #5; AC3, AC4, AC8, AC9).
- Runtime message IDs are MSG-PLT-N009-03, -04, -05, -06 in place of -13 and -14 (#6).
- Left pending: error-map source and path (GAP-1401, ASM-2438); endpoint longer than 100 characters (NEW-GAP-F08-8, #8).

**Change log.** D-RCV-60, 22 November 2026: new platform contract story for the RFC 9457 problem detail and Idempotency-Key helpers, their error map and their fakes, with no legacy story behind it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 3 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-N009-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (no size value in the source documents) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| Contract version | v1, Draft until the first consumer freezes it; `Problem` schema identical to the component of API Specification v7 |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004 |

### 1. Story

As a **tech lead**, I want **the published contract of two shared helpers — the RFC 9457 problem detail writer (members `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional); media type `application/problem+json`) with the error map from a domain exception to a status and a message code, and the `Idempotency-Key` helper (header rule on every POST, stored-response scope and key, same-key/same-result rule, mismatch rule, expiry rule) with their exceptions and fakes**, so that **all 19 services write one error shape and one repeat-safety rule from Day 1 and a consumer can be built and tested before the producer exists**.

This is the contract story of new platform key N009 under epic RWB-PLT-LIB. The Change Register reads "RFC 9457 problem and Idempotency-Key helpers - interface and fake" and creates the pair RWB-PLT-N009-CON and RWB-PLT-N009-APP; there is no legacy story, no legacy acceptance criterion and no legacy test case behind the key, so every criterion below is new and tests only the contract deliverable in the title.

What the contract fixes is stated by the target architecture and not by this story. Architecture v5 slide 11 puts RFC 9457 problem details on every error and an `Idempotency-Key` on every POST, with a 2 s timeout, GET retried once and no call chain deeper than one hop; slide 20 makes every service come from the service template and the shared libraries; slide 49 fixes OpenTelemetry with the W3C Trace Context as the one trace across REST, Kafka and Temporal.

The contract covers:

- The two published interfaces: the problem detail writer with its domain-exception to status and message code map, and the idempotency helper with its header rule, its scope and its stored-response rule.
- The error map as data: one table shipped with the library, one row per message code, holding the HTTP status and the problem `type`; service code never holds a literal.
- The body rule: no stack trace, no internal path, no SQL and no personal data in a problem detail, and the trace identifier as the W3C trace id of the request.
- The repeat rule: the header on every POST, the first stored response returned for a repeated key with no second effect, a repeat with a different request body refused with a 409 problem detail, and the expiry rule.
- The exceptions and the fakes: the refusal each case carries, and a fake of both helpers with an error-map fixture so a consumer is built and tested before the implementation exists.

The platform library is shared platform and not one of the 19 services: it has no service short name, so it owns no `rwb_*` schema, no topic, no REST base and no task queue of its own. The stored response and its scope live in the `idempotency_key` table, a library object owned by PLT and created in each service's own schema from the DDL contract published by RWB-PLT-TE006-CON (Ownership Map, `idempotency_key` row); this story defines the header, the scope and the semantics and creates no table. The problem schema is fixed by RD-P1-004 and the header format, stored-response scope and expiry by RD-P1-001; the table the error map is built from and its file path remain Not specified in the source documents (GAP-1401 item (a); ASM-2438).

### 2. Business rationale

One monolith had one exception handler, one error body and one place where a repeated command was recognised. The split gives every service its own repository, its own pipeline and its own squad, and an error body or a repeat rule written nineteen times drifts nineteen ways: a screen shows one shape from one owner and another shape from the next, an officer repeats a command after a timeout and the second submission posts a payment twice, and a support call cannot quote a trace identifier that one service writes and another omits.

This contract makes both rules a published artefact before either is code. The problem detail writer fixes one body with one member set, one media type and one trace identifier, and it takes its status and its `type` from a map shipped as data, so a new message code is a map row and not a code change in nineteen services. The idempotency helper fixes the header on every POST, the scope and the key of a stored response, the replay of the first answer and the refusal of a repeated key with a different body, so a retried submission has one effect.

Publishing it on Day 1 is what makes the wave 0 plan work. Every service CON story in waves 1 to 4 publishes an error set, and every one of them would otherwise negotiate a shape with the edge and with each other. A frozen interface and a fake let those stories, and the app story of this key, be built and tested before the implementation and before the producers of the calls they consume exist. It is the mechanism behind the guardrails every service inherits: no business value in code, no personal data in a log or an error body, and one repeat-safety rule everywhere.

The measure is narrow and testable: one error body shape across the 19 services, one row per message code in a data file, and zero second effects for a repeated key in the contract test of every consumer.

### 3. Preconditions

- The two rules are fixed by Architecture v5 slide 11: RFC 9457 problem details on every error, an `Idempotency-Key` on every POST, HTTPS/JSON with mesh mutual TLS, OpenAPI 3.1 with `/v1` in the path, a 2 s timeout, GET retried once with jitter, and no call chain deeper than one hop (ADR-020).
- Every service is built from the service template and the shared libraries (Architecture v5 slide 20), so a helper published once reaches all 19 services through the template and not through a local copy.
- The trace standard is fixed by Architecture v5 slides 11, 22 and 49: OpenTelemetry with the W3C Trace Context, one trace across REST, Kafka and Temporal, and the `traceparent` header on the event path; the `traceId` member of the problem detail is the W3C trace id of the request.
- The `idempotency_key` table is a library object owned by PLT and created in each service's own schema from the DDL contract of RWB-PLT-TE006-CON, with its unique key on the key and its endpoint, request-hash and stored-response columns (Ownership Map `idempotency_key` row; DP-09).
- The gateway route contract RWB-PLT-N001-CON fixes the public error envelope at the edge and the rule that the owner's message identifier and detail pass through unchanged, so this contract fixes the shape the owner writes and the edge carries.
- The message catalogue fixes the `MSG-` identifiers the error map is keyed by; the catalogue entry that owns a code, and the file path the map is built from, are Not specified in the source documents (GAP-1401; ASM-2438).
- The header value is a UUID in canonical 8-4-4-4-12 lower-case hexadecimal form, 36 characters, and a stored response is kept 24 hours from its first write (RD-P1-001; LDM DF-OPS-184 to DF-OPS-188).
- No approval is required to publish a Draft contract: the artefact is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests against it and its fake.

### 4. Flow

1. Fix the two interfaces in the contract artefact: the problem detail writer taking a domain exception or a message code with the request instance and the trace identifier, and the idempotency helper exposing the header name, the scope, the stored-response read and the stored-response write.
2. Fix the problem detail member set and the media type: `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional), no other member, and `application/problem+json` on every 4xx and 5xx answer (RFC 9457; RD-P1-004).
3. Write the error map as data: one row per `MSG-` identifier with its HTTP status, its problem `type`, its `title`, its `detail` and the service that owns the code, so a status or a `type` never appears in service code.
4. Fix the body rule: no stack trace, no internal path, no SQL, no personal data, the trace identifier as the W3C trace id, and a message code in `messageCode` that a support call can quote.
5. Fix the header rule: `Idempotency-Key` on every POST with a UUID value; a POST with no header, a blank value or a value that is not a UUID is refused with 400 `MSG-PLT-N009-03` before the handler runs. PUT, PATCH, GET and DELETE carry no `Idempotency-Key`.
6. Fix the stored-response rule: the first response (status, body and headers) is stored in the `idempotency_key` table of the caller's own schema with `idempotency_key` = the header value, `endpoint` = method plus resolved path and `request_hash` = SHA-256 of the raw request body (of the empty string when there is no body), and is kept 24 hours; the same key, endpoint and hash replays the stored status and body with no second effect; the same key with another endpoint or hash, or while the first request is still in flight, is refused with 409 `MSG-PLT-N009-05`; an unreachable store answers 503 `MSG-PLT-N009-06` and rolls back.
7. Fix the version rule and the contract test: major version 1, an additive change raises the minor number, a removed or retyped member or a changed media type or rule raises major version 2, and a published version is never edited in place.
8. Publish the fake of both helpers with the error-map fixture, the idempotency store fake and the event and edge route fake, and hand the pinned version to RWB-PLT-N009-APP and to every service CON story that publishes an error set.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A problem detail is written with a stack trace, an internal path, SQL or a personal value | The contract test fails the build and the body shape is not accepted | MSG-PLT-N009-11 | AC2 |
| X2 | An error is raised with a message code that has no error-map row | The build or the start-up check fails and names the code; no default status is invented | MSG-PLT-N009-12 | AC2 |
| X3 | A POST arrives with no `Idempotency-Key` header, with a blank value or with a value that is not a UUID | Refused with a 400 problem detail before the handler runs; nothing is read and nothing is written | MSG-PLT-N009-03 | AC3, AC8 |
| X4 | The same key arrives with a different endpoint or request body, or while the first request is still in flight | Refused with a 409 problem detail; the stored response is not overwritten and the second request has no effect | MSG-PLT-N009-05 | AC4, AC9 |
| X5 | The contract test finds a drift between the artefact, the error map and section 12 | The build fails and names the differing element; no service compiles against the drifted artefact | MSG-PLT-N009-15 | AC5 |
| X6 | The idempotency store is unavailable or its read times out | A 503 problem detail, nothing written and the caller's transaction rolled back | MSG-PLT-N009-06 | AC9 |
| X7 | A value no source names is needed (error-map source table and file path) | Published as the working read of the assumption with the gap open; it is never guessed into the contract text | Not specified in the source documents (GAP-1401; ASM-2438) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, an artefact, an error map and the fakes; it builds no runtime, reads no business data and needs no service to be finished |
| Negotiable | The file paths of the map are open until the contract freezes; the header format and the expiry window are fixed by RD-P1-001; the member set, the media type, the header name and the three repeat rules are fixed by the architecture |
| Valuable | Every service in waves 1 to 4 writes one error shape and one repeat rule from Day 1, and its CON story is built and tested against a fake before the implementation exists |
| Estimable | Two interfaces, one map schema, one header rule, one stored-response rule, one version rule and the fakes |
| Small | One sprint for the contract, the map and the fakes |
| Testable | Each criterion is a schema assertion, an artefact drift test, a store behaviour or a refusal in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the RFC 9457 problem detail and Idempotency-Key helper contract and its fakes

  Background:
    Given the platform library is published as one versioned contract artefact
    Given every service writes its errors and repeats its commands through the two helpers

  Scenario: AC1 The two interfaces and the media type are published and stable (new, D-RCV-60)
    Given the contract artefact of the platform library published with major version 1
    When a service compiles against it and writes an error
    Then the problem detail writer returns one body with the required members type, title, status, messageCode and traceId, the optional members detail, instance, messageTh, field and errors, and no other member
    Then the error map answers the HTTP status and the problem type for a message code, and the idempotency helper exposes the header name, the scope and the stored-response read and write
    Then the media type of every error answer is application/problem+json and no other error body shape is published
    Then no method of either interface opens a transaction, calls another service or writes a table

  Scenario: AC2 The error map is data and no error carries a stack trace, an internal path, SQL or personal data (new, D-RCV-60)
    Given the error map shipped with the library as a data file, one row per message code
    When an error is written for a message code
    Then the HTTP status and the problem type come from the map row for that code and never from a literal in service code
    Then a code with no map row fails the build or the start-up check, and no default status and no default type are invented
    Then the body carries the message code in messageCode, matching ^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$, and the 32-hex W3C trace identifier of the request in traceId
    Then no stack trace, no internal path, no SQL and no personal data appear in the body, in the detail or in the log record written beside it

  Scenario: AC3 The Idempotency-Key header is required on every POST and a stored response is replayed (new, D-RCV-60)
    Given a service that applies the helper with its own idempotency_key table
    When a POST arrives with no Idempotency-Key header or with a blank value
    Then the answer is 400 with messageCode MSG-PLT-N009-03 and the handler does not run, the transaction is not opened and nothing is written
    When a POST with key "3f0c9a52-7d1e-4c0b-9a1e-2b6f5d8c1a10" answers 201 and the same key arrives again on the same endpoint with the same request body inside 24 hours
    Then the stored 201 status and body are returned and the operation has no second effect and publishes no second event
    Then MSG-PLT-N009-04 appears in the log only and never in a body
    Then the stored response and its scope are read from the idempotency_key table whose DDL contract is published by RWB-PLT-TE006-CON, and the helper creates no table of its own
    Then the stored row holds idempotency_key, endpoint as method plus resolved path, request_hash as the SHA-256 of the raw body and response as status, headers and body

  Scenario: AC4 A repeat of the key with a different request body is refused with a 409 problem detail (new, D-RCV-60)
    Given a key already stored with its first endpoint, request body and response
    When the same key arrives with a different request body or on a different endpoint
    Then the answer is 409 with messageCode MSG-PLT-N009-05, and 422 is never answered for a key conflict
    Then the first stored response is not overwritten, no row is added and the handler does not run
    Then the refusal itself writes no row and leaves the stored response and its scope unchanged

  Scenario: AC5 The fake answers both helpers for a consuming service and the drift test fails its build (new, D-RCV-60)
    Given the published fake of the two helpers and the error-map fixture
    When a consuming service builds and tests against the fake
    Then the fake writes a problem detail for every error-map row, replays the stored response for a repeated key and refuses a repeated key with a different body with 409
    Then the fake answers an idempotency store that is unavailable, reads no table and calls no service
    Then the contract test of the consuming service runs against the published artefact and fails its build on any drift from section 12

  Scenario: AC6 The contract is versioned and a breaking change is a new major version (new, D-RCV-60)
    Given the published contract with major version 1
    When a member, the media type, the header rule or an error-map column changes
    Then an additive change with a default raises the minor version and keeps the member set, the media type and the header name
    Then a removed or retyped member, a changed media type or a changed repeat rule raises major version 2, and version 1 stays published and pinnable
    Then a service that has not moved its pin keeps the version it pinned, and no published version is edited in place

  Scenario: AC7 Each business rule BR1 to BR9 of section 8 is held by a criterion or a boundary test (new, D-RCV-60)
    Given the business rules BR1 to BR9 of section 8 and the published artefact of the library
    When the boundary test scans the artefact, the error map, the fake and the fixture
    Then the library holds no table, no column, no key, no topic, no REST base and no task queue, and no business or Thai message text, and the message code, status, type, title and detail come from the map only
    Then BR1 to BR6 are held by AC1 to AC4, BR8 by AC6, and BR7 and BR9 by this criterion, and a rule with no criterion or test row fails the boundary test

  Scenario: AC8 A key that is not a UUID is refused (new, RD-P1-001)
    Given a POST with Idempotency-Key "RET-2026-12-06"
    When the helper reads the header
    Then the answer is 400 with messageCode MSG-PLT-N009-03, the handler does not run and no row is written
    Given a PUT, a PATCH, a GET and a DELETE with no Idempotency-Key
    Then the helper does not refuse any of them and stores nothing

  Scenario: AC9 In flight, store down and expiry (new, RD-P1-001)
    Given a first POST with a key that is still in flight
    When a second POST with the same key arrives
    Then the answer is 409 with messageCode MSG-PLT-N009-05, and after the first completes the same request receives the replay
    Given the idempotency store is unreachable
    Then the answer is 503 with messageCode MSG-PLT-N009-06 and the caller's transaction is rolled back with nothing written
    Given a stored response first written more than 24 hours ago
    When the same key arrives again
    Then the request is treated as a first request and the handler runs
    Given a POST with no body, replayed with the same key on the same resolved path
    Then request_hash is the SHA-256 of the empty string and the stored response is replayed, and the same key on another resolved path answers 409 MSG-PLT-N009-05

  Scenario: AC10 A request with more than one failing input lists each one (new, RD-P1-004)
    Given a request body with two failing inputs
    When the writer answers 422 with messageCode MSG-GEN-001
    Then field names the first failing input and errors holds two rows of field, messageCode and detail
    Given a single failing input
    Then the body has no errors member
```

These criteria are new and test only the contract and the fake: N009 has no legacy story, no legacy acceptance criterion and no legacy test case, and every value quoted comes from Architecture v5 slides 11, 20, 22 and 49 and from the Ownership Map. The header format and the expiry window are those of RD-P1-001 and the problem schema is that of RD-P1-004; the table the error map is built from and its file path are Not specified in the source documents (GAP-1401; ASM-2438).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every error is one RFC 9457 problem detail with the members `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional), and the media type is `application/problem+json`; no service publishes another error body | Architecture v5 slide 11; RD-P1-004 |
| BR2 | The HTTP status and the problem `type` are read from the error map shipped as data, keyed by the message code; a literal status or type in service code is a defect, and a code with no row fails the build or the start-up check | Architecture v5 slide 11; ASM-2438 |
| BR3 | No stack trace, no internal path, no SQL and no personal data appear in a problem detail or in the log record written beside it, and the trace identifier is the W3C trace id of the request | Architecture v5 slides 11, 35 and 49 |
| BR4 | Every POST carries an `Idempotency-Key` with a UUID value; a POST with no header, a blank value or a value that is not a UUID is refused with 400 `MSG-PLT-N009-03` before the handler runs | Architecture v5 slide 11; RD-P1-001 |
| BR5 | The first response is stored against the key with its endpoint and request hash for 24 hours; the same key, endpoint and hash replays the stored status and body with no second effect; another endpoint or hash, or an in-flight first request, is refused with 409 `MSG-PLT-N009-05`; an unreachable store answers 503 `MSG-PLT-N009-06` | Architecture v5 slide 11; RD-P1-001 |
| BR6 | The stored response and its scope live in the `idempotency_key` table, a PLT-owned library object created in the caller's own schema from the DDL contract of RWB-PLT-TE006-CON; this contract creates no table, no column and no key of its own | Ownership Map `idempotency_key` row; RWB-PLT-TE006-CON |
| BR7 | The helper carries no business value and no business message text: the message code, its status, its type, its title and its detail come from the map built from the message catalogue, and the Thai text belongs to the owning service and DL10 | Architecture v5 slide 20; Template and Rules §R7.2 s17 |
| BR8 | The contract is versioned: major version 1 of the two interfaces, the member set and the rules; an additive change raises the minor number and a breaking change raises the major number, and a published version is never edited in place | Template and Rules §R8.2 |
| BR9 | The library owns no schema, no topic, no REST base and no task queue: it supplies the error writer and the filter that a consuming service applies to its own operations | Template and Rules §R4; Architecture v5 slide 20 |

### 9. State transitions

The contract itself has the lifecycle of a published version; the stored response of one key has the states below. Neither is a case status: no case, task or account state is held by this contract.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The two interfaces, the member set, the map schema and the rules are written | The working tree holds the artefact and the map fixture | In review |
| In review | The review closes | The no-PII and no-path scan and the map completeness check pass | Published |
| Published | Version 1 is frozen | The first consuming service passes its contract test against the fake | Frozen |
| Frozen | An additive change with a default | The minor number rises and every existing member is unchanged | Published |
| Frozen | A breaking change | A member, the media type, the header rule or a repeat rule changes | Deprecated, with version 2 published |
| Deprecated | The last consumer moves its pin | No consumer pins the old version | Retired |
| Stored response ABSENT | A POST with a UUID key succeeds | None | STORED, with the status, the body and the headers of that answer |
| Stored response STORED | The same key arrives on the same endpoint with the same request body | The stored response is no older than 24 hours | REPLAYED, no second effect |
| Stored response STORED | The same key arrives with a different endpoint or request body | None | REFUSED with 409, the stored response unchanged |
| Stored response STORED | 24 hours pass since the first write | A purge removes older rows | EXPIRED, and the next request with that key is treated as a first request |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the contract artefact, the error map schema, the rules and the fakes |
| The platform team | Owns the version rule, approves a breaking change and a freeze, and retires a version |
| The message-catalogue owner | Owns the message codes and their status, type, title and text; the library only reads the map built from the catalogue |
| The service teams of waves 1 to 4 | Read the contract, pin a version, consume the helper and raise a change request; they never fork the map or write a local error body |
| The security architecture reviewer | Confirms the no-personal-data, no-stack-trace and no-internal-path rule and the log rule beside it |
| RW-SECADM, security administrator | Confirms the header rule and the personal-data rule of the map and of the log record |
| RW-AUDIT, auditor | Reads the message code and the trace identifier a problem detail carries |
| No delegation of authority level applies | A contract artefact and a technical rule, not a credit decision |

No personal name, no email address and no credential appears in the artefact, in the map, in a fake or in an example. Where a party must be named, the contract uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Problem detail members | `type`, `title`, `status`, `messageCode` and `traceId` (required) and `detail`, `instance`, `messageTh`, `field` and `errors` (optional); `errors` is an array of `field`, `messageCode`, `detail`; media type `application/problem+json`; the owning service stamps `instance` (request path plus trace ID) and the edge passes `messageCode` and `detail` through (RD-P1-004) | None owned |
| Error map | One row per `MSG-` identifier: the code, the HTTP status, the problem `type`, the `title`, the `detail` and the owning service; shipped with the library as data | None owned |
| Error map source | The map is built from the message catalogue as a data file at the library resource root; the catalogue entry that owns a code is Not specified in the source documents (GAP-1401; ASM-2438) | None owned |
| `Idempotency-Key` header | Required on every POST; the name is case-insensitive and the value is a UUID in canonical 8-4-4-4-12 lower-case form, 36 characters (RD-P1-001) | DF-OPS-185 |
| Stored response | The status, the body and the headers of the first answer, with `endpoint` and `request_hash` | DF-OPS-186 to DF-OPS-188 |
| Scope | The service schema plus the key; the key is unique on its own inside the schema, so one key is never used on two endpoints (RD-P1-001; DF-OPS-185) | DF-OPS-185 |
| Expiry window | 24 hours from the first write; a chart value of the platform with default 24 h; a purge removes older rows (RD-P1-001) | None owned |
| Trace identifier | The W3C trace id of the request, in the W3C Trace Context format carried on REST, Kafka and Temporal (Architecture v5 slides 11, 22 and 49) | None owned |
| Business data | None. The contract publishes no threshold, band, limit, rate, date, amount or reference value | None owned |
| Personal data | None, in any record the helpers write: no name, no email address, no account number, no amount, no request body and no document content in a problem detail or a log record; `request_hash` is a hash and the stored `response` is the answer of the owning service. No field in this story is classed as personal data by this story | None owned |
| Tables owned | None. The stored response lives in `idempotency_key`, a PLT-owned library object whose DDL contract is published by RWB-PLT-TE006-CON and applied by each service in its own schema | None owned |
| Field identifiers | None owned. The problem detail members are RFC 9457 members, and the stored-response columns are fixed by RWB-PLT-TE006-CON | None owned |
| Contract version | Major version 1 of the two interfaces, the member set and the rules (BR8) | None owned |
| Open decisions | DL10 is still open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 apply | None owned |
| Library artefact | Package name, registry and version label are the baseline release of RWB-PLT-NF02-APP (GAP-1400) | None owned |

### 12. Contract

#### 12.1 REST operations provided

None — the library has no REST surface of its own. What the contract publishes is the error body every service writes and the request header rule every service's POST carries; the operations themselves belong to each service's own contract story and the public envelope to RWB-PLT-N001-CON.

#### 12.2 REST operations consumed

None at runtime — the helper joins the caller's own request and calls no service. The contract test of a consuming service reads the published artefact from the package registry and calls nothing else.

#### 12.3 Events published

None — the library owns no topic and publishes no event. A repeated POST that is replayed from a stored response publishes no second event, and the trace context of the first request travels on the headers of the event the consuming service publishes.

#### 12.4 Events consumed

None — the library consumes no event of its own; the idempotency rule applies to a command and not to an event, and the inbox rule for events belongs to RWB-PLT-TE006-CON.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity and starts none. A command that a workflow starts is started once, because the repeated POST is answered from the stored response before the caller's handler runs.

#### 12.6 Schedules

None — the contract owns no Schedule and names none.

#### 12.7 Tables owned

None — the library creates no table. The stored response and its scope live in the `idempotency_key` table, a PLT-owned library object whose DDL contract is published by RWB-PLT-TE006-CON and applied by each service in its own schema under its own login; this story defines the header, the scope and the semantics and creates no table.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Problem detail fake | The published member set and the `application/problem+json` media type, including a refusal of a stack trace, an internal path, SQL and a personal value | RWB-PLT-N009-APP and the contract test of every consuming service |
| Error-map fixture | One row per message code with its status, its `type`, its `title` and its `detail`, plus one code with no row and one refused row | The error-map test and the drift test of AC2 and AC5 |
| Idempotency store fake | A stored response per key with endpoint and request hash, a replay with the stored status, a 409 `MSG-PLT-N009-05` mismatch and in-flight answer, a 503 `MSG-PLT-N009-06` unavailable store and an expired row | RWB-PLT-N009-APP and the no-second-effect test of every consuming service |
| Event and edge route fake | The header set of an event and the public error envelope of RWB-PLT-N001-CON | The test that a replayed POST publishes no second event and that the edge carries the owner's `messageCode` and detail |

The event and edge route fake is a test asset only: the contract still publishes no event and no route of its own, and the fake answers with the owner's message code and detail unchanged.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The contract adds no path; it fixes the error body and the `Idempotency-Key` header of the operations each service publishes |
| Kafka | 0 | 0 | No topic and no consumer group; a replayed POST publishes no second event |
| Temporal | 0 | 0 | No workflow, no activity and no Schedule; a replayed command starts no second workflow |
| File | 0 | 0 | No file is read or written by the library |

The contract creates no service, no schema, no topic, no queue and no screen: it is one versioned contract artefact, one error map shipped as data and a set of fakes.

### 13. Solution plan

**Deliverables.** `problem-and-idempotency-contract.md` (the two interfaces, the member set, the media type, the error-map schema and the four repeat rules), `platform-api.jar` with the interfaces and the exception types, `error-map.json` as the shipped map schema with its fixture, the fake of both helpers, the error-map fixture, the idempotency store fake and the event and edge route fake, and the drift test.

**Problem detail (fixed by this contract).**

| Member | Meaning | Rule |
|---|---|---|
| `type` | The problem class, as an absolute URI | From the error-map row of the message code; never a path inside a service |
| `title` | A short, stable summary of that class | From the error-map row; the same text for the same code in every service |
| `status` | The HTTP status code | From the error-map row, and repeated in the response status |
| `detail` | The occurrence-specific message | Optional; the `detail` of the map row; no stack trace, no SQL, no internal path and no personal data |
| `instance` | The occurrence | Optional; the request path plus the trace identifier, stamped by the owning service |
| `messageCode` | The message code, a `MSG-` identifier | Required; pattern `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$`; the key the error-map row is stored under, so a support call can quote it |
| `traceId` | The W3C trace id of the request | Required; the 32-hex trace id of the W3C trace context, carried across REST, Kafka and Temporal |
| `messageTh` | The Thai text of the code | Optional; written only when a Thai text exists for the code (DL10 pending) |
| `field` | The first failing input | Optional; a JSON Pointer or a parameter or header name |
| `errors` | The failing inputs | Optional; only on 400 or 422 with more than one failing input; each row `field`, `messageCode`, `detail` |

The media type is `application/problem+json` on every error answer. The published schema is the `Problem` component above, identical in every service contract file; no other member is allowed (RD-P1-004). The platform rows of the error map include 400 `MSG-PLT-N009-03`, 409 `MSG-PLT-N009-05` and 503 `MSG-PLT-N009-06`.

**Error map (fixed by this contract).**

| Column | Rule |
|---|---|
| `code` | The `MSG-` identifier; the key of the map, one row per code, unique |
| `status` | The HTTP status of that code, one value per row, never computed in service code |
| `type` | The absolute URI of the problem class of that code |
| `title` | The summary of that class; stable across services |
| `detail` | The published text of that code, or the text pattern with its named fields |
| `owner` | The service that owns the code and its text, from the Ownership Map |
| `version` | The map version that row belongs to, so a consumer sees the map it pinned |

The map is data, shipped with the library and loaded at start-up: an error raised for a code with no row fails the build or the start-up check, and no default status and no default type are substituted. The catalogue entry that owns a code and the file path the map is built from are Not specified in the source documents (GAP-1401; ASM-2438).

**Idempotency rule (fixed by this contract).**

| Item | Rule |
|---|---|
| Header | `Idempotency-Key` on every POST; the name is case-insensitive and a POST with no header, a blank value or a non-UUID value is refused with 400 `MSG-PLT-N009-03` |
| Header format | A UUID in canonical 8-4-4-4-12 lower-case hexadecimal form, 36 characters |
| Scope | The service schema plus the key; the key is unique on its own, so a key used on a second endpoint is refused |
| Endpoint and hash | `endpoint` = method plus resolved path, for example `POST /admin/jobs/{jobId}/rerun` with the job ID filled in; `request_hash` = SHA-256 of the raw request body, of the empty string when there is no body. `endpoint` is varchar(100) (DF-OPS-186); the answer for a longer value is Pending: owner platform library owner, tracked as NEW-GAP-F08-8 |
| Stored response | The status, the body and the headers of the first answer, held against the key with its endpoint and request hash |
| Same key, same endpoint, same hash | The stored status and body are replayed (201 stays 201, 202 stays 202) with no second effect and no second event; `MSG-PLT-N009-04` is a log code only |
| Same key, different endpoint or hash | Refused with 409 `MSG-PLT-N009-05`; the stored response is not overwritten; 422 is never used for a key conflict |
| In flight | A second request while the first is in flight is refused with 409 `MSG-PLT-N009-05`; the caller retries and then receives the replay |
| Expiry | 24 hours from the first write (chart value, default 24 h); after expiry the same key is a first request |
| Store unavailable | A 503 `MSG-PLT-N009-06` problem detail, nothing written and the caller's transaction rolled back |
| Table | The `idempotency_key` table whose DDL contract is published by RWB-PLT-TE006-CON; this contract creates no table |

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| `ProblemDetails` | Published interface | Writes one problem detail from a domain error, or from a message code with the instance and the trace identifier |
| `ErrorMap` | Published interface | Answers the status, the type, the title and the detail of a message code, and refuses a code with no row |
| `IdempotencyKeys` | Published interface | Answers the header name, validates the header value and derives the endpoint and the request hash |
| `IdempotencyStore` | Published interface | Reads and writes the stored response against the key, and reports the store state |
| Contract document | Document | The member set, the media type, the map schema and the four repeat rules |
| ErrorMapFixture | Test asset | One row per code, one code with no row and one refused row, for the map test and the drift test |
| HelperFake and store fake | Test asset | Deterministic answers for both helpers, with the replay, the 409 mismatch and the unavailable store |
| Event and edge route fake | Test asset | The event headers and the public error envelope, for the no-second-effect and the pass-through test |

**Versioning rule.** Major version 1 covers the two interfaces, the member set, the media type, the map schema and the repeat rules together. An additive member with a default raises the minor number; a removed or retyped member, a changed media type, a changed header name or a changed repeat rule raises the major number; a wording fix raises the patch number. Version 1 is frozen at the first consumer and is never edited; the rename of `code` to `messageCode` and the added optional members of RD-P1-004 are made before that freeze, while version 1 is Draft.

**Pattern application.** None. N009 is a new platform key with no legacy marker, so no Template and Rules §R5.5 row is applied here: the two helpers are the shared mechanism the consuming stories apply, and this contract adds no dependency of its own. It is a CON story and starts on Day 1 by rule.

**Build steps**

1. Write the contract document with the two interfaces, the member set, the media type and the four repeat rules (AC1).
2. Generate `platform-api.jar` from the document and prove that the documented members and the generated types agree, and that no method opens a transaction (AC1).
3. Write the error-map schema and the fixture, and the scan that fails on a literal status or type in service code (AC2).
4. Write the body scan: a stack trace, an internal path, SQL or a personal value in a body or in the log record beside it fails the build (AC2).
5. Write the header rule and the stored-response rule, and the store-unavailable answer, against the interface only (AC3, AC4).
6. Build the two fakes and the event and edge route fake, with the replay, the 409 mismatch and the unavailable store (AC5).
7. Write the drift test and prove that a removed member, a retyped member, a changed media type, a changed header name and a changed rule each fail the build; publish version 2 in place of a breaking change (AC6).
8. Publish version 1, hand the pin to RWB-PLT-N009-APP and to the service CON stories that publish an error set, and record the version each consumer pins.

**Done when.** The artefact, the map fixture and the fakes carry one version; the scans and the drift test are green; the two stories that consume the contract answer every case of section 16 against the fakes; and the interface has not changed since it was handed to the consuming stories.

### 14. Validation and messages

The library raises no user-facing business message of its own. MSG-PLT-N009-03, -05 and -06 are the runtime answers and -04 the replay log code, with the texts of Error and Message Standard v6; MSG-PLT-N009-11, -12, -15 and -16 are contract messages of this story used by the build, the start-up check and the test harness, whose text is fixed by the library release note. They are not business messages: none names a customer, an account, a case or a business value.

| ID | When | Message | Result |
|---|---|---|---|
| MSG-PLT-N009-11 | A problem detail or the log record beside it carries a stack trace, an internal path, SQL or a personal value | Names the field and the rule that failed, never the value | The contract test fails and the shape is not accepted |
| MSG-PLT-N009-12 | An error is raised for a message code with no error-map row | Names the code and the map version | The build or the start-up check fails, with no default status and no default type |
| MSG-PLT-N009-03 | A POST arrives with no `Idempotency-Key` header, with a blank value or with a non-UUID value | The Idempotency-Key header is required and must be valid for {operation}. | 400 with a problem detail, the handler is not invoked |
| MSG-PLT-N009-04 | The same key and request arrive again inside the window | The stored response for {operation} was replayed; no second action was taken. | Log code only; the stored response is returned |
| MSG-PLT-N009-05 | The key is reused for a different endpoint or request, or the first request is still in flight | The Idempotency-Key conflicts with another request to {operation}. | 409 with a problem detail, the stored response unchanged |
| MSG-PLT-N009-06 | The idempotency store is unavailable or its read times out | The idempotency store for {operation} is unavailable. No changes were saved. Try again in a few minutes. | 503 with a problem detail, nothing written |
| MSG-PLT-N009-15 | The contract test finds a drift between the artefact, the error map and section 12 | Names the element that differs and the version | The build fails |
| MSG-PLT-N009-16 | A value no source names is needed (the error-map source table and file path) | Names the value and cites the gap and the assumption | Published as the working read, the gap stays open |

Every runtime error a consuming service writes through the contract is one RFC 9457 problem detail carrying the message code and the trace identifier, with no stack trace and no internal path. A business message that an officer reads is the owning service's own message and its Thai text follows DL10; neither is carried by this contract.

### 15. Screens and states

None in this story: the contract publishes no screen, no route and no state of its own, and the platform library has no user interface. What it fixes for the screens of the 19 services is only what a screen receives when a call fails — one problem detail with a message code and a trace identifier that a support call can quote — and the rule that no screen error reveals a stack trace, an internal path or a personal value. The screens themselves belong to the owning services and the public error envelope to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N009-CON-01 | AC1 | Contract | A sample service compiles against the artefact; the member set of BR1 and the media type `application/problem+json` asserted; the two interfaces carry no transaction and no service call. |
| TC-PLT-N009-CON-02 | AC2 | Contract | The error-map fixture: one code with a row, one code with no row; a literal status in service code fails the build; a body and a log record scanned for a stack trace, an internal path, SQL and a personal value |
| TC-PLT-N009-CON-03 | AC3 | Component | A POST with no header, a blank header and a well-formed header; the first response stored; the same key and body replayed with no second effect; the table is the `idempotency_key` of RWB-PLT-TE006-CON and no table is created. |
| TC-PLT-N009-CON-04 | AC4 | Component | A stored key with a first body and a second body that differs; 409 with a problem detail; the stored response and its scope unchanged, also for a second endpoint. |
| TC-PLT-N009-CON-05 | AC5, AC6 | Contract | The fake on every error-map row, on the replay, on the 409 mismatch and on the unavailable store; a removed member, a retyped member, a changed media type, a changed header name and a changed rule each fail the drift test; version 2 published in place of a breaking change |
| TC-PLT-N009-CON-06 | AC7 | Contract | Boundary test: scan the artefact, the error map, the fake and the fixture for a table, column, key, topic, REST base, task queue, business or Thai message text, and trace BR1 to BR9 to a criterion; test method Not specified in the source documents (NEWAC-RWB-PLT-N009-CON-AC7) |
| TC-PLT-N009-CON-07 | AC8 | Component | AC8 A key that is not a UUID is refused (new, RD-P1-001) |
| TC-PLT-N009-CON-08 | AC9 | Component | AC9 In flight, store down and expiry (new, RD-P1-001) |
| TC-PLT-N009-CON-09 | AC10 | Contract | AC10 A request with more than one failing input lists each one (new, RD-P1-004) |

No test in this story is an integration copy: the contract is exercised against its own fakes and a sample service, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business value in the contract: a threshold, a band, a limit, a rate, a date and a reference value live in the owning service, a parameter or the message catalogue, never in the library or the error map.
- No personal data in a problem detail, a log record, a fixture or an example: the message code, the identifiers, the status and the trace identifier only.
- No stack trace, no internal path and no SQL in any error body: a build scan fails on all three.
- ACE data only through the owner's contract or a `v_ace_*` view read by the source-data service; the library reads no database at all.
- One trace context across REST, Kafka and Temporal in the W3C format, and the trace identifier on every problem detail.
- The map is data: a status or a `type` in service code is a defect, and a code with no row fails the build.
- A published version is never edited in place; a breaking change raises a major version and keeps the old one pinnable.
- The library creates no service, schema, table, topic, queue, schedule or screen, and it writes no row of its own.
- The header value is never logged and a request body is never logged with it: the scope, the key and the outcome are enough to diagnose a repeat.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| N009 legacy trace | RFC 9457 problem and Idempotency-Key helpers | Change Register v1 N009 row | TC-PLT-N009-CON-01 … -05 |

No requirement identifier exists for N009: the Change Register creates the key as a new story with no legacy requirement row, and the standards it implements are the architecture standards named in section 8. The row above is the trace for the key itself.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N009-APP | App development | H: implements the two helpers, the map and the fakes this contract publishes |
| RWB-PLT-TE006-CON | Contract | The DDL contract of the `idempotency_key` table the stored response lives in, and of the outbox and inbox tables beside it |
| RWB-PLT-N001-CON | Contract | The gateway-bff route contract whose error shape this contract fixes and whose envelope passes the owner's `messageCode` and detail through unchanged |
| RWB-PLT-NF02-APP | App development | The shared library baseline whose error handling and configuration areas publish these helpers with the rest of the baseline |
| The 19 services (rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-payment, rwb-reporting, rwb-agent, rwb-valuation, rwb-treatment, rwb-guarantee, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-deviation, rwb-partner) | All work types | Consumers: each writes its errors and repeats its commands through the pinned contract and its fake |

### 19. Out of scope

- The implementation of the two helpers, the error map loading, the filter and the template wiring: RWB-PLT-N009-APP.
- The outbox, inbox and idempotency tables and their DDL: RWB-PLT-TE006-APP, RWB-PLT-TE006-CON and the per-service database stories that apply the template in each service's own schema.
- The gateway's own error translation, its problem envelope and its pass-through of the owner's `messageCode` and detail: RWB-PLT-N001-CON and RWB-PLT-N001-APP.
- The message catalogue, the status and text of each code, and the Thai text of every message: the owning services and DL10.
- The operations that carry the header and write the error body: each service's own contract and app stories.
- The authorisation, masking and scope data a failed call may mention: the access owner (rwb-access) and the owning services.
- The trace instrumentation itself, the log record shape and the configuration loader: RWB-PLT-NF02-APP and the observability stories.

### Remaining delivery steps

- Publish version 1 of the artefact, the fakes and the error-map fixture and record the pinned version (platform team).
- Close the error-map source part of GAP-1401 and NEW-GAP-F08-8 (platform library owner).
- Size the story at refinement (squad).
- Add the new and changed TC-PLT-N009-CON assertions to Test Cases v9 and the RTM (QA lead).
