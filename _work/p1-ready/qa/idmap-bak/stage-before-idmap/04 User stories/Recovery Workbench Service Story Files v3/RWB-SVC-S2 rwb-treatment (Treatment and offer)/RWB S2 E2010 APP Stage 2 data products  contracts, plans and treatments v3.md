# RWB-S2-E2010-APP Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6. Applied the follow-up v9 citation corrections. Backfilled 8 mapped v9 test case IDs.
- `Stage2ProductWorkflow` is started as a child of `AceIngestCheck` after the ALS stamp, not by consuming `AceDataReady` (RD-P1-003 as amended, RD-P1-040).

**Change log.** D-RCV-60, 22 November 2026: the secondary slice of RWB-E2-010 for rwb-treatment. The in-process `TreatmentQuery.changedBetween` and `countActive` of the legacy stage 2 step become two read operations on `/api/recovery/treatment/v1` with a mock and a 2 s timeout (DP-11, DP-13), reading `rwb_treatment` only (DP-01) and labelling every code from the reference data of the day (DP-07); the contract number, contract date and plan terms are neither stored nor read here (DP-05); the window is driven by the event-started `Stage2ProductWorkflow` of rwb-source-data, so this service owns no job and no schedule for it (DP-10); the read is additive on one Flyway version of this service (DP-15) and the screens are composed by gateway-bff (DP-19). No legacy acceptance criterion is carried: AC1 to AC8 and TC-S2-E2010-APP-12 to TC-E2-010-09 stay with RWB-P1-E2010-APP, the primary slice (GAP-2695). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 21 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S2-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E2010-CON, RWB-S2-E2010-CON |
| Contract version | /v1 path version; the exact contract version is Not specified in the source documents (DOR-RWB-S2-E2010-APP-23) |
| Readiness decisions | RD-P1-003, RD-P1-004, RD-P1-040 |
| Integration dependencies | None |
| Screens | None owned here; SCR-03 and SCR-45 are composed by gateway-bff (DP-19); SCR-14 is unaffected |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-RDF-014, REQ-RDF-010) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **recovery developer on the treatment service (RW-TRIBE)**, I want **the treatment side of the stage 2 data product: a changed-window read and an active-count read on `/api/recovery/treatment/v1` that hand the DP04 build of rwb-source-data exactly the treatment facts DP04 holds — the case, the treatment type, the approval level, the installments, the outcome and the plan facts — over a half-open business-date window, with every code labelled from the reference data of the day, and with no contract number, contract date, plan or account ever stored or read in this service**, so that **the stage 2 product is built from the service that owns the treatment record, the settlement, restructure and deed-in-lieu screens read one checked place, and nothing is copied out of ACE**.

This story is the secondary slice of legacy RWB-E2-010 and the treatment half of the split. It owns:

- the changed-window read `GET /treatments` and the active-count read `GET /treatments/active-count` on base `/api/recovery/treatment/v1` (DP-13), which replace the in-process `TreatmentQuery.changedBetween` and `countActive` of the legacy stage 2 step with a contract and a fake (DP-11);
- the DP04 field set the answer carries from the `treatment` row, with the reference-data version of every list (DP-01, DP-07);
- one Flyway version on this service's own sequence that adds the index the window read needs and changes no applied version (DP-15);
- the scope and right rule of the two reads, and the statement that the contract and plan facts are not this service's to serve (DP-05).

It does not own: the eight legacy acceptance criteria and the nine legacy test cases, the `dp_treatment` and `dp_guarantee_claim` copies, the link check, the count check, the DP04 freshness stamp, the break list, the catalog entry and the rerun, which are RWB-P1-E2010-APP and its contract RWB-P1-E2010-CON; the treatment entity, its write path and the plan timers, which are RWB-S2-E2004-APP; the guarantee claim facts, which are RWB-S3-E2010-APP; the contract number, contract date and plan terms, which stay in `recovery.v_ace_account` and `recovery.v_ace_plan`; the screens and their composite routes (DP-19); the deployment of the read (RWB-P1-E2010-OPS covers the build that calls it).

### 2. Business rationale

From Epic 3 the settlement, restructure and deed-in-lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place (REQ-RDF-014), read only through a data-product access row (REQ-RDF-010). The target keeps two things apart that the legacy step held together: the live treatment record stays with S2 in `rwb_treatment`, and the dated DP04 copy stays with P1 as the data engine, built from the live facts and read-only for reporting (DP-01).

The legacy step called the treatment module in process, so the copy and the record moved together. In the target the copy is built by `Stage2ProductWorkflow` of rwb-source-data, which asks the owner over one contract for the treatments changed in the business-date window and for the number of active treatments it reconciles against (DP-10, DP-11). Nothing of ACE crosses that seam: the contract number, the contract date and the plan terms are read by rwb-source-data from the `v_ace_*` views at request time, never copied and never re-exposed here (DP-05).

What is left to S2 is a narrow read with three duties: the boundary the legacy step used (a change at 23:59:59 belongs to the day, one second later to the next), the field set DP04 holds for a treatment, and a count whose rule is data, not code (BR4). The volumes do not change: about 3,000 restructure accounts a month reach the restructure process (NFR-005), and every treatment of the day must be in the copy before the Epic 3 screens open.

### 3. Preconditions

- RWB-P1-E2010-CON is published: it declares the DP04 record read and the page shape the DP04 build answers with, and this story builds the two reads against its fake, so the dependency never blocks (Contract dependency; DP-11).
- The two reads are published on this service's base, because the `treatment` table and its REST owner are S2's, although RWB-P1-E2010-APP names the changed window and the active count under the case contract of RWB-P3-E2004-CON; the assumption and the conflict row are ASM-4458 and GAP-2695, and the consumer adapts its fake, not its logic, if the conflict is resolved the other way.
- The `treatment` table of schema `rwb_treatment` exists with DF-TRT-001 to DF-TRT-033 and the seven standard record columns of TSD S2 T3.0, and this service's Flyway sequence is at the version that carries the platform library tables; the Work Package lists no build dependency, so the table and the platform libraries are taken as present (ASM-4461; DP-01, DP-15).
- The reference-data read of rwb-case for LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME reaches the service through the client library, with a version and a fake (DP-07).
- The platform guard library that answers a role's right on a capability area is on the service template, so the two reads declare the right "Treatment and offer R" and nothing else (ASM-4461).
- The gateway-bff composite route that serves SCR-03 Case record from the case read and this service's reads is published; no screen calls this service directly (DP-19; RWB-PLT-N001-CON).
- The active-state rule of the count read is a parameter row of the parameters contract of rwb-case, with its version, and no local constant (ASM-4459; DP-07 for the lists, DP-11 for the read).
- Feature switch `rwb.treatment.stage2-read` exists; its default is off in the non-production environments until the DP04 build of rwb-source-data is wired to the operation (ASM-4461).

### 4. Flow

1. The `snapshot(page)` activity of `Stage2ProductWorkflow` in rwb-source-data calls `GET /treatments?changedFrom=<start of D>&changedTo=<start of D+1>&page=1&size=<page size>` on base `/api/recovery/treatment/v1`, one hop, 2 s timeout (DP-10, DP-11, DP-13).
2. The controller refuses an empty or inverted window, a page below one and a size above the declared maximum before a statement runs (X1, X2). The declared maximum page size and the answer to an empty window are Not specified in the source documents (GAP-2696).
3. The guard answers the right "Treatment and offer R" for the caller; a role without it is refused, and a service identity is authorised by its own right row (X3; rights are data).
4. The read selects from `treatment` of `rwb_treatment` only, where `updated_at` is at or after `changedFrom` and strictly before `changedTo`, ordered by `updated_at` and `id`, and cuts the requested page (DP-01, DP-15).
5. `TreatmentFactsAssembler` builds the DP04 field set: the treatment and case IDs, the type, the proposer, the proposed date, the offer and haircut amounts, the installments, the validity date, the approval level, the booked date, the outcome and its date, the first due date, the installment amount, the installments paid and the shortfall.
6. `ReferenceLabelResolver` answers each label with the version of the reference data of the day and stamps that version on the page; a missing version fails the page rather than answering a bare code (X6; DP-07). The reference-data read path is Not specified in the source documents (GAP-2696).
7. The answer carries the items, the window, `page`, `size` and a `total` computed with the caller's scope applied, and the consumer asks for the next page until `total` is reached.
8. The consumer then calls `GET /treatments/active-count` and compares the number with the active rows it wrote for D; the zero-tolerance hold on a difference is its decision and is not taken here (BR6).
9. Both reads write nothing — no row, decision record, outbox row or state change — and a repeat of the same request returns the same page (BR8).
10. No ACE view and no other service is called on this path: the contract and plan facts are named by the DP04 answer of rwb-source-data, not by this service (DP-05).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `changedFrom` or `changedTo` is missing, or the window is empty or inverted | 400; no statement runs and no partial page is returned | MSG-GEN-001 | AC1 |
| X2 | `page` below one, or `size` above the declared maximum | 400 with the accepted range named | MSG-GEN-003 | AC4 |
| X3 | A role without Treatment and offer R, or a caller outside the scope of the rows | 403; the refusal is logged with the role and the operation, and no row is disclosed | MSG-P4-002 | AC5 |
| X4 | A page of a multi-page scan is requested while a treatment of the window is being changed | The changed row appears once, under its later `updated_at`, and no row is repeated across pages | None | AC4 |
| X5 | The treatment store or the connection pool is unavailable | 503; the consumer's step fails on its side and the copy of the day is not stamped | MSG-GEN-006 | AC7 |
| X6 | The reference-data version of a list cannot be resolved | 503; the page is not answered with unversioned codes | MSG-GEN-006 | AC7 |
| X7 | A caller asks this service for a contract number, a contract date or a plan term | No such field exists in the answer and the request is refused as an unsupported query parameter | MSG-GEN-001 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1: the table is in this service's schema, the reference data arrives through a fake and the DP04 contract is faked; no live rwb-source-data, rwb-case or ACE view is needed |
| Negotiable | The operation names, the page shape, the index name, the parameter name of the active rule and the flag are this story's choice; the field set, the half-open window, the rights and the messages are fixed |
| Valuable | The stage 2 product is built from the owner of the treatment record, with no copy of a contract, a plan or an account |
| Estimable | One controller, two read services, one assembler, one reference-label resolver, one index, one migration |
| Small | Fits one sprint with its tests |
| Testable | Each criterion of section 7 is one automated test on the window boundary, the field set, the count, the paging, the right or the absence of a foreign fact |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments, the treatment side

  Background:
    Given business date 2026-12-14 and the treatments of the day are in schema rwb_treatment
    Given 40 active treatments, 12 of them restructure plans, and 9 of the 12 plans carry a credit approval recorded on the case
    Given LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME are reference data with version "REF-2026.12"

  Scenario: AC1 The changed-window read returns exactly the treatments of the half-open business-date window (new, D-RCV-60)
    Given the rwb-source-data contract mock returns a DP04 page request for business date 2026-12-14
    Given treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When GET /api/recovery/treatment/v1/treatments?changedFrom=2026-12-14T00:00:00+07:00&changedTo=2026-12-15T00:00:00+07:00 is called
    Then the page carries "TRT-SYN-0601" and does not carry "TRT-SYN-0602"
    Then the same read with changedFrom=2026-12-15T00:00:00+07:00 carries "TRT-SYN-0602" and does not carry "TRT-SYN-0601"
    Then no treatment of the two windows is returned by both, and a row is never returned twice in one scan

  Scenario: AC2 The answer carries the DP04 facts this service owns, with the version of every list (new, D-RCV-60)
    Given a restructure treatment for case "RW-2026-000512" with approval level "L2", 24 installments, offer amount 850000.00 and no outcome
    When the changed-window read answers it
    Then the item carries treatmentId, caseId, treatmentType, proposedBy, proposedAt, offerAmount, haircutAmount, installments, validUntil, approvalLevel, bookedAt, outcome, outcomeAt, firstDueDate, installmentAmount, installmentsPaid and installmentShortfall
    Then treatmentType, approvalLevel and outcome are answered with the label and the version "REF-2026.12" of LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME
    Then the item carries no contractNumber, no contractDate, no planRef, no recommendedInstallment and no accountKey
    Then no list member and no label is written in the code or in the migration as a constant

  Scenario: AC3 The active count answers the active set of the business date from one data rule (new, D-RCV-60)
    Given the active-state rule of the parameter of the day names the states the count includes
    Given 40 treatments in the states the rule includes and 5 treatments whose outcome is COMPLETED, CANCELED or DECLINED
    When GET /api/recovery/treatment/v1/treatments/active-count is called
    Then the answer is 40 with the business date and the version of the rule
    Then a treatment moved to outcome "COMPLETED" leaves the count and a treatment moved back into an included state returns to it
    Then the count reads the same set in one statement, so no row is counted twice and no state is written in the code

  Scenario: AC4 A scan of the window is paged, stable and repeatable (new, D-RCV-60)
    Given 40 treatments changed on 2026-12-14 and a page size of 15
    When the three pages of the window are read in order
    Then the three pages carry 15, 15 and 10 items with the same total of 40, and the union holds 40 distinct treatment IDs
    Then a page requested twice with the same parameters returns the identical items and total
    Then a page below one, or a size above the declared maximum, is refused with MSG-GEN-003 and no items

  Scenario: AC5 The reads answer only in scope and only with the right (new, D-RCV-60)
    Given user "u-phone-02" holds RW-PHONECOL, which has no Treatment and offer right
    When the user calls GET /api/recovery/treatment/v1/treatments/active-count
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and operation "active-count"
    Then a caller holding Treatment and offer R reads the window with its scope applied, and the total of the page is the total in scope, so no out-of-scope case reference is disclosed

  Scenario: AC6 No contract, plan or account fact is stored or read here, and no foreign table is touched (new, D-RCV-60)
    Given the migration of this story, the code of the two reads and a scan of the schema
    When the absence test runs
    Then rwb_treatment holds no contract_no, contract_date, plan_ref, recommended_installment or account_key column for this story
    Then the code of the two reads names no recovery.v_ace_* view, no rwb_case table, no rwb_source_data table and no other Recovery schema
    Then a query parameter for a contract number, a contract date or a plan term is refused with MSG-GEN-001
    Then the absence test fails a build that declares any of them

  Scenario: AC7 An unavailable store or an unresolved list version answers no partial page (new, D-RCV-60)
    Given the treatment store is unavailable, or the reference data of version "REF-2026.12" cannot be read
    When the changed-window read is called for 2026-12-14
    Then the answer is 503 with MSG-GEN-006 naming the store or the list, and no items
    Then no page is answered with a bare code and no null label
    Then the consumer's step fails on its own side, where MSG-GEN-006 names system "Treatment"

  Scenario: AC8 The two reads write no row, decision record, outbox row or state and give the same answer when repeated (new, D-RCV-60)
    Given the two reads are called on one treatment window
    When each read is called twice with the same window
    Then no row is written to treatment, decision record or outbox, and no state changes
    Then both calls return the same answer

  Scenario: AC9 The two reads hold no write statement, no outbox write and no publish (new, D-RCV-60)
    Given the code of the two reads and a scan of the code of this service
    When the guardrail scan runs
    Then no INSERT, UPDATE, DELETE or MERGE statement is found in the code of the two reads
    Then no outbox row is written and no event is published on rwb.treatment.events.v1 by either read
    Then the guardrail fails a build that declares any of them

  Scenario: AC10 A call without a valid credential, or to a path no operation provides, is answered 401 or 404 (new, D-RCV-60)
    Given a caller presents no valid credential, or a path under /api/recovery/treatment/v1 that no operation provides
    When the caller calls that path
    Then the answer is 401 for the missing credential and 404 for the unknown path, with no items
    Then no treatment of the window is returned with either answer
```

These ten criteria are new for the secondary slice and test only the treatment side; AC1 to AC8 of RWB-E2-010 and their nine test cases stay with RWB-P1-E2010-APP (GAP-2695).



### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds the treatments from the Workbench and the contract and plan facts from `v_ace_account` and `v_ace_plan`, with one system of record and one owner for each part; this service serves its part of the treatments only | REQ-RDF-014; legacy BR1; DP-05 |
| BR2 | No Workbench table copies a contract, a plan or an account, and this service stores no such column and reads no such view | legacy BR2; DP-01, DP-05 |
| BR3 | The window is half-open: a change at 23:59:59+07:00 of day D belongs to D and a change one second later belongs to D+1 | legacy AC8; BR2 of this story |
| BR4 | The set of states the active count includes is a parameter row with a version, never a constant in code or in the migration | legacy BR4; ASM-4459 |
| BR5 | A role reads the treatment facts only with the right in force and only inside its scope | legacy BR5; REQ-RDF-010 |
| BR6 | The active count is compared with the rows written for D with zero tolerance, and a difference holds the publish: the comparison and the hold are the consumer's, this service returns the number only | legacy BR4; DL25 (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602) |
| BR7 | Every code in the answer carries the version of the reference data it was labelled from | DP-07; FSD S2 BR-S2-001 |
| BR8 | The two reads are read-only and repeatable: no row, decision record, outbox row or state is written by them | legacy section 9; section 12.3 |

### 9. State transitions

None. This story changes no case status, no treatment state and no DP04 freshness status: the LOADED and STALE statuses of a data product, and the state of the stage 2 step on the run, are rwb-source-data's and are held by RWB-P1-E1015-APP's freshness stamp and by the run of `Stage2ProductWorkflow`. The treatment state vocabulary of section 9 of RWB-S2-E2004-APP is read by this story and never moved by it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data, through its service identity | Reads the changed window and the active count for the DP04 build (Treatment and offer R; ASM-4460) |
| RW-DATASTEW, data steward | Owns the DP04 product of rwb-source-data; reads the treatment facts and the breaks of the copy |
| RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD | Read the treatment facts for cases in scope |
| RW-COE, RW-AUDIT | Read the treatment facts for all cases |
| RW-TEAMMGR | Reads the treatment facts and the exception queue of its team |
| RW-PHONECOL and every role with no Treatment and offer right | May not read either operation |

The access rows of the data product itself are not this story's: they are held by rwb-source-data and checked there (legacy section 10; REQ-RDF-010).

### 11. Data

| BR Field ID | Table or source | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, treatment_type, proposed_by, proposed_at, offer_amount, haircut_amount, installments, valid_until, approval_level, booked_at, outcome, outcome_at | Read |
| DF-TRT-029 to DF-TRT-033 | treatment | first_due_date, installment_amount, installments_paid, installment_shortfall and the signature status | Read |
| Not specified in the source documents (DOR-RWB-S2-E2010-APP-7) | treatment | updated_at and the seven standard record columns of TSD S2 T3.0 | Read |
| Not specified in the source documents (DOR-RWB-S2-E2010-APP-7) | reference data of rwb-case | the members, the labels and the version of LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME | Read through the contract, never from a table |
| DF-ACE-001, DF-ACE-006, DF-ACE-007, DF-ACE-160, DF-ACE-168, DF-ACE-174, DF-ACE-175 | `recovery.v_ace_account` and `recovery.v_ace_plan` | account key, contract number, contract date, plan reference, booked date, installments, recommended installment | Not owned and not read here: read by rwb-source-data at request time (DP-05) |
| DF-TRT-034 to DF-TRT-061, DF-OPS-001 to DF-OPS-009 | dp_treatment, dp_guarantee_claim, data_product_load | the snapshot rows and the load row of DP04 | Not owned: written by RWB-P1-E2010-APP and its freshness stamp |

The `treatment` row is the only table this story reads, and no field of it is copied out of `rwb_treatment` by a statement of this service (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/treatment/v1`; owner rwb-treatment; both operations are additive to the two of RWB-S2-E2004-APP; right "Treatment and offer R" from TSD S2 T6.1; every operation applies scope and answers the platform error envelope.

| Operation | Purpose | Right | Notes |
|---|---|---|---|
| GET /treatments?changedFrom=&changedTo=&page=&size= | The treatments changed in the half-open window, paged | Treatment and offer R | Ordered by `updated_at`, `id`; 400 on an empty or inverted window and on a size above the maximum; 503 with MSG-GEN-006 when the store or a list version is unavailable |
| GET /treatments/active-count | The active treatments of the business date | Treatment and offer R | Answers the number, the business date and the version of the active-state rule; 40 for the fixture of AC3 |

The operation names, the page shape, the maximum size and the parameter name of the active rule are a target design choice fixed by no source document (GAP-2696; ASM-4459). A refused caller is refused with MSG-P4-002 and an out-of-scope row is never disclosed; the two operations are declared in the OpenAPI 3.1 document of this service and their fake is the one in section 12.8.

#### 12.2 REST operations consumed

| Operation | Owner | Purpose | Budget |
|---|---|---|---|
| the reference-data read for LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME | rwb-case (P3) | the members, the labels and the version of the three lists | one hop, 2 s, GET retried once, breaker (DP-07, DP-11); operation name Not specified in the source documents (GAP-2696; ASM-4459) |

No other service is called: the contract and plan facts are not read here, and the case reference arrives on each treatment row.

#### 12.3 Events published

None. This story writes no outbox row and publishes nothing on `rwb.treatment.events.v1`; the treatment announcements are RWB-S2-E2004-APP's, and the DP04 build is started by rwb-source-data's own event.

#### 12.4 Events consumed

None. The window is driven by the consumer's workflow, not by an event of this service (DP-10).

#### 12.5 Workflows and activities

None. This story runs on the API deployment of rwb-treatment only: the window is one call of the `snapshot(page)` activity of `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, and `TreatmentWorkflow` on queue `rwb-treatment` belongs to RWB-S2-E2004-APP (DP-10). The workflow is `Stage2ProductWorkflow` on queue `rwb-source-data` in namespace `rwb-recovery`, with activities `snapshot(page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04`, started by `AceIngestCheck` as a child workflow (parent close policy `ABANDON`, workflow ID `stage2-dp04-{businessDate}`) in the workflow task that commits the ALS stamp, and not by a consumer of `rwb.source-data.AceDataReady.v1` (RD-P1-003, RD-P1-040; GAP-0510). The DP04 expected-by time is 08:00, carried from decision log row DL11 until the data steward records it in the `data_product` row (GAP-0511). Every deployment value, threshold and timing is a named chart value set per environment, and the fixture owner is named at the wave 2 entry check (GAP-0513).

#### 12.6 Schedules

None. The legacy JOB-02 stage 2 step leaves no Quartz job, no Spring Batch job and no Temporal Schedule in this service: the daily trigger is the event-started workflow of rwb-source-data (DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | Notes |
|---|---|---|---|
| treatment | rwb_treatment | rwb-treatment | Read only in this story; this story adds `ix_treatment_updated_at` on (`updated_at`, `id`) for the window read and changes no other object |

No table of another service is read, and `dp_treatment`, `dp_guarantee_claim` and `data_product_load` are not created, read or written here (DP-01). The dated copy `dp_treatment` is P1's data engine: it is built from this service's events and read only for reporting, never as the source of a treatment; the live `treatment` row of `rwb_treatment` is the only treatment record this story reads (GAP-1716).

#### 12.8 Contract fakes

| Fake | Answers | Used by |
|---|---|---|
| treatment read fake | the two operations of section 12.1, with the fixtures of section 7 and the 503 cases of X5 and X6 | the app tests of this story and the DP04 build of RWB-P1-E2010-APP |
| DP04 page-request fake | a `snapshot(page)` call for business date 2026-12-14 with a page size of 15, and a second page | AC1, AC4 |
| reference-data fake | the three lists with version "REF-2026.12", an empty list and a timeout | AC2, AC7 |
| guard fake | the right answer of RW-RESTRUCT, RW-CASEOWN and the service identity, and a refusal for RW-PHONECOL | AC5 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST provided | 2 | GET /treatments and GET /treatments/active-count on `/api/recovery/treatment/v1` (DP-13) |
| REST consumed | 1 | the reference-data read of rwb-case, one hop, 2 s (DP-07, DP-11) |
| Kafka published | None | no outbox row, no event |
| Kafka consumed | None | the window is driven by the consumer's workflow |
| Temporal | None | no workflow and no activity in this service for this story |
| File | None | no file in or out |
| SQL view | None | no `v_ace_*` read: the ACE facts stay in rwb-source-data (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `stage2` beside the `record` and `plan` modules of RWB-S2-E2004-APP.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Stage2TreatmentReadController | REST | The two operations of section 12.1, the checks of X1, X2 and X7 and the problems of section 14 |
| ChangedWindowService | Service | Builds the half-open window, applies the scope, orders by `updated_at` and `id` and cuts the page |
| ActiveCountService | Service | Reads the active-state rule with its version and counts the included states in one statement |
| TreatmentFactsAssembler | Service | Builds the DP04 field set of AC2 from the row and nothing else |
| ReferenceLabelResolver | Service | Answers every label with the version of the day and fails the page when the version is missing |
| TreatmentReadRepository | Repository | Reads `treatment` of `rwb_treatment` only, never another schema |

**Database.** One Flyway version on the service sequence, `V<next>__rwb_treatment_ix_updated_at.sql`, which adds `ix_treatment_updated_at` on (`updated_at`, `id`); it changes no applied version, no column and no table, because the contract and plan facts are not held here (DP-01, DP-05, DP-15).

**Configuration and reference data.** The active-state rule is a parameter row with a version (states assumed from the outcome vocabulary of LOV-TRT-OUTCOME; ASM-4459); LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME are reference-data rows with a version, read through the contract (DP-07). The page size default and maximum are named chart values, not constants.

**Build steps**

1. Write the migration and prove that it adds one index, changes no column and names no other schema.
2. Build `TreatmentReadRepository` with the schema-boundary test that refuses a statement on another schema's table or on a `v_ace_*` view.
3. Build `ChangedWindowService` for the half-open window, the page cut and the stable order; build `ActiveCountService` and `TreatmentFactsAssembler`, and prove that no state and no list member is written in code.
4. Build `ReferenceLabelResolver` with the version stamp and the fail-closed answer of X6, then the controller with the scope and right rules of AC5.
5. Add the absence test of AC6, the paging test of AC4 and the tests of section 16 against the fakes of section 12.8.

**Feature flag.** `rwb.treatment.stage2-read` (ASM-4461). Off: the two operations answer 404 with MSG-P4-003 and the DP04 build is not wired.

**Done when.** The tests of section 16 pass; a scan of 40 treatments on 2026-12-14 answers 40 distinct IDs over three pages, the count answers 40, and no statement, column or constant outside `rwb_treatment` is used.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A window parameter is missing or inverted, or an unsupported query parameter is sent | Enter {field}. |
| MSG-GEN-003 | A page or a size is out of range | {field} is outside the accepted range {range}. |
| MSG-GEN-006 | The store or a reference-data version is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | The caller is not signed in | Sign in to continue. |
| MSG-P4-002 | A role without Treatment and offer R calls either operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| Not specified in the source documents (CG-ALL-8340) | The feature switch is off | Not specified in the source documents (CG-ALL-8340) |

For MSG-GEN-006 the {system} is "Treatment" for the store, as the legacy story used it, and the list code for a missing version; no consumer re-words a message text. The DP04 messages MSG-P1-001 and MSG-P1-002 belong to rwb-source-data and are not restated here.

### 15. Screens and states

No new screen. SCR-03 Case record shows the DP04 facts of a case and SCR-45 Data quality shows the DP04 breaks of the data steward, both composed by the gateway-bff route from the DP04 record read of rwb-source-data (DP-19). This service's two reads are called by the DP04 build and by no screen; SCR-14 Treatment record is unaffected and keeps the treatment entity of RWB-S2-E2004-APP.

States of SCR-03 (CG-ALL-8344): empty: Not specified in the source documents (CG-ALL-8344); loading: as Screen Specifications v1 section SCR-03; error: Not specified in the source documents (CG-ALL-8344); no access: Not specified in the source documents (CG-ALL-8344).

States of SCR-14 (CG-ALL-8345): empty: Not specified in the source documents (CG-ALL-8345); loading: Not specified in the source documents (CG-ALL-8345); error: Not specified in the source documents (CG-ALL-8345); no access: Not specified in the source documents (CG-ALL-8345).

States of SCR-45 (CG-ALL-8346): empty: Not specified in the source documents (CG-ALL-8346); loading: as Screen Specifications v1 section SCR-45; error: Not specified in the source documents (CG-ALL-8346); no access: Not specified in the source documents (CG-ALL-8346).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E2010-APP-12 | AC1 | Component | AC1 The changed-window read returns exactly the treatments of the half-open business-date window (new, D-RCV-60) |
| TC-S2-E2010-APP-13 | AC2 | Component | AC2 The answer carries the DP04 facts this service owns, with the version of every list (new, D-RCV-60) |
| TC-S2-E2010-APP-14 | AC3 | Component | AC3 The active count answers the active set of the business date from one data rule (new, D-RCV-60) |
| TC-S2-E2010-APP-15 | AC4 | Component | AC4 A scan of the window is paged, stable and repeatable (new, D-RCV-60) |
| TC-S2-E2010-APP-16 | AC5 | Component | AC5 The reads answer only in scope and only with the right (new, D-RCV-60) |
| TC-S2-E2010-APP-17 | AC6 | Component | AC6 No contract, plan or account fact is stored or read here, and no foreign table is touched (new, D-RCV-60) |
| TC-S2-E2010-APP-18 | AC7 | Component | AC7 An unavailable store or an unresolved list version answers no partial page (new, D-RCV-60) |
| TC-S2-E2010-APP-08 | BR3 | Component | Treatment rows at the window boundaries and rows with the same updated_at ordered by id; boundary values Not specified in the source documents (DOR-RWB-S2-E2010-APP-12); the window read uses ix_treatment_updated_at on (updated_at, id) |
| TC-S2-E2010-APP-19 | AC8 | Component | AC8 The two reads write no row, decision record, outbox row or state and give the same answer when repeated (new, D-RCV-60) |
| TC-S2-E2010-APP-10 | AC9, BR8 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2010-APP-AC9) |
| TC-S2-E2010-APP-11 | AC10 | Component | A call without a valid credential and a call to a path no operation provides; answers 401 and 404 with no items |

The nine legacy test cases TC-S2-E2010-APP-12 to TC-E2-010-09 belong to RWB-P1-E2010-APP, which owns AC1 to AC8 of the legacy story; they are not re-tagged and not copied here (GAP-2695).

### 17. Guardrails

- No business value in code or in a migration: the active states, the page limits and every list member are data rows with a version (DP-07).
- No personal data in the answer, the logs or the tests beyond the treatment and case identifiers: the fixture carries amounts and codes, and no name, address, identity number or contact point.
- ACE data only through the owner's contract or the `v_ace_*` views of rwb-source-data; this service reads no ACE table and no view, and re-exposes no contract or plan fact (DP-05).
- No read of another service's table and no foreign key across schemas; the only table of this story is `treatment` in `rwb_treatment` (DP-01).
- The reads write nothing: no state, no decision record and no outbox row on a read path.
- The reference-data version is stamped on every answer; an unversioned label fails the page instead of being served.
- The DP04 product, its access rows, its freshness stamp and its breaks stay with rwb-source-data; this service supplies the number the consumer reconciles with and takes no publish decision (BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25 (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602); BR1 to BR4 of this story | TC-S2-E2010-APP-01, TC-S2-E2010-APP-02, TC-S2-E2010-APP-03, TC-S2-E2010-APP-08 |
| REQ-RDF-010 | A role reads a data product only through its access row and its scope | Business Requirements Epic 2, section 4 | FEAT-CHO-09 | 07 Route, settle and claim | BR5 of this story | TC-S2-E2010-APP-05 |

The legacy rows of RWB-E2-010 and the traceability of the DP04 copy, the stamp and the catalog are held by RWB-P1-E2010-APP; the guarantee claim half is RWB-S3-E2010-APP's.

### 19. Out of scope

- AC1 to AC8 of RWB-E2-010, its nine test cases, the `dp_treatment` and `dp_guarantee_claim` copies, the link check, the active-count comparison, the break list, the DP04 stamp, the catalog entry and the rerun, which are RWB-P1-E2010-APP.
- The treatment entity, its write path, the plan facts and the plan timers, which are RWB-S2-E2004-APP.
- The guarantee claim facts of the stage 2 product, which are RWB-S3-E2010-APP.
- The contract number, contract date and plan terms of the ACE views, which rwb-source-data reads at request time.
- The access rows of DP04 and the data-product read of rwb-source-data (RWB-P1-E1016-CON), the freshness stamp (RWB-P1-E1015-APP) and the deployment of the DP04 build (RWB-P1-E2010-OPS).
- The screens, their composite routes and the deployment of this service (DP-19; RWB-PLT-N001-CON).
