# RWB-P6-E1052-APP Notice generation v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1052-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1046-APP |
| Depends on (build) | RWB-P6-E1052-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P6-E1046-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P1-E1015-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-003, FR-P6-005, FR-P6-006, FR-P6-007, FR-P6-008, FR-P6-009, FR-P6-010, FR-P6-011, FR-P6-012, FR-P6-013, FR-P6-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-052 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E1052-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **a demand, recall or guarantor notice generated inside rwb-comms from the Legal-approved template, with the case facts merged from the contract of the service that owns each fact, the footer carrying the case number, template code, template version and generation date, the PDF stored write-once on the case and the decision recorded locally**, so that **letters are produced without re-keying, the address and the amount on the notice are the ones ACE holds, and every notice carries a decision record**.

### 2. Business rationale

Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. Under D-RCV-35 the Workbench holds no party and no contact point: the name comes from the customer record by `person_key`, the notice address and phone from the contact record by the composite `contact_key` (`contact_type:key`), and the outstanding from the account record by `account_key`. The clear identity number never leaves ACE, so it is never merged. The legacy story merges those values into the current approved template, stores the PDF write-once on the case with the template version in the footer and records the decision. It serves REQ-OCC-001 and control CTL-14, and is the input to dispatch and proof of delivery, where the WIN record is read from the ACE proof-of-delivery view. The FSD P6 measure "notices with proof of delivery, 100 percent" depends on it.

This story is the rwb-comms part of legacy RWB-E1-052 and it changes who owns each fact, not what the notice says. `notice`, `template` and `merge_field` are written only in schema `rwb_comms` by this service (DP-01). The case, the parties, the party roles and the "Complete notice data" task belong to rwb-case; the customer, the contact point, the account balance, the freshness stamp and the delivery facts belong to rwb-source-data, which is the only reader of the ACE views; the generated PDF belongs to rwb-document; the central decision ledger belongs to rwb-decision. Every one of those is a contract call on the owner's base with one hop and a 2 s budget (DP-05, DP-11, DP-13), and the screens reach the answer through gateway-bff (DP-19).

The notices move to the service's own base `/api/recovery/comms/v1` with `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}`, the two operations of API-P6-001 and API-P6-002 (DP-13). Every generated notice writes one row in the local decision record in the same transaction as the notice row and the outbox row, publishes `DecisionRecorded` on the shared topic `rwb.decision-record.v1` through the local decision-record library (DP-03), and publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` (DP-09) with IDs only. The event carries no name, no address and no account number, and the merge snapshot carries the merge code, the source column, the business key and the field ID of each value and never the value.

The split of the legacy key is recorded in section 19: the ITG slice RWB-ITG-E1052-ITG keeps legacy AC7 and proves the journey end to end, dispatch and proof of delivery belong to RWB-P6-E1055-APP and RWB-P6-E2021-APP, SMS and LINE to RWB-P6-E2022-APP, and the template catalog this story reads to RWB-P6-E1046-APP.

### 3. Preconditions

- RWB-P6-E1052-CON is published: the request and answer shapes of API-P6-001 and API-P6-002, the notice fields, the state values, the error envelope, the `Idempotency-Key` rule and the two event envelopes (DP-11).
- RWB-P6-E1046-APP is done: `template` and `merge_field` carry the current Approved version per template code, language and product group, and `merge_field.is_required` is in force.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1043-CON is published: the client library of the reference-data contract, so LOV-NOTICE, LOV-SENT-TYPE and LOV-PRODUCT are read and none is written in code (DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library and the CloudEvents envelope (DP-09).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence, so this story's migration runs in `rwb_comms` and in no other schema (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff route on which SCR-01, SCR-18 and SCR-30 reach the two notice operations (DP-19).
- RWB-P3-E1018-CON is published: the case summary, the case parties and the party roles, and the operation that raises a task on the case.
- RWB-P3-E1043-CON is published: the reference-data read for LOV-NOTICE, LOV-SENT-TYPE and LOV-PRODUCT.
- RWB-P1-E1015-CON is published: the data-product contract that serves the customer, the contact point, the account balance and its `data_as_of`, the freshness stamp and the proof-of-delivery facts. The exact field names behind that contract are Not specified in the source documents (GAP-1080; ASM-2028).
- RWB-P7-E1027-CON is published: the central ledger read of the decision log, used to read back a D7.1 entry.
- The rwb-document contract is used for the write-once PDF and returns a document ID with `source` "GENERATED" and `write_once` true; it has no contract dependency row in this story, so it is built against its published document as a contract fake (GAP-1079; ASM-2027).
- No `document` row, `recovery_case` row, `task` row or `decision_log_entry` row is read or written directly: each arrives or leaves through its owner's contract (DP-01).
- The login is the rwb-comms login (DP-02). The per-service login name is not given by any source read here and is carried as a gap of the platform database story.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. Caller: `POST /api/recovery/comms/v1/cases/{caseId}/notices` with the case ID, the notice type, `person_key`, the language, the business date and an `Idempotency-Key` (API-P6-001).
2. rwb-comms: reads the case summary — case number, product group, status and owner — and the case parties with their roles, through the rwb-case contract, and refuses a `person_key` that is not a party on the case.
3. rwb-comms: checks the `Idempotency-Key` against `idempotency_key`; a key already answered is replayed from the stored answer and no second notice is written.
4. rwb-comms: asks its own `template` catalog for the current Approved LETTER version for the notice type, product group and language on the business date. No Approved version is a refusal with MSG-P6-005 and nothing is stored; a Withdrawn current version is a hold with `hold_reason` "TEMPLATE_WITHDRAWN" and a task to the litigation officer team with MSG-P6-003.
5. rwb-comms: resolves each merge code through the owner of its source: `CASE_NO`, `PRODUCT_GROUP` and `ENTRY_DATE` through rwb-case; `CUSTOMER_NAME`, `POSTAL_ADDRESS` and `PHONE` through rwb-source-data; `TOTAL_OUTSTANDING` through rwb-source-data by the case's primary `account_key`. Each value carries the ACE business date of its data product.
6. rwb-comms: a required merge value that is empty holds the notice with `hold_reason` naming the merge code, stores no document and raises the task "Complete notice data" to the case owner through rwb-case with MSG-P6-007.
7. rwb-comms: writes the local D7.1 decision record — rule "R-LIT-03", template code and version, data date and the merge snapshot reference — in the same transaction as the notice row and the outbox row. A failed write returns 503 with MSG-P7-003 and raises an incident under R-UNI-39, and nothing is stored.
8. rwb-comms: renders the approved template body to PDF and adds the footer: case number, template code, template version and generation date.
9. rwb-comms: stores the PDF through the rwb-document contract as a generated, write-once document on the case and receives the document ID. A store that exceeds 2 s or fails rolls the notice back (R-UNI-24).
10. rwb-comms: writes the `notice` row with `person_key`, `template_id`, notice type, sent type and state Generated, and the `NoticeGenerated` row in the outbox in the same transaction.
11. Outbox relay: publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` keyed by caseId with IDs only, and the local decision-record library publishes `DecisionRecorded` on `rwb.decision-record.v1`.
12. `GET /api/recovery/comms/v1/notices/{noticeId}` returns the notice with its state, hold reason, template version, document ID and the delivery facts read through rwb-source-data by `notice_ref`. The notice row is never changed by the read, and the Workbench writes no WIN delivery fact of its own.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The template has no Approved version | Refused; no notice row and no document created | MSG-P6-005 | AC2 |
| X2 | A required merge value is empty, for example no ADDRESS row in the contact record for the person | Notice held with the field named in `hold_reason`; task to the case owner | MSG-P6-007 | AC3 |
| X3 | The current version is withdrawn | Notice held; task to the litigation officer team | MSG-P6-003 | AC4 |
| X4 | The local decision record cannot be written | Nothing stored; incident raised; no document and no event | MSG-P7-003 | AC5 |
| X5 | The same request arrives twice on one business date with the same `Idempotency-Key`, or with the same case, notice type, `person_key` and business date | The first notice is returned; no second notice and no second document | None | AC6 |
| X6 | The ACE account batch is stale | Generation proceeds with the ACE business date shown; the decision record carries that date | MSG-P1-001 | AC7, held by RWB-ITG-E1052-ITG |
| X7 | The person is not on the case | Refused; no notice row and no document | MSG-P4-003 | AC8 |
| X8 | The proof-of-delivery source holds no row for the notice reference | The notice shows as generated with no delivery confirmation; the delivery matcher of RWB-E1-055 lists it; the notice row is unchanged | None | TC-E1-052-11, AC9 |
| X9 | A consumed call does not answer inside 2 s | The generation is not taken from a partial answer: no notice is written on a missing required value, the caller is told the system is unavailable and the request is retried under the `Idempotency-Key` | MSG-GEN-006 | AC3, AC8 |
| X10 | The document store returns a failure after the record write | The notice row and the outbox row roll back; a correcting decision record follows under R-UNI-24; no orphan document is left | MSG-P7-003 for the incident path only | TC-E1-052-10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E1052-CON and the five contract fakes; the case, reference-data, source-data, decision and document answers are stubbed, and rwb-case and rwb-source-data are not touched in code |
| Negotiable | Which notice types, templates, merge codes and product groups exist is data; the merge order, the checks, the footer and the two hold paths are fixed |
| Valuable | Ends re-keying of demand, recall and guarantor notices, and the address and the amount on the notice are the ones ACE holds |
| Estimable | One service, one renderer, two operations, five consumed contracts, one local decision record and one event |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a component test with synthetic cases, templates and contract fakes, and each cross-service answer has a named fake |

### 7. Acceptance criteria

```gherkin
Feature: Notice generation v1

  Background:
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RW-2026-000123" has product group "MORTGAGE" and borrower person_key "P-0001"
    Given v_ace_account holds the case's primary account_key with total_balance 1,250,000.00 and data_as_of 2026-11-25
    Given the rwb-source-data contract mock returns the case's primary account_key with total_balance 1,250,000.00 and data_as_of 2026-11-25 on data product "DP01" Account and arrears
    Given the rwb-case contract mock returns case "RW-2026-000123" with case number "RW-2026-000123" and product group "MORTGAGE"
    Given the business date is 2026-11-25

  Scenario: AC1 Generated (legacy RWB-E1-052 AC1)
    Given v_ace_customer holds person_key "P-0001" with first_name "Anan" and last_name "Sukjai"
    Given the rwb-source-data contract mock returns person_key "P-0001" with first_name "Anan" and last_name "Sukjai" on data product "DP01" Account and arrears
    Given v_ace_contact holds an ADDRESS row for "P-0001" with contact_key "ADDRESS:A-9001" and contact_value "88/1 Bangkok"
    Given the rwb-source-data contract mock returns an ADDRESS row for "P-0001" with contact_key "ADDRESS:A-9001" and contact_value "88/1 Bangkok"
    Given the rwb-case contract mock returns person_key "P-0001" as the borrower party role on case "RW-2026-000123"
    Given the rwb-document contract mock returns the stored document with source "GENERATED" and write_once true
    Given the rwb-decision contract mock returns one D7.1 entry with rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND", person_key "P-0001" and language "TH"
    Then the system stores a PDF on the case with source "GENERATED" and write_once true
    Then the PDF shows "RW-2026-000123", the customer name and 1,250,000.00 THB
    Then the footer reads "RW-2026-000123 DEMAND-MTG v2 2026-11-25"
    Then a notice row exists with notice_type "DEMAND", sent_type "NPL", person_key "P-0001", template_id and state "Generated"
    Then one decision log entry exists with decision code "D7.1", rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference
    Then the system writes noticeGenerated to the outbox with the notice ID and template version 2

  Scenario: AC2 Template approval checked (legacy RWB-E1-052 AC2)
    Given template "RECALL-HP" "TH" has only version 1 in state "Draft"
    Given case "RW-2026-000456" has product group "HIRE_PURCHASE"
    Given the rwb-case contract mock returns case "RW-2026-000456" with product group "HIRE_PURCHASE"
    When NoticeApi.generate is called for case "RW-2026-000456", notice type "RECALL" and language "TH"
    Then the system refuses it with MSG-P6-005 naming "RECALL-HP" version 1
    Then no notice row and no document are created

  Scenario: AC3 Missing field (legacy RWB-E1-052 AC3)
    Given v_ace_contact holds no ADDRESS row for person_key "P-0001"
    Given the rwb-source-data contract mock returns no ADDRESS row for person_key "P-0001"
    Given the rwb-case contract mock returns the case owner of "RW-2026-000123" and accepts the task "Complete notice data" with MSG-P6-007 naming "POSTAL_ADDRESS"
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND" and person_key "P-0001"
    Then a notice row exists in state "Held" with hold_reason "POSTAL_ADDRESS"
    Then the system stores no document
    Then the system raises a task "Complete notice data" to the case owner of "RW-2026-000123" with MSG-P6-007 naming "POSTAL_ADDRESS"

  Scenario: AC4 Withdrawn template holds the notice (legacy RWB-E1-052 AC4)
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    Given the rwb-case contract mock accepts the task raised to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG"
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then a notice row exists in state "Held" with hold_reason "TEMPLATE_WITHDRAWN"
    Then the system raises a task to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC5 Decision log write fails (legacy RWB-E1-052 AC5)
    Given the decision log store is unavailable
    Given the rwb-decision contract mock returns the central ledger read, and the local decision-record library is forced to fail for the next write
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then the call fails with MSG-P7-003
    Then no notice row and no document are created
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC6 Repeated request on the same business date (legacy RWB-E1-052 AC6)
    Given a notice for case "RW-2026-000123", notice type "DEMAND", person_key "P-0001" was generated on 2026-11-25
    When NoticeApi.generate is called again with the same values on 2026-11-25
    Then the system returns the existing notice
    Then the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC8 Person not on the case (legacy RWB-E1-052 AC8)
    Given person_key "P-0999" is not a party on case "RW-2026-000123"
    Given the rwb-case contract mock returns the parties of "RW-2026-000123" without person_key "P-0999"
    When NoticeApi.generate is called with person_key "P-0999"
    Then the system refuses it with MSG-P4-003

  Scenario: AC9 Proof of delivery read from ACE (legacy RWB-E1-052 AC9)
    Given notice "N-0001" on case "RW-2026-000123" has notice_ref "WIN-77001"
    Given v_ace_pod holds pod_key "POD-0001" with notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED"
    Given the rwb-source-data contract mock returns pod_key "POD-0001" with notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED" on data product "DP07" Legal
    When an officer reads notice "N-0001" through GET /cases/{caseId}/notices
    Then the notice shows sent date 2026-11-27, barcode "RR123456789TH" and status "DELIVERED" from v_ace_pod
    Then the notice row is unchanged
```

The eight criteria above are the legacy criteria this story owns, copied word for word from RWB-E1-052 section 7 and tagged with their origin. Legacy AC7 belongs to RWB-ITG-E1052-ITG and is not copied here. Each `v_ace_*` Given line stands as the value fixture of the legacy story and is kept unchanged; the `contract mock` line beside it names the contract through which the target service reads the same value, so the assertion is unchanged and the reader moves from the view to its owner (DP-05). AC9's legacy When line reads the notice through `GET /cases/{caseId}/notices`; in the target that read is `GET /api/recovery/comms/v1/notices/{noticeId}` of API-P6-002, and the legacy line and its values are kept as written.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A notice is generated only from the current Approved template for its notice type, product group and language | RWB-E1-052 BR1; R-LIT-03; CTL-14 |
| BR2 | A withdrawn template holds generation and raises a task to the litigation officer team | RWB-E1-052 BR2; R-LIT-04 |
| BR3 | A required merge value that is empty holds the notice, names the field and raises a task to the case owner | RWB-E1-052 BR3; merge_field.is_required; pattern of R-RES-36 |
| BR4 | The footer carries the case number, template code, template version and generation date | RWB-E1-052 BR4; REQ-OCC-001; CTL-14 evidence |
| BR5 | The generated PDF is a write-once document on the case, held by rwb-document | RWB-E1-052 BR5; CTL-12; DT06 |
| BR6 | A notice whose local decision record cannot be written is not generated; the record, the notice row and the outbox row commit together or not at all | RWB-E1-052 BR6; Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR7 | Sent type is NPL for a case at 90 days past due or more; the mapping is reference data | RWB-E1-052 BR7; LOV-SENT-TYPE; DL16 |
| BR8 | One notice per case, notice type, `person_key` and business date | RWB-E1-052 BR8; R-UNI-40; notice key of the service |
| BR9 | The party, the customer name and the notice address are read by `person_key` and the composite `contact_key` (`contact_type:key`) through rwb-source-data; no service holds a party or contact copy and no service reads an ACE view except rwb-source-data | RWB-E1-052 BR9; D-RCV-35 U4; ADR-010; DP-01; DP-05 |
| BR10 | A merge code resolves to a case field, a source-data field or a template field. The clear `identification_number` is never a merge source; `id_no_masked` and `id_no_last4` only | RWB-E1-052 BR10; ADR-010; DF-ACE-073 |
| BR11 | Proof of delivery is read through rwb-source-data by `notice_ref`; the Workbench writes no WIN delivery fact | RWB-E1-052 BR11; RWB-E1-055; DP-05 |
| BR12 | The merge snapshot holds the merge code, the source column, the business key and the field ID of each value used, never the value | RWB-E1-052 BR12; NFR-040; guardrail on personal data |
| BR13 | The litigation route rule decides when a notice is asked for; this story answers a request and evaluates no route rule, so R-LIT-01 stays with rwb-decision | R-LIT-01; RWB-E1-052 section 19 |
| BR14 | A document store that fails after the record write rolls the notice back and a correcting decision record follows | R-UNI-24; RWB-E1-052 section 12 (order of writes) |
| BR15 | The notice rule set is R-LIT-03 for generation and R-LIT-04 for a withdrawn template; a variant of either is a new rule version in rwb-decision, never a code change | R-LIT-03; R-LIT-04; DP-01 |

### 9. State transitions

None. This story does not change a case status. It sets the notice state (standard column `state`), and the template check runs before any state is written:

| From | Event | Condition | To |
|---|---|---|---|
| None | Generate through POST /cases/{caseId}/notices | The current template version is Approved and every required merge value is present | Generated |
| None | Generate | A required merge value is empty, for example POSTAL_ADDRESS | Held, hold_reason "POSTAL_ADDRESS" |
| None | Generate | The current template version is Withdrawn and no later version is Approved | Held, hold_reason "TEMPLATE_WITHDRAWN" |
| None | Generate | The template has no Approved version at all | No row; the call is refused with MSG-P6-005 |
| Held | Generate | The missing value arrives or a new version is Approved | Generated, in a new request |
| Generated | Dispatch through WIN, owned by RWB-P6-E2021-APP | The notice is written to the WIN file | Sent |
| Sent | Proof of delivery read, owned by RWB-P6-E2021-APP | The delivery status is DELIVERED | Delivered |
| Sent | Proof of delivery read, owned by RWB-P6-E2021-APP | The delivery status is UNDELIVERABLE or REFUSED | Unserved |
| Any | A read of the notice | Never | The same state; a read changes no row |

The template check is part of generation and not a state of its own: it decides between Generated, the two hold reasons and the MSG-P6-005 refusal before any row is written. The state `APPROVED` of the legacy check constraint belongs to the notice approval story RWB-E2-014 and is not set here. `Sent`, `Delivered` and `Unserved` are set by the dispatch and proof-of-delivery stories; this story only reads and returns the state it finds.

### 10. Authority

The letters below are taken from the rwb-comms RBAC matrix of the module specification and from no other table.

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity (the rwb-comms login, DP-02) | Serves the two notice operations, reads the five contracts, writes `rwb_comms` only |
| RW-LITOFF, litigation officer | Documents CRU and Litigation CRUA: reads the notice and the document for a case in scope, and requests generation; receives the withdrawn-template task |
| RW-LEGAL, Legal counsel | Documents CRUA and Litigation RA: reads the notice; approves the template version this story reads |
| RW-CASEOWN, case owner | Documents CRU and Litigation R: reads the notice and receives the "Complete notice data" task |
| RW-TEAMMGR, team manager | Documents R and Litigation R: reads the notice for a case in scope |
| RW-PLATADM, platform administrator | Documents R only: reads the notice for a case in scope; no Litigation right, so the notice read is not granted by the matrix and is refused at the edge |

No delegation-of-authority level applies to notice generation: the two rights that matter are the Documents right and the Litigation right, and the authorisation itself is enforced at gateway-bff and not in this story (GAP-1083; ASM-2031). No role in this story grants itself a right.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6 rwb_comms) | id | Write |
| DF-LEG-016 | notice (P6 rwb_comms) | case_id | Write |
| DF-LEG-017 | notice (P6 rwb_comms) | document_id | Write |
| DF-LEG-018 | notice (P6 rwb_comms) | notice_type | Write |
| DF-LEG-019 | notice (P6 rwb_comms) | sent_date | Read, from the delivery facts |
| DF-LEG-020 | notice (P6 rwb_comms) | barcode | Read, from the delivery facts |
| DF-LEG-021 | notice (P6 rwb_comms) | callback_date | Read, from the delivery facts |
| DF-LEG-022 | notice (P6 rwb_comms) | delivery_status | Read, from the delivery facts |
| DF-LEG-023 | notice (P6 rwb_comms) | sent_type | Write |
| DF-LEG-030 | notice (P6 rwb_comms) | person_key | Write; the TSD names this field party_id, and the conflict is carried in the gap register (GAP-1084; ASM-2032) |
| DF-LEG-031 | notice (P6 rwb_comms) | template_id | Write |
| DF-LEG-032 | notice (P6 rwb_comms) | hold_reason | Write |
| DF-LEG-033 | notice (P6 rwb_comms) | dispatch_file_id | Not written here; the dispatch story writes it |
| DF-LEG-034 | notice (P6 rwb_comms) | dispatch_attempts | Write the initial value; the dispatch story increments it |
| Standard column | notice (P6 rwb_comms) | state | Write |
| DF-REF-045 | template (P6 rwb_comms) | id | Read |
| DF-REF-046 | template (P6 rwb_comms) | template_code | Read |
| DF-REF-047 | template (P6 rwb_comms) | template_version | Read |
| DF-REF-048 | template (P6 rwb_comms) | language | Read |
| DF-REF-049 | template (P6 rwb_comms) | product_group | Read |
| DF-REF-050 | template (P6 rwb_comms) | body_ref | Read |
| DF-REF-051 | template (P6 rwb_comms) | approved_by_legal | Read |
| DF-REF-063 | template (P6 rwb_comms) | approved_by | Read |
| DF-REF-064 | template (P6 rwb_comms) | approved_at | Read |
| DF-REF-065 | template (P6 rwb_comms) | valid_from | Read |
| DF-REF-066 | template (P6 rwb_comms) | channel | Read |
| DF-REF-067 | template (P6 rwb_comms) | notice_type | Read |
| DF-REF-068 | template (P6 rwb_comms) | signature_basis | Read |
| DF-REF-069 | template (P6 rwb_comms) | merge_codes | Read |
| DF-REF-252 | merge_field (P6 rwb_comms) | id | Read |
| DF-REF-253 | merge_field (P6 rwb_comms) | merge_code | Read |
| DF-REF-254 | merge_field (P6 rwb_comms) | source_entity | Read |
| DF-REF-255 | merge_field (P6 rwb_comms) | source_field | Read |
| DF-REF-256 | merge_field (P6 rwb_comms) | field_id | Read |
| DF-REF-257 | merge_field (P6 rwb_comms) | is_required | Read |
| DF-REF-258 | merge_field (P6 rwb_comms) | personal_data | Read |
| DF-REF-259 | merge_field (P6 rwb_comms) | catalog_version | Read |
| DF-REF-260 | merge_field (P6 rwb_comms) | valid_from | Read |
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-009 | recovery_case (P3 rwb-case) | id, case_no, product_group, owner_user_id | Read through the P3 contract |
| DF-CAS-031, DF-CAS-032, DF-CAS-033 | case_party (P3 rwb-case) | case_id, person_key, party_role | Read through the P3 contract |
| DF-WRK-019, DF-WRK-023 | task (P3 rwb-case) | task_code, owner_role | Written through the P3 contract |
| DF-ACE-056, DF-ACE-057, DF-ACE-058, DF-ACE-075, DF-ACE-076, DF-ACE-077, DF-ACE-078, DF-ACE-081, DF-ACE-082, DF-ACE-083, DF-ACE-001, DF-ACE-020, DF-ACE-036, DF-ACE-251, DF-ACE-253, DF-ACE-254, DF-ACE-255, DF-ACE-256, DF-ACE-257 | the data products of P1 rwb-source-data, over the ACE views | person_key, first_name, last_name, contact_type, contact_key, contact_value, city, post_code, country, account_key, total_balance, data_as_of, pod_key, notice_ref, sent_date, barcode, callback_date, delivery_status | Read through the P1 data-product contract; never read from a view here (DP-05) |
| DF-DOC-001 to DF-DOC-011 | document (P5 rwb-document) | all fields, with `source` "GENERATED" and `write_once` true | Written through the P5 contract; no field copied into `rwb_comms` |
| DF-DEC-001 to DF-DEC-018 | local decision record (P6 rows in `rwb_comms`, written through the decision-record library) | decision code D7.1, rule, template code and version, data date and the merge snapshot reference | Write |

The merge snapshot is an artefact of this service and not one of its three business tables: no source read here names the table or the store it lives in, so the reference is carried on the decision record and the location is a gap (GAP-1081; ASM-2029). Its content is fixed by BR12: merge code, source column, business key and field ID, never the value. No `document`, `recovery_case`, `task`, `timer`, `interaction`, `signature_request` or `decision_log_entry` row is read or written directly. The schema is `rwb_comms`, its migration runs in the per-service Flyway sequence (DP-15), and the service holds no foreign key into another schema (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`; naming per the service catalog.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P6-001 | POST | `/cases/{caseId}/notices` | Generate a notice from the approved template for a case, notice type, `person_key`, language and business date; answer 201 with the Notice | Litigation, right C, scope applied | `Idempotency-Key` header |
| API-P6-002 | GET | `/notices/{noticeId}` | Read one notice with its state, hold reason, template version, document ID and its dispatch and proof-of-delivery facts; answer 200 with the Notice | Litigation, right R, scope applied | Not applicable |

Errors for API-P6-001: 401, 403, 404, 409, 422, 503. Errors for API-P6-002: 401, 403, 404, 503. The request and answer shapes, the field list of the Notice resource and the error codes are fixed by RWB-P6-E1052-CON; the response field names are Not specified in the source documents beyond the type name (GAP-1082; ASM-2030).

#### 12.2 REST operations consumed

Every row is one hop on the owner's base with a 2 s timeout, a breaker per downstream, a single GET retry with jitter and a POST retried only with the same `Idempotency-Key` (DP-11, ADR-020).

| Method and path | Owner | Use in this story |
|---|---|---|
| GET `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The customer name, the contact address and phone, the account balance and `data_as_of`, and the proof-of-delivery facts, for DP01 Account and arrears and DP07 Legal; contract RWB-P1-E1015-CON |
| GET `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The data date and freshness stamp of each data product the notice merges, carried onto the decision record |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number, product group, status and owner; contract RWB-P3-E1018-CON |
| GET `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | The party links and roles, and the AC8 check that `person_key` is a party on the case; contract RWB-P3-E1018-CON |
| POST `/api/recovery/case/v1/cases/{caseId}/tasks` | P3 rwb-case | Raise "Complete notice data" to the case owner and the withdrawn-template task to the litigation officer team; the raise path is Not specified in the source documents as an operation of the Ownership Map (GAP-1085; ASM-2033) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE, LOV-SENT-TYPE and LOV-PRODUCT, so no notice type or sent type is written in code; contract RWB-P3-E1043-CON |
| GET `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Read back the D7.1 entry of a notice in the component tests and on the failure path; the write itself is local (DP-03) |
| POST `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | Store the rendered PDF write-once on the case and receive the document ID with `source` "GENERATED" and `write_once` true; no contract dependency row exists for P5 (GAP-1079; ASM-2027) |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Schema element (IDs and facts only) |
|---|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` (EV-13) | `rwb.comms.events.v1` | P6 rwb-comms | caseId | noticeId, caseId, templateId, templateVersion, noticeType, generatedAt; one event for every stored notice, written to the outbox in the same transaction as the notice row |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision code D7.1, rule "R-LIT-03", rule version, template code and version, data date, record reference; published by the local decision-record library (DP-03) |

`generatedAt` is the outbox write time of the notice; the element list of the event is not enumerated beyond the legacy payload, so the field is carried with the placeholder of GAP-1082 and ASM-2030. The event carries no name, no address, no account number and no account key, and no notice body.

#### 12.4 Events consumed

| Event | Topic | Owner | Declared shape | Handler in this story |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, fromState, toState, changedAt | None for generation; declared so the hold rules of the later stories have one owner for the case state |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, raisedAt, contactStop | None here; the contact-stop and conduct rules are applied before an outbound contact in RWB-P6-E2021-APP and RWB-P6-E2022-APP |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, clearedAt, outcome | None here, as above |

The three rows are declared for the hold rules this capability depends on; this story subscribes to none of them and each is consumed inside rwb-comms by the dispatch stories. The inbox table is in place so those stories consume idempotently (DP-09).

#### 12.5 Workflows and activities

None. Generation is synchronous inside rwb-comms: the POST answers with the notice and its document reference. No workflow, activity or Nexus operation is started here, and no workflow input carries a personal value. `NoticeDispatchWorkflow` exists in the service (Architecture v5 slide 17) and belongs to the dispatch loop, which is RWB-P6-E2021-APP; its contract reference is fixed there and not here.

#### 12.6 Schedules

None. JOB-10 WIN notices at 16:00 is the dispatch job and belongs to RWB-P6-E2021-APP and rwb-integration (Architecture v5 slide 44). This story registers no Schedule, no cron entry and no job name, and reads no shared scheduler table (DP-10).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The notice row: case, document, notice type, sent type, `person_key`, template, hold reason and state |
| template | P6 (rwb_comms) | The template catalog this story reads; written by RWB-P6-E1046-APP |
| merge_field | P6 (rwb_comms) | The merge code catalog and `is_required`; written by RWB-P6-E1046-APP |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox of the two published events, the inbox of the three declared events and the `Idempotency-Key` answer store (DP-09) |
| local decision record | P6 rows in `rwb_comms`, written through the decision-record library | The D7.1 entry of every notice (DP-03) |

Not owned and never read directly: `document` and `signature_request` (P5 rwb-document), `interaction` (P1 rwb-source-data), `recovery_case`, `case_party`, `task` and `timer` (P3 rwb-case), `decision_log_entry` (P7 rwb-decision).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers |
|---|---|---|
| rwb-source-data WireMock | RWB-P1-E1015-CON | DP01 Account and arrears for case "RW-2026-000123" with person_key "P-0001", first_name "Anan", last_name "Sukjai", the ADDRESS row "ADDRESS:A-9001" with contact_value "88/1 Bangkok", total_balance 1,250,000.00 and `data_as_of` 2026-11-25; the same person with no ADDRESS row for AC3; DP07 Legal with pod_key "POD-0001", notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED"; and a delayed answer beyond 2 s |
| rwb-case WireMock | RWB-P3-E1018-CON | Case "RW-2026-000123" with product group "MORTGAGE" and party "P-0001" as borrower; case "RW-2026-000456" with product group "HIRE_PURCHASE"; the parties of "RW-2026-000123" without "P-0999"; the owner of "RW-2026-000123"; the two accepted task raises; and a delayed answer beyond 2 s |
| rwb-case reference-data WireMock | RWB-P3-E1043-CON | LOV-NOTICE with DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE; LOV-SENT-TYPE with BEFORE_NPL and NPL; LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED; and a delayed answer beyond 2 s |
| rwb-decision WireMock | RWB-P7-E1027-CON | One D7.1 entry for case "RW-2026-000123" with rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference; an empty answer for a refused attempt; and a delayed answer beyond 2 s |
| rwb-document WireMock | The published rwb-document document | A stored generated document with `source` "GENERATED", `write_once` true, the case number, the customer name, 1,250,000.00 THB and the footer "RW-2026-000123 DEMAND-MTG v2 2026-11-25"; a failure answer after the write; and a delayed answer beyond 2 s |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 8 consumed | API-P6-001 and API-P6-002 provided; the eight rows of 12.2 consumed, one hop each with a 2 s budget |
| Kafka | 2 published, 3 declared as consumed | `NoticeGenerated` and `DecisionRecorded` published; `CaseStateChanged`, `DeviationRaised` and `DeviationCleared` declared, consumed by the dispatch stories |
| Temporal | None | No workflow, no activity and no Schedule in this story |
| File | None | The PDF is handed to rwb-document through its contract; this service writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `notices`, Java package `th.co.scb.ace.workbench.recovery.comms.notices`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this service reads no view | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for DP-04, DP-06, DP-08, DP-10, DP-14 or DP-18: this story evaluates no rule package, reads no parameter, calls no authorise operation, starts no job, keeps the platform topic name and writes no interaction ledger.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}`, with validation and the problem mapping of the error envelope |
| NoticeGenerationService | Service | Steps 2 to 10 of the flow: the idempotency answer, the template check, the hold paths, the record write, the render and the store |
| TemplateCatalog | Service | The current Approved version for a notice type, product group and language, from `template` |
| MergeValueResolver | Service | Resolves each merge code through the owner named by `merge_field.source_entity` and the column named by `merge_field.source_field`, and builds the merge snapshot |
| LetterRenderer | Service | Fills the approved body and renders the PDF with the footer: case number, template code, template version and generation date |
| NoticeRepository | Repository | Reads and writes `notice`; finds by case, notice type, `person_key` and business date |
| SourceDataClient | Client | The two rwb-source-data reads of 12.2, one hop with the 2 s budget |
| CaseClient | Client | The case, the parties, the task raise and the reference-data reads of rwb-case |
| DocumentClient | Client | Stores the generated PDF through rwb-document and returns the document ID |
| LocalDecisionRecordWriter | Service | Writes the D7.1 entry through the decision-record library, first in the transaction, and its outbox row |
| NoticeGeneratedPublisher | Service | Writes `NoticeGenerated` to the outbox in the same transaction as the notice row |

**Database and migrations**

- Writes `notice`, `template` (read only here) and `merge_field` (read only here) in schema `rwb_comms`; writes the local decision record and the outbox, inbox and idempotency rows of the platform library.
- Migration `V1052_1__notice_generation.sql` in the rwb-comms Flyway sequence: the unique index on `(case_id, notice_type, person_key, created_at::date)` and the check constraint on `state` in ('GENERATED','HELD','APPROVED','SENT','DELIVERED','UNSERVED'). No party or contact column is added (BR9).
- The merge snapshot reference is stored on the local decision record; where the snapshot itself is persisted is Not specified in the source documents (GAP-1081; ASM-2029).

**Configuration and reference data**

- LOV-NOTICE, LOV-SENT-TYPE, LOV-PRODUCT, LOV-LANG and LOV-DELIVERY are reference rows read through the rwb-case contract; no notice type, product group, sent type or language is written in code.
- The task code "Complete notice data" and the task owner roles are reference rows of the case model, read through the rwb-case contract.
- The feature switch is `rwb.comms.notice-generation`. Proof of delivery reads a data product the source marks as behind a flag, so the delivery read of API-P6-002 is switched on only when that data product is published, and the notice answer stays complete without it.
- The login is the rwb-comms login (DP-02); its name is allocated by the platform database story and is not fixed here.

**Build steps**

1. Migration and `NoticeEntity`: the unique index, the state check and a test for each.
2. `TemplateCatalog` over `template` and `merge_field`, with the Draft-only and Withdrawn cases of AC2 and AC4; no template value in code.
3. `SourceDataClient`, `CaseClient` and the reference read, each against its WireMock fake, with the missing-row, the timeout and the delayed-answer tests.
4. `MergeValueResolver` with every merge code of the synthetic catalog and the empty required value of AC3; assert that the snapshot holds the column, the business key and the field ID and no value.
5. `LetterRenderer` with the merged text and the footer string of AC1 from a synthetic body.
6. `NoticeGenerationService` with the template check, the two hold paths and the two task raises; tests for AC2, AC3, AC4 and AC8.
7. `LocalDecisionRecordWriter` before `DocumentClient`, with the rollback path; tests for AC5 and the file-store failure of X10.
8. The `Idempotency-Key` answer store and the repeat test of AC6.
9. `NoticeGeneratedPublisher` and the outbox, with the key and the payload asserted; the proof-of-delivery read of AC9.
10. The contract-fake run of the five fakes, so the story builds before rwb-case, rwb-source-data, rwb-document and rwb-decision are live.

**Done when.** The tests in section 16 pass, a generated PDF from the synthetic set opens in a standard PDF reader with Thai text rendered, one `NoticeGenerated` and one `DecisionRecorded` leave the outbox per notice, and no personal value appears in an event, a log or the merge snapshot.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The local decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE account batch is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-002 | A reference or data-product load behind a merged value is refused by its owner | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P4-003 | The person is not on the case, or the case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | The caller holds no Litigation right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required request field is missing | Enter {field}. |
| MSG-GEN-006 | A consumed call does not answer inside 2 s | {system} is not available. Your request is queued and will be retried. |

The message IDs and wording are copied from RWB-E1-052 section 14, with MSG-P1-002 from the message catalog of rwb-source-data and MSG-P4-002, MSG-GEN-001 and MSG-GEN-006 from the platform message catalog. MSG-P1-001 is raised by rwb-source-data on the freshness read and is carried unchanged; its outcome in generation is asserted by legacy AC7, which belongs to RWB-ITG-E1052-ITG. MSG-P4-002 and MSG-P4-003 are raised at the gateway-bff edge and by the case contract, not by this service. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The three screens named by the legacy story are read through the gateway-bff composite route (DP-19):

| Screen | What it shows for this story | State read |
|---|---|---|
| SCR-30 Case documents | The generated notice as a generated document on the case, with its sent date, barcode and delivery status when the delivery facts exist | Generated, Held |
| SCR-01 My work | The "Complete notice data" task for the case owner and the withdrawn-template task for the litigation officer team | Held with its hold reason |
| SCR-18 Notice approval | The notice in state Generated, waiting for approval before dispatch; the approval itself comes in RWB-E2-014 | Generated |

The composite route, its per-screen field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON; this story fixes only the two answers the route reads.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-11 | AC9, BR11 | End to end | `v_ace_pod` row POD-0001 with notice_ref WIN-77001, and a notice with no `v_ace_pod` row |
| TC-E1-052-01 | AC1, BR1, BR4, BR5, BR7, BR9 | End to end | RW-2026-000123 Mortgage, P-0001 with an ADDRESS row in `v_ace_contact`, DEMAND-MTG TH v2 |
| TC-E1-052-02 | AC2, BR1 | End to end | RW-2026-000456 Hire purchase, RECALL-HP TH v1 Draft |
| TC-E1-052-03 | AC3, BR3, BR9 | End to end | P-0001 with no ADDRESS row in `v_ace_contact` |
| TC-E1-052-04 | AC4, BR2 | End to end | DEMAND-MTG TH v2 Withdrawn |
| TC-E1-052-05 | AC5, BR6 | End to end | Decision log store stubbed unavailable |
| TC-E1-052-06 | AC6, BR8 | End to end | Same request twice on 2026-11-25 |
| TC-E1-052-07 | AC7, BR9 | End to end | No COMPLETED ALS row for 2026-11-25, `data_as_of` 2026-11-24 |
| TC-E1-052-08 | AC8 | End to end | P-0999 not on the case |
| TC-E1-052-09 | Access | Component | Service identity without Litigation R calls NoticeApi.generate; refused with MSG-P4-002 |
| TC-E1-052-10 | Principle 5 | NFR | Decision log write forced to fail during generation of 20 notices; none stored |

The eleven cases are the legacy cases of this key, kept in the legacy order with their covers and data unchanged; legacy level System maps to End to end, Access to Component and Resilience to NFR. TC-E1-052-07 covers legacy AC7, which belongs to RWB-ITG-E1052-ITG and is proved there end to end. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: notice types, product groups, languages, templates, merge codes, task codes, the sent type mapping and the delivery status list are data or reference rows read through the owner's contract.
- No personal data in events, logs, workflow inputs or tests. The name and the address reach the PDF only; the notice event carries IDs and the template version only; there is no merge value, no notice body and no addressee in an event, a workflow input or a log line.
- The merge snapshot holds the merge code, the source column, the business key and the field ID of each value, never the value, and the decision record holds only a reference to it.
- ACE data only through the owner's contract: the customer, the contact point, the account balance, the freshness stamp and the delivery facts come from rwb-source-data, and this service reads no ACE view and holds no foreign key into another schema (DP-01, DP-05).
- The clear identity number never leaves ACE and is never merged into a notice; only `id_no_masked` and `id_no_last4` exist for a merge code.
- One hop and a 2 s timeout on every consumed call, with a breaker and a single GET retry; a POST is retried only with the same `Idempotency-Key` (DP-11, ADR-020).
- The generated PDF is write-once and is never overwritten; a correction is a new notice.
- The local decision record, the notice row and the outbox row commit together or not at all, and a failed record means no notice (R-UNI-39, DP-03).
- No production data, no production copy and no production connection in any test or fixture.
- No screen is built here and no route is declared here: the three screens are read through gateway-bff (DP-19).

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | API-P6-001, API-P6-002, MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P7-003, `NoticeGenerated` | TC-E1-052-01 to TC-E1-052-10 |
| RWB-E1-052 | The legacy key whose AC1 to AC6, AC8 and AC9 this story owns | The eight criteria of section 7 | TC-E1-052-01 to TC-E1-052-06, TC-E1-052-08 to TC-E1-052-11 |
| DP-01 | Owner's schema; no service reads another service's tables | `notice`, `template` and `merge_field` in `rwb_comms`, and the not-owned list of 12.7 | TC-E1-052-01, TC-E1-052-03 |
| DP-02 | One login per service | The rwb-comms login as the service identity of section 10 | TC-E1-052-09 |
| DP-03 | Local decision record and the shared topic | The D7.1 record and `DecisionRecorded` on `rwb.decision-record.v1` | TC-E1-052-01, TC-E1-052-05, TC-E1-052-10 |
| DP-05 | ACE data through rwb-source-data's contract | The two rwb-source-data reads of 12.2 and the delivery read of AC9 | TC-E1-052-01, TC-E1-052-03, TC-E1-052-07, TC-E1-052-11 |
| DP-07 | Reference data through rwb-case's contract | LOV-NOTICE, LOV-SENT-TYPE and LOV-PRODUCT reads | TC-E1-052-01, TC-E1-052-02 |
| DP-09 | Outbox, inbox and CloudEvents | `NoticeGenerated` on `rwb.comms.events.v1` and the three declared consumed events | TC-E1-052-01, TC-E1-052-06 |
| DP-11 | REST contract with mock, one hop, 2 s | The eight consumed rows and the five fakes of 12.8 | TC-E1-052-01 to TC-E1-052-08 |
| DP-13 | Per-service REST base | `/api/recovery/comms/v1` for both provided operations | TC-E1-052-01 to TC-E1-052-11 |
| DP-15 | Per-service Flyway | `V1052_1__notice_generation.sql` in `rwb_comms` | TC-E1-052-06 |
| DP-19 | Screen through gateway-bff | The SCR-01, SCR-18 and SCR-30 reads of section 15 | TC-E1-052-01, TC-E1-052-03 |
| ADR-013 | 19 services inside ACE | The service boundary: rwb-comms writes `rwb_comms` only | TC-E1-052-01 |
| ADR-014 | Schema and login per service | `rwb_comms` and its own login | TC-E1-052-09 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The outbox write of 12.3 and the inbox of 12.4 | TC-E1-052-01, TC-E1-052-06 |
| ADR-020 | Contract-first REST, one hop, 2 s | The 2 s budget, the breaker and the retry rule of 12.2 | TC-E1-052-08, TC-E1-052-10 |
| ADR-021 | Per-service Flyway and migration ownership | The migration of section 13 | TC-E1-052-06 |

### 19. Out of scope

- Legacy AC7, the stale ACE account batch, which belongs to RWB-ITG-E1052-ITG, and the end-to-end proof of the whole journey, which is the same slice.
- The write-once generated document itself: the rwb-document part of this legacy key, built through the document contract and faked here.
- The case, the parties, the party roles and the task rows: the rwb-case part of this legacy key.
- The central decision ledger entry and its read: the rwb-decision part, read through `RWB-P7-E1027-CON`.
- The customer, contact, account, freshness and delivery data products: the rwb-source-data part, read through `RWB-P1-E1015-CON`.
- Dispatch to WIN and proof-of-delivery capture: RWB-P6-E1055-APP and RWB-P6-E2021-APP, with JOB-10 and `NoticeDispatchWorkflow`.
- SMS and LINE dispatch through NSS and LINE OA: RWB-P6-E2022-APP.
- Template authoring, approval and withdrawal, and the merge field catalog: RWB-P6-E1046-APP.
- Approval of demand and recall notices before dispatch: RWB-E2-014.
- The litigation route rules that call generation in production: R-LIT-01 and the Epic 5 rule work.
- Contract, credit approval and mortgage documents: RWB-E2-026.
- The authorisation decision itself, which is enforced at gateway-bff under RWB-PLT-N001-CON and RWB-P4-E1037-CON, not in this story.
- The three screens themselves and the gateway-bff composite route specification.
