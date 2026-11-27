# RWB-S2-E3003-CON Approve a settlement below the floor - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-003 for rwb-treatment. The contract is published on Day 1 and fixes the elements the treatment carries when a below-floor price is approved, the `rwb.treatment.TreatmentApproved.v1` envelope on `rwb.treatment.events.v1`, the rule that no table is created for the second signature, the compatibility rule and the fakes; the implementation is RWB-S2-E3003-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the below-floor approval — the elements the treatment carries when a settlement offer or a transfer price under the floor is approved (`approvalLevel`, `approverRole`, `finalCall`, `decidedAt`, `reasonCode`), the `rwb.treatment.TreatmentApproved.v1` envelope on `rwb.treatment.events.v1` with key `caseId` and identifiers and facts only, the rule that no new table is created for the second signature, the compatibility rule and the fakes — instead of the monolith's `decision_log_entry` row in the shared `recovery` schema and its in-process call to the approval routing**, so that **rwb-comms and rwb-payment can build against one frozen event on Day 1, RWB-S2-E3003-APP can build the below-floor branch of `TreatmentWorkflow` against one frozen element set, and no reader mistakes the approval outcome for a record of its own**.

### 2. Business rationale

The monolith kept the whole answer in one place: the S2 service compared the offer or the transfer price with `floor_price`, called the approval routing of FEAT-APD-01 in the same process, wrote one `decision_log_entry` row with the rule version, and set the treatment's `approval_level` in the same schema. Two consequences followed that the target cannot keep. The record existed once, centrally, so no service could announce a decision; and the second signature had no shape of its own, so any team adding it would have added a table.

Ten of the nineteen services now write their own decision record locally and announce it on `rwb.decision-record.v1` (DP-03), and the approval itself is the workflow kit's `ApprovalWorkflow` started as a child on rwb-decision's queue (Architecture v5 slide 18, "TMP  Decision: child: approval"). What is left for this contract is the part two other services depend on: what an approved below-floor price carries on the treatment, and what `TreatmentApproved` says to rwb-comms and rwb-payment. Architecture v5 slide 42 names the producer and the two consumers of that event (row 10) and fixes no payload, and the TSD lists DF-TRT-001 to DF-TRT-033 with `approval_level` as the only approval field and no reason-code list (TSD S2 T3.1 and T3.2). The element names and the payload are therefore the working read of ASM-3068, and the gap stays open (GAP-1872).

**The division of the legacy key is fixed.** This WP delivers the **contract**. The **implementation** — the below-floor branch of `TreatmentWorkflow`, its four activities and the child workflow call — is **RWB-S2-E3003-APP**, and the **cross-service proof** is the wave 2 integration harness. The four legacy acceptance criteria **stay with RWB-S2-E3003-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title.

The contract has to exist before the code for three reasons. rwb-comms and rwb-payment build in the same wave and cannot wait for a payload to appear: they need the type name, the key and the field list on Day 1. The element set is the only thing that stops a second table: a team that finds no field for the final call adds `treatment_approval` and the decision is then recorded twice, once as a row and once as a record, which is exactly what DP-03 forbids. And the compatibility rule is what lets rwb-comms and rwb-payment pin a version while the approval workflow of rwb-decision is still changing its own side: a new optional element is a minor change, and a removed or renamed element raises the major version and a new `ce_type`, never an edit in place.

The fake is the Day-1 unblocker: RWB-S2-E3003-APP builds and tests the approved and the refused answer before rwb-decision, rwb-access or rwb-comms exists, and the two consumers build their offer and payment steps against the same envelope.

### 3. Preconditions

- The treatment of the case is rwb-treatment's own object in schema `rwb_treatment` (Architecture v5 slide 41; Ownership Map row `treatment`, owner S2), and `approval_level` (DF-TRT-011, LOV-APPROVAL-LEVEL L1 to L6) is its only published approval field (TSD S2 T3.1 and T3.2).
- The approved treatment elements reuse the published names where they exist: `approvalLevel` is declared on the treatment representation of the API Specification v5, and `finalCall` is declared on its `DecisionRecord` schema; `approverRole`, `decidedAt` and `reasonCode` have no published element on the treatment, which is the gap this contract closes for the wave (GAP-1872; ASM-3068).
- The event is named and owned by the source documents: `TreatmentApproved`, producer rwb-treatment, topic `rwb.treatment.events.v1`, consumers rwb-comms and rwb-payment (Architecture v5 slide 42 row 10; slide 18 S2 OUT line), CloudEvents on Kafka with key `caseId` (slide 42 note).
- The rule that gives the approval its reason code is in force as data: R-SET-05 and R-DIL-15 route a price under the floor, and R-DIL-17 returns the case with reason `price_below_floor` (Business Rules and Routing Logic v4); the settlement's refusal reason is `below_floor_refused` (R-SET-08). The codes are reference values, never a list held by this contract (BR-S2-003).
- The delegation facts are not this contract's: the level and the limit are rwb-access's `delegation_limit` (Ownership Map row, owner P4), carried on the approval request the kit's `ApprovalWorkflow` builds (ASM-3068).
- The decision record is written through RWB-PLT-E1027-CON, whose `DecisionRecord` carries `approvalLevel` and `finalCall` and whose write refuses with MSG-P7-009 and fails with MSG-P7-003; this contract declares the record's use and not its shape (DP-03).
- The schema registry is in BACKWARD mode and the AsyncAPI document per service is the contract, so the event is registered against it (Architecture v5 slides 42 and 43 notes).
- The case status stays rwb-case's and reaches the stage on the case signal, so this contract declares no case status and no case event (ASM-3062).
- No build dependency and no approval stop: a CON story is Day 1 by rule and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element set of an approved below-floor price on the treatment: one existing element (`approvalLevel`) and four new ones (`approverRole`, `finalCall`, `decidedAt`, `reasonCode`), with their value domains and their "absent while the approval is open" rule.
2. The author fixes the no-new-table rule and states where each fact already lives: the treatment row, the library's `decision_record`, P7's `approval` and P4's `delegation_limit`.
3. The author writes the `TreatmentApproved` section: CloudEvents 1.0 binary mode, the attribute set, `ce_type` `rwb.treatment.TreatmentApproved.v1`, key `caseId`, the ten payload fields and the rule that the payload carries identifiers and facts only.
4. The author writes the compatibility rule: which change keeps major version 1, which raises major version 2 with a new `ce_type`, and how a consuming service pins a version.
5. The author writes the refusal rule: no event on a refusal, the reason code carried on the treatment, and the two decision-record exceptions that keep a refusal or an approval from taking effect.
6. The author writes the fake set: an element fake with an approved settlement and an approved deed in lieu, a refused answer, an envelope fake with a valid and an invalid body, and a consumer fake for rwb-comms and rwb-payment.
7. The lint step runs: the element names compared with the API Specification, the payload compared with the AsyncAPI document, and the example scanned for personal data.
8. The schema step runs: the envelope validated against the registry fake in BACKWARD mode, one accepted and one refused body.
9. The contract test runs the fakes against the document on every change and fails the build on any drift in this story and in RWB-S2-E3003-APP.
10. The document and the fakes are published at v1; RWB-S2-E3003-APP, rwb-comms and rwb-payment pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A team adds a `treatment_approval` table, or a second write path for the final call | The boundary and drift checks fail the build; the treatment row plus the decision record are the only places the outcome lives | None | AC1 |
| X2 | The event is published without the key `caseId`, or with a field outside the ten | The envelope validation fails the build | None | AC2, AC3 |
| X3 | A payload carries a personal field or free text | The personal-data scan fails the build; the payload carries identifiers and facts only | None | AC3 |
| X4 | An approval is refused and an event is still published | The contract test fails: a refusal publishes nothing and carries the reason code on the treatment | None | AC4 |
| X5 | The record cannot be written and the treatment is still updated | The `MANDATORY` rule and the drift test fail the build; the caller's transaction rolls back | MSG-P7-003 | AC4 |
| X6 | An element is renamed or removed | The change raises major version 2 and a new `ce_type`; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A value the consumers need is named by no source — the payload field list, the value domains of the four new elements, or the reason-code list | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1872; ASM-3068) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The value domains, the example values and the fixture set are open until v1 is frozen; the element names, the key, the ten payload fields and the no-new-table rule are fixed |
| Valuable | Unblocks RWB-S2-E3003-APP, rwb-comms and rwb-payment on Day 1 and keeps a second approval table out of the service plan |
| Estimable | One element set, one envelope, two rules, one fake set and one document |
| Small | One sprint for the document, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the below-floor approval contract of rwb-treatment

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the treatment of a case is owned by rwb-treatment in schema rwb_treatment
    Given the case status stays rwb-case's and reaches the stage on the case signal

  Scenario: AC1 The approved treatment carries the approval element and creates no new table (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated against the treatment representation and the TSD
    Then an approved below-floor price carries approvalLevel, approverRole, finalCall, decidedAt and reasonCode on the treatment row
    Then approvalLevel keeps the value domain L1 to L6 of LOV-APPROVAL-LEVEL and its published element name
    Then the four other elements are absent while an approval is open and present once it has decided
    Then the document declares that no table is created for the second signature, and names decision_record as the library object of DP-03, approval as P7's and delegation_limit as P4's
    Then a proposed treatment_approval table fails the boundary test

  Scenario: AC2 The TreatmentApproved envelope is fixed (new, D-RCV-60)
    Given the event section of the document
    When one approved settlement and one approved deed in lieu are validated against it
    Then the event is rwb.treatment.TreatmentApproved.v1 published on rwb.treatment.events.v1 in CloudEvents 1.0 binary mode with ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header
    Then the payload carries treatmentId, caseId, treatmentType, offerAmount, approvalLevel, approverRole, finalCall, decidedAt, ruleId and ruleVersion
    Then the topic is the service's own and the event name follows Template and Rules §R4
    Then the registry holds one accepted schema version and refuses a body that does not match it

  Scenario: AC3 The key is the case and the payload carries no personal data (new, D-RCV-60)
    Given the same envelope section
    When the key rule and the payload of the two examples are checked
    Then the record key is caseId and ce_subject is the same case identifier
    Then the payload carries identifiers, codes, amounts, levels and versions only
    Then the payload carries no name, no national identifier, no account number, no address, no document content and no free text
    Then the personal-data scan fails the build on any of them

  Scenario: AC4 A refusal is carried on the treatment and publishes nothing, and a failure to record stops the approval (new, D-RCV-60)
    Given the refusal section of the document
    When a refused second signature and a refused settlement approval are put through it
    Then the treatment carries the final call and the reason code in force, price_below_floor for the deed in lieu and below_floor_refused for the settlement
    Then no TreatmentApproved event is published and no outbox row is written
    Then the decision record is written through DecisionRecordWriter with propagation MANDATORY, and a failed write answers MSG-P7-003 and rolls the treatment back
    Then a refused field answers MSG-P7-009 with the field name and no event

  Scenario: AC5 A compatible change keeps major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element or to the payload
    Then an added optional element keeps major version 1 and the ce_type version, and is accepted by the registry in BACKWARD mode
    Then a renamed, removed or retyped element raises major version 2 and a new ce_type, and v1 is never edited in place
    Then rwb-comms, rwb-payment and RWB-S2-E3003-APP each pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test runs on both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake, the envelope fake and the two consumer fakes
    Then the element fake answers an approved settlement at L6 under DOA-2026.11, an approved deed in lieu, a refusal with its reason code and a treatment with no decision
    Then the envelope fake answers one valid and one invalid TreatmentApproved body for the registry
    Then the consumer fakes of rwb-comms and rwb-payment accept the approved body and refuse a body with no key
    Then the drift test fails on any difference from sections 12 and 13 in this story and in RWB-S2-E3003-APP
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-003 stay with RWB-S2-E3003-APP** — and every identifier comes from the legacy story, the API Specification, the TSD, Architecture v5 or the Temporal and Drools Design, character for character. The value domains of `approverRole`, `decidedAt` and `reasonCode`, and the event payload beyond the fields listed, are the working read of ASM-3068 (GAP-1872).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An approved below-floor price is carried on the treatment row as `approvalLevel`, `approverRole`, `finalCall`, `decidedAt` and `reasonCode`, and no table is created for the second signature | GAP-1872; ASM-3068; TSD S2 T3.1 |
| BR2 | `approvalLevel` keeps the L1 to L6 domain of LOV-APPROVAL-LEVEL and is a level in force, never a constant | TSD S2 T3.2; DF-TRT-011; BR-S2-003 |
| BR3 | `TreatmentApproved` is published once per approved treatment on the service's own topic, in CloudEvents 1.0 binary mode, with key `caseId` | Architecture v5 slide 42 row 10; slide 42 note; Template and Rules §R4 |
| BR4 | The payload carries identifiers and facts only, and the ten fields of section 12.3; it carries no personal data and no free text | Architecture v5 slide 42 note; NFR-054 |
| BR5 | A refusal publishes nothing and is carried on the treatment with the reason code in force: `price_below_floor` for the deed in lieu, `below_floor_refused` for the settlement | R-DIL-17; R-SET-07; R-SET-08; BR-S2-003 |
| BR6 | The approval is recorded through DecisionRecordWriter with propagation MANDATORY, refusing with MSG-P7-009 and failing with MSG-P7-003, so a record that cannot be written stops the approval | DP-03; R-UNI-39; RWB-PLT-E1027-CON |
| BR7 | The approval record `approval` is P7's and the delegation facts are P4's: this contract names them and declares no field, no read and no write of either | DP-01; Ownership Map rows `approval` and `delegation_limit` |
| BR8 | The case status is rwb-case's: this contract declares no status value and no case event | ASM-3062 |
| BR9 | A published version is never edited: a backward-compatible change keeps major version 1, a breaking change raises major version 2 with a new `ce_type`, and every consumer pins a version | Template and Rules §R7.2; Architecture v5 slides 42 and 43 notes |

### 9. State transitions

None in this story: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3003-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Treatment approval element | Absent | No below-floor approval has been requested; the treatment carries no level and no final call |
| Treatment approval element | Open | An approval is with the level the matrix names; the four outcome elements are empty and `approvalLevel` may already name the level that is deciding |
| Treatment approval element | Decided | The final call, the approver role, the decided-at time and the reason code are present |
| TreatmentApproved | Published | The caller's outbox relay published the event after the transaction committed |
| TreatmentApproved | Absent | The approval was refused or the transaction rolled back; no event exists |
| Contract version | v1 | The published version RWB-S2-E3003-APP, rwb-comms and rwb-payment pin |
| Contract version | v2 | Raised by a breaking change, with a new `ce_type`; v1 stays readable and is never edited |

The approval statuses WAITING, APPROVED, REFUSED and HELD_NO_LIMIT are the `approval` record's and the approval routing's (P7). This contract refers to the final call the routing answers with and holds no status list of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element section, the envelope section and the fakes |
| The owner of rwb-treatment | Approves a breaking change to the element set and freezes a version |
| The rwb-comms owner (P6) and the rwb-payment owner (P8) | Consume the envelope, pin the version and raise a change request rather than a private variant |
| The rwb-decision owner (P7) | Confirms the approval side: the `approval` record, the `ApprovalWorkflow` and the DoA routing the event announces |
| The rwb-access owner (P4) | Confirms the delegation facts the approval request carries; this contract declares none of them |
| The rwb-case owner (P3) | Confirms that no case status and no case event is declared here |
| RW-AUDIT, RW-COE | Audit the decisions through the P7 ledger and the local record, not through this contract |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller or an approver must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes element names, value domains, the event, codes and message identifiers; no customer, account or case value appears outside a synthetic example |
| Element set published | `approvalLevel` (L1 to L6), `approverRole`, `finalCall`, `decidedAt`, `reasonCode`, with the rule that the four outcome elements are absent while an approval is open |
| Personal data | None. The approver is a reference such as a user identifier, never a name; no account number, national identifier or document content appears |
| Tables published | None created: the treatment row of S2, the library object `decision_record` of DP-03, P7's `approval` and P4's `delegation_limit` are named, and the document declares explicitly that no table is added for the second signature |
| Field identifiers | `approvalLevel` carries DF-TRT-011; `approverRole`, `finalCall`, `decidedAt` and `reasonCode` carry no field ID in the TSD, which stops at DF-TRT-033 with `approval_level` as its only approval field (GAP-1872; ASM-3068) |
| Retention | The treatment row and the local record follow their owners' retention; the event is retained on the topic under the platform policy |

The element set is the one place where a business value could leak into the contract, so the document fixes that an element carries a code, a level, an amount or a timestamp and never a floor, a limit, a matrix row or a clock.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, no path, no method and no media type. The below-floor branch is entered from the offer operation `POST /treatments/{treatmentId}/offer`, whose surface and below-floor answer — `belowFloor`, the floor in force and `gapToFloor` — are RWB-S2-E3002-CON's and are named in section 19; this contract fixes only the elements an approved treatment carries, and the treatment resource that shows them is RWB-S2-E3001-CON's. No `/submit` form is published: API Specification v4 and TSD S2 T-A.1 API-S2-004 name one, and RWB-S2-E3002-CON records that form as superseded under the source precedence of Template and Rules §R3, because Architecture v5 slide 18 names `POST /treatments/{id}/offer` as the rwb-treatment operation.

| Element the branch and the screens use | Source | This contract |
|---|---|---|
| `belowFloor`, the floor in force, `gapToFloor` | The offer answer of RWB-S2-E3002-CON | Named only; the branch re-tests the price and never trusts the flag as the trigger |
| `approvalLevel`, `approverRole`, `finalCall`, `decidedAt`, `reasonCode` on the treatment | `approvalLevel` is published on the treatment of API Specification v5; the four others are fixed here | The names, the domains and the absence rule of section 12.3 |

#### 12.2 REST operations consumed

None. The contract consumes no operation: the approval is a child workflow of the kit on rwb-decision's queue, the delegation facts arrive on that request, and the rule version arrives as an event. RWB-S2-E3003-APP consumes no service either, because the case status arrives on the case signal.

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | treatmentId, caseId, treatmentType, offerAmount, approvalLevel, approverRole, finalCall, decidedAt, ruleId, ruleVersion | EV-10: tells rwb-comms to issue the approved offer and rwb-payment to expect the settlement or the proceeds (Architecture v5 slide 42 row 10); written to the caller's outbox in the same transaction |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.treatment.TreatmentApproved.v1 |
| ce_source | rwb-treatment |
| ce_subject | The case ID of the approved treatment |
| ce_id and traceparent | The event identifier and the W3C trace context of the transaction that wrote it |
| Payload | Identifiers and facts only; no personal data and no free text |

| Payload field | Domain or source | Note |
|---|---|---|
| treatmentId | UUID of the treatment | The S2 row, DF-TRT-001 |
| caseId | UUID of the case | Also the record key |
| treatmentType | LOV-TREATMENT; SETTLEMENT or DEED_IN_LIEU on this path | DF-TRT-004 |
| offerAmount | numeric(18,2), baht | DF-TRT-007: the approved offer or the approved transfer price |
| approvalLevel | L1 to L6 | DF-TRT-011, LOV-APPROVAL-LEVEL |
| approverRole | The role code that approved, or the committee's role code | No published domain; the working read (GAP-1872; ASM-3068) |
| finalCall | The option decided; `approved` on a published event | No published domain; the working read |
| decidedAt | timestamptz of the decision | No published field; the working read |
| ruleId | The rule that routed the answer, R-SET-05 or R-DIL-15 | R-SET-05; R-DIL-15 |
| ruleVersion | The version label of the package in force, or the delegation version used | Temporal and Drools Design slides 6 and 15 |

The event name follows Template and Rules §R4 and the topic is the service's own `rwb.treatment.events.v1`. The payload has no published shape beyond the producer, the consumers and the key: Architecture v5 slide 42 names no field, and the ten fields above are the working read of ASM-3068 (GAP-1872). A refusal publishes nothing: the reason code is carried on the treatment row and in the decision record.

#### 12.4 Events consumed

None. The contract consumes no event; `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed by RWB-S2-E3003-APP and names a version this document refers to only as the `ruleVersion` value.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The branch that writes the treatment and the outbox row is RWB-S2-E3003-APP's, and the approval child is the workflow kit's on rwb-decision's queue; a workflow class never writes the element set or the event itself, and a replay reuses the recorded decision.

#### 12.6 Schedules

None. The branch is signal- and event-started, and the three-working-day approval clock of R-SET-05 and R-DIL-15 belongs to the approval routing on rwb-decision's side. This contract declares no Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Carries `approval_level` (DF-TRT-011) and the four outcome columns `final_call`, `approver_role`, `decided_at` and `reason_code` fixed by this contract; no column of a floor, a limit or a matrix row is added |
| `decision_record` | `rwb_treatment` | PLT (library object, DP-03) | The record of the approval, written through RWB-PLT-E1027-CON in the same transaction; its shape is that contract's and is not restated here |
| (none) | — | — | No table is created for the second signature, and no foreign key crosses a schema |
| `approval` | `rwb_decision` | P7 | Named only: the contract declares no field of it and no read or write of it |
| `delegation_limit` | `rwb_access` | P4 | Named only: the delegation level and limit are carried on the approval request and are never read here |

The no-new-table rule is the contract's, not a coding preference: a second table would let the same decision be recorded twice, once as a row and once as a record, which DP-03 and Principle 5 forbid. The treatment columns are added on the service's own migration sequence by RWB-S2-E3003-APP, and this contract fixes their names and their domains only (GAP-1872; ASM-3068).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The treatment approval element | An approved settlement at L6 under DOA-2026.11 and the same case at L5 under DOA-2027.01; an approved deed in lieu under R-DIL-15; a refusal with `price_below_floor`; a settlement refusal with `below_floor_refused`; a treatment with no decision |
| Envelope fake | The `TreatmentApproved` body and the registry | One valid body with the ten fields and key `caseId`; one body with an unknown field; one body with no key; one body carrying a personal field |
| Consumer fake of rwb-comms | The approved offer step | An accepted body, the treatment ID and the case it issues the offer for; a refused body with no key |
| Consumer fake of rwb-payment | The payment expectation | An accepted body and the settlement or transfer the payment side waits for; a refused body with no key |
| Decision-record fake | The record write of DP-03 | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming service rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract declares no operation | 0 | The offer operation is RWB-S2-E3002-CON's and the treatment resource RWB-S2-E3001-CON's; no `/submit` form is published |
| Kafka | 1 event type fixed by the contract, published by the caller's outbox | 0 | AsyncAPI 3.0, CloudEvents 1.0 binary mode, key `caseId` on `rwb.treatment.events.v1` |
| Temporal | 0 | 0 | No workflow and no activity; the approval child is the kit's and the branch is the APP story's |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element set and the envelope in the service's contract document, with the published types in `th.co.scb.ace.workbench.recovery.treatment.api` for the treatment approval element. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The implementation is RWB-S2-E3003-APP.

**Element surface**

| Element | Domain | Absence rule |
|---|---|---|
| `approvalLevel` | L1 to L6 (LOV-APPROVAL-LEVEL, DF-TRT-011) | Empty while no approval has decided; may name the deciding level while an approval is open |
| `approverRole` | A role code, or the committee's role code | Empty while the approval is open |
| `finalCall` | The option decided, as the approval answers it | Empty while the approval is open |
| `decidedAt` | timestamptz | Empty while the approval is open |
| `reasonCode` | The reason in force: `price_below_floor` or `below_floor_refused` | Empty on a granted approval |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; this contract declares the record's use and not its shape | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract adds no path and the offer operation stays under the treatment base | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route; SCR-14 and SCR-15 reach the element set through the route | referred to; the consuming story carries the dependency |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentApprovalElement` | Document section | The five element names, their domains and their absence rule (BR1, BR2) |
| `TreatmentApprovedEnvelope` | Document section and AsyncAPI fragment | The CloudEvents attribute set, the `ce_type`, the key rule and the ten payload fields (BR3, BR4) |
| `RefusalRule` | Document section | No event on a refusal, the reason code in force, and the two decision-record exceptions (BR5, BR6) |
| `VersioningSpecification` | Document section | Major version 1, the compatible versus breaking rule, the pinning rule (BR9) |
| Fake set and fixtures | Test asset | The element, envelope, consumer and decision-record fakes used by this story and the APP story (AC6) |

**Build steps**

1. Write the element section against the treatment representation of the API Specification and the TSD list, and lint the names and domains (AC1).
2. Write the no-new-table rule and name `decision_record`, `approval` and `delegation_limit` with their owners (AC1).
3. Write the envelope section and validate the two examples against the registry fake; assert the type, the key and the ten fields (AC2, AC3).
4. Write the refusal rule with the two reason codes and the two decision-record exceptions (AC4).
5. Write the versioning section with the compatible and the breaking example (AC5).
6. Generate the fake set and write the drift test for this story and RWB-S2-E3003-APP (AC6).
7. Scan every example for personal data and publish v1 with the pinned versions recorded (AC3, AC5).

**Feature flag.** `rwb.treatment.below-floor-approval`.

**Done when.** The document validates, the two examples pass the registry fake and one body is refused, the element fake answers the approved, the refused and the undecided case, the consumer fakes of rwb-comms and rwb-payment accept the approved body and refuse a body with no key, the drift test is green on this story and on the build of RWB-S2-E3003-APP, and v1 is published with the pinned versions of all three consumers recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written and the approval is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException` of RWB-PLT-E1027-CON |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException` with `field` |
| MSG-S2-001 | A settlement offer is below the floor and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. | The caller's screen; the contract fixes the element, not the display |
| MSG-P4-002 | A role without right U prepares the below-floor offer, or a role without RA answers the approval | You cannot {action} here. Your role does not include it. | The guard's answer, unchanged |

The four texts are copied unchanged from RWB-E3-003 and from the decision-record contract; this story adds no message ID. MSG-P7-003 and MSG-P7-009 are the two exceptions that keep an approval from taking effect without its record, and their published catalogue entry format is not specified in the source documents (GAP-1872; ASM-3068). Thai text follows decision DL10.

### 15. Screens and states

No screen is declared by this contract, and it fixes no field of one. SCR-14 Treatment record (states Draft, submitted, approved, booked, broken) and SCR-15 Settlement offer (states Draft, below floor, approved, sent, accepted) read the element set through the gateway-bff composite route (DP-19), and the screen field list and the composite route specification belong to the platform edge story and the screen owners. The contract fixes only the names, domains and absence rule of the five elements, so a screen can render "awaiting second signature" without inventing a field.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3003-CON-01 | AC1 | Contract | The element section linted against the treatment representation and the TSD list; `approvalLevel` L1 to L6; the absence rule of the four outcome elements; the no-new-table statement; a proposed `treatment_approval` table refused |
| TC-S2-E3003-CON-02 | AC2 | Contract | Two examples validated: an approved settlement and an approved deed in lieu; the CloudEvents attribute set; `ce_type`; the ten payload fields; one accepted and one refused body in BACKWARD mode |
| TC-S2-E3003-CON-03 | AC3 | Contract | The key rule with a case and `ce_subject`; the personal-data scan on both examples, with a name, an account number and a free-text field each refused |
| TC-S2-E3003-CON-04 | AC4 | Contract | A refused second signature with `price_below_floor` and a refused settlement with `below_floor_refused`; no event and no outbox row; a forced record failure with MSG-P7-003 and a refused field with MSG-P7-009 |
| TC-S2-E3003-CON-05 | AC5, AC6 | Component | A compatible change and a breaking change against the registry; the element, envelope and two consumer fakes; the drift test on this story and on RWB-S2-E3003-APP |

The legacy test set of RWB-E3-003, TC-E3-003-01 to TC-E3-003-06, is carried by RWB-S2-E3003-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the floor, the DoA levels and limits, the approval clock and the reason-code list are values in force of their owners; the only values this document fixes are the element names, their domains and the synthetic examples.
- No personal data in a schema, an example, a fake or a log: the approver is a reference, the subject is a case identifier, and the scan fails the build otherwise.
- No new table and no second write path for the approval outcome: the treatment row and the decision record are the only places it lives, and the boundary test fails the build on a third.
- No cross-schema reference and no foreign key across services: `approval` and `delegation_limit` are named, never joined and never read.
- No REST surface of this contract's own: the offer operation belongs to RWB-S2-E3002-CON and the treatment resource to RWB-S2-E3001-CON, and no `/submit` form is published.
- No event on a refusal, and no field in the payload beyond the ten: rwb-comms and rwb-payment hear only of an approved treatment.
- A published version is never edited in place: a breaking change raises major version 2 with a new `ce_type` and a migration note.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Business Requirements Program, section 5.9 | FEAT-TRT-03 | 07 Route, settle and claim | R-SET-05; R-DIL-15; R-DIL-17 | TC-S2-E3003-CON-01 to TC-S2-E3003-CON-05 |
| Legacy test set RWB-E3-003 | TC-E3-003-01, TC-E3-003-02, TC-E3-003-03, TC-E3-003-04, TC-E3-003-05, TC-E3-003-06 | Program, section 5.9 | The legacy story's own feature | 07 Route, settle and claim | R-DIL-15; R-DIL-17; R-SET-05 | Executed by RWB-S2-E3003-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3003-APP | App development | H consumer: implements the below-floor branch, the element set and the publisher against this contract and its fakes |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment contract baseline that carries the treatment representation and its read |
| RWB-S2-E3002-CON | Contract | Referred to: the settlement range and the offer operation, which are not declared here |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library whose shape and exceptions are named and not restated |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route by which the screens read the element set |
| P6 rwb-comms, P8 rwb-payment | Consumer | Subscribe `TreatmentApproved` and pin the version |
| P7 rwb-decision | Owner | The `approval` record, the `ApprovalWorkflow` and the DoA routing the event announces |
| P4 rwb-access | Owner | `delegation_limit`, the levels and limits carried on the approval request |
| The wave 2 integration harness | Integration | The cross-service proof of the event against the live rwb-comms and rwb-payment |

### 19. Out of scope

- The implementation — the below-floor branch of `TreatmentWorkflow`, its four activities, the child workflow call, the treatment columns and the publish: RWB-S2-E3003-APP.
- The offer operation `POST /treatments/{treatmentId}/offer`, its below-floor answer and the settlement range and payoff: RWB-S2-E3002-CON and RWB-S2-E3002-APP.
- The treatment resource, its creation and its field list DF-TRT-001 to DF-TRT-033: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The `Approval` schema of the API Specification and the operation that answers with it: the published specification and RWB-S2-E3002-CON, adopted and not re-declared here.
- The `approval` record, the `ApprovalWorkflow`, the DoA routing of FEAT-APD-01, the approval clock and its escalation: rwb-decision, the workflow kit and its own stories.
- The delegation data, the levels L1 to L6, their holders, substitutes and valid-from dates: rwb-access.
- The decision-record library, its shape, its chain and its two exceptions: RWB-PLT-E1027-CON.
- The case status, the case table and the case signal: rwb-case.
- The documents, the e-signature and the customer notice that follow a granted second signature: rwb-document, rwb-comms and the sibling stories of this service.
- The topic, its ACLs, the retry topics and the dead-letter topic: RWB-PLT-N002-INF and the event platform.
- The deployment, the flag and the dashboards of this build: this legacy key's DevOps story.
- The real cross-service proof of the event against the live rwb-comms and rwb-payment: the wave 2 integration harness.
 integration harness.
ss.
 integration harness.

n harness.

ess.

