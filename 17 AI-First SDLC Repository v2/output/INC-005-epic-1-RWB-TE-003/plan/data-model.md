# Data model — RWB-TE-003

No database, no entity and no migration. The data artefacts are the API contract, the E1 enforcement
baseline, the report and the generated package map.

## 1. API operation

Source: `api/recovery-api.yaml` (OpenAPI 3.1, API Specification v4).

| Field | Type | Source | Meaning |
|---|---|---|---|
| `operationId` | string | `paths.*.{method}.operationId` | Unique; Java method name in the generated interface. |
| `method`, `path` | string | `paths` | HTTP operation. |
| `x-module` | string | extension | P1–P10 or S1–S9. |
| `x-capability.area` | string | extension | Capability area used by the access suite; `None` means authentication-only. |
| `x-capability.right` | string | extension | `R`, `C`, `U`, `D` or `A`. |
| `x-first-release` | string | extension | E1–E6. |
| `responses` | map | `responses` | At least one 4xx/5xx; each resolves to `Problem`. |

Counts: 141 operations; 73 E1, 38 E2, 8 E3, 10 E4, 8 E5, 4 E6.

## 2. E1 enforcement baseline

File: `api/recovery-api-implementation.yaml`.

```yaml
release: E1
operations:
  - operationId: getCases
    story: RWB-E1-002
    enforce: false
  - operationId: getCasesCaseidTimers
    story: RWB-E1-028
    enforce: false
  # ... 73 E1 rows
```

| Field | Type | Constraint |
|---|---|---|
| `release` | string | `E1` for this baseline. |
| `operationId` | string | Must exist in the spec; unique; exactly one row per E1 operation. |
| `story` | string | Must exist in the story manifest; the story that owns the controller. |
| `enforce` | boolean | `true` only when the controller is in the same MR; initially `false`. |

Rules:

- A missing E1 row is a lint failure.
- A non-E1 row in the E1 baseline is a failure.
- `enforce: true` with no controller → `{operationId} has no implementation`.
- A controller method for an operation with no row → `operation not in baseline`.
- An E1 operation with `enforce: false` → `PENDING` with its story in the report.

## 3. Report

File: `build/reports/recovery-contract/contract-report.json` and `.md`.

```json
{
  "release": "E1",
  "generatedAt": "2026-11-17T10:00:00Z",
  "operations": [
    {
      "operationId": "getCasesCaseidTimers",
      "release": "E1",
      "story": "RWB-E1-028",
      "status": "PENDING",
      "contract": "NOT_RUN",
      "access": "NOT_RUN",
      "reason": "pending: story not yet merged"
    }
  ],
  "summary": {"passed": 0, "failed": 0, "pending": 73}
}
```

No request/response body, personal data or token is written. The report carries operationIds, stories,
statuses and failure text only.

## 4. Generated packages and module map

| Item | Value |
|---|---|
| Server interfaces | `th.co.scb.ace.demo.recovery.integration.generated.web` (one per tag) |
| Server models | `th.co.scb.ace.demo.recovery.integration.generated.model` |
| `@NamedInterface` | `generated.web`, `generated.model` on the generated `package-info.java` |
| Module map | P2 `integration` `published` gains `generated.web` and `generated.model` |
| New module | None; P2 remains one of the 19 nested modules |
| Front end | `frontend/src/modules/recovery/api/generated/schema.d.ts`, `client.ts` (gitignored) |

## 5. Test-support classes

| Class | Package | Data |
|---|---|---|
| `OperationCatalog` | `recovery.contract` | The 141 operations, grouped by release. |
| `ContractBaseline` | `recovery.contract` | The 73 E1 rows; enforced/pending/story. |
| `ImplementedOperationResolver` | `recovery.contract` | Controller beans and generated interface methods. |
| `ContractFixtures` | `recovery.contract` | Synthetic request/response per operation. |
| `RecoveryContractTest` | `recovery.contract` | Parameterised over enforced operations. |
| `RecoveryAccessContractTest` | `recovery.contract` | Parameterised over enforced operations and roles. |
| `RecoveryApiReport` | `recovery.contract` | Build report. |

No class reads another module's tables; the fixtures are in memory.
