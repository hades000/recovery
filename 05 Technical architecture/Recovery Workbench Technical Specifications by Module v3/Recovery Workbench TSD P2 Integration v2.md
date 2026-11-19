# Recovery Workbench P2 Integration

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P2 Integration |
| Document ID | P2-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P2 Integration | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | NEW | Error Handling and Resilience Standard | Built in P2 for the recovery module |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

## T1. Architecture overview

P2 Integration is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: file adapters, outbound files, use of the ACE integration paths. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| IntegrationController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| IntegrationService | Business logic; calls the rules component; writes the decision log entry before any change |
| IntegrationRepository | Reads and writes the module's tables only |
| Jobs | Quartz and Spring Batch jobs the module owns |
| Published interface | Java interface other modules call; no table is read across modules |

## T3. Data model

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

**interface_config** (NEW). The settings of one file interface, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-136 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-137 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-138 | direction | LOV | varchar(8) | Yes | LOV-DIRECTION | Workbench |
| DF-OPS-139 | transport | LOV | varchar(10) | Yes | LOV-TRANSPORT | Workbench |
| DF-OPS-140 | inbound_path | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-141 | file_pattern | TEXT | varchar(120) | No | None | Workbench |
| DF-OPS-142 | data_product | LOV | varchar(25) | No | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-143 | max_attempts | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-144 | retry_intervals_min | TEXT | varchar(60) | No | None | Workbench |
| DF-OPS-145 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-OPS-146 | alert_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-OPS-147 | valid_from | DATE | date | Yes | None | Workbench |
| DF-OPS-148 | valid_to | DATE | date | No | None | Workbench |

**interface_run** (NEW). One inbound file received by the adapter and the result of its file checks.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-149 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-150 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-151 | file_name | TEXT | varchar(200) | Yes | None | Workbench |
| DF-OPS-152 | file_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-OPS-153 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-154 | record_count | NUMBER | integer | No | None | Workbench |
| DF-OPS-155 | control_total | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-OPS-156 | status | LOV | varchar(12) | Yes | LOV-INTERFACE-RUN | Workbench |
| DF-OPS-157 | failed_check | TEXT | varchar(40) | No | None | Workbench |
| DF-OPS-158 | checks | TEXT | jsonb | No | None | Workbench |
| DF-OPS-159 | started_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-160 | ended_at | DATE | timestamptz | No | None | Workbench |

**interface_signoff** (NEW). The data steward's sign-off that an interface no longer needs manual handling.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-161 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-162 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-163 | from_date | DATE | date | Yes | None | Workbench |
| DF-OPS-164 | to_date | DATE | date | Yes | None | Workbench |
| DF-OPS-165 | clean_days | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-166 | signed_by | USER_REF | uuid | Yes | None | Workbench |
| DF-OPS-167 | signed_at | DATE | timestamptz | Yes | None | Workbench |

**outbound_item** (NEW). One outbound file waiting to be sent, sent or in the exception queue.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-168 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-169 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-170 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-171 | payload_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-OPS-172 | case_ids | TEXT | jsonb | No | None | Workbench |
| DF-OPS-173 | attempt_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-174 | next_attempt_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-175 | status | LOV | varchar(12) | Yes | LOV-OUTBOUND-STATUS | Workbench |
| DF-OPS-176 | last_error | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-177 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |

**processed_event** (NEW). An event or work key a consumer has already processed, so a repeat is ignored and counted.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-178 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-179 | consumer | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-180 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-181 | event_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-182 | hit_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-183 | last_seen_at | DATE | timestamptz | No | None | Workbench |

**idempotency_key** (NEW). The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-184 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-185 | idempotency_key | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-186 | endpoint | TEXT | varchar(100) | Yes | None | Workbench |
| DF-OPS-187 | request_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-OPS-188 | response | TEXT | jsonb | Yes | None | Workbench |

**outbox_event** (NEW). An application event or outbound work request written in the same transaction as the change.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-189 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-190 | event_type | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-191 | schema_version | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-192 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-193 | case_seq | NUMBER | bigint | No | None | Workbench |
| DF-OPS-194 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-195 | payload | TEXT | jsonb | Yes | None | Workbench |
| DF-OPS-196 | actor_ref | TEXT | varchar(64) | No | None | Workbench |
| DF-OPS-197 | occurred_at | DATE | timestamptz | Yes | None | Workbench |

**outbox_delivery** (NEW). The delivery of one outbox event to one consumer, with its retries.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-198 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-199 | event_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-OPS-200 | consumer | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-201 | status | LOV | varchar(12) | Yes | LOV-OUTBOX-DELIVERY | Workbench |
| DF-OPS-202 | attempt_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-203 | next_attempt_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-204 | last_error_code | TEXT | varchar(40) | No | None | Workbench |
| DF-OPS-205 | delivered_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-206 | task_id | CROSS_REF | uuid | No | None | Workbench |

**feature_flag** (NEW). A feature flag with its value per environment, owner and removal date.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-207 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-208 | flag_key | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-209 | description | TEXT | varchar(400) | Yes | None | Workbench |
| DF-OPS-210 | owner_user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-OPS-211 | owner_team | TEXT | varchar(60) | No | None | Workbench |
| DF-OPS-212 | default_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-213 | dev_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-214 | sit_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-215 | uat_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-216 | prod_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-217 | removal_date | DATE | date | Yes | None | Workbench |

**feature_flag_change** (NEW). One change of a feature flag value in one environment.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-218 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-219 | flag_key | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-220 | environment | LOV | varchar(4) | Yes | LOV-ENVIRONMENT | Workbench |
| DF-OPS-221 | old_value | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-222 | new_value | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-223 | reason | TEXT | varchar(400) | Yes | None | Workbench |

**job_catalog** (NEW). A scheduled job with its owner, run book and expected duration.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-224 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-225 | job_id | TEXT | varchar(6) | Yes | None | Workbench |
| DF-OPS-226 | job_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-227 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-OPS-228 | schedule_text | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-229 | runbook_path | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-230 | expected_minutes | NUMBER | integer | No | None | Workbench |
| DF-OPS-231 | alert_after_minutes | NUMBER | integer | No | None | Workbench |
| DF-OPS-232 | first_release | TEXT | varchar(3) | No | None | Workbench |

**party_product** (NEW). Another product the party holds at the bank, from the customer profile.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PTY-022 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PTY-023 | party_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PTY-024 | product_type | TEXT | varchar(20) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-025 | account_no | TEXT | varchar(20) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-026 | product_status | LOV | varchar(15) | Yes | LOV-PRODUCT-STATUS | SCBPDM via COLLINS |
| DF-PTY-027 | data_as_of | DATE | date | Yes | None | SCBPDM via COLLINS |

**efs_ledger_outcome** (NEW). Which EFS action codes enter the interaction ledger and on which channel.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-128 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-129 | action_code | LOV | varchar(10) | Yes | LOV-ACTION-CODE | Workbench |
| DF-REF-130 | channel | LOV | varchar(15) | Yes | LOV-CHANNEL | Workbench |
| DF-REF-131 | in_ledger | BOOLEAN | boolean | Yes | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH |
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 |
| LOV-DIRECTION | INBOUND, OUTBOUND |
| LOV-ENVIRONMENT | DEV, SIT, UAT, PROD |
| LOV-INTERFACE-RUN | RECEIVED, LOADED, REFUSED, MISSING, DUPLICATE, FAILED |
| LOV-OUTBOUND-STATUS | PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED |
| LOV-OUTBOX-DELIVERY | PENDING, RETRYING, DELIVERED, EXCEPTION |
| LOV-PRODUCT-STATUS | ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF |
| LOV-TRANSPORT | SFTP, COLLINS |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| processed_event | event_id | outbox_event | Many to 0 or 1 |
| outbox_event | case_id | recovery_case | Many to 0 or 1 |
| outbox_delivery | event_id | outbox_event | Many to 1 |
| outbox_delivery | task_id | task | Many to 0 or 1 |
| party_product | party_id | party | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-02 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next day's load | As approved |
| INT-04 | SCBPDM | In | COLLINS batch | Daily, end of day |
| INT-05 | UDP | In | COLLINS batch | Daily, end of day |
| INT-06 | AAL | In | COLLINS batch | Daily, end of day |
| INT-07 | EFS | In | COLLINS batch | Daily, end of day |
| INT-08 | COLLINS models | In | COLLINS batch | Daily; monthly for some models |
| INT-09 | LIT | In | COLLINS batch | Daily, end of day |
| INT-10 | CCMS | In | File load | Weekly |
| INT-11 | SVAF | In | File load | Weekly |
| INT-12 | AMIS | In | File load | Monthly |
| INT-13 | RPS | In | File load | Weekly |
| INT-14 | WIN | Out | File | Daily |
| INT-15 | WIN | In | File load | Weekly |
| INT-16 | GL | In | File load | Monthly |
| INT-17 | NSS | Out | ACE notification path | As sent |
| INT-18 | LINE OA | Out | ACE notification path | As sent |
| INT-19 | Data lake and Power BI | Out | Daily batch | Daily |
| INT-20 | COLLINS | Out | Daily batch to the data lake | Daily |
| INT-21 | Entra ID and the bank IAM | In | ACE sign-in | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE logging | As they happen |
| INT-23 | Enterprise AI model endpoint | Both | Private endpoint in the SCB tenant | Per request |
| INT-24 | Partner portal | Both | Workbench screens through the external gateway | As entered |
| INT-25 | Debt buyers | Out | File through the data room | Per lot |
| INT-26 | NLEADS | Out | Submitted by the officer in NLEADS | As needed |
| INT-27 | HOME.SCB | Out | Not available today; published by the sale officer | As listed |
| INT-28 | SCIS | Out | Not available today; prepared by the officer | As needed |
| INT-29 | Thai Credit Guarantee Corporation | Both | Not available today; entered and filed by the guarantee officer | As needed |
| INT-30 | NCB | In | Not available today; by the officer | As needed |
| INT-31 | Aric | Out | Not available today; by the fraud investigator | As needed |
| INT-32 | Salesforce | In | Not available today | None |
| INT-33 | Legal Execution Department and courts | In | Through the law firms in the partner portal | As entered |
| INT-34 | ACE common module | Both | Published module interface | Per request |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| None | |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Platform administration |
|---|---|
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | CRUD |
| RW-SECADM Security administrator | CRUDA |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

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
| REQ-DRI-006 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-007 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-008 | FEAT-RDF-21 | RWB-E1-007 | TC-E1-007-01 |
| REQ-DRI-013 | None | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P2-001 | GET | /api/recovery/v1/admin/outbound-items | Platform administration R | E1 |
| API-P2-002 | POST | /api/recovery/v1/admin/outbound-items/{itemId}/resend | Platform administration U | E1 |
| API-P2-003 | GET | /api/recovery/v1/admin/outbox/deliveries | Platform administration R | E1 |
| API-P2-004 | POST | /api/recovery/v1/admin/outbox/deliveries/{deliveryId}/resend | Platform administration U | E1 |
| API-P2-005 | GET | /api/recovery/v1/feature-flags | None R | E1 |
| API-P2-006 | GET | /api/recovery/v1/admin/feature-flags | Platform administration R | E1 |
| API-P2-007 | POST | /api/recovery/v1/admin/feature-flags | Platform administration C | E1 |
| API-P2-008 | PATCH | /api/recovery/v1/admin/feature-flags/{flagKey} | Platform administration U | E1 |
| API-P2-009 | GET | /api/recovery/v1/admin/scheduled-jobs | Platform administration R | E1 |
| API-P2-010 | GET | /api/recovery/v1/cases/{caseId}/plan-status | Case record R | E2 |
| API-P2-011 | GET | /api/recovery/v1/cases/{caseId}/customer-products | Case record R | E2 |
| API-P2-012 | GET | /api/recovery/v1/treatments/{treatmentId}/credit-pack | Treatment and offer R | E2 |
| API-P2-013 | POST | /api/recovery/v1/treatments/{treatmentId}/credit-result | Treatment and offer U | E2 |
| API-P2-014 | POST | /api/recovery/v1/admin/interfaces/{interfaceCode}/manual-retirement | Reference data U | E2 |

### T-A.2 Endpoint detail

#### API-P2-001 GET /admin/outbound-items

| Item | Value |
|---|---|
| Purpose | List outbound file items by status and interface for the exception queue |
| Request | Query: status, interfaceId, from, to |
| Response | OutboundItem[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-002 POST /admin/outbound-items/{itemId}/resend

| Item | Value |
|---|---|
| Purpose | Send an outbound item in the exception queue again: status PENDING, attempt count 0 |
| Request | None |
| Response | OutboundItem |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-003 GET /admin/outbox/deliveries

| Item | Value |
|---|---|
| Purpose | List application event outbox deliveries by status and consumer |
| Request | Query: status, consumer, eventType, from, to, page, size |
| Response | OutboxDeliveryPage |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-004 POST /admin/outbox/deliveries/{deliveryId}/resend

| Item | Value |
|---|---|
| Purpose | Send an outbox delivery in the exception queue again: status PENDING, attempt count 0 |
| Request | None |
| Response | OutboxDelivery |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-005 GET /feature-flags

| Item | Value |
|---|---|
| Purpose | Read the effective feature flag values for the caller's environment |
| Request | None |
| Response | FeatureFlagValue[] |
| Errors | 401, 503 |
| Authorization | None, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-006 GET /admin/feature-flags

| Item | Value |
|---|---|
| Purpose | List feature flags with values per environment, owner and removal date |
| Request | Query: overdue, owner |
| Response | FeatureFlag[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-007 POST /admin/feature-flags

| Item | Value |
|---|---|
| Purpose | Create a feature flag |
| Request | FeatureFlagRequest |
| Response | FeatureFlag |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Platform administration, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-008 PATCH /admin/feature-flags/{flagKey}

| Item | Value |
|---|---|
| Purpose | Change a feature flag value for one environment with a reason |
| Request | FeatureFlagChange |
| Response | FeatureFlag |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Not applicable |

#### API-P2-009 GET /admin/scheduled-jobs

| Item | Value |
|---|---|
| Purpose | List the job catalog with owner, schedule, run book and alert threshold |
| Request | None |
| Response | JobCatalogEntry[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-010 GET /cases/{caseId}/plan-status

| Item | Value |
|---|---|
| Purpose | Read the ACE restructure plan status of the case, live with fallback to the stored status |
| Request | None |
| Response | PlanStatus |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-011 GET /cases/{caseId}/customer-products

| Item | Value |
|---|---|
| Purpose | Read the other products of the case's borrowers from the customer profile, masked by role |
| Request | None |
| Response | CustomerProducts |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-012 GET /treatments/{treatmentId}/credit-pack

| Item | Value |
|---|---|
| Purpose | Assemble the credit approval pack for submission in NLEADS |
| Request | None |
| Response | CreditPack |
| Errors | 401, 403, 404, 503 |
| Authorization | Treatment and offer, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-013 POST /treatments/{treatmentId}/credit-result

| Item | Value |
|---|---|
| Purpose | Record the NLEADS reference, result, approval level and reason on the treatment |
| Request | CreditResult |
| Response | Treatment |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-014 POST /admin/interfaces/{interfaceCode}/manual-retirement

| Item | Value |
|---|---|
| Purpose | Sign off the end of manual file handling for an interface after the required clean days |
| Request | ManualRetirementRequest |
| Response | InterfaceSignoff |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Reference data, right U, scope applied |
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
