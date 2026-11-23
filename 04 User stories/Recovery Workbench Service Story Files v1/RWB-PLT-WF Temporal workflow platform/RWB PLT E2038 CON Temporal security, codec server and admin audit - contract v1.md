# RWB-PLT-E2038-CON Temporal security, codec server and admin audit - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2038-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-038 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-038 for the workflow platform epic; the codec protocol, the authorizer audit call, the entry contract and the error codes are published on Day 1 with three fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the codec and admin-audit contract** (the Temporal Web UI, the authorizer plugin, the security administrator and the audit team), I want **the codec protocol models, the authorizer audit call contract, the decision entry contract and the error codes published on Day 1 with fakes**, so that **the codec server, the plugin and the audit reconciliation are built and tested against one frozen set**.

This is the contract story of legacy key RWB-E2-038 under epic RWB-PLT-WF. It publishes, as a platform contract of the Temporal layer:

- The codec server protocol document: `POST /decode` and `POST /encode`, the request and response models of the Temporal codec server protocol, the payload metadata rule and the 401, 403, 413, 422 and 503 errors.
- The authorizer audit call contract: the operation, namespace, workflow ID, run ID, actor reference, grant, reason and request ID the frontend plugin sends, the 201 entry identifier it must receive, and the rule that any non-201 answer denies the call.
- The decision entry contract: the AC-READ, AC-DENY and PLATFORM_ADMIN codes and the field list of the entry, with no payload and no personal data.
- The idempotency contract: one entry per operation on one run, from the Web UI request ID and from the frontend request ID.
- Three fakes — a codec server, an audit receiver and an authorizer — and a contract test, so the plugin, the Web UI and the reconciliation can be built and tested with no Key Vault and no cluster.

The codec server and the audit path are shared platform, not one of the 19 services: Template and Rules §R4 has no platform row, so this document declares no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base. The codec server publishes the Temporal codec server protocol behind the platform internal ingress, and the authorizer audit call is an mTLS call with no HTTP path of the Workbench API. The contract is published at status Draft (realignment v1) and is frozen when its consumers pass their contract tests.

### 2. Business rationale

The decode path is the one place a clear payload leaves the engine, and the authorizer path is the one place an administrative action becomes recordable. Both must be frozen before any code, because they are consumed from three sides at once: the Temporal Web UI sets a codec endpoint per environment, the Temporal frontend loads a plugin that must agree on the audit call, and the reconciliation and the audit team read the same entry fields. If the three are written to three private readings, the first integration test in SIT discovers it, and by then the plugin configuration, the key resolver and the reconciliation are all built on the wrong shape.

ADR-020 makes the contract the first artefact: an OpenAPI-style protocol document for the two codec operations, a typed call contract for the audit path, a field contract for the entry and one error table, published with fakes. The fake is the second reason: the plugin and the Web UI integration can then be tested with no Key Vault and no cluster, so a decode test does not need a key and an audit test does not need a namespace. That is what keeps REQ-DRI-001, REQ-DRI-005 and NFR-045 testable on Day 1 rather than at the end of the wave, and it is what lets RWB-PLT-E2038-APP start on the same day as this story.

### 3. Preconditions

- RWB-PLT-E1070-CON is published: the namespace `rwb-recovery`, the mTLS identities, the Web UI codec endpoint setting and the frontend authorizer plugin slot from the values file.
- RWB-PLT-E1071-CON is published: the codec contract of the worker and SDK side, so the payload metadata this document declares is the metadata the codec writes.
- RWB-P4-E1039-CON is published: the ACTIVE break-glass grant, the AC-BGON entry, `GET /api/recovery/access/v1/admin/access-log` and the LOV-DECISION codes AC-READ and AC-DENY.
- RWB-P7-E1027-CON is published: the decision-record contract behind DecisionLogApi, so the entry this document declares is the entry that library writes.
- The Temporal codec server protocol is the protocol of the platform's Temporal version 1.30 or later (Architecture v5 slide 23); this contract republishes it and adds no field of its own to the request or the response.
- The values 100 payloads and 1 MB per request, the 02:00 reconciliation and the key versions 1, 2 and 3 are carried from the legacy story; the key rotation period, the archive retention and the platform identity that runs the codec server are Not specified in the source documents (GAP-1441; ASM-2536) and are published as the working read of that assumption.
- The contract is Draft until its consumers pass: RWB-PLT-E2038-APP, the Web UI integration and the reconciliation test. No approval is required to publish a Draft contract.

### 4. Flow

1. The contract author writes the codec protocol document: `POST /decode` and `POST /encode`, the request model (namespace, workflowId, runId, requestId, payloads), the response model (payloads and entryId) and the error table.
2. The author writes the payload metadata rule: every payload carries `metadata.encoding` and `metadata.keyVersion`, and a payload without metadata is refused whole, with no key guessed and no clear fallback.
3. The author writes the authorizer audit call: operation, namespace, workflowId, runId, actorRef, grantId (nullable), reason and requestId, answered with a 201 and an entryId, with any other answer denying the call.
4. The author writes the decision entry contract: the three codes AC-READ, AC-DENY and PLATFORM_ADMIN and the field list of the entry, with no payload and no personal data.
5. The author writes the error contract and the idempotency contract: 401, 403 with MSG-P4-002, 413, 422 and 503, and one entry per operation on one run for a repeated requestId.
6. The fake codec, the fake audit receiver and the fake authorizer are generated from the documents, with the 201 and 503 answers and the refusal examples.
7. The contract test runs the fakes against the documents on every change: a field, a code or a status that drifts fails the build.
8. The documents and the fakes are published at v1 to the contract registry; RWB-PLT-E2038-APP, the Web UI integration and the reconciliation test pin v1, and the contract is frozen when all three pass.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A payload in a document example carries no codec metadata | The lint step fails the build; the metadata rule is mandatory in every request model and in every example | Lint finding, no message id |
| X2 | A document lets a role other than RW-SECADM decode | The lint step fails the build; the authorization clause names RW-SECADM and the break-glass grant, and the 403 example uses MSG-P4-002 | Lint finding, no message id |
| X3 | A document or a fake treats an ended grant as a valid one | The lint step fails the build; the grant states are ACTIVE and ENDED, and only ACTIVE passes the check in every example | Lint finding, no message id |
| X4 | The decision log is unavailable in the audit-call contract or in the fake | The contract declares 503 and the deny rule; the fake answers 503 and the authorizer refuses; the workflow stays unchanged in the example | None (503 refusal text) |
| X5 | A breaking change is made to a published field, code or error | v1 is not edited; the change raises v2 and deprecates v1, and no consumer sees a changed v1 | Lint finding, no message id |
| X6 | A value the consumers need is named by no source: the platform identity that runs the codec server, its internal base, the key rotation period and the archive retention the version list depends on | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1441; ASM-2536) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and three fakes; builds nothing, reads no business data, depends on nothing |
| Negotiable | Field order inside the models, the example values and the fake's transport are open until the version is frozen; the codes, the 201 rule and the write-before-act rule are fixed |
| Valuable | The codec server, the plugin, the Web UI integration and the reconciliation start on Day 1 against one frozen set and three fakes |
| Estimable | Two protocol operations, one audit call, one entry contract, one error table, three fakes, one contract test |
| Small | One sprint for the documents, the fakes and the lint rules |
| Testable | Each criterion in section 7 is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal security, codec server and admin audit contract

  Background:
    Given the codec server answers the Temporal codec server protocol on the platform internal ingress
    Given the platform publishes no schema, no topic and no /api/recovery base of its own

  Scenario: AC1 The codec protocol document is published (new, D-RCV-60)
    Given the codec server protocol document
    When it is validated and linted
    Then it declares POST /decode and POST /encode with the request model namespace, workflowId, runId, requestId and payloads
    Then it declares the response model payloads in the same order plus entryId
    Then it declares 401 no session, 403 with MSG-P4-002, 413 above 100 payloads or 1 MB, 422 without codec metadata or with a key version that is not enabled, and 503 with no payload returned
    Then it declares the authorization as Platform administration R plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION

  Scenario: AC2 The payload metadata rule is mandatory (new, D-RCV-60)
    Given a payload object of the request model
    When the schema is validated
    Then every payload declares metadata with encoding and keyVersion, and data as base64
    Then a request holding one payload without metadata is refused with 422 as a whole, and no payload of that request is answered
    Then no example and no fake answers a payload the metadata cannot attribute to a version

  Scenario: AC3 The authorizer audit call is published (new, D-RCV-60)
    Given the audit record the Temporal frontend plugin sends over mTLS
    When the call contract is reviewed
    Then it declares operation as TERMINATE, RESET or SIGNAL, and namespace, workflowId, runId, actorRef, grantId, reason and requestId
    Then grantId is nullable, because an administrative call may carry a grant and a decode always does
    Then a 201 answer returns entryId and any non-201 answer denies the call with PERMISSION_DENIED, leaving the workflow unchanged

  Scenario: AC4 The entry contract is published (new, D-RCV-60)
    Given the decision entry a decode, a refusal and an administrative call each write
    When the entry contract is reviewed
    Then it declares the codes AC-READ, AC-DENY and PLATFORM_ADMIN
    Then it declares the operation, namespace, workflow ID, run ID, actor, grant, incident and reason fields
    Then it declares that no payload, no history event and no clear personal data field is part of an entry
    Then a decode is AC-READ, a refusal is AC-DENY and a terminate, reset or signal is PLATFORM_ADMIN

  Scenario: AC5 The idempotency contract is published (new, D-RCV-60)
    Given a decode and an administrative call repeated with the same requestId
    When the contract and the fake are read together
    Then the codec takes requestId from the Web UI and a repeat returns the same payloads and entryId and writes no second entry
    Then the audit call takes requestId from the frontend request and one operation on one run writes one entry
    Then a second entry for the same requestId is refused and logged, and no duplicate entry reaches the decision log

  Scenario: AC6 The fakes answer every contract test and a breaking change raises v2 (new, D-RCV-60)
    Given the fake codec, the fake audit receiver and the fake authorizer, generated from the documents
    When the contract test runs
    Then the fake codec answers both operations, every error example and the payload without metadata
    Then the fake audit receiver answers the 201 entryId and the 503 failure, and the fake authorizer denies on any non-201 answer
    Then a breaking change raises v2 and marks v1 deprecated, and no consumer sees an edited v1
```

These criteria are new and test only the contract baseline: no legacy criterion is repeated here, and every value in the examples comes from RWB-E2-038, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The codec server is the only path to a clear payload and the protocol is the Temporal codec server protocol; this contract adds no field and no operation of its own | Architecture v5 slide 24; legacy RWB-E2-038 section 12 |
| BR2 | Every payload carries encoding and keyVersion in its metadata; a request with one payload without metadata is refused whole and no key is guessed | NFR-045; legacy BR8 |
| BR3 | A decode needs RW-SECADM with an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION and right R; no standing right and no other role is declared | RWB-P4-E1039-CON; legacy BR1 |
| BR4 | The entry is written before the payload is returned, and before the frontend executes an administrative call; a failed write answers no payload and denies the call | REQ-DRI-005; legacy BR3, BR4 |
| BR5 | Every entry names the operation, namespace, workflow ID, run ID, actor, reason and, where one applies, the grant and the incident | REQ-DRI-001; legacy BR5 |
| BR6 | An entry carries no payload, no history event and no clear personal data field, and the codes are AC-READ, AC-DENY and PLATFORM_ADMIN from LOV-DECISION | LOV-DECISION; NFR-045; legacy BR6 |
| BR7 | One entry per operation on one run: the codec and the audit call are idempotent on requestId and a duplicate writes nothing | Legacy section 12 |
| BR8 | A breaking change raises a new version and deprecates v1; v1 is never edited in place | Template and Rules §R7.2; ADR-020 |

### 9. State transitions

| Object | State | Meaning in this contract |
|---|---|---|
| Contract document | DRAFT | Published (realignment v1) and open to comment |
| Contract document | PUBLISHED | v1 in the contract registry, the fakes generated from it, consumers pinning it |
| Contract document | FROZEN | The app story, the Web UI integration and the reconciliation test have passed; a change now raises v2 |
| Contract document | DEPRECATED | A v2 exists; v1 is read-only and still served by its fake |
| Break-glass grant | ACTIVE | The only state in which the codec answers a decode |
| Break-glass grant | ENDED | The grant's end time was reached or it was revoked; the decode is refused with 403 and MSG-P4-002 |
| Fake audit receiver | 201 | The entry was written; the authorizer allows the frontend call |
| Fake audit receiver | 503 | The entry could not be written; the authorizer denies the call and the workflow is unchanged |

The grant states are the P4 contract's and the fake answers are the fake's; this contract owns only the document states and the answer vocabulary.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents, the error table and the fakes |
| Security architecture | Confirms the decode rule, the grant area and right, and the no-standing-right clause |
| The platform owner of the Temporal platform | Approves a breaking change and a version freeze, and owns the values file that loads the plugin |
| Internal audit | Confirms the entry field list, the three codes and the no-payload rule |
| The rwb-access owner (P4) | Confirms the grant states and the access log read the document names |
| The rwb-decision owner (P7) | Confirms the entry fields and the code list it writes and seals |
| RW-SECADM, RW-PLATADM, RW-AUDIT | Read the contract; raise a change request rather than a private variant |
| No delegation of authority level applies | A codec and audit contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document, a schema, an example or a fake. Where a caller must be named, the example uses a user identifier or a role code only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The documents publish operation names, model shapes, field names, codes and status codes; no customer, account, case or document value appears |
| Payload content in an example | Encoded base64 data of a synthetic payload with `metadata.encoding` and `metadata.keyVersion`; no clear value is published, and the response example shows the shape with a synthetic body |
| Workflow identifiers in examples | Synthetic: case-RW-2026-000301 to case-RW-2026-000307, and the run identifiers that go with them |
| Personal data | None. No name, no email address, no account number, no national identifier and no document content in a schema, an example or a fake |
| Entry fields | The field names and shapes of `decision_log_entry`, owned by rwb-decision (P7) and fixed by RWB-P7-E1027-CON: the operation, namespace, workflow ID, run ID, actor, grant, incident, reason, code and timestamps |
| Tables published | None. This document declares no table and no migration; the entry table is P7's and the frontend audit log is the Temporal namespace's |
| Retention | None at the contract: a document keeps no data, and the fakes hold only the examples they publish |

### 12. Contract

#### 12.1 REST operations provided

The codec server speaks the Temporal codec server protocol on the platform internal ingress. It has no `/api/recovery/<short>/v1` base, no gateway route and no place in the Workbench API Specification.

| Method | Path | Purpose | Responses |
|---|---|---|---|
| POST | `/decode` | Returns the clear payloads of one history request | 200 payloads and entryId; 401; 403; 413; 422; 503 |
| POST | `/encode` | Returns the encoded form of payloads written by an authorised client | 200 payloads and entryId; 401; 403; 413; 422; 503 |

| Model | Fields |
|---|---|
| Request | namespace, workflowId, runId, requestId, payloads: an array of { metadata: { encoding, keyVersion }, data: base64 } |
| Response 200 | payloads: an array of { metadata, data: base64 } in the same order, and entryId |
| Error | status, code or message identifier where one exists (MSG-P4-002 on 403), and a detail that names the payload index and the missing metadata on 422, never the payload |

The internal ingress base per environment is Not specified in the source documents (GAP-1441; ASM-2536); the two operations and the models above are the published surface, and the base is environment configuration of the Web UI.

#### 12.2 REST operations consumed

None. The contract publishes two operations and consumes none: the grant read and the entry write belong to the consumers, through RWB-P4-E1039-CON and DecisionLogApi.

#### 12.3 Events published

None. The platform owns no topic, and the entry event `DecisionRecorded` on `rwb.decision-record.v1` is the decision-record library's (RWB-PLT-E1027-CON).

#### 12.4 Events consumed

None. The reconciliation reads the frontend audit log and the access log; it subscribes to no topic.

#### 12.5 Workflows and activities

The authorizer audit call and the reconciliation contract, both without an HTTP path:

| Model | Fields |
|---|---|
| Audit call request | operation (TERMINATE, RESET or SIGNAL), namespace, workflowId, runId, actorRef, grantId (nullable), reason, requestId |
| Audit call response | 201 with entryId; any other status denies the call with PERMISSION_DENIED, and the workflow is unchanged |
| Audit call transport | mTLS from the Temporal frontend pods only, with the frontend's client certificate; no gateway, no Workbench route |
| Audit call idempotency | requestId from the frontend request; one entry per operation on one run |
| Reconciliation contract | The 02:00 run on task queue `rwb-platform` reads the frontend audit log and the AC-READ, AC-DENY and PLATFORM_ADMIN entries, reports each unmatched terminate, reset or signal with its workflow ID, operation and time, and writes no entry of its own |

The reconciliation is a Temporal Schedule in namespace `rwb-recovery` (RWB-PLT-E1071-CON); this contract fixes what the run compares and what it reports, not the workflow's internals.

#### 12.6 Schedules

None owned by this contract. The 02:00 reconciliation Schedule is the app story's (RWB-PLT-E2038-APP section 12.6); this contract fixes the cadence and the report only.

#### 12.7 Tables owned

None. `decision_log_entry` is rwb-decision's (P7) and the frontend audit log belongs to the Temporal namespace; this document declares no table, no column and no migration.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Fake codec server (this story) | `POST /decode` and `POST /encode` with the request and response models, the 401, 403 with MSG-P4-002, 413, 422 and 503 examples, a payload without metadata and a key version that is not enabled | RWB-PLT-E2038-APP, the Web UI integration |
| Fake audit receiver (this story) | The audit call with the 201 entryId and the 503 failure | The plugin configuration test, RWB-PLT-E2038-APP AC6 |
| Fake authorizer (this story) | The allow-on-201 and deny-on-any-other-answer rule, for the Web UI and CLI path | The plugin test and the denial example |
| rwb-access break-glass fake (RWB-P4-E1039-CON) | The grant read, the AC-BGON entry, the access log read and the LOV-DECISION codes, with ACTIVE, ENDED and wrong-area variants | The role, grant and area examples |
| Decision-record fake (RWB-PLT-E1027-CON) | The DecisionLogApi write, the entry fields and the write failure | The entry contract examples and the 503 path |

The three fakes answer from the two owner fakes rather than from copied payloads, so a change to the grant contract or the entry contract shows up as a contract-test failure here.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 codec operations on the internal ingress, with no service base | 0 | Temporal codec server protocol, 401, 403, 413, 422 and 503 |
| Kafka | 0 | 0 | No topic of its own |
| Temporal | 1 audit call contract (mTLS, 201 or deny) and the 02:00 reconciliation contract | 0 | Namespace `rwb-recovery`, task queue `rwb-platform` |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Deliverables.**

- `codec-server.yaml`: the two operations, the request and response models, the payload metadata rule and the error table.
- `authorizer-audit.yaml`: the audit call request and response, the mTLS clause, the 201 rule and the deny rule.
- `decision-entry.yaml`: the three codes, the entry field list and the no-payload rule.
- The error and idempotency sections of this document, generated into the three artefacts.
- The fake codec server, the fake audit receiver and the fake authorizer, generated from the artefacts.
- The lint rules and the contract test.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | the entry contract this story publishes is DP-03 applied: H RWB-PLT-E1027-CON for its consumer |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none: the access log read is a C row of the app story |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows that apply to this contract. The story documents them and adds no build dependency of its own: it is a CON story, starts on Day 1 and is frozen when its consumers pass. DP-03 and DP-11 are the two rows the document is about: DP-03 because every decode, refusal and administrative call is a decision record through the local library, and DP-11 because the access log is read as a REST contract, one hop, instead of the monolith's in-process call. DP-13 is why the legacy module path for the access log is never repeated here: the read is `/api/recovery/access/v1/admin/access-log`, and the codec server, which never sat under the monolith base, publishes no base of its own.

**Build steps**

1. Write `codec-server.yaml` with the two operations, the request and response models and the payload metadata rule.
2. Write the error table: 401, 403 with MSG-P4-002, 413 at 100 payloads or 1 MB, 422 without metadata or with a key version that is not enabled, 503 with no payload returned.
3. Write `authorizer-audit.yaml` with the call fields, the nullable grant, the 201 entryId and the deny rule.
4. Write `decision-entry.yaml` with the three codes, the entry fields and the no-payload rule.
5. Add the lint rules: no service base in the codec paths, metadata mandatory, RW-SECADM and the ACTIVE grant in the authorization clause, a message identifier on the 403, a personal-data scan over every example, and one entry per requestId.
6. Generate the three fakes over the P4 break-glass fake and the P7 decision-record fake, write the contract test, and publish v1 to the contract registry with the version the consumers pin.

**Done when.** The three artefacts and the schemas validate, every lint rule passes, the three fakes answer every example including the payload without metadata and the 503 denial, the contract test is green on the build of this story, and RWB-PLT-E2038-APP, the Web UI integration and the reconciliation test have pinned v1.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The role is not RW-SECADM, the grant is missing, ended or for another area, or the caller is not the platform identity on the internal endpoint | You cannot {action} here. Your role does not include it. | 403, reused unchanged, with {action} set to "decode this workflow payload" or "record this workflow action" |
| PLT-CODEC-401 | No session, or the session has expired | The standard no-session text; the title and detail are Not specified in the source documents (GAP-1441; ASM-2536) | 401 |
| PLT-CODEC-413 | More than 100 payloads or more than 1 MB in one request | The request is refused before any key is resolved; the text names the count or the size only | 413 |
| PLT-CODEC-422 | A payload without codec metadata, or a key version that is not enabled | The request is refused whole; the text names the payload index and the missing metadata, never the payload | 422 |
| PLT-CODEC-503 | Key Vault is unavailable, or the entry could not be written | The action was not taken because the decision could not be recorded; no payload is returned and the workflow is unchanged | 503, and the deny answer of the audit call |

MSG-P4-002 is reused unchanged and is the only message identifier the documents borrow from a service. The three PLT-CODEC identifiers are reserved for this contract; when the message catalogue gains platform codec entries they replace the placeholder text and no other value changes.

### 15. Screens and states

No screen in this story, and the contract declares none. The codec server has no user interface: the Temporal Web UI's payload panel is its only surface, and the panel shows encoded, decoding, decoded and refused with MSG-P4-002. The audit path has no screen either; the entries appear on the access log read and on SCR-38 Decision log query. This contract fixes the document states of section 9 so that the app story, the plugin test and the audit team share one vocabulary.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E2038-CON-01 | AC1 | Contract | `codec-server.yaml` validated and linted; both operations; the request and response models; the five errors; no service base in a path |
| TC-PLT-E2038-CON-02 | AC2 | Contract | The metadata rule: encoding and keyVersion mandatory; 100 payloads and 1 MB; the 422 example for a payload without metadata; a personal-data scan of every example |
| TC-PLT-E2038-CON-03 | AC3 | Contract | `authorizer-audit.yaml`: the operation values TERMINATE, RESET and SIGNAL; the nullable grant; the 201 entryId; the deny on any non-201 answer |
| TC-PLT-E2038-CON-04 | AC4 | Component | `decision-entry.yaml` and the entry fake: the three codes, the field list, no payload and no personal data; the code of each operation |
| TC-PLT-E2038-CON-05 | AC5 | Contract | The idempotency section and the fake: one entry per requestId from the Web UI and from the frontend request; the duplicate refusal |
| TC-PLT-E2038-CON-06 | AC6 | Component | The three fakes over the P4 break-glass fake and the P7 decision-record fake; every example answered; a breaking change raises v2 and deprecates v1 |

### 17. Guardrails

- No service base and no gateway route in the codec contract: the protocol is the Temporal codec server protocol on the internal ingress, and the lint step fails the build if a `/api/recovery/<short>/v1` path appears.
- The metadata rule is mandatory: a payload without encoding and keyVersion is refused whole and is never resolved with a guessed key.
- Decode is never a standing right: the authorization clause names RW-SECADM, the ACTIVE grant, the area and right R, and the 403 example carries MSG-P4-002.
- No entry, no action: the contract declares the 201 rule and the deny rule, and no example shows an action taken after a failed write.
- No personal data in a schema, an example, a fake or a log: identifiers, codes and status values only, and the scan fails the build otherwise.
- No payload and no clear field in an entry: the entry contract lists the operation, namespace, workflow ID, run ID, actor, grant, incident, reason, code and timestamps, and nothing else.
- No table and no migration in this contract: the entry table is P7's and the frontend audit log is the namespace's.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-001 | One record per decision, with the seven field groups | RWB-E2-038 section 18 (Epic 2, 3.4; Program, 5.7) | TC-PLT-E2038-CON-03, TC-PLT-E2038-CON-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | RWB-E2-038 section 18 (Epic 2, 3.4; Program, 5.7) | TC-PLT-E2038-CON-03, TC-PLT-E2038-CON-06 |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies | RWB-E2-038 section 18; Program BRD v4, NFR table | TC-PLT-E2038-CON-02, TC-PLT-E2038-CON-04 |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | Business Rules and Routing Logic, R-UNI-39 | TC-PLT-E2038-CON-03, TC-PLT-E2038-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout: the contract is published with a fake before any code | Architecture Decision Records, ADR-020 | TC-PLT-E2038-CON-01, TC-PLT-E2038-CON-06 |
| DP-03 | The entry is a decision record through the local decision-record library and `rwb.decision-record.v1` | Template and Rules §R5.5 DP-03; RWB-PLT-E1027-CON | TC-PLT-E2038-CON-04 |
| DP-11 | The access log is read as a REST contract, one hop, 2 s timeout | Template and Rules §R5.5 DP-11; RWB-P4-E1039-CON | TC-PLT-E2038-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2038-APP | App development | H consumer: implements the codec server, the audit receiver, the plugin configuration and the reconciliation against this contract and its fakes |
| RWB-PLT-E1070-CON | Contract | H: the namespace, the mTLS identities, the Web UI codec endpoint setting and the authorizer plugin slot this document describes |
| RWB-PLT-E1071-CON | Contract | H: the codec contract of the worker side and the Schedule template the 02:00 reconciliation uses |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library and the entry fields this contract republishes |
| RWB-P4-E1039-CON | Contract | C: the break-glass grant, the access log read and the LOV-DECISION codes AC-READ and AC-DENY |
| RWB-P7-E1027-CON | Contract | C: the owner contract of the entry the central ledger seals |
| Legacy RWB-E2-037 (now RWB-PLT-E2037-APP, RWB-PLT-E2037-CON) | App development, Contract | Out of scope: alerts, the stuck scanner and the workflow dashboard |
| Legacy RWB-E2-039 | - | Out of scope: backup, failover, upgrade and archive; its archive period is what the key version list depends on |
| Legacy RWB-E2-040 | - | Out of scope: the replay gate and build ID rollout |

### 19. Out of scope

- The codec server, the audit receiver, the plugin configuration and the reconciliation implementation (RWB-PLT-E2038-APP).
- The Temporal cluster, the namespace, mTLS, the Web UI sign-in and the values file (legacy RWB-E1-070; RWB-PLT-E1070-APP).
- The codec itself, the worker and the smoke workflow (legacy RWB-E1-071; RWB-PLT-E1071-APP).
- The break-glass request, approval, review and access log writer (legacy RWB-E1-039; RWB-P4-E1039-CON and its app story).
- The decision-record entry, the central ledger and the hash chain (RWB-PLT-E1027-CON and rwb-decision).
- Alerts, the stuck scanner and the workflow dashboard (legacy RWB-E2-037; RWB-PLT-E2037-APP).
- Backup, failover, upgrade and archive (legacy RWB-E2-039).
- The replay gate and build ID rollout (legacy RWB-E2-040).
- A Workbench screen for workflow payloads or for the admin audit (Epic 8, SCR-43 Roles and access).
- Key Vault provisioning, key escrow and the bank key management standard (SCB IT platform).
