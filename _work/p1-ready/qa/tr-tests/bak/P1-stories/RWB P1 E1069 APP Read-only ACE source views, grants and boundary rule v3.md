# RWB-P1-E1069-APP Read-only ACE source views, grants and boundary rule

**Version 3 changes**

- The three Architecture v5 reads GET /customers/{id}, /accounts/{id} and /collateral/{id} are this story's; the data-product records operation is RWB-P1-E1016-APP's (RD-P1-005, RD-P1-021; findings 1 to 4 and 14).
- Views, helper functions, conformance, boundary rule and dictionary types aligned to Physical Schema v9 and LDM v11; extension tables and grants stay with RWB-P1-E1069-DB (findings 5, 6, 17 to 20, 24 and 25).
- Section B build and gate behaviour and no writer for the appraisal fields (RD-P1-041, RD-P1-043; findings 7, 8, 13 and 16).
- Messages, authorisation, audit, timing, traceability and AC14 to AC20 corrected or added (findings 9 to 12, 15, 21 to 23 and 26).
- Batch D: the three reads are published in rwb-source-data.yaml 5.1.0 as getCustomer, getAccount and getCollateral with masking by policy (RD-P1-060); a read writes the PII access log only and publishes no decision record (RD-P1-072); AC5 states the dictionary baseline of at least 123 objects and 1,379 fields (RD-P1-025); test case IDs of Test Cases v9 cited.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1069-APP |
| Version | 3 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-069 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1069-APP-16) |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP baseline, RWB-PLT-NF06-DB and RWB-PLT-E1044-CON; Section A views before the Section A grants of RWB-P1-E1069-DB; Section B after its gate outside DEV and pipeline test |
| Depends on (build) | RWB-P1-E1001-APP, RWB-PLT-NF06-DB, RWB-PLT-E1044-CON, RWB-PLT-E1027-CON, RWB-P4-E1037-CON |
| Contract dependencies | rwb-source-data.yaml 5.1.0 (API Specification v7) for the three reads and the Problem body; RWB-P4-E1037-CON (authorise schema Pending; FieldMasker) |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1069-DB (grants and extension tables; AC3 closes with it); RWB-P1-ACE001-DB for the Section B gate; DL43 (ACE team lead; recommended answer A is the planning basis) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-002, FR-P1-005) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); the three reads of section 12.1 are part of it (RD-P1-060) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-008, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-041, RD-P1-043, RD-P1-025, RD-P1-060, RD-P1-072 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for rwb-source-data. The 30 `recovery.v_ace_*` views stay in schema `recovery` with `ace_view_owner` as their owner and are read by the `rwb_source_data` login only (DP-02, DP-05; Architecture v5 slides 11 and 29); the view SQL, the conformance test and the ACE read contract move to this story, the login, the grant block and the four extension tables to RWB-P1-E1069-DB, and the proof across the 19 logins to RWB-ITG-E1069-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1069-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 36 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: Section A and B view behaviour, three ACE reads, authorisation, audit, boundary checks and acceptance criteria. Agent: S7-stories.

### 1. Story

As a recovery developer (RW-TRIBE), I want the 16 Section A and 14 Section B ACE views on the rwb-source-data migration sequence, their dictionary and boundary checks, and the three reads GET /customers/{personKey}, GET /accounts/{accountKey} and GET /collateral/{assetKey} of Architecture v5 slide 15, so that only rwb-source-data reads ACE views and every consumer reaches ACE data through its contract.

This story creates the views, the three helper functions and the three reads. It does not create extension tables, logins or grants; RWB-P1-E1069-DB owns them. It does not build GET /data-products/{productCode}/records, which RWB-P1-E1016-APP builds on these views (RD-P1-021), or freshness, which is RWB-P1-E1015-APP's. The account-page read used by rwb-case is published in RWB-P1-E1015-CON and built by RWB-P1-E1002-APP (RD-P1-024). The service login is rwb_source_data. Section B is built against the synthetic Tier 2 fixture in DEV and pipeline test and remains gated in other environments (RD-P1-043).

### 2. Business rationale

The 30 recovery.v_ace_* views remain the only ACE source read path for rwb-source-data. The service login rwb_source_data reads the views; ace_view_owner owns them and reads the ACE source tables. Other services use rwb-source-data's published API contract and do not read the views directly (D-RCV-60).

The only REST contract file of the service is rwb-source-data.yaml (API Specification v7). Version 5.1.0 publishes the three reads of Architecture v5 slide 15 as getCustomer, getAccount and getCollateral, and this story builds them (RD-P1-060; RD-P1-005 rule 1); no story-local OpenAPI file is created. They give RWB-P1-DM001-APP, RWB-P1-DM002-APP and the consumers in other services the ACE facts of one key.

### 3. Preconditions

- RWB-P1-E1001-APP has applied the rwb_source_data baseline and dictionary rows.
- RWB-P1-E1069-DB has created the four extension tables. This story does not create or write them.
- Section A uses 16 views over the current ACE schema. Section B uses 14 views over the synthetic tier2-ddl.sql fixture in DEV and pipeline test.
- In SIT, UAT and PROD, Section B is not applied until RWB-ACE-001 lands in that environment; relevant flags stay off. With the flag off, freshness is STALE with businessDate null and MSG-P1-001 (RD-P1-043).
- There is no RWB-P1-E1069-CON story and no story-local OpenAPI. The keys are personKey (ACE person_key), accountKey and assetKey; response fields are the view columns in camelCase (RD-P1-060; GAP-0549 and GAP-0566 closed for the response schemas).
- Pending: the story that appends the 12 RWB-ACE-001 columns to v_ace_account, v_ace_customer and v_ace_efs_action, owner data architect with the ACE team lead (NEW-GAP-W4-3).
- Pending: the masking rule rows that unmask firstName, lastName and the ADDRESS contact values for the rwb-comms notice and rwb-integration outbound-file workload identities, owner data protection officer with the rwb-access owner (NEW-GAP-D1).
- DL43 is open with the ACE team lead; recommended answer A (scope and dates as in RWB-ACE-001) is the planning basis (RD-P1-043).
- The statements that create views in schema recovery run under the privileged principal Pending in NEW-GAP-S7-05; the service migrator has no right there.
- RWB-P4-E1037-CON names POST /api/recovery/access/v1/authorise and FieldMasker.mask(dto, session). The capability of the three reads is Case record R (RD-P1-060); the authorise request and response schemas and the case-reference rule remain Pending under GAP-0925, GAP-0990 and GAP-1404.
- Exact mask forms and personal fields remain Pending under GAP-0901, GAP-0903 and GAP-1404. A value already masked by a view is never unmasked.
- Inner authorization/database budgets, retry policy and circuit-breaker thresholds remain Pending under GAP-0567.
- This story writes no freshness data and is not the writer of valuation_ext.stale_flag or age_days; that writer is not ruled and stays with GAP-1509 (RD-P1-041).

### 4. Flow

1. Add the 16 Section A view definitions and three helper functions from recovery_views.sql to the service sequence using a new versioned migration.
2. Add the 14 Section B view definitions in a later sequence version and apply them in DEV and pipeline test over tier2-ddl.sql.
3. Run view conformance: view compilation, dictionary rows, constraints in rwb_source_data, and the privilege assertions delivered by E1069-DB.
4. Run BND-6 over this service's package. Check Java dependencies and SQL strings in JDBC, JPA native queries and query annotations for public relation references; fail with the class and relation.
5. Implement the three reads, each by one key (RD-P1-060): the account read answers the v_ace_account Section A columns, relations[] from v_ace_ca_relation, accountFacts from account_ext (null when no row) and the DP01 freshness; the customer read answers the v_ace_customer Section A columns, partyFacts from party_ext (null when no row), contacts[] from v_ace_contact with consentStatus and verifiedAt of contact_point_ext, and the DP02 freshness; the collateral read answers the v_ace_collateral rows of the asset key, the v_ace_collateral_detail columns only when Section B is live, and the DP06 freshness. No read refuses on freshness; the caller applies its own stale rule.
6. Call the rwb-access authorise operation once for the requested fields before any value is returned, then pass every field tagged is_personal through FieldMasker.mask(dto, session); a field with no rule is masked. contactValue, firstName, lastName and the address columns are clear only when the rule unmasks them for the caller.
7. Write the PII access log entry, then answer; a read publishes no DecisionRecorded (RD-P1-072). Errors are RFC 9457 Problem bodies: 400 MSG-GEN-001, 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003 for a key with no row or outside scope, and 503 MSG-GEN-006 for a timeout, an unavailable view or a failed access-log write.
8. With Section B off, run no Section B view query: the collateral read omits the detail part, and freshness (RWB-P1-E1015-APP) answers STALE with null businessDate and MSG-P1-001 (RD-P1-043).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A Section A view fails to compile | Its migration fails and names the view and missing source column | Pipeline result | AC1 |
| X2 | Section B table or deployment gate is absent | Section B is withheld outside DEV; its feature flags remain off | Pipeline result | AC2 |
| X3 | A P1 constraint references an object outside rwb_source_data | Boundary check fails naming the constraint and target object | Pipeline result | AC4 |
| X4 | A view or column has no dictionary row | Conformance fails naming the view or field | Pipeline result | AC5 |
| X5 | A service login has a grant on public or an unauthorized view grant exists | Conformance fails naming grantee and object | Pipeline result | AC2 |
| X6 | A class uses public through a JDBC, JPA native query or query annotation | BND-6 fails naming class and relation | Boundary rule BND-6 | AC6 |
| X7 | Authorise refuses the read or omits a requested field | A refusal returns no field; an omitted or masked field is returned masked or not at all; the mask form is Pending | 403 MSG-P4-002 | AC8, AC9 |
| X8 | Authorise or the view read exceeds its budget, or the database is unavailable | Return 503 Problem with no partial fields | MSG-GEN-006 | AC10 |
| X9 | RWB-ACE-001 is not deployed outside DEV | No Section B migration; flags stay off; freshness is STALE, null businessDate | MSG-P1-001 | AC2, AC12, AC15 |
| X10 | No view row for the key, or the key is outside the caller's scope | 404 Problem and nothing written to a business table | MSG-P4-003 | AC16 |
| X11 | No valid caller identity | 401 Problem and no view is read | MSG-P4-001 | AC17 |
| X12 | The PII access log write fails | 503 Problem; no business field is returned | MSG-GEN-006 | AC11 |
| X13 | ACE text that is not a date or a flag | The helper function returns NULL and the read does not fail | None | AC18 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Section A follows the P1 baseline; Section B uses a fixture in DEV and waits on the environment gate elsewhere |
| Negotiable | View names and fields follow recovery_views.sql and the published API v7 schema |
| Valuable | One ACE read path serves consumers without giving them database access |
| Estimable | The authorise schema, mask forms, masking rule rows, timing budgets and the view-to-consumer map remain Pending |
| Small | Size is Not specified and remains for squad refinement |
| Testable | Each criterion has a build, contract or authorisation test; AC1 to AC20 have rows in Test Cases v9 |

### 7. Acceptance criteria

~~~gherkin
Feature: Read-only ACE source views and the three ACE reads

Scenario: AC1 Section A views compile and match the source definitions
  Given the ACE schema, the P1 baseline and Section A migration
  When the Section A migration runs
  Then the three helper functions and 16 Section A views exist in recovery
  And each view compiles and a one-row select completes
  And no table is created in recovery
  And the migration is versioned after the baseline without a reused legacy version
  # TC-E1-069-01

Scenario: AC2 Section B views use the fixture and the DL43 gate
  Given tier2-ddl.sql is applied in DEV and pipeline test
  When Section B migration runs there
  Then the 14 Section B views compile
  And Section A conformance runs in every environment
  And Section B conformance runs after that migration is applied
  And in SIT, UAT and PROD the migration waits for RWB-ACE-001 and feature flags stay off
  And freshness while the flag is off is STALE with null businessDate and MSG-P1-001
  # TC-E1-069-02

Scenario: AC3 The login reads views and not ACE tables
  Given RWB-P1-E1069-DB grants Section A views to rwb_source_data
  When a session as rwb_source_data selects an applied view and public.account
  Then the view select completes
  And public.account is refused with SQLSTATE 42501
  And has_table_privilege is false for SELECT on every public table
  And has_table_privilege is false for INSERT, UPDATE, DELETE and TRUNCATE on each applied view
  And direct writes on join views fail with SQLSTATE 55000 or 42501
  # TC-E1-069-03

Scenario: AC4 P1 constraints do not cross schemas
  Given rwb_source_data is at head and recovery contains views only
  When the conformance test lists constraints in rwb_source_data
  Then none references an object outside rwb_source_data
  And a fixture foreign key from account_ext.account_key to public.account fails naming the constraint and public.account
  # TC-E1-069-04

Scenario: AC5 View dictionary rows match the views
  Given the E1001 dictionary and both view sections are applied
  When the conformance test compares each view with its dictionary rows
  Then 30 view objects have 304 fields, DF-ACE-001 to DF-ACE-304, 177 in Section A and 127 in Section B
  And each view column has one matching sys_fields row with the same name and the physical type of LDM v11
  And a column without a dictionary row, or with a different type, fails naming the view and column
  And the dictionary holds at least 123 objects and 1,379 fields, the RD-P1-025 baseline
  # TC-E1-069-05

Scenario: AC6 Boundary rule BND-6 rejects direct ACE table references
  Given a class in th.co.scb.ace.workbench.recovery.sourcedata includes SQL naming public.account
  When the source boundary scan checks JDBC, JPA native queries and query annotations
  Then the build fails with BND-6 naming the class and public.account
  And a query naming recovery.v_ace_account passes
  # TC-E1-069-06

Scenario: AC7 The account read answers from the ACE views
  Given the authorise fake grants every field and account "ACC0000017" is in v_ace_account with days_past_due 95
  When GET /api/recovery/source-data/v1/accounts/ACC0000017 is called
  Then 200 returns the values of v_ace_account for that key in camelCase, including daysPastDue 95, with relations from v_ace_ca_relation and the DP01 freshness
  And accountFacts is null when account_ext holds no row for the key
  And no recovery view outside v_ace_account and v_ace_ca_relation is queried
  And a PII access log entry is written and no DecisionRecorded is published
  # TC-E1-069-07

Scenario: AC8 Authorisation limits the fields and masked values stay masked
  Given the authorise fake grants the customer read for personKey "P0000123" to a user role with no unmasking rule
  When GET /api/recovery/source-data/v1/customers/P0000123 is called
  Then 200 returns only the granted fields, and contactValue carries the contact_value_masked value
  And the identity number appears only as idNoMasked and idNoLast4
  And no clear contactValue, firstName or lastName appears in the body or in a log line
  And for the rwb-comms notice and rwb-integration outbound-file identities the FieldMasker fake rules answer firstName, lastName and contactValue clear
  And the masking rule rows remain Pending under NEW-GAP-D1 and the mask forms under GAP-0901, GAP-0903 and GAP-1404
  # TC-E1-069-08

Scenario: AC9 An authorisation refusal returns a problem response
  Given the authorise fake refuses the caller
  When any of the three reads is called
  Then the response is 403 Problem with MSG-P4-002 and no business field
  And the refusal publishes no DecisionRecorded
  # TC-E1-069-09

Scenario: AC10 Authorisation or view timeout fails closed
  Given the authorise fake or the database does not answer within its inner budget, which fits inside the caller's 2 s
  When a read is called
  Then the response is 503 Problem with MSG-GEN-006
  And no partial field, cached answer or clear value is returned
  And inner budgets, retries and breaker thresholds remain Pending under GAP-0567
  # TC-E1-069-10

Scenario: AC11 Access log write failure returns no data
  Given the PII access log write fails
  When a read of a personal field runs
  Then the response is 503 Problem with MSG-GEN-006 and no business field is returned
  # TC-E1-069-11

Scenario: AC12 Section B freshness is stale while its flag is off
  Given RWB-ACE-001 is absent from an environment and the Section B flag is off
  When freshness for an affected product is read
  Then status is STALE, businessDate is null and the response carries MSG-P1-001
  And no Section B view is queried
  # TC-P1-E1069-APP-01

Scenario: AC13 Applied migration edits are refused
  Given a Section A or Section B migration is already applied
  When Flyway validate checks an edited applied file
  Then validation fails with a checksum mismatch naming the version
  And no statement runs
  # TC-P1-E1069-APP-02

Scenario: AC14 The customer read composes the person and contacts
  Given "P0000123" has three contacts and no party_ext row
  When GET /customers/P0000123 is called by a caller granted all fields
  Then 200 lists three contacts, partyFacts is null and the DP02 freshness is carried
  And the only identity values are idNoMasked and idNoLast4
  # TC-P1-E1069-APP-03

Scenario: AC15 Collateral read before Section B
  Given the Section B migration is not applied
  When GET /collateral/{assetKey} is called for a key present in v_ace_collateral
  Then 200 returns the v_ace_collateral rows of the asset key, the DP06 freshness and no collateral detail part
  And v_ace_collateral_detail is not queried
  # TC-P1-E1069-APP-04

Scenario: AC16 Unknown key
  Given no view row for the key, or a key outside the caller's scope
  When any of the three reads is called
  Then the response is 404 Problem with MSG-P4-003 and no business row is written
  # TC-P1-E1069-APP-05

Scenario: AC17 No caller identity
  Given no valid caller identity
  When any of the three reads is called
  Then the response is 401 Problem with MSG-P4-001, authorise is not called and no view is queried
  # TC-P1-E1069-APP-06

Scenario Outline: AC18 Conversion functions return a value or NULL
  Given the input <input>
  When <function> runs
  Then it returns <result> without error

  Examples:
    | function | input | result |
    | ace_to_date | 2026-11-27 | 2026-11-27 |
    | ace_to_date | 20261127 | 2026-11-27 |
    | ace_to_date | 27/11/2026 | 2026-11-27 |
    | ace_to_date | abc, an empty string or null | NULL |
    | ace_to_boolean | Y, yes, true or 1 | true |
    | ace_to_boolean | N, no, false or 0 | false |
    | ace_to_boolean | X, an empty string or null | NULL |
    | ace_mask_value | 0812345678 | ******5678 |
    | ace_mask_value | ab@example.com | a***@example.com |
    | ace_mask_value | an empty string or null | NULL |
  # TC-P1-E1069-APP-07

Scenario: AC19 Response time
  Given the busiest-hour load of the read paths
  When the three reads run
  Then the 95th percentile answer time is under 2 seconds (NFR-P1-001)
  # TC-P1-E1069-APP-08

Scenario: AC20 Only this service reads the views
  Given a class of another service module or a login other than rwb_source_data
  When it names or selects a recovery.v_ace_ view
  Then the build rule or the database refuses it, as RWB-ITG-E1069-ITG and RWB-P1-E1069-DB prove
  And every other service reads ACE data only through the rwb-source-data contract
  # TC-P1-E1069-APP-09
~~~

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | rwb-source-data reads ACE only through the 30 recovery.v_ace_* views | D-RCV-35; ADR-010 |
| BR2 | ace_view_owner is NOLOGIN and owns views; service logins are not members of it | D-RCV-60; RWB-P1-E1069-DB |
| BR3 | rwb_source_data is the only service login with SELECT on the views, with rwb_sandbox_read as the DEV-only exception; no service login has table privilege on public | D-RCV-60; Security and Access Design v6 |
| BR4 | No constraint in rwb_source_data references another schema; recovery is views-only | D-RCV-35; DP-01 |
| BR5 | Every view column has one matching dictionary row from E1001 with the same physical type | LDM v11; RD-P1-025 |
| BR6 | ace_to_date and ace_to_boolean return NULL for values they cannot convert; ace_mask_value keeps the last four characters, or the first character and the domain of an email address | Physical Schema v9 recovery_views.sql |
| BR7 | Extension tables are owned and created by E1069-DB; this story neither writes them nor owns stale_flag/age_days | RD-P1-021; GAP-1509 |
| BR8 | BND-6 rejects direct public table references in this service; ITG checks other services | REQ-DRI-006; RWB-TE-001 |
| BR9 | Section B builds against the fixture and deploys after RWB-ACE-001; flags remain off before the gate | RD-P1-043 |
| BR10 | A personal field is returned only after authorise, FieldMasker and the PII access log write succeed; a view-masked value is never unmasked; a read is logged, never recorded as a decision | RD-P1-060; RD-P1-072; DP-08 |
| BR11 | This story writes no freshness data and no extension table | RD-P1-041; RD-P1-022 |

### 9. State transitions

This story changes no business state. Section A moves from Pending to Applied after the baseline. Section B moves from Pending to Applied only after its environment gate passes. An applied migration is never edited; a correction uses a new version.

### 10. Authority

| Role | Authority |
|---|---|
| Recovery squad (RW-TRIBE) | Owns view SQL, conformance test, BND-6 and the three reads of section 12.1 |
| Platform sequence owner | Assigns migration versions |
| ACE team lead | Owns DL43 decision; recommended answer A is a planning basis only |
| P4 contract owner | Owns authorise request and response schema, right and case-reference rule |
| Data protection officer with the rwb-access owner | Own the masking rule rows for the notice and outbound-file identities (NEW-GAP-D1) |
| Product owner | Owns epic design sign-off; sign-off remains Pending |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-042 | v_ace_account | all 42 fields | Read |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | all 12 fields | Read |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | all 20 fields | Read |
| DF-ACE-075 to DF-ACE-083 | v_ace_contact | all 9 fields | Read |
| DF-ACE-084 to DF-ACE-088 | v_ace_ca_relation | all 5 fields | Read |
| DF-ACE-089 to DF-ACE-090 | v_ace_aa_relation | all 2 fields | Read |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | all 8 fields | Read |
| DF-ACE-099 to DF-ACE-107 | v_ace_asset | all 9 fields | Read |
| DF-ACE-108 to DF-ACE-127 | v_ace_efs_action | all 20 fields | Read |
| DF-ACE-128 to DF-ACE-130 | v_ace_efs_action_code | all 3 fields | Read |
| DF-ACE-131 to DF-ACE-139 | v_ace_efs_assignment | all 9 fields | Read |
| DF-ACE-140 to DF-ACE-145 | v_ace_bucket_log | all 6 fields | Read |
| DF-ACE-146 to DF-ACE-150 | v_ace_product | all 5 fields | Read |
| DF-ACE-151 to DF-ACE-154 | v_ace_branch | all 4 fields | Read |
| DF-ACE-155 to DF-ACE-159 | v_ace_holiday | all 5 fields | Read |
| DF-ACE-160 to DF-ACE-177 | v_ace_plan | all 18 fields | Read |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | all 9 fields | Read |
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | all 9 fields | Read |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | all 12 fields | Read |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset | all 12 fields | Read |
| DF-ACE-220 to DF-ACE-230 | v_ace_npa_sale | all 11 fields | Read |
| DF-ACE-231 to DF-ACE-243 | v_ace_lawsuit | all 13 fields | Read |
| DF-ACE-244 to DF-ACE-250 | v_ace_hearing | all 7 fields | Read |
| DF-ACE-251 to DF-ACE-260 | v_ace_pod | all 10 fields | Read |
| DF-ACE-261 to DF-ACE-269 | v_ace_write_off | all 9 fields | Read |
| DF-ACE-270 to DF-ACE-279 | v_ace_score | all 10 fields | Read |
| DF-ACE-280 to DF-ACE-285 | v_ace_party_product | all 6 fields | Read |
| DF-ACE-286 to DF-ACE-293 | v_ace_credit_decision | all 8 fields | Read |
| DF-ACE-294 to DF-ACE-300 | v_ace_esign | all 7 fields | Read |
| DF-ACE-301 to DF-ACE-304 | v_ace_iam_group | all 4 fields | Read |
| DF-EXT-001 to DF-EXT-012 | party_ext | all 12 fields | Not created or written here; table of RWB-P1-E1069-DB |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all 14 fields | Not created or written here; table of RWB-P1-E1069-DB |
| DF-EXT-027 to DF-EXT-035 | account_ext | all 9 fields | Not created or written here; table of RWB-P1-E1069-DB |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | all 14 fields | Not created or written here; table of RWB-P1-E1069-DB |

Field IDs are those in the Logical Data Model and Data Dictionary.

Names such as `ace_view_owner`, `v_data_dictionary` and `ace_to_date` are physical database objects (roles, views and functions). They are not LDM fields or entities in LDM v11 or Data Classification and Personal Data Inventory v6.

**Which side is this story's.** The 304 `DF-ACE-` fields are this story's: the view SQL defines those columns with the LDM v11 physical types (explicit casts), and the conformance test asserts their compilation, dictionary row and type. The `DF-EXT-` fields belong to RWB-P1-E1069-DB, which creates the four tables; this story reads party_ext and contact_point_ext values in the customer read and account_ext values in the account read, and writes none of them.

**Source tables.** Section A reads 21 ACE tables: `account`, `payment`, `customer`, `phone`, `email`, `address`, `ca_relation`, `aa_relation`, `collateral`, `asset`, `efs_action`, `efs_action_code`, `efs_assignment`, `bucket_log_snapshot`, `product`, `branch`, `bot_holiday`, `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation` and `ai_recommended_plan`. Section B reads 14, all added by RWB-ACE-001: `ace_batch_run`, `valuation`, `collateral_detail`, `npa_asset`, `npa_sale`, `lawsuit`, `hearing`, `pod_receipt`, `gl_write_off`, `collins_score`, `party_product`, `credit_decision`, `esign_request` and `iam_group`.

### 12. Contract

**12.1 REST operations provided**

The three read operations of Architecture v5 slide 15 on base `/api/recovery/source-data/v1`, published in rwb-source-data.yaml 5.1.0; this story builds them (RD-P1-060). Each has x-capability Case record R.

| Method | Path | Key | Views read | Success response |
|---|---|---|---|---|
| GET | `/accounts/{accountKey}` (getAccount) | accountKey | v_ace_account, v_ace_ca_relation; account_ext | 200 Account: the account columns, relations[], accountFacts, freshness (DP01) |
| GET | `/customers/{personKey}` (getCustomer) | personKey, maxLength 255 | v_ace_customer, v_ace_contact; party_ext, contact_point_ext | 200 Customer: the person columns, partyFacts, contacts[], freshness (DP02) |
| GET | `/collateral/{assetKey}` (getCollateral) | assetKey | v_ace_collateral; v_ace_collateral_detail when Section B is live (DL43 flag) | 200 Collateral: assetKey, rows[] of the key, detail once Section B is live, freshness (DP06) |

Response properties are the view columns in camelCase. Customer holds personKey, cifNo, firstName, lastName, dateOfBirth, deceasedDate, deceasedFlag, gender, nationality, maritalStatus, occupation, customerStatus, category, countryOfResidence, isStaff, branchCode, idNoMasked, idNoLast4, spouseName and vatNumber, with partyType, idType and segment once RWB-ACE-001 deploys (DL43 flag); each contact holds contactKey, contactType, usageCode, contactValue, contactValueMasked, city, postCode, country, consentStatus and verifiedAt. Callers: getCustomer – gateway-bff, rwb-comms, rwb-integration, rwb-deviation, rwb-case, RWB-P1-DM002-APP verification; getAccount – gateway-bff, rwb-case, rwb-payment, RWB-P3-E2006-APP; getCollateral – RWB-P3-E2006-APP, rwb-asset. Reads need no Idempotency-Key. Errors use the published Problem schema (RD-P1-004): 400 MSG-GEN-001, 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003 and 503 MSG-GEN-006. `GET /data-products/{productCode}/records` (RWB-P1-E1016-APP, which answers no contact value), freshness (RWB-P1-E1015-APP), payments, readiness and the account-page read (RD-P1-022, RD-P1-024; GAP-3274) are other stories'. The full mapping of the 30 views to operations, owners and consumers is Pending under GAP-0549.

**12.2 REST operations consumed**

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | /api/recovery/access/v1/authorise | RWB-P4-E1037-CON | Authorise the requested field IDs before returning them. Request and response schemas and case-reference rule are Pending under GAP-0925, GAP-0990 and GAP-1404. One hop, 2 s at most and inside the caller budget; inner budgets, retries and breaker thresholds Pending under GAP-0567. |
| library | FieldMasker.mask(dto, session) | RWB-P4-E1037-CON | Mask every field tagged is_personal for the caller's user session or workload identity; a field with no rule is masked (RD-P1-060). |

**12.3 Events published**

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (published in RWB-P1-E1015-CON). This story publishes no business event and no decision record: a read is written to the PII access log only (RD-P1-072).

**12.4 Events consumed**

None. A view migration is a deployment step, not a reaction to an event, and Architecture v5 slide 15 gives the service no consumed event ("none: Airflow call; fallback polls ACE batch record").

**12.5 Workflows and activities**

None. The two view migrations, the conformance test and the three reads are synchronous steps. The workflows `AceIngestCheck` and `ReconciliationWorkflow` and the activities `reconciliation`, `listEligibleAccounts` and `snapshot(page)` are other P1 stories; the task queue is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story.

**12.7 Tables owned**

| Object | Schema | Owner | This story |
|---|---|---|---|
| 16 Section A and 14 Section B views | recovery | ace_view_owner; contract owner rwb-source-data | Creates from the source view definitions |
| three helper functions | recovery | ace_view_owner | Creates in Section A |
| sys_objects and sys_fields | rwb_source_data | P1 | Reads rows delivered by E1001; writes none |
| four extension tables | rwb_source_data | P1 | Created by E1069-DB; this story does not write them |

No table is created in recovery. The service login reads views only and has no table privilege on public.

**Contract version built against.** rwb-source-data.yaml 5.1.0 (API Specification v7), which holds the three reads (RD-P1-060).

**12.8 Contract fakes**

| Fake | Serves | Contract |
|---|---|---|
| RWB-P4-E1037-CON fake | POST /api/recovery/access/v1/authorise | Grant, refuse, field masking and timeout; exact request/response schema Pending under GAP-0925, GAP-0990 and GAP-1404 |
| tier2-ddl.sql fixture | Section B views | 14 tables and 12 added columns in DEV and pipeline test |
| recovery_views.sql of Physical Schema v9 | View definitions and helper functions | The conformance test compares the applied views with this file; a checksum list of the definitions is Pending under GAP-0566 |
| rwb-source-data fake package | getCustomer, getAccount, getCollateral | Examples of the three reads under fakes/rwb-source-data/5.1.0/ (RD-P1-011; RD-P1-060) |

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | GET /customers/{personKey}, /accounts/{accountKey}, /collateral/{assetKey} | POST /api/recovery/access/v1/authorise | Authorise schema Pending |
| Kafka | None | None | A read publishes no decision record (RD-P1-072) |
| Temporal | None | None | No workflow in this story |
| File | None | Migration and fixture files | Section B uses tier2-ddl.sql in DEV and pipeline test |
| SQL view | 30 recovery.v_ace_* views | ACE source tables | SELECT only; service login rwb_source_data |

### 13. Solution plan

**Migrations.** Add Section A views and helper functions after the P1 baseline. Add Section B views in a later sequence version, built against tier2-ddl.sql in DEV and pipeline test, and apply in other environments only after RWB-ACE-001. The sequence owner assigns new versions; applied files are never edited.

**API contract.** `AceReadController` serves getCustomer, getAccount and getCollateral of section 12.1; one repository per view family issues one SELECT per view keyed by the business key on the rwb_source_data login, with the statement timeout inside the caller budget (value Pending, GAP-0567). RWB-P1-DM001-APP and RWB-P1-DM002-APP prove the migrated read paths behind the account and customer reads. No records route is added here (RWB-P1-E1016-APP).

**Boundary.** BND-6 checks class references in `th.co.scb.ace.workbench.recovery.sourcedata` and SQL strings passed to JDBC, JPA native queries and query annotations for public relations; its failure fixtures sit in that package. The failure text is "Boundary rule BND-6 broken: {class} reads public.{table}. Read recovery.v_ace_{name} instead." Dynamic SQL detection remains Pending with the platform architecture owner under GAP-0906. The ITG rule rejects other services' view references.

**Authorization and audit.** Call the P4 authorise operation before returning restricted fields and apply FieldMasker to every is_personal field. Every read, masked or clear, writes one PII access log entry through ACE Common with the user, product, case UUID, field names and time, never a value; a failed write answers 503 MSG-GEN-006 with no data. No decision record is written for a read (RD-P1-072). The interim FieldMasker fake unmasks firstName, lastName and contactValue for the rwb-comms notice and rwb-integration outbound-file identities only; all other callers get masked values (NEW-GAP-D1).

**Section B.** Build against the fixture now. Outside DEV and pipeline test, with the Section B flag off, query no Section B view; freshness answers STALE with null businessDate and MSG-P1-001 (RD-P1-043). The flag key is Pending under GAP-0596.

### 14. Validation and messages

| Condition | Response |
|---|---|
| Invalid key or request | 400 Problem, MSG-GEN-001 |
| No valid caller identity | 401 Problem, MSG-P4-001 |
| Authorise refuses | 403 Problem, MSG-P4-002 |
| No view row for the key, or key outside scope | 404 Problem, MSG-P4-003 |
| PII access log write fails | 503 Problem, MSG-GEN-006 |
| Authorise or view timeout/unavailable | 503 Problem, MSG-GEN-006 |
| Section B feature flag off | Freshness STALE, null businessDate, MSG-P1-001 |

Responses use the Problem schema of RD-P1-004 (application/problem+json). A refusal uses MSG-P4-002; a timeout never does. No partial field list is returned on failure.

### 15. Screens and states

No screen is delivered by this story. SCR-44 is not built here; no screen states are asserted.

### 16. Test cases

| Acceptance criteria | Test case |
|---|---|
| AC1 to AC11 | TC-E1-069-01 to -11 |
| AC12, AC13 | TC-P1-E1069-APP-01, -02 |
| AC14 to AC20 | TC-P1-E1069-APP-03 to -09 |

The Test Cases v9 rows TC-E1-069-07 to -09, TC-E1-069-11 and TC-P1-E1069-APP-03 need the revised Then lines of AC7 to AC9, AC11 and AC14.

### 17. Guardrails

- Never read a public table from service code; read ACE through recovery views only.
- Never let another service login select a recovery view; every other service reads ACE data through this service's contract only.
- Never unmask a field already masked by a view.
- Do not return partial fields on authorise, database or audit failure.
- Keep Section B reads off until RWB-ACE-001 lands in the target environment.
- Do not write stale_flag or age_days; GAP-1509 is unresolved.
- Return no personal value without a successful authorise call, masking and PII access log entry; log no customer value; publish no decision record for a read.
- Mark auth shapes, mask forms, masking rule rows, timings and view mappings Pending; do not invent them.

### 18. Traceability

| Reference | Use |
|---|---|
| RD-P1-004 | Problem response schema and statuses |
| RD-P1-005 | One contract file, which holds the three reads |
| RD-P1-060; RD-P1-072 | Entity reads, masking and callers; reads are logged, not recorded as decisions |
| RD-P1-025 | Dictionary baseline asserted by AC5 |
| RD-P1-021 | Table and read ownership; records operation is RWB-P1-E1016-APP's |
| RD-P1-022; RD-P1-041 | Event owner; no freshness or stale-flag write here |
| RD-P1-024 | Case-list functions retired from P1 |
| RD-P1-043 | Section B fixture and feature-flag gate |
| GAP-0549; GAP-0566; GAP-0567; GAP-0568; GAP-0596; GAP-0901; GAP-0903; GAP-0906; GAP-0925; GAP-0990; GAP-1404; GAP-1509; NEW-GAP-S7-05 | Open view map, checksum list, timing, flag, mask, boundary, authorisation, stale writer and executing principal |
| Physical Schema v9; LDM v11; API Specification v7; Test Cases v9; RTM v9 | Current schema, fields, contract, tests and matrix |
| REQ-RDF-001; REQ-RDF-002; REQ-RDF-004; REQ-DRI-006 | ACE source data through the views only, collateral and appraisal read, no direct system-of-record call (TC-E1-069-01 to -06) |

### 19. Out of scope

- GET /data-products/{productCode}/records (RWB-P1-E1016-APP), freshness, payments, readiness and the account-page read (their P1 stories).
- Creating the four extension tables or the grants (RWB-P1-E1069-DB) and the service login (RWB-PLT-NF06-DB).
- Writing valuation_ext.stale_flag or age_days; Pending under GAP-1509.
- P3 case status, case-list workflows and case numbers.
- Section B deployment before RWB-ACE-001 lands.
- The `rwb_source_data` login (RWB-PLT-NF06-DB); the grant block, the PUBLIC revokes, the view owner `ace_view_owner` with its SELECT on the ACE tables, and the four extension tables: RWB-P1-E1069-DB.
- The proof of the grant matrix across the 19 logins and the second half of boundary rule BND-6 (no `v_ace_*` view named outside rwb-source-data, no other service's schema named): RWB-ITG-E1069-ITG.
- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The masking policy rows and the masking answer itself: rwb-access, RWB-P4-E1069-APP (DP-08); this story takes the answer and applies the marker.
- The dictionary content and its maintenance: RWB-P1-E1001-APP for the metadata rows and RWB-E1-064 in the legacy set for the dictionary of the 14 data products.
- The freshness stamp (RWB-P1-E1015-APP), reconciliation, data products and business-day operations: the other P1 stories. P1 holds no case list (RD-P1-024).
- The features that read a Section B view: their own stories, behind their flags until the Section B migration is applied.
- The screens that show a customer, an account or a collateral record: gateway-bff and the screen owners (DP-19).
- The rest of RWB-TE-001 in the target: this story adds boundary rule BND-6 and the `sourceViews` list only.
- Any change to the 30-view list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map.

### 20. Remaining delivery steps

- Size: Not specified; owner squad lead at refinement.
- Epic design sign-off: Pending; owner product owner and design authority.
- CON Done: Pending the P4 authorise shape; the three reads are in rwb-source-data.yaml 5.1.0; owner service contract owner and P4 contract owner.
- Fake published: Pending the examples of the three reads under fakes/rwb-source-data/5.1.0/; owner service contract owner and QA lead.
- Test data in DEV: Pending Section B and authorise fixtures; owner QA and platform DB owner.
