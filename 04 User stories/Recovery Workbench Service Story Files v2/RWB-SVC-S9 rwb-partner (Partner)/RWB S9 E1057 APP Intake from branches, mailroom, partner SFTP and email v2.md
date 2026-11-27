# RWB-S9-E1057-APP Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E1057-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S9-C |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E1057-APP-16); the squad sizes it at refinement; INVEST Small: fits within two weeks (DOR-RWB-S9-E1057-APP-15) |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1057-CON; GET /partners with the code filter (API-S9-001), not yet published in rwb-partner.yaml (CG-ALL-11749); built against API Specification v5, base /api/recovery/partner/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to REQ-DCM-009, REQ-DCM-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the partner-panel slice of RWB-E1-057 in `rwb-partner`. The legacy in-process `PartnerDirectory.findByCode` of section 12 becomes the published partner read of this service — the `code` filter branch of `GET /partners` (API-S9-001) under base `/api/recovery/partner/v1` (DP-13), one hop with a 2 s timeout and a fake (DP-11) — answered from `partner` in schema `rwb_partner` (DP-01) with the panel status and partner type taken from the reference lists of `rwb-case` (DP-07); the read writes nothing, publishes and consumes no event (DP-09) and declares no Schedule (DP-10), because the fifteen-minute intake and its five `INTAKE_*` parameters stay with RWB-P5-E1057-APP (the parameters contract of DP-06). The service owns the topic `rwb.partner.events.v1` and the queue `rwb-partner`. The split plan gives this secondary slice no legacy criterion and no build row, while the P5 slice of the same key states that the partner criteria are proved here; the partner read has no published operation of its own, the two refusal reasons are the caller's, no panel transition table and no cache rule is published, and EP01 wave 1 is earlier than the service wave 4 (GAP-3146; ASM-5513 to ASM-5521). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**.

This story owns no channel reader and writes no intake row: it is the partner half of that intake, the slice that legacy RWB-E1-057 declares as the published interface `PartnerDirectory.findByCode(partnerCode)` in its section 12. It builds:

- the partner-by-code read of `rwb-partner` on `GET /partners` (API-S9-001) with the additive optional `code` filter, partner-portal right R and the scope applied, one hop and a 2 s budget (DP-11, DP-13);
- the answer: the partner id, code, registered name, type, panel status and score of the row in `partner` of schema `rwb_partner`, and no other property (DP-01);
- the panel status that BR4 of the legacy story reads, so that a partner subfolder of an unknown code and a partner whose panel status is not ACTIVE are two distinct refusals in the caller, with the legacy reasons `PARTNER_UNKNOWN` and `PARTNER_NOT_ACTIVE` (AC2, AC3);
- the reference reads behind the panel status and the partner type: LOV-PANEL and LOV-PARTNER-TYPE as list rows, through the reference-data contract of `rwb-case` (DP-07);
- the answer shape that RWB-P5-E1057-CON, the contract baseline of the document intake, declares for the partner reference of an intake item (the C row of this story).

It does not own: the branch scanner, mailroom, SFTP and mailbox readers, the file hash, the duplicate window, the type and size checks, the copy to the hold container, the `document_intake` rows, the moves to the processed, rejected and archive folders and the intake run record, which are RWB-P5-E1057-APP; the malware scan and OCR (RWB-P5-E1041-APP, RWB-P5-E1049-APP); the partner panel, its states and its fee schedule as maintained data (RWB-S9-E6029-APP, RWB-S9-E6030-APP); the instructions placed with a partner (RWB-S9-E6031-APP and the fee stories of the module); the public shapes of the partner operation, which RWB-S9-E1057-APP reads from the contract baseline of P5 and from the published API specification.

The split plan assigns this secondary slice no legacy criterion of its own, so section 7 carries ten criteria tagged "(new, D-RCV-60)" that test only the partner read. The eleven criteria the plan gives RWB-P5-E1057-APP stay there, and the two that turn on this read — AC2 Partner SFTP and AC7 An unknown or suspended partner is refused — are answered here at component level and proved end to end by RWB-P5-E1057-APP and RWB-ITG-E1057-ITG, as the P5 slice states (GAP-3146; ASM-5513).

### 2. Business rationale

Documents reach recovery today by courier, shared folders and personal email, and an original that goes to the wrong desk is rebuilt for each audit. The intake of RWB-E1-057 reads the four inbound paths every 15 minutes, records where each file came from, refuses a file that is not allowed or comes from an unknown partner, and leaves every accepted file for the malware scan and the OCR steps, so a document received in the morning is on the case the same day. It meets REQ-DCM-009 and puts every inbound file through the virus scan of REQ-DCM-010, and it removes email hand-offs of customer documents (CTL-11).

The partner half of that promise is one question asked once per partner file: which firm is this, and may it send us work today. The legacy story asks it of an interface inside the monolith; D-RCV-60 changes the mechanics and nothing of the rule:

1. **The panel row is this service's.** `partner` with its code, name, type, panel status, contract end and score is S9's own table (context pack ownership rows; TSD S9 T3.1, DF-PRT-001 to DF-PRT-007), and its panel status is what BR4 of the intake reads. No caller reads that table (DP-01): the intake asks this service.
2. **The legacy in-process call becomes a published read.** `PartnerDirectory.findByCode` was a Java interface other modules called in process (legacy section 12). It is now one REST read of this service, one hop, 2 s budget and a breaker, faked in the build, so the intake can be built and tested before this service is up (DP-11, ADR-020).
3. **One operation, one filter, no new shape.** The service publishes six operations and `GET /partners` (API-S9-001) already lists partners with panel status and score; the code the intake holds is the same key, so the read is that operation with one additive optional `code` filter and the published `Partner` element as its answer. No second path and no new element is declared (GAP-3146; ASM-5514).
4. **The states and types are data.** LOV-PANEL publishes ACTIVE, ON_NOTICE, SUSPENDED and EXITED and LOV-PARTNER-TYPE the eight partner types (TSD S9 T3.2); both are list rows read through the reference-data contract of `rwb-case` (DP-07) and no value is a constant or a branch of the code (FSD S9 BR-S9-002).
5. **The refusal stays with the caller.** The legacy reasons `PARTNER_UNKNOWN` and `PARTNER_NOT_ACTIVE` are the reasons of the intake run record (legacy AC7), and the caller renders them in its own message. This service answers the row or an empty list and decides nothing, so the panel rule is executed in one place and the partner data has one owner (BR4; ASM-5514).
6. **A read writes nothing.** No partner row, no decision record, no outbox row and no idempotency row is written, no event is published and none is consumed, and the service owns no job and no Schedule (context pack: Jobs 0). The events EV-20 and EV-21 of this service belong to the instruction steps and not to a read (ASM-5517).
7. **The build row the plan leaves empty.** The `code` filter is a read over an existing table in this service's own schema and the two list reads come from a client library; the plan gives this secondary slice no H row, so the DP-07 rows it would add are tracked instead (ASM-5516).

No business value moves: the partner types, the panel states, the two reasons, the right and the intake parameters stay reference data, parameters and legacy values, read with their version and never written in code.

### 3. Preconditions

- RWB-P5-E1057-CON is published and faked: it declares the partner reference of an intake item, the shape this story answers, and the consumer contract test of section 16 runs against it from Day 1 (C row).
- `partner` exists in schema `rwb_partner` from the per-service Flyway baseline of this service, with the columns and the lists of TSD S9 T3.0, T3.1 and T3.2; this story adds no table, no column and no migration (DP-15).
- Panel rows exist: `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end` and `score` are maintained by the partner and agency manager through RWB-S9-E6029-APP and RWB-S9-E6030-APP (FEAT-PRM-01, FEAT-PRM-02). The legacy fixture of the intake story is partner "LF-007", a law firm with panel_status "ACTIVE".
- LOV-PANEL and LOV-PARTNER-TYPE are readable as reference data through the client library of `rwb-case` (`RWB-PLT-E1043-CON`, DP-07); a failed list read stops the answer and is not served from code.
- The service runs as its own login on schema `rwb_partner` (DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `rwb_document` or on an ACE view is refused by the database and fails the boundary test.
- The document intake of `rwb-document` calls this read with the partner code of the SFTP subfolder or of the mailbox sender's firm, one hop with a 2 s timeout and a breaker (DP-11). No screen calls this read directly for the intake; the partner portal reaches `GET /partners` through the gateway-bff composite route (DP-19).
- The five intake parameters `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, `INTAKE_DUPLICATE_WINDOW_DAYS`, `INTAKE_MIN_IMAGE_KB` and `INTAKE_ALERT_AFTER_FAILURES` are P5's rows and P5's reads; this story reads none of them and duplicates no limit (DP-06, section 12.2).
- Wave 1 is the plan's and is kept because EP01 is wave 1 while the service's Arch v5 wave is 4 (R5.6); release 30 November 2026 is copied unchanged and marked tentative (ASM-5520).
- No approval of the realigned story is recorded, so the status is Draft (realignment v1) and the build starts on the Draft contract with its fake (ASM-5521).

### 4. Flow

1. The document intake of `rwb-document` lists the partner SFTP inbound folders and the recovery mailboxes and holds one partner_code per SFTP subfolder and per sender firm (RWB-P5-E1057-APP, steps 2 and 5 of the legacy flow).
2. It asks this service for that code: `GET /api/recovery/partner/v1/partners?code=<partner_code>`, one hop, partner-portal right R with the scope applied, 2 s budget and a breaker (DP-11, DP-13).
3. `PartnerDirectoryController` validates the query, resolves the right and the scope, and calls `PartnerDirectoryService` (section 13).
4. `PartnerDirectoryService` resolves the code against `partner` in `rwb_partner` by one indexed lookup, and reads the panel status and the partner type against the list rows of LOV-PANEL and LOV-PARTNER-TYPE obtained through the reference-data client of `rwb-case` (DP-07).
5. `PartnerAnswerMapper` builds the answer: for a resolving code, one `Partner` element with id, partner_code, partner_name, partner_type, panel_status and score, and nothing else; a code that resolves to no row answers an empty list with 200, never a not-found error, because that operation publishes 401, 403 and 503 only (GAP-3146; ASM-5514).
6. The caller reads the answer: a row with `panel_status` ACTIVE takes the file in, a row with any other status refuses it with the legacy reason `PARTNER_NOT_ACTIVE`, and an empty list refuses it with `PARTNER_UNKNOWN`, both recorded on the intake run record (legacy AC2, legacy AC7, legacy X3).
7. No row, no decision record, no outbox row and no idempotency row is written, and no event leaves the service (section 9, section 12.3).
8. A repeat of the same read answers the row as it stands at that moment: the panel status is never copied into this service and no stale answer is served (AC9).
9. The partner and agency manager sees and keeps the same rows on SCR-34 Partner list through the gateway-bff composite route (DP-19); that screen and its maintenance actions belong to RWB-S9-E6029-APP and RWB-S9-E6030-APP.
10. The intake run book and the run record are P5's; this story contributes no count and no rerun, and its failures surface to the caller as 503 with MSG-GEN-006 naming this service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No partner holds the requested code | 200 with an empty list; the caller refuses the file with the reason "PARTNER_UNKNOWN" and writes no intake row | MSG-P5-007 (rendered by the caller) | AC2 |
| X2 | The partner exists and its panel status is not ACTIVE | 200 with the row and its stored panel status; the caller refuses the file with the reason "PARTNER_NOT_ACTIVE" | MSG-P5-007 (rendered by the caller) | AC3 |
| X3 | The caller's role does not hold partner-portal right R | 403 before any read; no row is returned and the scope is never widened | MSG-P4-002 | AC4 |
| X4 | The query carries a value outside its list, or the code is empty or over its published length | 422 with the platform envelope and nothing read | MSG-GEN-001 | AC5 |
| X5 | The database of `rwb_partner` does not answer, or the reference-data read of `rwb-case` fails | 503 with the system that failed; the caller leaves the file at its channel and retries on its next run | MSG-GEN-006 | AC7 |
| X6 | A statement, a component or a test names another `rwb_*` schema, `document_intake` or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6 |
| X7 | The panel status changes between two reads | The next read answers the row as it stands; no cached copy and no second copy of the partner row exists in this service | None | AC9 |
| X8 | The answer, a log line or an interface payload carries a personal field | The contract test fails the build; the partner row holds a firm name and a firm code only | None (pipeline log) | AC10 |

X1 and X2 are the partner paths of legacy exception X3 (Partner subfolder code unknown or partner not ACTIVE); the legacy X9 (an email with no usable attachment) is P5's and is no path of this read. X3 and X4 are the access and validation paths of the published operation; X5 to X8 are the paths the target call types and the schema boundary add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 on its own schema against the reference-data fake and the P5 contract fake, and needs no live P3, P5 or P9 |
| Negotiable | The mapper, the no-cache rule and the component names are this story's choice; the operation, the filter, the element, the right, the lists and the reasons are fixed |
| Valuable | The intake asks one owner for the panel row instead of holding a copy of the partner table, so an instruction and a refusal read the same fact |
| Estimable | One operation branch, one repository read, one reference reader, one mapper and eight test cases |
| Small | Finished inside one week with its tests on the fakes |
| Testable | Each criterion runs on a synthetic panel fixture through the fakes, plus the access, list, boundary and purity cases |

### 7. Acceptance criteria

```gherkin
Feature: The partner panel read behind the document intake

  Background:
    Given partner "LF-007" is a law firm with panel_status "ACTIVE" in schema rwb_partner
    Given the rwb-case contract mock returns the lists LOV-PANEL "ACTIVE, ON_NOTICE, SUSPENDED, EXITED" and LOV-PARTNER-TYPE "AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC"
    Given the rwb-document contract mock returns the partner reference of one intake item by partner code
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The partner by code answers the panel row (new, D-RCV-60)
    Given partner "LF-007" holds partner_type "LAW_FIRM" and panel_status "ACTIVE"
    When the document intake of rwb-document asks for partner code "LF-007"
    Then the answer carries the partner id, partner_code "LF-007", partner_type "LAW_FIRM", panel_status "ACTIVE" and the score of the row
    Then the answer is one hop within the 2 s budget and carries no other property

  Scenario: AC2 A code that resolves to no partner (new, D-RCV-60)
    Given no partner holds the code "LF-099"
    When the intake asks for partner code "LF-099"
    Then the answer is 200 with an empty list
    Then the intake refuses the file with the reason "PARTNER_UNKNOWN" and writes no intake row
    Then this service writes no row and publishes no event

  Scenario: AC3 A partner whose panel status is not ACTIVE (new, D-RCV-60)
    Given partner "LF-008" holds panel_status "SUSPENDED"
    When the intake asks for partner code "LF-008"
    Then the answer carries partner_code "LF-008" and panel_status "SUSPENDED"
    Then the intake refuses the file with the reason "PARTNER_NOT_ACTIVE"
    Then the file is taken in only when the panel status of its subfolder's partner is "ACTIVE"

  Scenario: AC4 The role without the partner-portal right R (new, D-RCV-60)
    Given a caller whose role does not hold partner-portal right R
    When the caller asks for partner code "LF-007"
    Then the answer is 403 with MSG-P4-002
    Then no partner row is returned and the scope is not widened

  Scenario: AC5 The panel states and the partner types are list rows (new, D-RCV-60)
    Given the reference-data mock returns LOV-PANEL and LOV-PARTNER-TYPE with their values
    When the panel status and the partner type of "LF-007" are checked
    Then "ACTIVE" and "LAW_FIRM" are matched as list rows and never as literals or branches of the code
    Then a query value outside its list is refused with 422 and MSG-GEN-001
    Then a failed list read answers 503 with MSG-GEN-006 and no row is served from code

  Scenario: AC6 The read touches rwb_partner.partner only (new, D-RCV-60)
    Given the service login of rwb_partner and its grants
    When the statements and the tests of the build are inspected
    Then no statement names recovery_case, document_intake, another rwb_* schema or a v_ace_* view
    Then the database refuses a statement on rwb_document and the boundary test fails the build

  Scenario: AC7 The read writes nothing (new, D-RCV-60)
    Given the read of partner "LF-007" answers
    When the answer is returned
    Then no partner row, no decision record, no outbox row and no idempotency row is written
    Then the same read repeated answers the same row

  Scenario: AC8 The answer is the shape RWB-P5-E1057-CON declares (new, D-RCV-60)
    Given the rwb-document contract baseline declares the partner reference of an intake item
    When the answer is validated against that baseline
    Then the answer carries exactly the declared properties and no other
    Then an answer with a missing declared property fails the consumer contract test

  Scenario: AC9 A panel change is visible on the next read (new, D-RCV-60)
    Given partner "LF-007" was read with panel_status "ACTIVE"
    When the partner and agency manager sets panel_status "SUSPENDED" on "LF-007"
    Then the next read answers "SUSPENDED"
    Then no copy of the panel row is kept in this service and no old answer is served

  Scenario: AC10 No personal data in the answer, the log or the payload (new, D-RCV-60)
    Given the read of partner "LF-007" answers
    When the answer, the log line and the caller's payload are inspected
    Then they carry the partner id, code, registered name, type, panel status and score only
    Then no sender address, no file name and no contact detail appears in any of them

  Scenario: AC11 Every rule of section 8 is traced to a criterion or a test (new, D-RCV-60)
    Given the rules BR1 to BR9 of section 8 and the test cases of section 16
    When the rule table is checked against sections 7 and 16 and against RWB-P5-E1057-APP
    Then each of BR1 to BR9 names a criterion or a test of this story or of RWB-P5-E1057-APP
    Then a rule with no criterion and no test fails the review; the guardrail or boundary test for an architecture rule is Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC17)

  Scenario: AC12 A call without credentials is answered 401 and a path naming no provided operation is answered 404 (new, D-RCV-60)
    Given a call to the partner read without credentials
    When the call is sent
    Then the answer is 401 and no partner row is returned
    Then a call to a path naming no provided operation is answered 404

  Scenario: AC13 A read over its 2 s budget is ended and its retries and timeouts follow the stated values (new, D-RCV-60)
    Given the partner read takes longer than its 2 s timeout
    When the read is ended
    Then the read is ended at 2 s and the answer is Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC19)
    Then the number of retries and the activity timeout are Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC19)
```

Every line above is target wording tagged "(new, D-RCV-60)"; no legacy criterion is copied, because the split plan gives this secondary slice no legacy criterion and the eleven criteria it gives RWB-P5-E1057-APP stay there (GAP-3146; ASM-5513). The values are the legacy ones of RWB-E1-057 and of the module: partner "LF-007" a law firm with panel_status "ACTIVE", the codes "LF-099" and "LF-008" of legacy AC7, the reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE", the two lists and their values of TSD S9 T3.2, and the messages MSG-P4-002, MSG-GEN-001, MSG-GEN-006 and the caller's MSG-P5-007. AC2 and AC3 are the partner half of legacy AC2 and legacy AC7 and are proved end to end by RWB-P5-E1057-APP and RWB-ITG-E1057-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Scanner and mailroom files have source SCAN; partner SFTP files PARTNER; mailbox attachments EMAIL | LOV-DOC-SOURCE; DF-DOC-005 | TC-E1-057-01, TC-E1-057-03, TC-E1-057-04 (RWB-P5-E1057-APP) |
| BR2 | Only the allowed types up to the size limit are taken in; the type is checked by content and extension | INTAKE_ALLOWED_TYPES, INTAKE_MAX_FILE_MB (25 MB assumed); VR-P5-001-1 | TC-E1-057-05, TC-E1-057-06 (RWB-P5-E1057-APP) |
| BR3 | Every file taken in is scanned for malware by scanStep before ocrStep reads it | REQ-DCM-010; FEAT-DCM-18; RWB-E1-041 | TC-E1-057-16 (RWB-P5-E1057-APP) |
| BR4 | A partner file is taken in only from the subfolder of a partner whose panel_status is ACTIVE | DF-PRT-002, DF-PRT-005; Partner panel reference table | TC-E1-057-02, TC-E1-057-07, TC-S9-E1057-02, TC-S9-E1057-03 (AC3) |
| BR5 | A file with the same hash from the same channel inside the window is a duplicate | INTAKE_DUPLICATE_WINDOW_DAYS (30 assumed); R-UNI-40 | TC-E1-057-08 (RWB-P5-E1057-APP) |
| BR6 | A source file is moved or an email archived only after the document_intake commit | Events rule "Transactions" | TC-E1-057-14 (RWB-P5-E1057-APP) |
| BR7 | JOB-12 runs every 15 minutes in business hours, once across instances; two failed runs in a row on a channel raise an alert | JOB-12; RWB-TE-007 | TC-E1-057-11, TC-E1-057-12, TC-E1-057-15 (RWB-P5-E1057-APP) |
| BR8 | Folders and mailboxes are properties; types, sizes and windows are parameters; none is code | Principle 1 | Section 12.2 and TC-S9-E1057-10 |
| BR9 | The sender address is personal data: masked by role and never logged | CTL-11; DL26 | AC10 and TC-S9-E1057-08 |

The nine legacy rules are kept by ID and wording because they are the rules of the same legacy key. This story executes BR4's data half and BR8 and BR9's data half, and none of the rest:

- BR4 is answered, not decided, here: the panel status is returned exactly as `partner` holds it (DF-PRT-005), so the caller can refuse any status other than ACTIVE. The rule is executed once, in the caller, and this service holds the only copy of the panel row (AC3).
- BR8 is why this story writes no folder name, no mailbox address, no type list, no size and no window in code: those are the property set of RWB-P5-E1057-INF and the five parameter rows of DP-06, read by P5 and by nothing in this story (section 12.2).
- BR9 is why no personal field is added to the answer: the partner row carries a firm name, a firm code, a type, a status, a contract end and a score, and the sender address, the file name and the mailbox code of the legacy story stay in `rwb_document` (AC10).
- BR1, BR2, BR3, BR5, BR6 and BR7 are P5's: the source values, the type and size gates, the scan order, the duplicate window, the commit-then-move order and the fifteen-minute schedule run in `rwb-document` and are proved by RWB-P5-E1057-APP.
- The lists are data: no panel status, partner type or reason is a literal, and every one of them is a row of LOV-PANEL, LOV-PARTNER-TYPE or of the caller's reason set, read through DP-07 (FSD S9 BR-S9-002).
- JOB-12 runs and reruns are read through the P1 admin job contract, and the four channels are proved through the P5 intake contract, not here (GAP-0367).

### 9. State transitions

None. This story changes no case status and writes no row. It reads `partner.panel_status`, whose values are the four of LOV-PANEL, and it moves nothing: the panel status is set by RWB-S9-E6029-APP and RWB-S9-E6030-APP and by the notice and exit stories of EP07, and the case stays with `rwb-case`.

| Read | Condition | What this service answers | What the caller does |
|---|---|---|---|
| `partner` by code | A row exists with `panel_status` ACTIVE | The row with status ACTIVE | Takes the file in (legacy AC2) |
| `partner` by code | A row exists with `panel_status` ON_NOTICE, SUSPENDED or EXITED | The row with its stored status | Refuses the file with the reason "PARTNER_NOT_ACTIVE" (legacy AC7) |
| `partner` by code | No row holds the code | 200 with an empty list | Refuses the file with the reason "PARTNER_UNKNOWN" (legacy AC7) |

No source publishes the transition table of LOV-PANEL, so only the reading above is stated and the moves themselves carry the placeholder (GAP-3146; ASM-5519). The three states that admit and refuse a file are the legacy rule's, not this story's invention: BR4 admits ACTIVE and refuses every other value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: keeps the partner codes, types and panel status this read answers, through the panel stories and not here |
| RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R as T6.1 gives it: the read, in scope, and nothing else |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal RU as T6.1 gives it: the read of its own firm's row, in scope |
| the `rwb-document` service identity | Reads the partner row of an SFTP subfolder or of a mailbox sender's firm on the intake path; a machine identity with right R, scoped, and no other right |

The right of the operation is partner-portal R, as TSD S9 T-A.1 declares for API-S9-001, and a role without it is refused with MSG-P4-002 (AC4). The authorisation decision is taken by `rwb-access` and held here as the cached permission decision of the operation; DP-08 is not in this story's pattern set and no guard is built. The rwb-access authorise check is Not specified in the source documents (DOR-RWB-S9-E1057-APP-6). The callers' identities are service identities under NFR-051 and are subject to the same role check as people. No person's name appears in the partner row, the answer or a log: the row is a firm.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id | Read, the partner reference the answer returns |
| DF-PRT-002 | partner (S9) | partner_code | Read, the key the read resolves; the code filter of the operation |
| DF-PRT-003 | partner (S9) | partner_name | Read, the registered name of the firm |
| DF-PRT-004 | partner (S9) | partner_type | Read, over LOV-PARTNER-TYPE |
| DF-PRT-005 | partner (S9) | panel_status | Read, the value BR4 of the intake turns on, over LOV-PANEL |
| DF-PRT-006, DF-PRT-007 | partner (S9) | contract_end, score | Read, returned as they stand; the contract end is not compared with the business date here |
| DF-DOC-046 to DF-DOC-057 | document_intake (P5) | source, source_ref, file_sha256, channel_code, file_name, file_size, captured_at, sender_address, partner_id and the rest | Not read and not written: the intake row is `rwb_document`'s and the partner id it stores is the identifier this answer returns (DP-01) |
| the list rows of LOV-PANEL and LOV-PARTNER-TYPE | reference data (P3) | value, label, version | Read through the reference-data contract of DP-07, never joined and never copied |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9) | instruction_type, instructed_at, due_at, status and the rest | Not read and not written: the instruction steps are RWB-S9-E6031-APP and the stories of the module |

The field-level types, lengths and lists are those of TSD S9 T3.0, T3.1 and T3.2; this story adds no table, no column and no migration, writes no row and returns six fields. The name and the definition of the constraint or index that makes the lookup on `partner_code` one row are Not specified in the source documents (GAP-3146; ASM-5518). `partner_user` is this service's and belongs to the portal identity story, not here. The answer never carries a sender address, a file name, a mailbox code or a contact detail, and no personal field is added to `partner` for the intake (BR9, AC10).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partners` (API-S9-001) with the additive optional `code` filter | `Partner[]` out with id, partnerCode, partnerName, partnerType, panelStatus and score; the branches without `code`, which list by `type` and by `status`, are the same operation | Partner portal, right R, scope applied | Not applicable (a read) |

The operation and its purpose are published — "List partners with panel status and score", query `type` and `status`, answer `Partner[]`, errors 401, 403 and 503, right R with the scope applied (TSD S9 T-A.1, T-A.2). The `code` filter is the one addition this story needs and its name and behaviour are Not specified in the source documents (GAP-3146; ASM-5514). An unknown code answers an empty list with 200, because that operation publishes no not-found error; a value outside its list answers 422 with MSG-GEN-001 through the platform envelope; a failed read answers 503 with MSG-GEN-006. The other five operations of the base — the instruction read, the issue, the acceptance, the result and the invoice — belong to other stories of the module and none of them is built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| the reference-data read of DP-07 | the reference-data contract of `rwb-case`, `/api/recovery/case/v1` | P3 rwb-case | LOV-PANEL and LOV-PARTNER-TYPE, cached for 5 minutes, one hop with a 2 s budget and a breaker |

That row is the only consumed call of the story, it is a class C dependency (`RWB-P3-E1043-CON`) behind the client library `RWB-PLT-E1043-CON`, and it is faked in the build. No parameter is consumed: the five `INTAKE_*` rows of the legacy story are the document intake's and are read by RWB-P5-E1057-APP through DP-06, so DP-06 adds no row here. No partner, case, document or ledger call is made: the panel row is this service's own data (DP-01).

#### 12.3 Events published

None. The service owns the topic `rwb.partner.events.v1` with its retry and `.dlt` topics and the event names `rwb.partner.<Event>.v1` (DP-09, DP-14), and its ownership rows give it two events, which TSD S9 T5.3 names `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21). Both belong to the instruction steps — the issue of an instruction and a result from the portal — and a read that changes nothing announces nothing: no outbox row, no producer group and no event name is declared by this story (ASM-5517). A build that publishes an event here fails the absence test.

#### 12.4 Events consumed

None. The read is started by the caller's request and by no event; the FSD declares no background event for the partner panel feature (FSD S9 A2.1.4.4, A2.2.4.4), and the intake's trigger is P5's Schedule and not an event of this service. This story holds no consumer group, no subscription and no inbox row.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| None in this story | — | — | The read is one synchronous REST answer and starts no workflow. `InstructionWorkflow` on queue `rwb-partner` in namespace `rwb-recovery` is this service's workflow and belongs to the instruction stories; the caller's intake workflow, `DocumentIntakeWorkflow` on queue `rwb-document`, is P5's and only calls this read (DP-11) |

No activity is registered by this story and no parent-child edge is declared: a read inside another service's activity is a REST call, one hop, and never a Temporal command (Arch v5 slide 12).

#### 12.6 Schedules

None. This service owns no job (context pack ownership rows, Jobs 0), and the fifteen-minute intake of the legacy story is a Temporal Schedule of `rwb-document` registered by RWB-P5-E1057-OPS (DP-10). This story declares no Schedule, no Quartz row and no shared job table, and the business-hours window and the holiday skip are P5's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| partner | S9 (`rwb_partner`) | The outside firm: read by code for the panel row; never written here |
| partner_user | S9 (`rwb_partner`) | Not read and not written: the portal identities of a firm are the identity story's |
| partner_instruction | S9 (`rwb_partner`) | Not read and not written: the instructions placed with a partner are the instruction and fee stories' |

No library table is used by a read: no outbox row, no inbox row, no idempotency row and no decision record is written (AC7). Not owned and never read: `recovery_case` and `assignment` (P3), `document_intake` and the rest of `rwb_document` (P5), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| reference-data fake of `rwb-case` (`RWB-PLT-E1043-CON`) | LOV-PANEL with ACTIVE, ON_NOTICE, SUSPENDED and EXITED and LOV-PARTNER-TYPE with its eight values, at their version, and a stopped answer | AC5, X5 |
| document-intake contract fake (`RWB-P5-E1057-CON`) | The declared partner reference of one intake item, so the answer is validated as a consumer sees it | AC1, AC8 |
| partner panel fixture | Partner "LF-007" ACTIVE as a law firm, "LF-008" SUSPENDED and no row for "LF-099" | AC1 to AC3, AC9 |
| gateway-bff composite route fake | The merged `GET /partners` answer for the partner portal, before and after a panel change | AC9 |

The fakes are test-only and are replaced by the real services in SIT. The `code` filter and the not-found behaviour carry the placeholder until the contract owner confirms them (GAP-3146; ASM-5514).

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 1 | `GET /api/recovery/partner/v1/partners` with the `code` filter; the reference-data read of `rwb-case`; one hop, 2 s |
| Kafka | Published 0, consumed 0 | EV-20 and EV-21 belong to the instruction steps; a read announces nothing (§12.3, §12.4) |
| Temporal | 0 workflows, 0 activities, 0 Schedules | The read is synchronous; `InstructionWorkflow` and the intake's `DocumentIntakeWorkflow` are other stories' |
| File | None | No file is read, moved or delivered: the channels are P5's and this story answers a code |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `directory`; no front-end component, because the read is called by the intake and rendered by SCR-34 in another story.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Where it lands in this slice |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | `partner` is read in `rwb_partner` only; the caller reads no partner table, and `partner_instruction` and `partner_user` are not read here. Adds no dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | Landed by RWB-P5-E1057-APP for the five `INTAKE_*` rows; this slice reads no parameter, so it adds no `RWB-PLT-E1042-CON` or `RWB-P3-E1042-CON` row |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | LOV-PANEL and LOV-PARTNER-TYPE through the client library: `H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON` (section 12.2; the plan's H row is empty, see the assumption) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | Inherited with the key: the topic `rwb.partner.events.v1` is this service's, but a read publishes and consumes nothing, so no library row and no `RWB-PLT-TE006-CON` is needed here |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | Landed by RWB-P5-E1057-APP and RWB-P5-E1057-OPS: the fifteen-minute Schedule is `rwb-document`'s. This service has no job and declares none |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | The substantive change of the slice: `PartnerDirectory.findByCode` becomes the published read, one hop with a 2 s budget, a breaker and a fake. Adds no H row; the C row is `RWB-P5-E1057-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | The operation is served under `/api/recovery/partner/v1`. Adds no dependency |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | The read runs on the per-service baseline that creates `partner`; this story adds no migration and no `RWB-PLT-E1044-CON` row |
| DP-19 | Screen, ace-web | gateway-bff composite route | The partner portal reaches `GET /partners` through the composite route and the intake reaches it server to server; this story adds no route and no `RWB-PLT-N001-CON` row |

The plan lists nine patterns for the key and four of them — DP-06, DP-09, DP-10 and DP-19 — take effect in the P5 slice or in the portal stories and not in this read; they are kept in the metadata because the pattern list is the key's, and section 12 states for each of them that it adds no row here (ASM-5516).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerDirectoryController` | Controller | The list and the `code` filter of API-S9-001, partner-portal right R, the scope, and the RFC 9457 problem mapping |
| `PartnerDirectoryService` | Service | Resolves the code to one `partner` row and returns the six published properties; decides nothing |
| `PartnerRepository` | Repository | Reads `partner` in `rwb_partner` only; the code filter is one lookup on the code |
| `PanelListReader` | Library adapter | Reads LOV-PANEL and LOV-PARTNER-TYPE through the reference-data client, with its 5-minute cache and its breaker |
| `PartnerAnswerMapper` | Mapper | Maps the row to the published `Partner` element and refuses any property outside the six |

**Deliverables and build steps.**

1. Map the contract: the list branch, the `code` filter and the `Partner` element as RWB-P5-E1057-CON and TSD S9 T-A.2 declare them; the consumer test of AC8 runs against the fake from Day 1.
2. Build `PartnerRepository` and the lookup on the code; the index that makes it one lookup is part of the service's own Flyway baseline and the constraint on the code carries the placeholder (GAP-3146; ASM-5518).
3. Build `PanelListReader` against the reference-data fake and stop the answer when the read fails, with MSG-GEN-006.
4. Build `PartnerAnswerMapper` and the emptiness rule: a code with no row answers an empty list and no error (AC2).
5. Build `PartnerDirectoryController` with the right, the scope and the problem mapping; test the 403 of AC4 and the 422 of AC5.
6. Prove the purity (AC7), the panel change (AC9) and the no-personal-data rule (AC10) on the fixtures, and add the boundary statement test of AC6 to the pipeline.

**Done when.** The ten criteria of section 7 pass on the fakes, the answer carries the six published properties and nothing else, a panel change is visible on the next read, and the boundary test shows no `v_ace_*`, no `recovery_case` and no `document_intake` statement.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role lacks the partner-portal right R the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required query value is absent or outside its list | Enter {field}. |
| MSG-GEN-006 | The database or the reference-data read does not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P5-007 | The caller refuses a file at intake for an unknown or a not-ACTIVE partner (new) | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. |

The three platform messages are three of the legacy message set of the key copied unchanged, and MSG-P5-007 is the caller's message: its two reasons `PARTNER_UNKNOWN` and `PARTNER_NOT_ACTIVE` are the legacy values of AC7 and this story supplies the fact they are built on, never the text. Delivery shape: every error is an RFC 9457 problem response with `messageId`, `detail` and `instance`; 403 for MSG-P4-002, 422 for MSG-GEN-001, 503 for MSG-GEN-006. The not-found behaviour of an unknown code is not an error: it is an empty list with 200, and no message is invented for it (GAP-3146; ASM-5514). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The partner portal's SCR-34 Partner list shows the same rows through the gateway-bff composite route, and its maintenance actions and states belong to RWB-S9-E6029-APP and RWB-S9-E6030-APP; the intake run of the legacy story shows on SCR-44 Interface and job monitor and belongs to P5 and to Epic 2.

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-34 Partner list | Loading; list | Partners with their code, name, type, panel status and score, read through the composite route; no action is built here |
| SCR-34 Partner list | Empty | Not specified in the source documents (CG-ALL-11753) |
| SCR-34 Partner list | Error | Not specified in the source documents (CG-ALL-11753) |
| SCR-34 Partner list | No access | Not specified in the source documents (CG-ALL-11753) |
| SCR-44 Interface and job monitor | running, complete, failed | The intake run with its counts per channel and result; published by RWB-P5-E1057-APP and not by this story |
| SCR-44 Interface and job monitor | Empty | Not specified in the source documents (CG-ALL-11754) |
| SCR-44 Interface and job monitor | Loading | Not specified in the source documents (CG-ALL-11754) |
| SCR-44 Interface and job monitor | Error | Not specified in the source documents (CG-ALL-11754) |
| SCR-44 Interface and job monitor | No access | Not specified in the source documents (CG-ALL-11754) |

The panel read adds no state, no dialog and no field to either screen: it answers the intake and the list. The refusal states the officer sees are the caller's, with MSG-P5-007 and its two reasons.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-057-17 | Access of the legacy key, answered here for the read | Component | A role without partner-portal right R asks for "LF-007"; 403 with MSG-P4-002 |
| TC-E1-057-01 | AC1 of RWB-P5-E1057-APP (the branch channel), proved there | End to end | Synthetic PDF in branch folder "BR-0123" |
| TC-E1-057-02 | Legacy AC2 Partner SFTP: the partner half is AC1 and AC3 here | Component | Synthetic PDF in SFTP subfolder "LF-007"; the panel fixture answers ACTIVE |
| TC-E1-057-03 | Legacy AC3 Mailbox, proved by RWB-P5-E1057-APP | End to end | Mailbox stub with one PDF attachment, synthetic sender |
| TC-E1-057-04 | AC4 of RWB-P5-E1057-APP (the mailroom channel) | End to end | Synthetic PDF in the mailroom folder |
| TC-E1-057-05 | AC5 of RWB-P5-E1057-APP (a refused type) | End to end | DOCX file |
| TC-E1-057-06 | AC6 of RWB-P5-E1057-APP (the size boundary) | End to end | Files of 25.1 MB and 25.0 MB |
| TC-E1-057-07 | Legacy AC7 An unknown or suspended partner is refused: AC2 and AC3 here | Component | Subfolders "LF-099" and "LF-008"; the empty list and the SUSPENDED row |
| TC-E1-057-08 | AC8 of RWB-P5-E1057-APP (the duplicate window) | End to end | The same file two days apart |
| TC-E1-057-09 | AC9 of RWB-P5-E1057-APP (an empty run) | End to end | All channels empty |
| TC-E1-057-10 | AC10 of RWB-P5-E1057-APP (the container refuses writes) | End to end | Hold container stub refusing writes, then accepting |
| TC-E1-057-11 | Run by RWB-P5-E1057-APP: AC11 (two failed runs raise the alert) | End to end | SFTP folder unreadable for two runs |
| TC-E1-057-12 | Run by RWB-P5-E1057-APP: AC12 (one run across two instances) | End to end | Two service instances, one run slot |
| TC-E1-057-13 | Run by RWB-P5-E1057-APP: AC13 (no usable attachment) | End to end | Email with no attachment; email with a 6 KB image |
| TC-E1-057-14 | Run by RWB-P5-E1057-APP: AC14 (a file seen again after a failed move) | End to end | The move to processed forced to fail |
| TC-E1-057-15 | Run by RWB-P5-E1057-APP: AC15 (outside business hours) | End to end | Clock set to 18:15 on a working day |
| TC-E1-057-16 | Run by RWB-P5-E1057-APP: AC16 (scanned before OCR) | End to end | An item taken in, the scan stub delayed |
| TC-S9-E1057-01 | AC1 | Contract | The `code` filter on "LF-007"; the six properties validated against the P5 contract fake |
| TC-S9-E1057-02 | AC2 | Component | No row for "LF-099"; 200 with an empty list and no write |
| TC-S9-E1057-03 | AC3 | Component | "LF-008" SUSPENDED; the row returned with its stored status |
| TC-S9-E1057-04 | AC4 | Component | A role without partner-portal right R; 403 with MSG-P4-002 |
| TC-S9-E1057-05 | AC5 | Component | The two list fakes; a value outside LOV-PANEL with 422; a stopped list read with 503 |
| TC-S9-E1057-06 | AC6 | Component | The grant inspection and a statement on `rwb_document`; refused by the database |
| TC-S9-E1057-07 | AC7 | Component | Two reads of "LF-007"; no row, no decision record, no outbox row and no idempotency row |
| TC-S9-E1057-08 | AC8, AC9, AC10 | Contract | The P5 contract fake, the answer validated, a panel change between reads and the log inspected for personal data |
| TC-S9-E1057-09 | Section 12.7 tables: partner_user and partner_instruction | Component | Read and write statements on partner_user and partner_instruction; refused by the database; no row changed |
| TC-S9-E1057-10 | BR8 (no folder, mailbox, type, size or window literal) | Component | Inspection of the service code for folder names, mailbox codes, type lists, sizes and windows; none found |
| TC-S9-E1057-11 | AC11 | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC17) | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC17) |
| TC-S9-E1057-12 | AC12 | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC18) | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC18) |
| TC-S9-E1057-13 | AC13 | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC19) | Not specified in the source documents (NEWAC-RWB-S9-E1057-APP-AC19) |

The seventeen legacy cases are the key's, kept by ID and in the plan's order; the cases of the eleven criteria the plan gives RWB-P5-E1057-APP are proved there and are listed here because they are the same legacy key, so the corpus holds one chain per legacy case. This story answers two of them at component level — TC-E1-057-02 and TC-E1-057-07, the partner half — and the wave 1 harness copies the end-to-end ones as `-ITG` cases in RWB-ITG-E1057-ITG. The thirteen new cases carry this story's own criteria and rules. The full tests, with their Given, When and Then, sit in the Workbench test case workbook, tab Story test cases, under the same IDs.

### 17. Guardrails

- No business value in code: the panel states, the partner types, the two reasons, the right and the lists are rows read through DP-07, never a literal or a branch of the code.
- No personal data in a row, an answer, a log or a payload: the partner row is a firm, the answer carries six fields, and no sender address, file name or mailbox code enters this service (BR9, AC10).
- No read of another service's tables and no copy of one: `partner` is read in `rwb_partner` only, `document_intake`, `recovery_case` and every `v_ace_*` view are out of reach of the login, and the boundary test proves it (DP-01, AC6).
- The read writes nothing: a build that inserts a partner row, writes a decision record, an outbox row or an idempotency row, or publishes an event from this read fails the purity test (AC7, DP-09).
- The rule stays in one place: this service answers the panel status and refuses nothing; the caller executes BR4 and renders MSG-P5-007 (ASM-5514).
- One base, one topic, one queue, one schema and one login per service: a build that names another service's base, topic or schema as its own fails the review (DP-13, DP-14).
- No parameter and no limit in this service: a file type, a size, a window or an alert threshold in this code duplicates P5's parameters and fails the review (DP-06, BR8).
- No cache of the panel row: a second copy of `partner` in any store would answer an old status after a suspension (AC9).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature and element | Test cases | L3 process |
|---|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | FEAT-DCM-14, the partner SFTP path; this story answers the partner panel read it needs | TC-E1-057-02, TC-E1-057-07, TC-S9-E1057-01 to -04 | 13 Manage documents and correspondence |
| REQ-DCM-010 | Retention class on every document; virus scan before storing | FEAT-DCM-13; not executed here, because the panel read stores no document | TC-E1-057-16 (proved by RWB-P5-E1057-APP) | 13 Manage documents and correspondence |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login, with no grant outside it | TC-S9-E1057-06 | 12 Manage partners |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The partner read the intake calls, and the reference read it makes | TC-S9-E1057-01, TC-S9-E1057-05 | 12 Manage partners |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-057, disposition Split (rework); L3 processes 13 Manage documents and correspondence and 12 Manage partners; module S9 Partner management |
| Legacy criteria | The plan gives this secondary slice none; the eleven criteria of RWB-P5-E1057-APP stay there, and the partner half of legacy AC2 and AC7 is answered here |
| Source text | Legacy RWB-E1-057 sections 1 to 19, section 12's `PartnerDirectory.findByCode` and section 3's partner panel; FSD S9 Partner management v3 A1.1 to A1.4, A2.1.3.1, A2.2.3.1, A2.2.4.4 and the requirements served; TSD S9 Partner management v2 T1, T2, T3.0 to T3.3, T5.2, T6.1, T7, T-A.1 and T-A.2; context pack S9 rwb-partner (service row, ownership rows, naming rules) |
| Test cases | The seventeen legacy cases of the key, kept by ID, and thirteen new cases TC-S9-E1057-01 to -13 |
| Feature and screens | FEAT-DCM-13, FEAT-DCM-14, FEAT-DCM-15; SCR-34 Partner list (the panel) and SCR-44 Interface and job monitor (the caller's run) |
| Screen states | SCR-34 and SCR-44 empty, error and no access states, and SCR-44 loading: Not specified in the source documents (CG-ALL-11753, CG-ALL-11754, DOR-RWB-S9-E1057-APP-10); the API answers 200 with an empty list, 403 with MSG-P4-002 and 503 are tested at API level (TC-S9-E1057-02, -04, -05) |
| Decoupling patterns | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Architecture decisions | ADR-014, ADR-020 |
| Open decisions | DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355); both remain open, each with its assumptions |

### 19. Out of scope

- The branch scanner, mailroom, SFTP and mailbox readers, the file hash, the duplicate window, the type and size checks, the hold-container copy, the `document_intake` rows, the moves to the processed, rejected and archive folders and the intake run record: RWB-P5-E1057-APP.
- The malware scan and quarantine, the OCR, the classification, the extraction and the match to a case: RWB-P5-E1041-APP, RWB-P5-E1049-APP, RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1032-APP.
- The partner panel, its states, its contract terms and its fee schedule as maintained data: RWB-S9-E6029-APP and RWB-S9-E6030-APP; the notice, the exit and the recall of work: the EP07 stories of the module.
- The instructions placed with a partner, their acceptance, their result and their invoice: RWB-S9-E6031-APP, RWB-S9-E6033-APP and the fee stories.
- The public shapes of the operation, the elements, the rights and the fakes: the API specification and RWB-S9-E1057-APP's own section 12; the intake contract is RWB-P5-E1057-CON.
- The SFTP and mailbox channels, the hold container, the identity, the secrets and the DMZ position: RWB-P5-E1057-INF. The chart, the Schedule registration, the flag, the dashboards and the runbook: RWB-P5-E1057-OPS.
- The gateway-bff composite route and the screen field lists of SCR-34 and SCR-44: RWB-PLT-N001-CON and the edge and Epic 2 stories.
- The real cross-service journey of the intake with a live partner service: RWB-ITG-E1057-ITG.
- The panel-transition table, the constraint on the partner code and the not-found behaviour of the read: held as open items (GAP-3146; ASM-5514, ASM-5518, ASM-5519).
