# Technical Specification — RWB-E1-018 Case ID issuance and case record v1

| Field | Value |
|---|---|
| Story | RWB-E1-018 — Case ID issuance and case record v1 |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-040-epic-1-RWB-E1-018` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-004); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 018 Case ID issuance and case record v1 v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-004; REQ-CWC-001..005, REQ-CWC-016, REQ-CHO-004; US-RWB-E1-018; CTX-FEATURE-003; CTX-BUSINESS-014..016; DL15..DL17; R-UNI-16, R-UNI-39 |
| Status | `SUCCESS` — CLAR-009 resolved by decision D-RCV-30 (2026-11-06) |
| Prepared | 2026-11-04 |
| Regated | 2026-11-06 — Technical Specifier re-run after the primary-account ruling and the API-spec updates |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — SCR-02 Case list and SCR-03 Case record already exist and display the new case and its accounts. No screen, component, route, label or state is added; the full read-only view is RWB-E1-023. |
| Logic In Scope | `YES` — entry rule, exclusions, grouping, numbering, case and link creation, decision log, event and idempotency. |
| API In Scope | `YES` — this story first delivers `GET /cases/{caseId}` and `GET /cases/{caseId}/accounts`, and adds the optional `caseNo` query parameter to `GET /cases` (a contract delta against API Specification v2). |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion` (new), `decision_log_entry`, outbox, SCR-02, SCR-03, P1 data query. |
| New Nodes Required | `YES` — `CaseCreationJob`, `EntryRuleEvaluator`, `CaseGrouping`, `CaseNumberIssuer`, `CaseCreationService`, `CaseAndWorkflowRepository`, `CaseAndWorkflowController`, `CaseStatusCatalog`, `ExclusionRuleTable`. |
| Inherited Existing Behavior | RWB-E1-016 data products; RWB-E1-027 decision log writer; RWB-E1-042 `case.entry.dpd`; RWB-E1-043 exposure bands and status list; RWB-E1-044 migrations; JOB-01 LoadCompleted (P1). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | An account enters recovery when days past due is at or above the entry threshold. | SPEC-RWB-E1-018-002 | DIRECT | `case.entry.dpd` = 90 (DL16); boundary 90 enters, 89 does not. | COVERED |
| BR2 | One case per customer and product, with every qualifying account linked. | SPEC-RWB-E1-018-004 | DIRECT | Group by primary customer and product group; partial unique index on open case. | COVERED |
| BR3 | An account matching an exclusion row gets no case; the reason is recorded. | SPEC-RWB-E1-018-003 | DIRECT | `case_entry_exclusion` with reason, rule ID and version. | COVERED |
| BR4 | The case number is RW, the entry year and a six-digit number from a yearly sequence; issued once and never reused. | SPEC-RWB-E1-018-005 | DIRECT | `case_no_seq_YYYY`; `RW-YYYY-NNNNNN`; max 999999. | COVERED |
| BR5 | A new case has status NEW and no owner until allocation. | SPEC-RWB-E1-018-006 | DIRECT | Status from LOV-CASE-STATUS; `owner_user_id` null. | COVERED |
| BR6 | Status values are read from the list, not from code. | SPEC-RWB-E1-018-006 | DIRECT | `CaseStatusCatalog`; no Java enum. | COVERED |
| BR7 | No case is created from a load that failed its checks. | SPEC-RWB-E1-018-009 | DIRECT | JOB-02 starts only on a passed LoadCompleted. | COVERED |
| BR8 | Every case creation writes its decision log entry in the same transaction; a failed write rolls the creation back. | SPEC-RWB-E1-018-008 | DIRECT | `DecisionLogWriter.write` last before commit. | COVERED |
| BR9 | Exposure band is set from total outstanding at entry using the band table in force. | SPEC-RWB-E1-018-007 | DIRECT | LOV-EXPOSURE / reference band table. | COVERED |
| BR10 | A case created on bad data is canceled by rule, never deleted. | SPEC-RWB-E1-018-014 | DIRECT | R-UNI-16 is Epic 2; this story never deletes a case. | COVERED |
| AC1 | Account A-5001 creates RW-2026-000123 with status NEW, no stage, entry date 2026-12-01; A-5001 primary; P-0101 BORROWER; CaseCreated published. | SPEC-RWB-E1-018-001, SPEC-RWB-E1-018-005, SPEC-RWB-E1-018-006, SPEC-RWB-E1-018-012 | DIRECT | Last number RW-2026-000122. | COVERED |
| AC2 | A-5002 at 92 DPD with `tdr_flag=true` creates no case; exclusion record holds ACTIVE_PLAN, rule ID and EXCL-2026.11. | SPEC-RWB-E1-018-003 | DIRECT | Exclusion rows in force. | COVERED |
| AC3 | P-0102 with two HP accounts gets one case with both linked; total outstanding THB 412,350.00. | SPEC-RWB-E1-018-004, SPEC-RWB-E1-018-007 | DIRECT | Sum of balances; primary selection is CLAR-009. | COVERED |
| AC4 | A closed case's number is not reused; a new case gets the next number; the old case is still searchable by case number. | SPEC-RWB-E1-018-005, SPEC-RWB-E1-018-011 | DIRECT | Sequence never reuses; `caseNo` search. | COVERED |
| AC5 | A new status WAITING_COURT in LOV-CASE-STATUS is accepted without code change and the move records the list version. | SPEC-RWB-E1-018-006 | DIRECT | List load with valid from 2027-01-01. | COVERED |
| AC6 | An open-dispute account creates no case; the exclusion record holds OPEN_DISPUTE. | SPEC-RWB-E1-018-003 | DIRECT | Exclusion rows as data. | COVERED |
| AC7 | A-5006 at 89 DPD gets no case; A-5007 at 90 gets one. | SPEC-RWB-E1-018-002 | DIRECT | Threshold boundary. | COVERED |
| AC8 | A repeated JOB-02 run for the same date creates no second case, link or number. | SPEC-RWB-E1-018-010 | DIRECT | Idempotency by account and business date; open-case unique index. | COVERED |
| AC9 | A refused COLLINS load stops JOB-02; the job monitor shows MSG-P1-001; JOB-02 runs after the next good load. | SPEC-RWB-E1-018-009 | DIRECT | No case from stale data. | COVERED |
| AC10 | A decision log failure leaves no case, records A-5009 as failed with MSG-P7-003 and retries next run. | SPEC-RWB-E1-018-008 | DIRECT | Rollback of case, links, party and outbox. | COVERED |
| AC11 | At RW-2026-999999, no case is created; the job record carries MSG-P3-025 and an incident is raised. | SPEC-RWB-E1-018-005 | DIRECT | Year range exhausted. | COVERED |
| AC12 | P-0103 with a mortgage and an HP account gets two cases, one per product. | SPEC-RWB-E1-018-004 | DIRECT | Product is part of the grouping key. | COVERED |
| X1..X9 | Exceptional paths in the table below map to SPEC-003..011 and the access rule. | SPEC-RWB-E1-018-003..011 | DIRECT | Exclusion, existing case, 89 DPD, repeat, refused load, log failure, range, two products, access. | COVERED |

## User story intent interpretation

As a **product owner**, I want **every account at 90 days past due or more that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts, created by rule from the daily load**, so that **every team, letter and document refers to one case ID**.

The story is the entry point of the module. It creates the master case object from the COLLINS data product, blocks excluded accounts with a logged reason, links every qualifying account, and issues the identifier that every later document and decision carries. It adds no screen; SCR-02 and SCR-03 display the result.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `LoadCompleted` (EV-26) for source COLLINS with all checks passed; JOB-02 Case creation. |
| Preconditions | RWB-E1-016 data products readable through the P1 interface; RWB-E1-027 decision log writer available; `case.entry.dpd` = 90 in force (DL16); EXCLUSION rows loaded with DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN, OPEN_DISPUTE; exposure bands served by RWB-E1-043; JOB-01 passed for the business date. |
| Input | Account snapshots at or above the threshold, exclusion rows in force, exposure band table, business date. |
| Output | `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`; decision log entries; `CaseCreated`; job counts. |
| Feature flag | `rwb.p3.casecreation`. Off: JOB-02 does not create cases. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `case_no` | `CaseNumberIssuer` | System-written, never reused | `RW-YYYY-NNNNNN`, unique; max 999999 per year. |
| `recovery_case` | `status` | LOV-CASE-STATUS | System writes `NEW` | No owner; no stage code; no route. |
| `recovery_case` | `product_group` | Account snapshot | System-written | LOV-PRODUCT; part of the grouping key. |
| `recovery_case` | `primary_customer_id` | Account snapshot | System-written | Part of the grouping key. |
| `recovery_case` | `entry_date`, `dpd_at_entry` | Business date / snapshot | System-written | Entry date is the business date. |
| `recovery_case` | `total_outstanding_at_entry` | Sum of linked balances | System-written | `numeric(18,2)`; sum over the group. |
| `recovery_case` | `exposure_band` | Band table in force | System-written | Set from total outstanding (BR9). |
| `recovery_case` | `stage_code`, `owner_user_id`, `route_code` | — | Null at creation | Allocation (RWB-E1-020) sets owner and queue. |
| `case_account` | `is_primary`, `linked_from`, `linked_to` | Grouping | System-written | One primary per case: the account the case was opened on (D-RCV-30); `linked_to` null while open. |
| `case_party` | `party_role` | Primary customer | System-written | `BORROWER` for the primary customer. |
| `case_entry_exclusion` | `reason_code`, `rule_id`, `rule_version`, `business_date` | Exclusion row | System-written | Unique (account_id, business_date). |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | `LoadCompleted`, entry rule | DPD at or above 90, no exclusion, no open case for customer and product | `NEW` | Case, account links, party, decision log, `CaseCreated`. |
| None | Entry rule | Exclusion matched | No case | `case_entry_exclusion` with reason and version. |
| None | Entry rule | DPD below 90 | No case | Account read again next day. |
| `NEW` | Allocation rule matched | Handled by RWB-E1-020 | `ASSIGNED` | Not in this story. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Account matches an exclusion row | No case; exclusion record | None |
| X2 | Customer already has an open case for the product | Account linked to that case; no new case | None |
| X3 | DPD is 89 | No case; read again next day | None |
| X4 | JOB-02 runs again for the same date | No duplicate case, link or number | None |
| X5 | COLLINS load refused or late | JOB-02 does not start; runs after the next good load | MSG-P1-001 |
| X6 | Decision log write fails | Case not created; number not attached; retry next run | MSG-P7-003 |
| X7 | Yearly range RW-2026-999999 used | Creation stops for the year; incident raised | MSG-P3-025 |
| X8 | Customer has a Mortgage and an HP account | Two cases, one per product | None |
| X9 | Role without Case record R reads a case | 403; nothing returned | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Endpoints delivered | `GET /api/recovery/v1/cases/{caseId}`; `GET /api/recovery/v1/cases/{caseId}/accounts`; `GET /api/recovery/v1/cases` with the new optional `caseNo` query parameter. |
| Contract delta | Add `caseNo` (string, max 18, exact match) to `GET /cases`; it filters the caller's scope and returns `CasePage`. The two path endpoints return the `Case` and `CaseAccount[]` already defined in API Specification v2. No other field changes. |
| Backward compatibility | Additive and backward compatible; a request without `caseNo` behaves as before. |
| Authorization | Case record R with scope; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503. |
| Versioning | No API version bump; the OpenAPI file is updated with the optional query parameter before implementation. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | SCR-02 and SCR-03 are existing screens; no component, route, state or label changes. | Existing SCR-02 and SCR-03 tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-004; SPEC-RWB-E1-018-001..015 | New job, evaluator, grouping, issuer, service, repository and controller. | Positive, negative, boundary and error-path tests: entry, exclusion, grouping, two products, numbering, range, repeat, refused load, log failure, status list, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CaseCreationJob` | Job | JOB-02; listens for LoadCompleted; runs the entry rule per account; writes job counts. |
| `EntryRuleEvaluator` | Service | Applies the threshold and exclusion rows; returns ENTER or EXCLUDE with reason and rule version. |
| `CaseGrouping` | Service | Groups accounts by primary customer and product group; finds an open case to link to. |
| `CaseNumberIssuer` | Service | Draws from `case_no_seq_YYYY` and formats `RW-YYYY-NNNNNN`; refuses above 999999. |
| `CaseCreationService` | Service | Decision log write, then case, account links, party link and outbox event in one transaction. |
| `CaseAndWorkflowRepository` | Repository | `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`. |
| `CaseAndWorkflowController` | Controller | `GET /cases/{caseId}`, `GET /cases/{caseId}/accounts`, `caseNo` search on `GET /cases`. |
| `CaseStatusCatalog` | Service | Reads LOV-CASE-STATUS through the P4 list interface; no Java enum. |
| `ExclusionRuleTable` | Rule table | Rule rows with rule table EXCLUSION, read through `RuleTableReader` (P4). |

### Package and boundaries

`recovery.casewf.casecreation`, published `CaseRecordService` in the same package. Account and party
data come through `RecoveryDataQuery` (P1); rules through `RuleTableReader` (P4); the decision log
through `DecisionLogWriter` (P7). No module reads another module's tables.

### Data and migration

- Writes `recovery_case` (all columns), `case_account`, `case_party`, `case_entry_exclusion` (new),
  `outbox`.
- Partial unique index `ux_case_open_customer_product ON recovery_case (primary_customer_id,
  product_group) WHERE closed_date IS NULL`.
- Unique `case_account (account_id) WHERE linked_to IS NULL`, so an account is on one open case.
- `V<seq>__rwb_e1_018_case_creation.sql` creates `case_entry_exclusion` (id, account_id, business_date,
  reason_code, rule_id, rule_version, standard columns, unique (account_id, business_date)), the yearly
  sequences `case_no_seq_2026` and `case_no_seq_2027` (the job creates the next year each December),
  and the two indexes. Schema from `${recoverySchema}` (D-RCV-28).

### Entry and grouping

1. JOB-02 reads `case.entry.dpd` and asks P1 for accounts at or above it with no open case link.
2. `EntryRuleEvaluator` applies the EXCLUSION rows in force; a match writes
   `case_entry_exclusion` and stops.
3. `CaseGrouping` groups the remaining accounts by primary customer and product group.
4. An existing open case for the pair receives the new account link; otherwise a new case is created.
5. `total_outstanding_at_entry` is the sum of the group's balances; the exposure band is set from the
   band table in force.
6. `case_party` holds the primary customer as `BORROWER`.
7. `is_primary` is true for the account the case was opened on (D-RCV-30). For a case created from a
   grouped batch, the group's first eligible account in account-number order opens the case; accounts
   linked later never take `is_primary`. The rule is recorded in the data dictionary (DF-CAS-027).

### Numbering

- `CaseNumberIssuer` draws the next value from `case_no_seq_YYYY` and formats `RW-YYYY-NNNNNN`.
- The sequence never reuses a value after a case closes; a gap is allowed when a transaction rolls
  back, because the number was never attached to a visible case.
- Above 999999 the issuer refuses, creation stops for the year, the job record carries MSG-P3-025 and
  an incident goes to the platform administrator.
- The job creates the next year's sequence each December.

### Transaction and events

One transaction per case: case row, account links, party link and `CaseCreated` outbox row. The last
step before commit is `DecisionLogWriter.write` with decision code `D6`, final call `CASE_CREATED`,
the entry rule version and the inputs. A failure rolls back every write; the job record lists the
account as failed with MSG-P7-003 and the next run retries it.

`CaseCreated` (EV-01) carries caseId, caseNo, productGroup, accounts and businessDate. It is written to
the outbox in the same transaction and delivered after commit with retry and idempotency.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Publishes LoadCompleted; no case write | All |
| SY-CASEWF | Case record CRU; creates case, links and party | All |
| SY-RULES | Rules and parameters R; evaluates exclusion rows | All |
| SY-DECLOG | Decision log C; writes the entry | All |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and accounts | Per scope |
| RW-COE | Owns exclusion rows and threshold; loads through RWB-E1-029 and RWB-E1-042 | All |
| RW-REFADM | No Case record right; refused on the read endpoints | — |

### Observability and operations

- Job record: accounts read, excluded, linked, created and failed; business date; start/end.
- SCR-02 shows the new case with case number, product, status NEW and entry date; SCR-03 shows the case
  and its accounts.
- Metrics: cases created, exclusions by reason, links, failures, number range use.
- Alerts: JOB-02 waiting for a load; decision log failure; number range exhausted.
- No personal data in logs, events or test fixtures; cases are named by case number only.

### Performance

- 3,110 new accounts a month (DL15); JOB-02 runs after JOB-01 and before JOB-03.
- One transaction per case; the grouping query uses the open-case index.
- The case-number sequence is a database sequence; no table lock across the run.

### Feature flag and rollback

- `rwb.p3.casecreation`: off means JOB-02 does not create cases.
- Rollback: turn the flag off; redeploy the previous tag. Cases already created remain; a case created
  on bad data is canceled by rule (R-UNI-16, Epic 2), never deleted.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-018-01 | AC1, BR1, BR4, BR5 | System | A-5001 at 90 DPD; last number RW-2026-000122 | RW-2026-000123; NEW; primary; BORROWER; CaseCreated |
| TC-E1-018-02 | AC2, BR3 | System | A-5002 with `tdr_flag=true` | No case; ACTIVE_PLAN; EXCL-2026.11 |
| TC-E1-018-03 | AC3, BR2 | System | P-0102 with two HP accounts | One case; both linked; THB 412,350.00 |
| TC-E1-018-04 | AC4, BR4 | System | Closed RW-2026-000123 | New case RW-2026-000124; old searchable |
| TC-E1-018-05 | AC5, BR6 | System | WAITING_COURT added to the list | Accepted; list version on the decision log |
| TC-E1-018-06 | AC6, BR3 | System | A-5005 with open dispute | No case; OPEN_DISPUTE |
| TC-E1-018-07 | AC7, BR1 | System | A-5006 at 89; A-5007 at 90 | No case for 89; case for 90 |
| TC-E1-018-08 | AC8 | System | JOB-02 twice for 2026-12-01 | One link; no new number |
| TC-E1-018-09 | AC9, BR7 | System | Load refused at control total | JOB-02 does not start; MSG-P1-001 |
| TC-E1-018-10 | AC10, BR8 | System | Decision log unavailable for A-5009 | No case; MSG-P7-003; retry next run |
| TC-E1-018-11 | AC11, BR4 | System | Sequence at 999999 | No case; MSG-P3-025; incident |
| TC-E1-018-12 | AC12, BR2 | System | P-0103 mortgage and HP | Two cases, one per product |
| TC-E1-018-13 | X9 | Security | RW-REFADM reads a case | 403; MSG-P4-002 |
| TC-E1-018-14 | BR8 | Resilience | Decision log fails for the whole run | No case, links, party or outbox row |

## Guardrails and out of scope

- No business value in code: the threshold, exclusion reasons, bands and status list are data.
- No personal data in logs, tests, events or prompts; synthetic account and customer IDs only.
- Account and party data come through `RecoveryDataQuery` (P1); rules through `RuleTableReader` (P4).
- The case number is printed on every outbound document; other modules take it from
  `CaseRecordService`, never from a copy.
- Out of scope: allocation to a queue and owner (RWB-E1-020); prescription date at creation
  (RWB-E1-028); EFS history hand-over (RWB-E2-001); merging a duplicate (R-UNI-17) and canceling a
  case created in error (R-UNI-16), Epic 2; the full read-only case record view (RWB-E1-023).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-011 | `caseNo` is not in API Specification v2. | Adds a query parameter to an existing endpoint. | The story says "see additions"; add optional `caseNo`, exact match, max 18, backward compatible. The OpenAPI file is updated before implementation. | RESOLVED | SPEC-011 |
| CLAR-002 | BR4; SPEC-005 | Who creates the next year's sequence? | January creation would fail without it. | JOB-02 creates `case_no_seq_YYYY+1` each December, as the story states. | RESOLVED | SPEC-005 |
| CLAR-003 | BR4, AC11; SPEC-005 | Is a gap in case numbers allowed after a rollback? | Strict sequence vs no reuse. | Yes; the number was never attached to a visible case. "Never reused" is the rule, not "gapless". | RESOLVED | SPEC-005 |
| CLAR-004 | BR5, AC1; SPEC-006 | Is `stage_code` empty at creation? | Field matrix. | Yes; no stage code and no owner until allocation. | RESOLVED | SPEC-006 |
| CLAR-005 | BR9, AC3; SPEC-007 | Which band table applies? | Exposure band. | The LOV-EXPOSURE / band table version in force on the entry date. | RESOLVED | SPEC-007 |
| CLAR-006 | Flow 8; SPEC-008 | What decision code and final call are written? | Audit. | Decision code `D6`, final call `CASE_CREATED`, entry rule version and inputs. | RESOLVED | SPEC-008 |
| CLAR-007 | BR3, AC2; SPEC-003 | Which exclusion reasons are in Epic 1? | Rule rows. | DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN, OPEN_DISPUTE; version EXCL-2026.11. | RESOLVED | SPEC-003 |
| CLAR-008 | AC4; SPEC-011 | Does the case-number search include closed cases? | The AC requires the closed case to be returned. | Yes; `caseNo` searches all cases in the caller's scope, open and closed. | RESOLVED | SPEC-011 |
| CLAR-009 | BR2, AC3; SPEC-004 | When several accounts are grouped into one case, which account is `is_primary`? The source said only "the account the case was opened on" and did not state a selection rule. | Determines `case_account.is_primary`, and which account's contract number later notices use. | **Ruled 2026-11-06 as D-RCV-30:** `is_primary` is true for exactly the account the case was opened on; grouped accounts are non-primary; for a case created from a grouped batch, the group's first eligible account in account-number order opens the case, and later linked accounts never take primary. The wording is the Physical Schema v4 comment on `case_account.is_primary`, now recorded in the data dictionary for DF-CAS-027 with the determinism clause. | `RESOLVED` | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` — CLAR-009 is answered by decision D-RCV-30
and recorded in the data dictionary for DF-CAS-027. All other items are resolved.

## Status reporting

```text
MCP_STATUS_SUMMARY: RESOLVED — the primary-account rule is recorded as D-RCV-30 in the decision log and the data dictionary (DF-CAS-027).
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New case creation, numbering and read capability; existing case endpoints delivered with one new optional query parameter; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: case creation plus the caseNo query parameter on GET /cases]
REQUIREMENT_COVERAGE_SUMMARY: All 10 business rules, 12 acceptance criteria, 9 exception paths and 4 entry outcomes are mapped; one clarification is open.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
