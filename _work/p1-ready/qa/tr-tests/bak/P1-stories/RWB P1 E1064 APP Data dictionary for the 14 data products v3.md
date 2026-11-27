# RWB-P1-E1064-APP Data dictionary for the 14 data products

**Version 3 changes.**
- Dictionary baseline is checked as at least 123 objects and 1,379 fields with every baseline name and field ID present (RD-P1-025).
- Load approval and state stay in rwb-case; this service applies an approved version atomically (RD-P1-020 G). The rwb-access dictionary gate deadlock for new fields is open (NEW-GAP-F09-5, blocker).
- Idempotency-Key on the publish POST only, `ETag` / `If-Match` on both PATCH operations, shared Problem body, `WORKBENCH` wire value, `SUPERSEDED` status, contract rows addressed by UUID (RD-P1-001, 004, 005, 006).
- AC rewrites and AC13 to AC22 from the review; rwb-case list path, authority table, validation limits and per-operation status codes corrected.
- Review findings fixed: 1 to 4, 7, 9 to 12, 17, 18, 21, 23 to 30. Left pending with an owner: 5, 6, 8, 13 to 16, 19, 20, 22.
- Batch D: the new-field gate deadlock is settled (RD-P1-071). The dictionary load validates its own rows and is applied before loads that name its new fields; this supersedes the open item of the second bullet (NEW-GAP-F09-5 closed).

**Version and date.** v3, 27 November 2026.

**Change log.** D-RCV-60, 27 November 2026: applied RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-020, RD-P1-025 and RD-P1-045, and corrected the cited review findings. Agent: S6-stories.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1064-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-064 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1064-APP-16) |
| Contract version | 5.1.0 (Recovery Workbench API Specification v7, rwb-source-data.yaml, base `/api/recovery/source-data/v1`) |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP and the contract baseline RWB-P1-E1064-CON |
| Depends on (build) | RWB-P1-E1064-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-004, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-026, FR-P1-027, FR-P1-029) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-020, RD-P1-025, RD-P1-045, RD-P1-071 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-064 for rwb-source-data. The 122 objects and 1,366 fields of that date (superseded: at least 123 objects and 1,379 fields, RD-P1-025), the nine business rules and the eight acceptance criteria stay as written; what changes is where the dictionary is served from and how its rows arrive. The five admin operations move onto the service's own base `/api/recovery/source-data/v1` (DP-13); the two published interfaces `DataDictionaryLoader` and `DataDictionaryQuery` become a REST read and a reference-table handler instead of a jar every caller imports (DP-11); the five tables stay P1's in `rwb_source_data` and no DDL is added (DP-01, DP-15, with the baseline from RWB-P1-E1001-APP); the governance and dictionary load arrives through the rwb-case reference-data contract and not through a monolith reference-load endpoint (DP-07); the 30 `recovery.v_ace_*` views stay in schema `recovery` and are reached by this service's own contract (DP-05); screens read the dictionary through gateway-bff (DP-19). The contract baseline is RWB-P1-E1064-CON, the deployment is RWB-P1-E1064-OPS. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E1064-APP-L266, X20 RWB-P1-E1064-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every object and field of the 14 data products (at least the baseline 123 objects and 1,379 fields) typed, sourced and owned, including the 30 ACE views and the four extension tables, with a data contract for the ACE read path that the ACE team confirms**, so that **every read has one published definition and a change to an ACE column reaches the dictionary through one governed load**.

This is the application slice of legacy RWB-E1-064 and it keeps all eight legacy acceptance criteria in scope, rewritten against the target service contracts. It delivers:

- the five admin operations on base `/api/recovery/source-data/v1` (DP-13): `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish` (section 12.1);
- `DataDictionaryService`: the paged read of `sys_objects`, `sys_fields` and `data_product` behind the field read, its four filters and its counts, and the versioned field change with a mandatory reason and an optimistic lock;
- `DataContractService`: the ACE read contract DC-ACE over the 304 ACE fields, the confirmation record, the publish rule, and the new DRAFT version a field change opens on a published contract;
- `DictionaryLoadHandler`, the reference-table handler for table code `sys_fields` that the rwb-case reference-data contract invokes, with the whole-load validation and the refusal in full of the legacy loader (DP-07);
- the read half of AC3, which resolves `days_past_due` from `sys_fields` and takes its value from `recovery.v_ace_account` through the read path of RWB-P1-E1069-APP (DP-05).

It does not create the five tables, the seed or the read model `v_data_dictionary`: they are the as-built baseline of RWB-P1-E1001-APP, and this story writes rows only. It creates none of the 30 `recovery.v_ace_*` views; they are RWB-P1-E1069-APP's, with their grants and the boundary rule in RWB-P1-E1069-DB. It publishes no OpenAPI document, no fake and no error envelope of its own: that is RWB-P1-E1064-CON, which this story builds against from Day 1. It deploys nothing: the chart, the flag values, the dashboards and the runbook are RWB-P1-E1064-OPS.

### 2. Business rationale

The dictionary is the only place that says what a field is, where it comes from and who owns it. Its E1001 baseline is at least 123 objects and 1,379 fields, and later stories add rows only by governed loads: the 89 Workbench tables of that baseline hold 1,026 fields, 49 of them on the four extension tables, and the 30 `recovery.v_ace_*` views hold 304 fields, 177 in Section A and 127 in Section B. The Workbench loads no source data (D-RCV-35 U1), so every source is either ACE, whose columns are recorded as `public.table.column` on the view fields where the view reads one column, or the Workbench itself.

V0001 creates `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` and seeds at least the 123 objects and 1,379 fields of the baseline. This story does not create a table or a column. It publishes the governance attributes on every field, records the change history, and takes the ACE team's confirmation of the read contract before it is published. A new ACE column is added to the dictionary by a governed load submitted through the reference-data contract of rwb-case, never by editing an applied migration; the view conformance test of RWB-P1-E1069-APP blocks the merge until the row exists. Serves REQ-RDF-001 (one system of record and one owner per product) and REQ-RDF-011 (catalog entry content). The measure is that all 1,379 baseline fields have a source, owner, refresh cycle and late behavior.

**What D-RCV-60 changes.** Not the content and not the rules. Three things move. The five admin operations are served by rwb-source-data under its own base, so a caller reaches the dictionary in one hop from the gateway and not through a monolith path (DP-11, DP-13; Architecture v5 slides 11, 15 and 41). The two published Java interfaces are no longer a jar that every module imports: `DataDictionaryQuery` becomes the REST read and `DataDictionaryLoader` becomes the reference-table handler the rwb-case reference-data contract calls, which is the same decoupling the pattern table prescribes for a published interface (DP-11, DP-07). And the load itself is submitted through the reference-data contract of rwb-case, because parameters and reference data are P3's under the default ruling, while the rows land in P1's tables (DP-01, DP-07; Template and Rules §R3).

**Why the dictionary stays with P1.** It is the one place where a field, a number or a source column is resolved to a data product and an owner (REQ-RDF-001, REQ-RDF-011). Split across 19 schemas it would answer 19 ways, and every other service reading it would be a cross-schema read the boundary rule forbids (DP-01; Architecture v5 slide 29). Held in `rwb_source_data` it stays one dictionary, reachable by contract, with no second copy.

**Why the views stay where they are.** The 30 `recovery.v_ace_*` views read ACE's own tables, so they stay in schema `recovery`, owned by `ace_view_owner` and reached only by the `rwb_source_data` login (DP-05, ADR-010; Architecture v5 slides 11 and 29). The dictionary describes them; it does not own them, and this story never creates or alters one.

### 3. Preconditions

- RWB-P1-E1001-APP is done: the service baseline created P1's tables in `rwb_source_data`, including the five tables of this story, at least 123 `sys_objects` rows and 1,379 `sys_fields` rows with every baseline object name and field ID, and the read model `v_data_dictionary` (legacy RWB-E1-064 §3, RWB-E1-001 in the target; DP-01, DP-15).
- RWB-P1-E1069-APP is done: the 30 `recovery.v_ace_*` views exist in schema `recovery`, and the view conformance test CHK-01 compares every view column with `sys_fields` (DP-05).
- RWB-PLT-E1044-CON is in place: the per-service Flyway sequence of rwb-source-data exists with its own history table in `rwb_source_data`, and the baseline version has been applied on it (DP-15).
- RWB-P1-E1064-CON is baselined: the OpenAPI 3.1 document of the five operations, the five schemas, the one error envelope and the message mapping are published with their fakes, so this story builds against a fixed contract from Day 1 (DP-11).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published with their client library: the reference-data contract of rwb-case accepts a validated load for a table code and calls the reference-table handler the owning service provides for it (DP-07).
- RWB-PLT-N001-CON is in place: the gateway-bff composite route that the dictionary and contract screens will use exists before the screens do (DP-19).
- The data steward holds RW-DATASTEW (Reference data U); the reference data administrator holds RW-REFADM (Reference data C).
- The ACE team lead is recorded as the confirming role for the ACE read contract; the confirmation is stored outside the Workbench and referenced by its document identifier (legacy RWB-E1-064 §3).
- `v_data_dictionary` in `rwb_source_data` returns every baseline object and field (at least 123 objects and 1,379 fields).
- The rwb-case list read is `GET /api/recovery/case/v1/admin/lists/{listCode}`; the lists used are LOV-ROLE and LOV-REFRESH (DAILY, WEEKLY, MONTHLY, ON_CHANGE).
- Pending: the column the field read takes `refreshCycle` from (`sys_fields.refresh_cycle` written by the load and PATCH, or the `data_product.refresh_cycle` that `v_data_dictionary` selects), owner data architect, tracked as NEW-GAP-S6-4. AC3 and AC4 read the field value once this is settled.
- The unknown-field check (MSG-P1-005) applies to rule versions, mappings and access loads, not to a dictionary load, which is how a field becomes known; when one release brings both, the dictionary load is applied first (RD-P1-071).

### 4. Flow

1. Data steward: prepares the governance load for every field in `v_data_dictionary` (at least the 1,379 baseline fields) with owner role, refresh cycle, late behavior and interface, and checks the source system and source field of each view field against the view definition (legacy RWB-E1-064 §4 step 1).
2. Reference data administrator: submits the file through the reference-data contract of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads`, P3, DP-07) with table code `sys_fields` and valid from 2026-11-30; the file reaches this service as a call into its reference-table handler, not as an endpoint of this service.
3. `DictionaryLoadHandler`: validates the load's own rows and refuses the whole load if a field code repeats, if a row's entity is not in `sys_objects`, if a type is not valid, if a view field's source system is not "ACE", if a Workbench field's source system is not "Workbench" (stored value; the wire value is `WORKBENCH`), if a view field's source field is not a column of that view and is not one of the 7 derived fields, or if any required attribute is empty. It applies a P3-approved version atomically in one transaction: version 1 for a new field, version n+1 for a changed field, and no new version row for unchanged values. P3 owns approval state, approver and rollback in `rwb_case.reference_version`; P1 records only the applied field version on its rows and creates no load-state record, and a re-delivered version is a no-op (RD-P1-020 G). The load applies no unknown-field check to the field codes it introduces (RD-P1-071).
4. Data steward: records the ACE team lead's confirmation of contract DC-ACE, which covers the 304 ACE view fields read through V0002 and V0003, with the confirming role, the date and the stored document reference, through `PATCH /admin/data-contracts/{contractId}` and an `If-Match` version.
5. Data steward: publishes DC-ACE with `POST /admin/data-contracts/{contractId}/publish` and an `Idempotency-Key`; the service refuses a contract without a confirmation (legacy RWB-E1-064 §4 step 5).
6. `DataContractService`: sets the contract PUBLISHED. The prior PUBLISHED version remains in force while the new DRAFT has no confirmation; it becomes SUPERSEDED only when the new version is confirmed and published.
7. Developer or analyst: calls `GET /admin/data-dictionary/fields` and reads a field's type, source system, source field, refresh, owner and behavior when late; the response is a `DataDictionaryFieldPage` with the page, the size and the total. Its query parameters are `product`, `entity`, `field`, `sourceSystem`, `page` and `size`, and its answer field names are those of section 12.1, as the API specification gives them. The answer carries the flag `isPersonal` and no marker vocabulary (GAP-0890, GAP-2306).
8. Data steward: changes a field definition with `PATCH /admin/data-dictionary/fields/{fieldCode}`, a reason and an `If-Match` version; the service writes a new `sys_field_version` row with its date and reason (legacy RWB-E1-064 §4 step 8).
9. `DataContractService`: when a changed field belongs to the published DC-ACE, opens a new DRAFT contract version; the published version stays in force.
10. ACE team and recovery developer: a new ACE column is added to a view by a Flyway migration on RWB-P1-E1069-APP's sequence and to the dictionary by a load through the rwb-case reference-data contract; no applied migration is edited, and CHK-01 passes only when both exist (legacy RWB-E1-064 §4 step 10; DP-15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Publish of a contract without the ACE team's confirmation | 409; contract stays DRAFT | MSG-P1-021 | AC6 |
| X2 | A field change without a reason | 422; no version written | MSG-GEN-001 | AC5 |
| X3 | A dictionary load with a repeated field code, an entity not in `sys_objects`, an invalid type, a missing attribute, a source system outside ACE and Workbench, or an ACE source field that is not a column of the view and not one of the 7 derived fields | Load refused in full; the dictionary in force stays | MSG-P1-002 | AC4, AC18 |
| X4 | Two stewards change the same field from the same version | The second change is refused with 409 | MSG-GEN-004 | AC7 |
| X5 | A field of a published contract changes | A new DRAFT contract version; the published version stays in force | None | AC8 |
| X6 | A view column exists with no `sys_fields` row | CHK-01 of RWB-P1-E1069-APP fails and the merge is blocked | v_ace_account.legacy_bucket has no data dictionary entry | AC22 |
| X7 | A field definition is changed with no If-Match version | 428; no version written | MSG-GEN-004 | AC7 |
| X8 | The rwb-case list read does not answer inside 2 s, or answers non-2xx, while the handler validates a load | The handler answers 503 and writes nothing; the dictionary in force stays and no answer is guessed from a stale cache | MSG-GEN-006 | AC12 |

X1 to X7 are the exception paths of RWB-E1-064 carried onto the split; X8 is the one path the reference-data contract of rwb-case adds (DP-07, DP-11; one hop, 2 s timeout). A dictionary row of another service's table is no longer a path of this story: the 74 tables of the other services carry their own dictionary rows in their owners' schemas (RWB-PLT-NF06-DB; DP-01).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contract baseline RWB-P1-E1064-CON and the rwb-case reference-data contract from Day 1; needs the baseline tables of RWB-P1-E1001-APP and the views of RWB-P1-E1069-APP; it publishes the definition every later read uses |
| Negotiable | Owners, refresh cycles, late behavior and contract content are data values; the story fixes the completeness, source and version rules |
| Valuable | Every read has one published definition, and a source change is governed in one place |
| Estimable | No DDL, five operations, two services, one reference-table handler, one contract service |
| Small | Finished inside two weeks with its tests, once the contract baseline is baselined |
| Testable | Each criterion is one API test against the seeded metadata tables and the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Data dictionary for the 14 data products

  Background:
    Given the dictionary holds every object and field of the E1001 baseline: at least 123 objects and 1,379 fields
    Given the governance load of owner role, refresh cycle and late behavior was published on 2026-11-30
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "ACE (ingested from ALS)"
    Given contract "DC-ACE" for source system "ACE" is "DRAFT" at version 1 with 304 mapped view fields, read through V0002 and V0003
    Given the fixture row of "DC-ACE" version 1 has contract id "00000000-0000-4000-8000-000000000064" and an empty interfaceIds list

  Scenario: AC1 Every field is defined (legacy RWB-E1-064 AC1)
    Given the 14 data products
    When a developer calls GET /admin/data-dictionary/fields?size=1
    Then the response is 200 with one item and total at least 1,379
    Then a query on `v_data_dictionary` returns at least 123 distinct entities and every E1001 baseline object name and field ID
    Then of the baseline objects 93 are tables and 30 are v_ace_* views
    Then the 89 baseline Workbench tables hold 1,026 baseline fields and the four extension tables hold 49 fields
    Then the 30 `v_ace_*` views hold 304 fields, 177 from Section A and 127 from Section B
    Then every field has a data type, a physical type, a description, a source system, an owner role, a refresh cycle and a behavior when late
    Then 297 of the 304 view fields name an ACE column in the form `public.table.column`
    Then the 7 derived view fields `v_ace_contact.contact_type`, `city`, `post_code`, `country`, and `v_ace_plan.installments`, `recommended_installment`, `recommended_package` carry source system ACE and no single ACE column

  Scenario: AC2 Every ACE view has dictionary rows (legacy RWB-E1-064 AC2)
    Given the RWB-P1-E1001-APP baseline and V0002/V0003 are applied in SIT
    When a developer counts v_data_dictionary by source system
    Then 30 objects named v_ace_* are returned with 304 fields
    Then each v_ace_* view has one sys_objects row and one sys_fields row per column
    Then no v_ace_* view has a column without a row and no row without a column
    Then the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext hold 49 fields, DF-EXT-001 to DF-EXT-049

  Scenario: AC3 The arrears field comes from the ACE delay days (legacy RWB-E1-064 AC3)
    Given V0001 and V0002 are applied in SIT
    Given one ACE account "ACC0000017" has delay_days 95
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER" and physical type "integer"
    Then the row holds source system "ACE" and source field "public.account.delay_days"
    Then the row holds data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and late behavior "Keep the previous value and mark DP01 stale"
    Then select days_past_due from recovery.v_ace_account for "ACC0000017" returns 95

  Scenario: AC4 An approved new ACE field is applied through the P3 handler (legacy RWB-E1-064 AC4)
    Given a dictionary fixture in which v_ace_collateral_detail holds 11 fields and no row for "insurance_expiry"
    Given RWB-ACE-001 adds public.collateral_detail.insurance_expiry and V0003 exposes it as v_ace_collateral_detail.insurance_expiry
    When the P3-approved reference load for table code `sys_fields` reaches the handler with field "DF-ACE-204", source system "ACE", source field "public.collateral_detail.insurance_expiry", owner RW-DATASTEW, refresh "WEEKLY" and late behavior "Keep the previous value and mark DP06 stale"
    Then the handler applies the approved version atomically and writes DF-ACE-204 with field version 1 because it is new; a changed existing field receives version n+1 and an unchanged field receives no new version row
    Then GET /admin/data-dictionary/fields?entity=v_ace_collateral_detail&field=insurance_expiry returns the row
    Then CHK-01 passes on the next pipeline run and no Flyway migration file was edited
    And no unknown-field check refuses the new field code, and this load is applied before any load of the release that names DF-ACE-204
    When the same approved version names source field "public.collateral_detail.insurance_date"
    Then the handler refuses the whole version with MSG-P1-002 and no P1 row is changed
    And the check code and the {source}, {date} and {check} values of the message are Pending (NEW-GAP-S6-5)

  Scenario: AC5 A change keeps its history (legacy RWB-E1-064 AC5)
    Given field "DF-ACE-018" is at version 1 with late behavior "Keep the previous value and mark DP01 stale"
    When the data steward changes its late behavior to "Keep the previous value, mark DP01 stale and alert the data steward daily" with reason "add the daily stale alert for DP01" on 2026-11-18
    Then field "DF-ACE-018" is at version 2 dated 2026-11-18 with that reason (time zone of the date Pending, NEW-GAP-S6-4)
    Then version 1 stays readable with its own date and late behavior
    When the data steward sends a further change with an empty reason
    Then the system refuses the call with status 422 and MSG-GEN-001 for field "reason"
    Then field "DF-ACE-018" stays at version 2

  Scenario: AC6 The ACE read path is agreed before it is published (legacy RWB-E1-064 AC6)
    Given the fixture contains DC-ACE confirmed by role "ACE team lead" on 2026-11-12 with document UUID "00000000-0000-4000-8000-000000006400"
    And the fixture contains DC-ACE-2 without confirmation
    When the data steward publishes "DC-ACE"
    Then the contract status is "PUBLISHED" with version 1 and the confirmation on 2026-11-12
    Then the response has fieldCount 304 and interfaceIds [] and the row holds published_at and published_by
    When the data steward publishes DC-ACE-2
    Then the response is 409 Problem with messageCode MSG-P1-021 for system "ACE"

  Scenario: AC7 Two changes to the same field at once (legacy RWB-E1-064 AC7)
    Given two data stewards read field "DF-ACE-020" at version 1
    When both send a change with version 1
    Then the system saves the first change as version 2
    Then the system refuses the second with status 409 and MSG-GEN-004
    Then the first answer carries ETag "2"
    When a third steward sends a change with no If-Match version
    Then the system refuses it with status 428 and MSG-GEN-004

  Scenario: AC8 A change to a field in a published contract (legacy RWB-E1-064 AC8)
    Given contract "DC-ACE" is "PUBLISHED" at version 1
    When field "DF-ACE-018" changes to version 2
    Then the system creates one version 2 as DRAFT with no inherited confirmation
    Then version 1 stays PUBLISHED until version 2 is confirmed and published, when version 1 becomes SUPERSEDED
    And a second field change while version 2 is DRAFT creates no version 3

  Scenario: AC9 This story adds no table, column, index or constraint (new, D-RCV-60)
    Given the baseline of RWB-P1-E1001-APP is applied
    When the database changes owned by this story are reviewed
    Then this story publishes no dictionary migration and adds no table, column, index or constraint to rwb_source_data
    Then rows are written only through the approved reference load and the five admin operations

  Scenario: AC10 An admin operation answers an unauthenticated, unauthorised or unknown call with 401, 403 or 404 (new, D-RCV-60)
    Given no session
    When GET /admin/data-contracts is called
    Then the response is 401 Problem with messageCode MSG-P4-001
    Given a caller with role RW-TRIBE
    When the caller sends PATCH /admin/data-dictionary/fields/DF-ACE-018 with If-Match "1"
    Then the response is 403 Problem with messageCode MSG-P4-002 and no row changes
    Given a caller with role RW-DATASTEW
    When the caller sends the same PATCH to /admin/data-dictionary/fields/DF-ACE-999, which does not exist
    Then the response is 404 Problem with messageCode MSG-P4-003 and no row changes

  Scenario: AC11 Only the publish POST uses idempotency (new, RD-P1-001)
    Given publish was sent with a canonical lowercase UUID Idempotency-Key
    When the same POST is repeated with the same key, path and body inside 24 hours
    Then the helper replays the stored status, headers and body and no second effect occurs
    When the key is reused with a different path or body, or while in flight
    Then the answer is 409 Problem with MSG-PLT-N009-05
    When the key is missing or is not a UUID
    Then the answer is 400 Problem with MSG-PLT-N009-03
    When the idempotency store is unavailable
    Then the answer is 503 Problem with MSG-PLT-N009-06
    And GET and PATCH operations do not use Idempotency-Key

  Scenario: AC12 A consumed call that fails or does not answer leaves the dictionary unchanged (new, D-RCV-60)
    Given the rwb-case list read used by the handler times out after 2 s or returns non-2xx
    When the approved load is validated
    Then the handler returns 503 Problem with messageCode MSG-GEN-006 naming rwb-case
    And no row of sys_fields, sys_field_version or data_contract changes

  Scenario: AC13 A role without the update right cannot confirm or publish (new, review finding 23)
    Given a caller with role RW-TRIBE and a DC-ACE contract in DRAFT
    When the caller sends the confirmation PATCH or publish POST
    Then each answer is 403 Problem with MSG-P4-002
    And the contract and its confirmation remain unchanged

  Scenario: AC14 Reason boundaries (new, review finding 13)
    Given field DF-ACE-018 is at version 1
    When the steward sends a change with a 400-character reason
    Then it is accepted and version 2 is written with the reason
    When the steward sends a change with a 401-character reason or a reason containing only spaces
    Then the first is refused with 422 MSG-GEN-002 (change_reason holds 400 characters) and the second with 422 MSG-GEN-001
    And no additional version is written

  Scenario: AC15 The personal flag cannot be cleared without an agreed approval rule (new, review finding 8)
    Given a field whose isPersonal is true in the synthetic fixture
    When a data steward sends isPersonal=false by PATCH
    Then the flag remains true
    And the response status, message code and the approval rule for a change of the flag are Pending, owner Compliance and PDPA officer (NEW-GAP-S6-3)

  Scenario: AC16 A published contract is not edited in place (new, review finding 24)
    Given DC-ACE is PUBLISHED at version 1
    When its confirmation is changed or it is published again with a new Idempotency-Key
    Then the response is 409 Problem and version 1 remains unchanged
    And the messageCode of the refusal is Pending, owner data architect with product owner (NEW-GAP-S6-2)

  Scenario: AC17 A second field change does not open another draft (new, review finding 24)
    Given a field change has opened DC-ACE version 2 as DRAFT with no confirmation
    When another field of DC-ACE changes
    Then no version 3 is created and version 1 remains PUBLISHED

  Scenario: AC18 A bad or repeated governed load does not partially write (new, review finding 18)
    Given a load for sys_fields has an invalid row, duplicate field row or no rows
    When DictionaryLoadHandler validates the load
    Then the whole load is refused at its first failing check and no row or version is written
    When an already applied load version is delivered again
    Then it creates no additional sys_field_version row
    And the handler treats the re-delivered version as a no-op, idempotent on table code and version (RD-P1-020 G)

  Scenario: AC19 A required dependency failure makes no write (new, review finding 18)
    Given the database or the rwb-access authorise call is unavailable
    When any of the five admin operations is called
    Then the response is 503 Problem with MSG-GEN-006
    And no dictionary or contract row is changed

  Scenario: AC20 An admin action is audited without a personal value (new, review finding 19)
    Given a field change, confirmation, publish and refused call
    When each action completes
    Then the audit record identifies the actor role, action, object and time
    And which platform record carries each of the four actions is Pending, owner solution architect (NEW-GAP-S6-7)
    And no field value, confirmation document value or personal data is recorded

  Scenario: AC21 Paging and filters return the documented result (new, review finding 18)
    Given the baseline
    When the field read requests a size above the maximum page size
    Then it returns 422 Problem with MSG-GEN-002 and no items
    When a field filter matches no field
    Then it returns 200 with total 0 and an empty items array
    And the maximum and default page size, the page base, the sort order and the filter match rule are Pending, owner solution architect (NEW-GAP-S6-1)

  Scenario: AC22 CHK-01 blocks a view column without a dictionary row (new, review finding 28; owned by RWB-P1-E1069-APP AC5)
    Given recovery.v_ace_account has column legacy_bucket with no sys_fields row
    When RWB-P1-E1069-APP runs CHK-01
    Then the check fails with "v_ace_account.legacy_bucket has no data dictionary entry"
    And the check is owned and maintained by RWB-P1-E1069-APP
```

**Target reading.** The criteria above are read against rwb-source-data.yaml 5.1.0 and the decision register. A contract confirmation PATCH and a field PATCH use `If-Match`; only the publish POST uses `Idempotency-Key`. A governed load is approved and versioned by rwb-case, while this service applies it atomically through its `sys_fields` handler. `DC-ACE` and `DC-ACE-2` are contract codes; the path parameter `{contractId}` is the UUID of one version row, found with `GET /admin/data-contracts` filtered by `sourceSystem` and `status`. `{fieldCode}` is the field ID, for example `DF-ACE-018`.

- **The five admin operations.** They are served by rwb-source-data on base `/api/recovery/source-data/v1` (DP-13; Architecture v5 slides 15 and 41), so `GET /admin/data-dictionary/fields` of AC1 and AC4, `POST /admin/data-contracts/{contractId}/publish` of AC6 and the field and contract writes of AC5, AC7 and AC8 are called with that base and with the contract of RWB-P1-E1064-CON. The paths, the query parameters and the returned field names are those of the API specification, which is why the path parameter is `{fieldCode}` in the contract and the response is a page with `page`, `size` and `total` rather than a pair of counts.
- **The two published interfaces.** `DataDictionaryQuery` and `DataDictionaryLoader` are no longer a jar that another module imports: the queries it answered are the field read and its four filters, and the load it applied is the reference-table handler the rwb-case reference-data contract calls (DP-11, DP-07). No AC text changes, because none of the legacy lines named the interface — they named the outcome.
- **The five tables.** `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` stay P1's, in schema `rwb_source_data`, created by the baseline of RWB-P1-E1001-APP; this story writes rows and adds no DDL (DP-01, DP-15; Template and Rules §R6, RWB-E1-001 "Must change").
- **The reference load.** The load of AC4 is submitted through the reference-data contract of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads`, DP-07) and reaches this service as a call into the handler for table code `sys_fields`; the legacy `POST /admin/reference-loads` of this service does not exist. The handler signature and its request and result schemas are Pending (NEW-GAP-S6-5).
- **The 30 views.** They stay in schema `recovery`, owned by `ace_view_owner` and read only by the `rwb_source_data` login (DP-05, ADR-010; Architecture v5 slides 11 and 29), so the value assertion of AC3 runs against `recovery.v_ace_account` through the read path RWB-P1-E1069-APP ships, and the row assertions of AC1, AC2 and AC3 run against the dictionary in `rwb_source_data`.
- **The screens.** Nothing in section 7 asserts a screen. The dictionary and contract screens read the five operations through the gateway-bff composite route, one hop per call (DP-19).

Personal fields are not stated as a fixed count anywhere in this story; the count is read from `sys_fields.is_personal` at the version in force. The list read of rwb-case is the published operation of section 12.2, so no placeholder path remains.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field carries its data type, physical type, source system, owner role, refresh cycle and behavior when late, and every view field names its ACE column as `public.table.column`, or, for the 7 derived view fields, states that the view derives it | REQ-RDF-001; sys_fields |
| BR2 | The dictionary holds at least the E1001 baseline: 123 objects and 1,379 fields (93 tables with 1,075 fields, 49 of them on the four extension tables, and 30 views with 304 fields, 177 in Section A and 127 in Section B), every baseline object name and field ID present; later rows arrive by governed loads | D-RCV-35; Data Tier Map v1 section 8; RD-P1-025 |
| BR3 | Each data product has exactly one system of record and one owner role; a source is either an ACE column recorded on a view field or the Workbench itself | REQ-RDF-001; data_product; D-RCV-35 U1 |
| BR4 | A data contract is published only after its confirming role is recorded with a date and a stored document reference | DL12; data_contract |
| BR5 | A field change creates a new `sys_field_version` row with a date and a reason; earlier versions stay readable | Reference data change process; DT02; Principle 1 |
| BR6 | A dictionary load with an exception is refused in full; an ACE source field that is not a column of the view is an exception unless the view derives it | Reference data change process, step 3; CTL-08 |
| BR7 | A change to a field of a published contract opens a new contract version; the published version stays in force until the new one is confirmed and published | R-UNI-38 |
| BR8 | V0001 owns `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract`; this story adds no table, column, index or constraint and publishes rows only through the reference load and the endpoints | RWB-E1-001; D-RCV-28 |
| BR9 | A new ACE column reaches the dictionary as a reference load after its view column exists; an applied migration is never edited, and CHK-01 blocks the merge until the row exists | RWB-E1-069; BR-P1-001 |

**Where each rule lives in the target.** The rules below apply with the RD-P1-025 baseline and RD-P1-020 load ownership. BR1, BR2 and BR3 are answered by `sys_fields`, `sys_objects` and `data_product` in `rwb_source_data`, which this story reads through `DataDictionaryService` and the `GET /admin/data-dictionary/fields` operation with its `product`, `entity`, `field` and `sourceSystem` filters. BR4 and BR7 are answered by `DataContractService` over `data_contract`: the confirmation is written by `PATCH /admin/data-contracts/{contractId}` and the publish by `POST /admin/data-contracts/{contractId}/publish`, PATCH operations with `If-Match`; publish POST with `Idempotency-Key`. BR5 and BR6 are answered by the field write and by `DictionaryLoadHandler`, which keeps the whole-load refusal of the legacy loader now that the load arrives as a call from the rwb-case reference-data contract (DP-07). BR8 is answered by the baseline: RWB-P1-E1001-APP created the five tables and this story adds no DDL, so an applied migration is never edited (DP-15). BR9 is the pair of the view migration on RWB-P1-E1069-APP's sequence and the dictionary row this story writes, with CHK-01 as the gate; it is also the one rule that depends on how the load is triggered now that rwb-case owns the load (the dictionary load is applied first, RD-P1-071). The ACE value is read through the read path of RWB-P1-E1069-APP (AC3).

### 9. State transitions

None. This story does not change a case status. It changes the data contract status: DRAFT to PUBLISHED after the confirming role is recorded, a new DRAFT version when a field of a published contract changes, and PUBLISHED to SUPERSEDED when that new version is published. Each field change adds a version; earlier versions stay readable.

| From | Event | Condition | To |
|---|---|---|---|
| Field version n | `PATCH /admin/data-dictionary/fields/{fieldCode}` | The `If-Match` version is current and a reason is given | Field version n+1; version n stays readable |
| Contract DRAFT, no confirmation | `POST /admin/data-contracts/{contractId}/publish` | No confirmation is recorded | Refused with 409 and MSG-P1-021; the contract stays DRAFT |
| Contract DRAFT, confirmed | `POST /admin/data-contracts/{contractId}/publish` | The confirming role, the date and the document reference are recorded | PUBLISHED at its version, in force |
| Contract PUBLISHED | A field of the contract changes | The change is accepted and no DRAFT is open | The same contract opens version n+1 as DRAFT with no confirmation; version n stays PUBLISHED |
| Contract version n+1 DRAFT, confirmed | `POST /admin/data-contracts/{contractId}/publish` | The confirmation is present | Version n+1 PUBLISHED and version n SUPERSEDED in one transaction |
| Contract PUBLISHED or SUPERSEDED | Confirmation PATCH or publish with a new key | Not allowed | Refused 409; messageCode Pending (NEW-GAP-S6-2) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Changes field definitions, records the confirmation, publishes the contract (Reference data RU) |
| RW-REFADM, reference data administrator | Submits the dictionary load through the rwb-case reference-data contract; holds Reference data CRUD, so may also change a field, record a confirmation and publish |
| RW-COE, center of excellence analyst | Holds Reference data CRUD: reads and changes field definitions, may record a confirmation and publish. No per-product owner check applies |
| ACE team lead | Confirms the ACE read contract; owns the ACE columns it names (RWB-ACE-001) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts |
| rwb-source-data service identity | Applies an approved dictionary load through the handler; the retired SY-DATALOAD role is not used |
| rwb-case (P3) | Owns the reference-data contract the load is submitted through, and calls this service's reference-table handler for table code `sys_fields` (DP-07) |
| rwb-access (P4) | Holds the roles and the rights as data and answers the authorise check of every call through the guard library (DP-08, not in this story's pattern set) |

Every "who" in this table is a role code. The roles, their permissions and the separation-of-duty conflicts are held as data in rwb-access (P4) and reached through its authorise contract, not by a table read (DP-01). No approval level from the delegation of authority applies: the story takes no business decision, it records the one the ACE team lead gives.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-088 | sys_objects | object_name | Read |
| DF-REF-091 | sys_objects | data_product | Read |
| DF-REF-092 | sys_objects | system_of_record | Read |
| DF-REF-095 | sys_fields | field_id | Read |
| DF-REF-096 | sys_fields | object_name | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Write |
| DF-REF-099 | sys_fields | physical_type | Write |
| DF-REF-103 | sys_fields | source_system | Write |
| DF-REF-104 | sys_fields | source_field | Write |
| DF-REF-105 | sys_fields | is_personal | Read; a change through PATCH is Pending (NEW-GAP-S6-3) |
| DF-REF-106 | sys_fields | description | Write |
| DF-REF-107 | sys_fields | owner_role | Write |
| DF-REF-108 | sys_fields | refresh_cycle | Write |
| DF-REF-109 | sys_fields | late_behavior | Write |
| DF-REF-110 | sys_fields | interface_id | Write |
| DF-REF-111 to DF-REF-115 | sys_field_version | all fields | Write |
| DF-OPS-010 to DF-OPS-020 | data_contract | all fields | Write |
| DF-REF-070 to DF-REF-079 | data_product | all fields | Read |

`sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` exist in Recovery Workbench Physical Schema v9 (`rwb_source_data.sql`), were created by the baseline of RWB-P1-E1001-APP, and sit in schema `rwb_source_data` (DP-01, DP-15). This story writes rows, not DDL. Field IDs are those in the Logical Data Model and Data Dictionary. The 304 view fields this story describes in AC1, AC2 and AC3 are the columns of the 30 `recovery.v_ace_*` views, which stay in schema `recovery` and are read through the read path of RWB-P1-E1069-APP (DP-05); this story writes none of them and reads them once, in AC3, through that path.

### 12. Contract

Base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14, DP-02, DP-15). The document, the five schemas, the error envelope and the fakes are RWB-P1-E1064-CON's; this section states what this story serves and consumes.

#### 12.1 REST operations provided

Five operations, all owned by P1 rwb-source-data (Ownership Map rows `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish`). Access is Reference data R for the two reads and Reference data U for the three writes.

| Method | Path | Purpose | Schemas | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/admin/data-dictionary/fields` | The paged field read with the filters `product`, `entity`, `field` and `sourceSystem`, returning `DataDictionaryFieldPage` (`items` of `DataDictionaryField`, `page`, `size`, `total`) | `DataDictionaryFieldPage`, `DataDictionaryField` | Reference data R | Idempotent by the query |
| PATCH | `/admin/data-dictionary/fields/{fieldCode}` | Changes a field definition with a reason and writes a new `sys_field_version` row | `DataDictionaryFieldChange` in, `DataDictionaryField` out | Reference data U | `If-Match` version; 428 without it, 409 on a stale version |
| GET | `/admin/data-contracts` | Lists the data contracts, filtered by `sourceSystem` and `status`, returning `DataContract[]` | `DataContract` | Reference data R | Idempotent by the query |
| PATCH | `/admin/data-contracts/{contractId}` | Records the confirming role, the date and the stored document reference of a contract | `DataContractConfirmation` in, `DataContract` out | Reference data U | `If-Match` version; 428 without it, 409 on a stale version |
| POST | `/admin/data-contracts/{contractId}/publish` | Publishes a confirmed contract; a contract without a confirmation is refused | `DataContract` | Reference data U | `Idempotency-Key` header |

The field names are the ones of API Specification v7, info.version 5.1.0, character for character. Every response carries the `version` of each row and every successful PATCH returns `ETag: "<version>"`; every PATCH requires `If-Match: "<version>"`, returns 428 MSG-GEN-004 when missing and 409 MSG-GEN-004 on mismatch without writing, increments version on success, and returns the new ETag. PATCH has no Idempotency-Key. The publish POST requires a canonical lowercase UUID Idempotency-Key, stores status, headers and body for 24 h, and replays that response; mismatch or in-flight reuse returns 409 MSG-PLT-N009-05, a missing or invalid key returns 400 MSG-PLT-N009-03, and an unavailable idempotency store returns 503 MSG-PLT-N009-06 (RD-P1-001/006). `DataDictionaryField` carries `fieldId`, `entity`, `fieldName`, `dataType`, `physicalType`, `mandatory`, `listCode`, `sourceSystem`, `sourceField`, `refreshCycle`, `ownerRole`, `lateBehavior`, `interfaceId`, `isPersonal`, `version` and `versionDate`. `DataDictionaryFieldChange` carries `dataType`, `physicalType`, `mandatory`, `listCode`, `sourceSystem`, `sourceField`, `refreshCycle`, `ownerRole`, `lateBehavior`, `interfaceId`, `isPersonal` and `reason`. PATCH changes only supplied properties and requires `reason`; the load checks of AC4 (source system and view column) apply to PATCH; approval rules for changing `isPersonal` are Pending with Compliance (NEW-GAP-S6-3). `DataContract` carries `id`, `contractCode`, `sourceSystem`, `interfaceIds`, `contractVersion`, `status` (`DRAFT`, `PUBLISHED` or `SUPERSEDED`), `fieldCount`, `confirmedByRole`, `confirmedOn`, `confirmationDocumentId` (UUID), `publishedAt` and `version`. `DataContractConfirmation` carries `confirmedByRole`, `confirmedOn` and `confirmationDocumentId`. Every 4xx/5xx uses `application/problem+json` and shared `Problem`: required `type`, `title`, `status`, `messageCode`, `traceId`; optional `detail`, `instance`, `messageTh`, `field`; and `errors` only for multi-input 400/422 (RD-P1-004). 400/422/409/428/503 mappings follow the RD-P1-004 and RD-P1-001 tables. Unknown field/contract is 404 MSG-P4-003, with the standard message text. `interfaceIds` is the empty list for the ACE view contract (the yaml description; V0002 and V0003 are the views it covers, not outbound interfaces) and `fieldCount` is derived, 304 for `DC-ACE` at baseline; the value stored in the NOT NULL column `data_contract.interface_id` for that contract is Pending (NEW-GAP-S6-6). `confirmationDocumentId` and `{contractId}` are UUIDs.

**Statuses per operation (rwb-source-data.yaml 5.1.0).**

| Operation | Statuses | Message codes |
|---|---|---|
| GET `/admin/data-dictionary/fields` | 200, 400, 401, 403, 503; 422 for a size above the maximum (AC21, to be declared in the yaml) | MSG-GEN-001, MSG-GEN-007, MSG-GEN-002, MSG-P4-001, MSG-P4-002, MSG-GEN-006 |
| PATCH `/admin/data-dictionary/fields/{fieldCode}` | 200, 400, 401, 403, 404, 409, 422, 428, 503 | MSG-GEN-001, MSG-GEN-002, MSG-GEN-007, MSG-GEN-004, MSG-P4-001 to MSG-P4-003, MSG-GEN-006 |
| GET `/admin/data-contracts` | 200, 400, 401, 403, 503 | MSG-GEN-007, MSG-P4-001, MSG-P4-002, MSG-GEN-006 |
| PATCH `/admin/data-contracts/{contractId}` | 200, 400, 401, 403, 404, 409, 422, 428, 503 | MSG-GEN-001, MSG-GEN-004, MSG-P4-001 to MSG-P4-003, MSG-GEN-006 |
| POST `/admin/data-contracts/{contractId}/publish` | 200, 400, 401, 403, 404, 409, 503 | MSG-PLT-N009-03, MSG-PLT-N009-05, MSG-PLT-N009-06, MSG-P1-021, MSG-P4-001 to MSG-P4-003, MSG-GEN-006 |

**Validation of a field change and of a load row.** PATCH changes only supplied properties; `reason` is required and not blank. Lengths are the column limits of Physical Schema v9: `reason` 400, `lateBehavior` 200, `sourceField` 80, `physicalType` 30, `listCode` 30, `refreshCycle` 30, `ownerRole` 20, `dataType` 12, `interfaceId` 10. A longer value is 422 MSG-GEN-002; a value outside LOV-ROLE or LOV-REFRESH is 422 MSG-GEN-007. The mandatory columns of a load row are Pending (DEF-049, open), owner business analyst.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-ROLE and LOV-REFRESH, read as data once per list and cached by list version, never written as a constant | DP-07; one hop, 2 s timeout, breaker; failure gives 503 MSG-GEN-006 (X8) |

The list read is the one consumed business operation of this story (the authorise call of the rwb-access guard library runs on every operation): `ownerRole` is checked against LOV-ROLE and `refreshCycle` against LOV-REFRESH, in the handler and in the field change. The published path and fake are those of RWB-P3-E1043-CON. The field-versus-product source of `refreshCycle` is Pending, owner data architect (NEW-GAP-S6-4). Breaker thresholds are platform configuration. The load of section 12.3 is submitted the other way round: rwb-case calls this service's reference-table handler for table code `sys_fields`, so no REST call of this story's own is made to apply it.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slide 15). A dictionary change, a confirmation and a publish are synchronous admin calls; this story writes no outbox row and no event of its own.

#### 12.4 Events consumed

None. A dictionary change is a person's admin call and a load is a reference-load call; neither is started by an event, and Architecture v5 slide 15 gives the service no consumed event ("none: Airflow call; fallback polls ACE batch record").

#### 12.5 Workflows and activities

None. The five operations, the validation of a load and the version writes are synchronous steps. The activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` on task queue `rwb-source-data` in namespace `rwb-recovery` belong to other P1 stories (Architecture v5 slide 15); this story starts no workflow and no activity on that queue.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the dictionary is changed by a person and loaded by a governed reference load (DP-07, DP-10 not in this story's pattern set).

#### 12.7 Tables owned

| Object | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| `sys_objects` | `rwb_source_data` | P1 | Read: at least the 123 baseline object rows, retired objects included and marked retired |
| `sys_fields` | `rwb_source_data` | P1 | Read and write: at least the 1,379 baseline fields; later fields arrive by approved governed loads |
| `sys_field_version` | `rwb_source_data` | P1 | Write: one row per accepted change, with its date and reason |
| `data_product` | `rwb_source_data` | P1 | Read: the 14 products, their systems of record and their owner roles |
| `data_contract` | `rwb_source_data` | P1 | Read and write: DC-ACE, its confirmation, its status and its versions |
| `recovery.v_ace_*` (30 views) | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data | **Not created here**: RWB-P1-E1069-APP creates the 30 views; this story describes their 304 fields and reads one of them in AC3 through that story's read path |

No DDL is added: RWB-P1-E1001-APP created the five tables and their read model `v_data_dictionary`, and this story writes rows only (DP-15). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P3-E1043-CON fake | `GET /api/recovery/case/v1/admin/lists/{listCode}` and the reference-table handler for table code `sys_fields` | LOV-ROLE with and without the role a load names, LOV-REFRESH, an empty list, a timeout, and a full load, a refused load and a repeated file for `sys_fields` |
| RWB-P1-E1064-CON provider fake 5.1.0 (`fakes/rwb-source-data/5.1.0/`) | The five operations of this story | A page of fields, a field change, a contract in DRAFT, a confirmed contract, a published contract and its new DRAFT version, plus each declared error status of 12.1 |
| Delivered-baseline fixture | RWB-P1-E1001-APP and RWB-P1-E1069-APP | A container with schema `rwb_source_data` holding the five tables and at least the 1,379 baseline rows, and schema `recovery` holding the 30 views, so AC1, AC2 and AC3 run against the real objects once and not against a copy |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 5 operations on `/api/recovery/source-data/v1` | 1 operation, the rwb-case list read of 12.2 | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11, DP-13) |
| Kafka | None | None | The topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1015-APP (DP-14) |
| Temporal | None | None | No workflow, activity or Schedule; queue `rwb-source-data` is not used by this story |
| File | None | None | A load file arrives inside the reference-load request of the rwb-case contract and is not read from a store by this story |
| Reference load | 1 reference-table handler (`sys_fields`) | 1 load submission through the rwb-case contract | The handler validates and applies in one transaction; the load is P3's operation and this service's rows (DP-07) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.dictionary`, with the published types in `...sourcedata.dictionary.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is this story's own pattern twice: the queries of `DataDictionaryQuery` become the field read of 12.1, and the whole-load apply of `DataDictionaryLoader` becomes the reference-table handler that rwb-case calls instead of a jar another module imports. DP-07 is used, not delivered: rwb-case owns the reference-data contract, and this service provides the handler and reads the lists of values through it. DP-05 is used, not delivered: the 30 views and their read path are RWB-P1-E1069-APP's, and AC3 takes its value from there.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DataDictionaryController` | Controller | The two dictionary operations of 12.1 and their RFC 9457 problem responses |
| `DataContractController` | Controller | The three contract operations of 12.1, with `If-Match` and `Idempotency-Key` |
| `DataDictionaryService` | Service | Field reads with the four filters and the page, the counts, the versioned change with its reason and the optimistic lock |
| `DataContractService` | Service | DC-ACE over the 304 ACE fields, the confirmation record, the publish rule and the new DRAFT version on a field change |
| `DictionaryLoadHandler` | Reference-table handler for table code `sys_fields` | Whole-load validation of the six attributes, the source system and the view column; refusal in full with MSG-P1-002 and the first failing check; apply in one transaction |
| `ReferenceDataClient` | Client | The rwb-case reference-data contract through its client library: the list read of 12.2, one hop, 2 s (DP-07) |
| `SysFieldRepository`, `SysFieldVersionRepository`, `SysObjectRepository`, `DataContractRepository`, `DataProductRepository` | Repository | Read and write the five tables in `rwb_source_data`; no statement names another schema |
| `SysField`, `SysFieldVersion`, `SysObject`, `DataContract`, `DataProduct` | Entity | One per table |

**Database.** No DDL. RWB-P1-E1001-APP created `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` in `rwb_source_data` with at least the 123 object and 1,379 field baseline rows and the read model `v_data_dictionary`; this story writes only rows, through the reference load and the five operations (DP-15). The 30 `recovery.v_ace_*` views are RWB-P1-E1069-APP's and are not created, altered or granted here (DP-05).

**Configuration and reference data**

- The governance load is prepared by the data steward from `v_data_dictionary` and the 30 view definitions.
- The data product owners and 14 system-of-record seed values follow RWB-P1-E1001-APP section 13 and RD-P1-025.
- Expected-by times are the ones the baseline holds: 08:00 for daily ACE products and Monday 08:00 for weekly ACE products (DL11).
- LOV-ROLE and LOV-REFRESH are read through the rwb-case reference-data contract and its fake, never written in code (DP-07).
- The map of table code to handler is configuration: this service registers the handler for table code `sys_fields` with the reference-data contract, and adds no endpoint of its own for the load (DP-07, DP-11).
- The feature flag `rwb.dataengine.data-dictionary` gates the module and is set per environment by RWB-P1-E1064-OPS.

**Build steps**

1. Read `v_data_dictionary`; confirm every baseline object name and field ID, at least 123 objects and 1,379 fields, and the 30 view rows. No migration (AC1, AC2).
2. `DictionaryLoadHandler` with whole-load validation of the six attributes, the source system and the view column; refusal with MSG-P1-002 and the first failing check (AC4, X3, X8).
3. `DataDictionaryService` change with `If-Match` and a mandatory reason; one `sys_field_version` row per change (AC5, AC7).
4. `DataContractService`: DC-ACE from the 304 ACE fields; the confirmation record; the publish rule with MSG-P1-021; a new DRAFT on a field change (AC6, AC8).
5. The five operations on the contract baseline, with RFC 9457 problem details and the exact schema field names of 12.1 (AC1, AC4, AC5, AC6, AC7).
6. `ReferenceDataClient` against the RWB-P3-E1043-CON fake: a list, an empty list and a timeout (12.2).
7. Tests for AC1 to AC22 against the delivered-baseline fixture and the fakes (section 16).
8. Remove every import of the legacy published interface from the other packages, so no module reaches the dictionary in process any more (DP-11).

**Feature flag.** `rwb.dataengine.data-dictionary`, from the platform flag library. The flag covers the module, the two controllers and the handler registration; the tables are not behind a flag. Off, the five operations answer 404 (RD-P1-045 item 4); the messageCode of that answer and what the handler does with a delivered version are Pending, owner release owner (NEW-GAP-S6-9).

**Done when.** The tests in section 16 pass, all 30 views have dictionary rows in SIT, DC-ACE is PUBLISHED, the five operations answer on `/api/recovery/source-data/v1` with the field names of 12.1, the response time target for the field read and the limit for applying a load are agreed (Pending, owner solution architect, DL11), and no module imports the legacy interface.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | Publish of a contract with no confirmation | The data contract for {system} cannot be published until its system owner confirms it. |
| MSG-GEN-001 | Reason or confirmation value empty, or a required value missing | Enter {field}. |
| MSG-GEN-007 | Value not in its list of values | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-GEN-002 | Value longer than its column, or size above the maximum | {field} must be between {min} and {max}. |
| MSG-P4-001 | No valid session or no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-PLT-N009-03 / -05 / -06 | Idempotency-Key missing or invalid; reused or in flight; store unavailable | As the Error and Message Standard v6 rows of the platform |
| MSG-GEN-004 | Change from an old version, or no If-Match version | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Dictionary load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | The store or a consumed service is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Role without Reference data U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Unknown field or contract (404) | This case is not in your scope. (the standard text; a field-specific text is not published) |

**Open decisions.** DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863), DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104), DL12 (ASM-0189, ASM-2559, ASM-2608) and DL43 (confirmation of the ACE read contract) remain open; each is carried with its assumption.

Thai text for each message follows decision DL10. Message texts follow the Error and Message Standard v6; nothing in the split renames a message. The {action} values of MSG-P4-002 for the three writes are not published. MSG-P4-002 is now raised by the guard library of rwb-access, so the refusal reads the same in every service; MSG-GEN-006 is the answer when the rwb-case reference-data contract does not answer inside 2 s (X8).

### 15. Screens and states

No screen in this story. Developers and analysts read the dictionary through `GET /admin/data-dictionary/fields` on `/api/recovery/source-data/v1`; SCR-40 Reference data shows versioned tables from Epic 8, and until then changes go by the reference load or the endpoints. The dictionary and contract screens of SCR-40 will reach the five operations through the gateway-bff composite route, which calls rwb-source-data once per operation, one hop with a 2 s budget (DP-19; RWB-PLT-N001-CON); the route, the screen field list and the rendering of a version belong to the screen owner and are not built or asserted here. The states of SCR-40 for empty, loading, error and no access are Not specified in the source documents (CG-ALL-2237).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 | End to end | Baseline of at least 123 objects and 1,379 fields; count, presence and completeness queries |
| TC-E1-064-02 | AC2, BR2 | End to end | 30 views, 304 fields; one view column with no dictionary row |
| TC-E1-064-03 | AC3, BR1, BR3 | End to end | Account ACC0000017 with delay_days 95; dictionary query for DF-ACE-018 |
| TC-E1-064-04 | AC4, BR6, BR9 | End to end | Dictionary fixture without DF-ACE-204; approved version with the right and the wrong ACE column |
| TC-E1-064-05 | AC5, BR5 | End to end | Change of DF-ACE-018 late behavior with a reason and with an empty reason |
| TC-E1-064-06 | AC6, BR4 | End to end | DC-ACE with 304 fields; confirmation on 2026-11-12; a second contract with no confirmation |
| TC-E1-064-07 | AC7 | End to end | Two changes to DF-ACE-020 from version 1; one change with no If-Match |
| TC-E1-064-08 | AC8, BR7 | End to end | Published DC-ACE and a change to DF-ACE-018 |
| TC-E1-064-09 | Access | Component | RW-TRIBE sends PATCH /admin/data-dictionary/fields/DF-ACE-018; refused with MSG-P4-002 |
| TC-E1-064-10 | Operations of section 12 | Component | Five operations against the RWB-P1-E1064-CON fake; this story has no event and no activity |
| TC-E1-064-11 | Section 12.7 tables | Component | Boundary rows of the five tables at the baseline minimum counts |
| TC-E1-064-12 | AC9, BR8 | Component | No table, column, index or constraint added by this story |
| TC-E1-064-13 | AC10 | Component | No session, RW-TRIBE write, unknown field ID |
| TC-E1-064-14 | AC11 | Component | Publish key replay, mismatch, in-flight reuse, missing key, invalid key, store failure |
| TC-E1-064-15 | AC12 | Component | rwb-case list read timeout and non-2xx during a load |
| TC-P1-E1064-APP-01 | AC13 | Component | RW-TRIBE confirmation and publish |
| TC-P1-E1064-APP-02 | AC14 | Component | Reason of 400 and 401 characters and of spaces only |
| TC-P1-E1064-APP-03 | AC15 | Component | isPersonal set to false on a personal field (expected answer Pending, NEW-GAP-S6-3) |
| TC-P1-E1064-APP-04 | AC16 | Component | Confirmation and republish of a published contract |
| TC-P1-E1064-APP-05 | AC17 | Component | Second field change while a DRAFT is open |
| TC-P1-E1064-APP-06 | AC18 | Component | Invalid, duplicate, empty and re-delivered load |
| TC-P1-E1064-APP-07 | AC19 | Component | Database and authorise unavailable |
| TC-P1-E1064-APP-08 | AC20 | Component | Audit record of change, confirmation, publish and refusal |
| TC-P1-E1064-APP-09 | AC21 | Component | Size above the maximum; filter with no match |
| TC-P1-E1064-APP-10 | AC22 | Component | View column with no dictionary row (owned by RWB-P1-E1069-APP) |

The test case IDs are those of Test Cases v9, tab Story test cases. The legacy level "System" maps to "End to end" and "Access" maps to "Component". The five operations of TC-E1-064-01 and TC-E1-064-05 to TC-E1-064-08 are called against the RWB-P1-E1064-CON fake at Component level inside the contract tests of that story, and against the delivered baseline at End to end here.

### 17. Guardrails

- No business value in code: owners, cycles, late behavior and contract content are data rows in `rwb_source_data`; the module reads them and never holds a constant (DP-07).
- No personal data in logs, tests, events or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person, and a load file in DEV and SIT is synthetic.
- No read of another service's tables: every statement names `rwb_source_data`, and the one ACE read of AC3 goes through the read path of RWB-P1-E1069-APP and the `recovery.v_ace_*` views (DP-01, DP-05).
- One hop and 2 s on the rwb-case reference-data read; a slow answer refuses the load and returns no list (DP-11).
- A published contract is never edited in place; a change makes a new version.
- No DDL: RWB-P1-E1001-APP owns the five tables; this story never adds, alters or drops a column, and an applied migration is never edited (DP-15).
- The service publishes no event of its own; the only message it causes is the library write of `DecisionRecorded` on `rwb.decision-record.v1`, which carries no personal data (DP-03, used through the library and not delivered here).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | Recovery data is organized in 14 data products, each with exactly one named system of record, one read path and one named owner. Source data is read from ACE through read-only views and is not copied | Business Requirements Epic 1, sections 3.1, 4 and 5 | FEAT-RDF-01 | All recovery processes | CTL-08; DL12; D-RCV-35 U1; BR1 to BR3, BR8 | TC-E1-064-01, TC-E1-064-02, TC-E1-064-03, TC-E1-064-06, TC-E1-064-09, TC-P1-E1064-APP-10 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record (ACE, ingested from the named source), refresh cycle and retention | Business Requirements Epic 1, sections 3.1, 4 and 5 | FEAT-RDF-01 | All recovery processes | R-UNI-38; BR4 to BR7, BR9 | TC-E1-064-04, TC-E1-064-05, TC-E1-064-07, TC-E1-064-08, TC-P1-E1064-APP-04, TC-P1-E1064-APP-05, TC-P1-E1064-APP-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1064-CON | Contract | H build dependency: the OpenAPI 3.1 document of the five operations, the five schemas, the error envelope and the fakes this story builds against from Day 1 |
| RWB-P1-E1001-APP | App development | H build dependency: the baseline migration, the five tables, at least the 123 objects and 1,379 fields and `v_data_dictionary` |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 `recovery.v_ace_*` views, the view conformance test CHK-01 and the read path AC3 takes its value from |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data contract of rwb-case, through which the load is submitted and the lists of values are read (DP-07) |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and migration ownership (DP-15) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the dictionary and contract screens will use (DP-19) |
| RWB-P1-E1064-OPS | DevOps | X external dependency: the chart, the flag values, the dashboards, the alerts and the runbook of the module; every deployment value (replica count, resource size, probe path and timing, alert threshold, window and incident route) is a named chart value set per environment by the platform team, not hard-coded (GAP-0500) |
| RWB-P1-E1065-APP, RWB-P1-E1066-APP, RWB-P1-E1067-APP | App development | Siblings of the same service: the sandbox generator and the interaction ledger; they read the dictionary and write none of its rows |
| RWB-P1-E1016-APP | App development | Sibling: access control per data product and the catalog entry maintenance on `data_product` and `data_product_access` |
| RWB-P1-E1069-DB | ACE DB | Sibling of the view key: the login, the grant block and the four extension tables whose 49 dictionary fields this story describes |

### 19. Out of scope

- The five tables, the seed rows and the read model `v_data_dictionary`: RWB-P1-E1001-APP the baseline, and this story writes rows only.
- The 30 `recovery.v_ace_*` views, the view conformance test CHK-01 and the read path of AC3: RWB-P1-E1069-APP.
- The login, the grant block, the view owner `ace_view_owner` and the four extension tables: RWB-P1-E1069-DB.
- The OpenAPI and AsyncAPI documents, the error envelope, the versioning rule and the fakes: RWB-P1-E1064-CON; this story implements against them.
- The chart, the flag values, the dashboards, the alerts, the runbook and the smoke run: RWB-P1-E1064-OPS.
- The reference-data contract itself, the reference-load operation and its approval: rwb-case, RWB-P3-E1043-CON (DP-07). This story provides one handler for table code `sys_fields` and reads the lists of values; it defines nothing of the contract.
- Access control per data product, PDPA masking and the catalog entry screen: RWB-P1-E1016-APP and rwb-access (DP-08).
- Freshness stamps per data product, retention per product and table, and the reconciliation report: RWB-P1-E1015-APP, RWB-P1-E1017-APP and RWB-P1-E1011-APP.
- The reference data screen SCR-40 in its final form: Epic 8, through the gateway-bff composite route.
- Contracts for stage 2 data products: RWB-P1-E2010-APP.

### 20. Remaining delivery steps

- Size: Not specified; owner delivery squad.
- Epic design sign-off: Pending; owner product owner and solution architect.
- Contract Done (RWB-P1-E1064-CON): Pending; owner contract owner.
- Fake published (provider fake 5.1.0 and the RWB-P3-E1043-CON handler fake): Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner QA lead.
