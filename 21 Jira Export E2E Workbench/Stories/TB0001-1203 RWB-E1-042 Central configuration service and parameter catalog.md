# TB0001-1203 [RWB-E1-042] Central configuration service and parameter catalog

| Field | Value |
|---|---|
| Jira | [TB0001-1203](https://scbjira.atlassian.net/browse/TB0001-1203) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Nuttapon Jittachotisak |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, QA-Reviewed, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad1; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:40.571+0700 |
| Updated | 2026-11-17T09:59:24.040+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 6 |
| Comments | 11 |

## Description

As a squad member (RW-TRIBE), I want every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used, so that no value is hard-coded and every parameter has an owner.

## Acceptance criteria

```gherkin
Feature: Central configuration service and parameter catalog

  Background:
    Given the catalog lists "case.entry.dpd" as INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by "recovery.casewf.casecreation"

  Scenario: AC1 Parameter read at run time
    Given the parameter "case.entry.dpd" set to 90 in PROD, version 1
    When the case service evaluates entry on 2026-12-01
    Then it uses 90 from the service, not a constant in code
    Then the entry decision records parameter version 1

  Scenario: AC2 Hard-coded value caught
    Given code in package "recovery.casewf.casecreation" with a literal 90 in the entry rule
    When the lint rule for magic numbers runs in the build
    Then the build fails
    Then the output names the file, the line and the parameter "case.entry.dpd"

  Scenario: AC3 Catalog complete
    Given the parameter catalog
    Given code that reads the key "allocation.retry.limit" which the catalog does not list
    When the pipeline compares the catalog with the parameters read by the services
    Then the build fails naming "allocation.retry.limit"
    Then every other parameter in use is in the catalog with an owner and a default

  Scenario: AC4 Required value missing at start-up
    Given "refdata.cache.ttl-seconds" is required and has no value and no default for UAT
    When the service starts in UAT
    Then the health check fails with MSG-P3-032 for "refdata.cache.ttl-seconds" and "UAT"
    Then the service takes no traffic

  Scenario: AC5 Value outside its range
    When RW-COE loads "case.entry.dpd" = 400 for PROD
    Then the system refuses the load with MSG-GEN-002 with minimum 1 and maximum 365

  Scenario: AC6 Wrong type
    When RW-COE loads "case.entry.dpd" = "ninety" for PROD
    Then the system refuses the load with MSG-P1-002 and check "value is not INTEGER"

  Scenario: AC7 Author cannot approve
    Given RW-COE user U-41 loaded value version 3
    When U-41 approves version 3
    Then the system refuses the approval with MSG-P7-002

  Scenario: AC8 Values per environment
    Given "refdata.cache.ttl-seconds" is 30 in SIT and 300 in PROD
    When the reference data service reads it in SIT and in PROD
    Then SIT uses 30 and PROD uses 300

  Scenario: AC9 Secrets are listed, never served
    Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
    When GET /admin/parameters is called by RW-COE
    Then the entry shows owner, environments and used by
    Then the system returns no value for "ace.db.password"

  Scenario: AC10 Rollback of a value version
    Given value version 2 of "case.entry.dpd" is in force and version 1 was in force before it
    When RW-COE calls rollback for version 2
    Then version 1 is in force and the service returns 90

  Scenario: AC11 A new value takes effect on its valid from date
    Given version 2 sets "case.entry.dpd" to 91 for PROD with valid from 2026-12-10 and is approved on 2026-12-05
    When the case service evaluates entry on 2026-12-09 and on 2026-12-10
    Then it uses 90 on 2026-12-09 and 91 on 2026-12-10
    Then the system restarts no instance
```

## Sub-tasks

- TB0001-1361 [In Progress] RWB-E1-042: nested Modulith fixture (stop condition)
- TB0001-1362 [To Do] RWB-E1-042: external gate, INC-001 (RWB-E1-044) on develop-recovery
- TB0001-1365 [In Progress] RWB-E1-042: architecture guards and build checks
- TB0001-1366 [In Progress] RWB-E1-042: P3 published types, catalog CSV, generators, messages, migration, entities
- TB0001-1367 [In Progress] RWB-E1-042: P4 access - port types, clock, caller identity, capability policy, error advice, load/approve/rollback endpoints
- TB0001-1368 [In Progress] RWB-E1-042: P3 config service - runtime mode, converter, ParameterService, cache, startup check, health
- TB0001-1369 [In Progress] RWB-E1-042: P3 PARAMETER handler and GET /admin/parameters
- TB0001-1370 [In Progress] RWB-E1-042: API Tester harness on bootTestRun (test code only)
- TB0001-1371 [In Progress] RWB-E1-042: verification, contract check, coverage gate, footprint, evidence
- TB0001-1393 [To Do] RWB-E1-042: REVIEW-074 fix, write reference_load before staging rows
- TB0001-1394 [To Do] RWB-E1-042: batch-merge hold check (SPEC-012 five conditions)
- TB0001-1363 [Cancelled] RWB-E1-042: move RWB-TE-001 packages to th.co.scb.ace.workbench.recovery
- TB0001-1364 [Cancelled] RWB-E1-042: restore recovery JaCoCo tasks (gate on test.exec only)

## Attachments

- [image-20261109-093824.png](../../Attachments/TB0001-1203/image-20261109-093824.png) (36641 bytes, Nuttapon Jittachotisak, 2026-11-09T16:46:11.512+0700)
- [image-20261109-093924.png](../../Attachments/TB0001-1203/image-20261109-093924.png) (167424 bytes, Nuttapon Jittachotisak, 2026-11-09T16:46:11.325+0700)
- [image-20261109-093948.png](../../Attachments/TB0001-1203/image-20261109-093948.png) (176567 bytes, Nuttapon Jittachotisak, 2026-11-09T16:46:11.416+0700)
- [parameter.csv](../../Attachments/TB0001-1203/parameter.csv) (326 bytes, Nuttapon Jittachotisak, 2026-11-10T18:13:00.175+0700)
- [RWB-E1-042  Central configuration service and parameter catalog.txt](../../Attachments/TB0001-1203/RWB-E1-042%20Central%20configuration%20service%20and%20parameter%20catalog.txt) (14830 bytes, Pe Chichareon, 2026-11-15T10:15:17.322+0700)
- [Screenshot 2569-11-12 at 09.14.27.png](../../Attachments/TB0001-1203/Screenshot%202569-11-12%20at%2009.14.27.png) (285193 bytes, Nate Trakarntanasuk, 2026-11-12T09:20:09.871+0700)
- [Screenshot 2569-11-12 at 09.21.15.png](../../Attachments/TB0001-1203/Screenshot%202569-11-12%20at%2009.21.15.png) (259916 bytes, Nate Trakarntanasuk, 2026-11-12T09:24:43.478+0700)
- [V0042__rwb_e1_042_parameter_catalog_and_seed.sql](../../Attachments/TB0001-1203/V0042__rwb_e1_042_parameter_catalog_and_seed.sql) (24495 bytes, CHANISSARA MAHAKITTIKUN, 2026-11-10T19:02:28.615+0700)
- [V042_1__parameter_catalog.sql](../../Attachments/TB0001-1203/V042_1__parameter_catalog.sql) (15382 bytes, CHANISSARA MAHAKITTIKUN, 2026-11-10T19:02:28.710+0700)
- [V042_2__parameter_seed.sql](../../Attachments/TB0001-1203/V042_2__parameter_seed.sql) (9730 bytes, CHANISSARA MAHAKITTIKUN, 2026-11-10T19:02:28.466+0700)

## Comments (11)

### Comment 1: Nuttapon Jittachotisak, 2026-11-09T16:46:11.632+0700

Comment ID 1781561

Question

|4.Flow 
#4|!image-20261109-093924.png|width=236,alt="image-20261109-093924.png"!
Please provide V042_1__parameter_catalog.sql, V042_2__parameter_seed.sql for migration|
|12. Contract
POST /api/recovery/v1/admin/reference-loads|As I understand this endpoint was use in many table update. How to decide which table to update? Is it choose by user? if yes, User would choose by table or by type. 
If by table: Would column be a table column name?
If by type: Need csv format for each type(please provide). such as each column should map to which {dbTable}.{dbColumn}|
|Test case TC-E1-042-12|!image-20261109-093824.png|width=236,alt="image-20261109-093824.png"!
TC-E1-042-12 could not be done and role function would not be worked becuase role would be implemented later on  E1-022/E1-037 
remark: should be ignore about role for now and create an open item and link to E1-022/E1-037 to track|
|4.Flow 
#2 build|!image-20261109-093948.png|width=236,alt="image-20261109-093948.png"!
This subject look like generate class from csv file at build time but as from my understand csv file for update parameter would be upload by user at runtime right?|
|Message|Everything refer to message would be mock or set with fixed text now. Because message table was not implement yet [E1-043 (#9)]|

### Comment 2: CHANISSARA MAHAKITTIKUN, 2026-11-10T12:31:22.311+0700

Comment ID 1782842

# *Flow #4: Please provide V042_1__parameter_catalog.sql and V042_2__parameter_seed.sql*

*Answer:*

The requested files, V042_1__parameter_catalog.sql and V042_2__parameter_seed.sql, will be provided separately at a later stage once they are finalized.

 

# *Contract: POST /api/recovery/v1/admin/reference-loads*

 

Decision:

 

The endpoint must not allow the user to select an arbitrary physical database table or database column.

 

The request identifies a supported reference table_code, and one load covers one reference-data table/type.

 

The selected table_code determines the expected schema for the uploaded CSV/XLSX, including:

 

column names;

data types;

key column(s);

validation rules.

 

The uploaded file columns therefore follow the schema defined for the selected table_code; they should not be interpreted as arbitrary physical {dbTable}.{dbColumn} names.

 

Action: The specification must provide or reference the authoritative supported table_code list and the corresponding CSV/XLSX schema for each supported code. Where physical database mapping is required, Development should use the approved data model/reference-data schema rather than infer the mapping.

 

 

# *Test Case TC-E1-042-12*

 

Decision:

 

Defer the access-control assertion in TC-E1-042-12 until the required role and permission capabilities from RWB-E1-022 and RWB-E1-037 are available.

 

The parameter functionality within RWB-E1-042 remains in scope.

 

Create an open dependency item linked to RWB-E1-022 / RWB-E1-037. Once those role and permission capabilities are available, complete TC-E1-042-12 and verify that a caller without the required permission is refused with MSG-P4-002.

 

Status: Access-control assertion deferred due to dependency; TC-E1-042-12 remains part of the acceptance scope.

 

 

# *Flow #2 Build: Parameter Catalog CSV*

 

Decision:

 

config/parameter-catalog.csv is a build-time source file for RWB-E1-042.

 

The flow is:

 

config/parameter-catalog.csv

 → ParameterKeysGenerator

 → generated ParameterKeys class

 → parameter access through ParameterService

 

This process runs as part of the build and does not represent a business-user runtime upload.

 

Runtime file uploads through POST /api/recovery/v1/admin/reference-loads belong to the reference-data load process and are separate from the build-time parameter catalog used by ParameterKeysGenerator.



# *Message handling*

Decision:

 

Continue to use the message codes defined by the story, including MSG-P4-002.

 

Where the final message-resolution capability is not yet available, record the dependency/open item against the story that delivers that capability.

 

Temporary test stubs/placeholders may be used for testing where required, but the final production implementation must resolve the defined message code through the agreed message capability.

 

 



 

### Comment 3: Nuttapon Jittachotisak, 2026-11-10T18:13:00.333+0700

Comment ID 1784330

# *Flow #4: Please provide V042_1__parameter_catalog.sql and V042_2__parameter_seed.sql*

Should this story wait until V042_1__parameter_catalog.sql and V042_2__parameter_seed.sql are finalised, or should we exclude *Flow #4* from the story?

# *Contract: POST /api/recovery/v1/admin/reference-loads*

Do you have an example CSV to upload? Would it look like this:

[^parameter.csv]



### Comment 4: CHANISSARA MAHAKITTIKUN, 2026-11-10T19:02:28.925+0700

Comment ID 1784376

@Nuttapon Jittachotisak 

*Migration SQL — three files*

# {{V042_1__parameter_catalog.sql}} — Creates {{parameter_catalog}} and {{parameter_value}}, guarded so it is also safe on top of the E1-001 baseline that already creates both tables. It adds the unique parameter key, scope/kind/type checks, environment and status checks, maker-checker, the catalog foreign key, and two important uniqueness rules: one version per key/environment/product group (NULL-safe) and one approved value per valid-from date. It also adds the story’s lookup indexes. Min/max range validation stays in {{ParameterLoadChecks}}, because the range columns are text and the check depends on {{value_type}}.
# {{V042_2__parameter_seed.sql}} — Generated from {{config/parameter-catalog.csv}}. It loads *13 catalog rows and 28 value rows* (7 value-bearing keys × 4 environments). It is idempotent, uses the system seed UUID as author, and ends with a deployment guard that fails if a required global parameter has no approved value for an environment. PRODUCT-scope rows carry no values by design; their values are {{PRODUCT_PARAMETER}} rows. The full Epic 1 catalog is not in the pack, so this is a bootstrap seed; the remaining candidates are listed in the clarification pack.
# {{V0042__rwb_e1_042_parameter_catalog_and_seed.sql}} — The same DDL and seed as one migration. D-RCV-28 requires one file per story named {{V<seq>__<story>_<name>.sql}}, so the requested {{V042_1}}/{{V042_2}} split is a review copy only. *Commit this consolidated file* unless a migration-lint exception is approved for the split.

All three use {{${recoverySchema}}}, not a literal schema name.

----

h2. 1. Contract 12 — how {{POST /admin/reference-loads}} decides what to update

The caller chooses *one table code*, not a database table, not a column, and not a type.

* One call carries one file for one code.
* The code must be in {{LOV-REF-TABLE}} *and* have a registered handler.
* The handler owns the target table and the column mapping; the caller never supplies {{{dbTable}.{dbColumn}}}.
* {{kind}} and {{value_type}} do not choose a table. {{value_type}} is used to parse and range-check the value.
* Adding a new code requires a LOV row, a handler, a schema entry and usually a target-table migration plus a release. Adding a value row requires only a load and approval.

That is why the endpoint appears to update many tables: it is a versioned load service with one handler per code. The first 20 LOV codes are reference-data codes; the last five ({{ENTRY}}, {{EXCLUSION}}, {{ALLOCATION}}, {{ASSIGNMENT}}, {{TRANSFER}}) are rule-table codes loaded through the rule-version endpoint instead.

{{PARAMETER}} *CSV:*

{noformat}key,environment,value{noformat}

{noformat}case.entry.dpd,PROD,91{noformat}

{noformat}refdata.cache.ttl-seconds,PROD,300{noformat}

|*CSV column*|*Target*|*Check*|
|{{key}}|{{parameter_value.param_key}}|Must exist in the catalog; unknown key refuses the whole load with MSG-P1-002|
|{{environment}}|{{parameter_value.environment}}|DEV/SIT/UAT/PROD and allowed by the catalog line|
|{{value}}|{{parameter_value.param_value}}|Parsed as the catalog type; must be inside min/max; wrong type = MSG-P1-002, out of range = MSG-GEN-002|
|—|{{product_group}}|NULL for {{PARAMETER}}; product values are {{PRODUCT_PARAMETER}}|
|—|{{version_no}}|Next number for key + environment; the seed is version 1|
|—|{{valid_from}}|The request {{validFrom}}; not before the business date, equal allowed|
|—|{{status}}|VALIDATED on load, APPROVED on approval|
|—|{{author_user_id}} / {{approver_user_id}}|Author = signed-in loader; approver set only by approve; approver must differ|

For other codes, there is no single CSV schema. {{PERMISSION}}, {{MASKING_RULE}}, {{DOCUMENT_TYPE}}, {{TEMPLATE}}, {{RETENTION_CLASS}}, {{PRODUCT}} and several others have published column sets. {{PRODUCT_PARAMETER}}, {{SERVICE_LEVEL}}, {{QUEUE}}, {{QUEUE_MEMBER}}, {{DELEGATION_LIMIT}} and {{DOCUMENT_CHECKLIST}} do *not* have an approved template yet; their owning stories must publish the header before a loader is built. Proposed headers are in §3.4 of the clarification pack and are clearly marked not approved.

----

h2. 2. Flow #2 — build-time CSV vs runtime CSV

They are two different files:

| |*Catalog file*|*Value file*|
|Path|{{config/parameter-catalog.csv}} in the repository|Uploaded to {{POST /admin/reference-loads}}|
|When|Build time and deployment|Runtime|
|Changed by|Reviewed pull request, owner approves|RW-COE through a checked load|
|What it changes|The *definition* of a key: type, range, default, owner, scope, required, environments, used by|The *value* of an existing key|
|Produces|{{ParameterKeys}} class and the {{V042_2}} seed|{{parameter_value}} version rows|
|Can add a key?|*Yes*|*No*; unknown key refuses the load|
|Needs a release?|Yes|No|

Build step 2 reads the repository catalog and generates typed constants such as {{ParameterKeys.CASE_ENTRY_DPD}} of type {{ParameterKey<Integer>}}. The runtime upload has only {{key,environment,value}}; it has no type, owner or range, so it cannot generate a class.

A new parameter is a reviewed PR and a release. A new value is a load and an approval, with no release.

----

h2. 3. TC-E1-042-12 — role test

*Correct status: Blocked, not Failed and not Pass.*

* RWB-E1-042 is Window 1. The 403 path is delivered by *RWB-E1-022* (SSO/MFA, session roles, {{AccessCheck}}, endpoint interceptor), and the permission matrix is loaded by *RWB-E1-037*. Both are Window 2.
* The Physical Schema v4 seed is also not sufficient for the test: 421 of 756 permission rows, no {{-}} rows, {{matrix_version='1'}}, and {{role.entra_group}} null for every role.
* Do not add a mock role or temporary permit. That would weaken the access test. Stub the identity provider if needed, but resolve roles from the real {{role}}/{{permission}} tables and use the real {{AccessCheck}}.
* The endpoint stays on *Rules and parameters R*, not Reference data R. RW-PHONECOL holds Reference data R but not Rules and parameters, which is exactly what the test proves.

----

h2. 4. Messages

The message table does not exist in Physical Schema v4 and no story currently owns it. “E1-043 #9” is an ambiguous reference: E1-043’s own item 9 is {{TEMPLATE}}, and its 13 table codes exclude {{MESSAGE}}. The ninth row of the *reference-data register* is “Messages — screen and letter messages in English and Thai”. The intent of the review note is right: use fixed text for now.

Use one {{MessageResolver}} seam, keyed by message ID:

* Controllers and services pass the ID and placeholders; they never hold the sentence.
* Fixed text is exactly the story §14 text, in {{config/messages-e1-042.csv}}.
* Tests assert the *message ID and placeholders*, not the English sentence.
* Switch to the table later with {{rwb.messages.source=fixed|table}}; the IDs do not change.
* Proposed Thai exists for all messages; only DL10 approval is missing. Include {{messageTh}} in the API {{Problem}} response.
* {{MSG-P4-001}} is used by the 401 response but missing from E1-042 §14; add it to the fixed catalog.

[^V0042__rwb_e1_042_parameter_catalog_and_seed.sql] [^V042_1__parameter_catalog.sql] [^V042_2__parameter_seed.sql] 

### Comment 5: CHANISSARA MAHAKITTIKUN, 2026-11-10T19:21:25.994+0700

Comment ID 1784383

@Nuttapon Jittachotisak 

Yes, the {{PARAMETER}} CSV is {{key,environment,value}}. Your example has the right shape, but four things must change before it will load.

h3. Why the sample would fail

|*Issue*|*Your file*|*Required*|
|Header spacing|{{key, environment, value}}|{{key,environment,value}} — no spaces after commas|
|Environment values|{{production}}, {{development}}|{{PROD}}, {{DEV}}, {{SIT}}, {{UAT}} — the LOV-ENVIRONMENT codes|
|Keys|{{api_url}}, {{db_connection}}|Must already exist in {{parameter_catalog}}. A {{PARAMETER}} load *cannot add a key*; an unknown key refuses the whole file with MSG-P1-002|
|Secret in the file|{{db_connection}} contains {{Password=mypassword}}|Never put a password or connection string in a reference-load file. Secrets stay in the ACE secret store; the catalog lists them with {{secret = true}} and no value|

h3. A valid {{PARAMETER}} file

{noformat}key,environment,value{noformat}

{noformat}case.entry.dpd,PROD,91{noformat}

{noformat}case.entry.dpd,SIT,30{noformat}

{noformat}refdata.cache.ttl-seconds,PROD,300{noformat}

{noformat}caselist.export.maxrows,PROD,10000{noformat}

### Comment 6: Nuttapon Jittachotisak, 2026-11-11T18:38:13.425+0700

Comment ID 1786550

@CHANISSARA MAHAKITTIKUN 

Please confirm scope of this story

This story expect to: 

* create table {{parameter_catalog}}, {{parameter_value}}
* create endpoint {{GET /admin/parameters}} 
* generates the {{ParameterKeys}} class ({color:#ff5630}Please answer: this would generate from catalog file[config/parameter-catalog.csv] or from catalog data in db[parameter_catalog]?{color})

What not include: 

* create endpoint {{POST /api/recovery/v1/admin/reference-loads}}, {{POST /api/recovery/v1/admin/reference-loads/{loadId}/approve}}, {{POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback}} because these api should be create on *RWB-E1-043*

Curious:

* Who handle {{POST /api/recovery/v1/admin/reference-loads}} upload with type “PARAMETER” E1-042 or E1-043

### Comment 7: Nate Trakarntanasuk, 2026-11-12T09:20:10.042+0700, edited 2026-11-12T10:47:07.798+0700

Comment ID 1786755

@CHANISSARA MAHAKITTIKUN 

Pls Confirm for this API 

Can you provide Sequence Diagram / Flow Chart of all the API 

*POST /api/recovery/v1/admin/reference-loads*

* table = “PARAMETER“ → It will send in body? 
* Can you provide full spec body for this API?
* Do you have example of response format for this API? ex. success case and fail case
* Error 503 Do it have a message?
* Error 401 Do it have a message?
* type or unknown key ({{MSG-P1-002}}), empty file ({{MSG-GEN-001}}) Not have error code? Can this error return in this API?

!Screenshot 2569-11-12 at 09.14.27.png|width=724,alt="Screenshot 2569-11-12 at 09.14.27.png"!

*GET /admin/parameters*

* For request Query key (prefix) can you provide what kind of prefix that we use?
* Can you provide full spec body for this API?
* Do you have example of response format for this API? ex. success case and fail case
* Error 503 Do it have a message?
* environment in request is DEV, SIT, UAT?

!Screenshot 2569-11-12 at 09.21.15.png|width=696,alt="Screenshot 2569-11-12 at 09.21.15.png"!

### Comment 8: CHANISSARA MAHAKITTIKUN, 2026-11-13T16:58:09.359+0700

Comment ID 1790603

@Nate Trakarntanasuk We have answer it via email and Team.

### Comment 9: CHANISSARA MAHAKITTIKUN, 2026-11-13T16:58:19.439+0700

Comment ID 1790605

@Nuttapon Jittachotisak We have answer it via email and Team.

### Comment 10: Pe Chichareon, 2026-11-15T10:15:17.477+0700

Comment ID 1791303

Due to Microsoft’s tool outage, Henka responded in email

[^RWB-E1-042  Central configuration service and parameter catalog.txt]



### Comment 11: NAMTIP WONGSOMBOON, 2026-11-17T09:42:36.422+0700, edited 2026-11-17T09:42:56.878+0700

Comment ID 1793801

Depends on [https://scbjira.atlassian.net/browse/TB0001-1205|https://scbjira.atlassian.net/browse/TB0001-1205|smart-link] 


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
