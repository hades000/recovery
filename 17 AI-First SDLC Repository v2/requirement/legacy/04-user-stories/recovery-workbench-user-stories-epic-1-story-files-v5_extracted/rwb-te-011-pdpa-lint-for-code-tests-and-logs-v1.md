<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 011 PDPA lint for code tests and logs v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 011 PDPA lint for code tests and logs v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-011 PDPA lint for code, tests and logs

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-011 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Program, section 6.7 and section 6.9 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.

## 2. Business rationale

Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.

## 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the pipeline checks exist.
- The data dictionary marks each personal field (the `is_personal` column of the metadata table sys_fields in the schema, and `x-personal-data: true` in the API specification).
- Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065).
- The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface).

## 4. Flow

1. Build: reads the personal fields from the sys_fields seed and the API specification.
2. Build: generates the lint rule set from the field list: Java getter names, entity class names, JSON property names and TypeScript property names.
3. Lint: scans `src/main` and the front end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
4. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
5. Lint: checks that each entity with a personal field excludes it from its text form.
6. Lint: compares each finding with the allow list; an entry past its expiry does not excuse the finding.
7. Pipeline: fails the build on any finding and prints the rule, the file, the line and the field, without printing the value found.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A log statement writes a personal field | Build fails | Build log: PDPA-LOG-FIELD | AC1 |
| X2 | A log statement writes a whole personal entity | Build fails | Build log: PDPA-LOG-ENTITY | AC2 |
| X3 | A fixture holds a valid Thai national identifier | Build fails | Build log: PDPA-FIXTURE-ID | AC3 |
| X4 | A fixture holds a value in a personal field without the synthetic prefix | Build fails | Build log: PDPA-FIXTURE-FIELD | AC4 |
| X5 | A field is newly marked personal in the dictionary | Rules regenerate; existing uses of the field are found | Build log: PDPA-LOG-FIELD | AC5 |
| X6 | An allow list entry is past its expiry | The finding fails the build | Build log: allow entry expired | AC6 |
| X7 | A front end console or logger call writes a personal property | Build fails | Build log: PDPA-LOG-FIELD | AC7 |
| X8 | A log statement writes a field through the masking helper | Passes | None | AC8 |
| X9 | An exception message carries a personal field | Build fails | Build log: PDPA-EXCEPTION | AC9 |
| X10 | An entity's text form includes a personal field | Build fails | Build log: PDPA-TOSTRING | AC10 |
| X11 | A person outside the code owners approves an allow list change | Merge refused | Repository host: review required from code owners | Access test TC-TE-011-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the pipeline of RWB-TE-001 and the dictionary seed |
| Negotiable | Patterns, the synthetic prefix and the allow list are configuration |
| Valuable | Personal data stays out of logs, artifacts and prompts |
| Estimable | One rule generator, one rule set, one allow list, one pipeline step |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one fixture file with one finding |

## 7. Acceptance criteria

```gherkin
Feature: PDPA lint for code, tests and logs

  Background:
    Given the data dictionary marks first_name, last_name, cif_no, id_no_token, date_of_birth, value_token, summary and field_value as personal

  Scenario: AC1 Log statement
    Given a log statement in "recovery.casewf.internal.SampleService" that writes party.getFirstName()
    When the pipeline runs
    Then the PDPA lint fails the build
    Then the build log names rule PDPA-LOG-FIELD, the file, the line and field first_name, and does not print a value

  Scenario: AC2 A whole entity in a log
    Given a log statement that writes the object "party" of type PartyEntity
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-ENTITY

  Scenario: AC3 A national identifier in a fixture
    Given a JSON fixture whose "idNoToken" holds a 13-digit number with a valid check digit, generated by the test at run time
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-ID

  Scenario: AC4 A personal field without the synthetic prefix
    Given a SQL seed that sets last_name to "TESTNAME"
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-FIELD
    Then the same seed with last_name "SYN-LAST-0001" passes

  Scenario: AC5 A field newly marked personal
    Given the dictionary marks loan_account.contract_no as personal in a new version
    Given a log statement writes account.getContractNo()
    When the pipeline runs
    Then the system regenerates the rule set with contract_no
    Then the build fails with rule PDPA-LOG-FIELD for contract_no

  Scenario: AC6 An expired allow list entry
    Given the allow list excuses PDPA-FIXTURE-FIELD in "ace-service/src/test/resources/recovery/legacy-seed.sql" until 30 November 2026
    When the pipeline runs on 1 December 2026
    Then the build fails with "allow entry expired"

  Scenario: AC7 The front end
    Given a component in "src/modules/recovery/caserecord" that calls console.log(party.lastName)
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-FIELD for lastName

  Scenario: AC8 A masked value passes
    Given a log statement that writes the contact point through the masking helper
    When the pipeline runs
    Then the lint passes for that line

  Scenario: AC9 An exception message
    Given code that throws an exception with message "No case for " + party.getCifNo()
    When the pipeline runs
    Then the build fails with rule PDPA-EXCEPTION for cif_no

  Scenario: AC10 The text form of an entity
    Given ContactPointEntity includes value_token in its text form
    When the pipeline runs
    Then the build fails with rule PDPA-TOSTRING for value_token
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The personal field list is read from the data dictionary and the API specification, never written in the lint | Logical Data Model, Personal data column; API x-personal-data |
| BR2 | No log statement, string built for a log, or exception message carries a personal field or a whole personal entity | NFR-054; CTL-11 |
| BR3 | Test fixtures, seeds and end-to-end data carry only synthetic values with the prefix "SYN-" in personal fields | NFR-045; RWB-E1-065 |
| BR4 | Literals matching a Thai national identifier with a valid check digit, a Thai mobile number or an email outside the example domains fail anywhere in code or tests | NFR-054 |
| BR5 | An entity with a personal field leaves it out of its text form | CTL-11 |
| BR6 | A finding is excused only by an allow list entry with an owner, a reason and an expiry date not yet passed | Principle 1 applied to build configuration |
| BR7 | The lint never prints the value it found | REQ-ACA-005 |

## 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a finding is not excused.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the lint; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PTY-002 | party | cif_no | Read (definition) |
| DF-PTY-004 | party | first_name | Read (definition) |
| DF-PTY-005 | party | last_name | Read (definition) |
| DF-PTY-007 | party | id_no_token | Read (definition) |
| DF-PTY-008 | party | date_of_birth | Read (definition) |
| DF-PTY-010 | party | vulnerable_flag | Read (definition) |
| DF-PTY-011 | party | deceased_flag | Read (definition) |
| DF-PTY-012 | party | bankruptcy_flag | Read (definition) |
| DF-PTY-016 | contact_point | value_token | Read (definition) |
| DF-INT-011 | interaction | summary | Read (definition) |
| DF-DOC-015 | document_field | field_value | Read (definition) |

The lint reads which fields are personal; it never reads their values. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Item | Value |
|---|---|
| Trigger | Every pull request and every build of main |
| Input | The sys_fields seed in the schema (is_personal), the API specification, the source and test folders, `pdpa-allow.yaml` |
| Rule set | Generated `pdpa-rules.yaml` with rules PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID |
| Output | Pass, or fail with rule, file, line and field name for each finding |
| Allow list entry | rule, path, line or pattern, owner, reason, expiry date |
| Idempotency | The same commit and dictionary give the same findings |
| Restart | Rerun the pipeline; the lint holds no state |

## 13. Solution plan

**Package.** Folder `tools/pdpa-lint` in the ACE repository; rules applied to the recovery back end and front end folders.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PersonalFieldReader | Service | Reads the personal fields from the schema seed and the API specification (BR1) |
| RuleGenerator | Service | Writes pdpa-rules.yaml with name variants: snake case, Java getter, camel case property |
| pdpa-rules.yaml | Rule table | The generated rules (BR2 to BR5) |
| pdpa-allow.yaml | Rule table | Allow list entries with owner and expiry (BR6) |
| CheckDigitMatcher | Service | Thai national identifier check digit test for BR4 |
| PdpaLintStep | Job | Pipeline step that runs the scan and prints findings without values (BR7) |

**Database.** None. The schema seed is read as a file.

**Configuration and reference data.** The synthetic prefix "SYN-" (assumed), the example email domains, the allow list; owned by the TechX tech leads through code owners. The personal field marks are owned by Compliance (DL26).

**Build steps**

1. Write PersonalFieldReader and RuleGenerator; test that a newly marked field appears in the rules (AC5).
2. Write the log, entity, exception and text form rules for Java and TypeScript with one fixture each (AC1, AC2, AC7, AC9, AC10).
3. Write the fixture rules and CheckDigitMatcher (AC3, AC4).
4. Add the masking helper exception to the log rules (AC8).
5. Write the allow list handling with expiry (AC6).
6. Add PdpaLintStep to the pull request pipeline and confirm it prints no value.

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The tests in section 16 pass and the lint runs on main with zero findings.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A finding | {rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper. |
| Build log | An expired allow entry | allow entry expired: {rule} {path} since {date} |
| Repository host | An allow list change without a code owner approval | Review required from code owners |

Build log text is for developers and is not part of the message standard.

## 15. Screens and states

No screen in this story. Developers read the findings in the pull request checks.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-011-01 | AC1, BR2, BR7 | System | Fixture log line with getFirstName() |
| TC-TE-011-02 | AC2, BR2 | System | Fixture log line with a PartyEntity object |
| TC-TE-011-03 | AC3, BR4 | System | JSON fixture with a 13-digit number with a valid check digit, made for the test |
| TC-TE-011-04 | AC4, BR3 | System | SQL seed with and without the SYN- prefix |
| TC-TE-011-05 | AC5, BR1 | System | Dictionary version marking contract_no personal |
| TC-TE-011-06 | AC6, BR6 | System | Allow entry expiring 30 November 2026, run on 1 December 2026 |
| TC-TE-011-07 | AC7, BR2 | System | Front end console.log of lastName |
| TC-TE-011-08 | AC8 | System | Log line through the masking helper |
| TC-TE-011-09 | AC9, BR2 | System | Exception message with getCifNo() |
| TC-TE-011-10 | AC10, BR5 | System | ContactPointEntity text form with value_token |
| TC-TE-011-11 | Access | Access | An allow list change approved only by a squad member outside the code owners; the merge is refused. This story has no Workbench endpoint, so MSG-P4-002 is not shown |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration.
- No personal data in logs, tests or prompts; the lint itself prints field names only, and its own check digit fixtures are generated at run time and never stored.
- No read of another module's tables; the lint reads files only.
- An allow list entry always has an owner and an expiry date.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Personal data is masked by role in line with PDPA | Business Requirements Program, section 6.7 | None | All recovery processes | None | TC-TE-011-03 to TC-TE-011-06, TC-TE-011-11 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | Business Requirements Program, section 6.9 | None | All recovery processes | None | TC-TE-011-01, TC-TE-011-02, TC-TE-011-07 to TC-TE-011-10 |

## 19. Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): the ACE pipeline, outside the recovery backlog.
- Masking rules by role at run time: RWB-E1-037.
- Masked data in SIT and UAT: RWB-TE-004.
- Which fields are personal and how long they are kept: DL26.
