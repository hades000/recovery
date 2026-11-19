# Run brief for every lifecycle agent in this repository

Read this before you start. It adapts the AISDLC v2 agent instructions to this repository's layout.
It does not change any gate, rule or output name in your instructions.

## Paths

| Name in your instructions | Path here |
|---|---|
| Workspace root (`.github/`, `docs/`, `requirement/`, `output/`) | `<repo>/aisdlc/` |
| ACE monorepo / code repository / `ace-monorepo/` | `<repo>/` (this repository's root; local stand-in for ACE) |
| `ace-monorepo/AGENTS.md`, coding standard | `<repo>/AGENTS.md`, `<repo>/aisdlc/.github/contexts/backend-standards.md`, `frontend-standards.md` |
| `requirement/legacy/` (the converted document set v14) | `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` (read only) |
| Story file paths in the increment cards | relative to `<docset>/17 AI-First SDLC Repository v2/` |
| Earlier v2 artefacts for your story, if any | `<repo>/aisdlc/output/<RUN_ID>/_v2-baseline/` (history: reuse what is still correct, never overwrite) |

`<repo>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench`.
`<docset>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14`.

## Hard rules for this run

1. **Never change anything in `<docset>` outside `<repo>`.** The document set is read only. A
   document that is wrong or silent is recorded as a gap (below), never edited.
2. **Write only to your own stage folder**, `aisdlc/output/<RUN_ID>/<stage>/`. The Implementation Builder
   also writes code, and only in the git worktree it is given.
3. **Shared files are not yours.** Do not edit `aisdlc/docs/open-items.md`,
   `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/increments/INDEX.md`, the increment cards
   or `aisdlc/DOCUMENT-GAPS.md`. Agents run in parallel. Write the rows you would add to
   `aisdlc/output/<RUN_ID>/<stage>/shared-updates.md`, and the orchestrator applies them in order.
   The Traceability Manager is the exception: it may edit `Traceability_Matrix.md`.
4. **No question to the user** (L-RCV-03). Record assumptions in your stage's `assumptions.md`.
5. **No Jira, Confluence, GitLab or Figma MCP is connected.** Follow your instructions' fallback
   paths, record `N/A` with the reason, and keep going. Playwright runs through the project's own
   `npx playwright` in `frontend/`.
6. **Subagents.** If you can spawn `compliance-reviewer` (or `figma-extractor`), do so where your
   instructions say to. If the Agent tool is not available to you, write your stage outputs, set
   `GATE_REVIEW: PENDING_ORCHESTRATOR` in your report, and the orchestrator runs Compliance Reviewer
   as the bounded gate review.
7. **No personal data** anywhere: no real names, ID numbers, account numbers or addresses in specs,
   tests or fixtures. Use synthetic values.
8. Cite sources by **document name and version** (and section or sheet), plus the `requirement/legacy/`
   path. Quote at most a short phrase.

## Document gaps (every stage records them; the specifier first)

When the document set is silent where the story needs an answer, or two sources disagree, record it
in `aisdlc/output/<RUN_ID>/<stage>/document-gaps.md`:

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|

- Record a gap only with evidence: two citations that disagree, or one citation plus the place the
  answer should be and is not. Never record a guess.
- **Blocker = Yes** only when no precedence rule or documented default lets the story proceed. The
  precedence is: client decisions D-RCV-35 and D-RCV-36 (`aisdlc/docs/decisions/`), then ADR v3,
  then Decision Log v10, then story files v7, then older maps and drafts.
- If the precedence settles it, apply it, say so, and mark Blocker = No.

## Local stack facts (verified 17 Nov 2026)

- Backend: Spring Boot 4.1.2, Java 21, Gradle Kotlin DSL, Spring Modulith 2.1.1, Jackson 3, Temporal
  Java SDK, embedded Drools, Azure Blob SDK, Quartz (in memory locally). Package
  `th.co.scb.ace.demo.recovery` with nested modules `platform`, `rules`, `workflow`, `documents`, each
  with `api/` and `internal/`.
- Recovery migrations: `backend/src/main/resources/db/modulemigration/recovery/`, run by the recovery
  Flyway bean (`RecoveryFlywayConfig`, history table `flyway_schema_history_recovery`, placeholder
  `${recoverySchema}`, clean disabled). The folder is empty today. The local database is built at
  init from Physical Schema v6 while `RWB_LOAD_REFERENCE_SCHEMA=true` (see `README.md`).
- Database roles (ADR-010): `rwb_migrator` (Flyway), `recovery_svc` (application: SELECT on the
  `v_ace_*` views, no access to `public`), `ace_view_owner`, `temporal_svc`. The init scripts are in
  `infra/postgres/init/`.
- Frontend: React 19, Vite 8, TypeScript 5.9, TanStack Query, i18next (Thai default), Tailwind,
  `openapi-fetch` with types generated from `api/recovery-api-v4.yaml` into
  `frontend/src/api/schema.d.ts`. The recovery module is in `frontend/src/modules/recovery/`, and
  ESLint enforces the D-RCV-39 import allow-list.
- Tests: `./scripts/dev.ps1 test` (unit, Modulith, boundary, migration lint, Vitest with 80%
  coverage), `it` (Testcontainers, tag `recovery-it`), `e2e` (REST Assured tag `e2e`, plus Playwright).
  Gradle in this workstation needs
  `$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"`.
- Local deviations already decided are listed in `README.md`, "Decisions taken while setting this up".
  Do not report them again as new findings. Cite them where they apply.
- **What already exists is baseline, not scope to rebuild.** `aisdlc/evidence/phase0-standards-audit.md`
  lists what the platform baseline already provides (A-04) and which gaps your story owns (Owner
  column). Specify and plan against the code as it is: extend or correct it, never duplicate it.
- **Migration numbers (D-RUN-07).** Never fix a migration number in a spec, plan or file name.
  D-RCV-28 makes `<seq>` the next four-digit number in merge order, and the orchestrator assigns it at
  merge. Use the placeholder `V<seq>__<story>_<name>.sql` until then. The lint requires a contiguous
  sequence from V0001.
- **Dependencies (D-RUN-08).** Depend only on what exists in this repository or what an earlier story
  in Build Sequence v6 delivers. Name work owned by a later story as a seam that is out of scope.
- `aisdlc/.github/rules/architectural-standards.md` is the toolkit's generic template (Flutter,
  `/api/v1`, `AUTH-XXX`). Where it conflicts with `aisdlc/.github/contexts/`, the contexts win.

## Your report back

End with: `STATUS`, the files written, the gate result (or `GATE_REVIEW: PENDING_ORCHESTRATOR`), the
document gaps (blockers first), and `NEXT_STEP`. Keep it under 300 words.
