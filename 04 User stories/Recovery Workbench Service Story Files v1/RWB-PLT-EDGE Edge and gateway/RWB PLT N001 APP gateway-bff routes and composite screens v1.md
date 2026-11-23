# RWB-PLT-N001-APP gateway-bff routes and composite screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N001-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-PLT-EDGE-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform app story for the gateway-bff route implementation, session filter and composite case screen. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Recovery officer opening a case in the workbench**, I want **one gateway that resolves my session, asks each owner service once in parallel and puts the case record view on one screen in under 2 seconds**, so that **I see the case, the customer, the account, the documents, the notices, the payments and the legal actions without the screen chaining calls or failing whole when one owner is slow**.

This is the app story of new platform key N001 under epic RWB-PLT-EDGE. It implements the route surface published by RWB-PLT-N001-CON as a Spring Cloud Gateway application:

- The route table and the filter chain, one hop per route, with Spring Cloud Gateway routes generated from the published document.
- The session filter: the opaque cookie resolved in Redis, the 15-minute sliding idle, 401 and the sign-in redirect on a miss.
- The short-lived user JWT obtained per request through ACE Common sign-in, forwarded with the workload identity and never exposed to the browser.
- The coarse permission check at the edge, with object-level authorisation left to the owner service.
- The composite case screen: rwb-case GET /v1/cases/{caseId} and rwb-source-data GET /v1/customers/{id} and /v1/accounts/{id} in parallel, merged into the screen model, budgeted at about 1.2 s against the 2 s target.
- The four tab routes and the officer task list, one hop each, loaded when clicked.
- Resilience: 2 s timeout per downstream, a breaker per downstream, a GET retried once with jitter, and a bulkhead so one slow owner cannot take the pool.
- The RFC 9457 problem envelope, the officer inbox push over the two inbox events, the permission-cache consumers over the three refresh events, OpenTelemetry traces and metrics, and the platform `/health` and `/metrics` endpoints.

The gateway is shared platform: it owns no schema, no topic and no task queue, and it stores no business data. The session store is Redis, provisioned by RWB-PLT-N006-INF; partners reach Recovery through the partner gateway in the DMZ and never through this surface (RWB-PLT-N007-INF).

### 2. Business rationale

The case record view is the screen an officer lives in, and the legacy build served it from one application with in-process calls, so latency and failure were somebody else's problem. After the split the screen is assembled from six owners, and two things must hold at once: the officer must not wait for a chain of calls, and one slow owner must not blank the screen. The design answers both at the edge — at most a few parallel calls, one hop each, a 2 s timeout, a breaker per downstream, and a degraded tab instead of a failed screen (DP-19, DP-11).

The gateway is also where the security baseline is enforced once instead of six times: an opaque cookie in the browser, the session in Redis with a 15-minute idle, a short-lived user JWT from ACE Common per request, and a coarse permission check. The owner services keep object-level authorisation (OWASP API1), which is what makes REQ-OCC-007 true without turning the edge into a second authorisation service.

The numbers come straight from the walkthrough: 0.15 s gateway and session, 0.6 s slowest parallel call, 0.3 s merge, about 1.2 s against the 2 s target, and the 50-document case of NFR-009 is the case that proves it.

### 3. Preconditions

- The route surface of RWB-PLT-N001-CON is published at v1, with the route fake, the error map and the consumed event schemas.
- The shared Azure App Gateway with WAF routes `/recovery/*` and `/api/recovery/*` to this application (Architecture v5 slide 8).
- The Redis session store is available with its keyspace and eviction policy (RWB-PLT-N006-INF); this story configures the client and the record shape only.
- ACE Common sign-in provides the authorization code flow, the short-lived user JWT and the audit path; this story configures the OAuth2 client and forwards the token, and does not implement sign-in.
- The owner services publish their contracts and fakes; this story builds against the fakes and never against a live service in its own tests.
- The service-to-service identity is the workload identity of the platform, mutually authenticated, as every service-to-service call is (Architecture v5 slide 35).
- The runtime is set by the platform: OpenTelemetry traces, metrics and logs, `/health` and `/metrics`, and the namespace of the Recovery services.
- No approval is required to start: the story is Draft (realignment v1) and builds against the published contract.

### 4. Flow

1. The browser calls `/api/recovery/cases/{caseId}` through the shared App Gateway with the opaque session cookie.
2. The session filter resolves the cookie in Redis; a miss or an idle expiry answers 401 with the sign-in redirect, a hit refreshes the 15-minute idle and continues.
3. The token filter obtains a short-lived user JWT for that session through ACE Common sign-in, caches it for its short life, and attaches it with the workload identity to the downstream call; it never returns the token to the browser.
4. The authorisation filter checks the coarse permission for the route against the cached policy; a refusal answers 403 problem details.
5. The composition filter calls rwb-case GET /v1/cases/{caseId} and rwb-source-data GET /v1/customers/{id} and GET /v1/accounts/{id} in parallel, each with a 2 s timeout, its own breaker and one retry with jitter on a GET.
6. The merge step takes the customer and account references from the case answer and writes the case, stage, tasks and timers beside the customer and the account into one screen model; nothing else is fetched, nothing off screen is loaded.
7. The response is written with `Cache-Control: no-store` and the correlation identifier of the trace; a downstream timeout or an open breaker answers 503 problem details for that part of the model, and the tab renders as temporarily unavailable while the rest of the screen renders.
8. A tab route repeats steps 2 to 5 with a single owner call and a pass-through body; the officer task list reads the identity from the session and never from a request parameter.
9. The inbox stream opens for the session, and ApprovalRequested and TimerBreached are pushed to the officer's own open session as they arrive; a push for a session that is closed is dropped.
10. AccessPolicyChanged, DoaLimitChanged and RulePackageInForce refresh the permission cache; on a failed refresh the last good copy stays in force and an alert is raised.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | No session cookie, or the session expired after 15 idle minutes | 401 problem details and the sign-in redirect; no downstream call is made | EDGE-401 |
| X2 | The session is valid but the coarse permission refuses the route | 403 problem details; nothing is fetched | EDGE-403 |
| X3 | A downstream exceeds 2 s | The call is abandoned, the breaker records the failure, and the affected part answers 503; the rest of the screen renders | EDGE-503 |
| X4 | A downstream breaker is open | The call is not attempted; the affected part answers 503 immediately and the tab shows temporarily unavailable | EDGE-503 |
| X5 | A GET fails with a retryable error | It is retried once with jitter; a second failure follows X3 | EDGE-503 |
| X6 | One owner is slow and the pool fills | The bulkhead limits concurrent calls per downstream, so the other routes keep serving | EDGE-503 on the affected route |
| X7 | The permission cache refresh fails | The last good cache stays in force and an alert is raised; no request is served from an empty policy | Alert, no message id |
| X8 | A push event arrives for a session that is no longer open | The push is dropped and the event is acknowledged; no queue builds up | None |
| X9 | A downstream answers 404 or 403 for the object | The owner's status, message identifier and detail pass through unchanged | Owner message id |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contract and its fake; adds no build dependency and waits for nothing |
| Negotiable | Filter order inside the chain, the screen model field order, the cache TTL and the push transport are open until the contract version is frozen |
| Valuable | The case record view works on one screen under 2 seconds, and one slow owner no longer blanks the screen |
| Estimable | Seven routes, one filter chain, one composition, one push, three refresh consumers |
| Small | One sprint for the routes, the filters, the composition and the tests |
| Testable | Each criterion is a component or integration assertion in section 16, with a p95 budget |

### 7. Acceptance criteria

```gherkin
Feature: gateway-bff routes, session filter and composite case screen

  Background:
    Given the gateway-bff public base is /api/recovery with no service segment and no /v1
    Given the route surface of RWB-PLT-N001-CON v1 is published and the owner fakes are running

  Scenario: AC1 The session filter resolves the opaque cookie in Redis (new, D-RCV-60)
    Given a request with the opaque session cookie
    When the session filter runs
    Then the session is resolved in Redis and the 15-minute idle is refreshed on every request
    Then a missing or idle-expired session answers 401 problem details with the sign-in redirect and makes no downstream call
    Then the session record holds the session identifier, user identifier, role codes, issued at, last seen and idle expiry, and Redis holds no business data

  Scenario: AC2 A short-lived user JWT is obtained per request and never exposed (new, D-RCV-60)
    Given an authenticated session
    When the token filter runs
    Then it obtains a short-lived user JWT through ACE Common sign-in and caches it only for its short life
    Then the JWT is forwarded to the owner with the workload identity and never appears in a response header, a cookie or a log
    Then a sign-in failure answers 503 problem details and is not retried in a loop

  Scenario: AC3 The case screen is composed from two parallel calls and merged (new, D-RCV-60)
    Given the case screen route GET /api/recovery/cases/{caseId}
    When the composition filter runs
    Then rwb-case GET /v1/cases/{caseId} and rwb-source-data GET /v1/customers/{id} and /v1/accounts/{id} are called in parallel, one hop each
    Then only what is on screen is fetched, and the merge writes case, stage, tasks and timers beside the customer and the account
    Then the p95 is 0.15 s gateway and session plus 0.6 s slowest call plus 0.3 s merge, about 1.2 s against the 2 s target

  Scenario: AC4 A slow owner is isolated and the rest of the screen still renders (new, D-RCV-60)
    Given one downstream is slow or its breaker is open
    When the route runs
    Then each downstream call has a 2 s timeout and a breaker of its own, a GET is retried once with jitter, and a bulkhead caps concurrent calls per downstream
    Then the affected part answers 503 problem details and the tab shows temporarily unavailable
    Then the rest of the screen renders, and the 2 s target is still met for the parts that answered

  Scenario: AC5 The permission cache refreshes from the three events and keeps the last good copy (new, D-RCV-60)
    Given the permission cache in force
    When AccessPolicyChanged, DoaLimitChanged or RulePackageInForce arrives
    Then the cache is refreshed from rwb-access and the new version is applied to the next request
    Then a failed refresh keeps the last good cache in force and raises an alert
    Then no request is ever served from an empty policy

  Scenario: AC6 The inbox push reaches only the officer's own open session (new, D-RCV-60)
    Given an open inbox stream for an authenticated officer session
    When ApprovalRequested or TimerBreached arrives
    Then the push is delivered to that session only, carrying identifiers and facts and no personal data
    Then a push for a closed or expired session is dropped and the event is acknowledged
    Then no push is delivered to another officer's session
```

These criteria are new and test only the edge implementation: no legacy acceptance criterion is repeated here, and every number comes from the Architecture v5 walkthrough, the contract of RWB-PLT-N001-CON or the requirements named in section 18.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every route is one hop to one owner service; no downstream call is chained | Architecture v5 slides 10 and 20 |
| BR2 | A composite screen calls its owners in parallel and only for what is on screen; the other tabs load on click | Architecture v5 slide 10 |
| BR3 | A session is an opaque cookie, resolved in Redis, 15 minutes idle, and a request refreshes the idle | Architecture v5 slide 20 |
| BR4 | The edge checks a coarse permission only; object-level authorisation stays inside the owner service | Architecture v5 slides 10 and 35 |
| BR5 | Every downstream call has a 2 s timeout, a breaker per downstream and one retry with jitter on a GET | Architecture v5 slide 10 |
| BR6 | A failure is answered as RFC 9457 problem details, and the owner's message identifier and detail pass through unchanged | Architecture v5 slide 11 |
| BR7 | No business data is stored at the edge: the session record holds identifiers and role codes, and Redis holds sessions only | Architecture v5 slide 20 |
| BR8 | The officer inbox push carries identifiers and facts only, to the session that owns them, and never to another officer | Architecture v5 slide 20; event catalogue |
| BR9 | The permission cache serves the last good copy when a refresh fails, and an alert is raised | Architecture v5 slide 20 |
| BR10 | The public base is `/api/recovery` with no service segment and no `/v1` | DP-13; Architecture v5 slides 10 and 20 |

### 9. State transitions

| Object | From | Event | To | HTTP result at the edge |
|---|---|---|---|---|
| Session | ABSENT | Sign-in completes in ACE Common and the session record is written | AUTHENTICATED | 302 back to the screen, then 200 |
| Session | AUTHENTICATED | A request arrives inside the 15-minute idle | AUTHENTICATED | 200, and the idle expiry moves |
| Session | AUTHENTICATED | 15 minutes pass with no request | IDLE_EXPIRED | 401 on the next request, with the sign-in redirect |
| Session | AUTHENTICATED | The officer signs out | SIGNED_OUT | 401, and the record is removed from Redis |
| Session | IDLE_EXPIRED | The officer signs in again | AUTHENTICATED | 302 back to the screen, a new session identifier |
| Session | SIGNED_OUT | Any request with the old cookie | SIGNED_OUT | 401, and no downstream call |
| Permission cache | FRESH | A request needs the coarse permission | FRESH | The check is answered from memory |
| Permission cache | FRESH | AccessPolicyChanged, DoaLimitChanged or RulePackageInForce arrives | STALE | The next request may see the old copy while the refresh runs |
| Permission cache | STALE | The refresh from rwb-access succeeds | REFRESHED | The new version is in force and the check uses it |
| Permission cache | STALE | The refresh fails | STALE | The last good copy keeps serving, and an alert is raised |
| Permission cache | REFRESHED | The next event arrives | STALE | As above |

A session never returns from SIGNED_OUT; the officer signs in again and gets a new session identifier. The permission cache is held in memory per pod, and its states are per pod.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The gateway team (any team, per U3) | Builds, tests and deploys the routes, the filters, the composition and the push |
| The platform owner of the edge | Owns the runtime, the deployment and the version pin of the contract |
| The ACE Common team | Owns sign-in, the user JWT and the audit path the gateway calls |
| The owner services (P3, P1, P5, P6, P8, S4) | Own the data and the object-level authorisation behind every route |
| The front-end team of the ACE workbench | Consumes the screen model; raises a change request rather than a private field |
| No delegation of authority level is checked at the edge | The edge checks a coarse permission; a DoA decision is the owner's and rwb-access's business |

No personal name, no email address and no credential appears in the code, the configuration, a log or a trace. A session and a user are identifiers and role codes only.

### 11. Data

| Item | Value |
|---|---|
| Session record in Redis | Session identifier, user identifier, role codes, issued at, last seen, idle expiry. Nothing else |
| Business data at the edge | None. No customer, account, case, document, notice, payment or legal-action row is stored, cached or logged at the gateway |
| Screen model | Assembled per request in memory and discarded with the response; never written to Redis, a log or a trace attribute |
| Permission cache | Policy version, role-to-route grants and the DoA band codes needed by the coarse check; identifiers and codes only, refreshed from rwb-access |
| Push payload | Event identifier, case identifier, decision or timer code, occurred at; no name, no amount, no document content |
| Retention | The session record expires with the session; the cache expires with the refresh; the gateway keeps no store of its own |
| Data at rest | None. The gateway writes no table and owns no schema; the session store is RWB-PLT-N006-INF |

### 12. Contract

**12.1 REST operations provided**

None. The route surface is published by RWB-PLT-N001-CON; this story implements it and publishes no document of its own. The seven routes it serves, all under `/api/recovery` with no service segment and no `/v1`, are GET /api/recovery/cases/{caseId}, GET /api/recovery/cases/{caseId}/documents, GET /api/recovery/cases/{caseId}/notices, GET /api/recovery/cases/{caseId}/payments, GET /api/recovery/cases/{caseId}/legal-actions, GET /api/recovery/me/tasks and GET /api/recovery/inbox/stream. The contract test of the CON story is the gate this implementation is verified against.

**12.2 REST operations consumed**

| Operation | Provider | Why the gateway calls it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId} | rwb-case (P3) | The case, stage, tasks and timers of the case screen | DP-19, DP-11 |
| GET /api/recovery/source-data/v1/customers/{id} | rwb-source-data (P1) | The customer half of the case screen, in parallel with the case read | DP-19, DP-11 |
| GET /api/recovery/source-data/v1/accounts/{id} | rwb-source-data (P1) | The account half of the case screen, in the same parallel call | DP-19, DP-11 |
| GET /api/recovery/document/v1/cases/{caseId}/documents | rwb-document (P5) | The Documents tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/comms/v1/notices/{noticeId} | rwb-comms (P6) | The Notices tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/payment/v1/proceeds | rwb-payment (P8) | The Payments tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/litigation/v1/legal-actions/{legalActionId} | rwb-litigation (S4) | The Legal tab, loaded on click | DP-19, DP-11 |
| GET /api/recovery/case/v1/me/tasks | rwb-case (P3) | The officer's own task list | DP-19, DP-11 |
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | The coarse permission check, answered from the cached policy when the cache is fresh | DP-08, DP-11 |

Eight owner reads over six services, and one authorise call to rwb-access, each one hop with a 2 s timeout, a breaker per provider and one retry with jitter on a GET. The authorise call is made only when the cache is stale; the steady path answers from memory.

**12.3 Events published**

None. The gateway has no topic of its own and publishes no event; the inbox push is a stream to the browser session, not a Kafka message.

**12.4 Events consumed**

| Event | Topic | Message schema | Payload carries | Use |
|---|---|---|---|---|
| rwb.decision.ApprovalRequested.v1 | rwb.decision.events.v1 | ApprovalRequested | Approval identifier, case identifier, decision type code, DoA band code, requested at | Push to the approver's own open session |
| rwb.case.TimerBreached.v1 | rwb.case.events.v1 | TimerBreached | Case identifier, timer code, stage code, breached at | Push to the owner's own open session |
| rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | AccessPolicyChanged | Policy identifier, version, in force at | Permission cache refresh |
| rwb.access.DoaLimitChanged.v1 | rwb.access.events.v1 | DoaLimitChanged | DoA table identifier, version, in force at | Permission cache refresh |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | RulePackageInForce | Rule package identifier, version, in force at | Permission and rule-version cache refresh |

All five are consumed through an inbox that dedupes by event identifier; the schemas are the ones published in RWB-PLT-N001-CON 12.4.

**12.5 Workflows and activities**

None. The gateway starts no Temporal workflow, polls no task queue and signals nothing.

**12.6 Schedules**

None. The gateway owns no Schedule; the idle sweep of expired sessions is a Redis expiry, not a job.

**12.7 Tables owned**

None. The gateway owns no `rwb_*` schema and no table. The session store is Redis, provisioned by RWB-PLT-N006-INF, and it holds session records only; the gateway writes no business row anywhere.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| rwb-case contract fake (P3) | GET /cases/{caseId}, GET /me/tasks | The composition and my-work component tests |
| rwb-source-data contract fake (P1) | GET /customers/{id}, GET /accounts/{id} | The composition test, including the slow and failing variants |
| rwb-document, rwb-comms, rwb-payment and rwb-litigation contract fakes (P5, P6, P8, S4) | The four tab reads | The tab tests and the degraded-tab test |
| rwb-access contract fake (P4) | POST /authorise | The coarse check and the cache-refresh tests |
| gateway-bff route fake (RWB-PLT-N001-CON) | The seven public routes and every example | The contract test this implementation is verified against |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 documents of its own; it serves the 7 routes published by RWB-PLT-N001-CON | 9 consumption rows: 8 owner reads over six services, plus the rwb-access coarse check, made only when the cache is stale | OpenAPI 3.1 at the contract, one hop, 2 s, breaker per downstream, one retry with jitter |
| Kafka | 0 published | 5 consumed message schemas | CloudEvents 1.0, inbox dedupe by event identifier |
| Temporal | 0 | 0 | The edge starts no workflow |
| File | 0 | 0 | No file crosses the edge |

### 13. Solution plan

**Deliverables.** The Spring Cloud Gateway application (route definitions generated from the published document), the filter chain, the reactive Redis session repository, the OAuth2 client for ACE Common, the Resilience4j configuration, the WebClient composition and merge, the problem-details writer, the server-sent-event inbox stream, the three cache-refresh consumers, the OpenTelemetry instrumentation, and `/health` and `/metrics`.

**Filter chain order** (global filters, in order):

| Order | Filter | Duty |
|---|---|---|
| 10 | Correlation filter | Takes or creates the trace and correlation identifier and puts it on the response |
| 20 | Session filter | Resolves the opaque cookie in Redis, refreshes the idle, answers 401 |
| 30 | Token filter | Obtains and caches the short-lived user JWT, attaches it with the workload identity |
| 40 | Authorisation filter | The coarse permission check from the cached policy, answers 403 |
| 50 | Route filter | Rewrites the public path to the owner operation, one hop |
| 60 | Resilience filter | Timeout, breaker, retry once with jitter on a GET, bulkhead |
| 70 | Composition filter | Runs the parallel calls and the merge for the case screen, or the pass-through for a tab |
| 80 | Problem filter | Writes RFC 9457 problem details, passes the owner's identifier and detail through unchanged |

**Pattern application.** DP-19 (gateway-bff composite route) and DP-11 (REST contract with mock, one hop, 2 s timeout) are the two rows of Template and Rules §R5.5 that this story applies; the story builds against the CON contract and its fake, so it adds no dependency of its own.

**Build steps**

1. Generate the route definitions from the published document and assert in the build that the generated table equals the document.
2. Implement the session filter over reactive Redis, with the record shape of section 11 and the 15-minute sliding idle.
3. Implement the token filter: the OAuth2 client for ACE Common sign-in, the short-lived JWT cache, the workload identity on the outgoing call, and a check that the token never reaches a response header, a cookie or a log.
4. Implement the authorisation filter and the in-memory permission cache, with the refresh from rwb-access and the FRESH, STALE and REFRESHED states of section 9.
5. Implement the composition filter with WebClient: parallel calls, the merge rule, the p95 budget, and the degraded part on a timeout or an open breaker.
6. Configure Resilience4j per downstream: 2 s timeout, breaker with a bounded half-open probe, one retry with jitter on a GET, and a bulkhead.
7. Implement the problem filter and the error map of section 14, with the pass-through of the owner's identifier and detail.
8. Implement the inbox stream over server-sent events and the two inbox events, with the session binding and the drop rule for a closed session.
9. Implement the three cache-refresh consumers with the last-good-copy rule and the alert.
10. Wire OpenTelemetry across the edge and the downstream call, add `/health` and `/metrics`, and run the component and end-to-end tests of section 16.

**Done when.** The seven routes answer against the owner fakes, the session, token and permission behaviours pass their component tests, the case screen meets its p95 budget with a 50-document case, a slow or open downstream degrades one tab only, the push reaches only the officer's own open session, the cache refresh keeps the last good copy, and every trace carries one correlation identifier across the edge and the owner.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| EDGE-400 | A path or query value fails the shape check | Problem details naming the parameter | 400 |
| EDGE-401 | No session cookie, or the session is idle-expired or signed out | Problem details with the sign-in entry point; the title and detail text are Not specified in the source documents (GAP-1394; ASM-2430) | 401 |
| EDGE-403 | The coarse permission check refuses the route | Problem details; where the owner refused, the owner's message identifier and detail are passed through unchanged | 403 |
| EDGE-404 | The owner answers not found for the case or the object | Problem details; the owner's identifier and detail pass through unchanged | 404 |
| EDGE-503 | A downstream exceeds 2 s, its breaker is open, or sign-in fails | Problem details naming the route and the downstream, so the tab shows temporarily unavailable | 503 |
| EDGE-500 | An unexpected failure at the edge | Problem details with the correlation identifier only; no stack trace, no downstream body | 500 |

The owner message identifiers are the owners' own and are never rewritten at the edge; the edge's own titles are the one family with no source text, and the placeholder records that.

### 15. Screens and states

The gateway has no screen of its own: it composes the models that the ACE front end renders. What it fixes per area is the state model and the HTTP result that drives it.

| Area | Loading | Loaded | Temporarily unavailable | Session expired |
|---|---|---|---|---|
| Case record view (REQ-OCC-007) | The case, customer and account parts render as they arrive from the two parallel calls | The merged model: account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions | One part answers 503 and renders as temporarily unavailable while the other parts render | 401 and the sign-in redirect |
| Documents tab | Opened on click, one owner call | The owner's page, unwrapped | 503, retried by the officer | 401 and the sign-in redirect |
| Notices tab | Opened on click, one owner call | The owner's page, unwrapped | 503, retried by the officer | 401 and the sign-in redirect |
| Payments tab | Opened on click, one owner call | The owner's page, unwrapped | 503, retried by the officer | 401 and the sign-in redirect |
| Legal tab | Opened on click, one owner call | The owner's page, unwrapped | 503, retried by the officer | 401 and the sign-in redirect |
| Officer inbox | The stream opens on sign-in | ApprovalRequested and TimerBreached items arrive as they happen | The stream reconnects with a backoff and the tab shows the last known items | The stream closes and the session state governs |

The case with 50 documents is the NFR-009 case: the case screen renders under 2 seconds because the documents tab loads on click and the screen itself calls two owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N001-APP-01 | AC1 | Component | Reactive Redis stub; a cookie present, absent and idle-expired; the record shape; the idle refreshed on every request; no business key in the store |
| TC-PLT-N001-APP-02 | AC2 | Component | ACE Common sign-in stub; the short-lived JWT cached and reused inside its life; no token in a response header, a cookie or a log; a sign-in failure answers 503 |
| TC-PLT-N001-APP-03 | AC3 | Integration | rwb-case and rwb-source-data fakes; the two calls in parallel; the merge into the screen model; the p95 of 0.15 + 0.6 + 0.3 s, about 1.2 s against 2 s |
| TC-PLT-N001-APP-04 | AC4 | Integration | One fake slowed past 2 s, one breaker open, one GET failing once; the tab answers 503; the other parts render; the bulkhead caps concurrency |
| TC-PLT-N001-APP-05 | AC5 | Component | The three refresh events; the version applied on the next request; a failed refresh keeps the last good copy and raises an alert; an empty policy is never served |
| TC-PLT-N001-APP-06 | AC6 | Integration | Two officer sessions and one closed session; ApprovalRequested and TimerBreached; delivery to the owning session only; the closed session's push dropped; the event acknowledged |
| TC-PLT-N001-APP-07 | AC1 to AC6 | End to end | The shared App Gateway path with the opaque cookie: the case screen with 50 documents, the four tabs, the inbox push, an idle expiry after 15 minutes, and one trace across the edge and the owner |

### 17. Guardrails

- No call chains: every route is one hop, the composition is parallel, and a needed chain is moved into the owner service.
- Owner services authorise the object; the edge checks a coarse permission and never stands in for object-level authorisation.
- No business values in code: thresholds, bands, limits and rule versions come from the owner contract, a parameter or the cached policy.
- No personal data in traces, logs, metrics or events: identifiers and codes only, no name, no email address, no account number, no document content.
- The session store holds no business data: an opaque session record with identifiers and role codes, and nothing else.
- 2 s timeout everywhere, a breaker per downstream, one retry with jitter on a GET, and a bulkhead per downstream.
- A failure is problem details with the owner's identifier passed through, never a swallowed error and never a stale screen presented as fresh.
- One correlation identifier across the edge and the owner, and the workload identity on every downstream call.
- The public base is `/api/recovery` with no service segment and no `/v1`; the monolith base is never served (DP-13).

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions on one screen | Program BRD v4, 5.6 | TC-PLT-N001-APP-03, TC-PLT-N001-APP-07 |
| NFR-008 | A screen responds within its target under normal load: under 2 seconds | Program BRD v4, NFR table | TC-PLT-N001-APP-03, TC-PLT-N001-APP-04, TC-PLT-N001-APP-07 |
| NFR-009 | The case record view loads for a case with 50 documents: under 2 seconds | Program BRD v4, NFR table | TC-PLT-N001-APP-07 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N001-CON | Contract | H: publishes the routes, the error map, the consumed event schemas and the route fake this story implements |
| RWB-PLT-N006-INF | Infrastructure | X: provisions the Redis session store this story reads and writes |
| RWB-PLT-N007-INF | Infrastructure | X: partners enter through the partner gateway in the DMZ and never through these routes |
| RWB-P3-E1018-CON, RWB-P1-E1064-CON, RWB-P5-E1032-CON, RWB-P6-E1052-CON, RWB-P8-E2008-CON, RWB-S4-E5001-CON | Contract | C: the owner contracts behind the nine downstream calls, built against their fakes |

### 19. Out of scope

- The route documents, the error map and the route fake: RWB-PLT-N001-CON.
- The Redis session store, its sizing, its eviction policy and its backup: RWB-PLT-N006-INF.
- Partner access, FAPI 2.0 and the DMZ gateway: RWB-PLT-N007-INF.
- The ACE front end, its screens, its layout and its client state: the front-end workbench.
- Object-level authorisation, the permission data itself and every business rule behind a screen: the owner services and rwb-access.
- Sign-in and MFA: ACE Common owns them; this story configures the client and forwards the token.
- The owner documents, schemas, tables and events: the six owner contract stories.
