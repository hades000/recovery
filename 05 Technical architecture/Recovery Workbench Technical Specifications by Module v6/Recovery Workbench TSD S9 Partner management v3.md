SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S9 Partner management

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S9 Partner management |
| Document ID | S9-RWB-TSD-v3 |
| Version | 3 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 3 is recorded (GAP-1998; ASM-3217) |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S9 Partner management | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

S9 Partner management is one of the 19 services of Architecture v5: `rwb-partner` (service name Partner, module S9, wave 4, service epic `RWB-SVC-S9`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S9 is the only service reachable from outside the bank: the partner gateway in the DMZ terminates partner traffic and S9 owns the panel, the instructions and the results (ADR-019).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S9 Partner management |
| Service | `rwb-partner` (Partner) |
| Service epic | `RWB-SVC-S9` |
| Wave | 4 |
| Schema | `rwb_partner` |
| Database login | `rwb_partner`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/partner/v1` |
| Kafka topic | `rwb.partner.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.partner.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-partner` |
| Java package | `th.co.scb.ace.workbench.recovery.partner` |
| Edge | gateway-bff for staff screens; the partner gateway in the DMZ for partner traffic |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-partner.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: panel, partner users, instructions, results, fees, scorecards. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_partner` | `partner`, `partner_instruction`, `partner_user` | 3 |
| REST operations | appendix T-A and `rwb-partner.yaml` | 6 |
| Events published | EV-20 InstructionIssued, EV-21 PartnerResultSubmitted | 2 |
| Workflows and schedules | InstructionWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_partner`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_partner`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-PRT-004 / partner_type / LOV / varchar(15) / Yes / LOV-PARTNER-TYPE…` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.partner.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S9-001 / GET / /api/recovery/v1/partners / Partner portal R / E2` | REST base `/api/recovery/partner/v1`. |
| DP-14 | — | Topic `rwb.partner.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_partner`. |
| DP-19 | `INT-24 / Partner portal / Both / Workbench screens through the external gateway / As entered` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It authenticates no staff user: staff arrive through gateway-bff and partners through the partner gateway (ADR-019).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S9 Partner management is delivered as the service `rwb-partner` (module S9, wave 4, service epic `RWB-SVC-S9`): one repository, one pipeline, one schema `rwb_partner` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: panel, allocation, fees, scorecards, conduct. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| PartnerManagementController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| PartnerManagementService | Business logic; calls the rules component; writes the decision log entry before any change |
| PartnerManagementRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-partner` lives in schema `rwb_partner` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `partner`, `partner_instruction` and `partner_user` are this service's tables; internal roles stay in P4 and partner users do not (Ownership Map ruling `partner_user`, ASM-0072).

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Object and field definitions

**partner** (NEW). An outside firm the bank places work with.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PRT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PRT-002 | partner_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-PRT-003 | partner_name | TEXT | varchar(160) | Yes | None | Workbench |
| DF-PRT-004 | partner_type | LOV | varchar(15) | Yes | LOV-PARTNER-TYPE | Workbench |
| DF-PRT-005 | panel_status | LOV | varchar(12) | Yes | LOV-PANEL | Workbench |
| DF-PRT-006 | contract_end | DATE | date | No | None | Workbench |
| DF-PRT-007 | score | NUMBER | numeric(5,2) | No | None | Workbench |

**partner_instruction** (NEW). Work placed with a partner on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PRT-008 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PRT-009 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PRT-010 | partner_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PRT-011 | instruction_type | LOV | varchar(20) | Yes | LOV-INSTRUCTION | Workbench |
| DF-PRT-012 | instructed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-PRT-013 | due_at | DATE | timestamptz | No | None | Workbench |
| DF-PRT-014 | status | LOV | varchar(12) | Yes | LOV-INSTR-STATUS | Workbench |
| DF-PRT-015 | result_code | TEXT | varchar(40) | No | None | Workbench |
| DF-PRT-016 | fee_amount | NUMBER | numeric(18,2) | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-INSTR-STATUS | SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE, RECALLED |
| LOV-INSTRUCTION | COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST, SELL |
| LOV-PANEL | ACTIVE, ON_NOTICE, SUSPENDED, EXITED |
| LOV-PARTNER-TYPE | AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| partner_instruction | case_id | recovery_case | Many to 1 |
| partner_instruction | partner_id | partner | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-24 | Partner portal | Both | Workbench screens through the external gateway | As entered |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/partner/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/partners` | `getPartners` |
| 2 | POST | `/cases/{caseId}/instructions` | `postCasesCaseidInstructions` |
| 3 | GET | `/partner/instructions` | `getPartnerInstructions` |
| 4 | POST | `/partner/instructions/{instructionId}/accept` | `postPartnerInstructionsInstructionidAccept` |
| 5 | POST | `/partner/instructions/{instructionId}/results` | `postPartnerInstructionsInstructionidResults` |
| 6 | POST | `/partner/instructions/{instructionId}/invoices` | `postPartnerInstructionsInstructionidInvoices` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| InstructionWorkflow (SLA timers) | Temporal workflow | S9 rwb-partner | Contract of T5.2.1 |
| issueInstruction, recordResult | Temporal activity | S9 rwb-partner | Called by S4 and S5 |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| InstructionIssued | EV-20 | `rwb.partner.events.v1` | partner portal |
| PartnerResultSubmitted | EV-21 | `rwb.partner.events.v1` | rwb-litigation, rwb-asset, rwb-case |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Partner upload link (time-limited) | REST | P5 rwb-document | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Partner gateway: partner identity and MFA (FAPI 2.0) | REST | Partner gateway | X | Tracked only; outside the Workbench; class X |

Events this service consumes:

None.

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 6 | 2 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 0 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 0 | Workflow and activity interfaces, queue `rwb-partner` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-partner.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| InstructionIssued | EV-20 | Published | `rwb.partner.events.v1` |
| PartnerResultSubmitted | EV-21 | Published | `rwb.partner.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Partner portal |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-LITOFF Litigation officer | CRU |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | CRU |
| RW-NPAMGR NPA and asset manager | CRU |
| RW-DEBTSALE Debt sale officer | CRU |
| RW-GUARANT Guarantee officer | CRU |
| RW-AGENCYMG Partner and agency manager | CRUDA |
| RW-CONDUCT Conduct and QA officer | R |
| RW-CAPACITY Capacity and workforce planner | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R |
| RW-HEADLIT Head of Litigation | RA |
| RW-HEADNPA Head of NPA | RA |
| RW-HEADASL Head of Asset Liquidity | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-AGENCY Collection agency (OA) user | RU |
| PT-LAWFIRM Law firm user | RU |
| PT-VALUER Valuer | RU |
| PT-AUCTION Auction vendor | RU |
| PT-BUYER Debt buyer and AMC | RU |
| PT-RAMC RAMC user | RU |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Proposed |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Proposed |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Proposed |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Proposed |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Proposed |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Proposed |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Proposed |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-S9-001 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-002 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-003 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-004 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-005 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-006 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-007 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-008 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-009 | FEAT-PRM-08 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S9-001 | GET | /api/recovery/partner/v1/partners | Partner portal R | E2 |
| API-S9-002 | POST | /api/recovery/partner/v1/cases/{caseId}/instructions | Partner portal C | E4 |
| API-S9-003 | GET | /api/recovery/partner/v1/partner/instructions | Partner portal R | E4 |
| API-S9-004 | POST | /api/recovery/partner/v1/partner/instructions/{instructionId}/accept | Partner portal U | E4 |
| API-S9-005 | POST | /api/recovery/partner/v1/partner/instructions/{instructionId}/results | Partner portal U | E4 |
| API-S9-006 | POST | /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices | Partner portal C | E6 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S9-001 GET /partners

| Item | Value |
|---|---|
| Purpose | List partners with panel status and score |
| Request | Query: type, status |
| Response | Partner[] |
| Errors | 401, 403, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S9-002 POST /cases/{caseId}/instructions

| Item | Value |
|---|---|
| Purpose | Issue an instruction to a partner by rule |
| Request | InstructionRequest |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Partner portal, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-003 GET /partner/instructions

| Item | Value |
|---|---|
| Purpose | List the instructions placed with the caller's firm |
| Request | Query: status, page, size |
| Response | InstructionPage |
| Errors | 401, 403, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S9-004 POST /partner/instructions/{instructionId}/accept

| Item | Value |
|---|---|
| Purpose | Accept or decline an instruction |
| Request | InstructionAcceptance |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Partner portal, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-005 POST /partner/instructions/{instructionId}/results

| Item | Value |
|---|---|
| Purpose | Record a result with its documents |
| Request | Multipart: result, files |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 415, 422, 503 |
| Authorization | Partner portal, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-006 POST /partner/instructions/{instructionId}/invoices

| Item | Value |
|---|---|
| Purpose | Submit a fee invoice |
| Request | InvoiceRequest |
| Response | Invoice |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Partner portal, right C, scope applied |
| Idempotency | Idempotency-Key header |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
