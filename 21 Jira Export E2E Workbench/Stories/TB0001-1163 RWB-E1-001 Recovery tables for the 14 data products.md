# TB0001-1163 [RWB-E1-001] Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Jira | [TB0001-1163](https://scbjira.atlassian.net/browse/TB0001-1163) |
| Type | Story |
| Status | Dev In Progress |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | NATAPATCHARA ANUROJE |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | QA-Reviewed, R-Requirement |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad1 |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:04.695+0700 |
| Updated | 2026-11-18T09:17:02.496+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 8 |
| Comments | 18 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want the recovery tables for the 14 data products created in the ACE database, with a data dictionary and one system of record and one owner per data product, so that every later load has one target table and one accountable owner.

## Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

Scenario: AC1 Schema deployed
Given the migration V0001__rwb_e1_001_recovery_schema.sql and the parameter recoverySchema = "recovery"
When the pipeline applies it in DEV and then in SIT
Then the recovery schema in each environment holds 44 tables: the 41 tables of the data products, sys_objects and sys_fields which hold the data dictionary, and data_product which is the catalog
Then the table loan_account has the 24 columns DF-ACC-001 to DF-ACC-021 and DF-ACC-029 to DF-ACC-031, plus the 7 standard columns
Then the conformance test reports 413 of the 413 fields of these tables matched by name and physical type

Scenario: AC2 Dictionary published
Given the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01
When a developer queries v_data_dictionary for entity "loan_account" and field "days_past_due"
Then the row holds field ID "DF-ACC-014", data type "NUMBER", physical type "integer"
Then source system "Core bank (ALS) via COLLINS", source field "DELAY_DAYS"
Then data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01

Scenario: AC3 One system of record
Given a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID
When the reference data administrator loads it with valid from 2026-11-20
Then data_product holds 14 rows
Then each row has exactly one system of record and one owner user ID
Then the catalog for DP06 names system of record "CCMS" and refresh cycle "WEEKLY"

Scenario: AC4 Failed migration leaves no partial schema
Given a copy of the migration in which the statement creating table valuation fails
When the pipeline applies it in DEV
Then the pipeline stage fails and names the failing statement
Then the recovery schema holds none of the tables of that migration
Then the Flyway history has no successful row for version 1.001

Scenario: AC5 Column without a dictionary entry fails the build
Given a branch that adds the column loan_account.branch_code with no sys_fields row
When the conformance test runs in the pipeline
Then the test fails with "loan_account.branch_code has no data dictionary entry"
Then a sys_fields row DF-ACC-021 whose column is changed to type text fails the test with "DF-ACC-021 physical type date expected, text found"

Scenario: AC6 Repeated migration has no effect
Given the migration version 1.001 already applied in SIT
When the pipeline runs again in SIT
Then Flyway reports version 1.001 as already applied
Then the row counts of sys_objects (41) and sys_fields (413) are unchanged

Scenario: AC7 Catalog row with two systems of record is refused
Given a catalog load file in which DP06 names system of record "CCMS; SVAF"
Given DP11 has no owner user ID
When the reference data administrator loads it
Then the system refuses the load in full with MSG-P1-003 for DP06 and for DP11
Then data_product keeps the rows of the version in force

Scenario: AC8 Catalog with a missing product is refused
Given a catalog load file with 13 rows and no row for DP09
When the reference data administrator loads it
Then the system refuses the load in full with MSG-P1-004 naming "DP09"
Then the system writes no row

Scenario: AC9 Value outside its list
Given a catalog load file in which row 4 (DP04) names owner role "DP_OWNER" and row 5 (DP05) names refresh cycle "HOURLY"
When the reference data administrator loads it
Then the system refuses the load in full with MSG-P1-007 "Row 4: owner_role must be one of the role codes in LOV-ROLE." and "Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE."

Scenario: AC10 Same catalog file loaded again
Given the catalog version loaded on 2026-11-20 is in force
When the reference data administrator loads the same file again
Then the system writes nothing
Then the response carries MSG-P1-011 "The data product catalog load for 2026-11-20 is already complete or running. It was not run again."
```

## Linked issues

- is tested by TB0001-1281: [Testing In Sprint][RWB-E1-001] Recovery tables for the 14 data products  (To Do)

## Sub-tasks

- TB0001-1356 [To Do] [RWB-E1-001] BE - Gate check, branch and domain layer (TASK-00, 01, 07, 08)
- TB0001-1357 [To Do] [RWB-E1-001] BE - Migration, seeds and dictionary conformance (TASK-02..06, 12)
- TB0001-1358 [To Do] [RWB-E1-001] BE - Data product catalog handler, feature flag and tests (TASK-09..11, 13, 14, 16)
- TB0001-1359 [To Do] [RWB-E1-001] BE - Authorisation and release readiness (TASK-15, 17)

## Attachments

- [image-20261111-041309.png](../../Attachments/TB0001-1163/image-20261111-041309.png) (323713 bytes, PIPAT SAENGOW, 2026-11-11T11:14:26.943+0700)
- [image-20261111-041649.png](../../Attachments/TB0001-1163/image-20261111-041649.png) (163801 bytes, PIPAT SAENGOW, 2026-11-11T11:16:57.574+0700)

## Comments (18)

### Comment 1: PREMMAST SUWANNIKOM, 2026-11-10T11:49:54.018+0700

Comment ID 1782757

@Chitchaya Muanchonchana Need confirmation for following question

*RWB-E1-001 specification is blocked on four source conflicts — four decisions needed*

The technical specification for RWB-E1-001 was re-run on 10 November 2026 against {{Recovery Workbench Physical Schema v4.sql}} rather than the story's prose totals. Every count in the story was re-verified; most hold. Four conflicts, however, cannot be resolved from any source we have, and each makes the migration or an acceptance criterion fail as the story currently stands. We need a ruling on each before the build can start.

Three of the four (questions 1, 3 and 4) each stop the migration on their own. The migration runs in a single transaction, so any one of them discards the whole schema — answering fewer than all three does not give us a migration that deploys.

----

h3. Question 1 — the data product catalog cannot hold every value {{sys_objects}} references

*What we found.* Physical Schema v4 declares:

{code:sql}ALTER TABLE sys_objects ADD CONSTRAINT fk_sys_objects_data_product{code}

{{  FOREIGN KEY (data_product) REFERENCES data_product (product_code) ON DELETE RESTRICT;}}

Of the 108 {{sys_objects}} seed rows in that file, 33 carry a {{data_product}} value that is not one of DP01 to DP14:

||Code||Rows||Example objects||
|{{OPS}}|22|{{load_run}}, {{dq_rule}}, {{tracker_inventory}}, {{interface_config}}, {{outbox_event}}, {{feature_flag}}|
|{{AGT}}|8|{{agent_policy}}, {{agent_run}}, {{agent_evaluation}}, {{agent_alert}}|
|{{RPT}}|3|{{measure_definition}}, {{measure_snapshot}}, {{measure_publish}}|

The Logical Data Model and Data Dictionary v6 (Entities tab) assigns the same 33 entities to the same three codes, so these are deliberate modelling, not a typo in the SQL.

*Why it blocks.* D-RCV-29 (DL41) requires the baseline migration to seed the full dictionary — all 108 {{sys_objects}} and all 1,256 {{sys_fields}} rows. AC3 and AC8 require {{data_product}} to hold exactly the 14 products DP01 to DP14. With the foreign key in place, those two requirements cannot both be met: the migration fails on 33 rows, so nothing in this story deploys.

*Options.*

|| ||Option||Consequence||
|*C* _(our recommendation)_|Do not create {{fk_sys_objects_data_product}} in this story; add it in the story that first needs it to be enforced.|Smallest deviation. The full dictionary seed stands, the catalog stays at 14 rows, AC3 and AC8 are unchanged. The constraint is lost until a later story.|
|*A*|Seed {{data_product}} with 17 rows: DP01 to DP14 plus {{AGT}}, {{OPS}} and {{RPT}} as operational products that the catalog load does not own.|Needs 3 further {{LOV-DATA-PRODUCT}} values (that list is seeded with exactly the 14 DP codes today, and {{DF-REF-071}} carries {{lov_code = LOV-DATA-PRODUCT}}), and an explicit exclusion of the three operational codes in the catalog validation, so AC3 and AC8 keep meaning "the 14 business products".|
|*B*|Seed {{sys_objects}} and {{sys_fields}} only for the 44 tables this story creates (44 objects, 533 fields).|Contradicts D-RCV-29, and departs furthest from the BA's own data model, which assigns all 108 objects to a product.|

*Please confirm: A, B, C, or another answer.*

----

h3. Question 2 — {{v_data_dictionary.owner_role}} is empty, so AC2 cannot pass

*What we found.* Every one of the 1,256 {{INSERT INTO sys_fields}} statements in Physical Schema v4 uses the same 12-column list:

{noformat}(field_id, object_name, field_name, data_type, physical_type, is_mandatory,{noformat}

{{ lov_code, references_object, source_system, source_field, is_personal, description)}}

The table also has {{owner_role}}, {{refresh_cycle}}, {{late_behavior}} and {{interface_id}}, and the seed never populates them — they are NULL on all 1,256 rows. {{v_data_dictionary}} in the same file takes {{owner_role}} from {{sys_fields}}:

{noformat}SELECT ... f.owner_role, p.owner_user_id, p.refresh_cycle ...{noformat}

{{FROM sys_fields f JOIN sys_objects o ... LEFT JOIN data_product p ...}}

*Why it blocks.* AC2 requires the row for {{loan_account.days_past_due}} to return {{owner role "RW-DATASTEW"}}. As the schema stands, the view returns NULL for it. AC2 and its test case cannot pass.

Note that story §12 always described {{owner_role}} as coming from {{data_product}}, not from {{sys_fields}} — it is the physical schema's view that differs from the story, not the other way round. Story §12 also names two view columns, {{product_system_of_record}} and {{entity_system_of_record}}, which the view does not have, and omits {{references_object}}, {{late_behavior}} and {{interface_id}}, which it does.

*Options.*

|| ||Option||Consequence||
|*1* _(our recommendation)_|Change {{v_data_dictionary}} to take {{owner_role}} from {{data_product}}, as story §12 always said.|{{data_product.owner_role}} is {{NOT NULL}} and seeded {{RW-DATASTEW}}, so AC2 passes once DP01 is in the catalog. The four unpopulated {{sys_fields}} columns stay NULL until RWB-E1-064 gives the dictionary its own maintenance path. Makes this a physical-schema defect rather than a story defect.|
|*2*|Extend the migration's {{sys_fields}} seed to populate {{owner_role}} (and where known {{refresh_cycle}}, {{late_behavior}}, {{interface_id}}) per field.|1,256 values that no source supplies today — the Fields tab of LDM v6 has no owner-role, refresh-cycle, late-behaviour or interface-ID column.|
|*3*|Re-read AC2 as asking for the data product's owner role.|A narrower restatement of option 1; the view is corrected the same way.|

*Please confirm: 1, 2, 3, or another answer.*

----

h3. Question 3 — the {{delegation_limit}} seed cannot run

*What we found.* D-RCV-29 requires the baseline migration to seed {{delegation_limit}}. All 24 {{INSERT INTO delegation_limit}} statements in Physical Schema v4 use the same 4-column list:

{code:sql}INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from){code}

{{VALUES ('ALL', 'L1', 'MORTGAGE', DATE '2026-11-30');}}

The table, in the same file, declares two further mandatory columns with no default:

{noformat}limit_version   varchar(20) NOT NULL,{noformat}

{{regulation_item varchar(10) NOT NULL,}}

Every one of the 24 rows therefore raises a not-null violation. We ran the same check on every other table the baseline seeds — {{sys_objects}}, {{sys_fields}}, {{lov_value}}, {{role}} and {{permission}} all pass; {{delegation_limit}} is the only one that fails.

*Why it blocks.* The migration is one transaction, so the first failing row discards the entire schema. This is independent of questions 1 and 2: answering those two still leaves the migration failing here.

*Options.*

|| ||Option||Consequence||
|*1* _(our recommendation)_|Supply the {{limit_version}} and {{regulation_item}} values for the 24 rows.|{{limit_version}} is most likely one constant per matrix version — {{permission.matrix_version}} is {{'1'}} throughout the same seed — but we will not guess it, and {{regulation_item}} we cannot derive at all.|
|*2*|Drop {{NOT NULL}} from both columns in the baseline, if the delegation-of-authority matrix does not in fact require them per row.|A schema change, so it needs your agreement as the model's owner.|
|*3*|Leave {{delegation_limit}} empty in the baseline and load the 24 rows through RWB-E1-043 as reference data.|Consistent with D-RCV-28, which already says later reference changes are loads rather than migrations.|

*Please confirm: 1, 2, 3, or another answer.* If option 1, we need the 24 pairs of values.

----

h3. Question 4 — the 14 data products have no definition text

*What we found.* {{data_product.definition}} is {{varchar(400) NOT NULL}}. The seed table in story §13 gives four columns — product, name, system of record, refresh cycle — and no definition. Physical Schema v4 contains no {{data_product}} insert at all, so there is no fallback. The 14 values do not exist in any source as a per-product definition.

*Why it blocks.* The seed cannot be written, and a not-null violation discards the migration.

*Options.*

|| ||Option||Consequence||
|*1* _(our recommendation)_|Supply the 14 definitions, or confirm that we may derive them from the subject-area descriptions in Conceptual Data Model v5.|The mapping there is not one-to-one — DP03 covers both "Case" and "Work management", for example — so if we derive them we need you to state the composition rule.|
|*2*|Make {{definition}} nullable in the baseline and require it on the catalog load.|Fits the story's own guardrail that product names and descriptions are data supplied by the catalog load, not values in code.|

*Please confirm: 1, 2, or another answer.* If option 1, we need the 14 definitions or the rule.

### Comment 2: CHANISSARA MAHAKITTIKUN, 2026-11-10T16:44:33.197+0700

Comment ID 1783899

@PREMMAST SUWANNIKOM 

h2. 1. Rulings at a glance

|*Question*|*Initial-phase best answer*|*Beats the minimal answer because*|
|Q1 — FK vs catalog|D (new option) — make sys_objects.data_product nullable, set the 33 operational rows to NULL, keep the FK|Fixes the real defect (overloaded column) from day one instead of deferring a knowingly-broken reference|
|Q2 — NULL owner_role|1 — the view takes owner_role from data_product, plus full section-12 alignment of the view in one pass|No consumers exist yet, so align the view to the contract completely, not just one column|
|Q3 — delegation_limit seed|3, amended|Already the root-cause answer; the real content belongs to RWB-E1-038|
|Q4 — missing definitions|1 — definitions from the CDM v5 Data products tab|Already the root-cause answer; the text is one-to-one for all 14 products|

h2. 2. Q1 — best: fix the overloading, keep the FK

The evidence supports the model correction better than deferral:

* LDM DF-REF-091 already anticipates it. Its own meaning text reads: "Data product the object belongs to, *DP01 to DP14 or None*". The Mandatory = Yes flag is the inconsistent part.
* Nothing is lost by emptying the 33 rows. For all 33, subject_area already equals data_product (OPS/AGT/RPT) — the subject_area column is the legitimate home for that classification.
* The story's own text survives unchanged. Section 13's "inserts the data_product seed rows before the sys_objects rows" and the FK statement both remain true. The 68-FK count in flow step 2 (and defect-register row 10, which records "68 FKs matching Physical Schema v4") stays accurate — deferring the FK would have silently changed it to 67.
* Every AC holds. AC1 (44 tables), AC3/AC8 (14 catalog rows), AC6 (108/1,256 after the count correction in section 6), and D-RCV-29's completeness counts. D-RCV-29 needs one wording amendment: "data_product empty for the 33 operational entities, which carry OPS/AGT/RPT in subject_area."

Required edits (details in clauses 1.1–1.8 of the Specification Rulings pack):

# LDM v6 → v7: DF-REF-091 → Optional, and the Entities tab drops OPS/AGT/RPT from the Data product column (they stay in Subject area).
# Physical Schema v4 → v5: sys_objects.data_product varchar(10) nullable; FK fk_sys_objects_data_product retained as declared.
# Story section 13: the seed statement becomes "75 sys_objects rows carry a data product; 33 operational entities leave it empty."
# Migration order unchanged: catalog rows → sys_objects → sys_fields.

h2. 3. Q2 — best: one full view alignment, not one line

The view takes owner_role from data_product — but do the whole reconciliation in one pass, since nobody consumes the view yet:

{noformat}-- align to story §12 exactly{noformat}

{noformat}o.system_of_record AS entity_system_of_record,   -- add (missing today){noformat}

{noformat}p.system_of_record AS product_system_of_record,  -- add (missing today){noformat}

{noformat}p.owner_role,                                    -- replace f.owner_role{noformat}

One naming decision to make now while it costs nothing: section 12 calls the flags {{mandatory}} and {{personal}}; the view exposes {{is_mandatory}} / {{is_personal}}. Update section 12 to the view's names (it matches every other physical column); either is fine, but it must be one set, not two.

h2. 4. Q3 — best: no placeholder rows, ever

Already the root-cause fix:

* The 24 rows are {{decision_code = 'ALL'}}, which is not in LOV-DECISION (D1–D9 plus X1–X7). They are a placeholder grid, not a subset of the 95-limit matrix.
* RWB-E1-038 is the content owner: it loads DOA-2026.11 — 218 rows from the 95 matrix limits (109 MORTGAGE + 109 SSME) — with limit_version and regulation_item properly populated.
* Chapter 8 limits (the 12 HIRE_PURCHASE/UNSECURED rows) "load when supplied (DL18)" per the matrix; they cannot be invented for a baseline.

Pre-build extras while editing:

* Delete the 24 stray inserts from Physical Schema v5 entirely — do not just comment them in the migration; the source file is what the next story copies.
* Amend D-RCV-29: remove delegation_limit from the seed list. The story's flow step 3 never mentioned it anyway, so this re-aligns the ruling with the story rather than diverging from it.
* RWB-E1-043's AC2 fixture (24 rows) stays valid as a version-mechanism test, but its rows should carry limit_version/regulation_item values so it is shape-consistent with real loads.
* RWB-E1-038 section 13 says its migration "adds" limit_version/regulation_item — but v4 already declares them. Correct E1-038 to say the columns come from V0001 and the story's migration adds only the lookup index ix_delegation_lookup, which is not yet in the schema file.

h2. 5. Q4 — best: seed the definitions, keep NOT NULL

Sourced from the CDM v5 Data products tab (identical text in Data Ownership v2); all 14 fit varchar(400) (longest 143 characters). The mapping is one-to-one for the 14 products — the non-one-to-one case is only on the Subject areas tab, so no composition rule is needed.

Pre-build extras:

* Correct story section 13's DDL outlier to {{definition varchar(400) not null}} (matching the LDM and the schema).
* Have each product's business owner approve the wording on record.

### Comment 3: PREMMAST SUWANNIKOM, 2026-11-10T19:40:08.114+0700, edited 2026-11-10T19:41:51.222+0700

Comment ID 1784386

@Jesniphat Pukkham  Please approve  the following questions ka .

*RWB-E1-001 — two naming decisions D-RCV-47 does not cover*

D-RCV-47 requires the {{rwb_}} prefix on every recovery *table, sequence and index ****. RWB-E1-001 is the first story to create objects outside that list — 1 view, 1 function, 2 triggers, 68 foreign keys and 21 named unique constraints — and the RWB-E1-044 lint says object kinds outside its list are an accepted gap left to code review, so nothing catches a wrong choice. Two proposals below; please confirm or correct. The same rule also fixes a problem in RWB-E1-043, noted after them.

----

h3. 1. Which object kinds carry the prefix

*Rule we propose: prefix what must be unique within the schema, leave what is only unique within its own table.*

||Object||Prefix||Unique within||
|Table, sequence, index|*Yes*|Schema {{ace}} — all share one namespace, so an index can even collide with a table name|
|View|*Yes* — {{rwb_v_data_dictionary}}|Schema {{ace}}|
|Function|*Yes* — {{rwb_refuse_change()}}|Schema {{ace}}|
|*Named UNIQUE constraint*|*Yes* — {{rwb_uq_*}}|*Its index is schema-level and carries the constraint's own name*|
|Trigger|No|Its own table|
|Foreign key|No|Its own table — creates no index|
|CHECK|No|Its own table|
|Primary key|—|Declared inline with no name, so PostgreSQL names the index {{rwb_<table>_pkey}} on its own|

Unique constraints look like the odd one out, and that is the point: it is an index rule, not a constraint rule. {{uq_loan_account}} would be an index called {{uq_loan_account}} sitting in {{ace}} beside ACE core's objects. A foreign key creates no index, so its name never leaves its table.

We did consider dropping the names and letting PostgreSQL generate them. The longest result here is 63 characters — PostgreSQL's identifier limit exactly, with no margin before silent truncation. Explicit names are 41 at most.

----

h3. 2. One spelling — we propose RWB-E1-043's

|| ||RWB-E1-001 (from Physical Schema v4)||RWB-E1-043 (from its plan)||
|Unique|{{uk_}}|{{uq_}}|
|Trigger|{{tr_}}|{{trg_}}|

*We propose* {{uq_}} *and* {{trg_}}: they read as what they are, and the Physical Schema v4 spelling exists only as DDL text we are rewriting anyway. That puts the work on RWB-E1-001 — 21 constraints and 2 triggers renamed, against 3 in RWB-E1-043.

----



h3. {color:#6a9a23}RWB-E1-043 is affected and needs the same fix  {color}[https://scbjira.atlassian.net/browse/TB0001-1344|https://scbjira.atlassian.net/browse/TB0001-1344|smart-link] 

Three constraints in its approved plan fail the lint under rule 1:

{noformat}uq_reference_version_table_version        →  rwb_uq_reference_version_table_version
uq_reference_version_table_validfrom_hash →  rwb_uq_reference_version_table_validfrom_hash
uq_reference_row_version_key              →  rwb_uq_reference_row_version_ke{noformat}

### Comment 4: PREMMAST SUWANNIKOM, 2026-11-10T20:34:55.103+0700, edited 2026-11-10T20:35:55.675+0700

Comment ID 1784432

@PIPAT SAENGOW Could you help check two things on the ACE database? 

*RWB-E1-001 — two facts needed about the ACE database*

All 44 tables in this story take their primary key from {{gen_random_uuid()}}, and line 8 of {{Recovery Workbench Physical Schema v4.sql}} is {{CREATE EXTENSION IF NOT EXISTS pgcrypto;}}. Whether our migration keeps that line decides whether it runs at all — if the function does not resolve, the migration fails at its first {{CREATE TABLE}}. We cannot tell from the repository: no ACE core migration under {{backend/src/main/resources/db/migration/}} mentions {{pgcrypto}} or {{gen_random_uuid}}.

Two questions, both answerable from the server:

# *What is the PostgreSQL major version in DEV, SIT, UAT and PROD?*

{noformat}SHOW server_version;{noformat}

From PostgreSQL 13 onward {{gen_random_uuid()}} is built in and no extension is needed.

# *Is* {{pgcrypto}} *already installed in the ACE database?*

{code:sql}SELECT extname, extversion FROM pg_extension WHERE extname = 'pgcrypto';{code}

*What we do with the answers.* On 13 or later, or with the extension already present, we drop line 8 and the recovery migration installs nothing — which is what D-RCV-47 asks of us, since an extension is database-wide rather than scoped to the {{ace}} schema. Only if neither holds do we come back and ask who installs it, and when.

cc @PONGCHAI CHAROENRUNGRODKUN @Pe Chichareon 

### Comment 5: Jesniphat Pukkham, 2026-11-10T22:35:22.959+0700

Comment ID 1784476

@PREMMAST SUWANNIKOM Approved

### Comment 6: PIPAT SAENGOW, 2026-11-11T11:07:01.250+0700

Comment ID 1784924

[Just unsolicited advice please don’t worry about it.]

K' @Chitchaya Muanchonchana It seems from skimming of this requirement that Henka is trying to replicate Databricks Unity Catalog. Does Henka really want to do this? Databricks is extensively used within SCB and can provides schema permission, data dictionary, manual upload ui, and more.   Databricks is an approved solution so it could be easily deployed within SCB and saves your development time.

### Comment 7: PIPAT SAENGOW, 2026-11-11T11:14:27.154+0700, edited 2026-11-11T11:17:58.875+0700

Comment ID 1784959

@PREMMAST SUWANNIKOM 

!image-20261111-041309.png|width=485,alt="image-20261111-041309.png"!



command work yes. Tested on Dev DB



!image-20261111-041649.png|width=589,alt="image-20261111-041649.png"!





Database version for all ENV



K' @PREMMAST SUWANNIKOM . Have anyone from TechX managed to access the development database yet or is there still issue? Additionally, do you have AZ portal access? Have P' @PONGCHAI CHAROENRUNGRODKUN  granted the required group to you? If there any permission missing please let P’TEE know quickly because those access are important.

### Comment 8: PREMMAST SUWANNIKOM, 2026-11-11T13:31:55.187+0700

Comment ID 1785279

@Chitchaya Muanchonchana  Please apporve ka

the *Backlog and specification approval* gate for RWB-E1-001. The specification is complete and its compliance gate no longer blocks.๑๑

*Where it stands*

|Specification|{{SUCCESS}} — 23 {{SPEC-RWB-E1-001-*}} items, 18 test cases, 0 open clarifications|
|Compliance gate|gate 008, 2026-11-11: {{FAIL}} with *Low findings only*, which per {{pdlc.md}} does not stop the handoff. Six gates were run; every finding is applied except the Traceability Manager's matrix expansion|
|Artefacts|{{output/INC-010-epic-1-RWB-E1-001/specify/}}|

The specification was re-run against {{Recovery Workbench Physical Schema v4.sql}} rather than the story's prose, and every figure in it was counted from that file and re-counted independently at each gate: 44 tables, 841 columns, 76 indexes, 68 foreign keys, 21 unique constraints, and seeds of 108 {{sys_objects}} / 1,256 {{sys_fields}} / 598 {{lov_value}} / 54 {{role}} / 421 {{permission}} / 14 {{data_product}}.

*The five conflicts that were found, and how each was closed*

|| ||Conflict||Ruling||
|CLAR-007|33 of the 108 {{sys_objects}} seed rows carry {{OPS}} / {{AGT}} / {{RPT}}, which a 14-row catalog cannot hold, so the foreign key failed|D-RCV-51 (BA) — the column becomes nullable; those 33 keep their classification in {{subject_area}}|
|CLAR-015|The {{sys_fields}} seed never populates {{owner_role}}, so AC2's {{RW-DATASTEW}} could not be returned|D-RCV-52 (BA) — the view takes {{owner_role}} from {{data_product}}, as story §12 always said|
|CLAR-017|All 24 {{delegation_limit}} inserts omit two {{NOT NULL}} columns|D-RCV-53 (BA) — not seeded here; RWB-E1-038 owns the real 218 rows|
|CLAR-018|No source gave the 14 {{data_product.definition}} values|D-RCV-54 (BA) — taken from the Conceptual Data Model v5|
|CLAR-019|D-RCV-47 names only tables, sequences and indexes; this story is the first to create a view, a function, triggers and 68 foreign keys|D-RCV-55 — approved by the recovery tech lead 2026-11-10|
|CLAR-020|Whether the migration installs {{pgcrypto}}|D-RCV-56 — it installs no extension; {{gen_random_uuid()}} is built into PostgreSQL from 13|

*What you would be approving alongside it.* One item, with an owner:

* *OPEN-039* — the same naming rule needs three constraint renames in the already-approved RWB-E1-043 plan, tracked on {{TB0001-1344}}. It does not affect this story's build.

Two items that were open when this request was drafted are now closed. *OPEN-038*, the PostgreSQL version behind D-RCV-56, was answered on 2026-11-11: all four environments run 17.11, so {{gen_random_uuid()}} is built in and the migration installs no extension. *OPEN-032 and OPEN-033*, which waited on the BA to reissue LDM v7, Physical Schema v5 and the story text, are closed by *D-RCV-57*: the base of record is Physical Schema v4 plus the rulings in the squad's decision register, because the Implementation Builder reads this specification rather than the BA's source files. D-RCV-57 carries the residual risk in writing — a later story copying that file raw would reintroduce what the rulings removed — and every migration story must apply the same deltas.

### Comment 9: PREMMAST SUWANNIKOM, 2026-11-11T13:36:23.684+0700

Comment ID 1785299

@PIPAT SAENGOW  Thanks for the version check ka
*Development database access — still blocked.* Nobody from TechX has connected yet. We are stuck at the VPN: without it we cannot reach the database.

### Comment 10: Chitchaya Muanchonchana, 2026-11-11T13:40:49.266+0700, edited 2026-11-11T13:51:09.318+0700

Comment ID 1785314

@PREMMAST SUWANNIKOM Backlog and specification is approved.

### Comment 11: PREMMAST SUWANNIKOM, 2026-11-11T15:29:45.897+0700

Comment ID 1785814

@Jesniphat Pukkham  please appove plan and task ka.

*plan approval* and *task approval* for RWB-E1-001 — the same pair you gave RWB-E1-044 and RWB-E1-043 on 2026-11-10.

*Where it stands*

|Plan|{{output/INC-010-epic-1-RWB-E1-001/plan/}} — plan, 18 tasks, data model, contracts, 18 test scenarios|
|Plan gate|*No blocking findings left.* Two rounds: the first raised 2 Medium and 7 Low, all applied; the re-review raised one Low, also applied|
|Spec|{{SUCCESS}}. Backlog and specification approved by Chitchaya Muanchonchana, 2026-11-11|

The two Medium findings were a coverage row pointing at the wrong task, and a missing delta — both fixed and re-reviewed. Both rounds stay recorded as {{FAIL}} because {{pdlc.md}} keeps that status on any review that found something; severity decides blocking, and Low-only does not stop a handoff.

*Two judgement calls worth your eye*

# *The migration is generated, not hand-written.* {{data-model.md}} specifies a scripted transformation of Physical Schema v4 with a 16-item delta list; TASK-02 generates the file and TASK-03 verifies it back against the source by parsing both. RWB-E1-043 carries literal DDL because its migration is two tables. This one is 44 tables and 841 columns out of a 6,652-line source, where a pasted block would be checked against nothing and could not be re-derived if the schema is reissued.

# *Delta 14 fixes a dictionary row the rulings left behind.* D-RCV-51 made {{sys_objects.data_product}} nullable, but the {{sys_fields}} seed row describing it, {{DF-REF-091}}, still ships {{is_mandatory = true}} — and D-RCV-57 closed the Physical Schema v5 reissue that would have fixed it. The conformance test compares name and physical type, not nullability, so nothing catches it. The migration now sets that row to {{false}}. Recorded as *derived* from D-RCV-51 with BR1 rather than as a new decision, with {{plan.md}} §Risks saying plainly that you or BA may overrule and leave the seed untouched. OPEN-034 carries it.

*What this approval does not unlock*

The Builder still cannot start, and TASK-00 and TASK-01 stop it rather than stubbing anything:

* *RWB-E1-044 and RWB-E1-043 are not implemented.* Both have a spec and a plan; neither has an {{implement/}} run, and {{TB0001-1344}} is still {{To Do}}.
* {{ReferenceTableHandler}} *has no owning specification* (OPEN-035). Story §12 is the only place it is written out, and 7 of the 18 tasks are designed against it; the RWB-E1-043 spec publishes {{ReferenceVersionRegistry}} and {{ReferenceDataService}} only. That spec needs a re-run.
* *OPEN-019* — the Jenkins recovery step must run as {{ACEDbFlywayRole_<ENV>}}, or ACE's default privileges will not reach the new {{rwb_}} objects. Blocks deployment, not the build.

*One thing to settle while you are here*

D-RCV-15 names EPIC-001, INC-001 and INC-002 only, so every later increment comes back to you for these same two gates — RWB-E1-043 and this story have both had to ask separately. If covering the whole squad was the intent, extending the decision would save the round trip.

*Please approve, or name what you want changed.*

### Comment 12: Jesniphat Pukkham, 2026-11-11T16:03:45.319+0700

Comment ID 1785950

@PREMMAST SUWANNIKOM Approved

### Comment 13: NATAPATCHARA ANUROJE, 2026-11-12T10:54:43.188+0700

Comment ID 1787084

@Jesniphat Pukkham @Chitchaya Muanchonchana

h2. Owner decisions needed before resuming TB0001-1356

* *OPEN-041:* Please initiate the Context Updater and arrange the affected-story impact review. A local implementation draft was started before this review; it remains uncommitted and needs an explicit disposition.
* *Plan and task dependencies:* The approved task list stops when PRE-6 or PRE-7 is absent, while TB0001-1356 says TASK-07 and TASK-08 can start despite TASK-01 being blocked. Please decide the intended dependency and review and approve any amended plan/tasks. The draft also includes a boundary-test tooling change not named in the current plan; please review its scope.
* *Catalog confirmation authority:* Please coordinate with the access-control owner to reconcile RWB-E1-001 SPEC-018/020 with RWB-E1-043 SPEC-005 and its CLAR-001/PRE-3 disposition. The generic clarification contains an assumption and does not settle the catalog-specific rule. Please record the outcome and update the affected specification/plan where required.

This comment requests decisions only; it does not record an approval or authorize a permission change. The supporting implementation report is local and uncommitted.

### Comment 14: Jesniphat Pukkham, 2026-11-12T11:28:54.120+0700

Comment ID 1787209

@NATAPATCHARA ANUROJE Approve ครับ

### Comment 15: NATAPATCHARA ANUROJE, 2026-11-13T09:49:07.720+0700, edited 2026-11-13T10:31:26.589+0700

Comment ID 1789062

h3. Plase confirmation request: Data Product Catalog approval

Following our verbal discussion, please confirm the authorization for step 8 of RWB-E1-001, where the catalog is confirmed after loading and validation:

* Follow the RWB-E1-043 Reference Data approval process for the catalog, rather than the Reference data U confirmation stated in RWB-E1-001.
* The approver is RW-RISK, holds Reference data A, and must be different from the person who loaded the catalog.
* Update the permission matrix to grant Reference data A to RW-RISK through the access-control owner's approval process. This comment does not itself grant the permission.

Background: RWB-E1-001 specifies Reference data U for confirmation, while the RWB-E1-043 approval contract requires Reference data A. RW-RISK is currently an assumption in the 043 specification, and the existing permission matrix does not grant that role Reference data A.

Please reply *Approved* if this accurately reflects the business decision, or specify any corrections. Approval from the access-control owner is also required for the permission change. The affected specification, plan, contract and tests must then be reconciled and reviewed again before implementation.

References: REVIEW-RWB-E1-001-PLAN-004-F-01; RWB-E1-001 SPEC-018/020; RWB-E1-043 approval contract.

### Comment 16: Chitchaya Muanchonchana, 2026-11-16T09:11:57.207+0700

Comment ID 1791603

@NATAPATCHARA ANUROJE Approved ka.

### Comment 17: Chitchaya Muanchonchana, 2026-11-17T09:09:09.946+0700

Comment ID 1793704

Pending E1-043 to finish before start the ticket

### Comment 18: Nitchayaphan Kanpirompachira, 2026-11-17T12:21:34.371+0700

Comment ID 1794359

*Clarification needed:*

# *Migration concurrency — duplicate trigger*

If the pipeline is triggered twice at (near) the same time (e.g. a duplicate CI run against the same commit), both attempts try to apply {{V0001__rwb_e1_001_recovery_schema.sql}} against an empty DB concurrently.

*Question:* Is this serialised by Flyway's lock (second run waits, then no-ops since the version is already applied), or does it fail some other way? Is it already covered by an existing AC / pipeline test?


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
| QA Owner | customfield_12725 | Piyawan Sanpanya |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Rework | customfield_17514 | Rework |
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
