# RWB-P2-E2007-CON Booking confirmation from the ALS load - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004, RD-P1-065, RD-P1-066; requests S10-stories-0245, S3-stories-0148; Test Cases v9 mappings.

- Decision-record event type name corrected to `rwb.decision.DecisionRecorded.v1`; topic `rwb.decision-record.v1` unchanged (RD-P1-008).
- `AceDataReady` consumption aligned: record key per source system and business date, daily work starts only on `sourceSystem` ALS with `status` COMPLETED (RD-P1-003, RD-P1-040).
- Freshness status values and stamp rule, and the batch status fixture, aligned (RD-P1-005, RD-P1-041).

| Item | Value |
|---|---|
| Story key | RWB-P2-E2007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (base path /api/recovery/integration/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-008, RD-P1-040, RD-P1-041, RD-P1-004, RD-P1-023, RD-P1-065, RD-P1-066 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2007-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 39 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)** role holder, I want **the rwb-integration side of booking confirmation fixed as a contract — the match request and result shape, the three task codes and their messages, the `TreatmentBooked` envelope the journey relies on, the job administration operations, the error envelope and the idempotency rule, with fakes for rwb-source-data, rwb-case, rwb-decision and rwb-treatment**, so that **the app and operations stories of this key, the case transition of RWB-P3-E2007-APP, the treatment slice of the S2 story and the integration harness build on Day 1 against one agreed, testable shape**.

The legacy story held the match, the job, the ACE view read, the task texts and the treatment writes in one P2 Integration module and named them as Java interfaces (`TreatmentQuery.approvedNotBooked`, `TreatmentCommands.markBooked`, `TreatmentCommands.recordBookingDifference`, `AccountQuery.forCase`, `BatchStatusQuery.forSource`, `RuleEvaluator.evaluate`, `TaskApi.raiseTask`). Under D-RCV-60 the match is a workflow of rwb-integration and every write belongs to the owner of the record. This contract fixes the seam: what the match is started with, what its result means, which task code each outcome raises, which event the journey waits for, and which operations the service serves and consumes.

The contract also states what this service does not own. The treatment record, its state, `booked_at` and the booking difference are rwb-treatment's behind RWB-P3-E2004-CON. The route state, the task rows and the case timeline are rwb-case's. The ACE accounts, the booked terms and the batch-completeness answer are rwb-source-data's, because only rwb-source-data reads the `recovery.v_ace_*` views and ACE data (ADR-010, DP-05). The BOOKING_MATCH rows and the version in force are rwb-decision's behind RWB-P3-E2042-CON. The authorise decisions are rwb-access's. `rwb_integration` holds no copy and no foreign key (DP-01).

**Two rulings this contract records rather than re-opens.** Architecture v5 slide 44 names rwb-payment the owner of JOB-08 and slides 42 and 43 list rwb-payment, not rwb-integration, among the consumers of `AceDataReady` and `TreatmentApproved`; this realignment keeps JOB-08 and its activities with rwb-integration, as RWB-P4-E2007-APP and RWB-ITG-E2007-ITG both state, and the conflict is carried here (GAP-0658; ASM-1121). TSD P2 Integration v3 T5.2 says that P2 reads the ACE views directly and calls nothing in P1; that sentence is superseded by ADR-010 and DP-05, and the same gap row carries it (ASM-1123).

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling rule (DP-11, ADR-020), and the record of a booking is split across rwb-treatment, rwb-case and rwb-payment. Both only work if the seam is written down once. The seam here is small and load-bearing: a run started by an event, a facts shape that a first-match decision table can consume, a result that names the row and the version, three task codes that already exist in the business rules, and an envelope the journey can wait for without this service publishing a second one.

Four teams move at once if the shape is agreed and faked on Day 1. The app story builds the workflow, the facts builder and the four contract clients against the fakes; the operations story deploys the worker, the job catalogue row, the alerts and the runbook against the names this document fixes; the case transition of RWB-P3-E2007-APP builds its task raise and its route move against the result shape; and the harness of RWB-ITG-E2007-ITG reads the same answer through the owning services. Without the contract, the outcome, the task code and the message would be interpreted in four places, and the measure the legacy story sets — REC-03, approved treatments against bookings, zero after two days — would have no single owner.

The contract is also where the legacy split is made explicit. Five statements of the legacy criteria belong to other slices and are proved there: the case move on BOOKING_CONFIRMED and SETTLEMENT_BOOKED with the route state and the case record (AC1, RWB-P3-E2007-APP), the batch gate and the missing-booking suppression (AC5, proven end to end in RWB-ITG-E2007-ITG), the absence of a second task on the next batch (AC7, RWB-P3-E2007-APP), the treatment state and the difference column (the S2 story), and the refusal of a role without the right (RWB-P4-E2007-APP). This document fixes what those slices may rely on when they do them: the result shape, its outcomes, the task codes and their texts, the idempotency of a repeat and the one-task rule.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the task queue and the event names follow the platform rule (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the RFC 9457 problem-details body and the platform message catalogue are the platform baseline; this document narrows them where it must and says so.
- The embedded Drools kit contract is available (RWB-PLT-E1072-CON, DP-04): the `RuleResult` and `NoPackageInForce` types, the first-match semantics, the cache bound and the checksum rule are its elements, and this document reuses them rather than redefining them.
- The workflow kit and its conventions are available (RWB-PLT-E1071-CON, RWB-PLT-WF): the task queue `rwb-integration`, the namespace `rwb-recovery`, the event-started start, the activity retry policy and the non-retryable outcomes.
- The outbox, inbox and idempotency library is available (RWB-PLT-TE006-CON): `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` in `rwb_integration` (DP-09).
- The local decision-record library is available (RWB-PLT-E1027-CON) with the shared topic `rwb.decision-record.v1` (DP-03).
- The rwb-treatment contract of RWB-P3-E2004-CON, the rwb-case task and reference contracts, the rwb-source-data account, freshness and reconciliation contracts of RWB-P1-E2007-APP and the rwb-decision rule-model read of RWB-P3-E2042-CON are published, or are faked to the shapes this document declares. This document consumes them and defines none of them.
- The rwb-access authorise contract (RWB-P4-E1037-CON) is published, or is faked to the shape this document declares (DP-19, DP-11).
- The legacy values of this key are the agreed values: package code BOOKING_MATCH, version `BKG-2026.12`, tolerance 0.00 baht, the task codes `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION`, the owner roles RW-RESTRUCT and RW-CREDITAD, the messages MSG-P2-011 and MSG-P2-012, the parameter `booking.missing.grace_loads` = 1 and the event names `AceDataReady`, `TreatmentApproved` and `TreatmentBooked`.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the provided operations, each on the per-service base with one hop and a 2 s timeout: `POST /admin/jobs/{jobId}/rerun` on the integration base, with its right, its input, its answer, its 401, 403, 404, 409 and 503 and its idempotency rule, and the statement that the job catalogue read of the base carries the JOB-08 row this key writes.
2. Publish the match request and result shape: the run input, the facts element set, the outcome enumeration `BOOKED`, `NO_BOOKING`, `TERMS_DIFFER`, the fired row and package version, the difference terms and the accounts without a booking. The decision code a booking decision carries is Not specified in the source documents (GAP-2486).
3. Publish the three task codes with their owner roles, their messages and their parameters, and the one-open-task rule.
4. Publish the `TreatmentBooked` envelope the journey relies on, its producer and its payload, and state that this service neither publishes nor consumes it.
5. Publish the consumed shapes: the treatment list, the treatment read, the mark-booked write, the difference write, the case-account read answered from the case list row (GAP-0595), the freshness answer as the DataProductFreshness record of RWB-P1-E1015-CON (GAP-0594), the reconciliation write, the task raise, the reference-data read, the parameters read, the rule-model read and the authorise call, each with its owner and the 2 s budget.
6. Publish the workflow contract: `BookingMatchWorkflow`, its six activities, the gates and the non-retryable outcomes. The retry count, backoff and timeout of each activity that retries or times out are Not specified in the source documents (NEWAC-RWB-P2-E2007-CON-AC11).
7. Publish the table section: the three tables of the service, the `job_catalog` row of JOB-08 and the library tables, with the statement that no treatment, case, account or task row is copied.
8. Publish the error mapping over the ten messages and the error envelope of every operation.
9. State the split of the legacy criteria and the ownership conflict of JOB-08, and record the superseded TSD P2 v3 T5.2 sentence.
10. Build the contract fakes of rwb-treatment, rwb-source-data, rwb-case, rwb-decision, rwb-access and the decision-record library.
11. Add the contract tests: the operation shapes, the consumed shapes, the workflow contract, the table section, the message mapping and the drift test between each fake and this document; tag the baseline and hand it to the app and operations stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An operation, a consumed shape or the result shape contradicts this document | The contract test fails and the merge is blocked | None | AC1, AC2, AC3, AC4 |
| X2 | A fake drifts from this document, or answers a shape this document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X3 | A field-level detail of a consumed operation is missing from the source material | The element carries the placeholder, one gap row and one assumption row are recorded, and the fake is written to the assumed shape | None | AC5, AC6 |
| X4 | An outcome is returned that the enumeration does not hold, or the result names no fired row or no package version | The consumer refuses the result and the run is failed as a contract defect, never as a business outcome | MSG-GEN-006 | AC1 |
| X5 | A task code is raised that is not one of the three, or with an owner role other than the one the table fixes | The rwb-case contract refuses the call and the run records the refusal | MSG-GEN-001 | AC2 |
| X6 | A document declares JOB-08 as a Schedule, or publishes `TreatmentBooked` from this service | The review refuses the document | None | AC3, AC4 |
| X7 | A document reads the ACE views or another service's table, or names the old monolith base | The review refuses the document | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and kits and the published contracts of the other services, and fakes them |
| Negotiable | The field-level detail of the consumed operations is settled with their owners; the result shape, the task table and the rerun operation are fixed by this realignment |
| Valuable | Unblocks the app and operations stories, the case transition of RWB-P3-E2007-APP, the treatment slice and the harness of this legacy key |
| Estimable | One operation provided, twelve consumed paths and operations, one workflow with six activities, four tables and seven fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion tests an artefact — the schema, the fake, the table section, the message map — and never a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation contract baseline for rwb-integration

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the embedded Drools kit contract of RWB-PLT-E1072-CON and the workflow kit of RWB-PLT-E1071-CON are in force
    Given the package code is BOOKING_MATCH and the package version is "BKG-2026.12" with tolerance 0.00 baht

  Scenario: AC1 The match request and result shape are fixed (new, D-RCV-60)
    Given the contract tables of sections 12.1, 12.2 and 12.5
    When the request and the result are reviewed
    Then the run input is documented as the source system ALS and the business date, with the treatment ID and the account list added per treatment
    Then the facts element set is documented as treatmentId, caseId, treatmentType, offerAmount, interestRate, approvalDate, accountKey, tdrFlag, lastTdrDate, principalOutstanding, interestRateBooked, settlementBookedDate, settlementBookedAmount and businessDate
    Then the result is documented with the outcome enumeration "BOOKED", "NO_BOOKING" and "TERMS_DIFFER", the fired rule ID, the package code and package version, the difference terms and the accounts without a booking
    Then a result that names no fired rule or no package version is documented as refused under MSG-GEN-006
    Then the result holds no account number, no party name and no identity number

  Scenario: AC2 The three task codes, their roles and their messages are fixed (new, D-RCV-60)
    Given the contract table of section 12.2 and the validation table of section 14
    When the task table is reviewed
    Then "WITH_OPS_BOOKING" is documented for role "RW-RESTRUCT" with MSG-P2-011 for a restructure whose booking is missing
    Then "WITH_OPS_SETTLEMENT" is documented for role "RW-RESTRUCT" with MSG-P2-011 for a settlement whose booking is missing
    Then "UNMATCHED_EXCEPTION" is documented for role "RW-CREDITAD" with MSG-P2-012 for a treatment whose terms differ
    Then MSG-P2-011 carries the treatment, the business date and the accounts not booked, and MSG-P2-012 carries the term, the booked value and the approved value
    Then both texts are the legacy texts unchanged, and a task code outside the three is refused by the rwb-case contract
    Then at most one open task exists per case, task code and treatment
    Then package version "BKG-2026.12", tolerance 0.00 baht and the grace parameter of 1 are documented as carried unchanged

  Scenario: AC3 The TreatmentBooked envelope and its producer are fixed (new, D-RCV-60)
    Given the contract tables of sections 12.3 and 12.4
    When the envelope is reviewed
    Then "rwb.payment.TreatmentBooked.v1" is documented on "rwb.payment.events.v1" with owner rwb-payment, key caseId and the payload treatmentId, bookingRef (account key and business date) and businessDate
    Then the document states that rwb-integration neither publishes nor consumes this event, and that the envelope is the one the journey waits for after a confirmed booking
    Then the document states that this service publishes no event of its own on "rwb.integration.events.v1" for this key, whose events are FileDelivered and FileFailed
    Then the document states that the local decision record is relayed as "rwb.decision.DecisionRecorded.v1" on "rwb.decision-record.v1" by the library
    Then one confirmed treatment and business date produce exactly one "TreatmentBooked" and no second one on a rerun

  Scenario: AC4 The job administration operations and the BookingMatchWorkflow registration are fixed (new, D-RCV-60)
    Given the contract tables of sections 12.1, 12.5 and 12.6
    When the job surface is reviewed
    Then POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun is documented with the Platform administration U right, the business date input, the 401, 403, 404, 409 and 503 answers and the Idempotency-Key rule
    Then a rerun is allowed only for a FAILED run on the same date with ALLOW_DUPLICATE_FAILED_ONLY; a complete or running run returns 409 with MSG-P2-006, and a job absent from this service's catalogue as 404 with MSG-P4-003
    Then the job catalogue read of the integration base is documented as the read that returns the BookingMatchWorkflow row and its run book path
    Then BookingMatchWorkflow is documented as an event-started workflow on queue rwb-integration, started by AceDataReady, with no Schedule ID and no cadence
    Then one run per business date is documented for BookingMatchWorkflow (BR10); its timezone, overlap, retry and fallback and the behaviour of the legacy feature flag when off are Not specified in the source documents (GAP-2491)
    Then the document records that Architecture v5 slide 44 names rwb-payment the owner of BookingMatchWorkflow and that the accepted split keeps it with rwb-integration, citing the gap row

  Scenario: AC5 The twelve consumed operations are published with one budget and the supersession is recorded (new, D-RCV-60)
    Given the contract table of section 12.2 and the guardrails of section 17
    When the consumed set is reviewed
    Then the treatment list, the treatment read, the mark-booked write, the difference write, the case-account read, the freshness answer, the reconciliation write, the task raise, the reference-data read, the parameters read, the rule-model read and the authorise call are each described with method or operation name, owner, use and the 2 s client budget
    Then each one is attributed to rwb-treatment, rwb-source-data, rwb-case, rwb-decision or rwb-access and none is declared as provided by rwb-integration
    Then the five paths and shapes that no source fixes carry the placeholder and cite the gap row
    Then the authorise decision is served from a cache keyed on identity, area, right, case reference, field list and matrix version, and dropped when the pack version changes; its lifetime is read as a parameter whose value is Not specified in the source documents (GAP-0924)
    Then the document states that the ACE accounts and the batch answer come only through the rwb-source-data contract, that TSD P2 Integration v3 T5.2 is superseded, and that rwb_integration holds no grant on recovery

  Scenario: AC6 The nine contract tables are complete, the fakes match them and the error envelope covers the ten messages (new, D-RCV-60)
    Given the contract section and the validation table of this story
    When the nine sub-tables and the fakes are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.7 names interface_config, outbound_item, job_catalog and the library tables only, and holds no treatment, case, account or task table
    Then 12.8 names the fakes of rwb-treatment, rwb-source-data, rwb-case, rwb-decision, rwb-access, the decision-record library and the inbox and idempotency stub, and the drift test fails on any difference
    Then MSG-P2-011, MSG-P2-012, MSG-P1-001, MSG-P7-003, MSG-P3-027, MSG-P2-006, MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-GEN-006 are each mapped to the operation or outcome that raises them
    Then MSG-P1-001 uses the FSD P2 Integration v3 wording and MSG-P3-027 names the package check and the business date only
    Then the old monolith base appears nowhere in the document
    Then the decision record is documented as written before any remote call, and a failed write as making no call and raising an incident
    Then no data lake and no lake file is named, built or sent by the contract
    Then the seven platform build rows RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON and the contract rows RWB-P3-E1042-CON and RWB-P3-E1043-CON are named with the treatment and task contracts, the key of the further contract row is Not specified in the source documents (GAP-2488), and their dependency map entry is decided at step D1 (GAP-2488)

  Scenario: AC7 Each business rule BR1 to BR14 is traced to a criterion, a test or a guardrail (new, D-RCV-60)
    Given the business rules of section 8
    When the rule table is reviewed
    Then each rule ID from BR1 to BR14 is named by an AC of this section, a test case of section 16 or a guardrail of section 17
    Then the proposed test for this trace is Not specified in the source documents (NEWAC-RWB-P2-E2007-CON-AC10)

  Scenario: AC8 Activity retry and timeout are fixed (new, D-RCV-60)
    Given the contract table of section 12.6
    When the BookingMatchWorkflow activities are reviewed
    Then the retry count, the backoff and the timeout of each activity that retries or times out are documented as Not specified in the source documents (NEWAC-RWB-P2-E2007-CON-AC11)
```

The eight criteria above are new and test only this deliverable: the contract baseline, the fakes and the message map of the booking-confirmation slice. The legacy criteria of RWB-E2-007 are owned elsewhere: AC2, AC3, AC4, AC6, AC8 and AC9 by RWB-P2-E2007-APP, AC1, AC6, AC8 and AC9 by RWB-P3-E2007-APP, AC1, AC5 and AC7 by RWB-ITG-E2007-ITG, and AC5 and AC7 also by RWB-P1-E2007-APP and RWB-P4-E2007-APP in their slices. This document derives its shapes from those criteria and re-states none of them as its own. The legacy levels map as System to Component, Access to Contract and Resilience to NFR (GAP-2490).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base and one task queue per service: this contract declares `/api/recovery/integration/v1` and `rwb-integration`, consumes the other bases and never declares another service's path as provided | DP-13; DP-14; Arch v5 slide 41 | AC5, AC6; TC-P2-E2007-CON-05, TC-P2-E2007-CON-06 |
| BR2 | The match is decided by package BOOKING_MATCH through the embedded kit, first match wins, and only `RuleResult` and `NoPackageInForce` cross the seam; no second engine and no rule table runs in this service | D-RCV-36 T3, T5, T7; DP-04 | AC1; TC-P2-E2007-CON-01 |
| BR3 | The treatment is written only by rwb-treatment, the task only by rwb-case, the account and batch facts are read only through rwb-source-data, the package only through rwb-decision, and the REC-03 result only through rwb-source-data, the owner of the break list being Not specified in the source documents (GAP-2492) | Arch v5 slides 41 and 45; DP-01; DP-05 | AC5, AC6; TC-P2-E2007-CON-05, TC-P2-E2007-CON-06 |
| BR4 | Only rwb-source-data reads the `recovery.v_ace_*` views; TSD P2 Integration v3 T5.2 is superseded on that point, and `rwb_integration` holds no grant on `recovery` | ADR-010; DP-05; Arch v5 slides 41 and 45 | AC5; TC-P2-E2007-CON-05 |
| BR5 | JOB-08 is an event-started workflow started by `AceDataReady`, not a Schedule, and the job catalogue row is the only catalogue trace of it | Arch v5 slides 42 and 44; DP-10; GAP-0658; ASM-1121 | AC4; TC-P2-E2007-CON-04 |
| BR6 | Three task codes only, each with one owner role and one message: `WITH_OPS_BOOKING` and `WITH_OPS_SETTLEMENT` to RW-RESTRUCT with MSG-P2-011, `UNMATCHED_EXCEPTION` to RW-CREDITAD with MSG-P2-012; at most one open task per case, task code and treatment | Legacy RWB-E2-007 §4, §5 and §14; BR5 and BR6 of RWB-P2-E2007-APP | AC2; TC-P2-E2007-CON-02 |
| BR7 | An outcome outside the enumeration, or a result naming no fired row or no package version, is refused as a contract defect and never interpreted | Legacy X9; D-RCV-36 T5 | AC1; TC-P2-E2007-CON-01 |
| BR8 | The decision record is written before any remote call; a failed write makes no call and raises an incident | R-UNI-39; DP-03 | AC6; TC-P2-E2007-CON-06 |
| BR9 | `TreatmentBooked` is rwb-payment's event; this service never publishes it and never consumes it, and the journey waits for exactly one per confirmed treatment and business date | Arch v5 slide 42 (EV-11); legacy RWB-E2-007 AC6 | AC3; TC-P2-E2007-CON-03 |
| BR10 | One run per business date and one record per treatment and business date; a repeat is answered by the idempotency record | Legacy RWB-E2-007 AC6; DP-09 | AC3, AC4; TC-P2-E2007-CON-03, TC-P2-E2007-CON-04 |
| BR11 | A consumed field, path or error that no source fixes is written with the placeholder and carried in one gap row plus its assumption rows, never invented | Template and Rules §R9 | AC5; TC-P2-E2007-CON-05 |
| BR12 | No personal data in an event, a result, an example or a fake: case IDs, treatment IDs, account keys, role codes, rule IDs, version labels and dates only | Arch v5 slide 42; Template and Rules §R7.2 s17 | AC1; TC-P2-E2007-CON-01; guardrails of section 17 |
| BR13 | The legacy values of the key are carried unchanged: package version `BKG-2026.12`, tolerance 0.00 baht, the three task codes, the two owner roles, the two task messages and the grace parameter of 1 | Legacy RWB-E2-007 §3, §7, §14; RWB-E2-042; GAP-0658; ASM-1125 | AC2; TC-P2-E2007-CON-02 |
| BR14 | No data lake and no lake file is named, built or sent by this contract | DP-17; Arch v5 slide 37 | AC6; TC-P2-E2007-CON-06 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the result, the task table, the envelope, the consumed set, the workflow, the tables and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the operations story, the case transition story, the treatment slice and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field or an error is added to an operation without removing one | Baselined |
| Baselined | Breaking change to a consumed shape | rwb-treatment, rwb-source-data, rwb-case, rwb-decision or rwb-access removes, renames or retypes an element this contract consumes | In review, with the owner of that operation |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A package version becomes in force | rwb-decision announces it and the cached model of the superseded version is dropped | Baselined |
| Baselined | JOB-08 moves to another owner | The solution architect rules a new owner and the job catalogue, the task queue and the consumer lists move with it | In review |

The run, treatment and route state machines are not this document's: the run states `NOT_STARTED`, `RUNNING`, `COMPLETED`, `FAILED` and `SKIPPED` belong to RWB-P2-E2007-APP, the treatment state to the S2 story and the route state to RWB-P3-E2007-APP. This contract fixes only the shapes they exchange.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns the document, the operation shape, the result shape, the task table and the seven fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed contract and the JOB-08 ownership ruling |
| The rwb-treatment owner | Owns the treatment list, the treatment read, the mark-booked write and the difference write; signs off the shapes taken from RWB-P3-E2004-CON |
| The rwb-source-data owner | Owns the case-account read, the freshness answer and the reconciliation write; signs off the ACE-read boundary of BR4 |
| The rwb-case owner | Owns the task raise and the reference-data and parameter reads; signs off the task codes and the one-task rule |
| The rwb-decision owner | Owns the BOOKING_MATCH registry and the rule-model read; signs off the result shape |
| The rwb-access owner | Owns the authorise contract and signs off its consumption |
| Platform workflow kit owner | Owns the event-started start, the task queue and the retry policy this document reuses |
| Data steward | Confirms that no personal data field is declared in a result, an event or an activity input |

The deployment identity that calls the consumed contracts is Not specified in the source documents (GAP-0658; ASM-1122); the document names it "the rwb-integration login (DP-02)" and leaves the name to RWB-P2-E2007-OPS.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Run input | source system ALS, business date; per treatment the treatment ID and the case ID | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Facts element set | treatmentId, caseId, treatmentType, offerAmount, interestRate, approvalDate, accountKey, tdrFlag, lastTdrDate, principalOutstanding, interestRateBooked, settlementBookedDate, settlementBookedAmount, businessDate | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Result | outcome `BOOKED`, `NO_BOOKING` or `TERMS_DIFFER`; fired rule ID; package code BOOKING_MATCH; package version; difference terms; accounts without a booking; treatment ID; case ID; business date | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Task row request | caseId, taskCode, ownerRole, messageId, parameters (treatment, date, accounts, term, booked, approved) | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Treatment write | treatmentId, businessDate, bookingRef (account key and business date), difference terms | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Reconciliation write | the REC-03 result: business date, treatments read, booked, missing, differing, the treatment IDs and the days missing | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Decision record | decision code, case ID, treatment ID, fired rule ID, package version, outcome, actions, decided at, hash chain, idempotency key | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Event envelope | CloudEvents 1.0 with the event type, the topic, the key caseId and the payload of the event | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Job catalogue row | job_id, job_name, owner_role, schedule_text (the event trigger), runbook_path, expected_minutes, alert_after_minutes | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Rerun request and answer | business date in; the job state, the business date and the run reference out | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |
| Booking facts read and batch status read | rwb-source-data.yaml 5.1.0 publishes GET /booking-facts (accountKey and businessDate, BookingFactsAnswer with full DataProductFreshness; 409 MSG-P1-001 when the gate refuses) and GET /batch-status (sourceSystem and businessDate, BatchStatusAnswer; 404 MSG-P4-003 if no row). caseId is the case UUID. The match translates a refused gate or absent batch into FAILED with MSG-P1-001. Only a FAILED run is rerun from the rwb-integration job monitor for the same date with ALLOW_DUPLICATE_FAILED_ONLY. | RWB-P1-E2007-APP; RD-P1-065 |
| Case account set and product group | read from the case list row for the case and business date (business date DF-RPT-002, case ID DF-RPT-003, account key DF-RPT-005, product group DF-RPT-007); the case_account table of rwb-case is not read | Not specified in the source documents (DOR-RWB-P2-E2007-CON-7) |

The field-level detail of the twelve consumed operations — property types, lengths, required flags and query parameters — is Not specified in the source documents (GAP-0658; ASM-1123); this document fixes the element names above and leaves the types to the review with each owner. The values of the package rows are the legacy values of this key and are carried unchanged (BR13). The account read answers account facts only: no treatment term, outcome, difference, tolerance or package version; BookingMatchFacts is built by the calling slice from its treatment contract and these facts (GAP-0598). How the read answers each of the three facts principalOutstanding, settlementBookedDate and settlementBookedAmount is Not specified in the source documents (GAP-0596). The flag that holds the read back is Not specified in the source documents (GAP-0596).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/jobs/{jobId}/rerun` | Path: `jobId`. Body: the business date of the run. Answer: the job state, the business date and the run reference; a treatment already handled for the date is skipped. 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 409 for a complete or running run (MSG-P2-006), 422 (MSG-GEN-001), 503 (MSG-P7-003, MSG-GEN-006) | Platform administration U, scope applied | `Idempotency-Key` per job and business date; the stored answer is replayed and no second run starts |

The job catalogue read `GET /admin/scheduled-jobs` and the outbox delivery operations belong to the integration base of RWB-P2-E1007-CON; this contract declares them as consumed surface, not as its own, and only adds the JOB-08 row that read returns (section 12.7). The rerun is the operation the legacy story named at `POST /admin/jobs/{jobId}/rerun`; API Specification v5 keeps that path with x-module P1 as the generic rerun of the job catalogue, while this realignment makes JOB-08 a rwb-integration job and therefore its rerun a rwb-integration operation. The placement and the split are recorded (GAP-0658; ASM-1122).

The match itself serves no REST operation: it is started by `AceDataReady`, and its outcome is read through the treatment contract, the task list of rwb-case and the reconciliation answer of rwb-source-data. A match read on the integration base was considered and is deliberately not declared, because the legacy story exposes none and no source fixes one.

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path or operation | Owner | Contracted use |
|---|---|---|---|
| GET | The approved-not-booked list read of RWB-P3-E2004-CON — Not specified in the source documents (GAP-0658; ASM-1123) | S2 rwb-treatment | The approved RESTRUCTURE and SETTLEMENT treatments not yet booked, with the type, the case and the approved terms |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Type, state, `offer_amount`, `interest_rate`, `booked_at` and the booking difference |
| POST | The mark-booked write of RWB-P3-E2004-CON — Not specified in the source documents (GAP-0658; ASM-1123) | S2 rwb-treatment | Marks booked with the business date and the booking reference; writes its own record and fails closed |
| PATCH | The booking-difference write of RWB-P3-E2004-CON — Not specified in the source documents (GAP-0658; ASM-1123) | S2 rwb-treatment | Records the difference terms |
| GET | The case-account read at a business date of the rwb-source-data contract — Not specified in the source documents (GAP-0658; ASM-1123) | P1 rwb-source-data | The accounts of the case and their booked terms at the business date |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The ALS batch status, business date and `is_complete` |
| POST | The reconciliation write of the rwb-source-data contract — Not specified in the source documents (GAP-0658; ASM-1123) | P1 rwb-source-data | The REC-03 result into `reconciliation_result` |
| POST | The `raiseTask` operation of the rwb-case contract (RWB-P3-E2007-APP) — Not specified in the source documents (GAP-0658; ASM-1123) | P3 rwb-case | One open task per case, task code and treatment, with the owner role and the message ID |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | The treatment-type and task-code LOV rows with the version in force |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | `booking.missing.grace_loads` with the version in force |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision through RWB-P3-E2042-CON | The BOOKING_MATCH model and checksum for the version in force |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Platform administration U for the rerun, cached per session |

**Task table.** The three task codes are the only ones this key raises, and the roles and texts are the legacy ones (GAP-0658; ASM-1125).

| Task code | Owner role | Message | Raised when | Parameters of the message |
|---|---|---|---|---|
| `WITH_OPS_BOOKING` | RW-RESTRUCT | MSG-P2-011 | A restructure is past the grace batches with no booking | treatment, date, accounts |
| `WITH_OPS_SETTLEMENT` | RW-RESTRUCT | MSG-P2-011 | A settlement is past the grace batches with no booking | treatment, date, accounts |
| `UNMATCHED_EXCEPTION` | RW-CREDITAD | MSG-P2-012 | A booked term differs from the approved term | term, booked, approved |

#### 12.3 Events published

None of the service's own. `rwb.integration.events.v1` carries `FileDelivered` and `FileFailed`, which belong to the outbound-file stories of this service (RWB-P2-E1007-APP), and this key publishes neither.

The local decision-record library publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the record, keyed by case ID, with the decision code, the fired rule ID, the package code and version, the outcome, the treatment ID and the business date (DP-03).

The envelope the journey relies on is another service's:

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | P8 rwb-payment | caseId | treatmentId, bookingRef (`account_key` + business date), businessDate |

The document states plainly that rwb-integration does not publish and does not consume `TreatmentBooked`, and that exactly one leaves rwb-payment per confirmed treatment and business date, with none on a rerun and none when the record cannot be written (BR9).

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event | Topic | Owner of the type | Contracted use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts `BookingMatchWorkflow` for the business date on only the event with `sourceSystem` ALS and `status` COMPLETED (record key `{sourceSystem}:{businessDate}`, `ce_subject` = sourceSystem, payload `sourceSystem`, `businessDate`, `status`, `completedAt`); a duplicate is dropped through `processed_event` |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | `TreatmentApprovedListener` records the approval date the match compares with the booked date; a duplicate is dropped through `processed_event` |

Both envelopes are CloudEvents 1.0 with the event ID, the source, the type, the subject and the time; the payload carries IDs and facts only. The consumer lists of Architecture v5 slides 42 and 43 do not name rwb-integration for either event; the subscriptions are additive for the JOB-08 run this realignment places here and the added consumer rows are carried in the gap (GAP-0658; ASM-1124).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `BookingMatchWorkflow` | Workflow, workflow ID prefix `booking-match-` | `rwb-integration` | Input: source system ALS, business date. Output: counts of treatments read, booked, missing, differing, skipped and failed, and the run outcome `COMPLETED`, `FAILED` or `SKIPPED` |
| `readBookedTerms` | Activity | `rwb-integration` | Input: case ID, business date. Output: the batch-completeness answer and the accounts with booked terms; raises `AceBatchNotComplete`, non-retryable |
| `listApprovedTreatments` | Activity | `rwb-integration` | Input: the treatment types, the grace count, the business date. Output: the approved treatments not yet booked |
| `evaluateBookingMatch` | Activity | `rwb-integration` | Input: treatment, accounts, business date. Output: the `RuleResult` per account; raises `NoPackageInForce`, non-retryable |
| `applyBookingOutcome` | Activity | `rwb-integration` | Input: the treatment and its result. Output: the record reference and the outcome applied; makes no remote call when the record cannot be written |
| `raiseBookingTasks` | Activity | `rwb-integration` | Input: treatment, outcome, accounts without a booking. Output: the task reference or the existing open task |
| `writeRunSummary` | Activity | `rwb-integration` | Input: the run counts and the business date. Output: the REC-03 result reference |

The activities carry the retry policy of the kit; the two named exceptions are non-retryable and end the run. The workflow has no timer, no signal, no child workflow and no Schedule.

#### 12.6 Schedules

None. JOB-08 is an event-started workflow and this contract declares no Schedule ID, no cadence and no catch-up window (DP-10). Architecture v5 slide 44 lists JOB-08 as `Airflow: ACE data ready`, owner rwb-payment, event-triggered workflow; the accepted split keeps the mechanism and moves the owner to rwb-integration, and the conflict is carried (GAP-0658; ASM-1121). The `job_catalog` row of JOB-08 is the only catalogue trace and is written by RWB-P2-E2007-OPS.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| interface_config | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | Read only by this key; the outbound interface register of the service |
| outbound_item | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | Not used by this key; named so that the service's table set is closed |
| job_catalog | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | One row for JOB-08: job_id, job_name, owner_role, the event trigger as schedule_text, runbook_path, expected_minutes, alert_after_minutes, first_release |
| decision_record | `rwb_integration` | PLT library, created in `rwb_integration` (DP-03) | The local record of each outcome, with the fired row and the package version |
| outbox_event, outbox_delivery, processed_event, idempotency_key | `rwb_integration` | PLT library, created in `rwb_integration` (DP-09) | The record's outbox row, the inbox of the two events and the run's idempotency record |

No treatment table, no case table, no account table and no task table is owned, read or copied: the treatment comes through RWB-P3-E2004-CON, the task and the case through the rwb-case contracts, and the account and batch facts through the rwb-source-data contract (DP-01, BR3). The Ownership Map ruling on `job_catalog` stands: each service's Schedules are not rows of a shared table, so this row exists for the job catalogue and the alerts, not to drive the run.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment WireMock | The approved-not-booked list with `TRT-SYN-0701` to `TRT-SYN-0704`; the treatments APPROVED and BOOKED with booked at 2026-12-16; the mark-booked write accepted once per treatment and date and answering 200 unchanged on a repeat; the difference write; one unavailable answer for AC8 | App story, contract tests |
| rwb-source-data WireMock | The ALS batch 2026-12-16 COMPLETED and 2026-12-17 FAILED with MSG-P1-001 on the batch status answer; accounts `A-0701` to `A-0705` with the booked terms; the reconciliation write accepted; one slow answer beyond 2 s | App story, contract tests |
| rwb-case WireMock | `raiseTask` accepting the three task codes and returning the open task on a repeat; the treatment-type and task-code LOV rows; the grace parameter = 1; one refusal of an unknown task code with MSG-GEN-001 | App story, contract tests |
| rwb-decision WireMock and kit stub | Package `BOOKING_MATCH` version `BKG-2026.12` with its RESTRUCTURE and SETTLEMENT rows and checksum; `NoPackageInForce` for 2026-12-17; one checksum mismatch | App story, contract tests |
| rwb-access WireMock | Platform administration U granted to RW-PLATADM, refused to RW-CASEOWN with MSG-P4-002, and a job absent from the catalogue answered 404 with MSG-P4-003 | App story, contract tests |
| Decision-record library stub | A committed record with its outbox row, and a stopped store that must leave the treatment fake uncalled | App story, contract tests |
| Inbox and idempotency stub | A duplicate `AceDataReady` and a duplicate `TreatmentApproved` dropped, and the treatment-and-date record of a repeat run | App story, contract tests |

Each fake is generated from the owning service's published OpenAPI or AsyncAPI document where one exists, and the drift test fails when a fake answers a shape or an error this document does not declare.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 12 consumed | The rerun provided; the treatment list, the treatment read, the mark-booked write, the difference write, the case-account read, the freshness answer, the reconciliation write, the task raise, the reference-data read, the parameters read, the rule-model read and the authorise call consumed; one hop, 2 s timeout |
| Kafka | None published by own work, 1 published by the library, 2 consumed | `DecisionRecorded` by the library on `rwb.decision-record.v1`; `AceDataReady` and `TreatmentApproved` consumed; `TreatmentBooked` documented as another service's envelope and neither published nor consumed here |
| Temporal | 1 workflow, 6 activities, no Schedule | `BookingMatchWorkflow` with its six activities on `rwb-integration`; JOB-08 is event-started |
| File | None | This contract names no file; the Workbench loads no ALS file and no lake file exists (DP-17) |

### 13. Solution plan

**Deliverables.** `contract/booking-confirmation-openapi.yaml` (the rerun operation and the job catalogue change), `contract/booking-confirmation-result.yaml` (the run input, the facts element set and the result shape), `contract/booking-confirmation-consumed.yaml` (the twelve consumed paths and operations with the 2 s budget and the placeholders), `contract/booking-confirmation-workflow.yaml` (the workflow, the six activities and the two non-retryable outcomes), `contract/booking-confirmation-split.md` (the ownership split, the task table, the envelope statement and the supersession note), and seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit types; the registry read through rwb-decision; no second engine | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read: the accounts and the batch answer come through rwb-source-data | none |
| DP-06 | Parameters, casewf.config | The parameters contract of rwb-case for the grace count | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | The reference-data contract of rwb-case for the treatment types and task codes | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; CloudEvents; the service topic of the owner | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The event-started workflow through the workflow kit; no Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-14 and SCR-01 | H RWB-PLT-N001-CON |

**Build steps**

1. Write the OpenAPI document of the rerun operation, with the input, the answer, the five errors and the idempotency; AC4, AC6.
2. Write the result document: the run input, the facts element set, the outcome enumeration and the refusal rule; AC1.
3. Write the task table and the two message parameter sets; AC2.
4. Write the envelope statement and the split note, including the JOB-08 ownership conflict and the TSD P2 v3 T5.2 supersession; AC3, AC4, AC5 (GAP-0658; ASM-1121; ASM-1123).
5. Write the consumed document: twelve paths and operations, their owner, their use, the 2 s budget and the placeholder on each unsettled path; AC5.
6. Write the workflow contract with the six activities and the two non-retryable outcomes; AC4.
7. Write the table section: the three tables, the JOB-08 row and the library tables, with the absence rule for the other services' data; AC6.
8. Build the seven fake sets and their fixtures.
9. Add the contract tests, including the drift test between each fake and this document, the message map and the check that the old monolith base appears nowhere, and a contract test that fails on any outcome-shaped field of the account read (GAP-0598).
10. Tag the baseline and collect the sign-off of the app story, the operations story, the case transition story, the treatment slice and the harness.

**Done when.** The contract files validate in the pipeline, the contract tests pass, the seven fakes answer every consumed path and operation, the message map covers the ten messages, and the app, operations, case transition, treatment and harness stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ACE batch late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision record write failed, or the decision log store is unavailable | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No BOOKING_MATCH version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-001 | No session on the rerun | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The job is absent from the catalogue, or the case is outside the scope | This case is not in your scope. |
| MSG-GEN-001 | A required value is missing, or a task code is outside the table | Enter {field}. |
| MSG-GEN-006 | A consumed contract did not answer, or the result is out of contract | {system} is not available. Try again in a few minutes. |

The texts are the legacy texts and the platform catalogue texts, unchanged, except MSG-P1-001, MSG-P2-006, MSG-P2-011, MSG-P3-027 and MSG-GEN-006, which take the Error and Message Standard v4 wording (CG-ALL-3148, CG-ALL-3149, CG-ALL-3150, CG-ALL-3151, DOR-RWB-P2-E2007-CON-9). For MSG-P3-027 the `{table}` value is the package code BOOKING_MATCH and the `{check}` value is "no package in force". For MSG-P4-002 `{action}` names the action tried and never a case fact. The operation or outcome that raises each message is named in sections 12.1, 12.2 and 12.3; MSG-P2-011 and MSG-P2-012 are carried by the task row and never returned as a problem body. The rerun under `Idempotency-Key` is served for the jobs of this service's catalogue only (GAP-0658; ASM-1122).

### 15. Screens and states

None in this story. The contract supplies the values behind SCR-14 Treatment record and SCR-01 My work, which gateway-bff composes from rwb-case, rwb-treatment and rwb-access (DP-19); it renders no page, holds no screen state of its own and declares no screen field. The SCR-01 My work states are empty and loading, per Screen Specifications v1; error and no access are Not specified in the source documents (CG-ALL-3156). The operator surface of the run is the job catalogue read of the integration base and the run summary, deployed and alerted by RWB-P2-E2007-OPS. The screen fields, the masking and the composite route of SCR-14 and SCR-01 are Not specified in the source documents (GAP-0658; ASM-1123). The SCR-14 Treatment record states are empty, loading, error and no access; Screen Specifications v1 gives none of them, so each is Not specified in the source documents (CG-ALL-3157).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2007-CON-01 | AC1 | Contract | The result against the schema: the three outcomes, a fired row and a version; a result with a missing row, a missing version and an unknown outcome is refused |
| TC-P2-E2007-CON-02 | AC2 | Contract | The three task codes with their roles, messages and parameters; a fourth code refused; the one-open-task rule declared; package version `BKG-2026.12`, tolerance 0.00 baht and the grace parameter of 1 unchanged |
| TC-P2-E2007-CON-03 | AC3 | Contract | The `TreatmentBooked` envelope with owner, topic, key and payload; the statement that this service neither publishes nor consumes it; the two service events |
| TC-P2-E2007-CON-04 | AC4 | Contract | The rerun operation with its right, errors and idempotency; the `BookingMatchWorkflow` row; the event-started workflow and the absence of a Schedule; the run zone, the one-run rule, the gate retry and the flag-off stop |
| TC-P2-E2007-CON-05 | AC5 | Contract | The twelve consumed operations with owner, use and the 2 s budget; the five placeholders; the ACE-read boundary statement; the cache key and the version-keyed drop |
| TC-P2-E2007-CON-06 | AC6 | Component | The nine sub-tables present; 12.7 with the three tables and the library only; the seven fakes matching; the ten messages mapped; the added platform and consumed rows named; the decision record written before any remote call, with no call on a failed write; no data lake and no lake file |
| TC-P2-E2007-CON-07 | AC6 | Component | Boundary of the 12.7 tables: this key writes one job_catalog row, for `BookingMatchWorkflow`; no treatment, case, account or task row exists in rwb_integration |
| TC-P2-E2007-CON-08 | AC7 | Contract | Trace of BR1 to BR14 to an AC, a test or a guardrail; proposed test Not specified in the source documents (NEWAC-RWB-P2-E2007-CON-AC10) |
| TC-P2-E2007-CON-09 | AC8 | Contract | Retry count, backoff and timeout of each `BookingMatchWorkflow` activity; Not specified in the source documents (NEWAC-RWB-P2-E2007-CON-AC11) |

### 17. Guardrails

- No business value in the contract: the compared terms, the tolerance, the grace count, the treatment types and the task codes are rows of the registry, parameters and reference data of their owners.
- No personal data in an answer, an event, an activity input, an example or a fake: case IDs, treatment IDs, account keys, role codes, rule IDs, version labels and dates only.
- The contract names only rwb-integration operations as provided; the treatment, the account, the task, the package and the authorise operations are consumed and never restated as this service's (DP-01, DP-13).
- Only rwb-source-data reads the `recovery.v_ace_*` views; a document that names a view read here, or a grant on `recovery`, fails the review (DP-05, BR4; GAP-0658; ASM-1123).
- One base, one queue and one namespace: a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- No second rule engine and no rule table: the kit's types and the version-in-force check are used (DP-04, BR2).
- No Schedule: JOB-08 is event-started, and a document that invents a Schedule ID or a cadence fails the review (BR5).
- `TreatmentBooked` is never published here, and the service publishes no business event of its own for this key (BR9).
- Every example and fixture is synthetic; no production case number, account number or rule row is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load | The result shape, the task table, the envelope statement and the rerun | TC-P2-E2007-CON-01, TC-P2-E2007-CON-02, TC-P2-E2007-CON-03 |
| REC-03 | Approved treatments against bookings, zero after two days | The reconciliation write and the run summary of the workflow | TC-P2-E2007-CON-04, TC-P2-E2007-CON-05 |
| ADR-010 | Only rwb-source-data reads the ACE views and ACE data | The ACE-read boundary of BR4 and the consumed case-account and freshness operations | TC-P2-E2007-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The twelve consumed operations with the 2 s budget | TC-P2-E2007-CON-05 |
| D-RCV-60 | The split of the legacy key into a service contract, an app story and an operations story | The rerun, the result shape, the task table and the split note | TC-P2-E2007-CON-01, TC-P2-E2007-CON-04 |

The requirement ID is the legacy one; this contract adds none of its own, and the rule row identifiers of package BOOKING_MATCH stay in the registry, which is rwb-decision's (GAP-0658; ASM-1125).

### 19. Out of scope

- The implementation of the workflow, the facts builder, the four clients and the rerun (RWB-P2-E2007-APP).
- The deployment of the worker, the JOB-08 registration, the chart, the alerts, the dashboards and the runbook (RWB-P2-E2007-OPS).
- The treatment record, the mark-booked state, `booked_at` and the booking difference (the S2 story of this legacy key, behind RWB-P3-E2004-CON).
- The case route state, the task rows, the timeline and the case-side record (RWB-P3-E2007-APP).
- The ACE account and batch-status reads, the freshness product and the reconciliation answer (RWB-P1-E2007-APP and RWB-P1-E1069-APP).
- The BOOKING_MATCH rows, the package authoring, the approval, the rollback and the registry (RWB-P7-E2007-APP, RWB-E2-042 and RWB-E1-073).
- The authorise contract and the role rows behind the rerun refusal (RWB-P4-E2007-APP, RWB-P4-E1037-CON).
- The real cross-service proof of the journey (RWB-ITG-E2007-ITG).
- The platform envelopes, the workflow kit, the naming library and the Kafka topic provisioning (RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The field-level detail of the five unsettled consumed paths and shapes (GAP-0658).
