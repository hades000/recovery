# RWB-S8-E7009-APP Match a complaint to the preceding contact

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7009-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the complaint-to-contact slice of RWB-E7-009 in rwb-deviation. The two legacy criteria are kept word for word with their origin tag; the step binds the open X1 deviation of a complaint to the contact that caused it, records the result through the local decision-record library before any change (DP-03), reads the preceding contact from rwb-source-data (DP-18) and the DEV package version from rwb-decision, and serves the match branch of the published `PATCH /deviations/{deviationId}` on base `/api/recovery/deviation/v1` (DP-13) behind SCR-08 through the gateway-bff composite route (DP-19). The `deviation` table carries no contact or complaint reference, no published rule row expresses the match, no requirement row traces to FEAT-DVF-09, and the Conduct and QA officer holds R only on the case record while the feature needs U (GAP-3068; ASM-5212, ASM-5214, ASM-5216, ASM-5217). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer**, I want **to link each complaint to the contact that caused it, which is how conduct is measured**, so that **every deviation has a handler and a clock**.

This is the complaint-to-contact slice of legacy RWB-E7-009. It owns:

- the two legacy criteria this story owns (AC1, AC2), copied verbatim with their origin tag, and the messages, the operation and the screen they depend on;
- one step of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` that can start at any time on a case (context pack, Temporal and Drools slide 13);
- the binding of an open X1 deviation to the contact that caused the complaint: the complaint reference and the contact reference are taken on the request, the contact is read from rwb-source-data, and the result is the match the conduct measure rests on (FSD S8 A2.18.2; ASM-5212, ASM-5213);
- the record of the match through the local decision-record library, with the DEV package version in force, **before any change**, because AC1 asks for the result in the decision log with the rule version (DP-03; ASM-5214);
- the match branch of the published `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1`, with the case-record right U, the scope filter, the `DeviationOutcome` request and the `Deviation` answer (DP-13);
- SCR-08 Deviation queue in its list state behind the gateway-bff composite route, where the officer confirms the match (DP-19).

It does not own: the published shapes of the two operations, the `Deviation`, `DeviationRequest` and `DeviationOutcome` elements, the match properties, the consumed rows, the error set and the fakes, which are RWB-S8-E7009-CON; the screening that proposes X1 (`RWB-S8-E1062-APP`, `RWB-S8-E2029-APP`); the raising of the flag, the pause of the stage clock and the contact stop of X1 (RWB-S8-E7001-APP to RWB-S8-E7007-APP); the review of an override (`RWB-S8-E7008-APP`) and the breach path of a contact sent while a block is on (`RWB-S8-E7010-APP`); the case of record and its route states, which are rwb-case (P3); the contact points and the interaction ledger, which are rwb-source-data's (P1) by the default ruling; the DEV route set, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: links each complaint to the contact that caused it, which is how conduct is measured, because complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock (FSD S8 A1.3, A2.18.1). Deviations closed within the service level are measured on the decision log and the Workbench records against a target set with DL22, reviewed monthly (FSD S8 A2.18.1). What D-RCV-60 changes is who owns the case, the contact, the package, the record and the screen.

- **The record is this service's.** `deviation` is S8's only table in `rwb_deviation` (context pack, ownership rows owned by S8; TSD S8 T3.1), and the DEV route set of 22 rules over 9 states is the deviation stage's (TSD S8 T4); the match is written on that stage.
- **The link has no column.** No field of DF-CAS-036 to DF-CAS-045 carries a contact or a complaint reference (TSD S8 T3.1), and the FSD field catalog of A2.18.3.2 lists the same eight deviation fields. The result therefore lives in the decision record only, which is also what legacy AC1 asks for (GAP-3068; ASM-5212).
- **The contact stays with rwb-source-data.** The S8 row of the connection matrix names REST and events to P1 and nothing to EFS, the FSD names EFS as an integration point, and the interaction ledger is P1's by the default ruling, so the preceding contact arrives on P1's contract and never from an ACE table or a direct EFS call (GAP-3068; ASM-5213).
- **The package is read, not embedded.** The DEV set is governed in rwb-decision and DP-04 is not in this key's pattern set, so the version in force arrives on the package read and is recorded with the match (ASM-5214).
- **The case is not touched.** The match moves no deviation state and no case state: X1 is already open at `DEV_WITH_OWNER` with the complaint officer under R-DEV-02, and the resume of R-DEV-18 is the clearance step's (Business Rules and Routing Logic v4).
- **The officer's right is short.** The FSD names the Conduct and QA officer as the primary role and gives the case record right U, while TSD S8 T6.1 gives RW-CONDUCT R only; the match needs U to be recorded, so the permission table and the right of the operation are taken over the matrix row and the conflict is recorded (GAP-3068; ASM-5216).
- **The measure has no event.** The service publishes EV-06 `DeviationRaised` and EV-07 `DeviationCleared` only, and rwb-reporting listens to S8, so a match carried by neither event leaves the conduct measure on the decision-record ledger and not on a projected event (GAP-3068; ASM-5215).

No business value moves: the deviation code, the lists, the right, the package version and the match outcome are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S8-E7009-CON is published: the match branch of `PATCH /deviations/{deviationId}` with its optional complaint and contact references, the `Deviation`, `DeviationRequest` and `DeviationOutcome` elements, the consumed rows, the right, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contact read is published with its fake: the contact point of the case's party with its channel, its time and the interaction it belongs to. The operation name is Not specified in the source documents (GAP-3068; ASM-5213).
- The rwb-decision package read is published with its fake and answers the DEV package at its version in force, with R-DEV-01 to R-DEV-22 among its rules (GAP-3068; ASM-5214).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-08 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `deviation` exists in schema `rwb_deviation` from the DB story of this service, with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration, and writes no column of it.
- The legacy X1 path is in place: a complaint logged against the case raises X1 under R-UNI-04 and the deviation is assigned to the complaint officer under R-DEV-02, which the raise and screening stories own (FSD S8 A2.18.2; Business Rules and Routing Logic v4).
- The service runs as its own login on schema `rwb_deviation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_source_data` or an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7009-CON when its tests pass.

### 4. Flow

1. A complaint has been logged against the case and X1 is open at `DEV_WITH_OWNER` with the complaint officer, raised under R-UNI-04 and assigned under R-DEV-02 by the raise stories; this story reads that state only (FSD S8 A2.18.2; Business Rules and Routing Logic v4).
2. The conduct and QA officer opens SCR-08 Deviation queue through the gateway-bff composite route, one hop, and reads the open X1 deviation of the complaint (DP-19).
3. The officer picks the contact the complaint arose from and confirms the match. The screen sends the deviation reference, the complaint reference, the contact reference and the officer's identity; the operation declares no `Idempotency-Key` header (TSD S8 T-A.2).
4. `ComplaintMatchController` serves the match branch of `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1`, declares the case-record right U with the scope applied and validates the inputs (DP-13).
5. The service reads the deviation row in `rwb_deviation`: its reference, its case, its code, its from state and its handler. A deviation that is not an open X1 of that case is refused with 409 and nothing is written.
6. The service reads the preceding contact on the rwb-source-data contract: the contact point, its channel, its time and the interaction it belongs to. The ledger is P1's by the default ruling and the FSD's EFS is reached only through P1 (DP-18; ASM-5213).
7. The service reads the DEV package version in force on the rwb-decision contract and holds it for the record; no rule row of the 22 expresses the match (ASM-5214).
8. `ComplaintMatchEvaluator` binds the complaint to the contact: the deviation is an open X1 of that case, the contact belongs to the party of that case, and the contact precedes the complaint. The matching condition is a rule of the package in force and never a branch of the code; the condition itself is Not specified in the source documents (GAP-3068; ASM-5214).
9. `DeviationDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the deviation reference and code X1, the complaint reference, the contact reference, the package version in force, the match outcome and the matched-at time. A failed write stops the step with nothing changed (DP-03; AC1, AC2).
10. The answer returns the deviation element with its decision-record reference, and the officer sees the match on SCR-08, read back from this service (DP-19).
11. No column of `deviation` is written by the match, and no deviation state and no case state moves: the states `DEV_WITH_OWNER` and the resume of R-DEV-18 belong to the clearance step (GAP-3068; ASM-5212).
12. A repeat of the same match answers the record that exists and writes no second one, matched on the deviation reference and the complaint reference. The contact reference is a key: no phone number, address, identity number or contact value is copied into the record, the answer or a log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no match is recorded and the deviation stays where it was, with no record | MSG-P7-003 | AC2, TC-E7-009-02, TC-E7-009-04 |
| X2 | The role does not hold the case record right U | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E7-009-03 |
| X3 | The deviation is not an open X1 of that case, or the complaint reference is absent | 409 or 422 with nothing written; a match is not recorded on a deviation that is not the complaint's | MSG-GEN-001 | AC1, X7 |
| X4 | The preceding contact is not found on the rwb-source-data contract | 422 and nothing recorded; the match is refused and the deviation keeps its handler | MSG-GEN-001 | AC1, X7 |
| X5 | The rwb-source-data or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written; the caller sees 503 with the platform error envelope | None | AC1, X2 |
| X6 | The complaint has no preceding contact on the ledger at all | The match is refused and nothing is recorded; no source publishes the path that follows, so the deviation stays with its owner | Not specified in the source documents (GAP-3068; ASM-5213) | AC1 |
| X7 | A repeated request for the same deviation and complaint | One record and one answer; the repeat answers the record that exists and is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 and X2 are the legacy exception paths carried onto the slice (the legacy set also carries MSG-GEN-001 and MSG-S8-001, kept in section 14), X3 to X7 are the paths the target call types and the interactive trigger add, and X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7009-CON, the rwb-source-data and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the record's internal shape and the property names of the match references are this story's and the baseline's choice; the operation, the right, the message set, the screen and the two criteria are fixed |
| Valuable | Every complaint carries the contact it arose from, so conduct is measurable on the ledger with the rule version that was in force instead of on a manual cross-check |
| Estimable | One workflow step, one evaluator, one record write, one operation branch, two clients and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic open X1 deviation through the contract fakes, plus the access, not-a-complaint, contact-not-found and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Match a complaint to the preceding contact

  Background:
    Given case "RW-2026-000502" has the deviation "X1" open at state "DEV_WITH_OWNER" with the complaint officer as its handler
    Given the DEV rule package is in force at its version and carries R-DEV-01 to R-DEV-22
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Match a complaint to the preceding contact (legacy RWB-E7-009 AC1)
    Given the rwb-source-data contract mock returns the contact record of the preceding interaction
    Given the rwb-decision contract mock returns the rule version in force
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then links each complaint to the contact that caused it, which is how conduct is measured
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E7-009 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E7-009 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines, and those are the only additions. AC2 has no cross-service part and is copied with nothing added. The same outcome is the one FSD S8 AC-S8-018-01 records as written one epic ahead — "The data and rules it needs are in place / The user acts / The result is recorded with its rule version" — so the legacy line and the module line agree. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_deviation`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

No rule row of the 22-row DEV set expresses the complaint-to-contact match, and the universal set carries no row for it either (Business Rules and Routing Logic v4, Rules sheet). The two rows below are the X1 rows of the set this step reads and does **not** own; they are copied character for character, and they are the rows that put the deviation in the state the match is recorded on.

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-02 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | Workbench | None |
| R-DEV-09 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | Workbench | None |

Their owner and systems columns name a business role and systems, not services: "Workbench" is the case of rwb-case and this service's own record read through the composite route, and "Case owner" and "Complaint officer" are read as the roles the permission table gives right U on the case record (GAP-3068; ASM-5216, ASM-5208). R-UNI-04, the universal row that raises X1 when a complaint is logged, is the trigger's rule and belongs to the raise story of the module.

| ID | Rule | Source |
|---|---|---|
| BR1 | The match is a step of the deviation stage: it runs in `DeviationWorkflow` on `rwb-deviation`, writes no column of `deviation` and moves no deviation state | TSD S8 T3.1, T4; context pack ownership rows (table and workflow); FSD S8 A2.18.2 |
| BR2 | The result is recorded before anything else happens, with the package version in force, the complaint reference and the contact reference; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | Only an open X1 deviation of that case is matched, and the contact must be the case party's own: any other deviation code, any other case and any other party is refused | Business Rules and Routing Logic v4 row R-DEV-02; FSD S8 A2.18.2 |
| BR4 | The contact is read from rwb-source-data and never from an ACE table, a `v_ace_*` view or EFS directly; the interaction ledger is P1's by the default ruling | DP-05 as a prohibition; DP-18; context pack connection matrix row S8 (REST and events to P1) |
| BR5 | No cross-schema join and no foreign key leaves `rwb_deviation`; `case_id` and the contact reference are identifiers of another service's fact | DP-01; TSD S8 T3.3 |
| BR6 | The package version in force is read from rwb-decision and recorded with the match; no rule row of the DEV set expresses the match, so no rule ID is recorded as the match's own | ASM-5214; TSD S8 T4 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the deviation code, the lists, the right, the match outcome and the package version | FSD S8 BR-S8-018; legacy Guardrails |
| BR8 | The same request twice writes one record and sends one answer; the operation declares no `Idempotency-Key`, so the repeat is matched on the deviation and complaint references | TSD S8 T-A.2; ASM-5212 |
| BR9 | No person name, address, contact value or identity number enters `rwb_deviation`, the decision record, a log or a workflow input; the contact reference is a key and not a contact value | Template and Rules §R7.2 (s17); TSD S8 T6.2 |

### 9. State transitions

The deviation state and the case route state are not changed by this story: X1 is already open at `DEV_WITH_OWNER`, and the resume of R-DEV-18 is the clearance step's. What this story owns is the step and the record.

| From (deviation state, rwb-deviation) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `DEV_WITH_OWNER` | A complaint matched to its preceding contact | The record is written | `DEV_WITH_OWNER`, unchanged | none; the match moves no deviation (ASM-5212) |
| `DEV_WITH_OWNER` | `DEVIATION_RESOLVED` | `deviation_code in (X1,X7)` | `DEV_RESOLVED` | rwb-deviation, on R-DEV-09, by RWB-S8-E7001-APP |
| `DEV_RESOLVED` | `CLOCK_RESUMED` | Any | `RESUMED` | rwb-deviation, on R-DEV-18 |
| Any state but `DEV_WITH_OWNER` | A complaint matched to its preceding contact | The deviation is not an open X1 | Unchanged | none; 409 (X3) |
| `DEV_WITH_OWNER` | A complaint matched to its preceding contact | The complaint has no preceding contact | Unchanged | none; the match is refused (X6) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A match request for an open X1 deviation | The package in force is read | Evaluating |
| Evaluating | The match binds | The deviation is an open X1 and the contact belongs to the case party | Recording |
| Evaluating | The match does not bind | The code, the case or the party is not the rule's | Waiting, nothing changed |
| Recording | The record is written and the answer sent | The transaction commits | Waiting for the next request |
| Recording | The record write fails | X1 | Waiting, nothing changed |

The states `DEV_WITH_OWNER`, `DEV_RESOLVED` and `RESUMED` are those of the DEV machine of TSD S8 T4 and the States sheet of the Business Rules and Routing Logic v4 (9 states over 22 rules); this step writes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CONDUCT, conduct and QA officer | Case record R in TSD S8 T6.1: the primary role of FSD S8 A2.18.3.3, matching a complaint to its preceding contact through the operation's right U (ASM-5216) |
| RW-COMPLAIN, complaint officer | Case record RU: the also-uses role of FSD S8 A2.18.3.3, matching and reading the record of an X1 it holds |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF | Case record U: the roles the legacy permission table names with right U |
| RW-DEBTSALE, RW-GUARANT, SY-CASEWF, SY-DATALOAD | Case record U: the four further identities TSD S8 T6.1 gives U, which are the legacy table's "and 4 more" (ASM-5208) |
| RW-TEAMMGR, RW-LEGAL, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE and the other PT-* and SY-* identities | Case record R: read only, in scope, and refused the match |
| rwb-deviation service identity | Evaluates the match, writes the record and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S8 T6.1 and nothing wider. The right this story needs is U: the legacy permission table gives right U on the case record to the eight roles it names plus four more, and TSD S8 T-A.2 declares right U on both API-S8-001 and API-S8-002. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the deviation reference the operation takes as `deviationId`; recorded in the decision record |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the case of the complaint; recorded in the decision record |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, the code the match requires to be X1 |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read, the time the complaint's flag was raised |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Read, the source of the flag |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read, the state in force during the deviation |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Read, the handler named by R-DEV-02; not changed by the match |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Read, the stop the match does not lift |
| DF-CAS-044, DF-CAS-045 | deviation (S8, `rwb_deviation`) | cleared_at, outcome | Not written here: the clearance step writes them (R-DEV-09) |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Not written: the match writes no column of the table (BR1) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before anything else: the complaint reference, the contact reference, the package version and the match outcome |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the stage clock is paused by the raise step and resumed by the clearance step (R-DEV-01, R-DEV-18) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package version arrives on the package read |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case reference arrives on the deviation row and the case itself on the composite route |
| `complaintReference`, `contactReference` | the match inputs | Read as request inputs and recorded in the decision record; neither has a column in `deviation` (TSD S8 T3.1), a field ID or a value format in any source: Not specified in the source documents (GAP-3068; ASM-5212) |
| `matchOutcome` | the result of the match | Write, the outcome the record carries; its value set is Not specified in the source documents (GAP-3068; ASM-5215) |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary, and the timer, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, this story writes none of its columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_deviation` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, codes, dates, list values, a package version, a match outcome and two references. The contact reference is a key: no phone number, address, e-mail, identity number or contact name is read into the record, the answer, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). This story supplies the match branch of the deviation-outcome operation, whose shape RWB-S8-E7009-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in with the outcome, the note and the optional match references, `Deviation` out with the decision-record reference and the state `DEV_WITH_OWNER` | Case record, right U, scope applied | Not applicable |
| POST | `/cases/{caseId}/deviations` (API-S8-001) | `DeviationRequest` in, `Deviation` out; declared by the same baseline and built by the raise stories of the module, not here | Case record, right U, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not on the case, 409 for a deviation that is not an open X1, 422 with MSG-GEN-001 for a missing reference or a contact that is not the party's, and 503 when the library or a consumed contract does not answer. TSD S8 T-A.1 publishes both operations with their requests, answers and the error set 401, 403, 404, 409, 422 and 503, so the operations themselves are published and need no placeholder; the match properties, the value format of the two references and the match outcome set are what no source gives (§11; GAP-3068; ASM-5212).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The contact read (operation name Not specified in the source documents (GAP-3068; ASM-5213)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The contact point of the case party with its channel, its time and the interaction it belongs to; the interaction ledger is P1's by the default ruling; read only, faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3068; ASM-5214)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV package at its version, with R-DEV-01 to R-DEV-22 over its 9 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Both rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3068; ASM-5213, ASM-5214).

#### 12.3 Events published

None. The service publishes on `rwb.deviation.events.v1` and its event set carries EV-06 `DeviationRaised` (`caseId`, `deviationCode`, `raisedBy`, consumed by Timers and Communications for the contact stop) and EV-07 `DeviationCleared` (`caseId`, `deviationCode`, `outcome`, consumed by Timers and Communications), and both belong to the raise and clearance steps of the stage (Event and Messaging Design v5; TSD S8 T5.3). A match changes no deviation state and lifts no stop, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry (GAP-3068; ASM-5215).

#### 12.4 Events consumed

None. The case router of rwb-case reaches this service through the deviation stage, and the service listens to rwb-case events on the connection matrix's column P3 (context pack connection matrix, row S8: events from P3, REST and events to P1, Temporal and events to P10); none of them belongs to the match, whose trigger is the officer's confirmation on SCR-08. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The FSD declares no background event for the feature (FSD S8 A2.18.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, can start at any time on a case, continues-as-new with the case stage | `rwb-deviation` in namespace `rwb-recovery` | Input: the case reference, the deviation reference and the package in force; signals: the match request and the clearance; outcome for the parent: the case move |
| `recordComplaintMatch` | Activity, the one match step of the stage | `rwb-deviation` | The deviation reference, the complaint reference, the contact reference and the package version in; the record reference and the match outcome out, with the record written before the answer |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the step runs from the officer's confirmation, and the stage itself can start at any time and pauses the stage clock (context pack, Temporal and Drools slide 13).

#### 12.6 Schedules

None. The match is an officer-driven step and owns no Temporal Schedule, no Quartz row and no shared job table. The service owns no job in the context pack's ownership rows (Jobs: None), and nothing of the pause, the escalation timer of R-DEV-20 or the screening run is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 of a case; this story reads the row of the complaint and writes none of its columns |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the match (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the raise operation, provided by the same baseline; the match declares none (§12.1) |
| outbox_event | PLT library, created in `rwb_deviation` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data contact fake | The contact record of the preceding interaction for the case party, and a case with no such contact | AC1, X4, X6 |
| rwb-decision rule-package fake | The DEV package at its version in force, with R-DEV-01 to R-DEV-22 | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-08 answer for the deviation of `RW-2026-000502`, before and after the match | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the contact read and the package read carry the placeholder until their owners confirm them (GAP-3068; ASM-5213, ASM-5214).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The match branch of `/api/recovery/deviation/v1/deviations/{deviationId}` and the raise operation of the same base; the contact read and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-06 and EV-07 belong to the raise and clearance steps; no event of this step (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `DeviationWorkflow` and `recordComplaintMatch` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `conduct`; front end `src/modules/recovery/deviation/DeviationQueue.tsx`, the fragment SCR-08 embeds, read only for this story's state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the answer commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the deviation-outcome operation its home. DP-19 is how SCR-08 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-05 (the ACE and contact read), DP-09 (the outbox and inbox library) and DP-18 (the ledger) are real dependencies of the step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3068; ASM-5213, ASM-5214, ASM-5215).

**Dependencies the tables add and the plan does not hold.** The two consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` match branch | Workflow | Receives the match request as a signal on the deviation stage, reads the package in force and reports the outcome to the parent |
| `recordComplaintMatch` | Activity | Reads the deviation and the contact, evaluates the match, writes the record and answers |
| `ComplaintMatchEvaluator` | Service | Binds the complaint to the contact over the package in force: the code test, the case test, the party test and the precedence test |
| `DeviationDecisionRecordWriter` | Library adapter | Writes the record with the package version before anything else, hash-linked; refuses the step when the write fails |
| `ComplaintMatchController` | Controller | The match branch of the deviation-outcome operation, the capability area and right U, the scope and the problem mapping |
| `SourceDataContactClient` | Client | The contact read of rwb-source-data, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The DEV package read of rwb-decision at its version in force |
| `DeviationQueue` | React component | Shows the open X1 deviation and the recorded match on SCR-08, read only |

**Database and migrations.** No Flyway file. The `deviation` table arrives with the DB story of this service, and the record is a library object created in `rwb_deviation` by the library's migration (DP-03). No column is added for the complaint reference, the contact reference or the match outcome: none has a source (ASM-5212).

**Configuration and reference data.**

- The match condition, the deviation code X1, the from state `DEV_WITH_OWNER` and the package version: rule rows and reference data with their version, never written in code (ASM-5214).
- The match outcome set and the value format of the two references: placeholders until the business lead confirms them (ASM-5212, ASM-5215).
- The capability area "Case record" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the match has no timer of its own.

**Build steps**

1. The match branch of `DeviationWorkflow` and its input record, registered on `rwb-deviation` as the deviation stage, with the officer's confirmation as its signal.
2. `SourceDataContactClient` against its fake, with the 2 s budget, the breaker and the no-contact path (AC1, X4, X6).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `ComplaintMatchEvaluator` over the package, with the code, case, party and precedence tests and the no-fire path (AC1, X3).
5. `DeviationDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
6. `ComplaintMatchController` with the match branch, right U, the scope and the problem mapping of the declared errors, and `DeviationQueue` on SCR-08 through the composite route fake (AC1, X2, X7).
7. The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_source_data` or any other schema, and no write to a column of `deviation` (X8, BR1, BR5).

**Feature flag.** `rwb.deviation.complaint-match-v1`, a flag of the platform library; off means the operation answers 503 with no write and SCR-08 hides the match action, and the raise, screening and clearance stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic open X1 deviation in SIT, the match is recorded with the package version in force, a deviation that is not the complaint's and a contact that is not the party's are refused, a repeated request writes once, a forced record failure changes nothing, no `recovery_case` row, no `deviation` column write and no `v_ace_*` read exists in the build, and SCR-08 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of RWB-E7-009: the deviation was raised and the case is with its handler. Raised by the raise story of the module, not by this step | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required element is absent or invalid: the complaint reference, the contact reference, or a contact that is not the party's (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the case record right U calls the match (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the match is answered (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S8-001 is kept because the legacy table of RWB-E7-009 lists it: it is the message the officer sees on the deviation this step matches, and it is not raised here.

### 15. Screens and states

SCR-08 Deviation queue is served through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation, its handler and the recorded match, and rwb-case for the case and its route state; this story fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-08 "Loading; list" and SCR-06 Raise deviation "Form; saved". This story produces the match from the list state of SCR-08: a matched deviation shows the contact it is bound to and the record reference, and **no column of the table changes**. SCR-06 is the raise form and belongs to the raise stories (RWB-S8-E7001-APP to RWB-S8-E7007-APP). Neither screen is described anywhere as a matching screen, so the match action's place on SCR-08 is Not specified in the source documents (GAP-3068; ASM-5212). The refusal, not-a-complaint, no-contact and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-009-01 | AC1 | Component | The open X1 deviation of `RW-2026-000502` on the fakes; the contact, the package version, the record and the state asserted |
| TC-E7-009-02 | AC2 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E7-009-03 | Access | Component | A role without the case record right U; 403 with MSG-P4-002 and no read |
| TC-E7-009-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; the deviation is unchanged and no record exists |

The four legacy cases are those of RWB-E7-009 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the match condition, the deviation code, the states, the right, the match outcome and the package version stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_deviation`, in a workflow input or in a log: identifiers, a code, dates, a reference and a package version only, and every fixture is synthetic. The contact reference is a key and never a contact value.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the contact arrives on rwb-source-data's contract (BR4).
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here.
- The deviation row is read, not written: no column of `deviation` is set by a match, and no deviation state moves (BR1).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `recovery_log` write.
- The record is written before the answer; a build that answers outside the record's transaction fails the review (DP-03).
- EFS is never called directly: the FSD's integration point is reached through rwb-source-data, and a build that adds an EFS client fails the boundary test (BR4).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-DVF-09 | The requirement this feature serves is Not specified in the source documents (GAP-3068; ASM-5217): TSD S8 T8 maps every REQ-DVH and REQ-S8 row to FEAT-DVH-01, FEAT-DVF-01 or a placeholder | The trace rests on the legacy key, the feature row and AC1 | TC-E7-009-01 |
| ADR-013 | 19 services inside ACE | rwb-deviation as the owner of the deviation stage | TC-E7-009-01 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-E7-009-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-E7-009-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the match is answered | TC-E7-009-02, TC-E7-009-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-009, disposition Split (rework); feature FEAT-DVF-09 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged from the plan; EP07 is wave 4 and the service's Arch v5 wave is 2, so the W-MAP wave is not earlier and no conflict is raised (ASM-5209) |
| Source text | Legacy RWB-E7-009; FSD S8 Deviation handling v3 A1.2, A2.18, A2.18.3.1, A2.18.3.2, A2.18.3.3 and A2.18.4; TSD S8 Deviation handling v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DEV-02 and R-DEV-09; Event and Messaging Design v5 events EV-06 and EV-07 |
| Test cases | TC-E7-009-01 to TC-E7-009-04 |
| Feature and screens | FEAT-DVF-09, SCR-08 Deviation queue (SCR-06 belongs to the raise stories) |
| Rules | R-DEV-02 and R-DEV-09 read as the X1 rows of the DEV set; no row expresses the match (ASM-5214) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the two operations, the `Deviation`, `DeviationRequest` and `DeviationOutcome` elements, the match properties, the consumed rows, the error set and the fakes: RWB-S8-E7009-CON.
- The screening that proposes X1 and the L1 agent: `RWB-S8-E1062-APP`, `RWB-S8-E2029-APP` and the other E1 and E2 stories of the module.
- The raising of the flag, the pause of the stage clock, the prescription clock and the contact stop of X1: RWB-S8-E7001-APP to RWB-S8-E7007-APP.
- The clearance of the deviation, the outcome of R-DEV-09 to R-DEV-22 and the resume of R-DEV-18: the clearance stories of the module.
- The override review: RWB-S8-E7008-APP. The breach path of a contact sent while a block is on: RWB-S8-E7010-APP.
- Every column of `deviation` and every deviation state: the match writes none of them and moves none of them (BR1).
- The requirement row of FEAT-DVF-09: no source publishes one, and the trace waits for the E7 BRD and the PRD (GAP-3068; ASM-5217).
- An event that carries the match to rwb-reporting: none is published by the service, so the conduct measure rests on the decision-record ledger (ASM-5215).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3). The contact points, the interaction ledger and EFS: rwb-source-data (P1). The DEV package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
