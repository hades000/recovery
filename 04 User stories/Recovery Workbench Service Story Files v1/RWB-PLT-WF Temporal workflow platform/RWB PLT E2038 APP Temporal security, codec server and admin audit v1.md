# RWB-PLT-E2038-APP Temporal security, codec server and admin audit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2038-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-PLT-WF-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E2038-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-PLT-E1070-CON, RWB-PLT-E1071-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1039-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-038 for the workflow platform epic; the codec server, the authorizer audit path and the daily reconciliation become platform work built against RWB-PLT-E2038-CON, and the seven legacy criteria are carried whole. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM)**, I want **decode of workflow payloads limited to an open break-glass grant and every decode, terminate, reset and signal written to the decision log**, so that **workflow history cannot leak personal data and no administrative action on a case workflow is unrecorded**.

This is the split (rework) slice of legacy key RWB-E2-038 under epic RWB-PLT-WF (Template and Rules §R6). No legacy section is copied word for word and no delta copy of an as-built story is made: section 7 carries the seven legacy criteria with every value kept, and the microservice change for the legacy key is described here. The change from the legacy story:

- **Placement.** The codec server stops being a servlet inside the monolith's access module and becomes the codec server of the shared Temporal platform, owned once and used by every workbench namespace (Architecture v5 slide 23; Temporal and Drools design slide 12). The platform team owns it, as it owns the cluster, the namespaces and the codec keys; the Workbench API Specification carries none of its paths.
- **Contract first.** The codec protocol, the authorizer audit call, the entry field contract and the error codes are published on Day 1 by RWB-PLT-E2038-CON with fakes, before any code (ADR-020). This story builds against that contract and its fake.
- **The entry.** The AC-READ, AC-DENY and PLATFORM_ADMIN entries are decision records, written through the DecisionLogApi of RWB-PLT-E1027-CON in the caller's transaction (DP-03); the table `decision_log_entry` stays with rwb-decision (P7) and this story owns no table (DP-01).
- **The read.** The access log is no longer a monolith path but the P4 REST contract `GET /api/recovery/access/v1/admin/access-log`, read one hop from the owner (DP-11, DP-13); the break-glass grant is read through the P4 break-glass contract, which is a C row.
- **The reconciliation.** The 02:00 job stops being Quartz (retired with RWB-TE-007 by Template and Rules §R6) and becomes a Temporal Schedule on the platform task queue that starts `TemporalAdminAuditListener` (DP-10 pattern, through RWB-PLT-E1071-CON).
- **The values.** `PLATFORM_ADMIN` stays a LOV-DECISION data row loaded through RWB-E1-043, now the reference-data contract RWB-PLT-E1043-CON (DP-07); the payload limits, the reconciliation time and the key version list stay configuration (DP-06); the flag `rwb.p3.temporal` stays a parameter read.

The codec server and the audit path are shared platform, not one of the 19 services: Template and Rules §R4 has no platform row, so this story writes no `rwb_*` schema, publishes no `rwb.<short>.events.v1` topic and owns no `/api/recovery/<short>/v1` base. What it does own is the codec server protocol behind the internal ingress, the audit receiver the Temporal frontend calls over mTLS, and the reconciliation Schedule on task queue `rwb-platform` in namespace `rwb-recovery`.

### 2. Business rationale

The history is encrypted by the payload codec, which protects it at rest, but the Temporal Web UI needs a codec server to show a payload. A codec server that answers any Workbench session turns the encryption into a display setting: every history the user can open becomes clear personal data, and no log names the reader. At the same time terminate, reset and signal change the path of a live case, and the only record today is the frontend audit log inside the Temporal namespace, which a Workbench audit query by case cannot read.

This story puts both behind one rule: a decode is allowed only for RW-SECADM with an open break-glass grant against an incident, and every administrative call writes a decision log entry before the frontend executes it. It meets REQ-DRI-001 (one record per decision) and REQ-DRI-005 (no action without its entry), and it supports NFR-045, because a synthetic history is the only thing a test may carry and a clear payload is never a screen default. The measure is that no clear payload leaves the codec server without an AC-READ entry naming the grant, and that the daily reconciliation finds no administrative action without an entry.

After the split the two paths are also the platform's, and that is the point of moving them into this epic. The codec server sits in the layer the platform team owns once (Architecture v5 slide 23), so a second workbench inherits the rule instead of writing its own; the authorizer plugin is configuration of the same frontend the platform team operates; and the reconciliation becomes a Temporal Schedule instead of a Quartz trigger, so it lives where every other Recovery timer lives. The alternative — a codec server per service and a Quartz job per module — would give the bank one place per workbench where a clear payload can be read and no single place where an administrative action is proven recorded.

### 3. Preconditions

- RWB-PLT-E2038-CON is published: the codec protocol models, the payload metadata rule, the authorizer audit call, the entry field contract, the error codes and the three fakes.
- The nine platform contracts are published: RWB-PLT-E1027-CON (the local decision-record library and the DecisionLogApi), RWB-PLT-E1042-CON (parameters), RWB-PLT-E1043-CON (reference data, the LOV-DECISION row), RWB-PLT-E1047-CON (naming), RWB-PLT-E1044-CON (per-service Flyway baseline), RWB-PLT-N001-CON (the gateway route the access log read passes through, DP-19), RWB-PLT-E1070-CON (the cluster, namespace `rwb-recovery`, mTLS, the Web UI values file and the authorizer plugin slot) and RWB-PLT-E1071-CON (the workflow kit and the Schedule template, DP-10).
- The three owner contracts are consumed as C rows through their fakes: RWB-P3-E1042-CON (parameters), RWB-P3-E1043-CON (reference data) and RWB-P4-E1039-CON (the break-glass grant, the AC-BGON entry, `GET /api/recovery/access/v1/admin/access-log` and the LOV-DECISION codes AC-READ and AC-DENY).
- `PLATFORM_ADMIN` is added as a LOV-DECISION value as a system event code through the versioned reference load of RWB-E1-043, loaded by the data steward role; the addition is recorded in the additions file.
- The codec server runs behind the internal ingress and the Web UI codec endpoint setting names it per environment; no key and no codec runs on a workstation.
- Key Vault holds the codec key with versions 1, 2 and 3, version 2 current at the start of the test and version 3 after the rotation drill; SY-CASEWF holds unwrap on every enabled version.
- The Temporal frontend loads the authorizer plugin from the values file of RWB-PLT-E1070-CON and reaches the audit receiver over mTLS.
- The platform login that runs the codec server, the audit receiver and the reconciliation Schedule, and the internal ingress base of the codec server, are Not specified in the source documents (GAP-1441; ASM-2536).
- The feature flag `rwb.p3.temporal` is on in SIT, read through the parameters contract rather than from a code constant.
- No approval is required to start: the story is Draft (realignment v1) and builds against the published contracts and their fakes.

### 4. Flow

1. RW-SECADM: raises a break-glass request in the bank IAM against an open incident for area PLATFORM_ADMINISTRATION and right R; the IAM approves it, and the account joins the break-glass group until the window ends (RWB-P4-E1039-CON, legacy RWB-E1-039).
2. RW-SECADM: calls `POST /api/recovery/access/v1/admin/break-glass-grants` with the incident reference, the IAM request ID, area PLATFORM_ADMINISTRATION, right R, the scope and the reason; the grant is ACTIVE with an end time.
3. RW-SECADM: opens a workflow in the Temporal Web UI and asks for a payload; the Web UI calls the codec server `POST /decode`, the Temporal codec server protocol, with the namespace, workflow ID, run ID, request ID and the encoded payloads.
4. BreakGlassGrantChecker: checks the session, the role RW-SECADM, the ACTIVE grant, its area and its right; a missing, ended or wrong-area grant is a refusal.
5. PayloadGuard: checks the payload count and size, 100 payloads and 1 MB per request, and that every payload carries codec metadata with a key version; a payload without metadata is refused whole.
6. CodecKeyResolver: resolves the key version from the metadata and unwraps it in Key Vault; it never guesses a version and never falls back to a clear read.
7. TemporalAdminAuditWriter: writes the AC-READ entry with the actor, operation DECODE, workflow ID, run ID, payload count, grant and incident through DecisionLogApi; CodecServerController returns the clear payloads only after the entry commits.
8. RW-PLATADM: terminates, resets or signals a workflow from the Web UI or the CLI; TemporalAuthorizerPlugin passes the operation, workflow ID, run ID, actor, grant or reason and the frontend request ID to TemporalAdminAuditReceiver over mTLS.
9. TemporalAdminAuditWriter: writes the PLATFORM_ADMIN entry and returns its ID; the authorizer allows the frontend call only on 201, and a 503 denies it with PERMISSION_DENIED, so the workflow is unchanged.
10. TemporalAdminAuditListener: every day at 02:00 the Temporal Schedule on task queue `rwb-platform` starts the listener, which reads the frontend audit log, matches each terminate, reset and signal to an entry, and raises an incident for any gap without writing an entry of its own. This is the DP-10 pattern in place of the retired Quartz job: the target has no Quartz.
11. RW-AUDIT: reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries through `GET /api/recovery/access/v1/admin/access-log` and holds no decode right.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A history payload carries no codec metadata, because a test or a job wrote it without the codec | The whole request is refused; no payload is returned; one AC-DENY entry records the payload index and the reason; an incident reaches RW-SECADM and RW-PLATADM; no key is guessed | None (422 refusal text) | AC5 |
| X2 | The decision log store is unavailable when an administrative call arrives | The authorizer receives 503 and denies the call with PERMISSION_DENIED; the workflow is unchanged and no entry exists | None (503 refusal text) | AC6 |
| X3 | The frontend audit log holds a terminate, reset or signal with no decision log entry | The reconciliation reports the gap and raises an incident; no entry is invented | None (incident only) | AC7 |
| X4 | A value the story needs is named by no source: the platform login and the internal ingress base of the codec server, the key rotation period and the archive retention the version list depends on | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open; no code constant is written for it | Not specified in the source documents (GAP-1441; ASM-2536) | Section 13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against nine platform contracts and three owner contracts and their fakes; reads no business table and waits for no other story in the lane |
| Negotiable | Payload limits, the reconciliation time, the key version list and the refusal texts are configuration; the role rule and the write-before-act rule are fixed |
| Valuable | A clear payload is one grant and one log entry away, and no administrative action on a case workflow is invisible to audit |
| Estimable | One controller, one grant check, one key resolver, one authorizer plugin, one audit writer and one receiver, one reconciliation workflow |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed grants, key versions and workflows |

### 7. Acceptance criteria

```gherkin
Feature: Temporal security, codec server and admin audit

  Background:
    Given the Temporal Web UI of RWB-E1-070 uses the codec server of the recovery module as its codec endpoint
    Given the codec key has versions 1 and 2 enabled, and version 2 is current
    Given workflow "case-RW-2026-000301" holds a salary slip payload encrypted with key version 2

  Scenario: AC1 Decode needs RW-SECADM and an open grant (legacy RWB-E2-038 AC1)
    Given U-88 holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    When U-88 asks the Web UI to decode the payload at 11:40
    Then the Web UI calls the codec server POST /decode and receives 200 with the clear payload
    Then one decision_log_entry exists with decision code AC-READ, actor U-88, operation DECODE, grant "BG-2026-0042" and incident "INC0004521"
    Then the entry is committed before the response carries the payload
    When U-88 asks again at 12:05, after the grant ended
    Then the response is 403 with MSG-P4-002 and no payload is returned
    When U-53 holds RW-PLATADM with an active grant and asks at 11:50
    Then the request is refused with 403 and MSG-P4-002 because decode needs RW-SECADM

  Scenario: AC2 Every decode and every administrative call writes an entry (legacy RWB-E2-038 AC2)
    Given U-70 holds RW-PLATADM and no break-glass grant
    Given U-88 holds RW-SECADM with grant "BG-2026-0042"
    When U-88 decodes a payload of "case-RW-2026-000301"
    When U-70 terminates "case-RW-2026-000302" with reason "stuck on a bad activity"
    When U-70 resets "case-RW-2026-000303" to event 12
    When U-70 sends signal CaseEvent to "case-RW-2026-000304"
    Then four decision_log_entry rows exist: AC-READ for the decode and PLATFORM_ADMIN for TERMINATE, RESET and SIGNAL
    Then each row carries namespace rwb-recovery, the workflow ID, the run ID, the actor and the reason, and the grant where one applies
    Then the TERMINATE row is committed before the frontend reports "case-RW-2026-000302" TERMINATED
    Then no row holds a payload or a clear personal data field

  Scenario: AC3 Other roles are refused (legacy RWB-E2-038 AC3)
    Given U-53 holds RW-AUDIT with an active grant for area PLATFORM_ADMINISTRATION, right R
    Given U-62 holds RW-CASEOWN and no grant
    When U-53 calls the decode endpoint for "case-RW-2026-000301"
    Then the response is 403 with MSG-P4-002 because RW-AUDIT reads the log and does not decode
    When U-62 calls the decode endpoint
    Then the response is 403 with MSG-P4-002 and no payload is returned
    Then one AC-DENY entry records each refusal with the actor and the area, and no payload

  Scenario: AC4 A key rotation keeps old histories decodable (legacy RWB-E2-038 AC4)
    Given "case-RW-2026-000301" was written when key version 1 was current
    Given "case-RW-2026-000304" was written when key version 2 is current
    When the key is rotated to version 3 and versions 1 and 2 stay enabled
    Then a decode of "case-RW-2026-000301" with a grant returns the clear payload using version 1
    Then a decode of "case-RW-2026-000304" uses version 2
    Then a workflow started after the rotation writes payloads with version 3
    Then the run book keeps every version that a history inside the retention or the archive of RWB-E2-039 names

  Scenario: AC5 A payload without codec metadata is refused (legacy RWB-E2-038 AC5)
    Given a SIT test wrote the history of "case-RW-2026-000305" with the codec off, so its payload carries no codec metadata
    When U-88 decodes that payload with an active grant
    Then the response is 422 and no payload is returned
    Then one AC-DENY entry records the payload index and the reason
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the codec does not guess a key and does not fall back to a clear read

  Scenario: AC6 A failed audit write blocks the administrative call (legacy RWB-E2-038 AC6)
    Given the decision log store is unavailable at 13:00 on 16 November 2026
    When U-70 terminates "case-RW-2026-000306" from the Web UI
    Then the authorizer receives 503 from the audit writer and denies the call with PERMISSION_DENIED
    Then "case-RW-2026-000306" stays RUNNING and no TERMINATE entry exists
    Then the Web UI shows that the action was not taken because the decision could not be recorded
    Then an incident reaches RW-PLATADM

  Scenario: AC7 The reconciliation finds an action with no entry (legacy RWB-E2-038 AC7)
    Given the frontend audit log holds a signal on "case-RW-2026-000307" at 13:02 with no decision_log_entry
    When TemporalAdminAuditListener runs at 02:00 on 17 November 2026
    Then it reports one gap with the workflow ID, the operation and the time
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the incident stays open until the security administrator records the finding in the bank IAM
    Then the job writes no entry of its own
```

The seven criteria above are copied from RWB-E2-038 with every value kept: BG-2026-0042, INC0004521, U-88, U-53, U-62, U-70, key versions 1, 2 and 3, 100 payloads, 1 MB, 422, 403, MSG-P4-002, 13:00, 13:02, 02:00 on 17 November 2026 and case-RW-2026-000301 to -000307. The reconciliation runs as a Temporal Schedule at 02:00 (DP-10 pattern; there is no Quartz in the target) and the codec server keeps the Temporal codec server protocol unchanged. The namespace is `rwb-recovery`, the codec server answers on the platform internal ingress and the access log is read from the P4 base `/api/recovery/access/v1/admin/access-log`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Decode is allowed only for RW-SECADM with an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION and right R; there is no standing decode right | RWB-P4-E1039-CON; REQ-DRI-001 |
| BR2 | The codec server is the only path to a clear payload; the Web UI names it per environment, and no key and no codec runs on a workstation | Architecture v5 slide 24; this contract |
| BR3 | The AC-READ entry is written before the clear payload is returned; a failed write returns no payload | REQ-DRI-005 |
| BR4 | Terminate, reset and signal are recorded by TemporalAuthorizerPlugin before the frontend executes them; a failed write denies the call and leaves the workflow unchanged | REQ-DRI-005 |
| BR5 | Every entry carries the operation, namespace, workflow ID, run ID, actor, reason and, where one applies, the grant and the incident | REQ-DRI-001 |
| BR6 | A decode is recorded with AC-READ and an administrative call with PLATFORM_ADMIN; no entry carries a payload or a personal data field | LOV-DECISION; NFR-045 |
| BR7 | CodecKeyResolver resolves the key version from the payload metadata; a rotation keeps every earlier version enabled for the retention and the archive period, so old histories stay decodable | KeyRotationRunBook; AC4 |
| BR8 | A payload without codec metadata is refused and raises an incident; the codec never guesses a key and never returns a payload it cannot attribute to a version | NFR-045 |
| BR9 | The daily reconciliation compares the frontend audit log with decision_log_entry and raises an incident on any gap; it never writes a missing entry | REQ-DRI-001 |
| BR10 | RW-AUDIT reads the entries through `GET /api/recovery/access/v1/admin/access-log` and has no decode right | RWB-P4-E1039-CON |

### 9. State transitions

None for a case. A break-glass grant and a workflow execution change state, and the story records the change.

| From | Event | Condition | To |
|---|---|---|---|
| ACTIVE (grant) | End time reached, or the grant is revoked in the bank IAM | - | ENDED |
| RUNNING (workflow) | TerminateWorkflowExecution | The PLATFORM_ADMIN entry is committed | TERMINATED |
| RUNNING (workflow) | ResetWorkflowExecution | The PLATFORM_ADMIN entry is committed | The current run closes and a new run starts at the reset point |
| RUNNING (workflow) | SignalWorkflowExecution | The PLATFORM_ADMIN entry is committed | RUNNING, with the signal handled |
| RUNNING (workflow) | TerminateWorkflowExecution with the decision log unavailable | The entry cannot be written | RUNNING, unchanged; the call is denied |

A refused call writes AC-DENY and changes no workflow state. The grant states are the P4 contract's; this story reads the grant and never writes it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM | Requests break-glass in the bank IAM; decodes a payload under an ACTIVE grant; reads the access log (Platform administration, R) |
| RW-PLATADM | Terminates, resets and signals a workflow (Platform administration, U); reads the entries; receives the reconciliation incident |
| RW-AUDIT | Reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries; holds no decode right (Platform administration and Decision log, R) |
| RW-TRIBE | Maintains the authorizer plugin configuration and the key rotation run book; may not decode |
| RW-CASEOWN and the other case roles | No decode right and no administrative call on a workflow |
| SY-CASEWF | Holds unwrap on every enabled key version; in SIT it runs the codec server and the audit writer and connects to the frontend with its certificate (Decision log C) |
| SY-RULES | No part in this story; a call to the codec server or the audit receiver with its certificate is refused |
| The platform identity that runs the codec server, the audit receiver and the reconciliation Schedule | Not specified in the source documents (GAP-1441; ASM-2536) |
| No delegation of authority level applies | A decode or an administrative call is not a credit decision |

Separation of duty: the security administrator who decodes is not the author of the case decision the payload supports, and no person reviews their own break-glass use (RWB-P4-E1039-CON).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per decode, refusal and administrative call) |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for an access event, as RWB-P4-E1039-CON sets it, with the workflow ID in the actions field |
| DF-DEC-003 | decision_log_entry | decision_code | Write, read |
| DF-DEC-014 | decision_log_entry | actions | Write (operation, workflow ID, run ID, payload count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Write, read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |

No field is added. `decision_log_entry` is owned by rwb-decision (P7) under the Ownership Map ruling; this story writes it through DecisionLogApi and reads it through the P4 access log contract. The PLATFORM_ADMIN value is a LOV-DECISION data row loaded through RWB-E1-043, now the reference-data contract of rwb-case, and recorded in the additions file. No payload, no history event and no clear personal data field is written to the decision log. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

The codec server speaks the Temporal codec server protocol on the platform internal ingress. It is not part of the Workbench API Specification: it has no `/api/recovery/<short>/v1` base and no gateway route, and only the Temporal Web UI and the internal network reach it.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/decode` | Returns the clear payloads of one history request | Platform administration R, plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION | `requestId` from the Web UI |
| POST | `/encode` | Returns the encoded form of payloads written by an authorised client | Platform administration R, plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION | `requestId` from the Web UI |

| Item | Value |
|---|---|
| Request | namespace, workflowId, runId, requestId, payloads: an array of { metadata: { encoding, keyVersion }, data: base64 } |
| Response 200 | payloads: an array of { metadata, data: base64 } in the same order, and entryId |
| Errors | 401 no session; 403 role, grant or area (MSG-P4-002); 413 more than 100 payloads or 1 MB; 422 a payload without codec metadata or a key version that is not enabled; 503 Key Vault unavailable or the entry could not be written (no payload returned) |
| Authorization | Platform administration, right R, plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION |
| Idempotency | `requestId` from the Web UI; a repeat with the same requestId returns the same payloads and entryId and writes no second entry |
| Base | The internal ingress base per environment is Not specified in the source documents (GAP-1441; ASM-2536); the operations above are the published surface |

#### 12.2 REST operations consumed

| Operation | Provider | Used for | Pattern |
|---|---|---|---|
| GET /api/recovery/access/v1/admin/access-log | rwb-access (P4) | The entries with event codes AC-READ, AC-DENY and PLATFORM_ADMIN, for RW-AUDIT and for the reconciliation read (authorization and errors unchanged) | DP-11, DP-13 |

The active grant is read through the published break-glass interface of RWB-P4-E1039-CON; this story adds no method to it. The DecisionLogApi of RWB-PLT-E1027-CON is called in process as a library, not over REST, so it is not a consumption row.

#### 12.3 Events published

None. The platform owns no topic: the entries travel through the decision-record library of RWB-PLT-E1027-CON, which publishes `DecisionRecorded` on `rwb.decision-record.v1` from the caller's transaction, and that event is the library's, not this story's.

#### 12.4 Events consumed

None. The reconciliation reads the frontend audit log through the Temporal frontend API and the entries through the access log read of 12.2; it subscribes to no topic.

#### 12.5 Workflows and activities

| Name | Type | Runs on | Purpose |
|---|---|---|---|
| CodecServerController | Controller | The codec server, internal ingress | `POST /decode` and `POST /encode` with the access check, the guard and the response after the entry (BR2, BR3) |
| BreakGlassGrantChecker | Service | The codec server process | Reads the ACTIVE grant through the P4 contract and checks role, area and right (BR1) |
| PayloadGuard | Service | The codec server process | Payload count and size limits, codec metadata and key version check (BR8) |
| CodecKeyResolver | Service | The codec server process | Resolves the key version from the metadata and unwraps it in Key Vault (BR7) |
| TemporalAdminAuditWriter | Service | The codec server process and the audit receiver | Builds and writes the AC-READ, AC-DENY and PLATFORM_ADMIN entries through DecisionLogApi (BR5, BR6) |
| TemporalAdminAuditReceiver | Service | The audit receiver, mTLS only | Receives the authorizer audit record from the frontend and writes it through TemporalAdminAuditWriter (BR4) |
| TemporalAuthorizerPlugin | Configuration | The Temporal frontend, from the values file of RWB-PLT-E1070-CON | The frontend Authorizer and ClaimMapper: calls the receiver and denies on any non-201 response (BR4) |
| TemporalAdminAuditListener | Workflow with an activity on task queue `rwb-platform` | Namespace `rwb-recovery` | Daily reconciliation of the frontend audit log against decision_log_entry (BR9) |

No other workflow is started, and no activity of this story runs on a service task queue.

#### 12.6 Schedules

| Schedule | Cadence | Task queue | Legacy reference |
|---|---|---|---|
| TemporalAdminAuditListener reconciliation | Daily at 02:00, overlap policy SKIP | `rwb-platform` | The legacy 02:00 reconciliation job, carried by a Temporal Schedule instead of Quartz (DP-10; RWB-TE-007 retired) |

The Schedule is created from the workflow kit template of RWB-PLT-E1071-CON, in namespace `rwb-recovery`, with the tenant and retention of the platform namespace. Its catch-up window and overlap policy are configuration.

#### 12.7 Tables owned

None. `decision_log_entry` is owned by rwb-decision (P7) under the Ownership Map ruling and is written through DecisionLogApi only; the frontend audit log belongs to the Temporal namespace and is read, never written. This story owns no `rwb_*` schema, no table and no migration, and it reads no table of another service (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Codec server fake (RWB-PLT-E2038-CON) | `POST /decode` and `POST /encode` with the payload metadata rule, the 401, 403, 413, 422 and 503 examples and the entryId | This story's controller and guard tests |
| Authorizer audit fake (RWB-PLT-E2038-CON) | The audit call with the 201 entryId and the 503 answer | The plugin configuration test and AC6 |
| Fake authorizer (RWB-PLT-E2038-CON) | The deny-on-non-201 rule, for the Web UI and CLI path | AC2 and AC6 |
| rwb-access break-glass fake (RWB-P4-E1039-CON) | The grant read, the AC-BGON entry, the access log read and the LOV-DECISION codes AC-READ and AC-DENY, with the ACTIVE, ENDED and wrong-area variants | AC1, AC3, AC7 and BR10 |
| Decision-record fake (RWB-PLT-E1027-CON) | The DecisionLogApi write and its failure, with the entry field contract | AC2, AC5 and AC6 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 codec operations on the internal ingress, with no service base | 1 consumption row (the P4 access log read) | Codec server protocol, one hop to the owner, 2 s timeout on the read |
| Kafka | 0 | 0 | No topic of its own; the entry event belongs to the decision-record library |
| Temporal | 1 Schedule (`TemporalAdminAuditListener`, 02:00) plus the codec path and the authorizer audit call | 0 | Namespace `rwb-recovery`, task queue `rwb-platform` |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** The codec server, the grant check, the guard, the key resolver, the audit writer and the receiver in the platform workflow module (Java package `th.co.scb.ace.workbench.recovery.workflow.security`); the authorizer plugin configuration in `deploy/temporal/plugins/`; the reconciliation workflow in the same module; the key rotation run book in `docs/operations/runbooks/`. The final Java package inside the plugin repository, and the deployment names of the two services, are Not specified in the source documents (GAP-1441; ASM-2536) and follow the platform template of RWB-PLT-TPL rather than this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CodecServerController | Controller | `POST /decode` and `POST /encode` on the codec server with the access check and the response after the entry (BR2, BR3) |
| BreakGlassGrantChecker | Service | Reads the ACTIVE grant and checks role, area and right (BR1) |
| PayloadGuard | Service | Payload count and size limits; codec metadata and key version check (BR8) |
| CodecKeyResolver | Service | Resolves the key version from the metadata and unwraps it in Key Vault (BR7) |
| TemporalAdminAuditWriter | Service | Builds and writes the AC-READ, AC-DENY and PLATFORM_ADMIN entries through DecisionLogApi (BR5, BR6) |
| TemporalAuthorizerPlugin | Configuration | The Temporal frontend Authorizer and ClaimMapper: calls the receiver and denies on any non-201 response (BR4) |
| TemporalAdminAuditReceiver | Service | Receives the authorizer audit record over mTLS and writes it through TemporalAdminAuditWriter (BR4) |
| TemporalAdminAuditListener | Workflow | Daily reconciliation of the frontend audit log against decision_log_entry, started by the 02:00 Schedule (BR9) |
| KeyRotationRunBook | Document | The rotation steps, the version list and the version retention rule (BR7, AC4) |

**Database.** No migration. The entries go to `decision_log_entry` through the existing writer in the caller's transaction, and the owner of that table is rwb-decision (P7). LOV-DECISION gains PLATFORM_ADMIN as a data row through RWB-E1-043; no table and no column is added, and the Flyway baseline of RWB-PLT-E1044-CON is unchanged by this story.

**Configuration and reference data**

- Codec endpoint URL per environment in the Web UI; the codec server is reachable only from the Web UI ingress and the internal network.
- Limits: 100 payloads and 1 MB per request; the reconciliation runs daily at 02:00. Both are read as parameters through RWB-PLT-E1042-CON and are never code constants (DP-06).
- Key versions: every version named by a history inside the retention (30 days) or the archive of legacy RWB-E2-039 stays enabled. The archive retention, the key rotation period and the retention that keeps a version enabled are Not specified in the source documents (GAP-1441; ASM-2536); the working read is section 3 of the assumption, and the run book carries the version list as release evidence.
- The LOV value PLATFORM_ADMIN is a data row in LOV-DECISION loaded through RWB-E1-043 (DP-07), recorded in the additions file.
- Feature flag `rwb.p3.temporal` through the parameters contract. Off: the codec endpoint returns 404, the authorizer plugin is not configured and the reconciliation Schedule is paused; the cluster and the Web UI are unchanged.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows the legacy markers call for. **DP-03** is the centre of the story: every decode, refusal and administrative call is a decision record, written through the local decision-record library with the seven field groups, hash-linked into the central ledger and published as `DecisionRecorded`; the story owns no ledger and no table, it fills DF-DEC-001 to DF-DEC-018 in the caller's transaction. **DP-11** replaces the monolith's in-process call to the access log with one REST hop to `GET /api/recovery/access/v1/admin/access-log`, with a 2 s timeout and a breaker, and the audit and the reconciliation both read it there; no path is copied into this story. **DP-13** is why the legacy module path for the access log is not republished: the read becomes `/api/recovery/access/v1/admin/access-log` and the codec server, which never sat under the monolith base, publishes no base of its own. DP-05 applies negatively — the story reads no ACE view and no extension table — and DP-15 applies as "no migration", because the only table touched is another owner's. DP-14 applies to the entry event the library publishes, not to a topic of this story. DP-19 is the gateway route the access log read passes through for the audit role. DP-10 is the pattern the 02:00 reconciliation follows; it adds no new dependency because the workflow kit contract is already an H row of this story.

**Build steps**

1. Add the PLATFORM_ADMIN LOV value through the versioned reference load and confirm the decision log writer accepts it as a system event (DP-07).
2. Build PayloadGuard and CodecKeyResolver with the version from the metadata; test AC4 with versions 1 and 2 and a rotation to 3.
3. Build BreakGlassGrantChecker and CodecServerController with the write-before-return order; tests AC1, AC3 and AC5.
4. Build TemporalAdminAuditWriter and TemporalAdminAuditReceiver; test AC2 for the four operations and the 201 rule.
5. Configure TemporalAuthorizerPlugin from the values file of RWB-PLT-E1070-CON to call the receiver and deny on 503; test AC6 with the decision log stopped.
6. Build TemporalAdminAuditListener and its 02:00 Schedule on task queue `rwb-platform`, with the incident; test AC7 with a planted frontend audit entry.
7. Run the two access tests, the key rotation drill in SIT, and record the version list and the run book in the release evidence.

**Done when.** The tests in section 16 pass, the rotation drill decodes a history written under an earlier key version, the reconciliation finds no gap over seven days, and the access log shows every decode with its grant and incident.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role is not RW-SECADM, the grant is missing, ended or for another area, or the caller is not the platform identity on the internal endpoint | You cannot {action} here. Your role does not include it. |

A 401 returns the standard no-session text. A 413 names the payload count or the request size only. A 422 names the payload index and the missing codec metadata, but never the payload. A 503 says the action was not taken because the decision could not be recorded. None of these adds a message ID. MSG-P4-002 exists and is reused unchanged, with {action} set to "decode this workflow payload" or "record this workflow action". The codec server publishes no message of its own, because it is not on the Workbench API.

### 15. Screens and states

No new Workbench screen. The decode result appears in the payload panel of the Temporal Web UI, which shows the states encoded, decoding and decoded for a user with a grant, and refused with MSG-P4-002 for every other user. The entries appear on the access log read of RWB-P4-E1039-CON and on SCR-38 Decision log query (legacy RWB-E2-005) with the operation in the actions field. SCR-43 Roles and access in Epic 8 shows the grant rule; this story adds no panel to it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-038-01 | AC1, BR1, BR3 | Integration | U-88 RW-SECADM, grant BG-2026-0042 ending 12:00; decode at 11:40 and 12:05 |
| TC-E2-038-02 | AC2, BR4, BR5, BR6 | Integration | One decode, one terminate, one reset and one signal |
| TC-E2-038-03 | AC3, BR1, BR10 | Component | RW-AUDIT and RW-CASEOWN call the decode endpoint; refused with MSG-P4-002 |
| TC-E2-038-04 | AC4, BR7 | Integration | Histories under key versions 1 and 2; rotation to version 3 |
| TC-E2-038-05 | AC5, BR8 | Integration | Payload without codec metadata |
| TC-E2-038-06 | AC6, BR4 | Integration | Decision log stopped; terminate attempted on case-RW-2026-000306 |
| TC-E2-038-07 | AC7, BR9 | Component | Planted frontend audit entry; reconciliation at 02:00 |
| TC-E2-038-08 | BR7, section 13 rotation drill | NFR | Key rotation drill in SIT: rotate to version 3, decode a history written under version 1 |
| TC-E2-038-09 | BR2, BR1 | Component | SY-RULES calls the codec server `POST /decode` with its own certificate; refused with MSG-P4-002 and no entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. Legacy levels map System to Integration and Operational and Access to Component, as above; the rotation drill keeps the NFR level because it measures that an old history stays decodable after a key change.

### 17. Guardrails

- No business value in code: the payload limits, the reconciliation time, the key version list and the refusal texts are configuration read through the parameters contract.
- No personal data in logs, tests, workflow history or prompts: the test payloads are synthetic, and no payload or clear field is written to the decision log or a log line.
- No read of another service's tables and no ACE view: the entries are written through DecisionLogApi and read through the P4 access log contract (DP-01, DP-03, DP-11).
- Decode is never a standing right: no grant, no clear payload, and every decode names its grant and incident.
- No entry, no action: a terminate, reset or signal the authorizer cannot record is denied, not retried after the fact.
- The codec never guesses a key version and never falls back to a clear read.
- No key version is disabled while a history inside the retention or the archive names it.
- The reconciliation never writes a missing entry: it reports the gap and leaves the record to the security administrator.
- The platform publishes no `/api/recovery/<short>/v1` base, no `rwb_*` schema and no topic of its own; the codec server is reached on the internal ingress only (DP-13, §R4).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision, with the seven field groups | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-01, TC-E2-038-02, TC-E2-038-05, TC-E2-038-07 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-02, TC-E2-038-06 |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies | Program BRD v4, NFR table | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-05, TC-E2-038-08 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2038-CON | Contract | H: the codec protocol, the audit call, the entry contract, the errors and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and DecisionLogApi the entries are written through |
| RWB-PLT-E1070-CON | Contract | H: the cluster, namespace `rwb-recovery`, mTLS, the Web UI values file and the authorizer plugin slot |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit and the Schedule template the 02:00 reconciliation uses (DP-10) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: parameters, reference data, naming, the Flyway baseline and the gateway route the audit read passes through |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the owner contracts behind the parameters and reference-data reads (DP-06, DP-07) |
| RWB-P4-E1039-CON | Contract | C: the break-glass grant, the AC-BGON entry, the access log read and the LOV-DECISION codes AC-READ and AC-DENY (DP-11) |
| Legacy RWB-E2-037 (now RWB-PLT-E2037-APP, RWB-PLT-E2037-CON) | App development, Contract | Out of scope: alerts, the stuck scanner and the workflow dashboard |
| Legacy RWB-E2-039 | - | Out of scope: backup, failover, upgrade and archive; its archive period is what the key version list of AC4 depends on |
| Legacy RWB-E2-040 | - | Out of scope: the replay gate and build ID rollout |

### 19. Out of scope

- The Temporal cluster, mTLS, Web UI sign-in and platform roles (legacy RWB-E1-070; RWB-PLT-E1070-APP).
- The codec itself, the worker and the smoke workflow (legacy RWB-E1-071; RWB-PLT-E1071-APP).
- The break-glass request, approval, review and access log writer (legacy RWB-E1-039; RWB-P4-E1039-CON and its app story).
- Alerts, the stuck scanner and the workflow dashboard (legacy RWB-E2-037; RWB-PLT-E2037-APP).
- Backup, failover, upgrade and archive (legacy RWB-E2-039).
- The replay gate and build ID rollout (legacy RWB-E2-040).
- A Workbench screen for workflow payloads or for the admin audit (Epic 8, SCR-43 Roles and access).
- Key Vault provisioning, key escrow and the bank key management standard (SCB IT platform).
- The contract documents and the fakes themselves: RWB-PLT-E2038-CON.
