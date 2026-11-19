# Assumptions — RWB-TE-003 specification

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-TE003-01` | The ACE repository holds the canonical OpenAPI file at `api/recovery-api.yaml`; the document-set copy is the source. | Story §3; API Specification v4. | Drift is a contract defect; the plan adds a byte-equality check. |
| `ASM-TE003-02` | The build can run the OpenAPI generator and the front-end generator in the existing Gradle/Nx build. | TE-001 evidence; story §3. | New dependency versions are pinned at the plan gate; no new runtime service. |
| `ASM-TE003-03` | Every E1 operation has an owning story; `api/recovery-api-implementation.yaml` is the versioned baseline. | Build Sequence v6; story §13. | A missing row is a lint failure; no operation is silently pending. |
| `ASM-TE003-04` | The permission matrix seed is available; until E1-037, a synthetic RW-REFADM fixture is used for the harness. | Story §3; RWB-E1-037. | The live access case stays blocked; no mocked role is recorded as passing. |
| `ASM-TE003-05` | Generated interfaces use the operationId as the Java method name, one interface per tag. | OpenAPI Generator `spring`; story §12. | The implemented-operation resolver changes; the contract does not. |
| `ASM-TE003-06` | Generated packages are P2 `integration` published packages `generated.web`/`generated.model`, not a new root module. | TE-001 map; D-RCV-37; L-RCV-14. | A root `recovery.generated` needs a 20th module and a map-schema change. |
| `ASM-TE003-07` | `warnAt` is already in API v4 `Timer`; AC1 uses a minimal fixture and the live generated model also has it. | API Specification v4 line 6602. | AC1 evidence is fixture-only; the live type still contains `warnAt`. |
| `ASM-TE003-08` | New build/test/runtime dependencies need plan-gate approval and pinned versions. | `AGENTS.md` §4.4; README known limits. | The plan gate rejects the dependency and the story is re-planned. |
| `L-RCV-03` | No question was asked; sequencing, count and package ambiguities are recorded here and in `docs/open-items.md`. | No-question rule. | A wrong default is visible at the plan gate. |

No question was asked. Items that need a human owner are in `docs/open-items.md` (`OPEN-039`, `OPEN-040`,
`OPEN-041`).
