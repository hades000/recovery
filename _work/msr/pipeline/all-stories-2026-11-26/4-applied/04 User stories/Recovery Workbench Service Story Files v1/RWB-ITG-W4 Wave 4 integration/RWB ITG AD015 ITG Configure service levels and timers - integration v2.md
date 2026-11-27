# RWB-ITG-AD015-ITG Configure service levels and timers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-AD015-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1028-APP, RWB-P4-AD015-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration proof of RWB-AD-015 for RWB-ITG-W4 — that one approved service-level version is the value the next timer uses across rwb-case, rwb-access and rwb-decision, that a running timer keeps its due date when a version takes effect, and that the approval is refused without the Rules and parameters A right or when the decision record cannot be written; the load and the right are RWB-P4-AD015-APP's, the timer and its projection are RWB-P3-E1028-APP's, and the approval and the ledger are rwb-decision's. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-AD015-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that one approved service-level version is the value the next timer uses across rwb-case, rwb-access and rwb-decision, that a running timer keeps its due date, and that the approval is refused without the right or when the decision record cannot be written**, so that **configuration is proved to change the clock once, at the next timer, and never to rewrite a clock that is already running**.

This story is a harness and an evidence report, and nothing else. It builds no production endpoint, no table, no workflow, no activity, no schedule, no screen and no event, and it writes no code in any service. It drives the published operations of the owners, reads the effect through the owners' published reads, counts the events on the owners' topics and writes one run report. On Day 1 it runs against stubs generated from the published contracts; as each I story lands, its stub is replaced and the same tests run again.

The legacy key splits three ways, and the split is the point of the story. **RWB-P3-E1028-APP owns rwb-case**: the `timer` table as the screen projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, the durable Temporal timer inside `CaseWorkflow`, the parameter contract (DP-06) and the reference-data contract (DP-07) that carry the service-level values and the state codes, and the rule rows the workflow reads its timer specification from. **RWB-P4-AD015-APP owns rwb-access and administration**: the Rules and parameters A and C rights, the governed load, and the session the refusal is answered from. **rwb-decision (P7) owns the rule-version approval** — `POST /api/recovery/decision/v1/admin/rule-versions` and `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` — and **the central ledger** behind `GET /api/recovery/decision/v1/decision-log`. SCR-42 Queues and service levels and SCR-39 Rules and parameters are gateway-bff composite routes over those calls (DP-19) and are not built here.

**This story proves the configuration effect and not the timer lifecycle.** The durable timer, the warning at its point, the breach, the catch-up after a worker outage, the pause and resume, and the prescription date belong to RWB-ITG-E1028-ITG on the same wave and are not restated in this file; the same applies to RWB-P3-E1028-APP, which builds all of it. What is asserted here is narrower and cannot be asserted by one service: that the value in force is the value the next timer uses, that the version is named on the timer that used it, that a new version does not retime a running clock, and that no approval and no timer exists without the right and without the decision record.

### 2. Business rationale

The legacy story loads the time allowed in each case state, its warning and its escalation point as data, so that clocks and escalations follow the agreed service levels. DL22 settles the reason it is data rather than a constant: how long a case may stay in each state is "not a choice. A value per state from the business", loaded as parameters, and escalation "runs from the day they are loaded". The legacy acceptance criteria are the two halves that matter — a new value takes effect for new timers, and a running timer keeps its due date unless the rule says to recompute.

Under D-RCV-60 the values become P3 parameter and reference rows, the approval becomes P7's, and the record of the approval leaves on `rwb.decision-record.v1` from the service that made the change (DP-03). The split matters because a service-level version is a fact about two reads and one approval rather than about one service: the value is read by `CaseWorkflow` in rwb-case, the right to load and approve it is answered by rwb-access, and the approval that puts it in force is rwb-decision's, with its decision record collected into the central ledger. A version that applied to running clocks would retime work already promised to a customer, and a version that took effect in one service but not the other would leave the screens, the clocks and the ledger disagreeing about the same case.

Two pieces of architecture set the shape of the proof. **JOB-05 and its five-minute Quartz timer check are retired**: the clock is a durable Temporal timer inside `CaseWorkflow` (Architecture v5 slide 44, "durable timers (retired)"; slide 42 records event #18 `TimerDue` as retired because the timer lives inside the workflow). **The `timer` row stays as the P3 projection** behind `GET /api/recovery/case/v1/cases/{caseId}/timers` (ASM-0078), so the proof reads the clock through the published P3 contract and needs no table access of its own. `TimerBreached` is still rwb-case's and still on `rwb.case.events.v1` (slide 42 event #19); this story does not produce it and observes it only if its report needs it. The rule rows that carry the timer specification — `from_state`, `timer_spec`, `valid_from`, `valid_to` — stay with P7 as the versioned catalogue (ASM-0069), and rwb-case reads them through the published contract.

The decoupling is the harness's too. Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). The parameters are read through the P3 parameter contract (DP-06) and the state codes and list values through the P3 reference-data contract (DP-07), so no service keeps a second copy. The decision record is written by the approving service through the local decision-record library and confirmed by the ledger (DP-03, ADR-022). Where a screen would compose these calls the path is the gateway-bff composite route (DP-19), and the gateway's contract list already carries `RulePackageInForce` as a cache-refresh event (Architecture v5 slide 20), which is why a version taking effect is expected to reach the running services by event and not by a restart.

The target split of the legacy key is therefore: **RWB-P4-AD015-CON and RWB-P4-AD015-APP** own the load, the two rights and their refusals; **RWB-P3-E1028-APP** owns the timer, the projection, the parameter and reference contracts and the rule rows the workflow reads; **P7** owns the rule-version approval and the ledger, whose build sits with RWB-P4-AD012-APP and RWB-P7-E2005-APP and not in this legacy key's split. **The two legacy acceptance criteria stay with RWB-P4-AD015-APP.** This integration story owns no legacy acceptance criterion: it owns the six new scenarios of section 7, which assert only what no single service can assert alone — that the value in force is the value the next timer used, that a running clock is untouched when the version changes, that the right is checked before the version enters force, and that the approval and the record are one thing.

Where the sources do not publish the exact surface this suite needs — the layout of the service-level file and its warning, the name of the valid-from parameter, the exact fields of the timer projection, the message a refused load answers, and the rule that says when a running timer is recomputed — the suite asserts through the owners' contracts and records the open point as GAP-0439 and ASM-0631. Release 30 June 2027 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1028-APP is the I story that owns the deliverable: the durable SERVICE_LEVEL timer inside `CaseWorkflow`, the `timer` projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, and the P3 parameter and reference-data contracts that carry the service-level values and the state codes. Its stub answers from Day 1 and is replaced when it lands.
- RWB-P4-AD015-APP is the I story that owns the load, the Rules and parameters A and C rights and their MSG-P4-002 refusal, and the session read. Its stub answers from Day 1 and is replaced when it lands.
- The published contracts of P3 rwb-case, P4 rwb-access and P7 rwb-decision are in the contract registry and deployed in SIT under `/api/recovery/<short>/v1` behind gateway-bff, and a stub set is generated from each one with its version pinned in the run report.
- The P7 rule-version approval and the central ledger are consumed through P7's published contract. Their build is not part of this legacy key's split — the rule-version load and approval are RWB-P4-AD012-APP's and the ledger read is RWB-P7-E2005-APP's — so they do not appear as I rows in the metadata, and the stub answers for both until those stories land.
- SIT is in place: the Temporal namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-access` and `rwb-decision`, and the topics `rwb.case.events.v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1` with their retry and `.dlt` topics.
- The SERVICE_LEVEL row for state `LIT_PACK` is loaded through the P3 parameter contract as 10 working days with a warning at 8 working days, and the state code `LIT_PACK` is present in the reference list served by the P3 reference-data contract. Both are held in the fixture as data and never written in code.
- The fixture calendar holds no non-working day between 2027-06-10 and 2027-06-30, so a due date computed from a working-day count can be read against the numbers in section 7.
- The synthetic case and user set is the harness's own: cases `RW-2027-000801`, `RW-2027-000803`, `RW-2027-000805`, `RW-2027-000806` and `RW-2027-000809`, the approver holding Rules and parameters A as `RW-RISK`, the loader holding Rules and parameters C as `RW-COE`, and `RW-OFF` as the caller without the right. No production data is used and no production connection is opened; the suite refuses an environment that is not SIT.
- The load layout of the service-level file, the name of the valid-from parameter, the exact fields of the timer projection, the message a refused load answers, and the rule that decides when a running timer is recomputed: Not specified in the source documents (GAP-0439; ASM-0631).
- The platform stories the patterns add — RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON — are platform wave deliveries that every service and the harness build against; they are not repeated in the metadata H row of this story, which stays None.
- No build dependency, so the story is ready on Day 1 under Template and Rules §R5.7. The two I stories replace their stubs and never block the lane; until they land, the run is reported as a stub pass.

### 4. Flow

1. Harness: loads the fixture — the five synthetic cases, the approver `RW-RISK`, the loader `RW-COE`, the refused caller `RW-OFF`, versions "3" to "6" of the service-level file, the state code `LIT_PACK` in the reference list, the calendar without a non-working day in the window, and the business date 2027-06-14. It takes a baseline read of the case and of the timer projection for every case, and it opens no production connection.
2. Harness: records the version in force before the run, read through the P3 parameter and reference-data contracts, so the "from its valid-from date" part of AC1 has a baseline it did not write itself.
3. Harness: loads version "3" of the service-level file through the P3 parameter and reference-data contracts with one Idempotency-Key — state `LIT_PACK`, 10 working days, a warning at 8 working days, valid from 2027-06-15 — and asserts the version is held as VALIDATED and is not in force yet.
4. Harness: approves version "3" as `RW-RISK` through `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve`, and asserts APPROVED with the valid-from date it was loaded with. It reads the decision record of the approval and counts one `rwb.decision-record.DecisionRecorded.v1` (AC4).
5. Harness: reads the state code, the allowed time, the warning point and the valid-from date back through the P3 contracts and holds them as the parameter and reference baseline of the run (AC6).
6. Harness: the fixture enters case `RW-2027-000801` into `LIT_PACK` on 2027-06-15 09:00, `CaseWorkflow` starts the durable timer, and the harness reads `GET /api/recovery/case/v1/cases/{caseId}/timers` — RUNNING, `expires_at` 2027-06-29 09:00, `warn_at` 2027-06-25 09:00, version "3" named on the timer (AC1).
7. Harness: reads case `RW-2027-000805`, which entered `LIT_PACK` on 2027-06-14 09:00, the day before the valid-from date, and asserts its timer does not name version "3", because the version in force at that date is the one that served it (AC1).
8. Harness: reads case `RW-2027-000803`, which entered `LIT_PACK` on 2027-06-16 09:00 under version "3", and holds the read — RUNNING, `expires_at` 2027-06-30 09:00, `warn_at` 2027-06-28 09:00.
9. Harness: approves version "4" as `RW-RISK` with valid from 2027-06-21 and with the time allowed and the warning point it carries for `LIT_PACK` held in the fixture as data; asserts one decision record and one `rwb.decision-record.DecisionRecorded.v1`; then re-reads case `RW-2027-000803` and asserts the timer is identical field for field, still RUNNING, still version "3", `expires_at` 2027-06-30 09:00 (AC2, AC4).
10. Harness: reads case `RW-2027-000806`, which enters `LIT_PACK` on 2027-06-22 09:00 after version "4" took effect, and asserts its due date and warning point are the ones computed from version "4", being the fixture's values and not a constant (AC2).
11. Harness: approves version "5" as `RW-OFF` through the same route and asserts 403 with `MSG-P4-002`, version "5" not in force, and case `RW-2027-000809` still served by the version in force (AC3). It then forces the decision-record write to fail, approves version "6" as `RW-RISK`, and asserts `MSG-P7-003`, no ledger entry, no event and version "6" not in force (AC5).
12. Harness: re-reads the state code, the allowed time and the warning point through the P3 contracts and asserts they are the same values the timer projection uses and exist once; loads version "7" carrying a state code the reference list does not hold and asserts the load is refused before any approval; then writes the evidence report, removes the fixtures and restores the clock (AC6).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | The version is loaded without its valid-from date | The load is refused and the version is not created, so nothing can be approved from it | MSG-GEN-001 | AC1 |
| X2 | The version carries a state code the reference list does not hold | The load is refused before it can be approved, and no timer in that state is ever started | None; the message ID for a refused service-level load is not specified | AC6 |
| X3 | A caller without Rules and parameters A approves a version | 403, the version is not in force, and new timers still use the version in force | MSG-P4-002 | AC3 |
| X4 | A caller without Rules and parameters C loads a version | 403 and no version row is created | MSG-P4-002 | AC1, AC4 |
| X5 | The decision record cannot be written at the approval | The approval stops, the version is not in force, no ledger entry and no event exist, and the next timer uses the version in force | MSG-P7-003 | AC5 |
| X6 | A new version is approved while a timer runs in the same state | The running timer keeps its `expires_at` and `warn_at` and keeps the version it started under | None | AC2 |
| X7 | Two versions claim the same state on the same date | The run fails on AC1 and names the two versions, their valid-from dates and the timer read | None | AC1 |
| X8 | The timer projection does not name the rule version that produced it | The run fails on AC1 and AC2 and names the case, the timer and the missing stamp | None | AC1, AC2 |
| X9 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | Preflight, AC1 |
| X10 | A consumed call exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy, the evidence report records it, and no assertion is made on data that was not read | None | AC1 to AC6 |

X1 to X8 are the configuration and clock failures the legacy story is written against, re-stated on the split services; X9 and X10 are the harness and cross-service failures that only appear when the run leaves one service. The one business message the load itself might carry is not published for a service-level row, so X2 is asserted on the refusal and not on a message ID, and the open point is held as GAP-0439 and ASM-0631.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module, needs the published contracts of P3, P4 and P7 and the stubs from Day 1, owns no schema and no table, and never writes a service-level row by hand |
| Negotiable | The fixture layout, the case and user keys, the business date, the version numbers and the report shape are agreed at the wave entry check; the state code, the allowed time, the warning point and the valid-from dates are data, and the legacy values are the only fixed ones |
| Valuable | Proves across services what one service cannot prove: the approved value is the value the next timer used, the version is stamped on that timer, a new version moves no running clock, the right is checked before the version enters force, and the approval and its record are one act |
| Estimable | One harness module, one fixture pack, four contract probes, one event observer, one report, and a direct swap from a stub to the owner |
| Small | Six scenarios over three services and two writes; no service code, no schema change, no production flag |
| Testable | Every scenario asserts a contract answer, a projected timer field, a version stamp, a ledger entry, an event count or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Configure service levels and timers - wave 4 integration harness

  Background:
    Given the services rwb-case, rwb-access and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given the harness runs against stubs generated from those contracts from Day 1 and no production data is used
    Given the service-level row for state "LIT_PACK" is 10 working days with a warning at 8 working days
    Given the fixture calendar holds no non-working day between 2027-06-10 and 2027-06-30 and the run business date is 2027-06-14

  Scenario: AC1 An approved service level is in force for new timers from its valid-from date (new, D-RCV-60)
    Given version "3" of the service-level file is loaded through the P3 parameter and reference-data contracts with state "LIT_PACK", 10 working days, a warning at 8 working days and valid from 2027-06-15
    When it is approved by "RW-RISK" through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve on 2027-06-14
    Then case "RW-2027-000801" entering LIT_PACK on 2027-06-15 09:00 carries a timer with expires_at 2027-06-29 09:00 and warn_at 2027-06-25 09:00
    Then GET /api/recovery/case/v1/cases/{caseId}/timers returns those values with version "3" named on the timer
    Then case "RW-2027-000805" entering LIT_PACK on 2027-06-14 09:00 does not name version "3", because the version in force on that date served it
    Then the allowed time, the warning point and the valid-from date are read from the approved version and are not constants in any service

  Scenario: AC2 A running timer keeps its due date when a new version takes effect (new, D-RCV-60)
    Given case "RW-2027-000803" entered LIT_PACK on 2027-06-16 09:00 under version "3" and its timer reads RUNNING with expires_at 2027-06-30 09:00 and warn_at 2027-06-28 09:00
    When version "4" is approved by "RW-RISK" with valid from 2027-06-21 and with the time allowed and the warning point it carries for LIT_PACK held in the fixture as data
    Then GET /api/recovery/case/v1/cases/{caseId}/timers returns the same timer RUNNING with expires_at 2027-06-30 09:00 and warn_at 2027-06-28 09:00, identical field for field to the read taken before the approval
    Then the timer still names version "3", the version in force when it started
    Then case "RW-2027-000806" entering LIT_PACK on 2027-06-22 09:00 gets its due date and warning point from version "4" and from the fixture values, not from a constant
    Then no running timer is recomputed, because no rule in version "4" marks a running timer for recompute (GAP-0439; ASM-0631)

  Scenario: AC3 A role without Rules and parameters A cannot approve the version (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" whose role does not hold Rules and parameters A
    When the caller approves version "5" through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the answer is 403 with "MSG-P4-002"
    And version "5" is not in force
    And case "RW-2027-000809" entering LIT_PACK after the attempt is served by the version in force and not by version "5"

  Scenario: AC4 The approval writes exactly one decision record with its rule id and rule version (new, D-RCV-60)
    Given version "4" is loaded and carries the rule id held in the fixture
    When it is approved by "RW-RISK" through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then GET /api/recovery/decision/v1/decision-log holds exactly one entry for the approval, with that rule id and rule version "4"
    And "rwb.decision-record.DecisionRecorded.v1" is published once on "rwb.decision-record.v1"
    And the central ledger confirms the entry with its chain sequence and its hash

  Scenario: AC5 A forced decision-record failure stops the approval (new, D-RCV-60)
    Given the decision record for the approval cannot be written
    When version "6" is approved by "RW-RISK" through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the answer carries "MSG-P7-003"
    And version "6" is not in force and a case entering LIT_PACK is still served by the version in force
    And GET /api/recovery/decision/v1/decision-log holds no entry for the approval and no "rwb.decision-record.DecisionRecorded.v1" is published

  Scenario: AC6 The state code, the allowed time and the warning point are read through the P3 contracts and held once (new, D-RCV-60)
    Given the state codes are read through the P3 reference-data contract and the allowed time and the warning point through the P3 parameter contract
    When the version in force is read back through both contracts and the timer projection of case "RW-2027-000801" is read beside it
    Then the state code "LIT_PACK", the 10 working days and the warning at 8 working days are the same values the projection uses
    Then no service holds a second copy of them and the timer names the rule version that produced it
    When version "7" is loaded carrying a state code the reference list does not hold
    Then the load is refused before any approval and no timer in that state is started
```

The two legacy acceptance criteria (AC1 the service level is loaded and new timers use the values, AC2 a running timer keeps its due date unless the rule says to recompute) are the business outcome RWB-P4-AD015-APP has to reach and are asserted here across the service boundary in AC1 and AC2. AC3 to AC6 are the new scenarios the split makes assertable: the right is checked by another service, the approval is another service's, the record is the ledger's, and the value must exist once.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The time allowed in each case state, its warning and its escalation point are loaded as data, and a business person can change them without a code change | RWB-AD-015 story and AC1; DL22 |
| BR2 | A new value runs from the date it is loaded and approved, and applies to timers started on or after its valid-from date | DL22, "escalation runs from the day they are loaded"; RWB-AD-015 AC1 |
| BR3 | A timer already running keeps its due date when a new version takes effect, unless the rule version says to recompute | RWB-AD-015 AC2 |
| BR4 | The clock is a durable Temporal timer inside `CaseWorkflow`, and JOB-05 and its five-minute Quartz check are retired | Architecture v5 slides 42 and 44; Template and Rules DP-10 |
| BR5 | The `timer` row stays as the rwb-case projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, so the clock is read through a published contract and never from a schema | ASM-0078; Architecture v5 slide 41 |
| BR6 | The values come from the rwb-case parameter contract and the state codes from the rwb-case reference-data contract, and no service keeps a second copy | DP-06, DP-07; Template and Rules §R3 default ruling |
| BR7 | The rule version that produced a timer is named on the timer, so the value in force at the start is knowable afterwards | DP-04; ASM-0069; Arch v5 slide 14 |
| BR8 | Approving a version needs the Rules and parameters A right, and a caller without it is refused with MSG-P4-002 | RWB-AD-015 permission checks; DP-08 pattern applied through P4 |
| BR9 | An action that cannot be recorded is not taken: a decision-record failure stops the approval with MSG-P7-003 and leaves the version out of force | RWB-AD-015 TC-AD-015-04; ADR-009; Temporal design slide 13, RecordAndApply |
| BR10 | Every call in the run is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout, and the composite path a screen would use is the gateway-bff route | DP-11, DP-13, DP-19; ADR-020 |
| BR11 | The decision record is written by the approving service through the local decision-record library on `rwb.decision-record.v1`, and the central ledger in rwb-decision confirms it | DP-03; ADR-022 |

The harness asserts these rules and changes none of them. The timer and its projection are P3's, the rights and the load are P4's, the approval and the ledger are P7's, and the value itself is business data held in the fixture.

### 9. State transitions

| Subject | From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|---|
| Service-level version | VALIDATED | APPROVED | the caller holds Rules and parameters A and the decision record is written | APPROVED | P7 rwb-decision, `POST /admin/rule-versions/{versionId}/approve`, one decision record |
| Service-level version | APPROVED | IN_FORCE | the valid-from date is reached | IN_FORCE | P7 rwb-decision, the version's valid-from date |
| Service-level version | VALIDATED | refused | the caller lacks Rules and parameters A, or the decision record cannot be written | VALIDATED, not in force | P4 rwb-access for the right; P7 rwb-decision for the record |
| Service-level version | VALIDATED | refused | the state code is not in the reference list, or the valid-from date is missing | not created | P3 rwb-case, the parameter and reference-data contracts |
| Running timer | RUNNING | a new version enters force | the new valid-from date is reached | RUNNING, same `expires_at` and `warn_at`, same version stamp | P3 rwb-case; no state change and no recompute |
| Running timer | RUNNING | a new timer starts | the case enters the state after the valid-from date | RUNNING, with the due date of the version in force | P3 rwb-case, `CaseWorkflow` |

The version states are the load, approval and in-force status of the versioned table; the timer has the RUNNING status of the projection and is not moved by configuration. The harness changes no state: every row above is made by the owner through its own operation, and the run reads the result through the owners' contracts. A state the harness set by hand would prove nothing, which is why the two writes in the run are the load and the approval and both are the owners' published operations.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK, risk officer | Holds Rules and parameters A and is the approver of AC1, AC2, AC4 and AC5; the approval is made as this role and never with a service identity |
| RW-COE, centre of excellence | Holds Rules and parameters C and is the loader of the versions in AC1 and AC4; the load is refused for any caller without it |
| RW-TEAMMGR and RW-CASEOWN | Read the case and its timers where their rights allow; they are the roles the clock is run for and the escalation points of the legacy story, and they change nothing here |
| RW-OFF, officer without the administration rights | Is the refused caller of AC3 and X4; holds no Rules and parameters right, so the approval and the load both answer MSG-P4-002 |
| QA lead | Owns the harness configuration, the fixture data, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the owning service |
| The owning services' identities | P3 starts and projects the timer, P4 answers the right and the session, P7 approves the version and holds the ledger; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, product_group, status, stage_code, rule_version | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer | timer_type, started_at, expires_at, warn_at, status | Read through the rwb-case timers contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, timer_spec, valid_from, valid_to | Read through the rwb-decision contract and applied by rwb-case |
| DF-REF-132 to DF-REF-146 | parameter_catalog | param_key, value_type, unit, default_value, scope, owner_role | Read through the P3 parameter contract |
| DF-REF-147 to DF-REF-158 | parameter_value | param_key, param_value, product_group, version_no, valid_from, valid_to, status | Read through the P3 parameter contract; changed only by P3's own load |
| DF-REF-159 to DF-REF-180 | reference_version | table_code, version_no, valid_from, valid_to, status, approver_user_id, content_hash | Read through the P3 reference-data contract |
| DF-REF-181 to DF-REF-184 | reference_row | version_id, row_key, row_data | Read through the P3 reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, chain_seq, entry_hash | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The case and the timer are P3's, the parameter and reference rows are P3's by the Template and Rules default ruling, the rule rows and the decision log are P7's, and the harness owns no table and writes no row. The harness reads every row through the owner's contract and never from a schema, and it writes nothing: the values it asserts enter through the owners' load and approval operations. Every key in the run is synthetic and no field in the table carries personal data.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The timer projection: `expires_at`, `warn_at`, the status and the rule version of each timer (AC1, AC2, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state, the stage code and the rule version behind the clock (AC1, AC2, AC3, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a load or an approval (AC3, AC4) |
| POST | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision | Creates the version of the service-level file, with one Idempotency-Key (AC1, AC4) |
| POST | `/api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` | P7 rwb-decision | Puts the version in force from its valid-from date, or refuses it (AC1, AC2, AC3, AC4, AC5) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision record of each approval, with its rule id, rule version and ledger confirmation (AC4, AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), and no operation is invented in this story: each path is the owner's published operation in the Ownership Map. The service-level values and the state codes travel through the P3 parameter and reference-data contracts (DP-06, DP-07) and are written by P3's own load operations, never by the harness; the run asserts them where they take effect, in the timer projection and in the case read, and confirms the single copy against the parameter and reference reads of AC6 rather than by re-reading a schema. Where a screen would compose these calls the path is the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | rwb-decision, through the local decision-record library (DP-03) | Counts exactly one publication per approval, and none for the refused and the failed approval (AC4, AC5) |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 rwb-case | Observed by count only, to show that a version change raises no breach of its own: the run asserts zero publications for the configuration steps and asserts no breach behaviour, which is RWB-ITG-E1028-ITG's (AC2) |

The harness subscribes to the two topics under one consumer group of its own and counts publications; it replays nothing, because the approval paths it exercises are single-shot and a replay would test P7's inbox rather than the configuration effect. The three other events of the legacy key — the warning, the breach escalation and the catch-up — are not asserted here and their behaviour stays with RWB-ITG-E1028-ITG.

#### 12.5 Workflows and activities

None added. The harness observes `CaseWorkflow` on the task queue `rwb-case`, the parent that starts and holds the durable SERVICE_LEVEL timer for a case and reads the service-level values at the start of the timer, and whose child-per-stage shape is Architecture v5 slide 25 and Temporal design slide 13. The timer is read through the P3 projection and never from the workflow's history, so the run asserts the effect and not the execution. Of the four steps of the workflow loop — receive, `EvaluateRules`, `RecordAndApply`, wait — this story observes the wait: the durable timer that the approved value produced. No workflow, activity, worker or Schedule is created, changed or owned here.

#### 12.6 Schedules

None added. JOB-05 and its five-minute Quartz timer check are retired (Architecture v5 slide 44), so there is no job to start, stop or time in this run: the clock is inside the workflow and the configuration effect is read from the projection. The harness moves no schedule and asserts no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): recovery_case and timer are P3's, parameter_catalog, parameter_value, reference_version and reference_row are P3's by the default ruling, and rule_row and decision_log_entry are P7's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | The five synthetic cases with their state, stage code and rule version; the timer projection with `expires_at`, `warn_at`, status RUNNING and the rule version, computed from the version the stub is told is in force |
| Stub for rwb-access | `GET /me/session` | Allows `RW-RISK` with Rules and parameters A and `RW-COE` with Rules and parameters C; refuses `RW-OFF` with 403 and MSG-P4-002 |
| Stub for rwb-decision | `POST /admin/rule-versions`, `POST /admin/rule-versions/{versionId}/approve`, `GET /decision-log` | Creates a version as VALIDATED once per Idempotency-Key, approves it from its valid-from date, answers MSG-P7-003 when the record write is forced to fail, and answers one ledger entry per approval with its rule id, rule version, chain sequence and hash |
| Service-level fixture | The load layout of the service-level file, the warning layout, the state code, the allowed time, the warning point and the valid-from dates | Version 3 with `LIT_PACK` at 10 working days and a warning at 8, valid from 2027-06-15; version 4 with the allowed time and warning held as data and valid from 2027-06-21; versions 5 to 7 for the refused, the failed and the invalid-state cases; the state code list |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The load layout of the service-level file and its warning layout, the name of the valid-from parameter, the exact fields of the timer projection, the message a refused load answers, and the rule that decides when a running timer is recomputed are Not specified in the source documents (GAP-0439; ASM-0631).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.decision-record.DecisionRecorded.v1` counted per approval and `rwb.case.TimerBreached.v1` observed at zero for the configuration steps |
| Temporal | None added; `CaseWorkflow` on `rwb-case` observed as the holder of the durable timer the approved value produced |
| File | None. The service-level file is loaded as data through the owners' contracts; no file is transferred, parsed or archived by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03, DP-06, DP-07 and DP-19 each add one platform H story — RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON — delivered by the platform wave, so they are not repeated in the metadata H row of this story, which stays None. The two C dependencies DP-06 and DP-07 add are P3 contract stories the harness builds against with their fakes, so they never block. DP-13 adds nothing. DP-05 is carried because the legacy key reaches account data behind the case; this run opens no ACE view and calls no source-data operation, so the pattern is applied by the owners and appears here only so the split is complete. The blocking dependencies are the two I stories, RWB-P3-E1028-APP and RWB-P4-AD015-APP, which replace their stubs; until they land the run uses the stub and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| ServiceLevelLoadDriver | Service | Loads the service-level version through the P3 parameter and reference-data contracts and the P7 rule-version operation, one Idempotency-Key per load, and holds the fixture's state code, allowed time, warning point and valid-from dates as data |
| ParameterReadProbe | Service | Reads the state code, the allowed time, the warning point and the valid-from date back through the P3 contracts, and asserts one copy and the refusal of a state code the reference list does not hold |
| TimerProbe | Service | Reads the timer projection for every case, records `expires_at`, `warn_at`, status and the rule version stamp, and compares two reads field for field |
| ApprovalProbe | Service | Drives the rule-version approval as `RW-RISK`, records the status and the valid-from date, and drives the refused and the forced-failure approvals |
| DecisionProbe | Service | Reads the decision log and asserts one entry per approval with its rule id, rule version, chain sequence and hash, and no entry for a refused or failed one |
| EventObserver | Service | Subscribes to `rwb.decision-record.v1` and `rwb.case.events.v1`, counts publications per approval and holds the zero-breach assertion of the configuration steps |
| StubSet | Fake | The three stubs and the service-level fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per run keyed by story and case_no, with the baseline and the post-approval read side by side, the contract version of each hop, whether the hop was a stub or the owner, and the gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-P3-E1028-APP and RWB-P4-AD015-APP land, on cases `RW-2027-000801`, `RW-2027-000803`, `RW-2027-000805`, `RW-2027-000806` and `RW-2027-000809`, the approver `RW-RISK`, the loader `RW-COE`, the refused caller `RW-OFF`, business date 2027-06-14 and versions 3 to 7 of the service-level file. The harness seeds nothing by hand, never writes a schema row, and never approves with a borrowed right. The load layout of the service-level file and its warning layout, the name of the valid-from parameter, the exact fields of the timer projection, the message a refused load answers, and the rule that decides when a running timer is recomputed are Not specified in the source documents (GAP-0439; ASM-0631).

**Build steps**

1. Generate the three stubs and the service-level fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X9).
2. Build the ServiceLevelLoadDriver and load version "3" through the P3 parameter and reference-data contracts, asserting VALIDATED and not in force (AC1, X4).
3. Add the ApprovalProbe for `RW-RISK` and `RW-COE` and approve version "3", asserting APPROVED from 2027-06-15 and the refused load and approval for `RW-OFF` (AC1, AC3).
4. Add the TimerProbe for AC1: the projection of case `RW-2027-000801` carries `expires_at` 2027-06-29 09:00, `warn_at` 2027-06-25 09:00 and version "3", and case `RW-2027-000805` does not name version "3" (X8).
5. Add the baseline read of case `RW-2027-000803`, approve version "4", and compare the two projections field for field, asserting the unchanged `expires_at` and the unchanged version stamp (AC2, X6).
6. Add the new-timer case `RW-2027-000806` and assert its due date is the one version "4" produces from the fixture values (AC2).
7. Add the DecisionProbe and the EventObserver for AC4: one entry per approval with its rule id, rule version, chain sequence and hash, and exactly one `rwb.decision-record.DecisionRecorded.v1`.
8. Add the forced decision-record failure for AC5, asserting MSG-P7-003, no entry, no event and the version left out of force (X5).
9. Add the ParameterReadProbe for AC6: the single copy, the version stamp beside the projection, and the refusal of a state code the reference list does not hold (X2).
10. Add the EvidenceReport gate and the zero-breach assertion, then swap each stub for the owning service as its I story lands, reporting a stub pass as a stub pass.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P3-E1028-APP and RWB-P4-AD015-APP when they land, and the wave entry check holds a run report keyed by story and case_no with the baseline and the post-approval timer read side by side and the version stamp on each.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Error | Enter {field}. |

The harness asserts the message ID and the substituted values on the answer it reads and owns no message text. MSG-P4-002 is asserted with the refused approval for a caller without Rules and parameters A (step 11, AC3) and with the refused load for a caller without Rules and parameters C (X4). MSG-P7-003 is asserted when the decision record cannot be written and the version is left out of force (step 11, AC5). MSG-GEN-001 is asserted with the missing field name when a version is loaded without its valid-from date (X1). The message ID for a service-level row that is missing or invalid — a state code the reference list does not hold, or a row with no allowed time — is not published in the source documents (GAP-0439; ASM-0631), so that path is asserted on the refusal and the absence of a version, never on a message string.

### 15. Screens and states

The legacy story's screens are SCR-42 Queues and service levels (versions; load) and SCR-39 Rules and parameters (versions; load; approval), and neither is built or rendered here: the harness calls the operations behind them and reads the states through the owners. Both are gateway-bff composite routes over the calls of §12.2 (DP-19), and no screen, route or user-interface element is created, changed or tested by this story.

| State | Read through | What the run asserts |
|---|---|---|
| Version VALIDATED | rwb-decision approval answer and the case read | The version is loaded and is not in force, so no timer can name it |
| Version APPROVED, in force from its date | rwb-decision approval answer and the decision log | The version carries its valid-from date and its rule id, and one record confirms the approval |
| Version refused | rwb-access session read and the approval answer | 403 with MSG-P4-002, or MSG-P7-003 when the record cannot be written, and the version is not in force |
| Timer RUNNING under version "3" | rwb-case timers read | `expires_at` and `warn_at` from the approved values, with version "3" named on the timer |
| Timer RUNNING across a version change | rwb-case timers read, before and after | The projection is identical field for field and the version stamp does not change |
| Timer RUNNING under version "4" | rwb-case timers read | A timer started after the valid-from date carries the due date version "4" produces |
| A load with an unknown state code | P3 parameter and reference-data answer | The load is refused and no version exists to approve |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-015-01-ITG | AC1 | End to end | Version "3" loaded and approved as `RW-RISK`, the timer of case `RW-2027-000801` read with 2027-06-29 09:00 and 2027-06-25 09:00 and version "3", and case `RW-2027-000805` read without the version stamp |
| TC-AD-015-02-ITG | AC2 | Integration | Case `RW-2027-000803` read before and after version "4" takes effect, compared field for field, and case `RW-2027-000806` read under version "4" with the fixture's values |
| TC-AD-015-03-ITG | AC3 | Component | A synthetic caller `RW-OFF` without Rules and parameters A, the approval refused with 403 and MSG-P4-002, and case `RW-2027-000809` still served by the version in force |
| TC-AD-015-04-ITG | AC4, AC5 | Integration | One approval with its rule id, rule version, chain sequence and hash and one event, then a forced decision-record failure with MSG-P7-003, no entry, no event and the version out of force |

The legacy test cases TC-AD-015-01 to TC-AD-015-04 are kept as the `-ITG` copies above, with their legacy Covers: AC1 for TC-AD-015-01, AC2 for TC-AD-015-02, Access for TC-AD-015-03 and Principle 5 for TC-AD-015-04. The full legacy tests, with their Given, When and Then, are in the legacy test case workbook under the same legacy IDs. The legacy AC1 and AC2 stay the build criteria of RWB-P4-AD015-APP; the `-ITG` copies assert the same behaviour across the service boundary, and AC6 has no legacy test case of its own in this key, so it is asserted with the parameter and reference reads of TC-AD-015-01-ITG and the refusal step of TC-AD-015-04-ITG.

### 17. Guardrails

- No business value in code: the state code, the allowed time, the warning point, the valid-from dates, the case and user keys, the version numbers and the report layout are data held in the fixture.
- No personal data in logs, events or reports: every key is synthetic, the events carry IDs and facts only, and no case field that carries personal data is read.
- The values are read through the P3 parameter and reference-data contracts and the clock through the P3 projection; no service's schema is read, no view is opened, and no second copy of a service level is allowed to exist (DP-01, DP-06, DP-07).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- No invented operation: only the six calls of §12.2, and the load and the approval are never asserted through a read the map does not publish.
- The approval is made as the right holder `RW-RISK` and never with a service identity; a harness that borrowed a service right would prove nothing about MSG-P4-002.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, never writes a version row by hand, and never sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script, and a version that retimes a running clock is a failure and not a variant.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-015 Configure service levels and timers | Recovery Workbench Administration Stories v4, lines 1220 to 1300 | Sections 1, 2, 3, 11, 14 and 19 of this file |
| Legacy AC1, the service level loaded and new timers using it | The same, lines 1239 to 1242 | Section 7, AC1; the legacy criterion itself stays with RWB-P4-AD015-APP |
| Legacy AC2, a running timer keeping its due date | The same, lines 1244 to 1247 | Section 7, AC2 |
| Legacy test cases TC-AD-015-01 to TC-AD-015-04, with Covers AC1, AC2, Access and Principle 5 | The same, lines 1291 to 1296 | Copied as `-ITG` in section 16 |
| Legacy data entities and field IDs: recovery_case, timer, rule_row | The same, lines 1250 to 1256 | Section 11 |
| Legacy endpoints, screens and permission checks | The same, lines 1258 to 1277 | Sections 12.2, 15 and 10 |
| Legacy messages MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001 and MSG-P7-003 | The same, lines 1279 to 1287 | Section 14, the three this run asserts |
| DL22, service levels per case state loaded as parameters | Decision Log v11, the DL22 row | Section 8, BR1 and BR2 |
| The P3 service table row, the timer and the projection | Architecture v5 slides 14 and 41, text extract lines 984, 1035 and 2880 | Sections 2, 11 and 12.2 |
| `TimerDue` retired and `TimerBreached` living in the workflow's service | Architecture v5 slide 42, text extract lines 2930 and 2931 | Sections 2, 12.4 and 12.6 |
| JOB-05 retired in favour of durable timers | Architecture v5 slide 44, text extract line 2981 | Sections 2, 8 and 12.6 |
| `RulePackageInForce` as a cache-refresh event at the gateway | Architecture v5 slide 20, text extract lines 1473 to 1479 | Section 2 |
| The four workflow steps and `RecordAndApply` writing the record and the change in one transaction | Temporal and Drools design slides 13 and 15, text extract lines 611 to 632 and 746 | Sections 8, 12.5 and 12.8 |
| "Stage clock paused; prescription never" and the pause boundary | Temporal and Drools design slide 24, text extract lines 1644 to 1657 | Section 19, as the behaviour this story does not own |
| The `timer` projection ruling and the rule-row ruling | Ownership Map v1 table rows for timer, rule_row, parameter_catalog, parameter_value, reference_version, reference_row and decision_log_entry | Sections 2, 11 and 12.7; ASM-0078 and ASM-0069 |
| The four P7 and one P4 published paths, and the P3 timer and case reads | Ownership Map v1 API rows for `GET /cases/{caseId}/timers`, `GET /cases/{caseId}`, `GET /me/session`, `POST /admin/rule-versions`, `POST /admin/rule-versions/{versionId}/approve` and `GET /decision-log` | Section 12.2 |
| DP-03, DP-05, DP-06, DP-07, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application, and the metadata Patterns applied row |
| ADR-020 and ADR-022 | Architecture Decision Records v4, with ADR-020 and ADR-022 as added by Template and Rules v1 §R8.4 | Sections 8, 12.2 and 12.4: contract-first REST with one hop and 2 s, and local decision record plus central ledger |
| GAP-0439 and ASM-0631 | This run's gap and assumption registers | Sections 2, 3, 5, 7, 12.8, 13 and 14 |
| Release 30 June 2027 | The legacy story header, line 1224, copied unchanged and marked tentative | The metadata Release row and section 19 |

### 19. Out of scope

- RWB-P3-E1028-APP: the durable timer, the timer projection, the warning, the breach, the catch-up, the pause and resume, and the prescription calculator. This story reads the projection and builds none of it.
- RWB-P4-AD015-CON and RWB-P4-AD015-APP: the load, the service-level file, the two rights and their refusals, the governed approval screen behind SCR-39 and SCR-42, and the two legacy acceptance criteria.
- The timer mechanics, the warning at its point, the breach and its escalation, the catch-up after a worker outage, the pause and resume, and the prescription date: all of it is RWB-ITG-E1028-ITG on the same wave and is not restated, built or asserted here.
- The rule-version load and approval build (RWB-P4-AD012-APP), the rollback of a version (RWB-P4-AD013-APP), the reference-data load and approval (RWB-P4-AD009-APP and RWB-P4-AD010-APP) and the ledger read build (RWB-P7-E2005-APP): consumed through the published contracts only.
- The platform stories the patterns add, including RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON.
- SCR-42 Queues and service levels and SCR-39 Rules and parameters, and every gateway-bff composite route: no screen, route or user-interface element is built or tested.
- The queue configuration of RWB-ITG-AD014-ITG and the interface and job monitor of RWB-ITG-AD018-ITG: the same seam, different stories.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag, parameter value or configuration in any service. The harness runs in SIT with synthetic data and release 30 June 2027 stays tentative.
