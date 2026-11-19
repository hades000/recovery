# Technical Specification — RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| Story | RWB-TE-011 — PDPA lint for code, tests and logs |
| Epic / module | E1 / P2 Integration (technical enabler) |
| RUN_ID | `INC-007-epic-1-RWB-TE-011` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 011 PDPA lint for code tests and logs v1.md`; REQ-RDF-010; REQ-ACA-005; BRD Program §6.7, §6.9 |
| Upstream IDs | REQ-RDF-010; REQ-ACA-005; NFR-045; NFR-054; CTL-11; DL26; RWB-E1-065; RWB-E1-037 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | TechX tech leads (code owners); Compliance and PDPA officer owns the personal-field marks (DL26); see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label, state or validation presentation. The lint scans front-end source but adds no UI code. |
| Logic In Scope | `YES` — personal-field rule generation, code/test/log matching, check-digit validation, allow-list expiry and reporting. |
| API In Scope | `NO` — no endpoint or schema change. The lint reads `x-personal-data` from the existing API specification. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | ACE pull request pipeline; recovery back-end and front-end source trees; `src/test` fixtures and SQL seeds; `sys_fields` metadata seed; `api/recovery-api.yaml` `x-personal-data` marks. |
| New Nodes Required | `YES` — `tools/pdpa-lint`; `PersonalFieldReader`; `RuleGenerator`; `pdpa-rules.yaml`; `pdpa-allow.yaml`; `CheckDigitMatcher`; `PdpaLintStep`. |
| Inherited Existing Behavior | Data dictionary and `sys_fields` marks (DL26); API specification; synthetic data convention (RWB-E1-065); masking helper in the common module (RWB-E1-037); code owners (RWB-TE-002); pipeline from RWB-TE-001. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` — the lint tool and pipeline step are back-end build code; no service runtime change. |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The personal field list is read from the data dictionary and the API specification, never written in the lint. | SPEC-RWB-TE-011-001, SPEC-RWB-TE-011-002 | DIRECT | `sys_fields.is_personal` plus `x-personal-data: true`; rule set regenerated each build. | COVERED |
| BR2 | No log statement, string built for a log, or exception message carries a personal field or a whole personal entity. | SPEC-RWB-TE-011-003..005 | DIRECT | Java and TypeScript matchers for getters, properties and object arguments. | COVERED |
| BR3 | Test fixtures, seeds and end-to-end data carry only synthetic values with the prefix `SYN-` in personal fields. | SPEC-RWB-TE-011-007 | DIRECT | Literal in a personal field position must start with `SYN-`. | COVERED |
| BR4 | Literals matching a Thai national identifier with a valid check digit, a Thai mobile number or an email outside the example domains fail anywhere. | SPEC-RWB-TE-011-008 | DIRECT | Check-digit algorithm plus configurable mobile/email patterns. | COVERED |
| BR5 | An entity with a personal field leaves it out of its text form. | SPEC-RWB-TE-011-006 | DIRECT | `toString`, `equals` display and generated text forms checked. | COVERED |
| BR6 | A finding is excused only by an allow-list entry with an owner, a reason and an expiry date not yet passed. | SPEC-RWB-TE-011-011, SPEC-RWB-TE-011-012 | DIRECT | Entry schema; expired entry does not excuse. | COVERED |
| BR7 | The lint never prints the value it found. | SPEC-RWB-TE-011-013 | DIRECT | Report holds rule, file, line and field name only. | COVERED |
| X1 | A log statement writes a personal field. | SPEC-RWB-TE-011-003 | DIRECT | PDPA-LOG-FIELD. | COVERED |
| X2 | A log statement writes a whole personal entity. | SPEC-RWB-TE-011-004 | DIRECT | PDPA-LOG-ENTITY. | COVERED |
| X3 | A fixture holds a valid Thai national identifier. | SPEC-RWB-TE-011-008 | DIRECT | PDPA-FIXTURE-ID. | COVERED |
| X4 | A fixture holds a personal value without `SYN-`. | SPEC-RWB-TE-011-007 | DIRECT | PDPA-FIXTURE-FIELD. | COVERED |
| X5 | A field is newly marked personal. | SPEC-RWB-TE-011-001, SPEC-RWB-TE-011-002 | DIRECT | Rules regenerate; existing uses found. | COVERED |
| X6 | An allow entry is past its expiry. | SPEC-RWB-TE-011-012 | DIRECT | `allow entry expired`. | COVERED |
| X7 | A front-end logger writes a personal property. | SPEC-RWB-TE-011-009 | DIRECT | PDPA-LOG-FIELD. | COVERED |
| X8 | A log statement writes through the masking helper. | SPEC-RWB-TE-011-010 | DIRECT | Passes. | COVERED |
| X9 | An exception message carries a personal field. | SPEC-RWB-TE-011-005 | DIRECT | PDPA-EXCEPTION. | COVERED |
| X10 | An entity's text form includes a personal field. | SPEC-RWB-TE-011-006 | DIRECT | PDPA-TOSTRING. | COVERED |
| X11 | A person outside the code owners approves an allow-list change. | SPEC-RWB-TE-011-018 | DIRECT | Merge refused; no Workbench endpoint, so MSG-P4-002 is not shown. | COVERED |
> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation
As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.

The story builds a lint tool whose rules are generated from the data dictionary and the API specification. It scans Java and TypeScript for log calls, string building, exception messages and text forms; it scans fixtures and seeds for non-synthetic values and for identifiers that look real; it honours an allow list with an owner and an expiry. It adds no screen and no endpoint. The control is a failed build.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Every pull request and every build of `main`. |
| Preconditions | RWB-TE-001 done; `sys_fields` marks each personal field; the API file marks `x-personal-data: true`; synthetic data uses `SYN-` (RWB-E1-065 convention); the common module masking helper is available. |
| Input | `sys_fields` seed; `api/recovery-api.yaml`; back-end and front-end source; `src/test` fixtures, SQL seeds and JSON; `pdpa-allow.yaml`. |
| Output | Pass, or a finding with rule, file, line and field name — never the value; an expired allow entry fails. |
| Feature flag | None — a build check has no runtime path. |
## Field-level behaviour matrix
| Entity / artefact | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `sys_fields` | `is_personal` | Data dictionary (DL26) | Editable by Compliance | Authoritative personal mark |
| API schema property | `x-personal-data` | API file | Editable by pull request | `true` adds the property to the rule set |
| `pdpa-rules.yaml` | `rule`, `field`, `name_variants`, `pattern` | Generated | Not hand-edited | Regenerated each build |
| `pdpa-allow.yaml` | `rule`, `path`, `line_or_pattern`, `owner`, `reason`, `expiry` | Tech leads | Editable by pull request | All six required; expiry not passed |
| Finding | `rule`, `file`, `line`, `field` | Lint run | Read-only | Never includes the value |
| `party.first_name`, `last_name`, `cif_no`, `id_no_token`, `date_of_birth` | definition only | Dictionary | Read-only | The lint reads the definition, never the value |
| `party.vulnerable_flag`, `deceased_flag`, `bankruptcy_flag`; `contact_point.value_token`; `interaction.summary`; `document_field.field_value` | definition only | Dictionary | Read-only | Sensitive attributes, token and free text; personal when marked |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Build passed | A finding is introduced | No valid allow entry | Build failed | Finding reported without the value; merge blocked |
| Build failed | The value is removed or masked, or a valid allow entry is added | Rule satisfied | Build passed | Merge allowed subject to review |
| Allow entry active | The build date passes `expiry` | Date after expiry | Allow entry expired | The finding fails the build |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Log writes a personal field | Build fails | `PDPA-LOG-FIELD: file:line uses personal field {field}` |
| X2 | Log writes a whole personal entity | Build fails | `PDPA-LOG-ENTITY` |
| X3 | Fixture holds a valid national identifier | Build fails | `PDPA-FIXTURE-ID` |
| X4 | Fixture holds a personal value without `SYN-` | Build fails | `PDPA-FIXTURE-FIELD` |
| X5 | Field newly marked personal | Rules regenerate; uses found | `PDPA-LOG-FIELD` |
| X6 | Allow entry expired | Finding fails | `allow entry expired: {rule} {path} since {date}` |
| X7 | Front-end logger writes a personal property | Build fails | `PDPA-LOG-FIELD` |
| X8 | Log uses the masking helper | Passes | None |
| X9 | Exception message carries a personal field | Build fails | `PDPA-EXCEPTION` |
| X10 | Text form includes a personal field | Build fails | `PDPA-TOSTRING` |
| X11 | Non-code-owner approves an allow-list change | Merge refused | Repository host: `Review required from code owners` |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | None. The lint reads the API file as a document; it does not call an endpoint. |
| Contract delta | None. `x-personal-data` already marks the personal properties the lint reads. |
| Backward compatibility | Unchanged. |
| Authorization | Repository rights for allow-list changes; no Workbench capability area. |
| Error behaviour | Build failure with rule, file, line and field; no value printed. |
| Versioning | No version change. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-RWB-TE-011-009 | No component, screen, route or state change. The lint scans front-end source; the rule is proven by a fixture in the pipeline (TC-TE-011-07). | Existing front-end suite stays green; the fixture fails with PDPA-LOG-FIELD. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR7; SPEC-RWB-TE-011-001..021 | New `PersonalFieldReader`, `RuleGenerator`, matchers, `CheckDigitMatcher`, allow-list handling and pipeline step. | Unit tests cover each rule, name variant generation, check-digit pass/fail, `SYN-` pass/fail, masking-helper pass, allow-list active/expired and no-value reporting. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `PersonalFieldReader` | Service | Reads `sys_fields.is_personal` and API `x-personal-data`; builds the field list (BR1). |
| `RuleGenerator` | Service | Writes `pdpa-rules.yaml` with snake case, Java getter, camel-case property and TypeScript property names. |
| `pdpa-rules.yaml` | Rule table | Generated rules PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD, PDPA-FIXTURE-ID. |
| `pdpa-allow.yaml` | Rule table | Allow entries with rule, path, line or pattern, owner, reason and expiry. |
| `CheckDigitMatcher` | Service | Thai national identifier check-digit test (13 digits, mod 11). |
| `PdpaLintStep` | Job | Pipeline step that runs the scan and prints findings without values (BR7). |

### Package and scope
Folder `tools/pdpa-lint` in the ACE repository. Applies to the recovery back-end and front-end folders. The lint reads files only; it does not call the service, the database or another module. Generated code is scanned; if a generated text form trips a rule, the generator template is fixed, never the generated file.

### Data and migration
No database object and no Flyway migration. The `sys_fields` seed is read as a file. The lint reads definitions only; it never reads a value.

### Rules
1. Generate the rule set from the dictionary and the API file on every build; a newly marked field is picked up without a code change.
2. Java: match log calls (`log.*`, `System.out`, `System.err`), string concatenation used as a log argument, exception constructor arguments, and `toString`/text-form bodies.
3. TypeScript: match `console.*` and the approved logger, plus template strings passed to them.
4. Fixtures and seeds: a literal in a personal-field position must start with `SYN-`; a 13-digit value with a valid check digit fails anywhere; a Thai mobile or non-example email fails (BR4).
5. A whole personal entity passed to a log or exception fails (BR2).
6. An allow entry excuses only when rule, path and line/pattern match and `expiry` is today or later (BR6).
7. The report prints rule, file, line and field name only (BR7).

### Transaction and events
None. The lint is stateless and deterministic for the same commit, dictionary and allow list. A rerun needs no cleanup.

### Security and authority
| Actor | What they may do |
|---|---|
| RW-TRIBE, tribe lead, squad members | Run the lint; propose an allow entry by pull request |
| TechX tech leads | Approve allow-list and rule changes (code owners, RWB-TE-002) |
| RW-COMPLY | Owns which fields are personal through the dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |

An allow-list change is a reviewed pull request; a non-owner approval does not satisfy the code-owner review.

### Observability and operations
- The finding count is the measure; merged personal-data findings target zero.
- The report is attached to the pull request; the lint runs on `main` with zero findings.
- No runtime metric, alert or run book.

### Performance
No runtime path. The scan runs in the pull request pipeline; no numeric target is stated. Cache the parsed rule set per build and scan in parallel by file to keep the step inside the pipeline budget.

### Feature flag and rollback
None. Rollback is a revert of a rule or allow-list change through a pull request.

### No UI change
No screen. Developers read findings in the pull request checks.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-011-01 | BR2, BR7 | System | Fixture log line with `getFirstName()` | Fails PDPA-LOG-FIELD; file, line, `first_name`; no value |
| TC-TE-011-02 | BR2 | System | Fixture log line with a `PartyEntity` object | Fails PDPA-LOG-ENTITY |
| TC-TE-011-03 | BR4 | System | JSON fixture with a valid 13-digit identifier, generated at run time | Fails PDPA-FIXTURE-ID |
| TC-TE-011-04 | BR3 | System | SQL seed with and without `SYN-` | `TESTNAME` fails; `SYN-LAST-0001` passes |
| TC-TE-011-05 | BR1 | System | Dictionary version marking `contract_no` personal | Rules regenerate; log use fails |
| TC-TE-011-06 | BR6 | System | Allow entry expiring 2026-11-30, build on 2026-12-01 | `allow entry expired` |
| TC-TE-011-07 | BR2 | System | Front-end `console.log(party.lastName)` | Fails PDPA-LOG-FIELD for `lastName` |
| TC-TE-011-08 | Engineering verification | System | Log line through the masking helper | Passes |
| TC-TE-011-09 | BR2 | System | Exception message with `getCifNo()` | Fails PDPA-EXCEPTION for `cif_no` |
| TC-TE-011-10 | BR5 | System | `ContactPointEntity` text form with `value_token` | Fails PDPA-TOSTRING |
| TC-TE-011-11 | X11 | Security | Allow-list change approved only by an outside squad member | Merge refused; no Workbench message |
| TC-TE-011-12 | BR1, BR2 | Unit | Field list with one field and all four name variants | Every variant matches; unrelated name does not |
| TC-TE-011-13 | BR4 | Unit | Check-digit valid, invalid and non-13-digit values | Only the valid 13-digit value fails |
## Guardrails
- No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration.
- No personal data in logs, tests or prompts; the lint prints field names only, and its check-digit fixtures are generated at run time and never stored.
- No read of another module's tables; the lint reads files only.
- An allow-list entry always has an owner and an expiry date; the lint never prints the value it found.
## Out of scope
- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): the ACE pipeline, outside the recovery backlog.
- Masking rules by role at run time: RWB-E1-037.
- Masked data in SIT and UAT: RWB-TE-004.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Personal data is masked by role in line with PDPA | Program §6.7 | None | All recovery processes | None | TC-TE-011-03..06, TC-TE-011-11 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | Program §6.9 | None | All recovery processes | None | TC-TE-011-01, 02, 07..10, 12, 13 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-007 | The `SYN-` prefix is assumed from RWB-E1-065. | A different convention would change every fixture check. | Use `SYN-`; it is the synthetic data convention and is configuration in `pdpa-rules.yaml`. | RESOLVED | SPEC-007 |
| CLAR-002 | BR4; SPEC-008 | The example email domains are not listed. | Determines which email literals fail. | Use the RFC 2606 reserved domains plus the bank's synthetic domain; Compliance owns the list under DL26. | RESOLVED | SPEC-008 |
| CLAR-003 | BR4; SPEC-008 | The Thai mobile pattern is not specified. | Determines the mobile matcher. | Hold the pattern in configuration, seeded from the dictionary's contact-point validation; the national ID check digit is the acceptance-tested matcher. | RESOLVED | SPEC-008 |
| CLAR-004 | §7 Background; §11 Data | The background lists 8 personal fields; the data table lists 11. | A mismatch would leave three fields unscanned. | `sys_fields.is_personal` is authoritative; the 8-field list is a fixture subset. The 11 field IDs are read as definitions. | RESOLVED | SPEC-001 |
| CLAR-005 | BR1; SPEC-001 | Does the lint scan generated code? | Generated models could trip the rules. | Scan `src/main` including generated code; fix the generator template, never the generated file. | RESOLVED | SPEC-002 |
| CLAR-006 | BR6; SPEC-011 | Who approves an allow-list change? | Determines the review control. | The TechX tech leads as code owners; a non-owner approval does not satisfy the review. | RESOLVED | SPEC-018 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, DL26 or the synthetic data convention.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this pipeline-control story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New PDPA lint and allow-list control over code, tests and logs; no screen, endpoint or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time personal-data control only]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 7 business rules, 11 exception paths and the allow-list access path are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
