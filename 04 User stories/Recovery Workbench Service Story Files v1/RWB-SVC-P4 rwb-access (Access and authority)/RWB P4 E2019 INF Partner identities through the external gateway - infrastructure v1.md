# RWB-P4-E2019-INF Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for rwb-access — the DMZ infrastructure slice that carries the partner identity resolution from the partner gateway to rwb-access: one route, the certificate and key handling, the mTLS and workload identity hop, the network policy and the rate limit. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E2019-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-AM |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-034) |
| Status | Draft (realignment v1) |

### 1. Story

As an **infrastructure and security engineer**, I want **the partner gateway in the DMZ to reach one operation of rwb-access — the partner identity resolution — over a mutually authenticated hop with a workload identity, across a network policy that opens the DMZ to the `rwb-recovery` namespace on that one hop and to nothing else, with the certificate and key handling and the rate limit that hop needs**, so that **a partner identity that the gateway has already authenticated can be turned into Recovery roles without a partner, a token or a database path ever leaving the edge, and without opening a second door into the Workbench**.

This is the rwb-access infrastructure slice of legacy key RWB-E2-019 under epic RWB-SVC-P4. The partner gateway itself is platform work and is delivered by **RWB-PLT-N007-INF**: the DMZ zone, the gateway product, the FAPI 2.0 security profile, the client registry, the certificate lifecycle, the WAF, the audit path and the penetration-test gate all belong to that story. This story cites it and adds only the slice that this legacy key needs, because the resolution call does not exist in the platform baseline:

- **One route.** The partner gateway gets one further upstream, rwb-access, matched on the single resolution path that RWB-P4-E2019-CON fixes, and no other path of rwb-access and no path of any other service.
- **One hop, at authorisation time.** The gateway calls the resolution once per sign-in, at the authorisation step and before a token is issued; every partner portal call after that stays on the rwb-partner route of RWB-PLT-N007-INF. The two routes are siblings: neither calls the other and neither chains.
- **The certificate and key handling of that hop.** The gateway presents a client certificate and a workload identity to rwb-access; the private key stays in the platform key store and never appears in a configuration file, an image or a log.
- **The network policy.** Deny by default from the DMZ into namespace `rwb-recovery`, allowing the rwb-access service port on the resolution path only, with no egress to the ACE database, to Kafka, to Temporal or to another Recovery service.
- **The rate limit.** A per-client limit on the resolution call, so a retry storm at sign-in cannot become a storm on rwb-access.

This story installs no application and changes no business rule. It writes no code of the resolver, it holds no table, it publishes no event, it starts no workflow, and it takes no decision about a partner: it opens one authenticated, rate-limited path and records what crosses it.

### 2. Business rationale

Partners are outside the bank, so the architecture gives them their own edge: a partner gateway in the DMZ with the FAPI 2.0 profile, in a separate trust boundary from the staff App Gateway (Architecture v5 slides 20 and 35). RWB-PLT-N007-INF delivers that edge and fronts rwb-partner for the partner portal. What it does not deliver is the identity question that has to be answered before any partner token is useful: which Recovery role, which scope and which masking policy does this partner identity get. That answer is rwb-access's, on the P4 base, and it needs one authenticated hop from the DMZ into the namespace that hosts the Recovery services.

**The division is fixed and is the same in all three stories of this legacy key.** **RWB-P4-E2019-APP**, **RWB-P4-E2019-CON** and **RWB-P4-E2019-INF** are the rwb-access slice: the resolution and its answer, the contract the gateway calls, and this DMZ plumbing. **RWB-S9-E2019-APP** owns the firm, the partner user, the binding and the instruction, because `partner`, `partner_user` and `partner_instruction` are S9's under the Ownership Map ruling ASM-0072; the gateway resolves those at rwb-partner and supplies them to rwb-access as claims. **RWB-P7-E2019-APP** owns the central ledger entries a partner sign-in and refusal leave behind. **RWB-ITG-E2019-ITG** is the end-to-end proof of the key and carries legacy AC1, AC2, AC3, AC4, AC5, AC7 and AC8; this story proves no business criterion at all.

The alternative is worse than the slice. Without a second upstream, the gateway would have to read the role matrix somewhere else — a copy of the roles at the edge, or a call routed through another service — and both break the architecture: the roles are the access owner's data and are cached, one-hop contracts for every service that authorises (slides 10 and 14), and a call chain deeper than one hop is forbidden (slide 11). Without a scoped network policy, the DMZ would be a second, unowned path into the whole namespace. Without the rate limit, a sign-in retry loop caused by a slow downstream becomes an outage of the service that answers authorisation for all staff screens and all services.

The controls are the ones the architecture already fixes for a partner path: mTLS on every service-to-service call with a workload identity (slide 35), deny by default (NIST SP 800-204), no token or secret in a configuration file or a log (NFR-052), FAPI 2.0 sender-constrained tokens with a short lifetime at the partner edge (RWB-PLT-N007-INF), and the penetration test that gates the opening (NFR-056). The values the tests use come from those sources unchanged: the DMZ zone of RWB-PLT-N007-INF, the namespace `rwb-recovery`, the rwb-access service port, the 2 s client budget, the 5-minute token lifetime of the gateway and the resolution path of RWB-P4-E2019-CON.

What no source fixes is carried as a placeholder rather than invented: the gateway product, the zone subnets and the firewall pair are RWB-PLT-N007-INF's and are not restated; the certificate profile, its lifetime and the rotation window of the rwb-access hop, and the numeric rate limit of the resolution call, are Not specified in the source documents (GAP-0786; ASM-1441) and (GAP-0786; ASM-1442). The story applies the recorded default in each case and moves no business rule.

### 3. Preconditions

- RWB-PLT-N007-INF is delivered: the DMZ network zone, the partner gateway with the FAPI 2.0 profile, the client registry, the certificate authority integration, the WAF, the audit and PII logging path, and the penetration-test gate.
- RWB-P4-E2019-CON is published: the resolution path, its claim set and its answer. This story proxies that one operation and adds no field, no path and no status of its own.
- The `rwb-recovery` namespace exists with the rwb-access service and its port, its service account and its workload identity, as the rwb-access deployment defines them.
- The platform key store is available and holds the private key of the gateway's client certificate for this hop; the trust anchors of the bank and of the ACE platform are available at both ends.
- The DMZ subnet plan, the gateway product and the firewall pair are RWB-PLT-N007-INF's and are taken as given; the address plan of this hop is Not specified in the source documents (GAP-0786; ASM-1441).
- The rwb-access service answers the resolution only when the feature flag `rwb.access.partner-signin` is on; with the flag off the hop is configured and unexercised, and no partner resolves.
- The 2 s client budget and the breaker are the platform standard for a one-hop call (Architecture v5 slide 11, ADR-020); this hop adopts them unchanged.
- The certificate profile of the hop, its lifetime, its rotation window and the revocation propagation are Not specified in the source documents (GAP-0786; ASM-1441).
- The per-client rate limit and its burst on the resolution call are Not specified in the source documents (GAP-0786; ASM-1442).
- No application is installed by this story and no business rule is changed by it: the resolver is RWB-P4-E2019-APP's and the partner facts are RWB-S9-E2019-APP's.
- No build dependency blocks the start: every dependency in the metadata table is empty, because this story configures infrastructure that other stories consume, and it is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The partner gateway of RWB-PLT-N007-INF authenticates a partner user with a second factor and resolves the partner user, the partner id and the partner role against rwb-partner (RWB-S9-E2019-APP).
2. At the authorisation step and before it issues a token, the gateway calls the resolution operation on the rwb-access upstream with its client certificate and its workload identity.
3. The network policy allows the packet from the DMZ to the rwb-access service port in namespace `rwb-recovery` and drops anything else the gateway tries to reach.
4. The rwb-access ingress terminates TLS, checks the client certificate against the trust anchor, checks the workload identity of the caller and passes the call to the resolver.
5. A call without a valid certificate, with an expired certificate, or with a certificate that does not chain to the trust anchor is refused at the ingress and never reaches the resolver.
6. A call from a workload identity that is not the partner gateway's is refused at the ingress with the same 401 shape.
7. The rate limiter counts the call per client and per partner identity. A client over its limit receives 429 with a retry hint and no upstream call is made.
8. The resolver answers roles, the `PLACED` scope, the matrix version, the masking version and the expiry; the gateway carries the answer into the token it issues and into the scope of the partner session.
9. Every call writes one audit record on the gateway side (RWB-PLT-N007-INF's audit path): the client id, the partner id, the partner identity reference, the path, the status, the latency and the correlation id — and no claim value beyond the identifiers, no token and no certificate material.
10. The private key of the hop stays in the platform key store; the gateway reads it by reference at start-up and at rotation, and the key never appears in a configuration map, an image layer or a log line.
11. On rotation, the new certificate is trusted at both ends inside the overlap window, and the old one is removed only after the new one is proven; a failed rotation raises an alert and leaves the previous certificate in place while it is still valid.
12. The hop is configured in every environment before the opening, proven with the resolution fakes of RWB-P4-E2019-CON, and exercised end to end only when the flag is on and the penetration test of RWB-PLT-N007-INF has passed (NFR-056).

### 5. Exception paths

| ID | Trigger | What happens | Response | Covered by |
|---|---|---|---|---|
| X1 | The gateway presents no client certificate | TLS is refused at the rwb-access ingress and no HTTP request reaches the resolver | TLS alert; no upstream call | AC2 |
| X2 | The certificate is expired, revoked or does not chain to the trust anchor | The call is refused at the ingress before any resolver code runs | 401 | AC2 |
| X3 | The workload identity of the caller is not the partner gateway's | The call is refused at the ingress, and the caller identity and the path are logged | 401 | AC3 |
| X4 | The gateway calls a path of rwb-access other than the resolution path, or a port of another service | The network policy drops the packet and the gateway records a connection failure | No response; policy drop logged | AC4 |
| X5 | The gateway reaches for the ACE database, Kafka, Temporal or another Recovery service | The egress policy of the DMZ denies it and the attempt is alerted | Policy drop; alert | AC4 |
| X6 | A client exceeds the rate limit of the resolution call | The call is refused at the edge and no upstream call is made | 429 with a retry hint | AC5 |
| X7 | The rwb-access service is down, times out after 2 s, or answers outside the contract | The gateway returns the platform problem detail and never a stale answer | 503 or 504 | AC5 |
| X8 | The certificate rotation fails at its deadline | The client is suspended at the deadline, an alert fires, and the previous certificate is restored only while it is valid | 401 | AC2 |
| X9 | The platform key store is unreachable at start-up | The gateway does not start the upstream, the alert fires, and no call is made without a certificate | Start-up refusal | AC3 |
| X10 | A configuration map, an image or a log is found to carry a private key, a token or a claim value beyond the identifiers | The pipeline check fails the change and the record is purged under the platform retention rule | Build failure | AC6 |

No exception path of this story changes a partner, a role or a scope: the answer is the resolver's, and a refusal at the edge only means the resolver was never asked.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency: the zone, the gateway and the profile are RWB-PLT-N007-INF's preconditions, and this story configures one route, one policy, one hop and one limit |
| Negotiable | The zone addresses, the certificate profile and the numeric limit are settled with the security design authority; the one-hop rule, the deny-by-default rule and the workload identity are fixed by the architecture |
| Valuable | Makes the resolution reachable from the DMZ without a second door into the namespace, and keeps the key, the token and the partner data at the edge |
| Estimable | One upstream, one route, one certificate pair, one network policy, one rate limit, one audit wiring and one rollback |
| Small | One sprint for the infrastructure team, with the negative tests |
| Testable | Every criterion is a configuration assertion, a negative request or a recorded scan, not a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The DMZ hop from the partner gateway to the rwb-access partner identity resolution

  Background:
    Given the partner gateway of RWB-PLT-N007-INF sits in its own DMZ network zone
    Given rwb-access runs in namespace "rwb-recovery" and answers POST /api/recovery/access/v1/partner-identities/resolve
    Given the platform key store holds the private key of the gateway client certificate for this hop

  Scenario: AC1 One route to the resolution and no other door (new, D-RCV-60)
    Given the route table of the partner gateway for the rwb-access upstream
    When the route table and the ingress policy are reviewed
    Then exactly one route matches, POST /api/recovery/access/v1/partner-identities/resolve
    Then no other path of rwb-access and no path of another service matches the rwb-access upstream
    Then the partner portal paths of rwb-partner stay on the upstream of RWB-PLT-N007-INF and are not duplicated here
    Then the two upstreams are siblings: the resolution route calls no partner portal path and the partner portal route calls no resolution
    Then an unlisted path answers 404 and an unlisted method 405 without leaving the gateway

  Scenario: AC2 The certificate and the key of the hop (new, D-RCV-60)
    Given the client certificate the gateway presents to rwb-access and the trust anchor at the rwb-access ingress
    When the hop is configured in the environment
    Then the certificate chains to the bank trust anchor and names the partner gateway as its subject
    Then the private key is read from the platform key store by reference and appears in no configuration map, image layer or log line
    Then a call with no certificate, an expired certificate or a certificate of another chain is refused at the ingress with 401 and reaches no resolver
    Then the certificate and the trust anchor rotate inside an overlap window, and a failed rotation suspends the client at its deadline with an alert

  Scenario: AC3 mTLS and workload identity on the hop (new, D-RCV-60)
    Given the mTLS policy and the workload identity of the partner gateway
    When the gateway calls the resolution
    Then the call is mutually authenticated: the gateway verifies the rwb-access certificate and rwb-access verifies the gateway certificate
    Then rwb-access accepts only the workload identity of the partner gateway for this operation
    Then a call from another workload identity is refused with 401 and logged with the caller identity and the path
    Then the caller's identity reaches the resolver as a service identity and never as a user token
    Then the 2 s client budget and a breaker sit on the hop, and a timeout answers the platform problem detail

  Scenario: AC4 The network policy from the DMZ into rwb-recovery (new, D-RCV-60)
    Given the egress policy of the DMZ zone and the ingress policy of namespace "rwb-recovery"
    When the policies are applied and a scan is run from the DMZ
    Then the DMZ reaches the rwb-access service port on the resolution path and nothing else in the namespace
    Then the DMZ reaches no other Recovery service, no ACE database port, no Kafka broker and no Temporal frontend
    Then a call to any other path or port is dropped and the attempt is alerted
    Then the policy is deny by default in both directions and names one namespace, one service and one port

  Scenario: AC5 The rate limit of the resolution call (new, D-RCV-60)
    Given the per-client rate limit and its burst on the resolution route
    When a client exceeds the limit
    Then the call is refused with 429 and a retry hint and no upstream call reaches rwb-access
    Then the limit is counted per client and per partner identity and is not shared with the partner portal route
    Then a client inside its limit is not delayed by another client's excess
    Then the refusals are counted on the audit path with the client id and the reason

  Scenario: AC6 No application and no business rule (new, D-RCV-60)
    Given the changes this story applies to the environment
    When the change set is reviewed
    Then it holds route, certificate, trust, policy, rate-limit and audit configuration only
    Then it installs no application, adds no table, publishes no event and starts no workflow
    Then the resolution logic, the refusal vocabulary and the answer stay with RWB-P4-E2019-APP and RWB-P4-E2019-CON
    Then a private key, a token or a claim value beyond the identifiers in a configuration map, an image or a log fails the pipeline check
    Then the change is reversible by restoring the previous route and policy, and the rollback is exercised once
```

These six criteria are new and test only the deliverable in the title: one route, the certificate and key handling, the authenticated hop, the network policy, the rate limit and the absence of an application. No legacy acceptance criterion is repeated, and no business value is invented; the zone, the product and the profile come from RWB-PLT-N007-INF, and the numbers that no source fixes follow the assumptions of section 11.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Partners reach the Workbench only through the partner gateway in the DMZ; this hop is one more upstream of that gateway and is not a second entry point | Architecture v5 slide 35; REQ-ACA-012 |
| BR2 | Every service-to-service call is mutually authenticated with a workload identity and authorised by policy, deny by default | Architecture v5 slide 35; NIST SP 800-204 |
| BR3 | Call depth is one: the gateway calls rwb-access on the resolution and rwb-partner on a partner portal path, and neither call chains to the other | Architecture v5 slide 11; ADR-020 |
| BR4 | The DMZ reaches namespace `rwb-recovery` on the rwb-access port for the resolution path only, and reaches no other service, database, broker or Temporal frontend | Architecture v5 slides 20 and 29; DENY-by-default zone policy |
| BR5 | No token, refresh token, private key, client secret or personal field is held in a configuration file, an image, an environment map or a log; the key is read from the platform key store by reference | NFR-052; ADR-010; Architecture v5 slide 35 |
| BR6 | The hop carries the claim set and the answer of RWB-P4-E2019-CON and adds no field, no path and no status of its own | RWB-P4-E2019-CON; DP-11 |
| BR7 | A client over its rate limit is refused at the edge with a retry hint and no upstream call, so a sign-in retry storm cannot reach the resolver | Architecture v5 slide 10 (breaker and bulkhead per downstream); NFR-050 |
| BR8 | The rwb-access upstream is enabled in an environment only when `rwb.access.partner-signin` is on and the penetration test and security review of RWB-PLT-N007-INF have passed | NFR-056; DL03 |
| BR9 | This story installs no application and changes no business rule: it configures the route, the certificate, the trust, the policy, the limit and the audit wiring only | Template and Rules §R5.4 class X; legacy RWB-E2-019 section 19 |
| BR10 | Every call is audited on the gateway side with the client id, the partner id, the partner identity reference, the path, the status, the latency and the correlation id, and with no token and no certificate material | Architecture v5 slide 35; NFR-042; RWB-PLT-N007-INF BR7 |

### 9. State transitions

**The rwb-access upstream of the partner gateway**

| From | Trigger | Condition | To | Result |
|---|---|---|---|---|
| (none) | The route, the certificate, the trust, the policy and the limit are applied in an environment | The certificate chains and the workload identity is accepted | CONFIGURED | The route answers the resolution; no partner call is possible while the flag is off |
| CONFIGURED | The flag `rwb.access.partner-signin` is turned on after the security gate | The penetration test and the security review of RWB-PLT-N007-INF have passed | ENABLED | A partner sign-in resolves its roles through the hop |
| ENABLED | The flag is turned off | None | CONFIGURED | The next resolution answers 404 and no partner resolves |
| ENABLED or CONFIGURED | The certificate expires or is revoked, or the key is unobtainable | The trust check fails | SUSPENDED | Every call answers 401, the alert fires, and a rotation or a restore is needed |
| SUSPENDED | A new certificate is trusted at both ends inside the overlap window | The new certificate chains and the key is readable | CONFIGURED | The route answers again once the flag is on |
| Any state | The previous route and policy are restored | None | (none) | The upstream is removed and the DMZ has no path to rwb-access |

No partner, role, scope, case or instruction state is held here: the resolution answer is the resolver's, and the partner state machines are rwb-partner's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the DMZ zone integration, the route, the network policy, the certificate installation, the rate limit and the runbook step of this hop |
| The security architect (security design authority) | Owns the certificate profile, the trust anchors, the mTLS policy, the workload identity binding and the numeric limit |
| SCB IT security | Runs the penetration test and the security review of the edge and blocks the enabling while a high or critical finding is open |
| The SOC | Receives the audit stream, alerts on a policy drop, a rate-limit burst or a certificate failure, and owns the incident |
| The rwb-access service owner | Owns the resolver behind the hop, its ingress policy and the workload identity it accepts |
| The rwb-partner service owner (S9) | Owns the partner portal upstream of the same gateway, which this story does not change |
| The ACE platform team | Owns the key store, the certificate authority and the workload identity platform the hop uses |
| No delegation of authority level applies | This story carries no credit decision; it carries one authenticated request |
| No business role is granted or changed here | A role, a scope and a masking version are the resolver's answer, not a configuration of the edge |

### 11. Data

No business data sits in this story. The hop holds configuration and an audit record, and nothing else.

| Item | Content | Written by |
|---|---|---|
| Route entry | The one resolution path, the rwb-access service and port in `rwb-recovery`, the method, the client certificate reference and the enabled state | The route configuration |
| Certificate and trust | The client certificate reference, its subject, its thumbprint, its validity window and the trust anchor reference of the rwb-access ingress | The certificate installation |
| Key reference | A reference to the platform key store entry; no key material, no password and no token | The key store |
| Policy | The egress rule of the DMZ to one namespace, one service and one port, and the ingress rule of the namespace that accepts only that source | The network policy |
| Rate limit | The per-client limit, the burst, the window and the retry hint of the resolution route | The rate-limit configuration |
| Audit record | Correlation id, client id, partner id, partner identity reference, path, method, status, latency, reason of a refusal, decision | The gateway on every call (RWB-PLT-N007-INF's audit path) |
| Personal data | The partner identity reference and the partner id only; no name, contact detail, identity number, document content or case detail | None |

The certificate profile of the hop, its lifetime, its rotation window and the revocation propagation are Not specified in the source documents (GAP-0786; ASM-1441); the per-client limit, its burst and its window are Not specified in the source documents (GAP-0786; ASM-1442); and the namespace, service and port names are taken from the rwb-access deployment rather than fixed here — Not specified in the source documents (GAP-0786; ASM-1443).

### 12. Contract

#### 12.1 REST operations provided

None. The infrastructure publishes no REST operation of its own. The one operation it exposes is rwb-access's, published by RWB-P4-E2019-CON and implemented by RWB-P4-E2019-APP; this story proxies it and adds no field, no path and no status.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/access/v1/partner-identities/resolve | P4 rwb-access | The one upstream this story opens: called by the partner gateway at the authorisation step, before a token is issued, with the claim set of RWB-P4-E2019-CON and with a 2 s client budget and a breaker |

It is one hop. The partner portal calls of the same gateway to rwb-partner are RWB-PLT-N007-INF's and are not changed or duplicated here.

#### 12.3 Events published

None. The edge publishes no Kafka event. The resolution answer is carried in the token and the session of the gateway, and the platform library publishes the decision record on the service side (DP-03).

#### 12.4 Events consumed

None. The route, the certificate, the policy and the limit are configuration read at start-up and at reload, not an event subscription.

#### 12.5 Workflows and activities

None. No Temporal workflow, activity, signal or task queue is created or used by this story.

#### 12.6 Schedules

None. The certificate rotation and the revocation sweep are platform schedulers of the gateway (RWB-PLT-N007-INF), outside Temporal and outside this story.

#### 12.7 Tables owned

None. This story creates no table in any `rwb_*` schema and reads none: `role`, `permission`, `masking_rule` and `role_conflict` are rwb-access's and are read by the resolver behind the hop, and `partner`, `partner_user` and `partner_instruction` are rwb-partner's (ASM-0072). The route, the certificate, the policy and the limit are platform configuration, not an ACE database table.

#### 12.8 Contract fakes

| Fake | Serves | Used by this story |
|---|---|---|
| Resolution fake | `POST /api/recovery/access/v1/partner-identities/resolve` with the resolved answer and the refusal cases of RWB-P4-E2019-CON | The hop's positive and negative tests, including the 401 and the 503 of section 5 |
| Mock certificate authority | Certificate issue, rotation, expiry and revocation for the hop | The certificate lifecycle tests of AC2 |
| rwb-access ingress fake | The TLS and trust check of the rwb-access ingress, and the workload identity acceptance | The mTLS and workload identity tests of AC3 |
| Policy scan fixture | The expected egress and ingress rules and the port scan result | The network policy test of AC4 |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 operations of its own | 1 proxied, the resolution of rwb-access | mTLS with a workload identity, one hop, 2 s timeout with a breaker, per-client rate limit |
| Kafka | 0 | 0 | No topic is produced or consumed by the edge |
| Temporal | 0 | 0 | No workflow and no Schedule |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Deliverables.** The route on the partner gateway for the resolution path; the client certificate and its trust at the rwb-access ingress; the mTLS and workload identity binding of the hop; the egress policy of the DMZ and the ingress policy of `rwb-recovery` for one service and one port; the per-client rate limit and its burst; the audit wiring on the gateway side; the negative test set; the rollback step; and the runbook entry of the hop.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. This story opens no database path at all | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the record is written on the service side, never at the edge | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; no ACE path is opened from the DMZ | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, read by the resolver behind the hop | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, read by the resolver behind the hop | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; this hop reaches the same service and adds no authorise path | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the hop carries the contract of RWB-P4-E2019-CON | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the route matches the P4 base and no other base | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_access`; this story runs no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the staff edge, which this story does not touch and a partner never uses | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule, is class X for the app story, and carries no H and no C of its own.

**What changes from the monolith.** The legacy story reached the partner identity directory from the external gateway through an integration path opened for the whole application, with the resolver, the binding and the firm status in the same process. In the target the edge holds no business logic and one authenticated route; the resolver sits in rwb-access, the partner facts sit in rwb-partner, and the DMZ can reach neither the database nor another service. No new hardware is implied beyond the DMZ zone and the gateway that RWB-PLT-N007-INF already creates: this story adds a route, a certificate pair, a policy and a limit.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `rwb-access-resolve` route | Gateway configuration | The one upstream and the one path, with the method, the certificate reference and the enabled state (BR1, BR6) |
| Hop certificate and trust | Configuration | The client certificate of the gateway, the trust anchor of the rwb-access ingress, and the rotation overlap (BR5) |
| Workload identity binding | Configuration | Accepts only the partner gateway's workload identity on this operation (BR2, BR3) |
| `dmz-to-rwb-recovery` policy | Network policy | Deny by default, one namespace, one service, one port, egress and ingress (BR4) |
| Resolution rate limit | Gateway configuration | Per-client and per-partner limit, burst, window and retry hint (BR7) |
| Audit wiring | Configuration | One audit record per call on the gateway's audit path, with no token and no key (BR10) |
| Rollback step | Runbook | Restores the previous route and policy and removes the upstream (BR9) |

**Configuration.** The certificate profile, the trust anchors, the limit, the burst and the retry hint are configuration read at start-up. The values this story tests against are the defaults of section 11, and they are fixed in the security design authority review of RWB-PLT-N007-INF rather than in a service configuration.

**Build steps**

1. Add the upstream and the one route for the resolution path, and prove that no other path and no other method matches (AC1).
2. Install the client certificate and the trust anchor, prove the chain, and bind the private key by reference from the platform key store (AC2).
3. Configure mTLS and the workload identity on the hop, and prove that another identity is refused with 401 and logged (AC3).
4. Apply the egress policy of the DMZ and the ingress policy of `rwb-recovery`, then run the port scan from the DMZ (AC4).
5. Configure the per-client rate limit, its burst and the retry hint, and prove the 429 with no upstream call (AC5).
6. Wire the audit record on the gateway side and scan the configuration, the image and the logs for a key, a token and a claim value beyond the identifiers (AC6).
7. Prove the negative set of section 5 with the fakes of section 12.8, including a timeout and a 503 of the resolver.
8. Exercise the rotation once inside the overlap window, and the rollback once (AC2, AC6).
9. Record the runbook entry and hand the hop to RWB-P4-E2019-APP's contract test and to RWB-ITG-E2019-ITG as the transport they run over.

**Feature switch.** The upstream is enabled per environment only when the flag `rwb.access.partner-signin` is on and the security gate has passed; with the flag off the route answers 404 and no partner resolves, and the route and the policy may stay in place unexercised.

**Done when.** The one route answers the resolution and nothing else, the certificate chain and the workload identity are proven with their negative cases, the DMZ reaches one namespace, one service and one port, the rate limit answers 429 without an upstream call, the audit record carries no token and no key, the rotation and the rollback have been exercised once, and the penetration test and the security review of the edge record the hop in their scope.

### 14. Validation and messages

| ID | When | Message | HTTP |
|---|---|---|---|
| MSG-PLT-N007-01 | The certificate is missing, expired or revoked, or the token is expired | A valid client certificate and a valid access token are required. | 401 |
| MSG-PLT-N007-03 | The token is not bound to the certificate presented | The access token is not valid for this client certificate. | 401 |
| MSG-PLT-N007-05 | The per-client rate limit of the resolution call is exceeded | Too many requests. Try again in {seconds} seconds. | 429 |
| MSG-PLT-N007-06 | rwb-access is unavailable or the audit path cannot be written | The partner service is temporarily unavailable. Try again later. | 503 |

The four messages are the platform messages of RWB-PLT-N007-INF and are relayed unchanged; this story adds no message of its own and changes no wording. A workload identity that is not the partner gateway's answers 401 with MSG-PLT-N007-01 and no text of its own, and the resolver's own refusals pass through the edge unchanged (MSG-P4-001, MSG-P4-005, MSG-P4-006, MSG-P4-008).

### 15. Screens and states

No screen belongs to this story: the hop renders nothing. What a partner sees is the partner sign-in page and the partner portal of rwb-partner, and the hop only decides whether the sign-in can be completed. The states it puts in front of that page are: the resolved sign-in, where the answer of the resolver is carried into the session; the refused sign-in, where the resolver's 401 or 403 reaches the partner unchanged; the rate-limited state, where MSG-PLT-N007-05 asks for a retry; and the unavailable state, where MSG-PLT-N007-06 asks for a later attempt. The desktop and tablet surfaces are the platform's (NFR-063) and are not changed by this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-INF-01 | AC1 | Integration | The route table of the partner gateway against the resolution fake: the one path matches, an unlisted path answers 404, an unlisted method 405, and no rwb-partner or foreign path is duplicated |
| TC-E2-019-INF-02 | AC2 | Component | The mock certificate authority: a valid chain, an expired certificate, a revoked certificate, a certificate of another chain, the key read by reference, and a rotation inside the overlap window |
| TC-E2-019-INF-03 | AC3 | Integration | The mTLS and workload identity fixture: the partner gateway accepted, another workload identity refused with 401, the caller identity reaching the resolver as a service identity, and a 2 s timeout answering 504 |
| TC-E2-019-INF-04 | AC4 | NFR | The applied policies and a port scan from the DMZ: the rwb-access port reachable, every other Recovery service, the ACE database, Kafka and Temporal unreachable, and each dropped attempt alerted |
| TC-E2-019-INF-05 | AC5 | NFR | The per-client limit at its configured value and the burst above it: a 429 with a retry hint, no upstream call recorded, one client's excess not delaying another, and the refusals counted on the audit path |
| TC-E2-019-INF-06 | AC6 | Component | The change set reviewed for scope, the key, token and claim scan of the configuration, the image and the logs, and the rollback that removes the upstream and restores the previous policy |

No test in this story is an integration copy of a business case: the hop is exercised against the fakes of section 12.8. The eleven legacy cases of RWB-E2-019 are executed by RWB-P4-E2019-APP and RWB-ITG-E2019-ITG — TC-E2-019-06, TC-E2-019-09, TC-E2-019-10 and TC-E2-019-11 in the app story, and TC-E2-019-01, TC-E2-019-02, TC-E2-019-03, TC-E2-019-04, TC-E2-019-05, TC-E2-019-07 and TC-E2-019-08 in the end-to-end proof that runs over this hop — and none is renumbered or restated here.

### 17. Guardrails

- One route, one path, one port: the DMZ reaches the resolution and nothing else, and a policy that opens a second port or a second service fails the review.
- Deny by default in both directions, with the allowed flow named explicitly (NIST SP 800-204).
- No private key, token, refresh token, client secret or password in a configuration map, an image layer, an environment map or a log; the key is a reference to the platform key store (NFR-052, ADR-010).
- No personal data at the edge beyond the partner identity reference and the partner id, and no business data at all: no instruction, no case, no document and no claim value beyond the identifiers.
- The hop is one hop: a route that would make the resolver call another service, or the partner portal call the resolver, fails the review.
- The edge authorises the transport and never the object: the role, the scope and the refusal are the resolver's, and the object authorisation stays with the owner of the object.
- The route is enabled only after the security gate of RWB-PLT-N007-INF has passed and the flag is on, and it is off in PROD until DL03 closes.
- The change is reversible: the previous route and policy are restored by the recorded rollback step, which is exercised once.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4; Program 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR10 | TC-E2-019-INF-01 to TC-E2-019-INF-06 |

| Legacy reference | Where it is kept |
|---|---|
| The external gateway that carries a partner sign-in | Sections 1, 4, 7, 12.2, 13 |
| The partner identity and the firm | RWB-S9-E2019-APP; named only, never read (ASM-0072) |
| The role, the scope and the masking policy of a partner | RWB-P4-E2019-APP and RWB-P4-E2019-CON, behind the hop |
| The record of a partner sign-in and refusal | RWB-P7-E2019-APP; the local record is written through RWB-P4-E1039-APP |
| The gateway platform, the profile and the client lifecycle | RWB-PLT-N007-INF |
| AC6 and AC9 of RWB-E2-019 | Carried verbatim by RWB-P4-E2019-APP |
| AC1, AC2, AC3, AC4, AC5, AC7 and AC8 of RWB-E2-019 | Carried by RWB-ITG-E2019-ITG, which runs over this hop |

The seven criteria of this key that this slice does not own — AC1, AC2, AC3, AC4, AC5, AC7 and AC8 — are carried by **RWB-ITG-E2019-ITG** alone, and no part of them is restated in this story.

### 19. Out of scope

- The partner gateway platform, its DMZ zone, its FAPI 2.0 profile, its client registry, its WAF, its audit pipeline and its penetration-test gate (RWB-PLT-N007-INF).
- The resolution itself, its claim set, its answer, its refusal vocabulary and its record (RWB-P4-E2019-APP and RWB-P4-E2019-CON).
- The firm, the partner user, the binding, the instruction and every partner portal path (`rwb-partner`, S9; RWB-S9-E2019-APP), including the rwb-partner upstream of the same gateway.
- The central decision ledger (rwb-decision, P7; RWB-P7-E2019-APP) and the access-entry writer (RWB-P4-E1039-APP).
- The staff edge, gateway-bff and its session store (RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-N006-INF), which a partner never uses.
- The end-to-end journey of the key and its evidence (RWB-ITG-E2019-ITG).
- The service deployment, the Helm chart of rwb-access, its database and its migrations.
- The DMZ network design details, the gateway product choice and the numeric security settings of the platform, which are recorded as Not specified in the source documents in RWB-PLT-N007-INF and fixed in the security design authority review before the penetration test.
