# RWB-PLT-E1070-CON Temporal platform on the ACE AKS clusters - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1070-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-070 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP04, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-070 for the workflow platform epic; the platform now publishes the namespace, client-identity, frontend API subset, OIDC role mapping and metrics and health contract of namespace rwb-recovery with a fake frontend, so the 19 services build against a frozen platform contract on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the Temporal platform contract, a service team or the platform team**, I want **the namespace, client identity and frontend API contract, the Web UI role mapping, the metrics and health contract and a fake frontend published on Day 1**, so that **the 19 services build and test against one frozen platform contract before the cluster exists**.

This is the contract story of legacy key RWB-E1-070 under epic RWB-PLT-WF. A shared cluster cannot wait for 19 teams to agree names, so the contract fixes, in one versioned document, the namespace `rwb-recovery` and its retention and search attributes, the client certificate profile that identifies a service's workload, the subset of the frontend gRPC API the services may call and the typed errors it may return, the Entra ID role mapping of the Web UI, the metrics and health endpoints the ACE monitoring namespace scrapes, and a fake frontend that answers every one of those declarations without a cluster.

The platform is shared platform, not one of the 19 services: it owns no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base, so this document publishes names and shapes only and never a business model (Template and Rules §R4, §R5.5 DP-13, DP-14). The namespace `rwb-recovery`, its 30-day retention and its four Keyword search attributes are fixed by R4 and Architecture v5. The contract is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 2. Business rationale

In the monolith one process held the workflow state, so the namespace and the certificate were an operational detail nobody had to publish. In the target the engine is shared platform in namespace `rwb-recovery`, one cluster per environment, with the workers living inside each of the 19 services (Architecture v5 slides 23 and 24; Temporal and Drools Design slides 11 and 12). Nineteen teams, four environments and one platform team then have to agree the namespace, the certificate profile, the API subset, the errors, the OIDC roles and the metrics endpoints before the first worker is written, or each team invents its own reading and the cluster is reconfigured per team.

Publishing the contract on Day 1 also protects the two boundaries the design depends on. First, a service reaches Temporal only as a client with its own certificate and its own namespace claim: no shared certificate, no anonymous client, and no cross-namespace call, which is what keeps AC3 of the legacy story meaningful after the split. Second, the platform publishes no business data and no personal-data attribute, so the search attributes stay case codes and queue codes and the payload encryption work stays with the codec-server story. The fake frontend is the instrument that makes this testable before the cluster exists: every service's worker test, every contract test and the integration harness run against the same declarations.

### 3. Preconditions

- The namespace `rwb-recovery`, retention 30 days and the four Keyword search attributes CaseId, Stage, ProductGroup and QueueCode are fixed by Template and Rules §R4 and Architecture v5 (slides 23, 24 and 41); the contract records them and changes none of them.
- The five-layer design fixes L1 and L2 as platform-owned: one cluster per environment, one namespace per workbench, the workflow kit above them (Architecture v5 slide 23; Temporal and Drools Design slide 12).
- The Release is 30 November 2026 (tentative) and is copied unchanged; the contract carries no date of its own.
- The contract is Draft (realignment v1) until the consuming stories pass their contract tests; no approval is required to publish a Draft contract.
- The frontend gRPC port 7233 is reachable only from the cluster network and the worker subnets, and the Web UI only on its internal ingress.
- The ACE internal certificate authority issues the client and server certificates, and the certificates are held in Key Vault.
- The ACE monitoring namespace exists and is the only network source allowed to scrape the platform endpoints.
- The RW-PLATADM and RW-AUDIT roles exist through the environment group (RWB-P4-E1022-CON), and every other Workbench role code is known to the mapping so it can be refused.
- The approved Temporal server and SDK release is not in the read sources: Not specified in the source documents (GAP-1440; ASM-2535).

### 4. Flow

1. The contract author writes the namespace contract: the namespace name, retention in hours and days, the four Keyword search attributes, the refusal of any personal-data attribute, and the rule that a second bootstrap run changes nothing.
2. The author writes the client identity and certificate profile: one client certificate per service workload identity, issued by the ACE internal CA, carrying the namespace claim, with the validity window and the renewal rule.
3. The author writes the frontend API subset and the typed errors: which gRPC calls a service may make, the request and response shapes at the level of names, and the error codes with the condition that produces each.
4. The author writes the Web UI role mapping: RW-PLATADM operates, RW-AUDIT reads, every other Workbench role is refused, and the refusal carries MSG-P4-002.
5. The author writes the metrics and health contract: the two endpoints, their schemes, ports, paths and result codes, and the network source allowed to call them.
6. The author writes the Helm values contract: the value names each environment supplies, with no value of its own beyond the pinned release family, so the app story and the environments fill the same keys.
7. The fake frontend is generated or assembled from the declarations: a Temporal dev server carrying the namespace, the search attributes, test CA certificates and one seeded smoke workflow.
8. The contract test runs the fake against the documents on every change: every declaration answered, every error produced, every refusal proved.
9. The contract is published as v1 to the contract registry; the app story, the worker and SDK story and the 19 services' worker tests pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A client connects with no certificate, an expired certificate or a certificate issued for another namespace, or it names a foreign namespace in the request | The TLS handshake fails for the first two cases and the call is refused with PERMISSION_DENIED for the last two; no workflow is started and the event is in the frontend log with the client identity only | None (TLS); PERMISSION_DENIED |
| X2 | A caller presents a Workbench role other than RW-PLATADM or RW-AUDIT to the Web UI mapping | The mapping refuses the role, no namespace is listed and no workflow is shown | MSG-P4-002 |
| X3 | The namespace bootstrap runs a second time | Nothing changes: the namespace, the retention and the four search attributes stay as declared, and the run is recorded as a no-op | None (idempotent) |
| X4 | A change to the contract breaks a consumer: a renamed namespace, a renamed search attribute, a removed API call or a changed error code | The change raises a new version, marks the current version deprecated, and no consumer sees an edited document | Lint finding, no message id |
| X5 | A value the consumers need is named by no read source (the platform login, the platform admin base, the approved release number) | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1440; ASM-2535) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds no cluster, reads no business data and depends on no other story |
| Negotiable | Document format, example workflow identifiers and the internal layout of the fake are open until the version is frozen; the namespace, the retention, the four search attributes, the API subset and the error codes are fixed |
| Valuable | The 19 services, the worker and SDK story and the platform app story start on Day 1 against one frozen platform contract |
| Estimable | One namespace contract, one client-identity profile, one API subset, one OIDC mapping, one metrics and health contract, one values schema, one fake and one contract test |
| Small | One sprint for the documents, the fake and the contract test |
| Testable | Each criterion in section 7 is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal platform contract for namespace rwb-recovery and the fake frontend

  Background:
    Given the platform is shared platform and owns no schema, no topic and no Workbench REST base
    Given the namespace rwb-recovery is the unit of isolation on one cluster per environment

  Scenario: AC1 The namespace contract is published and a second bootstrap run changes nothing (new, D-RCV-60)
    Given the namespace contract document
    When it is validated against the platform schema
    Then it declares the namespace rwb-recovery
    Then it declares retention 720 hours, 30 days
    Then it declares the search attributes CaseId, Stage, ProductGroup and QueueCode as Keyword
    Then it declares that no search attribute holds a name, a national ID or another personal data field
    When the namespace bootstrap runs a second time
    Then the namespace, the retention and the four search attributes are unchanged

  Scenario: AC2 The frontend API subset and its typed errors are declared (new, D-RCV-60)
    Given the frontend API document
    When it is validated
    Then the allowed calls are StartWorkflowExecution, SignalWorkflowExecution, DescribeWorkflowExecution, ListWorkflowExecutions and GetWorkflowExecutionHistory
    Then every other frontend call is declared out of the subset for a service client
    Then the typed errors are TLS handshake failure, NOT_FOUND, PERMISSION_DENIED, FAILED_PRECONDITION and UNAVAILABLE
    Then each error names the condition that produces it and carries no business value and no personal data

  Scenario: AC3 One client certificate per service workload identity (new, D-RCV-60)
    Given the client identity and certificate profile
    When it is validated
    Then it declares one client certificate per service workload identity, issued by the ACE internal CA, carrying the namespace claim rwb-recovery
    Then it declares the validity window and the renewal rule, and that a certificate is never shared between two services
    When a client connects with no certificate
    Then the TLS handshake fails and no workflow call is served
    When a client connects with an expired certificate
    Then the TLS handshake fails with certificate expired
    When a client connects with a certificate issued for another namespace
    Then the call is refused with PERMISSION_DENIED and no workflow is started

  Scenario: AC4 The Web UI role mapping is published (new, D-RCV-60)
    Given the OIDC role mapping in the contract
    When it is reviewed
    Then RW-PLATADM maps to operate and RW-AUDIT maps to read
    Then every other Workbench role is refused with MSG-P4-002 and no namespace is listed
    Then the mapping names roles only and never a person, an account or an email address

  Scenario: AC5 The metrics and health contract is published (new, D-RCV-60)
    Given the metrics and health contract
    When it is validated
    Then it declares HTTPS GET /metrics on port 9090
    Then it declares HTTP GET /health on port 8080, answering 200 when the service is ready and 503 when it is not
    Then it declares that both endpoints are scraped and probed only from the ACE monitoring namespace and the cluster probe
    Then neither endpoint carries a business value or a personal data field

  Scenario: AC6 The fake frontend answers every declaration and a breaking change raises v2 (new, D-RCV-60)
    Given the fake frontend, a Temporal dev server with the namespace rwb-recovery, test CA certificates and the seeded smoke workflow
    When the contract test runs
    Then every declaration of sections 12 and 14 is answered or refused as declared, including the no-certificate, expired-certificate and foreign-namespace cases
    Then the fake is declared test-only and is never deployed to SIT, UAT or PROD
    Then a breaking change raises v2, marks v1 deprecated, and no consumer sees an edited v1
```

These six criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here; the values they assert are the namespace, retention, search attributes, API calls and error codes the read sources fix, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The namespace is the unit of isolation: one namespace per environment is `rwb-recovery`, with its own retention, certificates and codec keys; a new workbench takes a namespace, not a cluster | Architecture v5 slides 23, 24 and 46; Template and Rules §R4 |
| BR2 | The server release is 1.30 or later, for Nexus and Worker Versioning; the approved release number is recorded in the environment design | Temporal and Drools Design slide 32 item 6; Architecture v5 slide 23 |
| BR3 | The frontend accepts mTLS only: every client presents a certificate from the ACE internal CA that names the namespace, and no anonymous or shared certificate is accepted | Architecture v5 slide 35; Temporal and Drools Design slide 11 |
| BR4 | The Web UI is OIDC only: RW-PLATADM operates, RW-AUDIT reads, every other Workbench role is refused with MSG-P4-002 | Architecture v5 slide 35; RWB-P4-E1022-CON |
| BR5 | The contract carries no service short, no schema name, no topic name and no Workbench REST base; the platform owns none of them | Template and Rules §R4 and §R5.5 DP-13, DP-14 |
| BR6 | The fake is test-only and is never deployed to SIT, UAT or PROD; no environment value points at it | Template and Rules §R7.2 section 12.8 |
| BR7 | A breaking change raises a new version and deprecates the current one; a published version is never edited in place | Template and Rules §R7.2 |
| BR8 | Every value the consumer supplies is configuration: replica counts, node sizes, retention and releases are declared keys with no value baked into the document | REQ-DRI-010; Architecture v5 slide 20 |

### 9. State transitions

The contract has its own lifecycle; the objects it describes have the states below. This story changes no case status.

| Object | From | Event | To |
|---|---|---|---|
| Contract | Draft | The consuming stories pass their contract tests | Published |
| Contract | Published | A consumer pins the version and the change window closes | Frozen |
| Contract | Published or Frozen | A breaking change is accepted | A new version, and the old version is Deprecated |
| Namespace | None | The namespace bootstrap runs once | REGISTERED |
| Namespace | REGISTERED | The bootstrap runs again | REGISTERED, unchanged |
| Client certificate | None | The ACE internal CA issues the certificate | VALID |
| Client certificate | VALID | The validity window ends | EXPIRED, and the handshake fails |
| Client certificate | VALID | The certificate is renewed before expiry | ROTATED, and the new certificate is VALID |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents, the mapping, the fake and the contract test |
| The platform owner of the Temporal layer | Approves a breaking change and a version freeze |
| Security architecture | Reviews the client certificate profile, the namespace claim and the refusal rules |
| The service teams of the 19 services | Read the contract, confirm the calls they need, raise a change request |
| The ACE Common team | Owns the Entra ID sign-in and the app roles the mapping references, and never republishes them |
| No delegation of authority level applies | A platform contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the contract or in an example. Where a caller must be named, the example uses a service workload identity or a role code only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The contract publishes names, shapes, codes and result codes only; no case, customer, account or document value appears |
| Personal data | None, and no search attribute may hold one: CaseId, Stage, ProductGroup and QueueCode are codes |
| Data held by the platform | The two Temporal persistence stores of the app story; their contents are workflow histories and visibility records, not business records |
| Data held by the fake | Synthetic workflow identifiers only: the seeded smoke workflow `platform-smoke-20261116` and the identifiers its test starts; no business data and no personal data |
| Field identifiers | None owned. The platform owns no `rwb_*` field and no ACE field |
| Retention | The namespace retains closed workflows for 30 days, as declared; the contract document itself keeps no data |

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The document declares the gRPC subset of section 12.5 as the interface, not a REST path.

#### 12.2 REST operations consumed

None. The platform consumes no Workbench REST operation. The Web UI calls the frontend and the OIDC provider only, and the cluster reads its configuration through the platform parameters contract.

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema; the decision-record, case and access events keep their owners (DP-14).

#### 12.4 Events consumed

None. The platform consumes no Kafka topic.

#### 12.5 Workflows and activities

None. The contract publishes the task-queue and activity-contract convention rather than a workflow: a service's worker polls only its own task queue `rwb-<short>` in namespace `rwb-recovery`, publishes its typed activity interfaces in a contract jar, and calls another service only through that interface or a child workflow on the owner's queue (Architecture v5 slides 23 and 24; Architecture v5 slide 11). The platform task queue is task queue `rwb-platform`; the document records it as the platform queue and owns no workflow on it in this story.

#### 12.6 Schedules

None. The contract declares no Schedule and no batch window; the platform jobs JOB-21 and JOB-22 belong to the observability and smoke stories.

#### 12.7 Tables owned

None. The platform owns no `rwb_*` schema and no table in the ACE database; its two persistence stores belong to the app story and are Temporal persistence, not ACE tables.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Temporal platform fake frontend (this story) | A Temporal dev server with the namespace `rwb-recovery`, its retention and four Keyword search attributes, test CA certificates, the declared frontend API subset with its typed errors, the declared metrics and health endpoints, and the seeded smoke workflow `platform-smoke-20261116` | The app story (RWB-PLT-E1070-APP), the worker and SDK story (RWB-PLT-E1071), the 19 services' worker tests and the Wave 1 integration harness |

The fake answers from the declarations of this document, so a change to a declaration shows up as a contract-test failure rather than as a difference between environments. It is test-only and is never deployed to SIT, UAT or PROD.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The platform publishes no Workbench REST base; the metrics and health endpoints are operational, not Workbench routes |
| Kafka | 0 | 0 | The platform owns no topic and consumes none |
| Temporal | The contract of the frontend gRPC subset, the client identity, the namespace, the task-queue convention, the metrics and health endpoints | 0 | Temporal only: the document describes the platform interface and the fake stands in for it |
| File | 0 | 0 | No file is read or written by the contract or the fake |

### 13. Solution plan

**Deliverables**

| Deliverable | Form | Content |
|---|---|---|
| Namespace contract | Versioned document plus schema | Namespace name, retention in hours and days, the four Keyword search attributes, the personal-data refusal, the idempotent bootstrap rule |
| Client-identity and certificate profile | Document plus profile file | One certificate per service workload identity, the ACE internal CA, the namespace claim, the validity window and the renewal rule |
| Frontend API document | Document plus interface stub | The five allowed calls, the calls outside the subset, the request and response names, the five typed errors |
| OIDC role mapping | Table in the document and in configuration | RW-PLATADM operates, RW-AUDIT reads, every other role refused with MSG-P4-002 |
| Metrics and health contract | Table in the document | HTTPS GET /metrics on 9090, HTTP GET /health on 8080 with 200 and 503, the allowed network source |
| Helm values schema | Schema file | The keys each environment supplies, with the release family pinned and no business value |
| Fake frontend | Runnable test double | Temporal dev server with the namespace, the search attributes, test CA certificates and the seeded smoke workflow |
| Contract test | Test suite in the build | Every declaration, every error and every refusal asserted against the fake |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |

These are the Template and Rules §R5.5 rows that bear on a platform contract. DP-01 and DP-02 are declared, not implemented: the contract states that the platform owns no `rwb_*` schema and that every client is one service workload identity, so the separation the app story proves in AC2 is already fixed here. DP-13 and DP-14 are declared as absences: the platform has no `/api/recovery` base and no topic, so a consumer that expects one finds the rule in the contract rather than in a review. DP-04, DP-05, DP-06, DP-07, DP-15 and DP-19 are recorded in the metadata because the platform sits under all of them; the document repeats none of their content, because the parameters, the Drools kit, the views, the migrations and the screens keep their owners. This story adds no dependency of its own: it is a CON story and starts on Day 1.

**Build steps**

1. Write the namespace contract and its schema: the name, retention 720 hours and 30 days, the four Keyword search attributes, the personal-data refusal and the idempotent second run.
2. Write the client-identity and certificate profile: one certificate per service workload identity, the ACE internal CA, the namespace claim, the validity window and the renewal rule.
3. Write the frontend API document and the interface stub: the five allowed calls, the calls outside the subset, and the five typed errors with their conditions.
4. Write the OIDC role mapping, the metrics and health contract and the Helm values schema, and generate the tables of sections 12 and 14 from them so the document, the mapping and the fake cannot drift.
5. Assemble the fake frontend: the dev server, the namespace with its retention and search attributes, the test CA certificates, the seeded smoke workflow and the declared error answers.
6. Write the contract test: every declaration answered, the no-certificate, expired-certificate and foreign-namespace cases refused, and the metrics and health codes produced.
7. Publish v1 to the contract registry, notify the app story, the worker and SDK story and the 19 services, and record the version each one pins.

**Done when.** Every document validates, the mapping and the tables match the documents, the fake answers every declaration of sections 12 and 14 including the three certificate cases, and the contract test is green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| PLT-TLS-NOCERT | A client connects with no certificate | The TLS handshake fails; the frontend log records the client identity only | TLS alert |
| PLT-TLS-EXPIRED | A client connects with an expired certificate | The TLS handshake fails with certificate expired | TLS alert |
| PLT-403 | A call presents a certificate issued for another namespace, or names a foreign namespace | The call is refused; no workflow is started | PERMISSION_DENIED |
| PLT-404 | The namespace named in the request is not registered on the cluster | The call is refused; no workflow is started | NOT_FOUND |
| PLT-412 | The request is well formed but the platform state does not allow it, for example a workflow start against a closing namespace | The call is refused with the condition named | FAILED_PRECONDITION |
| PLT-503 | The frontend or the persistence layer is unavailable | The call is refused; the client retries under its own policy | UNAVAILABLE |
| MSG-P4-002 | A Workbench role other than RW-PLATADM or RW-AUDIT is presented to the Web UI mapping | You cannot {action} here. Your role does not include it. | 403 on the Web UI |

The contract's own error identifiers are reserved for the implementation; the message catalogue's identifiers for edge and platform entries replace them when they exist and no other value changes.

### 15. Screens and states

No screen in this story, and the document declares none: the Web UI is an operational console behind Entra ID, not a Workbench screen, and no screen is composed by gateway-bff for the platform (DP-19). The mapping fixes the two states the console exposes, operate for RW-PLATADM and read-only for RW-AUDIT, and the refusal state for every other Workbench role. The screens of the Workbench are the gateway-bff surface and the front end, and the platform adds nothing to them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1070-CON-01 | AC1, BR1 | Contract | The namespace contract validated; `rwb-recovery`, 720 hours, 30 days, the four Keyword search attributes, the personal-data refusal; a second bootstrap run as a no-op |
| TC-PLT-E1070-CON-02 | AC2, BR3 | Contract | The frontend API document: the five allowed calls, the calls outside the subset, the five typed errors and their conditions |
| TC-PLT-E1070-CON-03 | AC3, BR3 | Contract | The certificate profile; no certificate, an expired certificate and a certificate for another namespace, all refused |
| TC-PLT-E1070-CON-04 | AC4, BR4 | Component | The OIDC mapping: RW-PLATADM operate, RW-AUDIT read, RW-CASEOWN and every other role refused with MSG-P4-002 |
| TC-PLT-E1070-CON-05 | AC5, BR8 | Contract | The metrics and health contract: HTTPS GET /metrics on 9090, HTTP GET /health on 8080 with 200 and 503, the allowed network source |
| TC-PLT-E1070-CON-06 | AC6, BR6, BR7 | Component | The fake frontend over every declaration; the seeded smoke workflow `platform-smoke-20261116`; a breaking change raising v2 and deprecating v1 |

### 17. Guardrails

- No business value and no personal data in the contract, in an example or in the fake: namespace names, role codes, result codes and synthetic workflow identifiers only.
- No service short, no schema name, no topic name and no Workbench REST base in the document: the platform owns none of them (DP-13, DP-14).
- The four search attributes stay CaseId, Stage, ProductGroup and QueueCode; a new attribute is a breaking change and is never added quietly.
- One certificate per service workload identity, from the ACE internal CA, with the namespace claim; no shared certificate and no anonymous client.
- The Web UI maps two roles only; every other Workbench role is refused, and no shared operator account exists.
- The fake is test-only, holds synthetic data and is never deployed to SIT, UAT or PROD; the values schema of no environment points at it.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.
- Every environment value is a declared key; the document bakes in no replica count, node size, retention value or release number beyond the namespace settings and the release family.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner; a tested way back | Epic 1, 3.2; Program, 5.2 | TC-PLT-E1070-CON-01, TC-PLT-E1070-CON-06 |
| REQ-DRI-010 | Environment values are versioned and changed without a code release | Epic 1, 3.2; Program, 5.1 and 5.7 | TC-PLT-E1070-CON-05, TC-PLT-E1070-CON-06 |

| Decision or source | What it fixes here |
|---|---|
| ADR-016 | The reusable Temporal layer: one cluster per environment, a namespace per workbench, a namespace rather than a second cluster for the next workbench |
| DP-10 | A Schedule or event-started workflow replaces Quartz; the contract publishes the task-queue convention, not a job |
| DP-13 | No monolith API base: the platform publishes no `/api/recovery` base and no service short |
| Architecture v5 slides 11, 20, 23, 24, 35 | Five call types and their contracts; the service contract rule; the five layers; one queue per service; mTLS and the two Web UI roles |
| Template and Rules §R4 | The namespace `rwb-recovery` and the naming rules the contract may not repeat |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1070-APP | App development | H consumer: installs the cluster, the two persistence stores, the namespace, the certificate binding, the OIDC mapping and the dashboard against this contract and its fake |
| RWB-PLT-E1071-CON, RWB-PLT-E1071-APP | Contract, App development | Consumers: the worker and SDK that poll task queue `rwb-<short>` under the client profile this contract declares |
| RWB-PLT-E1072-CON | Contract | Consumer: the Drools kit runs inside the services' activities on the workers this contract admits |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | Consumers: the platform parameters and reference data are read at deploy time through these contracts |
| RWB-PLT-E1047-CON | Contract | Consumer: the naming library; the platform declares that it owns no topic |
| RWB-PLT-E1044-CON | Contract | Consumer: the Flyway convention the Temporal persistence stores do not use |
| RWB-PLT-N001-CON | Contract | Consumer: the Web UI is not a Workbench screen and no route is added to the edge |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1022-CON | Contract | C: the parameters, reference data and roles this contract references but does not own |
| RWB-PLT-E1056-OPS | DevOps | X: registers the run book that names the namespace, the certificates and the parameter `temporal.target` |

### 19. Out of scope

- The cluster, its persistence stores, the namespace bootstrap job, the certificate binding, the OIDC application, the dashboard and the run book: RWB-PLT-E1070-APP.
- The worker, the SDK wiring, the payload codec and the worker-side retry policy: RWB-PLT-E1071.
- The workflow kit templates and their versioning: the workflow kit contract story.
- Workflow observability, alerts and the stuck workflow scan: the successors of RWB-E2-037.
- The codec server, decode and the admin audit: the successors of RWB-E2-038.
- Backup, restore, zone failover, upgrade and archive: the successors of RWB-E2-039.
- The `ace-collection` namespace, the Nexus endpoints in ACE and the ACE team's own Temporal use.
- The 19 services' schemas, topics, task queues, REST bases and business models; the platform owns none of them.
- Workbench screens and the admin console (Epic 8); the Web UI is an operational console.
