<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/recovery-workbench-fsd-p6-communications-v2.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/recovery-workbench-fsd-p6-communications-v2.md`. Edit the source, not this copy.

# Recovery Workbench P6 Communications

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P6 Communications |
| Document ID | P6-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P6 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P6 | Communications | E1 notices; E2 dispatch; E4 self-service |

**Feature scope.** Letters, notices, SMS, LINE, proof of delivery.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P6 Communications | TSD | Pair |
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

**In scope.** Letters, notices, SMS, LINE, proof of delivery.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-ACA-04; FEAT-CHO-06; FEAT-COM-01; FEAT-DCM-06; FEAT-DCM-17; FEAT-DCM-19; FEAT-DRI-15; FEAT-DRI-16

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P6 | FEAT-OCC-01 | Generate a letter from an approved template | System | Merges the case facts into the approved template and produces the letter ready to send. | E2 | A2.1 |
| P6 | FEAT-OCC-02 | Dispatch a letter through WIN and capture proof of delivery | System | Sends the letter through WIN, tracks it and writes the proof of delivery back onto the case. | E2 | A2.2 |
| P6 | FEAT-OCC-03 | Dispatch SMS through NSS | System | Sends an SMS from the template, records the result code and the delivery state. | E2 | A2.3 |
| P6 | FEAT-OCC-04 | Dispatch a LINE message through LINE OA | System | Sends a LINE message from the template and records the result on the case. | E2 | A2.4 |
| P6 | FEAT-OCC-05 | Run the conduct check before every outbound contact | System | Tests every outbound message against the conduct and consent rules before it is sent. | E2 | A2.5 |
| P6 | FEAT-OCC-06 | Block an outbound contact when a contact stop is in force | System | Stops the send, records the reason and leaves the message unsent when a stop applies. | E2 | A2.6 |
| P6 | FEAT-OCC-07 | Generate contract, credit approval and mortgage documents | System | Produces the deed in lieu wave 1 document set from templates, with the case and title data merged in. | E2 | A2.7 |
| P6 | FEAT-OCC-08 | Run the e-signature flow for the customer and the bank | User | Sends the document for signature, tracks it and returns the signed copy to the case. | E2 | A2.8 |
| P6 | FEAT-OCC-09 | Record the signature result on the case | System | Writes signed or not signed onto the treatment, which is the event the routing rules read. | E2 | A2.9 |
| P6 | FEAT-OCC-10 | Match a payment to the plan | System | Matches an incoming payment to the plan installment it belongs to and updates the plan state. | E2 | A2.10 |
| P6 | FEAT-OCC-11 | Raise the plan payment missed event | System | Raises the application event for a missed plan payment, which the broken plan rules act on. | E2 | A2.11 |
| P6 | FEAT-OCC-12 | Publish the steering dashboard | User | Gives the Tribe and the steering committee the first view of volume, ageing, owners and decisions. | E2 | A2.12 |
| P6 | FEAT-OCC-13 | Give partners identities through the external gateway | Admin | Issues partner logins through the external gateway with multi-factor authentication, scoped to their own cases. | E2 | A2.13 |
| P6 | FEAT-COM-01 | View the offer on LINE and web | User | Lets the customer see the offer the bank has made, on the channel they use. | E4 | A2.14 |
| P6 | FEAT-COM-02 | Accept an offer in self-service | User | Lets the customer accept without a call or a branch visit, which records the acceptance on the case. | E4 | A2.15 |
| P6 | FEAT-COM-03 | Pay in self-service | User | Lets the customer pay against the plan or the settlement from the same screen. | E4 | A2.16 |
| P6 | FEAT-COM-04 | Raise a dispute in self-service | User | Lets the customer raise a dispute, which opens X1 and applies the contact stop. | E4 | A2.17 |
| P6 | FEAT-COM-05 | Maintain the contact repository | Admin | Keeps the verified contact points for every party, with consent state per channel. | E4 | A2.18 |
| P6 | FEAT-COM-06 | Record a custody movement of a document | System | Tracks a physical document leaving and returning, so the original is never lost. | E4 | A2.19 |
| P6 | FEAT-COM-07 | Answer a legal or audit document request | User | Returns the documents and the index entries a legal or audit request asks for. | E4 | A2.20 |
| P6 | FEAT-COM-08 | Apply retention on case closure | System | Applies the retention class to every document on the case when the case closes. | E4 | A2.21 |

### A1.3 Background

Letters and notices are prepared by hand; proof of delivery is chased by phone.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Generate a letter from an approved template

#### A2.1.1 Intent

**Business objective.** Merges the case facts into the approved template and produces the letter ready to send.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Merges the case facts into the approved template and produces the letter ready to send.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate a letter from an approved template | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, WIN

**Prerequisites.** FEAT-DRI-15

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-001-1 | Template withdrawn (R-LIT-04) | MSG-P6-003 The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| BR-P6-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-001-01 | Dispatch | JOB-10 runs at 16:00 on 2026-12-14 | the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026 | notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15 And the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH" And GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH" | RWB-E2-021 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-001-01 | Proof back | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026 | notice "N-0101" is "Delivered" with callback date 2026-12-18 And the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18 And case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18 | RWB-E2-021 |
| AC-ALT-P6-001-02 | Undelivered | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE" | notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE" And one decision log entry exists with decision code "D7.1" and rule "R-LIT-09" And case "RC-2026-000321" is transferred to its owner's queue with reason "NOTICE_UNSERVED" And the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE" And no notice period timer is started | RWB-E2-021 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-001-01 | Consent withdrawn does not stop a statutory notice | the borrower's postal address contact point has consent status "WITHDRAWN" And notice type "DEMAND" is a statutory notice | JOB-10 runs on 2026-12-14 | notice "N-0101" is written to the WIN file And the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn" | RWB-E2-021 |
| AC-EXC-P6-001-02 | Template withdrawn after approval | template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13 | JOB-10 runs on 2026-12-14 | notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file And a task is raised to the litigation officer team with MSG-P6-003 | RWB-E2-021 |
| AC-EXC-P6-001-03 | Decision log write fails on a held notice | case "RC-2026-000321" has an open deviation "X2" with contact stop on And the decision log store is unavailable | JOB-10 runs on 2026-12-14 | notice "N-0101" stays "Approved" and is not in the WIN file And the job record shows MSG-P7-003 for "N-0101" And an incident is raised under rule R-UNI-39 | RWB-E2-021 |
| AC-EXC-P6-001-04 | Repeated request | "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001" | the same request is sent again with Idempotency-Key "a1b2c3d4-0001" | the response is the first notice with status 201 And case "RC-2026-000321" has one RECALL notice | RWB-E2-021 |
| AC-EXC-P6-001-05 | Notice type missing | "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope | "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type | the response is status 422 with MSG-GEN-001 naming "notice type" | RWB-E2-021 |
| AC-EXC-P6-001-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-001-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-001-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.2 Dispatch a letter through WIN and capture proof of delivery

#### A2.2.1 Intent

**Business objective.** Sends the letter through WIN, tracks it and writes the proof of delivery back onto the case.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Sends the letter through WIN, tracks it and writes the proof of delivery back onto the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Dispatch a letter through WIN and capture proof of delivery | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN

**Prerequisites.** FEAT-OCC-01, FEAT-DRI-17

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-002-01 | Dispatch | JOB-10 runs at 16:00 on 2026-12-14 | the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026 | notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15 And the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH" And GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH" | RWB-E2-021 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-002-01 | Proof back | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026 | notice "N-0101" is "Delivered" with callback date 2026-12-18 And the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18 And case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18 | RWB-E2-021 |
| AC-ALT-P6-002-02 | Undelivered | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE" | notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE" And one decision log entry exists with decision code "D7.1" and rule "R-LIT-09" And case "RC-2026-000321" is transferred to its owner's queue with reason "NOTICE_UNSERVED" And the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE" And no notice period timer is started | RWB-E2-021 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-002-01 | Consent withdrawn does not stop a statutory notice | the borrower's postal address contact point has consent status "WITHDRAWN" And notice type "DEMAND" is a statutory notice | JOB-10 runs on 2026-12-14 | notice "N-0101" is written to the WIN file And the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn" | RWB-E2-021 |
| AC-EXC-P6-002-02 | Template withdrawn after approval | template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13 | JOB-10 runs on 2026-12-14 | notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file And a task is raised to the litigation officer team with MSG-P6-003 | RWB-E2-021 |
| AC-EXC-P6-002-03 | Decision log write fails on a held notice | case "RC-2026-000321" has an open deviation "X2" with contact stop on And the decision log store is unavailable | JOB-10 runs on 2026-12-14 | notice "N-0101" stays "Approved" and is not in the WIN file And the job record shows MSG-P7-003 for "N-0101" And an incident is raised under rule R-UNI-39 | RWB-E2-021 |
| AC-EXC-P6-002-04 | Repeated request | "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001" | the same request is sent again with Idempotency-Key "a1b2c3d4-0001" | the response is the first notice with status 201 And case "RC-2026-000321" has one RECALL notice | RWB-E2-021 |
| AC-EXC-P6-002-05 | Notice type missing | "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope | "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type | the response is status 422 with MSG-GEN-001 naming "notice type" | RWB-E2-021 |
| AC-EXC-P6-002-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-002-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-002-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.3 Dispatch SMS through NSS

#### A2.3.1 Intent

**Business objective.** Sends an SMS from the template, records the result code and the delivery state.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Sends an SMS from the template, records the result code and the delivery state.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Dispatch SMS through NSS | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** NSS

**Prerequisites.** FEAT-OCC-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-003-1 | Template withdrawn (R-LIT-04) | MSG-P6-003 The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| BR-P6-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-003-01 | SMS sent | party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" | "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077" | the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED" And the interaction has delivery status "DELIVERED" and reference "NSS-7781" And NSS received one message | RWB-E2-022 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-003-01 | LINE | party "P-0077" has a verified "LINE" contact point with consent "GIVEN" | "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND" | the interaction has channel "LINE", conduct check "PASSED" and delivery status "READ" And LINE OA received one message | RWB-E2-022 |
| AC-ALT-P6-003-02 | Contact stop on lost contact | case "RC-2026-000777" has an open deviation "X6" lost contact | "CO-0201" sends a message with channel "SMS" | the response is status 409 with MSG-P6-001 naming "X6 Lost contact" And nothing is sent to NSS And an interaction with conduct check "BLOCKED" is written And one decision log entry exists with decision code "X6" and final call "contact refused" | RWB-E2-022 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-003-01 | No consent on the channel | party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN" | "CO-0201" sends a message with channel "SMS" | the response is status 409 with MSG-P6-002 naming "SMS" And nothing is sent to NSS And an interaction with conduct check "BLOCKED" is written | RWB-E2-022 |
| AC-EXC-P6-003-02 | Template withdrawn | template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved | "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND" | the response is status 409 with MSG-P6-003 naming "SMS-REMIND" | RWB-E2-022 |
| AC-EXC-P6-003-03 | NSS unavailable | the ACE notification path returns "unavailable" for NSS | "CO-0201" sends a message with channel "SMS" | the response is status 202 with MSG-GEN-006 naming "NSS" And JOB-11 retries the send on its schedule And after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED" | RWB-E2-022 |
| AC-EXC-P6-003-04 | NSS failure result | party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0 | NSS returns result "FAILED" for the message | the interaction has delivery status "FAILED" And the contact point has failed count 1 | RWB-E2-022 |
| AC-EXC-P6-003-05 | Repeated request | "CO-0201" sent a message with Idempotency-Key "c0ffee00-0001" | the same request is sent again with Idempotency-Key "c0ffee00-0001" | the response is the first response And NSS received one message | RWB-E2-022 |
| AC-EXC-P6-003-06 | Decision log write fails on a refusal | case "RC-2026-000777" has an open deviation "X6" And the decision log store is unavailable | "CO-0201" sends a message with channel "SMS" | the response is status 503 with MSG-P7-003 And nothing is sent to NSS And an incident is raised under rule R-UNI-39 | RWB-E2-022 |
| AC-EXC-P6-003-07 | Channel missing | template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point | "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel | the response is status 422 with MSG-GEN-001 naming "channel" | RWB-E2-022 |
| AC-EXC-P6-003-08 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-003-09 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-003-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.4 Dispatch a LINE message through LINE OA

#### A2.4.1 Intent

**Business objective.** Sends a LINE message from the template and records the result on the case.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Sends a LINE message from the template and records the result on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Dispatch a LINE message through LINE OA | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** LINE OA

**Prerequisites.** FEAT-OCC-01

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-004-1 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| VR-P6-004-2 | Template withdrawn (R-LIT-04) | MSG-P6-003 The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| BR-P6-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-004-01 | SMS sent | party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" | "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077" | the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED" And the interaction has delivery status "DELIVERED" and reference "NSS-7781" And NSS received one message | RWB-E2-022 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-004-01 | LINE | party "P-0077" has a verified "LINE" contact point with consent "GIVEN" | "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND" | the interaction has channel "LINE", conduct check "PASSED" and delivery status "READ" And LINE OA received one message | RWB-E2-022 |
| AC-ALT-P6-004-02 | Contact stop on lost contact | case "RC-2026-000777" has an open deviation "X6" lost contact | "CO-0201" sends a message with channel "SMS" | the response is status 409 with MSG-P6-001 naming "X6 Lost contact" And nothing is sent to NSS And an interaction with conduct check "BLOCKED" is written And one decision log entry exists with decision code "X6" and final call "contact refused" | RWB-E2-022 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-004-01 | No consent on the channel | party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN" | "CO-0201" sends a message with channel "SMS" | the response is status 409 with MSG-P6-002 naming "SMS" And nothing is sent to NSS And an interaction with conduct check "BLOCKED" is written | RWB-E2-022 |
| AC-EXC-P6-004-02 | Template withdrawn | template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved | "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND" | the response is status 409 with MSG-P6-003 naming "SMS-REMIND" | RWB-E2-022 |
| AC-EXC-P6-004-03 | NSS unavailable | the ACE notification path returns "unavailable" for NSS | "CO-0201" sends a message with channel "SMS" | the response is status 202 with MSG-GEN-006 naming "NSS" And JOB-11 retries the send on its schedule And after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED" | RWB-E2-022 |
| AC-EXC-P6-004-04 | NSS failure result | party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0 | NSS returns result "FAILED" for the message | the interaction has delivery status "FAILED" And the contact point has failed count 1 | RWB-E2-022 |
| AC-EXC-P6-004-05 | Repeated request | "CO-0201" sent a message with Idempotency-Key "c0ffee00-0001" | the same request is sent again with Idempotency-Key "c0ffee00-0001" | the response is the first response And NSS received one message | RWB-E2-022 |
| AC-EXC-P6-004-06 | Decision log write fails on a refusal | case "RC-2026-000777" has an open deviation "X6" And the decision log store is unavailable | "CO-0201" sends a message with channel "SMS" | the response is status 503 with MSG-P7-003 And nothing is sent to NSS And an incident is raised under rule R-UNI-39 | RWB-E2-022 |
| AC-EXC-P6-004-07 | Channel missing | template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point | "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel | the response is status 422 with MSG-GEN-001 naming "channel" | RWB-E2-022 |
| AC-EXC-P6-004-08 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-004-09 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-004-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.5 Run the conduct check before every outbound contact

#### A2.5.1 Intent

**Business objective.** Tests every outbound message against the conduct and consent rules before it is sent.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Tests every outbound message against the conduct and consent rules before it is sent.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the conduct check before every outbound contact | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-OCC-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-005-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-005-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-005-01 | Dispatch | JOB-10 runs at 16:00 on 2026-12-14 | the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026 | notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15 And the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH" And GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH" | RWB-E2-021 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-005-01 | Proof back | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026 | notice "N-0101" is "Delivered" with callback date 2026-12-18 And the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18 And case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18 | RWB-E2-021 |
| AC-ALT-P6-005-02 | Undelivered | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE" | notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE" And one decision log entry exists with decision code "D7.1" and rule "R-LIT-09" And case "RC-2026-000321" is transferred to its owner's queue with reason "NOTICE_UNSERVED" And the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE" And no notice period timer is started | RWB-E2-021 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-005-01 | Consent withdrawn does not stop a statutory notice | the borrower's postal address contact point has consent status "WITHDRAWN" And notice type "DEMAND" is a statutory notice | JOB-10 runs on 2026-12-14 | notice "N-0101" is written to the WIN file And the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn" | RWB-E2-021 |
| AC-EXC-P6-005-02 | Template withdrawn after approval | template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13 | JOB-10 runs on 2026-12-14 | notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file And a task is raised to the litigation officer team with MSG-P6-003 | RWB-E2-021 |
| AC-EXC-P6-005-03 | Decision log write fails on a held notice | case "RC-2026-000321" has an open deviation "X2" with contact stop on And the decision log store is unavailable | JOB-10 runs on 2026-12-14 | notice "N-0101" stays "Approved" and is not in the WIN file And the job record shows MSG-P7-003 for "N-0101" And an incident is raised under rule R-UNI-39 | RWB-E2-021 |
| AC-EXC-P6-005-04 | Repeated request | "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001" | the same request is sent again with Idempotency-Key "a1b2c3d4-0001" | the response is the first notice with status 201 And case "RC-2026-000321" has one RECALL notice | RWB-E2-021 |
| AC-EXC-P6-005-05 | Notice type missing | "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope | "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type | the response is status 422 with MSG-GEN-001 naming "notice type" | RWB-E2-021 |
| AC-EXC-P6-005-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-005-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-005-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.6 Block an outbound contact when a contact stop is in force

#### A2.6.1 Intent

**Business objective.** Stops the send, records the reason and leaves the message unsent when a stop applies.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Stops the send, records the reason and leaves the message unsent when a stop applies.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Block an outbound contact when a contact stop is in force | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-OCC-05, FEAT-DVH-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-006-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-006-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer, Complaint officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-006-01 | Dispatch | JOB-10 runs at 16:00 on 2026-12-14 | the conduct check passes and WIN acknowledges contract "CT-88001" with barcode "RR223344556TH" and sent date 15122026 | notice "N-0101" is "Sent" with barcode "RR223344556TH" and sent date 2026-12-15 And the ledger entry for the letter has conduct check "PASSED" and summary naming barcode "RR223344556TH" And GET /notices/N-0101 returns sentDate 2026-12-15 and barcode "RR223344556TH" | RWB-E2-021 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-006-01 | Proof back | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "DELIVERED" and call-back date 18122026 | notice "N-0101" is "Delivered" with callback date 2026-12-18 And the ledger has an entry "Delivered" for case "RC-2026-000321" on 2026-12-18 And case "RC-2026-000321" has a running "NOTICE_PERIOD" timer started on 2026-12-18 | RWB-E2-021 |
| AC-ALT-P6-006-02 | Undelivered | notice "N-0101" is "Sent" on 2026-12-15 | the INT-15 file of 2026-12-21 returns barcode "RR223344556TH" with result "UNDELIVERABLE" | notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE" And one decision log entry exists with decision code "D7.1" and rule "R-LIT-09" And case "RC-2026-000321" is transferred to its owner's queue with reason "NOTICE_UNSERVED" And the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE" And no notice period timer is started | RWB-E2-021 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-006-01 | Consent withdrawn does not stop a statutory notice | the borrower's postal address contact point has consent status "WITHDRAWN" And notice type "DEMAND" is a statutory notice | JOB-10 runs on 2026-12-14 | notice "N-0101" is written to the WIN file And the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn" | RWB-E2-021 |
| AC-EXC-P6-006-02 | Template withdrawn after approval | template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13 | JOB-10 runs on 2026-12-14 | notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file And a task is raised to the litigation officer team with MSG-P6-003 | RWB-E2-021 |
| AC-EXC-P6-006-03 | Decision log write fails on a held notice | case "RC-2026-000321" has an open deviation "X2" with contact stop on And the decision log store is unavailable | JOB-10 runs on 2026-12-14 | notice "N-0101" stays "Approved" and is not in the WIN file And the job record shows MSG-P7-003 for "N-0101" And an incident is raised under rule R-UNI-39 | RWB-E2-021 |
| AC-EXC-P6-006-04 | Repeated request | "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001" | the same request is sent again with Idempotency-Key "a1b2c3d4-0001" | the response is the first notice with status 201 And case "RC-2026-000321" has one RECALL notice | RWB-E2-021 |
| AC-EXC-P6-006-05 | Notice type missing | "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope | "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type | the response is status 422 with MSG-GEN-001 naming "notice type" | RWB-E2-021 |
| AC-EXC-P6-006-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-006-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-006-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.7 Generate contract, credit approval and mortgage documents

#### A2.7.1 Intent

**Business objective.** Produces the deed in lieu wave 1 document set from templates, with the case and title data merged in.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Produces the deed in lieu wave 1 document set from templates, with the case and title data merged in.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate contract, credit approval and mortgage documents | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub, CCMS

**Prerequisites.** FEAT-DRI-16

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-007-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR), Legal counsel | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-007-01 | Generate | the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10 | the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT" | one document is stored with document_type "CONTRACT", source "GENERATED", state "DRAFT" and write_once false And the document carries template_code "DIL-CONTRACT", template_version 2 and treatment_id "TRT-0301" And the PDF shows "1,250,000.00 บาท (หนึ่งล้านสองแสนห้าหมื่นบาทถ้วน)" and "10 ธันวาคม 2569" And one decision log entry is written with decision code "D6.4" and an inputs reference to the merge snapshot And one DocumentStored event is in the outbox | RWB-E2-026 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-007-01 | Version | template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15 And document "DOC-0310" was generated on 2026-12-10 from version 2 | the engine runs on 2026-12-15 | the new document carries template_version 3 And "DOC-0310" still carries template_version 2 and its file opens And template version 2 stays readable in the template catalog | RWB-E2-026 |
| AC-ALT-P6-007-02 | Two requests at the same time | two requests for treatment "TRT-0301" and template "DIL-CONTRACT" with different keys arrive together | both run | one returns 201 with one DRAFT document And the other returns 409 with MSG-GEN-004 | RWB-E2-026 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-007-01 | Missing field | the case has no title_doc_no | the engine runs for template "DIL-CONTRACT" | the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no" And no document, no file and no decision log entry is stored | RWB-E2-026 |
| AC-EXC-P6-007-02 | A version not approved by Legal is refused | template "DIL-CA" has only version 1 with approved_by_legal false | the engine runs for template "DIL-CA" | the response is 422 with MSG-P5-010 naming "DIL-CA" version 1 And nothing is stored | RWB-E2-026 |
| AC-EXC-P6-007-03 | A withdrawn template holds generation | template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved | the engine runs for template "DIL-MORTGAGE" | the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE" And a task is raised to the restructuring officer who requested it | RWB-E2-026 |
| AC-EXC-P6-007-04 | A treatment that is not approved is refused | treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id | the engine runs for treatment "TRT-0302" | the response is 409 with MSG-P5-011 And nothing is stored | RWB-E2-026 |
| AC-EXC-P6-007-05 | The decision log write fails | the decision log store does not accept writes | the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT" | the response is 503 with MSG-P7-003 And no document row exists for "TRT-0301" and the draft file is removed from the container And an incident is raised as in R-UNI-39 | RWB-E2-026 |
| AC-EXC-P6-007-06 | A repeated request | a request with Idempotency-Key "K-0301" generated document "DOC-0311" | the same request with Idempotency-Key "K-0301" arrives again | the response is 201 with document "DOC-0311" And no second document or decision log entry is written | RWB-E2-026 |
| AC-EXC-P6-007-07 | A template body that cannot be rendered | the body of "DIL-CONTRACT" version 2 is a damaged file | the engine runs | the response is 503 with MSG-GEN-006 naming "document generation" And nothing is stored and an incident is raised | RWB-E2-026 |
| AC-EXC-P6-007-08 | No template for the product group | template "DIL-CONTRACT" exists only for product group "MORTGAGE" And case "RW-2026-000305" has product group "HIRE_PURCHASE" | the engine runs for that case and "DIL-CONTRACT" | the response is 422 with MSG-P5-010 naming "DIL-CONTRACT" for "HIRE_PURCHASE" | RWB-E2-026 |
| AC-EXC-P6-007-09 | A set is stored whole or not at all | templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved And template "DIL-CA" has no version approved by Legal | the engine runs for treatment "TRT-0301" with the three template codes | the response is 422 with MSG-P5-010 naming "DIL-CA" And none of the three documents is stored and no decision log entry is written | RWB-E2-026 |
| AC-EXC-P6-007-10 | Generate for a treatment that is not approved | treatment "TRT-0402" of type "DEED_IN_LIEU" has no decision_log_id | the officer opens SCR-14 for "TRT-0402" | Generate documents is disabled with MSG-P5-011 And a direct call to POST generated-documents returns 409 with MSG-P5-011 | RWB-E2-017 |
| AC-EXC-P6-007-11 | A locked value cannot be corrected | transfer_price is locked in the merge field catalog | the officer tries to change transfer_price on "DOC-0411" from 1250000.00 to 1200000.00 | the response is 422 with MSG-P5-014 naming "Transfer price" And nothing changes | RWB-E2-017 |
| AC-EXC-P6-007-12 | Send with a draft not reviewed | two drafts of "TRT-0401" are "REVIEWED" and "DIL-MORTGAGE" is still "DRAFT" | the officer chooses Send for signature | the response is 422 with MSG-P5-013 naming the mortgage document And no document is copied to the write-once container and no signature request starts | RWB-E2-017 |
| AC-EXC-P6-007-13 | A sent document cannot be changed | "DOC-0411" is in state "SENT" | the officer tries to correct contract_date | the response is 409 with MSG-P5-002 And "DOC-0411" is unchanged | RWB-E2-017 |
| AC-EXC-P6-007-14 | The decision log write fails on a correction | the decision log store does not accept writes | the officer corrects contract_date on "DOC-0411" with a reason | the response is 503 with MSG-P7-003 And "DOC-0411" stays at its doc_version and no file is added | RWB-E2-017 |
| AC-EXC-P6-007-15 | The signature service refuses the request | SignatureRequests in P6 returns "UNAVAILABLE" | the officer chooses Send for signature for the three reviewed drafts | the response is 503 with MSG-GEN-006 naming "e-signature" And the documents stay in state "REVIEWED" And a second send after the service returns completes with one signature request | RWB-E2-017 |
| AC-EXC-P6-007-16 | The template changed after the drafts were made | the three drafts were made from "DIL-CONTRACT" version 2 And "DIL-CONTRACT" version 3 became current after the drafts were made | the officer chooses Send for signature | the response is 422 with MSG-P5-013 naming the contract and "template version 3" And no document is sent | RWB-E2-017 |
| AC-EXC-P6-007-17 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-007-18 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-007-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.8 Run the e-signature flow for the customer and the bank

#### A2.8.1 Intent

**Business objective.** Sends the document for signature, tracks it and returns the signed copy to the case.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Sends the document for signature, tracks it and returns the signed copy to the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Restructuring officer (FCR) | Opens the screen and run the e-signature flow for the customer and the bank | Checks the role, the capability area and the scope |
| 2 | Restructuring officer (FCR) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** E-signature, the Workbench document hub

**Prerequisites.** FEAT-OCC-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-008-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-008-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Restructuring officer (FCR) | Primary |
| Customer (borrower), Legal counsel | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-008-01 | Customer signs | "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10 | EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00 | within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true And the signature request has status "SIGNED" and signed at 2026-12-11 10:15:00 And TreatmentApi.recordSignature is called for "T-0501" with signed true and method "E_SIGNATURE" | RWB-E2-018 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-008-01 | Branch | "RS-0301" created a signature request for "D-0601" with method "BRANCH" And the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12 | "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12 | the signature request has status "SIGNED" and method "BRANCH" And "D-0602" is linked to the case as the signed agreement And TreatmentApi.recordSignature is called for "T-0501" with signed true and method "BRANCH" | RWB-E2-018 |
| AC-ALT-P6-008-02 | DIL paper | case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE" And its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED" And "RS-0301" created a signature request for "D-0701" with method "PAPER" | "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14 | the signature request has status "SIGNED" and method "PAPER" And TreatmentApi.recordSignature is called for "T-0502" with signed true and method "PAPER" And P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18 | RWB-E2-018 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-008-01 | E-signature refused where Legal requires wet ink | document "D-0701" has signature basis "WET_INK_REQUIRED" | "RS-0301" sends POST /treatments/T-0502/signature-requests with method "E_SIGNATURE" for "D-0701" | the response is status 409 with MSG-P6-009 naming "DIL-CONTRACT-MTG" And no request is sent to EasyApp | RWB-E2-018 |
| AC-EXC-P6-008-02 | Offer validity passes with no signature | "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT" And P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel | EasyApp returns signing result "SIGNED" for that request on 2026-12-21 | the signature request keeps status "EXPIRED" And the result is held on the exception queue And TreatmentApi.recordSignature is not called | RWB-E2-018 |
| AC-EXC-P6-008-03 | EasyApp path unavailable | the ACE path to EasyApp returns "unavailable" | "RS-0301" sends "D-0601" for e-signature | the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp" And JOB-11 retries the send until it is accepted or the retry limit of 5 is reached | RWB-E2-018 |
| AC-EXC-P6-008-04 | Signing result repeated | the signing result "SIGNED" for request reference "EA-30001" was applied | the same result for "EA-30001" arrives again | no second document is stored And TreatmentApi.recordSignature is called once And the repeat is counted under rule R-UNI-40 | RWB-E2-018 |
| AC-EXC-P6-008-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-008-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-008-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.9 Record the signature result on the case

#### A2.9.1 Intent

**Business objective.** Writes signed or not signed onto the treatment, which is the event the routing rules read.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Writes signed or not signed onto the treatment, which is the event the routing rules read.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the signature result on the case | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-OCC-08

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-009-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-009-01 | Customer signs | "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10 | EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00 | within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true And the signature request has status "SIGNED" and signed at 2026-12-11 10:15:00 And TreatmentApi.recordSignature is called for "T-0501" with signed true and method "E_SIGNATURE" | RWB-E2-018 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-009-01 | Branch | "RS-0301" created a signature request for "D-0601" with method "BRANCH" And the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12 | "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12 | the signature request has status "SIGNED" and method "BRANCH" And "D-0602" is linked to the case as the signed agreement And TreatmentApi.recordSignature is called for "T-0501" with signed true and method "BRANCH" | RWB-E2-018 |
| AC-ALT-P6-009-02 | DIL paper | case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE" And its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED" And "RS-0301" created a signature request for "D-0701" with method "PAPER" | "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14 | the signature request has status "SIGNED" and method "PAPER" And TreatmentApi.recordSignature is called for "T-0502" with signed true and method "PAPER" And P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18 | RWB-E2-018 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-009-01 | E-signature refused where Legal requires wet ink | document "D-0701" has signature basis "WET_INK_REQUIRED" | "RS-0301" sends POST /treatments/T-0502/signature-requests with method "E_SIGNATURE" for "D-0701" | the response is status 409 with MSG-P6-009 naming "DIL-CONTRACT-MTG" And no request is sent to EasyApp | RWB-E2-018 |
| AC-EXC-P6-009-02 | Offer validity passes with no signature | "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT" And P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel | EasyApp returns signing result "SIGNED" for that request on 2026-12-21 | the signature request keeps status "EXPIRED" And the result is held on the exception queue And TreatmentApi.recordSignature is not called | RWB-E2-018 |
| AC-EXC-P6-009-03 | EasyApp path unavailable | the ACE path to EasyApp returns "unavailable" | "RS-0301" sends "D-0601" for e-signature | the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp" And JOB-11 retries the send until it is accepted or the retry limit of 5 is reached | RWB-E2-018 |
| AC-EXC-P6-009-04 | Signing result repeated | the signing result "SIGNED" for request reference "EA-30001" was applied | the same result for "EA-30001" arrives again | no second document is stored And TreatmentApi.recordSignature is called once And the repeat is counted under rule R-UNI-40 | RWB-E2-018 |
| AC-EXC-P6-009-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-009-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-009-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.10 Match a payment to the plan

#### A2.10.1 Intent

**Business objective.** Matches an incoming payment to the plan installment it belongs to and updates the plan state.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Matches an incoming payment to the plan installment it belongs to and updates the plan state.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Match a payment to the plan | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL, Workbench

**Prerequisites.** FEAT-CHO-06

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-010-01 | Payment matched | the ALS load for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14 | JOB-07 runs on 2026-12-15 | a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT" And TreatmentApi.recordInstallmentPaid is called for "T-0701" with due date 2026-12-15 And ProceedsMatched is written to the outbox And after the ALS load of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15 | RWB-E2-008 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-010-01 | Missed payment | no payment on account "A-0555" was loaded between 2026-12-05 and 2026-12-15 | JOB-07 runs on 2026-12-16 for business date 2026-12-15 | PaymentMissed is written to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00 And P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27 And the transfer rule records the case movement for reason "payment missed" | RWB-E2-008 |
| AC-ALT-P6-010-02 | Window boundary | plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16 And the ALS load for business date 2026-12-05 holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05 And the same load holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05 | JOB-07 runs on 2026-12-06 | "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" And "PAY-90005", 11 days before its due date, is matched to "UNMATCHED" | RWB-E2-008 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-010-01 | Exception | the ALS load for business date 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555" | JOB-07 runs on 2026-12-15 | a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment And GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer And the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14 | RWB-E2-008 |
| AC-EXC-P6-010-02 | Payment on an account with no open case | the ALS load holds payment "PAY-90003" on account "A-0999" that is on no open case | JOB-07 runs on 2026-12-15 | no proceeds row is written for "PAY-90003" And "PAY-90003" is held on the data quality exception list with check "References" | RWB-E2-008 |
| AC-EXC-P6-010-03 | ALS load refused | the ALS load for business date 2026-12-15 was refused at check "control total" | the scheduled time for JOB-07 on 2026-12-16 passes | JOB-07 does not run for business date 2026-12-15 And no PaymentMissed is written for due date 2026-12-15 And the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14 | RWB-E2-008 |
| AC-EXC-P6-010-04 | Repeated run | JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment | JOB-07 is rerun for business date 2026-12-14 from SCR-44 | the proceeds table still has 2 rows for business date 2026-12-14 And no second ProceedsMatched or PaymentMissed is written | RWB-E2-008 |
| AC-EXC-P6-010-05 | No parameter row in force | no payment matching parameter row is valid on 2026-12-15 | JOB-07 starts for business date 2026-12-15 | it stops before matching with MSG-P8-002 And no proceeds row and no event is written And the job monitor shows JOB-07 as failed with an alert to Credit Administration | RWB-E2-008 |
| AC-EXC-P6-010-06 | Late payment inside and outside the window | the ALS load for 2026-12-18 holds payment "PAY-91004" of 12,500.00 THB on account "A-0555", 3 days after due date 2026-12-15 And the same load holds payment "PAY-91005" of 12,500.00 THB on account "A-0666" of plan "T-0702", 4 days after its due date 2026-12-14 | JOB-07 runs on 2026-12-19 | "PAY-91004" is matched with row "WINDOW" and P3 receives PAYMENT_RECEIVED_LATE under R-RES-28 And "PAY-91005" is matched to "UNMATCHED" with a decision log entry under rule "R-UNI-03" | RWB-E2-027 |
| AC-EXC-P6-010-07 | Invalid parameter load refused | a parameter file for version "PM-2027.02" where rows "WINDOW" and "PARTIAL" both have priority 2 and "PARTIAL" has tolerance 120 | it is loaded through POST /admin/reference-loads | the response is status 422 with MSG-GEN-002 naming "amount_tolerance_pct", 0 and 100 And the load is refused whole and "PM-2026.12" stays in force | RWB-E2-027 |
| AC-EXC-P6-010-08 | Decision log write fails | the decision log store is unavailable during JOB-07 on 2026-12-15 | "PAY-91001" is matched | no proceeds row is written for "PAY-91001" And the run summary shows MSG-P7-003 for "PAY-91001" And an incident is raised under rule R-UNI-39 And the next run of JOB-07 for 2026-12-14 matches "PAY-91001" | RWB-E2-027 |
| AC-EXC-P6-010-09 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-010-10 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-010-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.11 Raise the plan payment missed event

#### A2.11.1 Intent

**Business objective.** Raises the application event for a missed plan payment, which the broken plan rules act on.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Raises the application event for a missed plan payment, which the broken plan rules act on.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Raise the plan payment missed event | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-OCC-10

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-011-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-011-01 | Payment matched | the ALS load for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14 | JOB-07 runs on 2026-12-15 | a proceeds row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00 and matched to "INSTALLMENT" And TreatmentApi.recordInstallmentPaid is called for "T-0701" with due date 2026-12-15 And ProceedsMatched is written to the outbox And after the ALS load of 2026-12-15 the plan shows installments paid 4 and next due date 2027-01-15 | RWB-E2-008 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-011-01 | Missed payment | no payment on account "A-0555" was loaded between 2026-12-05 and 2026-12-15 | JOB-07 runs on 2026-12-16 for business date 2026-12-15 | PaymentMissed is written to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00 And P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27 And the transfer rule records the case movement for reason "payment missed" | RWB-E2-008 |
| AC-ALT-P6-011-02 | Window boundary | plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16 And the ALS load for business date 2026-12-05 holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05 And the same load holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05 | JOB-07 runs on 2026-12-06 | "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" And "PAY-90005", 11 days before its due date, is matched to "UNMATCHED" | RWB-E2-008 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-011-01 | Exception | the ALS load for business date 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555" | JOB-07 runs on 2026-12-15 | a proceeds row exists for "PAY-90002" with matched to "UNMATCHED" and no treatment And GET /proceeds?matched=false returns "PAY-90002" for the Credit Administration officer And the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14 | RWB-E2-008 |
| AC-EXC-P6-011-02 | Payment on an account with no open case | the ALS load holds payment "PAY-90003" on account "A-0999" that is on no open case | JOB-07 runs on 2026-12-15 | no proceeds row is written for "PAY-90003" And "PAY-90003" is held on the data quality exception list with check "References" | RWB-E2-008 |
| AC-EXC-P6-011-03 | ALS load refused | the ALS load for business date 2026-12-15 was refused at check "control total" | the scheduled time for JOB-07 on 2026-12-16 passes | JOB-07 does not run for business date 2026-12-15 And no PaymentMissed is written for due date 2026-12-15 And the plan view shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14 | RWB-E2-008 |
| AC-EXC-P6-011-04 | Repeated run | JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment | JOB-07 is rerun for business date 2026-12-14 from SCR-44 | the proceeds table still has 2 rows for business date 2026-12-14 And no second ProceedsMatched or PaymentMissed is written | RWB-E2-008 |
| AC-EXC-P6-011-05 | No parameter row in force | no payment matching parameter row is valid on 2026-12-15 | JOB-07 starts for business date 2026-12-15 | it stops before matching with MSG-P8-002 And no proceeds row and no event is written And the job monitor shows JOB-07 as failed with an alert to Credit Administration | RWB-E2-008 |
| AC-EXC-P6-011-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-011-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-011-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.12 Publish the steering dashboard

#### A2.12.1 Intent

**Business objective.** Gives the Tribe and the steering committee the first view of volume, ageing, owners and decisions.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Gives the Tribe and the steering committee the first view of volume, ageing, owners and decisions.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reporting and BI analyst | Opens the screen and publish the steering dashboard | Checks the role, the capability area and the scope |
| 2 | Reporting and BI analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-19

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P6-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reporting and BI analyst | Primary |
| Tribe lead and squad members, Finance and CFO delegate | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-012-01 | Refresh | the loads of business date 2026-12-15 passed their checks | JOB-15 runs at 01:30 on 2026-12-16 | GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15" And the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh | RWB-E2-009 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-012-01 | Reconciles | the case list shows 240 open cases at the 2026-12-15 cut-off | JOB-15 runs at 01:30 on 2026-12-16 | the sum of "CASES_BY_STAGE" for 2026-12-15 is 240 And "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day | RWB-E2-009 |
| AC-ALT-P6-012-02 | Agent measures | agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason | JOB-15 runs at 01:30 on 2026-12-16 | "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent And "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent And SCR-37 shows both rates by agent | RWB-E2-009 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-012-01 | Counts do not match | the case list shows 240 open cases at the 2026-12-15 cut-off And the case facts read for the dashboard total 239 | JOB-15 runs at 01:30 on 2026-12-16 | no snapshot rows and no extract are published for 2026-12-15 And SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15 And an alert goes to the Reporting and BI analyst and the data steward | RWB-E2-009 |
| AC-EXC-P6-012-02 | Agent with no runs | agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15 | JOB-15 runs at 01:30 on 2026-12-16 | no "AGENT_ACCEPTANCE" value is written for "deviation-screen" on 2026-12-15 And SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15 | RWB-E2-009 |
| AC-EXC-P6-012-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-012-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-012-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.13 Give partners identities through the external gateway

#### A2.13.1 Intent

**Business objective.** Issues partner logins through the external gateway with multi-factor authentication, scoped to their own cases.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Issues partner logins through the external gateway with multi-factor authentication, scoped to their own cases.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and give partners identities through the external gateway | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** EAPI gateway, Partner portal

**Prerequisites.** FEAT-ACA-04

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-013-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P6-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Partner and agency manager, Collection agency (OA) user | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-013-01 | Partner sign-in | partner identity "P-5101" is in group "RWB-UAT-PT-LAWFIRM" and bound to "LF-0012" And 5 open instructions are placed with "LF-0012" and 3 with "LF-0019" | "P-5101" signs in through the external gateway with password and second factor | the session holds role "PT-LAWFIRM", scope "PLACED" and partner "LF-0012" And PRT-01 Partner home lists the 5 instructions of "LF-0012" and none of "LF-0019" And one entry with decision code "AC-SIGN" and actor "P-5101" is written | RWB-E2-019 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P6-013-01 | Role per partner | partner identity "P-5102" is in group "RWB-UAT-PT-VALUER" and bound to "VL-0004" And "VL-0004" holds 2 instructions of type "APPRAISE" and 1 of type "LIST" | "P-5102" signs in | PRT-01 Partner home lists the 2 "APPRAISE" instructions only | RWB-E2-019 |
| AC-ALT-P6-013-02 | Revoked | partner identity "P-5101" is bound to "LF-0012" And "LF-0012" moves to panel status "EXITED" at 11:00 on 4 January 2027 | "P-5101" tries to sign in at 11:20 | access is refused with message MSG-P4-008 And one entry with decision code "AC-DENY" and reason "PARTNER_NOT_ACTIVE" is written And a session of "P-5101" opened at 10:00 is ended at its first request after 11:05 | RWB-E2-019 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-013-01 | A partner identity with no binding is refused | partner identity "P-5103" is in group "RWB-UAT-PT-LAWFIRM" and has no active binding | "P-5103" signs in | the session is refused with status 401 and message MSG-P4-001 And one entry with decision code "AC-DENY" and reason "NO_PARTNER_BINDING" is written | RWB-E2-019 |
| AC-EXC-P6-013-02 | A partner without a second factor is refused | partner identity "P-5101" signs in with a token whose amr claim holds "pwd" only | the token reaches the Workbench | the session is refused with status 401 and message MSG-P4-005 | RWB-E2-019 |
| AC-EXC-P6-013-03 | An instruction of another firm is not returned | "P-5101" is signed in for "LF-0012" | "P-5101" requests instruction "INS-2027-000431" placed with "LF-0019" | the call returns status 404 with message MSG-P4-003 and no instruction data | RWB-E2-019 |
| AC-EXC-P6-013-04 | Two partner roles or a bank role are refused | partner identity "P-5104" is in groups "RWB-UAT-PT-LAWFIRM" and "RWB-UAT-PT-VALUER" | "P-5104" signs in | the session is refused with message MSG-P4-006 and an incident is raised to the security administrator queue | RWB-E2-019 |
| AC-EXC-P6-013-05 | A partner cannot reach bank screens | "P-5101" is signed in with role "PT-LAWFIRM", whose Queue and allocation letter is "-" | "P-5101" calls GET /queues | the call is refused with status 403 and message MSG-P4-002 | RWB-E2-019 |
| AC-EXC-P6-013-06 | A bank identity cannot use the external gateway | test user "U-5105" holds RW-LITOFF with a bank identity | "U-5105" signs in through the external gateway | the session is refused with message MSG-P4-001 And one entry with decision code "AC-DENY" and reason "BANK_IDENTITY_ON_PARTNER_ROUTE" is written | RWB-E2-019 |
| AC-EXC-P6-013-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-013-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-013-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.14 View the offer on LINE and web

#### A2.14.1 Intent

**Business objective.** Lets the customer see the offer the bank has made, on the channel they use.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Lets the customer see the offer the bank has made, on the channel they use.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Customer (borrower) | Opens the screen and view the offer on LINE and web | Checks the role, the capability area and the scope |
| 2 | Customer (borrower) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LINE OA, HOME.SCB

**Prerequisites.** FEAT-OCC-04

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-014-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-014-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Customer (borrower) | Primary |
| Case owner | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-014-01 | View the offer on LINE and web | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-014-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.15 Accept an offer in self-service

#### A2.15.1 Intent

**Business objective.** Lets the customer accept without a call or a branch visit, which records the acceptance on the case.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Lets the customer accept without a call or a branch visit, which records the acceptance on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Customer (borrower) | Opens the screen and accept an offer in self-service | Checks the role, the capability area and the scope |
| 2 | Customer (borrower) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LINE OA, HOME.SCB

**Prerequisites.** FEAT-COM-01

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-015-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-015-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Customer (borrower) | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-015-01 | Accept an offer in self-service | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-015-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.16 Pay in self-service

#### A2.16.1 Intent

**Business objective.** Lets the customer pay against the plan or the settlement from the same screen.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Lets the customer pay against the plan or the settlement from the same screen.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Customer (borrower) | Opens the screen and pay in self-service | Checks the role, the capability area and the scope |
| 2 | Customer (borrower) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** HOME.SCB, payments

**Prerequisites.** FEAT-COM-01

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-016-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-016-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Customer (borrower) | Primary |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-016-01 | Pay in self-service | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-016-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.17 Raise a dispute in self-service

#### A2.17.1 Intent

**Business objective.** Lets the customer raise a dispute, which opens X1 and applies the contact stop.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Lets the customer raise a dispute, which opens X1 and applies the contact stop.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Customer (borrower) | Opens the screen and raise a dispute in self-service | Checks the role, the capability area and the scope |
| 2 | Customer (borrower) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LINE OA, HOME.SCB

**Prerequisites.** FEAT-DVH-05

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-017-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-017-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Customer (borrower) | Primary |
| Complaint officer | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-017-01 | Raise a dispute in self-service | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-017-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.18 Maintain the contact repository

#### A2.18.1 Intent

**Business objective.** Keeps the verified contact points for every party, with consent state per channel.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Keeps the verified contact points for every party, with consent state per channel.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and maintain the contact repository | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-RDF-04

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-018-1 | Contact attempted while a contact stop is in force | MSG-P6-001 Contact with this customer is stopped for {reason}. |
| VR-P6-018-2 | Message to a channel without consent | MSG-P6-002 The customer has not consented to {channel}. Use another channel. |
| BR-P6-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Case owner | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-018-01 | Maintain the contact repository | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-018-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.19 Record a custody movement of a document

#### A2.19.1 Intent

**Business objective.** Tracks a physical document leaving and returning, so the original is never lost.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Tracks a physical document leaving and returning, so the original is never lost.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record a custody movement of a document | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-19

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-019-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Legal counsel | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-019-01 | Record a custody movement of a document | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-019-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-019-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-019-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.20 Answer a legal or audit document request

#### A2.20.1 Intent

**Business objective.** Returns the documents and the index entries a legal or audit request asks for.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Returns the documents and the index entries a legal or audit request asks for.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Legal counsel | Opens the screen and answer a legal or audit document request | Checks the role, the capability area and the scope |
| 2 | Legal counsel | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-DCM-06

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-020-1 | Template withdrawn (R-LIT-04) | MSG-P6-003 The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| BR-P6-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| notice.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| notice.document_id | The generated notice | uuid | No | None | No |
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | No |
| notice.sent_date | Date sent | date | No | None | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | No |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| Legal counsel | Primary |
| Internal audit, Compliance and PDPA officer | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-020-01 | Answer a legal or audit document request | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-020-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-020-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-020-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

### A2.21 Apply retention on case closure

#### A2.21.1 Intent

**Business objective.** Applies the retention class to every document on the case when the case closes.

**Problem.** Letters and notices are prepared by hand; proof of delivery is chased by phone.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Notices with proof of delivery | 100 percent | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Applies the retention class to every document on the case when the case closes.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply retention on case closure | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub, Blob storage

**Prerequisites.** FEAT-DCM-17

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P6-021-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P6-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P6-021-01 | Apply retention on case closure | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P6-021-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P6-021-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P6-021-01 | WIN outbound notices | Schedule | Daily 16:00 | Writes approved notices to WIN | Notices dispatched the same day | Notice periods start on time |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-OCC-001 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying. | Must | E1 |
| REQ-OCC-002 | Letter templates are versioned, and the Legal approval is recorded against the version. | Must | E1 |
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case. | Must | E2 |
| REQ-OCC-004 | Messages are sent by SMS and LINE through the bank's channel platforms, with the result recorded on the case. | Must | E2 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result, and a contact that fails the check is held. | Must | E2 |
| REQ-OCC-006 | A customer who withdraws consent for a channel stops receiving on that channel, and statutory notices continue. | Must | E2 |
| REQ-OCC-007 | The case record view shows account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions on one screen. | Must | E1 |
| REQ-OCC-008 | The case record view carries a history timeline showing every state change, transfer, contact, document and decision in order. | Must | E2 |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it. | Must | E2 |
| REQ-OCC-010 | A new verified contact point updates the contact data and clears a lost contact deviation. | Must | E2 |
| REQ-OCC-011 | Customer self-service for an offer, a signature, a payment and a dispute is available on the bank's digital channels. | Should | E4 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-33 Template approval | Letter and notice templates and their approval | E2 |

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
| Demand notice | หนังสือบอกกล่าวทวงถาม | A notice demanding payment before legal action |
| Recall notice | หนังสือบอกเลิกสัญญา | A notice ending the loan and calling the full balance |
| Proof of delivery | หลักฐานการส่งหนังสือ | Evidence that a registered notice reached the party |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
