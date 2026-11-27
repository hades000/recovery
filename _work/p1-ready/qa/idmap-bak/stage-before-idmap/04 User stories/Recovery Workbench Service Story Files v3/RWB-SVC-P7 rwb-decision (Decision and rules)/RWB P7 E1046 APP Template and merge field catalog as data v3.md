# RWB-P7-E1046-APP Template and merge field catalog as data

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1046-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-M |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1046-CON |
| Contract version | v1 (major version 1 of RWB-P6-E1046-CON, base /api/recovery/comms/v1) |
| Readiness decisions | RD-P1-004 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-OCC-001, REQ-OCC-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: the P7 slice of RWB-E1-046. The template and merge-field catalog itself, its load, its version numbering, its Legal approval and its withdrawal are `rwb-comms`'s (RWB-P6-E1046-CON and RWB-P6-E1046-APP); this story holds the decision side of the same legacy key: the template version, the catalog version in force and the merge-field set that an answer used, kept as data rows in `rwb_decision` and checked against the catalog owner's contract before the answer is accepted. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1046-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal audit lead (RW-AUDIT) and a decision approver inside their authority**, I want **the template version, the merge-field catalog version and the merge-field set that each answer used held as data rows in `rwb_decision`, resolved through the catalog owner's contract on the business date and refused in whole when that version is unapproved, withdrawn or names a merge code the catalog does not hold**, so that **an answer can be explained months later by the exact template and catalog version that produced it, without any template code, merge code, language or catalog version being written in code and without this service holding a second copy of the catalog**.

This is one slice of RWB-E1-046, and the split is fixed by the Ownership Map and by the sibling slices:

- **P6 rwb-comms** owns the catalog as data: `template` and `merge_field` in `rwb_comms`, the versions, the Legal approval and the withdrawal, the merge-field checks and the current-version selection (RWB-P6-E1046-CON, RWB-P6-E1046-APP).
- **P7 rwb-decision**, this story, owns the record side: one `template_use` row per answer it accepts, naming the template code, the language, the version, the catalog version in force, the merge codes used, the notice type, the product group, the approver reference and the valid-from date of the version, plus the refusals that keep an unapproved, withdrawn or unknown field out of the record.
- Not this story's: the load path, the version numbering, the approval and withdrawal operations, the delivery of a notice (RWB-P6-E1052), the notice approval screen (RWB-P7-E2014) and the cross-service proof (RWB-ITG-E1046-ITG).

This story owns **no legacy acceptance criterion**. The eight criteria of RWB-E1-046 are owned by RWB-P6-E1046-APP; the eight criteria in section 7 are new, tagged `(new, D-RCV-60)`, and test only the deliverable above (GAP-2453; ASM-4064).

### 2. Business rationale

A notice or an approval is only defensible if the record says which wording and which field catalog produced it. That is the whole point of legacy RWB-E1-046: a template change is a data release approved by Legal and never a code release, and the letter engine can only fill fields the catalog knows. The legacy story put the catalog and the record in one module, so the entry could read the catalog rows directly.

D-RCV-60 separates the two owners. The catalog stays one catalogue owned by the service that holds the notices (P6 rwb-comms, schema `rwb_comms`, DP-01); the decision service may not read those tables and may not keep a second copy that could drift, so it consumes them through the published contract of RWB-P6-E1046-CON, one hop and a 2 s timeout (DP-11, ADR-020), and stores only the values of the answer it decided. The FSD P7 module already asks for exactly this: the D7.1 notice decision record holds decision code D7.1, rule R-LIT-03 and template DEMAND-MTG version 2 (FSD P7 A2.10, AC-P7-010-01), and an approval on a withdrawn template is refused with MSG-P6-003 (FSD P7 A2.22, AC-EXC-P7-022-02).

What changes in the microservice:

1. The monolith read `template` and `merge_field` inside the same module. Here the values arrive only through the catalog contract of RWB-P6-E1046-CON and are stored once, on the row that explains the answer (BR8, BR10).
2. The version is resolved on the **business date of the answer**, not on the date of a load: the Approved version with the highest version number whose valid from is on or before that date, and the catalog version in force on the same date (BR2, AC6). A version with a future valid-from date changes nothing until its date arrives.
3. The refusals of the legacy story move with the check: an unapproved version (MSG-P6-005), a withdrawn version (MSG-P6-003) and an unknown merge code (MSG-P6-006) now refuse the **answer**, not a load, because this service loads nothing (BR3, BR4, AC2 to AC4).
4. `sys_fields` is no longer read at all: the BR Field ID of a merge code is the catalog owner's check, and this service stores the merge **codes** it was given and never a value (BR12).

It serves REQ-OCC-001 and REQ-OCC-002 on the record side. The legacy values stand unchanged: the template codes `DEMAND-MTG`, `RECALL-HP` and `GUARANTOR-SSME`, the merge codes `CASE_NO`, `CUSTOMER_NAME`, `POSTAL_ADDRESS`, `TOTAL_OUTSTANDING`, `NOTICE_DATE` and `GUARANTOR_EMAIL`, the approver `LEG-0001`, the catalog version `MF-2026.11` and the dates of the legacy scenarios.

Three points no source settles are carried as the placeholder and as one gap with one assumption each: the slice boundary itself, because the FSD P7 module claims FEAT-DRI-16 while the Ownership Map gives `template` and `merge_field` to P6 (GAP-2453; ASM-4064), the row name and columns of the snapshot table (ASM-4065) and the exact read paths of the catalog contract (ASM-4067 and ASM-4068).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E1046-CON | The published catalog contract of `rwb-comms`: the current version of a template code and language on a date, the merge-field set of a version, the catalog version in force, the state and approval fields, and the message IDs. The story's only contract dependency (C) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client and the `rwb-case` reference-data contract (DP-07): LOV-NOTICE and LOV-PRODUCT in force, with their fake |
| RWB-PLT-E1044-CON | The per-service Flyway sequence of `rwb_decision` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which the decision-log view reads the values |
| RWB-P7-E1027-APP, RWB-P7-E2005-APP | The entry the row explains (the decision-record writer) and the read that projects the values (the decision-log query). Both are reused, neither is built or changed here |
| RWB-P6-E1046-APP | The sibling that owns the catalog, its load, its versions and its approvals; it is not built, loaded or approved here |

Business preconditions:

- Catalog version "MF-2026.11" is in force with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"; template "DEMAND-MTG" in language "TH" has version 1 Approved by "LEG-0001" on 2026-10-01 and version 2 approved on 2026-11-10 with valid from 2026-11-10 (legacy values, kept as fixtures).
- Lists LOV-NOTICE and LOV-PRODUCT are in force on the business date: "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE", "GUARANTOR_NOTICE" and "MORTGAGE", "HIRE_PURCHASE", "SSME", "UNSECURED".
- The template version named on an answer is a value the caller supplies; a version that is not in the catalog answer is refused, never created here.
- The approver reference on a version is a staff identifier such as "LEG-0001" on the file and a `USER_REF` uuid in the target model; the conversion between the two is Not specified in the source documents (GAP-1066; ASM-4071).
- The `rwb_decision` schema and the rwb-decision login exist (DP-01, DP-02); the login name is Not specified in the source documents (GAP-2453; ASM-4070).
- The catalog read path, the merge-field read path and the catalog-version read path are Not specified in the source documents (GAP-2453; ASM-4067, ASM-4068, ASM-4069).
- The release date 30 November 2026 is tentative; a date is never a condition of this story.

### 4. Flow

1. The caller (an approval decision on a D7.1 notice, or any answer that names a template) hands in the template code, the language, the notice type and the merge codes it used, with the business date of the answer. No template code, merge code, language, notice type or catalog version is written in code (BR10).
2. rwb-decision reads the current version of that template code and language **on the business date** through the catalog contract of RWB-P6-E1046-CON, one hop with the 2 s budget, a single GET retry with jitter and a breaker per downstream (DP-11, BR2, BR11).
3. The answer is refused when the catalog answers no Approved version (MSG-P6-005 naming the template and the version), when the only version in force is Withdrawn (MSG-P6-003 naming the template), or when the template code, language or business date is missing (MSG-GEN-001 naming the field).
4. rwb-decision reads the merge-field set of that version and the catalog version in force on the same business date through the same contract, and compares it with the merge codes the caller used.
5. A merge code that the catalog version in force does not hold refuses the answer in whole with MSG-P6-006 naming the template and the code; the refusal names no merge value, because none is present (BR4, BR12).
6. rwb-decision validates the notice type and the product group against LOV-NOTICE and LOV-PRODUCT read from the `rwb-case` reference-data contract at the version in force (DP-07, BR9).
7. rwb-decision writes one `template_use` row in `rwb_decision`: the entry reference it explains, the template code, the language, the template version, the catalog version in force, the merge codes, the notice type, the product group, the approver reference, the valid-from date of the version and the business date (BR1, AC1).
8. The row and the answer are one unit of work: when the row cannot be written the answer is refused and nothing is recorded (BR13, AC5).
9. The values are read back on the decision-log view through the gateway-bff composite route (DP-19), which projects the row of the entry the reader asked for; this story provides no read of its own (section 12.1).

Nothing here loads a template, numbers a version, approves or withdraws a version, resolves a merge value, generates a notice or changes a case status.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The catalog answers no Approved version for the template code and language | The answer is refused in whole; no row, nothing recorded | MSG-P6-005 | AC2 |
| X2 | The only version in force is Withdrawn | The answer is refused in whole; nothing recorded | MSG-P6-003 | AC3 |
| X3 | The answer names a merge code the catalog version in force does not hold | The answer is refused in whole; the code is named; no value is echoed | MSG-P6-006 | AC4 |
| X4 | The template code, the language or the business date is missing on the answer | The answer is refused and the field is named | MSG-GEN-001 | AC1 |
| X5 | The catalog read or the reference-data read does not answer inside the 2 s budget, or answers 503 | The answer is refused with the system that failed; no row is written and nothing partial is stored | MSG-GEN-006 | AC5 |
| X6 | The notice type or the product group is not in the list in force | The answer is refused and the list and the value are named | MSG-GEN-001 | AC8 |
| X7 | An UPDATE or a DELETE is attempted on a `template_use` row | Refused; the row is append only and the answer keeps the version it was decided under | None (the database refusal) | AC1, AC7 |
| X8 | The template version has a valid-from date in the future | The earlier Approved version stays the one recorded until that date; no other change | None | AC6 |
| X9 | The catalog returns a version whose state is neither Approved nor Withdrawn, or an unknown template code | The answer is refused as unapproved, because no state other than Approved may be recorded | MSG-P6-005 | AC2 |

X1 to X4 are the legacy X1 to X5 family on the record side: the refusals that kept a bad version or an unknown field out of a letter now keep them out of the record. X5 is the microservice failure of DP-11, X6 the list check of DP-07, X7 the append-only rule and X8 the effective-dating rule of the legacy AC8.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P6-E1046-CON, the reference-data contract, the Flyway convention and the gateway route, each with the fake of section 12.8; the entry and the read of RWB-P7-E1027-APP and RWB-P7-E2005-APP are reused |
| Negotiable | The template codes, merge codes, languages, notice types, product groups and dates are data of the catalog and the lists; the story fixes only what is recorded, what is refused and how the version is selected |
| Valuable | An answer is explainable after the fact by the exact template version and catalog version that produced it, and an unapproved, withdrawn or unknown-field version can never be recorded |
| Estimable | One recorder, one catalog client, one merge-field checker, one entity, one repository and one migration |
| Small | One sprint with its tests; the catalog it reads is P6's and is not touched |
| Testable | Every criterion runs on synthetic rows against a catalog fake and a list fake, with a fixed business date and no production data |

### 7. Acceptance criteria

```gherkin
Feature: The template version and merge-field set of an answer held as data in rwb-decision

  Background:
    Given the rwb-comms catalog mock returns catalog version "MF-2026.11" in force on 2026-11-20 with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Given the rwb-comms catalog mock returns template "DEMAND-MTG" in language "TH" with version 2 Approved by user "LEG-0001" on 2026-11-10 and valid from 2026-11-10
    Given the rwb-case reference-data mock returns LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE" and LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"

  Scenario: AC1 An accepted answer stores the template version and the catalog version as data (new, D-RCV-60)
    Given an answer on case "RC-2026-000123" that names template "DEMAND-MTG" language "TH" version 2, notice type "DEMAND", product group "MORTGAGE" and merge codes "CASE_NO" and "TOTAL_OUTSTANDING"
    When rwb-decision records the answer on the business date 2026-11-20
    Then one template_use row is written in rwb_decision with templateCode "DEMAND-MTG", language "TH", templateVersion 2, catalogVersion "MF-2026.11", noticeType "DEMAND", productGroup "MORTGAGE" and mergeCodes "CASE_NO" and "TOTAL_OUTSTANDING"
    Then the row carries approver "LEG-0001", the version validFrom 2026-11-10 and the entry reference it explains
    Then the row carries no merge value and no template body
    Then an update and a delete of the row are refused, and the answer keeps the version and the catalog version it was decided under
    Given an answer that carries no template code
    When it is recorded
    Then it is refused with MSG-GEN-001 naming the field "template code" and no row is written

  Scenario: AC2 An answer that names an unapproved version is refused (new, D-RCV-60)
    Given the rwb-comms catalog mock returns template "RECALL-HP" language "TH" whose only version 1 is in state "Draft"
    When an answer names "RECALL-HP" "TH" version 1 on 2026-11-20
    Then the answer is refused with MSG-P6-005 naming "RECALL-HP" version 1
    Then no template_use row is written for the answer and nothing is recorded
    Given the catalog mock answers a version of "RECALL-HP" whose state is neither "Approved" nor "Withdrawn", and answers no template for the code "UNKNOWN-XX"
    When each is recorded
    Then each answer is refused with MSG-P6-005 naming "RECALL-HP" and "UNKNOWN-XX" and no row is written, because only an Approved version is recorded

  Scenario: AC3 An answer that names a withdrawn version is refused (new, D-RCV-60)
    Given version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn" with no later Approved version
    When an answer names "DEMAND-MTG" "TH" on 2026-11-20
    Then the answer is refused with MSG-P6-003 naming "DEMAND-MTG"
    Then no template_use row is written and the earlier row of the same case stays readable
    Then this story changes no notice state and no case state, and the hold that MSG-P6-003 describes remains the notice path's at RWB-P6-E1052

  Scenario: AC4 An answer that names an unknown merge code is refused (new, D-RCV-60)
    Given an answer on template "GUARANTOR-SSME" whose merge codes include "GUARANTOR_EMAIL"
    Given "GUARANTOR_EMAIL" is not in catalog version "MF-2026.11"
    When the answer is recorded
    Then the answer is refused in full with MSG-P6-006 naming "GUARANTOR-SSME" and "GUARANTOR_EMAIL"
    Then no template_use row is written and catalog version "MF-2026.11" stays in force
    Then the refusal echoes no merge value and stores none

  Scenario: AC5 An unanswered catalog read refuses the answer and stores nothing (new, D-RCV-60)
    Given the rwb-comms catalog mock returns 503 for the current-version read, and a second call answers beyond the 2 s client budget
    When rwb-decision records an answer on 2026-11-20
    Then the answer is refused with MSG-GEN-006 naming the catalog read of rwb-comms
    Then no template_use row is written and no partial row is left behind
    Given the rwb-case reference-data mock answers beyond the 2 s budget
    When the answer is recorded
    Then the answer is refused with MSG-GEN-006 naming the reference-data read of rwb-case and nothing is written

  Scenario: AC6 The version recorded is the one in force on the business date (new, D-RCV-60)
    Given the rwb-comms catalog mock returns version 2 with valid from 2026-11-10 and version 3 of "DEMAND-MTG" "TH" Approved with valid from 2026-12-01
    When an answer is recorded on 2026-11-30 and another on 2026-12-01
    Then the first row names templateVersion 2 and the second names templateVersion 3
    Then no code change, no rebuild and no release is needed between the two, and the two rows stay readable with their own version and valid-from date
    Given catalog version "MF-2026.12" is in force from 2026-12-15 with the merge code "NOTICE_DATE" added
    When an answer is recorded on 2026-12-20 using "NOTICE_DATE"
    Then its row names catalogVersion "MF-2026.12" and the earlier rows keep "MF-2026.11"

  Scenario: AC7 rwb-decision holds no catalog table and reads none (new, D-RCV-60)
    Given the migration of this story applied to an empty rwb_decision schema
    Then it creates template_use and no template and no merge_field table, and it adds no foreign key into another schema
    Then no table of rwb_decision carries a copy of a template body, a merge code list or a catalog version in force
    When the service records an answer
    Then every catalog value comes through the contract of RWB-P6-E1046-CON and every list value through the reference-data contract of RWB-P3-E1043-CON
    Then a search of the service shows no read of a rwb_comms table, no read of a rwb_case table and no read of sys_fields
    Then the six owned tables of P7 plus template_use are the only tables the story names, and the outbox, inbox and idempotency tables are the platform library's

  Scenario: AC8 The values are data, never code, and the lists are the owner's (new, D-RCV-60)
    Given a new template code, a new merge code or a new notice type added as data at rwb-comms and rwb-case
    When an answer that uses it is recorded
    Then the answer is accepted with no code change, no rebuild and no release of rwb-decision
    Then no template code, merge code, language, notice type, product group, catalog version or date appears in the service code or in a resource file
    Given an answer whose notice type is "STATUTORY_SALE_NOTICE" and an answer whose notice type is "COURT_FILING" while LOV-NOTICE holds no such value
    When each is recorded
    Then the first is accepted and the second is refused with MSG-GEN-001 naming the list LOV-NOTICE and the value "COURT_FILING"
```

The eight criteria are new, test only the record side of the legacy key and copy no legacy criterion: RWB-E1-046 AC1 to AC8 are owned by RWB-P6-E1046-APP, and the cross-service proof of the same values is RWB-ITG-E1046-ITG. Every value used is the legacy value of RWB-E1-046 or of FSD P7 A2.10, A2.11 and A2.22 (GAP-2453; ASM-4064). `Given the rwb-comms catalog mock returns …` and `Given the rwb-case reference-data mock returns …` name the contract through which each cross-service value is stubbed, so no test reads another service's schema.

### 8. Business rules

| BR | Rule | Source |
|---|---|---|
| BR1 | Only a version in state Approved, carrying the Legal approver and the approval date, may be recorded; the row keeps the approver and the valid-from date it was given | RWB-E1-046 BR1; REQ-OCC-002; CTL-14 |
| BR2 | The version in force on a business date is the Approved version with the highest version number whose valid from is on or before that date, and the catalog version in force is chosen on the same date | RWB-E1-046 BR2; R-LIT-03 (template_status = current) |
| BR3 | A withdrawn version has no current version, so an answer that would need one is refused and nothing is recorded | RWB-E1-046 BR3; R-LIT-04, R-LIT-06 |
| BR4 | Every merge code an answer uses exists in the catalog version in force; the BR Field ID behind a code is the catalog owner's check and is not repeated here | RWB-E1-046 BR4; REQ-OCC-001; Principle 1 |
| BR5 | A refused answer is refused in whole: no row, no partial row, and the rows already written stay as they are | RWB-E1-046 BR5; refdata change process, step 3 |
| BR6 | A row is never updated or deleted, and an answer keeps the version it was decided under even after a later version or a withdrawal | RWB-E1-046 BR6; refdata change process, step 6; R-UNI-38 |
| BR7 | Templates are Legal counsel's reference data and the approver named on a version is that authority; this service records the authority but grants none | RWB-E1-046 BR7; DL28 |
| BR8 | `template` and `merge_field` are P6's in `rwb_comms`; rwb-decision holds no catalog table, copies no catalog row and reaches the catalog only through RWB-P6-E1046-CON (DP-01, DP-11) | Ownership Map; Architecture v5 slides 17 and 41; DP-01 |
| BR9 | The notice type and the product group are validated against LOV-NOTICE and LOV-PRODUCT read from the rwb-case reference-data contract at the version in force; no list value is written in code (DP-07) | TSD P7 T3.2; DP-07 |
| BR10 | No business value in code: template codes, merge codes, languages, notice types, product groups, catalog versions and dates are data of the catalog or the lists | Template and Rules §R7.2 s17; RWB-E1-046 section 17 |
| BR11 | Every catalog and list read is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream; a failed read refuses the answer and never accepts a partial version | DP-11; ADR-020 |
| BR12 | The row carries codes, versions, identifiers and dates only: no merge value, no template body and no personal data; a merge field marked personal_data is resolved at generation time by its owner | RWB-E1-046 section 17; section 17 of this story |
| BR13 | The row and the answer are one unit of work: a row that cannot be written refuses the answer, so no answer is recorded without the version that explains it | R-UNI-39; DP-03 principle applied locally to this row |

### 9. State transitions

None for a case status: this story moves no case, no notice and no template version. It sets the state of its own row only. It adds no value to LOV-NOTICE or LOV-PRODUCT; COURT_FILING is named in AC8 only as a value those lists do not hold.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | An answer is recorded | The catalog answers an Approved version, every merge code is in the catalog version in force and the lists hold the values | Stored, with the version, the catalog version and the valid-from date |
| (none) | An answer is recorded | The version is unapproved, withdrawn or unknown, a merge code is unknown, or a read fails | Refused; no row; the refusal names the check and the message ID |
| Stored | A later version takes effect on its valid-from date | A new answer is recorded after that date | A new row for the new answer; the earlier row is unchanged |
| Stored | A version is withdrawn at the owner | Nothing | The earlier row is unchanged; a later answer is refused under BR3 |
| Stored | An update or a delete is attempted | Never | Refused; the row stays as written |
| (none) | An answer is recorded | The notice type or product group is not in LOV-NOTICE or LOV-PRODUCT | Refused with a message code Not specified in the source documents (DOR-RWB-P7-E1046-APP-5) naming the list and the value; no row is written |

The catalog states this story reads are the owner's: Draft, Approved and Withdrawn, with Draft never usable and Withdrawn never current (RWB-P6-E1046-CON). The state word of a `template_use` row is this story's own and is stored on the standard `state` column; the column names of the row are Not specified in the source documents (GAP-2453; ASM-4065).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-decision service identity (the rwb-decision login, DP-02) | Reads the catalog and the lists; writes `template_use` in `rwb_decision` |
| The caller of an answer (the approval path of the service, the notice decision path) | Supplies the template code, language, version, notice type and merge codes; receives the refusal and its message ID |
| RW-AUDIT, internal audit lead | Reads the values of an entry through the decision-log read of RWB-P7-E2005-APP (Decision log R) |
| RW-LITOFF, litigation officer | Reads the values of the entries on their cases (Decision log R) |
| RW-LEGAL, Legal counsel | Owns the approval of a version at rwb-comms (Documents A); grants nothing here and approves nothing here |
| RW-REFADM, reference data administrator | Loads the catalog and the template versions at rwb-comms (Reference data C); has no path into this story |
| RW-COE, center of excellence analyst | Reads the catalog and the rows (Decision log R, Reference data R) |
| No delegation of authority level applies | A version and a catalog version are not a credit decision; the authority on the record is the approver named by the catalog |

No personal name, no e-mail address and no credential appears in this story, its examples or its fixtures. Where an actor must be named, the story uses a role code or a staff identifier only.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (DOR-RWB-P7-E1046-APP-7) | template_use (P7, `rwb_decision`) | id, entry_ref, template_code, language, template_version, catalog_version, merge_codes, notice_type, product_group, approver_ref, valid_from, business_date, state | Write; the row name and the column names are Not specified in the source documents (GAP-2453; ASM-4065) |
| DF-REF-045 to DF-REF-051, DF-REF-063 to DF-REF-069 | template (P6 `rwb_comms`) | the version, its state, the approver, the approval date, the valid from, the channel, the notice type, the signature basis and the merge codes | Read through the catalog contract only |
| DF-REF-252 to DF-REF-260 | merge_field (P6 `rwb_comms`) | the merge code, its BR Field ID, the catalog version and the valid from | Read through the catalog contract only; the BR Field ID check stays the owner's |
| DF-REF-028, DF-REF-029 | lov_value (P3 `rwb_case`) | lov_code, value_code | Read through the reference-data contract (DP-07) |
| DF-DEC-001, DF-DEC-003, DF-DEC-008 | decision_log_entry (P7) | id, decision_code, inputs_ref | Read as the entry reference the row explains; the entry is written by RWB-P7-E1027-APP |
| Standard column | template_use | state, created_at, created_by | Write |
| Not specified in the source documents (DOR-RWB-P7-E1046-APP-7) | outbox_event, processed_event, idempotency_key (PLT library in `rwb_decision`) | — | Created with the schema; not written by this story |

Keys and rules in `rwb_decision`:

- `template_use`: primary key `id`; unique `uk_template_use_entry (entry_ref, template_code, language)` so one entry names one version of one template; index `(template_code, language, business_date)` for the audit read; check that `template_code`, `language`, `template_version`, `catalog_version` and `business_date` are present.
- The migration is one per-service Flyway step in the `rwb_decision` sequence (DP-15, RWB-PLT-E1044-CON): `V_E1046__template_use.sql` creates `template_use` and alters no existing table. Its name and its position in the sequence are Not specified in the source documents (GAP-2453; ASM-4065).
- No row is seeded by the migration: the catalog and the lists are the owners' data, reached through their contracts, and the fixtures of section 12.8 live in the test environment only.
- The row holds no foreign key into another schema and no copy of a catalog row; `template_code` and `language` are values, not references (DP-01).

### 12. Contract

#### 12.1 REST operations provided

None. The base of this service is `/api/recovery/decision/v1` (DP-13), and this story adds no operation to it: the row is written inside the answer the caller already asked for, and the values are read back through the decision-log read of RWB-P7-E2005-APP, which is named here and not declared as provided. A template-catalog read on this base would be a second catalogue and is refused by BR8.

#### 12.2 REST operations consumed

Every row is one hop on the owner's base with a 2 s timeout, a breaker per downstream and a single GET retry with jitter (DP-11, ADR-020).

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | The current version of a template code and language on the business date, with its state, approver, approval date, valid from, notice type, channel and signature basis. The query parameter names and the answer field names are Not specified in the source documents (GAP-2453; ASM-4067); contract RWB-P6-E1046-CON (C) |
| GET | `/api/recovery/comms/v1/admin/templates/{templateId}/content` | P6 rwb-comms | Named and not called: the body is the owner's claim-check file and this story stores the reference, never the body. The merge-field set of a version is reached through the catalog contract and its path is Not specified in the source documents (GAP-2453; ASM-4068) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE and LOV-PRODUCT in force on the business date (DP-07, RWB-P3-E1043-CON) |

The catalog-version-in-force read of the same contract is the value matched in AC1 and AC6; its path and its field names are Not specified in the source documents (GAP-2453; ASM-4069). A failed read of any row refuses the answer with MSG-GEN-006 naming the system that did not answer; no answer is ever accepted on a partial answer (BR11).

#### 12.3 Events published

None. A recorded row is not an event of this story: the `DecisionRecorded` event of the entry is published by RWB-P7-E1027-APP on the shared topic `rwb.decision-record.v1` (DP-03), and the service's own topic `rwb.decision.events.v1` carries `ApprovalRequested`, `ApprovalDecided` (RWB-P7-E2013-APP) and `RulePackageInForce` (RWB-P7-E1073-CON), never a template reference. If the template values must travel, they travel inside the record of the entry, not as a new event type.

#### 12.4 Events consumed

None. The values are read on demand at the moment of the answer, so a catalog change reaches this service on the next answer and needs no subscription; a cached copy would be the second catalogue BR8 forbids.

#### 12.5 Workflows and activities

None. The recording is synchronous inside the caller's step, in the caller's thread and transaction: this story registers no workflow, adds no activity and holds nothing on task queue `rwb-decision` in namespace `rwb-recovery`. `ApprovalWorkflow` belongs to RWB-P7-E2013-APP and the record activity `RecordAndApply` to RWB-P7-E1027-APP.

#### 12.6 Schedules

None. No Schedule, no cron entry and no job name is registered; the nightly chain check JOB-14 at 02:00 is RWB-P7-E1008-APP's Schedule, the promote run JOB-20 at 00:01 is rwb-decision's rule Schedule, and this story reads no scheduler row.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template_use | P7 (`rwb_decision`) | One row per accepted answer: the entry reference, the template code, the language, the version, the catalog version in force, the merge codes, the notice type, the product group, the approver reference, the valid from, the business date and the state. Appended, never updated. Row and column names Not specified in the source documents (GAP-2453; ASM-4065) |
| decision_log_entry | P7 (`rwb_decision`) | Contracted use only: the entry id that `entry_ref` names; the entry is written by RWB-P7-E1027-APP and this story writes no entry |
| approval | P7 (`rwb_decision`) | Contracted use only: `source_ref` may name the template version of an approval; the approval row is RWB-P7-E2013-APP's and this story writes none |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Created with the schema; this story writes no row of any of them |

`template` and `merge_field` are P6 rwb-comms's in `rwb_comms`; `lov_value` is P3 rwb-case's; `sys_fields` and the data dictionary are P1 rwb-source-data's; `document` is P5 rwb-document's. None of them is declared as owned here, read directly or copied (DP-01, BR8).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers |
|---|---|---|
| rwb-comms catalog WireMock | RWB-P6-E1046-CON (DP-11) | Catalog version "MF-2026.11" in force on 2026-11-20 with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"; "DEMAND-MTG" "TH" version 1 Approved by "LEG-0001" on 2026-10-01 and version 2 approved 2026-11-10 with valid from 2026-11-10; version 3 with valid from 2026-12-01; "RECALL-HP" "TH" with one Draft version; a withdrawn version 2; "GUARANTOR-SSME" without "GUARANTOR_EMAIL"; catalog version "MF-2026.12" in force from 2026-12-15; an unknown template code; 503; and a delayed answer beyond 2 s |
| rwb-case reference-data WireMock | RWB-P3-E1043-CON (DP-07) | LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE"; LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"; no value for "COURT_FILING"; and a delayed answer beyond 2 s |
| Catalog refusal set | RWB-P6-E1046-CON | The refusal of an unapproved version, the refusal of a withdrawn version, the refusal of an unknown merge code and the refusal of a repeated answer, each inside the owner's error envelope with its message ID |
| Entry fixture | RWB-P7-E1027-APP | An entry "DL-2026-0009981" on case "RC-2026-000123" with decision code "D7.1", used only as the reference a row explains |

The fakes carry synthetic values and the legacy identifiers only: no production data, no template body and no merge value.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | The current-version read and the merge-field read on rwb-comms, the lists read on rwb-case; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | None | No event is published or consumed by this story; `DecisionRecorded` belongs to RWB-P7-E1027-APP |
| Temporal | None | None | No workflow, no activity and no Schedule |
| File | None | None | The template body stays the owner's claim-check file and is never read here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `templateuse`, Java package `th.co.scb.ace.workbench.recovery.decision.templateuse`; the artefact is the `rwb-decision` api deployment of the service template.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Six patterns are applied and every one is a row above. Two readings matter and are stated rather than silently resolved. First, the DP rows add `H RWB-PLT-E1043-CON`, `H RWB-PLT-E1044-CON` and `H RWB-PLT-N001-CON` while the plan's build list is empty; the three are read as wave-0 platform prerequisites of the service template, so the lane L-P7-M and the Day-1 start do not change (GAP-2453; ASM-4066). Second, DP-11 carries the legacy in-process catalog call across the service boundary and the only dependency it adds is the plan's C row RWB-P6-E1046-CON, which is built against and faked. DP-05 is not claimed because this story reads no ACE view and no data dictionary; DP-03, DP-08 and DP-16 are not claimed because this story writes no decision entry, declares no authorise call and reaches no integration adapter.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateUseRecorder | Service | The one entry point: takes the answer facts, calls the catalog and the lists, applies BR1 to BR5 and BR9, and writes the row in the caller's unit of work |
| CatalogClient | Client | The current-version read, the merge-field read and the catalog-version read on RWB-P6-E1046-CON, with the 2 s budget, the GET retry and the breaker |
| MergeCodeChecker | Service | Compares the merge codes of the answer with the set of the version and the catalog version in force |
| CatalogRefusalMapper | Service | Maps each refusal of the owner and each local check to its message ID of section 14, never to an accepted row |
| TemplateUseEntity, TemplateUseRepository | Entity, Repository | Map and write `template_use`; the append-only guard; the audit read by template and business date |
| ReferenceListReader | Service | Reads LOV-NOTICE and LOV-PRODUCT through the reference-data client (DP-07) |

**Database and migration.** `template_use` in `rwb_decision` with the keys and checks of section 11, created by `V_E1046__template_use.sql` in the per-service sequence (DP-15). The table is written by insert only; a trigger or a missing grant refuses UPDATE and DELETE, following the append-only pattern of the ledger.

**Configuration and reference data.**

- The catalog base URL, the list base URL and the timeouts are configuration, never a value in code.
- The feature switch is `rwb.decision.template-use`; off means the recording is refused with MSG-GEN-006 and no answer is recorded without its version, never a silent accept.
- The login is the rwb-decision login (DP-02); its name is Not specified in the source documents (GAP-2453; ASM-4070).

**Build steps**

1. The migration, the entity and the repository with the unique key and the append-only refusal; test them on Testcontainers.
2. `CatalogClient` on the catalog fake with the 2 s budget and the retry, and the refusal mapping of MSG-P6-005, MSG-P6-003 and MSG-P6-006; test AC2, AC3 and AC5.
3. `MergeCodeChecker` against the merge-field read and the catalog version in force; test AC4.
4. `ReferenceListReader` and the MSG-GEN-001 refusal for an unknown notice type; test AC8.
5. `TemplateUseRecorder` with the business-date rule and the one-unit-of-work rule; test AC1 and AC6.
6. The append-only and no-catalog-table assertions of AC7, including a schema scan and a dependency scan.
7. A contract-fake run in isolation, so the story builds before rwb-comms and rwb-case are live.

**Done when.** The nine test cases of section 16 pass, the migration runs clean on an empty schema and on the SIT schema, the contract tests of RWB-P6-E1046-CON and RWB-P3-E1043-CON stay green, and no merge value, template body or personal value appears in a log or an evidence line.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The catalog answers no Approved version for the template code and language | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | An answer uses a merge code not in the catalog version in force | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-003 | The only version in force is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-GEN-001 | A required value is missing on the answer, or the notice type or product group is not in the list in force | Enter {field}. |
| MSG-GEN-006 | A catalog or list read does not answer inside the 2 s budget, or the feature switch is off | {system} is not available. Try again in a few minutes. |

The texts of MSG-P6-005, MSG-P6-006 and MSG-P6-003 are copied character for character from RWB-E1-046 section 14 and keep their legacy meanings; MSG-GEN-001 and MSG-GEN-006 are the platform messages of the same legacy section. The word "load" in MSG-P6-006 is the legacy wording and is kept unchanged even though this story refuses an answer and loads nothing. Thai text for each message follows decision DL10; no new message ID is introduced by this story.

### 15. Screens and states

No screen is built here. The values of a row are read back on the decision-log view that RWB-P7-E2005-APP serves and that the gateway-bff composite route projects (DP-19): a reader with the Decision log right asks for an entry and sees the template code, the version, the catalog version, the notice type, the product group and the valid-from date of the answer. The screen field list and the route specification belong to RWB-PLT-N001-CON, and the read itself to RWB-P7-E2005-APP.

SCR-33 Template catalog admin and SCR-40 Reference data are the legacy screens of the catalogue and stay P6's (RWB-P6-E1046-APP, RWB-P6-E1034); their states — Loading, Read only, Draft, Approved and Withdrawn — describe the catalog, not this row. The empty, loading, error and no access states of SCR-33 are Not specified in the source documents (CG-ALL-6984); those of SCR-40 are Not specified in the source documents (CG-ALL-6985). The row's own states are the three of section 9, and a refused answer leaves no state behind because no row is written.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-046-01 | AC1, AC6, BR1, BR2, BR6 | Component | Catalog MF-2026.11; DEMAND-MTG TH version 1 Approved; a row naming version 2 |
| TC-E1-046-02 | AC2, BR1 | Component | RECALL-HP TH with one Draft version; an unknown template code |
| TC-E1-046-03 | AC3, BR4 | Component | GUARANTOR-SSME answer using GUARANTOR_EMAIL |
| TC-E1-046-04 | AC4, BR8 | Component | The migration on an empty rwb_decision schema, and the dependency scan |
| TC-E1-046-05 | AC5, BR5 | Component | An answer with no template code, and one with no language |
| TC-E1-046-06 | AC6, BR6 | Component | The same answer recorded twice against one entry |
| TC-E1-046-07 | AC7, BR3 | Component | DEMAND-MTG TH version 2 withdrawn |
| TC-E1-046-08 | AC8, BR2 | Component | DEMAND-MTG TH version 3 valid from 2026-12-01; catalog MF-2026.12 from 2026-12-15 |
| TC-E1-046-09 | AC8, BR9 | Contract | An entry read outside the reader's scope, and an answer whose notice type is not in LOV-NOTICE |
| TC-E1-046-10 | AC5 | Component | A catalog read answering 503, a second catalog call beyond the 2 s budget, and a reference-data read beyond 2 s |
| TC-E1-046-11 | AC7, BR8 | Component | Each table of section 12.7 on the empty rwb_decision schema, and a check that no table outside section 12.7 is created |

The nine legacy test case IDs of RWB-E1-046 are kept, in the legacy order, and re-pointed at this slice: each is answered here at component or contract level against the catalog fake and the record path, and the business outcome of each is proved by RWB-P6-E1046-APP. TC-E1-046-09 keeps its legacy access intent: the read of the values is refused at the edge with MSG-P4-002, which is asserted here at the contract level and delivered by RWB-P7-E2005-APP. Legacy levels map System to Component and Access to Contract. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: template codes, merge codes, languages, notice types, product groups, catalog versions and dates come from the catalog contract, the list contract or the caller; no such value appears in Java, a resource file or a migration.
- No personal data in rows, events, workflow inputs, logs, tests or prompts. The row holds codes, versions, identifiers and dates; a merge value is resolved at generation time by the owner and never stored here.
- No template body and no merge value in a row, a payload, a log or an evidence line; the body stays the owner's claim-check file behind `body_ref`.
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE table and no ACE view, and reads no `sys_fields` and no data dictionary.
- No cross-schema read and no copy: `rwb_decision` holds no foreign key into another schema and no catalog row; `template` and `merge_field` stay P6's (DP-01, BR8).
- One REST base and one topic per service; this story declares neither a new operation nor a new event (DP-13).
- The row is append only: an update and a delete are refused, and an answer keeps the version it was decided under (BR6, R-UNI-38).
- One hop, a 2 s timeout and a breaker per downstream; a failed read refuses the answer and never accepts a partial version (BR11).
- Every fixture is synthetic and uses the legacy identifiers only; no production payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Element of this story | Test cases |
|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The merge-code check against the catalog version in force, MSG-P6-006, and the merge codes recorded on the row | TC-E1-046-03, TC-E1-046-08, TC-E1-046-10 |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The version, the approver and the valid-from date recorded on the row, the Approved-only rule, MSG-P6-005 and MSG-P6-003 | TC-E1-046-01, TC-E1-046-02, TC-E1-046-05, TC-E1-046-06, TC-E1-046-07, TC-E1-046-09, TC-E1-046-11 |

| Decision or pattern | Feature | L3 process | Where it sits in this story |
|---|---|---|---|
| DP-01 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | `template_use` in `rwb_decision`; the catalog stays P6's and is read through the contract |
| DP-07 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The LOV-NOTICE and LOV-PRODUCT read of section 12.2 and its fake |
| DP-11 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The three consumed reads with one hop, a 2 s timeout and a fake |
| DP-13 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The service base `/api/recovery/decision/v1` and no new operation |
| DP-15 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The `rwb_decision` Flyway sequence and the template_use migration at the next free V number of that sequence, Not specified in the source documents (CG-ALL-6983) |
| DP-19 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The decision-log view of the entry through gateway-bff |
| ADR-013 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | The `rwb_decision` schema and the rwb-decision login |
| ADR-020 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Not specified in the source documents (DOR-RWB-P7-E1046-APP-2) | Per-service Flyway and migration ownership |

Open decisions: DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL28 (ASM-1861, ASM-1925, ASM-2093, ASM-2727). Each decision is still open; its assumptions are not confirmed in the source documents.

The legacy key is RWB-E1-046. This story owns no legacy acceptance criterion: its AC1 to AC8 are new and test the record side only, RWB-P6-E1046-APP owns the legacy AC1 to AC8 and the nine legacy test cases at their business level, RWB-P6-E1046-CON owns the catalogue contract and RWB-ITG-E1046-ITG proves the same values across rwb-comms, rwb-decision, rwb-case and rwb-source-data.

### 19. Out of scope

- The catalog as data, its load, its version numbering, its Legal approval, its withdrawal and the current-version selection: RWB-P6-E1046-CON and RWB-P6-E1046-APP.
- The template screen and the reference-data load screen (legacy RWB-E1-034), and the merge-field BR Field ID check against the P1 data dictionary.
- The decision entry itself and its chain: RWB-P7-E1027-APP and RWB-P7-E1008-APP; the decision-log read: RWB-P7-E2005-APP.
- The notice approval screen and the delegation-of-authority routing: RWB-P7-E2014, RWB-P7-E2013 and their contracts.
- Generating a notice from a version, dispatching it and capturing proof of delivery: RWB-P6-E1052, RWB-P6-E2021 and RWB-P6-E1055.
- The cross-service proof of these values: RWB-ITG-E1046-ITG.
- The Compliance approval path for a template (FEAT-ADM-05, Epic 8) and contract, credit approval and mortgage document generation (RWB-E2-026).
- The `rwb_decision` schema baseline, the topic and queue provisioning, the dashboards and the runbook of the service.
