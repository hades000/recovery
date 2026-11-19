<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD P2 Integration v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD P2 Integration v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P2 Integration

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P2 Integration |
| Document ID | P2-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P2 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P2 | Integration | E1 |

**Feature scope.** File adapters, outbound files, use of the ACE integration paths.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P2 Integration | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** File adapters, outbound files, use of the ACE integration paths.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-RDF-21; FEAT-RDF-23

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P2 | FEAT-RDF-21 | Run the integration adapters for file loads and outbound files | System | Provides the one pattern every file load and outbound file uses, with checks, retry and an exception queue. | E1 | A2.1 |
| P2 | FEAT-RDF-23 | Queue and retry a failed interface call | System | Holds an outbound call when the target system is unavailable and retries it on the interface schedule. | E1 | A2.2 |
| P2 | FEAT-RDF-24 | Raise an interface failure to the exception queue | System | Moves a call that has used its retries to the exception queue and raises a task for the platform team. | E1 | A2.3 |
| P2 | FEAT-DRI-09 | Run the file adapters for sources outside COLLINS | System | Loads CCMS, SVAF, AMIS, RPS, WIN and GL files through one adapter pattern, never by a direct call to the source. | E1 | A2.4 |
| P2 | FEAT-DRI-10 | Run file and SFTP adapters | System | Moves bulk data in and out by file where an interface has no API. | E1 | A2.5 |
| P2 | FEAT-DRI-11 | Route every outbound file through the integration adapters | System | Puts every outbound file through one adapter, so retries, logging and throttling are in one place. | E1 | A2.6 |
| P2 | FEAT-DRI-13 | Detect and ignore a duplicate event | System | Recognizes an event that has already been processed by its key, and records the repeat without acting twice. | E1 | A2.7 |

### A1.3 Background

Each system is reached by hand or by a one-off file; failures are found late.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Run the integration adapters for file loads and outbound files

#### A2.1.1 Intent

**Business objective.** Provides the one pattern every file load and outbound file uses, with checks, retry and an exception queue.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Provides the one pattern every file load and outbound file uses, with checks, retry and an exception queue.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the integration adapters for file loads and outbound files | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-001-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-001-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-001-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-001-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-001-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-001-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
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
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Queue and retry a failed interface call | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** FEAT-RDF-21

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-002-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-002-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-002-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-002-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-002-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
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
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Raise an interface failure to the exception queue | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** FEAT-RDF-23

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-003-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-003-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-003-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-003-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-003-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-003-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
| AC-EXC-P2-003-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-003-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-003-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-003-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Run the file adapters for sources outside COLLINS

#### A2.4.1 Intent

**Business objective.** Loads CCMS, SVAF, AMIS, RPS, WIN and GL files through one adapter pattern, never by a direct call to the source.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Loads CCMS, SVAF, AMIS, RPS, WIN and GL files through one adapter pattern, never by a direct call to the source.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the file adapters for sources outside COLLINS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** FEAT-RDF-21

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-004-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-P2-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-004-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-004-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-004-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-004-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-004-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
| AC-EXC-P2-004-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-004-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-004-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-004-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Run file and SFTP adapters

#### A2.5.1 Intent

**Business objective.** Moves bulk data in and out by file where an interface has no API.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Moves bulk data in and out by file where an interface has no API.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run file and SFTP adapters | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SFTP, COLLINS

**Prerequisites.** FEAT-RDF-21

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-005-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-005-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-005-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-005-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-005-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-005-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
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
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route every outbound file through the integration adapters | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** FEAT-RDF-21

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-006-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-006-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-006-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-006-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-006-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-006-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
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

**Business objective.** Recognizes an event that has already been processed by its key, and records the repeat without acting twice.

**Problem.** Each system is reached by hand or by a one-off file; failures are found late.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Outbound items in the exception queue over one day | Zero | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Recognizes an event that has already been processed by its key, and records the repeat without acting twice.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Detect and ignore a duplicate event | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Integration adapters

**Prerequisites.** FEAT-RDF-21

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P2-007-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P2-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P2-007-01 | Pattern described | a developer adds the file load "INT-15" WIN proof of delivery | the build pipeline runs | the load is declared as an interface configuration row and uses FileLoadAdapter And the contract test "INT-15" parses the synthetic sample file of 120 records and passes And the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter | RWB-E1-007 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P2-007-01 | File load checked | a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201 | the adapter loads it | the file is refused whole with failed check "DQ-059 Control total" And no collateral record is passed to the loader And the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale And the data steward is alerted with message MSG-P1-002 | RWB-E1-007 |
| AC-ALT-P2-007-02 | Every file check runs before any record is used | a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected | the adapter loads it | the file is refused with failed check "DQ-057 Business date" And the run row shows status "REFUSED" and record count 0 | RWB-E1-007 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P2-007-01 | Retry and exception queue | the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases And the SFTP transfer fails on attempts 1, 2 and 3 | the outbox sender runs | attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2 And each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33) And after attempt 3 the item status is "EXCEPTION" And each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34) And the item shows in the exception queue with message MSG-P2-001 | RWB-E1-007 |
| AC-EXC-P2-007-02 | File missing at the cut-off | no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00 | JOB-09 runs | the run row for "INT-11" shows status "MISSING" And on 2026-11-10 the SVAF data product is marked stale with message MSG-P1-001 | RWB-E1-007 |
| AC-EXC-P2-007-03 | Duplicate application event ignored | consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1" | the same event arrives again with the same key | the consumer does not act And the hit count for that key becomes 2 (R-UNI-40) | RWB-E1-007 |
| AC-EXC-P2-007-04 | Resend from the exception queue | outbound item "OB-0002" has status "EXCEPTION" after 3 attempts | a platform administrator resends it | the item status is "PENDING" with attempt count 0 And the resend is written to the ACE audit log with the user and the time And the response carries message MSG-GEN-005 | RWB-E1-007 |
| AC-EXC-P2-007-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P2-007-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly. Data comes in through COLLINS or a file load, and leaves through paths ACE already has. | Must | E1 |
| REQ-DRI-007 | The integration adapters log every file in and out, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. | Must | E1 |
| REQ-DRI-008 | Data from other systems moves by the COLLINS daily batch or a file load. Interfaces that need same-day data are named under DL06 before any is built. | Must | E1 |
| REQ-DRI-013 | Case hand-over from EFS arrives in the COLLINS daily load, and plan status is read from the ACE common module, so a case is current the morning after it changes. | Must | E2 |

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
