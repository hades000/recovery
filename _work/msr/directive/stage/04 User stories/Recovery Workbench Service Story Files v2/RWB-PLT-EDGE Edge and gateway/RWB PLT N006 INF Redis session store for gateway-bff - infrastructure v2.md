# RWB-PLT-N006-INF Redis session store for gateway-bff

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N006-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EDGE |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N006 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EDGE-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-PLT-N006-INF-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-PLT-N001-CON |
| Contract version | Not specified in the source documents (DOR-RWB-PLT-N006-INF-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-PLT-N006-INF-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-EDGE, legacy key N006. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 5 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the Redis session store that gateway-bff uses for authenticated staff sessions — a managed, private, zone-redundant store with TLS, credentials in Key Vault, the 15-minute idle expiry set at the store, capacity and failover for the peak staff load, monitoring and a tested rebuild — provisioned and operated in the ACE subscription and network**, so that **the shared edge can hold one opaque session per signed-in user from Day 1, without a new platform, without a database, and without a single business or personal value at the edge**.

The store is shared platform, not one of the 19 services. The shared platform of the target architecture is gateway-bff with its Redis session, Temporal shared with ACE, the Kafka business-event topics, the bank scheduler and observability (Arch v5 slide 4). gateway-bff is a Spring Cloud Gateway and keeps the session in Redis (Arch v5 slides 8 and 27). The browser holds an opaque session cookie with a 15-minute idle timeout (Arch v5 slide 33), and sign-in is the ACE Common sign-in with Entra ID and MFA at the shared gateway-bff (Arch v5 slide 35). The gateway's own OUT contract states the boundary this story has to provision: Redis holds sessions only and no business data (Arch v5 slide 33).

What this story delivers is therefore narrow and complete: a store, its network placement, its credentials, its keyspace and expiry, its size and failover, its dashboards and alerts, its rebuild runbook and the evidence that it holds nothing but sessions. The gateway code, the cookie and the route contract belong to RWB-PLT-N001-APP and RWB-PLT-N001-CON, and this story does not change either of them.

### 2. Business rationale

The edge is where every staff user meets Recovery, so the session store is on the path of every screen. Three properties of the target design make it a Wave 0 item. First, the browser never receives a token it can read: it holds an opaque cookie, and the gateway resolves that cookie to a session in the store. A store that is slow, full or unreachable is therefore a sign-in failure for every user, not a degraded tab. Second, the 15-minute idle timeout is a stated security control of the shared sign-in layer, so the expiry has to be enforced at the store as well as at the gateway; a key that outlives the timeout is a control failure, not a performance issue. Third, the privacy rule of the platform is that personal data is masked and encrypted inside the owning service and never carried in events or workflow payloads; the same rule applied to the edge means the session store holds an identifier for the user and nothing of the case.

Capacity is small but not zero. NFR-002 sets about 370 staff users online in the busiest hour of 914 named users, and NFR-020 and NFR-021 set 99.9 percent in business hours and 99.5 percent outside them. A session record of a few kilobytes for 370 users is a few megabytes, so the design question is not throughput but availability, failover and the behaviour when the store is lost: a lost session must cost the user a sign-in and nothing else, because no business value was ever in the store. That is what makes the failover and rebuild criteria testable and cheap.

The story also closes a realignment risk. In the monolith the session lived inside the application that also held the data; splitting the service boundary must not recreate that coupling at the edge by parking a case snapshot, a cached customer record or a document pointer in Redis. Section 11, section 17 and AC3 fix that boundary while the store is new, before any screen is built on it.

### 3. Preconditions

- The shared platform decision is fixed and unchanged: Recovery runs in the same ACE AKS cluster and behind the same Azure App Gateway as ACE Collection, and gateway-bff with its Redis session is part of the shared platform, not one of the 19 services (Arch v5 slides 4, 7 and 8).
- The subscription, the virtual network, the private DNS zone and the Recovery namespace of the shared cluster exist and the platform team can create a private endpoint and a managed data service in the ACE subscription (Arch v5 slides 7 and 8).
- The Key Vault of the platform exists and the workload identity of gateway-bff holds the read grant on the secrets of this story (Arch v5 slide 8, "Key Vault · codec server").
- The gateway's session contract is published and fixed at version v1 by RWB-PLT-N001-CON: the opaque cookie, the 15-minute idle timeout, the 401 behaviour and the redirect to the ACE Common sign-in. This story provisions what that contract consumes and does not restate it.
- The no-business-data rule is accepted by this story and by the gateway story: the store holds sessions only, and no case, customer, account, document, decision or payment value is written to it (Arch v5 slide 33).
- The security baseline of the platform applies: TLS on every listener, deny by default, no shared administrative credential and no secret in a manifest, an image or a log (Arch v5 slide 35; NIST SP 800-204 zero trust).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), because it provisions infrastructure and builds nothing on another story.

### 4. Flow

1. Record the sizing input from the requirements: the peak of about 370 staff sessions of NFR-002, the record of section 11, and the resulting memory, so that the tier choice is arithmetic and not opinion.
2. Provision the store in the ACE subscription and the ACE region, in the same virtual network as the AKS cluster, with public network access disabled and a private endpoint in the Recovery subnet.
3. Create the private DNS record and the network rule that admits only the gateway-bff workload identity in the Recovery namespace; every other namespace, service and address range is refused.
4. Configure TLS with the bank certificate, require it on every listener, disable the non-TLS port if the product offers one, and record the cipher policy with the security architecture.
5. Put the credential in Key Vault, grant the workload identity read-only access to it, and wire the gateway to read it at run time; verify that no manifest, ConfigMap or image carries it.
6. Set the session keyspace: one key per session, the fields of section 11, a time to live of 15 minutes refreshed on each authenticated call, and the eviction policy of section 13.
7. Turn on the metrics, the dashboard and the alerts of section 13, and route the alerts to the platform on-call rota with the store name, region and environment as labels.
8. Test: a plain-text connection is refused, an unauthenticated connection is refused, an off-namespace connection is refused, a key expires after the idle timeout, the peak load fits with headroom, one node and one zone are lost, and a credential is rotated.
9. Rehearse the rebuild from the runbook, time it, and hand the store over to the gateway story and to the platform rota with the runbook, the dashboard and the alert list.

### 5. Exception paths

| ID | Trigger | What happens | What the user or the operator sees | Covered by |
|---|---|---|---|---|
| X1 | The store is unreachable when a request arrives | The gateway cannot resolve the cookie, so it cannot authenticate the request; the call answers 401 and the browser is sent to the ACE Common sign-in. No cached business answer is served in place of the session | A sign-in page, not a screen with a stale case | AC6 |
| X2 | The primary node fails and the replica takes over | The client reconnects to the promoted node through the same private endpoint; the session survives the failover, and the gateway retries the call within its own timeout | The screen loads after the retry, or a single retry by the user | AC4 |
| X3 | The store reaches the memory warning threshold or an eviction occurs | The alert fires to the platform on-call rota before users are signed out; an eviction of a live session is treated as an incident, because the configured policy is no eviction | An operator alert; the user sees a sign-in only if the eviction happened | AC4, AC5 |
| X4 | The credential is rotated in Key Vault | The gateway reads the new credential on its rotation cycle, the old one is accepted until the end of the overlap window, and a failed read raises an alert instead of a silent sign-in failure | Nothing, if the rotation succeeds; a sign-in failure and an alert if it does not | AC2 |
| X5 | A zone is lost | The store fails over to the standby zone inside the availability target and the sessions of the lost zone at that moment are signed out; no business value is lost because none was held | At worst a re-sign-in for the users in flight at that second | AC4, AC6 |
| X6 | A key outlives the idle timeout beyond the configured bound | The sweep is treated as a control failure: the expiry is corrected at the store, the finding is raised to security architecture, and the test of AC3 fails until it passes | An operator finding, not a user message | AC3 |
| X7 | A business or personal value is found in a key | The key is removed, the writer is identified from the trace, the gateway is corrected under RWB-PLT-N001-APP, and the finding is raised to the data steward | An operator finding; no business value is left at the edge | AC3 |

The source supports the first statement of X1 without qualification: a session loss forces re-authentication (Arch v5 slide 33, opaque cookie with a 15-minute idle; slide 35, sign-in at the shared gateway-bff). What a screen that was already loaded shows when a later call returns 401 is fixed by the gateway and the screen stories, not by this store.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions and operates infrastructure; builds nothing on another story and needs no code change |
| Negotiable | The product, the tier, the zone and region placement, the eviction policy and the absolute session lifetime are agreed at the platform infrastructure review; the private endpoint, TLS, Key Vault, the 15-minute idle expiry and the sessions-only boundary are fixed |
| Valuable | Gives gateway-bff a working session store on Day 1 and gives every staff screen a sign-in path from the first sprint |
| Estimable | One managed store, one private endpoint, one credential, one keyspace, one dashboard, one alert set, one runbook and six acceptance criteria |
| Small | Fits one sprint with provisioning, the negative tests, the failover test and the rebuild rehearsal |
| Testable | Every criterion is tested against the provisioned store, its settings and its metrics, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Redis session store for the shared gateway-bff

  Background:
    Given gateway-bff is the shared Spring Cloud Gateway of the Recovery Workbench and runs in the Recovery namespace of the shared ACE AKS cluster
    Given the browser holds an opaque session cookie with a 15-minute idle timeout and sign-in is the ACE Common sign-in (Entra ID, MFA)

  Scenario: AC1 The store is provisioned in the ACE subscription and network with private access only and TLS required (new, D-RCV-60)
    Given the session store of this story
    When its network settings are reviewed
    Then it sits in the ACE subscription, in the ACE region and in the same virtual network as the AKS cluster
    Then public network access is disabled and the only route to it is a private endpoint in the Recovery subnet with its private DNS record
    Then only the gateway-bff workload identity in the Recovery namespace holds a credential, and a connection from another namespace, another service or another address range is refused
    Then every listener requires TLS with a bank certificate, and a plain-text connection is refused

  Scenario: AC2 The credential is held in Key Vault, rotated and never written to a manifest or a log (new, D-RCV-60)
    Given the store credential and the access key
    When the deployment configuration of gateway-bff is reviewed
    Then the credential is read at run time from Key Vault through the workload identity
    Then no key, password or connection string appears in a manifest, a ConfigMap, an image, a repository or a pipeline log
    When the credential is rotated in Key Vault
    Then the gateway picks the new credential up on its rotation cycle without a redeploy, and the old credential stops working at the end of the overlap window
    Then no log line, metric label or trace attribute carries the credential, and the rotation is exercised once and timed in the runbook

  Scenario: AC3 The keyspace holds sessions only and the 15-minute idle expiry is enforced at the store (new, D-RCV-60)
    Given the session keyspace of gateway-bff
    When a session is written
    Then one key holds the session id, the user id, the role codes, the issued time, the last-seen time and the idle expiry, and nothing of the business
    Then the idle expiry is 15 minutes, held as a time to live on the key and refreshed by the gateway on each authenticated call
    When a key is not touched for 15 minutes plus the configured sweep bound
    Then the key is gone, and the next call with that cookie answers 401 and redirects to the ACE Common sign-in
    Then no key holds a case number, a customer name, an account number, a document, a decision or any other business value, and a scan of the keyspace in the test environment finds none

  Scenario: AC4 The store carries the peak staff sessions and survives the loss of one node or one zone (new, D-RCV-60)
    Given the peak of about 370 staff users online in the busiest hour of the 914 named users (NFR-002)
    When a load test opens that many concurrent sessions with the session record of section 11
    Then every session is held and the memory used stays below the warning threshold with at least 50 percent headroom
    Then the eviction count stays zero, because the configured policy is no eviction
    When one node fails
    Then the sessions continue on the surviving node and the gateway call succeeds within its retry
    When one availability zone is lost
    Then the store fails over to the standby zone inside the availability target applied to it, and only the sessions in flight at that moment are signed out
    When memory reaches the warning threshold or one eviction occurs
    Then the alert reaches the platform on-call rota before a user is signed out

  Scenario: AC5 The store is on the dashboard and alerts the platform on-call rota (new, D-RCV-60)
    Given the dashboard of this story
    When it is opened
    Then it shows the latency of the session read and the session write, the connected client count, the memory used and available, the eviction count, the cache hit ratio and the failover state
    Then every series carries the store name, the region and the environment as labels
    Then an alert fires to the platform on-call rota on latency above the threshold, memory above the threshold, a non-zero eviction count, a failover, a refused connection and a failed authentication
    Then no metric label, log line or trace attribute carries a session id, a user id or any personal data

  Scenario: AC6 A store loss forces re-authentication only and the rebuild is tested and timed (new, D-RCV-60)
    Given the store is lost, emptied or rebuilt
    When a user calls the gateway with the old cookie
    Then the gateway answers 401 and redirects to the ACE Common sign-in
    Then after sign-in the case, the customer and the documents are intact, because none of them was in the store
    Then no business table, event or workflow payload is read or written by the store, and the recovery restores sessions and nothing else
    When the rebuild procedure of the runbook is rehearsed
    Then the rebuild completes without a restore from a backup, the elapsed time is recorded against the recovery time objective of the platform, and the runbook names who performs each step and what the user sees

  Scenario: AC7 The store meets the business rules BR1 to BR8 of section 8 (new, D-RCV-60)
    Given the store, its keyspace and the gateway-bff deployment configuration of this story
    When the store is reviewed against the business rules of section 8
    Then the store has no schema rwb_*, no topic, no task queue and no REST base of its own (BR1)
    Then no key holds a business value, and the only personal value is the user id, with no name, email address, account number, national identifier or document (BR2, BR3)
    Then the idle expiry is 15 minutes, held as a time to live refreshed on each authenticated call (BR4)
    Then the store credential belongs to gateway-bff alone, and no person holds a shared administrative credential (BR5)
    Then every listener uses TLS, private access only with deny by default, and the store is never reachable from the public internet (BR6)
    Then no secret is in a manifest, an image, a repository or a log, and the credential is read from Key Vault through the workload identity (BR7)
    Then the store is never the system of record and is never backed up as one, and a lost session costs one sign-in and nothing more (BR8)
```

These seven criteria are new and test only the deliverable in the title: the store, its access, its credential, its keyspace, its capacity and failover, its observability, its rebuild and its business rules. No legacy acceptance criterion is repeated here and no business value is asserted.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The session store is shared platform, not one of the 19 services: it has no schema `rwb_*`, no topic, no task queue and no REST base of its own | Arch v5 slide 4; Template and Rules §R4 |
| BR2 | The store holds sessions only and no business data; no case, customer, account, document, decision or payment value is written to a key | Arch v5 slide 33, gateway-bff OUT contract |
| BR3 | The only personal value in the store is the user id; a name, an email address, an account number, a national identifier or a document is never written | Arch v5 slide 35, data layer; Template and Rules §R7.2 s17 |
| BR4 | The idle expiry is 15 minutes and is enforced at the store as a time to live, refreshed on each authenticated call | Arch v5 slides 33 and 35 |
| BR5 | One login per schema and one identity per workload: the store credential belongs to gateway-bff alone and no person holds a shared administrative credential | Arch v5 slide 35; DP-02 |
| BR6 | TLS on every listener, private access only, deny by default; the store is never reachable from the public internet | Arch v5 slides 7, 8 and 35 |
| BR7 | No secret in a manifest, an image, a repository or a log; the credential lives in Key Vault and is read through the workload identity | Arch v5 slide 8; Template and Rules §R7.2 s17 |
| BR8 | A lost session costs one sign-in and nothing more: the store is never the system of record and is never backed up as one | Arch v5 slide 33; NFR-022 and NFR-023 follow the ACE recovery objectives |

### 9. State transitions

None in the store itself: the store has no business state machine and no record is approved, closed or reopened here. What the store has is a key lifecycle, driven by gateway-bff and by the expiry the store enforces. It is described here so that the tests of AC3 and AC6 have something to assert.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | Sign-in completes at the ACE Common sign-in | The gateway writes the key with the idle expiry | Created |
| Created | First authenticated call | The key is read and the idle expiry is refreshed | Active |
| Active | Each authenticated call | The idle expiry moves forward by 15 minutes | Active |
| Active | No call for 15 minutes | The store reaches the time to live of the key | Idle expired |
| Active | The store is full and an eviction happens | The configured policy is no eviction, so this path is an incident and not a normal transition | Evicted |
| Active, Idle expired or Evicted | Sign-out, or the key is removed on purpose | The gateway deletes the key at sign-out; the cookie is cleared in the browser | Removed |
| Idle expired or Removed | A call arrives with the old cookie | The key is absent and the gateway cannot authenticate the request | Absent, with 401 and the redirect to sign-in |
| Absent | Sign-in completes again | A new key is created with a new session id | Created |

The transition owner is gateway-bff in every row: this story provisions the store, the time to live and the policy, and it never writes a key itself. The absolute lifetime of a session, beyond the idle expiry, is Not specified in the source documents (GAP-1392; ASM-2428).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the store, the private endpoint, the keyspace settings and the runbook |
| ACE platform team | Owns the ACE subscription, the virtual network, the private DNS zone and the shared cluster; admits the store and its endpoint into the platform |
| Security architecture | Approves the network placement, the TLS policy, the credential handling, the 15-minute expiry and the sessions-only boundary |
| Key Vault owner | Owns the vault, the secret name and the read grant of the gateway workload identity |
| Data steward | Confirms that no key carries personal data beyond the user id and no key carries a business value |
| Platform on-call rota | Receives the alerts of section 13 and runs the runbook |
| gateway-bff owners (RWB-PLT-N001-APP and RWB-PLT-N001-CON) | Consume the store; they state the fields and the expiry they need and they never change a store setting directly |

The tier, the memory, the zone and region placement, the availability target of the store, the absolute session lifetime, the eviction policy, the maximum number of concurrent sessions, the persistence and backup choice, the RPO and RTO and the product are Not specified in the source documents (GAP-1392; ASM-2428). They are agreed at the platform infrastructure review before wave 0 exit, and section 13 carries the assumption that is in force until then.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Keyspace | One keyspace for gateway-bff sessions; one key per session, keyed by the session id that the opaque cookie carries | BR2 |
| Session record fields | Session id, user id, role codes, issued at, last seen, idle expiry, and the encrypted ticket to the ACE Common sign-in where the gateway needs one | BR2, BR3 |
| Personal data | The user id only; no name, no email address, no account number, no national identifier, no document and no contact detail | BR3 |
| Business data | None. No case, customer, account, document, decision, payment or partner value is written to a key (Arch v5 slide 33) | BR2 |
| Value size | About 8 KB per session, taken as the sizing unit of section 13 | None |
| Idle expiry | 15 minutes, sliding, refreshed by the gateway on each authenticated call, held as a time to live on the key (Arch v5 slides 33 and 35) | BR4 |
| Absolute lifetime | Not specified in the source documents (GAP-1392; ASM-2428) | None |
| Encryption | TLS in transit on every connection; at-rest encryption of the managed service as the platform default; the payload keys of the codec server are not used by this store | BR6, BR7 |
| Persistence | Off, because no business value is held; the record is rebuilt by a new sign-in and never restored from a backup | BR8 |
| Retention | A key lives no longer than the idle expiry plus the configured sweep bound; there is no archive, no export and no read replica for reporting | BR4 |
| Peak volume | About 370 concurrent staff sessions from NFR-002, of 914 named users; the resulting footprint is a few megabytes, so the sizing question is availability and not volume | None |
| Access | The gateway-bff workload identity only, read and write on its own keys; no person reads the store by hand, and an operator session is a break-glass action with a recorded reason | BR5 |

The store holds no field that a source does not define and no field that a business rule needs. Where the gateway needs a value the sources do not name — the absolute lifetime and the ticket format — the record carries the placeholder and the change waits for the gap to close; the ticket itself stays encrypted and never leaves the session key.

### 12. Contract

**12.1 REST operations provided**

None. The store is a data service and publishes no REST operation; the gateway's public paths (`/api/recovery/cases/{caseId}` and the rest of its surface) are published by RWB-PLT-N001-CON and carry no service segment of their own.

**12.2 REST operations consumed**

None direct. The store has exactly one client, gateway-bff, and it speaks the Redis protocol over TLS and not REST. The REST operations the gateway consumes — the ACE Common sign-in and the owner services — are published and consumed in RWB-PLT-N001-CON and are not restated here.

**12.3 Events published**

None. No session fact is published to a topic: a session start, a session expiry and a sign-out are gateway events and are not business facts; the authorization and audit evidence of a sign-in comes from the ACE Common audit and PII logging path, not from this store (Arch v5 slide 7).

**12.4 Events consumed**

None. The store reacts to no event; the expiry is a time to live and the access policy refresh of the gateway is a cache concern of RWB-PLT-N001-APP and RWB-P4-E1037-CON.

**12.5 Workflows and activities**

None. No Temporal workflow, activity or signal touches the session store; a session is not a workflow and a sign-in is not a saga.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job is created here; the expiry is enforced by the store and not by a sweep job of this story.

**12.7 Tables owned**

None in the ACE PostgreSQL schemas. The store is Redis, sessions only, and this story creates or reads no `rwb_*` table, no view and no login; the only login it creates is the store credential in Key Vault (BR5, DP-02 applied to a platform credential and not to a database schema).

**12.8 Contract fakes**

None. The store has no service contract to fake; the gateway's route surface is faked by RWB-PLT-N001-CON, and this story's tests run against a throwaway store of the same product and settings.

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No HTTP surface; the gateway's paths belong to RWB-PLT-N001-CON |
| Kafka | 0 | 0 | A session never travels on a topic |
| Temporal | 0 | 0 | No workflow, activity or Schedule |
| File | 0 | 0 | No file is read or written |
| Data store | 1 (Redis, sessions only) | None | One keyspace, one client, TLS only, 15-minute idle time to live, no persistence |

The summary is five lines and not four because the store itself is the call type of this story: one managed data store with one client and no business data.

### 13. Solution plan

**Deliverables.** The store and its private endpoint as code (the resource definitions of the platform toolchain), the private DNS record and the network rule, the Key Vault secret and the read grant, the gateway connection profile (host, port, TLS, credential reference), the keyspace and expiry configuration, the dashboard and the alert rules, the rebuild and rotation runbook, and the test evidence of section 16.

**Settings in force**

| Setting | Value |
|---|---|
| Product | A managed Redis service in the ACE subscription; whether it is Azure Cache for Redis or the bank's shared Redis service is Not specified in the source documents (GAP-1392; ASM-2428) |
| Tier and memory | Not specified in the source documents (GAP-1392; ASM-2428); the smallest tier that offers zone redundancy is sufficient, because the footprint is about 4.4 MB |
| Zone and region | The ACE region, with zone redundancy across the availability zones of that region; the exact zone and region placement is Not specified in the source documents (GAP-1392; ASM-2428) |
| Availability target | Not specified for the store itself; the availability of the service it serves is 99.9 percent in business hours and 99.5 percent outside them (NFR-020, NFR-021) |
| Private access | A private endpoint in the Recovery subnet, a private DNS record, public network access disabled, and a network rule that admits the gateway-bff workload identity only |
| TLS | Required on every listener with a bank certificate; a plain-text connection is refused |
| Authentication | The store credential from Key Vault, read by the gateway workload identity; no person holds a shared administrative credential |
| Keyspace | One key per session under a prefix per environment; the record of section 11 |
| Idle expiry | 15 minutes, sliding, refreshed by the gateway on each authenticated call |
| Absolute lifetime | Not specified in the source documents (GAP-1392; ASM-2428) |
| Memory sizing | Peak concurrent sessions × 8 KB plus 50 percent headroom: 370 × 8 KB is about 2.9 MB, and about 4.4 MB with the headroom |
| Eviction policy | No eviction; an eviction is an incident and not a normal path |
| Persistence | Off, because the store holds no business data and a loss costs a sign-in |
| Backup and restore | No backup is taken as a business record; the recovery is a rebuild, rehearsed and timed |
| Monitoring | Latency, connected clients, memory, evictions, hit ratio, failover state and authentication failures, labelled by store, region and environment |
| Alerts | Memory warning, non-zero eviction, latency above the threshold, failover, refused connection and failed authentication, to the platform on-call rota |
| Patching | The managed maintenance window of the platform, outside business hours, with the failover expected and alerted |
| Runbook | Provision, rotate, fail over, rebuild, verify and break-glass, each step with its owner role |

**Pattern application.** None of the decoupling-pattern markers of Template and Rules §R5.5 appears in this new platform story: it introduces no legacy table, no legacy login, no legacy topic name, no legacy task queue and no legacy API base, so no DP row is applied and the metadata row "Patterns applied" reads None. The two patterns the edge does exercise are applied by the stories that own them: DP-13 (the service base path, for the routes the gateway serves) and DP-19 (screen, ace-web to gateway-bff composite route) sit in RWB-PLT-N001-CON and RWB-PLT-N001-APP.

**Build steps**

1. Provision the store from the resource definitions with the region, the zone redundancy, the private endpoint and public access disabled.
2. Create the private DNS record and the network rule; verify from the Recovery namespace that the endpoint resolves and connects, and from another namespace and from outside the virtual network that it does not.
3. Enable TLS on every listener, install the bank certificate, and prove that a plain-text connection is refused.
4. Write the credential to Key Vault, grant the workload identity read-only access, and wire the gateway connection profile to the secret reference.
5. Apply the keyspace configuration: the record of section 11, the 15-minute idle time to live and no eviction.
6. Turn on the metrics and the dashboard, write the alert rules, and route them to the platform on-call rota with the labels of section 13.
7. Run the negative tests: plain text, no credential, another namespace, another address range, an expired key refreshed, and a keyspace scan for business values.
8. Run the capacity test at the NFR-002 peak with the 8 KB record and confirm the headroom and a zero eviction count.
9. Run the failover test for one node and one zone, and record the observed outage and the sessions lost.
10. Rotate the credential once, then rehearse the rebuild, time it, write the runbook and hand the store over.

**Done when.** The store exists in every environment with the settings of section 13, the four negative tests fail closed, the peak load of NFR-002 fits with headroom and no eviction, one node and one zone have been lost in a test with the observed outage recorded, the dashboard and the alerts are live on the platform rota, the rotation and the rebuild have been exercised and timed, and the gateway story connects to the store without a code change.

### 14. Validation and messages

| ID | When | Message | Raised to |
|---|---|---|---|
| MSG-PLT-N006-01 | A connection is refused because it is plain text, unauthenticated or from outside the Recovery namespace | The session store refused a connection from {source}: {reason}. Only the gateway identity over TLS is admitted. | Security architecture and the platform rota |
| MSG-PLT-N006-02 | Memory crosses the warning threshold, or one eviction occurs | The session store is at {percent} of its memory and has evicted {count} keys. Sessions will be signed out if the store fills. | Platform on-call rota |
| MSG-PLT-N006-03 | The store fails over, or a node is lost | The session store failed over at {time}. Sessions in flight were signed out and no business data was affected. | Platform on-call rota |
| MSG-PLT-N006-04 | A credential rotation succeeds or fails | The session store credential was rotated at {time}, or the rotation failed and the old credential is still in force. | Key Vault owner and the platform rota |
| MSG-PLT-N006-05 | A key holds a value that is not a session field | A session key carried a value outside the session record. The key was removed and the writer is under investigation. | Data steward and security architecture |

The five message IDs belong to this story; they are operator messages and not business messages, and none of them carries a user id, a session id or a personal value. The message a user sees when a session expires — the redirect to the ACE Common sign-in and the text on it — is owned by RWB-PLT-N001-CON and is not fixed here.

### 15. Screens and states

No screen in this story, and no screen state either. The visible effect of this store on a screen is indirect and limited to two moments: when the session expires, the browser is sent to the ACE Common sign-in, and when a call arrives without a valid session, the gateway answers 401. Both behaviours are fixed by RWB-PLT-N001-CON, not here. What the store contributes to the screen experience is only the speed of the session lookup, which stays inside the screen response target of NFR-008 because it is one lookup on the request path, and the fact that no screen ever reads business data from the edge.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N006-INF-01 | AC1 | Component | The provisioned store in a test environment; public access disabled; a private endpoint and DNS record; a connection from the Recovery namespace succeeds and one from another namespace fails; a plain-text connection is refused |
| TC-PLT-N006-INF-02 | AC2 | Integration | The gateway deployed with the Key Vault secret reference; a scan of manifests, ConfigMaps, images and pipeline logs finds no credential; a rotation is performed and the gateway keeps authenticating, with the old credential refused after the overlap |
| TC-PLT-N006-INF-03 | AC3 | Component | A session written with the fields of section 11; the time to live measured at the store; a key left untouched expires after 15 minutes plus the sweep bound; the next call answers 401; a keyspace scan finds no case, customer, account or document value |
| TC-PLT-N006-INF-04 | AC4 | NFR | A load test at the peak of about 370 concurrent sessions of NFR-002 with the 8 KB record; memory below the threshold with at least 50 percent headroom; zero evictions; one node lost and one zone lost, with the observed outage and the sessions lost recorded |
| TC-PLT-N006-INF-05 | AC5 | Component | The dashboard renders latency, clients, memory, evictions, hit ratio and failover; each alert rule is fired once in a test and reaches the platform rota; a label and log scan finds no session id, user id or personal value |
| TC-PLT-N006-INF-06 | AC6 | Integration | The store emptied with a live cookie; the gateway answers 401 and redirects; the case and the documents are intact after sign-in; the rebuild is rehearsed from the runbook and the elapsed time is compared with the platform recovery time objective |
| TC-PLT-N006-INF-07 | AC7 | Component | The store, its keyspace and the gateway-bff deployment configuration; a review of schemas, topics, task queues and REST bases (BR1); a keyspace scan for business and personal values (BR2, BR3); the idle expiry read as a time to live (BR4); the credential holders listed (BR5); a listener and reachability check (BR6); a secret scan of manifests, images, repositories and logs (BR7); a rebuild with no restore from backup (BR8) |

### 17. Guardrails

- Sessions only at the edge: the store carries no case, customer, account, document, decision, payment or partner value, and a key with one is removed and raised (BR2, AC3, X7).
- No personal data beyond the user id: no name, no email address, no account number, no national identifier and no contact detail is written to a key, a metric label or a log line (BR3).
- TLS everywhere and deny by default: private access only, no public listener, no plain-text port and no connection from a namespace that is not the Recovery namespace (BR6, AC1).
- Secrets in Key Vault and nowhere else: no credential in a manifest, a ConfigMap, an image, a repository, a pipeline log or a runbook example (BR7, AC2).
- No shared administrative credential and no hand access: the store is read and written by the gateway identity, and an operator session is a break-glass action with a recorded reason (BR5).
- Capacity is alerted before eviction: the memory warning fires before a user is signed out, and an eviction is an incident rather than a cache behaviour (AC4).
- Small and replaceable: the store is never a system of record, is never backed up as one, and its loss costs one sign-in (BR8, AC6).
- No business value in configuration: the expiry, the memory threshold and the alert thresholds are platform settings with the sources of section 13 and are never parameters of a business rule.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | What this story provides | Test cases |
|---|---|---|---|---|
| NFR-002 | The system supports the peak number of staff users signed on at once: about 370 staff online in the busiest hour, of 914 named users | Program BRD v4 §6.1 | The memory sizing and the capacity test at that peak, with 50 percent headroom and no eviction | TC-PLT-N006-INF-04 |
| NFR-020 | The Workbench is available during business hours: 99.9 percent | Program BRD v4 §6.4 | Zone redundancy, node failover, a private endpoint inside the platform and alerts before a user is signed out | TC-PLT-N006-INF-04, TC-PLT-N006-INF-05 |
| NFR-021 | Availability outside business hours: 99.5 percent, excluding the change window | Program BRD v4 §6.4 | The maintenance window and the patching path, with the failover expected and alerted | TC-PLT-N006-INF-04, TC-PLT-N006-INF-06 |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts | Program BRD v4 §6.4 (open; follows the ACE recovery point objective) | No business data is held, so the store contributes no data loss; the rebuild is timed against the platform objective | TC-PLT-N006-INF-06 |
| NFR-023 | Recovery time objective: the maximum time to restore service | Program BRD v4 §6.4 (open; follows the ACE recovery time objective) | The rebuild is rehearsed and timed in the runbook, and a lost session costs one sign-in | TC-PLT-N006-INF-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N001-APP | App development | The only client of this store: it writes, reads and expires the session key |
| RWB-PLT-N001-CON | Contract | Publishes the session contract this story provisions against: the opaque cookie, the 15-minute idle timeout and the 401 behaviour |
| RWB-PLT-N007-INF | Infrastructure | Sibling, not a consumer: partners reach Recovery through the separate partner gateway in the DMZ and their sessions never enter this store |
| RWB-P4-E1037-CON | Contract | The authorise contract whose data the gateway caches; the cache is a gateway concern and no permission value is stored in this store |

The two open recovery objectives are the only requirement rows without a target: NFR-022 and NFR-023 are Open in the program BRD and follow the ACE objectives, so this story times the rebuild and states it against the platform objective rather than inventing a number.

### 19. Out of scope

- The gateway code: the session filter, the cookie handling, the route definitions and the composite screens belong to RWB-PLT-N001-APP.
- The session cookie contract: the cookie name, the attributes, the 15-minute idle timeout and the 401 and redirect behaviour belong to RWB-PLT-N001-CON.
- Partner identities and partner sessions: they belong to RWB-PLT-N007-INF and the partner gateway in the DMZ, and they never use this store.
- Any business data at the edge, including a case snapshot, a cached customer record, a document pointer or a permission decision keyed by case.
- The ACE Common sign-in service itself, its Entra ID configuration and its MFA policy; this story only follows the 15-minute idle timeout it sets.
- The ACE PostgreSQL schemas, the `rwb_*` databases and the per-service logins; this store creates no table and no schema login.
- The authorise contract of rwb-access and the access cache the gateway keeps, which belong to RWB-P4-E1037-CON and RWB-PLT-N001-APP.
