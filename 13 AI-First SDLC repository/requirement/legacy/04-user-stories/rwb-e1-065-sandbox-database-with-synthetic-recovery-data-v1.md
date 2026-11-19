<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 065 Sandbox database with synthetic recovery data v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 065 Sandbox database with synthetic recovery data v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-065 Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-065 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Requirement IDs | REQ-RDF-001, REQ-RDF-010 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-001, REQ-RDF-010); Business Requirements Program, section 6.7 (NFR-045) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **Tribe lead and squad member (RW-TRIBE)**, I want **a sandbox database holding synthetic recovery data**, so that **I can build and test before the real interfaces are available**.

## 2. Business rationale

The COLLINS loads, the file loads and the masked SIT copy are not available when the squads start on 2 November, and NFR-045 forbids production data in development. A sandbox in DEV built from the same Flyway migrations as the recovery schema, filled by a seeded generator with synthetic cases across Mortgage, Hire Purchase and SSME and the exception shapes the rules must handle, lets every squad build and test from the first day. The generator reads the data dictionary, so a schema change reaches the sandbox with no manual rebuild. Serves REQ-RDF-001 (the 14 data products in one schema) and REQ-RDF-010 (no personal data outside its permitted use).

## 3. Preconditions

- RWB-E1-001 is done: the Flyway migrations create the recovery tables, sys_objects, sys_fields and the seed lists of values.
- A PostgreSQL database `rwb_sandbox` exists in DEV with schema `recovery`, reachable from the pipeline.
- The Entra ID group RWB-DEV-RW-TRIBE exists and maps to the sandbox read-only database role.
- The role to permission matrix rows (roles.txt, Permissions) are available as a seed file for the sandbox.
- The ACE service can be deployed in DEV against the sandbox database.

## 4. Flow

1. Pipeline: on a merge to main that changes a recovery Flyway migration, or on a manual start, runs the sandbox build stage in DEV.
2. Pipeline: drops and recreates schema `recovery` in `rwb_sandbox` and applies every Flyway migration.
3. SandboxGenerator: reads sys_objects, sys_fields and lov_value from the sandbox to learn every table, column, type and list.
4. SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions.
5. SandboxGenerator: adds 10 cases for each exception shape in section 8, BR4.
6. SandboxGenerator: loads the 54 roles, the permission matrix and one named test user per role.
7. SandboxVerifier: checks every table has rows, every LOV column holds list values, every foreign key resolves and no value matches a personal data pattern.
8. Pipeline: grants SELECT on schema `recovery` to role `rwb_sandbox_read` and publishes the build result with the row count per table.
9. Developer or analyst: queries the sandbox with SQL or the export script, or calls the DEV service, without a request to another team.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the migrations and the metadata tables from RWB-E1-001 |
| Negotiable | Volumes, seed and exception shapes are properties; the story fixes the generator, the checks and the access |
| Valuable | Every squad builds and tests from the first day with no production data |
| Estimable | One generator tool, one verifier, one pipeline stage, one database role |
| Small | Finished inside two weeks with its tests |
| Testable | The test cases in section 16 query the built sandbox |

## 7. Acceptance criteria

No business acceptance criteria. This story is an engineering enabler for the synthetic sandbox database; its development-process criteria were removed on 4 November 2026.

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; the sandbox holds synthetic data only | NFR-045; CTL-11 |
| BR2 | The sandbox schema comes from the same Flyway migrations as every other environment | RWB-E1-001; ADR-001 |
| BR3 | Generated values come from the data dictionary and the lists of values, not from code | sys_fields; lov_value; Principle 1 |
| BR4 | Exception shapes generated: duplicate case for one customer and product (R-UNI-17), deceased customer (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) | rules.txt; DL16 |
| BR5 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent | DL15 |
| BR6 | Every role has a named test user before it has real users | DL39 |

## 9. State transitions

None. This story does not change a case status. It changes the sandbox build state in the pipeline: Building, Published or Failed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Read and extract the sandbox through role `rwb_sandbox_read`; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database and the pipeline stage |
| Test users per role | Call the DEV service against the sandbox with their role's rights |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-CAS-036 to DF-CAS-045 | deviation | all fields | Write |
| DF-PTY-001 to DF-PTY-012 | party | all fields | Write |
| DF-PTY-013 to DF-PTY-020 | contact_point | all fields | Write |
| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Write |
| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Write |
| DF-COL-001 to DF-COL-013 | collateral | all fields | Write |
| DF-COL-014 to DF-COL-017 | account_collateral | all fields | Write |
| DF-COL-018 to DF-COL-027 | valuation | all fields | Write |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-DEC-019 to DF-DEC-027 | score | all fields | Write |
| DF-REF-034 to DF-REF-039 | role | all fields | Write |
| DF-REF-040 to DF-REF-044 | permission | all fields | Write |
| DF-REF-027 | lov_value | id | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-REF-097 | sys_fields | field_name | Read |
| DF-REF-098 | sys_fields | data_type | Read |
| DF-REF-105 | sys_fields | is_personal | Read |

The other entity tables in the Logical Data Model are filled the same way from their sys_fields rows. decision_log_entry is not generated: entries come from running the Workbench jobs against the sandbox. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Merge to main that changes a file under the recovery Flyway migration folder; manual start by RW-TRIBE or RW-PLATADM |
| Job name | Sandbox build, a DEV pipeline stage; not a scheduled job and not in the production job list (batch.txt) |
| Schedule | On trigger only |
| Input | Flyway migrations; sys_objects, sys_fields and lov_value after migration; role and permission seed file; properties in section 13 |
| Output | Schema `recovery` in `rwb_sandbox` with synthetic rows; build report with row count per table and the verifier result |
| Events published | None |
| Idempotency key | Commit hash and seed. The same pair produces the same rows |
| Restart behavior | The build works on a staging schema `recovery_next` and swaps it for `recovery` only after the verifier passes; a failed build leaves the previous sandbox |

**Endpoint used in DEV against the sandbox**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/cases | A test user lists sandbox cases in scope | Case record, R | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 |

## 13. Solution plan

- Package: folder `tools/sandbox-generator`, Java package `recovery.tools.sandbox`, built as a separate build module that is not packaged into the ACE service.

| Component | Type | Responsibility |
|---|---|---|
| SandboxGenerator | Service | Reads the metadata and writes synthetic rows table by table in foreign key order |
| ValueFactory | Service | Produces a value per data type and list, seeded; synthetic names as "SYN-FIRST-000123"; tokens as random 64-character hex |
| ExceptionShapeBuilder | Service | Adds the shapes in BR4, 10 cases each |
| SandboxVerifier | Service | Row, list, key and personal data pattern checks |
| AccessSeedLoader | Service | Loads 54 roles, the permission matrix and one test user per role |
| SandboxExport | Service | Writes a table to CSV for the read-only role |
| Sandbox build stage | Job | Pipeline stage: migrate staging schema, generate, verify, swap, grant |

- Database: no new recovery table. The stage creates schema `recovery_next`, applies the Flyway migrations, fills it, renames it to `recovery` after the check, and grants SELECT to role `rwb_sandbox_read` mapped to RWB-DEV-RW-TRIBE. The pipeline holds a PostgreSQL advisory lock for the whole build.
- Configuration and reference data: properties `rwb.sandbox.seed=20261128`, `rwb.sandbox.cases.mortgage=1226`, `rwb.sandbox.cases.hire-purchase=1296`, `rwb.sandbox.cases.ssme=290`, `rwb.sandbox.shape-count=10`, owned by the tech lead; lists of values from the seed migration; roles and permissions from the roles.txt seed file.
- Build steps:
  1. Metadata reader over sys_objects, sys_fields and lov_value with foreign key order from the relationships.
  2. ValueFactory per data type and list, seeded; a column with no sys_fields row fails the build.
  3. SandboxGenerator for the case volumes with linked accounts, parties, contact points, collateral, valuations, payments and interactions.
  4. ExceptionShapeBuilder for the shapes in BR4.
  5. AccessSeedLoader with a test user per role.
  6. SandboxVerifier: rows per table, list values, foreign keys, personal data patterns (national ID with check digit, mobile number, email).
  7. Pipeline stage with staging schema, swap, grant and lock.
  8. Tests on the sandbox and the access test.
- Feature flag: `rwb.dataengine.sandbox` (enables the DEV profile that points the service at `rwb_sandbox`).
- Done when: the tests in section 16 pass and squads use the sandbox in DEV.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the right calls the DEV service | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |

Build failures are reported in the pipeline result with the table and column named; no user message applies.

## 15. Screens and states

No screen in this story. Developers and analysts read the sandbox with SQL and the export script, and see the build result and row counts in the pipeline. Screens built in DEV show sandbox cases through the normal endpoints.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | BR4, BR5 | System | Seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-03 | BR3 | System | Test migration adding recovery_case.risk_tier with its dictionary row |
| TC-E1-065-04 | BR3 | System | Test migration adding loan_account.note_x with no dictionary row |
| TC-E1-065-07 | BR1 | System | Injected 13-digit value with a valid check digit in party.id_no_token |
| TC-E1-065-08 | BR4 | System | Boundary accounts at 89 and 90 days past due |
| TC-E1-065-10 | Access | Access | Test user with RW-REFADM calls GET /cases on the sandbox; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: volumes, seed and shape counts are properties; values come from the dictionary and the lists.
- No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks values that look real.
- No read of another module's tables at runtime: the generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production.
- The sandbox is in DEV only; no copy goes to another environment.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | R-UNI-17, R-UNI-05, R-UNI-07, R-UNI-20, R-UNI-10; DL15, DL16 | TC-E1-065-01 to TC-E1-065-06, TC-E1-065-08, TC-E1-065-09 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, sections 3.1 and 4; Program section 6.7 | None | All recovery processes | CTL-11 | TC-E1-065-07 |

## 19. Out of scope

- Masked copies of production data in SIT and UAT (RWB-TE-004).
- The rule table test harness (RWB-TE-005) and the performance test harness (RWB-TE-009).
- The PDPA lint for code, tests and logs (RWB-TE-011).
- Real loads from COLLINS and the file interfaces (RWB-E1-003, RWB-E1-004, RWB-E1-007).
