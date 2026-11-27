# RWB-S3-E4013-APP Prepare a TCG guarantee claim

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-013 split out for rwb-guarantee (S3). The preparation leaves the monolith's method of `GuaranteesAndGuarantorsService` and becomes the prepare branch of `GuaranteeClaimWorkflow` on this service's own task queue; the claim is written on `guarantee_claim` in `rwb_guarantee` with its local decision record in the same transaction (DP-03); the case facts and the case statuses arrive on the case signal the parent `CaseWorkflow` forwards and are never a case write; the officer's two operations sit on base `/api/recovery/guarantee/v1` (DP-13) and are reached through the gateway-bff composite route (DP-19); the four legacy criteria this story owns are copied word for word with their origin tag. No source gives the preparation window a value, the claim deadline a home, the scheme checklist an interface or the "claim preparation agent" a runtime (GAP-2708; ASM-4492 to ASM-4497). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S3-E4013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Size | Not specified in the source documents (DOR-RWB-S3-E4013-APP-16); the squad sizes it at refinement |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S3-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4013-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **guarantee officer (RW-GUARANT)**, I want **the Workbench to assemble the TCG guarantee claim from the case facts and the documents the scheme requires, on the prepare branch of `GuaranteeClaimWorkflow`, with the claim written on `guarantee_claim`, its decision recorded in the same transaction and the deadline timer started when the guarantee is found** — so that **no guarantee claim misses its deadline, which is the failure the module exists to prevent**.

This is the application slice of legacy RWB-E4-013. It owns:

- the four legacy acceptance criteria this story is given (AC1 to AC4), copied verbatim with their origin tag, and the rules, rows, states and messages they carry;
- the prepare branch of `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`: the steps that evaluate the `GUA` rule set (32 rules over 17 states) when the guarantee is found and when preparation falls due, and that record the claim (Temporal and Drools Design slides 5 and 13; TSD S3 T4);
- the three answers of the rule set this story builds: R-GUA-01 (guarantee found on the scheme and a scheme code present: start the claim deadline timer from the date the default conditions are met, to `DEADLINE_TIMER_RUNNING`), R-GUA-04 (days to `claim_deadline` at or inside the preparation window: assemble the claim against the scheme checklist, to `CLAIM_PREPARATION`, 5 working days) and R-GUA-02 (the scheme default conditions are not satisfied: record that no claim arises and hold the guarantee, to `NOT_ELIGIBLE`), with their conditions, owners and service levels carried unchanged (Business Rules and Routing Logic v4; FSD S3 A2.1.3.1);
- the claim row in `rwb_guarantee`: `claim_type`, `claim_deadline`, `claimed_amount` and `status` written from the case facts and the rules, with the local decision record of the step written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON; DF-TRT-017 to DF-TRT-022);
- the scheme checklist assembled from the case facts and the document references the scheme requires, resolved through the platform document client library that rwb-document publishes, with no document row and no blob reference owned here (ASM-4494);
- the stage report to the parent `CaseWorkflow` carrying `DEADLINE_TIMER_RUNNING`, `CLAIM_PREPARATION`, `CLAIM_APPROVAL` or `NOT_ELIGIBLE` with the rule version, because the case status, the case task and the case timer are rwb-case's (DP-12);
- the officer's two operations of RWB-S3-E4013-CON implemented behind the published shape, and the `Not due` and `due` states of SCR-17 reached through the gateway-bff composite route (DP-13; DP-19);
- the refusal and failure paths: no record, nothing changes and MSG-P7-003; a role without the right is refused with MSG-P4-002; a missing value is named with MSG-GEN-001.

It does not own: the published resource shape, the DDL template, the error set, the versioning rule and the fakes, which are RWB-S3-E4013-CON; the approval of the assembled claim and its submission on the TCG claim channel, which are RWB-S3-E4014-APP; the tracking of the claim to payment, the lost claim and the service level breach, which are RWB-S3-E4015-APP; the subrogation position, which is RWB-S3-E4016-APP; the guarantor notices, which are RWB-S3-E4017-APP; the case, its status, its tasks and its timers, which are rwb-case's; the rule package, its approval and the central ledger, which are P7 rwb-decision's; the guarantee documents themselves, which are rwb-document's; the TCG portal, which is INT-29 and outside the cluster.

### 2. Business rationale

In the monolith the preparation was a method of `GuaranteesAndGuarantorsService` behind `GuaranteesAndGuarantorsController`: it read the case from the one `recovery` schema, assembled the claim, wrote `recovery.guarantee_claim` and `recovery.decision_log_entry` beside it and moved the case status in the same transaction, all in one process and one schema (TSD S3 T2). The consequence was the one the module exists to prevent — the claim deadline and the assembly lived in the same code as the case, so a preparation that stopped left no trace of why, and the module's own note that "guarantee and TCG claims are late because deadlines are not tracked" was a statement about the code, not about the officers (FSD S3 A1.3).

D-RCV-60 changes the source of each input and the owner of each fact, and nothing about the officer's work. The claim becomes a row of `rwb_guarantee` with its own login and no cross-schema key (DP-01, DP-02). The decision is recorded locally in the same transaction as the preparation, so a preparation that cannot be recorded does not happen (DP-03; ADR-022). The case moves because the stage reports and the parent applies the rule, never because this service writes a case row (DP-01, DP-12). The preparation is a branch of the stage workflow the service owns: one child per case on the owner's queue `rwb-guarantee`, event in, rule decides, person signs, timer waits (Temporal and Drools Design slides 5 and 13).

Four facts of the target are recorded rather than designed away. The preparation window of R-GUA-04 is a value in force with no number in any source, so it is exported as a rule-row parameter and the only figure carried is the 5 working day service level of the rule (ASM-4493). The claim deadline is a date of the claim row while the timer is the platform's, so the date is written here and the durable timer runs in the workflow (ASM-4492). The scheme checklist names the Document Hub as its system, and no operation and no contract dependency exist for it, so the references are resolved through the platform document client library and the interface stays open (ASM-4494). The "claim preparation agent" of AC2 is bound to no runtime by any source, so it is the unattended preparation step of this service and no rwb-agent call is made (ASM-4495).

Delivery is EP04 in wave 3 on release 28 February 2027 (tentative). REQ-S3-001 of FSD S3 — "a guarantee claim is prepared from case data and submitted inside the guarantor's deadline" — is the requirement this story traces to, and REQ-S3-007 carries the eligibility filter of R-GUA-02 (Section 18).

### 3. Preconditions

- RWB-S3-E4013-CON is published: the base `/api/recovery/guarantee/v1`, `GuaranteeClaimRequest` and `GuaranteeClaim` over the eight DF-TRT fields, the `guarantee_claim` DDL template, the error set, the `Idempotency-Key` rule and the fakes. The build starts against the Draft baseline, because every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` propagation, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-17 from the case read and this service's claim answer (DP-19).
- The `rwb_guarantee` schema and its login exist from the platform database story, and `guarantee_claim` is on the per-service Flyway sequence with DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1 and the seven standard columns of T3.0; `decision_record` is created as the platform library object in the same schema (DP-01; DP-15).
- The case is signalled by the parent `CaseWorkflow` in `GUARANTEE_DETECTED` with the guarantee type, the scheme code and the date the default conditions are met, or in `DEADLINE_TIMER_RUNNING` with the claim row and its deadline (ASM-4497).
- The `GUA` package and route set are in this service's rule cache at the version the answer names; the rule identifiers, the conditions, the preparation window and the 5 working day service level are rule rows, not code (EV-30; BR-S3-001).
- The document references the scheme checklist requires are resolvable through the platform document client library; no document row and no blob is read directly (ASM-4494).
- No approval stop: FSD S3 v3 and TSD S3 v2 carry status "In review", and nothing in this story needs a human sign-off to start on Day 1 (ASM-4498).

### 4. Flow

1. rwb-case: the parent `CaseWorkflow` starts the `GuaranteeClaimWorkflow` child of the case and forwards the case signal when the valuation decides the guarantee route at D6.5 and D6.6, carrying the case ID, the case status `GUARANTEE_DETECTED`, the guarantee type, the scheme code and the date the default conditions are met (Architecture v5 slide 13; TSD S3 T4).
2. `GuaranteeClaimWorkflow`: the prepare branch opens the step, calls `EvaluateRules` and the `GUA` set in force answers R-GUA-01 when `guarantee_type` is the TCG scheme and a `scheme_code` is present, or R-GUA-02 when the scheme default conditions are not satisfied (R-GUA-01; R-GUA-02).
3. On R-GUA-01 the step computes the claim deadline from the date the default conditions are met and the rule's own period, and `RecordAndApply` writes the claim row and the decision record in one transaction (R-GUA-01; DF-TRT-018; DP-03).
4. The stage reports `DEADLINE_TIMER_RUNNING` with the rule version and the deadline; the parent applies the status and raises the case timer, and the workflow waits on a durable timer to the deadline (ASM-4492).
5. On R-GUA-02 the stage records that no claim arises and holds the guarantee: the claim row takes the hold with its reason code, the decision record is written, and the stage reports `NOT_ELIGIBLE` (R-GUA-02).
6. At the preparation window the timer fires and `EvaluateRules` answers R-GUA-04: `assembleChecklist` collects the scheme checklist from the case facts and the document references the scheme requires, resolved through the platform document client library, and names every missing item (R-GUA-04; ASM-4494).
7. `recordPreparation` builds the claim from the case facts — `claim_type` of LOV-CLAIM-TYPE, `claim_deadline`, `claimed_amount` — and, when the checklist is complete, presents it for approval; when it is not, the answer is the checklist-incomplete one (R-GUA-04; DF-TRT-017 to DF-TRT-019).
8. `RecordAndApply`, one transaction: the claim row takes `status = PREPARING` of LOV-CLAIM-STATUS and its standard columns, the decision record is written with the rule ID, the rule version and the checklist outcome, and the stage report is emitted (DP-03; TSD S3 T3.2).
9. The stage reports `CLAIM_PREPARATION`, and on a complete checklist `CLAIM_APPROVAL` with the rule version and the 5 working day service level; the parent applies the status and raises the case task for the officer (R-GUA-04; R-GUA-07 read from TSD S3 T4).
10. The officer sees the `due` state, the claim deadline and the checklist on SCR-17 through the gateway-bff composite route, which composes the case read and this service's claim answer in one hop each (DP-19).

The approval and the submission that follow are RWB-S3-E4014-APP's and start where step 9 leaves the claim.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | The transaction rolls back: no claim row, no status, no stage report; the officer sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC4 |
| X2 | A required claim value is missing — the guarantee type, the scheme code or the claim amount | The step names the field, writes nothing and raises a guarantee officer task | MSG-GEN-001 | AC5; Section 12.8 |
| X3 | The scheme default conditions are not satisfied | No claim arises; the guarantee is held with its reason code and the stage reports `NOT_ELIGIBLE` | None | AC6; R-GUA-02 |
| X4 | The scheme checklist is incomplete at the preparation window | The claim stays in `PREPARING`, the missing items are named on the task and the defect hold answer is reported; nothing is filed | None | AC7; R-GUA-08 read; GAP-2708 |
| X5 | A role without the right in the capability area tries the action | 403 from the access guard on the operation, and nothing changes | MSG-P4-002 | AC8; Section 10 |
| X6 | The document references cannot be resolved inside the retry budget | The activity is retried by the workflow's policy; when the attempts are exhausted the step stays where it was, the officer task names the missing items and no business message is fixed | Not specified in the source documents (GAP-2708; ASM-4494) | AC9; Section 12.8 |
| X7 | A second case signal arrives while the branch is running | The inbox dedupes by the cloud event id and the branch is idempotent on the case, the rule version and the claim status, so no second claim row is written | None | AC10; Section 12.5 |
| X8 | The date the default conditions are met is absent from the signal | The step cannot compute the deadline, names the fact and reports nothing; the case stays in `GUARANTEE_DETECTED` | Not specified in the source documents (GAP-2708; ASM-4497) | AC11; Section 9 |

X1 to X5 are the legacy paths of RWB-E4-013 carried onto the split; X6 to X8 are the boundaries the missing interface, the missing value and the missing fact record.

The wording of MSG-P4-002, MSG-P7-003 and MSG-GEN-001 has no named owner in the shared message catalogue: Not specified in the source documents (GAP-1731). Thai and English approval of the shown versions: Not specified in the source documents (GAP-1731).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S3-E4013-CON, its fakes and the gateway route; the case arrives on a signal fixture, the documents on a client fake and the rule package on a fake, so no deployment of P3, P5, P7 or rwb-document is needed |
| Negotiable | The activity names, the shape of the stage report, the retry numbers and the checklist representation are this story's choice; the rules, the condition terms, the states and the messages are fixed |
| Valuable | A guarantee that is found becomes a claim with a deadline, a checklist and a date, in one unattended step, and the case moves without a hand-written status |
| Estimable | One workflow branch, three activities, one checklist assembly, one claim write, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case, a document-reference fixture and a rule-package fake, plus component tests of the not-eligible, incomplete-checklist and refusal paths |

### 7. Acceptance criteria

```gherkin
Feature: Prepare a TCG guarantee claim

  Background:
    Given case "RW-2026-000913" carries a TCG guarantee with a scheme code
    Given the rule package in force is version "GUA-2026.11"

  Scenario: AC1 Prepare a TCG guarantee claim (legacy RWB-E4-013 AC1)
    Given the rwb-case contract mock returns the case in state DEADLINE_TIMER_RUNNING
    Given the decision-record library mock returns an accepted record
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then assembles the claim from the case facts and the documents the scheme requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-04 (legacy RWB-E4-013 AC2)
    Given the rwb-case contract mock returns the case in state DEADLINE_TIMER_RUNNING
    Given a case in state DEADLINE_TIMER_RUNNING
    When preparation due
    Then the claim preparation agent assembles the claim against the scheme checklist
    Then the case moves to CLAIM_PREPARATION

  Scenario: AC3 Rule R-GUA-01 (legacy RWB-E4-013 AC3)
    Given the rwb-case contract mock returns the case in state GUARANTEE_DETECTED
    Given a case in state GUARANTEE_DETECTED
    When guarantee found
    Then start the claim deadline timer from the date the default conditions are met
    Then the case moves to DEADLINE_TIMER_RUNNING

  Scenario: AC4 Not recorded (legacy RWB-E4-013 AC4)
    Given the decision-record library mock returns the failure MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Required claim value missing (exception X2 of section 5) (new, D-RCV-60)
    Given the case carries a TCG guarantee without a required claim value
    When the prepare branch assembles the claim
    Then the step names the missing field, writes nothing and raises a guarantee officer task with MSG-GEN-001

  Scenario: AC6 Scheme default conditions not satisfied (exception X3 of section 5) (new, D-RCV-60)
    Given the scheme default conditions are not satisfied
    When the rule is evaluated
    Then no claim arises, the guarantee is held with its reason code and the stage reports NOT_ELIGIBLE

  Scenario: AC7 Scheme checklist incomplete (exception X4 of section 5) (new, D-RCV-60)
    Given the scheme checklist is incomplete at the preparation window
    When the claim is prepared
    Then the claim stays in PREPARING, the missing items are named on the task, the defect hold answer is reported and nothing is filed

  Scenario: AC8 Role without the right (exception X5 of section 5) (new, D-RCV-60)
    Given a role without the right in the capability area
    When it tries the action
    Then the access guard returns 403 on the operation, nothing changes and the user sees MSG-P4-002

  Scenario: AC9 Document references unresolved (exception X6 of section 5) (new, D-RCV-60)
    Given the document references cannot be resolved inside the retry budget
    When the retry attempts are exhausted
    Then the step stays where it was, the officer task names the missing items and no business message is fixed

  Scenario: AC10 Second case signal (exception X7 of section 5) (new, D-RCV-60)
    Given a second case signal arrives while the branch is running
    When the inbox receives it
    Then the inbox dedupes by the cloud event id and no second claim row is written

  Scenario: AC11 Deadline date absent (exception X8 of section 5) (new, D-RCV-60)
    Given the date the default conditions are met is absent from the signal
    When the step computes the claim deadline
    Then the step cannot compute the deadline, names the fact, reports nothing and the case stays in GUARANTEE_DETECTED

  Scenario: AC12 Business rules BR1 to BR10 (section 8) (new, D-RCV-60)
    Given the case carries a TCG guarantee with a scheme code
    When the prepare branch runs
    Then no business value is held in code, the claim row holds only the BR5 fields, the claim write and its decision record commit in one transaction, no case status, case task or case timer is written, no document row is read directly, the preparation runs under the service identity and the capability area of BR10 is checked on the operations

  Scenario: AC13 Error answers of the provided operations (new, D-RCV-60)
    Given a provided operation of the claim contract
    When a request arrives without a valid identity, from a role without the right, or for a claim the service does not hold
    Then the answer is 401, 403 or 404 respectively and nothing changes

  Scenario: AC14 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given a write of the branch has been accepted with an idempotency key
    When the same write is replayed with the same idempotency key
    Then no second claim row is written

  Scenario: AC15 Activity retry and timeout (new, D-RCV-60)
    Given an activity of the prepare branch fails or does not answer
    When the activity is retried or the agent does not answer inside 60 seconds
    Then the activity is retried by the workflow's policy and the checklist result is taken

  Scenario: AC16 Disallowed status change refused (new, D-RCV-60)
    Given a case status change the model does not allow
    When the branch attempts the change
    Then the change is refused and nothing changes

  Scenario: AC17 Business rule BR1 (section 8) (new, D-RCV-60)
    Given the prepare branch runs
    When it reads a rule, the preparation window, the service level, a list or a message text
    Then each is read from a rule row or a governed row with a version and no such value is held in code

  Scenario: AC18 Business rule BR2 (section 8) (new, D-RCV-60)
    Given a guarantee found on the TCG scheme with a scheme code
    When the default conditions are met
    Then the claim deadline timer starts from that date and the claim moves to DEADLINE_TIMER_RUNNING

  Scenario: AC19 Business rule BR3 (section 8) (new, D-RCV-60)
    Given the scheme default conditions are not satisfied
    When the branch evaluates the guarantee
    Then no claim arises, the guarantee is held and the claim moves to NOT_ELIGIBLE

  Scenario: AC20 Business rule BR4 (section 8) (new, D-RCV-60)
    Given days to claim_deadline are at or inside the preparation window
    When the branch prepares the claim
    Then the claim is assembled against the scheme checklist and moves to CLAIM_PREPARATION inside the 5 working day service level

  Scenario: AC21 Business rule BR5 (section 8) (new, D-RCV-60)
    Given the claim is prepared
    When the claim row is written
    Then it is one write on guarantee_claim with claim_type, claim_deadline, claimed_amount and status PREPARING, filed_at and paid_amount are null, and the claim status is derived from the workflow state through versioned reference data

  Scenario: AC22 Business rule BR6 (section 8) (new, D-RCV-60)
    Given the claim write and its decision record
    When the decision record cannot be written
    Then nothing changes and MSG-P7-003 is shown

  Scenario: AC23 Business rule BR7 (section 8) (new, D-RCV-60)
    Given the prepare branch runs
    When the outcome is reported to the parent
    Then no case status, case task or case timer is written here, and the stage reports the outcome, rule version and service level

  Scenario: AC24 Business rule BR8 (section 8) (new, D-RCV-60)
    Given the scheme checklist is assembled
    When it resolves documents
    Then it uses case facts and the document references the scheme requires, and no document row, blob reference or document content is owned or read directly

  Scenario: AC25 Business rule BR9 (section 8) (new, D-RCV-60)
    Given the preparation runs
    When a value is missing or the checklist is incomplete
    Then the preparation runs unattended under the service identity and rwb-case raises the officer task

  Scenario: AC26 Business rule BR10 (section 8) (new, D-RCV-60)
    Given an operation of the contract
    When a caller invokes it
    Then the capability area "Treatment and offer" is checked, with right C on create and right U on update
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, which service holds each fact and how it is reached. "Assembles the claim from the case facts and the documents the scheme requires" is no longer a method of `GuaranteesAndGuarantorsService` writing `recovery.guarantee_claim`: it is the prepare branch of `GuaranteeClaimWorkflow` on queue `rwb-guarantee`, and the claim row is `rwb_guarantee.guarantee_claim`. The case facts arrive on the case signal the parent forwards; no case table and no case column is read, and no case status is written here (DP-01, DP-12).

"Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction as the claim write, with MSG-P7-003 on failure (DP-03; RWB-PLT-E1027-CON); `decision_log_entry` stays P7's and is never written here. "The claim preparation agent assembles the claim against the scheme checklist" is the `assembleChecklist` activity of this service, which calls the agent through the rwb-agent contract as a Temporal activity, takes the checklist result when the agent does not answer inside 60 seconds or fails the schema check (NFR-024; NFR-055), and records which of the two assembled the claim; the checklist's documents are resolved through the document client library of rwb-document (ASM-4494). "Start the claim deadline timer from the date the default conditions are met" writes `guarantee_claim.claim_deadline` and arms the durable workflow timer to it, while the case timer row stays rwb-case's and is raised from the stage report (ASM-4492). "The case moves to DEADLINE_TIMER_RUNNING" and "the case moves to CLAIM_PREPARATION" are the stage report and the rule the parent applies (ASM-4496). "Its trigger arrives" is the case signal the parent forwards, because the FSD names "a completed ACE batch, an event or a timer" and no source names which one.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value a business person may change is written in code: the rule IDs, the conditions, the preparation window, the 5 working day service level, the list members and the message texts are rule rows or governed rows with a version | BR-S3-001 of FSD S3 A2.1.3.1 |
| BR2 | A guarantee found on the TCG scheme with a scheme code starts the claim deadline timer from the date the default conditions are met, and the claim moves to `DEADLINE_TIMER_RUNNING` | R-GUA-01 |
| BR3 | Where the scheme default conditions are not satisfied, no claim arises, the guarantee is held and the claim moves to `NOT_ELIGIBLE` | R-GUA-02; FSD S3 A2.1.3.1 |
| BR4 | When days to `claim_deadline` are at or inside the preparation window, the claim is assembled against the scheme checklist and moves to `CLAIM_PREPARATION`, inside the 5 working day service level of the rule | R-GUA-04 |
| BR5 | The claim row is one write on `guarantee_claim`: `claim_type` from LOV-CLAIM-TYPE, `claim_deadline`, `claimed_amount` and `status = PREPARING` of LOV-CLAIM-STATUS, with `filed_at` and `paid_amount` left null until the filing; the workflow state is the state of record and the claim status is derived from it at each transition through a mapping held as versioned reference data | TSD S3 T3.1, T3.2; GAP-1720 |
| BR6 | The claim write and its decision record are written in one transaction; if the record cannot be written nothing changes and MSG-P7-003 is shown | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR7 | The case status, the case task and the case timer are never this service's: the stage reports the outcome, the rule version and the service level, and the parent applies the rule | DP-01; DP-12; ASM-4496 |
| BR8 | The scheme checklist is assembled from the case facts and the document references the scheme requires; no document row, blob reference or document content is owned or read directly here | ASM-4494; FSD S3 A2.1.3.1 |
| BR9 | The preparation is unattended under the service identity; the officer task is raised by rwb-case when a value is missing or the checklist is incomplete | FSD S3 A2.1.3.3; TSD S3 T6.2 |
| BR10 | The capability area is "Treatment and offer" with right C on the create and right U on the update; the right is declared per operation and checked by the platform guard | TSD S3 T6.1 |

**Where each rule lives in the target.** BR1 is why the rules, the window and the service level are inputs of the step; the parameters and reference data they read are held by rwb-case (DP-06, DP-07); BR2 and BR3 are the two answers at the finding of the guarantee; BR4 is the preparation-window evaluation and the checklist activity; BR5 is the single claim write; BR6 is the `MANDATORY` propagation of the library write; BR7 is the boundary to rwb-case; BR8 is the checklist assembly and the reason no document is owned; BR9 is the service identity and the officer task; BR10 is the `security` section of the two operations the contract publishes.

### 9. State transitions

None of the case statuses below is this service's; the table shows what the stage reports and does not write, so a reader can see the boundary of this story.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-GUA-01 | `GUARANTEE_DETECTED` | `GUARANTEE_FOUND` | `guarantee_type` = TCG scheme and `scheme_code` present | Writes the claim row with its deadline, records the decision, arms the workflow timer and reports `DEADLINE_TIMER_RUNNING` | `DEADLINE_TIMER_RUNNING` |
| R-GUA-02 | `GUARANTEE_DETECTED` | `CONDITIONS_NOT_MET` | the scheme default conditions are not satisfied | Records that no claim arises, holds the guarantee with its reason code and reports `NOT_ELIGIBLE` | `NOT_ELIGIBLE` |
| R-GUA-03 (read only) | `NOT_ELIGIBLE` | `CONDITIONS_LATER_MET` | the default conditions are met later | Re-enters at R-GUA-01 on the next signal; the row is in force and this story writes nothing for it beyond the new deadline | `DEADLINE_TIMER_RUNNING` |
| R-GUA-04 | `DEADLINE_TIMER_RUNNING` | `PREPARATION_DUE` | days to `claim_deadline` at or inside the preparation window | Assembles the checklist and the claim, records the decision and reports `CLAIM_PREPARATION` with the 5 working day service level | `CLAIM_PREPARATION` |
| R-GUA-07 (reported, not owned) | `CLAIM_PREPARATION` | `CHECKLIST_COMPLETE` | every scheme item is present | Reports `CLAIM_APPROVAL` so the officer can verify the claim; the approval and the submission are RWB-S3-E4014-APP's | `CLAIM_APPROVAL` |
| R-GUA-08 (reported, not owned) | `CLAIM_PREPARATION` | `CHECKLIST_INCOMPLETE` | a scheme item is missing | Leaves the claim in `PREPARING`, names the missing items on the task and reports the defect hold | `CLAIM_DEFECT_HOLD` |

The states of this story's own row are the claim's, from LOV-CLAIM-STATUS: a row is written in `PREPARING` and takes no other member here. The seventeen rule states of TSD S3 T4 and this five-member list are two vocabularies and no source maps them, so only the one member this story needs is fixed (GAP-2708; ASM-4496). The `GuaranteeClaimWorkflow` execution has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the checklist assembly and the write are activities and not workflow-local computation. The claim deadline is the workflow's durable timer once armed, and a Continue-As-New at the stage end keeps the run inside the platform limit (Temporal and Drools Design slide 13).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the checklist activity, the claim write and the tests |
| RW-GUARANT, guarantee officer | Sees the claim and its checklist, verifies the assembled claim at D6.5 and completes a missing value; holds rights C, R and U on Treatment and offer |
| RW-CASEOWN, case owner | Owns the case the claim is prepared on; holds rights C, R and U |
| RW-RESTRUCT, restructuring officer (FCR) | Holds rights C, R, U and A; sees the preparation |
| RW-SPECIAL, hardship and vulnerability specialist | Holds rights C, R and U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S3 T6.1 | Right R only: they read the claim and its checklist and cannot prepare or change it |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity and reports to the parent |
| rwb-case (P3) | Owns the case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Owns the `GUA` package, the 32 rows, their approval, their effective date and the central ledger |
| rwb-document (P5) | Owns the guarantee documents, their metadata and their blob references |
| ACE and its DBA | Own the ACE database, its batch and the `recovery.v_ace_*` views this story does not read |
| The platform workflow and data owners | Own the task queue, the namespace, the ACE PostgreSQL grants and the decision-record library |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right C or U on each entry point, and no check is written in code. Each entry point calls the rwb-access authorise check of DP-08 through that library. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the claim ID, dates, amounts and versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Write (the new row) |
| DF-TRT-016 | guarantee_claim | case_id | Write (from the case signal) |
| DF-TRT-017 | guarantee_claim | claim_type | Write (LOV-CLAIM-TYPE, from the guarantee type) |
| DF-TRT-018 | guarantee_claim | claim_deadline | Write (from the date the default conditions are met) |
| DF-TRT-019 | guarantee_claim | claimed_amount | Write (from the case facts) |
| DF-TRT-020 | guarantee_claim | filed_at | Not written here; the filing is RWB-S3-E4014-APP's |
| DF-TRT-021 | guarantee_claim | paid_amount | Not written here; the payment is the tracking story's |
| DF-TRT-022 | guarantee_claim | status | Write (`PREPARING` of LOV-CLAIM-STATUS) |
| TSD S3 T3.0, no field identifier | guarantee_claim | the seven standard columns is_active, state, version, created_at, created_by, updated_at, updated_by | Write (`created_at`, `created_by`, `version`) |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, product_group, status, stage_code, the guarantee type and the scheme code | Read on the case signal only |
| DF-WRK-027 to DF-WRK-036 | timer | the case timer to the claim deadline | Not this service's; rwb-case writes it (ASM-4492) |
| DF-DOC-001 to DF-DOC-011 | document | document_type, source and storage_ref of the scheme documents | Read as references through the document client library; no row owned here |
| DF-DEC-001 to DF-DEC-018 | decision_record | the field groups of the record | Write |
| DF-REF-001 to DF-REF-015 | rule_row | the `GUA` rows in force, their conditions, the preparation window and the 5 working day service level | Read |

`guarantee_claim` and `decision_record` are this service's own objects in `rwb_guarantee`, written through its own repository and login (DP-01). The case fields arrive on the case signal and are never read from a table. The document rows are rwb-document's and only their references are used, so no document column, blob reference or content is stored in `rwb_guarantee` (ASM-4494). The rule rows are read through the rule loader and are never joined to this service's tables. The ACE database is not read by this story: the preparation needs no account fact, because the claimed amount comes from the case facts and the rule. Any account or freshness read is made through the rwb-source-data contract; this service reads no ACE view or table (GAP-1717). The date the default conditions are met has no column of `guarantee_claim` and no field identifier anywhere, so it is carried on the signal (GAP-2708; ASM-4497).

### 12. Contract

#### 12.1 REST operations provided

This story implements the two operations that RWB-S3-E4013-CON publishes on base `/api/recovery/guarantee/v1` (DP-13), and adds no path of its own.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest`; `caseId` from the path | 201 with `GuaranteeClaim` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` | 200 with `GuaranteeClaim` | Treatment and offer U, scope applied | Not applicable | 401, 403, 404, 409, 422, 503 |

The two operations, their entities, their rights, their idempotency and their error statuses are TSD S3 T-A.1 and T-A.2 for API-S3-001 and API-S3-002 with the base renamed by DP-13; the shape, the DDL template, the message identifiers and the fakes are RWB-S3-E4013-CON's and are not restated here. The create is the officer's route to a claim opened by hand; the workflow opens the row by the same server-side service method the create uses, so one validation path serves both.

#### 12.2 REST operations consumed

None. The case facts and the case status arrive on the case signal the parent `CaseWorkflow` forwards, and Architecture v5 slide 13 shows the P3 to S3 edge as a Temporal child started on this service's queue, with no REST line in either direction. The document references are resolved through the platform document client library that rwb-document publishes, which is a library binding and not an operation of this service (ASM-4494); the rule rows arrive on the package event of 12.4 and the screen is composed by the gateway route of 12.8 (DP-19). No source publishes an operation for this step and none is invented.

#### 12.3 Events published

None. The service's topic is `rwb.guarantee.events.v1` with names `rwb.guarantee.<Event>.v1` (DP-14), and the ownership rows give S3 no event type; the connection matrix has rwb-reporting listening to S3, which no catalogued event satisfies, so the preparation raises no Kafka event and its signal is the stage report to the parent `CaseWorkflow` (GAP-2708; ASM-4499). The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this service (DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the `GUA` package and route set in force, verifies the checksum, swaps them atomically and keeps the last good set on failure; EV-30 |

The service also listens to P8 payment events on the connection matrix, and the event that opens R-GUA-20 sits with the tracking story RWB-S3-E4015-APP; no event name is published for it in the sources read here, so none is named. Both subscriptions are the service template's inbox and rule loader; this story adds no subscription of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` (the prepare branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case ID, the case status on the signal, the guarantee type, the scheme code, the date the default conditions are met, the rule version and the case facts. Output: the stage report with the claim ID, the deadline, the checklist outcome, the rule version and the service level |
| `EvaluateRules` | Activity of the template | `rwb-guarantee` | The package and route set in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `assembleChecklist` | Activity | `rwb-guarantee` | The case facts and the document references in; the checklist with each item present or missing out; a missing reference is non-retryable |
| `recordPreparation` | Activity | `rwb-guarantee` | The rule answer and the checklist in; the `GuaranteeClaimRequest` of RWB-S3-E4013-CON out, with `status = PREPARING` |
| `RecordAndApply` | Activity of the template | `rwb-guarantee` | The request and the decision record in one transaction, then the stage report |

The workflow name is fixed by Temporal and Drools Design slide 13; the three activity names are this story's choice. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; a missing reference and `NoPackageInForce` non-retryable). A replay never re-resolves a document: the answer is recorded by the activity and read from history, and the branch is idempotent on the case, the rule version and the claim status, so a repeated signal writes no second claim. The claim deadline is a durable timer of this workflow, so a restart after Continue-As-New still fires at the same instant.

#### 12.6 Schedules

None. The step is signal-driven and timer-driven inside the workflow and owns no Temporal Schedule and no legacy Quartz job; the ownership rows give S3 no job. The preparation window of R-GUA-04 and the claim deadline of R-GUA-01 are workflow timers driven by the platform, and the case timer row they raise is rwb-case's (ASM-4492).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 rwb-guarantee | Created by the per-service Flyway sequence and written here for the claim fields, `status` and the standard columns; DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1 |
| `decision_record` | `rwb_guarantee` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). The case table, the timer table and the task rows of rwb-case, the document tables of rwb-document, the rule tables of rwb-decision and the ledger of P7 are never named in SQL, and no `recovery.v_ace_*` view is read by this story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S3-E4013-CON claim fake | The two operations of 12.1 | A 201 create with a `GuaranteeClaim` in `PREPARING`; a 200 update; a 409 for a claim already open; a 422 and a 403 refusal; a 404 and a 503 |
| Case-signal fake | The signal the parent forwards | `GUARANTEE_DETECTED` with a TCG scheme and a scheme code; the same with no scheme code; `DEADLINE_TIMER_RUNNING` at the preparation window; `DEADLINE_TIMER_RUNNING` with no default-conditions date |
| Document client fake | The scheme checklist references | Every item present; one item missing; an unresolvable reference |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The `GUA` package and rows in force | Version `GUA-2026.11` with R-GUA-01, R-GUA-02 and R-GUA-04; a set with no matching row; a checksum mismatch |
| Gateway route fake (RWB-PLT-N001-CON) | The SCR-17 composite route | The case read and the claim answer composed in one response |

The case-signal fake and the document client fake are the Day-1 unblockers: the build and every test run against them, and no test reads a production view, needs a live case or reaches rwb-document.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations implemented on `/api/recovery/guarantee/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches them through gateway-bff (DP-19) |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic named, no event type declared; inbox dedupe by cloud event id |
| Temporal | `GuaranteeClaimWorkflow` and 4 activities on `rwb-guarantee` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; a durable claim-deadline timer; no Schedule |
| Library | 0 | 1 (the document client of rwb-document) | A client binding, not an operation; no document row or blob read directly (ASM-4494) |
| SQL view | 0 | 0 | This story reads no `recovery.v_ace_*` view |
| File | 0 | 0 | No file is read or written; the scheme checklist carries references only |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, modules `claimprepare` and `workflow`, with the published types in `...guarantee.api`. Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record of the preparation, DP-13 the base the two operations sit on, and DP-19 the path SCR-17 is read on. The outbox and inbox library, the workflow kit, the access guard, the embedded Drools runtime and the document client are the service template's wave-0 capabilities and add no build dependency of their own; the embedded Drools kit carries DP-04, which the Work Package does not record for this key and which adds no story-level dependency because the `GUA` rows arrive on the package event of 12.4.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ClaimPrepareBranch` | Workflow | The branch of `GuaranteeClaimWorkflow` that opens the step, arms the deadline timer, reports the outcome and waits |
| `EvaluateRules` | Activity | Runs the `GUA` package and route set in force and returns the rule ID, the action and the next event |
| `ChecklistAssembler` | Activity | Builds the scheme checklist from the case facts and the document references, and names each missing item |
| `ClaimPreparation` | Service | Builds the claim from the case facts, computes the deadline and decides between preparation and the not-eligible answer |
| `ClaimPrepareRepository` | Repository | Writes the claim fields and the standard columns on `guarantee_claim` |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report with the claim ID, the deadline, the checklist outcome, the rule version and the service level |

**Database.** No new table and no new column beyond the contract's template: this story writes DF-TRT-015 to DF-TRT-019 and DF-TRT-022 with the standard columns in `rwb_guarantee`, and `decision_record` is the library object of DP-03. The date the default conditions are met is not given a column because no field identifier exists for it; if it must be persisted it becomes a field of the Logical Data Model first (GAP-2708; ASM-4497). The claim deadline, the TCG quota, the preparation window and the warning window are not restated in this document: they are read at run time from versioned reference data per scheme (GAP-1728; GAP-1476). The filing stays with RWB-S3-E4014-APP, and the guarantee officer files the claim by hand until INT-29 is available.

**Configuration and reference data.** The rule IDs, the conditions, the preparation window and the 5 working day service level are data of rwb-decision and the reference lists, read with their version and never configured here (BR-S3-001). The retry numbers, the activity names and the 2 s budget are configuration of the activity. The capability area "Treatment and offer" and the rights are access data of P4 read through the guard library.

**Build steps**

1. The prepare branch of `GuaranteeClaimWorkflow` on `rwb-guarantee`, its input record and the stage report.
2. `EvaluateRules` against the package fake, with R-GUA-01, R-GUA-02 and R-GUA-04 as rule rows and the `NoPackageInForce` answer (AC2, AC3).
3. `ClaimPreparation` with the deadline computation from the date the default conditions are met, and the not-eligible answer (AC3, X3, X8).
4. `ChecklistAssembler` against the document client fake, with the complete, incomplete and unresolvable paths (AC2, X4, X6).
5. The claim write and the `GuaranteeClaimRequest` against the claim fake, with the 409 of a claim already open (AC1).
6. `RecordAndApply` with the record in the same transaction and the rollback path of MSG-P7-003 (AC4).
7. The stage report with the rule version, the service level and the claim ID, and the parent's `CLAIM_APPROVAL` report on a complete checklist (AC2).
8. Tests for AC1 to AC4 against the fakes, the component tests of X2, X3, X4, X6 and X8, and the replay test of X7.

**Feature flag.** `rwb.guarantee.claim-preparation`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the document client, the package and the parent faked, the claim shows `PREPARING` with its deadline and amount, the record is written in the same transaction and rolls back with the claim, the not-eligible path holds the guarantee, the incomplete checklist reports the defect hold without writing a filed claim, and the case reaches `DEADLINE_TIMER_RUNNING`, `CLAIM_PREPARATION` and `CLAIM_APPROVAL` on the report.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required claim value is missing and the step cannot build the claim | Enter {field}. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the preparation is not made | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The texts are copied unchanged from the legacy story, FSD S3 A2.1.3.1 and the platform message set, and this story adds no message ID. The 403 of a right the role does not hold and the 409 of a claim already open carry the platform problem body; the 409 has no business text in any source read for this key. A missing scheme document and an unresolvable reference have no message identifier in any source: the checklist names the item on the officer task and no text is invented (GAP-2708; ASM-4494). Thai text for each message follows decision DL10.

### 15. Screens and states

The states empty, loading, error and no access of SCR-17: Not specified in the source documents (CG-ALL-8835).

SCR-17 Guarantee claim shows the guarantee, the claim deadline, the checklist and the claim result, in the states `Not due`, `due`, `submitted`, `paid` and `refused`. This story makes `Not due` and `due` real: the guarantee, the claim deadline, the claim type, the claimed amount and the checklist are read on the same screen through the gateway-bff composite route, which calls rwb-case and this service's claim answer in one hop each (DP-19; Architecture v5 slide 41). TSD S3 T-A.1 publishes no read operation, so the screen's claim content is what the create and update answers return and the composite route composes it with the case read (ASM-4501). The screen field list and the route specification belong to the platform edge story and the screen owner; this story fixes what the service writes. A held guarantee shows its reason code, never a claim deadline; an incomplete checklist shows the missing items, never a filed claim.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-013-01 | AC1 | End to end | Prepare a TCG guarantee claim |
| TC-E4-013-02 | AC2 | End to end | Rule R-GUA-04 |
| TC-E4-013-03 | AC3 | End to end | Rule R-GUA-01 |
| TC-E4-013-04 | AC4 | End to end | Not recorded |
| TC-E4-013-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-013-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-E4-013-07 | AC5 | Component | Required claim value missing |
| TC-E4-013-08 | AC6 | Component | Scheme default conditions not satisfied |
| TC-E4-013-09 | AC7 | Component | Scheme checklist incomplete at the preparation window |
| TC-E4-013-10 | AC8 | Component | A role without the right is refused with 403 |
| TC-E4-013-11 | AC9 | Component | Document references unresolved inside the retry budget |
| TC-E4-013-12 | AC10 | Component | Second case signal while the branch is running |
| TC-E4-013-13 | AC11 | Component | Date the default conditions are met is absent |
| TC-E4-013-14 | Section 12 | Component | Operations, events and activities of section 12 |
| TC-E4-013-15 | Section 12.7 (ASM-3438) | Component | Boundary of the tables of section 12.7 |
| TC-E4-013-16 | AC12 | Component | Business rules BR1 to BR10 of section 8 |
| TC-E4-013-17 | AC13 | Component | Error answers 401, 403 and 404 of the provided operations |
| TC-E4-013-18 | AC14 | Component | Replay of a write with the same idempotency key |
| TC-E4-013-19 | AC15 | Component | A retried or timed-out activity |
| TC-E4-013-20 | AC16 | Component | A case status change the model does not allow |
| TC-E4-013-21 | AC17 | Component | Business rule BR1 of section 8 |
| TC-E4-013-22 | AC18 | Component | Business rule BR2 of section 8 |
| TC-E4-013-23 | AC19 | Component | Business rule BR3 of section 8 |
| TC-E4-013-24 | AC20 | Component | Business rule BR4 of section 8 |
| TC-E4-013-25 | AC21 | Component | Business rule BR5 of section 8 |
| TC-E4-013-26 | AC22 | Component | Business rule BR6 of section 8 |
| TC-E4-013-27 | AC23 | Component | Business rule BR7 of section 8 |
| TC-E4-013-28 | AC24 | Component | Business rule BR8 of section 8 |
| TC-E4-013-29 | AC25 | Component | Business rule BR9 of section 8 |
| TC-E4-013-30 | AC26 | Component | Business rule BR10 of section 8 |

The legacy test case IDs, their Covers and their Data are kept in order and character for character; the story level "System" of the legacy suite is carried as "End to end" and the two exception cases as "Component", as in the other stories of this run. TC-E4-013-05 and TC-E4-013-06 restate the same guard as the legacy suite, so they run once each. The claim, case-signal, document-client, decision-record, rule-package and gateway fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The `-ITG` copies (TC-E4-013-01-ITG to TC-E4-013-06-ITG) belong to the wave 3 integration harness (RWB-ITG-W3) and are not written by this story. The contract's own tests are TC-S3-E4013-CON-01 to -05 and are owned by RWB-S3-E4013-CON.

### 17. Guardrails

- No value a business person may change is written in code: the rule IDs, the conditions, the preparation window, the 5 working day service level, the list members and the four messages are rule rows or governed rows with a version (BR-S3-001; BR1).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the claim ID, dates, amounts and versions only, and the fixture is synthetic.
- No read of another service's tables: the case arrives on the signal, the rule rows on the package event, the documents as references through the client library, and nothing joins across a schema (DP-01).
- No document content and no blob reference owned here: the checklist holds references only (BR8).
- ACE data only through the owner's contract or the `v_ace_*` views, and this story reads neither: the claimed amount comes from the case facts and the rule.
- No business value in the record: the `DecisionRecord` carries the rule ID, the rule version, the claim amount and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule (BR7).
- No live document store, no live case and no live rule package in any test: the client fake, the signal fake and the package fake are the only endpoints.
- No invented message for a missing document or an unresolvable reference: the item is named on the task and the gap stays open (GAP-2708).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline | Business Requirements Program v5, section 5.10 | FEAT-GUA-01 | 07 Route, settle and claim | R-GUA-01; R-GUA-04; BR1 to BR10 | TC-E4-013-01, TC-E4-013-02, TC-E4-013-03, TC-E4-013-04, TC-E4-013-05, TC-E4-013-06 |
| REQ-S3-007 | Claims are filtered for eligibility before submission so that ineligible claims are not filed | Business Requirements Program v5, section 5.10 | FEAT-GUA-01 | 07 Route, settle and claim | R-GUA-02; BR3 | TC-E4-013-01, TC-E4-013-02 |

REQ-S3-001 and REQ-S3-007 are the two requirements whose text names this behaviour, so the trace runs on them; TSD S3 T8 maps the module's requirements to FEAT-GUA-01 as the "written one epic ahead" placeholder, and the feature code FEAT-GUA-01 of FSD S3 A2.1 is carried alongside until the C1 PRD settles the mapping (Section 19). The legacy key names FEAT-DCM-16 as its prerequisite; that feature is the case and decision data of P3 and P7 and is reached through the case signal and the package event, so it is not carried as a row.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4013-CON | Contract | H: declares the resource, the DDL template, the error set, the versioning rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-17 shows the `Not due` and `due` states |
| RWB-S3-E4014-APP | App development | Sibling: approves the assembled claim and submits it on the TCG claim channel; starts where this branch leaves the claim |
| RWB-S3-E4015-APP | App development | Sibling: tracks the claim to payment, records the lost claim and the service level breach |
| RWB-S3-E4016-APP | App development | Sibling: records the subrogation position after payment |
| RWB-S3-E4017-APP | App development | Sibling: notifies guarantors and co-borrowers |
| P3 rwb-case | Service | The case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P5 rwb-document | Service | The scheme documents whose references the checklist resolves |
| P7 rwb-decision | Service | The `GUA` package and the 32 rows; EV-30 is consumed here |
| RWB-ITG-W3 | Integration | I: the cross-service proof of the preparation against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published resource, the DDL template, the error set, the versioning rule and the fakes: RWB-S3-E4013-CON.
- The approval of the assembled claim and its submission on the TCG claim channel: RWB-S3-E4014-APP, with INT-29 outside the cluster.
- The tracking of the claim to payment, the query and rejection answers, the lost claim and the service level breach: RWB-S3-E4015-APP.
- The subrogation position and the closing of a guarantee that clears the balance: RWB-S3-E4016-APP.
- The guarantor and co-borrower notices: RWB-S3-E4017-APP.
- The case, its status, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3), reached only through the forwarded case signal and the stage report.
- The rule authoring, the four-eyes approval, the effective date and the central ledger: rwb-decision (P7).
- The guarantee documents, their metadata and their blob references: rwb-document (P5); the checklist holds references only.
- The value of the preparation window, a rule-row parameter of the `GUA` package set by the rule owner, and the date the default conditions are met, a fact of the case signal and not a `guarantee_claim` field: the values are Not specified in the source documents (GAP-2708; ASM-4493; ASM-4497).
- Any call to the rwb-agent runtime for the "claim preparation agent" of AC2: the preparation is confirmed as one unattended step, so no agent binding is built in this story (ASM-4495).
- SCR-17, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof against the live owners and the `-ITG` copies of the legacy cases: RWB-ITG-W3.
- Open decision DL10 (the Thai wording of every message): still open; the Thai text of the messages of this story follows DL10.
