# Data model — RWB-TE-001

No database object, no Flyway migration, no business field (spec §Data and migration, story §11). The only data artefacts are the module map and the fixture maps, both test resources, never packaged in the boot jar.

## 1. Module map — `backend/src/test/resources/architecture/recovery-modules.yaml`

Source: SPEC-RWB-TE-001-002; field rules from spec §Field-level behaviour matrix; contract `CON-RWB-TE-001-001`. Initial content (TASK-RWB-TE-001-03):

```yaml
# Recovery module map (RWB-TE-001, D-RCV-37). Source of truth for module names,
# packages, published packages and client permissions (BR6). Changes need code-owner approval (D-RCV-21).
rootPackage: th.co.scb.ace.demo.recovery
modules:
  - { code: P1,  name: dataengine,  published: [api], clientPackages: [] }
  - { code: P2,  name: integration, published: [api], clientPackages: [adapter] }
  - { code: P3,  name: casewf,      published: [api], clientPackages: [] }
  - { code: P4,  name: access,      published: [api], clientPackages: [] }
  - { code: P5,  name: dochub,      published: [api], clientPackages: [] }
  - { code: P6,  name: comms,       published: [api], clientPackages: [] }
  - { code: P7,  name: decision,    published: [api], clientPackages: [] }
  - { code: P8,  name: payments,    published: [api], clientPackages: [] }
  - { code: P9,  name: reporting,   published: [api], clientPackages: [] }
  - { code: P10, name: agent,       published: [api], clientPackages: [client] }
  - { code: S1,  name: valuation,   published: [api], clientPackages: [] }
  - { code: S2,  name: treatment,   published: [api], clientPackages: [] }
  - { code: S3,  name: guarantee,   published: [api], clientPackages: [] }
  - { code: S4,  name: litigation,  published: [api], clientPackages: [] }
  - { code: S5,  name: asset,       published: [api], clientPackages: [] }
  - { code: S6,  name: debtsale,    published: [api], clientPackages: [] }
  - { code: S7,  name: writeoff,    published: [api], clientPackages: [] }
  - { code: S8,  name: deviation,   published: [api], clientPackages: [] }
  - { code: S9,  name: partner,     published: [api], clientPackages: [] }
external:
  - { name: common,     rootPackage: th.co.scb.ace.demo.common,     published: [api] }  # story §3, DL05
  - { name: collection, rootPackage: th.co.scb.ace.demo.collection, published: [api] }  # CLAR-004 A, OPEN-024
clientLibraries:
  - java.net.http
  - java.net.HttpURLConnection
  - java.net.Socket
  - java.net.URL
  - org.springframework.web.client
  - org.springframework.web.reactive.function.client
  - org.apache.hc
  - org.apache.http
  - okhttp3
  - com.jcraft.jsch
  - org.apache.sshd
  - net.schmizz.sshj
  - org.apache.commons.net
  - com.azure.storage
  - org.springframework.kafka
  - org.apache.kafka
```

The flow style above is a readability choice; block style is equally valid. Builder keeps the values exactly.

### Field rules (enforced by `ModuleMapLoader`, SPEC-003)

| Field | Required | Rule | Error text names |
|---|---|---|---|
| `rootPackage` | yes | One valid Java package name | file + `rootPackage` |
| `modules[].code` | yes | Unique; `^(P([1-9]\|10)\|S[1-9])$` | file + `modules[i].code` |
| `modules[].name` | yes | Unique; `^[a-z][a-z0-9]*$`; package = `rootPackage.name` | file + `modules[i].name` |
| `modules[].published` | yes, ≥1 | Unique within module; `^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)*$`; never `internal` or `internal.*` | file + `modules[i].published[j]` |
| `modules[].clientPackages` | yes (may be `[]`) | Same pattern; a permission, package need not exist | file + `modules[i].clientPackages[j]` |
| `external[]` | yes | Entries `common` and `collection` both present; `rootPackage` valid; `published` ≥1 | file + `external[i].<field>` |
| `clientLibraries` | yes, ≥1 | Unique; package name or fully qualified class name; matched on a name boundary (SPEC-009) | file + `clientLibraries[k]` |
| any other key | — | Unknown field → error | file + key path |

### Immutable model (test scope, `th.co.scb.ace.demo.recovery.architecture`)

```text
ModuleMap(String rootPackage, List<Module> modules, List<External> external, List<String> clientLibraries)
Module(String code, String name, List<String> published, List<String> clientPackages)   // packageName() = root + "." + name
External(String name, String rootPackage, List<String> published)
```

## 2. Fixture maps — `backend/src/test/resources/architecture/fixtures/`

Same schema, `rootPackage` under `th.co.scb.ace.recoveryfixture` (outside `th.co.scb.ace.demo`, see plan §Plan-time verification). One map per rule scenario (TASK-RWB-TE-001-07) and one invalid file per loader error under `fixtures/loader/` (TASK-RWB-TE-001-05). Content: package and class names only.

## 3. Frontend

No data model. The import allow-list is configuration (`frontend/eslint.config.js`, contract `CON-RWB-TE-001-F01`).
