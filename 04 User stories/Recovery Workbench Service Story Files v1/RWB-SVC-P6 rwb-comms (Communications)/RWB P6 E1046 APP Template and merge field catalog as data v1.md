# RWB-P6-E1046-APP Template and merge field catalog as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1046-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E1046-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-006, FR-P6-007, FR-P6-008, FR-P6-009, FR-P6-010, FR-P6-011, FR-P6-012, FR-P6-013, FR-P6-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-046 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF), a Legal counsel (RW-LEGAL) and a reference data administrator (RW-REFADM)**, I want **letter and document templates and their merge fields held as versioned data in `rwb_comms` — every template version with its Legal approval record, every merge code with its BR Field ID checked against the rwb-source-data data dictionary, and the current version served on the admin template operations of `rwb-comms`**, so that **a template change is a data release approved by Legal and never a code release, and the letter engine of RWB-P6-E1052 can only use a version Legal approved and only fill fields the catalog knows**.

### 2. Business rationale

Letters and notices are prepared by hand today, so the wording and the facts on a notice depend on who typed it. Legacy RWB-E1-046 holds every template version, the merge fields it draws from the case and the Legal approval as rows of `template` and `merge_field` in the single recovery schema, loads them through the P4 reference-load path `POST /admin/reference-loads`, checks each catalog row against `sys_fields` inside the same module and lets the letter engine ask an in-process `TemplateCatalog` interface for the current version.

This story is the rwb-comms part of that legacy key. Architecture v5 gives P6 rwb-comms the notices, templates, merge fields and proof of delivery in schema `rwb_comms` (slides 17 and 41), so the two tables move to `rwb_comms` with the rwb-comms login (DP-01, DP-02); the catalog rows are loaded, approved and withdrawn on the admin template operations of `/api/recovery/comms/v1` that the TSD P6 appendix T-A.1 already names for Epic 1 (API-P6-003 to API-P6-007); the field-ID check reads the rwb-source-data data dictionary through its contract instead of reading `sys_fields` in-process (DP-05, DP-11); the lists come from the rwb-case reference-data contract (DP-07); and the earlier template versions are never updated or deleted (DP-15, ADR-021).

It serves REQ-OCC-001 and REQ-OCC-002 and the FSD P6 measure "notices with proof of delivery, 100 percent", which needs every notice to come from a known, Legal-approved template version (CTL-14). The legacy checks, messages and test values stand unchanged: the same load files, the same merge codes, the same approver identifier on the file, the same refusals in full, and the same current-version rule (the Approved version with the highest version number whose valid-from date is on or before the date asked for).

Two points the sources do not settle are carried as the placeholder and as gap and assumption rows: the legacy load path `POST /admin/reference-loads` against the TSD admin template API `Not specified in the source documents (GAP-1063; ASM-2011)`, and the exact request and answer field names of the five admin operations, which appendix T-A.2 names by resource only `Not specified in the source documents (GAP-1067; ASM-2015)`.

### 3. Preconditions

- RWB-P6-E1046-CON is published: the five admin template operations with the `Template`, `TemplatePage`, `TemplateApproval` and `TemplateWithdrawal` shapes, the error envelope and the message mapping, all on base `/api/recovery/comms/v1` (DP-11, DP-13).
- RWB-PLT-E1043-CON is published: the reference-data client library, so the lists reach this service without a hand-written client (DP-07).
- RWB-PLT-E1044-CON is published: the per-service Flyway convention and the migration pipeline for `rwb_comms` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route, so SCR-40 Reference data reads the versions behind one route (DP-19).
- RWB-P3-E1043-CON is published: the reference-data contract of rwb-case for LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL, with its fake. It is a consumed contract and never blocks this build.
- The `rwb_comms` schema and the rwb-comms login exist (DP-02); the per-service login name is Not specified in the source documents (GAP-1068; ASM-2016).
- Lists LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL are in force on the business date (TSD P6 T3.2).
- The merge field catalog file is prepared by the reference data administrator (RW-REFADM), one row per merge field, each naming its BR Field ID in the Logical Data Model; template files carry the Legal approval columns where Legal has signed.
- The data dictionary of rwb-source-data is published with the BR Field IDs of the catalog and with no field for an unknown ID such as `XX-CAS-999`; the read has no contract dependency in the plan `Not specified in the source documents (GAP-1064; ASM-2012)`.
- The template body is a claim-check file: `body_ref` names an object in the Blob container. Whether the object is held by P5 rwb-document or by this service's own container is `Not specified in the source documents (GAP-1065; ASM-2013)`.
- The release date 30 November 2026 is tentative; the date is not a condition of this story.

### 4. Flow

1. Reference data administrator: loads the merge field catalog file through `POST /api/recovery/comms/v1/admin/templates` with the file, the table `merge_field` and a valid-from date, or through the catalog load fixture of the service in the lower environment. The legacy path is `POST /admin/reference-loads` on module P4; the mapping from that path to this operation is recorded as a gap (GAP-1063).
2. rwb-comms: checks every row — merge code unique within the catalog version, BR Field ID present in the rwb-source-data data dictionary, source entity and field present, required flag set, personal-data flag set. A row that fails refuses the whole load and stores nothing (legacy refdata change process, step 3).
3. rwb-comms: reads every merge code `{{CODE}}` from the body and compares the set with the declared `mergeCodes` list and with the catalog version in force; an unknown code refuses the load and names the code (MSG-P6-006).
4. Reference data administrator: loads a template version file through `POST /admin/templates` with template code, language, product group, channel, notice type, signature basis, the body file reference and the merge codes used; the version is created in state Draft (API-P6-004).
5. rwb-comms: assigns the next version number for the template code and language, keeps every earlier version readable, and writes the version with `state = DRAFT`; nothing is Approved on upload (T-A.2, state rules of section 9).
6. Legal counsel: records the approval of a draft version through `POST /admin/templates/{templateId}/approve` with the valid-from date; the version moves to Approved with its approver, approval time and valid-from date (API-P6-006), and a version whose approval is incomplete stays Draft (MSG-GEN-001 on the missing field).
7. Legal counsel: withdraws an approved version through `POST /admin/templates/{templateId}/withdraw` with a reason; the version moves to Withdrawn and keeps its rows (API-P6-007, R-LIT-04, R-LIT-06).
8. Generation (RWB-P6-E1052): asks the catalog for the current version of a template code and language on a date; the service answers the Approved version with the highest version number whose valid-from date is on or before that date, refuses a Draft-only template with MSG-P6-005, and refuses a template whose only Approved version is Withdrawn with MSG-P6-003.
9. Reference data administrator and auditor: read the versions and their state through `GET /admin/templates` and the body through `GET /admin/templates/{templateId}/content`; both are read-only answers (API-P6-003, API-P6-005).
10. rwb-comms: writes the load or approval result (rows loaded, rows refused, version numbers, state transition) to the service log and to the audit entry, and the request outcome to the `idempotency_key` row for each POST.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Generation asks for a template whose versions are all Draft | No current version is returned; nothing is generated | MSG-P6-005 | AC2 |
| X2 | A template uses a merge code that is not in the catalog | The whole load is refused and the unknown code is named; no version is created | MSG-P6-006 | AC3 |
| X3 | A catalog row names a BR Field ID that is not in the data dictionary | The whole catalog load is refused and the check is named; the catalog version in force stays in force | MSG-P1-002 | AC4 |
| X4 | A template row has no template code, language or body reference | The whole load is refused and the field is named | MSG-GEN-001 | AC5 |
| X5 | The same template file is loaded twice with the same file hash | The repeat is refused and no new version is created | MSG-P1-002 | AC6 |
| X6 | The only Approved version is withdrawn | No current version is returned and generation holds | MSG-P6-003 | AC7 |
| X7 | A version has a valid-from date in the future | The earlier Approved version stays current until that date | None | AC8 |
| X8 | A caller holds no Documents right for the operation | The operation is refused before the handler runs and nothing changes; the declared area and right are enforced at gateway-bff | MSG-P4-002 | Section 10; TC-E1-046-09 |
| X9 | The data-dictionary read or the reference-data read does not answer inside the 2 s budget | The load is refused with MSG-GEN-006 for the system that failed; no row is stored and no version is created | MSG-GEN-006 | Section 12.2 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | Builds against RWB-P6-E1046-CON and the platform contract libraries; the rwb-case reference-data read and the rwb-source-data data-dictionary read are contract fakes (DP-11) |
| Negotiable | Pass | Merge codes, template codes, languages, field mappings, channels and dates are data rows of the load files; the story fixes the checks, the version numbering and the current-version rule |
| Valuable | Pass | Every notice from wave 1 on is traceable to one Legal-approved template version and one catalog version in force |
| Estimable | Pass | Two tables, one migration, two load handlers, one merge-code scanner, one approval and one withdrawal operation |
| Small | Pass | Fits one sprint with its tests and its contract fakes |
| Testable | Pass | Every criterion in section 7 is one automated test over synthetic load files with its message ID and status |

### 7. Acceptance criteria

```gherkin
Feature: Template and merge field catalog as data

  Background:
    Given the merge field catalog version "MF-2026.11" is in force with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Given template "DEMAND-MTG" in language "TH" has version 1 Approved by user "LEG-0001" on 2026-10-01
    Given the rwb-case reference-data contract mock returns LOV-LANG "TH" and "EN", LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED", LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE", and LOV-CHANNEL "LETTER", "SMS" and "LINE"

  Scenario: AC1 Template versioned (legacy RWB-E1-046 AC1)
    Given a load file for template "DEMAND-MTG" language "TH" approved by user "LEG-0001" on 2026-11-10 with valid from 2026-11-10
    When it is loaded on 2026-11-10
    Then the system creates version 2 of "DEMAND-MTG" with state "Approved", approver "LEG-0001" and approval date 2026-11-10
    Then TemplateCatalog returns version 2 as current for "DEMAND-MTG", "TH" on 2026-11-10
    Then version 1 stays readable with its own approver and approval date

  Scenario: AC2 Unapproved template blocked (legacy RWB-E1-046 AC2)
    Given template "RECALL-HP" in language "TH" has only version 1 in state "Draft"
    When the letter engine asks TemplateCatalog for the current version of "RECALL-HP", "TH"
    Then the catalog refuses with TemplateNotApprovedException
    Then the refusal carries MSG-P6-005 naming "RECALL-HP" version 1

  Scenario: AC3 Merge fields checked (legacy RWB-E1-046 AC3)
    Given a load file for template "GUARANTOR-SSME" whose body uses the merge code "GUARANTOR_EMAIL"
    Given "GUARANTOR_EMAIL" is not in the catalog
    When it is loaded
    Then the system refuses the load in full with MSG-P6-006 naming "GUARANTOR_EMAIL"
    Then the system creates no version of "GUARANTOR-SSME"

  Scenario: AC4 Catalog row with an unknown field ID is refused (legacy RWB-E1-046 AC4)
    Given a catalog load file of 12 rows where row 7 names a BR Field ID "XX-CAS-999" that is not in the data dictionary
    Given the rwb-source-data data-dictionary contract mock returns the BR Field ID of every row of the file except "XX-CAS-999"
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming the check "field ID not in the data dictionary"
    Then catalog version "MF-2026.11" stays in force

  Scenario: AC5 Template row with a missing required field is refused (legacy RWB-E1-046 AC5)
    Given a template load file whose row has no body reference
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "body_ref"

  Scenario: AC6 Repeated load creates no new version (legacy RWB-E1-046 AC6)
    Given the load file of AC1 has been loaded once and version 2 exists
    When the same file with the same file hash is loaded again
    Then the system refuses the load with MSG-P1-002 naming the check "repeat of load"
    Then "DEMAND-MTG" still has 2 versions

  Scenario: AC7 Withdrawn current version leaves no current version (legacy RWB-E1-046 AC7)
    Given version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn"
    When the letter engine asks TemplateCatalog for the current version of "DEMAND-MTG", "TH" on 2026-11-20
    Then TemplateCatalog returns no current version and throws TemplateWithdrawnException
    Then the refusal carries MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC8 Future valid from date keeps the earlier version current (legacy RWB-E1-046 AC8)
    Given version 3 of "DEMAND-MTG" "TH" is Approved with valid from 2026-12-01
    When TemplateCatalog is asked on 2026-11-30 and on 2026-12-01
    Then it returns version 2 on 2026-11-30
    Then it returns version 3 on 2026-12-01
```

The eight criteria are the legacy scenarios of RWB-E1-046 AC1 to AC8, copied verbatim with their values, IDs and messages; each carries its origin tag. Two Given lines are added and no legacy line is changed: the background line that names the rwb-case reference-data mock and the AC4 line that names the rwb-source-data data-dictionary mock. `TemplateCatalog` names the catalog behaviour of RWB-P6-E1052's generation path, served here by the admin template operations of section 12.1; the exception names `TemplateNotApprovedException` and `TemplateWithdrawnException` are the legacy contract names and are carried on the message IDs MSG-P6-005 and MSG-P6-003.

### 8. Business rules

| BR | Rule | Source |
|---|---|---|
| BR1 | A template version is used only when its state is Approved and it carries the Legal approver and approval date | RWB-E1-046 BR1; REQ-OCC-002; CTL-14 |
| BR2 | The current version for a template code and language on a date is the Approved version with the highest version number whose valid from is on or before that date | RWB-E1-046 BR2; R-LIT-03 (template_status = current) |
| BR3 | A withdrawn template has no current version, and generation holds until Legal approves a new one | RWB-E1-046 BR3; R-LIT-04, R-LIT-06 |
| BR4 | Every merge code a template uses exists in the catalog in force, and every catalog row names a BR Field ID in the data dictionary | RWB-E1-046 BR4; REQ-OCC-001; Principle 1 |
| BR5 | A load with any refused row is refused in full and the previous version, or the previous catalog version, stays in force | RWB-E1-046 BR5; refdata change process, step 3 |
| BR6 | Earlier versions are never changed or deleted; open cases keep the version they were generated under | RWB-E1-046 BR6; refdata change process, step 6; R-UNI-38 |
| BR7 | Templates are owned by Legal counsel as reference data | RWB-E1-046 BR7; refdata reference table "Letter and notice templates"; DL28 |
| BR8 | `template` and `merge_field` live in `rwb_comms` and are read and written only through this service; no other service's table is read (DP-01) | Architecture v5 slides 17 and 41; DP-01 |
| BR9 | The BR Field ID of a catalog row is checked against the rwb-source-data data dictionary through its contract, one hop with a 2 s timeout; a missing answer refuses the load and never allows it (DP-05, DP-11) | DP-05; DP-11; ADR-020 |
| BR10 | The lists a load is validated against are LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL read from the rwb-case reference-data contract at the version in force; no list value is written in code (DP-07) | TSD P6 T3.2; DP-07 |
| BR11 | A template version is created in state Draft by upload; Approved and Withdrawn are reached only through the approve and withdraw operations, with the approver, the approval time and the valid-from date recorded on the version | TSD P6 T-A.2 (API-P6-004, API-P6-006, API-P6-007) |
| BR12 | A POST carries an Idempotency-Key and its answer is stored; a repeat with the same key returns the first answer and creates nothing | Architecture v5 slide 11; DP-09 |
| BR13 | The template body is a claim-check file named by `body_ref`; the service stores the reference and never the merge values, and no template body or merge value reaches a log | TSD P6 T3.1 (DF-REF-050); section 17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| (none) | `POST /admin/templates` | The row carries template code, language and a body reference, and every merge code exists in the catalog in force | Draft, with the next version number for the code and language |
| Draft | `POST /admin/templates/{templateId}/approve` | The `TemplateApproval` carries the approver and a valid-from date | Approved, with `approved_by`, `approved_at` and `valid_from` set |
| Draft | `POST /admin/templates/{templateId}/withdraw` | A draft version is withdrawn before it was ever current | Withdrawn; it was never a current version |
| Approved | `POST /admin/templates/{templateId}/withdraw` | The `TemplateWithdrawal` carries a reason | Withdrawn; no current version remains for that code and language while no later Approved version exists |
| Approved | a later version is approved with a valid-from date on or before the business date | The later version has the higher version number and its valid from has arrived | Approved, still readable, no longer current |
| Withdrawn | (no transition) | A withdrawn version is never returned to Draft or Approved; Legal approves a new version instead | Withdrawn, readable |

The merge-field catalog version moves when a catalog load is accepted: the catalog version of the file becomes the version in force from its valid-from date, the previous catalog version stays readable, and every template load and every generation is checked against the version in force on the business date. A refused catalog load changes nothing and leaves the previous catalog version in force (BR5). No case status and no notice state is set by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads the catalog file and the template version files, and reads the load result (Documents C, declared by the TSD as the Documents area) |
| RW-LEGAL, Legal counsel | Approves a version through the approve operation and withdraws a version through the withdraw operation (Documents A) |
| RW-LITOFF, litigation officer | Reads template versions and the catalog (Documents R) |
| RW-COE, center of excellence analyst | Reads the catalog and its versions (Documents R) |
| SY-CASEWF, case workflow module, and the letter engine of RWB-P6-E1052 | Asks the catalog for the current version of a template code and language on a date (Documents R) |
| rwb-comms service identity (the rwb-comms login, DP-02) | Serves the five operations, writes `template`, `merge_field`, the idempotency row and the audit entry |

No approval level from the delegation of authority applies. The declared area and right of each operation are enforced at gateway-bff (DP-19); the service holds the declared right per operation in its own configuration and answers 403 MSG-P4-002 when the declared right is absent, and no rwb-access contract is declared for this story `Not specified in the source documents (GAP-1068; ASM-2016)`.

### 11. Data

| BR Field ID | Entity in `rwb_comms` | Field | Physical type | Required | Read or write |
|---|---|---|---|---|---|
| DF-REF-045 | template | id | uuid | Yes | Write |
| DF-REF-046 | template | template_code | varchar(30) | Yes | Write |
| DF-REF-047 | template | template_version | integer | Yes | Write |
| DF-REF-048 | template | language | varchar(2), LOV-LANG | Yes | Write |
| DF-REF-049 | template | product_group | varchar(15), LOV-PRODUCT | No | Write |
| DF-REF-050 | template | body_ref | varchar(400), claim-check reference | Yes | Write |
| DF-REF-051 | template | approved_by_legal | boolean | Yes | Write |
| DF-REF-063 | template | approved_by | uuid, USER_REF | No | Write |
| DF-REF-064 | template | approved_at | timestamptz | No | Write |
| DF-REF-065 | template | valid_from | date | No | Write |
| DF-REF-066 | template | channel | varchar(15), LOV-CHANNEL | No | Write |
| DF-REF-067 | template | notice_type | varchar(25), LOV-NOTICE | No | Write |
| DF-REF-068 | template | signature_basis | varchar(20), LOV-SIGNATURE-BASIS | No | Write |
| DF-REF-069 | template | merge_codes | jsonb | No | Write |
| Standard column | template | state | varchar(40): DRAFT, APPROVED, WITHDRAWN | No | Write |
| DF-REF-252 | merge_field | id | uuid | Yes | Write |
| DF-REF-253 | merge_field | merge_code | varchar(40) | Yes | Write |
| DF-REF-254 | merge_field | source_entity | varchar(60) | Yes | Write |
| DF-REF-255 | merge_field | source_field | varchar(60) | Yes | Write |
| DF-REF-256 | merge_field | field_id | varchar(16), the BR Field ID | Yes | Write |
| DF-REF-257 | merge_field | is_required | boolean | Yes | Write |
| DF-REF-258 | merge_field | personal_data | boolean | Yes | Write |
| DF-REF-259 | merge_field | catalog_version | varchar(20) | Yes | Write |
| DF-REF-260 | merge_field | valid_from | date | Yes | Write |
| DF-REF-028 | lov_value (P3 rwb-case) | lov_code | — | — | Read through the reference-data contract |
| DF-REF-029 | lov_value (P3 rwb-case) | value_code | — | — | Read through the reference-data contract |

Keys and indexes in `rwb_comms`:

- `template`: primary key `id`; unique `uk_template_version (template_code, language, template_version)`; index `(template_code, language, valid_from)` for the current-version read; check `state in ('DRAFT','APPROVED','WITHDRAWN')`; check that `approved_by` and `approved_at` are both set when `state = 'APPROVED'`. The legacy `uk_template UNIQUE (template_code)` is replaced, because one code holds many versions.
- `merge_field`: primary key `id`; unique `(merge_code, catalog_version)`; index `(catalog_version, valid_from)`.
- Flyway: the migration `V1_046__template_catalog.sql` (legacy name kept) creates `merge_field` and alters `template`, applied in the `rwb_comms` sequence under the per-service Flyway convention (DP-15, ADR-021). The exact position of the script in that sequence is Not specified in the source documents (GAP-1067; ASM-2015).
- Field IDs are those in the Logical Data Model and Data Dictionary; the entity names follow the TSD P6 T3.1 and the Ownership Map (`template` and `merge_field` are P6's). `approved_by` is a USER_REF of type uuid in T3.1, while the legacy load files name an approver as "LEG-0001"; how the file value resolves to a uuid is `Not specified in the source documents (GAP-1066; ASM-2014)`.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The five operations are the TSD P6 appendix T-A.1 rows API-P6-003 to API-P6-007 re-based on the per-service base (DP-13); their detail is T-A.2 and their field-level shapes are `Not specified in the source documents (GAP-1067; ASM-2015)`.

| Method | Path | API ID | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/admin/templates` | API-P6-003 | List template versions by code, language and state; answers `TemplatePage` | Documents R | Not applicable |
| POST | `/admin/templates` | API-P6-004 | Upload a new template version in state Draft; answers `Template` | Documents C | `Idempotency-Key` header |
| GET | `/admin/templates/{templateId}/content` | API-P6-005 | Download a template body; answers the binary named by `body_ref` | Documents R | Not applicable |
| POST | `/admin/templates/{templateId}/approve` | API-P6-006 | Record the Legal approval of a draft version with its valid-from date; request `TemplateApproval`, answer `Template` | Documents A | `Idempotency-Key` header |
| POST | `/admin/templates/{templateId}/withdraw` | API-P6-007 | Withdraw an approved version with a reason; request `TemplateWithdrawal`, answer `Template` | Documents A | `Idempotency-Key` header |

Error statuses are those of T-A.2 per operation: 401, 403, 503 on the two reads; 401, 403, 413, 415, 422, 503 on the upload; 401, 403, 404, 409, 422, 503 on the approve and the withdraw. Every error uses the platform error envelope and one message ID of section 14. The catalog behaviour AC1 to AC8 tests — the next version number, the state set, the merge-code check, the field-ID check, the repeated-file check and the current-version selection — is served behind these five operations; the query parameter that selects the current version on a date is `Not specified in the source documents (GAP-1067; ASM-2015)`.

`POST /cases/{caseId}/notices` (API-P6-001) and `GET /notices/{noticeId}` (API-P6-002) exist in this service but belong to the contract of RWB-P6-E1052-CON; this story references them and claims neither.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | Read LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL at the version in force (DP-07, RWB-P3-E1043-CON) |
| GET | `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data | Check every BR Field ID named by a catalog row (DP-05). The read has no contract dependency in the plan: `Not specified in the source documents (GAP-1064; ASM-2012)` |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failure on either row refuses the load with MSG-GEN-006 naming the system that did not answer; no load is ever accepted on a partial answer.

#### 12.3 Events published

None. This story generates no notice, so it publishes none of the service's events: `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` on `rwb.comms.events.v1` are published by the notice path of RWB-P6-E1052 and the dispatch stories of wave 2. A template load or an approval is a synchronous answer and is audited in the service log and the audit entry, not published as an event.

#### 12.4 Events consumed

None. The catalog is read on demand by its callers; this story subscribes to no topic, and the reference-data and data-dictionary answers of section 12.2 are synchronous reads. A change of a list or of a data-dictionary field reaches the service on its next load, and the version in force is compared at that moment.

#### 12.5 Workflows and activities

None. The loads, the approvals and the withdrawals are synchronous REST operations in the caller's thread; this story starts no workflow, registers no activity and holds nothing on task queue `rwb-comms` in namespace `rwb-recovery` (DP-10 does not apply to this key).

#### 12.6 Schedules

None. No Schedule, no cron entry and no job name is registered; JOB-10 WIN notices belongs to the dispatch stories of wave 2 and JOB-11 is the platform outbox relay. This story holds no Schedule of its own.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (`rwb_comms`) | The template versions, their state and their Legal approval record |
| merge_field | P6 (`rwb_comms`) | The merge codes and their BR Field ID, by catalog version |
| notice | P6 (`rwb_comms`) | Contracted use only: `template_id` names the version a notice was generated from; this story writes no notice row (RWB-P6-E1052) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The idempotency row of each POST and the envelope objects of the service; this story writes the idempotency row only (DP-09) |

`signature_request` and `document` are P5 rwb-document's, `interaction` is P1 rwb-source-data's, `recovery_case` is P3 rwb-case's and `decision_log_entry` is P7 rwb-decision's; they are named only as consumed answers and never read or written here (DP-01). `sys_fields` is P1's and is reached through the data-dictionary contract, never as a table.

#### 12.8 Contract fakes

| Fake | Documented answer |
|---|---|
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /admin/lists/{listCode}` answers LOV-LANG "TH" and "EN"; LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"; LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE"; LOV-CHANNEL "MOBILE", "HOME_PHONE", "WORK_PHONE", "LINE", "EMAIL", "POSTAL_ADDRESS", "CALL", "VISIT", "SMS", "LETTER", "PORTAL" and "BRANCH" |
| rwb-source-data data-dictionary fake | `GET /admin/data-dictionary/fields` answers DF-REF-045 to DF-REF-051 and DF-REF-252 to DF-REF-260 as known BR Field IDs, and answers no field for `"XX-CAS-999"` |
| merge-field catalog fixture, version "MF-2026.11" | Rows for merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE", each naming a BR Field ID of the data dictionary, with catalog version "MF-2026.11" and its valid-from date |
| template load fixture pack | The DEMAND-MTG "TH" version 1 file (Approved by "LEG-0001" on 2026-10-01), the DEMAND-MTG "TH" version 2 file (approved 2026-11-10, valid from 2026-11-10), the DEMAND-MTG "TH" version 3 file (valid from 2026-12-01), the GUARANTOR-SSME file with "GUARANTOR_EMAIL", the RECALL-HP "TH" Draft file, the file with no `body_ref`, and the SHA-256 file hash of each |

The two consumed fakes answer the paths of section 12.2 with the values above, so the story builds and its tests run before rwb-case and rwb-source-data are live (DP-11). The exact response field names of the data-dictionary read are `Not specified in the source documents (GAP-1067; ASM-2015)`.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The five admin template operations of 12.1 provided; the reference-data read and the data-dictionary read of 12.2 consumed; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No notice event is published by this key; no topic is subscribed |
| Temporal | None | No workflow, no activity and no Schedule |
| File | 1 | The template body as a claim-check file named by `body_ref`; the body is stored as a reference and never as a row |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `template`, Java package `th.co.scb.ace.workbench.recovery.comms.template`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-08 is not among the patterns of this story: no rwb-access contract is declared as a dependency, the declared area and right of each operation are enforced at gateway-bff (DP-19), and the local guard on the admin load is recorded as a gap `Not specified in the source documents (GAP-1068; ASM-2016)`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateAdminController | Controller | The five admin operations with validation, the `Idempotency-Key` handling and the problem mapping of 12.1 |
| TemplateService | Service | Version numbering, the state rules of section 9, the current-version selection and the approve and withdraw transitions |
| MergeFieldService | Service | Catalog rows by catalog version, and the BR Field ID check against the rwb-source-data data-dictionary contract |
| TemplateLoadValidator | Service | The required-field checks, the merge-code set check and the repeated-file check of AC3, AC5 and AC6 |
| MergeCodeScanner | Service | Reads every `{{CODE}}` from a body and compares it with the declared `mergeCodes` and the catalog in force |
| TemplateRepository | Repository | Reads and writes `template`; finds the current version by code, language and date |
| MergeFieldRepository | Repository | Reads and writes `merge_field` by catalog version |
| DataDictionaryClient | Client | The one-hop read of the data dictionary with the 2 s timeout, the retry and the breaker (DP-11) |
| ReferenceCatalog | Service | Reads LOV-LANG, LOV-PRODUCT, LOV-NOTICE and LOV-CHANNEL through the reference-data client (DP-07) |
| TemplateBodyStore | Service | Resolves `body_ref` to the claim-check object and streams it on the content operation |
| TemplateAuditWriter | Service | Writes the load and state-transition result to the service log and the audit entry; never a body or a merge value |

**Database and migrations**

- `template` and `merge_field` in `rwb_comms`, with the keys, indexes and checks of section 11.
- The migration `V1_046__template_catalog.sql` creates `merge_field`, alters `template` with the approval, valid-from, channel, notice-type, signature-basis and merge-codes columns, replaces the legacy unique constraint and adds the state check; it runs in the `rwb_comms` sequence (DP-15).
- No row is seeded by the migration: the catalog and the templates are data loaded through the operations, never code.

**Configuration and reference data**

- The lists in force: LOV-LANG "TH" and "EN"; LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"; LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE"; LOV-CHANNEL with "LETTER", "SMS" and "LINE" among its values; LOV-SIGNATURE-BASIS "E_SIGNATURE_ALLOWED" and "WET_INK_REQUIRED" (TSD P6 T3.2).
- The merge field catalog file, agreed with Legal counsel and loaded by RW-REFADM; template files and their approvals are Legal counsel's.
- The data-dictionary base URL and the reference-data client are configuration, never a list value in code.
- The feature switch is `rwb.comms.template-catalog` (legacy name kept), read as a parameter: off means the admin operations answer 503 with MSG-GEN-006 and nothing is loaded, never a silent accept.
- The login is the rwb-comms login (DP-02); its name is Not specified in the source documents (GAP-1068; ASM-2016).

**Build steps**

1. The migration and the two entities with the constraints of section 11; test the constraints with Testcontainers.
2. MergeFieldService and the data-dictionary client with the unknown-field refusal; test AC4 on the fake and its gap row.
3. MergeCodeScanner over the body; test that it finds every `{{CODE}}` and nothing else.
4. TemplateService with version numbering, the state rules and the required-field checks; test AC1, AC3 and AC5.
5. The repeated-file check on the SHA-256 hash of the file; test AC6.
6. The current-version selection with the Draft refusal, the Withdrawn refusal and the future valid-from rule; test AC2, AC7 and AC8.
7. The approve and withdraw operations with the `Idempotency-Key` rule and the error mapping; test the state table of section 9.
8. The content operation over `body_ref`, with no body in the log; test the reference and the claim-check read.
9. A contract-fake run of both consumed reads in isolation, so the story builds before rwb-case and rwb-source-data are live.

**Done when.** The nine test cases of section 16 pass, the migration runs clean on an empty schema and on the SIT schema, the contract tests of RWB-P6-E1046-CON and RWB-P3-E1043-CON stay green, and no template body and no merge value appears in a log of the run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | Generation asks for a template with no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A template uses a merge code not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-003 | The current version is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P1-002 | A catalog load fails a check, or repeats a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A required field is empty in a load row | Enter {field}. |
| MSG-P4-002 | A caller holds no Documents right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A consumed read does not answer in time, or the feature switch is off | {system} is not available. Your request is queued and will be retried. |

The texts of MSG-P6-005, MSG-P6-006, MSG-P6-003, MSG-P1-002 and MSG-GEN-001 are copied character for character from RWB-E1-046 section 14 and keep their legacy meanings; MSG-P4-002 is the reference-data refusal of the legacy load path (TC-E1-046-09) and MSG-GEN-006 is the platform unavailable message. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-40 Reference data (states Versions; load): the reference data administrator and the auditor see the `template` and `merge_field` tables with their versions, their state and the load result on the reference load record. SCR-33 Template catalog admin (states Loading, Read only, Draft, Approved, Withdrawn): the Legal counsel approves or withdraws a version and the officer reads it. Both screens are read-only projections of this story's operations through the gateway-bff composite route (DP-19), which calls the five admin operations and merges the answers into the screen model; neither screen is built here, and the screen field list and the route specification belong to RWB-PLT-N001-CON.

The template screen with upload, approval and withdrawal as a delivered screen is the legacy RWB-E1-034 and sits outside this story; the screen names SCR-33 and SCR-40 are the ones the legacy story uses.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-046-01 | AC1, BR1, BR2, BR6 | End to end | Catalog MF-2026.11; DEMAND-MTG TH version 1 Approved; load of version 2 |
| TC-E1-046-02 | AC2, BR1 | End to end | RECALL-HP TH with one Draft version |
| TC-E1-046-03 | AC3, BR4 | End to end | GUARANTOR-SSME body using GUARANTOR_EMAIL |
| TC-E1-046-04 | AC4, BR4, BR5 | End to end | Catalog file of 12 rows, row 7 with an unknown field ID |
| TC-E1-046-05 | AC5, BR5 | End to end | Template row with empty body_ref |
| TC-E1-046-06 | AC6 | End to end | The AC1 file loaded twice |
| TC-E1-046-07 | AC7, BR3 | End to end | DEMAND-MTG TH version 2 withdrawn |
| TC-E1-046-08 | AC8, BR2 | End to end | DEMAND-MTG TH version 3 valid from 2026-12-01 |
| TC-E1-046-09 | Access | Component | RW-LITOFF calls POST /admin/reference-loads; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component. TC-E1-046-09 keeps its legacy load path in its Data column; the path it exercises in this story is the upload operation it maps to, and the mapping is the gap GAP-1063.

### 17. Guardrails

- No business value in code: template codes, languages, merge codes, field mappings, channels, signature bases and dates are read from `template`, `merge_field` and the reference-data contract; no list value and no template code appears in Java.
- No personal data in events, workflow inputs, logs, tests or prompts. Template bodies in tests use synthetic wording, a merge field marked `personal_data` is resolved only at generation time (RWB-P6-E1052), and no template body and no merge value appears in a log or an evidence line.
- ACE data only through the owner's contract or the owner's `v_ace_*` views. This story reads no ACE table and no ACE view: the BR Field IDs are checked at the rwb-source-data data-dictionary contract and the lists at the rwb-case reference-data contract.
- No cross-schema read: `rwb_comms` holds no foreign key into another schema and no copy of a case, notice, document or decision row (DP-01).
- Earlier template versions are never updated or deleted; a withdrawn version stays readable and a new version is approved instead (BR6, R-UNI-38).
- Every POST carries an `Idempotency-Key` and stores its answer; a repeat creates nothing (BR12).
- One hop, a 2 s timeout and a breaker per downstream on both consumed reads; a failed read refuses the load and never allows it (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | The `merge_field` rows, the BR Field ID check, MSG-P6-006 and MSG-P1-002 | TC-E1-046-03, TC-E1-046-04 |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | The `template` version, its state and approval columns, MSG-P6-005, MSG-P6-003, MSG-GEN-001 | TC-E1-046-01, TC-E1-046-02, TC-E1-046-05, TC-E1-046-06, TC-E1-046-07, TC-E1-046-08, TC-E1-046-09 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | `template` and `merge_field` in `rwb_comms`; no other service's table read |
| DP-07 | The reference-data read of section 12.2 and the lists of section 13 |
| DP-11 | The two consumed reads with one hop, a 2 s timeout and a fake |
| DP-13 | Base `/api/recovery/comms/v1` on all five operations |
| DP-15 | The `rwb_comms` Flyway sequence and the migration of section 11 |
| DP-19 | SCR-33 and SCR-40 read through gateway-bff |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_comms` schema and the rwb-comms login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E1-046; this story owns its AC1 to AC8 and its TC-E1-046-01 to TC-E1-046-09. The integration proof of the same values across rwb-case, rwb-source-data, rwb-comms, rwb-document and rwb-decision is RWB-ITG-E1046-ITG.

### 19. Out of scope

- Generating notices from the template versions: RWB-P6-E1052-APP and RWB-P6-E1052-CON.
- Dispatching letters, SMS and LINE and capturing proof of delivery: RWB-P6-E2021 and RWB-P6-E2022, with RWB-P6-E1055.
- The end-to-end proof of these values across the wave 1 services: RWB-ITG-E1046-ITG.
- Authoring or editing a template body: the body is a claim-check file produced outside the service and named by `body_ref`.
- The delivered template screen with upload, approval and withdrawal (legacy RWB-E1-034) and the reference-data load screen beyond its read-only projection.
- The Compliance approval path for a template (FEAT-ADM-05, Epic 8).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- The `rwb_comms` schema baseline, the topic and queue provisioning, the dashboards and the runbook of the service.
