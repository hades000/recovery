# RWB-S9-E7014-APP Issue a notice on a missed target

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-P |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E7014-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S9-E7014-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the notice slice of RWB-E7-014 in rwb-partner. The legacy criterion AC2 is kept word for word with its origin tag; the step reads the partner and its latest score, compares it with the target in reference data, sets the panel status to `ON_NOTICE`, requests the contractual notice from rwb-comms (which owns the `notice` row), writes the local decision record with the rule ID and the version in force before any change (DP-03), and is submitted on the published `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1` (DP-13), reached from SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19). No source owns the notice in S9 (FSD S9 T5.2 gives notices to P6), no rule row decides a missed target, no source gives the cure period a length or the target a threshold, and EV-21 is published in TSD S9 T5.3 while the event catalogue reads it as consumed (GAP-3127; ASM-5450, ASM-5451, ASM-5452, ASM-5453, ASM-5454, ASM-5459). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 14 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **to send the contractual notice when a partner misses its targets, and to start the cure period**, so that **partners are placed, paid and measured by rule**.

This is the notice slice of legacy RWB-E7-014. It owns:

- the legacy criterion this story owns (AC2), copied with its origin tag and with the term decision log changed to decision record, and the messages and the screens it depends on;
- one step of `InstructionWorkflow` on task queue `rwb-partner`, the notice step of the partner panel;
- the reading of the partner row (DF-PRT-001 to DF-PRT-007) and of its latest score (DF-PRT-007) against the target held as reference data, both with their version;
- the setting of the panel status to `ON_NOTICE` (LOV-PANEL) on the partner row, and the audit columns of the update;
- the request for the contractual notice through the rwb-comms contract, which owns the `notice` row and its dispatch (FSD S9 T5.2);
- the local decision record written through RWB-PLT-E1027-CON with the rule ID, the version in force, the score, the target, the notice reference and the from and to panel status, **before any change** (DP-03);
- the submission of the notice on the published `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1`, partner portal right C, scope applied (DP-13);
- the partner panel read on SCR-34 Partner list and SCR-35 Placement and allocation behind the gateway-bff composite route (DP-19).

It does not own: the published shapes, the elements, the lists, the rights of the document, the error envelope and the fakes, which are RWB-S9-E7014-CON; the scorecard that measures the partner (FEAT-PRM-08, RWB-S9-E7011-APP); the panel, the fee schedule and the service levels as versioned reference data (FEAT-PRM-02, RWB-S9-E6030); the allocation and its override (RWB-S9-E6031, RWB-S9-E6032); the partner result (RWB-S9-E6033); the fee approval (RWB-S9-E7012); the partner review (RWB-S9-E7013); ending the contract and recalling the work (FEAT-PRM-12, RWB-S9-E7015); the conduct check (RWB-S9-E7016); the notice document, its template and its dispatch, which are rwb-comms (P6); the case, its states and its clock, which are rwb-case (P3); and the cross-service journey of AC1, which is RWB-ITG-E7014-ITG.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: the notice is sent when a partner misses its targets and the cure period starts, because partners are instructed and paid by email and spreadsheet and allocation is not based on performance (FSD S9 A1.3, A2.11.1), and placements by scorecard are measured on the decision log and the Workbench records against 100 percent set with DL22, reviewed monthly (FSD S9 A2.11.1). What D-RCV-60 changes is who owns the notice, the panel, the rule, the record and the screen.

- **The notice is not this service's row.** FSD S9 T5.2 gives notices to P6, the event catalogue gives `NoticeGenerated` and `NoticeDispatched` to Communications (EV-13, EV-14), and the ownership rows give S9 three tables, none of them a notice. The legacy Data table's `notice` (DF-LEG-015 to DF-LEG-023) is therefore read as rwb-comms' element, requested through its contract, and never written here (ASM-5450).
- **The panel status is this service's.** `partner` is S9's in `rwb_partner` (context pack ownership rows; TSD S9 T3.1) and LOV-PANEL already carries `ON_NOTICE`, so the notice's own effect on this service is the panel status of the partner row and the audit columns (ASM-5455).
- **No rule row decides the notice.** The Business Rules and Routing Logic v4 has no partner route set: the nearest rows are R-UNI-25 to R-UNI-29, which recall work on a missed service level, a panel exit, a conflict, insolvency or a conduct breach, and none of them issues a notice or starts a cure period. The rule ID and the version in force the record must carry have no row to cite and carry the placeholder (ASM-5451).
- **The cure period has no length.** A cure-period field exists for a broken treatment plan (R-RES-27 to R-RES-29) and no partner parameter of that kind exists; the FSD names the cure period as an effect of the notice and gives it no length, no list and no parameter (ASM-5452).
- **The measure has no threshold.** `partner.score` is the latest scorecard result (DF-PRT-007) and the targets and incentives are kept as versioned reference data (FEAT-PRM-02, REQ-S9-001), but no target value, no measure and no threshold for a missed target is published (ASM-5459).
- **The instruction surface carries the act.** The legacy endpoint table of RWB-E7-014 gives `POST /cases/{caseId}/instructions` and `GET /partner/instructions`, TSD S9 T-A.1 publishes them as API-S9-002 and API-S9-003, and no notice path is published by any source, so the notice is submitted on the instruction operation and carries the placeholder for the request property the notice facts would use (ASM-5453).
- **Events are not this step's.** The service owns EV-20 and EV-21 only: an instruction issued and a partner result. A notice is a Communications fact, its dispatch is EV-14, and this step publishes nothing (ASM-5454).
- **No requirement row names the feature.** TSD S9 T8 maps every REQ-S9 row to FEAT-PRM-01 or FEAT-PRM-08, and REQ-S9-001 is the only row that names notice and exit at the level of the six points, so the story cites no requirement ID until the E7 BRD and the PRD publish one (ASM-5458).

No business value moves: the panel list, the partner type list, the target, the cure period, the rule ID and its version are reference data and rule values, read with their version and never written in code.

### 3. Preconditions

- RWB-S9-E7014-CON is published: the instruction operations on `/api/recovery/partner/v1`, the partner and instruction elements, the lists, the rights, the error envelope, the consumed rows and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision record is written in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in schema `rwb_partner` from the DB story of this service, with the columns of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- The partner is on the panel at `ACTIVE` with a contract that has not ended, and its latest score (DF-PRT-007) is published by the scorecard of FEAT-PRM-08 (RWB-S9-E7011-APP).
- The target the score is measured against and the cure period are in force as reference data with their version. The parameter names, the values and the read are Not specified in the source documents (GAP-3127; ASM-5452, ASM-5459).
- The rwb-comms notice contract is published with its fake and answers a notice reference for a partner notice. Its operation name and the notice's property for a partner are Not specified in the source documents (GAP-3127; ASM-5450, ASM-5453).
- The service runs as its own login on schema `rwb_partner`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_comms` or an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7014-CON when its tests pass.

### 4. Flow

1. The scorecard of FEAT-PRM-08 publishes the partner's latest score on `partner.score` (DF-PRT-007) against the target in reference data; the manager reads the panel on SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route, one hop (DP-19).
2. The partner and agency manager selects a partner whose score is below its target, confirms the missed target and the notice, and the screen sends the partner reference, the case reference, the instruction type, the due date and the manager's identity.
3. `PartnerInstructionController` serves `POST /cases/{caseId}/instructions` (API-S9-002) on base `/api/recovery/partner/v1`, declares partner portal right C with the scope applied, requires the `Idempotency-Key` header and validates the request (DP-13).
4. The step reads the partner row in `rwb_partner`: its reference, its panel status, its contract end and its latest score. A partner at `SUSPENDED` or `EXITED`, a contract that has ended, or a partner already at `ON_NOTICE` is refused and nothing is written (X3).
5. The step reads the target and the cure period from reference data at their version in force and holds the pair for the record. The parameter names and the values carry the placeholder (ASM-5452, ASM-5459).
6. `PartnerNoticeDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the partner reference, the case reference, the rule ID and the version in force, the score, the target, the notice type, the from panel status and `ON_NOTICE`, and the decided-at time. A failed write stops the step with nothing changed (DP-03; AC2).
7. `NoticeClient` requests the contractual notice from rwb-comms with its type, the partner and the case, one hop, a 2 s budget and a breaker; rwb-comms answers the notice reference and owns the row, its template and its dispatch (ASM-5450).
8. `RecordAndApply` commits in one transaction: `partner.panel_status = ON_NOTICE` (DF-PRT-005), the standard columns `updated_at` and `updated_by`, and the optimistic-lock version. The record written at step 6 is void if this commit does not happen, so no record exists without a change (DP-03).
9. The answer returns the instruction element with the notice reference, the from and to panel status and the decision-record reference; the manager sees the partner at `ON_NOTICE` on SCR-34, read back from this service.
10. The cure period starts at the notice's `sent_date`; its length is reference data and its expiry is tracked by the case stage's timer in P3, which owns `timer`. This service holds no timer and starts no Schedule (ASM-5452).
11. No event is published: the notice's own facts are rwb-comms' (`NoticeGenerated` EV-13, `NoticeDispatched` EV-14) and the instruction's `InstructionIssued` (EV-20) belongs to the instruction stories.
12. A repeat of the same submission with the same `Idempotency-Key` answers the instruction and the notice that exist and writes no second record; no phone number, address, identity number or other personal value is copied into the record, the answer or a log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: the panel status stays where it was, no notice is requested and no record exists | MSG-P7-003 | AC2, TC-E7-014-02, TC-E7-014-04 |
| X2 | The role does not hold partner portal right C | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC3, TC-E7-014-03, TC-E7-014-07 |
| X3 | The partner is at `SUSPENDED` or `EXITED`, its contract has ended, or it is already at `ON_NOTICE` | 409 with nothing written; a notice is never issued twice and never to a partner off the panel | Not specified in the source documents (GAP-3127; ASM-5455) | AC2 |
| X4 | The target or the cure period is absent from reference data at its version | 422 or 503 with nothing written; the step never falls back to a value of the code | MSG-GEN-001 | Section 17, BR7, AC4, TC-E7-014-08 |
| X5 | The rwb-comms notice request does not answer inside 2 s, or its breaker is open | The transaction rolls back, the activity retries on the workflow's schedule under the same `Idempotency-Key`, and nothing is committed | None | BR4, AC5, TC-E7-014-09 |
| X6 | The same submission arrives twice | One instruction, one notice and one record; the repeat answers what exists | None | BR10, AC6, TC-E7-014-10 |
| X7 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` or `timer` row, a `notice` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6, AC7, TC-E7-014-11 |

X1 and X2 are the legacy exception paths, carried onto the slice with the legacy messages; X3 to X6 are the paths the trigger, the reference data and the two contracts add; X7 is the ACE, notice and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7014-CON, the rwb-comms notice fake, the reference-data fake and the decision-record stub, on its own schema, and needs no live P3 or P6 |
| Negotiable | The activity and component names, the internal record shape and the front-end placement are this story's and the baseline's choice; the operation, the right, the panel list, the messages and the criterion are fixed |
| Valuable | A partner that misses its target receives one dated contractual notice and starts a cure period, and the panel change is provable from the decision record instead of an e-mail |
| Estimable | One workflow step, one comparator against reference data, one record write, one notice request, one operation branch, one client and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | AC2 runs on the decision-record stub; the step runs on a synthetic partner at `ACTIVE` through the fakes, plus the refused, not-in-force, no-answer and repeat cases |

### 7. Acceptance criteria

```gherkin
Feature: Issue a notice on a missed target

  Background:
    Given the partner "PRT-0007" of type "AGENCY" is on the panel at state "ACTIVE" with its contract in force and its latest score published
    Given the target and the cure period are in force as reference data with their version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-014 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without partner portal right C (X2) (new, D-RCV-60)
    Given the user's role does not hold partner portal right C
    When the notice is requested
    Then the request is refused with 403 before any read or write, nothing changes, no record is written and the user sees MSG-P4-002

  Scenario: AC4 Target or cure period absent at its version (X4) (new, D-RCV-60)
    Given the target or the cure period is absent from reference data at its version
    When the notice is requested
    Then the request is refused with 422 or 503, nothing is written and the user sees MSG-GEN-001

  Scenario: AC5 rwb-comms does not answer inside 2 s (X5) (new, D-RCV-60)
    Given the rwb-comms notice request does not answer inside 2 s or its breaker is open
    When the action is taken
    Then the transaction rolls back, nothing is committed and the activity retries under the same Idempotency-Key

  Scenario: AC6 Same submission twice (X6) (new, D-RCV-60)
    Given the same submission arrives twice
    When the action is taken
    Then one instruction, one notice and one record exist and the repeat answers what exists

  Scenario: AC7 Statement outside the boundary (X7) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case or timer row, a notice row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC8 Business rules BR1 to BR11 covered (section 8) (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8 are in force
    When the story is verified
    Then each rule has a test row listed in the rule coverage line of section 8

  Scenario: AC9 Error answers of the provided operations (new, D-RCV-60)
    Given a provided operation is called without a valid credential, by a role without the right, or for a resource that does not exist
    When the call is made
    Then the answer is 401, 403 or 404 respectively and nothing is written

  Scenario: AC10 Replay of a write with the same Idempotency-Key (new, D-RCV-60)
    Given the same write is sent again with the same Idempotency-Key
    When the action is taken
    Then the repeat answers the stored result and no second instruction, notice or record is written

  Scenario: AC11 Activity retried or timed out (new, D-RCV-60)
    Given the issuePartnerNotice activity is retried or times out
    When the action is taken
    Then the notice is issued once under the same Idempotency-Key and one record exists

  Scenario: AC12 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed contract call fails or does not answer
    When the action is taken
    Then the transaction rolls back and nothing is committed

  Scenario: AC13 Status change not allowed by the model (new, D-RCV-60)
    Given a status change the status model does not allow is requested
    When the action is taken
    Then the change is refused and nothing is written
```

AC2 is the legacy criterion of RWB-E7-014 with its origin tag added; the only term changed is `decision log`, now `decision record`, and the rest of the wording (`the action is taken` and the single `Then`) stands. AC2 has no cross-service part that could be mocked, so no `Given the <service> contract mock returns <x>` line is added to it and the notice, the reference data and the record are reached at the level the criterion names.

The other legacy criterion of RWB-E7-014 is AC1, and it is not owned by this story: the split plan gives AC1 to RWB-ITG-E7014-ITG, which runs the journey across the partner panel, the notice and the case, and it is not restated here. The step this story builds is the one AC1 describes, so the business outcome is proved by TC-E7-014-01 at component level until the integration story runs it end to end. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

**Rule coverage.** BR1 TC-E7-014-06; BR2 AC2, TC-E7-014-02, TC-E7-014-04; BR3 TC-E7-014-12; BR4 AC5, TC-E7-014-05, TC-E7-014-09; BR5 AC7, TC-E7-014-06, TC-E7-014-11; BR6 AC7, TC-E7-014-11; BR7 AC4, TC-E7-014-08; BR8 TC-E7-014-13; BR9 TC-E7-014-11; BR10 AC6, TC-E7-014-10; BR11 TC-E7-014-05.

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice step is a step of `InstructionWorkflow` on `rwb-partner`: it reads `partner` and `partner_instruction`, writes `partner.panel_status` and the audit columns, and writes nothing else in `rwb_partner` | TSD S9 T3.0, T3.1, T4; context pack ownership rows (3 tables, 1 workflow, no job); FSD S9 A2.11.2 |
| BR2 | The result is recorded before the change, with the rule ID, the version in force, the score, the target, the notice reference and the from and to panel status; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S9 T2 ("writes the decision log entry before any change"); legacy AC2 |
| BR3 | A notice is issued only to a partner at `ACTIVE` with a contract in force and a score below its target; a partner at `ON_NOTICE`, `SUSPENDED` or `EXITED`, or a contract that has ended, is refused | TSD S9 T3.2 (LOV-PANEL); ASM-5455; legacy AC1 |
| BR4 | The notice is a rwb-comms element, requested on one hop with a 2 s budget and a breaker; this service holds no notice row, no notice template and no dispatch status | FSD S9 T5.2; Event and Messaging Design v5 events EV-13 and EV-14; ASM-5450 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of other services' facts | DP-01; TSD S9 T3.3 |
| BR6 | The service reads no `v_ace_*` view and holds no grant on one; ACE data reaches the panel only through rwb-source-data or the owner's contract | DP-01, DP-05; Template and Rules §R7.2 (s17) |
| BR7 | Every value a business person may change is reference data or a rule value read with its version: the panel list, the partner type list, the target, the cure period and the rule in force. The target, the cure period and the rule ID have no published row and carry the placeholder | FSD S9 BR-S9-011; ASM-5451, ASM-5452, ASM-5459 |
| BR8 | No personal data in `rwb_partner`, the decision record, a log or a workflow input: partner identifiers, codes, list values, dates, an amount, a rule ID and a version only | Template and Rules §R7.2 (s17); TSD S9 T6.2 |
| BR9 | The cure period starts at the notice's `sent_date`; its length is reference data, its expiry is the case stage's timer in P3 and this service starts no Schedule and holds no timer row | ASM-5452; TSD S9 T4; context pack ownership rows (jobs: None) |
| BR10 | The same submission twice writes one record, one instruction and one notice: the operation declares the `Idempotency-Key` header and stores the key and its answer | TSD S9 T-A.2 |
| BR11 | This step publishes and consumes no event; the partner result (EV-21) and the instruction (EV-20) belong to other steps of the service | Event and Messaging Design v5 events EV-20 and EV-21; TSD S9 T5.3; ASM-5454 |

### 9. State transitions

| From (panel status, rwb-partner) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `ACTIVE` | The contractual notice is issued and the record is written | The score is below the target and the contract is in force | `ON_NOTICE` | rwb-partner, by this story (ASM-5455) |
| `ON_NOTICE` | A further notice request | The partner is already on notice | `ON_NOTICE`, unchanged | none; 409 (X3) |
| `ON_NOTICE` | The cure period is met | The targets are met again inside the cure period | `ACTIVE` | Not specified in the source documents (GAP-3127; ASM-5455) |
| `ON_NOTICE` | The cure period lapses | The targets are not met inside the cure period | `SUSPENDED` | Not specified in the source documents (GAP-3127; ASM-5455) |
| `ON_NOTICE` | The contract ends, or a conduct breach is upheld | FEAT-PRM-12 or FEAT-PRM-13 applies | `SUSPENDED` or `EXITED` | RWB-S9-E7015-APP and RWB-S9-E7016-APP, not this story |
| `SUSPENDED`, `EXITED` | A notice request | The partner is off the panel | Unchanged | none; 409 (X3) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A notice submission | The partner, the target and the cure period are read | Evaluating |
| Evaluating | The score is below the target | The partner is at `ACTIVE` with a contract in force | Recording |
| Evaluating | The partner is off the panel or already on notice | X3 | Waiting, nothing changed |
| Recording | The record and the panel status commit | The notice reference is held and the transaction commits | Waiting for the next submission |
| Recording | The record, the notice call or the commit fails | X1, X5 | Waiting, nothing changed |

LOV-PANEL is `ACTIVE`, `ON_NOTICE`, `SUSPENDED` and `EXITED` (TSD S9 T3.2). This story writes `ON_NOTICE` only; the two exits from `ON_NOTICE` — back to `ACTIVE` when the cure is met and to `SUSPENDED` when it lapses — have no trigger, no rule row and no story in any source, so they carry the placeholder and are not built here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: the primary role of FSD S9 A2.11.3.3, issuing the notice with right C |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Partner portal CRU in TSD S9 T6.1: right C, the six further roles the legacy permission table names with right C |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R in TSD S9 T6.1: read only and refused the notice; they are part of the legacy "and 21 more" (ASM-5456) |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal RU in TSD S9 T6.1: the partner's own users read their instructions and hold no right C, so a partner never issues its own notice |
| rwb-partner service identity | Reads the partner and the reference data, writes the record and the panel status and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and T-A.1 and nothing wider: the seven identities that hold C are exactly the seven the legacy permission table names, and the 29 identities of the Partner portal column all hold R, which is the legacy "and 21 more" (ASM-5456). DP-08 is not in this story's pattern set, but the rwb-access authorise check is named here: each operation calls the authorise check of rwb-access for the capability area "Partner portal" and the right it declares (C for the notice, R for the reads), and the access guard of the service template applies it, so the check is stated here and built by the template.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Read, the partner reference the operation takes and the record cites |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partner_code | Read, the partner code the notice names |
| DF-PRT-003 | partner (S9, `rwb_partner`) | partner_name | Read, the registered name the notice carries |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partner_type | Read, the type over LOV-PARTNER-TYPE |
| DF-PRT-005 | partner (S9, `rwb_partner`) | panel_status | Write, the from status read and `ON_NOTICE` written (LOV-PANEL) |
| DF-PRT-006 | partner (S9, `rwb_partner`) | contract_end | Read, the contract the partner must still hold |
| DF-PRT-007 | partner (S9, `rwb_partner`) | score | Read, the latest scorecard result the target is compared with |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read the case, the partner, the type and the status the notice rides; no column is written by this step |
| Standard columns | partner (S9, `rwb_partner`) | `state`, `version`, `updated_at`, `updated_by` | Write the audit columns and guard the update with `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before anything else |
| DF-LEG-015 to DF-LEG-023 | notice (P6 rwb-comms) | id, case_id, document_id, notice_type, sent_date, barcode and three further fields the legacy table does not name | Not written here: the notice is requested on the P6 contract and this service holds its reference only |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case reference arrives on the instruction |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the cure expiry is P3's timer |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: no partner route set exists, so the rule ID and version carry the placeholder |
| the target and the cure period | reference data of the owner of FEAT-PRM-02 and of the parameters contract | The threshold the score is measured against and the length of the cure period | Read with their version; no field ID, no parameter name and no value in any source: Not specified in the source documents (GAP-3127; ASM-5452, ASM-5459) |

Field IDs are those of TSD S9 T3.1 and the Logical Data Model and Data Dictionary. **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, and the decision record and `idempotency_key` are library objects created in `rwb_partner` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry partner identifiers, codes, dates, list values, an amount, a rule ID and a version. A partner firm is a legal person: no contact name, e-mail, phone number or identity number is read into the record, the answer, a log or a workflow input, and the fixtures are synthetic.

### 12. Contract

Contract version: Not specified in the source documents (DOR-RWB-S9-E7014-APP-23); the paths in this section carry the base /api/recovery/partner/v1 only.

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the notice branch of the instruction operation, whose shape RWB-S9-E7014-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` (API-S9-002) | `InstructionRequest` in; `PartnerInstruction` out with the notice reference, the from and to panel status and the decision-record reference | Partner portal, right C, scope applied | `Idempotency-Key` header |
| GET | `/partner/instructions` (API-S9-003) | `InstructionPage` out: the instructions placed with the caller's firm with status, page and size | Partner portal, right R, scope applied | Not applicable |
| GET | `/partners` (API-S9-001) | `Partner[]` out: the panel with panel status and score, query type and status | Partner portal, right R, scope applied | Not applicable |

The errors of API-S9-002 are 401, 403 with MSG-P4-002, 404 for a case that is not in scope, 409 for a partner off the panel or already on notice, 422 with MSG-GEN-001 for a missing or unformed request, and 503. TSD S9 T-A.1 and T-A.2 publish the three operations, their requests, answers and error sets, so the surface needs no placeholder; what has no published property is the notice itself, its type value and the target, and they carry the placeholder (GAP-3127; ASM-5450, ASM-5453). API-S9-004 accept, API-S9-005 results and API-S9-006 invoices are the result and invoice stories' (RWB-S9-E6033, RWB-S9-E6035) and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The notice request (operation name Not specified in the source documents (GAP-3127; ASM-5450)) | `/api/recovery/comms/v1` | P6 rwb-comms | The contractual notice of the partner with its type, its template and its document; answers the notice reference; faked |
| The reference-data read at its version (operation name Not specified in the source documents (GAP-3127; ASM-5459)) | `/api/recovery/case/v1` | P3 rwb-case | The target, the cure period and the panel list at their version in force, per the R3 default ruling that gives parameters and reference data to rwb-case; faked |

Both rows are one hop with a 2 s timeout, a breaker per downstream and a retry governed by the workflow's own schedule (ADR-020). They are contract dependencies of class C that this story's C row does not carry, and DP-07, the reference-data pattern, is not in the pattern set of the key; the absence is recorded (GAP-3127; ASM-5450, ASM-5459).

#### 12.3 Events published

None. The service owns the topic `rwb.partner.events.v1` and its event set carries EV-20 `InstructionIssued` (`instructionId`, `partnerId`, `type`, `dueOn`, consumed by the partner portal) and EV-21 `PartnerResultSubmitted` (`instructionId`, `result`, `documents`), and both belong to the instruction and result steps of the service (Event and Messaging Design v5; TSD S9 T5.3). A notice is a Communications fact: rwb-comms publishes `NoticeGenerated` (EV-13) and `NoticeDispatched` (EV-14), and this step only requests the notice and records the panel change. It therefore declares no event, no producer group and no outbox row, and a build that publishes EV-20 or an event of its own here fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays an event is the DP-09 dependency the plan does not carry (GAP-3127; ASM-5454).

#### 12.4 Events consumed

None. The service's only consumed event is EV-21 `PartnerResultSubmitted`, which arrives from the partner portal when a firm reports a result and belongs to the result step (RWB-S9-E6033); the trigger of this step is the manager's confirmation on SCR-34 and SCR-35, and the FSD declares no background event for the feature (FSD S9 A2.11.4.4). The direction of EV-21 is itself in conflict between the event catalogue, which reads it as consumed, and TSD S9 T5.3, which lists it as published; the conflict is recorded and does not touch this step (ASM-5454). This story holds no consumer group, no subscription of its own and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner instruction; the notice step rides it | `rwb-partner` | Input: the case reference, the partner reference and the instruction; the notice request is the step's input. Workflow ID form: Not specified in the source documents (CG-ALL-12050). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-12050). |
| `issuePartnerNotice` | Activity, the one notice step | `rwb-partner` | The partner reference, the case reference, the score, the target, the cure period and the notice type in; the notice reference, the panel status and the record reference out, with the record written before the row |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The panel status and the notice reference as the stage result; the case stage, its clock and its timer are P3's and no REST row is declared for them |

The service owns one workflow and no job in the context pack's ownership rows, and TSD S9 T4 gives it no case state machine of its own. The activity name is a target design choice fixed by no source document, and the parent edge is declared, not built.

#### 12.6 Schedules

None. The notice is an officer-driven step and owns no Temporal Schedule, no Quartz row and no shared job table. The service owns no job in the context pack's ownership rows (Jobs: None), and the cure expiry of BR9 is the case stage's timer in P3, not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The panel firm, its type, its panel status, its contract end and its latest score; this story writes `panel_status` and the audit columns |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a partner on a case; read here, written by the instruction stories |
| partner_user | S9 (`rwb_partner`) | The partner's own users, owned by the service; this story neither reads nor writes it |
| decision record (PLT library object) | PLT library, created in `rwb_partner` | The local hash-linked decision record of the notice (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the instruction operation and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `notice` (P6), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `payment` (P8). No foreign key leaves the schema, and `case_id` and `partner_id` are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | A notice reference for a partner notice of the type requested, with its template and its sent date | AC2, X5, TC-E7-014-01 |
| rwb-case reference-data fake | The target, the cure period and the panel list at their version in force | AC2, X4, TC-E7-014-01 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1, TC-E7-014-02, TC-E7-014-04 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for the panel of the manager, before and after the notice | TC-E7-014-01, TC-E7-014-03 |

The fakes are test-only and are replaced by the real services in SIT. The notice operation and the reference-data read carry the placeholder until their owners confirm them (GAP-3127; ASM-5450, ASM-5459).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | API-S9-001, API-S9-002 and API-S9-003 on `/api/recovery/partner/v1`; the notice request of rwb-comms and the reference-data read of rwb-case, one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to other steps of the service; the notice's facts are rwb-comms' (EV-13, EV-14) |
| Temporal | 1 workflow and 1 activity | `InstructionWorkflow` and `issuePartnerNotice` on `rwb-partner`; the stage outcome returns to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `notice`; front end `src/modules/recovery/partner/PartnerPanel.tsx`, the fragment SCR-34 and SCR-35 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the panel status commit together or not at all, and the legacy "writes the result to the decision log with the rule version" is that record. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the instruction operation its home. DP-19 is how SCR-34 and SCR-35 reach this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-07 (the reference-data contract of rwb-case) and DP-06 (the parameters contract) are the real dependencies of the target and the cure period, DP-08 (the access guard of the template) and DP-09 (the outbox and inbox library) are real dependencies of the service, and they are recorded in the registers instead of the metadata table (GAP-3127; ASM-5459).

**Dependencies the tables add and the plan does not hold.** The plan gives this story H RWB-S9-E7014-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, and C, I and X empty. The two consumed rows of §12.2 are class C dependencies in fact: the notice request of rwb-comms and the reference-data read of rwb-case, both built against their documents and fakes on Day 1. DP-07 would add RWB-PLT-E1043-CON and RWB-P3-E1043-CON; the reference-data read is declared with the placeholder instead, so no row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` notice branch | Workflow | Receives the notice submission, reads the target and the cure period in force and reports the panel status and the notice reference to the parent |
| `issuePartnerNotice` | Activity | Reads the partner and the score, compares the score with the target, requests the notice, writes the record and the panel status and answers |
| `PartnerTargetComparator` | Service | Compares the score with the target in force and refuses a partner off the panel or already on notice; the threshold is reference data and never a constant |
| `PartnerNoticeDecisionRecordWriter` | Library adapter | Writes the record with the rule ID, the version, the score, the target, the notice reference and the two panel statuses before anything else; refuses the step when the write fails |
| `NoticeClient` | Client | The rwb-comms notice request, one hop, 2 s, breaker; holds the returned notice reference |
| `ReferenceData.java` | Client | The target, the cure period and the panel list at their version in force, one hop, 2 s |
| `PartnerInstructionController` | Controller | The notice branch of the instruction operation, the capability area and right C, the scope, the `Idempotency-Key` and the problem mapping |
| `PartnerPanel` | React component | Shows the partner, its panel status and its score on SCR-34 and SCR-35 |

**Database and migrations.** No Flyway file. `partner` and `partner_instruction` arrive with the DB story of this service, and the record and the key are library objects created in `rwb_partner` by the library's migration (DP-03). No column is added for the target, the cure period or the notice: none has a source (ASM-5452, ASM-5459).

**Configuration and reference data.**

- The panel list, the partner type list, the target and the cure period: reference data with their version, read through the owner's contract, never written in code (ASM-5452, ASM-5459).
- The rule ID and the version in force: recorded from the value in force; no partner route set exists in the Business Rules and Routing Logic v4, so the value carries the placeholder (ASM-5451).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard of the template.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the service holds no timer.
- The notice harness of RWB-ITG-E7014-ITG: the SIT base hosts, the fixture layout, the synthetic partner, instruction, case and notice keys, the stub answer shapes, the missed-target comparison against the named rule version, the evidence format and retention, and the pass or fail gate are agreed at the wave 4 entry check and recorded in the harness README, so the fixture stays data and no business value is hard-coded (GAP-0475).

**Build steps**

1. The notice branch of `InstructionWorkflow` and its input record, registered on `rwb-partner`, with the manager's confirmation as its trigger.
2. `ReferenceData.java` against its fake, with the target, the cure period, the version and the not-in-force path (X4).
3. `PartnerTargetComparator`, with the below-target path and the off-panel and already-on-notice paths (X3).
4. `PartnerNoticeDecisionRecordWriter` against the stub, with the failed-write path (AC2, X1).
5. `NoticeClient` against the rwb-comms fake, with the 2 s budget, the breaker and the no-answer path (X5).
6. `PartnerInstructionController` with the notice branch, right C, the scope, the `Idempotency-Key` and the problem mapping of the declared errors, and `PartnerPanel` through the composite route fake (X2, X6).
7. The transaction step: the record, `panel_status` and the audit columns in one commit, with the optimistic-lock version (X1, X5).
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no write to any other service's schema, and no write to a `notice` or `timer` row (X7, BR4, BR5, BR9).

**Feature flag.** `rwb.partner.notice-v1`, a flag of the platform library; off means the operation answers 503 with no write and SCR-34 hides the notice action, and the panel, allocation and result stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic partner at `ACTIVE` in SIT, the notice reference and the panel status are recorded with the target, the cure period and the version in force, a partner off the panel and an already-noticed partner are refused, a repeated submission writes once, a forced record failure changes nothing, no `recovery_case`, `notice` or `timer` row and no `v_ace_*` read exists in the build, and SCR-34 answers through the composite route.

**Open decision.** DL22 stays open with assumptions ASM-1162, ASM-1304, ASM-2217 and ASM-2569; this story does not close the decision.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element is absent or invalid, or the target and the cure period are not in force (X4) | Enter {field}. |
| MSG-P4-002 | A role without partner portal right C calls the notice (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the notice is requested (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| the refusal of X3 | The partner is at `SUSPENDED` or `EXITED`, its contract has ended, or it is already at `ON_NOTICE` | Not specified in the source documents (GAP-3127; ASM-5455) |

The three IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. The refusal of X3 has no message in any source, so it carries the placeholder and no invented text.

### 15. Screens and states

SCR-34 Partner list and SCR-35 Placement and allocation are served through the gateway-bff composite route (DP-19). The route calls rwb-partner for the partner, its panel status, its contract end and its score, and rwb-case for the case and its stage; this story fixes the rwb-partner answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives both screens "Loading; list", so this story produces the notice from the list state: the manager sees the partner with its panel status and its score against its target, and confirms the notice. The partner-side screens PRT-01 to PRT-04 (FSD S9) show the partner its own instructions and hold no notice action, and the rights of §10 confirm it: a partner user holds R and U and never C. No source describes a notice form or a cure-period panel, so the place of the notice action on SCR-34 and the return of the panel status after the cure period are Not specified in the source documents (GAP-3127; ASM-5455). The refusal, not-in-force, no-answer and not-recorded states read the messages of section 14. The states of SCR-34 are loading, shown as the list state above, and its empty, error and no access states are Not specified in the source documents (CG-ALL-12056). The states of SCR-35 are loading, shown as the list state above, and its empty, error and no access states are Not specified in the source documents (CG-ALL-12057).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-014-01 | AC1, run by RWB-ITG-E7014-ITG | Component | The partner `PRT-0007` at `ACTIVE` with a score below its target, the reference-data fake and the rwb-comms fake; the notice reference, `ON_NOTICE`, the record, the target and the version asserted |
| TC-E7-014-02 | AC2 | Component | The decision-record stub stopped; nothing written, no notice requested and MSG-P7-003 shown |
| TC-E7-014-03 | Access | Component | A role without partner portal right C; 403 with MSG-P4-002 and no read of the partner |
| TC-E7-014-04 | Principle 5 | Component | A forced decision record write failure inside the transaction; the panel status is unchanged and no record and no notice exist |
| TC-E7-014-05 | Section 12 operations, events and activities | Contract | API-S9-001, API-S9-002 and API-S9-003, the workflow InstructionWorkflow and the activity issuePartnerNotice, each checked against its contract element in section 12.5 |
| TC-E7-014-06 | Section 12.7 tables (ASM-3438) | Component | Each table of section 12.7 read and written only by its owner; no foreign key across the schema (DP-01); boundary values: Not specified in the source documents (ASM-3438) |
| TC-E7-014-07 | AC3 | Component | A role without partner portal right C; 403 with MSG-P4-002 before any read or write, nothing changed and no record written |
| TC-E7-014-08 | AC4 | Component | The target or the cure period absent from reference data at its version; 422 or 503 with MSG-GEN-001, nothing written and no fallback value used |
| TC-E7-014-09 | AC5 | Component | The rwb-comms fake does not answer inside 2 s, or its breaker is open; the transaction rolls back, nothing is committed and the retry reuses the same Idempotency-Key |
| TC-E7-014-10 | AC6 | Component | The same submission sent twice; one instruction, one notice and one record, and the repeat answers the existing result |
| TC-E7-014-11 | AC7 | Component | A statement that reaches a v_ace_* view, a recovery_case or timer row, a notice row or another service's schema; the grant refuses it and the boundary test fails the build |
| TC-E7-014-12 | BR3, X3 | Component | Partners at SUSPENDED or EXITED, at ON_NOTICE, or with a contract ended; each refused with 409 and nothing written |
| TC-E7-014-13 | BR8 | Component | The record, the answer, a log line and a workflow input of the synthetic partner; no contact name, e-mail, phone number or identity number present |
| TC-E7-014-14 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S9-E7014-APP-AC10) |
| TC-E7-014-15 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-S9-E7014-APP-AC11) |
| TC-E7-014-16 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-S9-E7014-APP-AC12) |
| TC-E7-014-17 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-S9-E7014-APP-AC13) |
| TC-E7-014-18 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S9-E7014-APP-AC9) |
| TC-E7-014-19 | AC8 | Component | Each of BR1 to BR11 checked against the rule coverage line of section 8; a rule with no test row fails the check |

The four legacy cases are those of RWB-E7-014 in their legacy order, with the Level column added: every case runs on the fakes, so every case is `Component`. TC-E7-014-01 exercises the notice step this story builds, and its criterion AC1 is owned by RWB-ITG-E7014-ITG, which runs the journey end to end and does not restate it here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story.

### 17. Guardrails

- No business value in code: the panel and partner type lists, the target, the cure period, the rule ID and its version stay reference data and rule values with a version, never a constant, a default or a branch.
- No personal data in `rwb_partner`, in a workflow input or in a log: partner identifiers, codes, dates, list values, an amount, a rule ID and a version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table.
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here; the stage outcome returns to the parent workflow.
- The notice stays with rwb-comms: no `notice` row, no template and no dispatch status is written here (BR4).
- The cure period stays with P3: no `timer` row and no Schedule is created by this step (BR9).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base and no event published by this step.
- The record is written before the row; a build that answers outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Feature | L3 process | Requirement (short) | Story element | Test cases |
|---|---|---|---|---|---|
| No requirement row traces to FEAT-PRM-11 | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | The requirement this feature serves is Not specified in the source documents (GAP-3127; ASM-5458): TSD S9 T8 maps REQ-S9-001 to REQ-S9-009 to FEAT-PRM-01 and FEAT-PRM-08, and REQ-S9-001 names notice and exit only among the six points | The trace rests on the legacy key, the feature row and AC-S9-011-01 | TC-E7-014-01 |
| REQ-S9-001 (nearest) | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | Every partner type is managed on the same six points, notice and exit among them | The notice step and the panel status | TC-E7-014-01 |
| ADR-013 | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | 19 services inside ACE | rwb-partner as the owner of the partner panel | TC-E7-014-01 |
| ADR-014 | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | Schema and login per service | `rwb_partner` and its own login | TC-E7-014-01 |
| ADR-020 | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | Contract-first REST, one hop, 2 s timeout | The notice request and the reference-data read with their budget and breaker | TC-E7-014-01 |
| ADR-022 | FEAT-PRM-11 | Not specified in the source documents (DOR-RWB-S9-E7014-APP-2) | Local decision record plus central ledger | The record written before the notice is requested | TC-E7-014-02, TC-E7-014-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-014, disposition Split (rework); feature FEAT-PRM-11 |
| Legacy criteria | AC2, owned word for word by this story; AC1 owned by RWB-ITG-E7014-ITG |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged from the plan; EP07 is wave 4 and the service's Arch v5 wave is 4, so the W-MAP wave is not earlier and no conflict is raised (ASM-5457) |
| Source text | Legacy RWB-E7-014; FSD S9 Partner management v3 A1.3, A2.11, A2.11.2, A2.11.3.1 to A2.11.3.3 and A2.11.4; TSD S9 Partner management v2 T1, T2, T3.0, T3.1, T3.2, T4, T5.2, T5.3, T6.1, T6.2, T8 and T-A; Business Rules and Routing Logic v4 rows R-RES-27 and R-UNI-25 to R-UNI-29; Event and Messaging Design v5 events EV-13, EV-14, EV-20 and EV-21; Epics 3 to 8 Specification v3 row FEAT-PRM-11 |
| Test cases | TC-E7-014-01 to TC-E7-014-04 |
| Feature and screens | FEAT-PRM-11, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | No partner route set exists; the rule ID and the version in force carry the placeholder (ASM-5451) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the operations, the partner and instruction elements, the lists, the rights of the document, the error envelope and the fakes: RWB-S9-E7014-CON.
- The cross-service journey of AC1 across the panel, the notice and the case: RWB-ITG-E7014-ITG.
- The notice document, its template, its dispatch and its delivery proof: rwb-comms (P6), whose contract this story consumes.
- The case of record, its stage, its clock and the cure-period timer: rwb-case (P3). The central `decision_log_entry` ledger and `rule_row`: rwb-decision (P7).
- The scorecard that measures the partner and publishes its score: FEAT-PRM-08 (RWB-S9-E7011-APP); the panel, the fee schedule and the service levels as reference data: FEAT-PRM-02 (RWB-S9-E6030).
- The allocation, the override and the partner result: RWB-S9-E6031-APP, RWB-S9-E6032-APP and RWB-S9-E6033-APP.
- The fee approval and the partner review: RWB-S9-E7012-APP and RWB-S9-E7013-APP.
- Ending the contract, recalling the work and the return of the panel status after the cure period: FEAT-PRM-12 (RWB-S9-E7015-APP). The conduct breach and the suspension: FEAT-PRM-13 (RWB-S9-E7016-APP).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories.
- The requirement row of FEAT-PRM-11 and the requirement traceability of the E7 BRD and the PRD: no source publishes one (GAP-3127; ASM-5458).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
