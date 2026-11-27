# RWB-ITG-AD022-ITG Partner firms and partner users

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-AD022-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-AD-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Squad sizes at refinement (DOR-RWB-ITG-AD022-ITG-16) |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-ITG-AD022-CON (not built yet) |
| Integration dependencies | RWB-P4-E1022-APP, RWB-S9-AD022-APP (not built yet; stubs until live) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-022 as the wave 4 integration proof that a partner user opening the partner portal sees only the instructions placed with that user's firm, that the firm and the user are resolved from rwb-partner and never from a client parameter or a copy in rwb-access, and that a missing right or another firm's identifier returns nothing; the build of the partner firms, the partner users, the instructions and the portal is RWB-S9-AD022-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-AD022-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that a partner user opening the partner portal sees only the instructions placed with that user's firm, that the firm and the partner user are resolved from rwb-partner and never from a client parameter or a copy in rwb-access, and that a missing right or a cross-firm identifier returns nothing**, so that **partners see only the work placed with their firm, on the internal list and on the portal alike**.

This story builds the harness and the evidence, and nothing else. S9 rwb-partner owns the partner firm, the partner user, the partner instruction, the recorded results and the panel, and it answers the staff side with `GET /api/recovery/partner/v1/partners`, `POST /api/recovery/partner/v1/cases/{caseId}/instructions` and the instruction reads of Arch v5 slide 17, and the partner side with `GET /api/recovery/partner/v1/partner/instructions`, `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/accept` and `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`. The partner gateway in the DMZ, with the second factor and the FAPI 2.0 profile, is the only route into the portal and fronts rwb-partner. P4 rwb-access answers the internal session, the internal role and the Partner portal R right, and holds no partner user at all, because the Ownership Map ruling ASM-0072 keeps partner users with S9 and leaves P4 the internal role model only. The partner data room is S6's operation, `GET /api/recovery/debtsale/v1/partner/data-room/{lotId}`, and is out of scope here.

The harness therefore drives the two sign-ins, reads the partner list and the portal instruction list through S9's own operations, reads the session through P4's operation, and asserts a refusal by its status and its message. It builds no endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service, no row in any schema and no partner, instruction or user state. Where the internal list and the portal would be composed for a screen the path is the gateway-bff composite route (DP-19), every path is the owner's own base `/api/recovery/<short>/v1` (DP-13), and no service reads another service's tables (DP-05).

### 2. Business rationale

The legacy story RWB-AD-022 holds partner firms, their contracts and their panel status as data, requests one partner user per firm, and then states the whole point in one line: a partner sees only the work placed with that firm. The failure it is written against is quiet rather than loud — a law firm user who opens the portal and finds the instructions of another firm has been shown a case, a debtor and a piece of litigation strategy that the bank has no basis to disclose, and nothing in the ledger would ever record that the disclosure happened. The Ownership Map moves the source of every fact and none of the behaviour: the firm, the partner user, the instruction and the panel stay with S9 rwb-partner in `rwb_partner` (Arch v5 slides 17 and 41), the internal identity, the internal role and the rights stay with P4 rwb-access in `rwb_access` (Arch v5 slide 41), and the portal stays behind the partner gateway in the DMZ with a second factor and the FAPI 2.0 profile (Arch v5 slides 8, 20 and 41; ADR-019).

The split matters because firm scope is a fact about two services and one sign-in, and it is exactly the fact that a copy destroys. If rwb-access kept a partner user row, or if the firm were taken from a parameter the caller sends, the portal's idea of the firm and rwb-partner's idea of the firm could disagree, and the day they disagree is the day one firm's work is shown to another. That is why the Ownership Map ruling on `partner_user` (ASM-0072) is a rule of this story and not a filing decision: the partner user and its firm are resolved from rwb-partner, one owner, and the internal session is answered by rwb-access with the internal role only. Asserted inside one service this passes while the next component quietly reads a second copy; asserted across the two owners it fails the moment the copy exists.

The story owns the legacy AC1 (firm scope) and the cross-service criteria that no single slice can prove. Legacy AC2 — a firm whose contract ends today has its user accounts disabled and its open instructions recalled — is the S9 slice's and is not restated here: its expiry is `partner_user.valid_to` against the firm's `contract_end` and the recall is the instruction lifecycle, both inside rwb-partner, and RWB-S9-AD022-APP asserts them. What this story adds is the boundary: the firm is resolved from the partner user, a client-supplied firm is refused or ignored, another firm's identifier answers nothing, a caller without Partner portal R is refused with the right message, rwb-access holds no partner user, and every portal call is one hop on the partner base with a 2 s budget.

Decoupling follows the target. The partner and the instruction are read on `/api/recovery/partner/v1` and never from `rwb_partner`; the session and the right are read on `/api/recovery/access/v1` and never from `rwb_access`; the portal route is the partner gateway and, where a staff screen composes the same answers, the gateway-bff composite route (DP-19). No view is opened and no schema is queried by the harness, which is DP-05 applied as the rule that no service reads another service's tables: S9 answers the firm and the user, P4 answers the internal role, and neither reads the other's rows. The route specification of the portal, the name of the firm-scope field and the shape of the partner session are not fixed by any source read for this story, and that is carried as one gap and one assumption: GAP-0442 and ASM-0634.

### 3. Preconditions

- RWB-S9-AD022-APP and RWB-P4-E1022-APP are the two I stories of this harness, and a stub generated from each published contract answers from Day 1, so the lane never waits: until an I story lands its stub answers and the run is reported as a stub pass.
- The published contract of S9 rwb-partner is in the contract registry: the partner read, the portal instruction read, the accept and the results operations, the staff instruction operation and the two events of `rwb.partner.events.v1`.
- The published contract of P4 rwb-access is in the contract registry: `GET /api/recovery/access/v1/me/session` answers the caller's roles and rights, and the access contract publishes no partner-user read, because partner users are S9's (ASM-0072).
- The partner gateway in the DMZ is available in front of rwb-partner, with the second factor and the FAPI 2.0 profile, and it is the only route the partner identity uses (Arch v5 slides 8, 20 and 41; ADR-019).
- The harness runs in SIT, against the stubs and then against the owners as the two I stories land, and never against UAT or production.
- The two synthetic firms, their panel status and contracts, the two synthetic partner users and the two synthetic instructions are held in the fixture as data. No production data is read, copied or connected to, and no real partner identity is used.
- The portal route specification, the name of the firm-scope field on the portal read, and the shape of the partner session and MFA assertion: Not specified in the source documents (GAP-0442; ASM-0634). A cross-firm identifier is answered 404 with no instruction detail and carries no message. The partner_user is a table of S9 with the fields identity_ref, partner_id, role_code, valid_from and valid_to, taken from Logical Data Model DF-REF-212 to DF-REF-217 (GAP-3104); the rwb-access operation name and the names of EV-20 and EV-21 are Not specified in the source documents (GAP-3104).
- The permission matrix in force in SIT holds Partner portal R for RW-NPAMGR, RW-DEBTSALE, RW-LEGAL, RW-LITOFF, RW-ENFORCE, RW-CASEOWN, RW-TEAMMGR and RW-SALEOFF, and does not hold it for RW-OFF, which is the refused caller of AC4.
- The release date 28 February 2027 is tentative and is copied unchanged.
- No build dependency. Day 1, with both stubs in place from the first run.

### 4. Flow

1. Harness: loads the fixture: firm `LAW-A` and firm `LAW-B`, each with its partner_code, partner_type, panel_status and contract_end; partner user `PU-SYN-LAW-A-01` bound to `LAW-A` and partner user `PU-SYN-LAW-B-01` bound to `LAW-B`, each with its identity_ref, role_code, valid_from and valid_to; instruction `INS-SYN-LAW-A-01` placed with `LAW-A` on case `RW-2027-001101` and instruction `INS-SYN-LAW-B-01` placed with `LAW-B` on case `RW-2027-001102`, each with its instruction_type, instructed_at, due_at and status; business date `2027-02-28`. It takes a snapshot of both instruction lists before it reads anything. On Day 1 the stubs of §12.8 return the same records.
2. PartnerSignIn: signs `PU-SYN-LAW-A-01` in through the partner gateway in the DMZ with a second factor, and asserts that the call is answered on the portal route with the FAPI 2.0 profile and that no owner is reached before the second factor is presented (AC1, AC6).
3. SessionProbe: calls `GET /api/recovery/access/v1/me/session` on the P4 base with the partner user's portal session and asserts the internal role answer and the Partner portal R right, and that the answer holds no partner user and no firm (AC5).
4. AccessProbe: asserts that rwb-access holds no partner user: the session answer carries no partner user id and no firm id, the access contract publishes no partner-user read, and the only answer that names the firm or the user is S9's; a partner user row is never read from `rwb_access` (AC5, X7).
5. FirmScopeProbe: reads `GET /api/recovery/partner/v1/partners` as the `LAW-A` user and asserts exactly one firm, `LAW-A`, with its partner_code, partner_type, panel_status and contract_end (AC1, AC2).
6. InstructionProbe: reads `GET /api/recovery/partner/v1/partner/instructions` as the same user and asserts exactly one instruction, `INS-SYN-LAW-A-01`, with its instruction_type, instructed_at, due_at and status, and that `INS-SYN-LAW-B-01` is not in the answer (AC1, AC2).
7. FirmScopeProbe: repeats the instruction read with firm `LAW-B` carried in a client parameter of the kind the legacy portal accepted, and asserts the parameter is refused or ignored and the answer still holds only the instruction of `LAW-A`; the report records which of the two it was (AC2, X6).
8. FirmScopeProbe: calls `POST /api/recovery/partner/v1/partner/instructions/INS-SYN-LAW-B-01/accept` as the `LAW-A` user, and asserts the answer is 404 and carries no instruction detail of `LAW-B`, that `LAW-B`'s instruction and its own are both unchanged, and that the list re-read is identical to the snapshot (AC3, X3). The accept of the user's own instruction is not taken, because this story changes no instruction state.
9. Refused caller: signs in a synthetic RW-OFF caller that does not hold Partner portal R, calls `GET /api/recovery/partner/v1/partner/instructions`, and asserts 403 with MSG-P4-002 and no instruction in the answer (AC4, X4).
10. Hop check: from the recorded call set, asserts that every call is one hop on `/api/recovery/partner/v1` or on `/api/recovery/access/v1` with a 2 s budget and a breaker per downstream, that no call passes through a second service, and that no service's table is read at any point (AC6, X10).
11. EvidenceReport: writes one report keyed by story and partner user, naming the contract version of each hop, whether the hop was a stub or the owner, the two firms, the two instructions, the panel status and contract of the firm read, the refusal status and message, and the verdict of each of the six criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-AD-022-01-ITG (ITG AC1) | AC1 |
| X2 | The partner gateway answers the sign-in with no session | The run fails on AC1 and AC6 and the report names the gateway route, the second-factor assertion and the answer; no owner is called and no instruction is read | None, and no business message is specified for it | TC-AD-022-01-ITG (ITG AC6) | AC1 and AC6 |
| X3 | `LAW-A`'s user calls the identifier of `LAW-B`'s instruction and the answer carries instruction detail, or is not a 404 | The run fails on AC3 and the report names the caller's firm, the instruction identifier and the fields the answer carried; a 200 with an empty body is a failure too, because it confirms the identifier exists | None, and no cross-firm message is specified (GAP-0442; ASM-0634) | TC-AD-022-02-ITG (ITG AC3) | AC3 |
| X4 | A caller without Partner portal R is allowed to read the instruction list | The run fails on AC4 and the report names the caller role, the right, the operation and the answer; a 200 is a failure even when the answer is empty | MSG-P4-002 (expected, and missing) | TC-AD-022-03-ITG (ITG AC4) | AC4 |
| X5 | A firm in the fixture has no panel status, or a status that does not allow work to be placed | The run fails on AC1 and the report names the firm and the field that was empty; the harness never supplies a panel status of its own | None | TC-AD-022-01-ITG (ITG AC1) | AC1 |
| X6 | The client-supplied firm parameter is honoured, so the answer carries `LAW-B`'s instruction | The run fails on AC2 and the report names the parameter, its value and the instructions the answer carried; an ignored parameter passes, a honoured one fails | None | TC-AD-022-02-ITG (ITG AC2) | AC2 |
| X7 | rwb-access answers a partner user, or a partner user row is read from `rwb_access` at any point in the run | The run fails on AC5 and the report names the field, the hop and the owner it came from, because a second copy of the partner user is the drift this story exists to catch | None | TC-AD-022-01-ITG (ITG AC5) | AC5 |
| X8 | The partner gateway does not answer inside the budget | The run fails on AC6 and the report names the route, the elapsed time and the budget; no criterion is marked passed on a timeout | None | TC-AD-022-01-ITG (ITG AC6) | AC6 and AC8 |
| X9 | rwb-partner answers 5xx, or answers a list without its firm scope | The run fails on AC1 and AC2 and the report names the operation, the status and the fields of the answer; a 5xx is never read as an empty list, because an empty list is the answer a broken scope rule also produces | None | TC-AD-022-02-ITG (ITG AC2) | AC1, AC2 and AC8 |
| X10 | A hop reads a table or a view directly instead of calling the owner | The run fails on AC6 and AC5 and the report names the schema, the table and the call that opened it, because a direct read is a pass that proves nothing about the contract | None | TC-AD-022-01-ITG (ITG AC6) | AC5 and AC6 |

X1 to X7 are the exception paths of the legacy story read across the two owners; X8 to X10 are the suite's own failure modes, so that a missing answer, a broken scope rule or a direct read never becomes a pass. Only two business messages exist for this story, in section 14; where a source specifies none the message column says so and the run asserts the status and the absence of detail instead.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only waits are RWB-S9-AD022-APP and RWB-P4-E1022-APP, and their fixtures answer until they land; the harness owns no schema and no table |
| Negotiable | The fixture layout, the two firm and user keys, the business date, the report shape and the pass or fail gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves across two services and one portal route what no single slice can prove: the firm comes from the partner user, a client parameter does not move it, another firm's identifier answers nothing, rwb-access holds no partner user, and the missing right is refused with the right message |
| Estimable | One runner, one stub set, one two-firm fixture, five probes and one report |
| Small | Fits in one sprint with its three test cases and no service code and no schema change |
| Testable | Each criterion asserts a status, a message, a field of an answer, the absence of a field, or the recorded call set; every firm, user and instruction key is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Partner firms and partner users - wave 4 integration harness

  Background:
    Given the environment is SIT and no production data and no real partner identity are used
    Given the synthetic firm "LAW-A" and the synthetic firm "LAW-B" are held in the fixture as data, each with its partner_code, partner_type, panel_status and contract_end
    Given the partner user "PU-SYN-LAW-A-01" is bound to "LAW-A" and the partner user "PU-SYN-LAW-B-01" is bound to "LAW-B"
    Given the instruction "INS-SYN-LAW-A-01" is placed with "LAW-A" and the instruction "INS-SYN-LAW-B-01" is placed with "LAW-B"

  Scenario: AC1 Firm scope (legacy RWB-AD-022 AC1)
    Given a law firm user
    When they open the partner portal
    Then only instructions placed with their firm show

  Scenario: AC2 The firm is resolved from the partner user and never from a client parameter (new, D-RCV-60)
    Given the partner user "PU-SYN-LAW-A-01" signs in through the partner gateway with a second factor
    When the user reads GET /api/recovery/partner/v1/partner/instructions
    Then the answer holds "INS-SYN-LAW-A-01" and not "INS-SYN-LAW-B-01"
    And GET /api/recovery/partner/v1/partners answers only the firm the partner user belongs to
    And a request that carries firm "LAW-B" as a client parameter is refused or ignored, and the answer still holds only the instructions of "LAW-A"

  Scenario: AC3 An instruction of another firm is not returned by its identifier (new, D-RCV-60)
    Given the partner user "PU-SYN-LAW-A-01" is signed in through the partner gateway
    When the user calls POST /api/recovery/partner/v1/partner/instructions/INS-SYN-LAW-B-01/accept
    Then the answer is 404 and it carries no instruction detail of "LAW-B"
    And no instruction of "LAW-B" is returned by the portal instruction list of "LAW-A"
    And the instruction of "LAW-A" and the instruction of "LAW-B" are both unchanged

  Scenario: AC4 A caller without Partner portal R is refused with MSG-P4-002 (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" that does not hold Partner portal R
    When the caller reads GET /api/recovery/partner/v1/partner/instructions
    Then the answer is 403 with "MSG-P4-002"
    And no instruction is returned

  Scenario: AC5 The partner user and its firm come from rwb-partner and rwb-access holds no partner user (new, D-RCV-60)
    Given the partner user "PU-SYN-LAW-A-01" is signed in through the partner gateway
    When the session is read through GET /api/recovery/access/v1/me/session
    Then the session answers the internal role and the rights of the caller only
    And no partner user and no firm is answered by rwb-access
    And the partner user and its firm are read only from rwb-partner
    And a partner user row is never read from "rwb_access"

  Scenario: AC6 Every portal call is one hop on the partner base with a 2 s budget (new, D-RCV-60)
    Given the partner user "PU-SYN-LAW-A-01" is signed in through the partner gateway
    When the partner list and the portal instruction list are read
    Then every call is one hop on /api/recovery/partner/v1 with a 2 s budget and a breaker per downstream
    And no call passes through a second service
    And no service's table is read by any hop of the run

  Scenario: AC7 Every business rule of section 8 is covered by a criterion or a test case of this story (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the story is reviewed before the run
    Then each of BR1 to BR10 is covered by at least one criterion of section 7 or one test case of section 16

  Scenario: AC8 A consumed call that fails or does not answer fails the run and is never read as an empty answer (new, D-RCV-60)
    Given the partner user "PU-SYN-LAW-A-01" is signed in through the partner gateway
    When a consumed call answers a 5xx or does not answer inside the budget
    Then the run fails on that call and the report names the operation, the status and the elapsed time
    And no criterion is marked passed on that call
```

Legacy AC2 (a firm whose contract ends today has its user accounts disabled and its open instructions recalled) is owned by RWB-S9-AD022-APP and is not restated here: it is the expiry of the partner user against the firm's contract end and the recall of the instruction, both inside rwb-partner. AC1 is the business outcome the whole boundary has to reach, and it is asserted exactly as the legacy story words it.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner user sees only the instructions placed with that user's firm, on the partner portal and on the internal list alike | Legacy RWB-AD-022 story line and AC1, Administration Stories v3 lines 1804 and 1811 to 1814 |
| BR2 | The partner firm, the partner user and the panel status are S9 rwb-partner's data in `rwb_partner`, and no other service holds a copy of the firm or of the partner user | Arch v5 slide 41 (S9 owns panel, partner users, instructions, results, fees, scorecards) and slide 17 (DB writes schema rwb_partner); ASM-0072 |
| BR3 | P4 rwb-access keeps the internal role model, answers the internal session and the Partner portal R right, and holds no partner user | Arch v5 slide 41 (P4 owns Recovery roles as data, scope, masking policy, DoA table, access log); ASM-0072 |
| BR4 | The firm is resolved from the partner user on every portal call and never from a parameter the caller supplies; a supplied firm parameter is refused or ignored | Derived from AC1 and from the gap that fixes no field name for it (GAP-0442; ASM-0634) |
| BR5 | An instruction of another firm is not returned or acted on by its identifier, and the answer carries no detail of it | Legacy AC1, Administration Stories v3 lines 1811 to 1814 |
| BR6 | A caller without Partner portal R is refused with MSG-P4-002 and no instruction is returned | Legacy permission table and messages, Administration Stories v3 lines 1845 to 1854 |
| BR7 | Partners reach the portal only through the partner gateway in the DMZ, with a second factor and the FAPI 2.0 profile; staff reach the same data through the internal edge | Arch v5 slide 17 (partner portal `/partner/v1/*` FAPI 2.0; via partner gateway, MFA), slides 8 and 20, ADR-019 |
| BR8 | Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a breaker, never an in-process call and never a second hop | DP-13, DP-19, ADR-020 |
| BR9 | No service reads another service's tables: the firm, the user and the instruction come from S9's contract, the session and the right from P4's, and the data room of S6 is a separate owner and a separate story | DP-05, DP-01; Arch v5 slides 17, 19 and 41 |
| BR10 | The instruction lifecycle, its SLA timers and the contract-end disablement and recall are S9's, run by InstructionWorkflow on `rwb-partner`, and this story observes them without changing them | Arch v5 slide 17 (InstructionWorkflow, SLA timers, issueInstruction, recordResult); Temporal and Drools design slide 25; legacy AC2 |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S9-AD022-APP for the firm, the user and the instruction, and in RWB-P4-E1022-APP for the session, the role and the right.

### 9. State transitions

None. The story reads and refuses: it changes no partner, no partner user, no partner instruction and no record of either service. The two sign-ins create a portal session and an internal session, which are the edge's, and the refused accept of another firm's instruction changes nothing on the instruction; every criterion of section 7 is a read, a refusal or an absence.

The transitions the legacy key does have are S9's and are asserted by RWB-S9-AD022-APP: the instruction moves from SENT through ACCEPTED, IN_PROGRESS and DONE or RECALLED, and the partner user's binding ends with `valid_to` no later than the firm's contract end, which is the contract-end disablement and the recall of legacy AC2. The harness never sets a state it then asserts, and a state it had set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, RW-DEBTSALE, RW-LEGAL, RW-LITOFF, RW-ENFORCE, RW-CASEOWN, RW-TEAMMGR, RW-SALEOFF | Hold Partner portal R on the staff side and may read the partner and the instruction list; they are the roles of the legacy permission table, which also names further holders |
| The partner user | Is S9's data, bound to one firm and one partner role, and holds the portal identity; it is the identity the portal route authenticates, and the run holds its firm and its role in the fixture, never a person |
| The partner gateway | Enforces the second factor and the FAPI 2.0 profile before rwb-partner is reached, and is the only route the partner identity uses |
| RW-OFF | Holds no Partner portal R and is the refused caller of AC4 |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S9 holds the firm, the partner user, the instruction and the panel and answers the portal; P4 answers the session, the internal role and the right; they make every value the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end | Read through the rwb-partner contract; the harness writes nothing |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code | Read through the rwb-partner contract; the harness writes nothing |
| DF-REF-212 to DF-REF-217 | partner_user | identity_ref, partner_id, role_code, valid_from, valid_to | Read through the rwb-partner contract, as the binding of the user to the firm; the harness writes nothing |
| DF-REF-034 to DF-REF-038 | role | role_code, role_name, role_class, default_scope | Read through the rwb-access contract, for the internal role of the caller |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The partner, the partner instruction and the partner user are S9's in `rwb_partner`; the role is P4's in `rwb_access`, and its `role_class` LOV names a partner-user class without any partner user row being held there. The harness owns no table and writes no row: it holds the two firms, their users, their instructions and their panel status in its own fixture as data, and it reads every asserted value back through the owner. `partner_user` has six fields in the data dictionary and is read for the binding only; its `identity_ref` is the partner identity directory reference and never a name, an address or an identity number, and the harness records the reference and the firm relation, never a personal value. The harness writes nothing.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The firm the partner user belongs to, with its panel status and its contract end (AC1, AC2, AC5) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions placed with that firm, on the portal list; the list of the other firm is the absence it asserts (AC1, AC2, AC3, AC6) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/accept` | S9 rwb-partner | The only published portal operation that takes an instruction identifier, so it is where another firm's identifier is called; the run asserts 404 and no detail, and takes no accept on its own instruction (AC3) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The internal role and the Partner portal R right, and the proof that the answer holds no partner user and no firm (AC4, AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-13, DP-19; ADR-020). No operation is invented in this story: each path is the owner's published operation in the Ownership Map. The Ownership Map publishes no instruction-by-id read for S9 and no partner-user read for P4, so the cross-firm identifier is called on the accept operation, which is published, and the absence of a partner user in rwb-access is asserted from the session answer and from the published contract set, never from an operation that does not exist. The partner data room of S6 is not consumed: it is a buyer-facing operation on `/api/recovery/debtsale/v1/partner/data-room/{lotId}` and belongs to the debt sale story, and nothing in this proof needs it.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness consumes no topic in this story: the two firms, their users and their instructions are fixture data, and every criterion is a read, a refusal or an absence. `rwb.partner.InstructionIssued.v1` and `rwb.partner.PartnerResultSubmitted.v1` are the two events of the S9 contract (Arch v5 slide 43, rows 20 and 21) and they belong to the instruction lifecycle that RWB-S9-AD022-APP builds and asserts; this run places no instruction and records no result, so it counts no publication and replays none. A run that seeded its instructions through the staff instruction operation would publish an InstructionIssued event and would change instruction state, which section 9 rules out for this story.

#### 12.5 Workflows and activities

None added. The harness observes InstructionWorkflow, S9's workflow on the task queue `rwb-partner` in the `rwb-recovery` namespace, as the workflow that carries an instruction placed with a firm, its SLA timers and its `issueInstruction` and `recordResult` steps (Arch v5 slide 17; Temporal and Drools design slide 25). It is observed from its history for the two instructions of the fixture and it is not built, started or changed here: no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The instruction lifecycle runs on its own SLA timers inside InstructionWorkflow, and the harness waits on nothing: it reads the two instructions as the fixture holds them and starts no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-05); partner, partner_instruction and partner_user are S9's in `rwb_partner`, and role is P4's in `rwb_access`.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-partner (S9) | `GET /partners`, `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/accept` | Firms `LAW-A` and `LAW-B` with their partner_code, partner_type, panel_status and contract_end; one instruction per firm with its case, type, dates and status; the partner read and the instruction list answer only the firm of the signed-in partner user, and a client-supplied firm parameter is ignored, never honoured; the accept of `INS-SYN-LAW-B-01` for the `LAW-A` user answers 404 with no instruction detail; a firm with no panel status answers the empty field for X5, and a 5xx variant answers for X9 |
| Stub for rwb-access (P4) | `GET /me/session` | Answers the internal role and the rights of the partner user, including Partner portal R, and no partner user and no firm; answers RW-OFF without Partner portal R with 403 and MSG-P4-002; a variant that answers a partner user is the X7 failure |
| Stub for the partner gateway | The portal route, the second factor and the FAPI 2.0 profile | Accepts the synthetic partner identity with a second factor and forwards one hop to the portal read of rwb-partner; refuses a call that presents no second factor; answers the timeout variant of X8 |
| Partner fixture | The two firms, their users, their instructions and the panel status | `LAW-A` and `LAW-B` as data, `PU-SYN-LAW-A-01` and `PU-SYN-LAW-B-01` bound one to one, `INS-SYN-LAW-A-01` and `INS-SYN-LAW-B-01` on their own cases, and the business date `2027-02-28` |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The portal route specification, the firm-scope field name and the partner session and MFA assertion shape are Not specified in the source documents (GAP-0442; ASM-0634). A cross-firm identifier is answered 404 with no instruction detail and carries no message (GAP-0442). The run holds them as configuration and asserts the shape of the answer, never a value it invented.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 4 consumed, one hop each on `/api/recovery/partner/v1` and `/api/recovery/access/v1` with a 2 s budget (DP-13, DP-19; ADR-020) |
| Kafka | None published and none consumed; the two partner events stay with the S9 slice of section 12.4 |
| Temporal | None added; InstructionWorkflow on `rwb-partner` observed from its history, with its SLA timers and its issueInstruction and recordResult steps |
| File | None. No document, upload or claim-check is transferred or read by this story |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through the owner's contract; no service reads another service's tables | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route, and the partner gateway for the portal | H RWB-PLT-N001-CON |

DP-05 is applied here as the rule that no service reads another's tables: the firm, the partner user and the instruction are S9's and the session and the right are P4's, and the harness reads each only through its owner. DP-13 adds no dependency: the partner and the session paths are on each owner's own base and there is no shared base left. The H dependency DP-19 adds, RWB-PLT-N001-CON, is a platform story delivered in the platform wave and is not repeated in the metadata H field of this story, which stays None. The blocking dependencies are the two I stories, RWB-S9-AD022-APP and RWB-P4-E1022-APP, which replace their stubs; until they are live the run uses the stubs, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| PartnerSignIn | Service | Signs the synthetic partner user in through the partner gateway with a second factor, records the portal route and the FAPI 2.0 profile, and holds the synthetic partner identity and its firm |
| FirmScopeProbe | Service | Reads the partner and the instruction list, asserts the one firm and its panel status, repeats the read with a client-supplied firm, and calls another firm's identifier |
| InstructionProbe | Service | Reads the portal instruction list and asserts the one instruction of the firm with its type, dates and status, and the absence of the other firm's instruction |
| AccessProbe | Service | Asserts that rwb-access answers the internal role and the right only, and that no partner user and no firm is answered or read from `rwb_access` |
| SessionProbe | Service | Reads `GET /api/recovery/access/v1/me/session`, asserts the role and the Partner portal R right, and holds the refused caller of AC4 |
| StubSet | Fake | The three stubs and the partner fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report keyed by story and partner user, with the two firms, the two instructions, the refusals and the verdict of each criterion, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S9-AD022-APP and RWB-P4-E1022-APP land, on the synthetic firms `LAW-A` and `LAW-B`, the partner users `PU-SYN-LAW-A-01` and `PU-SYN-LAW-B-01`, the instructions `INS-SYN-LAW-A-01` on case `RW-2027-001101` and `INS-SYN-LAW-B-01` on case `RW-2027-001102`, and the business date `2027-02-28`. The harness seeds nothing by hand and never writes a schema row. The portal route, the firm-scope field name and the partner session and MFA assertion shape are Not specified in the source documents (GAP-0442; ASM-0634).

**Build steps**

1. Generate the three stubs and the partner fixture from the published contracts and pin each contract version in the run report (contract version Not specified in the source documents (DOR-RWB-ITG-AD022-ITG-23)); fail the run on a mismatch (X1).
2. Build PartnerSignIn: the portal sign-in with a second factor, the route recorded, and the firm and the role of the synthetic user held as data (AC1, AC6, X2).
3. Add SessionProbe: the session read returns the internal role and Partner portal R, and the report names them (AC5).
4. Add AccessProbe for AC5: the session answer carries no partner user and no firm, the access contract publishes no partner-user read, and no hop reads `rwb_access`; a stub that answers a partner user fails the run (X7).
5. Add FirmScopeProbe for AC1 and AC2: the partner read returns one firm with its panel status and contract end, and a firm with no panel status fails the run (X5).
6. Add InstructionProbe for AC1 and AC2: the portal list returns the one instruction of the firm, and the other firm's instruction is absent (X9).
7. Add the firm parameter and the cross-firm identifier to FirmScopeProbe for AC2 and AC3: the client-supplied firm is refused or ignored and is recorded as which, and another firm's identifier answers 404 with no detail and changes nothing (X3, X6).
8. Add the refused caller of AC4 through the session read and the instruction list, and assert 403 with MSG-P4-002 and no instruction (X4).
9. Add the hop and budget check for AC6, the EvidenceReport and the gate, and swap a stub for the real owner as each I story lands (X8, X10).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Screens, states and reference data.** This story builds no screen, so SCR-34 (P3) and its empty, loading, error and no-access states are specified by P3, not here. The harness reads no list or parameter from a reference-data contract, so DP-06 and DP-07 do not apply; the client-supplied firm in step 7 is a test input.

**Done when.** The tests of section 16 pass against the fakes and again against both I stories when they land, and the wave entry check holds a run report keyed by story and partner user that names, for every call, the contract version and whether the hop was a stub or the owner.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-P4-002 is asserted with the refused read of the instruction list by the RW-OFF caller (step 9, AC4). MSG-GEN-001 is the general message of the legacy story and is asserted where a requested read is short of a required field, naming the missing field; the legacy story carries it and this run changes neither its text nor its use. No message is specified in any source read for a cross-firm identifier or for a gateway refusal: the 404 of AC3 therefore carries no business message and the run asserts the status and the absence of instruction detail instead, and the gateway refusal of X2 is asserted the same way. That absence is part of GAP-0442 and ASM-0634.

### 15. Screens and states

The legacy story's screens are SCR-34 Partner list and PRT-01 Partner home, and neither is built or rendered here: the harness calls the operations behind them and reads the states through the owners. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0442; ASM-0634).

| State | Read through | What the run asserts |
|---|---|---|
| Loading | The partner gateway route and the portal reads | The call is on the portal route with a second factor and the answer arrives inside the 2 s budget and the breaker |
| List | S9 partner read and portal instruction read | One firm with its panel status and contract end, and one instruction with its type, dates and status, for the firm of the signed-in user |
| Refused | P4 session read and the refuse answer | 403 with MSG-P4-002 for the caller without Partner portal R, and 404 with no detail for another firm's identifier |
| No instruction | S9 portal instruction read | A firm with no instruction answers an empty list and never the instruction of another firm; the empty answer is never read as a 5xx |
| Loading | Not specified in the source documents (CG-ALL-970) | Not specified in the source documents (CG-ALL-970) |
| Empty | Not specified in the source documents (CG-ALL-970) | Not specified in the source documents (CG-ALL-970) |
| Error | Not specified in the source documents (CG-ALL-970) | Not specified in the source documents (CG-ALL-970) |
| No access | Not specified in the source documents (CG-ALL-970) | Not specified in the source documents (CG-ALL-970) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-022-01-ITG | AC1 (legacy); ITG AC1, AC5 and AC6 | End to end | The two firms, their two users and their two instructions, the portal sign-in with a second factor, the partner and instruction reads, the session read, and the recorded call set |
| TC-AD-022-02-ITG | ITG AC2 and AC3 | Integration | The same user reading with firm `LAW-B` in a client parameter, and calling `INS-SYN-LAW-B-01` on the accept operation, with both instruction lists read before and after |
| TC-AD-022-03-ITG | Access; ITG AC4 | Component | A synthetic RW-OFF caller without Partner portal R, and a read short of its required field |
| TC-AD-022-04-ITG | ITG AC7; BR1 to BR10 | Not specified in the source documents (NEWAC-RWB-ITG-AD022-ITG-AC7) | Not specified in the source documents (NEWAC-RWB-ITG-AD022-ITG-AC7) |
| TC-AD-022-05-ITG | ITG AC8 | Not specified in the source documents (NEWAC-RWB-ITG-AD022-ITG-AC8) | Not specified in the source documents (NEWAC-RWB-ITG-AD022-ITG-AC8) |

The AC column names the legacy test case each -ITG copy derives from and the ITG criteria it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. The legacy test cases TC-AD-022-01 to TC-AD-022-03 are kept as the `-ITG` copies with the legacy Covers (AC1, AC2, Access): the legacy Covers of TC-AD-022-01 is AC1 and is AC1 here, the legacy Covers of TC-AD-022-03 is Access and is AC4 here, and TC-AD-022-02 is the copy whose legacy AC2 (the contract-end disablement and the recall) stays with RWB-S9-AD022-APP — the -ITG copy asserts the same firm boundary from the portal side, which is the answer the firm's user gets when the firm scope moves. AC5 and AC6 have no legacy test case of their own in this key and are folded into the one end-to-end run of TC-AD-022-01-ITG.

### 17. Guardrails

- No business value in code: the two firms, their panel status and contracts, the two partner users and their bindings, the two instructions, the business date, the report layout and the gate are data.
- No personal data anywhere: the run holds partner and user keys only, and never a name, an address, an identity number, a telephone number or a document; the partner identity is the directory reference of the synthetic binding and nothing else.
- No cross-schema read: the firm, the partner user and the instruction come from S9's contract, the session and the right from P4's, and a hop that opens `rwb_partner` or `rwb_access` fails the run (DP-05).
- P4 holds no partner user: a partner user answered by rwb-access, or read from `rwb_access`, fails the run, because that copy is the drift the story exists to catch (ASM-0072).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where a screen would (DP-13, DP-19; ADR-020).
- The second factor is on the partner gateway and is never bypassed by the harness: a run that reached rwb-partner without presenting it is not a pass (ADR-019).
- SIT only, with synthetic identities only: the harness never runs against UAT or production and never writes a row by hand or sets a state it then asserts.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-022 Partner firms and partner users | Recovery Workbench Administration Stories v3, lines 1792 to 1864 | Sections 1, 2, 3, 11, 14 and 19 of this file |
| Legacy AC1, verbatim | The same, lines 1811 to 1814 | Section 7, AC1, marked (legacy RWB-AD-022 AC1) |
| Legacy AC2, the contract ends and the users are disabled with open instructions recalled | The same, lines 1816 to 1819 | Named in sections 2, 8 and 9 as RWB-S9-AD022-APP's; not restated here (section 19) |
| Legacy test cases TC-AD-022-01 to TC-AD-022-03 and their Covers (AC1, AC2, Access) | The same, lines 1856 to 1862 | Section 16, kept as the `-ITG` copies |
| Legacy data table, partner and partner_instruction field ranges | The same, lines 1822 to 1827 | Section 11 |
| Legacy endpoints, screens, permission table and messages | The same, lines 1829 to 1854 | Sections 12.2, 15, 10 and 14 |
| Arch v5 slide 17: S9 IN staff `GET/POST /partners`, `/instructions`; partner portal `/partner/v1/*` FAPI 2.0; InstructionWorkflow with SLA timers; partner gateway, MFA | Architecture v5 Text Extract v1, lines 1245 to 1256 and 1270 to 1272 | Sections 1, 2, 8, 12.2, 12.5 and 13 |
| Arch v5 slide 41: S9 owns panel, partner users, instructions, results, fees, scorecards; P4 owns Recovery roles as data | The same, lines 2878 to 2903 | Sections 1, 2, 8 and 11 |
| Arch v5 slides 19 and 43: the data room is S6's; InstructionIssued (row 20) and PartnerResultSubmitted (row 21) are S9's | The same, lines 1393 to 1403 and 2944 to 2962 | Sections 1, 12.2, 12.4 and 19 |
| Arch v5 slides 8 and 20: the partner gateway in the DMZ, FAPI 2.0, partners do not use the staff edge | The same, lines 552, 681, 1456 to 1462 and 2560 | Sections 1, 2, 8 and 17 |
| ASM-0072: partner users stay with S9 rwb-partner and P4 keeps the internal role model only | Ownership Map v1 ruling on `partner_user`; Arch v5 slide 41 | Sections 1, 2, 8, 11, 12.7 and 17 |
| Ownership Map rows for `partner`, `partner_user`, `partner_instruction`, `role`, `permission` | `_work/msr/plan/ownership.json` | Sections 1, 11 and 12.7 |
| Ownership Map rows for `GET /partners`, `GET /partner/instructions`, `POST /partner/instructions/{instructionId}/accept`, `POST /partner/instructions/{instructionId}/results`, `POST /cases/{caseId}/instructions`, `GET /partner/data-room/{lotId}`, `GET /me/session` | The same | Sections 1 and 12.2 |
| DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application, and section 2 |
| ADR-019, the edge with gateway-bff and the partner gateway; ADR-020, contract-first REST with one hop and 2 s | Architecture Decision Records v4, with both as added by Template and Rules v1 §R8.4 | Sections 1, 2, 8 and 12.2 |
| DF-PRT-001 to DF-PRT-007, DF-PRT-008 to DF-PRT-016, DF-REF-212 to DF-REF-217, DF-REF-034 to DF-REF-038 | Logical Data Model and Data Dictionary v9 | Section 11 |
| The portal route, the firm-scope field name, the partner session and MFA assertion shape, the partner_user field set as published, and the answer and message for a cross-firm identifier | No source read for this story specifies them | Sections 3, 5, 12.8 and 14, as GAP-0442 and ASM-0634 |
| Release 28 February 2027 | The WP story line and the legacy story, line 1796 | The metadata table of this file; the date is tentative, is copied unchanged, and is never raised as a gap, even though the business-epic tag is EP08 |

### 19. Out of scope

- RWB-S9-AD022-CON and RWB-S9-AD022-APP: the partner firms, the partner users, the panel, the instructions, the results and the portal reads themselves.
- RWB-P4-E1022-APP: the sign-on, the second factor, the group-to-role mapping and the first roles; this story consumes its session contract as an I dependency.
- The contract-end disablement and the recall of legacy AC2: the expiry of the partner user's binding against the firm's contract end and the recall of the open instructions, inside rwb-partner.
- The partner data room of S6, `GET /api/recovery/debtsale/v1/partner/data-room/{lotId}`, and every buyer-facing operation of the debt sale story.
- The fees and the scorecards of S9, the fee approval and the partner review of the same service.
- SCR-34 Partner list and PRT-01 Partner home, and every gateway-bff composite route behind a staff screen.
- The partner gateway build, its FAPI 2.0 profile and its second-factor configuration, which are the platform's and the portal's own product.
- The platform stories named in section 13, including RWB-PLT-N001-CON.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
