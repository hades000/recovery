# RWB-P7-E1052-APP Notice generation v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1052-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-N |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1052-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-OCC-001) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-052 for rwb-decision; the D7.1 generation record of a notice in the central decision ledger, its merge-snapshot guard and its two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor (RW-AUDIT), a compliance and PDPA officer (RW-COMPLY) and a litigation officer (RW-LITOFF)**, I want **the D7.1 record of every notice generation — the decision code, rule R-LIT-03 with the version in force, the case reference, the notice reference and notice type, the template code and version, the ACE data date the merged values came from, the reference to the merge snapshot and the final call GENERATED, HELD or REFUSED with its hold reason or its refusal message — appended once to the central decision ledger of `rwb-decision` and readable by case and date, carrying no customer name, no notice address, no account number and no amount**, so that **a generated, a held or a refused notice can be explained years later from the rule and the version that decided it, and a notice whose decision cannot be recorded is never generated**.

Inside `rwb-decision` this is the decision-record slice of legacy RWB-E1-052, the feature the FSD files under this module as FEAT-DRI-14:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: the appender of the D7.1 generation record and the two decision-log reads. The generation itself is decided and performed by the service that owns the notice; this service appends the record once, chained and append only, and serves one entry and the entries of a case in a date range (GAP-2455; ASM-4076).
- What stays with `rwb-comms` (P6, RWB-P6-E1052-CON and RWB-P6-E1052-APP): the notice row and its states, the template check, the merge-value resolution and the merge snapshot, the PDF with its footer, the hold and the task to the case owner, the local decision record, `NoticeGenerated` and the WIN dispatch. None of it is rebuilt here.
- What stays with `rwb-source-data` (P1) is every `recovery.v_ace_*` read — the customer, the contact point, the account balance and the freshness stamp (DP-05); with `rwb-document` (P5) the write-once PDF; with `rwb-case` (P3) the case, the parties, the task and the reference data (DP-07). The entry names those facts by reference and never copies a value.
- The record and the decision are one pair under DP-03: the owning service writes the record inside the transaction of the notice it records and publishes it; this service appends it to the ledger in one idempotent transaction of its own, so a record with no generation behind it is never appended and a generation whose record cannot be appended does not proceed (BR9).
- The service appends and exposes; it evaluates no rule, resolves no merge code, renders no document, holds no notice and dispatches nothing (BR9). The database login is the per-service login of DP-02, and the story refers to "the `rwb-decision` login (DP-02)".

The legacy behaviour carried into the decision service is unchanged in meaning: one entry for every generation decision and no exception, the rule id and the rule version on the entry, the template code and version on the entry, the ACE data date on the entry, the merge snapshot as a reference and never as values, a notice that cannot be recorded is not generated, and a repeated request on one business date leaves one entry (legacy RWB-E1-052 AC1, AC2, AC5, AC6, AC7 and BR4, BR6, BR8, BR10, BR12).

Which fields of the record this service consumes, where the template code and version, the hold reason, the data date and the merge snapshot reference sit inside `inputs_ref`, `actions` and `outcome`, and which final-call values a generation decision uses are Not specified in the source documents (GAP-2454; ASM-4072; ASM-4075).

### 2. Business rationale

Notices are the bank's formal demand, and a notice period counted from a notice that was never authorised, or from an amount taken off a stale batch, can be challenged. The monolith recorded the generation with the notice row in one process and one schema, so the two could not drift apart. In the target the notice is `rwb-comms`'s and the evidence of every decision is collected in `rwb-decision` (Architecture v5 slides 14 and 41), so the generation record has to be appended there, chained, unchangeable and readable by the officer who follows the letter and the auditor who later asks why the notice went out.

The realignment changes the mechanism, not the business rule:

1. The in-process `DecisionLogApi.write` call of the monolith becomes the decision-record path of DP-03: the record is written where the generation commits and is appended here from `rwb.decision-record.v1`, with the append-only rule and the hash chain the FSD already carries (FEAT-DRI-01, FEAT-DRI-03).
2. The entry is not a copy of the notice and not a copy of the PDF: it names the notice, the notice type, the case, the rule and version, the template code and version, the ACE data date, the merge snapshot reference and the final call, and it names no addressee, no address, no account number and no amount (BR4, BR12).
3. The final call, the hold reasons and the message ids are reference rows, registry rows and parameters at the version in force, never literals (BR10); the notice, the template, the merge fields, the PDF, the task and the dispatch stay with their owners, and this story reads none of their tables (DP-01).
4. The one decision-log read of the legacy story becomes two operations on the service's own base (DP-13): the entries of a case in a date range, and one entry with its rule version, its template version and its chain fields.
5. The ACE data date is stored on the entry, so a notice generated from a stale batch is explained rather than hidden, and the data-lake copy of the log is retired with the data lake (DP-17).

This story meets REQ-OCC-001 on the record side and carries control CTL-14 (the notice is produced from the Legal-approved template with its version in evidence) and CTL-06 (no action proceeds unlogged, R-UNI-39).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E1052-CON | The published contract of the notice generation (P6): the declaration of `rwb.decision-record.DecisionRecorded.v1` with the record reference, the case reference, the decision code D7.1, the rule id and version, the notice reference and type, the template code and version, the ACE data date, the merge snapshot reference and the final call; the refusal messages MSG-P6-005, MSG-P6-007, MSG-P6-003 and MSG-P1-001; and the contract fakes. Which further fields of the record this service consumes is Not specified in the source documents (GAP-2454; ASM-4075) |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the idempotency key the record carries |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): the inbox dedupe of a repeated record and the CloudEvents 1.0 envelope of the fact |
| RWB-PLT-E1044-CON | The per-service Flyway sequence of `rwb_decision` (DP-15), in which this story adds one index step and no table |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which SCR-38 Decision log query and the auditor's view reach the two operations |
| The baselines of this service | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE, the unique key on the idempotency key and the chain check JOB-14 at 02:00; and the rule registry `rule_package`, `rule_package_version` and `rule_row` read by rule id and version. Both are the service's own earlier work and are in no H row of this story (GAP-2455; ASM-4078) |
| The parameters and the edge answer | LOV-DECISION holding D7.1, the final-call list, the page-size bound and the completeness target, read at the version in force with no default in code; and the capability area, the right and the scope of each operation, declared on the operations and enforced at gateway-bff, which asks `rwb-access` (GAP-2454; ASM-4073) |

Business preconditions carried from RWB-E1-052:

- Template `DEMAND-MTG` "TH" version 2 is Approved and current with merge codes `CASE_NO`, `CUSTOMER_NAME`, `POSTAL_ADDRESS` and `TOTAL_OUTSTANDING`; template `RECALL-HP` "TH" has only version 1 in state Draft.
- Case `RW-2026-000123` has product group `MORTGAGE` and borrower `person_key` "P-0001"; case `RW-2026-000456` has product group `HIRE_PURCHASE`; business date 2026-11-25; the ACE account data of case `RW-2026-000123` is from 2026-11-24 in the stale-batch case.
- The decision under test is produced by the contract fake of RWB-P6-E1052-CON for the generated, refused, held-on-missing-field, held-on-withdrawn-template and stale-data paths.
- No build dependency. Day 1: the story builds against RWB-P6-E1052-CON and its fakes, and the platform contracts of wave 0 and 1 are in place.

### 4. Flow

1. `rwb-comms` takes the generation decision of a notice on its own base: the template check, the merge-value resolution and the render. The rules and the merge codes are its own data and this story evaluates none of them (RWB-P6-E1052-APP).
2. In the same transaction as the notice row, the PDF reference and its outbox row, the owning service writes its local D7.1 record through the decision-record path of DP-03, carrying the case reference, the notice reference and type, the rule "R-LIT-03" with its version, the template code and version, the ACE data date, the reference to the merge snapshot and the final call `GENERATED`, `HELD` or `REFUSED` with its hold reason or its refusal message (Architecture v5 slide 28).
3. The record path publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the record reference, the decision code, the rule id and version, the final call and the decision time (DP-09; slide 42, event 08).
4. `rwb-decision` `NoticeGenerationRecordListener` reads the fact into the inbox of DP-09, deduplicates by event ID and by the record reference (R-UNI-40), keeps the facts whose decision code is D7.1 and whose rule is R-LIT-03, and passes them to `NoticeGenerationAppendService`; every other decision code and rule is the ledger baseline's general ingest.
5. `NoticeGenerationAppendService` checks the entry: the decision code D7.1 is a value of LOV-DECISION at the version in force; the rule pair "R-LIT-03" and its version exists in the rule registry at the version in force; the case reference, the notice reference and the notice type are present; the template code carries its version; the ACE data date is present; the merge snapshot reference is present; the final call is one of the three; a `HELD` record carries a hold reason and a `REFUSED` record carries its message. A record that fails the check is refused with MSG-P7-009 naming the field and nothing is written (BR5, BR8, BR11).
6. `MergeSnapshotGuard` refuses a record whose merge snapshot arrives as values rather than as a reference: the snapshot holds the merge code, the view column, the business key and the field ID of each value used, never the value, and a payload carrying a customer name, an address, an account number or an amount is refused with MSG-P7-009 naming `mergeSnapshot` (BR12).
7. `NoticeGenerationAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with `decided_at` from the record, and writes the inbox row and the idempotency row of the record reference. A failed append changes nothing: no entry, no chain position and no inbox row (BR3, BR9).
8. A repeated fact with the same record reference, or a second generation request for the same case, notice type, `person_key` and business date, returns the first entry's ID, adds one to the repeat count for R-UNI-40 and appends nothing (BR7). A held notice and its later generation are two decisions and give two entries, chained in decision order (BR1).
9. A generation whose record cannot be appended does not proceed: the record path answers the owning service with MSG-P7-003, the notice row and the PDF are not stored, no chain position is used and an incident is raised under R-UNI-39 (BR9).
10. A litigation officer or an internal audit reader reads one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, and the entries of a case in a date range with `GET /api/recovery/decision/v1/decision-log?caseId=…&decision=D7.1&from=…&to=…`, one page at a time in `decidedAt` order with the total count of the range (BR8). A caller without the Decision log right is refused with 403 and MSG-P4-002; a case outside the caller's scope is refused with 404 and MSG-P4-003, and no entry of that case is returned.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record lacks its case reference, notice reference, template version, data date or merge snapshot reference, or carries a final call outside its list | The append is refused, nothing is written and no chain position is used | MSG-P7-009 | AC5, AC8 |
| X2 | The rule id carries no version, or the pair "R-LIT-03" and its version is absent from the registry at the version in force | The append is refused and the fact stays on the topic for redelivery | MSG-P7-009 | AC5, AC8 |
| X3 | The merge snapshot arrives as values, or the payload carries an address, an account number or an amount | The append is refused at the snapshot guard and nothing is written | MSG-P7-009 | AC8 |
| X4 | The decision-log store is unavailable, or the chain position cannot be taken | The generation is not recorded: the record path answers MSG-P7-003, no notice row and no PDF are stored, no chain position is used and an incident is raised as in R-UNI-39 | MSG-P7-003 | AC5 |
| X5 | The same record is delivered again, or the same generation is requested twice on one business date | One entry exists; the inbox dedupe, the record reference and the business-date key all hold, and the repeat is counted for R-UNI-40 | None | AC6 |
| X6 | The ACE account batch is stale | The record is appended with the ACE data date it carries, and the entry names the freshness message | MSG-P1-001 | AC7 |
| X7 | The template has no Approved version, so the generation is refused | The refusal is recorded with its template and version, and no PDF exists behind it | MSG-P6-005 | AC2 |
| X8 | The decision code is not D7.1, or the rule is not R-LIT-03 | The fact is left to the ledger baseline's general ingest and this story appends nothing | None | AC1 |
| X9 | The caller holds no Decision log right, or asks for a case outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC9 |

An entry is only ever appended beside the generation that caused it: the entry, its chain position, its inbox row and its idempotency row are written in one transaction, so a generation can never leave a half record and a record can never exist for a notice that was not produced (BR9).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the generation contract RWB-P6-E1052-CON, the decision-record path of DP-03, the inbox library and the fakes; no template, merge code, PDF, notice state, task or dispatch is rebuilt here |
| Negotiable | The final-call set, the hold reason and message vocabulary, the payload field set, the parameter names and the message ids are data, registry rows or parameters of their owners; the story fixes only the entry, the append-only rule, the chain and the two reads |
| Valuable | Every generated, held and refused notice is explained by the rule, the version, the template version and the data date that produced it, and that explanation cannot be quietly changed |
| Estimable | One listener, one appender with the chain and the snapshot guard, one query controller with two operations, one index step and one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as one automated test against the contract fakes, with a fixed business date and a fixed chain |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E1-052, and every legacy criterion of the key acts on the notice row, the PDF, the footer, the task or the WIN facts — which belong to RWB-P6-E1052-APP, RWB-P6-E1052-CON, `rwb-document`, `rwb-case` and RWB-ITG-E1052-ITG. The nine criteria below are new for the `rwb-decision` slice and test only the D7.1 generation record and its two reads; each keeps the legacy values of RWB-E1-052 and introduces no business value.

```gherkin
Feature: The D7.1 generation record of a notice in rwb-decision

  Background:
    Given the environment is SIT
    Given case "RW-2026-000123" has product group "MORTGAGE" and borrower person_key "P-0001"
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current
    Given the decision code "D7.1" is a value of LOV-DECISION at the version in force
    Given rule "R-LIT-03" is in force at version "LIT-2026.12"
    Given the business date is 2026-11-25

  Scenario: AC1 A generated notice is recorded with its template version and data date (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0001", case "RW-2026-000123", notice type "DEMAND", rule "R-LIT-03", template "DEMAND-MTG" version 2, data date 2026-11-25, merge snapshot reference "MS-000123-01" and final call "GENERATED"
    When the ledger consumes rwb.decision-record.DecisionRecorded.v1 for that record
    Then one decision_log_entry exists with decision code "D7.1", rule "R-LIT-03", rule version "LIT-2026.12", case reference "RW-2026-000123", notice reference "N-0001", notice type "DEMAND", final call "GENERATED", template "DEMAND-MTG" version 2 and data date 2026-11-25
    Then the entry carries the merge snapshot reference "MS-000123-01" and no customer name, no address, no account number and no amount
    Then the PDF, the notice row and NoticeGenerated stay with rwb-comms and rwb-document and are asserted through their fakes

  Scenario: AC2 A refused generation is recorded with its template and message (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for case "RW-2026-000456", notice type "RECALL", rule "R-LIT-03", template "RECALL-HP" version 1 and final call "REFUSED", naming MSG-P6-005
    When the ledger consumes that record
    Then one entry exists with final call "REFUSED", template "RECALL-HP" version 1 and MSG-P6-005 in its outcome
    Then the entry carries no document reference, because this story stores no document

  Scenario: AC3 A notice held for missing data is recorded with its hold reason (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0002", case "RW-2026-000123", notice type "DEMAND", template "DEMAND-MTG" version 2, final call "HELD" and hold reason "POSTAL_ADDRESS", naming MSG-P6-007
    When the ledger consumes that record
    Then one entry exists with final call "HELD", hold reason "POSTAL_ADDRESS" and MSG-P6-007 in its outcome
    Then the entry names the field "POSTAL_ADDRESS" as a merge code and carries no address value

  Scenario: AC4 A withdrawn template is recorded with its own rule (new, D-RCV-60)
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    Given rule "R-LIT-04" is in force at version "LIT-2026.12"
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0003", case "RW-2026-000123", notice type "DEMAND", rule "R-LIT-04", template "DEMAND-MTG" version 2, final call "HELD" and hold reason "TEMPLATE_WITHDRAWN", naming MSG-P6-003
    When the ledger consumes that record
    Then one entry exists with rule "R-LIT-04", final call "HELD", hold reason "TEMPLATE_WITHDRAWN" and template "DEMAND-MTG" version 2
    Then the case still holds one DEMAND notice for 2026-11-25, because the repeated request appends nothing (AC6)

  Scenario: AC5 A record that cannot be appended stops the generation (new, D-RCV-60)
    Given the decision log store does not accept writes
    Given the rwb-comms contract mock holds the generation of notice "N-0001" open in one transaction with the decision-record path of rwb-decision
    When the decision-record path refuses the append
    Then the record path answers the owning service with MSG-P7-003
    Then no entry exists for "N-0001" and no chain_seq is consumed
    Then no notice row and no PDF are stored and an incident is raised under rule R-UNI-39
    When the same record reference is retried and the store accepts the append
    Then one entry is appended and it takes the chain_seq the refused write did not use

  Scenario: AC6 A repeated generation gives one entry (new, D-RCV-60)
    Given the record under record reference "RW-2026-000123-DEMAND-P-0001-2026-11-25" was appended and the ledger returned its entry ID
    When the same record arrives again, and the topic is replayed from the first offset of the business date
    Then one entry exists for the record, the first entry ID is returned and the repeat count of R-UNI-40 is raised by one
    Then no second entry and no second chain position are written, and the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC7 A stale data date is recorded with its freshness message (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0004", case "RW-2026-000123", notice type "DEMAND", rule "R-LIT-03", template "DEMAND-MTG" version 2, data date 2026-11-24, merge snapshot reference "MS-000123-04" and final call "GENERATED", naming MSG-P1-001 with "DP01 Account and arrears" and 2026-11-24
    When the ledger consumes that record
    Then one entry exists with data date 2026-11-24 and MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24 in its outcome
    Then the entry carries no balance and no account number, and the balance of 2026-11-24 stays in rwb-source-data and rwb-comms

  Scenario: AC8 A record whose merge snapshot carries a value is refused (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0005" with final call "GENERATED" whose merge snapshot arrives with the value of merge code "POSTAL_ADDRESS" instead of the reference
    When the ledger consumes that record
    Then the append is refused with MSG-P7-009 naming "mergeSnapshot" and nothing is written
    Then no chain_seq is consumed and the fact stays on the topic for redelivery
    When the record is corrected to carry merge snapshot reference "MS-000123-05"
    Then one entry is appended and it carries the reference and no value

  Scenario: AC9 The two reads return the entries and their chain and are scoped (new, D-RCV-60)
    Given the generated entry of AC1 and the held entry of AC3 are stored for case "RW-2026-000123" on 2026-11-25
    Given a reader with the Decision log right R in scope of case "RW-2026-000123"
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 200 with final call "GENERATED", rule "R-LIT-03", rule version "LIT-2026.12", notice reference "N-0001", notice type "DEMAND", template "DEMAND-MTG" version 2, data date 2026-11-25, decidedAt, prevHash and entryHash
    When the reader sends GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123&decision=D7.1&from=2026-11-25&to=2026-11-25&page=1
    Then the page holds the two entries in decidedAt order with a total of 2, and the later entry's prevHash equals the earlier entry's entryHash
    Given the rwb-access contract mock returns no Decision log right R for one caller and the scope of team "MTG-BKK" for the reader, against case "RW-2026-000456" of team "HP-NE"
    When each caller sends the read
    Then the responses are 403 with MSG-P4-002 and 404 with MSG-P4-003, and no entry is returned
```

The nine criteria are new and `acs` is empty for this story, because each legacy criterion of RWB-E1-052 acts on the notice row, the PDF or the WIN facts and belongs to its own slice. The values are the legacy values — cases `RW-2026-000123` and `RW-2026-000456`, `person_key` "P-0001", product groups `MORTGAGE` and `HIRE_PURCHASE`, templates `DEMAND-MTG` "TH" version 2 and `RECALL-HP` "TH" version 1, the business date 2026-11-25 and the stale date 2026-11-24, decision code D7.1, rules `R-LIT-03` and `R-LIT-04`, merge codes `CASE_NO`, `CUSTOMER_NAME`, `POSTAL_ADDRESS` and `TOTAL_OUTSTANDING`, the hold reasons `POSTAL_ADDRESS` and `TEMPLATE_WITHDRAWN`, and the messages MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P1-001, MSG-P7-003, MSG-P7-009, MSG-P4-002 and MSG-P4-003. No new business value is introduced. The payload field set of the record, the placement of the template version, the data date and the merge snapshot reference, the final-call set and the message text of this slice have no source and are carried in GAP-2454 with ASM-4072, ASM-4074 and ASM-4075. The `-ITG` copies of the test cases belong to RWB-ITG-E1052-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One entry per generation decision: a generated notice, a held notice and a refused generation each give one entry, and a held notice and its later generation are two entries chained in decision order | Legacy RWB-E1-052 AC1 to AC4; FSD P7 v3 A2.10; REQ-OCC-001 |
| BR2 | The entry carries decision code D7.1 and rule "R-LIT-03" with the version in force, written through the decision-record path of DP-03; the decision code is read from LOV-DECISION at the version in force and is never a literal | Legacy RWB-E1-052 section 4 step 7 and section 18; FSD P7 v3 AC-P7-010-01; Routing Logic v4 row R-LIT-03; BR-P7-010 |
| BR3 | Every entry is hash chained and append only: a `chain_seq`, a `prev_hash` equal to the previous entry's `entry_hash` (64 zeros for the first), an `entry_hash` equal to the SHA-256 of the canonical form, no UPDATE and no DELETE, and a correction as a new entry with `corrects_entry_id` | REQ-DRI-002, REQ-DRI-003; FSD P7 v3 AC-P7-001-01; Architecture v5 slide 28 |
| BR4 | The entry names the case reference, the notice reference and type, the rule id with its version, the template code with its version, the ACE data date, the merge snapshot reference and the final call with its hold reason or message; it carries no addressee name, no address, no phone, no account number, no balance and no PDF payload | Legacy RWB-E1-052 AC1, section 17; Architecture v5 slides 42 and 43 notes; §R7.2 s17 |
| BR5 | The rule id and the rule version are both on the entry and the pair exists in the rule registry at the version in force; a record with a rule id and no version is refused | FSD P7 v3 AC-EXC-P7-002-01 and A2.3; Drools design slide 16 |
| BR6 | A withdrawn template holds the notice under rule "R-LIT-04" and the entry records the hold reason `TEMPLATE_WITHDRAWN`; the withdrawal itself is template reference data of `rwb-comms` and is never evaluated here | Legacy RWB-E1-052 BR1, BR2; R-LIT-03; R-LIT-04 |
| BR7 | One entry per case, notice type, `person_key` and business date: the inbox dedupe and the record reference make a second entry impossible, and the repeat is counted for R-UNI-40 | Legacy RWB-E1-052 AC6, BR8; R-UNI-40 |
| BR8 | The two reads declare the Decision log right R with the scope applied; a role without it is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2; REQ-DRI-012; Legacy RWB-E1-052 AC8 |
| BR9 | A generation that cannot be recorded is not generated: the record path answers MSG-P7-003, no notice row, no PDF and no chain position exist, and an incident is raised under R-UNI-39 | Legacy RWB-E1-052 AC5, BR6; Principle 5; R-UNI-39; FSD P7 v3 AC-P7-010-04 |
| BR10 | The final-call set, the hold reasons and the message ids are read at the version in force; no business value a business person may change is written in code | BR-P7-010; §R7.2 s17 |
| BR11 | A record that lacks its case, notice or template reference, its data date, its merge snapshot reference or its rule version, or that carries a value outside its list, is refused with MSG-P7-009 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-EXC-P7-002-01, AC-EXC-P7-002-05 and AC-ALT-P7-002-01 read on this slice; GAP-2454 |
| BR12 | The merge snapshot holds the merge code, the view column, the business key and the field ID of each value used and never the value; the entry carries a reference to it and the guard refuses a payload that carries a value | Legacy RWB-E1-052 BR12; NFR-040; ADR-010 |
| BR13 | The story appends and exposes: it evaluates no rule, resolves no merge code, renders no document, holds no notice, raises no task and dispatches no file | Architecture v5 slides 14 and 41; DP-01; GAP-2455 |
| BR14 | The two reads are one hop from the gateway-bff composite route, the service reads no table of another service, and the notice, the case, the template and the merge facts arrive as facts of the record or stay with their owners | Architecture v5 slide 13; DP-01; DP-11; DP-19 |

### 9. State transitions

None for a notice, a case or a document. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | `DecisionRecorded` arrives with decision code D7.1, rule R-LIT-03 and final call `GENERATED` | The template code carries its version, the data date and the merge snapshot reference are present, and the rule pair exists in the registry | Appended at the next `chain_seq` with its `prev_hash`, its `entry_hash`, its inbox row and its idempotency row in one transaction |
| Absent | `DecisionRecorded` arrives with final call `HELD` under R-LIT-03 or R-LIT-04 | The hold reason is a value of the reference list and the refusal names its message | Appended at the next `chain_seq`, as above |
| Absent | `DecisionRecorded` arrives with final call `REFUSED` | The record names the template with its version and the message MSG-P6-005 | Appended at the next `chain_seq`, as above |
| Absent | The record fails the check of BR11 or of BR12, or the store or the chain is unavailable | The record is refused, or the append cannot commit | Absent: MSG-P7-009 or MSG-P7-003, nothing written, no chain position used, the fact redelivered and the generation stopped |
| Absent | The decision code is not D7.1, or the rule is not R-LIT-03 or R-LIT-04 | The fact is not this slice's | Absent by design: the ledger baseline's general ingest appends it |
| Appended | The same record arrives again with the same record reference, or the same generation is requested again on one business date | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A later decision of the same notice arrives | The notice was held and then generated | A second entry is appended at the next `chain_seq`, chained to the first |
| Appended | A correction is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted, or the daily check and seal run | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule, and the seal verifies the chain |

The notice stays in the state `rwb-comms` gives it (Generated, Held or none at all after a refusal), the case is `rwb-case`'s and the PDF is `rwb-document`'s; this story changes none of them (BR13).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Reads the generation entries of the notices of the cases in scope, with the template version and the data date |
| RW-CASEOWN, case owner | Reads the entries of the cases owned, including a held notice and its hold reason |
| RW-LEGAL, legal counsel | Reads the entries that name a withdrawn template and the holds it caused |
| RW-AUDIT, internal audit and RW-COMPLY, Compliance and PDPA officer | Reads one entry and the entries of a case in a date range, with the chain fields, and never a customer value (Decision log R, scope ALL) |
| Every role of TSD P7 v2 T6.1 | Holds R on the decision log and reads the entries of the cases in its scope |
| SY-DECLOG, decision record writer | Writes the D7.1 record inside the generation transaction at `rwb-comms` and appends it to the ledger here; the append is the service identity's and not a person's |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, the rule registry and the reference lists, and appends the entry, its inbox row and its idempotency row (DP-02) |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| No approval level from the delegation of authority applies | The approval of a demand or recall notice is the D7.1 approval of RWB-P7-E2014-APP; this story reads no `delegation_limit` row and approves nothing |

The right and the scope behind the two reads are declared on the operations and enforced at gateway-bff (DP-19), which asks `rwb-access`; this story adds no guard of its own, holds no role, scope or delegation row, and makes no authorise call (GAP-2454; ASM-4073). The database login is per service (DP-02).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case reference `RW-2026-000123`) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (D7.1, a value of LOV-DECISION) | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id (`R-LIT-03`, or `R-LIT-04` for a withdrawn template) | Write |
| DF-DEC-005 | `decision_log_entry` | rule_version | Write; the label of the version in force is read from the registry (ASM-4074) |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Not written: no model and no agent take part in a notice generation |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the merge snapshot reference, the template code and version and the ACE data date) | Write; the container shape is Not specified in the source documents (GAP-2454; ASM-4075) |
| DF-DEC-009, DF-DEC-010, DF-DEC-011, DF-DEC-013 | `decision_log_entry` | recommendation, approver_user_id, approval_level, override_reason | Not written: the generation is a rule answer, the approval is another story's entry and a generation is not an override |
| DF-DEC-012 | `decision_log_entry` | final_call (`GENERATED`, `HELD` or `REFUSED`) | Write; the set is the reading of ASM-4072 |
| DF-DEC-014 | `decision_log_entry` | actions (the notice reference and notice type, the template code and version) | Write; the container is TSD P7 v2 T3.1 |
| DF-DEC-015 | `decision_log_entry` | outcome (the hold reason or the refusal message, the data date and the freshness message where one applies) | Write; the placement is the reading of ASM-4072 |
| DF-DEC-016, DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | decided_at, prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029, DF-DEC-030, DF-DEC-031 | `decision_log_entry` | corrects_entry_id, actor_user_id, idempotency_key (the record reference of the generation) | Write; `corrects_entry_id` on a correction only |
| DF-LEG-015, DF-LEG-016, DF-LEG-017, DF-LEG-018, DF-LEG-023, DF-LEG-030, DF-LEG-031, DF-LEG-032 | `notice` (P6) | id, case_id, document_id, notice_type, sent_type, person_key, template_id, hold_reason | Read as facts of the record, never a table |
| DF-REF-046, DF-REF-047 | `template` (P6) | template_code, template_version | Read as facts of the record, never a table |
| DF-REF-253, DF-REF-254, DF-REF-255, DF-REF-257 | `merge_field` (P6) | merge_code, source_entity, source_field, is_required | Read as facts of the merge snapshot reference, never a table |
| DF-ACE-020, DF-ACE-036 | `v_ace_account` (P1) | total_balance, data_as_of | Not read; only the data date arrives as a fact of the record (DP-05) |
| DF-CAS-001, DF-CAS-002, DF-CAS-003 | `recovery_case` (P3) | id, case_no, product_group | Read as facts of the record, never a table |
| DF-DOC-001 to DF-DOC-011 | `document` (P5) | all fields, written through the document hub interface | Not read and not written: the PDF is `rwb-document`'s and its reference arrives as a fact |
| (rule registry) | `rule_package_version`, `rule_row` (P7) | rule id and version at the version in force | Read, to prove that `R-LIT-03` or `R-LIT-04` exists at that version |
| (reference lists, parameters) | reference data (P3) and the service's parameter store | LOV-DECISION which holds D7.1, the final-call list, the page-size bound and the completeness target | Read at the version in force; a direct call would add one C row (ASM-4078) |
| `processed_event`, `idempotency_key` | PLT library in `rwb_decision` | event_id, consumer, processed_at; the record reference and the first entry ID | Write |
| `outbox_event` | PLT library in `rwb_decision` | none | Not written: this story publishes no event |

No row of `notice`, `template`, `merge_field`, `document`, `recovery_case` or `interaction` is copied into `rwb_decision`: the notice, the case, the template and the merge snapshot arrive as facts of the record (DP-01). The merge snapshot itself is an artefact of `rwb-comms` and its store is Not specified in the source documents (GAP-2454; ASM-4075); the entry holds only the reference, by BR12. Field IDs are those of the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries and the Ownership Map gives to P7. The request and response field set of a generation entry is Not specified in the source documents (GAP-2454; ASM-4075).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: the entries of a case in a date range, searched by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: one entry with its decision code, final call, rule id and version, notice reference and type, template code and version, data date, merge snapshot reference and chain fields; 200 with the DecisionLogEntry | Decision log, right R, scope applied | Not applicable, read only |

The DecisionLogEntry body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `inputsRef`, `finalCall`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`, and for a generation entry the notice reference, the notice type, the template code and version, the data date and the merge snapshot reference. The field-level shape is the reading of ASM-4075.

Errors: 401 no session; 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the case is absent or outside the scope (MSG-P4-003); 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. The recommendation read and the approval operations of this service belong to its approval and recommendation stories and are declared neither as provided nor as consumed here.

#### 12.2 REST operations consumed

| Item | Value |
|---|---|
| Operations consumed | None. The record of a generation arrives as the `DecisionRecorded` fact of 12.4 and not over REST, and this story calls no operation of another service: the notice, the case, the template and the merge snapshot stay with their owners and no value of them is read back |

The capability area, the right and the scope of the two reads are declared on the operations and enforced at gateway-bff through the composite route of DP-19, which asks `rwb-access`, so this story adds no `RecoveryAccessGuard` equivalent and no authorise call (GAP-2454; ASM-4073).

#### 12.3 Events published

| Item | Value |
|---|---|
| Events published | None. This story publishes no event of its own: the record is a fact of `rwb-comms` on `rwb.decision-record.v1`, and the entries of the ledger are read through the operations of 12.1 |

`rwb.decision-record.DecisionRecorded.v1` is published by the owning service of each decision and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42, event 08). The approval and rule-package events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-comms` for the generation decisions, and by all 19 services for their own | `NoticeGenerationRecordListener`: inbox dedupe by event ID and by the record reference, then `NoticeGenerationAppendService` for the decision code D7.1, the rule and version, the notice reference and type, the template code and version, the data date, the merge snapshot reference and the final call with its hold reason or message |

The fact carries IDs, codes, versions, a rule reference, a snapshot reference and dates only; no addressee, no address, no account number, no balance and no PDF payload travels on the topic (BR4, BR12). Which further fields of the fact this service requires is Not specified in the source documents (GAP-2454; ASM-4075). Records with any other decision code or rule are the ledger baseline's general ingest.

#### 12.5 Workflows and activities

| Item | Value |
|---|---|
| Workflows and activities | None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09 |

The `ApprovalWorkflow` of `rwb-decision` and the case workflow of `rwb-case` are neither started nor signalled here: this story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules

| Item | Value |
|---|---|
| Schedules | None. This story creates no Temporal Schedule and starts nothing on a clock: the generation run belongs to `rwb-comms`, and the one Schedule of this service's ledger, the chain check JOB-14 at 02:00, is the decision-log baseline's |

DP-10 applies here only to the owning service: a Schedule is registered by the service that owns the job, and the record ingest of this story is continuous Kafka and not a clock (BR14).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The generation entry: the case, the notice, the rule and version, the template and version, the data date, the merge snapshot reference, the final call and the chain position; append only |
| `rule_package`, `rule_package_version`, `rule_row` | P7 (`rwb_decision`) | Read by rule id and version to prove that the rule that decided the generation exists at the version in force |
| `approval`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written here: the approval of a notice is another story's, and no rule package is tested by this story |
| `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Inbox dedupe and the idempotency key of the record reference (DP-09) |
| `outbox_event` | PLT library, created in `rwb_decision` | Present but not written: this story publishes no event |

Not owned and never read: `notice`, `template`, `merge_field` (P6), `recovery_case`, `case_party`, `task` (P3), `document` (P5), `interaction` (P1), `role`, `permission` and `delegation_limit` (P4). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms record fake | RWB-P6-E1052-CON | The D7.1 records of case `RW-2026-000123`: generated under `R-LIT-03` with template `DEMAND-MTG` version 2, data date 2026-11-25 and merge snapshot reference `MS-000123-01`; held under `R-LIT-03` with `POSTAL_ADDRESS`; held under `R-LIT-04` with `TEMPLATE_WITHDRAWN`; generated from data date 2026-11-24 with MSG-P1-001; the refusal of `RECALL-HP` version 1 for case `RW-2026-000456`; a record with no rule version; a record whose snapshot carries a value |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the record reference and a forced failure for AC5 |
| central ledger fake | The ledger side of `rwb.decision-record.v1` | The completeness reading of the ingest, the replay of the same record of AC6, and the chain head AC5 asserts against |
| rwb-access scope fake | The edge declaration of DP-19 | The allow answer with the Decision log right R and case `RW-2026-000123` in scope; the refusal of MSG-P4-002 and the scope `MTG-BKK` against case `RW-2026-000456` of team `HP-NE` for MSG-P4-003 |
| reference, parameter and registry fake | The lists, parameters and rule registry of the service | LOV-DECISION holding D7.1, the final-call list, the hold reason vocabulary, the page-size bound, the completeness target, and `R-LIT-03` and `R-LIT-04` at version `LIT-2026.12` with one rule id present and no version |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 0 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; no operation of another service is called, and the right and the scope are enforced at the edge (DP-19) |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed, with the inbox dedupe by event ID and record reference; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the generation runs in `rwb-comms` and the chain check is the baseline's |
| File | None | No file input and no file output; the PDF, the DOCX template and the WIN file never reach this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/notice`, Java package `th.co.scb.ace.workbench.recovery.decision.notice`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record itself: the append through the decision-record path, the chain, the append-only rule and the shared topic. DP-01 and DP-02 are the boundary and the login: the entry lives in `rwb_decision` and the notice, the template, the merge fields, the PDF and the case are never read as tables. DP-07 is the D7.1 code, the final-call set and the hold reason vocabulary at the version in force. DP-09 is the inbox dedupe, the record reference and the CloudEvents envelope. DP-11 is the one hop with a 2 s timeout behind the edge, and it is why no service call is made on the consumer path. DP-13 is the base `/api/recovery/decision/v1`; DP-15 is the single Flyway step; DP-19 is the gateway-bff route through which SCR-38 Decision log query reaches the two operations. DP-05 has an instance only as an absence: this service reads no `v_ace_*` view, because the balance and the data date arrive as facts of the record.

The platform H dependencies of the DP table and the published C dependencies of other services are not in the metadata rows of this story, which name None and `RWB-P6-E1052-CON`; they are the dependencies the DP table adds and they are recorded in GAP-2455 and ASM-4078, with the two baselines of 12.7. None of them blocks the build beyond Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeGenerationRecordListener | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and record reference, keeps the D7.1 facts ruled by `R-LIT-03` or `R-LIT-04` and hands them to the appender |
| NoticeGenerationAppendService | Service | Checks the decision code, the rule pair, the case, notice and template references, the data date, the merge snapshot reference and the final call, and writes the entry, its chain position, its inbox row and its idempotency row in one transaction (BR2, BR5, BR11, BR9) |
| MergeSnapshotGuard | Service | Refuses a payload whose merge snapshot arrives as values; keeps the reference-only rule of BR12 |
| ChainHasher | Service | The canonical form of an entry and its SHA-256, the first `prev_hash` of 64 zeros and the `prev_hash` of every later entry (BR3) |
| RuleRegistryReader | Repository | Reads `rule_row` and `rule_package_version` by rule id and version to prove the rule that decided the generation (BR5) |
| DecisionLogQueryController | Controller | The two operations of 12.1 with the declared right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogQueryService | Service | The date-range search of a case and the single read, the row shape of a generation entry, and the total count of the page |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, insert only, with the search indexes and the idempotency key |
| ReferenceListClient, ParameterClient | Client | LOV-DECISION, the final-call list, the hold reason vocabulary, the page-size bound and the completeness target at the version in force |

**Database and migrations**

- Writes `decision_log_entry`, its inbox and idempotency rows in schema `rwb_decision`, and reads `rule_row` and `rule_package_version` in the same schema; reads no other schema (DP-01).
- The table, its columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE and the unique key on the idempotency key belong to the decision-log store baseline and are not rebuilt here (GAP-2455).
- One migration step in the per-service Flyway sequence (DP-15): `V1052_1__decision_log_notice_index.sql` adds the composite index `ix_declog_notice_case ON decision_log_entry (case_id, decision_code, decided_at DESC)` that the date-range read uses. The index name is Not specified in the source documents (GAP-2454; ASM-4075).
- No row of `notice`, `template`, `merge_field`, `document` or `recovery_case` is written here.

**Configuration and reference data**

- LOV-DECISION which holds D7.1, the final-call list of `GENERATED`, `HELD` and `REFUSED`, and the hold reason vocabulary `POSTAL_ADDRESS` and `TEMPLATE_WITHDRAWN` are read at the version in force; the values are the legacy values (ASM-4072).
- The page-size bound of the search and the completeness target of the ingest are parameters with no default in code; their names are Not specified in the source documents (GAP-2454; ASM-4078). The rule version label is read from the registry and never composed in code (ASM-4074).
- The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON). The switch of the generation is `rwb.comms.notice-generation` of RWB-P6-E1052-APP; this story adds no feature switch of its own.

**Build steps**

1. `DecisionLogRepository` and the index step; test the date-range read of a case, the single read and the INSERT-only constraint (AC9).
2. `ChainHasher` and the canonical form: `chain_seq`, `prev_hash` from the previous entry, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC1, AC9).
3. `NoticeGenerationRecordListener` with the inbox and the dedupe by event ID and record reference; test the replay and the repeated record of AC6.
4. `NoticeGenerationAppendService` with the checks of BR11 and the fail-closed transaction; test the forced failure of AC5 and the chain position the refused write does not use.
5. `RuleRegistryReader` and the rule id with its version; test a record without a version and a pair absent from the registry (X2).
6. `MergeSnapshotGuard`; test the payload that carries a value of AC8 and the corrected record that carries only the reference.
7. `ReferenceListClient` and `ParameterClient` with the version in force, and the refusal rather than an assumed final call or message (BR10, BR11).
8. The four record shapes: generated under `R-LIT-03`, refused under `R-LIT-03` with MSG-P6-005, held with `POSTAL_ADDRESS` and held under `R-LIT-04` with `TEMPLATE_WITHDRAWN`; tests for AC1, AC2, AC3 and AC4.
9. `DecisionLogQueryController` with the declared right, the scope, the paging and the problem mapping; tests for AC9, MSG-P4-002 and MSG-P4-003, and the stale data date of AC7.
10. The boundary test: no write to `rwb_comms`, `rwb_case`, `rwb_document` or `rwb_source_data`, and no name, address, account number, balance or PDF payload in any entry, event payload or log line (AC1, AC8, BR4).

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, a generated and a held notice of one case leave two chained entries naming their own rule, template version and data date, a refused generation leaves its own entry with MSG-P6-005, a generation that cannot be recorded leaves none and consumes no chain position, a repeated request leaves one entry, both reads answer inside the 2 s budget of the frame, and no notice, template, document or case was changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | A generation record cannot be appended, or the store or the chain is unavailable | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path, on the append; the owning service stops the generation, no notice and no PDF are stored, and an incident is raised under R-UNI-39 |
| MSG-P7-009 | A record lacks its case, notice or template reference, its data date, its snapshot reference or its rule version, or carries a value outside its list | Not specified in the source documents (GAP-2454; ASM-4077) | This story, on the schema check of the append, naming the missing field |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | The edge, through the authorise answer of the read |
| MSG-P4-003 | The case or the entry is outside the caller's scope | This case is not in your scope. | The edge, through the authorise answer of the read |
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. | `rwb-comms`; asserted here and named in the outcome of the refused entry |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. | `rwb-comms`; asserted and named in the outcome of the held entry |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms`; asserted and named in the outcome of the held entry |
| MSG-P1-001 | The ACE account batch is stale | {product} is from {date}. Today's ACE batch has not arrived. | `rwb-source-data`, shown by `rwb-comms`; asserted and named in the outcome of the entry |

MSG-P7-003, MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P1-001, MSG-P4-002 and MSG-P4-003 are copied unchanged from RWB-E1-052 section 14 and the P7 message set. MSG-P7-009 is named by FSD P7 v3 and its text is written by no source, so the placeholder stands (GAP-2454; ASM-4077). Thai text for each message follows decision DL10. Delivery shape: every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request, with the status mapping 401 no session, 403 MSG-P4-002, 404 MSG-P4-003, 422 a query value outside its list and 503 MSG-P7-003 on the record path.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by case, rule, approver and date with export (FSD P7 v3 Screens), and by the auditor's view of the ledger; both are reached through the gateway-bff composite route of DP-19 and are another story's. The notice screens stay `rwb-comms`'s — SCR-30 Case documents shows the generated PDF and SCR-01 My work carries the task of a held notice — and SCR-18 Notice approval is the D7.1 approval screen of this service (RWB-P7-E2014-APP).

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The D7.1 generation entries of the case in decidedAt order, each with its rule and version, its notice reference and type, its template and version, its data date and its final call with its hold reason or message |
| The entry read | One entry | The same row with its merge snapshot reference, its `decidedAt`, its `prevHash` and its `entryHash`, and a `correctsEntryId` beside the entry it corrects |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a case outside the scope; no row is returned |

A panel or screen id for showing the generation record beside the notice on the notice screens, and the field list of SCR-38, are Not specified in the source documents (GAP-2454; ASM-4075). The screen field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-01 | AC1, BR2, BR4; legacy Covers "AC1" | Contract | Case `RW-2026-000123`, `DEMAND-MTG` "TH" version 2, data date 2026-11-25, snapshot reference `MS-000123-01`; one generated entry, and the PDF and footer stay in `rwb-comms` and `rwb-document` |
| TC-E1-052-02 | AC2, BR11; legacy Covers "AC2" | Component | Case `RW-2026-000456`, `RECALL-HP` "TH" version 1 Draft; entry `REFUSED` with MSG-P6-005 and no document reference |
| TC-E1-052-03 | AC3, BR11, BR12; legacy Covers "AC3" | Component | No ADDRESS contact point for `P-0001`; entry `HELD` with `POSTAL_ADDRESS` and MSG-P6-007, no address value |
| TC-E1-052-04 | AC4, BR6; legacy Covers "AC4" | Component | `DEMAND-MTG` "TH" version 2 withdrawn, no later version Approved; entry `HELD` under `R-LIT-04` with `TEMPLATE_WITHDRAWN` and MSG-P6-003 |
| TC-E1-052-05 | AC5, BR9; legacy Covers "AC5, BR6" | Component | Decision log store stubbed unavailable; MSG-P7-003, no entry, no chain position, incident under R-UNI-39, then the retry takes the position |
| TC-E1-052-06 | AC6, BR7; legacy Covers "AC6, BR8" | Contract | The same record reference twice and a replay from the first offset of 2026-11-25; one entry and one repeat count |
| TC-E1-052-07 | AC7, BR4; legacy Covers "AC7" | Component | Data date 2026-11-24 with no COMPLETED ALS row for 2026-11-25; entry with the data date and MSG-P1-001 naming "DP01 Account and arrears" |
| TC-E1-052-08 | AC9, BR8; legacy Covers "AC8" | Component | Read of case `RW-2026-000456` outside the scope of team `MTG-BKK`; 404 with MSG-P4-003 and no entry |
| TC-E1-052-09 | AC9, BR8; legacy Covers "Access" | Component | Service identity and a role without Decision log R; 403 with MSG-P4-002 and no entry |
| TC-E1-052-10 | AC5, BR9; legacy Covers "Principle 5" | NFR | Decision log write forced to fail on 20 generation records; no entry, no chain position used, MSG-P7-003 and the incident raised |
| TC-E1-052-11 | AC1, BR4; legacy Covers "AC9, BR11" | Component | `v_ace_pod` row POD-0001 with notice_ref WIN-77001; the generation entry carries no delivery status and no WIN field, and the delivery record is RWB-P7-E2021-APP's |

The eleven legacy test cases of RWB-E1-052 are kept in the order of the work package and each is answered here on the record side: the generation entry, its rule and version, its template version, its data date, its snapshot reference, its chain and its two reads. The notice row, the PDF, the footer, the task and the WIN facts are the contract fakes' and their own services'. The legacy level System maps to Component, Contract or Integration as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases end in `-ITG` and belong to RWB-ITG-E1052-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code, the final-call set, the hold reasons, the rule versions, the page-size bound, the completeness target and the message ids are reference rows, registry rows or parameters read at the version in force.
- No personal data in the entry, the snapshot reference, the event, the audit line, the tests or the logs: the notice reference, the notice type, the case reference, the rule and version, the template and version, the data date, the final call, the hold reason or message and the hashes only.
- No read of another service's tables (DP-01): the notice, the template, the merge facts, the PDF and the case arrive as facts of the record or are never touched.
- ACE data only through the owner's contract or `v_ace_*` views (DP-05): this story reads no ACE data, because the balance and the data date arrive as facts through `rwb-source-data` and `rwb-comms`.
- The merge snapshot is never copied: the entry holds a reference, and a payload that carries a value is refused (BR12).
- No entry without its generation and no generation without its entry: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and a generation whose record cannot be appended is stopped with an incident (BR9, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1 (BR3).
- One entry per generation: the inbox dedupe, the record reference and the business-date key make a second entry impossible (BR1, BR7).
- One base, one topic and one queue: `/api/recovery/decision/v1`, `rwb.decision-record.v1` for the record and `rwb.decision.events.v1` for this service's own events, with `rwb-decision` in namespace `rwb-recovery` (DP-13, DP-14 in the naming library).
- One hop and 2 s with a breaker per downstream behind the edge; an unreadable list, parameter or rule row refuses the append rather than writing an assumed value (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 | TC-E1-052-01 to TC-E1-052-11 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-052, disposition Split (rework) |
| Legacy criteria owned here | None verbatim: `acs` is empty, and the nine criteria of section 7 are new for the decision-record slice |
| Legacy behaviour carried | AC1 to AC8 on the record side, with BR1, BR2, BR4, BR6, BR8, BR10 and BR12 |
| Test cases | TC-E1-052-01 to TC-E1-052-11, all eleven in the legacy order |
| Decoupling patterns | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-017 (embedded Drools per service, rule registry in rwb-decision), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 |
| Messages | MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P1-001 |

| Legacy reference | Where it is kept |
|---|---|
| The D7.1 entry with rule "R-LIT-03", the template code and version and the merge snapshot reference | Sections 1, 4 (steps 2 and 5), 7 (AC1), 8 (BR2, BR4), 11, 13 |
| A notice that cannot be recorded is not generated (legacy AC5) | Sections 5 (X4), 7 (AC5), 8 (BR9), 14 |
| The footer, the PDF and the notice row | Not rebuilt: RWB-P6-E1052-APP, RWB-P6-E1052-CON, `rwb-document`; asserted through fakes in sections 7 and 16 |
| The withdrawn template holds the notice (legacy AC4) | Sections 7 (AC4), 8 (BR6), 11 |
| The stale ACE batch is shown with its data date (legacy AC7) | Sections 7 (AC7), 8 (BR4), 14 |
| One notice per case, notice type, `person_key` and business date (legacy AC6) | Sections 7 (AC6), 8 (BR7), 13 |
| The merge snapshot holds no value (legacy BR12) | Sections 7 (AC8), 8 (BR12), 13, 17 |
| The two decision-log reads and the access refusal (legacy AC8, TC-09) | Sections 4, 7 (AC9), 8 (BR8), 12.1, 15 |
| Cases `RW-2026-000123` and `RW-2026-000456`, `DEMAND-MTG` v2, `RECALL-HP` v1, business date 2026-11-25, stale date 2026-11-24 | Sections 3, 7, 11, 16 |
| Legacy key RWB-E1-052, story RWB-P7-E1052-APP, contract RWB-P6-E1052-CON, test cases TC-E1-052-01 to TC-E1-052-11, patterns DP01 to DP19 as listed | Metadata, sections 3, 12, 16 |

The other slices of the key answer the rest: RWB-P6-E1052-CON and RWB-P6-E1052-APP the notice, the template check, the merge values and the snapshot, the PDF, the footer, the hold, the task and the dispatch; `rwb-source-data` the ACE reads and the freshness stamp; `rwb-document` the write-once PDF; `rwb-case` the case, the parties, the task and the reference data; RWB-P7-E2014-APP the D7.1 approval; RWB-P7-E2021-APP the dispatch record; RWB-ITG-E1052-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- The notice row and its states, the template check, the merge-value resolution, the merge snapshot itself, the PDF and its footer, the hold, the task to the case owner and the WIN dispatch: RWB-P6-E1052-APP, with the contract in RWB-P6-E1052-CON, and `rwb-document`. This story appends the record of a decision and produces no notice.
- The ACE reads of the customer, the contact point, the account balance and the freshness stamp: `rwb-source-data` (P1, DP-05). The data date reaches this story only as a fact of the record.
- The template reference data, the merge field catalog and their Legal approval: RWB-P6-E1046-APP and the template stories of `rwb-comms`.
- The D7.1 approval of a demand and recall notice and its screen: RWB-P7-E2014-APP. This story approves nothing and reads no `delegation_limit` row.
- The dispatch record and the proof of delivery: RWB-P7-E2021-APP, RWB-P6-E1055-APP and `rwb-integration` (P2, DP-16). No delivery status and no WIN field is written on a generation entry.
- The general ingest of every other decision code into the ledger, the append-only table itself, the daily chain check JOB-14 at 02:00 and the daily seal: the decision-log baseline of this service.
- The data-lake copy of the log: retired with the data lake (DP-17).
- SCR-38 Decision log query as a built screen and the composite route: the screen stories and RWB-PLT-N001-CON.
- The litigation route rules that call generation in production (R-LIT-01, Epic 5) and notice approval under R-LIT-04 beyond its record, as the legacy story left them.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E1052-ITG. The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story and the platform stories.
