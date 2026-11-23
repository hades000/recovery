# RWB-PLT-E1047-APP Feature flags for module release with a removal date

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-047 for the platform shared libraries. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1047-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-047 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-PLT-LIB-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1047-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018) |
| Status | Draft (realignment v1) |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a feature flag library embedded in every service, with each flag held as data (key, owner, value per environment, removal date) in one platform-owned store, the surface published once for the front end and the admin console, and read in process at run time**, so that **a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told**.

The legacy story was one module inside the monolith. The D-RCV-60 split keeps the behaviour and moves the ownership, in the terms of Template and Rules §R6:

- **Stays with the platform library (PLT), schema owned by PLT:** the tables `feature_flag` and `feature_flag_change`, the `FeatureFlags` interface, the per-service cache and the weekly removal report. The library is embedded in every service, as Architecture v5 Text Extract v1 slide 20 puts every service on the service template and the shared libraries (DP-01). No service reads another service's tables; the library reads only its own store.
- **Served once, not nineteen times:** the four documented operations are served by rwb-integration (P2) against the library, under the Ownership Map ruling that keeps the flags with PLT and lets P2 serve the HTTP surface. The library has no service short, so the four paths carry no service segment (ASM-2463).
- **Consumed from rwb-case (P3):** the environment codes (DEV, SIT, UAT, PROD) and the owner-team codes are reference data, read through the reference-data client library (DP-07; build dependency RWB-PLT-E1043-CON; contract dependency RWB-P3-E1043-CON).
- **Scheduled, not Quartz:** the legacy weekly Quartz job becomes a Temporal Schedule through the workflow kit (DP-10; build dependency RWB-PLT-E1071-CON). No shared Quartz table is used.
- **Named by the naming library:** flag keys follow `rwb.<module>.<short-name>` and topic names are fixed by the naming library (DP-14; build dependency RWB-PLT-E1047-CON).
- **Migrated per service:** the platform store follows the per-service Flyway sequence (DP-15; build dependency RWB-PLT-E1044-CON). The store and its schema name come from RWB-PLT-DB and are Not specified in the source documents (GAP-1411; ASM-2462).
- **Screens:** through the gateway-bff composite route (DP-19; build dependency RWB-PLT-N001-CON). The flag admin screen is SCR-44 of Epic 8 and is out of scope here.
- **No event of its own:** the library publishes no business event and owns no topic. Flag values are data, never code.

### 2. Business rationale

Two squads release monthly from one repository, and one squad's unfinished change must not hold the other's release (ADR-008, DT11). A flag held as a data row lets the platform administrator switch a change off in SIT or UAT and let the release go ahead, with every change logged. A weekly report lists flags past their removal date so old code paths are removed. It meets REQ-DRI-010 (configuration changed without a code release).

The realignment changes where the flag is read, not what a flag is. In the monolith every module read the flag through an in-process interface and one module owned the two tables; in the target the same interface ships as a platform library inside all nineteen services, so a flag read is still local and free of a network hop, while the store, the change history and the removal report are owned once by the platform. Publishing the surface once, against the library, keeps the front end and the admin console on one contract instead of nineteen copies. The removal date keeps its purpose: a flag that outlives its date is a code path nobody removes, and the weekly report is the only thing that makes the date real.

### 3. Preconditions

- RWB-PLT-E1047-CON is published on Day 1: the flag-key schema, the change-row schema, the `FeatureFlags` interface with its off-by-default rule, the four documented operations with their problem details and the `Idempotency-Key` rule, the weekly removal report input and output, and the contract fake. This story builds against the fake from Day 1 (DP-11).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are in place (DP-07): the environment and owner-team codes are read through the reference-data client library from rwb-case `GET /api/recovery/case/v1/admin/lists/{listCode}`, one hop, 2 s timeout.
- RWB-PLT-E1071-CON is in place (DP-10): the workflow kit provides the Schedule template, and the weekly report runs as a Temporal Schedule in namespace `rwb-recovery`.
- RWB-PLT-E1044-CON is in place (DP-15): the store is created on the per-service Flyway sequence. The store, its schema name and the deployment of the admin component are Not specified in the source documents (GAP-1411; ASM-2462).
- RWB-PLT-N001-CON is in place (DP-19): the gateway-bff composite route carries the flag reads of the staff screens.
- The four paths sit at v1 with no service segment and exactly as the Ownership Map names them (ASM-2463).
- The person holds RW-PLATADM in the environment through the Entra ID group, for example RWB-UAT-RW-PLATADM.
- The ACE audit log service of the common module is available (Architecture v5 Text Extract v1 slide 30).
- The ACE front end loads the recovery module folder (ADR-006).
- Flag `rwb.casewf.case-list-queue-column` is created with default off and removal date 2027-01-31 for the tests.
- No approval is needed to start: the story is Draft (realignment v1), has only contract build dependencies and therefore starts on Day 1.

### 4. Flow

1. Platform administrator: creates a flag with key, description, owner, default value and removal date through `POST /admin/feature-flags`, served by rwb-integration against the library.
2. System: validates the key pattern `rwb.<module>.<short-name>`, the removal date and the owner, and writes the flag row with every environment set to the default.
3. Service code: calls FeatureFlags.isOn(key) at each request; the value comes from the service-local cache of the library, refreshed every 30 seconds (assumed; DL11), and the interval is a chart value, never a code constant (ASM-2464).
4. Front end: reads GET /feature-flags at page load through the gateway-bff composite route and hides or shows the component.
5. Platform administrator: switches the flag on for one environment with a reason through `PATCH /admin/feature-flags/{flagKey}` and `If-Match` with the version.
6. System: checks the version, writes the new value and a feature_flag_change row with user, time, old and new value, and writes the ACE audit log entry.
7. Front end: after reload, shows the component; no deployment takes place.
8. The Temporal Schedule `Flag removal report` runs every Monday 08:00 Asia/Bangkok with overlap SKIP (the legacy weekly Quartz job; DP-10) and lists every flag past its removal date with its owner.
9. System: sends the report to each owner and to the RW-PLATADM group by email through the ACE notification path and logs MSG-P2-003 per flag.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Removal date missing at creation | Refused; no flag is created | MSG-GEN-001 | AC4 |
| X2 | Removal date before today | Refused | MSG-GEN-003 | AC4 |
| X3 | Change without a reason | Refused | MSG-GEN-001 | AC5 |
| X4 | Code asks for a key that does not exist | Returns off, the old code path runs, a warning is logged | None | AC6 |
| X5 | The flag store is unavailable | The last cached value is used; with no cached value the flag is off | None | AC7 |
| X6 | Two administrators change the same flag at once | The second change is refused | MSG-GEN-004 | AC8 |
| X7 | A change to a key that does not exist | Refused | MSG-P2-016 | AC9 |
| X8 | A role without the right changes a flag | Refused; nothing changes | MSG-P4-002 | TC-E1-047-10 |

X1 to X8 keep the legacy triggers and messages character for character. The store being unavailable at start is X5 and is answered by the library, not by a service: there is no second owner to call and no service-wide outage to declare.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One library, two tables in one platform-owned store, one published interface, one Schedule; every later service uses it |
| Negotiable | Flags, owners, values and dates are data rows; the cache interval is a chart value and the key pattern is configuration of the naming library |
| Valuable | A failed change is switched off in SIT or UAT and the release goes ahead, in every service at once |
| Estimable | Two tables, one library with a cache, four documented operations, one weekly Schedule, one React hook |
| Small | Within two weeks with its tests, against the contract fake |
| Testable | Each criterion below is one automated test, and the legacy test cases are carried with their IDs |

### 7. Acceptance criteria

```gherkin
Feature: Feature flags for module release with a removal date

  Background:
    Given flag "rwb.casewf.case-list-queue-column" exists with default off, owner team "P3 squad" and removal date 2027-01-31

  Scenario: AC1 Flag off by default (legacy RWB-E1-047 AC1)
    Given the flag has no value set for UAT
    When the case list service starts in UAT
    Then FeatureFlags.isOn("rwb.casewf.case-list-queue-column") returns false
    Then the system hides the queue column on SCR-02 Case list

  Scenario: AC2 Flag switched on (legacy RWB-E1-047 AC2)
    Given the platform library contract mock returns the FeatureFlag and FeatureFlagChange schemas for flag "rwb.casewf.case-list-queue-column"
    Given a platform administrator sets the flag to on in UAT with reason "UAT test of queue column" at 10:15
    When the case list page is reloaded at 10:16
    Then the queue column shows without a deployment
    Then a change row holds environment "UAT", old value off, new value on, the user and the time 10:15
    Then the ACE audit log holds the same change

  Scenario: AC3 Flag expiry (legacy RWB-E1-047 AC3)
    Given flag "rwb.p5.ocr-intake" has removal date 2026-11-30 and owner team "P5 squad"
    Given today is Monday 2026-12-07
    When the weekly flag report runs at 08:00
    Then the system lists the flag for removal with its owner and 7 days past its removal date
    Then the report carries message MSG-P2-003 for the flag
    Then the system does not list flag "rwb.casewf.case-list-queue-column" with removal date 2027-01-31

  Scenario: AC4 Removal date checked at creation (legacy RWB-E1-047 AC4)
    Given the platform library contract mock returns 422 with message MSG-GEN-003 for a removal date before today
    Given today is 2026-11-16
    When a platform administrator creates flag "rwb.p6.line-dispatch" with removal date 2026-11-10
    Then the system does not creat the flag
    Then the response is 422 with message MSG-GEN-003
    Then a creation with no removal date returns 422 with message MSG-GEN-001

  Scenario: AC5 Change without a reason refused (legacy RWB-E1-047 AC5)
    Given the platform library contract mock returns 422 with message MSG-GEN-001 for an empty reason
    When a platform administrator sets the flag to on in SIT with an empty reason
    Then the response is 422 with message MSG-GEN-001
    Then the flag stays off in SIT

  Scenario: AC6 Unknown key in code (legacy RWB-E1-047 AC6)
    When code calls FeatureFlags.isOn("rwb.casewf.not-defined")
    Then the result is false
    Then a warning with the key and no user data is written to the application log

  Scenario: AC7 Flag store unavailable (legacy RWB-E1-047 AC7)
    Given the flag is on in UAT and the cache holds the value from 10:20
    When the flag table cannot be read at 10:21
    Then FeatureFlags.isOn returns true from the cache
    Then after a restart with the table still unavailable it returns false

  Scenario: AC8 Two changes at once (legacy RWB-E1-047 AC8)
    Given the platform library contract mock returns the FeatureFlag schema with version 4 for flag "rwb.casewf.case-list-queue-column"
    Given two platform administrators read the flag at version 4
    When both send a change with If-Match version 4
    Then the system saves one change with version 5
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC9 Change to a key that does not exist (legacy RWB-E1-047 AC9)
    Given the platform library contract mock returns 404 with message MSG-P2-016 for an unknown flag key
    When a platform administrator sends a change for flag "rwb.p9.unknown"
    Then the response is 404 with message MSG-P2-016
```

AC1 to AC9 are the legacy criteria of RWB-E1-047, character for character, including the legacy wording of AC4. The only addition is one first Given in each criterion whose step crosses the published contract, so the criterion can run against the contract fake on Day 1; every value, flag key, date, version, message ID and the times 10:15 and 10:16 are unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Unfinished work is behind a flag; a flag that is off returns the previous code path | DT11; ADR-008 |
| BR2 | Every flag has a key, an owner, a value per environment (DEV, SIT, UAT, PROD) and a removal date | Reference tables: Feature flags, Configuration |
| BR3 | A flag value changes without a code release, and each change is logged with user, time and reason | REQ-DRI-010; DT02 |
| BR4 | A flag past its removal date is reported to its owner every week until it is removed | ADR-008 consequences |
| BR5 | An unknown key or an unreadable store gives off, never on | DT11 |
| BR6 | Flag keys follow `rwb.<module>.<short-name>` | Story brief format, section 13 |

The rules are data and library behaviour, not service code: BR2 is the two tables, BR3 is the change row and the ACE audit call, BR4 is the weekly Schedule, BR5 is the off-by-default rule of the interface, and BR6 is enforced by the naming library (DP-14), so a key that breaks the pattern never reaches the store.

### 9. State transitions

None. This story does not change a case status. It changes the value of a flag per environment (off to on, on to off) and the flag's is_active column when a flag is retired. The value per environment is the only state the library caches, and the cache holds the last read value per key, never a computed value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Creates flags, changes values, retires flags (Platform administration, CRUD) |
| RW-SECADM, security administrator | Reads and changes flags (Platform administration, CRUDA) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read flags and their change history (Platform administration, R) |
| RW-TRIBE, tribe lead and squad members | Receive the weekly report as flag owners; no change right |
| Every signed-in Workbench role | Reads the effective values through GET /feature-flags |

The role codes are resolved by rwb-access (P4) at run time and appear here as codes only; the library stores user IDs and team codes, never a name.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-207 to DF-OPS-217 | feature_flag | all fields | Write |
| DF-OPS-209 | feature_flag | description | Write |
| DF-OPS-210 | feature_flag | owner_user_id | Write |
| DF-OPS-211 | feature_flag | owner_team | Write |
| DF-OPS-212 | feature_flag | default_on | Write |
| DF-OPS-213 | feature_flag | dev_on | Write |
| DF-OPS-214 | feature_flag | sit_on | Write |
| DF-OPS-215 | feature_flag | uat_on | Write |
| DF-OPS-216 | feature_flag | prod_on | Write |
| DF-OPS-217 | feature_flag | removal_date | Write |
| DF-OPS-218 to DF-OPS-223 | feature_flag_change | all fields | Write |
| DF-OPS-219 | feature_flag_change | flag_key | Write |
| DF-OPS-220 | feature_flag_change | environment | Write |
| DF-OPS-221 | feature_flag_change | old_value | Write |
| DF-OPS-222 | feature_flag_change | new_value | Write |
| DF-OPS-223 | feature_flag_change | reason | Write |
| Standard column | feature_flag_change | created_by | Write |
| Standard column | feature_flag_change | created_at | Write |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The two tables are PLT-owned (Ownership Map) and sit in the platform store, whose schema name is Not specified in the source documents (GAP-1411; ASM-2462). `role_code` is read from rwb-access over its contract, never from a table of another service (DP-01). The environment and owner-team codes are reference data of rwb-case and arrive through the reference-data contract (DP-07).

### 12. Contract

**12.1 REST operations provided**

| Operation | Served by | Request | Responses | Owner |
|---|---|---|---|---|
| GET /feature-flags | rwb-integration (P2) against the platform library | None | 200 map of flag key to boolean for the caller's environment; 401 no session (MSG-P4-001) | PLT |
| GET /admin/feature-flags | rwb-integration (P2) against the platform library | Query: overdue, owner (the legacy operation names the query `?overdue=true`); the FeatureFlag array is paged | 200 array of FeatureFlag: key, description, ownerTeam, values per environment, removalDate, daysOverdue, version; 401; 403 (MSG-P4-002) | PLT |
| POST /admin/feature-flags | rwb-integration (P2) against the platform library | FeatureFlagRequest: key, description, ownerUserId, ownerTeam, defaultOn, removalDate; `Idempotency-Key` | 201 FeatureFlag; 401; 403 (MSG-P4-002); 409 key exists (MSG-GEN-004); 422 field missing or date in the past (MSG-GEN-001, MSG-GEN-003) | PLT |
| PATCH /admin/feature-flags/{flagKey} | rwb-integration (P2) against the platform library | FeatureFlagChange: environment, value, reason; header If-Match with the version | 200 FeatureFlag; 401; 403 (MSG-P4-002); 404 unknown key (MSG-P2-016); 409 version changed (MSG-GEN-004); 422 reason empty (MSG-GEN-001) | PLT |

The four paths are exactly the four operations of the Ownership Map, at v1 and with no service segment (ASM-2463). The library has no service short, so it declares no REST base of its own; rwb-integration serves these paths against the library and adds no field of its own. The interface itself is published in the client library, not over HTTP:

```java
public interface FeatureFlags {
    boolean isOn(String flagKey); // false for an unknown key or an unreadable store with no cached value
}
```

**12.2 REST operations consumed**

| Operation | Provider | Why this story needs it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | rwb-case (P3) | The environment codes DEV, SIT, UAT, PROD and the owner-team codes are reference data; the store holds codes and the codes are read through the client library, one hop, 2 s timeout | DP-07, DP-11 |

**12.3 Events published**

None. The library publishes no business event. The topic naming it fixes for the rest of the platform comes from the naming library (DP-14; build dependency RWB-PLT-E1047-CON), and the flag values never travel in an event.

**12.4 Events consumed**

None. The library consumes no event; a change reaches the other services through the cache refresh, not through a topic.

**12.5 Workflows and activities**

None. The weekly report is a Temporal Schedule, not a workflow, and no activity is declared here. The library has no service short, so it declares no Temporal task queue of its own; the Schedule runs on the workflow kit (DP-10; build dependency RWB-PLT-E1071-CON).

**12.6 Schedules**

| Schedule | When | Overlap policy | Owner | What it does |
|---|---|---|---|---|
| Flag removal report | Monday 08:00 Asia/Bangkok | SKIP | PLT | Lists every active flag whose removal date is before today with its owner and days overdue, sends the report to each owner and to the RW-PLATADM group, and logs MSG-P2-003 per flag; the idempotency key is the report date, so a rerun on the same date sends nothing new |

The legacy Quartz trigger becomes this Temporal Schedule (DP-10). JOB-11 is not involved: the report writes no event.

**12.7 Tables owned**

| Table | Key and indexes | Owner | Schema | Rows exposed |
|---|---|---|---|---|
| feature_flag | Primary key flag_key; check constraint on the key pattern `^rwb\.[a-z0-9]+\.[a-z0-9-]+$`; removal_date not null; is_active | PLT | Not specified in the source documents (GAP-1411; ASM-2462) | GET /feature-flags; GET /admin/feature-flags; the weekly report |
| feature_flag_change | Index on flag_key and changed_at; created_by and created_at | PLT | Not specified in the source documents (GAP-1411; ASM-2462) | GET /admin/feature-flags change history; GET /admin/feature-flags with overdue |

Both tables are PLT-owned in the Ownership Map and sit in the platform-owned store, whose schema name comes from RWB-PLT-DB and is Not specified in the source documents (GAP-1411; ASM-2462). The store is created on the per-service Flyway sequence (DP-15; build dependency RWB-PLT-E1044-CON). This story adds no table outside the platform store and reads no table of another service (DP-01).

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| Platform library contract fake (RWB-PLT-E1047-CON) | The four documented operations, the flag-key schema, the change-row schema and the examples of the `FeatureFlags` interface | This story, rwb-integration's admin component and every service that reads a flag |
| ACE audit fake (ACE Common) | The audit write of a flag change | AC2 and AC8 |
| ACE notification fake (ACE Common) | The weekly email to each owner and to the RW-PLATADM group | AC3 and TC-E1-047-03 |
| rwb-case reference-data fake (P3) | `GET /api/recovery/case/v1/admin/lists/{listCode}` for the environment and owner-team codes | The store validation and the admin component |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations, at v1 with no service segment, served by rwb-integration against the library | 1 operation (the rwb-case reference-data read) | OpenAPI 3.1, one hop, 2 s timeout, `Idempotency-Key` on POST, `If-Match` on PATCH, errors as problem details |
| Kafka | 0 | 0 | No topic and no event of its own; the naming library fixes the topic names of the platform |
| Temporal | 1 Schedule (Flag removal report) | 0 | Namespace `rwb-recovery`, overlap SKIP, no task queue of its own |
| File | 0 | 0 | The report is an email through the ACE notification path, not a file |

### 13. Solution plan

**Hardware and software change.** The library is embedded in every service (Architecture v5 Text Extract v1 slide 20): each service carries the library as a build dependency and reads a flag in process, so no service makes a network hop to read a flag and the nineteen deployments share one implementation instead of nineteen copies. One PLT-owned admin component stores the flags in one platform-owned store, so the two tables exist once and not once per service. P2 rwb-integration serves the HTTP surface against the library under the Ownership Map ruling, so the four paths are published once for the front end and the admin console. The weekly report becomes a Temporal Schedule on the workflow kit instead of a Quartz job on a shared scheduler (DP-10). Flag values are data, never code: a value change is a row change, and no deployment, migration or restart is needed for a value to take effect.

| Component | Type | Responsibility |
|---|---|---|
| FeatureFlagController (in rwb-integration) | Controller | The four operations; validation; problem responses |
| FeatureFlagService | Service | Create, change and retire; version check; change row; ACE audit call |
| FeatureFlagsImpl | Published interface | isOn with a service-local cache refreshed every 30 seconds; environment from the property `rwb.environment` |
| FeatureFlagRepository, FeatureFlagChangeRepository | Repository | The two PLT tables only |
| FeatureFlag, FeatureFlagChange | Entity | Entities with the standard columns |
| FlagRemovalReportSchedule | Temporal Schedule | Weekly report on the workflow kit |
| useFeatureFlag | React hook | Reads GET /feature-flags once per page load and returns the value for a key |
| FlagGate | React component | Renders its children only when the flag is on |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The rows are the Template and Rules §R5.5 rows, character for character. Read for this story: DP-01 gives the PLT-owned store, and no service reads another service's tables; DP-07 reads the environment and owner-team codes through the reference-data client library; DP-10 turns the weekly Quartz job into a Temporal Schedule; DP-11 is the published `FeatureFlags` interface with its contract fake, one hop and 2 s timeout for the one consumed read; DP-14 is the naming library for the `rwb.<module>.<short-name>` flag keys and the topic names; DP-15 is the per-service Flyway sequence for the store; DP-19 is the gateway-bff composite route for the future admin screen of SCR-44.

**Store and configuration**

- Migration: one migration on the per-service Flyway sequence creating `feature_flag` (primary key flag_key, the key-pattern check constraint, removal_date not null) and `feature_flag_change` (index on flag_key and changed_at). The store, its schema name and the deployment of the admin component are Not specified in the source documents (GAP-1411; ASM-2462).
- Property `rwb.environment` (DEV, SIT, UAT, PROD) per deployment.
- Property `rwb.flags.cache-seconds` = 30 (assumed; DL11), held as a chart value and never as a code constant (ASM-2464).
- Flag rows are created through the endpoints by RW-PLATADM.

**Build steps**

1. Write the migration, the entities and the repositories with repository tests.
2. Build FeatureFlagService with key, date and reason validation and the version check.
3. Build FeatureFlagsImpl with the service-local cache and the off-by-default rules for unknown keys and store failure.
4. Build the four operations in rwb-integration against the library, with the access check, the `Idempotency-Key` rule and the ACE audit write, tested against the contract fake.
5. Build useFeatureFlag and FlagGate with a component test that hides and shows a child.
6. Build FlagRemovalReportSchedule on the workflow kit with the email through the ACE notification path for staff.
7. Put the case list queue column behind `rwb.casewf.case-list-queue-column` as the reference use.
8. Run the contract test of RWB-PLT-E1047-CON in the build, so the library, the surface and the fake cannot drift.

- **Feature flag:** none. This story builds the flag library, which ships switched on.
- **Done when:** the tests in section 16 pass and the reference flag hides and shows the queue column in UAT without a deployment.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Removal date or change reason empty | Enter {field}. |
| MSG-GEN-003 | Removal date before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version changed between read and write | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Flag created or changed | Saved. |
| MSG-P2-003 | Weekly report, flag past its removal date | Flag {flag} passed its removal date on {date}. Owner: {owner}. Remove the flag and its old code path. |
| MSG-P2-016 | Change to a key that does not exist | Flag {flag} does not exist. |
| MSG-P4-002 | A role without the right changes a flag | You cannot {action} here. Your role does not include it. |

The message IDs and texts are the legacy ones, character for character, and every service that raises one raises it with the same HTTP status: MSG-GEN-001 and MSG-GEN-003 as 422, MSG-GEN-004 as 409, MSG-P2-016 as 404 and MSG-P4-002 as 403. MSG-GEN-005 is the success notice.

### 15. Screens and states

No screen in this story. The platform administrator uses the four operations through the admin console API client; the flag list screen comes with SCR-44 in Epic 8 and is out of scope here. The business user sees the queue column on SCR-02 Case list appear or disappear after a reload, which is the visible state of the flag: on shows the column, off hides it, and the removal date eventually removes both.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-047-01 | AC1, BR1, BR5 | Component | Flag with default off, no UAT value |
| TC-E1-047-02 | AC2, BR3 | Component | Flag switched on in UAT with a reason |
| TC-E1-047-03 | AC3, BR4 | Component | Two flags, one past its removal date |
| TC-E1-047-04 | AC4, BR2 | Component | Removal date 2026-11-10 and an empty removal date |
| TC-E1-047-05 | AC5, BR3 | Component | Change with an empty reason |
| TC-E1-047-06 | AC6, BR5 | Component | Unknown key |
| TC-E1-047-07 | AC7, BR5 | NFR | Flag table made unreadable |
| TC-E1-047-08 | AC8 | Component | Two changes with If-Match version 4 |
| TC-E1-047-09 | AC9 | Component | Change to an unknown key |
| TC-E1-047-10 | Access | Component | RW-CASEOWN calls PATCH /admin/feature-flags/{flagKey}; refused with MSG-P4-002 |

The legacy test case IDs are kept. The legacy level column mapped to the four levels of this template: an Access test is a Component test, a System test is a Component test, and the Resilience test is an NFR test. The full test, with its Given, When and Then, is in the legacy test case workbook, tab Story test cases, under the same test case ID; the ten tests run against the contract fake and, from the moment the store exists, against the store.

### 17. Guardrails

- No business value in code: flag values, owners and dates are rows; code holds only the key. The cache interval is a chart value (ASM-2464).
- No personal data in logs, tests or prompts; the change log holds user IDs and team codes, never names.
- No read of another service's tables (DP-01); the environment and owner-team codes come through the rwb-case reference-data contract (DP-07), and the role codes through rwb-access.
- Every flag that is off runs the previous code path; a test covers both paths of every flag.
- The four paths are published once, with no service segment, and no service copies them (ASM-2463).
- The report is a Schedule with overlap SKIP; a rerun on the same report date sends nothing new and writes nothing twice.
- The store schema is not invented: until RWB-PLT-DB names it, the story carries the placeholder and the gap.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Configuration changed without a code release | Program 5.7; Epic 1 3.2 | FEAT-CWC-26 | All recovery processes | None | TC-E1-047-01 to TC-E1-047-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1047-CON | Contract | H: the published flag-key and change-row schemas, the interface, the four operations and the fake |
| RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: reference-data client library, workflow kit Schedule, per-service Flyway, gateway-bff composite route |
| RWB-P3-E1043-CON | Contract | C: the rwb-case reference-data contract this story reads for the environment and owner-team codes |
| RWB-E2-036 | App development | The queue write flag for models and agents, a different legacy key |
| SCR-44 (Epic 8) | Screen | The admin flag screen, out of scope here |

### 19. Out of scope

- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04.
- The queue write flag for models and agents: RWB-E2-036.
- The service-specific implementation of the flag reads (the reference use on the case list queue column is RWB-SVC-P3 work) and the 19 service stories that consume the library.
- The store provisioning itself: it belongs to RWB-PLT-DB and the per-service DB stories.
- Any event, topic or workflow of the library: it has none by design.
