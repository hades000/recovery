# RWB-ITG-TE009-ITG Performance test harness

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE009-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-ITG-NFR |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-TE-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized; the squad sizes it at refinement |
| Patterns applied | DP01, DP07, DP10, DP13, DP19, DP20 |
| Parallel lane | L-ITG-NFR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-TE-009 is split and reworked as the integration story RWB-ITG-TE009-ITG, the busiest-hour load harness that runs in the SIT release pipeline and gates the release stage on the per-service bases through the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 14 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a busiest-hour load harness in the SIT release pipeline that exercises the screens through gateway-bff on the per-service bases and fails the release stage when a screen request is too slow**, so that **response targets are proven before users feel them**.

### 2. Business rationale

About 370 staff and 50 partner users are online in the busiest hour (NFR-002, NFR-003) and every screen must respond in under 2 seconds (NFR-008). A screen that is fast with ten testers can be slow with 410 virtual users at 3 requests a minute each on 23,600 open cases. The harness runs the busiest hour on the SIT data set before each release and stops the release stage when a target is missed. It proves the response of the case record view (REQ-OCC-007) and the team manager's case list (REQ-WKM-002) under load. The measure is the 95th percentile response time per screen request in the busiest hour.

In the target architecture the screen request is served by the gateway-bff composite route (DP-19), and each call inside the route goes to the owner's base `/api/recovery/<short>/v1` (DP-13), not to a monolith base. The harness therefore measures the routes and the per-service bases that the real screens use, so a slow hop is visible at the same point a user would feel it.

### 3. Preconditions

- SIT holds at least 23,600 open cases of masked data (RWB-TE-004, NFR-001).
- Named test users exist for each role in the operation mix, with Entra ID groups per role. The identity set of the test users per role is fixed at the harness configuration review before the first SIT run and kept in configuration, never in the script (GAP-0330).
- An SIT deployment slot is booked for the run.
- The operation mix file and the pass criteria are loaded in the harness configuration: 410 virtual users at 3 requests a minute each; 95th percentile under 2,000 ms per operation; error rate under 1 percent.
- The build under test is deployed to SIT with its release feature flags as planned for the release.
- The gateway-bff composite routes and the per-service bases are reachable in SIT. The composite routes are fixed at the harness configuration review before the first SIT run and kept in configuration, never in the script (GAP-0330).
- No build dependency. Day 1.

### 4. Flow

1. Release pipeline: starts the SIT performance stage for the build, or a squad member starts it by hand.
2. Harness: takes the SIT run lock and refuses to start when another run holds it.
3. Harness: counts open cases through `GET /api/recovery/case/v1/cases` and refuses to start when fewer than 23,600 are found.
4. Harness: signs in the test users for each role in the mix.
5. Harness: ramps to 410 virtual users over 10 minutes, then holds 60 minutes at 3 requests a minute per user, following the weights in the mix file.
6. Harness: records the response time and the status of each request; 403 responses on operations the mix marks as refusals count as expected.
7. Harness: computes the 50th, 95th and 99th percentiles, the throughput and the error rate per operation over the 60 steady minutes.
8. Gate: passes when every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent; otherwise it fails the stage.
9. Harness: attaches the report to the release record with the build ID, releases the lock and triggers the restore of the SIT data set.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Another run holds the SIT run lock | The run refuses to start and the stage stops before any load | run already in progress | AC5 |
| X2 | Fewer open cases than the test base | The run refuses to start and reports the count against the base | data volume below the test base: {count} of {base} | AC4 |
| X3 | A test user of a role in the mix cannot sign in | The stage fails and names the role; no load is generated for that role | None | AC1 |
| X4 | gateway-bff or a service answers 503 | The request counts as an error; the stage fails on the error rate when the limit is crossed | error rate above limit: {rate} percent | AC3 |
| X5 | An operation's 95th percentile is at or above 2,000 ms | The gate fails the stage and the report names the operation, its 95th percentile and the limit | target missed: {operation} {p95} ms, limit {limit} ms | AC2 |
| X6 | The error rate is at or above 1 percent | The gate fails the stage and the report names the operation and the rate | error rate above limit: {rate} percent | AC3 |
| X7 | A run is stopped part way | The run is marked failed and the lock is released within 90 minutes | None | AC5 |

The report text is for the release team and is not part of the message standard. MSG-P4-002 is the business message for an expected refusal, and the harness records it as an expected result, not as an error.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the SIT data set of RWB-TE-004, a deployed build and reachable routes; no build dependency |
| Negotiable | The mix, the user count and the pass limits are configuration, never code |
| Valuable | A slow screen is found in SIT, not by the busiest hour of users in production |
| Estimable | One load script, one mix file, one gate, one report publisher |
| Small | Fits in one sprint with its tests |
| Testable | The gate is tested with result fixtures; the run is tested in SIT against the deployed services |

### 7. Acceptance criteria

```gherkin
Feature: Busiest-hour performance harness for the recovery screens

  Background:
    Given the build under test is deployed to SIT with its release feature flags
    Given the harness configuration holds the operation mix, the user count and the pass limits
    Given the screens are reached through the gateway-bff composite routes
    Given each call uses the owner's per-service base /api/recovery/<short>/v1
    Given the owner service of each operation is read from the OperationCatalog of RWB-PLT-TE003-APP before the first gated run

  Scenario: AC1 The busiest-hour load runs at 410 virtual users and 3 requests a minute (new, D-RCV-60)
    Given the SIT performance stage starts for the build
    When the harness ramps to 410 virtual users over 10 minutes and holds for 60 minutes at 3 requests a minute per user
    Then every request follows the weights of the operation mix file
    Then the measured period is the 60 steady minutes only
    Then the operations exercised are GET /api/recovery/case/v1/cases, GET /api/recovery/case/v1/cases/{caseId}, GET /api/recovery/case/v1/cases/{caseId}/timeline, GET /api/recovery/case/v1/queues/{queueId}/cases, GET /api/recovery/document/v1/cases/{caseId}/documents, POST /api/recovery/source-data/v1/cases/{caseId}/interactions and POST /api/recovery/case/v1/cases/{caseId}/transfer as the expected refusal for RW-PHONECOL

  Scenario: AC2 The gate fails the stage when a 95th-percentile target is missed (new, D-RCV-60)
    Given the per-operation results of the steady period
    When an operation's 95th percentile is at or above 2,000 ms
    Then the gate fails the stage
    Then the report names the operation, its 95th percentile and the 2,000 ms limit
    When every operation's 95th percentile is under 2,000 ms
    Then the gate passes for that operation

  Scenario: AC3 The gate fails the stage when the error rate is at or above 1 percent (new, D-RCV-60)
    Given the per-operation results of the steady period
    When the error rate of an operation is at or above 1 percent
    Then the gate fails the stage and the report names the operation and its error rate in percent against the 1 percent limit
    Then a 403 response on an operation the mix marks as a refusal is counted as expected and not as an error
    When the error rate of every operation is under 1 percent
    Then the gate passes for those operations

  Scenario: AC4 The run refuses to start below 23,600 open cases (new, D-RCV-60)
    Given the SIT data set of masked data
    When the harness counts open cases through GET /api/recovery/case/v1/cases before the run
    Then it refuses to start when fewer than 23,600 are found and reports the count and the base
    Then it starts when 23,600 or more are found

  Scenario: AC5 One run at a time and the lock is released within 90 minutes (new, D-RCV-60)
    Given a run holds the SIT run lock
    When a second run starts
    Then it is refused with "run already in progress"
    When the first run ends or stops part way
    Then the lock is released, and in every case within 90 minutes at most
    Then a run stopped part way is marked failed

  Scenario: AC6 The report is attached to the release record (new, D-RCV-60)
    Given a finished run
    When the harness publishes the report
    Then the report carries the build ID, the mix file version and, per operation, the count, the 50th, 95th and 99th percentiles, the throughput and the errors
    Then it carries the gate result, and the latest run for a build decides the gate
    Then it holds operation names and numbers only and no personal data

  Scenario: AC7 The operation mix, the user count and the limits are read from the harness configuration and not from the script (new, D-RCV-60)
    Given the harness configuration holds the operation mix, the user count and the limits
    When one of these values is changed in the configuration and the script is not edited
    Then the run uses the changed value

  Scenario: AC8 Every exercised operation calls the owner's per-service base through the gateway-bff composite route (new, D-RCV-60)
    Given an operation in the operation mix
    When the harness calls the operation
    Then the call reaches the owner's per-service base through the gateway-bff composite route

  Scenario: AC9 A consumed call that fails or does not answer is counted as an error of its operation (new, D-RCV-60)
    Given a consumed call through the gateway-bff composite route
    When the call fails or does not answer
    Then the call is counted as an error of its operation and the error rate of AC3 applies
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The load is 410 concurrent users at 3 requests a minute each, the busiest hour of staff and partner users | NFR-002; NFR-003 | AC1; TC-ITG-TE009-ITG-01 |
| BR2 | Each screen request responds under 2,000 ms at the 95th percentile; 2,000 ms fails | NFR-008 | AC2; TC-ITG-TE009-ITG-02 |
| BR3 | The error rate over the steady period is under 1 percent; expected 403 refusals are not errors | Legacy RWB-TE-009 BR3 | AC3; TC-ITG-TE009-ITG-03 |
| BR4 | The run uses at least 23,600 open cases of masked data | NFR-001; NFR-045 | AC4; TC-ITG-TE009-ITG-04 |
| BR5 | The operation mix, the user count and the limits are read from the harness configuration, never from the script | Legacy RWB-TE-009 BR5 | AC7; TC-ITG-TE009-ITG-07 |
| BR6 | One run at a time in SIT; the latest run for a build decides the gate | Legacy RWB-TE-009 BR6 | AC5; TC-ITG-TE009-ITG-05 |
| BR7 | Every exercised operation calls the owner's per-service base through the gateway-bff composite route | DP-13; DP-19 | AC8; TC-ITG-TE009-ITG-08 |
| BR8 | The 2,000 ms budget is measured at the gateway-bff response | ASM-0423 | AC2; TC-ITG-TE009-ITG-02 |

### 9. State transitions

| From | To | Trigger |
|---|---|---|
| Not started | Running | The release pipeline starts the SIT performance stage for the build |
| Running | Passed | Every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent |
| Running | Failed | A limit is missed, a 503 raises the error rate, or the run is stopped part way |
| Failed | Running | A rerun for the same build, which replaces the gate result for that build |

This story changes the state of the SIT performance stage only. It never changes a case status and writes no row through any service other than the SIT interaction writes of section 11.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Start a run, change the mix file through a reviewed pull request, read reports |
| RW-PLATADM, platform administrator | Books the SIT slot and restores the SIT data set after the run |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-PHONECOL | Make the simulated requests with their own rights |
| QA lead | Owns the harness configuration: the mix file, the user count and the pass limits |
| Platform edge owner | Owns the gateway-bff route list the harness calls |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-WRK-001 | queue | id | Read |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, SIT only, by `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` |

The harness reads and writes only through the API: it owns no schema and reads no other service's tables (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary. The SIT data set is restored after each run.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a pipeline stage and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Open-case count before the run and the case list operation of the mix |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case record operation (SCR-03) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | Case timeline operation (SCR-04) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | Team queue operation (SCR-07) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Document list operation of the case record |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Interaction write, SIT only, from the mix |
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 rwb-case | Expected refusal for RW-PHONECOL (MSG-P4-002) |

Every operation is called through the gateway-bff composite route (DP-19) and on the owner's per-service base (DP-13).

#### 12.3 Events published

None. The harness publishes no Kafka event; the report goes to the release record through its pipeline integration.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. The harness runs as a pipeline stage and starts no Temporal workflow or activity; DP-10 is applied by keeping the harness out of the job list, so no Schedule is created.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

None. The harness owns no table (DP-01); it reads and writes through the API of the owning services only.

#### 12.8 Contract fakes

None used, and none is needed. The stage runs against the deployed SIT services and their real contracts: no contract fake is named for `rwb-case.yaml`, for `rwb-document.yaml` or for `rwb-source-data.yaml`, each built against version 5.0.0 (`info.version`) as recorded below. A fake enters this section only when a stage must run before the owner service is deployed in SIT, and no operation of section 12.2 needs that. Contract fake library version: Not specified in the source documents (DOR-RWB-ITG-TE009-ITG-22).

Contract version built against: version 5.0.0 (`info.version`) of `rwb-case.yaml`, `rwb-document.yaml` and `rwb-source-data.yaml` in 05 Technical architecture/Recovery Workbench API Specification v5.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, every call through gateway-bff on the owner's base |
| Kafka | None |
| Temporal | None |
| File | None |

### 13. Solution plan

**Package.** Folder `perf/recovery` in the ACE repository, package `<ACE base package>.recovery.perf`. Not part of the deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusiestHourSimulation | Job | Sign-in, ramp, steady period and weighted operations |
| mix file | Rule table | Operation, weight, role, expected status |
| perf settings | Rule table | User count, request rate, durations, limits |
| DataVolumeCheck | Service | Counts open cases before the run |
| RunLock | Service | One run at a time in SIT |
| PerformanceGate | Service | Evaluates the result against the limits |
| ReportPublisher | Service | Attaches the report and the gate result to the release record |

**Database.** None. The harness owns no schema and uses the API only.

**Configuration.** The mix file and the settings sit in `perf/recovery/config`; the test users per role come from the SIT identity set; the gateway route list comes from the platform edge.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The story carries no H, C, I or X dependency (the plan keeps them empty) because the harness runs against the deployed SIT services and their published contracts, and the DP dependencies stay with the service implementation stories; DP-10 resolves to "no Schedule" and DP-20 resolves to "the agent is not in the mix" (NFR-010 is out of scope, the P10 stories own it).

**Build steps**

1. Write PerformanceGate with unit tests from result fixtures for the 2,000 ms boundary and the error rate.
2. Write DataVolumeCheck and RunLock.
3. Write BusiestHourSimulation reading the mix file and the settings.
4. Add the expected refusal for RW-PHONECOL on the transfer operation and count 403 as expected.
5. Write ReportPublisher with the build ID and the latest-run rule.
6. Add the stage to the release pipeline before the UAT exit and run it once on the Epic 2 build.

**Done when.** The tests of section 16 pass and the Epic 2 release record holds a passed report for the release build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | An operation's 95th percentile is at or above the limit | `target missed: {operation} {p95} ms, limit {limit} ms` |
| Report | The error rate is at or above the limit | `error rate above limit: {rate} percent` |
| Report | Not enough data for the run | `data volume below the test base: {count} of {base}` |
| Report | Another run holds the lock | `run already in progress` |
| MSG-P4-002 | Expected refusal for a role without the right | You cannot {action} here. Your role does not include it. |

The report text is for the release team and is not part of the message standard.

### 15. Screens and states

No screen in this story; the release team reads the report attached to the release record. The screens under load are SCR-02 Case list, SCR-03 Case record, SCR-04 Case timeline and SCR-07 Team queues, each reached through the gateway-bff composite route. States from Screen Specifications v1: SCR-02 Case list has loading and empty; error and no access are Not specified in the source documents (CG-ALL-102). SCR-03 Case record has loading; empty, error and no access are Not specified in the source documents (CG-ALL-103). SCR-04 Case timeline has loading; empty, error and no access are Not specified in the source documents (CG-ALL-104). SCR-07 Team queues has loading; empty, error and no access are Not specified in the source documents (CG-ALL-105). The composite routes are fixed at the harness configuration review before the first SIT run (GAP-0330).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ITG-TE009-ITG-01 | AC1 | NFR | Mix fixture; ramp 10 minutes and steady 60 minutes at 410 virtual users and 3 requests a minute |
| TC-ITG-TE009-ITG-02 | AC2 | NFR | Result fixture at 1,999 ms passes and at 2,000 ms fails |
| TC-ITG-TE009-ITG-03 | AC3 | NFR | Error rate 0.9 percent passes and 1.0 percent fails; an expected 403 is not counted |
| TC-ITG-TE009-ITG-04 | AC4 | Integration | 23,599 open cases refuses and 23,600 starts |
| TC-ITG-TE009-ITG-05 | AC5 | Integration | A second run is refused; the lock is released within 90 minutes after a stopped run |
| TC-ITG-TE009-ITG-06 | AC6 | Component | Report fixture with two operations and one missed target, build ID and mix version present |
| TC-ITG-TE009-ITG-07 | AC7 | Component | Harness configuration fixture with a changed user count; the script is not edited |
| TC-ITG-TE009-ITG-08 | AC8 | Integration | Exercised operations route through the gateway-bff composite route to the owner's per-service base |
| TC-ITG-TE009-ITG-09 | AC9 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-TE009-ITG-AC8) |

### 17. Guardrails

- No business value in code: the mix, the user counts and the limits are configuration.
- No personal data in logs, reports, tests or prompts: the run uses the SIT masked data set, and the report holds operation names and numbers only.
- No read of another service's tables: the harness uses the API only (DP-01).
- The harness never runs against UAT or production.
- An exception to a limit is never added to the script; a limit that must change is changed in the configuration through a reviewed pull request.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | GET case operations | TC-ITG-TE009-ITG-01, TC-ITG-TE009-ITG-02 |
| REQ-WKM-002 | Team manager sees every team queue with filters | GET queues/{queueId}/cases | TC-ITG-TE009-ITG-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | gateway-bff one hop and the 2,000 ms budget | TC-ITG-TE009-ITG-02 |

### 19. Out of scope

- Masked data in SIT and UAT: RWB-TE-004.
- Batch window timing of the daily jobs: the job stories.
- Agent response times, NFR-010: the P10 agent runtime stories (DP-20).
- Production monitoring of response times: RWB-E1-056.
- UAT and production runs.
- The gateway-bff route specification: the platform edge story.
