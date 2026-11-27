# RWB-PLT-TE011-APP PDPA lint for code, tests and logs
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP19 |
| Parallel lane | L-PLT-TPL-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-011 for the 19-repository target. The legacy lint is kept as a build step and re-pointed: the PDPA step is generated once in the golden pipeline and the service template, so every repository generated from the template runs the same rule set at the same version; the personal field marks are read from one pinned dictionary version served by the reference-data contract of rwb-case instead of from a per-repository `sys_fields` seed file, and the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views; the approver of an allow-list change is the code-owner role resolved through the authorise contract of rwb-access, with the repository host merge rule unchanged; and a dictionary read that does not answer fails the build closed. Every legacy value is kept unchanged: rule ids PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID; the fixture values "recovery.casewf.internal.SampleService", "customer.getFirstName()", "CustomerEntity", "idNoMasked", "TESTNAME", "SYN-LAST-0001", "v_ace_account.contract_no", "ace-service/src/test/resources/recovery/legacy-seed.sql", 30 November 2026, 1 December 2026, "src/modules/recovery/caserecord", "console.log(customer.lastName)", "No case for ", "ContactEntity"; the field names first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value; the roles RW-TRIBE and RW-COMPLY; and the TechX tech leads as code owners. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-TE011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)** and a **member of the platform team that owns the service template (TechX)**, I want **the PDPA lint delivered as one generated step of the golden pipeline and of the service template, so that every one of the 19 repositories generated from the template runs the same rule set at the same version, the personal field marks are read from one pinned dictionary version served by the reference-data contract of rwb-case, the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views, and an allow-list change is approved by the role that the role-to-permission matrix of rwb-access names**, so that **personal data never reaches code, test fixtures, log statements, exception messages, build artifacts or prompts to coding agents, and any finding in any repository is explained by the one dictionary version that its build record names**.

The rework keeps the lint and changes the object it reads. In the monolith the lint reads a `sys_fields` seed file and the API specification inside one repository, generates `pdpa-rules.yaml` there, and runs once in one pipeline. The target has 19 repositories generated from one service template, each with its own `rwb_<name>` schema and its own login, and no repository may read another service's tables (Arch v5 slide 29). A rule generator copied into 19 repositories is 19 rule sets that drift; a dictionary read per repository is 19 answers to one question. The legacy lint was never built (the legacy story is Ready for build, this story is Not started), so no built code is discarded, the six rule ids and every fixture value are carried unchanged, and the change is the source of the marks, the place the step is generated, the approver of an allow-list change and the read of the release quality view.

### 2. Business rationale

Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal field marks and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero in every repository, not only in one.

The split makes the lint a property of the estate rather than of one build. Arch v5 slide 11 makes the contract the first artefact of every service and runs contract tests in every build; slide 20 gives every service the same block from the service template and the shared libraries; slide 29 fixes one schema and one login per service with no cross-schema read and a boundary test in every build; slide 35 places personal data in the owning service, masked and encrypted, never in events or workflow payloads, with the masking rules of P4 enforced in each service, and holds the pipeline to NIST SP 800-204C and 800-204D; slide 47 records the risk "Schema rules broken over time", its impact "Hidden coupling between services", and the mitigation "Database grants per schema; boundary test in every build; review of every new grant", owned by Architecture. A lint generated once from one pinned dictionary version is how 19 builds give one answer; a lint generated per repository is how the estate re-learns the same personal field 19 times, differently.

Three moves follow. The marks become reference data: the dictionary is served by the reference-data contract of rwb-case (DP-07), `sys_fields` is owned by P1 rwb-source-data in `rwb_source_data`, and the ACE field definitions are reached only through the owner's contract or the `v_ace_*` views (DP-05, slide 29). The allow-list approval becomes an authorisation decision: the approver role comes from the role-to-permission matrix as data behind the authorise contract of rwb-access (DP-08), and the repository host still enforces the merge rule. And the release quality view a role reads — findings per repository, per gate and per dictionary version — arrives through a gateway-bff composite route (DP-19); this story provides no screen and invents no route. The folder rules and the boundary test the step plugs into stay with RWB-PLT-TE001-APP, which is tracked and does not block this build.

### 3. Preconditions

- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its client library (DP-07). The dictionary version and the personal field marks are read through it and are never a value in the lint.
- **RWB-PLT-E1037-CON** is published: the authorise contract of rwb-access and the guard library (DP-08). The approver role of an allow-list change is resolved through it.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The release quality view a role reads is behind that route; this story publishes no route of its own.
- The **two service CON dependencies** are published: **RWB-P3-E1043-CON**, the rwb-case contract behind the reference data (DP-07), and **RWB-P4-E1037-CON**, the rwb-access contract behind the authorise call (DP-08). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- The service template and the golden pipeline exist, and the 19 repositories are generated from that template (Arch v5 slides 11 and 20). RWB-PLT-TE001-APP supplies the folder rules and the boundary test this step plugs into; it is tracked, not blocking.
- The dictionary marks each personal field: `is_personal` in `sys_fields` in `rwb_source_data` (P1 rwb-source-data, Ownership Map) and `x-personal-data: true` in the API specification of the owning service.
- Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065, kept).
- The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface, kept).
- The pinned dictionary version, the operation that serves it and the rule-set version convention are Not specified in the source documents (GAP-1436; ASM-2525), and the release quality view is Not specified in the source documents (GAP-1436; ASM-2527); both are applied as the working defaults of section 13.

### 4. Flow

1. Service template: the golden pipeline generates the PDPA step, the rule generator and the allow-list check from one definition, so a repository created from the template receives the same step and the same rule-set version as the other 18, and no repository holds a step of its own.
2. Build start: DictionaryVersionGuard reads the pinned dictionary version through the reference-data contract of rwb-case; when the contract does not answer, the step stops here and fails the build closed.
3. PersonalFieldReader: reads the marks of that version — the `is_personal` flag and `x-personal-data` — and never a value of any field.
4. RuleGenerator: generates `pdpa-rules.yaml` from the field list, with the Java getter names, entity class names, JSON property names and TypeScript property names of each marked field.
5. Lint: scans `src/main` and the front-end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
6. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
7. Lint: checks that each entity with a personal field excludes it from its text form.
8. Lint: compares each finding with `pdpa-allow.yaml`; an entry past its expiry does not excuse the finding, and an entry without an owner, a reason or an expiry is refused at load.
9. RuleSetVersionRecorder: writes the dictionary version and the rule-set version into the build record of the repository, so a rerun of the same commit against the same version gives the same findings.
10. Pipeline: fails the build on any finding and prints the rule, the file, the line and the field, without printing the value found.
11. Allow-list change: the pull request is approved by the code-owner role of the repository, resolved through the authorise contract of rwb-access; the repository host refuses the merge without that approval.
12. Release quality view: a role reads findings per repository, per gate and per dictionary version through the gateway-bff composite route of RWB-PLT-N001-CON; this story adds no screen and no route.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A log statement writes a personal field | Build fails | Build log: PDPA-LOG-FIELD | AC1 |
| X2 | A log statement writes a whole personal entity | Build fails | Build log: PDPA-LOG-ENTITY | AC2 |
| X3 | A fixture holds a valid Thai national identifier | Build fails | Build log: PDPA-FIXTURE-ID | AC3 |
| X4 | A fixture holds a value in a personal field without the synthetic prefix | Build fails | Build log: PDPA-FIXTURE-FIELD | AC4 |
| X5 | A field is newly marked personal in the pinned dictionary version | The rule set is regenerated from that version and existing uses of the field are found | Build log: PDPA-LOG-FIELD | AC5 |
| X6 | An allow list entry is past its expiry | The finding fails the build | Build log: allow entry expired | AC6 |
| X7 | A front end console or logger call writes a personal property | Build fails | Build log: PDPA-LOG-FIELD | AC7 |
| X8 | A log statement writes a field through the masking helper | Passes | None | AC8 |
| X9 | An exception message carries a personal field | Build fails | Build log: PDPA-EXCEPTION | AC9 |
| X10 | An entity's text form includes a personal field | Build fails | Build log: PDPA-TOSTRING | AC10 |
| X11 | A person outside the code owners approves an allow list change | Merge refused; the code-owner role of the repository is the only approver the authorise contract returns | Repository host: review required from code owners | Access test TC-TE-011-11 |
| X12 | The reference-data contract does not answer at pipeline time | No rule set is generated and the build fails closed instead of passing with an empty rule set; the failure names the dictionary read, not a finding | Build log: dictionary version not read | AC11 |
| X13 | A repository resolves a rule-set version other than the pinned one | The build fails and names the repository and both versions; a stale rule set never excuses a finding | Build log: rule-set version mismatch | AC11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three platform contracts, the two service contracts of the run and the template; the marks arrive through a contract, so no service has to be built first; no screen and no route of its own |
| Negotiable | The synthetic prefix, the example domains, the allow list and the rule-set version convention are configuration; the rule ids, the field marks and the fail-closed behaviour are fixed by NFR-054, DL26 and Arch v5 slides 11, 20, 29 and 35 |
| Valuable | Personal data stays out of logs, artifacts and prompts in all 19 repositories, and one dictionary version explains every finding |
| Estimable | One generated pipeline step, one rule generator, one rule set, one allow list, one version recorder and one dictionary guard |
| Small | Fits in one sprint with its tests, in the template and one generated repository |
| Testable | Each legacy criterion is one fixture file with one finding; the new criterion runs the generated step in the template and in a second generated repository and compares their rule-set versions |

### 7. Acceptance criteria

```gherkin
Feature: PDPA lint for code, tests and logs

  Background:
    Given the data dictionary marks first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value as personal

  Scenario: AC1 Log statement (legacy RWB-TE-011 AC1)
    Given a log statement in "recovery.casewf.internal.SampleService" that writes customer.getFirstName()
    When the pipeline runs
    Then the PDPA lint fails the build
    Then the build log names rule PDPA-LOG-FIELD, the file, the line and field first_name, and does not print a value

  Scenario: AC2 A whole entity in a log (legacy RWB-TE-011 AC2)
    Given a log statement that writes the object "customer" of type CustomerEntity
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-ENTITY

  Scenario: AC3 A national identifier in a fixture (legacy RWB-TE-011 AC3)
    Given a JSON fixture whose "idNoMasked" holds a 13-digit number with a valid check digit, generated by the test at run time
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-ID

  Scenario: AC4 A personal field without the synthetic prefix (legacy RWB-TE-011 AC4)
    Given a SQL seed that sets last_name to "TESTNAME"
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-FIELD
    Then the same seed with last_name "SYN-LAST-0001" passes

  Scenario: AC5 A field newly marked personal (legacy RWB-TE-011 AC5)
    Given the rwb-case reference-data contract mock returns the dictionary version that marks v_ace_account.contract_no as personal
    Given the dictionary marks v_ace_account.contract_no as personal in a new version
    Given a log statement writes account.getContractNo()
    When the pipeline runs
    Then the system regenerates the rule set with contract_no
    Then the build fails with rule PDPA-LOG-FIELD for contract_no

  Scenario: AC6 An expired allow list entry (legacy RWB-TE-011 AC6)
    Given the allow list excuses PDPA-FIXTURE-FIELD in "ace-service/src/test/resources/recovery/legacy-seed.sql" until 30 November 2026
    When the pipeline runs on 1 December 2026
    Then the build fails with "allow entry expired"

  Scenario: AC7 The front end (legacy RWB-TE-011 AC7)
    Given a component in "src/modules/recovery/caserecord" that calls console.log(customer.lastName)
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-FIELD for lastName

  Scenario: AC8 A masked value passes (legacy RWB-TE-011 AC8)
    Given a log statement that writes the contact point through the masking helper
    When the pipeline runs
    Then the lint passes for that line

  Scenario: AC9 An exception message (legacy RWB-TE-011 AC9)
    Given code that throws an exception with message "No case for " + customer.getCifNo()
    When the pipeline runs
    Then the build fails with rule PDPA-EXCEPTION for cif_no

  Scenario: AC10 The text form of an entity (legacy RWB-TE-011 AC10)
    Given ContactEntity includes contact_value in its text form
    When the pipeline runs
    Then the build fails with rule PDPA-TOSTRING for contact_value

  Scenario: AC11 One pinned dictionary version and every one of the 19 repositories (new, D-RCV-60)
    Given the service template publishes the PDPA step and its rule set as part of the golden pipeline
    Given the 19 repositories are generated from that template
    When every one of the 19 builds runs the step
    Then every repository runs the same rule-set version, generated from one pinned reference-data version read through the rwb-case reference-data contract
    Then the lint records that dictionary version and the rule-set version in the build record of each repository
    When the dictionary version cannot be read at pipeline time
    Then the build fails closed and no repository passes with an empty rule set
    When a repository is inspected for a read of another service's schema, or of a sys_fields table it does not own
    Then no such read exists, because the marks arrive through the contract and no repository opens rwb_source_data
```

**Note on the criteria.** AC1 to AC10 are the legacy criteria of RWB-TE-011, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed. AC5 gains one `Given` line, the reference-data contract mock, because the dictionary is no longer a seed file in the repository: the marks are reference data behind the rwb-case contract, and the AC5 version that marks `v_ace_account.contract_no` as personal is answered by that mock; every legacy `Given`, `When` and `Then` of AC5 is kept as written. AC11 is the only new criterion and it names no business value: it tests that the step is generated by the service template, that all 19 repositories run the same rule-set version from one pinned dictionary version, that the version is recorded in the build record, that an unreadable dictionary fails the build closed, and that no repository reads another service's schema.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The personal field list is read from one pinned version of the data dictionary, served by the reference-data contract of rwb-case; it is never written in the lint and never copied into a repository | Logical Data Model, Personal data column; API x-personal-data; DP-07 |
| BR2 | No log statement, string built for a log, or exception message carries a personal field or a whole personal entity | NFR-054; CTL-11 |
| BR3 | Test fixtures, seeds and end-to-end data carry only synthetic values with the prefix "SYN-" in personal fields | NFR-045; RWB-E1-065 |
| BR4 | Literals matching a Thai national identifier with a valid check digit, a Thai mobile number or an email outside the example domains fail anywhere in code or tests | NFR-054 |
| BR5 | An entity with a personal field leaves it out of its text form | CTL-11 |
| BR6 | A finding is excused only by an allow list entry with an owner, a reason and an expiry date not yet passed; the change that adds or renews the entry is approved by the code-owner role of the repository, resolved through the authorise contract of rwb-access | Principle 1 applied to build configuration; DP-08 |
| BR7 | The lint never prints the value it found | REQ-ACA-005 |
| BR8 | One rule set at one version is generated from one pinned dictionary version and is inherited by every repository generated from the service template; no repository adds, edits or suppresses a rule, and the build record of each repository names the dictionary version and the rule-set version it ran | Arch v5 slides 11, 20 and 29; this story (ASM-2525) |
| BR9 | The step fails closed: a dictionary version that cannot be read, a rule set that cannot be generated or a scan that errors fails the build and never passes it with an empty rule set | Arch v5 slide 35; this story (ASM-2525) |

### 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a finding is not excused.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The step starts | The pinned dictionary version is read through the reference-data contract | Rules generated |
| Not started | The dictionary read does not answer | None | Failed closed |
| Rules generated | The scan starts | The rule set is written at the pinned rule-set version | Scanning |
| Rules generated | The rule set is empty | None | Failed closed |
| Scanning | No finding, or every finding excused by a live allow entry | None | Passed |
| Scanning | A finding is not excused | None | Failed |
| Scanning | The scan errors | None | Failed closed |
| Failed | A fix is built | The fix removes the finding, or adds an allow entry approved by the code-owner role | Rules generated |
| Failed closed | A fix is built | The dictionary version is readable and the rule set is generated | Rules generated |
| Passed | The same commit is rebuilt against the same dictionary version | None | Passed (same findings) |

The states are states of the pipeline step and of the build result, not of a case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the lint in their repository; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes; the approver role is the code-owner role of the repository, resolved through the authorise contract of rwb-access |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |
| RW-PLATADM, platform administrator, and a role that reads the release quality view | Read findings per repository, per gate and per dictionary version through the gateway-bff composite route of RWB-PLT-N001-CON; write no finding and change no rule set |
| No role | May merge a finding past its allow entry, read another repository's build record, or edit the rule set outside the dictionary |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-055 | v_ace_customer | cif_no | Read (definition) |
| DF-ACE-057 | v_ace_customer | first_name | Read (definition) |
| DF-ACE-058 | v_ace_customer | last_name | Read (definition) |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read (definition) |
| DF-ACE-059 | v_ace_customer | date_of_birth | Read (definition) |
| DF-EXT-002 | party_ext | vulnerable | Read (definition) |
| DF-ACE-061 | v_ace_customer | deceased_flag | Read (definition) |
| DF-EXT-004 | party_ext | bankruptcy | Read (definition) |
| DF-ACE-078 | v_ace_contact | contact_value | Read (definition) |
| DF-INT-011 | interaction | summary | Read (definition) |
| DF-DOC-015 | document_field | field_value | Read (definition) |

The lint reads which fields are personal; it never reads their values. Field IDs are those in the Logical Data Model and Data Dictionary.

The marks are now reference data. `sys_fields` lives in `rwb_source_data` and is owned by P1 rwb-source-data (Ownership Map); the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views (DP-05; Arch v5 slide 29), and no repository opens `rwb_source_data` or any other service's schema. `party_ext` now lives in `rwb_source_data` and `document_field` and `interaction` are owned by `rwb_document` (P5) and `rwb_source_data` (P1) respectively; the lint reads only their definitions from the dictionary and never a row of any of them, because the entity and field names it needs are metadata and not data (DP-01).

The pinned dictionary version, the operation that serves it and the rule-set version convention are Not specified in the source documents (GAP-1436; ASM-2525); the lint takes the working defaults of section 13 until the gap closes.

### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it. The step runs inside the pipeline of each repository it is generated into.

#### 12.1 REST operations provided

None. The lint is a build step and provides no REST operation: the platform row has no REST base, no topic, no task queue and no schema of its own, and no path is invented for it. A developer reads a finding in the pull request checks, and a role reads the release quality view through the gateway-bff composite route of RWB-PLT-N001-CON, which this story consumes and does not publish.

#### 12.2 REST operations consumed

None as a path of this story. The step calls the two contracts below at pipeline time and repeats no path, version or payload of either; the dictionary path is published by the contract story that owns it.

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The reference-data contract that serves the pinned dictionary version and the personal field marks the rule set is generated from (DP-07) |
| `RWB-P4-E1037-CON` | P4 rwb-access (the platform contract behind it is `RWB-PLT-E1037-CON`, epic RWB-PLT-LIB) | The authorise envelope and the approver role of an allow-list change, resolved from the role-to-permission matrix (DP-08) |

#### 12.3 Events published

None. A build step publishes no business event; a finding is a build log line and a build record row, and neither is a Kafka event.

#### 12.4 Events consumed

None. The step is synchronous: it is started by the pipeline, reads the dictionary through the contract and produces its result in the same run, and it waits on no topic.

#### 12.5 Workflows and activities

None. A build step is not a Temporal workflow or activity; it starts nothing on a service task queue and awaits no child workflow.

#### 12.6 Schedules

None. The step runs on every pull request and every build of main, not on a schedule, and it creates no Temporal Schedule.

#### 12.7 Tables owned

None. `pdpa-rules.yaml` and `pdpa-allow.yaml` are build artefacts of the repository, not tables; the marks are rows of `sys_fields` in `rwb_source_data`, owned by P1 rwb-source-data, and this story owns no table in any schema.

#### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind the reference-data contract | One pinned dictionary version that marks first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value as personal, and the AC5 version that also marks v_ace_account.contract_no; no value of any field, and no answer at all for the fail-closed case (AC11) |
| rwb-access authorise fake | `RWB-P4-E1037-CON` behind the authorise contract | The code-owner role of the repository granted the approval of an allow-list change, and a squad member outside the code owners refused with the documented refusal; the story has no Workbench endpoint, so no Workbench message ID is shown (TC-TE-011-11) |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 consumed | The rwb-case reference-data read of the pinned dictionary version and the marks, and the rwb-access authorise read of the approver role, one hop each at pipeline time; none provided |
| Kafka | None | No event is published or consumed by the step |
| Temporal | None | A build step is not a workflow or an activity |
| File | 3 | The generated rule set `pdpa-rules.yaml`, the allow list `pdpa-allow.yaml`, and the source, test and fixture folders the scan reads in the repository of the build |

### 13. Solution plan

**Package.** `tools/pdpa-lint` as the one definition consumed by every repository generated from the service template (the legacy package is kept). The step and its rule set are published by the template and the golden pipeline, and a repository holds no copy it may edit.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PersonalFieldReader | Service | Reads the personal field marks of the pinned dictionary version through the reference-data contract of rwb-case (BR1) |
| RuleGenerator | Service | Writes `pdpa-rules.yaml` with name variants: snake case, Java getter, camel case property (BR2 to BR5) |
| pdpa-rules.yaml | Rule table | The generated rules, at the rule-set version derived from the dictionary version (BR8) |
| pdpa-allow.yaml | Rule table | Allow list entries with owner, reason and expiry, refused at load when one is missing (BR6) |
| CheckDigitMatcher | Service | Thai national identifier check-digit test for BR4 |
| PdpaLintStep | Job | The pipeline step generated by the template: runs the scan and prints findings without values (BR7) |
| RuleSetVersionRecorder | Service | Writes the dictionary version and the rule-set version into the build record of the repository (BR8) |
| DictionaryVersionGuard | Service | Fails the build closed when the dictionary version cannot be read or the rule set cannot be generated (BR9) |

**Database.** None. The `sys_fields` seed is no longer read as a file: the marks arrive through the reference-data contract of rwb-case, and `sys_fields` in `rwb_source_data` is behind that contract, owned by P1 rwb-source-data (DP-01, DP-05, DP-07). The dictionary version and the operation that serves it are Not specified in the source documents (GAP-1436; ASM-2525).

**Configuration and reference data.**

- `rwb.pdpa.synthetic-prefix=SYN-`, the assumed convention of RWB-E1-065, kept.
- `rwb.pdpa.example-email-domains`, the domains that a fixture may use; every other address fails BR4.
- `rwb.pdpa.allow-list=pdpa-allow.yaml`: rule, path, line or pattern, owner, reason and expiry date; owned by the TechX tech leads through code owners.
- `rwb.pdpa.dictionary-version`: the one pinned reference-data version the rule set is generated from, read through the contract and never a value in the lint.
- `rwb.pdpa.rule-set-version`: derived from the dictionary version and the generator version, so the same version always produces the same rules.
- The personal field marks are owned by Compliance (DL26); the approver role of an allow-list change is the code-owner role, read from the role-to-permission matrix behind the authorise contract (DP-08).

**Build steps**

1. Publish the step, the rule generator and the allow-list check once in the service template and the golden pipeline, and prove that a repository created from the template runs them at the same rule-set version (AC11).
2. Write DictionaryVersionGuard and PersonalFieldReader against the rwb-case reference-data fake; prove that a dictionary that does not answer fails the build closed (AC11).
3. Write RuleGenerator with the snake case, Java getter, camel case and TypeScript variants; test that a newly marked field appears in the rules (AC5).
4. Write the log, entity, exception and text-form rules for Java and TypeScript with one fixture each (AC1, AC2, AC7, AC9, AC10).
5. Write the fixture rules and CheckDigitMatcher (AC3, AC4).
6. Add the masking helper exception to the log rules (AC8), and the allow-list handling with expiry and the code-owner approval through the authorise contract (AC6).
7. Write RuleSetVersionRecorder, add the step to the pull request pipeline, and confirm it prints no value and reads no other service's schema (AC11).

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The twelve test cases of section 16 pass, the step runs from the template in every one of the 19 generated repositories at one rule-set version, a dictionary that cannot be read fails the build closed, and main shows zero findings.

The pinned dictionary version, the operation that serves it, the rule-set version convention and the release quality view are Not specified in the source documents (GAP-1436; ASM-2525; ASM-2527); the version and its fail-closed read are ASM-2525, the approver role is ASM-2526 and the release quality view is ASM-2527.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A finding | {rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper. |
| Build log | An expired allow entry | allow entry expired: {rule} {path} since {date} |
| Repository host | An allow list change without a code owner approval | Review required from code owners |
| Build log | The reference-data contract does not answer at pipeline time | dictionary version not read: {repository} at {dictionaryVersion}. No rule set was generated and the build fails closed. |

Build log text is for developers and is not part of the message standard. The fourth row is the fail-closed read of the pinned dictionary version; it prints the repository and the version it asked for, and never a value of any field.

### 15. Screens and states

No screen in this story. Developers read the findings in the pull request checks, one line per finding with the rule, the file, the line and the field name. The release quality view — findings per repository, per gate and per dictionary version — is a gateway-bff composite route of RWB-PLT-N001-CON (DP-19); this story provides no screen, report or route of its own and invents none.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-011-11 | Access | End to end | An allow list change approved only by a squad member outside the code owners; the merge is refused. This story has no Workbench endpoint, so MSG-P4-002 is not shown |
| TC-TE-011-01 | AC1, BR2, BR7 | Component | Fixture log line with getFirstName() |
| TC-TE-011-02 | AC2, BR2 | Component | Fixture log line with a PartyEntity object |
| TC-TE-011-03 | AC3, BR4 | Component | JSON fixture with a 13-digit number with a valid check digit, made for the test |
| TC-TE-011-04 | AC4, BR3 | Component | SQL seed with and without the SYN- prefix |
| TC-TE-011-05 | AC5, BR1 | Component | Dictionary version marking contract_no personal |
| TC-TE-011-06 | AC6, BR6 | Component | Allow entry expiring 30 November 2026, run on 1 December 2026 |
| TC-TE-011-07 | AC7, BR2 | Component | Front end console.log of lastName |
| TC-TE-011-08 | AC8 | Component | Log line through the masking helper |
| TC-TE-011-09 | AC9, BR2 | Component | Exception message with getCifNo() |
| TC-TE-011-10 | AC10, BR5 | Component | ContactEntity text form with contact_value |
| TC-PLT-TE011-APP-12 | AC11 | Integration | The service template with the generated step and two repositories created from it; one pinned dictionary version read through the rwb-case fake, the same rule-set version in both build records, then a dictionary that returns no answer and a repository pinned to a different rule-set version |

The eleven legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy `System` rows TC-TE-011-01 to TC-TE-011-10 become Component, and the legacy Access row TC-TE-011-11 becomes End to end. TC-PLT-TE011-APP-12 is the new row for AC11. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the personal field marks come from the reference-data contract of rwb-case, and the patterns, the synthetic prefix and the allow list are configuration (DP-07).
- No personal data in logs, tests or prompts: the lint prints field names only and generates its own check-digit fixtures at run time, and no fixture or finding stores a value.
- No read of another module's or another service's tables: the step reads files and the dictionary contract, never `rwb_source_data` or any other schema, and the boundary test of RWB-PLT-TE001-APP fails a cross-schema reference before it could ship (DP-01, DP-05; Arch v5 slide 29).
- An allow-list entry always has an owner, a reason and an expiry date, and its change is approved by the code-owner role resolved through the authorise contract (DP-08).
- The rule-set version always travels with the build record, so a finding is reproduced against the dictionary version that produced it (BR8).
- The step is generated by the template and is never edited in a repository; a change to a rule is a change to the dictionary or to the template, and the build record names both versions (Arch v5 slides 11 and 20).
- The step fails closed: no answer from the dictionary, no rule set, or a scan error is a failed build and never a pass (BR9; Arch v5 slide 35).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Personal data is masked by role in line with PDPA | Business Requirements Program, section 6.7 | None | All recovery processes | None | TC-TE-011-03 to TC-TE-011-06, TC-TE-011-11, TC-PLT-TE011-APP-12 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | Business Requirements Program, section 6.9 | None | All recovery processes | None | TC-TE-011-01, TC-TE-011-02, TC-TE-011-07 to TC-TE-011-10, TC-PLT-TE011-APP-12 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | The step reads no table of any service; the marks arrive through a contract, and the rule set is a build artefact of its own repository | TC-PLT-TE011-APP-12 |
| DP-05 | Template and Rules §R5.5; Arch v5 slide 29 | The ACE field definitions are reached only through rwb-source-data's contract or the `v_ace_*` views, never from a repository read of `rwb_source_data` | TC-TE-011-05, TC-PLT-TE011-APP-12 |
| DP-07 | Template and Rules §R5.5 | The dictionary version and the personal field marks are read through the reference-data contract of rwb-case | TC-TE-011-05, TC-PLT-TE011-APP-12 |
| DP-08 | Template and Rules §R5.5; Arch v5 slide 35 | The approver of an allow-list change is the code-owner role resolved through the authorise contract of rwb-access | TC-TE-011-11 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The release quality view is a gateway-bff composite route; this story provides no route of its own | TC-PLT-TE011-APP-12 |
| Arch v5 slide 11 | Every service publishes its contracts before code, and contract tests run in every build | The step and its rule set are published by the template, and the contract read of the dictionary is a contract test in every build | TC-PLT-TE011-APP-12 |
| Arch v5 slide 29 | One schema and one login per service; no cross-schema read; a boundary test in every build | The dictionary is read through the owner's contract, and no repository opens `rwb_source_data` or another service's schema | TC-PLT-TE011-APP-12 |
| Arch v5 slide 35 | Personal data stays in the owning service, masked, and the pipeline follows 800-204C and 800-204D | The step fails closed, prints no value, and the marks are masked-by-role data owned by Compliance | TC-TE-011-01, TC-TE-011-09, TC-PLT-TE011-APP-12 |
| Arch v5 slide 47 | Risk "Schema rules broken over time", mitigated by grants per schema, a boundary test in every build and review of every new grant | The step runs from the template at one version, and the allow-list approval is a reviewed role decision | TC-TE-011-11, TC-PLT-TE011-APP-12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the authorise contract and the gateway-bff route contract this story builds against |
| RWB-P3-E1043-CON, RWB-P4-E1037-CON | Contract | C: the two service contracts consumed at pipeline time, as published contracts and fakes |
| RWB-PLT-TE001-APP | APP | X: it owns the folder rules and the boundary test this step plugs into; tracked, not blocking |
| RWB-PLT-NF05-OPS | OPS | The gate set that hosts this step; the step is a gate member and does not define the gate set |
| RWB-PLT-NF04-OPS | OPS | The secret and personal-data gate rules that the step consumes for the pattern side; this story owns the dictionary-driven field rules only |

### 19. Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054; RWB-PLT-NF05-OPS and RWB-PLT-NF04-OPS).
- Masking rules by role at run time (RWB-E1-037, delivered by RWB-P4-E1037-CON).
- Masked data in SIT and UAT (RWB-TE-004, delivered by RWB-PLT-TE004-APP).
- Which fields are personal and how long they are kept: Compliance owns them under DL26.
- The dictionary registry operation itself, and the `sys_fields` rows behind it: rwb-source-data (P1) owns them and RWB-P3-E1043-CON publishes the read path.
- The contents of `RWB-PLT-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1043-CON` and `RWB-P4-E1037-CON`; this story builds against them and adds no path.
