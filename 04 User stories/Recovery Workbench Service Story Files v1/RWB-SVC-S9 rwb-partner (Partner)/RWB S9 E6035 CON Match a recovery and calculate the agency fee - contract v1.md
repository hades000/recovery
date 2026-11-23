# RWB-S9-E6035-CON Match a recovery and calculate the agency fee - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6035-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the agency-fee match of rwb-partner, split from RWB-E6-035. It fixes the two published reads the legacy story names, `GET /partner/instructions` (API-S9-003) and `GET /partners` (API-S9-001), on base `/api/recovery/partner/v1` (DP-13), the `Partner`, `PartnerInstruction` and `InstructionPage` elements over the columns of DF-PRT-001 to DF-PRT-016 with the four lists of TSD S9 T3.2, the fee properties of the answer with their placeholders, the four consumed rows of rwb-payment, rwb-case and rwb-decision, the decision-record element of DP-03, the Partner portal rights of TSD S9 T6.1, the error set of T-A.2, the fakes and the absence tests. No source publishes a fee schedule, a rate, a basis or a rounding; the plan's C row is empty although the baseline declares four consumed rows; DP-04, DP-06, DP-07, DP-10 and DP-16 are absent from the pattern set; and no requirement row traces to FEAT-PRM-07 (GAP-3120; ASM-5404, ASM-5405, ASM-5406, ASM-5407, ASM-5412). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the agency-fee match of rwb-partner — the two instruction and partner reads on `/api/recovery/partner/v1`, the partner, instruction and page elements with their required flags and lists, the fee properties of the answer, the four consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-35, SCR-34 and the wave 4 harness build against one fixed, testable contract on Day 1, and a fee property, a consumed row or an answer shape can never drift between rwb-partner, rwb-payment, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy fee calculation of RWB-E6-035 crossed four boundaries at once: the case of record, the money an agency recovered, the contracted schedule and the rule version in force, and it named two reads that carry every partner action of the module with no element published for either. The target splits them: rwb-case owns the case and the reference data, rwb-payment owns the payment, rwb-decision owns the package, and rwb-partner owns the partner, the instruction and the fee due on it. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, `rwb_payment` or `rwb_decision`, so DP-05 is declared as a prohibition.

Four points are carried as gaps and assumptions rather than decided quietly: the contracted fee schedule has no table, column, rate, tier, rounding or basis in any source (ASM-5405); the plan's C row is None while the baseline declares four consumed rows, and DP-04, DP-06, DP-07, DP-10 and DP-16 are absent from the pattern set (ASM-5404, ASM-5406, ASM-5407); the fee is a property of the instruction answer and not an operation of its own (ASM-5403); and no requirement row traces to FEAT-PRM-07 (ASM-5412).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` is P3's, `payment` is P8's, `decision_log_entry` and `rule_row` are P7's and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own.
- The two reads are published: TSD S9 T-A.1 gives API-S9-001 `GET /partners` and API-S9-003 `GET /partner/instructions` with their access and idempotency rules, and T-A.2 gives their requests, answers and the error set 401, 403 and 503. What the sources do not give are the fee properties and the schedule (GAP-3120; ASM-5403, ASM-5405).
- The rwb-payment payment row, the rwb-case case and reference-data rows and the rwb-decision package row are published with their fakes; they are not in this story's contract-dependency row, which is None, and the absence is recorded (ASM-5404, ASM-5406, ASM-5407).
- The four lists of TSD S9 T3.2 are published as they stand and are copied unchanged; this baseline adds no member to any of them.
- The two tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. The fee schedule has no table to declare (ASM-5405).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the two reads of the OpenAPI 3.1 document of rwb-partner: API-S9-001 and API-S9-003, with their query parameters, their answers, the rights and the error responses.
2. Fix the `Partner` element over DF-PRT-001 to DF-PRT-007, the `PartnerInstruction` element over DF-PRT-008 to DF-PRT-016 and the `InstructionPage` wrapper with its page and size of TSD S9 T-A.2.
3. Fix the fee properties of the instruction answer — the matched recovery, the recovered amount and the fee due — and mark them with the placeholder where no source gives a name or a format.
4. Fix the four lists of TSD S9 T3.2 as they stand: LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION and LOV-INSTR-STATUS.
5. Fix the four consumed rows and their placeholders: the payment read of rwb-payment, the case read and the reference-data read of rwb-case and the package read of rwb-decision.
6. Record the decision-record element of DP-03, written before the fee is accrued, and the rule that the fee is accrued on DF-PRT-016 only.
7. Record the Partner portal rights of TSD S9 T6.1 and the error envelope of the two reads.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the elements and their required flags, the lists, the fee placeholders, the rights, the scope, the error envelope, the boundary, the absence of a private command and of an event of this step, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S9-E6035-APP, the fee-approval story of E7 that shares these reads, SCR-35, SCR-34 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | The fee properties or the schedule are declared as an enumeration, a rate or a basis taken from no source | The vocabulary test fails the build: no source publishes either | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a `payment` row, a `rule_row` or a `decision_log_entry` | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic, a Schedule or a fee command of its own | The absence test fails the build | None | AC7 |
| X8 | The rights of the reads are not the Partner portal rights TSD S9 T6.1 and T-A.2 give them | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices, the API Specification and the published owner contracts of rwb-payment, rwb-case and rwb-decision only |
| Negotiable | The names of the fee properties and the example values are settled in the baseline review; the base, the reads, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E6035-APP, the fee-approval story that shares these reads, SCR-35, SCR-34 and the wave 4 harness on Day 1, and the rwb-payment, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and twelve contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the agency-fee match of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner and partner_instruction is S9, of recovery_case and the reference data is P3, of payment is P8 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The instruction and partner reads are declared with their elements and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partner/instructions as API-S9-003 with the query parameters status, page and size and an InstructionPage answer of status 200, under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then it declares GET /partners as API-S9-001 with the query parameters type and status and a Partner[] answer of status 200
    Then both reads declare the answers 401, 403 and 503 with one envelope and one message ID per condition, and declare Idempotency-Key as not applicable
    Then no write operation of the module is declared by this document, and the invoice operation API-S9-006 is named as the fee-approval story's

  Scenario: AC2 The partner and instruction elements, the lists and the fee properties are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.1, T3.2 and T-A.2, and with the API Specification v4
    Then the Partner element declares the seven columns of DF-PRT-001 to DF-PRT-007: id, partnerCode, partnerName, partnerType, panelStatus, contractEnd and score
    Then the PartnerInstruction element declares the nine columns of DF-PRT-008 to DF-PRT-016: id, caseId, partnerId, instructionType, instructedAt, dueAt, status, resultCode and feeAmount
    Then the required flags are id, partnerCode, partnerName, partnerType, panelStatus and score on the partner, and id, caseId, partnerId, instructionType, instructedAt and status on the instruction, as TSD S9 T3.1 gives them, and the other properties are optional
    Then the lists are LOV-PARTNER-TYPE AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED and EXITED, LOV-INSTRUCTION COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, and LOV-INSTR-STATUS SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, copied from TSD S9 T3.2 and published unchanged
    Then the fee properties of the answer — the matched recovery, the recovered amount and the fee due on feeAmount — carry the placeholder Not specified in the source documents (GAP-3120; ASM-5405)
    Then no property is added for a fee rate, a basis, a tier, a rounding, a rule row, a case state or an ACE extract

  Scenario: AC3 The four consumed rows are declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the payment read is declared as consumed from P8 rwb-payment, with the payment reference, its amount, its value date and its case reference
    Then the case read is declared as consumed from P3 rwb-case, with the case and its write-off route state
    Then the reference-data read is declared as consumed from P3 rwb-case, with the contracted fee schedule of the partner type and instruction type at a date, with its version
    Then the package read is declared as consumed from P7 rwb-decision, with the partner package and its version in force
    Then the four operation names and the schedule's columns are Not specified in the source documents (GAP-3120; ASM-5404, ASM-5405, ASM-5406) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no payment property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The Partner portal rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1, T-A.2 and T6.1
    Then both reads declare the Partner portal right R with the scope applied
    Then the 29 identities of TSD S9 T6.1 hold R or better on the Partner portal: the eight roles the legacy permission table names — RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR and RW-DEBTSALE — and the 21 further identities the table's "and 21 more" resolves to (ASM-5410)
    Then no role is given a right the matrix does not give it, and RW-AGENCYMG alone holds CRUDA
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the fee is accrued (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S9 T2
    Then one decision record is declared per match with the case reference, the instruction reference, the partner reference, the payment reference, the recovered amount, the schedule version, the package version, the fee due and the calculated-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the fee leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the fee is declared as accrued on partner_instruction.feeAmount (DF-PRT-016) in the record's transaction, and on no other column of the table
    Then the record carries no rule row, no account number and no personal data, and the payment reference is declared as a key and not as an account value

  Scenario: AC6 The six fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-payment fake answers a payment after charge-off for the case and a payment that matches no placement
    Then the rwb-case case fake answers the case and its route state, and the reference-data fake answers the schedule in force and a date with no row
    Then the rwb-decision fake answers the partner package at its version in force, and the decision-record stub answers a healthy chain and a stopped chain
    Then the gateway-bff fake answers the merged SCR-35 and SCR-34 answers before and after the fee
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event or fee command is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, the reference data, payment, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic, no Schedule and no fee command, and it names EV-20 and EV-21 as the service's two events with their names carrying the placeholder (ASM-5409)
    Then the absence test fails a build that adds a published event of this step, a consumed event, a second topic, a Schedule, a write operation or a v_ace_* read
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E6035-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The fee accrues on an instruction: no instruction status moves and no write-off route state moves, and no event of this step is declared (ASM-5408, ASM-5409).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The partner and instruction rows are rwb-partner's, and the contract declares the fields and the required flags on the `Partner`, `PartnerInstruction` and `InstructionPage` elements only | TSD S9 T3.1, T-A.2; context pack ownership rows (tables `partner`, `partner_instruction`) |
| BR2 | The match record is declared as an element written before the fee is accrued, through the local library on the shared topic, and the fee is accrued on DF-PRT-016 in the same transaction; a failed write changes nothing | DP-03; TSD S9 T2; legacy AC1 and AC2 |
| BR3 | The payment stays with rwb-payment and the case with rwb-case: the contract declares both as consumed, declares no payment property, no case property and no `v_ace_*` property, and describes no write to either | DP-05, DP-18; ASM-5404 |
| BR4 | The contracted schedule is reference data of rwb-case, declared as a consumed row with its version and with no rate, tier, basis or rounding, because no source publishes one | FSD S9 FEAT-PRM-02; TSD S9 T3.1; ASM-5405, ASM-5407 |
| BR5 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule ID as a property set | ASM-5406 |
| BR6 | No event of this step is declared: EV-20 and EV-21 are the placement's and the result's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5409; TSD S9 T5.3 |
| BR7 | The two reads declare `Idempotency-Key` as not applicable, so a repeat of a trigger is matched on the payment reference and the instruction reference and not on a stored key | TSD S9 T-A.2; ASM-5403 |
| BR8 | The fee properties and the schedule carry a placeholder, because no source publishes a name, a format or a basis | ASM-5405; FSD S9 A2.7.3.1; TSD S9 T3.1 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, dates, amounts, versions and a reference only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-partner, and the two reads are the only ones the legacy story names; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; legacy RWB-E6-035 Endpoints |
| BR13 | The rights of the reads are the Partner portal right R of TSD S9 T6.1, held by all 29 identities of the matrix | TSD S9 T6.1, T-A.2; legacy permission table of RWB-E6-035; ASM-5410 |
| BR14 | The instruction status vocabulary is LOV-INSTR-STATUS and carries no fee member, so the contract declares no `PAYMENT_MATCHED` and no fee state | TSD S9 T3.2; ASM-5408 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the elements, the lists, the fee properties, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the fee-approval story that shares the reads, SCR-35, SCR-34, the wave 4 harness and the owners of rwb-payment, rwb-case, rwb-decision and rwb-access accept the document and the fakes | Baselined |
| Baselined | The schedule and the fee properties are confirmed | The business lead replaces the placeholders inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional recovered-at date | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a fee property becomes an enumeration over an unconfirmed set | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` or `payment` property, an account value, a write operation, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's, and this baseline fixes the vocabulary and moves no instruction and no route state: the instruction statuses are LOV-INSTR-STATUS of TSD S9 T3.2 and `PAYMENT_MATCHED` is a state of the write-off route of rwb-writeoff, which this document does not declare (BR14).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed fee properties and schedule, and the correction of the plan rows the baseline consumes, including the four consumed rows and the absent DP-04, DP-06, DP-07, DP-10 and DP-16 rows |
| Business lead | Confirms the names and formats of the fee properties and the contracted schedule that replace the placeholders |
| Consuming teams (the app story, the fee-approval story, SCR-35, SCR-34, the wave 4 harness and the owners of rwb-payment, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field and no account value is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Partner element | The seven columns of DF-PRT-001 to DF-PRT-007: `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd` and `score` |
| Instruction element | The nine columns of DF-PRT-008 to DF-PRT-016: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode` and `feeAmount` |
| Page element | `InstructionPage`: the page, its size and the instructions, as TSD S9 T-A.2 gives the query and the answer |
| Required flags | `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus` and `score` on the partner, and `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt` and `status` on the instruction; the other properties optional, `id` read-only |
| Lists | LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION and LOV-INSTR-STATUS, copied from TSD S9 T3.2 and published unchanged |
| Fee properties | The matched recovery, the recovered amount and the fee due on `feeAmount`, whose names, formats and value sets are Not specified in the source documents (GAP-3120; ASM-5405) |
| Schedule | The contracted fee schedule of the partner type and instruction type at a date, with its version; its columns, its rate basis and its rounding are Not specified in the source documents (GAP-3120; ASM-5405) |
| Event data | None of this step: no event is declared (§12.3) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the fee is accrued (DP-03) |
| Case, payment and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, the payment of P8 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and the reference data (P3), `payment` (P8), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) |

The field-level types and lengths of the added fee properties are settled in the baseline review; this story fixes the element names, the lists, the required flags of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partner/instructions` (API-S9-003) | Query status, page, size in; `InstructionPage` of status 200 out, each instruction with its matched recovery and its `feeAmount` | Partner portal, right R, scope applied | Not applicable |
| GET | `/partners` (API-S9-001) | Query type, status in; `Partner[]` of status 200 out, with panel status and score | Partner portal, right R, scope applied | Not applicable |

Both reads answer 401, 403 with MSG-P4-002 and 503, each with the error envelope and one message ID of section 14, which is the error set TSD S9 T-A.2 publishes. The paths, the operation IDs, the element names, the rights and the error codes are published; the fee properties carry the placeholder (GAP-3120; ASM-5403, ASM-5405). The four write operations of the module — `POST /cases/{caseId}/instructions` (API-S9-002), `POST /partner/instructions/{instructionId}/accept` (API-S9-004), `POST /partner/instructions/{instructionId}/results` (API-S9-005) and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) — belong to the placement, acceptance, result and fee-approval stories and none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The posted-payment read (operation name Not specified in the source documents (GAP-3120; ASM-5404)) | `/api/recovery/payment/v1` | P8 rwb-payment | The payment reference, its amount, its value date and its case reference; faked |
| The case read (operation name Not specified in the source documents (GAP-3120; ASM-5404)) | `/api/recovery/case/v1` | P3 rwb-case | The case and its write-off route state; faked |
| The reference-data read of the contracted fee schedule and the LOVs (operation name Not specified in the source documents (GAP-3120; ASM-5407)) | `/api/recovery/case/v1` | P3 rwb-case | The schedule in force with its version; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3120; ASM-5406)) | `/api/recovery/decision/v1` | P7 rwb-decision | The partner package at its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (ASM-5404, ASM-5406, ASM-5407).

#### 12.3 Events published

None. The service owns the topic `rwb.partner.events.v1` and its event set carries EV-20 and EV-21, named InstructionIssued and PartnerResultSubmitted in TSD S9 T5.3; the pairing of ID and name is Not specified in the source documents (GAP-3120; ASM-5409). No fee event exists, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the events is the platform library object of DP-09, which the pattern set for this key does not carry.

#### 12.4 Events consumed

None. TSD S9 T5.3 names the two published events and no consumed event, and the context pack's ownership rows give the service no consumer group, so the payment fact is declared as a consumed read in §12.2 and the baseline declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step; the absence test of AC7 fails a build that adds one (GAP-3120; ASM-5404).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, continues-as-new with the case stage | `rwb-partner` in namespace `rwb-recovery` | The stage that hosts the match and the fee steps; its input and its outcome for the parent are declared, not built |
| `matchAgencyRecovery` | Activity, the match step | `rwb-partner` | The payment reference, the case reference and the agency in; the instruction reference and the matched amount out |
| `calculateAgencyFee` | Activity, the fee step | `rwb-partner` | The instruction reference, the schedule and package versions and the recovered amount in; the fee due and the record reference out |

The service owns one workflow and no job in the context pack's ownership rows (Workflows: 1, Jobs: 0). The two activity names are a target design choice, and no activity is registered by this story.

#### 12.6 Schedules

None. R-WO-37 measures the step at "next working day" and FSD S9 A2.7.2 gives the trigger as "a completed ACE batch, an event or a timer"; whether that is an event-started workflow or a Temporal Schedule is Not specified in the source documents (GAP-3120; ASM-5403). This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and the daily scan of the write-off route is rwb-writeoff's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm, its type, panel status, contract end and score; the table the partner element is drawn from |
| partner_instruction | S9 (`rwb_partner`) | Work placed with a partner on a case, with its status, its result code and its `fee_amount`; the table the instruction element is drawn from |
| partner_user | S9 (`rwb_partner`) | The partner's own portal users; named as owned and not part of the two answers of this baseline |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the match and the fee (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the write operations of the module; the two reads declare none |
| outbox_event | PLT library, created in `rwb_partner` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and the reference data (P3), `payment` (P8), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `notice` (P6) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment posted-payment fake | A payment after charge-off for `RW-2026-000611`, and a payment that matches no placement | AC3, AC6 |
| rwb-case case fake | The case with its write-off route state and its party reference | AC3, AC6 |
| rwb-case reference-data fake | The contracted fee schedule in force at a date, by partner type and instruction type, with its version; and a date with no row | AC3, AC6 |
| rwb-decision rule-package fake | The partner package at its version in force | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-35 and SCR-34 answers before and after the fee | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed owners, the schedule's shape and the fee properties carry the placeholder until their owners and the business lead confirm them (GAP-3120; ASM-5404, ASM-5405, ASM-5406, ASM-5407).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | API-S9-001 and API-S9-003 on `/api/recovery/partner/v1`; the payment read, the case read, the reference-data read and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; EV-20 and EV-21 are the placement's and the result's, and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `InstructionWorkflow`, `matchAgencyRecovery` and `calculateAgencyFee` on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no payment, no instruction and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the fee is accrued. DP-13 moves the base of the legacy paths and gives the two reads their home. DP-19 sits behind SCR-35 and SCR-34, whose screen model is the edge contract's. DP-04, DP-06, DP-07, DP-10 and DP-16 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the parameters and the reference data as another service's data with their versions, the workflow as the service's own stage without the platform kit row, and the outside money leg as rwb-payment's rather than an integration adapter of this service (GAP-3120; ASM-5404, ASM-5406, ASM-5407).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, the reference-data rows `RWB-PLT-E1043-CON` and `RWB-P3-E1043-CON`, the workflow kit row `RWB-PLT-E1071-CON` and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`. The four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the two reads of API-S9-001 and API-S9-003 and validate the additive rule of AC1 in the pipeline.
2. Write the `Partner` element with its seven properties and six required flags, the `PartnerInstruction` element with its nine properties and six required flags, and the `InstructionPage` wrapper of AC2.
3. Publish the four lists of AC2 unchanged, and the fee properties and the schedule of AC2 with their placeholders.
4. Record the four consumed rows of AC3 with their owner, their budget and their placeholders.
5. Record the rights and the error envelope of AC4, with the 29 identities of the matrix.
6. Record the decision-record element and the `feeAmount` accrual rule of AC5 and validate them against the library schema.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline, the tables owned and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml`, the three elements, the contract README rows for the four consumed rows and their placeholders, and the six fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the twelve contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the fee-approval story, SCR-35, SCR-34 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a query or an answer is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P1-001 | The contract describes the stale-product state of a data product or the payment, carried from the module rule VR-S9-007-1 | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | The role lacks the Partner portal right R the reads declare | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the fee is accrued | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-35 Placement and allocation and SCR-34 Partner list in their list states, before and after the fee, through the gateway-bff composite route (DP-19). The route calls rwb-partner for the instruction, the partner and the fee, rwb-case for the case and rwb-payment for the payment; this baseline fixes the rwb-partner answers only, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON. The legacy screen table gives both screens "Loading; list", and the FSD gives SCR-35 as "Work placed with partners by rule, with recalls and re-selection" and SCR-34 as "Partners, contracts, panel status and scorecards": neither is described as a calculation screen, so the place of the fee on the two screens is Not specified in the source documents (GAP-3120; ASM-5405). The refusal, stale-product and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-035-01 | AC1, AC3 | Contract | The placed case `RW-2026-000611` on the fake; the contract half answers the two reads, the elements and the consumed rows |
| TC-E6-035-02 | AC2, AC5 | Contract | The elements and the lists; the contract half answers the sixteen properties, the four lists, the fee placeholders and the decision element |
| TC-E6-035-03 | AC4 | Contract | A role without the Partner portal right R and a malformed query; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-035-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S9-E6035-CON-01 | AC1 | Contract | The document validates; the two reads, the base, the query parameters, the `Idempotency-Key` rule and the three error answers are present |
| TC-S9-E6035-CON-02 | AC2 | Contract | The three elements validate with their seven, nine and page properties, the twelve required flags, the four lists and the fee placeholders |
| TC-S9-E6035-CON-03 | AC3, AC4 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-`payment`, no-account-value and no-rule-row boundary; the 29 identities |
| TC-S9-E6035-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema and the `feeAmount` rule; the six fakes match the document and a drifted fake fails the build |
| TC-S9-E6035-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the four write operations left to other stories, and the absence of a published event, a consumed event, a second topic and a Schedule |

The four legacy cases are those of RWB-E6-035 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E6035-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S9-E6035-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the schedule basis, the tiers, the rounding, the four lists, the rights and the package version stay reference data and rule data, never a schema default, an enumeration member or a constant of the code.
- No personal data and no account value in a schema, an example or a fake: identifiers, codes, dates, amounts, versions and a reference only, and every example is synthetic.
- The payment stays with rwb-payment and the case with rwb-case: the document declares no payment property, no `recovery_case` property, no `v_ace_*` path and no ACE table read (BR3).
- The rule rows stay with rwb-decision: the document declares no rule row, no threshold and no rule ID set.
- The fee schedule stays with the reference-data owner: the document declares it as consumed with its version and declares no rate, tier, basis or rounding (BR4).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner; the four write operations belong to other stories and are never declared here (BR12).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule, a Quartz row or a fee command.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-07 | The requirement this feature serves is Not specified in the source documents (GAP-3120; ASM-5412): TSD S9 T8 maps every REQ-S9 row to FEAT-PRM-01, FEAT-PRM-08 or a placeholder, and maps REQ-S9-004 — whose text names the contracted fee schedule — to FEAT-PRM-01 | The two reads, the three elements and the four consumed rows | TC-E6-035-01, TC-E6-035-02, TC-S9-E6035-CON-01, TC-S9-E6035-CON-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E6035-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S9-E6035-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S9-E6035-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the `feeAmount` rule | TC-S9-E6035-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-035, disposition Split (rework); feature FEAT-PRM-07 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S9-E6035-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-035; FSD S9 Partner management v3 A1.2, A2.7, A2.7.2, A2.7.3 and Features (FEAT-PRM-02, FEAT-PRM-07, FEAT-PRM-09); TSD S9 Partner management v2 T2, T3.0, T3.1, T3.2, T3.3, T5.1, T5.2, T5.3, T6.1, T8 and T-A; API Specification v4 elements Partner and PartnerInstruction; Business Rules and Routing Logic v4 row R-WO-37 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S9-E6035-CON-01 to -05 |
| Feature and screens | FEAT-PRM-07, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | VR-S9-007-1 and BR-S9-007 of the module; no row expresses the fee basis (ASM-5405, ASM-5406) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the reads, the match, the calculation and the record: RWB-S9-E6035-APP.
- The contracted fee schedule as reference data, its authoring, its versioning and its approval: FEAT-PRM-02 and the reference-data owner in rwb-case, whose rows this baseline declares as consumed and faked (ASM-5405, ASM-5407).
- The payment of record and its ALS and GL leg: rwb-payment (P8), whose row this baseline declares as consumed and faked (ASM-5404).
- The case of record and its route states: rwb-case (P3). The rule package and its rows: rwb-decision (P7) (ASM-5406).
- The four write operations of the module and their behaviour: the placement, acceptance, result and fee-approval stories; the fee claim and its approval are FEAT-PRM-09 in E7 (ASM-5413).
- The names, the formats and the basis of the fee properties and the schedule: the business lead confirms them at the baseline review and the placeholder stands until then (GAP-3120; ASM-5405).
- The gateway-bff composite route and the screen field lists of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- An event that carries the fee to another service: none exists, so none is declared (ASM-5409).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
