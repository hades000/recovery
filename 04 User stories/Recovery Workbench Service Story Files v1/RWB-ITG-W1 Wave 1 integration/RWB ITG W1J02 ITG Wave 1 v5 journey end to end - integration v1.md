# RWB-ITG-W1J02-ITG Wave 1 v5 journey end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-W1J02-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | W1J02 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new wave 1 end-to-end journey harness story for the wave 1 release gate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the QA team**, I want **one repeatable wave 1 end-to-end journey harness that chains the wave 1 business behaviour of EP01 on one synthetic case for one business date across rwb-source-data (P1), rwb-case (P3), rwb-access (P4), rwb-document (P5), rwb-comms (P6), rwb-decision (P7), rwb-reporting (P9), rwb-agent (P10) and rwb-integration (P2), asserting each hop through the owner's published contract and composing through gateway-bff where a screen would**, so that **the wave 1 release is accepted on evidence of the whole journey and not on nine separate service test results, and a red hop stops the release rather than being found in production**.

This story builds the harness, its evidence and its gate. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table. The behaviour it proves is owned by the wave 1 service stories; the harness only drives the owners' published operations, reads the owners' published answers, consumes the owners' events and records what happened.

The journey chains, in this order, only the wave 1 business behaviour of EP01 (wave map §R5.6: EP01 is wave 1): the seeded set and its readiness for the business date; the case, its accounts, its queue and its owner read from rwb-case; a synthetic document posted into the document hub, its OCR, classification and extraction, and its automatic attachment to the case; the document-received transfer of the case with a reason code; the decision record of every hop that took a decision; the case intake agent run in SHADOW, which recommends and moves nothing; the demand notice on an approved template with its document reference; the 16:00 WIN file of the business date with its manifest; the 01:30 measures of the same business date; the interaction ledger with one entry per hop; and the authorisation answer on every call.

The nine owners the journey drives are rwb-source-data (P1), rwb-case (P3), rwb-document (P5), rwb-comms (P6), rwb-decision (P7), rwb-reporting (P9), rwb-agent (P10), rwb-integration (P2) and rwb-access (P4), which answers the authorisation of every call. The harness adds no business rule of its own: every expectation it asserts is copied from a rule, a state or an operation that a source already gives.

The harness stories are what give the QA team its Day 1 work (Template and Rules §R5.7 rule 6). W1J01 is the contract-test harness and its synthetic set and W1J02 is this journey; together they are the wave 1 release gate of Architecture v5 slide 46, which lists contract tests per API, event and activity, Temporal replay tests and a daily journey smoke workflow and asks how the 19 services are tested as a set.

The direct precedent is the wave 2 counterpart RWB-ITG-W2J01-ITG; this story takes the same shape for wave 1 and chains the wave 1 hops that the wave 1 integration suites prove one loop at a time.

### 2. Business rationale

A service can be green on its own contract tests and still leave the wave broken, because what wave 1 sells is a journey: a case arrives from the daily list, a document arrives from the branch and attaches itself, the case moves to the team that must act on it, the decision behind each move is written once and hash-chained, the intake agent reads the case without touching it, a demand notice leaves on Legal-approved wording and reaches WIN in the 16:00 file, the measures of the day are published from the same facts, and the ledger tells the whole story in order. Each of those outcomes is produced by a different owner, on a different task queue, through a different call type, and each one is only as good as the hop before it.

The wave 1 chain crosses the platform on every hop: the case and its allocation in rwb-case, the ledger in rwb-source-data, the decision record in rwb-decision, the authorisation answer in rwb-access, the file and its manifest in rwb-integration. So the defects this harness catches are the ones no single service test can see: an owner that answers a shape its contract does not allow, a hop that quietly grows a second owner, a decision record written after the state change instead of in the same transaction (R-UNI-39, Principle 5), a stale ACE data product read as if it were today's, a notice that leaves without its document reference, a file built twice for one business date, and a repeat of the same run that produces a second business effect.

The harness is also the cheapest place to hold the wave entry check. The alternative is a manual walk-through per wave, which proves the behaviour once for one person on one day and leaves no evidence the release can be judged on. The report this harness produces is keyed by story and by business date, holds one trace per run, names the contract version of every hop, and holds the pass or fail the gate reads.

It meets REQ-CWC-001, REQ-CWC-002, REQ-CWC-007, REQ-CWC-010, REQ-DCM-007, REQ-DRI-004, REQ-DRI-005, REQ-OCC-001, REQ-ILG-005, REQ-RDF-009, REQ-ACA-005 and REQ-RDF-012 at the integration level, and leaves every business rule and every screen behaviour with the owning stories. The journey's business rules are R-UNI-39, R-UNI-40, R-UNI-24, R-UNI-33 and R-UNI-34, which the owning services run and the harness only asserts.

### 3. Preconditions

- The harness repository, its environment and its namespace: Not specified in the source documents (GAP-0385; ASM-0559). The run is in SIT against the wave 1 services, the Temporal namespace `rwb-recovery`, the wave 1 topics with their retry and `.dlt` topics, and the schema registry.
- The synthetic set of the harness RWB-ITG-W1J01-ITG is loaded for business date 2026-11-25, the WIN notice date of RWB-E1-055: the ACE batch rows of the date, the synthetic accounts, customers, contact points and relations, and the synthetic case set (GAP-0385; ASM-0559).
- Case `RW-2026-000123` has entered from the daily case list, is at status New and carries its product and its account; the case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002 (GAP-0385; ASM-0559).
- `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1` and `rwb.case.CaseAllocated.v1` are already on their topics for the seeded set, so the harness starts its run from a state the owners themselves produced and never fabricates an event.
- The published contracts of P1, P2, P3, P4, P5, P6, P7, P9 and P10 are in the contract registry of the run and their versions are pinned in the report; one stub set is generated from each contract, so the journey runs from Day 1 before the wave 1 app stories are live.
- The business date under test is fixed at 2026-11-25 and every clock the journey asserts is read from the owner, never from the harness. The measures hop runs at 01:30 on 2026-11-26 for business date 2026-11-25, the cadence JOB-15 uses.
- The agent `INTAKE` is approved at version `INTAKE@P1/PR1` in SHADOW mode, and the demand template of the notice hop is approved for the product group of the seeded case; both are read through the owning contract and never set by the harness.
- The evidence format, the evidence retention, the wave gate name and any threshold beyond all-green: Not specified in the source documents (GAP-0385; ASM-0560).
- The gateway-bff composite route path and its merge order: Not specified in the source documents (GAP-0385; ASM-0559).
- The P10 agent-run start path is not an operation of the Ownership Map: Not specified in the source documents (GAP-0385; ASM-0559).
- No production data is read, copied or connected to; every account, person key, case number, notice and file in the run is synthetic.
- No build dependency and no contract dependency: the story is Day 1 (§R5.7 rule 1 and rule 6) against the stub set, with each stub replaced by the real owner as its wave 1 story lands.

### 4. Flow

1. Harness: asserts the seeded set for business date 2026-11-25 — the case `RW-2026-000123` at status New with its product and account, the readiness of the set, and `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1` and `rwb.case.CaseAllocated.v1` already on their topics — and reads the freshness of the seeded data products through `GET /api/recovery/source-data/v1/data-products/freshness`.
2. P3: `GET /api/recovery/case/v1/cases` with the case-number search and `GET /api/recovery/case/v1/cases/{caseId}` return the case, its accounts, its queue and its owner; the allocation the harness asserts is the state the owner returns and never a state the harness sets.
3. P5: the harness posts a synthetic document through `POST /api/recovery/document/v1/cases/{caseId}/documents`, which returns the upload link; `DocumentIntakeWorkflow` runs the OCR, classify and extract steps; `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` arrive on `rwb.document.events.v1`; and `GET /api/recovery/document/v1/cases/{caseId}/documents` shows the document attached with its extracted fields.
4. P3: the document-received transfer rule moves the case (REQ-CWC-010); the harness calls `POST /api/recovery/case/v1/cases/{caseId}/transfer` with a reason code, `rwb.case.CaseTransferred.v1` arrives on `rwb.case.events.v1`, and the case read shows the new queue and owner.
5. P7: every decision of the run writes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, and `GET /api/recovery/decision/v1/decision-log` returns one record per decision with the rule ID and version, append-only and hash-chained.
6. P10: the harness starts `AgentRunWorkflow` on queue `rwb-agent` through the P10 contract with the case-intake agent `INTAKE` at version `INTAKE@P1/PR1` in SHADOW mode, consumes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, and reads `GET /api/recovery/agent/v1/admin/agent-runs` and `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`; the run recommends and the case state does not move. The start path of the run is Not specified in the source documents (GAP-0385; ASM-0559).
7. P6: the harness requests a demand notice through `POST /api/recovery/comms/v1/cases/{caseId}/notices` on an approved template, consumes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1`, and reads `GET /api/recovery/comms/v1/notices/{noticeId}`; the notice carries its document reference and no personal data leaves in the event.
8. P2: the harness opens the Airflow 16:00 WIN file window on 2026-11-25 — the JOB-10 path of RWB-E1-055, with the P6 `NoticeDispatchWorkflow` and the P2 `deliverFile` activity — consumes `rwb.integration.FileDelivered.v1` on `rwb.integration.events.v1`, and reads `GET /api/recovery/integration/v1/admin/outbound-items` for one file with its manifest (fileId, batchId, sha256, record count) holding the notice once.
9. P9: the harness triggers the JOB-15 measures run once for 01:30 on 2026-11-26 for business date 2026-11-25 with the same input the cadence uses, consumes `rwb.reporting.ReportPublished.v1` on `rwb.reporting.events.v1`, and reads `GET /api/recovery/reporting/v1/reports/measures` for the baseline of the date.
10. P1: the ledger read `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`, or `GET /api/recovery/source-data/v1/data-products/{productCode}/records` where the seeded records are asserted instead, holds one entry per hop in order; the harness posts nothing to the ledger itself.
11. P4: every call is authorised through `POST /api/recovery/access/v1/authorise`; the refusal path is a role without the right, which answers MSG-P4-002, and the response masks the personal fields of the case (REQ-ACA-005).
12. Harness: asserts the trace of the run — one owner per hop, one hop and a 2 s budget with a circuit breaker per downstream, no cross-schema read, no retired monolith base, and the case record composition through the gateway-bff composite route (DP-19). The composite route path and its merge order are Not specified in the source documents (GAP-0385; ASM-0559).
13. Harness: returns to the same seeded state and runs the journey again for 2026-11-25; the report is the same assertion by assertion, and no second case, allocation, transfer, document, notice, file or measure is created and the ledger and the decision log hold no duplicate entry.
14. Harness: publishes the per-run evidence report keyed by story and business date with the contract version of every hop, and holds the wave gate that reads every wave 1 harness result recorded for 2026-11-25 and passes the release only when all are green; one red result fails the release and names the harness and the hop.

The harness never writes another owner's table and never calls an owner through another owner: every assertion is made on a contract response or on an event, and every write it needs is a call to the owner's own operation.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A hop answers a shape its published contract does not allow | The run stops at that hop before any assertion of the next hop; the report names the owner, the operation and both contract versions, and the state of the earlier hops is unchanged | None | TC-W1J02-06-ITG |
| X2 | A hop does not answer inside the 2 s budget | The run fails at that hop and names it; the report holds the elapsed time and the contract version, and the earlier state is unchanged | MSG-GEN-006 | TC-W1J02-07-ITG |
| X3 | The decision record of a hop cannot be written | Nothing moves: the state change, the record and the outbox row are one transaction, so the hop fails and the run is reported failed, never passed (R-UNI-39, Principle 5) | MSG-P7-003 | TC-W1J02-08-ITG |
| X4 | A role without the right calls a hop | The hop is refused and the run fails; nothing is written and the refusal carries the message, not an empty answer | MSG-P4-002 | TC-W1J02-09-ITG |
| X5 | An ACE data product behind a hop is stale for the business date | The hop does not treat the stale product as today's; the run fails and the report names the product and the date it carries | MSG-P1-001 | TC-W1J02-10-ITG |
| X6 | The same request reaches a hop twice for the same business date | The owner's inbox or its idempotency key produces one effect and the repeat is counted (R-UNI-40); no second case, transfer, document or notice exists and the lock route of R-UNI-33 and R-UNI-34 is not entered | None | TC-W1J02-11-ITG |

The report text of a failed run is for the wave entry check and is not part of the message standard. The harness produces none of these messages itself: it asserts the message the owning service returns. The business messages the journey produces are asserted as data on the owners' answers and are listed in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stub set of the harness RWB-ITG-W1J01-ITG from Day 1; it waits for no wave 1 build, and each stub is replaced by its owner as the owner lands |
| Negotiable | The seed, the fixed business date, the evidence format and the gate thresholds are configuration agreed at the wave entry check, not business values in code |
| Valuable | The wave 1 journey is proved as a whole before the release is accepted, which is the outcome no per-service test can give |
| Estimable | One harness runner, one stub set, one owner client, one event probe, seven probes for the document, transfer, agent, notice, outbound-item, measures and ledger hops, one evidence report and one gate |
| Small | Fits in one iteration with its tests |
| Testable | Each scenario of section 7 is one automated run with a machine-checkable result, and a repeated run must reproduce it |

### 7. Acceptance criteria

```gherkin
Feature: Wave 1 v5 journey end to end - integration harness

  Background:
    Given the business date under test is 2026-11-25
    Given the synthetic set of RWB-ITG-W1J01-ITG is loaded for 2026-11-25 and case "RW-2026-000123" has entered from the daily case list at status New
    Given the published contracts of rwb-source-data, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-reporting, rwb-agent and rwb-integration are in the contract registry with a stub set generated from each
    Given every account, person key, case number, notice and file in the run is synthetic

  Scenario: AC1 The journey runs green for one business date (new, D-RCV-60)
    Given case "RW-2026-000123" is at status New with its product and its account
    When the harness runs the journey for business date 2026-11-25 across the nine owners
    Then GET /api/recovery/case/v1/cases with the case-number search and GET /api/recovery/case/v1/cases/{caseId} return the case, its accounts, its queue and its owner
    And the allocation the owner returns is the state the harness asserts
    And the synthetic document is posted, DocumentIntakeWorkflow runs, and the document is attached with its extracted fields
    And the document-received transfer moves the case and the case read shows the new queue and owner
    And GET /api/recovery/decision/v1/decision-log returns one record per decision with the rule ID and version
    And the agent "INTAKE" run completes in SHADOW on queue "rwb-agent" and the case state does not move
    And the demand notice is generated on an approved template with its document reference
    And the 16:00 WIN file of 2026-11-25 is delivered once with its manifest
    And the 01:30 measures run of 2026-11-26 publishes the baseline of 2026-11-25
    And the ledger read holds one entry per hop in order
    And the run is green with one trace

  Scenario: AC2 Each hop is one owner, one hop, a 2 s budget (new, D-RCV-60)
    Given the harness records the trace of the run
    When the harness reads every hop from the trace
    Then each hop calls exactly one owner and no owner calls a second owner inside the hop
    And each call answers inside the 2 s budget with a circuit breaker per downstream
    And no hop reads another owner's schema, and every read names a published operation
    And the case record composition is read through the gateway-bff composite route
    And no call uses the retired monolith base (DP-13)

  Scenario: AC3 A forced failure names the hop and leaves the earlier state unchanged (new, D-RCV-60)
    Given the document hop or the notice hop is forced to answer a shape its contract does not allow
    When the harness runs the journey for business date 2026-11-25
    Then the run stops at that hop and names the owner, the operation and both contract versions
    And the case, the allocation and the ledger carry the state they carried before the hop
    And the run is reported failed and is never reported passed
    And the evidence report names the hop that failed

  Scenario: AC4 A repeated run produces the same evidence and no duplicate business effect (new, D-RCV-60)
    Given the first run of the journey ended green for business date 2026-11-25
    When the harness returns to the same seeded state and runs the journey again for 2026-11-25
    Then the evidence report is the same as the first run on every assertion it holds
    And no second case, allocation, transfer, document, notice, file or measure is created
    And the ledger and the decision log hold no duplicate entry for the journey

  Scenario: AC5 The wave gate fails the release on one red harness result (new, D-RCV-60)
    Given the wave gate reads every wave 1 harness result recorded for business date 2026-11-25
    When one wave 1 harness result is red
    Then the gate reports the release as failed and names the red harness and the hop that failed
    And the gate reports the release as passed only when every wave 1 harness result is green
```

The five criteria are new for this harness and restate no app criterion. The criteria of the wave 1 services are owned by their own stories; the notice/WIN hop and the measures hop are asserted here only as hops of the wave 1 chain, and the sibling harness stories RWB-ITG-E1055-ITG and RWB-ITG-E1013-ITG own their detail.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily case list once the ACE batch for ALS is complete | REQ-CWC-001 |
| BR2 | Each case carries a case ID in the form RW-YYYY-NNNNNN, issued once, never reused, and printed on every letter and document | REQ-CWC-002 |
| BR3 | Every new case is placed in a queue and assigned to a person by rule, and no case is allocated by hand as a matter of course | REQ-CWC-007 |
| BR4 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code | REQ-CWC-010 |
| BR5 | A classified document attaches to its case without a person doing it | REQ-DCM-007 |
| BR6 | Records are written for case creation, owner assignment, case transfer and document attachment | REQ-DRI-004 |
| BR7 | No action proceeds if its decision log entry cannot be written; the record, the state change and the outbox row are one transaction, append-only and hash-chained | REQ-DRI-005; R-UNI-39 |
| BR8 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying | REQ-OCC-001 |
| BR9 | Every action the Workbench takes on a case writes to the ledger as it happens: case creation, allocation, transfer, escalation, document attachment and decisions taken | REQ-ILG-005 |
| BR10 | Every data product carries a freshness stamp taken from the ACE batch record, and every decision records the freshness of the data it used; a stale data product is never read as today's | REQ-RDF-009; MSG-P1-001 |
| BR11 | Personal data is masked by role on every screen and in every agent call | REQ-ACA-005 |
| BR12 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe | REQ-RDF-012 |
| BR13 | The same request twice for the same business date produces one effect and the repeat is counted; an unacknowledged outbound item is retried and reaches the exception queue only after the retry limit | R-UNI-40; R-UNI-33; R-UNI-34 |
| BR14 | A booked decision corrected after the event is a correcting record naming the original and never an overwrite | R-UNI-24 |

The harness asserts these fourteen rules against the owners and the published contracts; it re-implements none of them and changes no BR row.

### 9. State transitions

The harness changes no case, document, notice, file, measure or decision state of its own. Every move below is made by the owner when the harness calls the owner's published operation, or when the owner's workflow reacts to an event the harness caused. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| The case exists at status New with its product and its account | rwb-case, JOB-02 case creation from the daily case list | The case read and the case-number search carry the case, its product and its account (TC-W1J02-01-ITG) |
| The case is allocated to a queue and an owner | rwb-case, JOB-03 morning allocation and the allocation package | The case read carries its queue and its owner, and `rwb.case.CaseAllocated.v1` is on the topic (TC-W1J02-01-ITG) |
| The document is stored and attached with its extracted fields | rwb-document, `DocumentIntakeWorkflow` and JOB-12 document intake | The document read shows the document on the case with its extracted fields; DocumentStored and DocumentFieldsExtracted are on the topic (TC-W1J02-01-ITG) |
| The case moves to the new queue and owner after the document | rwb-case, the transfer package on the document-received trigger (REQ-CWC-010) | The transfer answer and the case read carry the new queue and owner, and `rwb.case.CaseTransferred.v1` is on the topic (TC-W1J02-01-ITG) |
| Every decision of the run is recorded once, with its rule ID and version | the owner of each hop, in the same transaction as its state change | The decision-log read returns one record per decision, append-only and hash-chained (TC-W1J02-01-ITG, TC-W1J02-08-ITG) |
| The agent run completes in SHADOW and the case does not move | rwb-agent, `AgentRunWorkflow` on queue `rwb-agent` | The run listing and the agent-output read carry the run at mode SHADOW, AgentRunCompleted is on the topic, and the case read before and after is the same (TC-W1J02-01-ITG) |
| The notice is generated with its document reference | rwb-comms, the notice generation path on an approved template | The notice read carries state Generated, the template version and the document reference; NoticeGenerated is on the topic without personal data (TC-W1J02-01-ITG) |
| One WIN file of the business date carries the notice once | rwb-comms and rwb-integration, JOB-10 with `NoticeDispatchWorkflow` and `deliverFile` | The outbound-item read carries one file with its manifest; FileDelivered is on the topic (TC-W1J02-01-ITG) |
| The baseline of the business date is published | rwb-reporting, the JOB-15 01:30 measures run | The measures read carries the baseline of 2026-11-25; ReportPublished is on the topic (TC-W1J02-01-ITG) |
| A hop forced to answer a shape its contract does not allow | the harness, on the stub set | The run stops at the hop and the earlier state is unchanged (TC-W1J02-06-ITG) |
| A decision record that cannot be written | the owner of the hop, whose transaction rolls back | Nothing moved and the run is failed (TC-W1J02-08-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-OFF, recovery officer | The synthetic user the harness drives: reads and drives the case through the owning contracts within the scope of the seeded queue |
| RW-CASEOWN, case owner | Reads the case, its queue, its owner and its ledger entry of the same seeded case |
| RW-TEAMMGR, team manager | Reads the same evidence across the queue; changes nothing |
| RW-AUDIT, internal audit | Reads the decision log and the ledger of the journey; changes nothing |
| RW-PLATADM, platform administrator | Reads the outbound item of the WIN file and the measures of the date the run asserts; resends nothing and reruns nothing by hand |
| QA lead | Owns the seeded data, the fixed business date, the stub set, the evidence format and the wave gate |
| Integration lead | Owns the harness code, the trace assertions and the swap from a stub to the real owner |
| The owning services' identities | rwb-source-data, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-reporting, rwb-agent and rwb-integration make every state change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; approvals inside the journey are the approval stories' |

Authorisation is answered on every call by `POST /api/recovery/access/v1/authorise`, and the harness asserts both the allow path for RW-OFF in scope and the refusal path for a role without the right (MSG-P4-002). The response masks the personal fields of the case, which the harness asserts as mask markers and never as values.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-005 | recovery_case | id, case_no, product_group, status | Read through the P3 contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 contract |
| DF-CAS-013, DF-CAS-016 | recovery_case | entry_date, total_outstanding_at_entry | Read through the P3 contract |
| DF-CAS-017 | recovery_case | prescription_date | Read through the P3 contract |
| DF-CAS-024, DF-CAS-027 | case_account | case_id, is_primary | Read through the P3 contract |
| DF-CAS-031, DF-CAS-032, DF-CAS-033 | case_party | case_id, person_key, party_role | Read through the P3 contract |
| DF-WRK-019, DF-WRK-023 | task | task_code, owner_role | Read through the P3 contract |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-008 | document | id, case_id, document_type, review_status | Written by rwb-document through `POST /cases/{caseId}/documents`, read back |
| DF-DOC-011 | document | the extracted field set of the document | Read through the P5 contract |
| DF-REF-046, DF-REF-047 | template | template_code, template_version | Read through the P6 contract |
| DF-LEG-015, DF-LEG-016, DF-LEG-017, DF-LEG-018 | notice | id, case_id, document_id, notice_type | Read through the P6 contract |
| DF-LEG-019, DF-LEG-021, DF-LEG-022 | notice | sent_date, callback_date, delivery_status | Read through the P6 contract |
| DF-LEG-033 | notice | dispatch_file_id | Read through the P6 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields, including rule ID, rule version and the hash chain | Read through the P7 contract |
| DF-INT-002, DF-INT-004, DF-INT-005, DF-INT-006, DF-INT-011 | interaction | case_id, occurred_at, channel, direction, summary | Read through the P1 ledger operation |
| DF-RPT-032 to DF-RPT-040 | measure_definition | measure_code, definition_version, data_product | Read through the P9 contract |
| DF-RPT-041 to DF-RPT-052 | measure_snapshot | business_date, value, case_count, is_baseline, frozen, published_at | Read through the P9 contract |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, case_id, autonomy_mode, status, output, confidence, data_as_of | Read through the P10 contract |

Field IDs are those of the Logical Data Model and Data Dictionary and are copied unchanged from the wave 1 stories that own them. The harness owns no table and writes no row directly: it reads through the owner's contract, and its only writes are the document it posts, the transfer it requests and the notice it requests, each through the owner's own operation (DP-01). Test data is synthetic; no production case, party, document or notice is copied, and no personal data is written to a report. The manifest fields of the WIN file (fileId, batchId, sha256, record count) are read from the P2 outbound-item answer and are held as references only.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner: it serves no operation, opens no port a service calls and publishes no endpoint. The names reserved for P2 rwb-integration — the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` — are consumed here as the owner's contract and are not provided by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The case-number search for the seeded case (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its accounts, its queue and its owner, read before and after each hop (AC1, AC3) |
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 rwb-case | The document-received transfer of the case with a reason code (AC1) |
| POST | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Posts the synthetic document and returns the upload link (AC1, AC3) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The document attached to the case with its extracted fields (AC1, AC3) |
| POST | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | The demand notice on an approved template (AC1, AC3) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice state, its template version and its document reference (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | One record per decision with the rule ID and version, append-only and hash-chained (AC1, X3) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | The shadow run of agent `INTAKE` with its mode, version and data date (AC1) |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | The recommendation of the shadow run, read and never acted on (AC1) |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The baseline of business date 2026-11-25 (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The WIN file of 2026-11-25 with its manifest and its delivery state (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness stamp of the seeded data products, and the stale answer of X5 (AC1, X5) |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions`, or `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The interaction ledger with one entry per hop in order; the records path is read where the seeded data product records are asserted instead (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on every call, including the refusal path (X4) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream; where a screen would compose several owners, the harness calls the gateway-bff composite route. The composite route paths and their merge order are Not specified in the source documents (GAP-0385; ASM-0559).

The harness starts nothing through a REST operation of P10 for the agent run: the run start path is Not specified in the source documents (GAP-0385; ASM-0559), and the run is asserted through the two P10 reads above and through `rwb.agent.AgentRunCompleted.v1`. No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owners' events and writes its evidence report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | What the harness asserts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The readiness of the seeded batch for 2026-11-25, where the environment replays it for the set |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Exactly one creation fact for the case, keyed by caseId, with the case number of REQ-CWC-002 and no personal data |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | The allocation fact that matches the queue and owner the case read returns |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | One transfer fact for the document-received transfer, with the reason code |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | The storage fact of the posted document, keyed by caseId |
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` | P5 rwb-document | The extraction fact behind the fields the document read returns |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | all 19 services | One record per decision of the run, arriving before the record is read from the central ledger |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | One completion fact for the shadow run of agent `INTAKE`, with the case ID and the mode |
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 rwb-comms | One generation fact per notice with the notice ID, the case ID and the template version, and no personal data |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | One delivery fact for the WIN file of 2026-11-25 |
| `rwb.reporting.ReportPublished.v1` | `rwb.reporting.events.v1` | P9 rwb-reporting | The publication fact of the measures run for business date 2026-11-25 |

The events carry IDs and business facts only, keyed by caseId, and the harness asserts the absence of personal data in each one (DP-09). Order per case is guaranteed by the case key, and every state the harness asserts is read from the owner's contract and never reconstructed from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow of its own, adds no activity and owns no task queue. It exercises the existing workflows of the wave 1 owners and asserts their effects through the owners' contracts and topics:

| Name | Type | Task queue | What the run exercises |
|---|---|---|---|
| `CaseWorkflow` | Workflow, owned by P3 | `rwb-case` | The parent of the seeded case; the run observes that each hop reaches it and changes no state of its own |
| `DailyCaseRun` | Workflow, owned by P3 | `rwb-case` | JOB-02 case creation and the JOB-03 allocation step that produced the seeded case and its queue and owner |
| `DocumentIntakeWorkflow` | Workflow, owned by P5 | `rwb-document` | The OCR, classify and extract steps of the posted document, and the two document facts |
| `NoticeDispatchWorkflow` | Workflow, owned by P6 | `rwb-comms` | The notice set of the business date in the WIN file window |
| `AgentRunWorkflow` | Workflow, owned by P10 | `rwb-agent` | The shadow run of agent `INTAKE` at version `INTAKE@P1/PR1`; the start path of the run is Not specified in the source documents (GAP-0385; ASM-0559) |
| JOB-15 measures | Measures run, owned by P9 | `rwb-reporting` | The measures publication of business date 2026-11-25, with `snapshot(page)` and `buildRegulatoryExtract` |
| JOB-11 outbox relay | Relay, every service | every service's queue | The outbox row of each hop reaching its topic once |

The harness never starts, signals or terminates a workflow it does not need to start: it triggers the JOB-15 run once with the same input the cadence uses, opens the WIN window the way the Airflow task does, and asserts every other effect through the contracts and the topics (DP-10, DP-12).

#### 12.6 Schedules

None added. The Schedules of the run belong to their owners and are exercised on business date 2026-11-25 or the run that follows it:

| Schedule or start | Cadence | Owner | Legacy reference |
|---|---|---|---|
| JOB-02 case creation and JOB-03 morning allocation | AceDataReady for the business date, then by 07:00 | P3 rwb-case | JOB-02, JOB-03 |
| JOB-10 WIN notices | Daily 16:00, Airflow file window with workers | P6 rwb-comms with P2 rwb-integration | JOB-10 |
| JOB-12 document intake | Every 15 minutes in business hours, event + KEDA workers | P5 rwb-document | JOB-12 |
| JOB-15 reporting extract | Daily 01:30, Airflow trigger, no data lake | P9 rwb-reporting | JOB-15 |
| JOB-11 outbox sender | Every minute | every service | JOB-11 |

The harness creates, moves and owns no Schedule and no cron; it holds the business date with its own clock control and records every trigger it makes in the run report.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). It reads the case through rwb-case, the document through rwb-document, the notice and template through rwb-comms, the decision record through rwb-decision, the measures through rwb-reporting, the run through rwb-agent, the file through rwb-integration, the ledger and freshness through rwb-source-data (DP-18) and the authorisation answer through rwb-access; it never reads another owner's tables and never writes a row.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for P1 rwb-source-data | `GET /data-products/freshness`, `GET /cases/{caseId}/interactions`, `rwb.source-data.events.v1` | Day-1 run of the seeded set, the freshness read and the ledger read, and the stale product of X5 |
| WireMock stub for P3 rwb-case | `GET /cases`, `GET /cases/{caseId}`, `POST /cases/{caseId}/transfer`, `rwb.case.events.v1` | Day-1 run of the case reads, the allocation state and the transfer hop |
| WireMock stub for P4 rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path of X4 |
| WireMock stub for P5 rwb-document | `POST /cases/{caseId}/documents`, `GET /cases/{caseId}/documents`, `rwb.document.events.v1` | Day-1 run of the document hop, and the forced bad shape of AC3 |
| WireMock stub for P6 rwb-comms | `POST /cases/{caseId}/notices`, `GET /notices/{noticeId}`, `rwb.comms.events.v1` | Day-1 run of the notice hop, and the forced bad shape of AC3 |
| WireMock stub for P7 rwb-decision | `GET /decision-log`, `rwb.decision-record.v1` | Day-1 run of the decision records and the forced decision-record failure of X3 |
| WireMock stub for P9 rwb-reporting | `GET /reports/measures`, `rwb.reporting.events.v1` | Day-1 run of the measures hop |
| WireMock stub for P10 rwb-agent | `GET /admin/agent-runs`, `GET /cases/{caseId}/agent-outputs`, `rwb.agent.events.v1` | Day-1 run of the shadow agent hop |
| WireMock stub for P2 rwb-integration | `GET /admin/outbound-items`, `rwb.integration.events.v1` | Day-1 run of the WIN file hop and its manifest |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The report names for every hop whether the answer came from the stub or from the real owner. The evidence format, the evidence retention, the wave gate definition and its thresholds, and the seeded identifier set are Not specified in the source documents (GAP-0385; ASM-0559, ASM-0560).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 15 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget and a breaker per downstream, composed through gateway-bff where a screen would (AC1, AC2, X1, X2, X4) |
| Kafka | None published; `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.document.DocumentStored.v1`, `rwb.document.DocumentFieldsExtracted.v1`, `rwb.decision-record.DecisionRecorded.v1`, `rwb.agent.AgentRunCompleted.v1`, `rwb.comms.NoticeGenerated.v1`, `rwb.integration.FileDelivered.v1` and `rwb.reporting.ReportPublished.v1` consumed for assertion (AC1) |
| Temporal | None added; `CaseWorkflow` and `DailyCaseRun` on `rwb-case`, `DocumentIntakeWorkflow` on `rwb-document`, `NoticeDispatchWorkflow` on `rwb-comms`, `AgentRunWorkflow` on `rwb-agent`, the JOB-15 measures run on `rwb-reporting` and the JOB-11 outbox relay exercised (AC1) |
| File | None. The harness reads and writes no file exchange; the WIN file is an outbound item of P2 with its manifest and is asserted as that item, and the evidence report is a harness artefact and not a service file (AC1) |

### 13. Solution plan

**Pattern application**

None. This story applies no decoupling pattern of §R5.5 and its metadata Patterns applied row is therefore None; it reads each owner through that owner's published contract and records the result.

The harness holds the architecture as an assertion, not as a pattern it applies: it calls one owner per hop on that owner's base and fails a run whose trace shows a call chain deeper than the gateway and one owner (DP-11), it composes through the gateway-bff composite route where a screen would (DP-19), it reads the ledger from rwb-source-data and not from a table (DP-18), it reads the case, the document, the notice, the decision record, the measures, the run, the file and the authorisation answer from their owners, and it fails a run that shows a cross-schema read. The H and C dependencies that the patterns add stay with the service, platform and operations stories that own them: this story carries none of its own, because an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the journey once per business date in hop order, holds the run lock and stops the run at the first failed hop |
| OwnerClient | Harness adapter | Calls the consumed operations of §12.2, one hop each, with the 2 s budget, the circuit breaker and the Idempotency-Key header where the operation requires one |
| StubSet | Fake | The nine WireMock stubs generated from the published contracts of §12.8, each with its version pinned in the report |
| EventProbe | Service | Consumes the eleven events of §12.4 and asserts each fact for the case inside the run window, including the absence of personal data |
| DocumentProbe | Assertion | Asserts the posted document, its storage and extraction facts, and the extracted fields of the document read |
| TransferProbe | Assertion | Asserts the transfer answer, the transferred fact and the new queue and owner of the case read |
| AgentProbe | Assertion | Asserts the shadow run of agent `INTAKE` at version `INTAKE@P1/PR1`, its completion fact and that the case state did not move |
| NoticeProbe | Assertion | Asserts the notice state, its template version and its document reference, and that the event carries no personal data |
| OutboundItemProbe | Assertion | Asserts one WIN file of 2026-11-25 with its manifest (fileId, batchId, sha256, record count) and the notice held once |
| MeasureProbe | Assertion | Asserts the baseline of business date 2026-11-25 and the publication fact of the JOB-15 run |
| LedgerProbe | Assertion | Asserts one ledger entry per hop, in order, with no duplicate after the repeated run |
| TraceAssertion | Assertion | Fails the run on a call chain deeper than the gateway and one owner, on a call outside the 2 s budget, on a retired monolith base and on any cross-schema reference in the trace |
| RepeatProbe | Assertion | Compares a repeated run from the same seed assertion by assertion, and fails on a second business effect or a duplicate ledger or decision entry |
| WaveGate | Reporter | Writes the per-run evidence report keyed by story and business date and holds the pass or fail the wave entry check reads |

**Environment and test data**

- Environment: SIT, with the Temporal namespace `rwb-recovery`, the wave 1 topics with their retry and `.dlt` topics and the schema registry. The harness repository and its namespace are Not specified in the source documents (GAP-0385; ASM-0559). The run is against the §12.8 stub set from Day 1 and against each real owner as its wave 1 story lands.
- Data: the seeded set of RWB-ITG-W1J01-ITG for business date 2026-11-25 and case `RW-2026-000123` with its product and its account; the seeded identifiers beyond these are Not specified in the source documents (GAP-0385; ASM-0559). The case ID keeps the form RW-YYYY-NNNNNN of REQ-CWC-002. No production record is copied.
- Reset: each run starts from the same seeded state and the same fixed business date, so a repeated run is deterministic and the two reports are comparable assertion by assertion.
- Seeding: through the owners' published operations only, never a schema write, so the seeded state is one the services themselves accept.
- Clock: the business date is held at 2026-11-25 for the journey hops and moved to 2026-11-26 only to trigger the 01:30 measures run of the same business date.

**Build steps**

1. Generate the nine stubs from the published contracts, pin each contract version in the report, and prove the journey runs green against the stub set from Day 1.
2. Build JourneyRunner and OwnerClient with the hop order of §4, the 2 s budget, the breaker per downstream and the run lock.
3. Add the precondition and the P3 hops: the seeded set, the freshness read, the case-number search and the case read with its accounts, queue and owner.
4. Add the P5 hop: post the synthetic document, assert the two document facts and the attached document with its extracted fields.
5. Add the transfer hop: the transfer with its reason code, the CaseTransferred fact and the new queue and owner of the case read.
6. Add the P7, P10 and P6 hops: one decision record per decision, the shadow agent run at `INTAKE@P1/PR1` with no move of the case, and the notice with its document reference.
7. Add the P2 and P9 hops: the 16:00 WIN file with its manifest, and the 01:30 measures run with the baseline of the date.
8. Add the P1 ledger probe and the P4 authorisation path, including the refusal path of X4 and the masking assertion of REQ-ACA-005.
9. Add TraceAssertion, the forced bad shape of AC3 and the timeout case of X2, and prove a forced failure names the hop and leaves the earlier state unchanged.
10. Add RepeatProbe and WaveGate: prove the repeated run reproduces the report with no duplicate business effect, and prove the release fails when one wave 1 harness result is red.

**Gate definition.** The gate reads the wave 1 harness results recorded for business date 2026-11-25 and passes the release only when every one of them is green; one red harness fails the release and names the harness and the hop. The gate's name, its evidence format and retention, and any threshold beyond all-green are Not specified in the source documents (GAP-0385; ASM-0560).

**Feature switch.** The harness has no production feature flag and runs in the test environment only. The wave 1 behaviour it exercises is switched on by the wave 1 stories' own flags; where a flag holds a behaviour off, the run reports the hop as skipped and the gate treats a skipped hop as not green.

**Done when.** The eleven test cases of section 16 pass; the journey runs green for business date 2026-11-25 against the stub set on Day 1 and again, hop by hop, against each real owner as its wave 1 story lands; the report holds one trace, the contract version of every hop, whether the hop was a stub or the real owner and every assertion of section 7; and the wave gate fails the release on one red harness result and passes it on all green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | An ACE data product behind a hop is stale for the business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the right calls a hop | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record of a hop cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A system of record behind a hop does not answer inside the budget | {system} is not available. Your request is queued and will be retried. |

The harness produces none of these messages itself: it asserts the message the owning service returns and names the message ID in the report, so a failed run points at an owner, an operation and a message and not only at a date. The four texts are copied unchanged from the wave 1 stories that own them, and this story adds no message ID. Thai text for each message follows decision DL10.

### 15. Screens and states

The harness renders no screen and opens no page. Where a screen would compose several owners, the harness calls the gateway-bff composite route and asserts the answer the screen consumes, so a green hop means the screen has the right data behind it:

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Case at New with its queue and owner | The case answers with its product, its accounts, its queue and its owner, and the case document list carries the posted document with its extracted fields |
| SCR-03 Case record | Case transferred on the document | The case answers with the new queue and the new owner after the transfer, and the ledger entry of the transfer is present |
| SCR-03 Case record | Notice and agent output present | The notice answers with its document reference and the agent output answers as a recommendation at mode SHADOW, with the case state unchanged |
| SCR-44 Interface and job monitor | WIN file of the business date | One outbound item with its manifest and its delivery state, and the JOB-10 run of 2026-11-25 |
| SCR-44 Interface and job monitor | Measures run of the business date | The JOB-15 run of 01:30 on 2026-11-26 for business date 2026-11-25 and its publication |

The screen behaviour of each state stays with the wave 1 app stories. What the wave entry check reads instead is the evidence report, whose format and retention are Not specified in the source documents (GAP-0385; ASM-0560).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-W1J02-01-ITG | AC1, BR1 to BR12 | End to end | Business date 2026-11-25, the seeded set and case `RW-2026-000123` through entry, allocation, document, transfer, decision records, shadow agent, notice, WIN file, measures and ledger |
| TC-W1J02-02-ITG | AC2 | Component | Run trace of the AC1 run; one owner per hop, 2 s budget, no cross-schema read, gateway-bff composition |
| TC-W1J02-03-ITG | AC3 | Integration | The document hop or the notice hop forced to answer a shape its contract does not allow |
| TC-W1J02-04-ITG | AC4 | Integration | The same seeded state run twice on 2026-11-25 |
| TC-W1J02-05-ITG | AC5 | End to end | Every wave 1 harness result recorded for 2026-11-25, one of them red |
| TC-W1J02-06-ITG | X1 | Component | A shape outside the OpenAPI document on one hop, and the contract version mismatch it shows |
| TC-W1J02-07-ITG | X2 | Integration | One hop delayed past the 2 s budget; MSG-GEN-006 and the earlier state unchanged |
| TC-W1J02-08-ITG | X3, BR7 | NFR | Decision record write forced to fail on the hops of the run; no state changes |
| TC-W1J02-09-ITG | X4, BR11 | Component | A role without the right calls a hop; refused with MSG-P4-002 and the personal fields masked |
| TC-W1J02-10-ITG | X5, BR10 | Integration | A data product behind a hop carries the previous business date; MSG-P1-001 |
| TC-W1J02-11-ITG | X6, BR13 | Integration | The same request twice for 2026-11-25; one effect, the repeat counted and no second effect and no exception-queue route |

The full test, with its Given, When and Then, is held under the same test case ID in the wave 1 harness pack; its pack, environment and evidence format are Not specified in the source documents (GAP-0385; ASM-0559).

### 17. Guardrails

- No business value in code: the state names, the template versions, the agent mode and version, the message texts and the expected counts are the owners' data, read by the harness and never held as a copy.
- No personal data in logs, traces, events, workflow inputs, tests or reports: the harness asserts IDs, codes and states only, the events are asserted for the absence of personal data, the authorisation answer is asserted as mask markers, and no production case, party, document or notice is copied.
- No read of another owner's tables: every read and every seed goes through the owner's contract (DP-01), the ledger is read from rwb-source-data (DP-18), and TraceAssertion fails a run that shows a cross-schema reference.
- One hop and a 2 s budget per call with a breaker per downstream, and a composition through gateway-bff where a screen would compose, so the harness fails where a screen would fail (DP-11, DP-19).
- A stub pass is never reported as a real-owner pass: the report names the contract version and whether the hop was a stub or the owner, and the gate treats a skipped hop as not green.
- A forced failure is an input to the run and never a waiver: a red hop is fixed in the owner that owns it or reported as a gap, and the run is reported failed.
- The harness never runs against UAT or production, never calls an outside system directly, and never sets a case, document, notice, file, measure or decision state by hand.
- A repeated run must reproduce the report: a second business effect or a duplicate ledger or decision entry fails the run.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due, created by rule from the daily case list | The seeded set, `GET /api/recovery/case/v1/cases`, `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1` | TC-W1J02-01-ITG, TC-W1J02-10-ITG |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, issued once and never reused | `GET /api/recovery/case/v1/cases` with the case-number search, `GET /api/recovery/case/v1/cases/{caseId}` | TC-W1J02-01-ITG, TC-W1J02-04-ITG |
| REQ-CWC-007 | Every new case is placed in a queue and assigned to a person by rule | `GET /api/recovery/case/v1/cases/{caseId}` queue and owner, `rwb.case.CaseAllocated.v1` | TC-W1J02-01-ITG, TC-W1J02-02-ITG |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on document received among others | `POST /api/recovery/case/v1/cases/{caseId}/transfer`, `rwb.case.CaseTransferred.v1` | TC-W1J02-01-ITG, TC-W1J02-11-ITG |
| REQ-DCM-007 | A classified document attaches to its case without a person doing it | `POST /api/recovery/document/v1/cases/{caseId}/documents`, `GET /api/recovery/document/v1/cases/{caseId}/documents`, the two document events | TC-W1J02-01-ITG, TC-W1J02-06-ITG |
| REQ-DRI-004 | Records written for case creation, owner assignment, case transfer and document attachment | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, `GET /api/recovery/decision/v1/decision-log` | TC-W1J02-01-ITG, TC-W1J02-07-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | The decision-log read before and after each hop and the hash chain | TC-W1J02-08-ITG |
| REQ-OCC-001 | Notices generated from Legal-approved templates with merge fields and no re-keying | `POST /api/recovery/comms/v1/cases/{caseId}/notices`, `GET /api/recovery/comms/v1/notices/{noticeId}`, `rwb.comms.NoticeGenerated.v1` | TC-W1J02-01-ITG, TC-W1J02-03-ITG |
| REQ-ILG-005 | Every action writes to the ledger as it happens | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | TC-W1J02-01-ITG, TC-W1J02-04-ITG |
| REQ-RDF-009 | Every data product carries a freshness stamp and every decision records the freshness it used | `GET /api/recovery/source-data/v1/data-products/freshness`, MSG-P1-001 | TC-W1J02-01-ITG, TC-W1J02-10-ITG |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | `POST /api/recovery/access/v1/authorise`, the masked case and agent-output answers, MSG-P4-002 | TC-W1J02-09-ITG |
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | `GET /api/recovery/reporting/v1/reports/measures`, `rwb.reporting.ReportPublished.v1`, JOB-15 | TC-W1J02-01-ITG, TC-W1J02-05-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The eleven events of §12.4, the consumer inbox dedupe, the schema-registry versioning | TC-W1J02-01-ITG, TC-W1J02-04-ITG, TC-W1J02-11-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The fifteen consumed operations of §12.2, the trace assertion and the preflight contract test | TC-W1J02-02-ITG, TC-W1J02-07-ITG |
| DP-03 | Decision record library and the shared topic | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, the P7 decision-log read | TC-W1J02-01-ITG, TC-W1J02-08-ITG |
| DP-09 | Outbox and inbox library, CloudEvents | The outbox row of each hop and the JOB-11 relay | TC-W1J02-01-ITG, TC-W1J02-11-ITG |
| DP-11 | REST contract with mock, one hop, 2 s timeout | The stub set of §12.8 and the trace assertion | TC-W1J02-02-ITG, TC-W1J02-07-ITG |
| DP-19 | Screen, ace-web | The gateway-bff composite route of the case record and the job monitor | TC-W1J02-02-ITG, TC-W1J02-05-ITG |

The requirements keep their Program BRD text and no requirement is tabulated here that a source does not give. The features of the journey sit with their wave 1 app stories; this table names only the contract element the harness asserts.

### 19. Out of scope

- Any production behaviour: the harness is test and evidence only. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table.
- The wave 1 service behaviour itself, which belongs to the service stories of the nine owners the journey drives.
- The build of the harness RWB-ITG-W1J01-ITG and its synthetic set, which is a precondition here and not a deliverable.
- The sibling wave 1 harness stories and their own loops: RWB-ITG-E1055-ITG for the notice dispatch and proof of delivery and RWB-ITG-E1013-ITG for the baseline measures. This story asserts those two hops only as hops of the wave 1 chain and does not restate their criteria or their test cases.
- The other wave 1 integration loops of the wave, including RWB-ITG-E1018-ITG for case creation and case record, which this journey takes as its starting state rather than re-proving.
- The platform owners' behaviour: the ledger (rwb-source-data), the decision log (rwb-decision), the authorisation answer (rwb-access) and the composite route (the platform edge story RWB-PLT-N001-CON).
- The wave 2 to wave 4 routes and services, which are later waves.
- The production feature flags of the wave 1 stories.
- UAT and production: the harness runs in SIT only.
- The harness environment, the seeded identifier set, the evidence format and retention, the composite route path and the gate name and thresholds: carried as one gap and two assumptions, not decided here.
