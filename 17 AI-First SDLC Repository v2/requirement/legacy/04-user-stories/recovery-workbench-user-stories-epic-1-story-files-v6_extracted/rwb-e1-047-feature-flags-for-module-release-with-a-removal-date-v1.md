<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 047 Feature flags for module release with a removal date v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 047 Feature flags for module release with a removal date v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-047 Feature flags for module release with a removal date

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-047 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | FEAT-CWC-26 Control module release with dated feature flags |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.7 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a feature flag service with each flag held as data (key, owner, value per environment, removal date) and read by the service and the front end at run time**, so that **a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told**.

## 2. Business rationale

Two squads release monthly from one repository, and one squad's unfinished change must not hold the other's release (ADR-008, DT11). A flag held as a data row lets the platform administrator switch a change off in SIT or UAT and let the release go ahead, with every change logged. A weekly report lists flags past their removal date so old code paths are removed. It meets REQ-DRI-010 (configuration changed without a code release).

## 3. Preconditions

- RWB-E1-001 (recovery schema) is done.
- The person holds RW-PLATADM in the environment through the Entra ID group, for example RWB-UAT-RW-PLATADM.
- The ACE audit log service of the common module is available.
- The ACE front end loads the recovery module folder (ADR-006).
- Flag `rwb.casewf.case-list-queue-column` is created with default off and removal date 2027-01-31 for the tests.

## 4. Flow

1. Platform administrator: creates a flag with key, description, owner, default value and removal date.
2. System: validates the key pattern `rwb.<module>.<short-name>`, the removal date and the owner, and writes the flag row with every environment set to the default.
3. Service code: calls FeatureFlags.isOn(key) at each request; the value comes from a cache refreshed every 30 seconds (assumed; DL11).
4. Front end: reads GET /feature-flags at page load and hides or shows the component.
5. Platform administrator: switches the flag on for one environment with a reason.
6. System: checks the version, writes the new value and a feature_flag_change row with user, time, old and new value, and writes the ACE audit log entry.
7. Front end: after reload, shows the component; no deployment takes place.
8. Scheduler: the weekly flag report job runs every Monday 08:00 and lists every flag past its removal date with its owner.
9. System: sends the report to each owner and to the RW-PLATADM group by email and logs MSG-P2-003 per flag.

## 5. Exception paths

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

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the schema; every later story uses it |
| Negotiable | Flags, owners, values and dates are data rows; the cache interval is a property |
| Valuable | A failed change is switched off in SIT or UAT and the release goes ahead |
| Estimable | Two tables, one service with a cache, four endpoints, one weekly job, one React hook |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Feature flags for module release with a removal date

  Background:
    Given flag "rwb.casewf.case-list-queue-column" exists with default off, owner team "P3 squad" and removal date 2027-01-31

  Scenario: AC1 Flag off by default
    Given the flag has no value set for UAT
    When the case list service starts in UAT
    Then FeatureFlags.isOn("rwb.casewf.case-list-queue-column") returns false
    Then the system hides the queue column on SCR-02 Case list

  Scenario: AC2 Flag switched on
    Given a platform administrator sets the flag to on in UAT with reason "UAT test of queue column" at 10:15
    When the case list page is reloaded at 10:16
    Then the queue column shows without a deployment
    Then a change row holds environment "UAT", old value off, new value on, the user and the time 10:15
    Then the ACE audit log holds the same change

  Scenario: AC3 Flag expiry
    Given flag "rwb.p5.ocr-intake" has removal date 2026-11-30 and owner team "P5 squad"
    Given today is Monday 2026-12-07
    When the weekly flag report runs at 08:00
    Then the system lists the flag for removal with its owner and 7 days past its removal date
    Then the report carries message MSG-P2-003 for the flag
    Then the system does not list flag "rwb.casewf.case-list-queue-column" with removal date 2027-01-31

  Scenario: AC4 Removal date checked at creation
    Given today is 2026-11-16
    When a platform administrator creates flag "rwb.p6.line-dispatch" with removal date 2026-11-10
    Then the system does not creat the flag
    Then the response is 422 with message MSG-GEN-003
    Then a creation with no removal date returns 422 with message MSG-GEN-001

  Scenario: AC5 Change without a reason refused
    When a platform administrator sets the flag to on in SIT with an empty reason
    Then the response is 422 with message MSG-GEN-001
    Then the flag stays off in SIT

  Scenario: AC6 Unknown key in code
    When code calls FeatureFlags.isOn("rwb.casewf.not-defined")
    Then the result is false
    Then a warning with the key and no user data is written to the application log

  Scenario: AC7 Flag store unavailable
    Given the flag is on in UAT and the cache holds the value from 10:20
    When the flag table cannot be read at 10:21
    Then FeatureFlags.isOn returns true from the cache
    Then after a restart with the table still unavailable it returns false

  Scenario: AC8 Two changes at once
    Given two platform administrators read the flag at version 4
    When both send a change with If-Match version 4
    Then the system saves one change with version 5
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC9 Change to a key that does not exist
    When a platform administrator sends a change for flag "rwb.p9.unknown"
    Then the response is 404 with message MSG-P2-016
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Unfinished work is behind a flag; a flag that is off returns the previous code path | DT11; ADR-008 |
| BR2 | Every flag has a key, an owner, a value per environment (DEV, SIT, UAT, PROD) and a removal date | Reference tables: Feature flags, Configuration |
| BR3 | A flag value changes without a code release, and each change is logged with user, time and reason | REQ-DRI-010; DT02 |
| BR4 | A flag past its removal date is reported to its owner every week until it is removed | ADR-008 consequences |
| BR5 | An unknown key or an unreadable store gives off, never on | DT11 |
| BR6 | Flag keys follow `rwb.<module>.<short-name>` | Story brief format, section 13 |

## 9. State transitions

None. This story does not change a case status. It changes the value of a flag per environment (off to on, on to off) and the flag's is_active column when a flag is retired.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Creates flags, changes values, retires flags (Platform administration, CRUD) |
| RW-SECADM, security administrator | Reads and changes flags (Platform administration, CRUDA) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read flags and their change history (Platform administration, R) |
| RW-TRIBE, tribe lead and squad members | Receive the weekly report as flag owners; no change right |
| Every signed-in Workbench role | Reads the effective values through GET /feature-flags |

## 11. Data

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

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

All endpoints are new and recorded in the additions file.

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /feature-flags | None | Map of flag key to boolean for the caller's environment | 401 no session (MSG-P4-001) | Any signed-in Workbench role (session check only) | Read only |
| GET /admin/feature-flags?overdue=true | Query: overdue, owner | Array of FeatureFlag: key, description, ownerTeam, values per environment, removalDate, daysOverdue, version | 401; 403 (MSG-P4-002) | Platform administration, R | Read only |
| POST /admin/feature-flags | FeatureFlagRequest: key, description, ownerUserId, ownerTeam, defaultOn, removalDate | 201 FeatureFlag | 401; 403 (MSG-P4-002); 409 key exists (MSG-GEN-004); 422 field missing or date in the past (MSG-GEN-001, MSG-GEN-003) | Platform administration, C | The key is unique; a repeat returns 409 |
| PATCH /admin/feature-flags/{flagKey} | FeatureFlagChange: environment, value, reason; header If-Match with the version | 200 FeatureFlag | 401; 403 (MSG-P4-002); 404 unknown key (MSG-P2-016); 409 version changed (MSG-GEN-004); 422 reason empty (MSG-GEN-001) | Platform administration, U | Setting the value it already has writes no change row |

**Job: weekly flag report (new, recorded in additions).** Trigger: Quartz, Monday 08:00 Asia/Bangkok. Input: feature_flag rows with is_active true and removal_date before today. Output: one email per owner and one to the RW-PLATADM group, one log line with MSG-P2-003 per flag. Events: none. Idempotency key: report date; a rerun on the same date sends nothing new. Restart: rerun from the start.

**Published interface (package recovery.integration.flags.api).**

```java
public interface FeatureFlags {
    boolean isOn(String flagKey); // false for an unknown key or an unreadable store with no cached value
}
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/flags`, Java package `recovery.integration.flags`; front end folder `src/modules/recovery/flags`.

| Component | Type | Responsibility |
|---|---|---|
| FeatureFlagController | Controller | The four endpoints; validation; problem responses |
| FeatureFlagService | Service | Create, change and retire; version check; change row; ACE audit call |
| FeatureFlagsImpl | Published interface | isOn with a 30-second cache per key; environment from property `rwb.environment` |
| FeatureFlagRepository, FeatureFlagChangeRepository | Repository | The two flag tables only |
| FeatureFlag, FeatureFlagChange | Entity | JPA entities with the standard columns |
| FlagRemovalReportJob | Job | Weekly report |
| useFeatureFlag | React component | Hook that reads GET /feature-flags once per page load and returns the value for a key |
| FlagGate | React component | Renders its children only when the flag is on |

- **Database:** Flyway migration `V2026_11_47__p2_feature_flags.sql` creates feature_flag (primary key flag_key, check constraint on the key pattern `^rwb\.[a-z0-9]+\.[a-z0-9-]+$`, removal_date not null) and feature_flag_change (index on flag_key, changed_at).
- **Configuration and reference data:** property `rwb.environment` (DEV, SIT, UAT, PROD) per deployment; property `rwb.flags.cache-seconds` = 30 (assumed; DL11). Flag rows are created through the endpoints by RW-PLATADM.
- **Build steps:**
  1. Write the migration, entities and repositories with repository tests.
  2. Build FeatureFlagService with key, date and reason validation and the version check.
  3. Build FeatureFlagsImpl with the cache and the off-by-default rules for unknown keys and store failure.
  4. Build the four endpoints with the access check and the ACE audit write.
  5. Build useFeatureFlag and FlagGate with a component test that hides and shows a child.
  6. Build FlagRemovalReportJob with the email through the ACE notification path for staff.
  7. Put the case list queue column behind `rwb.casewf.case-list-queue-column` as the reference use.
- **Feature flag:** none. This story builds the flag service, which ships switched on.
- **Done when:** the tests in section 16 pass and the reference flag hides and shows the queue column in UAT without a deployment.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Removal date or change reason empty | Enter {field}. |
| MSG-GEN-003 | Removal date before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version changed between read and write | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Flag created or changed | Saved. |
| MSG-P2-003 | Weekly report, flag past its removal date | Flag {flag} passed its removal date on {date}. Owner: {owner}. Remove the flag and its old code path. |
| MSG-P2-016 | Change to a key that does not exist | Flag {flag} does not exist. |
| MSG-P4-002 | A role without the right changes a flag | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The platform administrator uses the four endpoints through the ACE admin console API client; the flag list screen comes with SCR-44 in Epic 8. The business user sees the queue column on SCR-02 Case list appear or disappear after reload.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-047-01 | AC1, BR1, BR5 | System | Flag with default off, no UAT value |
| TC-E1-047-02 | AC2, BR3 | System | Flag switched on in UAT with a reason |
| TC-E1-047-03 | AC3, BR4 | System | Two flags, one past its removal date |
| TC-E1-047-04 | AC4, BR2 | System | Removal date 2026-11-10 and an empty removal date |
| TC-E1-047-05 | AC5, BR3 | System | Change with an empty reason |
| TC-E1-047-06 | AC6, BR5 | System | Unknown key |
| TC-E1-047-07 | AC7, BR5 | Resilience | Flag table made unreadable |
| TC-E1-047-08 | AC8 | System | Two changes with If-Match version 4 |
| TC-E1-047-09 | AC9 | System | Change to an unknown key |
| TC-E1-047-10 | Access | Access | RW-CASEOWN calls PATCH /admin/feature-flags/{flagKey}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: flag values, owners and dates are rows; code holds only the key.
- No personal data in logs, tests or prompts; the change log holds user IDs, never names.
- No read of another module's tables; other modules call FeatureFlags.isOn.
- Every flag that is off runs the previous code path; a test covers both paths of every flag.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Configuration changed without a code release | Program 5.7; Epic 1 3.2 | FEAT-CWC-26 | All recovery processes | None | TC-E1-047-01 to TC-E1-047-09 |

## 19. Out of scope

- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04.
- The queue write flag for models and agents: RWB-E2-036.
