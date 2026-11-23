SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Environment and deployment design

| Item | Detail |
|---|---|
| Document | Recovery Workbench environment and deployment design |
| Version | 5 |
| Date | 22 November 2026 |
| Supersedes | Version 4, 16 November 2026 |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | arc42 deployment view, with C4 deployment and ISO/IEC/IEEE 42010 viewpoints |


This version realigns the deployment view to Architecture v5: Recovery runs inside ACE as 19 services, one per business module, each an API deployment and a worker deployment, each with its own schema and login in the ACE database, its own Kafka topic and its own Temporal task queue (ADR-013, ADR-014, ADR-015, ADR-016). Every section, ID, number and date of version 4 is kept; section 9 lists what changed. No approval of version 5 is recorded, so the document is issued as Draft (ASM-B-TECH-05-1). No release date is written in any source; the monthly release window is the only cadence, and any date added later is tentative (ASM-B-TECH-05-9).

# 1. The design on one page

| Element | Design | Status |
|---|---|---|
| Where it runs | The 19 services on the shared ACE AKS clusters in the SCB Azure tenant, Southeast Asia region, in one Kubernetes namespace, rwb-recovery | Agreed; ADR-013 |
| Case workflow engine | Temporal, self-hosted on the ACE AKS clusters, one cluster per environment with the Temporal namespace rwb-recovery and one task queue per service, rwb-<short>. Case data stays in the ACE database (D-RCV-36, ADR-011, ADR-016) | Agreed; RWB-E1-070 |
| Source data | Read from the ACE database through read-only recovery.v_ace_* views by rwb-source-data alone. The Workbench runs no inbound load and receives no source file | Agreed; D-RCV-35 |
| Deployment dependency | RWB-ACE-001, the ACE tables and columns the Section B views read, is a deployment dependency, not a parallel workstream. DL43 must be accepted by 21 November 2026 and the additions must land in each environment before the release that switches on a Section B feature | Blocking; DL43 |
| Environments | DEV, SIT, UAT and PROD on one pattern, built from code; each of the 19 services is deployed in all four | Agreed |
| Deployment slots | Four in DEV and two in SIT planned, so squads test in parallel; one of each available today | Open, DL35 |
| Repository | 19 service repositories created from one service template (RWB-PLT-TPL) and the shared libraries (RWB-PLT-LIB), with one Helm chart and one pipeline template | Agreed |
| Module set-up | One module per service. TechX builds in its own package from 2 November; the ACE team applies the module boundaries; the rule holds for each of the 19 services | Assumed, DL05 |
| Branching | Trunk based in each service repository, with short branches merged into main at least once a working day | Agreed |
| Merge owner | Each squad merges into the service it owns through code owners; the ACE team owns the shared libraries and the release decision | Assumed, DL04 |
| Feature flags | Every unfinished or cross-squad change is behind a flag held as configuration per environment and per service | Agreed |
| Release | One production release at each month end, shared with the collection squad, and each service releases on its own tag inside that window (ASM-B-TECH-05-10) | Agreed; window DL34 |


The 19 services are the deployment units. The shared platform pieces (gateway-bff with its Redis session store, Temporal, Kafka, the bank Airflow scheduler and observability) are not counted in the 19, and the four groups of Architecture v5 slide 4 (case and control, recovery routes, shared capabilities, data and AI) are reading groups, not deployment units.

# 2. Environments

| Environment | Purpose | Data | Deployed | Who uses it |
|---|---|---|---|---|
| DEV | Build and developer testing | Synthetic only | On every merge into main of the service it belongs to | Squads |
| SIT | System and integration testing against the SCB test systems | Masked copies from the PII service | On a release tag of the service | QA with SCB IT |
| UAT | Business acceptance | Masked copies from the PII service | In the week before each release | Business testers |
| PROD | Live service | Live | In the monthly change window | Bank staff and partners |


No production data reaches DEV. Each environment holds its own configuration, feature flag values, secrets and Entra ID groups. Every environment holds the ACE schema the views read; in DEV and in the pipeline test database it is the ACE schema with synthetic rows, so the views compile and return data.

The four environment names are DEV, SIT, UAT and PROD, and each of the 19 services is deployed in all four. The names a service takes inside an environment (Helm release, Kubernetes deployment, DNS name) are not fixed by any source: Not specified in the source documents (CG-B-TECH-05-1; ASM-B-TECH-05-2).

# 3. What runs in each environment

| Component | What it is | Shared with ACE |
|---|---|---|
| Services | 19 Spring Boot services, one per business module (P1 to P10 and S1 to S9), built from the service template and the shared libraries. Each has an API deployment of 2 pods for availability and a worker deployment scaled by KEDA, in the namespace rwb-recovery on the ACE AKS cluster. A service is released, scaled and reused on its own (ADR-013) | Yes; same cluster |
| Front end | The ACE React front end with the recovery module folder; gateway-bff composes the screens from the service APIs and holds the session in Redis (DP-19, ADR-019) | Yes |
| Database | PostgreSQL flexible server, zone redundant: the ACE database, with 19 schemas rwb_<short> and one login per service. A service reads and writes only its own schema, and rwb-source-data reads ACE tables only through the recovery.v_ace_* views (ADR-014, DP-01) | Same server and database; own schema and login |
| Document storage | Blob storage with a write-once container for legal document types. No load container, no inbound file folder and no file share: the Workbench receives no source files | New containers |
| Secrets | Key Vault, reached by a managed identity per service. No secret in code, configuration or prompts | Yes |
| Ingress | Internal application gateway with web application firewall for staff, routing /recovery/* and /api/recovery/* to gateway-bff; the partner gateway in the DMZ for partners (DL03, ADR-019) | Yes |
| Network | Private endpoints to storage and the database | Yes |
| Kafka | Business-event topics on the bank Kafka platform: one topic per service, rwb.<short>.events.v1, plus the shared rwb.decision-record.v1. 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, outbox and inbox in the schema of the producing and consuming service, retry 1 min, 10 min, 1 h then .dlt; Event Hubs Premium is the fallback (ADR-015) | Yes; separate topics and ACLs from PII logging |
| Scheduler | Quartz for the Epic 1 and Epic 2 scheduled jobs and Spring Batch for their automated chains (case creation, reconciliation, payment matching, allocation, write-off scan) and outbound files, with restart from the last chunk; JOB-05 timer check runs on Quartz behind the TimerScheduler port. From Epic 3, Temporal runs the case lifecycle with durable timers and retries. In the target each scheduled job is a Temporal Schedule or an event-started workflow in the owning service (JOB-02, JOB-03, JOB-04, JOB-06, JOB-07, JOB-08, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15, JOB-16, JOB-17, JOB-18, JOB-19, JOB-20, JOB-22), and the new services add no qrtz_ or batch tables (ADR-016; CG-B-TECH-05-7; ASM-B-TECH-05-7). No Spring Batch job loads source data | Yes; same Quartz and Spring Batch tables |
| Source loads | None. No load container, no inbound file folder, no file share, no staging table and no load job. ACE ingests every source and records each batch in ace_batch_run; rwb-source-data reads the batch record through v_ace_batch_status | ACE ingestion |
| Identity | Entra ID single sign-on with multi-factor authentication through ACE Common; one managed identity per service | Yes |
| ACE read role | recovery_svc, the ACE read role and the login of rwb-source-data: SELECT on the 30 recovery.v_ace_* views only, no direct public read, no write. ace_view_owner: a NOLOGIN ACE role that owns the views and holds SELECT on the ACE tables they read. PUBLIC is revoked. These are the names the ACE Source Views v1 grants use. The other 18 service logins hold USAGE on their own schema only and no grant on the views: their names are Not specified in the source documents (CG-B-TECH-05-4; ASM-B-TECH-05-5) | ace_view_owner is an ACE role |
| Logs | Log Analytics for logs, traces and metrics, with OpenTelemetry from every service (ADR-023); PII Kafka and the SOC log | Yes |
| Model endpoint | Private endpoint in the SCB tenant | Open, DL33 |
| Temporal server | Official Temporal Helm chart, Helm release rwb-temporal in the ACE namespace, one cluster per environment on the ACE AKS clusters. Services frontend, history, matching, internal-worker and web. Server and Java SDK versions are pinned to the SCB IT approved release: Temporal server 1.28.1 and Temporal Java SDK 1.31.0 (CG-B-TECH-05-3) | New; separate persistence |
| Temporal persistence | Databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, owned by temporal_svc. The schema is created by the Temporal schema tool in the pipeline (TemporalSchemaJob). temporal_svc has no grant on the ACE database and recovery_svc has no grant on either Temporal database | Same server, separate databases |
| Temporal grants | temporal_svc owns temporal and temporal_visibility and has no grant on the ACE database. recovery_svc has no grant on either Temporal database, and no other service login has one. The pipeline checks the denials in every environment | Separate roles; no cross-grant |
| Temporal namespace and queues | Namespace rwb-recovery in each cluster. One task queue per service, rwb-<short> (section 3.2), so each worker polls only its own queue; rwb-integration keeps multi-step outbound chains and rwb-platform keeps smoke and health workflows. Workflow IDs case-{caseId} and platform-smoke-{yyyymmdd}. Search attributes CaseId, Stage, ProductGroup and QueueCode, all Keyword and all free of personal data | New |
| Temporal worker | Runs in the worker deployment of each service and polls only that service's task queue. Connects to the frontend over mTLS with certificates from Key Vault. No worker runs in a separate container | New |
| Drools engine | Embedded in the worker of every service that evaluates rules; no separate deployment. rwb-decision governs the packages (ADR-017). KIE runtime libraries only, with no KIE Server, Business Central or KJAR. Rule workbooks and generated DRL are stored in Blob and the database with a checksum | Embedded |


Owners of the shared rows are the roles the sources name: the ACE platform team owns the Kafka cluster and Enterprise Architecture owns the broker choice (Arch v5 slide 39, decision 1; the sizing and the Event Hubs fallback stay open, CG-B-TECH-05-6); the Platform team and the ACE team own the Temporal cluster and the workflow kit (Arch v5 slide 39, decision 3, RWB-PLT-WF); the ACE team and the DBA own the schemas and logins (Arch v5 slide 39, decision 2, RWB-PLT-DB); P5 rwb-document owns the document containers. Every service row of the Ownership Map v1 (sheet Services) owns its schema, topic and task queue (ASM-B-TECH-05-8).

The Kubernetes namespace is not settled by the sources. Version 4 puts the service in the ACE namespace and installs the Temporal release there, while Architecture v5 draws the 19 services in a namespace named rwb-recovery. This version places the 19 services in rwb-recovery and keeps the Temporal release in the ACE namespace exactly as version 4 records it, and the question of one namespace or two is raised as a gap: Not specified in the source documents (CG-B-TECH-05-2; ASM-B-TECH-05-3). Temporal's own namespace, rwb-recovery, is a separate thing from the Kubernetes namespace and is unchanged.

## 3.1 Temporal platform

Temporal runs the case lifecycle from Epic 3. There is one Temporal cluster per environment (DEV, SIT, UAT and PROD), on the ACE AKS clusters, installed with the official Temporal Helm chart as Helm release rwb-temporal in the ACE namespace. Each cluster runs the frontend, history, matching, internal-worker and web services. The server and Java SDK versions are pinned to the release SCB IT approves at build. The approved versions recorded for this release are Temporal server 1.28.1 and Temporal Java SDK 1.31.0; a change of either version is a platform change under the release process.

Persistence is separate from the ACE database. The temporal and temporal_visibility databases sit on the zone-redundant PostgreSQL flexible server and are owned by temporal_svc. The pipeline runs the Temporal schema tool as TemporalSchemaJob before the service deploy, so no hand-made DDL is used. temporal_svc has no grant on the ACE database, and recovery_svc has no grant on the Temporal databases.

Each cluster registers the namespace rwb-recovery; ace-collection stays with the ACE team. Every service runs its own worker on its own task queue rwb-<short> (section 3.2), so rwb-case keeps the case workflows, rwb-integration keeps multi-step outbound chains and rwb-platform keeps the smoke and health workflows. Workflow IDs are case-{caseId} for a case and platform-smoke-{yyyymmdd} for the daily smoke workflow. The four search attributes are CaseId, Stage, ProductGroup and QueueCode, all Keyword and none carrying personal data. Closed workflows are retained for 30 days and archived to Blob in RWB-E2-039.

The pinned server version does not support the two Temporal features the target architecture uses. Architecture v5 requires 1.30 or later for Nexus and Worker Versioning, and the Temporal and Drools design states the same floor, while version 4 records server 1.28.1 as the approved release; the sources disagree, so 1.28.1 is kept as recorded until SCB IT approves a later release (CG-B-TECH-05-3; ASM-B-TECH-05-6). Nexus and Worker Versioning are therefore not used in the Epic 1 and Epic 2 scope.

mTLS protects every connection between the worker, the frontend and the internal services. Certificates are issued from Key Vault and rotated there. The frontend gRPC port 7233 is internal only and is not exposed through the application gateway. The Web UI sits behind Entra ID OIDC.

## 3.2 Per-service deployment

Every service has the same two-part shape and is deployed on its own (Arch v5 slides 2, 8 and 33). All 19 services sit in the one Kubernetes namespace rwb-recovery. The API deployment runs 2 pods for availability and is scaled on CPU or requests if ever needed; the worker deployment is scaled by KEDA on the Temporal task-queue backlog or Kafka consumer lag, down to zero for bursty work such as OCR or agent runs. At rest the estate is about 38 small deployments. The contract values below are those of the Ownership Map v1 (sheet Services); the Helm release, the Kubernetes deployment name and the DNS name of a service in each environment are Not specified in the source documents (CG-B-TECH-05-1; ASM-B-TECH-05-2).

| Code | Service | Wave | Schema | Topic | Task queue | API pods | Worker scaling |
|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | rwb_source_data | rwb.source-data.events.v1 | rwb-source-data | 2 | KEDA 0 to n |
| P2 | rwb-integration | 1 | rwb_integration | rwb.integration.events.v1 | rwb-integration | 2 | KEDA 0 to n |
| P3 | rwb-case | 1 | rwb_case | rwb.case.events.v1 | rwb-case | 2 | KEDA 0 to n |
| P4 | rwb-access | 1 | rwb_access | rwb.access.events.v1 | rwb-access | 2 | KEDA 0 to n |
| P5 | rwb-document | 1 | rwb_document | rwb.document.events.v1 | rwb-document | 2 | KEDA 0 to n |
| P6 | rwb-comms | 1 | rwb_comms | rwb.comms.events.v1 | rwb-comms | 2 | KEDA 0 to n |
| P7 | rwb-decision | 1 | rwb_decision | rwb.decision.events.v1 | rwb-decision | 2 | KEDA 0 to n |
| P8 | rwb-payment | 2 | rwb_payment | rwb.payment.events.v1 | rwb-payment | 2 | KEDA 0 to n |
| P9 | rwb-reporting | 1 | rwb_reporting | rwb.reporting.events.v1 | rwb-reporting | 2 | KEDA 0 to n |
| P10 | rwb-agent | 1 | rwb_agent | rwb.agent.events.v1 | rwb-agent | 2 | KEDA 0 to n |
| S1 | rwb-valuation | 3 | rwb_valuation | rwb.valuation.events.v1 | rwb-valuation | 2 | KEDA 0 to n |
| S2 | rwb-treatment | 2 | rwb_treatment | rwb.treatment.events.v1 | rwb-treatment | 2 | KEDA 0 to n |
| S3 | rwb-guarantee | 3 | rwb_guarantee | rwb.guarantee.events.v1 | rwb-guarantee | 2 | KEDA 0 to n |
| S4 | rwb-litigation | 3 | rwb_litigation | rwb.litigation.events.v1 | rwb-litigation | 2 | KEDA 0 to n |
| S5 | rwb-asset | 2 | rwb_asset | rwb.asset.events.v1 | rwb-asset | 2 | KEDA 0 to n |
| S6 | rwb-debtsale | 3 | rwb_debtsale | rwb.debtsale.events.v1 | rwb-debtsale | 2 | KEDA 0 to n |
| S7 | rwb-writeoff | 4 | rwb_writeoff | rwb.writeoff.events.v1 | rwb-writeoff | 2 | KEDA 0 to n |
| S8 | rwb-deviation | 2 | rwb_deviation | rwb.deviation.events.v1 | rwb-deviation | 2 | KEDA 0 to n |
| S9 | rwb-partner | 4 | rwb_partner | rwb.partner.events.v1 | rwb-partner | 2 | KEDA 0 to n |


The wave is the delivery wave of Architecture v5 slide 41 in which the service is created: P1, P2, P3, P4, P5, P6, P7, P9 and P10 in wave 1; P8, S2, S5 and S8 in wave 2; S1, S3, S4 and S6 in wave 3; S7 and S9 in wave 4. On top of the 19, gateway-bff runs as the edge service and Temporal runs as the platform release rwb-temporal; neither is a Recovery service. Per-service CPU, memory and autoscaling thresholds are not stated by any source (CG-B-TECH-05-5; ASM-B-TECH-05-4).

# 4. The pipeline

## 4.1 Gates before merge

| Gate | Checks |
|---|---|
| 1 Build and unit tests | The service builds and every unit, rule package and rule scenario test passes |
| 2 Lint | Code style and the naming rules |
| 3 Secret scan | No credential, key or token in the code |
| 4 PDPA lint | No personal data in code, tests or log statements |
| 5 Container scan | No known vulnerability above the bank threshold in the image |
| 6 Service boundary | No call or table read across a service boundary; a service reads and writes only its own schema rwb_<short>; only rwb-source-data reads the recovery.v_ace_* views (TE-001, ADR-010, ADR-014) |
| 7 Integration and contract tests | The service works with the database and the generated types; its REST, event and activity contracts pass against the fakes of its contract dependencies; the view conformance test passes against the ACE schema (section 5) |
| 8 AI first-pass review | Bugs, security, PDPA and style, with a summary on the pull request |
| 9 Human approval | One named reviewer, and the code owner where another service or a shared library is touched |


## 4.2 The release path

| Step | When | Approved by |
|---|---|---|
| Deploy to DEV | On every merge into main of the service | Pipeline |
| Deploy to SIT | On a release tag of the service | Tech lead |
| SIT exit | After one week of SIT | QA lead with SCB IT |
| Deploy to UAT | In the week before the release | QA lead |
| UAT exit | After the business scripts are signed | Business lead |
| ACE dependency gate | RWB-ACE-001 accepted and landed in the environment (DL43) before the release that turns on a Section B view | ACE team lead and release owner |
| Temporal schema job | Before the service deploy in every environment, after that service's migrations | Pipeline as temporal_svc |
| Per-service release | Any service may release alone on its own tag; the release note names the services it changes, and gateway-bff releases with the services whose screens it composes | Release owner in the ACE team with the application owner |
| Deploy to PROD | In the monthly change window, service by service | Release owner in the ACE team with the application owner |
| Rollback | Switch the feature flag off first; redeploy the previous tag of the service if a flag does not cover the fault | Release owner |


# 5. Database changes

- Every schema change is a versioned migration script in the service that owns the schema, run by that service's pipeline in each environment in order. Each service has its own Flyway sequence in its own schema rwb_<short> (DP-15, ADR-021); the 19 sequences are independent.

- V0001 is the baseline of the recovery schema (D-RCV-28), and the built migration is kept. The split of that schema into the 19 rwb_<short> schemas is new work: RWB-PLT-NF06-DB and the DB story of each service. No recovery migration creates or alters a table in the ACE public schema; the ACE tables and columns change only through the ACE team's own migrations (RWB-ACE-001).

- Two-migration rule. A view cannot be created over a table that does not exist, so the ACE views ship in two migrations. Section A, the 16 Tier 1 views over the ACE tables that exist today, with the grants and the revoke from PUBLIC, ships with RWB-E1-069 as the next free sequence after V0001.

- Section B, the 14 Tier 2 views over the tables and columns the ACE team adds, ships as a later sequence in the week RWB-ACE-001 lands in each environment. Until then the features that read the Section B views stay behind their feature flags, switched off.

- The Section A migration also creates or confirms the two database roles. ace_view_owner is a NOLOGIN ACE role that owns the 16 views and holds SELECT on the ACE tables they read. recovery_svc is the ACE read role and the login of rwb-source-data: USAGE on schema recovery and SELECT on the 16 views, and nothing else. PUBLIC is revoked. A direct read of a public table or any write fails in the catalog, not only in code review. The other 18 service logins hold USAGE on their own schema only and no grant on schema recovery; their names are Not specified in the source documents (CG-B-TECH-05-4; ASM-B-TECH-05-5).

- The pipeline runs the view conformance test after the migrations in every environment: every v_ace_* view compiles; no constraint in schema recovery references a public table; recovery_svc cannot select a public table directly and cannot insert, update or delete on any public or recovery table. A failure stops the deployment, so an ACE column change that breaks a view is found before release.

- In DEV and the pipeline test database the ACE schema runs first, then V0001, then Section A, then Section B once the ACE additions are present.

- Schema names are parameters, so the same script runs in every environment.

- A migration that changes data shape runs behind a feature flag until both code paths are no longer needed.

- Temporal tables are outside the recovery schema. temporal and temporal_visibility are created and upgraded by the Temporal schema tool in TemporalSchemaJob, which runs as temporal_svc before the service deploy. No recovery migration creates or alters a Temporal table.

- temporal_svc has no grant on the ACE database, and recovery_svc has no grant on the Temporal databases. The pipeline checks both denials in every environment.

- Reference data, limits and lists of values load through the validated load, not through migrations. Rule packages load through the rule package endpoints, not through a reference load (RWB-E1-073).

- The decision log and the interaction ledger are append only; migrations never update or delete their rows. Each service's local decision-record table and the central ledger in rwb_decision are covered by the same rule (ADR-022).

# 6. Feature flags

| Rule | Detail |
|---|---|
| What a flag does | Chooses between the new code path and the previous one. Off returns the previous path |
| Where it is held | As configuration for each environment and each service. Changing a value needs no code release |
| What it records | Name, owner, story key, value in each environment, and the release in which it is removed |
| At release | A change that fails SIT or UAT has its flag switched off and the release goes ahead without it |
| Removal | The old path and the flag are removed in the release after the flag is switched on in production |
| Flag ownership | The flag is held by the platform feature-flag library and served by rwb-integration's admin API (R-PREC default ruling); the flag belongs to the service whose change it protects |
| Flag naming | One flag per unfinished change in the owning service. The two Epic 1 and Epic 2 flags below keep the rwb.p3 prefix they were built with and are not renamed |
| rwb.p3.temporal | Starts the Temporal worker. Off leaves the worker unregistered and the smoke endpoint returns 404 |
| rwb.p3.drools | Opens the rule package endpoints. Off returns 404 on those endpoints and changes nothing else |


## 6.1 Environment parameters

The parameters below are set in each environment. A change needs no code release.

| Parameter | Value | Used by |
|---|---|---|
| temporal.target | rwb-temporal-frontend.{env}.svc.cluster.local:7233 | Temporal worker and WorkflowGateway |
| temporal.namespace | rwb-recovery | Temporal worker and WorkflowGateway |
| temporal.taskqueue.platform | rwb-platform | Smoke and health workflows |
| temporal.retention.days | 30 | Namespace registration and archive |
| drools.kiebase.cache.max | 20 | KieBaseRegistry |
| rules.testcases.min | 50 | Rule load validation and build gate |


Each service's worker also reads temporal.target and temporal.namespace from its own environment and polls the queue rwb-<short> of section 3.2; no separate parameter name for that queue is given by any source. The {env} token is kept exactly as version 4 writes it. No source resolves it to a value for the 19 services, and no source states whether the token is one shared value per environment or one value per service and environment: Not specified in the source documents (CG-B-TECH-05-1; ASM-B-TECH-05-2).

# 7. Resilience and recovery

| Item | Design | Status |
|---|---|---|
| Availability | 99.9% in business hours | Proposed, DL11 |
| Recovery point and time | Set by SCB IT for the ACE service | Open, DL11 |
| Database | Zone-redundant PostgreSQL with point-in-time restore | ACE pattern |
| Documents | Blob storage backup on the bank schedule; restore tested before the first production release | Open, DL27 |
| Agent or model outage | The rule result is used and the case still routes | Designed |
| Late ACE data | There is no Workbench load to fail. Data is stale when ace_batch_run, read through v_ace_batch_status, has no COMPLETED record for the business date at the Workbench cut-off. AceDataLate goes to the data steward, the data products show their last complete business date and are marked stale, and the data jobs start when the record arrives | Designed; D-RCV-35 |
| Service outage | A failed service pauses only its own work: the work waits on its task queue and its topic offset and resumes when it is back, while the other 18 keep running | Designed |
| Kafka down | Events wait in each service's outbox and are sent when the broker returns; nothing is lost | Designed |
| ACE database busy | Each service's pool is capped, so Recovery cannot starve ACE; reports read projections in rwb_reporting | Designed |
| Temporal | One cluster per environment, one worker per service. The temporal and temporal_visibility databases sit on the zone-redundant PostgreSQL server with point-in-time restore. A zone failover and a one-minor-version upgrade are tested in SIT. Closed histories are archived to Blob after 30 days (RWB-E2-039) | Designed |


# 8. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL04 | Who merges between the recovery and collection squads, now that each service has its own repository | Each squad merges into the services it owns; the ACE team owns the shared libraries and the release decision |
| DL05 | Who creates the 19 services in ACE and applies their boundaries | TechX builds in its own package from 2 November; the ACE team applies the boundaries, service by service |
| DL11 | Non-functional target values, including the per-service recovery point and time | The ACE values where ACE has them; the solution architect proposes the rest |
| DL27 | Storage, backup, legal hold and e-discovery for the document hub | The ACE storage pattern with a write-once container and the bank backup service |
| DL33 | The model endpoint the agents call | A private endpoint in the SCB tenant |
| DL34 | The monthly production release window | The last working week of each month |
| DL35 | Further ACE deployment slots | One DEV and one SIT slot shared by all squads |
| DL37 | Code owners and the browser test runner | Tech leads review every pull request; QA runs browser tests outside the pipeline |
| DL43 | Whether the ACE team accepts the RWB-ACE-001 scope and dates, needed by 21 November 2026 | Section A views only; the features that need the Section B views stay behind their flags |


The per-service naming of environments, the Kubernetes namespace of the 19 services, the 19 logins, the Temporal server version and the scheduler cut-over are not decisions of this table; they are carried as gaps in this version (CG-B-TECH-05-1, CG-B-TECH-05-2, CG-B-TECH-05-3, CG-B-TECH-05-4 and CG-B-TECH-05-7) and are resolved in the verification loop.

# 9. Changes in this version

| Area | Version 4 | Version 5 | Basis |
|---|---|---|---|
| Deployment unit | One ACE service with the recovery module | 19 services, one per business module, each an API deployment and a worker deployment | ADR-013; Arch v5 slides 2, 8 and 33 |
| Repository and pipeline | One ACE repository with common, collection and recovery modules | 19 service repositories from one template, with one Helm chart and one pipeline template | RWB-PLT-TPL, RWB-PLT-LIB; Arch v5 slide 38 |
| Schema and login | One recovery schema and the recovery_svc login | 19 schemas rwb_<short>, one login per service; recovery_svc is the login of rwb-source-data | ADR-014; DP-01, DP-02 |
| Events | Outbox without a broker | Kafka topics rwb.<short>.events.v1 plus rwb.decision-record.v1, outbox and inbox per service | ADR-015 |
| Workflow | One worker polling three task queues | One worker per service polling rwb-<short>; rwb-platform keeps smoke and health | ADR-016 |
| Scheduling | Quartz and Spring Batch for Epic 1 and Epic 2 | A Temporal Schedule or an event-started workflow in the owning service from Epic 3; no new qrtz_ or batch tables | ADR-016; CG-B-TECH-05-7 |
| Rules | Drools embedded in the recovery module | Drools embedded in every service that decides, with the rule registry in rwb-decision | ADR-017 |
| Database changes | One migration sequence in the recovery schema | One Flyway sequence per service in its own schema | ADR-021; DP-15 |
| Edge | One front end with the recovery module | gateway-bff composite screens and the partner gateway | ADR-019; DP-19 |
| Pipeline gates | Module boundary at gate 6 | Service boundary at gate 6, contract tests per service at gate 7 | ADR-014, ADR-020 |
| Observability | Logs and traces for the module | OpenTelemetry from each of the 19 services | ADR-023 |
| Environments | Four environments for one service | Four environments for each service; the per-service names are open | CG-B-TECH-05-1 |
| Temporal version | Server 1.28.1 pinned | 1.28.1 kept as recorded; 1.30 or later is needed for Nexus and Worker Versioning | CG-B-TECH-05-3 |
| Kafka | Not covered | One topic per service, 12 partitions, replication factor 3, 7-day retention, retry and .dlt | ADR-015; Arch v5 slide 9 note |

