# Document gaps: RWB-TE-003 spec gate round 2 (INC-005-epic-1-RWB-TE-003, review stage)

These are candidate gaps for the orchestrator to number into `aisdlc/DOCUMENT-GAPS.md`. The document set was not edited. They add to the gaps in `review/document-gaps.md` (TE003-SG-DG-01..08) and `specify/document-gaps.md` (TE003-SP-DG-01..06).

- **Paths.** Legacy paths are relative to `17 AI-First SDLC Repository v2/requirement/legacy/`.
- **Story citations.** "E1-071 v7" is `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-071-temporal-worker-and-sdk-in-the-recovery-module-v1.md`.
- **Finding IDs.** `SG3-nn` refers to a finding in `spec-gate-review-2.md`.

**Precedence applied:** D-RCV-35 and D-RCV-36, then ADR v3, then Decision Log v10, then story files v7, then older documents (`RUN-BRIEF.md`).

**Blockers: 0.**

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| TE003-SG3-DG-01 | Story file v7, RWB-E1-071 v1, §5 X6 ("A role without Platform administration U") and §16 TC-E1-071-08 | The story gives right U for refusal on the admin smoke endpoint. | API Specification v4 (`05-technical-architecture/recovery-workbench-api-specification-v4.yaml`), `postAdminWorkflowsSmoke` `x-capability` right C. `TemporalAdminController.java:91` also comments "right C". | No | RWB-TE-003 v7 BR1 makes the OpenAPI file the only source of endpoints, so the TE-003 access suite reads the right from API v4. Whether RW-CASEOWN lacks C needs the RWB-E1-037 matrix (OPEN-040). | Finding SG3-04: the fixture row needs its own cited source. The gap goes to the BA for E1-071 alignment. |
| TE003-SG3-DG-02 | Story file v7, RWB-E1-071 v1, §4 step 9 (the response gives "workflow ID, run ID and status") | The story's smoke response fields differ from the API. | API Specification v4, `postAdminWorkflowsSmoke` 202 inline schema: `workflowId` and `workflowType` only. The code returns the same two fields (`TemporalAdminController.java:133`). | No | TE-003 v7 BR1: the API file governs the contract. The SPEC-014 retrofit keeps the API v4 shape. | Accepted in the spec (SPEC-014). The gap goes to the BA and API owner for E1-071. |
| TE003-SG3-DG-03 | Local decisions D-RCV-28 (3) and D-RCV-40 (`aisdlc/docs/decisions/INC-001-decisions.md`): JaCoCo checks run "outside `check`" | The decisions keep coverage verification out of the build gate. | `aisdlc/evidence/phase0-standards-audit.md` A-09 (coverage verification job missing, owner RWB-TE-003/RWB-TE-011). `README.md` "Coverage verification … not yet part of `check`. Add it once the first story's code lands". TE-001 v3 SU-10 hands CI wiring to TE-003. | No | D-RCV-05 forbids a pipeline change. The recovery tech lead can supersede or confirm the "outside `check`" clause. The story's functional scope does not depend on it. | Finding SG3-01 requires a decision request in `shared-updates.md`. SPEC-017 is made conditional on that decision. |
