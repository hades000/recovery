# RWB-P7-E2041-APP Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2041-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-041 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-AN |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2041-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-030, FR-P7-032, FR-P7-035) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-041 for rwb-decision — the rule change checklist on the registry version and the rule change report of the audit. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE), a risk and model risk officer (RW-RISK), an internal auditor (RW-AUDIT) and the rwb-decision service that owns the rule registry**, I want **the rule change checklist — request, impact, test result, approver, load, verify and rollback plan — held on every rule package version in `rwb_decision`, required before that version can be approved, and reported by package version for a period with the rows the version added, changed and removed and the decisions that version made**, so that **a rule change is as controlled as a code change and audit reads one report of every package change instead of asking the team**.

Inside `rwb-decision` this is the governance and audit half of the legacy story RWB-E2-041:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` on which every governance action writes a decision record (DP-03).
- The checklist: the seven items of the legacy section 1 as one JSON object in DF-REF-295 `change_checklist` on the `rule_package_version` row, with `testResult`, `loadedAt`, `author`, `approver` and `checksum` filled by the service from the row, so no item is typed twice (legacy BR9).
- The approval gate: `approve(...)` refuses a version whose request reference, impact summary, verify record or rollback plan is missing, whose test result is not PASSED, or whose approver is its author (legacy BR1 and BR2).
- The change report: `GET /admin/rule-packages/change-report` for a period and a package, as JSON or CSV, one entry per package version — the checklist, the state, the dates, the rows added, changed and removed against the version it replaces, the rule IDs changed and the decisions that version made (legacy BR5 to BR8).
- The counts: read from `decision_log_entry` `rule_id` (DF-DEC-004) and `rule_version` (DF-DEC-005) by period; the report never recomputes a decision (legacy BR8).
- No new table and no new column: the checklist is the JSON column of the registry baseline, and this story adds three indexes only (legacy BR9).

Not this story, and stated again in section 6 and section 19:

- The package version load, the six checks, the 50-scenario gate, the dry run, the four-eyes mechanics, the 00:01 promotion and the one-call rollback are **RWB-P7-E2042-APP**. This story adds one part to the load and four checks to the approve; it rebuilds neither operation and re-implements neither the promotion nor the rollback.
- The case-side audit read, the impact count over open cases, the screens, the roles and the permission matrix are **RWB-P3-E2041-APP**, **RWB-P4-E2041-APP** and **RWB-P4-E1037-CON**. The ten legacy criteria AC1 to AC10 are owned by RWB-P3-E2041-APP; this story writes criteria of its own for the registry half (section 7).
- The cross-service journey — a load, an approval, a promotion, a report read and a reconciliation across rwb-case, rwb-access and rwb-decision — is **RWB-ITG-E2041-ITG**.

The four tables this story reads and writes — `rule_package`, `rule_package_version`, `rule_row` and `decision_log_entry` — are P7's under the R-PREC default ruling (rule package registry, P7 rwb-decision) and ASM-0069, and no other service reads them (DP-01). The database login is the per-service login of DP-02, written only as "the rwb-decision login (DP-02)"; its name is Not specified in the source documents (GAP-2413; ASM-4018).

### 2. Business rationale

Audit found the collection procedure was not followed because the rules lived in documents (CTL-08). Rules are data now: one wrong row in a package changes every case that reaches it, so each package version needs the same evidence as a code change — who asked, what it affects, the test result, who approved, when it took effect and how to undo it. The legacy story closed that gap in the monolith; the target keeps the governance central in rwb-decision (ADR-017) while evaluation stays local to the service that owns each decision (DP-04), so the checklist and the report have to travel with the registry and not with a screen.

The registry is the only place in the target where the answer to "which version decided this, who approved it and what did it say" exists. That makes the checklist a registry property rather than a form: a version is approved by a second person only when the seven items are present and the scenarios passed, and every later reader — audit, risk, the case-side read of RWB-P3-E2041-APP — takes the evidence from the same rows.

This story is the rwb-decision half of the RWB-E2-041 split. It owns the checklist column and its intake, the four approval checks, the change effect, the change report with its JSON and CSV answers, and the decision counts per package version; the case-side audit read, the impact count and the screens are RWB-P3-E2041-APP's and RWB-P4-E2041-APP's, and the load, the approve, the promotion and the rollback it extends are RWB-P7-E2042-APP's. It meets REQ-CWC-013 and REQ-DRI-011 and gives RWB-P3-E2041-APP, the Epic 8 rules and parameters screen and the ITG story of this key one report to read.

The measure is registry-shaped: every package version in force carries a complete checklist with all seven items; one refusal per missing item, per FAILED test result and per author-as-approver; one entry per package version in a period, with the rows added, changed and removed against the predecessor and the rule IDs changed; a decision count per package version that equals the decision-log read for the same period; a CSV with no party identifier and no case data; and a migrated `rwb_decision` with no new table and no new column.

The realignment changes the mechanism, not the business rule:

1. The single recovery schema becomes `rwb_decision`, with the registry tables, the checklist column and `decision_log_entry` inside it and no other service reading them (DP-01); the DF-REF and DF-DEC field IDs are unchanged.
2. The monolith `RulePackageEffectiveDateJob`, the P4 package `recovery.accessadmin.rulepackages` and the P3 module become the rwb-decision registry and the report on `/api/recovery/decision/v1` (DP-13); the legacy module pointer is GAP-2415.
3. The checklist stays one JSON column; the four approval checks become `ChangeChecklistValidator` in front of the registry's own approve, so a refusal is a service answer and not a screen validation.
4. The effect computation reads the version's `rule_row` rows through the embedded Drools kit's compiled catalogue by rule name and row order (DP-04), never the live rule rows.
5. The decision counts are an in-service read of `decision_log_entry` (P7's table) and the report reconciles with the decision-log read, so no tally is mailed between services.
6. The legacy flag `rwb.p3.rule-change-report` is read as a parameter of rwb-decision (DP-06) and is not a code constant; the feature-flag ruling of R3 is a platform library concern, recorded in ASM-4021.

The outcome is unchanged and easier to audit: a rule change carries its evidence, it is approved by a second person only when the tests passed, it is reversible, and every answer names the version that made it (R-UNI-38).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2041-CON | The published contract of the legacy key as rwb-case consumes it: the change-report request and answer, the load with its checklist part, the approve with its refusals, the version list, the decision-log read and the fakes. This story provides the registry side of that contract and restates nothing of the case side |
| RWB-P7-E2042-APP | The registry mechanics this story extends and never rebuilds: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the load with the six checks and the scenario gate, the dry run, the approve, the JOB-20 promotion at 00:01 and the one-call rollback (legacy RWB-E1-073) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one hash-chained record per governance action, written in the same transaction as the action |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): the compiled catalogue of a version by rule name and row order that the change effect compares, and the checksum the report shows |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the rwb-case parameters contract (DP-06): `rules.testcases.min`, the report paging defaults and maxima, the checklist limits and the legacy flag |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the rwb-case reference-data contract (DP-07): LOV-DECISION, the package-version state list and the checklist item list, with the version in force |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The authorise contract and the guard library (DP-08): the Rules and parameters right C, A, R and U behind the three operations |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic, event and queue names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15): the index migration of section 13 |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the Epic 8 screen and the CSV download reach the report through it; this story serves no screen |
| RWB-P7-E1073-CON, RWB-P7-E2005-CON | This service's rule-package contract, which publishes the report and the version operations to other services, and its decision-log read API-P7-006 and API-P7-007, which is the reconciliation source of AC8 |

The DP-added H and C dependencies above — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON — are not repeated in the metadata rows, which name Depends on (build) None and Contract dependencies RWB-P3-E2041-CON (GAP-2414; ASM-4019). They are platform contracts of wave 0 and published contracts of other services, so none blocks this story and Ready to start stays Day 1 (R5.7 rule 2).

Business preconditions carried from RWB-E2-041:

- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows, loaded by "U-41" and approved by "U-51" (legacy section 3).
- The checklist JSON schema is agreed on 16 November 2026: `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt` and `rollbackPlan`; the service fills `testResult`, `loadedAt`, `author`, `approver` and `checksum` (legacy section 3).
- The business date of the run is 2026-12-01. "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT, with Rules and parameters C, A and R (legacy sections 7 and 10).
- The legacy flag `rwb.p3.rule-change-report` is on in DEV and SIT; in the target it is read as a parameter through DP-06 (ASM-4021).
- Synthetic data only: package codes, version labels, rule IDs, queue codes, dates and a checksum prefix. No account, customer, party or case fact appears in a checklist, a report entry or a CSV.

### 4. Flow

1. Center of excellence analyst: raises the change request outside the Workbench and holds its reference, for example "CR-2026-0042" (legacy step 1).
2. Center of excellence analyst: calls `POST /api/recovery/decision/v1/admin/rule-packages/ALLOCATION/versions` as multipart with `file`, `validFrom` and the new `checklist` part carrying `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt` and `rollbackPlan`.
3. `ChangeChecklistIntake`: validates the part — the five members present or explicitly empty, the 8 KB size and the field maxima read through DP-06 — and refuses a `verifiedAt` before `loadedAt` with 422 and MSG-GEN-003 naming both fields (AC4, legacy X5). A caller item that is missing does not refuse the load (legacy section 12).
4. `RuleVersionService` of RWB-P7-E2042-APP: runs its own pipeline — parse, the six checks, the scenario gate, the dry run — and stores the row with the checklist in DF-REF-295 beside the author, `loaded_at`, the checksum, the test result and the dry-run counts. This story supplies the part and the storage of it and touches nothing else in that pipeline.
5. Risk officer: calls `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve`. `ChangeChecklistValidator` runs in front of the registry's checks: it looks for the four caller items, then the test result, then the author identity.
6. A failure is a refused approval: 409 with MSG-P3-022 naming the first missing item, 409 with MSG-P3-022 naming "test result" when it is FAILED, or 403 with MSG-P7-002 when the caller prepared the version. The version stays LOADED with an empty approver and no record is written (AC2, AC3, AC5).
7. A pass leaves the answer to the registry: the version becomes APPROVED with the approver and the approval time, and `DecisionRecordWriter` writes the record on `rwb.decision-record.v1` in the same transaction (DP-03).
8. JOB-20 of RWB-P7-E2042-APP: at 00:01 on the valid-from date an APPROVED version becomes IN_FORCE and the version it replaces becomes SUPERSEDED. A version whose valid-from date arrives without an approval is not promoted and stays LOADED (AC8, legacy AC2).
9. Internal audit or the center of excellence analyst: reads `GET /api/recovery/decision/v1/admin/rule-packages/change-report` with `from`, `to`, an optional `packageCode`, `format`, `page` and `size`. `RuleChangeReportService` selects every version whose load, approval, valid-from, verification or rollback falls in the period (legacy BR5), computes the change effect against the version it replaces (legacy BR6) and reads the decision counts by version and by rule ID (legacy BR8).
10. The answer is a `ChangeReportPage` or the same columns as `text/csv`; the CSV carries no party identifier and no case data, and the read writes no row and changes no version (AC6, AC7, AC9).
11. The report is the reconciliation source: for the same period and package version its counts equal `GET /api/recovery/decision/v1/decision-log`, and RWB-P3-E2041-APP reconciles its case-side tally from this report rather than recomputing it (legacy AC10).

Nothing in this flow evaluates a package for a case, sets a case state, reads an ACE view, matches a payment or writes a row outside `rwb_decision`: the checklist and the report are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An approval whose request, impact, verify record or rollback plan is missing | 409; the item is named; the version stays LOADED with an empty approver and no approval record | MSG-P3-022 | AC2 |
| X2 | An approval of a version whose test result is not PASSED | 409 naming "test result"; the version stays LOADED | MSG-P3-022 | AC3 |
| X3 | The author of the version calls approve, whatever right the author holds | 403; the version stays LOADED; no record | MSG-P7-002 | AC5 |
| X4 | `verifiedAt` is before `loadedAt` | 422 before any row is written; the fields are named; no version row exists | MSG-GEN-003 | AC4 |
| X5 | The checklist part exceeds 8 KB, or a member is longer than its maximum, or the JSON does not parse | 422 naming the member and its maximum, read through DP-06; no version row exists | MSG-GEN-001 | AC4 |
| X6 | A version reaches its valid-from date with no approval | Not promoted; the version in force keeps serving; the report shows the version LOADED with an empty approver | None | AC8 |
| X7 | The report period ends before it starts | 422 naming `to` and `from`; nothing is read | MSG-GEN-003 | AC7 |
| X8 | The report period holds no change | 200 with an empty `items` and `total` 0 | None | AC7 |
| X9 | The caller holds no Rules and parameters R for the report, or no C or A for the load and the approve | 403 through the guard of RWB-P4-E1037-CON; nothing is read, loaded or approved | MSG-P4-002 | AC7 |
| X10 | The decision record of an approval cannot be written | Nothing is committed: no approval state, no approver, no time; 503 and the caller retries | MSG-P7-003 | AC2, AC5 |

A refused approval leaves the version exactly as it was, and the report is a read: no exception path of this story changes a version state, a rule row or an earlier decision. The load pipeline's own exceptions — a failed check, a short scenario set, a dry run that cannot complete — are RWB-P7-E2042-APP's and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2041-CON, the platform contracts of its DP table and the registry of its own service; the load, the approve, the promotion and the rollback are consumed as the published operations and the fake of RWB-P7-E2042-APP, and the rights answer is declared but not built |
| Negotiable | The checklist limits, the paging defaults, the item list, the message texts, the state vocabulary and the CSV columns are data and parameters; the story fixes only the seven items, the four checks, the effect rule and the read |
| Valuable | Audit reads one report of every package change and of the decisions each version made, and no version is approved without its evidence |
| Estimable | One intake, one validator, one effect calculator, one count reader, one report service, one controller, one index migration and one client set |
| Small | Fits two weeks with its tests. It builds no load pipeline, no promotion, no rollback, no screen and no case-side read |
| Testable | Each criterion is a load, an approve, a report read, a CSV answer or a schema check, with a fixed Given, When and Then and a recorded result; the cross-service journey is not claimed here, it is the ITG story's |

### 7. Acceptance criteria

The ten legacy criteria AC1 to AC10 of RWB-E2-041 are owned by RWB-P3-E2041-APP and are not restated. The nine below are new under D-RCV-60 and test only the registry half: the checklist on the version, the approval gate, the change report and the counts. Every value inside them is a legacy value of RWB-E2-041 sections 3, 4, 7, 8 and 12.

```gherkin
Feature: Rule change governance and audit report in rwb-decision

  Background:
    Given the business date is 2026-12-01
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given user "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT
    Given the rwb-case parameters contract mock returns page size default 50, page size max 200, checklist max 8 KB, changeRequestRef 30, impactSummary 1000, verifyNote 1000 and rollbackPlan 1000
    Given the rwb-case reference-data contract mock returns LOV-DECISION and the package-version state list with their versions in force
    Given the rwb-access contract mock returns Rules and parameters R and C to RW-COE, A and R to RW-RISK, R to RW-AUDIT and no right to RW-CASEOWN

  Scenario: AC1 The seven checklist items are stored on the version and read back from the report (new, D-RCV-60)
    Given "U-41" loads ALLOCATION version "ALLOC-2026.12" on 2026-12-08 with request "CR-2026-0042", impact summary "412 open Mortgage cases in the BKK queue", verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases", verify date 2026-12-08 and rollback plan "Roll back to ALLOC-2026.11"
    Given the load checks and the 50 scenarios pass with checksum "9f2c...e1b4"
    When "U-51" approves version "ALLOC-2026.12" on 2026-12-09 with valid from 2026-12-10
    Then the version row holds one change_checklist JSON object in DF-REF-295 with changeRequestRef "CR-2026-0042", impactSummary "412 open Mortgage cases in the BKK queue", verifyNote "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases", verifiedAt 2026-12-08 and rollbackPlan "Roll back to ALLOC-2026.11"
    Then the same object carries testResult "PASSED", loadedAt 2026-12-08, author "U-41", approver "U-51" and checksum "9f2c...e1b4", written by the service and not supplied by the caller
    Then the checklist holds all seven items: request, impact, test result, approver, load, verify and rollback plan
    When "U-AUD-01" reads GET /api/recovery/decision/v1/admin/rule-packages/change-report for 2026-12-01 to 2026-12-31 with packageCode ALLOCATION
    Then one entry shows packageCode "ALLOCATION", versionLabel "ALLOC-2026.12", changeRequestRef "CR-2026-0042", impactSummary, verifyNote, verifiedAt 2026-12-08, testResult "PASSED", author "U-41", loadedAt 2026-12-08, approver "U-51", approvedAt 2026-12-09, checksum "9f2c...e1b4", rollbackPlan and validFrom 2026-12-10
    Then the verify date is on or after the load time and before the approval time

  Scenario: AC2 An approval is refused when a checklist item is missing (new, D-RCV-60)
    Given RESTRUCTURE version "RES-2026.12" is loaded with no rollback plan
    When "U-51" calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve
    Then the call is refused with 409 and MSG-P3-022 naming "rollback plan"
    Then version "RES-2026.12" stays LOADED with an empty approver and an empty approval time
    Then no decision record of an approval is written
    Given the decision-record library cannot write
    When "U-51" approves a version whose checklist is complete
    Then the answer is 503 with MSG-P7-003 and the version stays LOADED with no approver

  Scenario: AC3 An approval is refused when the test result is not PASSED (new, D-RCV-60)
    Given PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    When "U-51" calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve
    Then the call is refused with 409 and MSG-P3-022 naming "test result"
    Then version "PMT-2026.12" stays LOADED and the version in force is unchanged

  Scenario: AC4 The checklist is refused at load when the verify date precedes the load or a limit is broken (new, D-RCV-60)
    Given ALLOCATION version "ALLOC-2026.14" offered with verify date 2026-12-07 and load time 2026-12-08
    When "U-41" calls POST /api/recovery/decision/v1/admin/rule-packages/ALLOCATION/versions
    Then the load is refused with 422 and MSG-GEN-003 naming "verifiedAt" and "loadedAt"
    Then no version row, no rule row and no checklist is written
    Given a checklist part of 9 KB, and a checklist whose changeRequestRef is 31 characters
    When "U-41" loads either of them
    Then each load is refused with 422 and MSG-GEN-001 naming the member and its maximum
    Then no version row is created for either attempt

  Scenario: AC5 The author of a version cannot approve it (new, D-RCV-60)
    Given version "ALLOC-2026.12" is LOADED and authored by "U-41"
    Given "U-41" also holds a role that carries Rules and parameters A
    When "U-41" calls POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve
    Then the call is refused with 403 and MSG-P7-002
    Then the version stays LOADED with an empty approver
    When "U-51" calls the same operation for the same version
    Then the version is APPROVED with approver "U-51" and the approval time
    Then one rwb.decision-record.DecisionRecorded.v1 names the package "ALLOCATION", the version "ALLOC-2026.12", the approver and the decision code read from LOV-DECISION
    Then no approval row and no ApprovalRequested event is raised, because a package-version approval is not a delegation-of-authority decision

  Scenario: AC6 The report shows the change effect of a version and the same columns as CSV (new, D-RCV-60)
    Given "ALLOC-2026.12" replaced "ALLOC-2026.11" with 24 rows, changing row "ALLOC-031" from queue "MTG-BKK-CO" to "MTG-CEN-CO" and changing no other row
    When "U-AUD-01" reads GET /api/recovery/decision/v1/admin/rule-packages/change-report for 2026-12-01 to 2026-12-31 with packageCode ALLOCATION and format "json"
    Then the entry for "ALLOC-2026.12" names 1 row changed, 0 added and 0 removed against "ALLOC-2026.11"
    Then the entry names rule ID "ALLOC-031" in rulesChanged and no other rule ID
    Then the entry names the version it is compared with and its checksum
    When "U-AUD-01" reads the same period with format "csv"
    Then the answer is text/csv with one header row and one row per package version, in the column order of the JSON entry
    Then it carries no party identifier and no case data
    Then both reads write no row and change no version state

  Scenario: AC7 The period, the empty period and the access are handled by the report (new, D-RCV-60)
    When "U-AUD-01" reads the report from 2026-12-31 to 2026-12-01
    Then the call is refused with 422 and MSG-GEN-003 naming "to" and "from"
    When "U-AUD-01" reads the report for 2026-11-01 to 2026-11-15
    Then the answer is 200 with an empty items list and total 0
    When "RW-CASEOWN" reads the report
    Then the call is refused with 403 and MSG-P4-002
    When "RW-CASEOWN" calls the load or the approve
    Then each call is refused with 403 and MSG-P4-002 and nothing is written

  Scenario: AC8 The decisions per package version are read from the decision log and never recomputed (new, D-RCV-60)
    Given "ALLOC-2026.11" was in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given decision_log_entry holds 96 entries with rule_version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    Given those entries carry rule_id "ALLOC-031" on 700 of them and "ALLOC-032" on 600
    When "U-AUD-01" reads the report for 2026-12-01 to 2026-12-31 with packageCode ALLOCATION
    Then version "ALLOC-2026.11" shows 96 decisions and version "ALLOC-2026.12" shows 1,204
    Then decisionsByRule shows "ALLOC-031" 700 and "ALLOC-032" 600 across both versions
    Then the total equals GET /api/recovery/decision/v1/decision-log for the same period and package version
    Then no decision is recomputed: the counts carry the rule_id and rule_version of the entries
    Given ALLOCATION version "ALLOC-2026.13" is loaded by "U-41" with a complete checklist, valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the version in force is still "ALLOC-2026.12"
    Then the report shows version "ALLOC-2026.13" with status "LOADED" and an empty approver

  Scenario: AC9 The checklist adds no table and no column (new, D-RCV-60)
    Given a database migrated from empty with the rwb-decision Flyway sequence of the release
    When the change-report schema check runs against rwb_decision
    Then change_checklist is one JSON column, DF-REF-295, on rule_package_version
    Then no rule_change table, no change_request table and no checklist child table exists in rwb_decision
    Then ix_rpv_loaded_at, ix_rpv_approved_at and ix_rpv_valid_from exist and are indexes, not fields
    Then the check reads only rwb_decision and no other schema
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version can be approved only when it carries a change request reference, an impact summary, a verify record, a rollback plan and a test result of PASSED | CTL-08; legacy BR1; rule package change process steps 1 to 4 |
| BR2 | The approver is not the author, and the check is made in the service, not only on a screen | legacy BR2; roles.txt separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013; legacy BR3 |
| BR4 | The verify item is dated on or after the load and before the approval | legacy BR4; rule package change process step 6 |
| BR5 | The report lists every package version whose load, approval, valid-from, verification or rollback falls in the period | REQ-DRI-011; legacy BR5 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, by Drools rule name and row order, and the rule IDs changed | D-RCV-36 T4, T5; ADR-012; legacy BR6 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38; legacy BR7 |
| BR8 | The decisions per package version are counted from `decision_log_entry` `rule_id` and `rule_version`; the report never recomputes a decision | REQ-DRI-011; D-RCV-36 T5; legacy BR8 |
| BR9 | The checklist is one JSON object in DF-REF-295; this story adds no table and no column | D-RCV-36 T4; RWB-E1-072; legacy BR9 |
| BR10 | The registry, the checklist and the report are rwb-decision's, in `rwb_decision`; no other service reads those tables and the report reads no other schema | Arch v5 slides 14, 27 and 41; R-PREC default ruling; ASM-0069; DP-01 |
| BR11 | Every governance action — an approval, a rollback — writes one hash-chained decision record in the same transaction, and an action whose record cannot be written is not taken | R-UNI-39; FSD P7 v3 VR-P7-001-2 and principle 5; DP-03 |
| BR12 | No business value is code: the checklist limits, the paging defaults and maxima, the checklist item list, the state vocabulary and the legacy flag are rows and parameters | Template and Rules §R7.2 s17; DP-06; DP-07; legacy section 17 |
| BR13 | The report is read-only: it writes no row, changes no version, and carries no party identifier and no case data | legacy AC9 and section 17; BR5 |

### 9. State transitions

This story changes no case status and no plan state. It gates one transition of the package version lifecycle and reads all the others without changing them.

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | Approve | The four caller items are present, the test result is PASSED and the caller is not the author | APPROVED |
| LOADED | Approve | A caller item is missing, or the test result is not PASSED | LOADED (refused, MSG-P3-022) |
| LOADED | Approve | The caller is the author, whatever right the caller holds | LOADED (refused, MSG-P7-002) |
| LOADED | The valid-from date arrives, JOB-20 runs | No approval | LOADED (not promoted; the report shows it with an empty approver) |
| APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK | A report read | Always | Unchanged; the report and the CSV are reads |
| Any | A governance action whose decision record cannot be written | — | Unchanged; MSG-P7-003 |

The version states are the vocabulary of LOV-DECISION's sibling list read through DP-07 and are never literals of the report. The promotion, the supersede and the rollback transitions are RWB-P7-E2042-APP's and are not observed here beyond the state a report entry shows.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a version with its checklist under Rules and parameters C; reads the report and the CSV under R; calls the rollback of a version under U through the registry |
| RW-RISK, risk and model risk officer | Approves a loaded version under Rules and parameters A; may not be the author of that version; reads the report under R |
| RW-AUDIT, internal audit | Reads and exports the report under Rules and parameters R; changes nothing |
| RW-PLATADM, platform administrator | Reads the report and the incident raised by a refused record write under R |
| RW-CASEOWN, RW-TEAMMGR and any role without a Rules and parameters right | Refused with MSG-P4-002 on the load, the approve and the report |
| The rwb-decision service identity | Validates the checklist, gates the approval, computes the change effect, counts the decisions and serves the report and the CSV |
| SY-RULES, Drools evaluator | Supplies the compiled catalogue the change effect compares; it approves nothing and writes no checklist |
| No delegation of authority level applies | A package version is not a credit decision; the approval is four eyes and raises no `approval` row and no `ApprovalRequested` event |

The rights are answered by the guard of RWB-P4-E1037-CON and the matrix of RWB-P4-E2041-APP; this story declares the right each operation needs and holds no role row. Separation of duty is a service rule and not a convention: the analyst who loaded a version never approves it (BR2). No person is named anywhere: the actors are roles and service identities.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package (P7) | id | Read |
| DF-REF-275 | rule_package (P7) | package_code | Read |
| DF-REF-276 | rule_package (P7) | title | Read |
| DF-REF-277 | rule_package (P7) | owner_role | Read |
| DF-REF-279 | rule_package_version (P7) | id | Read |
| DF-REF-280 | rule_package_version (P7) | package_id | Read |
| DF-REF-281 | rule_package_version (P7) | version_label | Read |
| DF-REF-282 | rule_package_version (P7) | status | Read |
| DF-REF-283 | rule_package_version (P7) | source_blob_ref | Read |
| DF-REF-285 | rule_package_version (P7) | checksum | Read and shown in the entry |
| DF-REF-286 | rule_package_version (P7) | valid_from | Read and used by the period query |
| DF-REF-287 | rule_package_version (P7) | valid_to | Read |
| DF-REF-288 | rule_package_version (P7) | author | Read |
| DF-REF-289 | rule_package_version (P7) | approver | Read and written at approval |
| DF-REF-290 | rule_package_version (P7) | loaded_at | Read and used by the period query |
| DF-REF-291 | rule_package_version (P7) | approved_at | Read and written at approval |
| DF-REF-292 | rule_package_version (P7) | test_result | Read; the gate of BR1 reads it |
| DF-REF-293 | rule_package_version (P7) | dry_run_counts | Read, not published in the entry |
| DF-REF-294 | rule_package_version (P7) | rollback_of | Read and shown as `rolledBackTo` |
| DF-REF-295 | rule_package_version (P7) | change_checklist | Write at load and read by the report; the seven items of section 1 and BR9 |
| DF-REF-002 | rule_row (P7) | rule_id | Read; the rule IDs changed and `decisionsByRule` |
| DF-REF-296 | rule_row (P7) | package_version_id | Read; the join to the version compared |
| DF-REF-297 | rule_row (P7) | drools_rule_name | Read; the change effect is keyed on it with row order |
| DF-DEC-004 | decision_log_entry (P7) | rule_id | Read through the in-service query; `decisionsByRule` |
| DF-DEC-005 | decision_log_entry (P7) | rule_version | Read through the in-service query; the per-version count |
| DF-DEC-016 | decision_log_entry (P7) | decided_at | Read; the period bound of the count |
| (outbox) | outbox_event in `rwb_decision` | the `DecisionRecorded` row of an approval | Write in the same transaction as the approval (DP-03) |
| DF-ACE-* | ACE views | — | Not read: this story reads no ACE view (DP-05) |

The field IDs are those of the Logical Data Model and Data Dictionary v8, as the legacy story cites them. No new field is added: the checklist is the JSON column DF-REF-295 of the registry baseline, and the three indexes of section 13 are constraints and not fields (BR9). The checklist item names are the five caller members of the agreed schema of 16 November 2026 and the five service-filled members read off the row; the item list is read through DP-07 as reference data (ASM-4022), and the exact list code is Not specified in the source documents (GAP-2413; ASM-4018).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1` (DP-13). Two operations are the registry operations of RWB-P7-E2042-APP with one part and four checks added, and one is new. The paths are the rule-package family of the Ownership Map; the report path, its query and its answer are the legacy section 12 shapes.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/rule-packages/{packageCode}/versions` | The load of RWB-P7-E2042-APP with one added multipart part `checklist` (JSON object, max 8 KB) carrying `changeRequestRef` (max 30), `impactSummary` (max 1000), `verifyNote` (max 1000), `verifiedAt` (date) and `rollbackPlan` (max 1000); 201 with the version. A missing caller item does not refuse the load; it refuses the approval (BR1) | Rules and parameters C | Package code and version label; a repeated label is 409 with MSG-GEN-004 |
| POST | `/admin/rule-package-versions/{versionId}/approve` | The approve of RWB-P7-E2042-APP with the checklist gate in front of it; 409 MSG-P3-022 naming the first missing item, 409 MSG-P3-022 naming "test result", 403 MSG-P7-002 when the caller is the author; 200 with the version at APPROVED | Rules and parameters A | Idempotency-Key header; a second approval of an APPROVED version changes nothing |
| GET | `/admin/rule-packages/change-report` | The change report for a period and an optional package, as JSON or CSV: one entry per package version with the checklist, the state, the dates, the change effect and the decisions | Rules and parameters R | Not applicable, read only |

The report takes the query `from` (date, required), `to` (date, required), `packageCode` (optional), `format` (`json` default or `csv`), `page` and `size` (default 50, max 200). It answers 200 with `ChangeReportPage`: `items[]` of `RulePackageChangeEntry` (`packageCode`, `packageTitle`, `versionLabel`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt`, `testResult`, `author`, `loadedAt`, `approver`, `approvedAt`, `checksum`, `rollbackPlan`, `rulesChanged[]`, `decisions`, `decisionsByRule[]`, `rolledBackTo`), `page`, `size` and `total`; or `text/csv` with the same columns. The element shape of `rulesChanged[]`, the placement of the rows added, changed and removed of BR6 inside it, and the CSV column order are Not specified in the source documents (GAP-2413; ASM-4018); this story reads them as `ruleId`, `added`, `changed` and `removed` per element, pending the contract review. Errors: 401 no session (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 404 an unknown package code; 422 `to` before `from` (MSG-GEN-003) and a checklist limit broken (MSG-GEN-001); 503 the store or the record writer is down. Every error is an RFC 9457 problem response with `messageId` set.

The version list `GET /admin/rule-packages/{packageCode}/versions` and the decision-log reads `GET /decision-log` and `GET /decision-log/{entryId}` that RWB-P3-E2041-APP consumes are the operations of RWB-P7-E2042-APP and RWB-P7-E2005-CON; this story supplies the checklist and the counts they read and publishes no duplicate path.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, on RWB-P3-E1042-CON | `rules.testcases.min`, the report paging defaults and maxima and the checklist limits (DP-06); faked |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION, the package-version state list and the checklist item list, with the version in force (DP-07); faked |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access, on RWB-P4-E1037-CON | The Rules and parameters right check behind the three operations of 12.1 (DP-08); faked |

The case-side audit read `GET /admin/rule-change-audit` of RWB-P3-E2041-APP is consumed by nobody here: this story is its provider side. No ACE view and no other service's schema is read (DP-05).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by this service | entryId | The hash-chained record of an approval or a rollback: the decision code read from LOV-DECISION, rule ID (the package code), rule version (the version label), inputs reference, actor, final call, decided at |

An approval and a rollback write the record row and its outbox row in the same transaction as the state change, and the platform relay publishes them with the CloudEvents 1.0 envelope (DP-03). This story publishes no event on `rwb.decision.events.v1`: the change of a version in force is announced by `rwb.decision.RulePackageInForce.v1`, which the JOB-20 promotion of RWB-P7-E2042-APP publishes. No event carries a name, an e-mail address, a mobile number, an account number or a case fact.

#### 12.4 Events consumed

None. The checklist arrives on the load, the approval on its operation and the counts from this service's own `decision_log_entry`; no Kafka event is consumed and no inbox row is written by this story.

#### 12.5 Workflows and activities

None. The load, the approve and the report are synchronous REST operations; the promotion stays the JOB-20 Schedule of RWB-P7-E2042-APP. This story registers nothing on the `rwb-decision` task queue, starts no workflow and adds no activity.

#### 12.6 Schedules

None of this story's own. The 00:01 promotion that puts an approved version in force is JOB-20 of RWB-P7-E2042-APP on the `rwb-decision` queue, and the nightly hash-chain check is JOB-14 of the decision-log story. This story adds no Schedule: the report is read on demand, and the period query uses the indexes of section 13.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `rule_package_version` | P7 (`rwb_decision`) | The version, its state, its dates, its author and approver, its test result, its checksum and its `change_checklist` (DF-REF-295) |
| `rule_package` | P7 (`rwb_decision`) | The package code, its title and its owner role, read for the entry |
| `rule_row` | P7 (`rwb_decision`) | The rule rows of a version and of its predecessor, compared by `drools_rule_name` and row order |
| `decision_log_entry` | P7 (`rwb_decision`) | Read in service for the decisions per version and per rule ID; this story writes no decision entry itself |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox and idempotency objects of the service (DP-09); no inbox row is written |
| `approval` | P7 (`rwb_decision`) | Not read and not written: a package-version approval is four eyes and not a DoA approval (section 10) |

Not owned and not read: `recovery_case`, `task`, `timer` and `queue` (P3); `role`, `permission` and `delegation_limit` (P4); `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row` and `lov_value` (P3, read through DP-06 and DP-07); `document*` (P5); `agent_*` (P10). No foreign key crosses a schema and no other service reads these four tables (DP-01). This story adds no table and no column (BR9, AC9).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON, RWB-P3-E1043-CON | `rules.testcases.min` 50; page size default 50 and max 200; checklist max 8 KB; the three member maxima; LOV-DECISION with its decision code; the state list LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED; the checklist item list with its version; a changed parameter value to prove the report reads the parameter |
| rwb-access guard fake | RWB-P4-E1037-CON, RWB-P4-E2041-APP | RW-COE with C and R; RW-RISK with A and R; RW-AUDIT with R; RW-PLATADM with R; RW-CASEOWN refused with MSG-P4-002 |
| decision-record library fake | RWB-PLT-E1027-CON | The append and the hash chain, the `DecisionRecorded` outbox row and a forced failure for the 503 of X10 |
| Drools kit fake | RWB-PLT-E1072-CON | The compiled catalogue of a version by rule name and row order and the checksum of a version, for the change effect |
| Registry fake | RWB-P7-E2042-APP, RWB-P7-E1073-CON | The load with its six checks and its scenario gate, the version states with their transitions, a version with an arrived valid-from date and no approval, a rolled-back version with its predecessor, and a version whose test result is FAILED |

Each fake is replaced by the real contract or library as its story lands, without a change to the scenarios. The fakes carry synthetic package codes, version labels, rule IDs, queue codes, user references and a checksum prefix only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 3 | The load with its checklist, the gated approve and the change report provided; the parameters, the reference lists and the authorise answer consumed, one hop and 2 s each |
| Kafka | Published 1 event type, consumed 0 | `rwb.decision-record.v1` with `DecisionRecorded`; `rwb.decision.events.v1` carries no event of this story |
| Temporal | None | No workflow, no activity and no Schedule of this story's own |
| File | 1 output | The `text/csv` change report the auditor downloads; no file input |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `rules/audit`, Java package `th.co.scb.ace.workbench.recovery.decision.rules.audit`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How each row is applied. **DP-01**: the checklist, the version rows, the rule rows and `decision_log_entry` stay in `rwb_decision`; the report reads no other schema and no other service reads these tables. **DP-03**: an approval and a rollback write one local decision record and its outbox row in the same transaction; a record that cannot be written stops the action. **DP-04**: the change effect compares the compiled catalogue of a version with the one it replaces by rule name and row order; the kit is embedded here as a platform library and evaluates no case decision. **DP-05**: no ACE view is read; the report sees no customer, account or case fact. **DP-06**: the checklist limits, the paging defaults and maxima, `rules.testcases.min` and the legacy flag are parameters, never constants. **DP-07**: LOV-DECISION, the state vocabulary and the checklist item list are reference data with the version in force. **DP-08**: the three operations declare Rules and parameters C, A and R and are answered by the rwb-access guard. **DP-11**: the three consumed calls are one hop with a 2 s timeout and a breaker, and their fakes are in 12.8. **DP-13**: every path of 12.1 uses `/api/recovery/decision/v1`; the monolith base appears nowhere. **DP-14**: the record is published as `rwb.decision-record.DecisionRecorded.v1` through the naming library and the queue is `rwb-decision`. **DP-15**: the index migration of this story sits in the `rwb_decision` Flyway sequence. **DP-19**: no screen is served here; SCR-39 and the CSV download reach the report through the gateway-bff composite route in Epic 8.

The platform H dependencies and the C dependencies of the table — H RWB-PLT-E1027-CON, H RWB-PLT-E1072-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1037-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON, C RWB-P7-E1073-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and C RWB-P4-E1037-CON — are the DP-added dependencies that are **not** in the metadata rows, which name None and RWB-P3-E2041-CON. They are recorded in GAP-2414 and ASM-4019: platform contracts of wave 0 and published contracts with fakes, none of them a same-lane story behind this one, so **Ready to start stays Day 1** (R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeChecklistIntake | Service | Validates the `checklist` part on the load — the five members, the 8 KB size, the member maxima through DP-06, `verifiedAt` not before `loadedAt` — and hands it to the version write (BR4) |
| ChangeChecklistValidator | Service | BR1 and BR2: the four caller items, the test result PASSED and the caller not the author; returns the first failing item for MSG-P3-022 and refuses an author with MSG-P7-002 |
| ChangeEffectCalculator | Service | BR6: compares a version's `rule_row` rows with those of the version it replaces by `drools_rule_name` and row order, counts added, changed and removed and lists the rule IDs changed |
| DecisionCountReader | Service | BR8: counts `decision_log_entry` rows by `rule_version` in the period and by `rule_id` across the versions, and reads `decided_at` as the period bound |
| RuleChangeReportService | Service | BR5: the period query over the load, approval, valid-from, verification and rollback dates; assembles the entries; pages them; writes the CSV stream |
| RuleChangeReportController | Controller | `GET /admin/rule-packages/change-report`, the query validation, the `text/csv` answer and the RFC 9457 problem responses |
| RulePackageVersionRepository | Repository | The period query, the version-in-force read and the optimistic lock of the version row |
| DecisionRecordWriter | Service | The local record and its outbox row in the same transaction as the approval or the rollback (DP-03) |
| ParameterClient, ReferenceDataClient, AuthoriseClient | Clients | The three consumed operations of 12.2, one hop, 2 s, breaker and metric |

**Database and migrations**

- Reads and writes `rule_package`, `rule_package_version`, `rule_row`, `decision_log_entry` and the library objects, all in schema `rwb_decision`; reads no other schema.
- `V2_041_1__change_report_indexes.sql` adds `ix_rpv_loaded_at` on `rule_package_version (loaded_at)`, `ix_rpv_approved_at` on `(approved_at)` and `ix_rpv_valid_from` on `(valid_from)`, the three indexes of the legacy section 13 placed in this service's Flyway sequence (DP-15). It adds no column, no constraint and no seed row.
- DF-REF-295 exists from the registry baseline of RWB-E1-072 and is not migrated here. No `rule_package_version` row is edited by this story except the approver, the approval time and the state of an approval, written with `WHERE id = ? AND version = ?`.
- An update that matches zero rows is MSG-GEN-004 and the action is retried, never applied twice.

**Configuration and reference data**

- Page size default 50 and max 200, checklist max 8 KB, `changeRequestRef` 30, `impactSummary` 1000, `verifyNote` 1000 and `rollbackPlan` 1000 are parameters with the legacy values (ASM-4023); a value above a maximum is refused with MSG-GEN-001 and never clamped silently.
- LOV-DECISION, the package-version state list and the checklist item list are read through DP-07 with the version in force (ASM-4022); the decision code of a governance entry is Not specified in the source documents (GAP-2413; ASM-4018).
- The legacy flag `rwb.p3.rule-change-report` keeps its name as the legacy reference and is read as a parameter of rwb-decision through DP-06 (ASM-4021). Off: the report answers 404 and the approve runs the registry checks only.
- The login phrase is "the rwb-decision login (DP-02)"; its name is Not specified in the source documents (GAP-2413; ASM-4018).
- Synthetic data only, as section 3 says.

**Build steps**

1. `ChangeChecklistIntake` and its parameter reads; tests for the 9 KB part, the 31-character request and the verify date before the load (AC4, X4, X5).
2. The storage of the checklist in DF-REF-295 beside the version write, in the transaction of the registry load; test that a missing caller item still loads and still refuses the approval (AC1, AC2).
3. `ChangeChecklistValidator` wired in front of the approve; tests for the missing rollback plan, the FAILED result and the author (AC2, AC3, AC5).
4. `DecisionRecordWriter` on the approval path and its failure test (X10); test that no `approval` row and no `ApprovalRequested` event is produced (AC5).
5. `ChangeEffectCalculator` over the rule rows of two versions; tests for 1 changed, 0 added and 0 removed, for a pure addition and for a pure removal (AC6).
6. `DecisionCountReader` and the decision-log reconciliation; tests for 96 and 1,204, for 700 and 600 by rule ID, and for a period that is a subset of December 2026 (AC8).
7. `RuleChangeReportService` with the period query, the three indexes, the paging and the CSV stream; tests for the empty period, the wrong order and the CSV columns (AC6, AC7).
8. `RuleChangeReportController` with the guard and the problem mapping; the access test for RW-CASEOWN on all three operations (AC7); the schema check for AC9 on a Testcontainers database migrated from empty; and the privacy test that no checklist, entry or CSV carries a name, an account number or a case fact.

**Feature switch.** The legacy flag is read as a parameter (ASM-4021). Off: `GET /admin/rule-packages/change-report` answers 404, the checklist part is ignored at load and the approve runs the registry checks only, so the version in force keeps running. The exact answer of the load with the switch off is Not specified in the source documents (GAP-2413; ASM-4018).

**Done when.** The tests in section 16 pass; a SIT environment shows a version loaded with a complete checklist and the seven items read back from the report; one approval refused for a missing rollback plan, one for a FAILED result and one for an author; one entry per package version for the SIT period with its counts and rule IDs; a CSV with no party identifier and no case data; a decision count per package version that equals the decision-log read for the same period; and a migrated `rwb_decision` with no new table and no new column.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P3-022 | An approval with a missing checklist item or a test result that is not PASSED | The change cannot be approved: {item} is missing or failed. | This story, on the approve |
| MSG-GEN-003 | `verifiedAt` before `loadedAt`, or a report period whose end is before its start | {field} cannot be before {other}. | This story, on the load and on the report |
| MSG-GEN-001 | A checklist member is empty where it is required, or above its maximum, or the part is not valid JSON | Enter {field}. | This story, on the load |
| MSG-P7-002 | The author of a version approves it | You prepared this decision, so you cannot approve it. | This story, on the approve |
| MSG-P4-002 | A role without the right calls the load, the approve or the report | You cannot {action} here. Your role does not include it. | This story, through the guard of RWB-P4-E1037-CON |
| MSG-P7-003 | The decision record of an approval cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the approve |

MSG-P3-022 moves here from RWB-E1-048 with the legacy story (D-RCV-36 T8) and is unchanged. The `{item}` value is one of "request", "impact", "verify", "rollback plan" or "test result"; the `{field}` of MSG-GEN-003 is `verifiedAt`, `loadedAt`, `to` or `from`; the `{field}` of MSG-GEN-001 is the checklist member. No message carries a case fact or a person. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. Internal audit and the center of excellence read the report through the endpoint and open the CSV in Excel, and SCR-39 Rules and parameters (Epic 8) shows the same entries through the gateway-bff composite route of DP-19; this story feeds the states and the counts that screen and the case-side read of RWB-P3-E2041-APP consume.

| Where | State | What the caller sees |
|---|---|---|
| The report entry | LOADED | The version, its checklist, its author, the checksum and its test result, with an empty approver |
| The report entry | APPROVED | The version, its approver and approval time, its valid-from date and its checklist |
| The report entry | IN_FORCE | The version in force, its dates, its checksum, its effect and its decisions |
| The report entry | SUPERSEDED, ROLLED_BACK | The version, the date it stopped being in force and, for a rollback, the version it returns to |
| The report entry | Any state | The rows changed, added and removed against the predecessor and the rule IDs changed |
| The CSV | Export | One header row and one row per package version, no party identifier and no case data |
| The approve | Refused | The refusal with MSG-P3-022 naming the item, or MSG-P7-002 for the author; the version is unchanged |
| SCR-39 Rules and parameters (Epic 8) | List and detail | The same entries and states; the screen is built by the Epic 8 story, not here |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-01 | AC1, AC6, BR5, BR6 | Component | ALLOCATION "ALLOC-2026.11" to "ALLOC-2026.12", request "CR-2026-0042", one changed row "ALLOC-031" |
| TC-E2-041-02 | AC8, BR3, BR5 | Component | ALLOCATION "ALLOC-2026.13" never approved with valid from 2026-12-15 |
| TC-E2-041-03 | AC2, BR1 | Contract | RESTRUCTURE "RES-2026.12" with no rollback plan |
| TC-E2-041-04 | AC3, BR1 | Contract | PAYMENT_MATCH "PMT-2026.12" with a FAILED result, 2 of 58 scenarios |
| TC-E2-041-05 | AC1, BR1, BR4 | Component | Verify date 2026-12-08, load 2026-12-08, approval 2026-12-09 |
| TC-E2-041-06 | AC7 | Contract | Period 2026-11-01 to 2026-11-15 with no version |
| TC-E2-041-07 | AC4, BR4 | Component | Verify date 2026-12-07 and load 2026-12-08; a 9 KB part; a 31-character request |
| TC-E2-041-08 | AC7 | Contract | Period end 2026-12-01 before start 2026-12-31 |
| TC-E2-041-09 | AC6, BR13 | Contract | CSV export of the December versions, one header row and one row per version |
| TC-E2-041-10 | AC8, BR8 | Component | 96 and 1,204 decisions in December 2026; 700 and 600 by rule ID |
| TC-E2-041-11 | AC7 | Component | RW-CASEOWN with no Rules and parameters right on the load, the approve and the report; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the column shows; the registry half of each case is proved here, and the `-ITG` copies of all eleven cases belong to the ITG story of this legacy key. The `Covers` column names the criteria and rules of this story; the legacy AC1 to AC10 the cases derive from are owned by RWB-P3-E2041-APP, so no legacy criterion is claimed by a case of this story.

### 17. Guardrails

- No business value in code: the checklist limits, the paging defaults and maxima, the item list, the state vocabulary, `rules.testcases.min` and the legacy flag are rows and parameters; only the message identifiers and the state machine are fixed by design.
- No personal data in logs, events, tests, CSV files or prompts: the checklist, the entries and the CSV hold staff user references, package codes, version labels, rule IDs, queue codes, dates and a checksum prefix only.
- No read of another service's tables and no other service reads `rwb_decision` (DP-01): the parameters and the reference lists arrive on their operations, and no case fact enters the report.
- The decision record is written before the approval commits; no version is approved without its record (BR11).
- The report never recomputes a decision and never reads the live rule rows for an old version: the decisions come from `decision_log_entry` and the effect from the stored `rule_row` rows of the two versions (BR6, BR8).
- The approver is never the author, and the service checks it, not only the screen (BR2).
- One JSON column and three indexes: no `rule_change` table, no `change_request` column and no checklist child table is created (BR9, AC9).
- No secret in a checklist, a record or the run material: the rwb-decision login (DP-02) comes from the platform secret store and the test data is synthetic.
- The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and a rollback | Business Requirements Epic 1 v4, section 3.3 and section 4; Program v4, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E2-041-01 to TC-E2-041-05, TC-E2-041-07, TC-E2-041-11 |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | Business Requirements Epic 1 v4, section 4; Program v4, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E2-041-01, TC-E2-041-05, TC-E2-041-06, TC-E2-041-08 to TC-E2-041-11 |

- ADR-012 and D-RCV-36 T4, T5, T8: the change checklist, the versioned table discipline and the count of decisions per version; this story carries them into `rwb_decision`.
- ADR-017: embedded Drools per service and the rule registry in rwb-decision — the change effect compares the compiled catalogue of two versions and evaluates no case decision.
- ADR-022: a local decision record plus the central ledger — every approval and rollback writes a record on `rwb.decision-record.v1` (DP-03).
- D-RCV-60: the realignment that splits RWB-E2-041 into the P3, P4, P7 and ITG stories; the P7 registry and report slice is this story.
- RWB-P3-E2041-CON is the contract this story provides the registry side of; RWB-P7-E2042-APP owns the load, the approve, the promotion and the rollback it extends; RWB-P3-E2041-APP owns the ten legacy criteria and the case-side read.

The requirement text and the BRD section pointers are those of RWB-E2-041 and match Business Requirements Epic 1 v4, where section 3.3 holds the P3 module requirements and section 4 holds REQ-CWC-013 and REQ-DRI-011. No requirement ID and no requirement text changes. The module pointer of the legacy story — "Module P3 Case and workflow" with the report in the P4 package `recovery.accessadmin.rulepackages` — is the conflict of GAP-2415, read as ASM-4020.

### 19. Out of scope

- The package version load, its six checks, the 50-scenario gate, the dry run, the four-eyes mechanics, the JOB-20 promotion at 00:01 and the one-call rollback — RWB-P7-E2042-APP. This story adds one part and four checks to those operations and rebuilds none of them.
- The case-side audit read `GET /admin/rule-change-audit`, the impact count over open cases and the version each open case keeps — RWB-P3-E2041-APP; the ten legacy criteria AC1 to AC10 of RWB-E2-041 are its.
- The screens of the load, the approval and the rules and parameters administration, the roles, the permission matrix and the delegation of authority — RWB-P4-E2041-APP, RWB-P4-E1037-CON and the Epic 8 stories. This story declares the right and holds no role row.
- The QA sample against the rule package version applied (FEAT-ADM-08, Epic 8) and the SCR-39 screen itself.
- The decision log store, the writer's field-level validation and the hash-chain check — RWB-E1-008, RWB-E1-027, RWB-P7-E2005-CON and the decision-log stories of this service. This story reads the log and writes none of its own entries.
- The reference table checklist fields and their report (RWB-E1-043); this report covers rule package versions only.
- A rule-change feed to rwb-reporting: no source names an event of this story beyond the local decision record, so no reporting event is invented here (GAP-2413; ASM-4018).
- The cross-service proof of a load, an approval, a promotion, a report read and a reconciliation — the ITG story of this legacy key.
- The field-level completeness of the report element beyond the legacy field names, the CSV column order, the `rulesChanged[]` element shape, the decision code and the DP-02 login name (GAP-2413; ASM-4018), the dependency reading (GAP-2414; ASM-4019), the module and flag ownership (GAP-2415; ASM-4020 and ASM-4021) and the legacy date conflict (GAP-2416; ASM-4024), all confirmed with their owners before SIT.
