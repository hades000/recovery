# Document gaps: RWB-TE-002 specify (remediation run 1)

RUN_ID `INC-004-epic-1-RWB-TE-002`, stage `specify`, 2026-11-17. SP-DG-01 to SP-DG-09 confirm the gate
reviewer's DG-01 to DG-09 (`review/document-gaps.md`) after re-checking the cited sources; SP-DG-10 is
new. Source paths are under `requirement/legacy/`. Precedence (RUN-BRIEF): D-RCV-35/36, ADR v3, Decision
Log v10, Story Files v7, older documents.

## Blockers

None.

## Non-blocking

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| SP-DG-01 (= review DG-01) | Story Files v7, RWB-TE-002 §3 (`04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md`) | Assumes a GitHub-format host "as ACE uses GitHub Copilot under DL32"; DL32 decides the coding tool, not the host. | Decision Log v10 DL32; D-RCV-50 ("MR"); this repository's `.gitlab-ci.yml`; L-RCV-12 | No | L-RCV-12 gives the GitLab equivalent; OPEN-038 confirms the ACE host. | `.gitlab/CODEOWNERS` (SPEC-001; ASM-TE002-01). |
| SP-DG-02 (= DG-02) | Story Files v7, RWB-TE-002 §7 AC1/AC2/AC4, §12 | Paths `ace-service/…`, `ace-web/…`, `db/migration/recovery/`, `/architecture/recovery-modules.yaml` do not match the agreed layout. | D-RCV-37 (module map path); D-RCV-10 (front end); RUN-BRIEF (migration folder `db/modulemigration/recovery/`) | No | Decisions settle the paths. | Repository paths (SPEC-002, -003; ASM-TE002-02). |
| SP-DG-03 (= DG-03) | Story Files v7, RWB-TE-002 §3, §4 step 3, §12, BR6 ("branch rule on main"); Architecture Decision Records v3 ADR-008; Engineering Practices v5 §4.1 | Protects `main` only; D-RCV-50 routes recovery MRs through `develop-recovery` then `develop`. | D-RCV-50; `project-context.md` §9; L-RCV-13 | No | L-RCV-13 applies the rule to all three branches. | SPEC-012, HC-01. |
| SP-DG-04 (= DG-04) | Story Files v7, RWB-TE-002 §1, §3, BR1; Engineering Practices v5 §4.2 | Owners are "the TechX tech leads"; D-RCV-21 and `backend-context.md` §2 say tech lead plus squad developers; DL36/DL37 unanswered in Decision Log v10. | D-RCV-21; Decision Log v10 DL36, DL37 | No | Handle from the story, membership from D-RCV-21; no person named. | ASM-TE002-03; OPEN-038. |
| SP-DG-05 (= DG-05) | Story Files v7, RWB-TE-002 §10 | ACE team alone approves the code owners file; BR4 and §12 make both teams owners. | Story Defects v4 row 91 (open); OPEN-041 | No | L-RCV-13: BR4 wins. | SPEC-005; ASM-TE002-07. |
| SP-DG-06 (= DG-06) | Recovery Workbench Test Cases v7, row TC-TE-002-08 (`09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md`) | Then-clause "Refused with MSG-P4-002; … the refusal is logged". | Story Files v7, RWB-TE-002 §16 ("no Workbench endpoint, so MSG-P4-002 is not shown") | No | Story files rank above the workbook. | HV-06 follows story §16. |
| SP-DG-07 (= DG-07) | Story Files v7, RWB-TE-002 BR3, AC2, AC3 | Assumes a common module folder exists. | Story Files v7 RWB-TE-001 (common packages assumed, DL05); Decision Log v10 DL05; OPEN-024; this repository has no `th/co/scb/ace/demo/common` path | No | DL05 and the TE-001 default root give the reserved pattern. | SPEC-004 reserved pattern; AC2/AC3 by resolver with synthetic paths. |
| SP-DG-08 (= DG-08) | Engineering Practices v5 §4.2 "Description"; AI Assisted Development Approach v1 §6 (`08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`) | The two sources list different MR fields (story key, ACs covered, AI first-pass summary vs story key, plan file, coding tool, reviewer, test results); Story Files v7 RWB-TE-002 is silent on an MR template. | `phase0-standards-audit.md` A-10 | No | The union breaks neither source. | SPEC-015 uses the union. |
| SP-DG-09 (= DG-09) | Engineering Practices v5 §10 (`11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`) | AGENTS.md owner "Solution architect with the tech leads" and pipeline-gate owner "TechX DevOps with SCB IT" have no repository handle. | Story Files v7 RWB-TE-002 §3 (handles for two teams only); Decision Log v10 DL36 | No | A marked placeholder plus an open item, as story §3 does for its two teams. | SPEC-017; `PROP-OI-1`. |
| SP-DG-10 (new) | Story Files v7, RWB-TE-002 §12 Entries (`/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads`, one line) | One line with two owners is satisfied by an approval from either owner under the host rule that story BR5 relies on, so the §12 entry does not make both teams review. | Story Files v7, RWB-TE-002 BR7 ("reviewed by both teams") and BR4 | No | BR4/BR7 state the intent; the contract line is the means. Rules win over the example line. | Two sections (SPEC-005; ASM-TE002-11); host effect HV-08. |

## Run 3 (2026-11-18): no new document gap

SG-017 and the re-alignment with RWB-TE-001 v4 were checked for document gaps under the RUN-BRIEF rule
(two citations that disagree, or one citation plus the place the answer is missing). None qualifies:

- SG-017 (which local record carries the MR text) concerns this repository's merge path (D-RUN-06), not
  the document set. The orchestrator's triage settles it (`AI-SDLC-BUILD-LOG.md` 2026-11-17T23:55:06),
  as review 3 also states ("Document gaps").
- The new `[Recovery module]` lines (`ModulithTest.java`, TE-001 fixture root and fixture maps,
  `frontend/eslint.config.js`) follow from story §1, §17, BR1 and BR2 and from RWB-TE-001 v4, a run
  artefact. The document set is silent on these local file names because they are local layout, not
  because an answer is missing: story §12 uses `<ACE base path>` placeholders (SP-DG-02 already covers
  the path mapping). Recorded as assumption ASM-TE002-18, not as a gap.

SP-DG-01 to SP-DG-10 are unchanged. Blockers: none.

