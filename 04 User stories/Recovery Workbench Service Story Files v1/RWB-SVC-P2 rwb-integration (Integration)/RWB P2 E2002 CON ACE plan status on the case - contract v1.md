# RWB-P2-E2002-CON ACE plan status on the case - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for rwb-integration. This document fixes the plan-status contract baseline: the resource, the operation, the error envelope, the ACE common module interface stub, the consumed shapes of rwb-case, rwb-access and rwb-decision, the configuration section and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-integration side of the ACE plan status fixed as a contract: the `GET /cases/{caseId}/plan-status` resource with its fields, rights, errors and read-only rule; the published `RestructurePlanQuery` interface with its batch and timeout budget; the consumed shapes of rwb-case, rwb-access and rwb-decision; the fakes for those three services and the ACE stub; and the statement of what the case side owns**, so that **the app story and the operations story of this key, the plan-status step of `RWB-P3-E2002-APP` and the integration harness build on Day 1 against one agreed, testable shape**.

The legacy story put the plan read, the stored status, the rule evaluation, the route move, the task, the timer and the decision log entry in one module, and it published `GET` on `/cases/{caseId}/plan-status` with `RestructurePlanQuery.statusFor(List<String> accountNos)` beside `CasePlanStatus.update` and `CaseEvents.raise`. Under D-RCV-60 the journey is cut in two: rwb-case holds the case of record, the stored status, the rules, the route state, the task, the timer and the record; rwb-integration holds the call to the ACE common module and the live answer. This document fixes the seam.

Three facts make the seam worth a contract of its own. The ACE common module is a published module interface and not a view, so the call has to be bounded by a batch size and a timeout that both sides can name (INT-34; ADR-010; DP-05). The resource has two providers in the target — the live answer here and the stored answer of rwb-case — so the flag that separates them and the message that says the value is old have to be fixed once (DP-19). And the daily step is rwb-case's, which means the batching, the answer and the refusal classes are the only things this service owes the caller (DP-10, DP-11).

The Ownership Map keeps `GET /cases/{caseId}/plan-status` with P2 and TSD P2 v3 keeps it at API-P2-010, so this document re-bases it on `/api/recovery/integration/v1` under DP-13 and records the reconciliation rather than leaving it to the app story.

### 2. Business rationale

Contract-first REST, one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020), and a plan status is read on a screen, in a nightly step and in an integration harness. All three work only if the resource, its flag, its refusals and its budget are written down once. The contract is also where the two-provider rule is made safe: a caller must be able to tell a value read from ACE now from a value the case holds from an earlier date, or the measure of the legacy story — no case with a live plan is treated as if it had none — cannot be evidenced at the seam.

The contract fixes four things no single source fixes together. The resource shape and the meaning of `live` and `messageCode`, because the API Specification carries the fields and the legacy story carries the rule, and neither says who fills the message when the live read fails. The ACE interface call and its budget, because the legacy story publishes the signature and assumes the batching and the timeout while the technical specification reads a view instead. The error classes, because the case side must know which refusal means "keep the stored value" and which means "this caller may not see the case". And the fakes, because four teams build before the other services exist.

The contract states what it does not own as plainly as what it does: the stored status, the compare, the route move, the decision record, the task and the timer are rwb-case's; the rights and the scope data are rwb-access's; the rule package, its version and the catalog rows are rwb-decision's; the ACE plan itself is ACE's under DL14. This service names them and calls them, and writes none of them.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the task queue and the topic names follow the platform rule (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the RFC 9457 problem-details body and the platform message catalogue are the platform baseline; this document narrows them where it must and says so.
- The integration base of RWB-P2-E1007-APP and RWB-P2-E2001-APP is available, with its controller conventions, its problem-response mapping, its contract-client and breaker handling and its health surface.
- The embedded Drools kit contract (RWB-PLT-E1072-CON), the decision-record library contract (RWB-PLT-E1027-CON), the workflow kit (RWB-PLT-E1071-CON), the parameter and reference-data client libraries (RWB-PLT-E1042-CON, RWB-PLT-E1043-CON), the outbox and inbox library (RWB-PLT-TE006-CON), the migration conventions (RWB-PLT-E1044-CON) and the gateway-bff composite route (RWB-PLT-N001-CON) are available. This document consumes them and defines none of them.
- The rwb-case contract baseline publishes the case read by reference with its account numbers, the reference-data read of RWB-P3-E1043-CON and the parameters read of RWB-P3-E1042-CON; the rwb-access contract publishes the authorise call. Where a contract is not yet published, this document's shape and its fake stand in.
- The ACE common module publishes `RestructurePlanQuery` in SIT and UAT (INT-34; DL14).
- The plan status list LOV-PLAN-STATUS holds CREATED, APPROVED, BOOKED and BROKEN (RW-COE), and the two settings `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 are the assumed values of the key (DL11).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the provided operation: `GET /cases/{caseId}/plan-status` on `/api/recovery/integration/v1`, with its path, right, answer, errors, read-only rule and the meaning of `live` and `messageCode`.
2. Publish the consumed shapes: the case read by reference, the reference-data read of LOV-PLAN-STATUS, the parameters read of the two settings and the authorise call, each with the 2 s client budget.
3. Publish the ACE interface contract: the `RestructurePlanQuery.statusFor` signature, the batch size, the per-call timeout, the breaker, the retry and the mapping of a plan to an account.
4. State the split between the live answer here and the stored answer, the compare, the route move and the record of rwb-case, and reconcile the ownership and specification conflicts.
5. Publish the status validation contract: the list, its version, the known-code answer and the unknown-code answer.
6. Publish the configuration section: LOV-PLAN-STATUS, the two settings, the flag and the fact that no table is added.
7. Publish the error mapping of the seven messages over the operation.
8. Build the fakes: rwb-case, its reference data and its parameters; rwb-access; rwb-decision; the ACE common module stub; and the composite route stub.
9. Add the contract tests: the operation shape, the consumed shapes, the interface contract, the split note, the configuration section and the drift test between each fake and this document; tag the baseline and hand it to the app and operations stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The operation, a consumed shape or a field contradicts this document | The contract test fails and the merge is blocked | None | AC1, AC2, AC3 |
| X2 | A fake drifts from this document, or answers a shape this document does not declare | The drift test fails and the merge is blocked | None | AC5 |
| X3 | A document declares the stored plan status, the route move, the rule evaluation or the record as this service's | The review refuses the document, because those are rwb-case's and rwb-decision's | None | AC6 |
| X4 | The operation is declared with a write, an event, a Schedule or a second provider of the stored answer | The review refuses it: a read writes nothing, publishes nothing and creates no Schedule, and the stored answer is rwb-case's | None | AC1, AC6 |
| X5 | The ACE plan is declared as a view read or a table read, or `rwb_integration` is given a grant on `recovery` | The review refuses it: the plan comes through the published interface (INT-34), and only rwb-source-data reads the views | None | AC2 |
| X6 | A field-level detail of a consumed shape or of the interface answer is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC2, AC5 |
| X7 | The caller holds no Case record R, or the case is outside the scope | The refusal is fixed with its status and its message before any ACE call is declared | MSG-P4-002, MSG-P4-003 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the ACE interface and the published rwb-case and rwb-access shapes, and fakes them |
| Negotiable | The field-level detail of the consumed reads is settled with their owners; the resource, the flag rule, the batch and the timeout are fixed by this realignment |
| Valuable | Unblocks the app story, the operations story, the plan-status step of RWB-P3-E2002-APP and the integration harness of the key |
| Estimable | One operation, four consumed reads, one outside interface, five fakes and one configuration section |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against an artefact — the schema, the fake, the table section — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Plan status contract baseline for rwb-integration

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the integration base, its problem-response mapping and its contract-client conventions are in force
    Given the plan status list LOV-PLAN-STATUS holds CREATED, APPROVED, BOOKED and BROKEN

  Scenario: AC1 The plan-status resource and the operation are fixed (new, D-RCV-60)
    Given the contract tables of section 12
    When the provided operation is reviewed
    Then GET /cases/{caseId}/plan-status is documented on the base /api/recovery/integration/v1 with the answer planRef, accountNo, status, statusDate, live and messageCode
    Then the document states that live is true on every 200 answer that read ACE, that live false without a plan is the flag-off answer, and that live false with MSG-P2-008 is the stored answer of rwb-case
    Then the document states that a read writes no row, publishes no event, creates no Schedule and stores no cache of the answer
    Then the operation declares Case record R with the scope applied and the 401, 403, 404 and 503 answers with their message IDs
    Then the monolith base of the legacy story appears nowhere in the document

  Scenario: AC2 The ACE interface and the consumed reads are published with one budget (new, D-RCV-60)
    Given the contract tables of section 12.2 and the interface section of section 13
    When the consumed calls are reviewed
    Then RestructurePlanQuery.statusFor is documented with the account list input, the planRef, accountNo, status and statusDate answer, batches of 500 and a per-call budget of 2000 ms
    Then the interface is documented as a published module interface of the ACE common module and not as a v_ace_* view and not as a table
    Then the case read, the LOV-PLAN-STATUS read, the two-setting read and the authorise call are each described with method, path or operation name, owner, use and the 2 s budget
    Then each one is attributed to rwb-case or rwb-access and none is declared as provided by rwb-integration
    Then the document states that rwb_integration holds no grant on recovery and no foreign key into another schema

  Scenario: AC3 The status validation and the error envelope are fixed (new, D-RCV-60)
    Given the contract tables of section 12.1 and the validation table of section 14
    When the validation and the errors are reviewed
    Then a status code in LOV-PLAN-STATUS is answered unchanged and a code outside it is answered unchanged and never mapped, defaulted or labelled
    Then the list is read with the version in force through the rwb-case reference-data contract and no status code appears in code
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002, 404 answers MSG-P4-003 and 503 answers MSG-GEN-006 naming its source
    Then a no-plan answer is documented as a 200 answer with the plan fields absent, and not as an error
    Then MSG-P2-008, MSG-P7-003 and MSG-P3-027 are named as the case side's and are not produced by this operation

  Scenario: AC4 The consumed read of the case and the access check are fixed (new, D-RCV-60)
    Given the contract table of section 12.2 and the fakes of section 12.8
    When the account resolution and the guard are reviewed
    Then the case is read by reference only, and its account numbers are the join key of DL21
    Then the Case record right and the scope are checked before any ACE call, with the refusal statuses of AC3
    Then the fakes answer an unknown case, a case with no account, a case outside the scope and a role without the right
    Then the document states that no case row, no account row and no plan row is copied into rwb_integration

  Scenario: AC5 The five fakes answer every declared shape (new, D-RCV-60)
    Given the fakes of section 12.8 and the drift test of the pipeline
    When each fake is compared with this document
    Then the rwb-case fakes answer the case read, the reference-data read and the parameters read with the shapes and errors of this document
    Then the rwb-access fake answers the authorise call granted, refused and out of scope
    Then the rwb-decision fake answers the evaluation and record calls this key drives, without being consumed by this service
    Then the ACE common module stub answers a known plan, no plan, an unknown code and an answer beyond the budget, and more than 500 accounts for the batch boundary
    Then the composite route stub answers the merged plan section and the stored fallback

  Scenario: AC6 The split is stated and the ownership conflicts are reconciled (new, D-RCV-60)
    Given the contract of this story, the Ownership Map row of GET /cases/{caseId}/plan-status and the TSD entry API-P2-010
    When the split is reviewed
    Then the document states that rwb-integration answers the live plan status and that rwb-case stores plan_ref, plan_status and plan_status_as_of, compares, moves the route state, raises the task, holds the timer and writes the decision record
    Then the document states that the daily plan-status step of JOB-02 and its activity are rwb-case's and that no P2 Schedule exists
    Then the document records that the technical specification reads v_ace_plan with a fallback while ADR-010 and DP-05 keep the views with rwb-source-data, and cites the gap row of the conflict
    Then the document records that the Ownership Map and the technical specification keep the operation with P2 and that this document re-bases it on the integration base
    Then the configuration section states that no table, no column and no migration is added
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan status is read from the ACE common module through its published interface, never from ACE tables and never from a `recovery.v_ace_*` view | INT-34; DL14; ADR-010; DP-05 |
| BR2 | The account number is the join between the case and the ACE plan | DL21 |
| BR3 | Plan status values are the rows of LOV-PLAN-STATUS with the version in force; any other code is held as an exception and never interpreted | LOV-PLAN-STATUS; DP-07 |
| BR4 | `live` is true on every 200 answer that read ACE, because such an answer means ACE answered; the flag-off answer is 200 with `live` false and no plan, and `live` false with MSG-P2-008 is the stored answer of rwb-case | Legacy plan-status resource; RWB-P3-E2002-APP |
| BR5 | A read writes nothing: no row, no outbox entry, no decision record, no cached answer | Legacy guardrail; DP-01 |
| BR6 | One base, one queue and one topic per service: this contract declares `/api/recovery/integration/v1`, `rwb-integration` and `rwb.integration.events.v1`, consumes the other bases and never declares another service's path as provided | DP-13; DP-14; Arch v5 slide 41 |
| BR7 | The ACE interface is bounded: batches of 500 account numbers, 2000 ms per call, a breaker per downstream and one retry of a read with jitter | Legacy section 13 (assumed; DL11); DP-11 |
| BR8 | The batch size and the timeout are data, read through the rwb-case parameters contract, and never code | DP-06; FSD P2 Integration v3 BR-P2-007 |
| BR9 | The Case record R right and the case scope are checked before any ACE call, and a refusal returns no data and writes nothing | Legacy AC8; DP-11 |
| BR10 | No table, no column and no index is added by this key, so no migration is added; the library objects exist from the service baseline | DP-15; Ownership Map |
| BR11 | The response shape keeps the legacy PlanStatus names and adds `accountNo`, because the ACE answer carries the account and the case side joins on it | Legacy API-P2-010; API Specification v4 PlanStatus |
| BR12 | A consumed field, path or error that no source fixes is written with the placeholder and carried in one gap row plus its assumption rows, never invented | Template and Rules §R9 |
| BR13 | No personal data appears in an answer, an example or a fake: the case reference, the plan reference, the status code, the flag and the counters only | Arch v5 slide 42; Template and Rules §R7.2 s17 |
| BR14 | The legacy values of the key are carried unchanged: the plan reference "TDR-SYN-0310", the account "A-0310", the statuses CREATED, APPROVED, BOOKED and BROKEN, the code "SUSPENDED" as the negative case, and the two settings 500 and 2000 | Legacy section 7 and section 13 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the interface, the consumed reads, the split and the configuration are described | In review |
| In review | Consumer sign-off | The app story, the operations story, the case plan-status step and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field or an error is added without removing one | Baselined |
| Baselined | Breaking change of a consumed shape | rwb-case or rwb-access removes, renames or retypes an element this contract consumes | In review, with the owner of that read |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new ACE interface version | The ACE team publishes a changed `RestructurePlanQuery` | In review, with the ACE team |

These are states of the document, not of a case: the case status and the route state do not move here. The route states of the legacy story are `recovery_case.route_state` writes of rwb-case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns the document, the operation shape, the interface contract and the five fakes; tags the baseline |
| Solution architect | Approves a breaking change of a consumed contract, the reconciliation of the two-provider resource and the interface-versus-view conflict |
| The rwb-case owner | Owns the case read, the reference-data read and the parameters read; signs off the shapes taken from its contract |
| The rwb-access owner | Owns the authorise contract and signs off its consumption |
| The rwb-decision owner | Owns the rule package, the catalog and the ledger; signs off the fake answers this key drives |
| The ACE team | Owns `RestructurePlanQuery` and signs off the interface contract, its batch and its budget |
| Platform workflow kit owner | Owns the task queue, the namespace and the conventions this document reuses |
| Data steward | Confirms that no personal data field and no account number is declared in an answer or a fake |

The deployment identity that calls the ACE interface and the consumed reads is Not specified in the source documents (GAP-0655; ASM-1105); the document names it "the rwb-integration workload identity (DP-02)" and leaves the name to RWB-P2-E2002-OPS.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Plan-status answer | planRef, accountNo, status, statusDate, live, messageCode |
| Case read | case reference, account numbers, owner, queue, closed flag |
| Reference read | LOV-PLAN-STATUS rows and the version in force |
| Parameter read | `rwb.ace.plan.batch-size`, `rwb.ace.plan.timeout-ms` and the version in force |
| Authorise answer | the Case record right and the case in or out of scope |
| ACE interface answer | planRef, accountNo, status, statusDate per plan returned |
| Interface budget | 500 account numbers per call, 2000 ms per call, breaker per downstream, one retry with jitter |

The field-level detail of the case read, the reference read, the parameter read, the authorise answer and the remaining interface elements — property types, lengths, required flags, query parameters and null rules — is Not specified in the source documents (GAP-0655; ASM-1106); this document fixes the element names above and leaves the types to the review with each owner. The values of the status list and of the two settings are the legacy values of this key and are carried unchanged (BR14).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/plan-status` | Answer planRef, accountNo, status, statusDate, live (true when the answer read ACE, false on the flag-off answer) and messageCode (empty); 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-GEN-006) | Case record R, scope applied | Read only: the same ACE state answers the same values, and nothing is written |

The operation is the one the Ownership Map keeps with P2 and the one TSD P2 v3 publishes as API-P2-010, re-based on the integration base under DP-13. Its JSON field names are the legacy PlanStatus names; `accountNo` is added because the ACE answer carries the account and the case side joins on it, and the Technical Specification and the API Specification differ on whether the field is present (GAP-0655; ASM-1106).

`live` and `messageCode` are the two fields with a rule rather than a type. `live` is true when the value was read from ACE now, which is every 200 answer that read ACE, and false on the flag-off answer, which read nothing and carries no plan; `live` false with MSG-P2-008 and the stored date is the answer of rwb-case on its own base, and the composite route chooses between them (DP-19). `messageCode` is therefore empty on every answer of this service: this service holds no stored value to date and has no older date to name (GAP-0655; ASM-1107).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path or operation | Owner | Contracted use |
|---|---|---|---|
| GET | the case read of the rwb-case contract, by case reference | P3 rwb-case | The account numbers of the case, the owner, the queue and the scope facts |
| GET | the reference-data read of RWB-P3-E1043-CON | P3 rwb-case | LOV-PLAN-STATUS with the version in force |
| GET | the parameters read of RWB-P3-E1042-CON | P3 rwb-case | `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms` with the version in force |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record right and the case scope, cached per session |
| Call | `RestructurePlanQuery.statusFor(List<String> accountNos)` | ACE team, the ACE common module | The plans of the account numbers, in batches of 500 within a 2000 ms budget per call |

The reference-data and parameters reads are named by DP-07 and DP-06 and their paths are taken from the P3 contract baseline when it is published; the case read and the authorise call are the case baseline and the access guard. The paths and element names of the case read, of the authorise answer and of the two reference answers are Not specified in the source documents (GAP-0655; ASM-1106).

The ACE interface is a published module interface: it is not on a `/api/recovery/...` base, it is not reached through gateway-bff, and `rwb_integration` holds no grant on `recovery`. The Technical Specification's `v_ace_plan` read with a fallback to the case columns is the conflict this contract records and does not follow (GAP-0655; ASM-1108).

#### 12.3 Events published

None. This contract declares no event type and publishes on no topic of its own. `rwb.integration.events.v1` carries FileDelivered and FileFailed, which belong to the outbound-file stories of this service, and `rwb.decision-record.v1` carries DecisionRecorded from the services that take a decision — here, rwb-case on each route move (DP-03, DP-09). A read has no outbox row.

#### 12.4 Events consumed

None. Every call of this story is call-driven: the operation is called by rwb-case's plan-status activity and by the composite route, and the service subscribes to no topic for this key, holds no inbox row and keeps no projection.

#### 12.5 Workflows and activities

None. This contract declares no workflow and no activity: the daily `PlanStatusStep` and its `readPlanStatus` activity are rwb-case's, on its own task queue, and this service answers a synchronous read on the request path with the batching and the budget inside the request. The integration harness lists a plan-status step on `rwb-integration`; that row conflicts with the sibling story and with the job map and is carried in the gap row (GAP-0655; ASM-1108).

#### 12.6 Schedules

None. No Schedule is declared by this contract or created by this key: the legacy plan-status step of JOB-02 runs inside the event-started DailyCaseRun of rwb-case, and a second daily run over the same cases fails the review (Arch v5 slide 44; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| interface_config | rwb_integration | P2 (Ownership Map; Arch v5 slide 41) | None: the ACE endpoint is a deployment value, not an interface row |
| outbound_item | rwb_integration | P2 (Ownership Map; Arch v5 slide 41) | None: this key builds and sends no file |
| job_catalog | rwb_integration | P2 (Ownership Map; TSD P2 v3 T3.1) | None: no job is catalogued, because no P2 Schedule exists |
| outbox_event, processed_event, outbox_delivery, idempotency_key | rwb_integration | PLT library, created in `rwb_integration` (DP-09) | Present from the service baseline and unused by this key |

No case table, no account table, no reference table, no parameter table and no rule table is owned, read or copied: the case, the reference rows and the parameters come through their owners' contracts, and the plan comes through the ACE interface (DP-01, BR5). The key adds no table, no column and no index, so it adds no migration (DP-15).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock — case | Case "RW-2026-000310" with account "A-0310", owner and queue filled; a case with no account; an unknown case answered 404; a case outside an Own scope answered 404 | App story, contract tests |
| rwb-case WireMock — reference data | LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN and its version label; one version without "SUSPENDED"; one answer beyond 2 s | App story, contract tests |
| rwb-case WireMock — parameters | `rwb.ace.plan.batch-size` 500 and `rwb.ace.plan.timeout-ms` 2000 with their versions; one answer beyond 2 s | App story, contract tests |
| rwb-access WireMock | The authorise call granted with Case record R in scope, refused for RW-REFADM, and out of scope for another owner | App story, contract tests |
| rwb-decision WireMock | The evaluation answer of package "RESTRUCTURE" version "RES-2026.12" and the record entries of the two moves, so the criteria that end in the case can be driven; this service consumes neither | App story, contract tests |
| ACE common module stub | `statusFor` with "APPROVED" and 2026-12-10, "BROKEN" and 2026-12-14, no plan for "A-0310", a 3-second answer, "SUSPENDED", and an answer for more than 500 accounts | App story, contract tests |
| gateway-bff composite route stub | The merged plan section of the case record and the stored fallback with MSG-P2-008 | App story, contract tests |

Each fake is generated from the owning service's published OpenAPI document where one exists, and the drift test fails when a fake answers a shape or an error this document does not declare.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The plan-status read provided; the case read, the reference-data read, the parameters read and the authorise call consumed; one hop, 2 s timeout each |
| Kafka | None declared | A read publishes nothing and consumes nothing (DP-09) |
| Temporal | None declared | No workflow, no activity and no Schedule in this service for this key (DP-10) |
| File | None | This contract names no file; the ACE common module interface is counted in the consumed table and not as a file exchange |

### 13. Solution plan

**Deliverables.** `contract/plan-status-openapi.yaml` (the operation and its answer), `contract/plan-status-consumed.yaml` (the four consumed reads with the 2 s budget), `contract/ace-plan-interface.yaml` (the `RestructurePlanQuery` contract, its batch and its budget), `contract/plan-status-split.md` (the two providers, the stored answer and the ownership reconciliation), `contract/plan-status-config.yaml` (the status list, the two settings, the flag and the no-table statement), and five WireMock mapping sets plus the ACE stub.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; a read writes no record | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; the packages stay with rwb-decision and are evaluated by the case side, so this contract declares no evaluation | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The ACE common module's published interface (INT-34) with a 2 s budget and batching; no view and no grant on `recovery` | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents; no event is declared here | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the step is rwb-case's, so no Schedule is declared | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; no migration is declared | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write the OpenAPI document of the operation, with its answer, the meaning of `live` and `messageCode`, its errors and its read-only rule; AC1, AC3.
2. Write the consumed document: the four reads with owner, use and the 2 s budget, and the placeholder where no source fixes a path; AC2, AC4.
3. Write the ACE interface contract: the signature, the batch of 500, the 2000 ms budget, the breaker, the retry and the plan-to-account mapping; AC2.
4. Write the split note: the live answer here, the stored answer, the compare, the route move, the task, the timer and the record there, and the two reconciliations; AC6.
5. Write the configuration section: the status list, the two settings, the flag and the no-table statement; AC6.
6. Write the validation table of the seven messages and the operation that carries each; AC3.
7. Build the five fake sets, the ACE stub and the composite route stub, with the fixtures of the legacy criteria.
8. Add the contract tests, including the drift test between each fake and this document, the batch boundary over 500 accounts and the check that the monolith base appears nowhere.
9. Tag the baseline and collect the sign-off of the app story, the operations story, the case plan-status step and the harness.

**Done when.** The five contract files validate in the pipeline, the contract tests pass, each fake answers every declared shape, and the app story, the operations story, RWB-P3-E2002-APP and RWB-ITG-E2002-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The ACE common module or a consumed read did not answer inside the budget | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No session, or the person holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the Case record right calls the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope, or unknown | This case is not in your scope. |
| MSG-P2-008 | A stored plan status is shown because the live answer is not available | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-P7-003 | The decision record of a route move could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force on the business date | The rule version was refused at the {check} check: {detail}. |

This contract returns MSG-GEN-006, MSG-P4-001, MSG-P4-002 and MSG-P4-003 and no other message. MSG-P2-008, MSG-P7-003 and MSG-P3-027 are the case side's and are declared here only so that the caller knows which message comes from which provider; the contract adds no wording. For MSG-GEN-006, {system} names the source that did not answer. The seven texts are the agreed texts of the legacy story and of the platform catalogue.

### 15. Screens and states

None in this story. The contract serves the SCR-03 plan section through the gateway-bff composite route, and it renders no page and holds no screen state. The panel and its stored fallback are the screen work of RWB-P3-E2002-APP; the merge of the two provider answers is the composite route of RWB-PLT-N001-CON, whose path and merge order are Not specified in the source documents (GAP-0655; ASM-1109).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2002-CON-01 | AC1 | Contract | The operation validated against the OpenAPI document; a wrong field, a missing error and a write declared on the read are each refused |
| TC-P2-E2002-CON-02 | AC2 | Contract | The four consumed reads with owner, use and the 2 s budget; the interface with batches of 500 and 2000 ms; the placeholder where no path is fixed |
| TC-P2-E2002-CON-03 | AC3 | Contract | The known code, the code outside the list, the no-plan answer and the four error classes with their message IDs |
| TC-P2-E2002-CON-04 | AC4 | Contract | An unknown case, a case with no account, a case outside an Own scope, and a role without Case record R, against the fakes |
| TC-P2-E2002-CON-05 | AC5 | Component | The five fake sets and the ACE stub compared with the document; the drift test fails on a shape the document does not declare |
| TC-P2-E2002-CON-06 | AC6 | Contract | The split note against the Ownership Map row and API-P2-010; the no-table and no-migration statement; the two reconciliations |

The levels map the platform taxonomy: a contract artefact is Contract, a fake compared with the document is Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. This story writes no `-ITG` copy: the cross-service proof of the key is RWB-ITG-E2002-ITG's.

### 17. Guardrails

- No business value in the contract: the status list, the two settings, the flag and the breaker thresholds are rows, parameters and values of their owners.
- No personal data and no account number in an answer, an example or a fake: the case reference, the plan reference, the status code, the flag and counters only; the fixtures use the synthetic account "A-0310" of the legacy story.
- The contract names only this service's operation as provided; the case, the reference data, the parameters and the authorise answer are consumed and never restated as this service's (DP-01, DP-13).
- One base, one queue and one topic: a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The plan is read only through the published module interface; a document that declares a `v_ace_*` read, a table read or a grant on `recovery` fails the review (DP-05, ADR-010).
- A read writes nothing and publishes nothing; a document that declares a write, an event, a Schedule or a cached answer on this operation fails the review (BR5).
- The stored plan status and its date are not declared here; a document that gives this service the stored answer or the route move fails the review (BR4, AC6).
- Every example and fixture is synthetic; no production payload, case number, account number or plan reference is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | The interface contract and the operation answer | TC-P2-E2002-CON-01, TC-P2-E2002-CON-02 |
| REQ-CHO-002 | Plan status change visible on the case | The `live` flag, the `messageCode` rule and the two-provider split note | TC-P2-E2002-CON-01, TC-P2-E2002-CON-03 |
| D-RCV-60 DP-05 | The ACE plan comes from the published interface, not from a view | The interface contract, the batch and the budget | TC-P2-E2002-CON-02 |
| D-RCV-60 DP-13 | The operation sits on the integration base | The provided operation on `/api/recovery/integration/v1` | TC-P2-E2002-CON-01 |
| D-RCV-60 DP-19 | The case record plan section is one gateway answer | The composite route stub and the split note | TC-P2-E2002-CON-05, TC-P2-E2002-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed reads and the budget | TC-P2-E2002-CON-02 |

### 19. Out of scope

- The implementation of the operation, the ACE client, the validation and the access check (RWB-P2-E2002-APP).
- The deployment of the service, the ACE endpoint, the flag, the dashboards, the alerts and the runbook (RWB-P2-E2002-OPS).
- The stored plan status, its date, the compare, the route state, the rule evaluation, the task, the durable timer and the decision record (RWB-P3-E2002-APP, RWB-P7-E2002-APP).
- The rule packages, their versions and the catalog rows (RWB-P3-E2042-APP, RWB-P7-E2002-APP).
- The roles, the scope and the rights data (RWB-P4-E2002-APP).
- The plan status panel on SCR-03 and the plan section of SCR-14, and their field-level behaviour (RWB-P3-E2002-APP).
- The ACE plan itself, which is created and changed in ACE under DL14.
- The real cross-service proof of the journey (RWB-ITG-E2002-ITG).
- The field-level detail of the consumed shapes and the remaining interface elements (GAP-0655).
