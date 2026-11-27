# RWB-ITG-E1021-ITG Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Event type corrected to `rwb.decision.DecisionRecorded.v1`; the topic stays `rwb.decision-record.v1`.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1021-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1021-ITG-16); squad sizes at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E1021-ITG-23); consumed contracts are addressed by their /v1 path only |
| Integration dependencies | RWB-P3-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP, RWB-P5-E1021-APP, RWB-P4-E1021-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008 |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-021 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1021-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (35 resolved, 11 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-021 transfer rules and engine across rwb-case (the case router with its inbox, the transfer path with its assignment swap, the two endpoints, the overflow placement and the local decision record), rwb-decision (the TRANSFER package version with its checksum and the central decision ledger), rwb-access (the Queue and allocation right U and the Case record right U that guard a transfer and a legal hold), rwb-document (the DocumentStored trigger), rwb-deviation (the DeviationRaised and DeviationCleared triggers) and the rwb-payment PaymentMissed trigger**, so that **a case changes hands by the rule package once per trigger, with its rule ID and package version in the central ledger, its one CaseTransferred event on the owner's topic, a legal hold that stops an automated move and a manual transfer that keeps its contract, and the hand-off between teams is proved on the real services before wave 1 exits**.

### 2. Business rationale

RWB-E1-021 moves a case between queues and roles by the TRANSFER rule package on eight triggers or on a manual request with a coded reason, so that the hand-off between the TDR, litigation, NPA and debt sale teams runs without email and a case never waits between teams with nobody holding it. The component copy of the behaviour already exists: RWB-P3-E1021-APP owns the legacy criteria AC1 to AC14 and the Access test in rwb-case, against the published contracts of the services it needs. This integration story owns no legacy criterion at all. Every criterion in section 7 is new, and each one tests only what no single service can prove: the trigger really arriving from its owner, the rule package really governed in another service, the record really reaching the central ledger, the event really leaving on the owner's topic, the hold really coming from another service's right, and the queue and the reason list really read as reference data instead of hard-coded.

The cross-service part is not decoration. Six of the eight triggers are facts produced by services that are not rwb-case: `rwb.payment.PaymentMissed.v1` from rwb-payment, `rwb.document.DocumentStored.v1` from rwb-document, `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` from rwb-deviation, `rwb.decision.ApprovalRequested.v1` from rwb-decision, and the stage-change and route-decided facts that rwb-case commits itself as `rwb.case.CaseStateChanged.v1`. The package is governed in rwb-decision and only evaluated locally, so a suite that read a local table would never notice an unapproved or unchecksummed version reaching the transfer path. The decision record of a transfer commits in rwb-case but is collected into the central ledger of rwb-decision within five minutes, and an assertion on the local record alone would pass while the ledger stayed empty. The manual transfer is guarded by a right that rwb-access owns, and the reason list, the queue, the cap and the overflow queue are reference rows that rwb-case owns. None of those can be proved inside one service.

The legacy story runs a listener on the monolith outbox (DP-09), evaluates TRANSFER through an in-process `RuleEvaluator` (DP-04), writes the decision log entry through a published interface of the case module (DP-03) and serves `/api/recovery/v1` (DP-13). The target delta is the mechanism and the delivery path, not the behaviour. The monolith outbox listener is replaced by Kafka events from their owners, each consumed once through the inbox of the rwb-case case router, which turns the fact into a Temporal signal on CaseWorkflow and never into a REST call (EV-29, Arch v5 slide 42 row 29, DP-09). The rule model is fetched from rwb-decision with its SHA-256 verified and evaluated locally inside the EvaluateRules activity of rwb-case, so no shared rule server sits on the hot path (DP-04). The decision record is written in the same transaction as the case move and collected into the central ledger as `rwb.decision.DecisionRecorded.v1` (DP-03, ADR-022). The endpoints move to `/api/recovery/case/v1/...` (DP-13), the events move to `rwb.case.events.v1` in the CloudEvents envelope (DP-14), and JOB-05 and the TimerDue event are retired, so the timer trigger is a durable timer inside CaseWorkflow and not a job (DP-10, Arch v5 slides 42 and 44). The queue row and the reason row come from the reference-data contract of rwb-case (DP-07), and the caller right comes from the authorise contract of rwb-access, which is DP-08 used as the guard of the two endpoints and is not one of the listed patterns of this story.

No service contract is faked in this story: the five integration dependencies are the real services on their published contracts, and a fake would defeat the purpose of the run. Two things the sources do not settle are recorded rather than invented. The route-decided trigger is read as the route-decided fact that rwb-case commits as `rwb.case.CaseStateChanged.v1`, while Arch v5 gives the route itself to rwb-valuation and announces it as RouteDecided to rwb-case, and rwb-valuation is a wave 3 service that a wave 1 run cannot observe; and the composition of the synthetic fixture set is left to the harness. Both are carried as GAP-0346 with ASM-0440. The legacy values stay as they are: package "TRF-2026.11" with rows TRF-001 to TRF-009, queues "TDR-BKK-CO", "TDR-BKK-APR", "LIT-BKK-OFF", "LIT-BKK-OVF", "DIL-BKK-CO", "NPA-BKK-CO" and "DEV-HANDLER", the cap of 150, the reasons R01 to R06, the cases RW-2026-000301 to RW-2026-000314 and the event ID EVT-88120. Release 30 November 2026 is tentative and is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1021-APP is done: the case router with its inbox and its `signalWithStart` call, the eight-trigger transfer path with the version lock and the assignment swap, the overflow placement, the two endpoints `POST /api/recovery/case/v1/cases/{caseId}/transfer` and `POST /api/recovery/case/v1/cases/{caseId}/legal-hold`, the local decision record with `rwb.case.CaseTransferred.v1` in the same transaction, and the reference data of the transfer reason list and the queues are in SIT on rwb-case.
- RWB-P7-E1021-APP is done: package TRANSFER version "TRF-2026.11" with its SHA-256 and its valid-from date, the rule-package version list and the central decision ledger are published by rwb-decision.
- RWB-S8-E1021-APP is done: `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` leave rwb-deviation on `rwb.deviation.events.v1` for the case that is screened and cleared.
- RWB-P5-E1021-APP is done: `rwb.document.DocumentStored.v1` leaves rwb-document on `rwb.document.events.v1` when a document is stored against a case.
- RWB-P4-E1021-APP is done: the Queue and allocation right U and the Case record right U are enforced by rwb-access, and its refusal is observable on the two endpoints.
- The published contracts of P3, P4, P5, P7 and S8 are versioned in the registry, and the harness consumes only those contracts; the suite opens no service schema.
- Package TRANSFER version "TRF-2026.11" is approved by RW-RISK, who is not the author, and is in force from 2026-11-30; each row holds the trigger event, the condition, the target queue code and the row order, and the reason list holds R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic case set RW-2026-000301 to RW-2026-000314, its synthetic queues and members U-21, U-22, U-23, U-24 and U-31, its loads, its cap of 150 and its overflow queues.
- SIT is in place: the Temporal namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-decision`, `rwb-access`, `rwb-document` and `rwb-deviation`, and the topics `rwb.case.events.v1`, `rwb.payment.events.v1`, `rwb.document.events.v1`, `rwb.deviation.events.v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1` with their retry and `.dlt` topics, plus the schema registry.
- The test-only event injector of the harness can publish `rwb.payment.PaymentMissed.v1` on `rwb.payment.events.v1`, because rwb-payment is a wave 2 service and its event is the one trigger of this story with no wave 1 producer; the injector writes the owner's published schema and nothing else.
- The agreed test-only fault switch on the decision-record library of rwb-case can fail the record write for one transfer (TC-E1-021-16-ITG), and its use is agreed with the rwb-case owner.
- No production data is read, copied or connected to; every case number, owner id, queue code, reason code and rule ID used by the run is synthetic.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules R5.7. The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: records the package evidence through `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` for TRANSFER - the version "TRF-2026.11" in force from 2026-11-30 and its SHA-256 - and reads the reason list through `GET /api/recovery/case/v1/admin/lists/{listCode}`, then seeds the synthetic cases RW-2026-000301 to RW-2026-000314, the queues, the members U-21 to U-24 and U-31, the loads, the cap of 150 and the overflow queues of the harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: confirms that package TRANSFER "TRF-2026.11" is the version in force for the business date through the P7 version list, before any trigger is raised, so that a transfer is never asserted against a package that was refused.
3. Harness: raises each of the eight triggers for its case - `rwb.case.CaseStateChanged.v1` for the stage change, `rwb.case.CaseStateChanged.v1` carrying the route-decided fact for the route trigger, the durable timer of CaseWorkflow for the timer trigger, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1`, `rwb.decision.ApprovalRequested.v1`, `rwb.document.DocumentStored.v1` and `rwb.payment.PaymentMissed.v1` - each one on the topic of its owner, with the event ID it later asserts.
4. System: the case router of rwb-case consumes each event once, records the event ID in its inbox in the same transaction as its own change, and calls `signalWithStart` on CaseWorkflow for the case; it calls no service over REST.
5. System: the EvaluateRules activity of the case workflow fetches version "TRF-2026.11" from rwb-decision, verifies its SHA-256, evaluates the trigger on the service's own copy of the package and returns the first matching row in row order, its rule ID and its package version.
6. System: RecordAndApply ends the open assignment, writes the new assignment with reason "TRANSFER" and the rule ID, updates the queue, the team and the owner, writes the local decision record with the rule ID and the package version, and writes the outbox row of `rwb.case.CaseTransferred.v1` in one transaction with the case change.
7. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` for each case and asserts the queue, the team, the owner and the package version on the case record, then reads `GET /api/recovery/case/v1/queues` and `GET /api/recovery/case/v1/queues/{queueId}/cases` for the overflow queue "LIT-BKK-OVF" and reconciles the overflow count with the case reads and with MSG-P3-011.
8. Harness: consumes `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1` and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, reads `GET /api/recovery/decision/v1/decision-log` and measures the elapsed collection of each record against the five-minute target, asserting exactly one record per transfer with its rule ID and package version.
9. Harness: places a legal hold through `POST /api/recovery/case/v1/cases/{caseId}/legal-hold` with the Case record right U, re-raises a transfer trigger for the case, and asserts that the case does not move and that the skip is recorded; then calls the manual transfer endpoint with reason "MANUAL", transfer reason "R03" and target owner U-22, and repeats the call with an identity that holds no Queue and allocation right U.
10. Harness: runs the remaining controls - the repeated event ID, the full target queue, the case that matches no row, the date with no version in force and the forced record failure - records every status, message and count, proves from the call set of the run that no service schema and no Quartz table was read, then writes the evidence report, removes the synthetic fixtures and restores the packages.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two transfers reach the same case in the same second | The first commits; the second is refused on the version check and recorded as rejected | MSG-GEN-004 | AC11, TC-E1-021-03-ITG, TC-E1-021-18-ITG |
| X2 | A manual transfer without a transfer reason | The call is refused with status 422 and nothing changes | MSG-P3-001 | AC7, TC-E1-021-06-ITG |
| X3 | A named target owner at the caseload cap | The call is refused with status 422 and nothing changes | MSG-P3-002 | AC12, TC-E1-021-07-ITG, TC-E1-021-19-ITG |
| X4 | A transfer of a closed case | The call is refused with status 409 | MSG-P3-005 | AC13, TC-E1-021-08-ITG, TC-E1-021-20-ITG |
| X5 | The decision record cannot be written | The transfer is refused and the case keeps its queue and owner; for a rule transfer the event is retried from the topic | MSG-P7-003 | AC14, TC-E1-021-09-ITG, TC-E1-021-16-ITG, TC-E1-021-21-ITG |
| X6 | A rule trigger arrives while a legal hold is in force | No automated transfer; the skip is recorded with the rule and the event ID | None | AC6, TC-E1-021-10-ITG |
| X7 | The same event ID arrives twice | The inbox finds the ID, the second delivery has no effect and the case has one transfer | None | AC2, TC-E1-021-11-ITG |
| X8 | No member of the target queue is below the cap of 150 | The case is placed in the overflow queue of the target queue with no owner and the team manager is told | MSG-P3-011 | AC8, TC-E1-021-12-ITG |
| X9 | A legal hold is placed on a case already on hold | The call is refused with status 409 | MSG-P3-005 | AC15, TC-E1-021-13-ITG, TC-E1-021-22-ITG |
| X10 | No TRANSFER row matches the trigger | No transfer, no assignment and no decision record; the event is recorded as unmatched | None | AC9, TC-E1-021-14-ITG |
| X11 | An identity without the Queue and allocation right U calls the transfer | The call is refused with status 403 and nothing changes | MSG-P4-002 | AC7, TC-E1-021-15-ITG |
| X12 | No TRANSFER version is in force on the business date | The trigger stays in the outbox of rwb-case and is retried when a version is in force; the case does not move and the message names the package | MSG-P3-027 | AC10 |
| X13 | A consumed contract drifts from the published one (path, field, status or event schema), or the package arrives with a checksum that does not match the one held by rwb-decision | The preflight fails and the run stops before any assertion, or the version is refused and the case does not move; the drift or the mismatch is reported against the owning service and no fake is put in its place | None | Preflight, AC3 |

X1 to X11 are the exception paths of the legacy story read on the wave 1 services; X12 is the legacy no-version rule on the target mechanism; X13 is the failure that only appears when the run leaves one service or loses its fixture, so that a timeout or a fixture fault never becomes a pass.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the five integration dependencies and the published contracts of P3, P4, P5, P7 and S8, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the wait window and the report layout are configuration; the trigger rows, the queues, the cap of 150, the reason codes, the package version and the messages are fixed by the legacy story and the package |
| Valuable | Proves across services what no single service story can prove: the eight triggers arriving as facts from their owners, one inbox-deduped router signal, the governed package with its checksum, one ledger record per transfer within five minutes, one CaseTransferred event per move, the hold that stops an automated move and the manual transfer that keeps its contract |
| Estimable | One suite module, one fixture builder with an event injector for the one wave 2 producer, five contract probes, one hold step and one evidence report |
| Small | Fits one sprint with the report; ten scenarios over five services, eight event types and eight consumed operations |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a workflow signal, a ledger record or a queue count |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1, proven across the wave 1 services

  Background:
    Given package TRANSFER version "TRF-2026.11" is in force from 2026-11-30
    Given queue "LIT-BKK-OFF" belongs to team "LIT-BKK" and role RW-LITOFF with method "LOWEST_LOAD" and cap 150
    Given queue "LIT-BKK-OFF" names the overflow queue "LIT-BKK-OVF"
    Given all involved services are deployed in SIT with published contracts
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded
    Given the route-decided fact is asserted in wave 1 as rwb.case.CaseStateChanged.v1 for TRF-002, and the RouteDecided announcement of rwb-valuation is asserted when rwb-valuation lands in wave 3 (GAP-0346)
    Given the operation names of the six consumed rows are not published; the clients and their fakes follow the documented use until the owners publish them (GAP-3076)
    Given the Kafka event names of the P3 and P1 case triggers are not published; the consumer groups are declared and faked on Day 1 and bound when the names are published (GAP-3079)
    Given the deviation triggers TRF-004 and TRF-005 are evaluated in the embedded rule kit of rwb-deviation against the package in force from rwb-decision, and the manual and case-trigger paths stay with rwb-case (GAP-3077)
    Given the rule ID and the package version of a transfer are recorded in the decision record of DP-03 only, and the case-side label stays with rwb-case (GAP-3080)
    Given the eight platform contract rows RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON and the two contract rows RWB-P7-E1073-CON and RWB-P3-E1043-CON are added by pattern application and are not in the split plan, whose build list stays empty (GAP-3075)
    Given the database login of rwb-case is Not specified in the source documents (GAP-0688); the chart takes it by vault secret reference once it is named

  Scenario: AC1 Each of the eight triggers moves the case by rule, one event one transfer (new, D-RCV-60)
    Given the package holds these trigger rows in row order:
      | row     | trigger            | fact or timer that carries it                                        | target queue |
      | TRF-001 | Stage change       | rwb.case.CaseStateChanged.v1                                         | NPA-BKK-CO   |
      | TRF-002 | Route decided      | rwb.case.CaseStateChanged.v1 carrying the route "R4" fact            | LIT-BKK-OFF  |
      | TRF-003 | Timer expired      | the durable timer of CaseWorkflow              | LIT-BKK-OFF  |
      | TRF-004 | Deviation raised   | rwb.deviation.DeviationRaised.v1                                     | DEV-HANDLER  |
      | TRF-005 | Deviation cleared  | rwb.deviation.DeviationCleared.v1                                    | TDR-BKK-CO   |
      | TRF-006 | Approval needed    | rwb.decision.ApprovalRequested.v1                                    | TDR-BKK-APR  |
      | TRF-008 | Document received  | rwb.document.DocumentStored.v1                                       | DIL-BKK-CO   |
      | TRF-009 | Payment missed     | rwb.payment.PaymentMissed.v1                                         | TDR-BKK-CO   |
    Given the eight cases RW-2026-000301 to RW-2026-000308 each meet the condition of one row
    When each row's fact or timer reaches the case router of rwb-case for its case
    Then each case is in its target queue once, with an owner below the cap of 150
    Then the open assignment of the old owner ends and the new assignment carries reason "TRANSFER" and the rule ID of its row
    Then each move leaves exactly one rwb.case.CaseTransferred.v1 and one decision record, one event to one transfer
    Then the status and the clocks of each case are unchanged

  Scenario: AC2 The case router signals the workflow and a repeated event moves the case once (new, D-RCV-60)
    Given the case router of rwb-case consumes rwb.payment.PaymentMissed.v1 and records the event ID in its inbox
    Given rwb.payment.PaymentMissed.v1 with event ID "EVT-88120" moved case RW-2026-000311 to queue "TDR-BKK-CO" by rule "TRF-009"
    When the case router consumes rwb.payment.PaymentMissed.v1 with event ID "EVT-88120" a second time
    Then the router signals CaseWorkflow for case RW-2026-000311 through signalWithStart and makes no REST call to any service
    Then the event ID is found in the inbox and the second delivery has no effect
    Then the case has one transfer for the event and one rwb.case.CaseTransferred.v1
    Then the repeat is counted as an inbox hit and writes no second decision record
    Then every cross-service call of the run is one hop to its owner with the 2 s budget

  Scenario: AC3 The TRANSFER package is fetched with its checksum and evaluated in the case activity (new, D-RCV-60)
    Given version "TRF-2026.11" carries its SHA-256 in rwb-decision
    Given GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions answers the version in force for "TRANSFER"
    When the EvaluateRules activity of rwb-case evaluates a transfer trigger for case RW-2026-000309
    Then the activity fetches version "TRF-2026.11" from rwb-decision and verifies its SHA-256 before use
    Then the rule is evaluated inside the activity on the case service's own copy of the package
    Then no shared rule server and no local rule table is read
    Then the RuleResult carries packageCode "TRANSFER", packageVersion "TRF-2026.11", the rule ID and the outputs of the row
    Then where two rows match the trigger and the condition, the earlier row in row order is the one that fires
    Then a version whose checksum does not match is refused and case RW-2026-000309 keeps its queue and owner

  Scenario: AC4 Every rule transfer leaves one record in the central ledger within five minutes (new, D-RCV-60)
    Given case RW-2026-000301 moves from queue "TDR-BKK-CO" to queue "NPA-BKK-CO" by rule "TRF-001"
    When the transfer commits
    Then the local record is written in the same transaction as the case move
    Then exactly one record exists for case RW-2026-000301 in GET /api/recovery/decision/v1/decision-log within five minutes
    Then that record carries rule ID "TRF-001", package version "TRF-2026.11", the from queue "TDR-BKK-CO" and the to queue "NPA-BKK-CO"
    Then one rwb.decision.DecisionRecorded.v1 carries the same rule ID and package version

  Scenario: AC5 One CaseTransferred event per move, in the envelope and with no personal data (new, D-RCV-60)
    Given case RW-2026-000303 moves from queue "TDR-BKK-CO" to queue "LIT-BKK-OFF" by rule "TRF-002"
    When the transfer commits
    Then exactly one rwb.case.CaseTransferred.v1 leaves on rwb.case.events.v1 with the key caseId
    Then the headers carry the CloudEvents 1.0 type rwb.case.CaseTransferred.v1, the source of the case service and the event ID of the move
    Then the body carries the case number, the from queue, the to queue, the reason code "TRANSFER" and rule ID "TRF-002"
    Then the body carries no personal data field and the schema is accepted by the registry as backward compatible
    Then a second transfer of the same case leaves a second and separate event, never a rewrite of the first

  Scenario: AC6 A legal hold placed through the case endpoint stops an automated transfer that arrives later (new, D-RCV-60)
    Given case RW-2026-000310 is "IN_PROGRESS" in queue "TDR-BKK-CO" with owner U-21
    Given an identity with the Case record right U places a legal hold through POST /api/recovery/case/v1/cases/{caseId}/legal-hold with reason "Court order" and reference "ORD-2026-0412"
    When rwb.payment.PaymentMissed.v1 arrives for the case and matches rule "TRF-009"
    Then the case keeps queue "TDR-BKK-CO" and owner U-21
    Then no rwb.case.CaseTransferred.v1 leaves and no decision record is written for the trigger
    Then the skip is recorded with rule "R-UNI-20", the rule ID "TRF-009" and the event ID of the trigger
    Then lifting the hold through the same endpoint returns the case to the status it paused in

  Scenario: AC7 The manual transfer keeps its contract and the reason list is reference data (new, D-RCV-60)
    Given an identity holds RW-TEAMMGR with the Queue and allocation right U
    When it calls POST /api/recovery/case/v1/cases/RW-2026-000302/transfer with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the call returns status 200 with the assignment of case RW-2026-000302 to U-22, its assigned time, reason "MANUAL" and no rule ID
    Then the reason codes offered to the caller are read from GET /api/recovery/case/v1/admin/lists/{listCode} and hold R01 to R06
    Then the caller right is taken from the authorise contract of rwb-access and never from the request body
    Then the manual call keeps its endpoint, request, response and errors, and it is one hop with the 2 s budget
    Then a call with no transfer reason returns status 422 with MSG-P3-001 and changes nothing
    Then an identity holding RW-CASEOWN and no Queue and allocation right U is refused with status 403 and MSG-P4-002

  Scenario: AC8 A full target queue sends the case to the overflow queue with no owner (new, D-RCV-60)
    Given every member of queue "LIT-BKK-OFF" holds 150 open cases
    When rule "TRF-002" fires for case RW-2026-000312
    Then the case is in queue "LIT-BKK-OVF" with no owner
    Then the case has one open assignment with reason "TRANSFER" and rule ID "TRF-002"
    Then the team manager of team "LIT-BKK" receives MSG-P3-011 with count 1
    Then the cases read in queue "LIT-BKK-OVF" equal the overflow count of the run

  Scenario: AC9 No TRANSFER rule matches, so nothing moves and nothing is logged (new, D-RCV-60)
    Given no TRANSFER row matches rwb.document.DocumentStored.v1 for case RW-2026-000314
    When rwb.document.DocumentStored.v1 arrives for the case
    Then the case keeps its queue, its owner and its assignment
    Then no rwb.case.CaseTransferred.v1 leaves and no assignment is written
    Then the event is recorded as unmatched with its event ID
    Then no decision record exists for the event and no entry reaches the central ledger

  Scenario: AC10 No version in force leaves the trigger in the outbox and moves no case (new, D-RCV-60)
    Given no TRANSFER version is in force on the business date
    When rwb.payment.PaymentMissed.v1 arrives for case RW-2026-000307
    Then the case keeps its queue, its owner and its assignment
    Then the trigger event stays in the outbox of rwb-case and is retried when a version is in force
    Then MSG-P3-027 names the package code "TRANSFER" and the check "package in force"
    Then no decision record exists for the trigger and no case was moved by a default row

  Scenario: AC11 Two transfers reach the same case in the same second and the second is refused (new, D-RCV-60)
    Given case RW-2026-000313 is in queue "TDR-BKK-CO" with owner U-21
    When two transfer triggers for case RW-2026-000313 commit in the same second
    Then the first transfer commits and the case moves once
    Then the second transfer is refused on the version check with MSG-GEN-004
    Then the second transfer is recorded as rejected and writes no decision record

  Scenario: AC12 A named target owner at the caseload cap is refused and nothing changes (new, D-RCV-60)
    Given a named owner of queue "LIT-BKK-OFF" holds 150 open cases
    Given case RW-2026-000304 is in queue "TDR-BKK-CO" with owner U-21
    When an identity with the Queue and allocation right U calls POST /api/recovery/case/v1/cases/RW-2026-000304/transfer with reason code "MANUAL", transfer reason "R03" and that owner as target owner
    Then the call returns status 422 with MSG-P3-002
    Then the case keeps its queue, its owner and its assignment

  Scenario: AC13 A transfer of a closed case is refused with status 409 (new, D-RCV-60)
    Given case RW-2026-000305 is closed in queue "TDR-BKK-CO" with owner U-21
    When an identity with the Queue and allocation right U calls POST /api/recovery/case/v1/cases/RW-2026-000305/transfer with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the call returns status 409 with MSG-P3-005
    Then the case keeps its queue, its owner and its assignment

  Scenario: AC14 A decision record that cannot be written refuses the transfer and the event is retried (new, D-RCV-60)
    Given the decision record write of rwb-case is forced to fail for one case of the run
    When an identity with the Queue and allocation right U calls POST /api/recovery/case/v1/cases/{caseId}/transfer for that case with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the call is refused with MSG-P7-003 and the case keeps its queue and owner
    Then a rule trigger for that case that matches rule "TRF-009" is retried from the topic and the case does not move until the record is written

  Scenario: AC15 A legal hold placed on a case already on hold is refused with status 409 (new, D-RCV-60)
    Given case RW-2026-000310 is on hold through the legal-hold endpoint
    When an identity with the Case record right U places a legal hold through POST /api/recovery/case/v1/cases/RW-2026-000310/legal-hold
    Then the call returns status 409 with MSG-P3-005
    Then the hold already in force is unchanged

  Scenario: AC16 Rules BR10 to BR18 hold on every transfer path (new, D-RCV-60)
    Given the transfer paths of AC1, AC4, AC7 and AC11 have run
    Then a transfer changes the queue, the team and the owner and never the status or the clocks of the case (BR10)
    Then the manual transfer keeps its endpoint, request, response, errors and authorization (BR11)
    Then a trigger with no TRANSFER version in force stays in the outbox and moves no case (BR12)
    Then the TRANSFER version is fetched from rwb-decision, its SHA-256 is verified and it is evaluated inside the activity of rwb-case (BR13)
    Then the decision record commits in the same transaction as the case move and is collected into the central ledger within five minutes (BR14)
    Then each move leaves one rwb.case.CaseTransferred.v1 on rwb.case.events.v1 with key caseId and no personal data (BR15)
    Then the case router signals CaseWorkflow through signalWithStart and makes no REST call to any service (BR16)
    Then every cross-service call of the run is one hop to its owner with the 2 s budget (BR17)
    Then the caller right comes from the authorise contract of rwb-access and an identity without it is refused (BR18)

  Scenario: AC17 A consumed call that fails or does not answer stops the transfer and moves no case (new, D-RCV-60)
    Given the call of rwb-case to rwb-decision for the TRANSFER version fails or does not answer within the 2 s budget
    When the EvaluateRules activity evaluates a transfer trigger for case RW-2026-000309
    Then the activity fails and no decision record is written
    Then the trigger stays in the outbox of rwb-case and the case keeps its queue and owner
    Then the failure is reported against the owning service and no fake is put in its place
```

**Target reading.** Against the monolith, the outbox listener that read the trigger events from the recovery schema is replaced by Kafka events from their owners, each consumed once through the inbox of the rwb-case case router, which signals CaseWorkflow and never calls a service (EV-29, DP-09). The rule model is no longer an in-process evaluator against a local rule table: the TRANSFER version is fetched from rwb-decision, its SHA-256 is verified, and it is evaluated inside the EvaluateRules activity of rwb-case on the service's own copy (DP-04). The decision record is no longer written into a shared log by the transfer call: it commits locally with the case move and is collected into the central ledger of rwb-decision as `rwb.decision.DecisionRecorded.v1` within five minutes (DP-03, ADR-022). The endpoints move under `/api/recovery/case/v1/...` (DP-13), the announcement moves to `rwb.case.events.v1` and the CloudEvents envelope (DP-14), the tables move to `rwb_case` with its own Flyway sequence (DP-01, DP-15), the queue, the cap, the overflow queue and the reason rows come from the reference-data contract of rwb-case (DP-07), the ACE data stays behind rwb-source-data (DP-05), the legacy scheduled timer check gives way to a durable timer inside CaseWorkflow (DP-10), every call is one hop with the 2 s budget (DP-11), and any screen reads behind gateway-bff (DP-19). The authorise contract of rwb-access guards the two endpoints as DP-08, and the caller right is never read from the request. What the sources leave open - the route-decided trigger arriving as a `rwb.case.CaseStateChanged.v1` fact while Arch v5 gives the route to rwb-valuation and announces it as RouteDecided, and the composition of the synthetic fixture set - is recorded as GAP-0346 and ASM-0440, and no value is invented in its place.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case moves by the first TRANSFER row, in row order, whose trigger and condition match; first match follows D-RCV-36 T5 | Package TRANSFER; REQ-CWC-010 |
| BR2 | The eight triggers are stage change, route decided, timer expired, deviation raised, deviation cleared, approval needed, document received and payment missed; each arrives as a fact of the service that owns it, and a manual request is a separate call with a caller-supplied reason | REQ-CWC-010; DP-09; Arch v5 slide 42 |
| BR3 | A manual transfer needs a reason from the list, and the list is reference data read through the contract of rwb-case and never written in code | REQ-WKM-003; DP-07; LOV-TRANSFER-REASON |
| BR4 | A transfer to an owner at the cap of the queue is refused, and the cap is the queue row read through the contract of rwb-case | queue.capacity_cap; REQ-CWC-010 |
| BR5 | A case is in exactly one queue with one open assignment | REQ-CWC-005 |
| BR6 | No automated transfer runs while a legal hold is in force, and the skip is recorded with the rule and the event ID | R-UNI-20 |
| BR7 | Lifting a hold through the case endpoint returns the case to the status it paused in | R-UNI-21 |
| BR8 | An event with the same ID is processed once, through the inbox of the case router in the same transaction as its change | R-UNI-40; DP-09 |
| BR9 | Every rule transfer is recorded with the rule ID and the package version before it takes effect, and every manual transfer with its caller and its reason | REQ-CWC-016; R-UNI-39; D-RCV-36 T5 |
| BR10 | A transfer changes the queue, the team and the owner, and never the status or the clocks of the case | R-UNI-18 |
| BR11 | The manual transfer keeps its endpoint, request, response, errors and authorization; only the base path and the guard library change | REQ-CWC-010; DP-08; DP-13 |
| BR12 | A TRANSFER version not in force leaves the trigger in the outbox and moves no case; it is never a default transfer | R-UNI-41; D-RCV-36 T5 |
| BR13 | The TRANSFER version is fetched from rwb-decision, its SHA-256 is verified, and it is evaluated inside the activity of rwb-case on its own copy of the model, never against a shared rule server and never against a local rule table | DP-04; Drools design slide 15; D-RCV-36 T3, T6 |
| BR14 | The decision record commits in `rwb_case` in the same transaction as the case move and leaves as `rwb.decision.DecisionRecorded.v1`; rwb-decision collects it into the central ledger within five minutes | DP-03; ADR-022; REQ-CWC-016 |
| BR15 | A move leaves one `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1` in the CloudEvents 1.0 envelope, key caseId, with IDs and facts only and no personal data | DP-09; DP-14; ADR-015; Arch v5 slide 42 row 04 |
| BR16 | The case router turns each consumed fact into a Temporal signal on CaseWorkflow through signalWithStart and commands no service over REST | Arch v5 slides 22 and 42 row 29; DP-09 |
| BR17 | Every cross-service call of the run is one hop to the owning service on its own base with the 2 s client budget, and no service is called through another service | ADR-020; DP-11; DP-13 |
| BR18 | The caller right of the two endpoints comes from the authorise contract of rwb-access and is enforced inside rwb-case; an identity without the right is refused and the refusal is the only observable the suite reads | DP-08 (the guard, not a listed pattern of this story) |

### 9. State transitions

The legacy case states of RWB-E1-021, observed through the case contract:

| From | Event | Condition | To |
|---|---|---|---|
| NEW, ASSIGNED, IN_PROGRESS, WAITING_APPROVAL, WAITING_CUSTOMER, WAITING_PARTNER | LEGAL_HOLD_PLACED (R-UNI-20) | Placed through the legal-hold endpoint by an identity with the Case record right U | On hold |
| On hold | LEGAL_HOLD_LIFTED (R-UNI-21) | Lifted through the legal-hold endpoint | One of NEW, ASSIGNED, IN_PROGRESS, WAITING_APPROVAL, WAITING_CUSTOMER, WAITING_PARTNER, the value of status_before_hold |

A rule or manual transfer changes the queue, the team and the owner, not the status.

The states the run observes across the services:

| Item | States |
|---|---|
| Transfer trigger | Received by the router, recorded in the inbox, signalled to CaseWorkflow, evaluated, matched, unmatched, skipped for a legal hold, refused for no version in force |
| Case | NEW, ASSIGNED, IN_PROGRESS, WAITING_APPROVAL, WAITING_CUSTOMER, WAITING_PARTNER, On hold; the case is never written by the suite, and the queue and the owner are read back through the case contract |
| Rule package version | LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |
| Decision record | Recorded locally in `rwb_case`, published as DecisionRecorded, collected in the ledger of rwb-decision |
| Suite run | Not started, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the event injector, the hold step and the evidence report |
| Service owner of rwb-case | Owns the case router, the transfer path, the assignment swap, the two endpoints, the local record and the events |
| Service owner of rwb-decision | Owns the TRANSFER version, the checksum, the version list and the central decision ledger |
| Service owner of rwb-access | Owns the Queue and allocation right U and the Case record right U and their refusals |
| Service owner of rwb-document | Owns the DocumentStored event that fires the document trigger |
| Service owner of rwb-deviation | Owns the DeviationRaised and DeviationCleared events that fire two triggers |
| RW-TEAMMGR team manager | Transfers and reassigns cases in team scope (Queue and allocation U) and receives MSG-P3-011 |
| RW-CAPACITY capacity planner | Transfers cases (Queue and allocation U) |
| RW-LITOFF litigation officer and other roles with the Case record right U | Places and lifts a legal hold on a Legal or court instruction |
| RW-CASEOWN case owner | Reads the case; may not transfer (Queue and allocation R) |
| No role | Reads a service schema directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 contract; written by rwb-case |
| DF-CAS-005 | recovery_case | status | Read through the P3 contract; written by rwb-case |
| DF-CAS-006 | recovery_case | stage_code | Read through the P3 contract; written by rwb-case |
| DF-CAS-008 | recovery_case | route_code | Read through the P3 contract; written by rwb-case |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 contract; written by rwb-case |
| DF-CAS-010 | recovery_case | queue_id | Read through the P3 contract; written by rwb-case |
| DF-CAS-011 | recovery_case | team_code | Read through the P3 contract; written by rwb-case |
| DF-CAS-019 | recovery_case | deviation_open | Read through the P3 contract and asserted from the S8 events; written by rwb-case |
| DF-CAS-020 | recovery_case | legal_hold | Read through the P3 contract, written by the legal-hold endpoint |
| DF-CAS-021 | recovery_case | rule_version (the package version label) | Read through the P3 contract; written by rwb-case |
| DF-CAS-055 | recovery_case | status_before_hold | Read through the P3 contract; written by rwb-case |
| DF-WRK-001 | queue | id | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-002 | queue | queue_code | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-004 | queue | team_code | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-007 | queue | capacity_cap | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-008 | queue | overflow_queue_id | Read through the P3 queue contract; written by rwb-case |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Read through the P3 contract; written by rwb-case |
| DF-WRK-040 | assignment | transfer_reason_code | Read through the P3 contract; written by rwb-case |
| DF-REF-002 | rule_row | rule_id | Read through the P7 package contract |
| DF-REF-003 | rule_row | rule_version (the package version label) | Read through the P7 package contract |
| DF-REF-006 | rule_row | event_code | Read through the P7 package contract |
| DF-REF-007 | rule_row | condition_expr | Not read by the suite |
| DF-REF-052 | rule_row | rule_table | Read through the P7 package contract |
| DF-REF-053 | rule_row | row_order | Read through the P7 package contract |
| DF-REF-054 | rule_row | target_queue_code | Read through the P7 package contract |
| DF-REF-296 to DF-REF-298 | rule_row | package_version_id, drools_rule_name, outputs | Read through the P7 package contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Written locally by rwb-case and in the ledger by rwb-decision; read through the P7 contract |

Field IDs are those of RWB-E1-021 and are copied unchanged. The suite owns no field and no table: every row is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract of section 12.2 or an event of section 12.4. The exact fixture composition, the load of each named owner beyond the members the criteria name, and the case that carries the forced record failure are Not specified in the source documents (GAP-0346; ASM-0440).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation and no service calls it. The names reserved for P2 rwb-integration - `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` - are recorded and unused, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/case/v1/cases/{caseId}/transfer | P3 rwb-case | The manual transfer of AC7 with reason code "MANUAL" and transfer reason "R03", and the refused call of the identity without the Queue and allocation right U |
| POST /api/recovery/case/v1/cases/{caseId}/legal-hold | P3 rwb-case | The hold and the lift of AC6, and the refusal on a case already on hold |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | One case: status, queue, team, owner, legal hold and the TRANSFER package version |
| GET /api/recovery/case/v1/queues | P3 rwb-case | The queue codes, the team, the role, the method, the cap of 150 and the overflow queue, and the queue ids of "LIT-BKK-OFF" and "LIT-BKK-OVF" |
| GET /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | The cases of a queue, for the overflow count of AC8 and the no-owner assertion |
| GET /api/recovery/case/v1/admin/lists/{listCode} | P3 rwb-case | The transfer reason list R01 to R06 of AC7, read as reference data and never written in the suite |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Exactly one record per transfer with rule ID and package version, and the elapsed collection against five minutes |
| GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | P7 rwb-decision | The version in force of TRANSFER, its valid-from date and its SHA-256, for AC3 and AC10 |

Every call is one hop to the owning service on its own base with the 2 s client budget (ADR-020, DP-11, DP-13); the suite calls no service through another service. The caller right of the two case operations is not a call of the suite: it is enforced inside rwb-case through the authorise contract of rwb-access (DP-08), and the suite observes it as the status 403 of AC7. The reference list code of the transfer reasons is Not specified in the source documents (GAP-0346; ASM-0440) and is taken from the P3 reference contract at run time.

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4, and injects one trigger with the test-only injector of 12.8.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite does |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Observed as produced by its owner; carries the stage-change trigger and the route-decided fact that fire TRF-001 and TRF-002 |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Consumed as the input of TRF-004 and asserted on the transfer path of the case |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Consumed as the input of TRF-005 |
| `rwb.decision.ApprovalRequested.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Consumed as the input of TRF-006 |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Consumed as the input of TRF-008, and as the unmatched event of AC9 |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 rwb-payment | Consumed as the input of TRF-009; in the wave 1 environment it is supplied by the test-only injector of 12.8 because rwb-payment is a wave 2 service |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Written by the transferring service, collected by P7 rwb-decision | Observed as produced by its owner; one event per transfer with the rule ID and the package version, matched to the ledger record of AC4 |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | Observed as produced by its owner; exactly one per move, CloudEvents 1.0, key caseId, no personal data |

The envelope is CloudEvents 1.0 and a consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the event and ledger assertions replace the monolith outbox listener and the local decision log of the legacy story.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case | `rwb-case` | Holds the case from entry to closure and receives the transfer trigger as a signal; the suite reads the state the move left through the case contract and takes no part in the order of its steps |
| Case router | Kafka consumer inside rwb-case, the `signalWithStart` path | `rwb-case` | Consumes the trigger event, records the event ID in its inbox and calls `signalWithStart` on CaseWorkflow with the case ID; it signals the workflow and never calls a service over REST (EV-29; Arch v5 slides 22 and 42 row 29) |
| allocate | Activity | `rwb-case` | The placement half of a move: the target queue, the member below the cap and the overflow queue of AC8 |
| transfer | Activity | `rwb-case` | The move half: the version lock, the hold check, the end of the open assignment, the new assignment with reason "TRANSFER" and the rule ID, and the queue, team and owner update |
| rebalance | Activity | `rwb-case` | Registered with the same case workflow release; observed only, and no criterion of this story drives it |
| EvaluateRules | Activity | `rwb-case` | Input the package code, the trigger facts and the business date; fetches the version from rwb-decision, verifies the checksum and returns package code, package version, rule ID and outputs (DP-04) |
| RecordAndApply | Activity | `rwb-case` | Writes the local decision record, the case change, the assignment and the outbox rows in one transaction and fails as one unit (DP-03, DP-09) |

All seven are registered by RWB-P3-E1021-APP on task queue `rwb-case` in namespace `rwb-recovery` (Arch v5 slides 14 and 25; Drools design slide 13). The suite starts no workflow of its own: it observes CaseWorkflow through the case contract, and it raises triggers only as events of their owners, through the timer of the workflow, and through the harness injector of 12.8.

#### 12.6 Schedules

None. JOB-05 Timer check is retired: the timer trigger is a durable timer inside CaseWorkflow and not a scheduled job (Arch v5 slide 44; D-RCV-36 T2 superseded by DP-10). The suite starts no Schedule, moves no Schedule and waits for no Schedule of its own; it lets the durable timer of the workflow fire for TRF-003 and observes the result through the case contract.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises - `recovery_case`, `queue`, `assignment` and the local decision record in `rwb_case`, the package version and the ledger in `rwb_decision` - are listed in section 11 with their owners and are read only through the contracts of 12.2 and the events of 12.4.

#### 12.8 Contract fakes

None for a service contract. No published contract of P3, P4, P5, P7 or S8 is faked, and a run that needs such a fake fails the preflight. The only stubs are external to the nineteen services, or stand in for the one producer that is not in wave 1:

| Stub | Purpose |
|---|---|
| Synthetic case, queue, member and cap fixture (RWB-ITG-W1J01-ITG) | Stands in for the ACE ingestion and the case set that the bank's Airflow and the case service produce, outside the nineteen services |
| Mock Entra sign-in | Gives the run its synthetic test identities, including RW-TEAMMGR with the Queue and allocation right U and RW-CASEOWN with no such right, as the platform demo sign-in does |
| Test-only event injector for `rwb.payment.PaymentMissed.v1` | Stands in for rwb-payment, which is a wave 2 service (Arch v5 slide 41), so that the TRF-009 payment-missed trigger and the repeated event ID of AC2 can be proved on the case side in wave 1; it writes the owner's published schema on `rwb.payment.events.v1` and is switched off as soon as rwb-payment is deployed in the same environment |
| Agreed test-only fault switch on the decision-record library of rwb-case | Stands in for a store that fails one record write (TC-E1-021-16-ITG), so that the retry and the unchanged case are proved; the service contract it sits behind is real. Its exact scope and reset are Not specified in the source documents (GAP-0346; ASM-0440) |

The deviation events are never injected: rwb-deviation is an integration dependency of this story and its two events are produced by the real service (AC1, AC6). A missing producer that is not rwb-payment is a fixture fault of the run, never a reason to add a fake.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 8 | The transfer and the legal-hold calls, the case read, the queue read and the queue-case read, the list read, the decision-log read and the version list; one hop, 2 s (DP-11, DP-13); the right itself is enforced inside rwb-case through rwb-access (DP-08) |
| Kafka | None | 8 event types | `rwb.case.CaseStateChanged.v1`, `rwb.case.CaseTransferred.v1` and `rwb.decision.DecisionRecorded.v1` observed as produced; `rwb.payment.PaymentMissed.v1`, `rwb.document.DocumentStored.v1`, `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1` and `rwb.decision.ApprovalRequested.v1` consumed as trigger inputs; CloudEvents 1.0, key caseId |
| Temporal | None | 1 workflow, 1 consumer path and 5 activities observed | CaseWorkflow, the case router as the `signalWithStart` path, and the allocate, transfer, rebalance, EvaluateRules and RecordAndApply activities on `rwb-case`; the suite starts none of them |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture builder for the synthetic case set, the queues, the members and the caps, a trigger step that raises the eight triggers of their owners plus the harness injector for `rwb.payment.PaymentMissed.v1`, a set of contract probes across P3, P4, P5, P7 and S8, a hold and manual-transfer step, a forced record failure step, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts, run order, one row of evidence per test case and exit code |
| CaseFixtureDriver | Test harness | Seeds the synthetic cases RW-2026-000301 to RW-2026-000314, the queues "TDR-BKK-CO", "TDR-BKK-APR", "LIT-BKK-OFF", "LIT-BKK-OVF", "DIL-BKK-CO", "NPA-BKK-CO" and "DEV-HANDLER", the members U-21 to U-24 and U-31 with their loads, through the W1J01 set |
| TriggerDriver | Test harness | Raises each of the eight triggers of its owner, on the owner's topic or as the durable timer of the workflow, holds the event ID of each for the later assertions, and publishes `rwb.payment.PaymentMissed.v1` on `rwb.payment.events.v1` with the owner's schema through the injector, including the repeated event ID "EVT-88120" of AC2 |
| RouterProbe | Test harness | Asserts the inbox hit of a repeated event and that the router signalled the workflow and called no service |
| PackageProbe | Test harness | Reads the version list with its SHA-256 and valid-from date, asserts the fetch and the checksum of AC3, and the refusal of a mismatched checksum |
| CaseProbe | Test harness | Calls the case, queue and queue-case reads and asserts the queue, team, owner, package version and the overflow count |
| LedgerProbe | Test harness | Consumes DecisionRecorded, reads the decision log and measures each collection against five minutes |
| EventProbe | Test harness | Consumes CaseTransferred and CaseStateChanged and asserts the envelope, the key, one event per move and the absence of a personal data field |
| HoldAndManualStep | Test harness | Places and lifts the legal hold of AC6 through the case endpoint and asserts the stop and the recorded skip; then calls the transfer endpoint of AC7 with "R03" and without a reason, reads the reason list, and repeats the call as RW-CASEOWN for the refusal |
| RecordFaultStep | Test harness | Drives the agreed test-only fault switch for the record write of one transfer |

**Database.** None of its own. The suite writes no service table and no schema object, and it holds no client for a service schema.

**Configuration and reference data**

- The SIT endpoints of P3, P4, P5, P7 and S8, the topic names, the task queues, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic case numbers RW-2026-000301 to RW-2026-000314, the members U-21, U-22, U-23, U-24 and U-31, the loads around the cap, the queues and the overflow queue "LIT-BKK-OVF", the cap of 150 and the business date.
- The package code TRANSFER with the version "TRF-2026.11" and the rows TRF-001 to TRF-009, read through the P7 contracts and never written in the suite code.
- The rule IDs "TRF-001", "TRF-002", "TRF-003", "TRF-004", "TRF-005", "TRF-006", "TRF-008" and "TRF-009", taken from the package answer and never computed by the suite.
- The reasons R01 to R06 through the P3 reference contract (DP-07), the cap of 150 and the overflow queue through the P3 queue contract.
- The 2 s client budget, the poll interval and the five-minute collection target.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C entries of the table belong to the owning APP stories - RWB-P3-E1021-APP for the router, the transfer path, the record and the events, and RWB-P7-E1021-APP for the package registry and the ledger - and this ITG story carries no H, no C and no X of its own. Its I list is the five services whose behaviour the run exercises, and an integration story never becomes a build dependency of another story (Template and Rules R5.4 and R5.7). DP-08 is not one of the listed patterns of this story: it is used as the guard of the two endpoints, and its H and C entries sit on RWB-P4-E1021-APP.

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG, wire it to the SIT endpoints of P3, P4, P5, P7 and S8, the six topics and the task queues, and write the preflight: the five services answer, the topics and their retry and `.dlt` topics exist, the queues are registered in `rwb-recovery`, and version "TRF-2026.11" is in force with its SHA-256.
2. Build CaseFixtureDriver and the W1J01 fixtures for the cases, the seven queues, the members and the cap; hold the full queue "LIT-BKK-OFF" for AC8 and leave it free again for the other criteria.
3. Build TriggerDriver and AC1: the eight triggers of their owners with the timer trigger taken from the durable timer of CaseWorkflow, one case per row, and the assertion that each case moved once with reason "TRANSFER" and its rule ID.
4. Build RouterProbe and AC2: the inbox record, the `signalWithStart` call with no REST call, and the repeated event ID "EVT-88120" that moves the case once and is counted as an inbox hit.
5. Build PackageProbe and AC3: the version list with its SHA-256 and valid-from date, the fetch and the checksum inside the activity, the first row in row order, and the refused version that moves no case.
6. Build LedgerProbe and AC4: exactly one ledger record per transfer with "TRF-001" and "TRF-2026.11", and the elapsed collection measured against five minutes.
7. Build EventProbe and AC5: the CloudEvents envelope, the key caseId, one CaseTransferred per move, the case number, the from and to queue and no personal data field.
8. Build HoldAndManualStep for AC6 and AC7: the hold through the case endpoint that stops a later "TRF-009" trigger with the skip recorded, the manual transfer with "R03", the reason list read from the reference contract, the 422 without a reason and the 403 of RW-CASEOWN.
9. Build the remaining steps: the overflow placement and MSG-P3-011 of AC8, the unmatched event of AC9 with its event ID, the date with no version in force and MSG-P3-027 of AC10, and RecordFaultStep for TC-E1-021-16-ITG.
10. Finish SuiteRunner with the evidence report, the cleanup of the synthetic set and the restored package state; run the whole suite twice to prove that a repeated run adds no transfer and no ledger entry.

**Done when.** The sixteen test cases of section 16 pass on the real services in SIT, the ten new criteria are signed off against the contracts, each of the eight triggers moved its case once with one CaseTransferred event and one ledger record inside five minutes, the hold stopped the later trigger with the skip recorded, the manual transfer kept its response and its errors and refused the identity without the right, the full queue sent the case to "LIT-BKK-OVF" with no owner and MSG-P3-011, the unmatched event and the date with no version in force moved nothing, no service schema and no Quartz table was read, the synthetic set is restored and the package is back in force, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | Manual transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-027 | No TRANSFER version is in force for a rule trigger | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The eight texts are copied unchanged from RWB-E1-021 and this story adds no message ID. For MSG-P3-027 the {check} value is "package in force" and the {table} names the package code only. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built or tested by this story. SCR-02 Case list (list; filtered; empty; loading; error: Not specified in the source documents (CG-ALL-264); no access: Not specified in the source documents (CG-ALL-264)) and SCR-03 Case record (read only; on hold; loading; empty: Not specified in the source documents (CG-ALL-265); error: Not specified in the source documents (CG-ALL-265); no access: Not specified in the source documents (CG-ALL-265)) show the new queue, the new owner and the hold banner after a move, and the suite reads the same facts through `GET /api/recovery/case/v1/cases/{caseId}` behind the gateway-bff composite route (DP-19). The transfer screen SCR-05 and the queue history come in Epic 2 (RWB-E2-012, RWB-E2-016) and are out of scope; its empty, loading, error and no access states: Not specified in the source documents (CG-ALL-266). The team manager receives MSG-P3-011 after an overflow placement, which the suite asserts on the message and on the queue read.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-15-ITG | Access, BR18 | Integration | RW-CASEOWN calls POST /cases/{caseId}/transfer and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-01-ITG | AC1, BR1, BR10 | Integration | Case in TDR-BKK-CO, route R4 approved; package TRANSFER "TRF-2026.11"; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-02-ITG | AC2, BR3, BR11 | Integration | Manual transfer with R03; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-03-ITG | AC11, BR5 | Integration | Two transfers on record version 7; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-04-ITG | AC4, BR2 | Integration | Eight TRANSFER rules; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-05-ITG | AC5, BR7 | Integration | Reassign, place hold, lift hold; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-06-ITG | AC6, BR3 | Integration | No transfer reason; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-07-ITG | AC7, BR4 | Integration | Owner U-24 at 150; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-08-ITG | AC13 | Integration | Closed case; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-09-ITG | AC14, BR9 | Integration | Decision record store down for a manual call; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-10-ITG | AC6, BR6 | Integration | legal_hold = true and the timer trigger of TRF-003; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-11-ITG | AC2, BR8, BR16 | Integration | Event EVT-88120 twice; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-12-ITG | AC8 | Integration | Every member of LIT-BKK-OFF at 150; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-13-ITG | AC15 | Integration | Hold on a case on hold; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-14-ITG | AC9, BR1 | Integration | DocumentStored with no rule; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-16-ITG | Principle 5 | NFR | Decision record write forced to fail for a rule transfer; event retried, case unchanged; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-17-ITG | Contract of section 12 (ADR-020, DP-13), BR17 | Contract | Preflight of the operations, events and activities of section 12 against the published contracts; drift stops the run before any assertion |
| TC-E1-021-18-ITG | AC11, BR5 | Integration | Two transfers of RW-2026-000313 in the same second; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-19-ITG | AC12, BR4 | Integration | Owner of LIT-BKK-OFF at 150 named as target; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-20-ITG | AC13 | Integration | Closed case RW-2026-000305; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-21-ITG | AC14, BR9 | Integration | Decision record write forced to fail for a manual call; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-22-ITG | AC15 | Integration | Hold on a case on hold; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-23-ITG | AC10, BR12 | Integration | No TRANSFER version in force on the business date; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-24-ITG | AC3, BR13 | Integration | TRANSFER version fetched, checksum verified and evaluated in the activity; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-25-ITG | AC4, BR14 | Integration | Rule transfer of RW-2026-000301 and its ledger record; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-26-ITG | AC5, BR15 | Integration | Move of RW-2026-000303 and its CaseTransferred event; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-27-ITG | AC16, BR10 to BR18 | Integration | Rules checked on the transfer paths of AC1, AC4, AC7 and AC11; end-to-end: real services on the wave 1 contracts |
| TC-E1-021-28-ITG | AC17, BR17 | Integration | rwb-decision call fails or does not answer for RW-2026-000309; end-to-end: real services on the wave 1 contracts |

This story owns no legacy criterion, so every one of the sixteen is regression evidence for the component copy RWB-P3-E1021-APP, which owns the legacy criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed. The Covers column names the legacy criterion each copy exercises, not the scenario number of section 7; the mapping of the new criteria to the copies is in section 18. The Level column follows Template and Rules R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, and the legacy Resilience level of TC-E1-021-16 becomes NFR. The new criteria of section 7 are what this story signs off. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case number, owner id, queue, member, cap and reason code, and no production data is read, copied or connected to; the suite refuses to start against an environment that is not SIT.
- No personal data in events, logs, workflow history, fixtures or the report: case numbers, queue codes, owner ids, rule IDs, package versions and business dates only.
- No cross-service table read: every fact is read through a contract of 12.2 or an event of 12.4, the ACE views stay behind rwb-source-data (DP-01, DP-05), and the suite ships with no client for a service schema and none for the Quartz tables.
- No business value in the test code: the cap of 150, the queue codes, the overflow queue, the reason codes and the trigger rows are the package, the queues and the lists in force, read through the P3 and P7 contracts (DP-04, DP-07).
- One evaluator and one copy: TRANSFER is evaluated only inside the EvaluateRules activity of the owning service on a checksum-verified copy of the package, and the suite never reads a workbook, a rule row or a local rule table directly.
- One observable right: the caller right is enforced inside rwb-case through the authorise contract of rwb-access (DP-08), the suite never passes a right in a request, and a 403 is never retried into a pass.
- CloudEvents 1.0 with IDs and facts only on every asserted event, one CaseTransferred per move, and the consumer inbox as the only dedupe.
- One hop and a 2 s budget on every REST call, and a timeout is never retried into a pass (ADR-020, DP-11).
- Clean-up in the same run: the synthetic cases, the held queue load, the injector switch, the fault switch, the started workflows and any package state a criterion touched are removed or restored, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers and manual request with a reason code | The case router and `signalWithStart`, the transfer path with the TRANSFER rows, `POST /api/recovery/case/v1/cases/{caseId}/transfer`, `POST /api/recovery/case/v1/cases/{caseId}/legal-hold` | TC-E1-021-01-ITG, TC-E1-021-02-ITG, TC-E1-021-03-ITG, TC-E1-021-04-ITG, TC-E1-021-05-ITG, TC-E1-021-10-ITG, TC-E1-021-15-ITG |
| REQ-CWC-016 | Every transfer logged with the rule ID and the rule version | `rwb.decision.DecisionRecorded.v1`, `GET /api/recovery/decision/v1/decision-log`, the local record in `rwb_case`, MSG-P7-003 | TC-E1-021-01-ITG, TC-E1-021-02-ITG, TC-E1-021-03-ITG, TC-E1-021-04-ITG, TC-E1-021-09-ITG, TC-E1-021-16-ITG |
| REQ-WKM-003 | A manual transfer or reassignment only with a reason code from the agreed list | `GET /api/recovery/case/v1/admin/lists/{listCode}`, the transfer request with `transferReasonCode`, MSG-P3-001 | TC-E1-021-02-ITG, TC-E1-021-06-ITG, TC-E1-021-15-ITG |
| REQ-CWC-005 | The case state model, one state at a time, with the legal-hold status | `POST /api/recovery/case/v1/cases/{caseId}/legal-hold`, the legal-hold and `status_before_hold` fields of the case read, MSG-P3-005 | TC-E1-021-05-ITG, TC-E1-021-08-ITG, TC-E1-021-13-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `rwb.case.CaseTransferred.v1` and `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1`, the inbox of the case router, schema-registry versioning | TC-E1-021-04-ITG, TC-E1-021-11-ITG |
| ADR-016 | Reusable Temporal layer; durable timers and Schedules replace Quartz | The `signalWithStart` path of the case router, the durable timer of TRF-003, and the retirement of JOB-05 | TC-E1-021-04-ITG, TC-E1-021-10-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eight REST operations of 12.2 and the preflight contract test | TC-E1-021-15-ITG, TC-E1-021-02-ITG |
| ADR-022 | Local decision record plus central ledger | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, the decision-log read, the five-minute target | TC-E1-021-01-ITG, TC-E1-021-09-ITG, TC-E1-021-16-ITG |
| DP-03 | Decision record library and the shared topic | RecordAndApply writing the record, the case move, the assignment and the outbox row in one transaction | TC-E1-021-09-ITG, TC-E1-021-16-ITG |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The "TRF-2026.11" version, its checksum and the version list of 12.2 | TC-E1-021-01-ITG, TC-E1-021-04-ITG |
| DP-07 | Reference data contract of rwb-case | The queue rows of `GET /api/recovery/case/v1/queues` and the reason list of `GET /api/recovery/case/v1/admin/lists/{listCode}` | TC-E1-021-02-ITG, TC-E1-021-07-ITG, TC-E1-021-12-ITG |
| DP-09 | Outbox and inbox with CloudEvents | The eight events of 12.4 and the inbox dedupe of the case router | TC-E1-021-04-ITG, TC-E1-021-11-ITG |
| DP-10 | Quartz replaced by a Temporal step, timer or Schedule | The durable timer of TRF-003 and the retirement of JOB-05 | TC-E1-021-10-ITG |
| DP-13 | The service base path of the owner | The eight `/api/recovery/case/v1` and `/api/recovery/decision/v1` operations of 12.2 | TC-E1-021-02-ITG, TC-E1-021-15-ITG |
| DP-14 | Topic naming of the owner | `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.decision.events.v1`, `rwb.document.events.v1`, `rwb.deviation.events.v1`, `rwb.payment.events.v1` | TC-E1-021-04-ITG, TC-E1-021-11-ITG |
| RWB-E1-021 (legacy story) | Transfer rules and engine v1: no criterion owned here | The eight REST operations, the eight events, the workflow, the router and the five activities of section 12 | The sixteen regression copies of section 16, with AC1 to AC10 of section 7 signed off |
| RWB-P3-E1021-APP (component copy) | The transfer behaviour in rwb-case, owning legacy AC1 to AC14 and the Access test | The case router, the transfer path, the two endpoints, the overflow placement, the local record and the events | The sixteen regression copies of section 16 |

### 19. Out of scope

- The five application builds this run depends on: RWB-P3-E1021-APP, RWB-P7-E1021-APP, RWB-S8-E1021-APP, RWB-P5-E1021-APP and RWB-P4-E1021-APP, with their unit and component tests.
- The contract, database, operations and infrastructure stories of the legacy key RWB-E1-021 and of the five services.
- The transfer screen and the queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap, and the escalation of a breached timer without moving the case (RWB-E1-028).
- The route decision itself (Epic 4, rwb-valuation) and the RouteDecided event of S1; the route-decided trigger is read here as the fact rwb-case commits, and the conflict is carried as GAP-0346.
- Loading, validating, approving and rolling back the TRANSFER package as a process (RWB-E1-073); only the version in force and its checksum are read here.
- The build of the harness RWB-ITG-W1J01-ITG itself, which is a precondition here and not a deliverable.
- The non-functional epic RWB-ITG-NFR and load or performance testing of the transfer path; the 150-case loads of the cap criteria are synthetic rows, not a volume test.
- The data lake, which is removed from the target architecture (DP-17), and any screen, agent run or report of the transfer history.
