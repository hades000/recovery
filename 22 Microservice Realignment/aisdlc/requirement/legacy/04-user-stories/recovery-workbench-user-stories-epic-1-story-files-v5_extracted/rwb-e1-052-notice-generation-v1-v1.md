<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 052 Notice generation v1 v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 052 Notice generation v1 v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-052 Notice generation v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-015, RWB-E1-027, RWB-E1-046 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **demand, recall and guarantor notices generated from the Legal-approved template with the case data merged**, so that **letters are produced without re-keying**.

## 2. Business rationale

Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. This story merges the case facts into the current approved template, stores the PDF write-once on the case with the template version in the footer and records the decision. It serves REQ-OCC-001 and control CTL-14, and is the input to dispatch and proof of delivery (RWB-E1-055), which the FSD P6 measure "notices with proof of delivery, 100 percent" depends on.

## 3. Preconditions

- RWB-E1-046 is done: TemplateCatalog returns the current Approved version.
- RWB-E1-027 is done: the decision log writer accepts D7.1 entries.
- RWB-E1-015 is done: each data product carries its freshness stamp.
- Templates for DEMAND, RECALL and GUARANTOR_NOTICE are Approved for the product groups in the synthetic set, in language TH.
- The case exists with its parties and contact points loaded through COLLINS (DP02, DP03).
- The caller is SY-CASEWF, or a person through RWB-E2-021 from Epic 2.

## 4. Flow

1. Caller: calls NoticeApi.generate with case ID, notice type, party ID and language.
2. System: reads the case summary (case number, product group, status) through the P3 interface and the party role through the case parties.
3. System: asks TemplateCatalog for the current LETTER template for the notice type, product group and language on the business date.
4. System: resolves each merge code of the template through the interface of the module that owns its source field, and detokenizes personal values through the ACE PII service, which writes the access to PII Kafka.
5. System: if a required merge value is empty, holds the notice, names the field and raises a task to the case owner; stops.
6. System: renders the DOCX template to PDF and adds the footer: case number, template code, template version and generation date.
7. System: writes the D7.1 decision log entry with rule R-LIT-03, the template code and version and the reference to the merge snapshot.
8. System: stores the PDF in the document hub as a generated, write-once document on the case.
9. System: creates the notice row in state Generated with the document ID, notice type and sent type, and writes NoticeGenerated to the outbox in the same transaction.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The template has no Approved version | Refused; no notice and no document created | MSG-P6-005 | AC2 |
| X2 | A required merge value is empty, for example no postal address | Notice held with the field named; task to the case owner | MSG-P6-007 | AC3 |
| X3 | The current version is withdrawn | Notice held; task to the litigation officer | MSG-P6-003 | AC4 |
| X4 | The decision log write fails | Nothing stored; incident raised | MSG-P7-003 | AC5 |
| X5 | The same request arrives twice on one business date | The first notice is returned; no second notice | None | AC6 |
| X6 | The account data product is stale | Generation proceeds with the data date shown; the decision log entry records it | MSG-P1-001 | AC7 |
| X7 | The party is not on the case | Refused | MSG-P4-003 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the catalog (RWB-E1-046) and the decision log writer (RWB-E1-027); no screen and no dispatch |
| Negotiable | Which notice types and products have templates is data; the merge and the checks are fixed |
| Valuable | Ends re-keying of demand, recall and guarantor notices |
| Estimable | One service, one renderer, one published interface |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion is a service test with synthetic cases and templates |

## 7. Acceptance criteria

```gherkin
Feature: Notice generation v1

  Background:
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RC-2026-000123" has product group "MORTGAGE", borrower party "P-0001" and total balance 1,250,000.00 THB
    Given the business date is 2026-11-25

  Scenario: AC1 Generated
    Given party "P-0001" has a postal address contact point
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND", party "P-0001" and language "TH"
    Then the system stores a PDF on the case with source "GENERATED" and write_once true
    Then the PDF shows "RC-2026-000123" and 1,250,000.00 THB
    Then the footer reads "RC-2026-000123 DEMAND-MTG v2 2026-11-25"
    Then a notice row exists with notice type "DEMAND", sent type "NPL", the document ID and state "Generated"
    Then one decision log entry exists with decision code "D7.1", rule "R-LIT-03" and template "DEMAND-MTG" version 2
    Then the system writes noticeGenerated to the outbox with the notice ID and template version 2

  Scenario: AC2 Template approval checked
    Given template "RECALL-HP" "TH" has only version 1 in state "Draft"
    Given case "RC-2026-000456" has product group "HIRE_PURCHASE"
    When NoticeApi.generate is called for case "RC-2026-000456", notice type "RECALL" and language "TH"
    Then the system refuses it with MSG-P6-005 naming "RECALL-HP" version 1
    Then no notice row and no document are created

  Scenario: AC3 Missing field
    Given party "P-0001" on case "RC-2026-000123" has no postal address contact point
    When NoticeApi.generate is called for notice type "DEMAND"
    Then a notice row exists in state "Held" with hold reason "POSTAL_ADDRESS"
    Then the system stores no document
    Then the system raises a task "Complete notice data" to the case owner of "RC-2026-000123" with MSG-P6-007 naming "POSTAL_ADDRESS"

  Scenario: AC4 Withdrawn template holds the notice
    Given template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then a notice row exists in state "Held" with hold reason "TEMPLATE_WITHDRAWN"
    Then the system raises a task to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC5 Decision log write fails
    Given the decision log store is unavailable
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then the call fails with MSG-P7-003
    Then no notice row and no document are created
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC6 Repeated request on the same business date
    Given a notice for case "RC-2026-000123", notice type "DEMAND", party "P-0001" was generated on 2026-11-25
    When NoticeApi.generate is called again with the same values on 2026-11-25
    Then the system returns the existing notice
    Then the case still has one DEMAND notice and one generated document for 2026-11-25

  Scenario: AC7 Stale account data
    Given the account data product is from 2026-11-24 because the 2026-11-25 load has not arrived
    When NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND"
    Then the system generates the notice from the 2026-11-24 data
    Then the decision log entry records data date 2026-11-24
    Then the result carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24

  Scenario: AC8 Party not on the case
    Given party "P-0999" is not a party on case "RC-2026-000123"
    When NoticeApi.generate is called with party "P-0999"
    Then the system refuses it with MSG-P4-003
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
| BR8 | One notice per case, notice type, party and business date | R-UNI-40 |

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
| SY-CASEWF, case workflow module | Calls NoticeApi.generate (Litigation R, Documents R) |
| SY-DECLOG, decision log writer | Writes the D7.1 entry |
| RW-LITOFF, litigation officer | Reads the notice and the document (Litigation CRUA, Documents CRU); receives the task on a withdrawn template |
| RW-CASEOWN, case owner | Reads the notice (Litigation R) and receives the task on missing data |
| RW-LEGAL, Legal counsel | Reads the notice (Litigation RA) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | party_id | Read |
| DF-CAS-033 | case_party | party_role | Read |
| DF-PTY-004 | party | first_name | Read |
| DF-PTY-005 | party | last_name | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-016 | contact_point | value_token | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
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
| Standard column | notice | state | Write |
| DF-LEG-030 | notice | party_id | Write |
| DF-LEG-031 | notice | template_id | Write |
| DF-LEG-032 | notice | hold_reason | Write |
| DF-WRK-019 | task | task_code | Write, through the P3 interface |
| DF-WRK-023 | task | owner_role | Write, through the P3 interface |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

No endpoint in Epic 1. POST /api/recovery/v1/cases/{caseId}/notices calls the same service from RWB-E2-021.

**Published interface NoticeApi** (P6)

```java
public interface NoticeApi {
    NoticeResult generate(NoticeGenerationRequest request)
        throws TemplateNotApprovedException, PartyNotOnCaseException, DecisionNotRecordedException;
}
public record NoticeGenerationRequest(UUID caseId, String noticeType, UUID partyId,
                                      String language, UUID requestedBy, LocalDate businessDate) {}
public record NoticeResult(UUID noticeId, String state, UUID documentId, String holdReason,
                           int templateVersion, List<String> messageCodes) {}
```

Calls out of the module, each through the owner's published interface:

```java
CaseSummary CaseWorkflowApi.getCaseSummary(UUID caseId);                       // P3
List<CasePartyView> CaseWorkflowApi.getCaseParties(UUID caseId);               // P3
UUID CaseWorkflowApi.raiseTask(UUID caseId, String taskCode, String ownerRole, String reasonCode); // P3
List<ContactPointView> PartyApi.contactPoints(UUID partyId, String channel);    // P1
AccountBalanceView RecoveryDataApi.caseBalance(UUID caseId);                   // P1, carries data_as_of
DocumentRef DocumentHubApi.storeGenerated(UUID caseId, UUID partyId, String documentType, byte[] pdf); // P5
DecisionLogRef DecisionLogApi.write(DecisionLogRequest request) throws DecisionLogWriteException;    // P7
```

| Item | Value |
|---|---|
| Event published | NoticeGenerated (EV-13): noticeId, caseId, type, templateVersion, written to the outbox in the same transaction |
| Idempotency key | caseId, noticeType, partyId and business date (unique index) |
| Order of writes | Decision log entry first, then document, notice row and outbox in one transaction; a failed document store rolls back the notice and the decision log entry is followed by a correcting entry under R-UNI-24 |

## 13. Solution plan

- Package: folder `recovery/comms/notices`, Java package `recovery.comms.notices`.

| Component | Type | Responsibility |
|---|---|---|
| NoticeEntity | Entity | Maps table notice with the new columns |
| NoticeRepository | Repository | Reads and writes notice; finds by the idempotency key |
| NoticeGenerationService | Published interface | Implements NoticeApi: steps 2 to 9 of the flow |
| MergeValueResolver | Service | For each merge code, calls the owning module interface named by merge_field.source_entity; detokenizes personal values through the ACE PII service |
| LetterRenderer | Service | Fills the DOCX body and renders PDF with the footer |
| NoticeGeneratedPublisher | Service | Writes NoticeGenerated to the outbox |

- Database: table notice (Recovery Workbench Physical Schema v4.sql) gets party_id uuid, template_id uuid and hold_reason varchar(30); unique index ux_notice_generation on (case_id, notice_type, party_id, (created_at::date)); check constraint on state in ('GENERATED','HELD','APPROVED','SENT','DELIVERED','UNSERVED'). Flyway migration `V1_052__notice_generation.sql` alters the existing table.
- Configuration and reference data: templates and merge field catalog (RWB-E1-046, Legal counsel); LOV-NOTICE, LOV-SENT-TYPE; LOV-DOC-TYPE value for a generated notice from the document checklist (data steward); task code "Complete notice data" as a task row of the case model (center of excellence). The renderer uses the ACE document rendering library, or docx4j with PDF export where ACE has none (dependency approval under NFR-054).
- Build steps:
  1. Write the migration and NoticeEntity; test the unique index and the state check.
  2. Build MergeValueResolver with stub interfaces; test every merge code in the synthetic catalog and the empty required value.
  3. Build LetterRenderer; test the merged text and the footer of AC1 from a synthetic DOCX.
  4. Build NoticeGenerationService with the template check, hold paths and task raise; test AC2, AC3, AC4, AC8.
  5. Add the decision log write before the document store and the rollback path; test AC5.
  6. Add the idempotency key and the stale data handling; test AC6 and AC7.
  7. Add the outbox write of NoticeGenerated; test AC1 end to end.
- Feature flag: `rwb.comms.notice-generation`.
- Done when: the tests in section 16 pass, and a generated PDF from the synthetic set opens in a standard PDF reader with Thai text rendered.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The account data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-003 | The party is not on the case | This case is not in your scope. |

## 15. Screens and states

No screen in this story. The generated notice shows on SCR-30 Case documents (state list) as a generated document, and the task on SCR-01 My work for the case owner or litigation officer. SCR-18 Notice approval, with the state Generated, comes in RWB-E2-014.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-01 | AC1, BR1, BR4, BR5, BR7 | System | RC-2026-000123 Mortgage, P-0001 with postal address, DEMAND-MTG TH v2 |
| TC-E1-052-02 | AC2, BR1 | System | RC-2026-000456 Hire purchase, RECALL-HP TH v1 Draft |
| TC-E1-052-03 | AC3, BR3 | System | P-0001 with no postal address |
| TC-E1-052-04 | AC4, BR2 | System | DEMAND-MTG TH v2 Withdrawn |
| TC-E1-052-05 | AC5, BR6 | System | Decision log store stubbed unavailable |
| TC-E1-052-06 | AC6, BR8 | System | Same request twice on 2026-11-25 |
| TC-E1-052-07 | AC7 | System | Account product dated 2026-11-24 |
| TC-E1-052-08 | AC8 | System | P-0999 not on the case |
| TC-E1-052-09 | Access | Access | Service identity without Litigation R calls NoticeApi.generate; refused with MSG-P4-002 |
| TC-E1-052-10 | Principle 5 | Resilience | Decision log write forced to fail during generation of 20 notices; none stored |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: notice types, templates, merge codes, task codes and the sent type mapping are data.
- No personal data in logs, tests or prompts. Names and addresses are detokenized only into the PDF; the decision log holds a reference to the merge snapshot, and the snapshot stores tokens, never clear values.
- No read of another module's tables. Case, party, account, task, document and decision log are reached through their published interfaces.
- The generated PDF is never overwritten; a correction is a new notice.
- PII Kafka receives one access event per detokenized field, through the ACE PII service.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 | TC-E1-052-01 to TC-E1-052-10 |

## 19. Out of scope

- Dispatch to WIN and proof of delivery (RWB-E1-055, RWB-E2-021).
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5, DL24).
- Contract, credit approval and mortgage documents (RWB-E2-026).
