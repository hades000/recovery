<!-- source: 05 Technical architecture/Recovery Workbench Security and Access Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Security and Access Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Security and access design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench security and access design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts, with C4 component views and ISO/IEC/IEEE 42010 viewpoints |

# 1. The design on one page

| Concern | Design | Status |
|---|---|---|
| Sign-in | Entra ID single sign-on with multi-factor authentication through the ACE front end; OpenID Connect with the authorization code flow and PKCE | ACE pattern |
| Identity to role | Entra ID group membership, granted through bank IAM, maps to Workbench roles held as data | Agreed; groups DL40 |
| Permission check | Every endpoint checks the role, the capability area, the right and the scope before it runs | Designed |
| Scope | Own cases, team, region or all, applied as a filter on every query | Designed |
| Approval limits | The delegation of authority table checked before an approval is accepted | Designed; limits DL18 |
| Masking | Personal fields masked in the response unless the role may see them; national ID tokenized at load | Designed; rules DL26 |
| Sessions | Token lifetime, inactivity timeout and break-glass window set by SCB IT security | Open, DL38 |
| Partners | Separate partner identities through the external gateway, limited to the cases placed with the firm | Open, DL03 |
| Service identities | Managed identities with credentials in Key Vault; one identity per non-human actor | ACE pattern |
| Logging | Access log in the Workbench, ACE audit log, PII log through PII Kafka, security events to the SOC log | ACE pattern |

# 2. Context

The Workbench is a module of the ACE service. It reuses the ACE sign-in, access check, audit, PII logging and SOC logging. The recovery module adds its roles, permissions, scope rules, masking rules and approval limits as data, and checks them on every request.

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

# 5. Personal data protection

| Control | Design |
|---|---|
| Tokenization | The national ID and passport number are tokenized at load. The clear value is not stored in the Workbench |
| Masking | Name, address, phone, email and account numbers are masked by the masking profile of the role. The profile is a data row per role and field |
| Unmasking | A role allowed to unmask a field does so per record; each unmask is written to the PII log |
| Exports | Exports carry the masking of the person who runs them. A debt sale data tape passes the masking check before the data room opens |
| Test data | Synthetic only in DEV. Masked copies from the PII service in SIT and UAT |
| Logs and prompts | No personal data in application logs, test fixtures or agent prompts. The PDPA lint gate checks code before merge |
| Retention | Each data product and document type carries a retention class (DL26). Expiry is held while a legal hold is in place |

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
| Managed identities | One per non-human actor: case workflow, rules component, data load, OCR pipeline, decision log writer, agent platform |
| Secrets | Key Vault, reached by managed identity. No secret in code, configuration or prompts. The secret scan gate checks every merge |
| Database | The service connects with its managed identity. The recovery schema is owned by the service; people do not hold write access in production |
| Agents | An agent reaches a system only through the tool gateway. The gateway holds the permissions; the agent holds none |
| Network | Private endpoints to storage and the database. No public endpoint on the service |

# 8. Logging and monitoring

| Record | Holds | Read by |
|---|---|---|
| Access log | Sign-ins, refusals, grants, removals, break-glass use and the versions in force. Append only | Application owner, security administrator, Compliance, internal audit |
| Decision log | Every decision with inputs, rule version, recommendation, approver and action. Append only and hash chained | Internal audit, Risk, center of excellence |
| ACE audit log | Every change made through the service | Security administrator, internal audit |
| PII log | Every read and unmask of a personal field, through PII Kafka | Compliance, internal audit |
| SOC log | Security events: repeated refusals, conflict refusals, break-glass, failed sign-ins | SCB security operations |

# 9. Threats and controls

| Threat | Example | Control |
|---|---|---|
| Spoofing | A stolen password used to sign in | Multi-factor authentication; conditional access; SOC alert on unusual sign-in |
| Tampering | A decision or legal document changed after the fact | Append-only, hash-chained decision log; write-once container for legal documents |
| Repudiation | An approver denies approving | Decision log entry with the approver identity, level and time |
| Information disclosure | Customer data read outside the role or sent outside the bank | Scope filter; masking; PII log; no personal data in exports beyond the role |
| Denial of service | A partner floods the portal | External gateway rate limits; web application firewall |
| Elevation of privilege | A person grants themselves a business role | Separation of duty at grant and at sign-in; access review every six months (DL38) |

# 10. Tests before each release

| Test | Passes when | Signed by |
|---|---|---|
| Sign-in per role | Each role in the release signs in and shows the right roles, scope and masking | Role owner |
| Endpoint permissions | An automated test calls every endpoint with a role that lacks the right and receives 403 | QA lead |
| Scope | A role reads a record outside its scope and receives 404 | QA lead |
| Masking | Three roles read the same case and see the fields their profiles allow | Compliance |
| Approval limit | An approval above the limit routes to the next level | Risk |
| Container and secret scans | No vulnerability above the bank threshold; no secret in code | Tech lead |
| Penetration test | Before the partner portal opens to users outside the bank | SCB IT security |

# 11. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL01 | Whether access is granted centrally or by the application owner | Application owner administration |
| DL03 | How partners reach the partner portal from outside the bank | Partners keep current channels until external access is approved |
| DL26 | Retention and masking per data product and document type | Masking profiles as proposed in the data classification |
| DL38 | Session, inactivity and break-glass timers | The values in 3.2 |
| DL40 | Entra ID groups for the Workbench roles | One group per role per environment |
