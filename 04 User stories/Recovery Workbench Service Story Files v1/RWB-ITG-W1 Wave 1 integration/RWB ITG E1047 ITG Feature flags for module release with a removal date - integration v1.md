# RWB-ITG-E1047-ITG Feature flags for module release with a removal date

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1047-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-047 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1001-APP, RWB-PLT-E1047-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-047 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-047 feature-flag behaviour between the platform library (PLT, the flag tables and the four operations), P3 rwb-case (a wave-1 consumer that hides and shows the queue column) and P1 rwb-source-data (a second wave-1 consumer)**, so that **a flag release, a flag change without deployment and the removal-date report are proved on the real services before wave 1 exits**.

### 2. Business rationale

The legacy story puts the flag tables in module P2 Integration with a Quartz weekly report. The target keeps the tables and the four operations with the platform library (Ownership Map: feature_flag and feature_flag_change owner PLT; GET /feature-flags, GET /admin/feature-flags, POST /admin/feature-flags and PATCH /admin/feature-flags/{flagKey} owner PLT), runs the weekly report as a Temporal Schedule (DP-10) and uses the naming library for topics and event names (DP-14). The sources name neither the platform base that serves the four flag operations nor the Schedule identifier of the weekly report: Not specified in the source documents (GAP-0361; ASM-0473).

The business case of the legacy story is unchanged. Two squads release monthly from one repository, and one squad's unfinished change must not hold the other's release (REQ-DRI-010, ADR-008, DT11 and DT02). A flag held as a data row lets the platform administrator switch a change off in SIT or UAT and let the release go ahead, with every change logged, and a weekly report lists the flags past their removal date so the old code paths are removed. The rule that unfinished work sits behind a flag, and that a flag which is off runs the previous code path, is carried over unchanged (BR1).

The target split for the legacy key is therefore: PLT owns the two flag tables, the four flag operations, the cache behind FeatureFlags.isOn and the weekly removal report Schedule; P3 rwb-case owns the case list and is the wave-1 consumer that hides and shows the queue column; P1 rwb-source-data is the second wave-1 consumer that proves a value change is seen without a deployment. This story is the integration proof across those three owners.

No service contract is faked. The suite exercises the published wave-1 contracts of the platform library and of the two consumers, and it reads and changes flags only through the four operations of section 12.2. Where the sources name no platform base and no Schedule identifier, the suite asserts through the published operations and records the open point as GAP-0361 and ASM-0473.

### 3. Preconditions

- RWB-PLT-E1047-APP is done: the two flag tables, the four flag operations, the cache and the weekly removal report Schedule are in SIT and UAT on the platform library.
- RWB-P1-E1001-APP is done: rwb-source-data reads the effective flag values through the platform operations and is a wave-1 consumer of the flag.
- The four flag operations are deployed and reached through gateway-bff, one hop from the caller.
- A wave-1 consumer reads GET /feature-flags at request time and hides or shows its component from the value.
- Flag `rwb.casewf.case-list-queue-column` exists with default off, owner team P3 squad and removal date 2027-01-31.
- Flag `rwb.p5.ocr-intake` carries removal date 2026-11-30 and owner team P5 squad.
- The SIT and UAT clock can be set to Monday 2026-12-07, and to 2026-11-16 for the creation checks.
- The ACE notification path for staff mail is available to the weekly report.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- The story has no build dependency and is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic flag rows and the two consumer fixtures of the harness; no production data is used.
2. Harness: reads the flag through GET /feature-flags in UAT and records the effective value of `rwb.casewf.case-list-queue-column` with no value set for UAT.
3. Harness: switches the flag on at 10:15 with the reason `UAT test of queue column` through PATCH /admin/feature-flags/{flagKey} with If-Match, and records the status and the message.
4. Harness: reloads the case list at 10:16, reads the change row through GET /admin/feature-flags and asserts the environment UAT, old value off, new value on, the user id and the time 10:15; it reads the same change in the ACE audit log.
5. Harness: reads the value in a second service within 30 seconds of the change and asserts that rwb-source-data sees on with no deployment.
6. Harness: sets the clock to Monday 2026-12-07 and fires the weekly report Schedule at 08:00.
7. Harness: reads the report and asserts that `rwb.p5.ocr-intake` with removal date 2026-11-30 is listed with owner team P5 squad and 7 days past its removal date, carries MSG-P2-003, and that `rwb.casewf.case-list-queue-column` with removal date 2027-01-31 is not listed.
8. Harness: posts the negative cases — a removal date 2026-11-10 with today 2026-11-16, a creation with no removal date, an empty reason, an unknown key in code, an unreadable flag store, two changes at version 4, a change to `rwb.p9.unknown` and a change by a role without the right — and records every status and message.
9. Harness: asserts that the naming library refuses a topic or event name built from the legacy prefixes `rwb.p<n>.` and `rwb.casewf.`, and that every wave-1 topic resolves to the owner service's topic.
10. Harness: writes the evidence report with the per-scenario statuses, the messages, the change rows and the report lines, then removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Removal date missing at creation | Refused; no flag is created | MSG-GEN-001 | AC4 |
| X2 | Removal date before today | Refused; no flag is created | MSG-GEN-003 | AC4 |
| X3 | Change without a reason | Refused; the value stays as it was | MSG-GEN-001 | AC5 |
| X4 | Code asks for a key that does not exist | Returns off, the old code path runs, a warning is logged with the key and no user data | None | AC6 |
| X5 | The flag store is unavailable | The last cached value is used; with no cached value the flag is off | None | AC7 |
| X6 | Two administrators change the same flag at once | The second change is refused; the first is saved as the next version | MSG-GEN-004 | AC8 |
| X7 | A change to a key that does not exist | Refused; no change row is written | MSG-P2-016 | AC9 |
| X8 | A role without the platform administration right changes a flag | Refused; nothing changes | MSG-P4-002 | AC10 |
| X9 | A flag is still active past its removal date | Nothing is removed automatically; the weekly report lists the flag with its owner and writes one report line per flag | MSG-P2-003 | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs RWB-PLT-E1047-APP and RWB-P1-E1001-APP and the published operations, not their source code |
| Negotiable | The flag keys, owners, values and dates are data rows of the harness; the story fixes the assertions and the call set |
| Valuable | A flag release, a flag change without a deployment and the removal-date report are proved on real services before wave 1 exits |
| Estimable | One suite module, one flag fixture pack, one clock control, one cache-window assertion and one evidence report |
| Small | Eleven scenarios over the platform library and two consumers, with one Schedule; no service code and no schema change |
| Testable | Every scenario asserts a response, a change row, a report line or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Feature flags for module release with a removal date, end-to-end across wave 1 services

  Background:
    Given the platform library serves the four flag operations through gateway-bff and the wave 1 services rwb-case and rwb-source-data are deployed in SIT and UAT with their published contracts
    Given flag "rwb.casewf.case-list-queue-column" exists with default off, owner team "P3 squad" and removal date 2027-01-31
    Given no production data is used

  Scenario: AC1 The flag is off by default when a wave 1 service reads it (new, D-RCV-60)
    Given the flag has no value set for UAT
    When the case list service starts in UAT and reads GET /feature-flags
    Then FeatureFlags.isOn("rwb.casewf.case-list-queue-column") returns false
    Then the system hides the queue column on SCR-02 Case list

  Scenario: AC2 A flag switched on in one place is seen by a second service without a deployment (new, D-RCV-60)
    Given a platform administrator sets the flag to on in UAT with reason "UAT test of queue column" at 10:15
    When the case list page is reloaded at 10:16 and a second service reads GET /feature-flags
    Then the queue column shows without a deployment
    Then a change row holds environment "UAT", old value off, new value on, the user and the time 10:15
    Then the ACE audit log holds the same change
    Then the second service reads the new value within 30 seconds

  Scenario: AC3 The weekly removal report lists a flag past its removal date with its owner (new, D-RCV-60)
    Given flag "rwb.p5.ocr-intake" has removal date 2026-11-30 and owner team "P5 squad"
    Given today is Monday 2026-12-07
    When the weekly flag report runs at 08:00
    Then the system lists the flag for removal with its owner and 7 days past its removal date
    Then the report carries message MSG-P2-003 for the flag
    Then the system does not list flag "rwb.casewf.case-list-queue-column" with removal date 2027-01-31

  Scenario: AC4 A removal date in the past and a missing removal date are refused at creation (new, D-RCV-60)
    Given today is 2026-11-16
    When a platform administrator creates flag "rwb.p6.line-dispatch" with removal date 2026-11-10
    Then the system does not create the flag
    Then the response is 422 with message MSG-GEN-003
    Then a creation with no removal date returns 422 with message MSG-GEN-001

  Scenario: AC5 A change without a reason is refused (new, D-RCV-60)
    When a platform administrator sets the flag to on in SIT with an empty reason
    Then the response is 422 with message MSG-GEN-001
    Then the flag stays off in SIT

  Scenario: AC6 An unknown key read by code is off and logs a warning (new, D-RCV-60)
    When code calls FeatureFlags.isOn("rwb.casewf.not-defined")
    Then the result is false
    Then a warning with the key and no user data is written to the application log

  Scenario: AC7 An unavailable flag store falls back to the last cached value and then to off (new, D-RCV-60)
    Given the flag is on in UAT and the cache holds the value from 10:20
    When the flag table cannot be read at 10:21
    Then FeatureFlags.isOn returns true from the cache
    Then after a restart with the table still unavailable it returns false

  Scenario: AC8 Two changes at once leave one winner (new, D-RCV-60)
    Given two platform administrators read the flag at version 4
    When both send a change with If-Match version 4
    Then the system saves one change with version 5
    Then the system refuses the other with 409 and message MSG-GEN-004

  Scenario: AC9 A change to a key that does not exist returns not found (new, D-RCV-60)
    When a platform administrator sends a change for flag "rwb.p9.unknown"
    Then the response is 404 with message MSG-P2-016

  Scenario: AC10 A role without the platform administration right is refused (new, D-RCV-60)
    Given RW-CASEOWN holds a role without the platform administration right
    When RW-CASEOWN sends a change for the flag
    Then the response is 403 with message MSG-P4-002
    Then nothing changes

  Scenario: AC11 The naming library refuses a legacy topic name (new, D-RCV-60)
    Given a topic or event name built from the legacy prefixes rwb.p n dot or rwb.casewf dot
    When the name is validated by the naming library
    Then the name is refused
    Then every wave 1 topic resolves to the owner service's topic per the naming library
    Then no legacy topic is created (DP-14)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Unfinished work is behind a flag; a flag that is off returns the previous code path | RWB-E1-047 BR1; DT11; ADR-008 |
| BR2 | Every flag has a key, an owner, a value per environment (DEV, SIT, UAT, PROD) and a removal date | RWB-E1-047 BR2; Reference tables: Feature flags, Configuration |
| BR3 | A flag value changes without a code release, and each change is logged with user, time and reason | RWB-E1-047 BR3; REQ-DRI-010; DT02 |
| BR4 | A flag past its removal date is reported to its owner every week until it is removed | RWB-E1-047 BR4; ADR-008 consequences |
| BR5 | An unknown key or an unreadable store gives off, never on | RWB-E1-047 BR5; DT11 |
| BR6 | Flag keys follow the key pattern of the flag, with a module segment and a short name | RWB-E1-047 BR6 |
| BR7 | PLT owns feature_flag and feature_flag_change and the four flag operations; no other service holds a copy of the flag tables or writes them | Ownership Map tables and api rows; Template and Rules v1 §R3 default ruling |
| BR8 | The weekly removal report runs as a Temporal Schedule in the owning service; the shared Quartz tables are not used | DP-10; ASM-0474; Architecture v5 slide 44 |

### 9. State transitions

None for the case status: this story does not change a case status. It reads and changes the flag value of an environment, the flag state and the state of the weekly removal report.

| Object | State | Meaning |
|---|---|---|
| Flag value in an environment | Off | The value is off in this environment; the previous code path runs |
| Flag value in an environment | On | The value is on in this environment; the component is shown after reload, with no deployment |
| Flag | Active | The flag is read by the services and is listed by the weekly report when its removal date has passed |
| Flag | Retired | The flag and its old code path are removed; it is no longer read and no longer reported |
| Weekly removal report | Not due | No flag is past its removal date on the report date, or the report date has not arrived |
| Weekly removal report | Reported | The report ran on its date and listed every active flag past its removal date with its owner |

The suite sets the clock and the values; it does not change a case status.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures and the flag rows, reads the evidence report |
| RW-PLATADM, platform administrator | Creates flags, changes values with a reason and reads the change rows through the four operations |
| RW-SECADM, security administrator | Reads and changes flags through the same operations |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read the flags and their change history |
| RW-TRIBE, tribe lead and squad members | Receive the weekly report as flag owners; no change right |
| Every signed-in Workbench role | Reads the effective values through GET /feature-flags |

No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-207 to DF-OPS-217 | feature_flag (PLT platform library) | all fields | Write |
| DF-OPS-209 | feature_flag (PLT platform library) | description | Write |
| DF-OPS-210 | feature_flag (PLT platform library) | owner_user_id | Write |
| DF-OPS-211 | feature_flag (PLT platform library) | owner_team | Write |
| DF-OPS-212 | feature_flag (PLT platform library) | default_on | Write |
| DF-OPS-213 | feature_flag (PLT platform library) | dev_on | Write |
| DF-OPS-214 | feature_flag (PLT platform library) | sit_on | Write |
| DF-OPS-215 | feature_flag (PLT platform library) | uat_on | Write |
| DF-OPS-216 | feature_flag (PLT platform library) | prod_on | Write |
| DF-OPS-217 | feature_flag (PLT platform library) | removal_date | Write |
| DF-OPS-218 to DF-OPS-223 | feature_flag_change (PLT platform library) | all fields | Write |
| DF-OPS-219 | feature_flag_change (PLT platform library) | flag_key | Write |
| DF-OPS-220 | feature_flag_change (PLT platform library) | environment | Write |
| DF-OPS-221 | feature_flag_change (PLT platform library) | old_value | Write |
| DF-OPS-222 | feature_flag_change (PLT platform library) | new_value | Write |
| DF-OPS-223 | feature_flag_change (PLT platform library) | reason | Write |
| Standard column | feature_flag_change (PLT platform library) | created_by | Write |
| Standard column | feature_flag_change (PLT platform library) | created_at | Write |
| DF-REF-035 | role (P4 rwb-access) | role_code | Read |
| Platform base and Schedule identifier | feature_flag, feature_flag_change and the weekly removal report | Base path of the four flag operations and the Schedule id | Not specified in the source documents (GAP-0361; ASM-0473) |

Field IDs are those in the Logical Data Model and Data Dictionary. The legacy story marks the flag rows as a write from module P2 Integration; in this suite every read and every write goes through the four platform operations of section 12.2, and the suite owns no table. feature_flag and feature_flag_change are PLT tables (BR7). Every row in the suite is synthetic, and the four flag keys keep the legacy values (ASM-0475).

### 12. Contract

#### 12.1 REST operations provided

None. The pack provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /feature-flags | PLT platform library | Read the effective values of the caller's environment |
| GET /admin/feature-flags | PLT platform library | Read the flags with their owner, values, removal date and days overdue |
| POST /admin/feature-flags | PLT platform library | Create a flag with its key, owner, default and removal date |
| PATCH /admin/feature-flags/{flagKey} | PLT platform library | Change the value of an environment with a reason and If-Match |
| GET /api/recovery/case/v1/cases | P3 rwb-case | Read the case list of a consumer whose queue column is behind the flag |

The four flag operations are platform operations owned by PLT per the Ownership Map. They are reached through gateway-bff, and they are not served from one of the 19 service bases. Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The pack publishes no event.

#### 12.4 Events consumed

None. The pack consumes no event; the flag value is read through the operations of section 12.2.

#### 12.5 Workflows and activities

None. The weekly removal report is a Schedule (section 12.6) and the pack starts no workflow of its own.

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| Weekly flag report (legacy Quartz trigger, retired) | Weekly flag removal report | Monday 08:00 Asia/Bangkok | PLT platform library | The report under test; the legacy Quartz trigger is retired under DP-10 (ASM-0474) |

The Schedule runs in the platform library and writes one report line per flag past its removal date with MSG-P2-003, one mail per owner and one mail to the platform administration group. A rerun on the same report date sends nothing new.

#### 12.7 Tables owned

None (DP-01). feature_flag and feature_flag_change are PLT tables, read and written only through the operations of section 12.2.

#### 12.8 Contract fakes

No service contract is faked. The four flag operations are the platform library's own and every consumer read goes to the real service. The flag table read is stopped with a test-only switch agreed with the platform owner for AC7, and the Schedule is fired with a clock control.

| Control or stub | Use |
|---|---|
| Test-only flag store switch, agreed with the platform owner | Stops the flag table read for AC7 and restores it afterwards |
| Clock control for the report date | Sets Monday 2026-12-07 and 2026-11-16, and restores the clock |
| Synthetic flag and case fixtures of the harness RWB-ITG-W1J01-ITG | The flag rows, the owner teams and the case list under test |

#### 12.9 Call-type summary

| Call type | Provided by the pack | Consumed by the pack |
|---|---|---|
| REST | 0 | 5 |
| Kafka | 0 | 0 |
| Temporal | 0 | 1 Schedule (weekly flag removal report) |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eleven scenarios against SIT and UAT and holds no service code |
| Flag fixture pack | Test data | The flag rows, the owner teams, the removal dates and the case list of the two consumers |
| Clock control for the report date | Harness control | Sets Monday 2026-12-07 and 2026-11-16, fires the Schedule on the report date and restores the clock |
| Cache window assertion | Assertion | Asserts that the second consumer reads the new value within 30 seconds of the change |
| Evidence report | Report | Records per scenario the statuses, the change rows, the report lines, the messages and the naming checks |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | The pack owns no table and asserts through the four platform operations and the P3 case list operation; feature_flag and feature_flag_change stay with PLT |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the consumer APP stories; the pack reads the case list through the P3 contract |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | On RWB-PLT-E1047-APP for the weekly removal report; the pack fires the Schedule with the clock control |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The five consumed REST operations of section 12.2 |
| DP-14 | Topic names with the legacy prefixes rwb.p n dot or rwb.casewf dot | rwb.<short>.events.v1; naming library | H RWB-PLT-E1047-CON | On the naming library and the wave 1 service stories; the pack asserts the refusal of a legacy name in AC11 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On the PLT and APP DB stories; the pack changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | Every flag call goes through gateway-bff; the queue column is read on SCR-02 Case list through the P3 case list operation |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own, and its I dependencies are RWB-P1-E1001-APP and RWB-PLT-E1047-APP. The H, C, I and X lists are exactly as the metadata table: Depends on (build) None, Contract dependencies None, Integration dependencies RWB-P1-E1001-APP and RWB-PLT-E1047-APP, External dependencies None.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the platform operations through gateway-bff and to the SIT and UAT endpoints of P3 and P1.
2. Build the flag fixture pack: the two flag keys with their owners, defaults and removal dates, plus a third key for the creation check, all as data rows.
3. Add the clock control and the report-date restore step, and fire the weekly removal report Schedule on Monday 2026-12-07 at 08:00.
4. Implement AC1 to AC3 in TC order and assert the effective value, the change row, the audit entry and the report lines.
5. Implement the cache window assertion of AC2 and the two-step fallback of AC7 through the test-only flag store switch.
6. Implement the negative cases of AC4, AC5, AC8, AC9 and AC10 and assert the exact statuses and messages.
7. Implement the naming check of AC11 against the naming library and assert that no legacy topic is created.
8. Write the evidence report with the statuses, the change rows, the report lines and the messages, remove the fixtures, restore the clock, and run the suite in SIT and UAT against the wave 1 release candidate.

Done when: all eleven test cases pass in SIT and UAT against the published wave 1 contracts and the platform operations, the evidence report is attached to the wave exit pack, and no service code or schema was changed by this story.

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

The message IDs and wording are copied from RWB-E1-047. No new message ID is added by this story. Thai text for each message follows decision DL10. The naming check reports one line per rejected name, holding the name, the reason and the rule of the naming library; it adds no message ID.

### 15. Screens and states

No screen in this story. The platform administrator uses the four operations through the admin API client. SCR-44 comes with Epic 8. The business user sees the queue column on SCR-02 Case list appear or disappear after reload, and the pack asserts that state through the P3 case list operation and the flag value, not through the screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-047-01-ITG | AC1 | Integration | Flag with default off, no UAT value; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-02-ITG | AC2 | Integration | Flag switched on in UAT with a reason; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-03-ITG | AC3 | Integration | Two flags, one past its removal date; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-04-ITG | AC4 | Integration | Removal date 2026-11-10 and an empty removal date; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-05-ITG | AC5 | Integration | Change with an empty reason; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-06-ITG | AC6 | Component | Unknown key; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-07-ITG | AC7 | NFR | Flag table made unreadable; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-08-ITG | AC8 | Integration | Two changes with If-Match version 4; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-09-ITG | AC9 | Component | Change to an unknown key; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-047-10-ITG | AC10 | Component | RW-CASEOWN calls PATCH /admin/feature-flags/{flagKey}; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1047-ITG-11 | AC11 | Contract | Legacy topic and event names built from the legacy prefixes; end-to-end: real services on the wave 1 contracts; no numeric business values added |

The legacy full test text, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the legacy test case id.

### 17. Guardrails

- No business value in code: flag values, owners and dates are rows; code holds only the key.
- No personal data in logs, events, evidence or fixtures; the change log holds user ids, never names.
- No cross-service table read: every assertion goes through the owner's operation, and the pack owns no table.
- One hop and a 2 s timeout on every call (ADR-020).
- Every flag that is off runs the previous code path; the suite covers both paths of the flags it changes.
- An unknown key or an unreadable store gives off, never on.
- Synthetic data only; no production access of any kind from the suite or its configuration.
- The test-only flag store switch is agreed with the platform owner, is limited to the test environment and is restored after the scenario.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-010 | Configuration changed without a code release | The four flag operations of section 12.2; MSG-GEN-005 | TC-E1-047-02-ITG, TC-E1-047-05-ITG |
| ADR-008 | A flag-based release; unfinished work behind a flag | Off by default and the previous code path; the change row and the audit entry | TC-E1-047-01-ITG, TC-E1-047-02-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed REST operations of section 12.2 | TC-E1-047-01-ITG, TC-E1-047-02-ITG, TC-E1-047-10-ITG |
| DP-01 | Owner's schema, never another service's tables | PLT owns feature_flag and feature_flag_change; the pack owns no table | All |
| DP-10 | Temporal Schedule replaces Quartz | The weekly flag removal report Schedule of section 12.6 | TC-E1-047-03-ITG |
| DP-14 | Per-service topic names through the naming library | The naming check of AC11; the legacy prefixes are refused | TC-ITG-E1047-ITG-11 |
| ASM-0473 | The flag tables and the four operations are PLT operations | GET /feature-flags, GET /admin/feature-flags, POST /admin/feature-flags, PATCH /admin/feature-flags/{flagKey} | TC-E1-047-01-ITG to TC-E1-047-10-ITG |
| ASM-0474 | The weekly report is a Temporal Schedule at Monday 08:00 | The Schedule of section 12.6; MSG-P2-003 | TC-E1-047-03-ITG |
| ASM-0475 | The four flag keys keep their legacy values as data rows | The flag fixtures of section 16 | TC-E1-047-01-ITG to TC-E1-047-10-ITG |

The legacy story is RWB-E1-047. The legacy AC1 to AC9 at component level belong to RWB-PLT-E1047-APP, not to this story.

### 19. Out of scope

- The platform library build: the two flag tables, the four operations, the cache and the weekly report, and their unit and component tests.
- The CON story RWB-PLT-E1047-CON.
- The legacy AC1 to AC9 at component level, which RWB-PLT-E1047-APP owns.
- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04 is not in this run's source set; the legacy section 19 stands.
- The queue write flag for models and agents: RWB-E2-036.
- The build of harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing.
