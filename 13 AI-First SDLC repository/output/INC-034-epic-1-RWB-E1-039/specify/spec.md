# Technical Specification — RWB-E1-039 Access log into the decision log and break-glass admin

| Field | Value |
|---|---|
| Story | RWB-E1-039 — Access log into the decision log and break-glass admin (P4/P7) |
| Epic / module | E1 / P4 Access and administration, with P7 Decision center and log |
| RUN_ID | `INC-034-epic-1-RWB-E1-039` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-013, FR-RWB-017); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 039 Access log into the decision log and break glass admin v1.md` |
| Upstream IDs | BRD-RWB-004, BRD-RWB-007; FR-RWB-013, FR-RWB-017; REQ-ACA-006, REQ-ACA-008; US-RWB-E1-039; FEAT-ACA-07..10, FEAT-ACA-16; CTL-09, CTL-11; NFR-042; R-UNI-39; DF-DEC-001..018, DF-DEC-030; DL38, DL40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — one shell component is added: `BreakGlassBanner`, which shows MSG-P4-004 with the end time while a grant is active. No business screen; the access log and decision log are read through APIs until SCR-43 and SCR-38. Design evidence is local: design system and label standard; no Figma and no shell prototype. |
| Logic In Scope | `YES` — access event writing, fail-closed reads, break-glass validation, grant end, marking, query. |
| API In Scope | `YES` — first delivery of `POST /api/recovery/v1/admin/break-glass-grants` (API-P4-013) and `GET /api/recovery/v1/admin/access-log` (API-P4-008); reuses `GET /api/recovery/v1/decision-log` (API-P7-006). |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | P3 case read, list and export; P5 document content read; P7 decision log writer and reader; session and `AccessCheck` (RWB-E1-022); ACE shell. |
| New Nodes Required | `YES` — `AccessLogWriter`, `BreakGlassService`, `BreakGlassGrantCheck`, `AccessLogQueryService`, `BreakGlassBanner`; `AccessEventPublisher` extended. |
| Inherited Existing Behavior | Append-only hash-chained decision log store (RWB-E1-008); session, access check and publisher (RWB-E1-022); decision log writer (RWB-E1-027); masking and leaver revalidation (RWB-E1-037); P3 and P5 read paths. |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every sign-in, refusal, read of the case store or document store, and export writes one access event to the decision log. | SPEC-RWB-E1-039-001..004 | DIRECT | `AccessLogWriter` from the caller's transaction. | COVERED |
| BR2 | A read or export whose access event cannot be written returns no data. | SPEC-RWB-E1-039-005 | DIRECT | Write before response; rollback and 503. | COVERED |
| BR3 | An access event lists field IDs and masking position, never field values. | SPEC-RWB-E1-039-006 | DIRECT | `actions.fieldIds[]` with `masked`. | COVERED |
| BR4 | Break-glass needs an IAM grant, an open incident reference and a reason of at least 20 characters. | SPEC-RWB-E1-039-007 | DIRECT | Group check; pattern; length; LOVs. | COVERED |
| BR5 | A grant ends at the earlier of the window (4 hours) and the IAM group end, with no action. | SPEC-RWB-E1-039-008 | DIRECT | `endsAt = min(now + window, groupEnd)`. | COVERED |
| BR6 | Every action under break-glass is marked with the grant and the incident reference. | SPEC-RWB-E1-039-009 | DIRECT | `actions.grantId` and `actions.incidentReference`. | COVERED |
| BR7 | The security administrator reviews each use inside the review window; an unreviewed use goes to the head of SCB IT security and Compliance. | SPEC-RWB-E1-039-018 | EXTERNAL | Review is a bank IAM control; the Workbench supplies the AC-BGON query and evidence. The alert is Epic 8 FEAT-ADM-12. | COVERED |
| BR8 | A platform administrator holds only the RW-PLATADM letters; any right beyond them comes only from an active grant. | SPEC-RWB-E1-039-015 | DIRECT | `BreakGlassGrantCheck` adds the grant right; no standing right. | COVERED |
| BR9 | A person may not review their own break-glass use. | SPEC-RWB-E1-039-018 | EXTERNAL | Enforced in the bank IAM; the Workbench records actor and review evidence, not the reviewer. | COVERED |
| AC1 | Opening a case writes AC-READ with actor, case ID, time and field IDs marked masked. | SPEC-RWB-E1-039-001, SPEC-RWB-E1-039-006 | DIRECT | P3 read path. | COVERED |
| AC2 | Break-glass activation at 10:30 with a 4-hour window and group end 18:00 ends at 14:30; banner; entries marked; 14:20 allowed; 14:31 refused. | SPEC-RWB-E1-039-007..011 | DIRECT | Clock fixed in the test. | COVERED |
| AC3 | Export of 37 filtered cases writes AC-EXPT with filter and row count, no case ID. | SPEC-RWB-E1-039-003 | DIRECT | Export path. | COVERED |
| AC4 | Opening a document writes AC-READ with case and document IDs before the file is returned. | SPEC-RWB-E1-039-002 | DIRECT | P5 read path. | COVERED |
| AC5 | Break-glass without the group is 403 MSG-P4-007 and AC-DENY `NO_BREAKGLASS_GRANT`. | SPEC-RWB-E1-039-007 | DIRECT | Group check first. | COVERED |
| AC6 | Missing incident is 422 MSG-GEN-001; 12-character reason is 422 MSG-GEN-002 with min 20 max 1000. | SPEC-RWB-E1-039-007, SPEC-RWB-E1-039-016 | DIRECT | Field-level validation. | COVERED |
| AC7 | Log store unavailable: case read returns 503 MSG-P7-003, no data, incident raised. | SPEC-RWB-E1-039-005 | DIRECT | Fail closed. | COVERED |
| AC8 | Three reads of one case on one day return in time order; the 11:02 entry carries the incident. | SPEC-RWB-E1-039-013 | DIRECT | `GET /decision-log` with caseId and AC-READ. | COVERED |
| AC9 | RW-PHONECOL calling `GET /admin/roles` is refused and writes AC-DENY with area, right and no case ID. | SPEC-RWB-E1-039-004 | DIRECT | Refusal path from RWB-E1-022. | COVERED |
| AC10 | Same Idempotency-Key returns the first response; a new key while active returns 409. | SPEC-RWB-E1-039-014 | DIRECT | Key store on the grant. | COVERED |
| X1 | The access log entry cannot be written. | SPEC-RWB-E1-039-005 | DIRECT | 503; no data; incident. | COVERED |
| X2 | Break-glass requested without the group. | SPEC-RWB-E1-039-007 | DIRECT | 403 MSG-P4-007; AC-DENY. | COVERED |
| X3 | No incident, bad pattern, or reason under 20 characters. | SPEC-RWB-E1-039-007, SPEC-RWB-E1-039-016 | DIRECT | 422 field-level. | COVERED |
| X4 | An action after the grant ended. | SPEC-RWB-E1-039-011 | DIRECT | Grant ignored; own letters; refusal logged. | COVERED |
| X5 | A second activation while a grant is active. | SPEC-RWB-E1-039-014 | DIRECT | Same key returns; new key 409. | COVERED |
| X6 | A role without Platform administration R calls an admin endpoint. | SPEC-RWB-E1-039-004 | DIRECT | 403; AC-DENY. | COVERED |

## User story intent interpretation

As a **security administrator (RW-SECADM)**, I want **every sign-in, refusal, read of a case record or document and export written to the decision log store, and emergency access taken only under a break-glass grant approved in the bank IAM against an open incident, for a limited time, with every action marked**, so that **every access can be audited from one log and emergency access is controlled and reviewed**.

The story connects access events to the same append-only log as decisions and replaces standing administrator access with a time-boxed grant. It adds the break-glass banner to the shell, not a business screen. The access log and decision log are read through APIs until the Epic 8 and Epic 2 screens arrive.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Every sign-in, refusal, case read, document read and export; `POST /admin/break-glass-grants`; `GET /admin/access-log`; `GET /decision-log`. |
| Preconditions | RWB-E1-008 store is append-only and hash-chained; RWB-E1-022 session and publisher exist; RWB-E1-027 writer exists; LOV-DECISION holds AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS; the break-glass group exists (DL40); parameters `rwb.access.breakglass.window-hours=4`, `incident-pattern=^INC[0-9]{7}$`, `reason-min=20`, `review-days=1` (assumed DL38); P3 and P5 call the publisher. |
| Input | Access event from P3/P5; break-glass activation (incident, IAM request, area, right, scope, reason); access log query; decision log query. |
| Output | `decision_log_entry` rows; `BreakGlassGrant`; session `breakGlass` state; `AccessLogPage`; `DecisionLogPage`; AC-BGON, AC-DENY and AC-READ entries. |
| Feature flag | `rwb.access.access-log`. Off: access events go only to the ACE audit and SOC log; break-glass is disabled and no standing administrator right is added. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `decision_log_entry` | `case_id` | Event | System | Null for sign-in, refusal, export and break-glass events; DF-DEC-002 already permits this. |
| `decision_log_entry` | `decision_code` | Event | System | `AC-SIGN`, `AC-DENY`, `AC-READ`, `AC-EXPT`, `AC-BGON` or `AC-VERS`; varchar(8). |
| `decision_log_entry` | `actor_user_id` | Session | System | Entra object ID or service identity. |
| `decision_log_entry` | `actions` | Event | System | `area`, `right`, `fieldIds[]` with `masked`, `filter`, `rowCount`, `documentId`, `grantId`, `incidentReference`. No values. |
| `decision_log_entry` | `final_call`, `decided_at` | Event | System | Result and time; hash chain fields written by P7. |
| Session | `breakGlass.active`, `endsAt`, `grantId`, `incidentReference` | Activation | System | Active only until `endsAt`; then ignored. |
| `BreakGlassActivation` | `incidentReference`, `iamRequestId`, `capabilityArea`, `right`, `scope`, `reason` | Request | Request | Pattern, LOVs, reason 20–1000; right C/R/U. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Activation | Group member, valid incident, reason, LOVs | Active | AC-BGON written; `endsAt` set; banner shown. |
| None | Activation | No group, bad incident, short reason, or log failure | Refused | 403/422/503; AC-DENY where a session exists; no grant. |
| Active | End time reached | `now >= endsAt` | Ended | Grant ignored by `AccessCheck`; no job or manual step. |
| Active | Same Idempotency-Key | Repeat of the same request | Active | First response returned; no new entry. |
| Active | New Idempotency-Key | Another activation | Active | 409 MSG-GEN-004; no new grant. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Access log write fails | Read/export returns no data; 503; incident | MSG-P7-003 |
| X2 | No break-glass group | 403; refusal logged | MSG-P4-007; AC-DENY `NO_BREAKGLASS_GRANT` |
| X3 | Missing incident, bad pattern, short reason | 422 naming the field | MSG-GEN-001 / MSG-GEN-002 |
| X4 | Action after the grant ended | Grant ignored; own letters apply; refusal logged | MSG-P4-002; AC-DENY |
| X5 | Second activation while active | Same key returns first; new key 409 | MSG-GEN-004 |
| X6 | Role without Platform administration R | 403; AC-DENY | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints delivered | `POST /api/recovery/v1/admin/break-glass-grants` (API-P4-013); `GET /api/recovery/v1/admin/access-log` (API-P4-008). |
| Existing endpoint used | `GET /api/recovery/v1/decision-log` (API-P7-006) for "who read this case". |
| Contract delta | None against API Specification v2; `BreakGlassActivation`, `BreakGlassGrant` and `AccessLogPage` already exist. The story flow's `/admin/break-glass` is resolved to `/admin/break-glass-grants` (CLAR-001). |
| Backward compatibility | Additive; no existing endpoint changes. |
| Authorization | Platform administration C plus the break-glass group to activate; Platform administration R for the access log; Decision log R for the decision log. |
| Error behaviour | 401; 403 MSG-P4-007 / MSG-P4-002; 409 MSG-GEN-004; 422 MSG-GEN-001 / MSG-GEN-002 / MSG-GEN-003; 503 MSG-P7-003 / MSG-GEN-006. |
| Versioning | No API version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-013; SPEC-RWB-E1-039-017 | New `BreakGlassBanner` and session `breakGlass` state. | Banner shows MSG-P4-004 and end time while active; hidden when inactive; no data leak. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-013, FR-RWB-017; SPEC-RWB-E1-039-001..018 | New writer, break-glass service, grant check, query service and publisher extension. | Positive, negative, boundary and error paths: each event code, fail-closed, group refusal, validation, window/group end, marking, after-end, idempotency, query. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AccessAndAdministrationController` | Controller | `POST /admin/break-glass-grants` and `GET /admin/access-log`. |
| `AccessLogWriter` | Service | Turns an `AccessEvent` into a `DecisionLogRecord` and calls the P7 writer in the caller's transaction. |
| `AccessEventPublisher` | Published interface | Called by P3 and P5 on every read and export; writes through `AccessLogWriter` and the ACE audit/SOC log. |
| `BreakGlassService` | Service | Checks group, incident pattern and reason; writes AC-BGON; holds the grant on the session. |
| `BreakGlassGrantCheck` | Service | Adds the grant's right in its area and scope to `AccessCheck` until `endsAt`; marks entries. |
| `AccessLogQueryService` | Service | Maps `GET /admin/access-log` to the P7 `DecisionLogReader`. |
| `BreakGlassBanner` | React component | Shows MSG-P4-004 with the end time from `GET /me/session`. |

### Package and boundaries

`recovery.access.accesslog` holds the implementation; published types in `recovery.access.accesslog.api`. P3 and P5 call only `AccessEventPublisher`; P4 reads the log only through the P7 `DecisionLogReader`. No module reads `decision_log_entry` directly.

### Data and migration

- No table of its own. Writes `decision_log_entry` only through the P7 writer; `ix_declog_actor_time` on `(actor_user_id, decided_at)` is created by RWB-E1-008.
- Access event codes are added to LOV-DECISION by RW-DATASTEW: `AC-SIGN`, `AC-DENY`, `AC-READ`, `AC-EXPT`, `AC-BGON`, `AC-VERS`.
- `DF-DEC-002` already permits a null `case_id` for access events; no schema change is needed.

### Access event mapping

| Event | When | Payload |
|---|---|---|
| `AC-SIGN` | Sign-in resolves | actor, roles, matrixVersion, conflictVersion |
| `AC-DENY` | Refusal | actor, area, right, reason, caseId if any |
| `AC-READ` | Case or document read | actor, caseId, documentId if any, fieldIds with masked |
| `AC-EXPT` | List export | actor, filter, rowCount, no caseId |
| `AC-BGON` | Break-glass activation | actor, grantId, incident, area, right, scope |
| `AC-VERS` | Reference version approval | actor, loadId, version, rowCount (used by RWB-E1-037/038) |

### Fail-closed read path

The read response is built in the same transaction as the access event. `AccessLogWriter` calls the P7 writer before the response is committed; if the write fails, the transaction rolls back and the caller receives 503 MSG-P7-003 with no data. An incident is raised to the platform administrator queue. There is no asynchronous or best-effort path for a read.

### Break-glass activation

1. The caller must hold RW-PLATADM and be in the break-glass group (RWB-SIT-BREAKGLASS in SIT; DL40).
2. `incidentReference` matches `rwb.access.breakglass.incident-pattern`; `iamRequestId` is present; `reason` is 20–1000 characters; `capabilityArea`, `right` (C/R/U) and `scope` are in their LOVs.
3. Write AC-BGON with the grant ID, incident, area, right and scope.
4. Set `endsAt = min(now + window-hours, group membership end)`; the banner reads it from `GET /me/session`.
5. A same-key repeat returns the first response; a new key while a grant is active returns 409 MSG-GEN-004.

### Grant enforcement and marking

- `BreakGlassGrantCheck` adds the grant's right in its area and scope to `AccessCheck` until `endsAt`; it never adds a right outside the grant.
- At `endsAt` the grant is ignored on the next request; the role's own letters apply. An action after the end is refused with MSG-P4-002 and an AC-DENY entry.
- Every entry written while the grant is active carries `actions.grantId` and `actions.incidentReference`.
- A grant is session-bound: sign-out or token expiry ends it; it cannot be reused in a new session.

### Queries

- `GET /admin/access-log` accepts user, from, to, event, page and size (1–500); it returns `AccessLogPage` from the P7 reader with `at`, `user`, `event`, `capability` and `result`.
- `GET /decision-log` with `caseId`, `decision=AC-READ`, from and to returns the reads in time order, including the incident on a break-glass entry.
- Both queries apply the caller's scope and the Platform administration or Decision log R right.

### Transaction and events

The access event and the read share one transaction. The break-glass activation writes AC-BGON in its own transaction before the grant is returned. No domain event is published; the ACE audit and SOC log receive a copy through INT-22.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration C; requests and activates break-glass | All |
| RW-SECADM | Approves in the bank IAM; reviews use; Platform administration R | All |
| RW-COMPLY | Reads the access log; receives unreviewed uses | All |
| RW-AUDIT | Reads the access log and decision log; changes nothing | All |
| RW-COE, RW-DATASTEW | Platform administration R | All |
| Every bank role | Generates access events | Own session |
| SY-DECLOG | Decision log C | All |

The break-glass right is additive only while the grant is active; it never changes the permission matrix. The reviewer separation (BR9) is a bank IAM control; the Workbench records the evidence.

### Observability and performance

- Metrics: access events by code, log write failures, break-glass activations, after-end refusals, query volume and latency.
- Alerts: log write failure; an AC-BGON with no later review (Epic 8 FEAT-ADM-12); a query with an invalid date range.
- Access events add one insert per read; the P7 indexes on actor/time and case/decision keep the query within the NFR target. Target 21 requests/second peak.

### Feature flag and rollback

- `rwb.access.access-log`. Off: access events go only to the ACE audit and SOC log; break-glass is disabled; no standing administrator right is added.
- Rollback: turn the flag off and redeploy the previous tag; no migration to reverse.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-039-01 | AC1, BR1, BR3 | System | RW-CASEOWN opens a synthetic case at 10:15 | AC-READ with actor, case ID, time; field IDs masked |
| TC-E1-039-02 | AC2, BR4..BR6, BR8 | System | Incident INC0004521; IAM-778812; clock 10:30→14:31 | Grant to 14:30; banner; entries marked; 14:20 allowed; 14:31 refused |
| TC-E1-039-03 | AC3, BR1 | System | Export of 37 filtered cases | AC-EXPT with filter, 37, no case ID |
| TC-E1-039-04 | AC4, BR1 | System | Document on the case | AC-READ with case and document IDs before the file |
| TC-E1-039-05 | AC5, BR4 | System | RW-PLATADM outside the group | 403 MSG-P4-007; AC-DENY |
| TC-E1-039-06 | AC6, BR4 | System | No incident; 12-character reason | 422 MSG-GEN-001; 422 MSG-GEN-002 |
| TC-E1-039-07 | AC7, BR2 | System | Log store off | 503 MSG-P7-003; no data; incident |
| TC-E1-039-08 | AC8, BR6 | System | Three reads on one day | Three entries in time order; 11:02 carries the incident |
| TC-E1-039-09 | AC9, BR1 | System | RW-PHONECOL calls `GET /admin/roles` | 403; AC-DENY area/right, no case ID |
| TC-E1-039-10 | AC10 | System | Same key; then a new key | First response; 409 MSG-GEN-004 |
| TC-E1-039-11 | X4, BR8 | Security | Action after 14:31 | 403 MSG-P4-002; AC-DENY; no grant right |
| TC-E1-039-12 | BR2, BR5 | Unit | Log write failure; window/group-end combinations | Fail closed; `endsAt` is the earlier time |

## Guardrails

- No business value in code: window, incident pattern, reason length and review window are parameters.
- No personal data in logs, tests or prompts; access events carry field IDs and the masking position, never values; the reason is free text and must not hold customer data.
- No read of another module's tables; the access log is read through the P7 interface.
- No right beyond the RW-PLATADM letters without an active grant; the grant end is enforced on every request, not by a job.

## Out of scope

- Logging reads of the data lake copy (RWB-E1-016).
- The break-glass request, approval and review records, held in the bank IAM.
- A scheduled alert for an unreviewed use (Epic 8, FEAT-ADM-12).
- The Decision log query screen SCR-38 (RWB-E2-005) and the Roles and access screen SCR-43 (Epic 8).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-007 | Is the activation path `/admin/break-glass` or `/admin/break-glass-grants`? | A wrong path fails every activation. | API-P4-013 and TSD appendix T-A use `/api/recovery/v1/admin/break-glass-grants`; the flow text is a short form. | RESOLVED | SPEC-007 |
| CLAR-002 | BR5, AC2; SPEC-008 | The token carries group names, not the group end time. Where does the group end come from? | The grant duration depends on it. | Read the break-glass group membership end through INT-21 at activation; if it is not exposed, the window end applies and the 5-minute revalidation ends the grant when the group is removed. Recorded as `ASSUMED`; confirm with the ACE/IAM team. | RESOLVED | SPEC-008 |
| CLAR-003 | Preconditions; SPEC-007 | What is the break-glass group name? | The group check needs a value. | `RWB-SIT-BREAKGLASS` in SIT; the bank standard names are DL40. | RESOLVED | SPEC-007 |
| CLAR-004 | BR5, BR7; SPEC-008, SPEC-018 | Are the window, pattern, reason length and review window fixed? | They are parameters, not code. | 4 hours, `^INC[0-9]{7}$`, 20–1000 characters and 1 working day, assumed under DL38. | RESOLVED | SPEC-008, SPEC-018 |
| CLAR-005 | BR1; SPEC-001..004 | Which codes identify access events? | The decision log code list must accept them. | AC-SIGN, AC-DENY, AC-READ, AC-EXPT, AC-BGON and AC-VERS; RW-DATASTEW adds them to LOV-DECISION. | RESOLVED | SPEC-001..004 |
| CLAR-006 | Data; SPEC-001 | `decision_log_entry.case_id` is not null in older notes. | A schema change would be needed. | DF-DEC-002 already allows null for access events with no case; no schema change. | RESOLVED | SPEC-001 |
| CLAR-007 | BR9; SPEC-018 | Can the Workbench stop a person reviewing their own break-glass use? | The review happens in the bank IAM. | No in-app control; the bank IAM enforces reviewer separation and the Workbench supplies the evidence query. Recorded as a Low finding. | RESOLVED | SPEC-018 |
| CLAR-008 | BR8, AC2; SPEC-010, SPEC-011 | Does a grant survive sign-out? | A reused grant would outlive the session. | No; the grant is session-bound and ends at sign-out or `endsAt`, whichever is first. | RESOLVED | SPEC-010, SPEC-011 |
| CLAR-009 | AC10; SPEC-014 | Can one person hold two grants? | X5 implies one active grant. | One active grant per person; a new key while active returns 409. | RESOLVED | SPEC-014 |
| CLAR-010 | Contract; SPEC-007 | Which rights can a grant carry? | The contract lists C, R, U only. | C, R or U; D and A are not available through break-glass in E1. | RESOLVED | SPEC-007 |

`CLARIFICATION_STATUS: RESOLVED` — all 10 items are answered from the story, the API specification, the admin and access model or the decision log. CLAR-002 and CLAR-007 are design resolutions with a named owner in the compliance review.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; local design system and label standard used for the banner.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New access-log and break-glass capability; two P4 endpoints; one shell banner; access events written through P7.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first delivery of the access-log and break-glass endpoints plus a shell banner]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 10 acceptance criteria, 6 exception paths and 5 grant states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
