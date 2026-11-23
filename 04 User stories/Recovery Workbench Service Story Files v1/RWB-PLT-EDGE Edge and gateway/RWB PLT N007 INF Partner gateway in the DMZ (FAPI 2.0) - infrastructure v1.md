# RWB-PLT-N007-INF Partner gateway in the DMZ (FAPI 2.0)

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N007-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EDGE |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N007 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EDGE-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-EDGE, legacy key N007. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure and security engineer**, I want **a separate partner gateway in the DMZ that fronts rwb-partner only, enforces the FAPI 2.0 security profile and signs partner users in with multi-factor authentication**, so that **partners reach their own instructions, results, invoices, data rooms and bids and nothing else in the Recovery workbench, and the staff edge stays a separate entry point with its own trust boundary**.

The partner gateway is the only network path a partner has. Arch v5 states it three ways: the system context shows `partner gateway` beside the shared App Gateway with `FAPI 2.0 → S9`; the service contract of rwb-partner gives it `Partner portal: /partner/v1/* (FAPI 2.0)` as an inbound REST surface and `Partners (law firms, agencies, buyers): via partner gateway, MFA` as its outbound note; and the edge section of the security slide says partners come only through the partner gateway (FAPI 2.0) while staff come through the shared App Gateway with WAF. The gateway-bff contract states the negative from the other side: partners do not use gateway-bff, they go partner gateway → rwb-partner.

This story delivers:

- A partner gateway in its own DMZ network zone, a separate zone from the shared App Gateway, with deny-by-default ingress and one allowed upstream: rwb-partner.
- The route surface: the partner portal paths `/partner/v1/*` of Arch v5 slide 17, mapped by the gateway to the base path of the service that owns each operation, and nothing else.
- The FAPI 2.0 Security Profile (final Feb 2025) in force at the authorisation server and at the gateway: pushed authorisation requests, sender-constrained access tokens bound to the client certificate over mTLS, strong client authentication, short-lived access tokens, refresh rules, and no token or secret in a URL.
- Multi-factor authentication at partner sign-in, and the mapping of an external partner identity to one partner user with the roles of that partner.
- Partner client registration and certificate and key lifecycle: onboarding, activation, suspension, revocation, rotation and an annual review.
- WAF policy, per-client rate limits, request size limits, TLS and mTLS to rwb-partner, workload identity on the upstream hop, and PII-safe audit logging to the SOC through the bank's PII logging path.
- Disaster recovery, a runbook, and the penetration test and security review gate that must be passed before the gateway is opened to partner users outside the bank.

The gateway is shared platform, not a service. It publishes no REST operation of its own, no Kafka event, no Temporal workflow and no table; the operations it exposes belong to rwb-partner (S9) and rwb-debtsale (S6) and are published by their contract stories. It holds no business data: at the edge there is a client registry, token metadata and an audit record, and nothing else.

### 2. Business rationale

Partners are outside the bank. Law firms, agencies, auction vendors and buyers hold recovery work in the Workbench, and the bank cannot give them an SCB account, an Entra ID identity of the staff directory or a session on the staff edge. Arch v5 answers with two edges rather than one: staff reach the shared Azure App Gateway with WAF and the Recovery gateway-bff, and partners reach a partner gateway in the DMZ that fronts rwb-partner only (Arch v5 slides 7, 8, 20 and 35). The split is not cosmetic. A partner is an untrusted caller by default, so the controls that fit an outside caller — a separate network zone, pushed authorisation requests, sender-constrained tokens, strong client authentication, a short token lifetime — are applied at that edge and not weakened for it at the staff edge.

The regulation-facing requirements that make this story mandatory are REQ-ACA-012 (partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases) and REQ-S9-008 (partners exchange data through the partner portal and the external gateway, and not by email). Epic 2 requirement RWB-E2-019 adds the identity side: law firms, valuers and agencies sign in to the partner portal with external identities through the external gateway, with roles per partner. Without this gateway those three requirements have no place to be enforced, and the partner work of Epics 4, 5 and 6 — instructions, accept and decline, results, invoices, data room and bids — has no entry point at all.

FAPI 2.0 is the profile the architecture fixes for that entry point, and it is a profile with an explicit separation of duties: the authorisation server holds the client registration and issues the tokens, the resource server checks the token and the object, and the gateway is the enforcement point between them. The profile closes the three failure modes that a plain OAuth deployment leaves open — a token replayed from another client, an authorisation request tampered with in the browser, and a client that authenticates with a shared secret — which matters here because a partner instruction, a result and a bid are the whole commercial relationship with that firm. OWASP API1 object-level authorisation stays where the object lives: the gateway scopes the call and rwb-partner still refuses another partner's instruction, lot or document.

Two operational facts size the edge. NFR-003 sets about 50 partner users online in the busiest hour, of about 320 named users across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers, so the gateway carries a small concurrent population and the design effort belongs in the controls, not in throughput. NFR-063 requires partner-facing screens on desktop browsers and tablets, so the edge keeps a modern protocol surface and a browser-based flow with no client-side installation. NFR-056 then sets the gate in front of the opening: penetration testing and a security review are completed before the first production release and before the partner portal opens to users outside the bank.

### 3. Preconditions

- The DMZ network zone exists with its own subnets, routing, address plan and ingress point, separate from the zone of the shared App Gateway. The zone layout, the subnet sizes and the firewall pair are Not specified in the source documents (GAP-1395; ASM-2431).
- The gateway product and its hosting are chosen: an API gateway product that terminates TLS and mTLS, enforces the profile at the token and request level and supports the client registry of section 11. The product, its version and its placement are Not specified in the source documents (GAP-1395; ASM-2431).
- The bank's external identity path for partner users exists and offers a second factor at sign-in. The identity provider product and the federation protocol used for a partner identity are Not specified in the source documents (GAP-1395; ASM-2431).
- The FAPI 2.0 Security Profile, final February 2025, is the profile in force, with pushed authorisation requests, sender-constrained access tokens, strong client authentication and the token and refresh rules the profile fixes (Arch v5 slide 35).
- The rwb-partner contract is in force for the operations the gateway exposes (section 12.2): the partner portal operations of `/partner/v1/*` belong to rwb-partner (S9) and rwb-debtsale (S6) by the Ownership Map, and their contract stories publish them. The gateway proxies them and republishes none.
- The certificate authority and the trust anchors of the bank are available, so a partner client certificate can be issued, rotated and revoked.
- The SOC logging path is available: audit and PII records leave the DMZ through the bank's PII logging path to the SOC, as the architecture shows for the shared platform.
- A security review slot and a penetration test window are booked before the partner portal opens to partner users outside the bank (NFR-056).
- No approval is needed to start: the story is Day 1 by rule and its status is Draft (realignment v1) (Template and Rules §R5.7).

### 4. Flow

1. Register the partner client: create the client entry with its partner id, its scopes, its certificate thumbprint and its validity window, and leave it in REGISTERED.
2. The partner user opens the partner portal sign-in page. The gateway redirects the browser to the bank's external identity path, where the partner identity is authenticated with a second factor.
3. The client pushes its authorisation request to the pushed authorisation request endpoint and receives a request reference; the browser is sent to the authorisation endpoint with that reference and no authorisation parameters of its own.
4. The authorisation endpoint validates the request reference once, resolves the partner user and the roles of that partner, and asks the partner user to consent to the requested scopes.
5. The authorisation code returns to the registered redirect address. The client exchanges it at the token endpoint with strong client authentication over mTLS and receives an access token sender-constrained to its certificate, with the lifetime of section 11.
6. The client calls a partner portal path of section 12.2 with the access token and its certificate.
7. The gateway validates the certificate, the token binding, the scope and the route, and forwards the call to rwb-partner over mTLS with a workload identity, carrying the partner id and the granted scopes and nothing else.
8. rwb-partner authorises the object and answers. The gateway writes one audit record and returns the answer unchanged; a partner never sees an internal host name, an internal path or a stack trace.
9. On a schedule, certificates are rotated inside their overlap window and clients are reviewed annually; on a partner exit, an incident or a key compromise, the client is suspended and then revoked.
10. Before the portal opens to partner users outside the bank, the penetration test and the security review are completed, and their record is attached to the opening decision (NFR-056).

### 5. Exception paths

| ID | Trigger | What happens | Response | Covered by |
|---|---|---|---|---|
| X1 | The caller presents no client certificate, or a certificate that does not chain to a trust anchor | The TLS handshake is refused at the DMZ edge and no HTTP request reaches rwb-partner | TLS alert; no upstream call | AC6 |
| X2 | The client is revoked or suspended | The token endpoint and every resource call are refused before any upstream call | 401 with MSG-PLT-N007-01 | AC6 |
| X3 | The access token is expired or has been revoked | The call is refused and the client must push a new authorisation request | 401 with MSG-PLT-N007-01 | AC2 |
| X4 | The token is presented without the certificate it is bound to, or from another client | The binding check fails and the call is refused | 401 with MSG-PLT-N007-03 | AC2 |
| X5 | The scope of the token does not include the operation | The gateway refuses before the upstream call and names the missing scope | 403 with MSG-PLT-N007-04 | AC4 |
| X6 | A refresh is attempted: by a browser partner client that holds no refresh token, or with a refresh token that is expired, replayed or not bound to the certificate | The refresh is refused and the client must push a new authorisation request; the refusal is logged against the client | 400 with MSG-PLT-N007-02, or 401 with MSG-PLT-N007-03 when the binding fails | AC2 |
| X7 | An authorisation request arrives without a pushed request reference, or the reference is replayed | The authorisation is refused and the replay is logged against the client | 400 with MSG-PLT-N007-02 | AC2 |
| X8 | The client exceeds its rate limit, or sends a body over the size limit | The request is refused at the edge; a rate-limited client receives a retry hint and an oversized body receives no upstream call | 429 with MSG-PLT-N007-05; 413 | AC5 |
| X9 | A WAF rule matches, or the request is malformed at the protocol level | The request is refused, the rule id and the client id are logged, and the payload is not written to the log | 403 with an incident reference; 400 | AC5 |
| X10 | rwb-partner is down, times out, or answers outside the agreed contract | The gateway returns a problem detail of the platform envelope and never a stale answer or an internal error page | 503 with MSG-PLT-N007-06; 504 on the timeout | AC5 |
| X11 | The audit stream cannot be written | The gateway refuses the request rather than serve it unaudited, and the alert fires to the SOC | 503 with MSG-PLT-N007-06 | AC5 |
| X12 | A certificate rotation fails: the new certificate is not accepted before the old one expires | The client is suspended at the rotation deadline, the alert fires, and the previous certificate is restored only if it is still inside its validity window | 401 with MSG-PLT-N007-01 | AC6 |
| X13 | A partner user's identity has no active partner user record, or an ambiguous partner | The sign-in completes at the identity provider and the gateway refuses the authorisation | 403 with MSG-PLT-N007-04 | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency: the DMZ zone, the profile and the owner contracts are preconditions, and the story provisions and configures the edge without changing a service |
| Negotiable | The zone layout, the gateway product, the identity provider and the numeric limits are settled with the security design authority; the profile, the deny-by-default rule and the pen-test gate are fixed |
| Valuable | Gives REQ-ACA-012, REQ-S9-008 and RWB-E2-019 a place to be enforced, and gives the partner work of Epics 4, 5 and 6 an entry point |
| Estimable | One DMZ zone, one gateway, one authorisation server configuration, one client registry, one WAF policy, one logging pipeline, one runbook and one test gate |
| Small | One sprint for the platform team to stand the zone and the profile up, with the conformance suite and the negative tests |
| Testable | Every criterion is a configuration assertion, a conformance run, a negative request or a recorded review, not a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Partner gateway in the DMZ with the FAPI 2.0 security profile, fronting rwb-partner only

  Background:
    Given the partner gateway sits in its own DMZ network zone and fronts rwb-partner only
    Given the public partner path is /partner/v1/* and the gateway maps it to the base of the service that owns the operation
    Given the FAPI 2.0 Security Profile, final February 2025, is the profile in force

  Scenario: AC1 A separate DMZ gateway with deny-by-default ingress (new, D-RCV-60)
    Given the ingress policy of the partner gateway and the ingress policy of the staff App Gateway
    When the two policies are compared
    Then they sit in different network zones with different ingress addresses and different certificate chains
    Then the only upstream route of the partner gateway is rwb-partner
    Then the six partner portal paths of section 12.2 are the only paths that match a route
    Then no route exists to gateway-bff, to any other Recovery service, to the ACE database, to Kafka or to Temporal
    When a partner calls an unlisted path, an unlisted method or a traversal form of a listed path
    Then the gateway answers 404 or 405 and the request never leaves the DMZ
    Then a scan from the DMZ zone reaches no service port other than the rwb-partner ingress

  Scenario: AC2 The FAPI 2.0 profile is enforced at the edge (new, D-RCV-60)
    Given a registered confidential client with a valid certificate
    When it starts an authorisation
    Then it must first push the authorisation request and present the returned request reference, and a request without one is refused with MSG-PLT-N007-02
    Then the access token is sender-constrained: it is bound to the client certificate over mTLS, and the same token from another certificate or with no certificate is refused with MSG-PLT-N007-03
    Then client authentication is strong, by private_key_jwt or mTLS as the profile fixes, and a client secret alone is refused
    Then no access token, refresh token or authorisation code appears in a query string or a fragment, and a request that carries one is refused
    Then the access token lifetime is 5 minutes (ASM-2431) and a browser partner client receives no refresh token
    Then a call after the lifetime answers 401 with MSG-PLT-N007-01 and requires a new pushed request and a new authorisation

  Scenario: AC3 Multi-factor sign-in and one partner user per identity (new, D-RCV-60)
    Given a partner user at the partner portal sign-in page
    When the partner user authenticates through the bank's external identity path
    Then a second factor is required before any token is issued
    Then a sign-in that stops before the second factor issues no token and answers 401
    Then the external identity maps to exactly one partner user record of rwb-partner with the roles of that partner
    Then an identity with no active partner user record, or an identity that resolves to two partners, is refused with MSG-PLT-N007-04
    Then the partner id and the partner user id are the only identity claims the gateway forwards

  Scenario: AC4 Scope at the edge and object authorisation in the owner (new, D-RCV-60)
    Given an access token issued for one partner with its permitted operations
    When the call reaches the gateway
    Then a token whose scope does not include the operation is refused at the edge with MSG-PLT-N007-04 and no upstream call is made
    Then an allowed call is forwarded with the partner id and the granted scopes and with no other identity claim
    When a partner asks for another partner's instruction, result, invoice, lot or document
    Then rwb-partner or rwb-debtsale authorises the object and answers 403 or 404 with no data
    Then the gateway never derives a partner id, a lot id or a case id from the request body alone

  Scenario: AC5 Edge protection and a PII-safe audit trail (new, D-RCV-60)
    Given the WAF policy, the per-client rate limits, the request size limits and the audit pipeline of the gateway
    When a request matches a WAF rule
    Then it is refused with 403 and an incident reference, and the rule id and the client id are logged without the payload
    When a client exceeds its rate limit or sends a body over the size limit
    Then the answer is 429 with a retry hint or 413, and no upstream call is made
    Then every request writes one audit record with the client id, partner id, partner user id, path, method, status, latency and correlation id
    Then no audit record, log line or trace holds an access token, a refresh token, a client secret, a certificate private key or personal data beyond the partner user id
    Then the audit and PII stream reaches the SOC through the bank's PII logging path, and a failed write is alerted and refuses the request with MSG-PLT-N007-06
    Then the same policy and the same answers hold for a desktop browser profile and a tablet browser profile (NFR-063)

  Scenario: AC6 The client registration and certificate lifecycle (new, D-RCV-60)
    Given the client registry of the gateway
    When a client is registered
    Then its entry carries the client id, partner id, certificate thumbprint, scopes, status, valid from and valid to
    Then it starts in REGISTERED and becomes ACTIVE only after a conformance call with its certificate and a valid token succeeds
    Then a certificate is valid for 12 months (ASM-2431) and rotation succeeds inside an overlap window without a failed call
    Then a revoked client and an expired certificate are both refused with 401 and never reach rwb-partner
    Then revocation takes effect on the thumbprint check immediately and on any cached decision within 30 days at the latest (ASM-2431)
    Then a client whose annual review is not recorded by its review date is suspended with MSG-PLT-N007-01 until the review is entered

  Scenario: AC7 The penetration test and security review gate the opening (new, D-RCV-60)
    Given the security review and the penetration test of the DMZ gateway
    When the partner portal is about to be opened to partner users outside the bank
    Then the penetration test report and the security review record exist and are attached to the opening decision
    Then the opening is blocked while a high or critical finding is open and not accepted by a named role
    Then the record names the gateway version, the FAPI 2.0 profile version, the test window and the scope tested, including the authorisation server, the client registry and the upstream hop
    Then the same gate is repeated before the first production release (NFR-056)
```

These criteria are new and test only the deliverable in the title: the DMZ gateway, its profile controls, its client lifecycle and its opening gate. No legacy acceptance criterion is repeated, and no business value is invented; the capacities come from NFR-003, the opening gate from NFR-056 and the device surface from NFR-063.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The partner gateway sits in its own DMZ network zone, separate from the shared App Gateway, and partners come only through it | Arch v5 slide 35 (edge: shared App Gateway with WAF; partners only through the partner gateway, FAPI 2.0) |
| BR2 | Ingress is deny by default and allow by explicit route: the only allowed upstream is rwb-partner, and no route reaches gateway-bff, another service, the database, Kafka or Temporal | Arch v5 slides 8 and 20 (partners do not use gateway-bff); zero trust per NIST SP 800-204 |
| BR3 | The FAPI 2.0 Security Profile (final February 2025) is mandatory and not negotiable per client: pushed authorisation requests, sender-constrained access tokens over mTLS, strong client authentication, short-lived access tokens and no token or secret in a URL | Arch v5 slide 35 |
| BR4 | A partner user signs in with multi-factor authentication through the bank's external identity path, and one external identity maps to one partner user with the roles of that partner | REQ-ACA-012; Epic 2 RWB-E2-019 |
| BR5 | Data moves through the partner portal and the external gateway and not by email, so the gateway is the only partner channel and no mail relay path is opened for a partner | REQ-S9-008 |
| BR6 | The edge authorises the scope and never the object: rwb-partner and rwb-debtsale authorise the object on every call, so a partner sees only its own work | Arch v5 slide 10 (OWASP API1 object-level authorisation); OWASP API Top 10 |
| BR7 | Every request is audited with the client, the partner and the partner user; no token, secret, key or personal data beyond the partner user id is written to a log, a trace or an audit record | Arch v5 slide 35 (audit and monitoring; PII logging to SOC); NFR-053 |
| BR8 | A client is onboarded, activated, suspended, revoked, rotated and reviewed on a recorded lifecycle, and a revoked client or an expired certificate is refused | Arch v5 slide 35; ASM-2431 |
| BR9 | The gateway carries about 50 partner users online in the busiest hour of about 320 named users, and a partner-facing surface works on desktop browsers and tablets | NFR-003; NFR-061; NFR-063 |
| BR10 | The gateway is not opened to partner users outside the bank until the penetration test and the security review are passed and recorded | NFR-056 |

### 9. State transitions

**Partner client states**

| From | Trigger | Condition | To | HTTP result at the edge |
|---|---|---|---|---|
| (none) | Client registered with a partner id, scopes and a certificate thumbprint | The certificate chains to a trust anchor and the partner is admitted | REGISTERED | 201 on the registration |
| REGISTERED | Conformance call made with the certificate and a valid token | The token is bound to the certificate and the scope matches | ACTIVE | 200 on the conformance call |
| REGISTERED | Conformance call fails | The certificate, the binding or the scope does not match | REGISTERED | 401 with MSG-PLT-N007-01 or 403 with MSG-PLT-N007-04 |
| ACTIVE | Partner or security suspends the client on conduct, incident or an overdue review | The suspension is recorded with a reason | SUSPENDED | 401 with MSG-PLT-N007-01 on the next call |
| SUSPENDED | Suspension lifted and the review recorded | The reason is closed | ACTIVE | 200 on the next conformance call |
| SUSPENDED | Review date passes without a lift | The deadline is reached | REVOKED | 401 with MSG-PLT-N007-01 |
| ACTIVE | Partner exits, key is compromised, or the annual review is refused | The decision is recorded | REVOKED | 401 with MSG-PLT-N007-01; tokens withdrawn |
| REVOKED | Any call | Terminal state; a return needs a new registration | REVOKED | 401 with MSG-PLT-N007-01 |

**Access token states**

| From | Trigger | Condition | To | HTTP result at the edge |
|---|---|---|---|---|
| (none) | Token issued at the token endpoint after a pushed request and a multi-factor sign-in | Strong client authentication passes and the certificate binding is set | ISSUED | 200 at the token endpoint |
| ISSUED | First resource call | The certificate matches the binding and the token is inside its lifetime | ACTIVE | 200 from rwb-partner |
| ISSUED | Resource call without the certificate, or with another certificate | The binding check fails | ISSUED (refused) | 401 with MSG-PLT-N007-03 |
| ACTIVE | Resource call inside the 5-minute lifetime | The binding and the scope hold | ACTIVE | 200 from rwb-partner |
| ACTIVE | Lifetime ends | The expiry instant passes | EXPIRED | 401 with MSG-PLT-N007-01 |
| ACTIVE | Client revoked, partner suspended or token withdrawn | The registry says the client may no longer act | REVOKED | 401 with MSG-PLT-N007-01 |
| EXPIRED | Resource call | The token is past its lifetime; a browser partner holds no refresh token | EXPIRED (refused) | 401 with MSG-PLT-N007-01; a new pushed request and authorisation are needed |
| REVOKED | Any call | Terminal state | REVOKED | 401 with MSG-PLT-N007-01 |

The two machines are the whole runtime state of the edge. No case, instruction, lot or bid state is held here: those belong to rwb-partner and rwb-debtsale and are unchanged by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the DMZ zone, the gateway, the certificate authority integration, the DR setup and the runbook |
| The security architect (security design authority) | Owns the FAPI 2.0 profile configuration, the client authentication method, the token lifetimes and the certificate lifecycle, and signs the security design decision |
| SCB IT security | Runs or commissions the penetration test and the security review, records the findings and blocks the opening while a high or critical finding is open |
| The SOC | Receives the audit and PII stream, owns the alerting on it and owns the incident handling of a blocked or rate-limited client |
| The rwb-partner service owner | Owns the operations behind the gateway, approves a change to a partner path and keeps the object authorisation in the service |
| The rwb-debtsale service owner | Owns the data room and bid operations the gateway exposes to buyers |
| The ACE platform team | Owns the shared App Gateway, the PII logging path and the workload identity platform the gateway uses |
| The partner and agency manager | Requests the onboarding, the suspension and the exit of a partner; the onboarding policy itself is S9 business and outside this story |
| No delegation of authority level applies | The gateway carries no credit decision; it carries the partner's own request to the service that decides |

Roles appear as role codes and partner ids only. No personal name, no email address and no credential appears in a configuration, an audit record or a test fixture; the partner user appears as a partner user id.

### 11. Data

No business data sits at the edge. The gateway holds three things: the client registry, token metadata and the audit record.

| Item | Content | Written by |
|---|---|---|
| Client registry entry | Client id, partner id, certificate thumbprint, scopes, status, valid from and valid to, review date, registration and suspension reasons | The client registration step |
| Token metadata | Token reference, client id, partner id, partner user id, granted scopes, issued at, expiry, binding thumbprint, state | The authorisation server and the gateway |
| Audit record | Correlation id, client id, partner id, partner user id, path, method, status, latency, WAF rule id or error code, decision (allow, refuse, rate-limited) | The gateway on every request |
| Personal data | The partner user id only. No name, no address, no identity number, no contact point, no document content, no account number, no case detail | None |
| Secrets | No client secret, no refresh token, no private key and no access token is stored in a log, a trace, an audit record or a configuration file; a reference to the key store is stored instead | The key store |

The client registry is the only durable store of the gateway and it is platform metadata, not a business record. Token metadata is short-lived and never leaves the edge. Audit records go to the SOC through the bank's PII logging path and are retained under the bank's security-logging retention rule, which is outside this story.

The numeric settings — the token lifetime, the refresh rules, the certificate validity, the revocation propagation, the rate limits, the body size limit and the WAF rule set — are Not specified in the source documents (GAP-1395; ASM-2431); the values this story tests against are the ones in the recorded assumption, and they are fixed in the security design authority review rather than in a service configuration.

### 12. Contract

**12.1 REST operations provided**

None. The partner gateway is shared platform and publishes no REST operation of its own. The partner operations a partner calls are published by the rwb-partner contract (S9) and the rwb-debtsale contract (S6), and the gateway proxies them under the public path of section 12.2; it republishes none of them and adds no field to a request or a response.

**12.2 REST operations consumed**

The gateway consumes the partner portal surface on behalf of the partner and exposes it on the public path `/partner/v1/*` of Arch v5 slide 17. The public form is the architecture path; the gateway maps it to the base path of the owner, so a partner never sees an internal base.

| Public path (FAPI 2.0) | Owner | Owner operation the gateway maps to | Purpose |
|---|---|---|---|
| GET /partner/v1/partner/instructions | S9 rwb-partner | GET /api/recovery/partner/v1/partner/instructions | List the instructions placed with the caller's firm |
| POST /partner/v1/partner/instructions/{instructionId}/accept | S9 rwb-partner | POST /api/recovery/partner/v1/partner/instructions/{instructionId}/accept | Accept or decline an instruction |
| POST /partner/v1/partner/instructions/{instructionId}/results | S9 rwb-partner | POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results | Record a result with its documents |
| POST /partner/v1/partner/instructions/{instructionId}/invoices | S9 rwb-partner | POST /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices | Submit a fee invoice |
| GET /partner/v1/partner/data-room/{lotId} | S6 rwb-debtsale | GET /api/recovery/debtsale/v1/partner/data-room/{lotId} | Read the lot tape and documents for an admitted buyer |
| POST /partner/v1/partner/data-room/{lotId}/bids | S6 rwb-debtsale | POST /api/recovery/debtsale/v1/partner/data-room/{lotId}/bids | Submit a bid on a lot |

The six operations are the partner portal rows of the Epics 3 to 8 operation table, and their owners are the Ownership Map owners: S9 for the four instruction operations, S6 for the two data room and bid operations. The document content a partner downloads is the claim-check content of rwb-document (P5, `GET /documents/{documentId}/content`): the gateway forwards the request that rwb-partner issues, it does not become a document server, and a partner never reaches rwb-document directly. The exact mapping of each public path to the owner's base is a gateway configuration, and the internal base is never returned to a partner.

**12.3 Events published**

None. The edge publishes no Kafka event: it writes an audit record and, through the bank's PII logging path, a PII log record. The partner events `rwb.partner.InstructionIssued.v1` and `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1` belong to rwb-partner and are published by its stories, not by the gateway.

**12.4 Events consumed**

None. The gateway reacts to no event. A client suspension or a revocation is a registry change that the gateway reads at the next call, not an event subscription.

**12.5 Workflows and activities**

None. No Temporal workflow, activity, signal or task queue is created by this story; the partner work behind the gateway runs on the `rwb-partner` task queue of rwb-partner.

**12.6 Schedules**

None. No Temporal Schedule is declared. The certificate rotation, the annual client review and the revocation sweep are platform schedulers of the gateway, outside Temporal.

**12.7 Tables owned**

None. The gateway creates no table in any `rwb_*` schema and reads none. The client registry is a platform store of the gateway, described in section 11, not an ACE database table.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| rwb-partner contract fake (S9) | The four instruction operations of section 12.2 | The conformance and negative tests of this story, and the end-to-end run of RWB-ITG-E2019-ITG |
| rwb-debtsale contract fake (S6) | The two data room and bid operations | The conformance and negative tests, including the cross-partner object refusal |
| Mock external identity provider | The partner sign-in, the second factor and the identity-to-partner-user mapping | The multi-factor and mapping tests of AC3 and TC-PLT-N007-INF-03 |
| Mock certificate authority | Certificate issue, rotation, expiry and revocation | The lifecycle tests of AC6 and TC-PLT-N007-INF-06 |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided by the edge | Consumed by the edge | Notes |
|---|---|---|---|
| REST | 0 operations of its own | Six partner portal operations exposed, four to rwb-partner and two to rwb-debtsale | FAPI 2.0 profile; mTLS; one hop; 2 s timeout with a circuit breaker per upstream |
| Kafka | 0 | 0 | No topic is produced or consumed; the audit path is the bank's PII logging path |
| Temporal | 0 | 0 | The partner workflows belong to rwb-partner |
| File | 0 | 0 | A partner document download is a forwarded claim-check call; the upload link is the rwb-document link rwb-partner issues |

### 13. Solution plan

**Deliverables.** The DMZ network zone and its firewall policy (ingress and egress, deny by default); the gateway deployment with its route table; the authorisation server configuration with the pushed authorisation request endpoint; the client registry; the certificate authority integration and the mTLS trust anchors; the WAF policy and the rate and size limits; the audit and PII logging pipeline to the SOC; the workload identity and mTLS configuration of the upstream hop; the certificate rotation, the annual review and the revocation sweep; the DR configuration; the runbook; the conformance suite and the negative test set; the penetration test and security review record.

**Pattern application.** None of the §R5.5 DP markers applies to this new platform story. It names no legacy table, no `recovery_svc` login, no old topic name, no in-process call, no scheduler and no screen of the monolith, so the DP table adds no row and no dependency. DP-19 (screen, ace-web) belongs to the staff edge (RWB-PLT-N001-CON) and is deliberately not applied here: a partner screen is served through the partner portal and never through a gateway-bff composite route. DP-13 (the `/api/recovery/<short>/v1` base) is applied by the owner services whose operations this gateway proxies; the gateway itself keeps the public partner path of Arch v5 slide 17.

**Build steps**

1. Create the DMZ network zone, its subnets, its routing and its firewall policy: one ingress from the partner network, one egress to the rwb-partner ingress, and no other egress.
2. Deploy the gateway in the zone and write the route table: the six partner portal paths of section 12.2, each mapped to its owner's base, with no wildcard route and no default route.
3. Configure the authorisation server: the pushed authorisation request endpoint, the sender-constrained token binding to the client certificate, strong client authentication, the 5-minute lifetime, the refresh rules and the refusal of a token or secret in a URL.
4. Wire the external identity path: the sign-in redirect, the second factor, the identity-to-partner-user mapping and the refusal of an unmapped or ambiguous identity.
5. Build the client registry and the lifecycle jobs: registration, activation, suspension, revocation, the 12-month certificate rotation, the annual review and the 30-day revocation propagation.
6. Apply the edge protection: the WAF rule set, the per-client rate limits and the request size limits, with the refusal answers of section 5.
7. Build the audit and PII pipeline to the SOC and the fail-closed rule when it cannot write; prove that no token, secret or personal datum appears in it.
8. Configure the upstream hop: TLS and mTLS to rwb-partner with a workload identity, a 2 s timeout and a circuit breaker, and the 503 and 504 answers of the platform envelope.
9. Configure DR for the zone and the gateway, write the runbook (client onboarding, suspension, revocation, rotation, incident and DR), and run the conformance and negative suites against the fakes of section 12.8.
10. Run the penetration test and the security review, record the findings and their closure, and attach the record to the opening decision.

**Done when.** The zone exists with deny-by-default ingress and the only route to rwb-partner, the FAPI 2.0 conformance suite passes, every negative case of section 5 answers as stated, the client lifecycle and the certificate rotation are proven with their negative tests, the audit stream reaches the SOC with no secret and no personal data, the DR runbook is exercised once, and the penetration test and security review record is attached to the opening.

### 14. Validation and messages

| ID | When | Message | HTTP |
|---|---|---|---|
| MSG-PLT-N007-01 | The certificate is missing, expired or revoked, or the token is expired or withdrawn | A valid client certificate and a valid access token are required. | 401 |
| MSG-PLT-N007-02 | A pushed authorisation request is missing, replayed or malformed | This client must push the authorisation request before it authorises. | 400 |
| MSG-PLT-N007-03 | The access token is not bound to the certificate presented | The access token is not valid for this client certificate. | 401 |
| MSG-PLT-N007-04 | The scope is missing, the partner user is not mapped, or the object belongs to another partner | You cannot perform this operation. | 403 |
| MSG-PLT-N007-05 | The per-client rate limit is exceeded | Too many requests. Try again in {seconds} seconds. | 429 |
| MSG-PLT-N007-06 | rwb-partner is unavailable or the audit path cannot be written | The partner service is temporarily unavailable. Try again later. | 503 |

These are platform messages of the edge; each carries a correlation id and never a token, a secret, a personal datum or an internal host name. The sign-in failures of the identity provider keep the messages of the bank's identity path and are not rewritten here.

### 15. Screens and states

No screen belongs to this story: the gateway renders nothing and returns the answer of the owner. What a partner sees is the partner portal served by rwb-partner — the instruction list, the instruction detail with accept and decline, the result entry with its documents, the invoice submission, the data room of a lot and the bid form — and the gateway only controls whether that page and its calls are reachable.

The states the edge puts in front of those screens are: the sign-in redirect to the bank's external identity path; the second-factor challenge; the authorised session, with the token lifetime of section 11 and a re-authorisation when it ends; the session-expired state, where the next call answers 401 and the portal sends the partner back to sign-in; the access-denied state, where an unmapped partner user or a missing scope answers 403; and the temporarily-unavailable state, where an upstream failure answers 503 and the portal shows a retry. The surface works on a desktop browser and a tablet browser (NFR-061, NFR-063); the gateway therefore keeps a modern TLS and HTTP surface and a redirect flow that needs no client-side installation.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N007-INF-01 | AC1 | Integration | A route and port scan from the DMZ zone: only the rwb-partner ingress is reachable; each of the six paths matches; an unlisted path answers 404 and an unlisted method 405; no route to gateway-bff, another service, the database, Kafka or Temporal |
| TC-PLT-N007-INF-02 | AC2 | Contract | The FAPI 2.0 conformance suite: a pushed request is required and its reference is single use; a sender-constrained token is accepted only with the bound certificate; a client secret alone is refused; a token in a query string is refused; the token expires at 5 minutes; no refresh token is issued to a browser partner client |
| TC-PLT-N007-INF-03 | AC3 | Integration | The mock external identity provider: second factor satisfied and not satisfied; an identity with no active partner user; an identity that resolves to two partners; the claim set forwarded to rwb-partner |
| TC-PLT-N007-INF-04 | AC4 | Integration | Two partners with overlapping instructions and lots against the rwb-partner and rwb-debtsale fakes: a cross-partner object call answers 403 or 404 with no data; a missing scope is refused at the edge with no upstream call recorded |
| TC-PLT-N007-INF-05 | AC5 | NFR | A WAF rule hit, the per-client rate limit at its configured value, a body over the size limit, a full audit record compared field by field, a secret and personal-data scan of the audit stream and the traces, the fail-closed answer when the audit path is down, and the same answers from a desktop browser profile and a tablet browser profile |
| TC-PLT-N007-INF-06 | AC6 | Component | The client lifecycle from REGISTERED to ACTIVE to SUSPENDED to REVOKED; a rotation inside the overlap window; a revoked client and an expired certificate refused with 401 and no upstream call; the revocation sweep inside 30 days; a client suspended at its review date |
| TC-PLT-N007-INF-07 | AC7 | NFR | The penetration test report and the security review record: the opening is blocked with an open high finding, released when it is closed or accepted by role, and the record names the gateway version, the profile version, the window and the scope tested |

### 17. Guardrails

- A partner never reaches gateway-bff, another Recovery service, the ACE database, Kafka or Temporal. The only upstream route is rwb-partner and the policy is deny by default.
- The FAPI 2.0 controls are not optional per client and are not relaxed for a partner that finds them hard: pushed authorisation requests, sender-constrained tokens over mTLS, strong client authentication and short-lived tokens apply to every client.
- No token, refresh token, secret or private key in a log, a trace, an audit record or a URL. A correlation id is the handle, never the credential.
- No personal data at the edge beyond the partner user id, and no business data at all: no instruction, result, invoice, lot, bid or document content is stored by the gateway.
- TLS everywhere and mTLS on the upstream hop, with a workload identity in place of a static credential.
- Least-privilege scopes per operation and per partner, and object authorisation stays in rwb-partner and rwb-debtsale, never in the gateway.
- A revoked client, an expired certificate and a suspended partner are refused before any upstream call, and the refusal is audited.
- The penetration test and the security review gate the opening to partner users outside the bank; a high or critical finding that is open keeps the portal closed to them.
- One partner identity, one partner user and one partner: an ambiguous mapping is refused rather than guessed.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Test cases |
|---|---|---|---|
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases | Program, 5.4 | TC-PLT-N007-INF-02, TC-PLT-N007-INF-03, TC-PLT-N007-INF-04 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email | Program, 5.9 | TC-PLT-N007-INF-01, TC-PLT-N007-INF-02 |
| NFR-003 | About 50 partner users online in the busiest hour, of about 320 named users across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers | Program, 6.1 | TC-PLT-N007-INF-05 |
| NFR-056 | Penetration testing and a security review before the first production release and before the partner portal opens to users outside the bank | Program, 6.9 | TC-PLT-N007-INF-07 |
| NFR-063 | Partner-facing screens work on desktop browsers and tablets | Program, 6.11 | TC-PLT-N007-INF-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-ITG-E2019-ITG | Integration | I: partner identities end to end through this gateway, the end-to-end carrier of Epic 2 RWB-E2-019 and of the app story RWB-S9-E2019-APP |
| RWB-S9-E6033-CON, RWB-S9-E6029-CON | Contract | C: the rwb-partner contract for instructions and results and for partner firms and users; the gateway proxies it and publishes no partner operation |
| RWB-S6-E5026-CON, RWB-S6-E6004-CON | Contract | C: the rwb-debtsale contract for the buyer data room and for buyer bids, the two operations the gateway exposes to buyers |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON | App development, Contract | The staff edge, separate from this one: gateway-bff routes and their contract, which a partner never uses |
| RWB-PLT-N006-INF | Infrastructure | Sibling in the same epic: the session store of the staff edge, which this gateway does not use |

### 19. Out of scope

- gateway-bff, its routes, its session store and its composite screens: the staff edge is RWB-PLT-N001-APP and RWB-PLT-N001-CON, and it is a separate zone and a separate trust boundary.
- The partner business logic: the instruction, accept and decline, result, invoice, data room and bid behaviour belongs to rwb-partner and rwb-debtsale.
- The operations and the data of rwb-partner and rwb-debtsale, including their schemas, their events, their tables and their object authorisation.
- The partner onboarding policy: panel admission, terms, conduct, suspension and exit as a business decision belong to rwb-partner (S9) and the partner and agency manager; this story executes a suspension, it does not decide one.
- The external identity provider itself and its federation: the bank's identity path is a precondition and its product is recorded as Not specified in the source documents (GAP-1395; ASM-2431).
- The partner portal screens and their rendering: they are the UI of rwb-partner; this story only controls reachability, the session states and the device surface.
- The rwb-document content service and its claim-check store (P5), which the gateway forwards to but never replaces.
- The DMZ network design details, the gateway product choice and the numeric security settings, which are recorded as Not specified in the source documents (GAP-1395; ASM-2431) and fixed in the security design authority review before the penetration test.
