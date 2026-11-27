# RWB-P6-E2042-APP Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P6-E2042-APP-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P6-R |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2042-CON |
| Contract version | v1 (path segment /api/recovery/decision/v1; no further contract version is stated in the source documents) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-CWC-013, REQ-CWC-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: secondary slice of RWB-E2-042 for rwb-comms. The three package codes, their workbook, the load checks, the 50-scenario gate, four-eyes approval, effective dating, one-call rollback and the registry are rwb-decision's (`RWB-P7-E2042-APP`); the workbook authoring, the write-once Blob store, the model cache and the build gate are rwb-case's (`RWB-P3-E2042-APP`); the local copy, the checksum, the KieBase registry and the evaluation inside this service are `RWB-P6-E1073-APP`. This story carries what is left on the notice side: the Epic 2 versions and their counts as this service resolves them, the route-set fields of a rule row, the package code, version and checksum on the notice decision, and the proof that a load, an approval, a promotion at 00:01 or a rollback raises no notice, no message and no dispatch. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2042-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 35 cross-document, 9 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF) who owns a demand or recall notice, and the rwb-comms service identity that generates it**, I want **every notice decision that reads one of the three Epic 2 packages to carry the package code, the version label and the checksum that decided it, the route-set fields of a rule row to be copied verbatim from the registry by rule ID and version, and the whole notice path — the notice row, the template, the merge-field catalog, the outbox, the ACE notification path, the dispatch item and the WIN file — to stay untouched by a load, an approval, a promotion at 00:01 or a one-call rollback of RESTRUCTURE, PAYMENT_MATCH or BOOKING_MATCH**, so that **a rule change reaches the desk as tested, approved, dated data and never as correspondence to a customer, and any notice can still name the version that decided it months later**.

Inside `rwb-comms` this is the notice-side slice of legacy RWB-E2-042. The service facts are schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with `rwb.comms.NoticeGenerated.v1` (EV-13), `rwb.comms.NoticeDispatched.v1` (EV-14) and `rwb.comms.NoticeDelivered.v1` (EV-15), queue `rwb-comms` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.comms`, and the shared topic `rwb.decision-record.v1` on which the library writes the record of a notice (DP-03). The slice:

- The three versions of 16 November 2026 — RESTRUCTURE "RES-2026.12" with 38 rows and 62 scenarios, PAYMENT_MATCH "PMT-2026.12" with 3 rows and 58 scenarios, BOOKING_MATCH "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-01 and each at or above `rules.testcases.min` = 50 — resolved only through the operations of RWB-P3-E2042-CON.
- The route-set fields `action_text` (DF-REF-008), `owner_role` (DF-REF-010) and `timer_spec` (DF-REF-011) of R-RES-04, copied into the next action, the owner and the due date of the notice instead of compiled into code.
- The seed, the load, the approve, the dry run, the promotion and the rollback: read as states and counts, never performed here.
- The assertion the set relies on: a governance action on the three packages writes no `notice`, no `template` and no `merge_field` row, puts nothing on `rwb.comms.events.v1`, sends nothing through the ACE notification path, adds no dispatch item, raises no task, and leaves the 16:00 run of JOB-10 (DP-10) with the notices it had before.
- The negative schema assertion: `payment_match_rule` and DF-REF-261 to DF-REF-273 exist nowhere in `rwb_comms`, and no rule row, DRL or test of this service names them.

Not this story, and stated again in section 6 and section 19:

- The local copy, the model fetch, the SHA-256 verification, the KieBase registry of 20 versions, the scenario re-run, the atomic swap, the `EvaluateRules` and `RecordAndApply` activities and the consumption of `rwb.decision.RulePackageInForce.v1` are **RWB-P6-E1073-APP**. This story uses them as published and adds no loader, no cache and no activity.
- The workbook, the Rows and Tests tabs, the write-once Blob object, the model cache and `RuleScenarioBuildGate` are **RWB-P3-E2042-APP**; the package rows, the checks, the four-eyes approval, the dry run, the promotion and the rollback are **RWB-P7-E2042-APP**; the rights, roles and screens are **RWB-P4-E2042-APP**; the cross-service proof of a load, an approval, a promotion, a swap and a record is **RWB-ITG-E2042-ITG**. Every criterion of this story is proved against this service alone or through a contract fake.
- The notice generation, the dispatch loop and the proof-of-delivery capture are `RWB-P6-E1052-APP`, `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`; the template lifecycle is `RWB-P6-AD017-APP`. This story changes none of their operations.

Which of the three packages a notice of this service actually reads is named in no source, and neither is the package code that `RWB-P6-E1073-APP` assigns to rwb-comms: the three Epic 2 packages serve the case engines of RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035, and the legacy story attaches no notice to any of them. The resolution is carried as GAP-2395 with ASM-3979 and is not settled silently here.

### 2. Business rationale

A rule change is a data change: authored in a workbook, compiled, tested against a scenario set, approved by a second person, dated and rolled back in one call (D-RCV-36 T3 to T6). The control exists because recovery decisions are taken under a procedure a supervisor has read, and audit found the procedure not followed because the rules were not in the system (CTL-08). Nothing in that control is safe if changing a rule also contacts a customer: a demand, recall or statutory notice starts a legal clock from the date of delivery, and a notice raised by a release cannot be unsent, unseen or re-dated.

That is the subject of this story. The legacy key puts three packages in one governance path and retires `payment_match_rule`; on this side the requirement is the one the integration story names as the harness assertion — *the notice path stays silent* (RWB-ITG-E2042-ITG, section 2) — and the one the registry story defers here: *the notices a rule change must not raise are RWB-P6-E2042-APP* (RWB-P7-E2042-APP, section 19). It meets REQ-CWC-013 and REQ-CWC-014 from the consumer side.

The measure is shaped like the notice path: three versions resolve by package code, rule ID and label with no value held in this service's code; the three route-set fields appear verbatim on the notice; every notice decision record names one package version and one checksum; and a load, an approval, a promotion and a rollback together add zero notice rows, zero template rows, zero outbox rows on `rwb.comms.events.v1`, zero dispatch items, zero tasks and zero messages to NSS or LINE OA. The 16:00 run of JOB-10 on the promotion date carries exactly the notices it carried before, and `rwb_comms` holds no `payment_match_rule` and no column of DF-REF-261 to DF-REF-273.

The realignment changes the mechanism, not the business control:

1. The single recovery schema becomes `rwb_comms` for the notice facts and the lapse of the decision record, with `rwb_decision` read only through its contract (DP-01, DP-15).
2. The monolith's in-process rule read becomes the published contract of RWB-P3-E2042-CON: the catalog read of a rule row, the model read with its checksum, the version list, the parameters and the reference data (DP-04, DP-06, DP-07).
3. The evaluation itself stays inside the service, in the embedded Drools kit on task queue `rwb-comms` (DP-04, DP-10), and the mechanism is `RWB-P6-E1073-APP`'s; this story pins its result.
4. The version is no longer read from a properties file: it is a resolved value of the contract, recorded on the local decision record written through the library on `rwb.decision-record.v1` (DP-03).
5. The API base becomes `/api/recovery/comms/v1` and the notice read keeps its shape (DP-13, DP-19); this story adds no path.
6. The event names of the service and of the shared record topic follow the naming rule (DP-14), and no new event is created for a rule change — the absence of that event is the requirement.
7. `payment_match_rule` is never created in `rwb_comms`, and the thirteen retired field IDs are referenced by no row, DRL or test.

The business outcome is the one a supervisor can check on a notice: the letter that went out names the version that decided it, and no letter went out because a version changed.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2042-CON | The published contract of the legacy key: the workbook Rows and Tests schema, the Blob object naming and metadata, the five consumed rwb-decision operations (the model read, the catalog read, the version list, the load and the approve), the `RulePackageInForce` consumption contract, the `EvaluateRules` activity contract with `RuleResult` and `NoPackageInForce`, the cache and swap rules, and the rwb-decision and rwb-access fakes |
| RWB-P6-E1073-APP | The local copy of the package this service is assigned, the checksum verifier, the KieBase registry of at most `drools.kiebase.cache.max` (20) versions, the two activities and the version stamped on every answer. Used as published; this story builds none of it |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one hash-chained record per notice decision, written in the same transaction as the notice row and the outbox row |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): compile, checksum, first-match semantics and the `NoPackageInForce` outcome |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): `NoticeDispatchWorkflow` and its activities run on queue `rwb-comms` |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the rwb-case parameters contract (DP-06): `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the rwb-case reference-data contract (DP-07): LOV-NOTICE with DEMAND as a statutory notice, LOV-DELIVERY, LOV-CHANNEL and the notice-state vocabulary |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic, event and queue names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and conventions (DP-15): the `rwb_comms` baseline. This story adds no migration |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the notice panel of a case reads this service through it; this story serves no screen |
| RWB-P4-E2042-APP, RWB-P4-E1037-CON | The rights and the authorise answer behind the notice operations of section 12.2. This story declares the right and names the roles; it holds no role row |
| RWB-P7-E2042-APP, RWB-P3-E2042-APP | The registry, the checks, the approval, the promotion and the workbook. Read here as states, labels and counts; nothing of the registry is written from this service |

The DP-added H and C dependencies of section 13 — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and C RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON — are not repeated in the metadata rows, which name Depends on (build) None and Contract dependencies RWB-P3-E2042-CON. They are wave-0 platform contracts and published contracts built against as fakes, so none blocks this story and Ready to start stays Day 1 (GAP-2398; ASM-3982).

Business preconditions carried from RWB-E2-042, unchanged:

- The version labels and their counts of 16 November 2026: "RES-2026.12" with 38 rows and 62 scenarios, "PMT-2026.12" with 3 rows and 58 scenarios, "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-15 (the valid-from date is the legacy assumption and is copied unchanged).
- The PAYMENT_MATCH rows are EXACT at priority 1, WINDOW at 2 and PARTIAL at 3 under rule R-RES-26; the RESTRUCTURE row set includes R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31 and R-LIT-02, and R-RES-04 carries action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days".
- The business date of the run is 2026-12-10, the loader is "U-41" holding RW-COE and the approver "U-51" holding RW-RISK, and they are two different people. The rights are Rules and parameters C for RW-COE, A for RW-RISK and R for RW-AUDIT.
- Open notices keep the package version they were decided under (R-UNI-38).
- Synthetic data only: package codes, labels, rule IDs, row orders, counts and payment codes of the legacy story. No real account, customer, party or payment appears in a test.

### 4. Flow

1. A capability of rwb-comms that generates a notice (`RWB-P6-E1052-APP`, `RWB-P6-E2021-APP`) calls `EvaluateRules` on queue `rwb-comms` with the package code, the facts of the case and the business date; Drools is never called in workflow code (DP-04, DP-10).
2. `NoticeRuleVersionResolver` resolves the package code the notice is assigned, the version in force for the business date and that version's checksum through the version list of RWB-P3-E2042-CON; no label, checksum or threshold is read from code or configuration (DP-04, DP-06).
3. The answer is `RuleResult` from `RWB-P6-E1073-APP`: package code, version label, rule ID and outputs. When no version is in force the answer is `NoPackageInForce`, which is non-retryable and creates no notice (X1). The caller is refused with a message that is Not specified in the source documents (GAP-2399); no notice row in any state is created, no hold reason of this service is added and nothing is dispatched.
4. Only for a notice decided by a rule that carries a route set, `RouteSetFieldReader` reads `action_text` (DF-REF-008), `owner_role` (DF-REF-010) and `timer_spec` (DF-REF-011) through the catalog read by rule ID and version and copies the three values verbatim onto the notice as its next action, owner and due date; the case next action stays with RWB-E2-035 and is not set here. A blank field refuses the read and no notice is created.
5. `RecordAndApply` writes, in one transaction in `rwb_comms`: the `notice` row, the local decision record naming the package code, version label, checksum and rule ID, and the outbox row of `rwb.comms.NoticeGenerated.v1` (DP-01, DP-03, DP-09). The library publishes `DecisionRecorded` on `rwb.decision-record.v1`.
6. Elsewhere, and at no request of this service, a version of RESTRUCTURE, PAYMENT_MATCH or BOOKING_MATCH is loaded, approved and promoted at 00:01 on its valid-from date, or rolled back in one call. On the notice path that is an observation and nothing else: no controller, listener, workflow, Schedule or activity of `rwb-comms` reacts to a package state, a load, an approval, a promotion or a rollback.
7. A new or restored version reaches this service through the local copy of `RWB-P6-E1073-APP`; the next notice decided after the swap names the new version, and a notice already decided keeps the version on its record (R-UNI-38). No `notice`, `template` or `merge_field` row changes because a version moved.
8. The 16:00 dispatch run of JOB-10 pins the version it started with for the whole run and writes the WIN file of INT-14 through the hand-off of `RWB-P6-E1007-APP`; a version promoted at 00:01 changes neither the file nor its contents.
9. Internal audit reads the decision records of the notices of a case and proves which version decided each one, without reading a registry row and without touching a notice.
10. Nothing in this flow sends an SMS or a LINE message: the conduct check, the contact stop and the send of `RWB-P6-E2021-APP` are untouched by a rule change, and steps 6 to 8 create no dispatch item, task or notification.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The version list answers no version in force for the package a notice is assigned | `RuleResult` is `NoPackageInForce`, the notice is not created, nothing is written and nothing is dispatched; the caller sees the message and no notice exists | MSG-GEN-006 | AC5 |
| X2 | A route-set row of the version carries an empty `action_text`, `owner_role` or `timer_spec` | The catalog read is refused, the check names the rule ID and the column, and the notice is not created | MSG-P3-027 | AC5 |
| X3 | The catalog read, the model read or the version list answers 503 or times out beyond the 2 s client budget | The notice is not created; the previous version stays in force; the failure is in the local run record and the call is retried once with jitter on a GET | MSG-GEN-006 | AC5 |
| X4 | A governance action on any of the three packages runs (load, approve, promote, roll back) | No notice, no message, no dispatch item, no task and no event of this service; the notice rows and the dispatch file are what they were | None | AC2, AC3, AC4 |
| X5 | A notice was decided under a version that is later rolled back | The decision record keeps the rolled-back version; no notice row is rewritten and no second notice is generated | None | AC5 |
| X6 | The notice path would need to learn of a change from `rwb.decision.events.v1` | It does not: no listener of this service subscribes for the notice path, so a promotion cannot raise a notice; the architecture test fails the build if one is added | None | AC4 |
| X7 | The local decision record of a notice cannot be written | Nothing is applied: no notice row and no outbox row; an incident is raised under R-UNI-39 | MSG-P7-003 | AC5 |
| X8 | A caller without the right asks for a notice or asks for a rule version of this service | Refused at the edge and by the guard of the P4 story; nothing is read or written | MSG-P4-002 | AC1 |
| X9 | A migration of `rwb_comms` creates `payment_match_rule` or a column of DF-REF-261 to DF-REF-273 | The service's schema check fails the build before the artefact is published | None | AC6 |

A refused decision leaves every row exactly as it was before the call, and the notice path has no compensating action: a notice is either created with its version and its record, or it does not exist. The state a request rests in when no version is in force is named by no source; the refusal of X1 is the reading carried as GAP-2399 with ASM-3983, and no hold reason of this service is invented for it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2042-CON, the platform contracts of its DP table and the local copy of `RWB-P6-E1073-APP`; no registry operation, no loader and no cache is implemented here |
| Negotiable | The package assignment, the version labels, the row and scenario counts, the route-set values and the message texts are data or registry rows; the silence of the notice path, the pinning of the version and the absence of the retired table are fixed |
| Valuable | A rule change cannot reach a customer, and every notice still names the approved version that decided it |
| Estimable | One version resolver, one catalog reader, one dispatch pin, one architecture test, one schema check and one probe of the notice path |
| Small | Fits one sprint with its tests. It builds no workbook, no loader, no cache, no registry operation, no screen and no event |
| Testable | Each criterion is a component, contract or end-to-end test on this service with fixed fixtures and a recorded result; the cross-service journey itself is RWB-ITG-E2042-ITG's |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages on the rwb-comms notice path

  Background:
    Given the rwb-case parameters contract mock returns rules.testcases.min 50 and drools.kiebase.cache.max 20
    Given the rwb-case reference-data contract mock returns LOV-NOTICE with DEMAND a statutory notice, LOV-DELIVERY and the notice-state vocabulary
    Given the business date is 2026-12-10 and the rwb_comms schema is migrated with the rwb-comms Flyway sequence
    Given case "RC-2026-000321" holds notice "N-0101" of type DEMAND from template "DEMAND-SSME" "TH" version 1 in state "Approved"

  Scenario: AC1 The three Epic 2 versions resolve by package code, rule ID and version, and no package value is held in code (new, D-RCV-60)
    Given the rwb-decision contract mock returns the versions in force RESTRUCTURE "RES-2026.12" with 38 rows and 62 scenarios, PAYMENT_MATCH "PMT-2026.12" with 3 rows and 58 scenarios and BOOKING_MATCH "BKG-2026.12" with 21 rows and 54 scenarios, all valid from 2026-12-01
    When rwb-comms resolves rule "R-RES-26" of package PAYMENT_MATCH for 2026-12-15
    Then the answer names package code "PAYMENT_MATCH", version label "PMT-2026.12", its checksum and the row of "R-RES-26"
    Then each version's scenario count is at or above rules.testcases.min 50 and is read through the parameters contract
    Then no package code, version label, row, cell, threshold, match type, tolerance or window is held in the code or the configuration of this service
    Then the read writes no notice, template or merge_field row and publishes no event
    Then a caller without the notice read right is refused the same read with MSG-P4-002

  Scenario: AC2 A load, an approval, a promotion and a rollback of the three packages write no notice row, no template row and no merge-field row (new, D-RCV-60)
    Given rwb-comms holds notice "N-0101" in state "Approved", template "DEMAND-SSME" "TH" version 1 in state "Approved" with its merge codes, and the merge_field rows of catalog version in force
    When RESTRUCTURE "RES-2026.13" is loaded, approved, promoted at 00:01 on 2026-12-15 and rolled back in one call
    Then rwb_comms holds the same notice row, the same template row and the same merge_field rows as before, with no new row and no changed column
    Then the state of notice "N-0101" and of template "DEMAND-SSME" "TH" version 1 is unchanged
    Then no task is raised to RW-LITOFF, RW-ENFORCE or any other queue because of the four actions
    Then no rwb.comms.NoticeGenerated.v1, rwb.comms.NoticeDispatched.v1 or rwb.comms.NoticeDelivered.v1 row is written to the outbox
    Then the same holds for PAYMENT_MATCH and BOOKING_MATCH

  Scenario: AC3 A rule change sends nothing to a customer through any channel (new, D-RCV-60)
    Given notice "N-0101" is "Approved" and the party "P-0077" holds verified MOBILE and LINE contact points with consent GIVEN
    When the four governance actions of AC2 run, and afterwards a dispatch run of NoticeDispatchWorkflow starts on 2026-12-15
    Then the ACE notification path receives no SMS and no LINE message with any reason of this service
    Then no dispatch item is created and no WIN file line is added beyond the notices of the business date
    Then no outbound item carries a package code, a version label or a checksum
    Then the conduct check and the contact stop of the notice path are unchanged and are not run because of a rule change

  Scenario: AC4 The 16:00 dispatch run carries the notices it had before the change and pins one version for the run (new, D-RCV-60)
    Given the dispatch run of 2026-12-15 starts at 16:00 with version "RES-2026.12" and notice "N-0101" among the notices of the business date
    When version "RES-2026.13" was promoted at 00:01 on 2026-12-15 and a second notice "N-0102" is generated at 14:00
    Then the file of the run carries notice "N-0101" once, as it stood, and notice "N-0102" once
    Then the run names "RES-2026.12" for "N-0101" and "RES-2026.13" for "N-0102" on their decision records
    Then no listener, controller, workflow, Schedule or activity of rwb-comms subscribes to rwb.decision.events.v1 for the notice path, and the architecture test fails the build if one is added
    Then a repeated run of the same business date adds no second item and no second file

  Scenario: AC5 The notice decision names the package version and the route-set fields are copied verbatim (new, D-RCV-60)
    Given the rwb-decision contract mock returns R-RES-04 of version "RES-2026.12" with action_text "Assign the case to a restructuring officer and start the offer clock", owner_role "RW-RESTRUCT" and timer_spec "2 working days"
    Given the rwb-decision contract mock returns the PAYMENT_MATCH rows in force in the order EXACT priority 1, WINDOW priority 2, PARTIAL priority 3
    When a notice of case "RW-2026-000777" is decided under version "RES-2026.12"
    Then the next action, the owner and the due date of the notice are the three values verbatim and none of them is held in code
    Then the local decision record names package "RESTRUCTURE", version "RES-2026.12", its checksum and rule "R-RES-04"
    Then the rows are tried in the order the registry holds and this service re-sorts them into no other order
    Then payment "PAY-91008" of 12,500.00 THB that both EXACT and WINDOW match is decided by EXACT
    Then payment "PAY-91002" of 11,875.00 THB is decided by PARTIAL with a shortfall of 625.00 THB
    Then a version rolled back after the decision leaves the record naming "RES-2026.12" and rewrites no notice row
    Given the version list answers no version in force
    When a notice is requested
    Then the answer is NoPackageInForce, no notice row is written, nothing is dispatched and the caller sees MSG-GEN-006

  Scenario: AC6 payment_match_rule and DF-REF-261 to DF-REF-273 exist nowhere in rwb_comms (new, D-RCV-60)
    Given a database migrated from empty with the rwb-comms migrations of the release
    When the rwb-comms schema check runs
    Then rwb_comms holds notice, template, merge_field and the library objects, and no table named payment_match_rule
    Then no column of DF-REF-261 to DF-REF-273 exists in any rwb_comms table
    Then no rule row, DRL, test or query of this service names that table or those field IDs
    Then the check reads only rwb_comms and fails the build when a migration creates either
    Then the 93-table count of the legacy criterion is not asserted here, because it is the monolith schema's and RWB-P3-E2042-APP's

  Scenario: AC7 Each business rule of section 8 is traced to a criterion or a test (new, D-RCV-60)
    Given the rules BR1 to BR13 of section 8 and their rows in section 7 and section 16
    When the traceability check of the build runs
    Then every rule BR1 to BR13 has at least one criterion of section 7 or one test row of section 16
    Then a rule with no criterion and no test fails the build
    Then a rule that is an architecture constraint, BR4, BR10 or BR11, is proved by the architecture test or the schema check of this service

  Scenario: AC8 A retried or timed-out EvaluateRules activity creates at most one notice row for the same decision (new, D-RCV-60)
    Given notice "N-0101" is being decided under version "RES-2026.12" and the EvaluateRules activity of the notice path is started for it
    When the activity is retried after a timeout
    Then the retry reads the same package code, version label and checksum as the first attempt
    Then at most one notice row exists for notice "N-0101" after the retry
    Then a timed-out attempt that wrote no notice row leaves no notice and dispatches nothing for it
    Then the retry adds no second item to the dispatch run

  Scenario: AC9 A consumed call that fails or does not answer creates no notice and dispatches nothing (new, D-RCV-60)
    Given the rwb-decision version list call fails or does not answer
    When a notice of case "RW-2026-000777" is requested under version "RES-2026.12"
    Then no notice row is written and nothing is dispatched
    Then the decision record names no package version that the call did not return
    Then the caller is returned the failure and is not returned a version
```

The six criteria are new under D-RCV-60, AC7 to AC9 are added at the readiness review, and each tests only a deliverable of this story. No legacy criterion is restated: AC1 to AC6 of RWB-E2-042 belong to RWB-P3-E2042-APP, and the load and approve path belongs to RWB-P7-E2042-APP. The registry, its seeding and JOB-20 are RWB-P7-E2042-APP's (ASM-A6-tables-3); AC1 is proved against the rwb-decision contract mock here and against the real service in RWB-ITG-E2042-ITG. The values inside the criteria are the legacy values — the package codes, the labels, the row and scenario counts, the valid-from date, the rule IDs, the three route-set values and the two payment fixtures — so this side is proved against the same data the legacy story used.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A rule change never raises a notice: a load, an approval, a promotion or a rollback of any package writes no `notice`, `template` or `merge_field` row, sends nothing on any channel and raises no task | RWB-ITG-E2042-ITG section 2; RWB-P7-E2042-APP section 19; legacy section 8 BR1 |
| BR2 | Every notice decision names the package code, the version label, the checksum and the rule ID that decided it, written on the local decision record in the same transaction as the notice row; the field IDs that carry the package code and the checksum are confirmed by the decision-record owner when the record is published, and no column is added to `notice`, `template` or `merge_field` (GAP-2397) | R-UNI-38; DP-03; Temporal and Drools design slide 16 |
| BR3 | A notice keeps the version it was decided under; a promotion or a rollback changes the next decision and never rewrites a past one | R-UNI-38; legacy BR8 |
| BR4 | The values of a package are data of rwb-decision: no package code, label, row, threshold, match type, tolerance or window is held in this service's code or configuration | D-RCV-36 T3 to T6; DP-04; template §R7.2 s17 |
| BR5 | The route-set fields `action_text`, `owner_role` and `timer_spec` are read by rule ID and package version and copied verbatim; a blank field refuses the read and the notice is not created. Where the three fields set the next action of a case, the behaviour stays with RWB-E2-035 (GAP-2400; ASM-3984) | D-RCV-36 T6; FEAT-CWC-28; legacy BR4 |
| BR6 | The rows of a package are tried in the order the registry holds, first match, exactly one row decides and the default row is last; this service re-sorts nothing | D-RCV-36 T5; legacy BR7 |
| BR7 | A package version is used only when it is in force and its checksum is verified; when no version is in force the answer is `NoPackageInForce`, the notice is not created and nothing is dispatched | RWB-P3-E2042-CON AC5; RWB-P6-E1073-APP AC1 |
| BR8 | The version in force is resolved through the contract on each decision and the scenario count is read against `rules.testcases.min` = 50 through the parameters contract; neither is a constant | REQ-CWC-014; DP-06 |
| BR9 | The dispatch run of JOB-10 pins one version for the whole run, so one file never mixes two versions of the same package | DP-10; Arch v5 slide 44; this story |
| BR10 | The notice path learns of a version through the local copy of `RWB-P6-E1073-APP` and never through a listener added for it; the architecture test fails the build when one is added | Arch v5 slides 17, 20 and 42; this story |
| BR11 | `payment_match_rule` is never created in `rwb_comms`, and DF-REF-261 to DF-REF-273 stay retired and are referenced by no row, DRL, test or query | D-RCV-36 T10; legacy BR5 |
| BR12 | Every notice operation declares its capability area and right and a caller without it is refused; no role row is held in `rwb_comms` | TSD P6 v2 T6.1; RWB-P4-E2042-APP |
| BR13 | The UNIVERSAL package (R-UNI-01 to 50) is evaluated in this service from its own local copy of the same approved version as the other packages; its authoring, scenarios and approval are rwb-decision's (`RWB-P7-E2042-APP`) | GAP-2034; Rules Engine Design v3 section 2; Temporal and Drools design slide 13 |

### 9. State transitions

This story adds no state to the notice and removes none. It records the package version that a notice was decided under and proves that the package lifecycle does not move a notice.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A notice is requested and a version is in force | The decision names one version and its checksum and the record is written | "Approved" (or "Held" where the template rule of RWB-P6-E2021-APP holds it) |
| (none) | A notice is requested and no version is in force | `NoPackageInForce` is answered | No `notice` row exists; nothing is dispatched |
| (none) | A route-set field of the decided rule is blank | The catalog read is refused | No `notice` row exists; MSG-P3-027 |
| Any notice state | A load, an approval, a promotion or a rollback of any package | None | Unchanged: no notice moves and no row is rewritten |
| Any notice state | The version it was decided under is rolled back | R-UNI-38 applies | Unchanged: the decision record keeps the rolled-back version |

The case transitions of RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 are those stories' and are neither raised nor observed here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Requests and reads a notice under Litigation C and R; sees the next action, the owner and the due date the route set gives, and no rule value |
| RW-ENFORCE, enforcement owner and RW-CASEOWN, case owner | Request and read a notice under Litigation C and R for a case in their scope |
| RW-COE, center of excellence analyst | Loads and rolls back a package version in rwb-decision under Rules and parameters C and U; here the actor is a registry role and not a user of this service |
| RW-RISK, risk and model risk officer | Approves a version in rwb-decision under Rules and parameters A; is never the author |
| RW-AUDIT, internal audit | Reads the decision records of the notices of a case and the version each one names, under Litigation R; changes nothing |
| SY-RULES, Drools evaluator | Returns `RuleResult` with the package code, the version, the rule ID and the outputs, or `NoPackageInForce` inside the activity |
| The rwb-comms service identity | Resolves the version, reads the route set, writes the notice, the record and the outbox row, and pins the version for a dispatch run; it performs no governance action on a package |
| The build pipeline, no user role | Runs the architecture test of BR10 and the schema check of AC6 on a Testcontainers database; never connects to SIT, UAT or PROD |
| No delegation of authority level applies | A rule package version is not a credit decision and a notice is not an approval item |

No person is named anywhere in this story: the actors are roles and service identities. The rights are answered by the guard of RWB-P4-E1037-CON and the matrix of RWB-P4-E2042-APP; this story names them and holds no role row. The database login is the per-service login of DP-02, written only as "the rwb-comms login (DP-02)".

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`) | id | Write at generation; read |
| DF-LEG-016 | notice | case_id | Write; read |
| DF-LEG-018 | notice | notice_type | Write from LOV-NOTICE through DP-07; read |
| DF-LEG-030 | notice | party_id | Write; read |
| DF-LEG-031 | notice | template_id | Write; read |
| DF-LEG-032 | notice | hold_reason | Read; written by the template and conduct rules of `RWB-P6-E2021-APP`, never by a rule change |
| DF-LEG-022 | notice | delivery_status | Read; unchanged by this story |
| DF-REF-046, DF-REF-047 | template (`rwb_comms`) | template_code, template_version | Read; unchanged by a rule change (AC2) |
| DF-REF-051, DF-REF-064 | template | approved_by_legal, approved_at | Read; the Legal approval of `RWB-P6-AD017-APP` is the only writer |
| DF-REF-253, DF-REF-259 | merge_field (`rwb_comms`) | merge_code, catalog_version | Read; no row written by a rule change (AC2) |
| DF-REF-008 | rule_row (P7 `rwb_decision`) | action_text | Read through the catalog by rule ID and version; copied verbatim (BR5) |
| DF-REF-010 | rule_row (P7) | owner_role | Read through the catalog; copied verbatim (BR5) |
| DF-REF-011 | rule_row (P7) | timer_spec | Read through the catalog; copied verbatim (BR5) |
| DF-REF-274 to DF-REF-278 | rule_package (P7) | Field names: Not specified in the source documents (CG-ALL-6617) | Read only through the contract; never written here |
| DF-REF-279 to DF-REF-295 | rule_package_version (P7) | Field names and the row and scenario counts: Not specified in the source documents (CG-ALL-6617) | Read only through the contract; never written here |
| DF-REF-296 to DF-REF-298 | rule_row (P7) | Field names: Not specified in the source documents (CG-ALL-6617) | Read only through the contract; never written here |
| DF-REF-299 | rule_test_case (P7) | Field names: Not specified in the source documents (CG-ALL-6617) | Read only through the contract; never written here |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | decision_log_entry (`rwb_comms`) | the record of a notice decision, with the rule ID and the rule version; the package code and the checksum: Not specified in the source documents (CG-ALL-6618) | Write one row per notice decision through the library (DP-03); read by audit |
| (outbox) | outbox_event in `rwb_comms` | the `NoticeGenerated` and `DecisionRecorded` rows | Write in the same transaction as the notice row |
| (inbox) | processed_event in `rwb_comms` | the dedupe row of a consumed event | The notice path of this story consumes no event |
| DF-ACE-* | ACE views | — | Not read: this story reads no ACE view (DP-05) |
| DF-REF-261 to DF-REF-273 | payment_match_rule (retired) | — | Not created, not read and not written; their absence is asserted by AC6 |

No field is added by this story: the package code, the version and the checksum sit on the decision record that DP-03 already defines, so `rwb_comms` needs no new table and no new column (GAP-2397; ASM-3981). `notice`, `template` and `merge_field` are this service's three tables and no other service reads them (DP-01); `rule_row`, `rule_package` and its versions are rwb-decision's and are read only through the contract. The field IDs are those of the Logical Data Model and Data Dictionary, as the legacy story and TSD P6 v2 T3.1 cite them.

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no REST operation, no path and no field: the notice operations it works with are `POST /api/recovery/comms/v1/cases/{caseId}/notices` (API-P6-001) and `GET /api/recovery/comms/v1/notices/{noticeId}` (API-P6-002), owned by `RWB-P6-E2021-APP`, and their answers are unchanged — a rule version is evidence on the decision record and not a field of the notice answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | `action_text`, `owner_role`, `timer_spec` and the outputs of one rule row by rule ID and version; faked for R-RES-04 and the route-set rows |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The compiled model, its version label and its SHA-256, which is the checksum the decision record names; faked with one correct and one wrong checksum |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version in force, its status, its valid-from date and its row and scenario counts; faked for the three packages |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | `rules.testcases.min` (50) and `drools.kiebase.cache.max` (20) on the business date, as parameters and never as code (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE with DEMAND as a statutory notice, LOV-DELIVERY and the notice-state vocabulary (DP-07) |

Each call is one hop with a 2 s client budget, a GET retries once with jitter and each downstream has its own circuit breaker (DP-11, ADR-020). No call changes a registry row and no call is made from workflow code.

#### 12.3 Events published

None by this story. `rwb.comms.events.v1` carries `rwb.comms.NoticeGenerated.v1` (EV-13), `rwb.comms.NoticeDispatched.v1` (EV-14) and `rwb.comms.NoticeDelivered.v1` (EV-15), published by the notice stories of this service; this story writes only the `DecisionRecorded` row that the local library publishes on `rwb.decision-record.v1` in the same transaction as the notice (DP-03). No event announces a rule version, and the absence is the requirement (BR1).

#### 12.4 Events consumed

None. This story consumes no event on any topic. The consumption of `rwb.decision.RulePackageInForce.v1` from `rwb.decision.events.v1` is `RWB-P6-E1073-APP`'s and feeds the local copy; the notice path of this story reacts to nothing, and AC4 fails the build if a listener is added for it. The consumed events of the service remain those of the notice, dispatch and proof-of-delivery stories. Architecture v5 slide 13 gives the P6 to P7 pair a Temporal cell and no event cell while the published contract and the local-copy story require the subscription; the difference is carried as GAP-2396 with ASM-3980, and this story declares no consumed event under either reading.

#### 12.5 Workflows and activities

| Name | Type | Queue | Use in this story |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow (kit Notify template, existing) | `rwb-comms` | Carries the notice decision and the dispatch run; this story adds no step to it. Started by a notice request (POST /notices) or a stage workflow that needs a letter; workflow ID form: Not specified in the source documents (CG-ALL-6621); start and duplicate-start policy: Not specified in the source documents (CG-ALL-6621) |
| `EvaluateRules` | Activity (existing) | `rwb-comms` | Input package code, facts and business date; output `RuleResult` or `NoPackageInForce`; returns the version the decision names |
| `RecordAndApply` | Activity (existing) | `rwb-comms` | Writes the notice row, the decision record with the package code, version and checksum, and the outbox row in one transaction |

The two activities and the KieBase they use are `RWB-P6-E1073-APP`'s; this story fixes only what they return and what is recorded from it.

#### 12.6 Schedules

None. This story registers no Temporal Schedule and no Quartz row. The 16:00 dispatch run of JOB-10 on queue `rwb-comms` belongs to `RWB-P6-E2021-APP` and `RWB-P6-E1007-APP` and is unchanged; the 00:01 promotion is JOB-20 in rwb-decision (DP-10).

#### 12.7 Tables owned

| Table | Schema | Access in this story | Owner service |
|---|---|---|---|
| `notice` | `rwb_comms` | Read; written by the notice stories. No row written by a rule change | rwb-comms |
| `template` | `rwb_comms` | Read; the Legal approval of `RWB-P6-AD017-APP` is the only writer | rwb-comms |
| `merge_field` | `rwb_comms` | Read; no row written by a rule change | rwb-comms |
| `decision_log_entry` | `rwb_comms` | Written one row per notice decision through the library (DP-03) | rwb-comms |
| `outbox_event`, `outbox_delivery`, `processed_event` | `rwb_comms` | PLT library objects: the `NoticeGenerated` and `DecisionRecorded` rows, written in the same transaction | rwb-comms |

No `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `recovery_case` or `payment_match_rule` row is owned or read: the first four are rwb-decision's and are read through 12.2, the case is rwb-case's, and the last is retired.

#### 12.8 Contract fakes

| Fake | Contract | What it answers |
|---|---|---|
| rwb-decision WireMock | The three consumed operations of 12.2 | The catalog row of R-RES-04 and the route-set rows; the model of each version with its checksum, plus one wrong checksum; the version list with the three in-force versions and their counts, plus an empty answer that produces `NoPackageInForce` |
| rwb-case WireMock | The parameters and reference-data contract | `rules.testcases.min` 50 and `drools.kiebase.cache.max` 20; LOV-NOTICE with DEMAND statutory, LOV-DELIVERY and the notice-state vocabulary; a delayed answer beyond the 2 s budget |

No fake of rwb-access is added: the refusal path of AC1 is proved against the guard of `RWB-P4-E1037-CON`.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 consumed, none provided | The catalog read, the model read and the version list of rwb-decision; the parameters and reference-data reads of rwb-case; one hop, 2 s budget |
| Kafka | 1 written by the library, none published by this story | `DecisionRecorded` on `rwb.decision-record.v1`; `rwb.comms.events.v1` untouched by a rule change |
| Temporal | 1 workflow and 2 activities (existing) on `rwb-comms` | `NoticeDispatchWorkflow`, `EvaluateRules` and `RecordAndApply` |
| File | None in this story | The WIN file of INT-14 is the dispatch run's, and a rule change adds no line to it |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms.rules` for the resolver and the catalog reader; the architecture test in the service's test tree alongside the schema check.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `NoticeRuleVersionResolver` | Service | Resolves the package code, the version in force and its checksum for the business date; holds no label in code (BR4, BR8) |
| `RouteSetFieldReader` | Service | Reads `action_text`, `owner_role` and `timer_spec` by rule ID and version; refuses a blank field (BR5) |
| `NoticeDecisionRecorder` | Service | Puts the package code, version and checksum on the record written by `RecordAndApply`, in the same transaction as the notice and the outbox row (BR2) |
| `DispatchVersionPin` | Configuration of the dispatch run | Pins the version the run started with for every notice of the file, so one file never mixes versions (BR9) |
| `NoticePathSilenceProbe` | Test support | Asserts that a governance action on any package writes no notice, template, merge_field or outbox row, sends nothing and raises no task (AC2, AC3) |
| `NoticePathListenerTest` | Architecture test | Fails the build when a class of the notice path subscribes to `rwb.decision.events.v1` or reacts to a package state (BR10) |
| `PaymentMatchRuleAbsentCheck` | Schema test | Fails the build when `payment_match_rule` or a column of DF-REF-261 to DF-REF-273 exists in `rwb_comms` (AC6) |
| `Epic2NoticeRunbook` | Run book | The order of the four governance actions, the version evidence to collect per notice, and the check that the 16:00 file is unchanged |

**Database and Blob.** No migration and no Blob object. The package code, version and checksum sit on `decision_log_entry` of DP-03; the local copy and its rows are `RWB-P6-E1073-APP`'s. The retired table and its thirteen field IDs are absent by construction and asserted by AC6.

**Configuration and reference data.** `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 through the parameters contract; LOV-NOTICE and the notice-state vocabulary through the reference-data contract; the three version labels and the valid-from date 2026-12-01 as registry data. The harness repository, SIT environment, seeding set, evidence format, gate and fake response bodies are Not specified in the source documents (GAP-0421); this story holds none of them.

**Build steps**

1. Build `NoticeRuleVersionResolver` against the fakes of 12.8; test AC1 and the empty answer of X1.
2. Build `RouteSetFieldReader` and copy the three values into the notice; test AC5 and the blank field of X2.
3. Put the package code, the version and the checksum on the record through `NoticeDecisionRecorder`; test the pinning and the rolled-back version of AC5.
4. Build `NoticePathSilenceProbe` and run the four governance actions against the fakes; test AC2, AC3 and AC4.
5. Add `DispatchVersionPin` and prove that one file never mixes two versions; test AC4 and the repeated run.
6. Add `NoticePathListenerTest` and `PaymentMatchRuleAbsentCheck`; test AC6 and X9.
7. Write the run book and hand the fixtures to `RWB-ITG-E2042-ITG`.

**Done when.** The tests of section 16 pass; the three versions resolve with their counts; the four governance actions add no row, no message and no dispatch item; and the migrated `rwb_comms` holds no `payment_match_rule` and no retired column.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | A downstream read is unavailable beyond the retry, or no version is in force | The service is unavailable. Try again later. |
| MSG-P3-027 | A rule row is incomplete at the catalog read | The rule version was refused at the {check} check: {detail}. |
| MSG-P6-003 | The template behind the notice was withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right calls a notice or a version read | You cannot {action} here. Your role does not include it. |

This story adds no message. For MSG-P3-027 the {check} value is catalog and the {detail} names the rule ID, the row order and the column name only, never a case fact or a person. The exact {detail} wording for the match order and catalog completeness checks is Not specified in the source documents (GAP-1300). The wording of MSG-GEN-006 for the empty-version case is the platform message and its text is the platform library's, not a value of this story.

### 15. Screens and states

No screen is built in this story and nothing is rendered. The notice panel, its states and its field list are `RWB-P6-E2021-APP`'s and are served through the gateway-bff composite route of DP-19; SCR-33 Template approval and SCR-39 Rules and parameters are unchanged. The states of SCR-33 (empty, loading, error, no access) are Not specified in the source documents (CG-ALL-6630), and the states of SCR-39 (empty, loading, error, no access) are Not specified in the source documents (CG-ALL-6631). What becomes visible to a reader of the notice and its audit trail is the evidence: the notice shows the next action, the owner and the due date from the route set, and the audit view of the decision record shows the package code, the version label and the checksum. No screen shows a package version it did not read from the record.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1 | Component | RESTRUCTURE RES-2026.12, 38 rows, 62 scenarios, in force from 2026-12-01 |
| TC-E2-042-02 | AC2 | Contract | PAYMENT_MATCH PMT-2026.12, 3 rows, 58 scenarios; the version list of the rwb-decision fake |
| TC-E2-042-03 | AC3 | Contract | BOOKING_MATCH BKG-2026.12, 21 rows, 54 scenarios; the model read returns the checksum |
| TC-E2-042-04 | AC4 | Component | PAY-91008 matched by EXACT and WINDOW; PAY-91002 5 percent short |
| TC-E2-042-05 | AC5 | Component | R-RES-04 and the route-set rows of RES-2026.12; a blank timer_spec; an empty version list |
| TC-E2-042-06 | AC6 | Component | Migrated `rwb_comms` database, no payment_match_rule and no DF-REF-261 to DF-REF-273 |
| TC-E2-042-07 | AC2 | End to end | Notices, templates and merge codes before and after a load, an approve, a promotion at 00:01 and a rollback of RES-2026.13 |
| TC-E2-042-08 | AC3, AC4 | End to end | The same four actions with the 16:00 dispatch run of 2026-12-15 and notices "N-0101" and "N-0102" |
| TC-E2-042-09 | Not specified in the source documents (DOR-RWB-P6-E2042-APP-12) | Component | Boundary values of each table of 12.7 (ASM-3438) |
| TC-E2-042-10 | AC7 | Component | Section 8 rules BR1 to BR13 and their rows in sections 7 and 16 |
| TC-E2-042-11 | AC8 | Component | EvaluateRules started for "N-0101" under "RES-2026.12" and retried after a timeout |
| TC-E2-042-12 | AC9 | Component | rwb-decision version list call failed or not answered; notice of "RW-2026-000777" requested |

The six legacy IDs, their numbers and their legacy fixtures are kept. Level follows the mapping used across the set: legacy System becomes Component or End to end, and legacy Schema becomes Component. Two rows are new on this side and are numbered in the same series, `TC-E2-042-07` and `TC-E2-042-08`, because the silence of the notice path is the deliverable of this story and no legacy test case covers it: in the monolith a rule read was an in-process call that could not raise a notice, so no case was written for it. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the package codes, the version labels, the row and scenario counts, the match types, the tolerances, the windows, the route-set values and `rules.testcases.min` are registry rows or parameters, read through DP-04, DP-06 and DP-07.
- No personal data in events, workflow inputs, logs, tests or prompts: the facts handed to the kit are the case reference, the notice type, the template code and version and the business date; the party, the address and the contact values never leave the notice row, and the payload check fails the build when one appears.
- No cross-schema read and no cross-service write: `notice`, `template`, `merge_field` and the record are `rwb_comms`; the rule facts come from the published operations of 12.2 and no statement names `rwb_decision`, `rwb_case` or another schema (DP-01).
- ACE data only through the owner's contract or the owner's `v_ace_*` views: this story reads no ACE view; the contact and address facts belong to `RWB-P6-E2021-APP` and to rwb-source-data (DP-05).
- A rule change never reaches a customer: no listener, controller, Schedule or activity of the notice path reacts to a package state, and the architecture test fails the build if one is added.
- `payment_match_rule` is never created and DF-REF-261 to DF-REF-273 are never referenced; the schema check reads only `rwb_comms`.
- The build gate and the schema check read a release manifest and a Testcontainers database; they never connect to SIT, UAT or PROD.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Epic 1, 3.3; Program, 5.3 (Epic 2, 3.2 and 3.8 is stale) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-UNI-38; R-RES-26 | TC-E2-042-01, TC-E2-042-02, TC-E2-042-03, TC-E2-042-06 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | Epic 1, 3.3; Program, 5.3 (Epic 2, 3.2 and 3.8 is stale) | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | R-RES-26; R-RES-04 | TC-E2-042-04, TC-E2-042-05, TC-E2-042-07, TC-E2-042-08 |

| Element | Trace |
|---|---|
| DP01, DP15 | The three tables and the record in `rwb_comms`, no migration in this story, no other schema read |
| DP03 | The local decision record written by the library on `rwb.decision-record.v1` with the package code, version and checksum |
| DP04, DP06, DP07 | The embedded kit, the parameters and the reference data read through the contracts of 12.2, and no value in code |
| DP05 | No ACE view and no ACE row read: the contact and address facts are other stories' |
| DP10 | JOB-10 as the 16:00 dispatch run on queue `rwb-comms`, JOB-20 as the 00:01 promotion in rwb-decision, and no Quartz row |
| DP13, DP14, DP19 | `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb.comms.<Event>.v1`, and the notice panel through gateway-bff |
| RWB-P6-E1073-APP | The local copy, the checksum, the KieBase registry and the two activities this story uses and does not rebuild |
| RWB-ITG-E2042-ITG | The cross-service proof that a load, an approval, a promotion, a swap and a record hold together |

### 19. Out of scope

- The registry rows, the load, the six checks, the 50-scenario gate, the dry run, the four-eyes approval, the effective dating, the one-call rollback and the decision-log reads (RWB-P7-E2042-APP).
- The workbook authoring, the Rows and Tests tabs, the write-once Blob store, the model cache and `RuleScenarioBuildGate` (RWB-P3-E2042-APP).
- The local copy, the model fetch, the checksum verification, the KieBase registry, the scenario re-run, the atomic swap, the `EvaluateRules` and `RecordAndApply` activities and the consumption of `RulePackageInForce` (RWB-P6-E1073-APP).
- The roles, the permission matrix, the delegation of authority and the screens (RWB-P4-E2042-APP, RWB-P4-E1037-CON).
- The notice generation, the conduct check, the contact stop, the SMS and LINE send, the dispatch loop, the WIN file and the proof-of-delivery capture (RWB-P6-E1052-APP, RWB-P6-E2021-APP, RWB-P6-E1007-APP, RWB-P6-E1055-APP).
- The template lifecycle and its Legal approval (RWB-P6-AD017-APP); a rule change withdraws no template and approves none.
- The rule evaluation of the case engines: the route set that sets a next action, an owner and a due date on the case is RWB-E2-035 and its service story, and the payment match of JOB-07 is RWB-E2-027 and the rwb-payment story of that key.
- The remaining 448 routing rules, the UNIVERSAL package and the Epic 3 rule sets.
- The cross-service proof itself (RWB-ITG-E2042-ITG): this story proves its own side against fakes only.
