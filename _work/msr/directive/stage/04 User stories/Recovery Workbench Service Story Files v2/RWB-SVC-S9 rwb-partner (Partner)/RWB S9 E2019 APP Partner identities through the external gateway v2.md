# RWB-S9-E2019-APP Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for rwb-partner — the partner portal side of a partner identity: the `partner_user` binding of one firm and one partner role, the firm-state answer the external gateway carries as the claim to rwb-access, the `PLACED` scope applied by the owner's own repository on `GET /partner/instructions` and `GET /partners`, and the read refused when the firm or the binding is no longer live. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E2019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 23 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S9-E2019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S9-D |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E2019-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E2019-CON, RWB-S9-E2019-CON |
| Contract version | Not specified in the source documents (DOR-RWB-S9-E2019-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (FR-S9-038, FR-S9-039) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** and the **rwb-partner service**, I want **the partner portal side of a partner identity — the `partner_user` binding that maps an authenticated partner identity to exactly one firm and one partner role for a period, the firm-state answer the external gateway reads to carry the claim to rwb-access, and the `PLACED` scope applied by this service's own repository so that a partner reads only the instructions of its firm and of its role's instruction types — with the read refused the moment the firm or the binding is no longer live**, so that **a law firm, valuer or agency works on exactly the work placed with its own firm from Epic 5 without an SCB account, and a firm that leaves the panel loses the data the same day**.

This is the rwb-partner slice of legacy key RWB-E2-019 under epic RWB-SVC-S9.

- **This story, rwb-partner (S9), schema `rwb_partner`:** `partner`, `partner_user` and `partner_instruction`; the binding of one partner identity to one firm and one partner role for a period; the firm-state answer (panel status and contract end) that the partner gateway carries to rwb-access as a claim; the `PLACED` scope descriptor applied in this service's own query on `GET /partner/instructions`; the load of the binding with its validation; and the per-request re-check that ends a read when the firm or the binding is no longer live.
- **Not this story, rwb-access (P4):** the resolution of a partner identity to Recovery roles, the matrix and masking versions and the expiry — RWB-P4-E2019-APP and its baseline RWB-P4-E2019-CON — and the DMZ plumbing of the partner gateway, RWB-P4-E2019-INF and RWB-PLT-N007-INF. This story reads none of their tables and decides no session.
- **Not this story, rwb-decision (P7):** `decision_log_entry` and the central ledger read. The record of a resolution is RWB-P7-E2019-APP's; this story writes only the record of its own refusal through the DP-03 library.
- **Not this story, rwb-case (P3):** `recovery_case`, the parameter catalogue, the reference lists and the authorise answer — consumed through their contracts and never read as tables (DP-06, DP-07, DP-08).
- **Not this story, the instruction writes:** `POST /cases/{caseId}/instructions` (API-S9-002), `POST /partner/instructions/{instructionId}/accept` (API-S9-004), `/results` (API-S9-005) and `/invoices` (API-S9-006) are the placement and result stories' (RWB-S9-E6034-APP, RWB-S9-E6033-APP and the Epic 4 and Epic 6 stories); they reuse the scope guard of this story and are declared in no row of 12.1.
- **The legacy criteria:** `acs` is empty for this story. AC1, AC2, AC3, AC4, AC5, AC7 and AC8 are carried by **RWB-ITG-E2019-ITG**, AC6 and AC9 by **RWB-P4-E2019-APP**, and section 7 carries eight new criteria on the S9 operations only.
- **Service naming:** base `/api/recovery/partner/v1` (DP-13), schema `rwb_partner`, topic `rwb.partner.events.v1` with `.retry` and `.dlt` (DP-14), Temporal task queue `rwb-partner` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.partner`.
- **Events:** this story publishes no event and consumes none. EV-20 `InstructionIssued` and EV-21 `PartnerResultSubmitted` are the placement and result stories'; the resolution record leaves through the DP-03 library on `rwb.decision-record.v1`.
- **Database access:** through the per-service login of the service baseline (DP-02). No statement of this story names another service's table or an ACE view (DP-01, DP-05).

### 2. Business rationale

Partners today use separate channels (the LIT lawyer web, the OA portal, SVAF and SFTP), and the bank cannot show one record of what a firm could see. The legacy story answered with one partner identity per person, separate from bank identities, bound to one firm and one partner role, limited to the work placed with that firm and to the instruction types of the role, and refused when the firm is suspended, exits the panel or reaches its contract end. That answer stays. What changes is where each fact lives.

Architecture v5 keeps one entry per audience: staff screens go through gateway-bff, and partners come only through a partner gateway in the DMZ with the FAPI 2.0 profile (slides 20 and 35). The panel, the partner users and the instructions are module S9's (slides 17 and 41), and the Ownership Map gives `partner`, `partner_user` and `partner_instruction` to rwb-partner. So the resolution of an identity becomes rwb-access's question, and the data the identity may read stays here. The division of the key is fixed and is the same in every slice: **RWB-P4-E2019-APP**, **RWB-P4-E2019-CON** and **RWB-P4-E2019-INF** are the access and DMZ slice; **this story** owns the firm, the partner user, the binding and the instruction; **RWB-P7-E2019-APP** owns the central ledger entry; **RWB-ITG-E2019-ITG** proves the whole journey end to end.

The scope filter is the reason this story exists at all. The legacy `ScopeFilter` of the access module carried type `PLACED`, the partner id and the instruction types, and the same module applied it. Across a boundary the descriptor still names the filter, but the owner applies it: the `PLACED` descriptor arrives with the resolved session, and this service's repository adds `partner_id` and `instruction_type` to its own query. No service reads another's tables and no caller passes a partner id it may not see (DP-01, DP-11). The firm state takes the opposite direction for the same reason: this service answers panel status and contract end on `GET /partners`, the partner gateway carries that answer to rwb-access as a claim, and rwb-access resolves a session without a partner table and without a second hop from inside a step.

The negative side is fixed as tightly as the positive one. A partner holds exactly one partner role and never a bank role; a read that arrives without a `PLACED` descriptor, or with a bank role on it, is refused with MSG-P4-002 rather than widened; an instruction of another firm answers 404 with MSG-P4-003 and no field of it is echoed; a firm that turns `SUSPENDED` or `EXITED`, or a binding whose `valid_to` has passed, ends the read at the owner's next check with MSG-P4-008 or MSG-P4-001 and one `AC-DENY` record; and no personal value, token or session identifier is read, written, logged or tested.

It supports REQ-ACA-012 and NFR-050, and it stays behind the partner route that DL03 gates, so no partner reaches the Workbench in PROD until the architecture change for external access is approved. Four points have no source and are carried as placeholders, not invented: the story keeps the EP02 wave 2 while the service's Arch v5 wave is 4 (GAP-3147; ASM-5522), and the load path, the message per refusal condition and the `partner_user` catalogue are absent from the sources (GAP-3148; ASM-5523, ASM-5525, ASM-5526).

### 3. Preconditions

- RWB-P4-E2019-CON is published: the `PLACED` scope descriptor with the partner id and the instruction types, the refusal vocabulary with its statuses and message ids, and its fakes. This story consumes that descriptor and answers its own refusals in the same vocabulary.
- RWB-PLT-E1037-CON and RWB-P4-E1037-CON are published: the guard library and the authorise contract of rwb-access behind the Partner portal right of every read (DP-08).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published with RWB-P3-E1042-CON and RWB-P3-E1043-CON behind them: the parameters and reference-data clients (DP-06, DP-07).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence in `rwb_partner` (DP-15). `partner`, `partner_user` and `partner_instruction` arrive with the DB story of this service; this story adds no table and no column.
- `partner_user` carries DF-REF-212 to DF-REF-217 of the Logical Data Model: `id`, `identity_ref` varchar(64), `partner_id` uuid with a foreign key to `partner`, `role_code` varchar(20), `valid_from` date and `valid_to` date. TSD S9 T3.1 has no catalogue entry for the table, so the field list is taken from the Logical Data Model (GAP-3148; ASM-5526).
- The partner role rows `PT-AGENCY`, `PT-LAWFIRM`, `PT-VALUER`, `PT-AUCTION`, `PT-BUYER` and `PT-RAMC` are loaded in rwb-access with role class `PARTNER_USER` and their groups, for example `RWB-SIT-PT-LAWFIRM` (DL40); `PT-LED` has no login. This story reads the role code as it arrives and holds no role row.
- The parameters are loaded at their version: `rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE`, `rwb.access.partner.instruction-types.PT-VALUER=APPRAISE`, `rwb.access.partner.instruction-types.PT-AGENCY=COLLECT` (assumed in the legacy story, owner RW-AGENCYMG) and `rwb.refload.approver.partner_user=RW-SECADM`. The refresh interval `rwb.access.membership-refresh-minutes=5` is assumed with DL38 (GAP-3148; ASM-5527, ASM-5529).
- The partner gateway in the DMZ fronts the partner portal and forwards the resolved partner id, the partner role and the `PLACED` descriptor on each call; the gateway itself, its certificates and its profile are RWB-PLT-N007-INF's and RWB-P4-E2019-INF's and are named here, not depended on (GAP-3148; ASM-5524).
- The synthetic data of the legacy story exist: firms `LF-0012` and `LF-0019` as LAW_FIRM and `VL-0004` as VALUER, all panel status `ACTIVE`, `LF-0012` with contract end 30 June 2027; 5 open instructions placed with `LF-0012` and 3 with `LF-0019`; 2 `APPRAISE` and 1 `LIST` instruction with `VL-0004`; instruction `INS-2027-000431` placed with `LF-0019`.
- No build dependency: the story is ready on Day 1 against the RWB-P4-E2019-CON descriptor and the platform and P3 fakes. The wave is 2 by the W-MAP of the business epic while the service's Arch v5 wave is 4; the story keeps the earlier wave (GAP-3147; ASM-5522).

### 4. Flow

1. A partner user opens the partner portal through the partner gateway in the DMZ and signs in with a second factor (RWB-PLT-N007-INF); the gateway resolves the identity with rwb-access and holds the answer.
2. On each portal call the gateway forwards the resolved partner id, the partner role and the `PLACED` scope descriptor with its instruction types.
3. `PartnerScopeGuard` reads the forwarded session and refuses before any data read when the descriptor is absent, when the role is not a partner role, or when the partner id is missing (X1, X2).
4. `PartnerBindingRepository` reads the caller's `partner_user` row by `identity_ref` for the business date and checks that it is live, that its `partner_id` is the partner id of the session and that its `role_code` is the role of the session (BR1, BR2). This story holds the `partner_user` binding that scopes a partner user to one firm and one partner role; P4 keeps the internal role model only, and the gateway enforces the external identity.
5. A row that is absent, ended or bound to another firm refuses the call with 401 and MSG-P4-001 or MSG-P4-008 and writes one `AC-DENY` record through the DP-03 library (X3, X4).
6. `AuthoriseClient` asks rwb-access for the Partner portal right of the call — R on the list and on the firm read — with the descriptor's scope, one hop and a 2 s timeout (DP-08, DP-11); a refusal answers 403 with MSG-P4-002 and no data.
7. On `GET /api/recovery/partner/v1/partner/instructions` (API-S9-003), `InstructionQueryRepository` applies the descriptor in its own query: `partner_id = <session partner id>`, `instruction_type IN <the role's instruction types>`, and the status filter the caller passes; it returns the `InstructionPage` of `PartnerInstruction` in due-date order (BR3, BR4).
8. On `GET /api/recovery/partner/v1/partners` (API-S9-001), `FirmStateQueryService` returns the caller's firm with its panel status, partner type and contract end, and no other firm; this is the answer the gateway carries to rwb-access as the firm claim (BR8).
9. A single instruction that is not of the caller's firm is answered 404 with MSG-P4-003 and no instruction data, whether it is asked for on the list, on the acceptance, on the results or on the invoice operation of another story (BR3, X5).
10. `PartnerFirmStateRevalidation` re-checks the firm's panel status and the binding's `valid_to` when the cached answer is older than the refresh interval; a firm that is `SUSPENDED`, `EXITED` or past its contract end, or a binding that has ended, refuses the call with 401 and MSG-P4-008 or MSG-P4-001 at the first request after the interval (BR4, X3).
11. The reason of each refusal at the owner is written through `PartnerRefusalRecorder` into the local decision record and published on `rwb.decision-record.v1` by the library, keyed by the request so a repeated call writes no second entry (BR10, DP-03). Dual path: rwb-access calls the record path within the resolution, and a record that cannot be appended refuses the access answer with MSG-P7-003 and no session. The same record is published on `rwb.decision-record.v1` for durability and replay, deduplicated by the idempotency key, and collected centrally within five minutes (Architecture v5 Text Extract v1 slides 14, 28 and 42).
12. Nothing in this story resolves an identity, mints or holds a token, opens a session, applies masking, changes a case, issues an instruction or ends a partner account: it answers the two portal reads, loads the binding and refuses what it may not serve.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The call carries no `PLACED` descriptor, or no partner id | Refused before any read; no instruction is returned and nothing is widened from a request parameter | MSG-P4-002 | AC4 |
| X2 | The forwarded session names a bank role, or a role outside the partner roles | Refused at the guard with 403; no partner data is read | MSG-P4-002 | AC4 |
| X3 | The caller's `partner_user` row is absent, or its `valid_to` has passed | Refused with 401; one `AC-DENY` record carries reason `NO_PARTNER_BINDING`; no data | MSG-P4-001 | AC7 |
| X4 | The binding names another firm than the session, or another partner role | Refused with 401; the mismatch is recorded; no data | MSG-P4-001 | AC1 |
| X5 | The requested instruction is placed with another firm | Answered 404 with no instruction data and no echoed field | MSG-P4-003 | AC6 |
| X6 | The firm's panel status is `SUSPENDED` or `EXITED`, or its contract end has passed | The read is refused at the next check after the refresh interval; one `AC-DENY` record carries reason `PARTNER_NOT_ACTIVE` | MSG-P4-008 | AC7 |
| X7 | A binding is loaded with a role outside the partner role list, with an unknown partner id, or in a period that overlaps a live one | The load is refused; no row is written and the live row is unchanged | None, or MSG-GEN-004 on the overlap | AC2 |
| X8 | The authorise answer refuses the right, or is unavailable | Refused with 403; where the answer is unavailable the call fails with 503 and no data is served | MSG-P4-002, MSG-GEN-006 | AC4 |
| X9 | The local record or the outbox row cannot be written | The read is refused with 503 and no data; nothing is served on an unrecorded refusal; an incident is raised | MSG-P7-003 | AC7 |
| X10 | A payload, a test file or a log line carries a personal value, a token or a session identifier | The field is rejected before the write and the log names the field only | None | AC8 |

None of these paths changes a case, an instruction status or a partner account: a case status is P3's, an instruction status is the placement story's, and the ending of an account's validity at the contract end is RWB-S9-AD022-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E2019-CON and its descriptor, the authorise contract, the parameters and reference-data fakes and the decision-record library; the resolution, the token and the session belong to rwb-access and the gateway, and are faked |
| Negotiable | The role roster, the instruction types, the refresh interval and the approver are rows and parameters; the load path and the message per condition are open until the review and are stated as defaults |
| Valuable | One controlled way for a partner identity to read its own firm's work, with the firm and the binding checked on every call and the data lost the day the firm leaves |
| Estimable | One guard, one binding repository, one binding loader, one firm-state query, one instruction query, one re-check and one refusal recorder |
| Small | Fits one sprint with its tests, as the portal slice of a key that four stories share |
| Testable | Each of the eight criteria is one component test against the fakes plus two contract tests on the descriptor and the refusal vocabulary |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E2-019, and every legacy criterion signs an identity in, refuses a session, returns or withholds an instruction, or refuses a bank screen across services. The ten criteria below are new for the rwb-partner slice and test only the S9 operations; each keeps the legacy values and adds no business value.

```gherkin
Feature: The partner portal side of a partner identity in rwb-partner

  Background:
    Given the rwb-partner base path is /api/recovery/partner/v1 for staff paths and /partner/v1/* for portal paths, and the schema is rwb_partner
    Given the rwb-access contract mock returns partner identity "P-5101" resolved to partner "LF-0012", partner role "PT-LAWFIRM", scope "PLACED" and instruction types "FILE_SUIT,ENFORCE"
    Given the rwb-access contract mock returns partner identity "P-5102" resolved to partner "VL-0004", partner role "PT-VALUER", scope "PLACED" and instruction type "APPRAISE"
    Given the rwb-case parameters mock returns "rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE" and "rwb.access.partner.instruction-types.PT-VALUER=APPRAISE"
    Given partner "LF-0012" is a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027, partner "LF-0019" is a LAW_FIRM with panel status "ACTIVE" and partner "VL-0004" is a VALUER with panel status "ACTIVE"
    Given 5 open instructions are placed with "LF-0012" and 3 with "LF-0019"

  Scenario: AC1 One live binding maps the identity to one firm and one role (new, D-RCV-60)
    Given partner identity "P-5101" has one live partner_user row bound to "LF-0012" with role "PT-LAWFIRM" from 1 April 2026 to 30 June 2027
    When "P-5101" calls GET /partner/instructions with status "SENT"
    Then this service reads that one row and answers the instructions of "LF-0012"
    Then the answer carries no instruction of another firm and no second partner role
    Then the query derives the partner id from the session and never from a request parameter
    When the row names "LF-0019" while the session names "LF-0012"
    Then the call is refused with status 401 and message MSG-P4-001 and no instruction data is returned

  Scenario: AC2 The binding load refuses a bad role, an unknown firm and an overlapping period (new, D-RCV-60)
    Given the partner roles are "PT-AGENCY", "PT-LAWFIRM", "PT-VALUER", "PT-AUCTION", "PT-BUYER" and "PT-RAMC", and "PT-LED" has no login
    When a binding for "P-5101" with role "PT-LED" is loaded
    Then the load is refused with status 422, the field "role_code" is named and no row is written
    When a binding for "P-5101" with an unknown partner id is loaded
    Then the load is refused with status 422, the field "partner_id" is named and no row is written
    When a second binding for "P-5101" overlapping 1 April 2026 to 30 June 2027 is loaded
    Then the load is refused with status 409 and message MSG-GEN-004 and the live row is unchanged
    When an approved binding with role "PT-AGENCY" for "LF-0019" is loaded
    Then the load needs the approval role from "rwb.refload.approver.partner_user", writes one row and returns it with the period

  Scenario: AC3 The firm-state answer carries the panel status and the contract end (new, D-RCV-60)
    Given "P-5101" is bound to "LF-0012"
    When the partner gateway reads GET /partners for the firm of the session
    Then the answer carries partner "LF-0012", its partner type, panel status "ACTIVE" and contract end 30 June 2027
    Then the answer carries no other firm, no instruction, no personal name, no contact value and no token
    When the same read names a partner id that "partner" does not hold
    Then the answer is 404 with MSG-P4-003 and no firm data

  Scenario: AC4 The owner applies the PLACED scope and the Partner portal right (new, D-RCV-60)
    Given "P-5101" is signed in with scope "PLACED" and the Partner portal right R
    When "P-5101" calls GET /partner/instructions at 09:20 with status "SENT"
    Then the 5 instructions of "LF-0012" are returned and none of the 3 of "LF-0019"
    Then each row carries its instruction id, type, status, instructed date and due date
    Given a call whose forwarded session lacks the "PLACED" descriptor, or names a bank role
    When that call reaches GET /partner/instructions
    Then it is refused with status 403 and message MSG-P4-002 and no instruction is returned
    Given the authorise answer refuses right R
    When "P-5101" calls GET /partner/instructions
    Then it is refused with status 403 and message MSG-P4-002 and no instruction is returned

  Scenario: AC5 The role's instruction types limit the answer inside the firm (new, D-RCV-60)
    Given "P-5102" is bound to "VL-0004" with role "PT-VALUER"
    Given "VL-0004" holds 2 instructions of type "APPRAISE" and 1 of type "LIST"
    When "P-5102" calls GET /partner/instructions
    Then the answer holds the 2 "APPRAISE" instructions and no "LIST" instruction
    Then the instruction types come from the parameter at its version and are no constant in code
    When the parameter cannot be read at its version
    Then the call fails with 503 and message MSG-GEN-006 and no instruction is returned

  Scenario: AC6 An instruction of another firm is not returned by its identifier (new, D-RCV-60)
    Given "P-5101" is signed in for "LF-0012"
    When "P-5101" requests instruction "INS-2027-000431" placed with "LF-0019"
    Then the call answers status 404 with message MSG-P4-003 and no instruction data
    Then no field of the instruction, its case or its partner is echoed in the problem detail
    Then the same check holds for the accept, results and invoice operations of the instruction, which other stories own

  Scenario: AC7 A firm that is not active, or an ended binding, refuses the read at the owner (new, D-RCV-60)
    Given "LF-0012" moves to panel status "EXITED" at 11:00 on 4 January 2027
    Given "P-5101" read the list at 10:00
    When "P-5101" calls GET /partner/instructions at 11:06
    Then the call is refused with status 401 and message MSG-P4-008 and no instruction of "LF-0012" is returned
    Then one entry with decision code "AC-DENY" and reason "PARTNER_NOT_ACTIVE" is written through the DP-03 library
    Given a binding whose "valid_to" was 31 December 2026
    When its identity reads the list on 4 January 2027
    Then the call is refused with status 401 and message MSG-P4-001 and one entry carries reason "NO_PARTNER_BINDING"
    When the local record cannot be written
    Then the read is refused with status 503 and message MSG-P7-003, no instruction is returned and an incident is raised

  Scenario: AC8 The answers carry references and codes and no personal value (new, D-RCV-60)
    Given "P-5101" is bound to "LF-0012" with role "PT-LAWFIRM"
    When the binding, the firm-state answer, the instruction page and the refusal entry are produced
    Then they carry identity_ref "P-5101", partner id "LF-0012", role "PT-LAWFIRM", scope "PLACED", instruction ids, types, statuses and dates, and nothing else of the person
    Then a repository row, an answer, an event, a log line and a test file hold no personal name, national id number, e-mail address, phone number, token, session identifier or Entra group name such as "RWB-UAT-PT-LAWFIRM"

  Scenario: AC9 The approvals, the partner route switch and the call rules hold in this service (new, D-RCV-60)
    Given a partner_user load carries the role owner approval but not the security administrator approval
    When the load is submitted
    Then the load is refused and no partner_user row is written
    Given the parameter "rwb.access.partner-signin" is off in PROD
    When a partner call reaches this service in PROD
    Then the call is not served and no partner route is open in PROD
    When the authorise call is made inside a request
    Then it is one hop with a 2 s timeout and a breaker, and no other service's table is read or second hop made
    Then the staff paths use "/api/recovery/partner/v1", the portal paths use "/partner/v1/*" and events use "rwb.partner.events.v1" only

  Scenario: AC10 A replayed write with the same idempotency key is not written twice (new, D-RCV-60)
    Given a partner_user load is written with an idempotency key
    When the same load is sent again with the same idempotency key
    Then the second call writes no second partner_user row and returns the answer of the first call
```

The ten criteria are new and test the S9 operations only. AC1, AC2, AC3, AC4, AC5, AC7 and AC8 of RWB-E2-019 stay with **RWB-ITG-E2019-ITG**, and AC6 and AC9 with **RWB-P4-E2019-APP**; the values they use are reused here unchanged — `LF-0012`, `LF-0019`, `VL-0004`, `P-5101`, `P-5102`, `INS-2027-000431`, `PLACED`, `PM-2026.11`, `MASK-SIT-01`, 30 June 2027, the panel statuses `ACTIVE` and `EXITED`, the reasons `PARTNER_NOT_ACTIVE` and `NO_PARTNER_BINDING`, the group `RWB-UAT-PT-LAWFIRM` and MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-008, MSG-P7-003 and MSG-GEN-004 — and no new business value is introduced.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner user holds a partner identity separate from bank identities, signs in only through the external gateway with multi-factor authentication, and holds exactly one partner role bound to exactly one firm | legacy RWB-E2-019 BR1, BR2; NFR-050; INT-24; REQ-ACA-012 |
| BR2 | The binding is this service's: one `partner_user` row per identity per live period, with a foreign key to `partner` and no row of another firm's schema | legacy RWB-E2-019 BR2 and section 13; DF-REF-212 to DF-REF-217; DP-01 |
| BR3 | A partner reads only the work placed with its firm: the owner applies `PLACED` with the partner id of the session and the instruction types of the role in its own query, and a request parameter never widens it | legacy RWB-E2-019 BR3, BR4; scope "Placed cases"; DP-01, DP-11 |
| BR4 | A partner role sees only the instruction types named for it, read from the parameter at its version and never from code | legacy RWB-E2-019 BR4; parameters `rwb.access.partner.instruction-types.*`; LOV-INSTRUCTION |
| BR5 | Access ends when the firm's panel status is `SUSPENDED` or `EXITED`, when its contract end has passed, or when the binding's `valid_to` has passed; the owner refuses the read at its next check | legacy RWB-E2-019 BR5 and flow step 9; DF-PRT-005, DF-PRT-006, DF-REF-217; LOV-PANEL |
| BR6 | The permission matrix, the masking and the access log apply to a partner as to a bank user, and every read declares the Partner portal right it needs | legacy RWB-E2-019 BR6; TSD S9 T6.1, T6.2 |
| BR7 | The binding is requested by the partner and agency manager, approved by the role owner in the bank IAM, created by the access administrator and loaded by the reference data administrator with the approval of the security administrator | legacy RWB-E2-019 BR8 and precondition 3; `rwb.refload.approver.partner_user` |
| BR8 | The firm-state answer is the only partner fact this service gives the gateway: panel status, partner type and contract end of the caller's firm, and no session decision | legacy RWB-E2-019 flow step 6 and section 12; RWB-P4-E2019-CON; Arch v5 slides 20 and 35 |
| BR9 | No partner reaches the Workbench in PROD until the architecture change for external access is approved; the partner route stays behind the parameter `rwb.access.partner-signin`, off in PROD | legacy RWB-E2-019 BR7; DL03; RWB-P4-E2019-APP |
| BR10 | A refusal at the owner is recorded once through the DP-03 library with its reason, and a refusal whose record cannot be written is not served | legacy RWB-E2-019 AC3, AC4 and section 17; principle 5; DP-03 |
| BR11 | One topic, one schema and one login per service, with two bases: `/api/recovery/partner/v1` for the staff paths behind gateway-bff and `/partner/v1/*` for the portal paths behind the partner gateway; `rwb.partner.events.v1`, `rwb_partner`, the per-service login | DP-02, DP-13, DP-14; Arch v5 slides 17 and 41; GAP-1849 |
| BR12 | Every consumed call is one hop with a 2 s timeout and a breaker; no other service's table is read and no second hop is made from inside a request | DP-11; Arch v5 slide 12 |
| BR13 | The answers carry references and codes only: no personal name, contact value, identity number, token or session identifier | legacy RWB-E2-019 section 17; NFR-039, NFR-040; ADR-010 |

### 9. State transitions

None for a case, a task or a case status: this story changes no case. The states below are the states of a binding period and of a portal read; the instruction lifecycle `SENT` to `RECALLED` is the placement story's (LOV-INSTR-STATUS).

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Binding period | (none) | An approved load within no live period for the identity | Live | One `partner_user` row; the identity's reads are scoped to its firm and its role, and the other read refuses an overlap |
| Binding period | Live | `valid_to` passes | Ended | The owner refuses the read with 401 and MSG-P4-001, and one `AC-DENY` entry carries reason `NO_PARTNER_BINDING` |
| Binding period | Live | The firm turns `SUSPENDED` or `EXITED`, or its contract end passes | Live until the owner's next check | The read is refused with 401 and MSG-P4-008 from the first request after the refresh interval; the ending of the row itself is RWB-S9-AD022-APP's |
| Portal read | Scoped | The scope, the binding, the right or the firm state fails a check | Refused | The stated status and message, one `AC-DENY` entry where the reason applies, and no data |
| Portal read | Scoped | The checks pass | Answered | The page or the firm answer of the scope, with references and codes only |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-partner service identity (the per-service login, DP-02) | Reads its own three tables, applies the scope, answers the two reads, loads the binding with its approval and writes the local record |
| RW-AGENCYMG Partner and agency manager | Requests the partner user and sets the firm's panel status and contract end; the firm itself is RWB-S9-E6029-APP's |
| Role owner (bank IAM, level 2) | Approves each partner user request |
| Access administrator (bank IAM, level 3) | Creates the partner identity and adds it to the partner role group |
| RW-REFADM Reference data administrator | Loads the partner user binding; loads no partner row of its own |
| RW-SECADM Security administrator | Approves the binding version, maintains the partner role groups and receives the mismatch incidents |
| PT-LAWFIRM, PT-VALUER, PT-AGENCY | Read their own firm's instructions with the letters of their role (Partner portal R, `PLACED`) |
| rwb-access (P4) | Owns the identity resolution, the role rows, the matrix and masking versions and the scope descriptor; this story decides no session |
| The architecture team | Approves external access before PROD (DL03); the partner route stays off until then |
| No delegation of authority level applies | A binding, a scope and a firm state are not a credit decision |

### 11. Data

| BR Field ID | Table in `rwb_partner` | Field | Read or write |
|---|---|---|---|
| DF-REF-212 | `partner_user` | id | Write on load |
| DF-REF-213 | `partner_user` | identity_ref | Write on load, read on each call; a directory reference and no name |
| DF-REF-214 | `partner_user` | partner_id | Write on load, read on each call; the firm of the binding |
| DF-REF-215 | `partner_user` | role_code | Write on load, read on each call; the one partner role |
| DF-REF-216 | `partner_user` | valid_from | Write on load, read on each call |
| DF-REF-217 | `partner_user` | valid_to | Write on load, read on each call; no later than the firm's contract end |
| DF-PRT-001, DF-PRT-004, DF-PRT-005, DF-PRT-006 | `partner` | id, partner_type, panel_status, contract_end | Read for the firm-state answer |
| DF-PRT-007 | `partner` | score | Not read here: the scorecard is RWB-S9-E7011-APP's |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | id, case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount | Read under the scope of AC4 and AC5 |
| DF-DEC-001 to DF-DEC-018 | local decision record of the DP-03 library | the `AC-DENY` fact of a refusal at the owner | Written by the library; this story writes no `decision_log_entry` |
| DF-REF-035, DF-REF-037 | `role` of rwb-access | role_code, role_class | Named only, never read: the role code arrives in the session and its class is rwb-access's |
| DF-REF-027 to DF-REF-033 | `lov_value` of rwb-case | lov_code, value_code, label_en | Read through the reference-data contract (DP-07) |
| DF-ACE-301 | `v_ace_iam_group` | entra_group | Not read: the group is in the token and in the bank IAM, and no ACE view is read here (DP-05) |

The `partner_user` field list is taken from the Logical Data Model because TSD S9 T3.1 has no catalogue entry for the table, and the table arrives with the DB story of this service; the shape is Not specified in the source documents (GAP-3148; ASM-5526). `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `lov_value` and `parameter_value` (P3), every `v_ace_*` view (P1), `document` (P5) and `payment` (P8) are other owners' and are named only; no foreign key leaves `rwb_partner` except the one inside it from `partner_user` and `partner_instruction` to `partner` (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/partner/v1/partner/instructions` | API-S9-003: the `InstructionPage` of `PartnerInstruction` for the caller's firm, filtered by the `PLACED` descriptor, the role's instruction types and the status the caller passes | Partner portal, right R, `PLACED` scope applied in this service's query | Not applicable, read only |
| GET | `/api/recovery/partner/v1/partners` | API-S9-001: the caller's firm with partner type, panel status and contract end — the claim the partner gateway carries to rwb-access | Partner portal, right R, the session's firm only | Not applicable, read only |
| POST | `/api/recovery/partner/v1/admin/reference-loads` (stated default) | The load of a `partner_user` binding for a table code `partner_user`, with the approval role from `rwb.refload.approver.partner_user` | Reference data administrator load, security administrator approval, no partner portal right | `Idempotency-Key` required; a replay answers the first row and writes no second |

Errors: 401 no session, no live binding or a firm that is not active (MSG-P4-001, MSG-P4-008); 403 the `PLACED` descriptor or the Partner portal right is absent (MSG-P4-002); 404 the firm is absent or the instruction is of another firm (MSG-P4-003); 409 an overlapping live period (MSG-GEN-004); 422 a load field that fails its rule, with the field named and messageId Not specified in the source documents (DOR-RWB-S9-E2019-APP-8); 503 a reference read, the authorise answer or the record is unavailable (MSG-GEN-006, MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set where a message applies.

The load path is Not specified in the source documents (GAP-3148; ASM-5523): TSD S9 T-A.1 lists exactly API-S9-001 to API-S9-006 and none of them is a reference load, and the legacy `POST monolith-base/admin/reference-loads` is rwb-access's API-P4-005, which cannot write `rwb_partner` (DP-01). The default above sits on the S9 base, carries no partner portal right, and is confirmed by the reference-data owner before it is frozen. The `partner_user` DDL (migration V_E2_019__partner_user.sql) and the reference load handler sit in this S9 story set; rwb-access keeps the session, role and scope checks.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| POST `/api/recovery/access/v1/authorise` | P4 rwb-access | The Partner portal right R and the scope of the caller behind the two reads; consumed, faked, one hop with a 2 s timeout and a breaker (DP-08, DP-11) |
| GET `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | `rwb.access.partner.instruction-types.*`, `rwb.refload.approver.partner_user` and the refresh interval, at the version in force (DP-06) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | `LOV-INSTRUCTION`, `LOV-INSTR-STATUS`, `LOV-PANEL` and `LOV-PARTNER-TYPE` at the version in force (DP-07) |

The resolution `POST /api/recovery/access/v1/partner-identities/resolve` is **not** called by this service: the partner gateway holds it and forwards the `PLACED` descriptor, and the descriptor's fields and its refusal vocabulary are the contract of RWB-P4-E2019-CON that this story consumes — the C dependency of the metadata. Neither operation of 12.1 is declared as consumed, and no operation of rwb-partner is declared as another service's.

#### 12.3 Events published

None. This story produces nothing on `rwb.partner.events.v1`: EV-20 `InstructionIssued` is the placement story's (RWB-S9-E6034-APP) and EV-21 `PartnerResultSubmitted` the result story's (RWB-S9-E6033-APP), both as `rwb.partner.InstructionIssued.v1` and `rwb.partner.PartnerResultSubmitted.v1`. The record of a refusal at the owner leaves through the DP-03 library as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, which is the platform library's event and is named here only to say where the record goes.

#### 12.4 Events consumed

None. This story subscribes to no topic, holds no consumer group and has no inbox handler: the firm state, the binding and the instruction are this service's own rows, and the versions in force are read at call time through the P3 contracts. The instruction writes of other stories publish no event that this story needs to keep the portal read correct.

#### 12.5 Workflows and activities

None. The two reads are synchronous on the caller's thread and start no workflow, activity, signal or query. `InstructionWorkflow` is the service's and belongs to the placement and result stories; the `rwb-partner` queue carries no workflow of this story.

#### 12.6 Schedules

None. The refresh of the firm state and the binding is a per-call check bounded by the parameter `rwb.access.membership-refresh-minutes`, not a Temporal Schedule, and the dated pass that ends an account's validity at the contract end is RWB-S9-AD022-APP's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `partner` | S9 (`rwb_partner`) | The firm of the session: partner type, panel status, contract end |
| `partner_user` | S9 (`rwb_partner`) | The binding of one identity to one firm and one partner role for a period |
| `partner_instruction` | S9 (`rwb_partner`) | The instructions read under the scope of the session |
| local decision record, `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in `rwb_partner` by the library and the service's own DB story | The `AC-DENY` fact of a refusal and the replay guard of the load |

`recovery_case` and the parameter and reference rows (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5) and `payment` (P8) are other owners' and are never read or written here (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access contract fake (RWB-P4-E2019-CON) | The forwarded resolution descriptor and the authorise answer | `P-5101` for `LF-0012` with `PT-LAWFIRM`, `PLACED` and `FILE_SUIT,ENFORCE`; `P-5102` for `VL-0004` with `PT-VALUER`; a descriptor without `PLACED`; a bank role on the descriptor; right R refused; authorise unavailable (AC1, AC4) |
| rwb-partner contract fake (RWB-S9-E2019-CON) | The rwb-partner operations of 12.1 | Not specified in the source documents (DOR-RWB-S9-E2019-APP-22) |
| Partner gateway session fake | The forwarded session of a portal call | The partner id, the role and the descriptor of AC1 and AC5, and the 11:06 call of AC7 |
| Parameters fake (P3) | `GET /admin/parameters` | The three instruction-type rows at version PAR-2026.11, the approver `RW-SECADM` and the refresh interval; a version that cannot be read (AC5, AC7) |
| Reference-data fake (P3) | `GET /admin/lists/{listCode}` | `LOV-INSTRUCTION` with `COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST, SELL`; `LOV-INSTR-STATUS`; `LOV-PANEL`; `LOV-PARTNER-TYPE` |
| Decision-record fake (DP-03) | The local library and `rwb.decision-record.v1` | A recorder that captures the decision code, the actor, the partner, the role, the scope and the reason, and a switch that fails the write (AC7) |
| Partner fixture | The `rwb_partner` rows of the run | `LF-0012` with contract end 30 June 2027 and 5 instructions, `LF-0019` with 3 and `VL-0004` with 2 `APPRAISE` and 1 `LIST`; the bindings of AC1, AC2 and AC5; instruction `INS-2027-000431` of `LF-0019` |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The two portal reads and the binding load provided on the S9 base; the authorise, parameters and reference-data reads consumed, one hop with a 2 s timeout and a breaker |
| Kafka | 0 published, 0 consumed | No topic produced or consumed by this story; the record leaves through the DP-03 library on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | None in this story |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.partner.portal` in the rwb-partner service, over the repository and entity layer of `th.co.scb.ace.workbench.recovery.partner.partner`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The firm, the binding and the instruction stay in `rwb_partner`; the role, the case and the ledger are named and never read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the `AC-DENY` fact of a refusal at the owner | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. No ACE view is read here: the group arrives in the token | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, for the role's instruction types, the approver and the refresh interval | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, for the four lists of TSD S9 T3.2 | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; every read declares its Partner portal right | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The descriptor is the legacy scope filter's successor and the owner applies it | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the two reads sit on the S9 base and the legacy partner paths move under it | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_partner`; the binding rows are dated data, and this story adds no table and no column | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the staff view of the same partner records (SCR-34); a partner never uses it | H RWB-PLT-N001-CON |

The platform H dependencies of the table and the C of RWB-P3-E1042-CON and RWB-P3-E1043-CON are delivered by waves 0 and 1 and are built against their fakes; they are the dependencies the pattern table adds and are not repeated in the metadata rows, which name None and RWB-P4-E2019-CON.

**What changes from the monolith.** The legacy `PartnerAccessService`, `PartnerSessionRevalidation` and `PartnerUserRepository` of `recovery.access.partner` are replaced by three pieces in three services: the resolution, the role rows and the versions move to rwb-access (RWB-P4-E2019-APP); the binding, the firm and the instruction stay here and are read by this story; and the refusal record moves to the DP-03 library and the central ledger (RWB-P7-E2019-APP). The legacy `ScopeFilter scopeFor(SessionContext)` becomes the `PLACED` descriptor of RWB-P4-E2019-CON applied by this service's own query, and the legacy `PartnerStatus partnerStatus(UUID)` published interface becomes `GET /partners` on the service base. `PartnerUserLoader` stays here and becomes the reference-load handler with the approval that the legacy story gave RW-SECADM.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerPortalController` | Controller | The two reads of 12.1: validation, the declared right, the problem responses and the session extraction (BR6) |
| `PartnerScopeGuard` | Component | Reads the forwarded `PLACED` descriptor, refuses an absent descriptor, a bank role, a partner role outside the list and a partner id mismatch before any read (BR1, BR3) |
| `PartnerBindingRepository` | Repository | Reads the caller's `partner_user` row and writes it on load, in `rwb_partner` only (BR2) |
| `PartnerBindingLoader` | Service | Validates a binding: a known partner id, a partner role code only, no identity bound twice in one period, the approval role from the parameter, and one row per load (AC2) |
| `PartnerFirmStateRevalidation` | Service | Re-checks the firm's panel status and the binding's `valid_to` after the refresh interval and refuses the read (BR5) |
| `FirmStateQueryService` | Service | The firm-state answer of API-S9-001 with partner type, panel status and contract end (BR8) |
| `InstructionQueryRepository` | Repository | The page of `partner_instruction` under the scope, the role's types and the status filter, and the single-instruction check that answers 404 (BR3, BR4) |
| `PartnerRefusalRecorder` | Client | Writes the `AC-DENY` fact of a refusal through the DP-03 library and fails the read when it cannot (BR10) |
| `AuthoriseClient`, `ParameterClient`, `ReferenceListClient` | Client | The right and scope, the parameters and the four lists, one hop with a 2 s timeout and a breaker (DP-06, DP-07, DP-08, DP-11) |

**Configuration and reference data.** The three instruction-type parameters, `rwb.refload.approver.partner_user`, the refresh interval `rwb.access.membership-refresh-minutes=5` (assumed, DL38) and the partner role roster are rows and parameters; none is a constant. The partner route is switched by `rwb.access.partner-signin`, read as a parameter: off, the two reads answer 404 and no partner data leaves the service. No default is written in code.

**Build steps**

1. `PartnerBindingRepository` and `PartnerBindingLoader` with the four load rules and the approval role; tests for AC2 and AC8.
2. `PartnerScopeGuard` over the descriptor: absent descriptor, bank role, unknown role, partner id mismatch, right refused (AC1, AC4, X1, X2).
3. `InstructionQueryRepository` with the scope, the role's types and the single-instruction 404; tests for AC4, AC5 and AC6.
4. `FirmStateQueryService` and `GET /partners`, with the absent-firm 404 and the no-other-firm rule (AC3).
5. `PartnerFirmStateRevalidation` with the refresh interval and the two ends — the firm's status and the binding's `valid_to` (AC7).
6. `PartnerRefusalRecorder` and the fail-closed read when the record cannot be written (AC7, X9).
7. The `AuthoriseClient`, `ParameterClient` and `ReferenceListClient` calls with their 2 s budget and breaker, and the 503 of an unreadable reference (AC5, X8).
8. The personal-value and personal-field scan of the rows, the answers, the events, the logs and the tests; then the flag off in PROD and the whole-slice run against the fakes (AC8, BR9).

**Done when.** The tests of section 16 pass against the fakes, the two reads answer only the work of the caller's firm and role, an instruction of another firm answers 404 with MSG-P4-003 and no data, a firm that is not active or an ended binding refuses the read at the owner with MSG-P4-008 or MSG-P4-001 and one `AC-DENY` entry, no statement names another service's table or an ACE view, and the partner route is off in PROD.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-008 | The firm is suspended, exited or past its contract end | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. | This story, on the re-check of the firm state (AC7) |
| MSG-P4-001 | No live binding, a binding of another firm, or an ended period | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on the binding check (AC1, AC7) |
| MSG-P4-002 | No `PLACED` descriptor, a bank role, or a caller without the Partner portal right | You cannot {action} here. Your role does not include it. | This story, at the guard and through the authorise answer (AC4) |
| MSG-P4-003 | An instruction of another firm, or a firm that is absent | This case is not in your scope. | This story, on the single-instruction check and the firm read (AC3, AC6) |
| MSG-P7-003 | The refusal cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The DP-03 library, whose status this story hands back (AC7) |
| MSG-GEN-004 | A load overlaps a live period for the same identity | Someone else changed this record. Reload it to see their change. | This story, on the load (AC2) |
| MSG-GEN-006 | The parameters, the lists or the authorise answer cannot be read | The service is temporarily unavailable. Try again in a few minutes. | This story, on an unreadable reference (AC5, X8) |

MSG-P4-001, MSG-P4-002, MSG-P4-003 and MSG-P4-008 are the legacy texts unchanged and their Thai text follows DL10; MSG-P7-003, MSG-GEN-004 and MSG-GEN-006 are the platform texts. The message per refusal condition is Not specified in the source documents (GAP-3148; ASM-5525): TSD S9 T-A.2 gives the status codes only, and the mapping above is the reading applied.

Open decisions that apply to this story are DL03, DL10, DL38 and DL40. Each is still open, and each assumption below holds until its decision closes: DL03 with ASM-0189, ASM-0193, ASM-0578 and ASM-2567; DL10 with ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL38 with ASM-0245, ASM-1413, ASM-1424 and ASM-1508; DL40 with ASM-0422 and ASM-2705.

### 15. Screens and states

| Screen | State | What the person does |
|---|---|---|
| PRT-01 Partner home | Loading | Waits while the firm's open instructions load through `GET /partner/instructions` |
| PRT-01 Partner home | List | Sees only the firm's instructions of the role's types, with due dates |
| PRT-01 Partner home | Empty by scope | Sees no instruction although the firm has work of another instruction type; nothing of another firm is shown |
| PRT-01 Partner home | Refused | Sees MSG-P4-008, MSG-P4-001 or MSG-P4-002 and no data |
| Partner sign-in page | Refused | Is sent back to the gateway's page with MSG-P4-008 or MSG-P4-001 and no data |
| SCR-34 | Loading | Not specified in the source documents (CG-ALL-11761) |
| SCR-34 | Empty | Not specified in the source documents (CG-ALL-11761) |
| SCR-34 | Error | Not specified in the source documents (CG-ALL-11761) |
| SCR-34 | No access | Not specified in the source documents (CG-ALL-11761) |

The partner sign-in page, its MFA steps and the token are the partner gateway's (RWB-PLT-N007-INF, RWB-P4-E2019-INF) and rwb-access's; this story serves the data of PRT-01 only, and the staff view of the same partner records is SCR-34's through the gateway-bff route of RWB-PLT-N001-CON. PRT-02 to PRT-06 are Epics 4 to 6 and are out of scope. Screen owners: PRT-01 is served by rwb-partner through the partner gateway on `/partner/v1/*`; SCR-34 is served through the gateway-bff composite route of RWB-PLT-N001-CON. Route owner: Not specified in the source documents (GAP-1848).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-01 | AC1, AC4; legacy Covers "AC1, BR1, BR3" | Component | Firms LF-0012 with 5 instructions and LF-0019 with 3; the binding of P-5101; the page of LF-0012 only |
| TC-E2-019-02 | AC5; legacy Covers "AC2, BR4" | Component | Valuer VL-0004 with 2 APPRAISE and 1 LIST instructions; P-5102 bound to PT-VALUER |
| TC-E2-019-03 | AC7; legacy Covers "AC3, BR5" | Component | LF-0012 moved to EXITED at 11:00 on 4 January 2027; the read at 11:06; MSG-P4-008 and reason PARTNER_NOT_ACTIVE |
| TC-E2-019-04 | AC1, AC7; legacy Covers "AC4, BR2" | Component | Partner identity P-5103 with no live binding; 401 with MSG-P4-001 and reason NO_PARTNER_BINDING |
| TC-E2-019-05 | AC4; legacy Covers "AC5, BR1" | Contract | A forwarded session without the PLACED descriptor, and one naming a bank role; 403 with MSG-P4-002 and no data |
| TC-E2-019-06 | AC6; legacy Covers "AC6, BR3" | Component | Instruction INS-2027-000431 of LF-0019 read by P-5101 for LF-0012; 404 with MSG-P4-003 and no echoed field |
| TC-E2-019-07 | AC2; legacy Covers "AC7, BR2" | Component | A load with role PT-LED, with an unknown partner id, and an overlapping period for P-5101; 422 and 409 with MSG-GEN-004 |
| TC-E2-019-08 | AC4; legacy Covers "AC8, BR6" | Component | A caller without the Partner portal right R on GET /partner/instructions; 403 with MSG-P4-002 and no data |
| TC-E2-019-09 | AC1, AC8; legacy Covers "AC9, BR1" | Contract | A forwarded session with a bank role and a partner id mismatch; 401 or 403, no data, and no bank role in any answer or entry |
| TC-E2-019-10 | AC4; legacy Covers "Access" | Component | The authorise answer refusing right R, and the descriptor missing on a second call; MSG-P4-002 both times |
| TC-E2-019-11 | AC7; legacy Covers "Principle 5" | NFR | The local record forced to fail during a refusal at the owner; 503 with MSG-P7-003, no data, an incident raised, and the retried read leaves one entry |
| TC-E2-019-12 | BR2, BR5; section 12.7 tables | Component | A binding with `valid_to` on the business date, read on that date and on the next day; the read on the next day refused with MSG-P4-001 and no data |
| TC-E2-019-13 | BR7 | Component | A `partner_user` load missing the role owner approval or the security administrator approval is refused; a load with both approvals is written |
| TC-E2-019-14 | BR8 | Contract | GET /partners read by a caller of firm LF-0012 and by a session naming LF-0019; the answer carries panel status, partner type and contract end of the caller's firm only, and no session decision |
| TC-E2-019-15 | BR9 | Component | Parameter `rwb.access.partner-signin` off in PROD; a partner call is not served and no partner route is open in PROD |
| TC-E2-019-16 | BR10 | Component | A refusal at the owner is recorded once with its reason; a repeated call writes no second entry |
| TC-E2-019-17 | BR11 | Contract | Calls only on `/api/recovery/partner/v1` and `/partner/v1/*`; events only on `rwb.partner.events.v1`; the table in `rwb_partner` and the per-service login are the only ones used |
| TC-E2-019-18 | BR12 | NFR | The authorise call is made as one hop with a 2 s timeout and a breaker; no other service's table is read and no second hop is made from inside a request |
| TC-E2-019-19 | BR13 | Contract | A served answer and a refusal carry references and codes only: no personal name, contact value, identity number, token or session identifier |
| TC-E2-019-20 | AC9; BR7 to BR13 | Component | A partner_user load without the security administrator approval is refused; with the parameter off in PROD the partner call is not served and no partner route is open |
| TC-E2-019-21 | AC10 | Component | A partner_user load replayed with the same idempotency key writes no second row |

The eleven legacy test-case ids of RWB-E2-019 are kept in the order of the work package and each is answered here on the portal side: the binding, the firm state, the scoped page, the single-instruction refusal and the read that ends. The resolution, the second factor, the role count and the bank route are the fakes' and their own services'. The legacy level System maps to Component, Contract or NFR as the row shows, and Access to Component. The `-ITG` copies of these cases belong to RWB-ITG-E2019-ITG, which runs the same values across the gateway, rwb-access and rwb-partner. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the partner roles, the instruction types, the refresh interval, the approver, the panel values and the instruction statuses are rows, parameters or reference values read through their contracts.
- No personal data anywhere: the partner identity is a directory reference, the firm is an id and an instruction is an id and a type; a payload, a log line or a test file that carries a name, a contact value or an identity number is rejected.
- No token, session identifier, password, secret or private key is read, held, cached or logged; the session is the gateway's and this story reads a descriptor (ADR-010).
- No read of another service's tables and no ACE view: `recovery_case` (P3), `decision_log_entry` (P7), `role` (P4), `lov_value` (P3) and every `v_ace_*` view (P1) are named only; the group arrives in the token (DP-01, DP-05).
- The owner authorises the object: the partner id comes from the session, never from a request parameter, and the scope is applied inside this service's query (BR3).
- A refusal at the owner is recorded with its reason; an unrecorded refusal is a defect and is not served (BR10).
- One base, one topic, one queue and one login: `/api/recovery/partner/v1`, `rwb.partner.events.v1`, `rwb-partner`, the per-service login; no monolith path or `recovery.*` base is declared here (DP-13, DP-14).
- Every consumed call is one hop with a 2 s timeout and a breaker; an unreadable parameter or list refuses the read rather than widening it (DP-11).
- The partner route stays behind `rwb.access.partner-signin` and off in PROD until DL03 closes.
- Every example, seed and test value is synthetic; no production payload is copied into a row, a fake or an evidence file.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4; Program 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR13 | TC-E2-019-01 to TC-E2-019-21 |

| Legacy reference | Where it is kept |
|---|---|
| The partner identity, the firm and the role of a session | Sections 1, 4, 8, 11, 12.1 — as the binding and the session descriptor |
| The `PLACED` scope and the instruction types of the role | Sections 4, 8, 12.1, 16 — as this service's own query |
| The firm's panel status and contract end | Sections 4, 8, 11, 12.1 — as the firm-state answer the gateway carries |
| The binding and its load, the approver and the period | Sections 3, 4, 8, 11, 12.1 — as `partner_user` and its load |
| AC1, AC2, AC3, AC4, AC5, AC7 and AC8 of RWB-E2-019 | Carried by RWB-ITG-E2019-ITG; this story states the portal behaviour behind them and restates none of them |
| AC6 and AC9 of RWB-E2-019 | Carried by RWB-P4-E2019-APP; this story answers the 404 of AC6 on its own operation |
| The resolution, the roles, the matrix and masking versions | RWB-P4-E2019-APP and RWB-P4-E2019-CON |
| The central ledger entry of a sign-in and a refusal | RWB-P7-E2019-APP; this story writes only its own refusal through DP-03 |
| The partner gateway, its profile and the DMZ | RWB-PLT-N007-INF and RWB-P4-E2019-INF |
| The placement and result writes of the instruction | RWB-S9-E6034-APP, RWB-S9-E6033-APP and the Epic 4 and Epic 6 stories |

### 19. Out of scope

- The resolution of a partner identity, the role rows, the matrix and masking versions and the expiry (RWB-P4-E2019-APP), and the contract document of the resolution (RWB-P4-E2019-CON).
- The partner gateway in the DMZ, its certificates, its mTLS hop, its network policy and its rate limit (RWB-P4-E2019-INF, RWB-PLT-N007-INF).
- The central decision ledger and its read, and the access-entry writer itself (RWB-P7-E2019-APP, RWB-P4-E1039-APP).
- The end-to-end journey of the key and its evidence, and the seven legacy criteria it owns (RWB-ITG-E2019-ITG).
- The instruction writes: issue, accept or decline, results and invoices (RWB-S9-E6034-APP, RWB-S9-E6033-APP and the Epic 4 and Epic 6 stories), and the instruction lifecycle states.
- The ending of an account's validity at the contract end and the dated pass that does it (RWB-S9-AD022-APP), and partner panel management, contracts and scorecards (Epic 6 and Epic 7, S9).
- The parameter catalogue and the reference lists (rwb-case, P3), consumed and faked, never defined here.
- The customers, guarantors, heirs and bidders, who do not sign in to the Workbench.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
