<!-- source: 05 Technical architecture/Recovery Workbench Environment and Deployment Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Environment and Deployment Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Environment and deployment design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench environment and deployment design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 deployment view, with C4 deployment and ISO/IEC/IEEE 42010 viewpoints |

# 1. The design on one page

| Element | Design | Status |
|---|---|---|
| Where it runs | The ACE service on the shared ACE AKS clusters in the SCB Azure tenant, Southeast Asia region | Agreed |
| Environments | DEV, SIT, UAT and PROD on one pattern, built from code | Agreed |
| Deployment slots | Four in DEV and two in SIT planned, so squads test in parallel; one of each available today | Open, DL35 |
| Repository | One ACE repository with common, collection and recovery modules | Agreed |
| Module set-up | TechX builds in its own package from 2 November; the ACE team applies the module boundaries | Assumed, DL05 |
| Branching | Trunk based, with short branches merged into main at least once a working day | Agreed |
| Merge owner | Each squad merges into its own module through code owners; the ACE team owns the common module and the release decision | Assumed, DL04 |
| Feature flags | Every unfinished or cross-squad change is behind a flag held as configuration per environment | Agreed |
| Release | One production release at each month end, shared with the collection squad | Agreed; window DL34 |

# 2. Environments

| Environment | Purpose | Data | Deployed | Who uses it |
|---|---|---|---|---|
| DEV | Build and developer testing | Synthetic only | On every merge into main | Squads |
| SIT | System and integration testing against the SCB test systems | Masked copies from the PII service | On a release tag | QA with SCB IT |
| UAT | Business acceptance | Masked copies from the PII service | In the week before each release | Business testers |
| PROD | Live service | Live | In the monthly change window | Bank staff and partners |

No production data reaches DEV. Each environment holds its own configuration, feature flag values, secrets and Entra ID groups.

# 3. What runs in each environment

| Component | What it is | Shared with ACE |
|---|---|---|
| Service | The ACE Spring Boot service with the recovery module, in the ACE namespace | Yes |
| Front end | The ACE React front end with the recovery module folder | Yes |
| Database | PostgreSQL flexible server, zone redundant, with the recovery schema | Same server; own schema |
| Document storage | Blob storage with a write-once container for legal document types | New containers |
| Secrets | Key Vault, reached by managed identity. No secret in code, configuration or prompts | Yes |
| Ingress | Internal application gateway with web application firewall for staff; the external gateway for partners (DL03) | Yes |
| Network | Private endpoints to storage and the database | Yes |
| Scheduler | Quartz for timers and scheduled jobs; Spring Batch for loads and outbound files | Yes |
| Identity | Entra ID single sign-on with multi-factor authentication; managed identities for services | Yes |
| Logs | Log Analytics for logs, traces and metrics; PII Kafka and the SOC log | Yes |
| Model endpoint | Private endpoint in the SCB tenant | Open, DL33 |

# 4. The pipeline

## 4.1 Gates before merge

| Gate | Checks |
|---|---|
| 1 Build and unit tests | The service builds and every unit and rule table test passes |
| 2 Lint | Code style and the naming rules |
| 3 Secret scan | No credential, key or token in the code |
| 4 PDPA lint | No personal data in code, tests or log statements |
| 5 Container scan | No known vulnerability above the bank threshold in the image |
| 6 Module boundary | No call or table read across a module boundary |
| 7 Integration and contract tests | Modules work with the database and the generated types |
| 8 AI first-pass review | Bugs, security, PDPA and style, with a summary on the pull request |
| 9 Human approval | One named reviewer, and the code owner where another module is touched |

## 4.2 The release path

| Step | When | Approved by |
|---|---|---|
| Deploy to DEV | On every merge into main | Pipeline |
| Deploy to SIT | On a release tag | Tech lead |
| SIT exit | After one week of SIT | QA lead with SCB IT |
| Deploy to UAT | In the week before the release | QA lead |
| UAT exit | After the business scripts are signed | Business lead |
| Deploy to PROD | In the monthly change window | Release owner in the ACE team with the application owner |
| Rollback | Switch the feature flag off first; redeploy the previous tag if a flag does not cover the fault | Release owner |

# 5. Database changes

- Every schema change is a versioned migration script in the recovery module, run by the pipeline in each environment in order.

- Schema names are parameters, so the same script runs in every environment.

- A migration that changes data shape runs behind a feature flag until both code paths are no longer needed.

- Reference data, rules, limits and lists of values load through the validated load, not through migrations.

- The decision log and the interaction ledger are append only; migrations never update or delete their rows.

# 6. Feature flags

| Rule | Detail |
|---|---|
| What a flag does | Chooses between the new code path and the previous one. Off returns the previous path |
| Where it is held | As configuration for each environment. Changing a value needs no code release |
| What it records | Name, owner, story key, value in each environment, and the release in which it is removed |
| At release | A change that fails SIT or UAT has its flag switched off and the release goes ahead without it |
| Removal | The old path and the flag are removed in the release after the flag is switched on in production |

# 7. Resilience and recovery

| Item | Design | Status |
|---|---|---|
| Availability | 99.9% in business hours | Proposed, DL11 |
| Recovery point and time | Set by SCB IT for the ACE service | Open, DL11 |
| Database | Zone-redundant PostgreSQL with point-in-time restore | ACE pattern |
| Documents | Blob storage backup on the bank schedule; restore tested before the first production release | Open, DL27 |
| Agent or model outage | The rule result is used and the case still routes | Designed |
| Load failure | The previous load stays in use and the data product is marked stale | Designed |

# 8. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL04 | Who merges between the recovery and collection squads | Each squad merges into its own module; the ACE team owns the common module and the release decision |
| DL05 | Who creates the recovery module in ACE | TechX builds in its own package from 2 November; the ACE team applies the boundaries |
| DL11 | Non-functional target values | The ACE values where ACE has them; the solution architect proposes the rest |
| DL27 | Storage, backup, legal hold and e-discovery for the document hub | The ACE storage pattern with a write-once container and the bank backup service |
| DL33 | The model endpoint the agents call | A private endpoint in the SCB tenant |
| DL34 | The monthly production release window | The last working week of each month |
| DL35 | Further ACE deployment slots | One DEV and one SIT slot shared by all squads |
| DL37 | Code owners and the browser test runner | Tech leads review every pull request; QA runs browser tests outside the pipeline |
