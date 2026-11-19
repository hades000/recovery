# TB0001-1187 [RWB-E1-025] Document types and fields agreed

| Field | Value |
|---|---|
| Jira | [TB0001-1187](https://scbjira.atlassian.net/browse/TB0001-1187) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:25.705+0700 |
| Updated | 2026-11-18T17:22:03.927+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 6 |

## Description

As a center of excellence analyst (RW-COE), I want the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data, so that the OCR pipeline, classification and extraction have one signed target list.

## Acceptance criteria

```gherkin
Feature: Document types and fields agreed

  Background:
    Given LOV-RETENTION holds "LEGAL10Y" and "GENERAL05Y"
    Given user "TEST-REFADM-01" holds RW-REFADM
    Given user "TEST-APPROVER-01" holds Reference data A

  Scenario: AC1 Field list signed
    Given the six types and their 26 fields in load file "DOCTYPE-2026.11"
    Given each row carries the legal counsel sign-off of user "TEST-LEGAL-01" dated 6 November 2026
    Given each row carries the NPA sign-off of user "TEST-HEADNPA-01" dated 6 November 2026
    When "TEST-REFADM-01" loads the file for table "DOCUMENT_TYPE" with valid from 30 November 2026
    Then the load has status "LOADED" with 6 rows
    Then every row holds both sign-off user IDs and both dates

  Scenario: AC2 Reference data
    Given the load from AC1
    When "TEST-APPROVER-01" approves it
    Then the document type table version "DOCTYPE-2026.11" is in force from 30 November 2026
    Then it holds DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE
    Then COURT_NOTICE holds the fields court_name, black_case_no, notice_date and hearing_date with retention class "LEGAL10Y" and write_once true
    Then APPRAISAL_REPORT has retention class "GENERAL05Y", write_once false and 4 fields

  Scenario: AC3 Load without both sign-offs is refused
    Given a load file where the GUARANTOR_NOTICE row has no NPA sign-off
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 naming row 6 and "NPA sign-off missing"
    Then no row of that file is written and the version in force is unchanged

  Scenario: AC4 Invalid values are refused in full
    Given a load file where the TITLE_DEED row has retention class "KEEP99" and a seventh row repeats the type code "COURT_NOTICE"
    When "TEST-REFADM-01" loads it
    Then the system refuses the load in full with MSG-P3-027 listing both rows
    Then the version in force is unchanged

  Scenario: AC5 The same version loaded twice
    Given version "DOCTYPE-2026.11" is loaded
    When "TEST-REFADM-01" loads a file with version "DOCTYPE-2026.11" again
    Then the system refuses the request with 409 and MSG-P3-027 naming "version already loaded"
    Then the first load is unchanged

  Scenario: AC6 A future version takes effect on its date
    Given version "DOCTYPE-2026.11" is in force
    Given version "DOCTYPE-2027.01" adds field "court_region" to COURT_NOTICE and is approved with valid from 1 January 2027
    When the type table is read on 31 December 2026 and on 1 January 2027
    Then the read on 31 December 2026 returns "DOCTYPE-2026.11"
    Then the read on 1 January 2027 returns "DOCTYPE-2027.01" with field "court_region"

  Scenario: AC7 The loader cannot approve their own load
    Given "TEST-REFADM-01" loaded version "DOCTYPE-2027.01" and also holds Reference data A in the test set
    When "TEST-REFADM-01" approves it
    Then the system refuses the request with 409 and MSG-P7-002
    Then the load stays "LOADED"
```

## Comments (6)

### Comment 1: Pe Chichareon, 2026-11-16T14:57:45.026+0700, edited 2026-11-16T15:07:16.518+0700

Comment ID 1792674



A1 - Request Henka to provide the initial data file in Excel format

A2 - Request Henka for example of Excel file

A3 - 

 AC3 & AC4 - MSG-P4-002   required 

 *RWB-E1-019*

 *RWB-E1-022*

 *RWB-E1-037*

 *RWB-E1-043*

A4 -   

   AC1 - In case of  V1 = Approved,   V2 = Loaded    , if there is a new load version – should this be V3?    TBC from Henka

   

### Comment 2: Chitchaya Muanchonchana, 2026-11-16T14:58:30.002+0700, edited 2026-11-16T17:16:01.139+0700

Comment ID 1792678

Question @CHANISSARA MAHAKITTIKUN 

# Request for excel file as example and initial SQL to insert data.
# if user load a file with “Load” status but not approved yet , then user try to load again in next week. what should the data keep in a Document_type table.
# What is logic to insert data eg, count running no. of each doc type , able to load more than 1 time even the previous is approved or not.



Note 

# E1-019 is prerequisite of this ticket.
# What is possible value of document type. >> LOV_DOC_TYPE.

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T11:20:38.537+0700

Comment ID 1794170

These points add to the template, version and dependency questions already on this card.

# *No role can approve.* The permission matrix gives Reference data A to no role. Granting it to legal counsel is an assumption under DL01.
#* Question: who approves DOCTYPE loads in SIT, UAT and PROD?
# *Actor mismatch.* The story is "As a COE analyst", but RW-REFADM does the load and COE only prepares the file. Please align the story text.
# *Personal fields are not marked.* {{owner_name}} (TITLE_DEED) and {{account_no}} (DEMAND_LETTER) are personal data, but {{field_definitions}} has no {{is_personal}} or {{personal}} flag.
#* Proposal: add the flag, with data_type, format and required, so that extraction (RWB-E1-053), masking and the PDPA lint (RWB-TE-011) can use it.
# *Sign-off is still pending.* DL19 (due 6 Nov) still holds the type and field list. The Legal and NPA signers must be named before RWB-E1-050 and RWB-E1-053 are built.
# *No withdraw.* There is no way to withdraw a wrong approved version (same gap as RWB-E1-043 point 1).

Who answers: Product Owner, Legal, Head of NPA, Henka (BA).

### Comment 4: VAISHNAVI KAULGE, 2026-11-17T12:51:39.313+0700

Comment ID 1794393

@Pe Chichareon 


Here are A1 and A2 as one answer: the *format* of the Excel first, then a *filled example*.

h3. Format of the Excel (one row per document type)

||#||Column||What it means||Allowed values||Required||Example||
|1|doc_type_code|Unique code of the document type|Capital letters and underscore; must not repeat|Yes|COURT_NOTICE|
|2|label_en|Name in English|Text|Yes|Court notice|
|3|label_th|Name in Thai|Text|No|หมายศาล|
|4|write_once|Is the document locked (no change or delete)?|TRUE / FALSE|Yes|TRUE|
|5|retention_class|How long to keep it|LEGAL10Y / GENERAL05Y (from LOV-RETENTION)|Yes|LEGAL10Y|
|6|fields|Fields to read from the document, separated by commas|At least one|Yes|court_name, black_case_no, notice_date, hearing_date|
|7|legal_signoff_by|User ID of the legal counsel who signed|A valid user ID|Yes|TEST-LEGAL-01|
|8|legal_signoff_date|Date Legal signed|YYYY-MM-DD|Yes|2026-11-06|
|9|npa_signoff_by|User ID of the Head of NPA who signed|A valid user ID|Yes|TEST-HEADNPA-01|
|10|npa_signoff_date|Date NPA signed|YYYY-MM-DD|Yes|2026-11-06|

*Upload details (entered at upload, not in the rows):* table = DOCUMENT_TYPE, valid from = 2026-11-30, version = DOCTYPE-2026.11.

h3. Example: the filled file (6 rows)

||doc_type_code||label_en||label_th||write_once||retention_class||fields||legal_signoff_by||legal_signoff_date||npa_signoff_by||npa_signoff_date||
|DEMAND_LETTER|Demand letter|หนังสือทวงถาม|TRUE|LEGAL10Y|case_no, account_no, letter_date, amount_demanded, pay_by_date|TEST-LEGAL-01|2026-11-06|TEST-HEADNPA-01|2026-11-06|
|COURT_NOTICE|Court notice|หมายศาล|TRUE|LEGAL10Y|court_name, black_case_no, notice_date, hearing_date|TEST-LEGAL-01|2026-11-06|TEST-HEADNPA-01|2026-11-06|
|APPRAISAL_REPORT|Appraisal report|รายงานการประเมินราคา|FALSE|GENERAL05Y|appraisal_no, appraisal_date, appraised_value, title_doc_no|TEST-LEGAL-01|2026-11-06|TEST-HEADNPA-01|2026-11-06|
|TITLE_DEED|Title deed|โฉนดที่ดิน|TRUE|LEGAL10Y|title_doc_no, land_office, owner_name, area_sq_wa|TEST-LEGAL-01|2026-11-06|TEST-HEADNPA-01|2026-11-06|
|SETTLEMENT_AGREEMENT|Settlement agreement|สัญญาประนีประนอมยอมความ|TRUE|LEGAL10Y|case_no, agreement_date, settlement_amount, installment_count, borrower_name|TEST-LEGAL-01|2026-11-06|TEST-HEADNPA-01|2026-11-06|
|GUARANTOR_NOTICE|Guarantor notice|หนังสือแจ้งผู้ค้ำประกัน|TRUE|LEGAL10Y|case_no, guarantor_name, notice_date, amount_claimed| | | | |

*A3:* Yes, agreed. Before checking the file (AC3 and AC4), the system first checks that the user is allowed to upload. If not, the upload is refused with MSG-P4-002.

For this to work, these stories must be built first: RWB-E1-022 (sign-in), RWB-E1-019 (roles), RWB-E1-037 (permissions) and RWB-E1-043 (upload and approval service). We will add them to “Depends on” and add a new AC for the “no permission” case.

*A4:* Yes, the new load becomes V3. Version numbers are never reused.

* When V3 is loaded, the pending V2 is closed automatically (status SUPERSEDED) and can no longer be approved. Only the latest pending version can be approved.
* V1 stays live until V3 is approved and its valid-from date is reached.

### Comment 5: VAISHNAVI KAULGE, 2026-11-17T13:22:27.541+0700

Comment ID 1794440

@Chitchaya Muanchonchana 


# *Excel example and initial SQL :*  Excel is available in below jira question and sql script is attached .The SQL that inserts the 6 types with status LOADED. The SQL includes an approval script.

# *File loaded but not approved, then loaded again next week*

* A LOADED version is never used. The last approved version stays in force.
* The same version label again is refused (409), and the first load is unchanged.
* A corrected file with a new version label inserts a new set of rows beside the old set. Old rows are never edited or deleted.
* Proposed: the earlier unapproved version becomes SUPERSEDED and can't be approved.
* The valid-from date must be on or after the business date.

# *Insert logic and running number*

* The running number is per table version: highest version_no + 1, whatever the status of earlier loads.
* Loading more than once is allowed, approved or not. The only refusals are:
** the same version label again;
** an invalid file;
** a past valid-from date.
* A count per doc type isn't stored. It can be derived from the versions.

*Note 2, possible values of document type:* the doc_type_code rows of the approved version in force. Today these are DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE. The list code is LOV-DOC-TYPE, written with hyphens.

*Note 1, E1-019 as prerequisite:* agreed. E1-019 supplies the roles that load and approve. We will add E1-019 and E1-043 to the story's "Depends on".


----

since attachment can’t be there below is sql pasted

----

-- RWB-E1-025 Document types and fields agreed
-- Initial data for table document_type: version DOCTYPE-2026.11, valid from 2026-11-30
-- Target: PostgreSQL, Recovery Workbench Physical Schema v6 (document_type, reference_version)
-- User IDs, load ID and content hash are synthetic example values.
-- A = load, B = approve (commented, run by a different person), C = checks.
-- =====================================================================

-- Pre-checks (must hold before the load runs)
--   * retention classes LEGAL10Y and GENERAL05Y exist in LOV-RETENTION (retention_rule.record_class)
--   * tables reference_version and document_type exist (RWB-E1-043 and RWB-E1-025 migrations)

-- ---------------------------------------------------------------------
-- A. LOAD  (status LOADED, not yet in force)
-- ---------------------------------------------------------------------
BEGIN;

-- A1. Serialise loads of this table. Running number = highest version_no of the table + 1,
--     whatever the status of the earlier loads. Refused loads write nothing, so they take no number.
SELECT pg_advisory_xact_lock(hashtext('REFLOAD:DOCUMENT_TYPE'));

WITH next_no AS (
    SELECT COALESCE(MAX(version_no), 0) + 1 AS n
    FROM   reference_version
    WHERE  table_code = 'DOCUMENT_TYPE'
),
v AS (
    INSERT INTO reference_version
        (table_code, version_no, version_label, valid_from, status,
         author_user_id, row_count, content_hash, load_id)
    SELECT 'DOCUMENT_TYPE', n, 'DOCTYPE-2026.11', DATE '2026-11-30', 'LOADED',
           '00000000-0000-4000-8000-0000000000c1'::uuid, 6, 'c3ca8bcb9df8fa7e2d6121a7229208804ef9056013a1d053970cd196d9e3fd21', '00000000-0000-4000-8000-0000000000d1'::uuid
    FROM next_no
    RETURNING id
)
-- A2. One document_type row per type; all rows carry the same table_version and reference_version_id.
INSERT INTO document_type
    (doc_type_code, label_en, label_th, write_once, retention_class, field_definitions,
     legal_signoff_by, legal_signoff_date, npa_signoff_by, npa_signoff_date,
     table_version, valid_from, reference_version_id)
VALUES
    ('DEMAND_LETTER', 'Demand letter', 'หนังสือทวงถาม', true, 'LEGAL10Y', '[{"name": "case_no", "label": "Case number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "account_no", "label": "Account number", "data_type": "TEXT", "personal": true, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "letter_date", "label": "Letter date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "amount_demanded", "label": "Amount demanded", "data_type": "DECIMAL", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "pay_by_date", "label": "Pay by date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v)),
    ('COURT_NOTICE', 'Court notice', 'หมายศาล', true, 'LEGAL10Y', '[{"name": "court_name", "label": "Court name", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "black_case_no", "label": "Black case number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "notice_date", "label": "Notice date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "hearing_date", "label": "Hearing date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v)),
    ('APPRAISAL_REPORT', 'Appraisal report', 'รายงานการประเมินราคา', false, 'GENERAL05Y', '[{"name": "appraisal_no", "label": "Appraisal number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "appraisal_date", "label": "Appraisal date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "appraised_value", "label": "Appraised value", "data_type": "DECIMAL", "personal": false, "required": true, "extraction_method": "MODEL", "review_only": false}, {"name": "title_doc_no", "label": "Title document number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v)),
    ('TITLE_DEED', 'Title deed', 'โฉนดที่ดิน', true, 'LEGAL10Y', '[{"name": "title_doc_no", "label": "Title document number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "land_office", "label": "Land office", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "owner_name", "label": "Owner name", "data_type": "TEXT", "personal": true, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "area_sq_wa", "label": "Area (square wa)", "data_type": "DECIMAL", "personal": false, "required": true, "extraction_method": "MODEL", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v)),
    ('SETTLEMENT_AGREEMENT', 'Settlement agreement', 'สัญญาประนีประนอมยอมความ', true, 'LEGAL10Y', '[{"name": "case_no", "label": "Case number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "agreement_date", "label": "Agreement date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "settlement_amount", "label": "Settlement amount", "data_type": "DECIMAL", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "installment_count", "label": "Installment count", "data_type": "INTEGER", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "borrower_name", "label": "Borrower name", "data_type": "TEXT", "personal": true, "required": true, "extraction_method": "TEMPLATE", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v)),
    ('GUARANTOR_NOTICE', 'Guarantor notice', 'หนังสือแจ้งผู้ค้ำประกัน', true, 'LEGAL10Y', '[{"name": "case_no", "label": "Case number", "data_type": "TEXT", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "guarantor_name", "label": "Guarantor name", "data_type": "TEXT", "personal": true, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "notice_date", "label": "Notice date", "data_type": "DATE", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}, {"name": "amount_claimed", "label": "Amount claimed", "data_type": "DECIMAL", "personal": false, "required": true, "extraction_method": "TEMPLATE", "review_only": false}]'::jsonb,
     '00000000-0000-4000-8000-0000000000a1', DATE '2026-11-06', '00000000-0000-4000-8000-0000000000b1', DATE '2026-11-06', 'DOCTYPE-2026.11', DATE '2026-11-30', (SELECT id FROM v));

COMMIT;

-- ---------------------------------------------------------------------
-- B. APPROVE  (a different person from the loader; run only after A)
-- ---------------------------------------------------------------------
-- BEGIN;
-- UPDATE reference_version
--    SET status = 'APPROVED',
--        approver_user_id = '00000000-0000-4000-8000-0000000000e1',      -- must differ from author_user_id
--        approved_at = now()
--  WHERE table_code = 'DOCUMENT_TYPE' AND version_label = 'DOCTYPE-2026.11' AND status = 'LOADED';
--
-- -- the approved version it replaces ends the day before this one starts
-- UPDATE reference_version old
--    SET valid_to = DATE '2026-11-30' - 1
--   FROM reference_version new
--  WHERE new.table_code = 'DOCUMENT_TYPE' AND new.version_label = 'DOCTYPE-2026.11'
--    AND old.table_code = 'DOCUMENT_TYPE' AND old.status = 'APPROVED'
--    AND [old.id|https://ddec1-0-en-ctp.trendmicro.com/wis/clicktime/v1/query?url=http%3a%2f%2fold.id&umid=fd6a5153-46d3-47c4-8cf7-38f82de53d9b&rct=1794896304&auth=a695af88d1b673c721f5ff48de7115384eac481f-cfd97fabb9138a645a09aca17070add6a403baf0] <> [new.id|https://ddec1-0-en-ctp.trendmicro.com/wis/clicktime/v1/query?url=http%3a%2f%2fnew.id&umid=fd6a5153-46d3-47c4-8cf7-38f82de53d9b&rct=1794896304&auth=a695af88d1b673c721f5ff48de7115384eac481f-3b5e1221231bb6af7270c6077efe8292b0893a46] AND old.valid_to IS NULL AND old.valid_from < new.valid_from;
--
-- UPDATE document_type dt SET valid_to = rv.valid_to
--   FROM reference_version rv
--  WHERE [rv.id|https://ddec1-0-en-ctp.trendmicro.com/wis/clicktime/v1/query?url=http%3a%2f%2frv.id&umid=fd6a5153-46d3-47c4-8cf7-38f82de53d9b&rct=1794896304&auth=a695af88d1b673c721f5ff48de7115384eac481f-d5fa5237ed062646f7ac0ba18394c9fad3c0f5fb] = dt.reference_version_id AND rv.table_code = 'DOCUMENT_TYPE' AND rv.valid_to IS NOT NULL;
-- COMMIT;

-- ---------------------------------------------------------------------
-- C. CHECKS
-- ---------------------------------------------------------------------
-- C1. Expect 6 types and 26 fields
-- SELECT COUNT(*) AS types, SUM(jsonb_array_length(field_definitions)) AS fields
--   FROM document_type WHERE table_version = 'DOCTYPE-2026.11';
--
-- C2. Document types in force on a business date (this is the LOV-DOC-TYPE value set)
-- SELECT dt.doc_type_code, dt.label_en, dt.retention_class, dt.write_once, dt.table_version
--   FROM document_type dt
--   JOIN reference_version rv ON [rv.id|https://ddec1-0-en-ctp.trendmicro.com/wis/clicktime/v1/query?url=http%3a%2f%2frv.id&umid=fd6a5153-46d3-47c4-8cf7-38f82de53d9b&rct=1794896304&auth=a695af88d1b673c721f5ff48de7115384eac481f-d5fa5237ed062646f7ac0ba18394c9fad3c0f5fb] = dt.reference_version_id
--  WHERE rv.table_code = 'DOCUMENT_TYPE' AND rv.status = 'APPROVED'
--    AND rv.valid_from = (SELECT MAX(valid_from) FROM reference_version
--                          WHERE table_code = 'DOCUMENT_TYPE' AND status = 'APPROVED'
--                            AND valid_from <= DATE '2026-12-01')
--  ORDER BY dt.doc_type_code;

### Comment 6: VAISHNAVI KAULGE, 2026-11-17T13:24:46.501+0700

Comment ID 1794447

@Chanapai Gingpuwaluck 


# Who approves DOCTYPE loads in SIT, UAT and PROD? (Product Owner and Legal to answer)

Our stories name three different approvers:
E1-043 assumes Risk (RW-RISK).
E1-019 assumes team manager (RW-TEAMMGR).
E1-025 and E1-040 assume legal counsel.
DL01 only says "role owners approve each grant". It does not name who holds Reference data A.
Proposal: legal counsel approves DOCUMENT_TYPE in all three environments. SIT and UAT use named test approvers, and PROD uses a named person.
The grant is then added to the permission matrix (RWB-E1-037). Please confirm.

# Actor mismatch

Agreed. We will change the story to "As a reference data administrator (RW-REFADM), I want to load the signed type list…". COE prepares the file only.

# Personal fields

A personal key is already named in the schema comment and in E1-053. The build notes mark four fields as personal: account_no, owner_name, borrower_name and guarantor_name. The card lists two of them.
E1-025 never defines the key list or tests it. We accept the proposal.
Keys to define: name, label, data_type, format, required, personal, extraction_method, review_only, pattern.
Acceptance criterion to add: a load is refused if a field has no data_type or personal flag.
format is new.

# Sign-off pending (Legal and Head of NPA to answer)

DL19 is owned by the Business lead with Legal. It was due 6 Nov and is still open.
The build uses our assumed list meanwhile.
Legal and Head of NPA must name the two signers before E1-050 and E1-053 are built (E1-025 BR1).

# No withdraw

Confirmed gap. E1-043 has a ROLLED_BACK status but no call or test. E1-019 has a rollback call.
Proposal: one rollback call for all reference tables, owned by E1-043 and used by E1-025.
It needs the approve right and a reason.
The earlier version returns to force.
Open work keeps the version it used.


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
