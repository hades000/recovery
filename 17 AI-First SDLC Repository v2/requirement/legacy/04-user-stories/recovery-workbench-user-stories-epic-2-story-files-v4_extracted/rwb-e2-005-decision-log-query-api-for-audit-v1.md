<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 005 Decision log query API for audit v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 005 Decision log query API for audit v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-005 Decision log query API for audit

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-005 |
| Epic | E2, release 31 December 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-CHO-11 Query the decision log for audit |
| Requirement IDs | REQ-DRI-012 |
| BRD section | Business Requirements Epic 2, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-E1-039 |
| Status | Ready for build |

## 1. Story

As an **internal auditor (RW-AUDIT)**, I want **to query the decision log by case or a population of cases, decision, approver, date and rule version, with the hash chain checked on every entry returned, and to export the result**, so that **an audit question is answered from the log in minutes, and I can rely on each entry I am given**.

## 2. Business rationale

Audit and the regulator ask for the decision history of a sample of cases: inputs, versions, approver and final call. Today this is assembled by hand from e-mails and files. This story gives one query over the append-only log, filtered by the caller's scope, with each returned entry checked against the chain and a flag on any entry that does not match. It meets REQ-DRI-012 and NFR-036 (an audit request answered inside its deadline). The measure is the time to answer an audit sample: the first page of a query over 10,000 matching entries in 3 seconds or less (assumed; DL11).

## 3. Preconditions

- RWB-E1-008 is done: the store, the canonical form and the verifier.
- RWB-E1-039 is done: access events are written to the decision log.
- RWB-E1-048 is done: the rule change audit report gives the count of decisions per rule version, for reconciliation.
- Test users hold RW-AUDIT (scope ALL), RW-CASEOWN (scope OWN) and RW-PHONECOL (no Decision log letter) in SIT.
- The SIT store holds the synthetic set used below.

## 4. Flow

1. Internal auditor: opens SCR-38 Decision log query and enters the filters: case or list of cases, decision, rule ID, rule version, approver, from and to.
2. ACE front end: calls GET /decision-log with the filters, page and size.
3. Workbench (DecisionLogQueryService): validates the filters; applies the caller's scope through the case of each entry; runs the query in chain_seq order.
4. Workbench (ResultChainCheck): for each entry on the page, recomputes entry_hash from the canonical form and compares prev_hash with the entry before it; sets chainVerified on the entry.
5. Workbench: where an entry does not verify, returns it with chainVerified false and the warning, and raises an incident to Compliance once per entry.
6. Workbench: writes one AC-READ access event with the filter and the row count.
7. Internal auditor: selects export; the Workbench returns the full result as CSV and writes one AC-EXPT access event with the filter and the row count.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without Decision log R queries | Refused with 403; refusal logged | MSG-P4-002 | AC3 |
| X2 | A returned entry does not match the chain | The entry is returned with chainVerified false; warning shown; incident to Compliance | MSG-P7-012 | AC5 |
| X3 | The caller's scope excludes some matching entries | Only entries of cases in scope return; the excluded count is not shown | None | AC6 |
| X4 | From is after to, or size is outside 1 to 500, or more than 500 case IDs are given | Refused with 422 naming the field | MSG-GEN-003, MSG-GEN-002 | AC7 |
| X5 | No entry matches | 200 with an empty page and total 0; the screen shows the empty state | None | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the store from RWB-E1-008 and writes access events through RWB-E1-039 |
| Negotiable | Page size limits and the performance target are parameters (DL11) |
| Valuable | Audit samples are answered from the log with each entry checked |
| Estimable | One query service, one per-entry check, one export, one screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Decision log query API for audit

  Background:
    Given the environment is SIT with the synthetic decision log set "DL-AUDIT-01"
    Given test user "U-8101" holds RW-AUDIT with scope "ALL"

  Scenario: AC1 Query by case
    Given case "RW-2026-000123" has six entries with chain_seq 101, 155, 160, 230, 231 and 402
    When "U-8101" calls GET /decision-log with caseId of that case
    Then the six entries return in chain_seq order
    Then each entry carries chainVerified true

  Scenario: AC2 Query by rule version
    Given rule R-LIT-03 at version "LIT-2026.12" was used in 200 decisions
    When "U-8101" calls GET /decision-log with ruleId "R-LIT-03" and ruleVersion "LIT-2026.12" and size 500
    Then 200 entries return and total is 200
    Then the total equals the count for "LIT-2026.12" in the rule change audit report

  Scenario: AC3 Access
    Given test user "U-8102" holds only RW-PHONECOL, whose Decision log letter is "-"
    When the user calls GET /decision-log
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then one entry with decision code "AC-DENY", area "DECISION_LOG" and right "R" is written

  Scenario: AC4 Query by approver and period
    Given approver "U-8103" approved 14 decisions between 1 and 31 December 2026 and 3 in November 2026
    When "U-8101" calls GET /decision-log with approver "U-8103", from "2026-12-01" and to "2026-12-31"
    Then 14 entries return with approverUserId "U-8103" and approvalLevel filled

  Scenario: AC5 An entry that does not match the chain is flagged
    Given the entry with chain_seq 230 was changed in the SIT database with the trigger disabled
    When "U-8101" queries case "RW-2026-000123"
    Then six entries return and entry 230 carries chainVerified false
    Then the response carries warning MSG-P7-012 naming entry 230
    Then the system raises one incident to the Compliance queue for entry 230

  Scenario: AC6 Scope limits the result
    Given test user "U-8104" holds RW-CASEOWN with scope "OWN" and owns 3 of the cases decided under "LIT-2026.12"
    When "U-8104" queries ruleVersion "LIT-2026.12"
    Then only the entries of those 3 cases return and total counts only them

  Scenario: AC7 Invalid filters are refused
    When "U-8101" calls GET /decision-log with from "2026-12-31" and to "2026-12-01"
    Then the call returns status 422 with message MSG-GEN-003 for field "from"
    Then when "U-8101" calls it with size 1000
    Then the call returns status 422 with message MSG-GEN-002 for field "size" with min 1 and max 500

  Scenario: AC8 Export
    Given the query of AC2 returns 200 entries
    When "U-8101" exports the result from SCR-38
    Then a CSV file with a header row and 200 entry rows is returned, with chainVerified on each row
    Then one entry with decision code "AC-EXPT", the filter and row count 200 is written

  Scenario: AC9 No match
    When "U-8101" queries approver "U-8199", who approved nothing
    Then the call returns status 200 with no items and total 0
    Then SCR-38 shows the empty state

  Scenario: AC10 A population of cases
    Given cases "RW-2026-000123", "RW-2026-000124" and "RW-2026-000125" have 6, 2 and 4 entries
    When "U-8101" calls GET /decision-log with caseIds for the three cases
    Then 12 entries return, grouped by case and in chain_seq order within each case
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Audit can query the log for a population of cases and receive inputs, versions, approver and final call | REQ-DRI-012 |
| BR2 | Scope filters entries through their case before any is returned; the excluded count is never shown | LOV-SCOPE; Admin and access model, section 4.3 |
| BR3 | Every returned entry is checked against the canonical form and the entry before it | REQ-DRI-003; canonical form, RWB-E1-008 |
| BR4 | An entry that does not verify is returned flagged, never hidden, and raises an incident to Compliance | NFR-035 |
| BR5 | Every query and export writes an access event with the filter and the row count | REQ-ACA-006; RWB-E1-039 |
| BR6 | Page size is 1 to 500; a population holds at most 500 cases | Parameters rwb.decision.query.max-size=500, rwb.decision.query.max-cases=500 (assumed; DL11) |
| BR7 | The log is read only through this service; nothing in the query path changes an entry | REQ-DRI-002; ADR-009 |

## 9. State transitions

None. This story does not change a case status, and it changes no entry.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT Internal audit | Queries and exports every entry (Decision log R, scope ALL) |
| RW-COMPLY Compliance and PDPA officer | Queries and exports (Decision log R, scope ALL); receives incidents for entries that do not verify |
| RW-RISK, RW-COE | Query and export (Decision log R, scope ALL) |
| RW-CASEOWN and other roles holding Decision log R | Query entries of cases in their scope |
| RW-PHONECOL and roles without Decision log R | Refused |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (AC-READ and AC-EXPT access events through the writer) |
| DF-CAS-009 | recovery_case | owner_user_id | Read by the P3 scope filter interface |
| DF-CAS-011 | recovery_case | team_code | Read by the P3 scope filter interface |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /decision-log** (API-P7-006)

| Item | Value |
|---|---|
| Request | Query: caseId, decision, ruleId, approver, from, to, page, size; added in this story: caseIds (comma separated, at most 500), ruleVersion; Accept text/csv for export (additions file) |
| Response | DecisionLogPage: items (DecisionLogEntry plus chainVerified, added in this story), page, size, total; warning MSG-P7-012 when any entry fails; CSV with the same columns for export |
| Errors | 401; 403 no Decision log R (MSG-P4-002); 422 invalid filter (MSG-GEN-002, MSG-GEN-003); 503 the access event cannot be written (MSG-P7-003) or the store is unavailable (MSG-GEN-006) |
| Authorization | Decision log, right R, scope applied |
| Idempotency | Not applicable, read only |

**GET /api/recovery/v1/decision-log/{entryId}** (API-P7-007): the same per-entry check and chainVerified flag.

**Published interface used:** ScopeService.scopeFor (P4, RWB-E1-037); the P3 interface `Set<UUID> casesInScope(ScopeFilter filter, Collection<UUID> caseIds)`.

## 13. Solution plan

- Package: folder `recovery/decision/audit` in the recovery module; Java package `recovery.decision.audit`. Front end: `recovery/decision/audit`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionCenterAndLogController | Controller | GET /decision-log with the new filters and the CSV export |
| DecisionLogQueryService | Service | Validates filters, applies scope, pages in chain_seq order |
| ResultChainCheck | Service | Per-entry recomputation with CanonicalEntryForm and the prev_hash check, one extra read per page for the entry before the first |
| ChainMismatchNotifier | Service | Raises one incident per entry that fails, to Compliance |
| DecisionLogCsvWriter | Service | Streams the CSV export |
| DecisionLogQueryScreen | React component | SCR-38 with the filters, results, chainVerified column and export |

- Database: reads decision_log_entry; uses ix_declog_case_time, ix_declog_rule and ix_declog_actor_time (RWB-E1-008); adds index ix_declog_approver_time on (approver_user_id, decided_at) with Flyway migration V_E2_005__declog_approver_index.sql.
- Configuration and reference data: parameters rwb.decision.query.max-size and rwb.decision.query.max-cases (500, assumed, DL11); Compliance incident queue.
- Build steps:
  1. Add the approver index migration.
  2. Build DecisionLogQueryService with the filters and validation; tests for AC2, AC4, AC7, AC9, AC10.
  3. Apply scope through the P3 interface; test AC6.
  4. Build ResultChainCheck and ChainMismatchNotifier; tests for AC1 and AC5.
  5. Write AC-READ and AC-EXPT access events through RWB-E1-039; tests for AC3 and AC8.
  6. Build DecisionLogCsvWriter; test AC8.
  7. Build SCR-38 with the loading, results, empty and export states.
  8. Run the performance check over 10,000 matching entries against the 3 second target.
- Feature flag: `rwb.decision.audit-query`.
- Done when: the tests in section 16 pass and the count in AC2 reconciles to the rule change audit report in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-012 | A returned entry does not match the chain (new) | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P4-002 | Query without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-002 | Size or the case list outside the limit | {field} must be between {min} and {max}. |
| MSG-GEN-003 | From after to | {field} cannot be before {other}. |
| MSG-P7-003 | The access event cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows DL10; proposed Thai for MSG-P7-012 is in the additions file.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-38 Decision log query | Loading | Waits while the first page loads; skeleton rows |
| SCR-38 Decision log query | Results | Reads entries with case, decision, rule and version, approver, level, final call, decided at and chainVerified; pages through; sees MSG-P7-012 at the top when an entry fails |
| SCR-38 Decision log query | Export | Downloads the CSV of the full result |
| SCR-38 Decision log query | Empty (common state) | Sees a sentence saying no entry matches the filters |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-005-01 | AC1, BR1, BR3 | System | Case with six synthetic entries |
| TC-E2-005-02 | AC2, BR1 | System | 200 entries under LIT-2026.12 and the rule change audit report |
| TC-E2-005-03 | AC3, BR5 | System | RW-PHONECOL test user |
| TC-E2-005-04 | AC4, BR1 | System | Approver with 14 December and 3 November entries |
| TC-E2-005-05 | AC5, BR4 | System | One entry changed in SIT with the trigger disabled |
| TC-E2-005-06 | AC6, BR2 | System | RW-CASEOWN test user owning 3 of the cases |
| TC-E2-005-07 | AC7, BR6 | System | Reversed dates; size 1000 |
| TC-E2-005-08 | AC8, BR5 | System | Export of 200 entries |
| TC-E2-005-09 | AC9 | System | Approver with no entries |
| TC-E2-005-10 | AC10, BR1 | System | Three cases with 6, 2 and 4 entries |
| TC-E2-005-11 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-005-12 | Principle 5 | Resilience | The decision log write of the access event forced to fail; the query returns nothing |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: limits and the target are parameters.
- No personal data in logs, tests or prompts; the export holds references and codes, and personal fields in recommendation or actions are masked per the masking rules before export.
- No read of another module's tables; scope comes through the P3 interface.
- No write to any entry from the query path.
- An entry that fails the check is shown, never dropped.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-012 | Audit queries the log for a population of cases with inputs, versions, approver and final call | Epic 2, 3.7 | FEAT-CHO-11 | 17 Run the decision center | BR1 to BR7 | TC-E2-005-01 to TC-E2-005-12 |

## 19. Out of scope

- The nightly check of the whole chain (RWB-TE-008).
- The approval queue and the decision screen SCR-10 and SCR-11 (RWB-E2-013, RWB-E2-014).
- The QA sample against the rule version applied (Epic 8, FEAT-ADM-08).
- Analysis on the data lake copy (RWB-E1-014).
