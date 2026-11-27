# RWB-ITG-E2038-ITG Temporal security, codec server and admin audit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-038 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2038-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2038-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-038 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement and confirms it fits two weeks |
| Depends on (build) | RWB-P4-E1039-APP, RWB-PLT-E2038-APP (not yet done) |
| Contract dependencies | None |
| Integration dependencies | RWB-P4-E1039-APP, RWB-PLT-E2038-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that decodes a workflow payload under an open break-glass grant and records every decode, terminate, reset and signal in the decision log before the frontend acts**, so that **the wave 2 workflow security and administrative audit journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, table, workflow or schedule, it serves no operation and it owns no table. The real behaviour is owned by the two I stories: RWB-P4-E1039-APP (the break-glass grant, the AC-BGON entry, the grant end time and the access log read) and RWB-PLT-E2038-APP (the codec server, the payload guard, the key resolver, the Temporal authorizer audit writer and the daily reconciliation), and those two stories block the ITG run.

The journey also reads the P7 decision log through its contract, because every AC-READ, AC-DENY and PLATFORM_ADMIN row is a decision log entry and the harness asserts the entry before it asserts the payload or the workflow state. That read is asserted through the published contract and the §12.8 fakes; it is not claimed as work of this story.

### 2. Business rationale

The legacy RWB-E2-038 journey crosses more than one service: rwb-access holds the break-glass grant, its end time and the access log read; rwb-decision holds the decision log writer and the entries themselves; the platform workflow service holds the codec server that turns an encrypted history into a readable payload and the Temporal authorizer audit that stands between a terminate, reset or signal and the workflow; and gateway-bff composes the access log for the screen. Until the real services are exercised together, the program cannot show that a clear payload costs one grant and one entry, and that no administrative action on a live case is unrecorded.

The harness gives one repeatable run per business date that proves a decode answers only for RW-SECADM with an ACTIVE grant and writes its AC-READ entry before the payload leaves, that a terminate, reset and signal each write a PLATFORM_ADMIN entry before the frontend acts, that other roles are refused with one AC-DENY entry per refusal, that a key rotation keeps an earlier history decodable while a payload without codec metadata is refused whole, and that a failed audit write denies the call and leaves the workflow RUNNING while the daily reconciliation reports a gap without inventing an entry. It meets REQ-DRI-001 and REQ-DRI-005 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The two I stories are published and deployed in the SIT environment: RWB-P4-E1039-APP (break-glass grants, the AC-BGON entry, the grant end time and the access log read) and RWB-PLT-E2038-APP (the codec server, the authorizer audit writer and the reconciliation).
- The Temporal Web UI of the cluster names the codec server of the platform workflow service as its codec endpoint, per environment.
- Key Vault holds the codec key with versions 1, 2 and 3, version 2 current at the start of the run and version 3 after the rotation step; the unwrap right on every enabled version is held by the workflow service account named in the legacy story.
- LOV-DECISION carries PLATFORM_ADMIN as a system event code, loaded through the versioned reference load by the owning stories; AC-READ, AC-DENY and AC-BGON are already present.
- gateway-bff is deployed with the composite route of DP-19 available for the access log screen.
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents and the codec server protocol stub, so the harness runs from Day 1 before the I stories land.
- The harness environment, its test-data seeding, its evidence format and retention, and the test certificate details: Not specified in the source documents (GAP-0417; ASM-0592).

### 4. Flow

1. Harness: seeds the grant, the users, the seven workflows and the key versions through the owning contracts or the published fakes, and reads the grant back to assert it is ACTIVE with its end time.
2. Harness: decodes the payload of "case-RW-2026-000301" through the codec server at 11:40 as "U-88" with the ACTIVE grant "BG-2026-0042", asserts 200, the clear payload and the entryId.
3. Harness: reads the AC-READ entry through the rwb-decision contract and asserts decision code, actor, operation DECODE, grant, incident "INC0004521" and that the entry time precedes the response time.
4. Harness: repeats the decode at 12:05 after the grant ended, asserts 403 with MSG-P4-002 and no payload.
5. Harness: terminates "case-RW-2026-000302", resets "case-RW-2026-000303" to event 12 and signals CaseEvent to "case-RW-2026-000304" as "U-70"; asserts four entries, the three PLATFORM_ADMIN entries committed before the frontend reports the result, and no payload or personal data field on any row.
6. Harness: drives the decode as "U-53" with RW-AUDIT and as "U-62" with RW-CASEOWN, asserts 403 with MSG-P4-002 on each and one AC-DENY entry per refusal.
7. Harness: rotates the key to version 3 with versions 1 and 2 enabled, decodes the history written under version 1 and the history under version 2, and asserts the version used from the payload metadata; then starts a workflow and asserts its payloads carry version 3.
8. Harness: decodes the history of "case-RW-2026-000305" written with the codec off, asserts 422, no payload, one AC-DENY entry with the payload index and the reason, and no key guess.
9. Harness: stops the decision log answer, terminates "case-RW-2026-000306" as "U-70", asserts 503 read as PERMISSION_DENIED by the authorizer, the workflow still RUNNING and no TERMINATE entry; then plants a signal on "case-RW-2026-000307" in the frontend audit log with no entry, runs the reconciliation at 02:00 and asserts one reported gap and no invented entry.
10. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0417; ASM-0592).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | The grant is missing, ended, or for another area or right | 403 from the codec server; no payload; nothing reaches the workflow | MSG-P4-002 | TC-E2-038-01-ITG | AC1 |
| X2 | The caller holds RW-PLATADM, RW-AUDIT or RW-CASEOWN | 403 from the codec server; no payload; one AC-DENY entry per refusal | MSG-P4-002 | TC-E2-038-03-ITG, TC-E2-038-09-ITG | AC2 |
| X3 | A payload carries no codec metadata | 422 for the whole request; no payload index answers; one AC-DENY entry with the payload index and the reason; no key is guessed | None (422 refusal text) | TC-E2-038-05-ITG | AC3 |
| X4 | More than 100 payloads, or more than 1 MB in one request | 413; no payload returned; no AC-READ entry | None (413 refusal text) | TC-E2-038-01-ITG, TC-E2-038-10-ITG | AC5 (new, D-RCV-60) |
| X5 | A payload names a key version that is not enabled | 422; no payload returned; one AC-DENY entry; no fallback to a clear read | None (422 refusal text) | TC-E2-038-04-ITG, TC-E2-038-11-ITG | AC6 (new, D-RCV-60) |
| X6 | The decision log store is unavailable when an administrative call arrives | 503 to the authorizer, read as PERMISSION_DENIED; the workflow is unchanged and no entry exists | None (503 refusal text) | TC-E2-038-06-ITG | AC4 |
| X7 | The frontend audit log holds a terminate, reset or signal with no entry | The reconciliation reports the gap with workflow ID, operation and time; no entry is written by the job | None (incident only) | TC-E2-038-07-ITG | AC4 |
| X8 | A caller presents a certificate that is not the workflow service's, or the frontend's on the audit endpoint | 403 with MSG-P4-002 on the codec path; a refused mTLS handshake on the audit endpoint; no entry | MSG-P4-002 | TC-E2-038-09-ITG, TC-E2-038-12-ITG | AC7 (new, D-RCV-60) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the two I stories are deployed; until then it runs against the §12.8 fakes and the codec protocol stub |
| Negotiable | The harness pack, the seeding, the evidence format and the certificate set are agreed with QA; no business value is fixed by the harness |
| Valuable | The decode and the administrative audit are evidenced across services rather than per service, with the entry order on the same trace |
| Estimable | One harness project, one journey specification, one fake pack, one rotation drill and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Temporal security, codec server and admin audit - wave 2 integration harness

  Background:
    Given the Temporal Web UI uses the codec server of the platform workflow service as its codec endpoint
    Given the codec key has versions 1 and 2 enabled, and version 2 is current
    Given the codec server accepts at most 100 payloads and 1 MB per request
    Given workflow "case-RW-2026-000301" holds a salary slip payload encrypted with key version 2
    Given the workflows "case-RW-2026-000302", "case-RW-2026-000303", "case-RW-2026-000304" and "case-RW-2026-000306" are RUNNING

  Scenario: AC1 A decode needs RW-SECADM with an open grant, and the entry is committed first (new, D-RCV-60)
    Given user "U-88" holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    When the harness decodes the payload of "case-RW-2026-000301" through the codec server at 11:40
    Then the codec server answers 200 with the clear payload and an entryId
    And one decision log entry exists with decision code AC-READ, actor "U-88", operation DECODE, grant "BG-2026-0042" and incident "INC0004521"
    And that entry is committed before the response carries the payload
    And the run report holds the entryId and the response time on one trace across the gateway and each owning service
    And no service reads another service's schema and no entry holds a payload
    When the harness decodes again at 12:05, after the grant ended
    Then the answer is 403 with MSG-P4-002 and no payload is returned

  Scenario: AC2 Terminate, reset and signal each write PLATFORM_ADMIN before the frontend acts, and other roles are refused (new, D-RCV-60)
    Given user "U-70" holds RW-PLATADM and no break-glass grant
    Given user "U-88" holds RW-SECADM with grant "BG-2026-0042"
    When the harness decodes a payload of "case-RW-2026-000301"
    When the harness terminates "case-RW-2026-000302" with reason "stuck on a bad activity"
    When the harness resets "case-RW-2026-000303" to event 12
    When the harness sends signal CaseEvent to "case-RW-2026-000304"
    Then four decision log entries exist: AC-READ for the decode and PLATFORM_ADMIN for TERMINATE, RESET and SIGNAL
    And each entry carries namespace rwb-recovery, the workflow ID, the run ID, the actor and the reason, and the grant where one applies
    And the TERMINATE entry is committed before the frontend reports "case-RW-2026-000302" TERMINATED
    And the RESET entry is committed before the current run closes, and the SIGNAL entry before the signal is handled
    And no entry holds a payload or a clear personal data field
    Given user "U-53" holds RW-AUDIT with an active grant for area PLATFORM_ADMINISTRATION, right R
    Given user "U-62" holds RW-CASEOWN and no grant
    When "U-53" asks the codec server to decode "case-RW-2026-000301"
    Then the answer is 403 with MSG-P4-002 because RW-AUDIT reads the log and does not decode
    When "U-62" asks the codec server to decode
    Then the answer is 403 with MSG-P4-002 and no payload is returned
    And one AC-DENY entry records each refusal with the actor and the area, and no payload

  Scenario: AC3 A key rotation keeps an older history decodable, and a payload without codec metadata is refused whole (new, D-RCV-60)
    Given "case-RW-2026-000301" was written when key version 1 was current and "case-RW-2026-000304" was written when key version 2 is current
    When the key is rotated to version 3 and versions 1 and 2 stay enabled
    Then a decode of "case-RW-2026-000301" with an active grant returns the clear payload using version 1
    And a decode of "case-RW-2026-000304" uses version 2
    And a workflow started after the rotation writes payloads with version 3
    And every version named by a history inside the retention stays enabled
    Given "case-RW-2026-000305" was written with the codec off, so its payload carries no codec metadata
    When "U-88" decodes that payload with an active grant
    Then the answer is 422 and no payload is returned
    And one AC-DENY entry records the payload index and the reason
    And the codec does not guess a key and does not fall back to a clear read

  Scenario: AC4 A failed audit write denies the call, and the reconciliation reports a gap without inventing an entry (new, D-RCV-60)
    Given the decision log store is unavailable at 13:00 on 16 November 2026
    When "U-70" terminates "case-RW-2026-000306" from the Web UI
    Then the authorizer receives 503 from the audit writer and denies the call with PERMISSION_DENIED
    And "case-RW-2026-000306" stays RUNNING and no TERMINATE entry exists
    When the frontend audit log holds a signal on "case-RW-2026-000307" at 13:02 with no decision log entry
    And the reconciliation runs at 02:00 on 17 November 2026
    Then it reports one gap with the workflow ID, the operation and the time
    And an incident reaches RW-SECADM and RW-PLATADM
    And the job writes no entry of its own, and no entry is invented for "case-RW-2026-000307"

  Scenario: AC5 A decode request over the codec limit is refused whole, with no payload and no read entry (new, D-RCV-60)
    Given user "U-88" holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    When the harness sends one decode request with more than 100 payloads at 11:40
    Then the codec server answers 413 and no payload is returned
    When the harness sends one decode request with more than 1 MB at 11:40
    Then the codec server answers 413 and no payload is returned
    And no AC-READ entry exists for either request

  Scenario: AC6 A payload naming a key version that is not enabled is refused with no fallback to a clear read (new, D-RCV-60)
    Given user "U-88" holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    And "case-RW-2026-000304" names a key version that is not enabled
    When "U-88" decodes the payload of "case-RW-2026-000304" at 11:40
    Then the answer is 422 and no payload is returned
    And one AC-DENY entry records the refusal
    And the codec does not fall back to a clear read

  Scenario: AC7 Only the codec path with the workflow service's certificate reaches a clear payload (new, D-RCV-60)
    Given the codec server is the only path to a clear payload for the Web UI
    When SY-RULES calls POST /decode with its own certificate
    Then the answer is 403 with MSG-P4-002 and no payload is returned
    And no entry is written
    When a caller presents a certificate that is not the frontend's to the audit endpoint
    Then the mTLS handshake is refused and no entry is written

  Scenario: AC8 The Web UI names the codec server per environment, and no key or codec runs on a workstation (new, D-RCV-60)
    Given the Temporal Web UI of the environment names the codec server of the platform workflow service as its codec endpoint
    When the harness reads the history of "case-RW-2026-000301" from a workstation without calling the codec server
    Then the payload stays encrypted and no clear payload is shown
    And no key and no codec runs on the workstation
```

These criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Decode is allowed only for RW-SECADM with an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION and right R; there is no standing decode right | RWB-E1-039; REQ-DRI-001 |
| BR2 | The codec server is the only path to a clear payload; the Web UI names it per environment, and no key or codec runs on a workstation | D-RCV-36 T1 |
| BR3 | The AC-READ entry is written before the clear payload is returned; a failed write returns no payload | REQ-DRI-005 |
| BR4 | Terminate, reset and signal are recorded by the Temporal authorizer before the frontend executes them; a failed write denies the call and leaves the workflow unchanged | REQ-DRI-005 |
| BR5 | Every entry carries the operation, namespace, workflow ID, run ID, actor, reason and, where one applies, the grant and the incident | REQ-DRI-001 |
| BR6 | A decode is recorded with AC-READ and an administrative call with PLATFORM_ADMIN; no entry carries a payload or a personal data field | LOV-DECISION; NFR-045 |
| BR7 | The codec resolves the key version from the payload metadata; a rotation keeps every earlier version enabled for the retention and the archive period, so old histories stay decodable | D-RCV-36 T1 |
| BR8 | A payload without codec metadata is refused and raises an incident; the codec never guesses a key and never returns a payload it cannot attribute to a version | NFR-045 |
| BR9 | The daily reconciliation compares the frontend audit log with decision_log_entry and raises an incident on any gap; it never writes a missing entry | REQ-DRI-001 |
| BR10 | RW-AUDIT reads the entries through the access log and has no decode right | RWB-E1-039 |

The harness asserts these ten rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None caused by the harness. The harness changes no grant and no workflow; it observes what the owning services do and asserts it.

| From | Event | Condition | To |
|---|---|---|---|
| ACTIVE (grant) | End time reached, or the grant is revoked in the bank IAM | - | ENDED |
| RUNNING (workflow) | TerminateWorkflowExecution | The PLATFORM_ADMIN entry is committed | TERMINATED |
| RUNNING (workflow) | ResetWorkflowExecution | The PLATFORM_ADMIN entry is committed | The current run closes and a new run starts at the reset point |
| RUNNING (workflow) | SignalWorkflowExecution | The PLATFORM_ADMIN entry is committed | RUNNING, with the signal handled |
| RUNNING (workflow) | TerminateWorkflowExecution with the decision log unavailable | The entry cannot be written | RUNNING, unchanged; the call is denied |

A refusal writes AC-DENY and changes no workflow state.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Grant ACTIVE then ENDED | rwb-access break-glass grant | The 403 with MSG-P4-002 at 12:05 (TC-E2-038-01-ITG) |
| Workflow TERMINATED | The authorizer and the frontend | The PLATFORM_ADMIN TERMINATE entry before the frontend result (TC-E2-038-02-ITG) |
| Workflow RUNNING after a refused terminate | The authorizer denial | No entry and no state change (TC-E2-038-06-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM, security administrator | The synthetic user the harness drives: requests break-glass, decodes a payload under an ACTIVE grant, reads the access log (Platform administration, R) |
| RW-PLATADM, platform administrator | Terminates, resets and signals a workflow (Platform administration, U); reads the entries; receives the reconciliation incident |
| RW-AUDIT, internal audit | Reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries and holds no decode right (Platform administration and Decision log, R); used by the refusal case |
| RW-CASEOWN, case owner | No decode right and no administrative call; used by the refusal case |
| SY-CASEWF, case workflow service account | Runs the codec server and the audit writer and calls the audit endpoint with its certificate (Decision log C); the harness asserts its result, it does not act for it |
| SY-RULES, rule evaluator service account | No part in this story; a call to the audit endpoint with its certificate is refused (used by the access case) |

No delegation of authority level applies: a decode or an administrative call is not a credit decision. Authorisation is answered by rwb-access through the break-glass grant and the access log of §12.2.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 rwb-decision contract |
| DF-DEC-002 | decision_log_entry | case_id | Read through the P7 rwb-decision contract; empty for an access event, with the workflow ID in the actions field |
| DF-DEC-003 | decision_log_entry | decision_code | Read through the P7 rwb-decision contract (AC-READ, AC-DENY, AC-BGON, PLATFORM_ADMIN) |
| DF-DEC-014 | decision_log_entry | actions | Read through the P7 rwb-decision contract (operation, workflow ID, run ID, payload count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Read through the P7 rwb-decision contract, and compared with the response time |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read through the P7 rwb-decision contract |
| DF-DEC-031 | decision_log_entry | idempotency_key | Read through the P7 rwb-decision contract |
| Break-glass grant fields | break-glass grant | grant reference, area, right, end time | Read through the P4 rwb-access contract |

No field is added. The PLATFORM_ADMIN value is a LOV-DECISION data row loaded through the owning stories. No payload, no history event and no clear personal data field is read into a run report. Test data is synthetic, and no production case, party or workflow is used.

### 12. Contract

Contract version: this harness builds against v1 of the rwb-access and rwb-decision REST contracts (the `/v1` paths of §12.2), of the event of §12.4, and of the codec server and authorizer audit contract. A breaking change raises v2 and deprecates v1; v1 is never edited in place.

#### 12.1 REST operations provided

None. The harness calls the owning services and the codec server; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/decode` (Temporal codec server protocol, on the codec service URL) | PLT platform workflow service | Decodes the payloads of one workflow execution for the Web UI, and returns the clear payloads with the entryId (Architecture v5: codec server in the cluster) |
| POST | `/api/recovery/access/v1/admin/break-glass-grants` | P4 rwb-access | Raises the ACTIVE grant "BG-2026-0042" with its area, right, scope, incident and end time |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | Reads the AC-READ, AC-DENY, AC-BGON and PLATFORM_ADMIN entries for the journey |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Reads the entries by workflow ID, actor and time, and asserts their order against the response and the frontend result |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Reads one entry back by the entryId the codec server or the audit writer returned |

The authorizer audit is an internal mTLS call from the Temporal frontend plugin, not an HTTP path: it carries operation (TERMINATE, RESET or SIGNAL), namespace rwb-recovery, workflow ID, run ID, actor, the grant where one applies, reason and the frontend request ID, and it answers entryId, which the plugin reads as 201. It is owned by the platform workflow service (PLT) with the frontend certificate and the network policy of the frontend pods only.

The access log screen is served through gateway-bff's composite route (DP-19), owned by the platform edge story RWB-PLT-N001-CON; the harness reads the log through the composite route and repeats the read directly on rwb-access, and both answers carry the same entries.

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The AC-READ, AC-DENY and PLATFORM_ADMIN entries of the journey reach the central ledger within 5 minutes of the call, and the entryId in the decode or audit answer resolves to the ledger entry |

The event is consumed for assertion only; the harness reads the ledger through the P7 contract rather than from a topic, and order per workflow is guaranteed by the workflow key on the topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity or schedule; it drives REST and the codec protocol, and it exercises the Temporal frontend terminate, reset and signal through the owning story's authorizer configuration.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow. The daily reconciliation at 02:00 is a Schedule owned and run by RWB-PLT-E2038-APP; the harness triggers it through the owning contract and asserts its report.

#### 12.7 Tables owned

None. The entries are decision_log_entry rows owned by P7 rwb-decision, and the grant and the access log are owned by P4 rwb-access.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-access | admin/break-glass-grants, admin/access-log | Grant "BG-2026-0042" ACTIVE for "U-88" with area PLATFORM_ADMINISTRATION, right R, incident "INC0004521" and an end time at 12:00; an ENDED grant for the 12:05 repeat; the access log rows of the journey; 403 with MSG-P4-002 for a role without RW-SECADM |
| rwb-decision | decision-log, decision-log/{entryId} | The AC-READ, AC-DENY, AC-BGON and PLATFORM_ADMIN entries of the seven workflows with their entryIds and times; a forced write failure for the 503 case; a forced missing entry for the reconciliation case |
| platform codec server (PLT) | POST /decode | 200 with clear payloads for key versions 1 and 2; 422 for a payload without codec metadata and for a version that is not enabled; 403 with MSG-P4-002 for RW-PLATADM, RW-AUDIT and RW-CASEOWN; 413 above 100 payloads or 1 MB |
| platform authorizer audit (PLT) | internal mTLS audit record | 201 with entryId for TERMINATE, RESET and SIGNAL; 503 for the unavailable-decision-log case, which the plugin denies with PERMISSION_DENIED |

The real-codec test path runs the same journey against the codec server of the platform workflow service in SIT, with the Key Vault versions 1, 2 and 3 and the test certificate of each caller, and replaces the codec fake as RWB-PLT-E2038-APP lands. The test certificate details, the harness repository, the seeding and the evidence format and retention: Not specified in the source documents (GAP-0417; ASM-0592).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Five consumed operations of §12.2: the codec server, the grant, the access log and two decision log reads; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 for the ledger assertion; publishes nothing |
| Temporal | Yes | Calls TerminateWorkflowExecution, ResetWorkflowExecution and SignalWorkflowExecution on the Temporal frontend over mTLS through the authorizer plugin of RWB-PLT-E2038-APP; starts no workflow and adds no activity |
| File | No | Reads and writes no payload file; every payload is asserted through the codec protocol answer and never stored in clear |

### 13. Solution plan

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

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the two I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| CodecClient | Harness adapter | Calls POST /decode with the namespace, workflow ID, run ID, requestId and the payloads, and records the answer, the entryId and the response time |
| AdminCallClient | Harness adapter | Drives the terminate, reset and signal on the Temporal frontend over mTLS, and the grant and access log reads through the owning contracts |
| FakePack | WireMock project | Serves rwb-access, rwb-decision and the codec protocol from the published OpenAPI documents and the codec contract of §12.8 |
| EntryOrderCheck | Assertion | Fails the run when an AC-READ entry is not committed before the clear payload is returned, or a PLATFORM_ADMIN entry when the frontend result is reported |
| DenyEvidenceCheck | Assertion | Fails the run when a refusal has no AC-DENY entry, or when an AC-DENY or AC-READ row carries a payload or a personal data field |
| KeyVersionCheck | Assertion | Fails the run when a decode uses a version other than the one in the payload metadata, when a rotation disables a version still named by a history, or when a payload without metadata returns anything but 422 |
| ReconciliationCheck | Assertion | Fails the run when the reported gap count differs from the planted gap, or when the job writes an entry of its own |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0417; ASM-0592) |

**Environment and test data**

- Environment: SIT, one namespace (rwb-recovery), the two I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment, certificate set and data seeding: Not specified in the source documents (GAP-0417; ASM-0592).
- Data: the synthetic workflows "case-RW-2026-000301" to "case-RW-2026-000307", the users "U-88", "U-70", "U-53" and "U-62", the grant "BG-2026-0042", the incident "INC0004521", the key versions 1, 2 and 3, the limits of 100 payloads and 1 MB, and the reconciliation time 02:00. Every payload is synthetic and no production record is copied.
- Reset: each run starts from the seeded state with version 2 current, so a repeated run is deterministic and the same report is produced; the rotation step restores version 2 current at the end of the run.

**Build steps**

1. Build JourneyRunner, CodecClient and AdminCallClient against the published contracts and the codec protocol.
2. Publish FakePack for rwb-access, rwb-decision and the codec protocol, and prove the harness runs green from Day 1 on the fakes.
3. Add the decode journey of AC1 with EntryOrderCheck: 200, the AC-READ entry, the grant, the incident and the 403 at 12:05.
4. Add the administrative set of AC2: the four entries, the three PLATFORM_ADMIN rows committed first, and the refusal of RW-AUDIT and RW-CASEOWN with one AC-DENY each.
5. Add the rotation and metadata set of AC3 with KeyVersionCheck: versions 1 and 2 decoded after the rotation to 3, and the 422 for a payload without metadata.
6. Add the failure and reconciliation set of AC4: the 503 read as PERMISSION_DENIED, the workflow still RUNNING, the planted gap and the reported gap with no invented entry.
7. Replace each fake with the real service as its I story lands, run the rotation drill in SIT against the real codec server, and publish the run report per business date with the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0417; ASM-0592).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.temporal` from the legacy solution plan: with the flag off the codec endpoint returns 404, the authorizer plugin is not configured and the reconciliation does not run; the harness asserts the disabled and the enabled state.

**Done when:** the journey runs green against the two deployed I stories in SIT, the rotation drill decodes a history written under an earlier key version, the run report for the business date holds every assertion of §7 and §16 with its trace, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role is not RW-SECADM, the grant is missing, ended or for another area, or the caller is not the workflow service account on the internal endpoint | You cannot {action} here. Your role does not include it. |

A 401 returns the standard no-session text. A 413 returns the standard payload-limit text. A 422 names the payload index and the missing codec metadata, but never the payload. A 503 says the action was not taken because the decision could not be recorded. The Temporal denial carries PERMISSION_DENIED and no message ID. None of these cases adds a message ID. MSG-P4-002 exists and is reused unchanged, with {action} set to "decode this workflow payload" or "record this workflow action".

The harness asserts the message ID and the substituted values; it does not own the message text. Thai text for each message follows decision DL10.

Open decision: DL10 (the Thai name for each field, label and message; business lead with Legal and Compliance) is still open, with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. It does not block this harness, which asserts only the message ID and the substituted values.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| Temporal Web UI payload panel | Encoded | The panel shows the encrypted payload and offers decode to a user with the right |
| Temporal Web UI payload panel | Decoding | The codec server is called once and the answer carries the entryId |
| Temporal Web UI payload panel | Decoded | The clear payload is returned after the AC-READ entry is committed |
| Temporal Web UI payload panel | Refused | The answer carries MSG-P4-002 and the panel shows no payload |
| SCR-38 Decision log query | Read only | The PLATFORM_ADMIN and AC-READ rows show the operation in the actions field |
| SCR-38 Decision log query | Empty | Not specified in the source documents (CG-ALL-788) |
| SCR-38 Decision log query | Loading | As set in Screen Specifications v1, section SCR-38 (CG-ALL-788) |
| SCR-38 Decision log query | Error | Not specified in the source documents (CG-ALL-788) |
| SCR-38 Decision log query | No access | Not specified in the source documents (CG-ALL-788) |
| SCR-43 Roles and access | Read only | The grant rule is shown; the harness asserts no panel is added to it |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-789) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-789) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-789) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-789) |

The harness opens no screen and renders no page; it asserts the codec protocol answer and the access log answer that the screens consume. Screen-level behaviour remains with the owning APP stories, and the harness environment and evidence detail: Not specified in the source documents (GAP-0417; ASM-0592), to be agreed by the integration lead with the platform workflow owner and QA at the wave 2 entry check.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-038-01-ITG | AC1, BR1, BR3; ITG AC1 | Integration | "U-88" RW-SECADM, grant "BG-2026-0042" ending 12:00; decode at 11:40 and 12:05 |
| TC-E2-038-02-ITG | AC2, BR4, BR5, BR6; ITG AC2 | Integration | One decode, one terminate, one reset and one signal |
| TC-E2-038-03-ITG | AC3, BR1, BR10; ITG AC2 | Component | RW-AUDIT and RW-CASEOWN call the decode endpoint; refused with MSG-P4-002 |
| TC-E2-038-04-ITG | AC4, BR7; ITG AC3 | Integration | Histories under key versions 1 and 2; rotation to version 3 |
| TC-E2-038-05-ITG | AC5, BR8; ITG AC3 | Integration | Payload without codec metadata on "case-RW-2026-000305" |
| TC-E2-038-06-ITG | AC6, BR4; ITG AC4 | Integration | Decision log stopped; terminate attempted on "case-RW-2026-000306" |
| TC-E2-038-07-ITG | AC7, BR9; ITG AC4 | NFR | Planted frontend audit entry on "case-RW-2026-000307"; reconciliation at 02:00 |
| TC-E2-038-08-ITG | Operational; ITG AC3 | NFR | Key rotation drill in SIT: rotate to version 3, decode a version 1 history |
| TC-E2-038-09-ITG | Access; ITG AC2 | Component | SY-RULES calls the codec server POST /decode with its own certificate; refused with MSG-P4-002 and no entry |
| TC-E2-038-10-ITG | AC5 (new, D-RCV-60) | Integration | "U-88" RW-SECADM, grant "BG-2026-0042" ending 12:00; decode with more than 100 payloads and with more than 1 MB at 11:40 |
| TC-E2-038-11-ITG | AC6 (new, D-RCV-60) | Integration | Payload on "case-RW-2026-000304" naming a key version not enabled; decode by "U-88" with grant "BG-2026-0042" |
| TC-E2-038-12-ITG | AC7 (new, D-RCV-60); BR2 | Component | SY-RULES calls POST /decode with its own certificate; a certificate that is not the frontend's presented to the audit endpoint |
| TC-E2-038-13-ITG | AC8 (new, D-RCV-60); BR2 | Component | Web UI codec endpoint setting of the environment; history of "case-RW-2026-000301" read from a workstation without the codec server |

The Covers column names the legacy AC of RWB-E2-038 that the ITG copy is derived from, and the ITG AC is the criterion of §7 that the copy asserts at integration level. The Level column maps the legacy System level to Integration, the legacy Access level to Component and the legacy Operational level to NFR. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the payload limits of 100 payloads and 1 MB, the reconciliation time of 02:00, the key version list and the refusal texts are configuration held by the owning stories; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the test payloads are synthetic, and no payload or clear field is written to the decision log, a log line or a run report.
- No read of another service's schema and no direct ACE read: every read goes through the owner's contract, and this journey reads no case and no ACE table.
- No production data and no outside system: the harness calls only the owning services, the codec server and their fakes, never a production endpoint.
- Decode is never a standing right: the harness fails the run when a clear payload leaves without an ACTIVE grant, an AC-READ entry and its incident.
- No entry, no action: the harness fails the run when a terminate, reset or signal reaches the workflow without its PLATFORM_ADMIN entry, or when a denial leaves the workflow changed.
- The codec never guesses a key version and never falls back to a clear read; the harness fails the run when a payload without metadata returns anything but 422 and one AC-DENY entry.
- The reconciliation never writes a missing entry: the harness fails the run when the job writes a row of its own or reports a gap other than the planted one.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision, with the seven field groups | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-01-ITG, TC-E2-038-02-ITG, TC-E2-038-03-ITG, TC-E2-038-05-ITG, TC-E2-038-07-ITG, TC-E2-038-09-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-02-ITG, TC-E2-038-06-ITG |

TC-E2-038-04-ITG and TC-E2-038-08-ITG assert the payload protection of NFR-045 named in legacy section 2 and in the guardrails; they add no requirement ID of its own. This story adds no requirement ID of its own.

### 19. Out of scope

- The two owning I stories: RWB-P4-E1039-APP (break-glass grants, the AC-BGON entry, the grant end time and the access log read) and RWB-PLT-E2038-APP (the codec server, the payload guard, the key resolver, the authorizer audit writer, the reconciliation and the key rotation run book), and every endpoint, table, workflow and schedule they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-access and rwb-decision and the codec contract of the platform workflow service, which their CON stories own.
- The Temporal cluster, mTLS, the Web UI sign-in and the platform roles (RWB-E1-070).
- The codec itself, the worker and the smoke workflow (RWB-E1-071).
- The break-glass request, approval and review in the bank IAM (RWB-E1-039).
- Alerts, the stuck scanner and the workflow dashboard (RWB-E2-037).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The replay gate and build ID rollout (RWB-E2-040).
- A Workbench screen for workflow payloads or for the administrative audit (Epic 8, SCR-43 Roles and access).
- Key Vault provisioning, key escrow and the bank key management standard.
