# Increment Card — INC-006-epic-1-RWB-TE-011

**RWB-TE-011 — PDPA lint for code, tests and logs**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-006` |
| Title | PDPA lint for code, tests and logs |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-011` |
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 6 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-001 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.

**Business outcome:** Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.

**Main flow:**
1. Build: reads the personal fields from the sys_fields seed and the API specification.
2. Build: generates the lint rule set from the field list: Java getter names, entity class names, JSON property names and TypeScript property names.
3. Lint: scans `src/main` and the front end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
4. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
5. Lint: checks that each entity with a personal field excludes it from its text form.
6. Lint: compares each finding with the allow list; an entry past its expiry does not excuse the finding.

**Acceptance criteria:**
- AC1: Log statement
- AC2: A whole entity in a log
- AC3: A national identifier in a fixture
- AC4: A personal field without the synthetic prefix
- AC5: A field newly marked personal
- AC6: An expired allow list entry
- AC7: The front end
- AC8: A masked value passes
- AC9: An exception message
- AC10: The text form of an entity

**Out of scope:**
- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): the ACE pipeline, outside the recovery backlog.
- Masking rules by role at run time: RWB-E1-037.
- Masked data in SIT and UAT: RWB-TE-004.
- Which fields are personal and how long they are kept: DL26.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-011-pdpa-lint-for-code-tests-and-logs-v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Program, section 6.7 and section 6.9 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the lint; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |

## Contract extract

| Item | Value | |---|---| | Trigger | Every pull request and every build of main | | Input | The sys_fields seed in the schema (is_personal), the API specification, the source and test folders, `pdpa-allow.yaml` | | Rule set | Generated `pdpa-rules.yaml` with rules PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID | | Output | Pass, or fail with rule, file, line and field name for each finding | | Allow list entry | rule, path, line or pattern, owner, reason, expiry date | | Idempotency | The same commit and dictionary give the same findings | | Restart | Rerun the pipeline; the lint holds no state |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration. - No personal data in logs, tests or prompts; the lint itself prints field names only, and its own check digit fixtures are generated at run time and never stored. - No read of another module's tables; the lint reads files only. - An allow list entry always has an owner and an expiry date.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-011-pdpa-lint-for-code-tests-and-logs-v1.md` |
| Specification | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` |
| Compliance validation | `output/INC-006-epic-1-RWB-TE-011/specify/compliance-validation.md` |
| Agent run log | `output/INC-006-epic-1-RWB-TE-011/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-006-epic-1-RWB-TE-011/plan/` |
| Implementation evidence | `output/INC-006-epic-1-RWB-TE-011/implement/` |
| API / functional test reports | `output/INC-006-epic-1-RWB-TE-011/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-006-epic-1-RWB-TE-011/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-011-pdpa-lint-for-code-tests-and-logs-v1.md` |
| Output run | `output/INC-006-epic-1-RWB-TE-011/` |

