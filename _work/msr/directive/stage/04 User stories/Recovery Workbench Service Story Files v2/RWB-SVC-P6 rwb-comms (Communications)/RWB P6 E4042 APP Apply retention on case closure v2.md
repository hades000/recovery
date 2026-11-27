# RWB-P6-E4042-APP Apply retention on case closure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P6-Z |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P6-E4042-APP-16) |
| Depends on (build) | RWB-P6-E4042-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P5-AD021-CON (nearest published baseline for the rwb-document retention-class read; its C row is added when P5 publishes the operation) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-042 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E4042-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 11 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer (RW-COMPLY)**, I want **the Workbench to check, when a case of rwb-comms closes, that every notice document of that case carries a retention class on the contract of the document hub, to record the coverage as a decision under the rule version in force, and, where a class is missing, to hold the closure and ask for the Document Hub task**, so that **a case never closes with a notice that has no retention class, and the class, its period and the disposal of the record stay the reference data of their owner and are never set by the communications service**.

### 2. Business rationale

A case that closes with a document that has no retention class cannot be disposed of or extended on the record, and a disposal that is not a recorded decision is the defect that REQ-DCM-019 and NFR-074 exist to prevent. The closure rules already state the gate: R-WO-47 closes the case when the retention timer expires and every document carries a retention class, and R-WO-48 holds the closure and raises a Document Hub task with five working days for a document with no class. The retention classes themselves are defined per document type with the periods not set (NFR-028, DL26), and the class, its period, the disposal or extension decision and the JOB-17 retention run all belong to rwb-document (Architecture v5 slides 16, 41 and 44; Ownership Map: `retention_rule`, `retention_action`, `document`, `document_type`, `case_document_check` all P5).

The communications service is therefore not the owner of retention: it is the owner of the notice, and the notice is what points at a document (`notice.document_id`, DF-LEG-017). This story is that slice. On the closure fact it reads the retention class of every notice document through the P5 contract, records the coverage through the local decision-record library with decision code D9 and rule R-WO-47 or R-WO-48 and the rule version in force, asks rwb-case for the hold and the Document Hub task where a class is absent, and serves the coverage on its own read so that the officer and the auditor can see it. It sets no class, holds no period, disposes of nothing and schedules nothing.

The legacy story is a thin auto-generated entry: module P6, FEAT-COM-08, depends FEAT-DCM-17, screen SCR-33, two criteria and four test cases. The decoupling of the target is the one this story applies: the notice rows are `rwb_comms` rows (DP-01); the coverage decision goes through the local library and the shared topic (DP-03); the base is `/api/recovery/comms/v1` (DP-13); and the coverage reaches the case record through the gateway-bff composite route (DP-19). DP-10 is deliberately absent: the trigger is the consumed `rwb.case.CaseStateChanged.v1` event and not a Temporal Schedule, and the only retention run in the catalogue is JOB-17, a Schedule of rwb-document. It serves REQ-DCM-010 and the closure gate portion of REQ-DCM-019, and it gives the FSD P6 A2.21 measure "notices with proof of delivery, 100 percent" its compliance-side evidence at closure.

### 3. Preconditions

- RWB-P6-E4042-CON is published: the coverage read on base `/api/recovery/comms/v1`, the consumed event element, the class-present vocabulary, the case-hold fact, the nine contract tables and the fakes, so this story builds against a fixed contract on Day 1.
- The `rwb_comms` baseline is in place from RWB-P6-E1046-APP and RWB-P6-E1052-APP: `notice`, `template`, `merge_field` and the per-service Flyway sequence exist, and `notice` carries `id`, `case_id`, `document_id` and `notice_type` (DF-LEG-015 to DF-LEG-018).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with RWB-PLT-E1027-CON (DP-03), and a failed write blocks the step (Principle 5, R-UNI-39).
- The gateway-bff composite route is live with RWB-PLT-N001-CON (DP-19) for the case record documents panel that shows the coverage.
- The rwb-document contract publishes a read of the retention class of a document. No such operation is named in any source and the plan declares no C row on a P5 contract for this key: the class, its list and the per-type mapping are P5 reference data and the read is Not specified in the source documents (GAP-1141; ASM-2088). The story is built against the rwb-document fake until that row exists.
- The rwb-case contract accepts the closing fact, the hold of the closure and the Document Hub task with the reason code RETENTION_CLASS_MISSING of R-WO-48. The operation, its body and the message a missing class shows are Not specified in the source documents (GAP-1143; ASM-2090).
- The closing state of a case is `CASE_CLOSED` as R-WO-47 names it; the other states that mean a case closes are the vocabulary of rwb-case and are read as data of their owner (GAP-1145; ASM-2092).
- The retention class list, the class per document type and the periods are unset in the sources (NFR-028, DL26) and are not this service's data; this story only needs presence or absence of a class per notice document (GAP-1144; ASM-2091).
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline of this key and two platform contract stories, and the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. rwb-case closes a case under R-WO-47 and publishes `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` with `caseId`, `fromState`, `toState` `CASE_CLOSED` and `changedAt`.
2. The event listener of this service dedupes the delivery by the CloudEvents id and starts the coverage check for the case.
3. The check reads the notice rows of the case (`id`, `case_id`, `document_id`, `notice_type`) from `rwb_comms`, and for each notice with a `document_id` it reads the retention class of that document on the rwb-document contract, one hop, one document at a time, with no table read of `rwb_document`.
4. If every notice document answers a class, the check records one decision through the local decision-record library: decision code D9, rule R-WO-47, the rule version in force, the case, the number of notice documents checked, and the result COVERED. The case is not held and needs nothing from this service.
5. If at least one notice document answers no class, the check records the decision with decision code D9, rule R-WO-48 and the same rule version, naming the notice and the document with no class, and sends one fact to rwb-case with the reason code RETENTION_CLASS_MISSING: closure is held and the Document Hub task with its five working days is raised by rwb-case, which owns the task and the timer (R-WO-48).
6. If the decision record cannot be written, nothing proceeds: no hold is asked, the case fact is not sent, the check is failed and an incident is raised under R-UNI-39, and the answer to the officer and the run record show MSG-P7-003.
7. An officer or an auditor reads the coverage with `GET /api/recovery/comms/v1/cases/{caseId}/retention-coverage` and the case record documents panel shows, for every notice document of the case, its notice type, its document reference and whether a class is present. The read computes the coverage on the contract of the owner at the moment it is called; it never returns a class value it did not receive from rwb-document.
8. When a later `CaseStateChanged` for the same case arrives and every notice document now answers a class, the check records the covered decision under R-WO-47 again; the earlier missing-class decision and its hold remain in the decision history, and no decision is overwritten.
9. A read of a case outside the caller's scope answers 404, and a read by a role without the Documents right answers 403 with MSG-P4-002.
10. A delivery of the same event with the same CloudEvents id is ignored, and a second run for the same case and the same closing state writes no second decision for the same document set.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A notice document of the closing case answers no retention class | Closure held; one decision under R-WO-48; the case fact with RETENTION_CLASS_MISSING is sent and rwb-case raises the Document Hub task | Not specified in the source documents (GAP-1143; ASM-2090) | AC1 |
| X2 | The rwb-document contract does not answer inside its budget, or answers an error | No class is assumed present and no covered decision is written; the check fails and is retried on the next delivery and the next closure event | None | AC1 |
| X3 | The decision record cannot be written | Nothing changes: no hold is asked, the fact is not sent, the incident is raised | MSG-P7-003 | AC2 |
| X4 | The closing case has no notice document | The coverage is an empty list and the decision records the case with no notice document; no hold is asked | None | AC1 |
| X5 | The same event is delivered twice, or the same case and closing state are checked twice | The second delivery is ignored by the CloudEvents id and no second decision is written for the same document set | None | AC1 |
| X6 | The caller holds no Documents right | Refused, nothing is returned | MSG-P4-002 | AC1 |
| X7 | The case is outside the caller's scope | Not found | The scope refusal envelope of the gateway-bff route | AC1 |

X2, X6 and X7 are the refusals of the read and of the check; they carry no new business rule. X1 is the only outcome of this story that asks another service to act.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4042-CON and the two platform contracts only; the document class read, the case fact and the decision library are fakes from the first run |
| Negotiable | The closing state, the class list, the class per document type and the five working days of the task are data of their owners; the story fixes the order of the check, the decision code D9 and the class-present vocabulary |
| Valuable | A case cannot close with a notice document that has no retention class, and the coverage is a recorded decision with its rule version |
| Estimable | One read, one event listener, one coverage service, two adapters and one decision path |
| Small | Fits one sprint with its tests, as the app slice of a thin legacy key |
| Testable | Each criterion of section 7 runs against the fakes; the coverage read is asserted field by field |

### 7. Acceptance criteria

```gherkin
Feature: Apply retention on case closure — the rwb-comms slice

  Background:
    Given the closing state of a case is "CASE_CLOSED"
    Given case "RC-2026-000412" has notice "N-0101" with document "DOC-0101" and notice "N-0102" with document "DOC-0102"

  Scenario: AC1 Apply retention on case closure (legacy RWB-E4-042 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns case "RC-2026-000412" closing with toState "CASE_CLOSED" and accepts the fact with reason "RETENTION_CLASS_MISSING"
    Given the rwb-document contract mock returns a retention class for document "DOC-0101" and a retention class for document "DOC-0102"
    When its trigger arrives
    Then applies the retention class to every document on the case when the case closes
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-042 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Each rule of section 8 without a criterion is covered by a test or a guardrail (new, D-RCV-60)
    Given the rules BR2, BR3, BR4, BR6 to BR12 of section 8 are in force
    When the story is built and its tests are listed
    Then each of these rules has a test case in section 16 or a guardrail or boundary test

  Scenario: AC4 A provided operation answers an error with status 401, 403 or 404 as the contract states (new, D-RCV-60)
    Given a provided operation of section 12 is called with no valid credential, without the right to the case, or for a resource that does not exist
    When the call is answered
    Then the answer carries the error status 401, 403 or 404 that the contract RWB-P6-E4042-CON names for that error

  Scenario: AC5 A redelivered rwb.case.CaseStateChanged.v1 event is handled as the contract states (new, D-RCV-60)
    Given the consumed event rwb.case.CaseStateChanged.v1 for case RC-2026-000412 has been handled once
    When the same event is delivered again
    Then the behaviour on the redelivered event is Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC5)

  Scenario: AC6 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call to the rwb-case or rwb-document contract fails or gives no answer
    When the step that needs the answer runs
    Then the outcome is Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC6)

  Scenario: AC7 A status change the model does not allow is refused (new, D-RCV-60)
    Given case RC-2026-000412 is in a state from which the requested change is not allowed by the model of its owner
    When the status change is sent
    Then the change is refused and the refusal is Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC7)
```

The two criteria above are the criteria of RWB-E4-042 copied line for line, with the origin tag on each scenario line and one mock line for each fact of another owner that the criterion names: the closure and the case fact on the rwb-case contract, and the retention class on the rwb-document contract. No legacy line and no legacy value is dropped. The target reading of "applies the retention class" is the one section 8 fixes in BR1 to BR5: the class and its period are P5 reference data, so this service checks that the class is present on every notice document and records the coverage; it never sets, changes or holds a class. The legacy gherkin uses no path, so no path of the legacy story is carried here and the base of this service is `/api/recovery/comms/v1` (DP-13).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case closes when the retention timer expires and no placement, sale or exception is open and a retention class is on every document; the closing state is `CASE_CLOSED` | R-WO-47 |
| BR2 | A document on the case with no retention class holds the closure and raises a Document Hub task with five working days | R-WO-48 |
| BR3 | Every document carries a retention class, and the class sets how long the document is kept; the classes are defined per document type and the periods are not set | REQ-DCM-010; NFR-028; DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) |
| BR4 | Retention runs by class, and a document at the end of its period is disposed of or extended by a recorded decision and never silently; the disposal or extension decision is P5's | REQ-DCM-019; NFR-074 |
| BR5 | The retention class, its list, the class per document type and the period are reference data of rwb-document; this service reads the class and never sets, defaults, maps or validates it | NFR-028; Ownership Map (`retention_rule`, `retention_action` P5); Architecture v5 slide 41 |
| BR6 | A legal hold overrides the retention class and stops every automated decision; a case under a hold is not presented for closure by rwb-case, and this service reads no hold of its own | REQ-DCM-016; R-UNI-20 |
| BR7 | The coverage is recorded through the local decision-record library with decision code D9, rule R-WO-47 or R-WO-48 and the rule version in force; a write that fails blocks the step and raises an incident | Principle 5; DP-03; R-UNI-39 |
| BR8 | The notice rows are `rwb_comms` rows; `retention_rule`, `retention_action`, `document`, `document_type` and `case_document_check` are P5's and are read on the owner's contract, never as tables | DP-01; Ownership Map |
| BR9 | The trigger is the consumed `rwb.case.CaseStateChanged.v1`; this story declares no workflow and no Schedule, and the only retention run is JOB-17 of rwb-document | Architecture v5 slides 42 and 44; Template and Rules §R5.5 (DP-10 not applied) |
| BR10 | The hold of the closure and the Document Hub task are rwb-case's; this service sends the fact with the reason code `RETENTION_CLASS_MISSING` and owns neither the task nor its timer | R-WO-48; Ownership Map (`task`, `timer` P3) |
| BR11 | The coverage reaches the case record documents panel through the gateway-bff composite route; this service serves the read and the panel belongs to its owner | DP-19; Template and Rules §R7.2 s15 |
| BR12 | No value a business person may change is written in code: the closing state, the class list and the task timer are data of their owners, read with the version in force | FSD P6 A2.21 BR-P6-021 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not checked | `rwb.case.CaseStateChanged.v1` with `toState` `CASE_CLOSED` for the case | The event is new and the case has notice rows | Checking |
| Checking | The rwb-document contract answers a class for every notice document | At least one notice document, or none to check | Covered: one decision under R-WO-47, no hold |
| Checking | The rwb-document contract answers no class for at least one notice document | R-WO-48 | Class missing: one decision under R-WO-48, the hold and the Document Hub task are asked of rwb-case |
| Checking | The decision record cannot be written | R-UNI-39 | Not checked: nothing is held and the incident is raised |
| Class missing | A later closure event for the case arrives and every notice document now answers a class | P5 applied the class | Covered: a new decision under R-WO-47; the earlier decision stays in the history |

The case state (RETENTION_RUNNING to CASE_CLOSED) is rwb-case's under R-WO-47 and is not state of this service; the four states above are states of the coverage check of one case and are recorded in the decision history, not in a table of the service. A notice with no `document_id` has no document to check and enters the coverage list as absent with no class, so that the panel never hides a notice.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Documents RU in the matrix of TSD P6 T6.1: reads the coverage of a case and its decisions |
| RW-LITOFF, litigation officer | Documents CRUA in TSD P6 T6.1: reads the coverage of the notices he owns |
| RW-LEGAL, legal counsel | Documents CRUA in TSD P6 T6.1: reads the coverage for a legal or an audit answer |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: reads the coverage and its decisions |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the coverage and operates the check through the run records |
| rwb-comms service identity | Consumes the event, reads its own `notice` rows, calls the two consumed rows and writes the local decision record (DP-02) |
| Decision-record library identity | Writes the coverage decision and relays it on `rwb.decision-record.v1` (DP-03) |

The FSD A2.21 names the primary actor as "None; runs unattended" and the Compliance and PDPA officer as the second actor; the matrix above is the only source used for the rights, and the capability area of the read is fixed by RWB-P6-E4042-CON (GAP-1142; ASM-2089). The authorise contract of rwb-access (DP-08) is not in this story's pattern set: the capability area and the right of the read are declared in the contract story and enforced at gateway-bff.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | `notice` in `rwb_comms` | id | Read, as the entry key of the coverage |
| DF-LEG-016 | `notice` in `rwb_comms` | case_id | Read, as the selection of the case |
| DF-LEG-017 | `notice` in `rwb_comms` | document_id | Read, as the document whose class is checked |
| DF-LEG-018 | `notice` in `rwb_comms` | notice_type | Read, for the coverage entry |
| DF-LEG-021, DF-LEG-022 | `notice` in `rwb_comms` | callback_date, delivery_status | Read only, to show a delivered notice beside its coverage; never written here |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code D9, rule R-WO-47 or R-WO-48, rule version, case, notice, decided at, hash chain | Write |
| DF-DOC-001 to DF-DOC-011 | `document`, through the rwb-document contract | id, document_type, the retention class and its presence | Read through the contract, never a table |
| DF-CAS-001 to DF-CAS-023 | `recovery_case`, through the rwb-case contract | id, status and the closing state | Read through the contract, never a table |
| The retention class and its period | `retention_rule`, `retention_action`, owned by P5 rwb-document | class code and period | Not read and not written: the class fact arrives on the owner's contract and this service stores neither |

No column is added to `rwb_comms` by this story and no table is created: the coverage of a case is a projection of its `notice` rows and of the class fact of the owner's contract at the moment of the read, and its result is the decision record. The read uses the index `ix_notice_case_id` on `notice (case_id)` of RWB-P6-E2021-APP, so no migration is needed (DP-15, ADR-021). No personal data is written or returned: the coverage carries notice IDs, a case ID, document IDs, a notice type and a boolean, and no name, address, identity number or account number. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shape is the one fixed in RWB-P6-E4042-CON at contract version Not specified in the source documents (DOR-RWB-P6-E4042-APP-23); this story implements it and adds no path.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/retention-coverage` | Read the retention coverage of the notice documents of a case: one entry per notice document with `noticeId`, `caseId`, `documentId`, `noticeType` and `classPresent`, 200 | Documents, right R, scope applied | Not applicable |

The operation is fixed by this baseline because no source names a retention operation of this service: the TSD P6 endpoint inventory stops at API-P6-011 and carries no retention path, and the legacy story names only the notice request and the notice read (GAP-1142; ASM-2089). Errors: 401 no session (Not specified in the source documents (CG-ALL-6784)); 403 the role lacks the Documents right (MSG-P4-002); 404 the case is absent or out of scope (Not specified in the source documents (CG-ALL-6784)); 503 the class read of the owner is unavailable (Not specified in the source documents (CG-ALL-6784)). The exact field types and the page shape are fixed in the contract story and are Not specified in the source documents (GAP-1142; ASM-2089).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | the retention class read of a document on the rwb-document contract | P5 rwb-document | The class present or absent for each notice document of the case; faked. The plan declares no C row for this contract and no P5 operation names the class read, so the path is Not specified in the source documents (GAP-1141; ASM-2088) |
| POST | the case fact that holds the closure and asks for the Document Hub task with reason `RETENTION_CLASS_MISSING` | P3 rwb-case | The hold and the task of R-WO-48, which rwb-case owns; faked. The operation, its body and the message of a missing class are Not specified in the source documents (GAP-1143; ASM-2090) |

Each row is one hop on the owner's published contract, read or written inside the same step that writes the decision, and a missing or late answer never counts as a class present. No row reads a table and no row reads a view of another service (DP-01).

#### 12.3 Events published

None. The event catalogue carries no retention event and this service announces no retention action of its own; the decision record is relayed on the shared `rwb.decision-record.v1` by the local library (DP-03), and JOB-17 and any retention outcome remain rwb-document's (Architecture v5 slide 44).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | The trigger of the check: `caseId`, `fromState`, `toState`, `changedAt`; a `toState` equal to the closing state `CASE_CLOSED` starts the coverage check of that case. Deduped by the CloudEvents id. The event catalogue names rwb-comms as a consumer of EV-05 |

The event carries IDs, state codes and a timestamp only. This story reads no other event and no event of this story is published to keep the local picture current: the coverage is computed from the live answers of its owners at the moment it is asked.

#### 12.5 Workflows and activities

None. The trigger is the consumed event and the check is one listener step in this service; no workflow, no activity and no Temporal element is declared, because DP-10 is not in the pattern set of this legacy key and the only retention run of the catalogue is JOB-17, a Schedule of rwb-document.

#### 12.6 Schedules

None. The retention run is JOB-17 of rwb-document on its own Schedule (Architecture v5 slides 16 and 44; Ownership Map: JOB-17 owner P5), and this story neither registers a Schedule nor reads a job table.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | Read for the notice documents of the case; written by RWB-P6-E1052-APP and RWB-P6-E2021-APP |
| template, merge_field | P6 (rwb_comms) | Read only, for the notice type and the template provenance of a coverage entry |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The coverage decisions of this story (DP-03) |

Not owned and never read: `retention_rule`, `retention_action`, `document`, `document_type` and `case_document_check` (P5), `recovery_case`, `task` and `timer` (P3), `decision_log_entry` (P7), `interaction` (P1), `outbound_item` and `interface_config` (P2). No table of this service carries a retention class, a period or a disposal, and no foreign key crosses a service boundary (DP-01, BR5).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-document fake | The retention class read | A class for `DOC-0101` and `DOC-0102`; no class for `DOC-0102`; a document absent; an answer beyond the budget; the answer is derived from the published document and carries the placeholder of the class list (GAP-1141; ASM-2088) |
| rwb-case fake | The closing event and the hold with the Document Hub task | `CaseStateChanged` with `toState` `CASE_CLOSED` for `RC-2026-000412`; a repeat delivery with the same CloudEvents id; an accepted fact with reason `RETENTION_CLASS_MISSING`; a refused fact; a case with no notice document |
| Decision-record library stub | The coverage decision | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-042-02 |

The fakes are derived from RWB-P6-E4042-CON, and the drift test of that story fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | The coverage read provided; the class read of P5 and the case fact of P3 consumed; one hop each |
| Kafka | None published, 1 consumed | `rwb.case.CaseStateChanged.v1` consumed as the trigger |
| Temporal | None | No workflow, no activity, no Schedule: the trigger is the event |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `retention`, Java package `th.co.scb.ace.workbench.recovery.comms.retention`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is applied as a prohibition and adds no dependency: this service reads no table of the rwb-document service, and the class arrives on the owner's contract (BR8). DP-10 is not applied: the trigger is the consumed event, there is no Schedule and no Quartz row, and JOB-17 stays rwb-document's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RetentionCoverageController | Controller | `GET /cases/{caseId}/retention-coverage` with the Documents right, the scope test and the problem mapping for 401, 403, 404 and 503 |
| CaseStateListener | Listener | Consumes `rwb.case.CaseStateChanged.v1`, dedupes by the CloudEvents id, filters on the closing state and starts the check |
| RetentionCoverageService | Service | Builds the coverage of a case from its `notice` rows plus the class fact of the owner, one document at a time, and answers present or absent per entry |
| ClosureCheck | Service | The ordered step of section 4: coverage, decision, case fact; fails closed on any missing answer |
| DocumentRetentionClient | Adapter | The retention class read on the rwb-document contract, one hop, with a breaker and no default class |
| CaseFactClient | Adapter | The hold of the closure and the Document Hub task with reason `RETENTION_CLASS_MISSING` on the rwb-case contract |
| CoverageDecision | Service | Writes the local decision record with decision code D9, the rule and its version through the library |

**Database and migrations**

- Reads `notice`, `template` and `merge_field`; writes the local decision record; all in schema `rwb_comms`. No table and no column is added and no migration is needed; the read uses `ix_notice_case_id` of RWB-P6-E2021-APP.
- No retention class, period or disposal is stored in `rwb_comms`, and no copy of `retention_rule` or `retention_action` is created (BR5).

**Configuration and reference data**

- The closing state of a case is `CASE_CLOSED` as R-WO-47 names it, held as a parameter and never in code; the other closing states are the vocabulary of rwb-case and are read as data of their owner (GAP-1145; ASM-2092). The parameter key is Not specified in the source documents (DOR-RWB-P6-E4042-APP-20); the patterns that govern it are DP-06 and DP-07.
- The reason code of the missing class is `RETENTION_CLASS_MISSING` of R-WO-48, and the five working days of the Document Hub task are the timer of rwb-case, not a value of this service.
- The retention classes and the periods are not configured here at all: they are P5 reference data and unset in the sources (NFR-028, DL26 with ASM-0247, ASM-0264, ASM-0275, ASM-0355; GAP-1144; ASM-2091).
- The feature switch `rwb.comms.retention-closure-check`, read as a parameter: when it is off the check writes no decision and holds the closure, because a class is never assumed present.

**Build steps**

1. RetentionCoverageController and CaseStateListener over the one read and the one consumed event, with the dedupe and the closing-state filter; tests for the empty case and the repeat delivery.
2. DocumentRetentionClient and the coverage service: one document at a time, no default class, a failed or late answer fails the step; tests for presence, absence and an absent document.
3. CoverageDecision and the fail-closed path: a failed write leaves nothing held and raises the incident; test for AC2 and TC-E4-042-02.
4. CaseFactClient and the missing-class path with reason `RETENTION_CLASS_MISSING`, behind the fake until the rwb-case row is published.
5. The closure step of section 4 end to end against the three fakes, and the covered decision under R-WO-47 for the all-present case; test for AC1 and TC-E4-042-01.
6. The contract-fake run of the whole check before the real services are live, and the drift test of RWB-P6-E4042-CON in the pipeline.

**Feature switch.** `rwb.comms.retention-closure-check`, read as a parameter; off writes no decision and holds the closure.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4042-CON stay green, and a SIT week shows every closing case of the service with one coverage decision and its rule version, every missing class with a hold and a Document Hub task under R-WO-48, no case held without a missing class, and no retention class, period or disposal value written by this service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |

The message a missing class shows to the officer and the message a refused case fact returns are Not specified in the source documents (GAP-1143; ASM-2090), because R-WO-48 names the hold and the task and no source names a message ID for either.

MSG-P7-003 and MSG-P4-002 are copied unchanged from the legacy story. The legacy table also carries MSG-P6-003, MSG-P6-004, MSG-P6-001 and MSG-GEN-001: those belong to the notice and dispatch capabilities of the same module (RWB-P6-E1052-APP, RWB-P6-E2021-APP) and are not used by this story. The check runs unattended, so the missing-class outcome is shown to a person only through the coverage read and through the Document Hub task of rwb-case, and both texts are fixed in the RWB-P6-E4042-CON review.

### 15. Screens and states

The legacy story names SCR-33 Template approval, which is the template screen of the same module and does not fit an unattended retention check (GAP-1145; ASM-2092). The coverage is shown on the case record documents panel of the case record view, served through the gateway-bff composite route (DP-19), where each notice document of the case shows:

| Coverage state | What the user sees |
|---|---|
| Class present | The notice type, the document reference and the class the owner returned |
| Class absent | The notice type, the document reference and the fact that no class is present, with the Document Hub task of the case |
| Not checked | The case has no coverage decision yet, or the check failed; MSG-P7-003 where the decision could not be written |
| Covered after a missing class | The newer decision under R-WO-47 beside the earlier R-WO-48 decision in the case timeline |

The panel, its field list and its masking belong to the story that owns the case record view and to RWB-PLT-N001-CON; this story serves only the coverage read. SCR-33 keeps the template capability of its own module and is not used for the coverage; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-6788). SCR-44 Batch and job monitor shows nothing for this story because there is no run of this service; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-6789). The FSD background row AC-BG-P6-021-01 is a copy of AC-BG-P6-020-01 and belongs to the notice dispatch capability, not to a retention run; this story takes no such row (GAP-1145).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-042-01 | AC1 | End to end | Case `RC-2026-000412` closing with `N-0101`/`DOC-0101` and `N-0102`/`DOC-0102`; the rwb-document fake answers a class for both; the decision carries D9 and R-WO-47 with its version |
| TC-E4-042-02 | AC2 | End to end | The decision chain is forced to fail; no hold is asked, no fact is sent, MSG-P7-003 and the incident of R-UNI-39 |
| TC-E4-042-03 | Access | Component | RW-COMPLY reads the coverage of a case in scope; a role without the Documents right is refused with MSG-P4-002 |
| TC-E4-042-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 closing cases; no case is held and no fact is sent |
| TC-E4-042-05 | Section 12 contract | Contract | Each operation, event and activity of section 12 is checked against the contract RWB-P6-E4042-CON; the consumed event rwb.case.CaseStateChanged.v1 is checked for its shape |
| TC-E4-042-06 | Section 12.7 tables (ASM-3438) | Boundary | Each table of section 12.7 is read or written only as listed; no table not owned here is read and no retention class, period or disposal value is written to rwb_comms |
| TC-E4-042-07 | AC3 | Boundary | Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC3) |
| TC-E4-042-08 | AC4 | Contract | Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC4) |
| TC-E4-042-09 | AC5 | NFR | Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC5) |
| TC-E4-042-10 | AC6 | NFR | Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC6) |
| TC-E4-042-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P6-E4042-APP-AC7) |

The first four cases keep their legacy order, their legacy coverage and their legacy test intent; the legacy story states no level, so the levels above follow the mapping of the run (System to End to end, Access to Component, Resilience to NFR) and the Data column carries the synthetic values the tests need. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the closing state, the reason code, the task timer, the class list and the periods are data of their owners, read with the version in force; this service writes none of them in code and none of them in its schema.
- This service sets no retention class, no period and no disposal: the class, its list, the per-type mapping, `retention_rule`, `retention_action` and JOB-17 are P5 rwb-document's (BR5).
- No personal data in events, logs, workflow inputs, tests or prompts: notice IDs, case IDs, document IDs, notice types, rule IDs and timestamps only.
- No read of another service's tables and no view of this service: the class and the case state arrive on the owner's contract (DP-01).
- A class is never assumed present: a missing, refused or late answer of the owner fails the step and never produces a covered decision.
- A decision that cannot be written stops the check, holds nothing and raises the incident (Principle 5, R-UNI-39).
- The consumed event is deduped and the check is idempotent for one case and one closing state, so a repeated delivery writes no second decision for the same document set.
- One base, one topic, one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no other base, topic or queue is declared as this service's own (DP-13, DP-14).
- No Quartz row, no shared job table, no batch table and no second Schedule: the trigger is the event and the only retention run is JOB-17 of rwb-document.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class | Business Requirements Program, document and records management | FEAT-COM-08 | 13 Manage documents and correspondence | R-WO-47, R-WO-48 | TC-E4-042-01, TC-E4-042-03 |
| REQ-DCM-019 | Retention runs by class; a disposal or an extension is a recorded decision | Business Requirements Program, document and records management | FEAT-COM-08 | 13 Manage documents and correspondence | R-WO-47, R-WO-48 | TC-E4-042-01, TC-E4-042-04 |
| REQ-DCM-016 | A legal hold overrides the retention class and stops expiry | Business Requirements Program, document and records management | FEAT-DCM-17 | 16 Manage risk, control and compliance | R-UNI-20 | TC-E4-042-01 |
| NFR-028 | Retention classes are defined per document type; the periods are not set | Business Requirements Program, non-functional | FEAT-DCM-17 | 13 Manage documents and correspondence | R-WO-47 | TC-E4-042-01 |
| NFR-074 | A document at the end of its period is disposed of or extended by a recorded decision | Business Requirements Program, non-functional | FEAT-DCM-17 | 13 Manage documents and correspondence | R-WO-48 | TC-E4-042-02, TC-E4-042-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-042, disposition Split (rework) |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-042 AC1) and (legacy RWB-E4-042 AC2) |
| Test cases | TC-E4-042-01 to TC-E4-042-11; TC-E4-042-01 to TC-E4-042-04 in the legacy order, TC-E4-042-05 to TC-E4-042-11 added as the contract, boundary and AC3 to AC7 cases |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-019 (edge: gateway-bff), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-20, R-UNI-39, R-WO-47, R-WO-48 |

This story serves REQ-DCM-019 and NFR-074 only for the closure gate: the disposal or the extension decision of a document at the end of its period, and the periods themselves, are P5 rwb-document's work under FEAT-DCM-17 and are named in section 19.

### 19. Out of scope

- The retention class, its list, the class per document type, the periods and the disposal or extension decision: P5 rwb-document (`retention_rule`, `retention_action`, `document_type`). This story reads the class and sets nothing.
- The retention run JOB-17 and its Schedule: rwb-document (P5), per Architecture v5 slides 16 and 44 and the Ownership Map.
- The case status, the closing state, the hold of the closure, the Document Hub task and its five working-day timer: rwb-case (P3). This story sends the fact with reason `RETENTION_CLASS_MISSING`.
- A legal hold and its block on outbound action and automated decision (R-UNI-20, REQ-DCM-016): rwb-case with rwb-document. A case under a hold is not presented for closure.
- The document, its metadata, its custody and its content: rwb-document (P5). This story reads the class on the owner's contract.
- The central decision ledger: rwb-decision (P7). This story writes the local record through the library (DP-03).
- The case record documents panel and the case timeline: the stories that own the case record view, and RWB-PLT-N001-CON for the composite route.
- SCR-33 Template approval and the template capability: RWB-P6-E1034-APP and RWB-P6-AD017-APP.
- The contract document, the coverage answer shape and the fakes as published artefacts: RWB-P6-E4042-CON.
- The deployment, the dashboards, the alerts and the runbook of this capability: the plan declares no OPS story for this legacy key, so the check ships with the service release.
