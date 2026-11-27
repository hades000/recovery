# RWB-ITG-E1052-ITG Notice generation v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Customer and contact facts are read from DP02, balance from DP01, by case uuid (RD-P1-005, RD-P1-021, RD-P1-023; finding #1).
- AC7 is driven by the DP01 STALE stamp; the three legacy Then lines are unchanged (RD-P1-041; findings #2, #3).
- Proof of delivery is read from the date-wide read, which writes nothing; rwb-comms alone appends delivery entries (RD-P1-007; finding #4).
- Build dependencies, contract version and the pending clear-value access for rwb-comms (findings #5 to #7, NEW-GAP-F02-1).
- The recipient name and postal address are read through `GET /customers/{personKey}` (`getCustomer`) by the rwb-comms notice workload identity, not from the DP02 records; the unmasking rules are pending as NEW-GAP-D1 (RD-P1-060).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1052-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1052-ITG-16); the squad confirms the estimate at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None; the integration dependencies below must be deployed in SIT before the suite runs |
| Contract dependencies | No build dependency on a contract. Used at run time, none faked (section 12.8): rwb-document generated-document contract (POST /cases/{caseId}/generated-documents, owner P5); request and answer shape Not specified in the source documents (GAP-1079), to come from RWB-P5-E2026-CON; rwb-case reference-data contract; platform contracts DP-03, DP-07, DP-09, DP-15 and DP-19 (no plan row carries them, GAP-2350) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7): records and freshness reads; proof-of-delivery read as published by RWB-P1-E1055-APP. Other providers: /v1 (published wave 1 contract) |
| Integration dependencies | RWB-P1-E1016-APP, RWB-P1-E1055-APP, RWB-P1-E1015-APP, RWB-P3-E1018-APP, RWB-P1-E1069-APP, RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP, RWB-P7-E1052-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-OCC-001) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005; RD-P1-007; RD-P1-021; RD-P1-023; RD-P1-041, RD-P1-060 |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-052 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1052-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 31 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-052 notice generation journey on the real wave 1 services — an approved template producing one notice and one write-once PDF through P6 rwb-comms and P5 rwb-document, one D7.1 decision record visible through P7 rwb-decision, the party and the notice values read through P3 rwb-case and P1 rwb-source-data, and the refusals, holds, repeat request, stale batch, rollback and role refusals proved on the same path**, so that **wave 1 can exit on evidence that demand, recall and guarantor notices are produced from Legal-approved wording with the address ACE holds, and that no service reads another service's data to do it**.

### 2. Business rationale

Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. The legacy story keeps the party and the contact point out of the Workbench: the name is read by `person_key`, the notice address and phone by the composite `contact_key`, and the outstanding by `account_key`. It merges those values into the current approved template, stores the PDF write-once on the case with the template version in the footer, and records the decision. It serves REQ-OCC-001 and control CTL-14, and the FSD P6 measure "notices with proof of delivery, 100 percent" depends on it.

The target changes who owns each fact, not what the notice says. `notice`, `template` and `merge_field` belong to P6 rwb-comms; `document` and the write-once PDF belong to P5 rwb-document; the case, the parties and the tasks belong to P3 rwb-case; the central decision ledger belongs to P7 rwb-decision; and P1 rwb-source-data is the only reader of the 30 `recovery.v_ace_*` views, so the customer, the contact point, the balance, the delivery facts and the freshness stamp reach P6 through P1's published data-product contract (DP-01, DP-05, DP-18). Each service writes its own local D7.1 record in the same transaction as its change and publishes `DecisionRecorded` on `rwb.decision-record.v1`, and the central ledger shows it within five minutes (DP-03). The notice operations move to P6's own base `/api/recovery/comms/v1` (DP-13) and are reached one hop through gateway-bff (DP-19).

The split is as follows. RWB-P6-E1052-APP builds generation inside P6 — the template check, the merge, the renderer, the footer, the two hold paths, the local decision record and `NoticeGenerated`. RWB-P5-E1052-APP builds the write-once generated document. RWB-P3-E1052-APP builds the case, party and party-role reads and the task raise. RWB-P7-E1052-APP builds the central ledger entry. RWB-P1-E1015-APP builds the freshness read, RWB-P1-E1016-APP the data-product records, RWB-P1-E1055-APP the proof-of-delivery read and RWB-P1-E1069-APP the ACE view contract behind them, and RWB-P3-E1018-APP the case and party reads. This story owns one legacy acceptance criterion, AC7, and adds eleven integration criteria that prove the journey and the recovery behaviour at the contract boundaries. AC1 to AC6, AC8 and AC9 repeat legacy accepted outcomes at integration level; AC10, AC11 and AC12 are new for the target and test only the cross-service behaviour in their titles.

No service contract is faked. Every call in section 12.2 goes to the real SIT service under its published wave 1 contract. The target reading of the points the sources leave open — the P1 contract that serves the ACE facts to P6, the home of the merge snapshot, the route of the stale-batch condition and the P5 operation that stores the generated PDF — is recorded in ASM-0482, ASM-0483, ASM-0485 and ASM-0486 and asserted through the owners' published contracts.

The measure is unchanged from the legacy story: notices produced without re-keying, with the address ACE holds, with the template version in the footer, and with a decision record for every notice.

### 3. Preconditions

- RWB-P6-E1052-APP is done: notice generation, the template check, the merge, the renderer with the footer, the two hold paths (`POSTAL_ADDRESS`, `TEMPLATE_WITHDRAWN`), the task raise through P3, the local D7.1 record and `rwb.comms.NoticeGenerated.v1` run on P6 rwb-comms and are in SIT.
- RWB-P5-E1052-APP is done: a generated PDF is stored write-once through P5 rwb-document and returns a document ID with `source` "GENERATED" and `write_once` true.
- RWB-P3-E1052-APP is done: the case summary, the case parties and party roles are served, and a task with task code "Complete notice data" is raised to the case owner and to the litigation officer team.
- RWB-P7-E1052-APP is done: the central ledger consumes `rwb.decision-record.v1` idempotently and serves the entry through `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` within five minutes.
- RWB-P1-E1015-APP is done: the freshness stamp per data product (`businessDate`, `status` LOADED or STALE, `staleSince`) is published on P1 rwb-source-data.
- RWB-P1-E1069-APP is done: the ACE view contract is in place. RWB-P1-E1016-APP is done: `GET /data-products/{productCode}/records` serves DP01 Account and arrears (account balance and `data_as_of`) and DP02 Customer and party (customer and contact point) for a case uuid, with the freshness stamp. RWB-P1-E1055-APP is done: `GET /proof-of-delivery?businessDate=` serves the WIN delivery facts of a completed WIN date and writes nothing. `GET /customers/{personKey}` (operationId `getCustomer`, built by RWB-P1-E1069-APP) serves the customer name and the contact rows with their values, masked unless the caller's identity is allowed (RD-P1-060).
- RWB-P3-E1018-APP is done: the case record and the party links are readable by business key.
- The P6, P5, P3, P1 and P7 contracts are deployed under their per-service bases behind gateway-bff.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases, templates, users and clock control.
- Templates for DEMAND, RECALL and GUARANTOR_NOTICE are Approved for the product groups in the synthetic set, in language TH; "DEMAND-MTG" "TH" version 2 is current on 2026-11-25 and "RECALL-HP" "TH" has only version 1 in state Draft.
- Synthetic users hold RW-LITOFF, RW-CASEOWN, RW-LEGAL and a role without the Litigation right; the P6 contract edge checks the Litigation and Documents rights from the P4 permission data already in SIT (a wave 1 platform precondition, not a build dependency of this story).
- The clock control reads 2026-11-25 and can move to 2026-11-27 and 2026-11-30; the P5 document-store fault switch, the P7 ledger lag control and the P1 data-product fixture set are available.
- No production data is used, no production copy is loaded and no production connection is opened. Every notice, address and delivery value in the suite is synthetic.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- This story has no build dependency, so it is ready on Day 1.

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, templates, users, P1 data products and P5 fault switch of harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: reads the case and the party links through P3 with `GET /api/recovery/case/v1/cases/RW-2026-000123` and `GET /api/recovery/case/v1/cases/RW-2026-000123/parties`, and asserts product group "MORTGAGE" and person_key "P-0001" as borrower.
3. Harness: reads the template list through P6 with `GET /api/recovery/comms/v1/admin/templates` and asserts "DEMAND-MTG" "TH" version 2 Approved and current on 2026-11-25.
4. Harness: reads DP01 Account and arrears through P1 with `GET /api/recovery/source-data/v1/data-products/freshness` and `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={case uuid}`, and asserts total_balance 1,250,000.00 and `data_as_of` 2026-11-25; it then reads `GET /api/recovery/source-data/v1/customers/P-0001` and asserts `firstName`, `lastName` and the ADDRESS contact row "ADDRESS:A-9001" (`contactValue`, `city`, `postCode`, `country`), clear for the rwb-comms notice workload identity and masked for every user role (RD-P1-060; ASM-0482).
5. Harness: calls `POST /api/recovery/comms/v1/cases/RW-2026-000123/notices` with notice type "DEMAND", person_key "P-0001", language "TH", business date 2026-11-25 and an Idempotency-Key (ASM-0486).
6. P6: resolves each merge code through the owner of its source field — `CASE_NO`, `PRODUCT_GROUP` and `ENTRY_DATE` from P3; `CUSTOMER_NAME`, `POSTAL_ADDRESS`, `PHONE` and `TOTAL_OUTSTANDING` from P1 — and carries the ACE business date of each value.
7. P6: renders the DOCX template to PDF with the footer case number, template code, template version and generation date, writes the local D7.1 record (rule "R-LIT-03", template code and version, merge snapshot reference held in P6 as references only, never the merged value), stores the PDF through P5 write-once, writes the notice row with `person_key`, `template_id`, notice type, sent type and state Generated, and writes `NoticeGenerated` to the outbox — record, document reference, notice and outbox in one transaction (ASM-0483; ASM-0484).
8. Harness: reads `GET /api/recovery/comms/v1/notices/{noticeId}` and asserts notice type "DEMAND", sent type "NPL", person_key "P-0001", template version 2, state "Generated" and the document ID.
9. Harness: reads `GET /api/recovery/document/v1/documents/{documentId}` and asserts `source` "GENERATED", `write_once` true, the case number, the customer name, 1,250,000.00 THB and the footer "RW-2026-000123 DEMAND-MTG v2 2026-11-25".
10. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123` within five minutes and asserts one entry with decision code "D7.1", rule "R-LIT-03", template "DEMAND-MTG" version 2, the merge snapshot reference and the data date (ASM-0484).
11. Harness: consumes `rwb.comms.events.v1` and `rwb.decision-record.v1` with a test consumer group and asserts one `rwb.comms.NoticeGenerated.v1` carrying the notice ID, case ID, notice type and template version and one `DecisionRecorded`, with IDs and facts only.
12. Harness: runs the refusal, hold, repeat, stale, rollback and role paths of AC2 to AC6 and AC8 to AC12, writes the evidence report with each status, message, state and data date, removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The template has no Approved version | Refused; no notice row and no document created | MSG-P6-005 | AC2 |
| X2 | A required merge value is empty, for example no ADDRESS row in the P1 contact records for the person | Notice held in state "Held" with `hold_reason` "POSTAL_ADDRESS"; no document; task "Complete notice data" to the case owner | MSG-P6-007 | AC3 |
| X3 | The current template version is Withdrawn and no later version is Approved | Notice held in state "Held" with `hold_reason` "TEMPLATE_WITHDRAWN"; task to the litigation officer team; no document | MSG-P6-003 | AC4 |
| X4 | The local D7.1 record cannot be written | Nothing is stored; the call fails with 503 and an incident is raised under rule R-UNI-39; the central ledger receives no entry | MSG-P7-003 | AC5 |
| X5 | The same request arrives twice on one business date | The first notice is returned; no second notice and no second document | None | AC6 |
| X6 | The ACE batch is stale — no COMPLETED ALS row for 2026-11-25, DP01 freshness status STALE with business date 2026-11-24 and `data_as_of` 2026-11-24 | Generation proceeds from the 2026-11-24 balance; the decision record carries data date 2026-11-24 | MSG-P1-001 | AC7 |
| X7 | The person is not a party on the case | Refused; no notice row and no document | MSG-P4-003 | AC8 |
| X8 | P1 holds no proof-of-delivery row for the notice reference | The notice shows as generated with no delivery confirmation and the delivery matcher of RWB-E1-055 lists it; the notice row is unchanged | None | AC9 |
| X9 | The P5 document store exceeds 2 s or returns 503 | The notice row and the PDF are rolled back; a correcting decision record follows under R-UNI-24; one retry succeeds and creates one notice and one document | MSG-P7-003 for the incident path only | AC10 |
| X10 | The caller holds a role without the Litigation right | Refused at the contract edge with 403; no data is returned | MSG-P4-002 | AC11 |
| X11 | A personal value appears in the event, the log or the merge snapshot | The assertion fails and the suite names the field and the sink; the run fails | None | AC12 |
| X12 | The fixture set does not match the harness expectations, or the clock, the P5 fault switch or the P7 lag control cannot be set | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC7, AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the APP stories it depends on and the published contracts of P6, P5, P3, P1 and P7, not their source code |
| Negotiable | Case numbers, person keys, template codes, account keys, dates and delivery references are fixture data; the story fixes the assertions and the call set |
| Valuable | Wave 1 can exit only on evidence that a notice, its write-once PDF, its decision record and its ACE facts hold together across five services, and that the holds and refusals behave |
| Estimable | One suite module, one fixture pack, five contract readers, one event consumer, one fault-control reader and one evidence report |
| Small | Twelve scenarios over five services; no service code, no schema change and no screen |
| Testable | Every scenario asserts a contract response, a state, a document flag, a ledger entry, a message or the absence of a personal value; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Notice generation v1, end-to-end across the wave 1 services

  Background:
    Given the wave 1 services rwb-comms, rwb-document, rwb-case, rwb-source-data and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RW-2026-000123" has product group "MORTGAGE" and borrower person_key "P-0001"
    Given the P1 data product "DP01" Account and arrears holds the case's primary account_key with total_balance 1,250,000.00 and data_as_of 2026-11-25
    Given the business date is 2026-11-25
    Given the RWB-ITG-W1J01-ITG synthetic cases, templates and ACE data products are loaded and no production data is used

  Scenario: AC1 An approved template generates one notice and one write-once PDF across the services (new, D-RCV-60)
    Given GET /api/recovery/source-data/v1/customers/P-0001 returns person_key "P-0001" with the customer name to the rwb-comms notice workload identity
    Given the same answer returns an ADDRESS contact row for "P-0001" with contact_key "ADDRESS:A-9001" and contact_value "88/1 Bangkok"
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with notice type "DEMAND", person_key "P-0001", language "TH" and business date 2026-11-25
    Then the call returns one notice ID in state "Generated" and one document ID
    Then GET /api/recovery/document/v1/documents/{documentId} returns source "GENERATED" and write_once true
    Then the PDF shows "RW-2026-000123", the customer name and 1,250,000.00 THB (the clear name and address come from `getCustomer` for the rwb-comms notice workload identity; the masking rule rows are Pending, owner data protection officer with the rwb-access owner, tracked as NEW-GAP-D1; the run uses the FieldMasker fake that unmasks `firstName`, `lastName` and `contactValue` for that identity and asserts the masked branch too)
    Then the footer reads "RW-2026-000123 DEMAND-MTG v2 2026-11-25"
    Then the notice row reads notice_type "DEMAND", sent_type "NPL", person_key "P-0001", template version 2 and state "Generated"
    Then GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123 shows one entry with decision code "D7.1", rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference within five minutes
    Then one rwb.comms.NoticeGenerated.v1 with the notice ID, the case ID, the notice type and template version 2 is read on rwb.comms.events.v1

  Scenario: AC2 A template with no Approved version is refused (new, D-RCV-60)
    Given template "RECALL-HP" "TH" has only version 1 in state "Draft"
    Given case "RW-2026-000456" has product group "HIRE_PURCHASE"
    When POST /api/recovery/comms/v1/cases/RW-2026-000456/notices is called with notice type "RECALL" and language "TH"
    Then the system refuses it with MSG-P6-005 naming "RECALL-HP" version 1
    Then no notice row and no document are created

  Scenario: AC3 A required merge value that is empty holds the notice and raises a P3 task (new, D-RCV-60)
    Given the P1 data product "DP02" Customer and party holds no ADDRESS row for person_key "P-0001"
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with notice type "DEMAND" and person_key "P-0001"
    Then GET /api/recovery/comms/v1/notices/{noticeId} returns state "Held" with hold_reason "POSTAL_ADDRESS"
    Then the suite reads no document ID on the notice and finds no generated document for it through P5
    Then a task "Complete notice data" exists on case "RW-2026-000123" for the case owner through P3 with MSG-P6-007 naming "POSTAL_ADDRESS"

  Scenario: AC4 A withdrawn template holds the notice (new, D-RCV-60)
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with notice type "DEMAND"
    Then the notice row exists in state "Held" with hold_reason "TEMPLATE_WITHDRAWN"
    Then a task to the litigation officer team exists through P3 with MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC5 A failed local decision record stops the notice and the document (new, D-RCV-60)
    Given the P6 local decision-record write is forced to fail for the next generation
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with notice type "DEMAND"
    Then the call fails with status 503 and MSG-P7-003
    Then no notice row and no document are created
    Then the system raises an incident under rule R-UNI-39
    Then GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123 holds no D7.1 entry for the attempt

  Scenario: AC6 A repeated request on the same business date returns the first notice (new, D-RCV-60)
    Given a notice for case "RW-2026-000123", notice type "DEMAND", person_key "P-0001" was generated on 2026-11-25
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called again with the same values on 2026-11-25
    Then the system returns the existing notice
    Then the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC7 Stale ACE account batch (legacy RWB-E1-052 AC7)
    Given no COMPLETED ALS row exists for 2026-11-25, the DP01 expected_by of 08:00 on 2026-11-26 has passed, and GET /api/recovery/source-data/v1/data-products/freshness returns DP01 with businessDate 2026-11-24, status STALE and staleSince 2026-11-25
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then the system generates the notice from the 2026-11-24 balance
    Then the decision log entry records data date 2026-11-24
    Then the result carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24

  Scenario: AC8 A person who is not on the case is refused (new, D-RCV-60)
    Given person_key "P-0999" is not a party on case "RW-2026-000123"
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with person_key "P-0999"
    Then the system refuses it with MSG-P4-003
    Then no notice row and no document are created

  Scenario: AC9 Proof of delivery is read through the source-data contract and the notice is unchanged (new, D-RCV-60)
    Given notice "N-0001" on case "RW-2026-000123" has notice_ref "WIN-77001"
    Given the WIN batch of business date 2026-11-27 is COMPLETED and GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-27 returns pod_key "POD-0001" with notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED"
    When GET /api/recovery/comms/v1/notices/N-0001 is called
    Then the notice shows sent date 2026-11-27, barcode "RR123456789TH" and status "DELIVERED" read through the P1 contract
    Then the notice row is unchanged and no direct view read is made
    Then the proof-of-delivery read writes no entry to the interaction ledger of the case

  Scenario: AC10 A document store timeout rolls the notice back with no orphan document (new, D-RCV-60)
    Given the P5 document store is set to exceed 2 s and return 503 for the next generated PDF
    When POST /api/recovery/comms/v1/cases/RW-2026-000123/notices is called with notice type "DEMAND"
    Then no notice row and no PDF exist for the attempt
    Then a correcting decision record follows the failed attempt under R-UNI-24
    When the P5 fault switch is cleared and the same request is sent once more
    Then one notice in state "Generated" and one write-once document exist and the case holds no second PDF

  Scenario: AC11 A role without the Litigation right is refused (new, D-RCV-60)
    Given a synthetic user holds a role without the Litigation read right
    When that user calls POST /api/recovery/comms/v1/cases/RW-2026-000123/notices
    Then the call returns 403 with MSG-P4-002
    Then no notice or document data is returned

  Scenario: AC12 Personal data stays out of events, logs and the merge snapshot (new, D-RCV-60)
    Given a notice is generated for case "RW-2026-000123" with person_key "P-0001"
    When the suite reads rwb.comms.NoticeGenerated.v1, rwb.decision-record.v1, the P6 and P5 logs of the run and the merge snapshot reference of the D7.1 entry
    Then the event, the log lines and the snapshot hold IDs, field references and business keys only
    Then no name, address, national ID or account number appears in the event, the log or the snapshot

  Scenario: AC13 Merge sources, snapshot content, contract-only reads and call resilience hold across the services (new, D-RCV-60)
    Given a notice is generated for case "RW-2026-000123" with person_key "P-0001" and merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    When the suite reads the merge snapshot referenced by the D7.1 entry, the calls of the run and the call settings of each consumed operation in section 12.2
    Then each merge code resolves to a P3 field or a P1 data-product field and none uses the clear identification_number, only id_no_masked or id_no_last4 where an identity number is merged
    Then each snapshot entry holds the merge code, the source system and column, the business key and the field ID and never the value
    Then every read of another service's data is a contract read and no service reads another service's tables
    Then notice, template and merge_field are written only by P6, document only by P5, the case, parties and tasks only by P3, the data products only by P1 and the central ledger only by P7
    Then each consumed call is one hop from gateway-bff or from the owning service with a 2 s timeout and a circuit breaker, a GET has a single retry with jitter and a POST is retried only with the same Idempotency-Key
```

**Target reading.** AC7 is the one legacy criterion this story owns and is copied word for word, tag included at the end of its Scenario line. The suite drives its condition through P1: `GET /api/recovery/source-data/v1/data-products/freshness` returns DP01 with business date 2026-11-24 and status STALE once the `expected_by` of 08:00 on 2026-11-26 has passed with no COMPLETED ALS row for 2026-11-25, the account balance for the notice is read from DP01 Account and arrears at 2026-11-24, and the assertions stay exactly the three legacy Then lines including MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24 (ASM-0485). AC1 to AC6, AC8 and AC9 repeat legacy accepted outcomes at integration level through the target contracts, which is why they carry the origin tag of this run and not a legacy tag; their component-level twins sit with RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP and RWB-P7-E1052-APP. AC10, AC11 and AC12 test only the cross-service behaviour named in their titles.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A notice is generated only from the current Approved template for its notice type, product group and language, read from P6 rwb-comms | RWB-E1-052 BR1; R-LIT-03; CTL-14 |
| BR2 | A withdrawn template holds generation in P6 and raises a task to the litigation officer through P3 | RWB-E1-052 BR2; R-LIT-04 |
| BR3 | A required merge value that is empty holds the notice, names the field and raises a task to the case owner through P3 | RWB-E1-052 BR3; merge_field.is_required; pattern of R-RES-36 |
| BR4 | The footer carries the case number, template code, template version and generation date, and P5 returns it on the stored document | RWB-E1-052 BR4; REQ-OCC-001; CTL-14 evidence |
| BR5 | The generated PDF is a write-once document on the case, held by P5 rwb-document | RWB-E1-052 BR5; CTL-12; DT06 |
| BR6 | A notice whose local decision record cannot be written is not generated; the local record, the notice and the outbox row commit together in P6, and the central ledger entry follows within five minutes | RWB-E1-052 BR6; Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR7 | Sent type is NPL for a case at 90 days past due or more; the mapping is reference data | RWB-E1-052 BR7; LOV-SENT-TYPE; DL16 (open; assumptions ASM-1094, ASM-5264) |
| BR8 | One notice per case, notice type, `person_key` and business date, enforced by the P6 idempotency key | RWB-E1-052 BR8; R-UNI-40; notice.person_key (DF-LEG-030) |
| BR9 | The party, the customer name and the notice address are read by `person_key` and the composite `contact_key` (`contact_type:key`) through P1 rwb-source-data's `getCustomer` operation (`GET /customers/{personKey}`, RD-P1-060); no service holds a party or contact copy and no service reads `recovery.v_ace_*` except P1 | RWB-E1-052 BR9; D-RCV-35 U4; ADR-010; DP-01; DP-05 |
| BR10 | A merge code resolves to a P3 field or a P1 data-product field. The clear `identification_number` is never a merge source; `id_no_masked` and `id_no_last4` only | RWB-E1-052 BR10; ADR-010; DF-ACE-073 |
| BR11 | Proof of delivery is read through P1 `GET /proof-of-delivery?businessDate=` and matched by `notice_ref` in rwb-comms; the read writes nothing, only rwb-comms appends delivery entries to the ledger, and the Workbench writes no WIN delivery fact | RWB-E1-052 BR11; RWB-E1-055; DP-05 |
| BR12 | The merge snapshot is held in P6 as references only — the merge code, the source system and column, the business key and the field ID — and never the value | RWB-E1-052 BR12; NFR-040; guardrail on personal data |
| BR13 | No service reads another service's tables. `notice`, `template` and `merge_field` are written only by P6, `document` only by P5, the case, parties and tasks only by P3, the data products only by P1 and the central ledger only by P7; every read in this story is a contract read | DP-01; Arch v5 slide 29; Arch v5 slide 11 |
| BR14 | Every consumed call is one hop from gateway-bff or from the owning service with a 2 s timeout, a circuit breaker and a single GET retry with jitter; a POST is retried only with the same Idempotency-Key | DP-11; DP-19; ADR-020; Arch v5 slides 10 and 11 |

The behaviour of BR1 to BR12 is built by the APP stories named in section 3. This story asserts it through the contracts and changes none of it. The five template operations are read from the P6 contract in the registry, the freshness stamp from the P1 freshness contract, and the generation hold stays with the P6 notice workflow and RWB-E1-052; no request, response, state or message changes.

### 9. State transitions

None. This story does not change a case status. It observes the notice state, the document state and the decision-record state of the legacy table:

| From | Event | Condition | To |
|---|---|---|---|
| None | Generate through POST /cases/{caseId}/notices | Template Approved and all required merge values present | Generated |
| None | Generate | A required merge value empty | Held, hold_reason "POSTAL_ADDRESS" |
| None | Generate | Template state Withdrawn and no later Approved version | Held, hold_reason "TEMPLATE_WITHDRAWN" |
| Generated | A notice is read while P1 holds no proof-of-delivery row | No delivery confirmation available | Generated, unchanged, with no delivery confirmation |
| Any | Generate with the same key on the same business date | caseId, noticeType, personKey and business date already present | The first notice is returned; no state change |

The P5 document moves from none to Generated and is never overwritten, so a correction is a new notice. The decision record is written locally in P6 in the same transaction as the notice and the outbox row, and the P7 central ledger entry appears within five minutes; after a rolled-back document store the correcting record follows under R-UNI-24 and the notice stays absent. No case status, stage or timer is changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic cases, templates, users and P1 data products, sets the clock and the fault controls, reads the evidence report |
| P6 rwb-comms service identity | Serves `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` and the template list; holds Litigation R and Documents R; writes only `rwb_comms` |
| P5 rwb-document service identity | Stores the generated PDF write-once and returns the document; writes only `rwb_document` |
| P3 rwb-case service identity | Serves the case, the parties and the party roles and raises the two tasks; writes only `rwb_case` |
| P1 rwb-source-data service identity | Serves the data-product freshness and records, including the customer, contact, account and proof-of-delivery facts; the only reader of `recovery.v_ace_*`; writes only `rwb_source_data` |
| P7 rwb-decision service identity | Consumes `rwb.decision-record.v1` into the central ledger and serves the entry; writes only `rwb_decision` |
| RW-LITOFF, litigation officer | Reads the notice and the document (Litigation CRUA, Documents CRU); receives the withdrawn-template task through P3 |
| RW-CASEOWN, case owner | Reads the notice (Litigation R); receives the missing-data task through P3 |
| RW-LEGAL, Legal counsel | Reads the notice (Litigation RA); approves the template versions the suite reads |
| A role without the Litigation right | Calls the notice operation and is refused with MSG-P4-002; no notice or document data is returned |
| The ACE data owner role | Owns the ACE tables and columns behind the views; not exercised directly by the suite |

No approval level from the delegation of authority applies to notice generation; the two rights that matter are the Litigation right and the Documents right. No other role is in scope for this story.

### 11. Data

| BR Field ID | Entity (owning service) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-009 | recovery_case (P3 rwb-case) | id, case_no, product_group, owner_user_id | Read through the P3 contract |
| DF-CAS-031, DF-CAS-032, DF-CAS-033 | case_party (P3 rwb-case) | case_id, person_key, party_role | Read through the P3 contract |
| DF-ACE-056, DF-ACE-057, DF-ACE-058 | v_ace_customer (P1 rwb-source-data) | person_key, first_name, last_name | Read through the P1 data-product contract |
| DF-ACE-073, DF-ACE-074 | v_ace_customer (P1 rwb-source-data) | id_no_masked, id_no_last4 | Read through the P1 contract; never merged in clear |
| DF-ACE-075, DF-ACE-076, DF-ACE-077, DF-ACE-078 | v_ace_contact (P1 rwb-source-data) | contact_type, contact_key, person_key, contact_value | Read through the P1 contract; contact_key is the composite `contact_type:key` |
| DF-ACE-081, DF-ACE-082, DF-ACE-083 | v_ace_contact (P1 rwb-source-data) | city, post_code, country | Read through the P1 contract |
| DF-ACE-001, DF-ACE-020, DF-ACE-036 | v_ace_account (P1 rwb-source-data) | account_key, total_balance, data_as_of | Read through the P1 contract; data_as_of 2026-11-25 in the base case and 2026-11-24 in AC7 |
| DF-ACE-251, DF-ACE-253, DF-ACE-254, DF-ACE-255, DF-ACE-256, DF-ACE-257 | v_ace_pod (P1 rwb-source-data) | pod_key, notice_ref, sent_date, barcode, callback_date, delivery_status | Read through the P1 contract |
| DF-REF-046, DF-REF-047 | template (P6 rwb-comms) | template_code, template_version | Read through the P6 contract |
| DF-REF-253, DF-REF-254, DF-REF-255, DF-REF-257 | merge_field (P6 rwb-comms) | merge_code, source_entity, source_field, is_required | Read through the P6 contract |
| DF-DOC-001 to DF-DOC-011 | document (P5 rwb-document) | all fields, `source` and `write_once` | Read through the P5 contract; written by P5, never by the suite |
| DF-LEG-015, DF-LEG-016, DF-LEG-017, DF-LEG-018 | notice (P6 rwb-comms) | id, case_id, document_id, notice_type | Read through the P6 contract |
| DF-LEG-023, DF-LEG-030, DF-LEG-031, DF-LEG-032 | notice (P6 rwb-comms) | sent_type, person_key, template_id, hold_reason | Read through the P6 contract |
| Standard column | notice (P6 rwb-comms) | state | Read through the P6 contract |
| DF-WRK-019, DF-WRK-023 | task (P3 rwb-case) | task_code, owner_role | Read through the P3 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 rwb-decision) | all fields, including decision code, rule, template version, data date and the merge snapshot reference | Read through the P7 contract; the local record is written by P6 inside `rwb_comms` |

DF-ACE-056 to DF-ACE-083 are read through `GET /customers/{personKey}` (RD-P1-060; the DP02 records answer contact rows without value, name or address), DF-ACE-001, DF-ACE-020 and DF-ACE-036 through its DP01 records, and DF-ACE-251 to DF-ACE-257 through the proof-of-delivery read. The `caseId` of every P1 call is the uuid of the case; RW-2026-000123 is display text.

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the field list of RWB-E1-052. The suite only reads through contracts: it never reads a schema of any service, never writes a notice, document, task or ledger row, and holds no table of its own (DP-01). The merge snapshot is P6's, and the suite reads only its reference through the notice and the decision record (ASM-0483). Every value in the suite is synthetic, and the notice address "88/1 Bangkok" is the synthetic address of the legacy fixture.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, task queue `rwb-integration`, schema `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/comms/v1/cases/{caseId}/notices | P6 rwb-comms | Request generation for a case, notice type, person_key, language and business date (ASM-0486) |
| GET /api/recovery/comms/v1/notices/{noticeId} | P6 rwb-comms | Read the notice row, its state, hold reason, template version, document ID and delivery facts |
| GET /api/recovery/comms/v1/admin/templates | P6 rwb-comms | Read the template versions, their states and the current version for a code and language |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the generated document, `source`, `write_once` and the footer values |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case number, product group, status and owner |
| GET /api/recovery/case/v1/cases/{caseId}/parties | P3 rwb-case | Read the party links and roles, and prove person_key is on the case |
| GET /api/recovery/source-data/v1/data-products/freshness | P1 rwb-source-data | Read `businessDate`, `status` (LOADED or STALE) and `staleSince` of DP01 Account and arrears and DP02 Customer and party |
| GET /api/recovery/source-data/v1/data-products/{productCode}/records | P1 rwb-source-data | Read the account records (`/data-products/DP01/records`), query `caseId` (uuid, required); `fields` entries of `fieldName`, `value`, `masked` |
| GET /api/recovery/source-data/v1/customers/{personKey} | P1 rwb-source-data | `getCustomer`: the clear name and ADDRESS row for the rwb-comms notice workload identity, with the DP02 freshness (RD-P1-060) |
| GET /api/recovery/source-data/v1/proof-of-delivery?businessDate={date} | P1 rwb-source-data (RWB-P1-E1055-APP) | Read the WIN delivery facts of a completed date; the read writes nothing; delivery entries are appended by rwb-comms only |
| GET /api/recovery/decision/v1/decision-log?caseId={caseId} | P7 rwb-decision | Read the D7.1 entry, its rule, template version, data date and merge snapshot reference |

Every call is one hop on the owner's base with a 2 s timeout (DP-11, DP-13, DP-19; ADR-020). No monolith path is called. P6 obtains the ACE facts through P1's data-product contract (ASM-0482) and stores the generated PDF through P5's generated-document operation (ASM-0483); the suite asserts the outcome through the contracts of this table, not the internal call.

#### 12.3 Events published

None. The suite publishes no event and owns no topic, no queue and no schema.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.comms.NoticeGenerated.v1 | rwb.comms.events.v1 | P6 rwb-comms | Assert one event per generated notice with the notice ID, case ID, notice type and template version, and no personal value |
| DecisionRecorded | rwb.decision-record.v1 | P6 rwb-comms | Assert the local record reaches the shared topic once per committed notice and carries IDs and facts only |

The suite consumes both with a test consumer group and its own inbox; it publishes nothing. `DecisionRecorded` is a shared topic, not a P6 topic, and the suite reads it to prove that the local record left P6 (DP-03, DP-09).

#### 12.5 Workflows and activities

None. Generation is synchronous inside P6 in this slice: the POST returns the notice and the document reference. No workflow, activity or Nexus operation is started or awaited by this story. Notice dispatch, `NoticeDispatchWorkflow` and JOB-10 belong to RWB-E1-055 and are not asserted here.

#### 12.6 Schedules

None. No Schedule is started, moved or waited for, and no shared scheduler table is read. The suite moves only its own clock control.

#### 12.7 Tables owned

None. The suite owns no table (DP-01). `notice`, `template` and `merge_field` belong to P6 rwb-comms; `document` to P5 rwb-document; `recovery_case`, `case_party` and `task` to P3 rwb-case; the data products and the ACE view contract to P1 rwb-source-data; `decision_log_entry` to P7 rwb-decision. The suite never reads any of those schemas.

#### 12.8 Contract fakes

No service contract is faked. No contract fake is used for rwb-case, rwb-comms, rwb-decision, rwb-document or rwb-source-data, so no contract fake library version applies. Every call in section 12.2 and every event in section 12.4 goes to the real SIT service under its published wave 1 contract. Only the outside-of-contract controls are synthetic:

| Control | Boundary | Why it is not a contract fake |
|---|---|---|
| P1 data-product fixture set | Data loaded into the real P1 sources: the DP01 account rows and the DP02 customer and contact rows for person_key "P-0001" and "P-0999", the missing ADDRESS case, the 2026-11-24 `data_as_of` case, and the proof-of-delivery row `POD-0001` with notice_ref "WIN-77001" under a COMPLETED WIN batch of 2026-11-27 | It seeds the owner's data; the response is produced by the real P1 contract and is read back through it |
| P5 document-store fault switch | A configuration switch on the real SIT P5 that makes the next generated store exceed 2 s and return 503 | It changes the timing of the real service; the P5 contract is not stubbed |
| P7 ledger lag control | A configuration control on the real SIT P7 ingest that holds the ledger entry for the five-minute window | It changes the arrival time of the real entry; `GET /decision-log` is not stubbed |
| Clock control | The harness clock on the P6 and P1 business date | It moves the date the real services read; no response is fabricated |
| Event consumer group | The suite's own test consumer group and inbox on `rwb.comms.events.v1` and `rwb.decision-record.v1` | It reads the real produced events; it does not produce any |

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 9 |
| Kafka | 0 | 2 |
| Temporal | 0 | 0 |
| File | 0 | 1 (the generated PDF through Blob, read through P5) |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the twelve scenarios against SIT and holds no service code |
| Notice fixture pack | Test data | The synthetic cases "RW-2026-000123" and "RW-2026-000456", person_key "P-0001" and "P-0999", template "DEMAND-MTG" "TH" version 2, "RECALL-HP" "TH" version 1 Draft, the withdrawn "DEMAND-MTG" case, notice "N-0001" with notice_ref "WIN-77001" and the missing-ADDRESS case |
| P1 data-product reader | Assertion | Reads freshness, the DP01 records, `getCustomer` and the proof-of-delivery rows through the P1 contract and compares the business date, the balance, the contact row and the delivery facts |
| Case and party reader | Assertion | Reads the case and the parties through the P3 contract and proves the party role and the task raise |
| Notice and template reader | Assertion | Reads the template list and the notice through the P6 contract and compares state, hold reason, notice type, sent type, template version and document ID |
| Document reader | Assertion | Reads the generated document through the P5 contract and compares `source`, `write_once`, the footer string and the printed values |
| Ledger reader | Assertion | Reads the decision log through the P7 contract within five minutes and compares decision code, rule, template version, data date and the merge snapshot reference |
| Event consumer | Assertion | Consumes `rwb.comms.events.v1` and `rwb.decision-record.v1` with a test group and asserts one event per notice, IDs only |
| Personal-data scanner | Assertion | Scans the two topics, the P6 and P5 log lines of the run and the merge snapshot reference for a name, an address, a national ID and an account number |
| Evidence report | Report | Records per scenario the status, the message, the notice state, the document flag, the data date and the ledger entry |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | notice, template and merge_field sit in rwb_comms; document in rwb_document; case, case_party and task in rwb_case; the data products in rwb_source_data; decision_log_entry in rwb_decision. The suite asserts through contracts only |
| DP-02 | recovery_svc login | One login per service | none | Each of the five services calls the others with its own login and workload identity; the suite holds no database login |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic rwb.decision-record.v1 | H RWB-PLT-E1027-CON | The D7.1 record is written in rwb_comms in the same transaction as the notice and the outbox row, published on rwb.decision-record.v1 and read back through P7 within five minutes |
| DP-05 | AceSourceQuery, v_ace_*, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | The customer, contact and account facts reach P6 through the P1 records read, delivery facts through the P1 proof-of-delivery read and freshness through the P1 freshness read; the suite seeds and reads the same contract (ASM-0482) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The sent type mapping and the notice type list are reference rows read through the P3 contract; the merge field catalog is P6's own row set read through the P6 contract |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | NoticeGenerated leaves P6 through its outbox on rwb.comms.events.v1 and DecisionRecorded on rwb.decision-record.v1; the suite reads both with its own inbox |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The nine consumed REST operations of section 12.2, each one hop with a 2 s timeout, a breaker and a single GET retry (BR14) |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | The P6 notice and template paths of section 12.2, and the P5, P3, P1 and P7 paths behind their own bases |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The notice table, its unique index on case_id, notice_type, person_key and the business date, and the state check are P6's own migration; the suite asserts the outcome through the contract and never the schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff and reads the same notice, document, case and ledger views the case documents and My work screens show; no screen is built here |

The dependency-added column records the build dependency of the owning APP and CON stories. This ITG story has no H, no C and no X, and it waits on no build of its own: its only declared dependencies are the seven APP stories in the I row, which must be deployed in SIT before the suite runs. An ITG story never blocks its own lane. Each schema named in the DP-01 row is owned by the service it is named for; this story owns none of them.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT bases of P6, P5, P3, P1 and P7 through gateway-bff.
2. Build the fixture pack — the two cases, the two persons, the four template states and the missing-ADDRESS case — and assert that no fixture carries a real personal value.
3. Seed the P1 data products DP01 Account and arrears and DP02 Customer and party for 2026-11-25 and 2026-11-24 and the proof-of-delivery row of 2026-11-27, and read them back through the P1 contract before any generation.
4. Implement AC1: the POST, the notice read, the document read, the ledger read within five minutes and the event read, and assert the footer string and the printed values.
5. Implement AC2 to AC6 and AC8 in TC order: the template refusal, the two holds, the local-record failure, the repeat request and the person refusal, asserting every status and message.
6. Implement AC7 through P1 freshness and the 2026-11-24 balance, keeping the legacy wording untouched, and assert the data date in the ledger entry.
7. Implement AC9 and AC11: the proof-of-delivery read through P1 with the notice row unchanged, and the role refusal at the contract edge with MSG-P4-002.
8. Implement AC10 with the P5 fault switch, assert the rollback, the correcting record and the single retry, then clear the switch.
9. Implement AC12: scan the two topics, the run logs and the merge snapshot reference for a name, an address, a national ID and an account number.
10. Write the evidence report, remove the fixtures, restore the clock and run the suite in SIT against the wave 1 release candidate.

Done when: all fourteen test cases pass in SIT against the published wave 1 contracts of P6, P5, P3, P1 and P7, the notice and its write-once PDF are read back through their owners, one D7.1 entry is visible through P7 within five minutes, every message is the legacy wording, no personal value appears in the event, the log or the snapshot, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The local decision record could not be written, or the decision could not be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE account batch is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-003 | The person is not on the case | This case is not in your scope. |
| MSG-P4-002 | The role lacks the Litigation right | You cannot {action} here. Your role does not include it. |

The message IDs and wording are copied from RWB-E1-052, except that the MSG-P1-001 wording is copied from Error and Message Standard v4 and MSG-P4-002 comes from the message catalog the legacy story cites for the role refusal. No new message ID is added by this story. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

No screen in this story, and no screen ID is invented. The generated notice shows on SCR-30 Case documents (states in the table below) as a generated document with its sent date, barcode and delivery status, and the hold tasks show on SCR-01 My work for the case owner or the litigation officer; both are read in this story and not built or tested. SCR-18 Notice approval, with the state Generated, comes in RWB-E2-014.

| State | What the user sees and does |
|---|---|
| Generated | The notice and its generated document are listed on the case with the footer, and the delivery facts appear when P1 holds a proof-of-delivery row |
| Held, POSTAL_ADDRESS | The notice is listed with the field that has no value, and the case owner has a "Complete notice data" task |
| Held, TEMPLATE_WITHDRAWN | The notice is listed with the withdrawn template, and the litigation officer team has a task |

SCR-30 states: Loading follows Screen Specifications v1 and the common Error state applies; Empty and No access are Not specified in the source documents (CG-ALL-346).

SCR-01 states: Empty and Loading follow Screen Specifications v1 and the common Error state applies; No access is Not specified in the source documents (CG-ALL-344). SCR-18 states: the common Loading and Error states apply; Empty and No access are Not specified in the source documents (CG-ALL-345). The suite reads the same states through the P6 and P3 contracts and takes no screenshot.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-01-ITG | AC1, BR1, BR4, BR5, BR7, BR9 | End to end | Case RW-2026-000123 Mortgage, person_key P-0001 with an ADDRESS row, DEMAND-MTG TH v2, 1,250,000.00 THB, data_as_of 2026-11-25; real services on the wave 1 contracts |
| TC-E1-052-02-ITG | AC2, BR1 | Integration | Case RW-2026-000456 Hire purchase, RECALL-HP TH v1 Draft; real services on the wave 1 contracts |
| TC-E1-052-03-ITG | AC3, BR3, BR9 | Integration | person_key P-0001 with no ADDRESS row in the P1 DP01 contact records; real services on the wave 1 contracts |
| TC-E1-052-04-ITG | AC4, BR2 | Integration | DEMAND-MTG TH v2 Withdrawn with no later Approved version; real services on the wave 1 contracts |
| TC-E1-052-05-ITG | AC5, BR6 | Integration | P6 local decision-record write forced to fail; real services on the wave 1 contracts |
| TC-E1-052-06-ITG | AC6, BR8 | Integration | The same request twice on 2026-11-25; real services on the wave 1 contracts |
| TC-E1-052-07-ITG | AC7, BR9 | End to end | No COMPLETED ALS row for 2026-11-25, DP01 STALE with business date 2026-11-24 after 08:00 on 2026-11-26, DP01 balance at 2026-11-24; real services on the wave 1 contracts |
| TC-E1-052-08-ITG | AC8 | Integration | person_key P-0999 not on case RW-2026-000123; real services on the wave 1 contracts |
| TC-E1-052-09-ITG | AC11, Access | Contract | A synthetic user without the Litigation right calls POST /cases/{caseId}/notices; refused with 403 and MSG-P4-002; real services on the wave 1 contracts |
| TC-E1-052-10-ITG | AC5, Principle 5 | NFR | The local decision-record write forced to fail during 20 generation attempts; no notice and no document stored in any attempt; real services on the wave 1 contracts |
| TC-E1-052-11-ITG | AC9, BR11 | End to end | Proof-of-delivery row POD-0001 (WIN date 2026-11-27) with notice_ref WIN-77001, sent_date 2026-11-27 and barcode RR123456789TH; a second notice with no proof-of-delivery row; real services on the wave 1 contracts |
| TC-ITG-E1052-ITG-12 | AC10 | Integration | The P5 document store set to exceed 2 s and return 503, then cleared for one retry; real services on the wave 1 contracts |
| TC-ITG-E1052-ITG-13 | AC11 | Contract | The same role refusal read on the notice read path with no data returned; real services on the wave 1 contracts |
| TC-ITG-E1052-ITG-14 | AC12 | End to end | A generated notice for RW-2026-000123 and person_key P-0001; scan of rwb.comms.events.v1, rwb.decision-record.v1, the run logs and the merge snapshot reference |
| TC-ITG-E1052-ITG-15 | AC13, BR10, BR12, BR13, BR14 | Contract | A generated notice for RW-2026-000123 and person_key P-0001; the merge snapshot of the D7.1 entry, the calls of the run, the table write ownership and the call settings of the consumed operations of section 12.2 |

The data of every case is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id; TC-ITG-E1052-ITG-12, -13, -14 and -15 are new in this run and are held with this story.

### 17. Guardrails

- No business value in code: notice types, templates, merge codes, task codes, the sent type mapping and the product groups are data or configuration read through the owner's contract.
- No personal data in events, logs, workflow inputs, prompts or the evidence report. The name and the address reach the PDF only. The event carries IDs and template version. The decision record holds a reference to the merge snapshot, and the snapshot holds the source system and column, the business key and the field ID of each value, never the value. AC12 proves it on the two topics, the run logs and the snapshot reference.
- ACE data only through the P1 data-product contract: the customer, the contact point, the balance, the delivery facts and the freshness stamp come from P1, and no service reads `recovery.v_ace_*` except P1 (DP-01, DP-05). The suite seeds P1 and never a view.
- The clear identity number never leaves ACE and is never merged into a notice; only `id_no_masked` and `id_no_last4` exist for a merge code.
- One hop and a 2 s timeout on every call, with a breaker per downstream and a single GET retry; a POST is retried only with the same Idempotency-Key (DP-11, DP-19; ADR-020).
- A generated PDF is write-once and is never overwritten; a correction is a new notice, and AC10 proves that a failed store leaves no orphan document.
- The local decision record and the notice commit together or not at all; the central ledger never blocks generation (DP-03, R-UNI-39).
- No production data, no production copy and no production connection of any kind from the suite or its configuration; the P5 fault switch, the P7 lag control and the clock control act on SIT only.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | The nine consumed REST operations of section 12.2, MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P7-003, MSG-P1-001, MSG-P4-003, MSG-P4-002 | TC-E1-052-01-ITG to TC-E1-052-11-ITG, TC-ITG-E1052-ITG-12 to TC-ITG-E1052-ITG-14 |
| DP-01 | Owner's schema; no service reads another service's tables | The five owners of section 12.7 and the nine contract reads | TC-E1-052-01-ITG, TC-E1-052-11-ITG, TC-ITG-E1052-ITG-14 |
| DP-03 | Local decision record plus the shared topic and the central ledger | The D7.1 entry through P7 and `DecisionRecorded` on `rwb.decision-record.v1` | TC-E1-052-01-ITG, TC-E1-052-05-ITG, TC-E1-052-10-ITG |
| DP-05 | ACE data through rwb-source-data's contract | The P1 reads of section 12.2 and MSG-P1-001 | TC-E1-052-01-ITG, TC-E1-052-03-ITG, TC-E1-052-07-ITG, TC-E1-052-11-ITG |
| DP-13 | Per-service REST base | The nine paths of section 12.2 under their owners' bases | TC-E1-052-01-ITG to TC-ITG-E1052-ITG-14 |
| DP-18 | Interaction ledger owned by P1 | The proof-of-delivery read writes no ledger entry; rwb-comms appends delivery entries; the suite writes no interaction | TC-E1-052-07-ITG, TC-E1-052-11-ITG |
| DP-19 | Screen through gateway-bff | The notice, document, case and ledger reads on the case documents and My work paths | TC-E1-052-01-ITG, TC-E1-052-11-ITG |
| ASM-0482 | P6 reads the ACE facts and the freshness stamp only through the P1 data-product contract | `GET /data-products/freshness`, `GET /data-products/{productCode}/records` and `GET /proof-of-delivery?businessDate=` | TC-E1-052-01-ITG, TC-E1-052-03-ITG, TC-E1-052-07-ITG, TC-E1-052-11-ITG |
| ASM-0483 | The merge snapshot stays in P6 as references only and the PDF is P5's write-once document | The notice read, the document read and the merge snapshot reference on the D7.1 entry | TC-E1-052-01-ITG, TC-ITG-E1052-ITG-14 |
| ASM-0484 | The local D7.1 record commits with the notice and the central entry follows within five minutes | `GET /decision-log?caseId=` and `DecisionRecorded` | TC-E1-052-01-ITG, TC-E1-052-05-ITG, TC-E1-052-10-ITG |
| ASM-0485 | The stale condition arrives through P1 freshness and keeps legacy AC7's outcome and message | `GET /data-products/freshness` and MSG-P1-001 | TC-E1-052-07-ITG |
| ASM-0486 | Generation is the P6 notice POST and the read is the P6 notice GET, with the legacy idempotency key | `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` | TC-E1-052-01-ITG, TC-E1-052-02-ITG, TC-E1-052-06-ITG |

The legacy AC1 to AC6, AC8 and AC9 sit at component level with RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP and RWB-P7-E1052-APP. AC7 is the one legacy criterion this story keeps, and it is proved end to end through P1, P6 and P7.

### 19. Out of scope

- The APP builds and their unit and component tests (RWB-P6-E1052-APP, RWB-P5-E1052-APP, RWB-P3-E1052-APP, RWB-P7-E1052-APP, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P3-E1018-APP).
- The CON stories those builds use, including the decision-record library, the outbox and inbox library, the reference-data contract and the gateway route.
- Dispatch to WIN and proof-of-delivery capture (RWB-E1-055); this story reads the delivery facts through P1 and writes none.
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5).
- Contract, credit approval and mortgage documents (RWB-E2-026).
- The build of the harness RWB-ITG-W1J01-ITG and the P1 contract baseline.
- NFR load and performance testing beyond the single timeout and rollback case (RWB-ITG-NFR).

### Remaining delivery steps

- rwb-source-data contracts (records, freshness, proof-of-delivery) Done and published: owner rwb-source-data service owner.
- Masking rule rows that unmask `firstName`, `lastName` and `contactValue` for the rwb-comms notice workload identity (NEW-GAP-D1): owner data protection officer with the rwb-access owner.
- Test Cases and RTM rows for AC1, AC3, AC7 and AC9: owner QA.
- Synthetic case uuid, DP01, DP02 and proof-of-delivery data loaded in SIT: owner QA integration engineer.
- Size and epic design sign-off: owner squad and Solution architect.
