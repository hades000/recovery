<!-- source: 05 Technical architecture/Recovery Workbench Environment and Deployment Design v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Environment and Deployment Design v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Environment and deployment design

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench environment and deployment design |
| Version | 3 |
| Date | 15 November 2026 |
| Change | D-RCV-35 (ADR-010): no inbound load. Spring Batch runs automated chains on the ACE Quartz and Spring Batch tables; two-migration rule for the ACE views and the view conformance test; stale data from ace_batch_run lateness; no load containers, inbound file folders or file shares; DL43 is a deployment dependency (sections 1, 3, 4, 5, 7, 8) |
| Prepared by | Henka Group |
| Structure | arc42 deployment view, with C4 deployment and ISO/IEC/IEEE 42010 viewpoints |

# 1. The design on one page

| Element | Design | Status |
|---|---|---|
| Where it runs | The ACE service on the shared ACE AKS clusters in the SCB Azure tenant, Southeast Asia region | Agreed |
| Source data | Read from the ACE database through read-only recovery.v_ace_* views. The Workbench runs no inbound load and receives no source file | Agreed; D-RCV-35 |
| Deployment dependency | RWB-ACE-001, the ACE tables and columns the Section B views read, is a deployment dependency, not a parallel workstream. DL43 must be accepted by 21 November 2026 and the additions must land in each environment before the release that switches on a Section B feature | Blocking; DL43 |
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

No production data reaches DEV. Each environment holds its own configuration, feature flag values, secrets and Entra ID groups. Every environment holds the ACE schema the views read; in DEV and in the pipeline test database it is the ACE schema with synthetic rows, so the views compile and return data.

# 3. What runs in each environment

| Component | What it is | Shared with ACE |
|---|---|---|
| Service | The ACE Spring Boot service with the recovery module, in the ACE namespace | Yes |
| Front end | The ACE React front end with the recovery module folder | Yes |
| Database | PostgreSQL flexible server, zone redundant: the ACE database, with the recovery schema owned by the service. The recovery module reads ACE tables only through the recovery.v_ace_* views | Same server and database; own schema |
| Document storage | Blob storage with a write-once container for legal document types. No load container, no inbound file folder and no file share: the Workbench receives no source files | New containers |
| Secrets | Key Vault, reached by managed identity. No secret in code, configuration or prompts | Yes |
| Ingress | Internal application gateway with web application firewall for staff; the external gateway for partners (DL03) | Yes |
| Network | Private endpoints to storage and the database | Yes |
| Scheduler | Quartz for timers and scheduled jobs; Spring Batch for automated chains (case creation, reconciliation, payment matching, allocation, write-off scan) and outbound files, with restart from the last chunk. No Spring Batch job loads source data. Both share ACE's existing Quartz (qrtz_*) and Spring Batch (batch_job_*, batch_step_*) tables; the Workbench adds no qrtz_ or batch tables | Yes; same Quartz and Spring Batch tables |
| Source loads | None. No load container, no inbound file folder, no file share, no staging table and no load job. ACE ingests every source and records each batch in ace_batch_run; the Workbench reads the batch record through v_ace_batch_status | ACE ingestion |
| Identity | Entra ID single sign-on with multi-factor authentication; managed identities for services | Yes |
| ACE read role | recovery_svc, the recovery service role: SELECT on recovery.v_ace_* only, no direct public read, no write. ace_view_owner: a NOLOGIN ACE role that owns the views and holds SELECT on the ACE tables they read. PUBLIC is revoked. These are the names the ACE Source Views v1 grants use | ace_view_owner is an ACE role |
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
| 6 Module boundary | No call or table read across a module boundary; the recovery module reads ACE only through recovery.v_ace_* views (TE-001) |
| 7 Integration and contract tests | Modules work with the database and the generated types; the view conformance test passes against the ACE schema (section 5) |
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
| ACE dependency gate | RWB-ACE-001 accepted and landed in the environment (DL43) before the release that turns on a Section B view | ACE team lead and release owner |
| Deploy to PROD | In the monthly change window | Release owner in the ACE team with the application owner |
| Rollback | Switch the feature flag off first; redeploy the previous tag if a flag does not cover the fault | Release owner |

# 5. Database changes

- Every schema change is a versioned migration script in the recovery module, run by the pipeline in each environment in order.

- V0001 is the baseline of the recovery schema (D-RCV-28). No recovery migration creates or alters a table in the ACE public schema; the ACE tables and columns change only through the ACE team's own migrations (RWB-ACE-001).

- Two-migration rule. A view cannot be created over a table that does not exist, so the ACE views ship in two migrations. Section A, the 16 Tier 1 views over the ACE tables that exist today, with the grants and the revoke from PUBLIC, ships with RWB-E1-069 as the next free sequence after V0001.

- Section B, the 14 Tier 2 views over the tables and columns the ACE team adds, ships as a later sequence in the week RWB-ACE-001 lands in each environment. Until then the features that read the Section B views stay behind their feature flags, switched off.

- The Section A migration also creates or confirms the two database roles. ace_view_owner is a NOLOGIN ACE role that owns the 16 views and holds SELECT on the ACE tables they read. recovery_svc is the recovery service identity: USAGE on schema recovery and SELECT on the 16 views, and nothing else. PUBLIC is revoked. A direct read of a public table or any write fails in the catalog, not only in code review.

- The pipeline runs the view conformance test after the migrations in every environment: every v_ace_* view compiles; no constraint in schema recovery references a public table; recovery_svc cannot select a public table directly and cannot insert, update or delete on any public or recovery table. A failure stops the deployment, so an ACE column change that breaks a view is found before release.

- In DEV and the pipeline test database the ACE schema runs first, then V0001, then Section A, then Section B once the ACE additions are present.

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
| Late ACE data | There is no Workbench load to fail. Data is stale when ace_batch_run, read through v_ace_batch_status, has no COMPLETED record for the business date at the Workbench cut-off. AceDataLate goes to the data steward, the data products show their last complete business date and are marked stale, and the data jobs start when the record arrives | Designed; D-RCV-35 |

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
| DL43 | Whether the ACE team accepts the RWB-ACE-001 scope and dates, needed by 21 November 2026 | Section A views only; the features that need the Section B views stay behind their flags |
