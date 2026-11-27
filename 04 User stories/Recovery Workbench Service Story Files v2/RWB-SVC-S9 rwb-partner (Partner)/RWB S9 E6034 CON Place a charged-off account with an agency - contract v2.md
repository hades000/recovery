# RWB-S9-E6034-CON Place a charged-off account with an agency - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6034-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Contract version | Major version 1 on `/api/recovery/partner/v1`; additive change only within major version 1 (BR10) |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; Not specified in the source documents (DOR-RWB-S9-E6034-CON-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S9-E6034-CON-14) |
| Depends on (build) | None |
| Contract dependencies | The case read of rwb-case (P3) and the placement-rule read of rwb-decision (P7), both in 12.2 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the placement of a charged-off account with an agency in rwb-partner, split from RWB-E6-034. It fixes the three operations of this key on `/api/recovery/partner/v1` (DP-13) — API-S9-001 `GET /partners`, API-S9-002 `POST /cases/{caseId}/instructions` with the `Idempotency-Key` header and API-S9-003 `GET /partner/instructions` — the `Partner`, `PartnerInstruction` and `InstructionRequest` elements over the columns of DF-PRT-001 to DF-PRT-016, the lists of TSD S9 T3.2, the consumed rows of the rwb-case case read and the rwb-decision placement-rule read, the decision-record element of DP-03, the rights of TSD S9 T6.1, the EV-20 event element, the fakes and the absence tests. The legacy story names two read endpoints and no write operation; `partner_user` has no field catalog; no source publishes the property list of `InstructionRequest` or of the answer and no message ID per condition; the plan's C row is empty while two rows are consumed; DP-04 and DP-09 are absent; and no requirement row traces to FEAT-PRM-06 (GAP-3118; ASM-5394, ASM-5395, ASM-5396, ASM-5397, ASM-5398, ASM-5402). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S9-E6034-CON-L228, X20 RWB-S9-E6034-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the placement of a charged-off account with an agency in rwb-partner — the three operations of the key on `/api/recovery/partner/v1`, the partner, instruction and request elements with their required flags, the lists, the two consumed rows, the decision-record element, the EV-20 event element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-35, SCR-34, the partner portal and the wave 4 harness build against one fixed, testable contract on Day 1, and an element, a list, a right or an answer shape can never drift between rwb-partner, rwb-case, rwb-decision and rwb-access without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy placement of RWB-E6-034 crossed four boundaries at once — the case and its post charge-off state, the panel and its scores, the rule version in force and two screens — and it named two read endpoints only, with no element published for either and no operation for the act that places the account. The target splits them: rwb-case owns the case and its route states, rwb-decision owns the placement rows, rwb-access owns the capability area and the right, and rwb-partner owns the partner, the instruction and the placement record. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition, and that the partner portal in front of it is the shared partner gateway and not part of this document.

Five points are carried as gaps and assumptions rather than decided quietly: the property list of `InstructionRequest` and of the answer, and the field catalog of `partner_user`, have no source (ASM-5394, ASM-5395); the plan's C row is None while the baseline declares two consumed rows, and DP-04 and DP-09 are absent from the pattern set (ASM-5396, ASM-5397, ASM-5398); the legacy permission table gives right R while the placement needs C, and the FSD's also-uses role has no matrix row (ASM-5399); the screens are list states with no placement form (ASM-5400); and no requirement row traces to FEAT-PRM-06 (ASM-5402).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention, the multipart rule and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `partner`, `partner_instruction` and `partner_user` are S9's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The six operations are published: TSD S9 T-A.1 gives API-S9-001 to API-S9-006 with their access, their first epic and their idempotency rules, and T-A.2 gives the error set as 401, 403, 404, 409, 415, 422 and 503 with the request and answer element names. This baseline fixes the three the placement key uses and names the other three as their stories' (GAP-3118; ASM-5394).
- The rwb-case case row and the rwb-decision placement-rule row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3118; ASM-5396, ASM-5398).
- The placement rows R-WO-29 to R-WO-32 and their version are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `partner` and `partner_instruction` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. `partner_user` has no field catalog and is not declared (ASM-5395).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for the three placement operations of API-S9-001, API-S9-002 and API-S9-003, with their rights, their idempotency rules and their error responses.
2. Fix the `Partner` element over the columns of DF-PRT-001 to DF-PRT-007 and the `PartnerInstruction` element over the columns of DF-PRT-008 to DF-PRT-016, with the required flags TSD S9 T3.1 gives.
3. Fix the `InstructionRequest` element and the paged `InstructionPage` answer, marking with the placeholder what the sources do not give.
4. Fix the consumed rows: the case read of rwb-case and the placement-rule read of rwb-decision with its version.
5. Record the decision-record element of DP-03, written before the instruction is sent, and the EV-20 event element with its IDs-only payload.
6. Record the rights of the three operations, the naming baseline and the rule that no value is a constant of the code; record the four lists of TSD S9 T3.2 as they stand.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the shapes, the scope, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the declared event of this step only.
9. Tag the baseline and hand it to RWB-S9-E6034-APP, to the stories that share the three operations, to SCR-35, SCR-34 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | The property list of `InstructionRequest` or of the answer is declared as an enumeration taken from no source | The vocabulary test fails the build: no source publishes either list | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares a consumed event, a second topic, a Schedule or an event of another step | The absence test fails the build | None | AC7 |
| X8 | The rights of the operations are not the ones TSD S9 T6.1 and T-A.1 give them | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S9 appendices, the API Specification and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The names of the request properties and the example values are settled in the baseline review; the base, the operations, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E6034-APP, the stories that share the three operations, SCR-35, SCR-34, the partner portal and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, four fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the placement of a charged-off account with an agency

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_instruction and partner_user is S9, of recovery_case and timer is P3, and of every v_ace_* view and rule_row is P1 and P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three placement operations are declared with their rights and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/instructions as API-S9-002 with an InstructionRequest body in and a PartnerInstruction answer carrying the instruction reference and the status SENT, under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then it declares GET /partners as API-S9-001 with a Partner[] answer, and GET /partner/instructions as API-S9-003 with an InstructionPage answer, each with a query, a scope and the Partner portal right R
    Then API-S9-002 declares the Idempotency-Key header and the Partner portal right C, and the two reads declare no idempotency
    Then the answers 400, 401, 403, 404, 409, 415, 422 and 503 are declared with one envelope and one message ID per condition
    Then the accept, results and invoices operations of the same base are named as the stories of the result and the fee, and no operation of another service is declared

  Scenario: AC2 The partner, instruction and request elements and the lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S9 T3.1, T3.2 and T-A.2, and with the API Specification v5
    Then the Partner element declares the seven columns of DF-PRT-001 to DF-PRT-007: id, partnerCode, partnerName, partnerType, panelStatus, contractEnd and score
    Then the PartnerInstruction element declares the nine columns of DF-PRT-008 to DF-PRT-016: id, caseId, partnerId, instructionType, instructedAt, dueAt, status, resultCode and feeAmount
    Then the required flags are id, partnerCode, partnerName, partnerType and panelStatus on the partner element, and id, caseId, partnerId, instructionType, instructedAt and status on the instruction element, and the other properties are optional
    Then the lists are LOV-INSTRUCTION COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST and SELL, LOV-INSTR-STATUS SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED, LOV-PANEL ACTIVE, ON_NOTICE, SUSPENDED and EXITED, and LOV-PARTNER-TYPE AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, copied from TSD S9 T3.2 and published unchanged
    Then the InstructionRequest element declares the partner reference, the instruction type and the due-at time of the legacy and FSD field catalog, with the property names of the source carrying the placeholder Not specified in the source documents (GAP-3118; ASM-5394)
    Then the InstructionPage answer is declared as a page of instruction elements with the page and size parameters of TSD S9 T-A.2
    Then no property is added for a rule row, an ACE extract, a case state, a contact value or a fee schedule

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case and its post charge-off state
    Then the placement-rule read is declared as consumed from P7 rwb-decision, with the D9 rows R-WO-29 to R-WO-32 and their version
    Then the operation names of the two rows are Not specified in the source documents (GAP-3118; ASM-5396, ASM-5398) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no timer property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S9 T-A.1, T-A.2 and T6.1
    Then API-S9-002 declares Partner portal right C with the scope applied, and API-S9-001 and API-S9-003 declare right R
    Then RW-AGENCYMG holds CRUDA and RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and RW-GUARANT hold CRU, and those seven identities are the only holders of C
    Then the legacy permission table's eight roles "and 21 more" resolve to the fifteen further staff roles and the six PT-* identities of the matrix, and no other identity places an account
    Then the Credit Administration officer, the FSD's also-uses role, has no matrix row and therefore no right until the access owner adds one (ASM-5399)
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record and event elements are declared (new, D-RCV-60)
    Given the record and event section of the baseline
    When it is compared with the library schema and with TSD S9 T2 and T5.3
    Then one decision record is declared per placement with the case reference, the partner reference, the instruction type, the picked agency, the rule version in force and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the instruction is sent, and a failed write leaves everything unchanged with MSG-P7-003
    Then EV-20 InstructionIssued is declared on rwb.partner.events.v1 with its retry and .dlt topics, with IDs only: the case reference, the partner reference and the instruction reference
    Then EV-21 PartnerResultSubmitted is named as the result story's and no second event, no consumed event and no inbox row is declared
    Then the record and the event carry no rule row, no personal data and no fee amount

  Scenario: AC6 The four fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the post charge-off case at its placement decision, and a case that is not post charge-off
    Then the rwb-decision fake answers R-WO-29 to R-WO-32 at their version and a package that cannot answer
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-35 and SCR-34 answers before and after the placement
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_partner, the login is rwb_partner, the base is /api/recovery/partner/v1, the topic is rwb.partner.events.v1 with its retry and .dlt topics, the queue is rwb-partner in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.partner
    Then the tables named as owned are partner, partner_instruction and partner_user, and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then partner_user is declared without a field catalog, because no source gives one (ASM-5395)
    Then the document declares one published event of this step, no consumed event, no second topic and no Schedule, and the service's job list is empty
    Then the absence test fails a build that adds a consumed event, a second topic, a Schedule, a v_ace_* read or a property of another owner's fact
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S9-E6034-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The three operations are the three the legacy story names as its endpoints plus the one the FSD's A2.6 describes; the two legacy endpoints are the reads and the write is API-S9-002 (GAP-3118; ASM-5394).

Scenario: AC8 Every rule of section 8 maps to a declared element, a consumed row, a right or a placeholder, and a rule with no declaration fails the build (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The partner and instruction rows are rwb-partner's, and the contract declares the fields and the required flags on the `Partner`, `PartnerInstruction` and `InstructionRequest` elements only | TSD S9 T3.1, T-A.2; context pack ownership rows (tables `partner`, `partner_instruction`, `partner_user`) |
| BR2 | The placement record is declared as an element written before the instruction is sent, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S9 T2; legacy AC1 and AC2 |
| BR3 | The case stays with rwb-case: the contract declares the case read as consumed, declares no `recovery_case` property, no case state property and no `v_ace_*` property, and describes no case write | DP-05, DP-11; TSD S9 T5.2; ASM-5398 |
| BR4 | The placement rows stay with rwb-decision: the contract declares the package read as consumed and declares no rule row, no threshold, no timer and no rule ID set as a property | R3 default ruling (rule package registry); ASM-5396 |
| BR5 | One event of this step is declared, EV-20 `InstructionIssued`, and EV-21 belongs to the result story; the outbox library of DP-09 is recorded as an absent H row | TSD S9 T5.3; context pack ownership rows (events EV-20, EV-21); ASM-5397 |
| BR6 | API-S9-002 declares the `Idempotency-Key` and stores its answer; API-S9-001 and API-S9-003 declare it not applicable | TSD S9 T-A.2 |
| BR7 | The property names of `InstructionRequest` and of the paged answer, and the field catalog of `partner_user`, are declared with a placeholder, because no source publishes a name, a format or a list | ASM-5394, ASM-5395; FSD S9 A2.6.3.2; TSD S9 T3.1, T3.2, T-A.2 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, dates, list values and an amount only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The rights are the Partner portal rows of TSD S9 T6.1: C on the issue, R on the two reads, held by the seven identities with C and the 29 identities with R | TSD S9 T6.1, T-A.1; legacy permission table of RWB-E6-034; ASM-5399 |
| BR13 | The six instruction statuses and the four lists are declared as the vocabulary of the answer and published unchanged from TSD S9 T3.2; they are read as reference data under DP-06 and DP-07, and the parameters they read are Not specified in the source documents (DOR-RWB-S9-E6034-CON-20) | TSD S9 T3.2; FSD S9 A2.6.3.2; DP-06; DP-07 |
| BR14 | The placement's D9 states `PLACEMENT_DECIDED` and `PLACED_WITH_AGENCY` are declared as another route set's vocabulary and move no case state from this service; S7 decides the placement treatment and posts the recovery, and this service issues and tracks the placement instruction and holds the panel, the terms and the recall (GAP-1854) | Business Rules and Routing Logic v4 rows R-WO-29, R-WO-30; ASM-5398 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the elements, the lists, the consumed rows, the record and event elements and the fakes are described | In review |
| In review | Consumer sign-off | RWB-S9-E6034-APP, the stories that share the three operations, SCR-35, SCR-34, the partner portal, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access accept the document and the fakes | Baselined |
| Baselined | The request property names and the `partner_user` catalog are confirmed | The business lead and the access owner replace the placeholders inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional note on the instruction | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value becomes an enumeration over an unconfirmed set | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a second topic, a consumed event, a Schedule or an operation of another owner | In review |

The state machine the document describes is the app story's: the instruction runs `SENT` to `RECALLED` under the step's own writes and the accept, result and recall stories', and the D9 states belong to the write-off route set of 27 states in the States sheet of the Business Rules and Routing Logic v4. This baseline fixes the vocabulary and the answer shapes and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-partner | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed request properties and the `partner_user` catalog, and the correction of the plan rows the baseline consumes, including the two consumed rows and the absent DP-04 and DP-09 rows |
| Business lead | Confirms the request property names and the due-at rule that replace the placeholders |
| Access owner in rwb-access | Confirms the Partner portal rights of the three operations and the row the FSD's also-uses role needs (ASM-5399) |
| Consuming teams (the app story, the stories that share the three operations, SCR-35, SCR-34, the partner portal, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-partner login (DP-02)" and is not part of this baseline. The partner gateway in the DMZ is the edge contract's and is not declared here. The rwb-access authorise check that enforces these rights under DP-08 is named as Not specified in the source documents (DOR-RWB-S9-E6034-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Partner element | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | The seven columns of DF-PRT-001 to DF-PRT-007: `id`, `partnerCode`, `partnerName`, `partnerType`, `panelStatus`, `contractEnd` and `score` |
| Instruction element | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | `PartnerInstruction`: `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt`, `dueAt`, `status`, `resultCode` and `feeAmount` |
| Issue element | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | `InstructionRequest`: the partner reference, the instruction type and the due-at time; its property names carry the placeholder Not specified in the source documents (GAP-3118; ASM-5394) |
| Page element | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | `InstructionPage`: a page of instruction elements with the `status`, `page` and `size` parameters of TSD S9 T-A.2 |
| Required flags | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | `id`, `partnerCode`, `partnerName`, `partnerType` and `panelStatus` on the partner element; `id`, `caseId`, `partnerId`, `instructionType`, `instructedAt` and `status` on the instruction element; `id` is read-only as the API Specification v5 gives it, and the other properties are optional |
| Lists | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | LOV-INSTRUCTION `COLLECT`, `FILE_SUIT`, `ENFORCE`, `APPRAISE`, `REPOSSESS`, `LIST`, `SELL`; LOV-INSTR-STATUS `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE`, `RECALLED`; LOV-PANEL `ACTIVE`, `ON_NOTICE`, `SUSPENDED`, `EXITED`; LOV-PARTNER-TYPE `AGENCY`, `LAW_FIRM`, `VALUER`, `AUCTION_VENDOR`, `BROKER`, `DEBT_BUYER`, `AMC`, `RAMC`, all copied from TSD S9 T3.2 |
| Event data | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | EV-20 `InstructionIssued` with IDs only: the case reference, the partner reference and the instruction reference (§12.3) |
| Decision record | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | DF-DEC-001 to DF-DEC-018 through the local library, written before the instruction is sent (DP-03) |
| Case and rule facts | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here |
| Not declared here | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | `partner_user` has no field catalog in TSD S9 T3.1 and is named without properties (ASM-5395); `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) |
| Consumed fields with no source | Not specified in the source documents (DOR-RWB-S9-E6034-CON-7) | The operation names of the case read and the rule read, and the property names of `InstructionRequest`: Not specified in the source documents (GAP-3118; ASM-5394, ASM-5396, ASM-5398) |

The field-level types, lengths and required flags of the added element properties are settled in the baseline review; this story fixes the element names, the required flags of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in, `PartnerInstruction` out at status `SENT`; the operation that places the account | Partner portal, right C, scope applied | `Idempotency-Key` header |
| GET | `/partners` (API-S9-001) | `Partner[]` out with the panel status and the score | Partner portal, right R, scope applied | Not applicable |
| GET | `/partner/instructions` (API-S9-003) | `InstructionPage` out for the caller's own firm | Partner portal, right R, scope applied | Not applicable |

API-S9-002 answers 400, 401, 403 with MSG-P4-002, 404 for a case that is not on the reference, 409 for a case that is not at its placement decision or a partner that is not on the panel, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The paths, the operation ids, the element names, the rights and the error codes are published in TSD S9 T-A.1 and T-A.2; the property list of the request carries the placeholder (GAP-3118; ASM-5394). The accept, results and invoices operations of the same base — API-S9-004, API-S9-005 and API-S9-006 — belong to the E4 instruction stories, RWB-S9-E6033-APP and the Epic 6 invoice story, and none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3118; ASM-5398)) | `/api/recovery/case/v1` | P3 rwb-case | The case and its post charge-off state; read only, faked |
| The placement-rule read in force (operation name Not specified in the source documents (GAP-3118; ASM-5396)) | `/api/recovery/decision/v1` | P7 rwb-decision | The D9 rows R-WO-29 to R-WO-32 at their version; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3118; ASM-5396, ASM-5398).

#### 12.3 Events published

| Event | Name | Topic | Payload | Fan-out |
|---|---|---|---|---|
| EV-20 | `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` with its retry and `.dlt` topics | IDs only: the case reference, the partner reference and the instruction reference; no personal data | The consumer set is Not specified in the source documents (GAP-3118; ASM-5397) |

EV-20 is this step's event and EV-21 `PartnerResultSubmitted` belongs to RWB-S9-E6033-APP (context pack, ownership rows: EV-20 and EV-21; TSD S9 T5.3). This baseline declares one published event, its envelope and its IDs-only payload, and no producer group row is written by this story. One event per instruction and one producer group: RWB-S9-E6031-APP issues the same event for a scorecard allocation, so a second event, topic or outbox is a forbidden element. The outbox that relays it is the platform library object of DP-09, which the pattern set for this key does not carry, so `RWB-PLT-TE006-CON` is recorded as an absent H row (ASM-5397).

#### 12.4 Events consumed

None. The placement's trigger is the officer's confirmation on SCR-35 after the post charge-off treatment decision of R-WO-29, and the FSD declares no background event for the feature (FSD S9 A2.6.4.4). This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, continues-as-new across the instruction's life | `rwb-partner`, namespace Not specified in the source documents (CG-ALL-11908) | The instruction's status machine; its signals and its outcome are declared, not built |
| `issueInstruction` | Activity, the one placement step; the architecture names it as the activity other routes call on rwb-partner | `rwb-partner` | The case reference, the partner reference, the instruction type and the rule version in; the instruction reference and its status out |

No child workflow and no second workflow exists in this service, and the service owns one workflow and no job in the context pack's ownership rows. The activity name comes from the Arch v5 slide 12 notes, so no name is invented, and no activity is registered by this story. Workflow ID form: Not specified in the source documents (CG-ALL-11909). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-11909).

#### 12.6 Schedules

None. The placement is an officer-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The service's job list is empty in the context pack's ownership rows, and the hold timer of R-WO-31 and the recall timer of R-WO-34 are the write-off stage's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| partner | S9 (`rwb_partner`) | The outside firm on the panel, its type, panel status, contract end and score; the row the partner element is drawn from, never written by a placement |
| partner_instruction | S9 (`rwb_partner`) | Work placed with a partner on a case; the row the instruction element is drawn from, written at `SENT` by the app story |
| partner_user | S9 (`rwb_partner`) | The panel user of the partner; named without a field catalog (ASM-5395) |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the placement (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of API-S9-002 and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The relay of EV-20 (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The post charge-off case of `RW-2026-000731` at `PLACEMENT_DECIDED`, and a case that is not post charge-off | AC1, AC3, AC6 |
| rwb-decision placement-rule fake | The D9 rows R-WO-29 to R-WO-32 at their version in force, and a package that cannot answer | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-35 and SCR-34 answers for the case of `RW-2026-000731` and the panel of `AG-014`, before and after the placement | AC6 |

The fakes are test-only and are replaced by the real services in SIT, and the partner portal answers through them in the harness. The operation names of the case read and the rule read carry the placeholder until their owners confirm them (GAP-3118; ASM-5396, ASM-5398).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | API-S9-001, API-S9-002 and API-S9-003 on `/api/recovery/partner/v1`; the case read and the rule read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | EV-20 `InstructionIssued` on `rwb.partner.events.v1` with IDs only; the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `InstructionWorkflow` and `issueInstruction` on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no partner and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and four fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the instruction is sent. DP-13 moves the base of the legacy paths and gives the three operations their home. DP-19 sits behind SCR-35 and SCR-34, whose screen models are the edge contract's. DP-04, DP-05 and DP-09 are not in the pattern set: the placement rows are declared as a consumed row rather than an embedded kit, the case as another service's fact and never a view, and the outbox as a library row the pattern table does not carry (GAP-3118; ASM-5396, ASM-5397, ASM-5398).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that EV-20 needs, and the Drools kit row `RWB-PLT-E1072-CON` that a rule evaluation would add; the rule-evaluation row of rwb-decision is not named, as no story of that key exists. The two consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the three operations of AC1 with their rights, the `Idempotency-Key` rule and the eight error answers, and validate the additive rule in the pipeline.
2. Write the `Partner` element with its seven properties and five required flags, the `PartnerInstruction` element with its nine properties and six required flags, and the four lists of AC2.
3. Write the `InstructionRequest` element and the `InstructionPage` answer with their placeholders.
4. Record the case row and the package row of AC3 with their owner, their budget and their placeholders.
5. Record the rights and the error envelope of AC4.
6. Record the decision-record element and the EV-20 element of AC5, and validate the record against the library schema.
7. Publish the four fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-partner-v1.yaml`, the four elements, the contract README rows for the two consumed rows and their placeholders, and the four fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and RWB-S9-E6034-APP, the stories that share the three operations, SCR-35, SCR-34, the partner portal and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, the partner reference or the instruction type among them, or a body fails schema validation or the multipart rule | Enter {field}. |
| MSG-P4-002 | The role lacks the Partner portal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the instruction is sent | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The legacy table carries no module message of its own, so none is declared.

### 15. Screens and states

The contract serves SCR-35 Placement and allocation and SCR-34 Partner list in their list states, before and after the placement, through the gateway-bff composite route (DP-19). The route calls rwb-partner for the panel, the scores, the instructions and the issued instruction, and rwb-case for the case and its placement decision; this baseline fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-35 "Loading; list" and SCR-34 "Loading; list". The SCR-34 states are loading and list; its empty, error and no access states are Not specified in the source documents (CG-ALL-11911). The SCR-35 states are loading and list; its empty, error and no access states are Not specified in the source documents (CG-ALL-11912). Neither screen is described as a placement form, so the form in which the officer confirms the placement, its field list and the place of the placement action are Not specified in the source documents (GAP-3118; ASM-5400). The refusal, not-post-charge-off, not-on-panel and not-recorded states read the messages of section 14 on the same route. The empty, error and no-access states of SCR-35 and SCR-34 are Not specified in the source documents (DOR-RWB-S9-E6034-CON-10); the loading state is the legacy "Loading; list" given above.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-034-01 | AC1, AC2 | Contract | The post charge-off case of `RW-2026-000731` on the fake; the contract half answers the three operations, the partner and instruction elements and the four lists |
| TC-E6-034-02 | AC2, AC5 | Contract | The instruction element and the request; the contract half answers the nine properties, the six required flags, the placeholders, the record and the EV-20 element |
| TC-E6-034-03 | AC4 | Contract | A role without the right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-034-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S9-E6034-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the rights, the `Idempotency-Key` rule and the eight error answers are present |
| TC-S9-E6034-CON-02 | AC2 | Contract | The three elements validate with their seven, nine and three properties, the required flags and the four lists |
| TC-S9-E6034-CON-03 | AC3, AC4 | Contract | The two consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary; the rights and the 29 identities |
| TC-S9-E6034-CON-04 | AC5, AC6 | Contract | The record element matches the library schema; the EV-20 element has an IDs-only payload; the four fakes match the document and a drifted fake fails the build |
| TC-S9-E6034-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the `partner_user` placeholder and the absence of a consumed event, a second topic and a Schedule |
| TC-S9-E6034-CON-06 | AC7 | Contract | The six tables of §12.7 at their boundary: each is owned or named only as an answer, and no foreign key leaves the schema |
| TC-S9-E6034-CON-07 | BR1 to BR14 | Contract | The fourteen rules of §8 each map to a declared element, a consumed row, a right or a placeholder; a rule with no declaration fails the build |
| TC-S9-E6034-CON-08 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S9-E6034-CON-AC8) |

The four legacy cases are those of RWB-E6-034 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S9-E6034-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The eight cases `TC-S9-E6034-CON-01` to `-08` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the placement rows, the panel statuses, the partner types, the instruction types and statuses, the service level, the right and the rule version stay rule rows and reference data, never a schema default, an enumeration member or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, dates, list values and an amount only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case state property and no `v_ace_*` path (BR3).
- The rule rows stay with rwb-decision: the document declares no rule row, no threshold and no timer.
- The partner row is read, not written: no element declares a write to the panel status, the score or the contract end.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-partner; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a consumed event, a second topic, a Schedule, a Quartz row or a data-lake extract.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-PRM-06 | The requirement this feature serves is Not specified in the source documents (GAP-3118; ASM-5402): TSD S9 T8 maps every REQ-S9 row to FEAT-PRM-01 or FEAT-PRM-08 | The three operations, the three elements and the two consumed rows | TC-E6-034-01, TC-E6-034-02, TC-S9-E6034-CON-01, TC-S9-E6034-CON-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E6034-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | EV-20 and the outbox library that relays it | TC-S9-E6034-CON-04, TC-S9-E6034-CON-05 |
| ADR-019 | Edge: gateway-bff and partner gateway | The composite route behind SCR-35 and SCR-34, and the partner portal outside this document | TC-S9-E6034-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S9-E6034-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S9-E6034-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-034, disposition Split (rework); feature FEAT-PRM-06 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S9-E6034-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-034; FSD S9 Partner management v3 A1.1, A1.2, A2.6, A2.6.2, A2.6.3 and A2.6.4; TSD S9 Partner management v2 T2, T3.1, T3.2, T3.3, T4, T5.2, T5.3, T6.1, T6.2, T8 and T-A; API Specification v5; Business Rules and Routing Logic v4 rows R-WO-29 to R-WO-32; Recovery Workbench Epics 3 to 8 Specification v3 row FEAT-PRM-06 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S9-E6034-CON-01 to -05 |
| Feature and screens | FEAT-PRM-06, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | R-WO-29 to R-WO-32 governed in rwb-decision; S9 owns no route set (ASM-5396) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operations, the placement step, the record write and the event: RWB-S9-E6034-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose row this baseline declares as consumed and faked (ASM-5398).
- The authoring, testing, approval and versioning of the placement rows R-WO-29 to R-WO-32: rwb-decision (P7) (ASM-5396).
- The property names of `InstructionRequest`, the panel service level and the field catalog of `partner_user`: the business lead and the data steward confirm them at the baseline review and the placeholders stand until then (GAP-3118; ASM-5394, ASM-5395).
- The accept, results and invoices operations of the same base: the E4 instruction stories (API-S9-004), RWB-S9-E6033-APP (API-S9-005) and the Epic 6 invoice story (API-S9-006). The onboarding, the panel, the allocation and the override: RWB-S9-E6029-APP to RWB-S9-E6032-APP.
- The partner portal sign-in, its multi-factor rule and the partner gateway in the DMZ: the edge contract and the ACE Common sign-in (FSD S9 NFR-049, NFR-050).
- The gateway-bff composite route and the field list of SCR-35 and SCR-34: RWB-PLT-N001-CON and the edge stories.
- The requirement row of FEAT-PRM-06: no source publishes one, and the trace waits for the E6 BRD and the PRD (GAP-3118; ASM-5402).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
