<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 051 Legacy feed jobs on ADF and Control M v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 051 Legacy feed jobs on ADF and Control M v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-051 Legacy feed jobs on ADF and Control-M

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-051 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | FEAT-RDF-22 Run legacy feed jobs on ADF and Control-M |
| Requirement IDs | REQ-DRI-008, REQ-RDF-002, REQ-RDF-003, REQ-RDF-004 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the ALS, EFS, CCMS and SVAF feed jobs scheduled on Control-M and ADF, each writing a run record and alerting on failure**, so that **the squad loads run every day or week without a manual step**.

## 2. Business rationale

ALS and EFS data reach the Workbench through the COLLINS daily batch, and CCMS and SVAF through weekly files (ADR-005). Today the extracts and file moves are started by hand. This story puts the four feeds on the bank schedulers, records each run in the Workbench and tests each file layout in the pipeline, so a changed source field is found before it reaches production. It meets REQ-DRI-008, REQ-RDF-002, REQ-RDF-003 and REQ-RDF-004.

## 3. Preconditions

- RWB-E1-001 (schema) and RWB-E1-007 (adapters, interface_run table) are done.
- SCB IT gives the platform administrator access to the Control-M folder and the ADF factory for the Workbench in DEV and SIT.
- The interface configuration rows for INT-01, INT-07, INT-10 and INT-11 are in force, version "IF-2026.11".
- The layout files for the four interfaces are in the repository under `contracts/`, built from the interface specifications and the source to target mapping.
- Synthetic sample files for the four interfaces are in `src/test/resources/contracts/`.

## 4. Flow

1. Platform administrator: commits the Control-M job definitions for the ALS and EFS extracts into COLLINS and the ADF pipelines for the CCMS and SVAF file moves to the `ops/` folder.
2. Pipeline: validates the definitions and deploys them to the environment through the bank's deployment path.
3. Control-M: runs the ALS and EFS extracts after COLLINS end of day; COLLINS completes its load before 05:00.
4. ADF: moves the weekly CCMS and SVAF files from the source drop folder to the Workbench SFTP inbound folder by Sunday 23:00 (assumed; DL12).
5. Scheduler: JOB-01 starts at 05:00 and reads the COLLINS load; JOB-09 starts Monday 04:00 and reads the CCMS and SVAF files through FileLoadAdapter.
6. SY-DATALOAD: each run writes an interface_run row with interface, business date, status, record count, start and end time.
7. SY-DATALOAD: on failure, the run row is FAILED or REFUSED, a structured event `rwb.integration.job.failed` is written to Log Analytics and the alert rule emails the data steward and the platform administrator with MSG-P2-004.
8. Pipeline: on every merge, the contract tests parse each sample file against its layout file and fail on any field that differs.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A Control-M or ADF job fails | The bank scheduler alerts the platform administrator; the Workbench run for that interface finds no file and is written as MISSING | MSG-P2-004 | AC4 |
| X2 | The COLLINS load has not arrived by 09:00 | JOB-01 stops retrying; the products are marked stale; the previous load stays in use | MSG-P1-001 | AC5 |
| X4 | A scheduler starts the same feed twice for one business date | The second Workbench run is written as DUPLICATE and loads nothing | None | AC6 |
| X5 | A role without the right reruns a feed job | Refused; nothing changes | MSG-P4-002 | TC-E1-051-07 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the adapters (RWB-E1-007); the loaders of each data product are separate stories |
| Negotiable | Times and folders are configuration rows and scheduler definitions held in the repository |
| Valuable | Removes the manual start of four feeds |
| Estimable | Four scheduler definitions, four layout files, four contract tests, one alert rule |
| Small | Within two weeks with its tests |
| Testable | Each criterion below is one automated test or a pipeline check |

## 7. Acceptance criteria

```gherkin
Feature: Legacy feed jobs on ADF and Control-M

  Background:
    Given the interface configuration rows for "INT-01", "INT-07", "INT-10" and "INT-11" are in force

  Scenario: AC1 Four jobs scheduled
    Given the Control-M definitions for the ALS and EFS extracts and the ADF pipelines for CCMS and SVAF are deployed in SIT
    When business date 2026-11-15 runs, with the CCMS and SVAF files moved on Sunday 2026-11-15
    Then JOB-01 writes run rows for "INT-01" and "INT-07" with status "LOADED" and start times from 05:00
    Then JOB-09 writes run rows for "INT-10" and "INT-11" on Monday 2026-11-16 with status "LOADED" and start times from 04:00
    Then each run row holds the business date, the record count and the start and end time

  Scenario: AC4 Alert on failure
    Given the ADF pipeline for CCMS fails on Sunday 2026-11-22
    When JOB-09 runs on Monday 2026-11-23 at 04:00
    Then the "INT-10" run row shows status "MISSING"
    Then the data steward and the platform administrator receive message MSG-P2-004 within 15 minutes (assumed; DL11)

  Scenario: AC5 COLLINS load late
    Given no COLLINS load for business date 2026-11-24 has arrived
    When JOB-01 retries at 06:00, 07:00, 08:00 and 09:00
    Then after the 09:00 attempt the run rows for "INT-01" and "INT-07" show status "MISSING"
    Then the account and arrears data product shows MSG-P1-001 with the date 2026-11-23

  Scenario: AC6 Feed started twice
    Given the "INT-07" load for business date 2026-11-25 is LOADED at 05:10
    When Control-M starts the EFS load again and JOB-01 is rerun at 05:40
    Then the system writes a run row with status "DUPLICATE"
    Then the system loads no EFS record a second time
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | ALS and EFS data arrive only through the COLLINS daily batch; CCMS and SVAF only through file loads | ADR-005; INT-01, INT-07, INT-10, INT-11 |
| BR2 | JOB-01 starts at 05:00 and retries hourly to 09:00; after that the previous load stays in use and the products are marked stale | batch.txt JOB-01 |
| BR3 | JOB-09 runs CCMS and SVAF weekly on Monday 04:00 | batch.txt JOB-09 |
| BR4 | Each run writes a run record and a failure alerts the data steward and the platform administrator | ifspec, Owner of the fix column; REQ-DRI-007 |
| BR5 | A changed source field fails the contract test and names the field | CTL-02 structure check; DQ-002, DQ-037, DQ-058, DQ-065 |
| BR6 | A repeat load for the same business date is not loaded twice | DQ-001, DQ-036, DQ-057, DQ-064 business date check |

## 9. State transitions

None. This story does not change a case status. It writes interface_run rows with status LOADED, MISSING, FAILED, REFUSED or DUPLICATE.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Maintains the Control-M and ADF definitions; reruns a feed job (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the alerts; reads run rows (Platform administration, R) |
| SY-DATALOAD, data load | Runs JOB-01 and JOB-09 and writes the run rows |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run rows (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-137 | interface_config | interface_id | Read |
| DF-OPS-140 | interface_config | inbound_path | Read |
| DF-OPS-141 | interface_config | file_pattern | Read |
| DF-OPS-142 | interface_config | data_product | Read |
| DF-OPS-146 | interface_config | alert_role | Read |
| DF-OPS-149 to DF-OPS-160 | interface_run | all fields | Write |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-COL-002 | collateral | collateral_no | Read, contract test only |
| DF-COL-021 | valuation | appraisal_no | Read, contract test only |
| DF-COL-023 | valuation | appraised_value | Read, contract test only |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job JOB-01 COLLINS load check and intake.** Trigger: Quartz, daily 05:00, retried hourly to 09:00. Input: the COLLINS load for INT-01 and INT-07. Output: interface_run rows; records to the P1 loaders. Events: P1 publishes LoadCompleted (EV-26) or LoadRefused (EV-27). Idempotency key: interface_id + business_date. Restart: POST /admin/jobs/{jobId}/rerun reruns from the failed step; a run already LOADED for the key writes DUPLICATE.

**Job JOB-09 File loads.** Trigger: Quartz, weekly Monday 04:00 for INT-10 and INT-11. Input and output as in RWB-E1-007. Idempotency key: interface_id + business_date + file hash.

**Bank scheduler definitions.** Control-M jobs `RWB_ALS_EXTRACT` and `RWB_EFS_EXTRACT` and ADF pipelines `rwb-ccms-file-move` and `rwb-svaf-file-move`, held as JSON in `ops/control-m/` and `ops/adf/`. The names are proposed until SCB IT issues the bank standard names (DL12).

**Endpoints.**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/jobs?type=INT-10&from=2026-11-16 | Query: type, status, from, to | Array of Job: id, type, businessDate, status, startedAt, endedAt, checks | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only |
| POST /admin/jobs/{jobId}/rerun | Path: jobId | Job | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 409 job running (MSG-P2-006); 503 | Platform administration, U | A rerun of a LOADED key writes DUPLICATE |

**Contract test interface (package recovery.integration.feeds.contract).**

```java
public interface LayoutContract {
    ContractResult check(String interfaceId, Path sampleFile); // result lists each field that differs from the layout file
}
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/feeds`, Java package `recovery.integration.feeds`; scheduler definitions in `ops/control-m/` and `ops/adf/`; layout files in `contracts/`.

| Component | Type | Responsibility |
|---|---|---|
| FeedRunRecorder | Service | Writes the interface_run row at start and end of each feed run; writes the failure event |
| LayoutContractImpl | Service | Reads a layout file (field, type, length, mandatory) and checks a sample file against it |
| FeedContractTest | Test | One parameterized test per interface: INT-01, INT-07, INT-10, INT-11 |
| CollinsIntakeJob | Job | JOB-01 entry point; hourly retry to 09:00 from property values |
| FileLoadJob | Job | JOB-09 entry point, from RWB-E1-007 |
| JobFailureAlert | Rule table | Log Analytics alert rule on `rwb.integration.job.failed`, held as code in `ops/monitoring/` |

- **Database:** reads and writes interface_run and reads interface_config, both created by RWB-E1-007. No migration.
- **Configuration and reference data:** interface_config rows INT-01, INT-07, INT-10, INT-11 (RW-REFADM); properties `rwb.jobs.collins.start` = 05:00, `rwb.jobs.collins.last-retry` = 09:00, `rwb.jobs.files.weekly-cron` = Monday 04:00; Control-M and ADF definitions owned by RW-PLATADM.
- **Build steps:**
  1. Write the four layout files from ifspec and s2t and the synthetic sample files.
  2. Build LayoutContractImpl and FeedContractTest; add the test to the merge pipeline.
  3. Build FeedRunRecorder and call it from CollinsIntakeJob and FileLoadJob.
  4. Build the hourly retry window in CollinsIntakeJob with the MISSING outcome after the last retry.
  5. Write the Control-M and ADF definitions and the pipeline step that validates them.
  6. Write the Log Analytics alert rule and test it with a forced failure in SIT.
  7. Add the four feeds to the JOB-01 and JOB-09 run books (RWB-E1-056 format).
- **Feature flag:** `rwb.integration.legacy-feeds`.
- **Done when:** the tests in section 16 pass and one full week of the four feeds runs in SIT with no manual start.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-002 | Contract test finds a field that differs | Field {field} in {interface} does not match the interface specification: expected {expected}, found {found}. |
| MSG-P2-004 | Feed job failed or file missing | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P1-001 | Data product stale after a late load | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-006 | Rerun while the job runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns a job | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The platform administrator and the data steward see run rows through GET /admin/jobs and the Log Analytics workbook "Recovery jobs"; SCR-44 Interface and job monitor comes in Epic 2. Alerts arrive by email.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-051-01 | AC1, BR1, BR2, BR3 | System | Synthetic COLLINS load and CCMS and SVAF files for 2026-11-15 |
| TC-E1-051-03 | BR5 | System | SVAF sample file with "Appraised Value" as text |
| TC-E1-051-04 | AC4, BR4 | System | ADF CCMS pipeline forced to fail |
| TC-E1-051-05 | AC5, BR2 | System | No COLLINS load for 2026-11-24 |
| TC-E1-051-06 | AC6, BR6 | System | EFS load started twice for 2026-11-25 |
| TC-E1-051-07 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: times, folders and retry windows are configuration rows or properties.
- No personal data in logs, tests or prompts; sample files are synthetic and run rows hold counts only.
- No read of another module's tables; records reach P1 only through its loaders.
- No direct call from the Workbench to ALS, EFS, CCMS or SVAF; the bank schedulers deliver to COLLINS and to the inbound folder.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-008 | Data moves by COLLINS or a file load | Program 5.2; Epic 1 3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, TC-E1-051-06 |
| REQ-RDF-002 | Account data current to the previous working day | Program 5.1; Epic 1 3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, TC-E1-051-05 |
| REQ-RDF-003 | EFS history reaches the case | Program 5.1; Epic 1 3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, TC-E1-051-06 |
| REQ-RDF-004 | Collateral and appraisals without a lookup in CCMS or SVAF | Program 5.1; Epic 1 3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, TC-E1-051-03, TC-E1-051-04 |

## 19. Out of scope

- The loaders and record checks for each data product: RWB-E1-003, RWB-E1-004 and RWB-E1-009.
- AMIS, RPS and GL feeds: Epic 3 and Epic 6.
- Run books for every other Epic 1 job: RWB-E1-056.
- The SCR-44 monitor screen: Epic 2.
