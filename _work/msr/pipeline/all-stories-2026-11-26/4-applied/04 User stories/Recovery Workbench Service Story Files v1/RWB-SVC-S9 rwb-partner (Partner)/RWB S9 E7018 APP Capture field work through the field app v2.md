# RWB-S9-E7018-APP Capture field work through the field app

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S9-E7018-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the field-work slice of RWB-E7-018 in rwb-partner. Both legacy criteria are kept word for word with their origin tags. The field collector submits the visit result and its evidence on the published `POST /partner/instructions/{instructionId}/results` (API-S9-005) as a multipart call on base `/api/recovery/partner/v1` (DP-13): the result and the status go on `partner_instruction`, the visit is an interaction entry requested from rwb-source-data (DP-18), the photographs and bills are documents handed to rwb-document as claim-check references, the local decision record is written before any change with the rule ID and the version in force (DP-03), and the panel read behind SCR-35 goes through the gateway-bff composite route (DP-19). No source gives the field visit a table in S9, publishes a field-collector role, a result-code list, a document or interaction operation name, or a partner route set, and TSD S9 T8 maps REQ-S9-009 to another feature (GAP-3135; ASM-5491, ASM-5492, ASM-5493, ASM-5494, ASM-5495, ASM-5496, ASM-5497, ASM-5498, ASM-5499, ASM-5500, ASM-5501). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S9-E7018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **field collector**, I want **the Workbench to let the field collector record visits, photos and bills against the case from the field**, so that **partners are placed, paid and measured by rule**.

This is the app slice of legacy RWB-E7-018 (FEAT-PRM-15). It owns:

- the two legacy criteria AC1 and AC2, copied verbatim with their origin tags, and the three messages they name;
- the field-work branch of the published result operation `POST /partner/instructions/{instructionId}/results` (API-S9-005), multipart `result` and `files`, partner portal right U, the `Idempotency-Key` header and the 2 s budget of one hop;
- the recording of the result on `partner_instruction`: `result_code` (DF-PRT-015) and `status = DONE` (DF-PRT-014, LOV-INSTR-STATUS);
- the resolution of the caller to one `partner_user` row and one firm, so a collector of one firm can never reach another firm's instruction;
- the visit as one interaction entry requested from rwb-source-data, channel `VISIT`, source `FIELD_VISIT` (DP-18);
- the photographs and the bills as rwb-document documents, handed over as claim-check references and never stored in `rwb_partner`;
- the local decision record written through RWB-PLT-E1027-CON with the rule ID, the version in force, the instruction, the result and the document count, **before any change** (DP-03);
- the offline capture and the upload on reconnect of NFR-062, carried as the client's queue plus the service's idempotent repeat;
- the panel read `GET /partners` (API-S9-001) behind SCR-35 through the gateway-bff composite route (DP-19), and the instruction on PRT-02 through the partner gateway.

It does not own: the published shapes, the elements, the lists, the rights of the document, the error envelope and the fakes, which are RWB-S9-E7018-CON; the portal result intake of the same operation, which is FEAT-PRM-05 (RWB-S9-E6033-APP); issuing and accepting an instruction (RWB-S9-E6031-APP, RWB-S9-E6032-APP, RWB-S9-E6034-APP); the fee and the invoice (RWB-S9-E7012-APP, RWB-S9-E6035-APP); scoring the partner (RWB-S9-E7011-APP) and the panel as reference data (RWB-S9-E6030); the document hub and its index (P5 rwb-document); the interaction ledger (P1 rwb-source-data); the case of record and its clock (P3 rwb-case); the rule rows and the central ledger (P7 rwb-decision); and the composite route and the field-app screen list (RWB-PLT-N001-CON and the edge stories).

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: the field collector records visits, photographs and bills against the case from the field, because partners are instructed and paid by email and spreadsheet and allocation is not based on performance (FSD S9 A1.3, A2.15.1), and placements by scorecard are measured on the decision log and the Workbench records against 100 percent, reviewed monthly (FSD S9 A2.15.1). What D-RCV-60 changes is where each fact of a field visit lives.

- **The evidence is not this service's row.** The ownership rows give S9 three tables and none of them is a document, and REQ-DCM-013 sends field photographs and bills to the same intake and index as scanned documents, so the evidence is a rwb-document element and the instruction holds its reference only (ASM-5491).
- **The visit is not this service's row either.** `interaction` is P1's by the default ruling, its channel list already carries `VISIT` and its source list carries `FIELD_VISIT` (DP-18, ASM-5493), so the visit is one ledger entry requested on that contract.
- **The result is this service's.** `partner_instruction` is S9's in `rwb_partner`, `result_code` and `status` already exist on it (DF-PRT-014, DF-PRT-015), and LOV-INSTR-STATUS already carries `DONE`, so the field-work outcome is one update of a row this service owns (ASM-5494).
- **The collector is a partner user.** `partner_user` binds one identity to one firm and one partner role (DF-REF-212 to DF-REF-217, LOV-ROLE), the partner gateway of the DMZ (FAPI 2.0) fronts this service for partner identities, and API-S9-005 declares partner portal right U, so the field app is a partner-side client of that gateway (ASM-5492, ASM-5501).
- **Offline capture is a client duty with a server duty.** NFR-062 asks the field application to capture evidence with no network connection and upload when it reconnects; the service's half of that promise is that a repeat of one submission writes one result, which is what the `Idempotency-Key` of API-S9-005 gives (ASM-5501).
- **No rule row decides a field visit.** The Business Rules and Routing Logic v4 has no partner route set: the nearest rows are R-UNI-38, R-UNI-39 and R-UNI-40, and none of them names a visit or a result, so the rule ID and the version in force the record carries have no row to cite (ASM-5496).

No business value is written in code: the result vocabulary, the panel and instruction lists, the role codes, the rule ID and its version are read with their version, and where a source is silent the placeholder stands.

### 3. Preconditions

- RWB-S9-E7018-CON is published: the field-work element of the result operation, the document and interaction references, the lists, the rights, the error envelope, the event shape and the fakes are baselined.
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-35 reaches this service through the gateway-bff composite route, one hop, and no staff screen calls a service directly (DP-19).
- `partner`, `partner_instruction` and `partner_user` exist in schema `rwb_partner` from the DB story of this service, with the columns of DF-PRT-001 to DF-PRT-016, DF-REF-212 to DF-REF-217 and the standard record columns of TSD S9 T3.0; this story adds no table, no column and no migration.
- The instruction exists at `SENT`, `ACCEPTED` or `IN_PROGRESS`, and its firm's contract is in force with the panel status `ACTIVE`.
- The rwb-document intake, the rwb-source-data ledger and the rwb-decision rule version are published with their fakes. Their operation names, the media types and size limits of an upload, and the result-code vocabulary are Not specified in the source documents (GAP-3135; ASM-5491, ASM-5493, ASM-5494, ASM-5496).
- The service runs as its own login on schema `rwb_partner`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_document`, `rwb_source_data` or an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7018-CON when its tests pass.

### 4. Flow

1. The field collector opens PRT-02 Instruction on the field app while offline, records the visit, takes the photographs and lists the bills, and the client keeps the submission in its own queue (NFR-062).
2. On reconnect the client resolves its `partner_user` identity through the partner gateway (FAPI 2.0) and sends one multipart submission to `POST /partner/instructions/{instructionId}/results` (API-S9-005) with the `Idempotency-Key` it minted offline.
3. `PartnerInstructionController` serves the operation on base `/api/recovery/partner/v1`, declares partner portal right U with the scope applied, requires the key, refuses a media type outside the declared set with 415 and validates the parts (DP-13).
4. `FieldWorkScope` resolves the caller to one `partner_user` row at its `valid_from` and `valid_to` and to its firm, and refuses an instruction of another firm with 404 and nothing read further (X2).
5. The step reads the instruction in `rwb_partner`: its reference, its case reference, its firm, its type, its status and its due date. An instruction already `DONE`, `DECLINED` or `RECALLED` is refused with 409 and nothing is written (X3).
6. The step reads the rule in force: the rule ID and the version at their effective date, read through the rwb-decision contract (R-UNI-38). No partner route set exists, so the value carries the placeholder (ASM-5496).
7. `FieldWorkDecisionRecordWriter` writes one record through the local library **before any change**: the instruction, the case, the firm, the result, the document count, the rule ID and the version in force, and the decided-at time. A failed write stops the step with nothing changed (DP-03; AC2).
8. `DocumentClient` hands the photographs and the bills to rwb-document as claim-check claims (link and manifest, never the bytes in this service) and holds the document references; rwb-document owns the document, its type, its index and its retention (ASM-5491).
9. `InteractionLedgerClient` records one interaction entry for the visit with channel `VISIT`, source `FIELD_VISIT`, the case, the firm and the visit date; the ledger is rwb-source-data's and this service holds no interaction row (DP-18).
10. `RecordAndApply` commits in one transaction: `partner_instruction.result_code`, `status = DONE`, the audit columns and the optimistic-lock version, the outbox row of EV-21 and the key of the submission. The record of step 7 is void if this commit does not happen (DP-03).
11. `rwb.partner.PartnerResultSubmitted.v1` (EV-21) leaves through the outbox, keyed by the case, carrying the instruction, the result and the document references, for rwb-case to apply and for rwb-reporting to read (DP-09).
12. The answer returns the instruction with its result, its status and its document references; a repeat of the same key answers that instruction and writes no second result, no second document set, no second ledger entry and no second record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: the instruction keeps its status and its result, no document is handed over and no ledger entry is written | MSG-P7-003 | AC2, TC-E7-018-02, TC-E7-018-04 |
| X2 | The caller holds no partner portal right U, or the instruction belongs to another firm | 403 with MSG-P4-002 for the right, 404 for the firm boundary, before any write | MSG-P4-002 | TC-E7-018-03 |
| X3 | The instruction is `DONE`, `DECLINED` or `RECALLED` | 409 with nothing written; a result is never recorded twice and never on a closed instruction | Not specified in the source documents (GAP-3135; ASM-5500) | AC2 |
| X4 | A required part is absent, an upload exceeds the declared limits, or the media type is not declared | 422 with MSG-GEN-001 for a missing or unformed part, 415 for the media type, nothing written | MSG-GEN-001 | Section 17, BR8 |
| X5 | rwb-document, rwb-source-data or rwb-decision does not answer inside 2 s, or its breaker is open | The transaction rolls back, the client retries the submission with the same key, and nothing is committed | None | BR5, BR10 |
| X6 | The same submission arrives twice, which is the normal reconnect case of NFR-062 | One result, one document set, one ledger entry, one record and one event; the repeat answers what exists | None | BR10 |
| X7 | A component, a statement or a test reaches a `v_ace_*` view, a `document` or `interaction` row, or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6, BR7 |
| X8 | The rule in force is absent at its effective date | 503 with nothing written; the step never falls back to a rule ID or a version of the code | Not specified in the source documents (GAP-3135; ASM-5496) | BR8 |

X1 and X2 are the legacy exception paths, carried onto the slice with the legacy messages; X3 to X8 are the paths the instruction state, the three contracts and the offline client add.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7018-CON, the decision-record stub and the document, ledger and rule fakes, on its own schema, and needs no live P1, P3, P5 or P7 |
| Negotiable | The component, activity and client names and the internal record shape are this story's and the baseline's choice; the operation, the right, the lists, the messages and the criteria are fixed |
| Valuable | A visit made in the field reaches its case with its photographs and bills the same day, once, with the decision record to prove which rule version it was recorded under |
| Estimable | One operation branch, one scope resolver, one comparator on the instruction state, one record write, three clients, one event and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Both criteria run on the stubs and the fakes, plus the closed-instruction, other-firm, media-type, no-answer and repeat cases |

### 7. Acceptance criteria

```gherkin
Feature: Capture field work through the field app

  Background:
    Given the instruction "INS-000318" of the firm "PRT-0007" is open with its case reference and its due date
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Capture field work through the field app (legacy RWB-E7-018 AC1)
    Given the rwb-source-data contract mock returns the visit entry of the ledger accepted for the case
    Given the rwb-document contract mock returns the document reference of each photograph and each bill the field collector uploads
    Given the rwb-decision contract mock returns the rule version this feature needs
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the field collector record visits, photos and bills against the case from the field
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E7-018 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E7-018 word for word, with their origin tag added and nothing else changed: `the data and the rule version this feature needs are in place`, `the user acts on the screen`, `the action is taken` and the single `Then` of AC2 all stand. AC1 is the only one with cross-service parts, so it carries the three `Given the <service> contract mock returns <x>` lines and they are the only additions; the three keep every legacy value — the data is the visit and its evidence, the rule version is the version in force. AC2 has no cross-service part and is copied with nothing added. On this story "the user" is the field collector on PRT-02, "the screen" is the field app, "the action" is the submission of the visit and "the result" is the instruction's result code with its `DONE` status. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_partner`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-38 | Universal rules | All | ANY_ACTIVE | RULE_VERSION_EFFECTIVE | a new rule version reaches its effective date | Apply it to decisions taken from that date. Open cases keep the version they were decided under | RESUME_STATE | Center of excellence | Workbench | on the effective date |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-40 | Universal rules | All | ANY_ACTIVE | DUPLICATE_EVENT | the same event arrives twice with the same key | Ignore the second event, record the idempotency hit | RESUME_STATE | Workbench | Workbench | None |

The three rows are copied character for character from the Business Rules and Routing Logic v4. This story reads R-UNI-38 for the version it stamps, R-UNI-39 for the record-first rule and R-UNI-40 for the reconnected repeat. No row of the ten route sets names a partner visit or a partner result, and no `R-PRM` set exists (ASM-5496).

| ID | Rule | Source |
|---|---|---|
| BR1 | The field-work step is a step of `InstructionWorkflow` on `rwb-partner`: it reads `partner`, `partner_instruction` and `partner_user`, writes `result_code`, `status` and the audit columns of the instruction, and writes nothing else in `rwb_partner` | TSD S9 T3.0, T3.1, T4; context pack ownership rows (3 tables, 1 workflow, no job); FSD S9 A2.15.2 |
| BR2 | The result is recorded before the change, with the rule ID, the version in force, the instruction, the case, the firm and the result; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S9 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | A result is recorded only on an instruction of the caller's own firm at `SENT`, `ACCEPTED` or `IN_PROGRESS`; `DONE`, `DECLINED` and `RECALLED` are refused | TSD S9 T3.2 (LOV-INSTR-STATUS); TSD S9 T6.1; ASM-5500; legacy AC1 |
| BR4 | The visit is one interaction entry of rwb-source-data with channel `VISIT` and source `FIELD_VISIT`; this service holds no interaction row and updates no ledger entry | DP-18; LDM v8 DF-INT-001 to DF-INT-013 and LOV-CONTACT-SRC; ASM-5493 |
| BR5 | The photographs and the bills are rwb-document documents handed over as claim-check claims; this service holds their references, never the content, the type, the index or the retention | FSD S9 A2.15.2; REQ-DCM-013; ASM-5491 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of other services' facts | DP-01; TSD S9 T3.3 |
| BR7 | The service reads no `v_ace_*` view and holds no grant on one; ACE data reaches the panel only through rwb-source-data or the owner's contract | DP-01, DP-05; Template and Rules §R7.2 (s17) |
| BR8 | Every value a business person may change is reference data, a list or a rule value read with its version: the result vocabulary, LOV-INSTR-STATUS, LOV-INSTRUCTION, LOV-PANEL, LOV-PARTNER-TYPE, the role codes and the rule in force. The result vocabulary has no list and carries the placeholder | FSD S9 BR-S9-015; TSD S9 T3.2; ASM-5494, ASM-5496 |
| BR9 | No personal data in `rwb_partner`, the record, a log, a workflow input or the event: identifiers, codes, list values, dates, a count of documents, a rule ID and a version only | Template and Rules §R7.2 (s17); TSD S9 T6.2; NFR-053 |
| BR10 | One submission writes one result: the operation declares the `Idempotency-Key` header and stores the key and its answer, so the offline queue of the field app may resend the same visit on reconnect and be answered once | TSD S9 T-A.2; NFR-062; R-UNI-40; ASM-5501 |
| BR11 | This step publishes EV-21 and consumes no event; the answer of the caller is the REST response and the case owner is told by the event | Event and Messaging Design v5 EV-21; TSD S9 T5.3; ASM-5495 |

### 9. State transitions

| From (instruction status, rwb-partner) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `SENT` | The field collector accepts and records the visit | The firm matches and the instruction is open | `IN_PROGRESS` then `DONE` | This story records the result; acceptance is RWB-S9-E6034-APP (ASM-5497) |
| `ACCEPTED` | The field collector records the visit | The firm matches and the instruction is open | `IN_PROGRESS` then `DONE` | rwb-partner, by this story |
| `IN_PROGRESS` | The field collector records the visit | The firm matches and the instruction is open | `DONE` | rwb-partner, by this story |
| `DONE` | A second submission, or the reconnect repeat with the same key | The instruction already holds a result | `DONE`, unchanged; the repeat is answered from the key | none; 409 for a new key (X3) and 200 for the same key (X6) |
| `DECLINED`, `RECALLED` | Any submission | The instruction is closed | Unchanged | none; 409 (X3) |
| `DONE` | The firm's contract ends or a conduct breach is upheld | FEAT-PRM-12 or FEAT-PRM-13 applies | `RECALLED` | RWB-S9-E7015-APP and RWB-S9-E7016-APP, not this story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Queued in the field app | The collector completes a visit offline | No network | Queued, nothing sent (NFR-062) |
| Waiting | A submission arrives on reconnect | The caller, the instruction and the rule are read | Evaluating |
| Evaluating | The firm matches and the instruction is open | BR3, X2 | Recording |
| Evaluating | The instruction is closed or belongs to another firm | X2, X3 | Waiting, nothing changed |
| Recording | The record, the document claims, the ledger entry and the row commit | The transaction commits | Done; the answer and the event leave |
| Recording | A write or a call fails | X1, X5 | Waiting, nothing changed |

LOV-INSTR-STATUS is `SENT`, `ACCEPTED`, `DECLINED`, `IN_PROGRESS`, `DONE` and `RECALLED` (TSD S9 T3.2). This story writes `DONE` only; the legacy PRT-02 states `New`, `accepted`, `in progress`, `result` and `closed` are the screen's words for `SENT`, `ACCEPTED`, `IN_PROGRESS` and `DONE`, and `DECLINED` and `RECALLED` have no screen state of their own (ASM-5497).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC | Partner portal RU in TSD S9 T6.1: the six partner identities that hold right U, so a field collector of a firm submits its own visits and reads nothing of another firm (ASM-5492) |
| RW-AGENCYMG, partner and agency manager | Partner portal CRUDA in TSD S9 T6.1: the primary business role of FSD S9 A2.15.3.3 besides the field collector, submitting on behalf of a firm |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT | Partner portal CRU in TSD S9 T6.1: right U, the six staff roles the legacy permission table names with right U (ASM-5492) |
| RW-CASEOWN, RW-TEAMMGR, RW-LEGAL, RW-CONDUCT, RW-CAPACITY, RW-PRODHEAD, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-BIANAL, RW-TRIBE | Partner portal R in TSD S9 T6.1: read only and refused the submission; they are part of the legacy "and 21 more" (ASM-5492) |
| `partner_user` row of the caller | Binds the identity to one firm and one partner role over LOV-ROLE, with `valid_from` and `valid_to`; no role code names a field collector, so the code the collector holds is Not specified in the source documents (GAP-3135; ASM-5492) |
| rwb-partner service identity | Reads the instruction, the partner and the caller's binding, writes the result and the record, and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S9 T6.1 and T-A.1 and nothing wider: the 13 identities that hold U are exactly the eight the legacy permission table names plus its "five more", and the 29 identities of the Partner portal column all hold R, which is the legacy "and 21 more". DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated and not built.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Read, to resolve the instruction, its case and its firm |
| DF-PRT-011, DF-PRT-012, DF-PRT-013 | partner_instruction (S9) | instruction_type, instructed_at, due_at | Read, LOV-INSTRUCTION and the clock |
| DF-PRT-014 | partner_instruction (S9) | status | Write `DONE`; read for the state check (LOV-INSTR-STATUS) |
| DF-PRT-015 | partner_instruction (S9) | result_code | Write, the reported result; its vocabulary has no list: Not specified in the source documents (GAP-3135; ASM-5494) |
| DF-PRT-016 | partner_instruction (S9) | fee_amount | Not written: the fee is FEAT-PRM-07 |
| DF-PRT-001, DF-PRT-002, DF-PRT-004, DF-PRT-005, DF-PRT-006 | partner (S9, `rwb_partner`) | id, partner_code, partner_type, panel_status, contract_end | Read, the firm, its type, its panel status and its contract |
| DF-REF-212, DF-REF-213, DF-REF-214, DF-REF-215, DF-REF-216, DF-REF-217 | partner_user (S9, `rwb_partner`) | id, identity_ref, partner_id, role_code, valid_from, valid_to | Read, the caller's binding to its firm and its role over LOV-ROLE |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before anything else (DP-03) |
| DF-INT-001 to DF-INT-013 | interaction (P1 rwb-source-data) | the case, the channel `VISIT`, the source `FIELD_VISIT`, the contact date and its reference | Not written here: the ledger is P1's by the default ruling (DP-18; ASM-5493) |
| document (P5 rwb-document) | document and its index | the type, the document date, the index entry and the retention of a photograph or a bill | Not written here: handed over as a claim-check claim, the reference held only (ASM-5491) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the rest | Not read as a table and not written: the case reference arrives on the instruction and leaves as the event key |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version | Not read as a table: the rule ID and the version in force are read as values through the contract, and no partner route set exists (ASM-5496) |
| Standard columns | partner_instruction (S9) | `version`, `updated_at`, `updated_by` | Write the audit columns and guard the update with `version` |
| processed_event, outbox_event, idempotency_key | PLT library, created in `rwb_partner` | the outbox row of EV-21 and the key of the submission | Write through the library, in the transaction |

`partner_instruction` is the only business table written, and only `result_code`, `status` and the audit columns of it. **No new table, no new column and no migration**: the three tables arrive with the DB story of this service, and `decision_record`, `processed_event`, `outbox_event` and `idempotency_key` are library objects created in `rwb_partner` by the library's own migration (DP-03, DP-09).

**No personal data.** The rows carry partner identifiers, codes, list values, dates, a count of documents, a rule ID and a version. A photograph of a property and a bill are documents of a case and never enter this schema, this record, this event or a log, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). This story supplies the field-work branch of the result operation, whose shape RWB-S9-E7018-CON declares additively within the baseline of RWB-S9-E6033-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart: `result` as JSON and `files` as one or more claims; `PartnerInstruction` out with the result, the status and the document references; errors 401, 403, 404, 409, 415, 422, 503 | Partner portal, right U, scope applied | `Idempotency-Key` header |
| GET | `/partners` (API-S9-001) | `Partner[]` out over the query type and status, holding the panel with its panel status, its contract end and its score | Partner portal, right R, scope applied | Not applicable |

The errors of API-S9-005 are those TSD S9 T-A.2 publishes, each with the error envelope and one message ID of section 14: 401, 403 with MSG-P4-002, 404 for an instruction outside the caller's firm, 409 for a closed instruction, 415 for an undeclared media type, 422 with MSG-GEN-001 for a missing or unformed part, and 503. The paths, the request and answer element names, the rights and the error codes are published in TSD S9 T-A.1 and T-A.2, so the surface needs no placeholder; what has no published property is the field-work element, the document reference and the result vocabulary, and they carry the placeholder (GAP-3135; ASM-5491, ASM-5494). API-S9-003, API-S9-004 and API-S9-006 belong to the instruction, acceptance and invoice stories and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The interaction entry of the visit (operation name Not specified in the source documents (GAP-3135; ASM-5493)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | One ledger entry for the visit with channel `VISIT`, source `FIELD_VISIT`, the case, the firm and the contact date; answers its reference; faked |
| The document intake of the photographs and the bills (operation name Not specified in the source documents (GAP-3135; ASM-5491)) | `/api/recovery/document/v1` | P5 rwb-document | The intake and the index of each photograph and each bill as a claim-check claim; answers the document reference; faked |
| The rule in force (operation name Not specified in the source documents (GAP-3135; ASM-5496)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule ID and the version at their effective date, read as values; faked |

All three rows are one hop with a 2 s timeout, a breaker per downstream and a retry governed by the client's queue (ADR-020). They are contract dependencies of class C that this story's C row does not carry, and DP-18, DP-05 and DP-09 are not in the pattern set of the key; the absence is recorded (GAP-3135; ASM-5491, ASM-5493, ASM-5496).

#### 12.3 Events published

| Event | Topic and name | Key and envelope | Payload | Consumers |
|---|---|---|---|---|
| EV-21 `PartnerResultSubmitted` | `rwb.partner.events.v1`; `rwb.partner.PartnerResultSubmitted.v1`, CloudEvents 1.0 binary, schema `rwb_partner_partner_result_submitted` | Key and subject: the case ID; `ce_source` rwb-partner; the trace context of the submission | `instructionId`, `result`, `documents`, the submitted time | rwb-case, which applies the result to the case, and rwb-reporting, which reads the fact |

The event leaves through the outbox in the same transaction as the row, so no result exists without its event and no event without its result (DP-09). Event and Messaging Design v5 lists EV-21 as a consumed portal event; in the target the portal ingress is the REST operation and this service publishes the same fact on its own topic, with the case added as key and subject, and the conflict of direction is recorded (ASM-5495). The payload carries identifiers, a result code and document references only: no personal data, no free text and no document content. The retry and `.dlt` topics are the service template's and add no row here.

#### 12.4 Events consumed

None. A visit arrives by the REST operation and the collector's offline queue, not on a topic; the FSD declares no background event for the feature (FSD S9 A2.15.4.4). This story holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per partner instruction; the field-work step rides it | `rwb-partner` in namespace `rwb-recovery` | The `resultSubmitted` signal with the instruction and the submission reference; closes the stage and reports to the parent `CaseWorkflow` of rwb-case |
| `recordFieldWorkResult` | Activity, the one field-work step | `rwb-partner` | The instruction, the caller's binding, the result, the file claims and the rule version in; the result, the status, the document references and the record reference out |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The result and the document count as the stage result; the case stage and its clock are P3's and no REST row is declared for them |

The service owns one workflow and no job in the context pack's ownership rows, and TSD S9 T4 gives it no case state machine of its own. The activity and signal names are a target design choice fixed by no source document, and the parent edge is declared, not built.

#### 12.6 Schedules

None. The submission is started by the collector's client, and the offline queue and the upload on reconnect of NFR-062 are the field application's, not a Temporal Schedule. The service owns no job in the context pack's ownership rows (Jobs: None), and the outbox relay is a library component in every service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The firm, its type, its panel status and its contract; read here, written by the panel stories |
| partner_instruction | S9 (`rwb_partner`) | The work placed with a firm on a case; this story writes `result_code`, `status` and the audit columns |
| partner_user | S9 (`rwb_partner`) | The firm's own identities with their role and validity; read here to resolve the caller (DF-REF-212 to DF-REF-217) |
| decision_record | PLT library, created in `rwb_partner` | The local hash-linked record of the field work (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The key of the submission and the answer it holds |
| outbox_event, processed_event | PLT library, created in `rwb_partner` | The relay of EV-21 and the inbox guard |

Not owned and never read as a table: `document` (P5), `interaction` (P1), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `notice` (P6) and `payment` (P8). No foreign key leaves the schema, and `case_id` and `partner_id` are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document intake fake | A document reference and its index entry for each photograph and each bill claimed | AC1, X5, TC-E7-018-01 |
| rwb-source-data ledger fake | The visit entry accepted with its reference, channel `VISIT` and source `FIELD_VISIT` | AC1, X5, TC-E7-018-01 |
| rwb-decision rule fake | The rule ID and the version in force at the effective date, and a missing-version answer | AC1, X8, TC-E7-018-01 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1, TC-E7-018-02, TC-E7-018-04 |
| Partner gateway and gateway-bff fakes | The caller's firm scope from `partner_user`, and the merged SCR-35 panel answer | TC-E7-018-01, TC-E7-018-03 |

The fakes are test-only and are replaced by the real services in SIT. The three consumed operation names, the upload media types and the result vocabulary carry the placeholder until their owners confirm them (GAP-3135; ASM-5491, ASM-5493, ASM-5494, ASM-5496).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | API-S9-005 and API-S9-001 on `/api/recovery/partner/v1`; the ledger entry of rwb-source-data, the document intake of rwb-document and the rule in force of rwb-decision, one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1`, keyed by the case, written to the outbox; the decision record rides `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity | `InstructionWorkflow` and `recordFieldWorkResult` on `rwb-partner`; the stage outcome returns to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None built or delivered | The photographs and the bills are claim-check claims handed to rwb-document; this service moves no file and holds no content |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `fieldwork`; front end `src/modules/recovery/partner/FieldWork.tsx`, the fragment PRT-02 embeds, behind the partner gateway.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the instruction row, the document claims and the outbox row commit together or not at all, and the legacy "writes the result to the decision log with the rule version" is that record. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the result operation its home. DP-19 is how SCR-35 reaches this service for the staff read, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The plan gives this story H RWB-S9-E7018-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, and C, I and X empty. The three consumed rows of §12.2 are class C dependencies in fact: the ledger of rwb-source-data, the intake of rwb-document and the rule version of rwb-decision, each built against its document and fake on Day 1. DP-18 (the ledger of rwb-source-data), DP-05 (ACE data through the owner) and DP-09 (the outbox and inbox library) are real dependencies of the step and are absent from the pattern set; the absence is recorded rather than added (GAP-3135; ASM-5491, ASM-5493, ASM-5495).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InstructionWorkflow` field-work branch | Workflow | Receives the `resultSubmitted` signal, holds the retry policy of the three calls and reports the result to the parent |
| `recordFieldWorkResult` | Activity | One `rwb_partner` transaction: the record, the row, the outbox row and the key |
| `FieldWorkScope` | Service | Resolves the caller to one `partner_user` binding and its firm and refuses an instruction of another firm |
| `InstructionStateGuard` | Service | Refuses `DONE`, `DECLINED` and `RECALLED`; accepts `SENT`, `ACCEPTED` and `IN_PROGRESS` |
| `FieldWorkDecisionRecordWriter` | Library adapter | Writes the record with the rule ID, the version, the instruction, the case, the firm, the result and the document count before anything else; refuses the step when the write fails |
| `DocumentClient` | Client | The rwb-document claim-check intake, one hop, 2 s, breaker; holds the returned references |
| `InteractionLedgerClient` | Client | The rwb-source-data ledger entry for the visit, one hop, 2 s, breaker |
| `RuleVersionClient` | Client | The rule ID and the version in force, one hop, 2 s; refuses the step when the version is absent |
| `PartnerInstructionController` | Controller | The field-work branch of API-S9-005, right U, the scope, the `Idempotency-Key`, the multipart limits and the problem mapping |
| `FieldWork` | React component | The offline form of PRT-02: the visit, the photographs, the bills and the queued submission |

**Database and migrations.** No Flyway file. The three tables arrive with the DB story of this service, and the record, the key and the outbox are library objects created in `rwb_partner` by the library's migration (DP-03, DP-09). No column is added for a visit or a document: neither has a source in this schema (ASM-5491, ASM-5493).

**Configuration and reference data.**

- LOV-INSTR-STATUS, LOV-INSTRUCTION, LOV-PANEL, LOV-PARTNER-TYPE and LOV-ROLE at their version; the result vocabulary has no list and carries the placeholder (ASM-5494).
- The rule ID and the version in force: read through the rwb-decision contract; no partner route set exists, so the value carries the placeholder (ASM-5496).
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard of the template.
- The upload media types, the size limits and the per-submission file count are Not specified in the source documents (GAP-3135; ASM-5501).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The field-work branch of `InstructionWorkflow` and its signal, registered on `rwb-partner`, with the client's submission as its trigger.
2. `FieldWorkScope` and `InstructionStateGuard` against their fakes, with the other-firm and closed-instruction paths (X2, X3).
3. `RuleVersionClient` against its fake, with the missing-version path (X8).
4. `FieldWorkDecisionRecordWriter` against the stub, with the failed-write path (AC2, X1).
5. `DocumentClient` and `InteractionLedgerClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (X5).
6. `PartnerInstructionController` with the multipart limits, right U, the scope, the `Idempotency-Key`, the 415 and 422 mapping, and `FieldWork` through the partner gateway fake (X4, X6).
7. The transaction step: the record, the row, the outbox row and the key in one commit, with the optimistic-lock version.
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no write to `rwb_document`, `rwb_source_data`, `rwb_case` or any other schema, and no `document` or `interaction` row (X7).

**Feature flag.** `rwb.partner.fieldwork-v1`, a flag of the platform library; off means the operation answers 503 with no write and PRT-02 hides the field-work action, and the portal result intake of RWB-S9-E6033-APP is unaffected.

**Done when.** The tests of section 16 pass, a synthetic collector of one firm submits a visit with two photographs and one bill in SIT, the result and `DONE` are recorded with the rule version, the references come back, the event is published, a closed instruction and another firm's instruction are refused, a repeat on reconnect writes once, a forced record failure changes nothing, and no `document`, `interaction`, `recovery_case` row and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required part is absent or invalid, or a required value is not in force (X4, X8) | Enter {field}. |
| MSG-P4-002 | A role without partner portal right U calls the submission (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the result is recorded (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| the refusal of X3 | The instruction is `DONE`, `DECLINED` or `RECALLED` | Not specified in the source documents (GAP-3135; ASM-5500) |

The three IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. The refusal of a closed instruction has no message in any source, so it carries the placeholder and no invented text.

### 15. Screens and states

SCR-35 Placement and allocation is a staff screen served through the gateway-bff composite route (DP-19): the route calls this service for the firm, its panel status and its score, and rwb-case for the case and its stage, and this story fixes the rwb-partner answer only. PRT-02 Instruction is the partner's own screen, reached through the partner gateway of the DMZ (FAPI 2.0) on the caller's firm scope, and the field app is a client of that gateway.

The legacy screen table gives SCR-35 "Loading; list" and PRT-02 "New; accepted; in progress; result; closed". PRT-02 is therefore the instruction screen with a result state, and this story produces it: the collector sees the instruction, its case reference, its type and its due date in the `New`, `accepted` and `in progress` states, and after a successful submission the `result` state with its result code and its document references. The offline state (queued, unsent) and the states of a rejected upload, a closed instruction and a missing right read the messages of section 14. No source describes the field-app form, its field list, its offline indicator or the words of the `result` and `closed` states, so those carry the placeholder (GAP-3135; ASM-5497, ASM-5501). PRT-01, PRT-03 and PRT-04 belong to the instruction, result and invoice stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-018-01 | AC1 | Component | The collector `partner_user` of `PRT-0007` and the open instruction `INS-000318`, the ledger, document and rule fakes; the result code, `DONE`, the record, the document references and the event asserted |
| TC-E7-018-02 | AC2 | Component | The decision-record stub stopped; nothing written, no document claimed, no ledger entry and MSG-P7-003 shown |
| TC-E7-018-03 | Access | Component | A role without partner portal right U, and an instruction of another firm; 403 with MSG-P4-002 and 404 with nothing read |
| TC-E7-018-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; the instruction is unchanged and no record, document claim or ledger entry exists |

The four legacy cases are those of RWB-E7-018 in their legacy order, with the Level column added: every case runs on the fakes, so every case is `Component`. TC-E7-018-01 exercises the field-work step this story builds and TC-E7-018-04 the record-first rule of DP-03. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story and the key has no ITG slice.

### 17. Guardrails

- No business value in code: the instruction, panel, partner type and role lists, the result vocabulary, the rule ID and its version stay reference data, lists and rule values with a version, never a constant, a default or a branch.
- No personal data in `rwb_partner`, a workflow input, an event or a log: partner identifiers, codes, dates, a count of documents, a rule ID and a version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table.
- The visit stays with rwb-source-data: no `interaction` row, no ledger update and no channel value of the code (BR4).
- The evidence stays with rwb-document: no document content, type, index entry or retention is stored here, and the upload is a claim-check claim (BR5).
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here; the case is told by EV-21.
- The rule rows and the central ledger stay with rwb-decision: no rule row, package or rule ID set is added to this service.
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base and no Schedule.
- The record is written before the row; a build that answers outside the record's transaction fails the review (DP-03).
- Offline capture never weakens the record: the client may resend, the service answers once (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S9-009 | Field work and its evidence reach the case through the field application (Should, E7) | The result operation, the visit entry, the document claims, the record and EV-21 | TC-E7-018-01, TC-E7-018-02 |
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents (Should, E2) | The rwb-document claim-check intake of the photographs and the bills | TC-E7-018-01, TC-E7-018-04 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email | The partner gateway access of the submission and the firm scope | TC-E7-018-03 |
| NFR-062 | The field application captures evidence with no network connection and uploads when it reconnects | The client's queue and the idempotent repeat of the submission | TC-E7-018-01 |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the instruction and its result | TC-E7-018-01 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E7-018-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | EV-21 on `rwb.partner.events.v1` through the outbox | TC-E7-018-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-E7-018-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the row | TC-E7-018-02, TC-E7-018-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-018, disposition Split (rework); feature FEAT-PRM-15 |
| Legacy criteria | AC1 and AC2, both owned word for word by this story; the key has no ITG slice in the plan |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged from the plan; EP07 is wave 4 and the service's Arch v5 wave is 4, so the W-MAP wave is not earlier and no conflict is raised (ASM-5499) |
| Source text | Legacy RWB-E7-018; FSD S9 Partner management v3 A1.3, A2.15, A2.15.2, A2.15.3.1 to A2.15.3.3, A2.15.4 and the Screens and Requirements served tables; TSD S9 Partner management v2 T1, T2, T3.0, T3.1, T3.2, T3.3, T4, T5.1, T5.2, T5.3, T6.1, T6.2 and T-A; Business Rules and Routing Logic v4 rows R-UNI-38 to R-UNI-40; LDM v8 `partner_user`, `interaction`, LOV-CHANNEL, LOV-CONTACT-SRC and LOV-ROLE; Event and Messaging Design v5 event EV-21; Program BRD v4 rows REQ-S9-009, REQ-DCM-013 and NFR-062 |
| Test cases | TC-E7-018-01 to TC-E7-018-04 |
| Feature and screens | FEAT-PRM-15, SCR-35 Placement and allocation and PRT-02 Instruction |
| Rules | No partner route set exists; R-UNI-38 to R-UNI-40 are the nearest rows, and the rule ID and the version in force carry the placeholder (ASM-5496) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the field-work element, the lists, the rights of the document, the error envelope, the event shape and the fakes: RWB-S9-E7018-CON.
- The portal result intake of the same operation: FEAT-PRM-05 (RWB-S9-E6033-APP), whose baseline this story narrows nothing of.
- Issuing, accepting and declining an instruction, and the override of an allocation: RWB-S9-E6031-APP, RWB-S9-E6032-APP and RWB-S9-E6034-APP.
- The document hub, its types, its index, its retention and its OCR: rwb-document (P5), whose intake this story consumes.
- The interaction ledger, its channel list, its source list and its deduplication: rwb-source-data (P1), whose ledger this story writes one entry into through its contract.
- The case of record, its stage and its clock: rwb-case (P3). The central `decision_log_entry` ledger, the rule rows and the rule packages: rwb-decision (P7).
- The fee of the field work, the invoice and the partner fee approval: FEAT-PRM-07 and FEAT-PRM-09 (RWB-S9-E6035-APP, RWB-S9-E7012-APP).
- The scorecard, the panel as reference data and the partner review: RWB-S9-E7011-APP, RWB-S9-E6030 and RWB-S9-E7013-APP.
- Ending the contract and the recall that closes an instruction: RWB-S9-E7015-APP. The conduct breach: RWB-S9-E7016-APP.
- The gateway-bff composite route, the partner gateway and the screen field lists of SCR-35 and PRT-02: RWB-PLT-N001-CON, RWB-PLT-EDGE and the edge stories.
- The offline behaviour and the devices of the field application, and their non-functional targets: the field application's own stories, with NFR-062 and NFR-063 at Proposed under DL11 (GAP-3135; ASM-5501).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
