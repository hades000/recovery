Recovery Workbench

Security and access design

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench security and access design |
| Version | 4 |
| Date | 16 November 2026 |
| Change | 4, 16 November 2026, D-RCV-36: Temporal workflow security with mTLS, Entra ID OIDC and a break-glass codec server; every payload encrypted by the PdpaPayloadCodec; temporal_svc and recovery_svc isolation; embedded Drools rule packages authored by RW-COE, approved by RW-RISK and stored with a checksum (sections 1, 4, 5, 7, 8, 9, 10) |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts, with C4 component views and ISO/IEC/IEEE 42010 viewpoints |


# 1. The design on one page

| Concern | Design | Status |
|---|---|---|
| Sign-in | Entra ID single sign-on with multi-factor authentication through the ACE front end; OpenID Connect with the authorization code flow and PKCE | ACE pattern |
| Case workflow engine | Temporal, self-hosted in the rwb-recovery namespace. mTLS between the worker, frontend and internal services. Web UI behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode only through the codec server (E1-070, E2-038) | Designed; D-RCV-36, ADR-011 |
| Rule packages | Embedded Drools. RW-COE authors a package and RW-RISK approves it; the author cannot approve. SY-RULES evaluates it, and the workbook and DRL are stored with a checksum (ADR-012) | Designed; D-RCV-36 |
| Identity to role | Entra ID group membership, granted through bank IAM, maps to Workbench roles held as data | Agreed; groups DL40 |
| Permission check | Every endpoint checks the role, the capability area, the right and the scope before it runs | Designed |
| Scope | Own cases, team, region or all, applied as a filter on every query | Designed |
| Approval limits | The delegation of authority table checked before an approval is accepted | Designed; limits DL18 |
| Masking | Personal fields masked in the response at the API unless the role may see them (E1-037). The national ID is never read in clear: v_ace_customer returns id_no_masked and id_no_last4 only. Every read of a personal field is audited | Designed; rules DL26 |
| Sessions | Token lifetime, inactivity timeout and break-glass window set by SCB IT security | Open, DL38 |
| Partners | Separate partner identities through the external gateway, limited to the cases placed with the firm | Open, DL03 |
| Service identities | Managed identities with credentials in Key Vault; one identity per non-human actor. No data load identity: ACE ingests every source | ACE pattern |
| ACE data access | Read only. The recovery service role holds SELECT on the recovery.v_ace_* views and nothing else; the views are owned by ace_view_owner, which reads the public ACE tables. No direct public read, no write, PUBLIC revoked | Designed; D-RCV-35, RWB-E1-069 |
| Logging | Access log in the Workbench, ACE audit log, PII log through PII Kafka, security events to the SOC log | ACE pattern |


# 2. Context

The Workbench is a module of the ACE service. It reuses the ACE sign-in, access check, audit, PII logging and SOC logging. The recovery module adds its roles, permissions, scope rules, masking rules and approval limits as data, and checks them on every request. The Workbench loads, copies and transforms no source data. ACE ingests every source into the ACE database, and the recovery module reads it only through SELECT-only recovery.v_ace_* views (D-RCV-35, ADR-010).

| Actor | How it reaches the Workbench | Identity |
|---|---|---|
| Bank staff | ACE front end on the bank network, through the internal application gateway with web application firewall | Entra ID user with multi-factor authentication |
| Partners | Partner portal through the external gateway, once external access is approved (DL03) | Partner identity, separate from bank identities |
| Customers | No sign-in. Offers and listings reach them through SCB Easy, LINE OA, SMS, branches and HOME.SCB | Bank channel identity |
| Non-human actors | Service to service inside the ACE namespace; outbound through the outbox | Managed identity |
| Agents | Through the tool gateway only | Managed identity per agent, limited by the autonomy level |


# 3. Sign-in and sessions

## 3.1 Sign-in flow

- The person opens the ACE front end. The front end redirects to Entra ID with the authorization code flow and PKCE.

- Entra ID applies multi-factor authentication and the bank conditional access policies.

- The front end receives the tokens. The ID token names the person; the access token carries the group claims for the ACE application.

- On the first request the service resolves the groups to Workbench roles, the scope and the masking profile, and writes the session start to the access log.

- A person with no Workbench role is refused with MSG-P4-001. A person whose groups hold a conflicting role pair is refused and an incident is raised.

## 3.2 Session rules

| Rule | Value used until DL38 is decided | Set by |
|---|---|---|
| Access token lifetime | The ACE value | SCB IT security |
| Inactivity timeout | 15 minutes, with a warning at 13 minutes | SCB IT security |
| Maximum session length | One working day | SCB IT security |
| Group change | Takes effect at the next request; a removed role ends the session | Workbench |
| Concurrent sessions | One active session per person per device | Workbench |
| Break-glass window | Four hours, then the grant ends with no action by anyone | SCB IT security |


# 4. The permission check

Every endpoint declares the capability area and the right it needs. The check runs in the service before any data is read, using the role permissions in force for the request date.

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

## 4.1 Rights on the new objects

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


# 5. Personal data protection

| Control | Design |
|---|---|
| National ID | ACE holds the national ID or passport number (customer.identification_number). The Workbench never reads it in clear: v_ace_customer returns id_no_masked, with only the last four digits shown, and id_no_last4. Nothing is tokenized at load, because there is no load; role masking at the API (E1-037) replaces the former id_no_token |
| Tokenization | None at load. There is no Workbench load to tokenize, so there is no id_no_token column and no token vault in the source path. Masking is applied in v_ace_customer (id_no_masked, id_no_last4) and by E1-037 at the API |
| Masking | Name, address, phone, email and account numbers are masked at the API by the masking profile of the role (E1-037). v_ace_contact returns the full phone, email and address, because notices and calls need them, so the API mask is the control. The profile is a data row per role and field |
| Unmasking | A role allowed to unmask a field does so per record; each unmask is written to the PII log |
| Audit of reads | Every read of a personal field, including each read through v_ace_customer and v_ace_contact, is written to the PII log through PII Kafka. The control is the read-only grant, E1-037 masking and the audit log together; the mask in a view is not a PDPA control on its own |
| Exports | Exports carry the masking of the person who runs them. A debt sale data tape passes the masking check before the data room opens |
| Test data | Synthetic only in DEV. Masked copies from the PII service in SIT and UAT |
| Logs and prompts | No personal data in application logs, test fixtures or agent prompts. The PDPA lint gate checks code before merge |
| Retention | Each data product and document type carries a retention class (DL26). Expiry is held while a legal hold is in place |
| Workflow history | Every Temporal payload is encrypted by PdpaPayloadCodec (AES-GCM) with a key in Azure Key Vault before it is written. Workflow history never holds clear personal data. Search attributes carry CaseId, Stage, ProductGroup and QueueCode only. Key rotation keeps old histories decodable (E2-038) |
| Rule facts | Drools evaluates facts in memory inside the recovery module. The decision log stores the rule ID and the package version; rule packages and the rule catalog hold no personal data |


# 6. Partners

- Partner users reach the partner portal through the external gateway once the architecture team approves external access (DL03).

- Each partner user has a partner identity, separate from bank identities, with multi-factor authentication.

- The partner and agency manager requests partner users; the role owner approves. Accounts end when the firm's contract ends.

- A partner user sees only the instructions placed with their firm. Scope is the firm, set on the instruction.

- Partner uploads pass a file type check and a malware scan before they reach the document hub.

- Until external access is in place, partners keep their current channels and bank staff record partner results.

# 7. Service identities and secrets

| Item | Design |
|---|---|
| Managed identities | One per non-human actor: case workflow (SY-CASEWF), Drools rules engine (SY-RULES), OCR pipeline, decision log writer, agent platform |
| Load identity | None. The Workbench runs no inbound load, so it holds no source load identity, no file share credential and no staging account. ACE ingestion uses its own identity and writes the ACE tables |
| Secrets | Key Vault, reached by managed identity. No secret in code, configuration or prompts. The secret scan gate checks every merge |
| Database | The service connects with its managed identity. The recovery schema is still owned by the service; people do not hold write access in production. No recovery migration creates or alters a table in the ACE public schema |
| Read-only ACE access | The recovery service role (recovery_svc) holds USAGE on schema recovery and SELECT on the recovery.v_ace_* views only. It holds no SELECT on any public ACE table and no INSERT, UPDATE, DELETE or TRUNCATE on any ACE table or view, so a direct public read or a write fails in the database catalog, not only in code review. This is the read-only ACE service identity of the Admin and Access Model v5 |
| View owner | The v_ace_* views are owned by ace_view_owner, a NOLOGIN ACE role that holds SELECT on the public ACE tables the views read and writes neither schema. It is not a Workbench role and nobody signs in as it. A view runs with its owner's privileges, so any row-level security ACE adds later is applied inside the view |
| PUBLIC | All privileges on the recovery tables and views are revoked from PUBLIC. A role reads a view only through an explicit grant |
| Grant check | The view conformance test in RWB-E1-069 runs in the pipeline and fails the build if recovery_svc can select a public table or write any table, if a v_ace_* view does not compile, or if a constraint in schema recovery references a public table |
| Agents | An agent reaches a system only through the tool gateway. The gateway holds the permissions; the agent holds none |
| Network | Private endpoints to storage and the database. No public endpoint on the service |
| temporal_svc isolation | temporal_svc owns the temporal and temporal_visibility databases. It has no grant on the ACE database, no read on any recovery.v_ace_* view and no sign-in right. Its only purpose is the Temporal persistence |
| recovery_svc isolation | recovery_svc has no grant on temporal or temporal_visibility and cannot read workflow history through SQL. It reads the ACE database only through the read-only recovery.v_ace_* views |
| Temporal certificates | mTLS certificates for the worker, frontend and internal services are issued from Key Vault and rotated there. The frontend gRPC port 7233 is internal only |
| Codec server | Runs with its own managed identity and the Key Vault key reference. A decode is open only to RW-SECADM inside an open break-glass session |
| Rule store | Rule workbooks and generated DRL are stored with a checksum. Only RW-COE uploads a version, only RW-RISK approves it, and SY-RULES reads the package in force and the catalog |


## 7.1 Temporal security

Temporal uses the same identity, transport and audit controls as the rest of the Workbench. The difference is that a workflow history holds payloads, so the codec and the decode right carry the personal data control.

| Control | Design |
|---|---|
| Transport | mTLS between the worker, the frontend and the internal services. Certificates come from Key Vault and rotate there. The frontend gRPC port 7233 is internal only |
| Web UI | Entra ID OIDC. RW-PLATADM operates and RW-AUDIT reads. Any role other than those two is refused with MSG-P4-002 |
| Payload decode | RW-SECADM only, through the codec server, with an open break-glass session (E1-039). Every decode is logged. Any other role is refused with MSG-P4-002 |
| Authorizer plugin | The Temporal authorizer plugin (TemporalAuthorizerPlugin) maps the OIDC role claim and the client certificate to the Workbench role. A call outside the role's right is refused with MSG-P4-002 (E2-038) |
| Admin audit | TemporalAdminAuditListener reads the Temporal frontend audit log and writes start, signal, terminate, reset and decode actions to the decision log (E2-038) |
| Payload codec | PdpaPayloadCodec: AES-GCM, key in Azure Key Vault, every payload encrypted before it leaves the worker. History never holds clear personal data. Key rotation keeps old histories decodable (E2-038) |
| Isolation | temporal_svc has no grant on the ACE database and recovery_svc has no grant on the Temporal databases. Neither role is a sign-in role |


## 7.2 Drools rule security

A rule package is business logic held as data, so it has the same maker-checker control as a reference load and an integrity check on every load.

| Control | Design |
|---|---|
| Authoring | RW-COE writes each package as an Excel workbook in Drools decision-table format and uploads a version. Only RW-COE writes a rule package |
| Approval | RW-RISK approves or rejects a version. The author cannot approve its own package; the check is on the person and on the role |
| Evaluation | SY-RULES evaluates an approved version in force through RuleEvaluator. It holds read only on the package version and the rule catalog |
| Integrity | The workbook and the generated DRL are stored with a checksum. A checksum mismatch refuses the version at load and raises an incident |
| No release | A version moves from upload to in force without a code release; rollback is one call |
| Traceability | The decision log records the rule ID (the Drools rule name) and the package version label for every decision |


# 8. Logging and monitoring

| Record | Holds | Read by |
|---|---|---|
| Access log | Sign-ins, refusals, grants, removals, break-glass use and the versions in force. Append only | Application owner, security administrator, Compliance, internal audit |
| Decision log | Every decision with inputs, rule version, recommendation, approver and action. Append only and hash chained | Internal audit, Risk, center of excellence |
| ACE audit log | Every change made through the service | Security administrator, internal audit |
| PII log | Every read and unmask of a personal field, including reads through v_ace_customer and v_ace_contact, through PII Kafka | Compliance, internal audit |
| SOC log | Security events: repeated refusals, conflict refusals, break-glass, failed sign-ins | SCB security operations |
| Temporal audit log | Workflow start, signal, terminate, reset and every Web UI or CLI admin action, read by TemporalAdminAuditListener. Append only | Security administrator, internal audit |
| Codec decode log | Every payload decode with the person, the break-glass session, the workflow ID and the time. Append only | Security administrator, Compliance, internal audit |


# 9. Threats and controls

| Threat | Example | Control |
|---|---|---|
| Spoofing | A stolen password used to sign in | Multi-factor authentication; conditional access; SOC alert on unusual sign-in |
| Tampering | A decision or legal document changed after the fact | Append-only, hash-chained decision log; write-once container for legal documents; no write grant on any ACE table or view |
| Repudiation | An approver denies approving | Decision log entry with the approver identity, level and time |
| Information disclosure | Customer data read outside the role or sent outside the bank | Scope filter; masking (E1-037); national ID masked in v_ace_customer; SELECT on recovery.v_ace_* only, no direct public read; PII log; no personal data in exports beyond the role |
| Denial of service | A partner floods the portal | External gateway rate limits; web application firewall |
| Elevation of privilege | A person grants themselves a business role | Separation of duty at grant and at sign-in; access review every six months (DL38) |
| Workflow history disclosure | A payload or history read outside the role | PdpaPayloadCodec; mTLS; OIDC roles; decode only through the codec server in break-glass and every decode logged |
| Rule package tampering | A rule changed or loaded without approval | RW-COE author and RW-RISK approval; checksum on the workbook and the DRL; append-only decision log |


# 10. Tests before each release

| Test | Passes when | Signed by |
|---|---|---|
| Sign-in per role | Each role in the release signs in and shows the right roles, scope and masking | Role owner |
| Endpoint permissions | An automated test calls every endpoint with a role that lacks the right and receives 403 | QA lead |
| Scope | A role reads a record outside its scope and receives 404 | QA lead |
| Masking | Three roles read the same case and see the fields their profiles allow | Compliance |
| Read-only ACE grant | The view conformance test passes: recovery_svc reads every v_ace_* view, cannot select a public table and cannot insert, update or delete on any table | Tech lead |
| Approval limit | An approval above the limit routes to the next level | Risk |
| Container and secret scans | No vulnerability above the bank threshold; no secret in code | Tech lead |
| Penetration test | Before the partner portal opens to users outside the bank | SCB IT security |
| Temporal mTLS | A client without a valid certificate is refused, and the worker, frontend and internal services connect over mTLS | Tech lead |
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

