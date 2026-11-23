SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Test strategy

| Item | Detail |
|---|---|
| Document | Recovery Workbench test strategy |
| Version | 3 |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |


Version 3 keeps sections 1 to 7 of version 2, with every level, environment, gate, owner label, figure and date in them, and adds what the realignment needs: a contract test for every call type, a component test in which every downstream service is a published fake, and one integration test group per delivery wave. The Workbench is now 19 services inside ACE, each with one schema, one login, one REST base, one Kafka topic and one Temporal task queue (R4; ADR-013, ADR-014, ADR-015, ADR-016). The test levels, the entry and exit gates and the test scope follow that shape.

The source file is named v2 and its metadata table gives Version 1 at 28 October 2026; the file name is taken as the version the source carries, and version 3 is issued next to it (CG-B-TESTDOC-39-1; ASM-B-TESTDOC-39-1). No approval of this version is recorded, so it is issued as Draft: Not specified in the source documents (CG-B-TESTDOC-39-2; ASM-B-TESTDOC-39-2).

# 1. Levels

| Level | What it covers | Who | Where | When | Exit |
|---|---|---|---|---|---|
| Unit | Every service method and rule evaluation | Developer | DEV and the pipeline | Every commit | 80 percent line coverage on new code |
| Rule table | Each rule row against its test case | Developer with the analyst | Pipeline | Every commit and every rule version | Every row passes |
| Integration | One service with a real PostgreSQL database in its own rwb_* schema, and Kafka through Testcontainers | Developer | Pipeline | Every pull request | All pass |
| Contract | Requests and responses against the OpenAPI file; events against the AsyncAPI file and the schema registry; activities and workflows against the contract jar of the owning service | Developer | Pipeline | Every pull request | All pass; a change that breaks backward compatibility fails the build |
| Component | One service run against the published fake of every contract it consumes, with its own schema, outbox, inbox and topic | Developer | DEV and the pipeline | Every pull request | No call leaves the service; every fake answers from the published contract; the boundary test finds no cross-schema reference |
| Integration test group, one per wave | The real cross-service behaviour of one wave, on the real contracts of the services that exist in that wave | QA team with TechX | SIT | End of each wave | Every journey of the wave passes; no open severity 1 or 2 |
| System | Stories end to end against the SCB test systems | QA engineer | SIT | Rolling, then the SIT week | Every test case for the release passes; no open severity 1 or 2 |
| Regression | The regression suite | QA engineer | SIT | Each release | All pass |
| Non-functional | Performance, resilience, security | QA with SCB IT | SIT | Before each release | Targets in the NFR specification |
| Accessibility | Automated scan and keyboard checks | QA engineer | SIT | Each screen | No level A or AA failure |
| User acceptance | Business scripts | Business testers | UAT | UAT week | Scripts signed by the business lead |


The nine levels of version 2 are kept in their order. The Integration row now means one service with its own real database, because each service owns one schema and one login and no service reads another service's tables (ADR-014). The API contract row is now the Contract row, and it covers the three contract shapes the realignment publishes: OpenAPI 3.1 for REST, AsyncAPI 3.0 with the JSON Schema registry for events, and a contract jar for the Temporal activity and workflow interfaces (Architecture v5 slide 11). The Component row and the integration-test-group row are new; their names, who runs them and what they prove come from Architecture v5 slides 11 and 46 and from Template and Rules §R5.4, and no source states their exit criteria, so the criteria written in those two rows are an assumption (CG-B-TESTDOC-39-3; ASM-B-TESTDOC-39-3).

The pipeline order is fixed by the dependency classes. A CON story has no build dependency, is Day 1 and sits in contract group CG-W<wave>, so the contract and its fake exist before the code that uses them (Template and Rules §R5.7). An APP story builds against the contract and the fake, and a C dependency never blocks (Template and Rules §R5.4). The real cross-service behaviour is tested at the integration level only, on ITG stories, because an I dependency is allowed there and nowhere else (§R5.4).

# 2. Environments

| Environment | Data | Use |
|---|---|---|
| DEV | Synthetic only | Developer and rule tests |
| SIT | Masked copies from the PII service | System, regression, non-functional |
| UAT | Masked copies | Business acceptance |


Each environment runs the 19 services of the wave under test, each with its own schema rwb_<name>, login, REST base /api/recovery/<short>/v1, topic rwb.<short>.events.v1 and task queue rwb-<short> (R4; Ownership Map v1 sheet Services). The contract fakes run in DEV and in the pipeline, never as a substitute for a service that exists in SIT.

In SIT the services of the wave under test run for real. A service of a later wave is not deployed yet; until it is, its published contract is served by its fake, and the statement of how SIT is composed across waves is not in any source read for this document: Not specified in the source documents (CG-B-TESTDOC-39-5; ASM-B-TESTDOC-39-5).

Architecture v5 slide 45 counts 19 x 4 environments and names none of them. Version 3 keeps the three environments version 2 names and does not name the fourth: Not specified in the source documents (CG-B-TESTDOC-39-6; ASM-B-TESTDOC-39-6).

# 3. Entry and exit

| Gate | Entry | Exit |
|---|---|---|
| ITG-W1 | The nine wave 1 services deployed in SIT (P1, P2, P3, P4, P5, P6, P7, P9, P10); every wave 1 contract in force; the harness RWB-ITG-W1J01-ITG done | Every wave 1 journey passes; no open severity 1 or 2 |
| ITG-W2 | Wave 1 exit met; P8, S2, S5 and S8 deployed | Every wave 2 journey passes; no open severity 1 or 2 |
| ITG-W3 | Wave 2 exit met; S1, S3, S4 and S6 deployed | Every wave 3 journey passes; no open severity 1 or 2 |
| ITG-W4 | Wave 3 exit met; S7 and S9 deployed | Every wave 4 journey passes; no open severity 1 or 2 |
| SIT | Release tag built; stories done in DEV; test data loaded | Every test case passes; no open severity 1 or 2; severity 3 with an agreed fix date |
| UAT | SIT exit met; scripts walked through with the testers | Scripts signed by the business lead; open defects accepted or behind a flag |
| Release | SIT and UAT exits | Go decision by the release owner |


The SIT, UAT and Release rows are unchanged. The four wave gates are new: one per integration epic, RWB-ITG-W1 to RWB-ITG-W4 (Template and Rules §R5.1), and each one closes before the next wave's services are taken as the subject of an integration test. The wave of each service is the wave the Ownership Map v1 gives it (sheet Services), which is the Architecture v5 wave in Template and Rules §R4.

Programme release dates are unchanged and tentative (R1 U7; DL48). A wave gate never moves a release date; it decides whether the wave's journeys can be signed off.

# 4. Test data

Synthetic in DEV; masked copies in SIT and UAT; no production data below production. The test data plan sets the data each test needs.

With 19 schemas the synthetic data is built per schema, and a test may not read another service's data (ADR-014): a component test seeds its own schema, and a component or contract test seeds a fake, not another service's tables. The contract-test harness and synthetic test data story RWB-ITG-W1J01-ITG holds the harness and the data set that every wave journey uses. A fake holds no personal data, and no test data is placed in a Kafka event, a workflow input or a log (Architecture v5 slide 11; Template and Rules §R7.2 section 17).

# 5. Who tests what

| Who | Tests |
|---|---|
| Developers | Unit, rule table, component, integration, contract |
| QA engineers | System, regression, accessibility, non-functional with SCB IT |
| Business testers | During the build with the squads; UAT scripts |
| SCB IT security | Penetration test before the partner portal opens |
| Role owners | Access tests per role |
| Contract owners, per service | The contract tests of the tables, REST operations, events, workflows and jobs the Ownership Map v1 assigns to that service, and the fakes it publishes |
| QA team, harness and NFR | The contract-test harness and the synthetic data (RWB-ITG-W1J01-ITG), the performance harness, the browser and accessibility tests, and the wave journeys |


The five rows of version 2 are kept; the Developers row now names component tests as well, because every service is tested against fakes of its downstream contracts before it meets them. The last two rows are new. The owner of a contract test and of a fake is the owner the Ownership Map v1 gives the table, REST operation, event, workflow or job (sheets Tables, Endpoints, Events, Workflows and activities, Jobs); the map names no test owner, so the test owner is read from the contract owner: Not specified in the source documents (CG-B-TESTDOC-39-4; ASM-B-TESTDOC-39-4).

Team types are suggestions only, and any team may pick up a story (Template and Rules §R5.3). Harness and NFR stories are suggested for the QA team; every other work type keeps the suggested owner of its work type.

# 6. Traceability

Every test case names its story and acceptance criterion or its rule ID. The requirements traceability matrix links requirement, feature, story, specification section and test.

With one service per business module, the traceability gains two points. The story ID names the service: the scope of RWB-<scope>-<legacy>-<work type> is a service, PLT or ITG (Template and Rules §R5.2), so a test case that fails names its owning service in its story ID. The ITG copy of a test case ends in -ITG and sits on the ITG story of its wave (Template and Rules §R7.2 section 16), so a system test case and its integration copy are always traceable to each other.

In Epic 1 the six preserved stories keep their as-built sections word for word, section 16 included, and the microservice tests sit on the delta stories and on the CON and OPS stories (R6; DL47; U2). No test case of a preserved story is rewritten.

# 7. Defects

Defects follow the defect management process: severity, owner, fix and retest. A release goes with no open severity 1 or 2 defect.

A defect raised by a wave journey names the owning service from the Ownership Map v1 and the contract it breaks, so a defect that crosses two services is routed to the owner of the contract, not to the caller. A defect that a contract test finds in the owner's build is fixed before the contract is published; a defect that a consumer's component test finds against a published contract is a contract defect and is raised with the owner.

# 8. Contract tests

Every service publishes its contracts before code, and contract tests run in every build (Architecture v5 slide 11): OpenAPI 3.1 for REST with /v1 in the path, AsyncAPI 3.0 for events with the JSON Schema registry in BACKWARD compatibility, and a contract jar for the Temporal activity and workflow interfaces. The test proves the published contract, not the implementation behind it, so it runs in the owner's build and in the build of every consumer that holds a fake of it.

| Call type | Contract under test | What the test proves | Owner |
|---|---|---|---|
| REST | OpenAPI 3.1, /v1 in the path | Every operation and status code; RFC 9457 problem details on failure; Idempotency-Key on every POST; a 2 second timeout, one retry on GET only, and breaker and bulkhead on the caller | The service the Ownership Map v1 assigns the operation (sheet Endpoints) |
| Kafka event | AsyncAPI 3.0 and the JSON Schema registry, BACKWARD compatibility | The CloudEvents 1.0 envelope in binary mode, key caseId and order per case; IDs and facts only, no personal data; a payload that passes the previous schema version; dedupe by the inbox; retry topics at 1 minute, 10 minutes and 1 hour, then the dead-letter topic with an alert | The producer the Ownership Map v1 assigns the event (sheet Events) |
| Temporal | The activity and workflow interface in the contract jar | Every activity and workflow signature and typed failure the caller uses; the caller imports the interface only and calls the owner's task queue; workflow ID is the business key | The owner the Ownership Map v1 assigns the workflow (sheet Workflows and activities) |
| File | The manifest: fileId, batchId, sha256 and record count | The manifest fields, the checksum on receipt, a 15 minute SAS link, and that a re-delivery is safe; the data stays out of the message | rwb-integration (P2) and the party that receives the file |
| SQL view | The 30 recovery.v_ace_* views | The read-only login reads the 30 views; no other service reads them; the 5 second statement timeout holds | rwb-source-data (P1) |


A contract test is not a substitute for a journey. It fixes the shape of one call type between one owner and one caller; what happens when several services react to one case is section 10.

# 9. Component tests with mocks

A component test runs one service with everything outside it replaced by the published fake of the contract it consumes. It is the level that lets a lane start on Day 1: the contract and its fake exist before the downstream service does, and the component test is green against the contract the owner will keep (Template and Rules §R5.7; ADR-020).

| In a component test | Real | Fake | What the test proves |
|---|---|---|---|
| Data | The service's own schema rwb_* on Testcontainers PostgreSQL, its own login and its Flyway sequence | Every other schema | The service reads and writes only its own schema, and the boundary test fails the build on a cross-schema reference (ADR-014, ADR-021) |
| Events | Its own topic, consumer group, outbox relay and inbox on Testcontainers Kafka | Every producer and consumer outside the service | The outbox publishes in the same transaction as the state change; the inbox drops a duplicate; a failure reaches the retry topics and the dead-letter topic (ADR-015) |
| Workflow | The Temporal test server and the workflow kit (RWB-PLT-N010-CON) | An activity of another service | The workflow is deterministic and replays; it holds no database call, clock, random, network call or Drools call; a recorded history replays against the new build (E2-040) |
| Rules | Embedded Drools and the rule package | The rule registry of rwb-decision (C RWB-P7-E1073-CON) | The answer names the rule and the package version, is returned in under 300 ms, and a package that fails a load check is REFUSED while the last good version keeps running (ADR-017) |
| Downstream calls | The code under test | The fake named in section 12.8 of the story | The call, the timeout, the problem details and the retry match the published contract; no call leaves the service |


Three assertions are always made in a component test. The decision record, the state change and the outbox row are one transaction, so a failed decision-record write moves nothing (R-UNI-39). An activity that finds no rule package in force fails at once with no retry, and the stuck-workflow scan JOB-21 raises it. An AI answer that is late is abandoned after 60 seconds and the rule result is used (R-UNI-32).

# 10. Integration test group per wave

The integration test group of a wave is the only level at which the real cross-service behaviour is tested, because an I dependency is allowed on ITG stories only (Template and Rules §R5.4). There is one integration epic per wave, RWB-ITG-W1 to RWB-ITG-W4, plus RWB-ITG-NFR for the non-functional work (Template and Rules §R5.1). Each wave has one journey story and shares one harness.

| Wave | Services under test | Journey story | What the journey proves | Exit |
|---|---|---|---|---|
| W1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | RWB-ITG-W1J02-ITG | ACE data ready, an eligible account becomes a case, the case is allocated, the officer is authorised, a decision is recorded, a timer breach is raised, and the case summary and the reporting projection agree with the case | Every W1 journey passes |
| W2 | W1 plus P8, S2, S5, S8 | RWB-ITG-W2J01-ITG | A settlement or restructure offer is approved and booked, a missed payment raises the cure path, a deviation is raised and cleared, an asset is taken on, and proceeds are matched | Every W2 journey passes |
| W3 | W2 plus S1, S3, S4, S6 | RWB-ITG-W3J01-ITG | A route is decided from the valuation, a guarantee claim is made, a judgment and an auction result are recorded, and a debt-sale lot is awarded | Every W3 journey passes |
| W4 | W3 plus S7, S9 | RWB-ITG-W4J01-ITG | A write-off is approved and the debt released, and a partner instruction is issued, answered and closed | Every W4 journey passes |


The harness RWB-ITG-W1J01-ITG (contract-test harness and synthetic test data) is Day 1 and serves all four waves. The journeys are the ones the wave's events already describe (Architecture v5 slides 42 and 43, A2 and A3 event catalogues), and each journey story carries its test cases with the -ITG suffix (Template and Rules §R7.2 section 16). The step-by-step journey and test case list per wave is not stated in any source read for this document: Not specified in the source documents (CG-B-TESTDOC-39-7; ASM-B-TESTDOC-39-7).

A wave journey uses the real contract of every Recovery service that exists in its wave and no fake between them. Systems outside the bank and ACE Common stay as they are for the test, and a party outside the bank is reached through the partner gateway and rwb-integration (ADR-019; Architecture v5 slide 11).

The platform keeps a daily journey smoke: the smoke workflow JOB-22 runs at 06:00 on a Schedule (Architecture v5 slide 44), so a broken journey is seen the next morning and not at the end of a wave.

# 11. Test scope per service

The scope of every contract and component test is the set of contracts the Ownership Map v1 assigns to the service. Across the 20 owner rows the map assigns 93 tables, 156 REST operations, 30 events, 15 workflows and 22 jobs; the table is the one to check a test plan against.

| Code | Service | Wave | Tables | REST operations | Events | Workflows | Jobs |
|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | 18 | 18 | 2 | 0 | 3 |
| P2 | rwb-integration | 1 | 3 | 11 | 0 | 0 | 0 |
| P3 | rwb-case | 1 | 15 | 22 | 7 | 1 | 3 |
| P4 | rwb-access | 1 | 5 | 4 | 0 | 0 | 1 |
| P5 | rwb-document | 1 | 12 | 17 | 2 | 1 | 2 |
| P6 | rwb-comms | 1 | 3 | 11 | 3 | 1 | 1 |
| P7 | rwb-decision | 1 | 6 | 19 | 3 | 1 | 3 |
| P8 | rwb-payment | 2 | 1 | 2 | 3 | 0 | 2 |
| P9 | rwb-reporting | 1 | 3 | 1 | 0 | 0 | 1 |
| P10 | rwb-agent | 1 | 8 | 11 | 1 | 1 | 0 |
| S1 | rwb-valuation | 3 | 0 | 3 | 0 | 1 | 0 |
| S2 | rwb-treatment | 2 | 1 | 4 | 1 | 1 | 0 |
| S3 | rwb-guarantee | 3 | 1 | 2 | 0 | 1 | 0 |
| S4 | rwb-litigation | 3 | 2 | 5 | 0 | 1 | 0 |
| S5 | rwb-asset | 2 | 2 | 6 | 1 | 1 | 1 |
| S6 | rwb-debtsale | 3 | 2 | 5 | 1 | 1 | 0 |
| S7 | rwb-writeoff | 4 | 1 | 2 | 1 | 1 | 1 |
| S8 | rwb-deviation | 2 | 1 | 2 | 2 | 1 | 0 |
| S9 | rwb-partner | 4 | 3 | 6 | 2 | 1 | 0 |
| PLT | Platform: shared libraries, workflow kit, event platform | 0 | 6 | 5 | 1 | 1 | 4 |


A zero in a column is not a gap in the tests. rwb-source-data owns no workflow and is called as an activity by rwb-case, so that call is tested against the contract jar of rwb-source-data, not against a workflow of its own. rwb-valuation owns no table row in the map at 22 November 2026, while Architecture v5 slide 18 gives it a schema rwb_valuation with valuations, the D6 route decision and the route agent output, so its storage and its data tests are open: Not specified in the source documents (CG-B-TESTDOC-39-8; ASM-B-TESTDOC-39-8).

# 12. Change log

| Change-log row | What changed |
|---|---|
| 1, 28 October 2026, baseline | The source as issued: sections 1 to 7, nine test levels, three environments, three gates, test data, who tests what, traceability and defects. The file is named v2, its metadata table gives Version 1, and it carries no change-log row, so no row 2 exists (CG-B-TESTDOC-39-1; ASM-B-TESTDOC-39-1) |
| 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | Section 1 adds the Contract and Component levels and the integration test group per wave; section 2 states the per-service environment and keeps the three environments; section 3 adds the four wave gates; section 4 adds synthetic data per schema and the fakes; section 5 adds the contract owner and the QA harness rows; section 6 adds the service and -ITG traceability; section 7 adds contract defect routing; sections 8, 9, 10 and 11 are new; section 12 is new |

