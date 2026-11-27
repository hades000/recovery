# RWB-S2-E2018-APP E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: treatment slice of legacy RWB-E2-018 for rwb-treatment (S2). The key is split three ways: the circuit — the signature basis of the template, the conduct check, the send to EasyApp on INT-34, the retry and the exception queue — and the eleven legacy criteria are `RWB-P6-E2018-APP`'s; the signature request row and the signed copy are `RWB-P5-E2018-APP`'s; this story owns the treatment signature record and its state machine, which the P6 story records only through the published treatment contract. New here: DP-01 own schema, DP-13 the new base, DP-11 the published update operation with a mock, DP-05 the party rows, DP-07 the two lists, DP-09 the outbox, DP-10 the stage timer, DP-15 the five columns and DP-19 the composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E2018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 30 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S2-G |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S2-E2018-APP-16) |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON (wave-0 platform release train prerequisites) |
| Contract dependencies | RWB-S2-E3001-CON and RWB-S2-E3002-CON (additive signature properties of TreatmentUpdate and Treatment), and RWB-P3-E1043-CON (DP-07 reference-data contract of rwb-case) |
| Contract version | v1 on base /api/recovery/treatment/v1 (DP-13) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-OCC-009) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **RW-RESTRUCT restructuring officer (FCR)**, I want **the treatment to hold its own signature record — whether the customer signed or did not, by which method and when, against which request reference, and until when the window was open — and to report that outcome to the case**, so that **the case that routes to booking is the one that knows how its agreement was signed, and no signature result is lost between the provider and the booking queue**.

This is the treatment-side slice of legacy RWB-E2-018. It owns:

- the signature record on the `treatment` row: DF-TRT-030 `signature_status` of TSD S2 T3.2 (PENDING, SIGNED, NOT_SIGNED) with the method, the provider's request reference and the three times, in five nullable columns this story's Flyway version adds (DP-15; no source field carries them — GAP-2699; ASM-4470);
- the idempotent apply step: a record keyed on the provider's reference and the outcome writes the row change and one outbox row in the same transaction, so a retried record from the P6 story writes once (DP-09; R-UNI-40; legacy BR8);
- the published record and read of the treatment as the seam: the additive signature properties of `TreatmentUpdate` and of the `Treatment` answer on base `/api/recovery/treatment/v1` (DP-13), which the P6 story calls one hop with a 2 s timeout against a fake (DP-11);
- the two lists the record is checked against at their version — LOV-SIGN-METHOD and LOV-TRT-SIGNATURE — read through the reference-data contract (DP-07), so no method and no status is a constant;
- the check that the party the record names is a party of the case, read from the service's own read-only `v_ace_customer` view (DP-05);
- the closure of the window: when the stage's offer-validity timer reaches `valid_until`, the row is NOT_SIGNED with reason OFFER_EXPIRED, the closure is announced once, and a later record is refused (DP-10; legacy BR5);
- the two events `rwb.treatment.SignatureRecorded.v1` and `rwb.treatment.SignatureWindowClosed.v1` on `rwb.treatment.events.v1`, which the parent `CaseWorkflow` routes on for R-RES-16, R-RES-17, R-RES-18, R-SET-10 and R-SET-11 (DP-09);
- the state SCR-14 shows through the gateway-bff composite route (DP-19).

It does not own: the signature basis of the template, the conduct check, the send to EasyApp, the retry limit 5 and the exception queue, which are `RWB-P6-E2018-APP`'s and rwb-comms'; the signature request row `signature_request`, the five request statuses, the bank signature, the signed PDF as a write-once version and the 60-second store target, which are `RWB-P5-E2018-APP`'s and rwb-document's; the offer, its validity rule and the send, which are RWB-S2-E3007-APP; the routing to operations and the return to the prior status, which are RWB-S2-E3008-APP and RWB-S2-E3009-APP; the case status, which is rwb-case's; and the read and update elements themselves, which are RWB-S2-E3001-CON's and RWB-S2-E3002-CON's.

### 2. Business rationale

Agreements are printed, signed and couriered today, and the case waits days for the signed copy before booking can start. The legacy story answers that by sending the generated agreement for e-signature where Legal permits it and taking branch and paper signatures where Legal requires wet ink, then recording signed or not signed on the treatment — the fact that R-RES-16, R-SET-10, R-RES-17, R-RES-18 and R-DIL-18 act on (REQ-OCC-009).

In the monolith the treatment row, the signature request row and the document version sat in one `recovery` schema, and the communications module wrote the treatment through an in-process `TreatmentApi.recordSignature`. In the target the three facts have three owners and the write crosses a boundary:

- the treatment and its signature state are S2's own row in `rwb_treatment`, and DF-TRT-030 is written by this service and by nothing else (DP-01);
- the request, its five statuses and the signed copy are rows of `rwb_document` that this service never reads; the only trace of a signature here is the provider's reference, the method and the three times (legacy BR7; CTL-12, DT06);
- the basis check, the conduct check and the EasyApp leg are rwb-comms' and reach this service only as a record on the published operation, one hop with a mock, so the flow builds on Day 1 without a treatment table and the treatment builds on Day 1 without a provider (DP-11; GAP-1183; ASM-2130);
- the window is the treatment's own offer validity, so the closure is the treatment's fact and not a case announcement, and the case hears the outcome rather than the intent (DP-10; legacy BR5);
- the method and the status are lists in force, so a change of vocabulary is a data row and not a build (DP-07).

Serves REQ-OCC-009. No business value is invented: the methods E_SIGNATURE, BRANCH and PAPER, the statuses PENDING, SIGNED and NOT_SIGNED, the values signed true and false, the messages MSG-P3-005 and MSG-P4-002, the request reference "EA-30001" and the times are the values the legacy story, TSD S2 T3.2 and the reference-data contract already carry.

### 3. Preconditions

- Treatment "T-0501" exists in `rwb_treatment` with type SETTLEMENT, `valid_until` 2026-12-20 and state OFFER_WITH_CUSTOMER_SET, or "T-0502" with type DEED_IN_LIEU for product MORTGAGE, built by RWB-S2-E3001-APP and sent by RWB-S2-E3007-APP.
- The additive signature properties of `TreatmentUpdate` and of the `Treatment` answer are published on base `/api/recovery/treatment/v1` by RWB-S2-E3001-CON and RWB-S2-E3002-CON with their error set and fakes (GAP-2699; ASM-4470). The exact operation and field names the caller consumes are Not specified in the source documents (GAP-1183; ASM-2130).
- `RWB-P6-E2018-APP` is built against this operation and its fake: it answers the signature basis of the agreement's template, the conduct check, the EasyApp leg and the signed copy, and calls the record with the legacy values signed true or false, method E_SIGNATURE, BRANCH or PAPER, the signed-at time and its request reference.
- The reference-data contract and client library of rwb-case are reachable (DP-07), carrying LOV-SIGN-METHOD with E_SIGNATURE, BRANCH and PAPER and LOV-TRT-SIGNATURE with PENDING, SIGNED and NOT_SIGNED; the operation names are Not specified in the source documents (GAP-2699; ASM-4472).
- `v_ace_customer` is readable by the login of rwb-treatment with SELECT only and carries the party rows of the case, so party "P-0088" is known to belong to case "RC-2026-000888" (DP-05; ASM-4475).
- The offer-validity timer of the stage is started by RWB-S2-E3007-APP at send and reaches `valid_until`; this story supplies the closure activity the timer invokes and registers no Schedule of its own (DP-10; ASM-4474).
- The outbox library, the workflow kit, the per-service Flyway sequence and the gateway-bff composite route are the service template's wave-0 capability and add no build row of this story (ASM-4473).
- No approval is needed to build against a Draft contract baseline, and this story holds no H dependency, so it starts on Day 1 (§R5.7).

### 4. Flow

1. RWB-S2-E3007-APP sends the treatment to the customer under R-RES-11 and sets `valid_until`; in the same transaction the stage opens the window: `signature_status` PENDING, the method the officer chose, the send time and the expiry copied from `valid_until`, and the durable timer is started (DP-10, DP-15).
2. `RWB-P6-E2018-APP` checks the basis of the agreement's template, runs the conduct check and sends the agreement to EasyApp; the treatment is told nothing until there is a result (BR6; legacy AC4 and AC7 are P6's).
3. The signature flow reads the treatment once through `GET /treatments/{treatmentId}` for its type, offer validity and state; a treatment that is not with the customer is refused with 409 and MSG-P3-005 at the source (DP-11).
4. A result arrives on the published record: `PATCH /treatments/{treatmentId}` with signed true or false, method E_SIGNATURE, BRANCH or PAPER, signedAt 2026-12-11 10:15:00 and the request reference "EA-30001".
5. `SignatureRecordApplier` checks the request reference against the row, the method against LOV-SIGN-METHOD, the status against LOV-TRT-SIGNATURE, the party against `v_ace_customer` and the state against the open window (DP-05, DP-07).
6. In one `rwb_treatment` transaction it writes `signature_status`, `signature_method`, `signature_signed_at`, the standard `updated_at`, `updated_by` and `version`, the idempotency row and the outbox row of `rwb.treatment.SignatureRecorded.v1` (DP-09; R-UNI-40).
7. The stage reports the outcome to the parent `CaseWorkflow` — signed with the method, or not signed with the reason — and the parent moves the case under R-RES-16 or R-SET-10 for a signature, R-RES-17 or R-RES-18 for a decline or an expiry, and R-DIL-18 to WITH_FIELD_INSPECTION where the agreement's basis is wet ink on a mortgage deed in lieu. This service writes no case table (ASM-4474).
8. The stage's timer reaches `valid_until`. If no record has been applied, `closeSignatureWindow` writes NOT_SIGNED with reason OFFER_EXPIRED, publishes `rwb.treatment.SignatureWindowClosed.v1` once, and the signature flow closes its request; a later record finds the window closed and is refused with 409 and MSG-P3-005 (legacy AC6; R-RES-18, R-SET-11).
9. A repeat of the same record for the same reference and outcome is answered from the first row and writes nothing new; the repeat is counted under R-UNI-40 (legacy AC9, BR8).
10. SCR-14 shows the status, the method and the signed time from this service, merged by the gateway-bff composite route with the document read of rwb-document that carries the signed copy; SCR-30 shows the signed copy against the generated agreement and SCR-09 lists what the signature flow held (DP-19; legacy section 15). Screen states: SCR-14 no access is the 403 with MSG-P4-002 of AC8; the empty, loading and error states of SCR-09, SCR-14 and SCR-30, and the no access state of SCR-09 and SCR-30: Not specified in the source documents (DOR-RWB-S2-E2018-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record names a method outside LOV-SIGN-METHOD, or a status outside LOV-TRT-SIGNATURE | Refused before any write, with the field named | MSG-GEN-001 | AC1 |
| X2 | The record names a party that is not a party of the case | Refused; the row is unchanged | MSG-GEN-001 | AC1 |
| X3 | The record names a reference the row does not hold | 404 with the problem body; nothing is written, published or stored | MSG-P4-003 | AC6 |
| X4 | The record arrives for a treatment that is not with the customer, or after the window closed | 409 with the problem body; the row keeps every column it had | MSG-P3-005 | AC4, AC6 |
| X5 | A result is DECLINED | The row moves to NOT_SIGNED with the method and no signed time, and one event is published | None | AC3 |
| X6 | The offer validity passes with no record applied | The timer closes the window: NOT_SIGNED with reason OFFER_EXPIRED, one closure event, and a later record is refused | MSG-P3-005 | AC4 |
| X7 | The same record arrives twice, or the caller retries after a timeout | The first state is answered; nothing second is written; the repeat is counted | None | AC5 |
| X8 | The record fails after the signed version was already stored by rwb-document | Nothing is written here and the caller retries from the same result; the write key makes the retry write once | None | AC2, AC5 |
| X9 | The caller holds no Treatment and offer U, or the case lies outside its scope | 403 or 404 before any write | MSG-P4-002, MSG-P4-003 | AC8 |
| X10 | A statement reaches `rwb_document`, `rwb_comms`, `rwb_case` or a `v_ace_*` view | The grant refuses it and the boundary test fails the build | None (pipeline log) | AC9, AC10 |

X1 to X3 are the record's own validation, X4 is the treatment's guard, X5 and X6 are the legacy decline and expiry carried onto the record, X7 and X8 are R-UNI-40 and X10 of the P6 story across the seam, X9 is the guard's answer and X10 the boundary rule of the target. Nothing is written before a record is accepted, and the only path that writes and then rolls back is a failure of the row write or of the outbox row, which is one transaction.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the treatment record and read fakes, the reference-data fake, the P6 and composite-route fakes and a `v_ace_customer` fixture; needs no live rwb-comms, rwb-document, rwb-case or rwb-decision |
| Negotiable | The activity names, the column names and the event payloads are this story's design; the methods, the statuses, the messages, the rules and the two case outcomes are values in force |
| Valuable | The treatment carries its own signature outcome, so the case routes on a fact its owner wrote rather than on a provider callback, and a retried record still writes once |
| Estimable | Two additive property sets, one applier, one closure activity, one view and two events |
| Small | Fits two weeks with its tests, as a treatment slice of a legacy split three ways |
| Testable | Each of the eight criteria is one automated test on the fakes and the view fixture, plus the twelve legacy cases as they stay with the P6 slice |

### 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank — the rwb-treatment signature record

  Background:
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20 and state "OFFER_WITH_CUSTOMER_SET"
    Given case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE"
    Given the borrower is party "P-0088" and is a party of both cases
    Given a restructuring officer "RS-0301" with role RW-RESTRUCT in scope of both cases

  Scenario: AC1 The record writes the method, the time and the reference, and its values are checked against the lists and the case (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns LOV-SIGN-METHOD with "E_SIGNATURE", "BRANCH" and "PAPER" and LOV-TRT-SIGNATURE with "PENDING", "SIGNED" and "NOT_SIGNED"
    Given "T-0501" holds signature_status "SENT" and request reference "EA-30001"
    When the record for "T-0501" arrives with signed true, method "E_SIGNATURE", signedAt 2026-12-11 10:15:00 and reference "EA-30001"
    Then signature_status is "SIGNED", signature_method "E_SIGNATURE" and signature_signed_at 2026-12-11 10:15:00 on the treatment row
    Then GET /treatments/{treatmentId} serves the same three values for "T-0501"
    Then a record with method "COURIER" is refused with 422 and MSG-GEN-001 naming "method", and a record for party "P-9999" is refused with 422 and MSG-GEN-001 naming "party", each with the row unchanged

  Scenario: AC2 The record and its event are one transaction, and a failed write moves nothing (new, D-RCV-60)
    Given the record for "T-0501" with signed true and method "E_SIGNATURE" is accepted
    When it is applied
    Then the row change, the idempotency row and the outbox row of rwb.treatment.SignatureRecorded.v1 are written in one rwb_treatment transaction
    Then a forced failure of the row write or of the outbox row leaves none of the three in rwb_treatment
    Then the signed copy "D-0601" version 2 that rwb-document already stored stays where it is and this service reads no byte of it

  Scenario: AC3 A decline and a wet ink paper result record NOT_SIGNED and SIGNED with their method (new, D-RCV-60)
    Given the record for "T-0501" arrives with signed false and method "E_SIGNATURE" on 2026-12-11
    When it is applied
    Then signature_status is "NOT_SIGNED" and signature_signed_at is empty
    Then the event rwb.treatment.SignatureRecorded.v1 carries signatureStatus "NOT_SIGNED" and no signed time
    Given the record for "T-0502" arrives with signed true, method "PAPER" and signedAt 2026-12-14
    When it is applied
    Then signature_status is "SIGNED", signature_method "PAPER" and signature_signed_at 2026-12-14
    Then the stage reports the outcome with the method "PAPER" to the parent CaseWorkflow, which routes under R-DIL-18 to the field inspection, and this service writes no case table

  Scenario: AC4 The offer validity closes the window and a later record changes nothing (new, D-RCV-60)
    Given "T-0501" holds signature_status "SENT" with expiry 2026-12-20
    When the stage's validity timer fires for "T-0501"
    Then signature_status is "NOT_SIGNED" and the closure is recorded with the time the timer fired
    Then exactly one event rwb.treatment.SignatureWindowClosed.v1 is published with reasonCode "OFFER_EXPIRED"
    Given a record for "T-0501" arrives on 2026-12-21 with signed true
    When that record is applied after the closure
    Then the answer is 409 with MSG-P3-005, signature_status stays "NOT_SIGNED" and no second event is published
    Then the row keeps every column it had and the result is held on the exception queue of the signature flow, not here

  Scenario: AC5 A repeated record writes once and is counted (new, D-RCV-60)
    Given the record for "T-0501" with reference "EA-30001" and signed true was applied at 2026-12-11 10:15:00
    When the same record for "EA-30001" arrives again, or the activity is replayed after a worker restart
    Then the row keeps signature_status "SIGNED" and 2026-12-11 10:15:00 and no second change is written
    Then exactly one outbox row of rwb.treatment.SignatureRecorded.v1 exists for "T-0501" and "EA-30001"
    Then the repeat is counted under R-UNI-40 and answered 200 with the first state

  Scenario: AC6 An unknown reference or a treatment not with the customer writes nothing (new, D-RCV-60)
    Given no treatment row holds request reference "EA-99999"
    When a record for "EA-99999" arrives
    Then the answer is 404 with MSG-P4-003 and nothing is written, published or stored
    Given treatment "T-0503" of the case is in state "DRAFT"
    When a record for "T-0503" arrives
    Then the answer is 409 with MSG-P3-005 and signature_status is unchanged
    Then no event is published on either path and no column of either row changes

  Scenario: AC7 The signature state shows on SCR-14 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-14 Treatment record for case "RC-2026-000888"
    Given treatment "T-0501" holds signature_status "SIGNED", signature_method "E_SIGNATURE" and signature_signed_at 2026-12-11 10:15:00
    When the officer opens SCR-14
    Then SCR-14 shows "SIGNED", the method "E_SIGNATURE" and the signed time, read from this service
    Then the signed copy "D-0601" version 2 is shown from the document read of rwb-document, merged by the route
    Then the browser calls no owner service directly, and this service serves no document byte and no exception-queue entry

  Scenario: AC8 The guard refuses a role without the right and no personal value is written, published or logged (new, D-RCV-60)
    Given a user with role "RW-PHONECOL" holds no Treatment and offer right on the record operation
    When the record for "T-0501" arrives
    Then the answer is 403 with MSG-P4-002 and nothing is written
    Given the record for party "P-0088" is applied
    Then the row, the two events and every log line carry the case ID, the treatment ID, the party KEY "P-0088", the method code, the status code, the request reference and the times
    Then no name, no national ID number, no signature image and no PDF byte appears in any of them, and the profile codec is on every payload

  Scenario: AC9 A statement that reaches another schema or a v_ace view is refused and fails the build (new, D-RCV-60)
    Given the grant of rwb_treatment refuses every table of rwb_document, rwb_comms and rwb_case and every v_ace_* view other than v_ace_customer
    When a statement of this service names one of those tables or views
    Then the grant refuses the statement, the boundary test fails the build and the failure is written to the pipeline log

  Scenario: AC10 The grant refuses a statement that names a table of rwb_comms and the build fails (new, D-RCV-60)
    Given the grant of rwb_treatment refuses the table "template" of rwb_comms
    When a statement of this service names "template"
    Then the grant refuses the statement, the boundary test fails the build and the pipeline log names the object

  Scenario: AC11 The method, reason and expiry values are data rows and the case status is not written here (new, D-RCV-60)
    Given the method list, the reason code and the offer expiry are rows read at their version
    When a list version changes in the data with no code change
    Then the next record is checked against the new rows and the code is unchanged
    Given a statement of this service names a table of rwb_case that holds the case status
    When the statement is run
    Then the grant refuses it and the case status stays with rwb-case

  Scenario: AC12 A call without a valid credential is answered 401 on each provided operation and nothing is written (new, D-RCV-60)
    Given a caller presents no valid credential
    When it calls PATCH /treatments/{treatmentId} or GET /treatments/{treatmentId}
    Then the answer is 401 and nothing is written, published or stored

  Scenario: AC13 A retried or timed-out activity answers the first state and writes nothing second (new, D-RCV-60)
    Given the record for "T-0501" with reference "EA-30001" and signed true was applied at 2026-12-11 10:15:00
    When the activity that records it times out after Not specified in the source documents (NEWAC-RWB-S2-E2018-APP-AC15) and is retried
    Then the answer is the first state, signature_status stays "SIGNED" and no second row or outbox row is written
```

The thirteen criteria are new under D-RCV-60 and test only the S2 deliverable of this story: the record with its checks, its one transaction, the decline and the wet ink case, the closure, the repeat, the two refusals, the screen, the data boundary (ASM-4469), the lists as data and no case write, the unauthenticated answer, and the retried or timed-out activity. The eleven legacy criteria AC1 to AC11 of RWB-E2-018 — Customer signs, Branch, DIL paper, E-signature refused where Legal requires wet ink, Customer declines, Offer validity passes with no signature, Contact stop, EasyApp path unavailable, Signing result repeated, Unknown request reference and Branch result without a scan — are copied word for word with their origin tags into `RWB-P6-E2018-APP`, which owns the circuit, and are not restated here; AC1, AC3, AC4 and AC5 of this story are the treatment consequence of the same events and not the flow itself. `RWB-P5-E2018-APP` owns the request row, its five statuses and the signed copy. The cross-service journey of one signature across rwb-comms, rwb-document, rwb-treatment and the ACE path is `RWB-ITG-E2018-ITG`'s and no criterion of this story claims it.

Three readings are stated here rather than hidden in code. TSD S2 T3.1 gives `treatment` DF-TRT-030 `signature_status` and no column for the method, the reference or the three times, so this story adds five nullable columns (GAP-2699; ASM-4470). The plan holds no rwb-treatment contract story for the P6 caller and no source names the operation a record arrives on, so the record rides on the additive properties of `TreatmentUpdate` over `PATCH /treatments/{treatmentId}` — the operation the Ownership Map gives — and the state is served on the read declared by RWB-S2-E3001-CON (GAP-2699, GAP-2700; ASM-4470, ASM-4471; GAP-1183). The legacy closes the request when P3 announces OFFER_EXPIRED and holds the treatment's own validity on the case side; the target keeps the validity on the treatment, so the window closes here and the case is told the outcome (GAP-2701; ASM-4474). Open decision DL10 stays open and is not decided here; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A signature record writes the treatment's own state and the values of the lists in force: signed true writes SIGNED with the method and the signed time, signed false writes NOT_SIGNED with the method and no signed time | Legacy RWB-E2-018 BR2, BR4; TSD S2 T3.2; DP-07 |
| BR2 | The record is accepted only for a treatment that is with the customer and inside its window; anything else is a refusal with the row untouched | Legacy X2, X3; AC4, AC6 |
| BR3 | A wet ink paper result is recorded with its method and is reported, so R-DIL-18 can route the mortgage deed in lieu to the collateral inspection before the transfer | Legacy BR3; R-DIL-18, R-DIL-27 |
| BR4 | The record is checked against LOV-SIGN-METHOD and LOV-TRT-SIGNATURE at their version and against the party rows of the case; no method, status or party value is a constant | Legacy BR1 and section 13; BR-S2-001; DP-05, DP-07 |
| BR5 | The window ends with the treatment's offer validity, and its closure writes NOT_SIGNED with reason OFFER_EXPIRED and announces the closure once | Legacy BR5; R-RES-18, R-SET-11 |
| BR6 | The basis check, the conduct check, the EasyApp send and the retry limit 5 are rwb-comms' and are not repeated here; this service records the result only | Legacy BR1, BR6, BR9; CTL-16, R-SET-12; R-UNI-33 |
| BR7 | The signed document is write-once on the case and stays in rwb-document; this service holds the provider's reference and never a byte, a version or a file | Legacy BR7; CTL-12, DT06; DP-01 |
| BR8 | The same record twice has one effect: the writer is keyed on the provider's reference and the outcome and answers the first state | Legacy BR8; R-UNI-40 |
| BR9 | This service reads no `signature_request`, `document`, `template` or `recovery_case` row and no `v_ace_*` view except its own, and its login holds no grant that would allow otherwise | DP-01; Architecture v5 slides 29 and 41; Ownership Map |
| BR10 | No value a business person may change is written in code: the method list, the reason code and the expiry are data rows read at their version; the status list LOV-TRT-SIGNATURE is a closed list (PENDING, SIGNED, NOT_SIGNED) and is not read as data | Legacy BR1 and section 17; BR-S2-001; DP-07 |
| BR11 | The case status stays rwb-case's: the stage reports the outcome and the parent moves the case, and this service writes no case table | DP-01; Architecture v5 slide 18; legacy section 9 |
| R-UNI-40 | A repeated request with the same key returns the first result and writes nothing new | Business Rules and Routing Logic v4 (R-UNI-40) |
| R-RES-18 | The case returns to its prior status when `signed = N` and the offer validity passed | Business Rules and Routing Logic v4 (R-RES-18); TSD S2 T4 |
| R-SET-11 | The case returns to the route when the settlement offer expires | Business Rules and Routing Logic v4 (R-SET-11); TSD S2 T4 |
| CTL-12 | A signed document is write-once and a new version never overwrites the one that was signed | Legacy RWB-E2-018 BR7; CTL-12 |

The rules hold in `rwb_treatment` as follows. BR1 is the writer's value map. BR2 and BR11 are the ordering: nothing opens a transaction until the reference, the state and the window have been accepted, and the case is the parent's. BR3 is the outcome report. BR4 is the two list reads and the view read. BR5 is the closure activity and its single event. BR6 is the boundary with rwb-comms. BR7 and BR9 are the grant, the type and the boundary test. BR8 is the write key. BR10 is the parameters and list reads.

### 9. State transitions

None of the rows below is a case status owned here: each is a change of this service's own record, and the case status the rules imply is reported to the parent `CaseWorkflow` (BR11; ASM-4474).

| From | Event | Condition | To |
|---|---|---|---|
| `signature_status` empty | The offer is sent to the customer | R-RES-11 fired | PENDING, with the method of the send and the expiry copied from `valid_until` |
| PENDING or SENT | A record with signed true | The reference matches, the method is in the list, the party belongs to the case, the treatment is with the customer, the window is open | SIGNED, with the method and the signed time |
| PENDING or SENT | A record with signed false | The same checks | NOT_SIGNED, with the method and no signed time |
| PENDING or SENT | The window timer reaches `valid_until` | No record applied | NOT_SIGNED, reason OFFER_EXPIRED |
| SIGNED or NOT_SIGNED | A further record for the same reference and outcome | The state is already written | Unchanged; the first state is answered |
| SIGNED or NOT_SIGNED | A record after the window closed | The closure is later than the record's own window | Unchanged; 409 with MSG-P3-005 |

DF-TRT-030 is read as PENDING, SIGNED and NOT_SIGNED because LOV-TRT-SIGNATURE of TSD S2 T3.2 holds exactly those three; the SENT value the stage uses before a record arrives is a stage state and is not a member of that list, so the column is written PENDING until the first record and the closure, and the stage's own state carries the wait (GAP-2699; ASM-4470). A re-sent treatment opens a new window from PENDING and keeps the earlier one only in the event history.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Treatment and offer CRUA in the TSD S2 T6.1 matrix: chooses the method at send and records a branch or paper result on cases in scope |
| RW-CASEOWN, case owner | Treatment and offer CRU: the same within scope |
| RW-SPECIAL, hardship and vulnerability specialist (CRU); RW-GUARANT, guarantee officer (CRU) | Read the signature state; record a result on their own cases as the matrix allows |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R) | Read the signature state and the method; write nothing |
| RW-LEGAL, Legal counsel | Sets the signature basis on the template version (Documents A, RWB-E1-034); reads the treatment state here and writes no treatment row |
| SY-CASEWF, the case workflow module (R) | Receives the outcome report and moves the case; calls no treatment write of its own |
| SY-RULES, the rules component (R) | Reads the treatment state the routing rules act on |
| The rwb-treatment service identity (login `rwb_treatment`, DP-02) | Writes the signature record, closes the window, writes the outbox rows and holds no grant on `rwb_document`, `rwb_comms`, `rwb_case` or a `v_ace_*` view other than `v_ace_customer` |
| rwb-access authorise check (DP-08) on every REST operation of this service | Each `PATCH` and `GET` on `/api/recovery/treatment/v1` is authorised through the rwb-access authorise check before the service runs; the check's operation name is Not specified in the source documents (DOR-RWB-S2-E2018-APP-6) |
| The `rwb_comms` service identity of `RWB-P6-E2018-APP` | Checks the basis, runs the conduct check, sends to EasyApp and calls the record with the legacy values; it writes no treatment row directly |
| CU-BORROW, customer (borrower) | Signs or declines in EasyApp, or signs at a branch; no Workbench login and no treatment write |
| No delegation of authority level applies | The treatment was approved before it was sent; this story records how it was signed |

No credential and no personal name appears in the row, the events or the logs. Where a person acts, the row carries a user identifier, never a name.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read: the treatment of the record |
| DF-TRT-002 | treatment (S2, `rwb_treatment`) | case_id | Read: the case identifier the events carry instead of any party name |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read: SETTLEMENT or DEED_IN_LIEU decides the outcome report |
| DF-TRT-010 | treatment (S2, `rwb_treatment`) | valid_until | Read: the end of the window, copied into `signature_expires_at` 2026-12-20 |
| DF-TRT-030 | treatment (S2, `rwb_treatment`) | signature_status | Write: PENDING, SIGNED or NOT_SIGNED, the values of LOV-TRT-SIGNATURE |
| No field ID | treatment (S2, `rwb_treatment`) | `signature_method`, `signature_request_ref`, `signature_sent_at`, `signature_signed_at`, `signature_expires_at` added by this story | Write: the method E_SIGNATURE, BRANCH or PAPER, the reference "EA-30001", the send time, the signed time 2026-12-11 10:15:00 and the window end (GAP-2699; ASM-4470) |
| DF-ACE-056 | v_ace_customer (P1 views, read only) | person_key | Read: the party rows of the case, to check that "P-0088" belongs to it; no name and no national ID number (DP-05; ASM-4475) |
| DF-DOC-096 to DF-DOC-107 | signature_request (P5, `rwb_document`) | all fields | Not read and not written: the request lives with the signature flow and only its reference reaches this row (BR7, BR9) |
| DF-DOC-004, DF-DOC-010, DF-DOC-011 | document (P5, `rwb_document`) | document_type, write_once, doc_version | Not read and not written: the signed version is the signature flow's and is chartered by the hub |
| DF-REF-068 | template (P6, `rwb_comms`) | signature_basis | Not read and not written here: the basis is the P6 story's and reaches the screens through its own answer |
| DF-CAS-001, DF-CAS-003 | recovery_case (P3, `rwb_case`) | id, product_group | Not read: the case identifier and the product group reach this service on the case signal and on the offer |
| Standard column | treatment (S2, `rwb_treatment`) | version, updated_at, updated_by | Write: move with each state change |
| idempotency_key | PLT library, created in `rwb_treatment` | the write key of the record | Write, once per reference and outcome |

Field IDs are those of TSD S2 T3.1, T3.2 and the Logical Data Model and Data Dictionary. **Five nullable columns and two indexes are added to `treatment`, and no table.** The five columns and the two indexes are not in LDM v9 or Data Classification v5 and are recorded here as this story's design (GAP-2699; ASM-4470). No foreign key leaves `rwb_treatment`: the provider reference is a value and not a key into `rwb_document`, and `case_id` is a cross reference (DP-01).

**No personal data.** The party key is the only identifier of a person that passes through this story. The signed PDF, the signature image, the name and the national ID number never enter `rwb_treatment`, are never logged and are never put on an event (CTL-11; ASM-4476).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story provides no operation of its own: it adds optional signature properties to two operations that RWB-S2-E3001-CON and RWB-S2-E3002-CON already declare, additively inside major version 1.

| ID | Method | Path | This story | Access | Idempotency |
|---|---|---|---|---|---|
| API-S2-003 | PATCH | `/treatments/{treatmentId}` | Adds the optional signature properties to `TreatmentUpdate`: signed, signatureStatus, signatureMethod, signatureRequestRef, signatureSignedAt, signatureExpiresAt; the declared operation, its error set and its fakes are RWB-S2-E3002-CON's | Treatment and offer U, scope applied, through the guard library | Not applicable in TSD S2 T-A.2 API-S2-003; the writer is idempotent on the reference and the outcome |
| API-S2-002 | GET | `/treatments/{treatmentId}` | Serves the same properties on the `Treatment` answer, read from `rwb_treatment`; declared by RWB-S2-E3001-CON; the caller's read of type, offer validity and state | Treatment and offer R, scope applied | Not applicable |

The errors remain those of the two declaring contracts: 401, 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-P3-005 for a treatment not with the customer and for a closed window, 422 with the validation body and MSG-GEN-001 naming the field, and 503 with MSG-GEN-006. Every added property is nullable, so a consumer that ignores them keeps working and a treatment with no signature answers empty values.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | the reference-data read of LOV-SIGN-METHOD, operation Not specified in the source documents (GAP-2699; ASM-4472) | P3 rwb-case (`RWB-P3-E1043-CON`) | The methods E_SIGNATURE, BRANCH and PAPER at their version, cached; a record naming another method is refused with 422 (DP-07) |
| GET | the reference-data read of LOV-TRT-SIGNATURE, operation Not specified in the source documents (GAP-2699; ASM-4472) | P3 rwb-case (`RWB-P3-E1043-CON`) | The statuses PENDING, SIGNED and NOT_SIGNED of TSD S2 T3.2 at their version; the writer refuses a value outside the list (DP-07) |

Both reads are one hop with a 2 s timeout and a breaker, and neither calls another service. A failed list read answers 503 with MSG-GEN-006 naming "Reference data"; no state change opens a transaction until both lists have answered.

#### 12.3 Events published

| Event | Topic | Shape | Written by |
|---|---|---|---|
| `rwb.treatment.SignatureRecorded.v1` | `rwb.treatment.events.v1` (DP-14) | CloudEvents 1.0, keyed by caseId; payload treatmentId, caseId, signatureStatus, signatureMethod, signatureRequestRef, signedAt; no name, no signature image, no PDF byte, no document version | The outbox row of the same `rwb_treatment` transaction as the state change (DP-09) |
| `rwb.treatment.SignatureWindowClosed.v1` | `rwb.treatment.events.v1` (DP-14) | The same envelope with reasonCode OFFER_EXPIRED, closedAt and no signedAt | The outbox row of the closure transaction |

Two event names are this story's design: the catalogues give rwb-treatment TreatmentApproved and TreatmentClosed and no source names a signature event, while the legacy raises CUSTOMER_SIGNED in P3 and the comms catalogue holds no signature event of its own (GAP-2699; ASM-4470). The parent `CaseWorkflow` of rwb-case listens to both for R-RES-16, R-RES-17, R-RES-18, R-SET-10 and R-SET-11, and the signature flow listens to the closure so it can shut the request without a second call.

#### 12.4 Events consumed

None. The record arrives on the published update operation, called by `RWB-P6-E2018-APP`, and the case signal is a Temporal signal the parent `CaseWorkflow` forwards into the running stage; this story holds no consumer group and writes no inbox row of its own. The inbox table of the platform library exists in `rwb_treatment` for the consumers the sibling stories add.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` | Named here as the stage the window runs in; built by RWB-S2-E3001-APP and unchanged by this slice |
| `openSignatureWindow` | Activity | `rwb-treatment` | The treatment and the method of the send in; the row at PENDING, the expiry and the outcome report out; runs in the send transaction of RWB-S2-E3007-APP |
| `recordSignatureResult` | Activity | `rwb-treatment` | The reference, signed true or false, the method and the time in; the row change, the idempotency row and the outbox row out; idempotent by the reference and the outcome |
| `closeSignatureWindow` | Activity, the timer callback | `rwb-treatment` | The treatment in; NOT_SIGNED with reason OFFER_EXPIRED and the closure event out |

The three activity names are this story's design and are fixed by no source document (GAP-2699; ASM-4470); `TreatmentWorkflow` is the design's own name. The catalog row names ROUTE_APPROVED with route R1 (restructure), R2 (settlement) or R3 (deed in lieu). Workflow ID form and duplicate-start policy: Not specified in the source documents (CG-ALL-8370).

#### 12.6 Schedules

None. The window is one durable timer of the stage and not a job: no row of the job map belongs to this capability, no cron entry, no Temporal Schedule and no event-started workflow is created or moved, and the send retry of the signature flow is that flow's. DP-10 is applied as the timer that RWB-S2-E3007-APP starts and the closure callback this story supplies; the legacy `JOB-11` outbox sender is the platform relay, not a schedule of this story (GAP-2701; ASM-4474).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Five nullable signature columns, a unique index on `signature_request_ref` and an index on `(signature_status, signature_expires_at)` added by this story's Flyway version; written by three activities and read by the treatment read |
| `outbox_event` | `rwb_treatment` | PLT library object | The `SignatureRecorded` and `SignatureWindowClosed` rows of the same transactions, relayed by the outbox sender (DP-09) |
| `idempotency_key` | `rwb_treatment` | PLT library object | The reference and the outcome of the record and the state it answers on a repeat |

Not owned and never read as a table or field: `signature_request`, `document`, `document_type`, `doc_version` (field of `document`) and `retention_rule` (P5, `rwb_document`), `template` and `merge_field` (P6, `rwb_comms`), `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` (P3, `rwb_case`), `decision_log_entry` (P7, `rwb_decision`) and every `v_ace_*` view except `v_ace_customer` (P1). No foreign key leaves the schema and no cross-schema join exists (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Treatment record and read fakes (`RWB-S2-E3001-CON`, `RWB-S2-E3002-CON`) | `PATCH /treatments/{treatmentId}` with the signature properties answered 200 with the `Treatment`; 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-P3-005, 422 with MSG-GEN-001 and the field, 503 with MSG-GEN-006; the read with the same properties | AC1 to AC8 |
| rwb-case reference-data fake (`RWB-P3-E1043-CON`) | LOV-SIGN-METHOD with E_SIGNATURE, BRANCH and PAPER and LOV-TRT-SIGNATURE with PENDING, SIGNED and NOT_SIGNED at their version; a delayed answer beyond 2 s | AC1, AC2, AC8 |
| `RWB-P6-E2018-APP` caller fake | The records of the legacy values: signed true with E_SIGNATURE at 2026-12-11 10:15:00 for "EA-30001"; signed true with BRANCH; signed true with PAPER on 2026-12-14 for "T-0502"; signed false for "T-0501"; the same record twice; a record for "EA-99999" | AC1, AC3, AC5, AC6 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 answer for "RC-2026-000888": this service's treatment read once and the document read of rwb-document once | AC7 |
| rwb-source-data contract fake (`v_ace_customer` parties) | The parties of "RC-2026-000888" including "P-0088", with no name and no national ID number, and a second case whose parties do not include "P-0088" | AC1, AC8 |
| outbox, idempotency and timer doubles | One outbox row per committed transaction; a repeat answered from the first row; a timer fired at a given instant | AC2, AC4, AC5 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and a published contract is a build failure of the contract story that owns it.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided (additive), 2 consumed | `PATCH /treatments/{treatmentId}` and `GET /treatments/{treatmentId}` on `/api/recovery/treatment/v1`, adding and serving the signature properties; the two reference-data reads of `RWB-P3-E1043-CON`, one hop and 2 s each |
| Kafka | 2 published, 0 consumed | `rwb.treatment.SignatureRecorded.v1` and `rwb.treatment.SignatureWindowClosed.v1` on `rwb.treatment.events.v1`, written in the outbox of their own transaction (DP-09) |
| Temporal | The stage, 3 activities and 1 durable timer | `TreatmentWorkflow` on queue `rwb-treatment` in namespace `rwb-recovery`, with `openSignatureWindow`, `recordSignatureResult` and `closeSignatureWindow`, and one timer per window; no Schedule |
| File | None | No file is read, built or delivered: the signed PDF and its version are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `signature`, Java package `th.co.scb.ace.workbench.recovery.treatment.signature`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is the seam: the legacy in-process `TreatmentApi.recordSignature` becomes the published update operation, built against a mock on both sides, so rwb-comms and this service start on the same day (ASM-4471). DP-01 keeps the write in `rwb_treatment` and makes the request, the template and the case unreachable as tables. DP-05 is a boundary rather than a call: the party rows come from the one view this service is granted. DP-07 is the method and status lists, so no method and no status is a constant. DP-09 announces the record and DP-10 is the window's clock. DP-13 is the base, DP-15 the migration and DP-19 the route SCR-14, SCR-30 and SCR-09 use.

**Dependencies the table adds and the plan does not hold.** The table adds five H rows — `RWB-PLT-E1043-CON`, `RWB-PLT-TE006-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1044-CON` and `RWB-PLT-N001-CON` — and one C row, `RWB-P3-E1043-CON`, while the plan's lists for this story hold Depends on (build) `None` and Contract dependencies `None`. They are platform library and contract deliverables the service template already carries, the story builds against their fakes until they publish, and the metadata keeps the plan's lists as they are (ASM-4473).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `SignatureRecordGuard` | Service | Checks that the treatment is with the customer and inside its window, refuses with MSG-P3-005 or MSG-P4-003 and opens no transaction (BR2) |
| `SignatureRecordApplier` | Service | Checks the reference, the method, the status and the party, then writes the row change and the outbox row in one transaction (BR1, BR4, BR8) |
| `SignatureStateWriter` | Repository | Writes the five columns and the standard columns of `treatment` in one `rwb_treatment` transaction, with the idempotency row |
| `SignatureEventPublisher` | Library adapter | Writes the `SignatureRecorded` and `SignatureWindowClosed` outbox rows of the same transactions (DP-09) |
| `SignatureListCatalog` | Client | The reference-data reads of LOV-SIGN-METHOD and LOV-TRT-SIGNATURE, one hop, 2 s, cached (DP-07) |
| `CasePartyReader` | Repository | Reads the party keys of the case from `v_ace_customer`, SELECT only (DP-05) |
| `SignatureWindowCloser` | Service | The timer callback: NOT_SIGNED with reason OFFER_EXPIRED and one closure event (BR5) |
| `TreatmentSignatureView` | Service | Serves the signature properties on the treatment read and nothing else |

**Database.** `treatment` gains five nullable columns: `signature_method` varchar(12), `signature_request_ref` varchar(40), `signature_sent_at` timestamptz, `signature_signed_at` timestamptz and `signature_expires_at` timestamptz, with a unique index `ux_treatment_signature_request_ref ON treatment (signature_request_ref)` and an index on `(signature_status, signature_expires_at)` for the timer. Their names, and the fact that the treatment rather than the signature request holds them, are this story's design and are Not specified in the source documents (GAP-2699; ASM-4470). No existing column changes, no backfill runs and no row of another service's table is copied (DP-01, DP-15).

**Configuration and reference data.**

- LOV-SIGN-METHOD with E_SIGNATURE, BRANCH and PAPER, and LOV-TRT-SIGNATURE with PENDING, SIGNED and NOT_SIGNED, are read through the reference-data contract and client library of rwb-case (DP-07); the operations are Not specified in the source documents (GAP-2699; ASM-4472).
- The reason code OFFER_EXPIRED is a parameter read at its version, not a literal.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020 and not a value of this story; the 60-second store target, the retry limit 5 and the signature basis are the P6 and P5 stories'.
- The feature switch `rwb.treatment.signature-window`, read as a flag of the platform library: off means the send opens no window, the five columns stay empty, no event is written and the treatment read answers empty values.

**Build steps**

1. The Flyway version with the five nullable columns and the two indexes, and its migration test against the sibling's `treatment` template (AC2; DP-15).
2. `SignatureListCatalog` and `CasePartyReader` over the reference-data fake and the view fixture, with an unknown method and a party outside the case (AC1).
3. `SignatureRecordGuard` with the not-with-customer and closed-window refusals (AC4, AC6).
4. `SignatureRecordApplier`, `SignatureStateWriter` and `SignatureEventPublisher` in one transaction, with the repeat, the forced outbox failure and the rollback (AC2, AC5).
5. `openSignatureWindow` with the expiry copied from `valid_until`, and `SignatureWindowCloser` with the timer and a worker restart during the wait (AC4).
6. The decline and the wet ink paper path, with the outcome report to the parent (AC3).
7. `TreatmentSignatureView` on the declared read and update, additive, with a treatment that was never sent (AC7).
8. The guard case and the property test that no name, no signature image and no PDF byte reaches a column, a log line or an event (AC8).
9. The boundary test: no statement outside `rwb_treatment`, no read of a `signature_request`, document, template or case table, one `v_ace_customer` read, two events only and no Schedule (BR9, section 12.9).

**Feature flag.** `rwb.treatment.signature-window`.

**Done when.** The tests of section 16 pass, the contract tests of the two declaring contracts stay green, a SIT week shows one window and one state per treatment, one event per outcome, a repeated record writing once, a closed window refused with MSG-P3-005, SCR-14 showing the state and the method through the composite route, and no read of a signature, document, template or case table in the logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | The record names a method, a status or a party that is not valid for the case (X1, X2, AC1) | Enter {field}. |
| MSG-P3-005 | The record arrives for a treatment that is not with the customer, or after the window closed (X4, X6, AC4, AC6) | This case cannot move to {state} from {current}. |
| MSG-P4-003 | The treatment or the request reference is not found, or the case lies outside the caller's scope (X3, X9, AC6) | This case is not in your scope. |
| MSG-P4-002 | The caller holds no Treatment and offer U on the record operation (X9, AC8) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A list read the record needs did not answer, or the service is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P6-009 | E-signature asked for a document that needs wet ink (the refusal is `RWB-P6-E2018-APP`'s) | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force (the refusal is `RWB-P6-E2018-APP`'s) | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case (the refusal is `RWB-P6-E2018-APP`'s) | This case is on hold for {deviation}. The prescription date is still {date}. |

The IDs and the wording are copied unchanged from legacy RWB-E2-018 section 14; the three refusals at the bottom are the P6 story's and are listed here only to show that this service re-words none of them. Thai text for each message follows decision DL10. Delivery shape: each error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-GEN-006 the {system} value is "Reference data" on the list reads and "Signature flow" on the send; for MSG-GEN-001 the {field} value is the wire name of the failing property; for MSG-P4-002 the {action} value names what the caller tried and never a case fact or a party key.

### 15. Screens and states

No screen is built in this story. Three surfaces show what it writes, all read through the gateway-bff composite route (DP-19), and only the first is this service's own read model.

| Screen | State | What the user sees |
|---|---|---|
| SCR-14 Treatment record | Loading | The placeholder while the composite route answers |
| SCR-14 Treatment record | Offer with the customer, no window yet | The treatment's terms and the send action, and no signature state |
| SCR-14 Treatment record | PENDING, window open to 2026-12-20 | The method of the send, the send time and the window end, with the request list as rwb-comms serves it |
| SCR-14 Treatment record | SIGNED | The status, the method and the signed time, with the signed copy as rwb-document serves it |
| SCR-14 Treatment record | NOT_SIGNED | The status, the method and, for a closed window, the reason OFFER_EXPIRED, with the routing the case took |
| SCR-14 Treatment record | Refused | MSG-P3-005, MSG-P4-002, MSG-P4-003 or MSG-GEN-001 as the guard or the record answered, the row unchanged |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-8379) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-8379) |
| SCR-14 Treatment record | No access | 403 with MSG-P4-002 as AC8 |
| SCR-30 Case documents | Any | The signed version of the agreement against the generated one, read from rwb-document and never from a table here |
| SCR-30 Case documents | Loading | Not specified in the source documents (CG-ALL-8380) |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-8380) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-8380) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-8380) |
| SCR-09 Exception queue | Any | The signature results the signature flow held; this service lists none of its own |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-8378) |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-8378) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-8378) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-8378) |
| EasyApp | Customer side | The customer's signing page; no Workbench login and no treatment read |

The route merges this service's answer with the document read of rwb-document; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON` and the edge stories, not here (ASM-4477). The field list and the layout of SCR-14, SCR-30 and SCR-09 belong to the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC1, AC2 (legacy AC1, BR2, BR7) | End to end | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; EasyApp stub SIGNED |
| TC-E2-018-02 | AC1 (legacy AC2, BR1) | End to end | Branch scan D-0602 |
| TC-E2-018-03 | AC3 (legacy AC3, BR1, BR3) | End to end | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04 | AC1 (legacy AC4, BR1) | End to end | E_SIGNATURE on D-0701; method list offered for WET_INK_REQUIRED |
| TC-E2-018-05 | AC3 (legacy AC5, BR4) | End to end | EasyApp stub DECLINED |
| TC-E2-018-06 | AC4 (legacy AC6, BR5) | End to end | Cancel on 2026-12-21, then SIGNED result |
| TC-E2-018-07 | AC6 (legacy AC7, BR6) | End to end | Open X2 with contact stop |
| TC-E2-018-08 | AC2 (legacy AC8, BR9) | End to end | EsignPort stub unavailable |
| TC-E2-018-09 | AC5 (legacy AC9, BR8) | End to end | Result EA-30001 twice |
| TC-E2-018-10 | AC6 (legacy AC10) | End to end | Result EA-99999 |
| TC-E2-018-11 | AC6 (legacy AC11) | End to end | Branch SIGNED with no document |
| TC-E2-018-12 | AC8 (legacy Access) | Component | RW-PHONECOL sends POST /treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 |
| TC-S2-E2018-APP-01 | AC1 | Component | The record for "T-0501": signed true, method "E_SIGNATURE", 2026-12-11 10:15:00, reference "EA-30001", written and served on the read; method "COURIER" and party "P-9999" refused with 422 and MSG-GEN-001 |
| TC-S2-E2018-APP-02 | AC2, AC3, AC5 | Integration | A SIGNED record writes the row and one outbox row in one transaction; a DECLINED record writes NOT_SIGNED; a repeat of "EA-30001" writes nothing second; a forced record failure rolls back |
| TC-S2-E2018-APP-03 | AC4, AC6 | Component | The timer at 2026-12-20 closes the window; a later SIGNED is refused with MSG-P3-005; "EA-99999" and "T-0503" write nothing |
| TC-S2-E2018-APP-04 | AC7, AC8 | Component | SCR-14 through the composite route shows "SIGNED", "E_SIGNATURE" and 2026-12-11 10:15:00; the events and the logs carry the party key and no name; RW-PHONECOL refused with MSG-P4-002 |
| TC-S2-E2018-APP-05 | AC9 | Component | A statement naming rwb_document, rwb_comms, rwb_case or a v_ace_* view other than v_ace_customer is refused by the grant and the boundary test fails the build |
| TC-S2-E2018-APP-06 | AC1 to AC8 | Contract | Each operation, event and activity of section 12 is checked against the contract fakes of section 12.8 |
| TC-S2-E2018-APP-07 | AC2, AC5 | Component | The tables of section 12.7 (ASM-3438) are written only in rwb_treatment; a write to any other table fails the build |
| TC-S2-E2018-APP-08 | AC10 | Component | A statement naming the table template of rwb_comms is refused by the grant, the boundary test fails the build and the pipeline log holds the failure |
| TC-S2-E2018-APP-09 | AC11 | Component | A changed value in the method, reason or expiry rows is read at its version with no code change; a statement writing a rwb_case table is refused |
| TC-S2-E2018-APP-10 | AC12 | Component | A call to PATCH /treatments/{treatmentId} or GET /treatments/{treatmentId} without a valid credential is answered 401 and writes nothing |
| TC-S2-E2018-APP-11 | AC13 | Component | An activity timed out after Not specified in the source documents (NEWAC-RWB-S2-E2018-APP-AC15) and retried answers the first state and writes nothing second |

The twelve legacy test case IDs, their Covers and their Data are kept in the order the work package lists, and the values of the legacy story are kept character for character; the legacy level "System" maps to "End to end" and the Access case to "Component". The eleven added cases are this story's and test only the S2 deliverable; the business outcome of the flow is proved by the twelve legacy cases as they are written in `RWB-P6-E2018-APP` and `RWB-P5-E2018-APP`, and the mapped criteria above name the treatment consequence each case also checks where the stories meet. The fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value a business person may change is written in code: the method list, the status list, the reason code and the expiry are reference data read with their version (BR10; DP-07).
- No personal data in logs, tests, workflow inputs or prompts: the row, the events and the logs carry case IDs, treatment IDs, the party key, codes, times and references only, and the profile codec is on every payload (CTL-11; ASM-4476; AC8).
- The signed PDF, the signature image and the bank certificate never enter this service: the certificate stays in the key store (NFR-052), the signed version stays in rwb-document, and this service holds a reference and no byte (BR7; AC2).
- No read of another module's tables: the signature request, the template and the case arrive through their owners' contracts or not at all, and `rwb_treatment` holds no foreign key into another schema (DP-01, BR9).
- ACE data only through the owner's contract or the `v_ace_*` views: the one view this story reads is `v_ace_customer`, SELECT only, for the party rows (DP-05; ASM-4475).
- The row change and its outbox row are one transaction, and a failed write moves nothing (DP-09; AC2).
- The basis check, the conduct check and the EasyApp path are never re-implemented here: no direct call to EasyApp leaves this service (BR6).
- An applied migration is never edited: a correction to the five columns is a new version on the service sequence (DP-15).
- No right is re-implemented: the capability area and the right are declared and the guard library answers; the treatment state is written by this service and by nothing else.
- Two events only: this module declares `SignatureRecorded` and `SignatureWindowClosed`, and a build that adds a third on this topic fails the review.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16, R-RES-17, R-RES-18, R-SET-10, R-SET-11, R-SET-12, R-DIL-18, R-DIL-27, R-UNI-33, R-UNI-40 | TC-E2-018-01 to TC-E2-018-12, TC-S2-E2018-APP-01 to TC-S2-E2018-APP-11 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P6-E2018-APP | App development | The circuit of the legacy key and the owner of its eleven criteria: the basis check, the conduct check, the EasyApp leg, the retry and the exception queue; it calls this story's record |
| RWB-P5-E2018-APP | App development | The signature request row, its five statuses and the signed copy in rwb-document |
| RWB-ITG-E2018-ITG | Integration | The cross-service proof of one signature across rwb-comms, rwb-document, rwb-treatment and the ACE path, held by the wave 2 harness |
| RWB-S2-E3001-CON, RWB-S2-E3002-CON | Contract | The declared treatment read and update the signature properties are added to, additively |
| RWB-S2-E3007-APP | App development | Sibling: sends the offer and opens the window in the same transaction |
| RWB-S2-E3008-APP, RWB-S2-E3009-APP | App development | Siblings: route the signed offer to operations, and return the case on no signature |
| RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H by the pattern table: reference data, outbox, workflow kit and timer, Flyway and the composite route (ASM-4473) |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract of rwb-case behind the method and status lists (DP-07; ASM-4473) |
| RWB-P6-E1046-APP | App development | P6 rwb-comms: the template, its signature basis and the Legal approval of a version |
| P3 rwb-case | App development | The parent `CaseWorkflow`, the case status and the routing rows the outcome feeds |
| P7 rwb-decision | App development | The RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages whose rows act on the outcome |

### 19. Out of scope

- The signature basis check, the conduct check, the EasyApp send on INT-34, the retry limit 5 and the exception queue: `RWB-P6-E2018-APP`.
- The signature request table with its five statuses, the bank signature and the request expiry: `RWB-P5-E2018-APP`, and the signed PDF as a write-once version, the 60-second store target and the retention: P5 rwb-document.
- The template, its signature basis as data and the Legal approval of a version: P6 rwb-comms and RWB-P6-E1046-APP.
- The offer itself, its validity rule and the send: RWB-S2-E3007-APP; the timer is started there and this story supplies only its closure callback.
- The route of a signed treatment to operations for booking, and the booking in ALS and NLEADS: RWB-S2-E3008-APP and Epic 3.
- The return of the case to its prior status on no signature, beyond the state this story writes: RWB-S2-E3009-APP.
- The deed in lieu field inspection and the Land Office transfer after a wet ink signature: RWB-S2-E3015-APP and Epic 3.
- The central decision ledger: P7 rwb-decision, whose library is not in this story's pattern set.
- Signature in customer self-service (FEAT-COM-02, Epic 4).
- The case status, the `CaseWorkflow` and the case table: rwb-case (P3).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of one signature and the live provider tenant: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.
