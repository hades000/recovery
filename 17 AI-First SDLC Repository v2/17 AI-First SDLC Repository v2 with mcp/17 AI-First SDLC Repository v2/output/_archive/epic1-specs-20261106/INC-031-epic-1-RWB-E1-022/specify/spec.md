# Technical Specification — RWB-E1-022 Sign-on with SSO, MFA and the first roles

| Field | Value |
|---|---|
| Story | RWB-E1-022 — Sign-on with SSO, MFA and the first roles |
| Epic / module | E1 / P4 Access and administration |
| RUN_ID | `INC-031-epic-1-RWB-E1-022` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-011); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 022 Sign on with SSO MFA and the first roles v1.md` |
| Upstream IDs | BRD-RWB-004; FR-RWB-011; REQ-ACA-001, REQ-ACA-002, REQ-ACA-010; US-RWB-E1-022; FEAT-ACA-01..03; CTL-09; NFR-049, NFR-051; DF-REF-034..044, DF-REF-205..211 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — two shell components are added: the session line (`SessionBanner`) and the no-role page (`AccessRequestPage`); the ACE shell menu is filtered by the session's effective letters. No business screen; SCR-43 is Epic 8. Design evidence is local: screen inventory/navigation, design system and label standard; no Figma and no shell prototype. |
| Logic In Scope | `YES` — token checks, group-to-role mapping, conflict check, session build, access check, version retention, refusal events. |
| API In Scope | `YES` — first delivery of `GET /api/recovery/v1/admin/roles` (API-P4-007) and `GET /api/recovery/v1/me/session` (API-P4-012). |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | ACE sign-in and Entra ID integration (INT-21); ACE front-end shell; `role`, `permission` tables (RWB-E1-001, rows loaded by RWB-E1-019); every recovery controller through `AccessCheckInterceptor`. |
| New Nodes Required | `YES` — `SessionResolver`, `AccessCheckService`, `AccessCheckInterceptor`, `AccessEventPublisher`, `AccessAndAdministrationRepository`, `RoleConflict`, `role_conflict`, `SessionBanner`, `AccessRequestPage`. |
| Inherited Existing Behavior | Recovery schema and `role`/`permission` tables (RWB-E1-001); 54 role rows and environment group names (RWB-E1-019); permission matrix PM-2026.11 and separation-of-duty version SOD-2026.11; ACE audit and SOC logging (INT-22); parameter catalogue (RWB-E1-042). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role; no Workbench password or local account. | SPEC-RWB-E1-022-003, SPEC-RWB-E1-022-012 | DIRECT | `role.entra_group` is the only mapping source; no local credential table. | COVERED |
| BR2 | A session is refused unless the token carries a second factor. | SPEC-RWB-E1-022-002 | DIRECT | `amr` must contain the value of `rwb.access.required-amr` (`mfa`). | COVERED |
| BR3 | No role inherits from another; two roles give the union of both roles' letters. | SPEC-RWB-E1-022-005 | DIRECT | `AccessCheckService` unions letters per capability area. | COVERED |
| BR4 | A capability area with no letter for any session role refuses every action in that area. | SPEC-RWB-E1-022-005 | DIRECT | Dash or absent row denies; no implicit read. | COVERED |
| BR5 | A role pair listed in the role conflict table may not be held in one session. | SPEC-RWB-E1-022-004, SPEC-RWB-E1-022-011 | DIRECT | `role_conflict` rows valid on the sign-in date; both directions checked. | COVERED |
| BR6 | A service identity holds a role in the same table and is checked the same way as a person. | SPEC-RWB-E1-022-010 | DIRECT | `role_class = NON_HUMAN_ACTOR`; role checks apply, MFA check does not. | COVERED |
| BR7 | A session keeps the matrix and conflict versions it resolved at sign-in until it ends. | SPEC-RWB-E1-022-006 | DIRECT | Versions stored on `SessionContext`; checks use the stored version. | COVERED |
| BR8 | Group names, roles, letters and conflicts are versioned data rows, never code. | SPEC-RWB-E1-022-011, SPEC-RWB-E1-022-017 | DIRECT | `role`, `permission` and `role_conflict` rows; no literal role or group in code. | COVERED |
| AC1 | SSO sign-in with MFA resolves RW-CASEOWN, scope OWN and PM-2026.11; the session line and menu follow. | SPEC-RWB-E1-022-001, SPEC-RWB-E1-022-003, SPEC-RWB-E1-022-008 | DIRECT | AC1 fixture: `RWB-SIT-RW-CASEOWN`. | COVERED |
| AC2 | RW-PHONECOL calling `GET /admin/roles` is refused 403 MSG-P4-002 and one refusal event is written. | SPEC-RWB-E1-022-005, SPEC-RWB-E1-022-007, SPEC-RWB-E1-022-009 | DIRECT | Interceptor runs before the handler. | COVERED |
| AC3 | No RWB-SIT group gives MSG-P4-001, 401 on every recovery endpoint, and a NO_ROLE refusal event. | SPEC-RWB-E1-022-003, SPEC-RWB-E1-022-007, SPEC-RWB-E1-022-013 | DIRECT | No role = no session; no data returned. | COVERED |
| AC4 | A token with `pwd` but not `mfa` is refused 401 MSG-P4-005 with a NO_MFA event. | SPEC-RWB-E1-022-002, SPEC-RWB-E1-022-007 | DIRECT | MFA check after group mapping, before conflict check. | COVERED |
| AC5 | RW-LITOFF plus RW-LEGAL gives Documents `CRUA`, the union of `CRU` and `CRUA`. | SPEC-RWB-E1-022-005 | DIRECT | Letter union per area. | COVERED |
| AC6 | RW-SECADM plus RW-CASEOWN is refused MSG-P4-006, an incident is raised and ROLE_CONFLICT is logged. | SPEC-RWB-E1-022-004, SPEC-RWB-E1-022-007, SPEC-RWB-E1-022-011 | DIRECT | `ANY_BUSINESS_ROLE` matches `role_class = BANK_USER`. | COVERED |
| AC7 | Managed identity SY-RULES calling `GET /admin/roles` is refused 403 MSG-P4-002 and logged. | SPEC-RWB-E1-022-010 | DIRECT | Non-human session resolves; Platform administration letter is `-`. | COVERED |
| AC8 | An unmapped or inactive group gives no role; the mapped group still resolves; the unmapped name is logged. | SPEC-RWB-E1-022-003, SPEC-RWB-E1-022-007 | DIRECT | Unmatched groups ignored; names recorded on the sign-in event. | COVERED |
| AC9 | An open session keeps PM-2026.11 after PM-2026.12 takes effect; a new session uses PM-2026.12. | SPEC-RWB-E1-022-006 | DIRECT | `matrixVersion` fixed at sign-in. | COVERED |
| X1 | A role without the right calls an endpoint. | SPEC-RWB-E1-022-005, SPEC-RWB-E1-022-007 | DIRECT | 403 before handler; AC-DENY event. | COVERED |
| X2 | The person is in no Workbench group. | SPEC-RWB-E1-022-003, SPEC-RWB-E1-022-013 | DIRECT | 401 MSG-P4-001; no data. | COVERED |
| X3 | The token has no second factor. | SPEC-RWB-E1-022-002 | DIRECT | 401 MSG-P4-005; NO_MFA. | COVERED |
| X4 | The groups give a conflicting role pair. | SPEC-RWB-E1-022-004 | DIRECT | Refuse; incident; ROLE_CONFLICT. | COVERED |
| X5 | A service identity calls an area its role does not hold. | SPEC-RWB-E1-022-010 | DIRECT | 403, same as a person. | COVERED |
| X6 | A group maps to no active role row. | SPEC-RWB-E1-022-003 | DIRECT | Ignore; if none left, X2. | COVERED |
| X7 | A new matrix version takes effect while a session is open. | SPEC-RWB-E1-022-006 | DIRECT | Open session keeps its version. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **to sign in once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow**, so that **access is controlled from the first release and nobody holds a Workbench password or a local account**.

The story is the access foundation for every Epic 1 screen and endpoint. It does not add a business screen. It adds the session line and the no-role page to the ACE shell, filters the menu by the effective permission matrix, and puts a capability check in front of every controller. The security administrator maintains groups in the bank IAM; the Workbench only reads them.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A person or service identity opens the Workbench; the ACE common module returns a verified OpenID Connect token to `SessionResolver`. |
| Preconditions | RWB-E1-001 tables exist; RWB-E1-019 loaded the 54 role rows and each environment's `role.entra_group`; PM-2026.11 is loaded; SOD-2026.11 is loaded; INT-21 is configured with the bank conditional-access policy; `rwb.access.required-amr=mfa` is in the parameter catalogue. |
| Input | Verified token: subject/object ID, `groups` claim, `amr` claim, token expiry. |
| Output | `SessionContext` (userRef, roles, matrixVersion, conflictVersion, scopeLine, permissions, breakGlass); `GET /me/session` response; sign-in or refusal event; filtered menu. |
| Feature flag | `rwb.access.sso-roles`. Off: the ACE common module's existing role check applies and the Workbench session components are not enabled. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `role` | `entra_group` | Loaded by RW-REFADM (RWB-E1-019) | Data load only | One group per role per environment; active rows only are mapped. |
| `role` | `is_active` | Data load | Data load only | Inactive rows are ignored at sign-in. |
| `permission` | `letters`, `matrix_version` | Loaded by RWB-E1-037 | Data load only | Read for the session's matrix version. |
| `role_conflict` | `role_code`, `conflicts_with`, `conflict_version`, `valid_from`, `valid_to` | SOD-2026.11 load | Data load only | `conflicts_with` is a role code, `ANY_BUSINESS_ROLE` or `ANY_OTHER_ROLE`. |
| Session | `userRef`, `roles` | Token subject / group mapping | System | Entra object ID only; active role rows only; zero roles refuses. |
| Session | `matrixVersion`, `conflictVersion`, `scopeLine`, `permissions` | Versions and letters in force at sign-in | System | Fixed until the session ends; labels from the content standard; Thai per DL10. |
| Access event | `eventCode`, `actorUserRef`, `area`, `right`, `result`, `reasonCode`, `unmappedGroups` | Request and session | System | No personal data; object ID only. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Verified token | At least one active role, MFA present, no conflict | Resolved | `SessionContext` built; AC-SIGN event; menu and session line available. |
| None | Verified token | No group maps to an active role | Refused (NO_ROLE) | 401 MSG-P4-001; AC-DENY event; no data. |
| None | Verified token | A bank-user role is present and `amr` lacks `mfa` | Refused (NO_MFA) | 401 MSG-P4-005; AC-DENY event. |
| None | Verified token | A role pair is in the conflict table | Refused (ROLE_CONFLICT) | MSG-P4-006; incident; AC-DENY event. |
| Resolved | Sign-out or token expiry | — | Ended | Session discarded; no role cache survives. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A role without the right calls an endpoint | 403 before the handler; nothing changes | MSG-P4-002; AC-DENY `NO_RIGHT` |
| X2 | No Workbench group | 401; access request page; no case, queue or reference data | MSG-P4-001; AC-DENY `NO_ROLE` |
| X3 | No second factor in `amr` | 401; refusal logged | MSG-P4-005; AC-DENY `NO_MFA` |
| X4 | Conflicting role pair | Session refused; incident to security administrator | MSG-P4-006; AC-DENY `ROLE_CONFLICT` |
| X5 | Service identity without the right | 403, exactly as a person | MSG-P4-002; AC-DENY |
| X6 | Unmapped or inactive group | Group ignored; other groups still resolve; name logged | None unless no role remains |
| X7 | Matrix version changes during a session | Open session keeps its version; next sign-in uses the new one | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints delivered | `GET /api/recovery/v1/admin/roles` (API-P4-007); `GET /api/recovery/v1/me/session` (API-P4-012). |
| Contract delta | `Session` adds an additive `permissions` array (`capabilityArea`, `letters`) so the shell can filter the menu without reading the matrix table. No existing field changes; recorded in the additions file. |
| Backward compatibility | Additive; no existing endpoint changes. |
| Authorization | `GET /admin/roles`: Platform administration, right R. `GET /me/session`: any resolved session; returns only the caller's own session. |
| Error behaviour | 401 MSG-P4-001 / MSG-P4-005 / MSG-P4-006; 403 MSG-P4-002; 503 MSG-GEN-006. |
| Versioning | No API version change; the OpenAPI file is unchanged until the additions are merged. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-011; SPEC-RWB-E1-022-008 | New `SessionBanner`, `AccessRequestPage` and menu filter. | Session line renders from `GET /me/session`; no-role page hides all data; menu shows only areas with R; refusal state is reachable. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-011; SPEC-RWB-E1-022-001..017 | New resolver, access check, interceptor, event publisher and repository. | Positive, negative, boundary and error paths: MFA, no role, unmapped group, conflict both directions, letter union, dash, service identity, version retention. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AccessAndAdministrationController` | Controller | `GET /admin/roles` and `GET /me/session`; maps refusals to problem responses with `messageCode`. |
| `SessionResolver` | Service | Maps groups to active roles, checks MFA and conflicts, builds `SessionContext` with both versions. |
| `AccessCheckService` | Published interface | Unions letters per capability area and tests the requested right against the session's matrix version. |
| `AccessCheckInterceptor` | Service | Reads the `x-capability` area and right declared on each operation and calls `AccessCheckService` before the handler. |
| `AccessEventPublisher` | Published interface | Writes sign-in and refusal events to the ACE audit and SOC log; RWB-E1-039 adds the decision log. |
| `AccessAndAdministrationRepository` | Repository | Reads `role`, `permission` and `role_conflict` rows in force. |
| `RoleConflict` | Entity | Maps the new `role_conflict` table. |
| `SessionBanner` / `AccessRequestPage` | React components | Session line and no-role page in the ACE shell; menu filtering by effective letters. |

### Package and boundaries

`recovery.access.signin` holds the implementation; published types in `recovery.access.signin.api`. The front end lives in `recovery/access`. Other modules call only `AccessCheck` and `AccessEventPublisher`; no module reads `role`, `permission` or `role_conflict` directly.

### Data and migration

- Reads: `role` (`id`, `role_code`, `role_name`, `role_class`, `default_scope`, `entra_group`, `is_active`), `permission` (`role_id`, `capability_area`, `letters`, `matrix_version`, `is_active`), `role_conflict` (`role_code`, `conflicts_with`, `reason`, `conflict_version`, `valid_from`, `valid_to`).
- Migration `V_E1_022__role_conflict.sql` creates `role_conflict` with the standard columns and `ix_role_entra_group` on `role (entra_group) WHERE is_active`.
- No table stores a password, token or local account.

### Session resolution

1. The ACE common module validates the token and passes the subject, `groups`, `amr` and expiry.
2. Map each group to an active `role.entra_group` row; ignore unmatched groups and record their names.
3. If no role remains, refuse `NO_ROLE`.
4. If any resolved role has `role_class = BANK_USER` and `amr` lacks `rwb.access.required-amr`, refuse `NO_MFA`.
5. Read `role_conflict` rows valid on the sign-in date; check both directions. A row with `ANY_BUSINESS_ROLE` matches any `BANK_USER` role; `ANY_OTHER_ROLE` matches any other role in the session. Refuse `ROLE_CONFLICT`.
6. Build `SessionContext`: userRef, roles, matrixVersion, conflictVersion, scopeLine, permissions, resolvedAt, breakGlass null.
7. Publish AC-SIGN with the role codes, versions and unmapped group names.

### Access check

The effective letters for an area are the union of the session roles' letters for the session's matrix version. A dash or a missing row denies. The interceptor runs before the handler and refuses with 403 MSG-P4-002; a refusal writes AC-DENY with the area, right and reason `NO_RIGHT`. A contract test fails the build when an operation in `api.yaml` has no declared capability area or right.

### Session line, menu and versions

- `scopeLine` is built from the role name and `default_scope` label, e.g. "Case owner. Scope: own cases."; Thai follows DL10.
- The menu manifest maps each screen to its capability area from the screen inventory; the shell shows a screen only when the session's permissions carry R for that area.
- `matrixVersion` and `conflictVersion` are fixed at sign-in. A new version applies to the next session only; an open session is never re-resolved.
- The AC-SIGN or AC-DENY event is written through `AccessEventPublisher` before the response; if the ACE audit path is unavailable the sign-in fails with 503 MSG-GEN-006 rather than proceeding unlogged.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| Any bank user | Sign-in with a role | Own session |
| RW-SECADM | Maintain groups and the IAM link (bank IAM); receives conflict incidents | All |
| RW-REFADM | Load role and group mapping versions; approves none | All |
| RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Platform administration R (`GET /admin/roles`) | All |
| SY-RULES and other service identities | Their own role row | All |

Every endpoint is checked by Spring Security method security plus `AccessCheckInterceptor`. Service identities use managed identity and are subject to the same role letters, not the human MFA check.

### Observability and operations

- Events: AC-SIGN and AC-DENY to the ACE audit and SOC log through INT-22; no field values.
- Metrics: sign-ins, refusals by reason, conflict incidents, unmapped groups, access-check denials by area.
- Alerts: a spike in ROLE_CONFLICT or NO_MFA; ACE sign-in unavailable.
- Run book: sign-in failure triage, group mapping check, conflict table version check.

### Observability, operations and performance

- Events: AC-SIGN and AC-DENY to the ACE audit and SOC log through INT-22; no field values.
- Metrics: sign-ins, refusals by reason, conflict incidents, unmapped groups, access-check denials by area.
- Alerts: a spike in ROLE_CONFLICT or NO_MFA; ACE sign-in unavailable.
- Run book: sign-in failure triage, group mapping check, conflict table version check.
- Session resolution is one indexed query on `role.entra_group` plus one on `role_conflict`; matrix rows are cached by version. Access checks are in-memory; no database call per request. Target 21 requests/second peak (NFR-RWB-002).

### Feature flag and rollback

- `rwb.access.sso-roles`. Off: the ACE common module's existing role check applies; the session endpoint, banner and menu filter are not enabled.
- Rollback: turn the flag off and redeploy the previous tag; the `role_conflict` migration is additive and remains harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-022-01 | AC1, BR1 | System | U-1001 in `RWB-SIT-RW-CASEOWN` with MFA | Roles RW-CASEOWN; scope OWN; PM-2026.11; scope line; no Administration menu |
| TC-E1-022-02 | AC2, BR4 | System | U-1002 holding RW-PHONECOL only | 403 MSG-P4-002 action "read roles"; one refusal event |
| TC-E1-022-03 | AC3, BR1 | System | U-1003 with no `RWB-SIT-` group | 401 MSG-P4-001; no data; NO_ROLE event |
| TC-E1-022-04 | AC4, BR2 | System | Token `amr = pwd` | 401 MSG-P4-005; NO_MFA event |
| TC-E1-022-05 | AC5, BR3 | System | U-1005 in RW-LITOFF and RW-LEGAL | Documents `CRUA`; no other permission |
| TC-E1-022-06 | AC6, BR5 | System | U-1006 in RW-SECADM and RW-CASEOWN | MSG-P4-006; incident; ROLE_CONFLICT event |
| TC-E1-022-07 | AC7, BR6 | System | Managed identity SY-RULES | 403 MSG-P4-002; event with user SY-RULES |
| TC-E1-022-08 | AC8, BR8 | System | U-1008 in one mapped and one unmapped group | Only RW-CASEOWN; unmapped group on the sign-in event |
| TC-E1-022-09 | AC9, BR7 | System | PM-2026.11 then PM-2026.12 one hour later | Open session allowed; new session refused |
| TC-E1-022-10 | X1, X5 | Security | Role without the right; service identity without the right | 403; nothing changes |
| TC-E1-022-11 | BR3, BR4 | Unit | Every letter and dash across two roles | Union correct; dash denies |
| TC-E1-022-12 | BR5 | Unit | Conflict row one way; `ANY_BUSINESS_ROLE` | Both directions refused; class match correct |

## Guardrails

- No role, group, letter, scope or conflict is written in code; all are rows with a version.
- No personal data in events, logs, tests or prompts; the actor is the Entra object ID, never a name or e-mail.
- No local password, local account or role cache that outlives the session.
- Every endpoint declares its capability area and right; an endpoint without one fails the contract test.
- No module reads `role`, `permission` or `role_conflict` directly.

## Out of scope

- Permission matrix load, PDPA masking, scope filtering and leaver handling (RWB-E1-037).
- Writing access events to the decision log and break-glass (RWB-E1-039).
- Partner identities through the external gateway (RWB-E2-019).
- Full administration screens SCR-43 (Epic 8, FEAT-ADM-01); the request, approval and grant steps run in the bank IAM.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-001 | Is the session path `/me/session` or `/api/recovery/v1/me/session`? | Wrong path breaks the shell. | The API base path applies: `GET /api/recovery/v1/me/session` (API-P4-012). | RESOLVED | SPEC-001, SPEC-008 |
| CLAR-002 | BR2, AC7; SPEC-002, SPEC-010 | Does the MFA check apply to service identities? | A service token normally has no `amr`; applying BR2 would block every job. | No. AC7 expects a 403 role refusal, not a 401 MFA refusal; NFR-051 applies role checks to service identities. The MFA check applies to `BANK_USER` roles only. | RESOLVED | SPEC-002, SPEC-010 |
| CLAR-003 | BR5, AC6; SPEC-004 | Is the conflict check symmetric when the table lists one direction? | A one-way row would let a pair through. | Check both directions; the loader stores the pair as written and the resolver tests both. | RESOLVED | SPEC-004, SPEC-011 |
| CLAR-004 | AC1; SPEC-008 | `GET /me/session` does not return the letters the menu needs. | The shell cannot filter the menu without reading the matrix table, which it must not do. | Add an additive `permissions` array (`capabilityArea`, `letters`) to `Session`; record it in the additions file. | RESOLVED | SPEC-008 |
| CLAR-005 | §9; SPEC-015 | How long does a session last? | Determines when versions are re-resolved. | The ACE token lifetime and sign-out govern; the Workbench adds no timeout. | RESOLVED | SPEC-015 |
| CLAR-006 | X2, X6; SPEC-003 | What if the token has no `groups` claim? | Same path as no role. | Treat as no group: 401 MSG-P4-001, NO_ROLE. | RESOLVED | SPEC-003 |
| CLAR-007 | AC3; SPEC-003 | Is the `RWB-SIT-` prefix authoritative or is `role.entra_group`? | A prefix rule would hard-code an environment convention. | `role.entra_group` is authoritative; the prefix is the naming pattern from the Single sign-on sheet (DL40). | RESOLVED | SPEC-003 |
| CLAR-008 | Contract; SPEC-009 | Is `GET /admin/roles` delivered in this story? | It is the endpoint AC2 uses to show a refusal. | Yes; API-P4-007 is first in E1 and the story contract defines its response. | RESOLVED | SPEC-009 |
| CLAR-009 | AC1; SPEC-008 | Is the scope line free text? | Label consistency and Thai. | Built from role name and `default_scope` labels; Thai per DL10. | RESOLVED | SPEC-008 |
| CLAR-010 | BR7; SPEC-006 | Which matrix version does an open session use? | Determines AC9. | The version resolved at sign-in; the next session uses the new one. | RESOLVED | SPEC-006 |

`CLARIFICATION_STATUS: RESOLVED` — all 10 items are answered from the story, the API specification, the permission matrix or the decision log. CLAR-002 and CLAR-004 are design resolutions with a named owner in the compliance review.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; local screen inventory, design system and label standard used.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SSO/MFA session and access-check capability; two P4 endpoints; two shell components; additive permissions field on Session.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first delivery of the session and role-list endpoints plus shell components]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 9 acceptance criteria, 7 exception paths and 5 session states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
