# RWB-PLT-TE004-APP Masked data in SIT and UAT
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP13, DP19 |
| Parallel lane | L-PLT-TPL-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P1-E1065-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-004 for the 19-schema target. The legacy acceptance criteria are kept word for word and re-pointed: the masked copy no longer refills the single `recovery` schema, it loads one staging schema per service and swaps the schema of each of the 19 services, and every legacy value is unchanged (masking rule version "MASK-2026.11", extract "PII-SIT-20261120", business date 2026-11-19, 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903). The legacy endpoint table is rewritten to the per-service base path. The integration copy of the same legacy key is RWB-ITG-TE004-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-TE004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)** and a **squad member (RW-TRIBE)**, I want **the masked copy that the PII service delivers for SIT or UAT loaded into the 19 `rwb_<name>` schemas of the ACE database — per environment, one staging schema per service (`<schema>_next`), every as-built check kept and applied to every service, the swap of each service's staging schema for that service's live schema only after the checks of all 19 services pass, and a load report per service that names the service, the schema, the extract ID, the business date, the masking rule version and the row counts — instead of one `recovery` schema refilled and swapped as a whole**, so that **SIT and UAT run at production volume and with production data shapes on the schema-per-service estate that will run them, no customer value is exposed, and one refused or missing service never leaves the estate half loaded**.

The rework keeps the loader and the checks of RWB-TE-004 and changes the object of the load. The legacy story hands one flat extract to one `recovery` schema, puts it in `recovery_next` and renames that schema in one step; the target has 19 schemas with one login each and no grant across them (Arch v5 slide 29), so the loader has to resolve each table of the extract to the schema of the service that owns it, stage it there, verify it there and swap it there. The legacy loader was never built (the legacy story is Ready for build, this story is Not started), so nothing built is changed and no as-built code is discarded; the legacy acceptance criteria and their values are carried unchanged and re-pointed, the legacy endpoint table is rewritten to the per-service base path a test user actually reads through gateway-bff, and the personal-data field list is read through the owner's contract instead of from a tag table the loader reads directly.

### 2. Business rationale

Masked copies are the only way SIT and UAT can run at production volume with production data shapes. Synthetic data proves the code path, not the volume, the skew or the shape of a real record, and NFR-045 allows masked copies in user acceptance while it forbids production data in development ("Synthetic in development, masked in user acceptance"; Proposed, owner Solution architect). The bank's PII service produces the masked copy under the Compliance masking rules, and this story is the load that puts it into SIT and UAT: it refuses any copy that still holds a personal value, keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production, and lets no copy near DEV. It serves REQ-RDF-010 (access to each data product controlled per role, personal data masked by role in line with PDPA) and REQ-ACA-005 (personal data masked by role on every screen and in every agent call), both Must and owned by Compliance, and it is governed by DL26, the Compliance decision on retention and masking that fixes which fields are masked for which role and keeps every personal field masked while the rules carry no values.

The change the rework carries is the object of the load. In the monolith the whole estate is one `recovery` schema: one file set, one `recovery_next` staging schema, one rename, one report. Arch v5 replaces that with 19 schemas `rwb_<name>`, one login each, no grant on another schema and no cross-schema join, view or foreign key (slide 29); slide 41 gives every schema an owner and its first API path, and slide 20 gives every service its own block of tables plus outbox and inbox. A table therefore belongs to exactly one service, and the loader can no longer treat the extract as one bundle. That changes the loader in five ways. The staging object becomes a schema per service rather than one schema. The foreign-key check can only pass inside a single schema, because a key that crosses a schema is forbidden and a service holds another service's ID and asks the owner through its contract. The masking verifier must scan every `is_personal` field in every schema, not the two tables the legacy story happened to name, or a new personal column in a new service is outside the check by construction. The swap becomes one swap per service, and it may only run after the checks of all 19 services pass, so a refusal anywhere leaves the previous copy in place everywhere and the estate is never mixed. And the report becomes per service, because the platform administrator and the squads need to know which schema holds which extract, at which business date and under which masking rule version.

The 19 schemas, their logins and their grants are database work outside this story (RWB-PLT-NF06-DB and the per-service DB stories). What this story owns is the decision of which table goes where, taken from the Ownership Map and from the per-service database stories, and the proof that the copy is complete, masked, consistent and refused in full when any one service fails.

### 3. Preconditions

- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its client library (DP-07). The lists the load compares against — the environment lists and the product groups the manifest totals are counted by — are reference rows read through it and never values in code.
- **RWB-PLT-E1037-CON** is published: the authorise contract of rwb-access and the guard library (DP-08). The load runs under its own identity and is authorised through it, and the masking policy that a test user's read is subject to is that service's policy.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The SIT and UAT endpoint a test user reads on the loaded copy is the per-service base path behind that route; the load provides no route of its own.
- The **two service CON dependencies of the run** are published: **RWB-P3-E1043-CON**, the rwb-case contract behind the reference data (DP-07), and **RWB-P4-E1037-CON**, the rwb-access contract behind the authorise call (DP-08). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- **RWB-P1-E1065-CON** is published: the rwb-source-data contract behind the personal-data field registry and the `is_personal` tags, which the plan gives to the sandbox and synthetic data story (the legacy RWB-E1-065). The field list the verifier scans comes through that contract; the registry operation itself is a gap and no path is invented for it here.
- The PII service delivers a masked extract per environment to the SIT or UAT intake container, with a manifest: extract ID, business date, masking rule version, and the row count per table, with the case accounts counted per product.
- The 19 schemas `rwb_<name>` and their 19 logins exist in SIT and UAT at the same Flyway version as the extract (Arch v5 slide 29), each with the grant on its own schema only.
- The masking rule version in force is the Compliance-owned version (DL26); until Compliance supplies the rules, every `is_personal` field is replaced by a token.
- The platform administrator (RW-PLATADM) starts the load; squad members hold RW-TRIBE; the load itself runs under the data-load identity SY-DATALOAD.
- The per-service staging schema naming, the per-service extract layout, the personal-data field registry operation and the tool schema name are Not specified in the source documents (GAP-1435; ASM-2522); they are applied as the working defaults of section 13 and are closed by the solution architect before the load is published.

### 4. Flow

1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT, the manifest naming the row count per table and the case accounts per product.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment; the start takes the per-environment lock or is refused if the lock is held.
3. MaskedCopyLoader: refuses to run when the target environment is not SIT or UAT (DEV and PROD are refused), before any file is read.
4. MaskedCopyLoader: preflight over the schema set: every service named in the manifest resolves to an existing schema at the extract's schema version, every service of the 19 has its schema, and no schema is present that the extract does not name. A new service with no schema, or a missing schema, fails the run here, before any file is read.
5. ManifestValidator: checks the extract ID against `tools.masked_copy_load` (a repeat is skipped), the masking rule version against the version in force, the schema version against the target, and the control totals of the manifest.
6. MaskedCopyLoader: resolves each table of the extract to the code of the service that owns it, from the Ownership Map and the per-service database stories, and loads each service's tables into that service's own staging schema `<schema>_next` under the service's staging grant, never writing into a second service's schema.
7. MaskedCopyLoader: runs the load checks of CTL-02 per file and per service — business date, structure, control totals (row count per table and per product) and keys — and checks that the foreign keys resolve inside each staging schema.
8. MaskingVerifier: scans every column tagged `is_personal`, in every one of the 19 staging schemas, for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address. The tag source is the personal-data field list read through the rwb-source-data contract.
9. MaskedCopyLoader: holds every swap until the checks of all 19 services have passed; on success, PerServiceSchemaSwap swaps each service's `<schema>_next` for that service's live schema, one service at a time under the environment lock.
10. LoadReportWriter: writes the load report and the `tools.masked_copy_load` row per service: the service, the schema, the extract ID, the business date, the masking rule version, the rows per table and the check results.
11. Squad member: runs SIT or UAT tests on the masked copy, reading the case through the per-service base path behind gateway-bff and the authorise call of rwb-access.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal | Load refused in full in every one of the 19 schemas; previous copy stays in use in all of them | MSG-P1-002 | AC2 |
| X2 | Row count differs from the manifest | Load refused in full; previous copy stays | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC4 |
| X4 | The same extract ID is loaded again | Load skipped; report shows the earlier load | None | AC5 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC6 |
| X6 | A second load starts while one runs | Second start refused by the per-environment lock | MSG-P2-006 | AC7 |
| X7 | A service's checks fail after the other services have passed | No service is swapped; every staging schema of the run is discarded and every previous copy stays in use | MSG-P1-002 | AC8 |
| X8 | A service appears in the extract with no schema in the environment, or a schema of the 19 is missing | Preflight fails the run before any file is read; no staging schema is written and no swap happens | MSG-P1-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three platform contracts, the two service contracts of the run and the rwb-source-data contract of the field list; the reader path is reached through gateway-bff, so no service has to be built first; no screen |
| Negotiable | The staging suffix, the swap order, the tool schema and the per-service layout are working defaults recorded as assumptions; the checks, the environment guard and the swap-after-all-checks rule are fixed by NFR-045, DL26 and Arch v5 slide 29 |
| Valuable | SIT and UAT run at production volume with no customer data exposed, on the 19-schema estate that will run them, and one refused service cannot leave the estate half loaded |
| Estimable | One tool module, four service classes, one per-service swap, one environment lock, one report writer and the configuration of the 19 schemas |
| Small | Fits in one sprint with its tests, on a test extract with a manifest |
| Testable | Each criterion runs on a test extract with a manifest against throwaway staging schemas, with the two contract fakes of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with row counts per product

  Scenario: AC1 Masked copy (legacy RWB-TE-004 AC1)
    Given a masked copy from the PII service
    When it is loaded into SIT
    Then every column tagged is_personal in interaction and document_field holds a token or a masked value
    Then the row counts keep their shape: the count per table and per product equals the manifest
    Then each person key joins to the same case_party and case_account rows as in the extract

  Scenario: AC2 A personal value left in the copy (legacy RWB-TE-004 AC2)
    Given interaction row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in summary
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in interaction.summary"
    Then the previous SIT copy stays in use

  Scenario: AC3 Totals that do not match the manifest (legacy RWB-TE-004 AC3)
    Given the case_account file holds 28,118 rows
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals case_account 28,118 against 28,119"

  Scenario: AC4 A copy aimed at DEV (legacy RWB-TE-004 AC4)
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file

  Scenario: AC5 The same extract twice (legacy RWB-TE-004 AC5)
    Given extract "PII-SIT-20261120" was loaded into SIT on 2026-11-20
    When it is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20

  Scenario: AC6 A masking rule version that is not in force (legacy RWB-TE-004 AC6)
    Given a manifest with masking rule version "MASK-2026.10"
    When the copy is loaded into UAT
    Then the system refuses the load in full with MSG-P1-002 and check "masking rule version MASK-2026.10 is not in force"

  Scenario: AC7 A second load while one runs (legacy RWB-TE-004 AC7)
    Given a masked copy load into SIT is running
    When a second load into SIT starts
    Then the system refuses the second load with MSG-P2-006

  Scenario: AC8 One staging schema per service and the swap only after every service passes (new, D-RCV-60)
    Given the manifest names each service it carries data for, with the row counts per table
    Given the 19 schemas rwb_<name> exist in SIT at the extract's schema version
    When the masked copy load starts for SIT
    Then MaskedCopyLoader resolves each table to the schema of the service that owns it and loads it into that service's staging schema <schema>_next
    Then it runs the environment guard, the extract-ID and masking-rule checks, the control totals, the masking verifier over every is_personal field and the foreign-key resolution for every service
    Then no staging schema is swapped while any service's checks are still open
    When the checks of every service have passed
    Then PerServiceSchemaSwap swaps each service's staging schema for that service's live schema, one service at a time under the environment lock
    Then the load report names the service, the schema, the extract ID, the business date, the masking rule version and the row counts
    When one service's checks fail, or the extract names a service with no schema, or a schema of the 19 is missing
    Then no service is swapped and every previous copy stays in use, and a missing schema fails the run before any file is read with MSG-P1-002
```

**Note on the criteria.** AC1 to AC7 are the legacy criteria of RWB-TE-004, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed, and the checks they name are kept as the legacy story specified them. AC8 is the only new criterion and it carries no business value: it tests the per-service staging and the swap-after-all-checks rule of the 19-schema target. The publisher of the extract is still the PII service, which is an outside system and not a contract of this estate.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force; the tag source is the personal-data field list read through the rwb-source-data contract, and the verifier scans every `is_personal` field in every one of the 19 schemas, not the two tables of the legacy story | Masking rules (Compliance, DL26); DP-05; this story |
| BR3 | A copy with any personal value left in it is refused in full, in every schema of the run | CTL-11; DQ check "Refuse the load" |
| BR4 | Dates and keys are not masked; counts equal the manifest per table and per product | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table and in every schema, so joins hold; a token crosses a schema only through the owner's contract, never through a join | Mapping rule "Personal data" (s2t.txt); DP-01 |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |
| BR7 | One staging schema per service, named `<schema>_next`; every check of the as-built story runs per service; the swap of a service's staging schema may run only after the checks of all 19 services pass, one service at a time under the environment lock; on any failure the previous copy stays in place everywhere and the estate is never mixed | Arch v5 slide 29; this story (ASM-2522, ASM-2523) |

### 9. State transitions

The case status does not change in this story. The states below are the load, the schema in the run and the copy of the environment.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | Platform administrator starts the load | Environment is SIT or UAT and the lock is taken | Preflight |
| Preflight | Schema set does not match the extract | A service with no schema, or a missing schema, or an extract with no service | Refused (no file read, no staging schema written) |
| Preflight | Environment is DEV or PROD | None | Refused (no file read) |
| Preflight | Manifest check fails | Extract ID already loaded, masking rule version not in force, schema version differs | Refused |
| Preflight | Preflight passes | None | Running |
| Running | Files load into the per-service staging schema | The service's staging grant holds | Staging |
| Staging | Control totals, keys and foreign keys pass for that service | None | Checks passed (for that service) |
| Checks passed | Another service's checks are open | None | Held (no swap) |
| Checks passed | The checks of every service have passed | None | Swapping |
| Swapping | The service's `<schema>_next` is renamed to its live schema | None | Swapped (per service) |
| Swapping | A swap fails | None | Refused in the run; the remaining services are not swapped and the previous copy is restored from the retained one |
| Any state before Swapping | Any check fails | None | Refused; staging schemas discarded; previous copy in use everywhere |
| Preflight | The extract ID is already loaded | None | Skipped (report names the earlier load) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT, owns the intake containers, reads the load report per service and reruns a refused run |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26); reads the verifier result of a run |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights, through the per-service base path behind gateway-bff |
| SY-DATALOAD, data load | The identity the loader runs under in SIT and UAT; holds the staging grant on the schemas of the run and writes no live schema outside the swap |
| ACE database administrator | Owns the 19 schemas, the 19 logins and the staging schemas of each environment; not a Workbench role |
| No role | May run a copy in DEV or PROD, read another service's schema, swap one service's schema on its own, or copy a masked extract from SIT or UAT to another environment |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-EXT-001 to DF-EXT-012 | party_ext | all fields | Write |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all fields | Write |
| DF-REF-105 | sys_fields | is_personal | Read |

The other recovery tables in the extract load the same way. Field IDs are those in the Logical Data Model and Data Dictionary.

Each table above now lives in the schema of the service that owns it, per the Ownership Map: `recovery_case`, `case_account` and `case_party` in `rwb_case` (P3 rwb-case, Arch v5 slide 41); `interaction`, `party_ext`, `contact_point_ext` and `sys_fields` in `rwb_source_data` (P1 rwb-source-data, the ledger and the extension tables under the R-PREC default ruling and DP-18); `document_field` in `rwb_document` (P5 rwb-document). The `Write` rows above are writes into that service's staging schema of the run and, after the swap, into its live schema; no row is written into a second service's schema and no foreign key crosses a schema (DP-01; Arch v5 slide 29). The `is_personal` read is now a read of the personal-data field list through the rwb-source-data contract, and `sys_fields.is_personal` in `rwb_source_data` is the tag source behind that list, never a table the loader opens directly.

The per-service staging schema naming, the layout of the extract per service, the operation that returns the personal-data field list and the name of the tool schema are Not specified in the source documents (GAP-1435; ASM-2522), and the tool schema and the field-list default are ASM-2524. The loader takes the working defaults of section 13 until the gap closes.

### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it.

#### 12.1 REST operations provided

None. The loader is a tool outside the ACE services and provides no REST operation; the platform administrator starts it in the pipeline and reads its report there. The reserved platform names of the naming rule — a platform REST base, a platform event topic and a platform task queue — are not used by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Ownership Map row | Use |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | `GET /cases/{caseId}` | The masked case a SIT or UAT test user reads on the loaded copy, with its parties and accounts, to prove that the load left the joins intact (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | `POST /authorise` | The right, the scope and the masking policy of the identity that starts the load and of the test user who reads the copy; a role without the right is refused with MSG-P4-002 (AC1) |

Both calls are one hop to the owning service on that service's own base, with the 2 s client budget (DP-11, DP-13). The test user's case read is reached through the gateway-bff composite route (DP-19).

Three contract dependencies are named and consumed as published contracts, not as paths of this story:

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The environment lists and the product groups the manifest totals are counted by (DP-07) |
| `RWB-P4-E1037-CON` | P4 rwb-access (the platform contract behind it is `RWB-PLT-E1037-CON`, epic RWB-PLT-LIB) | The authorise envelope, the error contract and the masking policy of the reader and of the load identity (DP-08) |
| `RWB-P1-E1065-CON` | P1 rwb-source-data | The personal-data field registry and the `is_personal` tags the verifier scans; the registry operation is a gap and no path is invented for it (GAP-1435; ASM-2524) |

No path, version or payload of a contract is repeated here; they belong to the contract stories that publish them.

#### 12.3 Events published

None. The load is a pipeline tool and publishes no business event; a run, a refusal and a swap are recorded in `tools.masked_copy_load` and in the report, and nothing is produced on a Kafka topic.

#### 12.4 Events consumed

None. The load waits on no topic: it is synchronous in the pipeline, its result is its own run row, and the reader assertions are made through the two operations of 12.2.

#### 12.5 Workflows and activities

None. No Temporal workflow, activity or Nexus operation is started or awaited; the load is a batch tool of the SIT and UAT pipeline and not a service worker, and it starts nothing on a service task queue.

#### 12.6 Schedules

None. The masked copy load is a manual pipeline stage started by the platform administrator for SIT or UAT after the PII service delivers an extract; it is not a scheduled job and not in the production job list, and it creates no Temporal Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `masked_copy_load` | `tools` | the loader (outside the 19 services) | One row per run and per service: extract ID, environment, business date, masking rule version, service, schema, row counts, check results and result. The schema name is the working default ASM-2524 (GAP-1435) |

The tool schema sits outside the 19 service schemas and is not one of them; the loader owns no business table, and it writes no service table except through the per-service swap of a staging schema that it filled.

#### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case case read fake | `RWB-P3-E1043-CON` behind `GET /api/recovery/case/v1/cases/{caseId}` | One masked case with its parties and accounts and the environment lists and product groups the manifest totals are counted by (AC1, TC-TE-004-01, TC-TE-004-08) |
| rwb-access authorise fake | `RWB-P4-E1037-CON` behind `POST /api/recovery/access/v1/authorise` | The case right granted to RW-TRIBE and to the load identity, the masking policy in force, and a refusal with MSG-P4-002 for a role without the right (AC1, TC-TE-004-08) |

The PII service is an outside system that supplies a file: it is not a contract of this estate and is not faked.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 consumed | The case read of rwb-case and the authorise call of rwb-access, one hop each, 2 s (DP-11, DP-13); none provided |
| Kafka | None | No event is published or consumed by the load |
| Temporal | None | The load is a pipeline tool, not a workflow or an activity |
| File | 1 | The masked extract and its manifest, read from the SIT or UAT intake container |

### 13. Solution plan

**Deliverables.** The tool module `tools/masked-copy-loader`, Java package `recovery.tools.maskedcopy`, built as a separate build module that is not packaged into any ACE service (the legacy packaging is kept); the per-service staging and swap; the table-to-schema resolution from the Ownership Map; the load report; and the pipeline stage with the per-environment lock.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MaskedCopyLoader | Job | Spring Batch job: environment guard, schema-set preflight, table-to-schema resolution, file load into one staging schema per service, checks, and the hand-off to the swap (BR1, BR2, BR7) |
| ManifestValidator | Service | Extract ID against `tools.masked_copy_load`, masking rule version against the version in force, schema version against the target, control totals per table and per product (BR4) |
| MaskingVerifier | Service | Personal value patterns over every `is_personal` field in every staging schema, with the field list read through the rwb-source-data contract (BR2, BR3) |
| LoadReportWriter | Service | Writes the load report and the `tools.masked_copy_load` row per service (BR7) |
| PerServiceSchemaSwap | Job | Swaps `<schema>_next` for the live schema of one service, only after every service's checks pass, one service at a time in the configured order, and restores from the retained previous copy if a swap fails (BR7) |
| EnvironmentLock | Service | One advisory lock per environment, so a second load cannot start and two swapper instances cannot run (BR7) |

**Database.** No new business table. The stage fills `<schema>_next` for each service of the run, checks the foreign keys inside that schema, and renames the staging schema to the live schema of the service after every service's checks pass; an advisory lock per environment prevents two loads at once; the tool table `tools.masked_copy_load` in schema `tools` records the extract ID, the environment, the business date, the masking rule version, the service, the schema, the row counts and the result. The schema `tools` is outside the 19 service schemas and is the working default ASM-2524 (GAP-1435; ASM-2522).

**Configuration and reference data.**

- `rwb.maskedcopy.allowed-environments=SIT,UAT`.
- `rwb.maskedcopy.intake-container` per environment, owned by the platform administrator.
- `rwb.maskedcopy.schemas`: the 19 schema names and the service code of each, used by the preflight and the swap order.
- `rwb.maskedcopy.staging-suffix=_next`, the working default of ASM-2522.
- `rwb.maskedcopy.swap-order`, the working default of ASM-2523.
- `rwb.maskedcopy.tool-schema=tools` and `rwb.maskedcopy.tool-table=masked_copy_load`, the working default of ASM-2524.
- The masking rule version and the allowed environment and product-group lists, read as reference rows (DP-07); the masking rule version comes from the Compliance-owned rules (DL26) and is never a value in code.
- The personal-data field list, read through the rwb-source-data contract (RWB-P1-E1065-CON); the registry operation is the gap of GAP-1435.
- Feature flag: `rwb.dataengine.masked-copy`, unchanged from the legacy story.

**Build steps**

1. Environment guard reading the deployment environment: refuse anything that is not SIT or UAT, before any file is read.
2. Schema-set preflight over `rwb.maskedcopy.schemas` and the manifest: a service with no schema, a missing schema and an extract naming no known service each fail the run here.
3. ManifestValidator with the extract ID check against `tools.masked_copy_load`, the masking rule version check and the schema-version check.
4. Table-to-schema resolution from the Ownership Map and the per-service database stories, and the file load into `<schema>_next` with the CTL-02 checks and the manifest totals.
5. MaskingVerifier over every `is_personal` field of every staging schema, with the field list from the rwb-source-data contract and the patterns of the as-built verifier.
6. Foreign-key resolution inside each staging schema, then the hold until every service has passed.
7. PerServiceSchemaSwap with the configured order and the environment lock, the retained previous copy and the restore path of a failed swap.
8. LoadReportWriter and the `tools.masked_copy_load` row per service.
9. Tests for AC1 to AC8 on a test extract, with the two contract fakes, and the reader test of a SIT test user through the per-service base path behind gateway-bff.

**Done when.** The nine test cases of section 16 pass, the checks of the as-built story are exercised per service on a test extract, a failure in one service leaves every previous copy in place, and the first masked copy of the 19 schemas is in SIT before the Epic 1 SIT run.

The per-service staging name, the extract layout per service, the field-list operation and the tool schema name are Not specified in the source documents (GAP-1435; ASM-2522); the swap order and the lock are ASM-2523 and the tool schema and field-list default are ASM-2524.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-004 and this story adds no message text. In MSG-P1-002 the {source}, {date} and {check} of a per-service refusal name the service, the business date and the check; the check names the schema and the table of the service that failed. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and no new screen state. The platform administrator and the squads read the load report in the pipeline, and a test user sees the masked copy through the normal SIT and UAT screens, which reach a service through the gateway-bff composite route (DP-19) and the per-service base path (DP-13), with personal fields shown as tokens or masked values under the masking policy of rwb-access (DP-08).

The load report is the surface of this story: one section per service, with the service, the schema, the extract ID, the business date, the masking rule version, the rows per table, the control totals, the verifier result and the swap result, and never a value from the copy.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01 | AC1, BR2, BR4, BR5 | Component | Test extract PII-SIT-20261120 with 28,119 accounts |
| TC-TE-004-02 | AC2, BR3 | Component | Injected value with a valid check digit in interaction row 4,512 |
| TC-TE-004-03 | AC3, BR4 | Component | case_account file with 28,118 rows |
| TC-TE-004-04 | AC4, BR1 | Component | Target environment DEV |
| TC-TE-004-05 | AC5 | Component | Extract loaded twice |
| TC-TE-004-06 | AC6, BR6 | Component | Manifest with MASK-2026.10 |
| TC-TE-004-07 | AC7 | Component | Two loads into SIT at once |
| TC-TE-004-08 | Access | End to end | SIT test user with RW-REFADM calls GET /cases/{caseId}; refused with MSG-P4-002 |
| TC-PLT-TE004-APP-09 | AC8, BR7 | Integration | The 19 schemas of SIT at the extract's version with one staging schema per service; one service's checks failed, then a service named by the extract with no schema and a missing schema |

The eight legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the loader and verifier checks TC-TE-004-01 to TC-TE-004-07 become Component, and the legacy Access row TC-TE-004-08 becomes End to end. TC-PLT-TE004-APP-09 is the new row for AC8. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same TC ID.

### 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance (DL26), the allowed environments are properties, and the lists the totals are counted by are reference rows read through the contract of rwb-case (DP-07).
- No personal data in logs, reports, tests or prompts: the load report and the `tools.masked_copy_load` row hold counts, totals, schema names and check names, never a value; test extracts are built from masked or synthetic data.
- ACE data only through the owner's contract or the `v_ace_*` views (DP-05): the loader reads the masked extract as a file, takes no ACE table directly, and where it needs ACE-sourced data it reads through the rwb-source-data contract.
- No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.
- No read of another service's schema and no cross-schema key: the loader resolves each table to one owning schema, writes only that schema's staging schema, and asks any other owner through its contract (DP-01).
- The tool never writes a live service schema outside the swap: a live schema changes only when PerServiceSchemaSwap renames into it after every service's checks have passed, and never row by row.
- The tool stays outside the ACE services and never becomes a runtime dependency of a service; it runs only in SIT and UAT (the legacy guardrail, kept).
- One refusal refuses the estate: a failure in any service means no swap anywhere and every previous copy stays in use.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, section 4; Program section 6.7 | None | All recovery processes | CTL-02, CTL-11; DL26 | TC-TE-004-01 to TC-TE-004-07, TC-PLT-TE004-APP-09 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Epic 1, section 4 | None | All recovery processes | CTL-11 | TC-TE-004-01, TC-TE-004-08, TC-PLT-TE004-APP-09 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | Each table of the extract goes into the schema of the service that owns it, and no second service's schema is read or written | TC-TE-004-01, TC-PLT-TE004-APP-09 |
| DP-05 | Template and Rules §R5.5; Arch v5 slides 29 and 41 | No ACE table is read directly; the personal-data field list comes through the rwb-source-data contract and the ACE views behind it | TC-TE-004-01, TC-TE-004-02 |
| DP-07 | Template and Rules §R5.5 | The environment lists and the product groups the manifest totals are counted by are read through the reference-data contract of rwb-case | TC-TE-004-01, TC-TE-004-03 |
| DP-08 | Template and Rules §R5.5; Arch v5 slides 14 and 35 | The load identity and the reading test user are authorised through the authorise contract of rwb-access, and a role without the right is refused with MSG-P4-002 | TC-TE-004-08 |
| DP-13 | Template and Rules §R5.5 | The endpoint a test user reads on the loaded copy is the per-service base path, not the monolith base; the load adds no path | TC-TE-004-08 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The test user reaches the case through the gateway-bff composite route, and the load provides no route of its own | TC-TE-004-08, TC-PLT-TE004-APP-09 |
| Arch v5 slide 29 | One login and one schema per service, no grant across schemas, no cross-schema keys, boundary test in every build | The per-service staging schema, the inside-a-schema foreign-key check and the swap-after-all-checks rule | TC-PLT-TE004-APP-09 |
| Arch v5 slide 35 | Personal data stays in the owning service, masked; deny by default | Every `is_personal` field of every staging schema is verified before any swap, and the copy never leaves SIT or UAT | TC-TE-004-02, TC-PLT-TE004-APP-09 |
| Arch v5 slides 20 and 41 | Each service writes its own schema, plus outbox and inbox; one owner per schema and its first path | The table-to-schema resolution and the per-service report | TC-PLT-TE004-APP-09 |
| NFR-045 | Synthetic in development, masked in user acceptance | The environment guard before any file is read, and no copy from SIT or UAT to another environment | TC-TE-004-04, TC-PLT-TE004-APP-09 |
| DL26 | The masking rules and their version are Compliance's | The version in force is compared with the manifest and is never a value in code; with no rule loaded every personal field is a token | TC-TE-004-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the authorise contract and the gateway-bff route contract this story builds against |
| RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P1-E1065-CON | Contract | C: the two service contracts consumed at run time and the source-data contract behind the personal-data field list |
| RWB-ITG-TE004-ITG | Integration | The integration copy of RWB-TE-004; it exercises this loader across the 19 schemas and owns none of it |
| RWB-PLT-NF06-DB and the per-service DB stories | DB | Related work outside this story: the 19 schemas, the 19 logins and the staging schemas of each environment |

### 19. Out of scope

- Synthetic data in DEV (RWB-E1-065 in the legacy numbering; RWB-P1-E1065-CON and the P1 stories behind it).
- The content of the masking rules, the values masked per field and per role, and their retention periods: Compliance owns them under DL26.
- Masking on the screens and the masking policy of a reader: rwb-access (P4) owns them, and `RWB-P4-E1037-CON` publishes the contract.
- The PII service itself, which the bank runs, and its extract contract, which is outside the source set.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).
- The integration copy of this legacy key, RWB-ITG-TE004-ITG, which exercises the loader end to end across the 19 schemas.
- The 19 schemas, the 19 logins and their grants: RWB-PLT-NF06-DB and the per-service database stories.
- The contents of `RWB-PLT-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON` and `RWB-P1-E1065-CON`; this story builds against them and adds no path.
