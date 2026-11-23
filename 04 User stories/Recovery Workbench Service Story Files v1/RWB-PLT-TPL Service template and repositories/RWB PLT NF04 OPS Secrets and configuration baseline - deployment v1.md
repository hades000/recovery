# RWB-PLT-NF04-OPS Secrets and configuration baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF04-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-04 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-TPL-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: platform story for legacy NF-04 (moved, no impact), the secrets and configuration baseline; the legacy NF-04 story text is not in the source set, so the baseline is derived from Arch v5 slides 8, 11, 20, 24, 29 and 35 and from NFR-052, NFR-054 and REQ-DRI-010. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **one versioned secrets and configuration baseline — every secret held as a key-store reference that is resolved at run time, one identity and one secret scope per service, and every non-secret value read from its named source, the parameters contract for thresholds, the reference-data contract for lists, the environment variables and the chart values for non-secret settings — established once and inherited by the 19 services and the platform epics**, so that **no secret and no business value ever reaches a repository, an image, a chart value, a pipeline log, a test or a prompt, no service can read another service's secret, and a secret is rotated without a rebuild and without a code release**.

The legacy story text for NF-04 is not in the source set: the NF-04 row of the legacy index holds the title "Secrets and configuration baseline" and no sections, no acceptance criteria, no test cases and no requirements (`_work/msr/plan/legacy_index.json`, NF-04 entry, all fields empty). The baseline in this story is therefore derived from the architecture slides and from NFR-052, NFR-054 and REQ-DRI-010, which section 2 and section 18 name, and it is not copied from a legacy narrative. The legacy title is kept word for word as the story title.

### 2. Business rationale

Arch v5 slide 8 puts a Key Vault and a codec server for payload keys in the shared part of the C4 diagram, next to the gateway-bff with its Redis session and JWT. Slide 20 gives every service the same block from the service template: its own schema for business tables and the outbox and inbox, its own task queue, and the platform `/health` and `/metrics` endpoints, so a service's credentials and settings are per service and per environment and not shared text. Slide 24 makes the payload encryption concrete: every Temporal client and worker uses the AES-GCM codec, the keys are in Key Vault, and the keys are per namespace, with a codec server for authorised staff. Slide 29 states the data rule that makes a per-service scope necessary: each service has one login that owns its schema and has no grant on any other schema, and a service that asks for another service's schema is refused. Slide 35 states the same rule at the security layer: nobody is trusted by default, every call is mutually authenticated with a workload identity and authorised by policy, deny by default, and personal data stays in the owning service and never travels in an event or a workflow payload. Slide 11 adds the identity of each call type: the user JWT from the BFF plus the workload identity on REST, OAUTHBEARER or mTLS with per-topic ACLs on Kafka, and the namespace certificate with a worker identity per service on Temporal.

NFR-052 (status Proposed, owner Solution architect) requires that secrets are held in the key store and never in code, configuration files or prompts, with the target "No secrets in code or prompts". NFR-054 requires that the build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency, with the target "Pipeline checks pass". REQ-DRI-010 (Must, Center of excellence) requires a parameter catalog and a configuration service that hold every threshold, limit and name, versioned, changed without a code release. DP-06 and DP-07 of the template give those two capabilities their contracts: the parameters contract `RWB-PLT-E1042-CON` and the reference-data contract `RWB-PLT-E1043-CON`, both platform contracts of the shared-library epic, with the rwb-case service contracts behind them.

Without this baseline the rule is a sentence in a document and nothing more. There are 19 services, 4 environments and one shared ACE cluster. Each service has a database login, a namespace certificate, a Kafka principal, a codec key and at least one outbound credential, which is five credential families per service and per environment, and each service also holds thresholds and list values that today sit in code or in a configuration file. A developer who is short of time copies a connection string into a chart value, a test fixture keeps a real password so the test passes, a pipeline echoes its environment into the log, and a prompt carries a token for a model endpoint. None of those events fails a build unless something checks. This story is that something: one key-store convention, one reference-not-value rule, one scope per service, one pipeline gate and one rotation path, established in wave 0 before the first service is built from the template.

The baseline is a Day-1 platform enabler with no build dependency. Every service and platform story from wave 0 onwards consumes it, and none of them may establish its own convention. NF-04 carries no legacy build impact, which is why it is Moved (no impact): no built code changes, and the convention is set before the first new service exists.

### 3. Preconditions

- The repository and pipeline baseline of RWB-PLT-NF01-OPS exists: one repository per service, one pipeline, the pipeline stages and the check step that a gate can join.
- The service pipeline template and the Helm chart of RWB-PLT-N004-OPS exist, including the values file per environment and the deployment descriptor, because this story fixes what those files may and may not hold.
- The environment baseline of RWB-PLT-NF03-OPS exists: DEV, SIT, UAT and production, the per-environment platform resources and the per-environment access path, because a secret and a configuration value are per environment.
- The parameters contract `RWB-PLT-E1042-CON` and the reference-data contract `RWB-PLT-E1043-CON` are published by the shared-library epic, with the client library, so that a threshold and a list have a named source that is not code (DP-06, DP-07).
- The workload identity, the service mesh mTLS and the per-service Kafka principal of Arch v5 slides 11 and 35 are provided by the platform, because the refusal of a cross-service read rests on an identity that is per service and not shared.
- The message catalogue exists, so that the one runtime alert this baseline raises carries an existing message ID and invents none.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The key-store naming, the rotation interval, the overlap window, the secret owners, the configuration key names and the pipeline scanner products are Not specified in the source documents (GAP-1427; ASM-2502).

### 4. Flow

1. Publish the baseline as code in the platform repository: the secret-reference convention, the per-service scope table, the configuration source map, the pipeline gate rules and the rotation job definition, one versioned commit per change, never edited in a workspace.
2. Fix the secret-reference convention: every secret is a reference of the form `<key store>/<object>/<version>` that is resolved at run time by the platform library; a code path, a chart value, a pipeline variable, a test fixture or a prompt holds the reference and never the value (NFR-052).
3. Fix the per-service identity and scope table: one row per service of the 19-service list, each with its own identity, its own key-store object path and its own set of readable references; a key-store policy grants that identity read on its own path only, and a request for another service's path is denied by the key store and not only by application code (Arch v5 slides 29 and 35).
4. Fix the configuration source map: secrets from the key store; thresholds, limits and names from the parameters contract `RWB-PLT-E1042-CON` (DP-06); versioned lists from the reference-data contract `RWB-PLT-E1043-CON` (DP-07); non-secret environment settings, such as an endpoint host, a port, a timeout, a profile name and a log level, from the environment variables and the chart values of the environment; and no business value in code.
5. Fix the codec keys: one key per Temporal namespace, held in the key store, used by every client and worker of that namespace, with the codec server using the same key for the authorised read in the Temporal UI (Arch v5 slide 24).
6. Wire the pipeline gate of NFR-054: a pre-commit and pipeline secret scan over the change, an image and image-history scan of the built artefact, a dependency check against the approved list, a personal-data pattern check over code, tests and logs, and a check that no chart value, pipeline variable or test fixture carries a literal credential; a finding blocks the change and names the file, the line and the rule.
7. Wire the rotation path: the rotation job writes a new version of the key-store object on the interval held as a configuration value; the service re-reads the current version at run time with no rebuild and no restart of the build; the previous version stays readable only for the overlap window of the configuration value and is then disabled, after which a call made with the old credential is refused (NFR-052).
8. Prove the baseline in DEV and then in SIT: a clone of the template repository with a planted secret, a planted personal-data field and an unapproved dependency is blocked by the gate; a service identity asks for another service's reference and is denied; a rotation is performed in the key store and the service reads the new version with no rebuild; then hand the baseline to the service OPS stories, which add only their own references and their own configuration keys.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A change carries a literal secret, a token or a private key | The gate blocks the change before merge, names the file, the line and the rule, and the change is not built; the value is not repeated in the gate output | None (release error with an exit code and a job log line) | AC1, AC4 |
| X2 | A built image or its history carries a secret or a personal-data pattern | The image scan fails the build after the image is built, the image is not published to the registry that the environments pull from, and the finding names the layer | None (release error with an exit code and a job log line) | AC4 |
| X3 | A service asks for another service's secret | The key-store policy denies the read for the asking identity, the call returns a forbidden answer, the attempt is logged with the asking identity and the requested path, and the service start-up or the guarded call fails closed | None (the key store returns a forbidden answer and the attempt is logged) | AC2 |
| X4 | A secret is rotated while services run | The new version is written to the key store; each service reads the current version at run time with no rebuild; the old version stays usable only for the overlap window and is then disabled, after which a call with the old credential is refused | None | AC5 |
| X5 | A threshold, a limit or a list value is hard-coded, or a configuration key is read from an unnamed source | The gate fails the change and names the key and the contract it must come from; a value with no contract is reported as a gap rather than invented in code | None (release error with an exit code and a job log line) | AC3 |
| X6 | A personal-data field reaches code, a test, a log or a prompt | The personal-data pattern check fails the change; where the field already sits in a log, the pipeline stage that produces it fails and the log is not published | None (release error with an exit code and a job log line) | AC4 |
| X7 | The key store does not answer at run time | The service fails closed, its readiness probe fails and it does not serve a call with a stale or cached credential; the alert goes to the platform owner role through the observability baseline | MSG-P2-004 | AC1, AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list, the platform resources, the two contracts and the message catalogue only; the service stories consume the convention and do not change it |
| Negotiable | The key-store naming, the rotation interval, the overlap window, the configuration key names, the scanner products and the secret owners are agreed with the platform administrator and the solution architect; the reference-not-value rule, the per-service scope, the source map and the two named contracts are fixed by NFR-052, NFR-054, REQ-DRI-010 and DP-06 and DP-07 |
| Valuable | Gives every service and platform story from wave 0 onwards one convention for its credentials and one source for each configuration value on Day 1, and makes NFR-052 and NFR-054 enforceable instead of advisory |
| Estimable | One baseline repository with five rule groups, one per-service scope table for 19 rows and 4 environments, one pipeline gate configuration and one rotation job; five acceptance criteria |
| Small | Fits one sprint with the convention, the scope table, the source map, the gate and the rotation proof; the actual credential values, the per-service references and the per-service configuration keys stay with the service OPS stories |
| Testable | Every criterion is tested against a planted secret, a planted personal-data field and an unapproved dependency in a clone of the template, against a denial in the key store, and against a rotation performed in DEV and SIT with no rebuild |

### 7. Acceptance criteria

```gherkin
Feature: Secrets and configuration baseline inherited by the 19 services and the platform epics

  Background:
    Given the repository and pipeline baseline of RWB-PLT-NF01-OPS and the pipeline template and chart of RWB-PLT-N004-OPS
    Given the environment baseline of RWB-PLT-NF03-OPS with DEV, SIT, UAT and production
    Given the parameters contract RWB-PLT-E1042-CON, the reference-data contract RWB-PLT-E1043-CON and the message catalogue

  Scenario: AC1 Every secret is a key-store reference resolved at run time, and no secret appears in git, an image, a Helm value, a pipeline log, a test or a prompt (new, D-RCV-60)
    Given the secret-reference convention of the baseline
    When a service of the 19-service list reads its database login, its key-store codec key and its outbound credential
    Then each value is resolved at run time from the key store through its reference
    And the repository history, the built image and its history, the Helm values, the pipeline log, the test fixtures and the prompts carry the reference and never the value
    When a literal secret is planted in a chart value, a test fixture and a prompt
    Then the gate blocks each of the three changes and names the file, the line and the rule
    And the gate output does not repeat the value it found

  Scenario: AC2 Each service has its own identity and its own secret scope, and a service is refused when it asks for another service's secret (new, D-RCV-60)
    Given one identity per service of the 19-service list and one key-store object path per service
    When a service reads its own secret
    Then the read is allowed by the key-store policy for that identity
    When a service asks for another service's secret
    Then the key store denies the read and no value is returned
    And the attempt is logged with the asking identity and the requested path
    And the refusal holds even when the request comes from inside the cluster over mTLS
    When two services share one identity or one key-store object path
    Then the baseline check fails and names both services

  Scenario: AC3 The configuration baseline names its sources and no business value is in code (new, D-RCV-60)
    Given the configuration source map of the baseline
    When a service reads a threshold, a limit or a name
    Then the value comes from the parameters contract RWB-PLT-E1042-CON and not from code (DP-06)
    When a service reads a versioned list
    Then the value comes from the reference-data contract RWB-PLT-E1043-CON and not from code (DP-07)
    When a service reads a non-secret environment setting such as an endpoint, a port, a timeout or a log level
    Then the value comes from the environment variables and the chart values of that environment
    And no secret is read from an environment variable, a chart value or a configuration file
    When a threshold, a limit or a list value is written into code
    Then the gate fails the change and names the key and the contract it must come from

  Scenario: AC4 The pipeline blocks a change carrying a secret or personal data and scans the image and its history (new, D-RCV-60)
    Given the pipeline gate of NFR-054 wired into the pipeline of RWB-PLT-NF01-OPS
    When a change carries a secret
    Then the change is blocked before merge and the finding names the file, the line and the rule
    When a change carries a personal-data field in code, a test or a log
    Then the change is blocked with the same detail
    When a change adds a dependency that is not on the approved list
    Then the change is blocked and the dependency is named
    When an image is built
    Then the image and its history are scanned and a finding stops the publication of that image
    When a change is clean
    Then the gate passes and records the rule set and its version in the build record

  Scenario: AC5 A secret is rotated in the key store without a rebuild, the service reads the current version, and the old credential is refused after the overlap (new, D-RCV-60)
    Given a running service that reads its secret by reference
    When a new version of the secret is written to the key store
    Then the service reads the current version at run time with no rebuild, no new image and no chart change
    And the previous version stays readable only for the overlap window held as a configuration value
    When the overlap window ends and the previous version is disabled
    Then a call made with the old credential is refused
    And the service continues to serve calls with the current version
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every secret is held in the key store and never in code, a configuration file or a prompt; code, charts, pipelines, tests and prompts hold the reference only | NFR-052; Arch v5 slides 8 and 20 |
| BR2 | One identity and one secret scope per service: a service reads its own key-store path only, and a read of another service's path is denied by the key store | Arch v5 slides 29 and 35; NFR-051; DP-02 |
| BR3 | The key store is the Key Vault of the shared platform, and the Temporal payload codec keys are per namespace, held in the same key store | Arch v5 slides 8, 20 and 24 |
| BR4 | Thresholds, limits and names come from the parameter catalog through the parameters contract, versioned and changed without a code release; lists come from the reference-data contract | REQ-DRI-010; DP-06; DP-07 |
| BR5 | Non-secret environment settings come from the environment variables and the chart values of that environment, which are versioned with the chart and hold no secret | Arch v5 slide 20; RWB-PLT-N004-OPS |
| BR6 | The pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency, and scans the image and its history | NFR-054 |
| BR7 | A rotation writes a new key-store version and needs no rebuild; the previous version is usable only for the overlap window and is then disabled, after which the old credential is refused | NFR-052; this story |
| BR8 | Personal data stays in the owning service, masked, and never travels in an event, a workflow payload or a log; the codec protects the payload and does not license the copy | Arch v5 slide 35; Template and Rules §R7.2 s17 |
| BR9 | Every call between services is mutually authenticated with the workload identity of the calling service, and authorisation is deny by default | Arch v5 slides 11 and 35 |

### 9. State transitions

None. This story changes no business state and no case status. A secret version moves through the key-store lifecycle (current, previous, disabled), and that is the lifecycle of a credential held by the platform, not a state of a case; a service that cannot resolve its secret fails closed and is restarted by the platform, which is a deployment state and not a business state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the baseline repository, the gate configuration and the rotation job; changes the convention, the source map and the gate rules through the repository only |
| Platform administrator | Owns the key store, the key-store policies, the per-service object paths, the rotation intervals and the overlap windows; performs and approves a rotation; is the only role that may read a secret value in a break-glass case |
| Solution architect | Approves the reference-not-value rule, the source map, the two named contracts and the configuration key naming; owns NFR-052 and NFR-054 |
| Security architect | Approves the personal-data patterns of the gate, the scanner rule set and the approved-dependency list |
| Service team | Reads the convention and its own scope row; adds its own references and its own configuration keys in its own service story, and never edits the baseline |
| RW-PLATADM | Reads the key-store policy list, the scope table and the rotation history for operations and break-glass support; holds no write right on the baseline |
| RW-SECADM | Reads the gate rule set, the findings and the approved-dependency list; writes nothing in the baseline |
| RW-AUDIT | Reads the rotation history and the gate findings of a release; writes nothing |

The platform stories carry no service short name, schema, topic or task queue in the §R4 service table, because that table has 19 service rows and no platform row. Where a service identity or a key-store path would be named for this story, it is Not specified in the source documents (GAP-1427; ASM-2502); the baseline itself runs under the platform identity in the `rwb-recovery` namespace.

### 11. Data

**Value classes and their source**

| Value class | Examples | Source of the value | Where the value is held |
|---|---|---|---|
| Secret | A database login and its password, a key-store codec key, an outbound partner credential, a client secret for a token endpoint | The key store (Key Vault) | Key Vault, per environment and per service; the consumer holds the reference |
| Temporal payload codec key | The AES-GCM key of a namespace | The key store, one key per namespace (Arch v5 slide 24) | Key Vault; used by every client and worker of that namespace and by the codec server |
| Threshold, limit and name | A cap, a limit, a window, a name of a rule or a message | The parameters contract `RWB-PLT-E1042-CON` (DP-06, REQ-DRI-010) | The parameter catalog of rwb-case, read through the contract; never in code |
| Versioned list | A product list, a status list, a reason list, a valid-from and valid-to table | The reference-data contract `RWB-PLT-E1043-CON` (DP-07, REQ-DRI-011) | The reference-data service of rwb-case, read through the contract; never in code |
| Non-secret environment setting | An endpoint host, a port, a timeout, a profile name, a log level, a feature switch that is not a secret | The environment variables and the chart values of that environment | The chart of the environment (RWB-PLT-N004-OPS), versioned with the chart |
| Secret inventory metadata | The owner role, the rotation interval, the overlap window, the last rotation and the consuming services | The baseline repository and the key-store metadata | The baseline repository, as values, with no secret value in it |

**Secret families per service**

| Family | Provided by | Scope | Source |
|---|---|---|---|
| Database login | The ACE DB story of the service (DP-02, DP-15) | One login per service, one schema, no grant on another schema | Arch v5 slide 29 |
| Temporal payload codec key | The workflow platform (RWB-PLT-WF) | One key per namespace; every client and worker of the namespace uses it | Arch v5 slide 24 |
| Kafka principal and its credential | The Kafka event platform (RWB-PLT-EVT) | Per-service principal with per-topic ACLs | Arch v5 slides 11 and 35 |
| Workload identity and namespace certificate | The platform and the service mesh | Per service, per namespace, mutually authenticated | Arch v5 slides 11, 24 and 35 |
| Outbound credentials | The integration stories of the calling service | Per target system, per environment | Arch v5 slide 11 |

The migration account secret is owned by RWB-PLT-E1044-OPS and is not repeated here; the environment, network and access path are owned by RWB-PLT-NF03-OPS and are not repeated here. This story fixes the rule that both of them follow: a reference in the consumer, a value in the key store, and one scope per service.

**Naming and values not in the source set**

| Value | Status |
|---|---|
| Key-store name and the object path convention per service | Not specified in the source documents (GAP-1427; ASM-2503) |
| Rotation interval per secret family | Not specified in the source documents (GAP-1427; ASM-2504) |
| Overlap window before the previous version is disabled | Not specified in the source documents (GAP-1427; ASM-2504) |
| Secret owner role per family, beyond the platform administrator of the key store | Not specified in the source documents (GAP-1427; ASM-2503) |
| Configuration key names of the non-secret environment settings | Not specified in the source documents (GAP-1427; ASM-2505) |
| Scanner products and the approved-dependency list | Not specified in the source documents (GAP-1427; ASM-2506) |

The baseline holds references, metadata and rule definitions only. It holds no secret value, no personal data and no business value: a business value belongs to the parameter catalog or the reference data, and a personal value belongs to the owning service, masked (Arch v5 slide 35; Template and Rules §R7.2 s17).

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. It is a platform baseline and a pipeline gate.

#### 12.1 REST operations provided

None. The baseline exposes no REST surface of its own; the platform administrator reads and changes it through the repository and the key store, and the consumer of a secret reads it from the key store and not from this baseline.

#### 12.2 REST operations consumed

None as a REST path. Two contract dependencies are consumed, and they are consumed as contracts and not as REST paths of this story, because the baseline names the source of a value and the service that reads the value is the caller:

| Contract dependency | Owner | What the baseline fixes about it |
|---|---|---|
| `RWB-PLT-E1042-CON` | Platform, epic RWB-PLT-LIB (shared libraries); the service contract behind it is `RWB-P3-E1042-CON` of rwb-case | That a threshold, a limit and a name are read from the parameters contract through the client library and never from code (DP-06, REQ-DRI-010) |
| `RWB-PLT-E1043-CON` | Platform, epic RWB-PLT-LIB (shared libraries); the service contract behind it is `RWB-P3-E1043-CON` of rwb-case | That a versioned list is read from the reference-data contract and never from code (DP-07, REQ-DRI-011) |

The path, the version and the payload of neither contract are repeated here; they belong to the contract stories that publish them.

#### 12.3 Events published

None. The baseline publishes no business event; a gate finding is a build result and a rotation is recorded in the key-store metadata, and neither is a Kafka event.

#### 12.4 Events consumed

None. The baseline subscribes to no business event.

#### 12.5 Workflows and activities

None. The rotation is a scheduled pipeline job and not a Temporal workflow; the workflow platform consumes the codec key that this baseline places, and the workflows themselves belong to the service stories.

#### 12.6 Schedules

None. The rotation runs on the pipeline schedule of the platform repository; no Temporal Schedule is created by this story.

#### 12.7 Tables owned

None. The baseline owns no table and no schema; it lives as code and metadata in the platform repository, the secret values live in the key store, and the threshold and list values live in the parameter catalog and the reference data of rwb-case.

#### 12.8 Contract fakes

None. This story calls neither contract at run time, so it needs no fake; the service stories that read a threshold or a list build against the fakes of `RWB-PLT-E1042-CON` and `RWB-PLT-E1043-CON`, which those contract stories provide.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | The baseline provides no REST operation and calls none |
| Kafka | None | The baseline publishes no event and consumes none |
| Temporal | None | The baseline runs no workflow, no activity and no Schedule; it places the codec key that the workflow platform uses |
| File | None | No file is read or written by the baseline at run time; the baseline itself is versioned files in the platform repository |

None: the baseline is configuration; no REST, Kafka, Temporal or File call of its own. The two contract dependencies of 12.2 are named as the source of a value and are read by the service that needs the value, in its own story.

### 13. Solution plan

**Artefacts.** All paths are relative to the platform repository of RWB-PLT-NF01-OPS.

| Path | Artefact | What it holds |
|---|---|---|
| `platform/secrets/convention.md` | The reference-not-value convention | The reference form, the rule for each artefact type (code, chart, pipeline, test, prompt) and the one worked example with a synthetic value |
| `platform/secrets/scope-table.yaml` | The per-service scope table | One row per service of the 19-service list: identity, key-store object path, readable references, owner role; validated against the 19-service list |
| `platform/secrets/key-store-policy.yaml` | The key-store policy as code | The read grant of each identity on its own path, the deny default, and the absence of a cross-service grant |
| `platform/config/source-map.yaml` | The configuration source map | The key, its source (key store, parameters contract, reference-data contract, environment variable or chart value) and the contract or rule it comes from |
| `platform/pipeline/gate/` | The pipeline gate | The secret scan, the personal-data pattern check, the approved-dependency check, the image and image-history scan, the rule set and its version, and the artefact types it refuses |
| `platform/rotation/rotation-job.yaml` | The rotation job | The interval and the overlap window as values, the key-store object families it rotates, and the record it writes |
| `platform/secrets/README` | The operating note | The rotation steps, the break-glass read, the owner role per family and the escalation path |

**Pattern application.** The metadata `Patterns applied` row stays None: this story carries no legacy table, no legacy login, no legacy topic name and no legacy call, so no DP row is applied to code here. The two contracts it names in 12.2 are exactly the contracts that DP-06 (parameters, from legacy parameter tables and `casewf.config`) and DP-07 (reference data and lists) attach to every service story, and DP-02 (one login per service) is the reason one scope per service is possible at all.

**Build steps**

1. Write the reference-not-value convention and the source map, and give each artefact type its rule: code, chart values, pipeline variables, test fixtures and prompts.
2. Build the per-service scope table for the 19-service list and the key-store policy as code, with deny by default and no cross-service grant.
3. Wire the gate into the pipeline of RWB-PLT-NF01-OPS: secret scan, personal-data pattern check, approved-dependency check, and the image and image-history scan; a finding blocks the change and stops the image publication. The split between the gate rules of this story and the stages of that pipeline is the assumption ASM-2506.
4. Wire the rotation job with the interval and the overlap window as values, and the reading path: the consumer resolves the current version at run time.
5. Prove the gate in a clone of the template repository with a planted secret in a chart value, in a test fixture and in a prompt, a planted personal-data field in code, a test and a log, and an unapproved dependency.
6. Prove the scope: a service identity asks for another service's reference and is denied; two services sharing one identity fail the baseline check.
7. Prove the source map: a hard-coded threshold, a hard-coded list value and a key read from an unnamed source each fail the change.
8. Prove the rotation in DEV and then in SIT: write a new version, read it with no rebuild, end the overlap window, and show that the old credential is refused.
9. Publish the baseline and the operating note, and hand the scope row and the source map to each service OPS story.

**Done when.** The gate blocks a planted secret in a chart value, a test fixture and a prompt, a planted personal-data field in code, a test and a log, and an unapproved dependency, and names the file, the line and the rule without repeating the value; an image with a finding is not published; a service identity is denied on another service's reference and two services sharing an identity fail the check; a hard-coded threshold, a hard-coded list value and a key from an unnamed source each fail the change; and a rotation in SIT is read by the running service with no rebuild, with the old credential refused after the overlap window.

The key-store name and the object path convention, the rotation interval and the overlap window per secret family, the secret owner role per family beyond the platform administrator, the configuration key names, the scanner products and the approved-dependency list are Not specified in the source documents (GAP-1427; ASM-2503). The rotation values are also ASM-2504, the configuration key names are ASM-2505, and the scanner products and the approved-dependency list are ASM-2506.

### 14. Validation and messages

| Message ID | When | Message |
|---|---|---|
| MSG-P2-004 | The rotation job, the key-store re-read or the secret-scope check fails or runs past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P4-002 | A role without the platform administrator right asks for a secret value or a scope change | You cannot {action} here. Your role does not include it. |

The baseline invents no message ID. The two IDs above already exist in the message catalogue: MSG-P2-004 for a scheduled job or step that failed or runs past its threshold, and MSG-P4-002 for an action the role does not include. Their wording is quoted from the catalogue and is not rewritten here. A gate finding is not a catalogue message and not a screen message: it is a release error with an exit code and a job log line naming the file, the line, the rule and the rule-set version, and it is never shown to a case user and never repeats the value it found. An attempt to read another service's secret is refused by the key store and logged with the asking identity and the requested path; it is a security event of the platform and it carries no message text to the caller beyond the forbidden answer.

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. The surfaces it uses are the pipeline report, the key-store metadata and the gate findings of a release, which are read-only for an operator and are changed only through the platform repository and the key store. The secret version lifecycle of section 9 is a lifecycle of a credential and not a screen state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF04-OPS-01 | AC1 | Component | A clone of the template repository with a synthetic literal secret planted in a chart value, in a test fixture and in a prompt; the gate blocks each of the three and names the file, the line and the rule; a clean change passes and records the rule-set version; the gate output, the repository, the image, the image history, the chart values, the pipeline log, the test fixtures and the prompts carry no secret value |
| TC-PLT-NF04-OPS-02 | AC2 | Integration | The 19-row scope table and the key-store policy: each identity reads its own reference; a service identity asks for another service's reference over mTLS inside the cluster and is denied with an answer that carries no value; the attempt is logged with the asking identity and the requested path; two services sharing one identity or one object path fail the baseline check |
| TC-PLT-NF04-OPS-03 | AC3 | Component | The source map: a threshold, a limit and a name resolve through `RWB-PLT-E1042-CON`; a versioned list resolves through `RWB-PLT-E1043-CON`; a non-secret setting resolves from the environment variables and the chart values; a hard-coded threshold, a hard-coded list value and a key read from an unnamed source each fail the change and name the key and its contract |
| TC-PLT-NF04-OPS-04 | AC4 | NFR | The gate of NFR-054: a secret in a change, a personal-data field in code, in a test and in a log, and an unapproved dependency each block the change before merge; an image with a finding in its history is not published; a clean change passes and the build record carries the rule set and its version |
| TC-PLT-NF04-OPS-05 | AC5 | Integration | A rotation in DEV and SIT: a new key-store version is written, the running service reads it at run time with no rebuild, no new image and no chart change; the previous version is readable only for the overlap window; after the window, a call with the old credential is refused and the service still serves calls with the current version |

### 17. Guardrails

- No secret in code, a configuration file, a chart value, a pipeline variable, a test fixture or a prompt: the artefact holds the reference and the value comes from the key store at run time (NFR-052).
- No business value in code: a threshold, a limit and a name come from the parameters contract, and a list comes from the reference-data contract (REQ-DRI-010, DP-06, DP-07).
- No personal data in code, tests, logs, events, workflow payloads or prompts: the pattern check fails the change, and personal data stays in the owning service, masked (Arch v5 slide 35; Template and Rules §R7.2 s17).
- One identity and one secret scope per service: a cross-service read is denied by the key store and not only by application code, and the deny is the default (Arch v5 slides 29 and 35).
- No unapproved dependency: a package that is not on the approved list blocks the change (NFR-054).
- No secret value in a gate finding, a log line, a test report or a run book: the finding names the file, the line and the rule, and never the value.
- ACE data only through the owner's contract or the `v_ace_*` views: the baseline reads no ACE data at all, and the migration account secret of RWB-PLT-E1044-OPS follows the same reference rule from its own story.
- Every test value is synthetic: the planted secret and the planted personal-data field of the tests are generated for the test and are not a copy of any real credential or any real personal record.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The reference-not-value convention, the key-store policy, the per-service scope table and the rotation job | TC-PLT-NF04-OPS-01, TC-PLT-NF04-OPS-02, TC-PLT-NF04-OPS-05 |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data or an unapproved dependency | The pipeline gate: the secret scan, the personal-data pattern check, the approved-dependency check and the image and image-history scan | TC-PLT-NF04-OPS-01, TC-PLT-NF04-OPS-04 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The configuration source map and the two named contracts, `RWB-PLT-E1042-CON` and `RWB-PLT-E1043-CON` | TC-PLT-NF04-OPS-03 |
| Arch v5 slides 24, 29 and 35 | Codec keys per namespace in Key Vault; one login and one scope per service with the cross-service read refused; zero trust with a workload identity and deny by default | The codec key rule of the source map, the scope table, the key-store policy and the identity used by the denial test | TC-PLT-NF04-OPS-02, TC-PLT-NF04-OPS-05 |

### 19. Out of scope

- The actual credential values and the per-service references: each service OPS story adds its own references, its own key-store object paths and its own configuration keys on top of this baseline.
- The database logins and their schemas: RWB-PLT-NF06-DB and the per-service DB stories own them, and this story only fixes the reference and the scope rule they follow.
- The migration account and its secret: RWB-PLT-E1044-OPS owns it.
- The environments, the network path and the access to the platform resources: RWB-PLT-NF03-OPS owns them.
- The repository layout, the pipeline stages and the build record: RWB-PLT-NF01-OPS owns them, and the chart and its values files: RWB-PLT-N004-OPS owns them; this story adds the gate and the rules those files must respect.
- The parameter catalog and the reference-data service themselves, their contract documents, their paths and their versions: `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON` own them.
- The workload identity, the service mesh mTLS and the per-topic Kafka ACLs: the platform and the Kafka event platform own them, and this story consumes the identity to prove the scope.
- The key-store infrastructure, its high availability and its backup: the platform infrastructure stories own them.
- The exact key-store naming, the rotation interval, the overlap window, the secret owners, the configuration key names, the scanner products and the approved-dependency list: the gap GAP-1427, for the solution architect and the platform administrator to close before the baseline is Published.
