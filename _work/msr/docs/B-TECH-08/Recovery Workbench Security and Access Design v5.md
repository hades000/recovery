SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Security and access design

| Item | Detail |
|---|---|
| Document | Recovery Workbench security and access design |
| Version | 5 |
| Date | 22 November 2026 |
| Change | 5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts, with C4 component views and ISO/IEC/IEEE 42010 viewpoints |
| Status | Draft. No approval is recorded for this version (ASM-B-TECH-08-9) |
| Source version | 4, 16 November 2026 |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60 |

# Change log

| Version | Date | Change |
|---|---|---|
| 5 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Login per service, workload identity and the authorise contract. Sections 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 and 11; the change table is at the end of the document |
| 4 | 16 November 2026 | 4, 16 November 2026, D-RCV-36: Temporal workflow security with mTLS, Entra ID OIDC and a break-glass codec server; every payload encrypted by the PdpaPayloadCodec; temporal_svc and recovery_svc isolation; embedded Drools rule packages authored by RW-COE, approved by RW-RISK and stored with a checksum (sections 1, 4, 5, 7, 8, 9, 10) |

# 1. The design on one page

| Concern | Design | Status |
|---|---|---|
| Sign-in | Entra ID single sign-on with multi-factor authentication through the ACE front end; OpenID Connect with the authorization code flow and PKCE. The session is held in the gateway-bff Redis store and the browser holds an opaque token; gateway-bff passes a short-lived JWT to the owning service, which validates it and authorises the object itself (Architecture v5 slides 10 and 35) | ACE pattern; ADR-019 |
| Permission check | Every endpoint checks the role, the capability area, the right and the scope before it runs, inside the owning service, against cached permission data from rwb-access. The contract is POST /authorise, GET /me/permissions, GET /doa-limits and /masking-policies of rwb-access (DP-08; Architecture v5 slides 10, 14 and 35) | Designed; ADR-020 |
| Authorise contract | rwb-access (P4) publishes the authorise contract and the guard library is a platform component; both are contract stories of wave 1 (H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON) | Designed; DP-08, ADR-020 |
| Database login | One login per service, rwb_<short with _>, with grants on its own schema only; a PgBouncer pool and a connection cap per login; Flyway per service; no cross-schema joins, views or foreign keys (Architecture v5 slide 29) | Designed; ADR-014, ADR-021 |
| 19 services | One service per module, P1 to P10 and S1 to S9, each with its own schema, login, topic rwb.<short>.events.v1, task queue rwb-<short> and workload identity (Rules v1 §R4; Architecture v5 slides 5 and 41) | Designed; D-RCV-60, ADR-013 |
| Case workflow engine | Temporal, self-hosted in the rwb-recovery namespace. mTLS between the workers, frontend and internal services, with one worker identity per service on its own task queue. Web UI behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode only through the codec server (E1-070, E2-038) | Designed; D-RCV-36, ADR-011, ADR-016 |
| Rule packages | Embedded Drools per service. The registry, the versions and the four-eyes approval sit in rwb-decision (P7) and each owning service loads the version in force and verifies the checksum. RW-COE authors a package and RW-RISK approves it; the author cannot approve. SY-RULES evaluates it, and the workbook and DRL are stored with a checksum (ADR-012) | Designed; D-RCV-36, ADR-017 |
| Identity to role | Entra ID group membership, granted through bank IAM, maps to Workbench roles held as data; the roles, the rights, the scope, the masking rows and the DoA rows are held in rwb-access (P4) | Agreed; groups DL40, ADR-014 |
| Scope | Own cases, team, region or all, applied as a filter on every query of the owning service | Designed |
| Approval limits | The delegation of authority table checked before an approval is accepted; the table is delegation_limit in rwb-access (P4) | Designed; limits DL18, ADR-014 |
| Masking | Personal fields masked in the response at the API of every service unless the role may see them (E1-037). The national ID is never read in clear: v_ace_customer returns id_no_masked and id_no_last4 only, and only rwb-source-data reads it. Every read of a personal field is audited (CG-B-TECH-08-3; ASM-B-TECH-08-3) | Designed; rules DL26, DP-05 |
| Sessions | Token lifetime, inactivity timeout and break-glass window set by SCB IT security; the session store is Redis in gateway-bff | Open, DL38; ADR-019 |
| Partners | Separate partner identities through the partner gateway in the DMZ, limited to the cases placed with the firm; partner users are rows of rwb_partner (S9) | Open, DL03; ADR-019 |
| Service identities | One workload identity per service (19) and one per non-human actor, with no static credential: mesh mTLS, OAUTHBEARER (Entra) or mTLS to Kafka, and mTLS to Temporal. No data load identity: ACE ingests every source | ACE pattern; ADR-013, ADR-014 |
| ACE data access | Read only. The rwb_source_data login holds SELECT on the 30 recovery.v_ace_* views and nothing else; the other 18 logins hold no grant on schema recovery and no grant on any ACE public table. The views are owned by ace_view_owner, which reads the public ACE tables. No direct public read, no write, PUBLIC revoked | Designed; D-RCV-35, RWB-E1-069, ADR-014 |
| Logging | Access log in the Workbench (rwb_access, P4), ACE audit log, PII log through PII Kafka, security events to the SOC log, one trace across the 19 services | ACE pattern; ADR-023 |

# 2. Context

The Workbench is a module of the ACE service. It reuses the ACE sign-in, access check, audit, PII logging and SOC logging. The recovery module adds its roles, permissions, scope rules, masking rules and approval limits as data, and checks them on every request. The Workbench loads, copies and transforms no source data. ACE ingests every source into the ACE database, and the recovery module reads it only through SELECT-only recovery.v_ace_* views (D-RCV-35, ADR-010).

Version 5 reads that paragraph per service. The Workbench is now 19 services, one per module, inside the ACE platform (Architecture v5 slides 3, 5 and 41; ADR-013). Each one has its own schema and login in the ACE database, its own Kafka topic and consumer group, its own Temporal task queue and its own workload identity (Architecture v5 slides 29 and 35; ADR-014). The roles, permissions, scope rules, masking rules and approval limits stay as data, in rwb-access (P4), and every service holds a cached copy and checks the object itself before it acts (Architecture v5 slide 10; DP-08). Only rwb-source-data (P1) holds the read-only login on the 30 recovery.v_ace_* views; every other service reads ACE data through the rwb-source-data REST contract and never through SQL (Architecture v5 slides 11, 29 and 30; DP-05).

| Actor | How it reaches the Workbench | Identity |
|---|---|---|
| Bank staff | ACE front end on the bank network, through the internal application gateway with web application firewall to gateway-bff | Entra ID user with multi-factor authentication; a short-lived JWT per service |
| Partners | Partner portal through the partner gateway in the DMZ, once external access is approved (DL03) | Partner identity, separate from bank identities; partner_user in rwb_partner (S9) |
| Customers | No sign-in. Offers and listings reach them through SCB Easy, LINE OA, SMS, branches and HOME.SCB | Bank channel identity |
| Non-human actors | Service to service inside the ACE namespace over mesh mTLS; outbound through the outbox | Workload identity per service (19), and one managed identity per non-human actor |
| Agents | Through the tool gateway only | Managed identity per agent, limited by the autonomy level |

# 3. Sign-in and sessions

## 3.1 Sign-in flow

- The person opens the ACE front end. The front end redirects to Entra ID with the authorization code flow and PKCE.

- Entra ID applies multi-factor authentication and the bank conditional access policies.

- The front end receives the tokens. The ID token names the person; the access token carries the group claims for the ACE application.

- On the first request the service resolves the groups to Workbench roles, the scope and the masking profile, and writes the session start to the access log.

- A person with no Workbench role is refused with MSG-P4-001. A person whose groups hold a conflicting role pair is refused and an incident is raised.

- The session is held in the gateway-bff Redis store and the browser holds an opaque token only (Architecture v5 slides 10 and 35; ADR-019).

- gateway-bff passes a short-lived JWT to the owning service. The service validates the token and authorises the object itself against cached permission data from rwb-access (Architecture v5 slide 10; DP-08).

## 3.2 Session rules

| Rule | Value used until DL38 is decided | Set by |
|---|---|---|
| Access token lifetime | The ACE value | SCB IT security |
| Inactivity timeout | 15 minutes, with a warning at 13 minutes | SCB IT security |
| Maximum session length | One working day | SCB IT security |
| Group change | Takes effect at the next request; a removed role ends the session | Workbench |
| Concurrent sessions | One active session per person per device | Workbench |
| Break-glass window | Four hours, then the grant ends with no action by anyone | SCB IT security |
| Session store | Redis in gateway-bff; the browser holds an opaque token | Platform, ADR-019 |
| Token to the service | A short-lived JWT passed by gateway-bff and validated by each service | Platform and P4 rwb-access |

The session itself is one; the permission check is repeated in every service that serves the request, so a role removed in rwb-access takes effect at the next call even when gateway-bff still holds a valid session (Architecture v5 slide 10; DP-08).

# 4. The permission check

Every endpoint declares the capability area and the right it needs. The check runs in the service before any data is read, using the role permissions in force for the request date.

In version 5 the check runs in the owning service, not only in the gateway. Each of the 19 services holds a cached copy of the role, right, scope, masking and DoA rows of rwb-access and refreshes it on AccessPolicyChanged and DoaLimitChanged from rwb.access.events.v1 (Architecture v5 slides 10, 14 and 27; DP-08). Architecture v5 slide 10 states the rule for every service: each service authorises the object itself (OWASP API1 object-level authorisation), using cached permission data from rwb-access.

| Step | What is checked | Refused with |
|---|---|---|
| 1 | The session is valid and the person holds at least one Workbench role | HTTP 401; MSG-P4-001 |
| 2 | One of the person's roles holds the right (C, R, U, D or A) in the capability area the endpoint declares | HTTP 403; MSG-P4-002 |
| 3 | The record is inside the person's scope: own cases, team, region or all | HTTP 404; MSG-P4-003 |
| 4 | For an approval: the person's approval level and the delegation of authority limit for the decision, product and amount | HTTP 409; MSG-P7-001 |
| 5 | For an approval: the person did not prepare or propose the decision | HTTP 409; MSG-P7-002 |
| 6 | The response is masked by the person's masking profile before it leaves the service | Not refused; fields masked |

Scope is applied in the query, so a record outside the scope is never read. A refusal returns 404 for records outside the scope, so the response does not reveal that the record exists.

The permission matrix, the scope per role and the masking rules are versioned data. A change is a validated load with a valid from date and needs no code release.

## 4.1 The authorise contract

The permission data is served by rwb-access (P4) and held by every service as a cache. The operations are the ones named in Architecture v5 slide 14.

| Operation | Owner | Held by | Use |
|---|---|---|---|
| POST /authorise (role, scope, DoA) | P4 rwb-access | every service, server side | the right, the scope and the DoA answer for one request |
| GET /me/permissions | P4 rwb-access | gateway-bff and every service | the rights of the signed-in person |
| GET /doa-limits | P4 rwb-access | P7 rwb-decision and each approving service | the delegation of authority limits |
| /masking-policies | P4 rwb-access | every service | the masking profile per role and field |
| rwb.access.events.v1: AccessPolicyChanged, DoaLimitChanged | P4 rwb-access | every service (cache refresh) | cache invalidation, no code release |
| Guard library: the check itself | Platform, RWB-PLT-E1037-CON | every service as a library | one implementation of steps 1 to 3, contract-tested against the fake |

The request and response shapes of these operations are not specified in the sources (CG-B-TECH-08-2; ASM-B-TECH-08-2); the contract is written in RWB-P4-E1037-CON and the fake in RWB-PLT-E1037-CON, so no service builds against a private copy.

## 4.2 Rights on the new objects

The matrix keeps the existing role codes. These are the rights added for Temporal and for rule packages; a right not listed here is refused with MSG-P4-002.

| Role | New rights on the new objects | Condition |
|---|---|---|
| RW-PLATADM | Temporal workflow (C, R, U, D); Temporal Web UI (R) | Operate the cluster and the Web UI; no payload decode |
| RW-AUDIT | Temporal workflow and history (R); Temporal Web UI (R); rule package version (R) | Read only; payloads stay encrypted |
| RW-SECADM | Temporal payload decode (R) | Codec server only, with an open break-glass session (E1-039); every decode logged |
| RW-COE | rule_package and rule_package_version (C, R, U) | Author and upload a version; cannot approve |
| RW-RISK | rule_package_version (R, A) | Approve or reject a version; cannot author |
| SY-RULES | rule_package_version and rule_row (R) | Evaluate only the version in force |
| SY-CASEWF | Temporal workflow (C, R, U) | Start and signal case workflows on rwb-case; no terminate or reset |
| All other roles | None | Refused with MSG-P4-002 |

The objects behind those rights have one owning service each, taken from the Microservice Ownership Map v1 and Architecture v5 slide 41.

| Object | Owning service |
|---|---|
| Temporal workflow | The service that runs it: CaseWorkflow in P3 rwb-case; RouteDecisionWorkflow in S1, TreatmentWorkflow in S2, GuaranteeClaimWorkflow in S3, LitigationWorkflow in S4, AssetDisposalWorkflow in S5, DebtSaleWorkflow in S6, WriteOffWorkflow in S7 and DeviationWorkflow in S8; ApprovalWorkflow in P7 rwb-decision |
| Temporal Web UI and codec server | Platform, RWB-PLT-WF |
| rule_package, rule_package_version, rule_row | P7 rwb-decision |
| Break-glass grant and the access log | P4 rwb-access |

# 5. Personal data protection

| Control | Design |
|---|---|
| National ID | ACE holds the national ID or passport number (customer.identification_number). The Workbench never reads it in clear: v_ace_customer returns id_no_masked, with only the last four digits shown, and id_no_last4. Nothing is tokenized at load, because there is no load; role masking at the API (E1-037) replaces the former id_no_token. Only the rwb_source_data login reads v_ace_customer; every other service receives the masked values through the rwb-source-data contract (DP-05) |
| Tokenization | None at load. There is no Workbench load to tokenize, so there is no id_no_token column and no token vault in the source path. Masking is applied in v_ace_customer (id_no_masked, id_no_last4) and by E1-037 at the API |
| Masking | Name, address, phone, email and account numbers are masked at the API by the masking profile of the role (E1-037). v_ace_contact returns the full phone, email and address, because notices and calls need them, so the API mask is the control. The profile is a data row per role and field, held as masking_rule in rwb-access (P4), and every service applies it before the response leaves (CG-B-TECH-08-3; ASM-B-TECH-08-3) |
| Unmasking | A role allowed to unmask a field does so per record; each unmask is written to the PII log |
| Audit of reads | Every read of a personal field, including each read through v_ace_customer and v_ace_contact, is written to the PII log through PII Kafka. The control is the read-only grant, E1-037 masking and the audit log together; the mask in a view is not a PDPA control on its own |
| Exports | Exports carry the masking of the person who runs them. A debt sale data tape passes the masking check before the data room opens |
| Test data | Synthetic only in DEV. Masked copies from the PII service in SIT and UAT |
| Logs and prompts | No personal data in application logs, test fixtures or agent prompts. The PDPA lint gate checks code before merge |
| Retention | Each data product and document type carries a retention class (DL26). Expiry is held while a legal hold is in place; retention_rule is owned by P5 rwb-document |
| Workflow history | Every Temporal payload is encrypted by PdpaPayloadCodec (AES-GCM) with a key in Azure Key Vault before it is written, and the keys are held per namespace (Architecture v5 slide 41 notes). Every worker of every service uses the codec, so workflow history never holds clear personal data. Search attributes carry CaseId, Stage, ProductGroup and QueueCode only. Key rotation keeps old histories decodable (E2-038; CG-B-TECH-08-8; ASM-B-TECH-08-8) |
| Rule facts | Drools evaluates facts in memory inside the owning service. The rule packages and versions are registry rows of rwb-decision (P7) and the service holds the evaluated copy in force (DP-04; ADR-017). The decision log stores the rule ID and the package version; rule packages and the rule catalog hold no personal data |

Nothing in this section changes the mask itself. The realignment adds two facts: the personal data stays in the owning service and moves between services as IDs and business facts only (Architecture v5 slide 35), and ACE data reaches the other 18 services through the rwb-source-data contract rather than through SQL (DP-05).

# 6. Partners

- Partner users reach the partner portal through the external gateway once the architecture team approves external access (DL03); the partner gateway sits in the DMZ with the FAPI 2.0 profile (Architecture v5 slide 35; ADR-019).

- Each partner user has a partner identity, separate from bank identities, with multi-factor authentication.

- The partner and agency manager requests partner users; the role owner approves. Accounts end when the firm's contract ends. The partner user is a row of rwb_partner (S9 rwb-partner); the roles it receives are the role rows of rwb-access (P4) (CG-B-TECH-08-7; ASM-B-TECH-08-7).

- A partner user sees only the instructions placed with their firm. Scope is the firm, set on the instruction.

- Partner uploads pass a file type check and a malware scan before they reach the document hub.

- Until external access is in place, partners keep their current channels and bank staff record partner results.

# 7. Service identities and secrets

| Item | Design |
|---|---|
| Managed identities | One per non-human actor: case workflow (SY-CASEWF), Drools rules engine (SY-RULES), OCR pipeline, decision log writer, agent platform |
| Workload identity | One workload identity per service, 19 in all, from the platform of wave 0. A service authenticates to the mesh, to Kafka and to Temporal with its own identity; there is no shared service account and no credential in a manifest (Architecture v5 slide 35; ADR-013, ADR-014). Wave 0 creates the identity with the service, from the service template RWB-PLT-TPL |
| Load identity | None. The Workbench runs no inbound load, so it holds no source load identity, no file share credential and no staging account. ACE ingestion uses its own identity and writes the ACE tables |
| Secrets | Key Vault, reached by the workload identity. No secret in code, configuration or prompts. The secret scan gate checks every merge |
| Database | Each service connects with its own login, rwb_<short with _>, which owns its schema and holds grants on that schema only. A PgBouncer pool and a connection cap per login protect ACE, and each service runs its own Flyway sequence in its own schema (Architecture v5 slide 29; ADR-014, ADR-021). People do not hold write access in production. No recovery migration creates or alters a table in the ACE public schema |
| Read-only ACE access | The rwb_source_data login holds USAGE on schema recovery and SELECT on the recovery.v_ace_* views only. It holds no SELECT on any public ACE table and no INSERT, UPDATE, DELETE or TRUNCATE on any ACE table or view, so a direct public read or a write fails in the database catalog, not only in code review. This is the read-only ACE service identity of the Admin and Access Model v5. The other 18 logins hold no grant on schema recovery and no grant on any ACE schema (Architecture v5 slides 11 and 29) |
| View owner | The v_ace_* views are owned by ace_view_owner, a NOLOGIN ACE role that holds SELECT on the public ACE tables the views read and writes neither schema. It is not a Workbench role and nobody signs in as it. A view runs with its owner's privileges, so any row-level security ACE adds later is applied inside the view |
| PUBLIC | All privileges on the recovery tables and views are revoked from PUBLIC, and the same is done for every rwb_* schema of the 19 services. A role reads a view or a table only through an explicit grant |
| Grant check | The view conformance test in RWB-E1-069 runs in the pipeline and fails the build if rwb_source_data can select a public table or write any table, if a v_ace_* view does not compile, or if a constraint in schema recovery references a public table. The boundary test of every service fails on any cross-schema reference (Architecture v5 slide 29; CG-B-TECH-08-6; ASM-B-TECH-08-6) |
| Kafka | Per-service ACLs on rwb.<short>.events.v1, on the retry topics and on the .dlt topic: a service produces on its own topic and consumes the topics it is contracted to read. The client identity is the workload identity (OAUTHBEARER with Entra, or mTLS) (Architecture v5 slide 11) |
| Agents | An agent reaches a system only through the tool gateway. The gateway holds the permissions; the agent holds none |
| Network | Private endpoints to storage and the database. No public endpoint on the service, and none on any of the 19 services |
| temporal_svc isolation | temporal_svc owns the temporal and temporal_visibility databases. It has no grant on the ACE database, no read on any recovery.v_ace_* view and no sign-in right. Its only purpose is the Temporal persistence |
| Service login isolation | None of the 19 logins has a grant on temporal or temporal_visibility, and none can read workflow history through SQL. Each reads ACE data only through the rwb-source-data contract, except rwb_source_data, which reads the views. The single recovery_svc role of version 4 is replaced by these 19 logins (Architecture v5 slide 29; ADR-014; CG-B-TECH-08-1; ASM-B-TECH-08-1) |
| Temporal certificates | mTLS certificates for the workers, frontend and internal services are issued from Key Vault and rotated there. They are held per namespace, so rwb-recovery has its own set. The frontend gRPC port 7233 is internal only |
| Codec server | Runs with its own managed identity and the Key Vault key reference, one key per namespace. A decode is open only to RW-SECADM inside an open break-glass session |
| Rule store | Rule workbooks and generated DRL are stored with a checksum. Only RW-COE uploads a version, only RW-RISK approves it in the registry of rwb-decision (P7), and SY-RULES in each owning service reads the package in force and the catalog |

## 7.1 Temporal security

Temporal uses the same identity, transport and audit controls as the rest of the Workbench. The difference is that a workflow history holds payloads, so the codec and the decode right carry the personal data control.

| Control | Design |
|---|---|
| Transport | mTLS between the workers, the frontend and the internal services. Certificates come from Key Vault, are held per namespace and rotate there. The frontend gRPC port 7233 is internal only |
| Worker identity | One worker identity per service; a worker polls only its own task queue rwb-<short> in namespace rwb-recovery (Temporal and Drools design, L2 and L4; Architecture v5 slide 41) |
| Web UI | Entra ID OIDC. RW-PLATADM operates and RW-AUDIT reads. Any role other than those two is refused with MSG-P4-002 |
| Payload decode | RW-SECADM only, through the codec server, with an open break-glass session (E1-039). Every decode is logged. Any other role is refused with MSG-P4-002 |
| Authorizer plugin | The Temporal authorizer plugin (TemporalAuthorizerPlugin) maps the OIDC role claim, the workload identity of the calling service and the client certificate to the Workbench role. A call outside the role's right is refused with MSG-P4-002 (E2-038; CG-B-TECH-08-4; ASM-B-TECH-08-4) |
| Admin audit | TemporalAdminAuditListener reads the Temporal frontend audit log and writes start, signal, terminate, reset and decode actions to the decision log (E2-038) |
| Payload codec | PdpaPayloadCodec: AES-GCM, keys in Azure Key Vault per namespace, every payload encrypted before it leaves the worker. History never holds clear personal data. Key rotation keeps old histories decodable (E2-038) |
| Isolation | temporal_svc has no grant on the ACE database and the 19 service logins have no grant on the Temporal databases. None of these roles is a sign-in role |

## 7.2 Drools rule security

A rule package is business logic held as data, so it has the same maker-checker control as a reference load and an integrity check on every load.

| Control | Design |
|---|---|
| Authoring | RW-COE writes each package as an Excel workbook in Drools decision-table format and uploads a version. Only RW-COE writes a rule package. The registry, the package versions and the approval history are rows of rwb_decision (P7 rwb-decision) |
| Approval | RW-RISK approves or rejects a version. The author cannot approve its own package; the check is on the person and on the role |
| Evaluation | SY-RULES evaluates an approved version in force through RuleEvaluator, in the service that owns the model, and holds read only on the package version and the rule catalog it has loaded (DP-04; ADR-017) |
| Integrity | The workbook and the generated DRL are stored with a checksum. A checksum mismatch refuses the version at load and raises an incident; the owning service verifies the checksum when it swaps a model (ADR-017) |
| No release | A version moves from upload to in force without a code release; rollback is one call |
| Traceability | The decision log records the rule ID (the Drools rule name) and the package version label for every decision; the local record is written by the owning service and sealed in the central ledger of rwb-decision (ADR-022) |

# 8. Logging and monitoring

| Record | Holds | Read by |
|---|---|---|
| Access log | Sign-ins, refusals, grants, removals, break-glass use and the versions in force. Append only. Held in rwb_access (P4 rwb-access) (CG-B-TECH-08-5; ASM-B-TECH-08-5) | Application owner, security administrator, Compliance, internal audit |
| Decision log | Every decision with inputs, rule version, recommendation, approver and action. Append only and hash chained. Written locally by the owning service in its own schema, then sealed in the central ledger of rwb-decision (P7) (ADR-022) | Internal audit, Risk, center of excellence |
| ACE audit log | Every change made through the service | Security administrator, internal audit |
| PII log | Every read and unmask of a personal field, including reads through v_ace_customer and v_ace_contact, through PII Kafka | Compliance, internal audit |
| SOC log | Security events: repeated refusals, conflict refusals, break-glass, failed sign-ins | SCB security operations |
| Temporal audit log | Workflow start, signal, terminate, reset and every Web UI or CLI admin action, read by TemporalAdminAuditListener. Append only. Each service reads the events of its own task queue | Security administrator, internal audit |
| Codec decode log | Every payload decode with the person, the break-glass session, the workflow ID and the time. Append only | Security administrator, Compliance, internal audit |

Every one of the 19 services sends its audit and personal-data access entries through the ACE PII Kafka path to the SOC, and one trace covers the chain from gateway-bff to the owning service (Architecture v5 slides 30 and 35; ADR-023).

# 9. Threats and controls

| Threat | Example | Control |
|---|---|---|
| Spoofing | A stolen password used to sign in | Multi-factor authentication; conditional access; SOC alert on unusual sign-in |
| Tampering | A decision or legal document changed after the fact | Append-only, hash-chained decision log; write-once container for legal documents; no write grant on any ACE table or view |
| Repudiation | An approver denies approving | Decision log entry with the approver identity, level and time |
| Information disclosure | Customer data read outside the role or sent outside the bank | Scope filter; masking (E1-037); national ID masked in v_ace_customer; SELECT on recovery.v_ace_* only for rwb_source_data, no direct public read; PII log; no personal data in exports beyond the role |
| Denial of service | A partner floods the portal | External gateway rate limits; web application firewall; a connection cap per login and per topic |
| Elevation of privilege | A person grants themselves a business role | Separation of duty at grant and at sign-in; access review every six months (DL38) |
| Lateral movement | A service reads another service's schema, topic or queue | One login, one topic ACL and one workload identity per service; no cross-schema grant; deny by default in the mesh; the boundary test fails on any cross-schema reference (Architecture v5 slides 29 and 35) |
| Credential theft | A copied password, key or connection string used from outside | No static credential: workload identity, Key Vault, short-lived SAS links of 15 minutes; secret scan gate on every merge |
| Workflow history disclosure | A payload or history read outside the role | PdpaPayloadCodec; mTLS; OIDC roles; decode only through the codec server in break-glass and every decode logged |
| Rule package tampering | A rule changed or loaded without approval | RW-COE author and RW-RISK approval; checksum on the workbook and the DRL; append-only decision log; the registry is P7 rwb-decision |

# 10. Tests before each release

| Test | Passes when | Signed by |
|---|---|---|
| Sign-in per role | Each role in the release signs in and shows the right roles, scope and masking | Role owner |
| Login per service | The 19 logins exist, each with grants on its own schema only, no grant on another schema and no grant on the ACE public schema | DBA and Tech lead |
| Endpoint permissions | An automated test calls every endpoint with a role that lacks the right and receives 403 | QA lead |
| Authorise contract | Every service refuses a request the authorise contract does not allow, and the guard library passes its contract test against the fake | QA lead |
| Scope | A role reads a record outside its scope and receives 404 | QA lead |
| Masking | Three roles read the same case and see the fields their profiles allow | Compliance |
| Read-only ACE grant | The view conformance test passes: rwb_source_data reads every v_ace_* view, cannot select a public table and cannot insert, update or delete on any table; no other login reads schema recovery | Tech lead |
| Approval limit | An approval above the limit routes to the next level | Risk |
| Workload identity | A service without a valid workload identity or client certificate is refused by the mesh, by Kafka and by Temporal | Tech lead |
| Container and secret scans | No vulnerability above the bank threshold; no secret in code | Tech lead |
| Penetration test | Before the partner portal opens to users outside the bank | SCB IT security |
| Temporal mTLS | A client without a valid certificate is refused, and the workers, frontend and internal services connect over mTLS | Tech lead |
| Temporal decode | RW-SECADM decodes only with an open break-glass session and the decode is logged; any other role gets MSG-P4-002 | Security administrator |
| Workflow payloads | No clear personal data appears in workflow history, payloads or search attributes | Compliance |
| Rule separation of duty | RW-COE cannot approve its own package, and RW-RISK approval is required before a version is in force | Risk |

# 11. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL01 | Whether access is granted centrally or by the application owner | Application owner administration |
| DL03 | How partners reach the partner portal from outside the bank | Partners keep current channels until external access is approved |
| DL26 | Retention and masking per data product and document type | Masking profiles as proposed in the data classification |
| DL38 | Session, inactivity and break-glass timers | The values in 3.2 |
| DL40 | Entra ID groups for the Workbench roles | One group per role per environment |
| DL43 | Whether the ACE team accepts the RWB-ACE-001 scope and dates, by 21 November 2026 | Section A views and grants only; Section B features stay behind flags |
| DL44 | Adopt Architecture v5 for the realignment | Decided on 22 November 2026 under D-RCV-60 |
| DL45 | One epic per service, with the business epic kept as a tag | Decided on 22 November 2026 under D-RCV-60 |
| DL46 | Soft ownership by team type, with no named person | Decided on 22 November 2026 under D-RCV-60 |
| DL47 | Epic 1 preservation rule for work built or in build | Decided on 22 November 2026 under D-RCV-60 |
| DL48 | Dates unchanged and read as tentative | Decided on 22 November 2026 under D-RCV-60 |
| DL49 | Gap and assumption registers held with the run material | Decided on 22 November 2026 under D-RCV-60 |

# Realignment changes in version 5 (D-RCV-60)

The table records what version 5 changes, where, why and under which decision. Every other statement, table, ID and number of version 4 is unchanged.

| # | Section | Version 4 | Version 5 | Decision and pattern |
|---|---|---|---|---|
| 1 | 1, 2, 7 | One recovery schema and one login, recovery_svc, for the whole Workbench | 19 schemas and 19 logins, rwb_<short with _>, one per service; schema recovery keeps only the 30 v_ace_* views | ADR-014; DP-02, DP-15 |
| 2 | 1, 2, 7, 10 | The recovery service role reads the views | Only rwb_source_data holds SELECT on the 30 views; the other 18 logins hold no grant on schema recovery | ADR-014; DP-05 |
| 3 | 1, 2, 5 | ACE data read by the module through the views | ACE data read by the other 18 services through the rwb-source-data REST contract; SQL only in P1 | DP-05, DP-11 |
| 4 | 1, 2, 7, 9 | Managed identities per non-human actor | One workload identity per service, plus one per non-human actor; mesh mTLS, Kafka ACLs, Temporal worker identity per service | ADR-013, ADR-014 |
| 5 | 1, 3, 4 | The check runs in the service | Each of the 19 services authorises its own objects against cached rwb-access data, with POST /authorise and its sibling operations, and the guard library as a platform component | DP-08; H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| 6 | 1, 4, 5 | Masking profile held as data | masking_rule rows of rwb-access (P4), applied by every service at its API | ADR-014 |
| 7 | 1, 4, 8 | Approval limits and DoA table | delegation_limit in rwb-access (P4) | ADR-014 |
| 8 | 1, 7 | Temporal mTLS with one worker identity | One worker identity per service on its own task queue, certificates and codec keys per namespace, workload identity in the authorizer plugin | ADR-016; E2-038 |
| 9 | 1, 7 | Rule packages authored and approved with a checksum | Registry and four-eyes approval in rwb-decision (P7); each owning service loads the version in force and verifies the checksum | ADR-017; DP-04 |
| 10 | 1, 6 | Partner users under the Workbench role model | Partner users in rwb_partner (S9), internal roles in rwb-access (P4), partner gateway in the DMZ with FAPI 2.0 | ADR-019; Ownership Map ruling on partner_user |
| 11 | 1, 8 | Decision log written centrally inside the call | Local record in the owning service's schema, sealed in the central ledger of rwb-decision (P7) | ADR-022 |
| 12 | 1, 8 | Audit, PII and SOC logging | Unchanged in content, read per service, with one trace across the 19 services | ADR-023 |

End of document. Version 5, 22 November 2026, D-RCV-60, T3 Code / OpenCode / DeepSeek v4.1 Flash.
