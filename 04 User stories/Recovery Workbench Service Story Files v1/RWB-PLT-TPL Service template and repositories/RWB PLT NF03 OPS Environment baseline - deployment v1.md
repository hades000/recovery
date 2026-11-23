# RWB-PLT-NF03-OPS Environment baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF03-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-03 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-TPL-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: platform story for legacy NF-03 (moved, no impact), environment baseline — the four environments, their Temporal clusters and namespaces, their key stores, their database logins and pools and their data classes fixed once for the 19 services, with the legacy NF-03 story text absent from the source set, so the baseline is derived from Arch v5 slides 23, 24 and 29 and NFR-045 and NFR-052. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **the four environments DEV, SIT, UAT and PROD provisioned for all 19 services from the same chart and the same migration sequence, with only values that differ, each environment holding its own Temporal cluster and `rwb-recovery` namespace, its own key store, its own database logins and PgBouncer pools and its own data class**, so that **a build is promoted from DEV to SIT to UAT to production with no code change, and no environment can read another environment's secret, reach another environment's namespace or hold production data where it must not**.

### 2. Business rationale

The recovery workbench is 19 services that all follow one shape (Arch v5 slides 33 and 41): an API deployment with 2 fixed copies and a worker deployment scaled by KEDA on its own task queue, one schema `rwb_<name>` with one login in the ACE database, a topic `rwb.<name>.events.v1`, a REST base `/api/recovery/<name>/v1` and a task queue `rwb-<name>` in the namespace `rwb-recovery`. Wave 0 builds that shape once (slide 38: "Service template + Helm", "19 schemas + logins", "Temporal 1.30+") and every later wave only adds services. The cost of getting the environments wrong is therefore paid 76 times over: four environments times 19 services, each with a front end, a worker, a schema, a login, a pool, a namespace and a set of codec keys. A per-environment manual build produces four estates that drift apart in the first sprint, and the first promotion then needs a code change.

Arch v5 fixes the four things this story must provision. One cluster per environment: "One Temporal cluster per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server" (slide 23), and at runtime "one cluster, a namespace per workbench, a queue per service" (slide 24), with "the payload codec (AES-GCM, keys in Key Vault per namespace)" (slide 24) and the codec server for the UI. One database per bank but ownership per service: "the ACE PostgreSQL server … 19 Recovery schemas `rwb_<service>` … each service has one database login that owns its schema and has no grant on any other schema" and "each login goes through its own PgBouncer pool with a connection cap and statement timeout" (slide 29). One shared edge: the shared Azure App Gateway with WAF in front of the shared ACE AKS cluster (slide 8). The services never choose these; the platform fixes them once, and a service only supplies its short name.

Two non-functional requirements then decide what each environment may contain. NFR-045 forbids production data in development and requires masked copies in user acceptance. NFR-052 keeps every secret in the key store and out of code, configuration files and prompts. Together they mean that the isolation between environments is not a naming convention but a credential and network fact: DEV's login cannot see UAT's schema, DEV's pod cannot read UAT's Key Vault, and DEV's Temporal client cannot open UAT's namespace. Compared with the monolith, where one application and one `recovery` schema ran in each environment and the environment was chosen at deploy time by a properties file, the target has 19 logins, 19 pools and one namespace per environment, so the surface that must be isolated is much larger and must be produced by one baseline rather than by 19 teams.

**The legacy NF-03 story text is not in the source set.** The legacy index entry for NF-03 holds the title "Environment baseline", the group NF and empty metadata, requirements, acceptance criteria, test cases, messages and sections; there is no story file behind it. Nothing is therefore copied from a legacy story, and no legacy acceptance criterion or test case exists to preserve. The baseline above is derived from Arch v5 slides 8, 23, 24, 29, 33, 38 and 41 and from NFR-045 and NFR-052, which is the order of precedence of Template and Rules §R3 for a legacy key with no story text. The exact hosts, subscriptions, sizing, data refresh cadence and environment owners are not in any source in the set; they are recorded as one gap (GAP-1426) and its assumptions, and every value of that kind reads Not specified in the source documents (GAP-1426; ASM-2499).

This is a Wave 0 Day-1 enabler with no build dependency. It is what lets RWB-PLT-NF01-OPS deploy the same repository to four environments, RWB-PLT-N004-OPS install one chart four times with four values files, RWB-PLT-NF04-OPS resolve every credential from the key store of the environment and RWB-PLT-E1044-OPS run the same migration sequence in each environment. The chart itself, the secret and configuration baseline and the repository and pipeline baseline are those three stories; this story owns only the environment matrix they are installed into.

### 3. Preconditions

- Wave 0 exists as a programme phase: the platform epic RWB-PLT-TPL owns this story and no service is in build, so the environment matrix can be fixed before the first service is created (Arch v5 slide 38).
- The shared ACE AKS cluster and the shared Azure App Gateway with WAF are provisioned and reachable for the four environments, with the `/recovery/*` and `/api/recovery/*` routes reserved for the Recovery gateway-bff (Arch v5 slide 8).
- The one Helm chart and the golden pipeline of RWB-PLT-N004-OPS exist in their first version, with a values file as the only per-environment difference; this story writes the four values files and never a chart template.
- The secret and configuration baseline of RWB-PLT-NF04-OPS exists, so that a credential in a values file is a reference to a key, never a value (NFR-052).
- The repository and pipeline baseline of RWB-PLT-NF01-OPS exists, so that the same pipeline runs against DEV, SIT, UAT and PROD with an environment as a parameter.
- The ACE database team has created the ACE PostgreSQL server for each environment with the 19 schemas `rwb_<name>` and the 19 logins, and one PgBouncer pool per login with a connection cap and a statement timeout (Arch v5 slide 29; the schema and login stories of RWB-PLT-NF06-DB and the 19 services).
- The Temporal cluster of each environment exists in version 1.30 or later with its own persistence database, UI, metrics and codec server, and the namespace `rwb-recovery` is created in it with its own retention, quotas, certificates and codec keys (Arch v5 slides 23 and 24).
- A Key Vault exists per environment and per namespace scope, holding the codec keys (AES-GCM) and the database and service credentials of that environment only (Arch v5 slide 24; NFR-052).
- The 19-service list and the short names of Template and Rules §R4 are fixed, so that the matrix has a stable set of rows.
- The exact hosts, subscriptions, sizing, data refresh cadence and environment owners are Not specified in the source documents (GAP-1426; ASM-2499).

### 4. Flow

1. Fix the environment matrix in one file: four rows, DEV, SIT, UAT and PROD, each with its cluster, its region and subscription reference, its namespace, its key store, its database server, its PgBouncer pool set and its data class. Every field that names infrastructure is a reference, never a value in code.
2. Fix the per-service values that change between environments: the schema and login of the service, the pool size and the connection cap of its login, the Temporal frontend address and the task queue, the Key Vault name and the key identifiers of its codec and credentials, the Kafka bootstrap of the environment and the replica counts. The topic names, the event names, the REST paths and the 19 schemas are identical in all four environments and are not values.
3. Install the chart of RWB-PLT-N004-OPS into DEV from its values file with an immutable image digest, with `RWB_SCHEMA` set to the service's own schema for that environment and every credential resolved from the DEV key store at deploy time.
4. Run the environment check in DEV: the namespace `rwb-recovery` is reachable with the DEV client only, the DEV Key Vault resolves the DEV keys and no other, the DEV login reaches its own schema and is refused on every other schema, and the pool cap of the login is the value of the matrix.
5. Promote the same image digest to SIT through the promotion gate, install the same chart version with only the SIT values file, run the same migration sequence in the same order and repeat the environment check with the SIT credentials.
6. Repeat the promotion for UAT and then for PROD, each time with the values file and the key store of that environment and with no rebuild, no chart change and no code change; a promotion that needs any of the three is refused.
7. Prove the data class of each environment: DEV holds synthetic data only and refuses a production extract before reading any file; SIT and UAT hold masked copies produced by the masking path of the bank, with the UAT copy required by NFR-045; PROD holds production data and receives no copy from a lower environment.
8. Record the migration identity per environment: the SHA-256 of every migration file of every service is identical in DEV, SIT, UAT and PROD, and the Flyway history of a service is held in that service's own schema in that environment and in no other schema.
9. Publish the environment check, the four values files and the promotion gate as the baseline, and hand them to the service OPS stories, which inherit them and add no environment of their own.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A workload of one environment presents the credential of another environment | The database, the key store and the Temporal frontend each refuse the call; the environment check fails and names the two environments and the credential | None | AC2 |
| X2 | A secret is committed to a values file, a chart template or an image layer | The secret scan fails the pipeline, the deployment stops before any environment is touched, and the finding names the file and the key without printing the value | None | AC5 |
| X3 | A migration file differs between two environments, or names a schema literally | The schema check fails on the SHA-256 difference or on the literal schema name, the promotion is blocked at the gate and the two environments and the file are named | None | AC4 |
| X4 | A production extract is targeted at DEV | The DEV guard refuses the load before any file is read, and the refusal is reported with the source and the target environment | None | AC3 |
| X5 | An environment is installed from a different chart version or a different image digest | The promotion gate refuses the move, names the environment that carries the other version, and no partial promotion is recorded | None | AC1 |
| X6 | A pool reaches its connection cap or its statement timeout | The login's own pool queues or refuses the extra session, the ACE server stays protected, and the pool panel of RWB-PLT-N005-OPS shows the cap and the use of that login | None | AC2 |
| X7 | The codec keys of an environment are missing or rotated | The worker and the client fail to convert the payload, the codec server of that environment refuses the read, and the environment reports the key identifier that is missing | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list of §R4, the chart of RWB-PLT-N004-OPS, the key store of RWB-PLT-NF04-OPS and the ACE database layout of slide 29 only |
| Negotiable | The hosts, subscriptions, region pairing, sizing, pool caps, replica counts and promotion approver are agreed with the platform administrator and the solution architect; the four environments, the one cluster per environment, the namespace `rwb-recovery`, the one login and pool per service and the data classes are fixed |
| Valuable | Gives all 19 services and every later wave four environments that are the same shape, so a build promotes with no code change, and makes the boundary between environments a testable fact rather than a convention |
| Estimable | One environment matrix file, four values files, one promotion gate and four checks (isolation, schema and migration identity, secret scan, data class) |
| Small | Fits one sprint with the matrix, the four installs and the checks; the chart, the key store client and the schema creation belong to the other Wave 0 stories |
| Testable | Every criterion is tested against the four deployed environments, with a positive check per environment and a negative check across two environments |

### 7. Acceptance criteria

```gherkin
Feature: Environment baseline for the 19 services — DEV, SIT, UAT and PROD

  Background:
    Given the shared ACE AKS cluster and the shared App Gateway
    Given the 19-service list and the short names of Template and Rules §R4
    Given the chart of RWB-PLT-N004-OPS, the key store of RWB-PLT-NF04-OPS and the pipeline of RWB-PLT-NF01-OPS

  Scenario: AC1 The four environments run the same chart and the same migration sequence, and only values differ (new, D-RCV-60)
    Given the environment matrix with the four environments DEV, SIT, UAT and PROD
    And one Helm chart version and one image digest for a build
    When each environment is installed from the same chart version
    Then the rendered manifests differ only in the values file of the environment
    And the migration files are applied in the same order in every environment
    When that build is promoted from DEV to SIT, then to UAT and then to PROD
    Then no code change, no rebuild and no chart change is needed between the four environments
    And a promotion that would need a code change is refused by the promotion gate

  Scenario: AC2 Every environment has its own Temporal cluster, key store, credentials and PgBouncer pool, and no environment can reach another's (new, D-RCV-60)
    Given the four environments on the shared ACE AKS cluster
    When the environment matrix is reviewed against the deployed environments
    Then each environment has its own Temporal cluster with its own persistence database and the namespace rwb-recovery
    And each environment's namespace has its own codec keys in its own Key Vault
    And each of the 19 schemas and logins exists in that environment's ACE database with its own PgBouncer pool and connection cap
    When a workload of DEV presents the credential of UAT, or reads a secret of UAT, or calls the Temporal namespace of UAT
    Then each of the three attempts is refused and recorded as a finding of the environment check
    And no environment can reach another environment's namespace, secret or database pool

  Scenario: AC3 DEV holds synthetic data only, UAT holds masked copies, and no production data is in DEV (new, D-RCV-60)
    Given the data class fixed for each environment
    When the data of DEV is scanned against the production identifiers and the personal-data patterns
    Then DEV holds synthetic data only, with no production record and no production extract file
    And UAT holds masked copies, as NFR-045 requires, and SIT holds the masked copy loaded by RWB-ITG-TE004-ITG
    And PROD holds production data and receives no copy from a lower environment
    When a production extract is targeted at DEV
    Then the load is refused before any file is read and the refusal is reported

  Scenario: AC4 RWB_SCHEMA is set per service per environment and the same migration file is byte-identical everywhere (new, D-RCV-60)
    Given the schema and the login of each of the 19 services in each of the four environments
    When a service is deployed to an environment
    Then RWB_SCHEMA is set to that service's own schema in that environment
    And no schema name is written in code, in a migration file or in a chart template
    And the migration files of a service are byte-identical across DEV, SIT, UAT and PROD, compared by the SHA-256 of each file
    When a migration differs between two environments or names a schema literally
    Then the schema check fails, names the file and the two environments, and stops the promotion
    And the Flyway history of a service is held in its own schema and in no other schema

  Scenario: AC5 Environment hosts, credentials and sizing are configuration or secret references, and the chart carries none of them (new, D-RCV-60)
    Given the chart, the four values files and the image of a service
    When they are scanned for a host name, a connection string, a password, a token or a key
    Then none is found in code, in a chart template or in a committed values file
    And every host, port, pool size and replica count is a value of the environment's values file
    And every credential is a reference to that environment's key store, resolved at deploy time
    And a chart or an image that carries a host or a credential fails the pipeline check and is not deployed to any environment
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Four environments, DEV, SIT, UAT and PROD, and the same chart and the same migration sequence in each; only the values file differs, so a build promotes with no code change | Arch v5 slides 8 and 38; Template and Rules §R5.5 DP-15 |
| BR2 | One Temporal cluster per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server; the namespace `rwb-recovery` in each, with its own retention, quotas, certificates and codec keys | Arch v5 slides 23 and 24 |
| BR3 | The codec keys are AES-GCM keys of the namespace, held in the Key Vault of that environment, and the codec server of that environment is the only way the UI reads a payload | Arch v5 slides 8 and 24 |
| BR4 | One ACE database per environment, with the 19 schemas `rwb_<name>` and one login per service; the login owns its own schema, has no grant on any other schema, and goes through its own PgBouncer pool with a connection cap and a statement timeout | Arch v5 slide 29 |
| BR5 | No production data in DEV and masked copies in UAT; DEV holds synthetic data only, SIT and UAT hold masked copies, and PROD receives no copy from a lower environment | NFR-045; RWB-ITG-TE004-ITG |
| BR6 | Every secret is held in the key store and never in code, a configuration file or a prompt; a values file carries a reference to a key and never a value | NFR-052 |
| BR7 | `RWB_SCHEMA` is set per service per environment, the migration files are byte-identical across environments, and the Flyway history of a service is held in its own schema in that environment | Template and Rules §R5.5 DP-15; Arch v5 slide 29 |
| BR8 | The 19 services share one ACE AKS cluster and one App Gateway, and each environment is a separate namespace, key store, database and pool set inside them; a service never provisions an environment of its own | Arch v5 slides 8, 23 and 29 |

### 9. State transitions

| Environment state | Meaning | What moves it on |
|---|---|---|
| Defined | The row exists in the environment matrix with its references and its data class | The platform administrator approves the row |
| Provisioned | The cluster, the namespace, the key store, the database, the 19 logins and the pools exist and the environment check passes | The environment check reports green for the environment |
| In service | Builds are deployed and promoted through the environment | The promotion gate admits a build |
| Frozen | No promotion enters the environment while a release window or an incident is open | The platform administrator closes the window or the incident |
| Retired | The environment accepts no deployment and its credentials are revoked | The platform administrator retires it at the end of the programme |

No case status changes in this story: these are states of an environment, not of a case, a treatment or a decision.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the environment matrix, the four values files, the promotion gate and the four checks; installs and promotes through the pipeline only |
| Platform administrator | Approves the environment matrix, the cluster and namespace assignment, the pool caps, the data class of each environment and the promotion; owns the key store of each environment |
| Solution architect | Approves the four environments, the isolation rules, the value set that may differ between environments and the data classes |
| ACE database administrator | Creates the 19 schemas and the 19 logins per environment, sets each PgBouncer pool and its cap, and confirms the grants of each login |
| Security architect | Approves the key store layout, the codec key scope per namespace, the secret scan and the cross-environment refusal tests |
| RW-PLATADM | Runs the environment check, reads the matrix and the promotion records, and may freeze an environment; never changes a values file by hand |
| RW-AUDIT | Reads the environment matrix, the promotion records and the check evidence; writes nothing |
| RW-SECADM | Reads the key store layout, the secret scan results and the cross-environment refusal evidence; writes nothing in the baseline |

The platform stories carry no service short name, schema, topic, event or task queue in the §R4 service table, because that table has 19 service rows and no platform row. The environment baseline therefore names a service's schema and login only through the §R4 short name of that service, and where a value of the baseline itself would need a name — a host, a subscription, a pool size, a refresh cadence, an owner — it is Not specified in the source documents (GAP-1426; ASM-2499).

The role assignment of the table above rests on ASM-2501: no source names an environment owner or a promotion approver, so every right is held by a role and a promotion records the role that approved it.

### 11. Data

**Environment matrix**

| Environment | Purpose | Data class | Temporal | Key store | Database | Enters from |
|---|---|---|---|---|---|---|
| DEV | First landing of every build: unit, component and contract tests of each service | Synthetic data only (NFR-045) | Own cluster, own persistence database, namespace `rwb-recovery`, own codec keys | Own Key Vault, own key set | ACE database, 19 schemas with one login and one PgBouncer pool each | The pipeline, on merge |
| SIT | System and integration tests over the full estate, including the harness runs of record | Masked copies (RWB-ITG-TE004-ITG) | Own cluster, own persistence database, namespace `rwb-recovery`, own codec keys | Own Key Vault, own key set | ACE database, 19 schemas with one login and one PgBouncer pool each | DEV, through the promotion gate |
| UAT | Business acceptance on masked copies, as NFR-045 requires | Masked copies (NFR-045) | Own cluster, own persistence database, namespace `rwb-recovery`, own codec keys | Own Key Vault, own key set | ACE database, 19 schemas with one login and one PgBouncer pool each | SIT, through the promotion gate |
| PROD | Production use | Production data | Own cluster, own persistence database, namespace `rwb-recovery`, own codec keys | Own Key Vault, own key set | ACE database, 19 schemas with one login and one PgBouncer pool each | UAT, through the promotion gate |

**Values that differ between environments**

| Value | Scope | Where it is held | Differs between environments |
|---|---|---|---|
| `RWB_SCHEMA` | Per service, for example `rwb_case` for `rwb-case`; the same schema name in all four environments | The values file of the environment, rendered into the deployment | No (the name is the same; the login credential is not) |
| Database login and its credential reference | One login per service per environment | A key reference to the environment's Key Vault | Yes (the reference, never the secret) |
| PgBouncer pool name, pool size and connection cap | One pool and cap per login | The ACE database configuration and the pool panel of RWB-PLT-N005-OPS | Yes |
| Temporal frontend address | Per environment | The values file of the environment | Yes |
| Temporal namespace and task queue | `rwb-recovery` and `rwb-<short>`, the same in all four environments | The values file of the environment | No |
| Codec key identifier | Per namespace per environment | A key reference to the environment's Key Vault | Yes |
| Kafka bootstrap and topic ACL scope | Per environment; the topic names are identical | The values file of the environment | Yes (the bootstrap only) |
| API and worker replica counts | 2 fixed API copies, worker 0 to many by KEDA | The values file of the environment | Yes |
| Ingress host and route prefix | Per environment, through the shared App Gateway | The values file of the environment | Yes |

**Data classes**

| Class | Where it is allowed | How it is produced | How it is proven |
|---|---|---|---|
| Synthetic | DEV | Generated by the synthetic-data path of the test data stories | Scan for production identifiers and personal-data patterns: none found |
| Masked | SIT and UAT | The masked copy loaded by RWB-ITG-TE004-ITG, with the masking rule version in force | Masking verifier of the load, and a read through the owner's contract |
| Production | PROD only | Production sources | No copy of a production extract exists in DEV, SIT or UAT |

The environment matrix, the values files and the four checks hold references and configuration only. They hold no schema definition, no migration, no business value and no personal data: the schemas and the migrations belong to the services through RWB-PLT-E1044-OPS, and the credentials belong to the key store of each environment through RWB-PLT-NF04-OPS.

The three data classes above and the refresh cadence they leave open rest on ASM-2500: NFR-045 fixes synthetic data in development and masked copies in user acceptance, the masked copy of SIT and UAT is loaded by RWB-ITG-TE004-ITG, and the cadence is a value of the environment matrix and never a production extract in a lower environment.

The exact hosts, subscriptions, region pairing, sizing of each cluster and database, data refresh cadence of DEV, SIT and UAT and the owner role of each environment are Not specified in the source documents (GAP-1426; ASM-2499).

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. It is an environment baseline only.

#### 12.1 REST operations provided

None. The baseline exposes no REST surface of its own; the environment is read through the cluster, the key store, the database and the pipeline, not through an API.

#### 12.2 REST operations consumed

None. The baseline calls no service contract; the environment check uses the platform tooling of the cluster and of the database, not a Workbench API.

#### 12.3 Events published

None. The baseline publishes no business event and no platform event; a promotion is a pipeline record and not a Kafka message.

#### 12.4 Events consumed

None. The baseline subscribes to no topic; the environment's Kafka bootstrap is a value it renders for the services that do.

#### 12.5 Workflows and activities

None. The baseline starts no workflow and defines no activity; it provisions the namespace `rwb-recovery` in which the service workers poll their own queues.

#### 12.6 Schedules

None. No Temporal Schedule is created, moved or paused by this story; the promotion gate is a pipeline stage and not a Schedule.

#### 12.7 Tables owned

None. The baseline owns no table and no schema. The 19 schemas `rwb_<name>` and their logins belong to the ACE database work of RWB-PLT-NF06-DB and the 19 service stories, the migrations to RWB-PLT-E1044-OPS, and the Flyway history of a service sits in that service's own schema.

#### 12.8 Contract fakes

None. The baseline runs against the real cluster, the real key store and the real database of each environment, and needs no fake: a fake environment would prove nothing about isolation, which is the whole point of the story.

#### 12.9 Call-type summary

None: the baseline is configuration and infrastructure; no REST, Kafka, Temporal or File call of its own.

### 13. Solution plan

**Artefacts.** All paths are relative to the environment baseline repository folder, which is the environment part of the platform repository of RWB-PLT-NF01-OPS.

| Path | Artefact | What it holds |
|---|---|---|
| `environments/matrix.yaml` | The environment matrix | One row per environment: cluster and subscription reference, region, namespace, key store, database server, pool set, data class and owner role |
| `environments/dev/values.yaml`, `environments/sit/values.yaml`, `environments/uat/values.yaml`, `environments/prod/values.yaml` | The four values files | The only difference between environments: `RWB_SCHEMA` binding, credential key references, pool names, Temporal frontend, codec key identifiers, Kafka bootstrap, ingress host and replica counts |
| `environments/<env>/secrets.ref.yaml` | The secret reference map | One line per credential: the key name, the key store path and the consumer; no value and no secret |
| `environments/checks/isolation-check` | The isolation check | The positive check per environment and the three refusals across environments: credential, secret and namespace |
| `environments/checks/schema-check` | The schema and migration check | `RWB_SCHEMA` present and equal to the service's schema, the SHA-256 of every migration file equal across the four environments, no literal schema name, Flyway history in the own schema |
| `environments/checks/secret-scan` | The secret scan | A scan of the chart, the four values files and each image layer for a host, a connection string, a password, a token or a key, with the finding naming the file and the key only |
| `environments/checks/data-class` | The data class guard | The synthetic-only proof of DEV, the masked-copy reference of SIT and UAT and the refusal of a production extract targeted at DEV |
| `environments/promotion/gate` | The promotion gate | The order DEV, SIT, UAT, PROD; the same image digest and the same chart version; the four checks green; the approver role; one promotion record per move |

**Pattern application.** None of the DP table applies to this story (`patterns` is empty): it introduces no legacy table, no legacy login, no legacy topic name and no legacy call. The two patterns its rules serve are used by the stories that own them: DP-15 (per-service Flyway sequence in the service's own schema) is applied by RWB-PLT-E1044-OPS, and DP-02 (one login per service) by the ACE database stories. This story only fixes the environments in which both hold.

**Build steps**

1. Write the environment matrix with four rows and references only, and agree the rows with the platform administrator and the solution architect.
2. Write the four values files and the secret reference map, and prove that the same chart version renders four manifest sets whose only difference is the values file.
3. Wire the promotion gate: order, same image digest, same chart version, four checks green, one approver role, one promotion record.
4. Build the isolation check and run it in DEV, SIT, UAT and PROD, including the three refusals across environments.
5. Build the schema and migration check and run it for the first service of wave 1, then for every service as it is created.
6. Build the secret scan and run it on the chart, the four values files and each image.
7. Build the data class guard and prove the DEV refusal of a production extract and the masked-copy reference of SIT and UAT.
8. Promote one build once through DEV, SIT, UAT and PROD with no rebuild, no chart change and no code change, and record the run as the evidence of the baseline.
9. Publish the baseline and hand it to the service OPS stories, which add no environment of their own and take these values files as their starting point.

**Done when.** The four environments exist and install from the same chart version and the same migration sequence with only the values file differing; each environment has its own Temporal cluster with its own persistence database and the namespace `rwb-recovery`, its own codec keys in its own Key Vault, its own key set, its own database logins and its own PgBouncer pools; the three cross-environment refusals are proven once per pair; DEV holds synthetic data only and UAT holds masked copies; `RWB_SCHEMA` is set per service per environment and the migration files are byte-identical in all four; and a chart, a values file or an image carries no host and no credential.

The exact hosts, subscriptions, region pairing, cluster and database sizing, pool caps, replica counts, data refresh cadence, environment owner roles, the approver role of the promotion gate and the key store naming are Not specified in the source documents (GAP-1426; ASM-2499).

### 14. Validation and messages

| ID | When | What is validated | Outcome |
|---|---|---|---|
| V1 | A value file is committed | It carries a reference for every credential and no value; the host, port, pool size and replica count are present | The pipeline stops on a value that is a secret or a missing key, and names the key |
| V2 | An install starts in an environment | The chart version and the image digest are the ones the promotion gate admitted | The install is refused on a different chart version or digest |
| V3 | A deployment renders | `RWB_SCHEMA` equals the service's own schema in that environment, and no schema name appears in code or in a migration | The deployment fails and names the schema and the file |
| V4 | A migration is applied | The SHA-256 of every migration file equals the value recorded for the other three environments | The promotion is blocked and the two environments and the file are named |
| V5 | The environment check runs | The environment's own credential, key and namespace answer; the credential, the secret and the namespace of another environment are refused | The environment is admitted or reported as not isolated, with the pair and the credential named |
| V6 | A data load is targeted at an environment | The data class of the environment admits the load: synthetic in DEV, masked in SIT and UAT, production in PROD only | A production extract targeted at DEV is refused before any file is read |
| V7 | A promotion is requested | The four checks are green for the source environment and the target environment is the next one in the order | The move is refused otherwise, and one promotion record is written per admitted move |

**Messages.** No message ID of the message catalogue applies to this story: the catalogue carries case, task, notice, job and access messages, and none of them describes an environment fault. The baseline therefore adds no user-facing message. Every validation above is a pipeline finding addressed to the owner role of the environment, with the environment, the key or the file and the two environments where a comparison is made; a finding that should become a message waits for the catalogue to give it an ID and is not written as free text. The secret scan never prints a secret value, and the data class refusal names the source and the target environment only.

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. The operator surfaces are the cluster, the key store, the database and the pipeline of each environment, which the DevOps engineer and the platform administrator read through their own consoles and not through the Workbench. The states of section 9 are environment states and not screen states, and the only Workbench view that shows the result is the pool and cluster panel of the observability baseline RWB-PLT-N005-OPS, which is read-only for this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF03-OPS-01 | AC1 | Component | The four values files and one chart version: the rendered manifests differ only in the values file; the migration order is identical in the four environments; one build promotes DEV → SIT → UAT → PROD with the same image digest and no rebuild; a promotion that needs a code change is refused |
| TC-PLT-NF03-OPS-02 | AC2 | Integration | The four deployed environments: the DEV credential against the UAT schema, the DEV key against the UAT Key Vault and the DEV client against the UAT namespace are each refused; each environment's own credential, key and namespace answer; the `rwb-recovery` namespace exists once per environment; a pool reaches its cap and queues or refuses without touching the ACE server |
| TC-PLT-NF03-OPS-03 | AC3 | NFR | A scan of the DEV data against production identifiers and personal-data patterns with no hit; a production extract targeted at DEV refused before any file is read; the masked copy in SIT and UAT verified through the loading story; no production extract file present in DEV, SIT or UAT |
| TC-PLT-NF03-OPS-04 | AC4 | Component | `RWB_SCHEMA` per service per environment; the SHA-256 of every migration file equal in DEV, SIT, UAT and PROD; one migration file changed in one environment fails and names the file and the two environments; a literal schema name in a migration fails; the Flyway history present in the own schema only |
| TC-PLT-NF03-OPS-05 | AC5 | NFR | The secret scan of the chart, the four values files and each image layer with no host, connection string, password, token or key; a committed credential fails the scan and names the file and the key without printing the value; every credential of a running pod resolved from the environment's key store at deploy time (NFR-052) |

### 17. Guardrails

- No business value in code: every host, port, pool size, replica count, refresh setting and threshold is a value of the environment's values file, and a change of environment is a value change, not a code change.
- No secret in code, a chart template, a values file, a log or a prompt: every credential is a reference to the environment's key store, resolved at deploy time (NFR-052), and the secret scan fails the build on a value.
- No personal data in a test, a values file or a check: DEV holds synthetic data only and SIT and UAT hold masked copies (NFR-045), and the checks name an environment, a key and a file and never a record.
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE table and no service table, and its only database interaction is the grant and pool check of a login against its own schema.
- No cross-environment reach: no credential, key, namespace, pool or route of one environment is accepted by another, and the isolation check proves the refusal once per pair.
- One login, one pool and one schema per service per environment: the login owns its own schema, has no grant on another schema, and its pool cap protects the ACE server (Arch v5 slide 29).
- No hand change in an environment: the matrix, the values files and the checks are code in the repository, a hand edit is reported by the next run, and no environment is created by a service team.
- No production data outside PROD and no copy upward: a lower environment never receives a production extract, and PROD receives no data from DEV, SIT or UAT.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NFR-045 | No production data in the development environment, and the user acceptance environment uses masked copies | The data class of each environment: the DEV synthetic-only guard, the masked-copy reference of SIT and UAT and the refusal of a production extract targeted at DEV | TC-PLT-NF03-OPS-03 |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The secret reference map of each environment, the secret scan of the chart, the values files and the images, and the deploy-time resolution from the environment's Key Vault | TC-PLT-NF03-OPS-02, TC-PLT-NF03-OPS-05 |
| Arch v5 slide 23 | One Temporal cluster per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server; a namespace per workbench with its own retention, quotas, certificates and codec keys | The cluster and namespace row of the environment matrix and the isolation check per environment | TC-PLT-NF03-OPS-02 |
| Arch v5 slide 24 | At runtime one cluster per environment, a namespace per workbench, a queue per service, and codec keys in Key Vault per namespace | The `rwb-recovery` namespace and codec key reference per environment, and the refusal of a cross-namespace call | TC-PLT-NF03-OPS-02 |
| Arch v5 slide 29 | One ACE database, one schema and one login per service, one PgBouncer pool and connection cap per login, no cross-schema join or grant | The per-environment login, pool and cap of each of the 19 services, and the schema and migration identity check | TC-PLT-NF03-OPS-02, TC-PLT-NF03-OPS-04 |
| Arch v5 slides 8 and 38 | One shared ACE AKS cluster and App Gateway, and wave 0 builds the template, the chart, the 19 schemas and logins and Temporal once | The environment matrix as the four installs of one chart, and the promotion gate that carries one build through the four | TC-PLT-NF03-OPS-01, TC-PLT-NF03-OPS-05 |

### 19. Out of scope

- The Helm chart itself, its templates and its first version: RWB-PLT-N004-OPS owns the chart, and this story writes only the four values files and the checks around it.
- The secret and configuration baseline, the key store client and the rotation of a credential: RWB-PLT-NF04-OPS owns them; this story only references the keys per environment.
- The repository and pipeline baseline and the golden pipeline: RWB-PLT-NF01-OPS owns them, and this story adds a promotion stage to that pipeline.
- The creation of the 19 schemas, the 19 logins and their grants in each environment: RWB-PLT-NF06-DB and the ACE database stories own the schema and login work; this story checks them, and it owns no DDL.
- The migration files, their versions and the Flyway history: RWB-PLT-E1044-OPS and the per-service DB stories own them; this story only compares their SHA-256 across the four environments.
- The masked copy load and its masking rules: RWB-ITG-TE004-ITG owns the SIT and UAT copy and its verifier; this story only fixes that UAT holds a masked copy and that DEV holds none.
- The synthetic data set of DEV and its verifier: the test data stories of the integration epics own them, per RWB-ITG-W1J01-ITG.
- The edge routes, the WAF policy and the partner gateway in the DMZ: RWB-PLT-N001-CON and RWB-PLT-EDGE own them; this story only carries the ingress host as a value.
- The observability of the four environments, the pool and cluster panels and the alerts: RWB-PLT-N005-OPS owns the baseline, and this story inherits it.
- Production cutover, the dress rehearsal, the go-live window and the BOT approval: the release and cutover material, outside this baseline.
- The exact hosts, subscriptions, region pairing, sizing, pool caps, replica counts, data refresh cadence, environment owner roles and promotion approver: the gap GAP-1426 and its assumptions, for the platform administrator and the solution architect to close before the first promotion is taken as the run of record.
