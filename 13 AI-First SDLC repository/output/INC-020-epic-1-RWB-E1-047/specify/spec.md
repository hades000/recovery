# Technical Specification — RWB-E1-047 Feature flags for module release with a removal date

| Field | Value |
|---|---|
| Story | RWB-E1-047 — Feature flags for module release with a removal date |
| Epic / module | E1 / P2 Integration |
| RUN_ID | `INC-020-epic-1-RWB-E1-047` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 047 Feature flags for module release with a removal date v1.md`; REQ-DRI-010; BRD Epic 1 §3.2; BRD Program §5.7 |
| Upstream IDs | REQ-DRI-010; FEAT-CWC-26; ADR-008; DT02; DT11; DL11; DL37; SCR-02; RWB-E1-002 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Platform administrator; Product Owner (TBC); see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — the SCR-02 Case list queue column is rendered through `FlagGate`; the column appears or disappears after a page reload without a deployment. No new screen. |
| Logic In Scope | `YES` — flag creation and change validation, per-environment value resolution, 30-second cache, off-by-default fallback, weekly removal report. |
| API In Scope | `YES` — four new E1 endpoints: `GET /feature-flags`, `GET /admin/feature-flags`, `POST /admin/feature-flags`, `PATCH /admin/feature-flags/{flagKey}`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `feature_flag` (new); `feature_flag_change` (new); SCR-02 Case list; ACE audit log; ACE notification path; `rwb.environment` property. |
| New Nodes Required | `YES` — `FeatureFlagController`; `FeatureFlagService`; `FeatureFlagsImpl`; two repositories/entities; `FlagRemovalReportJob`; `useFeatureFlag`; `FlagGate`. |
| Inherited Existing Behavior | Recovery schema (RWB-E1-001); SCR-02 case list and queue column (RWB-E1-002); ACE audit log; ACE notification path; sign-in and roles (RWB-E1-022); permission matrix (RWB-E1-037). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Unfinished work is behind a flag; a flag that is off returns the previous code path. | SPEC-RWB-E1-047-003, SPEC-RWB-E1-047-013 | DIRECT | `isOn` false; the old component path renders. | COVERED |
| BR2 | Every flag has a key, an owner, a value per environment (DEV, SIT, UAT, PROD) and a removal date. | SPEC-RWB-E1-047-001, SPEC-RWB-E1-047-002 | DIRECT | `feature_flag` columns; `removal_date` not null. | COVERED |
| BR3 | A flag value changes without a code release; each change is logged with user, time and reason. | SPEC-RWB-E1-047-005, SPEC-RWB-E1-047-006 | DIRECT | `feature_flag_change`; ACE audit. | COVERED |
| BR4 | A flag past its removal date is reported to its owner every week until it is removed. | SPEC-RWB-E1-047-007 | DIRECT | Monday 08:00 job; MSG-P2-003 per flag. | COVERED |
| BR5 | An unknown key or an unreadable store gives off, never on. | SPEC-RWB-E1-047-004 | DIRECT | Unknown → false + warning; store failure → cache or false. | COVERED |
| BR6 | Flag keys follow `rwb.<module>.<short-name>`. | SPEC-RWB-E1-047-001 | DIRECT | Check constraint `^rwb\.[a-z0-9]+\.[a-z0-9-]+$`. | COVERED |
| AC1 | With no UAT value, `isOn` returns false and SCR-02 hides the queue column. | SPEC-RWB-E1-047-003, SPEC-RWB-E1-047-014 | DIRECT | Default off; `FlagGate` renders the old path. | COVERED |
| AC2 | A platform administrator switches the flag on in UAT with a reason at 10:15; the page reloads at 10:16 and shows the column; a change row and ACE audit hold the change. | SPEC-RWB-E1-047-005, SPEC-RWB-E1-047-006, SPEC-RWB-E1-047-012 | DIRECT | No deployment; 30-second cache. | COVERED |
| AC3 | A flag with removal date 2026-11-30 and owner P5 is listed on Monday 2026-12-07 as 7 days overdue with MSG-P2-003; a 2027-01-31 flag is not listed. | SPEC-RWB-E1-047-007 | DIRECT | `daysOverdue`; active flags only. | COVERED |
| AC4 | Creating a flag with a past removal date returns 422 MSG-GEN-003; no date returns 422 MSG-GEN-001. | SPEC-RWB-E1-047-002, SPEC-RWB-E1-047-010 | DIRECT | Validation before insert. | COVERED |
| AC5 | A change with an empty reason returns 422 MSG-GEN-001 and the flag stays off. | SPEC-RWB-E1-047-005, SPEC-RWB-E1-047-011 | DIRECT | No change row on rejection. | COVERED |
| AC6 | An unknown key in code returns false and logs a warning with the key and no user data. | SPEC-RWB-E1-047-004 | DIRECT | Warning only; no PII. | COVERED |
| AC7 | With the store unavailable, the cached value is used; after a restart with no cache it returns false. | SPEC-RWB-E1-047-004 | DIRECT | Cache-first; off on cold start. | COVERED |
| AC8 | Two administrators change the same flag at version 4; one saves version 5, the other gets 409 MSG-GEN-004. | SPEC-RWB-E1-047-005 | DIRECT | `If-Match` version check. | COVERED |
| AC9 | A change to an unknown key returns 404 MSG-P2-016. | SPEC-RWB-E1-047-011 | DIRECT | Key lookup before validation. | COVERED |
| X1 | Removal date missing at creation. | SPEC-RWB-E1-047-002 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X2 | Removal date before today. | SPEC-RWB-E1-047-002 | DIRECT | 422 MSG-GEN-003. | COVERED |
| X3 | Change without a reason. | SPEC-RWB-E1-047-005 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X4 | Code asks for an unknown key. | SPEC-RWB-E1-047-004 | DIRECT | False; warning. | COVERED |
| X5 | The flag store is unavailable. | SPEC-RWB-E1-047-004 | DIRECT | Cached value; false with no cache. | COVERED |
| X6 | Two administrators change the same flag at once. | SPEC-RWB-E1-047-005 | DIRECT | 409 MSG-GEN-004. | COVERED |
| X7 | A change to a key that does not exist. | SPEC-RWB-E1-047-011 | DIRECT | 404 MSG-P2-016. | COVERED |
| X8 | A role without the right changes a flag. | SPEC-RWB-E1-047-015 | DIRECT | 403 MSG-P4-002. | COVERED |
## User story intent interpretation
As a **platform administrator (RW-PLATADM)**, I want **a feature flag service with each flag held as data (key, owner, value per environment, removal date) and read by the service and the front end at run time**, so that **a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told**.

The story builds the flag service, its four endpoints, a weekly removal report and the React hook and gate. The reference use puts the SCR-02 queue column behind `rwb.casewf.case-list-queue-column`. The platform administrator switches a flag in one environment; the change is logged and audited; the page shows the new value on reload. A flag past its removal date is reported weekly until it is removed.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Page load (`GET /feature-flags`); administrator action on the four endpoints; weekly report job Monday 08:00 Asia/Bangkok. |
| Preconditions | RWB-E1-001 schema; the person holds RW-PLATADM in the environment through Entra ID; ACE audit log available; the ACE front end loads the recovery module; reference flag `rwb.casewf.case-list-queue-column` created with default off and removal date 2027-01-31. |
| Input | `feature_flag` and `feature_flag_change` rows; `rwb.environment`; flag request/change payloads. |
| Output | Effective flag values; change rows; ACE audit entries; weekly report emails; MSG-P2-003 per overdue flag. |
| Feature flag | None on the flag service itself; it ships switched on. The reference use is gated by `rwb.casewf.case-list-queue-column`. |
## Field-level behaviour matrix
| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `feature_flag` | `flag_key` | Request | Create only | `^rwb\.[a-z0-9]+\.[a-z0-9-]+$`; unique |
| `feature_flag` | `description` | Request | Editable by create | Required; no personal data |
| `feature_flag` | `owner_user_id`, `owner_team` | Request | Create | Owner required; team optional |
| `feature_flag` | `default_on` | Request | Create | Every environment starts at this value |
| `feature_flag` | `dev_on`, `sit_on`, `uat_on`, `prod_on` | Default | Change per environment | Boolean; never null |
| `feature_flag` | `removal_date` | Request | Create | Required; not before today |
| `feature_flag` | `is_active` | True | Retire | Retired flags are not reported |
| `feature_flag_change` | `environment`, `old_value`, `new_value`, `reason` | Change request | Append only | Reason required; environment in LOV-ENVIRONMENT |
| `feature_flag_change` | `created_by`, `created_at` | Session | Append only | User ID, never a name |
| `FeatureFlagValue` | `key`, `value` | Effective value | Read-only | Value for the caller's environment |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Flag absent | Create | Valid key, owner and removal date | Flag active, all environments at default | 201; no change row |
| Flag off | Change to on | Reason present; version matches | Flag on in that environment | Change row; ACE audit; page shows after reload |
| Flag on | Change to off | Reason present; version matches | Flag off | Change row; ACE audit; previous code path |
| Flag active | Retire | `is_active = false` | Retired | No longer reported; no delete |
| Flag overdue | Weekly report | Removal date before today | Reported | MSG-P2-003; email to owner and RW-PLATADM |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Removal date missing | Refused; no flag | 422 MSG-GEN-001 |
| X2 | Removal date before today | Refused | 422 MSG-GEN-003 |
| X3 | Change without reason | Refused; flag unchanged | 422 MSG-GEN-001 |
| X4 | Unknown key in code | False; warning with key only | Application log |
| X5 | Flag store unavailable | Cached value; false with no cache | None |
| X6 | Two changes at once | One saves; other refused | 409 MSG-GEN-004 |
| X7 | Change to unknown key | Refused | 404 MSG-P2-016 |
| X8 | Role without Platform administration U | 403; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/feature-flags` (any signed-in role, session check only); `GET /api/recovery/v1/admin/feature-flags` (Platform administration R); `POST /api/recovery/v1/admin/feature-flags` (C); `PATCH /api/recovery/v1/admin/feature-flags/{flagKey}` (U). |
| Contract delta | `FeatureFlagValue[]` for the read (the front end builds a map); `FeatureFlag` with per-environment values, owner, removal date, `daysOverdue` and `version`; `FeatureFlagRequest`; `FeatureFlagChange` with environment, value and reason. The PATCH requires `If-Match` with the version — the OpenAPI file must declare it. |
| Backward compatibility | New endpoints; no existing operation changes. |
| Authorization | Session for the read; Platform administration R/C/U for the admin operations; 403 MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P2-016; 409 MSG-GEN-004; 422 MSG-GEN-001/003; 503. |
| Versioning | No version change; all four operations are first in E1. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | AC1, AC2; SPEC-RWB-E1-047-012..014 | New `useFeatureFlag` hook and `FlagGate`; SCR-02 column visibility changes. | Hook returns on/off from the payload; `FlagGate` hides and shows its child; loading and error paths; no deployment path. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR6; SPEC-RWB-E1-047-001..020 | New entities, service, cache, four endpoints and the weekly job. | Create/change validation; key pattern; per-environment resolution; cache hit/miss/store failure; unknown key; version conflict; report selection; audit. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `FeatureFlagController` | Controller | Four endpoints; validation; Problem responses. |
| `FeatureFlagService` | Service | Create, change and retire; version check; change row; ACE audit call. |
| `FeatureFlagsImpl` | Published interface | `isOn(key)` with a 30-second cache per key; environment from `rwb.environment`. |
| `FeatureFlagRepository`, `FeatureFlagChangeRepository` | Repository | The two flag tables only. |
| `FeatureFlag`, `FeatureFlagChange` | Entity | JPA entities with the standard columns. |
| `FlagRemovalReportJob` | Job | Weekly report, Monday 08:00. |
| `useFeatureFlag` | React hook | Reads `GET /feature-flags` once per page load; returns the value for a key. |
| `FlagGate` | React component | Renders children only when the flag is on; otherwise the previous path. |

### Data and migration
Flyway `V2026_11_47__p2_feature_flags.sql` creates `feature_flag` (primary key `flag_key`, check on the key pattern, `removal_date` not null, one boolean per environment) and `feature_flag_change` (index on `flag_key`, `created_at`). No hard-coded flag values; rows are created through the endpoints.

### Rules
1. Create validates key pattern, owner, default and removal date (not before today); writes every environment at the default.
2. `isOn` resolves the caller's environment from `rwb.environment`; a missing row or an unreadable store returns false; a cached value is used before the store.
3. The cache refreshes every `rwb.flags.cache-seconds` (30, DL11) per key.
4. Change validates reason and version; writes the change row, updates the environment value, and writes the ACE audit entry in one transaction.
5. Setting the value it already has writes no change row and returns the flag.
6. The weekly job selects active flags with `removal_date < today`, computes `daysOverdue`, sends one email per owner and one to the RW-PLATADM group, and logs MSG-P2-003 per flag.
7. The report is idempotent by report date; a rerun sends nothing new.

### Transaction and events
Create and change are one transaction each: flag row, change row and audit call. A failed audit rolls back the change. No application event is published. The weekly report is idempotent by report date.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration CRUD | All |
| RW-SECADM | Platform administration CRUDA | All |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Platform administration R | All |
| RW-TRIBE | Receives the report as owner; no change right | Own |
| Every signed-in role | Reads effective values | Own environment |

Every endpoint has a method check; the client hides what the role cannot use, but hiding is not the control.

### Observability and operations
- Metrics: flag reads, cache hits/misses, store failures, changes, overdue flags.
- Alerts: flag store unavailable; report job failure.
- Logs: change with key, environment and user ID (no name); unknown key warning with key only.
- Run book: the weekly report job follows the RWB-E1-056 format.

### Performance
- `isOn` is served from an in-memory cache; a miss reads one row by primary key.
- `GET /feature-flags` returns the environment's values in one query; no N+1.
- Screen response target is under 2 seconds at P95 (NFR-008); the flag read is part of page load.

### Feature flag and rollback
The flag service ships switched on. The reference use `rwb.casewf.case-list-queue-column` is off by default. Rollback: switch the reference flag off (previous column path); the flag tables and endpoints remain. The migration is forward-only and additive.

### UI behaviour (SCR-02)
The queue column exists from RWB-E1-002; RWB-E1-031 adds filters. `FlagGate` wraps the column; with the flag off the column is absent, with it on the column renders after reload. No new screen; design evidence is the SCR-02 screen specification and the local prototype, not Figma.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-047-01 | AC1, BR1, BR5 | System | Flag off, no UAT value | `isOn` false; column hidden |
| TC-E1-047-02 | AC2, BR3 | System | Flag switched on in UAT at 10:15 with reason | Column shows at 10:16; change row; audit |
| TC-E1-047-03 | AC3, BR4 | System | Two flags, one overdue | Overdue listed with owner and 7 days; other not listed; MSG-P2-003 |
| TC-E1-047-04 | AC4, BR2 | System | Past date and empty date | 422 MSG-GEN-003 / MSG-GEN-001; no flag |
| TC-E1-047-05 | AC5, BR3 | System | Empty reason | 422 MSG-GEN-001; flag stays off |
| TC-E1-047-06 | AC6, BR5 | System | Unknown key | False; warning with key only |
| TC-E1-047-07 | AC7, BR5 | Resilience | Flag table unreadable | Cached true; after restart false |
| TC-E1-047-08 | AC8 | System | Two changes at version 4 | One version 5; other 409 MSG-GEN-004 |
| TC-E1-047-09 | AC9 | System | Change to `rwb.p9.unknown` | 404 MSG-P2-016 |
| TC-E1-047-10 | X8 | Security | RW-CASEOWN calls PATCH | 403; MSG-P4-002 |
| TC-E1-047-11 | BR1, BR3 | Unit | Hook and gate; cache hit/miss/failure | On/off render; cache fallback; no change row on same value |
## Guardrails
- No business value in code: flag values, owners and dates are rows; code holds only the key.
- No personal data in logs, tests or prompts; the change log holds user IDs, never names.
- No read of another module's tables; other modules call `FeatureFlags.isOn`.
- Every flag that is off runs the previous code path; a test covers both paths of every flag.
## Out of scope
- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04.
- The queue write flag for models and agents: RWB-E2-036.
- Retiring a flag through an endpoint: no E1 operation; `is_active` is set through the admin data path and the E8 screen.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Configuration changed without a code release | Program §5.7; Epic 1 §3.2 | FEAT-CWC-26 | All recovery processes | None | TC-E1-047-01..09, 11 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1; SPEC-003 | AC1 says "no value set for UAT", but `uat_on` is not null. | A null state would contradict the table. | "No value set" means the flag was created with the default off, so `uat_on = false`; every environment always has a value. | RESOLVED | SPEC-003 |
| CLAR-002 | §12; SPEC-008 | The story says `GET /feature-flags` returns a map; the API specification returns `FeatureFlagValue[]`. | The response shape is a contract. | The API specification wins: return the array; `useFeatureFlag` builds the map. | RESOLVED | SPEC-008 |
| CLAR-003 | §4; SPEC-004 | The 30-second cache interval is assumed (DL11). | Determines how long a change takes to appear. | 30 seconds via `rwb.flags.cache-seconds`; the value is configuration. | RESOLVED | SPEC-004 |
| CLAR-004 | §10; SPEC-017 | The authority says RW-PLATADM retires flags, but no endpoint retires one. | A missing operation would block retirement. | Retirement is `is_active = false` through the admin data path; the E8 screen exposes it. E1 does not add a retire endpoint. | RESOLVED | SPEC-017 |
| CLAR-005 | AC1; SPEC-014 | Which story supplies the SCR-02 queue column? | Determines whether the reference use can ship. | The column exists from RWB-E1-002; RWB-E1-031 adds filters. `FlagGate` wraps the existing column. | RESOLVED | SPEC-014 |
| CLAR-006 | AC3; SPEC-007 | `daysOverdue` is not a stored field. | The report needs a value. | Computed as report date minus `removal_date`; the API returns it. | RESOLVED | SPEC-007 |
| CLAR-007 | §12; SPEC-011 | `If-Match` is required by the PATCH but not declared in the OpenAPI file. | A contract delta is needed. | Add the required `If-Match` header to the PATCH operation; a missing or stale value returns 409 MSG-GEN-004. | RESOLVED | SPEC-011 |
| CLAR-008 | §4; SPEC-004 | Which environment does the caller read? | Determines the value returned. | `rwb.environment` (DEV, SIT, UAT, PROD) per deployment. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all eight items are answered from the story, the API specification or the data model.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP source; design evidence is the local SCR-02 specification and prototype.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New feature-flag service, four E1 endpoints, weekly removal report and the SCR-02 column gate.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new flag capability, four endpoints and a screen visibility change]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 9 acceptance criteria, 8 exception paths and 6 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
