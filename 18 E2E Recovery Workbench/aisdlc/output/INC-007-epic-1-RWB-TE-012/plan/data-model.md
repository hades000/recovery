---
title: "Data model: RWB-TE-012"
run_id: "INC-007-epic-1-RWB-TE-012"
revision: "v1 (18 Nov 2026): first data model, against spec v10 and plan v1"
---

# Data model: RWB-TE-012

## 0. Database: no change

No table, column, view, index, grant or migration is added or changed. Evidence: `[S]` §13 "Database: No table or column"; SPEC-016 "No baseline class remains … no data migration is needed"; SPEC-018 "no database" for unit tests; the plan's file list contains no `V<seq>__*.sql` and D-RUN-07 is not exercised. `storage_ref` already exists in Physical Schema v6 (`document.storage_ref varchar(400)`, DF-DOC-006); this story only defines the value format and the `BlobRef` reader. The document row, `document_index`, `write_once` and `doc_version` belong to RWB-E1-024 (SPEC-019).

The "data" of this story is configuration and in-memory state: the template model, the container names, the blob name and reference format, the published records, the properties, the readiness state, the audit event and the health details. Nothing is persisted by this story.

## 1. Template model

`infra/azure/document-storage/azuredeploy.json` is the single deployment unit. It has three groups of parameters.

### 1.1 Required inputs (no `defaultValue`; the schema list and the check enforce them)

| Name | Type | Shape (plan pattern) | Owner | Needed by | Source |
|---|---|---|---|---|---|
| `storageAccountName` | string | `^[a-z0-9]{3,24}$` | Platform team | Before the first DEV apply | `[AZ-GET]` `accountName`; environment fact (open item) |
| `location` | string | `^[a-z0-9]+$` | Compliance with security | Before the first DEV apply | DGAP-13 (open item) |
| `skuName` | string | `^[A-Za-z0-9_]+$` | DL27 owner (solution architect with Compliance) | Before the first DEV apply | DGAP-07 (open item) |
| `accessTier` | string | One of `Hot`, `Cool`, `Cold`, `Archive` (schema regex alternation) | Platform team with Compliance | Before the first DEV apply | DGAP-05 (open item) |
| `privateEndpointSubnetId` | string | ARM subnet resource ID: `^/subscriptions/[0-9a-fA-F-]{36}/resourceGroups/[A-Za-z0-9._() -]{1,90}/providers/Microsoft.Network/virtualNetworks/[A-Za-z0-9._-]+/subnets/[A-Za-z0-9._-]+$` | Platform team | Before that environment's apply | `[S]` §3, §4 step 1; `[ENV]` §3; environment fact (open item) |
| `aceServicePrincipalId` | string | UUID `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` | Platform team with security | Before that environment's apply | `[S]` §4 step 2, AC5; object ID, not a secret |
| `ocrPrincipalId` | string | UUID (same pattern) | Platform team with security | Before that environment's apply | `[S]` §4 step 2, AC5; `[URP]` |
| `deployLegalPolicy` | boolean | `type` boolean, no pattern | Platform team with the release owner | First PROD apply | SPEC-004; ASM-TE012-33 |

The schema file is `{ "requiredInputs": [ { "name", "type", "pattern", "owner", "neededBy" }, … ] }`, read with Jackson 3. The plan-chosen patterns for `location`, `skuName`, `accessTier` and the subnet are permissive because no document gives a pattern (PA-06, PA-08); only the account and container shapes are cited (`[AZ-GET]`).

### 1.2 Parameters with defaults (not in the schema list; an environment file may set them)

| Name | Default | Rule | Source |
|---|---|---|---|
| `intakeContainerName` | `rwb-intake` | 3–63, `^[a-z0-9]+(-[a-z0-9]+)*$` | `[S]` §4 step 1, §13 |
| `standardContainerName` | `rwb-docs` | same | `[S]` §4 step 1; FSD P5 |
| `legalContainerName` | `rwb-docs-legal` | same; carries the policy and is the `<legal>` the check reads | `[S]` §4 step 1; D-RCV-31 |
| `quarantineContainerName` | `rwb-quarantine` | same | `[S]` §4 step 1; E1-041 |
| `legalRetentionDays` | `3650` | positive integer | ASM-TE012-01; DL26 open |
| `softDeleteDays` | `30` | positive integer | ASM-TE012-02; DL27 open |

### 1.3 Resources (what the conformance test reads)

| Resource | Key properties | Source |
|---|---|---|
| `Microsoft.Storage/storageAccounts` | `allowSharedKeyAccess: false`, `publicNetworkAccess: Disabled`, `minimumTlsVersion: TLS1_2`, `supportsHttpsTrafficOnly: true`, `allowBlobPublicAccess: false`, `kind: StorageV2`, SKU and tier from parameters | SPEC-001 |
| `Microsoft.Network/privateEndpoints` | `subnet.id` = `privateEndpointSubnetId`; one connection with `privateLinkServiceId` = the account and `groupIds: ["blob"]` | SPEC-001 |
| `Microsoft.Storage/storageAccounts/blobServices` | `isVersioningEnabled: true`; `deleteRetentionPolicy.enabled: true`, `days` = `softDeleteDays` | SPEC-003 |
| Four `blobServices/containers` | names from the four parameters; `publicAccess: None` | SPEC-002 |
| `blobServices/containers/immutabilityPolicies` | name expression contains `legalContainerName`; `immutabilityPeriodSinceCreationInDays` = `legalRetentionDays`; `allowProtectedAppendWrites: false`; `condition` = `[parameters('deployLegalPolicy')]`; no lock parameter or property | SPEC-004 |
| Six `Microsoft.Authorization/roleAssignments` | Storage Blob Data Contributor at each of 3 ACE containers and 3 OCR containers; `principalType: ServicePrincipal`; no account-scope data role | SPEC-005 |

The role definition GUID is one ARM `variables` entry (`storageBlobDataContributorRoleId`); it is an Azure built-in role constant, not a business threshold (PA-08).

## 2. Environment parameter files

`azuredeploy.<env>.parameters.json` (`dev`, `sit`, `uat`, `prod`):

- `$schema` = `https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#`, `contentVersion` `1.0.0.0`.
- `parameters.<name>.value` for every required input: a decided value or exactly `__SET_BEFORE_APPLY__`.
- `deployLegalPolicy` = `true` in DEV, SIT, UAT; `false` in PROD.
- Any container-name parameter it sets is 3–63 and matches `^[a-z0-9]+(-[a-z0-9]+)*$`, and equals the matching `rwb.dochub.container.*` value (the conformance test compares against `application.yaml`; a mismatch is also fail-safe at runtime as `CONTAINER_MISSING:<name>`).

`azuredeploy.local.parameters.json` is synthetic: account `rwbconformance001`, location `conformance`, SKU `Standard_LRS`, tier `Hot`, subnet `/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rwb-conformance/providers/Microsoft.Network/virtualNetworks/rwb-conformance/subnets/private-endpoints`, principals `00000000-0000-0000-0000-000000000001` and `...0002`, `deployLegalPolicy` false. It is used only by T-TE012-15 and is refused by the check because `local` is not an allowed environment.

## 3. Blob naming and `BlobRef`

| Item | Rule | Source |
|---|---|---|
| Document blob name | `{caseId}/{documentId}/v{docVersion}`, UUIDs canonical lower-case; `docVersion` ≥ 1 | `[S]` §4 step 4, §11; D-RCV-31 |
| Intake blob name | Set by RWB-E1-026/E1-057; any 1–1024 characters not starting `/` | SPEC-010; `[E1-024]` step 1 |
| Container | 3–63 characters, `[a-z0-9-]`, not null | SPEC-010; Azure container naming |
| Blob name | 1–1024 characters, not starting `/` | SPEC-010; Azure blob naming |
| `BlobRef.storageRef()` | `container + "/" + blobName` | `[S]` §11; `[SCH]` `storage_ref varchar(400)` |
| `BlobRef.fromStorageRef(String)` | Split at the first `/`; each part validated; null, blank, no `/`, or over 400 characters → `IllegalArgumentException` | SPEC-010; `[SCH]` |
| Length bound | A document name is at most 149 characters with a 63-character container and 100 with the default names, so it fits `varchar(400)` | SPEC-010 |

The D-RCV-31 re-store uses the same target name `{caseId}/{documentId}/v{docVersion}` with `writeOnce=true` and the standard-container object at that same name as the source; the standard object is kept.

## 4. Published records (`dochub.api`)

| Type | Members | Invariants | Source |
|---|---|---|---|
| `DocumentStorage` | `StoredBlob store(BlobWriteRequest)`, `byte[] open(BlobRef)`, `StorageReadiness readiness()` | No Azure type; the only write path | SPEC-010 |
| `BlobRef` | `String container`, `String blobName`; `storageRef()`; `fromStorageRef(String)` | Field rules of §3; defensive validation in the compact constructor | SPEC-010 |
| `BlobWriteRequest` | `UUID caseId`, `UUID documentId`, `int docVersion`, `boolean writeOnce`, `BlobRef source` | `caseId` and `documentId` not null; `docVersion ≥ 1`; `source` not null and allowed by the source rule; violations are `IllegalArgumentException` before any storage call | SPEC-010, SPEC-011 |
| `StoredBlob` | `BlobRef ref`, `String sha256`, `long size`, `boolean existing` | `sha256` lower-case hex; `size` bytes; `existing` true only when the guard returned an existing write-once blob | SPEC-010, SPEC-012 |
| `StorageReadiness` | `boolean ready`, `List<String> reasons`, `Instant checkedAt` | `reasons` unmodifiable; `checkedAt` null when never evaluated | SPEC-010 |
| `WriteOnceViolationException` | `container`, `blobName` | No content or hash of content | SPEC-010; `[S]` X1 |
| `StorageUnavailableException` | `Reason reason`, `String container` | `Reason` = `NOT_READY`, `TIMEOUT`, `UNAVAILABLE`, `ACCESS_REFUSED`, `BLOB_MISSING` | SPEC-010 |

The source rule: intake (any name) is allowed for `writeOnce` true or false; the standard container is allowed only with `writeOnce=true` and `blobName` equal to the target name; legal, quarantine and unknown containers are refused. The target container is legal when `writeOnce=true`, standard otherwise.

## 5. Configuration properties

`DocumentStorageProperties` (`@ConfigurationProperties("rwb.dochub")`) has `boolean storageContainers`, `Storage storage` and `Container container`:

| Component | Key | Default | Validation |
|---|---|---|---|
| `storageContainers` | `rwb.dochub.storage-containers` | `${RWB_DOCHUB_STORAGE_CONTAINERS:false}` | Boolean |
| `storage.accountUrl` | `rwb.dochub.storage.account-url` | `${RWB_DOCHUB_ACCOUNT_URL:}` | Required and `https://` when flag on and emulator false |
| `storage.timeoutSeconds` | `rwb.dochub.storage.timeout-seconds` | `10` | 1–60 |
| `storage.readinessRecheckSeconds` | `rwb.dochub.storage.readiness-recheck-seconds` | `30` | 1–300 |
| `storage.serviceIdentityClientId` | `rwb.dochub.storage.service-identity-client-id` | `${RWB_DOCHUB_SERVICE_MI_CLIENT_ID:}` | Blank allowed (default managed identity) |
| `storage.ocrIdentityClientId` | `rwb.dochub.storage.ocr-identity-client-id` | `${RWB_DOCHUB_OCR_MI_CLIENT_ID:}` | Blank → readiness reason, not startup failure |
| `storage.emulator` | `rwb.dochub.storage.emulator` | `false` | Boolean |
| `storage.emulatorConnectionString` | `rwb.dochub.storage.emulator-connection-string` | absent in base, local placeholder | Only when emulator true; blank, wrong account or wrong host is a startup failure |
| `container.intake` | `rwb.dochub.container.intake` | `rwb-intake` | 3–63, pattern, distinct |
| `container.standard` | `rwb.dochub.container.standard` | `rwb-docs` | same |
| `container.legal` | `rwb.dochub.container.legal` | `rwb-docs-legal` | same |
| `container.quarantine` | `rwb.dochub.container.quarantine` | `rwb-quarantine` | same |

Cross-field rules: the four names are distinct; flag on and emulator false requires the URL; emulator false forbids the emulator string; emulator true forbids the account URL; emulator true requires the `local` profile, a non-blank string, account `devstoreaccount1` and host `127.0.0.1`, `localhost` or `azurite`. The profile rule is validated in `DocumentContainersConfig`; the others in the record.

## 6. Readiness state (in memory only)

Held by `StorageReadinessIndicator`; written only by `ContainerReadinessProbe`. Fields: state (`FLAG_OFF`, `NOT_EVALUATED`, `READY`, `NOT_READY`), reasons, `checkedAt`, the last probe's container/legal/identity detail maps, the single in-flight `CompletableFuture`, the last probe end time and the `Clock`.

| From | Event | Guard | To |
|---|---|---|---|
| (start) | Context starts | Flag off | FLAG_OFF |
| (start) | Context starts | Flag on | NOT_EVALUATED |
| NOT_EVALUATED | Probe ends | Four containers present; policy present or `EMULATED`; identities configured or `EMULATED` | READY |
| NOT_EVALUATED, READY or NOT_READY | Probe ends | Any check fails, unreachable, or the deadline passes | NOT_READY with reasons and `checkedAt` |
| NOT_READY | Probe ends | All checks pass | READY |
| READY | Probe ends | All checks pass | READY with `checkedAt` updated |
| NOT_EVALUATED | `ApplicationReadyEvent` | No probe in flight and none ended inside the window | Starts the probe; otherwise joins or starts none |
| NOT_EVALUATED | `store()` | No probe in flight | Caller starts the one probe and waits at most `timeout-seconds` |
| NOT_READY | `store()` | Probe result younger than `readiness-recheck-seconds` | Refused at once with NOT_READY, no storage call |
| NOT_READY | `store()` | Result older than the window | One probe starts or is joined; READY proceeds, NOT_READY refuses, TIMEOUT when the wait ends first |
| any | `store()` or `open()` ends in TIMEOUT, transport UNAVAILABLE or ContainerNotFound | No probe in flight and none ended inside the window | One background probe is requested; the state is unchanged until it ends |
| any | Any other operation outcome | — | No probe; the state is unchanged |
| any | Health read | — | No storage call; the state is unchanged |

`checkedAt` is the probe end instant, never an operation's outcome. The reason vocabulary is `FLAG_OFF`, `NOT_EVALUATED`, `CONTAINER_MISSING:<name>`, `LEGAL_POLICY_MISSING:<name>`, `IDENTITY_NOT_CONFIGURED:<name>`, `UNREACHABLE`.

## 7. Audit event `DOCUMENT_CHANGE_REFUSED`

| Field | Value | Source |
|---|---|---|
| `eventType` | `DOCUMENT_CHANGE_REFUSED` | FSD P5; SPEC-014 |
| `occurredAt` | UTC instant | `[S]` AC1 |
| `storageIdentity` | `ACE_SERVICE` or `SY_OCR` (role label) | `[S]` AC1, AC5; `[URP]` |
| `operation` | `WRITE` or `DELETE` | SPEC-013 |
| `documentId` | The UUID parsed from a document-form blob name; absent otherwise | FSD P5 |
| `actorId` | Authenticated principal subject; absent for system calls | FSD P5; `[PDPA]` §1 |
| `container`, `blobName` | As `BlobRef` | SPEC-014 |
| `reason` | `HASH_MISMATCH`, or `STORAGE_REFUSED` with the Azure error code | SPEC-012, SPEC-013 |
| `traceId` | Current trace ID when present | Observability baseline |

One structured line on logger `recovery.audit`; no content, no hash of another blob, no account URL, client ID or personal data.

## 8. Health component `documentHub`

| Detail | Values |
|---|---|
| status | Flag off `UNKNOWN`; READY `UP`; NOT_READY `DOWN`; NOT_EVALUATED `UNKNOWN` |
| `ready` | true or false |
| `containers` | Each configured name → `PRESENT`, `MISSING` or `UNVERIFIED` (flag on only) |
| `legalPolicy` | `PRESENT`, `MISSING` or `EMULATED` (flag on only) |
| `identities` | `CONFIGURED`, `NOT_CONFIGURED` or `EMULATED` (flag on only) |
| `reasons` | The reason vocabulary of §6 |
| `checkedAt` | The probe end instant; absent when never evaluated |

Not in the `liveness` or `readiness` group. Details only for RW-PLATADM (existing `show-details: when-authorized`). No account URL, key or client ID.

## 9. Pre-deploy check report

The check prints this on every outcome; the Builder evidence quotes the values:

```text
RESULT: ACCEPT | REFUSE
REASON: <stage-1 rule> | ROW <n>: <short text>
LEGAL CONTAINER: <legalContainerName value or the template default>
READ 1 COMMAND: <az command>
READ 1 OUTPUT: <raw output>
READ 1 ROW: <n>
READ 2 COMMAND: ...
READ 2 OUTPUT: ...
READ 2 ROW: <n>
READ 3 COMMAND: ...
READ 3 OUTPUT: <raw saved payload, or its path>
READ 3 ROW: <n>
DEPLOY COMMAND: az deployment group create --resource-group <rg> --template-file azuredeploy.json --parameters @<parameter file> deployLegalPolicy=<effective value> --mode Incremental
```

Only the reads that ran are printed. `DEPLOY COMMAND` is printed only on accept. The report and `legal-container.json` live in `reports/<environment>-<yyyyMMddTHHmmssZ>/` beside the script; the folder is not committed.

### 9.1 Output shapes of the three reads

| Read | Command | Accept shapes | Refuse shapes |
|---|---|---|---|
| 1 | `az storage account list --resource-group <rg> --query "[?name=='<account>'].name" --output json` | `[]` → row 1; `["<account>"]` → row 2 | Non-zero exit, another array length or name, unparsable output → row 7 |
| 2 | `az storage container-rm exists --resource-group <rg> --storage-account <account> --name <legal> --output json` | Object with `exists` boolean `false` → row 3; `true` → row 4 | Non-zero exit, missing or non-boolean `exists` → row 7 |
| 3 | `az rest --method get --url "/subscriptions/{subscriptionId}/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default/containers/<legal>?api-version=2026-09-01" --output-file <report folder>/legal-container.json` | Saved payload `properties.hasImmutabilityPolicy` boolean `false` → row 5; `true` (any state) → row 6 | Non-zero exit, no saved payload, missing or non-boolean property → row 7 |

Reads 1 and 2 shapes are the labelled assumption ASM-TE012-32; read 3 is the documented "Blob Containers - Get" response. Any unlisted output refuses, so a wrong assumption can only refuse an apply, never accept one.

## 10. Persistence and personal data

Nothing in §1–§9 is persisted by this story. No field holds personal data: container and blob names carry UUIDs; the audit event carries IDs, a role label, a reason and a trace ID; the health details carry container names and status words. Test data is random UUIDs and generated bytes; the Azurite key is generated per run and never committed.
