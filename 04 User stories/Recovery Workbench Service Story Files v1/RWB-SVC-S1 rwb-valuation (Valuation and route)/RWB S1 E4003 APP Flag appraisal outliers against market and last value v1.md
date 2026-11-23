# RWB-S1-E4003-APP Flag appraisal outliers against market and last value

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4003-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-003 split out for rwb-valuation. Both legacy criteria of the key are copied word for word with their origin tags; the outlier check becomes a step of `RouteDecisionWorkflow` on task queue `rwb-valuation`, reads the new value, the previous value and the acceptance on the rwb-source-data data product (DP-05), takes the market benchmark and the gap rule as versioned inputs read with their version, never as constants, records the comparison and the flag through the local decision-record library before anything is written (DP-03) and answers the route operation on base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. The gap that counts as an outlier is not stated and no S1 rule package carries it (GAP-2596; ASM-4297); the market benchmark has no published owner, operation or element (GAP-2597; ASM-4298); the basis of the previous value is not fixed (GAP-2598; ASM-4299); the store of the flag is not fixed (GAP-2599; ASM-4300); the names of the consumed operations are not published (GAP-2600; ASM-4301); the trigger that starts the check is not named (GAP-2601; ASM-4302). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to compare the new value to the market and the previous value and flag the gap for a person**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-003. It owns:

- both legacy criteria of the key, AC1 and AC2, copied verbatim, and the rules, messages and screen states they depend on;
- the outlier check as a step of `RouteDecisionWorkflow` on `rwb-valuation`, run for the appraisal of the case under assessment;
- the read of the new value, its type and date, the acceptance and the previous value of the same asset on the rwb-source-data data product, one hop, 2 s, read only, with no `v_ace_*` grant of this service (DP-05);
- the market benchmark of the asset and the gap rule, taken as declared inputs with their version and never as a constant or a default;
- the comparison of the new value with the market benchmark and with the previous value, and the flag the rule in force raises on the gaps it names (FEAT-VAL-03; REQ-S1-002);
- the decision record of the check, written through RWB-PLT-E1027-CON in the caller's transaction before the flag is presented, with the rule version and the two deltas (DP-03);
- the presentation of the flag and its reasons before the value is accepted, so that the accept step of RWB-S1-E4004-APP fixes the band on a value a person has seen (R-DIL-09);
- the route operation `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, its right, its `Idempotency-Key` and its answer, whose shape is baselined by RWB-S1-E4003-CON (DP-13);
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4003-CON; the appraisal order and the appraisal intake, which are RWB-S1-E4001-APP and RWB-S1-E4002-APP; the acceptance of the value and the band it fixes, which is RWB-S1-E4004-APP; the ACE appraisal, valuation and acceptance facts and the freshness of the data product, which are rwb-source-data's (P1); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows and the central ledger, which are rwb-decision's (P7); the market model and the route agent behind it, which are rwb-agent's (P10); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the field list of SCR-13, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

A value that is far from the market and from the last value moves the expected return of every route the bank may take, and a value accepted without a look prices a settlement, a sale or a write-off on a number nobody checked. The FSD keeps the feature as FEAT-VAL-03 in module S1: the new value is compared with the market and with the previous value and the gap is flagged for a person, and the result is written to the decision log with its rule version. The requirement it serves is REQ-S1-002: a valuation that is an outlier against the market and the last value is flagged before it is accepted. The module measure is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records.

Under D-RCV-60 the facts change hands, and that is what this story carries.

- **the values are ACE's, not this service's.** `v_ace_valuation` is ACE's, and only rwb-source-data reads the `recovery.v_ace_*` views, so the new value, the previous value and the acceptance arrive on the owner's data product with a freshness stamp and are never read as a table here (DP-05).
- **the flag is a record before it is a screen.** The flag is worth nothing if it cannot be proved, so the comparison, both deltas, the rule version and the verdict are written before the value is presented, in the transaction of the step (DP-03; R-UNI-39).
- **the market is an input, not a call of this service.** The FSD names a model gateway as the system behind the market value, and no owner or operation is published for it, so the benchmark is declared as an input element of the step and this service asserts no model call of its own (GAP-2597).
- **the person decides, the rule flags.** R-DIS-16 to R-DIS-18 and R-DIL-09 read the flag as a gate before the value is accepted; the rule that settles the outlier is business-owned and versioned, and this story never states a threshold (BR-S1-003; GAP-2596).
- **nothing is published.** The ownership rows give S1 no event, so the step adds no name to `rwb.valuation.events.v1`; the fact reaches the ledger on `rwb.decision-record.v1` through the library and reaches the screen through the route answer (12.3).

### 3. Preconditions

- RWB-S1-E4003-CON is published: the route operation, the consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the appraisal of `v_ace_valuation`, the acceptance of `valuation_ext`, the previous value of the asset and the freshness stamp is published with its fake. Its operation name is Not specified in the source documents (GAP-2600; ASM-4301), and the row is not in this story's contract-dependency list, which is None.
- The market benchmark of the asset is a declared input element of the step with its source and its date; the FSD names a model gateway and no owner, operation or element is published, so the row carries the placeholder (GAP-2597; ASM-4298).
- The gap that counts as an outlier is a reference-data row or a rule row in force, read with its version and never written in code; the sources name neither the value nor the rule id of this step, and no S1 rule package is in force (GAP-2596; ASM-4297).
- The bases of the two comparisons are fixed as follows: the market benchmark per the row above, and the previous value as the latest prior appraisal of the same asset on the data product; the sources do not state which prior value is meant, so the basis is recorded on every flag (GAP-2598; ASM-4299).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_valuation`, `recovery.valuation_ext` or `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the flag is persisted outside the decision record is not fixed: the Ownership Map gives S1 no table, TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2599; ASM-4300).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4003-CON when its tests pass.

### 4. Flow

1. The route assessment of a case reaches the value step inside `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery`; the value it judges arrived on the rwb-source-data data product after ACE ingested the SVAF result (FEAT-VAL-02; DP-05).
2. The step reads, one hop with a 2 s budget and a breaker, the new value with its appraisal number, type and date, the acceptance fields of `valuation_ext`, the previous value of the same asset and the freshness stamp (GAP-2600).
3. If the product is stale after a late or failed ACE batch, the step holds, writes nothing, flags nothing and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (VR-S1-003-1, X3).
4. The step loads the market benchmark of the asset and the gap rule in force with its version. The threshold is never a constant: it is the versioned row the rule names, and where the row or the rule cannot be resolved the step flags nothing rather than inventing a limit (BR-S1-003; GAP-2596, X6).
5. The step computes two gaps: the new value against the market benchmark, and the new value against the previous value. Both are computed whatever the verdict, and both are recorded with the basis of the previous value that was used (GAP-2598).
6. The rule in force turns the two gaps into the flag: where it names the gaps as an outlier, the check returns flagged with its reasons; otherwise it returns clear with the same two gaps (FEAT-VAL-03; REQ-S1-002).
7. Before anything is presented or written, `AppraisalOutlierRecordWriter` writes one decision record through the local library: the case, the appraisal number, the new value, the market value, the previous value, both gaps, the flag, the threshold with its version and the rule id and version. A failed write stops the step with nothing changed (AC2; DP-03, R-UNI-39).
8. The flag and its reasons are presented to the person who accepts the value: they are part of the route answer and of SCR-13, and the accept step of RWB-S1-E4004-APP reads them before it fixes the band on the value (R-DIL-09; R-DIS-16 to R-DIS-18).
9. The step returns its outcome to the workflow, being flagged or clear, with the two gaps and the rule version; the case state stays rwb-case's and is reported, not written, by this service.
10. A repeat of the same assessment, or the same fact arriving twice, finds the record of the first and writes no second one and raises no second flag (R-UNI-40, X9).
11. A new appraisal on the data product re-runs the step at the next assessment of the case, and the earlier record stands as the evidence of the earlier flag (R-UNI-37).
12. SCR-13 Route decision shows the value, its two gaps, the flag and its reasons, and the states of the step, read through the gateway-bff composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no flag is presented and the route answer is refused | MSG-P7-003 | AC2, TC-E4-003-02, TC-E4-003-04 |
| X2 | The role does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-003-03 |
| X3 | The ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | TC-E4-003-01 |
| X4 | No market benchmark is available for the asset | The market gap is recorded as not computed for that basis, the previous-value comparison stands, and no benchmark is invented | Not specified in the source documents (GAP-2597; ASM-4298) | TC-E4-003-01 |
| X5 | The asset has no previous appraisal | The previous-value gap is recorded as not computed, the market comparison stands, and the record says so | None | TC-E4-003-01 |
| X6 | The gap rule or its reference-data row cannot be resolved | The step flags nothing and presents the value with the rule gap; no constant, default or branch stands in for the rule | None (gap log) | TC-E4-003-01 |
| X7 | rwb-source-data, rwb-case, rwb-decision or rwb-access does not answer inside 2 s, or its breaker is open | The step waits and is retried by the workflow; nothing is written and the caller sees 503 with the platform envelope | None | TC-E4-003-01 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR5, BR8 |
| X9 | The same assessment is submitted twice, or the same fact arrives twice | One record, one flag, and the stored answer is returned; the repeat is counted | None | TC-E4-003-01 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X7 are the paths of the target call types and of the two missing inputs, X8 is the DP-05 and DP-01 boundary and X9 the duplicate rule. No percentage, limit or threshold is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4003-CON, the rwb-source-data, rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P4 or P7 |
| Negotiable | The activity names, the decision code, the flag wording and the shape of the step outcome are this story's choice; the operation, the two comparisons, the rules, the messages, the screen and the appraisal elements are fixed |
| Valuable | A value far from the market and from the last value reaches the person who accepts it with its reasons, before the band is fixed |
| Estimable | One workflow step, two activities, five clients, one record write and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic appraisals through the contract fakes, plus the stopped record write, the stale product, a missing benchmark, a first appraisal and a duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Flag appraisal outliers against market and last value

  Scenario: AC1 Flag appraisal outliers against market and last value (legacy RWB-E4-003 AC1)
    Given the rwb-source-data contract mock returns the appraisal of asset "AST-2026-000403" with its appraised value, the market value of the same asset and the previous value of the same asset
    Given the rwb-decision contract mock returns the rule version of the outlier check in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then compares the new value to the market and the previous value and flags the gap for a person
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-003 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line stands character for character, including the legacy repetition of `Then`; what changes is who produces each fact and where it is asserted. The two added `Given` lines of AC1 stand in for the two cross-service facts the legacy monolith read in process: the appraisal, the market value and the previous value come from the rwb-source-data data product (DP-05), and the rule version in force comes from rwb-decision (DP-03). "The trigger" is no longer a monolith request but the value step of `RouteDecisionWorkflow` on task queue `rwb-valuation`, reached from the route assessment of the case (GAP-2601; ASM-4302). "Flags the gap for a person" is the flag element of the route answer and of SCR-13, read before the accept step fixes the band (R-DIL-09). "Writes the result to the decision log with the rule version" is the local `decision_record` row written in the same `rwb_valuation` transaction through the RWB-PLT-E1027-CON library, hash-linked and published to the central ledger of P7 (DP-03). AC2's "nothing changes" is the rollback of the one transaction that also holds the flag and the idempotency row. Neither criterion carries a business value: the threshold, the appraisal type and the route codes are data in force (BR-S1-003; GAP-2596).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S1-003 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-37 | A segment dimension changes after a correction upstream: recompute the segment and re-run the gates | None |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The VR and BR rows are those of FSD S1 A2.3.3.1, copied character for character. The four universal rules are the rows of Business Rules and Routing Logic v4 that this step depends on: R-UNI-38 is why the record carries the rule version in force, R-UNI-37 is why a corrected value re-runs the check, and R-UNI-39 is the legacy AC2.

| ID | Rule | Source |
|---|---|---|
| BR1 | The new value, the previous value, the acceptance and the freshness are ACE facts read only on the rwb-source-data data product; this service holds no `v_ace_*` grant, keeps no copy and reads no appraisal row as a table | DP-05; Ownership Map rows of S1; REQ-S1-002 |
| BR2 | The gap that counts as an outlier is a versioned reference-data or rule row, read in force on the business date; no percentage, distance, limit or appraisal type is a constant, a default or a branch of the build, and where the rule cannot be resolved nothing is flagged | FSD S1 A2.3.3.1 BR-S1-003; GAP-2596 |
| BR3 | Both comparisons are always computed and recorded with the basis used, being the market benchmark row and the previous appraisal of the same asset; a basis that is absent is recorded as not computed and never replaced by a guess | FSD S1 A2.3.2; GAP-2597, GAP-2598 |
| BR4 | The market benchmark is an input element of the step: this service calls no model gateway, no agent and no external system of its own | FSD S1 A2.3.2 integration points; GAP-2597 |
| BR5 | The flag reaches a person before the value is accepted: the accept step reads it, and a flagged value is presented with its reasons and its two gaps, never silently accepted | R-DIL-09; R-DIS-16 to R-DIS-18; REQ-S1-002 |
| BR6 | The decision is recorded before anything is presented or changed, with the rule id and version, the appraisal, the two gaps, the flag and the threshold version; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR7 | The case is not this service's: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the case state is read and reported | Ownership Map (`recovery_case` owner P3) |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the asset, the appraisal and the rule are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR9 | One check per assessment: a repeated command or a repeated fact writes no second record and raises no second flag | API-S1-001; R-UNI-40 |
| BR10 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4301 |
| BR11 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a screen payload or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case state is rwb-case's and this story does not write it: the step returns its outcome and the parent `CaseWorkflow` applies it. What this story owns is the state of the outlier step, and the appraisal states it reports are the ones the routing logic publishes for a value on its way to acceptance.

| From (outlier step) | Event | Condition | To |
|---|---|---|---|
| Not checked | The value step of the assessment | A fresh product carries the new appraisal | Checked, clear, with the two gaps recorded |
| Not checked | The value step of the assessment | The rule in force names the gaps as an outlier | Flagged, presented for acceptance with its reasons |
| Not checked | The value step of the assessment | The product is stale, or the rule cannot be resolved | Held, nothing flagged (X3, X6) |
| Checked, clear | The next assessment of the case | A new appraisal or a corrected value arrives (R-UNI-37) | Not checked, and the step runs again |
| Flagged | The person accepts the value | The accept step of RWB-S1-E4004-APP records the acceptance | Flagged, closed with the acceptance and its reason |
| Flagged | The person rejects the value | R-DIS-18 applies on the case of record | Flagged, and the appraisal is re-ordered by RWB-S1-E4001-APP |
| Any | The record cannot be written | X1 | Unchanged, nothing flagged and no answer (AC2) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The assessment reaches the value step | `RouteDecisionWorkflow` runs on `rwb-valuation` | Reading the values |
| Reading the values | The data product answers fresh | The new appraisal is present | Comparing |
| Comparing | The benchmark and the rule are resolved | Both gaps are computed | Recording |
| Recording | The record commits | The transaction commits | Returning the outcome |
| Any | The record write or the transaction fails | X1 | Waiting, nothing changed |

The states VALUATION_RECEIVED and VALUATION_ACCEPTED of the deed-in-lieu set (R-DIL-09, R-DIL-12) and REAPPRAISAL_RECEIVED, VALUE_ACCEPTED and VALUE_REJECTED of the asset-disposal set (R-DIS-16 to R-DIS-18) are case states applied by rwb-case on this step's outcome; the only one this story sets is the flag that stands between the value and its acceptance. No S1 route rule is in force, because the S1 package is Phase 2 (GAP-2596).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the route decision and read the value, its two gaps and the flag |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, matched to the right the legacy permission table gives |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: the approval of a route, which is a sibling story's and not this step's |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the data product, the benchmark and the rule, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs under the service identity with no officer task on the happy path. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a capability of the service template, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date, and the prior appraisal used as the previous value | Read only, on the rwb-source-data data product (DP-05) |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` (P1 data product; the acceptance is written by RWB-S1-E4004-APP) | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days | Read on the data product; not written here |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per check, before anything is presented |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-COL-018 to DF-COL-027, DF-COL-043 and DF-COL-044 | `valuation` as TSD S1 T3.1 declares it | id, appraised_value, appraisal_date, accepted, stale_flag, age_days | Not written here: the store of the flag and of the two gaps is not fixed (GAP-2599; ASM-4300) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read as a table: the case state arrives on the rwb-case row |
| The market benchmark elements | Owner Not specified in the source documents (GAP-2597; ASM-4298) | the market value of the asset, its source and its date | Consumed as a declared input, not stored |
| The outlier threshold row | Reference data, owner P3 rwb-case by the default ruling | the gap limit, its unit, its valid-from date and its version | Consumed, read with its version (GAP-2596) |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03).

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates, a gap and a rule version. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a screen payload or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy story names, and its shape is baselined by RWB-S1-E4003-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, with the route, the override reason code and the note of the request and the decision, its level, its amount and its status of the answer (API-S1-001; TSD S1 T-A.2) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second record is written |

The published `Approval` of API Specification v4 carries no appraisal, market or outlier element, so the flag reaches SCR-13 as a fragment of the composite route and reaches the ledger as the decision record, and the element that will carry it in the route answer is declared by RWB-S1-E4003-CON under the placeholder of GAP-2602 (ASM-4303). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer. No other operation is provided by this step.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal and acceptance data-product read (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The new value with its number, type and date, the acceptance fields, the previous value of the asset and the freshness stamp; faked |
| The market benchmark read (owner, operation and elements Not specified in the source documents (GAP-2597; ASM-4298)) | Not published; the FSD names a model gateway | Not specified (GAP-2597) | The market value of the asset, its source and its date; faked |
| The reference-data read of the gap rule (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/case/v1` | P3 rwb-case, by the default ruling | The gap limit in force with its unit and its version; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its asset link, checked before the check runs; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force for the check, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2600 with ASM-4301.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR10). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. FSD S1 A2.3.2 names three possible triggers, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the step runs inside `RouteDecisionWorkflow` when the assessment reaches it, and on the re-assessment that follows a corrected or new value, and it subscribes to nothing (GAP-2601; ASM-4302). The freshness of the data product is an element of the rwb-source-data row, and a duplicate fact is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the asset key, the route set and the rule package in force; signals: the freshness answer and the outcome of the value step |
| `checkAppraisalOutlier` | Activity, the comparison of this story | `rwb-valuation` | The new value, the market benchmark, the previous value and the gap rule in force in; the two gaps, the flag, the threshold version and the rule version out |
| `flagAppraisalOutlier` | Activity, the record and the presentation of this story | `rwb-valuation` | The appraisal, the two gaps and the flag in; the decision record, the idempotency row and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the route assessment and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. A batch-completion or valuer-report trigger is not built: no source names the event or the Schedule it would need (GAP-2601; ASM-4302).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the flag and the two gaps is not fixed (GAP-2599; ASM-4300) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per check (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8), `template` (P6), `deviation` (S8), `document` and `document_custody` (P5), every `v_ace_*` view and `valuation_ext` (P1). No foreign key leaves `rwb_valuation`: the case, the asset, the appraisal and the rule are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Asset `AST-2026-000403` with its new appraisal, its appraised value, its acceptance and its previous appraisal; the same asset with no previous appraisal; a stale product with its date; no answer beyond 2 s | AC1, X3, X5, X7 |
| Market benchmark fake | The market value of asset `AST-2026-000403` with its source and its date; an asset with no benchmark | AC1, X4 |
| rwb-case reference-data fake | The gap rule in force with its unit and its version; a rule that cannot be resolved | AC1, X6 |
| rwb-case case-state fake | Case `RC-2026-000403` at the route assessment with its asset link; a case in another state | AC1, X7 |
| rwb-decision rule and log fake | The rule id and its version in force; the record the ledger holds | AC1, AC2 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | X2, TC-E4-003-03 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000403`, with the value, the two gaps and the flag read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names and elements are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2597, GAP-2600).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data product, the market benchmark row, the rwb-case reference-data row, the rwb-case state, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `checkAppraisalOutlier` and `flagAppraisalOutlier` on `rwb-valuation`; no Schedule |
| File | None of this service | The appraisal report travels through SVAF and rwb-integration, and this service writes no file (GAP-2597) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `appraisaloutlier`, Java package `th.co.scb.ace.workbench.recovery.valuation.appraisaloutlier`; front end `src/modules/recovery/valuation/RouteAppraisalOutlier.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the new value, the previous value and the acceptance are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the step: the record, the idempotency row and the flag commit together or not at all. DP-13 moves the base of the one operation, and DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2600 (ASM-4301). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` value branch | Workflow | The value step of the route decision: waits for the assessment, runs the comparison, presents the flag and reports the outcome to the parent |
| `checkAppraisalOutlier` | Activity | Reads the values and the benchmark, resolves the gap rule with its version, computes both gaps and returns the flag and the versions |
| `flagAppraisalOutlier` | Activity | Writes the decision record and the idempotency row and returns the flag element and the outcome in one transaction |
| `SourceDataProductClient` | Client | The appraisal, acceptance and previous-value read of rwb-source-data, one hop, 2 s, breaker, with the stale path |
| `MarketBenchmarkClient` | Client | The market value of the asset as a declared input element, one hop, 2 s, with the absent-benchmark path |
| `ReferenceDataClient` | Client | The gap rule and its unit at their version in force, one hop, 2 s |
| `CaseStateClient` | Client | The case state and the asset link read of rwb-case, one hop, 2 s |
| `RuleInForceClient` | Client | The rule id and its version in force, from rwb-decision, one hop, 2 s |
| `AppraisalOutlierRecordWriter` | Library adapter | Writes one record per check before anything is presented, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteAppraisalOutlier` | React component | Shows the value, its two gaps, the flag and its reasons on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the flag or the gaps: they are computed per check and recorded, and the store is GAP-2599 until its owner names it.

**Configuration and reference data.**

- The gap rule that settles an outlier, with its unit, its valid-from date and its version, read as reference data or as a rule row and never as a constant (BR-S1-003; GAP-2596).
- The appraisal types of `LOV-APPRAISAL` and the route codes of `LOV-ROUTE` are read at their version in force; neither list is enumerated in code (TSD S1 T3.2).
- The market benchmark source and its date are an input; no endpoint, credential or model version of this service points at a model gateway (GAP-2597).
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard of the service template.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.

**Build steps**

1. The value branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the assessment as its trigger.
2. `SourceDataProductClient` against its fake, with the 2 s budget, the breaker, the stale path and the no-previous-value path (X3, X5, X7).
3. `MarketBenchmarkClient` and `ReferenceDataClient`, with the absent-benchmark path and the unresolved-rule path (X4, X6).
4. `RuleInForceClient` and `checkAppraisalOutlier`, with the flagged, clear and both-bases-absent paths.
5. `AppraisalOutlierRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `flagAppraisalOutlier` and the idempotency row, with the repeat of the same assessment (X9).
7. `CaseStateClient` and the state guard of the step.
8. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-003-03).
9. `RouteAppraisalOutlier` and SCR-13 through the composite route fake (TC-E4-003-01).
10. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_source_data`, and no outbox row (X8, BR8, BR10).

**Feature flag.** `rwb.valuation.appraisal-outlier-v1`, read as a flag of the platform library; off means the step records the two gaps without flagging and the value goes to acceptance unremarked, which the release note must state.

**Done when.** The tests of section 16 pass, a flagged value reaches the accept step with its two gaps and its reasons in SIT, a clear value reaches it with the same two gaps, a stale product writes nothing, an absent benchmark or an unresolved rule flags nothing and records why, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of a request or of the appraisal row is absent or invalid | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the flag is presented (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal is stale after a late or failed batch (X3) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are the rows of FSD S1 A2.3.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged. No message of the sources covers an absent benchmark or an unresolved rule, so those paths show the reason on the flag and record the gap rather than inventing a message (GAP-2596, GAP-2597).

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the value part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the values are read and compared; recommendation with the value, its two gaps and the flag with its reasons; overridden with the owner's reason for accepting a flagged value; submitted with the route answer. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, and held where a basis is absent or the rule cannot be resolved |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the value fragment, the two gaps and the four service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-003-01 | AC1: the value is compared with the market and with the previous value and the gap is flagged for a person, and the result is recorded with the rule version; a value inside the rule is not flagged; both gaps are recorded either way | Component | Case `RC-2026-000403` with asset `AST-2026-000403`, a new appraisal, its previous appraisal and the market benchmark; plus an absent benchmark and a first appraisal |
| TC-E4-003-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no flag, and MSG-P7-003 shown |
| TC-E4-003-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-003-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the flag and the record; no record, no flag and no event |
| TC-S1-E4003-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 10, plus an outbox that must stay empty |
| TC-S1-E4003-APP-02 | The trigger, the re-assessment and the duplicate: the step runs from the assessment, re-runs on a corrected value and writes one record for a repeated command | Component | Two assessments of the same case, one corrected appraisal and a repeated `Idempotency-Key` |

The four legacy case IDs are the legacy cases of RWB-E4-003 in their legacy order, with the Level column added. TC-E4-003-01 is Component because the step is tested on its fakes; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to the wave 3 harness and are owned by RWB-ITG-E4003-ITG.

### 17. Guardrails

- No business value in code: the gap rule, its unit, the appraisal types and the route codes stay reference data or rule rows read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input, in a screen payload or in a log: identifiers, codes, amounts, dates, gaps and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case, the rule with rwb-decision and the market model with rwb-agent: no `recovery_case`, `assignment`, `task` or `timer` row, no rule table and no model call is built here.
- The record is written before the flag is presented and the command is idempotent; a build that presents a flag before its record fails the review (DP-03, BR6, BR9).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-003, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-03 Flag appraisal outliers against market and last value, module S1, epic E4, systems SVAF and Model gateway, depends on FEAT-VAL-02 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.3.2 steps and integration points; A2.3.3.1 VR-S1-003-1 and BR-S1-003; A2.3.3.3 roles; A2.3.4.3 exception flows; requirements REQ-S1-002 and REQ-S1-008; SCR-13 | 2, 3, 4, 5, 8, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| API Specification v4 | `/cases/{caseId}/route`, `RouteRequest` and `Approval`, the 401, 403, 404, 409, 422 and 503 responses | 12.1 |
| Logical data model | DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-COL-018 to DF-COL-027, DF-COL-043 and DF-COL-044 | 11 |
| Routing logic | R-UNI-37, R-UNI-38, R-UNI-39 and R-UNI-40; R-DIL-09 and R-DIL-12; R-DIS-16 to R-DIS-18; no S1 route rule is in force, because the S1 package is Phase 2 | 4, 8, 9, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2596 to -6; ASM-4297 to -6; the route-answer element GAP-2602 belongs to RWB-S1-E4003-CON and is cited here where the answer is read | 1, 3, 4, 11, 12, 13, 14, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the route operation, the consumed rows, the decision-record element, the workflow elements, the error set, the fakes and the outlier element of the answer: RWB-S1-E4003-CON.
- The appraisal order and the appraisal intake: RWB-S1-E4001-APP and RWB-S1-E4002-APP.
- The acceptance of the value and the band it fixes, and the reason recorded with an acceptance or a rejection: RWB-S1-E4004-APP.
- The order of a fresh appraisal after a rejection: RWB-S1-E4001-APP, under R-DIS-18.
- The market model, the valuation agent and the model gateway themselves, their version, their confidence and their fallback: rwb-agent (P10) and the platform; no dependency of this story (GAP-2597).
- The ACE appraisal, acceptance and freshness facts: rwb-source-data (P1). The store of the flag and the two gaps: the data owner of this service (GAP-2599).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the ledger: rwb-decision (P7). The gap rule and its value: GAP-2596.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
