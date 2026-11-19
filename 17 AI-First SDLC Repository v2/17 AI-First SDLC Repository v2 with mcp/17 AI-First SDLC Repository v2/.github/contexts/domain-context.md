# Recovery Workbench — domain context

**Context ID:** `CTX-DOMAIN-RWB-V2`
**Version:** 2.0, 16 November 2026
**Purpose:** supplemental banking, recovery and platform vocabulary. Business requirements and rules
stay in `project-context.md`; this file explains the terms.

## 1. The bank and the recovery domain

| Term | Meaning |
|---|---|
| SCB | Siam Commercial Bank. The Workbench is built for SCB Collections and Recovery. |
| Collections | The pre-90-DPD collection process, owned by ACE's collection module. |
| Recovery | The post-90-DPD process: restructure, legal, asset sale, debt sale, write-off, recovery. |
| DPD | Days past due. The entry point for recovery is 90 DPD. |
| Arrears | The unpaid amount due; principal, interest, fees and charges. |
| NPA | Non-performing asset; a loan or asset classified as unlikely to be collected. |
| TDR | Troubled debt restructuring; a change to the terms of a loan for a distressed borrower. |
| Deed in lieu | The borrower transfers the asset to the bank instead of foreclosure. |
| Write-off | Removing an uncollectible amount from the books, with recovery still pursued. |
| Debt sale | Selling a portfolio of defaulted debt to a buyer. |
| Legal action | Litigation, enforcement, bankruptcy and judgement execution. |
| Guarantee | A third party's promise to pay the borrower's debt; a guarantor is the person. |
| Collateral | An asset pledged as security; valuation and custody are tracked. |
| Proof of delivery | Evidence that a notice or letter reached the customer. |
| Prescription date | The date a legal claim may expire under Thai law. |
| Restructure | A change to repayment terms: extension, rate, grace period, capitalisation. |
| Settlement | A negotiated final payment less than the outstanding balance. |
| DoA | Delegation of authority; the approval limit and level for a role. |
| RW-COE | Central operations / centre of excellence; authors rules and reference data. |
| RW-RISK | Risk function; approves rule packages and high-risk treatments. |
| RW-PLATADM | Platform administrator; operates Temporal and the flags. |
| RW-SECADM | Security administrator; break-glass decode of Temporal payloads. |

## 2. Products and portfolio

| Term | Meaning |
|---|---|
| Mortgage | Home loan secured by property. |
| HP | Hire purchase, typically a vehicle. |
| SSME | Small and small-medium enterprise lending. |
| Product group | The product family that drives the route, rules and queue. |
| Segment | Customer risk/value segment used in assignment and prioritisation. |
| Bucket | The arrears bucket (1–30, 31–60, 61–90, 90+ DPD). |
| Route | The recovery path chosen for a case: restructure, legal, asset sale, debt sale, write-off. |

## 3. Case and workflow vocabulary (CMMN 1.1)

| Term | Meaning |
|---|---|
| Case | One recovery matter for one customer and product, from 90 DPD to close. |
| Stage | A major phase of the case (entry, assessment, treatment, legal, closure). |
| Milestone | A measurable point in a stage. |
| Task | A unit of work assigned to a person, partner or system. |
| Sentry | A condition that enables or terminates a task or stage. |
| Event listener | A reaction to an external event. |
| Case file item | A document or data item attached to the case. |
| Timer | A due date or interval that triggers an action. |
| Queue | The work list that owns a case before an officer is assigned. |
| Assignment | The link between a case and its owner. |
| Transfer | A move of a case between queues or owners, with a reason. |
| Rebalancing | A daily move of cases to balance queue load. |

## 4. Systems and platforms

| Term | Meaning |
|---|---|
| ACE | The bank's collections engine; the Workbench is its recovery module. |
| COLLINS | The bank's collections data platform; historically the inbound source. Under D-RCV-35 ACE ingests source data, and the Workbench reads ACE views. |
| ASS | Auto-debit / account servicing system for payments. |
| ALS | Account and loan system; account and arrears data. |
| EFS | Field servicing / asset visit system. |
| CCMS | Collateral and custody management system. |
| SVAF | Security valuation and asset finance. |
| AMIS | Asset management / NPA system. |
| RPS | Repossession system. |
| LIT | Legal case management system. |
| WIN | Document delivery / proof-of-delivery provider. |
| NLEADS | Credit decision system. |
| EasyApp | E-signature platform. |
| SCBPDM | Party and customer master data. |
| NSS | Notification service. |
| LINE OA | LINE official account messaging. |
| Entra ID | Microsoft identity provider used for SSO and MFA. |
| AKS | Azure Kubernetes Service; the ACE clusters. |
| Blob | Azure Blob storage for documents. |
| Key Vault | Azure key management for the payload codec. |

## 5. Architecture vocabulary

| Term | Meaning |
|---|---|
| Modular monolith | One deployable service with modules checked at build time (ADR-002). |
| Spring Modulith | The module verification library used for BND-3. |
| ArchUnit | The test library used for BND-1, BND-2, BND-4, BND-5, BND-6. |
| Flyway | The migration tool; one history table per module. |
| Temporal | The durable workflow engine; one workflow per case from Epic 3. |
| Task queue | A Temporal queue that a worker polls. |
| Activity | A Temporal unit that performs I/O; the only place rules are evaluated. |
| Determinism | Workflow code must replay to the same result; no clock, random or I/O. |
| Drools | The embedded rules engine; XLS decision tables compiled to a KieBase. |
| KieBase | The compiled rule package held in memory. |
| Rule package | A versioned row with workbook, generated DRL, checksum and valid-from date. |
| Decision table | A Drools XLS workbook with RuleSet, RuleTable, condition and action columns. |
| Salience | Rule priority derived from row order; the default row is last. |
| Outbox | A table of pending outbound side effects, retried by a job. |
| Idempotency key | A client key that makes a command safe to retry. |
| Feature flag | A switch that returns the previous path when off. |
| PDPA | Thailand's Personal Data Protection Act. |
| PII | Personally identifiable information. |
| Masking | Replacing personal data with a role-appropriate masked value. |
| Hash chain | Each decision-log entry includes the hash of the previous entry. |

## 6. Data vocabulary

| Term | Meaning |
|---|---|
| Data product | One of the 14 Epic 1 data products (account, payment, customer, etc.). |
| Tier 1 | ACE tables that exist today, read through 16 views. |
| Tier 2 | 14 ACE tables and 12 columns added by RWB-ACE-001, read through 14 views. |
| Extension table | A Workbench 1:1 table keyed by an ACE business key. |
| Business key | The ACE key used to link a recovery row to a source record; no FK to `public`. |
| Data dictionary | `sys_objects` and `sys_fields` rows that describe every object and field. |
| Reference data | Versioned lists of values: roles, queues, document types, checklists, parameters. |
| Parameter | A named, typed, owned value with a default, range and environment. |
| Freshness stamp | The business date and load time of the data a case decision used. |
| Reconciliation | The daily comparison of source counts and totals with the Workbench view. |
| Interaction ledger | An append-only record of every Workbench action. |

## 7. Regulatory and control vocabulary

| Term | Meaning |
|---|---|
| BOT | Bank of Thailand; the regulator. |
| PDPA | Personal Data Protection Act B.E. 2562 (2019). |
| AML/CFT | Anti-money laundering and counter-financing of terrorism. |
| Model risk | The risk that a model or rule produces a wrong or unfair outcome. |
| Maker-checker | One person prepares, another approves. |
| Break-glass | Time-boxed emergency access, logged and reviewed. |
| Legal hold | A instruction to preserve documents for litigation or investigation. |
| E-discovery | The process of finding and producing documents for legal proceedings. |
| Retention class | The period and disposal rule for a document type. |
| Audit trail | The evidence that every action, rule and approver is recorded. |

## 8. Source register

| Term source | Version |
|---|---|
| Business Glossary | v3 |
| Users, Roles and Permissions | v4 |
| Target Operating Model | v3 |
| Partner Operating Model | v2 |
| Physical Schema | v6 |
| Logical Data Model and Data Dictionary | v8 |
| ACE DB Alignment Change Register | v1 |
| Temporal and Drools Change Register | v1 |
| Error and Message Standard | v4 |

## 9. Required guidance

Use these terms in class, field, table and endpoint names. Do not invent a synonym when a glossary
term exists. If a term is missing, record it as an open item for the Context Updater; do not add a new
business fact to this file.

## 10. N/A and evidence scope

- N/A — no direct customer-facing mobile app; the Workbench is a web module in the ACE front end.
- N/A — no non-banking industry vocabulary; the domain is SCB retail and SME recovery.
