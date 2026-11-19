# Increment Card — INC-016-epic-1-RWB-E1-047

**RWB-E1-047 — Feature flags for module release with a removal date**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-016` |
| Title | Feature flags for module release with a removal date |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-047` |
| RUN_ID | `INC-016-epic-1-RWB-E1-047` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | User story |
| Priority | Should |
| Build order | 16 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P2 Integration.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **a feature flag service with each flag held as data (key, owner, value per environment, removal date) and read by the service and the front end at run time**, so that **a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told**.

**Business outcome:** Two squads release monthly from one repository, and one squad's unfinished change must not hold the other's release (ADR-008, DT11). A flag held as a data row lets the platform administrator switch a change off in SIT or UAT and let the release go ahead, with every change logged. A weekly report lists flags past their removal date so old code paths are removed. It meets REQ-DRI-010 (configuration changed without a code release).

**Main flow:**
1. Platform administrator: creates a flag with key, description, owner, default value and removal date.
2. System: validates the key pattern `rwb.<module>.<short-name>`, the removal date and the owner, and writes the flag row with every environment set to the default.
3. Service code: calls FeatureFlags.isOn(key) at each request; the value comes from a cache refreshed every 30 seconds (assumed; DL11).
4. Front end: reads GET /feature-flags at page load and hides or shows the component.
5. Platform administrator: switches the flag on for one environment with a reason.
6. System: checks the version, writes the new value and a feature_flag_change row with user, time, old and new value, and writes the ACE audit log entry.

**Acceptance criteria:**
- AC1: Flag off by default
- AC2: Flag switched on
- AC3: Flag expiry
- AC4: Removal date checked at creation
- AC5: Change without a reason refused
- AC6: Unknown key in code
- AC7: Flag store unavailable
- AC8: Two changes at once
- AC9: Change to a key that does not exist

**Out of scope:**
- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04.
- The queue write flag for models and agents: RWB-E2-036.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-047-feature-flags-for-module-release-with-a-removal-date-v1.md` |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.7 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Creates flags, changes values, retires flags (Platform administration, CRUD) |
| RW-SECADM, security administrator | Reads and changes flags (Platform administration, CRUDA) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read flags and their change history (Platform administration, R) |
| RW-TRIBE, tribe lead and squad members | Receive the weekly report as flag owners; no change right |
| Every signed-in Workbench role | Reads the effective values through GET /feature-flags |

## Contract extract

All endpoints are new and recorded in the additions file. | Method and path | Request | Response | Errors | Authorization | Idempotency | |---|---|---|---|---|---| | GET /feature-flags | None | Map of flag key to boolean for the caller's environment | 401 no session (MSG-P4-001) | Any signed-in Workbench role (session check only) | Read only | | GET /admin/feature-flags?overdue=true | Query: overdue, owner | Array of FeatureFlag: key, description, ownerTeam, values per environment, removalDate, daysOverdue, version | 401; 403 (MSG-P4-002) | Platform administration, R | Read only | | POST /admin/feature-flags | FeatureFlagRequest: key, description, ownerUserId, ownerTeam, defaultOn, removalDate | 201 FeatureFlag | 401; 403 (MSG-P4-002); 409 key exists (MSG-GEN-004); 422 field missing or date in the past (MSG-GEN-001, MSG-GEN-003) | Platform administration, C | The key is unique; a repeat…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: flag values, owners and dates are rows; code holds only the key. - No personal data in logs, tests or prompts; the change log holds user IDs, never names. - No read of another module's tables; other modules call FeatureFlags.isOn. - Every flag that is off runs the previous code path; a test covers both paths of every flag.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-047-feature-flags-for-module-release-with-a-removal-date-v1.md` |
| Specification | `output/INC-016-epic-1-RWB-E1-047/specify/spec.md` |
| Compliance validation | `output/INC-016-epic-1-RWB-E1-047/specify/compliance-validation.md` |
| Agent run log | `output/INC-016-epic-1-RWB-E1-047/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-016-epic-1-RWB-E1-047/plan/` |
| Implementation evidence | `output/INC-016-epic-1-RWB-E1-047/implement/` |
| API / functional test reports | `output/INC-016-epic-1-RWB-E1-047/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-016-epic-1-RWB-E1-047/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-047-feature-flags-for-module-release-with-a-removal-date-v1.md` |
| Output run | `output/INC-016-epic-1-RWB-E1-047/` |

