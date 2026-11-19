# RWB-TE-009 Performance test harness

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-009 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-OCC-007, REQ-WKM-002 |
| BRD section | Business Requirements Program, section 6.1 and section 6.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-004 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **a load test at the busiest-hour volume, run in SIT before each release, that fails the release stage when a screen request is too slow**, so that **response targets are proven before users feel them**.

## 2. Business rationale

About 370 staff and 50 partner users are online in the busiest hour (NFR-002, NFR-003), and every screen must respond in under 2 seconds (NFR-008). A screen that is fast with ten testers can be slow with four hundred users on 23,600 cases. The harness runs the busiest hour on the SIT data set before each release and stops the release stage when a target is missed. It proves the response of the case record view (REQ-OCC-007) and the team manager's case list (REQ-WKM-002) under load. The measure is the 95th percentile response time per screen request in the busiest hour.

## 3. Preconditions

- RWB-TE-004 is done: SIT holds at least 23,600 open cases read from the ACE views (NFR-001).
- SIT has named test users for each role in the operation mix (roles.txt key: test users before the release that gives a role real users), with Entra ID groups per DL40.
- An SIT deployment slot is booked for the run (DL35).
- The operation mix file and the pass criteria are loaded in the harness configuration: 410 virtual users at 3 requests a minute each; 95th percentile under 2,000 ms per operation; error rate under 1 percent (assumed; DL11).
- The build under test is deployed to SIT with its feature flags as planned for the release.

## 4. Flow

1. Release pipeline: starts the SIT performance stage for the build, or a squad member starts it by hand.
2. Harness: takes the SIT run lock; refuses to start when another run holds it.
3. Harness: counts open cases through GET /api/recovery/v1/cases and refuses to start when fewer than 23,600 are found.
4. Harness: signs in the test users for each role in the mix.
5. Harness: ramps to 410 virtual users over 10 minutes, then holds 60 minutes at 3 requests a minute per user, following the weights in the mix file.
6. Harness: records the response time and status of each request; 403 responses on operations the mix marks as refusals count as expected.
7. Harness: computes the 50th, 95th and 99th percentiles, the throughput and the error rate per operation over the 60 steady minutes.
8. Gate: passes when every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent; otherwise fails the stage.
9. Harness: attaches the report to the release record with the build ID, releases the lock and triggers the restore of the SIT data set.

## 5. Exception paths

None.

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the SIT data set of RWB-TE-004 and a deployed build |
| Negotiable | Mix, user count and pass criteria are configuration (DL11) |
| Valuable | A slow screen is found in SIT, not by 410 users in production |
| Estimable | One load script, one mix file, one gate, one report |
| Small | Fits in one sprint with its tests |
| Testable | The gate is tested with result fixtures; the run is tested in SIT |

## 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The load is 410 concurrent users at 3 requests a minute each, the busiest hour of staff and partner users | NFR-002; NFR-003; current story value |
| BR2 | Each screen request responds under 2,000 ms at the 95th percentile; 2,000 ms fails | NFR-008; DL11 |
| BR3 | The error rate over the steady period is under 1 percent; expected 403 refusals are not errors | DL11 (assumed) |
| BR4 | The run uses at least 23,600 open cases of masked data | NFR-001; NFR-045 |
| BR5 | The operation mix, user count and limits are read from the harness configuration, never from the script | Principle 1 applied to test configuration |
| BR6 | One run at a time in SIT; the latest run for a build decides the gate | DL35 |

## 9. State transitions

None. This story does not change a case status. It changes the state of the SIT performance stage: running, passed or failed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Start a run, change the mix file through a reviewed pull request, read reports |
| RW-PLATADM, platform administrator | Books the SIT slot and restores the SIT data set after the run |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-PHONECOL | Make the simulated requests with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-WRK-001 | queue | id | Read |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, SIT only, by postCasesCaseidInteractions |

The harness reads and writes only through the API. The SIT data set is restored after each run; the ACE views are read live. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Item | Value |
|---|---|
| Trigger | The SIT performance stage of the release pipeline before the UAT exit, or a manual start |
| Operations exercised | getCases, getCasesCaseid, getCasesCaseidTimeline, getCasesCaseidInteractions, getQueuesQueueidCases, getCasesCaseidDocuments and postCasesCaseidInteractions on /api/recovery/v1; postCasesCaseidTransfer as the expected refusal for RW-PHONECOL |
| Input | Mix file, user counts and limits; the list of test users per role; case and queue IDs read at start |
| Output | Report per operation: count, 50th, 95th and 99th percentiles, throughput, errors; gate result; build ID; mix file version |
| Schedule | Ramp 10 minutes, steady 60 minutes, measured on the steady period only |
| Idempotency | Each run has its own run ID; a rerun adds a report and replaces the gate result for the build |
| Restart | A run stopped part way is marked failed; the lock is released after 90 minutes at most |

This is a pipeline stage, not a scheduled Workbench job; it has no entry in the job list.

## 13. Solution plan

**Package.** Folder `perf/recovery` in the ACE repository, Java package `<ACE base package>.recovery.perf`. Not part of the deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusiestHourSimulation | Job | Load script: sign-in, ramp, steady period, weighted operations |
| mix file | Rule table | Operation, weight, role, expected status |
| perf settings | Rule table | User count, request rate, durations, limits |
| DataVolumeCheck | Service | Counts open cases before the run (BR4) |
| RunLock | Service | One run at a time in SIT (BR6) |
| PerformanceGate | Service | Evaluates the result against the limits (BR2, BR3) |
| ReportPublisher | Service | Attaches the report and the gate result to the release record |

**Database.** None directly. The harness uses the API only.

**Configuration and reference data.** Mix file and settings in `perf/recovery/config` (assumed values in section 3; DL11), owned by the TechX tech leads through code owners. Test users per role from the SIT identity set (DL40).

**Build steps**

1. Write PerformanceGate with unit tests from result fixtures for the boundary and the error rate (AC2, AC3).
2. Write DataVolumeCheck and RunLock (AC4, AC5).
3. Write BusiestHourSimulation reading the mix file and the settings (AC1, AC7).
4. Add the expected refusal for RW-PHONECOL on postCasesCaseidTransfer and count 403 as expected (access test).
5. Write ReportPublisher with the build ID and the latest-run rule (AC6).
6. Add the stage to the release pipeline before the UAT exit and run it once on the Epic 2 build.

**Feature flag.** None. The harness is a pipeline stage and does not ship in the service.

**Done when.** The tests in section 16 pass and the Epic 2 release record holds a passed report for the release build.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | 95th percentile at or above the limit | target missed: {operation} {p95} ms, limit {limit} ms |
| Report | Error rate at or above the limit | error rate above limit: {rate} percent |
| Report | Not enough data | data volume below the test base: {count} of {base} |
| Report | Lock held | run already in progress |
| MSG-P4-002 | Expected refusal for a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for the release team and is not part of the message standard.

## 15. Screens and states

No screen in this story. The release team reads the report attached to the release record. The screens under load are SCR-02, SCR-03, SCR-04 and SCR-07 through their API calls.

## 16. Test cases

None.

## 17. Guardrails

- No business value in code: the mix, user counts and limits are configuration.
- No personal data in logs, tests or prompts; the run uses the SIT data set, whose personal fields the ACE views mask, and the report holds operation names and numbers only.
- No read of another module's tables; the harness uses the API only.
- The harness never runs against UAT or production.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | Business Requirements Program, section 6.2 | None | All recovery processes | None | None |
| REQ-WKM-002 | Team manager sees every team queue with filters | Business Requirements Program, section 6.2 | None | All recovery processes | None | None |

## 19. Out of scope

- Masked data in SIT and UAT: RWB-TE-004.
- Batch window timing of the daily jobs (NFR-013, NFR-019): the job stories, for example RWB-TE-007.
- Agent response times (NFR-010): the P10 agent runtime stories, for example RWB-TE-013.
- Production monitoring of response times: RWB-E1-056.
