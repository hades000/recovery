<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 004 Masked data in SIT and UAT v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 004 Masked data in SIT and UAT v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-004 Masked data in SIT and UAT

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-004 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Epic 1, section 4 (REQ-RDF-010, REQ-ACA-005); Business Requirements Program, section 6.7 (NFR-045) |
| L3 process | All recovery processes |
| Decision | DL26 |
| Priority | Must |
| Depends on | RWB-E1-065 |
| Status | Ready for build |

## 1. Story

As a **Tribe lead and squad member (RW-TRIBE)**, I want **masked copies of recovery data loaded into SIT and UAT from the PII service**, so that **tests run on realistic volumes without exposing customers**.

## 2. Business rationale

SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development. The bank's PII service produces the masked copy under the Compliance masking rules; this story loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps balances, dates and keys unchanged so counts and reconciliations behave as in production. Serves REQ-RDF-010 and REQ-ACA-005; decision DL26 sets the masking rules.

## 3. Preconditions

- RWB-E1-065 is done: the generator's personal data pattern checks and the sys_fields is_personal tags are available to the loader.
- The PII service delivers a masked extract per environment to the SIT or UAT intake container, with a manifest: extract ID, business date, masking rule version, row count and balance totals per table.
- The masking rule version in force is held in the masking rules reference table (DL26; until Compliance supplies the rules, every is_personal field is replaced by a token).
- The SIT and UAT databases hold the recovery schema at the same Flyway version as the extract.
- The platform administrator (RW-PLATADM) starts the load; squad members hold RW-TRIBE.

## 4. Flow

1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment.
3. MaskedCopyLoader: refuses to run when the target environment is DEV or PROD.
4. MaskedCopyLoader: checks the manifest: extract ID not loaded before, masking rule version equal to the version in force, schema version equal to the target.
5. MaskedCopyLoader: runs the load checks of CTL-02 on each file: business date, structure, control totals (row count and balance sum), keys.
6. MaskingVerifier: scans every column tagged is_personal for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.
7. MaskedCopyLoader: loads the files into a staging schema, checks foreign keys resolve, and swaps the staging schema for the live one in one step.
8. MaskedCopyLoader: writes the load report: extract ID, business date, masking rule version, rows and balance totals per table, check results.
9. Squad member: runs SIT or UAT tests on the masked copy.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal | Load refused in full; previous copy stays | MSG-P1-002 | AC2 |
| X2 | Row count or balance total differs from the manifest | Load refused in full; previous copy stays | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC4 |
| X4 | The same extract ID is loaded again | Load skipped; report shows the earlier load | None | AC5 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC6 |
| X6 | A second load starts while one runs | Second start refused | MSG-P2-006 | AC7 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the personal data checks from RWB-E1-065 and the PII service extract; no screen |
| Negotiable | Masking rules belong to Compliance (DL26); the story fixes the checks and the load |
| Valuable | SIT and UAT run at production volume with no customer data exposed |
| Estimable | One loader, one verifier, one pipeline stage |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on a test extract with a manifest |

## 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 loan accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with total_balance sums per product

  Scenario: AC1 Masked copy
    Given a masked copy from the PII service
    When it is loaded into SIT
    Then every column tagged is_personal in party and contact_point holds a token or a masked value
    Then balances keep their shape: the count and the total_balance sum per product equal the manifest
    Then each party token joins to the same case_party and loan account rows as in the extract

  Scenario: AC2 A personal value left in the copy
    Given party row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in id_no_token
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in party.id_no_token"
    Then the previous SIT copy stays in use

  Scenario: AC3 Totals that do not match the manifest
    Given the loan_account file holds 28,118 rows
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals loan_account 28,118 against 28,119"

  Scenario: AC4 A copy aimed at DEV
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file

  Scenario: AC5 The same extract twice
    Given extract "PII-SIT-20261120" was loaded into SIT on 2026-11-20
    When it is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20

  Scenario: AC6 A masking rule version that is not in force
    Given a manifest with masking rule version "MASK-2026.10"
    When the copy is loaded into UAT
    Then the system refuses the load in full with MSG-P1-002 and check "masking rule version MASK-2026.10 is not in force"

  Scenario: AC7 A second load while one runs
    Given a masked copy load into SIT is running
    When a second load into SIT starts
    Then the system refuses the second load with MSG-P2-006
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force | Masking rules reference table; DL26; sys_fields.is_personal |
| BR3 | A copy with any personal value left in it is refused in full | CTL-11; DQ check "Refuse the load" |
| BR4 | Balances, dates and keys are not masked; counts and totals equal the manifest | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table, so joins hold | Mapping rule "Personal data" (s2t.txt) |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |

## 9. State transitions

None. This story does not change a case status. It changes the masked copy load state in the pipeline: Running, Loaded, Refused or Skipped.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT; owns the intake containers |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26) |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights |
| SY-DATALOAD, data load | Identity the loader runs under in SIT and UAT |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PTY-001 to DF-PTY-012 | party | all fields | Write |
| DF-PTY-013 to DF-PTY-020 | contact_point | all fields | Write |
| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Write |
| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Write |
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-REF-105 | sys_fields | is_personal | Read |

The other recovery tables in the extract load the same way. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Manual start by the platform administrator for SIT or UAT after the PII service delivers an extract |
| Job name | Masked copy load, a SIT and UAT pipeline stage; not a scheduled job and not in the production job list (batch.txt) |
| Schedule | On request |
| Input | Masked extract files and manifest from the PII service in the environment's intake container |
| Output | Recovery schema in SIT or UAT replaced by the masked copy; load report with extract ID, business date, masking rule version, rows and totals per table and the check results |
| Events published | None |
| Idempotency key | Extract ID; a repeat is skipped |
| Restart behavior | Files load into staging schema `recovery_next`; the swap happens only after every check passes, so a failure leaves the previous copy |

**Endpoint used in SIT on the loaded copy**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId} | A test user reads a masked case | Case record, R, scope applied | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 503 |

## 13. Solution plan

- Package: folder `tools/masked-copy-loader`, Java package `recovery.tools.maskedcopy`, built as a separate build module that is not packaged into the ACE service.

| Component | Type | Responsibility |
|---|---|---|
| MaskedCopyLoader | Job | Spring Batch job: environment guard, manifest checks, file load to staging, swap |
| ManifestValidator | Service | Extract ID, masking rule version, schema version, control totals |
| MaskingVerifier | Service | Personal value patterns on every is_personal column; reuses the RWB-E1-065 verifier |
| LoadReportWriter | Service | Writes the load report for the pipeline |
| Masked copy stage | Job | Pipeline stage for SIT and UAT with a lock per environment |

- Database: no new recovery table. The stage loads into schema `recovery_next` in SIT or UAT and renames it to `recovery` after the checks; an advisory lock per environment prevents two loads at once; a small table `masked_copy_load` in the tool's own schema `tools` records extract ID, environment, business date, masking rule version and result.
- Configuration and reference data: properties `rwb.maskedcopy.allowed-environments=SIT,UAT`, `rwb.maskedcopy.intake-container` per environment (platform administrator); masking rule version from the masking rules reference table (Compliance, DL26).
- Build steps:
  1. Environment guard reading the deployment environment; refuse DEV and PROD.
  2. ManifestValidator with the extract ID check against `tools.masked_copy_load`.
  3. File load into `recovery_next` with the CTL-02 checks and the manifest totals.
  4. MaskingVerifier on every is_personal column, reusing the RWB-E1-065 patterns.
  5. Foreign key check, swap and load report.
  6. Pipeline stage with the per-environment lock.
  7. Tests for AC1 to AC7 on a test extract, and the access test in SIT.
- Feature flag: `rwb.dataengine.masked-copy`.
- Done when: the tests in section 16 pass and the first masked copy is in SIT before the Epic 1 SIT run.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator and the squads read the load report in the pipeline. Test users see the masked copy through the normal SIT and UAT screens, with personal fields shown as tokens or masked values.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01 | AC1, BR2, BR4, BR5 | System | Test extract PII-SIT-20261120 with 28,119 accounts |
| TC-TE-004-02 | AC2, BR3 | System | Injected value with a valid check digit in party row 4,512 |
| TC-TE-004-03 | AC3, BR4 | System | loan_account file with 28,118 rows |
| TC-TE-004-04 | AC4, BR1 | System | Target environment DEV |
| TC-TE-004-05 | AC5 | System | Extract loaded twice |
| TC-TE-004-06 | AC6, BR6 | System | Manifest with MASK-2026.10 |
| TC-TE-004-07 | AC7 | System | Two loads into SIT at once |
| TC-TE-004-08 | Access | Access | SIT test user with RW-REFADM calls GET /cases/{caseId}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance; allowed environments are properties.
- No personal data in logs, tests or prompts: the load report holds counts, totals and check names, never a value; test extracts are built from synthetic data.
- No read of another module's tables at runtime: the loader is a tool outside the ACE service and runs only in SIT and UAT.
- No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, section 4; Program section 6.7 | None | All recovery processes | CTL-02, CTL-11; DL26 | TC-TE-004-01 to TC-TE-004-07 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Epic 1, section 4 | None | All recovery processes | CTL-11 | TC-TE-004-01, TC-TE-004-08 |

## 19. Out of scope

- Synthetic data in DEV (RWB-E1-065).
- The masking rule values per field and role (DL26, Compliance) and masking on screens (RWB-E1-037).
- The PII service itself, which the bank runs.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).
