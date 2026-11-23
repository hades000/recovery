<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD P2 Integration v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD P2 Integration v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P2 Integration

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P2 Integration |
| Document ID | P2-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| FSD owner | Business analyst, P2 |
| Business owner | Business lead |
| Decision | D-RCV-35 (U1 to U5); ADR-010; open point DL43 |

| Module code | Module name | First in |
|---|---|---|
| P2 | Integration | E1 |

**Feature scope.** Outbound adapters only: outbound files, outbound retry and exception queue, duplicate-event handling, and use of the ACE outbound paths. P2 loads no source data.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P2 Integration | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |
| Recovery Workbench ACE DB Alignment Change Register v1 | Decision record | D-RCV-35, ADR-010, Appendix A removed stories |
| Recovery Workbench ACE Data Tier Map v1 | Frozen input | The views an outbound file reads |
| Recovery Workbench Interface Specifications v3 | Design | INT-14, INT-19, INT-20, INT-25 outbound; inbound INT-01 to INT-16 owned by the ACE team |
| Recovery Workbench Batch and Scheduling Design v3 | Design | JOB-10, JOB-11, JOB-13, JOB-15; JOB-01 and JOB-09 retired |
| Recovery Workbench Event and Messaging Design v3 | Design | EV-26 AceDataReady, EV-27 AceDataLate, R-UNI-40 duplicates |

### Change note, version 3

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Baseline: one adapter pattern for file loads and outbound files |
| 3 | 15 November 2026 | Re-based under D-RCV-35 (U1) and ADR-010. P2 becomes outbound only. The inbound file-load functions are removed and parked with their IDs kept: FEAT-DRI-09 (A2.4) in full; the inbound half of FEAT-RDF-21 (A2.1) and FEAT-DRI-10 (A2.5); FileLoadAdapter; the file checks DQ-057 and DQ-059; the missing-file check of JOB-09. Each is marked "Removed by D-RCV-35 - later home: ACE ingestion". ACE ingests every inbound source and the Workbench reads it through the `recovery.v_ace_*` views. `interface_config` holds outbound interfaces only; `interface_run` and `interface_signoff` leave the schema and outbound runs are recorded in `outbound_item` and `outbox_delivery`. New section A1.5 (outbound interface register) and A1.6 (removed functions). New ACs AC-ALT-P2-00n-03 and AC-EXC-P2-007-07. Requirements REQ-DRI-006, 008 and 013 restated as amended by D-RCV-35. Stale-data message MSG-P1-001 reworded. |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only; NSS (INT-17) and LINE OA (INT-18) |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |
| Inbound source data | REUSE | ACE ingestion (D-RCV-35, ADR-010; RWB-ACE-001) | Read through `recovery.v_ace_*` views. No Workbench file load, SFTP pickup, data quality gate, run record or sign-off |
| PII Kafka, audit and SOC logs | REUSE | ACE logging (INT-22) | No Workbench adapter |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** The outbound adapters: the WIN registered-mail notice file (INT-14, JOB-10), the reporting extract to the data lake and Power BI (INT-19, JOB-15), the decision and outcome feed to COLLINS through the data lake (INT-20, JOB-13), and the debt buyer data tape (INT-25). One outbound pattern: build from Workbench tables and the `recovery.v_ace_*` views, send through the outbox (JOB-11), acknowledge, retry, exception queue. Duplicate detection for every consumed event, including EV-26 AceDataReady. Use of the ACE outbound paths for NSS, LINE OA and the PII, audit and SOC logs.

**Out of scope.** Every inbound source load: ALS, SCBPDM, EFS, COLLINS scores, LIT, CCMS, SVAF, AMIS, RPS, WIN proof of delivery, GL write-off postings, NLEADS, EasyApp and Entra ID land in ACE through ACE's ingestion (RWB-ACE-001) and are read through the views; the batch-complete record and the late-batch alert are P1 (EV-26, EV-27). GL write-off posting is not a Workbench file: the approved write-off raises EV-24 WriteOffApproved, the posting is made in GL, and the posted result is read back through `v_ace_write_off` (INT-16, into ACE). Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-RDF-21; FEAT-RDF-23; RWB-E1-069 (ACE source views, for the data an outbound file reads)

**Constraints.** Built in the ACE service as part of the recovery module; source data is read from the ACE database through the read-only `recovery.v_ace_*` views and is never loaded, copied or written (D-RCV-35, ADR-010); P2 has no inbound adapter; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section | Status v3 |
|---|---|---|---|---|---|---|---|
| P2 | FEAT-RDF-21 | Run the integration adapters for outbound files | System | Provides the one pattern every outbound file uses, with checks, retry and an exception queue. v2 name: "for file loads and outbound files"; the file-load half is removed by D-RCV-35. | E1 | A2.1 | Rescoped |
| P2 | FEAT-RDF-23 | Queue and retry a failed interface call | System | Holds an outbound call when the target system is unavailable and retries it on the interface schedule. | E1 | A2.2 | Kept |
| P2 | FEAT-RDF-24 | Raise an interface failure to the exception queue | System | Moves a call that has used its retries to the exception queue and raises a task for the platform team. | E1 | A2.3 | Kept |
| P2 | FEAT-DRI-09 | Run the file adapters for sources outside COLLINS | System | Removed by D-RCV-35 - later home: ACE ingestion. ACE ingests CCMS, SVAF, AMIS, RPS, WIN and GL. | E1 | A2.4 | Removed |
| P2 | FEAT-DRI-10 | Run outbound file and SFTP adapters | System | Moves bulk data out by file where the target has no API. v2 name: "Run file and SFTP adapters"; the inbound pickup is removed by D-RCV-35. | E1 | A2.5 | Rescoped |
| P2 | FEAT-DRI-11 | Route every outbound file through the integration adapters | System | Puts every outbound file through one adapter, so retries, logging and throttling are in one place. | E1 | A2.6 | Kept |
| P2 | FEAT-DRI-13 | Detect and ignore a duplicate event | System | Recognizes an event that has already been processed by its key, and records the repeat without acting twice. | E1 | A2.7 | Kept |

### A1.3 Background

Each system is reached by hand or by a one-off file; failures are found late. Under D-RCV-35 the Workbench no longer receives files: ACE ingests the sources, and the Workbench only sends.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale. Freshness comes from the ACE batch record, `v_ace_batch_status`.

### A1.5 Outbound interface register

| Interface | Target | Built from | Adapter | Trigger | Retry and exception |
|---|---|---|---|---|---|
| INT-14 | WIN, registered mail | `notice`, `document`; addressee and address from `v_ace_contact` by `notice.person_key` and `contact_key` | OutboundFileAdapter over SFTP | JOB-10, daily 16:00 | Hold the case step until acknowledged; 3 attempts, then the exception queue (R-UNI-33, R-UNI-34) |
| INT-19 | Data lake and Power BI | Case, queue, task, timer, decision log and outcome records changed that day | OutboundFileAdapter | JOB-15, nightly 01:30 | Hold the publish and alert; run again in the next window |
| INT-20 | COLLINS, through the data lake | Decision log entries and outcomes changed that day | OutboundFileAdapter | JOB-13, nightly 01:00 | Hold the publish and alert; run again in the next window |
| INT-25 | Debt buyers | `debt_sale_account` by `account_key`; account data from `v_ace_account`; personal data as the sale terms allow | OutboundFileAdapter over SFTP | Lot awarded (EV-23) | Hold the case step until acknowledged; 3 attempts, then the exception queue |
| INT-17, INT-18 | NSS, LINE OA | Recovery templates | ACE notification path | As sent | ACE |
| INT-22 | PII Kafka, audit and SOC logs | Access and security events | ACE logging | As they happen | ACE |

Every row is an `interface_config` row with direction "OUT". An outbound run is recorded in `outbound_item` and `outbox_delivery`. An outbound file reads ACE through the `recovery.v_ace_*` views only.

### A1.6 Functions removed by D-RCV-35

The inbound interfaces INT-01 to INT-16 leave this module. They are re-owned to ACE ingestion, and their contracts, schedules and acceptance remain in Recovery Workbench Interface Specifications v3 under the inbound family; this FSD keeps only the traceability rows below. The outbound interfaces INT-14, INT-19, INT-20 and INT-25 stay in P2 and keep their contracts there.

| v2 function | Where in v2 | Disposition |
|---|---|---|
| FEAT-DRI-09 file adapters for CCMS, SVAF, AMIS, RPS, WIN and GL | A2.4 | Removed by D-RCV-35 - later home: ACE ingestion |
| Inbound half of FEAT-RDF-21 ("file loads") and FEAT-DRI-10 ("in") | A2.1, A2.5 | Removed by D-RCV-35 - later home: ACE ingestion |
| FileLoadAdapter and the inbound folders | All sections, AC-P2-00n-01 | Removed by D-RCV-35 - later home: ACE ingestion |
| File checks: business date (DQ-057), structure, control total (DQ-059), keys, repeated file | AC-ALT-P2-00n-01, AC-ALT-P2-00n-02 | Removed by D-RCV-35 - later home: ACE ingestion; ACE ingestion refuses a feed whole |
| Missing file at the cut-off, JOB-09 run row "MISSING" | AC-EXC-P2-00n-02 | Removed by D-RCV-35 - later home: ACE ingestion; a late ACE batch raises EV-27 AceDataLate (P1) |
| Inbound run record and sign-off (`interface_run`, `interface_signoff`) | All sections | Removed by D-RCV-35 - later home: ACE ingestion; ACE team sign-off in RWB-ACE-001 |
| JOB-01 COLLINS load check and JOB-09 file loads | Batch and Scheduling Design | Retired by D-RCV-35 |

## A2. Functional decomposition

### A2.1 Run the integration adapters for outbound files

#### A2.1.1 Intent

**Business objective.** Provides the one pattern every outbound file uses: build from Workbench tables and the `recovery.v_ace_*` views, send through the outbox, acknowledge, retry and exception queue. The file-load half of the v2 pattern is removed by D-RCV-35 - later home: ACE ingestion.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Provides the one pattern every outbound file uses: build from Workbench tables and the `recovery.v_ace_*` views, send through the outbox, acknowledge, retry and exception queue. The file-load half of the v2 pattern is removed by D-RCV-35 - later home: ACE ingestion.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the integration adapters for outbound files | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters (outbound); outbox (JOB-11)

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-001-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-001 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-001-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-001-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-001-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-001-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-001-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-001-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-001-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-001-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-001-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-001-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-001-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Queue and retry a failed interface call

#### A2.2.1 Intent

**Business objective.** Holds an outbound call when the target system is unavailable and retries it on the interface schedule.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Holds an outbound call when the target system is unavailable and retries it on the interface schedule.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Queue and retry a failed interface call | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters (outbound); outbox (JOB-11)

**Prerequisites.** FEAT-RDF-21

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-002-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-002 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-002-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-002-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-002-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-002-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-002-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-002-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-002-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-002-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-002-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-002-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-002-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Raise an interface failure to the exception queue

#### A2.3.1 Intent

**Business objective.** Moves a call that has used its retries to the exception queue and raises a task for the platform team.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Moves a call that has used its retries to the exception queue and raises a task for the platform team.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Raise an interface failure to the exception queue | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters (outbound); exception queue (SCR-09)

**Prerequisites.** FEAT-RDF-23

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-003-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-003 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-003-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-003-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-003-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-003-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-003-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-003-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-003-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-003-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-003-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-003-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-003-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Run the file adapters for sources outside COLLINS (removed)

**Status.** Removed by D-RCV-35 - later home: ACE ingestion. CCMS, SVAF, AMIS, RPS, WIN proof of delivery and GL write-off postings land in ACE through ACE's ingestion (INT-10, INT-11, INT-12, INT-13, INT-15, INT-16, into ACE; RWB-ACE-001) and are read through `v_ace_collateral_detail`, `v_ace_valuation`, `v_ace_npa_asset`, `v_ace_npa_sale`, `v_ace_pod` and `v_ace_write_off`. The stories behind the v2 loads leave the backlog (RWB-E1-009, RWB-E1-051; Change Register Appendix A).

The IDs are kept so that traceability does not break. None of them is built or tested.

| ID | v2 content | Disposition |
|---|---|---|
| FEAT-DRI-09 | Loads CCMS, SVAF, AMIS, RPS, WIN and GL files through one adapter pattern | Removed by D-RCV-35 - later home: ACE ingestion |
| VR-P2-004-1, BR-P2-004 | Role permission check; no value in code | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-P2-004-01 | File load "INT-15" declared with FileLoadAdapter | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-ALT-P2-004-01, AC-ALT-P2-004-02 | CCMS file refused on control total and business date | Removed by D-RCV-35 - later home: ACE ingestion |
| AC-EXC-P2-004-01 to AC-EXC-P2-004-06 | Retry, missing file, duplicate, resend, role, decision log | Removed with the feature; the outbound cases are kept in A2.1 to A2.3 and A2.6 |

---

### A2.5 Run outbound file and SFTP adapters

#### A2.5.1 Intent

**Business objective.** Moves bulk data out by file over SFTP where the target has no API: WIN notices (INT-14) and the debt buyer tape (INT-25). The inbound pickup of the v2 adapter is removed by D-RCV-35 - later home: ACE ingestion.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Moves bulk data out by file over SFTP where the target has no API: WIN notices (INT-14) and the debt buyer tape (INT-25). The inbound pickup of the v2 adapter is removed by D-RCV-35 - later home: ACE ingestion.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run outbound file and SFTP adapters | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SFTP (outbound), WIN, debt buyers

**Prerequisites.** FEAT-RDF-21

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-005-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-005 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-005-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-005-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-005-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-005-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-005-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-005-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-005-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-005-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-005-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-005-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-005-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Route every outbound file through the integration adapters

#### A2.6.1 Intent

**Business objective.** Puts every outbound file through one adapter, so retries, logging and throttling are in one place.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Puts every outbound file through one adapter, so retries, logging and throttling are in one place.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route every outbound file through the integration adapters | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters (outbound); data lake (INT-19, INT-20)

**Prerequisites.** FEAT-RDF-21

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-006-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-006 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-006-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-006-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-006-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-006-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-006-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-006-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-006-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-006-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-006-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-006-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-006-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Detect and ignore a duplicate event

#### A2.7.1 Intent

**Business objective.** Recognizes an event that has already been processed by its key, and records the repeat without acting twice. This includes EV-26 AceDataReady, raised from the ACE batch record.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Recognizes an event that has already been processed by its key, and records the repeat without acting twice. This includes EV-26 AceDataReady, raised from the ACE batch record.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: an outbound item, an event or a timer | Reads the version of the rules in force |
| 2 | System | Detect and ignore a duplicate event | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters; outbox; `v_ace_batch_status` for EV-26

**Prerequisites.** FEAT-RDF-21

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-007-1 | Outbound file built while the ACE batch for its business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-P2-007 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P2-007-ACE | An outbound file reads ACE only through `recovery.v_ace_*`; it never reads a public table and never writes to ACE (D-RCV-35, U4) | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-007-01 | Pattern described | a developer adds the outbound file "INT-25" debt buyer data tape | the build pipeline runs | the file is declared as an interface configuration row with direction "OUT" and uses OutboundFileAdapter And the contract test "INT-25" builds the synthetic tape of 120 accounts from debt_sale_account and `v_ace_account` and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter And no interface configuration row has direction "IN" | RWB-E1-007 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-007-01 | Removed by D-RCV-35 - later home: ACE ingestion | v2: CCMS file refused on the control total check "DQ-059" | - | - | - |
| AC-ALT-P2-007-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: file refused on the business date check "DQ-057" | - | - | - |
| AC-ALT-P2-007-03 | Outbound file reads ACE only through the views | 85 approved notices for business date 2026-11-10, each with person_key and contact_key | JOB-10 builds the WIN file "WIN_NOTICE_20261110.txt" | each addressee and address is read from `v_ace_contact` by contact_key And no statement of the build reads a public table And the outbound item records ACE business date 2026-11-10 from `v_ace_batch_status` | RWB-E1-007 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-007-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-007-02 | Removed by D-RCV-35 - later home: ACE ingestion | v2: SVAF file missing at the cut-off, JOB-09 run row "MISSING". A late ACE batch now raises EV-27 AceDataLate (P1) | - | - | - |
| AC-EXC-P2-007-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-007-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-007-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-007-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |
| AC-EXC-P2-007-07 | Duplicate AceDataReady ignored | consumer "case-creation" processed event key "EV-26:ALS:2026-11-10" | the ACE batch record for ALS and business date 2026-11-10 is read again and EV-26 arrives with the same key | JOB-02 does not start a second time for 2026-11-10 And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly. Source data arrives in ACE through ACE's ingestion and is read through the `recovery.v_ace_*` views; data leaves through the paths ACE already has and the Workbench outbound adapters (amended by D-RCV-35). | Must | E1 |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. | Must | E1 |
| REQ-DRI-008 | Data from other systems reaches the Workbench through ACE's ingestion, read through the views; the Workbench runs no file load. Interfaces that need same-day data are named under DL06 before any is built (amended by D-RCV-35). | Must | E1 |
| REQ-DRI-013 | Case hand-over from EFS arrives in ACE through ACE's ingestion and is read through `v_ace_efs_action`, and plan status is read from ACE through `v_ace_plan`, so a case is current the morning after it changes (amended by D-RCV-35). | Must | E2 |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| See the glossary | | |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
