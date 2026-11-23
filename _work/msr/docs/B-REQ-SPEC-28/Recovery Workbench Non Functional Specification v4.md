SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

## Non-functional specification

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench non-functional specification |
| Version | 4 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC 25010 quality characteristics |
| Requirements | 80 (78 in version 3, plus NFR-079 and NFR-080) |
| Decision | D-RCV-60 microservice realignment, on the Architecture v5 target; ADR-019, ADR-020 |
| Owner of record | Microservice Ownership Map v1; the owning service in every table below is taken from it |
| Status | Draft (no approval recorded; ASM-B-REQ-SPEC-28-1) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### Change log

| Version | Date | Change |
|---|---|---|
| 4 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

Version 4 keeps every section, requirement ID, number and date of version 3. What is new is listed in section 6.1;
the short note under each affected section gives the reason in place.


# 1. Targets on one page

| Area | Main target | Status | Owning service (Ownership Map v1) |
|---|---|---|---|
| Volume | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month | Sized; DL15 | P3 rwb-case (case store); P1 rwb-source-data (ACE accounts) |
| Users | About 370 staff and 50 partner users online in the busiest hour; 1,234 named users | Proposed | P4 rwb-access; PLT (gateway-bff session store) |
| Screens | Under 2 seconds at the 95th percentile at the busiest-hour load | Proposed, DL11 | PLT (gateway-bff composition); the owner of each call |
| Agents | Answer within 60 seconds; after that the rule result is used | Proposed, DL11 | P10 rwb-agent |
| Freshness | Case list available by 07:00 on the latest completed ACE batch; reconciled to the ACE account view every day | Proposed; DL43 | P1 rwb-source-data (data_product_load) |
| Availability | 99.9 percent in business hours; recovery point and time as set for ACE | Proposed; open DL11 | PLT (platform); all 19 services |
| Storage | About 5.8 million documents and 2.8 TB by the end of 2031; about 36 GB of decision log and ledger | Proposed | P5 rwb-document; P7 rwb-decision; P1 rwb-source-data |
| Audit | Every decision reproducible from the log with its rule, model and prompt versions | Proposed | P7 rwb-decision (decision_log_entry) |
| Security | Single sign-on with multi-factor authentication; masking by role; no secrets in code | Proposed | P4 rwb-access; PLT (platform) |
| Partners | Partner access from outside the bank through the external gateway | Open, DL03 | S9 rwb-partner; PLT (partner gateway) |
| Calls | REST is one hop from gateway-bff to the owning service, with a 2 s call timeout, a single GET retry with jitter and a circuit breaker and bulkhead per downstream | Proposed, D-RCV-60 | PLT (gateway-bff); all 19 services |


Each requirement has a measure, the test that proves it and an owner. A requirement marked Proposed is built and tested against the value shown until the owner confirms it under the decision named.

Realignment (D-RCV-60). The owning service cell is new: it names the service that owns the object a target measures,
taken from the Microservice Ownership Map v1 (Tables, Endpoints, Events, Workflows and activities, and Jobs sheets), with PLT
for the platform items the map leaves to the platform (gateway-bff, the key store, observability, the build pipeline). Every
source target, status and decision cell is unchanged, and a target whose owner the map does not name carries the section R9
placeholder.

# 2. Volumes and concurrency

| Measure | Value | Basis | Owning service (Ownership Map v1) |
|---|---|---|---|
| Accounts at 90 days past due, active inventory | 28,119 | Mortgage 12,256; hire purchase 12,960; SSME 2,903 at 30 June 2026 | P1 rwb-source-data (30 recovery.v_ace_* views) |
| New accounts at 90 days past due a month | 3,110 | Average of the last 12 months | P1 rwb-source-data |
| Open cases at go-live | About 23,600 | 1.2 accounts per case (DL17) | P3 rwb-case |
| Open cases at the end of 2027 | About 26,500 | 15 percent inflow growth a year (DL15) | P3 rwb-case |
| Named users | 1,234 | 466 recovery staff, 448 collections staff reading the case record, 320 partner users | P4 rwb-access |
| Online in the busiest hour | About 410 | 40 percent of bank users and 15 percent of partner users | PLT (gateway-bff session store) |
| Requests a second in the busiest hour | About 21 | Three requests a minute for each active user | PLT (gateway-bff) |
| Documents held at the end of 2031 | About 5.8 million | 15 per new case and one per open case each month | P5 rwb-document |
| Hire purchase accounts outside the active inventory | 156,351 | Held in ACE; read through v_ace_account when a case is opened, not copied | P1 rwb-source-data (v_ace_account view) |

Realignment (D-RCV-60). The concurrency figures do not agree across the sources: this table has about 410 users online in
the busiest hour, NFR-002 and NFR-003 give about 370 staff and about 50 partners, and Architecture v5 slide 48 gives 414
concurrent staff and 48 concurrent partners. Every number is kept as written; the difference is recorded as
CG-B-REQ-SPEC-28-5 with ASM-B-REQ-SPEC-28-6, which reads 414 staff and 48 partners as the load-test figures.


# 3. Requirements by quality characteristic

## 3.1 Volume and capacity

ISO/IEC 25010: Performance efficiency: capacity. Tested by: Load test in SIT with data at the stated volume; query times read at that size.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. Confirmed under DL15 | Risk with the data product owner | Proposed from the volume forecast | P3 rwb-case (recovery_case, case_account) |
| NFR-002 | The system supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | Business lead | Proposed from the volume forecast | PLT (gateway-bff session store); P4 rwb-access |
| NFR-003 | The system supports the peak number of partner users signed on at once across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour, of about 320 named users | Partner and agency manager | Proposed from the volume forecast | S9 rwb-partner (partner, partner_user) |
| NFR-004 | The document store holds the annual inbound document volume with its growth rate. | About 860,000 documents in 2027, rising with 15 percent inflow growth a year | Legal with Autonomous Ops | Proposed from the volume forecast | P5 rwb-document (document_intake) |
| NFR-005 | The restructure path carries the monthly case volume reaching the Workbench. | About 3,000 restructure accounts a month reach the bank's restructure process today | Solution architect | Proposed | S2 rwb-treatment (treatment) |
| NFR-006 | The deed in lieu path carries its target monthly volume. | 1,000 cases a month in 2027, from 685 today | Solution architect | Proposed | S2 rwb-treatment (treatment) |
| NFR-007 | The decision log holds one record for every decision on every case for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | Compliance with the solution architect | Proposed, DL11 | P7 rwb-decision (decision_log_entry) |
| NFR-069 | The document hub holds the full recovery document estate as a system of record, including every version and every held document, with storage sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031, with every version and held document | Solution architect with Compliance | Proposed, DL11 | P5 rwb-document (document, document_custody) |
| NFR-070 | The interaction ledger holds every interaction on every open and closed case within its retention period, and reads a single case history inside the user wait. | One case history reads in under 2 seconds with the ledger at its 2031 size | Data lead with the solution architect | Proposed, DL11 | P1 rwb-source-data (interaction) |


## 3.2 Response time

ISO/IEC 25010: Performance efficiency: time behavior. Tested by: Performance test in SIT at the busiest-hour load; 95th percentile read from the traces. The NFR-008 and NFR-009 targets include reads through the recovery.v_ace_* views, with ACE and recovery data joined at the busiest hour.

Realignment (D-RCV-60). REST is one hop from gateway-bff to the owning service, and a composite screen is composed from
parallel one-hop calls, never a call chain: gateway and session 0.15 s, the slowest parallel call 0.6 s and the merge 0.3 s
come to about 1.05 s, planned at about 1.2 s, against the 2 s target at the 95th percentile (Architecture v5 slides 10 and 11;
DP-11; ADR-020). Every REST call carries a 2 s timeout, a single GET retry with jitter, and a circuit breaker and bulkhead per
downstream (Architecture v5 slide 11). NFR-008 and NFR-009 are read against that composition, and NFR-079 and NFR-080 state
the rule as requirements.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-008 | A screen responds within its target under normal load. | Under 2 seconds | Solution architect | Proposed | PLT (gateway-bff composition); the owner of each call |
| NFR-009 | The case record view loads for a case with 50 documents. | Under 2 seconds | Solution architect | Proposed | P3 rwb-case; P5 rwb-document |
| NFR-010 | An agent returns an answer within its target, after which the rule result is used and the case still routes. | Under 60 seconds | Solution architect | Proposed | P10 rwb-agent (agent_run, AgentRunWorkflow) |
| NFR-011 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | Solution architect | Proposed, DL11 | P7 rwb-decision (rule_package); each service's embedded Drools kit (DP-04) |
| NFR-012 | A search across cases and documents returns within its target. | Under 3 seconds for a search across cases; under 5 seconds across documents | Business lead | Proposed, DL11 | P3 rwb-case; P5 rwb-document |
| NFR-079 | A REST call between services completes inside its timeout, and no call chain is deeper than one hop from gateway-bff. | 2 seconds per REST call; one hop only; GET retried once with jitter; circuit breaker and bulkhead per downstream | Solution architect | Proposed, D-RCV-60 | PLT (service template and gateway-bff) |
| NFR-080 | A composite screen is composed by gateway-bff from parallel one-hop calls to the owning services, and never by one service calling another for a screen. | One hop per call; about 1.05 seconds budgeted at the 95th percentile, about 1.2 seconds planned, against the 2 second target | Solution architect | Proposed, D-RCV-60 | PLT (gateway-bff) |


## 3.3 Freshness and availability of ACE data

ISO/IEC 25010: Performance efficiency and reliability. Tested by: Hold an ACE batch in SIT and confirm the case list shows the last completed business date and alerts the data steward; release the batch and confirm the case list catches up with no Workbench load. NFR-016, NFR-017 and NFR-019 remain Workbench document and scheduling jobs; they load no source data.

Realignment (D-RCV-60). Only P1 rwb-source-data reads the 30 recovery.v_ace_* views, with its own read-only login and a
statement timeout; every other service reads ACE data through P1's published contract or its own v_ace_* view (Architecture v5
slides 9 and 11; DP-05). The view names and the batch-status row of NFR-013 and NFR-014 therefore belong to P1, and the
freshness rule, the business date and the alerts stay exactly as written.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-013 | Under D-RCV-35 (U1 and U4) and ADR-010, the Workbench reads source data only through the recovery.v_ace_* views, and every case list and decision states the business date and load time of the ACE source batches behind it. | Case list available by 07:00 on the latest completed ACE batch | Solution architect | Proposed, DL43 | P1 rwb-source-data (data_product, data_product_load) |
| NFR-014 | Freshness is read from recovery.v_ace_batch_status, one row per source and business date; a missing, failed or late batch is visible on the case list and alerts the data steward. | Start of day, on the ACE business date (target unchanged) | Solution architect | Proposed, DL43 | P1 rwb-source-data (data_product_load) |
| NFR-015 | The Workbench holds no load window: a late ACE batch delays the case list and raises an alert rather than starting a Workbench load, catch-up job or staging table. | Visible as soon as the ACE batch completes; no Workbench lag; same-day needs under DL06 | Solution architect | Proposed, DL43 | P1 rwb-source-data |
| NFR-016 | The document intake pipeline processes its throughput in the test environment. | 500 pages per hour | Solution architect | Proposed | P5 rwb-document (document_intake, DocumentIntakeWorkflow) |
| NFR-017 | Document classification is correct on the labeled sample, and anything below the confidence threshold goes to a review queue. | 90 percent correct | Solution architect | Proposed | P5 rwb-document; P10 rwb-agent (classification) |
| NFR-018 | The case list reconciles to the ACE account view daily. | No unexplained variance; tolerance under DL25 (target unchanged) | Solution architect | Proposed, DL25 | P1 rwb-source-data (reconciliation_result, JOB-04); P3 rwb-case (case list API) |
| NFR-019 | The daily rebalancing job completes before the working day starts. | Complete by 07:00 | Team manager | Proposed, DL11 | P3 rwb-case (JOB-06 Schedule rebalancing) |


## 3.4 Availability and recovery

ISO/IEC 25010: Reliability: availability and recoverability. Tested by: Failover and restore test before the first production release; availability read monthly from monitoring.

Realignment (D-RCV-60). Architecture v5 splits the Workbench into 19 services and records that the recovery point and recovery
time objectives are not set (slide 48). NFR-022 and NFR-023 keep their source targets and stay Open under DL11; because the
value and the per-service tier are both missing, their owning service cell carries the section R9 placeholder and
CG-B-REQ-SPEC-28-1 and CG-B-REQ-SPEC-28-2 are raised. NFR-024 to NFR-027, NFR-071 and the two availability targets stay as
written and apply service by service.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-020 | The Workbench is available during business hours. | 99.9 percent in business hours | Solution architect | Proposed | PLT (platform); all 19 services |
| NFR-021 | Availability outside business hours, when batch, dispatch and partner exchange run. | 99.5 percent outside business hours, excluding the change window | IT lead | Proposed, DL11 | P2 rwb-integration (file windows); P6 rwb-comms |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts. | The ACE recovery point objective | IT lead with Operational Risk | Open, DL11 | All 19 services (value not set; CG-B-REQ-SPEC-28-1; ASM-B-REQ-SPEC-28-2) |
| NFR-023 | Recovery time objective: the maximum time to restore service. | The ACE recovery time objective | IT lead with Operational Risk | Open, DL11 | All 19 services (value not set; CG-B-REQ-SPEC-28-2; ASM-B-REQ-SPEC-28-3) |
| NFR-024 | An agent or model outage falls back to the rule result, and the case still routes. | Fallback always on | Solution architect | Proposed | P10 rwb-agent |
| NFR-025 | A system of record outage queues the outbound action and retries on a schedule, and does not lose it. | Queue and retry | Solution architect | Proposed | P2 rwb-integration (outbound_item) |
| NFR-026 | An interface failure after the retry limit moves the item to an exception queue with a task for a named owner. | Three retries per item, then the exception queue | Platform administrator | Proposed, DL11 | P2 rwb-integration (outbound_item); PLT (outbox, inbox and .dlt) |
| NFR-027 | A production release rolls back by redeploying the previous tag. | Rollback by previous tag | Solution architect | Proposed | PLT (service template and deployment) |
| NFR-071 | Documents in the hub are backed up on a stated schedule, and a restore is tested before the first production release and at each release after it. | Backup on the bank schedule; restore tested before the first production release and at each release | IT lead | Open, DL27 | P5 rwb-document (document, document_custody); PLT (Blob storage) |


## 3.5 Retention

ISO/IEC 25010: Security: accountability; compliance. Tested by: Set a short retention class in SIT and confirm expiry, hold and disposal behave as stated.

Realignment (D-RCV-60). Retention periods are not set (DL26). The 28 days in the source set is the Temporal Continue-As-New
interval, at each stage end and at least every 28 days (Recovery Workbench Temporal and Drools Design Text Extract v1, slide 13),
not a retention period; any "weeks" wording used for the same period is a conflict, recorded as CG-B-REQ-SPEC-28-3 with
ASM-B-REQ-SPEC-28-4. Retention stays with P5 rwb-document (retention_rule, retention_action), the decision log with P7
rwb-decision and the interaction ledger with P1 rwb-source-data.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Retention classes defined per type; periods not set | Compliance with Legal | Open, DL26 | P5 rwb-document (document_type, retention_rule) |
| NFR-029 | Legal documents are held in a write-once container and cannot be altered or deleted inside their retention period. | Write-once for legal types | Solution architect | Proposed | P5 rwb-document (Blob WORM) |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Log retention is set by Compliance | Compliance | Open, DL26 | P7 rwb-decision (decision_log_entry) |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Not set | Compliance | Open, DL26 | P3 rwb-case (recovery_case) |
| NFR-032 | Under D-RCV-35 (U5), retired local files and Excel and SharePoint trackers are handled through the Cutover and Go Live Plan, which keeps each as a read-only archive at a recorded location. The Workbench loads and holds no tracker. | Archive location recorded per file in the Cutover and Go Live Plan | Solution architect | Proposed | Not specified in the source documents (CG-B-REQ-SPEC-28-6; ASM-B-REQ-SPEC-28-7) |
| NFR-072 | A legal hold stops deletion and expiry for the case or document it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | Solution architect | Proposed | P3 rwb-case (POST /cases/{caseId}/legal-hold); P5 rwb-document |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Not set as a response time | Legal counsel | Open, DL26 | P5 rwb-document; P3 rwb-case |
| NFR-074 | A document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | Solution architect | Proposed | P5 rwb-document (retention_action) |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Not set | Compliance | Open, DL26 | P1 rwb-source-data (interaction) |


## 3.6 Auditability

ISO/IEC 25010: Security: accountability and non-repudiation. Tested by: Re-run a sample of decisions from the log and compare the result; hash chain check report.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-033 | Every decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | Solution architect | Proposed | P7 rwb-decision (decision_log_entry) |
| NFR-034 | Every action carries the rule version applied and the approver who allowed it. | Every action | Solution architect | Proposed | P7 rwb-decision (approval, rule_package_version) |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day. | Daily check, same-day report | Solution architect | Proposed | P7 rwb-decision |
| NFR-036 | An audit or regulatory request is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | Solution architect | Proposed | P7 rwb-decision; P5 rwb-document |
| NFR-037 | Quality assurance reaches first-time-right on case packs and write-off returns. | 90 percent | Solution architect | Proposed | P3 rwb-case; S7 rwb-writeoff |
| NFR-038 | Every outbound contact carries a conduct check result, and a contact without one is held. | Every contact | Solution architect | Proposed | P6 rwb-comms (notice) |
| NFR-076 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it, to the standard a court applies. | Every document produced | Solution architect | Proposed | P5 rwb-document (document, document_custody) |
| NFR-077 | A failed write to the interaction ledger raises an incident, and no entry is discarded. | No silent gaps | Solution architect | Proposed | P1 rwb-source-data (interaction) |
| NFR-078 | A model or agent write to a queue is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | Solution architect | Proposed | P10 rwb-agent (agent_run); P7 rwb-decision |


## 3.7 Data protection

ISO/IEC 25010: Security: confidentiality. Tested by: Role-based tests on masked fields; PDPA lint in the pipeline; review of the PII log.

Realignment (D-RCV-60). NFR-042 names a data lake copy. Architecture v5 has no data lake: reporting is built from events into
P9 rwb-reporting (DP-17; ADR-018). The requirement text is kept as written and the contradiction is recorded as
CG-B-REQ-SPEC-28-4 with ASM-B-REQ-SPEC-28-5; the logged reads are the P1, P5 and P7 reads named in the row.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-039 | Party identifiers are masked at rest in the case store, and on every screen and every agent call, by role. | Masked at rest and in use | Solution architect | Proposed | P4 rwb-access (masking_rule); P1 rwb-source-data (party_ext) |
| NFR-040 | Each screen and each agent receives only the personal data it needs. | Data minimization per screen and per agent | Solution architect | Proposed | P4 rwb-access; P10 rwb-agent |
| NFR-041 | The debt sale data tape is masked before it reaches the data room. | Masked tape | Solution architect | Proposed | S6 rwb-debtsale (debt_sale_account, data room) |
| NFR-042 | Every read of the case store, the document store and the data lake copy is logged. | Every read | Solution architect | Proposed | P1 rwb-source-data (data_product_access); P5 rwb-document; P7 rwb-decision |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period, Not set as a working service level | Compliance | Open, DL26 | P1 rwb-source-data (party_ext); P5 rwb-document |
| NFR-044 | Consent state per channel is held and applied, and statutory notices continue when consent is withdrawn. | Applied on every send | Solution architect | Proposed | P6 rwb-comms (notice) |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | Solution architect | Proposed | PLT (platform environments) |


## 3.8 Data residency and classification

ISO/IEC 25010: Security: confidentiality. Tested by: Architecture review of deployed resources; classification present on every data product.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-046 | Workbench data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | Solution architect | Proposed | PLT (platform, SCB Azure tenancy) |
| NFR-047 | Every data product and every document type carries a data classification, and the classification sets its handling. | Classification scheme to be applied | Compliance with Security | Open, DL26 | P1 rwb-source-data (data_product); P5 rwb-document (document_type) |
| NFR-048 | The approved large language model endpoint is reached over a private endpoint inside the bank's tenancy. | Private endpoint | Solution architect | Proposed | P10 rwb-agent (private endpoint) |


## 3.9 Security

ISO/IEC 25010: Security: authenticity and integrity. Tested by: Pipeline gates on every merge; penetration test; access tests per role.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Solution architect | Proposed | P4 rwb-access; PLT (ACE Common sign-in) |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Solution architect | Proposed | S9 rwb-partner; P4 rwb-access |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Solution architect | Proposed | P4 rwb-access |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Solution architect | Proposed | PLT (key store) |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Solution architect | Proposed | PLT (platform) |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Solution architect | Proposed | PLT (build pipeline) |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Solution architect | Proposed | P10 rwb-agent (agent_policy, guardrails) |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | SCB IT security with the IT lead | Proposed, DL11 | PLT (platform); SCB IT security |


## 3.10 Language

ISO/IEC 25010: Usability: operability. Tested by: UAT scripts in Thai and English.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-057 | Document text is read and extracted in Thai and in English. | Thai and English | Solution architect | Proposed | P5 rwb-document (document_text) |
| NFR-058 | Customer-facing documents and messages are produced in the customer's language. | Thai by default; English where the customer has chosen English | Legal counsel with Compliance | Proposed, DL10 | P6 rwb-comms (template, merge_field) |
| NFR-059 | Screen labels, validation messages and error messages are available in Thai and in English. | Every screen, label and message in Thai and English | Business lead | Proposed, DL10 | PLT (gateway-bff screens) |


## 3.11 Accessibility and devices

ISO/IEC 25010: Usability and compatibility. Tested by: Automated accessibility scan and a manual check on the main screens; browser and device test.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-060 | Screens meet the bank's accessibility standard. | WCAG 2.1 level AA for every screen | Tech leads with the ACE team | Proposed, DL11 | PLT (gateway-bff screens) |
| NFR-061 | Screens work on the browsers and versions the bank supports. | The current and previous major versions of Microsoft Edge and Google Chrome | IT lead | Proposed, DL11 | PLT (gateway-bff screens) |
| NFR-062 | The field application captures evidence with no network connection and uploads when it reconnects. | Offline capture | Solution architect | Proposed | PLT (gateway-bff screens) |
| NFR-063 | Partner-facing screens work on the devices partners actually use. | Desktop browsers as in NFR-061 and tablets for field and auction partners | Partner and agency manager | Proposed, DL11 | S9 rwb-partner; PLT (partner gateway) |


## 3.12 Observability

ISO/IEC 25010: Maintainability: analysability. Tested by: Inject a failure in SIT and confirm the alert reaches the named owner within the target.

| ID | Requirement | Target | Owner | Status | Owning service (Ownership Map v1) |
|---|---|---|---|---|---|
| NFR-064 | Logs, traces and metrics are produced across the workflow, the decision service and the agents. | Across all three | Solution architect | Proposed | PLT (observability); all 19 services |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count. | From the log | Solution architect | Proposed | P7 rwb-decision; P9 rwb-reporting (measure_definition) |
| NFR-066 | Agent acceptance, override rate, latency and cost are measured and reported. | Measured per agent | Solution architect | Proposed | P10 rwb-agent (agent_evaluation, agent_run); P9 rwb-reporting |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel. | Every job | Solution architect | Proposed | PLT (observability); the owner of each job |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target. | Alert within 15 minutes to the named owner | Platform administrator | Proposed, DL11 | PLT (observability) |


# 4. Partner access from outside the bank

| Item | Requirement |
|---|---|
| Route | Through the external gateway approved by the architecture team (DL03) |
| Identity | Partner identities separate from bank identities, with multi-factor authentication |
| Scope | Each partner user sees only the instructions placed with their firm |
| Lead time | One to three months from approval of the change |
| First needed | Valuers, auction vendors and RAMC at Epic 4; law firms and debt buyers at Epic 5; collection agencies at Epic 6 |
| Owner | Architecture team, with the partner and agency manager for onboarding |
| Test | Penetration test and a load test at 50 partner users online before the portal opens |
| Route in the target architecture | Staff through gateway-bff; partners through the partner gateway in the DMZ (FAPI 2.0), fronting S9 rwb-partner (Architecture v5 slides 8 and 10; ADR-019) |
| Owning service (Ownership Map v1) | S9 rwb-partner for partner, partner_user, partner_instruction and results; PLT for the partner gateway (Architecture v5 slides 8 and 17) |


# 5. Targets still to set

| ID | Requirement | Owner | Decision | Owning service (Ownership Map v1) |
|---|---|---|---|---|
| NFR-022 | Recovery point objective: the maximum data loss the business accepts. | IT lead with Operational Risk | DL11 | All 19 services (value not set; CG-B-REQ-SPEC-28-1; ASM-B-REQ-SPEC-28-2) |
| NFR-023 | Recovery time objective: the maximum time to restore service. | IT lead with Operational Risk | DL11 | All 19 services (value not set; CG-B-REQ-SPEC-28-2; ASM-B-REQ-SPEC-28-3) |
| NFR-071 | Documents in the hub are backed up on a stated schedule, and a restore is tested before the first production release and at each release after it. | IT lead | DL27 | P5 rwb-document (document, document_custody); PLT (Blob storage) |
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Compliance with Legal | DL26 | P5 rwb-document (document_type, retention_rule) |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Compliance | DL26 | P7 rwb-decision (decision_log_entry) |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Compliance | DL26 | P3 rwb-case (recovery_case) |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Legal counsel | DL26 | P5 rwb-document; P3 rwb-case |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Compliance | DL26 | P1 rwb-source-data (interaction) |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Compliance | DL26 | P1 rwb-source-data (party_ext); P5 rwb-document |
| NFR-047 | Every data product and every document type carries a data classification, and the classification sets its handling. | Compliance with Security | DL26 | P1 rwb-source-data (data_product); P5 rwb-document (document_type) |


# 6. Realignment record (D-RCV-60)

## 6.1 What version 4 changes

Version 4 keeps every section, requirement ID, number and date of version 3. The changes are these, and nothing else.

- An owning service cell is added to every target and requirement table, from the Microservice Ownership Map v1; no source cell is rewritten (ASM-B-REQ-SPEC-28-9).
- Section 3.2 states the one-hop REST rule and the 2 s call timeout of Architecture v5, and NFR-079 and NFR-080 are added (78 requirements in version 3, 80 here).
- Section 3.3 states that only P1 rwb-source-data reads the 30 recovery.v_ace_* views.
- Section 3.4 records that the recovery point and recovery time objectives are not stated for the 19 services (CG-B-REQ-SPEC-28-1 and CG-B-REQ-SPEC-28-2).
- Section 3.5 records the 'weeks' versus '28 days' wording (CG-B-REQ-SPEC-28-3).
- Section 3.7 records the data lake copy named by NFR-042 against Architecture v5 (CG-B-REQ-SPEC-28-4).
- Section 2 keeps the concurrency figures and records their difference from Architecture v5 slide 48 (CG-B-REQ-SPEC-28-5).
- Section 4 records the partner gateway of ADR-019 and the owning service.
- No release date is named by this document; the version 3 date of 15 November 2026 is kept, and every release date named elsewhere in the programme stays tentative (U7; DL48; ASM-B-REQ-SPEC-28-8).

## 6.2 The realigned targets

| Item | Value | Source |
|---|---|---|
| REST hop | One hop from gateway-bff to the owning service, and no call chain deeper than one in any service | Recovery Workbench Architecture v5 Text Extract v1, slide 11 |
| REST call timeout | 2 s per call; GET retried once with jitter; circuit breaker and bulkhead per downstream; RFC 9457 problem details | Architecture v5, slide 11; ADR-020 |
| Composite screen budget | Gateway and session 0.15 s, slowest parallel call 0.6 s, merge 0.3 s: about 1.05 s, planned at about 1.2 s, against the 2 s target at the 95th percentile | Architecture v5, slide 10; NFR-008, NFR-009 |
| ACE data reads | Only P1 rwb-source-data reads the 30 recovery.v_ace_* views, with a read-only login and a statement timeout; every other service reads P1's contract | Architecture v5, slides 9 and 11; DP-05 |
| Agent fallback | 60 s, then the rule result and the case still routes | Architecture v5, slide 16; NFR-010, NFR-024 |
| Partner route | Partner gateway (FAPI 2.0) in the DMZ, fronting S9 rwb-partner; staff through gateway-bff | Architecture v5, slide 8; ADR-019 |
| Decisions | D-RCV-60; ADR-013 to ADR-023; DL44 to DL49 | ids.json; Template and Rules R8.4 |
| Story coverage | RWB-PLT-NF01-OPS, RWB-PLT-NF02-APP, RWB-PLT-NF03-OPS, RWB-PLT-NF04-OPS, RWB-PLT-NF05-OPS, RWB-PLT-NF06-DB, RWB-PLT-NF07-INF and RWB-PLT-NF08-INF carry the non-functional work in wave 0 | split plan, legacy rows NF-01 to NF-08 |

## 6.3 Requirements by owning service

Built from the owning service cell of every requirement table, in the order of this document.

| Service | Requirements |
|---|---|
| P1 rwb-source-data | NFR-070, NFR-013, NFR-014, NFR-015, NFR-018, NFR-075, NFR-077, NFR-039, NFR-042, NFR-043, NFR-047 |
| P2 rwb-integration | NFR-021, NFR-025, NFR-026 |
| P3 rwb-case | NFR-001, NFR-009, NFR-012, NFR-018, NFR-019, NFR-031, NFR-072, NFR-073, NFR-037 |
| P4 rwb-access | NFR-002, NFR-039, NFR-040, NFR-049, NFR-050, NFR-051 |
| P5 rwb-document | NFR-004, NFR-069, NFR-009, NFR-012, NFR-016, NFR-017, NFR-071, NFR-028, NFR-029, NFR-072, NFR-073, NFR-074, NFR-036, NFR-076, NFR-042, NFR-043, NFR-047, NFR-057 |
| P6 rwb-comms | NFR-021, NFR-038, NFR-044, NFR-058 |
| P7 rwb-decision | NFR-007, NFR-011, NFR-030, NFR-033, NFR-034, NFR-035, NFR-036, NFR-078, NFR-042, NFR-065 |
| P8 rwb-payment | None |
| P9 rwb-reporting | NFR-065, NFR-066 |
| P10 rwb-agent | NFR-010, NFR-017, NFR-024, NFR-078, NFR-040, NFR-048, NFR-055, NFR-066 |
| S1 rwb-valuation | None |
| S2 rwb-treatment | NFR-005, NFR-006 |
| S3 rwb-guarantee | None |
| S4 rwb-litigation | None |
| S5 rwb-asset | None |
| S6 rwb-debtsale | NFR-041 |
| S7 rwb-writeoff | NFR-037 |
| S8 rwb-deviation | None |
| S9 rwb-partner | NFR-003, NFR-050, NFR-063 |
| PLT platform | NFR-002, NFR-008, NFR-020, NFR-026, NFR-027, NFR-071, NFR-045, NFR-046, NFR-049, NFR-052, NFR-053, NFR-054, NFR-056, NFR-059, NFR-060, NFR-061, NFR-062, NFR-063, NFR-064, NFR-067, NFR-068, NFR-079, NFR-080 |

## 6.4 Gap rows raised by this version

| ID | Title | Type | Severity | Owner role |
|---|---|---|---|---|
| CG-B-REQ-SPEC-28-1 | Recovery point objective not stated for the 19 services | Missing | P1 | IT lead with Operational Risk |
| CG-B-REQ-SPEC-28-2 | Recovery time objective not stated for the 19 services | Missing | P1 | IT lead with Operational Risk |
| CG-B-REQ-SPEC-28-3 | 'Weeks' versus '28 days' wording for the same period | Conflict | P2 | Business analyst |
| CG-B-REQ-SPEC-28-4 | NFR-042 logs reads of a data lake copy that Architecture v5 removes | Conflict | P3 | Solution architect |
| CG-B-REQ-SPEC-28-5 | Concurrency and named-user figures disagree between section 2, NFR-002/NFR-003 and Architecture v5 | Conflict | P2 | Business lead |
| CG-B-REQ-SPEC-28-6 | Owning service not derivable from the Ownership Map for NFR-032 | Missing | P3 | Solution architect |

Numbering is left to step D1 (Template and Rules R9); the ids here are the work-package ids.

## 6.5 Assumption rows raised by this version

| ID | Assumption | Confidence |
|---|---|---|
| ASM-B-REQ-SPEC-28-1 | The specification is issued as Draft version 4. No review or approval of any version is recorded, and this run takes no human approval step. | High |
| ASM-B-REQ-SPEC-28-2 | Until the recovery point objective is confirmed, no RPO value is tested; NFR-022 stays Open under DL11 and recovery testing uses the ACE platform tier. | Low |
| ASM-B-REQ-SPEC-28-3 | Until the recovery time objective is confirmed, no RTO value is tested; NFR-023 stays Open under DL11 and recovery testing uses the ACE platform tier. | Low |
| ASM-B-REQ-SPEC-28-4 | The 28 days is read only as the Temporal Continue-As-New interval; no retention period is 28 days and every retention period stays Not set under DL26. | Medium |
| ASM-B-REQ-SPEC-28-5 | The data lake copy named by NFR-042 is read as removed (DP-17, ADR-018); the logged reads are the P1, P5 and P7 reads, and no lake copy is built. | Medium |
| ASM-B-REQ-SPEC-28-6 | Where the concurrency figures differ, Architecture v5 slide 48 (414 staff, 48 partners) is used for the load test; the requirement text stays as written. | Medium |
| ASM-B-REQ-SPEC-28-7 | The archive location of NFR-032 is recorded per file in the Cutover and Go Live Plan; no single service owns it until that plan names one. | Medium |
| ASM-B-REQ-SPEC-28-8 | Every date of the source is copied unchanged and every release date named anywhere is tentative; this document names no release date of its own. | High |
| ASM-B-REQ-SPEC-28-9 | The version 4 change is additive: an owning service cell per row, the section notes, NFR-079 and NFR-080, two section 4 rows and section 6. PLT is used for the items the Ownership Map leaves to the platform, and no source cell is rewritten. | High |

## 6.6 Sources read for version 4

| Source | Used for |
|---|---|
| 03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx (and its text extract) | Every section, requirement and number kept |
| 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (slides 8 to 11, 16, 48) | One-hop REST, the 2 s timeout, the screen budget, the ACE read rule, RPO and RTO, the partner gateway |
| 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md (slide 13) | The 28 days Continue-As-New interval |
| 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx and _work/msr/plan/ownership.json | The owning service of every requirement |
| 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (R1, R3, R5, R8, R9) | Header, change log, DP table, gaps and assumptions |
| _work/msr/plan/ids.json and _work/msr/plan/split_plan.json (stats and legacy) | Decision ids and the NF-01 to NF-08 story coverage |
