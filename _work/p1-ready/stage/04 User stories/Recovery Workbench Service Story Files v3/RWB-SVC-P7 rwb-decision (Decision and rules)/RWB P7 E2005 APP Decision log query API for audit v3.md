# RWB-P7-E2005-APP Decision log query API for audit

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-005 for rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 11 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E2005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P7-B |
| Ready to start | After RWB-P7-E1008-APP |
| Depends on (build) | RWB-P7-E2005-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P7-E1008-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P4-E1039-CON, RWB-P3-E2041-CON |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P7-E2005-APP-14) |
| Fake library version | Not specified in the source documents (DOR-RWB-P7-E2005-APP-22) |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E2005-APP-23) |
| Readiness decisions | RD-P1-004 |
| Integration dependencies | None |
| External dependencies | None |
| Flyway migration | V2005_1__declog_approver_index.sql (index only) in the rwb-decision sequence after the RWB-P7-E1008-APP baseline; no file of RWB-P7-E1008-APP is edited |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-003, FR-P7-004, FR-P7-012, FR-P7-013, FR-P7-014, FR-P7-015, FR-P7-016, FR-P7-036) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-P7-E2005-APP-16) |

### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **to query the central decision ledger of rwb-decision by case or a population of cases, decision, approver, date and rule version, with the hash chain checked on every entry returned, and to export the result**, so that **an audit question is answered from the ledger in minutes on the rwb-decision contract, and I can rely on each entry I am given because the query, the scope and the chain check are three separate, testable things**.

### 2. Business rationale

Audit and the regulator ask for the decision history of a sample of cases: inputs, versions, approver and final call. In the monolith that answer came from one table in the single `recovery` schema, filtered by an in-process scope interface, and the export was a CSV written by the same module. Architecture v5 keeps the capability and changes every mechanism around it: the ledger is `decision_log_entry` in `rwb_decision` and it is P7's (Architecture v5 slides 14 and 41); the read is one more contract of rwb-decision under `/api/recovery/decision/v1` (DP-13); the right and the scope are data of rwb-access asked through the authorise contract with the guard library (DP-08); the limits and the lists are parameters and reference rows of rwb-case (DP-06, DP-07); the access record of a query and of an export is a local decision record on the shared topic and not a row written through another module's interface (DP-03); and there is no data lake copy to analyse afterwards (DP-17). Slide 28 states what auditors get in the target in one line: one place to search every decision, with the rule version and the approver, alerts for missing records and the chain checked every day. This story builds the search.

The story is the app slice of legacy RWB-E2-005 and it owns all ten legacy criteria, AC1 to AC10, because every one of them is answered by the two operations of this service: the case query, the rule-version query with its reconciliation to the rule change audit report, the access refusal, the approver-and-period query, the chain mismatch, the scope limit, the invalid filters, the export, the no-match page and the population of cases. The three facts the criteria need from other owners — the right and the scope, the two limits and the lists, and the count per rule package version — are contract fakes from the first run, and every one of them is named in section 12.2 with its owner and its contract ID.

Three decisions make this slice buildable on its own. The chain check is local: it recomputes `entry_hash` from the canonical form of the entry and compares `prev_hash` with the `entry_hash` of the entry before it, so it needs no service call and no write (REQ-DRI-003). The check never hides an entry: an entry that does not verify is returned with `chainVerified` false and the warning MSG-P7-012, and one incident is raised per failing entry, because a hidden mismatch is worse than a flagged one (NFR-035, REQ-DRI-002). And the query path writes: it writes one access record per query and one per export through the local decision-record library, in the access-event shape that carries no case and needs no subject group (DP-03), so the access log of rwb-access can read the record back without this service calling it on the read path.

The measure is the time to answer an audit sample: the first page of a query over 10,000 matching entries in 3 seconds or less, carried as a working target and tested in SIT as a parameter and not a fixed value; DL11 confirms or replaces the number before the wave 2 exit (GAP-1247; ASM-2211).

### 3. Preconditions

- RWB-P7-E1008-APP is done: `decision_log_entry` exists in `rwb_decision` with the canonical form, the chain columns `chain_seq`, `prev_hash` and `entry_hash`, the append-only rule, the verifier and the indexes `ix_declog_case_time`, `ix_declog_rule` and `ix_declog_actor_time`.
- RWB-P7-E2005-CON is published: the two operations on base `/api/recovery/decision/v1`, the query parameters, the paging shape, the `DecisionLogEntry` resource, the error envelope with one message ID per condition, the fakes and the drift test, so this story builds against a fixed contract on Day 1.
- The authorise contract of rwb-access is live (RWB-P4-E1037-CON) with the guard library (RWB-PLT-E1037-CON), so the Decision log right R and the caller's scope are read as data and never written in code.
- The parameters contract (RWB-PLT-E1042-CON, C RWB-P3-E1042-CON) and the reference-data contract (RWB-PLT-E1043-CON, C RWB-P3-E1043-CON) are live: `rwb.decision.query.max-size` = 500 and `rwb.decision.query.max-cases` = 500 are parameters, and LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE are reference rows read with the version in force.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract, so the AC-READ and AC-EXPT access records are written locally in the caller's transaction and relayed by the outbox (DP-03).
- The rule change audit report of rwb-case (RWB-P3-E2041-CON) answers the count of decisions per rule package version, which is the figure AC2 reconciles to.
- The access log of rwb-access (RWB-P4-E1039-CON) reads the access records of a query and of an export back, which the tests of AC8 use. P4 keeps the access-log read, the break-glass path and the role model, and no read path of this service calls P4 to write.
- The per-service Flyway sequence of rwb-decision runs (RWB-PLT-E1044-CON, DP-15) and the gateway-bff route exists (RWB-PLT-N001-CON, DP-19), so SCR-38 reaches the two operations through the composite route and not directly.
- Test users hold RW-AUDIT (scope ALL), RW-CASEOWN (scope OWN) and RW-PHONECOL (no Decision log right) in SIT, and the SIT ledger holds the synthetic set of section 16. The users and the set are the legacy ones and are unchanged.
- The retention period of a ledger entry is set by Compliance and is not yet a value: NFR-030 says the log is retained for the period the regulator and internal audit require and the decision is still open (DL26). The value is Not specified in the source documents (GAP-1241; ASM-2205).
- The scope predicate is fixed by the authorise answer and applied to the case of each entry; no case read of rwb-case is added to the read path. The shape of the scope answer and the owner of the predicate are Not specified in the source documents (GAP-1245; ASM-2209).
- No approval stop: the story starts at status Draft (realignment v1) and only H rows in the metadata table block the build (Template and Rules §R5.7).

### 4. Flow

1. An internal auditor opens SCR-38 Decision log query and enters the filters: a case or a list of cases, a decision, a rule ID, a rule version, an approver, and a from and a to date.
2. gateway-bff forwards the read with the user JWT; the guard of RWB-PLT-E1037-CON asks the authorise contract of rwb-access for the Decision log right R and the caller's scope, and caches the answer for the token's life (DP-08).
3. `DecisionLogController` receives `GET /api/recovery/decision/v1/decision-log` with the filters, `page` and `size`, and forwards them to `DecisionLogQueryService`.
4. `FilterValidator` validates the filters against the parameters and the lists of RWB-P3-E1042-CON and RWB-P3-E1043-CON: `from` not after `to`, `size` between 1 and `rwb.decision.query.max-size`, and at most `rwb.decision.query.max-cases` case IDs on `caseIds` (DP-06, DP-07).
5. `ScopeFilter` applies the scope of the authorise answer to the case of each entry inside the query, so no matching entry outside the scope is ever counted or returned; the excluded count is not shown (BR2).
6. `DecisionLogQueryService` runs the paged query in `chain_seq` order on `decision_log_entry` in `rwb_decision`, using `ix_declog_case_time`, `ix_declog_rule` or `ix_declog_approver_time` according to the filter set (DP-01).
7. `ResultChainCheck` reads the page plus the entry before the first one, recomputes `entry_hash` from the canonical form of each entry, compares `prev_hash` with the `entry_hash` of the entry before it, and sets `chainVerified` on each entry of the page.
8. Where an entry does not verify, the entry is returned with `chainVerified` false, the response carries the warning MSG-P7-012 naming the entry, and `ChainMismatchNotifier` raises one incident to the Compliance queue for that entry. Nothing is dropped and nothing is corrected (BR4).
9. `AccessRecorder` writes one AC-READ access record through the decision-record library in the same transaction as the read, naming the filter and the row count, and the library relays `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (DP-03). If the record cannot be written the answer is 503 with MSG-P7-003 and no page is returned.
10. The auditor pages through the result with `page` and `size`; each page repeats steps 6 to 9 with its own access record.
11. The auditor selects export on SCR-38; the same request is repeated with `Accept: text/csv`, `DecisionLogCsvWriter` streams the full result page by page with a header row and `chainVerified` on each row, and one AC-EXPT access record is written with the filter and the row count. The export path and its budget are the reading of ASM-2206 (GAP-1242).
12. An entry is read on its own with `GET /api/recovery/decision/v1/decision-log/{entryId}`: the same per-entry check, the same `chainVerified` flag, the same scope test, and 404 with MSG-P4-003 where the entry is absent or its case is outside the scope.
13. A read that matches nothing answers 200 with an empty page and `total` 0, and SCR-38 shows the empty state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Decision log R queries | Refused with 403; the refusal is recorded as an access record; SCR-38 shows the no access state | MSG-P4-002 | AC3 |
| X2 | A returned entry does not match the chain | The entry is returned with `chainVerified` false; the warning names it; one incident per entry to Compliance | MSG-P7-012 | AC5 |
| X3 | The caller's scope excludes some matching entries | Only entries of cases in scope return; the excluded count is not shown | None | AC6 |
| X4 | `from` is after `to`, `size` is outside 1 to 500, or more than 500 case IDs are given | Refused with 422 naming the field | MSG-GEN-003, MSG-GEN-002 | AC7 |
| X5 | No entry matches | 200 with an empty page and `total` 0; SCR-38 shows the empty state; the loading state of SCR-38 is Not specified in the source documents (DOR-RWB-P7-E2005-APP-10) | None | AC9 |
| X6 | The access record cannot be written | Nothing is returned; 503; an incident is raised, because a read that cannot be recorded is not served | MSG-P7-003 | AC8, TC-E2-005-12 |
| X7 | The ledger query does not answer inside the budget | 503 with the platform unavailable message; the page is not partially returned; SCR-38 shows the error state | MSG-GEN-006 | AC11 |
| X8 | An entry is asked for by ID and is absent or outside the scope | 404; nothing is read and nothing is recorded as a successful read | MSG-P4-003 | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the store of RWB-P7-E1008-APP and builds against RWB-P7-E2005-CON and the four platform contracts; the right, the scope, the limits, the lists, the rule-version count and the access-log read are contract fakes from the first run |
| Negotiable | The page limits and the performance target are parameters and an open decision (DL11); the story fixes the filter set, the order, the chain rule and the fail-closed rule |
| Valuable | An audit sample is answered from one ledger on the service's own contract, with every entry checked and every read recorded |
| Estimable | Two operations, one filter validator, one scope filter, one chain check, one notifier, one CSV writer and one access recorder |
| Small | Fits in two weeks with its tests, as the app slice of the legacy key |
| Testable | Each criterion in section 7 is one test in section 16, run against the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Decision log query API for audit — the rwb-decision slice

  Background:
    Given the environment is SIT with the synthetic decision log set "DL-AUDIT-01"
    Given test user "U-8101" holds RW-AUDIT with scope "ALL"
    Given the rwb-access contract mock returns "U-8101" with the Decision log right "R" and scope "ALL"

  Scenario: AC1 Query by case (legacy RWB-E2-005 AC1)
    Given case "RW-2026-000123" has six entries with chain_seq 101, 155, 160, 230, 231 and 402
    When "U-8101" calls GET /decision-log with caseId of that case
    Then the six entries return in chain_seq order
    Then each entry carries chainVerified true

  Scenario: AC2 Query by rule version (legacy RWB-E2-005 AC2)
    Given rule R-LIT-03 at version "LIT-2026.12" was used in 200 decisions
    Given the rwb-case contract mock returns the rule change audit report with 200 decisions for version "LIT-2026.12"
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500
    Then 200 entries return and total is 200
    Then the total equals the count for "LIT-2026.12" in the rule change audit report

  Scenario: AC3 Access (legacy RWB-E2-005 AC3)
    Given test user "U-8102" holds only RW-PHONECOL, whose Decision log letter is "-"
    Given the rwb-access contract mock refuses "U-8102" with MSG-P4-002 for the Decision log right "R"
    When the user calls GET /decision-log
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" is written

  Scenario: AC4 Query by approver and period (legacy RWB-E2-005 AC4)
    Given approver "U-8103" approved 14 decisions between 1 and 31 December 2026 and 3 in November 2026
    When "U-8101" calls GET /decision-log with approver "U-8103", from "2026-12-01" and to "2026-12-31"
    Then 14 entries return with approverUserId "U-8103" and approvalLevel filled

  Scenario: AC5 An entry that does not match the chain is flagged (legacy RWB-E2-005 AC5)
    Given the entry with chain_seq 230 was changed in the SIT database with the trigger disabled
    When "U-8101" queries case "RW-2026-000123"
    Then six entries return and entry 230 carries chainVerified false
    Then the response carries warning MSG-P7-012 naming entry 230
    Then the system raises one incident to the Compliance queue for entry 230

  Scenario: AC6 Scope limits the result (legacy RWB-E2-005 AC6)
    Given test user "U-8104" holds RW-CASEOWN with scope "OWN" and owns 3 of the cases decided under "LIT-2026.12"
    Given the rwb-access contract mock returns "U-8104" with the Decision log right "R" and scope "OWN"
    Given the rwb-case contract mock returns the three cases decided under "LIT-2026.12" with owner "U-8104"
    When "U-8104" queries ruleVersion "LIT-2026.12"
    Then only the entries of those 3 cases return and total counts only them

  Scenario: AC7 Invalid filters are refused (legacy RWB-E2-005 AC7)
    When "U-8101" calls GET /decision-log with from "2026-12-31" and to "2026-12-01"
    Then the call returns status 422 with message MSG-GEN-003 for field "from"
    Then when "U-8101" calls it with size 1000
    Then the call returns status 422 with message MSG-GEN-002 for field "size" with min 1 and max 500

  Scenario: AC8 Export (legacy RWB-E2-005 AC8)
    Given the query of AC2 returns 200 entries
    When "U-8101" exports the result from SCR-38
    Then a CSV file with a header row and 200 entry rows is returned, with chainVerified on each row
    Then one entry with decision code "AC-EXPT", the filter and row count 200 is written

  Scenario: AC9 No match (legacy RWB-E2-005 AC9)
    When "U-8101" queries approver "U-8199", who approved nothing
    Then the call returns status 200 with no items and total 0
    Then SCR-38 shows the empty state

  Scenario: AC10 A population of cases (legacy RWB-E2-005 AC10)
    Given cases "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" have 6, 2 and 4 entries
    When "U-8101" calls GET /decision-log with caseIds for the three cases
    Then 12 entries return, grouped by case and in chain_seq order within each case

  Scenario: AC11 The ledger query that does not answer inside the budget returns no page (new, D-RCV-60)
    Given the ledger read of the query runs past the 2 s budget of BR13
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12"
    Then the call returns status 503 with message MSG-GEN-006
    Then no page is returned, not even a partial one

  Scenario: AC12 An entry asked for by ID that is absent or outside the scope is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns "U-8104" with the Decision log right "R" and scope "OWN"
    Given the rwb-case contract mock returns case "RW-2026-000123" with an owner other than "U-8104"
    When "U-8104" asks for the entry with chain_seq 230 of case "RW-2026-000123" by ID
    Then the call returns status 404 with message MSG-P4-003
    Then when "U-8101" asks by ID for an entry that does not exist in case "RW-2026-000123", the call returns status 404 with message MSG-P4-003
    Then nothing is recorded as a successful read

  Scenario: AC13 The rules without a criterion hold on every query (new, D-RCV-60)
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500
    Then no entry is changed or purged, and the service login holds SELECT on decision_log_entry only
    Then the page is ordered by chain_seq, and personal fields appear only in recommendation and actions

  Scenario: AC14 The provided operations answer 401 without a token and 404 for an absent entry (new, D-RCV-60)
    When a caller without a valid token calls GET /decision-log
    Then the call returns status 401 with message Not specified in the source documents (GAP-1249)
    Then when "U-8101" asks by ID for an entry that does not exist in case "RW-2026-000123", the call returns status 404 with message MSG-P4-003

  Scenario: AC15 A consumed call that fails or does not answer returns no page (new, D-RCV-60)
    Given the rwb-access contract mock does not answer within the 2 s budget of BR13
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12"
    Then the GET is retried once and the call returns status 503 with message MSG-GEN-006
    Then no page is returned, not even a partial one
```

The ten criteria above are the legacy criteria of RWB-E2-005, copied line for line with the origin tag on each scenario and one mock line added where a criterion names a fact of another owner: the right and the scope of rwb-access, the case ownership of rwb-case for the scope test, and the rule change audit report for the reconciliation of AC2. The paths in the criteria are the paths of the operations as the legacy story names them; the base of this service is `/api/recovery/decision/v1` and the full paths are those of section 12.1 (DP-13). Every value of the legacy criteria — the six `chain_seq` values, "LIT-2026.12", the 200 and the 14 and the 3, the 6, 2 and 4 entries, "U-8101" to "U-8104" and "U-8199", the dates, the message identifiers and the 1 to 500 and 500 limits — is kept unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Audit can query the ledger for a population of cases and receive inputs, versions, approver and final call | REQ-DRI-012; FEAT-CHO-11 |
| BR2 | The scope filters entries through their case before any is returned, and the excluded count is never shown; the case facts of the scope test come from the rwb-case read in the contract dependencies | LOV-SCOPE; legacy BR2; Admin and access model, section 4.3 |
| BR3 | Every returned entry is checked against the canonical form and against the entry before it | REQ-DRI-003; canonical form of RWB-P7-E1008-APP |
| BR4 | An entry that does not verify is returned flagged, never hidden, and one incident per entry goes to the Compliance queue read from platform configuration | NFR-035; REQ-DRI-002; legacy BR4 |
| BR5 | Every query and every export writes one access record naming the filter and the row count, through the local decision-record library | REQ-ACA-006; DP-03; RWB-PLT-E1027-CON |
| BR6 | Page size is 1 to `rwb.decision.query.max-size` and a population holds at most `rwb.decision.query.max-cases` cases, both parameters and not code | DP-06; legacy BR6; DL11 (open; assumptions ASM-0553, ASM-0703, ASM-1051, ASM-1104) |
| BR7 | The ledger is read only through this service: nothing in the query path changes an entry, and the service login holds SELECT on `decision_log_entry` only | REQ-DRI-002; ADR-009; DP-01 |
| BR8 | The ledger is `decision_log_entry` in `rwb_decision` and it is P7's; this story reads it and writes no other service's table | Architecture v5 slides 14, 29 and 41; DP-01 |
| BR9 | The right, the role and the scope come from the authorise contract of rwb-access through the guard library, which carries the scope kind and the case-scope predicate applied to the case ID of each entry inside the query; no role name and no scope value is written in code | DP-08; FSD P4 access model; RWB-P4-E1037-CON |
| BR10 | The decision codes, the approval levels and the scope values are reference rows of rwb-case read with the version in force | DP-07; RWB-P3-E1043-CON |
| BR11 | The access record of a query or an export is a local decision record in the access-event shape, written in the same transaction as the read and relayed on `rwb.decision-record.v1` | DP-03; RWB-PLT-E1027-CON AC2; ASM-2214 |
| BR12 | A read that cannot be recorded is not answered: the page is withheld, the status is 503 and an incident is raised | Principle 5; R-UNI-39; MSG-P7-003 |
| BR13 | Every cross-service call is one hop with a 2 s budget, a GET retried once with jitter and a breaker per downstream; a timeout never returns a page as clean | DP-11; ADR-020 |
| BR14 | No data lake and no reporting copy is written or read on the query path; the legacy lake analysis is retired and the reporting read model takes the events | DP-17; ADR-018; GAP-1244; ASM-2208 |
| BR15 | The answer carries IDs, codes, versions, hashes, dates and counts and carries personal data only in `recommendation` and `actions`; a personal field in those two is masked per the masking policy before it is returned or exported; the field list of personal data is Not specified in the source documents (DOR-RWB-P7-E2005-APP-11) | NFR-039; NFR-040; Template and Rules §R7.2 s17 |
| BR16 | The page order is `chain_seq`; within a population of cases the answer is grouped by case and ordered by `chain_seq` inside each case | Legacy AC1 and AC10; REQ-DRI-003 |
| BR17 | The retention of the ledger is Compliance's and is not yet a value, so nothing in this story purges, archives or truncates an entry | NFR-030; DL26 (open; assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355); GAP-1241 |

### 9. State transitions

None. This story changes no case status and no ledger entry: it reads `decision_log_entry` and writes only an access record. The two verdicts it sets are computed per answer and are never stored.

| Object | Value in the answer | Meaning |
|---|---|---|
| Returned entry | `chainVerified` true | The entry hash matches its canonical form and its `prev_hash` matches the entry before it |
| Returned entry | `chainVerified` false | One of the two checks failed; the entry is still returned, the warning names it, and an incident is raised |
| Returned entry | Absent from the page | The case is outside the caller's scope; the count of excluded entries is not disclosed |
| Query | Served | The access record was written and the page is returned |
| Query | Refused | The access record could not be written, or the store did not answer; no page is returned |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Queries and exports every entry: Decision log R with scope ALL |
| RW-COMPLY, Compliance and PDPA officer | Queries and exports with scope ALL, and receives the incident for an entry that does not verify |
| RW-RISK, RW-COE | Query and export with Decision log R and scope ALL |
| RW-CASEOWN and other roles holding Decision log R | Query the entries of the cases in their scope |
| RW-PHONECOL and roles without Decision log R | Refused with MSG-P4-002 |
| rwb-decision service identity | Reads its own schema, writes the access record through the library, and holds no write grant on `decision_log_entry` |
| Decision-record library identity | Writes the AC-READ and AC-EXPT record and relays it on `rwb.decision-record.v1` (DP-03) |
| Compliance queue | Receives one incident per entry that fails the chain check (AC5) |

The letters are the legacy ones of RWB-E2-005 section 10, kept unchanged. The role-to-right matrix behind them is rwb-access's and is read through the authorise contract (DP-08); this story writes no role name and no right into code.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Read |
| DF-DEC-002 | decision_log_entry | case_id | Read (the scope test and the grouping of AC10) |
| DF-DEC-003 | decision_log_entry | decision_code | Read (the `decision` filter) |
| DF-DEC-004 | decision_log_entry | rule_id | Read (the `ruleId` filter and the answer) |
| DF-DEC-005 | decision_log_entry | rule_version | Read (the `ruleVersion` filter and the answer) |
| DF-DEC-006, DF-DEC-007 | decision_log_entry | model_version, agent_version | Read (the version group of the answer) |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read (the answer names the inputs snapshot; the snapshot itself is not returned) |
| DF-DEC-009, DF-DEC-014, DF-DEC-015 | decision_log_entry | recommendation, actions, outcome | Read, masked per the masking policy before return or export |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read (the `approver` filter and the answer) |
| DF-DEC-011 | decision_log_entry | approval_level | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read, masked per the masking policy |
| DF-DEC-016 | decision_log_entry | decided_at | Read (the `from` and `to` filter and the created time of the answer) |
| DF-DEC-017, DF-DEC-018 | decision_log_entry | prev_hash, entry_hash | Read (the chain check and the answer) |
| DF-DEC-028 | decision_log_entry | chain_seq | Read (the page order and the sequence of the answer) |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Read (the answer names the entry a correction corrects) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read (the actor of the answer) |
| DF-DEC-031 | decision_log_entry | idempotency_key | Not read: it is the writer's key and it is not part of an audit answer |
| DF-DEC-001 to DF-DEC-018, DF-DEC-030 | local decision record, through the library | decision code AC-READ or AC-EXPT, filter reference, row count, actor, decided at, chain link | Write through the library, never a direct row |
| DF-CAS-009, DF-CAS-011 | recovery_case, through the rwb-case contract | owner_user_id, team_code | Read through the contract for the scope test, never a table |

Two indexes carry the story: `ix_declog_approver_time` on `decision_log_entry (approver_user_id, decided_at)` is added by this story for the query of AC4, and the legacy indexes `ix_declog_case_time`, `ix_declog_rule` and `ix_declog_actor_time` of RWB-P7-E1008-APP serve the case, rule and actor filters. The migration is one per-service Flyway step in the `rwb-decision` sequence, `V2005_1__declog_approver_index.sql`, and it changes no column, no key and no trigger of the table (DP-15; GAP-1246). No personal data is a column of an answer: the answer carries a user identifier, a case identifier, a decision code, hashes and dates, and the free-text fields of `recommendation`, `actions` and `override_reason` are masked per the policy before they leave the service. Field IDs are those in the Logical Data Model and Data Dictionary.

Whether the audit role may see an unmasked person key is Not specified in the source documents (GAP-1243; ASM-2207): the legacy story masks the personal fields of `recommendation` and `actions` before export and gives no other rule, so this story masks under the policy of rwb-access, offers no unmasking operation on either read, and holds the value as an open gap for Compliance and the data steward.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-decision (P7); base `/api/recovery/decision/v1`. The shapes are those fixed in RWB-P7-E2005-CON; this story implements them and adds no path.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P7-006 | GET | `/decision-log` | Search the central ledger by case, cases, decision, rule, rule version, approver and period, and page the answer | Decision log, right R, scope applied | Not applicable, read only |
| API-P7-007 | GET | `/decision-log/{entryId}` | Read one ledger entry with its inputs reference, its versions and its chain verdict | Decision log, right R, scope applied | Not applicable, read only |

Request: the query parameters `caseId`, `caseIds` (comma separated, at most `rwb.decision.query.max-cases`), `decision`, `ruleId`, `ruleVersion`, `approver`, `from`, `to`, `page` and `size`, and the header `Accept: text/csv` for the export of the same result. Answer: `DecisionLogPage` with `items`, `page`, `size`, `total` and `messageCodes`, and `DecisionLogEntry` with the elements fixed in RWB-P7-E2005-CON section 12.1; the export answers the same rows as CSV with a header row.

Errors: 401 no session (message Not specified in the source documents (CG-ALL-7064)); 403 the role lacks Decision log R (MSG-P4-002); 404 the entry is absent or out of scope (MSG-P4-003); 422 a filter fails validation (MSG-GEN-002, MSG-GEN-003); 503 the access record cannot be written (MSG-P7-003) or the ledger does not answer (MSG-GEN-006). A response that contains a failing entry carries the warning MSG-P7-012 in `messageCodes` with status 200, never an error status.

#### 12.2 REST operations consumed

| Method and path | Owner | Contract | Use in this story |
|---|---|---|---|
| POST authorise read (role, scope, DoA) | P4 rwb-access | RWB-P4-E1037-CON, through the guard library RWB-PLT-E1037-CON | The Decision log right R and the caller's scope of every read; cached for the token's life (DP-08) |
| GET parameter read | P3 rwb-case | RWB-P3-E1042-CON, through RWB-PLT-E1042-CON | `rwb.decision.query.max-size` and `rwb.decision.query.max-cases` (DP-06) |
| GET reference-data read | P3 rwb-case | RWB-P3-E1043-CON, through RWB-PLT-E1043-CON | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE read with the version in force (DP-07) |
| GET case read with owner and queue | P3 rwb-case | RWB-P3-E2041-CON (the C row of this story); faked | The case facts of the scope test of AC6; the scope source and the shape of this read are Not specified in the source documents (GAP-1245; ASM-2209) |
| GET the rule change audit report | P3 rwb-case | RWB-P3-E2041-CON; faked | The count per rule package version that AC2 reconciles to |
| GET the access-log read | P4 rwb-access | RWB-P4-E1039-CON; faked | The read-back of the AC-READ and AC-EXPT records in the tests of AC3 and AC8 |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (DP-11, ADR-020). No row reads a table and no row reads a `v_ace_*` view. The access record itself is not a consumed operation: it is written in process through the decision-record library of RWB-PLT-E1027-CON (DP-03).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared topic) | P7 rwb-decision, written by the local library | The entry id, because an access record has no case | decision code AC-READ or AC-EXPT, the filter reference, the row count, the actor reference, the decided-at time, the chain sequence and the entry hash |

The query path publishes no event of `rwb.decision.events.v1`: it is a read, and a read produces no business fact. The one envelope above exists because the access record of BR5 is written as a decision record through the library, in the access-event shape that carries no case and needs no subject group (RWB-PLT-E1027-CON AC2), and the library writes it to the outbox in the same transaction as the read (DP-09 as used by the library, DP-03 here). rwb-decision's own ingest does not consume its own producer's record for the ledger, so no loop is created; the reporting read model and the access log of rwb-access read it.

#### 12.4 Events consumed

None. The query path reads the ledger table it owns and the four contracts of section 12.2; it subscribes to nothing, because a consumer would only add a second, stale copy of the facts it can read at the moment of the question. The ingest of `rwb.decision-record.v1` into the ledger is RWB-P7-E1027-APP and is not this story.

#### 12.5 Workflows and activities

None. The two operations are synchronous reads with a 2 s budget: there is no long-running step, no wait for a human, no durable timer and no compensation, so no workflow and no activity is declared. Running a read inside a Temporal activity would add a replay and codec cost to a screen call that a person waits for (DP-10 not claimed).

#### 12.6 Schedules

None. The two schedules of the ledger — the continuous ingest of JOB-13 and the chain check of JOB-14 at 02:00 with the daily WORM seal — belong to RWB-P7-E1008-APP and RWB-P7-E1027-APP and are named in section 19. This story registers no Schedule, no cron entry and no job name, and reads no shared scheduler table (DP-10 not claimed).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_log_entry | P7 (rwb_decision) | Read only here: the query path holds SELECT only, adds the index `ix_declog_approver_time` in its own Flyway step, and changes no column, key or trigger (BR7, BR8) |
| decision record (local) | P7 rows in `rwb_decision`, written through the P7 library | The AC-READ and AC-EXPT access records of every query and every export (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | The outbox row of the access record and the library objects the service template creates (DP-09 as used by the library) |

Not owned and not declared here: `delegation_limit` is P4 rwb-access's (the DoA table, Architecture v5 slides 14 and 41), `parameter_catalog` and `parameter_value` are P3 rwb-case's, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case's, `recovery_case`, `case_party`, `task` and `timer` are P3 rwb-case's, `approval` is P7's own but belongs to RWB-P7-E2013-APP, and `role`, `permission`, `masking_rule` and `delegation_limit` are P4's. No foreign key crosses a service boundary and no view of another schema is read (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-access authorise fake (RWB-P4-E1037-CON) | The right and the scope of the caller | RW-AUDIT with Decision log R and scope ALL; RW-CASEOWN with scope OWN; RW-PHONECOL refused with MSG-P4-002; a delayed answer beyond 2 s |
| rwb-case parameters fake (RWB-P3-E1042-CON) | The two query limits | max-size 500 and max-cases 500; a changed value read from the parameter row, so no test depends on the code |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE | The legacy decision codes including D5.1 to D9.3 and the access codes AC-DENY, AC-READ and AC-EXPT; the approval levels; the scope values ALL and OWN |
| rwb-case case and rule-change fake (RWB-P3-E2041-CON) | The case read and the rule change audit report | Case "RW-2026-000123" and its owner; the three cases of "U-8104" under "LIT-2026.12"; the report with 200 decisions for "LIT-2026.12"; a case outside the caller's scope |
| rwb-access access-log fake (RWB-P4-E1039-CON) | The read-back of an access record | The AC-READ and AC-EXPT records of a query and an export with their filter reference and row count |
| Ledger and chain fixture (RWB-P7-E1008-APP baseline) | `decision_log_entry` and the canonical form | The set "DL-AUDIT-01": six entries on case "RW-2026-000123" at `chain_seq` 101, 155, 160, 230, 231 and 402; 200 entries under "LIT-2026.12"; 6, 2 and 4 entries on the three cases of AC10; one entry changed with the trigger disabled for AC5 |
| Decision-record library fake (RWB-PLT-E1027-CON) | The write of the access record | A healthy write with `chainSeq` and `entryHash`; a refusal with MSG-P7-009 and the field; an unavailable store for TC-E2-005-12 |

The fakes are derived from the published contracts and from the legacy values of section 16, so a component and a contract test read the same fixtures, and the drift test of RWB-P7-E2005-CON fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | API-P7-006 and API-P7-007 provided; the six rows of 12.2 consumed; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `DecisionRecorded` of the access record, written through the library on the shared topic |
| Temporal | None | No workflow, no activity and no Schedule: the two reads are synchronous |
| File | None | The export is a response body with the media type `text/csv`, not a file interface of rwb-integration |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `ledger` and `audit`, Java packages `th.co.scb.ace.workbench.recovery.decision.ledger` and `...decision.audit`. The front end is the SCR-38 page served through gateway-bff.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap where the story needs lake data (GAP-1244) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for DP-02 (the login is the service's and is not this story's), DP-04 (this story evaluates no rule), DP-05 (no ACE view is read: the ledger is P7's own table), DP-09 (the outbox is the library's, declared by RWB-PLT-E1027-CON and RWB-PLT-TE006-CON, not by this story), DP-10 (no job and no workflow), DP-12 (no case workflow), DP-14 (this story renames no topic), DP-16 (no integration adapter), DP-18 (the interaction ledger is rwb-source-data's and this story neither reads nor writes it) or DP-20 (no agent client).

**Hardware and software change.** The story needs no new infrastructure: it adds two read operations and one index to the schema that RWB-P7-E1008-APP already creates in the ACE PostgreSQL server, uses the Kafka platform for the shared decision-record topic, and reads the existing gateway route. The legacy approver index migration is renumbered into the `rwb-decision` Flyway sequence as `V2005_1__declog_approver_index.sql`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the problem mapping for 401, 403, 404, 422 and 503 |
| FilterValidator | Service | Validates the filters against the two parameters and the three lists; names the field in the refusal |
| ScopeFilter | Service | Applies the scope of the authorise answer to the case of each entry inside the query and to the case of a single entry |
| DecisionLogQueryService | Service | Builds the paged query in `chain_seq` order from the filter set, and groups a population by case |
| ResultChainCheck | Service | Recomputes `entry_hash` from the canonical form per entry, compares `prev_hash` with the previous `entry_hash`, and reads one extra row per page |
| ChainMismatchNotifier | Service | Raises one incident per entry that fails, to the Compliance queue, with the entry id and the case |
| DecisionLogCsvWriter | Service | Streams the export with a header row and `chainVerified` on every row |
| AccessRecorder | Service | Writes the AC-READ and AC-EXPT record through the library in the caller's transaction, and fails the read closed when it cannot |
| CaseScopeClient | Adapter | The case read with owner and queue on the rwb-case contract, for the scope test |
| RuleChangeReportClient | Adapter | The count per rule package version on the rwb-case contract, for the reconciliation of AC2 and the tests |
| DecisionLogQueryScreen | React component | SCR-38 with the filters, the results, the `chainVerified` column, the warning banner and the export |

**Database and migrations**

- Reads `decision_log_entry` in `rwb_decision` only, through the service login, with SELECT and no write grant (BR7).
- One migration in this story: `V2005_1__declog_approver_index.sql` adds `ix_declog_approver_time` on `(approver_user_id, decided_at)` for AC4. It adds no column, no constraint and no trigger, and it changes no file of RWB-P7-E1008-APP (GAP-1246; ASM-2210).
- Writes the local decision record and the library objects, all in `rwb_decision`, through the library and the service template.

**Configuration and reference data**

- `rwb.decision.query.max-size` = 500 and `rwb.decision.query.max-cases` = 500, read as parameters (DP-06). The two values are the legacy ones and the legacy story marks them assumed (DL11).
- LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE read with the version in force (DP-07).
- The Compliance incident queue and the incident severity of a chain mismatch are read from the platform configuration; the queue name is Not specified in the source documents (GAP-1245; ASM-2209).
- The feature switch `rwb.decision.audit-query`, read as a parameter: off answers 503 without reading the ledger, so a broken chain check is never served as a clean page.

**Build steps**

1. DecisionLogController and DecisionLogQueryService over the two operations, with the paging shape of RWB-P7-E2005-CON; tests for AC1, AC9 and AC10.
2. FilterValidator onto the two parameters and the three lists; tests for AC7, including the boundary of 500 case IDs and the size 1000 case.
3. ScopeFilter and CaseScopeClient; tests for AC6 and the out-of-scope read of a single entry.
4. ResultChainCheck with the canonical form, the extra read per page and the boundary at `chain_seq` 1; tests for AC1 and AC5.
5. ChainMismatchNotifier with one incident per failing entry; test for AC5.
6. AccessRecorder with the fail-closed path; tests for AC3, AC8 and TC-E2-005-12.
7. DecisionLogCsvWriter and the export path behind the same request; test for AC8.
8. RuleChangeReportClient and the reconciliation test of AC2 against the report fake.
9. SCR-38 with the loading, results, warning, export and empty states, served through the gateway-bff route.
10. The performance check over 10,000 matching entries against the 3 second target of ASM-2211, with the target read from a parameter so a change of the number is a change of data.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P7-E2005-CON stay green, the count of AC2 reconciles to the rule change audit report in SIT, a query over 10,000 entries answers its first page inside the target read from the parameter, and no query or export in the SIT log exists without its AC-READ or AC-EXPT record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-012 | A returned entry does not match the chain | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P4-002 | The query is made without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The entry is absent, or its case is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-002 | The size or the case list is outside the limit | {field} must be between {min} and {max}. |
| MSG-GEN-003 | The from date is after the to date | {field} cannot be before {other}. |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The ledger does not answer inside the budget | {system} is not available. Try again in a few minutes. |
| MSG-P7-009 | Not specified in the source documents (DOR-RWB-P7-E2005-APP-9) | Not specified in the source documents (DOR-RWB-P7-E2005-APP-9) |

MSG-P7-012, MSG-P4-002, MSG-GEN-002, MSG-GEN-003 and MSG-P7-003 are copied unchanged from RWB-E2-005 section 14; MSG-P4-003 and MSG-GEN-006 are the platform messages of the access and unavailable paths. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863), as the legacy story states; the proposed Thai for MSG-P7-012 is in the legacy additions file and is not published by any source read here.

### 15. Screens and states

SCR-38 Decision log query is served through the gateway-bff composite route (DP-19), and the field list, the masking and the timeout budget of the route belong to RWB-PLT-N001-CON. The panel on SCR-38 is Not specified in the source documents (GAP-1339). The composite query route path and merge order are Not specified in the source documents (GAP-0387).

| Screen | State | What the user does |
|---|---|---|
| SCR-38 Decision log query | Loading | Waits while the first page loads; skeleton rows |
| SCR-38 Decision log query | Results | Reads the entries with case, decision, rule and version, approver, level, final call, decided at and the `chainVerified` column; pages through; sees MSG-P7-012 at the top when an entry fails |
| SCR-38 Decision log query | Export | Downloads the CSV of the full result, and sees the row count that the AC-EXPT record holds; the export delivery against the 2 s budget, the size cap, column order and file name are Not specified in the source documents (GAP-1242) |
| SCR-38 Decision log query | Empty (common state) | Sees a sentence saying no entry matches the filters |
| SCR-38 Decision log query | Refused | Sees MSG-P4-002 when the role lacks the right, and MSG-P7-003 when the read could not be recorded |
| SCR-38 Decision log query | Error | Not specified in the source documents (CG-ALL-7070) |
| SCR-38 Decision log query | No access | Not specified in the source documents (CG-ALL-7070) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-005-01 | AC1, BR1, BR3, BR16 | End to end | Case with six synthetic entries |
| TC-E2-005-02 | AC2, BR1 | End to end | 200 entries under LIT-2026.12 and the rule change audit report |
| TC-E2-005-03 | AC3, BR5 | End to end | RW-PHONECOL test user |
| TC-E2-005-04 | AC4, BR1 | End to end | Approver with 14 December and 3 November entries |
| TC-E2-005-05 | AC5, BR4 | End to end | One entry changed in SIT with the trigger disabled |
| TC-E2-005-06 | AC6, BR2 | End to end | RW-CASEOWN test user owning 3 of the cases |
| TC-E2-005-07 | AC7, BR6 | End to end | Reversed dates; size 1000 |
| TC-E2-005-08 | AC8, BR5 | End to end | Export of 200 entries |
| TC-E2-005-09 | AC9 | End to end | Approver with no entries |
| TC-E2-005-10 | AC10, BR1 | End to end | Three cases with 6, 2 and 4 entries |
| TC-E2-005-11 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-005-12 | Principle 5, BR11, BR12 | NFR | The decision log write of the access event forced to fail; the query returns nothing |
| TC-E2-005-13 | AC11, BR13 | NFR | Ledger read held past the 2 s budget |
| TC-E2-005-14 | AC12, BR2, BR9 | End to end | Entry 230 of RW-2026-000123 asked for by U-8104, whose case has another owner |
| TC-E2-005-15 | Section 12, BR9, BR10, BR13, BR14, BR15 | Contract | Contract mocks of rwb-access and rwb-case for the operations of section 12 |
| TC-E2-005-16 | Section 12.7, BR7, BR8, BR17 | Component | Service login tried with a write on decision_log_entry; SELECT only |
| TC-E2-005-17 | AC13, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17 | Component | RW-AUDIT test user and the ledger of DL-AUDIT-01 |
| TC-E2-005-18 | AC14 | Contract | Call without a token; entry ID that does not exist |
| TC-E2-005-19 | AC15, BR13 | NFR | rwb-access contract mock held past the 2 s budget |

The twelve cases are the legacy cases of this key, kept in the legacy order with their covers and their data unchanged; the legacy level System maps to End to end, Access to Component and Resilience to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The end-to-end evidence across the real services is carried by `RWB-ITG-E2005-ITG`, which holds the `-ITG` copies of these twelve cases.

### 17. Guardrails

- No business value in code: the two limits, the performance target, the decision codes, the approval levels and the scope values are parameters and reference rows read with the version in force.
- No personal data in events, logs, tests or prompts: the answer carries user identifiers, case identifiers, codes, versions, hashes, dates and counts; the free-text fields of an entry are masked per the policy before they are returned or exported (NFR-039, NFR-040).
- No read of another service's tables and no `v_ace_*` read: the right, the scope, the case facts, the limits and the lists arrive on the owner's contract (DP-01, DP-08).
- ACE data only through the owner's contract or the owner's views: this service reads no ACE row, because the ledger is P7's own table.
- The query path holds SELECT on `decision_log_entry` only; no statement of the query path updates, deletes or truncates an entry, and the append-only trigger of RWB-P7-E1008-APP is never disabled.
- A read that cannot be recorded is not served: the page is withheld, the status is 503 and an incident is raised (R-UNI-39).
- An entry that fails the chain check is shown, never dropped, and never silently corrected (BR4).
- No data lake and no reporting copy on the query path; the reporting read model takes the events (DP-17, ADR-018).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`; the shared decision-record topic is named only as the library's (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never returns a page as clean and never passes a scope test (DP-11).
- Every example and every fixture is synthetic; no production decision record is copied into a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-012 | Audit queries the ledger for a population of cases with inputs, versions, approver and final call | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-CHO-11 | 17 Run the decision center | BR1, BR2, BR6, BR16 | TC-E2-005-01, TC-E2-005-02, TC-E2-005-04, TC-E2-005-06, TC-E2-005-09, TC-E2-005-10, TC-E2-005-13, TC-E2-005-14, TC-E2-005-15 |
| REQ-DRI-003 | The ledger is hash chained and the chain integrity is checked | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR3, BR4, BR16 | TC-E2-005-01, TC-E2-005-05, TC-E2-005-10 |
| REQ-ACA-006 | Every read of the case store and the document store is written to the access log | Business Requirements Epic 2, section 4; Program, section 5.4 | FEAT-ACA-06 | 16 Manage risk, control and compliance | BR5, BR11, BR12 | TC-E2-005-03, TC-E2-005-08, TC-E2-005-12 |
| REQ-DRI-002 | The ledger is append only and a correction is a new record naming the one it corrects | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR4, BR7, BR8 | TC-E2-005-01, TC-E2-005-05, TC-E2-005-16 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-005, disposition Split (rework) |
| Legacy criteria owned here | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, each tagged (legacy RWB-E2-005 ACn); AC11 to AC15 are new under D-RCV-60 and carry no legacy tag |
| Test cases | TC-E2-005-01 to TC-E2-005-19; TC-E2-005-01 to TC-E2-005-12 in the legacy order, TC-E2-005-13 to TC-E2-005-19 new under D-RCV-60 |
| Decoupling patterns | DP01, DP03, DP06, DP07, DP08, DP11, DP13, DP15, DP17, DP19 |
| Architecture decisions | ADR-009 (append-only log that blocks an action it cannot record), ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-018 (no data lake), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Non-functional requirements | NFR-030 (retention, open under DL26), NFR-033 (every decision reproducible), NFR-035 (daily chain check, same-day report), NFR-036 (audit request answered inside its deadline), NFR-039 and NFR-040 (masking and data minimisation) |
| Rules | R-UNI-39 (no action without its record) |

The supporting features of the legacy key — FEAT-CHO-11 (query the log for audit), FEAT-DRI-01 (store the entries append-only and hash chained) and FEAT-ACA-06 (write the access log) — are answered here for the rwb-decision slice and by the other services for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The contract document, the OpenAPI and AsyncAPI fragments, the message mapping and the fakes as published artefacts: RWB-P7-E2005-CON.
- The ledger store, the canonical form, the append-only rule, the verifier and the daily chain check of JOB-14 with the WORM seal: RWB-P7-E1008-APP, RWB-P7-E1008-CON and RWB-P7-E1008-DB.
- The continuous ingest of JOB-13 and the completeness boundary of 5 minutes: RWB-P7-E1027-APP and RWB-P7-E1027-CON.
- The approval queue and the approval operations: RWB-P7-E2013-APP and RWB-P7-E2013-CON.
- The D7.1 approval screen: RWB-P7-E2014-APP and RWB-P7-E2014-CON.
- The nightly check of the whole chain as a job and its alerting: named above with the store, and not built here (the per-entry check of this story is a read-time check, not the daily job).
- The QA sample against the rule version applied (Epic 8, FEAT-ADM-08) and the rule change governance of rwb-case (RWB-P3-E2041-APP and RWB-P3-E2041-CON): this story reads the report and never produces it.
- Analysis on the data lake copy of the ledger: RWB-E1-014, retired under DP-17 with no target path; the reporting read model takes the events instead.
- The access log screen, the break-glass path and the access records of other capabilities: P4 rwb-access, RWB-P4-E1039-APP and RWB-P4-E1039-CON.
- The gateway-bff composite route, its field list, its masking and its timeout budget: RWB-PLT-N001-CON.
- The end-to-end journey across the real services: `RWB-ITG-E2005-ITG`.
- The deployment, the dashboards, the alerts and the runbook of this capability: no operations story is allocated to this key in the plan.
