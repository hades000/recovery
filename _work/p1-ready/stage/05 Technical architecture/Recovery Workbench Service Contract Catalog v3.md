SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench Service Contract Catalog v3

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Document | Recovery Workbench Service Contract Catalog |
| Version | 3 |
| Date | 27 November 2026 |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Owner role | Solution architect |
| Services in scope | 19: P1 to P10 and S1 to S9, plus the shared platform (PLT), gateway-bff and the partner gateway |
| Source of record | Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); Recovery Workbench Temporal and Drools Design Text Extract v1 (slides 11 to 14); Recovery Workbench Microservice Ownership Map v1 |
| Change log | below |

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Contract Catalog. The contract model, the call-type matrix of Architecture v5 slide 13, every provider and consumer pair, the contract artefact per call type, the dependency classes and the contract tests are stated once, per service. No earlier version of this family exists (GAP-0099; ASM-0168). |
| 3 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) | v3 · 27 November 2026 · D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits: shared error envelope and idempotency/If-Match rules; one contract file and one provider fake per contract version; rwb-source-data 5.1.0 operations, workflows and event consumers; new contract pairs of RD-P1-007, 010, 020, 022, 024 and 047; registration of version 5.1.0; batch D (RD-P1-060 to RD-P1-066): customer, account and collateral reads, one GET /payments with two query forms, ledger callers, authorise and parameter reads, new consumer pairs, section 6.1 aligned to Service Catalog v2. |

# 1. Purpose and scope

This catalogue is the contract register of the 19 Recovery services. For every service it states what the service provides, to whom, in which call type, under which artefact and version, and what it consumes from which provider. It is the document a team reads before writing code, the document the contract tests are generated from, and the register in which each service publishes its contract document (the CON stories of every service epic name this catalogue as the place of publication).

It answers five questions:

- What is the interface between these two services, and which call type is it?
- Which artefact carries the contract, and which version of it?
- May this call be synchronous, and if not, what replaces it?
- What does the consumer build against while the provider is not yet built?
- Which test proves that the contract holds, and which story runs it?

What this catalogue does not contain: the operation schemas and examples (API Specification v5, one file per service plus gateway-bff and an index), the event payloads (Kafka Topic and Event Catalog v1), the workflow steps and activity signatures (Temporal Workflow and Activity Catalog v1), the table columns (Logical Data Model and Physical Schema) and the story-level build order (Build Sequence). Where those documents define a payload, this catalogue names the contract and points at them.

Release dates are not held here. They are held in the Release Plan, they are unchanged, and every one of them is tentative (Decision U7 and DL48).

# 2. How this catalogue is built

## 2.1 Precedence

Where two sources disagree, the higher one in the list below wins and the loser is recorded as a gap row and an assumption row (Template and Rules §R3). The order used here is:

1. the Arch v5 catalogue slides 13 to 20 and 41 to 44, for services, resources, call types and jobs;
2. the Recovery Temporal and Drools Design v1, for the workflow split, the activity contracts and the rules placement;
3. the Arch v5 narrative slides, for the standards that every contract follows;
4. the Recovery Workbench Microservice Ownership Map v1, for the owner of every table, endpoint, event, workflow and job;
5. the current architecture documents (Decision Log, ADRs, TSDs, FSDs, LDM), which the realignment rewrites.

The Ownership Map is used for every owner in this catalogue. Its Services sheet is the source of the code, the service name, the wave, the schema, the REST base, the topic and the task queue. Its Endpoints, Events, Workflows and activities, Jobs and Tables sheets are the source of the owner of every contract element named below. Where the map carries a ruling, the ruling is applied and the assumption behind it is named in the map.

## 2.2 What changed in this version

- The one recovery service with one REST surface and one schema becomes 19 services, each with its own OpenAPI contract, its own AsyncAPI contract, its own activity contract jar and its own schema (Arch v5 slide 41; ADR-013 and ADR-014).
- Contract-first becomes the rule: the contract artefact is published before the code, the consumer builds against it and its fake, and a contract test in both builds proves the pair (ADR-020; Architecture v5 slide 46).
- The call-type matrix of Architecture v5 slide 13 is reproduced in section 4 and is the authority for every pair in section 5. A pair that is not in the matrix is not a contract.
- Every cross-service pair is classified in the dependency classes of Template and Rules §R5.4: C for the consuming story, which builds against the provider's published contract and its fake, and I for the integration story of the wave, which tests the real behaviour.
- Version 3: contract pairs ruled by the P1 decision register (RD-P1-nnn) that slide 13 does not print are listed in section 5 with the ruling or story as source; they are contracts although the matrix of section 4 does not show them.
- No service or call type is added, removed or renamed against Architecture v5. The points the sources leave open are recorded in section 11 and in the two registers.

# 3. The contract model

## 3.1 One call type per interface

A service never mixes call types for the same purpose. A REST call answers a person who is waiting. An event announces a fact that has already happened. A Temporal call commands a step in another service or runs a long process. A file moves bulk data or reaches a party outside the bank. A SQL view reads ACE data, and only rwb-source-data does that.

| Call type | What it is for | Contract artefact | Version form | Source |
|---|---|---|---|---|
| REST | A person waits for the answer: gateway-bff to the owner service, one hop, in parallel for composite screens, and a cached reference read | OpenAPI 3.1 document per service, server /api/recovery/<short>/v1 | /v1 in the path | Arch v5 slides 10, 11, 13 |
| Kafka event | A fact others may react to; never a command | AsyncAPI 3.0 per service, CloudEvents 1.0 binary mode, JSON Schema in the registry, BACKWARD compatibility | rwb.<short>.events.v1; event name rwb.<short>.<Event>.v1 | Arch v5 slides 11, 22, 42, 43 |
| Temporal | A step in another service, a child workflow per stage, or a Schedule | Typed activity and workflow interface in a contract jar, published on task queue rwb-<short> | Contract jar major version; workflow type name | Arch v5 slide 11; Temporal and Drools Design slides 11 to 14 |
| Nexus | A call into another namespace, used once in this design for the restructure calculator in ACE | Nexus operation restructure.calculate in namespace ace-collection | Operation name and version | Arch v5 slides 9 and 18; Temporal and Drools Design slide 12 |
| File | Bulk data or a party outside the bank: WIN registered mail, debt-buyer files, WORM storage | Manifest with fileId, batchId, sha256 and record count; SAS link open for 15 minutes | Manifest version and file naming | Arch v5 slides 11, 16 |
| SQL view | Reading ACE data, rwb-source-data only | The 30 recovery.v_ace_* views, SELECT only (ADR-010) | View name and column contract | Arch v5 slides 11, 15, 29 |

The database is not a contract between services. A service writes only its own schema rwb_<name>, holds no grant on any other schema, and never joins across schemas (DP-01; Arch v5 slide 29). The only database contract in this catalogue is the ACE view contract between rwb-source-data and the ACE database.

## 3.2 The contract key

A contract is named in this catalogue by four values, all of them taken from the sources and none of them a new identifier:

- the provider service code (P1 to P10, S1 to S9, PLT, gateway-bff, ACE Common, ACE database, outside the cluster);
- the consumer service code, or All 19 services where the source says every service;
- the call type of section 3.1;
- the interface as the source names it: the operation path, the event name, the activity, child workflow or Schedule, the file, or the view.

Where the source gives no consumer for an event, the row states Not specified in the source documents (GAP-0102; ASM-0171) rather than a guess.

## 3.3 What every contract states

| Element | REST | Kafka | Temporal | File |
|---|---|---|---|---|
| Provider | The owning service of the resource | The service that writes the fact | The service whose queue runs the activity or workflow | The service that writes the file |
| Consumer | gateway-bff or a service, one hop | Every service that reacts; never a command target | The caller, on the provider's queue | The receiving party |
| Identity and authorisation | User JWT from ACE Common sign-in; the service authorises through rwb-access | Workload identity per service; topic ACL by service | Workload identity; namespace rwb-recovery | Partner gateway FAPI 2.0 or the bank MFT channel |
| Timeout and retry | 2 s timeout, one GET retry with jitter, breaker and bulkhead per downstream | Retry 1 min, 10 min, 1 h, then .dlt with an alert and a replay tool | 1 s initial interval, back-off 2, 10 attempts; non-retryable list per activity | FileFailed event, operator retry, checksum on receipt |
| Idempotency | Idempotency-Key (canonical UUID) on every POST, stored response replayed for 24 hours; missing or malformed 400 MSG-PLT-N009-03, mismatch or in flight 409 MSG-PLT-N009-05, store down 503 MSG-PLT-N009-06 (RD-P1-001). PUT and PATCH use If-Match and ETag: missing 428, stale 409, both MSG-GEN-004 (RD-P1-006) | idempotency_key and processed_event in the same transaction as the change | Workflow ID and activity idempotency key | batchId and sha256 checked before the file is accepted |
| Error form | RFC 9457 problem details, application/problem+json, one Problem schema: type, title, status, messageCode and traceId required; detail, instance, messageTh, field and errors optional (RD-P1-004) | CloudEvents data with an error code and no personal data | Typed failures; the workflow decides | Manifest with the reason and the record count reached |
| Source | Arch v5 slides 10, 11, 13 | Arch v5 slides 11, 22, 42 | Arch v5 slide 11; Temporal and Drools Design slide 14 | Arch v5 slide 11 |

## 3.4 Versioning and compatibility

- REST carries the version in the path, /v1, and a breaking change is a new path version served side by side until the consumers move. Additive change inside v1 is allowed when every consumer tolerates unknown fields.
- Events are versioned in the registry with BACKWARD compatibility, and the topic carries the version: rwb.<short>.events.v1, with the retry and dead-letter topics .retry.1m, .retry.10m, .retry.1h and .dlt beside it.
- Temporal contract jars are versioned with the workflow kit and the activity interfaces; a change to an activity signature is a new major version of the jar and a new worker deployment, so a running workflow keeps replaying against the version it started with.
- The file manifest is versioned with the interface; INT-14 and INT-25 keep their identifiers unchanged.
- A contract document is registered in section 7 of this catalogue with its version and its publisher, and the CON story of the service epic is what publishes it.
- One contract file per service: the published service OpenAPI and AsyncAPI files; a story adds its fragment to the service file and creates no story-local contract file (RD-P1-005).
- Each provider publishes a fake per contract version, generated from that contract, at fakes/<service>/<contract version>/ in the platform contract fake library; every consumer story pins the contract version and the fake version (RD-P1-011; the library path is a working value).

# 4. The call-type matrix (Architecture v5 slide 13)

Row = the service that starts the interaction; column = the service it calls or listens to. The table is reproduced exactly as Architecture v5 slide 13 prints it, including the combined cells. It is the authority for section 5.

| starts / target | P3 | P7 | P4 | S8 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | P5 | P6 | P8 | S9 | P2 | P1 | P9 | P10 | ACE Cmn | ACE DB | Outside |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P3 rwb-case |  | E | R | T E | T E | T E | T E | T E | T E | T E | T E | E | E | E | E |  | T E |  |  |  |  |  |
| P7 rwb-decision |  |  | R |  |  |  |  |  |  |  |  |  | E |  |  |  |  |  | E |  |  | F |
| P4 rwb-access |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  |  |
| S8 rwb-deviation | E |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R E |  | T E |  |  |  |
| S1 rwb-valuation |  | T E |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  | T |  |  |  |
| S2 rwb-treatment |  | T E |  | E |  |  |  |  |  |  |  | T |  | T E |  |  |  |  |  | N |  |  |
| S3 rwb-guarantee |  | T |  |  |  |  |  |  |  |  |  |  | T E | E |  |  |  |  |  |  |  |  |
| S4 rwb-litigation |  | T |  |  |  |  |  |  |  |  |  |  | T E |  | T E |  |  |  |  |  |  |  |
| S5 rwb-asset |  | T |  |  |  |  |  | E |  |  |  |  | T | T E | T E |  |  |  |  |  |  |  |
| S6 rwb-debtsale |  | T |  |  |  |  |  |  |  |  |  | T |  | T E |  | T |  |  |  |  |  |  |
| S7 rwb-writeoff |  | T |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | R E |  |  |  |  |  |
| P5 rwb-document |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | F |
| P6 rwb-comms | E | T |  | E |  | E |  |  |  |  |  | T |  | E |  | T |  |  |  | R |  |  |
| P8 rwb-payment |  | E |  |  |  | E |  |  | E | E | E |  |  |  |  | T | T E |  |  |  |  |  |
| S9 rwb-partner |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | R |
| P2 rwb-integration |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | F |
| P1 rwb-source-data |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | S |  |
| P9 rwb-reporting | E |  |  |  |  | E | E |  |  | E | E |  | E |  |  | T | T |  |  |  |  |  |
| P10 rwb-agent | E |  |  |  |  |  |  |  |  |  |  | R E |  |  |  |  | R |  |  |  |  | R |

| Cell | Meaning |
|---|---|
| T | Temporal: an activity on the owner's queue, or a child workflow there |
| N | Nexus operation into ACE |
| R | REST call |
| E | Listens to the column's Kafka events |
| S | SQL views |
| F | File |

Four rules come with the matrix and hold in every section below (Arch v5 slide 13):

1. Route services reach the shared capabilities through Temporal, never REST.
2. Only rwb-source-data touches ACE's tables; every other service asks it through its contract.
3. rwb-decision and rwb-reporting listen widely and call almost nobody.
4. The case router in rwb-case turns events into signals; no service calls another service directly for a business step.

Pairs ruled by the P1 decision register that slide 13 does not print (for example the interaction ledger appends and the ledger intake of rwb-source-data) are listed in section 5 and not added to the matrix.

Not shown in the matrix because every service does it: audit and PII logs to ACE Common on Kafka, DecisionRecorded to rwb-decision on rwb.decision-record.v1, permission data cached from rwb-access, and traces to OpenTelemetry. The first two and the permission cache are carried in section 5 as All 19 services so that they are not lost; traces are a platform contract and are named in section 7.3.

# 5. The contract inventory

Every pair in the matrix, resolved to the interface the sources name. The order is provider code, then consumer code, then call type. The dependency class is the class of Template and Rules §R5.4 that the consuming story takes: C means the consuming story builds against the provider's published contract and its fake, X means the pair crosses an edge outside the 19 services and is tracked rather than built against, and H appears once, where rwb-case consumes its own CaseAllocationFailed.

| Call type | Pairs |
|---|---|
| File | 3 |
| Kafka | 89 |
| Nexus | 1 |
| REST | 51 |
| SQL view | 1 |
| Temporal | 38 |
| Total | 183 |

| Provider | Consumer | Call type | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|---|
| ACE Common | gateway-bff | REST | Sign-in through ACE Common; session to short-lived user JWT | ACE Common API (sign-in, notification path) | X | slide 20 |
| ACE Common | P4 rwb-access | REST | Sign-in, group-to-role (Entra ID) | ACE Common API (sign-in, notification path) | X | slide 13, slide 14 |
| ACE Common | P6 rwb-comms | REST | Notification path (SMS, LINE OA) | ACE Common API (sign-in, notification path) | X | slide 13, slide 17 |
| ACE Common | S2 rwb-treatment | Nexus | restructure.calculate (Nexus operation, namespace ace-collection) | Nexus operation, ace-collection | X | slide 13, slide 18 |
| ACE database | P1 rwb-source-data | SQL view | SELECT on the 30 recovery.v_ace_* views, read only (ADR-010) | View contract, SELECT only | X | slide 13, slide 15 |
| All 19 services | ACE Common | Kafka | Audit and PII logs | AsyncAPI 3.0, ACE Common logging topics | X | slide 13 note |
| All 19 services | P7 rwb-decision | Kafka | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | slide 42, slide 43 (EV-08) |
| All 19 services | P9 rwb-reporting | Kafka | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | slide 42, slide 43 (EV-08) |
| Outside the cluster | P10 rwb-agent | REST | Enterprise AI private endpoint (INT-23), HTTPS | The external API or interface of that party | X | slide 13, slide 16 |
| Outside the cluster | S9 rwb-partner | REST | Partners (law firms, agencies, buyers) through the partner gateway, FAPI 2.0, MFA | The external API or interface of that party | X | slide 13, slide 17 |
| P1 rwb-source-data | gateway-bff | Kafka | AceDataLate | AsyncAPI 3.0, rwb.source-data.events.v1 | X | slide 42, slide 43 (EV-27) |
| P1 rwb-source-data | gateway-bff | REST | GET /customers/{personKey}; GET /accounts/{accountKey}; GET /data-products/freshness (composite case screen, one hop each in parallel) | OpenAPI 3.1, /api/recovery/source-data/v1 | X | slide 15, slide 20; RD-P1-060 |
| P1 rwb-source-data | P10 rwb-agent | REST | Tool: read case facts (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 16 |
| P1 rwb-source-data | P3 rwb-case | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| P1 rwb-source-data | P3 rwb-case | Temporal | Activity: listEligibleAccounts(EligibleAccountsRequest) | Activity contract jar on task queue rwb-source-data | C | slide 14 |
| P1 rwb-source-data | P8 rwb-payment | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| P1 rwb-source-data | P8 rwb-payment | Temporal | Activity: payments for business date | Activity contract jar on task queue rwb-source-data | C | slide 13, slide 17 |
| P1 rwb-source-data | P9 rwb-reporting | Temporal | Activity: snapshot(page) for measures | Activity contract jar on task queue rwb-source-data | C | slide 13, slide 15 |
| P1 rwb-source-data | S1 rwb-valuation | REST | Collateral and appraisals (GET /collateral/{assetKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 18; RD-P1-060 |
| P1 rwb-source-data | S7 rwb-writeoff | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| P1 rwb-source-data | S7 rwb-writeoff | REST | GL outcome | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 20 |
| P1 rwb-source-data | S8 rwb-deviation | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| P1 rwb-source-data | S8 rwb-deviation | REST | Party flags (GET /customers/{personKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 15; RD-P1-060 |
| P10 rwb-agent | P5 rwb-document | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| P10 rwb-agent | P5 rwb-document | Temporal | Child workflow: classify / extract run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 16 |
| P10 rwb-agent | P7 rwb-decision | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| P10 rwb-agent | S1 rwb-valuation | Temporal | Child workflow: route agent run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 18 |
| P10 rwb-agent | S8 rwb-deviation | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| P10 rwb-agent | S8 rwb-deviation | Temporal | Child workflow: screening agent run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 15 |
| P2 rwb-integration | Outside the cluster | File | WIN registered mail, daily outbound file (INT-14); debt buyers, per lot, encrypted (INT-25) | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 16 |
| P2 rwb-integration | P6 rwb-comms | Temporal | Activity: deliverFile (WIN letters) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 17 |
| P2 rwb-integration | P8 rwb-payment | Temporal | Activity: deliverFile (posting file) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 17 |
| P2 rwb-integration | P9 rwb-reporting | Temporal | Activity: deliverFile (regulatory extract) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 15 |
| P2 rwb-integration | The requesting service | Kafka | FileDelivered | AsyncAPI 3.0, rwb.integration.events.v1 | X | slide 43 (event catalogue, not numbered) |
| P2 rwb-integration | The requesting service | Kafka | FileFailed | AsyncAPI 3.0, rwb.integration.events.v1 | X | slide 43 (event catalogue, not numbered) |
| P2 rwb-integration | S6 rwb-debtsale | Temporal | Activity: deliverFile (buyer file) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 19 |
| P3 rwb-case | gateway-bff | Kafka | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | X | slide 42, slide 43 (EV-19) |
| P3 rwb-case | gateway-bff | REST | GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id} | OpenAPI 3.1, /api/recovery/case/v1 | X | slide 14, slide 20 |
| P3 rwb-case | P10 rwb-agent | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| P3 rwb-case | P3 rwb-case | Kafka | CaseAllocationFailed | AsyncAPI 3.0, rwb.case.events.v1 | H | slide 42, slide 43 (EV-03) |
| P3 rwb-case | P6 rwb-comms | Kafka | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-05) |
| P3 rwb-case | P9 rwb-reporting | Kafka | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-02) |
| P3 rwb-case | P9 rwb-reporting | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| P3 rwb-case | P9 rwb-reporting | Kafka | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-05) |
| P3 rwb-case | P9 rwb-reporting | Kafka | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-04) |
| P3 rwb-case | S8 rwb-deviation | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| P4 rwb-access | All 19 services | Kafka | AccessPolicyChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | slide 43 (event catalogue, not numbered) |
| P4 rwb-access | All 19 services | Kafka | DoaLimitChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | slide 43 (event catalogue, not numbered) |
| P4 rwb-access | P3 rwb-case | REST | POST /authorise (role, scope, DoA), cached in rwb-case | OpenAPI 3.1, /api/recovery/access/v1 | C | slide 13, slide 14 |
| P4 rwb-access | P7 rwb-decision | REST | GET /doa-limits (DoA limits) | OpenAPI 3.1, /api/recovery/access/v1 | C | slide 13, slide 14 |
| P5 rwb-document | Outside the cluster | File | Azure Blob (WORM): files, 2.8 TB by 2031 | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 16 |
| P5 rwb-document | P10 rwb-agent | Kafka | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-16) |
| P5 rwb-document | P10 rwb-agent | REST | Tool: read extracted fields (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 16 |
| P5 rwb-document | P2 rwb-integration | REST | Fetch file by ID (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 16 |
| P5 rwb-document | P3 rwb-case | Kafka | DocumentFieldsExtracted | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-17) |
| P5 rwb-document | P3 rwb-case | Kafka | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-16) |
| P5 rwb-document | P6 rwb-comms | Temporal | Document: generate letter | Activity contract jar on task queue rwb-document | C | slide 13, slide 17 |
| P5 rwb-document | S2 rwb-treatment | Temporal | Contract document generation and e-sign | Activity contract jar on task queue rwb-document | C | slide 13, slide 18 |
| P5 rwb-document | S6 rwb-debtsale | Temporal | Document: data room pack | Activity contract jar on task queue rwb-document | C | slide 13, slide 19 |
| P5 rwb-document | S9 rwb-partner | REST | Partner uploads (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 17 |
| P6 rwb-comms | P3 rwb-case | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| P6 rwb-comms | P7 rwb-decision | Kafka | NoticeGenerated | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-13) |
| P6 rwb-comms | P9 rwb-reporting | Kafka | NoticeDispatched | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-14) |
| P6 rwb-comms | S3 rwb-guarantee | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| P6 rwb-comms | S3 rwb-guarantee | Temporal | Child workflow: guarantor notice | Activity contract jar on task queue rwb-comms | C | slide 13, slide 18 |
| P6 rwb-comms | S4 rwb-litigation | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| P6 rwb-comms | S4 rwb-litigation | Temporal | Child workflow: demand notice | Activity contract jar on task queue rwb-comms | C | slide 13, slide 19 |
| P6 rwb-comms | S5 rwb-asset | Temporal | Not specified in the source documents (GAP-0106; ASM-0175) | Activity contract jar on task queue rwb-comms | C | slide 13 |
| P7 rwb-decision | gateway-bff | Kafka | ApprovalRequested | AsyncAPI 3.0, rwb.decision.events.v1 | X | slide 42, slide 43 (EV-09) |
| P7 rwb-decision | Outside the cluster | File | Immutable storage: daily ledger seal (WORM) | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 14 |
| P7 rwb-decision | Not specified in the source documents (GAP-0102; ASM-0171) | Kafka | ApprovalDecided | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 43 (event catalogue, not numbered) |
| P7 rwb-decision | P3 rwb-case | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| P7 rwb-decision | P6 rwb-comms | Temporal | Child workflow: approval | Activity contract jar on task queue rwb-decision | C | slide 13, slide 17 |
| P7 rwb-decision | P8 rwb-payment | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| P7 rwb-decision | S1 rwb-valuation | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| P7 rwb-decision | S1 rwb-valuation | Temporal | Child workflow: ApprovalWorkflow (kit template) | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| P7 rwb-decision | S2 rwb-treatment | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| P7 rwb-decision | S2 rwb-treatment | Temporal | Child workflow: ApprovalWorkflow (DoA) | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| P7 rwb-decision | S3 rwb-guarantee | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| P7 rwb-decision | S4 rwb-litigation | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| P7 rwb-decision | S5 rwb-asset | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| P7 rwb-decision | S6 rwb-debtsale | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| P7 rwb-decision | S7 rwb-writeoff | Temporal | Child workflow: committee approval | Activity contract jar on task queue rwb-decision | C | slide 13, slide 20 |
| P8 rwb-payment | P3 rwb-case | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| P8 rwb-payment | P3 rwb-case | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| P8 rwb-payment | P3 rwb-case | Kafka | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-11) |
| P8 rwb-payment | P6 rwb-comms | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| P8 rwb-payment | S2 rwb-treatment | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| P8 rwb-payment | S2 rwb-treatment | Kafka | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-11) |
| P8 rwb-payment | S2 rwb-treatment | Temporal | Activity: postProceeds (saga step) | Activity contract jar on task queue rwb-payment | C | slide 13, slide 18 |
| P8 rwb-payment | S3 rwb-guarantee | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| P8 rwb-payment | S5 rwb-asset | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| P8 rwb-payment | S5 rwb-asset | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 19 |
| P8 rwb-payment | S6 rwb-debtsale | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| P8 rwb-payment | S6 rwb-debtsale | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 19 |
| P8 rwb-payment | S7 rwb-writeoff | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| P8 rwb-payment | S7 rwb-writeoff | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 20 |
| P9 rwb-reporting | Not specified in the source documents (GAP-0102; ASM-0171) | Kafka | ReportPublished | AsyncAPI 3.0, rwb.reporting.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S1 rwb-valuation | P3 rwb-case | Kafka | RouteDecided | AsyncAPI 3.0, rwb.valuation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S1 rwb-valuation | P3 rwb-case | Temporal | Child workflow: RouteDecisionWorkflow | Activity contract jar on task queue rwb-valuation | C | slide 14, slide 18 |
| S2 rwb-treatment | P3 rwb-case | Kafka | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S2 rwb-treatment | P3 rwb-case | Temporal | Child workflow: the treatment stage workflows (TreatmentWorkflow) | Activity contract jar on task queue rwb-treatment | C | slide 14, slide 18 |
| S2 rwb-treatment | P6 rwb-comms | Kafka | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 42, slide 43 (EV-10) |
| S2 rwb-treatment | P8 rwb-payment | Kafka | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 42, slide 43 (EV-10) |
| S2 rwb-treatment | P9 rwb-reporting | Kafka | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S3 rwb-guarantee | P3 rwb-case | Kafka | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S3 rwb-guarantee | P3 rwb-case | Kafka | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S3 rwb-guarantee | P3 rwb-case | Temporal | Child workflow: GuaranteeClaimWorkflow | Activity contract jar on task queue rwb-guarantee | C | slide 14, slide 18 |
| S3 rwb-guarantee | P9 rwb-reporting | Kafka | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S3 rwb-guarantee | P9 rwb-reporting | Kafka | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S4 rwb-litigation | P3 rwb-case | Kafka | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S4 rwb-litigation | P3 rwb-case | Kafka | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S4 rwb-litigation | P3 rwb-case | Temporal | Child workflow: LitigationWorkflow | Activity contract jar on task queue rwb-litigation | C | slide 14, slide 19 |
| S4 rwb-litigation | S5 rwb-asset | Kafka | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S4 rwb-litigation | S5 rwb-asset | Kafka | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S5 rwb-asset | P3 rwb-case | Kafka | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S5 rwb-asset | P3 rwb-case | Kafka | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 42, slide 43 (EV-22) |
| S5 rwb-asset | P3 rwb-case | Temporal | Child workflow: AssetDisposalWorkflow | Activity contract jar on task queue rwb-asset | C | slide 14, slide 19 |
| S5 rwb-asset | P8 rwb-payment | Kafka | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S5 rwb-asset | P8 rwb-payment | Kafka | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 42, slide 43 (EV-22) |
| S6 rwb-debtsale | P3 rwb-case | Kafka | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S6 rwb-debtsale | P3 rwb-case | Kafka | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 42, slide 43 (EV-23) |
| S6 rwb-debtsale | P3 rwb-case | Temporal | Child workflow: DebtSaleWorkflow | Activity contract jar on task queue rwb-debtsale | C | slide 14, slide 19 |
| S6 rwb-debtsale | P8 rwb-payment | Kafka | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 42, slide 43 (EV-23) |
| S6 rwb-debtsale | P9 rwb-reporting | Kafka | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 43 (event catalogue, not numbered) |
| S7 rwb-writeoff | P3 rwb-case | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| S7 rwb-writeoff | P3 rwb-case | Temporal | Child workflow: WriteOffWorkflow | Activity contract jar on task queue rwb-writeoff | C | slide 14, slide 20 |
| S7 rwb-writeoff | P8 rwb-payment | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| S7 rwb-writeoff | P9 rwb-reporting | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| S8 rwb-deviation | P3 rwb-case | Kafka | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-07) |
| S8 rwb-deviation | P3 rwb-case | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| S8 rwb-deviation | P3 rwb-case | Temporal | Child workflow: DeviationWorkflow | Activity contract jar on task queue rwb-deviation | C | slide 14, slide 15 |
| S8 rwb-deviation | P6 rwb-comms | Kafka | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-07) |
| S8 rwb-deviation | P6 rwb-comms | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| S8 rwb-deviation | S2 rwb-treatment | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| S9 rwb-partner | P3 rwb-case | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| S9 rwb-partner | Partner portal | Kafka | InstructionIssued | AsyncAPI 3.0, rwb.partner.events.v1 | X | slide 42, slide 43 (EV-20) |
| S9 rwb-partner | S4 rwb-litigation | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| S9 rwb-partner | S4 rwb-litigation | Temporal | Activity: issueInstruction (law firm) | Activity contract jar on task queue rwb-partner | C | slide 13, slide 19 |
| S9 rwb-partner | S5 rwb-asset | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| S9 rwb-partner | S5 rwb-asset | Temporal | Activity: issueInstruction (auction vendor) | Activity contract jar on task queue rwb-partner | C | slide 13, slide 19 |
| P1 rwb-source-data | P2 rwb-integration | REST | GET /efs-history | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-010 |
| P1 rwb-source-data | P2 rwb-integration | REST | POST /cases/{caseId}/interactions (EFS history, one call per row) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| P1 rwb-source-data | P2 rwb-integration | REST | GET /booking-facts; GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2007-APP |
| P1 rwb-source-data | P3 rwb-case | REST | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| P1 rwb-source-data | P3 rwb-case | REST | Account-page read for a page of account keys (path and keys per call pending, GAP-3274) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-024 |
| P1 rwb-source-data | P6 rwb-comms | REST | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| P1 rwb-source-data | P6 rwb-comms | REST | GET /proof-of-delivery | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007; RWB-P1-E1055-APP |
| P1 rwb-source-data | P6 rwb-comms | REST | GET /contact-points; POST /contact-points/{contactPointKey}/failed-contacts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2022-APP |
| P1 rwb-source-data | P6 rwb-comms | REST | GET /data-products/{productCode}/records (DP02 contact rows) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2021-APP |
| P1 rwb-source-data | P8 rwb-payment | REST | GET /payments?businessDate=; GET /accounts/{accountKey}/installment-facts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2008-APP |
| P1 rwb-source-data | P5 rwb-document | REST | POST /retention-runs; GET /retention-runs/{runId} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-047 |
| P1 rwb-source-data | P9 rwb-reporting | REST | GET /payments?accountKey= (baseline measures) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-022; RD-P1-061 |
| P1 rwb-source-data | gateway-bff | REST | PUT /extension-facts/parties/{personKey}; PUT /extension-facts/accounts/{accountKey} (exclusion screen) | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-006; RWB-P1-E1018-APP |
| P1 rwb-source-data | ACE Airflow | REST | POST /business-days/{date}/ready; GET /business-days/{date}/status | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-005; slide 32 |
| P2 rwb-integration | P1 rwb-source-data | REST | GET /admin/scheduled-jobs | OpenAPI 3.1, /api/recovery/integration/v1 | C | RD-P1-021 |
| P3 rwb-case | P1 rwb-source-data | REST | GET /cases/{caseId}; GET /cases/{caseId}/accounts | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-007; RD-P1-024 |
| P3 rwb-case | P1 rwb-source-data | REST | GET /cases/retention-exclusions; GET /cases/closure-dates | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-047 |
| P3 rwb-case | P1 rwb-source-data | REST | GET /parameters/{key}; GET /admin/lists/{listCode} | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-028 |
| P3 rwb-case | P1 rwb-source-data | REST | Reference load apply handler for the P1 table codes | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-020 |
| P3 rwb-case | P1 rwb-source-data | REST | Open-case key list and allocation state for a business date (paths pending, GAP-3273) | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-022; RD-P1-040 |
| P5 rwb-document | P1 rwb-source-data | REST | Retention classes read | OpenAPI 3.1, /api/recovery/document/v1 | C | RWB-P1-E1016-APP |
| P7 rwb-decision | P1 rwb-source-data | REST | GET /decision-log/{entryId} | OpenAPI 3.1, /api/recovery/decision/v1 | C | RWB-P1-E1066-CON |
| P3 rwb-case | P1 rwb-source-data | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| P3 rwb-case | P1 rwb-source-data | Kafka | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| P3 rwb-case | P1 rwb-source-data | Kafka | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| P3 rwb-case | P1 rwb-source-data | Kafka | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| P5 rwb-document | P1 rwb-source-data | Kafka | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | RD-P1-003; RD-P1-009 |
| All 19 services | P1 rwb-source-data | Kafka | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | RD-P1-003; RD-P1-009 |
| P1 rwb-source-data | P6 rwb-comms | REST | GET /customers/{personKey} (recipient name and postal address for notices) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| P1 rwb-source-data | P2 rwb-integration | REST | GET /customers/{personKey} (INT-14 outbound file) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| P1 rwb-source-data | P3 rwb-case | REST | GET /customers/{personKey}; GET /accounts/{accountKey}; GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| P1 rwb-source-data | P8 rwb-payment | REST | GET /accounts/{accountKey} (fee facts) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| P1 rwb-source-data | S5 rwb-asset | REST | GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060; RD-P1-069 |
| P1 rwb-source-data | P8 rwb-payment | REST | GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-066 |
| P1 rwb-source-data | P2 rwb-integration | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RD-P1-066 |
| P1 rwb-source-data | gateway-bff | REST | GET /payments?accountKey= | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-061 |
| P1 rwb-source-data | P5 rwb-document | REST | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| P1 rwb-source-data | P8 rwb-payment | REST | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| P1 rwb-source-data | S2 rwb-treatment | REST | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| P1 rwb-source-data | S9 rwb-partner | REST | POST /cases/{caseId}/interactions (partner results) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| P1 rwb-source-data | S5 rwb-asset | REST | GET /cases/{caseId}/interactions (notice delivery state) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| P4 rwb-access | P1 rwb-source-data | REST | POST /authorise (request and answer pending, GAP-3322) | OpenAPI 3.1, /api/recovery/access/v1 | C | RD-P1-063 |

The same inventory is the Contract pairs sheet of the workbook next to this document.

# 6. Service contracts

One section per service, in Ownership Map order: platform services P1 to P10, then the route services S1 to S9. Each section has the identity and the contract artefacts, the contracts the service provides, the contracts it consumes, and the REST operations the Ownership Map assigns to it. A row under Temporal that names another service is a call the service makes on that service's queue; a row that names no other service is its own work and is not a contract.

The REST operations are the operation set of the Ownership Map v1 Endpoints sheet. The per-service base path applies to every operation of that service (Template and Rules §R4); the final per-service paths and payloads are written in API Specification v5 (GAP-0100; ASM-0169).

## 6.1 P1 rwb-source-data — Source data

| Item | Value |
|---|---|
| Service code | P1 |
| Service | rwb-source-data |
| Service name | Source data |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P1 |
| Schema and login | rwb_source_data |
| REST base | /api/recovery/source-data/v1 |
| Kafka topic | rwb.source-data.events.v1 |
| Retry and dead-letter topics | rwb.source-data.events.v1.retry.1m, rwb.source-data.events.v1.retry.10m, rwb.source-data.events.v1.retry.1h, rwb.source-data.events.v1.dlt |
| Temporal task queue | rwb-source-data |
| Java package | th.co.scb.ace.workbench.recovery.sourcedata |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/source-data/v1; AsyncAPI 3.0 for rwb.source-data.events.v1; activity contract jar on rwb-source-data |
| Owns (Arch v5 slide 41) | ACE view contract, extension tables, freshness, reconciliation, product-to-source map (RD-P1-021) |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | gateway-bff | AceDataLate | AsyncAPI 3.0, rwb.source-data.events.v1 | X | slide 42, slide 43 (EV-27) |
| Kafka | P3 rwb-case | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| Kafka | P8 rwb-payment | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| Kafka | S7 rwb-writeoff | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| Kafka | S8 rwb-deviation | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | slide 42, slide 43 (EV-26) |
| REST | gateway-bff | GET /customers/{personKey}; GET /accounts/{accountKey}; GET /data-products/freshness (composite case screen, one hop each in parallel) | OpenAPI 3.1, /api/recovery/source-data/v1 | X | slide 15, slide 20; RD-P1-060 |
| REST | P10 rwb-agent | Tool: read case facts (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 16 |
| REST | S1 rwb-valuation | Collateral and appraisals (GET /collateral/{assetKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 18; RD-P1-060 |
| REST | S7 rwb-writeoff | GL outcome | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 20 |
| REST | S8 rwb-deviation | Party flags (GET /customers/{personKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | slide 13, slide 15; RD-P1-060 |
| Temporal | P3 rwb-case | Activity: listEligibleAccounts(EligibleAccountsRequest) | Activity contract jar on task queue rwb-source-data | C | slide 14 |
| Temporal | P8 rwb-payment | Activity: payments for business date | Activity contract jar on task queue rwb-source-data | C | slide 13, slide 17 |
| Temporal | P9 rwb-reporting | Activity: snapshot(page) for measures | Activity contract jar on task queue rwb-source-data | C | slide 13, slide 15 |
| REST | P2 rwb-integration | GET /efs-history | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-010 |
| REST | P2 rwb-integration | POST /cases/{caseId}/interactions (EFS history, one call per row) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| REST | P2 rwb-integration | GET /booking-facts; GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2007-APP |
| REST | P3 rwb-case | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| REST | P3 rwb-case | Account-page read for a page of account keys (path and keys per call pending, GAP-3274) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-024 |
| REST | P6 rwb-comms | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007 |
| REST | P6 rwb-comms | GET /proof-of-delivery | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-007; RWB-P1-E1055-APP |
| REST | P6 rwb-comms | GET /contact-points; POST /contact-points/{contactPointKey}/failed-contacts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2022-APP |
| REST | P6 rwb-comms | GET /data-products/{productCode}/records (DP02 contact rows) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2021-APP |
| REST | P8 rwb-payment | GET /payments?businessDate=; GET /accounts/{accountKey}/installment-facts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-P1-E2008-APP |
| REST | P5 rwb-document | POST /retention-runs; GET /retention-runs/{runId} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-047 |
| REST | P9 rwb-reporting | GET /payments?accountKey= (baseline measures) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-022; RD-P1-061 |
| REST | gateway-bff | PUT /extension-facts/parties/{personKey}; PUT /extension-facts/accounts/{accountKey} (exclusion screen) | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-006; RWB-P1-E1018-APP |
| REST | ACE Airflow | POST /business-days/{date}/ready; GET /business-days/{date}/status | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-005; slide 32 |
| REST | P6 rwb-comms | GET /customers/{personKey} (recipient name and postal address for notices) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| REST | P2 rwb-integration | GET /customers/{personKey} (INT-14 outbound file) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| REST | P3 rwb-case | GET /customers/{personKey}; GET /accounts/{accountKey}; GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| REST | P8 rwb-payment | GET /accounts/{accountKey} (fee facts) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060 |
| REST | S5 rwb-asset | GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-060; RD-P1-069 |
| REST | P8 rwb-payment | GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-066 |
| Kafka | P2 rwb-integration | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RD-P1-066 |
| REST | gateway-bff | GET /payments?accountKey= | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RD-P1-061 |
| REST | P5 rwb-document | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| REST | P8 rwb-payment | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| REST | S2 rwb-treatment | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| REST | S9 rwb-partner | POST /cases/{caseId}/interactions (partner results) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |
| REST | S5 rwb-asset | GET /cases/{caseId}/interactions (notice delivery state) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RD-P1-064 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| SQL view | ACE database | SELECT on the 30 recovery.v_ace_* views, read only (ADR-010) | View contract, SELECT only | X | The edge stub named in section 8.4 | slide 13, slide 15 |
| REST | P2 rwb-integration | GET /admin/scheduled-jobs | OpenAPI 3.1, /api/recovery/integration/v1 | C | The provider's published contract and its fake | RD-P1-021 |
| REST | P3 rwb-case | GET /cases/{caseId}; GET /cases/{caseId}/accounts | OpenAPI 3.1, /api/recovery/case/v1 | C | The provider's published contract and its fake | RD-P1-007; RD-P1-024 |
| REST | P3 rwb-case | GET /cases/retention-exclusions; GET /cases/closure-dates | OpenAPI 3.1, /api/recovery/case/v1 | C | The provider's published contract and its fake | RD-P1-047 |
| REST | P3 rwb-case | GET /parameters/{key}; GET /admin/lists/{listCode} | OpenAPI 3.1, /api/recovery/case/v1 | C | The provider's published contract and its fake | RD-P1-028 |
| REST | P3 rwb-case | Reference load apply handler for the P1 table codes | OpenAPI 3.1, /api/recovery/case/v1 | C | The provider's published contract and its fake | RD-P1-020 |
| REST | P3 rwb-case | Open-case key list and allocation state for a business date (paths pending, GAP-3273) | OpenAPI 3.1, /api/recovery/case/v1 | C | The provider's published contract and its fake | RD-P1-022; RD-P1-040 |
| REST | P5 rwb-document | Retention classes read | OpenAPI 3.1, /api/recovery/document/v1 | C | The provider's published contract and its fake | RWB-P1-E1016-APP |
| REST | P7 rwb-decision | GET /decision-log/{entryId} | OpenAPI 3.1, /api/recovery/decision/v1 | C | The provider's published contract and its fake | RWB-P1-E1066-CON |
| Kafka | P3 rwb-case | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| Kafka | P3 rwb-case | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| Kafka | P3 rwb-case | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| Kafka | P3 rwb-case | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| Kafka | P5 rwb-document | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| Kafka | All 19 services | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | The provider's published contract and its fake | RD-P1-003; RD-P1-009 |
| REST | P4 rwb-access | POST /authorise (request and answer pending, GAP-3322) | OpenAPI 3.1, /api/recovery/access/v1 | C | The provider's published contract and its fake | RD-P1-063 |

The list below is the operation list of rwb-source-data.yaml 5.1.0 (API Specification v7), 32 operations (RD-P1-005, RD-P1-060). The tracker and data quality exception operations of API Specification v4 are not in it (removed under D-RCV-35). The account-page read of RD-P1-024 is added when its path is fixed (GAP-3274).

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /accounts/{accountKey} | /api/recovery/source-data/v1/accounts/{accountKey} | P1 |
| GET /accounts/{accountKey}/installment-facts | /api/recovery/source-data/v1/accounts/{accountKey}/installment-facts | P1 |
| GET /admin/data-contracts | /api/recovery/source-data/v1/admin/data-contracts | P1 |
| GET /admin/data-dictionary/fields | /api/recovery/source-data/v1/admin/data-dictionary/fields | P1 |
| GET /admin/data-products | /api/recovery/source-data/v1/admin/data-products | P1 |
| GET /admin/jobs | /api/recovery/source-data/v1/admin/jobs | P1 |
| GET /admin/reconciliation/results | /api/recovery/source-data/v1/admin/reconciliation/results | P1 |
| GET /admin/reconciliation/results/{resultId} | /api/recovery/source-data/v1/admin/reconciliation/results/{resultId} | P1 |
| GET /batch-status | /api/recovery/source-data/v1/batch-status | P1 |
| GET /booking-facts | /api/recovery/source-data/v1/booking-facts | P1 |
| GET /business-days/{date}/status | /api/recovery/source-data/v1/business-days/{date}/status | P1 |
| GET /cases/{caseId}/interactions | /api/recovery/source-data/v1/cases/{caseId}/interactions | P1 |
| GET /cases/{caseId}/interactions/{entryId} | /api/recovery/source-data/v1/cases/{caseId}/interactions/{entryId} | P1 |
| GET /collateral/{assetKey} | /api/recovery/source-data/v1/collateral/{assetKey} | P1 |
| GET /contact-points | /api/recovery/source-data/v1/contact-points | P1 |
| GET /customers/{personKey} | /api/recovery/source-data/v1/customers/{personKey} | P1 |
| GET /data-products/freshness | /api/recovery/source-data/v1/data-products/freshness | P1 |
| GET /data-products/{productCode}/records | /api/recovery/source-data/v1/data-products/{productCode}/records | P1 |
| GET /efs-history | /api/recovery/source-data/v1/efs-history | P1 |
| GET /payments | /api/recovery/source-data/v1/payments | P1 |
| GET /proof-of-delivery | /api/recovery/source-data/v1/proof-of-delivery | P1 |
| GET /retention-runs/{runId} | /api/recovery/source-data/v1/retention-runs/{runId} | P1 |
| PATCH /admin/data-contracts/{contractId} | /api/recovery/source-data/v1/admin/data-contracts/{contractId} | P1 |
| PATCH /admin/data-dictionary/fields/{fieldCode} | /api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode} | P1 |
| POST /admin/data-contracts/{contractId}/publish | /api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish | P1 |
| POST /admin/jobs/{jobId}/rerun | /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun | P1 |
| POST /business-days/{date}/ready | /api/recovery/source-data/v1/business-days/{date}/ready | P1 |
| POST /cases/{caseId}/interactions | /api/recovery/source-data/v1/cases/{caseId}/interactions | P1 |
| POST /contact-points/{contactPointKey}/failed-contacts | /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts | P1 |
| POST /retention-runs | /api/recovery/source-data/v1/retention-runs | P1 |
| PUT /extension-facts/accounts/{accountKey} | /api/recovery/source-data/v1/extension-facts/accounts/{accountKey} | P1 |
| PUT /extension-facts/parties/{personKey} | /api/recovery/source-data/v1/extension-facts/parties/{personKey} | P1 |

**Workflows, schedules and events (RD-P1-002, 003, 022, 040, 047)**

| Workflow | Workflow ID | Started by | Activities |
|---|---|---|---|
| AceIngestCheck | ace-ingest-check-{businessDate} | Readiness handler, the 05:30 Schedule rwb-source-data-ace-late-check and the fallback poll | readBatchStatus, stampProducts, markStale, checkDailyCompleteness |
| ReconciliationWorkflow (JOB-04) | recon-{businessDate} | Child of AceIngestCheck after the ALS stamp; admin rerun | reconciliation |
| Stage2ProductWorkflow | stage2-dp04-{businessDate} | Child of AceIngestCheck after the ALS stamp | readDp04SourcePage, writeDp04Page, checkActiveCount, stampDp04 |
| RetentionRunWorkflow | retention-run-{runDate} | POST /retention-runs | Eight activities (Temporal Workflow and Activity Catalog) |

Task queue rwb-source-data; no case-list workflow or Schedule exists in P1 (RD-P1-024). Provided activities: listEligibleAccounts and snapshot(page); provided query: FreshnessQuery (Service Catalog v2 section 6.1). AceDataReady and AceDataLate are written through the outbox with record key {sourceSystem}:{businessDate}; rwb-source-data does not consume its own topic and reads rwb.case.events.v1, rwb.document.events.v1 and rwb.decision-record.v1 for the ledger intake, one consumer group per topic (RD-P1-003, RD-P1-009). Consumers of AceDataReady are rwb-case, rwb-payment, rwb-integration, rwb-deviation and rwb-writeoff, each with one consumer group <service>.rwb.source-data.events.v1; every consumer has WRITE and READ on the retry topics and WRITE on the .dlt topic of each topic it reads (RD-P1-066). Pending: whether the slide 17 payments activity is replaced by GET /payments, owner solution architect, tracked as GAP-3556.

**Schema boundary**

- Writes rwb_source_data only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).
- Reads the 30 recovery.v_ace_* views, SELECT only; the only service with that grant (ADR-010).

## 6.2 P2 rwb-integration — Integration

| Item | Value |
|---|---|
| Service code | P2 |
| Service | rwb-integration |
| Service name | Integration |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P2 |
| Schema and login | rwb_integration |
| REST base | /api/recovery/integration/v1 |
| Kafka topic | rwb.integration.events.v1 |
| Retry and dead-letter topics | rwb.integration.events.v1.retry.1m, rwb.integration.events.v1.retry.10m, rwb.integration.events.v1.retry.1h, rwb.integration.events.v1.dlt |
| Temporal task queue | rwb-integration |
| Java package | th.co.scb.ace.workbench.recovery.integration |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/integration/v1; AsyncAPI 3.0 for rwb.integration.events.v1; activity contract jar on rwb-integration |
| Owns (Arch v5 slide 41) | interface config, file runs, outbound items, ACE integration paths |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| File | Outside the cluster | WIN registered mail, daily outbound file (INT-14); debt buyers, per lot, encrypted (INT-25) | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 16 |
| Kafka | The requesting service | FileDelivered | AsyncAPI 3.0, rwb.integration.events.v1 | X | slide 43 (event catalogue, not numbered) |
| Kafka | The requesting service | FileFailed | AsyncAPI 3.0, rwb.integration.events.v1 | X | slide 43 (event catalogue, not numbered) |
| Temporal | P6 rwb-comms | Activity: deliverFile (WIN letters) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 17 |
| Temporal | P8 rwb-payment | Activity: deliverFile (posting file) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 17 |
| Temporal | P9 rwb-reporting | Activity: deliverFile (regulatory extract) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 15 |
| Temporal | S6 rwb-debtsale | Activity: deliverFile (buyer file) | Activity contract jar on task queue rwb-integration | C | slide 13, slide 19 |
| REST | P1 rwb-source-data | GET /admin/scheduled-jobs | OpenAPI 3.1, /api/recovery/integration/v1 | C | RD-P1-021 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| REST | P5 rwb-document | Fetch file by ID (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | The provider's published contract and its fake | slide 13, slide 16 |
| REST | P1 rwb-source-data | GET /efs-history | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-010 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions (EFS history, one call per row) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-007 |
| REST | P1 rwb-source-data | GET /booking-facts; GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RWB-P1-E2007-APP |
| REST | P1 rwb-source-data | GET /customers/{personKey} (INT-14 outbound file) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-060 |
| Kafka | P1 rwb-source-data | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | The provider's published contract and its fake | RD-P1-066 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/outbound-items | /api/recovery/integration/v1/admin/outbound-items | P2 |
| GET /admin/outbox/deliveries | /api/recovery/integration/v1/admin/outbox/deliveries | P2 |
| GET /admin/scheduled-jobs | /api/recovery/integration/v1/admin/scheduled-jobs | P2 |
| GET /cases/{caseId}/customer-products | /api/recovery/integration/v1/cases/{caseId}/customer-products | P2 |
| GET /cases/{caseId}/plan-status | /api/recovery/integration/v1/cases/{caseId}/plan-status | P2 |
| GET /treatments/{treatmentId}/credit-pack | /api/recovery/integration/v1/treatments/{treatmentId}/credit-pack | P2 |
| GET /treatments/{treatmentId}/credit-result | /api/recovery/integration/v1/treatments/{treatmentId}/credit-result | P2 |
| POST /admin/interfaces/{interfaceCode}/manual-retirement | /api/recovery/integration/v1/admin/interfaces/{interfaceCode}/manual-retirement | P2 |
| POST /admin/outbound-items/{itemId}/resend | /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend | P2 |
| POST /admin/outbox/deliveries/{deliveryId}/resend | /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend | P2 |
| POST /treatments/{treatmentId}/credit-result | /api/recovery/integration/v1/treatments/{treatmentId}/credit-result | P2 |

**Schema boundary**

- Writes rwb_integration only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.3 P3 rwb-case — Case and workflow

| Item | Value |
|---|---|
| Service code | P3 |
| Service | rwb-case |
| Service name | Case and workflow |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P3 |
| Schema and login | rwb_case |
| REST base | /api/recovery/case/v1 |
| Kafka topic | rwb.case.events.v1 |
| Retry and dead-letter topics | rwb.case.events.v1.retry.1m, rwb.case.events.v1.retry.10m, rwb.case.events.v1.retry.1h, rwb.case.events.v1.dlt |
| Temporal task queue | rwb-case |
| Java package | th.co.scb.ace.workbench.recovery.case |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/case/v1; AsyncAPI 3.0 for rwb.case.events.v1; activity contract jar on rwb-case |
| Owns (Arch v5 slide 41) | case, CMMN state, queues, tasks, allocation, timers |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | gateway-bff | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | X | slide 42, slide 43 (EV-19) |
| Kafka | P10 rwb-agent | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| Kafka | P3 rwb-case | CaseAllocationFailed | AsyncAPI 3.0, rwb.case.events.v1 | H | slide 42, slide 43 (EV-03) |
| Kafka | P6 rwb-comms | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-05) |
| Kafka | P9 rwb-reporting | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-02) |
| Kafka | P9 rwb-reporting | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| Kafka | P9 rwb-reporting | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-05) |
| Kafka | P9 rwb-reporting | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-04) |
| Kafka | S8 rwb-deviation | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | slide 42, slide 43 (EV-01) |
| REST | gateway-bff | GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id} | OpenAPI 3.1, /api/recovery/case/v1 | X | slide 14, slide 20 |
| REST | P1 rwb-source-data | GET /cases/{caseId}; GET /cases/{caseId}/accounts | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-007; RD-P1-024 |
| REST | P1 rwb-source-data | GET /cases/retention-exclusions; GET /cases/closure-dates | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-047 |
| REST | P1 rwb-source-data | GET /parameters/{key}; GET /admin/lists/{listCode} | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-028 |
| REST | P1 rwb-source-data | Reference load apply handler for the P1 table codes | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-020 |
| REST | P1 rwb-source-data | Open-case key list and allocation state for a business date (paths pending, GAP-3273) | OpenAPI 3.1, /api/recovery/case/v1 | C | RD-P1-022; RD-P1-040 |
| Kafka | P1 rwb-source-data | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| Kafka | P1 rwb-source-data | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| Kafka | P1 rwb-source-data | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |
| Kafka | P1 rwb-source-data | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | C | RD-P1-003; RD-P1-009 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P1 rwb-source-data | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-26) |
| Kafka | P3 rwb-case | CaseAllocationFailed | AsyncAPI 3.0, rwb.case.events.v1 | H | Its own contract and its own contract test | slide 42, slide 43 (EV-03) |
| Kafka | P5 rwb-document | DocumentFieldsExtracted | AsyncAPI 3.0, rwb.document.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-17) |
| Kafka | P5 rwb-document | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-16) |
| Kafka | P6 rwb-comms | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-15) |
| Kafka | P7 rwb-decision | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-30) |
| Kafka | P8 rwb-payment | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-12) |
| Kafka | P8 rwb-payment | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-25) |
| Kafka | P8 rwb-payment | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-11) |
| Kafka | S1 rwb-valuation | RouteDecided | AsyncAPI 3.0, rwb.valuation.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S2 rwb-treatment | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S3 rwb-guarantee | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S3 rwb-guarantee | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S4 rwb-litigation | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S4 rwb-litigation | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S5 rwb-asset | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S5 rwb-asset | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-22) |
| Kafka | S6 rwb-debtsale | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S6 rwb-debtsale | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-23) |
| Kafka | S7 rwb-writeoff | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-24) |
| Kafka | S8 rwb-deviation | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-07) |
| Kafka | S8 rwb-deviation | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-06) |
| Kafka | S9 rwb-partner | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-21) |
| REST | P4 rwb-access | POST /authorise (role, scope, DoA), cached in rwb-case | OpenAPI 3.1, /api/recovery/access/v1 | C | The provider's published contract and its fake | slide 13, slide 14 |
| Temporal | P1 rwb-source-data | Activity: listEligibleAccounts(EligibleAccountsRequest) | Activity contract jar on task queue rwb-source-data | C | The provider's published contract and its fake | slide 14 |
| Temporal | S1 rwb-valuation | Child workflow: RouteDecisionWorkflow | Activity contract jar on task queue rwb-valuation | C | The provider's published contract and its fake | slide 14, slide 18 |
| Temporal | S2 rwb-treatment | Child workflow: the treatment stage workflows (TreatmentWorkflow) | Activity contract jar on task queue rwb-treatment | C | The provider's published contract and its fake | slide 14, slide 18 |
| Temporal | S3 rwb-guarantee | Child workflow: GuaranteeClaimWorkflow | Activity contract jar on task queue rwb-guarantee | C | The provider's published contract and its fake | slide 14, slide 18 |
| Temporal | S4 rwb-litigation | Child workflow: LitigationWorkflow | Activity contract jar on task queue rwb-litigation | C | The provider's published contract and its fake | slide 14, slide 19 |
| Temporal | S5 rwb-asset | Child workflow: AssetDisposalWorkflow | Activity contract jar on task queue rwb-asset | C | The provider's published contract and its fake | slide 14, slide 19 |
| Temporal | S6 rwb-debtsale | Child workflow: DebtSaleWorkflow | Activity contract jar on task queue rwb-debtsale | C | The provider's published contract and its fake | slide 14, slide 19 |
| Temporal | S7 rwb-writeoff | Child workflow: WriteOffWorkflow | Activity contract jar on task queue rwb-writeoff | C | The provider's published contract and its fake | slide 14, slide 20 |
| Temporal | S8 rwb-deviation | Child workflow: DeviationWorkflow | Activity contract jar on task queue rwb-deviation | C | The provider's published contract and its fake | slide 14, slide 15 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-007 |
| REST | P1 rwb-source-data | Account-page read for a page of account keys (path and keys per call pending, GAP-3274) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-024 |
| REST | P1 rwb-source-data | GET /customers/{personKey}; GET /accounts/{accountKey}; GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-060 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/change-log | /api/recovery/case/v1/admin/change-log | P3 |
| GET /admin/lists/{listCode} | /api/recovery/case/v1/admin/lists/{listCode} | P3 |
| GET /admin/parameters | /api/recovery/case/v1/admin/parameters | P3 |
| GET /cases | /api/recovery/case/v1/cases | P3 |
| GET /cases/export | /api/recovery/case/v1/cases/export | P3 |
| GET /cases/{caseId} | /api/recovery/case/v1/cases/{caseId} | P3 |
| GET /cases/{caseId}/accounts | /api/recovery/case/v1/cases/{caseId}/accounts | P3 |
| GET /cases/{caseId}/next-action | /api/recovery/case/v1/cases/{caseId}/next-action | P3 |
| GET /cases/{caseId}/parties | /api/recovery/case/v1/cases/{caseId}/parties | P3 |
| GET /cases/{caseId}/timeline | /api/recovery/case/v1/cases/{caseId}/timeline | P3 |
| GET /cases/{caseId}/timers | /api/recovery/case/v1/cases/{caseId}/timers | P3 |
| GET /me/tasks | /api/recovery/case/v1/me/tasks | P3 |
| GET /parameters/{key} | /api/recovery/case/v1/parameters/{key} | P3 |
| GET /queues | /api/recovery/case/v1/queues | P3 |
| GET /queues/{queueId}/cases | /api/recovery/case/v1/queues/{queueId}/cases | P3 |
| PATCH /tasks/{taskId} | /api/recovery/case/v1/tasks/{taskId} | P3 |
| POST /admin/reference-loads | /api/recovery/case/v1/admin/reference-loads | P3 |
| POST /admin/reference-loads/{loadId}/approve | /api/recovery/case/v1/admin/reference-loads/{loadId}/approve | P3 |
| POST /admin/reference-loads/{loadId}/rollback | /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback | P3 |
| POST /admin/reference-loads/{loadId}/verify | /api/recovery/case/v1/admin/reference-loads/{loadId}/verify | P3 |
| POST /cases/{caseId}/legal-hold | /api/recovery/case/v1/cases/{caseId}/legal-hold | P3 |
| POST /cases/{caseId}/transfer | /api/recovery/case/v1/cases/{caseId}/transfer | P3 |
| POST /queues/{queueId}/placements | /api/recovery/case/v1/queues/{queueId}/placements | P3 |
| GET /cases/closure-dates | /api/recovery/case/v1/cases/closure-dates | P3 |
| GET /cases/retention-exclusions | /api/recovery/case/v1/cases/retention-exclusions | P3 |

**Schema boundary**

- Writes rwb_case only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).
- Owns the case list API, the parameters and the reference data by the R-PREC default ruling (E1-042, E1-043).

## 6.4 P4 rwb-access — Access and authority

| Item | Value |
|---|---|
| Service code | P4 |
| Service | rwb-access |
| Service name | Access and authority |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P4 |
| Schema and login | rwb_access |
| REST base | /api/recovery/access/v1 |
| Kafka topic | rwb.access.events.v1 |
| Retry and dead-letter topics | rwb.access.events.v1.retry.1m, rwb.access.events.v1.retry.10m, rwb.access.events.v1.retry.1h, rwb.access.events.v1.dlt |
| Temporal task queue | rwb-access |
| Java package | th.co.scb.ace.workbench.recovery.access |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/access/v1; AsyncAPI 3.0 for rwb.access.events.v1; activity contract jar on rwb-access |
| Owns (Arch v5 slide 41) | Recovery roles as data, scope, masking policy, DoA table, access log |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | All 19 services | AccessPolicyChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | All 19 services | DoaLimitChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | slide 43 (event catalogue, not numbered) |
| REST | P3 rwb-case | POST /authorise (role, scope, DoA), cached in rwb-case | OpenAPI 3.1, /api/recovery/access/v1 | C | slide 13, slide 14 |
| REST | P7 rwb-decision | GET /doa-limits (DoA limits) | OpenAPI 3.1, /api/recovery/access/v1 | C | slide 13, slide 14 |
| REST | P1 rwb-source-data | POST /authorise (request and answer pending, GAP-3322) | OpenAPI 3.1, /api/recovery/access/v1 | C | RD-P1-063 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| REST | ACE Common | Sign-in, group-to-role (Entra ID) | ACE Common API (sign-in, notification path) | X | The edge stub named in section 8.4 | slide 13, slide 14 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/access-log | /api/recovery/access/v1/admin/access-log | P4 |
| GET /admin/roles | /api/recovery/access/v1/admin/roles | P4 |
| GET /me/session | /api/recovery/access/v1/me/session | P4 |
| POST /admin/break-glass-grants | /api/recovery/access/v1/admin/break-glass-grants | P4 |
| POST /authorise | /api/recovery/access/v1/authorise | P4 |

**Schema boundary**

- Writes rwb_access only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.5 P5 rwb-document — Document

| Item | Value |
|---|---|
| Service code | P5 |
| Service | rwb-document |
| Service name | Document |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P5 |
| Schema and login | rwb_document |
| REST base | /api/recovery/document/v1 |
| Kafka topic | rwb.document.events.v1 |
| Retry and dead-letter topics | rwb.document.events.v1.retry.1m, rwb.document.events.v1.retry.10m, rwb.document.events.v1.retry.1h, rwb.document.events.v1.dlt |
| Temporal task queue | rwb-document |
| Java package | th.co.scb.ace.workbench.recovery.document |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/document/v1; AsyncAPI 3.0 for rwb.document.events.v1; activity contract jar on rwb-document |
| Owns (Arch v5 slide 41) | metadata, custody, OCR text and fields, signatures, retention |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| File | Outside the cluster | Azure Blob (WORM): files, 2.8 TB by 2031 | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 16 |
| Kafka | P10 rwb-agent | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-16) |
| Kafka | P3 rwb-case | DocumentFieldsExtracted | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-17) |
| Kafka | P3 rwb-case | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | slide 42, slide 43 (EV-16) |
| REST | P10 rwb-agent | Tool: read extracted fields (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 16 |
| REST | P2 rwb-integration | Fetch file by ID (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 16 |
| REST | S9 rwb-partner | Partner uploads (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | slide 13, slide 17 |
| Temporal | P6 rwb-comms | Document: generate letter | Activity contract jar on task queue rwb-document | C | slide 13, slide 17 |
| Temporal | S2 rwb-treatment | Contract document generation and e-sign | Activity contract jar on task queue rwb-document | C | slide 13, slide 18 |
| Temporal | S6 rwb-debtsale | Document: data room pack | Activity contract jar on task queue rwb-document | C | slide 13, slide 19 |
| REST | P1 rwb-source-data | Retention classes read | OpenAPI 3.1, /api/recovery/document/v1 | C | RWB-P1-E1016-APP |
| Kafka | P1 rwb-source-data | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | RD-P1-003; RD-P1-009 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P10 rwb-agent | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-28) |
| Temporal | P10 rwb-agent | Child workflow: classify / extract run | Activity contract jar on task queue rwb-agent | C | The provider's published contract and its fake | slide 13, slide 16 |
| REST | P1 rwb-source-data | POST /retention-runs; GET /retention-runs/{runId} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-047 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-064 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /cases/{caseId}/document-checklist | /api/recovery/document/v1/cases/{caseId}/document-checklist | P5 |
| GET /cases/{caseId}/documents | /api/recovery/document/v1/cases/{caseId}/documents | P5 |
| GET /documents | /api/recovery/document/v1/documents | P5 |
| GET /documents/{documentId} | /api/recovery/document/v1/documents/{documentId} | P5 |
| GET /documents/{documentId}/content | /api/recovery/document/v1/documents/{documentId}/content | P5 |
| GET /intake-items/{intakeItemId} | /api/recovery/document/v1/intake-items/{intakeItemId} | P5 |
| GET /intake-items/{intakeItemId}/content | /api/recovery/document/v1/intake-items/{intakeItemId}/content | P5 |
| GET /review-items | /api/recovery/document/v1/review-items | P5 |
| PATCH /documents/{documentId}/fields/{fieldId} | /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} | P5 |
| POST /cases/{caseId}/documents | /api/recovery/document/v1/cases/{caseId}/documents | P5 |
| POST /cases/{caseId}/field-captures | /api/recovery/document/v1/cases/{caseId}/field-captures | P5 |
| POST /cases/{caseId}/generated-documents | /api/recovery/document/v1/cases/{caseId}/generated-documents | P5 |
| POST /documents/{documentId}/custody | /api/recovery/document/v1/documents/{documentId}/custody | P5 |
| POST /documents/{documentId}/regenerate | /api/recovery/document/v1/documents/{documentId}/regenerate | P5 |
| POST /documents/{documentId}/review | /api/recovery/document/v1/documents/{documentId}/review | P5 |
| POST /documents/{documentId}/versions | /api/recovery/document/v1/documents/{documentId}/versions | P5 |
| POST /intake-items/{intakeItemId}/resolve | /api/recovery/document/v1/intake-items/{intakeItemId}/resolve | P5 |

**Schema boundary**

- Writes rwb_document only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.6 P6 rwb-comms — Communications

| Item | Value |
|---|---|
| Service code | P6 |
| Service | rwb-comms |
| Service name | Communications |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P6 |
| Schema and login | rwb_comms |
| REST base | /api/recovery/comms/v1 |
| Kafka topic | rwb.comms.events.v1 |
| Retry and dead-letter topics | rwb.comms.events.v1.retry.1m, rwb.comms.events.v1.retry.10m, rwb.comms.events.v1.retry.1h, rwb.comms.events.v1.dlt |
| Temporal task queue | rwb-comms |
| Java package | th.co.scb.ace.workbench.recovery.comms |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/comms/v1; AsyncAPI 3.0 for rwb.comms.events.v1; activity contract jar on rwb-comms |
| Owns (Arch v5 slide 41) | notices, templates, merge fields, proof of delivery |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| Kafka | P7 rwb-decision | NoticeGenerated | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-13) |
| Kafka | P9 rwb-reporting | NoticeDispatched | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-14) |
| Kafka | S3 rwb-guarantee | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| Kafka | S4 rwb-litigation | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | slide 42, slide 43 (EV-15) |
| Temporal | S3 rwb-guarantee | Child workflow: guarantor notice | Activity contract jar on task queue rwb-comms | C | slide 13, slide 18 |
| Temporal | S4 rwb-litigation | Child workflow: demand notice | Activity contract jar on task queue rwb-comms | C | slide 13, slide 19 |
| Temporal | S5 rwb-asset | Not specified in the source documents (GAP-0106; ASM-0175) | Activity contract jar on task queue rwb-comms | C | slide 13 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P3 rwb-case | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-05) |
| Kafka | P8 rwb-payment | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-12) |
| Kafka | S2 rwb-treatment | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-10) |
| Kafka | S8 rwb-deviation | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-07) |
| Kafka | S8 rwb-deviation | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-06) |
| REST | ACE Common | Notification path (SMS, LINE OA) | ACE Common API (sign-in, notification path) | X | The edge stub named in section 8.4 | slide 13, slide 17 |
| Temporal | P2 rwb-integration | Activity: deliverFile (WIN letters) | Activity contract jar on task queue rwb-integration | C | The provider's published contract and its fake | slide 13, slide 17 |
| Temporal | P5 rwb-document | Document: generate letter | Activity contract jar on task queue rwb-document | C | The provider's published contract and its fake | slide 13, slide 17 |
| Temporal | P7 rwb-decision | Child workflow: approval | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 17 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-007 |
| REST | P1 rwb-source-data | GET /proof-of-delivery | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-007; RWB-P1-E1055-APP |
| REST | P1 rwb-source-data | GET /contact-points; POST /contact-points/{contactPointKey}/failed-contacts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RWB-P1-E2022-APP |
| REST | P1 rwb-source-data | GET /data-products/{productCode}/records (DP02 contact rows) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RWB-P1-E2021-APP |
| REST | P1 rwb-source-data | GET /customers/{personKey} (recipient name and postal address for notices) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-060 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/templates | /api/recovery/comms/v1/admin/templates | P6 |
| GET /admin/templates/{templateId}/content | /api/recovery/comms/v1/admin/templates/{templateId}/content | P6 |
| GET /notices/{noticeId} | /api/recovery/comms/v1/notices/{noticeId} | P6 |
| GET /treatments/{treatmentId}/signature-requests | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | P6 |
| POST /admin/templates | /api/recovery/comms/v1/admin/templates | P6 |
| POST /admin/templates/{templateId}/approve | /api/recovery/comms/v1/admin/templates/{templateId}/approve | P6 |
| POST /admin/templates/{templateId}/withdraw | /api/recovery/comms/v1/admin/templates/{templateId}/withdraw | P6 |
| POST /cases/{caseId}/messages | /api/recovery/comms/v1/cases/{caseId}/messages | P6 |
| POST /cases/{caseId}/notices | /api/recovery/comms/v1/cases/{caseId}/notices | P6 |
| POST /signature-requests/{requestId}/result | /api/recovery/comms/v1/signature-requests/{requestId}/result | P6 |
| POST /treatments/{treatmentId}/signature-requests | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | P6 |

**Schema boundary**

- Writes rwb_comms only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.7 P7 rwb-decision — Decision and rules

| Item | Value |
|---|---|
| Service code | P7 |
| Service | rwb-decision |
| Service name | Decision and rules |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P7 |
| Schema and login | rwb_decision |
| REST base | /api/recovery/decision/v1 |
| Kafka topic | rwb.decision.events.v1 |
| Retry and dead-letter topics | rwb.decision.events.v1.retry.1m, rwb.decision.events.v1.retry.10m, rwb.decision.events.v1.retry.1h, rwb.decision.events.v1.dlt |
| Temporal task queue | rwb-decision |
| Java package | th.co.scb.ace.workbench.recovery.decision |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/decision/v1; AsyncAPI 3.0 for rwb.decision.events.v1; activity contract jar on rwb-decision |
| Owns (Arch v5 slide 41) | approvals, central decision ledger, DMN model registry |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| File | Outside the cluster | Immutable storage: daily ledger seal (WORM) | File manifest (fileId, batchId, sha256, record count) | X | slide 13, slide 14 |
| Kafka | gateway-bff | ApprovalRequested | AsyncAPI 3.0, rwb.decision.events.v1 | X | slide 42, slide 43 (EV-09) |
| Kafka | Not specified in the source documents (GAP-0102; ASM-0171) | ApprovalDecided | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P3 rwb-case | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| Kafka | P8 rwb-payment | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| Kafka | S1 rwb-valuation | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| Kafka | S2 rwb-treatment | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | slide 42, slide 43 (EV-30) |
| Temporal | P6 rwb-comms | Child workflow: approval | Activity contract jar on task queue rwb-decision | C | slide 13, slide 17 |
| Temporal | S1 rwb-valuation | Child workflow: ApprovalWorkflow (kit template) | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| Temporal | S2 rwb-treatment | Child workflow: ApprovalWorkflow (DoA) | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| Temporal | S3 rwb-guarantee | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 18 |
| Temporal | S4 rwb-litigation | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| Temporal | S5 rwb-asset | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| Temporal | S6 rwb-debtsale | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | slide 13, slide 19 |
| Temporal | S7 rwb-writeoff | Child workflow: committee approval | Activity contract jar on task queue rwb-decision | C | slide 13, slide 20 |
| REST | P1 rwb-source-data | GET /decision-log/{entryId} | OpenAPI 3.1, /api/recovery/decision/v1 | C | RWB-P1-E1066-CON |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | All 19 services | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-08) |
| Kafka | P10 rwb-agent | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-28) |
| Kafka | P6 rwb-comms | NoticeGenerated | AsyncAPI 3.0, rwb.comms.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-13) |
| REST | P4 rwb-access | GET /doa-limits (DoA limits) | OpenAPI 3.1, /api/recovery/access/v1 | C | The provider's published contract and its fake | slide 13, slide 14 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/rule-package-versions/{versionId}/dry-run | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run | P7 |
| GET /admin/rule-packages | /api/recovery/decision/v1/admin/rule-packages | P7 |
| GET /admin/rule-packages/change-report | /api/recovery/decision/v1/admin/rule-packages/change-report | P7 |
| GET /admin/rule-packages/{packageCode}/versions | /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | P7 |
| GET /admin/rule-versions | /api/recovery/decision/v1/admin/rule-versions | P7 |
| GET /approvals | /api/recovery/decision/v1/approvals | P7 |
| GET /approvals/{approvalId} | /api/recovery/decision/v1/approvals/{approvalId} | P7 |
| GET /cases/{caseId}/recommendation | /api/recovery/decision/v1/cases/{caseId}/recommendation | P7 |
| GET /decision-log | /api/recovery/decision/v1/decision-log | P7 |
| GET /decision-log/{entryId} | /api/recovery/decision/v1/decision-log/{entryId} | P7 |
| POST /admin/rule-package-versions/{versionId}/approve | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve | P7 |
| POST /admin/rule-package-versions/{versionId}/rollback | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback | P7 |
| POST /admin/rule-packages/{packageCode}/versions | /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | P7 |
| POST /admin/rule-versions | /api/recovery/decision/v1/admin/rule-versions | P7 |
| POST /admin/rule-versions/{versionId}/approve | /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve | P7 |
| POST /admin/rule-versions/{versionId}/rollback | /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback | P7 |
| POST /approvals/{approvalId}/approve | /api/recovery/decision/v1/approvals/{approvalId}/approve | P7 |
| POST /approvals/{approvalId}/refuse | /api/recovery/decision/v1/approvals/{approvalId}/refuse | P7 |
| POST /approvals/{approvalId}/return | /api/recovery/decision/v1/approvals/{approvalId}/return | P7 |

**Schema boundary**

- Writes rwb_decision only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).
- Owns the rule package registry by the R-PREC default ruling; every service evaluates its own rules with the package version it was told is in force.

## 6.8 P8 rwb-payment — Payment

| Item | Value |
|---|---|
| Service code | P8 |
| Service | rwb-payment |
| Service name | Payment |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-P8 |
| Schema and login | rwb_payment |
| REST base | /api/recovery/payment/v1 |
| Kafka topic | rwb.payment.events.v1 |
| Retry and dead-letter topics | rwb.payment.events.v1.retry.1m, rwb.payment.events.v1.retry.10m, rwb.payment.events.v1.retry.1h, rwb.payment.events.v1.dlt |
| Temporal task queue | rwb-payment |
| Java package | th.co.scb.ace.workbench.recovery.payment |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/payment/v1; AsyncAPI 3.0 for rwb.payment.events.v1; activity contract jar on rwb-payment |
| Owns (Arch v5 slide 41) | payment and proceeds matching, fees, bookings, posting files |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| Kafka | P3 rwb-case | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| Kafka | P3 rwb-case | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-11) |
| Kafka | P6 rwb-comms | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| Kafka | S2 rwb-treatment | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-12) |
| Kafka | S2 rwb-treatment | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-11) |
| Kafka | S3 rwb-guarantee | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| Kafka | S5 rwb-asset | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| Kafka | S6 rwb-debtsale | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| Kafka | S7 rwb-writeoff | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | slide 42, slide 43 (EV-25) |
| Temporal | S2 rwb-treatment | Activity: postProceeds (saga step) | Activity contract jar on task queue rwb-payment | C | slide 13, slide 18 |
| Temporal | S5 rwb-asset | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 19 |
| Temporal | S6 rwb-debtsale | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 19 |
| Temporal | S7 rwb-writeoff | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | slide 13, slide 20 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P1 rwb-source-data | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-26) |
| Kafka | P7 rwb-decision | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-30) |
| Kafka | S2 rwb-treatment | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-10) |
| Kafka | S5 rwb-asset | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S5 rwb-asset | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-22) |
| Kafka | S6 rwb-debtsale | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-23) |
| Kafka | S7 rwb-writeoff | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-24) |
| Temporal | P1 rwb-source-data | Activity: payments for business date | Activity contract jar on task queue rwb-source-data | C | The provider's published contract and its fake | slide 13, slide 17 |
| Temporal | P2 rwb-integration | Activity: deliverFile (posting file) | Activity contract jar on task queue rwb-integration | C | The provider's published contract and its fake | slide 13, slide 17 |
| REST | P1 rwb-source-data | GET /payments?businessDate=; GET /accounts/{accountKey}/installment-facts | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RWB-P1-E2008-APP |
| REST | P1 rwb-source-data | GET /accounts/{accountKey} (fee facts) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-060 |
| REST | P1 rwb-source-data | GET /batch-status | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-066 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-064 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /proceeds | /api/recovery/payment/v1/proceeds | P8 |
| POST /proceeds/{proceedsId}/match | /api/recovery/payment/v1/proceeds/{proceedsId}/match | P8 |

**Schema boundary**

- Writes rwb_payment only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.9 P9 rwb-reporting — Reporting

| Item | Value |
|---|---|
| Service code | P9 |
| Service | rwb-reporting |
| Service name | Reporting |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P9 |
| Schema and login | rwb_reporting |
| REST base | /api/recovery/reporting/v1 |
| Kafka topic | rwb.reporting.events.v1 |
| Retry and dead-letter topics | rwb.reporting.events.v1.retry.1m, rwb.reporting.events.v1.retry.10m, rwb.reporting.events.v1.retry.1h, rwb.reporting.events.v1.dlt |
| Temporal task queue | rwb-reporting |
| Java package | th.co.scb.ace.workbench.recovery.reporting |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/reporting/v1; AsyncAPI 3.0 for rwb.reporting.events.v1; activity contract jar on rwb-reporting |
| Owns (Arch v5 slide 41) | measures, snapshots, steering dashboard, regulatory reports |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | Not specified in the source documents (GAP-0102; ASM-0171) | ReportPublished | AsyncAPI 3.0, rwb.reporting.events.v1 | C | slide 43 (event catalogue, not numbered) |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | All 19 services | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-08) |
| Kafka | P3 rwb-case | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-02) |
| Kafka | P3 rwb-case | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-01) |
| Kafka | P3 rwb-case | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-05) |
| Kafka | P3 rwb-case | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-04) |
| Kafka | P6 rwb-comms | NoticeDispatched | AsyncAPI 3.0, rwb.comms.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-14) |
| Kafka | S2 rwb-treatment | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S3 rwb-guarantee | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S3 rwb-guarantee | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S6 rwb-debtsale | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S7 rwb-writeoff | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-24) |
| Temporal | P1 rwb-source-data | Activity: snapshot(page) for measures | Activity contract jar on task queue rwb-source-data | C | The provider's published contract and its fake | slide 13, slide 15 |
| Temporal | P2 rwb-integration | Activity: deliverFile (regulatory extract) | Activity contract jar on task queue rwb-integration | C | The provider's published contract and its fake | slide 13, slide 15 |
| REST | P1 rwb-source-data | GET /payments?accountKey= (baseline measures) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-022; RD-P1-061 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /reports/measures | /api/recovery/reporting/v1/reports/measures | P9 |

**Schema boundary**

- Writes rwb_reporting only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.10 P10 rwb-agent — Agent

| Item | Value |
|---|---|
| Service code | P10 |
| Service | rwb-agent |
| Service name | Agent |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P10 |
| Schema and login | rwb_agent |
| REST base | /api/recovery/agent/v1 |
| Kafka topic | rwb.agent.events.v1 |
| Retry and dead-letter topics | rwb.agent.events.v1.retry.1m, rwb.agent.events.v1.retry.10m, rwb.agent.events.v1.retry.1h, rwb.agent.events.v1.dlt |
| Temporal task queue | rwb-agent |
| Java package | th.co.scb.ace.workbench.recovery.agent |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/agent/v1; AsyncAPI 3.0 for rwb.agent.events.v1; activity contract jar on rwb-agent |
| Owns (Arch v5 slide 41) | agent policies, prompts, runs, guardrails, evaluations |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P5 rwb-document | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| Kafka | P7 rwb-decision | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| Kafka | S8 rwb-deviation | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | slide 42, slide 43 (EV-28) |
| Temporal | P5 rwb-document | Child workflow: classify / extract run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 16 |
| Temporal | S1 rwb-valuation | Child workflow: route agent run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 18 |
| Temporal | S8 rwb-deviation | Child workflow: screening agent run | Activity contract jar on task queue rwb-agent | C | slide 13, slide 15 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P3 rwb-case | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-01) |
| Kafka | P5 rwb-document | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-16) |
| REST | Outside the cluster | Enterprise AI private endpoint (INT-23), HTTPS | The external API or interface of that party | X | The edge stub named in section 8.4 | slide 13, slide 16 |
| REST | P1 rwb-source-data | Tool: read case facts (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | slide 13, slide 16 |
| REST | P5 rwb-document | Tool: read extracted fields (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/document/v1 | C | The provider's published contract and its fake | slide 13, slide 16 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /admin/agent-configs | /api/recovery/agent/v1/admin/agent-configs | P10 |
| GET /admin/agent-evaluations | /api/recovery/agent/v1/admin/agent-evaluations | P10 |
| GET /admin/agent-evaluations/{evaluationId}/report | /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report | P10 |
| GET /admin/agent-metrics | /api/recovery/agent/v1/admin/agent-metrics | P10 |
| GET /admin/agent-runs | /api/recovery/agent/v1/admin/agent-runs | P10 |
| GET /cases/{caseId}/agent-outputs | /api/recovery/agent/v1/cases/{caseId}/agent-outputs | P10 |
| POST /admin/agent-configs | /api/recovery/agent/v1/admin/agent-configs | P10 |
| POST /admin/agent-configs/{versionId}/approve | /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve | P10 |
| POST /admin/agent-evaluations | /api/recovery/agent/v1/admin/agent-evaluations | P10 |
| POST /admin/agent-samples | /api/recovery/agent/v1/admin/agent-samples | P10 |
| POST /agent-runs/{runId}/feedback | /api/recovery/agent/v1/agent-runs/{runId}/feedback | P10 |

**Schema boundary**

- Writes rwb_agent only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.11 S1 rwb-valuation — Valuation and route

| Item | Value |
|---|---|
| Service code | S1 |
| Service | rwb-valuation |
| Service name | Valuation and route |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S1 |
| Schema and login | rwb_valuation |
| REST base | /api/recovery/valuation/v1 |
| Kafka topic | rwb.valuation.events.v1 |
| Retry and dead-letter topics | rwb.valuation.events.v1.retry.1m, rwb.valuation.events.v1.retry.10m, rwb.valuation.events.v1.retry.1h, rwb.valuation.events.v1.dlt |
| Temporal task queue | rwb-valuation |
| Java package | th.co.scb.ace.workbench.recovery.valuation |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/valuation/v1; AsyncAPI 3.0 for rwb.valuation.events.v1; activity contract jar on rwb-valuation |
| Owns (Arch v5 slide 41) | valuations, D6 route decision, route agent output |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | RouteDecided | AsyncAPI 3.0, rwb.valuation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Temporal | P3 rwb-case | Child workflow: RouteDecisionWorkflow | Activity contract jar on task queue rwb-valuation | C | slide 14, slide 18 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P7 rwb-decision | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-30) |
| REST | P1 rwb-source-data | Collateral and appraisals (GET /collateral/{assetKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | slide 13, slide 18; RD-P1-060 |
| Temporal | P10 rwb-agent | Child workflow: route agent run | Activity contract jar on task queue rwb-agent | C | The provider's published contract and its fake | slide 13, slide 18 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow (kit template) | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 18 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| POST /assets/{assetId}/valuations | /api/recovery/valuation/v1/assets/{assetId}/valuations | S1 |
| POST /assets/{assetKey}/valuations | /api/recovery/valuation/v1/assets/{assetKey}/valuations | S1 |
| POST /cases/{caseId}/route | /api/recovery/valuation/v1/cases/{caseId}/route | S1 |

**Schema boundary**

- Writes rwb_valuation only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.12 S2 rwb-treatment — Treatment and offer

| Item | Value |
|---|---|
| Service code | S2 |
| Service | rwb-treatment |
| Service name | Treatment and offer |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S2 |
| Schema and login | rwb_treatment |
| REST base | /api/recovery/treatment/v1 |
| Kafka topic | rwb.treatment.events.v1 |
| Retry and dead-letter topics | rwb.treatment.events.v1.retry.1m, rwb.treatment.events.v1.retry.10m, rwb.treatment.events.v1.retry.1h, rwb.treatment.events.v1.dlt |
| Temporal task queue | rwb-treatment |
| Java package | th.co.scb.ace.workbench.recovery.treatment |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/treatment/v1; AsyncAPI 3.0 for rwb.treatment.events.v1; activity contract jar on rwb-treatment |
| Owns (Arch v5 slide 41) | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P6 rwb-comms | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 42, slide 43 (EV-10) |
| Kafka | P8 rwb-payment | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 42, slide 43 (EV-10) |
| Kafka | P9 rwb-reporting | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Temporal | P3 rwb-case | Child workflow: the treatment stage workflows (TreatmentWorkflow) | Activity contract jar on task queue rwb-treatment | C | slide 14, slide 18 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P7 rwb-decision | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-30) |
| Kafka | P8 rwb-payment | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-12) |
| Kafka | P8 rwb-payment | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-11) |
| Kafka | S8 rwb-deviation | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-06) |
| Nexus | ACE Common | restructure.calculate (Nexus operation, namespace ace-collection) | Nexus operation, ace-collection | X | The edge stub named in section 8.4 | slide 13, slide 18 |
| Temporal | P5 rwb-document | Contract document generation and e-sign | Activity contract jar on task queue rwb-document | C | The provider's published contract and its fake | slide 13, slide 18 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow (DoA) | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 18 |
| Temporal | P8 rwb-payment | Activity: postProceeds (saga step) | Activity contract jar on task queue rwb-payment | C | The provider's published contract and its fake | slide 13, slide 18 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-064 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /treatments/{treatmentId} | /api/recovery/treatment/v1/treatments/{treatmentId} | S2 |
| PATCH /treatments/{treatmentId} | /api/recovery/treatment/v1/treatments/{treatmentId} | S2 |
| POST /cases/{caseId}/treatments | /api/recovery/treatment/v1/cases/{caseId}/treatments | S2 |
| POST /treatments/{treatmentId}/submit | /api/recovery/treatment/v1/treatments/{treatmentId}/submit | S2 |

**Schema boundary**

- Writes rwb_treatment only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.13 S3 rwb-guarantee — Guarantee

| Item | Value |
|---|---|
| Service code | S3 |
| Service | rwb-guarantee |
| Service name | Guarantee |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S3 |
| Schema and login | rwb_guarantee |
| REST base | /api/recovery/guarantee/v1 |
| Kafka topic | rwb.guarantee.events.v1 |
| Retry and dead-letter topics | rwb.guarantee.events.v1.retry.1m, rwb.guarantee.events.v1.retry.10m, rwb.guarantee.events.v1.retry.1h, rwb.guarantee.events.v1.dlt |
| Temporal task queue | rwb-guarantee |
| Java package | th.co.scb.ace.workbench.recovery.guarantee |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/guarantee/v1; AsyncAPI 3.0 for rwb.guarantee.events.v1; activity contract jar on rwb-guarantee |
| Owns (Arch v5 slide 41) | TCG and insurance claims, guarantor notices and pursuit |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P3 rwb-case | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P9 rwb-reporting | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P9 rwb-reporting | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Temporal | P3 rwb-case | Child workflow: GuaranteeClaimWorkflow | Activity contract jar on task queue rwb-guarantee | C | slide 14, slide 18 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P6 rwb-comms | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-15) |
| Kafka | P8 rwb-payment | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-25) |
| Temporal | P6 rwb-comms | Child workflow: guarantor notice | Activity contract jar on task queue rwb-comms | C | The provider's published contract and its fake | slide 13, slide 18 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 18 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| PATCH /guarantee-claims/{claimId} | /api/recovery/guarantee/v1/guarantee-claims/{claimId} | S3 |
| POST /cases/{caseId}/guarantee-claims | /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims | S3 |

**Schema boundary**

- Writes rwb_guarantee only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.14 S4 rwb-litigation — Litigation

| Item | Value |
|---|---|
| Service code | S4 |
| Service | rwb-litigation |
| Service name | Litigation |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S4 |
| Schema and login | rwb_litigation |
| REST base | /api/recovery/litigation/v1 |
| Kafka topic | rwb.litigation.events.v1 |
| Retry and dead-letter topics | rwb.litigation.events.v1.retry.1m, rwb.litigation.events.v1.retry.10m, rwb.litigation.events.v1.retry.1h, rwb.litigation.events.v1.dlt |
| Temporal task queue | rwb-litigation |
| Java package | th.co.scb.ace.workbench.recovery.litigation |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/litigation/v1; AsyncAPI 3.0 for rwb.litigation.events.v1; activity contract jar on rwb-litigation |
| Owns (Arch v5 slide 41) | legal actions, hearings, judgments, enforcement, LED auction ladder |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P3 rwb-case | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | S5 rwb-asset | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | S5 rwb-asset | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Temporal | P3 rwb-case | Child workflow: LitigationWorkflow | Activity contract jar on task queue rwb-litigation | C | slide 14, slide 19 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P6 rwb-comms | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-15) |
| Kafka | S9 rwb-partner | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-21) |
| Temporal | P6 rwb-comms | Child workflow: demand notice | Activity contract jar on task queue rwb-comms | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | S9 rwb-partner | Activity: issueInstruction (law firm) | Activity contract jar on task queue rwb-partner | C | The provider's published contract and its fake | slide 13, slide 19 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /legal-actions/{legalActionId} | /api/recovery/litigation/v1/legal-actions/{legalActionId} | S4 |
| PATCH /legal-actions/{legalActionId} | /api/recovery/litigation/v1/legal-actions/{legalActionId} | S4 |
| POST /cases/{caseId}/legal-actions | /api/recovery/litigation/v1/cases/{caseId}/legal-actions | S4 |
| POST /legal-actions/{legalActionId}/hearings | /api/recovery/litigation/v1/legal-actions/{legalActionId}/hearings | S4 |
| POST /notices/{noticeId}/approve | /api/recovery/litigation/v1/notices/{noticeId}/approve | S4 |

**Schema boundary**

- Writes rwb_litigation only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.15 S5 rwb-asset — Asset

| Item | Value |
|---|---|
| Service code | S5 |
| Service | rwb-asset |
| Service name | Asset |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S5 |
| Schema and login | rwb_asset |
| REST base | /api/recovery/asset/v1 |
| Kafka topic | rwb.asset.events.v1 |
| Retry and dead-letter topics | rwb.asset.events.v1.retry.1m, rwb.asset.events.v1.retry.10m, rwb.asset.events.v1.retry.1h, rwb.asset.events.v1.dlt |
| Temporal task queue | rwb-asset |
| Java package | th.co.scb.ace.workbench.recovery.asset |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/asset/v1; AsyncAPI 3.0 for rwb.asset.events.v1; activity contract jar on rwb-asset |
| Owns (Arch v5 slide 41) | assets taken on, holding, floor price, listings, auction rounds |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P3 rwb-case | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 42, slide 43 (EV-22) |
| Kafka | P8 rwb-payment | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P8 rwb-payment | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | slide 42, slide 43 (EV-22) |
| Temporal | P3 rwb-case | Child workflow: AssetDisposalWorkflow | Activity contract jar on task queue rwb-asset | C | slide 14, slide 19 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P8 rwb-payment | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-25) |
| Kafka | S4 rwb-litigation | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S4 rwb-litigation | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | The provider's published contract and its fake | slide 43 (event catalogue, not numbered) |
| Kafka | S9 rwb-partner | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-21) |
| Temporal | P6 rwb-comms | Not specified in the source documents (GAP-0106; ASM-0175) | Activity contract jar on task queue rwb-comms | C | The provider's published contract and its fake | slide 13 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | P8 rwb-payment | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | S9 rwb-partner | Activity: issueInstruction (auction vendor) | Activity contract jar on task queue rwb-partner | C | The provider's published contract and its fake | slide 13, slide 19 |
| REST | P1 rwb-source-data | GET /collateral/{assetKey} | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-060; RD-P1-069 |
| REST | P1 rwb-source-data | GET /cases/{caseId}/interactions (notice delivery state) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-064 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /assets | /api/recovery/asset/v1/assets | S5 |
| GET /assets/{assetId} | /api/recovery/asset/v1/assets/{assetId} | S5 |
| GET /assets/{assetKey} | /api/recovery/asset/v1/assets/{assetKey} | S5 |
| POST /assets/{assetId}/listings | /api/recovery/asset/v1/assets/{assetId}/listings | S5 |
| POST /assets/{assetKey}/listings | /api/recovery/asset/v1/assets/{assetKey}/listings | S5 |
| POST /listings/{listingId}/rounds | /api/recovery/asset/v1/listings/{listingId}/rounds | S5 |

**Schema boundary**

- Writes rwb_asset only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.16 S6 rwb-debtsale — Debt sale

| Item | Value |
|---|---|
| Service code | S6 |
| Service | rwb-debtsale |
| Service name | Debt sale |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S6 |
| Schema and login | rwb_debtsale |
| REST base | /api/recovery/debtsale/v1 |
| Kafka topic | rwb.debtsale.events.v1 |
| Retry and dead-letter topics | rwb.debtsale.events.v1.retry.1m, rwb.debtsale.events.v1.retry.10m, rwb.debtsale.events.v1.retry.1h, rwb.debtsale.events.v1.dlt |
| Temporal task queue | rwb-debtsale |
| Java package | th.co.scb.ace.workbench.recovery.debtsale |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/debtsale/v1; AsyncAPI 3.0 for rwb.debtsale.events.v1; activity contract jar on rwb-debtsale |
| Owns (Arch v5 slide 41) | lots, data room, buyer terms, bids, award, transfer |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Kafka | P3 rwb-case | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 42, slide 43 (EV-23) |
| Kafka | P8 rwb-payment | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 42, slide 43 (EV-23) |
| Kafka | P9 rwb-reporting | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | slide 43 (event catalogue, not numbered) |
| Temporal | P3 rwb-case | Child workflow: DebtSaleWorkflow | Activity contract jar on task queue rwb-debtsale | C | slide 14, slide 19 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P8 rwb-payment | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-25) |
| Temporal | P2 rwb-integration | Activity: deliverFile (buyer file) | Activity contract jar on task queue rwb-integration | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | P5 rwb-document | Document: data room pack | Activity contract jar on task queue rwb-document | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | P7 rwb-decision | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 19 |
| Temporal | P8 rwb-payment | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | The provider's published contract and its fake | slide 13, slide 19 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /debt-sale-lots/{lotId} | /api/recovery/debtsale/v1/debt-sale-lots/{lotId} | S6 |
| GET /partner/data-room/{lotId} | /api/recovery/debtsale/v1/partner/data-room/{lotId} | S6 |
| POST /debt-sale-lots | /api/recovery/debtsale/v1/debt-sale-lots | S6 |
| POST /debt-sale-lots/{lotId}/award | /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award | S6 |
| POST /partner/data-room/{lotId}/bids | /api/recovery/debtsale/v1/partner/data-room/{lotId}/bids | S6 |

**Schema boundary**

- Writes rwb_debtsale only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.17 S7 rwb-writeoff — Write-off

| Item | Value |
|---|---|
| Service code | S7 |
| Service | rwb-writeoff |
| Service name | Write-off |
| Wave (Arch v5) | 4 |
| Service epic | RWB-SVC-S7 |
| Schema and login | rwb_writeoff |
| REST base | /api/recovery/writeoff/v1 |
| Kafka topic | rwb.writeoff.events.v1 |
| Retry and dead-letter topics | rwb.writeoff.events.v1.retry.1m, rwb.writeoff.events.v1.retry.10m, rwb.writeoff.events.v1.retry.1h, rwb.writeoff.events.v1.dlt |
| Temporal task queue | rwb-writeoff |
| Java package | th.co.scb.ace.workbench.recovery.writeoff |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/writeoff/v1; AsyncAPI 3.0 for rwb.writeoff.events.v1; activity contract jar on rwb-writeoff |
| Owns (Arch v5 slide 41) | eligibility, committee, posting, recovery after charge-off |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| Kafka | P8 rwb-payment | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| Kafka | P9 rwb-reporting | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | slide 42, slide 43 (EV-24) |
| Temporal | P3 rwb-case | Child workflow: WriteOffWorkflow | Activity contract jar on task queue rwb-writeoff | C | slide 14, slide 20 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P1 rwb-source-data | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-26) |
| Kafka | P8 rwb-payment | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-25) |
| REST | P1 rwb-source-data | GL outcome | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | slide 13, slide 20 |
| Temporal | P7 rwb-decision | Child workflow: committee approval | Activity contract jar on task queue rwb-decision | C | The provider's published contract and its fake | slide 13, slide 20 |
| Temporal | P8 rwb-payment | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | The provider's published contract and its fake | slide 13, slide 20 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| POST /write-off-scans | /api/recovery/writeoff/v1/write-off-scans | S7 |
| POST /write-offs/{writeOffId}/committee-decision | /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision | S7 |

**Schema boundary**

- Writes rwb_writeoff only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.18 S8 rwb-deviation — Deviation

| Item | Value |
|---|---|
| Service code | S8 |
| Service | rwb-deviation |
| Service name | Deviation |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S8 |
| Schema and login | rwb_deviation |
| REST base | /api/recovery/deviation/v1 |
| Kafka topic | rwb.deviation.events.v1 |
| Retry and dead-letter topics | rwb.deviation.events.v1.retry.1m, rwb.deviation.events.v1.retry.10m, rwb.deviation.events.v1.retry.1h, rwb.deviation.events.v1.dlt |
| Temporal task queue | rwb-deviation |
| Java package | th.co.scb.ace.workbench.recovery.deviation |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/deviation/v1; AsyncAPI 3.0 for rwb.deviation.events.v1; activity contract jar on rwb-deviation |
| Owns (Arch v5 slide 41) | X1-X7 screening, pause, handling, return |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-07) |
| Kafka | P3 rwb-case | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| Kafka | P6 rwb-comms | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-07) |
| Kafka | P6 rwb-comms | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| Kafka | S2 rwb-treatment | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | slide 42, slide 43 (EV-06) |
| Temporal | P3 rwb-case | Child workflow: DeviationWorkflow | Activity contract jar on task queue rwb-deviation | C | slide 14, slide 15 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| Kafka | P1 rwb-source-data | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-26) |
| Kafka | P10 rwb-agent | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-28) |
| Kafka | P3 rwb-case | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | The provider's published contract and its fake | slide 42, slide 43 (EV-01) |
| REST | P1 rwb-source-data | Party flags (GET /customers/{personKey}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | slide 13, slide 15; RD-P1-060 |
| Temporal | P10 rwb-agent | Child workflow: screening agent run | Activity contract jar on task queue rwb-agent | C | The provider's published contract and its fake | slide 13, slide 15 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| PATCH /deviations/{deviationId} | /api/recovery/deviation/v1/deviations/{deviationId} | S8 |
| POST /cases/{caseId}/deviations | /api/recovery/deviation/v1/cases/{caseId}/deviations | S8 |

**Schema boundary**

- Writes rwb_deviation only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).

## 6.19 S9 rwb-partner — Partner

| Item | Value |
|---|---|
| Service code | S9 |
| Service | rwb-partner |
| Service name | Partner |
| Wave (Arch v5) | 4 |
| Service epic | RWB-SVC-S9 |
| Schema and login | rwb_partner |
| REST base | /api/recovery/partner/v1 |
| Kafka topic | rwb.partner.events.v1 |
| Retry and dead-letter topics | rwb.partner.events.v1.retry.1m, rwb.partner.events.v1.retry.10m, rwb.partner.events.v1.retry.1h, rwb.partner.events.v1.dlt |
| Temporal task queue | rwb-partner |
| Java package | th.co.scb.ace.workbench.recovery.partner |
| Contract artefacts | OpenAPI 3.1 for /api/recovery/partner/v1; AsyncAPI 3.0 for rwb.partner.events.v1; activity contract jar on rwb-partner |
| Owns (Arch v5 slide 41) | panel, partner users, instructions, results, fees, scorecards |
| Status | Draft |

**Contracts provided**

| Call type | Consumer | Interface | Contract artefact | Class | Source |
|---|---|---|---|---|---|
| Kafka | P3 rwb-case | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| Kafka | Partner portal | InstructionIssued | AsyncAPI 3.0, rwb.partner.events.v1 | X | slide 42, slide 43 (EV-20) |
| Kafka | S4 rwb-litigation | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| Kafka | S5 rwb-asset | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | slide 42, slide 43 (EV-21) |
| Temporal | S4 rwb-litigation | Activity: issueInstruction (law firm) | Activity contract jar on task queue rwb-partner | C | slide 13, slide 19 |
| Temporal | S5 rwb-asset | Activity: issueInstruction (auction vendor) | Activity contract jar on task queue rwb-partner | C | slide 13, slide 19 |

**Contracts consumed**

| Call type | Provider | Interface | Contract artefact | Class | Build against | Source |
|---|---|---|---|---|---|---|
| REST | Outside the cluster | Partners (law firms, agencies, buyers) through the partner gateway, FAPI 2.0, MFA | The external API or interface of that party | X | The edge stub named in section 8.4 | slide 13, slide 17 |
| REST | P5 rwb-document | Partner uploads (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | The provider's published contract and its fake | slide 13, slide 17 |
| REST | P1 rwb-source-data | POST /cases/{caseId}/interactions (partner results) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | The provider's published contract and its fake | RD-P1-064 |

**REST operations owned (Ownership Map v1, Endpoints sheet)**

| Operation | Contract path | Owner |
|---|---|---|
| GET /partner/instructions | /api/recovery/partner/v1/partner/instructions | S9 |
| GET /partners | /api/recovery/partner/v1/partners | S9 |
| POST /cases/{caseId}/instructions | /api/recovery/partner/v1/cases/{caseId}/instructions | S9 |
| POST /partner/instructions/{instructionId}/accept | /api/recovery/partner/v1/partner/instructions/{instructionId}/accept | S9 |
| POST /partner/instructions/{instructionId}/invoices | /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices | S9 |
| POST /partner/instructions/{instructionId}/results | /api/recovery/partner/v1/partner/instructions/{instructionId}/results | S9 |

**Schema boundary**

- Writes rwb_partner only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).
- The partner portal is the only partner surface, behind the partner gateway (FAPI 2.0).

# 7. Contract artefacts and registration

## 7.1 What each service publishes

A service publishes three artefacts before any code story starts, and registers them here with the version it publishes. The artefacts are the deliveries of the service's CON story in its service epic.

| Code | Service | OpenAPI 3.1 | AsyncAPI 3.0 | Activity contract jar | Published by |
|---|---|---|---|---|---|
| P1 | rwb-source-data | /api/recovery/source-data/v1 (5.1.0) | rwb.source-data.events.v1 (5.1.0) | rwb-source-data | RWB-SVC-P1 CON story |
| P2 | rwb-integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | RWB-SVC-P2 CON story |
| P3 | rwb-case | /api/recovery/case/v1 (5.1.0) | rwb.case.events.v1 (5.1.0) | rwb-case | RWB-SVC-P3 CON story |
| P4 | rwb-access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | RWB-SVC-P4 CON story |
| P5 | rwb-document | /api/recovery/document/v1 (5.1.0) | rwb.document.events.v1 (5.1.0) | rwb-document | RWB-SVC-P5 CON story |
| P6 | rwb-comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | RWB-SVC-P6 CON story |
| P7 | rwb-decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | RWB-SVC-P7 CON story |
| P8 | rwb-payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | RWB-SVC-P8 CON story |
| P9 | rwb-reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | RWB-SVC-P9 CON story |
| P10 | rwb-agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | RWB-SVC-P10 CON story |
| S1 | rwb-valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | RWB-SVC-S1 CON story |
| S2 | rwb-treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | RWB-SVC-S2 CON story |
| S3 | rwb-guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | RWB-SVC-S3 CON story |
| S4 | rwb-litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | RWB-SVC-S4 CON story |
| S5 | rwb-asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | RWB-SVC-S5 CON story |
| S6 | rwb-debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | RWB-SVC-S6 CON story |
| S7 | rwb-writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | RWB-SVC-S7 CON story |
| S8 | rwb-deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | RWB-SVC-S8 CON story |
| S9 | rwb-partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | RWB-SVC-S9 CON story |

Registered versions, 27 November 2026 (API Specification v7): every OpenAPI document and gateway-bff carry 5.1.0 (shared Problem schema, RD-P1-004); AsyncAPI 5.1.0 for rwb.source-data.events.v1, rwb.case.events.v1, rwb.document.events.v1 and rwb.decision-record.v1, the other AsyncAPI documents stay 5.0.0. DecisionRecorded is rwb.decision.DecisionRecorded.v1 (RD-P1-008). Stories cite rwb-source-data.yaml 5.1.0 as their build contract.

The coordinates of the contract jars (groupId, artifactId, version) are Not specified in the source documents (GAP-0101; ASM-0170). The Java package column of section 6 is the package root the jar follows; the exact coordinates are allocated with the repositories in the service template work.

## 7.2 The artefact rules

| Rule | Detail | Source |
|---|---|---|
| Contract first | The OpenAPI document, the AsyncAPI document and the activity contract jar are published and versioned before the implementation story of the contract starts | ADR-020; Arch v5 slide 46 |
| One artefact per service | One OpenAPI document per service, one AsyncAPI document per service, one contract jar per service; gateway-bff has its own OpenAPI document and no topic | Arch v5 slides 20 and 41; Template and Rules §R8.4 |
| Registry | Event schemas are registered with BACKWARD compatibility; the registry product is Not specified in the source documents (GAP-0103; ASM-0172) | Arch v5 slide 42 |
| Validation | The documents validate against OpenAPI 3.1, AsyncAPI 3.0 and the Temporal SDK interface rules; the build fails on a validation error | Arch v5 slide 46 |
| Fake | Each provider publishes a fake from its own contract; the consumer runs its contract tests against the fake, so the consumer never waits for the provider. The fake is published with the contract it fakes, is named '<service> contract fake' and carries that contract's version; the Given line of a consuming story names this artefact (GAP-3152) | Template and Rules §R5.4 (class C); D-RCV-60 |
| Publication | The contract document is registered in section 7 of this catalogue with its version; the CON story is Done when it is registered | Story set, CON stories of every service epic |

## 7.3 The shared platform contracts

| Contract | Provider | Consumers | Artefact | Source |
|---|---|---|---|---|
| Workflow kit: Approval, Notify, Document intake, Agent run, Human task with SLA, Saga runner, Scheduled job, Partner instruction | PLT | All 19 services | Versioned workflow kit library | Temporal and Drools Design slides 12 and 14 |
| EvaluateRules and RecordAndApply activities | Every service, on its own queue | Its own workflows | Activity contract jar plus the rule package contract | Temporal and Drools Design slide 12; ADR-017 |
| Rule package in force | P7 rwb-decision | All services that evaluate rules | RulePackageInForce event on rwb.decision.events.v1 plus the package checksum | Arch v5 slides 14 and 43; ADR-017 |
| Decision record | Every service, locally | P7 rwb-decision central ledger | DecisionRecorded on rwb.decision-record.v1, hash-chained | Arch v5 slides 20 and 43; ADR-022 |
| Authorise | P4 rwb-access | All staff-facing services | POST /authorise on /api/recovery/access/v1, cached at the caller | Arch v5 slide 14 |
| Feature flags | PLT platform library | All 19 services | Feature flag tables in every schema and the flag API | Ownership Map v1 ruling; Template and Rules §R3 |
| Observability | PLT | All 19 services | OpenTelemetry traces, metrics and logs; /health and /metrics per service | ADR-023; Arch v5 slide 20 |

# 8. Dependency classes and decoupling rules

## 8.1 The four classes

| Class | Meaning for a contract | Blocks the build? | Source |
|---|---|---|---|
| H | The same service, or a platform CON story. Inside one service the contract is its own module boundary. | Only H on a non-CON story, in the same lane | Template and Rules §R5.4 |
| C | Another service's CON story. The consumer builds against the published contract and its fake; the provider is never a build blocker. | No | Template and Rules §R5.4 |
| I | The real cross-service behaviour. Allowed only on ITG stories, which run the contract harness against the real providers. | ITG only | Template and Rules §R5.4 |
| X | External or team-type work: gateway-bff, ACE Common, the ACE database, Blob, Enterprise AI, partners, the bank file channels, and the DB, INF or OPS story of the same legacy key. | No; tracked | Template and Rules §R5.4 |

Every row of section 5 carries its C or X class. The same pair becomes an I dependency on the integration story of the later wave, which is how the real behaviour is proved without making any service wait for another.

## 8.2 The decoupling patterns as contract rules

| DP | Legacy marker | Contract rule in this catalogue | Dependency |
|---|---|---|---|
| DP-01 | recovery.<table> or the recovery schema | The owner's schema rwb_<name>; a reader uses the owner's contract, never its tables | none |
| DP-02 | recovery_svc login | One login per service; no shared login is a contract | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library plus DecisionRecorded on rwb.decision-record.v1 | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit in the owning service; rule packages arrive from rwb-decision on RulePackageInForce | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, v_ace_*, account_ext | Read through rwb-source-data's contract, or through the service's own ACE views where the ruling gives it one | none |

The full DP table is Template and Rules §R5.5; the rows above are the ones that create or remove a contract in this catalogue.

## 8.3 The one-hop rule

- REST is one hop: gateway-bff to the owner service, or a cached reference read from rwb-access or rwb-source-data. A service never calls another service to answer a screen.
- A composite screen is composed in gateway-bff with parallel calls, each with a 2 s timeout and its own breaker, and the budget for the case screen is about 1.2 s (Arch v5 slide 46).
- Anything longer than one hop is a workflow. The route services reach decision, document, payment, partner and communications through Temporal, never through REST (section 4, rule 1).
- Trace analysis flags a call depth above one, and the build fails on it (ADR-020).

## 8.4 The edge contracts

| Edge | Contract | Stub used by the 19 services | Source |
|---|---|---|---|
| gateway-bff | OpenAPI 3.1 for the browser surface; session cookie with a 15 minute idle timeout; one hop to the owner | A gateway stub with the route table of section 5 | Arch v5 slide 20 |
| ACE Common | Sign-in and group-to-role (Entra ID), notification path (SMS, LINE OA), audit and PII logging on Kafka | The ACE Common test double in the integration harness | Arch v5 slides 14, 17, 20 |
| ACE database | The 30 recovery.v_ace_* views, SELECT only | View fixtures in the P1 contract test | ADR-010; Arch v5 slide 29 |
| Enterprise AI | HTTPS private endpoint (INT-23) from rwb-agent | A recorded-response double | Arch v5 slide 16 |
| WIN and debt buyers | INT-14 daily outbound file; INT-25 encrypted buyer files through the bank MFT channel | A file fixture with a manifest | Arch v5 slide 16 |
| Partner gateway | FAPI 2.0 in the DMZ fronting rwb-partner; MFA for partner users | The partner gateway stub | Arch v5 slides 8 and 17; ADR-019 |

# 9. Contract conformance and tests

A contract is conformant when every row below is true. The list is the contract part of the Definition of Done in the Service Template Specification v1, and each row names the test that proves it.

| # | Contract rule | Tested by |
|---|---|---|
| 1 | The provider publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar before the implementation story starts | Contract publication gate in the pipeline |
| 2 | Every operation in section 6 exists in the published contract, under the service's own base path | OpenAPI diff against the Ownership Map Endpoints sheet |
| 3 | Every event the service publishes is in its AsyncAPI document, on its own topic, with CloudEvents 1.0 binary mode and key caseId | AsyncAPI validation plus a schema registry check |
| 4 | Every event the service consumes is deduplicated in processed_event, in the same transaction as the change | Inbox test |
| 5 | Every activity and child workflow the service calls is declared in the provider's contract jar; no service imports another service's code | Activity contract test |
| 6 | No REST chain longer than one hop; route services reach shared capabilities through Temporal | Contract test plus trace-depth check |
| 7 | No cross-schema read, join, view or foreign key; the boundary test fails the build on any violation | Architecture test |
| 8 | Every POST and PATCH is idempotent through Idempotency-Key, and every consumer of the same key returns the first result | Idempotency test |
| 9 | Error responses follow RFC 9457 for REST and the error code form for events | Contract example test |
| 10 | The provider's fake serves every operation and every event of its contract | Fake conformance test in the consumer build |
| 11 | The pair is proved end to end in the integration story of the later wave | RWB-ITG-W<n> harness |
| 12 | The contract document is registered in section 6 with its version | Registration check on the CON story |

The integration stories that run the harness are RWB-ITG-W1 to RWB-ITG-W4, one per wave, plus RWB-ITG-NFR for the non-functional contracts. A pair is assigned to the harness of the later of its two waves.

# 10. Contract change control

| Step | What happens | Recorded in |
|---|---|---|
| Propose | The provider team raises the change against its own contract and names the consumers from section 5 | The service's CON story |
| Assess | Every consumer in section 5 is checked; an additive change stays in v1, a breaking change takes a new path version or a new topic version | This catalogue, section 5 and 6 |
| Publish | The new artefact version is published with its fake before the code changes | Section 7.1 |
| Prove | The consumer contract test and the wave harness pass against both the old and the new version for one release | Section 9 |
| Retire | The old version is withdrawn only when no consumer in section 5 names it | This catalogue, section 6 |

A change to a shared edge contract (ACE Common, ACE database views, Enterprise AI, WIN, debt buyers, the partner gateway) follows the same steps and is tracked as class X against the owning external party.

# 11. Open points

| ID | Point | Effect in this catalogue | Owner role |
|---|---|---|---|
| GAP-0099 | No earlier Service Contract Catalog exists, so v1 carries no inherited sections, IDs, numbers or dates | Version 1, status Draft; the change-log row is the first | Delivery lead |
| GAP-0100 | The Ownership Map Endpoints sheet holds the monolith operations of API Specification v4, while Architecture v5 slide 41 states a per-service base path; the per-service paths and payloads are written in API Specification v5 | Section 6 lists the operation per owning service under its base path and leaves the final path to API Specification v5 | Solution architect |
| GAP-0101 | The coordinates of the activity contract jars (groupId, artifactId, version) are not specified | Section 7.1 states the artefact and the package root, and leaves the coordinates open | Tech lead |
| GAP-0102 | The event catalogue does not name the consumers of ApprovalDecided or ReportPublished | The two rows state Not specified in the source documents (GAP-0102; ASM-0171) | Solution architect |
| GAP-0103 | The schema registry product and its deployment are not specified; only the BACKWARD compatibility rule is stated | Section 7.2 states the compatibility rule and not the product | Platform architect |
| GAP-0104 | The slide 13 rule that route services reach shared capabilities through Temporal sits beside REST cells from S1, S7 and S8 to rwb-source-data | Section 8.3 reads the rule as covering the five shared capabilities named in the slide note; the rwb-source-data reads stay REST | Solution architect |
| GAP-0105 | The request and response content of the Enterprise AI private endpoint (INT-23) is not specified | Section 8.4 names the edge and the stub, not a payload | Solution architect |
| GAP-0106 | The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one | Section 6.15 carries the placeholder in its Temporal row and no interface is invented | Solution architect |
| GAP-3274 | Path and maximum keys per call of the rwb-source-data account-page read | The pair is listed without a path | Solution architect |
| GAP-3555 | The If-Match value of the first write of an extension-facts key is not ruled | The two PUT operations carry If-Match with no first-write rule | API contract owner |
| GAP-3556 | Slide 17 names a payments activity of rwb-source-data; RWB-P1-E2008-APP publishes REST GET /payments | Both pairs are listed | Solution architect |
| GAP-3322 | Request and answer fields of POST /authorise are not published | The path is in rwb-access.yaml 5.1.0; callers assert only allow or deny and the messageCode | rwb-access contract owner |
| GAP-3385 | Name of the business date query parameter of GET /parameters/{key} | rwb-case.yaml 5.1.0 publishes the path parameter only | rwb-case service owner |
| GAP-3283 | Masking rule rows that unmask recipient name and postal address for the rwb-comms notice and rwb-integration outbound-file identities | GET /customers/{personKey} answers masked values until the rows exist | Data protection officer with the rwb-access owner |

The full text of every gap and assumption is in the Gap Register and the Assumptions Register (folder 23). Candidate rows are in `_work/msr/gaps/B-ARCH-CON.jsonl` and `_work/msr/assumptions/B-ARCH-CON.jsonl`.

# 12. Change log

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Contract Catalog: the contract model and the five call types, the call-type matrix of Architecture v5 slide 13, the contract inventory of every provider and consumer pair, the contract by service with its artefacts, the shared platform contracts, the dependency classes and decoupling rules, the contract tests and the change control. |
| 3 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) | v3 · 27 November 2026 · D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits: shared error envelope and idempotency/If-Match rules; one contract file and one provider fake per contract version; rwb-source-data 5.1.0 operations, workflows and event consumers; new contract pairs of RD-P1-007, 010, 020, 022, 024 and 047; registration of version 5.1.0; batch D (RD-P1-060 to RD-P1-066): customer, account and collateral reads, one GET /payments with two query forms, ledger callers, authorise and parameter reads, new consumer pairs, section 6.1 aligned to Service Catalog v2. |

