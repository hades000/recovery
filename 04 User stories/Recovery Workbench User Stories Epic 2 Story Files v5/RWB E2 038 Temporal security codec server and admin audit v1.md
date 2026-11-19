# RWB-E2-038 Temporal security, codec server and admin audit

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-038 |
| Epic | E2, release 31 December 2026 |
| Module | P4 Access and administration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005 |
| BRD section | Business Requirements Epic 2, section 3.4; Business Requirements Program, sections 6.7 and 6.9 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E1-071, RWB-E1-039 |
| Status | Ready for build |

## 1. Story

As a **security administrator (RW-SECADM)**, I want **decode of workflow payloads limited to an open break-glass grant and every decode, terminate, reset and signal written to the decision log**, so that **workflow history cannot leak personal data and no administrative action on a case workflow is unrecorded**.

## 2. Business rationale

The history is encrypted by PdpaPayloadCodec (RWB-E1-071), which protects it at rest, but the Temporal Web UI needs a codec server to show a payload. A codec server that answers any Workbench session turns the encryption into a display setting: every history the user can open becomes clear personal data, and no log names the reader. At the same time, terminate, reset and signal change the path of a live case, and today the only record is the frontend audit log inside the Temporal namespace, which a Workbench audit query by case cannot read.

This story puts both behind one rule: a decode is allowed only for RW-SECADM with an open break-glass grant against an incident, and every administrative call writes a decision log entry before the frontend executes it. It meets REQ-DRI-001 (one record per decision) and REQ-DRI-005 (no action without its entry), and it supports NFR-045 for personal data in workflow history. The measure is that no clear payload leaves the codec server without an AC-READ entry naming the grant, and that the daily reconciliation finds no administrative action without an entry.

## 3. Preconditions

- RWB-E1-070 is done: the cluster, the namespace rwb-recovery, mTLS, and the Web UI behind Entra ID OIDC with RW-PLATADM operate and RW-AUDIT read.
- RWB-E1-071 is done: PdpaPayloadCodec encrypts every payload with a Key Vault key and records the key version in the payload metadata.
- RWB-E1-039 is done: break-glass grants through POST /admin/break-glass-grants, the AC-BGON entry, the grant end time, GET /admin/access-log and LOV-DECISION with AC-READ, AC-DENY and AC-BGON.
- LOV-DECISION gains PLATFORM_ADMIN as a system event code through the versioned reference load of RWB-E1-043, loaded by RW-DATASTEW; the addition is recorded in the additions file.
- The codec server runs inside the recovery module behind the internal ingress, and the Web UI codec endpoint setting names it per environment.
- Key Vault holds the codec key with versions 1, 2 and 3, version 2 current at the start of the test and version 3 after the rotation drill; SY-CASEWF holds unwrap on every enabled version.
- The Temporal frontend loads the authorizer plugin from the values file of RWB-E1-070 and can reach the internal audit endpoint over mTLS.
- Feature flag rwb.p3.temporal is on in SIT.

## 4. Flow

1. RW-SECADM: raises a break-glass request in the bank IAM against an open incident for area PLATFORM_ADMINISTRATION and right R; the IAM approves it, and the account joins the break-glass group until the window ends (RWB-E1-039).
2. RW-SECADM: calls POST /admin/break-glass-grants with the incident reference, the IAM request ID, area PLATFORM_ADMINISTRATION, right R, the scope and the reason; the grant is ACTIVE with an end time.
3. RW-SECADM: opens a workflow in the Temporal Web UI and asks for a payload; the Web UI calls the codec server POST /decode, the Temporal codec server protocol, with the namespace, workflow ID, run ID and the encoded payloads.
4. BreakGlassGrantChecker: checks the session, the role RW-SECADM, the ACTIVE grant, its area and its right; a missing, ended or wrong-area grant is a refusal.
5. PayloadGuard: checks the payload count and size and that every payload carries codec metadata with a key version; a payload without metadata is refused whole.
6. CodecKeyResolver: resolves the key version from the metadata and unwraps it in Key Vault; it never guesses a version and never falls back to a clear read.
7. TemporalAdminAuditWriter: writes the AC-READ entry with the actor, operation DECODE, workflow ID, run ID, payload count, grant and incident through DecisionLogApi; the controller returns the clear payloads only after the entry commits.
8. RW-PLATADM: terminates, resets or signals a workflow from the Web UI or the CLI; the Temporal authorizer plugin passes the operation, workflow ID, run ID, actor, grant or reason and the frontend request ID to the audit writer over mTLS.
9. TemporalAdminAuditWriter: writes the PLATFORM_ADMIN entry and returns its ID; the authorizer allows the frontend call only on 201, and a 503 denies it with PERMISSION_DENIED, so the workflow is unchanged.
10. TemporalAdminAuditListener: every day at 02:00 reads the frontend audit log, matches each terminate, reset and signal to an entry, and raises an incident for any gap without writing an entry of its own.
11. RW-AUDIT: reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries through GET /admin/access-log and holds no decode right.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A history payload carries no codec metadata, because a test or a job wrote it without the codec | The whole request is refused; no payload is returned; one AC-DENY entry records the payload index and the reason; an incident reaches RW-SECADM and RW-PLATADM; no key is guessed | None (422 refusal text) | AC5 |
| X2 | The decision log store is unavailable when an administrative call arrives | The authorizer receives 503 and denies the call with PERMISSION_DENIED; the workflow is unchanged and no entry exists | None (503 refusal text) | AC6 |
| X3 | The frontend audit log holds a terminate, reset or signal with no decision log entry | The reconciliation reports the gap and raises an incident; no entry is invented | None (incident only) | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cluster and Web UI of RWB-E1-070, the codec of RWB-E1-071 and the break-glass grant of RWB-E1-039; it adds the decode path and the audit path only |
| Negotiable | Payload limits, the reconciliation time, the key version list and the refusal texts are configuration; the role rule and the write-before-act rule are fixed |
| Valuable | A clear payload is one grant and one log entry away, and no administrative action on a case workflow is invisible to audit |
| Estimable | One controller, one grant check, one key resolver, one authorizer plugin, one audit writer and one daily reconciliation |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed grants, key versions and workflows |

## 7. Acceptance criteria

```gherkin
Feature: Temporal security, codec server and admin audit

  Background:
    Given the Temporal Web UI of RWB-E1-070 uses the codec server of the recovery module as its codec endpoint
    Given the codec key has versions 1 and 2 enabled, and version 2 is current
    Given workflow "case-RW-2026-000301" holds a salary slip payload encrypted with key version 2

  Scenario: AC1 Decode needs RW-SECADM and an open grant
    Given U-88 holds RW-SECADM and the ACTIVE break-glass grant "BG-2026-0042" for area PLATFORM_ADMINISTRATION, right R, ending at 12:00 on 16 November 2026
    When U-88 asks the Web UI to decode the payload at 11:40
    Then the Web UI calls the codec server POST /decode and receives 200 with the clear payload
    Then one decision_log_entry exists with decision code AC-READ, actor U-88, operation DECODE, grant "BG-2026-0042" and incident "INC0004521"
    Then the entry is committed before the response carries the payload
    When U-88 asks again at 12:05, after the grant ended
    Then the response is 403 with MSG-P4-002 and no payload is returned
    When U-53 holds RW-PLATADM with an active grant and asks at 11:50
    Then the request is refused with 403 and MSG-P4-002 because decode needs RW-SECADM

  Scenario: AC2 Every decode and every administrative call writes an entry
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

  Scenario: AC3 Other roles are refused
    Given U-53 holds RW-AUDIT with an active grant for area PLATFORM_ADMINISTRATION, right R
    Given U-62 holds RW-CASEOWN and no grant
    When U-53 calls the decode endpoint for "case-RW-2026-000301"
    Then the response is 403 with MSG-P4-002 because RW-AUDIT reads the log and does not decode
    When U-62 calls the decode endpoint
    Then the response is 403 with MSG-P4-002 and no payload is returned
    Then one AC-DENY entry records each refusal with the actor and the area, and no payload

  Scenario: AC4 A key rotation keeps old histories decodable
    Given "case-RW-2026-000301" was written when key version 1 was current
    Given "case-RW-2026-000304" was written when key version 2 is current
    When the key is rotated to version 3 and versions 1 and 2 stay enabled
    Then a decode of "case-RW-2026-000301" with a grant returns the clear payload using version 1
    Then a decode of "case-RW-2026-000304" uses version 2
    Then a workflow started after the rotation writes payloads with version 3
    Then the run book keeps every version that a history inside the retention or the archive of RWB-E2-039 names

  Scenario: AC5 A payload without codec metadata is refused
    Given a SIT test wrote the history of "case-RW-2026-000305" with the codec off, so its payload carries no codec metadata
    When U-88 decodes that payload with an active grant
    Then the response is 422 and no payload is returned
    Then one AC-DENY entry records the payload index and the reason
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the codec does not guess a key and does not fall back to a clear read

  Scenario: AC6 A failed audit write blocks the administrative call
    Given the decision log store is unavailable at 13:00 on 16 November 2026
    When U-70 terminates "case-RW-2026-000306" from the Web UI
    Then the authorizer receives 503 from the audit writer and denies the call with PERMISSION_DENIED
    Then "case-RW-2026-000306" stays RUNNING and no TERMINATE entry exists
    Then the Web UI shows that the action was not taken because the decision could not be recorded
    Then an incident reaches RW-PLATADM

  Scenario: AC7 The reconciliation finds an action with no entry
    Given the frontend audit log holds a signal on "case-RW-2026-000307" at 13:02 with no decision_log_entry
    When TemporalAdminAuditListener runs at 02:00 on 17 November 2026
    Then it reports one gap with the workflow ID, the operation and the time
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then the incident stays open until the security administrator records the finding in the bank IAM
    Then the job writes no entry of its own
```

## 8. Business rules

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
| BR10 | RW-AUDIT reads the entries through GET /admin/access-log and has no decode right | RWB-E1-039 |

## 9. State transitions

None for a case. A break-glass grant and a workflow execution change state, and the story records the change.

| From | Event | Condition | To |
|---|---|---|---|
| ACTIVE (grant) | End time reached, or the grant is revoked in the bank IAM | - | ENDED |
| RUNNING (workflow) | TerminateWorkflowExecution | The PLATFORM_ADMIN entry is committed | TERMINATED |
| RUNNING (workflow) | ResetWorkflowExecution | The PLATFORM_ADMIN entry is committed | The current run closes and a new run starts at the reset point |
| RUNNING (workflow) | SignalWorkflowExecution | The PLATFORM_ADMIN entry is committed | RUNNING, with the signal handled |
| RUNNING (workflow) | TerminateWorkflowExecution with the decision log unavailable | The entry cannot be written | RUNNING, unchanged; the call is denied |

A refusal writes AC-DENY and changes no workflow state.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM | Requests break-glass in the bank IAM; decodes a payload under an ACTIVE grant; reads the access log (Platform administration, R) |
| RW-PLATADM | Terminates, resets and signals a workflow (Platform administration, U); reads the entries; receives the reconciliation incident |
| RW-AUDIT | Reads the AC-READ, AC-DENY and PLATFORM_ADMIN entries; holds no decode right (Platform administration and Decision log, R) |
| RW-TRIBE | Maintains the authorizer plugin configuration and the key rotation run book; may not decode |
| RW-CASEOWN and the other case roles | No decode right and no administrative call on a workflow |
| SY-CASEWF | Runs the codec server and the audit writer; connects to the frontend with its certificate (Decision log C) |
| SY-RULES | No part in this story; a call to the audit endpoint with its certificate is refused |
| No delegation of authority level applies | A decode or an administrative call is not a credit decision |

Separation of duty: the security administrator who decodes is not the author of the case decision the payload supports, and no person reviews their own break-glass use (RWB-E1-039).

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per decode, refusal and administrative call) |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for an access event, as RWB-E1-039 sets it, with the workflow ID in the actions field |
| DF-DEC-003 | decision_log_entry | decision_code | Write, read |
| DF-DEC-014 | decision_log_entry | actions | Write (operation, workflow ID, run ID, payload count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Write, read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |

No field is added. The PLATFORM_ADMIN value is a LOV-DECISION data row loaded through RWB-E1-043 and recorded in the additions file. No payload, no history event and no clear personal data field is written to the decision log. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**No Workbench API endpoint is added.** The codec server and the authorizer audit writer are internal Temporal services; they are not part of the Workbench API Specification v4.

**Codec server: POST /decode and POST /encode (Temporal codec server protocol)**

| Item | Value |
|---|---|
| Service | The codec server of the recovery module, called by the Temporal Web UI over mTLS at its own service URL |
| Request | namespace, workflowId, runId, requestId, payloads: an array of { metadata: { encoding, keyVersion }, data: base64 } |
| Response 200 | payloads: an array of { metadata, data: base64 } in the same order, and entryId |
| Errors | 401 no session; 403 role, grant or area (MSG-P4-002); 413 more than 100 payloads or 1 MB; 422 a payload without codec metadata or a key version that is not enabled; 503 Key Vault unavailable or the entry could not be written (no payload returned) |
| Authorization | Platform administration, right R, plus an ACTIVE break-glass grant for area PLATFORM_ADMINISTRATION |
| Idempotency | requestId from the Web UI; a repeat with the same requestId returns the same payloads and entryId and writes no second entry |

**Authorizer audit: TemporalAdminAuditWriter (internal mTLS call, no HTTP path)**

| Item | Value |
|---|---|
| Caller | The Temporal frontend authorizer plugin, configured in deploy/temporal/plugins/ |
| Request | operation (TERMINATE, RESET or SIGNAL), namespace, workflowId, runId, actorRef, grantId (nullable), reason, requestId |
| Response | entryId, read as 201 by the plugin |
| Failure | Any non-201 response denies the call with PERMISSION_DENIED; the workflow is unchanged |
| Authorization | mTLS client certificate of the Temporal frontend and the network policy of the frontend pods only |
| Idempotency | requestId from the frontend request; one entry per operation on one run |

**Temporal frontend** (gRPC over mTLS, port 7233): TerminateWorkflowExecution, ResetWorkflowExecution and SignalWorkflowExecution pass through the authorizer plugin, which calls TemporalAdminAuditWriter before allowing the call. A decode is not a Temporal API call; it is the codec server path above.

**GET /api/recovery/v1/admin/access-log** (existing, RWB-E1-039): reads the entries with event codes AC-READ, AC-DENY and PLATFORM_ADMIN. Authorization and errors are unchanged.

**Published interfaces called**

```java
// P7 decision log
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException;
```

The active grant is read through the published break-glass interface of RWB-E1-039; this story adds no method to it.

## 13. Solution plan

**Package.** The codec server, the grant check, the audit writer and the reconciliation in `recovery/accessadmin/temporal` (Java package `recovery.accessadmin.temporal`); the authorizer plugin configuration in `deploy/temporal/plugins/`; the key rotation run book in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CodecServerController | Controller | POST /decode on the codec server with the access check and the response after the entry (BR2, BR3) |
| BreakGlassGrantChecker | Service | Reads the ACTIVE grant and checks role, area and right (BR1) |
| PayloadGuard | Service | Payload count and size limits; codec metadata and key version check (BR8) |
| CodecKeyResolver | Service | Resolves the key version from the metadata and unwraps it in Key Vault (BR7) |
| TemporalAdminAuditWriter | Service | Builds and writes the AC-READ, AC-DENY and PLATFORM_ADMIN entries through DecisionLogApi (BR5, BR6) |
| TemporalAuthorizerPlugin | Configuration | The Temporal frontend Authorizer and ClaimMapper: calls TemporalAdminAuditWriter and denies on any non-201 response (BR4) |
| TemporalAdminAuditReceiver | Service | Receives the authorizer audit record over mTLS and writes it through TemporalAdminAuditWriter (BR4) |
| TemporalAdminAuditListener | Job | Daily reconciliation of the frontend audit log against decision_log_entry (BR9) |
| KeyRotationRunBook | Document | The rotation steps, the version list and the version retention rule (BR7) |

**Database.** No migration. The entries go to decision_log_entry through the existing writer in the caller's transaction. LOV-DECISION gains PLATFORM_ADMIN as a data row through RWB-E1-043; no table and no column is added.

**Configuration and reference data**

- Codec endpoint URL per environment in the Web UI; the codec server is reachable only from the Web UI ingress and the internal network.
- Limits: 100 payloads and 1 MB per request; the reconciliation runs daily at 02:00.
- Key versions: every version named by a history inside the retention (30 days, assumed) or the archive of RWB-E2-039 stays enabled.
- Feature flag rwb.p3.temporal through RWB-E1-047.
- No business parameter and no reference table beyond the LOV value in this story.

**Build steps**

1. Add the PLATFORM_ADMIN LOV value through the versioned reference load and confirm the decision log writer accepts it as a system event.
2. Build PayloadGuard and CodecKeyResolver with the version from the metadata; test AC4 with versions 1 and 2 and a rotation to 3.
3. Build BreakGlassGrantChecker and the codec endpoint with the write-before-return order; tests AC1, AC3 and AC5.
4. Build TemporalAdminAuditWriter and its mTLS receiver; test AC2 for the four operations.
5. Configure the authorizer plugin to call the writer and deny on 503; test AC6 with the decision log stopped.
6. Build TemporalAdminAuditListener and its incident; test AC7 with a planted frontend audit entry.
7. Run the two access tests, the key rotation drill in SIT, and record the version list in the release evidence.

**Feature flag.** `rwb.p3.temporal`. Off: the codec endpoint returns 404, the authorizer plugin is not configured and the reconciliation does not run; the cluster and the Web UI are unchanged.

**Done when.** The tests in section 16 pass, the rotation drill decodes a history written under an earlier key version, the reconciliation finds no gap over seven days, and the access log shows every decode with its grant and incident.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role is not RW-SECADM, the grant is missing, ended or for another area, or the caller is not SY-CASEWF on the internal endpoint | You cannot {action} here. Your role does not include it. |

A 401 returns the standard no-session text. A 422 names the payload index and the missing codec metadata, but never the payload. A 503 says the action was not taken because the decision could not be recorded. Neither case adds a message ID. MSG-P4-002 exists and is reused unchanged, with {action} set to "decode this workflow payload" or "record this workflow action".

## 15. Screens and states

No new Workbench screen. The decode result appears in the payload panel of the Temporal Web UI, which shows the states encoded, decoding and decoded for a user with a grant, and refused with MSG-P4-002 for every other user. The entries appear on the access log read of RWB-E1-039 and on SCR-38 Decision log query (RWB-E2-005) with the operation in the actions field. SCR-43 Roles and access in Epic 8 shows the grant rule; this story adds no panel to it.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-038-01 | AC1, BR1, BR3 | System | U-88 RW-SECADM, grant BG-2026-0042 ending 12:00; decode at 11:40 and 12:05 |
| TC-E2-038-02 | AC2, BR4, BR5, BR6 | System | One decode, one terminate, one reset and one signal |
| TC-E2-038-03 | AC3, BR1, BR10 | Access | RW-AUDIT and RW-CASEOWN call the decode endpoint; refused with MSG-P4-002 |
| TC-E2-038-04 | AC4, BR7 | System | Histories under key versions 1 and 2; rotation to version 3 |
| TC-E2-038-05 | AC5, BR8 | System | Payload without codec metadata |
| TC-E2-038-06 | AC6, BR4 | System | Decision log stopped; terminate attempted on case-RW-2026-000306 |
| TC-E2-038-07 | AC7, BR9 | Operational | Planted frontend audit entry; reconciliation at 02:00 |
| TC-E2-038-08 | Operational | Operational | Key rotation drill in SIT: rotate to version 3, decode a version 1 history |
| TC-E2-038-09 | Access | Access | SY-RULES calls the codec server /decode with its own certificate; refused with MSG-P4-002 and no entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the payload limits, the reconciliation time, the key version list and the refusal texts are configuration.
- No personal data in logs, tests, workflow history or prompts: the test payloads are synthetic, and no payload or clear field is written to the decision log or a log line.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- Decode is never a standing right: no grant, no clear payload, and every decode names its grant and incident.
- No entry, no action: a terminate, reset or signal the authorizer cannot record is denied, not retried after the fact.
- The codec never guesses a key version and never falls back to a clear read.
- No key version is disabled while a history inside the retention or the archive names it.
- The reconciliation never writes a missing entry: it reports the gap and leaves the record to the security administrator.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision, with the seven field groups | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-01, TC-E2-038-02, TC-E2-038-05, TC-E2-038-07 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.4; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-038-02, TC-E2-038-06 |

## 19. Out of scope

- The Temporal cluster, mTLS, Web UI sign-in and platform roles (RWB-E1-070).
- The codec itself, the worker and the smoke workflow (RWB-E1-071).
- The break-glass request, approval, review and access log writer (RWB-E1-039).
- Alerts, the stuck scanner and the workflow dashboard (RWB-E2-037).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The replay gate and build ID rollout (RWB-E2-040).
- A Workbench screen for workflow payloads or for the admin audit (Epic 8, SCR-43 Roles and access).
- Key Vault provisioning, key escrow and the bank key management standard (SCB IT platform).
