# RWB-PLT-N001-CON gateway-bff route contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned masked customer and account calls, shared Problem pass-through and gateway-owned errors. Backfilled 4 mapped v9 test case IDs. RD-P1-060, RD-P1-063.
- Cited the Test Cases v9 row TC-PLT-N001-CON-11 for AC2.
- Shared problem schema and pass-through of `messageCode`, `detail` and the other members; edge-written problems carry message codes (RD-P1-004; findings #2, #3; AC4, AC10).
- `ETag` and `If-Match` pass through unchanged (RD-P1-006; #5; BR14, AC9).
- Sixth consumed event `rwb.source-data.AceDataLate.v1` for the late-data banner (RD-P1-003, RD-P1-040; #4; AC5).
- Contract and fake versions pinned (#6, #7).
- Left pending: banner route and clearing rule (GAP-3313), message code of the edge 500 (GAP-3312).

| Item | Value |
|---|---|
| Story key | RWB-PLT-N001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EDGE |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N001 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; no size is set in this document |
| Contract version | v1 of the public route surface and consumed event schemas (BR9); problem schema of API Specification v7 (gateway-bff.yaml 5.1.0); downstream rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0 (provider fake version 5.1.0) |
| Composite screen route | GET /api/recovery/cases/{id} (case screen): gateway-bff checks the Redis session and coarse permission, calls rwb-case GET /v1/cases/{id} and rwb-source-data GET /v1/customers/{personKey} and GET /v1/accounts/{accountKey} in parallel, and merges the answers into the screen model; 1.2 s composition budget against the 2 s target per downstream. The customer and account operations are published by RWB-P1-E1069-APP in rwb-source-data.yaml 5.1.0; the composite uses policy-masked values (RD-P1-060) |
| Notice operations edge check | Not specified in the source documents (GAP-1083) |
| Field app route | Not specified in the source documents (GAP-0951) |
| Documents tab route (SCR-30) | Not specified in the source documents (GAP-1035) |
| Screen tab, inbox and payment-tab routes | Not specified in the source documents (GAP-1393); route document, inbox push transport and payment-tab operation to be confirmed at the edge contract review |
| Depends on (build) | None |
| Contract dependencies | None to start (Day 1); the P1 shapes behind the case screen and the banner are pinned from RWB-P1-E1069-APP (account read) and RWB-P1-E1015-CON (AceDataLate) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-011, RD-P1-040, RD-P1-044, RD-P1-060, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: new platform contract story for the gateway-bff public route surface and its consumed events, published Day 1 with a fake. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 157 cross-document, 19 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the gateway-bff route contract**, I want **the public route surface of the edge, its error mapping and its consumed event schemas published on Day 1 as OpenAPI 3.1 and AsyncAPI 3.0 documents with a working route fake**, so that **the gateway implementation, the ACE front end and every owner service can build and test against one frozen set of paths, models and failure codes before the gateway exists**.

This is the contract story of new platform key N001 under epic RWB-PLT-EDGE. It publishes, as the shared platform entry of the Recovery Workbench:

- The OpenAPI 3.1 document of the gateway-bff public route surface, under `/api/recovery` with no service segment and no `/v1` (Architecture v5 slides 10 and 20): the case screen, the four screen tabs, the officer task list and the inbox stream.
- The AsyncAPI 3.0 document of the six events the gateway consumes: the two that push to the officer inbox, the three that refresh the permission cache and the late-load event `rwb.source-data.AceDataLate.v1` behind the data banner.
- The route table of section 12.1: public path, downstream operation, downstream owner, merge rule and response codes.
- The error-mapping table of section 14: RFC 9457 problem details, and the rule that the owner's `messageCode` passes through unchanged.
- A route fake that answers the seven public routes with the examples of this document, and a contract test that fails the build when a route, a model or a code drifts.

The gateway is shared platform, not one of the 19 services: it owns no schema, no topic and no task queue, its routes carry no service segment and no `/v1`, and it never chains calls. The seven downstream operations are owned by rwb-case (P3), rwb-source-data (P1), rwb-document (P5), rwb-comms (P6), rwb-payment (P8) and rwb-litigation (S4), and those owners are taken from the Ownership Map only. This story builds nothing that reads or writes business data; it has no build dependency and starts on Day 1. The contact panel of a party (consent state and verification of contact points) is served through a gateway-bff composite route published here; its screen identifier, field list and masking are not specified in the source documents (GAP-2379) and are left to the case record view story and the edge contract. SCR-33 Template approval stays with the template stories of the same service. The gateway-bff composite route list is the route list of this contract, and the service template reads that list and adds no route of its own. The per-service module map file is not specified in the source documents (GAP-1430).

### 2. Business rationale

The monolith served the case screen from one process, so the screen, the case data and the customer data could be read in one transaction and nobody had to agree a failure code. In the target the browser reaches the gateway over the shared App Gateway, and the gateway asks each owner once, in parallel, with a 2 s timeout and a breaker per downstream (DP-19, DP-11). Nothing in that path can wait for the six owner services to be built: the front end, the gateway and the six owner contract tests need the route surface, the screen model and the 401, 403, 404 and 503 codes on Day 1.

The contract also fixes the two boundaries the realignment depends on. First, the edge holds sessions only: an opaque cookie, a 15-minute idle timeout, the session record in Redis and a short-lived user JWT from ACE Common sign-in, with no business data at the edge. Second, object-level authorisation stays inside the owner service (OWASP API1), which uses cached permission data from rwb-access; the edge checks a coarse permission and then trusts the owner's answer. Writing both down before the code is what keeps REQ-OCC-007, NFR-008 and NFR-009 defensible after the split: one screen, one hop per owner, under 2 seconds even with 50 documents.

### 3. Preconditions

- The edge placement is fixed by Architecture v5: the shared Azure App Gateway with WAF routes `/` and `/api/*` to ACE and `/recovery/*` and `/api/recovery/*` to the Recovery gateway-bff (slide 8).
- The agent monitoring dashboard v2 read and override panel route is registered under RWB-PLT-N001-CON. Its path is specified by the edge story, not by this story. Login, alert thresholds, topology, Schedule path and consumer group are owned by the dashboard story (GAP-0631).
- The gateway is shared platform, not a service: it has no row in the Ownership Map, no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `rwb-<short>` task queue. Its own owner in section 12 is PLT; every downstream owner is taken from the Ownership Map. gateway-bff is owned by PLT under epic RWB-PLT-EDGE. The partner gateway (FAPI 2.0, in the DMZ) is part of the same edge: its owner is PLT under epic RWB-PLT-EDGE, and, as for gateway-bff, it has no Ownership Map code, wave, schema, topic or task queue.
- The naming rule of Template and Rules §R4 applies to the services behind the edge, not to the edge: a public path is `/api/recovery/...` with no service segment and no `/v1`, and no document repeats the monolith base (DP-13).
- The session rules are fixed: an opaque session cookie, 15 minutes idle, the session record in Redis and no business data there; a short-lived user JWT is obtained per request through ACE Common sign-in (slide 20).
- The resilience rules are fixed: 2 s timeout per downstream, a circuit breaker per downstream, and a GET retried once with jitter (slide 10).
- The REST contract rule is fixed: OpenAPI 3.1, one hop, depth 1 only, RFC 9457 problem details and an `Idempotency-Key` on every POST (slide 11). The v1 route surface publishes GET only.
- The event consumers are fixed by the event catalogue: ApprovalRequested (row 09) and TimerBreached (row 19) drive the officer inbox push; AccessPolicyChanged, DoaLimitChanged (rwb-access) and RulePackageInForce (row 30) drive the cache refresh (slide 20). `rwb.source-data.AceDataLate.v1` (EV-27) on `rwb.source-data.events.v1` drives the gateway-bff late-data banner (Kafka Topic and Event Catalog v3; RD-P1-003, RD-P1-040).
- No approval is required to publish a Draft contract: the surface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document for the seven public routes, one tag per screen area: Case screen, Documents, Notices, Payments, Legal, My work, Inbox.
2. The author writes the AsyncAPI 3.0 document for the six consumed events, with channel, CloudEvents 1.0 headers, key and payload schema.
3. The author writes the route table and the error-mapping table into sections 12 and 14, and generates the document paths from them, so the table, the document and the fake cannot drift.
4. The lint and schema steps run: OpenAPI 3.1 validation, no service segment and no `/v1` in a public path, one problem envelope, a 401, 403, 404 and 503 on every route that has a downstream, a depth-of-1 assertion that every downstream operation belongs to an owner service and calls no further service, and an AsyncAPI 3.0 validation with CloudEvents 1.0 headers.
5. A personal-data scan runs over every example: no name, no email address, no account number, no national identifier; customer and account rows appear as identifiers and codes only.
6. The route fake is generated from the documents; it answers the seven routes, including the 401, 403, 404 and 503 examples and the degraded-tab example of section 14.
7. The documents and the fake are published to the contract registry; RWB-PLT-N001-APP and the ACE front end pin the version.
8. The contract test runs the fake against the documents on every change; a breaking change raises a new version and marks v1 deprecated rather than editing v1 in place.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A public route is published without the 401, 403, 404 and 503 responses | The lint step fails the build and the document is not published | Lint finding, no message id | AC4 |
| X2 | A public route declares a chain, that is a downstream operation that calls another service | The depth-of-1 step fails the build; the route must be split or the call moved into the owner | Lint finding, no message id | AC1 |
| X3 | A public path carries a service segment or `/v1`, or repeats the monolith base | The lint step fails the build; the edge publishes `/api/recovery/...` only | Lint finding, no message id | AC1 |
| X4 | An example carries a customer name, an email address, an account number or a national identifier | The scan rejects the example; identifiers and codes only | Review finding | AC5 |
| X5 | A consumed event schema adds a field holding personal data | The schema review rejects the change; the payload keeps identifiers and facts | Review finding | AC5 |
| X6 | A value the consumers need is named by no source (the tab paths, the push transport, the payment-tab operation) | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1393; ASM-2429) | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds nothing, reads no business data, depends on nothing |
| Negotiable | Path shape below `/api/recovery`, model field order, example values and the push transport are open until the version is frozen |
| Valuable | The gateway implementation, the ACE front end and the six owner contract tests start on Day 1 against the fake |
| Estimable | Seven public routes, six consumed events, one route fake, one contract test |
| Small | One sprint for the documents, the fake and the lint rules |
| Testable | Each criterion is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: gateway-bff public route surface, error mapping and consumed events

  Background:
    Given the gateway-bff public base is /api/recovery with no service segment and no /v1
    Given the edge is shared platform and owns no schema, no topic and no task queue

  Scenario: AC1 The route document is published and every route is one hop with a named downstream owner (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the public route surface
    When it is validated and linted
    Then it declares GET /api/recovery/cases/{caseId}, GET /api/recovery/cases/{caseId}/documents, GET /api/recovery/cases/{caseId}/notices, GET /api/recovery/cases/{caseId}/payments, GET /api/recovery/cases/{caseId}/legal-actions, GET /api/recovery/me/tasks and GET /api/recovery/inbox/stream
    Then every route names one downstream operation, one downstream owner code from the Ownership Map, and exactly one hop with no chain
    Then no public path carries a service segment or a /v1 segment, and no document repeats the monolith base

  Scenario: AC2 The case screen route declares the parallel calls, the merge rule and the p95 budget (new, D-RCV-60)
    Given the case screen route on /api/recovery/cases/{caseId}
    When the route table and the document are read together
    Then the route declares rwb-case GET /cases/{caseId} and rwb-source-data GET /customers/{personKey} and /accounts/{accountKey} as parallel calls with a 2 s timeout each
    Then the merge rule states that the case answer supplies the customer and account references and that the screen model carries case, stage, tasks and timers beside the customer and the account
    Then the budget is published as 0.15 s gateway and session plus 0.6 s slowest parallel call plus 0.3 s merge, about 1.2 s budgeted, inside the 2 s target
    Then if either parallel call fails, the route returns the AC4 problem for that failure and no partial screen model is returned; the owner's identifier passes through unchanged

  Scenario: AC3 The session and authorisation rules at the edge are published (new, D-RCV-60)
    Given the security section of the document and the route table
    When the rules are reviewed
    Then the browser presents an opaque session cookie and the gateway resolves the session in Redis with a 15-minute idle timeout
    Then the gateway obtains a short-lived user JWT per request through ACE Common sign-in and never exposes it to the browser
    Then the edge checks a coarse permission only, and object-level authorisation stays with the owner service, which uses cached permission data from rwb-access
    Then no business data is stored at the edge and the session record holds identifiers and role codes only

  Scenario: AC4 The error mapping is published (new, D-RCV-60)
    Given the problem schema used by every public route
    When the error examples are validated
    Then every error is application/problem+json with type, title, status, messageCode and traceId required, detail, instance, messageTh, field and errors optional, and no other member
    Then the map declares 401 when no session exists or it has expired, 403 when the coarse check refuses, 404 when the owner answers not found, and 503 when a downstream exceeds 2 s or its breaker is open
    Then the owner's status, messageCode and detail pass through unchanged together with every other member of the owner's problem, including its 400, 409, 422 and 428 answers, and no error carries business values or personal data
    Then a problem the edge writes itself carries messageCode MSG-P4-001 on 401, MSG-P4-002 on 403, MSG-GEN-001 on a malformed path or query value and MSG-GEN-006 on a downstream timeout or open breaker

  Scenario: AC5 The consumed event schemas are published in AsyncAPI 3.0 (new, D-RCV-60)
    Given the AsyncAPI 3.0 document for the six consumed events
    When it is validated
    Then it declares ApprovalRequested and TimerBreached on their producer topics as the officer inbox push, and AccessPolicyChanged, DoaLimitChanged and RulePackageInForce as the cache refresh
    Then it declares rwb.source-data.AceDataLate.v1 on rwb.source-data.events.v1 with record key {sourceSystem}:{businessDate}, ce_subject sourceSystem and the data fields sourceSystem (string, at most 10), businessDate (date), status (string) and completedAt (date-time, nullable)
    Then every message is CloudEvents 1.0, keyed by the case id, the policy identifier or, for AceDataLate, {sourceSystem}:{businessDate}, with a payload of identifiers and facts only
    Then no payload schema carries a name, an email address or an account number

  Scenario: AC6 The route table, the fake and the contract test agree, and a breaking change raises a new version (new, D-RCV-60)
    Given the route table, the error map and the published documents
    When the contract test and the fake are run
    Then the fake answers all seven routes, including the 401, 403, 404 and 503 examples and the degraded-tab example
    Then the routes, the models and the codes in the table equal those in the documents and in the fake
    Then a breaking change raises v2 and marks v1 deprecated, and no consumer sees an edited v1

  Scenario: AC7 Every business rule BR1 to BR9 in section 8 has a named criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8
    When each rule is traced to its criterion in section 7 and its test case in section 16
    Then every rule BR1 to BR9 names at least one criterion and one test case, and each named criterion exists in section 7
    Then the architecture-constraint rules are checked by the contract test of their criterion, and no rule is left without a test

  Scenario: AC8 A status change the owner's model does not allow is refused and changes nothing (new, D-RCV-60)
    Given the v1 route surface publishes GET only, so no status change is exposed (BR7)
    When a status change the owner's model does not allow is sent to a case route
    Then the request is refused with the AC4 problem and the case state is unchanged
    Then the refusal carries no business values or personal data

  Scenario: AC9 The edge passes ETag and If-Match through unchanged (new, RD-P1-006)
    Given the route fake answers a pass-through route with the owner header ETag "3"
    When the caller reads the route
    Then the response carries ETag "3" unchanged
    Given a PUT or PATCH route is added by a later version of this contract
    When a request carries If-Match "3"
    Then the owner receives If-Match "3" unchanged, and its 428 or 409 problem with messageCode MSG-GEN-004 and its new ETag on success pass back unchanged

  Scenario: AC10 A problem with several failing inputs passes through whole (new, RD-P1-004)
    Given an owner fake answers 422 with messageCode MSG-GEN-001, field, two errors rows, messageTh and traceId
    When the caller reads the route
    Then the response is 422 application/problem+json with every member byte-equal to the owner's answer and no member added or removed
```

These criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every value in the examples comes from Architecture v5 or the Ownership Map, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every public route is one hop to one owner service; the gateway never calls a service that then calls another | Architecture v5 slides 10 and 20 | AC1, TC-PLT-N001-CON-01 |
| BR2 | A composite screen asks its owners in parallel, and only for what is on screen; other tabs load on click | Architecture v5 slide 10 | AC2, TC-PLT-N001-CON-02 |
| BR3 | A session is an opaque cookie, 15 minutes idle, resolved in Redis; no business data is stored at the edge | Architecture v5 slide 20 | AC3, TC-PLT-N001-CON-03 |
| BR4 | The edge checks a coarse permission; object-level authorisation stays with the owner service | Architecture v5 slides 10 and 35 | AC3, TC-PLT-N001-CON-03 |
| BR5 | Every downstream call has a 2 s timeout and a breaker per downstream; a GET is retried once with jitter | Architecture v5 slide 10 | AC2 and AC4, TC-PLT-N001-CON-02 and TC-PLT-N001-CON-04 |
| BR6 | Every error is RFC 9457 problem details, and the owner's `messageCode`, `detail` and other problem members pass through unchanged | Architecture v5 slide 11 | AC4 and AC10, TC-PLT-N001-CON-04 (AC10: TC-PLT-N001-CON-04, TC-PLT-N001-CON-10) |
| BR7 | Every POST carries an `Idempotency-Key`; the v1 route surface publishes GET only, so no POST is exposed yet | Architecture v5 slide 11 | AC1, TC-PLT-N001-CON-01 |
| BR8 | A public path is `/api/recovery/...` with no service segment and no `/v1`; the monolith base is never republished | DP-13; Architecture v5 slides 10 and 20 | AC1, TC-PLT-N001-CON-01 |
| BR9 | A breaking change raises a new version and deprecates v1; v1 is never edited in place | Template and Rules §R7.2 | AC6, TC-PLT-N001-CON-06 |
| BR10 | SCR-17 Guarantee claim is served as a gateway-bff composite route over this contract and the case contract; its owner and route are recorded in the edge catalogue | DP-19; FSD S3 Screens | AC2, TC-PLT-N001-CON-02 |
| BR11 | SCR-20 shows the deferred state DEFERRAL_RECORDED beside the four legacy states, with the recorded reason, review date and rule version; its field list is Not specified in the source documents (GAP-2832) | R-LIT-55; DP-19; TSD S4 T6.1 | Not specified in the source documents (GAP-2832) |
| BR12 | SCR-22 shows the eviction state of the asset, EVICTION_REQUIRED, raised by R-DIS-13 against a held asset; its on-screen presentation is Not specified in the source documents (GAP-2891) | Business Rules v4 R-DIS-13; TSD S5 v2 T3.2 | Not specified in the source documents (GAP-2891) |
| BR13 | SCR-22 shows the holding state from LOV-HOLDING and the case state beside it; take-on reads as ASSET_ON_BOOKS and ASSET_HELD; the legacy wording stays the business description | TSD S5 T3.2; Business Rules v4 R-DIS-54 | Not specified in the source documents (GAP-2952) |
| BR14 | `ETag` on a read and `If-Match` on a PUT or PATCH pass through the edge unchanged; the edge never creates, checks or strips either header | RD-P1-006 | AC9, TC-PLT-N001-CON-09 |

### 9. State transitions

None in this story: a document has no runtime state. This story fixes the vocabulary and the HTTP result that the app story implements:

| Object | State | HTTP result of the route |
|---|---|---|
| Session | ABSENT | 401 with the sign-in entry point |
| Session | AUTHENTICATED | 200, and every request refreshes the 15-minute idle |
| Session | IDLE_EXPIRED | 401, and the browser is sent to sign-in |
| Session | SIGNED_OUT | 401, and the session record is gone from Redis |
| Permission cache | FRESH | The coarse check is answered from memory |
| Permission cache | STALE | The coarse check is answered from the last good copy while the refresh runs |
| Permission cache | REFRESHED | The new policy, DoA limit or rule package version is in force |

The state machine itself, its timers and its metrics are specified in RWB-PLT-N001-APP section 9.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents, the route table, the error map and the fake |
| The platform owner of the edge | Approves a breaking change and a version freeze |
| The owner services of the seven downstream operations (P3, P1, P5, P6, P8, S4) | Read the route table, confirm the operation they serve, raise a change request |
| The ACE Common team | Owns the sign-in, the short-lived user JWT and the audit path the document references and never republishes |
| The front-end team of the ACE workbench | Consumes the screen model, pins the version, raises a change request |
| No delegation of authority level applies | A route contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document or an example. Where a caller or a grantee must be named, the example uses a user identifier or a role code only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes route paths, model shapes, codes and status codes; no customer, account, case or document value appears | None |
| Data held at the edge | The session record only: session identifier, user identifier, role codes, issued at, last seen and idle expiry (RWB-PLT-N001-APP section 11) | None |
| Data held in Redis | Sessions only, provisioned by RWB-PLT-N006-INF; no business data, no cached customer or case row | None |
| Screen model | Assembled per request from the owner answers; the model field list is fixed in RWB-PLT-N001-APP section 11 | None |
| Personal data in examples | None. Customers and accounts appear as identifiers, queues as queue codes, people as user identifiers | None |
| Field identifiers | None owned. Every field shown on a screen belongs to the contract of the owner service that publishes it | None |
| Retention at the edge | None. The session record expires with the session; the document itself keeps no data | None |
| Masking rule for customer fields on the SCR-02 and SCR-03 composite | Not specified in the source documents (GAP-0674) | None |
| Composite route of the SCR-45 screen (path, merge rules, per-call timeout ownership) | Not specified in the source documents (GAP-0728) | None |
| Plan-status composite route of the case record (SCR-03 plan section) | Path: Not specified in the source documents (GAP-0773). Merge rule: the live answer of rwb-integration wins; when it is missing or not live, the stored answer of rwb-case is shown with MSG-P2-008. Masking rule and 2 s budget split: Not specified in the source documents (GAP-0773) | None |
| Other-products panel composite route (path and merge order) | Not specified in the source documents (GAP-0390) | None |

### 12. Contract

**12.1 REST operations provided**

| Operation | Downstream operation | Downstream owner | Merge rule | Responses | Owner |
|---|---|---|---|---|---|
| GET /api/recovery/cases/{caseId} | rwb-case GET /api/recovery/case/v1/cases/{caseId}, and rwb-source-data GET /api/recovery/source-data/v1/customers/{personKey} and GET /api/recovery/source-data/v1/accounts/{accountKey} | P3, P1 | Composite: the two reads run in parallel with a 2 s timeout each; the case answer supplies the customer and the account references, and the merge puts case, stage, tasks and timers beside the customer and the account on one screen model | 200 CaseScreen; 401; 403; 404; 503 | PLT |
| GET /api/recovery/cases/{caseId}/documents | rwb-document GET /api/recovery/document/v1/cases/{caseId}/documents | P5 | Pass-through: the tab model is the owner's page unchanged, and no field is added at the edge | 200 DocumentTabPage; 401; 403; 404; 503 | PLT |
| GET /api/recovery/cases/{caseId}/notices | rwb-comms GET /api/recovery/comms/v1/notices/{noticeId} | P6 | Pass-through, one owner answer per tab; the Ownership Map names GET /notices/{noticeId} and the case-scoped list path is the working read of the assumption below | 200 NoticeTabPage; 401; 403; 404; 503 | PLT |
| GET /api/recovery/cases/{caseId}/payments | rwb-payment GET /api/recovery/payment/v1/proceeds | P8 | Pass-through, one owner answer per tab; the Ownership Map names GET /proceeds and the case-scoped list path is the working read of the assumption below | 200 PaymentTabPage; 401; 403; 404; 503 | PLT |
| GET /api/recovery/cases/{caseId}/legal-actions | rwb-litigation GET /api/recovery/litigation/v1/legal-actions/{legalActionId} | S4 | Pass-through, one owner answer per tab | 200 LegalTabPage; 401; 403; 404; 503 | PLT |
| GET /api/recovery/me/tasks | rwb-case GET /api/recovery/case/v1/me/tasks | P3 | Pass-through: the officer's own task list, taken from the session identity and never from a request parameter | 200 TaskPage; 401; 403; 404; 503 | PLT |
| GET /api/recovery/inbox/stream | None: the gateway holds the push and reads the two inbox events | PLT | The stream carries ApprovalRequested and TimerBreached as they arrive, to the session that owns them; the transport is Not specified in the source documents (GAP-1393; ASM-2429) | 200 stream; 401; 403; 503 | PLT |

Only `/api/recovery/**` and `/api/recovery/cases/{id}` appear in Architecture v5, and the tab owners appear on slide 10 (Documents rwb-document, Notices rwb-comms, Payments rwb-payment, Legal rwb-litigation). The tab paths above, the inbox stream path and the case-scoped shape of the notice and payment reads are therefore the working read of ASM-2429, recorded with GAP-1393: no source states the gateway's own path table, the transport of the push, or which payment operation a case-scoped tab read uses. The document is published at that read and is corrected by a new version when the gap closes.

**12.2 REST operations consumed**

| Operation | Provider | Why the gateway calls it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId} | rwb-case (P3) | The case, stage, tasks and timers of the case screen | DP-19, DP-11 |
| GET /api/recovery/source-data/v1/customers/{personKey} | rwb-source-data (P1) | Case screen customer read: getCustomer in rwb-source-data.yaml 5.1.0, with policy-masked values (RD-P1-060) | DP-19, DP-11 |
| GET /api/recovery/source-data/v1/accounts/{accountKey} | rwb-source-data (P1) | Case screen account read: getAccount in rwb-source-data.yaml 5.1.0 (RWB-P1-E1069-APP) | DP-19, DP-11 |
| GET /api/recovery/document/v1/cases/{caseId}/documents | rwb-document (P5) | The Documents tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/comms/v1/notices/{noticeId} | rwb-comms (P6) | The Notices tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/payment/v1/proceeds | rwb-payment (P8) | The Payments tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/litigation/v1/legal-actions/{legalActionId} | rwb-litigation (S4) | The Legal tab, loaded on click | DP-19, DP-11 |

Seven consumption rows and eight HTTP calls, because the rwb-source-data row carries the customer read and the account read. Every row is one hop, 2 s, with a breaker per provider and a GET retried once with jitter. No row points at a service that calls another service.

**12.3 Events published**

None. gateway-bff is shared platform and has no topic of its own: it publishes no `rwb.<short>.events.v1` and no event schema. The two inbox events it consumes belong to rwb-decision and rwb-case, and the three cache-refresh events to rwb-access and rwb-decision.

**12.4 Events consumed**

| Event | Topic | Message schema | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.ApprovalRequested.v1 | rwb.decision.events.v1 | ApprovalRequested | Approval identifier, case identifier, decision type code, DoA band code, requested at | Officer inbox push to the approver's own session |
| rwb.case.TimerBreached.v1 | rwb.case.events.v1 | TimerBreached | Case identifier, timer code, stage code, breached at | Officer inbox push to the owner's own session |
| rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | AccessPolicyChanged | Policy identifier, version, in force at | Permission cache refresh at the edge |
| rwb.access.DoaLimitChanged.v1 | rwb.access.events.v1 | DoaLimitChanged | DoA table identifier, version, in force at | Permission cache refresh at the edge |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | RulePackageInForce | Rule package identifier, version, in force at | Permission and rule-version cache refresh at the edge |
| rwb.source-data.AceDataLate.v1 | rwb.source-data.events.v1 | AceDataLate | sourceSystem, businessDate, status, completedAt (nullable) | Late-data banner (EV-27). The banner route, text and clearing rule are Pending: owner platform edge owner with the solution architect, tracked as GAP-3313 |

All six are CloudEvents 1.0, keyed by the case identifier for the two inbox events, by the policy, table or package identifier for the three refresh events and by `{sourceSystem}:{businessDate}` for AceDataLate, with identifiers and facts only. AceDataLate is published once per due source system and business date (05:30 Asia/Bangkok, or at once on a FAILED batch row); the gateway's consumer group on `rwb.source-data.events.v1` (one group per service, KTEC Rules R13) is declared by the edge deployment story (RD-P1-044). This story publishes the consumer schemas; the producers keep their own contracts, and the dedupe inbox that makes the consumers idempotent is part of RWB-PLT-N001-APP.

**12.5 Workflows and activities**

None. The edge starts no Temporal workflow and polls no task queue; it has no `rwb-<short>` queue and no Schedules.

**12.6 Schedules**

None. The edge owns no Schedule and no batch window.

**12.7 Tables owned**

None. gateway-bff owns no `rwb_*` schema and no table. The session store is Redis, provisioned by RWB-PLT-N006-INF, and it holds session records only. No document in this contract references a table of any owning service.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| gateway-bff route fake (this story) | The seven public routes, with the case screen, the four tabs, the task list, the stream, and the 401, 403, 404 and 503 examples | RWB-PLT-N001-APP, the ACE front end, the integration harness |
| rwb-case contract fake (P3) | GET /cases/{caseId}, GET /me/tasks | The case screen and my-work examples |
| rwb-source-data contract fake (P1), version 5.1.0 under `fakes/rwb-source-data/5.1.0/` (RD-P1-011) | AceDataLate message; GET /customers/{personKey} and GET /accounts/{accountKey} masked examples per RD-P1-060 | The customer and account half of the case screen |
| rwb-document, rwb-comms, rwb-payment and rwb-litigation contract fakes (P5, P6, P8, S4) | The four tab reads | The tab examples and the degraded-tab example |

The gateway fake answers from these owner fakes rather than from copied payloads, so an owner model change shows up as a contract-test failure at the edge.

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 7 public routes under `/api/recovery`, with no service segment and no `/v1` | 7 consumption rows, 8 HTTP calls (the rwb-source-data row carries the customer and the account read) | OpenAPI 3.1, one hop, depth 1, 2 s timeout, breaker per downstream, GET retried once with jitter |
| Kafka | 0 published | 6 consumed message schemas | AsyncAPI 3.0, CloudEvents 1.0, key case id, policy identifier or sourceSystem:businessDate |
| Temporal | 0 | 0 | The edge starts no workflow |
| File | 0 | 0 | No file crosses the edge; documents are read through the owner |

### 13. Solution plan

**Deliverables.** `gateway-routes.yaml` (OpenAPI 3.1, the seven public routes and the screen model), `gateway-consumers.yaml` (AsyncAPI 3.0, the six consumed events), the route table and the error map of sections 12 and 14 (generated into the document), the route fake, and the contract test.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` for the services, and `/api/recovery/...` with no service segment for the shared edge | none |
| DP-19 | Screen, ace-web (includes run screen GET /agent-runs/{id}; data owner remains P10) | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows that apply to a screen composite. The story documents them and adds no dependency of its own: it is a CON story and starts on Day 1.

**Build steps**

1. Write `gateway-routes.yaml` with the seven routes, one tag per screen area, the screen model and the tab page models.
2. Write the security section: the opaque cookie, the 15-minute idle, the session in Redis, the short-lived user JWT from ACE Common and the coarse permission, with object-level authorisation declared as the owner's duty.
3. Write `gateway-consumers.yaml` with the six channels, the CloudEvents headers, the keys and the payload schemas.
4. Add the lint rules: OpenAPI 3.1 and AsyncAPI 3.0 validation, no service segment and no `/v1`, one problem envelope, the four error responses on every route, depth 1 per route, and a personal-data scan over the examples.
5. Generate the route table and the error map from the document, and fail the build if section 12 and the document disagree.
6. Generate the route fake over the owner fakes and write the contract test that pins the routes, the models and the codes.
7. Publish v1 to the contract registry, notify RWB-PLT-N001-APP and the ACE front end, and record the version they pin.

**Done when.** Both documents validate, every lint rule passes, the route table and the error map match the documents, the fake answers all seven routes and every example, and the contract test is green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| EDGE-401 | No session cookie, or the session is idle-expired or signed out in Redis | Problem details with `messageCode` MSG-P4-001 and the sign-in entry point; edge-specific title and detail text are Not specified in the source documents (GAP-1393; ASM-2429) | 401 |
| EDGE-403 | The coarse permission check at the edge refuses the screen | Problem details with `messageCode` MSG-P4-002; where the refusal comes from the owner, the owner's problem passes through unchanged | 403 |
| EDGE-404 | The owner answers not found for the case or the object | The owner's problem, including `messageCode` MSG-P4-003 and detail, passes through unchanged | 404 |
| EDGE-503 | A downstream exceeds 2 s, or its breaker is open | Problem details with `messageCode` MSG-GEN-006, naming the route and the downstream service in `detail`, so the screen can mark one tab temporarily unavailable | 503 |
| EDGE-400 | A path or query value fails the shape check at the edge | Problem details with `messageCode` MSG-GEN-001 (MSG-GEN-007 for a value outside its list) and `field` naming the parameter | 400 |
| EDGE-500 | An unexpected failure at the edge, with the detail kept out of the response | Problem details with `traceId`; `messageCode` Pending: owner platform edge owner, tracked as GAP-3312 | 500 |

Every error is `application/problem+json` on the shared `Problem` schema (RD-P1-004): `type`, `title`, `status`, `messageCode` (pattern `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$`) and `traceId` required; `detail`, `instance`, `messageTh`, `field` and `errors` optional; no other member. The identifiers EDGE-nnn name the rows of this table and are never sent on the wire. Edge-written problems use the message codes of the RD-P1-004 table; edge-specific titles have no source text (Architecture v5 slides 10 and 11 state only RFC 9457, the 2 s timeout, the breaker and the pass-through rule), and the code of the 500 row is Pending (GAP-3312).

### 15. Screens and states

No screen in this story, and the document declares none: the gateway composes the models that the ACE front end renders. The route surface fixes what the case record view of REQ-OCC-007 can show and the four states each area owns: loading, loaded, temporarily unavailable and session expired.

- The case screen is one composite model over rwb-case and rwb-source-data, loaded on open.
- Documents, Notices, Payments and Legal load on click, each from its owner, one hop.
- The officer inbox is a push stream over the two inbox events, and the state it adds is "new item" beside loading, loaded and session expired.

The states the edge exposes are the session states and the permission-cache states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N001-CON-01 | AC1 | Contract | `gateway-routes.yaml` validated and linted; the seven routes compared against section 12.1; the depth-of-1 assertion; no service segment and no `/v1` in any path |
| TC-PLT-N001-CON-02 | AC2 | Contract | The case screen route: the two parallel calls, the merge rule, the 0.15 + 0.6 + 0.3 s budget, about 1.2 s inside the 2 s target; one failed parallel call returns the AC4 problem and no partial model |
| TC-PLT-N001-CON-03 | AC3 | Contract | The security section: opaque cookie, 15-minute idle, session in Redis, per-request short-lived user JWT, coarse permission only, object-level authorisation with the owner |
| TC-PLT-N001-CON-04 | AC4 | Contract | The problem schema and the 400, 401, 403, 404, 500 and 503 examples; the pass-through of the owner's `messageCode`, `detail` and other members. |
| TC-PLT-N001-CON-05 | AC5 | Contract | `gateway-consumers.yaml` validated; six channels; CloudEvents headers; keys; a personal-data scan of every example. |
| TC-PLT-N001-CON-06 | AC6 | Component | The route fake over the owner fakes; all seven routes and every example answered; the table equals the document; a breaking change raises v2 and deprecates v1 |
| TC-PLT-N001-CON-07 | AC7 | Contract | The section 8 trace table against sections 7 and 16; every rule BR1 to BR9 names an existing criterion and test case |
| TC-PLT-N001-CON-08 | AC8 | Component | A disallowed status change sent to a case route; the AC4 problem returned; the case state unchanged; no business values or personal data in the refusal |
| TC-PLT-N001-CON-09 | AC9 | Component | AC9 The edge passes ETag and If-Match through unchanged (new, RD-P1-006) |
| TC-PLT-N001-CON-10 | AC10 | Contract | AC10 A problem with several failing inputs passes through whole (new, RD-P1-004) |
| TC-PLT-N001-CON-11 | AC2 | Contract | The case screen route: the two parallel calls, the merge rule, the 0.15 + 0.6 + 0.3 s budget, about 1.2 s inside the 2 s target; one failed parallel call returns the AC4 problem and no partial model |

### 17. Guardrails

- One hop, depth 1: no route points at a service that calls another service, and a needed chain is moved into the owner rather than added at the edge.
- 2 s timeout on every downstream call, a breaker per downstream, and a GET retried once with jitter; a timeout is answered as 503 problem details, never as a stale screen.
- No business values in the document: thresholds, bands and limits stay behind the owner's contract or its parameters.
- No personal data in examples, logs or events: identifiers, codes and status values only, and the scan fails the build otherwise.
- No business data at the edge: the session record holds identifiers and role codes, Redis holds sessions only, and no customer, account, case or document row is cached at the gateway.
- Object-level authorisation stays with the owner service; the edge never stands in for it by hiding a screen.
- The public base is `/api/recovery` with no service segment and no `/v1`, and the monolith base is never republished (DP-13).
- The surface is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions on one screen | Program BRD v4, 5.6 | TC-PLT-N001-CON-01, TC-PLT-N001-CON-02, TC-PLT-N001-CON-06, TC-PLT-N001-CON-11 |
| NFR-008 | A screen responds within its target under normal load: under 2 seconds | Program BRD v4, NFR table | TC-PLT-N001-CON-02 |
| NFR-009 | The case record view loads for a case with 50 documents: under 2 seconds | Program BRD v4, NFR table | TC-PLT-N001-CON-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N001-APP | App development | H consumer: implements the seven routes, the session filter and the composition against this contract and its fake |
| RWB-PLT-N006-INF | Infrastructure | X: provisions the Redis session store the routes read, with sessions only |
| RWB-PLT-N007-INF | Infrastructure | X: partners enter through the partner gateway in the DMZ and never through this route surface |
| RWB-P3-E1018-CON, RWB-P1-E1064-CON, RWB-P5-E1032-CON, RWB-P6-E1052-CON, RWB-P8-E2008-CON, RWB-S4-E5001-CON | Contract | C: the owner contracts behind the seven downstream operations |

### 19. Out of scope

- The gateway implementation: the Spring Cloud Gateway routes, the session filter, the composition, the resilience and the push are RWB-PLT-N001-APP.
- The Redis session store and its sizing, keyspace and eviction policy: RWB-PLT-N006-INF.
- Partner access, FAPI 2.0 and the DMZ gateway: RWB-PLT-N007-INF. Partners never call this surface.
- Object-level authorisation and every business rule behind a screen: the owner services and the rwb-access contract.
- The ACE front end itself: the screens, the layout and the client state are the front-end workbench.
- The owner documents themselves, their schemas, topics and tables: the six owner contract stories.
- The monolith base and its route table: retired, never republished (DP-13).

### Remaining delivery steps


- Size the story at refinement (squad).
- Publish the route fake and gateway-consumers.yaml to the contract registry and record the pinned versions (platform edge owner).
- Add the new and changed TC-PLT-N001-CON assertions to Test Cases v9 and the RTM (QA lead).
