# RWB-P6-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P6-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-RDF-007, REQ-RDF-008, REQ-CWC-004) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-011 is split and reworked as the rwb-comms APP story RWB-P6-E1011-APP, the quality and reconciliation slice of the notices this service sent and of their dispatch and delivery; the enterprise case-list reconciliation stays with rwb-source-data and the data lake is removed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **a daily quality run in rwb-comms that reconciles the notices this service sent on a business date against the acknowledgments and the deliveries it holds, computes the variance and the variance percent against the tolerance parameter in force, writes one result per check for the date and lists every notice or row that breaks, and makes both the run record and the quality facts readable through this service's own operations**, so that **the data steward can say each morning whether the notices of the date were sent, acknowledged and delivered, and whether the proof-of-delivery measure of the Communications module is met**.

### 2. Business rationale

A notice that WIN never acknowledged, or that the proof-of-delivery batch never returned, is a notice whose date cannot be trusted in court, and today nobody sees the gap: the legacy capability reconciled the case list to ACE, treatments and payments, and every business key, and it wrote its report to a data lake. In `rwb-comms` the same idea is applied to the facts this service holds. Every business date the quality run compares the notices dispatched for the date with the notices that came back with a barcode and a sent date, and the notices it holds as delivered with the rows of the proof-of-delivery batch, computes the variance and the variance percent per check, compares the percent with the tolerance in force, writes one result per check for the date and lists every breaking notice or row. It serves the FSD P6 measure "notices with proof of delivery, 100 percent", meets REQ-RDF-007, REQ-RDF-008 and REQ-CWC-004, and applies control CTL-01.

Three edges of the legacy capability are no longer this service's to reach. The enterprise reconciliation of the case list to ACE, the treatments and payments checks, the REC-05 business-key resolution and the `reconciliation_result` rows are rwb-source-data's (Ownership Map: `reconciliation_result` is P1's; Architecture v5 slide 15 gives P1 the reconciliation, and slide 44 gives it JOB-04), and the end-to-end proof of JOB-04 across the wave-1 services is `RWB-ITG-E1011-ITG`. This story is the secondary rwb-comms slice of the same legacy key and owns a different set of facts: the notices, their barcodes, their sent dates and their delivery status.

The target removes what the legacy story relied on. The data lake is gone (DP-17, ADR-018), so the reconciliation extract and the data quality extract that the legacy publish step wrote through INT-19 have no target, and the measures come to rwb-reporting from the business events and the projections of the services; this story therefore writes no extract file and no lake path (GAP-1170; ASM-2117). No ACE view and no ACE table is read (DP-05, a prohibition here): the completeness answer and the proof-of-delivery rows arrive through the rwb-source-data contract, which is the single reader of `recovery.v_ace_*` (Architecture v5 slide 15). The tolerance and the list values are data: the parameter comes through the parameters contract of rwb-case with its version (DP-06), and the notice types, product groups and delivery statuses come through its reference-data contract (DP-07); neither contract is in this story's Contract dependencies, so both are faked from the published documents (GAP-1168; ASM-2115). The run is a Temporal workflow started by a Schedule in this service (DP-10), the tables live in `rwb_comms` (DP-01, DP-15), and the run record and the quality facts are reached through the gateway-bff composite route (DP-19).

The legacy key numbers the notice barcode break REC-09, while the dispatch story RWB-E1-055 numbers the same break REC-05, where the legacy RWB-E1-011 numbers the business-key orphan check REC-05. The collision is recorded and not resolved in this story (GAP-1169; ASM-2116).

### 3. Preconditions

- RWB-P6-E1055-APP is done: the notice row and its dispatch and proof-of-delivery fields live in `rwb_comms`, the WIN acknowledgment writes `sent_date`, `barcode` and `sent_type`, and the delivery matcher writes `callback_date` and `delivery_status`; the two are this story's source facts.
- RWB-P6-E1052-APP is done: notices exist in state Generated with a notice type and a template version, so a notice of the date can be reconciled.
- RWB-P6-E1055-CON is published: the `GET /notices/{noticeId}` shape with the dispatch and proof fields, the delivery-status list, the event envelopes and the fakes the run reads its own rows against. This story builds against it and its fakes; it is not in the Depends on (build) list, which the plan sets to None.
- The platform libraries are in place: the decision-record library (RWB-PLT-E1027-CON, DP-03), the parameters client (RWB-PLT-E1042-CON, DP-06), the reference-data client (RWB-PLT-E1043-CON, DP-07), the workflow kit with Schedules (RWB-PLT-E1071-CON, DP-10), the per-service Flyway sequence (RWB-PLT-E1044-CON, DP-15), the naming library (RWB-PLT-E1047-CON, DP-14) and the gateway-bff composite route (RWB-PLT-N001-CON, DP-19). None of them is in this story's Depends on (build) list, which the plan sets to None; they arrive through the platform release train of wave 0 and are assumed present before the wave-1 build (GAP-1167; ASM-2114).
- RWB-P3-E1042-CON is published for the parameter `recon.tolerance.pct` per check with its version; the contract story is not in this story's Contract dependencies, so the parameter read is faked from the published parameters document (GAP-1168; ASM-2115).
- RWB-P3-E1043-CON is published for LOV-NOTICE, LOV-PRODUCT and LOV-DELIVERY by version, so no list value is written in code; it is faked for the same reason (GAP-1168; ASM-2115).
- The rwb-source-data contract is published for the freshness answer of a data product and for the proof-of-delivery rows of a business date; it is not in this story's Contract dependencies, so it is faked, and the element names behind the two operations are not specified in the source documents (GAP-1168; ASM-2115; GAP-1097; ASM-2045).
- The parameter `recon.tolerance.pct` is 0.00 in force for REC-09 on the business date, the legacy value under DL25; its owner is the center of excellence analyst and a change needs the reference-data change process.
- The parameter key per check, the state names of the run, the check codes and the alert groups are configuration of this service and are read with their version; no value is compiled in.
- The proof-of-delivery batch of source WIN is COMPLETE for the business date in the SIT fixture, and the SIT stub of 12.8 holds synthetic rows only: no production data and no real WIN connection.
- The login is the rwb-comms login (DP-02); it holds no grant on any `recovery.v_ace_*` view, no grant on another service's schema and no other service's credential.

### 4. Flow

1. The Temporal Schedule of this service starts `NoticeQualityWorkflow` for the business date on task queue `rwb-comms` in namespace `rwb-recovery`, one run per business date; no event starts it (12.4).
2. The workflow asks the load-tolerance activity for the tolerance of each check of the run through the parameters contract of rwb-case, with the version in force (DP-06); the value is 0.00 in the fixture of the date.
3. The workflow asks the read-delivery-facts activity for the completeness answer of the proof-of-delivery data product for the business date through the rwb-source-data contract; a run that cannot obtain a COMPLETE answer writes no result and holds the date (AC4).
4. The same activity reads the proof-of-delivery rows of the business date through the rwb-source-data contract, one hop with a 2 s timeout (DP-11); no ACE view and no ACE table is read by this service (DP-05).
5. The workflow reads the notice rows of the business date from `rwb_comms`: the notices dispatched for the date by their `dispatch_file_id` and `sent_date`, the barcode and sent type returned by the acknowledgment, and the callback date and delivery status of the proof of delivery.
6. The reconciler computes, per check, the source count, the workbench count, the variance count and the variance percent: by the notice reconciliation it compares the notices dispatched for the date with the notices that hold a barcode and a sent date of the date, and with the proof-of-delivery rows of the date that match a notice by barcode and then by reference.
7. It compares each variance percent with the tolerance in force and sets the result of the check: PASS when the percent is equal to or below the tolerance, BREAK when it is above it (AC2, AC3).
8. It writes one row per check for the business date, the break rows of every notice or row that does not match in either direction, and the run row, in one transaction, replacing the rows of that date on a rerun; the unique key is the check code, the check name and the business date (AC5, AC6).
9. It sets the state of the run to RELEASED when every check is PASS and to HELD when any check is BREAK or not run, and it writes the not-run reason of a held run.
10. On a break it lists the breaking notices and rows for the data steward and, where the row is missing in ACE, for the ACE team, and it sends the break alert to the data steward, the platform administrator and the team managers with MSG-P1-012 (AC2).
11. It writes no event and no file: DP-09 is not in the pattern set of this story, and the data lake, the INT-19 adapter and the two extracts of the legacy publish step do not exist in the target (AC8; GAP-1170; GAP-1171).
12. `GET /quality-runs/{businessDate}` answers the run record and `GET /quality-results` answers the quality facts with their break rows from `rwb_comms` alone, so the data steward on SCR-45, rwb-source-data for the REC-09 answer and rwb-reporting for the report read the same rows (12.1); the notice person keys of a case are answered on `GET /cases/{caseId}/notices` for the REC-05 resolution that rwb-source-data runs in `RWB-ITG-E1011-ITG`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A check's variance is above the tolerance | Result BREAK; the run state HELD; the breaking notices and rows listed; the alert sent | MSG-P1-012 | AC2 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | The proof-of-delivery batch of the date is not COMPLETE | The run is HELD, writes no result for the date and shows every check as not run with the reason; the state of the previous date is unchanged | MSG-P1-001 | AC4 |
| X4 | The run repeats for the same date after a fix | The rows of that date are replaced and the run state is RELEASED if every check is PASS | None | AC5 |
| X5 | Two runs for the same date on two workers | One row per check and business date; no row written twice | None | AC6 |
| X6 | A proof-of-delivery row names an unknown barcode or reference, or a notice's barcode is on no row | The row or the notice is on the break list with its reason; no notice row changes | None | AC7 |
| X7 | The parameters contract or the rwb-source-data contract returns an error mid-run | No result is written for the date; the run state is FAILED with the system named; the rerun writes every row | MSG-GEN-006 | TC-E1-011-09 |
| X8 | A role without Platform administration R reads the run record or the break rows | 403, and nothing is written | MSG-P4-002 | TC-E1-011-07 |
| X9 | A caller reads a path outside `/api/recovery/comms/v1`, a cross-schema read appears, or an extract file or lake path is written | The build fails the boundary test and nothing is released | None | BR10 |
| X10 | The token carries no Workbench role | 401, and nothing is written | MSG-P4-001 | TC-E1-011-07 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the notice rows that RWB-P6-E1055-APP writes and builds against RWB-P6-E1055-CON and the fakes of 12.8; it changes no notice and reads no table of another service |
| Negotiable | The tolerance is a parameter with a version, the list values are reference data, and the check codes, the alert groups and the Schedule are configuration, not code |
| Valuable | The data steward sees each morning which notices of the date were not acknowledged or not delivered, before the proof-of-delivery measure is reported |
| Estimable | One workflow, one Schedule, two checks, three tables and three read operations |
| Small | Fits two weeks with its tests, as the secondary slice of the legacy key |
| Testable | Each criterion below is one automated test on synthetic rows and the four contract fakes, with no ACE view and no data lake |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality of the notices sent, in rwb-comms

  Background:
    Given the business date is 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-09
    Given the rwb-source-data contract mock returns the completeness answer COMPLETE for the proof-of-delivery batch of 2026-11-30

  Scenario: AC1 Variance zero (new, D-RCV-60)
    Given the rwb-comms notice rows of 2026-11-30 hold 25 notices dispatched for the date
    Given 25 of them carry a barcode and a sent date of 2026-11-30
    Given the rwb-source-data contract mock returns 25 proof-of-delivery rows of 2026-11-30, every one matched to one of the 25 notices
    When the quality run of 2026-11-30 runs
    Then the system writes two rows for 2026-11-30, REC-09 ACK and REC-09 POD, each with variance 0 and result PASS
    Then the run state of 2026-11-30 is RELEASED
    Then GET /quality-results answers both rows with their counts, the tolerance 0.00 and no break row

  Scenario: AC2 Variance over the tolerance (new, D-RCV-60)
    Given the rwb-comms notice rows of 2026-11-30 hold 25 notices dispatched for the date
    Given 24 of them carry a barcode and a sent date of 2026-11-30, a variance of 1 notice, 4.00 percent
    When the quality run of 2026-11-30 runs
    Then the REC-09 ACK result is BREAK with variance count 1 and variance percent 4.00
    Then the notice without the barcode is on the break list with its notice ID, its product group and its sent date
    Then the run state of 2026-11-30 is HELD
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 with the date, the product group, the variance 1 and the percent 4.00
    Then SCR-45 shows the REC-09 ACK break with the break row, and the REC-09 POD result is unchanged

  Scenario: AC3 Variance equal to the tolerance (new, D-RCV-60)
    Given the parameter recon.tolerance.pct for REC-09 is changed by a reference load to 0.10 from 2026-11-30
    Given the REC-09 ACK variance is 0.10 percent and the REC-09 POD variance is 0.11 percent
    When the quality run of 2026-11-30 runs
    Then the REC-09 ACK result is PASS and the REC-09 POD result is BREAK

  Scenario: AC4 Delivery batch not complete (new, D-RCV-60)
    Given the rwb-source-data contract mock returns no COMPLETE proof-of-delivery batch for 2026-11-30 and the stale marker naming "DP07 Legal" and 2026-11-23
    When the Schedule starts the quality run of 2026-11-30
    Then the run writes no quality result for 2026-11-30 and its state is HELD
    Then GET /quality-runs/2026-11-30 shows REC-09 ACK and REC-09 POD as not run with the reason "DP07 Legal is from 2026-11-23"
    Then the data steward, platform administrator and team manager groups receive MSG-P1-001 naming the product and the date

  Scenario: AC5 Rerun after the fact is fixed (new, D-RCV-60)
    Given the REC-09 ACK result for 2026-11-30 is BREAK and the run state is HELD
    Given the acknowledgment for the missing notice has since been applied and the notice carries barcode "RR123456789TH" and sent date 2026-11-30
    When the platform administrator restarts the quality run for 2026-11-30
    Then the run replaces the two rows for 2026-11-30 and both are PASS
    Then the run state of 2026-11-30 is RELEASED
    Then GET /quality-results answers the two rows of the rerun and no row of the earlier run

  Scenario: AC6 Two runs for the same date (new, D-RCV-60)
    Given two quality runs for 2026-11-30 start on two workers
    When both reach the reconciliation activity
    Then comms_quality_result holds one row per check and business date, two rows in all
    Then no row is written twice for the same rec_code, quality_check and business_date

  Scenario: AC7 An unknown barcode or reference (new, D-RCV-60)
    Given the rwb-source-data contract mock returns one proof-of-delivery row of 2026-11-30 with barcode "RR000000000TH" and reference "WIN-99999" that matches no notice
    Given one notice of 2026-11-30 carries barcode "RR123456789TH" and no row of the batch names it
    When the quality run of 2026-11-30 runs
    Then the unmatched row is on the break list with the reason that no notice holds its barcode or reference
    Then the unmatched notice is on the break list with its notice ID, its barcode and its product group
    Then no notice row changes and both checks remain BREAK for the date

  Scenario: AC8 No data-lake extract (new, D-RCV-60)
    Given the quality run of 2026-11-30 has finished with PASS on both checks
    When the run completes
    Then the two rows and their break rows are readable through GET /quality-runs/2026-11-30 and GET /quality-results
    Then no reconciliation extract and no data quality extract is written, no INT-19 adapter is called and no lake path exists for the date
```

Every criterion above is new under D-RCV-60; no legacy acceptance criterion of RWB-E1-011 is owned or restated here. The legacy criteria of the key are owned by `RWB-P1-E1011-APP` (AC5, AC6 and AC8) and by `RWB-ITG-E1011-ITG` (AC1, AC2, AC3, AC4 and AC7).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business date, rwb-comms reconciles the notices it dispatched for that date against the acknowledgments and the deliveries it holds, and the proof-of-delivery rows of the date, by count and by sum where the source carries an amount | REC-09; REQ-RDF-007; legacy RWB-E1-011 section 7 |
| BR2 | The variance count is the difference between the two sides of a check; the variance percent is that difference over the source side of the check, and both are written on the result row with the tolerance applied | TSD P1 v3 reconciliation_result (DF-OPS-122 to DF-OPS-129); legacy section 7 |
| BR3 | A result is BREAK when the variance percent is above the tolerance and PASS when it is equal to or below it; the boundary value is a PASS | Legacy RWB-E1-011 AC3 and BR6 |
| BR4 | The tolerance per check is the parameter `recon.tolerance.pct` read through the parameters contract of rwb-case with the version in force, never a value in code; 0.00 is the value of the date under DL25 | DP-06; legacy preconditions and BR6; DL25 |
| BR5 | No reconciliation runs until the owner of the delivery facts answers COMPLETE for the business date; a run that cannot obtain that answer writes no result and holds the date | Legacy BR9; VR-P1-011-1; MSG-P1-001 |
| BR6 | A repeated run for the same date replaces that date's rows, and a passing rerun releases the date | Legacy BR11 and AC5; R-UNI-40 |
| BR7 | Two runs for the same date produce one row per check and business date; the unique key is the rec code, the check name and the business date | Legacy AC6; R-UNI-40 |
| BR8 | A proof-of-delivery row with no notice for its barcode or reference, and a notice whose barcode is on no row of the batch, are breaks; neither side is changed and both are listed | Legacy RWB-E1-011 BR13 and RWB-E1-055 AC6; R-UNI-40 |
| BR9 | A break lists the notice ID, the barcode or reference, the product group and the reason, for the data steward and, where the row is missing in ACE, for the ACE team | Legacy BR7 and BR13; FEAT-RDF-12 |
| BR10 | The quality facts are this service's own rows: no data lake, no INT-19 adapter, no extract file and no outbound item is written for the date, and no table of another service is read | DP-17; ADR-018; Architecture v5 slides 37 and 44 (JOB-15); legacy BR "writes the extracts to the data lake" reversed |
| BR11 | Report grades of the run: PASS, BREAK, and not run with its reason | Legacy BR10; FEAT-RDF-12 |
| BR12 | The run uses one business date, the date of the batch it was started by, and never a mix of two business dates | Legacy BR12; BR-P1-011-2 |
| BR13 | A role without the right of the capability area is refused with MSG-P4-002 and nothing is written | FSD P1 A2.11.4.3 AC-EXC-P1-011-03; legacy section 5 X8 |
| BR14 | The person keys of a case's notices are answered by this service for the REC-05 resolution that rwb-source-data runs; the resolution itself and every orphan decision are the enterprise reconciliation's and stay with rwb-source-data | Legacy RWB-E1-011 BR5; Architecture v5 slide 17 (rwb-comms IN: GET /cases/{id}/notices); RWB-ITG-E1011-ITG |

The notice barcode break is numbered REC-09 here, as the legacy RWB-E1-011 numbers it in section 19 and as RWB-E1-055 numbers the same break REC-05; the collision with the REC-05 business-key orphan check of RWB-E1-011 is recorded and not decided in this story (GAP-1169; ASM-2116).

### 9. State transitions

None for a case status. This story changes no notice and no case; it writes the state of its own run row and the result rows of the business date.

| From | Event | Condition | To |
|---|---|---|---|
| Not run | The Schedule starts the run | The completeness answer of the delivery source is COMPLETE for the business date | Running |
| Not run | The Schedule starts the run | The answer is not COMPLETE, or cannot be read | Held, with the not-run reason on the run row |
| Running | Both checks are computed | Every check is PASS | Released |
| Running | Both checks are computed | At least one check is BREAK | Held |
| Running | A source read fails | The parameters or the delivery facts cannot be read | Failed, with the system named and no result row for the date |
| Held | A rerun for the same date | The rows of the date are replaced and every check is PASS | Released |
| Released | A rerun for the same date | A check is BREAK | Held |

The result value of a check is the legacy value set of `reconciliation_result.result`, LOV-REC-RESULT: PASS and BREAK, plus the not-run grade and its reason that legacy BR10 defines and that this story writes on the run row only, never as a third result value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity | Runs the workflow, reads the parameters, the reference data and the delivery facts through their owners' operations, and writes the run row, the result rows and the break rows of `rwb_comms`; it holds no grant on another schema and no grant on `recovery.v_ace_*` |
| RW-DATASTEW, data steward and data product owner | Platform administration R: reads the run record, the results and the break rows, and signs the daily quality result of the notices |
| RW-PLATADM, platform administrator | Platform administration R and U: reads the results and restarts the run for a business date |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read the results and the break rows in the Platform administration area, right R |
| RW-TEAMMGR, RW-BIANAL and other report readers | Reporting R on the report of the date; RW-BIANAL builds it with Reporting CRUD, outside this story |
| rwb-source-data service identity | Reads `GET /cases/{caseId}/notices` for the REC-05 resolution of its reconciliation run; no write and no other operation |
| ACE team | Reads the break rows of a notice whose row is missing in ACE, through the data steward's listing |

The right of the two quality reads is declared in the Platform administration capability area, right R, as the legacy story declares it for its job listing. TSD P6 T6.1 has no Platform administration column, so the module matrix neither grants nor refuses it; the legacy story comes first in the fill order and the right is kept (GAP-1173; ASM-2120). DP-08 is not in the patterns applied to this story: the declared area and right are enforced at gateway-bff for the screen path, and where a local guard is required on the operation itself the guard and its story are not named in the sources.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read, for the case notice answer only |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read, the acknowledgment side of the check |
| DF-LEG-020 | notice | barcode | Read, the key the two sides are matched on |
| DF-LEG-021 | notice | callback_date | Read, the delivery side of the check |
| DF-LEG-022 | notice | delivery_status | Read, the delivery side of the check |
| DF-LEG-023 | notice | sent_type | Read, as the reason of a break row |
| DF-LEG-033 | notice | dispatch_file_id | Read, to select the notices dispatched for the date |
| DF-LEG-030 | notice | person key of the notice party | Read, for the case notice answer; the module specification names the same ID party_id and the legacy story names person_key, already recorded as GAP-1084 |
| Standard column | notice | state | Read |
| DF-REF-049 | template | product_group | Read, the product group a break row carries |
| DF-ACE-253 to DF-ACE-258 | pod record (P1) | notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type | Read, through the rwb-source-data contract only (GAP-1097; ASM-2045) |
| No BR Field ID | comms_quality_run, comms_quality_result, comms_quality_break | the run state, the check, the counts, the variance, the tolerance and the break reason | Write; the service's own tables, whose columns carry no field ID in the sources (GAP-1172; ASM-2119) |

**Indexes and migration.** The three tables arrive in the service's per-service Flyway sequence (DP-15), as `V1011_1__comms_quality.sql` by the convention of the service, after the `notice` table of RWB-P6-E1052-APP and the dispatch columns of RWB-P6-E1055-APP: `comms_quality_run` with a unique business date, `comms_quality_result` with a unique (rec_code, quality_check, business_date), and `comms_quality_break` with an index on (business_date, rec_code) and on the notice ID.

**The proof-of-delivery link.** The pod record is rwb-source-data's data product and is read through its contract only; the barcode is the match key and is stored on the notice row by RWB-P6-E1055-APP. Nothing in this story is a foreign key across schemas (DP-01).

**No personal data.** The run row, the result rows and the break rows carry a notice ID, a case ID, a barcode, a reference, a product group, dates, counts and a percent. The addressee, the address, the contact value and the identity number never enter these tables, are never logged and are not part of any break row.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/quality-runs/{businessDate}` | The run record of the business date: the state RELEASED, HELD or FAILED, each check with PASS, BREAK or not run and its reason, the variance count and percent, the tolerance in force, the count of break rows and the times of the run | Platform administration R, scope applied | Not applicable |
| GET | `/quality-results` | The quality facts of a business date with their break rows: rec code, check, source and workbench counts, variance count, variance percent, tolerance percent, result, and per break row the notice ID, the barcode or reference, the product group and the reason | Platform administration R, scope applied; Reporting R for the report reader | Not applicable |
| GET | `/cases/{caseId}/notices` | The notices of a case with their notice type, sent date, barcode, callback date, delivery status, state and person key, for the REC-05 resolution that rwb-source-data runs (RWB-ITG-E1011-ITG) | Litigation R, scope applied; the rwb-source-data service identity for the reconciliation run | Not applicable |

All three are reads: they declare no Idempotency-Key, answer 401, 403, 404 and 503 with the platform error envelope, and answer from `rwb_comms` only. The two quality operations and their paths are this story's design, because no source names a quality run record, a result read or a break list for rwb-comms (GAP-1172; ASM-2119); the case notice operation is the one Architecture v5 slide 17 gives rwb-comms (`GET /cases/{id}/notices`) and the one `RWB-ITG-E1011-ITG` asserts.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The completeness answer of the proof-of-delivery data product for the business date, and its stale marker, before any check runs (AC4); faked (GAP-1168; ASM-2115) |
| GET | `/api/recovery/source-data/v1/data-products/DP07/records` | P1 rwb-source-data | The proof-of-delivery rows of the business date, for the delivery side of REC-09 POD; faked, and the element names are not in the source documents (GAP-1097; ASM-2045) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameter `recon.tolerance.pct` per check with the version in force (DP-06, AC3); faked (GAP-1168; ASM-2115) |
| The reference-data read of the rwb-case contract (RWB-P3-E1043-CON) | P3 rwb-case | LOV-NOTICE, LOV-PRODUCT and LOV-DELIVERY by version, so no list value is in code (DP-07); faked, and the path is not named in the source documents (GAP-1168; ASM-2115) |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The quality facts are handed over through the two reads of 12.1: rwb-source-data reads them for the REC-09 answer of its run and rwb-reporting reads them for the report of the date. No operation of rwb-reporting or rwb-source-data accepts a push: the reporting operations of P9 are `GET /dashboards/{id}`, `GET /reports/{id}` and `POST /reports/{id}/run` (Architecture v5 slide 15), and the reconciliation read of P1 is API-P1-003, a read. The hand-off is therefore this service's read model, and no target operation for a push is named in the sources (GAP-1171; ASM-2118).

#### 12.3 Events published

None. DP-09 is not in the pattern set of this story, so no event is written to the outbox and no Kafka record is published by this run; the topic `rwb.comms.events.v1` carries the dispatch and delivery facts of RWB-P6-E1055-APP and none of this story, and the quality facts are served by the reads of 12.1 (GAP-1171; ASM-2118).

#### 12.4 Events consumed

None. The run is started by the Schedule of 12.6 and reads no event; the delivery facts are read synchronously through the rwb-source-data contract, and a redelivered event cannot start a second run.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `NoticeQualityWorkflow` | Workflow from the kit template; one per business date | `rwb-comms` in namespace `rwb-recovery` | Owns the run: the parameter read, the completeness gate, the two checks, the rows of the date and the run state |
| `loadTolerance` | Activity, calls rwb-case (P3) | `rwb-comms` | Reads `recon.tolerance.pct` per check with its version before any check runs |
| `readDeliveryFacts` | Activity, calls rwb-source-data (P1) | `rwb-comms` | Reads the completeness answer and the proof-of-delivery rows of the business date; writes nothing when the answer is not COMPLETE |
| `reconcileNotices` | Activity, reads `rwb_comms` only | `rwb-comms` | Computes the two checks, their variance and percent, and the break rows of the date |
| `writeQualityFacts` | Activity, writes `rwb_comms` only | `rwb-comms` | Writes the run row, the result rows and the break rows in one transaction and replaces the rows of the date |

The workflow is idempotent by business date and check: a retried run does not write a second row for the same key and does not restart a released date without a rerun request.

#### 12.6 Schedules

One Schedule, owned by this service.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The quality Schedule of rwb-comms (RWB-PLT-E1071-CON) | Not specified in the source documents (GAP-1172; ASM-2119) | SKIP | Catch-up window of the workflow kit | `NoticeQualityWorkflow` for the business date, after the proof-of-delivery read of the date |

No Quartz row, no shared job table entry and no Control-M job is registered for this run; JOB-04 stays rwb-source-data's event-triggered workflow (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notices, their dispatch fields and their proof-of-delivery fields; read only in this story |
| template | P6 (rwb_comms) | The product group of the template version, read only |
| merge_field | P6 (rwb_comms) | The merge codes of the template catalog, read only |
| comms_quality_run | P6 (rwb_comms) | The run of one business date: state, not-run reason, times and break count |
| comms_quality_result | P6 (rwb_comms) | One row per check and business date: counts, amounts, variance, percent, tolerance and result |
| comms_quality_break | P6 (rwb_comms) | One row per breaking notice or row of a check, with the reason |

The three quality tables are this story's design and carry no field ID in the sources (GAP-1172; ASM-2119). Not owned and never read as a table: `reconciliation_result` and `case_list_row` (P1), `case_entry_exclusion`, `recovery_case` and `timer` (P3), `document` and `signature_request` (P5), `interaction` (P1), `outbound_item` (P2).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data freshness fake | COMPLETE for 2026-11-30 with the load time; not COMPLETE with the stale marker naming "DP07 Legal" and 2026-11-23; an error after the first read | AC1, AC2, AC3, AC4, AC7 |
| rwb-source-data pod records fake | 25 rows of 2026-11-30 matched to the 25 notices; 24 matched rows and no row for one notice; one row with barcode `RR000000000TH` and reference `WIN-99999` matching no notice | AC1, AC2, AC7 |
| rwb-case parameters fake | `recon.tolerance.pct` 0.00 for REC-09, and the 0.10 version in force from 2026-11-30 of AC3 | AC1, AC2, AC3 |
| rwb-case reference-data fake | LOV-NOTICE, LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE and SSME, and LOV-DELIVERY with DELIVERED and PENDING, by version | AC1, AC2, AC7 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the published document is a build failure. The fixture values are the synthetic notice fixtures of the dispatch and delivery loop of RWB-P6-E1055-APP, and no production value is used.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The run record, the quality facts and the case notices; the freshness answer, the pod records, the parameter read and the reference read; one hop and 2 s each |
| Kafka | 0 published, 0 consumed | DP-09 is not in the pattern set of this story and the run is Schedule-started |
| Temporal | 1 workflow, 4 activities | `NoticeQualityWorkflow` on `rwb-comms` with `loadTolerance`, `readDeliveryFacts`, `reconcileNotices` and `writeQualityFacts` |
| File | 0 | No extract file and no outbound item: the data lake and the INT-19 adapter are removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `quality`, Java package `th.co.scb.ace.workbench.recovery.comms.quality`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Seven of these patterns add a platform CON in the DP table (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) and two add a contract of rwb-case (RWB-P3-E1042-CON and RWB-P3-E1043-CON), while the plan sets this story's Depends on (build) and Contract dependencies to None. Both lists stay None as the plan sets them: the platform CONs land through the platform release train of wave 0, before the wave-1 build, and they are not a lane dependency of an APP story (GAP-1167; ASM-2114); the two rwb-case contracts and the rwb-source-data contract are built against their published documents and their fakes and never block the build (GAP-1168; ASM-2115). DP-05 applies only as a prohibition: this service reads no ACE view and no ACE table, and the completeness answer and the pod rows arrive through the rwb-source-data contract; the freshness check over `recovery.v_ace_*` is rwb-source-data's own check and is consumed here as its answer, never as a view. DP-17 is applied as the removal of the lake target: the two extracts of the legacy publish step are dropped and the measure is served from this service's read model (GAP-1170; ASM-2117). DP-14 applies to the naming only: this story publishes no event, and the topic constant comes from the naming library for the events RWB-P6-E1055-APP publishes. DP-03 is applied where a rule decides the handling of a break; the record is written first through the library and a failed write stops the run.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| QualityRunController | Controller | `GET /quality-runs/{businessDate}` and `GET /quality-results`, with the problem mapping for 401, 403, 404 and 503 |
| CaseNoticeController | Controller | `GET /cases/{caseId}/notices` for the REC-05 resolution of rwb-source-data |
| NoticeQualityWorkflow | Workflow | The run of section 4: parameter read, completeness gate, the two checks, the rows and the state |
| ToleranceReader | Service | Reads `recon.tolerance.pct` per check with its version through the parameters contract |
| DeliveryFactReader | Service | Reads the completeness answer and the proof-of-delivery rows of the date through the rwb-source-data contract, and returns nothing when the answer is not COMPLETE |
| NoticeReconciler | Service | Computes the source and workbench counts, the variance, the variance percent and the result of the ACK and POD checks |
| QualityFactWriter | Service | Writes the run, the results and the break rows in one transaction, replacing the rows of the date |
| QualityBreakNotifier | Service | Sends the MSG-P1-012 wording and the MSG-P1-001 wording to the configured groups |
| QualityReadModel | Service | Answers the three reads of 12.1 from `rwb_comms` only |

**Database and migrations.** `V1011_1__comms_quality.sql` creates `comms_quality_run`, `comms_quality_result` and `comms_quality_break` with the unique keys and indexes of section 11, after the notice baseline of RWB-P6-E1052-APP and the dispatch columns of RWB-P6-E1055-APP. No column is added to `notice`, and no column carries another service's data (DP-01, DP-15).

**Configuration and reference data.** The parameter key of each check, the check codes `REC-09` with the check names `ACK` and `POD`, the state names, the alert recipient groups and the Schedule cron are configuration and reference data read with a version, owned by the platform administrator; the tolerance value is the parameter of 12.2 and is never compiled in. The notice types, the product groups and the delivery statuses are reference data through DP-07.

**Build steps**

1. Write the migration and test the three unique keys and the two query indexes.
2. Build `ToleranceReader` and `DeliveryFactReader` over the two fakes, with the completeness gate and the stale marker; test AC4.
3. Build `NoticeReconciler` for the ACK and POD checks; unit test variance 0, the tolerance boundary and a break; tests for AC1, AC2 and AC3.
4. Build `QualityFactWriter` with the replace of one date and the unique key; tests for AC5 and AC6.
5. Build the break listing in both directions, the unknown barcode and reference, and the no-change rule; test AC7.
6. Build `QualityReadModel` and the three controllers over the read model; test the access refusal and the no-extract assertion of AC8.
7. Build `NoticeQualityWorkflow` with the Schedule hook and the retry rule by business date and check.
8. Add the run to the job monitor surface of SCR-44 and to the break list of SCR-45 through the gateway-bff route, and prove that no file, no outbound item and no lake path is written.

**Feature flag.** `rwb.comms.quality-run-v1`, read as a flag of the platform library; off means the Schedule starts no run, the read model answers nothing for the date and no result row is written.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E1055-CON stay green, and a SIT week shows one run per business date, two result rows per date, a HELD date on a break and a RELEASED date after the rerun, no notice changed by the run, and no extract file, outbound item or lake path for any date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A check breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The proof-of-delivery batch is not complete; the run is held | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A contract or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Platform administration right reads the run or the breaks | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | The token carries no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |

The five texts are copied unchanged from the legacy story and the platform message catalog, and the placeholders are the values the tests of section 7 assert: the business date, the product group, the variance 1 and the percent 4.00 for MSG-P1-012, and "DP07 Legal is from 2026-11-23" for MSG-P1-001. The legacy wording of MSG-P1-012 speaks of the case list, which is rwb-source-data's check; the text is kept because the legacy message set is kept, and the product group and the count of the notice check fill the same placeholders.

### 15. Screens and states

No screen is built in this story. Existing surfaces show what it writes, through the gateway-bff composite route (DP-19):

| Surface | What it shows |
|---|---|
| SCR-44 Interface and job monitor | The quality run of the business date in the states Running, failed and complete, with the state RELEASED or HELD, the two checks, the variance and the break count |
| SCR-45 Data quality | The results of the date with PASS, BREAK or not run and the reason, the break rows of each check, and the quality facts that rwb-source-data and rwb-reporting read for the report |
| The report "Reconciliation and data quality" (rwb-reporting) | Read-only for RW-BIANAL and the report readers: the notice quality result of the date beside the enterprise reconciliation result that rwb-source-data publishes |

The route merges the answers of this service with the case and the report; the screen field lists and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | Access; the run record and the quality facts of 12.1 | Component | RW-CASEOWN calls `GET /quality-runs/2026-11-30`; refused with MSG-P4-002; no token is refused with MSG-P4-001 |
| TC-E1-011-01 | AC1, AC8, BR1, BR2, BR10, BR11 | End to end | 25 notices of 2026-11-30, 25 acknowledged and 25 matched pod rows; no extract file and no lake path |
| TC-E1-011-02 | AC2, BR3, BR9, BR11 | End to end | 25 notices, 24 acknowledged, a variance of 1 notice, 4.00 percent |
| TC-E1-011-03 | AC3, BR3, BR4 | End to end | Tolerance 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04 | AC4, BR5, BR11 | End to end | No COMPLETE proof-of-delivery batch for 2026-11-30; stale marker "DP07 Legal is from 2026-11-23" |
| TC-E1-011-05 | AC5, BR6, BR7 | End to end | Break of 1 notice, the acknowledgment applied, restart |
| TC-E1-011-06 | AC6, BR7 | End to end | Two runs for 2026-11-30 on two workers |
| TC-E1-011-08 | AC7, BR8, BR9 | End to end | Pod row with barcode RR000000000TH and reference WIN-99999; notice with barcode RR123456789TH on no row |
| TC-E1-011-09 | AC4, BR5, BR12 | NFR | The rwb-source-data contract forced to fail after the first read; MSG-GEN-006 naming the system; the rerun writes both rows |

The nine legacy test cases of the key are kept with their legacy IDs and their legacy data and are run on the fixtures of this slice. TC-E1-011-07 has no acceptance criterion of its own: the legacy Access case is carried as the access row of this story, exactly as the legacy table carries it. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the tolerance, the check codes, the state names, the alert groups and the cron are configuration or parameters read with a version; the notice types, the product groups and the delivery statuses are reference data.
- No personal data in logs, tables, tests or prompts: the run, the results and the break rows carry a notice ID, a case ID, a barcode, a reference, a product group, dates, counts and a percent only; no addressee, address, contact value or identity number is read or written.
- ACE data only through the owner's contract: the completeness answer and the proof-of-delivery rows arrive through the rwb-source-data contract, and this service holds no grant on any `recovery.v_ace_*` view and opens no ACE table (DP-05).
- No read of another service's tables and no cross-schema join: `reconciliation_result` stays rwb-source-data's and is not read here, the exclusions and the case are rwb-case's, and the report is rwb-reporting's (DP-01).
- No data lake and no extract: no INT-19 adapter, no outbound item and no extract file is written or read for any date, and the boundary test fails the build if a lake path appears (DP-17).
- The run is Schedule-started only: no event starts it and no Kafka record is published by it, because DP-09 is not in this story's pattern set.
- Every consumed call is one hop with a 2 s budget, one GET retry with jitter and a breaker per downstream; no call chain.
- A break never changes a notice, a case or an ACE row; the rerun through the workflow is the only path that replaces the rows of a date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | The case list reconciles daily to the count of accounts in v_ace_account with no variance, and every business key on a Workbench table resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13 | All recovery processes | REC-09; CTL-01; R-UNI-40 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-08 |
| REQ-RDF-008 | Data quality checks run in ACE ingestion; the Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-09; CTL-01 | TC-E1-011-02, TC-E1-011-03, TC-E1-011-04, TC-E1-011-05 |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 Take over the case at 90 days past due | None in this slice | None in this slice; the exclusions are RWB-P1-E1011-APP's and RWB-P3-E1011-APP's |

REC-01 and REC-02 are not in the rules column of this story: they compare the case list with `v_ace_account` and are the enterprise reconciliation's, owned by `RWB-P1-E1011-APP` and proved end to end by `RWB-ITG-E1011-ITG`. CTL-01 is the control the legacy key applies and REC-09 is the notice barcode break this slice owns.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-011 | The quality and reconciliation slice of the notices and their dispatch and delivery; no legacy AC owned here, since AC1 to AC8 belong to RWB-P1-E1011-APP and RWB-ITG-E1011-ITG |
| The enterprise case-list reconciliation | rwb-source-data's JOB-04 workflow, its `reconciliation_result` rows, REC-01, REC-02, REC-03, REC-04 and the REC-05 business-key resolution (RWB-P1-E1011-APP) |
| RWB-ITG-E1011-ITG | The end-to-end proof of JOB-04 across the wave-1 services, which reads `GET /cases/{caseId}/notices` of this service for the notice person keys |
| The P1 reconciliation_result table | Owned by P1 and never written or read as a table here |
| The P9 reporting model | Reads the quality facts of 12.1 and the business events of the date; no event of this story feeds it |
| The lake removal | The two legacy extracts and the INT-19 adapter are dropped (DP-17, ADR-018) |
| The job monitor | SCR-44 shows the run of the date with its state and its two checks |
| DP-01 | The notice and the three quality tables live in `rwb_comms`; no table of another service is read |
| DP-02 | The rwb-comms login runs the workflow and reads the two contracts |
| DP-03 | The decision record is written through the library where a rule decides the handling of a break |
| DP-05 | The completeness answer and the pod rows arrive through the rwb-source-data contract; no ACE view is read |
| DP-06 | The tolerance is a parameter with a version, read through the rwb-case contract |
| DP-07 | The notice types, product groups and delivery statuses are reference data with a version |
| DP-10 | The run is a Temporal Schedule plus a workflow, not a Quartz row |
| DP-11 | Four consumed operations, one hop and 2 s each |
| DP-14 | The topic name comes from the naming library; this story publishes no event |
| DP-15 | The three tables arrive in the per-service Flyway sequence |
| DP-17 | The data lake and the two extracts are removed, and the measure is served from the read model |
| DP-19 | SCR-44, SCR-45 and the report are reached through the gateway-bff composite route |
| ADR-013 | 19 services inside ACE: the notice quality run lives in rwb-comms |
| ADR-014 | Schema and login per service: `rwb_comms` and the rwb-comms login |
| ADR-018 | No data lake; the reporting read model is fed from the services |
| ADR-020 | Contract-first REST, one hop and 2 s on every consumed row |
| ADR-021 | Per-service Flyway and migration ownership of the three tables |

### 19. Out of scope

- The enterprise reconciliation of the case list to ACE, its REC-01 to REC-05 checks, its `reconciliation_result` rows, the publish gate of the case list and the REC-05 business-key resolution: `RWB-P1-E1011-APP`, `RWB-P1-E1011-CON` and `RWB-P1-E1011-OPS`.
- The end-to-end proof of JOB-04 across the wave-1 services, including the read of `GET /cases/{caseId}/notices`: `RWB-ITG-E1011-ITG`.
- The exclusion rules and the exclusion resource of rwb-case: `RWB-P3-E1011-APP`.
- The asset keys of rwb-asset for the REC-05 resolution: `RWB-S5-E1011-APP`.
- The generation of notices, the template and merge-field catalog, the dispatch loop and the proof-of-delivery capture: RWB-P6-E1052-APP, RWB-P6-E1046-APP and RWB-P6-E1055-APP.
- The other legacy reconciliations REC-06 (write-offs), REC-07 (assets taken on) and REC-08 (the decision log copy): not in this slice. The notice barcode check REC-09 is owned here, and the REC-05 label that RWB-E1-055 gives the same break is recorded as a collision (GAP-1169; ASM-2116).
- The data quality console SCR-45 and the quality measure definitions of the reporting module (Epic 2 and Epic 8); this story only writes the rows those surfaces read.
- The reporting model of rwb-reporting: its measure definitions, its snapshots, its steering dashboard and its 07:30 refresh, and the question of whether it reads the quality facts of this service or receives a quality event in wave 2 (GAP-1171; ASM-2118).
- Any data lake, lake copy, INT-19 adapter or INT-20 extract: removed from the target under DP-17, so none is built, migrated, provisioned or tested here.
- The platform job monitor and its alerting beyond the read-only SCR-44 answer of this run, and the deployment, the Schedule registration, the dashboards, the alerts and the runbook of this run: the platform observability epic and the OPS slice of this legacy key.
- Working a break to closure with an owner and a date: FEAT-RPT-09 full scope, Epic 2.
- The report of the date itself and the reading of it by the report users: rwb-reporting and RWB-ITG-E1011-ITG.
