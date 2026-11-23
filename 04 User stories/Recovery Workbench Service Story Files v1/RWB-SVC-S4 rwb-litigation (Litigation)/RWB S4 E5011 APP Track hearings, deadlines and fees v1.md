# RWB-S4-E5011-APP Track hearings, deadlines and fees

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5011-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-011 for rwb-litigation (S4). The court calendar is the `hearing` table of schema `rwb_litigation` served on `/api/recovery/litigation/v1` (DP-13); each deadline is a durable timer of `LitigationWorkflow` and not a `timer` row of the case service (GAP-2789; ASM-4627); the accrued fee is read on the rwb-payment contract and never written here (GAP-2788; ASM-4626); one decision record is written through the local decision-record library before any hearing or deadline changes (DP-03); the two workspaces read the calendar through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the court calendar of a legal action held in this service, every hearing raising its deadline as a durable clock of the litigation workflow, and the fee accrued against the case shown from the service that owns the money, with one decision record written before any of it changes**, so that **no sitting, no next date and no spend deadline is lost while a case runs for years, and the case, the rules and the money stay with the services that own them**.

This story owns the hearings of a legal action and the deadlines they raise:

- the `hearing` row of schema `rwb_litigation` with DF-LEG-024 to DF-LEG-029 (id, legal_action_id, hearing_date, hearing_type of LOV-HEARING, outcome of LOV-HEARING-OUTCOME, next_date), created on `POST /legal-actions/{legalActionId}/hearings` (API-S4-005), read on `GET /legal-actions/{legalActionId}` (API-S4-003) and updated on `PATCH /legal-actions/{legalActionId}` (API-S4-004), all on base `/api/recovery/litigation/v1` (DP-13; TSD S4 T-A.1, T-A.2);
- the deadline that a hearing raises: a durable timer of `LitigationWorkflow` on task queue `rwb-litigation`, armed from the hearing date and re-armed from `next_date`, with no `timer` row written, because the `timer` row DF-WRK-027 to DF-WRK-036 of the legacy data table is rwb-case's projection and not a litigation table (GAP-2789; ASM-4627);
- the sitting result: `outcome` of LOV-HEARING-OUTCOME and the `next_date` the court sets, and the calendar read that SCR-19 Litigation workspace and SCR-20 Enforcement workspace show;
- the evaluation of R-LIT-33, R-LIT-34, R-LIT-35, R-LIT-41, R-LIT-42 and R-LIT-43 of the LITIGATION route set with the rule rows at their version in force, and the one decision record each evaluation writes before the row changes (DP-03; legacy AC1 and AC2);
- the accrued fee and the spend deadline of the case, **read** on the rwb-payment contract: this service shows the accrual, raises the fee-due fact and records the spend decision; it posts no fee, holds no fee table and moves no balance (GAP-2788; ASM-4626).

It owns nothing else. `recovery_case`, its route states and its `timer` and `task` rows are rwb-case's (P3); the judgment facts on `legal_action` (DF-LEG-011, DF-LEG-012) belong to the judgment story of this service; the pack, the notice and its proof belong to rwb-document (P5) and rwb-comms (P6); the firm instruction belongs to the partner route and its own story. No component writes a `recovery_case`, a `timer`, a `task`, a `notice`, a `document` or a fee row, and none reads a `v_ace_*` view.

### 2. Business rationale

Litigation is the longest journey in the Workbench: the architecture slides say a case runs "for years without anyone holding a spreadsheet", the court dates "arrive as signals", and the legal prescription clock is never paused although a deviation pauses the stage clock (context pack slides 3 and 7). The legacy feature states the answer — "Follows the court calendar, raises each deadline and accrues the fees against the case" (FSD S4 A2.11.1) — and the legacy story gives that whole step to one process against one `recovery` schema, with the case row, a `timer` row, the decision log entry and a rule row written together.

The target cuts the same step three ways. The hearing and its dates stay with litigation, because `hearing` and `legal_action` are this service's two tables (context pack ownership rows). The case state and the case clock leave for rwb-case, because `recovery_case`, `timer` and `task` are P3's rows and the stage clock of the case belongs to `CaseWorkflow` (TSD S4 T5.2). The fee leaves for rwb-payment, because no column of `hearing` or `legal_action` carries a fee (TSD S4 T3.1) and R-LIT-42 posts the spend "against the case" through the core bank and the general ledger, which is the payment module's work (context pack slide 4). What remains here is the owned row, the owned clock and the rule answer, and that is what this story builds.

Two consequences are written down rather than hidden. A hearing date can arrive in years, so the clock must be a durable workflow timer and not a scheduled job: the service has no Job and DP-10 is outside the pattern set of this key. And "accrues the fees" cannot be an S4 write: the accrual is read on the rwb-payment contract, whose operation is named by no source (GAP-2788).

It serves FEAT-LIT-11 "Track hearings, deadlines and fees", it carries the module measure "litigation turnaround, 6 days" by keeping every court date and every spend deadline on one owned row and one owned clock, and it holds the legacy prerequisite FEAT-LIT-10 through the filing that the previous story records. The two legacy criteria AC1 and AC2 belong to this story and are copied word for word in section 7. The requirement identifiers of the key are absent from the legacy master and from TSD S4 T8, so the story traces to the feature until the PRD adds them (GAP-2792; ASM-4630).

### 3. Preconditions

- `RWB-S4-E5011-CON` is published: the three operations on `/api/recovery/litigation/v1`, the `HearingRequest`, `Hearing` and `LegalActionUpdate` schemas, the two LOV vocabularies, the error envelope, the `Idempotency-Key` rule and the fakes. It is the first build dependency of this story, so the story starts on Day 1.
- The `hearing` and `legal_action` tables exist in schema `rwb_litigation` with DF-LEG-001 to DF-LEG-014 and DF-LEG-024 to DF-LEG-029 of TSD S4 T3.1 and the standard columns of T3.0. No table and no column is created by this story.
- The legal action the hearing hangs on exists: it is opened by the legal-action story of this service (API-S4-002) and the filing that sets the hearing timers is recorded under R-LIT-30 by the previous story of this key.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`), and the record is relayed on the shared topic `rwb.decision-record.v1`.
- `LitigationWorkflow` runs on task queue `rwb-litigation` in namespace `rwb-recovery` as a child of `CaseWorkflow`, and it hosts the hearing and deadline timers. The workflow kit contract is not in this story's dependency rows although the workflow is a platform capability; the absence is recorded as GAP-2789 with ASM-4627.
- The case read that answers the route state, the prescription date and the product group is consumed on rwb-case, operation `Not specified in the source documents (GAP-2791; ASM-4629)`; it is consumed and faked, not built.
- The accrued fee and the spend limit of the case are consumed on rwb-payment (P8), operation `Not specified in the source documents (GAP-2788; ASM-4626)`.
- The rule rows of the LITIGATION route set are read from rwb-decision at their version in force, operation `Not specified in the source documents (GAP-2790; ASM-4628)`.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-19 and SCR-20, so the calendar is readable from Day 1 (DP-19).
- LOV-HEARING (`FIRST_HEARING`, `WITNESS`, `JUDGMENT_READING`, `MEDIATION`) and LOV-HEARING-OUTCOME (`HELD`, `ADJOURNED`, `SETTLED`, `JUDGMENT`) of TSD S4 T3.2 are read as values in force with their version on the reference data of rwb-case, whose dependency row this key does not carry (GAP-2792; ASM-4630).
- The caller holds a Workbench role with a Litigation right on the operation it calls (TSD S4 T6.1): RW-LITOFF holds CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM and the case-workflow and rules identities hold R or U as T6.1 gives them.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. `LitigationWorkflow` is signalled with a court date by the firm or by the court entry that rwb-partner records; the date arrives as a signal and is never polled from an ACE view.
2. The officer opens SCR-19 Litigation workspace in its hearing state through the gateway-bff composite route (DP-19) and reads the action and its hearings on `GET /legal-actions/{legalActionId}`: status, court fields, and each hearing with its date, type, outcome and next date.
3. The officer records a sitting on `POST /legal-actions/{legalActionId}/hearings` with `HearingRequest`: `hearingDate`, `hearingType` of LOV-HEARING and the `legalActionId`. The `Idempotency-Key` header is required and its answer is stored.
4. `HearingValidator` checks the legal-action reference and its status, the hearing type against LOV-HEARING, the presence of the date and the caller's scope. A failed check answers 404, 409 or 422 and nothing is written.
5. `HearingDecisionWriter` evaluates R-LIT-33 with the rule rows at their version in force and writes one decision record through the local library **before** the row changes: rule ID, version in force, inputs reference, the answer and the decision code (DP-03; legacy AC1).
6. `HearingWriter` writes, in one `rwb_litigation` transaction, the `hearing` row and the idempotency row of the request. The legal action is read, not changed, on this step.
7. `DeadlineScheduler` returns the deadline to the workflow: `hearing_date` for the sitting itself and `next_date` (DF-LEG-029) when the court sets one. The workflow arms one durable timer per deadline on queue `rwb-litigation` and writes no `timer` row (GAP-2789; ASM-4627).
8. When the court sits, the officer records the result on `PATCH /legal-actions/{legalActionId}` with `LegalActionUpdate`: `outcome` of LOV-HEARING-OUTCOME and `nextDate` where the court adjourned. R-LIT-34 re-arms the timer and records the postpone reason code; R-LIT-35 returns the case to the calendar on the new date.
9. When a timer fires, `DeadlineSignal` raises the deadline fact to the case of record and to the officer's task list on their contracts and writes the deadline decision the same way as step 5; nothing is written to a case row or a task table of this service.
10. Where a court fee or a legal expense falls due, R-LIT-41 routes the spend to the approver at the D7.4 limit, R-LIT-42 records the approved fee against the case and R-LIT-43 records a rejection with its reason. The posting itself is rwb-payment's; this service records the decision and the approved fact (GAP-2788; ASM-4626).
11. `FeeAccrualReader` reads the accrued fee and the spend deadline of the case on the rwb-payment contract and returns them to the workspace with the case reference, the spend type, the value date and the approval state. A fee due inside the horizon raises the fee-due fact.
12. A repeated create with the same action, date and type, or with the same `Idempotency-Key`, writes once and returns the stored answer; the repeat is counted under R-UNI-40.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no `hearingDate`, no `hearingType`, or a type outside LOV-HEARING | 422; no decision record and no row | MSG-GEN-001 | AC1 |
| X2 | The legal-action ID names no row inside the caller's scope | 404; an out-of-scope action cannot be told from a missing one | None | AC1 |
| X3 | The legal action is `CLOSED` or `WITHDRAWN`, or the same date and type already has a hearing | 409; nothing changes | None | AC1 |
| X4 | The case read reports the claim inside the warning window | MSG-S4-002 is shown with the date; the hearing is not blocked | MSG-S4-002 | AC1 |
| X5 | A role without the Litigation right records, reads or patches a hearing | Refused before any read or write; no decision record | MSG-P4-002 | AC1 |
| X6 | The local decision-record write fails | The transaction writes nothing: no hearing, no timer, no fact | MSG-P7-003 | AC2 |
| X7 | The rwb-payment fee read does not answer inside 2 s or its breaker is open | The calendar still answers from this service's own rows; the accrual panel shows the stale marker | MSG-P1-001 | AC1 |
| X8 | A timer fires for a hearing that has since been adjourned or cancelled | The timer completes without a second decision and the fact is not raised twice | None | AC1 |
| X9 | A statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | BR6 |
| X10 | The case read refuses or delays the deadline fact | The hearing keeps what it wrote, because that fact is this service's own; the failed hand-off is visible and the workflow re-raises it | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5011-CON`, the decision-record library, the composite route and the fakes of rwb-case, rwb-payment and rwb-decision; no C dependency blocks the build |
| Negotiable | The hearing lead time, the escalation horizon and the fee horizon are versioned reference rows; the story fixes the shape and the behaviour, not the values |
| Valuable | Every sitting, next date and spend deadline of a case that runs for years sits on one owned row and one owned clock, with a decision record before each change |
| Estimable | Three operations, one validator, one rule evaluation, one library write, one repository write, one workflow step with three activities, two clients and a read-only workspace fragment |
| Small | Fits one sprint with its tests, as the primary slice of the legacy key |
| Testable | Each criterion of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5011-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Track hearings, deadlines and fees, in rwb-litigation

  Background:
    Given the legal action "LA-2026-001211" exists on case "RC-2026-001211" with status "FILED"
    Given the rule rows of the LITIGATION route set are in force at their version, and LOV-HEARING and LOV-HEARING-OUTCOME are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Track hearings, deadlines and fees (legacy RWB-E5-011 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-payment contract mock returns the accrued fee and the spend deadline of case "RC-2026-001211"
    Given the rwb-case contract mock returns the route state "IN_HEARING" and the prescription date of the case
    When its trigger arrives
    Then follows the court calendar, raises each deadline and accrues the fees against the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E5-011 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two scenarios are the legacy criteria word for word, with the cross-service reads the target adds stated as mock Givens: the fee and its spend deadline are rwb-payment's and the route state and the prescription date are rwb-case's. Nothing in the legacy wording is changed, reordered or narrowed.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The court calendar of a legal action is this service's `hearing` row; no other service writes it and this service writes no other service's calendar | Context pack ownership rows; TSD S4 T3.1 |
| BR2 | Every hearing raises its deadline as a durable timer of `LitigationWorkflow`; the time of a case is the workflow's, not a `timer` row, a Quartz job or a Schedule | DP-10 (not in this key's set); context pack ownership rows (Jobs 0, Workflows 1); GAP-2789 |
| BR3 | The decision record is written before any hearing, deadline or spend decision changes, through the local library on `rwb.decision-record.v1`; a failed write changes nothing | DP-03; TSD S4 T2; legacy AC1 and AC2 |
| BR4 | A hearing is scheduled under R-LIT-33, reset under R-LIT-34 with its postpone reason code and returned to the calendar under R-LIT-35; the rule rows and their version are read from rwb-decision | Business Rules and Routing Logic v4 (R-LIT-33 to R-LIT-35); GAP-2790 |
| BR5 | A fee is routed under R-LIT-41, recorded as approved under R-LIT-42 or rejected under R-LIT-43; the fee row, the posting and the balance stay with rwb-payment | Business Rules and Routing Logic v4 (R-LIT-41 to R-LIT-43); GAP-2788 |
| BR6 | No value a business person may change is written in code: the hearing lead time, the escalation horizon, the spend limit and every LOV value are reference or rule rows with a version | FSD S4 A2.11.3.1 (BR-S4-011); principle 1 |
| BR7 | A deviation pauses the litigation stage clock but never the prescription clock; this service pauses its own timers and never pauses a legal deadline | Context pack slide 3 notes (R-DEV-01); context pack slide 7 |
| BR8 | The stale marker of a source product is shown with MSG-P1-001 and blocks no hearing; the batch-status check is the owner's | FSD S4 A2.11.3.1 (VR-S4-011-1) |
| BR9 | No personal data in a log, a workflow input, a fixture or a prompt; the row carries references, dates, codes and a rule version only | Template and Rules §R7.2 (s17); FSD S4 A2.11 |
| BR10 | One REST base, one topic, one queue and one login per service; this service never chains a call to a third service on behalf of a screen | DP-13, DP-14; ADR-020 |

### 9. State transitions

The transition table is TSD S4 T4 and the Business Rules and Routing Logic v4; this story owns the hearing part of it and answers the rest to rwb-case.

| From | Event | Condition | To | Rule |
|---|---|---|---|---|
| FILED_IN_COURT | Hearing scheduled | the court sets a hearing date | IN_HEARING | R-LIT-33 |
| IN_HEARING | Hearing adjourned | outcome = `ADJOURNED` | HEARING_ADJOURNED | R-LIT-34 |
| HEARING_ADJOURNED | New date set | `scheduled_for` reset by the court | IN_HEARING | R-LIT-35 |
| IN_HEARING | Fee due | a court fee or legal expense falls due | LEGAL_SPEND_APPROVAL | R-LIT-41 |
| LEGAL_SPEND_APPROVAL | Fee approved | inside the limit, or the committee approves above it | IN_HEARING | R-LIT-42 |
| LEGAL_SPEND_APPROVAL | Fee rejected | the approver rejects the spend | IN_HEARING | R-LIT-43 |

The case state itself is written by rwb-case on this service's answer: the stage outcome carries the state name, the rule ID and the package version, and this service writes no `recovery_case` row. The hearing row moves through its own values of LOV-HEARING-OUTCOME (`HELD`, `ADJOURNED`, `SETTLED`, `JUDGMENT`) on the same `hearing` row, and `legal_action.lit_status` (DF-LEG-013) follows the LOV-LEGAL-STATUS values `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Litigation officer (RW-LITOFF) | Record a hearing, record its outcome and next date, read the calendar and the accrual |
| Enforcement owner (RW-ENFORCE) | Record a hearing of an enforcement action and read the calendar (CRU) |
| Legal counsel, product head, head of litigation (RW-LEGAL, RW-PRODHEAD, RW-HEADLIT) | Read the calendar and approve the spend path where R-LIT-41 routes it |
| Partner and agency manager (RW-AGENCYMG) | Read the calendar of the instructed firm's actions |
| Rules and agent identities (SY-RULES, SY-AGENT) | Read the rule answer and the calendar under a service identity, never write a hearing |
| Tech lead of rwb-litigation | Owns the implementation and the four build steps of section 13 |
| Architect of the platform library and of the edge | Own the decision-record library, the envelope and the composite route this story consumes |

### 11. Data

| Entity | Fields | Owner | Use in this story |
|---|---|---|---|
| hearing | DF-LEG-024 to DF-LEG-029: id, legal_action_id, hearing_date, hearing_type, outcome, next_date | S4 `rwb_litigation` | Created, read and updated by this story |
| legal_action | DF-LEG-001 to DF-LEG-014; read for status and court fields, and `lit_status` and `filed_date` read only | S4 `rwb_litigation` | Read here; its judgment and filing columns belong to their own stories |
| decision_record | DF-DEC-001 to DF-DEC-018 shape, through the local library | PLT library in `rwb_litigation` | One record per hearing or deadline decision (DP-03) |
| idempotency_key | The key of a repeated create or update | PLT library in `rwb_litigation` | Stores the answer of a repeated request |
| recovery_case, timer, task | DF-WRK-027 to DF-WRK-036 for the timer | P3 rwb-case | Read through the case and answer contracts only |
| rule_row | DF-REF-001 to DF-REF-015 | P7 rwb-decision | Read at the version in force (GAP-2790) |
| Fee and posting rows | No field list in any source for this key | P8 rwb-payment | Read as the accrued fee and the spend deadline (GAP-2788) |

The standard columns of TSD S4 T3.0 (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`) apply to the two owned tables. No new table, no new column and no migration is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Contract element |
|---|---|---|---|---|
| POST | `/legal-actions/{legalActionId}/hearings` | Add a hearing date to a legal action (API-S4-005) | Litigation U | `HearingRequest` in, `Hearing` out; `Idempotency-Key` required |
| GET | `/legal-actions/{legalActionId}` | Read the action with its pack, instruction, hearings and judgment (API-S4-003) | Litigation R | `LegalAction` out, hearings included |
| PATCH | `/legal-actions/{legalActionId}` | Record the hearing outcome and the next date (API-S4-004) | Litigation U | `LegalActionUpdate` in, `LegalAction` out |

Base `/api/recovery/litigation/v1`. The other two operations of the service — `POST /cases/{caseId}/legal-actions` (API-S4-002) and `POST /notices/{noticeId}/approve` (API-S4-001) — belong to the sibling stories of this service and are not provided by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use here |
|---|---|---|---|
| `Not specified in the source documents (GAP-2788; ASM-4626)` | `/api/recovery/payment/v1` | P8 rwb-payment | The accrued fee, its spend deadline, its value date and its approval state; faked |
| `Not specified in the source documents (GAP-2791; ASM-4629)` | `/api/recovery/case/v1` | P3 rwb-case | The route state and the prescription date, and the answer that carries the stage outcome, the case timer and the officer task; faked |
| `Not specified in the source documents (GAP-2790; ASM-4628)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-33 to R-LIT-35 and R-LIT-41 to R-LIT-43; faked |

Every row is one hop with a 2 s timeout, a breaker per downstream and a GET retried once with jitter (ADR-020). None of the three is a dependency row of this key; each is a C dependency in fact and the absence is recorded as GAP-2788, GAP-2790 and GAP-2791.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14) and the ownership rows of this service publish zero events; DP-09 is outside this key's pattern set. The decision record leaves on `rwb.decision-record.v1` through the library of DP-03 and is not an event of this service.

#### 12.4 Events consumed

None. `HEARING_SCHEDULED`, `HEARING_ADJOURNED`, `NEW_DATE_SET`, `FEE_DUE`, `FEE_APPROVED` and `FEE_REJECTED` are the event names of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions: the service holds no consumer group and no inbox, and every fact arrives on the contracts of 12.2 (GAP-2791; ASM-4629).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | Hosts the hearing and deadline timers; its signals and its stage outcome are declared, not built |
| `recordHearing` | Activity | `rwb-litigation` | The hearing row in; the decision record, the rule ID with its version and the deadline out |
| `armHearingDeadline` | Activity | `rwb-litigation` | The hearing date or `next_date` in; one durable timer armed and its fact out |
| `recordSpendDecision` | Activity | `rwb-litigation` | The fee and its approval state in; the decision record and the approved fact out |

The three activity names and the signal names are target design choices fixed by no source; the timers themselves are the pattern of DP-10 applied as durable workflow timers, because the service owns no Job (context pack ownership rows).

#### 12.6 Schedules

None. The two clocks of the story are durable timers of `LitigationWorkflow`: the sitting date and the re-armed date from `next_date`. This story declares no Temporal Schedule, no Quartz row, no shared job table and no batch window; the prescription warning is a case fact read on 12.2 and never a Schedule of this service (GAP-2789).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| hearing | S4 (`rwb_litigation`) | Created, read and updated by this story |
| legal_action | S4 (`rwb_litigation`) | Read for status and court fields; `lit_status` and `filed_date` read only |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of every hearing and spend decision (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated create or update |

`recovery_case`, `timer` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `notice` (P6), `document` (P5) and the fee rows (P8) are not owned here, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment fee fake | The accrued fee and the spend deadline of case `RC-2026-001211` with its value date and the approval states `PENDING`, `APPROVED` and `REJECTED`; no amount is fixed by any source (GAP-2788) | AC1 |
| rwb-case fake | The route state `IN_HEARING` and another state, the prescription date and the accepted stage outcome with the case timer and the officer task | AC1 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-33 to R-LIT-35 and R-LIT-41 to R-LIT-43, and a second version | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC1, AC2 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 model of case `RC-2026-001211` | AC1 |

The fakes are test-only and are replaced by the owners' services in SIT. The fee amounts, the hearing lead time and the spend horizon are reference values and are never fixed in the fake beyond the shape the document gives (GAP-2788, GAP-2789).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The hearing create, the action read and the action update provided; the fee read, the case read and answer, and the rule package read consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities, 2 durable timers | `LitigationWorkflow`, `recordHearing`, `armHearingDeadline`, `recordSpendDecision`, the sitting date and the next date; no Schedule |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Deliverables.** The hearing API (three operations on the base of DP-13), `HearingValidator`, the rule evaluation of the six rules and the decision-record writer of DP-03, the `hearing` repository, the three workflow activities and the two durable timers, the fee and case clients with their breakers, and the SCR-19 and SCR-20 read fragment behind the composite route of DP-19.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is applied in behaviour but not in the pattern set: the deadline is a durable timer of the workflow, and no Schedule or Quartz row is introduced. DP-06, DP-07 and DP-04 are outside the set although the story reads reference values and rule rows; the read is on the owners' contracts and the absence of the dependency rows is recorded (GAP-2790, GAP-2792).

**Build steps**

1. Publish the three operations and the two schemas of 12.1 against the CON, with the validator and the error envelope.
2. Write the decision-record writer and prove the "nothing changes" rule of AC2 on a stopped chain.
3. Write the `hearing` repository and the idempotency row in one transaction.
4. Write the three activities and the two durable timers of `LitigationWorkflow`; prove a timer armed for a date in a later year still fires.
5. Write the fee and case clients with their fakes, their 2 s budget and their breakers, and the accrual panel behind the composite route.
6. Wire the six rules to the rule rows at their version in force and record the rule ID with its version on every decision.
7. Finish the boundary tests: no read of another `rwb_*` schema, no `v_ace_*` view, no write of a case, a timer or a fee row.

**Done when.** The two legacy criteria pass end to end against the fakes, the deadline survives a restart and a release, the accrual panel shows the owner's value with its stale marker, and the boundary tests are green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack of the action is incomplete at filing, which is the pack story's path; no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The prescription date of the case is inside the warning window, as the case read reports it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The source product of a consumed read is stale after a late or failed ACE batch | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs and their text are the legacy set of this key and the FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is VR-S4-011-1 of the feature, and the batch-status check itself is the owner's, not this service's.

### 15. Screens and states

| Screen | States |
|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment |
| SCR-20 Enforcement workspace | Requested; seized; auctioned; closed |

Both screens read the calendar, the next date and the accrual through the gateway-bff composite route (DP-19), next to the case route state of rwb-case and the fee of rwb-payment. The hearing state of SCR-19 shows the next sitting, its deadline and the accrual panel; the refusal, stale-marker and timer-held states read the messages of section 14 on the same route. The composite route specification and the screen field list belong to `RWB-PLT-N001-CON`.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-011-01 | AC1 | End to end | Track hearings, deadlines and fees |
| TC-E5-011-02 | AC2 | Component | Not recorded |
| TC-E5-011-03 | AC1 (access path) | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-011-04 | AC2 (forced failure) | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The four legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy table carries no level column, so the case that exercises the whole step maps to `End to end`, the access case and the not-recorded case to `Component`, and the forced failure of Principle 5 to `NFR`. The access and forced-failure cases test the same two criteria from their own angle, which is why they are listed against AC1 and AC2. The fakes and the stub of 12.8 stand behind every case, and the fixture data — case `RC-2026-001211`, legal action `LA-2026-001211`, a sitting on 2026-12-15 and a next date in 2027 — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the hearing lead time, the escalation horizon, the spend limit, the LOV values and the message texts are values of reference or rule rows with a version; no day count, list value or state name appears in Java.
- No personal data in logs, workflow inputs, fixtures or prompts: references, dates, codes and a rule version only, and every fixture is synthetic.
- The case stays with rwb-case: no `recovery_case` row, no route state, no `timer` row and no `task` row is written here; the stage outcome is answered with the rule and its version (BR2).
- The money stays with rwb-payment: no fee row, no posting and no balance is written here; the accrual is read and the fee-due fact is raised (BR5).
- ACE data only through the owner's contract: no component reads a `v_ace_*` view or an ACE table, and the service holds no such grant (DP-05 applied as a prohibition).
- No read of another service's tables and no cross-schema join: `recovery_case`, `timer`, `task`, `rule_row`, `decision_log_entry`, `notice`, `document` and the fee rows are reached only through their owners' contracts (DP-01).
- Every change of a hearing, a deadline or a spend decision is preceded by its decision record; a failed write leaves the row untouched and the user sees MSG-P7-003.

### 18. Traceability

| Requirement ID | Requirement (short) | How this story satisfies it | Test cases |
|---|---|---|---|
| FEAT-LIT-11 | Track hearings, deadlines and fees (FSD S4 A2.11); the legacy master and TSD S4 T8 carry no requirement ID for this key (GAP-2792; ASM-4630) | The `hearing` row, the two durable timers, the six rules and the read accrual | TC-E5-011-01 to -04 |
| R-LIT-33, R-LIT-34, R-LIT-35 | Hearing scheduled, adjourned and re-dated (Business Rules and Routing Logic v4) | The scheduling, the reset and the return to the calendar, each with its decision record | TC-E5-011-01, TC-E5-011-02 |
| R-LIT-41, R-LIT-42, R-LIT-43 | Fee due, approved and rejected | The spend decision recorded here and posted by rwb-payment | TC-E5-011-01 |
| BR-S4-011, VR-S4-011-1 | No value in code; the stale marker of a source product | Reference rows with a version and the stale marker with MSG-P1-001 | TC-E5-011-03, TC-E5-011-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-011, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Legacy screens | SCR-19 Litigation workspace; SCR-20 Enforcement workspace |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal and durable timers), ADR-020 (contract-first REST, one hop, 2 s), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The case of record, its route states, the case clock, the case-stage timer and the officer task: rwb-case (P3), consumed on 12.2 (GAP-2791).
- The fee row, the posting, the balance and the payment match: rwb-payment (P8), consumed on 12.2 (GAP-2788).
- The rule rows, their authoring, testing, approval and versioning, and the LITIGATION package: rwb-decision (P7) (GAP-2790).
- The pack, the notice and its proof of delivery, the firm instruction and the judgment: the pack and notice stories of this service, rwb-document (P5), rwb-comms (P6), rwb-partner (S9) and the judgment story of S4.
- The prescription clock and its warning value: the case of record and the deviation route, with MSG-S4-002 read from them.
- The rights, roles, scope and masking data, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this key.
