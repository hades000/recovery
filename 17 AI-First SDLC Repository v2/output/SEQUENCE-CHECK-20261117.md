# Sequence check — 17 November 2026

Scope: confirm the next two items to take through Technical Specifier and Implementation Planner in the
v2 repository. No code is built in this run.

## 1. Where the sequence stands

Source: `docs/increments/build-sequence.md` (Build Sequence v6, 16 November 2026) and
`docs/increments/INDEX.md`.

| Order | Key | Status before this run | Why it is or is not next |
|---:|---|---|---|
| 1 | `RWB-E1-044` | Planned — historical | Spec and plan are the 10 November carry-over; re-baseline is `OPEN-036` and is not a build-ready item. |
| 2 | `RWB-TE-001` | Implemented | Dependency for TE-002 and TE-003 is done. |
| 3 | `RWB-E1-042` | Implemented | Done. |
| **4** | **`RWB-TE-002`** | **Ready for specify** | **Depends on TE-001 only; next unplanned item whose dependency is done.** |
| **5** | **`RWB-TE-003`** | **Ready for specify** | **Depends on TE-001 only; second unplanned item whose dependency is done.** |
| 6 | `RWB-TE-011` | Ready for specify | Next after TE-002/TE-003. |
| 8 | `RWB-E1-043` | Planned — historical | Re-baseline is `OPEN-036`; not build-ready. |

**Decision:** specify and plan `RWB-TE-002` (INC-004) and `RWB-TE-003` (INC-005). Do not start
`RWB-TE-011` or any later item in this run.

## 2. Sequence conflicts found and how this run handles them

| ID | Conflict | Handling |
|---|---|---|
| `SEQ-01` | TE-002 references `ace-service/...` and `ace-web/...` placeholders; the actual ACE layout from TE-001 is `backend/src/main/java/th/co/scb/ace/demo/recovery/`, `backend/src/test/java/th/co/scb/ace/demo/recovery/`, `backend/src/main/resources/db/modulemigration/recovery/`, `frontend/src/modules/recovery/`, and `backend/src/test/resources/architecture/recovery-modules.yaml`. | The TE-002 spec maps the contract to the actual paths. Story placeholders are not copied into the plan. |
| `SEQ-02` | TE-002 says GitHub-format `.github/CODEOWNERS` and a branch rule on `main`; ACE CI evidence in TE-001 is `.gitlab-ci.yml`, and D-RCV-50 routes recovery MRs through `develop-recovery`. | The spec uses the story's GitHub-compatible contract and adds `develop-recovery`/`develop` to the protected branches so no recovery MR bypasses code-owner review. The repository host is a build precondition (`OPEN-038`). |
| `SEQ-03` | TE-003 is build order 5, before any controller exists, but AC5 fails the build when a current E1 operation has no implementation. The story's own "Done when" allows an E1 operation to be **pending with a named story**. | The spec introduces a versioned implementation baseline (`L-RCV-11`): an E1 operation is pending with its owning story until that story flips it to enforced; AC5 is proven with a fixture operation that is in the baseline and has no controller. The live E1 build is not failed by the 73 not-yet-built operations. `OPEN-039` records the plan-gate acceptance. |
| `SEQ-04` | TE-003's business rationale cites FSD `AC-P2-001-01`, but that AC is the outbound file-interface contract test (INT-25), not the API contract test. | The spec treats the API contract requirement as the story's BR1/BR3 and REQ-DRI-007; it does not claim `AC-P2-001-01` as the API contract source. |
| `SEQ-05` | TE-003 says 79 API operations; API Specification v4 has 141 operationIds (73 E1, 38 E2, 8 E3, 10 E4, 8 E5, 4 E6). | The lint and contract suite read the file, not a fixed count. The E1 build selects 73 operations. The count delta is recorded as an assumption/open item. |
| `SEQ-06` | TE-003 needs generated packages listed in the TE-001 module map, but the TE-001 map has no shared generated package. TE-001's own spec notes this must be extended in TE-003. | The TE-003 spec adds `generated.web` and `generated.model` to the P2 `integration` `published` list, so no 20th module is created, and plans the package-info/boundary-rule update (`L-RCV-14`). |
| `SEQ-07` | TE-003's live access test `TC-TE-003-09` needs roles and the permission matrix from E1-022/E1-037, which are later in the sequence. | The harness and fixture-level negative test are built now; the live access case is `BLOCKED` until E1-022/E1-037 (`OPEN-040`). No mocked role is recorded as passing. |
| `SEQ-08` | TE-003's access suite assumes every operation has a capability area; two E1 operations (`getFeatureFlags`, `getMeSession`) declare `x-capability.area: None`. | The spec treats them as authentication-only: `NOT_APPLICABLE_AUTHENTICATED` plus a 401 test, never a 403 pass. `OPEN-042` asks the API owner to confirm or assign an area. |

## 3. Outputs of this run

| Story | RUN_ID | Specification | Plan |
|---|---|---|---|
| `RWB-TE-002` | `INC-004-epic-1-RWB-TE-002` | `output/INC-004-epic-1-RWB-TE-002/specify/` | `output/INC-004-epic-1-RWB-TE-002/plan/` |
| `RWB-TE-003` | `INC-005-epic-1-RWB-TE-003` | `output/INC-005-epic-1-RWB-TE-003/specify/` | `output/INC-005-epic-1-RWB-TE-003/plan/` |

Both runs follow the no-question rule (`L-RCV-03`). Ambiguities are in each run's `assumptions.md`;
items that need a human owner are in `docs/open-items.md` (`OPEN-038` to `OPEN-042`).
