<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 023 Automated EFS file load v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 023 Automated EFS file load v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-023 Automated EFS file load

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-023 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CHO-10 Automate the EFS file load |
| Requirement IDs | REQ-RDF-007, REQ-RDF-006, REQ-CHO-001 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 6.1 Take over the case at 90 days past due |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E2-001, RWB-E1-051 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the EFS hand-over load automated end to end and reconciled each day, with the manual EFS file handling retired after ten clean days in a row**, so that **one checked path remains for every account handed over from collections**.

## 2. Business rationale

The EFS hand-over moves today by a manual file as well as the COLLINS load. Two paths give two answers and no one checks the difference. This story reconciles each day the accounts EFS hands over at 90 days past due against the cases created or linked, lists every difference, alerts above the threshold, and lets the data steward retire the manual path with a recorded sign-off after ten clean days. It meets REQ-RDF-007, REQ-RDF-006 and REQ-CHO-001.

## 3. Preconditions

- RWB-E2-001 (case creation from the COLLINS load) and RWB-E1-051 (feed jobs on Control-M) are done.
- JOB-04 Daily reconciliation runs after JOB-02.
- Parameter `recon.efs.alert_pct` = 0.1 percent (assumed; DL25 recommends zero) and parameter `recon.efs.clean_days_required` = 10.
- The manual EFS upload path is behind flag `rwb.integration.efs-manual-upload`, on until sign-off.
- The builder of the EFS file automation is the Workbench squad (DL30, option A assumed).
- The person holds RW-DATASTEW.

## 4. Flow

1. Scheduler: JOB-04 starts after JOB-02 for business date D.
2. SY-DATALOAD: the EfsReconService reads the count and the list of accounts EFS handed over at 90 days past due on D through the P1 EfsHandoverQuery.
3. SY-DATALOAD: reads the cases created and the accounts linked by JOB-02 for D from the hand-over run summary.
4. SY-DATALOAD: compares the two lists by account ID; each account on one side only is a difference with a reason (no case, held in the exception list, case without a hand-over).
5. SY-DATALOAD: writes each difference as a data quality exception with product DP05 and check "EFS hand-over reconciliation", and writes the day result (counts, difference percent, clean or not) to the run record.
6. SY-DATALOAD: when the difference is above the alert threshold, alerts the data steward and the platform administrator with MSG-P2-013.
7. Data steward: after ten clean days in a row, signs off the retirement of the manual EFS file handling.
8. System: checks the clean days, writes the sign-off record and switches flag `rwb.integration.efs-manual-upload` off for the environment.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Difference above 0.1 percent | Data steward and platform administrator alerted | MSG-P2-013 | AC3 |
| X2 | Difference at or below the threshold but not zero | Differences listed; no alert; the day is not clean | None | AC4 |
| X3 | Sign-off with fewer than ten clean days in a row | Refused; the manual path stays on | MSG-P2-014 | AC5 |
| X4 | JOB-02 did not run for D (late load) | No reconciliation for D; the day is not clean; the clean count restarts | MSG-P1-001 | AC6 |
| X5 | JOB-04 runs twice for D | The second run writes no new exception and no second alert | None | AC7 |
| X6 | A role without the right signs off | Refused; nothing changes | MSG-P4-002 | TC-E2-023-09 |
| X7 | Sign-off for an interface already retired | Refused; nothing changes | MSG-P2-019 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the hand-over run (RWB-E2-001) and the feeds (RWB-E1-051) |
| Negotiable | Threshold and clean days are parameters |
| Valuable | One checked path for the hand-over; the manual file ends |
| Estimable | One reconciliation step, one table, one endpoint |
| Small | Within one week with its tests |
| Testable | Each criterion below is one automated test |

## 7. Acceptance criteria

```gherkin
Feature: Automated EFS file load

  Background:
    Given parameter "recon.efs.alert_pct" is 0.1 and "recon.efs.clean_days_required" is 10

  Scenario: AC1 Reconciled
    Given the EFS data of business date 2026-12-14 in the COLLINS load hands over 104 accounts
    Given JOB-02 created 98 cases and linked 4 accounts for 2026-12-14
    When the reconciliation job runs
    Then the system compares the count of 104 accounts handed over with 102 accounts on cases
    Then the system lists the 2 differences as data quality exceptions with the account ID and the reason

  Scenario: AC2 Manual step retired
    Given the days 2026-12-03 to 2026-12-12 each reconciled with no difference
    When the data steward signs off on 2026-12-13
    Then the sign-off record holds the interface "INT-07", the dates 2026-12-03 to 2026-12-12, 10 clean days, the user and the time
    Then flag "rwb.integration.efs-manual-upload" is off in the environment
    Then the response carries message MSG-P2-015

  Scenario: AC3 Alert
    Given 2,000 accounts handed over on 2026-12-15 and 1,997 on cases, a difference of 0.15 percent
    When the job runs
    Then the data steward and the platform administrator are alerted with message MSG-P2-013

  Scenario: AC4 Small difference listed without an alert
    Given 2,000 accounts handed over on 2026-12-16 and 1,999 on cases, a difference of 0.05 percent
    When the job runs
    Then the system lists 1 difference
    Then the system sends no alert
    Then the system records the day as not clean

  Scenario: AC5 Sign-off too early
    Given 7 clean days in a row ending 2026-12-12
    When the data steward signs off
    Then the response is 409 with message MSG-P2-014
    Then flag "rwb.integration.efs-manual-upload" stays on

  Scenario: AC6 No hand-over run for the day
    Given JOB-02 did not run for business date 2026-12-17 because the load was late
    When the reconciliation job runs on 2026-12-18
    Then the system records no reconciliation for 2026-12-17
    Then 2026-12-17 counts as not clean and the clean count restarts at 0

  Scenario: AC7 Job run twice
    Given the reconciliation for 2026-12-15 listed 3 differences and sent 1 alert
    When the job is rerun for 2026-12-15
    Then the exception list still holds 3 differences for 2026-12-15
    Then the system sends no second alert

  Scenario: AC8 Sign-off after retirement refused
    Given the manual EFS file handling for "INT-07" was retired on 2026-12-13
    When the data steward signs off again on 2026-12-20
    Then the response is 409 with message MSG-P2-019
    Then the system writes no second sign-off record
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every account handed over from EFS has exactly one open case each day, reconciled each day | CTL-01; REC-01; REQ-RDF-007 |
| BR2 | Every difference is listed with its account and reason for the data steward | REC-01, Break goes to; REQ-RDF-008 |
| BR3 | A difference above the alert threshold alerts the data steward and the platform administrator; threshold 0.1 percent, assumed | DL25 |
| BR4 | A clean day is a day with a reconciliation and no difference | Story intent |
| BR5 | The manual EFS file handling ends only after ten clean days in a row and the data steward's sign-off, and the sign-off is kept | REQ-RDF-006 |
| BR6 | A repeat run for the same business date adds nothing | R-UNI-40 |
| BR7 | Threshold and clean days are parameters, never code | Principle 1 |

## 9. State transitions

None. This story does not change a case status. It writes the day result (clean or not) per business date, the sign-off record, and turns flag `rwb.integration.efs-manual-upload` from on to off.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the differences; signs off the retirement (Reference data, RU) |
| RW-PLATADM, platform administrator | Receives alerts; reruns JOB-04 (Platform administration, U) |
| SY-DATALOAD, data load | Runs the reconciliation and writes the exceptions and the day result |
| RW-AUDIT, RW-COMPLY | Read the sign-off record (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-CAS-028 | case_account | linked_from | Read |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-OPS-158 | interface_run | checks | Write |
| DF-OPS-161 to DF-OPS-167 | interface_signoff | all fields | Write |
| DF-OPS-162 | interface_signoff | interface_id | Write |
| DF-OPS-163 | interface_signoff | from_date | Write |
| DF-OPS-164 | interface_signoff | to_date | Write |
| DF-OPS-165 | interface_signoff | clean_days | Write |
| DF-OPS-166 | interface_signoff | signed_by | Write |
| DF-OPS-167 | interface_signoff | signed_at | Write |
| DF-OPS-215 | feature_flag | uat_on | Write |
| DF-OPS-216 | feature_flag | prod_on | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step: EFS hand-over reconciliation in JOB-04 Daily reconciliation.** Trigger: daily after JOB-02. Input: EFS hand-over accounts for D; JOB-02 run summary for D. Output: data quality exceptions, the day result, the alert. Events: none. Idempotency key: "INT-07:" + business date. Restart: a rerun replaces the day result and writes only exceptions not already listed for D; the alert is sent once per business date.

**Endpoints.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/data-quality/exceptions?product=DP05&from=2026-12-14 | Query: product, from, to | Array of DataQualityException: id, product, check, record, raisedOn | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only |
| POST /admin/interfaces/{interfaceCode}/manual-retirement (new, recorded in additions) | ManualRetirementRequest: note (up to 500 characters) | 201 InterfaceSignoff: interfaceId, fromDate, toDate, cleanDays, signedBy, signedAt | 401; 403 (MSG-P4-002); 404 unknown interface (MSG-P4-003); 409 too few clean days (MSG-P2-014) or already retired (MSG-P2-019) | Reference data, U | One sign-off per interface; a repeat returns 409 |

**Published interfaces called.**

```java
// P1 recovery.data.api
List<UUID> EfsHandoverQuery.handedOver(LocalDate businessDate);
void DataQualityExceptions.add(String dataProduct, String check, String recordKey, LocalDate businessDate, String reason);
// P2 recovery.integration.handover.api (RWB-E2-001)
HandoverSummary HandoverRun.summary(LocalDate businessDate);
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/efsrecon`, Java package `recovery.integration.efsrecon`.

| Component | Type | Responsibility |
|---|---|---|
| EfsReconService | Service | Compares the two lists, writes exceptions, the day result and the alert |
| EfsReconStep | Job | Step of JOB-04 |
| CleanDayCounter | Service | Counts clean days in a row back from the last business date; a missing day breaks the count |
| ManualRetirementController | Controller | POST /admin/interfaces/{interfaceCode}/manual-retirement |
| ManualRetirementService | Service | Checks clean days, writes the sign-off, switches the flag off through FeatureFlagService |
| InterfaceSignoffRepository | Repository | interface_signoff only |

- **Database:** Flyway migration `V2026_12_23__p2_interface_signoff.sql` creates interface_signoff with the standard columns and a unique constraint on interface_id.
- **Configuration and reference data:** parameters recon.efs.alert_pct = 0.1 (assumed; DL25) and recon.efs.clean_days_required = 10 (RW-COE); flag rwb.integration.efs-manual-upload (RW-PLATADM).
- **Build steps:**
  1. Build EfsReconService with the compare and the reasons, with tests for each reason.
  2. Build EfsReconStep in JOB-04 with the idempotency key and the once-per-date alert.
  3. Build CleanDayCounter with tests for a gap day and a day with one difference.
  4. Write the migration and InterfaceSignoffRepository.
  5. Build ManualRetirementService and the endpoint with the flag switch and the ACE audit write.
- **Feature flag:** `rwb.integration.efs-recon`.
- **Done when:** the tests in section 16 pass and ten synthetic clean days in SIT allow the sign-off.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-013 | Difference above the alert threshold | {count} EFS hand-overs for {date} do not match a case ({pct} percent). See the data quality exceptions. |
| MSG-P2-014 | Sign-off refused | {count} clean days in a row so far. Sign-off needs {required}. |
| MSG-P2-019 | Sign-off for an interface already retired | Manual handling for {interface} was already retired on {date}. |
| MSG-P2-015 | Sign-off accepted | Manual EFS file handling ended on {date}. The sign-off is recorded. |
| MSG-P1-001 | No hand-over run for a late load | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right signs off | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-45 Data quality, states loading and breaks: the data steward sees the EFS hand-over differences per business date. The sign-off is made through the endpoint from the same screen in Epic 2; alerts arrive by email.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-023-01 | AC1, BR1, BR2 | System | 104 synthetic hand-overs, 102 on cases |
| TC-E2-023-02 | AC2, BR5 | System | Ten clean synthetic days |
| TC-E2-023-03 | AC3, BR3 | System | 2,000 hand-overs, 3 differences |
| TC-E2-023-04 | AC4, BR4 | System | 2,000 hand-overs, 1 difference |
| TC-E2-023-05 | AC5, BR5 | System | Seven clean days |
| TC-E2-023-06 | AC6, BR4 | System | No JOB-02 run for 2026-12-17 |
| TC-E2-023-07 | AC7, BR6 | System | JOB-04 rerun for 2026-12-15 |
| TC-E2-023-08 | AC8, BR5 | System | Sign-off record for INT-07 already present |
| TC-E2-023-09 | Access | Access | RW-PLATADM (no Reference data U right) calls POST /admin/interfaces/{interfaceCode}/manual-retirement; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: threshold and clean days are parameters.
- No personal data in logs, tests or prompts; differences hold account IDs and reasons only.
- No read of another module's tables; hand-overs and exceptions go through the P1 interfaces.
- The manual path is switched off only through the sign-off.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Daily reconciliation with no variance | Program 5.1; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-023-01, TC-E2-023-03, TC-E2-023-04, TC-E2-023-07 |
| REQ-RDF-006 | Local copy retired with the owner's confirmation | Program 5.1; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | None | TC-E2-023-02, TC-E2-023-05, TC-E2-023-08 |
| REQ-CHO-001 | Hand-over reaches the Workbench with its history | Program 5.3; Epic 2 3.2 | FEAT-CHO-10 | 6.1 Take over the case at 90 days past due | None | TC-E2-023-06 |

## 19. Out of scope

- The reconciliation of all accounts at 90 days past due against open cases (REC-01): RWB-E1-003.
- Retiring the Excel and SharePoint trackers: RWB-E1-012.
- A same-day hand-over event: DL06.
