<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 039 Access log into the decision log and break glass admin v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 039 Access log into the decision log and break glass admin v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-039 Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-039 |
| Epic | E1, release 30 November 2026 |
| Module | P4 Access and administration, with P7 Decision center and log |
| Feature | FEAT-ACA-07 Write every access event to the access log; FEAT-ACA-08 Write the access log into the decision log; FEAT-ACA-09 Use break-glass access with an incident reference; FEAT-ACA-10 Review break-glass use; FEAT-ACA-16 Answer an access audit query |
| Requirement IDs | REQ-ACA-006, REQ-ACA-008 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
| L3 process | 16 Manage risk, control and compliance; 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-E1-022, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **security administrator (RW-SECADM)**, I want **every sign-in, refusal, read of a case record or document and export written to the decision log store, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked**, so that **every access can be audited from one log and emergency access is controlled and reviewed**.

## 2. Business rationale

The bank cannot answer today who read a debtor's record on a given date, and administrators have standing access to production data. This story writes each access event into the append-only, hash-chained decision log, so access and decisions are queried together, and replaces standing access with a break-glass grant that names an incident, ends on its own and marks every action. It meets REQ-ACA-006 and REQ-ACA-008 and supports controls CTL-09 and CTL-11. The measure is reads of the case store and the document store written to the access log: target 100 percent (NFR-042).

## 3. Preconditions

- RWB-E1-008 is done: the decision log store is append only and hash chained.
- RWB-E1-022 is done: sessions, AccessCheck and the AccessEventPublisher exist.
- RWB-E1-027 is done: the decision log writer validates and writes entries.
- LOV-DECISION holds the access event codes AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS (loaded by RW-DATASTEW with this story; recorded in the additions file).
- The Entra ID break-glass group for each environment exists, granted only through the bank IAM with an end time (name per DL40; RWB-SIT-BREAKGLASS assumed in SIT).
- Parameters in the catalog: rwb.access.breakglass.window-hours=4, rwb.access.breakglass.incident-pattern=^INC[0-9]{7}$, rwb.access.breakglass.reason-min=20, rwb.access.breakglass.review-days=1 (assumed values; DL38).
- The case store (P3) and the document hub (P5) call AccessEventPublisher on every read they serve.

## 4. Flow

1. Person: signs in, or reads a case record, a document or a list, or exports a list.
2. Owning module: calls AccessEventPublisher.publish with the event, the case ID where there is one, and the field IDs returned with their masking position, or the filter and row count for a list or export.
3. Workbench (AccessLogWriter): writes one decision log entry with an access event code, the actor, the area, the result and the details in actions, in the same transaction as the read response is built; if the write fails, the read returns nothing.
4. Platform administrator (RW-PLATADM): raises a break-glass request in the bank IAM naming the open incident, the capability area, the scope and the reason; the security administrator approves it there, and the IAM adds the administrator to the break-glass group until the window ends.
5. RW-PLATADM: calls POST /admin/break-glass with the incident reference, the IAM request ID, the area, the right, the scope and the reason.
6. Workbench (BreakGlassService): checks the break-glass group, the incident reference pattern and the reason length; writes an AC-BGON entry; sets the session grant to end at the earlier of the window end and the group end.
7. Workbench: marks every entry written while the grant is active with the grant ID and the incident reference; the ACE front end shows the MSG-P4-004 banner with the end time.
8. Workbench: after the end time, AccessCheck ignores the grant with no action by anyone.
9. Security administrator: reviews each use inside the review window from GET /admin/access-log with event AC-BGON and the entries marked with its incident, and records the review in the bank IAM.
10. Internal audit (RW-AUDIT): asks who read a case over a period through GET /decision-log with caseId, decision AC-READ, from and to.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The access log entry cannot be written | The read or export returns no data; status 503; an incident is raised | MSG-P7-003 | AC7 |
| X2 | Break-glass is requested by a person not in the break-glass group | Refused with 403; the refusal is logged | MSG-P4-007 | AC5 |
| X3 | Break-glass is requested with no incident reference, a reference that fails the pattern, or a reason under 20 characters | Refused with 422 naming the field | MSG-GEN-001, MSG-GEN-002 | AC6 |
| X4 | An action is attempted after the grant has ended | The grant is ignored; the role's own letters apply; a refusal is logged | MSG-P4-002 | AC2 |
| X5 | A second activation is sent while a grant is active | With the same Idempotency-Key the first response returns; with a new key the call returns 409 | MSG-GEN-004 | AC10 |
| X6 | A role without Platform administration R calls an admin endpoint, such as the access log or the roles list | Refused with 403; an AC-DENY entry is written | MSG-P4-002 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the store (RWB-E1-008), the session (RWB-E1-022) and the writer (RWB-E1-027) |
| Negotiable | The window, the incident pattern and the reason length are parameters (DL38) |
| Valuable | One log answers who saw what and when, and ends standing administrator access |
| Estimable | One writer adapter, one break-glass endpoint, query through existing endpoints |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Access log into the decision log and break-glass admin

  Background:
    Given the environment is SIT
    Given the decision log store is available

  Scenario: AC1 Read logged
    Given test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026
    When the case record view loads
    Then the system writes one decision log entry with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15
    Then its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked"

  Scenario: AC2 Break-glass granted
    Given incident "INC0004521" is open
    Given the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00
    When "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters
    Then the grant is active until 14:30, the earlier of 4 hours and the group end
    Then the banner shows MSG-P4-004 with time "14:30"
    Then every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521"
    Then the system allows at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" and marked with the grant
    Then the system refuses at 14:31 the same call with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone

  Scenario: AC3 Export logged
    Given test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows
    When the user exports the list
    Then the system writes one decision log entry with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID

  Scenario: AC4 Document read logged
    Given test user "U-4101" holding RW-CASEOWN opens document "DOC-2026-0009981" on case "RW-2026-000123"
    When GET /documents/{documentId}/content returns the file
    Then one entry with decision code "AC-READ", the case ID and the document ID is written before the file is returned

  Scenario: AC5 Break-glass without an IAM grant is refused
    Given test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with incident "INC0004521"
    Then the system refuses the call with status 403 and message MSG-P4-007
    Then one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written

  Scenario: AC6 Break-glass with a missing incident or a short reason is refused
    Given test user "U-4102" is in group "RWB-SIT-BREAKGLASS"
    When the user calls POST /admin/break-glass with no incident reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "incidentReference"
    Then when the user calls it with incident "INC0004521" and a reason of 12 characters
    Then the system refuses the call with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000

  Scenario: AC7 A read that cannot be logged returns nothing
    Given the decision log store is unavailable
    When test user "U-4101" opens case "RW-2026-000123"
    Then the call returns status 503 with message MSG-P7-003 and no case data
    Then the system raises an incident to the platform administrator queue

  Scenario: AC8 Access audit query
    Given case "RW-2026-000123" was read by "U-4101" at 10:15, by "U-4102" at 11:02 under break-glass, and by "U-4101" at 16:40 on 3 December 2026
    When test user "U-4105" holding RW-AUDIT calls GET /decision-log with that case ID, decision "AC-READ", from "2026-12-03" and to "2026-12-03"
    Then three entries return in time order with actor, time and fields shown
    Then the 11:02 entry carries incident "INC0004521"

  Scenario: AC9 Refusals are written to the decision log
    Given test user "U-4106" holds only RW-PHONECOL
    When the user calls GET /admin/roles
    Then the system refuses the call with MSG-P4-002
    Then one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written

  Scenario: AC10 A repeated activation does not open a second grant
    Given "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001"
    When the user sends the same request again with key "k-001" at 10:31
    Then the first response returns and no new entry is written
    Then when the user sends a request with key "k-002" at 10:32
    Then the call returns status 409 with message MSG-GEN-004
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every sign-in, refusal, read of the case store or the document store, and export writes one access event to the decision log | REQ-ACA-006; NFR-042; FEAT-ACA-08 |
| BR2 | A read or export whose access event cannot be written returns no data | Principle 5; R-UNI-39 |
| BR3 | An access event lists field IDs and their masking position, never field values | NFR-040; guardrail on personal data |
| BR4 | Break-glass needs a grant approved by the security administrator in the bank IAM, an open incident reference and a reason of at least 20 characters | Admin and access model, section 5.3; Access flow sheet, roles.txt; REQ-ACA-008 |
| BR5 | A grant ends at the earlier of the window (4 hours, assumed) and the IAM group end, with no action by anyone | rwb.access.breakglass.window-hours; DL38 |
| BR6 | Every action under break-glass is marked with the grant and the incident reference | Admin and access model, section 5.3 |
| BR7 | The security administrator reviews each use inside the review window (one working day, assumed); an unreviewed use goes to the head of SCB IT security and to Compliance | DL38; Access flow sheet, roles.txt |
| BR8 | A platform administrator holds only the letters of RW-PLATADM in the matrix version in force; any right beyond them comes only from an active break-glass grant | Admin and access model, section 3.2; permission matrix |
| BR9 | A person may not review their own break-glass use | Admin and access model, section 6.2 |

## 9. State transitions

None. This story does not change a case status. A break-glass grant moves from Active to Ended at its end time.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM Platform administrator | Requests break-glass in the bank IAM and activates an approved grant with POST /admin/break-glass (Platform administration C) |
| RW-SECADM Security administrator | Approves break-glass in the bank IAM and reviews each use; reads the access log (Platform administration R) |
| RW-COMPLY Compliance and PDPA officer | Reads the access log; receives unreviewed uses |
| RW-AUDIT Internal audit | Reads the access log and queries access to a case through the decision log; changes nothing |
| RW-COE, RW-DATASTEW | Read the access log (Platform administration R) |
| Every bank role | Generates access events by signing in, reading and exporting |
| SY-DECLOG Decision log writer | Writes the access events (Decision log C) |
| Head of SCB IT security | Receives a break-glass use not reviewed inside the window |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (one entry per access event) |
| DF-DEC-002 | decision_log_entry | case_id | Write; empty for sign-in, refusal, export and break-glass events (change recorded in the additions file) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, read |
| DF-DEC-003 | decision_log_entry | decision_code | Read (query by access event code) |
| DF-DEC-014 | decision_log_entry | actions | Read (area, right, fields, filter, row count, grant, incident) |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /admin/break-glass-grants** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | BreakGlassActivation: incidentReference, iamRequestId, capabilityArea (LOV-CAPABILITY), right (one of C, R, U), scope (LOV-SCOPE), reason (20 to 1000 characters) |
| Response | 201 BreakGlassGrant: grantId (the AC-BGON entry ID), incidentReference, capabilityArea, right, scope, startsAt, endsAt |
| Errors | 401 no session; 403 caller not RW-PLATADM or not in the break-glass group (MSG-P4-007); 409 a grant is already active (MSG-GEN-004); 422 field missing or invalid (MSG-GEN-001, MSG-GEN-002); 503 entry could not be written (MSG-P7-003) |
| Authorization | Platform administration, right C, plus membership of the break-glass group |
| Idempotency | Idempotency-Key header |

**GET /api/recovery/v1/admin/access-log** (API-P4-008)

| Item | Value |
|---|---|
| Request | Query: user, from, to, event (an access event code), page, size (1 to 500) |
| Response | AccessLogPage of AccessLogEntry: at (decided_at), user (actor), event (decision_code), capability (actions.area), result (final_call) |
| Errors | 401; 403 no Platform administration R (MSG-P4-002); 422 from after to (MSG-GEN-003) or size outside 1 to 500 (MSG-GEN-002); 503 (MSG-GEN-006) |
| Authorization | Platform administration, right R |
| Idempotency | Not applicable, read only |

**GET /api/recovery/v1/decision-log** (API-P7-006), used for "who read this case": Query caseId, decision "AC-READ", from, to, page, size; response DecisionLogPage; Decision log, right R, scope applied; errors 401, 403, 503.

**Published interface AccessEventPublisher** (package recovery.access.accesslog), extended from RWB-E1-022:

```java
void publish(AccessEvent event) throws DecisionLogUnavailableException;
// AccessEvent: eventCode (AC-SIGN|AC-DENY|AC-READ|AC-EXPT|AC-BGON), actorUserRef, caseId (nullable), area, right,
//   result, fieldIds with masked flag, filter, rowCount, documentId, reasonCode
```

## 13. Solution plan

- Package: folder `recovery/access/accesslog` in the recovery module; Java package `recovery.access.accesslog`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | POST /admin/break-glass and GET /admin/access-log |
| AccessLogWriter | Service | Turns an AccessEvent into a DecisionLogRecord and calls the P7 DecisionLogWriter in the caller's transaction |
| AccessEventPublisher | Published interface | Called by P3 and P5 on every read and export; now writes through AccessLogWriter as well as the ACE audit and SOC log |
| BreakGlassService | Service | Checks the group, the incident pattern and the reason; writes AC-BGON; holds the grant on the session |
| BreakGlassGrantCheck | Service | Adds the grant's right in its area and scope to AccessCheck until endsAt; marks entries with grant and incident |
| AccessLogQueryService | Service | Maps GET /admin/access-log to the P7 DecisionLogReader interface |
| BreakGlassBanner | React component | Shows MSG-P4-004 with the end time from GET /me/session |

- Database: no table of its own; writes decision_log_entry only through the P7 writer. Index ix_declog_actor_time on decision_log_entry (actor_user_id, decided_at) is created by RWB-E1-008.
- Configuration and reference data: access event codes in LOV-DECISION (RW-DATASTEW); break-glass parameters above (values DL38); break-glass group name (DL40).
- Build steps:
  1. Build AccessLogWriter and extend AccessEventPublisher; tests for AC1, AC3, AC9.
  2. Add the publish call to the P3 case read and list export and to the P5 document content read, through the published interface; tests for AC1, AC3, AC4.
  3. Make the read fail closed when the write fails; test for AC7.
  4. Build BreakGlassService and the endpoint with validation and idempotency; tests for AC5, AC6, AC10.
  5. Build BreakGlassGrantCheck with the end time from the session; test AC2 with a clock fixed at 10:30 and moved to 14:31.
  6. Build AccessLogQueryService and the access log endpoint; test for AC8 with the decision log query.
  7. Add the session breakGlass fields to GET /me/session and the BreakGlassBanner.
- Feature flag: `rwb.access.access-log`.
- Done when: the tests in section 16 pass and the break-glass test of the access test set (one request with an open incident, one without) passes in SIT and is signed by the security administrator.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-004 | Break-glass access is active | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-007 | Break-glass requested with no approved IAM grant (new) | Emergency access needs an approved break-glass request in the bank IAM with an open incident. |
| MSG-P4-002 | An action after the grant has ended, or an access log query without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | Incident reference empty | Enter {field}. |
| MSG-GEN-002 | Reason shorter than 20 characters, or page size outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Query from date after to date | {field} cannot be before {other}. |
| MSG-GEN-004 | A second activation while a grant is active | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows DL10; proposed Thai for MSG-P4-007 is in the additions file.

## 15. Screens and states

No screen in this story. The ACE front end shell shows the MSG-P4-004 banner while a grant is active. The access log is read through GET /admin/access-log until SCR-43 Roles and access in Epic 8, and access to a case through SCR-38 Decision log query from Epic 2 (RWB-E2-005).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-01 | AC1, BR1, BR3 | System | Synthetic case RW-2026-000123 with masked personal fields |
| TC-E1-039-02 | AC2, BR4, BR5, BR6, BR8 | System | Incident INC0004521, IAM request IAM-778812, test clock 10:30 to 14:31 |
| TC-E1-039-03 | AC3, BR1 | System | Case list filter returning 37 synthetic cases |
| TC-E1-039-04 | AC4, BR1 | System | Synthetic document on the case |
| TC-E1-039-05 | AC5, BR4 | System | RW-PLATADM test user outside the break-glass group |
| TC-E1-039-06 | AC6, BR4 | System | Missing incident reference; 12-character reason |
| TC-E1-039-07 | AC7, BR2 | System | Decision log store switched off in the test double |
| TC-E1-039-08 | AC8, BR6 | System | Three reads of one case on one day |
| TC-E1-039-09 | AC9, BR1 | System | RW-PHONECOL test user calling the admin API |
| TC-E1-039-10 | AC10 | System | Two keys for one active grant |
| TC-E1-039-11 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E1-039-12 | Principle 5 | Resilience | The decision log write forced to fail during a case read |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the window, the incident pattern, the reason length and the review window are parameters.
- No personal data in logs, tests or prompts. Access events carry field IDs and the masking position, never values; the reason text is free text written by the administrator and must not hold customer data.
- No read of another module's tables; the access log is read through the P7 published interface.
- No right beyond the letters of RW-PLATADM without an active grant.
- The grant end is enforced on every request, not by a job.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | Epic 1, 3.4 | FEAT-ACA-07, FEAT-ACA-08, FEAT-ACA-16 | 16 Manage risk, control and compliance | BR1, BR2, BR3 | TC-E1-039-01, TC-E1-039-03, TC-E1-039-04, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-12 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | Epic 1, 3.4 | FEAT-ACA-09, FEAT-ACA-10 | 16 Manage risk, control and compliance | BR4, BR5, BR6, BR7, BR8, BR9 | TC-E1-039-02, TC-E1-039-05, TC-E1-039-06, TC-E1-039-10 |

## 19. Out of scope

- Logging reads of the data lake copy (RWB-E1-016, data lake access by data product).
- The break-glass request, approval and review records, which are held in the bank IAM.
- A scheduled alert for an unreviewed break-glass use to the head of SCB IT security and Compliance (Epic 8, FEAT-ADM-12 Manage an incident).
- The Decision log query screen SCR-38 (RWB-E2-005) and the Roles and access screen SCR-43 (Epic 8).
