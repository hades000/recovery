# RWB-P3-E1045-APP Multi-product parameters for Mortgage, HP and SSME

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1045-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-045 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP11, DP13, DP14, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | Day 1 |
| Size (INVEST Small) | Fits two weeks; numeric size set by the squad at refinement. Not specified in the source documents (DOR-RWB-P3-E1045-APP-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1 (the /v1 path of this story's contracts) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P3-E1045-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-E1-045 to rwb-case with behaviour unchanged. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1045-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product group in the versioned parameter and reference data of rwb-case, read only through the parameters contract of rwb-case (DP-06) and the reference-data contract of rwb-case (DP-07), with the notice and cure clocks running as durable Temporal timers inside CaseWorkflow on task queue `rwb-case` and their due dates computed by the CalculateDueDate activity from those values**, so that **a new product or a product change needs no code change**.

### 2. Business rationale

Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.

In the target, PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL are versions in the reference-data service of rwb-case: the catalog and its dated values in `parameter_catalog` and `parameter_value` (DF-REF-132 to DF-REF-158), the table versions and their rows in `reference_version` and `reference_row` (DF-REF-159 to DF-REF-184), and the lists in `lov_value`, all in schema `rwb_case`, owned by P3 under the R-PREC default ruling that gives parameters and reference data (E1-042, E1-043) to rwb-case (Template and Rules §R3; Ownership Map). The load and the completeness check now run inside the reference-data service of rwb-case, and every engine reads a value through the contract and its client library, never from a table of another service (DP-06, DP-07; DP-01). No service holds a product value, a product name or a period in code.

The clock changes shape as well. What the legacy story wrote as a `timer` row from a five-minute check is now a durable Temporal timer inside CaseWorkflow on task queue `rwb-case`: JOB-05 Timer check and the TimerDue event are retired, and the `timer` row is kept only as the screen projection behind `GET /cases/{caseId}/timers` (Architecture v5 slides 42 and 44; Ownership Map ruling ASM-0078). The due date is computed in the CalculateDueDate activity, which is where the value in force, its unit and the holiday calendar meet, and the reference version the calculation used is written to the local decision record through the decision-record library and published as DecisionRecorded on `rwb.decision-record.v1` (DP-03).

The holiday calendar moves behind the rwb-source-data contract (DP-05): rwb-case no longer reads the `v_ace_holiday` view itself, so a change in the ACE public-holiday list is absorbed in one service (Architecture v5 slide 45, "Who reads ACE's data?").

### 3. Preconditions

- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case with the client library, the catalog fields `scope` (DF-REF-140) and `required` (DF-REF-141), the dated value row `parameter_value`, and the build rule that fails on a parameter read that the catalog does not list (DP-06; FSD P3 A2.22).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case with the client library, the version and row shapes of `reference_version` and `reference_row`, the load, approve and rollback operations of the reference-data service, and its table checks (DP-07; FSD P3 A2.23).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1`, so the reference version a due date was computed from is recorded and published in the same transaction as the timer projection (DP-03).
- RWB-PLT-E1072-CON is published: the embedded Drools kit, so the engines that consume these values (entry, allocation, transfer) evaluate their packages with the rule version in force beside the parameter version in force (DP-04).
- RWB-PLT-E1047-CON is published: the topic and event naming library, so the one published event carries its agreed name and envelope (DP-14).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the case record and the exception queue, so the timer projection and the refusal messages reach a person without a second screen model in this service (DP-19).
- Tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force, and the catalog marks each parameter with scope PRODUCT or GLOBAL, required yes or no, type, unit and allowed range.
- The loader holds RW-COE or RW-REFADM (Reference data C); the approver holds the approve right in Reference data, and an author never approves the same version.
- The `timer` and `task` rows and the CaseWorkflow wiring exist in schema `rwb_case` from their own stories: CaseWorkflow runs on task queue `rwb-case`, the CalculateDueDate, EvaluateRules and RecordAndApply activities are registered on that queue, and the notice timer is started on a task that carries the owner role. This story adds no column to either table.
- The engines that consume a product value (case creation, allocation, the stage clocks) are switchable, so the value can be moved behind the client library without a second release.
- The login is the rwb-case login (DP-02): one login and one connection pool for the service, with grants on schema `rwb_case` only.

### 4. Flow

1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status; the values are the business's, never the code's.
2. Reference data administrator: loads each file through the load operation of the reference-data service of rwb-case (`POST /admin/reference-loads`, owner P3, carried by RWB-P3-E1043-APP), with the table code and the valid-from date; the call stays inside rwb-case, so no contract of another service is called.
3. Reference-data service: runs the RWB-E1-043 checks (content hash, row count, dry-run counts, valid-from discipline), then the product completeness check: every product in the PRODUCT version in force on the valid-from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.
4. Reference-data service: checks each value against the catalog type and range, and refuses a second row for the same product group and parameter code inside one version.
5. Approver: approves the version; it takes effect on its valid-from date and the version before it stays readable up to the day before, so a decision can always name the version in force on its business date.
6. CaseWorkflow: when a notice or a cure clock starts on a case, the CalculateDueDate activity reads the period through the parameters contract of rwb-case, `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)`, takes the unit from the same answer, and adds calendar days or working days; for working days it reads the holiday calendar through the rwb-source-data contract, never from an ACE view (DP-05). The activity writes `timer.expires_at` and `timer.warn_at` in the `timer` projection of schema `rwb_case` and returns the expiry to the workflow, which waits on a durable Temporal timer until that date.
7. Case creation and allocation: read the entry threshold, the exclusion list and the exposure bands for the case's product group the same way, through the parameters contract; a product group that has no value in force is never guessed from a default.
8. Each engine: writes the PRODUCT_PARAMETER version it used, with the table code and the version number, into its decision record through the decision-record library, and publishes the event rwb.decision.DecisionRecorded.v1 on `rwb.decision-record.v1` in the same transaction as its own change, so an auditor can name the version behind every deadline and every entry decision.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product has no SERVICE_LEVEL row for a required status | The load is refused in full and the missing product and status are named | MSG-P3-034 | AC3 |
| X2 | A parameter value is outside the catalog range or of the wrong type | The load is refused in full | MSG-GEN-002 | AC4 |
| X3 | Two rows for the same product and parameter | The load is refused in full | MSG-P3-027 | AC5 |
| X4 | A PRODUCT version removes a product that still has open cases | The load is refused in full; the open case count is read from `recovery_case` in rwb_case, not from another service | MSG-P3-027 | AC6 |
| X5 | At run time a case's product has no parameter row in force | The CalculateDueDate activity throws `MissingProductParameterException`; no timer is set and no durable timer starts; the case goes to the exception queue; the gap is named | MSG-P3-034 | AC7 |
| X6 | A parameter changes while a timer is running | The running timer keeps its expiry; new timers use the new value from its valid-from date | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the P3 contract stories and their fakes only: the parameters and reference-data contracts of rwb-case, the decision-record and Drools platform contracts and the composite route. The rwb-source-data holiday answer comes from its contract fake, so neither the source-data service nor an ACE view is needed in the development environment |
| Negotiable | The parameter list and every value are data; the story fixes the lookup, the completeness check and the point where the due date is computed |
| Valuable | A product change becomes a reference load approved by its owner, and every deadline names the value version behind it |
| Estimable | Two read clients, one completeness check, one due-date calculation in one activity, one projection repository, two read operations |
| Small | Fits in one week with its tests |
| Testable | Every owned criterion has a test case in section 16; each cross-service answer is stubbed in a contract fake and real in SIT |

### 7. Acceptance criteria

```gherkin
Feature: Multi-product parameters for Mortgage, HP and SSME

  Background:
    Given the business date is 2026-12-01
    Given PRODUCT_PARAMETER version 2 is in force with NOTICE_PERIOD_DAYS 30 calendar days for "MORTGAGE" and 60 calendar days for "HIRE_PURCHASE"
    Given PRODUCT version 1 is in force with "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"

  Scenario: AC1 Product value differs (legacy RWB-E1-045 AC1)
    Given case "RW-2026-000101" with product group "MORTGAGE" and case "RW-2026-000102" with product group "HIRE_PURCHASE"
    When the timer engine sets the notice timer on both cases on 2026-12-01
    Then the notice timer of "RW-2026-000101" expires on 2026-12-31
    Then the notice timer of "RW-2026-000102" expires on 2027-01-30
    Then each timer start records PRODUCT_PARAMETER version 2

  Scenario: AC2 New product added (legacy RWB-E1-045 AC2)
    Given PRODUCT version 2 adds product group "AUTO_LEASE" with valid from 2026-12-05
    Given PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 add every required row for "AUTO_LEASE" with valid from 2026-12-05
    Given all three versions are approved
    Given the rwb-source-data contract mock returns an AUTO_LEASE account at 90 days past due on 2026-12-05
    When the ACE data for 2026-12-05 holds an "AUTO_LEASE" account at 90 days past due
    Then the system creates a case with product group "AUTO_LEASE"
    Then the system sets its timers from the "AUTO_LEASE" rows
    Then no deployment took place between 2026-12-01 and 2026-12-05

  Scenario: AC3 Missing parameter blocked (legacy RWB-E1-045 AC3)
    Given a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER"
    When the load validates
    Then the system refuses the load with MSG-P3-034 naming "SSME" and "WAITING_PARTNER"
    Then SERVICE_LEVEL version 3 stays in force

  Scenario: AC4 Value outside its range (legacy RWB-E1-045 AC4)
    Given the catalog range for NOTICE_PERIOD_DAYS is 1 to 365
    When a PRODUCT_PARAMETER load sets NOTICE_PERIOD_DAYS to 0 for "SSME"
    Then the system refuses the load with MSG-GEN-002 naming "NOTICE_PERIOD_DAYS", 1 and 365

  Scenario: AC5 Duplicate product row (legacy RWB-E1-045 AC5)
    Given a PRODUCT_PARAMETER load with two NOTICE_PERIOD_DAYS rows for "MORTGAGE", 30 and 45
    When the load validates
    Then the system refuses the load with MSG-P3-027 naming "MORTGAGE" and "NOTICE_PERIOD_DAYS"

  Scenario: AC6 Product removed while cases are open (legacy RWB-E1-045 AC6)
    Given 3 open cases with product group "UNSECURED"
    When a PRODUCT load with valid from 2026-12-15 leaves out "UNSECURED"
    Then the system refuses the load with MSG-P3-027 naming "UNSECURED" and 3 open cases

  Scenario: AC7 No parameter in force at run time (legacy RWB-E1-045 AC7)
    Given case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force
    When the timer engine sets the notice timer on 2026-12-01
    Then the system writes no notice timer
    Then the system places the case in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS"

  Scenario: AC8 Value changes while a timer runs (legacy RWB-E1-045 AC8)
    Given the notice timer of "RW-2026-000101" started on 2026-12-01 and expires on 2026-12-31
    Given PRODUCT_PARAMETER version 4 with NOTICE_PERIOD_DAYS 45 for "MORTGAGE" takes effect on 2026-12-03
    When the timer engine sets a notice timer on Mortgage case "RW-2026-000150" on 2026-12-03
    Then the timer of "RW-2026-000101" still expires on 2026-12-31
    Then the timer of "RW-2026-000150" expires on 2027-01-17

  Scenario: AC9 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given a request to a provided operation carries no valid credential
    When the request is sent
    Then the response status is 401
    Given a request to a provided operation comes from a caller without permission
    When the request is sent
    Then the response status is 403
    Given a request to GET /cases/{caseId}/timers names a case that does not exist
    When the request is sent
    Then the response status is 404

  Scenario: AC10 An activity that fails is retried and timed out (new, D-RCV-60)
    Given an activity of CaseWorkflow fails on its first attempt
    When the activity is retried
    Then the retry count is Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC10)
    Given an activity of CaseWorkflow does not finish in time
    When the timeout elapses
    Then the timeout is Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC10)

  Scenario: AC11 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-source-data contract mock fails or does not answer for the ACE data
    When the timer engine sets the notice timer
    Then the failed call is handled as Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC11)

  Scenario: AC12 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case whose status does not allow the requested change
    When the status change is requested
    Then the system refuses the change with Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC12)
    Then the case status stays unchanged
```

**Note.** The eight criteria are the ones this story owns, copied word for word from RWB-E1-045 with one added Given in AC2: the "rwb-source-data contract mock returns an AUTO_LEASE account at 90 days past due on 2026-12-05" line stands in for the rwb-source-data answer that the ACE data would carry, so the criterion proves the product parameter load and not the source-data service. In the target the notice timer is a durable Temporal timer inside CaseWorkflow and `timer` is its projection, so AC1, AC7 and AC8 read the result through `GET /cases/{caseId}/timers`, and AC2 proves that a new product group gets its case and its timers from the new rows; AC3 to AC6 prove the completeness check inside the reference-data service of rwb-case. No value in any criterion is new.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every product-specific value is a PRODUCT_PARAMETER or SERVICE_LEVEL row keyed by product group and read through the parameters contract of rwb-case; no engine holds a product value or a product name in code | Principle 1; DT02; DP-06 |
| BR2 | The parameters required per product are those the catalog marks with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. Values per product are the business's (entry 90 days, DL16; service levels DL22; caps DL23) | RWB-E1-042 catalog; DL16; DL22 |
| BR3 | Every product in force has one SERVICE_LEVEL row per status in `servicelevel.required-statuses` (assumed NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL; DL22; the list itself is Not specified in the source documents (GAP-0760; ASM-1382)) | REQ-CWC-011; casemodel.txt Case status |
| BR4 | A load that leaves a required row missing, a value out of range or a duplicate key is refused in full; the check runs inside the reference-data service of rwb-case | CTL-08; refdata.txt Change process step 3; DP-07 |
| BR5 | A product with open cases cannot be removed from PRODUCT; the count is taken from `recovery_case` in schema rwb_case | R-UNI-38 |
| BR6 | A timer takes the value in force on the date it starts and keeps it; new values apply from their valid-from date, and the version used is named on the decision record | R-UNI-38; DP-03 |
| BR7 | A value in unit WORKING_DAYS skips the public holidays returned by the rwb-source-data contract; a value in CALENDAR_DAYS does not. rwb-case reads no ACE view for the calendar | refdata.txt Reference tables; DP-05 |
| BR8 | A case whose product has no required value in force is not timed and goes to the exception queue; R-UNI-41 handles the case once a person decides | Principle 5; R-UNI-41 |

### 9. State transitions

None on the case. This story does not change a case status. It changes how the notice and cure clocks set `timer.expires_at` and adds the completeness check to reference version validation (status VALIDATED or refused, RWB-P3-E1043-APP). A case sent to the exception queue under X5 keeps status New or its current status.

| Object | From | Event | Condition | To | Note |
|---|---|---|---|---|---|
| timer (projection) | None | A notice or cure clock starts and the CalculateDueDate activity computes the due date | A PRODUCT_PARAMETER row is in force for the product group on the business date | RUNNING | The row is the screen projection of the durable Temporal timer and carries `started_at`, `expires_at` and `warn_at` |
| timer (projection) | RUNNING | The durable Temporal timer inside CaseWorkflow reaches `expires_at` | No payment and no cure clears the clock first | EXPIRED | The clock is a durable Temporal timer and not a five-minute job; the case status does not change |
| recovery_case | Any status | X5 — no PRODUCT_PARAMETER row is in force | The CalculateDueDate activity throws `MissingProductParameterException` | Same status, queue set to the exception queue | No timer row is written and no durable timer starts; MSG-P3-034 names the gap |

No row above moves a case status: the clock is now a durable Temporal timer inside CaseWorkflow, its expiry no longer moves the case by itself, and the stage clock behaviour belongs to RWB-P3-E1028-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Prepares and loads PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-REFADM, reference data administrator | Loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C); has no Case record right and is refused on the timer read |
| RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |
| RW-RISK, risk and model risk officer | Approves a version where a limit or threshold moves, and never approves a version they authored (refdata.txt Change process step 4; assumed approve right as in RWB-E1-043) |
| rwb-case service identity (the rwb-case login, DP-02) | Runs the completeness check inside the reference-data service, reads the parameter and reference answers, computes the due date in the CalculateDueDate activity and writes the timer projection |
| Drools evaluator (SY-RULES identity) | Reads product values for allocation and entry through the parameters contract, never from a copy (Rules and parameters R; DP-04) |
| Decision-record library identity | Writes the local decision record of a timer start and publishes DecisionRecorded on `rwb.decision-record.v1` (Decision log C; DP-03) |
| rwb-access authorise check (DP-08) | Authorises each REST operation of this story before it runs; a refused call gets the message of section 14 that fits the refusal |

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Write (exception queue under X5) |
| DF-WRK-028 | timer | case_id | Write |
| DF-WRK-030 | timer | timer_type | Write |
| DF-WRK-031 | timer | started_at | Write |
| DF-WRK-032 | timer | expires_at | Write |
| DF-WRK-033 | timer | warn_at | Write |
| DF-REF-160 | reference_version | table_code | Read |
| DF-REF-161 | reference_version | version_no | Read |
| DF-REF-183 | reference_row | row_key | Read |
| DF-REF-184 | reference_row | row_data | Read |
| DF-REF-140 | parameter_catalog | scope | Read |
| DF-REF-141 | parameter_catalog | required | Read |

The timer rows are the screen projection behind `GET /cases/{caseId}/timers`; they are written by the CalculateDueDate activity together with the decision record of that timer start, and the clock that fires is the durable Temporal timer inside CaseWorkflow (Ownership Map ruling ASM-0078). The holiday calendar is read only through the rwb-source-data contract inside the same activity: rwb-case holds no copy of a holiday row and reads no ACE view (DP-05, DP-01). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/parameters` | Read the parameter catalog with the value in force per environment and product group, so a person can see the value behind a due date; a secret parameter is listed without its value | Rules and parameters R, scope applied | Not applicable |
| GET | `/cases/{caseId}/timers` | Read the clocks of a case: stage, service level, prescription and notice, as the projection the durable timer writes; used by AC1, AC2, AC8 | Case record R, scope applied | Not applicable |

The timers answer is `Timer[]` (`timerType`, `startedAt`, `expiresAt`, `warnAt`, `status`) ordered by `expiresAt` ascending, with the reference version behind a due date on the decision record and not on the timer. Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 unknown case or out of scope (MSG-P4-003), 503 store down. Idempotency is not applicable to a read. The load, approve, verify and rollback operations of the reference-data service are its own surface, carried by RWB-P3-E1043-APP, and this story adds no operation to them.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| Activity read inside the CalculateDueDate activity | Holiday calendar read on the rwb-source-data contract; operation name and path: Not specified in the source documents (GAP-0759; ASM-1380) | rwb-source-data (P1) | The public holidays of a date range, so a value in unit WORKING_DAYS can be added without reading an ACE view (DP-05) | One hop, 2 s (DP-11) |

One call, no chain: the holiday answer is read inside the activity that computes the due date, so CaseWorkflow never calls a service from workflow code. The parameters and reference-data answers are not REST calls of this story: they arrive through the published client libraries of rwb-case (DP-06, DP-07).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | decision code, the table code and the version number in force, the product group, the business date and the record reference |

The event is written to the outbox in the same transaction as the timer projection and the decision record and relayed with the CloudEvents envelope; it carries IDs, codes and dates only, never a customer key and never a product value (DP-03).

#### 12.4 Events consumed

None. The load and the completeness check are synchronous; the rule version in force reaches the evaluating services through their own RulePackageInForce consumption and this story consumes nothing.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Waits on the durable notice and cure timers this story's calculation produces; adds no workflow of its own |
| CalculateDueDate | Activity | `rwb-case` | Reads the period and its unit through the parameters contract, adds calendar or working days with the holiday calendar from the rwb-source-data contract, writes the `timer` projection and the decision record in one transaction |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Evaluates the entry, allocation and transfer packages with the embedded Drools kit, using the product values this story publishes (DP-04) |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the state change and the outbox rows in one transaction, including the reference version in force |

#### 12.6 Schedules

None. A notice or cure clock is a durable Temporal timer inside CaseWorkflow and not a Schedule; JOB-05 Timer check is retired (Architecture v5 slide 44; Ownership Map ruling ASM-0078). This story registers no Schedule and carries no daily parameter check.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| parameter_catalog | P3 (rwb_case) | The definition of every parameter: key, kind, type, unit, range, default, scope, required, owner role (DF-REF-132 to DF-REF-146) |
| parameter_value | P3 (rwb_case) | The approved, dated value per environment and product group (DF-REF-147 to DF-REF-158) |
| reference_version | P3 (rwb_case) | One version of PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL with author, approver, row count and content hash (DF-REF-159 to DF-REF-180) |
| reference_row | P3 (rwb_case) | One row of a version, keyed by `row_key` with its `row_data` (DF-REF-181 to DF-REF-184) |
| lov_value | P3 (rwb_case) | The list values, including LOV-PRODUCT, LOV-PARAM-SCOPE and LOV-CASE-STATUS, read with their version (DP-07) |
| timer | P3 (rwb_case) | The screen projection of the durable timer: type, start, expiry, warning point, paused flag, status (DF-WRK-027 to DF-WRK-044) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects of the platform library |

rwb-case reads no table of another service and holds no foreign key across services (DP-01). The holiday calendar is not a table of this schema: it is read through the rwb-source-data contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | The holiday calendar answer for the 2026-12-31 year end and for 2027-01-30, and a delayed answer beyond 2 s (operation name and path Not specified in the source documents (GAP-0759; ASM-1380)) |
| Parameters contract fake of rwb-case | The DP-06 client library of RWB-P3-E1042-CON | `parameter_catalog` and `parameter_value` answers for NOTICE_PERIOD_DAYS 30 and 60, 45 from 2026-12-03, CURE_PERIOD_DAYS, and `servicelevel.required-statuses` |
| Reference-data contract fake of rwb-case | The DP-07 client library of RWB-P3-E1043-CON | PRODUCT versions 1 and 2, PRODUCT_PARAMETER versions 2, 3 and 4 and SERVICE_LEVEL version 3 with their valid-from dates, the version in force per business date, and the refusal answers MSG-P3-034, MSG-P3-027 and MSG-GEN-002 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | Parameters and timers provided; the holiday calendar consumed inside the activity; one hop, 2 s timeout |
| Kafka | 1 published, none consumed | DecisionRecorded on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities | CaseWorkflow holds the durable timer; CalculateDueDate computes the date, EvaluateRules reads the values, RecordAndApply writes the record and the outbox row |
| File | 1 in, through the reference-data contract | The PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL load files are uploaded to the reference-data service of rwb-case; this story reads no file itself |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `refdata`, Java package `th.co.scb.ace.workbench.recovery.case.refdata`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | The monolith base path of the legacy API (Template and Rules §R5.5, DP-13) | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and the shared `rwb.decision-record.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The same-service contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON and the platform contracts RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON are class H dependencies and are not DP rows. The C dependency of DP-04 belongs to the packages that consume these values and is carried where they are governed; this story's own contract dependencies are None (Template and Rules §R5.4).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ProductParameterServiceClient | Client | Reads `parameter_catalog` and `parameter_value` through the parameters contract of rwb-case with the version in force; throws `MissingProductParameterException` when no row is in force (DP-06) |
| ReferenceDataClient | Client | Reads `reference_version`, `reference_row` and `lov_value` through the reference-data contract of rwb-case; resolves PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL for a business date (DP-07) |
| ParameterVersionResolver | Service | Resolves the version in force for a product group, parameter code and business date, and returns the value, its unit and the table code and version number so the caller can record them |
| ProductCompletenessCheck | Service | The load check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL: required rows, catalog type and range, duplicate key, products with open cases |
| OpenCaseCounter | Repository | Counts open cases by product group in `recovery_case` (status not CLOSED) inside schema rwb_case |
| DueDateCalculator | Service | Adds calendar days or working days, reading the holiday calendar through the rwb-source-data contract (DP-05); called by the CalculateDueDate activity |
| TimerProjectionRepository | Repository | Writes and reads the `timer` projection rows of a case in schema rwb_case; no write to any other schema |
| ProductParameterController | Controller | `GET /admin/parameters` and `GET /cases/{caseId}/timers`, with the right and the scope check behind each |
| DecisionRecordWriter | Library client | Writes the local decision record of a timer start or a refusal and its outbox row in the same transaction (DP-03) |

**Database and migrations**

- No new table. This story reads `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`, `lov_value` and `recovery_case`, and writes `timer`, `recovery_case.queue_id` and the outbox, all in schema `rwb_case`.
- Migration in the `V0001` to `Vnnnn` form of the per-service Flyway sequence of rwb-case, using the next free number of that sequence (the number is Not specified in the source documents (CG-ALL-3765)), adds three indexes and no column: `ix_case_status_queue ON recovery_case (status, queue_id)` for the open-case count, `ix_timer_case_expiry ON timer (case_id, expires_at)` for the timers answer, and `ix_parameter_value_lookup ON parameter_value (param_key, product_group, valid_from)` for the version-in-force lookup.
- Uniqueness of a version and of a row is enforced by the reference-data service baseline of RWB-P3-E1043-APP and is not re-created here; the duplicate-row refusal of AC5 is that constraint plus the completeness check.

**Configuration and reference data**

- PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions, loaded by the reference data administrator and owned by the product heads (values per DL16, DL22, DL23).
- Catalog entries for the five parameters of BR2 with scope, required, type, unit and allowed range, loaded by the center of excellence analyst through RWB-P3-E1042-APP.
- Parameter `servicelevel.required-statuses`, whose list is Not specified in the source documents (GAP-0760; ASM-1382); the legacy assumed list is carried until it is confirmed.
- The holiday calendar is read through the rwb-source-data contract and is not a version of this service (DP-05).
- The 2 s timeout and the retry policy of the holiday read are service configuration values fixed by DP-11 and held outside code.

**Build steps**

1. `ProductParameterServiceClient` and `ParameterVersionResolver` over the parameters contract of rwb-case, with `MissingProductParameterException` and the version number returned beside the value; tests for AC1 and AC7.
2. `ReferenceDataClient` over the reference-data contract: version in force per business date, the row of a product group and the list values; tests for AC2 and AC8.
3. `ProductCompletenessCheck` and `OpenCaseCounter`, added as the table check of the three table codes in the reference-data service; tests for AC3, AC4, AC5 and AC6.
4. `DueDateCalculator` with the calendar and working-day rules and the holiday read through the rwb-source-data contract; test across the 2026-12-31 year end and a holiday row.
5. `CalculateDueDate` activity: the value in force, the unit, the projection write of `timer.started_at`, `expires_at` and `warn_at`, and the decision record with the table code and version number, in one transaction; tests for AC1, AC7 and AC8.
6. Move every product group name and period out of the case creation, allocation and stage-clock code so that each reads through the client; the catalog-versus-code build rule of RWB-P3-E1042-APP fails the build on a leftover literal.
7. `ProductParameterController` with the two read operations, the right and scope check, and the 401, 403, 404 and 503 answers; tests for AC1, AC2 and AC8 and the refusal of TC-E1-045-09.
8. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-source-data exists in the environment.

**Feature switch.** The legacy flag name `rwb.p3.product-parameters` is kept as the legacy reference. In the target the switch is a parameter read through the parameters contract: off, the engines use the values they read before this story and the CalculateDueDate activity falls back to the projection only; on, every value and every due date comes from the parameter and reference answers.

**Done when.** Every test in section 16 passes, `GET /cases/{caseId}/timers` returns the projection of a case with a notice timer and its expiry inside the 2 s budget, every decision record of a timer start names the table code and the version number in force, and a search of the rwb-case code finds no product group code literal outside test fixtures and the generated API types.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-034 | A product has no required parameter or service level row, at load or at run time | {product} has no {parameter} row. Add it before the load. |
| MSG-P3-027 | Duplicate row, or a product with open cases removed | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-002 | A value is outside its catalog range | {field} must be between {min} and {max}. |
| MSG-P4-002 | A role without Reference data C loads a file, or a role without the read right calls either operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | A call arrives with no valid session, or the person holds no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | The case is outside the person's scope, or its ID is unknown | This case is not in your scope. |

MSG-P3-027 and MSG-P3-034 are new (see Additions). MSG-P3-027 carries the message text of the Error and Message Standard v4 (table 3, row 84). Thai text follows DL10. For MSG-P3-027 the {check} value names the failed check only; for MSG-P3-034 the {parameter} value is the parameter code or the case status that has no row.

### 15. Screens and states

No screen in this story. A person sees the result on SCR-03 Case record, read only: the notice timer and its due date for each case, returned by `GET /cases/{caseId}/timers` and rendered by the case record view. States of SCR-03: Loading; list. Empty, error and no access are Not specified in the source documents (CG-ALL-3766). A case sent to the exception queue under X5 shows on SCR-09 Exception queue with MSG-P3-034. States of SCR-09: Loading; list. Empty, error and no access are Not specified in the source documents (CG-ALL-3767). Both screens are served by the gateway-bff composite route, which calls rwb-case for the case and its timers and rwb-source-data for the account and customer facts in parallel, one hop each, and merges the answers into the screen model (DP-19; RWB-PLT-N001-CON). The screen fields, the mask of customer fields and the route specification are owned by that platform contract; this story fixes only the content of the timers answer.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-045-01 | AC1, BR1, BR6 | End to end | One Mortgage and one HP case; NOTICE_PERIOD_DAYS 30 and 60 |
| TC-E1-045-02 | AC2, BR1, BR2 | End to end | New product group AUTO_LEASE with all required rows; one synthetic account |
| TC-E1-045-03 | AC3, BR3, BR4 | End to end | SERVICE_LEVEL load missing SSME and WAITING_PARTNER |
| TC-E1-045-04 | AC4, BR4 | End to end | NOTICE_PERIOD_DAYS 0 against range 1 to 365 |
| TC-E1-045-05 | AC5, BR4 | End to end | Two MORTGAGE rows for one parameter |
| TC-E1-045-06 | AC6, BR5 | End to end | Three open UNSECURED cases; PRODUCT load without UNSECURED |
| TC-E1-045-07 | AC7, BR8 | End to end | SSME case with no NOTICE_PERIOD_DAYS in force |
| TC-E1-045-08 | AC8, BR6, BR7 | End to end | Value changes from 30 to 45 on 2026-12-03 |
| TC-E1-045-09 | Access | Component | RW-PHONECOL (Reference data R only) loads PRODUCT_PARAMETER; refused with MSG-P4-002 |
| TC-E1-045-10 | Section 12 operations, events and activities | Component | Contract test of each operation, event and activity in section 12 |
| TC-E1-045-11 | Section 12.7 tables | Component | Boundary test of each table in section 12.7 |
| TC-E1-045-12 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC9) |
| TC-E1-045-13 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC10) |
| TC-E1-045-14 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC11) |
| TC-E1-045-15 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1045-APP-AC12) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR; no case of this story carries a Resilience level, so no NFR row is created and no `-ITG` copy exists for an APP story.

### 17. Guardrails

- No business value in code: no product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat a product group as a string checked against LOV-PRODUCT, not as a closed enum, and every value arrives through the parameters or reference-data contract (DP-06, DP-07).
- No personal data in logs, tests, workflow history, events or prompts: test cases use synthetic case numbers and synthetic account and customer keys, no customer name, address or identity number is read into a timer calculation, and the one published event carries IDs, codes and dates only.
- ACE data is read only through the owner's contract or the `v_ace_*` views of rwb-source-data: the holiday calendar comes through the rwb-source-data contract inside the CalculateDueDate activity, and rwb-case reads no ACE view at all (DP-05, DP-01).
- No read of another service's table: `rwb_case` holds no foreign key and no join into another schema, and the parameters and reference answers arrive only through their published client libraries.
- One evaluator: the product values feed the embedded Drools kit in the owning service, and no code reads a workbook, a DRL source or a rule row directly (DP-04).
- A running timer is never recalculated when a parameter changes, and its expiry keeps the value in force on the day it started (BR6).
- Every write of a timer projection goes with its decision record and its outbox row in one transaction, so a record never exists without the clock it explains (DP-03).
- The load is refused in full on any failed check, so no half-approved product version ever reaches an engine.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service hold every threshold, limit and name, versioned | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-25 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-045-01 to TC-E1-045-09 |
| REQ-CWC-011 | Service levels per queue and status held as data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-25 | 14 Set strategy, policy and decision rules | R-UNI-30; R-UNI-38 | TC-E1-045-01, TC-E1-045-03, TC-E1-045-08 |
| D-RCV-60 | Parameters and reference data move to the contracts of rwb-case, no product value stays in code, and the clock becomes a durable Temporal timer with the `timer` row kept as its projection | Decision log D-RCV-60; Template and Rules §R5.5 DP-06, DP-07, DP-05; Ownership Map ruling ASM-0078 | FEAT-CWC-25 | 14 Set strategy, policy and decision rules | DP-06; DP-07; DP-05; BR6; BR7 | TC-E1-045-01, TC-E1-045-02, TC-E1-045-07, TC-E1-045-08 |

### 19. Out of scope

- Letter and notice templates per product (P6 rwb-comms, DL28).
- Treatment bands, floors and ranges per product (FEAT-ADM-04, Epic 8).
- Delegation limits per product (RWB-E1-038, now the DoA table of rwb-access in RWB-P4-E1038-APP).
- The timer engine, the warnings and the escalations themselves (RWB-E1-028, now the timer story RWB-P3-E1028-APP).
- The parameter catalog and its own administration (RWB-E1-042, now RWB-P3-E1042-APP and RWB-PLT-E1042-APP).
- The reference-data service, its loads, approvals, rollback and version checks (RWB-E1-043, now RWB-P3-E1043-APP and RWB-PLT-E1043-APP).
- Product parameter screens (SCR-39 and SCR-42, Epic 8).
- The `rwb_case` schema baseline and the constraints and indexes that the parameter, reference and timer stories carry themselves.
