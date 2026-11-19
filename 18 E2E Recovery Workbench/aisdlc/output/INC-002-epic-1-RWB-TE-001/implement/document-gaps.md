# Document gaps: RWB-TE-001 (implement stage)

No new document gap was found while implementing. The plan-stage gaps carried into this stage, with
the precedence that settled them:

| Local ID | Document (name, version, section) | Gap or conflict | Second source | Blocker? | Why | How this stage proceeded |
|---|---|---|---|---|---|---|
| PG-04 / GC-1 (carried from `../plan/document-gaps.md`) | AGENTS.md v2 §7 and §9 ("touches one module") vs story v7 / `../specify/spec.md` §13 (19 nested design modules) | "Module" can mean the ACE module or a nested design module | `AI-SDLC-BUILD-LOG.md` decision D-RUN-21 (18 Nov 2026, orchestrator) reads it as the ACE module; open item OPEN-050 records the pending ratification | No | D-RUN-21 is the build-level decision and the plan's PA-12 applies it | Applied D-RUN-21: the story touches the recovery ACE module only. The 19 nested modules are created inside it. |
| DG-01 (carried) | `contracts/backend-apis.json` `publishedTypesInitial` vs TASK-09's text "publishedJavaTypesAfterRelocation" | The contract key has a different name from the plan's reference | The contract content is the same list; the plan's reference is a wording slip | No | The list is unambiguous and was used as the assertion | `RecoveryBoundaryTest.publishedSurfaceIsExactlyTheSpecifiedTypes` asserts the contract's list exactly. |
| DG-02 (new, non-blocking) | `backend/build.gradle.kts` `dependencyManagement` imports `spring-modulith-bom:${property("springModulithVersion")}` while the version is declared as `extra["springModulithVersion"]` | The property form is unusual but resolves today | `./gradlew` resolves Modulith 2.1.1 (baseline capture) | No | Not exercised by this story; no build change is in scope | Left unchanged; the builds pass. |
