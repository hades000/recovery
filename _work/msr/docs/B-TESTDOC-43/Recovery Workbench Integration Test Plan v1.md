SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Integration test plan

| Item | Detail |
|---|---|
| Document | Recovery Workbench integration test plan |
| Version | 1 |
| Date | 22 November 2026 |
| Supersedes | None (first version) |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119-3 test plan, aligned to the test strategy version 3 |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

This plan is the integration test plan of the Recovery Workbench in its target shape: 19 services inside ACE, each with one schema rwb_<name>, one login, one REST base /api/recovery/<short>/v1, one Kafka topic rwb.<short>.events.v1 and one Temporal task queue rwb-<short> (Architecture v5 slide 41; ADR-013, ADR-014, ADR-015, ADR-016). It states what is tested when two or more services meet, on which data, against which contract, under which gate, and with which evidence. It is the companion of the test strategy version 3, which fixes the levels, the environments, the entry and exit gates and the defect process, and of the non-functional test plan version 3, which fixes the non-functional tests and their pass marks. Where those two documents already state a rule, this plan cites it and does not restate the target.

The plan is new. The Workbench document set of 22 November 2026 holds no integration test plan for the monolith, and the folder 09 Testing and quality holds no earlier file of this family, so this is version 1 with no source to carry forward: no section, identifier, number or date of a predecessor is kept, because there is none (CG-B-TESTDOC-43-1; ASM-B-TESTDOC-43-1). Its content is read from the sources the work package names: the Recovery Workbench Microservice Story Template and Rules v1 (sections R1, R3, R4, R5 and R9), the Microservice Ownership Map v1, the Architecture v5 text extract, the Temporal and Drools design text extract, the split plan and the story files of the five integration epics.

The plan is written for the integration level only. Unit, rule-table, service component, system, regression, accessibility and user acceptance tests are owned by the test strategy version 3 sections 1 to 7 and by the non-functional test plan version 3, and are not repeated here. Where this plan names a service test case, it names the test case that the story of the integration epic already holds, so the two plans point at one artefact and not at two.

No approval of this version is recorded, so the document is issued as Draft (ASM-B-TESTDOC-43-11). Every release date is copied unchanged from the plan and marked tentative (R1 U7; ASM-B-TESTDOC-43-12).

# 1. Purpose and scope

The purpose of the plan is to fix how the real cross-service behaviour of the Recovery Workbench is proven, wave by wave, and what evidence closes an integration gate. The Workbench sells a set of contracts: a screen reads a case through rwb-case, a case workflow calls an activity on another owner's task queue, and an event leaves one schema and enters another. None of those edges is proven by the service that owns one end of it, so each wave carries its own integration test group, its own journey and its own gate (test strategy version 3, section 10).

In scope:

- The contract tests of the five call types of Architecture v5 slide 11: REST, Kafka event, Temporal activity and workflow, File and SQL view.
- The component tests in which one service runs against the published fake of every contract it consumes.
- The four wave journeys RWB-ITG-W1J02-ITG, RWB-ITG-W2J01-ITG, RWB-ITG-W3J01-ITG and RWB-ITG-W4J01-ITG, and the integration test cases of the service stories of each wave.
- The non-functional integration evidence that the non-functional test plan version 3 assigns to a wave and a journey, and the two non-functional integration stories RWB-ITG-TE009-ITG and RWB-ITG-TE010-ITG.
- The harness RWB-ITG-W1J01-ITG, which gates every build and supplies the synthetic fixture set every wave suite starts from.
- The wave gates RWB-ITG-W1 to RWB-ITG-W4 and RWB-ITG-NFR.

Out of scope: unit and rule-table tests, the service-level system tests, the regression suite, user acceptance, screen design, production monitoring and the service stories' own acceptance criteria. The plan tests the published contracts and the journeys across them; it changes no contract and no story.

# 2. Test basis and precedence

The sources of this plan, in the precedence order of Template and Rules section R3:

| Rank | Source | What the plan takes from it |
|---|---|---|
| 1 | Architecture v5 catalogue slides (13 to 20 and 41 to 44) | The 19 services, their schemas, REST bases, topics, task queues and waves; the five call types; the event and job catalogues |
| 2 | Recovery Temporal and Drools Detailed Design v1 | Workflow, activity, replay and rule-package behaviour asserted at the integration level |
| 3 | Architecture v5 narrative slides | The contract-first rule, the outbox and inbox, the edge, the journey smoke |
| 4 | Decision Log, latest version | D-RCV-60 and the DL44 to DL49 rows |
| 5 | Architecture Decision Records, latest version | ADR-013 to ADR-023 |
| 6 | Technical Specifications by Module, latest version | The per-service interfaces the contract tests pin |
| 7 | Functional Specifications by Module, latest version | The behaviour the journeys assert at each hop |
| 8 | Physical Schema and Logical Data Model, latest version | Table ownership, used only to read the Ownership Map |
| 9 | The story masters | The test cases this plan schedules |

The Ownership Map v1 is the single source of every owner in this plan (Template and Rules section R3 default rulings). A table, a REST operation, an event, a workflow or a job is tested against the service code the map assigns it, and that code is written next to every element this plan names. No owner in this plan is read from a story title or from a module name.

# 3. Services and waves under integration test

The programme delivers in four waves. The wave of a service is the wave of Architecture v5 slide 41 and of the Ownership Map v1 sheet Services. Nine services exist in wave 1, four more in wave 2, four more in wave 3 and the last two in wave 4 (Template and Rules section R4).

| Wave | Integration epic | Services under test | Business epics | Journey story | Release (tentative) |
|---|---|---|---|---|---|
| 1 | RWB-ITG-W1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 (9 services) | EP01 | RWB-ITG-W1J02-ITG | 30 November 2026 (tentative) |
| 2 | RWB-ITG-W2 | Wave 1 plus P8, S2, S5, S8 (13 services) | EP02, EP03 | RWB-ITG-W2J01-ITG | 31 December 2026 and 31 January 2027 (tentative) |
| 3 | RWB-ITG-W3 | Wave 2 plus S1, S3, S4, S6 (17 services) | EP04, EP05 | RWB-ITG-W3J01-ITG | 28 February 2027 and 31 March 2027 (tentative) |
| 4 | RWB-ITG-W4 | Wave 3 plus S7, S9 (19 services) | EP06, EP07, EP08 | RWB-ITG-W4J01-ITG | 30 April 2027, 31 May 2027 and 30 June 2027 (tentative) |
| 0 and every wave | RWB-ITG-NFR | Every service in the wave, plus the platform | NF | RWB-ITG-TE009-ITG, RWB-ITG-TE010-ITG | Same dates as the wave under test (tentative) |

The business epic of a story fixes its wave under the wave map of Template and Rules section R5.6: EP01 is wave 1, EP02 and EP03 are wave 2, EP04 and EP05 are wave 3, EP06, EP07 and EP08 are wave 4, and the platform and non-functional work is wave 0. Where a story's wave map wave is earlier than its service's Architecture v5 wave, the story keeps the wave map wave and the conflict is raised once per service and business epic in the story set. The plan reads the wave of a test from the same rule, so a wave journey always tests the services that exist in its wave and no service that arrives later, except through a published fake.

The 19 services, with the element names the contract tests pin (Ownership Map v1 sheet Services; Template and Rules section R4):

| Code | Service | Wave | Schema | REST base | Topic | Task queue |
|---|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data |
| P2 | rwb-integration | 1 | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration |
| P3 | rwb-case | 1 | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case |
| P4 | rwb-access | 1 | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access |
| P5 | rwb-document | 1 | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document |
| P6 | rwb-comms | 1 | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms |
| P7 | rwb-decision | 1 | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision |
| P8 | rwb-payment | 2 | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment |
| P9 | rwb-reporting | 1 | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting |
| P10 | rwb-agent | 1 | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent |
| S1 | rwb-valuation | 3 | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation |
| S2 | rwb-treatment | 2 | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment |
| S3 | rwb-guarantee | 3 | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee |
| S4 | rwb-litigation | 3 | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation |
| S5 | rwb-asset | 2 | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset |
| S6 | rwb-debtsale | 3 | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale |
| S7 | rwb-writeoff | 4 | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff |
| S8 | rwb-deviation | 2 | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation |
| S9 | rwb-partner | 4 | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner |

The shared topic rwb.decision-record.v1, the Temporal namespace rwb-recovery and the two edges (gateway-bff with its session store, and the partner gateway in the DMZ) complete the picture (Template and Rules section R4; Architecture v5 slide 11).

# 4. The levels inside this plan

Four test levels belong to this plan. They run in this order, and each one answers a question the next cannot.

| Level | The question it answers | Real | Fake | Where | Evidence |
|---|---|---|---|---|---|
| Contract | Does every published contract still hold its shape | The published OpenAPI 3.1, AsyncAPI 3.0 and contract jars | Nothing; the contract is the object under test | The pipeline of the owner and of every consumer | One report line per checked element, with its contract version |
| Component with fakes | Does one service behave against the contracts it consumes | The service, its own schema, its own topic, its own task queue | The published fake of every contract it consumes | The pipeline | No call leaves the service; the boundary test finds no cross-schema reference |
| Integration test group of a wave | Do the real services of the wave behave together | Every service of the wave on its real schema, topic and queue | No fake between two services of the wave | SIT | The journey trace and the wave's integration test cases |
| Non-functional integration | Does the wave hold its targets under load and on the bank's browsers | The services of the wave at the SIT volume | Screens measured through gateway-bff | SIT | The load report and the accessibility report |

A contract test is not a substitute for a journey, and a journey is not a substitute for a load test. The contract fixes one edge; the component fixes one service against its edges; the journey fixes the whole chain of one wave; the non-functional test fixes the behaviour of that chain under its target load.

The dependency classes of Template and Rules section R5.4 fix where a real call is allowed to appear. A C dependency is built and tested against a published contract and its fake, so no test of this plan waits for another service's build. An I dependency is the real cross-service behaviour, and it is allowed on an integration story only. This is why the real journey exists only at the integration level: it is the one level at which an I dependency is legal.

# 5. The contract-test harness RWB-ITG-W1J01-ITG

The harness is the integration epic's Day-1 story. It is a test project outside the 19 services that checks every published OpenAPI 3.1 document, every AsyncAPI 3.0 document and every activity and workflow contract jar, replays recorded Temporal histories, proves the Kafka and PostgreSQL round trip and the per-schema boundary on Testcontainers, and generates, loads and resets one synthetic test data set through the owners' published operations in the DEV sandbox (RWB-ITG-W1J01-ITG, sections 1, 4 and 12).

| What the harness checks | How | Test case |
|---|---|---|
| Every operation against its OpenAPI 3.1 document | Path, method, request and response schema, status codes and RFC 9457 problem details, with the contract version recorded | TC-W1J01-01-ITG |
| Every event against its AsyncAPI 3.0 document and JSON Schema | CloudEvents 1.0 binary envelope, key caseId, identifiers and facts only, no personal data, BACKWARD compatibility | TC-W1J01-02-ITG |
| Every activity and workflow contract, and five recorded histories | Contract-jar comparison against the implementation, then a replay compared decision by decision | TC-W1J01-03-ITG |
| The Kafka and PostgreSQL round trip, and the schema boundary | Outbox to topic to inbox with a duplicate delivery, then a cross-schema scan | TC-W1J01-04-ITG |
| The deterministic synthetic set | Two generations from the same seed and business date compared key for key | TC-W1J01-05-ITG |
| The load and reset through owner operations only | Owner operations for every class, an idempotent repeat load and a complete reset | TC-W1J01-06-ITG, TC-W1J01-07-ITG, TC-W1J01-08-ITG |
| The build gate and the stub set | One red check fails the build; one WireMock stub per service per wave from its pinned contract | TC-W1J01-09-ITG, TC-W1J01-10-ITG |

Two properties of the harness matter to this plan. First, the harness is extended wave by wave rather than rebuilt: the contracts of the wave under test are pinned, and one stub is generated per service of that wave. The test strategy version 3 section 10 states that the harness serves all four waves, while the story scopes its criteria to the wave 1 services; the plan reads the story as the wave 1 increment of one harness that each later wave extends (CG-B-TESTDOC-43-9; ASM-B-TESTDOC-43-9). Second, a stub pass is never reported as a real-owner pass: the report names the contract version and whether the hop was served by a stub or by the owner, and a skipped hop is not green.

# 6. Component tests against published fakes

A component test runs one service with everything outside it replaced by the published fake of the contract it consumes. It is the level that lets a lane start on Day 1, because the contract and its fake exist before the downstream service does (Template and Rules section R5.7 rule 2; ADR-020).

| In a component test | Real | Fake | What the test proves |
|---|---|---|---|
| Data | The service's own schema rwb_* on Testcontainers PostgreSQL, with its own login and its own Flyway sequence | Every other schema | The service reads and writes only its own schema, and the boundary test fails the build on any cross-schema reference (ADR-014, ADR-021; DP-01) |
| Events | Its own topic, consumer group, outbox relay and inbox | Every producer and consumer outside the service | The outbox row is written in the same transaction as the state change, the inbox drops a duplicate, and a failure reaches the retry topics and the dead-letter topic (ADR-015; DP-09) |
| Workflow | The Temporal test server and the workflow kit | An activity of another service | The workflow is deterministic and replays; it holds no database call, clock, random, network call or rule call |
| Rules | Embedded Drools and the rule package | The rule registry of rwb-decision | The answer names the rule and the package version, is returned inside the target, and a refused package leaves the last good version running (ADR-017; DP-04) |
| Downstream calls | The code under test | The fake named in section 12.8 of the story | The call, the timeout, the problem details and the retry match the published contract, and no call leaves the service |

Three assertions are made in every component test of a service that takes a decision. The decision record, the state change and the outbox row are one transaction, so a failed decision-record write moves nothing. An activity that finds no rule package in force fails at once with no retry, and the stuck-workflow scan JOB-21 raises it. An agent answer that is late is abandoned after 60 seconds and the rule result is used (NFR-010, NFR-024).

# 7. Contract tests by call type

Every service publishes its contracts before code, and the contract tests run in every build (Architecture v5 slide 11; ADR-020). The five call types and what the integration plan proves on each:

| Call type | Contract under test | What the test proves | Owner |
|---|---|---|---|
| REST | OpenAPI 3.1 with /v1 in the path | Every operation and status code; RFC 9457 problem details on failure; Idempotency-Key on every POST; a 2 second timeout with one retry on GET only, plus breaker and bulkhead on the caller; one hop, never a chain | The service the Ownership Map v1 assigns the operation (sheet Endpoints) |
| Kafka event | AsyncAPI 3.0 and the JSON Schema registry, BACKWARD compatibility | The CloudEvents 1.0 envelope in binary mode; key caseId and order per case; identifiers and facts only, no personal data; a payload that passes the previous schema version; dedupe by the inbox; retry topics at 1 minute, 10 minutes and 1 hour, then the dead-letter topic with an alert | The producer the Ownership Map v1 assigns the event (sheet Events) |
| Temporal | The activity and workflow interface in the contract jar | Every activity and workflow signature and typed failure the caller uses; the caller imports the interface only and calls the owner's task queue; the workflow identifier is the business key; a recorded history replays to the same decisions | The service the Ownership Map v1 assigns the workflow (sheet Workflows and activities) |
| File | The manifest: fileId, batchId, sha256 and record count | The manifest fields, the checksum on receipt, a 15 minute SAS link, and that a re-delivery is safe; the data stays out of the message | P2 rwb-integration, and the party that receives the file |
| SQL view | The 30 recovery.v_ace_* views | The read-only login reads the 30 views; no service other than P1 reads them; the 5 second statement timeout holds | P1 rwb-source-data |

The scope of the contract tests of a service is the set of contracts the Ownership Map v1 assigns it: across the 20 owner rows of the map the tests cover 93 tables, 156 REST operations, 30 events, 15 workflows and 22 jobs (Ownership Map v1 sheets Tables, Endpoints, Events, Workflows and activities, Jobs; test strategy version 3 section 11). A zero in one column is not a gap: P1 rwb-source-data owns no workflow and is called as an activity by other owners, so its interface is tested through the contract jar and not through a workflow of its own.

# 8. The wave journeys

Each wave carries one journey story that chains the wave's business behaviour for one business date and one seeded case or portfolio, asserts each hop through the owner's published contract, composes through gateway-bff where a screen would compose, and records one trace per run. The journeys are new under D-RCV-60 and carry no legacy test case; the legacy integration copies stay with the service stories of the wave (Template and Rules section R7.2 section 16).

## 8.1 Wave 1 journey RWB-ITG-W1J02-ITG

The chain of EP01 on business date 2026-11-25, in this order:

| Hop | Owner | Call type | What the journey asserts |
|---|---|---|---|
| 1 | P1 rwb-source-data | REST and event | The seeded set and the readiness of the business date; AceDataReady opens the day |
| 2 | P3 rwb-case | REST | The case, its accounts, its queue and its owner are created and read back |
| 3 | P5 rwb-document | REST and event | A document is posted, its OCR, classification and extraction complete, and it attaches itself to the case automatically |
| 4 | P3 rwb-case | REST and event | The document-received transfer of the case completes with its reason code |
| 5 | P7 rwb-decision | Kafka event | Every hop that took a decision writes one decision record, in the same transaction as its state change |
| 6 | P10 rwb-agent | REST and event | The case intake agent runs in SHADOW, recommends and moves nothing |
| 7 | P6 rwb-comms | REST and event | The demand notice leaves on an approved template and carries its document reference |
| 8 | P2 rwb-integration | File | The 16:00 WIN file of the business date is built once, with its manifest and checksum |
| 9 | P9 rwb-reporting | REST | The 01:30 measures of the same business date are published from the same facts |
| 10 | P1 rwb-source-data | REST | The interaction ledger holds one entry per hop, in order |
| 11 | P4 rwb-access | REST | Every call is authorised, and a role without the right is refused with the fields masked |

The journey's test cases are TC-W1J02-01-ITG to TC-W1J02-11-ITG, and they cover the chain, one owner per hop, the 2 second budget, the decision-record transaction, the authorisation refusal, the stale data product and the repeat run (RWB-ITG-W1J02-ITG, section 16).

## 8.2 Wave 2 journey RWB-ITG-W2J01-ITG

The chain of EP02 and EP03 on business date 2026-12-15, in this order:

| Hop | Owner | Call type | What the journey asserts |
|---|---|---|---|
| 1 | P3 rwb-case and P7 rwb-decision | REST and event | Case entry and route, with the decision record of the route |
| 2 | P8 rwb-payment | REST and event | A payment is matched to the case and its clearance is confirmed |
| 3 | S2 rwb-treatment | REST and event | The settlement or TDR treatment is approved and booked |
| 4 | P2 rwb-integration | File | The collateral release instruction reaches CCMS and the case sits at COLLATERAL_RELEASE_REQUESTED |
| 5 | S5 rwb-asset | REST and event | The asset is taken on and held |
| 6 | S5 rwb-asset and P2 rwb-integration | REST, Temporal and file | The monthly re-appraisal falls due and the order leaves to SVAF on JOB-19 |
| 7 | S8 rwb-deviation | REST and event | A deviation is raised, the stage clock pauses and the prescription clock keeps running |
| 8 | P3 rwb-case | REST and event | The case closes or is sold |
| 9 | P1 rwb-source-data, P7 rwb-decision and P4 rwb-access | REST | The ledger is read through P1, every decision record reaches P7, and every call is authorised |

The journey's test cases are TC-W2J01-01-ITG to TC-W2J01-10-ITG (RWB-ITG-W2J01-ITG, section 16).

## 8.3 Wave 3 journey RWB-ITG-W3J01-ITG

The chain of EP04 and EP05 on business date 2026-12-14, in this order:

| Hop | Owner | Call type | What the journey asserts |
|---|---|---|---|
| 1 | S1 rwb-valuation and P2 rwb-integration | REST, Temporal and file | An appraisal is ordered when the last one is older than the limit, and the order leaves to SVAF |
| 2 | S1 rwb-valuation | REST and event | The appraisal value received into ACE is accepted and the route is decided |
| 3 | P8 rwb-payment | REST | Fees and charges are worked out from the fee tables held as data |
| 4 | P1 rwb-source-data | REST | The money movements of the business date reconcile against the ACE payment and write-off rows, with the outcome by rec_code |
| 5 | P8 rwb-payment | REST and event | The settlement booking is posted and the general ledger posting follows |
| 6 | S3 rwb-guarantee | REST and event | The guarantee claim is made and reaches its state |
| 7 | P6 rwb-comms | REST and event | The notice is dispatched and its proof of delivery is recorded |
| 8 | S9 rwb-partner and P2 rwb-integration | REST and file | The instruction to the firm is issued and its result is received |

The journey's test cases are TC-W3J01-01-ITG to TC-W3J01-10-ITG (RWB-ITG-W3J01-ITG, section 16).

The wave 3 journey names S9 rwb-partner at its last hop, while the Ownership Map v1 and Template and Rules section R4 place S9 in wave 4. In wave 3 the hop is therefore proven against the published contract of S9 served by its fake, and the real-owner hop is proven in the wave 4 journey, which chains a partner instruction, its recorded result and the partner review (CG-B-TESTDOC-43-10; ASM-B-TESTDOC-43-10).

## 8.4 Wave 4 journey RWB-ITG-W4J01-ITG

The chain of EP06, EP07 and EP08 on business date 2027-04-30, in this order:

| Hop | Owner | Call type | What the journey asserts |
|---|---|---|---|
| 1 | S6 rwb-debtsale | REST and event | The lot is awarded, the accounts transfer, and derecognition and the general ledger posting follow |
| 2 | S7 rwb-writeoff | REST and event | The monthly scan runs, the population routes to the committee, the write-off is posted with its provision release, and the completeness check agrees |
| 3 | S9 rwb-partner | REST and event | The instruction is issued, the result is recorded, the fee is claimed and the partner review is held |
| 4 | S8 rwb-deviation | REST and event | A deviation of code X5 holds the case out of the population, pauses the stage clock and returns the case |
| 5 | S7 rwb-writeoff | REST and event | The case closes after its retention period |
| 6 | P3, P1, P7 and P4 | REST and event | The hardening controls that only a whole journey can prove: the case state, the ledger, the decision records and the authorisation answer of every hop |

The journey's test cases are TC-W4J01-01-ITG to TC-W4J01-14-ITG (RWB-ITG-W4J01-ITG, section 16).

Every journey obeys the same five rules. It uses the real contract of every service of its wave and no fake between them. It runs on the synthetic fixture set of RWB-ITG-W1J01-ITG in the DEV sandbox for a component run, and on the masked SIT data set for the wave run. It never sets a case, document, notice, file, measure or decision state by hand. It reproduces its own report when it is run twice on the same business date. And it fails on a second business effect, a duplicate ledger entry or a duplicate decision record, because a repeat of one run must leave one effect.

# 9. Non-functional integration

The non-functional side of a wave gate is owned by the non-functional test plan version 3 and by the two integration stories of the epic RWB-ITG-NFR. This plan schedules that evidence into the wave gate and does not repeat the pass marks.

| Element | Story or plan | What it contributes to the gate |
|---|---|---|
| Performance test harness | RWB-ITG-TE009-ITG | The busiest-hour load of a screen through gateway-bff on the per-service bases, with 410 virtual users at 3 requests a minute, and a release stop when a target is missed (NFR-002, NFR-003, NFR-008) |
| Browser and accessibility tests | RWB-ITG-TE010-ITG | The six main screens on four browser configurations in Thai and English, with a WCAG 2.1 AA scan and a keyboard-only check (NFR-059, NFR-060, NFR-061) |
| Journey non-functional tests | Non-functional test plan version 3, NFT-J-01 to NFT-J-12 | The non-functional behaviour of the journey of each wave, mapped to the NFR identifiers it proves |
| Platform non-functional tests | Non-functional test plan version 3, NFT-PLT-01 to NFT-PLT-08 | The edge, the event platform, the Temporal platform, the schemas and logins, observability, the pipeline, availability and restore |
| Per-service non-functional tests | Non-functional test plan version 3, sections 6.1 to 6.5 | The four test rows of every service of the wave |

The wave assignment of the non-functional tests is the one the non-functional test plan version 3 fixes: wave 1 takes NFT-J-01, NFT-J-09 and NFT-J-12; wave 2 takes NFT-J-03, NFT-J-06 and NFT-J-11; wave 3 takes NFT-J-02, NFT-J-04, NFT-J-05 and NFT-J-07; wave 4 takes NFT-J-08 and NFT-J-10. A wave gate does not close until the non-functional evidence assigned to that wave is green.

Which NFR identifiers are proven at the integration level rather than at the system level is not stated in any source read for this plan. The plan takes the integration evidence to be the two RWB-ITG-NFR stories, the NFT-J rows and the NFR level test cases of the wave journeys, and leaves every other identifier to the per-service and system tests of the non-functional test plan (CG-B-TESTDOC-43-7; ASM-B-TESTDOC-43-7).

# 10. Environments and test data

| Environment | Data | What runs there |
|---|---|---|
| The DEV sandbox | Synthetic only, generated from a seed and a business date | The contract harness, the component tests, the stub set and the fixture load and reset |
| SIT | Masked copies from the PII service at the target volume | The wave journeys, the integration test cases of the wave, the non-functional tests and the regression suite |
| UAT | Masked copies | The business acceptance scripts, outside this plan |

The DEV sandbox is the sandbox of RWB-E1-065 with the ACE schema, the ACE views and synthetic recovery data, the 19 schemas and the 19 logins. The fixture set is generated by RWB-ITG-W1J01-ITG and loaded only through the owners' published operations, never by writing a schema. The seed, the business date, the volumes and the identifiers of the set are Not specified in the source documents (CG-B-TESTDOC-43-4; ASM-B-TESTDOC-43-4); under the assumption they follow the fixtures the wave stories already name, and every value is synthetic.

In SIT each service of the wave under test runs with its own schema, login, REST base, topic and task queue. A service of a later wave is not deployed yet; until it is, its published contract is served by its fake, and the journey report names every hop that was a stub. How SIT is composed across waves is not stated in any source read for this plan (CG-B-TESTDOC-43-6; ASM-B-TESTDOC-43-6).

Four data rules hold on every test of this plan. No production data is used below production (NFR-045). No personal data is placed in an event, a workflow input, a log or a report (Template and Rules section R7.2 section 17). A test seeds its own schema or a fake, never another service's tables. A reset is part of every harness run, so no suite starts on a mixed estate.

The business date of each journey is the one its story names: 2026-11-25 for wave 1, 2026-12-15 for wave 2, 2026-12-14 for wave 3 and 2027-04-30 for wave 4. Those dates are test data and not a programme calendar, and they do not move a release date (ASM-B-TESTDOC-43-12).

# 11. Entry and exit criteria

| Gate | Entry | Exit |
|---|---|---|
| ITG-W1 | The nine wave 1 services deployed in SIT; every wave 1 contract pinned; RWB-ITG-W1J01-ITG done; the synthetic set loaded | Every wave 1 journey test case passes; no open severity 1 or 2 defect; the non-functional evidence of wave 1 green |
| ITG-W2 | Wave 1 exit met; P8, S2, S5 and S8 deployed; their contracts pinned; the harness extended to the wave 2 contracts | Every wave 2 journey test case passes; no open severity 1 or 2 defect; the non-functional evidence of wave 2 green |
| ITG-W3 | Wave 2 exit met; S1, S3, S4 and S6 deployed; their contracts pinned; the harness extended to the wave 3 contracts | Every wave 3 journey test case passes; no open severity 1 or 2 defect; the non-functional evidence of wave 3 green |
| ITG-W4 | Wave 3 exit met; S7 and S9 deployed; their contracts pinned; the harness extended to the wave 4 contracts | Every wave 4 journey test case passes; no open severity 1 or 2 defect; the non-functional evidence of wave 4 green |
| ITG-NFR | The wave under test deployed; the load mix and the browser matrix configured | Every assigned NFT row green; no accessibility exception without an owner and an expiry date |

The exit wording is the SIT exit of the test strategy version 3 section 3; no source states a separate integration threshold, so the plan adopts that wording and does not invent a pass rate (CG-B-TESTDOC-43-2; ASM-B-TESTDOC-43-2).

Three further conditions are conditions of entry, not of exit. A contract that is not published and pinned is a red check on Day 1 and not a reason to wait. A journey whose fixture class is missing fails as a fixture fault and substitutes no value. A hop served by a stub is reported as a stub and never counted as a real-owner pass.

The number and the calendar of integration test cycles per wave are not stated in any source read for this plan (CG-B-TESTDOC-43-3; ASM-B-TESTDOC-43-3). The plan therefore fixes one cycle per wave that closes the gate before the wave's first release date, and asserts no window beyond that. A wave gate never moves a release date.

Who signs a wave gate is not stated in any source read for this plan (CG-B-TESTDOC-43-8; ASM-B-TESTDOC-43-8). The plan records the gate as signed by the QA lead with the integration lead, on the report of the harness and of the journey, and names roles only.

# 12. Sequence, dependencies and Day 1

The plan follows the dependency classes and the Day-1 rules of Template and Rules sections R5.4 and R5.7.

| Rule | What it means for the plan |
|---|---|
| A CON story has no build dependency and is Day 1 | The contract and its fake exist before the code that uses them, so the contract test and the stub of a service are available on Day 1 |
| An APP story builds against CON stories and their fakes | A component test is green against a published contract before the downstream service exists, and a C dependency never blocks the schedule |
| An H dependency points only to the same service or to a platform contract | A lane's tests run in the order of the lane, and no test of a lane waits on another service's build |
| An I dependency sits only on an ITG story | The real cross-service behaviour is tested at the integration level and nowhere else |
| The harness and the journeys are Day-1 work for the QA team | RWB-ITG-W1J01-ITG and the four journey stories need no build dependency; the contracts and the fixture classes are enough to start |

The execution order of a wave is therefore: the contract tests of every service of the wave in every build; the component tests of the wave in every pull request; the harness extension and the fixture load before the first journey run; the wave journeys and the integration test cases of the wave in SIT; and the non-functional evidence of the wave on the same SIT estate. The daily journey smoke JOB-22 at 06:00 keeps the chain under observation between waves (Architecture v5 slide 44), so a broken journey is seen the next morning and not at the end of a wave.

Programme release dates are unchanged and tentative (R1 U7; ASM-B-TESTDOC-43-12). A gate decides whether the wave's journeys can be signed off; it never changes a date.

# 13. Test case inventory

The five integration epics hold 147 stories. Section 16 of those stories holds 1,416 test case identifiers, by level as follows.

| Epic | Stories | Contract | Component | Integration | End to end | NFR | Total |
|---|---|---|---|---|---|---|---|
| RWB-ITG-W1 | 52 | 34 | 35 | 543 | 43 | 32 | 687 |
| RWB-ITG-W2 | 43 | 0 | 47 | 400 | 2 | 29 | 478 |
| RWB-ITG-W3 | 9 | 0 | 11 | 24 | 2 | 9 | 46 |
| RWB-ITG-W4 | 41 | 0 | 45 | 115 | 30 | 1 | 191 |
| RWB-ITG-NFR | 2 | 0 | 6 | 3 | 1 | 4 | 14 |
| Total | 147 | 34 | 144 | 1,085 | 78 | 75 | 1,416 |

The identifier families this plan schedules directly are the harness and journey families: TC-W1J01-01-ITG to TC-W1J01-10-ITG, TC-W1J02-01-ITG to TC-W1J02-11-ITG, TC-W2J01-01-ITG to TC-W2J01-10-ITG, TC-W3J01-01-ITG to TC-W3J01-10-ITG, TC-W4J01-01-ITG to TC-W4J01-14-ITG, TC-ITG-TE009-ITG-01 to TC-ITG-TE009-ITG-06 and TC-ITG-TE010-ITG-01 to TC-ITG-TE010-ITG-08. Every other identifier of the table belongs to the story that holds it, is executed by its owner, and is cited here only so the wave gate can be read against one count.

The full text of a test, with its Given, When and Then, is held under the same identifier in the pack of its story. The packs of the journeys and the harness, their environments and their evidence format are Not specified in the source documents (CG-B-TESTDOC-43-5; ASM-B-TESTDOC-43-5).

# 14. Defects, evidence and reporting

Defects follow the defect management process: severity, owner, fix and retest. A wave gate closes with no open severity 1 or 2 defect, and no journey is signed off on a waiver.

A defect that a wave journey raises names the owning service from the Ownership Map v1 and the contract it breaks, so a defect that crosses two services is routed to the owner of the contract and not to the caller. A defect that a contract test finds in the owner's build is fixed before the contract is published. A defect that a consumer's component test finds against a published contract is a contract defect and is raised with the owner. This keeps one rule: the owner of the contract owns the fix, whatever service noticed the break.

The evidence a gate reads is the harness report keyed by build, with one line per checked element naming the owner, the element, the contract version and the result; the journey report keyed by story and business date, with one trace per run and the contract version of every hop; the load and accessibility reports of RWB-ITG-NFR; and the defect list at the gate date. How long that evidence is kept is not stated in any source read for this plan (CG-B-TESTDOC-43-5; ASM-B-TESTDOC-43-5); the plan keeps it with the build and beyond the gate that reads it.

# 15. Roles and ownership

| Role or owner | What they own in this plan |
|---|---|
| QA lead | The harness and journey definition, the fixture seed and business date as configuration, the wave gate report and the gate signature |
| QA integration engineer | The harness code, the contract probes, the replay runner, the container tests and the stub publisher |
| Integration lead | The contract pinning per build, the swap of a stub for a real owner, and the gate signature with the QA lead |
| Contract owner, per service | The contract tests of the tables, REST operations, events, workflows and jobs the Ownership Map v1 assigns to that service, and the fakes it publishes |
| Service owner, per service | The behaviour that a red hop or a red journey names |
| Platform administrator | The harness stage and the pipeline block of NFR-054 |
| Compliance and PDPA officer | The rule that the development set is synthetic (NFR-045) and the report of a refused set |
| ACE database administrator | The DEV sandbox, its 19 schemas and its 19 logins |

The map names no test owner, so the test owner is read from the contract owner: the owner of a table, an operation, an event, a workflow or a job is the owner of the test that pins it (Ownership Map v1; ASM-B-TESTDOC-43-13). Team types are suggestions only and any team may pick up a story; harness and non-functional integration stories are suggested for the QA team, and every other work type keeps the suggested owner of its work type (Template and Rules section R5.3). No person is named in this plan.

# 16. Traceability

| Requirement or decision | What it fixes | Where this plan proves it |
|---|---|---|
| ADR-013 | 19 services inside ACE | The wave table of section 3 and the journey of each wave |
| ADR-014 and ADR-021 | A schema and a login per service, and per-service migration ownership | The boundary test of TC-W1J01-04-ITG and the data row of section 6 |
| ADR-015 and DP-09 | Kafka with outbox, inbox and CloudEvents | TC-W1J01-02-ITG, TC-W1J01-04-ITG and the event row of section 7 |
| ADR-016 and DP-12 | A reusable Temporal layer, and a case workflow with a child per stage | TC-W1J01-03-ITG and the Temporal row of section 7 |
| ADR-017 and DP-04 | Embedded Drools per service with the registry in rwb-decision | The rules row of section 6 and the rule assertions of the journeys |
| ADR-019 and DP-19 | gateway-bff and the partner gateway at the edge | The composition assertion of every journey and the accessibility route of TC-ITG-TE010-ITG-01 |
| ADR-020 and DP-11 | Contract-first REST, one hop, 2 second timeout | TC-W1J01-01-ITG, TC-W1J01-10-ITG and the REST row of section 7 |
| ADR-022 and DP-03 | A local decision record plus the central ledger | Hop 5 of the wave 1 journey and TC-W4J01-06-ITG |
| ADR-018 and DP-17 | No data lake, and reporting from events | Hop 9 of the wave 1 journey and the measures read |
| NFR-045 and NFR-054 | Synthetic development data, and a pipeline that blocks a secret or personal data | TC-W1J01-05-ITG, TC-W1J01-07-ITG and TC-W1J01-09-ITG |
| NFR-008, NFR-059, NFR-060 and NFR-061 | Response targets, labels in Thai and English, and WCAG 2.1 AA | RWB-ITG-TE009-ITG and RWB-ITG-TE010-ITG |
| D-RCV-60 and DL48 | The realignment, and dates unchanged and tentative | Every release in this plan carries (tentative) |

The chain for a story is: the business epic, the service epic, the story, its acceptance criteria, its test cases and the wave gate that reads them. The chain for a gate is: the gate, the journey and harness identifiers, the contract versions pinned in the build, and the defect list at the gate date.

# 17. Risks and mitigations

| Risk | Effect on this plan | Mitigation |
|---|---|---|
| A later-wave service is not deployed when its contract is consumed | A journey hop runs against a stub | The report names every stub hop, the harness fails a stale stub set, and the real-owner hop is proven in the wave that deploys the service |
| A contract changes without its document | A component test passes while the journey breaks | The missing-document check of TC-W1J01-01-ITG fails the build, and a registry operation with no document is never a skip |
| The synthetic set and the SIT data set disagree | A journey fails on its fixture and not on its service | One set generated from a seed and a business date, loaded through owner operations, and a preflight that names the class that is missing |
| The 2 second budget is met per call but missed over a composite route | A screen is slow although every service is green | The load harness of RWB-ITG-TE009-ITG measures the screen through gateway-bff at the busiest hour |
| A wave gate is passed on a partial journey | A defect is found in production | A skipped, stubbed or red hop is not green, and the gate reads the whole trace and not a summary |
| The integration evidence outlives its environment | A gate cannot be re-read after the wave | The report is keyed by build and by business date and kept with the build |

# 18. Change log

| Change-log row | What changed |
|---|---|
| 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First version. It fixes the integration levels of the 19-service target, the wave composition and the four wave journeys, the harness RWB-ITG-W1J01-ITG, the non-functional integration evidence of RWB-ITG-NFR, the environments and the synthetic fixture set, the entry and exit of the five gates, the execution order, the test case inventory, defect routing and evidence, ownership and traceability. No earlier version of this family exists, so no section, identifier, number or date is carried forward (CG-B-TESTDOC-43-1; ASM-B-TESTDOC-43-1) |
