# RWB-P7-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-G |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E1020-APP-16); the squad sizes it at refinement |
| Contract version | v1, path `/api/recovery/decision/v1` |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1020-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E1-020, keeping the ALLOCATION and ASSIGNMENT packages in the rule registry, serving a version only while it is in force, and collecting the allocation record of every morning run in the central ledger. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 29 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR), an internal auditor (RW-AUDIT) and the owning service itself**, I want **every allocation and assignment decision of a morning run recorded in rwb-decision as one ledger entry per case and business date, carrying the ALLOCATION rule ID and package version and the ASSIGNMENT rule ID and package version with the queue and owner identifiers, and the compiled models of the two packages served only while their version is in force and only with a matching SHA-256**, so that **every case that was queued and given an owner can be explained the same day from its record, and no run can cite a rule version that rwb-decision never promoted**.

Inside `rwb-decision` this is the registry and record half of the allocation engine:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- The record: `rwb.decision.DecisionRecorded.v1` arrives on the shared topic `rwb.decision-record.v1`, key caseId, and is consumed idempotently into `decision_log_entry`: one entry per case and business date, final call "OWNER_ASSIGNED" when the case was queued and given an owner and "RULE_GAP" when no rule matched it (legacy AC5, AC6).
- The values: rule ID "ALLOC-014" with version "ALLOC-2026.11" in `rule_id` and `rule_version`; assignment rule ID "ASSIGN-007" with version "ASSIGN-2026.11", the queue identifier and the owner identifier in the actions payload. No product group, region, band, amount or case number: identifiers only.
- The read: `GET /api/recovery/decision/v1/decision-log?caseId=...&ruleId=ALLOC-014&from=...&to=...` explains every allocation of a date, with the result of the chain check on each item.
- The registry: the two packages and their row sets live in `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case`; JOB-20 promotes the version whose date has arrived, and the compiled model is served to the owning service only while in force and only with a matching SHA-256.
- No rule is evaluated here: the KieBase, the first-match evaluation and the 300 ms budget stay in the owning service (DP-04), and a version not in force is never a default allocation.

The legacy facts are unchanged: first match wins, the rule ID is the row name, ALLOC-014 sends a MORTGAGE case in BKK to queue MTG-BKK-CO, and the entry cannot be altered once written.

### 2. Business rationale

Legacy RWB-E1-020 promised that every new case is queued and given an owner by rule on the morning it arrives, with the rule ID and package version on the decision log entry, so any allocation can be explained afterwards. In the target that promise has two halves in two services: the allocation, the owner choice and the case update stay with rwb-case; the proof of it, and the authority of the rules it cites, are this service's.

Both mechanisms changed, and each fails silently. The log is no longer one table written by one writer: each service writes a local record in its own transaction and announces it on `rwb.decision-record.v1`, and rwb-decision collects it (ADR-022, DP-03). Rules are no longer read from one shared schema: governance is central here and evaluation is local in the service that owns the model, which fetches a version and verifies its checksum before it swaps it (DP-04, ADR-017). A run can now finish with no ledger entry and no error, or cite a version this service never promoted, and every case still looks allocated.

This story puts the two guarantees back: one entry per case and business date in `decision_log_entry`, carrying both rule identities and the queue and owner identifiers, append only and hash-chained, so the allocations of a date are one read; and one promoted version per package, announced to the owning services, with a model served only while in force and only with a matching SHA-256.

This is the secondary slice of legacy RWB-E1-020. The run, the two evaluations, the assignment methods, the cap, the owner choice, the overflow and exception queues and the case update stay with rwb-case (RWB-P3-E1020-APP); the deviation handler queue with rwb-deviation; the rerun right with rwb-access. It answers REQ-CWC-016, supports REQ-CWC-007, REQ-CWC-008 and REQ-CWC-009 on the record side, and serves NFR-033 and control CTL-03.

### 3. Preconditions

- RWB-P3-E1020-CON is published: the rwb-case allocation contract, with the case read `GET /cases/{caseId}` and the queue read `GET /queues`, their error envelope, the not-found answer and its fake (DP-11). This service reads the case number and the queue code through it at display time and stores neither.
- The `rwb_decision` baseline is in place from the service template: the schema, the six tables of this service, the outbox and inbox objects of DP-09, the base, the topic, the task queue and the chart.
- The database login of rwb-case is Not specified in the source documents (GAP-3207) and is published in RWB-PLT-DB; the queue cap of 150 stays data on the queue (`queue.capacity_cap` and `queue_member.capacity`), with its default delivered through the parameter contract of DP-06.
- `decision_log_entry` exists with `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock, the canonical form and the append-only trigger, and the service role holds INSERT and SELECT with no UPDATE or DELETE grant (RWB-P7-E1008-APP).
- The record contract of RWB-PLT-E1027-CON is published: the record shape, the envelope on `rwb.decision-record.v1`, the idempotency key and the transaction rule, with its fake. The business date travels in that envelope as a record attribute, and the queue and owner identifiers as named members of the actions payload; their field names are Not specified in the source documents (GAP-2441; ASM-4049) and are fixed at the contract review of RWB-PLT-E1027-CON.
- The two versions are loaded, tested and approved: ALLOCATION "ALLOC-2026.11" and ASSIGNMENT "ASSIGN-2026.11", each with its workbook, generated DRL, SHA-256, valid-from date of 2026-11-30 and an approver holding RW-RISK who is not the author (RWB-P7-E1073-APP). This story reads, promotes and serves those rows; it loads none of them.
- The version-state list and LOV-DECISION are in force and are read as reference data through the contract of DP-07; no list value is written in this service's code.
- The workflow kit, the namespace `rwb-recovery` and the task queue `rwb-decision` are provisioned, so JOB-20 can run as a Temporal Schedule (DP-10): the event start on AceDataReady is the primary trigger, with one catch-up Schedule per business date and overlap policy SKIP; the cron expression is Not specified in the source documents (GAP-3208) and is fixed in RWB-P3-E1020-OPS, with 07:00 Asia/Bangkok as the deadline the alert measures.
- The synthetic facts of the tests: case RW-2026-000201 with product group MORTGAGE, region BKK and band B2 in queue MTG-BKK-CO of team MTG-BKK with owner U-03; and case RW-2026-000204 with product group SSME and region NE3, which matches no rule. The business date is 2026-12-01.
- Readers hold Decision log R and an owning service holds a model-owner service identity (TSD P7 T6.1). The authorisation decision is the cached permission decision the service template holds from rwb-access; DP-08 is not in this slice's pattern set, so this story adds no guard of its own.

### 4. Flow

1. Morning run: the JOB-03 step of DailyCaseRun in rwb-case evaluates ALLOCATION and then ASSIGNMENT locally, gives case RW-2026-000201 queue MTG-BKK-CO and owner U-03, and writes its record with the case change and the outbox row in one transaction (RWB-P3-E1020-APP).
2. The record leaves as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, key caseId, carrying the decision code, the final call, the rule ID, the rule version, the inputs reference, the actions payload and the actor.
3. rwb-decision: `AllocationRecordIngest` consumes it through the inbox, deduplicating on the event identifier and again on the case and business date.
4. rwb-decision: `AllocationRecordValidator` applies the refusals of this slice and checks the fields an entry cannot be written without: the inputs reference, the final call and the decided time.
5. rwb-decision: `LedgerAppender` appends one `decision_log_entry`: the decision code the record carries and final call "OWNER_ASSIGNED", `rule_id` "ALLOC-014", `rule_version` "ALLOC-2026.11", the inputs reference, the decided time, the actor, and an actions payload holding "ASSIGN-007", "ASSIGN-2026.11", the queue identifier and the owner identifier. The chain columns come from the ledger's chain.
6. rwb-decision: a case that matched no rule arrives with final call "RULE_GAP", no rule ID and no rule version, and is appended the same way; the exception queue and the case status are rwb-case's and are recorded here as identifiers at most.
7. rwb-decision: a repeat of the same case and business date appends nothing, answers the first entry's id and adds one to the repeat count for R-UNI-40.
8. Any time: `AllocationDecisionReader` answers the decision-log query with the entries of the date, their rule and version, their final call and, per entry, the result of the recomputed hash chain.
9. 00:01 daily: JOB-20 finds every version whose valid-from date has arrived and whose state is APPROVED, sets it in force, supersedes the version it replaces, writes its own record in the same transaction and publishes `rwb.decision.RulePackageInForce.v1`; on that announcement and on a cache miss an owning service asks for the compiled model, which is served only if the version is in force and the recomputed checksum matches.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record carries a rule ID and an empty rule version | Refused; nothing appended; the refusal is logged with the case ID and the missing field and one incident is raised | MSG-P7-009 with "ruleVersion" | AC5 |
| X2 | A record carries a decision code that is not in LOV-DECISION | Refused as X1, naming the decision code field; nothing appended | MSG-P7-009 with "decisionCode" | AC5 |
| X3 | The same record arrives twice, or the morning run for the date is repeated | One entry for the case and the business date; the first entry's id is answered and the repeat is counted | None | AC3 |
| X4 | The ledger store is unavailable | The append is refused and the read answers with no partial page; the records wait in the producers' outboxes, so none is lost, and the ingest catches up | MSG-P7-003 | AC7 |
| X5 | A model is asked for under a version that is not in force | Refused; no model body; the answer names the package code, the version label and its state | None | AC6 |
| X6 | The recomputed SHA-256 of the stored artifact differs from the recorded one | Refused; no model body; one incident for the version, and the version in force keeps serving | None | AC6 |
| X7 | The chain does not hold for an entry on the page | The entry is returned with the check result false, a warning names it on the page and one incident goes to the Compliance queue; the entry is never hidden | Not specified in the source documents (GAP-2442; ASM-4050) | AC4 |
| X8 | A record carries a decision code of another point in a case's life, for example CASE_CREATED | Not this slice's mapping: the ledger's own ingest appends it (RWB-P7-E1027-APP) and this story adds no entry and no refusal | None | AC8, AC15 |

A package version that is not in force is never a default allocation: where nothing is servable the owning service stops its run with NoPackageInForce and MSG-P3-027 before it touches a case, and this service never hands out an older, a superseded or an unchecked version to fill the gap.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-case contract and its fake (RWB-P3-E1020-CON), the envelope of RWB-PLT-E1027-CON, the `rwb_decision` baseline and the registry rows of RWB-P7-E1073-APP; it calls no rule engine and no other service at run time |
| Negotiable | Nothing business is fixed: the rule IDs, versions, queue codes, caps and methods are rows of the two packages; this story fixes the record and the serving rules |
| Valuable | One read explains every allocation of a date, and no service can fetch a version that was not promoted or does not match its checksum |
| Estimable | One consumer, one validator, one appender, one reader, one model service and one short Schedule workflow |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against the record fixture and the registry fixture, with the synthetic cases the legacy story fixes |

### 7. Acceptance criteria

```gherkin
Feature: Allocation and assignment engine v1, the allocation record and the models in force

  Background:
    Given the rwb-case contract mock returns case "RW-2026-000201" in queue "MTG-BKK-CO" with owner "U-03"
    Given the rwb-case contract mock returns queue "MTG-BKK-CO" with team "MTG-BKK"
    Given package ALLOCATION version "ALLOC-2026.11" is in force from 2026-11-30 with its SHA-256 held
    Given package ASSIGNMENT version "ASSIGN-2026.11" is in force from 2026-11-30 with its SHA-256 held
    Given the business date is 2026-12-01
    Given rule ID "ALLOC-014" is test data; no current source document holds it

  Scenario: AC1 The allocation record carries both rule identities and identifiers only (new, D-RCV-60)
    Given a record arrives for case "RW-2026-000201" with decision code "OWNER_ASSIGNED", rule ID "ALLOC-014", rule version "ALLOC-2026.11" and an inputs reference
    Given its actions payload carries "ASSIGN-007", "ASSIGN-2026.11", the identifier of queue "MTG-BKK-CO" and owner "U-03"
    When the ledger consumes the record for business date 2026-12-01
    Then one decision_log_entry exists for case "RW-2026-000201" and 2026-12-01 with final call "OWNER_ASSIGNED", rule_id "ALLOC-014" and rule_version "ALLOC-2026.11"
    Then the entry carries chain_seq, prev_hash, entry_hash and the decided time
    Then the entry holds no product group, no region, no exposure band, no amount and no case number
    Then the queue code "MTG-BKK-CO" is read from the rwb-case contract when the entry is displayed

  Scenario: AC2 A case no rule matched is recorded as a rule gap (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000204" in the exception queue with no owner
    Given a record arrives for case "RW-2026-000204" with final call "RULE_GAP", no rule ID and no rule version
    When the ledger consumes the record for business date 2026-12-01
    Then one decision_log_entry exists for case "RW-2026-000204" with final call "RULE_GAP" and no rule_id, no rule_version and no owner
    Then it is accepted although it has no rule ID, because the only refused shape is a rule ID with no rule version
    Then the exception queue and the case status stay with rwb-case and no queue value is written by this service

  Scenario: AC3 One entry per case and business date, and a repeat returns the first id (new, D-RCV-60)
    Given the record for case "RW-2026-000201" on 2026-12-01 was appended once and its entry id is known
    When the same record arrives again with the same idempotency key
    When the morning run for 2026-12-01 is repeated and announces the case again
    Then exactly one decision_log_entry exists for case "RW-2026-000201" and 2026-12-01
    Then the ingest answers the first entry's id and adds one to the repeat count for R-UNI-40
    Then the rule version on the entry stays "ALLOC-2026.11" and is not rewritten

  Scenario: AC4 The read explains every allocation of the date, and a break is shown (new, D-RCV-60)
    Given six entries exist for 2026-12-01 with rule "ALLOC-014", one of them with a link that does not hold
    When a reader holding Decision log R calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000201&ruleId=ALLOC-014&from=2026-12-01&to=2026-12-01
    Then the page returns the entries of the date with rule_id, rule_version, final_call, decided_at and the assignment rule and version from the actions payload
    Then five entries carry the check result true and the sixth carries it false, and no entry is dropped
    Then a warning names the sixth entry, one incident is raised for it, and a role without Decision log R is refused with MSG-P4-002

  Scenario: AC5 A record that cannot be trusted is refused and nothing is appended (new, D-RCV-60)
    Given the ledger holds no entry for case "RW-2026-000210" on 2026-12-01
    When a record arrives for it with rule ID "ALLOC-014" and an empty rule version
    Then it is refused with MSG-P7-009 naming "ruleVersion" and nothing is appended
    When a record arrives for it with decision code "D99"
    Then it is refused with MSG-P7-009 naming "decisionCode" and nothing is appended
    Then both refusals are logged with the case ID and the field, and the entry count for the case stays zero

  Scenario: AC6 Only a version in force with a matching checksum is served, and JOB-20 is the only way in (new, D-RCV-60)
    Given package ALLOCATION "ALLOC-2026.11" and package ASSIGNMENT "ASSIGN-2026.11" are in force with their valid-from date of 2026-11-30
    When an owning service asks for the compiled model of "ALLOC-2026.11"
    Then the answer carries the compiled model, the version label "ALLOC-2026.11" and its SHA-256, and no rule is evaluated and no KieBase built here
    Given version "ALLOC-2026.12" of package ALLOCATION is APPROVED with a valid-from date of 2026-12-15
    When an owning service asks for "ALLOC-2026.12" on 2026-12-01
    Then the call is refused, no model body is served, and the answer names the package code, the version label and its state
    When the stored artifact of "ALLOC-2026.11" is altered so that its SHA-256 no longer matches
    Then the call for "ALLOC-2026.11" is refused, no model body is served and one incident is raised for the version
    When JOB-20 runs at 00:01 on 2026-12-15
    Then "ALLOC-2026.12" is in force, "ALLOC-2026.11" is superseded and rwb.decision.RulePackageInForce.v1 is published for the new version

  Scenario: AC7 A ledger that cannot take the append or answer the read leaves no partial entry and no partial page (new, D-RCV-60)
    Given the ledger store is forced unavailable for the whole run
    When a record arrives for case "RW-2026-000201" on 2026-12-01 and the decision log is read for 2026-12-01
    Then the append is refused with MSG-P7-003 and no decision_log_entry is written
    Then the read answers MSG-P7-003 with no partial page and the entry count is unchanged
    Then the record waits in the producers' outboxes and the ingest catches up once the ledger is available, so none is lost

  Scenario: AC8 A decision code of another point in a case's life is not appended by this story (new, D-RCV-60)
    Given a record arrives for case "RW-2026-000201" with decision code "CASE_CREATED"
    When the ledger consumes the record for business date 2026-12-01
    Then this story adds no decision_log_entry and no refusal for the record
    Then the record is appended by the ledger's own ingest in RWB-P7-E1027-APP

  Scenario: AC15 A decision code of another point in a case's life is neither refused nor appended by this story (new, D-RCV-60)
    Given a record arrives for case "RW-2026-000201" with decision code "CASE_CREATED" and no rule ID
    When this service receives the record for business date 2026-12-01
    Then no MSG-P7-009 refusal is issued for the decision code
    Then the record is left to the ledger's own ingest in RWB-P7-E1027-APP and the entry count for the case stays unchanged

  Scenario: AC16 The ledger entry is append only and no rule is evaluated in rwb-decision (new, D-RCV-60)
    Given one decision_log_entry exists for case "RW-2026-000201" and 2026-12-01
    When an UPDATE or a DELETE is issued against that entry
    Then the append-only trigger refuses it and the entry is unchanged
    Then RuleModelService holds no evaluator, working memory or agenda, and the model read evaluates no rule

  Scenario: AC17 The provided operations answer 401, 403 and 404 with no page (new, D-RCV-60)
    Given a reader holding Decision log R and a valid credential
    When a call to GET /api/recovery/decision/v1/decision-log carries no valid credential
    Then the answer is 401 and no page is returned
    When a role without Decision log R calls the same path
    Then the answer is 403 with MSG-P4-002 and no page is returned
    When a call asks for a path the contract does not provide
    Then the answer is 404 and no page is returned

  Scenario: AC18 A retried or timed-out append leaves one entry or none (new, D-RCV-60)
    Given the record for case "RW-2026-000201" on 2026-12-01 was appended once and its entry id is known
    When the producer retries the same record after no answer
    Then exactly one decision_log_entry exists for case "RW-2026-000201" and 2026-12-01 and the first entry's id is answered
    Given the ledger store does not answer within the append time limit (value not specified in the source documents, NEWAC-RWB-P7-E1020-APP-AC18)
    When the record is sent for case "RW-2026-000202" on 2026-12-01
    Then the append is refused, no decision_log_entry is written, and the record waits in the producer's outbox

  Scenario: AC19 A consumed rwb-case call that fails or does not answer writes no queue value (new, D-RCV-60)
    Given the rwb-case contract mock fails the call for case "RW-2026-000201"
    When the ledger consumes the record for business date 2026-12-01
    Then one decision_log_entry exists for case "RW-2026-000201" with the rule ID and rule version from the record
    Then no queue value is written by this service and the failed call is logged with the case ID
```

The thirteen criteria above are new and test only this deliverable: the allocation record in the central ledger, its refusals, its read, and the two packages held and served only while in force. The legacy criteria are owned elsewhere: AC1 to AC9 and AC11 to AC13 are the run and the case update of rwb-case (RWB-P3-E1020-APP); AC10 is the wait on case creation, proved across services by RWB-ITG-E1020-ITG; the deviation branch is rwb-deviation's; the rerun right is rwb-access's. The legacy test cases this story answers are listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every allocation of a morning run is recorded once in the central ledger, one entry per case and business date, with final call "OWNER_ASSIGNED" when the case was queued and given an owner and "RULE_GAP" when no rule matched it | REQ-CWC-016; FSD P7 AC-P7-002-01; legacy AC5, AC6, BR9 |
| BR2 | The entry carries the ALLOCATION rule ID and version in `rule_id` and `rule_version`, and the ASSIGNMENT rule ID and version with the queue identifier and the owner identifier in the actions payload. First match wins and the rule ID is the row name | REQ-CWC-016; CTL-03; legacy BR1 and BR9. The FSD P7 names the same row "ALLOC-MTG-BKK-01" (GAP-2440; ASM-4048) |
| BR3 | A record with a rule ID and no rule version, or with a decision code outside LOV-DECISION, is refused and nothing is appended; the refusal names the field | FSD P7 AC-EXC-P7-002-01 and AC-EXC-P7-002-05; MSG-P7-009 |
| BR4 | An entry is append only and hash-chained: nothing updates or deletes it, and the chain is the record of the order of decisions | FSD P7 AC-P7-001-01; DF-DEC-017, DF-DEC-018, DF-DEC-028; legacy BR7 |
| BR5 | The read names the rule and its version for every allocation of a date, and a break in the chain is shown on the page, never hidden and never dropped, and reported to Compliance the same day | REQ-CWC-016; NFR-033; NFR-035; FSD P7 AC-BG-P7-006-01 |
| BR6 | A decision whose record cannot be written does not proceed, and a read against an unavailable ledger answers with no partial page | Principle 5; R-UNI-39; CTL-06; FSD P7 AC-EXC-P7-002-07; MSG-P7-003 |
| BR7 | An allocation is recorded at most once for a case and a business date: a repeated event or a repeated run gives one entry and the repeat is counted | R-UNI-40; FSD P7 AC-EXC-P7-002-03; legacy AC8 and BR8 |
| BR8 | A model is served only while its version is in force, and only when the recomputed SHA-256 of the stored artifact matches the recorded one | DP-04; ADR-017; RWB-P7-E1073-APP |
| BR9 | No rule is evaluated in rwb-decision: the KieBase, the first-match evaluation and the 300 ms budget stay in the owning service, which keeps its last good model when a new one is refused | DP-04; ADR-017; legacy BR1 and guardrail "one evaluator" |
| BR10 | JOB-20 promotes a version at 00:01 on its valid-from date, supersedes the earlier one and announces the promotion; a version not in force is never a default allocation | REQ-CWC-008; DP-10; FSD P7 AC-P7-007-01 and AC-ALT-P7-007-02 |

How the rules hold in `rwb-decision`: BR1 and BR7 run in the ingest and in the unique key on the case and the business date, so a second delivery finds the first entry and changes nothing. BR2 runs in the mapper, which copies the rule identity as it arrives and derives nothing from a case attribute. BR3 runs before any append, so a refused record leaves the ledger as it was. BR4 runs in the schema, where the append-only trigger refuses an UPDATE and a DELETE. BR5 runs in the reader, which recomputes each hash and compares it with the link before it. BR8 and BR9 run in `RuleModelService` and in what it does not hold: it reads a state and a checksum, serves bytes, and contains no evaluator, working memory or agenda. BR10 runs in `VersionPromotionService` under JOB-20, which moves a state and publishes an event and evaluates nothing.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | an accepted record for a case and a business date | No entry exists for the pair | One `decision_log_entry` at the next `chain_seq`, final call "OWNER_ASSIGNED" or "RULE_GAP" |
| Appended | the same case and business date again | The idempotency key repeats | No change; the first entry id is answered and the repeat counted |
| APPROVED | JOB-20 at 00:01 on the valid-from date | The version passed its load checks and its approver is not its author | In force; the version in force before it is superseded |
| In force | a model fetch | The recomputed checksum matches the recorded one | Served, unchanged |
| In force | a model fetch | The checksum does not match | Refused, no model body, an incident raised; the state is unchanged |
| LOADED, APPROVED, superseded, rolled back or refused | a model fetch | The version is not in force | Refused, the state named in the answer; no model body |

The case state machine is not this service's: rwb-case owns the case status, queue, owner and stage (TSD P7 T4, "No case state machine of its own"), and this slice changes no case state. The load, the checks, the approval and the rollback that move a version between its states are RWB-P7-E1073-APP; this story owns the promotion at 00:01 and the refusal of anything not in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity (SY-DECLOG) | Appends the ledger entry, serves the two models, promotes a version under the Schedule and publishes the announcement |
| SY-CASEWF, case workflow module | Writes the allocation record in its own schema and transaction and announces it; holds no grant on `rwb_decision` |
| RW-TEAMMGR, team manager; RW-CASEOWN, case owner | Read the ledger for their team or their own cases (Decision log R, scope applied) |
| RW-AUDIT, internal audit; RW-COMPLY, Compliance and PDPA officer | Read the ledger with its chain state (Decision log R) |
| RW-RISK, risk and model risk officer | Approves each version through RWB-P7-E1073-APP; this story records the approval and promotes on its date |
| RW-PLATADM, platform administrator | Operates JOB-20, reads the promotion result and the incidents of a refused fetch |
| rwb-case (P3) | Owns the case, queue, owner and the rule row behind the decision; this service holds their identifiers and reads their codes at display |

The authorisation decision is the cached permission decision the service template holds from rwb-access, and each REST operation of this story is checked through the rwb-access authorise check; the path of that check is Not specified in the source documents (DOR-RWB-P7-E1020-APP-6). DP-08 is not in this slice's pattern set, so this story adds no access entry. The refusal shapes are 403 with MSG-P4-002 for a role that holds no Decision log right and 503 with MSG-P7-003 when the ledger cannot be read. The role codes above are rows of the role model in `rwb_access` (TSD P7 T6.1) and are not fixed in code.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id (a value from the record, with no foreign key into `rwb_case`) | Write |
| DF-DEC-003 | decision_log_entry | decision_code (a value of LOV-DECISION carried by the record) | Write |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id ("ALLOC-014"), rule_version ("ALLOC-2026.11") | Write |
| DF-DEC-008, DF-DEC-016, DF-DEC-030 | decision_log_entry | inputs_ref, decided_at, actor_user_id | Write |
| DF-DEC-012 | decision_log_entry | final_call ("OWNER_ASSIGNED" or "RULE_GAP") | Write |
| DF-DEC-014 | decision_log_entry | actions ("ASSIGN-007", "ASSIGN-2026.11", queue identifier, owner identifier) | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key (the case and the business date, as the record carries them) | Write |
| DF-REF-002, DF-REF-003, DF-REF-053, DF-REF-054 | rule_row | rule_id, rule_version, row_order, target_queue_code | Read, as the catalog served with the model |
| Not specified in the source documents (GAP-2439; ASM-4047) | rule_package_version | state, valid_from, approver, generated DRL and content_sha256 | Read; the state is written only by the 00:01 promotion |
| DF-CAS-002, DF-CAS-010, DF-WRK-002 | case and queue, through the rwb-case contract of RWB-P3-E1020-CON | case number, queue identifier, queue code | Read only, at display; never written |

Field IDs are those in the Technical Specification P7 Decision center and log v2 T3.1 and the Logical Data Model and Data Dictionary. `decision_log_entry.case_id` is the only case value in `rwb_decision`: no case number, product group, region, band, amount, queue code or owner name column exists, and no foreign key points into another schema (DP-01). The physical columns of `rule_package_version` and the payload a compiled artifact is served in are Not specified in the source documents (GAP-2439; ASM-4047): the sources fix what a version stores, not its physical form.

### 12. Contract

The base is `/api/recovery/decision/v1` (DP-13), the topic is `rwb.decision.events.v1` (DP-14), the queue is `rwb-decision` and the schema is `rwb_decision`.

#### 12.1 REST operations provided

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/decision-log` | Search the ledger for the allocations of a case, a rule or a date: query `caseId`, `ruleId`, `from`, `to`, `page`, `size`; each item carries `chainVerified`, the result of its chain check, and the page names an entry that fails it | Decision log, right R, scope applied |
| GET | `/rule-models/{packageCode}/{version}` | Serve one compiled model version with its SHA-256 to the owning service that holds the package | A model-owner service identity, under the rule-package contract |

API-P7-006 of the TSD appendix T-A is the decision-log query and carries the same four filters. The model-serving operation is Not specified in the source documents as a provided operation of the Ownership Map, which lists 19 operations without it (GAP-2443; ASM-4051). This story fills the query with the allocation read on the path the ledger story declares and adds no third path: the entry read `GET /decision-log/{entryId}` and the audit export stay with RWB-P7-E1027-APP and legacy RWB-E2-005.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3), under RWB-P3-E1020-CON | The case number shown beside an entry on the page, read at display time | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/queues` | rwb-case (P3), under RWB-P3-E1020-CON | The queue code and team shown for a queue identifier in the actions payload | One hop, 2 s (DP-11) |

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | `rwb.decision.events.v1` | The package code | Catalog v1 fields: packagecode, packageversion, validfrom, versionid, approvedby; identifiers and facts only |

#### 12.4 Events consumed

| Event | Topic | From | Used for | Owner |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | `rwb.decision-record.v1` (shared) | The owning services; the allocations of this story from rwb-case | The append of `decision_log_entry`: decision code, final call, rule ID and version, inputs reference, actions and actor | rwb-decision (P7) |

Consumed through an inbox that deduplicates on the event identifier and again on the case and business date, with the retry and dead-letter topics of DP-09. The envelope is the one RWB-PLT-E1027-CON fixes; how the business date and the queue and owner identifiers are carried in it is Not specified in the source documents (GAP-2441; ASM-4049).

#### 12.5 Workflows and activities

| Name | Kind | Queue | What it does |
|---|---|---|---|
| RulePromotionWorkflow | Workflow | `rwb-decision` | Starts at 00:01, reads the versions due that night, promotes each and asks the activity to announce it |
| PromoteDueVersions | Activity | `rwb-decision` | Sets APPROVED versions whose valid-from date has arrived in force, supersedes the version each replaces, and writes the record and the outbox row in one transaction |

#### 12.6 Schedules

| Job | When | Queue | Mechanism |
|---|---|---|---|
| JOB-20 Rule promote | 00:01 daily, Asia/Bangkok | `rwb-decision` | Temporal Schedule starting RulePromotionWorkflow, which publishes RulePackageInForce (DP-10) |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | The central ledger entry of an allocation and of every other decision announced to this service |
| `rule_package`, `rule_package_version` | P7 (rwb_decision) | The registry and its versions; this story reads both and writes the version state at 00:01 |
| `rule_row`, `rule_test_case` | P7 (rwb_decision) | The parsed catalog of each version, which travels with the model; read only here |
| approval | P7 (rwb_decision) | The waiting approvals of this service; this story reads none of them (RWB-P7-E2013-APP) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case contract fake (RWB-P3-E1020-CON) | The case and queue reads | Case `RW-2026-000201` in queue `MTG-BKK-CO` with owner `U-03`; case `RW-2026-000204` in the exception queue with no owner; a queue answer with team `MTG-BKK`; a not-found and a slow answer past 2 s |
| DecisionRecorded fixture (RWB-PLT-E1027-CON) | The consumed envelope | One accepted allocation record for 2026-12-01; a RULE_GAP record; a duplicate; a rule ID with no version; decision code `D99`; decision code `CASE_CREATED` |
| Registry fixture (RWB-P7-E1073-APP) | `rule_package_version` | `ALLOC-2026.11` and `ASSIGN-2026.11` in force with matching checksums; `ALLOC-2026.12` APPROVED and due on 2026-12-15; a superseded version; a version whose artifact no longer matches its SHA-256 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `GET /decision-log` and `GET /rule-models/{packageCode}/{version}`; `GET /cases/{caseId}` and `GET /queues` at display, one hop within 2 s |
| Kafka | 1 published, 1 consumed | `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`; `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | 1 Schedule, 1 workflow, 1 activity | JOB-20 at 00:01 on queue `rwb-decision`; RulePromotionWorkflow and PromoteDueVersions |
| File | 1 read | The workbook and the generated DRL of a version, read as the claim-check behind the model answer |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `allocationrecord` and `rulemodel`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AllocationRecordIngest | Consumer | Consumes the record through the inbox, deduplicates on the event and on the case and business date, and hands it to the validator |
| AllocationRecordValidator | Service | The refusals and the required fields, before any append |
| LedgerAppender | Service | Maps the record to one `decision_log_entry`, appends it with `chain_seq`, `prev_hash` and `entry_hash` in one transaction, and answers the first entry id on a repeat |
| AllocationDecisionReader | Service | The allocation read with the chain result per item, the warning on a broken link, and the case number and queue code taken from the rwb-case contract |
| RuleModelService | Service | Serves a compiled version only when it is in force and its recomputed SHA-256 matches; serves no evaluator |
| VersionPromotionService | Service | Under JOB-20, promotes the versions due, supersedes the earlier one, writes the record and the outbox row, and publishes the announcement with the package code as the key |

**Database and migrations**

- Writes `decision_log_entry` (append only) and the version state at 00:01; writes no case, queue or owner value.
- Reads `rule_package`, `rule_package_version`, `rule_row` and their catalog projection.
- Index on `(case_id, rule_id, decided_at)` for the read, and a unique key on the idempotency key of the case and business date.
- Per-service migration of DP-15: `V1020_1__allocation_record.sql` adds the two indexes and no column carrying a case attribute. The tables arrive with the baseline and the registry stories; no row is seeded here.

**Configuration and reference data**

- No business value is configured: the package codes, rule IDs, versions, queue codes and caps are rows of the two packages and values of rwb-case; parameters and lists come through DP-06 and DP-07 and none is written in Java.
- Two settings only: the 00:01 time of the Schedule and the two package codes this service holds in the registry.

**Build steps**

1. `AllocationRecordIngest` and `AllocationRecordValidator` against the fixture, with the accepted, the RULE_GAP, the duplicate, the two refusals and the foreign decision code; tests for AC1, AC2, AC3 and AC5.
2. `LedgerAppender` with `chain_seq`, the hashes and the repeat path; tests for AC1 and AC3.
3. `AllocationDecisionReader` with the filters, the chain result and the warning on a broken link; test for AC4.
4. `RuleModelService` with the state check and the checksum comparison, and a schema assertion that `rwb_decision` holds no case attribute column; test for AC6.
5. `VersionPromotionService` and the JOB-20 Schedule, with the record, the outbox row and the event in one transaction, then the display path with the case number and queue code taken from the contract fake; tests for AC1 and AC6.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no build dependency of its own (metadata "Depends on (build)" = None) and builds against the `rwb_decision` baseline, the registry rows and the RWB-P3-E1020-CON fake. The platform H rows and the C rows of the table are the dependencies the patterns add; they are held by the platform and contract stories and are not repeated in the metadata rows, which name the one contract dependency of the legacy key. DP-01, DP-13 and DP-15 are the target shape itself. DP-03 is the record path: the local record of the owning service, the shared topic and the ledger here, with no shared table and no call into rwb-case. DP-04 is the point of this slice: governance central here, evaluation local there, so this service holds no KieBase and serves bytes and states. DP-05, DP-06 and DP-07 are prohibitions: no ACE view is read, and no parameter or list value is written in this service's code. DP-09, DP-10, DP-11 and DP-14 are the mechanism: the inbox dedupe and the keyed announcement, the 00:01 Schedule with no Quartz row, one 2 s hop for the display read, and `rwb.decision.events.v1` supplied by the naming library. DP-19 is the gateway-bff composite route behind the decision log page.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1020-CON and RWB-PLT-E1027-CON stay green, and a SIT week shows one entry per case and business date with both rule identities, a repeated run adding none, a page that names a broken link and hides no entry, and no model served for a version not in force or with a mismatched checksum.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-003 | The ledger cannot take the append or answer the read | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role holds no Decision log right for the action | You cannot {action} here. Your role does not include it. |
| MSG-P3-027 | No version of a package is in force at the owning service | The {table} load was refused: {check}. The version in force is unchanged. |

MSG-P7-009 is written to the service log and the incident and is never shown to a customer; its {field} value is "ruleVersion" or "decisionCode", and its text is the row above. A broken chain on a page carries a warning naming the entry, with the same gap. For MSG-P4-002 the {action} value is "read the decision log". For MSG-P3-027 the {table} value is the package code and the {check} value is "package in force". Every error is an RFC 9457 problem response with `messageId` and `detail` filled; the reads answer 401 without a session, 403 for a role without the right and 503 with MSG-P7-003 when the ledger cannot be read, and a refused model names the package code, the version label and its state without a model body.

### 15. Screens and states

No new screen. The allocation view of SCR-38 Decision log query shows, for one case or one business date, the rule ID and version, the final call, the assignment rule ID and version, the queue, the owner, the decided time and the chain result; the case number and queue code beside them are read from the rwb-case contract at display time. Its states are Loading, Results, Empty, Error and No access; the Empty, Error and No access states, their wording and MSG-P7-003 are Not specified in the source documents (CG-ALL-6904), and a broken link puts a warning at the top and leaves the entry in place. The screen itself, its filters beyond the four query parameters, its paging and its export are legacy RWB-E2-005's, served by the gateway-bff composite route (DP-19), which calls this service for the entries and rwb-case for the case header.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-01 | AC1, BR1, BR2: the allocation leaves one entry naming rule `ALLOC-014` and version `ALLOC-2026.11` | End to end | Case `RW-2026-000201`, product group `MORTGAGE`, region `BKK`, band `B2`, queue `MTG-BKK-CO`; business date 2026-12-01; the FSD row label `ALLOC-MTG-BKK-01` is recorded as the row description of the same row |
| TC-E1-020-02 | AC2, BR2: the entry carries `ASSIGN-007` and `ASSIGN-2026.11` with the owner identifier | End to end | Owners `U-01`, `U-02`, `U-03` with 120, 95 and 140 open cases; `U-03` chosen; cap 150 |
| TC-E1-020-03 | AC3, BR1: a case that found no owner below the cap is still one entry of the date | End to end | Owners at the cap; overflow queue `MTG-BKK-OVF`; the entry names no owner |
| TC-E1-020-04 | AC4, BR1: an overflow case is recorded once with the queue identifier it went to | End to end | `U-01`, `U-02`, `U-03` each at 150 open cases; case `RW-2026-000203` |
| TC-E1-020-05 | AC5, BR1, BR3: a case that matched no rule is `RULE_GAP`, and an unknown decision code is refused | End to end | Case `RW-2026-000204`, product group `SSME`, region `NE3`; exception queue `RWB-EXC`; decision code `D99` |
| TC-E1-020-06 | AC6, BR2, BR5: one entry per allocation with both rule identities, and one page for the date | Contract | Synthetic set of 2026-12-01 against the envelope of RWB-PLT-E1027-CON and the page of the date |
| TC-E1-020-07 | AC7, BR1: a case diverted for a deviation is recorded with no owner and no rule gap; the diversion is rwb-deviation's | End to end | Case `RW-2026-000206`, deviation queue `DEV-HANDLER`, no owner, no rule ID |
| TC-E1-020-08 | AC8, BR7: the same run repeated for 2026-12-01 writes no second entry | End to end | Case `RW-2026-000201` allocated on 2026-12-01, then the run repeated for the same date |
| TC-E1-020-09 | BR10: a night with no allocation and no due version promotes nothing and announces nothing | End to end | No NEW cases on 2026-12-01; no version due at 00:01; zero promotions |
| TC-E1-020-10 | AC10, BR7: a date whose case creation did not run holds no entry, and a late record is appended once | End to end | ALS batch for 2026-12-01 not `COMPLETED`; MSG-P1-001; no record on the ledger |
| TC-E1-020-11 | AC11, BR7: two deliveries of the same decision give one entry | End to end | The same record delivered twice at the same time; repeats counted per R-UNI-40 |
| TC-E1-020-12 | AC12, BR2: an owner one case below the cap is recorded with that owner identifier | End to end | `U-03` at 149 open cases, then at 150 after the case; case `RW-2026-000208` |
| TC-E1-020-13 | AC2, BR1: a queue with no overflow queue leaves the case with the exception queue, recorded with no owner | End to end | Queue `HP-CEN-CO`, no overflow queue, every owner at 150; case `RW-2026-000209` |
| TC-E1-020-14 | BR3, BR5: a role without Decision log R is refused with no entry; the right itself is rwb-access's | Component | Role `RW-REFADM` calls the decision log read and is refused with MSG-P4-002; the same call with Decision log R returns the page |
| TC-E1-020-15 | BR6: a ledger that cannot take the append or answer the read leaves no partial entry and no partial page | NFR | Ledger store forced unavailable for the whole run; MSG-P7-003 on the read; entry count unchanged |
| TC-E1-020-16 | AC6, BR8: a version not in force, or a model whose SHA-256 does not match, is refused and no model is served | Component | Version `ALLOC-2026.11` not in force at 00:01; a version with a mismatched SHA-256; the owning service identity calls the model read |
| TC-E1-020-17 | AC6: the tables of section 12.7 sit in `rwb_decision` and hold no case attribute column (boundary) | Component | Migration `V1020_1__allocation_record.sql` applied to `rwb_decision`; each table of section 12.7 checked for case attribute columns |
| TC-E1-020-18 | AC7, BR6: a ledger that cannot take the append or answer the read leaves no partial entry and no partial page | NFR | Ledger store forced unavailable for the whole run; MSG-P7-003 on the append and the read; entry count unchanged |
| TC-E1-020-19 | AC8: a record with decision code `CASE_CREATED` adds no entry and no refusal in this slice | Component | Case `RW-2026-000201` on 2026-12-01 with decision code `CASE_CREATED`; entry count unchanged |
| TC-E1-020-20 | AC6: only a version in force with a matching SHA-256 is served, and JOB-20 is the only route in | Component | Version `ALLOC-2026.11` in force from 2026-11-30; `ALLOC-2026.12` APPROVED with valid-from 2026-12-15; JOB-20 run at 00:01 on 2026-12-15 |
| TC-E1-020-21 | AC15: a record with decision code `CASE_CREATED` is neither refused nor appended by this story | Component | Case `RW-2026-000201` on 2026-12-01 with decision code `CASE_CREATED` and no rule ID; refusal log and entry count checked |
| TC-E1-020-22 | AC16, BR4, BR9: an UPDATE or a DELETE on a decision_log_entry is refused, and no evaluator is held in rwb-decision | Component | One entry for `RW-2026-000201` on 2026-12-01; UPDATE and DELETE issued; `RuleModelService` checked for evaluator, working memory and agenda |
| TC-E1-020-23 | AC17: calls without a valid credential, without Decision log R, or to an unprovided path answer 401, 403 and 404 | Component | No credential; role `RW-REFADM` without Decision log R; unprovided path under `/api/recovery/decision/v1` |
| TC-E1-020-24 | AC18: a retried record leaves one entry, and a timed-out append leaves none and waits in the outbox | NFR | Record for `RW-2026-000201` retried on 2026-12-01; ledger store not answering within the append time limit for `RW-2026-000202` |
| TC-E1-020-25 | AC19: a failed or unanswered rwb-case call writes no queue value and the entry is appended with the record's rule identity | Component | rwb-case contract mock fails the call for `RW-2026-000201`; business date 2026-12-01 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. Every legacy test case of RWB-E1-020 is listed above with the slice this story answers; the -ITG copies belong to RWB-ITG-E1020-ITG, which proves the same values across rwb-case, rwb-decision, rwb-access and rwb-deviation end to end.

### 17. Guardrails

- No business value in code: the rule IDs, versions, queue codes, caps and methods are rows of the two packages and values of rwb-case. No rule form, prefix, queue code or cap appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests. The entry carries a case identifier, a queue identifier, an owner user identifier and a rule identity; no name, address, identity number or account number is written or logged. Test data uses synthetic keys (`RW-2026-000201`, `MTG-BKK-CO`, `U-03`, `ALLOC-014`).
- No cross-schema read (DP-01): `rwb_decision` reads no `rwb_case` table and no table of another service, and holds no foreign key into one.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads neither: the case and queue facts behind a decision stay with rwb-case.
- The record is the owning service's and the entry is this service's: no service writes another's schema, and the append is never done twice for one case and business date.
- An entry is never corrected in place: a correction is a new entry naming the one it corrects, and the append-only trigger refuses an UPDATE and a DELETE.
- No rule engine in this service: no KieBase, no working memory and no evaluation on this queue, so the 300 ms budget of an evaluation is never spent here.
- The announcement is keyed by the package code, the consumed record by the case ID, and no topic name is typed in code (DP-09, DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-E1-020-01, TC-E1-020-02, TC-E1-020-09 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-E1-020-05, TC-E1-020-07 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-E1-020-03, TC-E1-020-04, TC-E1-020-12, TC-E1-020-13 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-E1-020-06, TC-E1-020-08, TC-E1-020-10, TC-E1-020-11, TC-E1-020-14, TC-E1-020-15, TC-E1-020-16, TC-E1-020-17 |

FEAT-CWC-07, FEAT-CWC-08 and FEAT-CWC-09 are carried by the case service; this slice answers them for the record each allocation leaves and for the rule version it cites.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-020; story RWB-P7-E1020-APP; contract RWB-P3-E1020-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| The row name as the rule ID; first match wins; `ALLOC-014` for `MORTGAGE` in `BKK` to queue `MTG-BKK-CO` | Sections 1, 8 (BR2), 11; the FSD name of the same row is recorded with GAP-2440 |
| `ASSIGN-007` and `ASSIGN-2026.11` on the record | Sections 1, 7 (AC1), 8 (BR2), 11 |
| Rule ID and version on every entry (legacy BR9, AC6); R-UNI-39 and R-UNI-40 | Sections 8 (BR3, BR6, BR7), 9, 14 |
| Append only and hash-chained (legacy BR7; FSD P7 AC-P7-001-01) | Sections 8 (BR4), 9, 17 |
| Version states, the 00:01 promotion and the checksum check | Sections 8 (BR8, BR10), 9, 12.3, 12.6 |
| Synthetic values: case `RW-2026-000201`, queue `MTG-BKK-CO`, team `MTG-BKK`, owners `U-01`, `U-02`, `U-03`, cap 150, date 2026-12-01 | Sections 3, 7, 16 |
| MSG-P7-009, MSG-P7-003, MSG-P4-002, MSG-P3-027 | Section 14, exception paths |
| Field IDs DF-DEC-001 to DF-DEC-031; DF-REF-002, DF-REF-003, DF-REF-053, DF-REF-054 | Section 11 |
| Legacy test cases TC-E1-020-01 to TC-E1-020-15 | Section 16 |
| The other slices of RWB-E1-020 | Sections 2, 19 |

### 19. Out of scope

- The JOB-03 run, the two package evaluations, the queue and assignment rules, the owner choice, the cap of 150, the overflow and exception queues, the assignment row and the case update: rwb-case (RWB-P3-E1020-APP).
- The deviation handler queue and the diversion of a flagged case: rwb-deviation.
- The rerun right of JOB-03 and the job monitor: rwb-access and the platform job stories.
- Loading, validating, approving and rolling back the ALLOCATION and ASSIGNMENT packages, the workbook, the test scenarios and the default row check: RWB-P7-E1073-APP.
- The general decision-log writer, the entry read, the hash-chain check job and the archive: RWB-P7-E1008-APP and RWB-P7-E1027-APP.
- Manual transfer and reassignment, reallocation at the cap and daily rebalancing: legacy RWB-E2-011, RWB-E2-012, RWB-E1-030.
- The values of the caseload caps and the service levels (DL22, DL23), and placement on a queue by a model or an agent (legacy RWB-E2-036).
