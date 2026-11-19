<!-- source: 03 Requirements and specifications/Recovery Workbench Non Functional Specification v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Non Functional Specification v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Non-functional specification

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench non-functional specification |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC 25010 quality characteristics |
| Requirements | 78 |

# 1. Targets on one page

| Area | Main target | Status |
|---|---|---|
| Volume | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month | Sized; DL15 |
| Users | About 370 staff and 50 partner users online in the busiest hour; 1,234 named users | Proposed |
| Screens | Under 2 seconds at the 95th percentile at the busiest-hour load | Proposed, DL11 |
| Agents | Answer within 60 seconds; after that the rule result is used | Proposed, DL11 |
| Loads | COLLINS load complete by 07:00; case list reconciled to the core bank every day | Proposed |
| Availability | 99.9 percent in business hours; recovery point and time as set for ACE | Proposed; open DL11 |
| Storage | About 5.8 million documents and 2.8 TB by the end of 2031; about 36 GB of decision log and ledger | Proposed |
| Audit | Every decision reproducible from the log with its rule, model and prompt versions | Proposed |
| Security | Single sign-on with multi-factor authentication; masking by role; no secrets in code | Proposed |
| Partners | Partner access from outside the bank through the external gateway | Open, DL03 |

Each requirement has a measure, the test that proves it and an owner. A requirement marked Proposed is built and tested against the value shown until the owner confirms it under the decision named.

# 2. Volumes and concurrency

| Measure | Value | Basis |
|---|---|---|
| Accounts at 90 days past due, active inventory | 28,119 | Mortgage 12,256; hire purchase 12,960; SSME 2,903 at 30 June 2026 |
| New accounts at 90 days past due a month | 3,110 | Average of the last 12 months |
| Open cases at go-live | About 23,600 | 1.2 accounts per case (DL17) |
| Open cases at the end of 2027 | About 26,500 | 15 percent inflow growth a year (DL15) |
| Named users | 1,234 | 466 recovery staff, 448 collections staff reading the case record, 320 partner users |
| Online in the busiest hour | About 410 | 40 percent of bank users and 15 percent of partner users |
| Requests a second in the busiest hour | About 21 | Three requests a minute for each active user |
| Documents held at the end of 2031 | About 5.8 million | 15 per new case and one per open case each month |
| Hire purchase accounts outside the active inventory | 156,351 | Loaded once as case history |

# 3. Requirements by quality characteristic

## 3.1 Volume and capacity

ISO/IEC 25010: Performance efficiency: capacity. Tested by: Load test in SIT with data at the stated volume; query times read at that size.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. Confirmed under DL15 | Risk with the data product owner | Proposed from the volume forecast |
| NFR-002 | The system supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | Business lead | Proposed from the volume forecast |
| NFR-003 | The system supports the peak number of partner users signed on at once across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour, of about 320 named users | Partner and agency manager | Proposed from the volume forecast |
| NFR-004 | The document store holds the annual inbound document volume with its growth rate. | About 860,000 documents in 2027, rising with 15 percent inflow growth a year | Legal with Autonomous Ops | Proposed from the volume forecast |
| NFR-005 | The restructure path carries the monthly case volume reaching the Workbench. | About 3,000 restructure accounts a month reach the bank's restructure process today | Solution architect | Proposed |
| NFR-006 | The deed in lieu path carries its target monthly volume. | 1,000 cases a month in 2027, from 685 today | Solution architect | Proposed |
| NFR-007 | The decision log holds one record for every decision on every case for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | Compliance with the solution architect | Proposed, DL11 |
| NFR-069 | The document hub holds the full recovery document estate as a system of record, including every version and every held document, with storage sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031, with every version and held document | Solution architect with Compliance | Proposed, DL11 |
| NFR-070 | The interaction ledger holds every interaction on every open and closed case within its retention period, and reads a single case history inside the user wait. | One case history reads in under 2 seconds with the ledger at its 2031 size | Data lead with the solution architect | Proposed, DL11 |

## 3.2 Response time

ISO/IEC 25010: Performance efficiency: time behavior. Tested by: Performance test in SIT at the busiest-hour load; 95th percentile read from the traces.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-008 | A screen responds within its target under normal load. | Under 2 seconds | Solution architect | Proposed |
| NFR-009 | The case record view loads for a case with 50 documents. | Under 2 seconds | Solution architect | Proposed |
| NFR-010 | An agent returns an answer within its target, after which the rule result is used and the case still routes. | Under 60 seconds | Solution architect | Proposed |
| NFR-011 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | Solution architect | Proposed, DL11 |
| NFR-012 | A search across cases and documents returns within its target. | Under 3 seconds for a search across cases; under 5 seconds across documents | Business lead | Proposed, DL11 |

## 3.3 Loads and batch

ISO/IEC 25010: Performance efficiency and reliability. Tested by: Run the load in SIT with a full-size file; time and result read from the job monitor.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-013 | The daily core system load completes before the working day starts, and a failure raises an alert. | Job runs by 07:00 | Solution architect | Proposed |
| NFR-014 | Collections data is ingested at start of day. | Start of day | Solution architect | Proposed |
| NFR-015 | The recovery data store is no more than the agreed lag behind its sources, and a decision that must be made the same day uses an event instead. | End of day; in the Workbench the next morning. Same-day needs are named under DL06 | Solution architect | Proposed |
| NFR-016 | The document intake pipeline processes its throughput in the test environment. | 500 pages per hour | Solution architect | Proposed |
| NFR-017 | Document classification is correct on the labeled sample, and anything below the confidence threshold goes to a review queue. | 90 percent correct | Solution architect | Proposed |
| NFR-018 | The case list reconciles to the core system count daily. | No unexplained variance; tolerance per data product under DL25 | Solution architect | Proposed, DL25 |
| NFR-019 | The daily rebalancing job completes before the working day starts. | Complete by 07:00 | Team manager | Proposed, DL11 |

## 3.4 Availability and recovery

ISO/IEC 25010: Reliability: availability and recoverability. Tested by: Failover and restore test before the first production release; availability read monthly from monitoring.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-020 | The Workbench is available during business hours. | 99.9 percent in business hours | Solution architect | Proposed |
| NFR-021 | Availability outside business hours, when batch, dispatch and partner exchange run. | 99.5 percent outside business hours, excluding the change window | IT lead | Proposed, DL11 |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts. | The ACE recovery point objective | IT lead with Operational Risk | Open, DL11 |
| NFR-023 | Recovery time objective: the maximum time to restore service. | The ACE recovery time objective | IT lead with Operational Risk | Open, DL11 |
| NFR-024 | An agent or model outage falls back to the rule result, and the case still routes. | Fallback always on | Solution architect | Proposed |
| NFR-025 | A system of record outage queues the outbound action and retries on a schedule, and does not lose it. | Queue and retry | Solution architect | Proposed |
| NFR-026 | An interface failure after the retry limit moves the item to an exception queue with a task for a named owner. | Three retries per item, then the exception queue | Platform administrator | Proposed, DL11 |
| NFR-027 | A production release rolls back by redeploying the previous tag. | Rollback by previous tag | Solution architect | Proposed |
| NFR-071 | Documents in the hub are backed up on a stated schedule, and a restore is tested before the first production release and at each release after it. | Backup on the bank schedule; restore tested before the first production release and at each release | IT lead | Open, DL27 |

## 3.5 Retention

ISO/IEC 25010: Security: accountability; compliance. Tested by: Set a short retention class in SIT and confirm expiry, hold and disposal behave as stated.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Retention classes defined per type; periods not set | Compliance with Legal | Open, DL26 |
| NFR-029 | Legal documents are held in a write-once container and cannot be altered or deleted inside their retention period. | Write-once for legal types | Solution architect | Proposed |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Log retention is set by Compliance | Compliance | Open, DL26 |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Not set | Compliance | Open, DL26 |
| NFR-032 | A retired local file is kept as a read-only archive at a recorded location. | Archive location recorded per file | Solution architect | Proposed |
| NFR-072 | A legal hold stops deletion and expiry for the case or document it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | Solution architect | Proposed |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Not set as a response time | Legal counsel | Open, DL26 |
| NFR-074 | A document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | Solution architect | Proposed |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Not set | Compliance | Open, DL26 |

## 3.6 Auditability

ISO/IEC 25010: Security: accountability and non-repudiation. Tested by: Re-run a sample of decisions from the log and compare the result; hash chain check report.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-033 | Every decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | Solution architect | Proposed |
| NFR-034 | Every action carries the rule version applied and the approver who allowed it. | Every action | Solution architect | Proposed |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day. | Daily check, same-day report | Solution architect | Proposed |
| NFR-036 | An audit or regulatory request is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | Solution architect | Proposed |
| NFR-037 | Quality assurance reaches first-time-right on case packs and write-off returns. | 90 percent | Solution architect | Proposed |
| NFR-038 | Every outbound contact carries a conduct check result, and a contact without one is held. | Every contact | Solution architect | Proposed |
| NFR-076 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it, to the standard a court applies. | Every document produced | Solution architect | Proposed |
| NFR-077 | A failed write to the interaction ledger raises an incident, and no entry is discarded. | No silent gaps | Solution architect | Proposed |
| NFR-078 | A model or agent write to a queue is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | Solution architect | Proposed |

## 3.7 Data protection

ISO/IEC 25010: Security: confidentiality. Tested by: Role-based tests on masked fields; PDPA lint in the pipeline; review of the PII log.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-039 | Party identifiers are masked at rest in the case store, and on every screen and every agent call, by role. | Masked at rest and in use | Solution architect | Proposed |
| NFR-040 | Each screen and each agent receives only the personal data it needs. | Data minimization per screen and per agent | Solution architect | Proposed |
| NFR-041 | The debt sale data tape is masked before it reaches the data room. | Masked tape | Solution architect | Proposed |
| NFR-042 | Every read of the case store, the document store and the data lake copy is logged. | Every read | Solution architect | Proposed |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period, Not set as a working service level | Compliance | Open, DL26 |
| NFR-044 | Consent state per channel is held and applied, and statutory notices continue when consent is withdrawn. | Applied on every send | Solution architect | Proposed |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | Solution architect | Proposed |

## 3.8 Data residency and classification

ISO/IEC 25010: Security: confidentiality. Tested by: Architecture review of deployed resources; classification present on every data product.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-046 | Workbench data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | Solution architect | Proposed |
| NFR-047 | Every data product and every document type carries a data classification, and the classification sets its handling. | Classification scheme to be applied | Compliance with Security | Open, DL26 |
| NFR-048 | The approved large language model endpoint is reached over a private endpoint inside the bank's tenancy. | Private endpoint | Solution architect | Proposed |

## 3.9 Security

ISO/IEC 25010: Security: authenticity and integrity. Tested by: Pipeline gates on every merge; penetration test; access tests per role.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Solution architect | Proposed |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Solution architect | Proposed |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Solution architect | Proposed |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Solution architect | Proposed |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Solution architect | Proposed |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Solution architect | Proposed |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Solution architect | Proposed |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | SCB IT security with the IT lead | Proposed, DL11 |

## 3.10 Language

ISO/IEC 25010: Usability: operability. Tested by: UAT scripts in Thai and English.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-057 | Document text is read and extracted in Thai and in English. | Thai and English | Solution architect | Proposed |
| NFR-058 | Customer-facing documents and messages are produced in the customer's language. | Thai by default; English where the customer has chosen English | Legal counsel with Compliance | Proposed, DL10 |
| NFR-059 | Screen labels, validation messages and error messages are available in Thai and in English. | Every screen, label and message in Thai and English | Business lead | Proposed, DL10 |

## 3.11 Accessibility and devices

ISO/IEC 25010: Usability and compatibility. Tested by: Automated accessibility scan and a manual check on the main screens; browser and device test.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-060 | Screens meet the bank's accessibility standard. | WCAG 2.1 level AA for every screen | Tech leads with the ACE team | Proposed, DL11 |
| NFR-061 | Screens work on the browsers and versions the bank supports. | The current and previous major versions of Microsoft Edge and Google Chrome | IT lead | Proposed, DL11 |
| NFR-062 | The field application captures evidence with no network connection and uploads when it reconnects. | Offline capture | Solution architect | Proposed |
| NFR-063 | Partner-facing screens work on the devices partners actually use. | Desktop browsers as in NFR-061 and tablets for field and auction partners | Partner and agency manager | Proposed, DL11 |

## 3.12 Observability

ISO/IEC 25010: Maintainability: analysability. Tested by: Inject a failure in SIT and confirm the alert reaches the named owner within the target.

| ID | Requirement | Target | Owner | Status |
|---|---|---|---|---|
| NFR-064 | Logs, traces and metrics are produced across the workflow, the decision service and the agents. | Across all three | Solution architect | Proposed |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count. | From the log | Solution architect | Proposed |
| NFR-066 | Agent acceptance, override rate, latency and cost are measured and reported. | Measured per agent | Solution architect | Proposed |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel. | Every job | Solution architect | Proposed |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target. | Alert within 15 minutes to the named owner | Platform administrator | Proposed, DL11 |

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

# 5. Targets still to set

| ID | Requirement | Owner | Decision |
|---|---|---|---|
| NFR-022 | Recovery point objective: the maximum data loss the business accepts. | IT lead with Operational Risk | DL11 |
| NFR-023 | Recovery time objective: the maximum time to restore service. | IT lead with Operational Risk | DL11 |
| NFR-071 | Documents in the hub are backed up on a stated schedule, and a restore is tested before the first production release and at each release after it. | IT lead | DL27 |
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Compliance with Legal | DL26 |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Compliance | DL26 |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Compliance | DL26 |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Legal counsel | DL26 |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Compliance | DL26 |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Compliance | DL26 |
| NFR-047 | Every data product and every document type carries a data classification, and the classification sets its handling. | Compliance with Security | DL26 |
