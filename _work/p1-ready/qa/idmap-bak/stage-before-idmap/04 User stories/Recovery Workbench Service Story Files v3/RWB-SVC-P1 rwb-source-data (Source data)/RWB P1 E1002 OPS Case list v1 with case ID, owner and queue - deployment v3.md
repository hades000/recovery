# RWB-P1-E1002-OPS Case list v1 with case ID, owner and queue - deployment

### Version 3 changes

- RD-P1-024, X-27 and RD-P1-044: this story is reduced to a delta on RWB-P1-E1015-OPS that deploys only the account-page read; no Schedule, workflow, consumer, flag or case-list alert (findings #2, #3, #6, #7, #8, #10, #11, #13, #18, #20, #21, #25, #27).
- PROD, rollback, readiness, negative paths, observability, capacity and security checks are now testable (findings #1, #9, #12, #14 to #17, #19, #22, #24, #26).
- AC1 to AC10 of version 2 are withdrawn; AC11 to AC19 are new.
- Pending: the read's path and page limit (NEW-GAP-B3) and the peak concurrent page reads (NEW-GAP-S1-5).
- Finishing pass (requests W2-tests-1058, W3-messages-0034; test case backfill): the Test Cases v9 IDs are cited, with the access and business-rule rows.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP11, DP14 |
| Parallel lane | L-P1-F |
| Ready to start | After RWB-P1-E1015-OPS and RWB-P1-E1002-APP |
| Depends on (build) | RWB-P1-E1015-OPS, RWB-P1-E1002-APP, RWB-P1-E1015-CON, RWB-P1-E1069-DB |
| Contract dependencies | RWB-P1-E1015-CON |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), REST base `/api/recovery/source-data/v1`; the service consumes no rwb-case contract for this read |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-024, RD-P1-043, RD-P1-044, RD-P1-045 |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P1-E1002-OPS-22) |
| Integration dependencies | None |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-P1-E1002-OPS-16) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (CAP-P1-010 retired and FR-P1-022 withdrawn; P1 supplies the account-page read, for which the PRD holds no requirement ID of its own) |
| Status | Draft (P1 developer readiness) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. This story deploys the case-list capability: the api and worker deployments of `rwb-source-data`, the Temporal worker for `CaseListBuildWorkflow` with its KEDA scaling, the `DailyCaseList` Schedule registration at 07:15 Asia/Bangkok, the configuration of the three parameters by contract, the read path of rwb-case and rwb-reporting, the dashboards, the MSG-P1-001 and PUBLISHED NO alerts, the runbook and the capacity. It deploys no lake credential, no file adapter and no data set (DP-17; GAP-0485, ASM-0677). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: reduced to the delta deployment of the account-page read (RD-P1-024, RD-P1-044, X-27). Agent: S1-stories.

### 1. Story

As a **platform engineer**, I want **the account-page read of rwb-source-data released as a delta on the service's one chart, reachable by rwb-case only, measured and alerted, and able to be rolled back**, so that **the case list shows ACE account values within its time budget in every environment and an operator can see when it does not**.

The chart, the api and worker Deployments, probes, migration job, login secret reference and base alerts belong to RWB-P1-E1015-OPS (RD-P1-044). This story adds values keys, one caller rule, one dashboard panel group, two alert rules and one runbook entry. The title and key are kept from the legacy case list.

### 2. Business rationale

rwb-case composes the case list at read time and gets the account values only through this read (RD-P1-024). A release that does not admit rwb-case, or that is slow or failing without an alert, leaves every recovery team without balances and days past due. The deadline of the morning list belongs to the rwb-case schedule and alerts; this release is measured on the 2 s budget of the read (finding #3).

### 3. Preconditions

- RWB-P1-E1015-OPS is deployed in the target environment: chart, api Deployment with 2 replicas, probes, migration job, `rwb_source_data` login secret reference, base alerts.
- RWB-P1-E1002-APP is built and its image is in the pipeline.
- RWB-P1-E1069-DB has granted `rwb_source_data` SELECT on `recovery.v_ace_account` and `recovery.v_ace_efs_action`. Both are Section A views: nothing here waits for RWB-ACE-001 or a Section B flag.
- The values files for DEV, SIT, UAT and PROD exist, and the rwb-case workload identity exists in each.

### 4. Flow

1. Pipeline: renders the service chart for DEV, SIT, UAT and PROD and compares it with the chart of RWB-P1-E1015-OPS; only added values keys are accepted.
2. Pipeline: builds one image, runs the tests of RWB-P1-E1002-APP and the provider contract test, and promotes the same digest.
3. Release: applies the caller rule that admits the rwb-case workload identity to the read.
4. Release: publishes the dashboard panels, the two alert rules and the runbook entry.
5. Pipeline: runs the smoke call with one synthetic account key under the rwb-case identity, and a refused call under another identity.
6. Release owner: promotes to PROD after the SIT capacity run and the UAT smoke call pass.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rendered chart adds or changes anything but values keys | The pipeline stage fails naming the object | None | AC11 |
| X2 | The contract test or the smoke call fails | The release stops; the previous image keeps serving | None | AC15 |
| X3 | The ACE views cannot be read | The pod stays ready; the read answers 503; the error alert fires | MSG-GEN-006 | AC16 |
| X4 | The read is slower than 2 s at the 95th percentile | The latency alert fires to the platform on-call | None | AC14 |
| X5 | Another identity calls the read | 403; counted on the refused-read panel | MSG-P4-002 | AC13 |
| X6 | A fault is found after release | `rwb.p1.case-list` is switched off by rwb-case, then the previous image tag is redeployed | None | AC17 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A delta on one existing chart |
| Negotiable | Alert windows and resource values are environment values |
| Valuable | Makes the read available, visible and reversible |
| Estimable | Values keys, one caller rule, panels, two alerts, one runbook entry, one capacity run |
| Small | Fits one sprint |
| Testable | Each criterion tests an artefact or a pipeline outcome |

### 7. Acceptance criteria

```gherkin
Feature: Delta deployment of the account-page read

  Scenario: AC11 Chart delta only, in every environment including PROD
    Given the chart of RWB-P1-E1015-OPS
    When the release is rendered with values for DEV, SIT, UAT and PROD
    Then each render differs only by values keys of the read
    Then no Deployment, Job, ScaledObject, Schedule, workflow registration, topic, consumer group or feature flag is added
    Then the same image digest is pinned in all four and no secret literal appears

  Scenario: AC12 rwb-case reaches the read
    Given the release is in SIT with one synthetic account key behind both views
    When the smoke call is made under the rwb-case workload identity with that key and its business date
    Then the answer is 200 with one entry within 2 s and no table of rwb_source_data has changed

  Scenario: AC13 Every other caller is refused and counted
    Given the release is in SIT
    When the read is called under the rwb-reporting workload identity and with a user token
    Then each answer is 403 with messageCode MSG-P4-002
    Then the refused-read panel shows 2 and nobody is paged

  Scenario: AC14 Panels and alerts
    Given the dashboards and rules are published
    When synthetic metrics show a p95 duration above 2 s, and separately 503 answers above the environment threshold, over the environment window
    Then the matching alert reaches the platform on-call and the operations channel within 15 minutes with its runbook entry
    Then the panels show request count, p95 duration, 503 count and 403 count of the read

  Scenario: AC15 A failing release does not replace the running one
    Given a build whose provider contract test fails, and separately one whose smoke call returns 500
    When the pipeline runs
    Then the stage fails and the pods of the previous image keep answering

  Scenario: AC16 ACE view fault does not take the api out of service
    Given recovery.v_ace_account cannot be read
    When the read is called and the readiness probe runs
    Then the read answers 503 with messageCode MSG-GEN-006 and the probe still passes
    Then the other operations of the api keep answering

  Scenario: AC17 Rollback
    Given the release is in SIT
    When rwb.p1.case-list is switched off and the previous image tag and chart version are redeployed
    Then the previous pods run against the unchanged schema, the read path of the new release is gone and no migration or undo script runs

  Scenario: AC18 Capacity at the planned book size
    Given SIT views holding 26,500 accounts for one business date and the maximum keys per call of the published contract
    When all 26,500 keys are read page by page
    Then each call answers within 2 s at the 95th percentile
    Then the run record holds keys per call, calls, concurrent callers, p95 duration and database connections used

  Scenario: AC19 No secret, no identifier in logs, no wider grant
    Given the release and the calls of AC12 and AC13
    When values, charts, logs, dashboard series and alert payloads are scanned and the grants of rwb_source_data are tested
    Then no secret literal and no account key or account number is found
    Then a SELECT on a public table with that login is refused
```

AC1 to AC10 of version 2 tested the case-list workflow, Schedule, read path and alerts. They are withdrawn and their numbers are not reused. AC18 cannot be run until NEW-GAP-B3 fixes the page size.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR9 | One owner per shared deployment object: this story adds values keys and redefines nothing | RD-P1-044 |
| BR10 | The same image digest is promoted through DEV, SIT, UAT and PROD | Environment and Deployment Design |
| BR11 | Rollback is flag off, then previous image and chart; migrations are never reversed | RD-P1-045 |
| BR12 | Downstream faults are shown by metrics and alerts, not by api readiness | Review finding #19; RD-P1-044 (probes owned by RWB-P1-E1015-OPS) |

BR1 to BR8 of version 2 are withdrawn with the case-list run; their IDs are not reused.

### 9. State transitions

| From | To | Trigger |
|---|---|---|
| Read not deployed | Deployed | The pipeline releases the new image to the environment |
| Deployed | Previous release | Rollback (AC17) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Values keys, caller rule, pipeline stages, panels, alerts, runbook |
| Release owner | Promotes the digest and decides a rollback (RD-P1-045 item 6) |
| rwb-case workload identity | The only caller of the read |
| Platform on-call | Receives the two alerts |

### 11. Data

No table, column or seed. The runtime login `rwb_source_data` reads `recovery.v_ace_account` and `recovery.v_ace_efs_action`; the grant is made by RWB-P1-E1069-DB. This release runs no migration of its own, so it needs no separate DDL identity.

### 12. Contract

#### 12.1 REST operations provided

None by this story. It deploys the account-page read of RWB-P1-E1015-CON, built by RWB-P1-E1002-APP (path pending, NEW-GAP-B3).

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

None.

#### 12.4 Events consumed

None. No consumer group is declared (RD-P1-044).

#### 12.5 Workflows and activities

None. `CaseListBuildWorkflow` is withdrawn.

#### 12.6 Schedules

None. `DailyCaseList` is withdrawn; GAP-0487 no longer applies.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

The provider contract test runs against rwb-source-data.yaml 5.1.0. The consumer fake is published by RWB-P1-E1015-CON (RD-P1-011).

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 1 deployed (path pending) | None |
| Kafka | None | None |
| Temporal | None | None |
| File | None | None |

### 13. Solution plan

**Values keys.** The caller allow-list entry for rwb-case, the alert window and 503 threshold per environment, and any resource change the capacity run shows to be needed. No object of the chart is redefined.

**Observability.** Four series of the read (request count, duration, 503 count, 403 count) as one panel group on the service dashboard of RWB-P1-E1015-OPS; two alert rules (latency above 2 s p95; 503 count above threshold), owner platform on-call, one runbook entry `account-page read`. The standard per-service alerts stay those of RWB-P1-E1015-OPS.

**Capacity.** The planning volume is 26,500 open cases at the end of 2027 (NFR-001: about 23,600 at go-live). Pending: peak concurrent page reads, owner solution architect, tracked as NEW-GAP-S1-5.

**Feature flag.** None of its own; the caller's flag `rwb.p1.case-list` belongs to rwb-case.

**Rollback.** Switch `rwb.p1.case-list` off, redeploy the previous image tag and chart version, correct forward. Because the chart is shared, the release note names every P1 capability the redeploy reverts (RD-P1-045).

**Runbook entry.** Symptoms: latency or 503 alert. Checks: ACE database reachability, view grants, connection pool. Actions: escalate to the ACE database administrator, or roll back as above.

**Done when.** AC11 to AC19 pass in SIT and the PROD values have been rendered and reviewed.

### 14. Validation and messages

| ID | When | Owner |
|---|---|---|
| MSG-P4-002 | A caller other than the rwb-case identity | RWB-P1-E1002-APP |
| MSG-GEN-006 | ACE database or view unreadable | RWB-P1-E1002-APP |

The alerts of this story carry no user message ID. MSG-P1-001 is not raised by this release.

### 15. Screens and states

No screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1002-OPS-20, TC-P1-E1002-OPS-24, TC-P1-E1002-OPS-26 | AC11, AC15, AC17 | Pipeline | Rendered charts; failing builds; previous tag |
| TC-P1-E1002-OPS-21, TC-P1-E1002-OPS-22, TC-P1-E1002-OPS-25, TC-P1-E1002-OPS-28 | AC12, AC13, AC16, AC19 | Integration | One synthetic account; refused identities; view revoked |
| TC-P1-E1002-OPS-23, TC-P1-E1002-OPS-27 | AC14, AC18 | Operational | Synthetic metrics; 26,500 synthetic accounts |

The TC-E1-002 rows of version 2 for this story test withdrawn behaviour and are retired in Test Cases v9, except TC-E1-002-20 (BR8). OPS rows have their own IDs and do not reuse the legacy business-test IDs.

| Criterion or rule | TC ID |
|---|---|
| Access | TC-P1-E1002-OPS-06 |
| BR1, BR2, BR3 | TC-P1-E1002-OPS-09 to TC-P1-E1002-OPS-11 |
| BR5, BR6 | TC-P1-E1002-OPS-13, TC-P1-E1002-OPS-14 |
| BR8 | TC-E1-002-20 |

### 17. Guardrails

- No personal data in logs, series, alert payloads or the runbook.
- ACE only through the two views; no grant on `public` or another `rwb_*` schema (DP-02, DP-05).
- No secret in values, templates, dashboards or the runbook.
- The same digest is promoted; no rebuild between environments.
- The smoke call writes nothing, so it needs no clean-up; it uses a synthetic account key in the environment's own namespace and schema.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | One case list that agrees with `v_ace_account` | Deployment and capacity of the account-page read | TC-P1-E1002-OPS-20 to TC-P1-E1002-OPS-28 |
| REQ-RDF-009 | Source data is shown with its business date | Smoke check of `dataAsOf` | TC-P1-E1002-OPS-20 to TC-P1-E1002-OPS-28 |
| ADR-020 | One hop, 2 s | Latency alert and capacity run | TC-P1-E1002-OPS-23, TC-P1-E1002-OPS-27 |
| ADR-023 | Observability per service | Panels, alerts, runbook entry | TC-P1-E1002-OPS-23 |

REQ-DRI-007 (delivery retry parking) is dropped: this release sends nothing.

### 19. Out of scope

- The chart, Deployments, probes, migration job, KEDA and base alerts (RWB-P1-E1015-OPS).
- The application code (RWB-P1-E1002-APP) and the contract and fake (RWB-P1-E1015-CON).
- The case list, its Schedule `rwb-case-caselist-daily`, its flag and its alerts (rwb-case).
- Job monitor and rerun deployment (RWB-P1-AD018-OPS).
- The end-to-end run of the list (RWB-ITG-E1002-ITG).

### 20. Remaining delivery steps

- Path and maximum keys per call of the read: Pending, NEW-GAP-B3; owner solution architect.
- Peak concurrent page reads for sizing: Pending, NEW-GAP-S1-5; owner solution architect.
- Alert window and 503 threshold values per environment: Pending; owner platform on-call lead.
- Size (DOR-RWB-P1-E1002-OPS-16), contract fake library version (DOR-RWB-P1-E1002-OPS-22), role code for the platform engineer: Pending; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect and business analyst.
- CON Done (RWB-P1-E1015-CON) and fake published: Pending; owner contract owner and platform library owner.
- Test data in DEV and SIT: Pending; owner QA lead.
