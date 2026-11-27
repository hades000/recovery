# RWB-S2-E3002-CON Offer a settlement inside the range - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-002 for rwb-treatment. The legacy acceptance criteria stay with the application slice; every criterion here is new (D-RCV-60) and tests only the contract deliverable. The contract publishes the offer surface on base `/api/recovery/treatment/v1` (DP-13), the `SettlementOffer` and `TreatmentUpdate` elements, the range and floor facts that are request context and never columns, the `belowFloor` answer, the error set and the fakes, and it resolves the operation-name conflict in favour of Architecture v5 slide 18 under the source precedence of §R3 (GAP-1870, GAP-1871; ASM-3066, ASM-3067). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S2-E3002-CON-L124, HELD-RWB-S2-E3002-CON-L243, HELD-RWB-S2-E3002-CON-L51). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Contract version | v1 on base `/api/recovery/treatment/v1` (DP-13) |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Sized by the squad at refinement; no size in this document (DOR-RWB-S2-E3002-CON-16) |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S2-E3002-CON-14) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner for rwb-treatment**, I want **the published contract of the settlement offer — the two operations on the service base, the `SettlementOffer` request and its answer, the `TreatmentUpdate` element of the draft terms, the range and floor facts that travel with a request and are never stored, the `belowFloor` answer with what the approval path needs, the error set with the `Idempotency-Key` rule, the compatibility rule and the fakes — instead of the monolith's one `recovery` schema and one in-process service class**, so that **the application slice, the approval sibling, the gateway-bff route and the wave 2 integration harness all build against one frozen offer surface from Day 1, and no consumer builds against a path that will not exist**.

This story owns:

- the two operation entries — `POST /treatments/{treatmentId}/offer` and `PATCH /treatments/{treatmentId}` — on base `/api/recovery/treatment/v1`, with their access right, their request and response elements, their errors and the `Idempotency-Key` on the offer (DP-13);
- the `SettlementOffer` and `TreatmentUpdate` elements and the request-context facts `rangeLow`, `rangeHigh` and `floor`, which are not columns of any table;
- the `belowFloor` response flag and the hand-off to the approval path of RWB-S2-E3003-CON;
- the error set with MSG-S2-001, MSG-S2-002, MSG-S2-003, MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009 mapped to status codes;
- the compatibility rule, the pinning rule and the drift test, and the fake set every consumer uses.

It does not own: the behaviour behind the two operations, which is RWB-S2-E3002-APP; the treatment resource and the treatment read element, which are RWB-S2-E3001-CON; the TDR plan body, which is RWB-S2-E3004-CON; the approval resource and its matrix, which are RWB-S2-E3003-CON; the decision-record library, which is RWB-PLT-E1027-CON; the gateway-bff composite route, which is RWB-PLT-N001-CON; the case status and its signal, which are rwb-case's; and the payoff and range calculation, which are S1 rwb-valuation's.

### 2. Business rationale

Legacy RWB-E3-002 offered the officer one screen and no contract: the offer amount, the haircut, the validity date and the decision log row were columns of one `recovery` schema written by one in-process service, so there was nothing to publish and nothing to fake. The microservice split removes that option. The offer is now written by rwb-treatment, approved by the same service in a separate story, reached by the screens through gateway-bff, and proved across services by the wave 2 harness, so four consumers need the same answer to the same questions before any of them writes code.

**The division of the legacy key is fixed.** The legacy acceptance criteria **AC1 to AC4 stay with RWB-S2-E3002-APP**, which owns the offer inside the range, the two rule outcomes and the failed record write; every criterion in section 7 is new and tests only the contract deliverable in this title. The treatment resource, its create and its read are RWB-S2-E3001-CON, and the plan body is RWB-S2-E3004-CON: this contract declares the offer and the draft terms and nothing else.

The contract has to exist first for three reasons. The **range and the floor have no place in the schema**: TSD S2 T3.1 carries no floor, no range and no validity column and defines no `SettlementOffer` entity, while the functional specification says the range comes from the payoff and range calculation of another module and that an offer below the floor needs approval. If the offer body is not fixed, one consumer will send a floor and another will read it from a table, and the second will copy S1's calculation into `rwb_treatment` (GAP-1870; ASM-3066). The **operation name is in conflict**: Architecture v5 slide 18 names `POST /treatments/{id}/offer`, while API Specification v5 and TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit` for the same purpose, and §R3 puts the catalogue slides first, so exactly one path may be published and the other has to be recorded as superseded (GAP-1871; ASM-3067). And the **decision record is transactional**: the offer and its record commit together through RWB-PLT-E1027-CON, so the contract has to say that the offer is a state change with a record and not a report (DP-03).

The contract also fixes what it does not do: it declares no table, adds no column for the range, the floor, the below-floor answer or the validity state, publishes no event of its own, declares no workflow, and copies no part of the treatment resource or the plan body.

The fake is the Day-1 unblocker: the application slice, the approval sibling, the gateway route and the harness can build the offer, the below-floor path, the repeated key and the error answers before the live service, the live case workflow or the live S1 calculation exists (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service identity is fixed by Template and Rules §R4 and Architecture v5 slides 18 and 41: schema `rwb_treatment`, base `/api/recovery/treatment/v1`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13).
- The offer operation is the one of Architecture v5 slide 18, `/offer`, because the source precedence of §R3 puts the catalogue slides above the Technical Specifications; the TSD and API Specification form is recorded as superseded (GAP-1871; ASM-3067).
- The offer body and the request-context facts are the working read of the assumption, because no source document gives the settlement offer an entity, a field list or a place in the schema (GAP-1870; ASM-3066).
- The capability area "Treatment and offer" and right U are the access declaration of TSD S2 T6.1 and T-A.2 for API-S2-003 and API-S2-004; the check is the guard library's and the contract declares the right only (ASM-3064).
- RWB-PLT-E1027-CON is published, so the contract can name the decision-record write the application slice makes in the same transaction, without redeclaring the library (DP-03).
- RWB-PLT-N001-CON is published, so the contract can name the composite route the two screens use, without declaring a route (DP-19).
- The treatment resource of RWB-S2-E3001-CON is named only: the answer of the offer carries the treatment reference and does not restate the treatment element, and the draft patch answers in the treatment element of that contract.
- The validation messages keep their legacy identifiers and texts, and no published catalogue defines their entry format, so the entry format is the working read (GAP-1870; ASM-3066).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), sits in contract group `CG-W2`, and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the two operation entries: the method, the path on the service base, the access right, the request element, the answer element, the errors and the idempotency rule of each.
2. The author fixes the `SettlementOffer` element: `offerAmount`, `haircutAmount`, `validityDate`, `rangeLow`, `rangeHigh`, `floor` and `deviationFlag`, and states for each one whether it is stored or context-only.
3. The author fixes the `TreatmentUpdate` element of the draft terms and its relation to the treatment resource of RWB-S2-E3001-CON.
4. The author fixes the answer of the offer: the stored terms, the treatment reference and the `belowFloor` flag with the floor and the gap to the floor that the approval path of RWB-S2-E3003-CON reads.
5. The author fixes the error set: the status codes, the message identifiers and the texts, and the `Idempotency-Key` rule with its repeat answer.
6. The author records the conflict resolution: `/offer` is published, `/submit` is not, and the reason is the precedence rule with the two sources named.
7. The author writes the compatibility rule — what a consumer may rely on and what raises a major version — and the pinning rule for the four consumers.
8. The lint and schema steps run: the operation entries compared against Architecture v5 slide 18, the two schemas validated against the OpenAPI document, the examples scanned for personal data, and the error table checked against the message identifiers of the legacy story.
9. The fake set is generated from the document: the offer fake, the below-floor fake, the repeated-key fake, the error fake, the treatment resource fake and the composite route fake.
10. The contract test runs the fakes against the document on every change and fails the build on any drift; the document and the fakes are published at v1 and the four consumers pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document publishes `/treatments/{treatmentId}/submit`, or both forms | The lint fails the build; only `/offer` is published and the TSD form is recorded as superseded | None | AC1 |
| X2 | An element of the offer body has no place in the schema, or the document adds a range, floor or below-floor column | The schema validation fails the build; the facts are declared context-only and no table is declared | None | AC2 |
| X3 | The `belowFloor` answer is published without the floor and the gap the approval path needs, or the flag is absent | The answer schema fails the build; the flag and the hand-off elements are required | MSG-S2-001 | AC3 |
| X4 | An error answer is published without a message identifier, or with a code the legacy story does not carry | The error-table check fails the build; every code is mapped to its identifier and its text | None | AC4 |
| X5 | The `Idempotency-Key` is declared optional, or a repeat is declared to store a second row | The lint fails the build; the header is required on the offer and a repeat returns the first answer | None | AC4 |
| X6 | A breaking change is made to a path, an element, an error code or the answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A consumer ships without the drift test, or its code drifts from the published schemas | The registry refuses the change and the drift test fails that consumer's build | None | AC6 |
| X8 | A value a consumer needs is named by no source — the field list, the schedule of the validity date or the gap element | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1870; ASM-3066) | AC7 |

X1 and X6 are contract-governance paths, X2, X3, X4 and X5 are the paths a missing or invented element adds, and X7 is the drift rule of class C. X8 is the reason the offer body is published as a working read and not as a value found in a source.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the fixture set are open until v1 is frozen; the two paths, the elements, the flag, the errors and the compatibility rule are fixed |
| Valuable | Unblocks the application slice, the approval sibling, the gateway route and the wave 2 harness on Day 1 and keeps the range and the floor out of the schema |
| Estimable | Two operations, two elements, one answer, seven errors, two rules and six fakes |
| Small | One sprint for the document, the schemas, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: settlement offer contract

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the service base is /api/recovery/treatment/v1, the schema rwb_treatment and the topic rwb.treatment.events.v1
    Given the contract declares the offer surface only, and no treatment resource and no plan body

  Scenario: AC1 The offer surface is two operations and the path conflict is resolved to /offer (new, D-RCV-60)
    Given the operation section of the contract document
    When it is validated against Architecture v5 slide 18 and the TSD appendix
    Then it publishes POST /api/recovery/treatment/v1/treatments/{treatmentId}/offer for the settlement offer, under capability area Treatment and offer with right U
    Then it publishes PATCH /treatments/{treatmentId} for the draft terms, under the same capability area with right U
    Then no other operation is declared under the offer surface, and in particular no POST /treatments/{treatmentId}/submit is published; the plan write is bound to the offer operation and no second path carries a plan
    Then the change note records that API Specification v5 and TSD S2 T-A.1 API-S2-004 name /submit for the same purpose and that the form is superseded under the source precedence of §R3, and the solution architect confirms the path at the wave 2 contract freeze
    Then the lint fails the build if a second form of the offer operation appears on any path

  Scenario: AC2 The SettlementOffer element is fixed and its facts are not stored (new, D-RCV-60)
    Given the request schema of the offer operation and the schema of the service
    When the schema is validated
    Then SettlementOffer carries offerAmount, haircutAmount, validityDate, rangeLow, rangeHigh, floor and deviationFlag
    Then the document states that rangeLow, rangeHigh, floor and deviationFlag are request context facts carried on the route decision signal and are not columns of rwb_treatment
    Then the document declares no table and no column for a range, a floor, a below-floor answer or a validity state
    Then TreatmentUpdate carries the draft terms of the offer and answers in the treatment element of RWB-S2-E3001-CON, which is named and not restated
    Then an example carries an amount, a haircut and a validity date and no account number, national identifier or name

  Scenario: AC3 The below-floor answer carries the flag and the approval hand-off (new, D-RCV-60)
    Given the answer schema of the offer operation
    When one inside-range answer and one below-floor answer are validated
    Then the answer carries the stored terms, the treatment reference and belowFloor
    Then a below-floor answer carries belowFloor true, the floor in force and the gap to the floor, which the approval path of RWB-S2-E3003-CON reads
    Then the document states that belowFloor is computed against the floor carried on the request context and never against a constant
    Then the element that carries the gap is named gapToFloor as the working read, because no source document fixes its name
    Then the message MSG-S2-001 of the below-floor answer keeps its legacy text and its two merge fields

  Scenario: AC4 The error set and the Idempotency-Key rule are fixed (new, D-RCV-60)
    Given the error section of the document
    When each declared answer is validated
    Then the operations declare 401, 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001 and 503
    Then the document maps MSG-S2-001, MSG-S2-002 and MSG-S2-003 to the answers that carry them, keeps their legacy texts and adds no message identifier
    Then the offer requires the Idempotency-Key header and a repeated key answers with the first result and stores no second row
    Then PATCH /treatments/{treatmentId} declares no idempotency key, as TSD S2 T-A.2 API-S2-003 states
    Then an error answer carries the message identifier, the merge fields and the trace identifier only

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then a backward-compatible change keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change to a path, a required element, an error code or the answer raises major version 2 and v1 is never edited in place
    Then each of the four consumers pins a published version and raises a change request rather than a private variant

  Scenario: AC6 The fake answers the document and every consumer runs the drift test (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the offer fake, the repeated-key fake, the error fake, the treatment resource fake, the composite route fake and the decision-record fake
    Then the offer fake answers an inside-range offer, a below-floor offer with the gap and a repeated key with the first result
    Then the error fake answers 403, 422 and 503 with their message identifiers and no personal data
    Then the treatment resource fake answers with the element of RWB-S2-E3001-CON and the composite route fake answers one hop for SCR-15
    Then the drift test fails the build of any consumer whose request, answer or error does not match section 12

  Scenario: AC7 A value named by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value a consumer needs is named by no source document
    When the contract publishes that value
    Then the value is published as the working read of the assumption, with Not specified in the source documents (GAP-1870; ASM-3066) as its source
    Then the gap stays open and the document does not present the value as a value found in a source

  Scenario: AC8 A status change the model does not allow is refused and stores no row (new, D-RCV-60)
    Given a treatment in a status for which the offer is not allowed, the list of such statuses being Not specified in the source documents (NEWAC-RWB-S2-E3002-CON-AC9)
    When the offer operation is called for that treatment
    Then the answer is 409 on a state conflict as AC4 declares, and the status is unchanged
    Then no second row is stored
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here, because **AC1 to AC4 of RWB-E3-002 are owned by RWB-S2-E3002-APP**, and every identifier, path element, message and code is taken from Architecture v5, the TSD appendix or the legacy story character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The offer surface is two operations on the service base: the offer under right U with an idempotency key, and the draft terms under right U | DP-13; TSD S2 T-A.1 API-S2-003 and API-S2-004; Architecture v5 slide 18 | AC1 / TC-S2-E3002-CON-01 |
| BR2 | Only `/treatments/{treatmentId}/offer` is published; the TSD and API Specification form `/submit` is recorded as superseded under the source precedence of §R3 | GAP-1871; ASM-3067; Template and Rules §R3 | AC1 / TC-S2-E3002-CON-01 |
| BR3 | The offer carries the amount, the haircut, the validity date, the range, the floor and the deviation flag; the range and the floor are context facts and are never columns | GAP-1870; ASM-3066; DP-01 | AC2 / TC-S2-E3002-CON-02 |
| BR4 | A below-floor offer answers with `belowFloor` true and the gap to the floor, which the approval path reads; the floor is the value in force and never a constant | R-SET-05; REQ-S2-004; MSG-S2-001 | AC3 / TC-S2-E3002-CON-03 |
| BR5 | An offer carries its validity date, and the contract states the date the offer to the customer ends | REQ-S2-002; MSG-S2-003 | AC2, AC4 / TC-S2-E3002-CON-02, TC-S2-E3002-CON-04 |
| BR6 | The contract declares the access right only; the check is the guard library's on capability area "Treatment and offer" | TSD S2 T6.1; ASM-3064 | AC1 / TC-S2-E3002-CON-01 |
| BR7 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C | AC5 / TC-S2-E3002-CON-04 |
| BR8 | The contract declares no table, publishes no event and declares no workflow; the offer is a state change with a record written in the caller's transaction | DP-01; DP-03 | AC2 / TC-S2-E3002-CON-02 |

**Where each rule lives in the target.** BR1 and BR6 are the operation table with its access column, and the guard is called by the application slice, not by the contract. BR2 is the conflict resolution of the change note and the lint rule of X1; this is the one place in the story where a legacy-adjacent path is deliberately not published, and the reason is written down so that no caller builds against it. BR3, BR4 and BR5 are the two schemas and the answer, and they are the reason the document states for every property whether it is stored or context-only. BR7 is the compatibility section and the pinning rule. BR8 keeps the contract out of the schema and the topic: the table is RWB-S2-E3001-APP's and the record is RWB-PLT-E1027-CON's.

### 9. State transitions

None at run time: a document and a schema have no state. Two vocabularies are fixed here and the runtime transitions behind them are specified by RWB-S2-E3002-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Offer request | Inside the range | `offerAmount` is at or above the floor and inside the range carried on the request |
| Offer request | Below the floor | `offerAmount` is below the floor carried on the request |
| Offer request | Repeated | The `Idempotency-Key` was presented before; the first answer is returned and nothing is stored |
| Offer answer | Stored | The answer carries the stored terms of the treatment and its reference |
| Offer answer | Refused | The answer carries an error code with its message identifier and merge fields |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited in place |

The offer states of SCR-15 — Draft, below floor, approved, sent, accepted — are the runtime states of the treatment record and are named by the application slice, not by this contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the two schemas, the error table and the fakes |
| The service team of rwb-treatment | Consumes the contract, pins the version and raises a change request rather than a private variant |
| The rwb-treatment tech lead | Confirms that the two operations are the ones the application slice builds |
| The solution architect | Confirms the conflict resolution in favour of Architecture v5 slide 18 under §R3 and accepts the superseded note |
| The S1 rwb-valuation owner | Confirms the names of the range and floor facts that travel on the route decision signal |
| The rwb-case owner (P3) | Confirms that the case status is the parent workflow's and that the signal carries no case table reference |
| The platform edge owner | Confirms the composite route the two screens use, which this contract names and does not declare |
| The wave 2 integration harness owner | Confirms the fake set is enough to prove the cross-service path |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

The two operations of AC1 are guarded by the rwb-access authorise check under DP-08 on capability area "Treatment and offer" with right U, as BR6 states. The operation identifier of that check is Not specified in the source documents (DOR-RWB-S2-E3002-CON-6).

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes operation entries, two element schemas, codes, message identifiers and one example; no customer, account or case value appears | BR1, BR8 |
| Request context facts published | `rangeLow`, `rangeHigh`, `floor` and `deviationFlag` on the request, and `belowFloor` on the answer with the floor and the gap to the floor; all of them context-only | BR3, BR4 |
| Stored fields referenced | The settlement columns of `treatment` — DF-TRT-007 `offer_amount`, DF-TRT-008 `haircut_amount` and DF-TRT-010 `valid_until` — referenced through the elements and declared by RWB-S2-E3001-CON, not redefined here | BR3, BR5 |
| Personal data | None. The example carries an amount, a haircut and a validity date, and the trace and actor references are identifiers, never names | BR8 |
| Tables published | None. The contract declares no table and no column; `treatment` is the application slice's and `decision_record` is the library's (DP-01, DP-03) | BR8 |
| Field identifiers | The stored fields carry DF-TRT-001 to DF-TRT-014; the range, the floor and the below-floor answer carry no field identifier, because no source document gives them one (GAP-1870; ASM-3066) | BR3, BR4 |
| Reference data read | None. The contract reads no list and no parameter; the range and the floor are request context facts (AC2), not parameters. Any list or parameter the application slice reads is governed by DP-06 and DP-07 | BR3 |

The one place where the contract could leak a value is the floor: the document therefore fixes that the floor is a property of the request context and of the answer, that it is never an enumeration and never a default, and that no example value is presented as a value in force.

The offer body is the working read of ASM-3066: offerAmount, haircutAmount, validityDate, rangeLow, rangeHigh, floor and deviationFlag, with belowFloor on the answer. The range and the floor are request context facts (AC2), and no range, floor or validity column is created in the treatment table. The S1 owner of FEAT-VAL-06 confirms the names at the wave 2 contract freeze.

The release of a treatment rides POST /treatments/{treatmentId}/offer; this contract declares no release path of its own. A redelivered release is deduped by cloud event id in the inbox and by the Idempotency-Key on the offer operation. The release body and the EV-10 body: Not specified in the source documents (GAP-2659); they are published by RWB-S2-E3007-CON.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The contract declares the offer surface only; the treatment resource and its read are RWB-S2-E3001-CON and the plan body is RWB-S2-E3004-CON.

| Method | Path | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/treatments/{treatmentId}/offer` | `SettlementOffer` | The stored terms, the treatment reference and `belowFloor` with the floor and the gap to the floor | Treatment and offer, right U | `Idempotency-Key` header required; a repeat returns the first answer |
| PATCH | `/treatments/{treatmentId}` | `TreatmentUpdate` | The treatment element of RWB-S2-E3001-CON | Treatment and offer, right U | Not applicable |

The operation is `/offer` and not `/submit`. Architecture v5 slide 18 names `POST /treatments/{id}/offer` as the rwb-treatment IN operation; API Specification v5 and TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit` for the same purpose, and the source precedence of §R3 puts the catalogue slides first, so the TSD form is recorded as superseded in the change note and is not published (GAP-1871; ASM-3067). The reasons API Specification v5 and the TSD use a different name, and whether the restructure and deed-in-lieu branches ever needed a distinct submit step, are Not specified in the source documents (GAP-1870; ASM-3066).

#### 12.2 REST operations consumed

None. The contract declares the surface and calls no service: the range, the floor and the payoff arrive on the route decision signal that the parent `CaseWorkflow` forwards, and the case status arrives the same way (ASM-3062). The two operations the screens use to reach the treatment read belong to RWB-S2-E3001-CON, and the decision record is an in-process call of RWB-PLT-E1027-CON (DP-03).

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its two events `TreatmentApproved` and `TreatmentClosed` belong to the stories that own the approval and the closure. The contract publishes no event schema of its own and declares no outbox row.

#### 12.4 Events consumed

None. The contract declares no subscription; the two events the application slice consumes — `rwb.decision.RulePackageInForce.v1` (EV-30) and `rwb.deviation.DeviationRaised.v1` (EV-06) — are named in section 19 as out of scope, and the case status is a workflow signal and not an event of this contract (ASM-3062).

#### 12.5 Workflows and activities

None. The contract declares no workflow and no activity. It states only that the offer is written inside an activity on the owner's own task queue and that the decision record is called from that activity, so a replay reuses the recorded decision; the workflow itself is RWB-S2-E3002-APP's `TreatmentWorkflow` settlement branch on `rwb-treatment` (DP-03).

#### 12.6 Schedules

None. The contract declares no Temporal Schedule and no legacy Quartz job; the offer clock of the settlement stage is a durable timer inside the workflow and is not part of the published surface.

#### 12.7 Tables owned

None. The contract declares no table, no column and no key. It states the negative rule that matters: the range, the floor, the deviation flag, the below-floor answer and the validity state have no place in `rwb_treatment`, because no source document gives them one and storing them would copy the S1 calculation into this schema (GAP-1870; ASM-3066; DP-01). `treatment` is RWB-S2-E3001-APP's business table and `decision_record` is the library object of RWB-PLT-E1027-CON; `decision_log_entry` is P7's ledger and is named here only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Offer fake | `POST /treatments/{treatmentId}/offer` | An inside-range offer with the stored terms and `belowFloor` false; a below-floor offer with `belowFloor` true, the floor and the gap to the floor |
| Repeated-key fake | The idempotency rule | The first answer returned for a repeated `Idempotency-Key`, with no second row and no second record |
| Error fake | The error table | 403 with MSG-P4-002, 404, 409 on a state conflict, 422 with MSG-GEN-001 and 503, each with its identifier, its merge fields and a trace identifier |
| Treatment resource fake | `PATCH /treatments/{treatmentId}` | The treatment element of RWB-S2-E3001-CON, referenced and not restated |
| Composite route fake | The gateway-bff composite route of RWB-PLT-N001-CON | One hop for SCR-15, joining the treatment read and the route facts; a refused route for a role without right U |
| Decision-record fake | The library write the application slice makes | An accepted record with an entry reference; a refusal with MSG-P7-009 and the field; a failed write with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consumer rather than as a surprise at run time. The decision-record fake is RWB-PLT-E1027-CON's and is referenced here, not redeclared.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operation entries on `/api/recovery/treatment/v1` | 0 | OpenAPI 3.1 fragment; one hop to the service, 2 s timeout |
| Kafka | 0 event schemas | 0 | The service topic is named; this contract declares no event |
| Temporal | 0 | 0 | The contract states the write happens in an activity and declares no workflow |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the OpenAPI fragment and the two element schemas in `th.co.scb.ace.workbench.recovery.treatment.api`, the error table and the compatibility note in the contract document, and the fake set as a test asset. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1870; ASM-3066).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 enters the contract as one statement — the offer is a state change whose record is written in the caller's transaction — and the H dependency sits on the application slice, which calls the library. DP-13 is the base of the two operations and the reason the legacy base appears nowhere in the document. DP-19 is the route the two screens use, named here so that the composite route fake has an owner.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentOfferOpenApi` | OpenAPI 3.1 fragment | The two operation entries, their parameters, their errors and their access declaration |
| `SettlementOfferSchema` | Request schema | `offerAmount`, `haircutAmount`, `validityDate`, `rangeLow`, `rangeHigh`, `floor`, `deviationFlag`, with the stored and context-only note on each |
| `OfferAnswerSchema` | Answer schema | The stored terms, the treatment reference, `belowFloor`, the floor and the gap to the floor |
| `TreatmentUpdateSchema` | Request schema | The draft terms of the offer, answering in the element of RWB-S2-E3001-CON |
| `ErrorCatalogue` | Document table | The status codes, the message identifiers, the legacy texts and the merge fields |
| `CompatibilityNote` | Document section | The conflict resolution, the compatible versus breaking rule and the pinning rule |
| `OfferFakeSet` | Test asset | The six fakes of section 12.8 and the drift test every consumer runs |

**Database.** None. The contract creates no table, adds no column and declares no key; the negative rule of section 12.7 is the deliverable, and a review that finds a range, floor, below-floor or validity-state column in `rwb_treatment` fails this story.

**Configuration and reference data.** The contract fixes no business value. The floor, the range, the validity and the leadership of the approval matrix are values in force in the owner's data; the only values in the document are the example values, and they are marked as examples. Capability area "Treatment and offer" and right U are read from rwb-access through the guard library, which the application slice calls (ASM-3064).

**Build steps**

1. Write the two operation entries, their access right and their idempotency rule; lint that no `/submit` form appears (AC1).
2. Write `SettlementOffer` and the stored-versus-context note for every property (AC2).
3. Write the offer answer with `belowFloor`, the floor, the gap and the treatment reference (AC3).
4. Write the error table with the seven identifiers and their legacy texts, and the repeated-key rule; validate one answer per code (AC4).
5. Write the compatibility note and the pinning rule (AC5).
6. Generate the six fakes and the drift test; wire the drift test into the build of RWB-S2-E3002-APP, RWB-S2-E3003-APP, the gateway route and the wave 2 harness (AC6).
7. Publish v1 and record the pinned version of each consumer.

**Feature flag.** `rwb.treatment.settlement-offer-contract`.

**Done when.** The document and the two schemas validate, the operation lint passes with no second form of the offer path, the error table matches the seven legacy identifiers and texts, the six fakes answer every example including the below-floor answer and the repeated key, the drift test is green on the build of this story and on the build of the application slice, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-S2-001 | The offer amount is below the floor in force | The offer is below the floor of {floor}. It has been sent for approval. | The `belowFloor` answer with the floor and the gap to the floor |
| MSG-S2-002 | The payoff carried on the request context is older than the freshness limit | The payoff is from {date}. A new figure has been requested. | The warning answer of the offer |
| MSG-S2-003 | The offer carries its validity date | The offer to the customer ends on {date}. | The answer, with the validity date |
| MSG-GEN-001 | A required field is absent or invalid | Enter {field}. | 422, with the field name |
| MSG-P4-002 | The role does not hold right U | You cannot {action} here. Your role does not include it. | 403, from the guard library |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, from RWB-PLT-E1027-CON |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. | 422, from RWB-PLT-E1027-CON, with the field |

The seven texts are the legacy texts carried unchanged and the contract adds no message identifier. The entry format of each message in a published catalogue is Not specified in the source documents (GAP-1870; ASM-3066) and is published as the working read. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. SCR-14 Treatment record and SCR-15 Settlement offer are reached through the gateway-bff composite route (DP-19), and the contract fixes only the answers those screens consume: the offer with its `belowFloor` flag, the floor and the gap to the floor on SCR-15, and the treatment element of RWB-S2-E3001-CON after a draft change. The screen states — Draft, below floor, approved, sent, accepted on SCR-15 and Draft, submitted, approved, booked, broken on SCR-14 — are the runtime states of the application slices and are named in section 9 only to keep the vocabulary apart. SCR-14 empty, loading, error and no access: Not specified in the source documents (CG-ALL-8482). SCR-15 empty, loading, error and no access: Not specified in the source documents (CG-ALL-8483).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3002-CON-01 | AC1 | Contract | The two operation entries linted against Architecture v5 slide 18 and the TSD appendix; the access right; the superseded note for the TSD form; the path lint that refuses a second form |
| TC-S2-E3002-CON-02 | AC2 | Contract | The `SettlementOffer` and `TreatmentUpdate` schemas validated; the stored and context-only note on every property; the absence of a table, a column and a field identifier for the range, the floor and the below-floor answer; a personal-data scan of the example |
| TC-S2-E3002-CON-03 | AC3 | Contract | One inside-range answer and one below-floor answer validated: the flag, the floor, the gap, the treatment reference, the MSG-S2-001 text and its merge fields |
| TC-S2-E3002-CON-04 | AC4, AC5 | Contract | One answer per error code with its identifier and merge fields; the required `Idempotency-Key` and the repeat answer; one compatible and one breaking change against the registry in BACKWARD mode |
| TC-S2-E3002-CON-05 | AC6 | Component | The six fakes answering every example, including the below-floor answer, the repeated key, the 403 and the 503; the drift test failing on a consumer that drifts |
| TC-S2-E3002-CON-06 | AC7 | Contract | A value named by no source published as the working read with its not-specified source and the gap left open |
| TC-S2-E3002-CON-07 | AC8 | Contract | A treatment in a status the offer does not allow: the 409 answer on a state conflict, the unchanged status and no second row stored; the disallowed-status list Not specified in the source documents (NEWAC-RWB-S2-E3002-CON-AC9) |

The legacy test set of RWB-E3-002 — TC-E3-002-01 to TC-E3-002-06 — is carried by RWB-S2-E3002-APP and by the wave 2 integration harness, and no legacy id is renumbered here: these five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the floor, the range, the validity and the approval matrix are values in force in the owner's data, and the only values in the document are examples, marked as examples.
- No personal data in a schema, an example, a fake or a log: the example carries an amount, a haircut and a validity date, and the scan fails the build otherwise.
- No table, no column and no key in the contract: the range, the floor, the deviation flag and the below-floor answer stay out of `rwb_treatment` (DP-01; ASM-3066).
- No second path for the offer: the lint of X1 fails any document that publishes both `/offer` and `/submit`.
- No event and no outbox row of the contract's own: the service topic is named and its events belong to the stories that own them.
- No REST call and no workflow in the contract: the record is written in process inside an activity and the case status stays the parent's.
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and a superseded marking.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Program 5.9 | FEAT-TRT-02 | 07 Route, settle and claim | BR3, BR4; R-SET-05 | TC-S2-E3002-CON-02, TC-S2-E3002-CON-03 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program 5.9 | FEAT-TRT-02 | 07 Route, settle and claim | BR5; MSG-S2-003 | TC-S2-E3002-CON-02, TC-S2-E3002-CON-03 |
| Legacy test set RWB-E3-002 | TC-E3-002-01, TC-E3-002-02, TC-E3-002-03, TC-E3-002-04, TC-E3-002-05, TC-E3-002-06 | Program 5.9 | The legacy story's own feature FEAT-TRT-02 | 07 Route, settle and claim | The legacy rules R-RES-04, R-RES-07, R-RES-15 and R-SET-05 | Executed by RWB-S2-E3002-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3002-APP | App development | H consumer: implements the two operations, the floor check, the validity check and the record write against this contract and its fakes; owner of the legacy acceptance criteria |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment resource and its element, which the draft patch answers in and which this contract does not restate |
| RWB-S2-E3003-CON | Contract | Referred to: the approval resource that reads the below-floor answer and its gap to the floor |
| RWB-S2-E3004-CON | Contract | Referred to: the TDR plan body, which is not declared here |
| RWB-PLT-E1027-CON | Contract | H: the decision-record library the application slice calls in the caller's transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the two screens use |
| rwb-case (P3) | Service, wave 1 | The case, its status and the route decision signal that carry the range and the floor facts |
| S1 rwb-valuation | Service, wave 3 | The payoff and range calculation of FEAT-VAL-06, whose facts appear in this contract as request context |
| Wave 2 integration harness | Integration | I: the cross-service proof of the offer against the live owners, with the `-ITG` copies of the legacy test set |

### 19. Out of scope

- The behaviour behind the two operations — the floor check, the validity check, the record write and the stage outcome: RWB-S2-E3002-APP.
- The treatment resource, its create, its read and its element: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The TDR plan body, its installments and its element: RWB-S2-E3004-CON and RWB-S2-E3004-APP.
- The approval resource, its matrix, its levels and its decision: RWB-S2-E3003-CON and RWB-S2-E3003-APP.
- The affordability pre-assessment through ACE: RWB-S2-E3005-APP and RWB-S2-E3005-CON.
- The decision-record library, its `MANDATORY` transaction, its chain and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners (DP-19).
- The case status, the parent `CaseWorkflow` and the route decision signal: rwb-case (P3), which owns them (ASM-3062).
- The payoff and the range calculation, and the names of the facts on the signal: S1 rwb-valuation and FEAT-VAL-06 (GAP-1870; ASM-3066).
- The SETTLEMENT rule package, its authoring, its promotion and its version labels: P7 rwb-decision and the service-template runtime (ASM-3063).
- The two events the application slice consumes, `rwb.decision.RulePackageInForce.v1` and `rwb.deviation.DeviationRaised.v1`: their schemas belong to P7 and S8.
- The error and message catalogue of the platform, the Thai texts and the incident route: the platform library stories (DL10).
- The cross-service proof of the offer and the `-ITG` copies of the legacy test set: the wave 2 integration harness.
