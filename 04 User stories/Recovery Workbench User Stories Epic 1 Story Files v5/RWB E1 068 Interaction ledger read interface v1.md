# RWB-E1-068 Interaction ledger read interface

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-068 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-ILG-03 Read the ledger in one ordered sequence |
| Requirement IDs | REQ-ILG-006, REQ-ILG-003, REQ-ILG-014 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-003, REQ-ILG-006, REQ-ILG-014) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-066 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **to read a case's ledger in one ordered sequence, filtered by channel, actor or date range**, so that **I can see what has happened to it before I decide anything**.

## 2. Business rationale

A case owner who decides a route, a settlement or a legal step must first know what was said, promised, sent and done on the case. One read interface returns the ledger in order with the source of each entry, filters it by channel, actor and date range, and masks personal content by role on the same rules as the case record. The case record view and every other consumer read through this interface, so there is one ordering and one masking rule for the history. Serves REQ-ILG-006, REQ-ILG-003 and REQ-ILG-014; NFR-070 (one case history read in under 2 seconds at its 2031 size; DL11).

## 3. Preconditions

- RWB-E1-066 is done: the interaction table carries event_code, actor, source, case_seq and the decision link.
- RWB-E1-037 is done: P4 publishes the masking interface; masking rules may be empty (DL26), in which case every personal field is masked.
- P3 publishes CaseScopeQuery (RWB-E1-016) to check that the caller may see the case.
- The reader holds Case record R.

## 4. Flow

1. Case owner: opens SCR-03 Case record; the history panel calls GET /cases/{caseId}/interactions?page=0&size=50.
2. P3 interactions handler (API-P3-014): checks Case record R and calls InteractionLedgerReader.read() with the caller's context.
3. InteractionLedgerReader: checks the case is in the caller's scope through CaseScopeQuery.
4. InteractionLedgerReader: validates the filter (channel in LOV-CHANNEL, from not after to, size 1 to 200).
5. InteractionLedgerReader: reads the case's entries matching the filter, ordered by occurred_at, then case_seq.
6. InteractionLedgerReader: masks the summary field (is_personal) through the P4 masking interface for the caller's roles.
7. InteractionLedgerReader: writes the read to the PII access log when a personal field is returned unmasked.
8. P3 handler: returns InteractionPage with each entry's event, time, actor, channel, outcome, promise and source.
9. Case owner: filters by channel, actor or date range; the panel calls the same endpoint with the filter.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | from is after to | 422; nothing returned | MSG-GEN-003 | AC4 |
| X2 | The case is outside the caller's scope | 404 | MSG-P4-003 | AC5 |
| X3 | No masking rule allows the caller to see the summary | Summary returned as "MASKED" | None | AC6 |
| X4 | Page size above 200 | 422 | MSG-GEN-002 | AC7 |
| X5 | The case has no entries | 200 with an empty page; the panel shows the Empty state | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the ledger store (RWB-E1-066); masking and scope come from published interfaces of P4 and P3 |
| Negotiable | Page size limits are properties; the story fixes the order, the filters and the masking |
| Valuable | The case owner reads the full history before deciding |
| Estimable | One reader, one endpoint change, one panel |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion is one API call on a synthetic ledger |

## 7. Acceptance criteria

```gherkin
Feature: Interaction ledger read interface

  Background:
    Given case "RW-2026-000401" has 9 ledger entries from 2026-08-04 to 2026-12-06
    Given 3 entries come from EFS with channel CALL between 2026-08-04 and 2026-10-15
    Given 2 entries come from user "u-owner-04" with channel VISIT on 2026-11-10 and 2026-11-20
    Given 4 entries come from the Workbench with no channel between 2026-12-01 and 2026-12-06
    Given user "u-owner-04" holds RW-CASEOWN and owns the case

  Scenario: AC1 The ledger reads in order
    Given a case with entries from several sources
    When user "u-owner-04" calls GET /cases/{caseId}/interactions for case "RW-2026-000401"
    Then 9 entries come back ordered by occurred time, earliest first
    Then each entry names its source system and source reference, for example "EFS, INT-07" or "WORKBENCH, P3 case and workflow"

  Scenario: AC2 It can be filtered
    Given the 9-entry ledger
    When it is read three times: filtered by channel "CALL", by actor "u-owner-04", and from 2026-12-01 to 2026-12-06
    Then the first read returns only the 3 EFS call entries
    Then the second read returns only the 2 VISIT entries
    Then the third read returns only the 4 Workbench entries

  Scenario: AC3 It is available to the case record
    Given the case record view SCR-03 for case "RW-2026-000401"
    When it loads
    Then its history panel shows the 9 entries from GET /cases/{caseId}/interactions
    Then the architecture test finds no class outside the ledger package that queries the interaction table

  Scenario: AC4 A date range in the wrong order
    When the case owner filters from 2026-12-06 to 2026-12-01
    Then the system refuses the call with status 422 and MSG-GEN-003 for "to" and "from"

  Scenario: AC5 A case outside the caller's scope
    Given user "u-owner-05" holds RW-CASEOWN and does not own case "RW-2026-000401"
    When the user reads its ledger
    Then the system refuses the call with status 404 and MSG-P4-003

  Scenario: AC6 Summary masked when no masking rule allows it
    Given no masking rule from Compliance is loaded for interaction.summary
    When user "u-owner-04" reads the ledger
    Then the system returns the summary of each entry as "MASKED"
    Then the channel, result, promise amount and promise date are returned in full

  Scenario: AC7 Page size at and above the limit
    When the case owner reads once with size 200 and once with size 201
    Then the read with size 200 returns the 9 entries with size 200
    Then the system refuses the read with size 201 with status 422 and MSG-GEN-002 for "size" between 1 and 200

  Scenario: AC8 A case with no entries
    Given case "RW-2026-000402" has no ledger entries
    When its owner reads the ledger
    Then the response holds 0 items and total 0
    Then the history panel shows the Empty state
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger reads back in one ordered sequence, by occurred time and then case sequence | REQ-ILG-006; interaction.occurred_at; interaction.case_seq |
| BR2 | The ledger can be filtered by channel, actor and date range through one interface | REQ-ILG-006 |
| BR3 | Entries carry channel, who or what was reached, and the outcome where the interaction had one | REQ-ILG-003; interaction.contact_result |
| BR4 | Personal data in the ledger is masked by role on the same rules as the case record | REQ-ILG-014; CTL-11; DL26 |
| BR5 | A case outside the caller's scope is refused | CTL-09 |
| BR6 | No consumer queries the interaction table directly | ADR-002; DT08 |

## 9. State transitions

None. This story does not change a case status. It reads the ledger and changes nothing.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the ledger of own cases (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the ledger of team cases (Case record R, scope Team) |
| RW-CONDUCT, RW-AUDIT and other roles with Case record R | Read the ledger of cases in their scope |
| RW-REFADM, reference data administrator | May not read (no Case record right) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules that decide who sees the summary (DL26) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 | interaction | id | Read |
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-003 | interaction | party_id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-007 | interaction | action_code | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-009 | interaction | promise_amount | Read |
| DF-INT-010 | interaction | promise_date | Read |
| DF-INT-011 | interaction | summary | Read |
| DF-INT-012 | interaction | conduct_check | Read |
| DF-INT-013 | interaction | source_system | Read |
| DF-CAS-001 | recovery_case | id | Read |
| DF-INT-014 | interaction | event_code | Read |
| DF-INT-015 | interaction | actor_type | Read |
| DF-INT-016 | interaction | actor_ref | Read |
| DF-INT-017 | interaction | source_ref | Read |
| DF-INT-019 | interaction | case_seq | Read |
| DF-INT-020 | interaction | decision_log_id | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoint (P3, API-P3-014, extended; see additions)**

| Item | Value |
|---|---|
| Method and path | GET /cases/{caseId}/interactions |
| Request | Path: caseId; query: channel, from, to, page, size as in api.yaml, plus actor (new) |
| Response | InteractionPage: items of Interaction, page, size, total. Interaction gains eventCode, caseSeq, actorType, actorRef, sourceRef and decisionLogEntryId (new); summary is masked by role |
| Errors | 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 case missing or out of scope (MSG-P4-003); 422 filter invalid (MSG-GEN-001, MSG-GEN-002, MSG-GEN-003); 503 store down (MSG-GEN-006) |
| Authorization | Case record, R, scope applied |
| Idempotency | Not applicable |

**Published interface (P1)**

```java
package recovery.dataengine.ledger.api;

public interface InteractionLedgerReader {
    LedgerPage read(UUID caseId, LedgerFilter filter, int page, int size, UserContext caller)
            throws CaseNotInScopeException;
}

public record LedgerFilter(String channel, String actorRef, LocalDate from, LocalDate to) {}
public record LedgerPage(List<LedgerEntryView> items, int page, int size, long total) {}
```

## 13. Solution plan

- Package: folder `recovery/dataengine/ledger/read`, Java package `recovery.dataengine.ledger.read`.

| Component | Type | Responsibility |
|---|---|---|
| InteractionLedgerReader | Published interface | The one read path for the ledger |
| LedgerReadService | Service | Scope check, filter validation, ordered query, masking, PII log |
| InteractionRepository | Repository | Read query by case and filter, ordered by occurred_at, case_seq |
| InteractionsHandler (P3, API-P3-014) | Controller | Existing P3 endpoint; adds the actor parameter and delegates to the reader |
| CaseHistoryPanel | React component | History panel on SCR-03 with channel, actor and date filters, paging and the Empty state |

- Database: no new table. Query on interaction by case_id with optional channel, actor_ref and occurred_at range, ordered by occurred_at, case_seq; uses ix_interaction_case_time (Recovery Workbench Physical Schema v4.sql). Add index (case_id, actor_ref) in a Flyway migration for the actor filter.
- Configuration and reference data: properties `rwb.dataengine.ledger.page-size-default=50` and `rwb.dataengine.ledger.page-size-max=200`; LOV-CHANNEL for the channel filter; masking rules from Compliance through RWB-E1-037 (DL26).
- Build steps:
  1. LedgerFilter validation: channel in LOV-CHANNEL, from not after to, size 1 to 200.
  2. Ordered, filtered, paged query in InteractionRepository and the actor index migration.
  3. Scope check through CaseScopeQuery before the query.
  4. Masking of summary through MaskingPolicy; PII access log write when a personal field is returned unmasked.
  5. P3 InteractionsHandler: actor parameter, new response fields, delegation to the reader.
  6. CaseHistoryPanel on SCR-03 with filters, paging, Loading and Empty states.
  7. Architecture test that no class outside `recovery.dataengine.ledger` queries interaction.
  8. Tests for AC1 to AC8 and the access test; a timed read of one case with 5,000 entries against the 2 second target (NFR-070).
- Feature flag: `rwb.dataengine.ledger-read`.
- Done when: the tests in section 16 pass and SCR-03 shows the ledger in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-003 | from is after to | {field} cannot be before {other}. |
| MSG-GEN-002 | size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-GEN-001 | Malformed channel or date | Enter {field}. |
| MSG-P4-003 | Case out of scope | This case is not in your scope. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-03 Case record (Epic 1, Read only): the history panel lists entries earliest first, each with time, event, actor, channel, outcome and source; the user filters by channel, actor and date range and pages through the list. States: Loading (skeleton rows), Empty (a sentence that no interaction is recorded on the case), Error (the message from section 14 above the panel). The full timeline screen SCR-04 comes in Epic 2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-068-01 | AC1, BR1, BR3 | System | Case RW-2026-000401 with 9 entries from EFS, the Workbench and the owner |
| TC-E1-068-02 | AC2, BR2 | System | Filters by channel CALL, actor u-owner-04, 2026-12-01 to 2026-12-06 |
| TC-E1-068-03 | AC3, BR6 | System | SCR-03 history panel; architecture test |
| TC-E1-068-04 | AC4 | System | from 2026-12-06, to 2026-12-01 |
| TC-E1-068-05 | AC5, BR5 | System | RW-CASEOWN u-owner-05, case not owned |
| TC-E1-068-06 | AC6, BR4 | System | No masking rule for interaction.summary |
| TC-E1-068-07 | AC7 | System | size 200 and size 201 |
| TC-E1-068-08 | AC8 | System | Case RW-2026-000402 with no entries |
| TC-E1-068-09 | Access | Access | RW-REFADM reads the ledger; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: page sizes are properties; channels and masking come from lists and rules.
- No personal data in logs, tests or prompts: summaries are never logged; test summaries are synthetic text.
- No read of another module's tables: scope comes from CaseScopeQuery and masking from MaskingPolicy; P3 reads the ledger only through InteractionLedgerReader.
- The read changes nothing in the ledger.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-006 | Ledger reads in one ordered sequence, filterable by channel, actor and date range | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | CTL-09 | TC-E1-068-01 to TC-E1-068-05, TC-E1-068-07, TC-E1-068-08 |
| REQ-ILG-003 | Entries carry channel, who was reached and the outcome | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | None | TC-E1-068-01 |
| REQ-ILG-014 | Personal data in the ledger masked by role as on the case record | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-03 | All recovery processes | CTL-11; DL26 | TC-E1-068-06 |

## 19. Out of scope

- The full case timeline screen SCR-04 and the ledger as a timeline on the case (FEAT-ILG-09, RWB-E2-034).
- Recording entries (RWB-E1-066, RWB-E1-067).
- Masking rule values (DL26, Compliance) and the masking mechanism (RWB-E1-037).

