# Test scenarios — RWB-E1-042

| ID | Given | When | Then | AC / Rule |
|---|---|---|---|---|
| `T-042-01` | `case.entry.dpd` is 90 in UAT | The entry decision runs | The decision reads 90 and records parameter version 1 | AC1 |
| `T-042-02` | A fixture class holds `if (dpd > 90)` | `RwbMagicNumberCheck` runs | The build fails naming file, line and `case.entry.dpd` | AC2 |
| `T-042-03` | A fixture reads `case.new.key` not in the CSV | `CatalogCompletenessCheck` runs | The build fails naming the key | AC3 |
| `T-042-04` | `case.entry.dpd` has no value and no default in UAT | The service starts | Readiness fails with `MSG-P3-032` naming key and UAT; no traffic | AC4 |
| `T-042-05` | `case.entry.dpd` is 1..365 | A load writes 366 | The load is refused whole with min 1 and max 365 (`MSG-GEN-002`) | AC5 |
| `T-042-06` | The key is INTEGER | A load writes `ninety` | The load is refused with `MSG-P1-002` | AC6 |
| `T-042-07` | U-41 authored version 3 | U-41 approves version 3 | 409 `MSG-P7-002`; value not approved | AC7 |
| `T-042-08` | The same key has SIT 90 and PROD 60 | Each environment reads | SIT returns 90, PROD returns 60 | AC8 |
| `T-042-09` | `ace.db.password` is a secret | The catalog is read | The row is listed with owner, environments, usedBy; no value | AC9 |
| `T-042-10` | Version 1 is approved, then version 2 | Rollback version 2 | Version 1 and its value are in force; decision log records it | AC10 |
| `T-042-11` | Version 2 is approved with `validFrom` tomorrow | A read today, then tomorrow | Today returns version 1; tomorrow returns version 2 without restart | AC11 |
| `T-042-12` | A new key is requested | The build runs | The key must be added to the CSV by a reviewed PR; a runtime load cannot add it | BR3, Flow 2 |
| `T-042-13` | V0001 already created both tables | V0042 runs | Only missing constraints/FK/indexes are added; no error | Migration |
| `T-042-14` | V0042 already applied | V0042 runs again | No change; no error | Migration |
| `T-042-15` | No Docker in the build agent | `recoveryIntegrationTest` runs | The task fails, not skips (D-RCV-28 (3)) | Test rule |
| `T-042-16` | The decision-log write fails | Approval is attempted | The approval rolls back; 503 | ADR-009 |

## Test data

| Key | Environment | Value | Purpose |
|---|---|---|---|
| `case.entry.dpd` | UAT | 90 | AC1 |
| `case.entry.dpd` | PROD | 60 | AC8 |
| `case.entry.dpd` | SIT | 90 | AC8 |
| `ace.db.password` | UAT | secret | AC9 |
| `temporal.namespace` | UAT | `rwb-recovery` | v2 parameter |
| `rules.testcases.min` | UAT | 50 | v2 parameter |

All values synthetic. No production data, no personal data.

## Evidence

| Test class / file | Output |
|---|---|
| `ParameterServiceTest` | `implement/backend/test-results/` |
| `ParameterLoadChecksTest` | same |
| `ParameterApprovalServiceTest` | same |
| `ParameterStartupCheckTest` | same |
| `RwbMagicNumberCheckTest` | same |
| `CatalogCompletenessCheckTest` | same |
| `tests/test_migrations.sh` | `implement/evidence/migration-test-output.txt` |
| JaCoCo | `implement/backend/recoveryCoverageReport.xml` |
