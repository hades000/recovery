# Preserved implementation — RWB-TE-001 (INC-002)

| Field | Value |
|---|---|
| Story | `RWB-TE-001` Recovery module folder and boundary test |
| Original run | 10 November 2026, recovery repository |
| Preserved on | 16 November 2026 |
| Status | Implemented — module boundary built and merged into ACE `develop-recovery` (MR !285, `7050e771`) |
| Baseline fit | The boundary rules BND-1..BND-5 are schema-independent and remain valid. The v2 baseline adds **BND-6** (no ACE `public` table read) from `RWB-E1-069`. |

## Evidence

| Path | Content |
|---|---|
| `report.md` | Implementation report |
| `backend/verification*.log` | Backend build and test logs |
| `backend/recoveryCoverageReport.xml` | JaCoCo coverage |
| `backend/test-results/*.xml` | Test results |
| `backend/jacoco-html/` | Coverage HTML |
| `frontend/*.log` | npm ci, typecheck, Vitest, mutation |
| `frontend/coverage-summary.json` | Frontend coverage |
| `unit-tests/report.md` | Unit-test report |
| `remediation-034.md` | Remediation record |

## What the v2 run adds

- The spec and plan are re-stated against the v2 baseline; the implementation evidence above is kept.
- `BND-6` is added to the boundary test in the plan as the E1-069 dependency.
- The module map stays at `backend/src/test/resources/architecture/recovery-modules.yaml`; it is not
  packaged in the jar (D-RCV-37).
- The access guard remains moved to `RWB-E1-022` (D-RCV-52, formerly D-RCV-36).
