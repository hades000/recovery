# RWB-S9-E6031-APP Allocate work by measured return

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S9-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E6031-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the placement slice of RWB-E6-031 in rwb-partner. Legacy AC2 is kept word for word with its origin tag and is the only legacy criterion this story owns; AC1 of the legacy key is proved end to end by RWB-ITG-E6031-ITG. The story builds the scorecard pick over the panel of `rwb_partner` and the measured return of rwb-source-data, the local decision record written before the instruction exists (DP-03), one `partner_instruction` row and one `InstructionIssued` fact per placement, and the three operations the API sheet gives this module on base `/api/recovery/partner/v1` (DP-13, API-S9-002 and API-S9-003 as the sheet numbers them), reached by staff through the gateway-bff composite route and by partners through the partner gateway (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E6031-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager**, I want **the Workbench to place work with the partner the scorecard rule picks, not by rotation or habit**, so that **partners are placed, paid and measured by rule**.

This is the placement slice of legacy RWB-E6-031. It owns:

- legacy AC2, copied verbatim with its origin tag, and the message and the record it depends on;
- the scorecard pick: the eligible partners of the panel, ranked on measured return, with the top-ranked partner chosen and the rank order kept as evidence;
- the anti-rotation rule in code form: no rotation counter, no round-robin position, no fixed share and no last-placed memory is read, stored or honoured anywhere on the path;
- the hold of R-WO-31 when no partner on the panel has capacity;
- the decision record of the pick, written before the instruction exists (DP-03), carrying the rule ID, the rule version and the scorecard version;
- one `partner_instruction` row per placement in `rwb_partner`, with the partner, the case, the instruction type, the status and the two clock dates;
- `InstructionWorkflow` on task queue `rwb-partner` in namespace `rwb-recovery` and its partner clock, started once per instruction;
- `POST /cases/{caseId}/instructions`, `GET /partner/instructions` and `GET /partners` on `/api/recovery/partner/v1` (DP-13), the SCR-35 placement state behind the gateway-bff composite route and the partner-facing read behind the partner gateway (DP-19);
- the one event of the placement, `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1`.

It does not own: the published shape of the three operations, the elements, the rights, the error set and the fakes, which are RWB-S9-E6031-CON; the panel and fee schedule as data (FEAT-PRM-02, legacy RWB-E6-030); the override with a reason (FEAT-PRM-04, RWB-S9-E6032-APP); the result received into the case (FEAT-PRM-05, RWB-S9-E6033-APP); the agency placement of a charged-off account (FEAT-PRM-06) and the fee (FEAT-PRM-07); the monthly scorecard (FEAT-PRM-08); the case of record and the work assignment, which are rwb-case's (P3); the measured return and the score products, which are rwb-source-data's (P1); the rule package and the decision ledger, which are rwb-decision's (P7); the right, which is rwb-access's (P4); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective is one sentence of the specification: FEAT-PRM-03 "Allocate work by measured return — Places work with the partner the scorecard rule picks, not by rotation or habit" (Epics 3 to 8 Specification v3, feature row; legacy RWB-E6-031). What D-RCV-60 changes is where each part of that sentence lives.

- **The panel is this service's data.** `partner`, `partner_instruction` and `partner_user` are S9's three tables in `rwb_partner` (context pack ownership rows), so the eligible set, the capacity state and the instruction that carries the pick are written here and nowhere else.
- **The number behind the pick is not this service's to invent.** The measured return of a partner is held as DP08 Partner performance, the Workbench product over this service's own partner and instruction records, and the score the pick rests on is DP11 Scores and route economics over `v_ace_score`; both are read on rwb-source-data's contract with their business date, and this service never reads an ACE view (DP-05).
- **The rule is governed, not coded.** The scorecard rule and its version are rule rows governed in rwb-decision; the evaluation runs here, so the same facts give the same pick and the version is recorded with the outcome. DP-04 is not part of this key's pattern set, and the absence is recorded rather than papered over (ASM-5364).
- **The version is what makes a pick defensible.** A pick recorded against "current" cannot be replayed after the panel or the scorecard moves, so the record carries the rule ID, the rule version and the scorecard version, and the panel and the scorecard are versioned data (BR-S9-003 as the wave 4 key states it).
- **Rotation is the failure this story removes.** A partner that improves gets work and a partner whose measured return falls stops getting it; nothing on the path counts what it placed last, and the rank order is kept in the record so the choice can be read back.
- **No capacity is a hold, not a placement.** R-WO-31 places nothing and escalates on the timer; a queue is never cleared by placing work where it cannot be worked.
- **The clock is the partner's service level, not a job.** S9 owns no job (context pack, jobs: none); the clock of an instruction is the `InstructionWorkflow` timer for the instruction type and partner type, and a Temporal Schedule is neither needed nor declared.
- **The edge has two faces.** Staff reach the placement on SCR-35 through gateway-bff; a firm reads its instructions and accepts them through the partner gateway (FAPI 2.0) that fronts rwb-partner (context pack, slide 8). DP-19 covers the composite route that carries the staff screen.

No business value moves: the scorecard weights, the panel thresholds, the capacity rule, the instruction types, the service level of each partner type and the ranking order are reference data or rule rows read with their version, never constants of the code.

### 3. Preconditions

- RWB-S9-E6031-CON is published: the three operations, their elements, the rights, the error envelope, the consumed rows and the fakes are baselined and handed to this story.
- The panel is populated as FEAT-PRM-02 leaves it: partner code, name, type, panel status, contract end, capacity state, fee schedule and service level, each with its version. Where a field of the panel beyond the seven the legacy Data table lists is needed, its name and list of values are Not specified in the source documents (GAP-3110; ASM-5362).
- The rwb-source-data products are published with their fakes: DP08 Partner performance, DP11 Scores and route economics and the freshness read that carries the business date and the load time of each product. Their operation names are Not specified in the source documents (GAP-3110; ASM-5362).
- The rwb-decision rule read is published with its fake and answers the scorecard rule at the version in force; its operation name is Not specified in the source documents (GAP-3110; ASM-5364).
- The rwb-case case read is published with its fake and answers the case reference, its state, its placement requirement and the work assignment reference; its operation name is Not specified in the source documents (GAP-3110; ASM-5368).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the placement, so the row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-35 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19). The partner-facing reads pass the partner gateway, whose route table is the edge story's.
- `partner`, `partner_instruction` and `partner_user` exist in schema `rwb_partner` from the DB story of this service; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_partner`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `v_ace_score` or `rwb_case` is refused by the database and fails the boundary test.
- The partner clock of each instruction type is the service level of the panel row; its duration per partner type is Not specified in the source documents (GAP-3110; ASM-5367).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E6031-CON when its tests pass.

### 4. Flow

1. A caller stage starts the placement: on R-WO-30 the write-off stage moves the case to `PLACEMENT_DECIDED` and calls the `issueInstruction` activity on queue `rwb-partner` with the case reference, the instruction type, the placement type and the rule version; the litigation, asset and debt-sale stages use the same activity when they instruct a firm, a vendor or a broker (context pack, slide 12 notes; Business Rules and Routing Logic v4, R-WO-30). A staff caller may drive the same path through `POST /cases/{caseId}/instructions`.
2. The activity reads the case on rwb-case, one hop with a 2 s budget and a breaker: the case reference, its state, its placement requirement and the assignment reference. It reads no `recovery_case` row (ASM-5368).
3. It builds the eligible set from `rwb_partner`: the partners of the required type whose `panel_status` admits allocation, whose `contract_end` has not passed and whose capacity is open. A partner under a conduct suspension is out of the set (R-UNI-29).
4. It reads the scorecard rule at its version in force from rwb-decision and the measured return of each eligible partner from DP08, with the business date of the product (ASM-5364).
5. It reads the score the pick rests on from DP11 and the freshness of that product. Where the product is behind its business date the run stops as X4: nothing is placed (DP-05; ASM-5369).
6. `ScorecardRanker` orders the eligible partners on measured return as the scorecard rule defines it and returns the order with the value behind each position. The order is kept for the record; it is never replaced by a rotation counter, a round-robin position, a last-placed pointer or a fixed share, and no such field exists in `rwb_partner`.
7. The top-ranked partner is the pick. Where the panel has no eligible partner or no open capacity, the run is held under R-WO-31 with no row, no event and the case unchanged, and the escalation is the timer of the caller's stage.
8. `PartnerDecisionRecordWriter` writes one decision record through the local decision-record library, **before the instruction exists**: the case reference, the instruction type, the candidate set with each partner's measured return, the pick, the rule ID, the rule version, the scorecard version, the business date of the products and the decided-at time. A failed write stops the run with nothing changed (legacy AC2; DP-03).
9. `InstructionWriter` inserts one `partner_instruction` row and its idempotency row in one `rwb_partner` transaction, with the instruction type, the partner, the case, `instructed_at`, the `due_at` the partner type's service level gives and the status `SENT` (ASM-5367).
10. `InstructionWorkflow` starts once for the instruction on queue `rwb-partner` with the instruction reference, the partner type and the due date, and holds the partner clock for that instruction type.
11. The outbox relay publishes `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` with the identifiers only. The event is written by the same transaction as the row, so the row and the fact cannot disagree (DP-09 is a real dependency of this step and is not in the plan's H row: ASM-5365).
12. The activity answers the caller with the instruction, the partner, the instruction type, `instructed_at`, `due_at` and the status; the caller's stage applies its own case move. This service writes no case state.
13. SCR-35 Placement and allocation shows the pick, the partner and the instruction in its loading and list states from this service through the gateway-bff composite route; the firm reads the same instruction through `GET /partner/instructions` behind the partner gateway (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no instruction row, no event, no clock, and the caller gets no instruction | MSG-P7-003 | AC2, TC-E6-031-02, TC-E6-031-04 |
| X2 | The caller does not hold the Partner portal C right of the placement | 403 before any read; nothing is placed and no record is written | MSG-P4-002 | TC-E6-031-03, AC7 |
| X3 | No partner on the panel is eligible, or none has open capacity | R-WO-31 holds the placement: no row, no event, no clock, the case unchanged, escalation on the caller's timer; no message ID is named for the hold | None named | AC4, TC-S9-E6031-01 |
| X4 | The DP11 score product is behind its business date | The run stops before any write; nothing is placed and the hold is reported with the product and its date | MSG-P1-001, whose text is Not specified in the source documents (GAP-3110; ASM-5369) | AC5 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The activity retries on the workflow's own schedule; nothing is written; a screen caller sees 503 with the platform envelope | None | AC1, X3 |
| X6 | The same placement arrives twice, or with the same `Idempotency-Key` | One row, one record, one event and one clock; the repeat returns the first answer | None | AC6, TC-S9-E6031-02 |
| X7 | The picked partner is suspended or its contract ends between the read and the write | The writer re-reads the panel row once inside the transaction and re-picks from the remaining rank order; if none remains, X3 | None | AC4 |
| X8 | A statement reaches another `rwb_*` schema, a `v_ace_*` view or a `recovery_case` row | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC7, section 17 |

X1 is legacy AC2 carried onto the slice, X2 is the third and fourth legacy test case, X3 to X7 are the panel, product and replay paths the rule names, and X8 is the schema and ACE boundary. The override with a reason is not an exception here: it is FEAT-PRM-04 and RWB-S9-E6032-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E6031-CON, the decision-record stub and the rwb-case, rwb-source-data and rwb-decision fakes, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The component names, the record's input payload and the activity's input shape are this story's choice; the rule, the messages, the operations, the tables, the topic and the queue are fixed |
| Valuable | Work goes to the partner with the best measured return, the choice is replayable with its versions, and no case is placed by habit |
| Estimable | One activity, one ranker, one record write, one row writer, one workflow start, four clients, one event and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic panel, synthetic products with a business date and the contract fakes, plus the hold, the stale product, the replay and the boundary cases |

### 7. Acceptance criteria

```gherkin
Feature: Allocate work by measured return

  Background:
    Given the panel of rwb-partner holds partners of the required type with their panel status, contract end, capacity and service level
    Given the scorecard rule is in force at its version and the panel carries its scorecard version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The pick is the partner the scorecard ranks first on measured return (new, D-RCV-60)
    Given the rwb-source-data contract mock returns DP08 with the measured return of each eligible partner for business date "2027-04-30" and DP11 with the score each pick rests on
    Given the rwb-case contract mock returns case "RW-2027-000831" at "PLACEMENT_DECIDED" with an instruction requirement
    Given the rwb-decision contract mock returns the scorecard rule at its version in force
    When the placement is started on case "RW-2027-000831"
    Then the partner the scorecard ranks first on measured return is picked
    And no rotation counter, round-robin position, fixed share or last-placed value is read, stored or honoured
    And the answer names the instruction, the partner, the instruction type, instructed_at, due_at and the status

  Scenario: AC2 Not recorded (legacy RWB-E6-031 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The pick is recorded with its rule and scorecard versions before the instruction exists (new, D-RCV-60)
    Given the panel holds four eligible partners and the measured return ranks "PRT-SYN-0031-A" first
    When the placement is started
    Then the decision record is written before the partner_instruction row
    And the record carries the case reference, the instruction type, the candidate set, the pick, the rule ID, the rule version, the scorecard version and the business date of the products
    And a forced failure of the record write leaves no row, no event and no clock

  Scenario: AC4 No eligible partner, or no open capacity, holds the placement (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2027-000832" at "PLACEMENT_DECIDED"
    Given every partner of the required type is out of the panel, past its contract end, under a conduct suspension or without open capacity
    When the placement is started
    Then the placement is held and no instruction is created
    And GET /partner/instructions answers no instruction for the case
    And the case is read back unchanged at "PLACEMENT_DECIDED"

  Scenario: AC5 A stale score product stops the placement (new, D-RCV-60)
    Given the rwb-source-data contract mock returns DP11 behind its business date for the placement date
    When the placement is started
    Then nothing is placed, no instruction is created and no event is published
    And the hold names the product and its business date

  Scenario: AC6 One placement carries one instruction, one event and one clock (new, D-RCV-60)
    Given the placement of case "RW-2027-000831" is accepted with one Idempotency-Key
    When the same placement arrives again with the same Idempotency-Key
    Then one partner_instruction row exists for the case
    And rwb.partner.InstructionIssued.v1 is published once on rwb.partner.events.v1 with the identifiers only
    And InstructionWorkflow on "rwb-partner" holds one partner clock for the instruction type
    And the replay returns the first answer and adds no row, no event and no second clock

  Scenario: AC7 The panel is this service's and the ACE data is not (new, D-RCV-60)
    Given the build of rwb-partner for this story
    When the boundary test inspects every statement, client and fixture
    Then no statement touches another rwb_* schema, a v_ace_* view or a recovery_case row
    And the measured return and the score arrive only on the rwb-source-data contract with their business date
    And the case state and the work assignment are read on the rwb-case contract and never written
```

AC2 is the legacy criterion word for word with its origin tag, and nothing else is added to it. AC1, AC3 to AC7 are new and test only what this story builds; the cross-service journey that legacy AC1 describes is proved by RWB-ITG-E6031-ITG and is not copied here. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-30 | Write-off | D9 | PLACEMENT_DECIDED | SOFT_RECOVERY_SELECTED | placement_type = soft_recovery and an agency on the panel has capacity | Place the account with the agency chosen on measured return and send the instruction | PLACED_WITH_AGENCY | Outsourced agency | Partner Portal, OA portal | same day on the portal |
| R-WO-31 | Write-off | D9 | PLACEMENT_DECIDED | NO_AGENCY_CAPACITY | no agency on the panel has capacity | Hold the placement and escalate on the timer | PLACEMENT_DECIDED | Partner and agency manager | Partner Portal | 5 working days |
| R-UNI-29 | Universal rules | All | ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | Suspend allocation, recall the affected cases, report to the partner review | PARTNER_RECALLED | Partner and agency manager | Partner Portal | same day |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days |
| R-LIT-23 | Litigation | D7 | PACK_VERIFIED | PACK_APPROVED | pack_verified_at set | Select the law firm by rule from the panel | FIRM_SELECTION | Workbench | Rules component, partner performance data | Same day |
| R-DIS-30 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | VENDOR_REQUIRED | asset_type = vehicle | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance | VENDOR_ALLOCATED | Auction and remarketing vendor | Rules component, Partner Portal | 2 working days |

The six rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" and the "partner performance data" are the scorecard rule of rwb-decision and the measured return of rwb-source-data read on their contracts, "Partner Portal" and "OA portal" are screens of this service's edge, and the case moves are written by rwb-case on the answer of this story. R-WO-30 and R-WO-31 are the placement itself; R-UNI-29 and R-UNI-45 are the suspension and the re-selection that re-enter the same pick; R-LIT-23 and R-DIS-30 show that one scorecard rule serves the law-firm, vendor and agency panels, which is why the pick is a service capability and not a write-off-only branch.

| ID | Rule | Source |
|---|---|---|
| BR1 | The panel, the partner users and the instructions are S9's: `partner`, `partner_instruction` and `partner_user` in `rwb_partner`, and no other service writes them | Context pack ownership rows; Arch v5 slide 41 |
| BR2 | The pick is by measured return against the scorecard, never by rotation, fixed share or last placed; the rank order is kept with the pick | REQ-S9-003; R-WO-30; legacy RWB-E6-031 |
| BR3 | The scorecard and the panel are versioned data and the version is recorded with every pick | ASM-5371; R-WO-30 |
| BR4 | The decision record is written before the instruction exists; a failed write leaves nothing placed and answers MSG-P7-003 | DP-03; legacy AC2 |
| BR5 | The ACE score and the measured return stay with rwb-source-data: this story holds no `v_ace_*` grant and takes both on the owner's contract with their business date | DP-05; context pack slide 8 |
| BR6 | No capacity is a hold and not a placement: R-WO-31 writes nothing and escalates on the caller's timer | R-WO-31 |
| BR7 | One placement carries one instruction, one fact and one clock; the `Idempotency-Key` makes the replay safe | TSD S9 (not in this WP's read set); ASM-5365 |
| BR8 | The case state and the work assignment are rwb-case's: this story reads them and answers the caller, and writes neither | ASM-5368 |
| BR9 | No person name, address, contact value or identity number enters `rwb_partner`, the record, the event, a log or a workflow input | Template and Rules §R7.2 (s17) |
| BR10 | No business value in code: the scorecard weights, the panel thresholds, the capacity rule, the instruction types, the service level by partner type and the rank order are reference data or rule rows read with their version | Legacy Guardrails; FEAT-PRM-02; ASM-5367 |

### 9. State transitions

The case state is rwb-case's and is not changed here: the caller's stage applies its own move on this story's answer (BR8). What this story owns is the state of the run and the row it writes.

| From (run) | Event | Condition | To |
|---|---|---|---|
| Waiting | The `issueInstruction` activity starts | The case and the panel are read | Ranking |
| Ranking | The rule and the measured return are read | The score product is current | Picking |
| Ranking | The score product is behind its business date | X4 | Held, nothing written, MSG-P1-001 |
| Picking | The rank order has an eligible partner with open capacity | The top-ranked partner is the pick | Recording |
| Picking | No partner is eligible or none has capacity | R-WO-31, X3 | Held, nothing written, escalation on the caller's timer |
| Recording | The record is written | X1 does not fire | Writing the row |
| Recording | The record write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Writing the row | The row, the idempotency key and the outbox row commit | The workflow starts | Answered |
| Answered | The clock is running and the fact is relayed | The activity returns | Done for this instruction |

| From (`partner_instruction.status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | A placement under R-WO-30 | The record is written and the panel row still admits allocation | One row, `SENT` |
| None, no row | A hold under R-WO-31 or a stale product | No capacity, no eligible partner, X4 | No row and no clock |
| `SENT` | The partner accepts or declines | The accept operation of this service, a later story of the module | Written there, not here |
| `SENT` | The partner clock passes its due date | R-UNI-25 or R-LIT-28 on the caller's route | Written on the caller's route, not here |

The status vocabulary beyond `SENT` is published by no source read for this WP, so the accept, decline, breach and recall values are recorded as a gap (GAP-3110; ASM-5362) and are not invented here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, RW-AGENCYMG, RW-CASEOWN, RW-TEAMMGR | Place the work: the Partner portal right C on `POST /cases/{caseId}/instructions`, and read the panel and the instructions |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE, RW-GUARANT, PT-AGENCY | Hold the Partner portal rights the legacy permission table gives them on the instruction: the U right belongs to the accept and result stories, not to this one |
| The 21 further R roles and 5 further U roles of the legacy permission table | R and U exactly as the table gives them, and no C |
| rwb-partner service identity | Runs the activity and the workflow, reads the case, the products and the rule, writes the record and the row, starts the clock and publishes the fact; it holds no grant on another schema and no `v_ace_*` grant |

The legacy permission table gives the capability area "Partner portal" with right R to the first row's roles and right U to the second row's roles, and the API sheet gives the placement right C ("Partner portal C", Epics 3 to 8 Specification v3). The C holders are read from the legacy U row because the sources name no separate C list, and that reading is an assumption (ASM-5370). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation on the contract and the guard is a service-template capability, so the check is stated here and built on RWB-PLT-E1037-CON and RWB-P4-E1037-CON (ASM-5370).

### 11. Data

| Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Write: the partner reference the pick names, carried on the instruction |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partner_code | Read: reported on the panel and the instruction answer |
| DF-PRT-003 | partner (S9, `rwb_partner`) | partner_name | Read: the name the screen shows |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partner_type | Read: with the instruction type, the filter of the eligible set and the source of the service level |
| DF-PRT-005 | partner (S9, `rwb_partner`) | panel_status | Read: only a partner whose status admits allocation may be picked; R-UNI-29 suspends allocation |
| DF-PRT-006 | partner (S9, `rwb_partner`) | contract_end | Read: a partner past its contract end is out of the set (R-UNI-26) |
| DF-PRT-007 | partner (S9, `rwb_partner`) | the seventh field of the legacy list | Not specified in the source documents (GAP-3110; ASM-5362) |
| partner_instruction (columns) | partner_instruction (S9, `rwb_partner`) | instruction reference, case reference, partner reference, instruction type, status, `instructed_at`, `due_at` | Write: one row per placement. The column list and its field IDs are Not specified in the source documents (GAP-3110; ASM-5362) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, scorecard version, inputs reference, outcome, decided at | Write through the local library, before the row exists |
| DF-WRK-009 to DF-WRK-016 | assignment (P3 rwb-case) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not written and not read as a table: the case and its assignment arrive on the rwb-case contract (ASM-5368) |
| DF-ACE-270 to DF-ACE-279 | v_ace_score (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not read: no `v_ace_*` grant. The score arrives on the DP11 contract with its business date |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule and its version arrive on the package read |
| Scorecard and panel version | panel reference data (S9, `rwb_partner`) | the version of the scorecard and of the panel in force | Read and recorded with the pick (ASM-5371) |

**No new table, no new column and no migration**: the three tables arrive with the DB story of this service, this story writes the instruction row and reads the panel row, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_partner` by the library's own migration (DP-03).

**No personal data.** The rows carry identifiers, a type, a status, two timestamps and a version. No name of a person, address, contact value or identity number enters `rwb_partner`, the record, the event, a log or a workflow input, and every fixture is synthetic. The instruction carries the partner organisation, never the customer.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the behaviour behind the operations whose shape RWB-S9-E6031-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` | The placement request in, the instruction of status 201 out, with the partner the scorecard picks (API-S9-002, "Issue an instruction to a partner by rule") | Partner portal C, scope applied | `Idempotency-Key` header |
| GET | `/partner/instructions` | The instructions placed with the caller's firm, with their partner, instruction type, `instructed_at`, `due_at` and status (API-S9-003) | Partner portal R | None, a safe read |
| GET | `/partners` | The panel: partner code, name, type, panel status, contract end and the capacity state | Partner portal R | None, a safe read |

The errors are 401, 403 with MSG-P4-002, 409 for a replay that conflicts, 422 with MSG-GEN-001 and 503 when a consumed contract or the library does not answer. The element names beyond the three the sources give are the contract's (RWB-S9-E6031-CON), and the accept, result and invoice operations of the module are neither built nor declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3110; ASM-5368)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its state, its placement requirement and the assignment reference; read only, faked |
| DP08 Partner performance, DP11 Scores and route economics and their freshness (operation names Not specified in the source documents (GAP-3110; ASM-5362)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The measured return per partner, the score the pick rests on and the business date and load time of each product; faked |
| The scorecard rule read in force (operation name Not specified in the source documents (GAP-3110; ASM-5364)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule and its version; faked |
| The access session of the caller (operation name Not specified in the source documents (GAP-3110; ASM-5370)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area and the right of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C in fact while this story's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-3110; ASM-5362).

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1`, with its retry and `.dlt` topics | the case reference | Identifiers only: the instruction, the case, the partner, the instruction type, `instructed_at`, `due_at`, the rule version and the scorecard version; no customer data |

The event is written to the outbox in the same transaction as the row and relayed after the commit, one event per placement (CloudEvents envelope, ADR-015). Its legacy identifier is EV-20 or EV-21 and the mapping of the two identifiers to their names is Not specified in the source documents (GAP-3110; ASM-5363); the name follows the naming rule of §R4. DP-09 is not in this key's pattern set and the outbox and inbox library it needs is recorded (ASM-5365).

#### 12.4 Events consumed

None. The placement is a command, not a fact: the caller's stage calls the `issueInstruction` activity of §12.5 and needs the result, which is the call-type answer the architecture gives for "another service must do a step and we need the result" (context pack, slide 12 notes). The service therefore declares no subscription for this story, and a build that subscribes to the write-off topic to learn of a placement fails the absence test. The instructions this service relays onwards are read by the firm on `GET /partner/instructions`, and the results, invoices and acceptances arrive on the operations of the other stories of the module.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction, started by the placement | `rwb-partner` in namespace `rwb-recovery` | Input: the instruction reference, the partner, the partner type, the instruction type and the due date; signals: the accept, decline, result and recall answers of the later stories; query: the remaining partner clock. Holds the partner clock of the instruction type and closes when the instruction ends |
| `issueInstruction` | Activity, the placement step | `rwb-partner` | The case reference, the instruction type, the placement type and the rule version in; the instruction, the partner, `instructed_at`, `due_at` and the status out, with the record, the row and the outbox written in one transaction |

The activity name is the one the context pack's call-type notes give as the example (`issueInstruction` on rwb-partner) and its input shape is a design choice fixed by no source document (ASM-5366). The workflow kit that hosts it is RWB-PLT-E1071-CON, which DP-10 would add and the plan's H row does not carry (ASM-5366). No child workflow for the case and no Schedule exists in this service.

#### 12.6 Schedules

None. S9 owns no job (context pack ownership rows, jobs: none), so this story registers no Temporal Schedule, no Quartz row and no shared job table; the only clock is the workflow timer of §12.5, which is a timer and not a schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The panel row of each partner; read for the eligible set, the capacity and the service level, and written only by the panel story |
| partner_instruction | S9 (`rwb_partner`) | The instruction of one placement; this story inserts one row and writes the columns of §11 |
| partner_user | S9 (`rwb_partner`) | The portal user of a firm; not touched by this story and named so the ownership is complete |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked decision record of the pick (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the replay and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The row of `InstructionIssued`, written in the same transaction |

Not owned and never read as a table: `recovery_case`, `assignment` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-read fake | Case `RW-2027-000831` at `PLACEMENT_DECIDED` with an instruction requirement and an assignment reference; a case that has moved on; no answer beyond 2 s | AC1, AC4, X5 |
| rwb-source-data DP08 fake | The measured return of four eligible partners for business date `2027-04-30`, ranking `PRT-SYN-0031-A` first; a partner with no record | AC1, AC3 |
| rwb-source-data DP11 and freshness fake | The score of each pick with its business date; a product behind its date; a product whose load failed | AC1, AC5 |
| rwb-decision rule fake | The scorecard rule at its version in force, with its weights and its thresholds as rows | AC1, AC3 |
| rwb-access session fake | A caller holding Partner portal C, and a caller holding R only | TC-E6-031-03, AC7 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-35 answer for the case, in its placement state | AC1 |
| Partner gateway fake | The firm-facing read of `GET /partner/instructions` behind FAPI 2.0 | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3110; ASM-5362, ASM-5364, ASM-5368, ASM-5370).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | `POST /cases/{caseId}/instructions`, `GET /partner/instructions` and `GET /partners` on `/api/recovery/partner/v1`; the case, the two products with freshness, the rule and the session reads; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1`; no subscription |
| Temporal | 1 workflow and 1 activity, 0 schedules | `InstructionWorkflow` with the partner clock and `issueInstruction` on `rwb-partner` |
| File | None | No file is read, built or delivered here; the instruction and its pack travel through the document and edge contracts, not as a file of this story |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `placement`; front end `src/modules/recovery/partner/PlacementAllocation.tsx`, the fragment SCR-35 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the row commit together or not at all. DP-05 is a prohibition in practice rather than a grant: `v_ace_score` is DP11's source and this service holds no `v_ace_*` grant, so the score and the measured return arrive on the owner's contract with their business date. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-35 reaches this service, one hop through the gateway; the partner-facing read uses the partner gateway of the same edge epic. DP-04, DP-06, DP-07, DP-08, DP-09, DP-10 and DP-14 are not in this key's pattern set although the step evaluates a rule, reads versioned reference data, checks a right, publishes a fact, starts a workflow and names a topic; each absence is recorded rather than added to the metadata (GAP-3110; ASM-5364, ASM-5365, ASM-5366, ASM-5370, ASM-5371).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `issueInstruction` | Activity | The placement step: reads the case, the panel, the rule and the products, writes the record, the row and the outbox row, starts the clock and answers |
| `EligibilityFilter` | Service | The eligible set: partner type, panel status, contract end, capacity and the conduct suspension of R-UNI-29 |
| `ScorecardRanker` | Service | The rank order on measured return as the rule defines it, with the value behind each position, and no rotation path |
| `PartnerDecisionRecordWriter` | Library adapter | Writes the record with the rule and scorecard versions before the row, hash-linked; refuses the run when the write fails |
| `InstructionWriter` | Repository | Inserts the row, the idempotency key and the outbox row in one `rwb_partner` transaction with the optimistic lock |
| `CaseClient` | Client | The case read of rwb-case, one hop, 2 s, breaker |
| `SourceDataClient` | Client | DP08, DP11 and the freshness read, with the business date, the load time and the stale path |
| `RulePackageClient` | Client | The scorecard rule at its version in force |
| `InstructionWorkflow` | Workflow | The partner clock of the instruction type, one execution per instruction |
| `PartnerInstructionController` | Controller | The three operations, the capability area and rights, the `Idempotency-Key` and the problem mapping |
| `PlacementAllocation` | React component | Shows the pick, the partner and the instruction on SCR-35, read only, with the hold, stale and refusal states |

**Database and migrations.** No Flyway file. The three tables arrive with the DB story of this service; the record, the idempotency key and the outbox row are library objects created in `rwb_partner` by the library's migration (DP-03, DP-09). No column is added for the case, the score, the measured return or the rule: those are facts of their owners and are referenced, not copied.

**Configuration and reference data.**

- The scorecard weights, the panel thresholds, the capacity rule, the instruction types and the service level of each partner type: reference data or rule rows with their version, never a constant (ASM-5367, ASM-5371).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the business date of a run is a parameter of the activity and not a constant.

**Build steps**

1. `issueInstruction` and its input record, registered on `rwb-partner`, with the transaction boundary of the step.
2. `CaseClient` and `SourceDataClient` against their fakes, with the business date, the load time of each product and the stale path (AC1, AC5, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the pick (AC1, AC3).
4. `EligibilityFilter` and `ScorecardRanker` over the panel, with the suspension, the contract end, the capacity and the no-eligible-partner path (AC1, AC4, X3, X7).
5. `PartnerDecisionRecordWriter` against the stub, with the failed-write path (AC2, AC3, X1).
6. `InstructionWriter` with the one transaction, the row, the idempotency row and the outbox row (AC1, AC6).
7. `InstructionWorkflow` and its partner clock, started once per instruction (AC6).
8. `PartnerInstructionController` with the three operations, the rights, the `Idempotency-Key` and the problem mapping, and `PlacementAllocation` on SCR-35 through the composite route fake and the partner gateway fake (AC1, AC6, X2).
9. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no write to `rwb_case`, `rwb_source_data` or `rwb_decision`, and no rotation field anywhere (AC7, BR2, BR5).

**Feature flag.** `rwb.partner.placement-v1`, a flag of the platform library; off means the activity holds the placement with no write, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the pick runs on a synthetic panel and synthetic products in SIT, the rank order decides and rotation never does, R-WO-31 holds with nothing written, a stale product stops the run, a replay writes once, a forced record failure changes nothing, no `v_ace_*` read and no foreign schema write exists in the build, and SCR-35 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record cannot be written before the instruction exists (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Partner portal C right calls the placement (X2) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of the request, the case or the panel row is absent or invalid | Enter {field}. |
| MSG-P1-001 | A data product the pick rests on is behind its business date (X4) | The text is Not specified in the source documents (GAP-3110; ASM-5369) |

The first three IDs and their text are the legacy message set of RWB-E6-031, copied unchanged; no message is reworded. MSG-P1-001 is the data-freshness message the wave 4 key uses for the same condition; its text is not in this WP's read set, so the row carries the placeholder and the gap, and the build must not invent wording of its own. The hold of R-WO-31 and the incident of X4 raise no message ID beyond this row.

### 15. Screens and states

SCR-35 Placement and allocation is served through the gateway-bff composite route (DP-19): the route calls rwb-partner for the pick and the instruction, rwb-case for the case and its state and rwb-source-data for the measured return and its business date; this story fixes the rwb-partner answers only, and the composite route and the field list of the screen belong to RWB-PLT-N001-CON. SCR-34 Partner list reads the panel of §12.1.

The legacy screen table gives the states "Loading; list" for both screens. The loading state is the read of the three contracts; the list state is the pick, the partner, the instruction type, `instructed_at`, `due_at` and the status, with the rank order behind the pick available as evidence. The hold of R-WO-31, the stale product of X4 and the refusals of §14 are the further states this story must render, and the override form of the partner manager is not one of them: it is FEAT-PRM-04. The firm's own view is `GET /partner/instructions` behind the partner gateway and carries no staff field.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-031-01 | AC1, AC3 | Component | Four eligible partners, DP08 ranked with `PRT-SYN-0031-A` first, DP11 and the rule on the fakes; the pick, the rank order, the record and the row asserted |
| TC-E6-031-02 | AC2 | Component | The decision-record stub stopped; nothing written, no event, no clock and MSG-P7-003 |
| TC-E6-031-03 | Access | Component | A caller holding Partner portal R and not C; 403 with MSG-P4-002 and no read |
| TC-E6-031-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; no `partner_instruction` row and no workflow start |
| TC-S9-E6031-01 | AC4 | Component | A panel with no eligible partner, then a panel with no open capacity, then a partner suspended between the read and the write; the hold with nothing written |
| TC-S9-E6031-02 | AC6, AC7 | Component | One placement replayed with the same `Idempotency-Key`; one row, one event, one clock; the boundary test over every statement and client |

The four legacy cases are those of RWB-E6-031 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. Their business journey, including legacy AC1, is proved by RWB-ITG-E6031-ITG with the `-ITG` copies, and this story writes none. The two `TC-S9-E6031-` cases are new and cover the criteria the split adds. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the scorecard weights, the panel thresholds, the capacity rule, the instruction types, the service level by partner type and the rank order stay reference data or rule rows with their version, never a constant, a default or a branch.
- No rotation: no counter, round-robin index, last-placed pointer, fixed share or queue position exists in the schema, the code, a cache or a workflow input, and a build that adds one fails the review (BR2).
- No personal data in `rwb_partner`, the record, the event, a workflow input or a log: identifiers, a type, a status, two timestamps and a version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR5).
- The case stays with rwb-case: no `recovery_case` row, no case-state column, no assignment write here (BR8).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The decision is recorded before the change; a build that writes a row outside the record's transaction fails the review (DP-03).
- No retired element is reintroduced: no Quartz job row, no shared job table, no monolith base, no data-lake extract and no event consumed as a command.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share (FSD S9 Requirements served; the split plan carries no requirement id for this slice, and the S9 FSD and TSD are not in this WP's extract set (GAP-3110)) | The ranker, the pick, the record and the instruction | TC-E6-031-01, TC-S9-E6031-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the panel and the instruction | TC-E6-031-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E6-031-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The outbox row of `InstructionIssued` in the placement transaction | TC-S9-E6031-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-031-01, TC-S9-E6031-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the instruction | TC-E6-031-02, TC-E6-031-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-031, disposition Split (rework); feature FEAT-PRM-03 |
| Legacy criteria | AC2, owned word for word by this story; AC1 proved by RWB-ITG-E6031-ITG |
| Source text | Legacy RWB-E6-031; Epics 3 to 8 Specification v3 (feature row FEAT-PRM-03, API rows for S9); Business Rules and Routing Logic v4 rows R-WO-30, R-WO-31, R-UNI-29, R-UNI-45, R-LIT-23 and R-DIS-30; context pack S9 |
| Test cases | TC-E6-031-01 to TC-E6-031-04, TC-S9-E6031-01, TC-S9-E6031-02 |
| Feature and screens | FEAT-PRM-03, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | R-WO-30, R-WO-31, R-UNI-29 and R-UNI-45, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the three operations, the elements, the rights, the error set, the tables and the fakes: RWB-S9-E6031-CON.
- The panel and the fee schedule as data, FEAT-PRM-02 and legacy RWB-E6-030: RWB-S9-E6030-APP.
- The override with a reason, FEAT-PRM-04 and R-WO-31's escalation beyond the hold: RWB-S9-E6032-APP.
- The result received into the case, FEAT-PRM-05, and the accept, decline, invoice and result operations of the module: the later stories of this service.
- The agency placement of a charged-off account and the fee (FEAT-PRM-06, FEAT-PRM-07), the monthly scorecard (FEAT-PRM-08) and the panel review, notice and contract exit (FEAT-PRM-10 to FEAT-PRM-12).
- The case of record, its state, the work assignment and the parent `CaseWorkflow`: rwb-case (P3).
- The measured return, the score and the freshness of their products: rwb-source-data (P1). The rule package and the decision ledger: rwb-decision (P7). The right and the guard: rwb-access (P4).
- The composite route and the screen field list of SCR-35 and SCR-34: RWB-PLT-N001-CON; the partner gateway route table: the edge stories of the same epic.
- The cross-service journey, its `-ITG` copies and the evidence: RWB-ITG-E6031-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
