# RWB-S9-E7016-APP Check partner conduct

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7016-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the conduct-check slice of RWB-E7-016 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The one legacy criterion this story owns (AC2, not recorded) is kept word for word with its origin tag and nothing is added to it, because it carries no cross-service part; the main criterion of the legacy key (AC1) is owned by the wave 4 integration harness RWB-ITG-E7016-ITG. The slice is a `conductCheck` branch of `InstructionWorkflow` on task queue `rwb-partner`: it reads the sample of partner contacts and complaints through the owners' reads, evaluates the conduct rules at the package version in force, writes one entry through the local decision-record library before any change (DP-03), raises a task to the Conduct and QA officer where a person is needed, and on an upheld breach suspends allocation, recalls the affected instructions to RECALLED and asks rwb-case to re-select each affected case. It declares no REST operation of its own, because the Ownership Map gives S9 six operations and all six belong to the instruction and partner stories; the effect is read through `GET /partners` and `GET /partner/instructions` on base `/api/recovery/partner/v1` (DP-13) behind the gateway-bff composite route (DP-19). The service owns EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted` and neither carries a conduct finding, so the check publishes nothing. No PRM rule set exists in the Business Rules and Routing Logic v4, the sample of contacts and complaints has no entity in any source, the sampling size and period are unpublished, the word "upheld" has no definition and the batch-status fact sits with rwb-source-data (GAP-3131; ASM-5473 to ASM-5481). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer (RW-CONDUCT)** — the role FSD S9 A2.13.3.3 names as also using this step, which runs unattended under the service identity — I want **the Workbench to sample partner contacts and complaints against the conduct rules at the version in force and raise each breach it finds, with the decision recorded before anything moves**, so that **partners are placed, paid and measured by rule and a partner that breaches conduct is suspended and its work pulled back the same day under the rule version that judged it**.

This story owns:

- the one legacy criterion of RWB-E7-016 that the plan gives it (AC2, not recorded), copied verbatim with its origin tag;
- the `conductCheck` branch of `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery`, run unattended under the rwb-partner service identity;
- the sample read: partner contacts and complaints taken through the owners' reads, because S9 owns no contact, notice or complaint table (ASM-5473);
- the evaluation of the conduct rules at the package version in force: R-UNI-29 for the breach, R-LIT-22 for a failed conduct check on a notice or a contact, and R-UNI-38 for the version an open case keeps (ASM-5474);
- the decision record: one hash-linked entry per check result, written through the local decision-record library **before** anything else, carrying the partner, the sample set with its case keys, the rule IDs and the package version (DP-03; legacy AC2);
- the breach effect on this service's own facts: `partner.panel_status` to SUSPENDED (allocation suspended) and each affected `partner_instruction.status` to RECALLED (DF-PRT-005, DF-PRT-014), in the transaction of the entry;
- the request to rwb-case to re-select each affected case under R-UNI-45, one Temporal command per case, and the report of the breach to the partner review forum (REQ-S9-007);
- the task raised to the Conduct and QA officer where a person is needed, and the reads behind SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19), on the service base `/api/recovery/partner/v1` (DP-13).

It does not own: the published shapes, the rights, the error set and the fakes (RWB-S9-E7016-CON); the main criterion AC1 and its end-to-end proof (RWB-ITG-E7016-ITG); the contacts, the notices and the complaints themselves and their owners' contracts; the monthly scorecard (FEAT-PRM-08) and the partner review (FEAT-PRM-10); the notice on a missed target (FEAT-PRM-11) and the contract end (FEAT-PRM-12); the receipt of a partner result onto the case (FEAT-PRM-05); the rule packages and the central ledger (rwb-decision P7); the roles and rights (rwb-access P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective, the problem and the metric are the module's and do not move: partners are instructed and paid by email and spreadsheet and allocation is not based on performance; the metric is the placements made by scorecard against 100 percent, measured on the decision log and the Workbench records and reviewed monthly (FSD S9 A2.13.1). The requirement this feature serves is REQ-S9-007, "Partner performance, conduct and complaint data are reported to the partner review forum"; the recall the breach triggers is REQ-S9-006, which names an upheld conduct breach beside a panel exit, a conflict and insolvency (Program BRD v4; FSD S9 Requirements served).

The legacy story states conduct as one clause of one screen-backed feature and gives it two endpoints and two screens that belong to the instruction path. What D-RCV-60 changes is where each fact of a conduct check lives:

- **The finding and the breach on the partner are this service's.** The panel status and the instruction status are the two places a suspension and a recall can be written without touching another service's table (TSD S9 T3.1, DF-PRT-005, DF-PRT-014), and R-UNI-29's to_state PARTNER_RECALLED is the partner side of the recall, not a case state.
- **The sample is not.** "Partner contacts and complaints" is the sample definition and no source gives it an entity: the LDM has no complaint table, TSD S9 T3.1 gives three partner tables, and FSD S9 A2.13 has no field catalog. The contact and the complaint are other modules' facts (FEAT-OCC-05, FEAT-DVF-09), so the check reads them through their owners' reads and this boundary is recorded as a gap rather than invented as a table (GAP-3131; ASM-5473).
- **The rules are governed elsewhere and evaluated here.** Embedded Drools with rule packages from rwb-decision is the platform rule (DP-04), and the conduct rows that exist are UNIVERSAL: R-UNI-29 for the breach, R-LIT-22 for the failed check on a notice or a contact and R-UNI-10 with R-UNI-44 for the contact stop. No PRM domain exists, so no rule is authored here (ASM-5474).
- **The check is a decision, so it is recorded before it acts.** Legacy AC2 says that where the decision log cannot be written nothing changes and MSG-P7-003 is shown; R-UNI-39 says the same. The entry commits before the panel status, the recall set and the case requests (DP-03).
- **The case is commanded, never written.** R-UNI-45's to_state is ROUTE_D6_REOPEN, a case route state, and `recovery_case` and its timers are P3's, so the re-selection is a Temporal command and the case applies it (ASM-5475).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-partner is created in wave 4, so the two waves agree and the date is copied unchanged and marked tentative (U7, R7; ASM-5467).

### 3. Preconditions

- RWB-S9-E7016-CON is published and tagged: the two read elements, the unchanged partner and instruction shapes, the sample and breach record elements with their placeholders, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner` and `partner_instruction` exist in `rwb_partner` from the DB story of this service, with the fields of DF-PRT-001 to DF-PRT-016 and the standard record columns of TSD S9 T3.0; at least one partner carries RECALLED-able instructions (DF-PRT-014).
- An `InstructionWorkflow` execution exists for the partner on `rwb-partner`. The one workflow the Ownership Map gives S9 is this one and it carries no job of its own (context pack ownership rows, Workflows: 1, Jobs: 0; ASM-5473).
- The UNIVERSAL package is in force at its version with R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45; it is authored, tested and approved in rwb-decision (P7) and loaded here. No PRM package exists in the rule set (ASM-5474).
- The sample boundary is available for its fake: the partner's contacts and its complaints arrive as answers of their owners' reads, one hop, 2 s. The operation names and the field lists are Not specified in the source documents (GAP-3131; ASM-5473).
- The lists of values this step reads — `LOV-PANEL` with ACTIVE, ON_NOTICE, SUSPENDED and EXITED and `LOV-INSTR-STATUS` with SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE and RECALLED — are reference data with their version, read on the owner's contract and never written in code (TSD S9 T3.2).
- The batch-status fact behind VR-S9-013-1 (`v_ace_batch_status`) is an ACE view that only rwb-source-data reads; this service holds no `v_ace_*` grant and takes the staleness answer from rwb-source-data's contract (DP-05; ASM-5477).
- The service runs as its own login on `rwb_partner` and holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_comms` or `rwb_decision` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7016-CON when its tests pass.

### 4. Flow

1. The trigger arrives. FSD S9 A2.13.2 names three: a completed ACE batch, an event or a timer; the Ownership Map gives S9 no job, so the check runs as a `conductCheck` branch started on `InstructionWorkflow` and the exact trigger is Not specified in the source documents (GAP-3131; ASM-5473).
2. `readConductSample` takes the sample of the partner's contacts and its complaints from their owners' reads, with the sample period and size read at their version; both parameters are Not specified in the source documents and carry the placeholder (GAP-3131; ASM-5478).
3. The stale-data gate: where the batch status the sample depends on is not today's, the branch stops with MSG-P1-001 and changes nothing (VR-S9-013-1).
4. `evaluateConductRules` loads the UNIVERSAL package version in force and evaluates R-UNI-29, R-LIT-22 and R-UNI-38 against the sample; no version in force stops the branch and changes nothing (ASM-5474).
5. `recordAndApplyBreach` writes one entry through the local library **before any other effect**: the partner, the sample set with its case keys, the findings, the rule ID R-UNI-29 with its package version, the actor (the service identity) and the check date. A failed write stops the step with nothing changed and MSG-P7-003 (DP-03; legacy AC2).
6. A clean sample records the result and ends there: no status moves, no case is asked to re-select and the next check waits for its trigger.
7. A finding raises a task to the Conduct and QA officer, who upholds or clears it; while a finding is open the allocation of that partner is not suspended and no instruction is recalled (R-UNI-29's condition is an upheld breach; ASM-5476).
8. On an upheld breach, in the transaction of the entry: `partner.panel_status` moves to SUSPENDED, so allocation is suspended, and every affected instruction of that partner moves to RECALLED (DF-PRT-005, DF-PRT-014).
9. `requestCaseReselection` asks rwb-case, one command per affected case on the case boundary, to reopen the route and re-select the next partner under R-UNI-45; this service writes no case row (ASM-5475).
10. The breach is reported to the partner review forum as REQ-S9-007 asks, and `breachClock` starts one durable timer for R-UNI-29's same-day service level and R-UNI-45's 2 working days; the expiry escalates under R-UNI-30.
11. A repeat of the same partner and check date is idempotent: one entry, one suspension, one recall set and one timer, and the repeat answers the entry already written (ASM-5479).
12. The partner reads SUSPENDED on `GET /partners` and its recalled instructions read RECALLED on `GET /partner/instructions`, both through the composite route, read only (DP-13, DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no finding is raised, the partner stays as it was, no instruction moves and no case is asked to re-select | MSG-P7-003 | AC2, TC-E7-016-02, TC-E7-016-04 |
| X2 | The caller does not hold Partner portal R for the read of the breach and the sample | 403 before the sample is read and before the record is written | MSG-P4-002 | TC-E7-016-03 |
| X3 | A required value is absent or invalid: no partner reference, no check date or no sample set | The branch refuses the check, writes nothing and names the field | MSG-GEN-001 (VR-S9-013-1) | TC-E7-016-02 |
| X4 | The data product the sample or the batch status depends on is stale after a late or failed ACE batch | The check does not run on stale data and says so; nothing is recorded as a finding | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. | TC-E7-016-02 |
| X5 | A sample owner's read does not answer inside 2 s, or its breaker is open | No finding is raised, the check is retried on the workflow's own schedule and the caller sees the platform 503 envelope | None (platform envelope) | TC-E7-016-02 |
| X6 | The UNIVERSAL package has no version in force for R-UNI-29 or R-LIT-22 | The branch waits, no finding is recorded and no status moves on an unversioned rule | None | TC-E7-016-02 |
| X7 | The same partner and check date arrive again | Idempotent: the entry already written is answered and nothing is written, suspended or escalated again | None | TC-E7-016-02 |
| X8 | The partner already reads SUSPENDED, or an instruction already reads RECALLED | The open set is taken as it stands, the entry names the set it moved and no instruction is moved twice | None | TC-E7-016-02 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case`, `rwb_comms` or `rwb_decision` row | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6, BR7 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X8 are the paths the sample, the rule version and the breach set add; X9 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7016-CON, the decision-record stub, the sample fake, the package fake and the gateway-bff fake, on its own schema, and needs no live P6, P3 or P7 |
| Negotiable | The activity names, the branch shape, the trigger binding and the entry attributes are this story's choice; the rules, the messages, the screens, the statuses and the lists are fixed |
| Valuable | Every partner contact and complaint is sampled against the conduct rules at their version, a breach is upheld with its rule version on the record, and a breaching partner is suspended and its work pulled back the same day |
| Estimable | One workflow branch, four activities, one record write, one partner update, one instruction update set, one child command per case and one durable timer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on a synthetic partner through the contract fakes, plus a clean sample, the open finding, the repeat, the stale batch, the refused right and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Check partner conduct

  Background:
    Given the UNIVERSAL rule package is in force at its version and carries R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-016 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The criterion is the legacy criterion of RWB-E7-016 word for word, with its origin tag added and nothing else changed: the wording of `the decision log cannot be written`, `the action is taken` and `nothing changes and the user sees MSG-P7-003` all stand. It carries no cross-service part, so no `Given the <service> contract mock returns <x>` line is added to it. On this story "the action" is the conduct check on a partner and the recording of its result; what the legacy line describes now happens in two places: rwb-partner writes the local record and moves the partner and the instructions, and rwb-case is asked to re-select each affected case. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the `decision_log_entry` ledger of rwb-decision behind it.

The main criterion of the key (AC1) stays with RWB-ITG-E7016-ITG, which owns it word for word; this story builds the path it proves and copies it nowhere.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-29 | Universal rules | All | ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | Suspend allocation, recall the affected cases, report to the partner review | PARTNER_RECALLED | Partner and agency manager | Partner Portal | same day |
| R-UNI-38 | Universal rules | All | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Center of excellence | Workbench | on the effective date |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days |
| R-LIT-22 | Litigation | D7 | PACK_VERIFIED | CONDUCT_CHECK_FAILED | the conduct check on the notice or the contact fails | Return the notice for correction before filing | NOTICE_BLOCKED | Conduct and QA officer | Workbench | 2 working days |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character. This story evaluates R-UNI-29 for the breach, R-LIT-22 for a failed check on a notice or a contact and R-UNI-38 for the version an open case keeps; it names R-UNI-45 as the rule of the request it sends to rwb-case and R-UNI-39 as the record-first rule. R-UNI-10 (consent withdrawn, HELD_CONDUCT) and R-UNI-44 (contact stop lifted) belong to the contact stop of the contact owners and are read, not fired, here. R-UNI-27 and R-UNI-28 recall work for a conflict and an insolvency and run through the same recall branch; they are not fired by this step. Their owner column names a business role and a system, not a service: "Partner Portal" is this service and its partner-facing screens.

| ID | Rule | Source |
|---|---|---|
| BR1 | The check is a decision first: one entry per check result is written through the local library with the partner, the sample set and its case keys, the findings, R-UNI-29 and the package version; a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy AC2 |
| BR2 | The finding and the breach on the partner are this service's: `partner.panel_status` SUSPENDED suspends allocation and `partner_instruction.status` RECALLED recalls the work, both inside the transaction of the entry | TSD S9 T3.1 (DF-PRT-005, DF-PRT-014); TSD S9 T3.2 (LOV-PANEL, LOV-INSTR-STATUS); R-UNI-29 |
| BR3 | It is the upheld breach that moves the panel and the work: an open finding suspends nothing and recalls nothing, and the same-day service level of R-UNI-29 runs from the check | R-UNI-29; ASM-5476 |
| BR4 | The sample is read, never owned: this service declares no contact, notice or complaint table and no field list of them, and takes the sample through the owners' reads | DP-01, DP-11; TSD S9 T3.1; ASM-5473 |
| BR5 | The rules are governed in rwb-decision and evaluated here at the version in force: no rule ID is authored, no threshold is written in code, and an open case keeps the version it was decided under | DP-04; R-UNI-38; FSD S9 BR-S9-013; ASM-5474 |
| BR6 | The case is not written here: the re-selection is a Temporal command to rwb-case under R-UNI-45, whose to_state ROUTE_D6_REOPEN is a case route state, and its outcome is the child result | R-UNI-45; Architecture v5 slides 8 and 12; ASM-5475 |
| BR7 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and the case reference are identifiers of another service's fact, and ACE data arrives only through rwb-source-data's contract | DP-01, DP-05; TSD S9 T3.3 |
| BR8 | The stale sample is not judged: where the batch status is not today's the check stops with MSG-P1-001 and records nothing | VR-S9-013-1; FSD S9 A1.4; ASM-5477 |
| BR9 | The check is idempotent per partner and check date: one entry, one suspension, one recall set and one timer, and a repeat answers the entry that exists | TSD S9 T-A.2; Architecture v5 slide 11; ASM-5479 |
| BR10 | No person name, customer identity, account number or contact value enters `rwb_partner`, an entry, a log, a workflow input or an event; the sample is referenced by case and instruction keys | Template and Rules v1 §R7.2 (s17); LDM v8 |

### 9. State transitions

This story moves two states of its own tables and one of the rule set, and never a case state:

| From (`partner.panel_status`, DF-PRT-005) | Event | Condition | To | What this story writes |
|---|---|---|---|---|
| ACTIVE | PARTNER_CONDUCT_BREACH | the breach is upheld (R-UNI-29) | SUSPENDED | `panel_status` in the transaction of the entry |
| ON_NOTICE | PARTNER_CONDUCT_BREACH | the breach is upheld while the partner is on notice | SUSPENDED | the same column |
| EXITED | PARTNER_CONDUCT_BREACH | the breach arrives after the contract ended | EXITED | Nothing; the entry is recorded and the recall set is empty |
| SUSPENDED | PARTNER_CONDUCT_BREACH | the same partner and check date arrive again | SUSPENDED | Nothing; the entry already written is answered |

| From (`partner_instruction.status`, DF-PRT-014) | Condition | To | Note |
|---|---|---|---|
| SENT | The instruction is affected by the upheld breach | RECALLED | The case is asked to re-select |
| ACCEPTED | The instruction is affected by the upheld breach | RECALLED | The case is asked to re-select |
| IN_PROGRESS | The instruction is affected by the upheld breach | RECALLED | The case is asked to re-select |
| DONE, DECLINED, RECALLED | Not affected | unchanged | Not named in the recall set |

| Branch step | Event | Condition | To |
|---|---|---|---|
| Waiting | A conduct-check trigger arrives for the partner | The package version is read | Reading |
| Reading | The sample of contacts and complaints is read | The batch status is today's | Evaluating |
| Reading | The batch status is stale | X4 | Waiting, MSG-P1-001 |
| Evaluating | R-UNI-29 holds and a version is in force | There is at least one finding | Recording |
| Evaluating | No finding holds | The sample is clean | Recorded, ended |
| Recording | The entry is written and a finding is raised | The task is open | Recording, waiting on the person |
| Recording | The entry write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Recording | The breach is upheld and the partner and instructions move | The transaction commits | Commanding |
| Commanding | A case answers the re-selection request | The child result is accepted | Clocked |
| Commanding | A case does not answer inside 2 s | X5 | Retried on the workflow's schedule |
| Clocked | The durable timer expires | The service level has run | Escalated under R-UNI-30 |

SUSPENDED and RECALLED are values of the two published lists and this story adds none; PARTNER_CONDUCT_BREACH and PARTNER_RESELECTED are the event codes of R-UNI-29 and R-UNI-45, and ROUTE_D6_REOPEN is the case state rwb-case moves to, not this service (ASM-5475).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Conduct and QA officer (RW-CONDUCT) | The "also uses" role of FSD S9 A2.13.3.3 and the owner of R-LIT-22: holds Partner portal R only in TSD S9 T6.1, reads the finding and upholds or clears it in the task |
| The unattended branch (rwb-partner service identity) | The primary actor of FSD S9 A2.13.3.3: runs the sample, the rules and the record under the service identity with the same role checks as a person (NFR-051) |
| Partner and agency manager (RW-AGENCYMG) | The owner column of R-UNI-29 (CRUDA in TSD S9 T6.1): owns the suspension, the recall and the re-selection that follow |
| Case owner (RW-CASEOWN), team manager (RW-TEAMMGR), legal counsel (RW-LEGAL), the six officer roles | Partner portal R in the legacy permission table: read the partner, its status and its instructions, and start no check |
| Partner portal users (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC) | Partner portal RU: read their own instructions and record results; they see no finding and no breach |
| rwb-case (P3) | Owns the case, its route state and its timers, and applies the re-selection request this story sends |
| rwb-decision (P7) | Owns the UNIVERSAL package, its rule rows and the central ledger; this story evaluates them and records locally |
| rwb-access (P4) | Owns the roles, the capability rights and the lists of values this story reads through the guard |
| rwb-comms (P6) and the complaint owner | Own the contacts, the notices and the complaints the sample is taken from; this story reads them and writes none |

No delegated authority limit is set here: the customer-level delegation table is rwb-access's (P4) and this act moves partner work, not a customer decision. The branch holds no right of a person and runs under the rwb-partner service identity with the same checks a person gets (NFR-051; ASM-5481).

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Read** `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score`; **write** `panel_status` to SUSPENDED (DF-PRT-005) on an upheld breach |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read** `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`; **write** `status` to RECALLED (DF-PRT-014) for the affected set only |
| None in the sources | `partner_user` | S9, `rwb_partner` | Not read and not written. The context pack gives S9 this table and TSD S9 T3.1 gives it no field list |
| None: library table | `decision_record` | Platform library in `rwb_partner` | **Write**: one hash-linked entry per check result, before anything else (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_partner` | The partner-and-check-date key and the answer it holds; the outbox object exists as a library row and this step writes no event row to it (§12.3) |
| None in the sources | contacts, notices and complaints | rwb-comms (P6) and the complaint owner | **Read only through the owners' reads**: the sample. No source gives an entity, a field list or an owner for a complaint table; the request and answer shapes are Not specified in the source documents (GAP-3131; ASM-5473) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | P3 rwb-case | Not read as a table and not written: the case reference arrives from `partner_instruction.case_id` and the re-selection is a command, not a row |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the UNIVERSAL package arrives loaded at its version in force |

No new table, no new column and no migration: the two tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's own migration (DP-03). The sample size, the sample stratum and the sample period are Not specified in the source documents (GAP-3131; ASM-5478).

**No personal data.** The entry and the commands carry a partner reference, a partner code, case and instruction keys, a status, a date and a rule version. The contact values the sample is taken from stay with their owner and never enter `rwb_partner`, an entry, a log or a workflow input (BR10).

### 12. Contract

#### 12.1 REST operations provided

None declared by this story. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The six operations the Ownership Map gives S9 are `GET /partners`, `GET /partner/instructions`, `POST /cases/{caseId}/instructions`, `POST /partner/instructions/{instructionId}/accept`, `POST /partner/instructions/{instructionId}/invoices` and `POST /partner/instructions/{instructionId}/results`; the check is unattended and none of the six starts it, so this story declares no seventh. The two reads answer the effect of this story — `panel_status` on the partner and `status` on the instruction — and both are declared by RWB-S9-E7016-CON. The trigger of the check has no published entry point and carries the placeholder (GAP-3131; ASM-5473). A build that declares a conduct-check operation here fails the absence test of RWB-S9-E7016-CON.

#### 12.2 REST operations consumed

None declared. The step reads its own two tables, the packages arrive loaded at their version, and the case is reached on the Temporal boundary (§12.5). The sample of contacts and complaints is read through the owners' reads and the batch status through rwb-source-data, so the step consumes two contracts in fact and neither is in the plan's C row, which is empty; the absence is recorded (GAP-3131; ASM-5473).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set is `InstructionIssued` (`rwb.partner.InstructionIssued.v1`, EV-20) and `PartnerResultSubmitted` (`rwb.partner.PartnerResultSubmitted.v1`, EV-21); both describe the issue of an instruction and the result the partner records, and both belong to the instruction stories of this service (context pack ownership rows; Event and Messaging Design v4 EV-20 and EV-21; TSD S9 T5.3). A conduct finding is neither, so this story declares no producer group, no envelope and no outbox row, and reports the breach to the review forum under REQ-S9-007 through the reporting read model rather than a second event (ASM-5480).

#### 12.4 Events consumed

None. No source gives rwb-partner a consumed event for a conduct check: the trigger is the batch, an event or a timer FSD S9 A2.13.2 names without a name or a topic, the contacts and the complaints are read through their owners' reads, and EV-21 is the result the partner portal records. This service therefore declares no consumer group, no subscription and no inbox of its own (GAP-3131; ASM-5473).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner holding its open instructions and their clocks, continues-as-new | `rwb-partner` in namespace `rwb-recovery` | Hosts the `conductCheck` branch; its input is the partner reference and the check date |
| `conductCheck` | Workflow branch | `rwb-partner` | The path from the trigger to the entry, the finding, the person's decision, the panel and instruction update, the case requests and the clock |
| `readConductSample` | Activity | `rwb-partner` | The partner in; the sample of contacts and complaints with its case keys out |
| `evaluateConductRules` | Activity | `rwb-partner` | The package in force and the sample in; the findings with R-UNI-29, R-LIT-22 and R-UNI-38 and their versions out |
| `recordAndApplyBreach` | Activity | `rwb-partner` | The entry, the partner suspension and the recall set out, one transaction |
| `requestCaseReselection` | Activity | `rwb-partner` | One child command per affected case on the case boundary under R-UNI-45; the request in and the child result out |
| `breachClock` | Durable timer of the branch | `rwb-partner` | The same-day service level of R-UNI-29 and the 2 working days of R-UNI-45 with their versions; the expiry is the escalation |

The breach answer carries the partner, the entry reference, the finding set, R-UNI-29 with its version, the recall set with its case keys, the number of cases asked to re-select and the clock start. The branch and activity names are a target design choice fixed by no source document, and the case-side command has no published name (GAP-3131; ASM-5475).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job (context pack ownership rows, Jobs: 0) and FSD S9 A2.13.4.4 declares no background event for the feature, so this story declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The trigger is the branch start and the service level is a durable timer inside the branch; DP-10 is not in this key's pattern set (ASM-5473).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `partner` | S9, `rwb_partner` | The partner, its type, its panel status, its contract end and its score; this story writes `panel_status` only |
| `partner_instruction` | S9, `rwb_partner` | The work placed with a partner on a case; this story writes `status` for the affected set only |
| `partner_user` | S9, `rwb_partner` | Owned per the context pack ownership rows; this story neither reads nor writes it |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked entry of the check result and the breach (DP-03) |
| `idempotency_key` | Platform library in `rwb_partner` | The partner-and-check-date key of the repeated run |
| `outbox_event` | Platform library in `rwb_partner` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` and the contact points (P6), the complaints (their owner is not named in the sources) and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC2, X1 |
| Sample fake | A sample with one contact finding and one complaint finding on case `RW-2027-001601`, and a clean sample | X3, section 16 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-29, R-LIT-22, R-UNI-38, R-UNI-39 and R-UNI-45; a package with no version in force | X6 |
| rwb-source-data batch-status fake | Today's batch, and a stale batch with its date | X4 |
| rwb-case re-selection fake | The case accepting the re-selection with its route reopened, the same case refusing it, and no answer inside 2 s | X5, X8 |
| rwb-access guard fake | RW-CONDUCT with Partner portal R, and a role with no right | X2 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answers for the partner, its panel status and its instructions | Section 15 |
| Partner fixture | Partner `PTR-2027-001601` of type AGENCY at ACTIVE, holding instructions `INS-2027-001601` (ACCEPTED) and `INS-2027-001602` (IN_PROGRESS) on case `RW-2027-001601`, and one at DONE | X3, X8 |

The fakes are test-only and are replaced by the real services in SIT. The sample element, its size and its period carry the placeholder until the sample owner and the rule owner publish them (GAP-3131; ASM-5478).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The two reads of the service are declared by RWB-S9-E7016-CON; the sample and the batch status are read through their owners' reads |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 belong to the instruction stories; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 4 activities, 1 durable timer and 1 child command per case | `InstructionWorkflow` and its `conductCheck` branch on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `conduct`; front end `src/modules/recovery/partner/PartnerConduct.tsx`, the SCR-34 and SCR-35 fragments this story answers.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the entry commits before the panel, the recall set and the case requests, and a failed write leaves nothing behind. DP-13 fixes the base of the service and gives the check no element of its own, because it is unattended. DP-19 is how SCR-34 and SCR-35 reach this service, one hop through the gateway. The sample boundary and the batch status are recorded in the registers rather than added to the plan, and the rule package is loaded from rwb-decision without a new dependency row (ASM-5473; ASM-5474).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` conduct branch | Workflow | Receives the trigger, hosts the task to the person and the clock, applies the idempotency key and reports the answer |
| `readConductSample` | Activity | Takes the sample of contacts and complaints through the owners' reads and builds the finding set |
| `evaluateConductRules` | Activity | Evaluates R-UNI-29, R-LIT-22 and R-UNI-38 and returns the findings with their package versions |
| `recordAndApplyBreach` | Activity | Writes the entry, suspends the partner and moves the recall set in one transaction |
| `BreachEntryWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the step when the write fails |
| `CaseReselectionClient` | Client | The Temporal command to rwb-case per affected case, with the breaker and the retry of the workflow |
| `ConductSampleClient` | Client | The owners' reads for the contacts, the notices and the complaints, one hop, 2 s |
| `PartnerConductRepository` | Repository | The partner and its instructions, read and written on this schema only |
| `BreachClock` | Durable timer | The same-day service level of R-UNI-29 and the 2 working days of R-UNI-45 |
| `PartnerConduct` | React component | Shows the finding, the panel status and the recall set on SCR-34 and SCR-35, read only |

**Database and migrations.** No Flyway file. `partner` and `partner_instruction` arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's migration (DP-03). No column is added: the suspension is carried by `partner.panel_status` and the recall by `partner_instruction.status`.

**Configuration and reference data.**

- The sample size, the sample stratum and the sample period: rule rows or reference data read at their version; Not specified in the source documents (GAP-3131; ASM-5478).
- The same-day service level of R-UNI-29 and the 2 working days of R-UNI-45: rule rows read at their version.
- The named escalation point of R-UNI-30 and the partner type classification: reference data with their versions.
- `LOV-PANEL` and `LOV-INSTR-STATUS`: read at their version through the reference-data contract of rwb-case (default ruling DP-07).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.

**Build steps**

1. The `conductCheck` branch and its input record on `rwb-partner`, registered as a branch of `InstructionWorkflow`, with the trigger binding, the idempotency key and the durable timer.
2. `ConductSampleClient` and `readConductSample` against the sample fake, with the empty sample and the unavailable owner (X3, X5, X8).
3. The stale-batch gate of VR-S9-013-1 against the batch-status fake, with MSG-P1-001 (X4).
4. `evaluateConductRules` over the package in force, with R-UNI-29, R-LIT-22 and R-UNI-38 and the unversioned-package path (X6).
5. `BreachEntryWriter` against the stub, with the failed-write path and MSG-P7-003 (AC2, X1).
6. `recordAndApplyBreach` with the suspension, the recall set and the entry in one transaction, and the repeat path (X7).
7. The task to the Conduct and QA officer and the upheld and cleared outcomes (BR3).
8. `CaseReselectionClient` against its fake, one command per case, with the 2 s budget and the unavailable path (X5).
9. The breach clock and the R-UNI-30 escalation, then the read-only SCR-34 and SCR-35 fragments through the composite route fake (DP-19).
10. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no `rwb_case` row and no write to another service's schema (X9, BR7).

**Feature flag.** `rwb.partner.conduct-check-v1`, a flag of the platform library; off means the branch does not start, no finding is raised and no status moves.

**Done when.** The tests of section 16 pass, a sample with a finding raises one entry and one task, an upheld breach suspends the partner and recalls every affected instruction, a case is asked to re-select and reads the recall after the child result, a clean sample changes nothing, a stale batch records nothing with MSG-P1-001, a repeated run writes once, a forced entry failure changes nothing, the refused right answers MSG-P4-002, and no `rwb_case` row and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the check is absent or invalid, for example no partner reference, no check date or no sample set (X3, VR-S9-013-1) | Enter {field}. |
| MSG-P4-002 | A caller without Partner portal R asks for the finding, the panel status or the instructions (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The entry cannot be written before anything else (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product the sample or the batch status depends on is stale after a late or failed ACE batch (X4, VR-S9-013-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four IDs are those of the legacy and FSD S9 message set of this key; the text of MSG-GEN-001, MSG-P4-002 and MSG-P7-003 is the legacy wording and the text of MSG-P1-001 is VR-S9-013-1's, all copied unchanged. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-34 Partner list | Loading; list; finding raised; suspended | The partner with its partner type, panel status SUSPENDED and its finding, read only through the composite route |
| SCR-35 Placement and allocation | Loading; list; recalled; re-selection requested | The recalled instructions of the partner and the case each one was pulled back from, read only |

The check itself has no screen: FSD S9 A2.13.3.3 names "None; runs unattended" as the primary actor and the legacy screen table gives the two reads of the instruction path. Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and its route state; this story fixes only its own partner and instruction answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The finding, refused, not-recorded, stale and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-016-01 | AC1 (legacy); the conduct check path built here | Component | Partner `PTR-2027-001601` at ACTIVE holding instructions ACCEPTED and IN_PROGRESS on case `RW-2027-001601`; the sample, the entry, the suspension, the recall set, the case request and the clock asserted; the end-to-end proof of AC1 is RWB-ITG-E7016-ITG |
| TC-E7-016-02 | AC2 | Component | The decision-record stub stopped; no entry, no finding, no suspension, no recall, no case request and MSG-P7-003 |
| TC-E7-016-03 | Access | Component | A caller with Partner portal R only and one with no right; 403 with MSG-P4-002 and no sample read |
| TC-E7-016-04 | Principle 5; AC2, X1 | Component | A forced decision-record write failure stops the check with MSG-P7-003 and leaves the partner, the instructions, the cases and the timer unchanged |

The four IDs are the legacy cases of RWB-E7-016 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The clean sample, the open finding, the stale batch, the unversioned package and the repeat are covered inside TC-E7-016-02 and by the new contract cases of RWB-S9-E7016-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; the `-ITG` copies of the four belong to RWB-ITG-E7016-ITG, and no `-ITG` copy is written by this story.

### 17. Guardrails

- No business value in code: the sample size, the sample period, the service levels, the escalation point, the panel and instruction lists and the package versions stay rule rows or reference data read with their version.
- No personal data in `rwb_partner`, in an entry, a command, a log or a prompt: identifiers, a status, a date and a rule version only; the contact values stay with their owner.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema (BR7).
- The case, its route state and its timers stay with rwb-case: this story sends a command and writes no case row and no timer row (BR6).
- One base, one topic, one queue and one login per service; this story adds no second topic, no event and no Schedule (DP-13, DP-14).
- The record is written before the change and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- The recall is never a hard delete: the instruction keeps its row and changes status, so the history of the placement survives the suspension.
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no `recovery_log` write and no data-lake path.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The finding, the entry, the report to the review forum and the panel status | TC-E7-016-01, TC-E7-016-04 |
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner (Must, E7) | The suspension, the recall set and the case re-selection request | TC-E7-016-01, TC-E7-016-02 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the partner and the instruction | TC-E7-016-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E7-016-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The UNIVERSAL package loaded at its version | TC-E7-016-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The sample reads and the case re-selection command with their budget and breaker | TC-E7-016-01 |
| ADR-022 | Local decision record plus central ledger | The check entry written before anything else | TC-E7-016-02, TC-E7-016-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-016, disposition Split (rework); feature FEAT-PRM-13 |
| Legacy criteria | AC2, owned word for word by this story; AC1 owned by RWB-ITG-E7016-ITG |
| Source text | Legacy RWB-E7-016; FSD S9 Partner management v3 A2.13 and Requirements served; TSD S9 Partner management v2 T2, T3.0 to T3.3, T4, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-UNI-10, R-UNI-29, R-UNI-30, R-UNI-38, R-UNI-39, R-UNI-44, R-UNI-45 and R-LIT-22; LDM and Data Dictionary v8 `partner`, `partner_instruction`, `LOV-PANEL` and `LOV-INSTR-STATUS`; Event and Messaging Design v4 EV-20 and EV-21; Program BRD v4 REQ-S9-006 and REQ-S9-007; Epics 3 to 8 Specification v3 FEAT-PRM-13 |
| Test cases | TC-E7-016-01 to TC-E7-016-04 |
| Feature and screens | FEAT-PRM-13, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-29, R-LIT-22 and R-UNI-38 evaluated; R-UNI-10, R-UNI-30, R-UNI-39, R-UNI-44 and R-UNI-45 read |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the sample and breach record elements, the rights, the error set and the fakes: RWB-S9-E7016-CON.
- The main criterion AC1 of this key and its end-to-end evidence through the real sample, partner, case and decision contracts: RWB-ITG-E7016-ITG.
- The contacts, the notices and the complaints themselves, their repositories and their owners: FEAT-COM-05, FEAT-DVF-09 and FEAT-DVF-10, and rwb-comms (P6).
- The monthly scorecard and the partner review forum (FEAT-PRM-08, FEAT-PRM-10), the notice on a missed target (FEAT-PRM-11) and the contract end (FEAT-PRM-12).
- The receipt of a partner result onto the case and the operations that carry it (FEAT-PRM-05; the instruction stories of this service).
- The case of record, its route state, its re-selection and its timers: rwb-case (P3), which applies the request this story sends.
- The UNIVERSAL package, its rule rows and the central ledger: rwb-decision (P7). The roles, the rights and the lists of values: rwb-access (P4).
- The partner gateway and FAPI 2.0: the edge stories' own scope.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
