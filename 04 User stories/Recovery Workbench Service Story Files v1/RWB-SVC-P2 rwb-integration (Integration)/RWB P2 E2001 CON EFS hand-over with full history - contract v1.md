# RWB-P2-E2001-CON EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-integration. The legacy story carried its interfaces as Java signatures inside one module; this story fixes the same seams as a contract — the hand-over activity and its summary, the `AceDataReady` intake, the elements this slice consumes from rwb-source-data, rwb-case and rwb-decision, the error envelope, the idempotency keys and the fakes — so the app, operations and test stories of this legacy key build on Day 1 against one agreed shape. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-integration side of the EFS hand-over fixed as a contract: the hand-over activity and its run summary, the `AceDataReady` intake with its key and dedupe, the elements this step consumes from the rwb-source-data, rwb-case and rwb-decision contracts, the error envelope and the idempotency keys, the objects of `rwb_integration` it uses and the fakes for the three owners**, so that **the app, operations and test stories of this legacy key build on Day 1 against one testable shape and no team waits for another service to exist**.

Under D-RCV-60 the legacy journey is six services and four owners: rwb-source-data owns the ACE view contract, the freshness stamps and the interaction ledger (DP-05, DP-18), rwb-case owns the case and publishes `CaseCreated`, rwb-decision owns the central ledger, and rwb-integration owns the hand-over step. A step that only calls other owners needs a contract more than an owner does: it must say what it is started by, what it calls and in which order, what it counts, what it refuses and what it never touches — and it must be faked so the app story is testable before the owners exist.

The contract also fixes the seam the split creates. The legacy story took the ledger append, the case creation and the decision record inside one transaction. Across four services there is no shared transaction, so the contract states the only rule that keeps the legacy guarantee: the per-account key is taken before the case is asked for, the EFS append is called after the case answers and is idempotent on `efs_record_key`, both calls are safe to repeat, and the run summary and the run's own record commit together. That single ordering rule is what makes a repeat, a held morning and a partial morning provable across services, and it is why this story is Day 1 work.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020) and the event contract is the platform rule (DP-09). Both only pay off if the seam is written down once. Here the seam is small and load-bearing: one consumed event, one workflow and its activities, five consumed P1 operations, one consumed P3 operation, one read of the central ledger, three idempotency keys and one summary shape.

If the shape is agreed and faked on Day 1, three teams move at once. The app story builds the listener, the run lock, the group builder, the clients and the summary writer against the fakes; the operations story wires the queue, the subscription, the alerts and the runbook against the same document; the test stories of this legacy key and RWB-ITG-E2001-ITG read one summary shape. Without it, each team invents its own key, its own hold rule and its own count names, and the one property the business asked for — that no case is built from a stale batch and no morning is silently lost — depends on which service answered first.

The contract also states what this service does not own. `interaction`, `efs_ledger_outcome` and `reconciliation_result` are rwb-source-data's; `recovery_case` and `case_account` are rwb-case's; `decision_log_entry` is rwb-decision's; the run statistics of JOB-02 are rwb-case's. This document defines the consumed side of each and restates none of them as its own.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1` and the queue `rwb-integration` follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the platform error envelope and the message catalogue are the platform baseline; this document narrows them where it must and says so (DP-09).
- The outbox and inbox library contract is available (RWB-PLT-TE006-CON): `processed_event`, `idempotency_key`, `outbox_event`, `outbox_delivery`, the retry topic and the `.dlt` topic are its elements and are reused, not redefined.
- The workflow kit is available (RWB-PLT-E1071-CON): one task queue per service in the namespace `rwb-recovery`, worker versioning and the payload codec.
- The decision-record library is available (RWB-PLT-E1027-CON) with the shared topic `rwb.decision-record.v1` (DP-03).
- The owners' published contracts are as consumed here: rwb-source-data's freshness, record, interaction and rerun operations and `AceDataReady` (RWB-P1-E1015-CON and the P1 stories of this legacy key), rwb-case's case creation, parameters and reference data (RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P3-E2001-CON), and rwb-decision's central ledger read.
- The gateway-bff composite routes of RWB-PLT-N001-CON are published for SCR-02, SCR-04 and SCR-45 (DP-19).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the consumed-event contract: `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`, its envelope, its key, its dedupe key and the `.dlt` rule.
2. Publish the hand-over activity contract: the workflow, its activities, their inputs and outputs, the retry policy of each and the `HandoverSummary` element.
3. Publish the consumed P1 elements: freshness, the eligible-account read, the customer read, the EFS append and the reconciliation write, with the 2 s budget and the 4xx and 5xx split.
4. Publish the consumed P3 element: the case-creation operation, its request shape, its created-or-linked answer, its record-failure answer and the absence of a create path in the Ownership Map.
5. Publish the consumed P7 element: the central ledger read as a proof surface only, and the library's `DecisionRecorded` element for the run record.
6. Fix the three idempotency keys and the run lock, and the ordering rule between the key, the case call and the append.
7. Fix the error envelope mapping: which answer becomes which of MSG-P1-001, MSG-P2-007, MSG-P7-003, MSG-P2-006, MSG-P4-002 and MSG-GEN-006.
8. State the table ownership: the five library objects of `rwb_integration`, and the explicit statement that no case, account, interaction or reconciliation table is among them.
9. Publish the fakes and the drift test, then tag the baseline and hand it to the app and operations stories of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A message does not carry the CloudEvents 1.0 attributes, carries no business date, or names a source other than ALS | The listener refuses it before any state change and routes it to `.dlt` with an alert; no run starts | None | AC2 |
| X2 | A fake drifts from this document, or the app calls a path this document does not declare | The contract test fails and the merge is blocked | None | AC7 |
| X3 | A service code path reads a case, account, interaction or reconciliation table, or an ACE view | The architecture boundary test fails the build | None | AC8 |
| X4 | A consumed operation removes, renames or retypes an element this document declares | The contract goes back to review with the owner of that operation, and the app and operations stories are re-baselined | None | AC4, AC5 |
| X5 | A field-level detail of a consumed operation is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1 |
| X6 | The case-creation answer is a success but the EFS append answers 5xx | The append is retried inside its attempt budget; a final failure marks the run partial and names the account, and the next run appends again under the same `efs_record_key` | None | AC6 |
| X7 | A second start arrives while the run lock is held | Refused with 409 and nothing changes; the run lock is the only arbiter | MSG-P2-006 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the owners' published operations and declares none of theirs as its own |
| Negotiable | Field-level detail of the consumed operations is settled with their owners; the keys, the summary shape and the ordering rule are fixed by this realignment |
| Valuable | Unblocks the app and operations stories of this key and gives rwb-source-data, rwb-case and rwb-decision one summary shape and one key set to agree on |
| Estimable | One consumed event, one workflow, nine activities, seven consumed operations, three keys, five library objects and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the AsyncAPI document, the activity contract, the fake, this file — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over contract baseline for rwb-integration

  Background:
    Given the service naming rule, the CloudEvents 1.0 envelope and the platform error envelope of the platform library are in force
    Given the outbox and inbox library contract of RWB-PLT-TE006-CON is in force
    Given the interaction ledger is owned by rwb-source-data and the case by rwb-case

  Scenario: AC1 The nine contract tables are complete and attributed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 is None and states that the step is event-started and provides no path
    Then 12.2 names the six rwb-source-data elements, the one rwb-case element and the central ledger element
    Then 12.3 is the decision-record element only, 12.4 is AceDataReady, 12.5 is the workflow and its nine activities, 12.6 is None and 12.8 is the four fakes
    Then 12.7 names only the five library objects of rwb_integration and states that no case, account, interaction or reconciliation table is among them
    Then a sub-table that names another service's table or operation as its own fails the review

  Scenario: AC2 The AceDataReady intake is fixed with its envelope, key and dedupe (new, D-RCV-60)
    Given the consumed-event contract of this story
    When a message of rwb.source-data.AceDataReady.v1 is validated against it
    Then the message carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype
    Then the message carries the source and the business date, and its dedupe key is EV-26:ALS:<businessDate>
    Then the message carries no personal data and names no account
    Then a message without the envelope, without a business date, or for a source other than ALS is refused and routed to .dlt with an alert

  Scenario: AC3 The hand-over activity and its run summary are fixed (new, D-RCV-60)
    Given the activity contract of this story
    When the workflow, its nine activities and the HandoverSummary are reviewed
    Then the workflow is started once per business date with workflow ID efs-handover-<businessDate> on the queue rwb-integration in the namespace rwb-recovery
    Then every activity names its input and its output and none of them carries a personal value
    Then the summary carries businessDate, outcome, accountsRead, groupsBuilt, casesCreated, accountsLinked, interactionEntriesWritten, interactionEntriesSkipped, repeats, held, gapDates and failures
    Then outcome is one of COMPLETED, HELD and PARTIAL and no other value is written
    Then the retry policy is the kit's, with a 4xx answer non-retryable except a 409, which is a repeat

  Scenario: AC4 The six consumed rwb-source-data elements are fixed and no ACE view is read (new, D-RCV-60)
    Given the consumed contract of this story
    When the six elements are reviewed against the rwb-source-data contract
    Then the elements are the freshness read, the eligible-account read, the customer read, the interaction append, the reconciliation write and the rerun seam
    Then each element is one hop on the base /api/recovery/source-data/v1 with a 2 s budget
    Then the interaction append is create-only and idempotent on efs_record_key, so a repeat returns the same entry reference and writes nothing
    Then the reconciliation write carries the REC-01 counts of the run and nothing else
    Then no element is an ACE view, a query text over recovery.v_ace_* or a second reader of the ACE views

  Scenario: AC5 The consumed rwb-case and rwb-decision elements are fixed (new, D-RCV-60)
    Given the consumed contract of this story
    When the case-creation element and the central ledger element are reviewed
    Then the case-creation element answers a case reference, a created-or-linked outcome and the account links with linked from and is primary
    Then a decision-record failure inside rwb-case is answered as its own error class and carries MSG-P7-003
    Then the case-creation element is the only write of the step on rwb-case, and the account link, the case status and CaseCreated are rwb-case's
    Then the central ledger is read at most for proof, and the run's own record is written locally and published as DecisionRecorded on rwb.decision-record.v1
    Then no element of this contract declares a table or an operation of rwb-case or rwb-decision as its own

  Scenario: AC6 The error envelope, the three keys and the ordering rule are fixed (new, D-RCV-60)
    Given the error and key element of this story
    When a failure of each class is raised against the contract
    Then a stale data product is MSG-P1-001, a held run is MSG-P2-007, a failed record is MSG-P7-003, a second start is 409 with MSG-P2-006, a refused role is MSG-P4-002 and an unanswered source is MSG-GEN-006
    Then the keys are EV-26:ALS:<businessDate> for the intake, handover-run:<businessDate> for the run lock and handover:<account_key>:<businessDate> for one account
    Then the per-account key is taken before the case-creation call, the append is called after the case answers, and the run summary and the run record commit together
    Then a repeat of any of the three keys writes nothing a second time and is counted
    Then no error payload carries an account holder, a contact point or an amount

  Scenario: AC7 The four fakes match this document and drift fails the build (new, D-RCV-60)
    Given the four fakes of 12.8
    When each fake is compared with the element it serves
    Then every consumed path and payload is answered with the shape of this document
    Then every error answer named in this document is reachable in a fake
    Then a drift between a fake and this document fails the contract test and blocks the merge

  Scenario: AC8 No cross-schema read and no foreign key leave this service (new, D-RCV-60)
    Given the code and the migrations of the app and operations stories of this key
    When the architecture boundary test runs
    Then no statement reads a table of another service and no statement reads an ACE view
    Then the only cross-service calls are the declared elements of 12.2, one hop each with a 2 s budget
    Then rwb_integration holds no foreign key into another schema and no copy of a case, an account, an interaction or a reconciliation row
    Then the single consumed topic is rwb.source-data.events.v1 and no topic of this service is subscribed
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base, one topic and one queue per service: this contract declares `/api/recovery/integration/v1`, `rwb.integration.events.v1` and `rwb-integration`, and consumes the owners' bases and topic | DP-13; DP-14; Arch v5 slide 41 |
| BR2 | The step is started by `rwb.source-data.AceDataReady.v1` for the ALS source and business date, and by nothing else; JOB-02 case creation stays rwb-case's and JOB-03 follows it there | DP-10; Arch v5 slide 44; RWB-ITG-E2001-ITG |
| BR3 | Only rwb-source-data reads the thirty `recovery.v_ace_*` views; this contract consumes its elements and declares no view, no query text and no grant on `recovery` | ADR-010; DP-05; Arch v5 slides 15, 41 and 45 |
| BR4 | The interaction ledger, `efs_ledger_outcome` and `reconciliation_result` are rwb-source-data's; the case, `case_account` and `CaseCreated` are rwb-case's; the central ledger is rwb-decision's | R-PREC default ruling; DP-18; Ownership Map |
| BR5 | One key per unit of work: the intake key, the run lock and the per-account key of BR6; a repeat writes nothing a second time and is counted | Legacy R-UNI-40 and AC2; FSD P2 Integration v3 AC-EXC-P2-007-07 |
| BR6 | The per-account key is `handover:<account_key>:<businessDate>`, the legacy `IdempotencyGuard.firstTime("handover", accountKey + ":" + D)` | Legacy RWB-E2-001 section 4 step 4 and section 12 |
| BR7 | The step takes the per-account key before the case-creation call, appends after the case answers, and commits the run summary with the run record; there is no shared transaction across the four services | DP-03; Temporal and Drools design slide 11 |
| BR8 | A business date whose DP01 or DP05 stamp is stale produces a held run with MSG-P1-001 and MSG-P2-007 and no case; the gap date is carried to the next good run | Legacy BR4; FSD P2 Integration v3 VR-P2-001-1 |
| BR9 | No business value in the contract: the threshold, the hold time, the product map, the action codes, the retry intervals and the attempt limit are rows and environment values | Template and Rules §R7.2 s17 |
| BR10 | No element of this contract carries a person: business keys, counts, codes, business dates and message ids only | Legacy BR5; ADR-023 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The nine sub-tables, the intake, the activity contract, the three keys and the four fakes are described | In review |
| In review | Owner sign-off | The P1, P3 and P7 owners accept the consumed elements and the app story accepts the activity contract | Baselined |
| Baselined | Additive change | A field, an error class or a fake is added without removing one | Baselined |
| Baselined | Breaking change to a consumed element | An owner removes, renames or retypes an element this contract declares | In review, with that owner |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The step gains a second trigger | A source other than ALS asks for a hand-over | In review, with the solution architect |

The run states `COMPLETED`, `HELD` and `PARTIAL`, and the refusal of a second start, are runtime states of the app story and are fixed in 12.5; they are not states of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns this document and the four fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed element, a second trigger and any change to the ordering rule |
| The rwb-source-data owner | Owns the six consumed elements and signs off the shapes taken from its contract |
| The rwb-case owner | Owns the case-creation element, the account link and `CaseCreated`, and signs off the answer shape |
| The rwb-decision owner | Owns the central ledger and the `DecisionRecorded` element this contract consumes |
| The rwb-integration app and operations stories | Review and accept the parts they consume |
| Data steward | Confirms that no personal value is declared in an event, an activity input or a fake |

The deployment identity that calls the owners' contracts is Not specified in the source documents (GAP-0652; ASM-1087); the document names it "the rwb-integration login (DP-02)" and leaves the name to the app and operations stories.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Consumed event envelope | id, source, type, specversion, time, subject, datacontenttype; payload keyed by source and business date |
| Intake record | consumer, key `EV-26:ALS:<businessDate>`, CloudEvents id, hit count, last seen (`processed_event`) |
| Run lock record | key `handover-run:<businessDate>`, endpoint, request hash, stored answer, expiry (`idempotency_key`) |
| Per-account key record | key `handover:<account_key>:<businessDate>`, endpoint, request hash, stored answer (`idempotency_key`) |
| Freshness answer | per data product: DP01 and DP05, the business date and the fresh or stale state |
| Candidate row | account key, product key, days past due, total balance, data as of, person key |
| Case-creation request | person key, product group, business date, entry date, days past due at entry, total outstanding at entry, the accounts with the primary flag |
| Case-creation answer | case reference, created or linked, the account links with linked from and is primary, or the decision-record failure class |
| Append request | case id, account key, business date, source system EFS |
| Append answer | entries written, entries skipped, the first and last `efs_record_key` of the set |
| Reconciliation request | business date, the REC-01 counts and the unexplained difference |
| HandoverSummary | the twelve elements of AC3 |
| Decision-record element | decision code "D6 entry", the business date, the freshness answer of DP01 and DP05, the counts, the outcome and the incident reference |
| Activity input and output | the business date and the CloudEvents id in; the `HandoverSummary` out |

The physical names, lengths and required flags of the consumed requests and answers are Not specified in the source documents (GAP-0652; ASM-1095); this story fixes the element names above and leaves the physical names to the review with each owner. The activity names and the `HandoverSummary` element names are likewise fixed here as the default and carry the same gap and assumption.

### 12. Contract

#### 12.1 REST operations provided

None. The hand-over step is event-started and answers an activity, so this slice adds no path to the base `/api/recovery/integration/v1`; the base and its existing operations — `GET /admin/scheduled-jobs`, `GET /admin/outbound-items`, `POST /admin/outbound-items/{itemId}/resend`, `GET /admin/outbox/deliveries` and `POST /admin/outbox/deliveries/{deliveryId}/resend` — are the integration base's, declared by RWB-P2-E1007-CON and RWB-P2-E2034-CON. The step provides no summary endpoint: its result is the activity answer of 12.5, the run's local decision record and the REC-01 row written through the P1 contract (ASM-1096). The refusal of a second start is the answer of the run lock, relayed by the rwb-source-data rerun operation, and is not a path of this service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the contract |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The DP01 and DP05 stamp answers at the business date; faked fresh, stale and unavailable |
| GET | The eligible-account read of the rwb-source-data contract (legacy `AccountQuery.findAtOrAboveDpd`) | P1 rwb-source-data | The candidate rows at or above the threshold and below the open-case filter; faked with two candidates and one excluded |
| GET | The customer read of the rwb-source-data contract | P1 rwb-source-data | The person key and the customer of a candidate, and the absence of a row; faked with one hit and one 404 |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The EFS append, create-only and idempotent on `efs_record_key`; faked with 201, the same reference on a repeat, 409 and 503 |
| POST | The reconciliation-result write of the rwb-source-data contract | P1 rwb-source-data | The REC-01 row of the run; faked with a committed row and a 503 |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | The administrative rerun seam that relays a refused second start; faked with 409 and MSG-P2-006 and with 403 for a refused role |
| POST | The case-creation operation of the rwb-case contract (legacy `CaseCreation.createOrLink`) | P3 rwb-case | The created, linked and record-failure answers of 12.2; faked with all three and with a 5xx |
| GET | `/api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case reference and status behind a created answer, for the asserters of the app and test stories; faked with one case and one 404 |
| GET | The parameter and reference-data reads of the rwb-case contract | P3 rwb-case | The threshold, the hold time and the product map with the version in force; faked with 90, 09:00 and the map |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The central ledger entry for the run record, read for proof only; faked with one entry and one empty page |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role and rights of the caller behind the refusal asserted by the access test of RWB-P2-E2001-APP section 16; faked granting the step and refusing the rerun |

Every operation is one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s client budget and no retry on a 4xx except a 409, which is a repeat (DP-11, ADR-020). The eligible-account read, the customer read and the reconciliation write are named by their legacy Java interfaces only, and the case-creation operation is named by `CaseCreation.createOrLink`; their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0652; ASM-1095). The paths that a source does give are used as published: the freshness read, the interaction append and the rerun from the P1 contract and the P2 baseline, the case and decision reads from the Ownership Map.

#### 12.3 Events published

None of this service's own: `rwb.integration.events.v1` carries `FileDelivered` and `FileFailed` from the outbound-file side (RWB-P2-E1007-APP; Arch v5 slide 16) and this slice publishes neither. The shared event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when the run record commits; its schema is unchanged by this story and is the one declared in RWB-PLT-E1027-CON (EV-08, Arch v5 slide 42 row 08). `rwb.case.CaseCreated.v1` is published by rwb-case and is consumed nowhere here.

#### 12.4 Events consumed

| Event type | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | CloudEvents 1.0; payload carries the source and the business date; dedupe `EV-26:ALS:<businessDate>`; starts `EfsHandoverWorkflow` for the ALS source and writes nothing by itself; a duplicate raises the hit count and starts no second run; a message that fails the envelope, lacks the business date or names another source is routed to `.dlt` with an alert |

One type and one topic are consumed, at least once, and idempotent by key (DP-09). The payload is the owner's; this contract declares the elements the listener reads and does not restate the owner's schema.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| EfsHandoverWorkflow | Workflow, one execution per business date, workflow ID `efs-handover-<businessDate>` | `rwb-integration` | Input: business date, source ALS, CloudEvents id. Output: `HandoverSummary` |
| acceptAceDataReady | Activity | `rwb-integration` | Input: the event envelope. Output: accepted or repeat, with the inbox key |
| readFreshness | Activity | `rwb-integration` | Input: business date. Output: the DP01 and DP05 answers |
| listCandidates | Activity | `rwb-integration` | Input: business date, threshold. Output: the candidate rows and the excluded count |
| buildGroups | Activity | `rwb-integration` | Input: the candidates and the product map. Output: the groups |
| createOrLinkCase | Activity | `rwb-integration` | Input: one group. Output: the case reference, the outcome and the links, or the record-failure class |
| appendEfsHistory | Activity | `rwb-integration` | Input: case id, account key, business date. Output: written and skipped counts |
| writeRunSummary | Activity | `rwb-integration` | Input: the counts and the outcome. Output: the REC-01 answer and the summary |
| recordRunDecision | Activity | `rwb-integration` | Input: the summary. Output: the local record and its outbox row |
| releaseRunLock | Activity | `rwb-integration` | Input: the run key. Output: released, with the elapsed time |

The retry policy of every activity is the workflow kit's: initial interval 1 s, back-off 2, maximum 3 attempts, with the 4xx answers of the case-creation and append calls classified as non-retryable except a 409, which is a repeat (DP-10). The workflow input and history carry identifiers, business dates, codes and counts only.

#### 12.6 Schedules

None. No Schedule is registered for this slice. The step is started by `AceDataReady`, not by a timer, and JOB-02 and JOB-03 are rwb-case's (BR2; Arch v5 slide 44). The outbox relay of the service runs on the platform relay interval of DP-09 and is not a Schedule of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| processed_event | PLT library, created in `rwb_integration` | The inbox: consumer, key, CloudEvents id, hit count |
| idempotency_key | PLT library, created in `rwb_integration` | The run lock and the per-account keys, with the stored answer |
| decision_record | PLT library, created in `rwb_integration` | The run's local decision record (DP-03) |
| outbox_event | PLT library, created in `rwb_integration` | The outbox row the decision-record library writes |
| outbox_delivery | PLT library, created in `rwb_integration` | The delivery of `DecisionRecorded` on `rwb.decision-record.v1` |

No other table is named. `interaction`, `efs_ledger_outcome` and `reconciliation_result` are rwb-source-data's; `recovery_case` and `case_account` are rwb-case's; `decision_log_entry` is rwb-decision's; `interface_config`, `outbound_item` and `job_catalog` are the integration base's and this contract writes no row in them. None of the other services' tables appears here as an object of this service (BR4, DP-01, DP-18).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | Freshness fresh at 2026-12-14 and DP05 stale at 2026-12-15; the candidate rows of "A-0001", "A-0002" and "A-0004" and the excluded "A-0003"; the customer read with one hit and one 404; the append answering 201 with 16 written, then the same reference with 16 skipped, a 409 and a 503; the reconciliation write committed and unavailable; the rerun seam answering 409 with MSG-P2-006 and 403 with MSG-P4-002 | App story, contract tests |
| rwb-case WireMock | The case-creation operation answering created, linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false, and the decision-record failure carrying MSG-P7-003; the case read with one case and one 404; the parameter read returning 90 and 09:00; the reference-data read returning the product map | App story, AC4 and AC7 of the legacy key |
| rwb-decision WireMock | One central ledger entry for the run record and an empty page for the failed group | App story |
| rwb-access WireMock | The session check granting the step and refusing a role without Platform administration U | App story, the access test in its section 16 |
| Decision-record library stub | A committed record with its outbox row, and the unavailable-store case that leaves the run summary uncommitted | App story, contract tests |
| Kafka stubs | One valid `AceDataReady`, one duplicate of the same key, one malformed envelope and one message of another source | Contract tests |

The fakes are published from the owning services' OpenAPI documents and are versioned with this baseline; a drift fails the contract test of AC7.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 11 consumed | Six P1 elements, the P3 case-creation element and its reads, the P7 ledger read and the P4 session check; one hop, 2 s timeout each |
| Kafka | 0 published by this slice, 1 published by the library, 1 type consumed | `rwb.source-data.events.v1` consumed with the inbox and `.dlt`; `rwb.decision-record.v1` carries `DecisionRecorded` for the run record |
| Temporal | 1 workflow, 9 activities | `EfsHandoverWorkflow` on the queue `rwb-integration` in the namespace `rwb-recovery`; 0 Schedules |
| File | None | ACE data arrives through the P1 contract, never as a file or a view |

### 13. Solution plan

**Deliverables.** `contract/handover-run-activities.yaml` (the activity contract, the `HandoverSummary` and the retry policy), `contract/ace-data-ready-consumed.yaml` (the consumed type, its envelope, key and dedupe), `contract/handover-consumed-p1.yaml` (the six rwb-source-data elements with their answers), `contract/handover-consumed-p3-p7.yaml` (the case-creation element and the central ledger read), `contract/handover-errors-keys.yaml` (the error classes, the three keys and the ordering rule), and the six WireMock mappings of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; no other schema is read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts through rwb-source-data's contract; no view is read here | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case with the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the product map stays rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the owner's topic, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data; the append is consumed | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02, SCR-04 and SCR-45 | H RWB-PLT-N001-CON |

The platform H dependencies those patterns add are the platform contracts the app and operations stories of this key consume; they are not repeated in the metadata H column, which stays None because a CON story is Day 1 by rule (§R5.7) and builds nothing itself.

**Build steps**

1. Write the consumed-event contract: the type, the topic, the envelope, the key, the dedupe key and the `.dlt` rule.
2. Write the activity contract: the workflow, the nine activities, their inputs and outputs, the retry policy and the `HandoverSummary`.
3. Write the six P1 elements with their answers, the 4xx and 5xx split and the append's `efs_record_key` idempotency.
4. Write the P3 case-creation element and the P7 ledger read, with the created, linked and record-failure classes.
5. Write the error and key element: six message classes, three keys, the ordering rule and the run-lock refusal.
6. Write the table ownership statement and the explicit absence of the case, account, interaction and reconciliation tables.
7. Build the six WireMock mappings and their fixtures.
8. Add the eight contract tests of section 16, including the drift test between each fake and this document.
9. Tag the baseline and collect the sign-off of the app and operations stories of this key.

**Done when.** The five contract files validate in the pipeline, the eight contract tests pass, the six fakes answer every consumed element and every documented error, and the app and operations stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product is stale at the business date of the run | {product} is from {date}. Today's data is not yet complete. |
| MSG-P2-007 | Case creation is held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | The decision record of a group or of the run cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | A second start while the run lock is held | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right requests the rerun | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A consumed source did not answer inside the budget | {source} could not be read. Try again in a few minutes. |

MSG-P1-001 uses the wording of FSD P2 Integration v3 and not the older wording of the legacy story; the divergence is recorded and not repaired here (GAP-0652; ASM-1093). Every other text is the legacy text unchanged. This contract adds no message and no wording.

### 15. Screens and states

None in this story. The step serves no screen and the contract fixes no field of one. The screens it feeds — SCR-02 case list, SCR-04 case timeline and SCR-45 data quality — are read through the gateway-bff composite routes of RWB-PLT-N001-CON, and their fields, states and masking belong to the app stories of rwb-case and rwb-source-data and to the app story of this key (DP-19). The contract states only the values a screen may receive: the counts of the run summary, the held state with its stale data product, and the repeat count.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2001-CON-01 | AC1 | Contract | The nine sub-tables present; 12.1 and 12.6 None with a reason; only the five library objects named; a sub-table naming another owner's table or operation fails |
| TC-P2-E2001-CON-02 | AC2 | Contract | One valid `AceDataReady`, one duplicate of the same key, one malformed envelope and one message of another source refused to `.dlt` |
| TC-P2-E2001-CON-03 | AC3 | Contract | The workflow and its nine activities with inputs and outputs; the twelve summary elements; the three outcomes and a fourth value refused; the retry classes |
| TC-P2-E2001-CON-04 | AC4 | Contract | The six P1 elements with their answers; the append's 201, repeat, 409 and 503; the reconciliation write; no view, no query text and no grant on `recovery` |
| TC-P2-E2001-CON-05 | AC5 | Contract | The case-creation answer created, linked with linked from 2026-12-15 and is primary false, and the record failure carrying MSG-P7-003; the ledger read; no declared case or decision table |
| TC-P2-E2001-CON-06 | AC6 | Component | One failure of each of the six classes; the three keys; a repeat of each key writing nothing; the ordering rule checked on the recorded call sequence |
| TC-P2-E2001-CON-07 | AC7 | Contract | Each of the six fakes compared with its element; every documented error answer reachable; one injected drift fails the test |
| TC-P2-E2001-CON-08 | AC8 | NFR | The boundary test finds no cross-schema statement, no ACE view, no undeclared path and no foreign key out of `rwb_integration` |

### 17. Guardrails

- No business value in the contract: the threshold, the hold time, the product map, the action codes, the retry intervals and the attempt limit stay rows of their owners and environment values.
- No personal data in an event, an activity input, a summary or a fake: business keys, codes, counts and business dates only.
- The contract names only rwb-integration's own base as its own; the P1, P3, P4 and P7 elements are consumed and are never restated as this service's (DP-01, DP-13).
- One REST base, one topic and one queue per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The interaction ledger, the EFS outcome list, the case, the account link and the central ledger appear nowhere as objects of this service (DP-18; BR4).
- Every example and fixture is synthetic; no production payload or key is copied into a schema or a fake.
- The envelope, the inbox, the retry topic and the `.dlt` rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch and is read through the ACE data path | The consumed `AceDataReady`, its key and the candidate element | TC-P2-E2001-CON-02, TC-P2-E2001-CON-04 |
| REQ-CHO-001 | Case with full contact and promise history | The case-creation element, the append element and the summary's append counts | TC-P2-E2001-CON-04, TC-P2-E2001-CON-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | The created-or-linked answer and the absence of a case write here | TC-P2-E2001-CON-05, TC-P2-E2001-CON-08 |
| REQ-RDF-003 | EFS history transfers to the case | The append element and its `efs_record_key` idempotency | TC-P2-E2001-CON-04 |
| ADR-010 | Only rwb-source-data reads the thirty ACE views | The six consumed elements and the absence of any view | TC-P2-E2001-CON-04, TC-P2-E2001-CON-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eleven consumed operations with the 2 s budget | TC-P2-E2001-CON-08 |

### 19. Out of scope

- The listener, the workflow, the group builder, the clients, the summary writer and the migration as code (RWB-P2-E2001-APP).
- The chart, the subscription, the Flyway step, the alerts, the dashboards and the runbook (RWB-P2-E2001-OPS).
- The case creation, the account link, `CaseCreated` and the case-creation decision record (RWB-P3-E2001-APP).
- The EFS history read, the `efs_ledger_outcome` filter, the interaction entries and the REC-01 row in `rwb_source_data` (RWB-P1-E2001-APP).
- The central decision ledger, its hash chain and its seal (RWB-P7-E2001-APP and RWB-PLT-E1027-CON).
- The freshness stamp, `AceDataReady` and the read-only ACE view contract (RWB-P1-E1015-CON, RWB-P1-E1069-APP).
- JOB-02, JOB-03 and the run statistics of the case creation (rwb-case).
- The integration base, its outbound-file adapters and its topic (RWB-P2-E1007-CON and RWB-P2-E1007-APP).
- The real cross-service proof of the journey against the live owners (RWB-ITG-E2001-ITG).
- The field-level completeness of the consumed contracts (GAP-0652).
