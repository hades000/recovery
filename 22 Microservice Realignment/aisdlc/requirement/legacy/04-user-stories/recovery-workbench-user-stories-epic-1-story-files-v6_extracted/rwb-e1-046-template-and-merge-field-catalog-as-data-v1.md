<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 046 Template and merge field catalog as data v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 046 Template and merge field catalog as data v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-046 Template and merge field catalog as data

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-046 |
| Epic | E1, release 30 November 2026 |
| Module | P6 Communications |
| Feature | FEAT-DRI-16 Hold the template catalog with merge fields |
| Requirement IDs | REQ-OCC-001, REQ-OCC-002 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-012 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **letter and document templates and their merge fields held as versioned data with the Legal approval record on each version**, so that **a template change is a data release approved by Legal and never a code release**.

## 2. Business rationale

Letters and notices are prepared by hand today, so the wording and the facts on a notice depend on who typed it. This story holds every template version, the merge fields it draws from the case and the Legal approval as data rows, so the letter engine (RWB-E1-052) can only use a version Legal approved and can only fill fields the catalog knows. It serves REQ-OCC-001 and REQ-OCC-002 and the FSD P6 measure "notices with proof of delivery, 100 percent", which needs every notice to come from a known template version (CTL-14).

## 3. Preconditions

- RWB-E1-012 is done: recovery data comes only from the recovery tables.
- The template table exists in schema recovery (Recovery Workbench Physical Schema v4.sql) and the reference data load path of P4 (POST /admin/reference-loads) is live.
- Lists LOV-LANG, LOV-PRODUCT and LOV-NOTICE are loaded (refdata.txt).
- The merge field catalog load file is prepared by the reference data administrator (RW-REFADM), one row per merge field, each naming its BR Field ID in the Logical Data Model.
- The person loading holds RW-REFADM (Reference data C). Legal counsel (RW-LEGAL) approves each template version through RWB-E1-034, or through the approval columns of the load file in Epic 1 before that screen is live.

## 4. Flow

1. Reference data administrator: loads the merge field catalog file through POST /admin/reference-loads with table "merge_field" and a valid from date.
2. System: checks every row: merge code unique, BR Field ID present in sys_fields, source entity and field present, required flag set. A row that fails refuses the whole load (refdata change process, step 3).
3. Reference data administrator: loads a template version file through POST /admin/reference-loads with table "template", carrying template code, language, product group, channel, notice type, signature basis, the body file reference, the merge codes used and, where Legal has signed, the approver and approval date.
4. System: reads every merge code in the body and in the merge code list and checks each one against the catalog in force. An unknown code refuses the load and names the code (MSG-P6-006).
5. System: assigns the next version number for the template code and language, keeps every earlier version readable and sets state Approved only where the approver and approval date are present, otherwise Draft.
6. System: the published interface TemplateCatalog returns, for a template code, language and date, the current version: the Approved version with the highest version number whose valid from date is on or before that date.
7. Letter engine (RWB-E1-052): asks TemplateCatalog for the current version. If none is Approved, the catalog refuses and names the missing approval (MSG-P6-005).
8. System: writes the load result (rows loaded, rows refused, version numbers) to the reference load record and the ACE audit log.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Generation asks for a template whose versions are all Draft | TemplateCatalog throws TemplateNotApprovedException; nothing is generated | MSG-P6-005 | AC2 |
| X2 | A template uses a merge code that is not in the catalog | The whole load is refused; the unknown code is named | MSG-P6-006 | AC3 |
| X3 | A catalog row names a BR Field ID that is not in the data dictionary | The whole catalog load is refused | MSG-P1-002 | AC4 |
| X4 | A template row has no template code, language or body reference | The whole load is refused; the field is named | MSG-GEN-001 | AC5 |
| X5 | The same template file is loaded twice | The second load creates no new version | MSG-P1-002 | AC6 |
| X6 | The only Approved version is withdrawn | TemplateCatalog returns no current version; generation holds | MSG-P6-003 | AC7 |
| X7 | A version has valid from in the future | The earlier Approved version stays current until that date | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the recovery tables (RWB-E1-012) and the P4 reference load path; the screen comes in RWB-E1-034 |
| Negotiable | The merge codes and the templates are data; the story fixes the checks and the selection of the current version |
| Valuable | Every notice from Epic 1 on is traceable to one Legal-approved version |
| Estimable | One new table, one validator, one published interface, two load handlers |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one automated test against synthetic load files |

## 7. Acceptance criteria

```gherkin
Feature: Template and merge field catalog as data

  Background:
    Given the merge field catalog version "MF-2026.11" is in force with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Given template "DEMAND-MTG" in language "TH" has version 1 Approved by user "LEG-0001" on 2026-10-01

  Scenario: AC1 Template versioned
    Given a load file for template "DEMAND-MTG" language "TH" approved by user "LEG-0001" on 2026-11-10 with valid from 2026-11-10
    When it is loaded on 2026-11-10
    Then the system creates version 2 of "DEMAND-MTG" with state "Approved", approver "LEG-0001" and approval date 2026-11-10
    Then TemplateCatalog returns version 2 as current for "DEMAND-MTG", "TH" on 2026-11-10
    Then version 1 stays readable with its own approver and approval date

  Scenario: AC2 Unapproved template blocked
    Given template "RECALL-HP" in language "TH" has only version 1 in state "Draft"
    When the letter engine asks TemplateCatalog for the current version of "RECALL-HP", "TH"
    Then the catalog refuses with TemplateNotApprovedException
    Then the refusal carries MSG-P6-005 naming "RECALL-HP" version 1

  Scenario: AC3 Merge fields checked
    Given a load file for template "GUARANTOR-SSME" whose body uses the merge code "GUARANTOR_EMAIL"
    Given "GUARANTOR_EMAIL" is not in the catalog
    When it is loaded
    Then the system refuses the load in full with MSG-P6-006 naming "GUARANTOR_EMAIL"
    Then the system creates no version of "GUARANTOR-SSME"

  Scenario: AC4 Catalog row with an unknown field ID is refused
    Given a catalog load file of 12 rows where row 7 names a BR Field ID "XX-CAS-999" that is not in the data dictionary
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming the check "field ID not in the data dictionary"
    Then catalog version "MF-2026.11" stays in force

  Scenario: AC5 Template row with a missing required field is refused
    Given a template load file whose row has no body reference
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "body_ref"

  Scenario: AC6 Repeated load creates no new version
    Given the load file of AC1 has been loaded once and version 2 exists
    When the same file with the same file hash is loaded again
    Then the system refuses the load with MSG-P1-002 naming the check "repeat of load"
    Then "DEMAND-MTG" still has 2 versions

  Scenario: AC7 Withdrawn current version leaves no current version
    Given version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn"
    When the letter engine asks TemplateCatalog for the current version of "DEMAND-MTG", "TH" on 2026-11-20
    Then TemplateCatalog returns no current version and throws TemplateWithdrawnException
    Then the refusal carries MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC8 Future valid from date keeps the earlier version current
    Given version 3 of "DEMAND-MTG" "TH" is Approved with valid from 2026-12-01
    When TemplateCatalog is asked on 2026-11-30 and on 2026-12-01
    Then it returns version 2 on 2026-11-30
    Then it returns version 3 on 2026-12-01
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A template version is used only when its state is Approved and it carries the Legal approver and approval date | REQ-OCC-002; CTL-14 |
| BR2 | The current version for a template code and language on a date is the Approved version with the highest version number whose valid from is on or before that date | R-LIT-03 (template_status = current) |
| BR3 | A withdrawn template has no current version, and generation holds until Legal approves a new one | R-LIT-04, R-LIT-06 |
| BR4 | Every merge code a template uses exists in the catalog in force, and every catalog row names a BR Field ID in the data dictionary | REQ-OCC-001; Principle 1 |
| BR5 | A load with any refused row is refused in full and the previous version stays in force | refdata.txt change process, step 3 |
| BR6 | Earlier versions are never changed or deleted; open cases keep the version they were generated under | refdata.txt change process, step 6; R-UNI-38 |
| BR7 | Templates are owned by Legal counsel as reference data | refdata.txt reference table "Letter and notice templates"; DL28 |

## 9. State transitions

None. This story does not change a case status. It sets the template version state (standard column state): Draft on load without an approver, Approved on load with an approver, Withdrawn when Legal withdraws it (RWB-E1-034). The reference load status moves from loaded to refused or in force.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads the catalog and template files (Reference data C) |
| RW-LEGAL, Legal counsel | Approves a template version; the approver named in the load (Documents A) |
| RW-LITOFF, litigation officer | Reads templates and the catalog (Documents R) |
| RW-COE, center of excellence analyst | Reads the catalog (Reference data R) |
| SY-CASEWF, case workflow module | Calls TemplateCatalog for the current version |

No approval level from the delegation of authority applies.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-045 | template | id | Write |
| DF-REF-046 | template | template_code | Write |
| DF-REF-047 | template | template_version | Write |
| DF-REF-048 | template | language | Write |
| DF-REF-049 | template | product_group | Write |
| DF-REF-050 | template | body_ref | Write |
| DF-REF-051 | template | approved_by_legal | Write |
| DF-REF-063 | template | approved_by | Write |
| DF-REF-064 | template | approved_at | Write |
| DF-REF-065 | template | valid_from | Write |
| DF-REF-066 | template | channel | Write |
| DF-REF-067 | template | notice_type | Write |
| DF-REF-068 | template | signature_basis | Write |
| DF-REF-069 | template | merge_codes | Write |
| Standard column | template | state | Write |
| DF-REF-252 | merge_field | id | Write |
| DF-REF-253 | merge_field | merge_code | Write |
| DF-REF-254 | merge_field | source_entity | Write |
| DF-REF-255 | merge_field | source_field | Write |
| DF-REF-256 | merge_field | field_id | Write |
| DF-REF-257 | merge_field | is_required | Write |
| DF-REF-258 | merge_field | personal_data | Write |
| DF-REF-259 | merge_field | catalog_version | Write |
| DF-REF-260 | merge_field | valid_from | Write |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (exists, module P4)

| Item | Value |
|---|---|
| Request | multipart/form-data: file, table ("template" or "merge_field"), validFrom |
| Response | 201 ReferenceLoad: id, table, validFrom, status, rows |
| Errors | 401 no session (MSG-P4-001); 403 role lacks Reference data C (MSG-P4-002); 409 a load for the same table and file hash already exists (MSG-P1-002); 422 a row fails a check (MSG-GEN-001, MSG-P6-006, MSG-P1-002); 503 store unavailable (MSG-GEN-006) |
| Authorization | Reference data, right C |
| Idempotency | SHA-256 hash of the file per table; a repeat is refused (AC6) |

P4 owns the endpoint. This story adds two table handlers to it through the P4 published interface:

```java
public interface ReferenceLoadHandler {
    String table();                                   // "template" or "merge_field"
    LoadValidation validate(LoadFile file, LocalDate validFrom);
    LoadResult apply(LoadFile file, LocalDate validFrom, UUID loadedBy);
}
```

**Published interface TemplateCatalog** (P6, called by RWB-E1-052, RWB-E2-022, RWB-E2-026)

```java
public interface TemplateCatalog {
    TemplateVersion current(String templateCode, String language, LocalDate onDate)
        throws TemplateNotApprovedException, TemplateWithdrawnException;
    Optional<TemplateVersion> version(String templateCode, String language, int templateVersion);
    List<MergeField> mergeFields(String templateCode, String language, int templateVersion);
}
```

TemplateVersion carries id, templateCode, templateVersion, language, productGroup, channel, noticeType, signatureBasis, bodyRef, approvedBy, approvedAt, validFrom and the merge codes. No personal data.

## 13. Solution plan

- Package: folder `recovery/comms/templates`, Java package `recovery.comms.templates`.

| Component | Type | Responsibility |
|---|---|---|
| TemplateEntity | Entity | Maps table template with the new columns |
| MergeFieldEntity | Entity | Maps table merge_field |
| TemplateRepository | Repository | Reads and writes template; finds the current version by code, language and date |
| MergeFieldRepository | Repository | Reads and writes merge_field by catalog version |
| TemplateLoadHandler | Service | ReferenceLoadHandler for table "template": parses rows, assigns versions, applies BR1 to BR6 |
| MergeFieldLoadHandler | Service | ReferenceLoadHandler for table "merge_field": checks field IDs against sys_fields |
| MergeCodeScanner | Service | Reads merge codes `{{CODE}}` from a DOCX body and compares them with the declared list |
| TemplateCatalogService | Published interface | Implements TemplateCatalog |

- Database: table template (Recovery Workbench Physical Schema v4.sql) gets the new columns approved_by uuid, approved_at timestamptz, valid_from date, channel varchar(15), notice_type varchar(25), signature_basis varchar(20), merge_codes jsonb. Constraint uk_template UNIQUE (template_code) is replaced by uk_template_version UNIQUE (template_code, language, template_version), because one code holds many versions. Check constraint: state in ('DRAFT','APPROVED','WITHDRAWN'); approved_by and approved_at both set when state = 'APPROVED'. New table merge_field with unique (merge_code, catalog_version). Flyway migration `V1_046__template_catalog.sql` creates merge_field and alters template.
- Configuration and reference data: LOV-LANG, LOV-PRODUCT, LOV-NOTICE (loaded by RW-REFADM); the merge field catalog file (RW-REFADM, content agreed with Legal counsel, DL28); template files and their approvals (Legal counsel); new lists for channel (LETTER, SMS, LINE) and signature basis (E_SIGNATURE_ALLOWED, WET_INK_REQUIRED) recorded as additions.
- Build steps:
  1. Write the Flyway migration and the two entities; test the constraints with an in-memory PostgreSQL (Testcontainers).
  2. Build MergeFieldLoadHandler with the sys_fields check; test AC4.
  3. Build MergeCodeScanner over DOCX bodies; test that it finds every `{{CODE}}` and nothing else.
  4. Build TemplateLoadHandler: required fields, merge code check, version numbering, state from the approval columns; test AC1, AC3, AC5.
  5. Add the file hash check on repeat loads; test AC6.
  6. Build TemplateCatalogService with the BR2 selection and the withdrawn and Draft refusals; test AC2, AC7, AC8.
  7. Add both handlers to the P4 reference load service behind the feature flag.
- Feature flag: `rwb.comms.template-catalog`.
- Done when: the tests in section 16 pass, and the migration runs clean on an empty schema and on the SIT schema.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | Generation asks for a template with no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A template uses a merge code not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-003 | The current version is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P1-002 | A catalog load fails a check, or repeats a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A required field is empty in a load row | Enter {field}. |

## 15. Screens and states

No screen in this story. The reference data administrator loads files through the P4 load path and reads the result on the reference load record. SCR-40 Reference data (states Versions; load) shows the template and merge_field tables with their versions when it is built. The template screen SCR-33 comes in RWB-E1-034.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-046-01 | AC1, BR1, BR2, BR6 | System | Catalog MF-2026.11; DEMAND-MTG TH version 1 Approved; load of version 2 |
| TC-E1-046-02 | AC2, BR1 | System | RECALL-HP TH with one Draft version |
| TC-E1-046-03 | AC3, BR4 | System | GUARANTOR-SSME body using GUARANTOR_EMAIL |
| TC-E1-046-04 | AC4, BR4, BR5 | System | Catalog file of 12 rows, row 7 with an unknown field ID |
| TC-E1-046-05 | AC5, BR5 | System | Template row with empty body_ref |
| TC-E1-046-06 | AC6 | System | The AC1 file loaded twice |
| TC-E1-046-07 | AC7, BR3 | System | DEMAND-MTG TH version 2 withdrawn |
| TC-E1-046-08 | AC8, BR2 | System | DEMAND-MTG TH version 3 valid from 2026-12-01 |
| TC-E1-046-09 | Access | Access | RW-LITOFF calls POST /admin/reference-loads; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: template codes, languages, merge codes, field mappings and dates are read from the template and merge_field tables.
- No personal data in logs, tests or prompts. Template bodies in tests use synthetic wording; merge values never appear in logs.
- No read of another module's tables. sys_fields is read through the P4 reference data interface; the load path is P4's.
- Earlier template versions are never updated or deleted.
- A merge field marked personal_data is resolved only at generation time through the masking rules (RWB-E1-052), never stored in the template.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-16 | 13 Manage documents and correspondence | R-LIT-03 | TC-E1-046-02, TC-E1-046-03, TC-E1-046-04 |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-16 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06 | TC-E1-046-01, TC-E1-046-05, TC-E1-046-06, TC-E1-046-07, TC-E1-046-08, TC-E1-046-09 |

## 19. Out of scope

- The template screen with upload, approval and withdrawal (RWB-E1-034).
- Generating notices from the templates (RWB-E1-052).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).
