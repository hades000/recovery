# Assumptions — RWB-TE-003 plan

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-TE003-01` | `api/recovery-api.yaml` is the canonical repository copy and byte-equal to the document-set v4 file. | Story §3; API v4. | Drift is a contract defect; PRE-2 and the lint block. |
| `ASM-TE003-02` | The existing build can run the OpenAPI generator and the front-end generator. | TE-001 evidence; story §3. | Pinned versions at PRE-3; no new runtime service. |
| `ASM-TE003-03` | Every E1 operation has an owning story; 73 baseline rows. | Build Sequence v6. | A missing row is a lint failure; no silent pending. |
| `ASM-TE003-04` | A permission matrix seed exists; until E1-037 a synthetic RW-REFADM fixture is used. | Story §3; E1-037. | The live access case stays blocked; no mocked pass. |
| `ASM-TE003-05` | operationId = Java method name; one interface per tag. | OpenAPI Generator `spring`; story §12. | The resolver changes; the contract does not. |
| `ASM-TE003-06` | Generated packages are P2 `integration` published `generated.web`/`.model`. | TE-001 map; D-RCV-37; L-RCV-14. | A root `recovery.generated` needs a 20th module. |
| `ASM-TE003-07` | `warnAt` is already in v4 `Timer`; AC1 uses a fixture and the live type also has it. | API v4 line 6602. | AC1 evidence is fixture-only; the live type still contains `warnAt`. |
| `ASM-TE003-08` | Dependencies are pinned and approved at PRE-3. | `AGENTS.md` §4.4. | The plan gate rejects the dependency and the story is re-planned. |
| `ASM-TE003-09` | `x-capability.area: None` is authentication-only; `getFeatureFlags` and `getMeSession` use it. | API v4; BR4; `OPEN-042`. | The API owner assigns a real area or confirms the exception; the suite does not record a 403 pass. |
| `L-RCV-03` | No question was asked. | No-question rule. | A wrong default is visible at the plan gate. |

No question was asked. Open items: `OPEN-039` (API file, versions, baseline, packages), `OPEN-040`
(live access case), `OPEN-041` (canonical defect closure).
