# RWB-ITG-E2005-ITG Decision log query API for audit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2005-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2005-ITG-16); the squad sets the size at refinement |
| Depends on (build) | RWB-P3-E2041-APP, RWB-P4-E1039-APP, RWB-P7-E2005-APP (not done yet) |
| Contract dependencies | The decision-log query contract of rwb-decision; contract story key Not specified in the source documents (DOR-RWB-ITG-E2005-ITG-21) |
| Contract version | Major version 1 of the decision-log query contract (path /v1); rwb-decision.yaml of API Specification v5, info.version 5.0.0 |
| Integration dependencies | RWB-P4-E1039-APP, RWB-P3-E2041-APP, RWB-P7-E2005-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015, FR-PLT-019, FR-PLT-026, FR-PLT-033) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-005 for the wave 2 integration harness. The harness proves the cross-service decision-log query deliverable on the owner's own endpoint: the query, the filters, the paging and the CSV export of `rwb_decision` served by rwb-decision at its own base, the chain verification performed inside rwb-decision and never repaired by the harness, the scope answered by rwb-access and never read from a table, the totals reconciled with the rule-change audit report, the refusal and its denial record written in the same transaction, the tampered entry flagged with its warning and its Compliance incident, and the end of the retired data-lake copy of the log, with one evidence report per run. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 8 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and test team (QA)**, I want **a repeatable cross-service harness that queries the decision log by case, by rule version, by approver and period and by a population of cases through rwb-decision, that has the caller's rights and scope answered by rwb-access, that reconciles the totals with the rule-change audit report of rwb-decision, that exports the result as a CSV stream and that records each entry's chain check, with one evidence report per run**, so that **an audit question is proved to be answerable from the append-only log in minutes across the services that now own its parts — with every entry checked, every refusal recorded, no scope taken from a table and no data-lake path left in the log — before the wave is accepted and after every release**.

This story is the wave 2 integration harness for the legacy key. It builds no production screen, endpoint, table, workflow or schedule and it owns no table. The behaviour under test is owned by the three I stories: RWB-P7-E2005-APP (the query API on `rwb_decision` at the owner's own base, the filters, the paging, the CSV export stream and the per-entry chain verification), RWB-P4-E1039-APP (the rights and scope answer the query filters on) and RWB-P3-E2041-APP (the rule-change audit report the totals must agree with). The harness builds the runner, the fakes, the seeds and the evidence, and it owns the nine acceptance criteria of section 7.

### 2. Business rationale

Audit and the regulator ask for the decision history of a sample of cases: inputs, versions, approver and final call. In the legacy monolith that history was read from one schema and one query service, and the same story also copied the log to a data lake. In the target architecture the history is split across services: rwb-decision owns the append-only decision log, its entry hashes and the central ledger; rwb-access owns the roles, the scope and the Decision log right the query filters on; rwb-case owns the case facts behind a case-id filter; and there is no data lake at all, so the export is a stream from rwb-decision and any reporting read model is built from events into rwb-reporting.

A defect at any of those seams would only be found by an auditor with a live case: a scope filter that reads an access table directly instead of asking rwb-access, a chain check that returns a stale flag, a total that no longer reconciles with the rule-change report, a refusal that writes no denial record, or an export that still leaves through a lake path. This story exercises those seams in one run per business date and attaches one evidence report per run, so the audit answer can be shown to hold before the wave is accepted and after every change. It meets REQ-DRI-012, REQ-DRI-003, REQ-ACA-006 and REQ-DRI-002 at the integration level, and it leaves every business rule, every screen behaviour and every table with the owning stories.

### 3. Preconditions

- The three I stories are published and deployed in the SIT environment as they land: RWB-P7-E2005-APP (the query API, the filters, the paging, the export stream and the chain verification on `rwb_decision`), RWB-P4-E1039-APP (the rights and scope answer the query filters on) and RWB-P3-E2041-APP (the rule change audit report the totals must agree with).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The SIT store holds the synthetic decision log set "DL-AUDIT-01": case "RW-2026-000123" with six entries with chain_seq 101, 155, 160, 230, 231 and 402; cases "RW-2026-000124" with 2 entries and "RW-2026-000125" with 4 entries; rule "R-LIT-03" at version "LIT-2026.12" used in 200 decisions; approver "U-8103" with 14 approval entries between 1 and 31 December 2026 and 3 in November 2026; and an approver "U-8199" who approved nothing.
- The synthetic users exist and are seeded through the access contract: "U-8101" (RW-AUDIT with scope ALL), "U-8102" (RW-PHONECOL only, whose Decision log right is "-"), "U-8104" (RW-CASEOWN with scope OWN, owning 3 of the cases decided under "LIT-2026.12") and "U-8103" and "U-8199" as the approvers above.
- The page-size bounds are those of the legacy story: size 1 to 500, and a population of at most 500 case ids.
- The tampered copy of entry 230 is prepared in the SIT store by the owning service's test support with the append-only trigger disabled, because the harness never writes another service's schema; the harness reads the flagged result and asserts it.
- Feature `rwb.decision.audit-query` is on in the harness environment, so the query and the export are served; the harness reads the flag through the platform library and asserts the off state with the fakes.
- The harness repository, the SIT and UAT environments, the seeding of the six-entry case set, the 200 "LIT-2026.12" entries and the tampered entry, the per-run evidence format and retention, the pass/fail gate and the gateway-bff composite route detail are Not specified in the source documents (GAP-0387; ASM-0562).
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands.

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the harness pack version and the fake or real mode of each of the owning services it touches.
2. Harness: seeds the run through the contract of each owning service, or through the fake in fake mode — the three cases with their 6, 2 and 4 entries, the 200 entries of "R-LIT-03" at "LIT-2026.12", the 14 December and 3 November entries of approver "U-8103", the four synthetic users with their roles and scopes, and the tampered entry 230.
3. Harness: queries `GET /api/recovery/decision/v1/decision-log` with caseId of "RW-2026-000123" as "U-8101" and asserts the six entries in chain_seq order, each with chainVerified true, and that the answer came from rwb-decision with no join to another service's table (AC1).
4. Harness: queries with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500, asserts 200 entries and total 200, then reads `GET /api/recovery/decision/v1/admin/rule-packages/change-report` for the same version and asserts the two counts are equal (AC2).
5. Harness: repeats the query as "U-8102" with RW-PHONECOL and asserts 403 with MSG-P4-002, then reads back one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" written locally by rwb-decision in the same transaction (AC3).
6. Harness: queries approver "U-8103" from 2026-12-01 to 2026-12-31 as "U-8101" and asserts the 14 entries with approverUserId and approvalLevel filled, and that the 3 November entries are excluded (AC4).
7. Harness: queries case "RW-2026-000123" again with entry 230 tampered and asserts six entries return, entry 230 carries chainVerified false, the response carries MSG-P7-012 naming entry 230, and one incident is raised to the Compliance queue for it (AC5).
8. Harness: queries ruleVersion "LIT-2026.12" as "U-8104" with RW-CASEOWN and scope OWN and asserts only the entries of the 3 cases it owns return and total counts only them, with the scope read from the rwb-access answer and not from any table (AC6).
9. Harness: sends the invalid filters — from 2026-12-31 with to 2026-12-01, and size 1000 — and asserts 422 with MSG-GEN-003 for field "from" and 422 with MSG-GEN-002 for field "size" with min 1 and max 500 (AC7).
10. Harness: exports the AC2 result as "U-8101" and asserts a CSV with a header row and 200 entry rows with chainVerified on each row, one entry with decision code "AC-EXPT" carrying the filter and the row count 200, no data-lake extract and no INT-19 or INT-20 interface, and then queries approver "U-8199" and asserts 200 with total 0 (AC8).
11. Harness: queries caseIds of "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" together and asserts 12 entries grouped by case and ordered within each case, and fails the run on a cross-schema read, on a call that is not one hop with a 2 s timeout, on a scope that is not the rwb-access answer and on an export that leaves through a lake path (AC9).
12. Harness: publishes the evidence report keyed by story id and business date, releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Decision log R queries | 403; no entry returned; one denial entry with decision code "AC-DENY" written in the same transaction | MSG-P4-002 | AC3; TC-E2-005-03-ITG |
| X2 | A returned entry does not match the chain (entry 230 tampered) | The entry is returned with chainVerified false, the response carries the warning naming entry 230, and one incident is raised to the Compliance queue | MSG-P7-012 | AC5; TC-E2-005-05-ITG |
| X3 | The caller's scope excludes some matching entries | Only entries of cases in scope return; total counts only them; the excluded count is not shown | None | AC6; TC-E2-005-06-ITG |
| X4 | From is after to, or size is outside 1 to 500 | The call is refused with 422 naming the field | MSG-GEN-003, MSG-GEN-002 | AC7; TC-E2-005-07-ITG |
| X5 | No entry matches | 200 with an empty page and total 0; the screen shows the empty state | None | AC8; TC-E2-005-09-ITG |
| X6 | The export is asked for a result larger than one page | The CSV carries the whole filtered result and not the current page, each row keeping its chainVerified value | None | AC8; TC-E2-005-08-ITG |
| X7 | The trace shows a cross-schema read, a second hop, a scope not answered by rwb-access, or an export through a lake path | The run fails and names the seam; no criterion passes on that run | None | AC9; TC-E2-005-10-ITG |

The harness asserts the status, the message id and the substituted values of every refusal, and never rewrites a message text.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the three I stories are deployed; until then it runs against the §12.8 fakes, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes, the evidence format and the gate are configuration and data; the criteria are the legacy behaviour at the cross-service seam |
| Valuable | The audit answer is proved to hold across rwb-decision, rwb-access and rwb-case, with the chain checked and no lake path left in the log |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each of the twelve `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Decision log query API for audit - wave 2 integration harness

  Background:
    Given the environment is SIT with the synthetic decision log set "DL-AUDIT-01"
    Given test user "U-8101" holds RW-AUDIT with scope "ALL"

  Scenario: AC1 Query by case on the owner's own endpoint (new, D-RCV-60)
    Given case "RW-2026-000123" has six entries with chain_seq 101, 155, 160, 230, 231 and 402
    When "U-8101" calls GET /api/recovery/decision/v1/decision-log with caseId of that case
    Then the six entries return in chain_seq order
    And each entry carries chainVerified true
    And the answer is served by rwb-decision at /api/recovery/decision/v1 from its own table rwb_decision decision_log_entry, with no join to another service's table
    And the trace holds no cross-schema read and no second hop

  Scenario: AC2 Query by rule version and the reconciled total (new, D-RCV-60)
    Given rule "R-LIT-03" at version "LIT-2026.12" was used in 200 decisions
    When "U-8101" calls GET /api/recovery/decision/v1/decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500
    Then 200 entries return and total is 200
    And the total equals the count for "LIT-2026.12" returned by GET /api/recovery/decision/v1/admin/rule-packages/change-report for the same period and version in rwb-decision
    And both answers are read through their own contract and neither service recomputes the other's count

  Scenario: AC3 Rights refuse the call and the denial is written in the same transaction (new, D-RCV-60)
    Given test user "U-8102" holds only RW-PHONECOL, whose Decision log right is "-"
    When "U-8102" calls GET /api/recovery/decision/v1/decision-log
    Then rwb-access refuses the call and the response is 403 with message MSG-P4-002
    And one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" is written locally by rwb-decision in the same transaction
    And no entry of any case is returned to "U-8102"

  Scenario: AC4 Query by approver and period (new, D-RCV-60)
    Given approver "U-8103" approved 14 decisions between 1 and 31 December 2026 and 3 in November 2026
    When "U-8101" calls GET /api/recovery/decision/v1/decision-log with approver "U-8103", from "2026-12-01" and to "2026-12-31"
    Then 14 entries return with approverUserId "U-8103" and approvalLevel filled on each
    And the 3 November 2026 entries are excluded

  Scenario: AC5 An entry that does not match the chain is flagged, never hidden (new, D-RCV-60)
    Given the entry with chain_seq 230 was changed in the SIT store with the append-only trigger disabled
    When "U-8101" queries case "RW-2026-000123"
    Then six entries return and entry 230 carries chainVerified false
    And the response carries messageCodes with MSG-P7-012 naming entry 230
    And the system raises one incident to the Compliance queue for entry 230
    And the harness repairs no entry and writes no entry of rwb-decision

  Scenario: AC6 Scope limits the result and comes from rwb-access (new, D-RCV-60)
    Given test user "U-8104" holds RW-CASEOWN with scope "OWN" and owns 3 of the cases decided under "LIT-2026.12"
    When "U-8104" queries ruleVersion "LIT-2026.12"
    Then only the entries of those 3 cases return and total counts only them
    And the excluded count is not shown
    And the scope is the answer of GET /api/recovery/access/v1/me/session and is not read from any table of rwb-decision

  Scenario: AC7 Invalid filters are refused (new, D-RCV-60)
    When "U-8101" calls GET /api/recovery/decision/v1/decision-log with from "2026-12-31" and to "2026-12-01"
    Then the call returns status 422 with message MSG-GEN-003 for field "from"
    When "U-8101" calls it with size 1000
    Then the call returns status 422 with message MSG-GEN-002 for field "size" with min 1 and max 500
    And no entry is returned and nothing is written by either refused call

  Scenario: AC8 Export streams from rwb-decision, and the data-lake copy is gone (new, D-RCV-60)
    Given the query of AC2 returns 200 entries
    When "U-8101" exports the result of that query as Accept text/csv
    Then a CSV with a header row and 200 entry rows is returned, with chainVerified on each row
    And the export streams page by page inside rwb-decision, with the 2 s budget read per page of 500 rows; the export size cap, the column order and the file name are Not specified in the source documents (GAP-1242)
    And one entry with decision code "AC-EXPT", the filter and row count 200 is written
    And no data-lake extract is called and no INT-19 or INT-20 interface is exercised, because there is no data lake and the retired copy RWB-E1-014 has no replacement
    When "U-8101" queries approver "U-8199", who approved nothing
    Then the call returns status 200 with no items and total 0

  Scenario: AC9 The boundary and the multiple-case query (new, D-RCV-60)
    Given cases "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" have 6, 2 and 4 entries
    When "U-8101" calls GET /api/recovery/decision/v1/decision-log with caseIds for the three cases
    Then 12 entries return, grouped by case and in chain_seq order within each case
    And the run fails on any cross-schema read in the trace
    And the run fails on any call that is not one hop with a 2 s timeout, read per page of 500 rows for the export
    And the run fails on any scope that is not the rwb-access answer
    And the run fails on any export that leaves through a lake path

  Scenario: AC10 The realignment rules BR7 to BR10 are asserted at the owning services (new, D-RCV-60)
    Given the runs of AC1 to AC9 have finished on "DL-AUDIT-01"
    Then the scope of each query is the rwb-access answer and no table of rwb-access is read (BR7)
    And the chain is verified and kept in rwb-decision, and each entry is written by its own service (BR8)
    And no step changes or deletes an entry (BR9)
    And no data-lake or Power BI path is called (BR10)

  Scenario: AC11 A redelivered decision-record event is applied once (new, D-RCV-60)
    Given the access event of the export in AC8 is relayed on rwb.decision-record.v1
    When the same event is delivered a second time
    Then the P4 access log holds one record for that event
    And the second delivery writes no entry and changes none
```

These eleven criteria AC1 to AC11 are new for the ITG harness. The legacy criteria AC1 to AC10 stay with RWB-P7-E2005-APP and are not restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Audit can query the log for a population of cases and receive inputs, versions, approver and final call | REQ-DRI-012 |
| BR2 | Scope filters entries through their case before any is returned; the excluded count is never shown | LOV-SCOPE; Admin and access model, section 4.3 |
| BR3 | Every returned entry is checked against the canonical form and the entry before it | REQ-DRI-003; canonical form, RWB-E1-008 |
| BR4 | An entry that does not verify is returned flagged, never hidden, and raises an incident to the Compliance queue read from platform configuration | NFR-035 |
| BR5 | Every query and export writes an access event with the filter and the row count; the event is written locally through the decision-record library and relayed on rwb.decision-record.v1, and the P4 access log reads the relayed record for its view; no read path calls P4 to write | REQ-ACA-006; RWB-E1-039 |
| BR6 | Page size is 1 to 500; a population holds at most 500 cases | Parameters rwb.decision.query.max-size=500, rwb.decision.query.max-cases=500 (assumed; DL11); first-page target of 3 s for 500 rows over 10,000 matching entries, carried as a parameter whose key is Not specified in the source documents (GAP-1247) |
| BR7 | The scope of the caller is the answer of rwb-access through its contract; the answer carries the scope kind and the case-scope predicate, which the service applies to the case ID of each entry inside the query, and the case facts of the scope test come from the P3 case read; no service reads an access table and no caller joins to one | DP-08; REQ-ACA-009; R-PREC default ruling |
| BR8 | The decision log is local to the owning service and centralised in rwb-decision: each service writes its own decision record in its own schema in the same transaction, and rwb-decision collects it into the central ledger and verifies the chain there | ADR-022; Architecture v5 slide 20 and slide 14 (Schedules: chain check 02:00) |
| BR9 | The log is append only: no query, export, refusal or harness step changes or deletes an entry, and a correction is a new entry naming the one it corrects | REQ-DRI-002; ADR-009 |
| BR10 | There is no data lake and no Power BI feed: the export is a stream from rwb-decision and any reporting read model is built from events into rwb-reporting | DP-17; ADR-018; Architecture v5 slide 37 and slide 44 (JOB-13 and JOB-15 have no lake) |

BR1 to BR6 are the legacy rules of RWB-E2-005 with their sources; they are copied word for word, except that BR4, BR5 and BR6 carry added detail for this harness. BR7 to BR10 are the realignment rules this harness proves; the harness asserts them against the owning services and the published contracts and re-implements none of them.

Open decisions that apply to this story are DL10 and DL11. DL10 has the assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL11 has the assumptions ASM-0553, ASM-0703, ASM-1051 and ASM-1104. Both decisions are still open, and each assumption stands until its decision is closed.

### 9. State transitions

None. This story changes no case status and no case state; the harness reads and asserts records only, and it adds no transition of its own. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| The refusal record with decision code "AC-DENY" written with the refused call | rwb-decision, in the same transaction as the refusal | One denial entry with area "DECISION_LOG" and right "R", no entry returned (TC-E2-005-03-ITG) |
| The export record with decision code "AC-EXPT" written with the export | rwb-decision, with the filter and the row count | One export entry with row count 200 (TC-E2-005-08-ITG) |
| Entry 230 returned with chainVerified false and warning MSG-P7-012 | rwb-decision chain verification, over a tampered SIT entry | The flag, the warning naming entry 230 and one Compliance incident (TC-E2-005-05-ITG) |
| The scope answer for "U-8104" limiting the result | rwb-access, through the session contract | 3 cases and a total that counts only them (TC-E2-005-06-ITG) |
| The count of decisions for "LIT-2026.12" in the change report | rwb-decision, from `rule_id` and `rule_version` | Equality of the query total and the report count (TC-E2-005-02-ITG) |
| The case facts behind the case-id filters | rwb-case, through its contract | The six-entry, 2-entry and 4-entry answers (TC-E2-005-01-ITG, TC-E2-005-10-ITG) |

The harness writes no entry, repairs no chain and changes no case; when it finds a broken chain it records the finding and the incident and leaves the store exactly as it was.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Queries and exports every entry (Decision log R, scope ALL); the synthetic user the harness drives |
| RW-CASEOWN, case owner | Queries entries of cases in scope (Decision log R, scope OWN); drives the scope boundary of AC6 |
| RW-PHONECOL, phone collections officer | Holds no Decision log right; the access case proves the refusal with MSG-P4-002 |
| RW-COMPLY, Compliance and PDPA officer | Receives the incident for an entry that does not verify; reads and exports (Decision log R, scope ALL) |
| RW-COE, center of excellence analyst | Reads the query and the rule-change report (Decision log R); changes nothing |
| RW-PLATADM, platform administrator | Reads the query and the export for a platform check; used by the access case only |
| QA lead | Owns the harness pack, the seeds, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Platform edge owner | Owns the gateway-bff composite route in SIT and UAT |

No delegation of authority level applies: this story takes no credit decision. The Decision log right is answered by rwb-access through the session contract of §12.2.

### 11. Data

The harness owns no table (DP-01). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (DOR-RWB-ITG-E2005-ITG-7) | decision_log_entry | all fields of decision_log_entry as LDM v9 lists them, including the approver user id, the approval level, the final call, the decided time, prev hash and entry hash | Read through the P7 contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through the P7 contract |
| DF-DEC-005 | decision_log_entry | rule_version | Read through the P7 contract |
| DF-DEC-016 | decision_log_entry | decided_at | Read through the P7 contract |
| DF-DEC-028 | decision_log_entry | chain_seq | Read through the P7 contract |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read through the P7 contract |
| DF-CAS-001 | recovery_case | id | Read through the P3 contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 contract |
| DF-CAS-011 | recovery_case | team_code | Read through the P3 contract |

The role, the scope and the Decision log right of the caller are read from rwb-access (`role`, `permission`) only through `GET /api/recovery/access/v1/me/session`; they are never joined from a table and the harness holds no copy. The tables are owned as follows: `decision_log_entry` and `approval` in schema `rwb_decision` by P7 rwb-decision (RWB-P7-E2005-APP); `role` and `permission` in schema `rwb_access` by P4 rwb-access; `recovery_case` in schema `rwb_case` by P3 rwb-case. The harness owns no table and writes none of them.

Test data is synthetic. No production case, party, approver or decision entry is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness serves no operation; it calls the owning services and their fakes.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The query by case, caseIds, rule, rule version, approver and period with page and size, and the CSV export through `Accept: text/csv` (AC1, AC2, AC4, AC5, AC6, AC7, AC8, AC9) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The single entry with the same chainVerified flag, read for the tampered entry 230 and for the denial and export entries (AC3, AC5, AC8) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/change-report` | P7 rwb-decision | The decisions per rule package version the query total of "LIT-2026.12" is reconciled with (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts behind the case-id filter and the ownership of the 3 cases of AC6 (AC1, AC6, AC9) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the scope and the Decision log right of the caller, asserted on AC3 and AC6 |

The SCR-38 query and export answers the screen consumes are read through the gateway-bff composite route (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path, its merge order and the way it composes the query answer with the case facts are Not specified in the source documents (GAP-0387; ASM-0562).

#### 12.3 Events published

None. The harness publishes no Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision owns the event type, the topic and the central ledger; every service writes its local record and publishes it (EV-08) | The refusal record with decision code "AC-DENY" and the export record with decision code "AC-EXPT" reach the central ledger with the filter and the row count, and the six entries of case "RW-2026-000123" and the 200 entries of "LIT-2026.12" are in the ledger with rule ID, rule version and chain fields (AC1, AC2, AC3, AC8) |

The harness consumes the topic as a test consumer with its own group and asserts the entries through the P7 contract; it holds no inbox table, gets no production record and publishes nothing. No case event is consumed: the query filters on the case id through the P3 contract, and the event design gives no case event that this query filters on.

#### 12.5 Workflows and activities

None added. The harness starts no Temporal workflow, calls no activity and uses no queue `rwb-decision`. The chain check of rwb-decision is a Temporal Schedule, not a workflow (JOB-14), and the harness reads its result and starts nothing.

#### 12.6 Schedules

None added and none started. The harness reads the chain check schedule of rwb-decision, JOB-14 at 02:00 (Architecture v5 slide 44; Temporal and Drools Design slide 16), as the job that would catch a break after this run; the harness never starts it, never pauses it and never changes it.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01, DP-15 resolves to no migration). The decision log tables `decision_log_entry` and `approval` in schema `rwb_decision` are owned by RWB-P7-E2005-APP, and the harness reads them only through the P7 contract.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-decision (WireMock, from its OpenAPI) | `GET /api/recovery/decision/v1/decision-log`, `GET /api/recovery/decision/v1/decision-log/{entryId}` and `GET /api/recovery/decision/v1/admin/rule-packages/change-report`, with the set "DL-AUDIT-01": case "RW-2026-000123" with chain_seq 101, 155, 160, 230, 231, 402 and chainVerified true, cases "RW-2026-000124" with 2 and "RW-2026-000125" with 4 entries, 200 entries and total 200 for "R-LIT-03" "LIT-2026.12", the matching change-report count, approver "U-8103" with 14 December and 3 November entries, approver "U-8199" with total 0, the tampered entry 230 with chainVerified false and MSG-P7-012, the denial entry "AC-DENY", the export entry "AC-EXPT", the CSV answer of 200 rows, 422 with MSG-GEN-003 naming "from" and 422 with MSG-GEN-002 naming "size" with min 1 and max 500 | AC1 to AC9 |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` for "U-8101" with RW-AUDIT and scope ALL, "U-8102" with RW-PHONECOL and Decision log "-", "U-8103" and "U-8199" as approvers, and "U-8104" with RW-CASEOWN and scope OWN over the 3 cases | AC3, AC6; the access case |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases/{caseId}` with the three cases, their owners and teams, and the 3 cases owned by "U-8104" | AC1, AC6, AC9 |
| gateway-bff composite query route (WireMock) | The one gateway answer the SCR-38 states are read from, composing the query answer with the case facts | AC1 to AC9 |

The fakes are published from the owning services' OpenAPI documents, are versioned with the harness pack and are replaced by the real service as each I story lands. The harness repository, the SIT and UAT environments, the seeding, the evidence format and retention, the gate and the composite route detail are Not specified in the source documents (GAP-0387; ASM-0562).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13); the CSV export is the same `GET /api/recovery/decision/v1/decision-log` read as a stream |
| Kafka | 0 published, 1 consumed: `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (EV-08) |
| Temporal | None: no workflow, no activity, no queue; the JOB-14 chain check is read and never started |
| File | None: the CSV is a REST response read as text and compared row by row; the harness writes no file to a service and calls no file interface |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-17 is the ruling as it stands: the data lake is removed, there is no lake copy of the decision log, the legacy copy RWB-E1-014 is retired with no replacement and JOB-13 is continuous Kafka ingest in rwb-decision, so reporting is built from events into rwb-reporting. A gap is raised only if the story needs lake data, and it does not: the export is a CSV stream from rwb-decision at `/api/recovery/decision/v1`, and the harness asserts that no INT-19 or INT-20 interface is exercised. DP-15 resolves to no migration because the harness owns no schema.

The platform H dependencies named in the table (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) and the C dependencies RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON are held by the service and platform stories and are not repeated in the metadata columns, which stay None. DP-06 is the parameters contract of rwb-case, where the page bounds of BR6 are held and read rather than written into the harness; DP-07 is its reference-data contract, which the harness builds against for a filter value and reads only where a value it needs to seed a filter is a reference row; and DP-08 is carried by RWB-P4-E1037-CON, because the scope and the Decision log right are the rwb-access answer and are never a table read. The blocking dependencies of this story are the three I stories, which replace the fakes with the real behaviour; they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogJourneyRunner | Test harness | Runs the twelve `-ITG` cases of §16 in one run per business date, in fake or real mode per service, and stops at the first failed assertion with the trace |
| DecisionLogClient | Harness adapter | Calls the five consumed operations of §12.2 with caseId, caseIds, ruleId, ruleVersion, approver, from, to, page, size and `Accept: text/csv`, and records the answer |
| ChainCheckAsserter | Assertion | Asserts chainVerified on every returned entry, the chain_seq order, the flag and the warning on the tampered entry 230, and the single Compliance incident |
| ScopeAsserter | Assertion | Asserts that the scope of "U-8104" is the rwb-access answer, that only the 3 owned cases return, and that the total counts only them |
| RightsAsserter | Assertion | Asserts 403 with MSG-P4-002 for "U-8102" and the "AC-DENY" denial entry written in the same transaction |
| FilterAsserter | Assertion | Asserts 422 with MSG-GEN-003 naming "from" and 422 with MSG-GEN-002 naming "size" with min 1 and max 500 |
| TotalReconciler | Assertion | Compares the query total for "LIT-2026.12" with the change-report count and fails the run on any difference |
| ExportAsserter | Assertion | Asserts one header row, 200 entry rows, chainVerified on each row and the "AC-EXPT" entry with the filter and row count 200 |
| LakePathGuard | Assertion | Fails the run on any lake extract, any INT-19 or INT-20 call and any export that leaves through a path other than the rwb-decision response stream |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema read or any trace deeper than one hop, so no service reads another service's tables |
| FakePack | WireMock project | Serves rwb-decision, rwb-access, rwb-case and the gateway-bff composite query route from the published OpenAPI documents |
| DecisionLogSeedLoader | Service | Seeds the three cases, the 200 entries, the approver entries, the four users and the tampered entry through the owner's contract or the fake |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01, DP-15).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.decision.audit-query` on in both. The data are the synthetic seeds of the legacy story: the set "DL-AUDIT-01" with case "RW-2026-000123" and its six entries with chain_seq 101, 155, 160, 230, 231 and 402, cases "RW-2026-000124" with 2 entries and "RW-2026-000125" with 4, rule "R-LIT-03" at "LIT-2026.12" with 200 decisions, approver "U-8103" with 14 December and 3 November entries, approver "U-8199" with none, and users "U-8101" (RW-AUDIT, ALL), "U-8102" (RW-PHONECOL), "U-8104" (RW-CASEOWN, OWN, 3 cases). Each run starts from the seeded state, so a repeated run is deterministic. The harness repository, the environments, the seeding of the six-entry case set, the 200 entries and the tampered entry, the evidence format and retention and the gate are Not specified in the source documents (GAP-0387; ASM-0562).

**Build steps**

1. Build DecisionLogJourneyRunner and DecisionLogClient against the published OpenAPI documents of the owning services and the gateway-bff route.
2. Publish FakePack for rwb-decision, rwb-access, rwb-case and the composite route from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write DecisionLogSeedLoader and the seed files, with the run lock and the fake or real mode per service.
4. Write ChainCheckAsserter and TotalReconciler for AC1, AC2 and AC5, with a unit test on fixtures for chain_seq order, chainVerified and the warning naming entry 230.
5. Write RightsAsserter, ScopeAsserter and FilterAsserter for AC3, AC6 and AC7, including the denial entry of the same transaction and the two 422 answers.
6. Write ExportAsserter and LakePathGuard for AC8, asserting the header row, the 200 rows, chainVerified on each row, the "AC-EXPT" entry, the empty answer of "U-8199" and the absence of any lake path.
7. Write SchemaBoundaryCheck and the boundary assertions of AC9, then replace each fake with the real service as its I story lands, in the order rwb-access, rwb-decision, rwb-case, and rerun in UAT.
8. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.

**Feature switch.** `rwb.decision.audit-query`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — the query operation is not served, no entry is returned and no denial or export entry is written — and asserts that the log is unchanged in that state.

**Done when.** The twelve `-ITG` test cases of section 16 pass in SIT and UAT with the three I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the nine owned criteria green; the query total for "LIT-2026.12" reconciles with the change-report count; and the access case, the empty answer and the tampered-entry warning are green with the messages and statuses of section 14.

### 14. Validation and messages

| ID | When | Message | Answer |
|---|---|---|---|
| MSG-P7-012 | A returned entry does not match the chain (new) | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. | 200 with the entry flagged and the warning naming entry 230 |
| MSG-P4-002 | Query without Decision log R | You cannot {action} here. Your role does not include it. | 403 for "U-8102" |
| MSG-GEN-002 | Size or the case list outside the limit | {field} must be between {min} and {max}. | 422 for field "size" with min 1 and max 500 |
| MSG-GEN-003 | From after to | {field} cannot be before {other}. | 422 for field "from" |

The harness asserts the message id, the rendered text, the substituted values and the status of each row, and it never rewrites a message. The empty answer of "U-8199" is 200 with no items and total 0 and carries no message. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-38 Decision log query | Loading | The first answer of a run returns the six entries of "RW-2026-000123" in chain_seq order, read as one gateway answer through the composite route |
| SCR-38 Decision log query | Results | Each entry carries case, decision, rule and version, approver, level, final call, decided time and chainVerified; the approver query of AC4 returns 14 entries |
| SCR-38 Decision log query | Warning | The top of the answer carries MSG-P7-012 naming entry 230 while the six entries still return, entry 230 flagged |
| SCR-38 Decision log query | Export | The export answer is a CSV with a header row and 200 entry rows, with chainVerified on each row |
| SCR-38 Decision log query | Empty | The approver "U-8199" answer is 200 with no items and total 0, and no error; the screen shows a sentence saying no entry matches the filters |
| SCR-38 Decision log query | Error | When the read cannot be recorded, the answer is 503 with MSG-P7-003 and returns no entries |
| SCR-38 Decision log query | No access | A role without the Decision log right gets 403 with MSG-P4-002 and no entries |
| SCR-38 Decision log query | Loading | Not specified in the source documents (CG-ALL-567) |

The harness opens no screen and renders no page: it asserts the composite route answer the screen consumes. Screen-level behaviour stays with RWB-P7-E2005-APP, and the composite route path, its merge order and the way it composes the answer are Not specified in the source documents (GAP-0387; ASM-0562).

### 16. Test cases

Harness and evidence. The harness repository, the SIT and UAT environments and the seeding order are Not specified in the source documents (GAP-0387); assumption ASM-B-ITG-W2-01-E2005-1 holds them until the integration lead agrees them with QA. Each run writes one evidence report per story and business date, with one row per criterion, seam, answering service or fake, observed value and result; the report is retained with the release record. The wave gate is every owned criterion green with the three I stories in place. The platform edge owner publishes the gateway-bff composite query route path and merge order in the gateway-bff contract before the screen assertions of section 15 are run. The approver index migration V2005_1__declog_approver_index.sql is added by this story after the table baseline of RWB-P7-E1008-APP, and no file of RWB-P7-E1008-APP is edited.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-005-01-ITG | AC1, BR1, BR3, BR8, BR9; ITG AC1 | Integration | Case "RW-2026-000123" with six entries with chain_seq 101, 155, 160, 230, 231 and 402 |
| TC-E2-005-02-ITG | AC2, BR1; ITG AC2 | Integration | 200 entries under "R-LIT-03" at "LIT-2026.12" and the rule change audit report |
| TC-E2-005-03-ITG | AC3, BR5; ITG AC3 | Integration | RW-PHONECOL test user "U-8102"; the denial entry written in the same transaction |
| TC-E2-005-04-ITG | AC4, BR1; ITG AC4 | Integration | Approver "U-8103" with 14 December and 3 November entries |
| TC-E2-005-05-ITG | AC5, BR4; ITG AC5 | Integration | Entry 230 changed in the SIT store with the trigger disabled; one incident to the Compliance queue |
| TC-E2-005-06-ITG | AC6, BR2, BR7; ITG AC6 | Integration | RW-CASEOWN test user "U-8104" owning 3 of the cases; scope answered by rwb-access |
| TC-E2-005-07-ITG | AC7, BR6; ITG AC7 | Integration | Reversed dates 2026-12-31 to 2026-12-01; size 1000 |
| TC-E2-005-08-ITG | AC8, BR5, BR10; ITG AC8 | Integration | Export of the 200 entries; no lake path; empty answer for "U-8199" |
| TC-E2-005-09-ITG | AC9; ITG AC8 | Integration | Approver "U-8199" with no entries |
| TC-E2-005-10-ITG | AC10, BR1; ITG AC9 | Integration | Three cases "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" with 6, 2 and 4 entries |
| TC-E2-005-11-ITG | Access; ITG AC3 | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-005-12-ITG | Principle 5; ITG AC3 | NFR | The decision record write of the refusal forced to fail; no entry is returned |
| TC-E2-005-13-ITG | AC10, BR7, BR8, BR9, BR10 | Integration | Runs of AC1 to AC9 on "DL-AUDIT-01"; test steps Not specified in the source documents (NEWAC-RWB-ITG-E2005-ITG-AC11) |
| TC-E2-005-14-ITG | AC11, BR5 | Integration | The access event of the AC8 export relayed on rwb.decision-record.v1 and delivered twice; test steps Not specified in the source documents (NEWAC-RWB-ITG-E2005-ITG-AC12) |

The twelve `-ITG` cases assert the same behaviour as the legacy test cases under the same base id and add the cross-service seam each one exercises. The legacy criteria stay with the app stories: this story owns none of them, and the `-ITG` cases add the seam only. TC-E2-005-09-ITG keeps the legacy Covers text "AC9" of the no-match case and asserts the empty answer at the ITG seam; TC-E2-005-10-ITG keeps the legacy "AC10" of the population case and asserts it across the three cases of AC9 here. The full legacy test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the page bounds, the explanation of the totals and the filter values are parameters and data held by rwb-decision; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces, fixtures or reports: the harness uses synthetic case, user and approver identifiers, and no production case, party, approver or decision entry is copied into an export fixture.
- No scope from a table: the scope and the Decision log right are the rwb-access answer through its contract; the SchemaBoundaryCheck fails the run on any access table read and on any join to one.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-decision reads `rwb_decision` (DP-01).
- No lake path: there is no data lake, the retired copy RWB-E1-014 has no replacement, and LakePathGuard fails the run on any lake extract or any INT-19 or INT-20 call (DP-17).
- The chain is verified and never repaired: the harness asserts the flag and the warning, raises nothing of its own, repairs no entry and writes no entry of rwb-decision.
- The log is append only: no query, export, refusal or harness step changes or deletes an entry; a denied call and an export add their own record only.
- No production data and no outside system: the harness calls only the owning services and their fakes, never a production endpoint or an outside gateway.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, and asserts the 2 s budget on every call (DP-11).
- The harness owns no table, no endpoint, no screen, no workflow and no schedule (DP-01, DP-15); it is test and evidence only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-CHO-11 | 17 Run the decision center | BR1; BR2; BR6 | TC-E2-005-01-ITG, TC-E2-005-02-ITG, TC-E2-005-04-ITG, TC-E2-005-06-ITG, TC-E2-005-09-ITG, TC-E2-005-10-ITG |
| REQ-DRI-003 | The decision log is hash chained, and the chain integrity is checked every day with a break reported to Compliance the same day | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR3; BR4; BR8 | TC-E2-005-01-ITG, TC-E2-005-05-ITG |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log | Business Requirements Epic 1, section 4; Program, section 5.4 | FEAT-ACA-01 | All recovery processes | BR5; BR7 | TC-E2-005-03-ITG, TC-E2-005-08-ITG, TC-E2-005-11-ITG, TC-E2-005-12-ITG |
| REQ-DRI-002 | The decision log is append only. A record cannot be changed or deleted, and a correction is a new record naming the one it corrects | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR9 | TC-E2-005-01-ITG, TC-E2-005-05-ITG |

The requirement IDs, their BRD sections and their rule text are those of the legacy story and the source extracts; this story adds no requirement ID of its own and traces all four at the integration level only. The retired data-lake part of REQ-ACA-006 is asserted by AC8 through its removal: no data-lake copy remains, so the read it named is now the export stream from rwb-decision.

### 19. Out of scope

- The three owning I stories and everything they build: RWB-P7-E2005-APP (the query API, the filters, the paging, the CSV export stream and the chain verification on `rwb_decision`), RWB-P4-E1039-APP (the rights and scope answer the query filters on) and RWB-P3-E2041-APP (the rule change audit report the totals must agree with).
- The legacy criteria AC1 to AC10 of RWB-E2-005 and their legacy test cases, which stay with RWB-P7-E2005-APP; this story owns none of them.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-decision, rwb-access and rwb-case, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The retired data-lake copy of the decision log (RWB-E1-014) and the data lake and Power BI feed (INT-19 and INT-20 removed); no new story replaces them.
- The decision log store, its append path, the canonical form, the local decision record and the central ledger ingest (RWB-E1-008, RWB-E1-027, RWB-E1-039, JOB-13).
- The rule change governance harness of the neighbouring integration story RWB-E2-041 (RWB-ITG-E2041-ITG); this run reads its report and does not exercise its load, approval or rollback.
- The approval queue and the decision screens SCR-10 and SCR-11 (RWB-E2-013, RWB-E2-014) and the screen-level behaviour of SCR-38, which stays with RWB-P7-E2005-APP.
- The QA sample against the rule version applied (Epic 8, FEAT-ADM-08) and the daily chain check JOB-14, which the harness reads and never starts.
