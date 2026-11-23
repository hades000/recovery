# RWB-PLT-E1047-CON Feature flags for module release with a removal date

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-047 for the platform shared libraries. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1047-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-047 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018) |
| Status | Draft (realignment v1) |

### 1. Story

As a **consumer of the platform shared libraries**, I want **the contract baseline for feature flags published on Day 1 with a working fake: the flag-key and change-row schemas, the `FeatureFlags` interface and its off-by-default rule, the four documented operations with their problem details and their `Idempotency-Key` rule, the weekly removal report input and output, the versioning rule and the fake**, so that **every service, rwb-integration's admin component and the front end can build and test against stable schemas before the store and the library exist**.

This is the contract story of legacy RWB-E1-047. It publishes, under the Ownership Map ruling that keeps the flags with the platform library:

- OpenAPI 3.1 documents for the four documented operations, with one problem envelope, the `Idempotency-Key` rule on the POST, the `If-Match` rule on the PATCH and the versioning rule.
- The schemas of the two PLT-owned tables, `feature_flag` and `feature_flag_change`, so the store migration, the app story and the fake agree.
- The `FeatureFlags` interface as the client library publishes it, with the off-by-default rule for an unknown key and for an unreadable store with no cached value.
- The input and the output of the weekly removal report, which is a Temporal Schedule and not a workflow (DP-10).
- A contract fake that answers every documented operation and every example in this document.

The four paths carry no service segment, because the platform library has no service short: they stay exactly as the Ownership Map names them, `GET /feature-flags`, `GET /admin/feature-flags`, `POST /admin/feature-flags` and `PATCH /admin/feature-flags/{flagKey}`, at v1 (ASM-2463). The environment and owner-team codes are reference data of rwb-case and are consumed, not republished (DP-07; contract dependency RWB-P3-E1043-CON). This story builds nothing that writes a business table, has no build dependency and starts on Day 1.

### 2. Business rationale

The legacy story exposed its behaviour through a Java interface and four endpoints inside one application, and both the interface and the endpoints were documented in prose only. In the target the interface ships inside nineteen services and the endpoints are served once by rwb-integration, so the two artefacts that other teams depend on — the interface signature and the HTTP surface — need one published, versioned source with a fake, or every consumer invents its own reading of them. Contract-first publication removes that wait (DP-11): the app story, the admin component, the front end hook and every service build and test from Day 1, a contract test fails the build when a field drifts, and the removal-report input and output are agreed before the first Schedule runs.

It also fixes the boundary the realignment depends on: the flags belong to the platform, the store is PLT-owned, the HTTP surface is served by rwb-integration against the library, and no service is invited to read the store or to copy the four paths. That is what keeps REQ-DRI-010 true after the split: a value changes as data, in one place, and every service sees it through one interface.

### 3. Preconditions

- The platform shared libraries are the owner of feature flags (Template and Rules §R3 default ruling; Ownership Map: `feature_flag` and `feature_flag_change` are PLT).
- The four paths are fixed exactly as the Ownership Map names them, at v1 and with no service segment (ASM-2463). The library has no service short, so it declares no REST base, no topic and no Temporal task queue of its own.
- The field identifiers DF-OPS-207 to DF-OPS-223 and the standard columns `created_by` and `created_at` are taken from the Logical Data Model and Data Dictionary, character for character.
- The legacy message IDs MSG-GEN-001, MSG-GEN-003, MSG-GEN-004, MSG-GEN-005, MSG-P2-003, MSG-P2-016 and MSG-P4-002 are used unchanged in the error and success examples.
- The schedule pattern of DP-10 is in force: the weekly report is a Temporal Schedule with overlap SKIP (build dependency RWB-PLT-E1071-CON), not a Quartz job.
- The schema names of the two tables are Not specified in the source documents (GAP-1412; ASM-2465), so the documents carry the placeholder and never invent a schema.
- No approval is required to publish a Draft contract: the baseline is published at status Draft (realignment v1) and the version is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document for the four documented operations, exactly as the Ownership Map names the paths, with one tag per resource: Flags, Administration.
2. The author writes the FeatureFlag and FeatureFlagChange schemas from the two tables of section 12, so the documents, the tables and the fake cannot drift.
3. The author publishes the `FeatureFlags` interface as the client library declares it, with the off-by-default rule written in the document as a testable sentence.
4. The author writes the input and the output of the weekly removal report as the Schedule declares them, and states the overlap policy and the idempotency key.
5. The lint and schema steps run: OpenAPI 3.1 validation, one problem envelope, `Idempotency-Key` on the POST, `If-Match` on the PATCH, no service segment in any path, no personal data in any example.
6. The contract fake is generated from the documents; it answers every operation and every example of this story, including the error examples of section 14.
7. The documents and the fake are published to the contract registry at v1; the consuming stories (RWB-PLT-E1047-APP, the rwb-integration admin component and every service that reads a flag) pin the version.
8. A contract test in this story runs the fake against the documents on every change; a breaking change raises a new version and marks v1 deprecated.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | An operation is published without a 4xx problem envelope | The lint step fails the build and the document is not published | Lint finding, no message id |
| X2 | The POST operation declares no `Idempotency-Key` header | The lint step fails the build | Lint finding, no message id |
| X3 | A path is published with a service segment | The lint step fails the build; the four paths stay exactly as the Ownership Map names them | Lint finding, no message id |
| X4 | An example carries a personal name, an email address or an account number | The review step rejects the example; only user IDs and team codes appear | Review finding |
| X5 | A schema invents a table schema name or a column that no source defines | The schema review rejects the change; the placeholder and the gap stay | GAP-1412 |
| X6 | A consumer needs a field that no source defines | The field is not invented: the schema carries the placeholder and a gap is raised | GAP-1412 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds nothing and depends on nothing |
| Negotiable | Field order, example values and error detail layout are open until the version is frozen |
| Valuable | The app story, the admin component, the front end and every service start on Day 1 against the fake |
| Estimable | Four operations, two schemas, one interface, one report input and output, one fake |
| Small | One sprint for the documents and the fake, with the lint and contract tests |
| Testable | Each criterion is a schema or lint assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Platform feature-flag contract baseline

  Background:
    Given the platform library has no service short
    Given the contract version is v1

  Scenario: AC1 The flag-key and change-row schemas are published (new, D-RCV-60)
    Given the OpenAPI 3.1 document for the platform library flag surface
    When it is validated
    Then the FeatureFlag schema carries key, description, ownerTeam, the value per environment for DEV, SIT, UAT and PROD, removalDate, daysOverdue and version
    Then the key is constrained by the pattern ^rwb\.[a-z0-9]+\.[a-z0-9-]+$ and removalDate is required
    Then the FeatureFlagChange schema carries flagKey, environment, oldValue, newValue, reason, createdBy and createdAt
    Then no field is published that no source defines, and a needed field with no source carries the placeholder

  Scenario: AC2 The FeatureFlags interface and its off-by-default rule are published (new, D-RCV-60)
    Given the client library declaration of FeatureFlags
    When a consuming service builds against it
    Then it publishes boolean isOn(String flagKey)
    Then an unknown key returns false and an unreadable store with no cached value returns false
    Then the document states the value is cached per service for 30 seconds (assumed; DL11) as a configurable chart value, never a code constant
    Then the interface is the only way a service reads a flag, and no service reads the store

  Scenario: AC3 The four operations, the problem details and the Idempotency-Key rule are published (new, D-RCV-60)
    Given the four paths exactly as the Ownership Map names them: GET /feature-flags, GET /admin/feature-flags, POST /admin/feature-flags and PATCH /admin/feature-flags/{flagKey}
    When the document is linted
    Then no path carries a service segment and every path is at v1
    Then POST requires the Idempotency-Key header and answers 409 when the key already exists (MSG-GEN-004)
    Then PATCH requires If-Match with the version and a non-empty reason, and answers 404 (MSG-P2-016), 409 (MSG-GEN-004) and 422 (MSG-GEN-001)
    Then POST answers 422 with MSG-GEN-001 and MSG-GEN-003
    Then every error is one problem envelope and the 403 example carries MSG-P4-002

  Scenario: AC4 The weekly removal report input and output are published (new, D-RCV-60)
    Given the schedule Flag removal report, Monday 08:00 Asia/Bangkok, overlap SKIP, owner PLT
    When the report input and output are validated
    Then the input is the active flags whose removal date is before today
    Then the output is one email per owner and one to the RW-PLATADM group, with one MSG-P2-003 log line per flag naming the flag, the removal date and the owner
    Then the idempotency key is the report date, so a rerun on the same date sends nothing new
    Then no Temporal workflow is published, because the deliverable is a Schedule

  Scenario: AC5 The versioning and compatibility rule is published (new, D-RCV-60)
    Given version v1 of the documents and of the interface
    When a published field is added or renamed
    Then a backward-compatible addition keeps v1 and a breaking change raises v2 and marks v1 deprecated
    Then the documents and the fake are published at the same version
    Then a consumer that pins v1 keeps working until v2 is in force

  Scenario: AC6 The fake answers every document and every example (new, D-RCV-60)
    Given the contract fake generated from the published documents
    When the contract test runs
    Then it answers the four operations with the success and error examples of section 14
    Then it answers the three interface cases: a known key, an unknown key and an unreadable store with no cached value
    Then the examples carry no personal data, only user IDs and team codes
    Then a change to a published field fails the contract test until the version is raised
```

These criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every value in the examples comes from the legacy story or from the field identifiers, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Unfinished work is behind a flag; a flag that is off returns the previous code path | Legacy BR1; DT11; ADR-008 |
| BR2 | Every flag has a key, an owner, a value per environment (DEV, SIT, UAT, PROD) and a removal date | Legacy BR2 |
| BR3 | A flag value changes without a code release, and each change is logged with user, time and reason | Legacy BR3; REQ-DRI-010 |
| BR4 | A flag past its removal date is reported to its owner every week until it is removed | Legacy BR4 |
| BR5 | An unknown key or an unreadable store gives off, never on | Legacy BR5; DT11 |
| BR6 | Flag keys follow `rwb.<module>.<short-name>` | Legacy BR6; DP-14 |
| BR7 | Every POST carries `Idempotency-Key`; a repeat returns the first result, and a duplicate key answers 409 | Architecture v5 Text Extract v1 slide 11; legacy contract row |
| BR8 | The contract publishes platform resources only; no service may read the store or copy the four paths | DP-01; Ownership Map; ASM-2463 |

### 9. State transitions

None in this story: a document has no runtime state. The states the documents describe are the flag value per environment (off to on, on to off) and the flag's is_active column when a flag is retired, each with the HTTP status that produces it: 201 on create, 200 on change, 404 for an unknown key, 409 for a version conflict and 422 for a refused value or date. The behaviour itself is the one specified in RWB-PLT-E1047-APP section 9.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents, the interface declaration and the fake |
| The platform library owner | Approves a breaking change and a version freeze |
| The consumer teams (every service, rwb-integration, the front end) | Read the documents, pin a version, raise a change request |
| rwb-case (P3) | Owns the reference-data contract this document consumes for the environment and owner-team codes |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

Role names appear in the examples only as role codes, resolved by rwb-access (P4) at run time (DP-08). No personal name, no email address and no credential appears in a document or an example.

### 11. Data

| Item | Value |
|---|---|
| Field identifiers published | DF-OPS-207 to DF-OPS-217 (feature_flag); DF-OPS-218 to DF-OPS-223 (feature_flag_change); the standard columns created_by and created_at |
| Field identifiers referenced, not published | DF-REF-035 (`role.role_code`), reached over the rwb-access contract (DP-08) |
| Table schema names | Not specified in the source documents (GAP-1412; ASM-2465) |
| Personal data in examples | None. Owners and approvers appear as user IDs and team codes only |
| Report artefacts | One email per owner and one to the RW-PLATADM group; one log line per flag with MSG-P2-003; no file, no event |

The documents carry no value that no source holds. Where a consumer needs a field that neither the legacy story nor the field identifiers define, the schema carries the placeholder text and the change waits for the gap to close; this is a draft baseline, so a new version can add the field without breaking a consumer.

### 12. Contract

**12.1 REST operations provided**

| Operation | Document | Request | Responses | Owner |
|---|---|---|---|---|
| GET /feature-flags | feature-flags.yaml | None | 200 map of flag key to boolean for the caller's environment; 401 no session (MSG-P4-001) | PLT |
| GET /admin/feature-flags | feature-flags.yaml | Query: overdue, owner (the legacy operation names the query `?overdue=true`) | 200 array of FeatureFlag: key, description, ownerTeam, values per environment, removalDate, daysOverdue, version; 401; 403 (MSG-P4-002) | PLT |
| POST /admin/feature-flags | feature-flags.yaml | FeatureFlagRequest: key, description, ownerUserId, ownerTeam, defaultOn, removalDate; `Idempotency-Key` | 201 FeatureFlag; 401; 403 (MSG-P4-002); 409 key exists (MSG-GEN-004); 422 field missing or date in the past (MSG-GEN-001, MSG-GEN-003) | PLT |
| PATCH /admin/feature-flags/{flagKey} | feature-flags.yaml | FeatureFlagChange: environment, value, reason; header If-Match with the version | 200 FeatureFlag; 401; 403 (MSG-P4-002); 404 unknown key (MSG-P2-016); 409 version changed (MSG-GEN-004); 422 reason empty (MSG-GEN-001) | PLT |

The four paths are exactly the four operations of the Ownership Map, at v1 and with no service segment (ASM-2463). rwb-integration serves them against the library; the contract says so explicitly, so no caller assumes a path per service and no service republishes the surface.

**12.2 REST operations consumed**

| Operation | Provider | Why this document needs it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | rwb-case (P3) | The environment codes DEV, SIT, UAT, PROD and the owner-team codes are reference data; the schemas validate against codes, never against a copied list | DP-07, DP-11 |

**12.3 Events published**

None. The contract publishes no event schema: the library emits no business event, and a flag value never travels in an event.

**12.4 Events consumed**

None. A change reaches the other services through the cache refresh of the interface, not through a topic.

**12.5 Workflows and activities**

None. The contract declares no Temporal workflow, no activity and no task queue of its own; the platform library has no service short, and the weekly report is a Schedule (DP-10).

**12.6 Schedules**

| Schedule | When | Overlap policy | Owner | Input and output |
|---|---|---|---|---|
| Flag removal report | Monday 08:00 Asia/Bangkok | SKIP | PLT | Input: active flags whose removal date is before today. Output: one email per owner and one to the RW-PLATADM group, with one MSG-P2-003 log line per flag; the idempotency key is the report date, so a rerun on the same date sends nothing new |

**12.7 Tables owned**

| Table | Key and indexes to publish in the baseline file | Owner | Schema | Rows exposed |
|---|---|---|---|---|
| feature_flag | Primary key flag_key; check constraint on the key pattern `^rwb\.[a-z0-9]+\.[a-z0-9-]+$`; removal_date not null; is_active | PLT | Not specified in the source documents (GAP-1412; ASM-2465) | GET /feature-flags; GET /admin/feature-flags; the weekly report |
| feature_flag_change | Index on flag_key and changed_at; created_by and created_at | PLT | Not specified in the source documents (GAP-1412; ASM-2465) | GET /admin/feature-flags; GET /admin/feature-flags change history |

Both tables are PLT-owned (Ownership Map) and arrive on the per-service Flyway sequence (DP-15; build dependency RWB-PLT-E1044-CON). This document adds no table outside the platform store and no reference to a table of another service (DP-01). The store, its schema name and the deployment of the admin component are Not specified in the source documents (GAP-1412; ASM-2465).

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| Platform library contract fake (this story) | The four documented operations, the success and error examples, the three interface cases and the report input and output | RWB-PLT-E1047-APP, the rwb-integration admin component, the front-end hook and every service that reads a flag |
| ACE audit fake (ACE Common) | The audit write of a flag change | The change examples of this document |
| ACE notification fake (ACE Common) | The weekly email to each owner and to the RW-PLATADM group | The report examples of this document |
| rwb-case reference-data fake (P3) | `GET /api/recovery/case/v1/admin/lists/{listCode}` for the environment and owner-team codes | The schema examples that carry an environment or a team code |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations, at v1 with no service segment | 1 operation (the rwb-case reference-data read) | OpenAPI 3.1, one problem envelope, `Idempotency-Key` on POST, `If-Match` on PATCH, one hop, 2 s timeout |
| Kafka | 0 | 0 | No topic and no event schema; the naming library fixes the topic names of the platform (DP-14) |
| Temporal | 1 Schedule (Flag removal report) | 0 | Declared as a Schedule, not a workflow; overlap SKIP |
| File | 0 | 0 | The report is an email through the ACE notification path, not a file |

### 13. Solution plan

**Hardware and software change.** The contract describes a library that is embedded in every service (Architecture v5 Text Extract v1 slide 20), so the interface is compiled into nineteen deployments while the two tables exist once in the PLT-owned store; P2 rwb-integration serves the HTTP surface against the library under the Ownership Map ruling, so the four paths are published once; the weekly report is a Temporal Schedule on the workflow kit and not a Quartz job (DP-10); and flag values are data, never code, so a value change needs no deployment and no rebuild of any service.

**Deliverables.** `feature-flags.yaml` (OpenAPI 3.1); the client-library declaration of `FeatureFlags`; the report input and output schema; `schema-baseline.sql` (the two tables of section 12, for reference only — the executable migration belongs to the app story and RWB-PLT-DB); the contract fake; the contract test.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The rows are the Template and Rules §R5.5 rows, character for character. Read for this document: DP-01 gives the PLT-owned store, and no service reads another service's tables; DP-07 reads the environment and owner-team codes through the reference-data client library; DP-10 declares the weekly report as a Schedule; DP-11 is the published interface with the fake; DP-14 is the naming library for the `rwb.<module>.<short-name>` flag keys and the topic names; DP-15 is the Flyway sequence of the store; DP-19 is the gateway-bff composite route under which a screen reads a flag. This is a CON story: it documents the patterns and adds no build dependency of its own.

**Build steps**

1. Write `feature-flags.yaml` with the four operations and the FeatureFlag, FeatureFlagChange and request schemas.
2. Add the problem envelope, the `Idempotency-Key` rule on POST, the `If-Match` rule on PATCH and the four legacy message examples.
3. Write the client-library declaration of `FeatureFlags` with the off-by-default rule and the cache interval as a documented chart value.
4. Write the report input and output schemas and the Schedule declaration with overlap SKIP and the report-date idempotency key.
5. Add the lint rules: OpenAPI 3.1 validation, one envelope, no service segment in any path, no personal data in examples, interface and documents at the same version.
6. Write `schema-baseline.sql` from section 12 and cross-check every column against the field identifiers.
7. Generate the fake and the contract test; wire both into the build of this story and into a nightly run against RWB-PLT-E1047-APP.
8. Publish v1 to the contract registry and notify the consumers.

**Done when.** Every document validates, the lint rules pass, the fake answers every operation and every example, and the contract test runs green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | Removal date or change reason empty | Enter {field}. | 422, problem detail with field |
| MSG-GEN-003 | Removal date before today | {field} cannot be before {other}. | 422, problem detail with field |
| MSG-GEN-004 | Version changed between read and write, or a duplicate key | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-GEN-005 | Flag created or changed | Saved. | 200 or 201 success notice |
| MSG-P2-003 | Weekly report, flag past its removal date | Flag {flag} passed its removal date on {date}. Owner: {owner}. Remove the flag and its old code path. | Report line |
| MSG-P2-016 | Change to a key that does not exist | Flag {flag} does not exist. | 404 |
| MSG-P4-002 | A role without the right changes a flag | You cannot {action} here. Your role does not include it. | 403 |

The message IDs and texts are the legacy ones, character for character, and the HTTP status beside each one is fixed by this contract and is the same in the surface that rwb-integration serves. Request validation is published as schema constraints where the value is defined (the key pattern, a required removal date, a non-empty reason, the four environment values) and as the placeholder where it is not (the store schema — GAP-1412; ASM-2465).

### 15. Screens and states

No screen in this story. The documents are read through the gateway-bff composite route when a screen needs a flag (DP-19), and the flag admin screen is SCR-44 of Epic 8, out of scope here. The states the responses expose are the value per environment (off or on) and the retirement state of a flag, each with the HTTP status that produces it: 201 on create, 200 on change, 404 for an unknown key, 409 for a version conflict and 422 for a refused value or date.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1047-CON-01 | AC1 | Contract | feature-flags.yaml validated and linted; FeatureFlag and FeatureFlagChange compared field by field with DF-OPS-207 to DF-OPS-223 and the standard columns |
| TC-PLT-E1047-CON-02 | AC2 | Contract | The `FeatureFlags` declaration; the three interface cases; the cache interval documented as a chart value |
| TC-PLT-E1047-CON-03 | AC3 | Contract | The four paths compared with the Ownership Map; `Idempotency-Key` and `If-Match` present; the problem envelope and the seven legacy message examples |
| TC-PLT-E1047-CON-04 | AC4 | Component | The Schedule declaration, Monday 08:00 Asia/Bangkok, overlap SKIP; the report input and output examples; the report-date idempotency key |
| TC-PLT-E1047-CON-05 | AC5, AC6 | Contract | v1 frozen; a breaking change raises v2 and deprecates v1; the fake run against every operation and example |

### 17. Guardrails

- No business value is embedded in a schema as a constant: the cache interval is published as a chart value (ASM-2464) and the environment values are reference data (DP-07).
- No personal data in examples, events or logs: owners and approvers appear as user IDs and team codes only.
- No cross-schema reference: the documents name the two PLT tables only, and the schema names are not invented (DP-01).
- One hop and 2 s timeout for the consumed reference read; the examples show the failure as a problem detail, never a stale answer.
- The four paths stay exactly as the Ownership Map names them, with no service segment (ASM-2463).
- Every POST carries `Idempotency-Key`, and every PATCH carries `If-Match` with the version.
- The document is Draft until the consumers pass, and it is versioned: a breaking change raises v2 and deprecates v1 rather than editing v1 in place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Configuration changed without a code release | Program 5.7; Epic 1 3.2 | FEAT-CWC-26 | All recovery processes | None | TC-PLT-E1047-CON-01 to TC-PLT-E1047-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1047-APP | App development | H consumer: builds the library, the store and the admin component against this contract and its fake |
| RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | The platform contracts the app story builds on (DP-07, DP-10, DP-15, DP-19); this contract documents the relation and adds no build dependency of its own |
| RWB-P3-E1043-CON | Contract | C: the rwb-case reference-data contract this document consumes |
| RWB-P2-E1007-CON | Contract | The rwb-integration contract that will serve the four paths against the library; named here, not added as a build dependency of this contract |

### 19. Out of scope

- Any implementation, repository, migration or deployment: this story publishes documents and a fake only.
- The store provisioning and its schema name: RWB-PLT-DB and the per-service DB stories.
- The library, the admin component and the report Schedule themselves: RWB-PLT-E1047-APP.
- The service-specific flag reads of the nineteen services and the reference use on the case list queue column.
- The admin screen SCR-44 (Epic 8), the gateway route definition and any event, topic or workflow of the library.
