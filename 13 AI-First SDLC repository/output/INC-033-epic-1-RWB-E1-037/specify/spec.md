# Technical Specification — RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

| Field | Value |
|---|---|
| Story | RWB-E1-037 — Role to permission matrix as data and PDPA field masking by role |
| Epic / module | E1 / P4 Access and administration |
| RUN_ID | `INC-033-epic-1-RWB-E1-037` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-012, FR-RWB-013); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md` |
| Upstream IDs | BRD-RWB-004; FR-RWB-012, FR-RWB-013; REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009, REQ-ACA-011; US-RWB-E1-037; FEAT-ACA-04, FEAT-ACA-05, FEAT-ACA-13, FEAT-ACA-14; CTL-09, CTL-10, CTL-11; NFR-039, NFR-040, NFR-045; DF-REF-038..044, DF-REF-198..204; DF-PTY-007/008/016; DF-CAS-009/011/012 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label or validation presentation changes. Masking is applied to DTOs before the existing case record view (RWB-E1-023) receives them; the menu and 404 behaviour are consumed from RWB-E1-022. |
| Logic In Scope | `YES` — matrix and masking load, approval, version activation, scope filter, field masking, leaver revalidation. |
| API In Scope | `NO` — no new or changed endpoint. Reuses `POST /api/recovery/v1/admin/reference-loads` and `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve` (delivered by RWB-E1-043), and the P3 transfer endpoint for AC3. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | Reference-load and approval service (RWB-E1-043); `permission` table (RWB-E1-001); P3 case list and case record repositories (scope); every P4/P5/P6 DTO carrying personal fields; session and access check (RWB-E1-022). |
| New Nodes Required | `YES` — `PermissionMatrixLoader`, `MaskingRuleLoader`, `ReferenceLoadApprovalService`, `ScopeService`, `FieldMasker`, `SessionRevalidationFilter`, `AccessAndAdministrationRepository`, `MaskingRule`, `masking_rule`, `uk_permission_version`. |
| Inherited Existing Behavior | Session, `AccessCheck` and refusal events (RWB-E1-022); reference load/approve/rollback (RWB-E1-043); decision log writer (RWB-E1-027); queue membership interface (RWB-E1-019); `sys_fields.is_personal` and the data dictionary (RWB-E1-001); parameters (RWB-E1-042). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The matrix version in force is the only source of what a role may do; a dash refuses every action in the area. | SPEC-RWB-E1-037-001, SPEC-RWB-E1-037-005, SPEC-RWB-E1-037-010 | DIRECT | `AccessCheck` reads the session's matrix version; no code list. | COVERED |
| BR2 | A matrix file holds every active role once for all 14 areas, letters `C,R,U,D,A` in order or `-`; any error refuses the file whole. | SPEC-RWB-E1-037-001, SPEC-RWB-E1-037-014 | DIRECT | Whole-file validation; no partial load. | COVERED |
| BR3 | A version is approved by the role named in the parameter for the table, never by its loader. | SPEC-RWB-E1-037-002 | DIRECT | `rwb.refload.approver.permission` / `masking_rule`. | COVERED |
| BR4 | Scope filters records first; an out-of-scope record is never returned and the excluded count is never shown. | SPEC-RWB-E1-037-005, SPEC-RWB-E1-037-006 | DIRECT | `ScopeFilter` applied by the owning module's query. | COVERED |
| BR5 | OWN, TEAM, REGION and ALL have the defined meanings. | SPEC-RWB-E1-037-005 | DIRECT | OWN = owns or has a task; TEAM = team queues; REGION = team regions; ALL = every case. | COVERED |
| BR6 | A personal field is masked unless the masking rule in force lets one of the session's roles see it; no rule means masked. | SPEC-RWB-E1-037-007, SPEC-RWB-E1-037-008 | DIRECT | Default deny; `masking_rule.unmasked = true` is required. | COVERED |
| BR7 | Masking is applied before data reaches a screen or an agent. | SPEC-RWB-E1-037-008 | DIRECT | `FieldMasker` runs on the DTO, not in the browser or agent. | COVERED |
| BR8 | A leaver's removal from a group ends the open session at the next request after the membership refresh. | SPEC-RWB-E1-037-011 | DIRECT | `SessionRevalidationFilter`; refresh interval is a parameter. | COVERED |
| BR9 | An approval that cannot be written to the decision log does not take effect. | SPEC-RWB-E1-037-004 | DIRECT | Log write is the last step in the approval transaction. | COVERED |
| AC1 | PM-2026.12 gives RW-LEGAL `R` in Queue and allocation; after approval RW-LEGAL calls `GET /queues` with 200; one log entry records 756 rows. | SPEC-RWB-E1-037-001, SPEC-RWB-E1-037-002, SPEC-RWB-E1-037-003 | DIRECT | 54 roles × 14 areas = 756. | COVERED |
| AC2 | RW-PHONECOL sees identity `XXXXXXXXX1234` and phone `XXXXXX5678`, no PII service call, and an access event with masked fields. | SPEC-RWB-E1-037-007, SPEC-RWB-E1-037-008, SPEC-RWB-E1-037-009 | DIRECT | Masking format and event. | COVERED |
| AC3 | RW-CASEOWN calling transfer is refused 403 before the handler; case unchanged; refusal event area/right. | SPEC-RWB-E1-037-010 | DIRECT | Interceptor from RWB-E1-022. | COVERED |
| AC4 | RW-CASEOWN with OWN sees 12 cases; an out-of-scope case returns 404 MSG-P4-003. | SPEC-RWB-E1-037-005, SPEC-RWB-E1-037-006 | DIRECT | Total equals returned rows; excluded count hidden. | COVERED |
| AC5 | A file with a duplicate role/area and invalid letters `RX` is refused whole; PM-2026.11 stays. | SPEC-RWB-E1-037-001 | DIRECT | MSG-P1-002 names row and letters. | COVERED |
| AC6 | The loader cannot approve; RW-COE is refused 403. | SPEC-RWB-E1-037-002 | DIRECT | MSG-P7-002 then MSG-P4-002. | COVERED |
| AC7 | Decision log unavailable: approval returns 503 MSG-P7-003; load stays Loaded. | SPEC-RWB-E1-037-004 | DIRECT | Rollback of the approval transaction. | COVERED |
| AC8 | A leaver's group removed at 10:00; request at 10:06 is 401 MSG-P4-001; session ends. | SPEC-RWB-E1-037-011 | DIRECT | 5-minute refresh. | COVERED |
| AC9 | A personal field with no masking rule is masked as `XXXX-XX-XX`. | SPEC-RWB-E1-037-007 | DIRECT | Default deny. | COVERED |
| AC10 | Two approvals at once: one approves and logs; the other 409 MSG-GEN-004 and writes nothing. | SPEC-RWB-E1-037-012 | DIRECT | Optimistic lock on the load. | COVERED |
| X1 | A role without the right calls an action. | SPEC-RWB-E1-037-010 | DIRECT | 403 before handler. | COVERED |
| X2 | A record outside scope is requested. | SPEC-RWB-E1-037-006 | DIRECT | 404 MSG-P4-003. | COVERED |
| X3 | A matrix file misses a role, repeats a role/area or holds a bad letter. | SPEC-RWB-E1-037-001, SPEC-RWB-E1-037-014 | DIRECT | Whole-file refusal. | COVERED |
| X4 | The loader approves their own load. | SPEC-RWB-E1-037-002 | DIRECT | MSG-P7-002. | COVERED |
| X5 | A role other than the table's approver calls approve. | SPEC-RWB-E1-037-002 | DIRECT | 403 MSG-P4-002. | COVERED |
| X6 | The decision log write fails. | SPEC-RWB-E1-037-004 | DIRECT | Load stays Loaded. | COVERED |
| X7 | A leaver's group is removed during a session. | SPEC-RWB-E1-037-011 | DIRECT | 401 MSG-P4-001. | COVERED |
| X8 | No masking rule exists for a field and role. | SPEC-RWB-E1-037-007 | DIRECT | Masked. | COVERED |
| X9 | Two approve calls arrive at once. | SPEC-RWB-E1-037-012 | DIRECT | 409 MSG-GEN-004. | COVERED |

## User story intent interpretation

As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies**, so that **a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it**.

The story is the data and enforcement layer behind RWB-E1-022. It adds no screen: it changes what the existing menu, case list, case record view and every DTO expose. It ends access for a leaver at the next request after the membership refresh and puts the permission, masking and scope controls under versioned data.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/reference-loads` for table `permission` or `masking_rule`; `POST /admin/reference-loads/{loadId}/approve`; every request through `SessionRevalidationFilter` and `ScopeService`; every DTO through `FieldMasker`. |
| Preconditions | RWB-E1-022 done; RWB-E1-043 done; RWB-E1-027 done; PM-2026.11 in force; MASK-2026.11 loaded with no unmasked rows in PROD (DL26); `rwb.refload.approver.permission=RW-SECADM` and `rwb.refload.approver.masking_rule=RW-COMPLY` in the catalogue; P3 queue membership interface returns teams and regions. |
| Input | Matrix or masking file, table code, valid from, caller identity, business date; request context for scope and masking. |
| Output | `permission` and `masking_rule` rows; approved version; `ScopeFilter`; masked DTO; access event; 404 for out-of-scope records. |
| Feature flag | `rwb.access.permission-matrix`. Off: the seeded PM-2026.11 rows and the default mask-all policy apply; new loads are refused. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `permission` | `role_id`, `capability_area`, `letters`, `matrix_version`, `state`, `is_active` | Load file | Data load only | One row per role and area per version; letters `C,R,U,D,A` in order or `-`. |
| `masking_rule` | `role_code`, `field_id`, `unmasked`, `masking_version`, `valid_from`, `valid_to` | Load file | Data load only | `field_id` must exist in `sys_fields` with `is_personal = true`. |
| `role` | `default_scope` | Role table (RWB-E1-019) | Data load only | `OWN`, `TEAM`, `REGION` or `ALL`. |
| `party` | `id_no_token`, `date_of_birth` | Owning module DTO | Read only | Masked by `FieldMasker`; clear value only through the ACE PII service. |
| `contact_point` | `value_token` | Owning module DTO | Read only | Masked by `FieldMasker`. |
| `recovery_case` | `owner_user_id`, `team_code`, `region_code` | P3 repository | Read only | Used by the P3 query to apply `ScopeFilter`. |
| `decision_log_entry` | `decision_code`, `final_call`, `actions` | Approval | System | One entry per approved version; `AC-VERS`. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every check passes | Loaded | Rows written; not in force. |
| None | Load | Any check fails | Refused | No row written; version in force stays. |
| Loaded | Approve | Approver role matches, caller is not the loader, log written | Approved | Valid from recorded; previous version's `valid_to` set. |
| Loaded | Approve | Loader, wrong role, or log failure | Loaded | 409/403/503; nothing changes. |
| Approved | New version approved | Later valid from | Superseded | Previous rows readable with `valid_to`. |
| Resolved | Group removed and refresh elapsed | Next request | Ended | 401 MSG-P4-001; no new session with the removed group. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Role without the right calls an action | 403 before handler; nothing changes | MSG-P4-002; refusal event |
| X2 | Out-of-scope record requested | 404; no record; excluded count hidden | MSG-P4-003 |
| X3 | Matrix file has a missing role, duplicate row or bad letter | Load refused whole; version in force stays | MSG-P1-002 |
| X4 | Loader approves own load | Refused; stays Loaded | MSG-P7-002 |
| X5 | Wrong role approves | 403; stays Loaded | MSG-P4-002 |
| X6 | Decision log write fails during approval | Approval rolled back; stays Loaded | MSG-P7-003 |
| X7 | Leaver's group removed during a session | Next request after refresh: 401; session ended | MSG-P4-001 |
| X8 | No masking rule for a field and role | Field masked | None |
| X9 | Two approvals at once | One approves; the other 409; one log entry | MSG-GEN-004 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`; `POST /api/recovery/v1/cases/{caseId}/transfer` (P3, used only to show the refusal). |
| Contract delta | None. `ScopeService` and `FieldMasker` are published Java interfaces, not REST contracts. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; the approver role parameter to approve; Queue and allocation U for transfer; Platform administration R for admin reads. |
| Error behaviour | 401; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P7-002 / MSG-GEN-004; 422 MSG-P1-002; 503 MSG-P7-003 / MSG-GEN-006. |
| Versioning | No API version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change. The case record view (RWB-E1-023) only receives masked DTOs. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-012, FR-RWB-013; SPEC-RWB-E1-037-001..014 | New loaders, approval service, scope service, masker, revalidation filter and repositories. | Positive, negative, boundary and error paths: whole-file validation, maker-checker, log failure, concurrent approve, each scope, out-of-scope 404, masking default, mask format, PII service, leaver refresh. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AccessAndAdministrationController` | Controller | Load and approve for `permission` and `masking_rule`. |
| `PermissionMatrixLoader` | Service | Whole-file validation and row storage with the new `matrix_version`. |
| `MaskingRuleLoader` | Service | Validates known roles and personal field IDs; stores the masking version. |
| `ReferenceLoadApprovalService` | Service | Approver role, maker-checker, decision log, status change in one transaction; shared with RWB-E1-038. |
| `ScopeService` | Published interface | Builds `ScopeFilter` from the session roles and the P3 queue membership interface. |
| `FieldMasker` | Published interface | Masks `@PersonalData("DF-...")` DTO fields; fetches clear values only through the ACE PII service. |
| `SessionRevalidationFilter` | Service | Compares session groups with the ACE common module's current groups on each request. |
| `AccessAndAdministrationRepository` | Repository | Reads and writes `permission`, `masking_rule`, `role`, `sys_fields`. |
| `MaskingRule` | Entity | Maps `masking_rule`. |

### Package and boundaries

`recovery.access.matrix` holds the implementation; published types in `recovery.access.matrix.api`. P3 applies `ScopeFilter` in its own query and P5/P6 apply `FieldMasker` to their DTOs; P4 never reads another module's tables. The approval service is shared with RWB-E1-038 through its interface.

### Data and migration

- Reads: `role` (`role_code`, `default_scope`, `role_class`), `permission` (`role_id`, `capability_area`, `letters`, `matrix_version`), `sys_fields` (`field_id`, `is_personal`), `queue_member` through the P3 interface.
- Writes: `permission` rows with `state` and `is_active`; `masking_rule` rows; `decision_log_entry` through the P7 writer.
- Migration `V_E1_037__masking_rule.sql` creates `masking_rule` (id, role_code, field_id, unmasked, masking_version, valid_from, valid_to, standard columns) with a unique index on `(masking_version, role_code, field_id)`, and `uk_permission_version` on `permission (matrix_version, role_id, capability_area)`.
- No personal value is copied into a new table; masking is applied at read time.

### Matrix and masking load checks

1. Table code is `permission` or `masking_rule`.
2. Every active role appears once for each of the 14 capability areas; no duplicate role/area.
3. Letters are `C`, `R`, `U`, `D`, `A` in that order or `-`; any other character fails.
4. Role codes and capability areas are known; `validFrom` is not before the business date.
5. Masking rows use a known role and a `sys_fields` row with `is_personal = true`.
6. A difference report against the version in force is produced for the approver.
7. Any failure refuses the load whole; no row is written.

### Approval and activation

- The approver must hold the role named by `rwb.refload.approver.<table>` and must not be the loader.
- The approval writes one `AC-VERS` decision log entry with the load ID, version, row count, approver and `final_call = APPROVED`, then sets the load Approved and the previous version's `valid_to` to the day before the new `valid_from`, in one transaction.
- If the log write fails, the whole approval rolls back; the load stays Loaded (MSG-P7-003).
- The optimistic `version` on the load makes two simultaneous approvals produce one success and one 409 (MSG-GEN-004).
- Open sessions keep the matrix version they resolved at sign-in (RWB-E1-022 AC9); the next session uses the new version.

### Scope

- `ScopeFilter` carries `type` (`OWN`, `TEAM`, `REGION`, `ALL`), `userRef`, `teamCodes`, `regionCodes`.
- OWN = cases the person owns or has a task on; TEAM = cases in the person's team queues; REGION = cases in the regions of the person's teams; ALL = every case.
- The effective scope of a multi-role session is the widest scope among its roles (`ALL` > `REGION` > `TEAM` > `OWN`), because roles are additive (RWB-E1-022 BR3); see CLAR-001.
- The owning module applies the filter in its query. An out-of-scope record returns 404 MSG-P4-003; the total never includes excluded records and the excluded count is never shown.

### Masking

- A DTO field annotated `@PersonalData("DF-...")` is masked unless a `masking_rule` row for one of the session's roles, in the version in force, has `unmasked = true`.
- With no rule, the field is masked. Identity and phone keep the last 4 characters (`rwb.access.mask.keep-last=4`, assumed DL26); date of birth shows `XXXX-XX-XX`.
- Masking happens before the DTO leaves the service, so the screen and any agent receive the masked value. A clear value is fetched only through the ACE PII service, which logs the read to PII Kafka (INT-22).
- The access event records the case ID and the field IDs with their masking position; it never records a value.

### Leaver revalidation

- `SessionRevalidationFilter` compares the session's groups with the groups the ACE common module holds for the person, refreshed at most every `rwb.access.membership-refresh-minutes` (5, assumed DL38).
- If a group has been removed, the session ends and the request is refused with 401 MSG-P4-001; a new sign-in with the removed group is refused.
- If the membership service is unavailable, the request fails closed with 503 MSG-GEN-006 and an alert; the session is not extended on stale groups.

### Transaction and events

The load and the approval are each one transaction. The approval writes the decision log entry last; a failure rolls back the status change. No domain event is published. Refusal and masked-view events go through `AccessEventPublisher`; RWB-E1-039 adds the decision log sink.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C (load); approves none | All |
| RW-COE | Reference data C for tables it owns; approves none | All |
| RW-SECADM | Approver for `permission`; Platform administration R | All |
| RW-COMPLY | Sets and approves `masking_rule`; Platform administration R | All |
| RW-AUDIT | Reference data R; reads versions and approvals | All |
| Every bank role | Sees cases in its scope with fields masked | Own session |
| SY-CASEWF, SY-RULES | Reference data R; apply `ScopeFilter` / masking | All |

Every endpoint is checked with Spring Security method security plus `AccessCheck`. The approval role is a parameter, not a hard-coded role code.

### Observability and performance

- Load response: status, row count, failed check and row; difference report.
- Metrics: loads, refusals by check, approvals, concurrent conflicts, masked fields, PII service calls, revalidation refusals.
- Alerts: approval log failure; membership service unavailable; a spike in out-of-scope 404s.
- The matrix is 756 rows; it is cached by version. Scope filters use the P3 indexes on owner, team and region. Masking is in-memory on the DTO; no extra query.

### Feature flag and rollback

- `rwb.access.permission-matrix`. Off: the seeded PM-2026.11 rows and default mask-all policy apply; new loads are refused.
- Rollback: turn the flag off and redeploy the previous tag; the `masking_rule` migration is additive.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-037-01 | AC1, BR1 | System | PM-2026.11 and PM-2026.12 differing in one letter | RW-LEGAL gets 200 on `GET /queues`; one log entry with 756 rows |
| TC-E1-037-02 | AC2, BR6, BR7 | System | RW-PHONECOL opens a synthetic case | `XXXXXXXXX1234`, `XXXXXX5678`; no PII call; masked-field event |
| TC-E1-037-03 | AC3, BR1 | System | RW-CASEOWN calls transfer | 403 MSG-P4-002; case unchanged; refusal event |
| TC-E1-037-04 | AC4, BR4, BR5 | System | 12 owned cases; one other-team case | 12 rows and total 12; other case 404 MSG-P4-003 |
| TC-E1-037-05 | AC5, BR2 | System | Duplicate row and `RX` letters | Refused; MSG-P1-002; PM-2026.11 stays |
| TC-E1-037-06 | AC6, BR3 | System | Loader approves, then RW-COE | MSG-P7-002; then 403 MSG-P4-002 |
| TC-E1-037-07 | AC7, BR9 | System | Decision log store off | 503 MSG-P7-003; stays Loaded |
| TC-E1-037-08 | AC8, BR8 | System | Group removed at 10:00; request at 10:06 | 401 MSG-P4-001; session ended |
| TC-E1-037-09 | AC9, BR6 | System | No rule for `party.date_of_birth` | `XXXX-XX-XX` |
| TC-E1-037-10 | AC10 | System | Two parallel approvals | One success; one 409 MSG-GEN-004; one log entry |
| TC-E1-037-11 | X1, X2 | Security | Role without the right; out-of-scope case | 403; 404; no data leak |
| TC-E1-037-12 | BR2, BR5 | Unit | Every letter; each scope; multi-role scope | Validation; filter type; widest scope |

## Guardrails

- No letter, scope, masking position, approver role or refresh interval is written in code; all are rows or parameters.
- No personal data in logs, tests or prompts; tests use tokenized synthetic values; access events list field IDs, never values.
- No read of another module's tables; the scope filter is applied by the owning module, masking works on DTOs.
- A field with no masking rule is masked; an unmasked value is fetched only through the ACE PII service.
- A version already approved is never edited; a change is a new version.

## Out of scope

- Reallocation of a leaver's or mover's open cases (RWB-E1-030; R-UNI-18 and R-UNI-19 in Epic 2).
- Administration screens SCR-43 and SCR-47 (Epic 8, FEAT-ADM-01 and FEAT-ADM-14).
- Masking values for each role and field (Compliance, DL26).
- Access per data product in the data lake copy (RWB-E1-016) and the six-monthly access review (JOB-18, Epic 2).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4, BR5; SPEC-005 | How do the scopes of two roles combine? | A person with OWN and TEAM would see a different number of cases under the narrowest and widest rule. | The widest scope wins (`ALL` > `REGION` > `TEAM` > `OWN`), because roles are additive (RWB-E1-022 BR3). Recorded as `ASSUMED`; confirm with the product owner before SIT. | RESOLVED | SPEC-005 |
| CLAR-002 | BR6; SPEC-007 | What mask format applies to identity, phone and date of birth? | The AC fixes the examples, not the rule. | Keep the last 4 characters for identity and phone (`rwb.access.mask.keep-last=4`, assumed DL26); date of birth `XXXX-XX-XX`. | RESOLVED | SPEC-007 |
| CLAR-003 | BR6, AC9; SPEC-007 | Is a field with no rule masked? | Default direction. | Yes; the story says masked, and Compliance supplies the rules under DL26. | RESOLVED | SPEC-007 |
| CLAR-004 | BR6, BR7; SPEC-008 | Where does a clear value come from? | The Workbench must not store or return clear personal data by another path. | Only through the ACE PII service, which logs the read to PII Kafka (INT-22). | RESOLVED | SPEC-008 |
| CLAR-005 | BR3; SPEC-002 | The matrix has no holder of Reference data A. Who approves? | Approval cannot proceed without an approver. | The parameter names the approver role: RW-SECADM for `permission`, RW-COMPLY for `masking_rule`; no matrix A right is used. | RESOLVED | SPEC-002 |
| CLAR-006 | AC1; SPEC-001 | Why 756 rows? | Row-count check. | 54 active roles × 14 capability areas. | RESOLVED | SPEC-001 |
| CLAR-007 | BR8; SPEC-011 | How often is group membership refreshed? | Leaver response time. | Every 5 minutes (`rwb.access.membership-refresh-minutes=5`, assumed DL38). | RESOLVED | SPEC-011 |
| CLAR-008 | BR8; SPEC-011 | What if the membership service is unavailable? | Fail open would extend a leaver's access. | Fail closed with 503 MSG-GEN-006 and an alert; the session is not extended on stale groups. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the reference-data process or the decision log. CLAR-001 and CLAR-008 are design resolutions with a named owner in the compliance review.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend access-data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New permission-matrix, masking and scope capability on the existing reference-load service; no screen or contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new loaders, scope and masking on existing load/approve endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 10 acceptance criteria, 9 exception paths and 6 load/session states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
