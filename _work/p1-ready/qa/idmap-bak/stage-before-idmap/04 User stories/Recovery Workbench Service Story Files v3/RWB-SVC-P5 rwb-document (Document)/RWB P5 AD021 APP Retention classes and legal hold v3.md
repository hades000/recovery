# RWB-P5-AD021-APP Retention classes and legal hold

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-AD021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P5-AD021-APP-16) |
| Contract version | Not specified in the source documents (DOR-RWB-P5-AD021-APP-23); REST base /api/recovery/document/v1 |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-P5-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P5-AD021-CON, RWB-PLT-N001-CON, RWB-P5-E1041-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-047, RD-P1-004 |

**Version 3 changes.**

- The case-state Given moves out of the Background, so AC1 runs on a closed, unheld case and AC2 on a held case (finding 1).
- The monthly run excludes held and open cases through the rwb-case retention-exclusions read; the panel keeps the single-case read for display; AC11 added (RD-P1-047; findings 2 and 3).
- The P1 side of the run is `POST /retention-runs` of rwb-source-data, started by RWB-P5-E1017-APP; this story shows no P1 row (RD-P1-047; finding 4).
- The legal-hold operation is cited to RWB-P3-E1021-CON and the list fake path is corrected (findings 3 and 5).
- Error answers use the shared Problem body with `messageCode` and `traceId` (RD-P1-004; finding 6).
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).
- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-021 for `rwb-document`; the retention class of a document type, the monthly retention run of JOB-17 and the legal hold of the case are re-homed to the target service, schema `rwb_document`, REST base `/api/recovery/document/v1` and the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-AD021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 10 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Compliance and PDPA officer**, I want **retention classes by data product and document type, and legal holds that stop expiry**, so that **nothing is kept longer than its rule and nothing held is lost**.

Legacy RWB-AD-021 carries this sentence unchanged, and the two acceptance criteria below are its own. Inside `rwb-document` the story is the retention-class and legal-hold read of the document service:

- Service `rwb-document` (P5), schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The class of a document type is served by this service: the retention class on the type row is read from the document type table version in force, and the class rules are read from `retention_rule` in `rwb_document`, which the Ownership Map gives to P5 (Architecture v5 slides 16, 41 and 44 JOB-17; ASM-0076). The published shape of the class and of the document retention state is the contract `RWB-P5-AD021-CON`; the class values, the type table and the virus scan on intake are `RWB-P5-E1041-CON` and `RWB-P5-E1041-APP`.
- The monthly retention run is **JOB-17**, a Temporal Schedule on `rwb-document` with the workflow and activities of `RWB-P5-E1017-APP`; this story starts no run, changes no run and owns no Schedule. What this story shows is the outcome of the run: the `retention_action` row of each document and the decision record its run wrote.
- The legal hold is a case attribute: `recovery_case.legal_hold` (DF-CAS-020) in P3. The Ownership Map has no document-level hold table, so the document service never copies the hold and never owns a hold row: it reads the case through the P3 case contract and projects the hold onto the documents of that case (GAP-1025; ASM-1936).
- The two screens the legacy key names, SCR-31 Document review queue and SCR-32 Document custody, are served through the gateway-bff composite route of `RWB-PLT-N001-CON` (DP-19); this story supplies the retention panel, the retention badge and the action panel of those screens and no route of its own.
- No other service's table is read (DP-01, named here as the pattern behind the ownership ruling). The case arrives through a contract, the lists arrive through the reference-data contract, and `decision_log_entry` stays P7's: this story reads the decision-log identifier the run recorded and never a decision-log row.

### 2. Business rationale

The bank keeps recovery documents under the retention schedule it agrees with Legal, and under the PDPA duty to keep personal data no longer than necessary (Program BRD, NFR-028; NFR-029; NFR-072; NFR-074). Two duties pull in opposite directions: a document past the end of its period must go, and a document a court or an investigation may need must stay. The legacy key answers both with a retention class per data product and document type and with a legal hold that overrides the class. The module features are FEAT-DCM-17 (apply retention classes to stored documents) and the retention part of FEAT-DCM-18 (the intake that assigns the class), and the requirements are REQ-DCM-016 (a legal hold stops deletion and expiry and overrides the class), REQ-DCM-019 (records retention runs by class and a disposal or an extension is a recorded decision, never silent) and REQ-DCM-020 (a records management position signed by Compliance and Legal). The legacy story carries no requirement ID of its own; the three IDs are the FSD P5 requirements it serves (FSD P5 v3 A2.17, A2.18 and section 3).

The realignment changes the mechanics, not the rule:

1. Service and base. The retention tables move to `rwb_document` under `/api/recovery/document/v1` (DP-13); no monolith table name and no shared schema survives.
2. The class becomes a resource. A class is answered as a `RetentionClass` from its own read, so the screen, the run and the tests read one shape instead of a table row, and the class code, the period, the end action and the rule version travel together (section 12.1).
3. The run belongs to `RWB-P5-E1017-APP`. JOB-17 is a Temporal Schedule in this service, not a step of this story; this story reads the run's outcome and shows it, and it never deletes, archives or extends a document itself.
4. The hold is read, never owned. `recovery_case.legal_hold` is P3's; for its reads the document service reads the case through the P3 case contract with a 2 s timeout and a breaker, and projects the flag onto its documents (GAP-1025; ASM-1936). The monthly run of RWB-P5-E1017-APP reads every held and open case through `GET /api/recovery/case/v1/cases/retention-exclusions` (RD-P1-047). No hold table, no hold column and no hold copy is created in `rwb_document`.
5. The screens come through gateway-bff (DP-19). SCR-31 and SCR-32 are composite screens: the edge calls this service once for the retention panel and the action panel, and the screen's route and field list stay `RWB-PLT-N001-CON`'s.
6. The decision record has a code. Every disposal, listing, hold or exception a run records names a decision record with the decision code **DOCRET** (FSD P5 AC-ALT-P5-017-02), and the identifier of that record is shown on the action panel, so a reader can trace a disposal to the record that authorised it.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-AD021-CON | The published contract of the class and the document retention state: the four reads of 12.1, the `RetentionClass`, `DocumentRetention`, `RetentionAction` and page shapes, the error envelope and the fakes (GAP-1025; ASM-1938) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves SCR-31 and SCR-32, so the retention panel, the badge and the action panel are reached in one hop from the edge (DP-19) |
| RWB-P5-E1041-CON | The retention classes of the document types and the virus-scan contract on intake: the class codes, the type table version in force and the class-to-type mapping this story reads |

Business preconditions carried from RWB-AD-021:

- A document is past its retention period, its case is closed and no hold applies to it (AC1), or a document whose case is under legal hold reaches the end of its period (AC2). A document of an open case is not proposed for disposal (AC11; RD-P1-047).
- Retention class values in force: **LEGAL10Y** for a demand letter of type DEMAND_LETTER and **GENERAL05Y** for an appraisal report of type APPRAISAL_REPORT (FSD P5 AC-ALT-P5-017-01 and AC-ALT-P5-017-02; RWB-P5-E1041-APP loads them).
- Retention rule version **RET-2026.11** in force, with its class rows and its valid-from date (FSD P5 AC-ALT-P5-017-02).
- The JOB-17 run date of the legacy examples is **2026-12-06** (FSD P5 AC-ALT-P5-017-02); the run itself is `RWB-P5-E1017-APP`'s.
- Lists LOV-RETENTION and LOV-RETENTION-ACTION are loaded and in force (TSD P5 T3.2; the load is `RWB-P5-E1041-APP`'s and the list rows are P3's reference data).
- A holder of the Documents right R performs the reads; a compliance or reference-data role performs the load (`RWB-P5-E1041-APP`).

The retention period of each class, the age basis of each class and the end action that follows it are **not set** in the source documents: the Program BRD records NFR-028 as Open with DL26 ("retention classes defined per type; periods not set"), so the numbers are data rows of the class load and not values of this story (GAP-1025; ASM-1939). The model of the legal hold is a case attribute with no document-level hold, so the projection onto the document is this story's reading of two sources (GAP-1025; ASM-1936). The database login is one per service (DP-02) and its name is Not specified in the source documents (GAP-1025; ASM-1942).

### 4. Flow

1. The compliance officer opens SCR-31 or SCR-32 through the gateway-bff composite route (DP-19). The edge calls this service once for the retention panel of the selected document type, with `productCode` and `docTypeCode`.
2. `RetentionClassReader`: answers the class of the type from the type row in force and the retention rule row in force, and returns `RetentionClass` (classCode, labelEn, labelTh, productCode, docTypeCode, retentionMonths, ageBasisField, endAction, ruleVersion, validFrom, validTo). A class not in force, or a type with no class, answers MSG-GEN-002 and no class.
3. The monthly retention run of `RWB-P5-E1017-APP` (JOB-17, first Sunday 02:30 Asia/Bangkok) proposes disposal for each document past its class period whose case is neither on legal hold nor open (RD-P1-047): it writes one `retention_action` row with `action` = LISTED, `run_month` and `decision_log_id`, and it records the decision record with code DOCRET naming the document, the class, the rule version and the expiry date (FSD P5 AC-ALT-P5-017-02). The same run starts the rwb-source-data side with `POST /api/recovery/source-data/v1/retention-runs` for P1's own tables; that run covers no document and this story shows none of its rows.
4. The screen shows the proposal: the retention badge turns to "Listed for disposal" with the run month and the decision-log reference. A disposal or an extension is never silent: every row of `retention_action` has a value of LOV-RETENTION-ACTION and, where the run decided, a DOCRET record (REQ-DCM-019; NFR-074).
5. `LegalHoldReader`: before this story shows a proposal, the service reads the case through the P3 contract `GET /api/recovery/case/v1/cases/{caseId}` and projects `legal_hold` (DF-CAS-020) onto the document. The run itself reads the exclusion set of held and open cases before it selects and again before each delete (`RWB-P5-E1017-APP`; RD-P1-047). Where the flag is true the document is kept, the run records `action` = HELD, and the badge shows "Legal hold" with the hold reference (REQ-DCM-016; NFR-072).
6. The action panel: `GET /documents/{documentId}/retention-actions` answers `RetentionActionPage` with documentId, runMonth, action, decisionLogId and recordedAt for the months on record, so the officer sees what the run did and when, and can name the record.
7. A refused read — no Documents right, a case outside the scope, a missing contract answer — answers the RFC 9457 error envelope with `messageCode` and changes nothing (MSG-P4-002, MSG-P4-003, MSG-GEN-006, section 14).

The order matters: the run acts first, the record is written with the action, and this story only reads and projects. No read here changes a document state, a class, a hold or a run.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The class of a document is not in the rule version in force, or the rule version has no class for that type | Refused with 422 on the class read; the panel shows no class and states that the class is not in force; no run acts on the document, which is listed as exception RETENTION_CLASS_MISSING by the run | MSG-GEN-002 | AC1, TC-AD-021-01 |
| X2 | The case of the document is under legal hold | The document is kept; the badge and the panel show the hold and its reference; `retention_action.action` is HELD and no disposal is proposed | None (the hold is information, not an error) | AC2, TC-AD-021-02 |
| X3 | The run of the month has not yet happened, so no `retention_action` row exists for the document | The action panel answers an empty page and the badge shows the class and the expiry date only; no proposal is invented | None | AC3, TC-AD-021-04 |
| X4 | The decision record cannot be read, or a `retention_action` row has no `decision_log_id` where the run decided | The panel shows the action with the reference "Not recorded" and the read answers 200 with that marker; the run's own failure is `RWB-P5-E1017-APP`'s exception, not this read's | MSG-P7-003 (raised by the run) | AC4, TC-AD-021-05 |
| X5 | The P3 case contract does not answer within 2 s, or the breaker is open | Refused with 503; no hold state is shown and no "no hold" is assumed, because the absence of an answer is not the absence of a hold | MSG-GEN-006 naming "Case service" | AC5, TC-AD-021-06 |
| X6 | The caller holds no Documents right R, or the case is outside the scope | Refused with 403; nothing is returned | MSG-P4-002 or MSG-P4-003 | AC6, TC-AD-021-07 |

Two target-service notes:

- X5 is the one place where the target is stricter than the legacy story: a legacy in-process read could not fail separately from the caller, while a one-hop read can. An unanswered case contract therefore fails closed — the screen shows no hold state rather than a "no hold" that might be wrong.
- X1 keeps the legacy behaviour of FSD P5 AC-EXC-P5-017-02: the document is unchanged and the run lists it as an exception; this story only shows the exception and never repairs the class.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs three contract stories (`RWB-P5-AD021-CON`, `RWB-PLT-N001-CON`, `RWB-P5-E1041-CON`), all contract work; no app story of another lane is a precondition |
| Negotiable | The class values, the periods, the end actions and the list values are data rows; the story fixes the reads, the panel and the badge |
| Valuable | It is the only place an officer can see why a document is still held, why it was listed for disposal, and which record authorised it |
| Estimable | One service, four reads, one panel, one badge, one action panel, no new table |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below is one test case in section 16; the run itself is proved by `RWB-P5-E1017-APP` |

### 7. Acceptance criteria

```gherkin
Feature: Retention classes and legal hold

  Background:
    Given retention rule version "RET-2026.11" is in force from its valid-from date
    Given retention class "LEGAL10Y" applies to document type "DEMAND_LETTER" for product "MORTGAGE"
    Given retention class "GENERAL05Y" applies to document type "APPRAISAL_REPORT" for product "MORTGAGE"
    Given the rwb-document retention contract mock returns retention class "GENERAL05Y" for type "APPRAISAL_REPORT"

  Scenario: AC1 Expiry (legacy RWB-AD-021 AC1)
    Given a document past its retention period with no hold
    And its case "RW-2026-000123" is closed, the rwb-case contract mock returns legal_hold false and the case is not in the retention-exclusions answer
    When the retention job runs
    Then the system proposes disposal and recorded, never silent

  Scenario: AC2 Hold (legacy RWB-AD-021 AC2)
    Given a document under legal hold
    And the rwb-case contract mock returns case "RW-2026-000123" with legal_hold true and the retention-exclusions answer holds it with reason LEGAL_HOLD
    When its retention period ends
    Then the system keeps it and the hold is shown

  Scenario: AC3 A run month with no retention action is shown empty and not invented (new, D-RCV-60)
    Given a document of class GENERAL05Y with no retention_action row for the run month
    When the action panel is read
    Then the panel answers an empty page, the badge shows the class and the expiry date only, and no proposal is shown

  Scenario: AC4 A missing decision reference is shown as Not recorded (new, D-RCV-60)
    Given a retention_action row with no decision_log_id where the run decided
    When the action panel is read
    Then the panel shows the action with the reference "Not recorded" and the read answers 200

  Scenario: AC5 A case contract that does not answer is refused and no hold is assumed (new, D-RCV-60)
    Given the rwb-case contract does not answer within 2 s
    When the retention panel is read
    Then the read is refused with 503 and MSG-GEN-006, and no hold state is shown

  Scenario: AC6 A case outside the caller's scope is refused (new, D-RCV-60)
    Given the caller holds Documents right R and the case is outside the caller's scope
    When the retention panel is read
    Then the read is refused with 403 and MSG-P4-003, and nothing is returned

  Scenario: AC7 The decision log is never disposed by this path (new, D-RCV-60)
    Given a retention run that cites a decision_log_entry held under the ledger's own period
    When the retention run and the retention panel are read
    Then no decision_log_entry row is read, written or deleted by this service

  Scenario: AC8 A read without a valid session or on an unknown document is refused with 401 or 404 (new, D-RCV-60)
    Given a caller with no valid session, or a documentId that does not exist
    When the retention panel or the action panel is read
    Then the read is refused with 401 or 404 and nothing is returned

  Scenario: AC9 A consumed call that fails or does not answer is refused and no hold is assumed (new, D-RCV-60)
    Given the rwb-case contract fails or does not answer the call
    When the retention panel is read
    Then the read is refused with 503 and MSG-GEN-006 naming "Case service", and no hold state is shown

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given a document whose retention action is ARCHIVED
    When a change of its status to LISTED is requested
    Then the change is refused and no retention_action row is written

  Scenario: AC11 A document of an open case is not proposed for disposal (new, RD-P1-047)
    Given a document past its retention period whose case is open and not on legal hold, so the retention-exclusions answer holds it with reason OPEN
    When the monthly run has completed and the action panel is read
    Then no "retention_action" row exists for the document for that run month and the panel answers an empty page for it
    And the badge shows the class and the expiry date only, with no "Listed for disposal" and no "Legal hold"
```

Every legacy Given, When and Then line is kept unchanged; the Background Givens and the case-state lines of AC1 and AC2 are added for the target run, because the class, the rule version and the hold now come from a contract that has to be named. **Target reading.** AC1's "retention job" is JOB-17, the Temporal Schedule of `RWB-P5-E1017-APP` (first Sunday 02:30 Asia/Bangkok); its proposal on a document past its period is `retention_action.action` = LISTED plus the decision record with code DOCRET naming the document, its class, the rule version and its expiry date, and "recorded, never silent" is read as that record and that row — the legacy wording is kept exactly as written, including its grammar, and is not paraphrased. AC2's hold is `recovery_case.legal_hold` (DF-CAS-020) in P3, read through the P3 case contract and projected onto the document by this service, shown on the badge and the panel with the hold reference; the run records `action` = HELD and archives nothing (GAP-1025; ASM-1936). Where a test needs a class or a hold that the fakes do not carry, the fixture is added to the fake of section 12.8 and no business value is written into the test.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document type carries one retention class, held as versioned data with its rule version, its valid-from and its valid-to date | NFR-028; REQ-DCM-019; FSD P5 A2.17; DL26 |
| BR2 | A document past its retention period is proposed for disposal by the monthly run, and a `retention_action` row plus a decision record states what the run did | REQ-DCM-019; NFR-074; FSD P5 AC-ALT-P5-017-02 |
| BR3 | A legal hold overrides the class: a document whose case is under hold is kept and is shown as held, whatever its period | REQ-DCM-016; NFR-072; FSD P5 AC-ALT-P5-017-02 |
| BR4 | A disposal, a listing, a hold and an exception are never silent: every action carries a LOV-RETENTION-ACTION value, and every decided disposal names its DOCRET record | REQ-DCM-019; NFR-074 |
| BR5 | The decision log is never disposed by this path: `decision_log_entry` is P7's and the retention run holds it under its own period | NFR-030 (the ledger's own period); Ownership Map; DP-01 |
| BR6 | The class and the hold are read, never copied: the class is read in the version in force and the hold is read through the P3 case contract on every read | DP-01; ASM-1936 |
| BR7 | Every read checks the role, the capability area and the scope before it answers, and is written to the access log by the ACE common module | CTL-09; REQ-ACA-006; legacy RWB-AD-021 permission rows |
| BR8 | The run belongs to `RWB-P5-E1017-APP`: this story starts no run, changes no run and owns no Schedule, and it never deletes, archives or extends a document itself | Architecture v5 slide 44 JOB-17; FSD P5 A2.17 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by `retention_rule` rows in `rwb_document` (DF-REF-116 to DF-REF-126) with `rule_version`, `valid_from` and `valid_to`, and by the class on the type row (DF-REF-223). Neither a period nor a class code is written in code; the load is `RWB-P5-E1041-APP`'s and the authority is RW-COMPLY's.
- BR2 and BR4 are executed by the run of `RWB-P5-E1017-APP` in one transaction: the `retention_action` row (DF-DOC-091 to DF-DOC-095) and the decision record with code DOCRET commit together, so there is no action without a record and no record without an action.
- BR3 is executed by the order of operations: the run reads the held and open cases through the rwb-case retention-exclusions read before it acts (RD-P1-047), and this story re-reads the case before it shows a state, so a hold placed after the last run is still shown, and a document whose case contract cannot answer is never shown as free of hold (X5).
- BR5 is executed by the Ownership Map: no `decision_log_entry` row is read, written or deleted here; the story shows `decision_log_id` as a reference and P7 keeps the ledger under NFR-030.
- BR6 is executed by there being no hold column and no class copy in `rwb_document`: the only persisted values are the class on the document row as assigned at intake (DF-DOC-009) and the action rows of the run; the hold itself stays a case attribute.
- BR7 is executed by the authorisation decision the service template's guard holds and by the ACE common module's PII access log; this package writes no access-log entry and returns no personal value.
- BR8 is executed by this story providing reads only (12.1): it declares no operation that starts, stops or re-runs JOB-17.

### 9. State transitions

The document's retention state as the officer sees it. The values are LOV-RETENTION-ACTION (TSD P5 T3.2); the case status is not changed by any transition here.

| From | Event | To |
|---|---|---|
| ACTIVE, not past the period | the monthly run of JOB-17 finds the document inside its period | ACTIVE (no `retention_action` row, or a row with no action value; nothing is written) |
| ACTIVE, past the period, case closed and no hold | the monthly run lists the document for disposal | LISTED, with `run_month`, `decision_log_id` and the DOCRET record |
| ACTIVE, past the period, case open and no hold | the monthly run finds the case in the retention-exclusions set with reason OPEN | ACTIVE (not selected; no `retention_action` row) |
| ACTIVE, past the period, case under legal hold | the monthly run finds the case in the retention-exclusions set with reason LEGAL_HOLD | HELD, with the hold shown on the badge and no disposal proposed |
| ACTIVE, past the period, class not in the rule version in force | the monthly run cannot resolve the class | EXCEPTION (RETENTION_CLASS_MISSING), the document unchanged (FSD P5 AC-EXC-P5-017-02) |
| LISTED | the run of a later month applies the end action of the class | ARCHIVED, with its own DOCRET record and `run_month` |
| LISTED | a hold is placed on the case before the end action | HELD; the disposal waits while the hold is in place |
| LISTED, HELD or EXCEPTION | a later run re-evaluates the document | the value of that month's action; the earlier rows stay readable |

Every transition is written by the run of `RWB-P5-E1017-APP`, never by this story: this story reads the latest row and shows it. The badge states in section 15 are the same values, so a screen state and a stored value can never disagree.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods and the class decisions; reads the retention panel, the badge and the action panel for any case in scope |
| RW-REFADM, reference data administrator | Loads the class rows and the lists (`RWB-P5-E1041-APP`); this story reads them and never writes them |
| Holder of Reference data A | Approves a class load and a rule version (`RWB-P5-E1041-APP`); this story names the approval and does not perform it |
| RW-DATASTEW, data steward | Reads the class of a type and the actions of a document to answer a records question |
| RW-PLATADM, platform administrator | Re-runs JOB-17 through `RWB-P5-E1017-APP`; this story provides no operation for it |
| Roles with Documents R (for example RW-CASEOWN, RW-TEAMMGR, RW-AUDIT) | Read the retention panel and the action panel inside their scope |
| SY-DOCUMENT, the rwb-document service identity | Reads the case hold through the P3 case contract on the flight of a read, and the retention-exclusions set in the run |
| SY-P7, the decision record writer | Writes the DOCRET record of each action in the run's transaction |
| Nobody | Changes a class, places or lifts a hold, or disposes of a document under a hold |

No delegation-of-authority level applies to this story: a retention class and a legal hold are not a financial decision, so no DoA value is read anywhere (the DoA table is P4's, `delegation_limit`). The authorisation decision is taken by `rwb-access` and consumed as the cached permission decision the service holds; the refusal shape is 403 with MSG-P4-002 or MSG-P4-003. The database login is per service (DP-02): the story refers to "the rwb-document login (DP-02)" and its name is Not specified in the source documents (GAP-1025; ASM-1942).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Read |
| DF-DOC-025 | `document` | previous_version_id (a superseded version keeps its class and is read with it) | Read |
| DF-DOC-026 | `document` | content_sha256 (named on the action panel as the evidence of the file the run acted on) | Read |
| Standard column | `document` | state, is_active, version, created_at | Read |
| DF-REF-116 to DF-REF-126 | `retention_rule` | id, product_code, table_name, record_class, retention_months, age_basis_field, end_action, rule_version, valid_from, valid_to, approved_by | Read |
| DF-REF-219 | `document_type` | doc_type_code (the type the class is resolved for) | Read |
| DF-REF-223 | `document_type` | retention_class | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-DOC-091 to DF-DOC-095 | `retention_action` | id, document_id, run_month, action, decision_log_id | Read |
| DF-CAS-020 | `rwb-case` case, through the contract | legal_hold | Read |
| DF-CAS-001 | `rwb-case` case, through the contract | id | Read |
| (decision record) | decision-record library table in `rwb_document`, written by `RWB-P5-E1017-APP` | the DOCRET record of each action | Read |

Field IDs are those of the Logical Data Model and Data Dictionary and of TSD P5 T3.1 and TSD P1 T3.1 (`retention_rule`, which Architecture v5 slides 16, 41 and 44 place with P5; ASM-0076). No `rwb_case` row is copied and no `v_ace_*` view is read by this service: DF-CAS-001 and DF-CAS-020 arrive inside the P3 case answer (DP-01). The legacy data table of RWB-AD-021 named `document` (id, case_id, person_key, document_type, source, storage_ref and 5 more; DF-DOC-001 to DF-DOC-011) and `rule_row` (DF-REF-001 to DF-REF-015); the first is kept with its field IDs, and the second is superseded in the target by `retention_rule` (DF-REF-116 to DF-REF-126), because `rule_row` is P7's rule registry and not a retention table (Ownership Map). The list LOV-RETENTION-END on DF-REF-122 holds ARCHIVE and REVIEW; the list LOV-RETENTION-ACTION on DF-DOC-094 holds ARCHIVED, LISTED, HELD and EXCEPTION (TSD P5 T3.2). No personal data enters a log, a test or an example: the panel shows the case number, the type code and the class, never a customer field.

### 12. Contract

#### 12.1 REST operations provided

Owner P5 (`rwb-document`); base `/api/recovery/document/v1`. The four reads below are this key's share of the retention surface and are published in `RWB-P5-AD021-CON`.

| Operation | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/retention-classes` | P5 | Query productCode, docTypeCode, page, size; answer `RetentionClassPage`; Documents R. The paths are this baseline's design and are Not specified in the source documents (GAP-1025; ASM-1938) |
| GET | `/api/recovery/document/v1/retention-classes/{classCode}` | P5 | Answer `RetentionClass`; the class of a type in the rule version in force; 404 when the class is not in force and 422 when the class has no row for the type |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention` | P5 | Answer `DocumentRetention` (documentId, retentionClass, expiryDate, state, legalHold, legalHoldRef, lastAction); the hold is the projected case hold |
| GET | `/api/recovery/document/v1/documents/{documentId}/retention-actions` | P5 | Answer `RetentionActionPage` (documentId, runMonth, action, decisionLogId, recordedAt); the rows of the months on record |

The admin load and the run operations of the same surface — `POST /api/recovery/document/v1/admin/retention-loads`, `POST /api/recovery/document/v1/admin/retention-loads/{loadId}/approve`, `GET /api/recovery/document/v1/admin/retention-runs` and `POST /api/recovery/document/v1/admin/retention-runs/{runId}/rerun` — belong to `RWB-P5-E1041-APP` (the load and its approval) and `RWB-P5-E1017-APP` (the run, its answer and its re-run, which answers 409 while a run is in progress). This story provides none of them and names them so no reader mistakes a run control for a document read.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | RWB-P3-E1018-CON | The case exists, is in the caller's scope and carries `legal_hold`; one hop, 2 s timeout, breaker per downstream (DP-11) |
| POST | `/api/recovery/case/v1/cases/{caseId}/legal-hold` | P3 | RWB-P3-E1021-CON | The hold is placed and lifted by `rwb-case`; this story never calls it, and it is listed so the baseline shows that no hold write exists here |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 | RWB-P3-E1043-CON | LOV-RETENTION and LOV-RETENTION-ACTION at the version in force; no list value is typed in code (DP-07's list, read as a contract) |

The story's Contract dependencies row is **None** in the plan, while these three P3 rows are consumed. That is recorded, not silently fixed: the rows are faked and the lists are read through the client library, and the missing C entries are the gap of the key (GAP-1025; ASM-1937). No row is added to the metadata table.

#### 12.3 Events published

None. The service publishes exactly two events, `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, on `rwb.document.events.v1` (Architecture v5 slides 41, 42 and 43); a class load, a read of a class and a `retention_action` row publish neither, and this key publishes no event at all. The decision record of a run reaches the shared decision-record topic through the decision-record library of `RWB-P5-E1017-APP`, not from this story.

#### 12.4 Events consumed

None. The hold is read synchronously through the P3 case contract on the flight of each read, so a hold placed a minute ago is already visible; nothing is projected from a topic and no inbox row is written by this story. The retention-exclusions read and the rwb-source-data retention-run operations belong to `RWB-P5-E1017-APP`.

#### 12.5 Workflows and activities

None. The run is the `RetentionRunWorkflow` of `RWB-P5-E1017-APP` on task queue `rwb-document`; this story contributes no workflow, no activity and nothing to the queue.

#### 12.6 Schedules

| Schedule | Job | Owner | Note |
|---|---|---|---|
| Retention | JOB-17, monthly, first Sunday 02:30 Asia/Bangkok | RWB-P5-E1017-APP | Named here because AC1's "retention job" is this Schedule; this story neither creates nor changes it, and the legacy Quartz entry is replaced by a Temporal Schedule (Architecture v5 slide 44) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Read: the class on the document row, the type, the case, the state and the hash |
| `retention_rule` | P5 | Read: the class rows in the version in force (ASM-0076) |
| `retention_action` | P5 | Read: the action, the run month and the decision-log reference of each month |
| `document_type` | P5 | Read: the class of the type and the type table version |
| decision-record library table | PLT library, created in `rwb_document` | Read only here: the DOCRET record the run wrote |

`decision_log_entry` is P7's, `recovery_case` is P3's, `lov_value` and `reference_row` are P3's reference data; they are named as consumed answers and never declared as this service's tables (DP-01). No foreign-schema read and no ACE view (DP-05).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case fake (`GET /api/recovery/case/v1/cases/{caseId}`) | RWB-P3-E1018-CON | The case with `legal_hold` true and false, closed and open, the case outside the scope, the 2 s timeout and the open breaker (X2, X5) |
| rwb-case retention-exclusions fixture | RWB-P3-E1021-CON | A case with reason LEGAL_HOLD and a case with reason OPEN, used by the run in the end-to-end pair (AC1, AC2, AC11) |
| rwb-case reference-data fake (`GET /api/recovery/case/v1/admin/lists/{listCode}`) | RWB-P3-E1043-CON | LOV-RETENTION with LEGAL10Y and GENERAL05Y, and LOV-RETENTION-ACTION with ARCHIVED, LISTED, HELD and EXCEPTION |
| retention contract fake | RWB-P5-AD021-CON | The four reads: a class in force, a class not in force, a document past its period, a document under hold, an empty action page and the 422 of X1 |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The one call the screen path makes for the panel and the badge (DP-19) |
| class and rule fixture | RWB-P5-E1041-APP | Rule version RET-2026.11 with a LEGAL10Y row for DEMAND_LETTER and a GENERAL05Y row for APPRAISAL_REPORT; the periods are placeholders of the fixture and not business values (ASM-1939) |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4, consumed 3 | The class list, the class read, the document retention read and the action page; the case read, the hold read and the reference-list read of P3 |
| Kafka | 0 published, 0 consumed | This key publishes none of the two `rwb.document` events and consumes no topic |
| Temporal | None | JOB-17 and `RetentionRunWorkflow` are `RWB-P5-E1017-APP`'s |
| File | None | The story reads no blob and writes no blob; the archive location of a run belongs to `RWB-P5-E1017-APP` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/retention`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentRetentionController | Controller | The four reads of 12.1; maps each exception to the RFC 9457 problem response with its `messageCode`; the access check and the scope |
| RetentionClassReader | Repository | Reads `retention_rule` and `document_type` in the version in force by `valid_from` and `valid_to`, and builds `RetentionClass`; never writes |
| DocumentRetentionService | Service | Composes `DocumentRetention` from the document row, the class, the expiry date and the latest `retention_action` row; resolves the state of section 9 |
| LegalHoldReader | Client | Reads the case through the P3 case contract, projects `legal_hold` and the hold reference, and fails closed on a timeout (X5) |
| RetentionActionPanel | React component | The action panel: one row per month with the action, the decision-log reference and the date |
| DocumentRetentionBadge | React component | The badge of SCR-31 and SCR-32: the class, the expiry date and the state of section 9, with the hold label |

**Database.**

- No new table and no migration of its own: the story reads `document`, `document_type`, `retention_rule` and `retention_action`, and the tables and their indexes arrive with `RWB-P5-E1041-APP` (`document_type`, `retention_rule`) and `RWB-P5-E1017-APP` (`retention_action`).
- Two read indexes are contributed when those stories create the tables: `ix_retention_rule_version_class ON retention_rule (rule_version, record_class)` and `ix_retention_action_document_month ON retention_action (document_id, run_month)`; the second is what keeps the action page inside the 2 s budget of the composite route.
- The decision-record row is read only; the story writes no row of any table.

**Configuration and reference data.**

- Rule version RET-2026.11 in force, loaded and approved through `RWB-P5-E1041-APP`; the class rows and their periods are data (NFR-028 is Open under DL26, so a period is never a constant in this module).
- LOV-RETENTION and LOV-RETENTION-ACTION read through the reference-data contract; LOV-RETENTION-END (ARCHIVE, REVIEW) read with the class row.
- Decision code DOCRET read from the class row of the run and shown as a reference; the LOV-DECISION list is the data steward's load, not this story's.
- Feature flag `rwb.document.retention-view`. Off: the four reads answer 404 and the panel and the badge are not rendered; the tables and the run are unaffected.

**Build steps**

1. Build `RetentionClassReader` with the `valid_from` and `valid_to` rule on both tables and the class-in-force resolution; unit test a boundary date and the missing-class case X1.
2. Build `DocumentRetentionService` over the document row, the class and the latest action row; unit test the seven states of section 9, including the empty action page of X3.
3. Build `LegalHoldReader` against the case fake, with the 2 s timeout and the open breaker; unit test the projection of a true and a false hold and the fail-closed path X5.
4. Build the four reads with the access check and the scope; API tests for AC1, AC2, X4, X5 and X6, and the access test TC-AD-021-03.
5. Build `RetentionActionPanel` and `DocumentRetentionBadge` against the composite-route fake; component tests for the hold label, the listed label, the exception label and the "Not recorded" marker of X4.
6. Run the end-to-end pair with `RWB-P5-E1017-APP` in SIT: a document of a closed case past its period with no hold (AC1), the same document under a case hold (AC2) and under an open case (AC11), each with its `retention_action` row and its DOCRET record read back through this story's reads.
7. Prove the boundary: no write of this module reaches `document`, `retention_rule`, `retention_action` or the case, and a read of a document of a case outside the scope answers 403 with MSG-P4-003.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as the negative of the legacy pattern and is stated so a reader does not look for a view: the legacy retention story read no ACE source, and in the target the document keeps the ACE customer as a business key (DF-DOC-003 `party_id`) and the case as a cross-reference (DF-DOC-002 `case_id`), so this service reads no `v_ace_*` view and no `account_ext` row, and any customer attribute a screen needs is requested through the owner's contract (`rwb-source-data` for the ACE views, `rwb-case` for the case). DP-13 fixes the base of the four reads and of the two screens' calls. DP-19 puts the panel and the badge behind the gateway-bff composite route, so the screen makes one call per service and never chains two. The hold read and the list read are DP-11 in shape — a published contract, one hop, a 2 s timeout, a fake — because the plan gives this story a Contract dependencies list of None and only step D1 may change the plan (GAP-1025; ASM-1937).

**Done when.** The tests of section 16 pass, the boundary test of build step 7 passes, the panel and the badge answer within 2 seconds in SIT through the composite route for a case with 40 documents, and a document past its period with no hold shows LISTED with its DOCRET reference while the same document under a case hold shows HELD and is not disposed of.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | A change to a write-once legal document is attempted from the panel (the legacy refusal of this key) | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-003 | A document is in the review queue and its class is not yet confirmed | Some fields need checking. The document is in the review queue. |
| MSG-P5-004 | An original document is overdue back from its holder | {document} is due back from {holder} since {date}. |
| MSG-GEN-001 | A required field of a read is empty, for example no `docTypeCode` on the class list | Enter {field}. |
| MSG-GEN-002 | A class is not in the rule version in force for its type (X1) | Not specified in the source documents (DOR-RWB-P5-AD021-APP-9) |
| MSG-P4-002 | The caller holds no Documents right R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record of a run action cannot be read (X4); raised by the run | Not specified in the source documents (DOR-RWB-P5-AD021-APP-9) |
| MSG-P1-020 | The run summary alert of the month names the cases kept on legal hold | The run summary of the month, whose text is Not specified in the source documents (GAP-1025; ASM-1936); the message ID and the count it carries are FSD P1 AC-ALT-P1-017-02's and `RWB-P5-E1017-APP`'s |
| MSG-GEN-006 | The P3 case contract does not answer within 2 s, or the breaker is open | {system} is not available. Try again in a few minutes. |

The five business messages are the legacy messages of RWB-AD-021, copied word for word, and they keep their legacy types: MSG-P5-002 and MSG-GEN-001 and MSG-P4-002 are errors, MSG-P5-003 is information and MSG-P5-004 is a warning. MSG-P4-003 is the scope refusal the legacy endpoints answered, MSG-GEN-006 is the platform unavailable message whose {system} value is "Case service" on a case-contract timeout, and MSG-P1-020 is the run summary this story displays and never composes. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

The HTTP mapping is carried from the legacy endpoints of the key, rebased under `/api/recovery/document/v1` (GAP-1025; ASM-1940): 401 when the caller is not authenticated, 403 for MSG-P4-002 and MSG-P4-003, 404 when the document or the class does not exist, 409 when a read meets a run in progress on the same document, 422 for MSG-GEN-002 when a class is not in the rule version in force (X1) and for MSG-GEN-001 when a required query field is empty, 503 for MSG-GEN-006 and for a P3 timeout. Every error is an RFC 9457 problem response with `messageCode` set to the ID above, `detail` carrying the text with its placeholders filled and `instance` naming the request; the four reads are GETs and declare no `Idempotency-Key`.

### 15. Screens and states

SCR-31 Document review queue and SCR-32 Document custody are published through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`); this story supplies the retention panel, the retention badge and the action panel of both, and the route, the screen field list and the merge order stay the edge contract's (GAP-1025; ASM-1941).

| Screen | Legacy states | What this story adds |
|---|---|---|
| SCR-31 Document review queue | Loading; list; reviewed; empty, error and no access: Not specified in the source documents (CG-ALL-5712) | The retention badge on each row: the class, the expiry date and the state of section 9; the panel opens from the badge |
| SCR-32 Document custody | Out; overdue; returned; empty, loading, error and no access: Not specified in the source documents (CG-ALL-5713) | The same badge on the custody row, and the hold label where the case is under hold, so a held original is never recalled for disposal |

| Badge state | What the user sees |
|---|---|
| Loading | The badge skeleton while the composite route answers |
| Active | The class label, the expiry date and no action label |
| Listed for disposal | The class label, the expiry date, "Listed for disposal", the run month and the decision-log reference |
| Legal hold | The class label, "Legal hold" and the hold reference; no proposal is shown |
| Exception | The class label in error state with the class-not-in-force message (MSG-GEN-002) and a link to the reference data record |
| Not read | The message of section 14 (MSG-P4-002, MSG-P4-003 or MSG-GEN-006) with a retry action; the badge never shows a "no hold" when the case contract did not answer (X5) |

The action panel is a tab of the same panel: one row per month with the action, the decision-log reference, the date, and the "Not recorded" marker where the run decided but the reference is missing (X4). A held document shows no action button anywhere, and no state of this story offers one.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-021-01 | AC1, BR1, BR2, BR4, BR8 | End to end | Appraisal report of class GENERAL05Y stored on 1 November 2021 on case RW-2026-000123 with no hold; JOB-17 runs on 6 December 2026; the document is listed with its DOCRET record (FSD P5 AC-ALT-P5-017-02) |
| TC-AD-021-02 | AC2, BR3, BR6 | End to end | The same appraisal report with case RW-2026-000123 under legal hold; the run keeps it and the badge shows the hold |
| TC-AD-021-03 | Access, BR7 | Component | A role without the Documents right R reads the retention panel; refused with MSG-P4-002 and nothing returned |
| TC-AD-021-04 | AC3, X3 | Component | A document of class GENERAL05Y with no retention_action row for the run month; the action panel answers an empty page and the badge shows the class and the expiry date only |
| TC-AD-021-05 | AC4, X4 | Component | A retention_action row with no decision_log_id where the run decided; the panel shows "Not recorded" and the read answers 200 |
| TC-AD-021-06 | AC5, X5 | Component | The P3 case contract does not answer within 2 s; the read is refused with 503 and MSG-GEN-006 naming "Case service", and no hold state is shown |
| TC-AD-021-07 | AC6, X6 | Component | A caller with Documents right R reads a case outside the caller's scope; refused with 403 and MSG-P4-003, and nothing is returned |
| TC-AD-021-08 | AC7, BR5 | Component | A retention run cites a decision_log_entry under the ledger's own period; no decision_log_entry row is read, written or deleted by this service |
| TC-AD-021-09 | AC8 | Component | A caller with no valid session, and a documentId that does not exist; the read is refused with 401 or 404 and nothing is returned |
| TC-AD-021-10 | AC9 | Component | The rwb-case contract fails the call; the read is refused with 503 and MSG-GEN-006 naming "Case service", and no hold state is shown |
| TC-AD-021-11 | AC10 | Component | A document whose retention action is ARCHIVED; a change of its status to LISTED is requested; the change is refused and no retention_action row is written |
| TC-AD-021-12 | Operations, events and activities of section 12 (contract) | Contract | Contract fake of section 12.8; each operation, event and activity of section 12 answered as the contract declares it |
| TC-AD-021-13 | Boundary of each table of section 12.7 (ASM-3438) | Component | Each table of section 12.7 read at its boundary, using the fake of section 12.8; no business value written into the test |

AC11: TC: TC-P5-AD021-APP-03 (Test Cases v9). The data of TC-AD-021-01 and TC-AD-021-02 gains the case state (closed and unheld; held): TC: to be updated in Test Cases v9 (W2-tests).

The legacy levels map System to End to end and Access to Component; the legacy `Test` column of the three cases is "Expiry", "Hold" and "A role without the right is refused with MSG-P4-002", and it is kept in the Data column. No integration harness copy is named for this key: no `RWB-ITG-AD021-ITG` story exists in the plan, so this story names none. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the class codes, the periods, the age bases, the end actions, the rule version, the list values and the decision code are data rows or list values, and where a period is unset it stays unset (NFR-028, DL26).
- No personal data in events, workflow inputs, payloads, logs, fakes or tests. The panel shows the case number, the type code, the class and the counts; a test document is synthetic and carries no customer field.
- No read of another service's tables (DP-01). The case and the hold arrive through the P3 case contract, the lists through the reference-data contract, one hop with a 2 s timeout; the decision ledger stays P7's and is named by its identifier only.
- No ACE view and no `account_ext` row is read by this service (DP-05); ACE data is reached only through the owner's contract.
- The hold is never overridden and never copied: no hold column, no hold table and no local hold state exists in `rwb_document`.
- The decision log is never disposed by this path: this story deletes no `decision_log_entry` and no record.
- The run is never started, stopped or re-run here; JOB-17 belongs to `RWB-P5-E1017-APP`.
- Every read checks the role, the capability area and the scope, and the PII access log entry is written by the ACE common module, never by this package.
- No module of this story writes a row: the SQL surface of the module is four reads, and a write fails the boundary test of build step 7.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Feature | Test cases | L3 process |
|---|---|---|---|---|---|
| REQ-DCM-016 | A legal hold applied to a case or a document stops deletion and expiry while it is in place, overriding the retention class | FSD P5 v3 section 3; Program BRD NFR-072 | FEAT-DCM-17 | TC-AD-021-02 | Not specified in the source documents (DOR-RWB-P5-AD021-APP-2) |
| REQ-DCM-019 | Records retention runs by class, and a document at the end of its period is disposed of or extended by a recorded decision, never silently | FSD P5 v3 section 3; Program BRD NFR-074 | FEAT-DCM-17 | TC-AD-021-01 | Not specified in the source documents (DOR-RWB-P5-AD021-APP-2) |
| REQ-DCM-020 | The hub carries a records management position signed by Compliance and Legal, covering storage, backup, legal hold, discovery and disposal | FSD P5 v3 section 3 | FEAT-DCM-17, FEAT-DCM-18 | TC-AD-021-01, TC-AD-021-02 (the position itself is a Compliance deliverable outside this service) | Not specified in the source documents (DOR-RWB-P5-AD021-APP-2) |

The legacy story RWB-AD-021 carries **no requirement ID of its own**: its metadata names the epic, the module, the feature, the process and the decision DL26, and the three IDs above are the FSD P5 requirements the behaviour serves. The story also serves NFR-028 (a class per type, periods not set), NFR-029 (write-once inside the period), NFR-072 and NFR-074, and the module features FEAT-DCM-17 (apply retention classes to stored documents) and FEAT-DCM-18 (virus scan on intake, which assigns the class at intake).

| Legacy reference | Where it is kept |
|---|---|
| Retention classes LEGAL10Y and GENERAL05Y | Background, sections 3, 7, 8, 12.8 |
| Retention rule version RET-2026.11 and the JOB-17 run date 2026-12-06 | Background, sections 3, 4, 12.6, 16 |
| Decision code DOCRET | Sections 2, 4, 8, 12.3, 13, 15 |
| LOV-RETENTION, LOV-RETENTION-ACTION (ARCHIVED, LISTED, HELD, EXCEPTION) and LOV-RETENTION-END (ARCHIVE, REVIEW) | Sections 3, 8, 9, 11, 12.7, 12.8 |
| Screens SCR-31 Document review queue and SCR-32 Document custody, and their legacy states Loading; list; reviewed and Out; overdue; returned | Sections 1, 12.9, 15 |
| Messages MSG-P5-002, MSG-P5-003, MSG-P5-004, MSG-GEN-001, MSG-P4-002 | Sections 5, 14 |
| Decision DL26 (retention classes defined per type, periods not set; open, assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) | Sections 2, 3, 8, 18 |
| Legacy key RWB-AD-021 and test cases TC-AD-021-01 to TC-AD-021-03 | Metadata, sections 3, 16 |
| The legacy permission rows (Documents C and Documents R with their role lists) | Sections 10, 17 |

### 19. Out of scope

- The retention run itself: the `RetentionRunWorkflow`, JOB-17, the archive action, the re-run and the run answer (`RWB-P5-E1017-APP`).
- The retention classes and the virus scan on intake: the type table, the class load, the list loads and the scan (`RWB-P5-E1041-APP`, `RWB-P5-E1041-CON`).
- The document store, the class assigned to a document at intake, and the document reads and version reads (`RWB-P5-E1024-APP`, `RWB-P5-E1026-APP`).
- The personal data screen SCR-47 and the PDPA data-subject paths (Epic 8), and the records management position document itself (REQ-DCM-020, a Compliance deliverable).
- The retention period of the decision log (NFR-030) and the ledger itself: `decision_log_entry` is P7's and `RWB-P7-E1027-CON` is its contract.
- Case closure or any case status change after a retention action (REQ-S7-008 and the case stories).
- The gateway-bff composite route, the screen field list and the merge order of SCR-31 and SCR-32 (`RWB-PLT-N001-CON`).
- The published contract documents of this service, their fakes and their versioning (`RWB-P5-AD021-CON`), and the Helm chart, the retry values, the metrics, the alerts and the runbook.

### 20. Remaining delivery steps

- Size the story at refinement (squad).
- RWB-P5-AD021-CON, RWB-P5-E1041-CON and RWB-PLT-N001-CON Done with their fakes published at a pinned version (contract owners).
- Bank retention schedule for the class periods, DL26 (Compliance).
- Add the AC11 test case row and update TC-AD-021-01 and -02 in Test Cases v9 and the RTM (test lead).
- Load the synthetic test data in DEV (platform administrator).
