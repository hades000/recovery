# RWB-ITG-E1039-ITG Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1039-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P7-E1008-APP, RWB-P4-E1039-APP, RWB-P5-E1039-APP, RWB-P7-E1039-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-039 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-039 access-log and break-glass behaviour across P4 rwb-access (the grant and the access log), P3 rwb-case (the case read and the task action), P5 rwb-document (the document read), P7 rwb-decision (the central ledger and the audit query) and the P7 rwb-decision log store story**, so that **access and emergency access are proved on the real services before wave 1 exits**.

### 2. Business rationale

The legacy story writes one append-only, hash-chained decision log entry inside the caller's transaction for every sign-in, refusal, read or export, and holds the break-glass grant on the session. In the 19-service target that single write is replaced by the decoupling pattern DP-03: each owning service writes a local decision record in its own schema in the same transaction as the change, and publishes `DecisionRecorded` to the shared topic `rwb.decision-record.v1`; P7 rwb-decision collects the records idempotently into the central ledger with a completeness target of five minutes, gap alerts and daily chain verification (DP-03, Arch v5 slide 28). Auditors keep one place to search every decision, and no service takes a synchronous dependency on the ledger for an ordinary read. Only the points of no return wait for the ledger acknowledgement, and none of them is in this story.

The target split for the legacy key is therefore: P4 rwb-access owns the break-glass grant, the grant end it shows on the session, the access log query and the masking policy; P3 rwb-case owns the case read, the task action and the local decision record written for each; P5 rwb-document owns the document content read and its local decision record; P7 rwb-decision owns the central ledger, the consumer of `rwb.decision-record.v1` and the audit query over it, and its own log store is the product of the legacy RWB-E1-008 work. This story is the integration proof across those four owners and the log store.

No service contract is faked. The suite exercises the published wave 1 contracts of the four services through gateway-bff and reads the bank IAM only as an outside system. Where the sources do not name the cross-service split of the grant and ledger operations, the exact fault point for the fail-closed case or the location of the SIT evidence, the suite asserts through the owners' contracts and records the open point as Not specified in the source documents (GAP-0359; ASM-0466).

The measure is unchanged from the legacy story: reads of the case store and the document store written to the access log, target 100 percent (NFR-042). The story meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11. It ends standing administrator access, because a platform administrator holds only the letters of RW-PLATADM except while an approved grant is active.

### 3. Preconditions

- RWB-P7-E1008-APP is done: the P7 rwb-decision decision log store is append only and hash chained, and it receives the central ledger records.
- RWB-P4-E1039-APP is done: the break-glass grant, the grant check, the access event writer and the access log query are in SIT on P4 rwb-access.
- RWB-P5-E1039-APP is done: the document content read writes its local decision record before the file is returned.
- RWB-P7-E1039-APP is done: the audit query over the central ledger, the ledger completeness alert and the chain check are in SIT.
- The published contracts of P3 rwb-case, P4 rwb-access, P5 rwb-document and P7 rwb-decision are deployed under their own per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases, users and documents.
- The SIT decision log store is available.
- The break-glass group RWB-SIT-BREAKGLASS exists in SIT (name per DL40, assumed).
- The four parameters rwb.access.breakglass.window-hours, rwb.access.breakglass.incident-pattern, rwb.access.breakglass.reason-min and rwb.access.breakglass.review-days are loaded, read as data rows through the parameters contract of P3 rwb-case.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, users and documents of the harness RWB-ITG-W1J01-ITG and the RWB-SIT-BREAKGLASS membership of the platform administrator; no production data is used.
2. Harness: opens case RW-2026-000123 through gateway-bff with GET /api/recovery/case/v1/cases/{caseId} as U-4101 holding RW-CASEOWN at 10:15 on 3 December 2026.
3. Harness: reads the local decision record of P3 rwb-case and asserts the entry through GET /api/recovery/decision/v1/decision-log is present within five minutes.
4. Harness: activates the grant with POST /api/recovery/access/v1/admin/break-glass-grants at 10:30, with incident INC0004521, IAM request IAM-778812, area CASE_RECORD, right U, scope ALL and a reason of 46 characters, and asserts the banner MSG-P4-004 with time 14:30 read through GET /api/recovery/access/v1/me/session.
5. Harness: allows PATCH /api/recovery/case/v1/tasks/{taskId} at 14:20 and asserts the action carries the grant and the incident; refuses the same call at 14:31 with MSG-P4-002.
6. Harness: reads the document DOC-2026-0009981 of case RW-2026-000123 through GET /api/recovery/document/v1/documents/{documentId}/content under the grant and asserts one entry written before the file is returned.
7. Harness: runs the access audit query through GET /api/recovery/decision/v1/decision-log with caseId, decision AC-READ, from 2026-12-03 and to 2026-12-03 and asserts three entries in time order.
8. Harness: reads the access events of the day through GET /api/recovery/access/v1/admin/access-log and compares them with the ledger entries of the same case and time window.
9. Harness: posts the negative cases — no grant, missing incident, a reason of 12 characters, a repeated key and a local decision record failure — and records every status, message and entry.
10. Harness: writes the evidence report, removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The access log entry cannot be written | The read returns no data; status 503; an incident is raised to the platform administrator queue | MSG-P7-003 | AC5 |
| X2 | Break-glass is activated with no IAM grant for the caller | Refused with 403; the refusal is written as an AC-DENY entry with reason NO_BREAKGLASS_GRANT | MSG-P4-007 | AC4 |
| X3 | Break-glass is activated with no incident reference, a reference that fails the pattern, or a reason under the minimum | Refused with 422 naming the field; no grant is opened | MSG-GEN-001, MSG-GEN-002 | AC2 |
| X4 | An action is attempted after the grant has ended | The grant is ignored; the role's own letters apply; a refusal is written | MSG-P4-002 | AC2 |
| X5 | A second activation is sent while a grant is active | With the same Idempotency-Key the first response returns and no entry is written; with a new key the call returns 409 | MSG-GEN-004 | AC7 |
| X6 | A role without Platform administration R calls the access log or another admin endpoint | Refused with 403; an AC-DENY entry is written | MSG-P4-002 | AC6 |
| X7 | The central ledger lags the local record beyond five minutes | The read is never blocked; the lag is reported against the five-minute target and the ledger completeness alert is raised | None | AC1, AC5 |
| X8 | A consumed call exceeds the 2 s timeout or returns a server error | The GET is retried once under the suite policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC6 |
| X9 | The fixture set does not match the harness RWB-ITG-W1J01-ITG expectations, or the clock control cannot move the time | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the four APP stories and the published contracts of P3, P4, P5 and P7, not their source code |
| Negotiable | The window, the incident pattern, the reason length, the review window, the fixture sizes and the exact fault-switch mechanism are data rows or properties of the harness; the story fixes the assertions and the call set |
| Valuable | Every access and every emergency access is proved on real services, and the ledger completeness of five minutes is measured rather than assumed, before wave 1 exits |
| Estimable | One suite module, one fixture pack, one grant clock control, one ledger completeness assertion and one evidence report |
| Small | Eight scenarios over four services and one shared topic; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an entry, a status or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-access, rwb-case, rwb-document and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given the decision log store is available
    Given the RWB-ITG-W1J01-ITG synthetic cases, users and documents are loaded and no production data is used

  Scenario: AC1 The case read is recorded in the owning service and reaches the central ledger within five minutes (new, D-RCV-60)
    Given test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 through gateway-bff
    When the case record view loads
    Then P3 rwb-case writes one local decision record with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15
    Then its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked"
    Then the entry is visible through GET /api/recovery/decision/v1/decision-log within five minutes

  Scenario: AC2 The break-glass grant is honoured on a case action and marked until it ends (new, D-RCV-60)
    Given incident "INC0004521" is open
    Given the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00
    When "U-4102" calls POST /api/recovery/access/v1/admin/break-glass-grants at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters
    Then the grant is active until 14:30, the earlier of 4 hours and the group end
    Then the banner shows MSG-P4-004 with time "14:30"
    Then every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521"
    Then the system allows at 14:20 PATCH /api/recovery/case/v1/tasks/{taskId} on case "RW-2026-000123" by "U-4102" and marked with the grant
    Then the system refuses at 14:31 the same call with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone

  Scenario: AC3 The grant is honoured on a document read and ends there too (new, D-RCV-60)
    Given test user "U-4101" holding RW-CASEOWN opens document "DOC-2026-0009981" on case "RW-2026-000123"
    Given "U-4102" holds an active break-glass grant for incident "INC0004521" until 14:30
    When GET /api/recovery/document/v1/documents/{documentId}/content returns the file
    Then one entry with decision code "AC-READ", the case ID and the document ID is written before the file is returned
    Then the entry is marked with the grant and with incident "INC0004521"
    Then after 14:31 the same call is refused with MSG-P4-002

  Scenario: AC4 Break-glass without an IAM grant is refused and recorded (new, D-RCV-60)
    Given test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /api/recovery/access/v1/admin/break-glass-grants with incident "INC0004521"
    Then the system refuses the call with status 403 and message MSG-P4-007
    Then one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written

  Scenario: AC5 A read that cannot be recorded returns nothing (new, D-RCV-60)
    Given the local decision record write of P3 rwb-case is switched to fail by the agreed test-only fault switch
    When test user "U-4101" opens case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no case data
    Then the system raises an incident to the platform administrator queue
    Then a central ledger lag is reported against the five-minute target and never blocks a read

  Scenario: AC6 The access audit query returns every service's entries in time order (new, D-RCV-60)
    Given case "RW-2026-000123" was read by "U-4101" at 10:15, by "U-4102" at 11:02 under break-glass, and by "U-4101" at 16:40 on 3 December 2026
    When test user "U-4105" holding RW-AUDIT calls GET /api/recovery/decision/v1/decision-log with that case ID, decision "AC-READ", from "2026-12-03" and to "2026-12-03"
    Then three entries return in time order with actor, time and fields shown
    Then the 11:02 entry carries incident "INC0004521"

  Scenario: AC7 A repeated activation opens no second grant (new, D-RCV-60)
    Given "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001"
    When the user sends the same request again with key "k-001" at 10:31
    Then the first response returns and no entry is written
    Then when the user sends a request with key "k-002" at 10:32
    Then the call returns status 409 with message MSG-GEN-004

  Scenario: AC8 No copy is written to a data lake (new, D-RCV-60)
    Given an access event has been written to the local decision record and collected into the central ledger of P7 rwb-decision
    When the suite inspects the call set of the run
    Then the central ledger is the only copy of the access event
    Then no lake endpoint is called by any service
    Then the legacy E1-014 copy path is absent (DP-17)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every sign-in, refusal, read of the case store or the document store, and export writes one access event to the decision log; in the target the record is local to the owning service and reaches the central ledger within five minutes | RWB-E1-039 BR1; REQ-ACA-006; NFR-042; DP-03 |
| BR2 | A read or export whose access event cannot be written returns no data; the fail-closed point is the local record write of the owning service | RWB-E1-039 BR2; Principle 5; ASM-0467 |
| BR3 | An access event lists field IDs and their masking position, never field values | RWB-E1-039 BR3; NFR-040 |
| BR4 | Break-glass needs a grant approved by the security administrator in the bank IAM, an open incident reference and a reason of at least the minimum length; the activation is served by P4 rwb-access | RWB-E1-039 BR4; REQ-ACA-008 |
| BR5 | A grant ends at the earlier of the window (4 hours, assumed) and the IAM group end, with no action by anyone, and the end is enforced on every request | RWB-E1-039 BR5; rwb.access.breakglass.window-hours; DL38 |
| BR6 | Every action under break-glass is marked with the grant and the incident reference, in the local record and in the ledger entry | RWB-E1-039 BR6 |
| BR7 | The security administrator reviews each use inside the review window (one working day, assumed); an unreviewed use goes to the role that heads SCB IT security and to Compliance | RWB-E1-039 BR7; DL38 |
| BR8 | A platform administrator holds only the letters of RW-PLATADM in the matrix version in force; any right beyond them comes only from an active break-glass grant | RWB-E1-039 BR8 |
| BR9 | A person may not review their own break-glass use | RWB-E1-039 BR9 |
| BR10 | Each owning service writes its own decision record in its own schema in the same transaction as the change and publishes `DecisionRecorded` to `rwb.decision-record.v1`; P7 rwb-decision owns the central ledger and collects the records within five minutes; no service writes another service's ledger table | DP-03; ADR-022; Arch v5 slide 28 |
| BR11 | Every cross-service call in the suite is one hop with a 2 s timeout | ADR-020; DP-11 |

### 9. State transitions

None for the case status. This story does not change a case status. It observes the break-glass grant moving from Active to Ended at its end time, and the decision record moving from Local to collected centrally within five minutes.

| Object | State | Meaning |
|---|---|---|
| Break-glass grant | Active | The grant adds its right in its area and scope to the access check until the end time read through GET /api/recovery/access/v1/me/session; every entry carries the grant and the incident |
| Break-glass grant | Ended | The end time has passed; the grant is ignored with no action by anyone and an action beyond the role's own letters is refused with MSG-P4-002 |
| Decision record | Local | The owning service holds the record in its own schema, chained to its previous record, written in the same transaction as the read or action |
| Decision record | Collected centrally within five minutes | P7 rwb-decision holds the record in the central ledger, visible through GET /api/recovery/decision/v1/decision-log inside the completeness target |

The suite reads these states through the owners' contracts; it changes none of them directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| RW-SECADM Security administrator | Approves break-glass in the bank IAM and reviews each use; reads the access log |
| RW-PLATADM Platform administrator | Requests break-glass in the bank IAM and activates an approved grant; holds only the role's own letters when no grant is active |
| RW-AUDIT Internal audit | Queries access to a case through the decision log; changes nothing |
| RW-COMPLY Compliance and PDPA officer | Reads the access log; receives an unreviewed use |
| RW-COE, RW-DATASTEW | Read the access log |
| Every bank role | Generates access events by signing in, reading and exporting |
| SY-DECLOG Decision log writer | Writes the local decision record and the central ledger entry |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (central ledger in P7 rwb-decision; local decision record in P3, P4 and P5) | all fields | Write (one entry per access event) |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for sign-in, refusal, export and break-glass events |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-DEC-003 | decision_log_entry | decision_code | Read (query by access event code) |
| DF-DEC-014 | decision_log_entry | actions | Read (area, right, fields, filter, row count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-REF-035 | role (P4 rwb-access) | role_code | Read |
| SIT fault point and evidence location | Local decision record of the owning service; evidence report of the suite | Test-only fault switch and report location | Not specified in the source documents (GAP-0359; ASM-0466) |

The legacy story writes decision_log_entry in the monolith. In the target the entry is written locally by the owning service and collected into the central ledger of P7 rwb-decision; the suite asserts both through contracts and never reads a schema. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/access/v1/admin/break-glass-grants | P4 rwb-access | Activate the grant with the incident, the IAM request, area CASE_RECORD, right U and scope ALL |
| GET /api/recovery/access/v1/admin/access-log | P4 rwb-access | Read the access events and the break-glass entries by user and date |
| GET /api/recovery/access/v1/me/session | P4 rwb-access | Read the grant end time shown in the banner |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Open the case record that produces the AC-READ entry |
| PATCH /api/recovery/case/v1/tasks/{taskId} | P3 rwb-case | The action allowed at 14:20 and refused at 14:31 |
| GET /api/recovery/document/v1/documents/{documentId}/content | P5 rwb-document | The document read under the grant |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | The audit query and the ledger confirmation |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | every service, with the ledger owned by P7 rwb-decision | The suite waits for the ledger entry of the owning service before it asserts the read |

The suite consumes no other event, and it produces none.

#### 12.5 Workflows and activities

None. No workflow, activity or Nexus operation is started or awaited by this story; the reads and the actions are synchronous REST calls.

#### 12.6 Schedules

None. No Schedule is started, moved or waited for. The clock control moves the request time only.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01).

#### 12.8 Contract fakes

The bank IAM break-glass group membership is an outside system, read through the P4 session and grant responses; it is not a service contract. No service contract is faked: every call in section 12.2 goes to the real SIT service. The AC5 fault point is a test-only switch on the owning service's decision-record library, agreed with the service owner, and it is the only intervention in a running service.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 7 |
| Kafka | 0 | 1 |
| Temporal | 0 | 0 |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eight scenarios against SIT and holds no service code |
| Fixture pack | Test data | Synthetic cases, users, documents and the RWB-SIT-BREAKGLASS membership of the platform administrator |
| Grant clock control | Harness control | Sets the grant start at 10:30 and moves the request time to 14:20, 14:31 and 18:00, then restores it |
| Ledger completeness assertion | Assertion | Polls GET /api/recovery/decision/v1/decision-log until the entry of the owning service appears and measures the elapsed time against the five-minute target |
| Evidence report | Report | Records per scenario the grant id, the entry ids of each service, the statuses, the messages and the elapsed ledger time |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | Each of P3, P4, P5 and P7 writes its own schema; the suite asserts through contracts only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | On RWB-P4-E1039-APP, RWB-P5-E1039-APP and RWB-P7-E1039-APP; not a build dependency of this suite, which only waits for the ledger entry |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On RWB-P4-E1039-APP for the four rwb.access.breakglass.* values; the suite reads the same rows as data |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories for the access event codes and the capability and scope lists; the suite sends the codes as data |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The seven consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none | The legacy E1-014 copy path is absent; AC8 asserts that the call set holds no lake endpoint |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; no screen is in scope, and the banner is read through the P4 session contract |

The dependency-added column records the build dependency of the owning story. The H, C, I and X lists of this story are exactly those of the metadata table: no H, no C, no X, and the four I dependencies RWB-P7-E1008-APP, RWB-P4-E1039-APP, RWB-P5-E1039-APP and RWB-P7-E1039-APP. An ITG story waits on no build of its own.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P3, P4, P5 and P7 through gateway-bff.
2. Build the fixture pack: synthetic cases, users, documents and the RWB-SIT-BREAKGLASS membership, with the four rwb.access.breakglass.* values read as data rows through the P3 parameters contract.
3. Add the grant clock control and the restore step.
4. Implement AC1 and AC6: the recorded case read, the ledger entry within five minutes and the audit query in time order.
5. Implement AC2, AC3 and AC7 with the clock at 10:30, 14:20, 14:31 and 18:00: the grant, the banner, the marked case action, the document read and the repeated activation.
6. Implement AC4 and the negative activation cases — no grant, missing incident and a reason of 12 characters — and assert the exact statuses and messages.
7. Implement AC5 through the agreed test-only fault switch on the owning service's decision-record library, and add the ledger lag report.
8. Prove AC8 over the call set of the run, write the evidence report and run the suite in SIT against the wave 1 release candidate.

Done when: all eight test cases pass in SIT against the published wave 1 contracts of P3, P4, P5 and P7, the ledger completeness report shows every entry collected inside the five-minute target, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-004 | Break-glass access is active | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-007 | Break-glass requested with no approved IAM grant | Emergency access needs an approved break-glass request in the bank IAM with an open incident. |
| MSG-P4-002 | An action after the grant has ended, or an access log query without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Incident reference empty | Enter {field}. |
| MSG-GEN-002 | Reason shorter than the minimum, or page size outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Query from date after to date | {field} cannot be before {other}. |
| MSG-GEN-004 | A second activation while a grant is active | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The ledger completeness check is reported as one line of the evidence report and carries no message ID: {collected} of {expected} access entries of case {caseId} were collected into the central ledger of rwb-decision, the slowest in {seconds} seconds against the five-minute target of 300 seconds.

The message IDs and wording are copied from RWB-E1-039. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The ACE front-end shell shows the MSG-P4-004 banner while a grant is active, and the suite reads the same end time through GET /api/recovery/access/v1/me/session. The access log is read through the P4 contract until SCR-43 Roles and access, and access to a case is read through the decision log query SCR-38 (RWB-E2-005). Neither screen is built or tested here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-01-ITG | AC1 | Integration | Synthetic case RW-2026-000123 with masked personal fields; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-02-ITG | AC2 | Integration | Incident INC0004521, IAM request IAM-778812, test clock 10:30 to 14:31; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-04-ITG | AC3 | Integration | Synthetic document DOC-2026-0009981 on the case; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-05-ITG | AC4 | Component | RW-PLATADM test user U-4104 outside the break-glass group; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-12-ITG | AC5 | NFR | The local decision record write forced to fail during a case read; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-08-ITG | AC6 | Integration | Three reads of one case on 3 December 2026; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-039-10-ITG | AC7 | Integration | Two keys k-001 and k-002 for one active grant; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1039-ITG-08 | AC8 | Integration | Central ledger as the only copy, no lake endpoint called, legacy E1-014 copy path absent; end-to-end: real services on the wave 1 contracts; no numeric business values added |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- No business value in code: the window, the incident pattern, the reason length and the review window are data rows read through the parameters contract.
- No personal data in logs, events, evidence or fixtures: field IDs and the masking position only, never values. The break-glass reason is free text written by the administrator and carries no customer data.
- No cross-service table read: every assertion goes through the owner's contract, and the suite owns no table.
- One hop and a 2 s timeout on every call (ADR-020).
- The grant end is enforced on every request and never by a job; the suite moves only its own clock.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | The local decision record of P3 and P5, the ledger entry through rwb.decision.DecisionRecorded.v1 and GET /api/recovery/decision/v1/decision-log | TC-E1-039-01-ITG, TC-E1-039-04-ITG, TC-E1-039-12-ITG, TC-E1-039-08-ITG, TC-ITG-E1039-ITG-08 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | POST /api/recovery/access/v1/admin/break-glass-grants, GET /api/recovery/access/v1/me/session, MSG-P4-004, MSG-P4-007, MSG-P4-002 | TC-E1-039-02-ITG, TC-E1-039-05-ITG, TC-E1-039-10-ITG |
| ADR-022 | Local decision record plus central ledger | The local record in P4, P5 and P7 in the caller transaction; the central ledger in P7 within five minutes | TC-E1-039-01-ITG, TC-E1-039-04-ITG, TC-E1-039-12-ITG, TC-ITG-E1039-ITG-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed REST operations of section 12.2 | TC-E1-039-01-ITG, TC-E1-039-02-ITG, TC-E1-039-08-ITG |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the suite asserts through contracts | All |
| ASM-0466 | The grant, the access log and the ledger query have target names on their owners | The four P4 operations, the P3 operations and the P7 decision-log query of section 12.2 | TC-E1-039-02-ITG, TC-E1-039-05-ITG, TC-E1-039-08-ITG |
| ASM-0467 | Fail closed on the local record only; ledger lag is reported | The fault switch of AC5 and the ledger completeness line of section 14 | TC-E1-039-12-ITG |

The legacy AC1 to AC10 at component level belong to RWB-P4-E1039-APP, RWB-P5-E1039-APP and RWB-P7-E1039-APP, not to this story.

### 19. Out of scope

- The P4, P5 and P7 APP builds and their unit and component tests, including the P7 log store of RWB-P7-E1008-APP.
- The CON, DB and OPS stories of the four services.
- The legacy AC1 to AC10 at component level, which the sibling APP stories own.
- The break-glass request, approval and review records, which are held in the bank IAM.
- The unreviewed-use alert (Epic 8, FEAT-ADM-12).
- SCR-38 Decision log query (RWB-E2-005) and SCR-43 Roles and access.
- The decision log copy to a data lake, which is removed (DP-17).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
