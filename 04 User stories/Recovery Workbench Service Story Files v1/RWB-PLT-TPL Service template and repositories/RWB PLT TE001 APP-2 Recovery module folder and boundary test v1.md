# RWB-PLT-TE001-APP-2 Recovery module folder and boundary test

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE001-APP-2 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-001 |
| Legacy disposition | Preserved + delta |
| Build status | Built |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP16, DP19, DP20 |
| Parallel lane | L-PLT-TPL-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: delta copy of RWB-TE-001 for the 19 service repositories, one module map per service and the re-pointed boundary rules (Arch v5 slides 20, 29 and 41; DP-01, DP-03, DP-07, DP-08, DP-09, DP-11, DP-13, DP-16, DP-19, DP-20). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **each of the 19 services in its own repository generated from the service template, with one Java package and one `api` and `internal` split per service, a module map kept per service and boundary rules that refuse a cross-schema read, an internal import, a chain, a raw Kafka send and a direct system call**, so that **no service can reach inside another service or around its published contract**.

### 2. Business rationale

The as-built story enforces the module boundaries inside one ACE service: one package tree, one recovery schema, one repository and one module map for all 19 Workbench modules. Arch v5 replaces that monolith with 19 services, each with its own repository, its own schema `rwb_<name>` and its own login (slides 20, 29 and 41), and it keeps the same promise — a build in every repository fails when a boundary is broken. Without the re-pointed rules, the same test that today forbids a cross-module read would pass in a repository that joins another service's schema, that imports another service's internal package, that calls two owner services in one request, that writes a decision record in its own table or that sends a Kafka record from the request thread. ADR-013, ADR-014 and ADR-020 are the decisions of record and DP-01, DP-03, DP-07, DP-08, DP-09, DP-11, DP-13, DP-16, DP-19 and DP-20 are the patterns. It supports REQ-DRI-006. The measure is the count of boundary violations merged to main, which must stay at zero in all 19 repositories.

### 3. Preconditions

- The service template of RWB-PLT-TPL supplies the repository skeleton, the module map loader, the boundary test and the golden pipeline, and the repository and pipeline baseline is in place (RWB-PLT-NF01-OPS).
- The five platform contract stories are available with their fakes: RWB-PLT-E1027-CON (decision-record library), RWB-PLT-E1043-CON (reference data), RWB-PLT-E1037-CON (authorise and guard), RWB-PLT-TE006-CON (outbox and inbox) and RWB-PLT-N001-CON (gateway-bff route).
- The four service contract stories publish the typed clients and fakes this story tests against: RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P2-E1007-CON and RWB-P10-TE013-CON.
- Each of the 19 services has its own schema `rwb_<name>`, its own login and its own repository (Arch v5 slides 29 and 41; ADR-013, ADR-014).
- ADR-020 (contract-first REST, one hop, 2 s timeout) is the decision in force.
- The per-service package map is one Java package per service, `th.co.scb.ace.workbench.recovery.<short without hyphen>`, with one `api` package and one `internal` package inside it. The exact packages inside each repository are Not specified in the source documents (GAP-1429; ASM-2511).
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules section R5.7).

### 4. Flow

1. Squad member: generates the 19 service repositories from the service template, one repository per service, each with the golden pipeline of RWB-PLT-NF01-OPS.
2. Squad member: creates in each repository the one Java package of its service, `th.co.scb.ace.workbench.recovery.<short without hyphen>`, with one `api` package for the published interfaces and one `internal` package for everything else.
3. Squad member: writes the module map of the service in its own repository, listing that service's module codes, packages, published packages and allowed client libraries.
4. Squad member: re-points the boundary rules at the split: no cross-schema read (DP-01), the decision-record library only (DP-03), the outbox and inbox library only (DP-09), the published REST contract or a Temporal activity and never an internal package or a chain (DP-11, DP-13), the shared clients for reference data and authorise (DP-07, DP-08), the integration adapter contract (DP-16), the gateway-bff composite route (DP-19) and the agent client (DP-20).
5. Squad member: writes the front end rule per service: a screen reaches its owner service through the gateway-bff composite route and imports no other service's screen.
6. Pipeline: on each pull request runs the back end boundary test in the unit test phase, the contract tests against the fakes and the front end dependency check.
7. Pipeline: fails the build when a rule is broken and prints the rule, the class and the class, table or path it depends on.
8. Squad member: fixes the call by going through the published contract, an application event through the outbox or a Temporal activity on the owner's queue, and the build passes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A class in one service repository imports the `internal` package of another service | Build fails with the rule and both package names | Build log: boundary rule broken on the internal import | AC3 |
| X2 | A query, view or foreign key in `rwb_<name>` names another service's schema | Build fails with the rule, the object and the other schema | Build log: boundary rule broken on the cross-schema reference | AC2 |
| X3 | A class sends a Kafka record or consumes one without the outbox and inbox library | Build fails | Build log: boundary rule broken on the direct producer or consumer | AC4 |
| X4 | A class writes a decision record in a table of its own instead of the decision-record library | Build fails | Build log: boundary rule broken on the decision record | AC4 |
| X5 | One request calls two owner services in a chain, or the browser calls an owner service directly | Build fails | Build log: boundary rule broken on the call depth | AC3 |
| X6 | A class reads reference data or an authorise answer outside the shared client of its contract | Build fails | Build log: boundary rule broken on the shared client | AC5 |
| X7 | A class opens an SFTP or HTTP client outside the integration adapter contract, or calls the enterprise model endpoint without the agent client | Build fails | Build log: boundary rule broken on the adapter or the agent client | AC5 |
| X8 | A screen calls a service REST base directly instead of the gateway-bff composite route | Front end build fails | Build log: boundary rule broken on the composite route | AC5 |
| X9 | A package is not in the service's own module map | Build fails | Build log: package not in the module map | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the service template and the contract fakes only; it builds no business behaviour |
| Negotiable | The module map content per service is settled per service; the rules and the package pattern are fixed |
| Valuable | Each of the 19 services can change without breaking another, and the boundary is checked in every repository |
| Estimable | One template change, one module map per service, one rule set and its breaking fixtures |
| Small | Fits in one sprint, one service at a time, with its fixtures |
| Testable | Each rule has a breaking fixture that fails the build and a passing fixture that clears it |

### 7. Acceptance criteria

```gherkin
Feature: Recovery module folder and boundary test in 19 service repositories

  Background:
    Given the service template supplies one module map loader, one boundary test and one golden pipeline
    Given each of the 19 services has its own repository, its own schema rwb_<name> and its own login

  Scenario: AC1 19 repositories from one template (new, D-RCV-60)
    Given the service template with the package pattern of section R4 of the template and rules
    When a repository is generated for each of the 19 services
    Then each repository carries one Java package "th.co.scb.ace.workbench.recovery.<short without hyphen>", for example "th.co.scb.ace.workbench.recovery.case" for rwb-case and "th.co.scb.ace.workbench.recovery.sourcedata" for rwb-source-data
    Then each package holds one "api" package and one "internal" package
    Then each repository holds its own module map for its own service only
    Then the build of each repository runs the boundary test and no repository compiles another repository's code

  Scenario: AC2 A service never reads another service's schema (new, D-RCV-60)
    Given a class in "th.co.scb.ace.workbench.recovery.case.internal" with a query that joins "rwb_payment.payment" from schema "rwb_case"
    When the boundary test runs in the build
    Then the build fails with the rule code and both objects named
    When the query holds the payment ID and calls the rwb-payment contract instead
    Then the build passes
    Then no view and no foreign key in "rwb_case" names another schema

  Scenario: AC3 A cross-service call is the published contract, one hop (new, D-RCV-60)
    Given the rwb-payment contract mock returns one payment state
    Given a class in the rwb-case repository that imports an internal class of the rwb-payment package
    When the boundary test runs
    Then the build fails on the internal import
    When the class calls the published REST contract "/api/recovery/payment/v1" through the typed client with the 2 s timeout instead
    Then the build passes
    Then a request that calls two owner services in one chain fails the build

  Scenario: AC4 Decisions and events go through the libraries (new, D-RCV-60)
    Given a class in a service repository that writes an entry to a decision-log table of its own
    When the boundary test runs
    Then the build fails, because a decision is recorded only through the decision-record library and the topic "rwb.decision-record.v1"
    When the class calls the decision-record library instead
    Then the build passes
    Given a class that sends a Kafka record from the request thread without the outbox
    Then the build fails and the record is published only through the outbox and inbox library

  Scenario: AC5 Reference data, authorise, adapters, the edge and the agent (new, D-RCV-60)
    Given the rwb-case contract mock returns one reference-data answer for the reference-data client
    Given the rwb-access contract mock returns an allow answer for the guard library
    Given a class in a service repository that reads a reference-data table of its own
    When the boundary test runs
    Then the build fails and reference data is read only through the RWB-PLT-E1043-CON client
    When the class reads through the client instead
    Then the build passes
    Given a class outside the integration adapter contract that opens an SFTP client
    Then the build fails
    Given a screen that calls a service REST base directly instead of the gateway-bff composite route
    Then the front end build fails
    Given a class that opens its own HTTP client to the enterprise model endpoint instead of the rwb-agent client
    Then the build fails
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each of the 19 services has its own repository, generated from the service template, with one Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>` and one `api` and one `internal` package inside it | Template and Rules section R4; Arch v5 slide 20; ADR-013 |
| BR2 | Each service keeps its own module map in its own repository; a package that is not in the map fails the build | Legacy RWB-TE-001 BR6; Arch v5 slide 29 |
| BR3 | One schema and one login per service; a service never reads another service's schema, and a cross-schema join, view or foreign key fails the build | DP-01; Arch v5 slide 29; ADR-014 |
| BR4 | The decision-record library and the topic `rwb.decision-record.v1` are the only way to record a decision; a local decision-log table is refused | DP-03; ADR-022 |
| BR5 | The outbox and inbox library is the only way to publish or consume an event; a direct producer or consumer fails the build | DP-09; ADR-015 |
| BR6 | A cross-service call is the published REST contract `/api/recovery/<short>/v1` with a fake in the build and one hop in the request, or a Temporal activity on the owner's queue; never an internal package and never a chain | DP-11; DP-13; ADR-020 |
| BR7 | Reference data and authorise answers arrive only through the shared-library clients of RWB-PLT-E1043-CON and RWB-PLT-E1037-CON over the contracts of rwb-case and rwb-access | DP-07; DP-08 |
| BR8 | An outbound file goes only through the rwb-integration adapter contract and the enterprise model endpoint only through the rwb-agent client | DP-16; DP-20 |
| BR9 | A screen reaches a service only through the gateway-bff composite route and no screen imports another service's screen | DP-19; Arch v5 slides 11 and 20 |
| BR10 | Generated code is never edited: the repository skeleton, the module map loader, the boundary test and the pipeline come from the template | RWB-PLT-NF01-OPS; Template and Rules section R6 |

### 9. State transitions

None. This story does not change a case status. It changes the build result of a pull request in one service repository from passed to failed when a boundary rule is broken, and the state of one repository's build has no effect on another repository's build.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Generate the repositories, write the module map and the boundary fixtures of a service |
| TechX tech leads (code owners, RWB-PLT-TE002-APP) | Approve a change to a module map or to the boundary rules |
| ACE team | Names the schema and the login of each service (Arch v5 slide 29) |
| Platform team (PLT) | Owns the service template, the module map loader and the golden pipeline |
| RW-PLATADM, platform administrator | Runs the pipeline of a repository |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

No business field is read or written. The boundary test reads source, compiled classes, the service's own module map and the schema object list of its own schema. It reads no row of any table and no payload of any event.

Field IDs are those in the Logical Data Model and Data Dictionary. No field is added or changed here.

### 12. Contract

#### 12.1 REST operations provided

None. The story provides no REST operation of its own; each of the 19 service REST bases `/api/recovery/<short>/v1` is published by that service's own contract story.

#### 12.2 REST operations consumed

None at runtime. The rules point the generated clients at the published contracts rather than at an internal package: the reference-data client of RWB-PLT-E1043-CON over RWB-P3-E1043-CON (owner P3 rwb-case), the guard library of RWB-PLT-E1037-CON over RWB-P4-E1037-CON (owner P4 rwb-access), the integration adapter contract of RWB-P2-E1007-CON (owner P2 rwb-integration), the agent client of RWB-P10-TE013-CON (owner P10 rwb-agent) and the gateway-bff route of RWB-PLT-N001-CON (owner PLT, the platform team). Those stories publish the operations and payloads; this story adds no path and no payload.

#### 12.3 Events published

None of its own. A service publishes on the topic of its owner, `rwb.<short>.events.v1`, through the outbox library of RWB-PLT-TE006-CON, and it publishes the shared decision record on `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON. The platform story owns neither topic and emits no event.

#### 12.4 Events consumed

None of its own. Each service consumes through its own inbox from RWB-PLT-TE006-CON, in its own consumer group, and this story only refuses a consumer that bypasses it.

#### 12.5 Workflows and activities

None. The rules are build-time checks. A cross-service step allowed by the rules is a Temporal activity on the owner's queue `rwb-<short>`, declared by that owner's contract; this story defines no workflow and no activity.

#### 12.6 Schedules

None. The checks run on every pull request and every build of main; there is no schedule.

#### 12.7 Tables owned

None. The module map is a file in the repository and every business table belongs to one of the 19 services in its own schema; the story creates no schema, no login and no table.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Decision-record library fake of RWB-PLT-E1027-CON | Accepts one decision record and answers the stored record id on `rwb.decision-record.v1` | AC4 fixture and the contract test of every service |
| Outbox and inbox library fake of RWB-PLT-TE006-CON | Accepts one record for `rwb.<short>.events.v1`; answers one inbox delivery as first time or duplicate | AC4 fixture and the contract test of every service |
| Reference-data fake of RWB-PLT-E1043-CON and RWB-P3-E1043-CON | One reference-data answer for one lookup code | AC5 fixture |
| Authorise and guard fake of RWB-PLT-E1037-CON and RWB-P4-E1037-CON | One allow answer and one refuse answer for one capability area and right | AC5 fixture |
| Integration adapter fake of RWB-P2-E1007-CON | One accepted outbound file manifest and one refused manifest | AC5 fixture |
| Agent client fake of RWB-P10-TE013-CON | One completed agent run answer and one fallback answer | AC5 fixture |
| gateway-bff route fake of RWB-PLT-N001-CON | One composite route answering the owner service's published contract | AC5 fixture and the front end rule |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed by this story | The rules keep every call on the published contract of the owner, one hop, 2 s timeout |
| Kafka | None published, none consumed by this story | The rules keep every record on the outbox and inbox library and on the owner's topic |
| Temporal | None | No workflow and no activity of its own; an activity on `rwb-<short>` is only allowed by the rule |
| File | None | No file is read or written except the module map and the sources in the repository |

### 13. Solution plan

**Deliverables.** The repository skeleton of the service template with the one package per service and the `api` and `internal` split, the per-service module map and its loader, the re-pointed boundary rules with one breaking and one passing fixture each, the front end rule per service, and the wiring of both checks into the golden pipeline of RWB-PLT-NF01-OPS.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

**Build steps**

1. Generate the 19 repositories from the service template and prove that each carries one package, one `api` and one `internal` package and its own module map (AC1).
2. Extend the module map loader to the per-service map and add one fixture package that is not in the map (AC1, X9).
3. Re-point rule BND-4 to the schema rule: a join, a view or a foreign key into another `rwb_<name>` fails the build, and the rule reads the schema list of the service's own login (AC2).
4. Add the contract rule: an import of another service's `internal` package, a chain of two owner services and a call from the browser to an owner service fail, and the published contract with its fake passes (AC3).
5. Add the library rules: a direct decision-log write, a direct Kafka producer and a direct consumer fail, and the decision-record library and the outbox and inbox library pass (AC4).
6. Add the shared-client rules: reference data, authorise, the integration adapter, the gateway-bff route and the agent client pass, and every direct read or direct client fails (AC5).
7. Wire both checks into the golden pipeline and confirm that a failing fixture blocks a merge in one repository without touching another repository's build.
8. Prove the pattern on two services (rwb-case and rwb-payment) and then generate the remaining 17 from the same template.

**Done when.** The five test cases of section 16 pass for two services and then for all 19, every repository build runs the boundary test and the front end rule, and no build produces a cross-schema reference, an internal import, a chain, a raw Kafka send, a local decision record or a direct system call.

The per-service module-map file name and the gateway-bff composite route list are Not specified in the source documents (GAP-1430; ASM-2512); the template names the map file at the root of each service repository and takes the route list from RWB-PLT-N001-CON until the point is closed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A boundary rule is broken | Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. |
| Build log | A package is not in the module map | package {package} is not in the module map |
| MSG-P4-002 | A role without the right calls a recovery endpoint | You cannot {action} here. Your role does not include it. |

The two build log lines carry the text of the as-built story unchanged; the code, the class and the dependency named in the text are those of the service that owns the repository. Build log text is for developers and is not part of the message standard.

### 15. Screens and states

No new screen. A developer reads the result in the pull request checks and the build log of the repository. The front end rule adds one state to the build: a screen that calls a service REST base directly, or that imports another service's screen, turns the front end build from passed to failed. SCR-44 is not involved.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE001-APP2-01 | AC1 | Contract | 19 repositories generated from the template; one package, one `api` and one `internal` package, one module map per repository |
| TC-PLT-TE001-APP2-02 | AC2 | Component | Cross-schema fixture in `rwb_case` naming `rwb_payment`; refused, and the contract call passes |
| TC-PLT-TE001-APP2-03 | AC3 | Component | Internal import fixture, published-contract fixture and two-service chain fixture; the chain is refused |
| TC-PLT-TE001-APP2-04 | AC4 | Component | Direct decision-log write and direct Kafka send; both refused, and the library calls pass |
| TC-PLT-TE001-APP2-05 | AC5 | Component | Reference-data, guard, adapter, gateway-bff route and agent client fixtures; each direct use is refused |

The as-built tests of RWB-TE-001 stay in RWB-PLT-TE001-APP section 16 under their legacy test case IDs, and the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code; module names, package names and published packages live in the module map of the service, never in the test (DP-01).
- No personal data in events, workflow inputs or logs; the fixtures hold class, package and schema names only and no payload.
- ACE data only through the owner's contract or the `v_ace_*` views; a service never reads an ACE table, another service's schema or a system of record.
- One schema and one login per service; a cross-schema join, view or foreign key fails the build in every repository (DP-01).
- Contract-first only: the published REST contract with its fake and one hop, or a Temporal activity on the owner's queue; never an internal package and never a chain (DP-11, DP-13).
- Decisions only through the decision-record library and events only through the outbox and inbox library (DP-03, DP-09).
- Generated code is never edited; a change is made in the service template and reaches every repository on regeneration.
- The breaking fixtures stay in `src/test` and never ship.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Boundary test in every repository; no direct client outside the adapter and the agent client | TC-PLT-TE001-APP2-05 |
| DP-01 | Owner's schema `rwb_<name>`; never read another service's tables | Cross-schema join, view and foreign key refused in every build | TC-PLT-TE001-APP2-02 |
| DP-03; DP-09 | Decision-record library and topic `rwb.decision-record.v1`; outbox and inbox library | Only library calls accepted; direct decision-log write, producer and consumer refused | TC-PLT-TE001-APP2-04 |
| DP-11; DP-13 | REST contract with mock, one hop; `/api/recovery/<short>/v1` | Published contract and one hop accepted; internal import and chain refused | TC-PLT-TE001-APP2-03 |
| DP-07; DP-08; DP-16; DP-19; DP-20 | Shared clients for reference data and authorise, the adapter contract, the gateway-bff route and the agent client | Only the contract-backed client accepted; every direct read, client or route refused | TC-PLT-TE001-APP2-05 |
| Arch v5 slide 20 | Every service built from one template and the shared libraries | 19 repositories from one template, one package and one map each | TC-PLT-TE001-APP2-01 |
| Arch v5 slide 29 | 19 schemas, one login each, no cross-schema joins or keys, boundary test in every build | Schema isolation, per-service map and the boundary test in the golden pipeline | TC-PLT-TE001-APP2-01, TC-PLT-TE001-APP2-02 |

### 19. Out of scope

- The as-built monolith module folder and its boundary test, kept word for word in RWB-PLT-TE001-APP.
- The per-service contract stories and their published operations, payloads and fakes: RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P2-E1007-CON and RWB-P10-TE013-CON, and the platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON.
- The repository and pipeline baseline of the platform (RWB-PLT-NF01-OPS) and the pipeline template and Helm chart (RWB-PLT-N004-OPS).
- The quality gates baseline (RWB-PLT-NF05-OPS).
- The business code of each service and its own module list, which each service epic delivers in its own repository.
- The schemas, logins and grants of the 19 services (Arch v5 slide 29; ADR-014).
