<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 010 Stage 2 data products contracts plans and treatments v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 010 Stage 2 data products contracts plans and treatments v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-010 Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-010 |
| Epic | E2, release 31 December 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-CHO-09 Build the stage 2 data products |
| Requirement IDs | REQ-RDF-014 |
| BRD section | Business Requirements Epic 2, section 3.1 (story) and section 4 (REQ-RDF-014) |
| L3 process | 07 Route, settle and claim |
| Decision | D6.4 to D6.6 |
| Priority | Should |
| Depends on | RWB-E2-004, RWB-E1-016, RWB-E1-015 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the stage 2 data products (treatments, plans, contracts and guarantees) added to the recovery data store with their systems of record**, so that **the settlement, TDR and DIL screens in Epic 3 read from one store**.

## 2. Business rationale

From Epic 3 the settlement, restructure and deed in lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place. The treatment record lives with the module that owns it (RWB-E2-004), plan terms come from the ACE restructure calculation, contract numbers come from ALS, and guarantee claims come from the guarantee module. A daily build of the DP04 Treatment product brings them into the data store with a catalog entry, a freshness stamp, access by role and checks that every row links to a case. Serves REQ-RDF-014: stage 2 data products exist before the first treatment goes live.

## 3. Preconditions

- RWB-E2-004 is done: the treatment entity exists and its module publishes TreatmentQuery (section 12).
- RWB-E1-016 is done: data_product_access and the data product read endpoint exist.
- RWB-E1-015 is done: freshness stamps and the stale check exist.
- RWB-E1-064 is done: data_product holds DP04 Treatment with system of record "Workbench" and owner RW-DATASTEW, and sys_fields holds treatment and guarantee_claim.
- data_product_access version "DPA-2026.12" gives DP04 read to RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT.
- The guarantee module publishes GuaranteeClaimQuery; before it is built (Epic 4), the interface returns no claims.

## 4. Flow

1. JOB-01: after the COLLINS load for business date D passes its checks, starts the stage 2 product step.
2. Stage2ProductService: calls TreatmentQuery.changedBetween(start of D, end of D) and receives the treatments created or changed on D, with plan terms from the ACE restructure calculation.
3. Stage2ProductService: calls GuaranteeClaimQuery.changedBetween() for guarantee claims changed on D.
4. Stage2ProductService: resolves each case's primary account through CaseScopeQuery and reads its contract number and contract date from loan_account.
5. Stage2ProductService: holds in the data quality exception list any row whose case does not resolve (check References), and writes the other rows to dp_treatment and dp_guarantee_claim keyed by record ID.
6. Stage2ProductService: compares the count of active treatments in dp_treatment with TreatmentQuery.countActive(); a difference holds the publish (DL25).
7. FreshnessStampService: on a match, writes the DP04 stamp for business date D.
8. Case owner or restructuring officer: reads DP04 for a case through GET /data-products/DP04/records?caseId=.
9. Data steward: reads the DP04 catalog entry and any breaks.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product | 403; refusal logged | MSG-P4-002 | AC3 |
| X2 | A guarantee claim names a case that does not exist | Claim held in the exception list with check References; retried with the next load | None | AC4 |
| X3 | TreatmentQuery is unavailable | Step fails; the previous DP04 rows and stamp stay; DP04 turns stale at its expected-by time | MSG-GEN-006, MSG-P1-001 | AC5 |
| X4 | The step runs again for the same business date | Rows replaced by record ID; no duplicate | None | AC6 |
| X5 | Active treatment counts differ | DP04 not stamped for D; break listed for the data steward | MSG-P1-002 | AC7 |
| X6 | A treatment changed at the end of business date D | Included in D; a change one second later goes to D+1 | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the treatment entity (RWB-E2-004), product access (RWB-E1-016) and freshness (RWB-E1-015); the guarantee interface may return no rows |
| Negotiable | Which roles read DP04 and the expected-by time are data rows; the story fixes the build, the link checks and the stamp |
| Valuable | The Epic 3 settlement, TDR and DIL screens read one checked store |
| Estimable | One job step, two read tables, two interface calls, one reconciliation |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments and claims through stub interfaces |

## 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments

  Background:
    Given business date 2026-12-14 and the COLLINS load for it passed its checks at 06:20
    Given the treatment module holds 40 active treatments, 12 of them restructure plans with installments from the ACE restructure calculation
    Given 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer

  Scenario: AC1 Products loaded
    Given treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer
    When the stage 2 step of JOB-01 runs
    Then dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and the contract number of the case's primary account
    Then DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED"
    Then the catalog entry for DP04 lists system of record "Workbench", owner RW-DATASTEW and the fields of treatment and guarantee_claim

  Scenario: AC2 Guarantee data
    Given 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht
    When the stage 2 step runs
    Then dp_guarantee_claim holds 5 rows, each linked to its case
    Then a read of DP04 for case "RW-2026-000512" returns its TCG claim with claim deadline 2027-02-28

  Scenario: AC3 Access
    Given user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row
    When the user calls GET /data-products/DP04/records?caseId=RW-2026-000512
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and product "DP04"

  Scenario: AC4 A guarantee claim for a case that does not exist
    Given a TCG claim names case ID "00000000-0000-0000-0000-000000000997"
    When the stage 2 step runs
    Then the system does not writ the claim to dp_guarantee_claim
    Then the data quality exception list holds it with product "DP04" and check "References"

  Scenario: AC5 The treatment interface is unavailable
    Given TreatmentQuery returns an error
    When the stage 2 step runs for 2026-12-14
    Then the step ends "FAILED" with MSG-GEN-006 for system "Treatment"
    Then dp_treatment keeps the rows for 2026-12-13
    Then the system flags at 08:00 DP04 stale with MSG-P1-001 "Treatment is from 2026-12-13. Today's load has not arrived."

  Scenario: AC6 A repeat run for the same date
    Given the stage 2 step completed for 2026-12-14 with 40 treatment rows
    When it runs again for 2026-12-14
    Then dp_treatment still holds 40 rows for 2026-12-14

  Scenario: AC7 Active treatment counts differ
    Given TreatmentQuery.countActive() returns 41 and the build produced 40 active rows
    When the count check runs
    Then the system does not stamp DP04 for 2026-12-14
    Then a break with check "Active treatment count 40 against 41" is listed for the data steward with MSG-P1-002

  Scenario: AC8 A change at the end of the business date
    Given treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When the stage 2 step runs for 2026-12-14
    Then "TRT-SYN-0601" is in the build for 2026-12-14
    Then "TRT-SYN-0602" is not
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds treatments, plan terms, contract references and guarantee claims, with one system of record and one owner | REQ-RDF-014; data_product DP04; sys_objects |
| BR2 | Every stage 2 row links to an existing case, or it is held in the exception list and retried with the next load | DQ load check "References" (ifspec.txt) |
| BR3 | The product is stamped for the day only when the active count matches the owning module, with zero tolerance | DL25; RWB-E1-011 hold rule (FEAT-RDF-13) |
| BR4 | A role reads DP04 only through an access row in force | data_product_access; REQ-RDF-010 |
| BR5 | Credit approval for a restructure is recorded on the case by the officer; there is no interface to NLEADS | INT-26; DL12 |
| BR6 | Plan installments come from the ACE restructure calculation | DF-TRT-009 source ACE; INT-34 |

## 9. State transitions

None. This story does not change a case status. It changes the DP04 freshness status (LOADED or STALE) and the state of the stage 2 step on the JOB-01 run (Complete or Failed).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs the stage 2 step, writes dp_treatment and dp_guarantee_claim, writes exceptions and the stamp |
| RW-DATASTEW, data steward | Owns DP04; reads the catalog entry and the breaks |
| RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD | Read DP04 for cases in scope |
| RW-COE, RW-AUDIT | Read DP04 for all cases |
| RW-PHONECOL and roles with no DP04 access row | May not read DP04 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-012 | treatment | booked_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Read |
| DF-TRT-022 | guarantee_claim | status | Read |
| DF-ACC-003 | loan_account | contract_no | Read |
| DF-ACC-007 | loan_account | contract_date | Read |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields | Write |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Write |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Write |

treatment and guarantee_claim fields are read through TreatmentQuery and GuaranteeClaimQuery, not from their tables. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | End of JOB-01 after the COLLINS load for business date D passes its checks |
| Job name | JOB-01 COLLINS load check and intake, stage 2 product step |
| Schedule | Daily, after the COLLINS load, before 07:00 (NFR-013) |
| Input | Treatments and guarantee claims changed on D through the published interfaces; contract number and date of each case's primary account |
| Output | dp_treatment and dp_guarantee_claim rows for D; exceptions with check References; DP04 freshness stamp; count check result on the job run |
| Events published | None |
| Idempotency key | Record ID and business date; a rerun replaces the rows for D |
| Restart behavior | The step writes in one transaction per product table; a failure leaves the previous day's rows; rerun from the job monitor with POST /admin/jobs/{jobId}/rerun |

**Published interfaces used**

```java
// Treatment module (RWB-E2-004)
public interface TreatmentQuery {
    List<TreatmentView> changedBetween(OffsetDateTime from, OffsetDateTime to);
    long countActive();
}

// Guarantee module (S3); returns an empty list until Epic 4
public interface GuaranteeClaimQuery {
    List<GuaranteeClaimView> changedBetween(OffsetDateTime from, OffsetDateTime to);
}

// P3 (RWB-E1-016), service call without a user scope
CaseLinks CaseScopeQuery.linksInScope(UUID caseId, UserContext systemContext);
```

**Endpoints used**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/data-products/{productCode}/records | Read DP04 for a case (RWB-E1-016) | Case record, R, plus a DP04 access row | 403 (MSG-P4-002); 404 (MSG-P4-003); 503 (MSG-GEN-006) |
| GET /api/recovery/v1/admin/data-quality/exceptions | Read DP04 References exceptions and breaks | Platform administration, R | 401; 403; 503 |
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Rerun the failed step | Platform administration, U | 404; 409 (MSG-P2-006) |

## 13. Solution plan

- Package: folder `recovery/dataengine/stage2`, Java package `recovery.dataengine.stage2`.

| Component | Type | Responsibility |
|---|---|---|
| Stage2ProductStep | Job | The stage 2 step of JOB-01 |
| Stage2ProductService | Service | Reads changes through the interfaces, resolves contracts, checks links, writes rows, runs the count check |
| DpTreatmentRepository, DpGuaranteeClaimRepository | Repository | Upsert by record ID and business date |
| DpTreatment, DpGuaranteeClaim | Entity | One row per record and business date |
| DP04 access rows | Rule table | data_product_access rows for DP04, version DPA-2026.12 |

- Database: tables dp_treatment and dp_guarantee_claim (new, Flyway migration in this story). dp_treatment mirrors the 14 treatment fields and adds business_date date, contract_no varchar(20), contract_date date; dp_guarantee_claim mirrors the 8 guarantee_claim fields and adds business_date date; both carry the standard columns, a unique key (record ID, business_date) and an index on case_id. Writes data_product_load for DP04 (RWB-E1-015) and exceptions (RWB-E1-006). Reads loan_account (P1).
- Configuration and reference data: DP04 row in data_product with expected-by 08:00 (assumed; DL11); DP04 access version DPA-2026.12 prepared by the data steward and loaded by the reference data administrator; dictionary rows for dp_treatment and dp_guarantee_claim added to sys_fields with the migration.
- Build steps:
  1. Flyway migration for dp_treatment and dp_guarantee_claim, with their sys_objects and sys_fields rows under DP04.
  2. Stage2ProductService reading changes for D through TreatmentQuery and GuaranteeClaimQuery; the business date window is [start of D, start of D+1).
  3. Contract resolution through CaseScopeQuery and loan_account.
  4. Link check with the References exception, and upsert of the other rows.
  5. Count check against countActive(); hold the stamp on a difference.
  6. Stamp DP04 through FreshnessStampService on a match.
  7. Stage2ProductStep wired into JOB-01 after the load checks.
  8. Tests for AC1 to AC8 with stub interfaces, and the access test.
- Feature flag: `rwb.dataengine.stage2-products`.
- Done when: the tests in section 16 pass and the DP04 catalog entry shows in GET /admin/data-products in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | Role without a DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | DP04 stale after a failed step | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Count check break held the publish | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | TreatmentQuery or GuaranteeClaimQuery unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-01 is running | {job} is already running. Wait for it to finish before you rerun it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-45 Data quality (Epic 2): state Loading while the list arrives; state Breaks shows DP04 References exceptions and count breaks for the data steward. The case record view SCR-03 shows DP04 data for roles with access. The settlement, TDR and DIL screens that use DP04 come in Epic 3.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-010-01 | AC1, BR1, BR5, BR6 | System | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | AC2, BR1 | System | 5 TCG claims for existing cases |
| TC-E2-010-03 | AC3, BR4 | System | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | AC4, BR2 | System | TCG claim for an unknown case ID |
| TC-E2-010-05 | AC5 | System | TreatmentQuery stub returning errors |
| TC-E2-010-06 | AC6 | System | Step run twice for 2026-12-14 |
| TC-E2-010-07 | AC7, BR3 | System | countActive() 41 against 40 rows |
| TC-E2-010-08 | AC8 | System | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Access | Access | RW-TRIBE calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: access, expected-by time and tolerance are data rows or decisions (DL25).
- No personal data in logs, tests or prompts: treatment and claim rows carry amounts and codes; test data is synthetic.
- No read of another module's tables: treatments and claims come through TreatmentQuery and GuaranteeClaimQuery; case links through CaseScopeQuery.
- No call to NLEADS or the Thai Credit Guarantee Corporation; their results arrive as recorded on the case.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-01 to TC-E2-010-08 |

## 19. Out of scope

- The treatment entity and its plan timers (RWB-E2-004).
- The credit approval pack for NLEADS (RWB-E2-006) and booking confirmation from the ALS load (RWB-E2-007).
- Settlement, TDR and DIL screens (Epic 3).
- Guarantee claim filing and the claim deadline timers (S3, Epic 4).
