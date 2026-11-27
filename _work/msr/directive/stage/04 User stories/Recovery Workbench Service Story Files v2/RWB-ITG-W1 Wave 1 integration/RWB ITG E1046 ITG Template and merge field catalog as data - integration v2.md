# RWB-ITG-E1046-ITG Template and merge field catalog as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1046-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None (the integration dependencies named in section 13 are not yet built) |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P6-E1046-APP, RWB-P7-E1046-APP, RWB-P5-E1046-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-OCC-001, REQ-OCC-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-046 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1046-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 19 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-046 template and merge field catalog across P3 rwb-case (the reference-load path), P1 rwb-source-data (the field registry), P6 rwb-comms (template and merge_field), P5 rwb-document (the body and the generated letter) and P7 rwb-decision (the approval decision)**, so that **a template change is proved as a data release before wave 1 exits**.

### 2. Business rationale

The legacy story keeps the catalog and the templates in the recovery schema with a P4 load path, checks every catalog row against sys_fields in the same module and lets the letter engine read the current version through an in-process published interface. The target puts the reference-load operations on P3 rwb-case (DP-07, Architecture v5 slides 14 and 41), the field registry on P1 rwb-source-data (the data dictionary contract of the data engine), the catalog rows on P6 rwb-comms (Architecture v5 slide 17: notices, templates, merge fields, proof of delivery), the template body on P5 rwb-document (the document hub and its Blob custody) and the Legal approval of a version as a decision record that reaches the rwb-decision ledger (DP-03, ADR-022). The split keeps every legacy check and changes only the owner of each artifact and the call type between them.

The legacy measures stand unchanged. A notice may only be produced from a Legal-approved template version whose merge fields the catalog knows, which serves REQ-OCC-001 and REQ-OCC-002 and the FSD P6 measure "notices with proof of delivery, 100 percent" under control CTL-14: every notice traces to one known template version and one catalog version in force. A template change is a data release approved by Legal and never a code release, so the same catalogue build proves the change without a deployment.

No service contract is faked. The suite exercises the published wave 1 contracts of the five services under their own per-service bases behind gateway-bff, and every call is one hop with a 2 s timeout (ADR-020, DP-11). Where the sources do not name the service that performs the field-ID check across the split, the container that holds the template body, or the point at which the approval of a version becomes a decision record, the suite asserts through the owners' contracts and records the open point as `Not specified in the source documents (GAP-0360; ASM-0469)`.

### 3. Preconditions

- RWB-P1-E1001-APP is done: the entity and field registry of rwb-source-data answers the data dictionary contract for every BR Field ID.
- RWB-P1-E1069-APP is done: the data dictionary and freshness surfaces of rwb-source-data are published and deployed in SIT.
- RWB-P6-E1046-APP is done: the template and merge_field tables live in rwb_comms, version numbering assigns the next version per template code and language, and the state is set from the approval columns.
- RWB-P5-E1046-APP is done: the body reference resolves through the document hub and a letter can be generated for a case.
- RWB-P7-E1046-APP is done: the central ledger collects rwb.decision.DecisionRecorded.v1 and answers the decision-log query.
- The published contracts of P1 rwb-source-data, P3 rwb-case, P5 rwb-document, P6 rwb-comms and P7 rwb-decision are deployed under their own per-service bases behind gateway-bff.
- Lists LOV-LANG, LOV-PRODUCT and LOV-NOTICE are loaded and in force on the business date.
- The merge field catalog file and the template files are prepared by the reference data administrator (RW-REFADM), one row per merge field with its BR Field ID, and the template files carry the Legal approval columns where Legal has signed.
- The catalog version MF-2026.11 is in force on the business date.
- The Blob container for the template body is available (Azurite in the lower environment) and body_ref names an object in it.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases and its clock control.
- No production data is used and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story, and there is no build dependency, so the story is ready on Day 1.

### 4. Flow

1. Harness: loads the 12-row merge field catalog file through the P3 reference-load path with table `merge_field` and the valid-from date; the P3 operation stores the load and the P6 handler answers for the rows.
2. Harness: verifies the load through the P3 verify operation and reads the refused rows; a refused load names the failing row check and stores no row.
3. Harness: loads the DEMAND-MTG TH version 2 file with the Legal approval columns, then reads the template versions and their state through the P6 contract.
4. Harness: reads version 2 and version 1 through the P6 content operation and asserts that version 1 is unchanged, with its own approver and approval date, and that both point at a body in the container.
5. Harness: loads the GUARANTOR-SSME file whose body uses the merge code GUARANTOR_EMAIL, which no catalog row defines, and reads the refusal.
6. Harness: repeats the first successful load with the same file hash and asserts that no new version is created and that DEMAND-MTG still has two versions.
7. Harness: generates one letter through the P5 generated-documents operation on the case, reading the template through the P6 catalog at generation time, and repeats the generation with the clock control on 2026-11-10, on 2026-11-30 and on 2026-12-01.
8. Harness: reads the approval decision of template DEMAND-MTG version 2 through the P7 decision log and compares the approver, the template code and the version.
9. Harness: posts the negative cases — a catalog row with no body_ref, a Draft-only template, a withdrawn version and a role without the reference-data right — and records every message and status.
10. Harness: writes the evidence report with the load results, the version numbers, the generated documents, the decision-log entry, the messages and the counts, and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Generation asks for a template whose versions are all Draft | The current version is refused; nothing is generated; the missing approval is named | MSG-P6-005 | AC7 |
| X2 | A template uses a merge code that is not in the catalog in force | The whole load is refused; the unknown merge code is named; no version is created | MSG-P6-006 | AC3 |
| X3 | A catalog row names a BR Field ID that is not in the data dictionary | The whole catalog load is refused in full; the check is named; no row is stored and the catalog version in force stays in force | MSG-P1-002 | AC1 |
| X4 | A template row has no template code, language or body reference | The whole load is refused; the field is named | MSG-GEN-001 | AC4 |
| X5 | The same template file is loaded twice | The second load creates no new version; the repeat is named | MSG-P1-002 | AC5 |
| X6 | The only Approved version is withdrawn | No current version is returned and generation holds | MSG-P6-003 | AC7 |
| X7 | A version has valid from in the future | The earlier Approved version stays current until that date | None | AC6 |
| X8 | A role without the reference-data right posts a load | Status 403; nothing is loaded and no version is created | MSG-P4-002 | AC8 |
| X9 | A consumed contract call exceeds the 2 s timeout or returns a server error | The step is retried under the pack policy; the evidence report records the call and the response; no load, version or generation result is asserted on unverified data | None | AC1, AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the five APP stories and the published contracts of P1, P3, P5, P6 and P7, not their source code |
| Negotiable | The merge codes, the template codes, the languages, the field mappings and the valid-from dates are data rows of the load files; the story fixes the checks, the current-version rule and the call set |
| Valuable | A template change is proved as a data release approved by Legal before wave 1 exits, and every check the legacy story held is proved across the five owners |
| Estimable | One suite module, one load-file fixture pack with its file hash, one clock control, one generation assertion and one evidence report |
| Small | Ten scenarios over five services; no service code and no schema change |
| Testable | Every scenario asserts a contract response, a version number, a version state, a generation result, a decision-log entry or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Template and merge field catalog as data, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-case, rwb-source-data, rwb-comms, rwb-document and rwb-decision are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used
    Given the merge field catalog version "MF-2026.11" is in force with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Given template "DEMAND-MTG" in language "TH" has version 1 Approved by user "LEG-0001" on 2026-10-01

  Scenario: AC1 A merge field catalog load is checked against the field registry and refused in full on an unknown field id (new, D-RCV-60)
    Given a catalog load file of 12 rows where row 7 names a BR Field ID "XX-CAS-999" that is not in the data dictionary
    When it is loaded through the P3 reference-load path with table "merge_field" on 2026-11-10
    Then the P6 handler checks every BR Field ID named by the file against the P1 data dictionary contract
    Then the system refuses the load in full with MSG-P1-002 naming the check "field ID not in the data dictionary"
    Then catalog version "MF-2026.11" stays in force
    Then no row of the file is stored

  Scenario: AC2 A template version is created with its Legal approval and the earlier version stays readable (new, D-RCV-60)
    Given a load file for template "DEMAND-MTG" language "TH" approved by user "LEG-0001" on 2026-11-10 with valid from 2026-11-10
    When it is loaded on 2026-11-10
    Then the system creates version 2 of "DEMAND-MTG" with state "Approved", approver "LEG-0001" and approval date 2026-11-10
    Then the P6 catalog returns version 2 as current for "DEMAND-MTG", "TH" on 2026-11-10
    Then version 1 stays readable with its own approver and approval date

  Scenario: AC3 A template that uses an unknown merge code is refused in full (new, D-RCV-60)
    Given a load file for template "GUARANTOR-SSME" whose body uses the merge code "GUARANTOR_EMAIL"
    Given "GUARANTOR_EMAIL" is not in the catalog
    When it is loaded
    Then the system refuses the load in full with MSG-P6-006 naming "GUARANTOR_EMAIL"
    Then the system creates no version of "GUARANTOR-SSME"

  Scenario: AC4 A template row with no body reference is refused in full (new, D-RCV-60)
    Given a template load file whose row has no body reference
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "body_ref"

  Scenario: AC5 A repeated load of the same file hash creates no new version (new, D-RCV-60)
    Given the load file of AC2 has been loaded once and version 2 exists
    When the same file with the same file hash is loaded again
    Then the system refuses the load with MSG-P1-002 naming the check "repeat of load"
    Then "DEMAND-MTG" still has 2 versions

  Scenario: AC6 The current version is chosen at generation time across the two services (new, D-RCV-60)
    Given version 3 of "DEMAND-MTG" "TH" is Approved with valid from 2026-12-01
    When a letter is generated for a synthetic case through the P5 generated-documents operation on 2026-11-10, on 2026-11-30 and on 2026-12-01
    Then the P6 catalog returns version 2 as current on 2026-11-10 and on 2026-11-30
    Then the P6 catalog returns version 3 as current on 2026-12-01
    Then the generated document is confirmed by rwb.document.DocumentStored.v1 and records the version it used

  Scenario: AC7 A Draft-only template and a withdrawn version leave no usable current version (new, D-RCV-60)
    Given template "RECALL-HP" in language "TH" has only version 1 in state "Draft"
    When the pack asks the P6 catalog for the current version of "RECALL-HP", "TH"
    Then the catalog refuses with MSG-P6-005 naming "RECALL-HP" version 1
    Given version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn"
    When a letter is generated for a synthetic case on 2026-11-20
    Then the catalog returns no current version and refuses with MSG-P6-003 naming "DEMAND-MTG"
    Then generation holds and no document is stored

  Scenario: AC8 A role without the reference-data right is refused at the load path (new, D-RCV-60)
    Given a user holds RW-LITOFF, a role without the reference-data right
    When the user posts a catalog load through the P3 reference-load path
    Then the service refuses the call with status 403 and MSG-P4-002
    Then nothing is loaded and no version is created

  Scenario: AC9 The approval of a template version reaches the decision ledger (new, D-RCV-60)
    Given the load of "DEMAND-MTG" "TH" version 2 approved by "LEG-0001" on 2026-11-10 completed
    When the pack reads GET /api/recovery/decision/v1/decision-log
    Then one entry names approver "LEG-0001", template "DEMAND-MTG" and version 2
    Then the entry is visible within five minutes of the load

  Scenario: AC10 No template body or merge value leaves the service in an event or a log (new, D-RCV-60)
    Given the events of the run on rwb.decision-record.v1 and rwb.document.events.v1 and the service logs of the run are collected
    When the pack searches them for the template body and for the resolved merge values
    Then they carry template codes, catalog versions, template versions and counts only
    Then a merge field marked personal_data carries no value in any event, log or evidence line

  Scenario: AC11 The business rules BR1 to BR9 of section 8 hold across the wave 1 services (new, D-RCV-60)
    Given the rules BR1 to BR9 of section 8 are in force
    When the pack runs the checks for each rule on the synthetic data set
    Then every rule BR1 to BR9 is confirmed by its check
    Then no service holds a copy of another service's table

  Scenario: AC12 A consumed call that fails or does not answer holds the generation and stores no document (new, D-RCV-60)
    Given the P6 catalog does not answer the generation call of a synthetic case
    When a letter is generated for the synthetic case through the P5 generated-documents operation on 2026-11-10
    Then the failed call is reported to the pack
    Then generation holds and no document is stored
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A template version is used only when its state is Approved and it carries the Legal approver and approval date | RWB-E1-046 BR1; REQ-OCC-002; CTL-14 |
| BR2 | The current version for a template code and language on a date is the Approved version with the highest version number whose valid from is on or before that date | RWB-E1-046 BR2; R-LIT-03 (template_status = current) |
| BR3 | A withdrawn template has no current version, and generation holds until Legal approves a new one | RWB-E1-046 BR3; R-LIT-04, R-LIT-06 |
| BR4 | Every merge code a template uses exists in the catalog in force, and every catalog row names a BR Field ID in the data dictionary | RWB-E1-046 BR4; REQ-OCC-001; Principle 1 |
| BR5 | A load with any refused row is refused in full and the previous catalog version stays in force | RWB-E1-046 BR5; refdata change process, step 3 |
| BR6 | Earlier versions are never changed or deleted; open cases keep the version they were generated under | RWB-E1-046 BR6; refdata change process, step 6; R-UNI-38 |
| BR7 | Templates are owned by Legal counsel as reference data | RWB-E1-046 BR7; DL28 |
| BR8 | P6 rwb-comms owns the template and merge_field rows, P1 rwb-source-data owns the field registry, P3 rwb-case owns the reference-load path and P5 rwb-document owns the body; no service holds a copy of another service's table and the pack reads each through its owner's contract | Architecture v5 slide 17 and slide 41; DP-01; ASM-0469; ASM-0470 |
| BR9 | The approval of a version is written as one local decision record by the owning service in its own schema and is collected into the P7 central ledger within five minutes; the pack reads the approval only through the ledger | DP-03; ADR-022; ASM-0472 |

Open decisions for section 8: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL28 (assumptions ASM-1861, ASM-1925, ASM-2093, ASM-2727). Each decision is still open and its assumptions apply until it closes.

### 9. State transitions

None for the case status. This story does not change a case status. It reads and asserts the template version state, the reference load state and the current-version selection.

| Object | State | Meaning |
|---|---|---|
| Template version | Draft | Loaded without an approver or an approval date; it is never a current version |
| Template version | Approved | Loaded with the Legal approver and approval date; it may be current from its valid-from date |
| Template version | Withdrawn | Withdrawn by Legal; it is no longer current and generation holds until a new version is Approved |
| Reference load | Loaded | Every row passed its checks and the rows are stored |
| Reference load | Refused | At least one row failed a check; no row of the file is stored and the catalog version in force stays in force |
| Reference load | In force | The loaded catalog version that every later load and every generation is checked against |

The pack moves a load from Loaded to Refused and a version to Withdrawn through the owners' contracts; it never writes a state directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the pack, seeds the synthetic fixtures, reads the evidence report |
| RW-REFADM, reference data administrator | Loads the catalog and template files and reads the reference load record |
| RW-LEGAL, Legal counsel | Is the approver named on a template version and owns the withdrawal of a version |
| RW-LITOFF, litigation officer | Reads templates and the catalog; posts a load in the negative case and is refused |
| RW-COE, center of excellence analyst | Reads the catalog and the data dictionary |
| Case workflow service identity | Asks the P6 catalog for the current version of a template at generation time |
| Service owner of rwb-case | Owns the reference-load path and the lists |
| Service owner of rwb-source-data | Owns the field registry and the data dictionary contract |
| Service owner of rwb-comms | Owns the template and merge_field rows, the version numbering and the state |
| Service owner of rwb-document | Owns the body, the container and the generated document |
| Service owner of rwb-decision | Owns the central ledger and the decision-log query |

No other role is in scope for this story. No delegation-of-authority level applies.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-045 | template (P6 rwb-comms) | id | Write (P6 rwb-comms) |
| DF-REF-046 | template (P6 rwb-comms) | template_code | Write (P6 rwb-comms) |
| DF-REF-047 | template (P6 rwb-comms) | template_version | Write (P6 rwb-comms) |
| DF-REF-048 | template (P6 rwb-comms) | language | Write (P6 rwb-comms) |
| DF-REF-049 | template (P6 rwb-comms) | product_group | Write (P6 rwb-comms) |
| DF-REF-050 | template (P6 rwb-comms) | body_ref | Write (P6 rwb-comms) |
| DF-REF-051 | template (P6 rwb-comms) | approved_by_legal | Write (P6 rwb-comms) |
| DF-REF-063 | template (P6 rwb-comms) | approved_by | Write (P6 rwb-comms) |
| DF-REF-064 | template (P6 rwb-comms) | approved_at | Write (P6 rwb-comms) |
| DF-REF-065 | template (P6 rwb-comms) | valid_from | Write (P6 rwb-comms) |
| DF-REF-066 | template (P6 rwb-comms) | channel | Write (P6 rwb-comms) |
| DF-REF-067 | template (P6 rwb-comms) | notice_type | Write (P6 rwb-comms) |
| DF-REF-068 | template (P6 rwb-comms) | signature_basis | Write (P6 rwb-comms) |
| DF-REF-069 | template (P6 rwb-comms) | merge_codes | Write (P6 rwb-comms) |
| Standard column | template (P6 rwb-comms) | state | Write (P6 rwb-comms) |
| DF-REF-252 | merge_field (P6 rwb-comms) | id | Write (P6 rwb-comms) |
| DF-REF-253 | merge_field (P6 rwb-comms) | merge_code | Write (P6 rwb-comms) |
| DF-REF-254 | merge_field (P6 rwb-comms) | source_entity | Write (P6 rwb-comms) |
| DF-REF-255 | merge_field (P6 rwb-comms) | source_field | Write (P6 rwb-comms) |
| DF-REF-256 | merge_field (P6 rwb-comms) | field_id | Write (P6 rwb-comms) |
| DF-REF-257 | merge_field (P6 rwb-comms) | is_required | Write (P6 rwb-comms) |
| DF-REF-258 | merge_field (P6 rwb-comms) | personal_data | Write (P6 rwb-comms) |
| DF-REF-259 | merge_field (P6 rwb-comms) | catalog_version | Write (P6 rwb-comms) |
| DF-REF-260 | merge_field (P6 rwb-comms) | valid_from | Write (P6 rwb-comms) |
| DF-REF-028 | lov_value (P3 rwb-case) | lov_code | Read |
| DF-REF-029 | lov_value (P3 rwb-case) | value_code | Read |
| Cross-service check and body location | template, merge_field, the field registry and the Blob container | The service that performs the field-ID check, the body container and the decision-record point | Not specified in the source documents (GAP-0360; ASM-0469) |

The read-or-write column keeps the legacy marking and names the owner that writes each row: template and merge_field are written by P6 rwb-comms, and this suite only reads them through the P6 contract. lov_value is reference data owned by P3 rwb-case under the default ruling and DP-07. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The pack provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/case/v1/admin/reference-loads | P3 rwb-case | Load the merge field catalog file and the template file with the table and the valid from date |
| POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify | P3 rwb-case | Verify a load and read the refused rows |
| GET /api/recovery/case/v1/admin/lists/{listCode} | P3 rwb-case | Read LOV-LANG, LOV-PRODUCT and LOV-NOTICE in force |
| GET /api/recovery/source-data/v1/admin/data-dictionary/fields | P1 rwb-source-data | Check every BR Field ID named by the catalog |
| GET /api/recovery/comms/v1/admin/templates | P6 rwb-comms | Read the template versions and their state |
| GET /api/recovery/comms/v1/admin/templates/{templateId}/content | P6 rwb-comms | Read the body reference and the merge codes of a version |
| POST /api/recovery/document/v1/cases/{caseId}/generated-documents | P5 rwb-document | Generate one letter so the catalog is read at generation time |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case the letter is generated for |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Read the approval decision record |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The pack publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | Every service; the ledger is owned by P7 rwb-decision | Follow the approval decision from the owning service into the central ledger |
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | Confirm that the generated letter was stored and read the version it used |

No event is produced by the pack. The ledger is complete within five minutes of the decision (ADR-022, DP-03).

#### 12.5 Workflows and activities

None. The letter is generated by the P5 generated-documents operation; no workflow is started by the pack, and the pack reads no workflow history.

#### 12.6 Schedules

None. The pack fires no Schedule and reads no Schedule state; the loads and the generations are triggered by the pack itself on the dates named in section 7.

#### 12.7 Tables owned

None. The pack owns no table and never reads another service's schema (DP-01).

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| Legal approval identity recorded on the load file | The approver named in the load file is the approval identity; no directory call is made |
| Azurite Blob container for the template body and the generated letter | The lower environment stands in for the managed container; the object layout is the production layout |
| Synthetic case and clock control (harness RWB-ITG-W1J01-ITG) | Supplies the case and moves the business date so the current-version rule can be read on three dates |

No service contract is faked: every call in section 12.2 goes to the real SIT service under its published wave 1 contract.

#### 12.9 Call-type summary

| Call type | Provided by the pack | Consumed by the pack |
|---|---|---|
| REST | 0 | 9 |
| Kafka | 0 | 2 |
| Temporal | 0 | 0 |
| File | 0 | 1 Blob container |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the ten scenarios against SIT and holds no service code |
| Load-file fixture pack | Test data | The 12-row catalog file, the DEMAND-MTG TH version 1 and version 2 files, the DEMAND-MTG TH version 3 file, the GUARANTOR-SSME file, the RECALL-HP file, the file with no body_ref, and the SHA-256 file hash of each |
| Current-version clock control | Harness control | Moves the business date to 2026-11-10, 2026-11-30 and 2026-12-01 and restores it after each assertion |
| Generation assertion | Assertion | Calls POST /cases/{caseId}/generated-documents on /api/recovery/document/v1 (P5 rwb-document) and reads the template version recorded on the stored document |
| Evidence report | Report | Records per scenario the load id, the refused rows, the version numbers and states, the generated documents, the decision-log entry, the messages and the counts |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | template and merge_field sit in rwb_comms (owner P6 rwb-comms), the body in the P5 schema, the field registry in P1; this story holds no table in any of them, reads the catalogue only through the P6 contract and asserts through contracts only |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The reference-load path (POST /admin/reference-loads, owner P3 rwb-case) and the three lists of section 12.2; on the APP stories, not a build dependency of the pack |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The nine consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The history of template and merge_field in rwb_comms; on the APP stories, the pack changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The reference load record is read through gateway-bff; no screen is built by this story |

The H, C, I and X lists are exactly those of the metadata table: no build dependency, no contract dependency, the five integration dependencies RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P6-E1046-APP, RWB-P7-E1046-APP and RWB-P5-E1046-APP, and no external dependency.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P1, P3, P5, P6 and P7.
2. Build the load-file fixture pack and record the SHA-256 file hash of every file as a data row.
3. Add the current-version clock control and the restore step for the three business dates.
4. Implement the twelve scenarios of section 7 in TC order and assert only through the contracts of section 12.2 and the events of section 12.4.
5. Add the load-result assertions: refused rows per load, the catalog version in force, the version number and state created, and the catalog version that stays in force on a refusal. The template load and its idempotency are asserted on the operation the legacy load maps to: POST /admin/templates on /api/recovery/comms/v1, with the legacy SHA-256 file hash as the idempotency key.
6. Add the generation assertion at the three business dates and compare the version used with the version the catalog reports as current.
7. Add the decision-log assertion and the log and event scan for template bodies and merge values, including the merge field marked personal_data.
8. Run the pack in SIT against the wave 1 release candidate and keep the evidence report with the wave exit evidence.

Done when: all eleven test cases pass in SIT against the published wave 1 contracts, the evidence report is attached to the wave exit pack, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | Generation asks for a template with no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A template uses a merge code not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-003 | The current version is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P1-002 | A catalog load fails a check, or repeats a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A required field is empty in a load row | Enter {field}. |
| MSG-P4-002 | A role without the reference-data right posts a load | You cannot {action} here. Your role does not include it. |
| RPT-E1046-GEN | Generation check report, one line per generated letter | Case {case} used template {template} language {language} version {version} on {date}; {count} merge codes resolved at generation time; no merge value recorded. |

The message IDs and wording are copied from RWB-E1-046. No new message ID is added by this story; RPT-E1046-GEN is an evidence report line, not a service message. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The reference data administrator loads files through the P3 reference-load path and reads the result on the reference load record, including the refused rows and the version numbers created. SCR-40 Reference data (states Versions; load) shows the template and merge_field tables with their versions when it is built. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-329). The template screen SCR-33 with upload, approval and withdrawal comes with RWB-E1-034 and is out of scope here.

| Screen (not built by this story) | States in Screen Specifications v1 | Empty state | Loading state | Error state | No access state |
|---|---|---|---|---|---|
| SCR-33 Template upload, approval and withdrawal | Not specified in the source documents (CG-ALL-328) | Not specified in the source documents (CG-ALL-328) | Not specified in the source documents (CG-ALL-328) | Not specified in the source documents (CG-ALL-328) | Not specified in the source documents (CG-ALL-328) |
| SCR-40 Reference data | Versions; load | Not specified in the source documents (CG-ALL-329) | Not specified in the source documents (CG-ALL-329) | Not specified in the source documents (CG-ALL-329) | Not specified in the source documents (CG-ALL-329) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-046-04-ITG | AC1, BR4, BR5, BR8 | Integration | Catalog file of 12 rows, row 7 with an unknown field ID "XX-CAS-999"; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-01-ITG | AC2, BR1, BR6 | Integration | Catalog MF-2026.11; DEMAND-MTG TH version 1 Approved by "LEG-0001" on 2026-10-01; load of version 2 approved on 2026-11-10 with valid from 2026-11-10; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-03-ITG | AC3, BR4 | Integration | GUARANTOR-SSME body using GUARANTOR_EMAIL, which is not in the catalog; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-05-ITG | AC4 | Integration | Template row with empty body_ref; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-06-ITG | AC5 | Integration | The DEMAND-MTG TH version 2 load file loaded twice under the same file hash; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-08-ITG | AC6, BR2, BR6, BR8 | Integration | DEMAND-MTG TH version 3 valid from 2026-12-01; generation on 2026-11-10, 2026-11-30 and 2026-12-01; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-02-ITG | AC7, BR1 | Component | RECALL-HP TH with one Draft version; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-07-ITG | AC7, BR3 | Integration | DEMAND-MTG TH version 2 withdrawn, generation on 2026-11-20; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-046-09-ITG | AC8, BR7 | Component | RW-LITOFF posts a catalog load through the P3 reference-load path; refused with 403 and MSG-P4-002; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1046-ITG-10 | AC9, BR9 | Integration | Approval of DEMAND-MTG TH version 2 by "LEG-0001" on 2026-11-10 read through GET /api/recovery/decision/v1/decision-log within five minutes; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1046-ITG-11 | AC10 | Contract | The events and the logs of one run, with one merge field marked personal_data; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1046-ITG-12 | AC11 | Integration | Synthetic data set; checks of BR1 to BR9 in section 8; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1046-ITG-13 | AC12 | Integration | P6 catalog not answering on the generation call of a synthetic case on 2026-11-10; end-to-end: real services on the wave 1 contracts; no numeric business values added |

The legacy full test text, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- No business value in code: template codes, languages, merge codes, field mappings and dates are data rows of the load files or properties of the suite.
- No personal data in logs, events, evidence or fixtures: template bodies in the fixtures use synthetic wording, and merge values never appear in a log, an event or an evidence line.
- No cross-service table read: every assertion goes through the owner's contract, and the pack owns no table (DP-01).
- One hop and a 2 s timeout on every call (ADR-020).
- Earlier template versions are never updated or deleted, and the pack never writes a version state.
- A merge field marked personal_data is resolved only at generation time; the pack asserts that it carries no value outside the generated letter.
- Synthetic data only, from the harness RWB-ITG-W1J01-ITG, and no production access of any kind from the pack or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | The P6 template and merge_field rows, the P1 field-registry check, MSG-P6-006, MSG-P1-002 | TC-E1-046-04-ITG, TC-E1-046-03-ITG |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | The P6 version, state and approval columns, the P7 decision log, MSG-P6-005, MSG-P6-003, MSG-GEN-001 | TC-E1-046-01-ITG, TC-E1-046-05-ITG, TC-E1-046-06-ITG, TC-E1-046-02-ITG, TC-E1-046-07-ITG, TC-E1-046-08-ITG, TC-E1-046-09-ITG, TC-ITG-E1046-ITG-10 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The nine consumed REST operations of section 12.2 | TC-E1-046-04-ITG, TC-E1-046-08-ITG, TC-ITG-E1046-ITG-11 |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the pack asserts through contracts | All |
| DP-15 | Per-service Flyway sequence in the service's own schema | The history of template and merge_field in rwb_comms; the pack changes no schema | TC-E1-046-01-ITG, TC-E1-046-06-ITG |
| ASM-0469 | The load path is P3 and P6 registers the handlers | POST /api/recovery/case/v1/admin/reference-loads and its verify operation | TC-E1-046-04-ITG, TC-E1-046-05-ITG, TC-E1-046-09-ITG |
| ASM-0470 | The field-ID check reads the P1 data dictionary | GET /api/recovery/source-data/v1/admin/data-dictionary/fields | TC-E1-046-04-ITG |
| ASM-0471 | The body stays in Blob through P5 and generation reads the catalog | POST /api/recovery/document/v1/cases/{caseId}/generated-documents; rwb.document.DocumentStored.v1 | TC-E1-046-08-ITG, TC-ITG-E1046-ITG-11 |

The legacy story is RWB-E1-046. The integration dependencies are RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P6-E1046-APP, RWB-P7-E1046-APP and RWB-P5-E1046-APP; the legacy AC1 to AC8 at component level belong to RWB-P6-E1046-APP, RWB-P5-E1046-APP and RWB-P7-E1046-APP, not to this story.

### 19. Out of scope

- The P1, P3, P5, P6 and P7 APP builds and their unit and component tests.
- The CON and OPS stories of those services.
- The legacy AC1 to AC8 at component level, which the sibling APP stories own.
- The template screen with upload, approval and withdrawal (RWB-E1-034).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- The Compliance approval path for a template (FEAT-ADM-05, Epic 8).
- The build of the harness RWB-ITG-W1J01-ITG.
- The NFR epic, including load and performance testing.
