# RWB-P1-DM002-APP Migrate customer and party

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-021: `contact_point_ext` rows are written at cutover by RWB-P1-DM005-APP; the flag-write operation is RWB-P1-E1018-APP's (findings #2, #4).
- RD-P1-027: section 11 gives the disposition of every field by dictionary ID (findings #1, #6).
- RD-P1-004 and RD-P1-041: refusal, not-found, freshness and timeout answers are fixed; the authorise contract dependency is recorded (findings #3, #5, #7, #9).
- AC1, AC2 and AC4 to AC7 rewritten and AC8 to AC10 added. Still pending: the delivery steps in section 20 (findings #8, #10). The response schema is published (RD-P1-060; GAP-0566) and this story has no feature switch of its own (see the batch D bullet).
- Batch D: the story is a verification story that reads `GET /customers/{personKey}` and writes no row; its Flyway migration, repositories, flag writes and feature switch are removed, and the contact cardinality and absent-row clause moves to RWB-P1-DM005-APP (RD-P1-068; RD-P1-060). A STALE or never-stamped DP02 no longer refuses the read (RD-P1-060; RD-P1-062). Section 11 holds EXCLUDE and ACE_READ rows only.

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
| Patterns applied | DP05 |
| Parallel lane | L-P1-E |
| Ready to start | Day 1 |
| Depends on (build) | None. This verification story adds no migration and no build edge (RD-P1-068); the live run needs `GET /customers/{personKey}` of RWB-P1-E1069-APP (RD-P1-060) |
| Contract dependencies | rwb-source-data.yaml 5.1.0 `getCustomer` and its fake `fakes/rwb-source-data/5.1.0/` (RD-P1-060; RD-P1-011); RWB-P4-E1037-CON (authorise; FieldMasker); RWB-P1-E1015-CON (freshness answer of DP02) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7): `getCustomer`, schema `Customer`, and the problem body (RD-P1-060; RD-P1-005) |
| Readiness decisions | RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-021; RD-P1-027; RD-P1-041; RD-P1-043; RD-P1-045; RD-P1-060; RD-P1-062; RD-P1-068; RD-P1-072 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-P1-DM002-APP-16); the squad sizes it at refinement |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-DM-002 for rwb-source-data, whose migration D-RCV-35 (U1) withdrew. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a collections officer (RW-PHONECOL) and a data steward (RW-DATASTEW)**, I want **proof that the customer facts, the masked identity, the contact points, the consent and the Workbench flags of one person are served by `GET /customers/{personKey}` from the ACE views and the two extension tables, with nothing migrated and nothing written**, so that **the case screen and the engines read the one copy that ACE holds, the clear identity number never leaves ACE, and no second copy of a person is created in the Workbench**.

**The legacy key is withdrawn, and this story is the replacement.** RWB-DM-002 is **Removed by D-RCV-35 (U1)**. The legacy story, its three acceptance criteria (AC1 to AC3) and its four test cases (TC-DM-002-01 to TC-DM-002-04) are withdrawn: ACE ingests the SCBPDM customer, phone, e-mail and address data and holds the one copy, and the Workbench loads none of it, so there is nothing to extract, transform, load, reconcile or cut over. This story therefore migrates nothing (Data Migration Approach; RD-P1-068). It is a verification story: it reads `GET /customers/{personKey}`, which RWB-P1-E1069-APP builds (RD-P1-060), and writes no row. It adds no table, no column, no migration and no repository; flag writes on `party_ext` are RWB-P1-E1018-APP's and `contact_point_ext` rows are written at cutover by RWB-P1-DM005-APP (RD-P1-021).

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

The withdrawal leaves a gap that this story fills. The legacy story was the only story in the key that named the customer and party data at all, so removing it without a replacement would leave the case screen and the engines with no read path. That read path is `GET /customers/{personKey}`, built by RWB-P1-E1069-APP (RD-P1-060): the customer and the masked identity from `v_ace_customer`, the phone, e-mail and address from `v_ace_contact`, the four flags of `party_ext` and the consent status of `contact_point_ext`; the borrower, guarantor and co-borrower roles of `v_ace_ca_relation` are answered as `relations[]` of `GET /accounts/{accountKey}`. This story verifies that the customer read answers what the legacy "Read path instead" row asks for, without a migration (D-RCV-35 U3; FSD P1 A2.1.3.2; TSD P1 T3.5; RD-P1-068).

Two boundaries hold the story together. The first is the identity number: it never leaves ACE, because `v_ace_customer` returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`) and nothing else, so no component of this service can render a clear number even by accident (FSD P1 BR-P1-001-6; TSD P1 T3.4). The second is ownership: `party_ext` and `contact_point_ext` hold a Workbench decision about an ACE record and never a copy of an ACE column, are 1:1 on the ACE business key, and carry no foreign key into `public` (FSD P1 BR-P1-001-5; TSD P1 T3.5). Nothing this story does writes a customer, a phone, an e-mail or an address anywhere, and nothing it does sends one to a data lake: the lake is removed and reporting reads events (DP-17; Architecture v5 slides 8 and 9).

DP02 stays in the data product catalog with system of record "ACE (ingested from SCBPDM)" and its view list, and this story verifies the customer read behind it (FSD P1 A2.2; legacy "Data product" row; RD-P1-068). The story adds no new requirement, because the legacy key carried none: it proves that the customer slice of DP02 needs no migrated row.

### 3. Preconditions

- RWB-P1-E1069-DB has delivered the 30 `recovery.v_ace_*` views in schema `recovery`, the per-service login, the grants and the four extension tables, so `party_ext` (`DF-EXT-001` to `DF-EXT-012`) and `contact_point_ext` (`DF-EXT-013` to `DF-EXT-026`) exist in `rwb_source_data` with `person_key` and `contact_key` as their primary keys (legacy RWB-E1-069 AC7; TSD P1 T3.5).
- RWB-P1-E1069-APP serves `GET /customers/{personKey}` of rwb-source-data.yaml 5.1.0 (RD-P1-060). Until it is deployed, the checks run against the contract fake `fakes/rwb-source-data/5.1.0/` and its examples (RD-P1-011).
- The rwb-source-data login holds SELECT on the 30 views and DML on `rwb_source_data` only, and no privilege of any kind in `public` (DP-02; ADR-010; FSD P1 BR-P1-001-4).
- The DP02 freshness record is part of the answer: RWB-P1-E1015-APP alone writes `data_product_load`. The customer read does not refuse on a STALE or never-stamped DP02; the caller applies its own stale rule (RD-P1-060; RD-P1-062). Until the Section B views land, DP02 answers STALE with no business date (RD-P1-043); DEV and the pipeline use the synthetic Section B fixture.
- The read is authorised over the rwb-access contract (`POST /api/recovery/access/v1/authorise`, Case record R) and every personal field passes `FieldMasker.mask(dto, session)` of RWB-P4-E1037-CON (RD-P1-060; DP-08).
- No migration, no table, no repository and no feature switch is a precondition or a deliverable of this story (RD-P1-068).

### 4. Flow

1. The verification calls `GET /api/recovery/source-data/v1/customers/{personKey}` with synthetic keys: against the contract fake until RWB-P1-E1069-APP is deployed, and against the service afterwards (RD-P1-060).
2. The operation resolves the caller's right (Case record R) before any view is read; a refusal answers 401 MSG-P4-001 or 403 MSG-P4-002 and no view is read.
3. The check confirms the person columns of `v_ace_customer` in camelCase, with `idNoMasked` and `idNoLast4` as the only forms of the identity number, because the view has no clear number (FSD P1 BR-P1-001-6; TSD P1 T3.4).
4. The check confirms `contacts[]` holds one entry for each `v_ace_contact` row of the person with `contactKey`, `contactType`, `consentStatus` and `verifiedAt`, and `partyFacts` holds the four `party_ext` booleans, or null when the person has no `party_ext` row.
5. The check confirms `freshness` is the DP02 record and that a STALE or never-stamped DP02 still answers 200 (RD-P1-060; RD-P1-062).
6. The check confirms masking per field for a user session and for the two workload identities of AC10.
7. Before and after the run the check records the tables and row counts of `rwb_source_data`: no row is added, changed or deleted, and the package record of section 11 holds no CARRY row (RD-P1-068). The PII access log entry of each read is written by the read operation itself (RD-P1-060; RD-P1-072).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A view read fails (statement timeout, connection loss or a missing view), also after another view has answered | The call answers 503 with no partial answer and nothing is written | MSG-GEN-006 | AC9 |
| X2 | The DP02 stamp in use is STALE, or DP02 has never been stamped | 200 with `freshness.status` STALE; for a never-stamped product `businessDate` is null; the read is not refused (RD-P1-060; RD-P1-062) | None | AC2 |
| X3 | The caller holds no right for the read | 403 before the first view read, so no customer fact, no flag and no contact is returned and nothing is written | MSG-P4-002 | AC6 |
| X7 | No session, or no Workbench role | 401 before the first view read | MSG-P4-001 | AC6 |
| X8 | The authorise call does not answer within 2 s | 503; no field is returned | MSG-GEN-006 | AC9 |
| X10 | The `personKey` is longer than 255 characters or otherwise invalid | 400; no view is read | MSG-GEN-001 | AC5 |
| X4 | The `personKey` has no row in `v_ace_customer`, or is outside the caller's scope | 404; the problem body and the logs do not carry the key; no default customer is returned and no row is written | MSG-P4-003 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the rwb-source-data 5.1.0 contract fake and synthetic view fixtures from Day 1; the live run needs the operation of RWB-P1-E1069-APP |
| Negotiable | The fixture keys and the harness are open; the boundaries (nothing migrated, nothing written, no clear identity) are fixed |
| Valuable | Proves that the customer and party facts of DP02 are readable from the one copy ACE holds, without a migration and without a second copy of a person |
| Estimable | One set of contract and component checks on one operation, plus the package record |
| Small | Fits one sprint, as the rework of a withdrawn story that carries no legacy criterion |
| Testable | Every criterion in section 7 is one automated test on synthetic keys; no ACE data is needed |

The wave tag of this story is the EP08 business-epic tag, and Ready to start is read from the dependency graph only, so the story may be picked up on Day 1 on its single platform contract (GAP-0555; ASM-0791).

### 7. Acceptance criteria

```gherkin
Feature: Verification that customer and party data needs no migration

  Background:
    Given the "rwb-source-data" 5.1.0 fake or the deployed service answers "GET /api/recovery/source-data/v1/customers/{personKey}"
    Given synthetic fixtures for "v_ace_customer", "v_ace_contact", "party_ext" and "contact_point_ext"
    Given the DP02 stamp in use is business date "2026-11-30" with status LOADED

  Scenario: AC1 The story adds no object and writes no row
    Given the list of the tables, views, columns and indexes of "rwb_source_data", its "flyway_schema_history" rows and its row counts, recorded before the run
    When the verification of this story runs
    Then the recorded list, the history rows and the row counts are unchanged
    And the schema holds no table named "party", "customer", "contact_point" or "phone"
    And the delivery of this story holds no Flyway migration, no repository and no write statement

  Scenario: AC2 The customer facts are served by the published read, also when DP02 is not current
    Given personKey "P0000123" exists in "v_ace_customer" and "v_ace_contact"
    When "GET /customers/P0000123" is called by a caller granted the read
    Then the answer is 200 with the person columns, "partyFacts", "contacts" and "freshness" of DP02 with business date "2026-11-30" and status LOADED
    Given the DP02 stamp in use is business date "2026-11-27" with status STALE
    When the same read is called
    Then the answer is 200 with "freshness" status STALE and business date "2026-11-27"
    Given DP02 has never been stamped
    When the same read is called
    Then the answer is 200 with "freshness" status STALE and "businessDate" null
    And no row of "rwb_source_data" is written by the verification

  Scenario: AC3 The identity answers masked and the clear number is unreachable
    Given personKey "P0000123" in "v_ace_customer" carries "id_no_masked" and "id_no_last4"
    When "GET /customers/P0000123" is called
    Then the answer holds "idNoMasked" and "idNoLast4" and no other form of the identity number
    And no log line, no event, no workflow input and no test fixture of this story holds a clear identity number

  Scenario: AC4 The flags and the consent come from the extension tables by business key
    Given personKey "P0000123" has one "party_ext" row with "vulnerable" true and one "contact_point_ext" row for contact_key "PHONE:PH-0001" with a recorded consent
    When "GET /customers/P0000123" is called
    Then "partyFacts" carries "vulnerable" true with the other three booleans of the row
    And the contact "PHONE:PH-0001" carries the "consentStatus" and "verifiedAt" of its row
    When personKey "P0000456" has no "party_ext" row and its record is read
    Then "partyFacts" is null and no row is created

  Scenario: AC5 A key with no view row answers 404 and an invalid key answers 400
    Given personKey "P0099881" has no row in "v_ace_customer"
    When "GET /customers/P0099881" is called
    Then the answer is 404 "application/problem+json" with messageCode "MSG-P4-003"
    And neither the problem body nor any log line carries "P0099881" and no default customer is returned
    When a personKey of 256 characters is read
    Then the answer is 400 with messageCode "MSG-GEN-001" and no view is queried

  Scenario: AC6 A caller without a session or the right is refused before any view is read
    Given the caller holds no Case record R right
    When "GET /customers/P0000123" is called
    Then the answer is 403 "application/problem+json" with messageCode "MSG-P4-002"
    And no view is read, no customer field is returned and nothing is written
    When a request with no session asks for the same record
    Then the answer is 401 with messageCode "MSG-P4-001" and no view is read

  Scenario: AC7 The package record and the boundary rules hold
    Given the rows of "RWB-P1-DM002-APP" in sheet "Migration packages" of Source to Target Mapping v7 and the delivered "rwb_source_data" schema
    When the package record, the grants and the constraints are checked
    Then every row of the package is EXCLUDE or ACE_READ and none is CARRY or KEY
    And the "rwb_source_data" login holds SELECT only on the "recovery.v_ace_*" views and no privilege in "public"
    And "v_ace_customer" gives "id_no_masked" and "id_no_last4" only
    And no column of "party_ext" or "contact_point_ext" copies an ACE column and neither has a foreign key into ACE

  Scenario: AC8 Several contacts keep every contact
    Given "P0000123" has contacts "PHONE:PH-0001", "EMAIL:EM-0001" and "ADDRESS:AD-0001" and only "PHONE:PH-0001" has a "contact_point_ext" row
    When "GET /customers/P0000123" is called
    Then "contacts" lists the three contacts
    And no "contact_point_ext" row is created

  Scenario: AC9 A timeout or a partial view failure returns no partial answer
    Given "v_ace_customer" answers and the statement on "v_ace_contact" is cancelled by its statement timeout
    When "GET /customers/P0000123" is called
    Then the answer is 503 with messageCode "MSG-GEN-006", with no customer field and no write
    Given the authorise fake does not answer within 2 s
    When the same read is called
    Then the answer is 503 with messageCode "MSG-GEN-006" and no view field is returned

  Scenario: AC10 Each personal field follows the masking rule
    Given the FieldMasker fake unmasks "firstName", "lastName" and "contactValue" for the rwb-comms notice and rwb-integration outbound-file identities only
    When a user session with no unmasking rule reads "P0000123"
    Then "contactValue" equals the "contactValueMasked" value and "firstName", "lastName" and the address fields are masked
    When each of the two workload identities reads "P0000123"
    Then "firstName", "lastName" and "contactValue" are clear
    And no log line holds a clear identity number
```

The ten criteria test only the deliverable of this story: the proof that the customer read answers without any migrated row and that the story writes nothing (RD-P1-068; RD-P1-060). The zero-or-one `contact_point_ext` row per `contact_key` and the absent-row defaults of RD-P1-027 are criteria of RWB-P1-DM005-APP (RD-P1-068). The masking rows of AC10 are the interim fake rules; the real rows are Pending, owner data protection officer with the rwb-access owner (NEW-GAP-D1). No legacy criterion and no legacy test text is copied into this story, because the legacy criteria of RWB-DM-002 (AC1 to AC3) and its test cases (TC-DM-002-01 to TC-DM-002-04) are withdrawn with the migration by D-RCV-35 (U1) (GAP-0552; ASM-0788).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The legacy key is withdrawn and this story migrates nothing: no extract, no identifier map, no load and no write; fields whose system of record is an ACE source system are read through the views and never carried | D-RCV-35 (U1); legacy RWB-DM-002 Status Removed; Data Migration Approach; RD-P1-027; RD-P1-068 |
| BR2 | The Workbench reads ACE only through the SELECT-only `recovery.v_ace_*` views, only rwb-source-data reads them, and no constraint in the schema references a `public` table; a link to an ACE record is a `varchar(255)` business key with no foreign key | D-RCV-35 (U4); ADR-010; Architecture v5 slides 7, 8, 9, 11, 12 and 37; FSD P1 BR-P1-001-2 and BR-P1-001-3 |
| BR3 | The clear identity number never leaves ACE: `v_ace_customer` returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`) only | FSD P1 BR-P1-001-6; TSD P1 T3.4 (DF-ACE-073, DF-ACE-074) |
| BR4 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column; it is 1:1 with the ACE record and carries the seven standard record columns | FSD P1 BR-P1-001-5; TSD P1 T3.5 |
| BR5 | `party_ext` is keyed by `person_key` and `contact_point_ext` by `contact_key` (`contact_type:key`); `contact_type` is PHONE, EMAIL or ADDRESS. The `contact_point_ext` cardinality and absent-row defaults are RWB-P1-DM005-APP's (RD-P1-068) | TSD P1 v3 T3.5 and T3.9; FSD P1 A2.1.3.2; RD-P1-027 as amended by RD-P1-068 |
| BR6 | The customer and party facts are data product DP02, system of record "ACE (ingested from SCBPDM)", with `party_ext` and `contact_point_ext` as its Workbench tables | FSD P1 A2.2 (DP02 row); legacy RWB-DM-002 "Data product" row |
| BR7 | No copy of the customer, the contact or the relation data reaches a data lake or a reporting table: the lake is removed and reporting reads events | DP-17; Architecture v5 slides 8 and 9 |
| BR8 | No value a business person may change is written in code: the flags and the consent are data rows, the key joins are read from the dictionary field IDs, and which fields the answer carries is fixed by the published contract and not by a parameter | FSD P1 BR-P1-001; DP-05; RD-P1-060 |
| BR9 | The verification writes no row, adds no migration and no repository, and flag writes are RWB-P1-E1018-APP's | RD-P1-068; RD-P1-021 |

Where each rule lives in the target: BR1 and BR9 are the reason this story exists and need no product code — they need the absence of code, which AC1 and AC7 test. BR2 and BR3 are properties of the views and of the grant, proved here by reading them. BR4, BR5 and BR8 are properties of `rwb_source_data` and of the published read. BR6 is a catalog row owned by the data product story of P1. BR7 is a prohibition: no relay, no export and no lake copy is written for DP02. The consent and contact-quality rows of `contact_point_ext` are written at cutover by RWB-P1-DM005-APP in the same transaction as its interaction rows (RD-P1-021); this story reads them through the contract and writes none.

### 9. State transitions

None. This story moves no case, task or account state and no Flyway version: it adds no migration (RD-P1-068).

DP02 freshness is moved by the batch gate of this service, not by this story: LOADED and STALE are set from `v_ace_batch_status` into `data_product_load` by RWB-P1-E1015-APP, and the customer read only reports it (FSD P1 A2.14; RD-P1-060).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Serves the read (RWB-P1-E1069-APP); this story writes no row of any table |
| RW-CASEOWN, case owner | Reads the customer and party facts of a case they own, masked as answered |
| RW-PHONECOL, collections officer | Reads the same facts for a case in their scope, masked as answered |
| RW-DATASTEW, data steward | Reads the facts and the DP02 freshness for any case; owns the catalog row of DP02, not this story |
| RW-COE, centre of excellence | Reads the facts and the freshness |
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
| DF-EXT-001 to DF-EXT-012 | `party_ext` (schema `rwb_source_data`) | `person_key`, `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` and the seven standard columns | Read through the contract (`partyFacts`); never written by this story |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` (schema `rwb_source_data`) | `contact_key`, `contact_type`, `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` and the seven standard columns | Read through the contract (`consentStatus`, `verifiedAt`); never written by this story |

No ACE row, no view column and no other service's row is copied into `rwb_source_data`: `party_ext` and `contact_point_ext` hold the Workbench's own decision about an ACE record, keyed by `person_key` and `contact_key`, and nothing else (FSD P1 BR-P1-001-5; D-RCV-35 U3). The legacy `party` table (13 fields) and the legacy table of 8 fields named `contact_point` (a name that is not a field or entity in LDM v9 or Data Classification v5) have no target: they are the copy that D-RCV-35 (U1) removes (TSD P1 T3.10). The customer read returns the phone, e-mail and address value from `v_ace_contact` because notices and calls need it, and the display masking of that value is applied per field before the answer leaves the service (FSD P1; TSD P1 T3.4). The field IDs are those in the Logical Data Model and Data Dictionary v11. The read path reads no business parameter and no reference list; the contact types are PHONE, EMAIL and ADDRESS (BR5).

The columns of the answer are the `Customer` schema of rwb-source-data.yaml 5.1.0: the `v_ace_customer` Section A columns in camelCase, with `partyType`, `idType` and `segment` once Section B is live (RD-P1-060; settles GAP-0566).

**Field disposition (RD-P1-027 as amended by RD-P1-068).** The rows of Source to Target Mapping v7, sheet Migration packages, for this story, by Logical Data Model v11 ID. The package holds no CARRY and no KEY row.

| BR Field ID | Entity | Disposition | Rule |
|---|---|---|---|
| DF-EXT-001 to DF-EXT-012 | `party_ext` | EXCLUDE | This story migrates nothing (Data Migration Approach; RD-P1-068): it verifies reads and writes no row |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | EXCLUDE | Carried by RWB-P1-DM005-APP, not by this package |
| DF-ACE-055 to DF-ACE-088 | `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation` | ACE_READ | Read through the views and never carried or stored |

Pending: the approving role of the EXCLUDE rows, owner data owner (as the mapping sheet records it).

### 12. Contract

#### 12.1 REST operations provided

None. `GET /customers/{personKey}` (operationId `getCustomer`) of rwb-source-data on base `/api/recovery/source-data/v1` is published in rwb-source-data.yaml 5.1.0 and built by RWB-P1-E1069-APP (RD-P1-060). This story claims no path, parameter or response field. The contacts are a list per person. Flag writes arrive on `PUT /extension-facts/parties/{personKey}` of RWB-P1-E1018-APP, which owns that operation; this story adds no write operation.

#### 12.2 REST operations consumed

`GET /customers/{personKey}` (rwb-source-data, RWB-P1-E1069-APP), called by the verification with synthetic keys. The authorise call `POST /api/recovery/access/v1/authorise` (P4 rwb-access, contract RWB-P4-E1037-CON) is made by that operation, one hop, 2 s; a timeout answers 503 and returns no field (Template and Rules §R5.5, DP-11 as the service standard).

#### 12.3 Events published

None. A customer read is a synchronous answer; it writes the PII access log and publishes no event and no decision record (RD-P1-072; DP-17).

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. No Temporal workflow and no activity is in this story.

#### 12.6 Schedules

None. No Temporal Schedule and no batch job sits in this story; the freshness schedule of the service belongs to RWB-P1-E1015-APP.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `party_ext` | `rwb_source_data` | P1 | None owned; read through the contract only, never written (RD-P1-068) |
| `contact_point_ext` | `rwb_source_data` | P1 | None owned; read through the contract only, never written (RD-P1-068) |
| `party`, `customer`, `contact_point`, `phone` | — | none | **Do not exist.** The legacy copy of SCBPDM data is removed by D-RCV-35 (U1) and this story creates no such table |
| `v_ace_*` views | `recovery` | ACE view owner, granted by RWB-P1-E1069-DB | Not created, altered or granted here |

No table of another service is read and no foreign key crosses a schema (DP-01). The dictionary tables `sys_objects`, `sys_fields` and `sys_field_version` stay with P1's catalog work, and this story writes no dictionary row.

#### 12.8 Contract fakes

| Fake | Serves | This story |
|---|---|---|
| rwb-source-data contract fake `fakes/rwb-source-data/5.1.0/` | `getCustomer` | The verification runs against it before the service is live (RD-P1-011; RD-P1-060) |
| ACE view fixtures | `v_ace_customer`, `v_ace_contact` | Synthetic rows only: a key with three contacts, a key with no `party_ext` row and a key with no view row (AC2, AC4, AC5, AC8) |
| extension fixtures | `party_ext`, `contact_point_ext` | Synthetic rows only, loaded by the test, never by the service (AC4) |
| authorise fake and FieldMasker fake | The rwb-access contract (RWB-P4-E1037-CON) | A granted and a refused read, a timeout and the unmask rules of AC10 |
| FreshnessQuery stub | The DP02 stamp in use | LOADED, STALE and never stamped, for AC2 |

Every fixture uses synthetic keys; no ACE row and no personal value is copied into a fixture, and the clear identity number appears in no fixture at all.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | `GET /customers/{personKey}` of rwb-source-data |
| Kafka | 0 published, 0 consumed | No topic is added or consumed; DP-09 is not applied |
| Temporal | None | No workflow, activity or schedule |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Test code only, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Customer read verification | Component and contract tests | Calls `getCustomer` with synthetic fixtures and asserts AC2 to AC6 and AC8 to AC10 |
| No-write and package check | Component test | Asserts AC1 and AC7: unchanged schema, history and row counts, grants, constraints and the mapping rows |

**Database and migrations**

- None. No Flyway migration, no table, no column and no view of this story (RD-P1-068).
- `party_ext` and `contact_point_ext` arrive with RWB-P1-E1069-DB; the views and the read arrive with RWB-P1-E1069-APP.

**Configuration and reference data**

- The two key joins are the field IDs of the dictionary: `person_key` (`DF-ACE-056`, `DF-EXT-001`) and `contact_key` (`DF-ACE-076`, `DF-EXT-013`).
- No feature switch and no parameter of this story.

**Build steps**

1. Write the synthetic view, extension, freshness, authorise and masking fixtures.
2. Write the contract tests of AC2 to AC6 against `fakes/rwb-source-data/5.1.0/`.
3. Write the component tests of AC8 to AC10.
4. Write the no-write and package check of AC1 and AC7.
5. Run the same tests against the deployed service once RWB-P1-E1069-APP is live and keep the result as the evidence of this story.

**Rollback.** Nothing is deployed to a running environment beyond test code, so there is nothing to switch off or reverse (RD-P1-045; RD-P1-068).

**Done when.** The tests in section 16 pass against the deployed read; the schema, the Flyway history and the row counts of `rwb_source_data` are unchanged by the story; the package record holds only EXCLUDE and ACE_READ rows; and the 401, 403, 404, 400 and 503 answers are as section 5 states.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | 400: the `personKey` is invalid | Enter {field}. |
| MSG-P4-001 | 401: no session or no Workbench role | As published in the Error and Message Standard |
| MSG-P4-003 | 404: no view row, or outside the caller's scope | As published in the Error and Message Standard |
| MSG-GEN-006 | 503: a view read fails or times out, or authorise does not answer | As published in the Error and Message Standard |
| MSG-P4-002 | The caller holds no right for the read | You cannot {action} here. Your role does not include it. |

The answers are those of the published operation (RD-P1-004; RD-P1-060) and the texts are those of the Error and Message Standard. For MSG-P4-002, {action} names the action the caller tried — for example "read the customer of this case" — and never a case fact and never a field value. No message of this story carries a name, an identity number, a phone number, an e-mail, an address or a `person_key`. A STALE or never-stamped DP02 raises no message on this read (RD-P1-060; RD-P1-062).

Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as NEW-GAP-W3M-003 (Error Handling and Resilience Standard v5 section 8.4). A REST read that times out answers 503 MSG-GEN-006; the authorise call is a POST and is not retried automatically.

### 15. Screens and states

No screen is built by this story. The customer and party facts are shown on the case screen of the recovery workspace, which reaches this service through the gateway-bff composite route (DP-19), one hop; the screen and its field-level rendering belong to the screen owner. The states an operator sees are the DP02 freshness (current or stale, shown by the caller) and the 404 answer of a key with no view row (AC5).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-002-01 | AC1, AC2, AC3, AC4 | Component | Synthetic `person_key` "P0000123" present in the view fixtures with one `party_ext` row and one `contact_point_ext` row; the unchanged-schema assertion of AC1 |
| TC-DM-002-04 | AC6 | Component | A caller with no Case record R right, against the authorise fake; 403 MSG-P4-002 and no view read |
| TC-DM-002-05 | AC5 | Component | Synthetic person_key "P0099881" with no row in the customer view fixture; 404 MSG-P4-003, nothing written and no default customer |
| TC-DM-002-06 | AC1, AC4 | Component | Boundary of AC1 and AC4: no object, history row or data row is added; flags answer from the extension rows |
| TC-DM-002-07 | BR1 | Component | Assertion that no extract, identifier map, load, reconciliation or cutover for customer and party data exists in the service |
| TC-DM-002-08 | BR2 | Component | Assertion that the service reads only the recovery.v_ace_* views and that a link to an ACE record is a varchar(255) business key with no foreign key |
| TC-DM-002-09 | BR3 | Component | Assertion that v_ace_customer answers id_no_masked and id_no_last4 only and that no clear identity number reaches the answer |
| TC-DM-002-10 | BR4 | Component | Assertion that party_ext and contact_point_ext hold no ACE column copy and carry the seven standard record columns |
| TC-DM-002-11 | BR5 | Component | Assertion that party_ext is keyed by person_key, contact_point_ext by contact_key, and contact_type is PHONE, EMAIL or ADDRESS |
| TC-DM-002-12 | BR6 | Component | Assertion that the DP02 catalog row names ACE as system of record with party_ext and contact_point_ext as Workbench tables |
| TC-DM-002-13 | BR7 | Component | Assertion that no customer, contact or relation data is written to a data lake or a reporting table |
| TC-DM-002-14 | BR8, BR9 | Component | Assertion that the flags and consent are read from data rows, key joins use dictionary field IDs and the story writes no row |
| TC-DM-002-15 | AC7 | Component | The package rows of Source to Target Mapping v7 and the grant and constraint checks of AC7 |
| TC-P1-DM002-APP-01 | AC2 | Component | LOADED, STALE and never-stamped DP02 stubs; 200 in all three |
| TC-P1-DM002-APP-02 | AC4 | Component | One person with a `party_ext` row and one without |
| TC-P1-DM002-APP-03 | AC8 | Component | Three contact types with one extension row |
| TC-P1-DM002-APP-04 | AC9 | Component and contract | View statement timeout and authorise timeout |
| TC-P1-DM002-APP-05 | AC10 | Component and contract | FieldMasker fake: user session and the two workload identities |

The legacy test text of both cases is withdrawn with the migration by D-RCV-35 (U1), together with `TC-DM-002-02` and `TC-DM-002-03`, which no story carries. The IDs TC-DM-002-01 and TC-DM-002-04 are kept so that the withdrawn case and its replacement can be followed under the same identifier, and each replacement is recorded under that ID in Recovery Workbench Test Cases v9.xlsx, tab Story test cases; the rows of that tab still describe the criteria before batch D and are to be updated (see section 20). The legacy levels are kept at Component for both, because each test exercises one service's component against fixtures and fakes and no cross-service path.

### 17. Guardrails

- No business value in code: the flags and the consent are data rows read through the contract; no column name, field-ID range or flag default is written in Java as a business value (BR8).
- No personal data in events, logs, workflow inputs, tests or prompts: the answer carries the masked identity and the view values only, every fixture is synthetic, and the clear identity number appears in no fixture, no log line and no event of this story (BR3).
- ACE data only through the owner's contract or `v_ace_*` views, and here only through the views: a class that names a `public` table fails the boundary rule of the service, and no statement of this story names another service's schema (DP-01; DP-05; ADR-010).
- This story writes nothing: no row, no copy of a customer, a phone, an e-mail or an address, no flag and no consent (BR4; BR9).
- One hop and 2 s on the authorise and masking path; a slow answer refuses the read and returns nothing (DP-11 as the service standard).
- No lake copy and no reporting copy of DP02 is written here (BR7; DP-17).
- No migration in this story; an applied version of the service sequence is never edited (DP-15; RD-P1-068).

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
| Withdrawn IDs | AC1 to AC3; TC-DM-002-01 to TC-DM-002-04 |
| Replacement test IDs | TC-DM-002-01, TC-DM-002-04 (new text, same IDs) |

| Story | Work type | Relation to this story |
|---|---|---|
| None | — | Build, integration and external dependencies are empty for this story |
| RWB-P1-E1069-APP, RWB-P1-E1069-DB | App development, ACE DB | E1069-APP builds `GET /customers/{personKey}` (RD-P1-060); E1069-DB delivers the views, grants and extension tables; needed for the live run, not build edges (GAP-0556; ASM-0792) |
| RWB-P1-E1015-APP | App development | Stamps the DP02 freshness the customer answer carries |
| RWB-P4-E1037-CON, RWB-P1-E1015-CON | Contract | Contract dependencies: authorise and the freshness answer |
| RWB-P1-E1018-APP | App development | Owns the flag-write operation on `party_ext` (RD-P1-068) |
| RWB-P1-DM005-APP | App development | Writes the `contact_point_ext` rows at cutover and holds the cardinality and absent-row criteria (RD-P1-068) |

The legacy key carried no requirement ID, so this story adds none and its fragment's requirement list is empty. Its business rules come from D-RCV-35 (U1, U3, U4), ADR-010, the FSD and TSD P1 v3 rules named in section 8, and the DP-05, DP-15 and DP-17 rows of the pattern table.

### 19. Out of scope

- The legacy extract, the identifier map, the load, the reconciliation and the cutover of RWB-DM-002: withdrawn by D-RCV-35 (U1), with AC1 to AC3 and TC-DM-002-01 to TC-DM-002-04.
- The 30 `recovery.v_ace_*` views, their SQL, their grants and the per-service login: RWB-P1-E1069-APP and RWB-P1-E1069-DB; the end-to-end grant proof across the 19 logins: RWB-ITG-E1069-ITG.
- The `GET /customers/{personKey}` operation, its path, parameters and response schema: built by RWB-P1-E1069-APP (RD-P1-060); this story only verifies it.
- The masking policy rows, the roster of roles that see a field unmasked, the identity rules and the authorise decision itself: rwb-access (P4), RWB-P4-E1069-APP and RWB-P4-E1037-APP.
- Freshness and readiness: the `data_product_load` stamp, `AceDataReady`, `AceDataLate` and the batch gate are RWB-P1-E1015-APP's; the readiness operations are RWB-P1-E1013-APP's (FSD P1 A2.14).
- DP01, the account and arrears read path and the reconciliation to `v_ace_account`: RWB-P1-DM001-APP and RWB-P1-E1011-APP.
- Writing `party_ext` flags (RWB-P1-E1018-APP) and `contact_point_ext` rows (RWB-P1-DM005-APP); the `relations[]` answer of `GET /accounts/{accountKey}` (RWB-P1-E1069-APP).
- The data lake and any reporting or analytic copy of DP02: removed (DP-17; Architecture v5 slides 8 and 9).
- Every screen, including the case screen that shows these facts: gateway-bff and the screen owners (DP-19); this story returns data and draws no screen.
- The catalog rows of DP02, the data dictionary rows of the views and the extension tables, and the baseline-measure set: the catalog, dictionary and baseline work of P1.

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Add the masking rule rows that unmask `firstName`, `lastName` and `contactValue` for the two workload identities (data protection officer with the rwb-access owner; NEW-GAP-D1).
- Provide the synthetic view, authorise and freshness fixtures in DEV (squad).
- Update the DM002 rows of Test Cases v9 and the traceability matrix to the verification criteria of section 7 (QA).
