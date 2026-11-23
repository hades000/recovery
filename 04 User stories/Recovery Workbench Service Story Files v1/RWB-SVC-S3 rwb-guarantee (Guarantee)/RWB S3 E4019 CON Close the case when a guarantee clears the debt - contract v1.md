# RWB-S3-E4019-CON Close the case when a guarantee clears the debt - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-019 split out for rwb-guarantee. The document publishes the `GuaranteeClose` element recorded against the guarantee claim, the read rule of the two ACE views with the batch date and the no-copy ban, the close rules of the GUARANTEE route set, the stage report that closes the case or returns the balance, the claim operation and its base, the decision-record group, the versioning rule and the fakes. The two legacy operations of TSD S3 T-A.1 are re-based to `/api/recovery/guarantee/v1` (DP-13) and the element rides the claim representation the claim contract publishes; the balance and the payments stay in ACE and are read only (DP-05); the closed claim is read through the gateway-bff composite route (DP-19). It is published on Day 1 at status Draft (realignment v1). No source gives the guaranteed share or the balance after it a field or a governed row (GAP-2731; ASM-4537), gives `LOV-CLAIM-STATUS` a closed value (GAP-2732; ASM-4538), gives the subrogation position a record (GAP-2733; ASM-4539), names the trigger of the feature (GAP-2734; ASM-4540) or resolves which login reads the ACE views (GAP-2735; ASM-4541). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4019-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-guarantee**, I want **the published contract of the guarantee close — the `GuaranteeClose` element recorded against the claim, the read rule of the balance and payment views with the batch date and the no-copy rule, the close rules of the GUARANTEE route set with their conditions and to states, the stage report that closes the case or returns the balance, the claim operation and its base, the decision-record group, the versioning rule and the fakes — instead of the monolith's method reading the `recovery` schema and `rule_row` in one process**, so that **the application story of this feature, the sibling claim stories of this service and the wave 3 integration harness build and test on Day 1 without a P1, P7 or rwb-case deployment and without a production ACE balance, and no reader of a closed guarantee depends on a position that was never defined**.

This is the contract slice of legacy RWB-E4-019. It owns:

- the `GuaranteeClose` element: the claim and case identifiers, the closing time, the closing basis, the claim status and paid amount, the guaranteed share, the balance after the share with its as-at date, and the rule and set versions, with the rule that it is recorded against the claim and against nothing else;
- the read rule of the balance and payment evidence: the views `recovery.v_ace_account`, `recovery.v_ace_payment` and `recovery.v_ace_batch_status`, the columns consumed, the batch date, the no-copy ban and the availability answers (DP-05);
- the close rules: the four rows of the GUARANTEE route set that end the claim — R-GUA-19, R-GUA-25, R-GUA-26 and R-GUA-27 — their from states, events, conditions and to states, and the two condition tests of the balance after the guaranteed share (GAP-2731; ASM-4537);
- the stage report: the outcome, the reason code and the 5 working day owner task of R-GUA-27 reported to the parent `CaseWorkflow`, the case statuses the parent applies, and the statement that the case is closed by rwb-case and never here (GAP-2732; ASM-4538);
- the claim operation and its base: `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}` (API-S3-002) on base `/api/recovery/guarantee/v1`, of which this element is a component, with the right, the errors and the compatibility rule (DP-13);
- the decision-record group of the same transaction, named as the local record of RWB-PLT-E1027-CON, with its refusal and failure messages;
- the guard answers — MSG-P1-001 for a stale data product, MSG-GEN-001 for a missing value, MSG-GEN-006 for a view that does not answer and MSG-P4-002 for a role without the right — the versioning and pinning rule, the fakes and the drift test.

It does not own: the close branch of `GuaranteeClaimWorkflow`, the close activity, the three reads, the claim result, the record call and the tests against them, which are RWB-S3-E4019-APP; the four legacy acceptance criteria of RWB-E4-019, which are carried verbatim by RWB-S3-E4019-APP; the claim representation, its create and result operations and its states, which are RWB-S3-E4015-CON and the claim stories of this service; the subrogation position entered by R-GUA-23 and R-GUA-24, which are RWB-S3-E4016-CON; the case status, the case closure, the case task and the case timer, which are rwb-case's; the ACE views and their grants, which are ACE's; the GUARANTEE rule rows, their approval and the central ledger, which are P7 rwb-decision's; the posting and booking of the payment, which are P8 rwb-payment's and the core bank's; and SCR-17 and its composite route, which are the platform edge story's under DP-19.

### 2. Business rationale

In the monolith the close had no contract at all. `GuaranteesAndGuarantorsService` read the balance and the payments from the `recovery` schema, read the GUARANTEE rows from `rule_row`, decided in code and wrote the claim status into `guarantee_claim` and the decision into `decision_log_entry` (TSD S3 T1 and T2). Nothing about that arrangement could be reused or tested alone: the balance was a live join, the policy was a row any module could read, and a closed guarantee had no shape — a reader of it had one option, which was to read the module's tables.

D-RCV-60 replaces three inputs and one output, and the contract is where each of them is written down. The balance and the payment stay in ACE and are read at the batch date from the service's own SELECT-only views (DP-05; D-RCV-35, ADR-010). The close becomes one of governed rows of the GUARANTEE route set, read with the version that decided (R-GUA-19, R-GUA-26, R-GUA-27). The decision becomes a local record in the same transaction (DP-03; ADR-022). And the output becomes an element with a field list, a required flag on each field, a version label and a set of fakes, recorded against the claim the officer already sees.

Two of the things this contract must fix are absences rather than decisions. The guaranteed share and the balance after it have no field in TSD S3 T3.1, no field identifier in the Logical Data Model and no governed row, so the contract states how they are composed — from the balance read at the batch date and the share the answered row names — and refuses to invent a column (GAP-2731; ASM-4537). And the routing logic says "close the guarantee and close the case" while `LOV-CLAIM-STATUS` offers `PREPARING`, `FILED`, `DEFECT`, `PAID` and `REJECTED` and no closed value; the contract therefore fixes the close as the element plus the case status `GUARANTEE_CLOSED` that rwb-case applies, and leaves the claim inside its published list (GAP-2732; ASM-4538).

The legacy key divides cleanly and the division is fixed. This WP delivers the **contract**. The **application** — the branch, the activity, the reads, the claim result and the guard paths — is **RWB-S3-E4019-APP**, and the **four legacy acceptance criteria stay with it**: AC1 to AC4 are listed in its section 7 with their origin tag and are not repeated here. The **cross-service proof** is **RWB-ITG-W3**. Every criterion in section 7 of this document is new and tests only the contract deliverable in this title.

### 3. Preconditions

- The rules whose states, events, conditions and to states the element and the report carry are fixed by the Routing Logic v4: R-GUA-19 (`CLAIM_REJECTED`, `RESUBMISSION_NOT_POSSIBLE`, "the reason is not curable, or claim_deadline has passed", to `RESIDUAL_TO_ROUTE`), R-GUA-25 (`SUBROGATION_POSITION`, `RESIDUAL_REMAINS`, "the balance after the guaranteed share is greater than zero", to `RESIDUAL_TO_ROUTE`), R-GUA-26 (`SUBROGATION_POSITION`, `BALANCE_SATISFIED`, "the balance after the guaranteed share is zero", to `GUARANTEE_CLOSED`) and R-GUA-27 (`DEADLINE_MISSED`, `LOSS_RECORDED`, "the loss amount and the reason are recorded", to `RESIDUAL_TO_ROUTE`). The names are copied into the element and the report, character for character.
- The fields the claim result lands on exist in TSD S3 T3.1: `status` (DF-TRT-022, varchar(12), LOV-CLAIM-STATUS) and `paid_amount` (DF-TRT-021, numeric(18,2)).
- The evidence is fixed in kind: FSD S3 A2.7.3.1 VR-S3-007-1 reads `v_ace_batch_status` for the data-product date, and the legacy data table names `v_ace_account` with DF-ACE-001 to DF-ACE-042 and `v_ace_payment` with DF-ACE-043 to DF-ACE-054. The columns consumed and the grant path are the working read of ASM-4541, and the conflict with Architecture v5 slide 8 is GAP-2735.
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003 (DP-03; RWB-PLT-E1027-CON).
- The element rides the claim representation on base `/api/recovery/guarantee/v1` (DP-13) and is served to SCR-17 through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), so the contract fixes the element and the base, not a second path.
- No source publishes the element's own field list, the share or the position record, or the trigger of the feature (GAP-2731 to GAP-2734; ASM-4537 to ASM-4540). The document is published as that working read, at major version 1 and status Draft (realignment v1).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7) and nothing in this story needs a human sign-off to start (ASM-4542).

### 4. Flow

1. The contract author fixes the `GuaranteeClose` element: its eleven fields, which are required, and the rule that it is recorded against the claim.
2. The author fixes the read rule of the evidence: the three views, the columns consumed, the batch date and the ban on copying.
3. The author fixes the four close rows with their from states, events, conditions, to states and owner roles, and the two condition tests of the balance after the guaranteed share.
4. The author fixes the stage report: the outcome, the reason code and the 5 working day owner task, with the boundary stated — no case row, no case task and no case timer is written here.
5. The author fixes the claim operation and the base it sits on, with the right, the errors and the compatibility rule, and states that the element is a component of the claim representation.
6. The author writes the guard answers with their messages and the decision-record group with the two library messages.
7. The fake set and the drift fixture are generated from the document, and the contract test runs them against it on every change.
8. The document and the fakes are published at v1; RWB-S3-E4019-APP and RWB-ITG-W3 pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published element drops a required field, or adds an optional one a consumer depends on | The schema check fails the build; required and optional fields are as published | None | AC1 |
| X2 | The read rule is published without the batch date, the column list or the no-copy ban, or allows a third view | The read lint and the no-copy check fail the build | None | AC2 |
| X3 | A close row is published with a fixed share, a renamed state or a missing to state | The rule lint fails the build; the share, the states and the conditions are named, never fixed | None | AC3 |
| X4 | The stage report is published as a case write, or without the reason or the owner task | The boundary check fails the build; the report carries the reason and the task and writes no case row | None | AC4 |
| X5 | The claim operation is published on the monolith base, or the element gets a path of its own | The base check fails the build; one base, `/api/recovery/guarantee/v1` (DP-13) | None | AC5 |
| X6 | A breaking change is made to the element, the read rule or a guard answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC6 |
| X7 | A consuming story ships without the drift test, or a fake stops answering the document | The drift test fails the build of the consuming story | None | AC6 |
| X8 | A value a consumer needs is named by no source — the share, the balance after it, the closed claim status or the trigger | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2731; ASM-4537) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | Field order, record widths and the fixture set are open until v1 is frozen; the element, the three views, the four rows, the report and the guards are fixed |
| Valuable | Unblocks the application story and the wave 3 harness on Day 1, and gives the claim stories of this service one definition of a closed guarantee |
| Estimable | One element, one read rule, one rule set, one report, one operation map, one versioning rule and five fakes |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion below is one schema, rule-lint, base check or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: guarantee-close contract of rwb-guarantee

  Background:
    Given the contract document is published with major version 1 on the base of rwb-guarantee
    Given the element is a component of the claim representation and the contract declares no second path
    Given the close is one of the rows of the GUARANTEE route set in force and the evidence is read from recovery.v_ace_account and recovery.v_ace_payment

  Scenario: AC1 The GuaranteeClose element and its required fields are published (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes GuaranteeClose with claimId, caseId, closedAt, closeBasis, claimStatus, claimPaidAmount, guaranteedShare, balanceAfterShare, balancesAsAt, ruleId and ruleVersion
    Then claimId, caseId, closedAt, closeBasis, claimStatus, balanceAfterShare and balancesAsAt are required and claimPaidAmount, guaranteedShare, ruleId and ruleVersion are optional
    Then closeBasis carries RESIDUAL_TO_ROUTE or GUARANTEE_CLOSED of the answered row, claimStatus stays inside LOV-CLAIM-STATUS, and the element maps claimId to DF-TRT-015, caseId to DF-TRT-016, claimStatus to DF-TRT-022 and claimPaidAmount to DF-TRT-021
    Then the element is recorded against the claim and against no other record, and it has no collection, no free-text field and no payment detail
    Then a document that drops a required field fails the schema check

  Scenario: AC2 The balance and payment read rule, the batch date and the no-copy ban are fixed (new, D-RCV-60)
    Given the read rule section of the contract document
    When it is linted against the views and the platform rules
    Then it names recovery.v_ace_account, recovery.v_ace_payment and recovery.v_ace_batch_status as the only ACE objects read, with the columns consumed and the SELECT-only grant
    Then the balance and the payments are read at the ACE batch date and balancesAsAt carries that date
    Then a data product older than today's ACE batch is answered with MSG-P1-001 naming the product and its date
    Then a read that does not answer is answered with MSG-GEN-006 and never with a guessed balance
    Then a rule that reads a fourth ACE object, keeps a copy or names a posting table of rwb-payment fails the lint

  Scenario: AC3 The close rows, their conditions and the guard answers are fixed (new, D-RCV-60)
    Given the rule section of the contract document
    When it is linted against the routing logic and the library contract
    Then R-GUA-19 answers CLAIM_REJECTED with RESUBMISSION_NOT_POSSIBLE to RESIDUAL_TO_ROUTE, R-GUA-26 answers SUBROGATION_POSITION with BALANCE_SATISFIED to GUARANTEE_CLOSED, R-GUA-27 answers DEADLINE_MISSED with LOSS_RECORDED to RESIDUAL_TO_ROUTE and R-GUA-25 keeps the residual at the same state
    Then the balance after the guaranteed share is composed per calculation from the balance read at the batch date and the share the answered row names, and no share, balance or position column is declared for rwb_guarantee
    Then the close adds no value to LOV-CLAIM-STATUS, which stays PREPARING, FILED, DEFECT, PAID and REJECTED, and the closing basis is carried in the element
    Then the claim result and the record are written in one transaction; a refused record names its field with MSG-P7-009 and a failed one stops the action with MSG-P7-003
    Then a missing value is answered with MSG-GEN-001 and a role without the right with MSG-P4-002

  Scenario: AC4 The stage report and the case boundary are fixed (new, D-RCV-60)
    Given the report section of the contract document
    When it is linted against the case boundary and the routing logic
    Then the report carries the outcome, the reason code, the balance tested and the rule version to the parent CaseWorkflow and orders the 5 working day owner task of R-GUA-27
    Then the document states that RESIDUAL_TO_ROUTE and GUARANTEE_CLOSED are case statuses applied by rwb-case, and that the closure of the case is the parent's act and never this service's
    Then the document states that no case row, case task and case timer is created by the consumer and that the case status and the claim deadline are read on the case signal only
    Then the document publishes no Kafka event and records why the event of the step is a stage report

  Scenario: AC5 The claim operation and its base are fixed (new, D-RCV-60)
    Given the operation section of the contract document
    When it is linted against DP-13 and the claim representation
    Then the element is a component of PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId} (API-S3-002 of TSD S3 T-A.1) with right U of the capability area Treatment and offer
    Then the create operation POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims (API-S3-001) with right C is named as the claim stories' and not restated
    Then the monolith base is named nowhere as an own base and a second path for the element fails the build
    Then the errors 401, 403, 404, 409, 422 and 503 and the idempotency rule of the two operations are carried as TSD S3 T-A.2 gives them

  Scenario: AC6 Versioning and fakes separate a compatible change and hold the document (new, D-RCV-60)
    Given the versioning section and the fake set generated from the document
    When a change is proposed and the contract test runs
    Then a backward-compatible change keeps major version 1 while a breaking change to the element, a rule row, the report or a guard answer raises major version 2 and v1 stays readable
    Then the balance fixture answers a cleared balance, a balance above zero after the share, a payment inside the batch, a product dated yesterday and an unreachable view
    Then the case-signal fake answers CLAIM_REJECTED, SUBROGATION_POSITION and DEADLINE_MISSED, and the element fake answers one variant per missing required field
    Then the drift test fails the build of a consuming story on any difference from sections 12 and 13
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is repeated here: **AC1 to AC4 of RWB-E4-019 are carried by RWB-S3-E4019-APP**. Every identifier used above comes from the legacy story, the Routing Logic v4, TSD S3 or the FSD, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The element recorded against the claim carries the claim and case identifiers, the closing time and basis, the claim status and paid amount, the guaranteed share, the balance after the share with its as-at date and the rule and set versions, and nothing else | RWB-E4-019 AC1 to AC3; DF-TRT-015; DF-TRT-022; ASM-4537 |
| BR2 | The basis and the to states are the routing logic's: `RESIDUAL_TO_ROUTE` from R-GUA-19 and R-GUA-27, `GUARANTEE_CLOSED` from R-GUA-26; no name is renamed by the element | R-GUA-19; R-GUA-26; R-GUA-27 |
| BR3 | The balance after the guaranteed share is composed per calculation from the balance read at the batch date and the share the answered row names; no share, balance or position column is declared | GAP-2731; ASM-4537 |
| BR4 | The claim status stays inside `LOV-CLAIM-STATUS` — `PREPARING`, `FILED`, `DEFECT`, `PAID`, `REJECTED`; the close of the guarantee is the element and the close of the case is the case status `GUARANTEE_CLOSED` applied by rwb-case | LOV-CLAIM-STATUS of TSD S3 T3.2; GAP-2732; ASM-4538 |
| BR5 | The balance and the payments are read at the ACE batch date from `recovery.v_ace_account`, `recovery.v_ace_payment` and `recovery.v_ace_batch_status` only, read only, and are never copied into `rwb_guarantee` | DP-05; VR-S3-007-1; D-RCV-35; ADR-010 |
| BR6 | A data product older than today's ACE batch is answered with MSG-P1-001, a missing value with MSG-GEN-001, a view that does not answer with MSG-GEN-006 and a role without the right with MSG-P4-002; none of them is an exception a consumer has to guess | VR-S3-007-1; FSD A2.7.3.1; legacy permission checks |
| BR7 | The claim result and the element are written with the local decision record in one transaction, through `DecisionRecordWriter` with `MANDATORY` propagation | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR8 | The case status, the case closure, the case task and the case timer stay rwb-case's: the report carries the outcome, the reason and the task due date, and the parent applies the rule | DP-01; R-GUA-19; R-GUA-26; ASM-4538 |
| BR9 | One base, `/api/recovery/guarantee/v1`, and one claim representation: the element is a component of the claim operation and invents no second path | DP-13; TSD S3 T-A.1 |
| BR10 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |

### 9. State transitions

None of the case statuses are this contract's, and the claim's states are published by the claim contract. The table fixes the outcomes the contract names so that a consumer cannot invent a fifth.

| Object | State | Meaning in the contract |
|---|---|---|
| Close step | Answered, residual | R-GUA-19 or R-GUA-27 answered; the full balance goes back to the route decision and the element records the basis |
| Close step | Answered, closed | R-GUA-26 answered; the balance after the guarantee is zero and the case closes at `GUARANTEE_CLOSED` |
| Close step | No close | The balance after the guaranteed share is above zero at `SUBROGATION_POSITION`; R-GUA-25 answers and the sibling story takes the residual |
| Close step | Blocked, stale product | A data product is older than today's ACE batch; MSG-P1-001, nothing written |
| Close step | Blocked, missing value | A required value is missing; MSG-GEN-001 with the field, nothing written |
| Close step | Blocked, no answer | A view did not answer; MSG-GEN-006, nothing written |
| Close step | Refused or rolled back | The record was refused with MSG-P7-009 or could not be written with MSG-P7-003; no claim result, no element |
| Element | Recorded or absent | Written against the claim in the same transaction, or not written at all; there is no partial element |
| Contract version | v1 / v2 | v1 is the published version every consumer pins; v2 is raised by a breaking change and v1 stays readable |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-guarantee | Approves a breaking change and freezes a version |
| The owner of P7 rwb-decision | Confirms the GUARANTEE rows, their conditions and their to states at the wave 3 contract freeze (ASM-4539) |
| The owner of P3 rwb-case | Confirms the case statuses the report triggers, the 5 working day task of R-GUA-27 and the case closure (ASM-4538) |
| The owner of the claim contract of this service | Confirms the claim representation and the result operation the element rides (BR9) |
| ACE and its DBA | Confirm the three views, the columns consumed and the SELECT-only grant to this service's login (ASM-4541) |
| The platform data and workflow owners | Confirm the decision-record library, the task queue and the retry policy |
| RW-GUARANT, guarantee officer | Consumes the element through SCR-17 and holds rights C, R and U on the capability area |
| RW-CASEOWN, case owner | Works the returned case and its task; holds rights C, R and U; the step itself runs unattended under the service identity |
| The consumer stories of this service | Consume the element, pin the version and raise a change request rather than a private variant |
| RW-AUDIT, RW-COE | Read the recorded element and the decision records; they do not consume this document directly |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake; where an actor must be named, a role code or a service identity is used.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes field names, the state and event names, the basis codes and the messages; no customer, account or case value appears |
| Element published | The eleven fields of section 12.1, with the required and optional flags and the claim columns they map to |
| Personal data | None. The element carries identifiers, a date, a basis code, a status, amounts of the claim and the balance, and versions; no name, national identifier, account number, payment reference or document content |
| Tables published | None. The consumer writes the claim result and the element against `guarantee_claim` in `rwb_guarantee`; `decision_record` is the platform library object |
| Field identifiers | DF-TRT-015, DF-TRT-016, DF-TRT-021 and DF-TRT-022 for the mapped fields; the element's own identifiers are Not specified in the source documents (GAP-2731; ASM-4537) |
| Retention | The element is kept with the claim row for the life of the case record; the retention period of the element is Not specified in the source documents (GAP-2731; ASM-4537) |

### 12. Contract

#### 12.1 REST operations provided

One mapping of the element onto the claim representation; the contract declares no path of its own beyond the service base `/api/recovery/guarantee/v1` (DP-13).

| Operation | Right | Declared with | This contract |
|---|---|---|---|
| `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}` (API-S3-002) | Treatment and offer U | The claim contract of this service, which owns the claim representation | Fixes the `GuaranteeClose` component the operation carries: its fields, their required flags and the recording rule |
| `POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` (API-S3-001) | Treatment and offer C | The claim contract that opens the claim | Named only: it creates the claim this element is recorded against |

Both are the legacy operations of TSD S3 T-A.1 re-based per DP-13, with the errors 401, 403, 404, 409, 422 and 503 and the idempotency rule TSD S3 T-A.2 gives (Idempotency-Key on the create, not applicable on the result). SCR-17 reaches the element through the gateway-bff composite route (DP-19).

**Element: `GuaranteeClose`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `claimId` | uuid | Yes | DF-TRT-015 `id` | The claim the element is recorded against |
| `caseId` | uuid | Yes | DF-TRT-016 `case_id` | The case the claim belongs to |
| `closedAt` | timestamptz | Yes | No claim column | The business time the guarantee was closed |
| `closeBasis` | string | Yes | No claim column | The to state of the answered row: `RESIDUAL_TO_ROUTE` or `GUARANTEE_CLOSED` |
| `claimStatus` | string | Yes | DF-TRT-022 `status` | A value of LOV-CLAIM-STATUS; the close adds none |
| `claimPaidAmount` | numeric(18,2) | No | DF-TRT-021 `paid_amount` | The amount paid on the claim where the payment is recorded |
| `guaranteedShare` | numeric(18,2) | No | No claim column | The share the answered row names, read with its version (GAP-2731) |
| `balanceAfterShare` | numeric(18,2) | Yes | No claim column | The balance read at the batch date less the guaranteed share; the zero test of R-GUA-26 |
| `balancesAsAt` | date | Yes | No claim column | The ACE batch date the balance and the payments were read at |
| `ruleId` | string | No | No claim column | The row that answered: R-GUA-19, R-GUA-25, R-GUA-26 or R-GUA-27 |
| `ruleVersion` | string | No | The version group of the decision record | The version of the package in force |

The element is recorded against the `guarantee_claim` row and against no other record; it has no collection, no free-text field and no payment detail, because the evidence is a balance, a share and a date, not the payments themselves. The element's own BR Field IDs have no row in the Logical Data Model, so the field names are the working read of ASM-4537 and ASM-4539 (GAP-2731; GAP-2733); the basis codes, the state names and the claim list keep the names the routing logic and TSD S3 T3.2 already use (BR4).

#### 12.2 REST operations consumed

None. The contract declares no REST read: the case status, the claim id and the payment reference arrive on the signal the parent `CaseWorkflow` forwards, the rule rows arrive with the package in force, and the evidence is the SQL read of 12.5. No source publishes an operation for this step, and the contract names the element rather than an invented path (GAP-2734; ASM-4540).

#### 12.3 Events published

None. This contract owns no topic and publishes no event; the service's topic `rwb.guarantee.events.v1` carries no catalogued event, because the ownership rows give S3 none (TSD S3 T5.3; DP-14). The "event" of the step is the stage report to the parent `CaseWorkflow`, a Temporal signal inside the case. A Kafka event for a closed guarantee would need a name, a payload, an outbox row and the event platform of DP-09, which the plan does not give this legacy key; the name and its consumers are the open question recorded in ASM-4538.

#### 12.4 Events consumed

None by this contract. The consumer's rule package arrives on the template's rule loader and the payment that clears the claim arrives on the case signal; the connection matrix of Architecture v5 slide 13 shows S3 listening to P6 and P8 and calling P7 by Temporal activity, and this contract adds no subscription and fixes none. What it does require is that the element and the record name the version that was in force.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue — `GuaranteeClaimWorkflow` on `rwb-guarantee` and its activities are RWB-S3-E4019-APP. What it fixes is the reads the consumer's activity makes, the composition it applies and the report it sends, so that both sides of each read are written down in one place.

| Read element | Value |
|---|---|
| ACE read | SQL, SELECT-only, on `recovery.v_ace_account`, `recovery.v_ace_payment` and `recovery.v_ace_batch_status`, in the ACE database, at the ACE batch date |
| ACE columns | `account_key`, `account_code`, `account_status`, `contract_no`, `product_category_efs`, `total_balance` and the rest of DF-ACE-001 to DF-ACE-042; `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and the rest of DF-ACE-043 to DF-ACE-054; the product date of the batch status |
| ACE rule | No copy is kept; no fourth ACE object is read; no write of any kind; no posting table of rwb-payment is named |
| Balance rule | The balance after the guaranteed share is composed per calculation from the balance read and the share the answered row names, tested against zero |
| Answer rule | R-GUA-19 and R-GUA-27 return the full balance; R-GUA-26 closes the guarantee and the case; R-GUA-25 keeps the residual at the same state |
| Claim rule | The claim status stays inside LOV-CLAIM-STATUS and the paid amount is written where the payment is recorded |
| Report | The outcome, the reason code, the balance tested and the 5 working day owner task of R-GUA-27, to the parent `CaseWorkflow` |
| On a stale product | MSG-P1-001 naming the product and its date; nothing decided |
| On a missing value | MSG-GEN-001 with the field; nothing decided |
| On no answer | MSG-GEN-006; nothing decided |

The column list, the grant path, the composition of the balance and the closed status are the working read of ASM-4537, ASM-4538 and ASM-4541, because no source document states them: the FSD names `v_ace_batch_status` in a validation rule, the legacy data table names the two other views with their field ranges, the routing logic states the conditions in words, and the Work Package records no contract dependency on P1 (GAP-2731, GAP-2732, GAP-2735). The owners confirm all of them at the wave 3 contract freeze.

#### 12.6 Schedules

None. The contract declares no Schedule: the step is entered on the case signal and reports the 5 working day task of R-GUA-27, and neither is a scheduled scan of this service. The ownership rows give S3 no job, and the legacy Quartz scheduler is retired.

#### 12.7 Tables owned

None. The claim result and the element are written by the consumer against `guarantee_claim` in `rwb_guarantee`, a table of this service created on its own Flyway sequence with DF-TRT-015 to DF-TRT-022, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column and adds no foreign key: there is deliberately no share, balance or position column, and `decision_log_entry` is P7's ledger in `rwb_decision`, named only and never written or read here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The `GuaranteeClose` shape | A complete element; one element per missing required field; an element with and without `ruleId`, `ruleVersion`, `guaranteedShare` and `claimPaidAmount` |
| ACE balance and payment fixture | The three views | A cleared balance; a balance above zero after the share; a payment inside the batch; a product dated yesterday; an unreachable view |
| Case-signal fake | The forwarded case signal | `CLAIM_REJECTED` with the deadline passed; `SUBROGATION_POSITION` with a zero balance; `DEADLINE_MISSED` with a recorded loss |
| Output fake | The guard answers | MSG-P1-001 with the product and its date, MSG-GEN-001 with the field, MSG-GEN-006 for no answer, MSG-P4-002 for a role without the right |
| Decision-record fake | The record group of AC3 | An accepted record with the rule and set versions; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Drift fixture | The contract test | One accepted and one refused body per section of the document |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The balance fixture and the case-signal fake are what make Day 1 possible for RWB-S3-E4019-APP and RWB-ITG-W3.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 mapping on `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}` | 0 | The element is a component of the claim representation; no operation is declared by this contract |
| Kafka | 0 | 0 | No topic and no event; the step's event is the stage report |
| Temporal | 0 | 0 | The contract fixes no workflow; it fixes the reads, the composition and the report of the consumer's activity |
| SQL view | 0 | 3 (`recovery.v_ace_account`, `recovery.v_ace_payment`, `recovery.v_ace_batch_status`) | SELECT only, at the batch date, no copy |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-guarantee: the element and the report types in `th.co.scb.ace.workbench.recovery.guarantee.api`, the fakes as a test resource, and the versioning rule in the contract document. The implementation that performs the reads, composes the balance and writes the claim result is RWB-S3-E4019-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2731; ASM-4537).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only views, because the Work Package records no contract dependency on P1 and the grant is the working read of ASM-4541 (GAP-2735). DP-13 fixes the one base the element rides, DP-03 is the record of the close, and DP-19 the path the closed claim is read on.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClose` | Published type | The eleven fields, the required and optional flags and the recording rule (BR1, BR2) |
| `BalanceReadRule` | Document | The three views, the columns, the batch date, the composition of the balance and the no-copy ban (BR3, BR5, AC2) |
| `GuaranteeCloseRules` | Document | The four rows, their conditions, their to states and the claim status rule (BR2, BR4, AC3) |
| `CloseReport` | Published type | The outcome, the reason code, the balance tested, the owner task and the case boundary (BR8, AC4) |
| `ClaimOperationMap` | Document | The two operations, their rights, their errors and the one base (BR9, AC5) |
| `GuardAnswers` | Document | MSG-P1-001, MSG-GEN-001, MSG-GEN-006, MSG-P4-002 and the two record messages (BR6) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (AC6) |
| Fake set and drift fixture | Test asset | The element, view, case-signal, output and record fakes and the drift test (AC6) |

**Database.** No table and no column in this contract. The claim result lands in `guarantee_claim.status` (DF-TRT-022) and `guarantee_claim.paid_amount` (DF-TRT-021), both TSD S3 T3.1 fields; the share, the balance and the position have no column and no field ID, which is why they exist only in the element (GAP-2731; GAP-2733).

**Configuration and reference data.** The share basis, the conditions and the four rule rows are data of rwb-decision with a version and are named here, never fixed. The 2 s budget and the retry policy are the activity's and the workflow kit's. The capability area, the rights C and U and the role set are access data of P4 and are named, not declared by this document.

**Build steps**

1. Write the element with its eleven fields, the required and optional flags and the claim columns (AC1).
2. Write the read rule with the three views, the columns, the batch date, the composition of the balance and the no-copy ban (AC2).
3. Write the four close rows with their from states, events, conditions and to states, the claim status rule and the guard answers with their messages (AC3).
4. Write the stage report and the case boundary, and lint them against rwb-case and the routing logic (AC4).
5. Write the operation map with the two operations, their rights, their errors and the one base, and lint it against DP-13 (AC5).
6. Write the versioning and pinning section with the compatible and breaking examples, generate the fake set and the drift fixture (AC6).
7. Publish v1 and record the pinned versions of RWB-S3-E4019-APP and RWB-ITG-W3.

**Feature flag.** `rwb.guarantee.guarantee-close-contract`.

**Done when.** The document and the schema validate, the read lint, the no-copy check, the base check and the case-boundary check are green, the fakes answer every criterion including the stale product, the missing value and the unreachable view, the drift test fails on an edited field and passes on the published version, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P1-001 | A data product is older than today's ACE batch | {product} is from {date}. Today's ACE batch has not arrived. | The stale-product answer of the read rule; the product named is the one the step read |
| MSG-GEN-001 | A required value is missing, for example the claim deadline | Enter {field}. | The missing-value answer of the rule section |
| MSG-GEN-006 | A view does not answer | {system} is not available. Your request is queued and will be retried. | The no-answer answer of the read rule |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. | The access answer, named from the legacy permission checks |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The library's refusal, named by the record group |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library's failure, named by the record group |

The six texts are copied unchanged from the legacy story, FSD S3 A2.7.3.1 and RWB-PLT-E1027-CON, and this contract adds no message ID. Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. The element and the claim result are shown on SCR-17 Guarantee claim — the guarantee, the claim deadline, the checklist and the claim result — which is reached through the gateway-bff composite route (DP-19) and whose field list belongs to the platform edge story and the screen owner. The contract fixes what that screen may show of the close: the closing basis, the claim status, the balance tested with its batch date and the rule version, and no payment detail beyond the paid amount. The screen's existing states `Not due`, `due`, `submitted`, `paid` and `refused` are unchanged by the element; the case's `GUARANTEE_CLOSED` is the state the report produces on the case, not a new state of the screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S3-E4019-CON-01 | AC1 | Contract | The element schema: the eleven fields, the required and optional flags, the mapping to DF-TRT-015, DF-TRT-016, DF-TRT-021 and DF-TRT-022; one element per missing required field refused |
| TC-S3-E4019-CON-02 | AC2 | Contract | The read rule linted: the three views, the columns, the batch date, the composition of the balance and the no-copy ban; a rule with a fourth ACE object, a copy or a rwb-payment table refused |
| TC-S3-E4019-CON-03 | AC3 | Component | The four rows linted with their conditions and to states, the claim status rule and the guard answers; a fixed share, a renamed state or a new claim status value refused |
| TC-S3-E4019-CON-04 | AC4 | Component | The report and the boundary: the reason, the balance tested, the 5 working day task; a case write, a case task, a case timer or a case closure refused |
| TC-S3-E4019-CON-05 | AC5 | Contract | The operation map: the two operations, right U and right C, the errors, the one base `/api/recovery/guarantee/v1`; a second path or the monolith base refused |
| TC-S3-E4019-CON-06 | AC6 | Component | A compatible and a breaking change on the element and the rows; the fake set and the drift fixture on a consuming story, green on the published version and red on an edited field |

The legacy test set of RWB-E4-019 — TC-E4-019-01 to TC-E4-019-06 — is carried by RWB-S3-E4019-APP and by the wave 3 integration harness, and no legacy id is renumbered here. These six are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the share, the balance and the conditions are named, never fixed as numbers, and the claim result lands on TSD S3 T3.1 fields (BR3, BR4).
- No personal data in the element, a read, an answer, a fake or a log: the element carries identifiers, a date, a basis code, a status, amounts of the claim and the balance, and versions, never a name, an account number or a payment reference.
- No copy of ACE data: no balance, share or position column is declared, and the consumer keeps no copy (BR5).
- One base and one representation: the element rides the claim operation on `/api/recovery/guarantee/v1` and invents no second path (BR9; DP-13).
- No second source for the share and no fourth ACE object: the answered row and three views.
- The outcome of a stale input, a missing value, a dead view or a missing right is a written answer, never an exception a consumer has to guess (BR6).
- A published version is never edited in place: a breaking change raises major version 2 and a consumer pins rather than forks (BR10).
- The case status is never the contract's and never the consumer's: the element is recorded, the report is sent and rwb-case closes the case (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-003 | A guarantee payment that clears the balance closes the case and records the subrogation position | Business Requirements Program; FSD S3 requirements served | FEAT-GUA-07 | 07 Route, settle and claim; 08 Guarantee claim | R-GUA-19; R-GUA-25; R-GUA-26; R-GUA-27 | TC-S3-E4019-CON-01 to TC-S3-E4019-CON-06 |
| Legacy test set RWB-E4-019 | TC-E4-019-01 to TC-E4-019-06 | FSD S3 A2.7 | FEAT-GUA-07 | 08 Guarantee claim | R-GUA-19; R-GUA-26 | Executed by RWB-S3-E4019-APP and the wave 3 integration harness; not owned here |

REQ-S3-003 is the one requirement whose text names this behaviour, so the trace runs on it; TSD S3 T8 maps the same set of IDs to FEAT-GUA-01, which is the module's "written one epic ahead" placeholder, and the feature code is carried alongside until the C1 PRD settles the mapping.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4019-APP | App development | H consumer: implements the branch, the activity, the three reads, the claim result and the report against this contract and its fakes; owner of the four legacy acceptance criteria |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library and its two messages. This contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route that shows the claim result on SCR-17 |
| RWB-S3-E4015-CON, RWB-S3-E4015-APP | Contract, App development | Siblings: the claim representation, the result operation this element rides and the claim states |
| RWB-S3-E4016-CON, RWB-S3-E4016-APP | Contract, App development | Siblings: the subrogation position entered by R-GUA-23 and R-GUA-24 and the residual of R-GUA-25 |
| P3 rwb-case | Service | The case statuses, the closure of the case, the case tasks and the case timers |
| P7 rwb-decision | Service | The GUARANTEE rows, their conditions, their version and the central ledger |
| P8 rwb-payment | Service | The posting and booking of the guarantee payment, whose result this contract never reads from a posting table |
| ACE and its DBA | External capability, existing | The three views, their columns and the SELECT grant (ASM-4541) |
| RWB-ITG-W3 | Integration | I: the cross-service proof of the reads and the report against the live owners, and the owner of the legacy `-ITG` copies |

### 19. Out of scope

- The close branch of `GuaranteeClaimWorkflow`, the close activity, the three reads, the claim result, the report and the tests against this contract: RWB-S3-E4019-APP.
- The four legacy acceptance criteria of RWB-E4-019, AC1 to AC4: carried verbatim by RWB-S3-E4019-APP; none is repeated or renumbered here.
- The claim representation, its create and result operations and its states beyond the component this element occupies: RWB-S3-E4015-CON and RWB-S3-E4015-APP.
- The preparation, the submission and the tracking of the claim: RWB-S3-E4013-CON, RWB-S3-E4014-CON and RWB-S3-E4015-CON.
- The subrogation position entered by R-GUA-23 and R-GUA-24 and the residual of R-GUA-25: RWB-S3-E4016-CON and RWB-S3-E4016-APP.
- The case, its status, its closure, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3); the contract declares no case read and no closure of its own.
- The posting, the booking and the reconciliation of the guarantee payment: P8 rwb-payment and the core bank.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2735).
- The GUARANTEE rows, their authoring, approval, effective date, rollback and the central ledger: P7 rwb-decision; this contract names the version and the conditions only.
- A Kafka event for a closed guarantee, its name, its schema and its consumers: not published by this contract; recorded as ASM-4538.
- SCR-17, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The real cross-service proof of the reads and the report against the live owners: RWB-ITG-W3, which also owns the `-ITG` copies of the legacy cases.
