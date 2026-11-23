# RWB-S3-E2010-APP Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the secondary slice of RWB-E2-010 for rwb-guarantee, the guarantee-claim half of the split. The in-process `GuaranteeClaimQuery.changedBetween` of the legacy stage 2 step becomes a changed-window read of the claim resource on `/api/recovery/guarantee/v1` with a mock and a 2 s timeout (DP-11, DP-13), reading `rwb_guarantee` only (DP-01) and labelling both claim lists from the reference data of the day (DP-07); the contract number, contract date and plan terms are neither stored nor read here (DP-05); the window is driven by the event-started `Stage2ProductWorkflow` of rwb-source-data, so this service owns no job and no schedule for it (DP-10); the read is additive on one Flyway version of this service (DP-15) and the DP04 screens are composed by gateway-bff (DP-19). No legacy acceptance criterion is carried: AC1 to AC8 and TC-E2-010-01 to TC-E2-010-09 stay with RWB-P1-E2010-APP, the primary slice (GAP-2738). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E2010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S3-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E2010-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to REQ-RDF-014, REQ-RDF-010) |
| Status | Draft (realignment v1) |

### 1. Story

As a **recovery developer on the guarantee service (RW-TRIBE)**, I want **the guarantee-claim side of the stage 2 data product: a changed-window read on `/api/recovery/guarantee/v1` that hands the DP04 build of rwb-source-data exactly the claim facts DP04 holds for a guarantee claim — the case, the claim type, the claim deadline, the claimed amount, the filing date, the paid amount and the status — over a half-open business-date window, with both claim lists labelled from the reference data of the day, and with no contract number, contract date, plan or account ever stored or read in this service**, so that **the stage 2 product is built from the service that owns the claim record, the settlement, restructure and deed-in-lieu screens read one checked place, and nothing is copied out of ACE**.

This story is the secondary slice of legacy RWB-E2-010 and the guarantee half of the split. It owns:

- the changed-window read `GET /guarantee-claims` on base `/api/recovery/guarantee/v1` (DP-13), which replaces the in-process `GuaranteeClaimQuery.changedBetween` of the legacy stage 2 step with a contract and a fake (DP-11);
- the DP04 field set the answer carries from the `guarantee_claim` row, with the reference-data version of `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS` (DP-01, DP-07);
- one Flyway version on this service's own sequence that adds the index the window read needs and changes no applied version (DP-15);
- the scope and right rule of the read, and the statement that the contract and plan facts are not this service's to serve (DP-05).

It does not own: the eight legacy acceptance criteria and the nine legacy test cases, the `dp_treatment` and `dp_guarantee_claim` copies, the case-link check, the active treatment count, the DP04 freshness stamp, the break list, the catalog entry and the rerun, which are RWB-P1-E2010-APP and its contract RWB-P1-E2010-CON; the treatment facts, which are RWB-S2-E2010-APP; the claim record itself, its preparation, its submission, its tracking, its negotiation and its close, which are the claim stories of this service (RWB-S3-E4013-APP to RWB-S3-E4019-APP); the contract number, contract date and plan terms, which stay in `recovery.v_ace_account` and `recovery.v_ace_plan`; the screens and their composite routes (DP-19); the deployment of the read, which follows the service deployment.

### 2. Business rationale

From Epic 3 the settlement, restructure and deed-in-lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place (REQ-RDF-014), read only through a data-product access row (REQ-RDF-010). The target keeps two things apart that the legacy step held together: the live claim record stays with S3 in `rwb_guarantee`, and the dated DP04 copy stays with P1 as the data engine, built from the live facts and read-only for reporting (DP-01).

The legacy step called the guarantee module in process, so the copy and the record moved together, and the legacy story could say that "before it is built (Epic 4), the interface returns no claims" without saying who answers the call in between. In the target the copy is built by `Stage2ProductWorkflow` of rwb-source-data, which asks the owner over one contract for the claims changed in the business-date window (DP-10, DP-11). Nothing of ACE crosses that seam: the contract number, the contract date and the plan terms are read by rwb-source-data from the `v_ace_*` views at request time, never copied and never re-exposed here (DP-05).

What is left to S3 is a narrow read with three duties: the boundary the legacy step used (a change at 23:59:59 belongs to the day, one second later to the next), the field set DP04 holds for a claim, and a label with a version for every code, so that a claim type or a claim status is never served bare. The volumes are those of the claim book, not of the case book: a case carries one or a few claims, and the whole claim set of the day must be in the copy before the Epic 3 screens open.

### 3. Preconditions

- RWB-P1-E2010-CON is published: it declares the DP04 record read, the page-request shape the DP04 build sends and the claim page it expects, and this story builds the read against its fake, so the dependency never blocks (Contract dependency; DP-11).
- The read is published on this service's base, because the `guarantee_claim` table and its REST owner are S3's: TSD S3 T-A.1 gives this service two operations, the claim create and the claim update, and no consumer read; the operation name, the path and the page parameters are fixed by no source document (GAP-2738; ASM-4550).
- The `guarantee_claim` table of schema `rwb_guarantee` exists with DF-TRT-015 to DF-TRT-022 and the seven standard record columns of TSD S3 T3.0, and this service's Flyway sequence is at the version that carries the platform library tables; the Work Package lists no build dependency, so the table and the platform libraries are taken as present (ASM-4552; DP-01, DP-15).
- The reference-data read of rwb-case for `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS` reaches the service through the client library, with a version and a fake (DP-07; ASM-4552).
- The platform guard library that answers a role's right on a capability area is on the service template, so the read declares the right "Treatment and offer R" of TSD S3 T6.1 and nothing else (ASM-4552).
- The gateway-bff composite route that serves SCR-03 Case record from the case read and the DP04 read of rwb-source-data is published; no screen calls this service directly (DP-19).
- The window is the half-open business-date window [start of D, start of D+1) in +07:00 over `guarantee_claim.updated_at`, and a claim changed at 23:59:59 of D belongs to D (ASM-4551).
- Feature switch `rwb.guarantee.stage2-read` exists; its default is off in the non-production environments until the DP04 build of rwb-source-data is wired to the operation (ASM-4550).
- No approval stop: the FSD S3 v3 and TSD S3 v2 documents carry status "In review" and the Epic 2 business requirements are not recorded as approved in this workspace, so the story starts on Day 1 at status Draft (realignment v1) (ASM-4556).

### 4. Flow

1. The `snapshot(page)` activity of `Stage2ProductWorkflow` in rwb-source-data calls `GET /guarantee-claims?changedFrom=<start of D>&changedTo=<start of D+1>&page=1&size=<page size>` on base `/api/recovery/guarantee/v1`, one hop, 2 s timeout (DP-10, DP-11, DP-13).
2. The controller refuses an empty or inverted window, a page below one and a size above the declared maximum before a statement runs (X1, X2).
3. The guard answers the right "Treatment and offer R" for the caller; a role without it is refused, and a service identity is authorised by its own right row (X3; rights are data).
4. The read selects from `guarantee_claim` of `rwb_guarantee` only, where `updated_at` is at or after `changedFrom` and strictly before `changedTo`, ordered by `updated_at` and `id`, and cuts the requested page (DP-01, DP-15).
5. `ClaimFactsAssembler` builds the DP04 field set: the claim and case IDs, the claim type, the claim deadline, the claimed amount, the filing date, the paid amount and the status (DF-TRT-015 to DF-TRT-022).
6. `ReferenceLabelResolver` answers the claim type and the status with the label and the version of the reference data of the day and stamps that version on the page; a missing version fails the page rather than answering a bare code (X6; DP-07).
7. The answer carries the items, the window, `page`, `size` and a `total` computed with the caller's scope applied, and the consumer asks for the next page until `total` is reached.
8. The consumer writes the rows it receives into `dp_guarantee_claim` in schema `rwb_source_data`, keyed by record ID and business date, and holds on its break list any row whose case does not resolve; both decisions are its own and are not taken here (BR6).
9. The read writes nothing — no row, decision record, outbox row or state change — and a repeat of the same request returns the same page (BR7).
10. No ACE view and no other service is called on this path: the contract and plan facts are named by the DP04 answer of rwb-source-data, not by this service (DP-05).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `changedFrom` or `changedTo` is missing, or the window is empty or inverted | 400; no statement runs and no partial page is returned | MSG-GEN-001 | AC1 |
| X2 | `page` below one, or `size` above the declared maximum | 400 with the accepted range named | MSG-GEN-003 | AC3 |
| X3 | A role without Treatment and offer R, or a caller outside the scope of the rows | 403; the refusal is logged with the role and the operation, and no row is disclosed | MSG-P4-002 | AC4 |
| X4 | A page of a multi-page scan is requested while a claim of the window is being changed | The changed row appears once, under its later `updated_at`, and no row is repeated across pages | None | AC3 |
| X5 | The claim store or the connection pool is unavailable | 503; the consumer holds the claim part of its page and does not stamp the copy of the day | MSG-GEN-006 | AC6 |
| X6 | The reference-data version of a list cannot be resolved | 503; the page is not answered with unversioned codes | MSG-GEN-006 | AC6 |
| X7 | A caller asks this service for a contract number, a contract date or a plan term | No such field exists in the answer and the request is refused as an unsupported query parameter | MSG-GEN-001 | AC5 |

X1, X2, X3 and the empty-answer path are the legacy step's own checks carried onto the read; X4 to X7 are the read's paths in the target. The stale-product path of the legacy story (MSG-P1-001) is the consumer's and is not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1: the table is in this service's schema, the reference data arrives through a fake and the DP04 contract is faked; no live rwb-source-data, rwb-case or ACE view is needed |
| Negotiable | The operation name, the page shape, the index name, the maximum size and the flag are this story's choice; the field set, the half-open window, the rights and the messages are fixed |
| Valuable | The stage 2 product is built from the owner of the claim record, with no copy of a contract, a plan or an account |
| Estimable | One controller, one read service, one assembler, one reference-label resolver, one index, one migration |
| Small | Fits one sprint with its tests |
| Testable | Each criterion of section 7 is one automated test on the window boundary, the field set, the paging, the right or the absence of a foreign fact |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments, the guarantee-claim side

  Background:
    Given business date 2026-12-14 and the guarantee claims changed on it are in schema rwb_guarantee
    Given 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht
    Given LOV-CLAIM-TYPE and LOV-CLAIM-STATUS are reference data with version "REF-2026.12"

  Scenario: AC1 The claim read returns exactly the claims of the half-open business-date window (new, D-RCV-60)
    Given the rwb-source-data contract mock returns a DP04 claim page request for business date 2026-12-14
    Given claim "GCL-SYN-0901" changed at 2026-12-14T23:59:59+07:00 and claim "GCL-SYN-0902" changed at 2026-12-15T00:00:00+07:00
    When GET /api/recovery/guarantee/v1/guarantee-claims?changedFrom=2026-12-14T00:00:00+07:00&changedTo=2026-12-15T00:00:00+07:00 is called
    Then the page carries "GCL-SYN-0901" and does not carry "GCL-SYN-0902"
    Then the same read with changedFrom=2026-12-15T00:00:00+07:00 carries "GCL-SYN-0902" and does not carry "GCL-SYN-0901"
    Then no claim of the two windows is returned by both, and a row is never returned twice in one scan

  Scenario: AC2 The answer carries the DP04 claim facts with the version of both lists (new, D-RCV-60)
    Given the rwb-source-data contract mock returns a DP04 claim page request for business date 2026-12-14
    Given a TCG claim of case "RW-2026-000512" with claim deadline 2027-02-28 and status FILED
    When the changed-window read answers it
    Then the item carries claimId, caseId, claimType, claimDeadline, claimedAmount, filedAt, paidAmount and status
    Then claimType and status are answered with the label and the version "REF-2026.12" of LOV-CLAIM-TYPE and LOV-CLAIM-STATUS
    Then the item carries no contractNumber, no contractDate, no planRef, no recommendedInstallment and no accountKey
    Then no list member and no label is written in the code or in the migration as a constant

  Scenario: AC3 A scan of the window is paged, stable and repeatable (new, D-RCV-60)
    Given 5 claims changed on 2026-12-14 and a page size of 2
    When the three pages of the window are read in order
    Then the three pages carry 2, 2 and 1 items with the same total of 5, and the union holds 5 distinct claim IDs
    Then a page requested twice with the same parameters returns the identical items and total
    Then a page below one, or a size above the declared maximum, is refused with MSG-GEN-003 and no items

  Scenario: AC4 The read answers only in scope and only with the right (new, D-RCV-60)
    Given user "u-phone-02" holds RW-PHONECOL, which has no Treatment and offer right
    When the user calls GET /api/recovery/guarantee/v1/guarantee-claims
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and operation "guarantee-claims"
    Then a caller holding Treatment and offer R reads the window with its scope applied, and the total of the page is the total in scope, so no out-of-scope case reference is disclosed

  Scenario: AC5 No contract, plan or account fact is stored or read here, and no foreign table is touched (new, D-RCV-60)
    Given the migration of this story, the code of the read and a scan of the schema
    When the absence test runs
    Then rwb_guarantee holds no contract_no, contract_date, plan_ref, recommended_installment or account_key column for this story
    Then the code of the read names no recovery.v_ace_* view, no rwb_case table, no rwb_source_data table and no other Recovery schema
    Then a query parameter for a contract number, a contract date or a plan term is refused with MSG-GEN-001
    Then the absence test fails a build that declares any of them

  Scenario: AC6 An unavailable store or an unresolved list version answers no partial page (new, D-RCV-60)
    Given the guarantee store is unavailable, or the reference data of version "REF-2026.12" cannot be read
    When the changed-window read is called for 2026-12-14
    Then the answer is 503 with MSG-GEN-006 naming the store or the list, and no items
    Then no page is answered with a bare code and no null label
    Then the consumer's step fails on its own side, where MSG-GEN-006 names system "Guarantee claim"
```

These six criteria are new for the secondary slice and test only the guarantee-claim side. AC1 to AC8 of RWB-E2-010 and their nine test cases stay with RWB-P1-E2010-APP, the primary slice: the `dp_guarantee_claim` copy, the References break of AC4, the treatment count of AC7 and the DP04 stamp of AC1 and AC5 are all that story's and are exercised there (GAP-2738; GAP-2739).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds the guarantee claims from the Workbench and the contract and plan facts from `v_ace_account` and `v_ace_plan`, with one system of record and one owner for each part; this service serves its part of the claims only | REQ-RDF-014; legacy BR1; DP-05 |
| BR2 | No Workbench table copies a contract, a plan or an account, and this service stores no such column, reads no such view and answers no such fact | legacy BR2; DP-01, DP-05 |
| BR3 | The window is half-open: a change at 23:59:59+07:00 of day D belongs to D and a change one second later belongs to D+1 | legacy AC8; ASM-4551 |
| BR4 | The claim facts DP04 holds are the record of the claim and never its outcome: the read answers the claim of the case as it stands and takes no decision on it | legacy BR1; FSD S3 A2.1 to A2.8 |
| BR5 | A role reads the claim facts only with the right in force and only inside its scope | legacy BR5; REQ-RDF-010 |
| BR6 | Every claim row DP04 holds links to an existing case, or it is held on the break list and retried with the next build; the link check is the consumer's, and this read answers the `case_id` of every claim in the window and resolves nothing | legacy BR3; GAP-2740; ASM-4555 |
| BR7 | The read is read-only and repeatable: no row, decision record, outbox row or state is written by it | legacy section 9; section 12.3 |
| BR8 | Every code in the answer carries the label and the version of the reference data of the day; a code is never served bare and no list member is written in code | DP-07; FSD S3 BR-S3-001 to BR-S3-008 |

**Where each rule lives in the target.** BR1 and BR2 are the two system-of-record statements of the legacy story, and they are why the claim facts are served here and the contract and plan facts are not. BR3 is the `updated_at` predicate of the statement. BR4 is why nothing of this story writes a claim status. BR5 is the scope clause and the guard. BR6 is the boundary to rwb-source-data: the answer names the case, the consumer checks it (GAP-2740). BR7 is why the read has no outbox row. BR8 is the reference-label resolver and the version stamp.

### 9. State transitions

None. This story changes no case status, no claim status and no DP04 freshness status: the LOADED and STALE statuses of a data product, and the state of the stage 2 step on the run, are rwb-source-data's and are held by the freshness stamp and by the run of `Stage2ProductWorkflow`. The claim status vocabulary of `LOV-CLAIM-STATUS` — PREPARING, FILED, DEFECT, PAID and REJECTED (TSD S3 T3.2) — is read by this story and never moved by it; the guaranteed claim's own state machine of 32 rules over 17 states (TSD S3 T4) belongs to the claim stories of this service, not to this read.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data, through its service identity | Reads the changed window for the DP04 build (Treatment and offer R; ASM-4550) |
| RW-DATASTEW, data steward | Owns the DP04 product of rwb-source-data; reads the claim facts and the breaks of the copy |
| RW-GUARANT, guarantee officer | Reads the claim facts for cases in scope (CRU in the matrix of TSD S3 T6.1) |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-CREDITAD | Read the claim facts for cases in scope |
| RW-COE, RW-AUDIT, RW-TEAMMGR and the read-only roles of TSD S3 T6.1 | Read the claim facts for all cases or for their team |
| RW-PHONECOL and every role with no Treatment and offer right | May not read the operation |

The access rows of the data product itself are not this story's: they are held by rwb-source-data and checked there (legacy section 10; REQ-RDF-010). No credential and no personal name appears in the request or the answer, which carry claim and case identifiers, dates, amounts, codes and a version only.

### 11. Data

| BR Field ID | Table or source | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read (labelled from LOV-CLAIM-TYPE) |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Read |
| DF-TRT-022 | guarantee_claim | status | Read (labelled from LOV-CLAIM-STATUS) |
| — | guarantee_claim | `updated_at` and the seven standard record columns of TSD S3 T3.0 | Read (the window predicate and the tie-break) |
| — | reference data of rwb-case | the members, the labels and the version of LOV-CLAIM-TYPE and LOV-CLAIM-STATUS | Read through the contract, never from a table |
| DF-ACE-001, DF-ACE-006, DF-ACE-007, DF-ACE-160, DF-ACE-168, DF-ACE-174, DF-ACE-175 | `recovery.v_ace_account` and `recovery.v_ace_plan` | account key, contract number, contract date, plan reference, booked date, installments, recommended installment | Not owned and not read here: read by rwb-source-data at request time (DP-05) |
| DF-TRT-034 to DF-TRT-061, DF-OPS-001 to DF-OPS-009 | dp_treatment, dp_guarantee_claim, data_product_load | the snapshot rows and the load row of DP04 | Not owned: written by RWB-P1-E2010-APP and its freshness stamp |

The `guarantee_claim` row is the only table this story reads, and no field of it is copied out of `rwb_guarantee` by a statement of this service (DP-01). The claim types served are the four members of `LOV-CLAIM-TYPE` — TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE and COLLATERAL_INSURANCE (TSD S3 T3.2) — with no filter but the window and the caller's scope (ASM-4553).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/guarantee/v1`; owner rwb-guarantee; this read is additive to the two operations of TSD S3 T-A.1 (`POST /cases/{caseId}/guarantee-claims`, right C, and `PATCH /guarantee-claims/{claimId}`, right U), which are the claim stories' and are not restated here. Right "Treatment and offer R" from TSD S3 T6.1; the operation applies scope and answers the platform error envelope.

| Operation | Purpose | Right | Notes |
|---|---|---|---|
| GET /guarantee-claims?changedFrom=&changedTo=&page=&size= | The guarantee claims changed in the half-open window, paged | Treatment and offer R | Ordered by `updated_at`, `id`; 400 on an empty or inverted window and on a size above the maximum; 503 with MSG-GEN-006 when the store or a list version is unavailable; the answer carries each claim's `caseId`, so the consumer resolves the case itself |

The operation name, the path, the page shape, the maximum size and the parameter names are a target design choice fixed by no source document, and the ownership rows give this service two claim operations and no read (GAP-2738; ASM-4550). A refused caller is refused with MSG-P4-002 and an out-of-scope row is never disclosed; the operation is declared in the OpenAPI 3.1 document of this service and its fake is the one in section 12.8.

#### 12.2 REST operations consumed

| Operation | Owner | Purpose | Budget |
|---|---|---|---|
| the reference-data read for LOV-CLAIM-TYPE and LOV-CLAIM-STATUS | rwb-case (P3) | the members, the labels and the version of the two lists | one hop, 2 s, GET retried once, breaker (DP-07, DP-11); operation name Not specified in the source documents (GAP-2738; ASM-4552) |

No other service is called: the contract and plan facts are not read here, and the case reference arrives on each claim row. The read consumes no case operation, because resolving the case is the consumer's check (BR6).

#### 12.3 Events published

None. This story writes no outbox row and publishes nothing on `rwb.guarantee.events.v1`; the ownership rows give S3 zero events (TSD S3 T5.3, "None"), and the DP04 build is started by rwb-source-data's own event (ASM-4554).

#### 12.4 Events consumed

None. The window is driven by the consumer's workflow, not by an event of this service (DP-10). The service's own inbox and rule loader are the template's and are not touched by this story.

#### 12.5 Workflows and activities

None. This story runs on the API deployment of rwb-guarantee only: the window is one call of the `snapshot(page)` activity of `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, and `GuaranteeClaimWorkflow` on queue `rwb-guarantee` belongs to the claim stories of this service (DP-10). The read creates no workflow, signals none and starts none.

#### 12.6 Schedules

None. The legacy JOB-02 stage 2 step leaves no Quartz job, no Spring Batch job and no Temporal Schedule in this service: the daily trigger is the event-started workflow of rwb-source-data (DP-10), and the ownership rows give S3 zero jobs.

#### 12.7 Tables owned

| Table | Schema | Notes |
|---|---|---|
| guarantee_claim | rwb_guarantee | Read only in this story; this story adds `ix_guarantee_claim_updated_at` on (`updated_at`, `id`) for the window read and changes no other object |

No table of another service is read, and `dp_treatment`, `dp_guarantee_claim` and `data_product_load` are not created, read or written here (DP-01).

#### 12.8 Contract fakes

| Fake | Answers | Used by |
|---|---|---|
| guarantee claim read fake | the operation of section 12.1, with the fixtures of section 7 and the 503 cases of X5 and X6 | the app tests of this story and the DP04 build of RWB-P1-E2010-APP |
| DP04 page-request fake | a `snapshot(page)` call for business date 2026-12-14 with a page size of 2, and the following pages | AC1, AC3 |
| reference-data fake | LOV-CLAIM-TYPE and LOV-CLAIM-STATUS with version "REF-2026.12", an empty list and a timeout | AC2, AC6 |
| guard fake | the right answer of RW-GUARANT, RW-CASEOWN and the service identity, and a refusal for RW-PHONECOL | AC4 |

The claim read fake is the Day-1 unblocker of the consumer: RWB-P1-E2010-APP builds against it and its own C dependency never waits for this service (ASM-4550).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST provided | 1 | GET /guarantee-claims on `/api/recovery/guarantee/v1` (DP-13) |
| REST consumed | 1 | the reference-data read of rwb-case, one hop, 2 s (DP-07, DP-11) |
| Kafka published | None | no outbox row, no event |
| Kafka consumed | None | the window is driven by the consumer's workflow |
| Temporal | None | no workflow and no activity in this service for this story |
| File | None | no file in or out |
| SQL view | None | no `v_ace_*` read: the ACE facts stay in rwb-source-data (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, module `stage2` beside the `claim` and `workflow` modules of the claim stories.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_guarantee`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/guarantee/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 and DP-13 are the pattern this story is built on: the in-process `GuaranteeClaimQuery` becomes one published read with a fake on this service's own base. DP-01 fixes the schema boundary and DP-05 the fact that no ACE fact is re-exposed here. DP-10 removes the job rather than moving it: the trigger is the consumer's event-started workflow and this service schedules nothing. DP-15 and DP-19 are one index and one composite route. DP-07, DP-10, DP-15 and DP-19 add four platform CON dependencies in the table; the reference-data client library, the workflow kit, the per-service Flyway baseline and the gateway route all arrive with the service template and the platform epics, the Work Package lists no build dependency, so the story is Day 1 against the published contracts and their fakes (ASM-4552; ASM-4554).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Stage2ClaimReadController | REST | The operation of section 12.1, the checks of X1, X2 and X7 and the problems of section 14 |
| ChangedWindowService | Service | Builds the half-open window, applies the scope, orders by `updated_at` and `id` and cuts the page |
| ClaimFactsAssembler | Service | Builds the DP04 field set of AC2 from the row and nothing else |
| ReferenceLabelResolver | Service | Answers the claim type and the status with the version of the day and fails the page when the version is missing |
| ClaimReadRepository | Repository | Reads `guarantee_claim` of `rwb_guarantee` only, never another schema |

**Database.** One Flyway version on the service sequence, `V<next>__rwb_guarantee_ix_updated_at.sql`, which adds `ix_guarantee_claim_updated_at` on (`updated_at`, `id`); it changes no applied version, no column and no table, because the contract and plan facts are not held here (DP-01, DP-05, DP-15).

**Configuration and reference data.** LOV-CLAIM-TYPE and LOV-CLAIM-STATUS are reference-data rows with a version, read through the contract (DP-07; ASM-4552); the page size default and maximum and the index name are named chart values, not constants (ASM-4550). The capability area "Treatment and offer" and its rights are access data of P4 read through the guard library.

**Build steps**

1. Write the migration and prove that it adds one index, changes no column and names no other schema.
2. Build `ClaimReadRepository` with the schema-boundary test that refuses a statement on another schema's table or on a `v_ace_*` view.
3. Build `ChangedWindowService` for the half-open window, the page cut and the stable order; build `ClaimFactsAssembler` and prove that no list member is written in code.
4. Build `ReferenceLabelResolver` with the version stamp and the fail-closed answer of X6, then the controller with the scope and right rules of AC4.
5. Add the absence test of AC5, the paging test of AC3 and the tests of section 16 against the fakes of section 12.8.

**Feature flag.** `rwb.guarantee.stage2-read` (ASM-4550). Off: the operation answers 404 with MSG-P4-003 and the DP04 build is not wired.

**Done when.** The tests of section 16 pass; a scan of 5 claims on 2026-12-14 answers 5 distinct IDs over three pages, every claim type and status carries its label and the version of the day, and no statement, column or constant outside `rwb_guarantee` is used.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A window parameter is missing or inverted, or an unsupported query parameter is sent | Enter {field}. |
| MSG-GEN-003 | A page or a size is out of range | {field} is outside the accepted range {range}. |
| MSG-GEN-006 | The store or a reference-data version is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | The caller is not signed in | Sign in to continue. |
| MSG-P4-002 | A role without Treatment and offer R calls the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The feature switch is off, or a record is out of scope | The record was not found. |

For MSG-GEN-006 the {system} is "Guarantee claim" for the store and the list code for a missing version; no consumer re-words a message text. The DP04 messages MSG-P1-001 and MSG-P1-002 belong to rwb-source-data and are not restated here. Thai text for each message follows decision DL10.

### 15. Screens and states

No new screen. SCR-03 Case record shows the DP04 facts of a case and SCR-45 Data quality shows the DP04 breaks of the data steward, both composed by the gateway-bff route from the DP04 record read of rwb-source-data (DP-19). This service's read is called by the DP04 build and by no screen; SCR-17 Guarantee claim keeps the claim of the claim stories of this service and is unaffected, and its `Not due`, `due`, `submitted`, `paid` and `refused` labels are the screen's, not the read's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S3-E2010-APP-01 | AC1, BR3 | Component | "GCL-SYN-0901" at 2026-12-14T23:59:59+07:00 and "GCL-SYN-0902" at 2026-12-15T00:00:00+07:00; both windows |
| TC-S3-E2010-APP-02 | AC2, BR4, BR8 | Contract | A TCG claim of case "RW-2026-000512", deadline 2027-02-28, claimed amount 1,250,000.00, status FILED; reference data version "REF-2026.12" |
| TC-S3-E2010-APP-03 | AC3 | Component | 5 claims on 2026-12-14 with a page size of 2; the pages read twice; a size of zero and one above the maximum |
| TC-S3-E2010-APP-04 | AC4, BR5 | Component | RW-PHONECOL refused; RW-GUARANT reads a window with claims both inside and outside its scope |
| TC-S3-E2010-APP-05 | AC5, BR1, BR2 | Component | Migration, code and schema scan for a contract, plan or account fact, and for a foreign table or view |
| TC-S3-E2010-APP-06 | AC6, X5, X6 | Component | Store unavailable; reference data version unresolvable |

The nine legacy test cases TC-E2-010-01 to TC-E2-010-09 belong to RWB-P1-E2010-APP, which owns AC1 to AC8 of the legacy story; they are not re-tagged and not copied here (GAP-2738). The fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases, tab Story test cases, under the same ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not written by this story.

### 17. Guardrails

- No business value in code or in a migration: the page limits, the window bounds and every list member are data rows with a version (BR8; DP-07).
- No personal data in the answer, the logs or the tests beyond the claim and case identifiers: the fixture carries amounts, dates and codes, and no name, address, identity number or contact point.
- ACE data only through the owner's contract or the `v_ace_*` views of rwb-source-data; this service reads no ACE table and no view, and re-exposes no contract or plan fact (DP-05).
- No read of another service's table and no foreign key across schemas; the only table of this story is `guarantee_claim` in `rwb_guarantee` (DP-01).
- The read writes nothing: no state, no decision record and no outbox row on a read path (BR7).
- The reference-data version is stamped on every answer; an unversioned label fails the page instead of being served (BR8).
- The DP04 product, its access rows, its freshness stamp, its breaks and the case-link check stay with rwb-source-data; this service serves the facts and takes no publish decision (BR6).
- No call to the Thai Credit Guarantee Corporation or to NLEADS: their results arrive as facts recorded on the claim and on the case (legacy guardrail 4).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12; BR1 to BR4 of this story | TC-S3-E2010-APP-01, TC-S3-E2010-APP-02, TC-S3-E2010-APP-03 |
| REQ-RDF-010 | A role reads a data product only through its access row and its scope | Business Requirements Epic 2, section 4 | FEAT-CHO-09 | 07 Route, settle and claim | BR5 of this story | TC-S3-E2010-APP-04 |

The legacy rows of RWB-E2-010 and the traceability of the DP04 copy, the stamp and the catalog are held by RWB-P1-E2010-APP; the treatment half is RWB-S2-E2010-APP's.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-CON | Contract | C: declares the DP04 record read and the page shape the DP04 build sends; built against its fake |
| RWB-P1-E2010-APP | App development | Consumer: `Stage2ProductWorkflow`, `dp_guarantee_claim`, the References break and the DP04 stamp |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract that answers LOV-CLAIM-TYPE and LOV-CLAIM-STATUS with a version (DP-07) |
| RWB-S2-E2010-APP | App development | Sibling: the treatment half of the same split |
| RWB-S3-E4013-APP to RWB-S3-E4019-APP | App development | Siblings: the claim record, its preparation, submission, tracking, position and close, which own the write path of `guarantee_claim` |
| P1 rwb-source-data | Service | Owner of DP04, its copy, its access rows, its freshness stamp and its breaks |
| P3 rwb-case | Service | Owner of the reference data and of the case that each claim points at |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the read against the live owner, and the owner of the `-ITG` copies |

### 19. Out of scope

- AC1 to AC8 of RWB-E2-010, its nine test cases, the `dp_treatment` and `dp_guarantee_claim` copies, the active treatment count comparison, the References break list, the DP04 stamp, the catalog entry and the rerun, which are RWB-P1-E2010-APP.
- The treatment facts of the stage 2 product, which are RWB-S2-E2010-APP.
- The claim record itself, its write path, its states, its deadline timers and its negotiation and close, which are the claim stories of this service (RWB-S3-E4013-APP to RWB-S3-E4019-APP).
- The contract number, contract date and plan terms of the ACE views, which rwb-source-data reads at request time (DP-05).
- The access rows of DP04 and the data-product read of rwb-source-data, and the freshness stamp and deployment of the DP04 build.
- A count read for claims, a per-case claim read and any Kafka event of this service: no source names them and the ownership rows give S3 zero events (GAP-2738; ASM-4554).
- The screens, their composite routes and the deployment of this service (DP-19).
