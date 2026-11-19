# RWB-E1-052 Notice generation v1

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-052 |
| Epic | E1, release 30 November 2026 |
| Module | P6 Communications |
| Feature | FEAT-DRI-14 Generate notices from approved templates to WIN |
| Requirement IDs | REQ-OCC-001 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
| L3 process | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence |
| Decision | D7.1; D-RCV-35 (U1, U4); ADR-010; DL43 open |
| Priority | Must |
| Depends on | RWB-E1-015, RWB-E1-018, RWB-E1-027, RWB-E1-046, RWB-E1-069 |
| Status | Ready for build, proof of delivery behind a flag until RWB-ACE-001 lands (DL43) |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **demand, recall and guarantor notices generated from the Legal-approved template with the case data merged, the party and the notice address read from the ACE views by business key**, so that **letters are produced without re-keying and the address on the notice is the address ACE holds**.

## 2. Business rationale

Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. Under D-RCV-35 the Workbench holds no party and no contact point: the name comes from `v_ace_customer` by `person_key`, the notice address and phone come from `v_ace_contact` by the composite `contact_key` (`contact_type:key`), and the outstanding comes from `v_ace_account` by `account_key`. The clear identity number never leaves ACE, so it is never merged. This story merges those values into the current approved template, stores the PDF write-once on the case with the template version in the footer and records the decision. It serves REQ-OCC-001 and control CTL-14, and is the input to dispatch and proof of delivery (RWB-E1-055), where the WIN record is read from `v_ace_pod`. The FSD P6 measure "notices with proof of delivery, 100 percent" depends on it.

## 3. Preconditions

- RWB-E1-046 is done: TemplateCatalog returns the current Approved version.
- RWB-E1-018 is done: cases exist with `person_key` links on case_party.
- RWB-E1-027 is done: the decision log writer accepts D7.1 entries.
- RWB-E1-015 is done: each data product carries its freshness stamp from the ACE batch.
- RWB-E1-069 is done: `v_ace_customer`, `v_ace_contact` and `v_ace_account` are Section A views. `v_ace_pod` is a Section B view over `public.pod_receipt`, so the delivery facts stay behind their flag until RWB-ACE-001 lands (DL43).
- Templates for DEMAND, RECALL and GUARANTOR_NOTICE are Approved for the product groups in the synthetic set, in language TH.
- The customer, the contact points and the account are in ACE (SCBPDM and ALS ingestion); `recovery_svc` holds SELECT on `recovery.v_ace_*` and no privilege on `public`.
- The caller is `recovery_svc`, or a person through RWB-E2-021 from Epic 2.

## 4. Flow

1. Caller: calls NoticeApi.generate with case ID, notice type, `person_key` and language.
2. System: reads the case summary (case number, product group, status) through the P3 interface and the party role through `case_party` by `person_key`.
3. System: asks TemplateCatalog for the current LETTER template for the notice type, product group and language on the business date.
4. System: resolves each merge code through the interface that owns its source field: `CASE_NO`, `PRODUCT_GROUP` and `ENTRY_DATE` from P3; `CUSTOMER_NAME` from `v_ace_customer.first_name` and `.last_name` by `person_key`; `POSTAL_ADDRESS` and `PHONE` from `v_ace_contact` by `person_key` and `contact_type`; `TOTAL_OUTSTANDING` from `v_ace_account.total_balance` by the case's primary `account_key`. Each value carries the ACE business date of its view or batch.
5. System: if a required merge value is empty, holds the notice, names the field and raises a task to the case owner; stops.
6. System: renders the DOCX template to PDF and adds the footer: case number, template code, template version and generation date.
7. System: writes the D7.1 decision log entry with rule R-LIT-03, the template code and version and the reference to the merge snapshot. The snapshot holds the merge code, the view column, the business key and the field ID of each value used, never the value.
8. System: stores the PDF in the document hub as a generated, write-once document on the case.
9. System: creates the notice row with `person_key`, `template_id`, notice type, sent type and state Generated, and writes NoticeGenerated to the outbox in the same transaction.
10. System: when the notice is read, takes the sent date, barcode, callback date and delivery status from `v_ace_pod` by `notice_ref`. The Workbench writes no WIN delivery fact of its own.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The template has no Approved version | Refused; no notice and no document created | MSG-P6-005 | AC2 |
| X2 | A required merge value is empty, for example no ADDRESS row in `v_ace_contact` for the person | Notice held with the field named; task to the case owner | MSG-P6-007 | AC3 |
| X3 | The current version is withdrawn | Notice held; task to the litigation officer | MSG-P6-003 | AC4 |
| X4 | The decision log write fails | Nothing stored; incident raised | MSG-P7-003 | AC5 |
| X5 | The same request arrives twice on one business date | The first notice is returned; no second notice | None | AC6 |
| X6 | The ACE account batch is stale | Generation proceeds with the ACE business date shown; the decision log entry records it | MSG-P1-001 | AC7 |
| X7 | The person is not on the case | Refused | MSG-P4-003 | AC8 |
| X8 | `v_ace_pod` holds no row for the notice reference | The notice shows as generated with no delivery confirmation; the delivery matcher of RWB-E1-055 lists it | None | TC-E1-052-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the catalog (RWB-E1-046), the case links (RWB-E1-018), the ACE views (RWB-E1-069) and the decision log writer (RWB-E1-027); no screen and no dispatch |
| Negotiable | Which notice types and products have templates is data; the merge and the checks are fixed |
| Valuable | Ends re-keying of demand, recall and guarantor notices, and the address is the one ACE holds |
| Estimable | One service, one renderer, one published interface, four view reads |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion is a service test with synthetic cases, templates and view rows |

## 7. Acceptance criteria

```gherkin
Feature: Notice generation v1

  Background:
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RW-2026-000123" has product group "MORTGAGE" and borrower person_key "P-0001"
    Given v_ace_account holds the case's primary account_key with total_balance 1,250,000.00 and data_as_of 2026-11-25
    Given the business date is 2026-11-25

  Scenario: AC1 Generated
    Given v_ace_customer holds person_key "P-0001" with first_name "Anan" and last_name "Sukjai"
    Given v_ace_contact holds an ADDRESS row for "P-0001" with contact_key "ADDRESS:A-9001" and contact_value "88/1 Bangkok"
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND", person_key "P-0001" and language "TH"
    Then the system stores a PDF on the case with source "GENERATED" and write_once true
    Then the PDF shows "RW-2026-000123", the customer name and 1,250,000.00 THB
    Then the footer reads "RW-2026-000123 DEMAND-MTG v2 2026-11-25"
    Then a notice row exists with notice_type "DEMAND", sent_type "NPL", person_key "P-0001", template_id and state "Generated"
    Then one decision log entry exists with decision code "D7.1", rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference
    Then the system writes noticeGenerated to the outbox with the notice ID and template version 2

  Scenario: AC2 Template approval checked
    Given template "RECALL-HP" "TH" has only version 1 in state "Draft"
    Given case "RW-2026-000456" has product group "HIRE_PURCHASE"
    When NoticeApi.generate is called for case "RW-2026-000456", notice type "RECALL" and language "TH"
    Then the system refuses it with MSG-P6-005 naming "RECALL-HP" version 1
    Then no notice row and no document are created

  Scenario: AC3 Missing field
    Given v_ace_contact holds no ADDRESS row for person_key "P-0001"
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND" and person_key "P-0001"
    Then a notice row exists in state "Held" with hold_reason "POSTAL_ADDRESS"
    Then the system stores no document
    Then the system raises a task "Complete notice data" to the case owner of "RW-2026-000123" with MSG-P6-007 naming "POSTAL_ADDRESS"

  Scenario: AC4 Withdrawn template holds the notice
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then a notice row exists in state "Held" with hold_reason "TEMPLATE_WITHDRAWN"
    Then the system raises a task to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC5 Decision log write fails
    Given the decision log store is unavailable
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then the call fails with MSG-P7-003
    Then no notice row and no document are created
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC6 Repeated request on the same business date
    Given a notice for case "RW-2026-000123", notice type "DEMAND", person_key "P-0001" was generated on 2026-11-25
    When NoticeApi.generate is called again with the same values on 2026-11-25
    Then the system returns the existing notice
    Then the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC7 Stale ACE account batch
    Given v_ace_batch_status holds no COMPLETED ALS row for 2026-11-25 and v_ace_account.data_as_of is 2026-11-24
    When NoticeApi.generate is called for case "RW-2026-000123", notice type "DEMAND"
    Then the system generates the notice from the 2026-11-24 balance
    Then the decision log entry records data date 2026-11-24
    Then the result carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24

  Scenario: AC8 Person not on the case
    Given person_key "P-0999" is not a party on case "RW-2026-000123"
    When NoticeApi.generate is called with person_key "P-0999"
    Then the system refuses it with MSG-P4-003

  Scenario: AC9 Proof of delivery read from ACE
    Given notice "N-0001" on case "RW-2026-000123" has notice_ref "WIN-77001"
    Given v_ace_pod holds pod_key "POD-0001" with notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED"
    When an officer reads notice "N-0001" through GET /cases/{caseId}/notices
    Then the notice shows sent date 2026-11-27, barcode "RR123456789TH" and status "DELIVERED" from v_ace_pod
    Then the notice row is unchanged
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A notice is generated only from the current Approved template for its notice type, product group and language | R-LIT-03; CTL-14 |
| BR2 | A withdrawn template holds generation and raises a task to the litigation officer | R-LIT-04 |
| BR3 | A required merge value that is empty holds the notice, names the field and raises a task to the case owner | merge_field.is_required; pattern of R-RES-36 |
| BR4 | The footer carries the case number, template code, template version and generation date | REQ-OCC-001; CTL-14 evidence |
| BR5 | The generated PDF is a write-once document on the case | CTL-12; DT06 |
| BR6 | A notice that cannot be written to the decision log is not generated | Principle 5; R-UNI-39; CTL-06 |
| BR7 | Sent type is NPL for a case at 90 days past due or more | LOV-SENT-TYPE; DL16 |
| BR8 | One notice per case, notice type, `person_key` and business date | R-UNI-40; notice.person_key (DF-LEG-030) |
| BR9 | The party, the customer name and the notice address are read from `v_ace_customer` and `v_ace_contact` by `person_key` and the composite `contact_key` (`contact_type:key`). The Workbench holds no party or contact copy | D-RCV-35 U4; ADR-010; Data Tier Map section 5 |
| BR10 | A merge code resolves to a view column or a P3 or P5 field. The clear `identification_number` is never a merge source because it never leaves ACE; `v_ace_customer` exposes `id_no_masked` and `id_no_last4` only | ADR-010; Data Tier Map section 7; DF-ACE-073 |
| BR11 | Proof of delivery is read from `v_ace_pod` by `notice_ref`; the Workbench writes no WIN delivery fact | Data Tier Map section 3; RWB-E1-055 |
| BR12 | The merge snapshot holds the merge code, the view column, the business key and the field ID of each value used, never the value | NFR-040; guardrail on personal data |

## 9. State transitions

None. This story does not change a case status. It sets the notice state (standard column state):

| From | Event | Condition | To |
|---|---|---|---|
| None | Generate | Template Approved and all required merge values present | Generated |
| None | Generate | A required merge value empty | Held |
| None | TEMPLATE_WITHDRAWN | Template state Withdrawn | Held |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Calls NoticeApi.generate (Litigation R, Documents R); reads `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod`; SELECT only |
| SY-DECLOG, decision log writer | Writes the D7.1 entry |
| RW-LITOFF, litigation officer | Reads the notice and the document (Litigation CRUA, Documents CRU); receives the task on a withdrawn template |
| RW-CASEOWN, case owner | Reads the notice (Litigation R) and receives the task on missing data |
| RW-LEGAL, Legal counsel | Reads the notice (Litigation RA) |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod` |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | person_key | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-057 | v_ace_customer | first_name | Read |
| DF-ACE-058 | v_ace_customer | last_name | Read |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read; never merged in clear |
| DF-ACE-074 | v_ace_customer | id_no_last4 | Read; never merged in clear |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read, composite `contact_type:key` |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | Read, the notice address and phone |
| DF-ACE-081 | v_ace_contact | city | Read |
| DF-ACE-082 | v_ace_contact | post_code | Read |
| DF-ACE-083 | v_ace_contact | country | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-251 | v_ace_pod | pod_key | Read |
| DF-ACE-253 | v_ace_pod | notice_ref | Read |
| DF-ACE-254 | v_ace_pod | sent_date | Read |
| DF-ACE-255 | v_ace_pod | barcode | Read |
| DF-ACE-256 | v_ace_pod | callback_date | Read |
| DF-ACE-257 | v_ace_pod | delivery_status | Read |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-050 | template | body_ref | Read |
| DF-REF-253 | merge_field | merge_code | Read |
| DF-REF-254 | merge_field | source_entity | Read |
| DF-REF-255 | merge_field | source_field | Read |
| DF-REF-257 | merge_field | is_required | Read |
| DF-DOC-001 to DF-DOC-011 | document | all fields, written through the document hub interface | Write |
| DF-LEG-015 | notice | id | Write |
| DF-LEG-016 | notice | case_id | Write |
| DF-LEG-017 | notice | document_id | Write |
| DF-LEG-018 | notice | notice_type | Write |
| DF-LEG-023 | notice | sent_type | Write |
| DF-LEG-030 | notice | person_key | Write |
| DF-LEG-031 | notice | template_id | Write |
| DF-LEG-032 | notice | hold_reason | Write |
| Standard column | notice | state | Write |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary v7. DF-ACE-* are the `recovery.v_ace_*` view fields of Physical Schema v6.

## 12. Contract

No endpoint in Epic 1. POST /api/recovery/v1/cases/{caseId}/notices calls the same service from RWB-E2-021.

**Published interface NoticeApi** (P6)

```java
public interface NoticeApi {
    NoticeResult generate(NoticeGenerationRequest request)
        throws TemplateNotApprovedException, PartyNotOnCaseException, DecisionNotRecordedException;
}
public record NoticeGenerationRequest(UUID caseId, String noticeType, String personKey,
                                      String language, UUID requestedBy, LocalDate businessDate) {}
public record NoticeResult(UUID noticeId, String state, UUID documentId, String holdReason,
                           int templateVersion, List<String> messageCodes) {}
```

Calls out of the module, each through the owner's published interface:

```java
CaseSummary CaseWorkflowApi.getCaseSummary(UUID caseId);                       // P3
List<CasePartyView> CaseWorkflowApi.getCaseParties(UUID caseId);               // P3
UUID CaseWorkflowApi.raiseTask(UUID caseId, String taskCode, String ownerRole, String reasonCode); // P3
// P1, RWB-E1-016; every method reads recovery.v_ace_*
Optional<AceCustomerView> AceSourceQuery.customer(String personKey);           // v_ace_customer
List<AceContactView> AceSourceQuery.contacts(String personKey, String contactType); // v_ace_contact
Optional<AceAccountView> AceSourceQuery.account(String accountKey);            // v_ace_account
Optional<AcePodView> AceSourceQuery.podForNotice(String noticeRef);            // v_ace_pod, Tier 2
DocumentRef DocumentHubApi.storeGenerated(UUID caseId, String personKey, String documentType, byte[] pdf); // P5
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException;    // P7
```

| Item | Value |
|---|---|
| Event published | NoticeGenerated (EV-13): noticeId, caseId, type, templateVersion, written to the outbox in the same transaction |
| Idempotency key | caseId, noticeType, personKey and business date (unique index) |
| Order of writes | Decision log entry first, then document, notice row and outbox in one transaction; a failed document store rolls back the notice and the decision log entry is followed by a correcting entry under R-UNI-24 |

## 13. Solution plan

- Package: folder `recovery/comms/notices`, Java package `recovery.comms.notices`.

| Component | Type | Responsibility |
|---|---|---|
| NoticeEntity | Entity | Maps table notice with the new columns |
| NoticeRepository | Repository | Reads and writes notice; finds by the idempotency key |
| NoticeGenerationService | Published interface | Implements NoticeApi: steps 2 to 9 of the flow |
| MergeValueResolver | Service | For each merge code, calls the P3, P1 or P5 interface named by merge_field.source_entity and reads the view column named by merge_field.source_field |
| AceSourceReader | Repository | Reads `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod` by business key; SELECT only |
| LetterRenderer | Service | Fills the DOCX body and renders PDF with the footer |
| NoticeGeneratedPublisher | Service | Writes NoticeGenerated to the outbox |

- Database: table notice (Physical Schema v6) carries `person_key`, `template_id` and `hold_reason`; this story adds unique index ux_notice_generation on (case_id, notice_type, person_key, (created_at::date)) and the check constraint on state in ('GENERATED','HELD','APPROVED','SENT','DELIVERED','UNSERVED'). Flyway migration `V1_052__notice_generation.sql` adds the index and the check. No party or contact copy is added.
- Configuration and reference data: templates and merge field catalog (RWB-E1-046, Legal counsel); LOV-NOTICE, LOV-SENT-TYPE; LOV-DOC-TYPE value for a generated notice from the document checklist (data steward); task code "Complete notice data" as a task row of the case model (center of excellence). The renderer uses the ACE document rendering library, or docx4j with PDF export where ACE has none (dependency approval under NFR-054).
- Build steps:
  1. Write the migration and NoticeEntity; test the unique index and the state check.
  2. Build AceSourceReader over the four views by `person_key`, `contact_key` and `account_key`; test the reads and the missing rows.
  3. Build MergeValueResolver with the view columns and the P3 fields; test every merge code in the synthetic catalog and the empty required value.
  4. Build LetterRenderer; test the merged text and the footer of AC1 from a synthetic DOCX.
  5. Build NoticeGenerationService with the template check, hold paths and task raise; test AC2, AC3, AC4, AC8.
  6. Add the decision log write before the document store and the rollback path; test AC5.
  7. Add the idempotency key and the stale data handling; test AC6 and AC7.
  8. Add the outbox write of NoticeGenerated and the proof of delivery read; test AC1 and AC9.
- Feature flag: `rwb.comms.notice-generation`. Proof of delivery reads a Section B view, so that part is on only after RWB-ACE-001 lands and V0003 creates `v_ace_pod` (DL43).
- Done when: the tests in section 16 pass, and a generated PDF from the synthetic set opens in a standard PDF reader with Thai text rendered.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE account batch is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-003 | The person is not on the case | This case is not in your scope. |

## 15. Screens and states

No screen in this story. The generated notice shows on SCR-30 Case documents (state list) as a generated document, with its sent date, barcode and delivery status read from `v_ace_pod`, and the task on SCR-01 My work for the case owner or litigation officer. SCR-18 Notice approval, with the state Generated, comes in RWB-E2-014.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-01 | AC1, BR1, BR4, BR5, BR7, BR9 | System | RW-2026-000123 Mortgage, P-0001 with an ADDRESS row in `v_ace_contact`, DEMAND-MTG TH v2 |
| TC-E1-052-02 | AC2, BR1 | System | RW-2026-000456 Hire purchase, RECALL-HP TH v1 Draft |
| TC-E1-052-03 | AC3, BR3, BR9 | System | P-0001 with no ADDRESS row in `v_ace_contact` |
| TC-E1-052-04 | AC4, BR2 | System | DEMAND-MTG TH v2 Withdrawn |
| TC-E1-052-05 | AC5, BR6 | System | Decision log store stubbed unavailable |
| TC-E1-052-06 | AC6, BR8 | System | Same request twice on 2026-11-25 |
| TC-E1-052-07 | AC7, BR9 | System | No COMPLETED ALS row for 2026-11-25, `data_as_of` 2026-11-24 |
| TC-E1-052-08 | AC8 | System | P-0999 not on the case |
| TC-E1-052-09 | Access | Access | Service identity without Litigation R calls NoticeApi.generate; refused with MSG-P4-002 |
| TC-E1-052-10 | Principle 5 | Resilience | Decision log write forced to fail during generation of 20 notices; none stored |
| TC-E1-052-11 | AC9, BR11 | System | `v_ace_pod` row POD-0001 with notice_ref WIN-77001, and a notice with no `v_ace_pod` row |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: notice types, templates, merge codes, task codes and the sent type mapping are data.
- No personal data in logs, tests or prompts. The name and address reach the PDF only; the decision log holds a reference to the merge snapshot, and the snapshot holds the view column, the business key and the field ID of each value, never the value.
- ACE data only through the `recovery.v_ace_*` views: the customer, the contact point, the account balance and the delivery facts come from `v_ace_customer`, `v_ace_contact`, `v_ace_account` and `v_ace_pod`. The recovery schema holds no foreign key into a `public` table.
- The clear identity number never leaves ACE and is never merged into a notice.
- The generated PDF is never overwritten; a correction is a new notice.
- PII Kafka receives one access event per personal field read, through RWB-E1-039.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 | TC-E1-052-01 to TC-E1-052-11 |
| D-RCV-35 U4 | The party, the address and the balance are read by business key from the `recovery.v_ace_*` views, and delivery comes from `v_ace_pod` | Decision log, D-RCV-35 section 6.1; ADR-010 | FEAT-DRI-14 | 8.1 Prepare pre-litigation | BR9, BR11; ADR-010 | TC-E1-052-01, TC-E1-052-03, TC-E1-052-11 |

## 19. Out of scope

- Dispatch to WIN and proof of delivery capture (RWB-E1-055, RWB-E2-021); the delivery facts are read from `v_ace_pod`.
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5, DL24).
- Contract, credit approval and mortgage documents (RWB-E2-026).
