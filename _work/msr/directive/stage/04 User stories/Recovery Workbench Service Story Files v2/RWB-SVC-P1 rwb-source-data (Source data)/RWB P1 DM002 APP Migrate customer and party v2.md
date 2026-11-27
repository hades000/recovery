# RWB-P1-DM002-APP Migrate customer and party

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15 |
| Parallel lane | L-P1-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1044-CON |
| Contract dependencies | None |
| Contract version | v1, the version named by the /v1 path this story builds against |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-P1-DM002-APP-16); the squad sizes it at refinement |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-DM-002 for rwb-source-data, whose migration D-RCV-35 (U1) withdrew. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a collections officer (RW-PHONECOL) and a data steward (RW-DATASTEW)**, I want **the customer and party read path of rwb-source-data built on the service's own read of `v_ace_customer` for the customer and the masked identity, `v_ace_contact` for phone, e-mail and address, `v_ace_ca_relation` for the borrower, guarantor and co-borrower roles, and on `party_ext` and `contact_point_ext` for the Workbench flags and consent**, so that **the case screen and the engines read the one copy that ACE holds, the clear identity number never leaves ACE, and the Workbench keeps only the decisions that are its own**.

**The legacy key is withdrawn, and this story is the replacement.** RWB-DM-002 is **Removed by D-RCV-35 (U1)**. The legacy story, its three acceptance criteria (AC1 to AC3) and its four test cases (TC-DM-002-01 to TC-DM-002-04) are withdrawn: ACE ingests the SCBPDM customer, phone, e-mail and address data and holds the one copy, and the Workbench loads none of it, so there is nothing to extract, transform, load, reconcile or cut over. This story therefore does not migrate a customer, a party, a phone, an e-mail or an address. It builds the read path that replaces the migration, and nothing else.

The legacy rows, character for character:

| Legacy row | Text |
|---|---|
| Status | Removed |
| Decision | D-RCV-35 (U1) |
| Why | ACE ingests the SCBPDM customer, phone, email and address data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile. |
| Read path instead | v_ace_customer for the customer and the masked identity, v_ace_contact for phone, email and address, v_ace_ca_relation for the borrower, guarantor and co-borrower roles, and party_ext and contact_point_ext for the Workbench flags and consent |
| Data product | DP02 stays in the catalog with system of record "ACE (ingested from SCBPDM)" and its view list. Only the migration story leaves. |
| Withdrawn IDs | AC1 to AC3; TC-DM-002-01 to TC-DM-002-04 |

### 2. Business rationale

A recovery case is about a person and the accounts behind that person. The customer profile, the identity number, the phone, the e-mail, the address and the borrower, guarantor and co-borrower roles are SCBPDM data, and ACE ingests them and holds the one copy (Architecture v5 slide 7; D-RCV-35 U1). Under D-RCV-35 and ADR-010 the Workbench reads that copy and never loads it: only rwb-source-data reads the 30 SELECT-only `recovery.v_ace_*` views, every other service asks rwb-source-data, and a link to an ACE record is a business key with no foreign key into ACE, because ACE cascades deletes on the account (Architecture v5 slides 8, 9, 11 and 12; D-RCV-35 U4; DP-05). The legacy migration story was written before that decision and is withdrawn with its criteria and its tests.

The withdrawal leaves a gap that this story fills. The legacy story was the only story in the key that named the customer and party data at all, so removing it without a replacement would leave the case screen and the engines with no read path. This story builds that read path: the customer and the masked identity from `v_ace_customer`, the phone, e-mail and address from `v_ace_contact`, the borrower, guarantor and co-borrower roles from `v_ace_ca_relation` — which is the legacy "Read path instead" row, applied — and the Workbench's own decisions about those ACE records in two 1:1 extension tables, `party_ext` for the vulnerable, deceased-override, bankruptcy and fraud flags and `contact_point_ext` for consent and contact quality (D-RCV-35 U3; FSD P1 A2.1.3.2; TSD P1 T3.5).

Two boundaries hold the story together. The first is the identity number: it never leaves ACE, because `v_ace_customer` returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`) and nothing else, so no component of this service can render a clear number even by accident (FSD P1 BR-P1-001-6; TSD P1 T3.4). The second is ownership: `party_ext` and `contact_point_ext` hold a Workbench decision about an ACE record and never a copy of an ACE column, are 1:1 on the ACE business key, and carry no foreign key into `public` (FSD P1 BR-P1-001-5; TSD P1 T3.5). Nothing this story builds writes a customer, a phone, an e-mail or an address anywhere, and nothing it builds sends one to a data lake: the lake is removed and reporting reads events (DP-17; Architecture v5 slides 8 and 9).

DP02 stays in the data product catalog with system of record "ACE (ingested from SCBPDM)" and its view list, and this story is the read path behind it (FSD P1 A2.2; legacy "Data product" row). The story adds no new requirement, because the legacy key carried none: it delivers the customer and party slice of DP02 that the withdrawal left unbuilt.

### 3. Preconditions

- RWB-P1-E1069-DB has delivered the 30 `recovery.v_ace_*` views in schema `recovery`, the per-service login, the grants and the four extension tables, so `party_ext` (`DF-EXT-001` to `DF-EXT-012`) and `contact_point_ext` (`DF-EXT-013` to `DF-EXT-026`) exist in `rwb_source_data` with `person_key` and `contact_key` as their primary keys (legacy RWB-E1-069 AC7; TSD P1 T3.5).
- RWB-P1-E1069-APP has delivered the per-service Flyway sequence of the view set and the conformance test, so this story adds one migration to a sequence that already runs and does not create, alter or grant on a view (DP-15).
- These two stories are **preconditions, not build dependencies**: the Work Package fixes the build edges of this story as `RWB-PLT-E1044-CON` only, and the story is built against the contract fakes of the view set from Day 1 (GAP-0556; ASM-0792).
- The platform Flyway contract RWB-PLT-E1044-CON is in place: one Flyway sequence per service, run in the service's own schema, with an applied version never edited in place (DP-15; ADR-021).
- The rwb-source-data login holds SELECT on the 30 views and DML on `rwb_source_data` only, and no privilege of any kind in `public` (DP-02; ADR-010; FSD P1 BR-P1-001-4).
- The batch gate and the freshness stamp are live in this service: a business date whose ACE batch is not COMPLETE gives the warning MSG-P1-001 and marks DP02 stale, so the read path never presents stale customer facts as current (RWB-P1-E1013-APP; FSD P1 A2.14, VR-P1-001-1; `data_product_load`, `v_ace_batch_status`).
- The masking answer is resolved before an ACE-sourced personal field is returned, as the service standard over the rwb-access authorise contract (DP-08 in the target, `POST /api/recovery/access/v1/authorise`); this story adds no contract dependency and no pattern for it, because the Work Package fixes `Contract dependencies` as None and `Patterns applied` as DP05 and DP15 (GAP-0554; ASM-0790).
- The feature switch of the read path is a parameter of the platform flag library (R-PREC default ruling, feature flags). Its key and its default are Not specified in the source documents (GAP-0556; ASM-0793).

### 4. Flow

1. A caller asks rwb-source-data for the customer and party facts of one `person_key`. The 13 columns of the legacy `party` table and the eight of `contact_point` are **not** in this service: they are read from the views on every call (TSD P1 T3.10; D-RCV-35 U1).
2. The guard resolves the caller's right for the capability area of the read before any view is touched; a refusal stops the call and no view is read (MSG-P4-002).
3. The batch gate is checked for the business date: when the ACE batch is not COMPLETE, the answer carries the warning MSG-P1-001 and the DP02 freshness of the business date, and the read is still answered with the date it is from (VR-P1-001-1; FSD P1 A2.14).
4. `CustomerPartyReadRepository` reads `v_ace_customer` by `person_key` for the customer profile, and selects `id_no_masked` and `id_no_last4` for the identity — never a clear number, because the view has none (FSD P1 BR-P1-001-6).
5. The same repository reads `v_ace_contact` by `person_key` for the phone, e-mail and address rows, with `contact_key` and `contact_type` carried through, and reads `v_ace_ca_relation` by `person_key` for the borrower, guarantor and co-borrower roles with their guarantee amounts and dates (TSD P1 T3.3; DF-ACE-084 to DF-ACE-088).
6. `PartyExtRepository` reads the one `party_ext` row for the `person_key`, and `ContactPointExtRepository` reads the one `contact_point_ext` row per `contact_key`, so the Workbench flags and consent join to the ACE rows by business key and by nothing else (TSD P1 T3.9).
7. The assembled answer names the masked identity, the contacts with their consent and quality, the relations with their roles, the flags, the business date and the freshness. It holds no copy of a customer, a phone, an e-mail or an address owned by this service, and nothing is written by the read.
8. The mandated masking is applied per field before the answer leaves the service; the clear identity number is not a field of the answer, of a log line, of an event or of a test fixture at any step (FSD P1 BR-P1-001-6; Architecture v5 slide 12).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A view read fails (statement timeout, connection loss or a missing view) | The call answers 503 with no partial answer and nothing is written; no flag and no consent is returned from a half read | None: 503 with no field text | AC2 |
| X2 | The ACE batch for the business date is not COMPLETE | The facts are answered with the business date they are from and the DP02 freshness; DP02 is flagged stale and the warning is shown | MSG-P1-001 | AC2, AC5 |
| X3 | The caller holds no right for the read | The call is refused before the first view read, so no customer fact, no flag and no contact is returned and nothing is written | MSG-P4-002 | AC6 |
| X4 | The `person_key` has no row in `v_ace_customer` | The answer is not-found and names the key; no default customer, no empty row and no extension row is written | None | AC5 |
| X5 | A second `party_ext` row is written for one `person_key` | The write is refused by the primary key and the first row is unchanged | SQLSTATE 23505 duplicate key value violates unique constraint party_ext_pkey | AC4 |
| X6 | The migration of this story is applied a second time | Flyway reports the version as already applied; no table is created twice and no version is edited in place | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the platform Flyway contract and the contract fakes of the view set; the views, the grants and the extension tables are preconditions owned by RWB-P1-E1069-APP and RWB-P1-E1069-DB |
| Negotiable | The answer field names, the feature-switch key and the shape of each extension read are open; the boundaries (no copy, no clear identity, one row per key) are fixed |
| Valuable | The customer and party facts of DP02 are readable from the one copy ACE holds, without a migration and without a second copy of a person |
| Estimable | One repository over three views, two extension repositories, one masking hook and one no-op migration |
| Small | Fits one sprint with its tests, as the rework of a withdrawn story that carries no legacy criterion |
| Testable | Every criterion in section 7 is one automated test on synthetic keys; no ACE data is needed |

The wave tag of this story is the EP08 business-epic tag, and Ready to start is read from the dependency graph only, so the story may be picked up on Day 1 on its single platform contract (GAP-0555; ASM-0791).

### 7. Acceptance criteria

```gherkin
Feature: The customer and party read path of rwb-source-data, replacing the withdrawn migration

  Background:
    Given schema "rwb_source_data" holds "party_ext", "contact_point_ext" and the Flyway history
    Given the 30 "recovery.v_ace_*" views exist in schema "recovery" and only the rwb-source-data login holds SELECT on them
    Given the ACE batch for the business date in force is COMPLETE in "v_ace_batch_status"

  Scenario: AC1 The service schema holds no migrated customer and no part of the legacy migration (new, D-RCV-60)
    Given the per-service Flyway sequence of "rwb_source_data" for this story
    When the pipeline applies it to schema "rwb_source_data"
    Then the schema holds "party_ext", "contact_point_ext" and the Flyway history
    And it holds no table named "party", "customer", "contact_point" or "phone"
    And the sequence holds no extract, no identifier map, no load, no reconciliation and no cutover step of the legacy key
    And the migration of this story creates no table, no view and no copy of an ACE row
    When the same version is applied a second time
    Then Flyway reports it as already applied and no object is created twice

  Scenario: AC2 The facts are read from the three views and the Workbench keeps only its own decisions (new, D-RCV-60)
    Given person_key "P0000123" exists in "v_ace_customer", in "v_ace_contact" and in "v_ace_ca_relation"
    Given "P0000123" has one "party_ext" row and one "contact_point_ext" row for contact_key "PHONE:PH-0001"
    When the read path answers the customer and party facts for "P0000123"
    Then the customer facts come from "v_ace_customer", the phone, e-mail and address facts from "v_ace_contact" and the borrower, guarantor and co-borrower roles from "v_ace_ca_relation"
    And the flags come from "party_ext" read by "person_key" and the consent from "contact_point_ext" read by "contact_key"
    And the answer names the business date and the DP02 freshness it was read at
    And "rwb_source_data" holds no row of the customer, the contact or the relation beyond the flags and the consent
    And no component of this story writes a customer, a phone, an e-mail or an address
    When the ACE batch for the business date is not COMPLETE
    Then the answer still names the date it is from and the freshness, and it is flagged stale with MSG-P1-001

  Scenario: AC3 The identity answers masked and the clear number is unreachable (new, D-RCV-60)
    Given person_key "P0000123" in "v_ace_customer" carries "id_no_masked" as "DF-ACE-073" and "id_no_last4" as "DF-ACE-074"
    When the read path answers the identity of "P0000123"
    Then the answer holds "id_no_masked" and "id_no_last4" and no other form of the identity number
    And the clear identity number is unreachable from this service, because the view returns the two masked columns only
    And no log line, no event, no workflow input and no test fixture of this story holds the clear number

  Scenario: AC4 The flags and the consent are read by business key, one row each (new, D-RCV-60)
    Given person_key "P0000123" has one "party_ext" row with "vulnerable" true and one "contact_point_ext" row for contact_key "PHONE:PH-0001" with "consent_given" true
    When the read path answers the flags and the consent for "P0000123"
    Then "party_ext" is read by "person_key" and returns one row with the four flags and the seven standard columns
    And "contact_point_ext" is read by "contact_key" and returns one row with "consent_given", "consent_at", "verified_at", "failed_count" and "source"
    And neither table carries a copy of a view column and neither carries a foreign key into ACE
    When a second "party_ext" row is written for "P0000123"
    Then the write fails with SQLSTATE 23505 duplicate key value violates unique constraint party_ext_pkey
    And "party_ext" still holds one row for "P0000123"

  Scenario: AC5 A person_key with no view row is not-found and writes nothing (new, D-RCV-60)
    Given person_key "P0099881" has no row in "v_ace_customer"
    When the read path is asked for the customer and party facts of "P0099881"
    Then the answer is not-found and names "P0099881"
    And no row is written to "party_ext", to "contact_point_ext" or to the Flyway history
    And no default customer, no placeholder identity and no empty contact list is returned

  Scenario: AC6 A caller without the right is refused before any view is read (new, D-RCV-60)
    Given the caller holds a role whose capability letters for the read are "-"
    When the caller asks the read path for the facts of "P0000123"
    Then the call is refused with status 403 and message MSG-P4-002
    And no view is read and no flag, no consent, no contact and no relation is returned
    And nothing is written

  Scenario: AC7 The business rules of section 8 hold across the schema and the read path (new, D-RCV-60)
    Given the delivered schema "rwb_source_data" and the read path of this story
    When the boundary checks of BR1 to BR8 run against them
    Then no extract, no identifier map, no load, no reconciliation and no cutover runs for the customer and party data
    And ACE is read only through the SELECT-only "recovery.v_ace_*" views, no constraint references a "public" table and each link to an ACE record is a "varchar(255)" business key with no foreign key
    And "v_ace_customer" returns the identity number only as "id_no_masked" and "id_no_last4"
    And each extension table holds no copy of an ACE column, is 1:1 with the ACE record and carries the seven standard record columns
    And "party_ext" is keyed by "person_key" and "contact_point_ext" by "contact_key", with "contact_type" PHONE, EMAIL or ADDRESS
    And the facts are data product DP02 with system of record "ACE (ingested from SCBPDM)" and with "party_ext" and "contact_point_ext" as its Workbench tables
    And no copy of the customer, the contact or the relation data reaches a data lake or a reporting table
    And the flags, the consent, the switch and the answer selection are data rows and parameters, and the key joins are read from the dictionary field IDs
```

The seven criteria above are new and test only the deliverable named in the title: the customer and party read path built on the service's own read of the views, and the Workbench's own flags and consent. No legacy criterion and no legacy test text is copied into this story, because the legacy criteria of RWB-DM-002 (AC1 to AC3) and its test cases (TC-DM-002-01 to TC-DM-002-04) are withdrawn with the migration by D-RCV-35 (U1) (GAP-0552; ASM-0788).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The legacy key is withdrawn: no extract, no identifier map, no load, no reconciliation and no cutover runs for the customer and party data, because ACE holds the one copy | D-RCV-35 (U1); legacy RWB-DM-002 Status Removed; TSD P1 v3 T3.10 (`party`, `contact_point` removed) |
| BR2 | The Workbench reads ACE only through the SELECT-only `recovery.v_ace_*` views, only rwb-source-data reads them, and no constraint in the schema references a `public` table; a link to an ACE record is a `varchar(255)` business key with no foreign key | D-RCV-35 (U4); ADR-010; Architecture v5 slides 7, 8, 9, 11, 12 and 37; FSD P1 BR-P1-001-2 and BR-P1-001-3 |
| BR3 | The clear identity number never leaves ACE: `v_ace_customer` returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`) only | FSD P1 BR-P1-001-6; TSD P1 T3.4 (DF-ACE-073, DF-ACE-074) |
| BR4 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column; it is 1:1 with the ACE record and carries the seven standard record columns | FSD P1 BR-P1-001-5; TSD P1 T3.5 |
| BR5 | `party_ext` is keyed by `person_key` and `contact_point_ext` by `contact_key` (`contact_type:key`), one row each; `contact_type` is PHONE, EMAIL or ADDRESS | TSD P1 T3.5 and T3.9; FSD P1 A2.1.3.2 |
| BR6 | The customer and party facts are data product DP02, system of record "ACE (ingested from SCBPDM)", with `party_ext` and `contact_point_ext` as its Workbench tables | FSD P1 A2.2 (DP02 row); legacy RWB-DM-002 "Data product" row |
| BR7 | No copy of the customer, the contact or the relation data reaches a data lake or a reporting table: the lake is removed and reporting reads events | DP-17; Architecture v5 slides 8 and 9 |
| BR8 | No value a business person may change is written in code: the flags, the consent, the switch and the answer selection are data rows and parameters, and the key joins are read from the dictionary field IDs | FSD P1 BR-P1-001; DP-05; DP-15 |

Where each rule lives in the target: BR1 is the reason this story exists and needs no code — it needs the absence of code, which AC1 tests. BR2 and BR3 are properties of the views and of the grant, proved here by reading them and by never selecting a column the view does not have. BR4, BR5 and BR8 are properties of `rwb_source_data` and of the read path. BR6 is a catalog row owned by the data product story of P1. BR7 is a prohibition: no relay, no export and no lake copy is written by this service for DP02. The consent and contact-quality rows of `contact_point_ext` are written at cutover by the legacy DM-005 cutover load, not by this service; this service reads them and writes none.

### 9. State transitions

None for the case. This story moves no case, no task and no account state: the case states move in rwb-case and the treatment states in rwb-treatment, and this story reads neither. The only states this story moves are the Flyway version of its own migration and the read path going live.

| From | Event | Condition | To |
|---|---|---|---|
| the previous applied version of the rwb-source-data Flyway sequence | the pipeline applies the migration of this story | The platform Flyway contract validates the sequence and the schema is `rwb_source_data` | The new version is recorded in the Flyway history; an applied version is never edited in place |
| the read path closed | the feature switch is turned on for the service | The views, the grants and the two extension tables exist | The customer and party read path answers; off closes it again |

The freshness of DP02 is moved by the batch gate of this service, not by this story: LOADED and STALE are set from `v_ace_batch_status` into `data_product_load` by RWB-P1-E1013-APP, and this story only reads the stamp it finds (FSD P1 A2.14).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Reads the three views, reads the two extension tables, applies the mandated masking and returns the answer; writes no customer row |
| RW-CASEOWN, case owner | Reads the customer and party facts of a case they own, masked as answered |
| RW-PHONECOL, collections officer | Reads the same facts for a case in their scope, masked as answered |
| RW-DATASTEW, data steward | Reads the facts and the DP02 freshness for any case; owns the catalog row of DP02, not this story |
| RW-COE, centre of excellence | Reads the facts and the freshness, and reads the read-path history through the Flyway history |
| RW-AUDIT, internal audit | Reads the facts and the freshness; the access entry of the read is written by the authorise path, not here |
| RW-COMPLY, Compliance and PDPA officer | Reads which fields are masked and confirms that the clear identity number is unreachable |
| ACE view owner and ACE DBA | Not this story: the views, the grants and the login stay with RWB-P1-E1069-DB and RWB-ACE-001 |
| No approval level from the delegation of authority applies | The story takes no credit decision and approves nothing |

Every "who" in this table is a role code, and the role codes, their permissions, their scope and the masking policy are data in rwb-access (P4); this service asks for the answer over the authorise contract and never reads `rwb_access` tables (DP-01). The roles named above are the ones the sources hold for a case read; this story adds no role and changes no permission row.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` (schema `recovery`) | `cif_no`, `person_key`, `first_name`, `last_name`, `date_of_birth`, `deceased_date`, `deceased_flag`, `gender`, `nationality`, `marital_status`, `occupation`, `spouse_name`, `customer_status`, `category`, `country_of_residence`, `is_staff`, `branch_code`, `vat_number`, `id_no_masked`, `id_no_last4` | Read |
| DF-ACE-073 and DF-ACE-074 | `v_ace_customer` (schema `recovery`) | `id_no_masked`, `id_no_last4` — the only identity the view exposes | Read; the clear number is not a column and is never written |
| DF-ACE-075 to DF-ACE-083 | `v_ace_contact` (schema `recovery`) | `contact_type`, `contact_key`, `person_key`, `contact_value`, `contact_value_masked`, `usage_code`, `city`, `post_code`, `country` | Read |
| DF-ACE-084 to DF-ACE-088 | `v_ace_ca_relation` (schema `recovery`) | `person_key`, `account_key`, `relation_type`, `amount_of_guarantee`, `date_of_guarantee` | Read |
| DF-EXT-001 to DF-EXT-012 | `party_ext` (schema `rwb_source_data`) | `person_key`, `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` and the seven standard columns | Read; one row per `person_key` |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` (schema `rwb_source_data`) | `contact_key`, `contact_type`, `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` and the seven standard columns | Read; one row per `contact_key` |
| Flyway history | schema `rwb_source_data` | version, description, checksum, applied at | Write (the version of this story's migration) |

No ACE row, no view column and no other service's row is copied into `rwb_source_data`: `party_ext` and `contact_point_ext` hold the Workbench's own decision about an ACE record, keyed by `person_key` and `contact_key`, and nothing else (FSD P1 BR-P1-001-5; D-RCV-35 U3). The legacy `party` table (13 fields) and the legacy table of 8 fields named `contact_point` (a name that is not a field or entity in LDM v9 or Data Classification v5) have no target: they are the copy that D-RCV-35 (U1) removes (TSD P1 T3.10). The read path returns the phone, e-mail and address value from `v_ace_contact` because notices and calls need it, and the display masking of that value is applied per field before the answer leaves the service (FSD P1; TSD P1 T3.4). The field IDs are those in the Logical Data Model and Data Dictionary v9. The read path reads the parameters of BR8 and the contact types of BR5 (PHONE, EMAIL, ADDRESS); the parameter names are Not specified in the source documents (DOR-RWB-P1-DM002-APP-20), and the reference-data contract is DP-06 and DP-07.

The exact selection of columns the answer carries, and whether the read path returns every one of the 20 customer fields or a subset, are Not specified in the source documents (GAP-0553; ASM-0789).

### 12. Contract

#### 12.1 REST operations provided

None new. The read of a customer and its parties is the operation `GET /customers/{id}` of rwb-source-data, which belongs to RWB-P1-E1069-APP and its published contract on base `/api/recovery/source-data/v1`; this story delivers the repository and the masking hook behind that operation and claims no path, no query parameter and no response field of its own. It is said once here so that the ownership is not in doubt: the path, the parameter and the response schema are RWB-P1-E1069-APP's, and the fields this story answers with are Not specified in the source documents (GAP-0556; ASM-0792).

#### 12.2 REST operations consumed

None at run time beyond the P1 read contract: the service reads its own views and its own schema, and the masking answer arrives on the authorise decision the caller path already takes, one hop, 2 s. The one-hop and 2 s budget is the service standard of the delivery model (Template and Rules §R5.5, DP-11); it is named here as the standard the story complies with and is not added to Patterns applied, because the Work Package fixes that row as DP05 and DP15.

#### 12.3 Events published

None. The read path publishes no event: a customer read is a synchronous answer and DP-09 is not a pattern of this story. The DP02 facts travel to reporting, when they do, as events of the reporting path and never as a copy written here (DP-17).

#### 12.4 Events consumed

None. The batch gate reads `v_ace_batch_status` and the freshness stamp in `data_product_load` inside this service; no topic starts the read.

#### 12.5 Workflows and activities

None. The read path is a synchronous repository call in the caller's thread; no Temporal workflow and no activity is in this story, and the task queue `rwb-source-data` carries none of its work.

#### 12.6 Schedules

None. No Temporal Schedule and no batch job sits in this story; the freshness schedule of the service belongs to RWB-P1-E1013-APP.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `party_ext` | `rwb_source_data` | P1 | Reads the one row per `person_key`; the primary key refuses a second row |
| `contact_point_ext` | `rwb_source_data` | P1 | Reads the one row per `contact_key` |
| Flyway history | `rwb_source_data` | P1 | Writes the version of this story's migration |
| `party`, `customer`, `contact_point`, `phone` | — | none | **Do not exist.** The legacy copy of SCBPDM data is removed by D-RCV-35 (U1) and this story creates no such table |
| `v_ace_*` views | `recovery` | ACE view owner, granted by RWB-P1-E1069-DB | Read only, never created, altered or granted here |

No table of another service is read and no foreign key crosses a schema (DP-01). The dictionary tables `sys_objects`, `sys_fields` and `sys_field_version` stay with P1's catalog work, and this story writes no dictionary row.

#### 12.8 Contract fakes

| Fake | Serves | This story |
|---|---|---|
| rwb-source-data contract fake (RWB-P1-E1069-APP) | `GET /customers/{id}` on `/api/recovery/source-data/v1` | The caller side of the read path, so consumers build before the service is live |
| ACE view fixtures | `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation` | Synthetic rows only: a key that exists in all three, a key with contacts and no relation, and a key with no view row (AC2, AC3, AC5) |
| extension fixtures | `party_ext`, `contact_point_ext` | Synthetic rows only, with the duplicate-key fixture of AC4 |
| authorise fake | The rwb-access authorise contract | A granted read and a refused read with MSG-P4-002 (AC6) |
| batch fixture | `v_ace_batch_status` | A COMPLETE batch and an incomplete batch, for MSG-P1-001 |

Every fixture uses synthetic keys; no ACE row and no personal value is copied into a fixture, and the clear identity number appears in no fixture at all.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided, 0 consumed | The read is served on the RWB-P1-E1069-APP operation; no path is added and no outbound call is made by this story |
| Kafka | 0 published, 0 consumed | No topic is added or consumed; DP-09 is not applied |
| Temporal | None | No workflow, activity or schedule |
| File | None | No file is read or written; the migration is SQL in the service's own sequence |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.customerparty`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (neither used by this story).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `CustomerPartyReadRepository` | Repository | Reads `v_ace_customer`, `v_ace_contact` and `v_ace_ca_relation` by `person_key`; selects `id_no_masked` and `id_no_last4` and never a clear identity; reads no `public` table and no other schema |
| `PartyExtRepository` | Repository | Reads the one `party_ext` row per `person_key` and writes the flag row of that key; the primary key is the 1:1 guard |
| `ContactPointExtRepository` | Repository | Reads the one `contact_point_ext` row per `contact_key` (`contact_type:key`) |
| `MaskingClient` | Client | Takes the masking answer for the ACE-sourced personal fields of the answer before they are returned, one hop, 2 s, and renders no clear value |
| `V<version>__customer_party_read_path.sql` | Migration | The no-op baseline of the read path in the service's own Flyway sequence: records the version, creates no table, no view, no copy and no index that the baseline does not already have |

**Database and migrations**

- Reads `v_ace_customer`, `v_ace_contact` and `v_ace_ca_relation` in schema `recovery` under the rwb-source-data login, and `party_ext` and `contact_point_ext` in `rwb_source_data`.
- The migration of this story carries the next version of the per-service sequence after the V0001 baseline (DP-15; ADR-021). It is deliberately a no-op: `party_ext` and `contact_point_ext` arrive with RWB-P1-E1069-DB, the views arrive with RWB-P1-E1069-APP, and this story adds no table and no column of its own.
- No `v_ace_*` object and no `public` object is created, altered or granted here.
- No row of `data_product`, `sys_objects` or `sys_fields` is written by this story; the DP02 catalog row belongs to the catalog work of P1.

**Configuration and reference data**

- The two key joins are read as field IDs from the dictionary: `person_key` (`DF-ACE-056`, `DF-EXT-001`) and `contact_key` (`DF-ACE-076`, `DF-EXT-013`). No column name and no field-ID list is written in Java as a business value.
- The feature switch is read as a parameter of the platform flag library. Its key and default are Not specified in the source documents (GAP-0556; ASM-0792); off closes the read path, answers 503 with no body, and reads no view.
- The login is the rwb-source-data login (DP-02); it is the only principal with SELECT on the 30 views.

**Build steps**

1. `CustomerPartyReadRepository` over the three views with synthetic fixtures; tests for AC2 and AC3, including the assertion that no selected column holds a clear identity number.
2. `PartyExtRepository` and `ContactPointExtRepository` with the 1:1 key reads and the duplicate-key path; tests for AC4.
3. The answer assembled with the business date and the DP02 freshness, and the stale path with MSG-P1-001; the rest of AC2.
4. The not-found path for a `person_key` with no view row, with the assertion that nothing is written; test for AC5.
5. The refusal path before the first view read, with MSG-P4-002 and no read; test for AC6.
6. The no-op migration in the service's Flyway sequence, with the schema assertion that no `party`, `customer`, `contact_point` or `phone` table exists and the repeated-run assertion; test for AC1.
7. A contract-fake run of the whole path through `GET /customers/{id}` of RWB-P1-E1069-APP, so the story builds before the views and the service are live.

**Feature switch.** A parameter of the platform flag library, read at start and per call; off closes the read path and reads no view. The key and the default are Not specified in the source documents (GAP-0556; ASM-0793).

**Done when.** The tests in section 16 pass; the schema of `rwb_source_data` holds `party_ext`, `contact_point_ext` and the Flyway history and no `party`, `customer`, `contact_point` or `phone` table; a `person_key` answers from the three views with the masked identity only; the flags and the consent answer by business key with a second row refused at SQLSTATE 23505; and no statement of the service names a `public` table or another service's schema.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not COMPLETE when the read path answers | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required value of the answer is missing at the boundary of the read | Enter {field}. |
| MSG-P4-002 | The caller holds no right for the read | You cannot {action} here. Your role does not include it. |
| SQLSTATE 23505 | A second `party_ext` row is written for one `person_key` | duplicate key value violates unique constraint party_ext_pkey |

The message IDs are the legacy ones; the text of MSG-P1-001 is the Error and Message Standard v4 text (CG-ALL-1893), and the other texts are the legacy ones, unchanged. For MSG-P4-002, {action} names the action the caller tried — for example "read the customer of this case" — and never a case fact and never a field value. The duplicate-key text is the legacy text of the extension-table key, character for character (legacy RWB-E1-069 AC7 and its message row). No message of this story carries a name, an identity number, a phone number, an e-mail or an address.

### 15. Screens and states

No screen is built by this story. The customer and party facts are shown on the case screen of the recovery workspace, which reaches this service through the gateway-bff composite route (DP-19), one hop; the screen and its field-level rendering belong to the screen owner, and this story returns the facts with the mandated masking applied and no rendering of its own. The states an operator sees are the freshness of DP02 (current or stale with MSG-P1-001) and the not-found answer of a key with no view row (AC5); the story adds no screen state of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-002-01 | AC1, AC2, AC3, AC4 | Component | Synthetic `person_key` "P0000123" present in the three view fixtures with one `party_ext` row and one `contact_point_ext` row; the schema assertion of AC1 on `rwb_source_data`; a repeated run of the migration |
| TC-DM-002-04 | AC6 | Component | A caller whose capability letters for the read are "-", against the authorise fake; the assertion that no view is read and MSG-P4-002 is returned |
| TC-DM-002-05 | AC5 | Component | Synthetic person_key "P0099881" with no row in the customer view fixture; the assertion that the answer is not-found, that nothing is written to party_ext, contact_point_ext or the Flyway history, and that no default customer is returned |
| TC-DM-002-06 | AC1, AC4 | Component | Boundary test of the tables of section 12.7: the schema of rwb_source_data holds only party_ext, contact_point_ext and the Flyway history, and a second party_ext row for one person_key is refused at SQLSTATE 23505 |
| TC-DM-002-07 | BR1 | Component | Assertion that no extract, identifier map, load, reconciliation or cutover for customer and party data exists in the service |
| TC-DM-002-08 | BR2 | Component | Assertion that the service reads only the recovery.v_ace_* views and that a link to an ACE record is a varchar(255) business key with no foreign key |
| TC-DM-002-09 | BR3 | Component | Assertion that v_ace_customer answers id_no_masked and id_no_last4 only and that no clear identity number reaches the answer |
| TC-DM-002-10 | BR4 | Component | Assertion that party_ext and contact_point_ext hold no ACE column copy and carry the seven standard record columns |
| TC-DM-002-11 | BR5 | Component | Assertion that party_ext is keyed by person_key, contact_point_ext by contact_key, and contact_type is PHONE, EMAIL or ADDRESS |
| TC-DM-002-12 | BR6 | Component | Assertion that the DP02 catalog row names ACE as system of record with party_ext and contact_point_ext as Workbench tables |
| TC-DM-002-13 | BR7 | Component | Assertion that no customer, contact or relation data is written to a data lake or a reporting table |
| TC-DM-002-14 | BR8 | Component | Assertion that the flags, consent, switch and answer selection are read from data rows and parameters and that key joins use dictionary field IDs |
| TC-DM-002-15 | AC7 | Component | The delivered schema of rwb_source_data and the read path against the three view fixtures; the boundary checks of BR1 to BR8 as listed in AC7 |

The legacy test text of both cases is withdrawn with the migration by D-RCV-35 (U1), together with `TC-DM-002-02` and `TC-DM-002-03`, which no story carries. The two IDs are kept so that the withdrawn case and its replacement can be followed under the same identifier, and each replacement is recorded under that ID in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The legacy levels are kept at Component for both, because each test exercises one service's component against fixtures and fakes and no cross-service path.

### 17. Guardrails

- No business value in code: the flags, the consent, the switch, the key joins and the answer selection are data rows and parameters read with the version in force; no column name, field-ID range or flag default is written in Java as a business value (BR8).
- No personal data in events, logs, workflow inputs, tests or prompts: the answer carries the masked identity and the view values only, every fixture is synthetic, and the clear identity number appears in no fixture, no log line and no event of this story (BR3).
- ACE data only through the owner's contract or `v_ace_*` views, and here only through the views: a class that names a `public` table fails the boundary rule of the service, and no statement of this story names another service's schema (DP-01; DP-05; ADR-010).
- No copy of a customer, a phone, an e-mail or an address is written by this story: `party_ext` and `contact_point_ext` hold a decision about an ACE record, keyed by a business key, 1:1, with no foreign key into ACE (BR4; BR5).
- One hop and 2 s on the authorise and masking path; a slow answer refuses the read and returns nothing (DP-11 as the service standard).
- No lake copy and no reporting copy of DP02 is written here (BR7; DP-17).
- One migration per story in the service's own Flyway sequence (DP-15); an applied version is never edited, and a change is a new version with a later number.

### 18. Traceability

| Item | Value |
|---|---|
| Legacy key | RWB-DM-002 |
| Module | P1 Recovery data engine |
| Feature | Not specified in the source documents (DOR-RWB-P1-DM002-APP-2) |
| L3 process | Not specified in the source documents (DOR-RWB-P1-DM002-APP-2) |
| Status | Removed |
| Decision | D-RCV-35 (U1) |
| Data product | DP02 |
| Pattern | DP-05 |
| Pattern | DP-15 |
| Withdrawn IDs | AC1 to AC3; TC-DM-002-01 to TC-DM-002-04 |
| Replacement test IDs | TC-DM-002-01, TC-DM-002-04 (new text, same IDs) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence of the service's own schema |
| None | — | Contract dependencies, integration dependencies and external dependencies are empty for this story |
| RWB-P1-E1069-APP, RWB-P1-E1069-DB | App development, ACE DB | Preconditions, not build edges: the read-only views and their grants, the login and the two extension tables (GAP-0556; ASM-0792) |
| RWB-P1-E1013-APP | App development | The batch gate and the DP02 freshness stamp this story reads and reports |

The legacy key carried no requirement ID, so this story adds none and its fragment's requirement list is empty. Its business rules come from D-RCV-35 (U1, U3, U4), ADR-010, the FSD and TSD P1 v3 rules named in section 8, and the DP-05, DP-15 and DP-17 rows of the pattern table.

### 19. Out of scope

- The legacy extract, the identifier map, the load, the reconciliation and the cutover of RWB-DM-002: withdrawn by D-RCV-35 (U1), with AC1 to AC3 and TC-DM-002-01 to TC-DM-002-04.
- The 30 `recovery.v_ace_*` views, their SQL, their grants and the per-service login: RWB-P1-E1069-APP and RWB-P1-E1069-DB; the end-to-end grant proof across the 19 logins: RWB-ITG-E1069-ITG.
- The `GET /customers/{id}` operation, its path, its parameters and its response schema on `/api/recovery/source-data/v1`: RWB-P1-E1069-APP; this story claims no operation of its own.
- The masking policy rows, the roster of roles that see a field unmasked, the identity rules and the authorise decision itself: rwb-access (P4), RWB-P4-E1069-APP and RWB-P4-E1037-APP.
- Freshness and readiness: the `data_product_load` stamp, `AceDataReady` and `AceDataLate`, and the batch gate: RWB-P1-E1013-APP (FSD P1 A2.14).
- DP01, the account and arrears read path and the case-list reconciliation to `v_ace_account`: RWB-P1-DM001-APP and the reconciliation stories of P1.
- The data lake and any reporting or analytic copy of DP02: removed (DP-17; Architecture v5 slides 8 and 9).
- Every screen, including the case screen that shows these facts: gateway-bff and the screen owners (DP-19); this story returns data and draws no screen.
- The catalog rows of DP02, the data dictionary rows of the views and the extension tables, and the baseline-measure set: the catalog, dictionary and baseline work of P1.
